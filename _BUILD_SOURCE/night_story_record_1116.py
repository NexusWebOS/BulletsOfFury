from pathlib import Path
import ast,sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/cinema_overnight_1116/stage3-current';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
tree=ast.parse((ROOT/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text(encoding='utf-8'))
RECORD=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='RECORD'for t in n.targets))
RECORD=RECORD.replace("state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'')","state+':'+(BOFCinematicDirector.current?.id||'')+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||drawLaunch._phase||'')+':'+(SL14.last?.mode||'')")
RECORD=RECORD.replace("part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0","part==='arrival'?state===GS.PLAY&&stateT>.8:part==='lead-in'?window.__sceneDone&&state===GS.STAGESEL&&SL14.mapFade===0&&stateT>1.4:window.__sceneDone===true")
RECORD=RECORD.replace('last:FURY14.last','last:{cinema:D1110.last,service:SL14.last,cockpit:CP15.last}')
RECORD=RECORD.replace('(now-start)>170000','(now-start)>360000')
report={'pilot':'cole','difficulty':'normal','source':str(ROOT),'scope':'Fresh native cinematic checkpoints: complete post-Stage-2 service data-link with lift-off/map handoff, Stage3 arrival, and post-Stage-3 HQ/prototypes. No dialogue skipped; not a campaign playthrough.','clips':[],'errors':[]}
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for part in ['lead-in','arrival','hq']:
  errors=[];p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(480000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?stage3-talking-record=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{BOFOnline.submitScore=()=>{};run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;diffKey='normal';Input.clearTaps();Input.mouse.down=false;window.__sceneDone=false;window.__returns=0;CP15.history=[];}")
  if part in ['lead-in','arrival']:
   n=2 if part=='lead-in'else 3
   p.evaluate('n=>{beginStage(n);warmStage(n);}',n)
   p.wait_for_function('n=>{stageLoadTick();ls112Warm(n);return stageLoadInfo(n).ready&&ls112Keys(n).every(k=>XART.rdy(k));}',arg=n,polling=50)
  if part=='lead-in':
   p.evaluate("()=>{bossActive=subBossActive=false;mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;campaign.rank={1:'A',2:'A'};campaign.unlockedMax=3;BOFCinematicDirector.start(2,()=>{__returns++;__sceneDone=true;openStageSelect(3,{});});}")
  elif part=='arrival':
   p.evaluate("()=>{BOFCinematicDirector.cancel();story=null;setState(GS.INTRO);resetIntro();drawLaunch._phase=undefined;}")
  else:
   p.evaluate("()=>{run.stage=3;curStage=STAGES[2];BOFCinematicDirector.start(3,()=>{__returns++;__sceneDone=true;setState(GS.TITLE);});}")
  if part!='arrival':
   p.wait_for_function('()=>{const s=BOFCinematicDirector.current;return s&&d1110Ready(s.d1110Keys||s.s113Keys||[]);}',polling=50)
   expected=p.evaluate('BOFCinematicDirector.current.beats.map(b=>({id:b.id,who:b.who,text:b.text,duration:b.duration,mode:b.service14}))')
  else:expected=[]
  p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
  print('RECORDING '+part+'; '+str(round(sum(q['duration']for q in expected),2))+' authored seconds',flush=True)
  r=p.evaluate(RECORD,part);(OUT/(part+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]))
  r.update({'part':part,'expectedBeats':expected,'errors':errors,'end':p.evaluate('({state,stage:run.stage,done:__sceneDone,returns:__returns,mapFade:SL14.mapFade})'),'cockpitFrames':p.evaluate('CP15.history'),'newCockpitAsset':p.evaluate('CP15_ART.banks.cole')})
  report['clips'].append(r);report['errors']+=errors;(OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
  print(json.dumps({'part':part,'seconds':r['seconds'],'frames':r['frames'],'peak':r['peak'],'end':r['end'],'errors':errors}),flush=True)
  p.close()
  assert not errors and r['peak']>.001
  assert r['end']['state']=='play'if part=='arrival'else r['end']['done']and r['end']['returns']==1
  assert all(any(':'+q['id']+':'in s['tag']for s in r['stages'])for q in expected)
  if part=='lead-in':
   assert len({q['frame']for q in r['cockpitFrames']if q['pilot']=='cole'})>=5
   assert all(any(':'+mode in s['tag']for s in r['stages'])for mode in ['heat','alert','takeoff','fade'])
 b.close()
print('All three fresh native cinematic clips recorded with no browser/asset errors.',flush=True)
