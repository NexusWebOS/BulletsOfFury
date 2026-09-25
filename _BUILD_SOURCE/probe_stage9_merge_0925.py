#!/usr/bin/env python3
"""Capture the actual two-sentinel Stage-9 fusion animation in Chromium."""
import base64,json,os,sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,os.path.join(ROOT,'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT=os.path.join(ROOT,'_shots','stage9_merge_0925')
def main():
    os.makedirs(OUT,exist_ok=True)
    port,stop=sh.serve(sh.GAME)
    try:
        with sync_playwright() as pw:
            br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
            pg=br.new_page(viewport={'width':1100,'height':1200})
            errors=[]
            pg.on('pageerror',lambda e:errors.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && (window.__bofFrames|0)>4",timeout=60000)
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(sh.SETUP,{'state':'PLAY','stage':9,'pilot':'cole','invuln':True})
            pg.evaluate("""() => {
              enemies.length=0;eBullets.length=0;spawnBoss('tidalfusion');
              if(!boss||!boss._s9fusion)throw Error('fusion not initialized');
              boss.enter=false;const F=boss._s9fusion;
              F.phase='twins';F.t=2;F.left.x=125;F.right.x=355;
              F.left.y=F.right.y=132;
              F.left.hp=F.right.hp=1;
              F.hit=F.left;s9FusionHit(boss,1);
              F.hit=F.right;s9FusionHit(boss,1);
              player.invuln=1e9;
            }""")
            for i in range(7):
                pg.evaluate(sh.STEP,36 if i else 1)
                pg.wait_for_timeout(95)
                v=pg.evaluate("() => ({phase:boss._s9fusion.phase,t:boss._s9fusion.t,kind:boss.kind})")
                raw=pg.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                with open(os.path.join(OUT,f'merge_{i:02d}.png'),'wb') as f:
                    f.write(base64.b64decode(raw.split(',',1)[1]))
                print(i,v,flush=True)
            print('errors',errors[:5],flush=True)
            br.close()
    finally:stop()

if __name__=='__main__':main()
