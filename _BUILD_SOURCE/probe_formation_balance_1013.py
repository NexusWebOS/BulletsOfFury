from pathlib import Path
import sys,json,os
from playwright.sync_api import sync_playwright
R=Path(os.environ.get('BOF_REPO',str(Path(__file__).resolve().parents[1])))
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/formation_balance_1013';O.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(R));errors=[];rows=[];health=[]
RESET='''()=>{story=null;s6Opening=null;s6Wing=null;run._mission29OpeningDone=true;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;Input.keys={};player.dead=false;player.invuln=1e9+2;player.x=camLeftX()+VW*.5;player.y=PLAY.y+PLAY.h*.82;EP13.next=9999;enemies=[];eBullets=[];pBullets=[];VP12.groups=[];VP12.events=[];run._lifeThreat=run._threatBuild=0;run.wlevel=0;run.weaponLevels={};run.shield=0;run.speedLevel=0;run.missileLevel=0;}'''
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' and '404' not in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  for stage in [1,4,6,8]:
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   p.wait_for_function('n=>{stageLoadTick();return stageLoadReady(n)&&XART.rdy(VP12_ART[n].key)&&XART.rdy(AM13_ART["flight_variant_"+n].heading.key)&&XART.rdy(AM13_ART["flight_variant_"+n].roll.key)}',arg=stage,timeout=120000)
   for diff in ['easy','normal','hard','furious']:
    p.evaluate(RESET);p.evaluate('d=>{diffKey=d;DIFF=DIFFS[d]}',diff)
    h=p.evaluate('''()=>{const h=vp12FamilyHealth(run.stage),e=spawnEnemy(h.family,240,100);const reference={family:h.family,hp:e.hp,maxhp:e.maxhp,derived:h.hp};enemies=[];vp12Spawn('corner');reference.corner=enemies[0].hp;enemies=[];VP12.groups=[];vp12Spawn('orbit');reference.small=enemies[0].hp;const z=enemies[0];let hits=0;z._noHit=false;while(!z.dead&&z._dyingT==null&&hits<100){hitEnemy(z,2);hits++}reference.basePellets=hits;reference.destroyed=z.dead||z._dyingT!=null;return reference}''')
    assert h['hp']==h['corner']==h['derived'],(stage,diff,h)
    assert h['small']<=h['corner'] and h['small']<= {'easy':6,'normal':8,'hard':10,'furious':12}[diff],h
    assert h['destroyed'] and h['basePellets']<=6,h
    health.append({'stage':stage,'difficulty':diff,**h})
    for kind in ['orbit','corner','barrel','south','spiral','kamikaze','mixed']:
     p.evaluate(RESET);p.evaluate('t=>vp12Spawn(t)',kind)
     hps=p.evaluate('enemies.filter(e=>e._vp12).map(e=>e.hp)')
     assert p.evaluate('enemies.filter(e=>e._vp12).every(e=>!e._cn)'), 'hidden native cannon'
     p.evaluate('''()=>{window.__seenShots=[];window.__seenKeys=new Set();window.__qaTick=()=>{for(const e of enemies)if(e._vp12){const q=e._vp12.q;while((q.probed||0)<q.shot){q.probed=(q.probed||0)+1;__seenShots.push({slot:q.slot,shot:q.probed,age:e._vp12.g.age})}if(e._air13RenderedKey)__seenKeys.add(e._air13RenderedKey)}}}''')
     for tick in range(16):
      err=p.evaluate(shoot.STEP,30);assert err is None,err;p.wait_for_timeout(5)
      if diff=='normal' and kind in ['corner','barrel','orbit'] and tick==3:p.screenshot(path=str(O/f's{stage}-{kind}.png'))
     q=p.evaluate('''()=>({state,events:VP12.events,shots:__seenShots,keys:[...__seenKeys],live:enemies.filter(e=>e._vp12&&!e.dead&&e._dyingT==null).length,finite:enemies.filter(e=>e._vp12).every(e=>Number.isFinite(e.x)&&Number.isFinite(e.y)),bullets:eBullets.filter(b=>b._vp12).length})''')
     assert q['state']=='play' and q['finite'] and q['keys'],(stage,diff,kind,q)
     assert kind=='kamikaze' or q['shots'],(stage,diff,kind,q)
     assert len(hps)=={'easy':3,'normal':5,'hard':7,'furious':9}[diff],hps
     rows.append({'stage':stage,'difficulty':diff,'pattern':kind,'hp':hps[0],**q})
    print('PASS',stage,diff,'familyHP',h['hp'],'smallHP',h['small'],'basePellets',h['basePellets'],flush=True)
   # Death immediately cancels release rather than letting its borrowed drone cannon fire.
   p.evaluate(RESET);p.evaluate('()=>{vp12Spawn("orbit");for(const e of enemies){e._noHit=false;hitEnemy(e,999);hitEnemy(e,999)}eBullets=[];VP12.events=[]}')
   assert p.evaluate(shoot.STEP,50) is None
   assert p.evaluate('eBullets.length===0&&!VP12.events.some(e=>e.event==="volley")')
   p.evaluate(RESET);p.evaluate('()=>{vp12Spawn("corner");warnT=1}');assert p.evaluate(shoot.STEP,3) is None
   assert p.evaluate('enemies.filter(e=>e._vp12&&!e.dead).length')==0
  b.close()
finally:
 stop();(O/'verification.json').write_text(json.dumps({'health':health,'patterns':rows,'errors':errors},indent=2))
assert not errors,errors
print('PASS',len(rows),'native formation fixtures and',len(health),'native HP/collision comparisons; zero errors')
