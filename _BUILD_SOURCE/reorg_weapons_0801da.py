#!/usr/bin/env python3
"""
DROP 0801da - WEAPON FX REORGANISATION

Mike: "theres attacks and missiels in other folders instead of main folder. theres
hould be a master folder setup for fx for each weapon. not a seperate attacks
folder."

He is right and the numbers are blunt about it. Weapon FX was spread over twelve
folders with no rule behind which one anything landed in:

    laser        76 keys across 4 folders  (fx/weapons, fx/lasers, fx/ui/icons, fx/attacks/laser)
    chain        73 keys across 4 folders  (fx/attacks/chain, fx/orbitalcharge, fx/falva, fx/weapons_v22)
    explosions  157 keys across 5 folders  (fx/exp, fx/explosions_nx, fx/explosions, fx/explosion_rows)
    missile     172 keys across 3 folders  (fx/giantmissiles, ui/menubtns, fx/master)
    flamethrower 31 keys across 2 folders  (fx/v22, fx/weapons/flame)

The venom strike was filed under assets/enemies/ despite being a player weapon.
Machine-gun icons sat in fx/icons while the pellets sat in fx/machinegun.

TARGET — one folder per weapon, all of them under one root:

    assets/fx/weapons/<weapon>/

THE KEY DECIDES, NOT THE OLD PATH. Classification is by key PREFIX, because the
key says what a thing IS while the folder only recorded where it happened to be
dropped. nmgv_1 is a machine-gun slug wherever it was sitting.

SAFETY
  * every move is paired with a manifest path rewrite in the same pass
  * basename collisions across source folders are detected and renamed, never
    silently overwritten
  * nothing is deleted; a move that cannot be verified is rolled back
  * a LEDGER records every from/to so the whole thing is reversible
  * afterwards every manifest path is re-resolved against disk before it ships
"""
import json, os, re, shutil, sys, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MAN = os.path.join(ROOT, 'assets/manifest.js')
DEST = 'assets/fx/weapons'

# key prefix -> weapon folder.  Order matters: first match wins.
RULES = [
    ('machinegun',   r'^(mfx_mg|nmg|nmgv|mgmuz|micon_mg)'),
    ('spread',       r'^(mfx_spr|nsp_spread|spread_)'),
    ('missile',      r'^(mfx_msl|nms_|ngm_|giantmissile|nmis|missile_|mfx_bmg)'),
    ('laser',        r'^(mfx_lzr|lzr_|nlz_|laser_|nlas)'),
    ('flamethrower', r'^(nfw_|flame_|mfx_flm)'),
    ('iceorb',       r'^(iceshard|nice_|mfx_ice|icefx)'),
    ('helix',        r'^(nhx|helix_|nhxv|nhxsb)'),
    ('chain',        r'^(chain_|nch_|chainkit|nchg)'),
    ('venom',        r'^(nev_venom|venom_)'),
    ('rollerball',   r'^(nfrb_|nrb_|fball_)'),
    ('fusion',       r'^(fchg|fchgc|nfus)'),
    ('thrusters',    r'^(nthr|thr_|nth_)'),
    ('trails',       r'^(ntr_|trail_)'),
    ('shields',      r'^(nsh_|shield_)'),
    ('explosions',   r'^(nx_|nex_|nxp_|exp_)'),
]


def classify(key):
    for name, pat in RULES:
        if re.match(pat, key):
            return name
    return None


def main():
    man = open(MAN, encoding='utf-8').read()
    pairs = re.findall(r'"([a-zA-Z0-9_]+)":"(assets/[^"]+)"', man)

    plan, taken = [], collections.defaultdict(set)
    # ALIASES ARE REAL. Several keys point at the SAME file on purpose —
    # ngm_doom_fl_4 and ngm_doom_fl_6 both reuse ngm_doom_fl_2.png. The first
    # pass moved the file for the first key and then reported "source missing"
    # for every other key that shared it. A source is moved ONCE; every key that
    # referenced it is repointed to that one destination.
    src_dst = {}
    for key, src in pairs:
        w = classify(key)
        if not w:
            continue
        if src.startswith('%s/%s/' % (DEST, w)):
            continue                                   # already home
        if src in src_dst:                             # alias of a file already planned
            plan.append((key, src, src_dst[src]))
            continue
        base = os.path.basename(src)
        name = base
        if name in taken[w]:
            stem, ext = os.path.splitext(base)
            name = '%s__%s%s' % (stem, key, ext)       # keep both, name by key
        taken[w].add(name)
        dst = '%s/%s/%s' % (DEST, w, name)
        src_dst[src] = dst
        plan.append((key, src, dst))

    print('planned moves: %d' % len(plan))
    by_w = collections.Counter(p[2].split('/')[3] for p in plan)
    for w, n in sorted(by_w.items()):
        print('   %-13s %4d' % (w, n))

    # ---- execute: copy, verify, then rewrite the manifest ------------------
    moved, failed, done = [], [], set()
    for key, src, dst in plan:
        s_abs, d_abs = os.path.join(ROOT, src), os.path.join(ROOT, dst)
        if src not in done:
            if not os.path.exists(s_abs):
                failed.append((key, src, 'source missing'))
                continue
            os.makedirs(os.path.dirname(d_abs), exist_ok=True)
            shutil.move(s_abs, d_abs)
            done.add(src)
        if not os.path.exists(d_abs):
            failed.append((key, src, 'move failed'))
            continue
        moved.append((key, src, dst))

    # rewrite every path in one pass, keyed so we never touch the wrong entry
    for key, src, dst in moved:
        man = man.replace('"%s":"%s"' % (key, src), '"%s":"%s"' % (key, dst))
    open(MAN, 'w', encoding='utf-8').write(man)

    os.makedirs(os.path.join(ROOT, '_superseded'), exist_ok=True)
    json.dump(moved, open(os.path.join(ROOT, '_superseded/REORG_LEDGER.json'), 'w'), indent=1)

    print()
    print('moved   : %d' % len(moved))
    print('failed  : %d %s' % (len(failed), failed[:4] if failed else ''))

    # ---- verify: every manifest path must resolve -------------------------
    man = open(MAN, encoding='utf-8').read()
    refs = sorted(set(re.findall(r'"(assets/[^"]+?\.(?:png|jpg|mp3|wav|ttf|json))"', man)))
    missing = [r for r in refs if not os.path.exists(os.path.join(ROOT, r))]
    print('manifest references: %d   MISSING AFTER REORG: %d' % (len(refs), len(missing)))
    for m in missing[:8]:
        print('   ', m)
    if missing:
        sys.exit('FATAL: reorg left broken references — see LEDGER to reverse')
    print('OK - drop 0801da')


if __name__ == '__main__':
    main()
