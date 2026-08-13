#!/usr/bin/env python3
"""probe_icons.py — what does the HUD actually DRAW for each weapon slot?

Mike: "I see your using a basic graphic for fireball icon". CLAUDE.md's standing warning is that
`micon_` lives in a THIRD art store (BOFX.icons -> iconDraw), not XART and not ASSETS, and that two
fixes in a row went to the wrong door. So this asks the one question that settles it: for each
weapon, WHICH KEY does the HUD resolve, does iconDraw return a width for it (i.e. did it draw), and
what does the composited HUD look like.
"""
import http.server, socketserver, threading, os, functools, base64, sys

GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

RUN = r"""
([stage, weapon, lv, pilot]) => {
  ASSETS.ready=true; run.pilot=pilot||'cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY);
  run.weapon=weapon; run.wlevel=lv; if(run.wlevels) run.wlevels[weapon]=lv;
  const t0=performance.now(); let f=0;
  for(let i=0;i<90;i++) loop(t0+(f++)*16.7);
  const key = (typeof weaponIconKey==='function') ? weaponIconKey(weapon, lv) : '?';
  // did iconDraw actually put pixels down? it returns the drawn width, or null
  let drew=null;
  try { drew = iconDraw(key, 10, 10, 40, false); } catch(e){ drew='THREW '+e.message; }
  return {stage, weapon, lv, key,
          inIcons: !!(BOFX.icons && BOFX.icons[key]),
          sheet: (BOFX.icons && BOFX.icons[key]) ? (BOFX.icons[key][4]||'nia_icons') : null,
          sheetReady: (BOFX.icons && BOFX.icons[key]) ? XART.rdy(BOFX.icons[key][4]||'nia_icons') : null,
          drewWidth: drew};
}
"""

# ⚠ icebreath is PILOT-gated, not stage-gated: weaponIconKey routes w===4 to micon_icebreath_*
# only for Freezer ("his kit, on every stage, not a stage rule"). Probing it as cole draws firewall.
CASES = [(3,5,3,'fireball_stage3','cole'), (2,5,3,'iceorb_stage2','cole'),
         (1,4,3,'icebreath_freezer','freezer'), (1,4,3,'firewall_cole','cole')]

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port = serve(GAME); url='http://127.0.0.1:%d/index.html'%port
    with sync_playwright() as p:
        for stage, wp, lv, tag, pilot in CASES:
            b = p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
            pg = b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
            try:
                pg.goto(url, wait_until='load', timeout=60000)
                pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
                pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
                for _ in range(24):
                    pg.evaluate("()=>{try{XART.rdy('nia_icons');XART.rdy('nia_icons2');}catch(e){}}")
                    pg.wait_for_timeout(200)
                    if pg.evaluate("()=>XART.rdy('nia_icons')&&XART.rdy('nia_icons2')"): break
                r = pg.evaluate(RUN, [stage, wp, lv, pilot])
                print('  %-18s key=%-22s sheet=%-11s ready=%-5s drew=%s'
                      % (tag, r['key'], r['sheet'], r['sheetReady'], r['drewWidth']))
                d = pg.evaluate("""()=>{const o=document.createElement('canvas');
                    const s=document.getElementById('screen'), h=document.getElementById('hud'),
                          e=document.getElementById('equipcv');
                    o.width=s.width; o.height=s.height; const g=o.getContext('2d');
                    g.drawImage(s,0,0); if(h)g.drawImage(h,0,0); if(e)g.drawImage(e,0,0);
                    return o.toDataURL('image/png');}""")
                open(os.path.join(OUT,'icons_hud_%s.png'%tag),'wb').write(base64.b64decode(d.split(',',1)[1]))
            except Exception as ex:
                print('  %-18s FAILED %s' % (tag, str(ex)[:90]))
            finally:
                pg.close(); b.close()

if __name__=='__main__':
    main()
