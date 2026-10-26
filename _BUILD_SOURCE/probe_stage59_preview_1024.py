from pathlib import Path
import json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage59_1024';errors=[];checks=[];port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/docs/previews/stage59_repair_1024/index.html');p.wait_for_function('!document.querySelector("#replay").disabled');g=p.frames[1]
  for scene in ['bomber','last','fleet','horizon','warp']:
   p.select_option('#scene',scene);p.wait_for_function('!document.querySelector("#replay").disabled');status=p.inner_text('#status');ok=status.startswith('Live native encounter') and g.evaluate('DBGT.god');checks.append(dict(name=scene,passed=bool(ok),status=status));print(('PASS 'if ok else'FAIL ')+scene,flush=True)
  b.close()
finally:stop()
checks.append(dict(name='No page errors',passed=not errors,data=errors));out=dict(passed=sum(x['passed']for x in checks),failed=sum(not x['passed']for x in checks),checks=checks);(O/'preview-report.json').write_text(json.dumps(out,indent=2)+'\n');print('SUMMARY',out['passed'],out['failed']);raise SystemExit(bool(out['failed']))
