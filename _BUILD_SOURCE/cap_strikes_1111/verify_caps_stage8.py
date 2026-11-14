from pathlib import Path
import sys,json,math,time,subprocess
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=W.parent/'outputs/End-cap-strikes'/('verification-stage'+sys.argv[1]);O.mkdir(parents=True,exist_ok=True)
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
  p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return ba119Warm(8)}',polling=50,timeout=180000)
  p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=false;B._noHit=false;BOFCinematicDirector.cancel();window.Q=hb20State(B);}")
  for diff in ['normal','hard','furious']:
   for mat in ['regular','chrome','red']:
    q=p.evaluate("""([d,m])=>{diffKey=d;DIFF=difficultyForRun(run.mode,d);B._r30.mode='fight';B._r30.v18.donorAge=0;Q.rf1110=null;Q.chrome=m!=='regular';Q.rage=m==='red';B.x=worldWidth()/2;B.y=viewTopY()+180;Q.action=null;Q.cool=999;BA119.events=[];hb20Start(B,'skystrike');const A=Q.action;let root=null,drift=0,poses=new Set(),behindFirst=0,behindSecond=0;for(let i=0;i<600&&Q.action===A;i++){v19NativeTick(B,1/60);if(Q.action===A){const q=hb20Pose(B);poses.add(q.a.bank+':'+q.a.frame);if(q.a.phase==='behind-head'){if(A.t-A.tell<1.4)behindFirst++;else behindSecond++;}if(A.t-A.tell>=.55){root??={x:B.x,y:B.y};drift=Math.max(drift,Math.hypot(B.x-root.x,B.y-root.y));}}}return{diff:d,mat:m,drift,unique:poses.size,behindFirst,behindSecond,events:BA119.events.slice()};}""",[diff,mat]);traces.append(q)
    ck(f'Stage8 {diff}/{mat}: correct one/double/four contacts',len(q['events'])==({'normal':1,'hard':2,'furious':4}[diff]),q['events'])
    ck(f'Stage8 {diff}/{mat}: no hops or torso chase after landing',q['drift']<.01,q['drift'])
    ck(f'Stage8 {diff}/{mat}: actual behind-head windup on every down strike',q['behindFirst']>0 and (diff=='normal' or q['behindSecond']>0),dict(first=q['behindFirst'],second=q['behindSecond']))
  p.evaluate("()=>{Q.rage=Q.chrome=false;B.x=worldWidth()/2;B.y=viewTopY()+220;Q.action=null;hb20Start(B,'skystrike');Q.action.t=Q.action.tell+1.8;ba119Root(B,Q.action);}");shot(p,'stage8-overhead-windup')
  p.evaluate('Q.action.t=Q.action.tell+1.0');shot(p,'stage8-contact-face')
  p.evaluate('Q.action.t=Q.action.tell+3.28');shot(p,'stage8-left-sweep')
  p.evaluate('Q.action.t=Q.action.tell+3.98');shot(p,'stage8-right-sweep')
  p.evaluate("()=>{Q.rage=Q.chrome=false;Q.rf1110=null;Q.action=null;hb20Start(B,'skystrike');Q.action.t=Q.action.tell+1.72;ba119Root(B,Q.action);B.flash=0;efxClock=Math.ceil(efxClock/.05)*.05;}");shot(p,'stage8-native-pose')
  p.evaluate('GP4.clock+=1;markHit(B,.16)');shot(p,'stage8-native-hit')
  ck('Stage8 white hit flash changes native damaged pixels',(O/'stage8-native-pose.png').read_bytes()!=(O/'stage8-native-hit.png').read_bytes())
  p.evaluate('for(let i=0;i<18;i++)updateBoss(1/60)')
  ck('Stage8 native white flash expires',p.evaluate('B.flash<=0'))
  from record_loaded import record_loaded
  record_loaded(p,8,errors)
  ck('No browser or renderer exceptions',not errors,errors)
  br.close()
finally:stop()
(O/'trace.json').write_text(json.dumps(traces,indent=2));print(json.dumps({'checks':len(checks),'failed':[c['name']for c in checks if not c['passed']],'errors':errors}),flush=True)
