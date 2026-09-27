"""Check the delivered review page and decode every attached recording."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927');errors=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 response=p.goto('http://127.0.0.1:8794/_shots/overnight_0927/review.html',wait_until='load')
 p.set_default_timeout(60000)
 media=p.evaluate("""async()=>{const out=[];for(const m of document.querySelectorAll('video,audio')){
  await new Promise((resolve,reject)=>{if(m.readyState>=2)return resolve();m.preload='auto';m.onloadeddata=resolve;m.onerror=()=>reject(Error(m.currentSrc));m.load()});
  out.push({type:m.tagName,src:m.getAttribute('src'),duration:m.duration,ready:m.readyState,width:m.videoWidth||null,height:m.videoHeight||null});
 }return out;}""")
 images=p.evaluate("()=>[...document.images].map(i=>({src:i.getAttribute('src'),ready:i.complete&&i.naturalWidth>0}))")
 links=p.evaluate("()=>[...document.querySelectorAll('nav a')].map(a=>({text:a.textContent,target:!!document.querySelector(a.getAttribute('href'))}))")
 p.screenshot(path=str(OUT/'review-top.png'))
 p.locator('#toxic-legged').scroll_into_view_if_needed();p.screenshot(path=str(OUT/'review-stage7.png'));b.close()
report={'status':response.status,'media':media,'images':images,'stageLinks':links,'errors':errors}
(OUT/'review_check.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert report['status']==200 and not errors
assert len(media)==43 and sum(q['type']=='VIDEO' for q in media)==29
assert all(q['duration']>0 and q['ready']>=2 for q in media)
assert all(q['ready'] for q in images) and len(links)==9 and all(q['target'] for q in links)
