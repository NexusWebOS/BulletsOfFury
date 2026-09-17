#!/usr/bin/env python3
"""
build_combo_card_0917.py - the combination system as ONE reference card.

Mike: "what you can combine and the lists and all."

⚠ EVERY ROW IS READ OUT OF THE LIVE ENGINE, NOT TYPED HERE. `INFUSIONS`, `INFUSION_CARRIERS`,
`INFUSION_FUSIONS`, `INFUSION_STAGE_BIAS` and `INFUSION_DROP_P` are pulled from the running game
and the card is drawn from what comes back - so a card that disagrees with the game is impossible
rather than merely unlikely. This repo's own history is the argument: a hand-written list goes
stale the moment something new lands, and it has cost a drop every time.
"""
import os, sys, base64, io, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

OUT = os.path.join(ROOT, 'docs', 'proofs', 'combos_0917')

DUMP = """() => ({
  infusions: INFUSIONS,
  carriers: Object.keys(INFUSION_CARRIERS),
  fusions: INFUSION_FUSIONS,
  bias: INFUSION_STAGE_BIAS,
  dropP: (typeof INFUSION_DROP_P!=='undefined') ? INFUSION_DROP_P : null,
  maxLv: (typeof INFUSION_MAX!=='undefined') ? INFUSION_MAX : null
})"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 900, 'height': 700})
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof INFUSIONS!=='undefined'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        data = pg.evaluate(DUMP)
        keys = list(data['infusions'].keys())
        pg.evaluate("(ks) => ks.forEach(k => { try{ XART.rdy('inf_'+k); }catch(_){} })", keys)
        pg.wait_for_timeout(2600)
        pg.evaluate("(ks) => ks.forEach(k => { try{ XART.rdy('inf_'+k); }catch(_){} })", keys)
        pg.wait_for_timeout(1400)
        icons = {}
        for k in keys:
            d = pg.evaluate("""(k) => { const key='inf_'+k; if(!XART.rdy(key)) return null;
              const im=XART.get(key); if(!im) return null;
              const w=im.naturalWidth||im.width, h=im.naturalHeight||im.height; if(!w||!h) return null;
              const c=document.createElement('canvas'); c.width=w; c.height=h;
              c.getContext('2d').drawImage(im,0,0); return c.toDataURL('image/png'); }""", k)
            if d:
                icons[k] = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGBA')
        br.close()
    stop()
    json.dump(data, open(os.path.join(OUT, '_tables.json'), 'w'), indent=2)

    CARRIER_NAME = {'mg': 'MACHINE GUN', 'spread': 'SPREAD FIRE', 'beam': 'LASER',
                    'missile': 'MISSILES', 'orb': 'ORB', 'shard': 'ORB SHARDS'}
    bias_by_elem = {}
    for st, el in (data['bias'] or {}).items():
        bias_by_elem.setdefault(el, []).append(str(st))

    IH = 78
    PAD = 16
    ROW = IH + 12
    W = 1180
    H = PAD * 2 + 46 + ROW * len(keys) + 220
    card = Image.new('RGB', (W, H), (11, 12, 17))
    d = ImageDraw.Draw(card)
    d.text((PAD, PAD), 'BULLETS OF FURY - WEAPON COMBINATION SYSTEM', fill=(255, 226, 120))
    sub = 'an ELEMENT layers onto whatever CARRIER you are holding - it is not a weapon slot.  %d levels.  %.0f%% of a drop-eligible kill.' % (
        data['maxLv'] or 3, (data['dropP'] or 0) * 100)
    d.text((PAD, PAD + 18), sub, fill=(150, 168, 196))
    d.text((PAD, PAD + 34), 'off on stages 5 and 9 (space weapons).  every row below is read out of the running game.', fill=(120, 136, 164))

    y = PAD + 58
    for k in keys:
        I = data['infusions'][k]
        if k in icons:
            ic = icons[k]
            s = IH / ic.height
            ic2 = ic.resize((max(1, int(ic.width * s)), IH), Image.LANCZOS)
            bg = Image.new('RGBA', ic2.size, (11, 12, 17, 255)); bg.paste(ic2, (0, 0), ic2)
            card.paste(bg.convert('RGB'), (PAD, y))
        tx = PAD + 92
        d.text((tx, y + 4), '%s   (%s)' % (I.get('name', k.upper()), k), fill=(255, 236, 160))
        named = I.get('named') or {}
        lv = []
        for n in range(1, (data['maxLv'] or 3) + 1):
            lv.append('L%d %s' % (n, named.get(str(n)) or named.get(n) or I.get('name', k.upper())))
        d.text((tx, y + 24), '   '.join(lv), fill=(198, 214, 236))
        bits = []
        if I.get('el'): bits.append('damage element: ' + I['el'])
        if I.get('gate'): bits.append('LOCKED until: ' + ('you beat the last stage (LASER MIST)' if I['gate'] == 'water' else 'NEW GAME +'))
        if k in bias_by_elem: bits.append('drops most on stage ' + '/'.join(sorted(bias_by_elem[k], key=int)))
        d.text((tx, y + 44), '   -   '.join(bits) if bits else '', fill=(138, 156, 184))
        y += ROW

    y += 10
    d.text((PAD, y), 'CARRIERS - the element rides any of these', fill=(150, 220, 255))
    d.text((PAD, y + 20), '   '.join(CARRIER_NAME.get(c, c.upper()) for c in data['carriers']), fill=(214, 228, 244))
    y += 52
    d.text((PAD, y), 'FUSIONS - hold one at L3, pick up a DIFFERENT element: the screen detonates and the new element takes the gun',
           fill=(150, 220, 255))
    y += 22
    fus = list((data['fusions'] or {}).items())
    for i, (pair, name) in enumerate(fus):
        a, b = pair.split('+')
        col = PAD + (i % 3) * 390
        row = y + (i // 3) * 20
        d.text((col, row), '%-22s %s' % (a.upper() + ' + ' + b.upper(), name), fill=(206, 222, 242))
    p = os.path.join(OUT, '_combination_card.png')
    card.save(p)
    print('->', p, card.size)
    print('   elements %d, carriers %d, fusions %d' % (len(keys), len(data['carriers']), len(fus)))

if __name__ == '__main__':
    main()
