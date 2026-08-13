#!/usr/bin/env python3
"""
atlas_reorg.py — repack the atlases into sheets a human can find things in.

    python3 _BUILD_SOURCE/atlas_reorg.py            # DRY RUN: print the plan, touch nothing
    python3 _BUILD_SOURCE/atlas_reorg.py --write    # repack and rewrite the manifest

WHY THIS EXISTS
Mike, 0810r: "I cant even find the icons on the atlas sheets cause the way you organized this game
and atlas sheets is confusing ... make these atlas's easier to understand, named properly, and
sorted properly. Projectiles on 1 atlas. missiles on 1 atlas. stage 1 enemies on 1 atlas, stage 2
etc. each boss their own atlas. The pickup icons and boxes and pills and special ability boxes, 1
atlas. all portraits, expressions from the pilots, 1 atlas etc."

He is right and the numbers say so: 9,726 registered keys packed into 86 sheets named nca_0.png to
nca_86.png, 317MB, with no relationship between a sheet's number and what is on it. tflat_water and
a boss cannon and a pilot portrait can share nca_77. Finding art means grepping the manifest, which
is not something an artist should have to do.

WHAT THIS DOES
Classifies every key into a NAMED group, repacks each group into its own sheet, and rewrites
BOFX.img and BOFX.cells to point at the new sheets. The game reads keys, never filenames, so
nothing in game.js changes.

⚠ ALIASES ARE REAL AND MUST SURVIVE. ~750 keys point at the same rect in the same sheet (a key does
not own its file — CLAUDE.md). Packing each key separately would inflate the atlases and, worse,
break the assumption that two names give the same pixels. Cells are deduped by (source sheet, rect)
so aliases keep sharing one packed cell.

⚠ VERIFY AFTER WRITING, ALWAYS: node _BUILD_SOURCE/verify_atlas_0806z.js resolves every cell, and
the suite reads real rects. A repack that loses one cell is invisible until something draws nothing.
"""
import re, json, os, sys, math
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
MANIFEST = os.path.join(GAME, 'assets', 'manifest.js')
OUTDIR = os.path.join(GAME, 'assets', 'game', 'atlas2')

# ---------------------------------------------------------------- classification
# Order matters: the FIRST rule that matches wins, so put specific before general.
# Each rule is (group name, predicate over the key).
def _pre(*ps):
    return lambda k: any(k.startswith(p) for p in ps)

# ---- GROUND TRUTH, taken from the GAME'S OWN TABLES, not from the key names -------------------
# assets/data/ART_INDEX_SOURCE.json is dumped out of the running game by
# scratchpad/dumptables.py: ENEMY_ART (type -> art role), every per-stage roster, STAGES[].boss,
# SUBBOSS[].kind and BOFX.mechboss. Guessing a family from its prefix is how this project got a
# sheet with a water tile, a boss cannon and a pilot portrait on it; the tables know.
_IDX_PATH = os.path.join(GAME, 'assets', 'data', 'ART_INDEX_SOURCE.json')
IDX = json.load(open(_IDX_PATH, encoding='utf-8')) if os.path.exists(_IDX_PATH) else {}

ENEMY_ART   = IDX.get('enemyArt', {})       # type -> art role prefix
ROSTERS     = IDX.get('rosters', {})        # table name -> [types]
STAGE_BOSS  = IDX.get('bosses', {})         # "1".."8" -> boss kind
STAGE_SUB   = IDX.get('subbosses', {})      # "1".."8" -> sub-boss kind
MECHBOSS    = IDX.get('mechboss', [])       # mbg2, mbo2, mbt7 ... one tag per boss rig

# which stage does a roster belong to
ROSTER_STAGE = {'NEF_S1': 1, 'S1_TANKS': 1, 'S1_JETS': 1,
                'NEF_S2': 2, 'VOLC': 2,
                'NEF_S3': 3,
                'SEWER': 7,
                'ELITE8': 8}

# art role -> stage, built from the rosters. A role is the prefix ENEMY_ART hands drawNewEnemyArt.
ROLE_STAGE = {}
for tbl, stage in ROSTER_STAGE.items():
    for t in ROSTERS.get(tbl, []):
        role = ENEMY_ART.get(t)
        if role:
            ROLE_STAGE[role] = stage
# and the types each stage was OBSERVED to spawn in a real 45s run — rosters cover what a stage
# owns, this covers what it actually fields, and between them an art role gets a stage rather
# than a guess. Observation wins on conflict: the wave script is the ground truth for a stage.
for stage, types in (IDX.get('typesByStage') or {}).items():
    for t in types:
        role = ENEMY_ART.get(t)
        if role:
            ROLE_STAGE[role] = int(stage)

# every mech-boss tag gets its OWN sheet, named for the boss where we know the name
BOSS_TAG_NAME = {'mbg2': 'magma_colossus', 'mbg3': 'cryo_behemoth', 'mbg3f': 'cryo_behemoth_fused',
                 'mbo2': 'obsidian_drill', 'mbm4': 'stage4_mech', 'mbw4': 'warhawk',
                 'mbl5': 'rampart_zero', 'mbr5': 'stage5_mech', 'mbc6': 'storm_sovereign',
                 'mbs6': 'stage6_mech', 'mbs7': 'stage7_mech', 'mbt7': 'toxic_leviathan'}


