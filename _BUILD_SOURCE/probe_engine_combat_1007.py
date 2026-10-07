"""Native weapon pickups, pause clocks, fast ordnance/co-op, warnings and arena."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import sys,json,base64,ast
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/engine_combat_1007';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];screens=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
CLEAN='''()=>{ht27Stop();coopOn=false;run.mode='arcade';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');diffKey='normal';DIFF=DIFFS.normal;beginStage(7);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;s6Wing=null;boss=null;bossActive=false;subBoss=null;subBossActive=false;enemies=[];eBullets=[];pBullets=[];powerups=[];player.reset();player.invuln=0;player.y=440;player.x=worldWidth()/2;timeScale=1;stageTimer=10;spawnClock=-100;}'''
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':950});p.add_init_script('navigator.getGamepads=()=>[]')
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None);p.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  if p.evaluate('()=>typeof EC7==="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/engine_combat_1007.js')
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));screens.append(name)
  p.evaluate(CLEAN)
  p.evaluate('()=>{for(const a of Object.values(REPAIR30_ART))if(a.key.includes("chaingun"))XART.rdy(a.key);for(const P of PILOTS){XART.rdy("ship_"+P.key+"_pv2");XART.rdy("ship_"+P.key+"_br0");}l23FovWarm();pw5Warm();}')
  p.wait_for_function('()=>PILOTS.every(P=>XART.rdy("ship_"+P.key+"_pv2"))&&Object.values(REPAIR30_ART).filter(a=>a.key.includes("chaingun")).every(a=>XART.rdy(a.key))',timeout=120000)
  for pilot in p.evaluate('()=>PILOTS.map(p=>p.key)'):
   q=p.evaluate('''pilot=>{run.pilot=pilot;pilotIndex=PILOTS.findIndex(p=>p.key===pilot);player.reset();player.invuln=0;run.wlevels=WEAPONS.map(()=>1);run.weapon=7;let pass=true;for(const slot of [1,3,4,5,0]){applyPowerup({kind:'weapon',wtype:slot});pass=pass&&run.weapon===slot;applyPowerup({kind:'weapon',wtype:7});const n=EC7.mountDraws;chaingunMountsDraw(0);pass=pass&&run.weapon===7&&EC7.mountDraws-n===2;}const old=player._chainSpinT;chaingunMountsDraw(1);chaingunMountsDraw(1);return{pass,readonly:old===player._chainSpinT};}''',pilot)
   ck(q['pass'],pilot+' reacquires both authored mounts after five actual weapon pickup transitions');ck(q['readonly'],pilot+' paused/repeated draw cannot advance barrel clock');snap('mount-'+pilot)
  # Real controller movement ends roll/somersault and returns the pods.
  q=p.evaluate('''()=>{player.invuln=0;startRoll(1);const hidden=!chaingunMountsVisible();for(let i=0;i<32;i++)updatePlay(1/60);player.invuln=0;const n=EC7.mountDraws;chaingunMountsDraw();const rolled=EC7.mountDraws-n===2;startSomersault();for(let i=0;i<65;i++)updatePlay(1/60);player.invuln=0;const m=EC7.mountDraws;chaingunMountsDraw();player._spin={crashed:true};player.reset(true);player.invuln=0;return{hidden,rolled,somer:EC7.mountDraws-m===2,reset:player._spin===null&&chaingunMountsVisible()};}''')
  for k,v in q.items():ck(v,'chaingun '+k+' transition')
  p.evaluate(CLEAN)
  q=p.evaluate('''()=>{coopOn=true;p2Index=PILOTS.findIndex(p=>p.key==='yuri');run2.pilot='yuri';run2.weapon=7;run2.wlevel=2;run2.wlevels=WEAPONS.map(()=>1);player2.reset();player2.invuln=0;run.weapon=7;player._chainSpinT=1;player2._chainSpinT=5;withSeat(1,()=>chaingunHeatTick(.1,true));const one=player._chainSpinT;withSeat(2,()=>chaingunHeatTick(.1,false));return{separate:one===player._chainSpinT&&player2._chainSpinT>5&&player2._chainSpinT<5.1};}''');ck(q['separate'],'co-op barrel clocks are independent per physical ship')
  p.evaluate('()=>{run.stage=1;window.ecShot={kind:"gem",x:240,y:240,vx:0,vy:5,t:.31,_ph:1,szMul:2};XART.rdy(projStaticKey(FIRETYPES.gem.art(ecShot)));for(let i=0;i<6;i++)XART.rdy(FIRETYPES.comet.art({t:i/12,pal:"red"}));}')
  p.wait_for_function('()=>XART.rdy(projStaticKey(FIRETYPES.gem.art(ecShot)))&&Array.from({length:6},(_,i)=>XART.rdy(FIRETYPES.comet.art({t:i/12,pal:"red"}))).every(Boolean)',timeout=120000)
  one=p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);drawFireType(ecShot);return cv.toDataURL();}')
  p.wait_for_timeout(260)
  two=p.evaluate('()=>{ctx.clearRect(0,0,VW,VH);drawFireType(ecShot);return cv.toDataURL();}')
  ck(one==two,'native static projectile pixels freeze on simulation age while wall time passes')
  keys=p.evaluate('()=>{const out=[],old=drawMfx;drawMfx=function(key,...a){out.push(key);return old(key,...a);};for(let i=0;i<6;i++)drawFireType({kind:"comet",x:240,y:240,vx:0,vy:5,t:i/12,pal:"red"});drawMfx=old;return out;}')
  ck(len(set(keys))>=4,'authored comet flight reel retains multiple native frames')
  for fps in [30,60,120]:
   p.evaluate(CLEAN)
   q=p.evaluate('''fps=>{player.invuln=1e6;window.shot={x:100,y:120,vx:2,vy:1,w:7,h:8,kind:'s6tracer',t:0};eBullets=[shot];for(let i=0;i<fps/2;i++)updatePlay(1/fps);return{x:shot.x,y:shot.y,t:shot.t};}''',fps)
   ck(abs(q['x']-160)<.001 and abs(q['y']-150)<.001 and abs(q['t']-.5)<.001,str(fps)+' FPS enemy tracer travels the same distance/age')
  p.evaluate(CLEAN)
  q=p.evaluate('''()=>{coopOn=true;player.x=150;player.y=380;player.invuln=0;run.shield=3;run._megaShield=false;p2Index=3;run2.pilot=PILOTS[3].key;run2.weapon=7;run2.wlevel=1;run2.wlevels=WEAPONS.map(()=>1);run2.shield=3;run2._megaShield=false;player2.reset();player2.x=330;player2.y=380;player2.invuln=0;eBullets=[{x:330,y:300,vx:0,vy:160,w:7,h:8,kind:'s6tracer',t:0}];updatePlay(1/60);return{p1:run.shield,p2:run2.shield,dead1:player.dead,dead2:player2.dead,n:eBullets.length};}''')
  ck(q['p1']==3 and q['p2']==2 and not q['dead1'] and not q['dead2'] and q['n']==0,'fast hostile round crosses P2 in one step: only P2 shield takes a hit')
  p.evaluate(CLEAN)
  q=p.evaluate('''()=>{const t={type:'fighter',x:240,y:300,w:24,h:24,hp:100,maxhp:100,vy:0,vx:0,t:0,dead:false,fireCd:999};enemies=[t];pBullets=[{x:240,y:350,vx:0,vy:-120,w:6,h:10,kind:'mg',dmg:3,lv:1,t:0}];player.invuln=1e6;updatePlay(1/60);return{hp:t.hp,shots:pBullets.length};}''')
  ck(q['hp']<100 and q['shots']==0,'fast player tracer hits a thin fighter crossed between frames')
  # Warning projection and dead/emitter cleanup use real collector.
  p.evaluate(CLEAN)
  q=p.evaluate('''()=>{run.stage=4;player.x=300;player.y=420;player._vx=player._vy=0;eBullets=Array.from({length:7},(_,i)=>({x:300,y:200+i*8,vx:0,vy:5,w:7,h:12,t:0}));eBullets.push({x:390,y:300,vx:0,vy:5,w:7,h:12});pw5Collect();const n=PW5.threats.length,first=PW5.threats[0]?.p;first.dead=true;pw5Collect();return{n,clean:PW5.threats.every(q=>!q.p.dead),safe:pw5Impact({x:390,y:300,vx:0,vy:5,w:7,h:12},player)===null,recede:pw5Impact({x:300,y:300,vx:0,vy:-5,w:7,h:12},player)===null};}''')
  ck(q['n']==2 and q['clean'] and q['safe'] and q['recede'],'all-stage warning budget prioritizes two true approaches, removes dead rounds and ignores safe lanes');snap('incoming-warning')
  p.evaluate('()=>{run.stage=6;window.warnOwner={x:worldWidth()/2,y:190,w:90,h:90,t:.93};drawWorld(0);window.warnChecks=[];for(const k of [.1,.55,.95]){EC7.alerts=new WeakSet();warnChecks.push(l23WarnSymbolDraw(warnOwner,{t:k,warm:1})&&!l23WarnSymbolDraw(warnOwner,{t:k,warm:1}));}}')
  ck(p.evaluate('()=>warnChecks.every(Boolean)'),'Stage 6 original warning symbols persist in every phase and deduplicate owner')
  p.evaluate('()=>{const base=drawWorld;drawWorld=function(dt){const r=base(dt);ctx.save();const z=viewZoom();ctx.scale(z,z);ctx.translate(-camX,VH*(1-z)/z);combatWarningDraw(warnOwner,{x:warnOwner.x,y:160,ex:warnOwner.x,ey:VH,width:24,progress:.8,laneShape:"line"});ctx.restore();return r;};}');snap('committed-lane');p.evaluate('()=>drawWorld=EC7_BASE.world')
  # Arena render captures three camera positions with one simulation instant.
  SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'normal'})
  p.evaluate('()=>{j3Encounter(B,2);on5FightStart(B);dr5State(B).introWanted=false;dr5State(B).introSeen=true;story=null;fb2Talk=null;BOFCinematicDirector.cancel();aa5Warm();}')
  p.wait_for_function('()=>Object.values(AA5_ART).every(c=>c.every(a=>XART.rdy(a.key)))',timeout=120000)
  q=p.evaluate('''()=>{const out=[],base=aa5Cell;aa5Cell=function(name,f,x,y,w,h,...rest){if(name==='back'||name==='front')out.push({name,x,y,w,h});return base(name,f,x,y,w,h,...rest);};for(const cam of [0,(worldWidth()-viewW())/2,worldWidth()-viewW()]){camX=cam;aa5ArenaDraw(B);}aa5Cell=base;return out;}''')
  ck(all(q[i]==q[i%2] for i in range(len(q))),'final arena back and architectural ribs keep identical world anchors at left/center/right cameras')
  for label,v in [('left',0),('center',.5),('right',1)]:p.evaluate('f=>{camX=(worldWidth()-viewW())*f;player.x=camX+viewW()/2;}',v);snap('arena-'+label)
  p.wait_for_timeout(500);ck(not errors,'zero native page/console/missing asset errors');br.close()
finally:stop()
(O/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors,'screens':screens,'scope':'Native controlled probes; no campaign-clear or human balance claim.'},indent=2),encoding='utf-8')
imgs=[Image.open(O/('mount-'+x+'.png')).convert('RGB').resize((240,256)) for x in ['axel','decker','maverick','freezer','juggernaut','lizzie','yuri','falva','cole']]
contact=Image.new('RGB',(720,768));
for i,im in enumerate(imgs):contact.paste(im,((i%3)*240,(i//3)*256))
contact.save(O/'mount-contact.jpg',quality=90)
print(json.dumps({'checks':len(checks),'failed':[q['name'] for q in checks if not q['ok']],'errors':errors}))
if errors or any(not c['ok'] for c in checks):raise SystemExit(1)
