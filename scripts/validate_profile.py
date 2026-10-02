#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/"profile"; ASSETS=PROFILE/"assets"; README=PROFILE/"README.md"
REQUIRED_ASSETS={
"hero.svg","hero-light.svg","project-snapshot.svg","evidence-pipeline.svg","model-lineage.svg","repository-map.svg","footer-endcap.svg",
"hero-mobile.svg","hero-light-mobile.svg","project-snapshot-mobile.svg","evidence-pipeline-mobile.svg","model-lineage-mobile.svg","repository-map-mobile.svg","footer-endcap-mobile.svg",
}
CANONICAL_FACTS={"0.74232","0.74231","PSP","BS","planB","Research-Papers","not a clinical diagnostic"}
FORBIDDEN_PROFILE_TERMS={"thisisstress","Production adopted","production model"}
FORBIDDEN_SVG_TERMS={"Arial","Times New Roman"}
GRID=16.0
MAX_README_CHARS=4800
MAX_H2=7
MOTION_MIN={"ambient":8.0,"sweep":10.0,"orbital":9.0,"pulse":5.0,"particle":4.5}

def fail(m): raise AssertionError(m)
def number(v,where=""):
    if v is None: fail(f"missing numeric attribute: {where}")
    try:return float(v)
    except ValueError as e: raise AssertionError(f"invalid numeric attribute {v!r}: {where}") from e
def quantized(v): return abs(v/GRID-round(v/GRID))<1e-9
def seconds(v):
    if not v or not v.endswith("s"): fail(f"animation duration must use seconds: {v!r}")
    return float(v[:-1])

def validate_manifest():
    actual={p.name for p in ASSETS.glob("*.svg")}
    if actual!=REQUIRED_ASSETS: fail(f"asset manifest mismatch: required={sorted(REQUIRED_ASSETS)}, actual={sorted(actual)}")
    text=README.read_text(encoding="utf-8")
    refs=set(re.findall(r"\./assets/([A-Za-z0-9._-]+\.svg)",text))
    if refs!=REQUIRED_ASSETS: fail(f"README/asset mismatch: refs={sorted(refs)}")
    if re.search(r"\.(png|jpe?g|gif|webp)(?:\)|\"|'|\s)",text,re.I): fail("raster asset reference found in profile README")
    if text.count("<picture>")!=7 or text.count("max-width: 640px")!=7: fail("responsive picture contract failed")
    if "#gh-light-mode-only" not in text or "#gh-dark-mode-only" not in text: fail("GitHub theme-specific Hero contract missing")

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

def card_rect(card,ns,path):
    rect=card.find("svg:rect",ns)
    if rect is None: fail(f"{path.name}: card missing rect")
    return tuple(number(rect.attrib.get(a),where=f"{path.name}:{a}") for a in ("x","y","width","height"))

def validate_card_sets(root,ns,path):
    for s in root.findall(".//svg:g[@data-card-set]",ns):
        layout=s.attrib["data-card-set"]
        cards=s.findall("svg:g[@data-card]",ns)
        if not cards: fail(f"{path.name}: empty card set")
        vals=[card_rect(c,ns,path) for c in cards]
        widths={v[2] for v in vals}; heights={v[3] for v in vals}
        if len(widths)!=1 or len(heights)!=1: fail(f"{path.name}: unequal card dimensions")
        if layout=="row":
            if len({v[1] for v in vals})!=1: fail(f"{path.name}: card row baseline mismatch")
            coords=sorted(vals,key=lambda v:v[0]); gaps=[coords[i+1][0]-(coords[i][0]+coords[i][2]) for i in range(len(coords)-1)]
        elif layout=="stack":
            if len({v[0] for v in vals})!=1: fail(f"{path.name}: card stack left edge mismatch")
            coords=sorted(vals,key=lambda v:v[1]); gaps=[coords[i+1][1]-(coords[i][1]+coords[i][3]) for i in range(len(coords)-1)]
        else: fail(f"{path.name}: unknown card-set layout {layout}")
        if gaps and (len({round(g,6) for g in gaps})!=1 or min(gaps)<16): fail(f"{path.name}: inconsistent card gaps {gaps}")

        role_offsets={}
        for card,rect in zip(cards,vals):
            cx,cy,_,_=rect
            template=card.attrib.get("data-template","default")
            for t in card.findall("svg:text",ns):
                role=t.attrib.get("data-role")
                if not role: continue
                off=(number(t.attrib.get("x"),where=f"{path.name}:{role}:x")-cx, number(t.attrib.get("y"),where=f"{path.name}:{role}:y")-cy)
                role_offsets.setdefault((template,role),[]).append(off)
        for (template,role),offsets in role_offsets.items():
            if len(offsets)>1 and len({(round(x,6),round(y,6)) for x,y in offsets})!=1:
                fail(f"{path.name}: optical text anchor mismatch for {template}/{role}: {offsets}")

def count_anims(node,ns):
    return len(node.findall(".//svg:animate",ns))+len(node.findall(".//svg:animateTransform",ns))+len(node.findall(".//svg:animateMotion",ns))

