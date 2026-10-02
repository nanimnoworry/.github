#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
QA.mkdir(exist_ok=True)
ASSETS = [
    ("01 · Hero", "hero.svg"),
    ("02 · Project Snapshot", "project-snapshot.svg"),
    ("03 · Evidence Pipeline", "evidence-pipeline.svg"),
    ("04 · Model Journey", "model-lineage.svg"),
    ("05 · Validation & Decision", "validation-evidence.svg"),
    ("06 · Repository System", "repository-map.svg"),
    ("07 · Scope Endcap", "footer-endcap.svg"),
]

def page(mobile: bool) -> str:
    width = "390px" if mobile else "min(1600px, calc(100vw - 64px))"
    gap = "18px" if mobile else "28px"
    cards = "".join(
        f'<section class="card"><div class="label">{label}</div><img src="../profile/assets/{asset}" alt="{label}"></section>'
        for label, asset in ASSETS
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NANIM NO WORRY · Visual QA</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#E8EDF4;color:#0B1220;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{width:{width};margin:0 auto;padding:32px 0 64px;display:grid;gap:{gap}}}
header{{background:#fff;border:1px solid #CBD5E1;border-radius:20px;padding:20px 24px}}
h1{{font-size:{'22px' if mobile else '28px'};margin:0 0 6px}}p{{margin:0;color:#64748B;font-size:14px}}
.card{{background:#fff;border:1px solid #CBD5E1;border-radius:20px;padding:{'10px' if mobile else '18px'};overflow:hidden}}
.label{{font-size:12px;font-weight:800;letter-spacing:.08em;color:#64748B;margin:0 0 10px}}
img{{display:block;width:100%;height:auto;border-radius:{'10px' if mobile else '14px'}}}
</style></head><body><main><header><h1>NANIM NO WORRY · {'Mobile ' if mobile else ''}Visual QA</h1>
<p>Boundary · title overlap · grid rhythm · motion-safe static frame · readable scaling</p></header>{cards}</main></body></html>'''

(QA / "contact-sheet.html").write_text(page(False), encoding="utf-8")
(QA / "mobile-sheet.html").write_text(page(True), encoding="utf-8")
print("visual QA pages generated")
