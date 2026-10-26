"""Native renderer fixtures for the requested Stage7/8 changes (not full-play footage)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF, STEP
from PIL import Image,ImageDraw
import base64,json

R=Path(__file__).resolve().parents[1];O=R/'_shots/stage78_review_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def ck(n,v,d=None):
    checks.append(dict(name=n,passed=bool(v),data=d));print(('PASS 'if v else'FAIL ')+n,flush=True)
    if not v:print(json.dumps(d),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof S78!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  def shot(name):
   p.evaluate('drawWorld(0)');file=O/(name+'.png');p.screenshot(path=str(file));shots.append((file,name))
  p.evaluate("()=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(7,'boss'),{pilot:'cole'});spawnBoss(debugFight.entry?.kind||'sludgeemperor');debugFight.spawned=true;bossActive=true;warnT=0;s7mInit(boss);s7mSet(boss,'recover');BOFCinematicDirector.cancel();DBGT.god=true;r25Warm(7);s7mWarm();}")
  p.wait_for_function('()=>{stageLoadTick();return r25Warm(7)&&stageLoadReady(7)}',timeout=180000)
  q=p.evaluate("""()=>{let n=0;for(const a of Object.values(R25_ART.legs))for(const f of a.frames){if(!XART.rdy(f.key)||!XART.rdy(f.white))return{n,ready:false};ctx.drawImage(XART.get(f.key),0,0,256,256);ctx.drawImage(XART.get(f.white),256,0,256,256);n++;}return{n,ready:true};}""")
  ck('All 32 walk and white-hit cells decode in the game context',q['ready']and q['n']==32,q)
  p.evaluate("()=>{boss.x=worldWidth()/2-65;boss.y=210;player.x=worldWidth()/2+130;player.y=VH-75;const M=boss._s7mod;M.r25Gait=null;s7mSet(boss,'chase');M.r25Walk=true;}")
  gait=[]
  for i in range(22):
   p.evaluate(STEP,4)
   q=p.evaluate("()=>{drawWorld(0);return{x:boss.x,y:boss.y,yaw:boss._s7mod.lean,legs:s7mPose(boss).filter(p=>p.r25).map(p=>({id:p.id,stance:p.stance,frame:p.frame,...s7mWorld(boss,p.toe)}))};}")
   gait.append(q)
   if i in [0,3,6,9,12,15,18,21]:shot('gait-'+str(i).zfill(2))
  planted=[]
  for a,b in zip(gait,gait[1:]):
   for x in a['legs']:
    y=next(z for z in b['legs']if z['id']==x['id'])
    if x['stance']and y['stance']and y['frame']>=x['frame']:planted.append(((x['x']-y['x'])**2+(x['y']-y['y'])**2)**.5)
  ck('Visible stance toes stay planted while the chassis travels',len(planted)>8 and max(planted)<.2,{'samples':len(planted),'maxDrift':max(planted,default=999),'travel':gait[-1]['x']-gait[0]['x']})
  ck('Opposite diagonal leg pairs use different recovery poses',any(len(set(x['frame']for x in q['legs']))>1 for q in gait))
  ck('Body steering remains bounded without attack rocking',max(abs(q['yaw'])for q in gait)<=.191)
  p.evaluate("()=>{const M=boss._s7mod;M.parts.find(p=>p.id==='frontL').hp=0;s7mSet(boss,'battery1009');}");p.evaluate(STEP,24);shot('warden-one-front-lost')
  ck('A destroyed leg stays absent from native targeting',p.evaluate("!s7mTargets(boss).some(t=>t.id==='frontL')"))
  p.evaluate("()=>{const M=boss._s7mod;for(const q of M.parts)q.hp=0;M.shield=0;M.core=5000;M.coreMax=5000;M.mode='laser';M.t=0;M.height=0;boss.flash=0;S78.pulses.delete(M);}")
  q=p.evaluate("""()=>{const b=boss,M=b._s7mod;drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;s7mHit(b,1,b.x,b.y,'core');drawWorld(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,timer:M.coreFlash};}""")
  ck('Warden native core hits still change visible pixels to white',q['white']>60 and q['timer']>0,q);shot('warden-hit')
  p.evaluate(STEP,11);p.evaluate('s7mHit(boss,1,boss.x,boss.y,"core");drawWorld(0)');shot('warden-repeated-hit-color')
  ck('Repeated core hits retain native timer while returning authored color',p.evaluate('boss._s7mod.coreFlash>0&&r25Pulse(boss._s7mod,boss._s7mod.coreFlash,boss._s7mod.clock)<.1'))
  p.evaluate(STEP,28);ck('Warden core flash expires natively',p.evaluate('boss._s7mod.coreFlash<=0'))
  p.close()
  p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{debugStartFight(debugFightFor(8,'boss'),{pilot:'cole'});spawnBoss('vileexistence');debugFight.spawned=true;bossActive=true;warnT=0;v18Warm();bi24Warm();r25Warm(8);}")
  try:p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bi24Warm()&&r25Warm(8)}',timeout=90000)
  except Exception:
   print(json.dumps(p.evaluate("()=>({stage:run.stage,load:stageLoadInfo(8),missing:[...v18Keys(),...bi24Keys(),...r25Keys(8)].filter(k=>!XART.rdy(k)).slice(0,25)})")),flush=True)
   raise
  p.evaluate("()=>{window.host78=()=>{const b=boss;b.parts=[];v18Budget(b);v18Enter(b,0,0);b._r30.v18.bi24Rolled=false;b._r30.v18.r25BallReady=false;b._r30.v18.arenaPhase=0;v18Fight(b);b.enter=false;b._noHit=false;b.x=worldWidth()/2;b.y=viewTopY()+220;BOFCinematicDirector.cancel();S78.debris=[];debugUnlocked=true;DBGT.god=true;run.lives=3;player.dead=false;player.out=false;player.invuln=1e9;setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;};host78();}")
  budget=p.evaluate('boss.parts.map(p=>({id:p.id,hp:p.hp}))');ck('First host retains 33.3 / 33.3 / 33.4 native budget',sum(q['hp']for q in budget)==p.evaluate('boss.maxhp'),budget)
  q=p.evaluate("()=>{const c=boss.parts.find(p=>p.id==='core'),hp=c.hp;boss._lastPart=c;modularHit(20);return{before:hp,after:c.hp};}");ck('Core remains protected while either arm lives',q['before']==q['after'],q)
  p.evaluate("()=>{host78();v18StartAttack(boss);const P=boss._r30.v18.attack;P.t=P.tell+.2;}");shot('eye-fire')
  q=p.evaluate("()=>{const e=rb23Eye(boss),q=r25HostSample(boss);return{eye:e,point:bi24World(boss,q.data.eye[0],q.data.eye[1]),offset:e.y-boss.y,frame:q.f};}");ck('Laser socket uses measured eye in the displayed connected pose',abs(q['eye']['y']-q['point']['y'])<.01 and q['eye']['w']>5,q)
  p.evaluate("()=>{host78();boss._r30.v18.rb23Seq=1;v18StartAttack(boss);}")
  for frames,label in [(20,'claw-raise'),(30,'claw-warning'),(25,'claw-fire'),(25,'claw-rockets')]:p.evaluate(STEP,frames);shot(label)
  events=p.evaluate("S78.events.filter(e=>e.type==='claw-shot').slice(-30)");ck('Raised claws release ordinary rounds and physical rockets',any(e['missile']for e in events)and any(not e['missile']for e in events),events[-4:])
  q=p.evaluate("()=>{const P=boss._r30.v18.attack;return{diffs:P.lanes.map(L=>{const q=rb23PartPoint(boss,boss.parts.find(p=>p.id===L.module),true);return Math.hypot(q.x-L.x,q.y-L.y)}),flashes:_navalFlashes.length,rockets:eBullets.filter(q=>q._v18Owner===boss&&q._shootable).map(q=>enemyOrdnanceCanIntercept(q))};}")
  ck('Claw FOV and the firing pose share exact socket origins',max(q['diffs'],default=999)<.01,q)
  ck('Native physical rockets are interceptable',len(q['rockets'])>0 and all(q['rockets']),q)
  p.evaluate("()=>{host78();const p=boss.parts.find(p=>p.id==='left');boss._lastPart=p;modularHit(p.hp);}");shot('arm-break');p.evaluate(STEP,20);shot('arm-shatter')
  q=p.evaluate("()=>{const b=boss,q=r25HostSample(b),im=r25Layer(q.name,'left',q.f),d=im.getContext('2d').getImageData(0,0,512,512).data;let point;for(let y=160;y<330&&!point;y++)for(let x=20;x<165;x++)if(d[(y*512+x)*4+3]>200){point=bi24World(b,x+.5,y+.5);break;}return{dead:b.parts.find(p=>p.id==='left').destroyed,target:retinaBossTargets(b).length,hit:r30At(b,point.x,point.y)?.id||null,shards:S78.debris.length,point};}")
  ck('Destroyed arm loses actual alpha hit region and Retina target',q['dead']and q['hit']is None and q['target']==1,q)
  ck('Arm physically breaks into authored alpha shards',q['shards']>=8,q)
  p.evaluate("()=>{const p=boss.parts.find(p=>p.id==='right');boss._lastPart=p;modularHit(p.hp);v18StartAttack(boss);}")
  positions=[]
  for i in range(22):
   p.evaluate(STEP,30);q=p.evaluate('({x:boss.x,y:boss.y,t:boss._r30.v18.attack?.t,drops:S78.events.filter(e=>e.type==="ball-code-drop").length})');positions.append(q)
   if i in [2,6,10,14,18]:shot('ball-'+str(i))
  drop=p.evaluate("S78.events.filter(e=>e.type==='ball-code-drop')")
  ck('Ball covers both sides and top/bottom without laser stops',max(q['x']for q in positions)-min(q['x']for q in positions)>200 and max(q['y']for q in positions)-min(q['y']for q in positions)>180,positions)
  ck('Ball drops spaced native code bombs with reaction time',len(drop)>=5 and all(q['warning']>=1.7 for q in drop),drop)
  ck('Ball remains folded between routes',p.evaluate('boss._r30.v18.r25BallReady&&boss._r30.v18.bi24Rolled'))
  p.evaluate("()=>{boss._lastPart=boss.parts[0];modularHit(boss.parts[0].hp+1);}");shot('host-fall-fragments')
  ck('Core exhaustion enters native rebirth once',p.evaluate("boss._r30.mode==='dr5er23rebirth'&&boss.hp===0"))
  p.evaluate("()=>{boss._r30.t=14;rb23SceneTick(boss,0);}")
  for t in [14,17,19,21,23,25.21,25.5]:p.evaluate('(t)=>{r25DebrisTick(Math.max(0,t-boss._r30.t));boss._r30.t=t;rb23SceneTick(boss,0);drawWorld(0)}',t);shot('download-'+str(t))
  q=p.evaluate('({download:S78.downloadLast,bolts:boss._r30.v18.rb23Rebirth.bolts,complete:boss._r30.v18.rb23Rebirth.r25Complete})');ck('Download reaches 100 percent after exactly 24 accelerating bolts',q['bolts']==24 and q['complete']and q['download']['progress']==1,q)
  p.evaluate('boss._r30.t=25.7;rb23SceneTick(boss,0)');shot('whiteout');ck('Native whiteout swaps into final arena',p.evaluate('j3State(boss).encounter===2&&boss._r30.v18.rb23Rebirth.swapped'))
  p.evaluate('boss._r30.t=28.6;rb23SceneTick(boss,0)');shot('final-reveal');ck('Reveal retains native protected final speech',p.evaluate("boss._r30.mode==='dr5Monologue'&&boss._noHit"))
  p.evaluate('host78();drawWorld(0)');shot('living-arena-a');before=p.evaluate('S78.arenaLast.t');p.evaluate(STEP,45);shot('living-arena-b');ck('Organic background advances independently of attacks',p.evaluate('S78.arenaLast.t')>before+.5,p.evaluate('({t:S78.arenaLast.t,clock:S78.arenaClock,state,mode:boss._r30.mode,dead:player.dead})'))
  q=p.evaluate("""async()=>{const a=Snd._audioCtx();await a.resume();const out=[];for(const k of ['enemyBossCannon','combatBeam0927','bossWeaponCharge','combatModule0927','timedBombBeep','timedBombBlast']){const d=await a.decodeAudioData(await(await fetch(BOFA.sfx[k])).arrayBuffer()),v=d.getChannelData(0);let peak=0;for(const x of v)peak=Math.max(peak,Math.abs(x));out.push({key:k,duration:d.duration,peak});}return out;}""")
  ck('Every updated attack uses decoded native mixer cues',all(q['peak']>.01 and q['duration']>0 for q in q),q)
  p.evaluate("r30Sound('enemyBossCannon')");p.wait_for_timeout(120);ck('Claw cue actually plays through shared mixer',p.evaluate("Snd.pools.enemyBossCannon.slots.some(s=>s?.el&&!s.el.paused&&s.el.currentTime>0)"))
  ck('No page, console or asset errors',not errors,errors);br.close()
finally:
 stop();(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8')
thumbs=Image.new('RGB',(4*320,((len(shots)+3)//4)*222),(5,10,17));g=ImageDraw.Draw(thumbs)
for i,(path,name)in enumerate(shots):thumbs.paste(Image.open(path).convert('RGB').resize((320,200)),((i%4)*320,(i//4)*222));g.text(((i%4)*320+4,(i//4)*222+202),name,fill='white')
thumbs.save(O/'contact.jpg')
print(json.dumps(dict(passed=sum(q['passed']for q in checks),failed=sum(not q['passed']for q in checks))))
raise SystemExit(0 if all(q['passed']for q in checks)else 1)
