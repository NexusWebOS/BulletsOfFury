from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:1400],flush=True)
def step(p,n=6):
 e=p.evaluate(shoot.STEP,n)
 if e:raise RuntimeError(e)
 p.wait_for_timeout(1)
def wait_state(p,wanted,limit=2000):
 for i in range(limit):
  step(p)
  if p.evaluate('state')==wanted:return True
 return False
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for main in ['storm','rebels']:
  p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000);prefix=main+' -> city '
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?city16-life='+main);p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
  p.evaluate("k=>{GP4.route=null;GP4.routeReady=false;BAL7.setup({stage:6,kind:k==='storm'?'warhive':'rebelsquad',pilot:'cole',diff:'furious',mode:'campaign',fire:false});player.invuln=9999;campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A'};campaign.unlockedMax=6;campaign.cityRescue16=city16Receipt({version:1,completed:true,verified:true,debriefSeen:true,travelSeen:true});s6WingInit();s6Wing.route=k==='storm'?'left':'right';s6Wing.fakeDone=true;}",main)
  p.wait_for_function("k=>{stageLoadTick();rg4Warm();return city16Warm()&&fate15Warm()&&(k==='rebels'||fb112Ready());}",arg=main,polling=50)
  if main=='storm':p.evaluate("()=>{B._fb112.phase='recover';B._fb112.wait=999;B._tc119.flow=null;B._tc119.di=0;B.enter=false;for(const part of [...B._fb112.parts,B._fb112.core]){let n=0;while(part.hp>0&&n++<500){const at=fb112PartPoint(B,part);efxClock+=1/60;fb112Damage(B,1e6,at.x,at.y,part);}}}")
  else:p.evaluate("()=>{for(let i=0;i<B._rebels.ships.length;i++){const q=B._rebels.ships[i];if(q.key==='nyx'){ny46Hidden(q);rd21Reveal(q,'retina');for(let n=0;n<85;n++){efxClock+=1/60;rebelSquadTick(B,1/60);}}let n=0;while(!q.dead&&q.hp>0&&n++<160){B._rebels.hit=i;efxClock+=1/30;rebelSquadDamage(B,1e6);}}}")
  ck(prefix+'main encounter reaches native StageClear',wait_state(p,'stageclear'),p.evaluate('({state,hp:boss?.hp,dead:boss?.dead,defeat:run._stage6FateDefeat})'))
  ck(prefix+'main native terminal receipt is verified',p.evaluate('run._stage6FateDefeat?.verified===true'))
  p.evaluate("()=>{computeStageResults();window.mainResult16=drawStageClear._res;scLeaveStage(mainResult16);}")
  ck(prefix+'new main victory clears an older rescue receipt',p.evaluate('campaign.cityRescue16===null'))
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50);p.wait_for_function('()=>{map4eWarm();return fury14MapReady();}',polling=50)
  for i in range(1700):
   step(p)
   if p.evaluate('state===GS.STAGESEL&&campaign.stage6Fate?.awardNotified'):break
  ck(prefix+'native post6/map offers mandatory city and locked7',p.evaluate('state===GS.STAGESEL&&city16NeedsCity()&&campaign.unlockedMax===6&&campReadAuto().stage===6&&campReadAuto().unlockedMax===6'),p.evaluate('({state,cap:campaign.unlockedMax,receipt:campaign.stage6Fate,auto:campReadAuto()?.stage})'))
  p.locator('#screen').screenshot(path=str(O/(main+'-city-required.png')))
  ck(prefix+'actual native city pursuit launches',p.evaluate('cf4LaunchX()'))
  for i in range(1600):
   step(p)
   if p.evaluate('!!boss'):break
  q=p.evaluate('({kind:boss?.kind,city:run._gp4StageX,storm:!!boss?._fb112})');target='rebels'if main=='storm'else'harrier'
  ck(prefix+'correct real city opponent',q.get('city')==('right'if target=='rebels'else'left')and q.get('kind')==('rebelsquad'if target=='rebels'else'warhive')and not q['storm'],q)
  damageCalls=0;prior=None
  for i in range(3600):
   # Native Retina and missile-impact dispatch. Protection, individual shield/
   # module pools, the carrier's Nightwing handoff, and all death owners run.
   q=p.evaluate("()=>{if(boss&&!boss.dead){for(const q of boss._rebels?.ships||[])if(q.key==='nyx'&&boss._rebels.frIntro?.done)rd21Reveal(q,'retina');let hits=0;for(const t of _lockTargets().slice())if((t===boss||t._retinaOwner===boss)&&!t.dead){if(retinaMissileDamage(t,1e6))hits++;}return{hits,hp:boss.hp,mode:boss._whv?.mode,scene:BOFCinematicDirector.current?.id,phase:boss._rebels?.frIntro?.done};}return{hits:0};}")
   damageCalls+=q['hits'];step(p)
   phase=(q.get('mode'),q.get('scene'),q.get('phase'))
   if phase!=prior:print(prefix+'PHASE',phase,flush=True);prior=phase
   if p.evaluate('state===GS.STAGECLEAR'):break
  q=p.evaluate('({state,hp:boss?.hp,dead:boss?.dead,proof:run._city16Defeat,role:run._gp4StageX})')
  ck(prefix+'all native city pools/deaths reach results',q['state']=='stageclear'and q['hp']<=0 and q['dead']and q.get('proof',{}).get('verified')and damageCalls>0,q)
  if q['state']!='stageclear':raise RuntimeError('Native city encounter did not finish: '+json.dumps(q))
  p.evaluate("()=>{computeStageResults();window.cityResult16=drawStageClear._res;window.scoreBefore16=run.score;scLeaveStage(cityResult16);window.scoreAfter16=run.score;scLeaveStage(cityResult16);}")
  q=p.evaluate('({state,id:BOFCinematicDirector.current?.id,score:run.score,before:scoreBefore16,after:scoreAfter16,bonus:cityResult16.bonus,receipt:campaign.cityRescue16,x:campaign.stageX1004,cap:campaign.unlockedMax,super:run.missileTier,rewards:AP10_X.events.filter(e=>e.event===\'air-superiority-reward\').length,mk2:fs11Enhanced(),auto:campReadAuto()})')
  ck(prefix+'native bonus settles exactly once',q['score']==q['after']==q['before']+q['bonus'],{k:q[k]for k in ['score','before','after','bonus']})
  ck(prefix+'city receipt waits for seven-beat debrief before7',q['state']=='cutscene'and q['id']=='post-city16'and q['receipt']['completed']and not q['receipt']['debriefSeen']and q['cap']==6 and q['x']['done'],q['receipt'])
  ck(prefix+'native Super Missile and MkII rewards retained once',q['rewards']==1 and q['mk2']and q['x'].get('rewarded'),{'super':q['super'],'events':q['rewards'],'mk2':q['mk2']})
  mid=q['auto'];ck(prefix+'mid-debrief autosave retains actual city victory and score',mid['rival24']['cityRescue16']['completed']and not mid['rival24']['cityRescue16']['debriefSeen']and mid['stage']==6 and mid['score']==q['score'])
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50);seen=set();album=False;chibi=False
  for i in range(1000):
   step(p);q=p.evaluate('({state,id:BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id,t:BOFCinematicDirector.current?.t,receipt:campaign.cityRescue16,travel:CITY16.travel,ship:sselShip,album:CITY16.lastAlbum})')
   if q.get('id')and q['t']>1.3 and q['id']not in seen:
    seen.add(q['id']);p.locator('#screen').screenshot(path=str(O/(main+'-'+q['id']+'.png')))
    if q['id']=='CITY16-ALBUM':album=True
   if q['state']=='stagesel'and q.get('travel')and 1.4<q['travel']['t']<1.65 and not chibi:chibi=True;p.locator('#screen').screenshot(path=str(O/(main+'-chibi-flight.png')))
   if q['state']=='stagesel'and q['receipt']['travelSeen']:break
  ck(prefix+'all six conversations and full smiling album appear',len(seen)==7 and album,sorted(seen))
  ck(prefix+'map chibi reaches7 without auto-starting the stage',chibi and q['state']=='stagesel'and q['receipt']['debriefSeen']and q['receipt']['travelSeen']and p.evaluate('sselCursor===7&&campaign.unlockedMax>=7&&!city16Gate()'),q)
  ck(prefix+'native autosave now resumes at unlocked7',p.evaluate('campReadAuto().stage===7&&campReadAuto().rival24.cityRescue16.travelSeen&&campReadAuto().score===run.score'))
  ck(prefix+'Stage7 selection is enabled after the city scene',p.evaluate("()=>{sselDeploy(7,()=>{});const ok=!!sselZoom;sselZoom=null;return ok;}"))
  # Resume an actual mid-scene checkpoint. The battle/rewards must not repeat.
  count=p.evaluate('AP10_X.events.filter(e=>e.event===\'air-superiority-reward\').length');p.evaluate('campApply',mid)
  ck(prefix+'loading a city-clear checkpoint resumes its debrief',p.evaluate('BOFCinematicDirector.current?.id===\'post-city16\'&&city16NeedsDebrief()&&campaign.unlockedMax===6&&campaign.stageX1004.done'))
  ck(prefix+'resume cannot repay city bonus or rewards',p.evaluate('run.score')==mid['score']and p.evaluate('AP10_X.events.filter(e=>e.event===\'air-superiority-reward\').length')==count)
  p.evaluate('()=>BOFCinematicDirector.finish()');ck(prefix+'native skip completes once and returns to7 map',p.evaluate('campaign.cityRescue16.debriefSeen&&state===GS.STAGESEL&&sselCursor===7'))
  p.close()
 ck('no native page/console/HTTP errors',not errors,errors);b.close()
(O/'lifecycle-qa.json').write_text(json.dumps({'scope':'Native scripted damage through real module/Retina/missile impact/terminal death/result owners; full post6/map and city-debrief/chibi continuation. Not unassisted gameplay wins.','checks':checks,'errors':errors},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' native lifecycle checks passed',flush=True)
assert all(c['ok']for c in checks)
