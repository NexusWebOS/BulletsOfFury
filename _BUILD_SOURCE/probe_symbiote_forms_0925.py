"""Pixel-review each current Stage 8 symbiote form in the real game renderer."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/symbiote_forms_0925');out.mkdir(parents=True,exist_ok=True)
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
   boss=null;bossActive=false;spawnBoss('vileexistence');boss._scene=null;boss._symEntry=null;
   boss.enter=false;boss.x=worldWidth()/2;boss.y=boss.ty;}""")
  rows=[]
  for i in range(4):
   pg.evaluate("""i=>{vileBuildForm(boss,i);boss._symEntry=null;boss._morphT=null;
     boss.enter=false;boss.x=worldWidth()/2;boss.y=boss.ty;boss._mcd=5;boss.flash=0;}""",i)
   pg.wait_for_function("i=>XART.rdy('s8symboss_form_'+i)",arg=i,timeout=30000)
   err=pg.evaluate(sh.STEP,2)
   if err:raise RuntimeError(err)
   row=pg.evaluate("""()=>({form:boss._vForm,name:boss.name,art:vileAnimKey(boss),parts:boss.parts.length})""")
   rows.append(row)
   pg.wait_for_timeout(25)
   png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
   (out/f'form_{i+1}.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report={'rows':rows,'errors':errors};(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert not errors and len(rows)==4
  assert all(r['art']==f's8symboss_form_{i}' for i,r in enumerate(rows))
  assert [r['parts'] for r in rows]==[3,3,1,1]
  br.close()
finally:stop()
