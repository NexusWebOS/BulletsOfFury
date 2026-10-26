"""Install the Chronos aura loops: union-crop all frames (no jitter), punch the
animator's grey matte, write one horizontal strip per aura."""
from PIL import Image
import colorsys, os
OUT = '../../assets/game/bosses/chronos_glow_1025/'
for src, dst in [('rage_anim.png', 'aura_rage.png'), ('chrome_anim.png', 'aura_chrome.png')]:
    im = Image.open(src).convert('RGBA'); fw = im.height; n = im.width // fw
    fr = [im.crop((i*fw, 0, i*fw+fw, fw)) for i in range(n)]
    for f in fr:
        px = f.load()
        for y in range(f.height):
            for x in range(f.width):
                r, g, b, a = px[x, y]
                if a == 0: continue
                h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
                if s < .12 and .30 < l < .62: px[x, y] = (0, 0, 0, 0)   # grey matte
    box = None
    for f in fr:
        bb = f.getchannel('A').getbbox()
        box = bb if box is None else (min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3]))
    w, h = box[2]-box[0], box[3]-box[1]
    s = Image.new('RGBA', (w*n, h))
    for i, f in enumerate(fr): s.paste(f.crop(box), (i*w, 0))
    s.save(OUT + dst); print(dst, n, 'frames', w, 'x', h)
