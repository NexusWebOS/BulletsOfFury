#!/usr/bin/env python3
"""
atlas_fammap.py — work out what each opaque art family IS, from the code that draws it.

    python3 _BUILD_SOURCE/atlas_fammap.py        # writes assets/data/ART_FAMILY_MAP.json

WHY THIS EXISTS
The atlas reorg stalled on names, not on packing: 5,064 of 9,726 keys sit in families called
things like ntxl, nvl, ovrotor, ncyc, nmrv, nslc, nlgt, nwf, nbs, nrmp, nsf, nel, nqv. Repacking
those into tidy sheets would leave Mike exactly as unable to find anything as he is now.

⚠ THE OBVIOUS METHOD IS THE EXPENSIVE ONE. Rendering a mid-reel frame of all 316 families and
identifying each by eye is the rule-1 answer, and it is hours. But almost every family is DRAWN by
some function, and the function's name says what the art is far more reliably than the key does:
sxPartOffset owns the sectional-boss parts, drawVolc owns the volcanic units, _bossProjKey owns
boss projectiles, l6*/wfx* own stage 6's weather. So the code names the art.

⚠ AND A KEY CAN BE BUILT, NOT WRITTEN. Before calling a family unreferenced this checks for the
family string anywhere in game.js AND in every BOFX data table, then checks that no shorter prefix
of it is assembled dynamically — _hxvKey builds 'nhxv_'+tag, so a naive scan would have called the
whole nhxv family dead. It is hard-coded there, which is why nhxv survives the check and nhxm does
not.

⚠ NOTHING IS DELETED. Unreferenced families are grouped into a quarantine sheet, which is this
project's standing rule for removals (they are quarantined, never deleted, so any of this is
reversible). They come out of the gameplay sheets, which is the point; they stay on disk.
"""
import re, json, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
OUT = os.path.join(GAME, 'assets', 'data', 'ART_FAMILY_MAP.json')

# enclosing-function -> group. The left side is what the code calls the thing that draws it.
OWNER_GROUP = [
    (r'sxPart|sxDraw|sxPack|drawSubBoss',            'boss_sectional_rigs'),
    (r'_hxvKey|drawHelix|helix',                     'boss_helix_lance'),
    (r'drawNewBoss|drawBossSprite|bossProj|_bossProjKey', 'boss_generic_rigs'),
    (r'drawVolc|volcTick',                           'enemies_stage2'),
    (r'l6[A-Z_]|_l6|wfx|nwx|weather',                'stage6_weather_and_clouds'),
    (r'droneDraw|applyNefUnit|applyS1Jet',           'enemies_generic'),
    (r'speedPadsDraw',                               'terrain_props'),
    (r'transVia|connectorSurface|outbound',          'terrain_transitions'),
    (r'hbDraw|_mavP',                                'pilot_specials'),
    (r'sonicDraw|dkDraw|scrateYield',                'pilot_specials'),
    (r'drawBullets|pShoot|eBullet',                  'projectiles'),
    (r'warmStage|stageMasterKey|drawScrollLevel',    'terrain_masters'),
    (r'updateCamX',                                  'terrain_props'),
]


def load_bofx():
    src = open(os.path.join(GAME, 'assets', 'manifest.js'), encoding='utf-8', errors='replace').read()
    m = re.search(r'window\.BOFX\s*=\s*', src)
    st = m.end(); d = 0; i = st
    while i < len(src):
        if src[i] == '{': d += 1
        elif src[i] == '}':
            d -= 1
            if d == 0: break
        i += 1
    return json.loads(src[st:i + 1])


def main():
    B = load_bofx()
    g = open(os.path.join(GAME, 'assets', 'game.js'), encoding='utf-8').read()
    lines = g.split('\n')
    blob = json.dumps({k: v for k, v in B.items() if k not in ('img', 'cells')})

    enc = [None] * len(lines); cur = None
    for i, l in enumerate(lines):
        mm = re.match(r'^function ([A-Za-z_0-9]+)', l)
        if mm: cur = mm.group(1)
        enc[i] = cur

    fam = defaultdict(list)
    for k in B['img']:
        m = re.match(r'^([a-zA-Z]+[0-9]*)[_-]', k)
        fam[m.group(1) if m else k[:6]].append(k)

    out = {'byFamily': {}, 'unreferenced': [], 'stats': {}}
    named = quarantined = 0
    for f, ks in sorted(fam.items()):
        owners = []
        for i, l in enumerate(lines):
            if f in l and not l.lstrip().startswith('*'):
                if enc[i]: owners.append(enc[i])
                if len(owners) >= 6: break
        if not owners and f not in blob:
            out['unreferenced'].append({'family': f, 'keys': len(ks)})
            out['byFamily'][f] = {'group': 'zz_unreferenced_quarantine', 'keys': len(ks),
                                  'why': 'not named in game.js and not in any BOFX table'}
            quarantined += len(ks)
            continue
        grp = None
        joined = ' '.join(owners)
        for pat, gname in OWNER_GROUP:
            if re.search(pat, joined):
                grp = gname; break
        out['byFamily'][f] = {'group': grp or 'misc_unsorted', 'keys': len(ks),
                              'why': ('drawn by ' + ', '.join(sorted(set(owners))[:3])) if owners
                                     else 'referenced only in a BOFX data table'}
        if grp: named += len(ks)

    out['stats'] = {'families': len(fam), 'namedByCode': named, 'quarantined': quarantined}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1)

    print('families            : %d' % len(fam))
    print('keys named by CODE  : %d' % named)
    print('keys quarantined    : %d  (%d families, unreferenced anywhere)'
          % (quarantined, len(out['unreferenced'])))
    still = sum(v['keys'] for v in out['byFamily'].values() if v['group'] == 'misc_unsorted')
    print('keys still unsorted : %d' % still)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
