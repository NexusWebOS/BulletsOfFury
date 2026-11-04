"""Which sheet cells does PFX13's cell hygiene modify? Before/after contact sheet for review.

    python _BUILD_SOURCE/audit_projectile_clean_1103.py

Fires every registry kind on all nine stages and runs each stage's miniboss and boss briefly, with
window.PFX13_DEBUG_CLEAN set, then writes _shots/projectiles_1103/audit/cleaned.png (original | cleaned
per cell, magnified) and cleaned.json.
"""
from pathlib import Path
import json, sys, base64, io, http.server
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
O = R / '_shots/projectiles_1103/audit'; O.mkdir(parents=True, exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
BOSSES = ['damkeeper','infernoreaver','cryospear','stormsovereign','xenoregent','warhive','sludgeemperor','vileexistence','tidalfusion']
MINIS = ['razorback','magmaward','frostcruiser','olivewarden','spacebomber','siegebomber','dualscoopdredger','heralddeath','voidhorizon']
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); p = br.new_page(viewport={'width': 1100, 'height': 950}); p.set_default_timeout(300000)
        p.add_init_script('window.PFX13_DEBUG_CLEAN=1;')
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        for f in ['balance_lab_1007.js', 'projectile_lab_1007.js', 'projectile_gallery_1103.js']: p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        def pump(n=30):
            for _ in range(n):
                p.evaluate('()=>{const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(performance.now());}'); p.wait_for_timeout(20)
        p.evaluate('()=>{PG3.prime=true;}')   # draw, never film
        for st in range(1, 10):
            for c in [dict(stage=st, kind=MINIS[st-1], mini=True), dict(stage=st, kind=BOSSES[st-1])]:
                c.update(id='c', diff='furious', pilot='yuri', level=3)
                for rep in range(2):   # second run draws with the art the first run requested
                    p.evaluate('c=>PG3.enemyCase(c)', c)
                    for _ in range(8): p.evaluate('()=>PG3.enemySteps(30)')
                    pump()
            kinds = p.evaluate('c=>PG3.registryCase(c)', dict(id='r', stage=st, kind=BOSSES[st-1], diff='furious', pilot='yuri', level=3))
            for rep in range(2):
                for k in kinds: p.evaluate('k=>PG3.registryFire(k,14)', k)
                pump()
            print('stage', st, p.evaluate('()=>(window.PFX13_CLEANED||[]).length'), flush=True)
        rows = p.evaluate('()=>window.PFX13_CLEANED||[]')
        br.close()
finally:
    stop()
seen, uniq = set(), []
for r in rows:
    k = (r['src'], tuple(round(v) for v in r['rect']))
    if k in seen: continue
    seen.add(k); uniq.append(r)
(O / 'cleaned.json').write_text(json.dumps([{k: v for k, v in r.items() if k not in ('orig', 'clean')} for r in uniq], indent=1))
cols, cw = 4, 2 * 130 + 20
H = 150; sheet = Image.new('RGB', (cols * cw, max(1, (len(uniq) + cols - 1) // cols) * H), (24, 26, 34)); d = ImageDraw.Draw(sheet)
for i, r in enumerate(uniq):
    x, y = (i % cols) * cw, (i // cols) * H
    for j, key in enumerate(['orig', 'clean']):
        im = Image.open(io.BytesIO(base64.b64decode(r[key].split(',', 1)[1]))).convert('RGBA')
        im.thumbnail((128, 128), Image.NEAREST)
        bg = Image.new('RGBA', im.size, (0, 0, 0, 255)); bg.alpha_composite(im)
        sheet.paste(bg.convert('RGB'), (x + 4 + j * 132, y + 16))
    d.text((x + 4, y + 2), (r['round'] or '?') + ' ' + r['src'][:28] + ' -' + str(r['dropped']), fill=(240, 220, 120))
sheet.save(O / 'cleaned.png')
print('unique cleaned cells', len(uniq))
