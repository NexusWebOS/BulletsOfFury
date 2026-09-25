"""Real Chromium sample of both ice-jet plates and newly scheduled mine drone."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/stage3_ice_drones_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':3,'pilot':'cole','invuln':True})
  start=pg.evaluate("""()=>{diffKey='normal';DIFF=difficultyForRun(run.mode,diffKey);
    const p=buildStagePlan(3);stagePlan=[];waveIdx=999;spawnClock=9999;
    enemies=[];eBullets=[];pBullets=[];aiQueue.length=0;
    spawnEnemy('s3interceptor',worldWidth()*.34,90,{});
    spawnEnemy('s3interceptor',worldWidth()*.66,115,{});
    const ice=p.find(w=>Math.abs(w.t-20.4)<.01);ice.fn();
    while(aiQueue.length)aiQueue.shift().fn();
    return {planned:p.length,iceWave:!!ice,units:enemies.map(e=>({type:e.type,art:e._biomePlate}))};}""")
  for k in ('stage3_ice_jet_01','stage3_ice_jet_02','stage3_ice_drone_01'):
   pg.wait_for_function("k=>XART.rdy('overhaul_'+k)",arg=k,timeout=30000)
  pg.evaluate(sh.STEP,1)
  png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
  (out/'jets.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  for i in range(12):
   err=pg.evaluate(sh.STEP,30)
   if err:raise RuntimeError(err)
   if i%3==0:pg.wait_for_timeout(22)
  finish=pg.evaluate("""()=>({drones:enemies.filter(e=>e.type==='s3mine').length,
    bullets:eBullets.map(q=>q.kind),jets:enemies.filter(e=>e.type==='s3interceptor').map(e=>e._biomePlate)})""")
  png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
  (out/'combat.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report={'start':start,'finish':finish,'errors':errors}
  (out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert not errors and start['iceWave'] and start['planned']>=12
  assert {e['art'] for e in start['units'] if e['type']=='s3interceptor'}=={'overhaul_stage3_ice_jet_01','overhaul_stage3_ice_jet_02'}
  assert any(e['type']=='s3mine' and e['art']=='overhaul_stage3_ice_drone_01' for e in start['units'])
  assert 's3shard' in finish['bullets']
  br.close()
finally:stop()
