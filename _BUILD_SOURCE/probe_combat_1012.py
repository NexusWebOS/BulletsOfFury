from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/combat_pressure_1012';O.mkdir(exist_ok=True);port,stop=shoot.serve(str(R));errors=[];results=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' and '404' not in m.text else None)
  p.goto(f'http://localhost:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for stage in ([] if '--fixtures' in sys.argv else [1,2]):
   for diff in ['easy','normal','hard','furious']:
    p.evaluate('(d)=>{diffKey=d;DIFF=DIFFS[d]}',diff);p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'axel','invuln':False});p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=120000)
    p.evaluate('()=>{player.invuln=0;run.shield=5;run.speedLevel=5;run.speed=5;run.weapon=1;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);CP12.events=[];CP12.stage=0;for(const k of keybindFor(1).fire||[])Input.keys[k]=true;}')
    for i in range(70):p.evaluate(shoot.STEP,30);p.wait_for_timeout(15)
    r=p.evaluate('()=>({stage:run.stage,difficulty:diffKey,t:stageTimer,state,lives:run.lives,shield:run.shield,ambushes:CP12.events.filter(e=>e.event==="ambush").length,volleys:CP12.events.filter(e=>e.event==="rocket-volley").length,finite:Number.isFinite(player.x)&&Number.isFinite(player.y),enemyShots:eBullets.length})');results.append(r);print(json.dumps(r),flush=True);p.screenshot(path=str(O/f'stage{stage}-{diff}.png'))
    assert r['finite'];assert r['ambushes']>0,r
  p.evaluate(shoot.SETUP,{'state':'PLAY','stage':1,'pilot':'axel','invuln':True});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=120000)
  p.evaluate('()=>{Input.keys={};pBullets=[];CP12.events=[];CP12.serial=0;CP12.stage=1;CP12.lastTimer=0;cp12Ambush();waveIdx=999;spawnClock=9999;}')
  for i in range(9):p.evaluate(shoot.STEP,30);p.wait_for_timeout(15)
  fixture=p.evaluate('()=>({volleys:CP12.events.filter(e=>e.event==="rocket-volley").length,rigs:enemies.filter(e=>e._cp12).map(e=>({dead:e.dead,y:e.y,t:e._cp12.t,round:e._cp12.round}))})');print(json.dumps(fixture),flush=True);assert fixture['volleys']>0,fixture;results.append(fixture);p.screenshot(path=str(O/'ambush-volley.png'))
  for diff in ['easy','normal','hard','furious']:
   r=p.evaluate('''d=>{diffKey=d;DIFF=DIFFS[d];const b={x:240,y:140,hp:500,maxhp:500,_hammer:{state:'nova_release',t:2,novaShots:0,attackCycle:0}};const old=eBullets;eBullets=[];hammerCombatTick(b,0);const result={difficulty:d,rounds:b._hammer.novaShots,shots:eBullets.length};eBullets=old;return result}''',diff);assert r['rounds']==(3 if diff=='furious' else 2);assert r['shots']==(72 if diff=='furious' else 64);results.append(r)
  p.evaluate('f=>debugStartFight(f,{pilot:"cole"})',{'stage':5,'role':'boss','kind':'chromehammer','name':'CHROMIUM HAMMER'});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}',timeout=120000)
  for i in range(9):p.evaluate('()=>player.invuln=1e9');p.evaluate(shoot.STEP,30);p.wait_for_timeout(40)
  p.evaluate('()=>{boss._noHit=false;hammerStormStart(boss);boss._hammer.recovery.status="charging";boss._hammer.cp12Caption={text:"Gotta Recharge!",t:99};boss._hammer.t=1.8;drawScene(0);}');p.screenshot(path=str(O/'hammer-recharge.png'))
  r=p.evaluate('''()=>{const b=boss,h=b._hammer;h.state='shield';h.recovery=null;const hp=b.hp;const shots=eBullets.length;const dmg=hammerBossDamage(b,25);pBullets=[{x:b.x+100,y:b.y+85,vy:-5,kind:'mg',dead:false}];hammerBossTick(b,.001);return{damage:dmg,absorbed:pBullets[0].dead,enemyShotDelta:eBullets.length-shots,hpUnchanged:b.hp===hp};}''');assert r['damage']==0 and r['absorbed'] and r['enemyShotDelta']==0,r;results.append(r)
  p.evaluate('()=>{ht27Start();const d=boss._hammerTime;d.mode="break";d.t=2;d.clock=24;d.shield=true;d.locked=true;d.from={x:boss.x,y:boss.y};d.homeX=boss.x;d.homeY=boss.y;const y=ht27WallBounds(d).y;pBullets=[{x:boss.x,y,vy:-5,kind:"mg",dead:false}];d.reflections=[{x:1,y:1}];}')
  password=p.evaluate('()=>{ht27Tick(boss,.001);return {absorbed:pBullets[0]?.dead,reflections:boss._hammerTime.reflections.length}}');assert password['absorbed'] and password['reflections']==0,password;results.append(password)
  b.close()
finally:stop()
(O/'verification.json').write_text(json.dumps({'results':results,'errors':errors},indent=2));assert not errors,errors
