"""Real Edge rendering and native gameplay checks for the October20 redesign."""
from pathlib import Path
from PIL import Image
from io import BytesIO
import ast,base64,json,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_redesign_1020';O.mkdir(exist_ok=True);checks=[];errors=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
BOOT=r'''()=>{
 window.clean20=()=>{H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=special=null;P2M.active=null;stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;zoneCols=[];enemies=[];eBullets=[];pBullets=[];explosions=[];particles=[];floaters=[];smokeTrails=[];sprAnims=[];fadeOuts=[];pilotFx=[];powerups=[];D27_MODULE_DEBRIS.length=0;_smokeRings.length=0;groundTargetingReset();player.dead=player.out=false;player._dr21Death=null;player._spin=null;player.invuln=999;player.roll=player.somer=null;player.fireCd=999999;player.x=worldWidth()/2;player.y=viewTopY()+viewH()-72;run.shield=0;shake=whiteBlast=0;for(const k of Object.keys(Input.keys))delete Input.keys[k];Input.clearTaps();Input.mouse.down=false;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;};
 window.setup20=(form,diff='normal')=>{B=boss;v18Clear(B);GP4.clock+=1;diffKey=diff;DIFF=DIFFS[diff];v18Budget(B);j3State(B).ph21=null;j3State(B).hb20=null;j3State(B).gp4Donors=[];v18Enter(B,2,form);v18Fight(B);B._r30.v18.arenaPhase=2;B._r30.cd=999;B.enter=B._noHit=false;B.flash=0;B.x=worldWidth()/2;B.y=viewTopY()+viewH()*.35;B._r30.v18.home={x:B.x,y:B.y};B._drawY=B.y;dr5State(B).radio=null;clean20();B20.events=[];window.Q=form===2?ph21State(B):form===8?hb20State(B):null;window.K20={keys:new Set(),arrows:0,ordinaryBoxes:0};};
 const get=XART.get,draw=ctx.drawImage,tags=new WeakMap();XART.get=function(key){const im=get.apply(this,arguments);if(im)tags.set(im,key);return im;};ctx.drawImage=function(im){const key=tags.get(im);if(key&&K20)K20.keys.add(key);return draw.apply(this,arguments);};
 window.tick20=n=>{for(let i=0;i<n;i++){GP4.clock+=1/60;r30Tick(B,1/60);groundTargetingTick(1/60);}};
 window.paint20=()=>{shake=whiteBlast=0;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();};
 window.capturePart20=id=>{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);for(const v of v18Rig(B))if(v.p.id===id)v19Paint(v,B);ctx.restore();return Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);};
}'''
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500);p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}',polling=80);p.evaluate(BOOT)
  def setup(form=2,diff='normal'):p.evaluate('([f,d])=>setup20(f,d)',[form,diff])
  def tick(n):
   if p.evaluate('diffKey')=='normal':
    e=p.evaluate(shoot.STEP,n)
    if e:errors.append(e)
   else:p.evaluate('tick20',n)
  def frame():
   p.evaluate('paint20');return Image.open(BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGB')
  def film(name,frames):frames[0].save(O/(name+'.webp'),save_all=True,append_images=frames[1:],duration=100,loop=0,quality=86)
  setup();ck('Phoenix has independent whole anatomy plus both added pods',p.evaluate('B.parts.length===8&&v18Rig(B).length===9&&B.parts.every(p=>p.hp>0)'))
  for id in ['core','head','wingL','wingR','clawL','clawR','cannonL','cannonR']:
   setup();p.evaluate('()=>{Q.stage="swoon";}');tick(1)
   row=p.evaluate('''id=>{const part=B.parts.find(q=>q.id===id),before=capturePart20(id),hp=part.hp;B._lastPart=part;modularHit(1);const after=capturePart20(id);let changed=0;for(let i=0;i<after.length;i+=4)if(after[i]!==before[i]||after[i+1]!==before[i+1]||after[i+2]!==before[i+2])changed++;return{changed,loss:hp-part.hp,flash:part.flash,owner:B.flash};}''',id);ck(id+' damage visibly flashes its actual pixels',row['changed']>10 and row['loss']==1 and row['flash']>0,row)
   tick(15);ck(id+' flash expires',p.evaluate('id=>B.parts.find(q=>q.id===id).flash<=0',id))
   if id!='core':
    row=p.evaluate('''id=>{const part=B.parts.find(q=>q.id===id);B._lastPart=part;modularHit(part.hp+1);return{gone:part.destroyed&&!v18Rig(B).some(v=>v.p===part),body:B.hp>0};}''',id);ck(id+' breaks without fading or deleting another owner',row['gone'] and row['body'],row)
  for diff in ['easy','normal','hard','furious']:
   setup(2,diff);p.evaluate('()=>{for(const id of ["cannonL","cannonR"]){B._lastPart=ph21Part(B,id);modularHit(B._lastPart.hp+1);}}');ck(diff+' destroying pods switches to Swoon with torso remaining',p.evaluate('Q.stage==="swoon"&&B.hp>0&&ph21Alive(B,"core")'))
   corners=set()
   for i in range(90):
    tick(6);mode=p.evaluate('Q.action?.mode');
    if mode=='corner':corners.add(p.evaluate('Q.action.corner'))
    if diff=='normal' and i%2==0:
     im=frame();
     if i==0:phoenix=[]
     phoenix.append(im)
   row=p.evaluate('({finite:Number.isFinite(B.x+B.y+B.hp),mode:Q.action?.mode,scale:Q.scale})');ck(diff+' fast diagonal swoops remain finite and animated',row['finite'] and row['scale']>0,row)
   choices=p.evaluate('()=>{const a=new Set();for(let i=0;i<80;i++)a.add(ph21Corner(B).corner);return [...a];}');ck(diff+' random entry selects all four X corners',len(choices)==4,choices)
  film('phoenix-swoon',phoenix)
  setup();p.evaluate('()=>{Q.stage="swoon";B._lastPart=ph21Part(B,"wingL");modularHit(8);window.save20=JSON.stringify(B.parts.map(p=>[p.id,p.hp,p.destroyed]));v18Enter(B,2,0);v18Enter(B,2,2);}');ck('Phoenix module health persists through copying away and back',p.evaluate('save20===JSON.stringify(B.parts.map(p=>[p.id,p.hp,p.destroyed]))'))
  for diff in ['easy','normal','hard','furious']:
   for attack in ['cross','plus','orbit','atomicPass']:
    setup(1,diff);p.evaluate('type=>h21Start(B,type)',attack);duration=p.evaluate('h21Action(B).tell+h21Action(B).active');shots=p.evaluate('eBullets.length');images=[]
    for i in range(int(duration*10)+3):
     tick(6)
     if diff=='normal':images.append(frame())
    row=p.evaluate('({finite:Number.isFinite(B.x+B.y),done:!h21Action(B),shots:eBullets.length,events:B20.events.slice(-20)})');ck(diff+' helicopter '+attack+' finishes its native movement and attack',row['finite'] and row['done'],row if not row['done'] else None)
    if attack in ['cross','plus','orbit']:ck(diff+' '+attack+' fires actual projectiles',row['shots']>shots)
    if attack=='orbit':ck(diff+' second orbit reverses its direction',any(q['kind']=='heli-orbit-reverse' for q in row['events']))
    if attack=='atomicPass':
     drops=[q for q in row['events'] if q['kind']=='heli-atomic-drop'];ck(diff+' atomic missiles have giant radii and fixed warnings',len(drops)==(3 if diff in ['hard','furious'] else 2) and all(q['radius']>=220 and q['warn']>=2 for q in drops),drops)
     ck(diff+' giant atomic targets leave an opposite upper escape corner',p.evaluate('()=>{const x=camRightX()-20,y=viewTopY()+20;return Math.hypot(x-(camLeftX()+viewW()*.28),y-(viewTopY()+viewH()*.66))>Math.max(220,viewW()*.46);}'))
    if images:film('heli-'+attack,images)
  for diff in ['easy','normal','hard','furious']:
   for attack in ['skystrike','shield','side','throw','ball','charge','spin','dance','pickup','gun','break','punch','fists']:
    setup(8,diff);p.evaluate('type=>{if(["punch","fists"].includes(type)){Q.rage=true;Q.broken=true;}hb20Start(B,type);}',attack);duration=p.evaluate('Q.action.duration');images=[]
    for i in range(int(duration*10)+2):
     tick(6)
     if diff=='normal':images.append(frame())
    row=p.evaluate('({finite:Number.isFinite(B.x+B.y+B.hp),type:Q.action?.type,rage:Q.rage,keys:K20.keys.size})');ck(diff+' code Hammer '+attack+' completes with finite native state',row['finite'],row)
    if attack=='pickup':ck(diff+' Hammer pickup becomes a held chaingun',p.evaluate('Q.gunSeen&&Q.action?.type==="gun"'))
    if attack=='break':ck(diff+' knee break enters the warned luminaire phase',p.evaluate('Q.broken&&Q.action?.type==="luminaire"'))
    if images:film('hammer-'+attack,images)
   setup(8,diff);p.evaluate('()=>{hb20Start(B,"break");}');tick(620);ck(diff+' final weapon break leads to permanent hammerless fire',p.evaluate('Q.rage&&Q.broken&&Q.parts[1].destroyed&&!v18Rig(B).some(v=>v.p.id==="hammer")'))
   ck(diff+' subsequent attack book has only punches and fist slams',p.evaluate('()=>{for(let i=0;i<12;i++){const A=hb20Start(B);if(!["punch","fists"].includes(A.type))return false;hb20Finish(B,A);}return true;}'))
   setup(8,diff);p.evaluate('()=>{hb20Start(B,"shield");Q.action.t=Q.action.tell+.1;Q.shield=1;}');row=p.evaluate('()=>{const hp=B.hp;B._lastPart=B.parts[0];modularHit(100);return{absorbed:B.hp===hp,flash:B.flash,enemyShots:eBullets.length};}');ck(diff+' code shield absorbs and flashes without deflecting',row['absorbed'] and row['flash']>0 and row['enemyShots']==0,row)
   setup(8,diff);p.evaluate('()=>{Q.gunSeen=true;Q.broken=true;Q.safe=0;hb20Start(B,"luminaire");}');ck(diff+' luminaire reserves exactly one safe quarter',p.evaluate('()=>{let safe=0;for(let i=0;i<4;i++){const x=camLeftX()+(i%2+.5)*viewW()/2,y=viewTopY()+((i>>1)+.5)*viewH()/2;if(hb20Quadrant(x,y)===Q.action.safe)safe++;}return safe===1&&Q.action.tell>=1.9;}'))
  setup(8);p.evaluate('()=>{Q.rage=true;Q.broken=true;Q.parts[1].destroyed=true;j3Save(B);v18Enter(B,2,0);v18Enter(B,2,8);}');ck('Hammerless rage persists across a copied-form return',p.evaluate('Q.rage&&Q.parts[1].destroyed&&!v18Rig(B).some(v=>v.p.id==="hammer")'))
  # Stage5 source encounter uses ordinary native damage and its original book.
  p.evaluate(SETUP,dict(stage=5,kind='chromehammer',diff='normal',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&b20Ready(HB20_ART.banks);}',polling=80);p.evaluate('()=>{clean20();B=boss;B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=viewTopY()+180;B._hammer.ballSeen=B._hammer.whirlSeen=true;hammerState(B,"hammer");}');p.evaluate('()=>hammerPhaseTwoStart(B)');images=[]
  for i in range(40):p.evaluate(shoot.STEP,6);images.append(frame())
  film('stage5-pickup',images);ck('Stage5 source hammer strikes the special-style box and obtains chaingun',p.evaluate('B._hammer.hb20PickupDone&&B._hammer.mode==="chaingun"&&!B._hammer.hb20Pickup'))
  ck('Stage5 native chaingun uses new held weapon art',p.evaluate('K20.keys.has("hb20_blue_gun_0")||[...K20.keys].some(k=>k.startsWith("hb20_blue_gun_"))'))
  # Real browser keyboard events during native multi-lock acquisition and queue.
  p.evaluate(SETUP,dict(stage=1,pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1);}',polling=80);p.evaluate('()=>{clean20();boss=null;bossActive=false;run.bombs=30;run.lives=10;player.brCd=player.ssCd=0;player._tapL=player._tapR=player._tapU=-9;window.E20=spawnEnemy("delta",worldWidth()/2,viewTopY()+130,{});E20.hp=E20.maxhp=99999;E20.vy=0;}')
  # Warm the freshly entered stage's first bank/reticle draw before timing a
  # 260ms keyboard gesture. Browser-driver rendering latency is not a double tap.
  for warm in ['a','d','w','y']:
   p.keyboard.down(warm);p.evaluate(shoot.STEP,1);p.keyboard.up(warm);p.evaluate(shoot.STEP,1)
  for mode in ['acquiring','locked','queued']:
   for key,prop in [('a','roll'),('w','somer')]:
    p.evaluate('''mode=>{Input.keys={};player.roll=player.somer=null;player._rollCool=player._somerCool=0;player._tapL=player._tapR=player._tapU=-9;player._retinaScan=null;retinaScanAdd(E20);if(mode!=="acquiring"){retinaScanTick(.46);}if(mode==="queued"){retinaScanFire();player._retinaScan.queue.next=.5;}}''',mode)
    p.evaluate(shoot.STEP,2);p.keyboard.down('y');p.keyboard.down(key);p.evaluate(shoot.STEP,1);p.keyboard.up(key);p.evaluate(shoot.STEP,1);p.wait_for_timeout(20);p.keyboard.down(key);p.evaluate(shoot.STEP,1);p.keyboard.up(key)
    row=p.evaluate('prop=>({active:!!player[prop],scan:!!player._retinaScan,invuln:player.invuln})',prop);ck('Real keyboard '+prop+' works while Multi-Retina is '+mode,row['active'] and row['scan'],row);p.keyboard.up('y');p.evaluate(shoot.STEP,45)
  ck('No native browser, asset, draw or update errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors,results=checks);(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True);raise SystemExit(not all(q['passed'] for q in checks) or bool(errors))
