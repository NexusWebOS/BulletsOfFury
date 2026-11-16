from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:900],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?fate-native-routes');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
 for diff in ['hard','furious']:
  for side in ['left','right']:
   p.evaluate("d=>{GP4.route=null;GP4.routeReady=false;BAL7.setup({stage:6,kind:'warhive',pilot:'cole',diff:d,mode:'campaign',fire:false});BOFCinematicDirector.cancel();story=null;AP10_X.intro=null;s6Opening=null;fb2Talk=null;CA111.active=null;CA111.completed=new Set(['pair-top','pair-bottom','nuclear','laser']);boss=null;bossActive=false;bossDefeated=false;debugFight=null;stagePlan=[];spawnClock=9999;stageTimer=80;run._mission29OpeningDone=true;s6WingInit();s6Wing.fakeDone=true;s6Wing._fb2Talked=true;s6Wing.beats=3;s6Wing.all=true;s6Wing.postMiniT=99;s6Wing.supplyIndex=3;s6Wing.choice=true;setState(GS.PLAY);Input.clearTaps();}",diff)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(6).ready&&city16Warm()&&fate15Warm();}',polling=50)
   for readyFrame in range(600):
    p.evaluate(shoot.STEP,6)
    if p.evaluate('(s6Wing.frChoice?.t||0)>.25'):break
    p.wait_for_timeout(2)
   print('INPUT_READY',diff,side,p.evaluate('({state,route:s6Wing.route,choice:s6Wing.choice,selector:s6Wing.frChoice,auto:s6Wing.autoRoute})'),flush=True)
   q=p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);s6WingChoiceDraw();return FATE15.lastChoice;}")
   ck(diff+' '+side+' pursuit label matches difficulty',q['left']==('HARRIER'if diff=='hard'else'STORM CANNON'),q)
   if diff=='hard'and side=='left':p.locator('#screen').screenshot(path=str(O/'hard-harrier-choice.png'))
   # Real pointer input starts a native campaign route briefing. Its callback,
   # rather than the initial click, commits W.autoRoute and the actual pursuit.
   box=p.locator('#screen').bounding_box();p.mouse.move(box['x']+box['width']*(.28 if side=='left'else .72),box['y']+box['height']*.49);p.mouse.down()
   for clickFrame in range(60):
    p.evaluate(shoot.STEP,1)
    if p.evaluate('!!BOFCinematicDirector.current'):break
   p.mouse.up()
   q=p.evaluate('({route:s6Wing.route,scene:BOFCinematicDirector.current?.id,lines:BOFCinematicDirector.current?.beats.map(b=>b.text)})')
   ck(diff+' '+side+' real pointer opens the native route briefing',q.get('scene')=='route-'+side,q)
   if side=='left':ck(diff+' route briefing names actual left boss',('Storm Cannon'if diff=='furious'else'Harrier')in' '.join(q.get('lines')or[]),q)
   for i in range(1000):
    p.evaluate(shoot.STEP,6)
    if p.evaluate('!!boss'):break
    p.wait_for_timeout(1)
   q=p.evaluate('({kind:boss?.kind,model:boss?._fb112?.model,rebels:!!boss?._rebels,harrier:!!boss?._whv,city:run._gp4StageX})')
   expected=side=='right'and q['rebels']or side=='left'and(q['model']=='thunder'if diff=='furious'else q['harrier'])
   ck(diff+' '+side+' native route spawns correct actual encounter',expected,q)
   ck(diff+' '+side+' briefing callback commits pursuit',p.evaluate('s6Wing.route')==side)
 ck('native logical route input has no page/console/HTTP errors',not errors,errors);b.close()
(O/'routes-qa.json').write_text(json.dumps({'scope':'Prepared native choice, actual Chromium pointer click, complete native campaign route briefing/callback, then actual boss spawn. No controller hardware claim.','checks':checks,'errors':errors},indent=2),encoding='utf8');print(str(sum(v['ok']for v in checks))+'/'+str(len(checks))+' native pointer-route checks passed',flush=True)
assert all(v['ok']for v in checks)
