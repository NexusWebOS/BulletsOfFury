import json
from pathlib import Path
from playwright.sync_api import sync_playwright
errors=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 response=p.goto('http://127.0.0.1:8794/_shots/toxic_modular_0927/review.html',wait_until='load')
 p.evaluate("async()=>{await Promise.all([...document.querySelectorAll('video')].map(v=>new Promise((resolve,reject)=>{v.preload='auto';v.onloadeddata=resolve;v.onerror=()=>reject(Error(v.currentSrc));v.load()})))}")
 result={'status':response.status,'videos':p.evaluate("()=>[...document.querySelectorAll('video')].map(v=>({src:v.getAttribute('src'),width:v.videoWidth,height:v.videoHeight,ready:v.readyState}))"),'images':p.evaluate("()=>[...document.images].map(i=>({src:i.getAttribute('src'),ready:i.complete&&i.naturalWidth>0}))"),'errors':errors}
 p.screenshot(path='_shots/toxic_modular_0927/review_verified.png',full_page=True);b.close()
Path('_shots/toxic_modular_0927/review_check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not errors and result['status']==200
assert all(x['width']>0 and x['ready']>=2 for x in result['videos'])
assert all(x['ready'] for x in result['images'])
