#!/usr/bin/env python3
"""probe_halo7.py - which level-7 sprites still carry a purple halo?

Mike: "theres still purple halo's left on level 7."

Standing rule (CLAUDE.md): purple halos are CONVERTED TO A BLACK EDGE, never deleted. So this has to
report two different things, because they need different handling:

  HALO PIXELS   magenta/purple that sits on the sprite's OUTER BOUNDARY - the halo, to be converted.
  INTERIOR      magenta inside the silhouette, which may be authored colour and must NOT be touched.

⚠ MAGENTA IS NOT ALWAYS A BUG IN THIS PACK. The RC2 masters punch magenta to ALPHA on purpose as
liquid openings (game.js:2439 - 8,412px on stage 7 alone, and nlq_sludgeF shows through them). That
is terrain, not a sprite halo. Only the nsw_ SPRITE plates are scanned here.

⚠ XART.rdy() STARTS the decode and returns false on that first call - every key is touched, then
waited on.
"""
import http.server, socketserver, threading, functools, base64, io, os, re, json
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

# pull every nsw_ key straight out of the manifest text
man = io.open(os.path.join(GAME, 'assets', 'manifest.js'), encoding='utf-8', errors='ignore').read()
KEYS = sorted(set(re.findall(r'"(nsw_[a-z0-9_]+)"', man)))

GRAB = r"""
(k)=>{
  if(!XART.rdy(k)) return null;
  const im=XART.get(k);
  const c=document.createElement('canvas');
  c.width=im.naturalWidth; c.height=im.naturalHeight;
  const g=c.getContext('2d'); g.imageSmoothingEnabled=false;
  g.clearRect(0,0,c.width,c.height); g.drawImage(im,0,0);
  return {img:c.toDataURL('image/png'), w:c.width, h:c.height};
}
"""

from playwright.sync_api import sync_playwright
from PIL import Image
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)

def is_purple(r, g, b, a):
    if a < 40: return False
    # magenta family: red and blue both well above green
    return r > 90 and b > 90 and g < min(r, b) * 0.62

with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = br.new_page(viewport={'width': 620, 'height': 900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(2500)

    print('scanning %d nsw_ plates' % len(KEYS))
    pg.evaluate("(ks)=>{for(const k of ks){ try{ XART.rdy(k); }catch(e){} }}", KEYS)
    try:
        pg.wait_for_function("(ks)=>ks.every(k=>{try{return XART.rdy(k);}catch(e){return true;}})",
                             arg=KEYS, timeout=30000)
    except Exception:
        print('(some plates did not settle; those are reported as unresolved)')

    worst = []
    unresolved = 0
    for k in KEYS:
        r = pg.evaluate(GRAB, k)
        if not r:
            unresolved += 1; continue
        im = Image.open(io.BytesIO(base64.b64decode(r['img'].split(',', 1)[1]))).convert('RGBA')
        W, H = im.size
        px = im.load()
        halo = interior = 0
        for y in range(H):
            for x in range(W):
                q = px[x, y]
                if not is_purple(*q): continue
                # boundary = touches a transparent/edge neighbour
                edge = False
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x+dx, y+dy
                    if nx < 0 or ny < 0 or nx >= W or ny >= H or px[nx, ny][3] < 40:
                        edge = True; break
                if edge: halo += 1
                else: interior += 1
        if halo or interior:
            worst.append((k, halo, interior, W*H))

    if unresolved: print('%d plate(s) never resolved' % unresolved)
    if not worst:
        print('\nno purple found on any nsw_ plate')
    else:
        print('\n%-26s %8s %10s  %s' % ('plate', 'halo px', 'interior', 'note'))
        for k, halo, inter, tot in sorted(worst, key=lambda t: -t[1]):
            note = '<- HALO, convert to black edge' if halo else 'interior only - may be authored'
            print('%-26s %8d %10d  %s' % (k[:26], halo, inter, note))
        th = sum(w[1] for w in worst)
        print('\n%d halo pixel(s) across %d plate(s)' % (th, sum(1 for w in worst if w[1])))
    if errs: print('PAGE ERRORS: %s' % errs[:2])
    br.close()
