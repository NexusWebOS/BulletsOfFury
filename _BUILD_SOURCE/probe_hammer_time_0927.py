"""Native password encounter, authored dance pixels and locked-break controls."""
import base64,json,http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/hammer_time_ship_0927');OUT.mkdir(exist_ok=True,parents=True)
def shot(p,name):
 p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0)}')
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
def seek(p,t):
 p.evaluate("async t=>{const m=Snd.music.hammerTime;await new Promise(r=>{m.addEventListener('seeked',r,{once:true});m.currentTime=t;});await m.play();}",t)
 p.wait_for_function('()=>Snd.music.hammerTime.readyState>=2&&!Snd.music.hammerTime.paused')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1050});p.set_default_timeout(60000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  # Keep the physical desktop controller from steering this keyboard-driven fixture.
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF)
  report['password']=p.evaluate("()=>{setState(GS.PASSWORD);pwInput='';for(const ch of 'HAMMER')pwKey(ch);pwKey('ENTER');return {state,pending:ht27Pending,stage:PENDING_STAGE};}")
  p.evaluate("()=>{diffKey='normal';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(PENDING_STAGE);}")
  p.wait_for_function("()=>Object.keys(HAMMER_TIME_ART.sheets).every(k=>XART.rdy('ht27_'+k))&&XART.rdy('arch_ship_transform')&&XART.rdy('arch_orbital_sweep_0926')&&furyShipReady()&&Snd.music.hammerTime.readyState>=2")
  # shoot.py's tiny HTTP server has no byte-range support. A complete local Blob of
  # the SAME shipped MP3 makes explicit seek fixtures reliable in Chromium.
  p.evaluate("async()=>{const m=Snd.music.hammerTime,b=await(await fetch(HAMMER_TIME_ART.audio.path)).blob();m.src=URL.createObjectURL(b);m.load();await new Promise(r=>m.addEventListener('canplaythrough',r,{once:true}));await m.play();}")
  p.evaluate('()=>updatePlay(1/60)')
  report['start']=p.evaluate("()=>({state,active:ht27Active,kind:boss.kind,hp:boss.hp,music:Snd.cur===Snd.music.hammerTime,space:spaceShipActive()})")
  report['entry']=p.evaluate("()=>({x:player.x,y:player.y,ammo:run.bombs,hp:boss.hp,locked:ht27Locked()})")
  for t,name in [(1,'entry-ship'),(2.8,'entry-unfold'),(5.5,'entry-windup'),(6.2,'entry-impact'),(6.9,'entry-helpers'),(10,'wall-rising'),(15.9,'entry-ready')]:
   seek(p,t)
   p.evaluate("()=>{for(const a of ['up','fire','bomb'])for(const k of keybind[a])Input.keys[k]=true;for(let i=0;i<30;i++)updatePlay(1/60);pShoot();useBomb();startSpecial();setState('paused');}")
   shot(p,name)
   if name=='entry-ship':report['ship']=p.evaluate("()=>{let found=false;const get=XART.get;XART.get=function(k){if(k==='arch_ship_transform')found=true;return get.call(XART,k);};try{ht27Draw(boss);}finally{XART.get=get;}return {drawn:found,frame:boss._hammerTime.shipFrame,time:boss._hammerTime.clock,music:Snd.cur===Snd.music.hammerTime};}")
   if name=='entry-impact':report['entryImpact']=p.evaluate("()=>({x:player.x,y:player.y,ammo:run.bombs,hp:boss.hp,locked:ht27Locked(),slammed:boss._hammerTime.slammed,helpers:boss._hammerTime.helpers.length,shots:pBullets.length,state})")
  report['entryReady']=p.evaluate("()=>{const r={locked:ht27Locked(),helpers:boss._hammerTime.helpers.length,allArrived:boss._hammerTime.helpers.every(q=>q.spawn===1),wall:ht27WallBounds(boss._hammerTime)};for(const k of Object.keys(Input.keys))Input.keys[k]=false;return r;}")
  seek(p,16.1)
  report['clockDebug']=p.evaluate("()=>({t:Snd.music.hammerTime.currentTime,paused:Snd.music.hammerTime.paused,ready:Snd.music.hammerTime.readyState,active:ht27Active,dead:boss.dead,wrapper:updatePlay.toString().slice(0,300),audio:HAMMER_TIME_ART.audio.breakStart})")
  report['lock']=p.evaluate("""()=>{const before={x:player.x,y:player.y,bombs:run.bombs,lives:run.lives};
   updatePlay(1/60);const first={time:boss._hammerTime.clock,mode:boss._hammerTime.mode,locked:ht27Locked()};for(const k of [...keybind.up,...keybind.fire,...keybind.bomb])Input.keys[k]=true;
   for(let i=0;i<60;i++)updatePlay(1/60);pShoot();useBomb();spaceLaserFire();spaceVolleyLaunchRack(3);startSpecial();setState('paused');
   return {first,time:Snd.music.hammerTime.currentTime,clock:boss._hammerTime.clock,before,after:{x:player.x,y:player.y,bombs:run.bombs,lives:run.lives},state,locked:ht27Locked(),shield:boss._hammerTime.shield,shots:pBullets.length,helpers:boss._hammerTime.helpers.length,special:!!special};}""")
  shot(p,'shield-stop')
  seek(p,19);p.evaluate("()=>{boss._hammerTime.t=3;updatePlay(1/60);}");shot(p,'shield-twirl')
  report['shieldDamage']=p.evaluate("()=>{const hp=boss.hp;hitBoss(100);return {before:hp,after:boss.hp};}")
  seek(p,24.2)
  report['release']=p.evaluate("""()=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;updatePlay(1/60);const x=player.x;for(const k of keybind.right)Input.keys[k]=true;updatePlay(1/60);pShoot();const r={locked:ht27Locked(),moved:player.x>x,shots:pBullets.length};setState('paused');r.pause=state;setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;return r;}""")
  p.evaluate("()=>{Snd.music.hammerTime.currentTime=30;ht27Attack(boss,boss._hammerTime);}");p.evaluate(sh.STEP,35);shot(p,'attack')
  report['attack']=p.evaluate("()=>({mode:boss._hammerTime.mode,hammerState:boss._hammer.state,zoom:viewZoom(),finite:eBullets.every(b=>Number.isFinite(b.x+b.y))})")
  report['cleanup']=p.evaluate("()=>{setState(GS.TITLE);const r={active:ht27Active,locked:ht27Locked(),music:Snd.cur===Snd.music.hammerTime};startRun(5);r.normalBoss=!(boss&&boss._hammerTime)&&!ht27Active;return r;}")
  report['difficulty']=[]
  for diff in ['easy','normal','hard','furious','insanity']:
   p.evaluate("d=>{setState(GS.TITLE);diffKey=d;DIFF=DIFFS[d];pwInput='HAMMER';submitPassword();startRun(5);Snd.music.hammerTime.pause();boss._hammerTime.clock=30;boss.hp=boss.maxhp*.6;boss.y=VH*.34;ht27Summon(boss._hammerTime,true);for(const q of boss._hammerTime.helpers){q.spawn=1;q.arrived=true;}ht27DanceStart(boss,boss._hammerTime,.1);player.invuln=999;window.htSeen=[];}",diff)
   for _ in range(36):
    p.evaluate("()=>{for(let i=0;i<60;i++){player.invuln=999;updatePlay(1/60);if(!htSeen.includes(boss._hammer.state))htSeen.push(boss._hammer.state);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}")
    p.wait_for_timeout(15)
   shot(p,'combat-'+diff)
   report['difficulty'].append(p.evaluate("()=>({difficulty:diffKey,states:htSeen,finite:eBullets.every(q=>Number.isFinite(q.x+q.y)),zoom:viewZoom(),active:ht27Active})"))
  report['helpers']=[]
  for diff in ['normal','hard','insanity']:
   p.evaluate("diff=>{diffKey=diff;DIFF=DIFFS[diff];boss._hammerTime.clock=30;ht27DanceStart(boss,boss._hammerTime,100);eBullets=[];pBullets=[];boss._hammerTime.helpers=[];ht27Summon(boss._hammerTime,true);for(const q of boss._hammerTime.helpers){q.spawn=1;q.arrived=true;q.shotCd=0;}window.htMaxActive=0;}",diff)
   for i in range(7):
    p.evaluate("()=>{for(let i=0;i<30;i++){ht27Helpers(boss,boss._hammerTime,1/60);htMaxActive=Math.max(htMaxActive,boss._hammerTime.helpers.filter(q=>q.aim||q.burst).length);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}")
    if i==0:shot(p,'helper-warning-'+diff)
   report['helpers'].append(p.evaluate("()=>{const q=boss._hammerTime.helpers[0],before=q.hp,listed=_lockTargets().includes(q)&&spaceTargets().includes(q);spaceDamageTarget(q,5,{x:q.x,y:q.y,kind:'spaceVolley'});return {difficulty:diffKey,shots:eBullets.filter(q=>q._ht27Helper).length,maxActive:htMaxActive,listed,damage:before-q.hp};}"))
  p.evaluate("()=>{boss._hammerTime.shield=true;boss._hammerTime.mode='break';boss._hammerTime.t=3;}");shot(p,'flat-wall')
  report['wall']=p.evaluate("()=>{let next=false,calls=[];const get=XART.get,draw=ctx.drawImage;XART.get=function(k){if(k==='ht27_wall')next=true;return get.call(XART,k);};ctx.drawImage=function(...a){if(next){calls.push({alpha:ctx.globalAlpha,dest:a.slice(5)});next=false;}return draw.apply(ctx,a);};try{ht27Draw(boss);}finally{XART.get=get;ctx.drawImage=draw;}return {calls,bounds:ht27WallBounds()};}")
  report['preVictory']=p.evaluate("()=>({state,titlePending,keys:Input.keys,mouse:Input.mouse,active:ht27Active})")
  p.evaluate("()=>{window.htExits=[];const base=setState;setState=function(s){const result=base(s);htExits.push({requested:s,actual:state});return result;};}")
  p.evaluate("()=>{boss.hp=1;boss._noHit=false;boss._hammerTime.mode='dance';boss._hammerTime.shield=false;hitBoss(99999);}")
  for _ in range(36):
   p.evaluate(sh.STEP,90);p.wait_for_timeout(15)
   if not p.evaluate('()=>ht27Active'):break
  report['victory']=p.evaluate("()=>({dead:boss?.dead,active:ht27Active,state,music:Snd.cur===Snd.music.hammerTime,exits:htExits})")
  report['errors']=errors;br.close()
