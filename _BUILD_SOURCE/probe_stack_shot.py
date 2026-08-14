#!/usr/bin/env python3
"""probe_stack_shot.py — the separation pass, in PIXELS.

probe_stack.py proves the numbers move. This proves you can SEE it, which is the whole of rule 2
in CLAUDE.md: a green suite proves state, a probe reading positions proves state one level out,
and neither of them proves a picture.

It builds the same deliberate pile-up twice in real Chromium — nine stage-1 units dropped into a
40px box, which is the failure Mike is describing when he says they "stack on each other like
that" — steps both for the same number of frames, and writes two PNGs of the same moment with the
pass off and on.

    docs/proofs/separation_0811l_off.png
    docs/proofs/separation_0811l_on.png

⚠ IT DRAWS THE FRAME IT MEASURES. probe_arrival.py spent two drops comparing two cinematic frames
because it read the canvas on a branch that had not stepped yet, and probe_seam.py asserted the
fix it was meant to test by RECOMPUTING the value under test. Both screenshots here are taken
after drawWorld has run on the same frame index, from the live canvas, with no recomputation.
"""
import http.server, socketserver, threading, os, functools, base64
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')

def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

RUN=r"""
([sepOn, frames])=>{
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(1); setState(GS.PLAY); player.reset();
  player.x=240; player.y=470; player.invuln=1e9;
  window.__sepOff = !sepOn;

  /* THE PILE-UP, built by hand so both arms get the identical one. Nine units into a 40px box —
     a wave that lands on top of itself, which is the shape of the complaint. */
  enemies.length=0; eBullets.length=0; pBullets.length=0;
  const spots=[[0,0],[12,8],[-10,14],[6,-12],[18,4],[-16,-6],[2,18],[-4,-18],[14,-14]];
  for(const [ox,oy] of spots) spawnEnemy('s1jetdelta', 240+ox, 210+oy, {route:'straight'});

  for(let i=0;i<frames;i++){ player.hp=99;
    for(const e of enemies) e._dodge=0;
    updatePlay(1/60); try{ drawWorld(1/60); }catch(err){} }

  /* worst burial still standing on the frame that is about to be photographed */
  let worst=0;
  for(let a=0;a<enemies.length;a++) for(let b=a+1;b<enemies.length;b++){
    const A=enemies[a], B=enemies[b];
    if(A.dead||B.dead) continue;
    const ox=(A.w+B.w)*0.42-Math.abs(B.x-A.x), oy=(A.h+B.h)*0.42-Math.abs(B.y-A.y);
    if(ox>0&&oy>0) worst=Math.max(worst, Math.min(ox/Math.min(A.w,B.w), oy/Math.min(A.h,B.h)));
  }
  const alive=enemies.filter(e=>!e.dead).length;
  return {alive, worstPct:+(worst*100).toFixed(1)};
}
"""
SHOT=r"""
()=>{
  /* ⚠ THE PLAY CANVAS ALONE, AND THE FIRST CUT OF THIS GOT IT WRONG. Copying shoot.py's
     three-canvas composite but drawing each one stretched to #screen's size produced a proof
     that was 100% EQUIPPED box — #equipcv blown up over the whole frame, no game visible at
     all. Rule 1 caught it in one look. #hud and #equipcv are separate elements at their own
     sizes and positions; they are not layers of the play canvas, and this proof does not need
     them. */
  const scr=document.getElementById('screen');
  return scr.toDataURL('image/png');
}
"""
from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
FRAMES=150
with sync_playwright() as p:
    for sep in [False, True]:
        # ⚠ a FRESH browser per arm. Six masters and many toDataURL calls on one page crash
        # Chromium outright ("Target crashed") and silently lose everything measured before it.
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
        r=pg.evaluate(RUN,[sep,FRAMES])
        data=pg.evaluate(SHOT)
        name='separation_0811l_%s.png' % ('on' if sep else 'off')
        with open(os.path.join(OUT,name),'wb') as fh:
            fh.write(base64.b64decode(data.split(',',1)[1]))
        print('sep %-3s  %d units alive after %d frames  worst burial %5.1f%%   -> docs/proofs/%s'
              % ('ON' if sep else 'off', r['alive'], FRAMES, r['worstPct'], name))
        b.close()
