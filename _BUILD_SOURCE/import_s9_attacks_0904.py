#!/usr/bin/env python3
"""
import_s9_attacks_0904.py - bring CF_BossAttacks-Lvl9 into the tree.

    python _BUILD_SOURCE/import_s9_attacks_0904.py            # report
    python _BUILD_SOURCE/import_s9_attacks_0904.py --write     # copy the frames

Mike, 0904: "plus more effects, attacks, projectiles, patterns we enver used and how they should
look in-game."

WHAT THE PACK IS. Eighteen effect families, 140 frames, for the two stage-9 ship bosses - the WARP
SENTINEL (miniboss) and the TIDAL SOVEREIGN (boss). Muzzles, projectiles, beam heads, tileable
beam bodies, impacts, mines, and five "surprise attacks" its README names: Singularity Bloom and
Dimensional Saw for the Sentinel, Tidal Cutter, Maelstrom Orb and the Abyssal Crown five-spear
volley for the Sovereign.

⚠ WHY THIS IS AN UPGRADE AND NOT A RESKIN. Every round those two bosses fire today is PROCEDURAL -
   `s9needle`, `s9warp`, `s9comet`, `s9gold`, `s9pair` all resolve to `procSpace:'s9-...'`, i.e.
   shapes drawn in code. The pack is authored 8-frame pixel art for exactly that ordnance.

⚠ THE "TWIN" MUZZLE PLATES HOLD BOTH FLASHES IN ONE IMAGE. Warp_TwinVoidMuzzle is 112x72 and
   Tidal_TwinHydroMuzzle 128x72, each containing the LEFT and RIGHT flash side by side, and the
   manifest's muzzle_anchors are the two cannon tips they belong to. Drawn once per cannon they
   would put four flashes on screen - the same trap the Chaos Harrier's twin sidelaser plate set
   two drops ago. They are drawn ONCE, centred between the anchors.

⚠ AND FRAME 1 IS A SPARK ON HALF OF THESE FAMILIES. Measured ink on frame 1: TwinVoidMuzzle 17x13,
   CrystalImpact 11x14, SingularityBloom 16x15 - against 87x87 mid-reel for the saw. Anything that
   identifies a family from frame 0 identifies it wrongly (CLAUDE.md rule 1); the contact sheet
   this import was checked against uses MID-reel frames.

Frames are copied as-is: they are already hard alpha, already nearest-neighbour clean, and already
sized to the canvases the manifest declares. No trimming - the canvas IS the registration, and the
anchors in the manifest are expressed in it.
"""
import io, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"C:\b9z\CF_BossAttacks-Lvl9"
DST = os.path.join(ROOT, 'assets', 'game', 's9_attacks')

from PIL import Image


def main():
    write = '--write' in sys.argv
    man = json.load(io.open(os.path.join(SRC, 'Documentation', 'CF_Stage9BossAttacks_Manifest.json'),
                            encoding='utf-8'))
    if write and not os.path.isdir(DST):
        os.makedirs(DST)
    rows, total = [], 0
    reg = []
    for b in man['bosses']:
        print('=== %s  canvas %s  muzzles %s  core %s'
              % (b['display_name'], b['boss_canvas'], b['muzzle_anchors'], b.get('core_beam_anchor')))
        for a in b['attacks']:
            d = os.path.join(SRC, a['folder'])
            fs = sorted(f for f in os.listdir(d) if '-alpha-' in f and f.endswith('.png'))
            if len(fs) != a['frame_count']:
                raise SystemExit('ABORT: %s declares %d frames, has %d'
                                 % (a['folder'], a['frame_count'], len(fs)))
            pre = a['prefix']
            for i, f in enumerate(fs):
                im = Image.open(os.path.join(d, f)).convert('RGBA')
                if list(im.size) != list(a['canvas']):
                    raise SystemExit('ABORT: %s frame %d is %dx%d, manifest says %s'
                                     % (a['folder'], i, im.size[0], im.size[1], a['canvas']))
                out = os.path.join(DST, '%s_%d.png' % (pre, i))
                if write:
                    shutil.copyfile(os.path.join(d, f), out)
                total += 1
            reg.append((pre, len(fs)))
            print('  %-24s %-6s %d frames  loop=%-5s %s'
                  % (a['folder'], 'x'.join(map(str, a['canvas'])), len(fs), a['loop'], a['prefix']))
    print('\n%d frames across %d families' % (total, len(reg)))
    # the registration block, so the wiring cannot disagree with what was copied
    print('\n--- XART registration (paste into game.js) ---')
    print('  const S9A_REELS={' + ','.join("%s:%d" % (p, n) for p, n in reg) + '};')
    print("  for(const _k in S9A_REELS) for(let _i=0;_i<S9A_REELS[_k];_i++)")
    print("    X._src[_k+'_'+_i]='assets/game/s9_attacks/'+_k+'_'+_i+'.png';")
    print('\n' + ('WROTE ' + DST if write else 'DRY RUN - pass --write'))


if __name__ == '__main__':
    main()
