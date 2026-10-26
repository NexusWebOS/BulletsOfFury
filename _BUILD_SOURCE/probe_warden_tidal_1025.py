"""Real Chromium coverage through shoot.py. Explicit fixtures are recorded as such.
Actual canvas differences verify connected arms, liquid motion and hit flashes.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
from PIL import Image,ImageDraw
import json,http.server,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_tidal_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];trails=[]
def ck(name,value,data=None):
 checks.append({'name':name,'passed':bool(value),'data':data});print(('PASS 'if value else'FAIL ')+name,flush=True)
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1';http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800})
  def page(stage):
   p=bc.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
   p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof WT25!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
   p.evaluate("n=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(n,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(n,'boss').kind);debugFight.spawned=true;bossActive=true;warnT=0;BOFCinematicDirector.cancel();DBGT.god=true;run.lives=3;player.dead=false;player.invuln=1e9;setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;}",stage)
   p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=180000)
   return p
  def shot(p,name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p=page(7)
  p.evaluate("()=>{s7mWarm();r25Warm(7);bm9Warm(bm9StageNames(7));window.wt7Setup=(mode,x,y)=>{const b=boss,M=s7mInit(b);b.enter=false;b.x=x;b.y=y;b._drawY=y;M.height=M.drop=M.lean=0;M._mission29IntroDone=true;M.r25Gait=null;M.counterTell=null;M.frExit=null;s7mSet(b,mode);for(const q of M.parts)q.hp=q.max;player.x=worldWidth()/2;player.y=VH-55;};wt7Setup('recover',worldWidth()/2,175);}")
  p.wait_for_function('r25Warm(7)&&bm9StageNames(7).every(n=>BM9_ART[n].every(a=>XART.rdy(a.key)))',timeout=180000)
  p.evaluate("()=>{wt7Setup('chase',worldWidth()/2,215);const G=r25Gait(boss);G.walks=1;boss._s7mod.r25Walk=true;player.x=boss.x-Math.sin(4.79992)*80;player.y=boss.y+145;window.wtFloorStart=mapScroll;}")
  trail=[]
  for i in range(18):
   p.evaluate(STEP,4);trail.append(p.evaluate("()=>({x:boss.x,y:boss.y,floor:mapScroll,rate:s7WardenReverseScroll(),distance:boss._s7mod.r25Gait.distance,speed:boss._s7mod.r25Gait.speed,legs:s7mPose(boss).filter(p=>p.r25).map(p=>({id:p.id,f:p.frame,stance:p.stance,...s7mWorld(boss,p.toe)}))})"))
   if i in [0,4,8,12,17]:shot(p,'warden-floor-'+str(i))
  ck('Retreating floor drives walking even with a stationary screen chassis',trail[0]['floor']-trail[-1]['floor']>70 and len(set(q['legs'][0]['f']for q in trail))>=5,trail)
  planted=[]
  for a,z in zip(trail,trail[1:]):
   for q in a['legs']:
    n=next(n for n in z['legs']if n['id']==q['id'])
    if q['stance']and n['stance']and n['f']>=q['f']:planted.append(abs((n['y']-q['y'])-(z['floor']-a['floor'])))
  ck('Stance feet travel with the actual retreating floor',len(planted)>=8 and max(planted)<.35,{'samples':len(planted),'max':max(planted,default=999)})
  p.evaluate("()=>wt7Setup('recover',worldWidth()/2,320)");trail=[]
  for i in range(6):p.evaluate(STEP,4);trail.append(p.evaluate('({y:boss.y,speed:boss._s7mod.r25Gait.speed,frames:s7mPose(boss).filter(p=>p.r25).map(p=>p.frame)})'))
  ck('Backward recovery uses leg motion on every moving update',all(q['speed']>1 for q in trail)and len(set(q['frames'][0]for q in trail))>=2,trail);shot(p,'warden-backward')
  p.evaluate("()=>wt7Setup('battery1009',worldWidth()/2,175)")
  mounts=p.evaluate("()=>{const M=boss._s7mod,out=[];for(const mode of ['battery1009','chaingun','aim','chain','recover','entry','jump','stomp','bounce']){s7mSet(boss,mode);for(const t of [0,.3,.65,1.2,2]){M.t=t;M.bm9Kick={gunL:1,gunR:.75};M.cgAng={gunL:.8,gunR:2.2};out.push({mode,t,guns:s7mPose(boss).filter(p=>p.id.startsWith('gun')).map(p=>({id:p.id,x:p.x+Math.sin(p.a)*37,y:p.y-Math.cos(p.a)*37,w:p.w,h:p.h,angle:p.a,muzzle:s7mMuzzle(boss,p.id)}))});}}return out;}")
  ck('Both turret trunnions stay fixed in every firing and recoil pose',all(abs(g['x']-(-34 if g['id']=='gunL'else 34))<.001 and abs(g['y']-12)<.001 and g['w']==34 and g['h']==84 for q in mounts for g in q['guns']),mounts)
  ck('Turrets change firing angle without changing hull socket',len(set(round(g['angle'],2)for q in mounts for g in q['guns']))>=3)
  arm_pixels=[]
  for mode in ['swipeL','swipeR','swipeX','jump','stomp','bounce']:
   p.evaluate("m=>wt7Setup(m,worldWidth()/2,215)",mode)
   for t in [0,.7,1.15,1.30,1.65,2.0]:
    q=p.evaluate("t=>{boss._s7mod.t=t;const M=boss._s7mod,out=[];drawWorld(0);for(const id of ['frontL','frontR']){const a=ctx.getImageData(0,0,cv.width,cv.height).data,p=M.parts.find(p=>p.id===id),hp=p.hp;p.hp=0;drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<a.length;i+=4)if(Math.abs(a[i]-z[i])+Math.abs(a[i+1]-z[i+1])+Math.abs(a[i+2]-z[i+2])>45)changed++;p.hp=hp;drawWorld(0);out.push({id,changed,pose:s7mPose(boss).find(p=>p.id===id)});}return out;}",t);arm_pixels.append({'mode':mode,'t':t,'arms':q})
    if t in [.7,1.30,2.0]:shot(p,'warden-'+mode+'-'+str(t))
  ck('Both live claws retain actual visible pixels throughout all swipe returns',all(a['changed']>80 and a['pose']['r25']for q in arm_pixels for a in q['arms']),arm_pixels)
  p.evaluate("()=>{wt7Setup('bh25',worldWidth()/2,175);bh25Start(boss,'warden',()=>s7mSet(boss,'recover'));}");p.evaluate(STEP,12)
  ck('Warden braces for its barrage and does not scroll the floor',p.evaluate('boss._s7mod.mode==="bh25"&&s7WardenReverseScroll()===0&&boss._s7mod.r25Gait.speed===0'));shot(p,'warden-braced-barrage')
  p.evaluate("()=>{bh25Cancel(boss,'fixture-end');wt7Setup('recover',worldWidth()/2,175);const M=boss._s7mod;for(const q of M.parts.filter(p=>p.id.startsWith('front')||p.id.startsWith('rear')))q.hp=0;M.mode='crawl';}")
  ck('No retreat scroll remains after the actual leg budget is exhausted',p.evaluate('s7WardenReverseScroll()===0'))
  p.close();p=page(9);p.wait_for_function('wt25Warm()',timeout=180000);p.evaluate(STEP,130)
  ck('Warp sentinels keep their native pre-fusion state',p.evaluate('boss._s9fusion.phase==="twins"&&!boss._wt25'))
  p.evaluate("()=>{for(const w of [boss._s9fusion.left,boss._s9fusion.right]){s9FusionHitTest(boss,w.x,w.y);s9FusionHit(boss,w.hp);}}")
  ck('Native damage to both sentinels begins their convergence',p.evaluate('boss._s9fusion.phase==="fuse"&&boss._s9fusion.left.disabled&&boss._s9fusion.right.disabled'));shot(p,'native-convergence')
  transition=None
  for i in range(170):
   p.evaluate(STEP,1)
   if p.evaluate('boss._s9fusion.phase==="tidal"'):
    transition=p.evaluate('({hp:boss.hp,max:boss.maxhp,expected:Math.ceil(5000*DIFF.eHp),owner:!!boss._wt25})');break
  ck('The first live water frame exposes its complete final HP pool once',transition and transition['owner']and transition['hp']==transition['max']==transition['expected'],transition)
  p.evaluate(STEP,35);p.wait_for_timeout(100);p.evaluate(STEP,2)
  ck('Native convergence enters the complete Tidal Sovereign owner',p.evaluate('boss._s9fusion.phase==="tidal"&&!!boss._wt25&&boss.name==="TIDAL SOVEREIGN"'))
  budget=p.evaluate('({hp:boss.hp,max:boss.maxhp,expected:Math.ceil(5000*DIFF.eHp),ring:boss._s9fusion.ringT})');ck('Native water HP budget and portal collapse clock are retained',budget['hp']==budget['max']==budget['expected']and budget['ring']>0,budget)
  q=p.evaluate("()=>{let n=0;for(const bank of Object.values(WT25_ART.banks))for(const f of bank.frames){if(!XART.rdy(f.key))return{n,ready:false};ctx.drawImage(XART.get(f.key),0,0);n++;}return{n,ready:true};}");ck('All 96 even fixed-canvas liquid hull frames decode in the native context',q['ready']and q['n']==96,q)
  q=p.evaluate("()=>{const a=wt25Frame('ns9_tidal_intact',0),z=wt25Frame('ns9_tidal_intact',.58),g=document.createElement('canvas');g.width=320;g.height=256;const c=g.getContext('2d');c.drawImage(a,0,0);const x=c.getImageData(0,0,320,256).data;c.clearRect(0,0,320,256);c.drawImage(z,0,0);const y=c.getImageData(0,0,320,256).data;let changed=0,alpha=0;for(let i=0;i<x.length;i+=4){if(x[i]!==y[i]||x[i+1]!==y[i+1]||x[i+2]!==y[i+2])changed++;if(x[i+3]!==y[i+3])alpha++;}return{changed,alpha};}");ck('Liquid pixels actually animate while the whole hull alpha stays fixed',q['changed']>2000 and q['alpha']==0,q)
  q=p.evaluate("()=>{const k='ns9_tidal_intact',T=boss._wt25;T.attack=null;T.rest=20;T.clock=0;drawWorld(0);window.wtNativeBefore=ctx.getImageData(0,0,cv.width,cv.height).data;T.clock=.58;drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<z.length;i+=4)if(Math.abs(z[i]-wtNativeBefore[i])+Math.abs(z[i+1]-wtNativeBefore[i+1])+Math.abs(z[i+2]-wtNativeBefore[i+2])>30)changed++;return{changed};}");ck('Native shipBossDraw displays moving liquid pixels',q['changed']>1000,q);shot(p,'living-water-hull')
  q=p.evaluate("()=>{const b=boss,out=[];for(const [slot,a]of Object.entries(WT25_ART.sockets)){const q=shipBossMount(b,slot),z=wt25Point(b,...a);out.push({slot,d:Math.hypot(q.x-z.x,q.y-z.y),...q});}return out;}");ck('Circle launchers and lower cannon sockets follow the displayed hull',all(q['d']<.001 for q in q),q)
  q=p.evaluate("()=>{const c=document.createElement('canvas');c.width=320;c.height=256;const g=c.getContext('2d');g.drawImage(XART.get('ns9_tidal_intact'),0,0);return Object.entries(WT25_ART.sockets).map(([slot,a])=>({slot,pixels:[...g.getImageData(a[0]-2,a[1]-2,5,5).data]}));}");ck('Measured water sockets overlap actual authored opaque blue pixels',all(any(q['pixels'][i+3]>100 and q['pixels'][i+2]>q['pixels'][i]+30 for i in range(0,len(q['pixels']),4))for q in q))
  ck('Supplemental targeting cannot create a second water attack owner',p.evaluate("!target17Ready(boss,target17Ports(boss,'water'))&&boss._target17?.phase!=='track'"))
  q=p.evaluate("()=>{const b=boss,T=b._wt25;T.attack=null;T.rest=100;T.geysers=[];T.mortars=[];T.walls=[{y:VH-100,gapX:worldWidth()/2,gap:150,speed:120,t:0}];player.y=VH-100;player.x=worldWidth()/2;let n=DBGT.stats.godBlocks;wt25DangerTick(b,0);const safe=DBGT.stats.godBlocks-n;player.x=camLeftX()+60;n=DBGT.stats.godBlocks;wt25DangerTick(b,0);const flooded=DBGT.stats.godBlocks-n;T.walls=[];return{safe,flooded};}");ck('Native flood collision leaves the visible opening safe',q['safe']==0 and q['flooded']>0,q)
  q=p.evaluate("()=>{const b=boss,T=b._wt25;T.geysers=[{x:worldWidth()/2,y:VH-90,t:.3,life:.8,height:196,width:36}];player.x=worldWidth()/2;player.y=VH-180;let n=DBGT.stats.godBlocks;wt25DangerTick(b,0);const spire=DBGT.stats.godBlocks-n;player.x+=80;n=DBGT.stats.godBlocks;wt25DangerTick(b,0);const outside=DBGT.stats.godBlocks-n;T.geysers=[];return{spire,outside};}");ck('Native geyser collision matches the visible spire and leaves side space',q['spire']>0 and q['outside']==0,q)
  q=p.evaluate("()=>{const b=boss,T=b._wt25,P=wt25Start(b,'mortars'),Q=P.plans[0];wt25Mortar(b,Q);const m=T.mortars[0];m.q.dead=true;const before=T.geysers.length;wt25DangerTick(b,.05);T.attack=null;return{remaining:T.mortars.length,newPlumes:T.geysers.length-before};}");ck('A defensive mortar clear cancels its pending eruption',q['remaining']==0 and q['newPlumes']==0,q)
  q=p.evaluate("()=>{const T=boss._wt25,n=T.clock;for(let i=0;i<8;i++)drawWorld(0);return{before:n,after:T.clock};}");ck('Repeated draws cannot advance the water animation or hazard clock',q['before']==q['after'],q)
  q=p.evaluate("()=>{const out=[];for(const key of ['normal','hard','furious']){diffKey=key;const flood=wt25Start(boss,'flood'),mist=wt25Start(boss,'mist');out.push({key,waves:flood.waves,warm:flood.warm,mistWarm:mist.plans[0].tell});}diffKey='furious';boss._wt25.attack=null;return out;}");ck('Normal and Hard retain fewer flood rows and longer reaction windows',q[0]['waves']<q[2]['waves']and q[1]['waves']<q[2]['waves']and q[0]['warm']>q[2]['warm']and q[1]['mistWarm']>q[2]['mistWarm'],q)
  p.evaluate('player.x=worldWidth()/2;player.y=VH-65')
  edges=[]
  for x,label in [(25,'left'),(655,'right')]:
   p.evaluate('(x)=>{player.x=x;boss._wt25.attack=null;boss._wt25.rest=100;}',x)
   for i in range(10):p.evaluate(STEP,12)
   edges.append(p.evaluate('({left:boss.x-boss.w/2,right:boss.x+boss.w/2,viewLeft:camLeftX(),viewRight:camRightX()})'));shot(p,'whole-tidal-camera-'+label)
  ck('The complete authored water hull stays visible at both camera edges',all(q['left']>=q['viewLeft']+8 and q['right']<=q['viewRight']-8 for q in edges),edges)
  p.evaluate('player.x=worldWidth()/2;player.y=VH-65')
  p.evaluate("()=>{const T=boss._wt25;T.rest=.05;T.seq=0;T.attack=null;WT25.events=[];}")
  coverage=[];seen=set();maxbullets=0;maxwalls=0;proof=True;proofsamples=0
  for batch in range(600):
   p.evaluate(STEP,10)
   q=p.evaluate("()=>{const T=boss._wt25,P=T.attack,qs=eBullets.filter(q=>q._wt25Owner&&!q.dead);return{clock:T.clock,kind:P?.kind,age:P?.t,fired:P?.fired,walls:T.walls.length,geysers:T.geysers.length,mortars:T.mortars.length,bullets:qs.length,ordinary:qs.filter(q=>!q._wt25Physical).every(q=>!enemyOrdnanceCanIntercept(q)&&!q._shootable&&!enemyDefensiveProof(q)),done:WT25.events.filter(e=>e.event==='water-attack-complete').map(e=>e.kind)};}")
   coverage.append(q);maxbullets=max(maxbullets,q['bullets']);maxwalls=max(maxwalls,q['walls'])
   if q['bullets']:proofsamples+=1;proof=proof and q['ordinary']
   kind=q.get('kind');label=None
   if kind and kind+'-tell'not in seen and q.get('fired',0)==0:label=kind+'-tell'
   elif kind and kind+'-fire'not in seen and q.get('fired',0)>0:label=kind+'-fire'
   elif kind and kind+'-field'not in seen and ((q['walls']and q['age']>3.5)or q['geysers']or q['mortars']or q['bullets']>40):label=kind+'-field'
   if label:seen.add(label);shot(p,label)
   if len(set(q['done']))>=6:break
   if batch%9==0:p.wait_for_timeout(1)
  ev=p.evaluate('WT25.events');(O/'water-events.json').write_text(json.dumps(ev,indent=2),encoding='utf8');(O/'water-coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf8')
  for kind in ['flood','geysers','mortars','mist','undertow','maelstrom']:ck('Native scheduler completes '+kind+' and leaves recovery',kind in q['done'])
  ck('Water attacks keep finite wall and bullet budgets',0<maxwalls<=3 and 0<maxbullets<=110,{'bullets':maxbullets,'walls':maxwalls})
  ck('Water energy remains ordinary unshootable ordnance with defensive clears',proof and proofsamples>20,proofsamples)
  ck('Water laser mortars launch from both measured circles',set(e['slot']for e in ev if e['event']=='circle-mortar-launch')=={'circleL','circleR'})
  ck('Mist pressure lasers fire from both lower turrets',set(e['slot']for e in ev if e['event']=='turret-mist-fire')=={'L','R'})
  p.evaluate("()=>{const b=boss,T=b._wt25;T.attack=null;T.rest=20;for(const q of eBullets)if(q._wt25Owner===b)q.dead=true;}");p.evaluate(STEP,24)
  q=p.evaluate("()=>{const b=boss,T=b._wt25;drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,hp=b.hp;hitBoss(1);drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<z.length;i+=4)if(z[i]>240&&z[i+1]>240&&z[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,hpBefore:hp,hpAfter:b.hp,flash:b.flash};}");ck('Native Tidal damage changes actual armor pixels to white',q['white']>500 and q['hpAfter']<q['hpBefore']and q['flash']>0,q);shot(p,'tidal-native-hit');p.evaluate(STEP,24);ck('Tidal hit flash expires through its native timer',p.evaluate('boss.flash<=0'))
  q=p.evaluate("()=>{const b=boss,o=wt25Shot(b,'circleL',Math.PI/2,2,'tidalmine'),m=wt25Shot(b,'L',Math.PI/2,1.8,'tidaltorp',true);return{ordinary:enemyOrdnanceCanIntercept(o),defensive:enemyDefensiveProof(o),physical:enemyOrdnanceCanIntercept(m),physicalHP:m.hp};}");ck('First-frame ordinary water cannot be intercepted; real torpedoes can',not q['ordinary']and not q['defensive']and q['physical']and q['physicalHP']==3,q)
  q=p.evaluate("async()=>{const a=Snd._audioCtx();await a.resume();const out=[];for(const k of WT25.cues){const d=await a.decodeAudioData(await(await fetch(BOFA.sfx[k])).arrayBuffer());let peak=0;for(const v of d.getChannelData(0))peak=Math.max(peak,Math.abs(v));out.push({key:k,duration:d.duration,peak});}return out;}");ck('All six water cues decode as audible native audio',all(a['duration']>0 and a['peak']>.01 for a in q),q)
  p.evaluate("wt25Cue(boss,'bossfireTidalfusion',0)");p.wait_for_timeout(150);ck('Water release plays through the shared mixer',p.evaluate('Snd.pools.bossfireTidalfusion.slots.some(s=>s?.el&&!s.el.paused&&s.el.currentTime>0)'))
  p.evaluate("()=>{const b=boss;wt25Start(b,'flood');b._wt25.walls.push({y:350,gapX:350,gap:150,speed:100,t:0});b.dead=true;updatePlay(0);}");ck('Native owner loss cancels all pending water hazards and releases',p.evaluate('!WT25.owners.has(boss)&&!boss._wt25.attack&&!boss._wt25.walls.length&&!boss._wt25.geysers.length&&!boss._wt25.mortars.length&&eBullets.every(q=>q._wt25Owner!==boss||q.dead)'))
  ck('No page, console or failed asset responses',not errors,errors);br.close()
finally:
 stop();(O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8')
if shots:
 c=Image.new('RGB',(1280,((len(shots)+3)//4)*222),(6,12,22));d=ImageDraw.Draw(c)
 for i,(f,label)in enumerate(shots):c.paste(Image.open(f).convert('RGB').resize((320,200)),(i%4*320,i//4*222));d.text((i%4*320+4,i//4*222+202),label,fill='white')
 c.save(O/'contact.jpg')
print(json.dumps({'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks),'errors':errors}),flush=True)
raise SystemExit(0 if checks and all(q['passed']for q in checks)and not errors else 1)
