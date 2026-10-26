"""Record all current native Chronos animation routes in a labelled dual-form reel.
Presentation-only staged poses. No gameplay source or authored art is edited.
"""
from pathlib import Path
import json,base64,subprocess
import imageio_ffmpeg
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_motion_1025/catalog';O.mkdir(exist_ok=True);errors=[];port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;stageLoadBegin(5);bi24Warm();c25Warm();c26Warm();c27Warm();ht23Warm();hf22WarmRed(boss);}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&c25Warm()&&c26Warm()&&c27Warm()&&ht23Warm()&&hf22WarmRed(boss)}',timeout=180000)
  p.evaluate((R/'_BUILD_SOURCE/chronos_animation_catalog_1025.js').read_text(encoding='utf8'))
  chapters=p.evaluate('CHRONOS_CATALOG.chapters');duration=p.evaluate('CHRONOS_CATALOG.duration')
  # Exercise every owner before capturing, allowing any lazy effect to decode.
  for sweep in range(3):
   for c in chapters:
    for u in [.12,.48,.85]:p.evaluate('t=>CHRONOS_CATALOG.draw(t)',c['start']+c['duration']*u)
   p.wait_for_timeout(500)
  validation=[]
  sheet=Image.new('RGB',(1280,278*len(chapters)),'#091320');draw=ImageDraw.Draw(sheet)
  for c in chapters:
   p.evaluate('t=>CHRONOS_CATALOG.draw(t)',c['start']+c['duration']*.62)
   png=p.evaluate("()=>CHRONOS_CATALOG.canvas.toDataURL('image/png').split(',')[1]")
   path=O/('chapter-'+str(c['id']+1).zfill(2)+'.png');path.write_bytes(base64.b64decode(png));im=Image.open(path).convert('RGB');sheet.paste(im.resize((416,260)),((c['id']%3)*426,(c['id']//3)*278));draw.text(((c['id']%3)*426+5,(c['id']//3)*278+261),c['name'],fill='white')
   pixels=p.evaluate("()=>{const a=ctx.getImageData(0,0,640,640).data;let n=0;for(let i=3;i<a.length;i+=4)if(a[i]>20)n++;return n}")
   validation.append(dict(chapter=c['name'],rightLaneAlphaPixels=pixels,passed=pixels>300))
  sheet.crop((0,0,1280,278*((len(chapters)+2)//3))).save(O/'contact.png')
  pre=p.evaluate('CHRONOS_CATALOG.errors');print(json.dumps(dict(chapters=len(chapters),seconds=duration,preflightErrors=pre,missing=[q for q in validation if not q['passed']])),flush=True)
  if pre or errors or any(not q['passed'] for q in validation):raise RuntimeError('Native catalog preflight failed')
  raw=O/'all-animations-both-forms.webm';f=raw.open('wb');p.expose_function('saveCatalogChunk',lambda data:f.write(base64.b64decode(data)))
  p.evaluate("""()=>{const C=CHRONOS_CATALOG;C.done=false;C.time=0;const rec=C.recorder=new MediaRecorder(C.canvas.captureStream(30),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:4500000});C.pending=Promise.resolve();
   rec.ondataavailable=e=>{if(!e.data.size)return;C.pending=C.pending.then(async()=>{const a=new Uint8Array(await e.data.arrayBuffer());let s='';for(let i=0;i<a.length;i+=32768)s+=String.fromCharCode(...a.subarray(i,i+32768));await saveCatalogChunk(btoa(s))})};rec.start(1000);
   let start;function frame(t){if(start==null)start=t;C.time=(t-start)/1000;C.draw(Math.min(C.time,C.duration-.001));if(C.time<C.duration)window.__bofRealRAF(frame);else{rec.onstop=async()=>{await C.pending;C.done=true};rec.stop()}}
   window.__bofRealRAF(frame);
  }""")
  for c in chapters:
   p.wait_for_function('t=>CHRONOS_CATALOG.time>=t||CHRONOS_CATALOG.done',arg=c['start'],timeout=30000);print('Recorded '+c['name'],flush=True)
  p.wait_for_function('CHRONOS_CATALOG.done',timeout=20000);f.close();seen=p.evaluate('Object.fromEntries(Object.entries(CHRONOS_CATALOG.seen).map(([k,v])=>[k,Array.from(v)]))');render_errors=p.evaluate('CHRONOS_CATALOG.errors');browser.close()
finally:stop()
video=O/'all-animations-both-forms.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-y','-loglevel','error','-i',str(raw),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
decode=subprocess.run([ff,'-v','error','-i',str(video),'-f','null','-'],capture_output=True)
report=dict(chapters=chapters,duration=duration,route='Staged animation catalog using current ha21Blue/hammerBossDraw and native effects; both material states; no gameplay edits.',video=str(video.relative_to(R)),validation=validation,selectedFrames=seen,errors=errors+render_errors,decoded=decode.returncode==0 and not decode.stderr)
(O/'catalog.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(video=str(video),decoded=report['decoded'],errors=report['errors'])),flush=True)
raise SystemExit(0 if report['decoded'] and not report['errors'] else 1)
