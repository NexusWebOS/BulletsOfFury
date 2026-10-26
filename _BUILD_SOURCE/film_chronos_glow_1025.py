"""A silent native-renderer clip of Chronos's transformations with the glow pass:
chromium activation -> plated idle -> rage charge -> Super Saiyan burst -> rage.
Drives the real state clocks frame by frame (30 fps). Output:
_shots/chronos_glow_1025/chronos_glow_transformations.mp4"""
from pathlib import Path
import subprocess, imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF
from probe_chronos_glow_1025 import SETUP, READY  # noqa: E402  (reuses the probe's setup)

R = Path(__file__).resolve().parents[1]
O = R / '_shots/chronos_glow_1025/film'
O.mkdir(parents=True, exist_ok=True)
for f in O.glob('*.png'):
    f.unlink()
port, stop = serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='msedge')
        p = br.new_page(viewport={'width': 1280, 'height': 800})
        p.goto(f'http://127.0.0.1:{port}/index.html')
        p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'", timeout=180000)
        p.mouse.click(3, 3); p.evaluate(TRAP_RAF); p.evaluate(SETUP)
        p.wait_for_function(READY, timeout=180000)
        p.evaluate("()=>{boss.x=340;boss.y=260;boss.flash=0;const h=boss._hammer;h.hb20Pickup=null;h._cgPrev={};}")
        n = 0
        def frame(js, t):
            global n
            p.evaluate("([js,t])=>{(0,eval)('('+js+')')(t);efxClock+=1/30;updateEffects(1/30);if(shake>0)shake=Math.max(0,shake-1.2);if(flashScreen>0)flashScreen=Math.max(0,flashScreen-.04);boss.x=340;boss.y=260;drawWorld(1/30);}", [js, t])
            p.screenshot(path=str(O / f'{n:04d}.png')); n += 1
        for i in range(0, 101):   # chromium activation 0 .. 3.35 s
            frame("t=>{const h=boss._hammer;h.state='fr_activation';h.t=t;}", i * 3.35 / 100)
        for i in range(45):       # plated idle with the glint
            frame("t=>{const h=boss._hammer;h.state='hammer';h.t=1;h.frArmor=Object.assign(h.frArmor||{},{hp:1000,activated:true});}", 0)
        frame("t=>{const h=boss._hammer;h.frArmor.activated=false;h.frArmor.hp=0;h.c27RagePending=true;boss.hp=boss.maxhp*.1;h._cgPrev={mode:'regular'};hf22BeginBlueRage(boss);}", 0)
        n_ssj = int(p.evaluate('CG_SSJ') * 30)
        for i in range(0, n_ssj):  # the rage charge at its real length (CG_SSJ s)
            frame("t=>{const h=boss._hammer;if(h._hf22Charge)h._hf22Charge.t=t;}", i * 1.8 / (n_ssj - 1))
        frame("t=>{const h=boss._hammer;delete h._hf22Charge;h._hf22Red=true;h.rage=999;h.state='hammer';h.t=1;}", 0)
        for i in range(75):       # the burst settles into permanent rage
            frame("t=>{}", 0)
        br.close()
finally:
    stop()
out = R / '_shots/chronos_glow_1025/chronos_glow_transformations.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-framerate', '30', '-i', str(O / '%04d.png'),
                '-vf', 'crop=760:640:260:80', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out)], check=True)
print('wrote', out, n, 'frames')
