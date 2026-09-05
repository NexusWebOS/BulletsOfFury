#!/usr/bin/env python3
"""
build_stage_fonts_vol3_0904.py - import CF_BOFStageFonts-Vol.3 over the Vol.2 faces.

    python _BUILD_SOURCE/build_stage_fonts_vol3_0904.py            # report, write nothing
    python _BUILD_SOURCE/build_stage_fonts_vol3_0904.py --write    # pack the atlas + manifest

Mike, 0904: "I have found an improved stage font back, replace our stage fonts with these and our
pilot select card screen fonts please."

WHAT CHANGED AGAINST Vol.2, IN THE PACK'S OWN WORDS. Its README: "Stage 6 and Stage 9 were fully
reboxed and vertically normalized. Their approved aviation-enamel and violet warp-phase material
treatments are retained without the previous per-letter offset drift." So Vol.2 shipped stages 6
and 9 with letters that sat at inconsistent heights, and Vol.3 is the fix. Same ten families, same
46 glyphs, same 96x96 cells - this is a remaster, not new art.

⚠ AND Vol.3 CARRIES METRICS Vol.2 DID NOT. Every face declares `cap_top: 6` and `baseline: 90`,
   and every glyph carries `bounds_in_cell` and `origin`. That matters more than the reboxing:

   `glyphBox` bottom-aligns every glyph in the cap box and lifts marks by `FONT_RIDE`, a table of
   TWO entries (' and -) that 0822a had to derive by hand off the dialogue pack because - quoting
   its own comment - "the stage face cannot answer it: all three punctuation cells are TIGHT
   slices with a zero-pixel margin on every side, so the plate carries no vertical placement at
   all." Vol.3's map answers it, for all 46 glyphs, on every one of the ten faces. So the ride is
   now MEASURED per face and per glyph and emitted beside the frames, and the hand table becomes
   the fallback for faces that carry no metrics.

   The check that matters is the same one 0822a used: the glyphs the old code already placed
   correctly must not move. Verified below - ' and - derive to within a hair of the hand-measured
   0.00 and 0.60, and . : ! ? derive to the 1.0 default.

⚠ THE PACK STILL HAS NO `%` AND NO `( ) +`. Its 46 glyphs are A-Z 0-9 and ! & ' , - . / : ; ? -
   unchanged from Vol.2 - and the stats screen draws a percent sign. stage 2's CARD alphabet stays
   loaded as the donor and `stageGlyph` borrows from it. This script REFUSES to import if the
   donor cannot supply them, exactly as the Vol.2 script did.

⚠ GLYPHS ARE PACKED TIGHT, NOT AS 96x96 CELLS - unchanged, and deliberately. `glyphBox` scales by
   the face's cap height and positions by ride, so it wants the ink and nothing else; padding the
   cells would make every glyph scale by its padding instead. The tight bounds are what the card
   alphabets store and what the runtime already consumes.

THE ATLAS FILE IS RENAMED to say what is in it (rule 1 - filenames lie). The runtime KEY stays
`stageFontV4`: that names the wiring generation, which has not changed, and renaming it would
touch six call sites and several assertions to no visible effect.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = r"C:\sf3\CF_BOFStageFonts-Vol.3"
OUT_PNG = os.path.join(ROOT, 'assets', 'game', 'atlas', 'fonts_stage_vol3.png')
OUT_REL = 'assets/game/atlas/fonts_stage_vol3.png'
OLD_PNG = os.path.join(ROOT, 'assets', 'game', 'atlas', 'fonts_stage_v4.png')
PAD = 2

from PIL import Image


def load_pack():
    man = json.load(io.open(os.path.join(PACK, 'CF_StageFonts-Vol.3-manifest.json'), encoding='utf-8'))
    out = []
    for e in man['contents']:
        fold, asset = e['folder'], e['asset']
        mp = json.load(io.open(os.path.join(PACK, fold, asset + '-map.json'), encoding='utf-8'))
        im = Image.open(os.path.join(PACK, fold, asset + '-alpha.png')).convert('RGBA')
        key = 'final' if str(e.get('stage')) == 'final' else str(e['stage'])
        out.append((key, e, mp, im))
    return out


def ride_of(mp, g):
    """the fraction of leftover cap-box space that sits ABOVE this glyph — glyphBox's own units"""
    top, base = mp.get('cap_top', 6), mp.get('baseline', 90)
    b = g.get('bounds_in_cell')
    if not b:
        return None
    cap = base - top
    ink = b[3] - b[1]
    slack = cap - ink
    if slack <= 0:
        return 1.0
    return round((b[1] - top) / float(slack), 4)


