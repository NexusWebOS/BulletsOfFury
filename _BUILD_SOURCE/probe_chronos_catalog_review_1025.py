from pathlib import Path
import json,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_motion_1025/catalog';errors=[];port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1440,'height':1050});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/chronos_frames_1025/all-animations.html');p.wait_for_function("document.querySelectorAll('#chapters button').length===21",timeout=60000)
  p.get_by_role('button',name='Play all animations',exact=True).click();p.wait_for_function('!v.paused&&v.currentTime>.5',timeout=60000)
  p.get_by_role('button',name='08 · Extended hammer rotation',exact=True).click();p.wait_for_function('v.currentTime>=31&&v.currentTime<36',timeout=60000);p.wait_for_timeout(300);p.screenshot(path=str(O/'review-page.png'))
  a=p.evaluate("()=>{const c=document.createElement('canvas');c.width=v.videoWidth;c.height=v.videoHeight;const g=c.getContext('2d');g.drawImage(v,0,0);return Array.from(g.getImageData(80,200,480,400).data).reduce((n,x,i)=>(n+x*(i%23+1))%1000000007,0)}")
  p.wait_for_timeout(400)
  z=p.evaluate("()=>{const c=document.createElement('canvas');c.width=v.videoWidth;c.height=v.videoHeight;const g=c.getContext('2d');g.drawImage(v,0,0);return Array.from(g.getImageData(80,200,480,400).data).reduce((n,x,i)=>(n+x*(i%23+1))%1000000007,0)}")
  p.get_by_role('button',name='21 · Death / kneeling',exact=True).click();p.wait_for_function('v.currentTime>=94&&v.currentTime<99',timeout=60000)
  result=p.evaluate("()=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,playing:!v.paused,time:v.currentTime,chapters:document.querySelectorAll('#chapters button').length,seekable:v.seekable.length?v.seekable.end(0):0})")
  result['motionPixelsChange']=a!=z;result['errors']=errors;result['passed']=result['duration']>=96 and result['width']==1280 and result['height']==800 and result['chapters']==21 and result['playing'] and a!=z and not errors
  (O/'review-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result),flush=True);b.close()
finally:stop()
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-y','-loglevel','error','-ss','32.5','-i',str(O/'all-animations-both-forms.mp4'),'-frames:v','1',str(O/'decoded-spin.png')],check=True)
raise SystemExit(0 if result['passed'] else 1)
