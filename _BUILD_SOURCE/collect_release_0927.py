"""Collect registered runtime assets from the real browser, without source archives."""
import json, re
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot
import http.server
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None

ROOT=Path(shoot.GAME)
OUT=ROOT/'_shots/repair_0927'; OUT.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  page=browser.new_page();page.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  page.wait_for_function('()=>window.__bofFrames>4',timeout=120000)
  page.evaluate(shoot.TRAP_RAF)
  # Space ships register modular parts only when the player enters space.
  # Exercise stage setup before snapshotting the registry, not just the boot menu.
  page.evaluate('''()=>{furyShipWarm();run.mode='arcade';run.pilot='yuri';
    pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');
    for(let stage=1;stage<=9;stage++){run.stage=stage;curStage=STAGES[stage-1];beginStage(stage);}
  }''')
  data=page.evaluate('''()=>({images:Object.fromEntries(Object.entries(XART._src).filter(([k])=>
    !(BOFX.cells?.[k]||BOFX.playercells?.[k]||BOFX.ships?.[k]))),
    registered:Object.values(XART._src).filter(v=>typeof v==='string'),
    primary:window.BOF,audio:{...BOFA,music:Object.fromEntries(Object.entries(BOFA.music).filter(([k])=>!k.startsWith('unused')))},
    scripts:[...document.scripts].map(s=>s.getAttribute('src')).filter(Boolean)})''')
  browser.close()
finally:stop()
paths=set()
def walk(o):
 if isinstance(o,dict):
  for v in o.values():walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
 elif isinstance(o,str) and o.startswith('assets/') and (ROOT/o).is_file():paths.add(o)
walk({k:v for k,v in data.items() if k!='registered'})
# Explicit HTML/CSS/module paths include fonts, cursors and non-registry media.
code=[ROOT/'index.html']+[ROOT/s for s in data['scripts']]
for f in code:
 if f.is_file():
  for p in re.findall(r'''["'](assets/[^"'\n]+\.(?:png|webp|jpg|jpeg|mp3|ogg|wav|woff2?|ttf|js|css|json))["']''',f.read_text(encoding='utf-8')):
   if (ROOT/p).is_file() and p not in data['registered'] and not '/music/unused' in p:paths.add(p)
paths.update(s for s in data['scripts'] if (ROOT/s).is_file())
result={'paths':sorted(paths),'count':len(paths),'bytes':sum((ROOT/p).stat().st_size for p in paths)}
(OUT/'runtime-assets.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='paths'},indent=2))
