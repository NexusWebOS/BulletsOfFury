from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
from io import BytesIO
import base64,json,http.server,math
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinematic_finish_1020';errors=[];frames=[];checks=[]
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/docs/BOSS_REDESIGN_1020.md')
  p.evaluate("()=>{document.body.innerHTML='<video id=film preload=auto></video>';document.querySelector('video').src='/_shots/cinematic_finish_1020/ending-native.webm';}")
  p.wait_for_function("document.querySelector('video').readyState>=2",timeout=60000);duration=p.evaluate("document.querySelector('video').duration");checks.append(dict(name='Recorded ending has finite seekable duration beyond the final-card entry',passed=math.isfinite(duration) and duration>=65,data=duration if math.isfinite(duration) else 'nonfinite'))
  for t in [1.5,11.5,28,34,39,46,51,57.5,65]:
   p.evaluate("t=>{const v=document.querySelector('video');v.currentTime=t;}",t);p.wait_for_function("!document.querySelector('video').seeking");data=p.evaluate("()=>{const v=document.querySelector('video'),c=document.createElement('canvas');c.width=v.videoWidth;c.height=v.videoHeight;c.getContext('2d').drawImage(v,0,0);return c.toDataURL().split(',')[1];}");im=Image.open(BytesIO(base64.b64decode(data))).convert('RGB');im.save(O/f'film-{str(t).replace(".","_")}.png');frames.append((t,im));checks.append(dict(name='Movie frame '+str(t)+' has real rendered content',passed=sum(max(px)>30 for px in im.getdata())>1000))
  b.close()
finally:stop()
sheet=Image.new('RGB',(1152,720),'#101522');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(frames):im.thumbnail((384,216));sheet.paste(im,(i%3*384,i//3*240));d.text((i%3*384+8,i//3*240+216),str(t)+'s / recorded native canvas',fill='white')
sheet.save(O/'recorded-film-contact-sheet.jpg',quality=90)
checks.append(dict(name='No video decode/browser errors',passed=not errors,data=errors));report=dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors,results=checks);(O/'film-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(not all(q['passed'] for q in checks))
