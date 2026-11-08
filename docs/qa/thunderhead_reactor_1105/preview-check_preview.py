from pathlib import Path
import json,urllib.request
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;url=json.loads((W/'server.json').read_text())['url'];clips=json.loads((W/'manifest.json').read_text());checks=[];errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url,wait_until='networkidle');p.wait_for_function('document.querySelectorAll(".card").length===3')
 for c in clips:
  p.locator('.card[data-id="'+c['id']+'"]').click();p.wait_for_function('document.querySelector("video").readyState>=2')
  info=p.evaluate('({duration:document.querySelector("video").duration,width:document.querySelector("video").videoWidth,height:document.querySelector("video").videoHeight})')
  checks.append(dict(name=c['name']+' loads with actual video frames',passed=info['width']==c.get('width',1280) and info['height']==c.get('height',800) and abs(info['duration']-c['duration'])<4,data=info))
  p.locator('#chapters button').nth(1).click();p.wait_for_timeout(900)
  sound=p.evaluate('''async()=>{const v=document.querySelector('video');if(!window.qaAudio){const ctx=new AudioContext(),src=ctx.createMediaElementSource(v),a=ctx.createAnalyser();a.fftSize=2048;src.connect(a);a.connect(ctx.destination);window.qaAudio={ctx,a};}await qaAudio.ctx.resume();await v.play();const start=v.currentTime;let peak=0;for(let i=0;i<15;i++){await new Promise(r=>setTimeout(r,40));const s=new Float32Array(2048);qaAudio.a.getFloatTimeDomainData(s);for(const n of s)peak=Math.max(peak,Math.abs(n));}v.pause();return{peak,advanced:v.currentTime-start,time:v.currentTime};}''')
  checks.append(dict(name=c['name']+' chapter seeking, playback and audio',passed=sound['peak']>.00001 and sound['advanced']>.25 and sound['time']>0,data=sound))
  p.locator('#movie').scroll_into_view_if_needed();p.screenshot(path=str(W/(c['id']+'-preview.png')))
  with urllib.request.urlopen(urllib.request.Request(url.rstrip('/')+c['url'],headers={'Range':'bytes=0-1023'}),timeout=15)as r:
   checks.append(dict(name=c['name']+' exact byte-range serving',passed=r.status==206 and r.read()==Path(json.loads((W/'routes.json').read_text())[c['url']]).read_bytes()[:1024]))
 p.locator('.card[data-id="razorwake"]').click();p.wait_for_function('document.querySelector("#vortex-video").readyState>=2')
 d=next(c['death']for c in clips if c['id']=='razorwake')
 info=p.evaluate('({visible:!document.querySelector("#vortex-demo").hidden,duration:document.querySelector("#vortex-video").duration,width:document.querySelector("#vortex-video").videoWidth})')
 checks.append(dict(name='Separate vortex movie metadata and visibility',passed=info['visible']and info['width']==960 and abs(info['duration']-d['seconds'])<1,data=info))
 sound=p.evaluate('''async()=>{const v=document.querySelector('#vortex-video'),a=new AudioContext(),src=a.createMediaElementSource(v),n=a.createAnalyser();n.fftSize=2048;src.connect(n);n.connect(a.destination);await a.resume();v.currentTime=4;await v.play();const start=v.currentTime;let peak=0;for(let i=0;i<20;i++){await new Promise(r=>setTimeout(r,40));const s=new Float32Array(2048);n.getFloatTimeDomainData(s);for(const x of s)peak=Math.max(peak,Math.abs(x));}v.pause();return{peak,advanced:v.currentTime-start};}''')
 checks.append(dict(name='Vortex movie playback and real game audio',passed=sound['peak']>.00001 and sound['advanced']>.25,data=sound))
 with urllib.request.urlopen(urllib.request.Request(url.rstrip('/')+d['url'],headers={'Range':'bytes=0-65535'}),timeout=15)as r:
  checks.append(dict(name='Vortex exact range serving',passed=r.status==206 and r.read()==Path(json.loads((W/'routes.json').read_text())[d['url']]).read_bytes()[:65536]))
 p.set_viewport_size({'width':390,'height':844});p.evaluate('window.scrollTo(0,0)');p.wait_for_timeout(200);p.screenshot(path=str(W/'mobile-preview.png'))
 checks.append(dict(name='Mobile page fits the viewport',passed=p.evaluate('document.documentElement.scrollWidth<=innerWidth')))
 b.close()
checks.append(dict(name='No browser or media errors',passed=not errors));out=dict(checks=checks,errors=errors);(W/'preview-checks.json').write_text(json.dumps(out,indent=2));print('PREVIEW_CHECKS',sum(c['passed']for c in checks),'/',len(checks));print('ERRORS',errors)
if not all(c['passed']for c in checks):raise SystemExit(1)
