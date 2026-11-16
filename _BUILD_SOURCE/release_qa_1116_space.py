from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/space';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?release-space=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate(shoot.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':False});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}',polling=50)
 for pk in p.evaluate('PILOTS.map(p=>p.key)'):
  for space in range(3):
   for lv in range(1,6):
    q=p.evaluate("""q=>{window.P16=forgePreviewNew(0,null,q.lv);P16.pilot=q.pk;P16.space=q.space;const before=JSON.stringify({pilot:run.pilot,stage:run.stage,weapon:run.weapon,space:run.spaceMode,levels:run.spaceLevels});let peak=0;const kinds=new Set();for(let i=0;i<150;i++){forgePreviewTick(P16,400,440,1/60);peak=Math.max(peak,P16.bullets.length+P16.parts.length+P16.bursts.length);for(const b of P16.bullets)kinds.add(b.kind);}forgePreviewDraw(P16,40,20,VW-80,VH-40);return{peak,kinds:[...kinds],error:P16.err,fired:P16.fired,isolated:before===JSON.stringify({pilot:run.pilot,stage:run.stage,weapon:run.weapon,space:run.spaceMode,levels:run.spaceLevels})};}""",{'pk':pk,'space':space,'lv':lv})
    rows.append({'pilot':pk,'space':space,'level':lv,**q});p.wait_for_timeout(1)
    if pk=='cole':p.locator('#screen').screenshot(path=str(O/f'space{space}-level{lv}.jpg'),type='jpeg',quality=87)
  print(pk+' space tiers checked',flush=True)
 b.close()
bad=[r for r in rows if r['error']or not r['peak']or not r['isolated']]
(O/'report.json').write_text(json.dumps({'rows':rows,'bad':bad,'errors':errors,'scope':'All9 pilots,5 tiers of native Laser/Fusion and auto-volley previews. Production emitter/render/state-isolation smoke, not full combat damage or every co-op/stage interaction.'},indent=2),encoding='utf8');print(json.dumps({'cases':len(rows),'bad':bad,'errors':errors}),flush=True)
