"""Inspect the served review, real video decode, cue buttons, and page/console errors."""
import json,http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/hammer_time_ship_0927');errors=[]
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport={'width':1440,'height':1080});p.set_default_timeout(60000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/hammer_time_ship_0927/review.html');p.wait_for_function('()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
  p.wait_for_function("()=>document.querySelector('video').readyState>=2")
  p.screenshot(path=str(OUT/'review.png'),full_page=True)
  p.get_by_role('button',name='Dance break',exact=True).click();p.wait_for_function("()=>document.querySelector('video').currentTime>15&&!document.querySelector('video').paused");p.wait_for_timeout(500)
  r=p.evaluate("()=>{const v=document.querySelector('video');return {images:[...document.images].length,duration:v.duration,playing:!v.paused,time:v.currentTime,videoError:v.error&&v.error.message};}")
  r['errors']=errors;br.close()
finally:stop()
(OUT/'review-check.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r,indent=2))
assert not errors and not r['videoError'] and r['duration']>=35.5 and r['playing'] and r['time']>15
