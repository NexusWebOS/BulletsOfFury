"""Native Stage5 actor-bank restoration, recovery/shield and hit feedback."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/hammer_acting_1021/native';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&window.BOF_HAMMER_ACTING');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('''()=>{window.hrKeys=[];const d=ctx.drawImage;ctx.drawImage=function(im){const key=HA21.tags.get(im)||HB20.tags.get(im)||PXG.tags.get(im)?.key;if(key)hrKeys.push(key);return d.apply(this,arguments);};
   window.hrDraw=(native=false)=>{BAL7.seed(1021);hrKeys=[];ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width/SS,cv.height/SS);ctx.translate(-camX,0);(native?HB20.base.draw:hammerBossDraw)(B);return [...new Set(hrKeys)];};
   window.hrPixels=()=>Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);window.hrChanged=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
   window.hrWhite=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]<650&&b[i]>240&&b[i+1]>240&&b[i+2]>240)n++;return n;};}''')
  def setup(diff):
   p.evaluate('diff=>BAL7.setup({stage:5,kind:"chromehammer",pilot:"cole",diff,fire:false,seconds:60})',diff)
   p.wait_for_function('()=>{stageLoadTick();hm10Warm();return stageLoadInfo(5).ready&&hc11Ready()&&hf19Ready()&&hm10Ready()&&ha21Ready();}')
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;AP10_X.intro=null;P2M.active=null;
    B._cin30Spoke=B._fb2IntroSeen=true;B.enter=B.dead=B._noHit=false;B.hp=B.maxhp=6000;B.flash=0;
    const h=B._hammer;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;h.mode='storm';h.phasePending=false;h.frRecovery=false;h.recovery=null;h.openingJump1003=false;
    h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};
    if(B._hammerTime)B._hammerTime.mode='attack';if(B._hama)B._hama.mode='attack';B.x=worldWidth()/2;B.y=200;h.stormHome={x:B.x,y:B.y};camX=B.x-viewW()/2;
    player.dead=player.out=false;player.invuln=40002;player.x=B.x;player.y=VH-70;run.shield=0;shake=whiteBlast=0;
    enemies=[];eBullets=[];pBullets=[];powerups=[];l5Rocks=[];l5RockT=9999;stagePlan=[];spawnClock=9999;hammerStormTarget(B);hammerStormImpact(B);h.leapFx=0;}''')
  states={'hammer':'blue_idle','warn':'blue_jump','leap':'blue_jump','spin':'blue_throw','whirlwind':'blue_spin','storm_raise':'blue_hold','spell':'blue_cast','mega_charge':'blue_beam_empty','enrage':'blue_rage','fr_activation':'blue_chromium','curl':'blue_to_ball','unfold':'blue_from_ship'}
  if '--partial' in sys.argv:states={k:v for k,v in states.items() if v in p.evaluate('Object.keys(HA21_ART.banks)')}
  for diff in ['normal','hard','furious']:
   setup(diff)
   for state,bank in states.items():
    p.evaluate("""state=>{const h=B._hammer;h.spellTargets=[];h.pillars=[];h.state=state;h.t=.7;h.throw=null;h.hammerDestroyed=state==='mega_charge';h.mode=state==='mega_charge'?'chaingun':'hammer';h.hc11Counter=null;h.bm9Counter=null;h.recovery=null;h.hb20Pickup=null;h.empowered=false;h.charged=true;B.flash=0;h.frArmor.activated=false;h.frArmor.barrier=0;h.angle=.6;}""",state)
    row=p.evaluate("""()=>{const q=ha21Blue(B),keys=hrDraw();return{kind:q?.kind,keys,suppressed:HA21.suppressed};}""")
    ck(diff+' '+state+' draws exactly one new whole actor without retired body blits',row['kind']==bank and sum(k.startswith('ha21_'+bank+'_') for k in row['keys'])==1 and not any(HA in k for k in row['keys'] for HA in ['arch_orbital_sweep','arch_storm_charge','arch_ship_transform','arch_whirlwind','arch_arsenal_cast']),row)
    if diff=='normal':
     p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
     p.screenshot(path=str(O/(state+'-scene.png')))
    row=p.evaluate("""()=>{B._gp4FlashNext=0;hrDraw();const plain=hrPixels();markHit(B,.12);hrDraw();const hit=hrPixels();const timer=B.flash;B.flash=0;hrDraw();const off=hrPixels();return{white:hrWhite(plain,hit),expiry:hrWhite(plain,off),timer};}""")
    ck(diff+' '+state+' retains visible hit flash and authored palette after expiry',row['white']>20 and row['expiry']<row['white']*.02+2 and row['timer']>0,row)
   # Native stun/death acting remains separate from attack poses.
   p.evaluate("()=>{B._hammer.state='hammer_stun';B._hammer.t=2;B.flash=0;}")
   row=p.evaluate("()=>({pick:ha21Blue(B),old:hf19Pick(B)?.kind,keys:hrDraw()})")
   ck(diff+' stun retains original kneeling recovery acting',row['pick'] is None and row['old']=='recovery',row)
   p.evaluate("()=>{B._hammer.state='storm_idle';B._hammer.hc11Counter=null;B._hammer.frArmor.activated=false;B._hammer.hammerDestroyed=false;player.y=hc11MidY()-60;}")
   row=p.evaluate("""()=>{const C=hc11BeginCounter(B,{x:player.x,y:player.y,seat:1}),keys=new Set();let error=0;for(let i=0;i<160&&B._hammer.hc11Counter;i++){hc11CounterTick(B,C,1/60);for(const k of hrDraw())keys.add(k);if(C.impact){const tip=hc11Tip(C,11,C.land.x,C.land.y,C.land.scale,C.land.angle);error=Math.hypot(tip.x-C.anchor.x,tip.y-C.anchor.y);}}return{done:!B._hammer.hc11Counter,keys:[...keys],error,finite:Number.isFinite(B.x+B.y)};}""")
   ck(diff+' real committed counter finishes with new measured side swing and aligned hammer contact',row['done'] and row['finite'] and row['error']<1 and any(k.startswith('ha21_blue_counter') for k in row['keys']),row)
  for diff in ['normal','hard','furious']:
   setup(diff)
   for attack in ['leap','storm_slam','giant_dive']:
    row=p.evaluate("""type=>{const h=B._hammer;h.frArmor=null;h.hc11Counter=h.bm9Counter=h.recovery=null;h.hb20Pickup=null;h.mode='hammer';h.hammerDestroyed=false;B.flash=0;B.x=worldWidth()/2;B.y=190;hammerTarget(B);let target;
     if(type==='giant_dive'){hammerGiantArm(B);target={x:h.tx,y:h.ty};}else if(type==='storm_slam'){hammerStormTarget(B);target={...h.stormTarget};}else target={x:h.tx,y:h.ty+32};
     hammerState(B,type);for(let i=0;i<120&&h.state===type;i++){if(type==='leap')hammerBossTick(B,1/60);else{h.t+=1/60;if(type==='storm_slam')hammerStormTick(B,1/60);else hammerCombatTick(B,1/60);}}
     const tip=hammerHeadPoint(B);hrDraw();return{state:h.state,error:Math.hypot(tip.x-target.x,tip.y-target.y),tip,target,finite:Number.isFinite(B.x+B.y)};}""",attack)
    ck(diff+' '+attack+' native impact coincides with the new visible hammer head',row['finite'] and row['state']!=attack and row['error']<1,row)
  setup('furious')
  row=p.evaluate("""()=>{const h=B._hammer;h.hc11Counter=null;h.hb20PickupDone=false;h.hb20Pickup=null;B.x=worldWidth()/2;B.y=200;hammerPhaseTwoStart(B);const C=h.hb20Pickup;let contact=null,keys=new Set();for(let i=0;i<200&&h.hb20Pickup;i++){const before=C.hit;hammerBossTick(B,1/60);if(!before&&C.hit){const at=hammerHeadPoint(B);contact=Math.hypot(at.x-C.box.x,at.y-C.box.y);}for(const k of hrDraw())keys.add(k);}return{done:h.hb20PickupDone,hit:C.hit,obtained:C.obtained,contact,keys:[...keys]};}""")
  ck('Native crate strike uses the new overhead reel with exact hammer-to-crate contact and chaingun handoff',row['done'] and row['hit'] and row['obtained'] and row['contact'] is not None and row['contact']<1 and any(k.startswith('ha21_blue_slam') for k in row['keys']),row)
  p.wait_for_function('()=>ha21Ready(0)')
  row=p.evaluate("""()=>{const h=B._hammer;h.hb20Pickup=null;h.recovery=null;h.hc11Counter=null;h.mode='hammer';h.hammerDestroyed=false;B._gp4FlashNext=0;hammerState(B,'hammer');hrDraw();const plain=hrPixels(),baseline=plain.filter((v,i,a)=>i%4===0&&v>240&&a[i+1]>240&&a[i+2]>240).length;markHit(B,.12);hrDraw();const white=hrPixels().filter((v,i,a)=>i%4===0&&v>240&&a[i+1]>240&&a[i+2]>240).length;return{timer:B.flash,white,baseline};}""")
  p.evaluate(shoot.STEP,18)
  after=p.evaluate("""()=>{hrDraw();const a=hrPixels();return{timer:B.flash,white:a.filter((v,i)=>i%4===0&&v>240&&a[i+1]>240&&a[i+2]>240).length};}""")
  ck('Actual native game frames expire the hit flash and restore authored body pixels',row['timer']>0 and after['timer']==0 and row['white']>row['baseline']+100 and after['white']<row['baseline']+max(50,(row['white']-row['baseline'])*.1),dict(before=row,after=after))
  # Actual source-cell playback through the live context, no image.src comparisons.
  row=p.evaluate("""()=>{let cells=0,visible=0;for(const rows of Object.values(HA21_ART.banks))for(const a of rows){const im=XART.get(a.key);ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(im,0,0);const data=ctx.getImageData(0,0,a.w,a.h).data;let n=0;for(let i=0;i<data.length;i+=4)if(data[i]+data[i+1]+data[i+2]>20)n++;cells++;if(n>100)visible++;}return{cells,visible};}""")
  ck('Every new source cell really draws nonempty authored pixels in Chromium',row['cells']==row['visible'] and row['cells']>80,row)
  if '--partial' not in sys.argv:
   p.evaluate('()=>BAL7.setup({stage:8,kind:"vileexistence",pilot:"cole",diff:"furious",fire:false,seconds:60})')
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}')
   p.evaluate("""()=>{B=boss;v18Budget(B);v18Enter(B,2,8);v18Fight(B);B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=PLAY.y+190;B._drawY=B.y;hb20Init(B);}""")
   for action,bank in {'skystrike':'corrupt_jump','side':'corrupt_side','throw':'corrupt_throw','ball':'corrupt_to_ball','charge':'corrupt_hold','shield':'corrupt_chromium','spin':'corrupt_spin','luminaire':'corrupt_beam_empty','fire':'corrupt_rage_empty','break':'corrupt_stun'}.items():
    row=p.evaluate("""([type,bank])=>{const Q=hb20State(B);Q.action=null;Q.broken=type==='luminaire';Q.safe=0;Q.rage=false;hb20Start(B,type);const A=Q.action;A.t=A.tell*.75;if(type==='fire')A.t=.8;if(type==='break')A.t=2;B.flash=0;const pose=hb20Pose(B);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return{kind:pose.kind,key:pose.a.key,owns:hb20Own(B)};}""",[action,bank])
    ck('Corrupted '+action+' uses its own generated whole actor',row['kind']==bank and row['owns'],row)
    p.screenshot(path=str(O/('corrupt-'+action+'.png')))
   for diff in ['normal','hard','furious']:
    row=p.evaluate("""diff=>{diffKey=diff;DIFF=difficultyForRun(run.mode,diff);const Q=hb20State(B);Q.action=null;Q.broken=Q.rage=false;Q.cool=0;Q.scale=1;B.x=worldWidth()/2;B.y=PLAY.y+190;hb20Start(B,'skystrike');const A=Q.action;let contact=null;for(let i=0;i<250&&Q.action===A;i++){const before=A.impact;v19NativeTick(B,1/60);if(!before&&A.impact){const p=hb20Pose(B),tip=hb20World(p.a,p.a.tip,B,p.k,p.rot);contact=Math.hypot(tip.x-A.target.x,tip.y-A.target.y);}}return{done:Q.action!==A,contact,finite:Number.isFinite(B.x+B.y)};}""",diff)
    ck(diff+' native corrupted jump completes with its real visible hammer at the warned impact',row['done'] and row['finite'] and row['contact'] is not None and row['contact']<6,row)
   row=p.evaluate("""()=>{const Q=hb20State(B);Q.action=null;Q.scale=1;hb20Start(B,'pickup');const A=Q.action,C=A.crate;let contact=null;for(let i=0;i<190&&Q.action===A;i++){const before=C.hit;v19NativeTick(B,1/60);if(!before&&C.hit){const p=hb20Pose(B),tip=hb20World(p.a,p.a.tip,B,p.k,p.rot);contact=Math.hypot(tip.x-C.box.x,tip.y-C.box.y);}}return{done:Q.action!==A,contact,hit:C.hit,obtained:C.obtained};}""")
   ck('Corrupted native crate strike aligns the new overhead pose and completes its pickup',row['done'] and row['hit'] and row['obtained'] and row['contact'] is not None and row['contact']<1,row)
  ck('No page console draw or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed');sys.exit(bool(report['failed']))
