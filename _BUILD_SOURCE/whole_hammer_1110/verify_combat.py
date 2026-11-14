from pathlib import Path
import sys,json,math,time,subprocess
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent;O=R/'_shots/whole_hammer_1110';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
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
    q=p.evaluate("""([diff,mat])=>{seed119(diff,mat);let root=null,maxDrift=0,seen=new Set(),poses=[],samples=[];for(let i=0;i<700;i++){updateBoss(1/60);const h=B._hammer,P=h._hj22Pair||h.c27Combo||h._hf22StormPair,q=ha21Blue(B);if(q?.a._ba119)seen.add(q.a.bank+':'+q.a.frame);if(P?.ba119){root??={x:B.x,y:B.y};maxDrift=Math.max(maxDrift,Math.hypot(B.x-root.x,B.y-root.y));samples.push({t:P.clock,x:B.x,y:B.y,bank:q?.a.bank,f:q?.a.frame});}if(i%5===0)poses.push({i,state:h.state,t:h.t,x:B.x,y:B.y,bank:q?.a.bank,f:q?.a.frame});if(root&&!P)break;if(diff==='normal'&&h.state==='back')break;}return{diff,mat,root,maxDrift,samples,poses,unique:seen.size,events:BA119.events.slice(),first:HF22.events.filter(e=>e.type==='first-down')};}""",[diff,mat]);traces.append(q)
    expected=0 if diff=='normal'else 3 if diff=='furious'else 1
    ck(f'Stage5 {diff}/{mat}: correct planted follow-up count',len(q['events'])-sum(e['type']=='planted-combo-start'for e in q['events'])==expected,q['events'])
    ck(f'Stage5 {diff}/{mat}: fixed root after landing',q['maxDrift']<.01,q['maxDrift'])
    ck(f'Stage5 {diff}/{mat}: new poses used',q['unique']>=12,q['unique'])
  p.evaluate("seed119('furious','regular');hammerState(B,'recover');B._hammer._hj22Pair=hj22Pair(B,'blue',{x:player.x,y:player.y});B._hammer._hj22Pair.clock=.6;B._hammer.t=.6")
  shot(p,'stage5-overhead-windup')
  p.evaluate('B._hammer._hj22Pair.clock=1.02');shot(p,'stage5-contact-face')
  p.evaluate('B._hammer._hj22Pair.clock=1.76');shot(p,'stage5-left-sweep')
  p.evaluate('B._hammer._hj22Pair.clock=2.82');shot(p,'stage5-right-sweep')
  p.evaluate("hammerState(B,'curl');B._hammer.t=HAMMER_BALL_WARN*.5");shot(p,'stage5-fold')
  p.evaluate("hammerState(B,'ball');B._hammer.t=1;B._hammer.angle=.5");shot(p,'stage5-ball')
  p.evaluate("hammerState(B,'warn');B._hammer.t=.4;B.flash=0");shot(p,'stage5-native-pose')
  p.evaluate('GP4.clock+=1;markHit(B,.16)');shot(p,'stage5-native-hit')
  ck('White hit flash changes native damaged pixels',(O/'stage5-native-pose.png').read_bytes()!=(O/'stage5-native-hit.png').read_bytes())
  p.close()
  p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return ba119Warm(8)}',polling=50,timeout=180000)
  p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=false;B._noHit=false;BOFCinematicDirector.cancel();window.Q=hb20State(B);}")
  for diff in ['normal','hard','furious']:
   for mat in ['regular','chrome','red']:
    q=p.evaluate("""([d,m])=>{diffKey=d;DIFF=difficultyForRun(run.mode,d);B._r30.mode='fight';B._r30.v18.donorAge=0;Q.rf1110=null;Q.chrome=m!=='regular';Q.rage=m==='red';B.x=worldWidth()/2;B.y=viewTopY()+180;Q.action=null;Q.cool=999;BA119.events=[];hb20Start(B,'skystrike');const A=Q.action;let root=null,drift=0,poses=new Set();for(let i=0;i<600&&Q.action===A;i++){v19NativeTick(B,1/60);if(Q.action===A){const q=hb20Pose(B);poses.add(q.a.bank+':'+q.a.frame);if(A.t-A.tell>=.55){root??={x:B.x,y:B.y};drift=Math.max(drift,Math.hypot(B.x-root.x,B.y-root.y));}}}return{diff:d,mat:m,drift,unique:poses.size,events:BA119.events.slice()};}""",[diff,mat]);traces.append(q)
    ck(f'Stage8 {diff}/{mat}: correct one/double/four contacts',len(q['events'])==({'normal':1,'hard':2,'furious':4}[diff]),q['events'])
    ck(f'Stage8 {diff}/{mat}: no hops or torso chase after landing',q['drift']<.01,q['drift'])
  p.evaluate("()=>{Q.rage=Q.chrome=false;B.x=worldWidth()/2;B.y=viewTopY()+220;Q.action=null;hb20Start(B,'skystrike');Q.action.t=Q.action.tell+1.8;ba119Root(B,Q.action);}");shot(p,'stage8-overhead-windup')
  p.evaluate('Q.action.t=Q.action.tell+1.0');shot(p,'stage8-contact-face')
  p.evaluate('Q.action.t=Q.action.tell+3.28');shot(p,'stage8-left-sweep')
  p.evaluate('Q.action.t=Q.action.tell+3.98');shot(p,'stage8-right-sweep')
  ck('No browser or renderer exceptions',not errors,errors)
  br.close()
finally:stop()
(O/'trace.json').write_text(json.dumps(traces,indent=2));print(json.dumps({'checks':len(checks),'failed':[c['name']for c in checks if not c['passed']],'errors':errors}),flush=True)
