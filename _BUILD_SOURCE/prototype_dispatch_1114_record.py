from pathlib import Path
import ast,sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/prototype_dispatch_1114';FILMS=OUT/'films';FILMS.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
tree=ast.parse((ROOT/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text(encoding='utf-8'))
RECORD=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='RECORD'for t in n.targets))
RECORD=RECORD.replace("state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'')","state+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||'')+':'+(KD17.last?.mode||CW16.last?.mode||SL14.last?.mode||'')+':'+(drawLaunch._furyIntro?.phase||drawLaunch._phase||'')+':'+(typeof gravityMode!=='undefined'?gravityMode?.phase||'':'')")
RECORD=RECORD.replace("part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0","part.startsWith('arrival')?state===GS.PLAY&&stateT>.8:part==='escape'?__done&&state===GS.STAGESEL&&SL14.mapFade===0&&stateT>1.4:__done")
RECORD=RECORD.replace('(now-start)>170000','(now-start)>400000').replace('last:FURY14.last','last:{cinema:D1110.last,custom:KD17.last,service:SL14.last,fury:drawLaunch._furyIntro}')
report={'pilot':'cole','difficulty':'normal','source':str(ROOT),'scope':'Complete native cinematic checkpoints, no dialogue skips; gameplay between scenes omitted. Not campaign playthroughs.','clips':[],'errors':[]}
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for part in (sys.argv[1:]or ['post4','arrival5']):
  errors=[];p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(480000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?cinematic-rework-record=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;diffKey='normal';Input.clearTaps();Input.mouse.down=false;window.__done=false;window.__returns=0;}")
  n={'escape':2,'arrival3':3,'hq3':3,'post4':4,'arrival5':5}[part]
  if part in ['escape','arrival3','arrival5']:
   p.evaluate('n=>{beginStage(n);warmStage(n);}',n)
   p.wait_for_function('n=>{stageLoadTick();ls112Warm(n);return stageLoadInfo(n).ready&&ls112Keys(n).every(k=>XART.rdy(k));}',arg=n,polling=50)
  if part=='escape':
   p.evaluate("()=>{bossActive=subBossActive=false;mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;campaign.rank={1:'A',2:'A'};campaign.unlockedMax=3;BOFCinematicDirector.start(2,()=>{__returns++;__done=true;openStageSelect(3,{});});}")
  elif part.startswith('arrival'):
   p.evaluate("()=>{BOFCinematicDirector.cancel();story=null;setState(GS.INTRO);resetIntro();drawLaunch._phase=undefined;}")
  else:
   p.evaluate("n=>{run.stage=n;curStage=STAGES[n-1];BOFCinematicDirector.start(n,()=>{__returns++;__done=true;setState(GS.TITLE);});}",n)
  expected=[]
  if not part.startswith('arrival'):
   p.wait_for_function('()=>{const s=BOFCinematicDirector.current;return s&&d1110Ready(s.d1110Keys||[]);}',polling=50)
   expected=p.evaluate('BOFCinematicDirector.current.beats.map(b=>({id:b.id,who:b.who,text:b.text,duration:b.duration,panel:b.panel,mode:b.kit17||b.cw16||b.service14}))')
  p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
  print('RECORDING '+part+'; '+str(round(sum(q['duration']for q in expected),2))+' authored seconds',flush=True)
  r=p.evaluate(RECORD,part);(FILMS/(part+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));r.update({'part':part,'expectedBeats':expected,'errors':errors,'end':p.evaluate('({state,stage:run.stage,done:__done,returns:__returns,gravityReady:run.gravityShipReady})')})
  report['clips'].append(r);report['errors']+=errors;(OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
  print(json.dumps({'part':part,'seconds':r['seconds'],'peak':r['peak'],'end':r['end'],'errors':errors}),flush=True);p.close()
  assert not errors and r['peak']>.001
  assert r['end']['state']=='play'if part.startswith('arrival')else r['end']['done']and r['end']['returns']==1
  assert all(any(':'+q['id']+':'in e['tag']for e in r['stages'])for q in expected)
 b.close()
print('Both revised Stage4-to-5 native cinematic checkpoints recorded.',flush=True)
