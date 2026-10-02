#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; QA=ROOT/"qa"; QA.mkdir(exist_ok=True)
ASSETS=[("01 · Hero","hero.svg","hero-mobile.svg"),("02 · Project Snapshot","project-snapshot.svg","project-snapshot-mobile.svg"),("03 · Evidence Pipeline","evidence-pipeline.svg","evidence-pipeline-mobile.svg"),("04 · Model Journey","model-lineage.svg","model-lineage-mobile.svg"),("05 · Repository System","repository-map.svg","repository-map-mobile.svg"),("06 · Scope Endcap","footer-endcap.svg","footer-endcap-mobile.svg")]
def page(mobile=False,grid=False):
    native=800 if mobile else 1600
    width=f"{native}px" if grid else ("390px" if mobile else "min(1600px, calc(100vw - 64px))")
    gap="18px" if mobile else "28px"
    cards=""
    for label,d,m in ASSETS:
        asset=m if mobile else d
        overlay='<span class="grid"></span>' if grid else ''
        cards+=f'<section class="card"><div class="label">{label}</div><div class="frame"><img src="../profile/assets/{asset}" alt="{label}">{overlay}</div></section>'
    gridcss=f'.grid{{position:absolute;inset:0;background-image:linear-gradient(to right,rgba(239,68,68,.16) 1px,transparent 1px),linear-gradient(to bottom,rgba(239,68,68,.11) 1px,transparent 1px);background-size:16px 16px;pointer-events:none}}' if grid else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{{box-sizing:border-box}}body{{margin:0;background:#E8EDF4;color:#0B1220;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}main{{width:{width};margin:0 auto;padding:32px 0 64px;display:grid;gap:{gap}}}header,.card{{background:#fff;border:1px solid #CBD5E1;border-radius:20px}}header{{padding:20px 24px}}h1{{font-size:{'22px' if mobile else '28px'};margin:0 0 6px}}p{{margin:0;color:#64748B;font-size:14px}}.card{{padding:{'10px' if mobile and not grid else '18px'};overflow:hidden}}.label{{font-size:12px;font-weight:800;letter-spacing:.08em;color:#64748B;margin:0 0 10px}}.frame{{position:relative}}img{{display:block;width:100%;height:auto;border-radius:12px}}{gridcss}</style></head><body><main><header><h1>NANIM NO WORRY · {'Mobile ' if mobile else ''}{'Alignment ' if grid else ''}QA</h1><p>Optical text anchors · quantized card geometry · motion-safe static frame</p></header>{cards}</main></body></html>'''
(QA/"contact-sheet.html").write_text(page(False,False),encoding="utf-8")
(QA/"mobile-sheet.html").write_text(page(True,False),encoding="utf-8")
(QA/"alignment-sheet.html").write_text(page(False,True),encoding="utf-8")
(QA/"alignment-mobile.html").write_text(page(True,True),encoding="utf-8")
hero_svg=(ROOT/"profile"/"assets"/"hero.svg").read_text(encoding="utf-8")
def motion_page(seconds):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>*{{box-sizing:border-box}}html,body{{margin:0;background:#E8EDF4}}main{{width:1600px;margin:32px auto}}.frame{{background:white;padding:18px;border:1px solid #CBD5E1;border-radius:20px}}.label{{font:800 12px system-ui;color:#64748B;letter-spacing:.08em;margin-bottom:10px}}svg{{display:block;width:100%;height:auto;border-radius:12px}}</style></head><body onload="document.querySelector('svg').setCurrentTime({seconds})"><main><div class="frame"><div class="label">HERO MOTION · t={seconds}s</div>{hero_svg}</div></main></body></html>'''
(QA/"hero-motion-t0.html").write_text(motion_page(0),encoding="utf-8")
(QA/"hero-motion-t6.html").write_text(motion_page(6),encoding="utf-8")
def theme_page(asset,label,bg):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>*{{box-sizing:border-box}}html,body{{margin:0;background:{bg}}}main{{width:1600px;margin:32px auto}}.frame{{background:{bg};padding:18px;border:1px solid #CBD5E1;border-radius:20px}}.label{{font:800 12px system-ui;color:#64748B;letter-spacing:.08em;margin-bottom:10px}}img{{display:block;width:100%;height:auto;border-radius:12px}}</style></head><body><main><div class="frame"><div class="label">{label}</div><img src="../profile/assets/{asset}" alt="{label}"></div></main></body></html>'''
(QA/"hero-theme-light.html").write_text(theme_page("hero-light.svg","HERO · GITHUB LIGHT THEME","#FFFFFF"),encoding="utf-8")
(QA/"hero-theme-dark.html").write_text(theme_page("hero.svg","HERO · GITHUB DARK THEME","#0D1117"),encoding="utf-8")
def mobile_theme_page(asset,label,bg):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>*{{box-sizing:border-box}}html,body{{margin:0;background:{bg}}}main{{width:800px;margin:24px auto}}.frame{{background:{bg};padding:14px;border:1px solid #CBD5E1;border-radius:20px}}.label{{font:800 12px system-ui;color:#64748B;letter-spacing:.08em;margin-bottom:10px}}img{{display:block;width:100%;height:auto;border-radius:12px}}</style></head><body><main><div class="frame"><div class="label">{label}</div><img src="../profile/assets/{asset}" alt="{label}"></div></main></body></html>'''
(QA/"hero-theme-light-mobile.html").write_text(mobile_theme_page("hero-light-mobile.svg","MOBILE HERO · GITHUB LIGHT THEME","#FFFFFF"),encoding="utf-8")
(QA/"hero-theme-dark-mobile.html").write_text(mobile_theme_page("hero-mobile.svg","MOBILE HERO · GITHUB DARK THEME","#0D1117"),encoding="utf-8")
switcher='''<!doctype html><html><head><meta charset="utf-8"><style>*{box-sizing:border-box}html,body{margin:0;background:#E8EDF4}main{width:1600px;margin:32px auto}.frame{background:white;padding:18px;border:1px solid #CBD5E1;border-radius:20px}img{display:block;width:100%;height:auto;border-radius:12px}</style></head><body><main><div class="frame"><picture><source media="(max-width: 640px) and (prefers-color-scheme: dark)" srcset="../profile/assets/hero-mobile.svg"><source media="(max-width: 640px) and (prefers-color-scheme: light)" srcset="../profile/assets/hero-light-mobile.svg"><source media="(prefers-color-scheme: dark)" srcset="../profile/assets/hero.svg"><source media="(prefers-color-scheme: light)" srcset="../profile/assets/hero-light.svg"><img src="../profile/assets/hero-light.svg" alt="theme switcher"></picture></div></main></body></html>'''
(QA/"hero-theme-switcher.html").write_text(switcher,encoding="utf-8")
print("visual + alignment + deterministic temporal + theme + single-picture switcher QA pages generated")
