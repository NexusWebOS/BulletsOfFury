from pathlib import Path
import ast,sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/service_link_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
tree=ast.parse((ROOT/'_BUILD_SOURCE/record_opening_fury_1114.py').read_text())
RECORD=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RECORD' for t in n.targets))
RECORD=RECORD.replace("state+':'+(FURY14.last?.kind||'')+':'+(FURY14.last?.shot||'')","state+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||'')+':'+(SL14.last?.mode||'')")
RECORD=RECORD.replace("part==='opening'?state===GS.STAGESEL&&FURY14.map?.done:state===GS.LAUNCH&&stateT>1.0","state===GS.STAGESEL&&SL14.mapFade===0&&stateT>1.4")
RECORD=RECORD.replace('last:FURY14.last','last:SL14.last')
errors=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?service-link-record=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');coopOn=false;beginStage(2);warmStage(2);}")
 p.wait_for_function('()=>{stageLoadTick();ls112Warm(2);return stageLoadInfo(2).ready&&ls112Keys(2).every(k=>XART.rdy(k));}',polling=50)
 p.evaluate("()=>{bossActive=subBossActive=false;mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;campaign.rank={1:'A',2:'A'};campaign.unlockedMax=3;window.serviceReturnCount=0;BOFCinematicDirector.start(2,()=>{serviceReturnCount++;openStageSelect(3,{});});}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 expected=p.evaluate('BOFCinematicDirector.current.beats.map(b=>({id:b.id,who:b.who,text:b.text,duration:b.duration}))')
 p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
 print('RECORDING '+str(sum(q['duration'] for q in expected))+' authored seconds',flush=True)
 r=p.evaluate(RECORD,'service2');(OUT/'service-datalink.webm').write_bytes(base64.b64decode(r.pop('video').split(',')[1]));r.update({'expected':expected,'errors':errors,'end':p.evaluate('({state,returns:serviceReturnCount})'),'scope':'Native post-Stage-2 scene checkpoint and map continuation, not a campaign clear.'});(OUT/'recording.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r,indent=2),flush=True);b.close()
assert not errors and r['peak']>.001 and r['end']=={'state':'stagesel','returns':1}
assert all(any(q['id'] in e['tag'] for e in r['stages']) for q in expected)
