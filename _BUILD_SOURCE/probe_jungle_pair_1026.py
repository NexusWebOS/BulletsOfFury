from pathlib import Path
import json,subprocess,imageio_ffmpeg
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/jungle_pair_1026';O.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(str(R));errors=[];rows=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(sh.TRAP_RAF)
  p.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
  p.wait_for_function("XART.rdy('air13_s1_s1jetdelta_heading')",timeout=90000)
  p.evaluate("()=>{enemies=[];eBullets=[];fb9SwoopPair();window.pair=enemies.slice();window.pairShots=0;const shoot=eShootT;eShootT=function(){pairShots++;return shoot.apply(this,arguments);};}")
  for i in range(115):
   p.evaluate(sh.STEP,2)
   q=p.evaluate("()=>{return {planes:pair.map(e=>({x:e.x,y:e.y,head:e._fb9Swoop.head,phase:e._fb9Swoop.phase,dead:!!e.dead,w:e.w,h:e.h,frame:e._air13Frame,key:e._air13RenderedKey})),shots:pairShots};}");rows.append(q)
   p.screenshot(path=str(O/f'{i:03d}.png'))
  b.close()
finally:stop()
checks={'authored_frames':len({e['frame'] for q in rows for e in q['planes'] if 'frame' in e})>=5,'pair':len(rows[0]['planes'])==2,'clearance':all(abs(q['planes'][0]['x']-q['planes'][1]['x'])>=180 for q in rows),'row':any(all(e['phase']=='row' for e in q['planes']) and abs(q['planes'][0]['y']-q['planes'][1]['y'])<1 for q in rows),'shooting':rows[-1]['shots']>10,'exit':all(e['dead'] for e in rows[-1]['planes']),'no_errors':not errors}
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors,rows=rows),indent=2));print(checks)
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','30','-i',str(O/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(O/'pair.mp4')],check=True)
assert all(checks.values())
