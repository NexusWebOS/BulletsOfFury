"""Real Chromium playback/seeking and clickable finding checks for the final viewer."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage78_review_1025'
url=json.loads((O/'server.json').read_text())['url'];clips=json.loads((R/'docs/previews/stage78_review_1025/review.json').read_text())['clips'];errors=[];checks=[];ranges=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1440,'height':1050})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:ranges.append(r.status)if '.mp4'in r.url else None)
 p.goto(url,wait_until='load');p.wait_for_selector('[data-stage]')
 for c in clips:
  p.locator(f'[data-stage="{c["stage"]}"]').click();p.locator(f'[data-build="{c["build"]}"]').click();p.wait_for_function('()=>document.querySelector("video").readyState>=2',timeout=60000)
  samples=[]
  for at in (min(16,c['duration']*.12),c['duration']*.55,c['duration']-3):
   samples.append(p.evaluate("""async at=>{const v=document.querySelector('video');v.pause();await new Promise(r=>{v.addEventListener('seeked',r,{once:true});v.currentTime=at});await v.play();await new Promise(r=>setTimeout(r,400));v.pause();const c=document.createElement('canvas');c.width=32;c.height=20;const g=c.getContext('2d');g.drawImage(v,0,0,32,20);let hash=0;for(const n of g.getImageData(0,0,32,20).data)hash=(hash*31+n)>>>0;return{time:v.currentTime,requested:at,w:v.videoWidth,h:v.videoHeight,error:v.error?.code||0,hash,muted:v.muted};}""",at))
  before=p.evaluate('document.querySelector("video").currentTime');p.locator('#next').click();p.wait_for_function('t=>document.querySelector("video").currentTime>t+.02',arg=before);after=p.evaluate('document.querySelector("video").currentTime')
  result=dict(stage=c['stage'],build=c['build'],checks=dict(plays=all(q['time']>q['requested']+.15 for q in samples),pixelsChange=len({q['hash']for q in samples})>1,fullFrame=all(q['w']==1280 and q['h']==800 for q in samples),noMediaError=not any(q['error']for q in samples),unmuted=not any(q['muted']for q in samples),frameStep=abs(after-before-1/30)<.015),samples=samples)
  checks.append(result);print(json.dumps(result),flush=True)
 # A finding selected from revised footage must seek into the original take.
 p.locator('[data-stage="8"]').click();p.locator('[data-build="after"]').click();p.wait_for_function('document.querySelector("video").readyState>=2');p.locator('#findings button').filter(has_text='Arm destruction').click();p.wait_for_function('document.querySelector("video").currentTime>70&&document.querySelector("[data-build=before]").classList.contains("active")',timeout=30000)
 finding=dict(jumpsToOriginal=p.evaluate('document.querySelector("video").currentSrc.includes("furious_789_1025")'),time=p.evaluate('document.querySelector("video").currentTime'))
 p.screenshot(path=str(O/'review-before.png'));p.locator('[data-build="after"]').click();p.wait_for_function('document.querySelector("video").readyState>=2');p.screenshot(path=str(O/'review-after.png'));br.close()
result=dict(clips=checks,finding=finding,errors=errors,byteRangeResponses=ranges)
(O/'browser-playback.json').write_text(json.dumps(result,indent=2),encoding='utf8')
ok=all(all(c['checks'].values())for c in checks)and finding['jumpsToOriginal']and not errors and 206 in ranges
print(json.dumps(dict(passed=ok,clips=len(checks),errors=errors,finding=finding)),flush=True)
raise SystemExit(0 if ok else 1)
