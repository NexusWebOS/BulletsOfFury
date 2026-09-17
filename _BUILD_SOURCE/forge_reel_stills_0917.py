#!/usr/bin/env python3
"""forge_reel_stills_0917.py - pull one still per caption out of the Forge reel's frames and lay them on a card."""
import os, json, sys
from PIL import Image, ImageDraw
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SRC = os.path.join(ROOT, '_shots', 'forge_0917')
OUT = os.path.join(ROOT, 'docs', 'proofs', 'forge_0917')
FPS = 15
os.makedirs(OUT, exist_ok=True)
log = json.load(open(os.path.join(SRC, '_log.json')))
want = [c for c in log if c['state'] == 'forge']
tiles = []
for c in want:
    # the frame ~0.8s after the caption is the settled picture for that beat
    i = int(round((c['t'] + 0.8) * FPS))
    p = os.path.join(SRC, 'f%05d.png' % i)
    if not os.path.exists(p): continue
    im = Image.open(p).convert('RGB')
    im.thumbnail((900, 900), Image.LANCZOS)
    tiles.append((im, c['caption'], c['msg']))
    im.save(os.path.join(OUT, 'reel_%02d.png' % len(tiles)))
cols = 2
W = 900 * cols + 30; rows = (len(tiles) + cols - 1) // cols
H = rows * (tiles[0][0].height + 46) + 20 if tiles else 100
card = Image.new('RGB', (W, H), (18, 18, 24)); d = ImageDraw.Draw(card)
for k, (im, cap, msg) in enumerate(tiles):
    x = 10 + (k % cols) * 910; y = 10 + (k // cols) * (im.height + 46)
    d.text((x, y), '%02d  %s' % (k + 1, cap), fill=(255, 230, 120))
    if msg: d.text((x, y + 14), 'screen says: ' + msg, fill=(160, 220, 255))
    card.paste(im, (x, y + 30))
p = os.path.join(OUT, 'forge_reel_stills.png'); card.save(p)
print('%d stills -> %s' % (len(tiles), p))
