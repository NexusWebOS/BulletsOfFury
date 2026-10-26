"""Close-up clip of Chronos's frame-animated cores: chrome, regular, rage."""
from pathlib import Path
import subprocess, imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from probe_chronos_glow_1025 import SETUP, READY, STATES
R = Path(__file__).resolve().parents[1]; O = R/'_shots/chronos_glow_1025/cores_film'; O.mkdir(parents=True, exist_ok=True)
for f in O.glob('*.png'): f.unlink()
port, stop = serve(str(R)); n = 0
try:
  with sync_playwright() as pw:
    br = pw.chromium.launch(channel='msedge'); p = br.new_page(viewport={'width':1280,'height':800})
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'", timeout=180000)
    p.mouse.click(3,3); p.evaluate(TRAP_RAF); p.evaluate(SETUP); p.wait_for_function(READY, timeout=180000)
    for st, secs in (('chrome', 4), ('regular', 3), ('rage', 3)):
      p.evaluate(STATES[st])
      for i in range(secs*30):
        p.evaluate("()=>{efxClock+=1/30;boss.x=340;boss.y=260;boss.flash=0;particles.length=0;boss._hammer._cgPrev={mode:cgMode(boss).mode};shake=0;flashScreen=0;drawWorld(0);}")
        p.screenshot(path=str(O/f'{n:04d}.png'), clip={'x':400,'y':260,'width':420,'height':400}); n += 1
    br.close()
finally: stop()
out = R/'_shots/chronos_glow_1025/chronos_cores_frames.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','30','-i',str(O/'%04d.png'),'-vf','scale=840:800:flags=neighbor','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
print('wrote', out, n)
