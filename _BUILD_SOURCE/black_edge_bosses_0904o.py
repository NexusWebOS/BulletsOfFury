"""
black_edge_bosses_0904o.py - give every boss plate an edge that SURVIVES its own minification.

Mike: "stage-7 yes the black edges for the frames it and almost all bosses."

⚠ THE BOSSES ALREADY HAD BLACK EDGES. THEY WERE JUST INVISIBLE. Measured the silhouette of all 29
   standalone boss plates: dark-edge coverage runs 69-100%, so the outlines are there and nearly
   complete. The problem is thickness against the draw size:

     OLIVE WARDEN   (stage 7)  477x516 plate drawn at 210x216  -> 2.39x   1px renders as 0.42px
     XENO REGENT               258x745 plate drawn at 216x208  -> 3.58x   1px renders as 0.28px
     MAGMA WARD                503x516 plate drawn at 210x216  -> 2.39x   1px renders as 0.42px
     RIME WALL                 488x516 plate drawn at 224x236  -> 2.19x   1px renders as 0.46px
     HERALD OF DEATH           512x512 plate drawn at 210x216  -> 2.37x   1px renders as 0.42px

   A sub-pixel outline is dropped by nearest-neighbour minification wherever it happens to fall,
   which is why the frames read as having "terrible edges" despite being outlined in the file.

   So the edge is thickened IN PROPORTION TO EACH PLATE'S OWN MINIFICATION - round(factor),
   clamped to 2..4 - so every boss lands at roughly one solid pixel on screen regardless of how
   its plate was authored. A flat 2px would still vanish on the Xeno Regent at 3.58x.

EXCLUDED, deliberately:
  nsb_bossfield_0     the energy shield. It is a GLOW; a black rim around it would read as a hole
                      punched in the screen.
  nsb_dcarrmk2_closed 3210x2992 - a multi-frame launch sheet, not a single hull. Outlining it
                      would trace every frame's own bbox inside the sheet and bleed between them.
  nsb_dcarrier_00     0.50x - it is UPSCALED at draw time, so its 1px edge already renders 2px.
"""
import io, os, re, sys, math
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clean_hull_edges_0904h as CH

SKIP = ('nsb_bossfield_0', 'nsb_dcarrmk2_closed', 'nsb_dcarrier_00',
        'nsb_doomsdaycarrier_damaged', 'nsb_doomsdaycarrier_critical')
MIN_FACTOR = 1.15          # below this the plate is barely reduced and needs no help


def plate_map():
    g = io.open(os.path.join(ROOT, 'assets', 'game.js'), encoding='utf-8', newline='').read()
    src = dict(re.findall(r"XART\._src\.([A-Za-z0-9_]+)='([^']+)'", g))
    src.update(dict(re.findall(r"X\._src\['([A-Za-z0-9_]+)'\]='([^']+)'", g)))
    man = io.open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read()
    mp = dict(re.findall(r'"([A-Za-z0-9_]+)":"(assets/[^"]+\.png)"', man))
    # ⚠ THE MANIFEST MAPS ATLAS-BACKED KEYS TO THE ATLAS FILE, NOT TO A PLATE OF THEIR OWN.
    #   The first cut trusted that map and outlined SIX SHARED ATLASES as if each were a single
    #   hull - boss_s2, boss_s3, boss_s5, mini_s2, mini_s3, mini_s4 - which traces every cell's
    #   silhouette inside the sheet and, with padding, invalidates every rect that indexes it.
    #   Caught it in git status and reverted. A key is only standalone if it has NO rect entry
    #   AND its file is named after it.
    atlas_backed = set(re.findall(r'"([A-Za-z0-9_]+)":\["[A-Za-z0-9_]+",\d+,\d+,\d+,\d+\]', man))
    for k in list(mp):
        if k in atlas_backed:
            del mp[k]
    # every boss: key + its damage states, and the height it is DRAWN at
    out = {}
    for k, key, nm, w, h in re.findall(
            r"(\w+):\s*\{key:'(nsb_[a-z0-9_]+)',\s*name:'([^']+)',\s*w:(\d+),h:(\d+)", g):
        keys = [key]
        m = re.search(re.escape(k) + r":\s*\{.*?dmg:\[([^\]]+)\]", g, re.S)
        if m:
            keys += re.findall(r"'(nsb_[a-z0-9_]+)'", m.group(1))
        for kk in keys:
            p = src.get(kk) or mp.get(kk)
            if not p or not os.path.exists(os.path.join(ROOT, p)):
                continue
            stem = os.path.splitext(os.path.basename(p))[0]
            if kk not in stem and stem not in kk:
                continue        # the file is not this key's own plate - almost certainly an atlas
            out[kk] = (p, int(h), nm)
    return out


def main():
    apply = '--apply' in sys.argv
    plates = plate_map()
    print('%-32s %-11s %-7s %-6s %s' % ('plate', 'size', 'reduce', 'edge', 'action'))
    done = 0
    for k in sorted(plates):
        rel, draw_h, nm = plates[k]
        full = os.path.join(ROOT, rel)
        im = Image.open(full).convert('RGBA')
        factor = im.size[1] / float(max(1, draw_h))
        if k in SKIP:
            print('%-32s %-11s %-7.2f %-6s SKIP (excluded by name)' % (k, '%dx%d' % im.size, factor, '-'))
            continue
        if factor < MIN_FACTOR:
            print('%-32s %-11s %-7.2f %-6s skip (barely reduced)' % (k, '%dx%d' % im.size, factor, '-'))
            continue
        px = max(2, min(4, int(round(factor))))
        margin = CH.room_check(im)
        pad = 0
        if margin < px:
            # ⚠ THE PLATES THAT NEED THIS MOST HAVE NO ROOM FOR IT. Olive Warden, Magma Ward,
            #   Rime Wall and Xeno Regent all run their art to the canvas edge - 0px margin - so
            #   an outline drawn OUTSIDE the silhouette has nowhere to go. Padding the canvas
            #   symmetrically gives it somewhere. The boss is drawn by scaling the plate to its
            #   hull box, so padding shrinks the hull by pad/height - 4px on a 516px plate is
            #   0.8%, invisible - and every damage state of a boss is the same size and takes the
            #   same padding, so the states stay aligned with each other.
            pad = px + 1
            big = Image.new('RGBA', (im.size[0] + pad * 2, im.size[1] + pad * 2), (0, 0, 0, 0))
            big.alpha_composite(im, (pad, pad))
            im = big
        CH.OUTLINE_PX = px
        new, rim, add, lab = CH.clean(im, allow_label=False)
        print('%-32s %-11s %-7.2f %-6d %dpx edge  (+%d px, rim -%d)  %s'
              % (k, '%dx%d' % im.size, factor, add, px, add, rim,
                 ('WRITTEN' if apply else 'dry run') + (' +pad%d' % pad if pad else '')))
        if apply:
            new.save(full)
        done += 1
    print()
    print('%s  %d plates' % ('APPLIED' if apply else 'DRY RUN (pass --apply)', done))


if __name__ == '__main__':
    main()
