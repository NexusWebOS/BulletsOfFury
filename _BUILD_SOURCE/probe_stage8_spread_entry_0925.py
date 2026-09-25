"""Verify the side-entry spread-wing jets survive global offscreen culling."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/stage8_spread_entry_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':8,'pilot':'cole','invuln':True})
  pg.evaluate("""()=>{stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];
   const W=worldWidth();spawnEnemy('s8spread',-120,VH*.18,{_side:1});
   spawnEnemy('s8spread',W+120,VH*.30,{_side:-1,_stagger:.28});}""")
  pg.wait_for_function("()=>XART.rdy('s8nf_spread_wing_fighter_idle')",timeout=30000)
  rows=[];kinds={}
  for i in range(90):
   err=pg.evaluate(sh.STEP,1)
   if err:raise RuntimeError(err)
   if i in (0,25,50,75,89):
    rows.append(pg.evaluate("""()=>({frames:window.__bofFrames,
      jets:enemies.filter(e=>e.type==='s8spread').map(e=>({x:e.x,y:e.y,side:e._side})),
      bullets:eBullets.filter(b=>b.kind==='s8nf_spread').length})"""))
   if i==50:
    pg.wait_for_timeout(60)
    png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
    (out/'crossing.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report={'rows':rows,'errors':errors};(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert not errors
  assert len(rows[0]['jets'])==2 and len(rows[2]['jets'])==2
  assert any(r['bullets']>0 for r in rows)
  br.close()
finally:stop()
