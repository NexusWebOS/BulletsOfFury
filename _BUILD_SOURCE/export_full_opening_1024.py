from pathlib import Path
import base64,subprocess,imageio_ffmpeg,json,math
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/opening_storyboard_1024';port,stop=serve(str(R));errors=[];fps=12;frames=0
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('!!window.BOF_STORYBOARD',timeout=180000);p.evaluate(TRAP_RAF);p.wait_for_timeout(80)
 p.evaluate("()=>{run.pilot='yuri';run.stage=1;campaignIntroStart(()=>openStageSelect(1,{boot:true}));campaignIntroWarm();}");p.wait_for_function('campaignIntroReady()',timeout=180000)
 p.evaluate("()=>{window.fullOut=document.createElement('canvas');fullOut.width=960;fullOut.height=600;window.fullGrab=()=>{const g=fullOut.getContext('2d');g.fillStyle='#000';g.fillRect(0,0,960,600);const k=Math.min(960/cv.width,600/cv.height);g.drawImage(cv,(960-cv.width*k)/2,(600-cv.height*k)/2,cv.width*k,cv.height*k);return fullOut.toDataURL('image/png').split(',')[1];};}")
 ff=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r',str(fps),'-i','pipe:0','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'full-opening-to-level1.mp4')],stdin=subprocess.PIPE)
 def put(raw):
  global frames
  ff.stdin.write(base64.b64decode(raw));frames+=1
 end=p.evaluate('IP21.end');print('Opening duration',end,flush=True)
 for f in range(math.ceil(end*fps)):
  put(p.evaluate("t=>{campaignIntro.t=Math.min(t,IP21.end-.001);drawCampaignIntro(0);return fullGrab();}",f/fps))
 p.evaluate('campaignIntroFinish()')
 for f in range(17*fps):
  p.evaluate(STEP,5);put(p.evaluate('fullGrab()'))
 p.evaluate("Input.injectTap('enter')")
 for f in range(18*fps):
  p.evaluate(STEP,5);put(p.evaluate('fullGrab()'))
  if f%24==0:p.wait_for_timeout(50)
  if f==17*fps: (R/'_shots/intro_order_1024/full-level1.png').write_bytes(base64.b64decode(p.evaluate('fullGrab()')))
 final=p.evaluate('({state,stage:run.stage,play:state===GS.PLAY,stagecard:state===GS.STAGEINTRO})');print('Final state',final,'errors',errors,flush=True)
 ff.stdin.close();assert ff.wait()==0
 (R/'_shots/intro_order_1024/full-sequence-report.json').write_text(json.dumps({'frames':frames,'fps':fps,'duration':frames/fps,'final':final,'errors':errors,'beats':p.evaluate('SB24.intro')},indent=2),encoding='utf8');br.close()
stop()
(O/'full-sequence.html').write_text('''<!doctype html><meta charset="utf-8"><title>Fury opening through Level 1</title><style>body{margin:0;background:#10161d;color:#eef4fa;font:18px system-ui;display:grid;place-items:center;min-height:100vh}main{width:min(1100px,96vw)}video{width:100%;background:black}</style><main><h2>Fury HQ → takeover → destruction → jungle → campaign map → Level 1</h2><video controls autoplay src="full-opening-to-level1.mp4"></video><p>Native game renderer. Yuri illustrates the selected pilot. Silent review export; game audio routes are preserved.</p></main>''',encoding='utf8')
print('Full sequence exported',frames/fps,'seconds')
