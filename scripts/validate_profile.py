#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/"profile"; ASSETS=PROFILE/"assets"; README=PROFILE/"README.md"
REQUIRED_ASSETS={
"hero.svg","project-snapshot.svg","evidence-pipeline.svg","model-lineage.svg","repository-map.svg","footer-endcap.svg",
"hero-mobile.svg","project-snapshot-mobile.svg","evidence-pipeline-mobile.svg","model-lineage-mobile.svg","repository-map-mobile.svg","footer-endcap-mobile.svg",
}
CANONICAL_FACTS={"0.74232","0.74231","PSP","BS","planB","Research-Papers","not a clinical diagnostic"}
FORBIDDEN_PROFILE_TERMS={"thisisstress","Production adopted","production model"}
FORBIDDEN_SVG_TERMS={"Arial","Times New Roman"}
GRID=16.0
MAX_README_CHARS=4800
MAX_H2=7

def fail(m): raise AssertionError(m)
def number(v,where=""):
    if v is None: fail(f"missing numeric attribute: {where}")
    try:return float(v)
    except ValueError as e: raise AssertionError(f"invalid numeric attribute {v!r}: {where}") from e
def quantized(v): return abs(v/GRID-round(v/GRID))<1e-9

def validate_manifest():
    actual={p.name for p in ASSETS.glob("*.svg")}
    if actual!=REQUIRED_ASSETS: fail(f"asset manifest mismatch: required={sorted(REQUIRED_ASSETS)}, actual={sorted(actual)}")
    text=README.read_text(encoding="utf-8")
    refs=set(re.findall(r"\./assets/([A-Za-z0-9._-]+\.svg)",text))
    if refs!=REQUIRED_ASSETS: fail(f"README/asset mismatch: refs={sorted(refs)}")
    if re.search(r"\.(png|jpe?g|gif|webp)(?:\)|\"|'|\s)",text,re.I): fail("raster asset reference found in profile README")
    if text.count("<picture>")!=6 or text.count("max-width: 640px")!=6: fail("responsive picture contract failed")

def validate_readme():
    text=README.read_text(encoding="utf-8"); lower=text.lower()
    if len(text)>MAX_README_CHARS: fail(f"editorial budget exceeded: {len(text)} > {MAX_README_CHARS}")
    h2=re.findall(r"^##\s+",text,re.M)
    if len(h2)>MAX_H2: fail(f"too many H2 sections: {len(h2)} > {MAX_H2}")
    if text.count("<details>")<2: fail("technical detail disclosure budget missing")
    for fact in CANONICAL_FACTS:
        if fact.lower() not in lower: fail(f"canonical fact missing: {fact}")
    for term in FORBIDDEN_PROFILE_TERMS:
        if term.lower() in lower: fail(f"forbidden or ambiguous profile term: {term}")
    order=["## 30-Second Path","## Project Snapshot","## Evidence Pipeline","## Model Journey","## Repository System","## Team","## Research Scope"]
    pos=[text.find(x) for x in order]
    if any(x<0 for x in pos) or pos!=sorted(pos): fail("README reading order contract failed")

def rect_values(rect,path):
    return tuple(number(rect.attrib.get(a),where=f"{path.name}:{a}") for a in ("x","y","width","height"))

def validate_card_contract(root,ns,path):
    for g in root.findall(".//svg:g[@data-card-row='true']",ns):
        rects=g.findall("svg:rect",ns)
        if len(rects)<2: fail(f"{path.name}: card row needs at least two rects")
        vals=[rect_values(r,path) for r in rects]
        ys={v[1] for v in vals}; ws={v[2] for v in vals}; hs={v[3] for v in vals}
        if len(ys)!=1 or len(ws)!=1 or len(hs)!=1: fail(f"{path.name}: card row width/height/baseline mismatch")
        xs=sorted(v[0] for v in vals); width=vals[0][2]
        gaps=[xs[i+1]-(xs[i]+width) for i in range(len(xs)-1)]
        if len({round(g,6) for g in gaps})>1 or any(g<16 for g in gaps): fail(f"{path.name}: card row gap mismatch")
    for g in root.findall(".//svg:g[@data-card-stack='true']",ns):
        rects=g.findall("svg:rect",ns)
        if len(rects)<2: fail(f"{path.name}: card stack needs at least two rects")
        vals=[rect_values(r,path) for r in rects]
        xs={v[0] for v in vals}; ws={v[2] for v in vals}; hs={v[3] for v in vals}
        if len(xs)!=1 or len(ws)!=1 or len(hs)!=1: fail(f"{path.name}: card stack width/height/alignment mismatch")
        ys=sorted(v[1] for v in vals); height=vals[0][3]
        gaps=[ys[i+1]-(ys[i]+height) for i in range(len(ys)-1)]
        if len({round(g,6) for g in gaps})>1 or any(g<16 for g in gaps): fail(f"{path.name}: card stack gap mismatch")

