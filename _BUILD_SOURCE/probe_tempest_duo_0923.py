import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from shoot import GAME,serve,SETUP,TRAP_RAF
from playwright.sync_api import sync_playwright

port,stop=serve(GAME); errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1280,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.goto(f'http://127.0.0.1:{port}/index.html')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4')
  pg.evaluate(TRAP_RAF)
  assert pg.evaluate(SETUP,{'state':'PLAY','stage':6,'pilot':'cole','invuln':True})['ok']
  pg.evaluate("()=>{s6Opening=null;stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;subBossDone=false;spawnSubBoss('tempestbrothers');subBoss._scene=null;window.testBoss=subBoss;}")
  pg.wait_for_function("()=>['tempestduo_black_intact_4','tempestduo_silver_intact_4','tempestduo_black_pitch_0','tempestduo_silver_pitch_0'].every(k=>XART.rdy(k))")
  report=pg.evaluate("""()=>{
    let b=testBoss,history=[],rotations=0;
    for(let i=0;i<1080;i++){
      tempestBrothersUpdate(b,1/60);
      if(i%60===0)history.push(b._tempestDuo.ships.map(p=>({ship:p._tempestGray?'silver':'black',phase:p._duoLite.phase,x:Math.round(p.x),y:Math.round(p.y),angle:p._jet.angle,src:tempestPlateKey(p)})));
    }
    let old=ctx.rotate;ctx.rotate=function(){rotations++;return old.apply(this,arguments)};
    try{b._tempestDuo.ships.forEach(tempestJetShipDraw)}finally{ctx.rotate=old}
    return {history,rotations,bullets:eBullets.length,bossHp:b.hp,phases:b._tempestDuo.ships.map(p=>p._duoLite.phase)};
  }""")
  print(json.dumps({'report':report,'errors':errors},indent=2))
  assert not errors,errors
  assert report['rotations']==0,report['rotations']
  assert report['bullets']>0,report['bullets']
  assert all(p['phase']!='entry' for p in report['history'][6]),report['history'][6]
  death=pg.evaluate("""()=>{const b=testBoss,D=b._tempestDuo;
    D.ships[0]._ai.vulnerable=true;D.ships[0]._ai.damage(9000);
    tempestBrothersSync(b);
    let soloPhases=new Set();
    for(let i=0;i<360;i++){tempestBrothersUpdate(b,1/60);soloPhases.add(D.ships[1]._duoLite.phase);}
    const solo={firstGone:D.ships[0]._ai.gone,secondAlive:!D.ships[1]._ai.gone,bossActive:!b.dead,phases:[...soloPhases]};
    D.ships[1]._ai.vulnerable=true;D.ships[1]._ai.damage(9000);
    tempestBrothersSync(b);
    const afterHit=D.ships.map(p=>({hp:p.hp,dead:p.dead}));
    for(let i=0;i<90;i++)tempestBrothersUpdate(b,1/60);
    return {solo,afterHit,done:b.dead,gone:D.ships.map(p=>p._ai.gone)};}""")
  print('DEATH_CHECK',json.dumps(death))
  assert all(p['dead'] for p in death['afterHit']) and death['done'] and all(death['gone'])
  assert death['solo']['firstGone'] and death['solo']['secondAlive'] and death['solo']['bossActive']
  assert 'fire' in death['solo']['phases']
  br.close()
finally:stop()
