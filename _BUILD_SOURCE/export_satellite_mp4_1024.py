from pathlib import Path
import base64,subprocess,imageio_ffmpeg,shutil
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/opening_storyboard_1024';port,stop=serve(str(R))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800});p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('!!window.BOF_STORYBOARD',timeout=180000);p.evaluate("()=>{run.pilot='yuri';campaignIntroStart(()=>{});campaignIntroWarm();}");p.wait_for_function('campaignIntroReady() && Object.values(OT24_ART).every(a=>XART.rdy(a.key)) && ip21Keys().every(k=>XART.rdy(k)) && c22Keys().every(k=>XART.rdy(k))',timeout=180000)
 ff=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r','24','-i','pipe:0','-vf','pad=ceil(iw/2)*2:ceil(ih/2)*2','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'dracodia-satellite-takeover.mp4')],stdin=subprocess.PIPE)
 for f in range(504):
  data=p.evaluate('''q=>{const b=IP21.beats.find(b=>b.replay===(q<8?'arrival':q<16?'takeover':'downlink')),t=q<8?q:q<16?q-8:q-16;campaignIntro.t=b.at+t;ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ip21Visual(b,campaignIntro,t,cutsceneViewWidth(),VH);ctx.restore();return cv.toDataURL('image/png').split(',')[1];}''',f/24)
  raw=base64.b64decode(data);ff.stdin.write(raw)
  if f in [48,144,264,432]:(R/f'_shots/intro_order_1024/mp4-{f}.png').write_bytes(raw)
 ff.stdin.close();assert ff.wait()==0;b.close()
stop();shutil.copyfile(O/'dracodia-satellite-takeover.mp4',O/'dracodia-attached-purple-downlink.mp4');s=(O/'video.html').read_text(encoding='utf8').replace('dracodia-satellite-takeover.webm','dracodia-satellite-takeover.mp4').replace('12-second','21-second');(O/'video.html').write_text(s,encoding='utf8');print('MP4 complete')
