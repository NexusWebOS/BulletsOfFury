"""Inspect the live Stage 4 Storm Sovereign warfare controller in Chromium."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
out=Path('_shots/stage4_warfare_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':4,'pilot':'cole','invuln':True})
  init=pg.evaluate("""()=>{stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];
   boss=null;bossActive=false;spawnBoss('stormsovereign');boss._be=null;boss.enter=false;boss.x=worldWidth()/2;boss.y=boss.ty;
   stage4WarfareSetMode(boss,'burst');return {name:boss.name,hp:boss.maxhp,mode:boss._s4war.mode,pat:SHIPBOSS.stormsovereign.pat};}""")
  pg.wait_for_function("()=>XART.rdy('s4w_boss_idle')",timeout=30000)
  seen={};maxflash=0
  for i in range(100):
   err=pg.evaluate(sh.STEP,2)
   if err:raise RuntimeError(err)
   q=pg.evaluate("""()=>({k:eBullets.map(q=>q.kind),mode:boss._s4war.mode,fl:_navalFlashes.length,shield:boss._s4war.shield.active})""")
   for kind in q['k']:seen[kind]=seen.get(kind,0)+1
   maxflash=max(maxflash,q['fl'])
   if i==25:pg.wait_for_timeout(25)
  last=pg.evaluate("""()=>({mode:boss._s4war.mode,round:boss._s4war.round,projectiles:eBullets.length,shield:boss._s4war.shield.active})""")
  png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
  (out/'combat.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report={'init':init,'seen':seen,'maxflash':maxflash,'last':last,'errors':errors}
  (out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert not errors and init['mode']=='burst' and seen and maxflash>0
  br.close()
finally:stop()
