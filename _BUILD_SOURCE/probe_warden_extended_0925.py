"""Observe Stage 7 Warden beyond its entrance in real Chromium."""
import base64
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/warden_extended_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4')
  pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':7,'pilot':'cole','invuln':True})
  pg.evaluate("""()=>{s7Opening=null;stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;
    spawnClock=9999;enemies=[];eBullets=[];pBullets=[];boss=null;bossActive=false;
    spawnBoss(curStage.boss);boss._scene=null;window.__seen=new WeakSet();window.__kinds={};}""")
  rows=[]
  for sec in range(1,41):
   for _ in range(2):
    err=pg.evaluate(sh.STEP,30)
    if err:raise RuntimeError(err)
   row=pg.evaluate("""()=>{for(const q of eBullets)if(q&&!__seen.has(q)){
     __seen.add(q);const k=q.kind||'unknown';__kinds[k]=(__kinds[k]||0)+1;}
     const F=boss&&boss._s7warden;return {phase:F&&F.final.phase,
       mode:F&&F.mode, hp:boss&&boss.hp,projectiles:{...__kinds},visible:eBullets.length};}""")
   rows.append({'second':sec,**row})
   if sec in (4,10,16,24,32,40):
    pg.wait_for_timeout(30)
    png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
    (out/f'{sec:02}.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report={'rows':rows,'errors':errors};(out/'report.json').write_text(json.dumps(report,indent=2))
  print(json.dumps({'transitions':[x for i,x in enumerate(rows) if i==0 or (x['phase'],x['mode'])!=(rows[i-1]['phase'],rows[i-1]['mode'])],
                    'final':rows[-1],'errors':errors},indent=2))
  assert not errors
  assert any(x['phase']=='fight' for x in rows)
  assert sum(rows[-1]['projectiles'].values())>0
  br.close()
finally:stop()
