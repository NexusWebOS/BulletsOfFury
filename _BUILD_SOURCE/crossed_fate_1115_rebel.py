from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/crossed_fate_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:1600],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?fate-rebel');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
 p.evaluate("()=>{GP4.route=null;GP4.routeReady=false;BAL7.setup({stage:6,kind:'rebelsquad',pilot:'cole',diff:'furious',mode:'campaign',fire:false});player.invuln=999;s6WingInit();s6Wing.route='right';s6Wing.fakeDone=true;}")
 p.wait_for_function('()=>{stageLoadTick();rg4Warm();return fate15Warm();}',polling=50)
 q=p.evaluate("()=>{const calls=[];for(let i=0;i<B._rebels.ships.length;i++){const q=B._rebels.ships[i];if(q.key==='nyx'){ny46Hidden(q);rd21Reveal(q,'retina');for(let f=0;f<85;f++){efxClock+=1/60;rebelSquadTick(B,1/60);}}let n=0;while(!q.dead&&q.hp>0&&n++<160){B._rebels.hit=i;efxClock+=1/30;rebelSquadDamage(B,1e6);}calls.push({key:q.key,hp:q.hp,dead:q.dead,shield:q.shield,hits:n});}return{kind:B.kind,hp:B.hp,dead:B.dead,ships:calls,scene:rg4State()?.scene,defeat:run._stage6FateDefeat,reveal:NY46.events};}")
 print('NATIVE_REBEL_POOLS',json.dumps(q),flush=True)
 ck('five native Rebel ships are defeated through damage owner',len(q['ships'])==5 and all(v['dead']or v['hp']<=0 for v in q['ships']),q)
 for i in range(400):
  err=p.evaluate(shoot.STEP,6)
  if err:errors.append(err);break
  if p.evaluate('!!run._stage6FateDefeat'):break
  p.wait_for_timeout(1)
 q['defeat']=p.evaluate('run._stage6FateDefeat||null')
 ck('verified Rebel outcome comes from native terminal callback',(q.get('defeat')or{}).get('defeated')=='rebels'and q['defeat']['verified'],q.get('defeat'))
 ck('Road Not Taken remains locked before the campaign map',not p.evaluate("achievementUnlocked('road_not_taken')"))
 p.evaluate("()=>{run.score=12000;window.rebelResult15={bonus:500,rank:'A'};campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A'};campaign.unlockedMax=6;scLeaveStage(rebelResult15);}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 p.wait_for_function('()=>{map4eWarm();return fury14MapReady();}',polling=50)
 road=False;west=False;message=False;before=p.evaluate('achievementPoints()')
 for i in range(1500):
  err=p.evaluate(shoot.STEP,6)
  if err:errors.append(err);break
  q=p.evaluate('({state,receipt:campaign.stage6Fate,last:FATE15.last,award:FATE15.lastAward,message:FATE15.lastMessage})')
  if q['state']=='stagesel':
   t=q['receipt']['elapsed']
   if not west and t>2.2 and t<3.6:west=True;p.locator('#screen').screenshot(path=str(O/'verified-storm-west.png'))
   if not message and q.get('message')and q['message']['shown']>90:message=True;p.locator('#screen').screenshot(path=str(O/'verified-rebel-password.png'))
   if not road and q.get('award')and q['award']['time']>.85:road=True;p.locator('#screen').screenshot(path=str(O/'road-not-taken-award.png'))
  if q['receipt']['awardNotified']:break
  p.wait_for_timeout(1)
 ck('native result routes Harrier to city and Storm west',q['receipt']['target']=='harrier'and q['receipt']['escape']and not q['receipt']['crash']and west,q['receipt'])
 ck('exact Furious redemption password is written and faded',message and q['receipt']['messageSeen'],q.get('message'))
 ck('generated Rebel victory medal appears only on map',road and q['state']=='stagesel',q.get('award'))
 ck('only correct route achievement unlocks once',p.evaluate("achievementUnlocked('road_not_taken')&&!achievementUnlocked('crossed_fate')&&achievementPoints()")-before==200)
 saved=p.evaluate('Rival24.save()');p.evaluate('Rival24.load',saved)
 ck('west escape and Harrier city target survive load',p.evaluate("campaign.stage6Fate.escape&&campaign.stage6Fate.awardNotified&&campaign.stageX1004.route==='left'"))
 ck('no page console HTTP errors',not errors,errors);b.close()
(O/'rebel-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' Rebel route checks passed',flush=True)
assert all(c['ok']for c in checks)
