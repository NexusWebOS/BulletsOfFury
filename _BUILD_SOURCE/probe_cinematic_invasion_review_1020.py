from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import sys,json,http.server,subprocess,shutil,time
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/cinematic_invasion_1020';checks=[];errors=[]
def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=1000),accept_downloads=True);p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300]) if m.type=='error' else None);p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.goto(f'http://127.0.0.1:{port}/docs/previews/cinematic_invasion_1020/index.html');p.wait_for_function('ready===true');g=p.frames[1]
  p.locator('[data-time="45"]').click();ck('Federation scene button reaches actual invasion story',g.evaluate('INV20.last.scene==="federation"'))
  p.locator('#pilot').select_option('falva');p.wait_for_function('ready===true');p.locator('[data-time="27"]').click();ck('Selector uses Falva actual new pose',g.evaluate('INV20.last.pilot==="falva"&&INV20.last.cast[0].key==="inv20_falva"'))
  p.locator('#coop').check();p.wait_for_function('ready===true');p.locator('[data-time="27"]').click();ck('Co-op reports with both selected pilot identities',g.evaluate('INV20.last.cast.length===2&&INV20.last.partner==="yuri"'))
  p.set_viewport_size(dict(width=390,height=844));p.wait_for_timeout(400);p.screenshot(path=str(O/'review-narrow.png'));ck('Narrow review has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'));ck('Paused resize repaints the native game canvas',g.evaluate('ctx.getImageData(0,0,cv.width,cv.height).data.some(v=>v>20)'))
  p.set_viewport_size(dict(width=1280,height=1000));p.locator('#pilot').select_option('cole');p.locator('#coop').uncheck();p.wait_for_function('ready===true');p.locator('#restart').click();p.wait_for_function('ready===true');p.screenshot(path=str(O/'review-desktop.png'))
  g.evaluate('''()=>{window.invChunks=[];window.invRecorder=new MediaRecorder(cv.captureStream(30),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:2200000});invRecorder.ondataavailable=e=>{if(e.data.size)invChunks.push(e.data);};invRecorder.start(1000);}''')
  p.locator('#play').click();last=0
  while True:
   p.wait_for_timeout(1000);t=g.evaluate('drawVictory._t')
   if int(t)//10>last:print('Native playback '+str(round(t,1))+'s',flush=True);last=int(t)//10
   if t>=151:break
  p.locator('#play').click();before=g.evaluate('drawVictory._t');p.wait_for_timeout(350);ck('Pause stops actual cinematic clock',g.evaluate('drawVictory._t')==before)
  ck('Uninterrupted native playback reaches final score',g.evaluate('INV20.last.scene==="card"&&drawVictory._t>=151'))
  ck('Alarm, Federation, scream and portal each request their cues naturally',g.evaluate("['alarm','federation-0','scream','escape'].every(k=>INV20.events.some(e=>e.id===k&&e.played))"),g.evaluate('INV20.events'))
  g.evaluate('''()=>new Promise(resolve=>{invRecorder.onstop=()=>{window.invMovie=URL.createObjectURL(new Blob(invChunks,{type:'video/webm'}));resolve();};invRecorder.stop();})''')
  with p.expect_download() as dl:g.evaluate("()=>{const a=document.createElement('a');a.href=invMovie;a.download='invasion-ending-native.webm';a.click();}")
  dl.value.save_as(O/'invasion-ending-native-raw.webm');subprocess.run(['ffmpeg','-v','error','-y','-i',str(O/'invasion-ending-native-raw.webm'),'-c','copy',str(O/'invasion-ending-native.webm')],check=True)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(O/'invasion-ending-native.webm')],text=True).strip());ck('Recorded native film has a finite full ending duration',duration>150,duration)
  ck('Review playback has no browser errors',not errors,errors);b.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),checks=len(checks),errors=errors,results=checks);(O/'review-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));raise SystemExit(not all(c['passed'] for c in checks))
