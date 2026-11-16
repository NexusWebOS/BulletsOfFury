from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path('D:/BOF-Downloads/2026-11-14/RevG-source');O=R/'_shots/hq_swarm_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[];tags=[];samples=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?stage67flow');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.mode='campaign';run.stage=6;curStage=STAGES[5];run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');diffKey='hard';DIFF=difficultyForRun('campaign','hard');campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A',6:'A'};campaign.unlockedMax=7;run.gravityShipReady=false;run.spaceMode=false;window.post6Done=0;BOFCinematicDirector.start(6,()=>{post6Done++;Input.clearTaps();beginStage(7);});}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 prior=None;playFrames=0
 for i in range(1500):
  err=p.evaluate(shoot.STEP,6)
  if err:errors.append(err);break
  q=p.evaluate("({state,stage:run.stage,t:stateT,scene:BOFCinematicDirector.current?.id,shot:BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id,story:story&&{i:story.i,t:story.t,who:story.who},phase:drawLaunch._phase,post6Done,brief:run._sewerBriefed17})")
  tag=str((q['state'],q.get('scene'),q.get('shot'),q.get('phase'),bool(q.get('story'))))
  if tag!=prior:
   tags.append(q);print(json.dumps(q),flush=True);prior=tag
  if i%60==0 or q.get('shot')in ['POST6-06','POST6-08']and i%15==0:p.locator('#screen').screenshot(path=str(O/('stage67-flow-%03d.png'%i)))
  if q['state']=='play'and q['stage']==7 and not q.get('story'):
   playFrames+=6
   if playFrames>=240:break
  p.wait_for_timeout(1)
 b.close()
(O/'stage67-flow.json').write_text(json.dumps({'tags':tags,'end':q,'errors':errors},indent=2),encoding='utf8');assert not errors;assert q['stage']==7 and q['state']=='play'and q['post6Done']==1
