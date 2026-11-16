from pathlib import Path
import ast,sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/cockpit_talk_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
tree=ast.parse((ROOT/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text(encoding='utf-8'))
RECORD=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RECORD' for t in n.targets))
TAG="state+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||'')+':'+(CP15.last?.pilot||'')+':'+(CP15.last?.frame??'')"
RECORD=RECORD.replace("state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'')",TAG).replace('last:FURY14.last','last:CP15.last')
END="part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0"
SERVICE=RECORD.replace(END,'state===GS.STAGESEL&&SL14.mapFade===0&&stateT>1.4')
MONTAGE=RECORD.replace(END,'(now-start)>4600')
errors=[];clips=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?cockpit-talk-record=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');coopOn=false;beginStage(2);warmStage(2);}")
 p.wait_for_function('()=>{stageLoadTick();ls112Warm(2);return stageLoadInfo(2).ready&&ls112Keys(2).every(k=>XART.rdy(k));}',polling=50)
 p.evaluate("()=>{bossActive=subBossActive=false;mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;campaign.rank={1:'A',2:'A'};campaign.unlockedMax=3;window.serviceReturnCount=0;BOFCinematicDirector.start(2,()=>{serviceReturnCount++;openStageSelect(3,{});});}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 expected=p.evaluate('BOFCinematicDirector.current.beats.map(b=>({id:b.id,who:b.who,text:b.text,duration:b.duration}))')
 p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
 print('Recording complete native service data-link scene',flush=True)
 r=p.evaluate(SERVICE,'service2');(OUT/'cole-service-datalink.webm').write_bytes(base64.b64decode(r.pop('video').split(',')[1]));r.update({'clip':'cole-service-datalink','expected':expected,'end':p.evaluate('({state,returns:serviceReturnCount})')});clips.append(r)
 assert r['end']=={'state':'stagesel','returns':1}
 assert all(any(q['id'] in e['tag'] for e in r['stages']) for q in expected)
 for pk in p.evaluate('CP15_ART.pilots'):
  p.evaluate("p=>FURY14.preview('stage1',p)",pk)
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
  p.evaluate('()=>{const s=BOFCinematicDirector.current;s.i=3;s.t=0;s.shown=0;Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
  print('Recording '+pk+' native jungle comic checkpoint',flush=True)
  r=p.evaluate(MONTAGE,pk);(OUT/(pk+'-talk.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));r['clip']=pk;clips.append(r)
  (OUT/'recording.json').write_text(json.dumps({'clips':clips,'errors':errors,'scope':'Complete native post-Stage-2 scene plus nine Stage1 dialogue checkpoints. Not a campaign playthrough.'},indent=2),encoding='utf-8')
 b.close()
assert not errors,errors
assert all(q['peak']>.001 for q in clips)
print('Recorded '+str(len(clips))+' audible native clips without browser errors.',flush=True)
