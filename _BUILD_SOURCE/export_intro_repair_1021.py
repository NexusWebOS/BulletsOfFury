"""Export current native cinematic identities with even transparent padding."""
from pathlib import Path
import sys,base64,json,hashlib,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
D=R/'_ART_SOURCES/intro_repair_1021/references';D.mkdir(parents=True,exist_ok=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));records=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(120000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready');p.evaluate(shoot.TRAP_RAF)
  keys=['cin_federation_station_1','cin_origin_radio','cin_origin_tower','cin_origin_hq_iso','cin_pilot_lizzie_open','cin_pilot_decker_open','ship_yuri','ship_decker','ship_lizzie','nbl_logo_0916']
  dr=p.evaluate('typeof DP20!=="undefined"?DP20.key:null')
  if dr:keys.append(dr)
  for key in keys:
   p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50)
   q=p.evaluate("k=>{const im=XART.get(k),w=im.width+(im.width%2),h=im.height+(im.height%2);cv.width=w;cv.height=h;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,w,h);ctx.drawImage(im,0,0);return {w,h,source:[im.width,im.height],data:cv.toDataURL().split(',')[1]};}",key)
   path=D/(key+'.png');path.write_bytes(base64.b64decode(q.pop('data')));records.append(dict(key=key,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**q));print(key,q,flush=True)
  b.close()
finally:stop()
(D/'manifest.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