def validate_motion(root,ns,path):
    total=count_anims(root,ns)
    groups=root.findall(".//svg:g[@data-motion-role]",ns)
    assigned=sum(count_anims(g,ns) for g in groups)
    if assigned!=total: fail(f"{path.name}: every animation must belong to exactly one motion role ({assigned}/{total})")
    roles={g.attrib["data-motion-role"] for g in groups}
    for g in groups:
        role=g.attrib["data-motion-role"]
        if role not in MOTION_MIN: fail(f"{path.name}: unknown motion role {role}")
        for tag in ("animate","animateTransform","animateMotion"):
            for a in g.findall(f".//svg:{tag}",ns):
                dur=seconds(a.attrib.get("dur"))
                if dur<MOTION_MIN[role]: fail(f"{path.name}: {role} motion too fast ({dur}s < {MOTION_MIN[role]}s)")
    if path.name in {"hero.svg","hero-light.svg"}:
        if roles!={"ambient","sweep","orbital","pulse","particle"}: fail(f"{path.name}: motion roles mismatch {roles}")
        if total<12 or total>20: fail(f"{path.name}: motion count outside premium budget: {total}")
    elif path.name in {"hero-mobile.svg","hero-light-mobile.svg"}:
        if roles!={"ambient","orbital","pulse","particle"}: fail(f"{path.name}: motion roles mismatch {roles}")
        if total<7 or total>14: fail(f"{path.name}: motion count outside premium budget: {total}")
    else:
        if roles and roles!={"ambient"}: fail(f"{path.name}: secondary panels may only use ambient motion")
        if total>1: fail(f"{path.name}: secondary motion budget exceeded")

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
        for rect in g.findall(".//svg:rect",ns):
            for attr in ("x","y","width","height"):
                v=number(rect.attrib.get(attr),where=f"{path.name}:{attr}")
                if not quantized(v): fail(f"{path.name}: non-quantized {attr}={v}")
    validate_card_sets(root,ns,path)
    validate_motion(root,ns,path)
    if path.name in {"hero.svg","hero-light.svg"}:
        safe=root.find(".//svg:rect[@id='text-safe-zone']",ns); fx=root.find(".//svg:g[@id='fx-zone']",ns)
        if safe is None or fx is None: fail(f"{path.name}: safe/fx zone missing")
        right=number(safe.attrib.get("x"))+number(safe.attrib.get("width"))
        m=re.search(r"translate\(([-0-9.]+)",fx.attrib.get("transform",""))
        if not m or float(m.group(1))<=right: fail(f"{path.name}: FX zone intrudes into text safe zone")
        bus=root.find(".//svg:path[@id='signal-bus']",ns)
        history=root.find(".//svg:path[@id='history-link']",ns)
        branches=root.find(".//svg:path[@id='model-branches']",ns)
        if bus is None or history is None or branches is None: fail(f"{path.name}: signal collector contract missing")
        if history.attrib.get("d")!="M176 400 H240": fail(f"{path.name}: EMBRYO / HISTORY link must visibly reach collector bus")
        if bus.attrib.get("d")!="M240 160 V400": fail(f"{path.name}: collector bus geometry drift")
    card_sizes=[float(t.attrib["font-size"]) for s in root.findall(".//svg:g[@data-card-set]",ns) for c in s.findall("svg:g[@data-card]",ns) for t in c.findall("svg:text",ns) if t.attrib.get("font-size")]
    if path.name.endswith("-mobile.svg"):
        if card_sizes and min(card_sizes)<22: fail(f"{path.name}: mobile card font below 22px design minimum")
    elif card_sizes and min(card_sizes)<13:
        fail(f"{path.name}: desktop card font below 13px premium minimum")

def validate_theme_pairs():
    ns={"svg":"http://www.w3.org/2000/svg"}
    for dark_name,light_name in (("hero.svg","hero-light.svg"),("hero-mobile.svg","hero-light-mobile.svg")):
        dark=ET.fromstring((ASSETS/dark_name).read_text(encoding="utf-8"))
        light=ET.fromstring((ASSETS/light_name).read_text(encoding="utf-8"))
        def geometry(root):
            items=[]
            for card in root.findall(".//svg:g[@data-card]",ns):
                rect=card.find("svg:rect",ns)
                if rect is not None:
                    items.append((card.attrib.get("data-card"),rect.attrib.get("x"),rect.attrib.get("y"),rect.attrib.get("width"),rect.attrib.get("height")))
            return items
        if geometry(dark)!=geometry(light): fail(f"{dark_name}/{light_name}: theme card geometry mismatch")

def main():
    validate_manifest(); validate_readme(); validate_theme_pairs()
    joined="\n".join([README.read_text(encoding="utf-8")]+[p.read_text(encoding="utf-8") for p in ASSETS.glob("*.svg")]).lower()
    for term in ("thisisstress","stress score","forest-green"):
        if term in joined: fail(f"cross-project contamination: {term}")
    for p in sorted(ASSETS.glob("*.svg")): validate_svg(p)
    print("profile validator: PASS")
    print("typography: role baselines + optical text anchors locked")
    print("layout: equal card dimensions + constant gaps + quantized geometry")
    print("motion: ambient / sweep / orbital / pulse / particle hierarchy locked")
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except AssertionError as e:
        print(f"profile validator: FAIL — {e}",file=sys.stderr); raise SystemExit(1)
