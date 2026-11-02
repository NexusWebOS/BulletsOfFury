"""Published guide, native media seeking/decoded frames, cue and roster checks."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/enemy_flight_1031';base='http://127.0.0.1:8805';rows=[];errors=[]
data=json.loads((W/'guide-manifest-current.json').read_text());items=[q for q in data['items']if 4<=q['stage']<=9]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto(base+'/enemy-showcase-1031.html?revision=stage4-9-flight-1031#enemy=stage4-s4interceptor',wait_until='networkidle',timeout=60000);p.evaluate('()=>{const v=document.querySelector("video");v.preload="auto";v.load();}');p.wait_for_function('document.querySelector("video")?.readyState>=2',timeout=30000);p.screenshot(path=str(W/'published-guide.png'))
  guide=p.evaluate('()=>({title:document.title,video:document.querySelector("video").currentSrc,text:document.body.innerText.slice(0,500)})');assert'stage4-s4interceptor-flight-1031.mp4'in guide['video'],guide
  p.set_content('<!doctype html><html><body style="margin:0;background:#070c14"><video id="v" muted playsinline preload="auto" style="width:100vw;max-height:100vh"></video><canvas id="c" width="96" height="60" style="display:none"></canvas></body></html>')
  for item in items:
   assert p.request.head(base+item['video']).status==200,item['id'];assert p.request.head(base+item['poster']).status==200,item['id']
   q=p.evaluate('''async url=>{const v=document.querySelector('#v'),c=document.querySelector('#c');v.pause();v.removeAttribute('src');v.load();v.src=url;v.load();
    await new Promise((ok,no)=>{const t=setTimeout(()=>no(Error('metadata timeout')),12000);v.onloadeddata=()=>{clearTimeout(t);ok()};v.onerror=()=>{clearTimeout(t);no(Error('media '+v.error?.code))};});
    v.currentTime=v.duration*.55;await new Promise((ok,no)=>{const t=setTimeout(()=>no(Error('seek timeout')),12000);v.onseeked=()=>{clearTimeout(t);ok()};});await v.play();await new Promise(r=>setTimeout(r,100));v.pause();const g=c.getContext('2d');g.drawImage(v,0,0,96,60);const a=g.getImageData(0,0,96,60).data;let lit=0;const colors=new Set();for(let i=0;i<a.length;i+=4){if(a[i]+a[i+1]+a[i+2]>50)lit++;colors.add((a[i]>>4)+','+(a[i+1]>>4)+','+(a[i+2]>>4));}
    return{duration:v.duration,time:v.currentTime,width:v.videoWidth,height:v.videoHeight,ready:v.readyState,lit,colors:colors.size,audioBytes:v.webkitAudioDecodedByteCount||0,error:v.error?.message||null};}''',base+item['video'])
   q.update(id=item['id'],passed=q['width']==1280 and q['height']==800 and q['ready']>=2 and q['lit']>1200 and q['colors']>80 and not q['error']);rows.append(q);print('PASS'if q['passed']else'FAIL',item['id'],'seek',round(q['time'],2),'audioBytes',q['audioBytes'],flush=True)
  br.close()
finally:
 (W/'video-browser-qa.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2))
assert len(rows)==114 and all(q['passed']for q in rows)and not errors,(len(rows),errors)
print('All114 published clips seek and decode in native Chromium; no page/console errors')
