#!/usr/bin/env python3
"""
build_stage_fonts_v4_0904.py - import CF_BOFStageFonts-Complete-Vol.2 as the game's stage faces.

    python _BUILD_SOURCE/build_stage_fonts_v4_0904.py            # report, write nothing
    python _BUILD_SOURCE/build_stage_fonts_v4_0904.py --write    # pack the atlas + manifest block

Mike, 0904, handing over the pack: "heres the actual stage fonts and pilot select font."

WHAT THE PACK IS. Ten bitmap families - one per stage 1-9 plus a FINAL LEVEL face - each a
1248x384 sheet of 96x96 cells, 46 mapped glyphs, hard alpha, no matte fringe. Every family is
themed to its stage: jungle temple stone, basalt with lava cracks, glacier ice, riveted gunmetal,
fractured amethyst, aviation enamel, corroded sewer metal, alien bone with crimson fissures,
violet warp glass, and ivory/old-gold for the finale.

WHY THIS REPLACES WHAT WAS THERE. The game had FIVE card alphabets (stages 1-5 only, embedded in
the stage card sheets) and stages 6-9 silently borrowed stage 1's grey stone. The nine v3 faces
recovered on 0903 were deleted on 0904u - Mike, shown all nine: "Oof. No, delete these." These are
the replacement, and unlike the v3 set they cover every stage including the bonus.

⚠ THE PACK HAS NO `%` AND NO `( ) +`. Its 46 glyphs are A-Z 0-9 and ! & ' , - . / : ; ? - so the
   stats screen's percent sign is NOT in it, nor the parentheses the old faces carried. That is
   fine and must stay fine: stageGlyph already borrows a missing glyph from a sibling face and
   stage 2's CARD alphabet (58 glyphs) is kept loaded as the donor exactly for this. Verified
   below rather than assumed - the script FAILS if a borrow source cannot supply them.

⚠ GLYPHS ARE PACKED TIGHT, NOT AS 96x96 CELLS. The pack gives a uniform cell plus `bounds_in_cell`
   for the ink. Packing the full cell would make every glyph carry up to 90px of transparent
   padding, and the renderer sizes by frame height - so an 'A' and a '.' would draw at the same
   height and the text would look randomly spaced. The tight bounds are what the existing card
   alphabets store, so the runtime consumes these unchanged.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = r"C:\fp\CF_BOFStageFonts-Complete-Vol.2\Runtime\CF_StageFonts-Vol.2"
OUT_PNG = os.path.join(ROOT, 'assets', 'game', 'atlas', 'fonts_stage_v4.png')
OUT_REL = 'assets/game/atlas/fonts_stage_v4.png'
PAD = 2

from PIL import Image


def load_pack():
    man = json.load(io.open(os.path.join(PACK, 'CF_StageFonts-Vol.2-manifest.json'), encoding='utf-8'))
    out = []
    for e in man['contents']:
        fold, asset = e['folder'], e['asset']
        mp = json.load(io.open(os.path.join(PACK, fold, asset + '-map.json'), encoding='utf-8'))
        im = Image.open(os.path.join(PACK, fold, asset + '-alpha.png')).convert('RGBA')
        key = 'final' if e['stage'] == 'final' else str(e['stage'])
        out.append((key, e, mp, im))
    return out


def main():
    write = '--write' in sys.argv
    fams = load_pack()
    print('%-8s %-11s %-8s %s' % ('face', 'sheet', 'glyphs', 'theme'))
    for key, e, mp, im in fams:
        print('%-8s %-11s %-8d %s' % (key, '%dx%d' % im.size, len(mp['glyphs']), e['theme'][:44]))

    # ---- what the pack cannot draw, and who covers it -------------------------------
    have = set()
    for _k, _e, mp, _i in fams:
        have |= set(mp['glyphs'].keys())
    need_extra = ['%', '(', ')', '+']
    missing = [c for c in need_extra if c not in have]
    print('\nglyphs absent from every family in the pack: %s' % (''.join(missing) or 'none'))
    if missing:
        card2 = os.path.join(ROOT, 'assets', 'manifest.js')
        man = io.open(card2, encoding='utf-8').read()
        i = man.index('"stageArt"'); j = man.index('{', i); d = 0
        for k in range(j, len(man)):
            if man[k] == '{': d += 1
            elif man[k] == '}':
                d -= 1
                if d == 0:
                    card = json.loads(man[j:k + 1]); break
        donor = (card.get('2') or {}).get('font') or {}
        gap = [c for c in missing if c not in donor]
        print("stage 2's card alphabet supplies: %s" % ''.join(c for c in missing if c in donor))
        if gap:
            raise SystemExit('ABORT: nothing can draw %r - importing would silently drop it' % ''.join(gap))
        print('-> every absent glyph is covered by the donor, so the borrow keeps text whole')

    # ---- pack every glyph tight, one shared atlas -----------------------------------
    cells = []
    for key, e, mp, im in fams:
        for ch, g in mp['glyphs'].items():
            r = g['rect']
            b = g.get('bounds_in_cell') or [0, 0, r[2], r[3]]
            box = (r[0] + b[0], r[1] + b[1], r[0] + b[2], r[1] + b[3])
            sub = im.crop(box)
            bb = sub.getbbox()
            if bb: sub = sub.crop(bb)
            if sub.width < 1 or sub.height < 1: continue
            cells.append((key, ch, sub))
    cells.sort(key=lambda c: -c[2].height)
    W = 2048
    x = y = rowh = 0
    place = []
    for key, ch, sub in cells:
        if x + sub.width + PAD > W:
            x = 0; y += rowh + PAD; rowh = 0
        place.append((key, ch, sub, x, y))
        x += sub.width + PAD
        rowh = max(rowh, sub.height)
    H = y + rowh + PAD
    atlas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    block = {}
    for key, ch, sub, px, py in place:
        atlas.alpha_composite(sub, (px, py))
        f = block.setdefault(key, {'atlas': OUT_REL, 'frames': {}, 'font': {}})
        name = 'sf4_%s_%s' % (key, ('p%d' % ord(ch)) if not ch.isalnum() else ch)
        f['frames'][name] = [px, py, sub.width, sub.height]
        f['font'][ch] = name
    print('\npacked %d glyphs into %dx%d' % (len(place), W, H))
    for k in sorted(block): print('   face %-6s %d glyphs' % (k, len(block[k]['font'])))

    if not write:
        print('\nDRY RUN - pass --write to emit the atlas and the manifest block')
        return
    atlas.save(OUT_PNG)
    print('wrote', OUT_PNG)
    js = 'window.BOF.stageFontV4=' + json.dumps(block, separators=(',', ':')) + ';\r\n'
    io.open(os.path.join(ROOT, 'assets', 'stagefonts_v4.js'), 'w', encoding='utf-8', newline='').write(js)
    print('wrote assets/stagefonts_v4.js (%d bytes)' % len(js))


if __name__ == '__main__':
    main()
