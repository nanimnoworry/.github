#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "profile" / "public-surface-contract.json").read_text(encoding="utf-8"))
PROFILE = (ROOT / "profile" / "README.md").read_text(encoding="utf-8")
ORG = CONTRACT["organization"]
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "nanimnoworry-public-surface-validator",
}

def fail(message: str) -> None:
    raise AssertionError(message)

def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.status != 200:
            fail(f"HTTP {response.status}: {url}")
        return response.read().decode("utf-8")

def fetch_json(url: str) -> dict:
    return json.loads(fetch_text(url))

def require(text: str, phrases: list[str], where: str) -> None:
    low = text.lower()
    for phrase in phrases:
        if phrase.lower() not in low:
            fail(f"{where}: missing canonical phrase {phrase!r}")

def ensure_path(repo: str, path: str) -> None:
    quoted = urllib.parse.quote(path, safe="/")
    url = f"https://api.github.com/repos/{ORG}/{repo}/contents/{quoted}?ref=main"
    data = fetch_json(url)
    if not data.get("sha"):
        fail(f"{repo}: path has no blob/tree SHA: {path}")

def validate_profile() -> None:
    require(PROFILE, ["## 30-Second Path", "Project Snapshot", "Evidence Pipeline", "PSP", "BS"], "Organization profile")
    if PROFILE.find("https://github.com/nanimnoworry/PSP") > PROFILE.find("https://github.com/nanimnoworry/BS"):
        fail("Organization profile: PSP must appear before BS in the reading path")
    for private_repo in CONTRACT["private_repositories"]:
        pattern = rf"\[[^\]]*{re.escape(private_repo)}[^\]]*\]\(https://github\.com/{ORG}/{re.escape(private_repo)}"
        if re.search(pattern, PROFILE, re.I):
            fail(f"Organization profile: private repository is linked publicly: {private_repo}")

def validate_repo(repo: str, spec: dict) -> None:
    readme = fetch_text(f"https://raw.githubusercontent.com/{ORG}/{repo}/main/README.md")
    require(readme, spec["required_phrases"], f"{repo}/README.md")
    forbidden = ("thisisstress", "forest-green", "production adopted", "production model")
    for term in forbidden:
        if term in readme.lower():
            fail(f"{repo}/README.md: forbidden or cross-project term {term!r}")

    meta = fetch_json(f"https://api.github.com/repos/{ORG}/{repo}")
    if meta.get("visibility") != spec["visibility"]:
        fail(f"{repo}: visibility drift: {meta.get('visibility')!r}")
    if meta.get("default_branch") != "main":
        fail(f"{repo}: default branch must remain main")
    if meta.get("description") != spec["description"]:
        fail(f"{repo}: About description drift")

    for path in spec["required_paths"]:
        ensure_path(repo, path)

    topics = set(meta.get("topics") or [])
    recommended = set(spec.get("recommended_topics") or [])
    missing_topics = sorted(recommended - topics)
    if missing_topics:
        print(f"WARNING {repo}: recommended topics not yet applied in GitHub UI: {', '.join(missing_topics)}")

def main() -> int:
    validate_profile()
    for repo, spec in CONTRACT["repositories"].items():
        validate_repo(repo, spec)
    print("public surface contract: PASS")
    print("reading order: Organization → PSP → BS")
    print("canonical result: Plan 2 0.74232 / Plan 3 0.74231")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, urllib.error.URLError, TimeoutError) as exc:
        print(f"public surface contract: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1)
