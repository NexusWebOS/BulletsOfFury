from pathlib import Path
import ast,sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/stage3_cinematics_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
tree=ast.parse((ROOT/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text())
RECORD=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RECORD' for t in n.targets))
RECORD=RECORD.replace("state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'')","state+':'+(BOFCinematicDirector.current?.id||'')+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||drawLaunch._phase||'')")
RECORD=RECORD.replace("part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0","part==='arrival'?state===GS.PLAY&&stateT>.8:window.__stage3SceneDone===true")
RECORD=RECORD.replace('last:FURY14.last','last:D1110.last')
report={'pilot':'cole','difficulty':'normal','source':str(ROOT),'scope':'Native cinematic checkpoint recordings, not campaign playthroughs. No dialogue skipped and no game source edited.','clips':[],'errors':[]}
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for part in (sys.argv[1:] or ['lead-in','arrival','hq']):
  errors=[];p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(240000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?stage3-cinema-record=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;diffKey='normal';Input.clearTaps();Input.mouse.down=false;window.__stage3SceneDone=false;}")
  if part=='arrival':
   p.evaluate('()=>{beginStage(3);warmStage(3);}')
   p.wait_for_function('()=>{stageLoadTick();ls112Warm(3);return stageLoadInfo(3).ready&&ls112Keys(3).every(k=>XART.rdy(k));}',polling=50)
   p.evaluate("()=>{BOFCinematicDirector.cancel();story=null;setState(GS.INTRO);resetIntro();drawLaunch._phase=undefined;player.invuln=99999;Input.clearTaps();Input.mouse.down=false;last=performance.now();}")
   expected=[]
  else:
   stage=2 if part=='lead-in' else 3
   p.evaluate("n=>{run.stage=n;curStage=STAGES[n-1];BOFCinematicDirector.start(n,()=>{window.__stage3SceneDone=true;setState(GS.TITLE);});}",stage)
   p.wait_for_function('()=>{const s=BOFCinematicDirector.current;return s&&d1110Ready(s.d1110Keys||s.s113Keys||[]);}',polling=50)
   expected=p.evaluate('BOFCinematicDirector.current.beats.map(b=>({id:b.id,who:b.who,text:b.text,duration:b.duration,c16:!!b.c16}))')
   p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
  print('RECORDING '+part+'; authored seconds '+str(round(sum(q['duration'] for q in expected),2)),flush=True)
  r=p.evaluate(RECORD,part);(OUT/(part+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));r.update({'part':part,'expectedBeats':expected,'errors':errors,'end':p.evaluate('({state,stage:run.stage,sceneDone:window.__stage3SceneDone})')})
  report['clips'].append(r);report['errors']+=errors;(OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
  print(json.dumps({'part':part,'seconds':r['seconds'],'peak':r['peak'],'end':r['end'],'errors':errors}),flush=True)
  p.close()
  assert not errors and r['peak']>.001
  assert r['end']['state']=='play' if part=='arrival' else r['end']['sceneDone']
 b.close()