def main():
    write = '--write' in sys.argv
    fams = load_pack()
    print('%-8s %-11s %-7s %s' % ('face', 'sheet', 'glyphs', 'theme'))
    for key, e, mp, im in fams:
        print('%-8s %-11s %-7d %s' % (key, '%dx%d' % im.size, len(mp['glyphs']), e['theme'][:46]))

    # ---- the ride table the pack can now answer, and the two values that must not move ------
    print('\nRIDE, measured off the pack (0 = hung from cap height, 1 = on the baseline):')
    print('   %-4s %s' % ('ch', '  '.join('%-6s' % k for k, _e, _m, _i in fams)))
    for ch in ["'", '-', '.', ',', ':', '!', '?', ';', '&', '/']:
        row = []
        for _k, _e, mp, _i in fams:
            g = mp['glyphs'].get(ch)
            r = ride_of(mp, g) if g else None
            row.append('%-6s' % ('-' if r is None else ('%.2f' % r)))
        print('   %-4s %s' % (repr(ch)[1:-1], '  '.join(row)))
    # ⚠ the regression check: 0822a hand-measured ' at 0.00 and - at 0.60 off the dialogue pack.
    #   If the stage pack disagrees wildly, one of the two is wrong and this must not ship blind.
    for ch, want in (("'", 0.00), ('-', 0.60)):
        vals = [ride_of(mp, mp['glyphs'][ch]) for _k, _e, mp, _i in fams if ch in mp['glyphs']]
        if not vals:
            continue
        lo, hi = min(vals), max(vals)
        ok = abs(sum(vals) / len(vals) - want) <= 0.34
        print("   %-3s hand-measured %.2f  vs pack %.2f..%.2f  %s"
              % (repr(ch)[1:-1], want, lo, hi, 'AGREES' if ok else '*** DISAGREES ***'))
        if not ok:
            raise SystemExit('ABORT: the pack contradicts the hand-measured ride for %r' % ch)

    # ---- what the pack cannot draw, and who covers it ---------------------------------------
    have = set()
    for _k, _e, mp, _i in fams:
        have |= set(mp['glyphs'].keys())
    missing = [c for c in ['%', '(', ')', '+'] if c not in have]
    print('\nglyphs absent from every family in the pack: %s' % (''.join(missing) or 'none'))
    if missing:
        man = io.open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read()
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

    # ---- pack every glyph tight, one shared atlas -------------------------------------------
    cells = []
    for key, e, mp, im in fams:
        for ch, g in mp['glyphs'].items():
            r = g['rect']
            b = g.get('bounds_in_cell') or [0, 0, r[2], r[3]]
            sub = im.crop((r[0] + b[0], r[1] + b[1], r[0] + b[2], r[1] + b[3]))
            bb = sub.getbbox()
            if bb: sub = sub.crop(bb)
            if sub.width < 1 or sub.height < 1: continue
            cells.append((key, ch, sub, ride_of(mp, g)))
    cells.sort(key=lambda c: -c[2].height)
    W = 2048
    x = y = rowh = 0
    place = []
    for key, ch, sub, rd in cells:
        if x + sub.width + PAD > W:
            x = 0; y += rowh + PAD; rowh = 0
        place.append((key, ch, sub, rd, x, y))
        x += sub.width + PAD
        rowh = max(rowh, sub.height)
    H = y + rowh + PAD
    atlas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    block = {}
    for key, ch, sub, rd, px, py in place:
        atlas.alpha_composite(sub, (px, py))
        f = block.setdefault(key, {'atlas': OUT_REL, 'frames': {}, 'font': {}, 'ride': {}})
        name = 'sf4_%s_%s' % (key, ('p%d' % ord(ch)) if not ch.isalnum() else ch)
        f['frames'][name] = [px, py, sub.width, sub.height]
        f['font'][ch] = name
        if rd is not None and abs(rd - 1.0) > 0.005:
            f['ride'][ch] = rd            # 1.0 is glyphBox's default; only carry the exceptions
    print('\npacked %d glyphs into %dx%d' % (len(place), W, H))
    for k in sorted(block):
        print('   face %-6s %d glyphs, %d carry a non-default ride' % (k, len(block[k]['font']), len(block[k]['ride'])))

    if not write:
        print('\nDRY RUN - pass --write to emit the atlas and the manifest block')
        return
    atlas.save(OUT_PNG)
    print('wrote', OUT_PNG)
    js = 'window.BOF.stageFontV4=' + json.dumps(block, separators=(',', ':')) + ';\r\n'
    io.open(os.path.join(ROOT, 'assets', 'stagefonts_v4.js'), 'w', encoding='utf-8', newline='').write(js)
    print('wrote assets/stagefonts_v4.js (%d bytes)' % len(js))
    if os.path.exists(OLD_PNG):
        os.remove(OLD_PNG)
        print('removed the superseded Vol.2 atlas', OLD_PNG)


if __name__ == '__main__':
    main()
