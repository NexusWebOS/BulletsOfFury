from pathlib import Path
import ast,sys,json,base64,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/hq_return_attack_1114';FILMS=OUT/'films';FILMS.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
source=(ROOT/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text(encoding='utf8');tree=ast.parse(source)
RECORD=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='RECORD'for t in n.targets))
RECORD=RECORD.replace("let peak=0,frame=0,stages=[],prior='',start=", "let peak=0,frame=0,stages=[],samples=[],sampled=new Set(),prior='',tagAt=0,start=")
RECORD=RECORD.replace("state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'')", "state+':'+(H3.ending?.hf17?.phase||'')+':'+(H3.ending?.phase||'')+':'+(H3.ending?.hf17?.line??'')+':'+(H3.ending?.cheer??'')+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||'')+':'+(s6Opening?.phase||drawLaunch._phase||'')+':'+(s6Opening?.radioIndex??'')+':'+(HQ19.last?.mode||'')+':'+(HQ19.last?.phase||'')")
RECORD=RECORD.replace("prior=tag;}", "prior=tag;tagAt=now;}if(now-tagAt>.65*1000&&!sampled.has(tag)){sampled.add(tag);samples.push({tag,at:(now-start)/1000,image:cv.toDataURL('image/png')});}")
RECORD=RECORD.replace("if(part==='stage1'&&state===GS.STAGESEL&&stateT>1.5&&!mapConfirm){mapConfirm=true;Input.injectTap('enter');}", "")
RECORD=RECORD.replace("part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0", "part==='chronos'?state===GS.STAGECLEAR&&stateT>1.7:state===GS.PLAY&&((s6Opening&&s6Opening.radioIndex>=5&&!['cloak','reveal','lock'].includes(s6Opening.phase)&&s6Opening.t>.75)||(!s6Opening&&run._mission29OpeningDone))")
RECORD=RECORD.replace('(now-start)>170000','(now-start)>360000').replace('peak,stages,last:FURY14.last','peak,stages,samples,last:{ending:H3.ending?.phase,hf:HF17.last,earth:HF17.earth,cinema:D1110.last,opening:s6Opening?.phase,openingRadioIndex:s6Opening?.radioIndex}')
report={'pilot':'cole','difficulty':'hard','source':str(ROOT),'scope':'Full revised native cinematic checkpoints: real Chronos destruction, delayed Earth approach, physical landing/walk/crew welcome/radar/evacuation/base invasion continuously into the native Stage6 opening through first interactive interception. Gameplay and optional equipment/result menus between checkpoints omitted. Not a campaign win.','clips':[],'errors':[],'coreBefore':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in ['assets/game.js','_BUILD_SOURCE/test_fl.js','index.html']}}
if sys.argv[1:] and (OUT/'recording.json').exists():
 report=json.loads((OUT/'recording.json').read_text(encoding='utf8'))
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for part in (sys.argv[1:]or ['chronos','hq5']):
  errors=[];p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(480000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?stage56-record=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;diffKey='hard';DIFF=difficultyForRun('campaign','hard');campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A'};campaign.unlockedMax=6;Input.clearTaps();Input.mouse.down=false;window.__done=false;window.__returns=0;}")
  expected=[]
  if part=='chronos':
   p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
   p.evaluate("()=>{BAL7.setup({stage:5,kind:'chromehammer',pilot:'cole',diff:'hard',mode:'campaign',fire:false});run.gravityShipReady=true;hf17Warm();}")
   p.wait_for_function("()=>{stageLoadTick();furyShipLoadTick();h3Warm();return stageLoadInfo(5).ready&&hf17Warm()&&furyShipReady()&&XART.rdy('fb1002_hammer_portrait');}",polling=50)
   p.evaluate("()=>{B.hp=0;bossDie();if(!H3.ending?.hf17)throw Error('Native Chronos finale did not start');}")
  elif part=='hq5':
   p.evaluate("()=>{run.stage=5;curStage=STAGES[4];run.gravityShipReady=true;BOFCinematicDirector.start(5);}")
   p.wait_for_function('()=>{const s=BOFCinematicDirector.current;return s&&d1110Ready(s.d1110Keys||[]);}',polling=50)
   expected=p.evaluate('BOFCinematicDirector.current.beats.map(b=>({id:b.id,who:b.who,text:b.text,duration:b.duration,kind:b.kind,upgrade:b.upgrade}))')
  else:
   p.evaluate('()=>{beginStage(6);warmStage(6);}')
   p.wait_for_function('()=>{stageLoadTick();ls112Warm(6);return stageLoadInfo(6).ready&&ls112Keys(6).every(k=>XART.rdy(k));}',polling=50)
   p.evaluate("()=>{BOFCinematicDirector.cancel();story=null;setState(GS.INTRO);resetIntro();drawLaunch._phase=undefined;}")
  p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
  print('RECORDING '+part+' '+str(round(sum(q['duration']for q in expected),2))+' authored seconds',flush=True)
  r=p.evaluate(RECORD,part);(FILMS/(part+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));shots=[]
  for i,s in enumerate(r.pop('samples')):
   f=part+'-sample-%02d.png'%i;(OUT/f).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({**s,'file':f})
  r.update({'part':part,'expectedBeats':expected,'errors':errors,'shots':shots,'end':p.evaluate('({state,stage:run.stage,done:__done,returns:__returns,gravityReady:run.gravityShipReady,opening:s6Opening?.phase,openingRadioIndex:s6Opening?.radioIndex})'),'finaleEvents':p.evaluate('HF17.events')if part=='chronos'else[]})
  report['clips']=[v for v in report['clips']if v['part']!=part]+[r];report['clips'].sort(key=lambda v:['chronos','hq5'].index(v['part']));report['errors']+=errors;(OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8')
  print(json.dumps({'part':part,'seconds':r['seconds'],'peak':r['peak'],'end':r['end'],'errors':errors}),flush=True);p.close()
  assert not errors and r['peak']>.001
  if part=='chronos':assert r['end']['state']=='stageclear' and all(any(':'+ph+':'in (s['tag']+':')for s in r['stages'])for ph in ['drain','pulse','lock','missile','engulf','burst','after','space-departure','earth-reveal','earth-descent'])
  elif part=='hq5':assert r['end']['state']=='play'and r['end']['stage']==6 and r['end'].get('openingRadioIndex',0)>=5 and all(any(':'+q['id']+':'in s['tag']for s in r['stages'])for q in expected)
  else:assert r['end']['state']=='play'and r['end'].get('openingRadioIndex',0)>=5
 b.close()
report['coreAfter']={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()for n in report['coreBefore']};assert report['coreBefore']==report['coreAfter'];(OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('Full revised native HQ evacuation and Stage6 handoff recorded without skipping cinematic beats.',flush=True)
