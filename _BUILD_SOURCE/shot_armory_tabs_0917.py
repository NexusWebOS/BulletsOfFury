#!/usr/bin/env python3
"""shot_armory_tabs_0917.py - render the ARMORY's three NEW tabs and count the icon blits per row.

⚠ micon_lasermist_* does not resolve through iconBlit (CLAUDE.md, 0916: it has its own path,
laserMistAtlasBlit), so the MIST tab is the one that can silently draw nothing. This renders FLAME,
MIST and BOLT and reports, per tab, how many row icons actually reached the canvas.
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'forge_noncarriers_0917')

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof drawArmory==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; XART.rdy('statpanel_full_0916');\
          for(const e of Object.keys(INFUSIONS)) for(const w of FORGE_WEAPONS) for(let l=1;l<=5;l++) XART.rdy('micon_forge_'+e+'_'+w+(l>1?'_'+l:''));\
          for(let i=1;i<=5;i++){ XART.rdy('micon_firewall_'+i); XART.rdy('micon_lasermist_'+i); XART.rdy('micon_lightningorb_'+i); }\
          armoryOpen('vault'); setState(GS.ARMORY); }" % sh.STEP)
        pg.wait_for_timeout(1200); pg.evaluate("() => { for(let i=0;i<30;i++) window.__step(1); }")
        # count what each ROW actually blits: wrap iconBlit and the lasermist's own path
        pg.evaluate("""() => {
          window.__icons=0; const ib=window.iconBlit; if(ib) window.iconBlit=function(){ window.__icons++; return ib.apply(this,arguments); };
          if(typeof laserMistAtlasBlit==='function'){ const lb=laserMistAtlasBlit; laserMistAtlasBlit=function(){ window.__icons++; return lb.apply(this,arguments); }; }
        }""")
        for tab, label in ((4, 'FLAME'), (6, 'MIST'), (8, 'BOLT')):
            i = pg.evaluate("([w]) => { armory.tab=FORGE_WEAPONS.indexOf(w); armory.i=0; armory.scroll=0; window.__icons=0; for(let k=0;k<12;k++) window.__step(1); return window.__icons; }", [tab])
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, 'armory_tab_%s.png' % label.lower()), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
            print('  %-6s tab: %d icon blits over 12 frames (5 rows x 12 = 60 if every row draws)' % (label, i))
        print('  errors:', len(errs))
        br.close()
    stop()

if __name__ == '__main__':
    main()
