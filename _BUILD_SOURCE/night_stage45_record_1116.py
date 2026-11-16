from pathlib import Path
from playwright.sync_api import sync_playwright
import ast,sys,json,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/stage45-current';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
tree=ast.parse((R/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text(encoding='utf8'));RECORD=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='RECORD'for t in n.targets))
RECORD=RECORD.replace("state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'')","state+':'+(BOFCinematicDirector.current?.id||'')+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||drawLaunch._phase||'')+':'+(gravityMode?.phase||'')")
RECORD=RECORD.replace("part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0","part==='assembly'?state===GS.PLAY&&run.stage===5&&stateT>.8:window.__done===true")
RECORD=RECORD.replace('(now-start)>170000','(now-start)>360000').replace('last:FURY14.last','last:{cinema:D1110.last,kit:KD18.last,gravity:gravityMode?.phase}')
report={'pilot':'cole','difficulty':'hard','scope':'Prepared native post4 and Stage5 assembly checkpoints; native clocks and mixer audio. No earned clear. Result/equipment/map menus omitted between clips.','clips':[],'errors':[]}
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for part in ['post4','assembly']:
  errors=[];p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(480000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?night-stage45=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{BOFOnline.submitScore=()=>{};run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;diffKey='hard';DIFF=difficultyForRun('campaign','hard');campaign.rank={1:'A',2:'A',3:'A',4:'A'};campaign.unlockedMax=5;Input.clearTaps();Input.mouse.down=false;window.__done=false;window.__returns=0;}")
  expected=[]
  if part=='post4':
   p.evaluate("()=>{run.stage=4;curStage=STAGES[3];BOFCinematicDirector.start(4,()=>{__returns++;__done=true;setState(GS.TITLE);});}");p.wait_for_function('()=>{const s=BOFCinematicDirector.current;return s&&d1110Ready(s.d1110Keys||[])}');expected=p.evaluate('BOFCinematicDirector.current.beats.map(b=>({id:b.id,who:b.who,text:b.text,duration:b.duration}))')
  else:
   p.evaluate("()=>{run.gravityShipReady=false;beginStage(5);warmStage(5);}");p.wait_for_function('()=>{stageLoadTick();furyShipLoadTick();return stageLoadReady(5)&&furyShipReady()}');p.evaluate("()=>{BOFCinematicDirector.cancel();story=null;setState(GS.LAUNCH);drawLaunch._phase=undefined;}")
  p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}');print('RECORDING '+part+' '+str(round(sum(q['duration']for q in expected),2)),flush=True)
  q=p.evaluate(RECORD,part);(O/(part+'.webm')).write_bytes(base64.b64decode(q.pop('video').split(',')[1]));q.update({'part':part,'expected':expected,'errors':errors,'end':p.evaluate('({state,stage:run.stage,returns:__returns,done:__done,ready:run.gravityShipReady})')});report['clips'].append(q);report['errors']+=errors;(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'part':part,'seconds':q['seconds'],'peak':q['peak'],'end':q['end'],'errors':errors}),flush=True);p.close();assert not errors and q['peak']>.001;assert q['end']['state']=='play'if part=='assembly'else q['end']['returns']==1
 b.close()
