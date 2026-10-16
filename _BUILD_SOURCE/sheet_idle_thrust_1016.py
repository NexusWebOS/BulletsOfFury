"""Contact sheet (1016): each pilot holding still, 8 consecutive frames of the tail, idle burn ON vs OFF."""
import base64, io, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh
ROOT = Path(__file__).resolve().parents[1]
PILOTS = ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']
GRAB = r"""
(args)=>{ const [n,off]=args; window.PF16_IDLE = off?0:undefined; enemies.length=0; eBullets.length=0;
  const outs=[];
  for(let i=0;i<n;i++){ for(let k=0;k<2;k++){ player.invuln=0; window.__bofStepNow+=1000/60; loop(window.__bofStepNow);} 
    const m=ctx.getTransform(); const sx=m.a, x=(player.x-(typeof _camEff==='number'?_camEff:camX))*sx, y=player.y*m.d;
    const c=document.createElement('canvas'); c.width=90; c.height=120; c.getContext('2d').drawImage(ctx.canvas, x-45, y-20, 90, 120, 0,0,90,120);
    outs.push(c.toDataURL()); }
  return outs; }
"""
port, stop = sh.serve(str(ROOT)); errs=[]
rows=[]
try:
  with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for pk in PILOTS:
      pg = br.new_page(viewport={'width':960,'height':1100}); pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
      pg.goto(f'http://127.0.0.1:{port}/index.html'); pg.wait_for_function('typeof loop==="function" && window.__bofAssetRuntimeReady', timeout=180000)
      pg.evaluate(sh.TRAP_RAF); pg.evaluate(sh.SETUP, {'state':'PLAY','stage':1,'pilot':pk,'invuln':True}); pg.evaluate("()=>{playerHit=function(){};}")
      for _ in range(6): pg.evaluate(sh.STEP, 60); pg.wait_for_timeout(250)
      for off in (1,0):
        rows.append((pk, off, [Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))) for u in pg.evaluate(GRAB,[8,off])]))
      pg.close()
    br.close()
finally: stop()
S=3; W=90*S; H=120*S
sheet=Image.new('RGB',(W*8, H*len(rows)),(20,20,20))
for r,(pk,off,ims) in enumerate(rows):
  for c,im in enumerate(ims): sheet.paste(im.convert('RGB').resize((W,H),Image.NEAREST),(c*W,r*H))
out=ROOT/'docs/proofs/idle_thrust_1016/idle_on_off.png'; sheet.save(out); print('wrote',out,'errors',errs[:3])