finally:stop()
(OUT/'native.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert not errors,errors
assert report['password']=={'state':'diff','pending':True,'stage':5},report['password']
assert report['start']['active'] and report['start']['music'] and report['start']['space']
assert report['lock']['locked'] and report['lock']['shield'] and report['lock']['before']==report['lock']['after'] and report['lock']['state']=='play' and report['lock']['shots']==0 and not report['lock']['special']
assert report['shieldDamage']['before']==report['shieldDamage']['after']
assert not report['release']['locked'] and report['release']['moved'] and report['release']['shots']>0 and report['release']['pause']=='paused'
assert not report['cleanup']['active'] and report['cleanup']['normalBoss'] and not report['cleanup']['music']
assert all(q['finite'] and q['zoom']==1 and q['active'] and 'ball' in q['states'] for q in report['difficulty'])
assert not report['victory']['active'] and not report['victory']['music'] and report['victory']['state']=='title'

a=report['entry'];b=report['entryImpact']
assert all(a[k]==b[k] for k in ['x','y','ammo','hp']) and b['locked'] and b['slammed'] and b['shots']==0 and b['state']=='play'
assert report['ship']['drawn'] and report['ship']['frame']==15 and report['ship']['music']
assert report['entryReady']['locked'] and report['entryReady']['helpers']==4 and report['entryReady']['allArrived']
assert len(report['wall']['calls'])==1 and report['wall']['calls'][0]['alpha']==.5
assert all(q['maxActive']<=1 and (q['shots']>0)==(q['difficulty']!='normal') and q['listed']==(q['difficulty']!='normal') and q['damage']==(0 if q['difficulty']=='normal' else 5) for q in report['helpers'])
