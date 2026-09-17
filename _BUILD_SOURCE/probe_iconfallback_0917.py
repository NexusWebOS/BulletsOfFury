#!/usr/bin/env python3
"""probe_iconfallback_0917.py - which weapon icons actually reach the canvas, per slot.

⚠ "0 blits" and "my trap missed" are the same number, so this measures PIXELS: each key is drawn onto a
scratch canvas through the real iconBlit and the lit pixels are counted. The control is slot 0, whose
icon is known to draw.
"""
import os, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

def main():
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof iconBlit==='function' && typeof weaponIconKey==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        keys = pg.evaluate("""() => {
          const out=[];
          for(const w of FORGE_WEAPONS){ run.weapon=w; run.forge={};
            out.push({w:w, base:weaponIconKey(w,3), forged:'micon_forge_fire_'+w}); }
          return out; }""")
        allk = sorted(set([k['base'] for k in keys] + [k['forged'] for k in keys]))
        # ⚠ micon_lasermist_* lives on its OWN atlas, not on nia_icons: touching the ICON key starts
        #   nothing, and laserMistAtlasBlit returns null until that sheet is ready. The 0916 unlock-page
        #   lesson - a row whose art is not on nia_icons must warm its own sheet or it is a silent hole.
        pg.evaluate("(ks) => { for(const k of ks) XART.rdy(k); if(typeof laserMistWarm==='function') laserMistWarm(); XART.rdy('bof_laser_mist_weapon_atlas'); }", allk)
        pg.wait_for_timeout(2000)
        res = pg.evaluate("""(ks) => {
          const c=document.createElement('canvas'); c.width=80; c.height=80; const g=c.getContext('2d');
          const out={};
          for(const k of ks){
            g.clearRect(0,0,80,80);
            try{ iconBlit(g,k,40,40,60,true); }catch(e){ out[k]='throw'; continue; }
            const d=g.getImageData(0,0,80,80).data; let n=0; for(let i=3;i<d.length;i+=4) if(d[i]>8) n++;
            out[k]=n;
          }
          return out; }""", allk)
        print(json.dumps(res, indent=1))
        print('\n  slot -> base icon lit px / forged icon lit px')
        for k in keys:
            print('   %d  %-28s %-7s   %-28s %s' % (k['w'], k['base'], res.get(k['base']), k['forged'], res.get(k['forged'])))
        br.close()
    stop()

if __name__ == '__main__':
    main()
