from pathlib import Path
from playwright.sync_api import sync_playwright
import json,http.server,time,subprocess,shutil
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinematic_finish_1020';checks=[];errors=[]
def ck(n,ok,data=None):checks.append(dict(name=n,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=1000),accept_downloads=True);p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/cinematic_finish_1020/index.html');p.wait_for_function('ready===true');p.screenshot(path=str(O/'review-desktop.png'))
  p.locator('[data-time="26.5"]').click();p.locator('[data-time="32"]').click();g=p.frames[1]
  ck('Scene controls call the actual game ending renderer',g.evaluate('CE20.last.scene==="pilot"'))
  p.locator('#pilot').select_option('falva');p.wait_for_function('ready===true');p.locator('[data-time="32"]').click();ck('Pilot selector changes the actual epilogue and source body',g.evaluate('CE20.last.pilot==="falva"'))
  p.locator('#coop').check();p.wait_for_function('ready===true');p.locator('[data-time="9.4"]').click();ck('Co-op preview shows the actual second aircraft',g.evaluate('CE20.partnerShip.pilot==="yuri"'))
  p.locator('#pilot').select_option('cole');p.locator('#coop').uncheck();p.wait_for_function('ready===true');p.locator('[data-time="32"]').click()
  p.set_viewport_size(dict(width=390,height=844));p.screenshot(path=str(O/'review-narrow.png'));ck('Narrow review has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  p.set_viewport_size(dict(width=1280,height=1000));p.locator('#restart').click();p.wait_for_function('ready===true');
  # Record the real cinematic canvas at actual playback speed. Video is silent;
  # interactive playback uses the approved native audio mixer.
  g.evaluate('''()=>{window.recordChunks20=[];window.record20=new MediaRecorder(cv.captureStream(30),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:3500000});record20.ondataavailable=e=>{if(e.data.size)recordChunks20.push(e.data);};record20.start(1000);}''')
  p.locator('#play').click();ck('Play advances the native homecoming clock',g.evaluate('drawVictory._t<2'))
  # Yield frequently so the caller can communicate while the complete film plays.
  p.wait_for_function('Number(document.querySelector("#seek").value)>=66',timeout=110000)
  p.locator('#play').click();ck('Real-time ending reaches its final card',g.evaluate('CE20.last.scene==="final-card"&&drawVictory._t>=66'))
  g.evaluate('''()=>new Promise(resolve=>{record20.onstop=()=>{const blob=new Blob(recordChunks20,{type:'video/webm'});window.recordUrl20=URL.createObjectURL(blob);resolve();};record20.stop();})''')
  with p.expect_download() as dl:g.evaluate("()=>{const a=document.createElement('a');a.href=recordUrl20;a.download='ending-native.webm';a.click();}")
  dl.value.save_as(O/'ending-native.webm')
  if shutil.which('ffmpeg'):
   shutil.copy2(O/'ending-native.webm',O/'ending-native-raw.webm');subprocess.run(['ffmpeg','-v','error','-y','-i',str(O/'ending-native-raw.webm'),'-c','copy',str(O/'ending-native.webm')],check=True)
  ck('Native movie contains a nonempty complete recording',(O/'ending-native.webm').stat().st_size>100000)
  ck('Review has no browser errors',not errors,errors);b.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors,results=checks);(O/'review-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));raise SystemExit(not all(q['passed'] for q in checks))
