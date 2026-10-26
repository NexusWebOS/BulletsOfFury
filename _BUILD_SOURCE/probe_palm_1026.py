"""Palm volley pose: frames stepped per drawn frame, old C32 pose vs the eased one, plus a film of the new."""
from pathlib import Path
import subprocess, imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from probe_chronos_glow_1025 import SETUP, READY
R=Path(__file__).resolve().parents[1]; O=R/'_shots/chronos_glow_1025/palm_seq'; O.mkdir(parents=True,exist_ok=True)
for f in O.glob('*.png'): f.unlink()
port,stop=serve(str(R)); errs=[]
try:
  with sync_playwright() as pw:
    br=pw.chromium.launch(channel='msedge'); p=br.new_page(viewport={'width':1280,'height':800}); p.on('pageerror',lambda e:errs.append(str(e)))
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'",timeout=180000)
    p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.evaluate(SETUP);p.wait_for_function(READY,timeout=180000)
    START="""()=>{playerHit=function(){};const h=boss._hammer;h.hb20Pickup=null;delete h._hf22Charge;h._hf22Red=true;h._c46Done=true;h.state='hammer';h.t=1;
      if(h.frArmor){h.frArmor.activated=false;h.frArmor.hp=0;}boss.x=340;boss.y=230;boss.hp=boss.maxhp*.1;eBullets.length=0;particles.length=0;
      for(let i=0;i<3;i++)updatePlay(1/60);const R=h.c30;R.cycle=0;R.volley=null;R.scale=1;c30Retreat(boss);}"""
    for arm in ('old','new'):
      p.evaluate(START)
      if arm=='old': p.evaluate("()=>{window.__nw=c32Pose;c32Pose=C46.oldPalm;}")
      r=p.evaluate("""()=>{const fs=[];for(let i=0;i<60*7;i++){player.x=340;player.y=470;updatePlay(1/60);if(c32Own(boss)&&boss._hammer.c30.phase.startsWith('volley_w')||boss._hammer.c30.phase==='volley_fire')fs.push(ha21Blue(boss).a.frame);}
        let big=0,sum=0;for(let i=1;i<fs.length;i++){const d=Math.abs(fs[i]-fs[i-1]);sum+=d;if(d>=4)big++;}return {n:fs.length,steps:sum,bigJumps:big};}""")
      print(arm,r)
      if arm=='old': p.evaluate("()=>{c32Pose=window.__nw;}")
    p.evaluate(START); n=0
    for i in range(150):
      p.evaluate("()=>{for(let k=0;k<2;k++){player.x=340;player.y=470;updatePlay(1/60);}eBullets.length=0;drawWorld(1/30);}")
      p.screenshot(path=str(O/f'{n:04d}.png'),clip={'x':300,'y':30,'width':680,'height':750}); n+=1
    print('errors',errs[:3]); br.close()
finally: stop()
out=R/'_shots/chronos_glow_1025/chronos_palm_volley.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','30','-i',str(O/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True);print('wrote',out)
