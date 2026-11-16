from pathlib import Path
import ast, sys, json, base64, hashlib
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source')
OUT=ROOT/'_shots/hq_swarm_1115'; FILMS=OUT/'films'
FILMS.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE')); import shoot
source=(ROOT/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text(encoding='utf8')
tree=ast.parse(source)
RECORD=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RECORD' for t in n.targets))
RECORD=RECORD.replace("let peak=0,frame=0,stages=[],prior='',start=", "let peak=0,frame=0,stages=[],samples=[],sampled=new Set(),prior='',tagAt=0,start=")
RECORD=RECORD.replace("state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'')", "state+':'+(BOFCinematicDirector.current?.id||'')+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||'')+':'+(s6Opening?.phase||drawLaunch._phase||'')+':'+(s6Opening?.radioIndex??'')+':'+(HQ19.last?.mode||'')")
RECORD=RECORD.replace("prior=tag;}", "prior=tag;tagAt=now;}if(now-tagAt>650&&!sampled.has(tag)){sampled.add(tag);samples.push({tag,at:(now-start)/1000,image:cv.toDataURL('image/png')});}")
RECORD=RECORD.replace("if(part==='stage1'&&state===GS.STAGESEL&&stateT>1.5&&!mapConfirm){mapConfirm=true;Input.injectTap('enter');}", "")
RECORD=RECORD.replace("part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0", "part==='hq5'?state===GS.PLAY&&s6Opening?.radioIndex>=5&&!['cloak','reveal','lock'].includes(s6Opening.phase)&&s6Opening.t>.75:state===GS.PLAY&&run.stage===7&&stateT>2.5&&!story")
RECORD=RECORD.replace('(now-start)>170000','(now-start)>180000').replace('peak,stages,last:FURY14.last','peak,stages,samples,last:{cinema:D1110.last,opening:s6Opening?.phase,openingRadioIndex:s6Opening?.radioIndex}')
core=['assets/game.js','_BUILD_SOURCE/test_fl.js','index.html','assets/hq_return_attack_1114.js','assets/hq_turn_art_1115.js','assets/hq_swarm_art_1115.js']
report={'pilot':'cole','difficulty':'hard','source':str(ROOT),'scope':'Native cinematic checkpoints, no dialogue skips. HQ recording starts at the evacuation, retaining the five-second quiet pause and ending after the native Stage6 opening. Stage6-7 recording follows the Harrier branch post-fight story and native Stage7 approach/card/launch; it connects the prepared cleared-stage checkpoint directly to Stage7 without results/map/gear-menu pauses. Neither recording is a campaign win.','clips':[],'errors':[],'coreBefore':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in core}}
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for part in sys.argv[1:]or ['hq5','stage67']:
  errors=[];p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(240000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?hq22-record='+part)
  p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;diffKey='hard';DIFF=difficultyForRun('campaign','hard');campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A',6:'A'};campaign.unlockedMax=7;Input.clearTaps();Input.mouse.down=false;window.post6Done=0;}")
  if part=='hq5':
   p.evaluate("()=>{run.stage=5;curStage=STAGES[4];run.gravityShipReady=true;BOFCinematicDirector.start(5);warmStage(6);}")
   p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
   p.evaluate("()=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.hq19==='launch');s.t=0;s.shown=0;s.age=0;}")
  else:
   p.evaluate("()=>{run.stage=6;curStage=STAGES[5];run.gravityShipReady=false;run.spaceMode=false;warmStage(7);ls112Warm(7);BOFCinematicDirector.start(6,()=>{post6Done++;Input.clearTaps();beginStage(7);});}")
   p.wait_for_function('()=>{const before=run.stage;try{run.stage=7;stageLoadTick();ls112Warm(7);}finally{run.stage=before;}return stageLoadInfo(7).ready&&ls112Keys(7).every(k=>XART.rdy(k))&&d1110Ready(BOFCinematicDirector.current.d1110Keys);}',polling=50)
  expected=p.evaluate('BOFCinematicDirector.current.beats.slice(BOFCinematicDirector.current.i).map(b=>({id:b.id,who:b.who,text:b.text,duration:b.duration}))')
  p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
  print('RECORDING '+part,flush=True)
  r=p.evaluate(RECORD,part)
  (FILMS/(part+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]))
  shots=[]
  for i,s in enumerate(r.pop('samples')):
   fn=part+'-sample-%02d.png'%i;(OUT/fn).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({**s,'file':fn})
  r.update({'part':part,'expectedBeats':expected,'errors':errors,'shots':shots,'end':p.evaluate('({state,stage:run.stage,post6Done,brief:run._sewerBriefed17,opening:s6Opening?.phase,openingRadioIndex:s6Opening?.radioIndex})'),'cues':p.evaluate("D1110.events.filter(e=>e.kind==='cue')")})
  report['clips'].append(r);report['errors']+=errors
  (OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8')
  print(json.dumps({'part':part,'seconds':r['seconds'],'peak':r['peak'],'end':r['end'],'errors':errors}),flush=True)
  assert not errors and r['peak']>.001
  assert all(any(':'+v['id']+':'in s['tag']for s in r['stages'])for v in expected)
  assert r['end']['state']=='play'and r['end']['stage']==(6 if part=='hq5'else 7)
  if part=='stage67':assert r['end']['post6Done']==1 and r['end']['brief']
  p.close()
 b.close()
report['coreAfter']={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in core}
assert report['coreBefore']==report['coreAfter']
(OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('Both native cinematic checkpoints recorded with game audio.',flush=True)
