from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/service_link_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
errors=[];report={'pilots':[],'shots':[]}
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?service-link-review=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;beginStage(2);warmStage(2);}")
 p.wait_for_function('()=>{stageLoadTick();ls112Warm(2);return stageLoadInfo(2).ready&&ls112Keys(2).every(k=>XART.rdy(k));}',polling=50)
 p.evaluate("()=>{bossActive=subBossActive=false;mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;campaign.unlockedMax=3;Input.clearTaps();Input.mouse.down=false;}")
 for pk in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
  p.evaluate("pk=>{BOFCinematicDirector.cancel();run.pilot=pk;pilotIndex=PILOTS.findIndex(p=>p.key===pk);BOFCinematicDirector.start(2,()=>{});}",pk)
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
  p.evaluate(shoot.STEP,100)
  (OUT/('radio-'+pk+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]))
  report['pilots'].append(p.evaluate('()=>({pilot:run.pilot,render:SL14.last,lines:BOFCinematicDirector.current.beats.map(b=>({id:b.id,who:b.who,text:b.text,mode:b.service14})),portrait:FP5_ART.banks["talk-zoom-cole"].key})'))
 # Full native post-Stage-2 continuation into its actual map owner.
 p.evaluate("""()=>{BOFCinematicDirector.cancel();run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');window.mapReturnCount=0;window.serviceSounds=[];const play=Snd.play;Snd.play=function(name,...v){const r=play.call(this,name,...v);if(['bossWeaponCharge','jetDash'].includes(name))serviceSounds.push({name,ok:r});return r;};BOFCinematicDirector.start(2,()=>{mapReturnCount++;openStageSelect(3,{});});Input.clearTaps();Input.mouse.down=false;window.serviceBefore={x:player.x,y:player.y,score:run.score,lives:run.lives};}""")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 seen=[]
 for sec in range(95):
  for _ in range(4):
   err=p.evaluate(shoot.STEP,15)
   if err:errors.append(err)
   p.wait_for_timeout(5)
  q=p.evaluate('()=>({state,render:SL14.last,row:BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id,done:mapReturnCount,mapFade:SL14.mapFade})');report['shots'].append(q)
  row=q.get('row')
  if row and row not in seen:
   seen.append(row);(OUT/(row+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]))
  if q['state']=='stagesel' and q['mapFade']==0:
   (OUT/'returned-map.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]));break
 report['completed']=p.evaluate('()=>({state,returns:mapReturnCount,events:SL14.events,sounds:serviceSounds,before:serviceBefore,after:{x:player.x,y:player.y,score:run.score,lives:run.lives},portrait:FP5_ART.banks["talk-zoom-cole"]})')
 # A skipped conversation still invokes the native map callback once.
 p.evaluate("()=>{BOFCinematicDirector.start(2,()=>{mapReturnCount++;openStageSelect(3,{});});}")
 p.evaluate(shoot.STEP,60);p.keyboard.press('Enter');p.evaluate(shoot.STEP,3)
 report['skip']=p.evaluate('({state,returns:mapReturnCount})')
 b.close()
report['errors']=errors;report['seen']=seen
checks={'noErrors':not errors,'allPilotsUseOwnCockpit':all(q['render']['identityKey']=='s113_cockpit-'+q['pilot'] for q in report['pilots']),'deckerUsesColeSupport':next(q for q in report['pilots'] if q['pilot']=='decker')['render']['tech']=='cole','newColeArt':report['completed']['portrait']['key']=='sl14_cole_talk_zoom','allTenShots':len(seen)==10,'returnsToMapOnce':report['completed']['state']=='stagesel' and report['completed']['returns']==1,'gameplayPositionAndRewardsUntouched':report['completed']['before']==report['completed']['after'],'skipReturnsOnce':report['skip']=={'state':'stagesel','returns':2},'chargeAndTakeoffCue':[q['name'] for q in report['completed']['sounds']]==['bossWeaponCharge','jetDash']}
report['checks']=checks;(OUT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'checks':checks,'completed':report['completed'],'skip':report['skip'],'errors':errors},indent=2),flush=True)
assert all(checks.values()),checks
