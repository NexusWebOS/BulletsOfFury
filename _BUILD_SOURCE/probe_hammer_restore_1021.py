"""Native Stage5 actor-bank restoration, recovery/shield and hit feedback."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/hammer_restore_1021';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('''()=>{window.hrKeys=[];const d=ctx.drawImage;ctx.drawImage=function(im){const key=HB20.tags.get(im)||PXG.tags.get(im)?.key;if(key)hrKeys.push(key);return d.apply(this,arguments);};
   window.hrDraw=(native=false)=>{BAL7.seed(1021);hrKeys=[];ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width/SS,cv.height/SS);ctx.translate(-camX,0);(native?HB20.base.draw:hammerBossDraw)(B);return [...new Set(hrKeys)];};
   window.hrPixels=()=>Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);window.hrChanged=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
   window.hrWhite=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]<650&&b[i]>240&&b[i+1]>240&&b[i+2]>240)n++;return n;};}''')
  def setup(diff):
   p.evaluate('diff=>BAL7.setup({stage:5,kind:"chromehammer",pilot:"cole",diff,fire:false,seconds:60})',diff)
   p.wait_for_function('()=>{stageLoadTick();hm10Warm();return stageLoadInfo(5).ready&&hc11Ready()&&hf19Ready()&&hm10Ready();}')
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;AP10_X.intro=null;P2M.active=null;
    B._cin30Spoke=B._fb2IntroSeen=true;B.enter=B.dead=B._noHit=false;B.hp=B.maxhp=6000;B.flash=0;
    const h=B._hammer;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;h.mode='storm';h.phasePending=false;h.frRecovery=false;h.recovery=null;h.openingJump1003=false;
    h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};
    if(B._hammerTime)B._hammerTime.mode='attack';if(B._hama)B._hama.mode='attack';B.x=worldWidth()/2;B.y=200;h.stormHome={x:B.x,y:B.y};camX=B.x-viewW()/2;
    player.dead=player.out=false;player.invuln=40002;player.x=B.x;player.y=VH-70;run.shield=0;shake=whiteBlast=0;
    enemies=[];eBullets=[];pBullets=[];powerups=[];l5Rocks=[];l5RockT=9999;stagePlan=[];spawnClock=9999;hammerStormTarget(B);hammerStormImpact(B);h.leapFx=0;}''')
  states=['hammer','warn','leap','spin','whirlwind','storm_raise','chaingun','shield','fr_activation','recover','hammer_stun','storm_stun','fr_stun']
  for diff in (['normal'] if '--compare' in sys.argv else ['normal','hard','furious']):
   setup(diff)
   for state in states:
    p.evaluate('''state=>{const h=B._hammer;h.state=state;h.t=.7;h.throw=null;h.hammerDestroyed=false;h.hc11Counter=null;h.bm9Counter=null;h.recovery=null;h.chainDestroyed=false;h.chainMuzzle=.09;h.chainHeat=.6;h.empowered=true;h.empowerLevel=1;h.charged=true;B.flash=0;h.frArmor.barrier=['shield','fr_activation'].includes(state)?2:0;}''',state)
    keys=p.evaluate('hrDraw()')
    if '--compare' in sys.argv:
     p.screenshot(path=str(O/(state+'-before.png')));p.evaluate('hrDraw(true)');p.screenshot(path=str(O/(state+'-native.png')));print(state,json.dumps(keys),flush=True);continue
    ck(diff+' '+state+' uses older authored actor without blue redesign overlay',bool(keys) and not any(k.startswith('hb20_blue') or k.startswith('hb20_counter') for k in keys),keys)
    if diff=='normal':
     p.screenshot(path=str(O/(state+'-restored.png')))
     if state in ['hammer','shield','hammer_stun','chaingun']:
      p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}')
      p.screenshot(path=str(O/(state+'-scene.png')))
    # Warm the actual lazy tint/companion canvases before comparing stable pixels.
    row=p.evaluate('''()=>{B._gp4FlashNext=0;markHit(B,.12);hrDraw();B.flash=0;hrDraw();B._gp4FlashNext=0;
     hrDraw();const a=hrPixels();hrDraw();const plain=hrPixels(),drift=hrChanged(a,plain);markHit(B,.12);hrDraw();const b=hrPixels();B.flash=0;hrDraw();const c=hrPixels();return{pixels:hrChanged(a,b),white:hrWhite(a,b),whiteExpiry:hrWhite(a,c),whiteDrift:hrWhite(a,plain),drift,expiry:hrChanged(a,c),pick:hf19Pick(B)?.kind};}''')
    # The animated emissive core can cross white on a few pixels. Require the
    # silhouette flash to lose at least99.9% of its added white after expiry.
    ck(diff+' '+state+' visibly flashes damaged pixels and returns to palette',row['pixels']>row['drift']+20 and row['white']>20 and row['whiteExpiry']<=max(row['whiteDrift'],row['white']*.001),row)
    if state in ['shield','fr_activation']:ck(diff+' '+state+' retains dedicated shield bank',row['pick']=='shield',row)
    if state in ['recover','hammer_stun','storm_stun','fr_stun']:ck(diff+' '+state+' retains knocked-down/get-up bank',row['pick']=='recovery',row)
   row=p.evaluate('''()=>{const out={};for(const s of ['hammer_stun','storm_stun','fr_stun']){const d=s==='hammer_stun'?5:4;B._hammer.state=s;out[s]=[0,.5,.95].map(u=>{B._hammer.t=u*d;hrDraw();return hf19Pick(B).nativeStun;});}return out;}''')
   ck(diff+' original hit/kneel/get-up poses span the complete stun state',all(v==[0,1,2] for v in row.values()),row)
   row=p.evaluate('''()=>{const h=B._hammer;h.hc11Counter=null;h.state='storm_idle';h.hammerDestroyed=false;h.throw=null;h.t=0;h.frArmor.barrier=0;
    const C=hc11BeginCounter(B,{x:player.x,y:hc11MidY()-60,seat:1}),keys=new Set();for(let i=0;i<160&&h.hc11Counter;i++){hc11CounterTick(B,C,1/60);for(const k of hrDraw())keys.add(k);}
    return{done:!h.hc11Counter,finite:Number.isFinite(B.x+B.y),bank:HM10_ART[C.bank].map(a=>a.key),keys:[...keys]};}''')
   ck(diff+' native jump counter finishes using the original sixteen-pose swing bank',row['done'] and row['finite'] and len(row['bank'])==16 and all(k.startswith('hm10_swing_') for k in row['bank']) and any(k.startswith('hm10_swing_') for k in row['keys']),row)
   if diff=='normal':
    p.evaluate('''()=>{const C=hc11BeginCounter(B,{x:player.x,y:hc11MidY()-60,seat:1});C.t=C.tell+.07;Object.assign(C,hc11Pose(C));B.x=C.x;B.y=C.y;hrDraw();}''')
    p.screenshot(path=str(O/'counter-strike.png'))
   row=p.evaluate('''()=>{const h=B._hammer;h.hc11Counter=null;h.hb20PickupDone=false;h.hb20Pickup=null;B.x=worldWidth()/2;B.y=200;hammerPhaseTwoStart(B);const C=h.hb20Pickup;let contact=null,keys=new Set();
    for(let i=0;i<200&&h.hb20Pickup;i++){const hit=C.hit;hammerBossTick(B,1/60);if(!hit&&C.hit){const p=hammerHeadPoint(B);contact=Math.hypot(p.x-C.box.x,p.y-C.box.y);}for(const k of hrDraw())keys.add(k);}
    return{done:h.hb20PickupDone&&!h.hb20Pickup,hit:C.hit,obtained:C.obtained,contact,keys:[...keys],state:h.state};}''')
   ck(diff+' phase-two crate uses original strike, aligned contact and native chaingun handoff',row['done'] and row['hit'] and row['obtained'] and row['contact'] is not None and row['contact']<1 and not any(k.startswith('hb20_blue') for k in row['keys']),row)
  # Dracodia's separate Hammer form still owns its current corrupt banks.
  p.evaluate('()=>BAL7.setup({stage:8,kind:"vileexistence",pilot:"cole",diff:"normal",fire:false,seconds:60})')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}')
  row=p.evaluate('''()=>{B=boss;v18Budget(B);v18Enter(B,2,8);v18Fight(B);B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=PLAY.y+190;B._drawY=B.y;
   hb20Start(B,'skystrike');return{owns:hb20Own(B),keys:v19HammerRig(B).map(v=>v.key),action:hb20State(B)?.action?.type};}''')
  ck('Stage8 keeps its independent corrupted Hammer rig and attack owner',row['owns'] and row['action']=='skystrike' and any(k.startswith(('hb20_corrupt','fv21_hammer')) for k in row['keys']),row)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors)
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/('comparison.json' if '--compare' in sys.argv else 'report.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['passed','failed','errors']}),flush=True);sys.exit(bool(report['failed']))
