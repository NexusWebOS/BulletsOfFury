from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage6_airframe_1101';base='http://127.0.0.1:8805';d=json.loads((W/'manifest-current.json').read_text());types=None;items=[q for q in d['items']if q['stage']==6 and q['id']=='stage6-l6v-s2'];rows=[];errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto(base+'/enemy-showcase-1031.html?revision=stage6-solid-hulls-1101#enemy=stage6-l6v-s2',wait_until='networkidle');p.evaluate('()=>{const v=document.querySelector("video");v.preload="auto";v.load();}');p.wait_for_function('document.querySelector("video")?.readyState>=2');assert'stage6-l6v-s2-airframe-1101.mp4'in p.evaluate('document.querySelector("video").currentSrc');p.screenshot(path=str(W/'guide-published.png'))
 p.goto(base+'/current/stage6-solid-hulls-1101.html',wait_until='networkidle');assert p.locator('video').count()==27;p.screenshot(path=str(W/'sky-preview-page.png'));p.set_content('<html><body><video id="v" muted playsinline preload="auto"></video><canvas id="c" width="96" height="60"></canvas></body></html>')
 for item in items:
  assert p.request.head(base+item['video']).status==200;assert p.request.head(base+item['poster']).status==200
  q=p.evaluate('''async url=>{const v=document.querySelector('#v');v.src=url;v.load();await new Promise((ok,no)=>{const t=setTimeout(()=>no(Error('load timeout')),12000);v.onloadeddata=()=>{clearTimeout(t);ok()};v.onerror=()=>no(Error('media '+v.error?.code))});v.currentTime=v.duration*.52;await new Promise((ok,no)=>{const t=setTimeout(()=>no(Error('seek timeout')),12000);v.onseeked=()=>{clearTimeout(t);ok()}});await v.play();await new Promise(r=>setTimeout(r,160));v.pause();const c=document.querySelector('#c'),g=c.getContext('2d');g.drawImage(v,0,0,96,60);const a=g.getImageData(0,0,96,60).data;let lit=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]>50)lit++;return {width:v.videoWidth,height:v.videoHeight,duration:v.duration,time:v.currentTime,audio:v.webkitAudioDecodedByteCount,lit,error:v.error?.message||null};}''',base+item['video'])
  q.update(id=item['id'],passed=q['width']==1280 and q['height']==800 and q['lit']>1200 and q['audio']>0 and not q['error']);rows.append(q);print('PASS'if q['passed']else'FAIL',item['id'],q['audio'],'audio bytes',flush=True)
 b.close()
(W/'video-browser-qa-teal-final.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2));assert len(rows)==1 and all(q['passed']for q in rows)and not errors
print('Final teal clip seeks/decodes video and audio; focused page and guide pass')
