from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:1300],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?city16-probe');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.wait_for_function('()=>city16Warm()',polling=50)
 ck('all new asset keys registered',p.evaluate('city16Keys().every(k=>!!XART._src[k])'))
 for pk in p.evaluate('PILOTS.map(p=>p.key)'):
  q=p.evaluate("pk=>{run.pilot=pk;return{demo:fb2TeamScript().some(b=>['demo','callisto'].includes(b.kind)||/PRIVATE FIELD TESTS|ALLOW ME TO DEMONSTRATE/.test(b.text||'')),rows:c16Rows('post-6',pk).map(b=>({id:b.id,who:b.who,text:b.text})),after:city16Rows(pk,[CITY16_PAIRS[pk]].filter(Boolean)).map(b=>({who:b.who,text:b.text,album:b.city16Album})),dj:city16AlbumPilot(pk,[CITY16_PAIRS[pk]].filter(Boolean)),fallback:city16AlbumPilot(pk,[])}}",pk)
  ck(pk+' has no weapon showoff or Callisto demo',not q['demo'])
  ck(pk+' gets eight city-first post6 beats',len(q['rows'])==8 and any(v['who']=='COLE'and v['text'].startswith('Route us for the city.')for v in q['rows'])and any(v['text'].startswith('Underground? After we save')for v in q['rows']),q['rows'])
  ck(pk+' post-city dialogue and smiling album frame',len(q['after'])==7 and q['after'][-1].get('album')and q['after'][0]['who']=='COLE'and not(q['after'][2]['who']==q['after'][3]['who']),q['after'])
  ck(pk+' Juggernaut owns the album joke regardless of ally pairing',q['fallback']=='juggernaut'and q['dj']=='juggernaut')
 ck('all nine city dialogues keep reply panels and pan between speakers',p.evaluate("()=>PILOTS.every(({key:p})=>{const a=city16Rows(p,[CITY16_PAIRS[p]].filter(Boolean));return a[0].cm3.group===a[1].cm3.group&&a[0].people.join('|')===a[1].people.join('|')&&a[0].people.indexOf(a[0].who.toLowerCase())!==a[1].people.indexOf(a[1].who.toLowerCase())&&a[2].cm3.group===a[3].cm3.group&&a[4].cm3.group===a[5].cm3.group;})"))
 p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
 p.evaluate("()=>{GP4.route=null;GP4.routeReady=false;BAL7.setup({stage:6,kind:'warhive',pilot:'cole',diff:'furious',mode:'campaign',fire:false});player.invuln=999;boss=null;bossActive=false;BOFCinematicDirector.cancel();story=null;AP10_X.intro=null;s6Opening=null;run._mission29OpeningDone=true;CA111.active=null;CA111.completed=new Set(['pair-top','pair-bottom','nuclear','laser']);s6WingInit();s6Wing.fakeDone=true;s6Wing._fb2Talked=true;s6Wing.all=true;s6Wing.choice=true;stageTimer=80;PR118.cityT=20;Input.clearTaps();}")
 p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(6).ready&&city16Warm();}',polling=50)
 for diff in ['hard','furious']:
  p.evaluate("d=>{diffKey=d;s6Wing.frChoice={side:'left',t:1,mouse:false};ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);s6WingChoiceDraw();}",diff);p.locator('#screen').screenshot(path=str(O/('menu-'+diff+'.png')))
  ck(diff+' generated pursuit plate and baked route names',p.evaluate('FATE15.lastChoice.generated')and p.evaluate('FATE15.lastChoice.left')==('STORM CANNON'if diff=='furious'else'HARRIER'))
 p.evaluate("()=>{s6Wing.choice=false;s6Wing.route='left';ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}");p.locator('#screen').screenshot(path=str(O/'rural-flight.png'))
 ck('Stage6 split terrain is rural while city encounter remains urban',p.evaluate("()=>{const rural=_levelCfg(6).city;run._gp4StageX='left';const city=_levelCfg(6).city;delete run._gp4StageX;return rural===CITY16_ART.images.rural.key&&city!==rural;}"))
 p.evaluate("()=>{campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A',6:'A'};campaign.unlockedMax=7;campaign.cityRescue16=null;campaign.stageX1004={route:'right',target:'rebels',done:false};campaign.stage6Fate=fate15Receipt({...fate15Outcome('storm','furious'),version:1,id:'city16-probe',verified:false,pilot:'cole',crew:['cole','decker','axel','freezer','yuri']});openStageSelect(7,{unlock:7});}")
 p.wait_for_function('()=>{map4eWarm();return fury14MapReady();}',polling=50)
 ck('Stage7 stays locked after native map offer',p.evaluate('campaign.unlockedMax===6&&campaign.justUnlocked===0&&!sselUnlockCine&&city16NeedsCity()'))
 for i in range(450):
  e=p.evaluate(shoot.STEP,6)
  if e:errors.append(e);break
  q=p.evaluate('({elapsed:campaign.stage6Fate.elapsed,transit:campaign.stage6Fate.transitSeen,message:campaign.stage6Fate.messageSeen,cam:cmap2.cam,city:CF4.focus})')
  if 6.2<q['elapsed']<6.4:p.locator('#screen').screenshot(path=str(O/'closer-map-battle.png'))
  if q['message']and q['transit']:break
  p.wait_for_timeout(1)
 ck('closer city framing reaches requested zoom',q['cam']['z']>.32,q)
 ck('only city pursuit is next after transit',p.evaluate('city16NeedsCity()&&CF4.focus&&campaign.unlockedMax===6'))
 q=p.evaluate("()=>{window.illegalCity16=false;sselDeploy(7,()=>illegalCity16=true);const a=!illegalCity16&&!sselZoom;beginStage(7);return{a,stage:run.stage,state,cap:campaign.unlockedMax,city:city16NeedsCity()};}")
 ck('direct Stage7 deploy and begin cannot bypass city',q['a']and q['stage']==6 and q['state']=='stagesel'and q['cap']==6 and q['city'],q)
 saved=p.evaluate('Rival24.save()');p.evaluate('Rival24.load',saved);ck('pending city gate survives story save/load',p.evaluate('city16NeedsCity()&&campaign.unlockedMax===6'))
 p.locator('#screen').screenshot(path=str(O/'mandatory-city.png'))
 # Current owner refuses a fabricated city result without the native terminal callback.
 q=p.evaluate("()=>{run._gp4StageX='right';delete run._city16Defeat;const old=run.score;scLeaveStage({bonus:500,rank:'A'});delete run._gp4StageX;return run.score===old&&!campaign.stageX1004.done&&!campaign.cityRescue16;}")
 ck('unverified city result cannot unlock Stage7 or spend rewards',q)
 ck('no native page/console/HTTP errors',not errors,errors);b.close()
(O/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' native presentation/gate checks passed',flush=True)
assert all(c['ok']for c in checks)
