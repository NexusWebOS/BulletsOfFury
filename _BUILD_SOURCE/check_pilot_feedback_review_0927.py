"""Decode every review clip and inspect the review in native Chromium."""
from pathlib import Path
import json,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/pilot_feedback_0927');errors=[]
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1440,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/pilot_feedback_0927/review.html')
  p.wait_for_function("()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0)&&[...document.querySelectorAll('video')].every(v=>v.readyState>=1)")
  media=p.evaluate("""async()=>{const out=[];for(const v of document.querySelectorAll('video')){v.currentTime=1;await new Promise(r=>v.addEventListener('seeked',r,{once:true}));out.push({src:v.getAttribute('src'),duration:v.duration,width:v.videoWidth,height:v.videoHeight,error:v.error});}return out;}""")
  p.screenshot(path=str(OUT/'review-page.png'))
  p.locator('#idle').click();p.wait_for_function("()=>document.querySelector('#fleet').complete")
  idle=p.locator('#idle').get_attribute('aria-pressed')
  p.locator('#boost').click();p.wait_for_function("()=>document.querySelector('#fleet').complete")
  boost=p.locator('#boost').get_attribute('aria-pressed')
  status=p.request.get(f'http://127.0.0.1:{port}/index.html').status
  report={'media':media,'idleToggle':idle,'boostToggle':boost,'gameLinkStatus':status,'errors':errors}
  b.close()
finally:stop()
(OUT/'review-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert not errors and status==200 and idle==boost=='true'
assert len(media)==3 and all(m['width']>0 and m['height']>0 and m['duration']>7 and m['error'] is None for m in media)
