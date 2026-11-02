"""Native interactive catalogue uses the new V31 actor from its first draw."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
W=R/'_shots/stage2_amplify_1031';checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1440,'height':980});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/enemy-atlas.html#bof-enemy-disc',wait_until='load',timeout=180000)
  p.wait_for_function('()=>document.querySelector("#engine")?.contentWindow?.BOF_ENEMY_ATLAS?.snapshot().actor?.type==="disc"',timeout=180000);p.wait_for_timeout(1500)
  q=p.evaluate('()=>{const w=document.querySelector("#engine").contentWindow;return{snapshot:w.BOF_ENEMY_ATLAS.snapshot(),spawn:w.BOF_VOLCANIC_REFIT.state.events.find(e=>e.event==="spawn"),title:document.querySelector("#name").textContent,native:w.eval("({stage:run.stage,enemies:enemies.map(e=>({type:e.type,model:e._v31?.model})),V31events:V31.events})")}}')
  (W/'atlas-live.json').write_text(json.dumps(q,indent=2));print(q,flush=True)
  checks.append({'name':'Native interactive field guide launches actual Magma Disc owner','passed':q.get('spawn')is not None and q['spawn']['model']=='disc'and q['title']=='Magma Disc'and not q['snapshot']['error'],'data':q})
  p.wait_for_function('()=>document.querySelector("#engine").contentWindow.BOF_ENEMY_ATLAS.snapshot().activeBeams===9',timeout=15000)
  live=p.evaluate('()=>{const api=document.querySelector("#engine").contentWindow.BOF_ENEMY_ATLAS;return{phase:api.snapshot().actor.phase,beams:api.snapshot().activeBeams,legacy:api.patterns}}');checks.append({'name':'Native catalogue displays all9 beams and current phase without legacy attack buttons','passed':live['phase']=='fire'and live['beams']==9 and not live['legacy'],'data':live});p.screenshot(path=str(W/'native-atlas-disc.png'));b.close()
finally:stop();checks.append({'name':'No interactive catalogue page/console errors','passed':not errors,'data':errors});(W/'atlas-checks.json').write_text(json.dumps(checks,indent=2))
for q in checks:print('PASS'if q['passed']else'FAIL',q['name'],flush=True)
assert all(q['passed']for q in checks)