def validate_svg(path):
    raw=path.read_text(encoding="utf-8")
    for term in FORBIDDEN_SVG_TERMS:
        if term.lower() in raw.lower(): fail(f"{path.name}: forbidden font term {term}")
    if "system-ui" not in raw: fail(f"{path.name}: system-ui stack missing")
    if re.search(r"[\uac00-\ud7a3]",raw): fail(f"{path.name}: Hangul text inside SVG risks font fallback boxes")
    try: root=ET.fromstring(raw)
    except ET.ParseError as e: raise AssertionError(f"{path.name}: XML parse failure: {e}") from e
    vb=root.attrib.get("viewBox","").split(); expected=800 if path.name.endswith("-mobile.svg") else 1600
    if len(vb)!=4 or vb[:2]!=["0","0"] or float(vb[2])!=expected: fail(f"{path.name}: viewBox width must be {expected}")
    if root.attrib.get("width")!=str(expected): fail(f"{path.name}: width must be {expected}")
    ns={"svg":"http://www.w3.org/2000/svg"}
    if root.find("svg:title",ns) is None or root.find("svg:desc",ns) is None: fail(f"{path.name}: accessible title/desc missing")
    for g in root.findall(".//svg:g[@data-title='true']",ns):
        texts=g.findall("svg:text",ns)
        if len(texts)!=1 or not texts[0].findall("svg:tspan",ns): fail(f"{path.name}: title must be one text + tspan structure")
    for g in root.findall(".//svg:g[@data-grid='16']",ns):
        rects=g.findall("svg:rect",ns)
        if not rects: fail(f"{path.name}: empty grid contract")
        for rect in rects:
            for attr in ("x","y","width","height"):
                v=number(rect.attrib.get(attr),where=f"{path.name}:{attr}")
                if not quantized(v): fail(f"{path.name}: non-quantized {attr}={v}")
    validate_card_contract(root,ns,path)
    animations=(len(root.findall(".//svg:animate",ns))+len(root.findall(".//svg:animateTransform",ns))+len(root.findall(".//svg:animateMotion",ns)))
    if path.name=="hero.svg":
        if animations<12: fail(f"hero.svg: cinematic motion budget too low ({animations})")
        safe=root.find(".//svg:rect[@id='text-safe-zone']",ns); fx=root.find(".//svg:g[@id='fx-zone']",ns)
        if safe is None or fx is None: fail("hero.svg: safe/fx zone missing")
        right=number(safe.attrib.get("x"))+number(safe.attrib.get("width"))
        m=re.search(r"translate\(([-0-9.]+)",fx.attrib.get("transform",""))
        if not m or float(m.group(1))<=right: fail("hero.svg: FX zone intrudes into text safe zone")
    elif path.name=="hero-mobile.svg":
        if animations<6: fail(f"hero-mobile.svg: motion budget too low ({animations})")
    elif animations>1: fail(f"{path.name}: secondary panel exceeds ambient motion budget")
    if path.name.endswith("-mobile.svg"):
        sizes=[float(v) for v in re.findall(r'font-size="([0-9.]+)"',raw)]
        if sizes and min(sizes)<22: fail(f"{path.name}: mobile font below 22px design minimum")

def main():
    validate_manifest(); validate_readme()
    joined="\n".join([README.read_text(encoding="utf-8")]+[p.read_text(encoding="utf-8") for p in ASSETS.glob("*.svg")]).lower()
    for term in ("thisisstress","stress score","forest-green"):
        if term in joined: fail(f"cross-project contamination: {term}")
    for p in sorted(ASSETS.glob("*.svg")): validate_svg(p)
    print("profile validator: PASS")
    print("assets: 12 / responsive SVG-first / desktop 1600px + mobile 800px")
    print("layout: equal card dimensions + constant gaps + common baselines")
    print("hero: cinematic motion isolated to FX safe zone")
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except AssertionError as e:
        print(f"profile validator: FAIL — {e}",file=sys.stderr); raise SystemExit(1)
