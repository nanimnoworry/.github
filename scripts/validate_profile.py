#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile"
ASSETS = PROFILE / "assets"
README = PROFILE / "README.md"

REQUIRED_ASSETS = {
    "hero.svg",
    "project-snapshot.svg",
    "evidence-pipeline.svg",
    "model-lineage.svg",
    "validation-evidence.svg",
    "repository-map.svg",
    "footer-endcap.svg",
}
CANONICAL_FACTS = {
    "0.74232", "0.74231", "PSP", "BS", "planB", "Research-Papers",
    "not a clinical diagnostic",
}
FORBIDDEN_PROFILE_TERMS = {"thisisstress", "Production adopted", "production model"}
FORBIDDEN_SVG_TERMS = {"Arial", "Times New Roman"}
GRID = 16.0

def fail(message: str) -> None:
    raise AssertionError(message)

def number(value: str | None, *, where: str) -> float:
    if value is None:
        fail(f"missing numeric attribute: {where}")
    try:
        return float(value)
    except ValueError as exc:
        raise AssertionError(f"invalid numeric attribute {value!r}: {where}") from exc

def quantized(value: float) -> bool:
    return abs((value / GRID) - round(value / GRID)) < 1e-9

def validate_manifest() -> None:
    actual = {p.name for p in ASSETS.glob("*.svg")}
    if actual != REQUIRED_ASSETS:
        fail(f"asset manifest mismatch: required={sorted(REQUIRED_ASSETS)}, actual={sorted(actual)}")
    text = README.read_text(encoding="utf-8")
    refs = set(re.findall(r"\./assets/([A-Za-z0-9._-]+\.svg)", text))
    if refs != REQUIRED_ASSETS:
        fail(f"README/asset mismatch: refs={sorted(refs)}")
    if re.search(r"\.(png|jpe?g|gif|webp)(?:\)|\"|'|\s)", text, re.I):
        fail("raster asset reference found in profile README")

def validate_readme() -> None:
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    for fact in CANONICAL_FACTS:
        if fact.lower() not in lower:
            fail(f"canonical fact missing: {fact}")
    for term in FORBIDDEN_PROFILE_TERMS:
        if term.lower() in lower:
            fail(f"forbidden or ambiguous profile term: {term}")
    order = [
        "## Start Here", "## Project Snapshot", "## Evidence Pipeline",
        "## Model Journey", "## Validation & Decision", "## Repository System",
        "## Team", "## Research Scope",
    ]
    positions = [text.find(label) for label in order]
    if any(p < 0 for p in positions) or positions != sorted(positions):
        fail("README reading order contract failed")

def validate_svg(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    for term in FORBIDDEN_SVG_TERMS:
        if term.lower() in raw.lower():
            fail(f"{path.name}: forbidden font term {term}")
    if "system-ui" not in raw:
        fail(f"{path.name}: system-ui font stack missing")
    if re.search(r"[\uac00-\ud7a3]", raw):
        fail(f"{path.name}: Hangul text inside SVG risks font fallback boxes")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise AssertionError(f"{path.name}: XML parse failure: {exc}") from exc

    vb = root.attrib.get("viewBox", "").split()
    if len(vb) != 4 or vb[:2] != ["0", "0"] or float(vb[2]) != 1600:
        fail(f"{path.name}: viewBox must start '0 0 1600 …'")
    if root.attrib.get("width") != "1600":
        fail(f"{path.name}: width must be 1600")

    ns = {"svg": "http://www.w3.org/2000/svg"}
    if root.find("svg:title", ns) is None or root.find("svg:desc", ns) is None:
        fail(f"{path.name}: accessible title/desc missing")

    for group in root.findall(".//svg:g[@data-title='true']", ns):
        texts = group.findall("svg:text", ns)
        if len(texts) != 1 or not texts[0].findall("svg:tspan", ns):
            fail(f"{path.name}: title must be one text + tspan structure")

    for group in root.findall(".//svg:g[@data-grid='16']", ns):
        rects = group.findall("svg:rect", ns)
        if not rects:
            fail(f"{path.name}: empty grid contract")
        for rect in rects:
            for attr in ("x", "y", "width", "height"):
                value = number(rect.attrib.get(attr), where=f"{path.name}:{attr}")
                if not quantized(value):
                    fail(f"{path.name}: non-quantized {attr}={value}")

    animations = len(root.findall(".//svg:animate", ns)) + len(root.findall(".//svg:animateTransform", ns))
    if path.name == "hero.svg":
        if animations < 4:
            fail("hero.svg: hero motion missing")
        safe = root.find(".//svg:rect[@id='text-safe-zone']", ns)
        fx = root.find(".//svg:g[@id='fx-zone']", ns)
        if safe is None or fx is None:
            fail("hero.svg: safe/fx zone missing")
        safe_right = number(safe.attrib.get("x"), where="safe x") + number(safe.attrib.get("width"), where="safe width")
        match = re.search(r"translate\(([-0-9.]+)", fx.attrib.get("transform", ""))
        if not match or float(match.group(1)) <= safe_right:
            fail("hero.svg: FX zone intrudes into text safe zone")
    elif animations > 1:
        fail(f"{path.name}: secondary panel exceeds ambient motion budget")

def validate_contamination() -> None:
    text = "\n".join([README.read_text(encoding="utf-8")] + [p.read_text(encoding="utf-8") for p in ASSETS.glob("*.svg")]).lower()
    for term in ("thisisstress", "stress score", "forest-green"):
        if term in text:
            fail(f"cross-project contamination: {term}")

def main() -> int:
    validate_manifest()
    validate_readme()
    validate_contamination()
    for path in sorted(ASSETS.glob("*.svg")):
        validate_svg(path)
    print("profile validator: PASS")
    print("assets: 7 / SVG-first / 1600px viewBox")
    print("contracts: reading-order, asset-manifest, XML, grid, title, safe-zone, motion, contamination")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"profile validator: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1)
