from pathlib import Path
import sys,json,math,time,subprocess
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=Path(r'C:/Users/Mike/Documents/Codex/2026-11-11/i-k/outputs/Three-way-hammer')/('verification-stage'+sys.argv[1]);O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot as original_boot
def boot(context,port,stage,errors,role='boss'):
 p=original_boot(context,port,stage,errors,role)
 p.wait_for_function('(s)=>{stageLoadTick();if(stageLoadReady(s))updatePlay(0);return stageLoadReady(s)&&!bp119Pending()}',arg=stage,timeout=180000)
 return p

from playwright.sync_api import sync_playwright
import imageio_ffmpeg
errors=[];checks=[];traces=[]
def ck(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS 'if value else'FAIL ')+name,str(data)[:220]if not value else'',flush=True)
 (O/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
def shot(p,name):
 p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(O/f'{name}.png'))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  p=boot(br.new_context(viewport={'width':1280,'height':800}),port,5,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return ba119Warm(5)}',polling=50,timeout=180000)
  p.evaluate("""()=>{window.B=boss;window.seed119=(diff,mat)=>{diffKey=diff;DIFF=difficultyForRun(run.mode,diff);BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=B,h=b._hammer;b.enter=b._noHit=b.dead=false;b.maxhp=11220;b.hp=b.maxhp;b.x=worldWidth()/2;b.y=viewTopY()+210;b._drawY=b.y;b.flash=0;h.balance0922=true;h.ballSeen=h.whirlSeen=h.hb20PickupDone=true;h.mode='hammer';h.phaseTwo=false;h.hammerDestroyed=false;h.c27RagePending=false;h._hf22Red=mat==='red';h._hf22Charge=null;h.frArmor={hp:mat==='regular'?0:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]};h.recovery=h.c25Knock=h.hb20Pickup=h.c26Return=h.c27Combo=h.throw=null;h.c30=null;h.phasePending=false;h._hj22Pair=h._hf22StormPair=null;eBullets=[];pBullets=[];enemies=[];l5Rocks=[];powerups=[];player.x=worldWidth()/2;player.y=VH-110;h.tx=player.x;h.ty=player.y-32;hammerState(b,'warn');BA119.events=[];HF22.events=[];};seed119('furious','regular');}""")
  p.wait_for_function("()=>{for(const n of ['blue-overhead','blue-sides','blue-right','blue-fold','blue-roll'])for(let f=0;f<16;f++)for(const m of ['regular','chrome','red']){const a=ba119Row(n,f,m);XART.rdy(a.key);XART.rdy(a.white);XART.rdy(a.redHit);}return ba119Warm(5)}",polling=50,timeout=180000)
  for diff in ['normal','hard','furious']:
   for mat in ['regular','chrome']:
    q=p.evaluate("""([diff,mat])=>{seed119(diff,mat);let root=null,maxDrift=0,seen=new Set(),poses=[],samples=[],behindFirst=0,behindSecond=0;for(let i=0;i<700;i++){updateBoss(1/60);const h=B._hammer,P=h._hj22Pair||h.c27Combo||h._hf22StormPair,q=ha21Blue(B);if(q?.a._ba119)seen.add(q.a.bank+':'+q.a.frame);if(q?.a.bank?.startsWith('blue-overhead')&&q.a.phase==='behind-head'){if(P?.ba119)behindSecond++;else behindFirst++;}if(P?.ba119){root??={x:B.x,y:B.y};maxDrift=Math.max(maxDrift,Math.hypot(B.x-root.x,B.y-root.y));samples.push({t:P.clock,x:B.x,y:B.y,bank:q?.a.bank,f:q?.a.frame,left:B.x+(q.a.bounds[0]-q.a.pivot[0])*(q.k||1)-camLeftX(),right:camRightX()-B.x-(q.a.bounds[2]-q.a.pivot[0])*(q.k||1)});}if(i%5===0)poses.push({i,state:h.state,t:h.t,x:B.x,y:B.y,bank:q?.a.bank,f:q?.a.frame});if(root&&!P)break;if(diff==='normal'&&h.state==='back')break;}return{diff,mat,root,maxDrift,samples,poses,unique:seen.size,behindFirst,behindSecond,events:BA119.events.slice(),first:HF22.events.filter(e=>e.type==='first-down')};}""",[diff,mat]);traces.append(q)
    expected=0 if diff=='normal'else 3 if diff=='furious'else 1
    ck(f'Stage5 {diff}/{mat}: correct planted follow-up count',len(q['events'])-sum(e['type']=='planted-combo-start'for e in q['events'])==expected,q['events'])
    ck(f'Stage5 {diff}/{mat}: fixed root after landing',q['maxDrift']<.01,q['maxDrift'])
    ck(f'Stage5 {diff}/{mat}: full planted combo remains inside playfield',all(z['left']>=0 and z['right']>=0 for z in q['samples']),q['samples'])
    ck(f'Stage5 {diff}/{mat}: new poses used',q['unique']>=24,q['unique'])
    ck(f'Stage5 {diff}/{mat}: actual behind-head windup on every down strike',q['behindFirst']>0 and (diff=='normal' or q['behindSecond']>0),dict(first=q['behindFirst'],second=q['behindSecond']))
  p.evaluate("seed119('furious','regular');hammerState(B,'recover');B._hammer._hj22Pair=hj22Pair(B,'blue',{x:player.x,y:player.y});B._hammer._hj22Pair.clock=.6;B._hammer.t=.6")
  shot(p,'stage5-overhead-windup')
  p.evaluate('B._hammer._hj22Pair.clock=1.02');shot(p,'stage5-contact-face')
  p.evaluate('B._hammer._hj22Pair.clock=1.76');shot(p,'stage5-left-sweep')
  p.evaluate('B._hammer._hj22Pair.clock=2.82');shot(p,'stage5-right-sweep')
  p.evaluate("hammerState(B,'curl');B._hammer.t=HAMMER_BALL_WARN*.5");shot(p,'stage5-fold')
  p.evaluate("hammerState(B,'ball');B._hammer.t=1;B._hammer.angle=.5");shot(p,'stage5-ball')
  p.evaluate("hammerState(B,'warn');B._hammer.t=.4;B.flash=0;B._hammer._hj22Pair=null;B._hammer.c27Combo=null;B._hammer._hf22StormPair=null");shot(p,'stage5-native-pose')
  p.evaluate('GP4.clock+=1;markHit(B,.16)');shot(p,'stage5-native-hit')
  ck('White hit flash changes native damaged pixels',(O/'stage5-native-pose.png').read_bytes()!=(O/'stage5-native-hit.png').read_bytes())
  p.evaluate('updateBoss(.2)')
  ck('Stage5 native white flash expires',p.evaluate('B.flash<=0'))


  activation=p.evaluate("""()=>{seed119('normal','regular');const hp=B.hp,armor=fr27BeginArmor(B);for(let i=0;i<1000&&B._hammer.state==='fr_activation';i++)fr27ActivationTick(B,1/60);const q=ha21Blue(B);return {activated:!!fr27Armor(B)?.activated,armorHP:fr27Armor(B)?.hp,state:B._hammer.state,bank:q?.a.bank,key:q?.a.key,hpSame:B.hp===hp,whole:q?.a.wholeGenerated};}""")
  ck('Native Chromium activation returns to new held-hammer form',activation['activated'] and activation['armorHP']>0 and activation['state']=='hammer' and activation['bank'].startswith('blue-overhead') and '_chrome_'in activation['key'] and activation['hpSame'] and activation['whole'],activation)
  shot(p,'stage5-chromium-native-ready')
  p.evaluate("hammerState(B,'recover');B._hammer.t=0;B._hammer._hj22Pair=null;B._hammer.c27Combo=null;B._hammer._hf22StormPair=null")
  shot(p,'stage5-chromium-front-contact')
  matrices=p.evaluate("""()=>{let out=[];for(const mat of ['regular','chrome','red']){seed119('normal',mat);for(const s of ['warn','leap','recover','giant_idle','giant_windup','giant_rise','giant_warn','giant_dive','giant_sweep','storm_warn','storm_slam','storm_split']){hammerState(B,s);B._hammer.t=s==='warn'?.5:s==='recover'?0:.2;const q=ha21Blue(B);out.push({mat,state:s,bank:q?.a.bank,key:q?.a.key,front:!!q?.a.faceForward,whole:!!q?.a.wholeGenerated});}}seed119('normal','regular');return out;}""")
  ck('Every normal/Chromium/red held strike and depth windup selects frontal art',all(q['bank'].startswith('blue-overhead')and q['front']and q['whole']and ('_'+q['mat']+'_')in q['key']for q in matrices),matrices)
  counts=p.evaluate("""()=>Object.fromEntries(Object.entries(BA119_ART).filter(([n])=>/^(blue|corrupt)-(overhead|sides|right|whirl)$/.test(n)).map(([n,a])=>[n,a.count]))""")
  ck('Real 32-frame overhead banks registered',counts['blue-overhead']==32 and counts['corrupt-overhead']==32,counts)
  spin=p.evaluate("""()=>{seed119('normal','regular');hammerWhirlStart(B);const h=B._hammer;let seen=new Set(),keys=new Set();for(let i=0;i<150;i++){updateBoss(1/60);const q=ha21Blue(B);if(q?.a.bank==='blue-whirl'){seen.add(q.a.frame);keys.add(q.a.key);}}return {frames:[...seen],keys:keys.size,whole:ha21Blue(B)?.a.wholeGenerated};}""")
  ck('Native whirlwind uses all 16 complete body turn drawings',len(spin['frames'])==16 and spin['keys']==16,spin)
  p.evaluate("seed119('normal','regular');hammerWhirlStart(B);hammerState(B,'whirlwind');B._hammer.c26SpinClock=B._hammer.ha1111SpinStart+4")
  shot(p,'stage5-native-whirl-back')
  from verify_three_way import run_three_way
  run_three_way(p,5,ck,shot)
  from front_record_loaded import record_loaded
  record_loaded(p,5,errors)
  ck('No browser or renderer exceptions',not errors,errors)
  br.close()
finally:stop()
(O/'trace.json').write_text(json.dumps(traces,indent=2));print(json.dumps({'checks':len(checks),'failed':[c['name']for c in checks if not c['passed']],'errors':errors}),flush=True)