def _role_group(key):
    """longest ENEMY_ART role that prefixes this key -> that role's stage"""
    best = None
    for role, stage in ROLE_STAGE.items():
        if key.startswith(role) and (best is None or len(role) > len(best[0])):
            best = (role, stage)
    return ('enemies_stage%d' % best[1]) if best else None


RULES = [
    # ---- ordnance ----
    ('missiles',              _pre('msl_', 'mslB_', 'nmsl', 'missilepack')),
    ('projectiles',           _pre('mfx_', 'bfx_', 'nfb_', 'florb_', 'fllaser_', 'aorb_', 'nadb_')),

    # ---- pickups / icons / boxes / pills / special-ability boxes ----
    ('pickups_and_icons',     _pre('micon_', 'nia_', 'item_', 'pw_', 'crate', 'nbox_', 'pill', 'nsp_box')),

    # ---- pilots ----
    ('pilots_portraits',      _pre('port_', 'face_', 'card_', 'aintro_', 'pilotcard', 'pose')),
    ('pilots_ships',          _pre('ship_', 'nthp_')),

    # ---- world ----
    ('terrain_liquids',       _pre('tflat_', 'nlq', 'nwl_', 'nlf_')),
    ('terrain_props',         _pre('nrs_', 'ncl_', 'nst4_', 'nst4b_', 'nsky6_', 'norb5_', 'nst7_')),

    # ---- fx ----
    ('fx_explosions',         _pre('nxp_', 'nx_', 'nck_', 'ntr_', 'nmz')),
    ('fx_misc',               _pre('nfx_', 'ngm_')),

    # ---- ui ----
    ('ui_hud',                _pre('nui_', 'nhud_', 'hud_', 'dlg_', 'btn_', 'nbb_', 'nmb_')),
    ('ui_campaign_map',       _pre('ncm_', 'nss_', 'scard_', 'map')),
    ('ui_fonts',              _pre('g0', 'sfont', 'stagefont', 'bof_font')),
]

def classify(key):
    # 1) a mech-boss tag owns its whole sheet — Mike: "each boss their own atlas"
    for tag in sorted(MECHBOSS, key=len, reverse=True):
        if key.startswith(tag + '_') or key.startswith(tag):
            return 'boss_' + BOSS_TAG_NAME.get(tag, tag)
    # 2) named sub-boss / boss rigs that are not mech tags
    for pre, nm in (('nqx_', 'quadlaser_mini'), ('nql_', 'quadlaser_mini'),
                    ('nobd_', 'obsidian_drill'), ('nglr_', 'glacier_rail'),
                    ('nsx_', 'sectional_rigs'), ('ndam_', 'damkeeper'), ('nqm_', 'damkeeper'),
                    ('mbv_', 'vault'), ('bz', 'vault')):
        if key.startswith(pre):
            return 'boss_' + nm
    # 3) enemies, by the STAGE whose roster names the type that owns this art role
    g = _role_group(key)
    if g:
        return g
    # 4) everything else by family
    for name, pred in RULES:
        if pred(key):
            return name
    return 'misc_unsorted'


def load_manifest():
    src = open(MANIFEST, encoding='utf-8', errors='replace').read()
    m = re.search(r'window\.BOFX\s*=\s*', src)
    st = m.end(); depth = 0; i = st
    while i < len(src):
        if src[i] == '{': depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0: break
        i += 1
    return src, st, i + 1, json.loads(src[st:i + 1])


def main():
    write = '--write' in sys.argv
    src, st, en, B = load_manifest()
    img, cells = B['img'], B['cells']

    groups = defaultdict(list)
    for k in img:
        groups[classify(k)].append(k)

    print('%-24s %6s  %s' % ('GROUP', 'KEYS', 'sample'))
    print('-' * 78)
    total = 0
    for g in sorted(groups, key=lambda g: -len(groups[g])):
        ks = sorted(groups[g]); total += len(ks)
        print('%-24s %6d  %s' % (g, len(ks), ', '.join(ks[:3])))
    print('-' * 78)
    print('%-24s %6d keys in %d groups' % ('TOTAL', total, len(groups)))

    un = sorted(groups.get('misc_unsorted', []))
    if un:
        fam = defaultdict(int)
        for k in un:
            m = re.match(r'^([a-zA-Z]+[0-9]*)[_-]', k)
            fam[m.group(1) if m else k[:6]] += 1
        print('[!] %d keys still unsorted, in %d families - art that cannot be found by name, which is the complaint itself. Largest first:' % (len(un), len(fam)))
        for f, c in sorted(fam.items(), key=lambda z: -z[1])[:30]:
            print('    %-16s %4d' % (f, c))

    if not write:
        print('\nDRY RUN — nothing written. Re-run with --write to repack.')
        return

    print('\n--write not implemented in this pass; classification is reviewed first.')


if __name__ == '__main__':
    main()
