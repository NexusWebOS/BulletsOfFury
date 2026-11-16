from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/crossed_fate_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:1200],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?fate-integration');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 q=p.evaluate("()=>{setState(GS.PASSWORD);pwInput='STRM';submitPassword();return{stage:PENDING_STAGE,state,passwordDifficulty};}")
 ck('native STRM submit enters difficulty selection for Stage6',q['stage']==6 and q['state']=='diff'and q['passwordDifficulty'],q)
 q=p.evaluate("()=>{setState(GS.PASSWORD);pwInput='BASE4';submitPassword();return{stage:PENDING_STAGE,state};}")
 ck('native BASE4 submit preserves Stage4 access',q['stage']==4,q)
 p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
 p.evaluate("()=>{GP4.route=null;GP4.routeReady=false;BAL7.setup({stage:6,kind:'warhive',pilot:'cole',diff:'furious',mode:'campaign',fire:false});player.invuln=999;B._fb112.phase='recover';B._fb112.wait=999;B._tc119.flow=null;B._tc119.di=0;B.y=180;B.enter=false;s6WingInit();s6Wing.route='left';s6Wing.fakeDone=true;}")
 p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&fate15Warm();}',polling=50)
 ck('Furious left route spawns actual modular Storm Cannon',p.evaluate("B._fb112.model==='thunder'&&B.name==='STORM CANNON'&&tc119Own(B)"))
 p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}");p.locator('#screen').screenshot(path=str(O/'storm-native-combat.png'))
 q=p.evaluate("()=>{const c=B._fb112.core,old=c.hp,at=fb112PartPoint(B,c),hit=fb112Damage(B,1e7,at.x,at.y,c);return{old,after:c.hp,hit};}")
 ck('actual protected core resists early damage',q['old']==q['after'],q)
 q=p.evaluate("()=>{const calls=[];for(const part of B._fb112.parts){let n=0;while(part.hp>0&&n++<250){const m=fb112PartPoint(B,part);efxClock+=1/60;fb112Damage(B,1e6,m.x,m.y,part);}calls.push({id:part.id,hp:part.hp,hits:n});}return{calls,open:B._fb112.open,core:B._fb112.core.hp,total:B.hp};}")
 ck('all six native module pools must fall before core opens',q['open']and len(q['calls'])==6 and all(v['hp']==0 for v in q['calls'])and q['core']>0,q)
 q=p.evaluate("()=>{const part=B._fb112.core;let n=0;while(part.hp>0&&n++<500){const m=fb112PartPoint(B,part);efxClock+=1/60;fb112Damage(B,1e6,m.x,m.y,part);}return{core:part.hp,hp:B.hp,dead:B.dead,defeat:run._stage6FateDefeat,events:FATE15.events};}")
 ck('native core defeat records verified Storm victory exactly once',q['core']==0 and q.get('defeat',{}).get('defeated')=='storm'and q['defeat']['verified']and sum(v['event']=='native-defeat'for v in q['events'])==1,q)
 ck('Storm achievement stays locked before map arrival',not p.evaluate("achievementUnlocked('crossed_fate')"))
 p.evaluate("()=>{run.score=12000;window.realResult15={bonus:500,rank:'A'};campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A'};campaign.unlockedMax=6;scLeaveStage(realResult15);window.firstReceipt15=campaign.stage6Fate.id;scLeaveStage(realResult15);}")
 ck('native settlement grants its bonus once and creates one receipt',p.evaluate("run.score===12500&&campaign.stage6Fate.id===firstReceipt15&&campaign.stage6Fate.verified&&campaign.stageX1004.route==='right'"),p.evaluate('({score:run.score,receipt:campaign.stage6Fate,state})'))
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 p.wait_for_function('()=>{map4eWarm();return fury14MapReady();}',polling=50)
 awardSeen=False;messageSeen=False;mapSeen=False;beforePoints=p.evaluate('achievementPoints()');prior=None
 for i in range(1400):
  e=p.evaluate(shoot.STEP,6)
  if e:errors.append(e);break
  q=p.evaluate('({state,shot:BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id,receipt:campaign.stage6Fate,award:FATE15.lastAward,message:FATE15.lastMessage})')
  if q['state']!=prior:print('STATE',q['state'],flush=True);prior=q['state']
  if q['state']=='stagesel':mapSeen=True
  if q.get('message')and not messageSeen:messageSeen=True
  if q.get('award')and q['award'].get('time',0)>.85 and not awardSeen:awardSeen=True;p.locator('#screen').screenshot(path=str(O/'crossed-fate-award.png'))
  if q['receipt'].get('awardNotified'):break
  p.wait_for_timeout(1)
 ck('all native post6 beats reach the map without replacing continuation',mapSeen and q['state']=='stagesel',q)
 ck('map displays password then generated Crossed Fate card',messageSeen and awardSeen and q['receipt']['awardNotified'],q)
 ck('route award grants exactly200 points once',p.evaluate('achievementPoints()')-beforePoints==200,{'before':beforePoints,'after':p.evaluate('achievementPoints()')})
 ck('recorded route and map progress persist in native autosave',p.evaluate("campReadAuto()?.rival24?.stage6Fate?.awardNotified===true&&campReadAuto().rival24.stageX1004.route==='right'"))
 ck('award survives profile reload without duplicate points',p.evaluate("()=>{const n=achievementPoints();achievementReload();return achievementUnlocked('crossed_fate')&&achievementPoints()===n&&!achievementUnlock('crossed_fate',{});}"))
 # The city encounter must remain the actual Harrier on Furious, never the storm replacement.
 p.evaluate("()=>{campaign.stageX1004={route:'left',target:'harrier',done:false};cf4LaunchX();}")
 for i in range(800):
  p.evaluate(shoot.STEP,6)
  if p.evaluate('!!boss'):break
  p.wait_for_timeout(2)
 q=p.evaluate("({state,stage:run.stage,city:run._gp4StageX,kind:boss?.kind,storm:!!boss?._fb112,receipt:campaign.stage6Fate.defeated,intro:AP10_X.intro,route:GP4.route,ready:GP4.routeReady,scene:BOFCinematicDirector.current?.id,load:stageLoadInfo(6)})")
 ck('Furious city left pursuit retains native Harrier',q['city']=='left'and q['kind']=='warhive'and not q['storm'],q)
 ck('city launch does not rewrite original Stage6 outcome',q['receipt']=='storm',q)
 # Native drawn split: both complete hulls and their independent shadow banks.
 p.evaluate("()=>{GP4.route=null;GP4.routeReady=false;BAL7.setup({stage:6,kind:'warhive',pilot:'cole',diff:'furious',mode:'campaign',fire:false});run._gp4StageX=null;BOFCinematicDirector.cancel();story=null;s6Opening=null;AP10_X.intro=null;boss=null;bossActive=false;s6WingInit();s6Wing.fake={t:1.35*1.3};s6Wing.all=true;setState(GS.PLAY);Input.clearTaps();}")
 q=p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return FATE15.last;}")
 ck('Furious overflight shows Harrier leading Storm Cannon',len(q['passes'])==2 and q['passes'][0]['u']>q['passes'][1]['u'],q)
 for t,label in [(.8,'harrier'),(1.95,'storm')]:
  p.evaluate("t=>{s6Wing.fake.t=t*1.35;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}",t)
  p.locator('#screen').screenshot(path=str(O/('furious-'+label+'-overflight.png')))
 p.evaluate("()=>{s6Wing.fake=null;s6Wing.choice=true;s6Wing.route=null;setState(GS.PLAY);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);s6WingChoiceDraw();}")
 p.locator('#screen').screenshot(path=str(O/'furious-storm-choice.png'))
 ck('no native page/console/HTTP errors',not errors,errors);b.close()
(O/'integration-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' integration checks passed',flush=True)
assert all(c['ok']for c in checks)
