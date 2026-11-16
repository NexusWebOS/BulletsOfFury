from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/('_shots/cinema_overnight_1116/'+(sys.argv[1]if len(sys.argv)>1 else'arrivals'));O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 pilots=['axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva','cole'];cases=[{'stage':7,'pilot':pk,'partner':None}for pk in pilots]+[{'stage':n,'pilot':'cole','partner':None}for n in[1,2,3,4,5,6,8,9]]+[{'stage':7,'pilot':'decker','partner':'cole'}]
 for case in cases:
  p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?night-arrivals=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{BOFOnline.submitScore=()=>{};}')
  e0=len(errors);p.evaluate("q=>{BOFCinematicDirector.cancel();D1110.paused=false;Input.clearTaps();Input.mouse.down=false;for(const k of Object.keys(Input.keys))Input.keys[k]=false;debugFight=null;P2M.active=null;run.mode='campaign';run.pilot=q.pilot;pilotIndex=PILOTS.findIndex(p=>p.key===q.pilot);diffKey='hard';coopOn=!!q.partner;if(q.partner)p2Index=PILOTS.findIndex(p=>p.key===q.partner);startRun(1);BOFCinematicDirector.cancel();campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A',6:'A'};campaign.unlockedMax=9;campaign.stageX1004=null;campaign.cityRescue16=null;delete run._gp4StageX;beginStage(q.stage);warmStage(q.stage);}",case)
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',polling=50)
  p.evaluate("()=>{BOFCinematicDirector.cancel();story=null;setState(GS.INTRO);resetIntro();drawLaunch._phase=undefined;window.NightPlayerPaints=[];window.NightIntroDraws=0;window.NightIntroPhases=[];}")
  phases=[];last=None;trace=[];play_at=None;step_error=None
  for j in range(1800):
   problem=p.evaluate(shoot.STEP,6)
   if problem:step_error=problem;break
   q=p.evaluate("()=>({state,phase:drawLaunch._phase,scene:BOFCinematicDirector.current?.id,shot:BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id,stage:run.stage,x:player.x,y:player.y,dead:player.dead,invuln:player.invuln,cam:camX,view:cv.width/SS,world:worldWidth(),mapScroll,clock:stageTimer,opening:s6Opening?.phase,water:CW16.water.last,bed:LS112.clock.bed,scroll:drawLaunch._bgScroll})")
   tag='|'.join(str(q.get(k,''))for k in['state','phase','scene','shot','opening'])
   if tag!=last:
    phases.append({'at':j*.1,'tag':tag,**q});last=tag
    if q['state']=='launch'and len(phases)%3==0:p.screenshot(path=str(O/(str(case['stage'])+'-'+case['pilot']+'-launch-'+str(len(phases))+'.jpg')),type='jpeg',quality=84)
   if q['state']=='play'and not q.get('scene')and not q.get('shot')and not p.evaluate('!!story'):
    if play_at is None:play_at=j
    trace.append(q)
    if j-play_at>=35:break
   else:play_at=None
   p.wait_for_timeout(1)
  p.evaluate('()=>SC12.refresh()');fn=str(case['stage'])+'-'+case['pilot']+('-coop'if case['partner']else'')+'-play.png';p.screenshot(path=str(O/fn));end=p.evaluate('({state,stage:run.stage,pilot:run.pilot,x:player.x,y:player.y,dead:player.dead,invuln:player.invuln,viewport:{w:cv.width,h:cv.height},view:viewW(),left:camLeftX(),right:camRightX(),p2:coopOn?{x:player2.x,y:player2.y,dead:player2.dead}:null,water:CW16.water})')
  jumps=[{'before':a,'after':z}for a,z in zip(trace,trace[1:])if abs(z['x']-a['x'])>5 or abs(z['y']-a['y'])>5]
  row={'case':case,'end':end,'phases':phases,'playTrace':trace,'jumps':jumps,'stepError':step_error,'errors':errors[e0:],'screenshot':fn,'reachedPlay':play_at is not None,'finite':all(isinstance(end[k],(int,float))for k in['x','y'])};rows.append(row)
  row['approachSeen']=any(z.get('scene')=='stage7-approach'for z in phases)if case['stage']==7 else None
  (O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors,'scope':'Fresh isolated pages and native startRun initialization for every prepared unlocked Hard campaign profile: all9 Stage7 native card/approach/sewer/launch handoffs, other stage arrivals with Cole and Decker+Cole Stage7 co-op. Actual loop and stage owners, no HP/god writes. First3.5 seconds of native PLAY sampled; not campaign wins or complete opening interceptions.'},indent=2),encoding='utf8')
  print(json.dumps({'case':case,'reached':row['reachedPlay'],'end':end,'jumps':len(jumps),'stepError':step_error,'errors':row['errors']}),flush=True)
  p.close()
 b.close()
