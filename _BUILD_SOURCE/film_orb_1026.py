"""The rage orb laser turn (C42) at real speed, forced to cycle 2 straight after the rage forms."""
from pathlib import Path
import subprocess, imageio_ffmpeg, sys
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from probe_chronos_glow_1025 import SETUP, READY
R=Path(__file__).resolve().parents[1]; O=R/'_shots/chronos_glow_1025/orb_seq'; O.mkdir(parents=True,exist_ok=True)
for f in O.glob('*.png'): f.unlink()
port,stop=serve(str(R)); errs=[]; n=0
try:
  with sync_playwright() as pw:
    br=pw.chromium.launch(channel='msedge'); p=br.new_page(viewport={'width':1280,'height':800}); p.on('pageerror',lambda e:errs.append(str(e)))
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'",timeout=180000)
    p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.evaluate(SETUP);p.wait_for_function(READY,timeout=180000)
    p.evaluate("""()=>{playerHit=function(){};const h=boss._hammer;h.hb20Pickup=null;delete h._hf22Charge;h._hf22Red=true;h._c46Done=true;h.state='hammer';h.t=1;
      if(h.frArmor){h.frArmor.activated=false;h.frArmor.hp=0;}boss.x=340;boss.y=230;boss.hp=boss.maxhp*.1;eBullets.length=0;particles.length=0;
      for(let i=0;i<3;i++)updatePlay(1/60);const R=h.c30;R.cycle=2;R.volley=null;c30Retreat(boss);}""")
    for i in range(int(float(sys.argv[1]) if len(sys.argv)>1 else 6)*30):
      p.evaluate("()=>{for(let k=0;k<2;k++){player.x=340;player.y=470;updatePlay(1/60);}eBullets.length=0;drawWorld(1/30);}")
      p.screenshot(path=str(O/f'{n:04d}.png'),clip={'x':300,'y':30,'width':680,'height':750}); n+=1
      if i%30==0: p.wait_for_timeout(20)
    print('phases',p.evaluate("BOF_CHRONOS_BEAM.events.filter(e=>e.type==='phase').map(e=>e.phase).join(',')"),'orb',p.evaluate("!!BOF_CHRONOS_ORB.lastOrb"))
    print('errors',errs[:3]); br.close()
finally: stop()
out=R/'_shots/chronos_glow_1025/chronos_orb_attack.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','30','-i',str(O/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True); print('wrote',out,n)
