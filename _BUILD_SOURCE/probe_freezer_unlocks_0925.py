"""Render Freezer's Stage 2 three-weapon announcement in real Chromium."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/freezer_unlocks_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':2,'pilot':'freezer','invuln':True})
  rows=pg.evaluate("""()=>{const r=unlockRowsFor(2,'freezer');unlocksStart(r,()=>{});
    return r.map(x=>x[0]);}""")
  for _ in range(9):
   err=pg.evaluate(sh.STEP,30)
   if err:raise RuntimeError(err)
   pg.wait_for_timeout(16)
  pg.wait_for_function("()=>XART.rdy('weapon_found_0918')",timeout=30000)
  pg.evaluate(sh.STEP,2)
  png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
  (out/'screen.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report={'rows':rows,'errors':errors};(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert not errors and rows==['FIRE ORB','ICE BREATH','THERMOSHOCK BALL']
  br.close()
finally:stop()
