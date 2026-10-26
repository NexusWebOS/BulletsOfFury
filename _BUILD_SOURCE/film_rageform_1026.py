"""The full rage sequence at real speed, driven by the game's own update loop:
hammer throw -> sequential strikes as the red burns in -> final strike -> settled rage.
Output: _shots/chronos_glow_1025/chronos_rage_sequence.mp4 (silent, 30 fps)."""
from pathlib import Path
import subprocess, imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from probe_chronos_glow_1025 import SETUP, READY
R = Path(__file__).resolve().parents[1]; O = R/'_shots/chronos_glow_1025/rage_seq'; O.mkdir(parents=True, exist_ok=True)
for f in O.glob('*.png'): f.unlink()
port, stop = serve(str(R)); n = 0; errs = []
try:
  with sync_playwright() as pw:
    br = pw.chromium.launch(channel='msedge'); p = br.new_page(viewport={'width':1280,'height':800})
    p.on('pageerror', lambda e: errs.append(str(e)))
    p.goto(f'http://127.0.0.1:{port}/index.html')
    p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'", timeout=180000)
    p.mouse.click(3,3); p.evaluate(TRAP_RAF); p.evaluate(SETUP); p.wait_for_function(READY, timeout=180000)
    # settle him in his regular idle in the middle of the field, then let the real 15% trigger start the charge
    p.evaluate("""()=>{playerHit=function(){};const h=boss._hammer;h.hb20Pickup=null;h.state='hammer';h.t=1;h._hf22Red=false;delete h._hf22Charge;
      if(h.frArmor){h.frArmor.activated=false;h.frArmor.hp=0;}boss.x=340;boss.y=230;eBullets.length=0;particles.length=0;
      h.c27RagePending=true;boss.hp=boss.maxhp*.1;hf22BeginBlueRage(boss);}""")
    import sys
    EXTRA = float(sys.argv[1]) if len(sys.argv) > 1 else 3.2
    total = int((p.evaluate('CG_SSJ') + EXTRA) * 30)
    for i in range(total):
      p.evaluate("()=>{for(let k=0;k<2;k++){player.x=340;player.y=470;updatePlay(1/60);}eBullets.length=0;drawWorld(1/30);}")
      p.screenshot(path=str(O/f'{n:04d}.png'), clip={'x':300,'y':30,'width':680,'height':750}); n += 1
      if i % 30 == 0: p.wait_for_timeout(20)
    st = p.evaluate("()=>({red:!!boss._hammer._hf22Red,charging:!!boss._hammer._hf22Charge,ev:BOF_CHRONOS_RAGEFORM.events.map(e=>e.type)})")
    k46=p.evaluate("()=>(window.BOF_CHRONOS_KAMEHAMEHA||{events:[]}).events.map(e=>e.type+'@'+e.t.toFixed(2))");print('kame',k46)
    print('state', st['red'], st['charging'], 'strikes', st['ev'].count('strike'), 'release' in st['ev'], 'final' in st['ev'])
    print('errors', errs[:3])
    br.close()
finally: stop()
out = R/'_shots/chronos_glow_1025/chronos_rage_sequence.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','30','-i',str(O/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
print('wrote', out, n, 'frames')
