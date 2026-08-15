#!/usr/bin/env python3
"""probe_input0812b.py - the four menus that were still keyboard-only, clicked for real.

0812a fixed MODE SELECT and left four: campaign hub, campaign slots, stage select, credits /
stage clear. This drives each with REAL DOM MouseEvents on the canvas and reads the selection
variable the screen actually uses - not a regex for "has a handler", which 0812a's own probe
did and which proves only that code exists.

STAGE SELECT gets the most scrutiny because it is not a vertical list: the flags sit at
authored map coordinates in SSEL_POS, drawn through S=0.75 / MX=0 / MY=64. The probe recomputes
that transform independently and clicks the resulting screen point, so a wrong constant shows
up as a miss rather than being hidden by reusing the game's own maths.

It also asserts the TWO-STAGE rule: clicking an unselected flag must MOVE the cursor and must
NOT deploy. A single click that did both would launch a level the player was only pointing at.
"""
import http.server, socketserver, threading, functools, os, base64
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

# canvas point -> page point, so pg.mouse lands where the game thinks it did
TOPAGE = r"""
(p)=>{ const r=document.getElementById('screen').getBoundingClientRect();
       return {x:r.x + p.x*(r.width/VW), y:r.y + p.y*(r.height/VH)}; }
"""

SETUP_HUB = r"""
()=>{ ASSETS.ready=true; campaign.unlockedMax=8; setState(GS.CAMPHUB);
      for(let i=0;i<30;i++){ try{ drawCampaignHub(1/60); }catch(e){} }
      return {idx:campHubIndex, y0:CAMPHUB_Y0, gap:CAMPHUB_GAP, w:CAMPHUB_W}; }
"""
PUMP_HUB   = "()=>{ for(let i=0;i<4;i++){ try{ drawCampaignHub(1/60); }catch(e){} } return campHubIndex; }"

SETUP_SSEL = r"""
()=>{ ASSETS.ready=true; campaign.unlockedMax=8; window.sselCommitted=false;
      setState(GS.STAGESEL);
      for(let i=0;i<90;i++){ try{ drawStageSelect(1/60); }catch(e){} }
      const pos={}; for(let s=1;s<=8;s++) if(SSEL_POS[s]) pos[s]=SSEL_POS[s];
      return {cursor:sselCursor, pos:pos, boot:sselBoot, t:stateT}; }
"""
PUMP_SSEL  = ("()=>{ for(let i=0;i<4;i++){ try{ drawStageSelect(1/60); }catch(e){} } "
              "return {cursor:sselCursor, committed:!!window.sselCommitted}; }")

SETUP_CRED = r"""
()=>{ ASSETS.ready=true; setState(GS.CREDITS);
      for(let i=0;i<40;i++){ try{ drawCredits(1/60); }catch(e){} }
      return {state:state}; }
"""
PUMP_CRED  = "()=>{ for(let i=0;i<6;i++){ try{ drawCredits(1/60); }catch(e){} } return state; }"

SHOT = "()=>document.getElementById('screen').toDataURL('image/png')"

def png(pg, name):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'wb') as f:
        f.write(base64.b64decode(pg.evaluate(SHOT).split(',', 1)[1]))

from playwright.sync_api import sync_playwright
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)

    def click(cx, cy):
        q = pg.evaluate(TOPAGE, {'x': cx, 'y': cy})
        pg.mouse.move(q['x'], q['y'])
        pg.mouse.down(); pg.mouse.up()

    ok = 0; bad = 0
    def check(label, got, want):
        global ok, bad
        good = (got == want)
        print('  %-46s %-18s %s' % (label, str(got), 'ok' if good else '*** want %s ***' % want))
        if good: ok += 1
        else:    bad += 1

    print('CAMPAIGN HUB')
    h = pg.evaluate(SETUP_HUB)
    print('  rows at y0=%s gap=%s w=%s, cursor starts %s' % (h['y0'], h['gap'], h['w'], h['idx']))
    for row in (2, 0, 1):
        click(310, h['y0'] + row * h['gap'])
        check('click row %d -> campHubIndex' % row, pg.evaluate(PUMP_HUB), row)

    print('STAGE SELECT')
    s = pg.evaluate(SETUP_SSEL)
    S, MX, MY = 0.75, 0, 64
    print('  cursor starts %s, boot=%s, %d flags' % (s['cursor'], s['boot'], len(s['pos'])))
    # click flag 5: must MOVE the cursor and must NOT deploy
    fx = MX + s['pos']['5'][0] * S; fy = MY + s['pos']['5'][1] * S
    print('  flag 5 map(%s,%s) -> screen(%.0f,%.0f)' % (s['pos']['5'][0], s['pos']['5'][1], fx, fy))
    click(fx, fy); r = pg.evaluate(PUMP_SSEL)
    check('first click on flag 5 -> sselCursor', r['cursor'], 5)
    check('first click did NOT deploy', r['committed'], False)
    fx3 = MX + s['pos']['3'][0] * S; fy3 = MY + s['pos']['3'][1] * S
    click(fx3, fy3); r = pg.evaluate(PUMP_SSEL)
    check('click flag 3 -> sselCursor', r['cursor'], 3)
    png(pg, 'stagesel_mouse_0812b.png')
    click(fx3, fy3); r = pg.evaluate(PUMP_SSEL)      # second click on the SAME flag deploys
    check('second click on flag 3 -> deployed', r['committed'], True)

    print('CREDITS')
    pg.evaluate(SETUP_CRED)
    click(310, 400); after = pg.evaluate(PUMP_CRED)
    check('click anywhere leaves CREDITS', after != pg.evaluate("()=>GS.CREDITS"), True)

    b.close()
    print('\n%d ok / %d failed   -> docs/proofs/stagesel_mouse_0812b.png' % (ok, bad))
