#!/usr/bin/env python3
"""
atlas_repack_0903.py - ONE NAMED SHEET PER THING, and nothing live left behind.

    python _BUILD_SOURCE/atlas_repack_0903.py --plan      # classify, report, write contact sheets; touch nothing
    python _BUILD_SOURCE/atlas_repack_0903.py --write     # pack sheets, rewrite manifest + PRELOAD, verify pixels

Mike (0902/0903): "all stage 1 enemies, stage 2, stage 3 get their own atlas's. every boss and mini
boss get their own atlas sheet. all fx's like clouds, lightning, rain get their own atlas. all player
weapon projectiles get their own atlas. all player boxes, pills, weapon pick up icons and specials
get their own atlas. all enemy projectiles per stage get their own atlas sheet... Then, delete old
atlas's that no longer serve purposes or graphics we're never going to use. Do not confuse this with
recent generations."

WHAT WENT WRONG LAST TIME (0903a, reverted): cells were repointed at new sheets in one write and the
sheets were registered in BOFX.img in a LATER write. In between, every boot/menu cell resolved to
nothing. This script produces the sheets, the cell table, the img registrations and the PRELOAD
patch from ONE plan and writes the manifest ONCE. It then re-reads every live cell from the new
sheet and compares the pixels with the old sheet, key by key, before the manifest is touched.

HOW A KEY IS PLACED (first rule that fires wins):
  1. the game's own tables: SHIPBOSS hull keys -> the boss/miniboss sheet of the stage that fields
     that kind; ENEMY_ART bases of the types each stage's plan actually spawns -> that stage's sheet;
     VAULT_AIR_STAGE (the per-stage airframe pools) -> that stage's sheet.
  2. an explicit family map for UI, pilots, fonts, terrain, player weapons, pickups, fx, debris.
  3. the live-run audit (docs/proofs/atlas_keyuse_0903.json): a family drawn only during one stage's
     waves is that stage's; drawn under several stages -> shared.
  4. anything else -> misc (kept, lazily loaded). Nothing live is dropped for being unclassified.

WHAT IS QUARANTINED (removed from the shipped manifest, listed in docs/ATLAS_QUARANTINE_0903.json with
the commit the pixels can be restored from):
  - the retired mech/modular/sectional boss rigs: no STAGES/SUBBOSS kind routes to mechInit,
    MEGABOSS, MINIBOSS or the sectional packs any more (spawnBoss is table-driven; measured 0903).
  - families with NO reference of any kind: no quoted prefix in game.js in any quote style, no
    manifest-table mention, no exact key literal, not drawn in either live-run audit, and not the
    one known dynamic idiom (the debris library: ramp+type+chunk+'_r'+rot+'_'+tier).
  Small doubtful families are KEPT in misc rather than quarantined - the saving is not worth a blank.

SHEET INDEX IS A NAME NOW. BOFX.cells rows are [sheet, x, y, w, h] and the loader resolves the sheet
as 'nca_'+sheet, so a row of ['en_s1', ...] reads assets/game/atlas/en_s1.png through the img key
'nca_en_s1'. 'nca_s1combatfx' already used this route, so no loader change is needed.
"""
import io, os, re, sys, json, math, struct, subprocess, collections, bisect
ROOT = os.path.dirname(os.path.abspath(__file__)); GAME = os.path.abspath(os.path.join(ROOT, '..'))
os.chdir(GAME)
MANIFEST = 'assets/manifest.js'; GAMEJS = 'assets/game.js'; ATLAS = 'assets/game/atlas'
OUTDOC = 'docs/proofs/atlas_repack_0903'; os.makedirs(OUTDOC, exist_ok=True)
WRITE = '--write' in sys.argv
MAXW = 4096; MAXH = 4096; PAD = 2
KEEP_SHEETS = {87, 88, 89}   # nca_87 is indexed WHOLE by the MG pack (P87_SHEET); 88/89 are its siblings. Untouched.
BT = '\x60'                  # a backtick, kept out of the source so shells never see one

# ------------------------------------------------------------------ load
man = io.open(MANIFEST, 'rb').read()
mi = man.find(b'window.BOFX='); ms = mi + len(b'window.BOFX=')
depth = 0; me = ms
while True:
    c = man[me:me+1]
    if c in (b'{', b'['): depth += 1
    elif c in (b'}', b']'):
        depth -= 1
        if depth == 0: break
    me += 1
BOFX = json.loads(man[ms:me+1].decode('utf-8'))
PRE, POST = man[:ms], man[me+1:]
img, cells = BOFX['img'], BOFX['cells']
game = io.open(GAMEJS, encoding='utf-8', errors='ignore').read()
man_tables = (man[:ms] + man[me+1:]).decode('utf-8', 'ignore') + json.dumps({k: v for k, v in BOFX.items() if k not in ('img', 'cells')})
IDX = json.load(open('assets/data/ART_INDEX_SOURCE_0903.json', encoding='utf-8'))
PLAN = json.load(open('assets/data/STAGE_PLAN_TYPES_0903.json', encoding='utf-8'))
def loadaudit(p):
    try:
        j = json.load(open(p, encoding='utf-8'))
        return j.get('use', j)
    except Exception:
        return {}
AUD = loadaudit('docs/proofs/atlas_keyuse_0903.json'); AUD2 = loadaudit('docs/proofs/atlas_keyuse_0902.json')
def audit_tags(k):
    return set(AUD.get(k, {}).get('s', {}).keys()) | set(AUD2.get(k, {}).get('s', {}).keys())
# numeric sheet index -> file (79 is stage1roster.png, not nca_79.png - resolve by registration, never by name)
SRCPATH = {i: img.get('nca_%d' % i) for i in range(0, 90)}

def pngsize(p):
    with open(p, 'rb') as f: h = f.read(32)
    return struct.unpack('>II', h[16:24])
def famof(k):
    m = re.match(r'^([A-Za-z]+[0-9]*[a-z]*)_', k); return m.group(1) if m else re.match(r'^([A-Za-z]+)', k).group(1)

# ------------------------------------------------------------------ the game's tables
STAGES = {s['n']: s['boss'] for s in IDX['STAGES']}
SUBB = {int(k): v['kind'] for k, v in IDX['SUBBOSS'].items() if isinstance(v, dict) and v.get('kind')}
SHIPBOSS = IDX['SHIPBOSS']; ENEMY_ART = IDX['ENEMY_ART']
KIND_STAGE = {}
for n, k in STAGES.items(): KIND_STAGE[k] = ('boss', n)
for n, k in SUBB.items(): KIND_STAGE[k] = ('mini', n)
KEY_GROUP = {}            # exact key -> group (tier 1)
for kind, d in SHIPBOSS.items():
    if not isinstance(d, dict) or kind not in KIND_STAGE: continue
    role, n = KIND_STAGE[kind]; g = '%s_s%d' % (role, n)
    for kk in [d.get('key')] + list(d.get('dmg') or []):
        if kk: KEY_GROUP[kk] = g
# stage-9: the fusion boss is the tidal + warp pair; the rift wardens mini uses the warp sentinel plates
for kk in ['ns9_tidal_intact', 'ns9_tidal_damaged', 'ns9_tidal_critical']: KEY_GROUP[kk] = 'boss_s9'
for kk in ['ns9_warpsen_intact', 'ns9_warpsen_damaged', 'ns9_warpsen_critical', 'ns9_warden']: KEY_GROUP[kk] = 'mini_s9'
# ENEMY_ART bases of the types each stage's plan spawns -> that stage
BASE_STAGE = {}
for n, pl in PLAN.items():
    for t in pl['types']:
        b = ENEMY_ART.get(t)
        if b: BASE_STAGE.setdefault(b, set()).add(int(n))
# VAULT_AIR_STAGE: the per-stage airframe pools (game.js, drop 0719b) - read from the source so it cannot drift
VAULT = {}
mv = re.search(r'const VAULT_AIR_STAGE=\{(.*?)\n\};', game, re.S)
if mv:
    for st, lst in re.findall(r'\n\s*(\d):\[(.*?)\]', mv.group(1), re.S):
        for key in re.findall(r"'([A-Za-z0-9_]+)'", lst): VAULT[key] = int(st)
# the SHIPBOSS 'proj' families per stage (bfx_<fam>_), plus bossVisualFamily's per-stage fallback
PROJ_STAGE = collections.defaultdict(set)
for kind, d in SHIPBOSS.items():
    if isinstance(d, dict) and d.get('proj') and kind in KIND_STAGE: PROJ_STAGE[d['proj']].add(KIND_STAGE[kind][1])
for n, f in {1: 'warhawk', 2: 'magma', 3: 'cryo', 4: 'mirv', 5: 'rampart', 6: 'storm', 7: 'toxic', 8: 'sludge', 9: 'cyclone'}.items(): PROJ_STAGE[f].add(n)

# ------------------------------------------------------------------ explicit family map (tier 2)
def P(*ps): return lambda k: any(k.startswith(p) for p in ps)
def RX(r):
    rr = re.compile(r); return lambda k: bool(rr.match(k))
FAMILY_RULES = [
  # --- retired rigs: unreachable by any live kind (spawnBoss routing measured 0903) ---
  # the twelve mech rigs Mike scrapped (0810q) or never assigned, the Colossus arena pieces (nqm/nqv), the
  # loose mech gun set (mgx) - no STAGES/SUBBOSS kind reaches mechInit, measured 0903
  ('quarantine_retired_rigs', RX(r'^(mbg2|mbg3|mbg3f|mbo2|mbm4|mbw4|mbl5|mbr5|mbc6|mbs6|mbs7|mbt7|mba|nqm_|nqv_|mgx_)')),
  # RETIRED BUT KEPT, on one lazy sheet, for Mike to delete with his eyes on the contact sheet: the sectional
  # packs (CLAUDE.md: "the sectional rig stays on disk"), the unassigned quad-laser, the megaboss/miniboss
  # hulls and the vault/ironrev modular sets. The suite still pins their registration (sections 104/105/136,
  # 160/190/202, the megaboss and esB fixtures); nothing in a stage can spawn them.
  ('retired_rigs', RX(r'^(nsx_|nobd_|nglr_|nlgt_|nmrv_|nslc_|nrmp_|ntxl_|ncyc_|nqx_|nql_|bz[0-6]_|esB_|mbp_|mbv_)')),
  ('quarantine_retired_rigs', RX(r'^nfx_(cycloneinterceptorcarrier|stormsovereign|legioncommandtank|rampartzero|mirvstalker|warhawkarsenal|glacierrailfortress|obsidiandrilltank)_')),
  # gravity mode's four weapon reels predate bof_gravity_mode_space_weapons; no quoted sub-prefix, never drawn
  ('quarantine_retired_rigs', RX(r'^ngm_(judge|titan|storm|doom)_')),
  # --- stage-owned enemy art the tables do not name but the code builds ('n6x_'+kind, 'nvl_'+art, the stage-1 roster camo) ---
  ('en_s6',    P('n6x_', 'n6e_', 'n6w_')),      # n6e sky units / n6w Tempest Missile Wall: registered, suite-pinned, not yet wired
  ('en_s2',    P('nvl_')),
  ('en_s1',    P('s1_', 'tk1_')),
  ('en_s4',    P('tk0_', 'tk2_', 'tk3_')),
  ('en_shared', P('tk4_')),
  ('eproj_s9', P('nep_', 'nbp_')),
  # --- UI ---
  ('ui_menu',     P('btn_', 'nms_', 'nbt_', 'nsel_', 'diff_', 'nbl_', 'cf_', 'cfic_', 'cfui_', 'bootimage', 'statscreen', 'menu', 'startile', 'newbootimage', 'scard_')),
  ('ui_hud',      P('nui_', 'nhud_', 'hud_', 'nbb_', 'nmb_', 'shield_', 'nequipbox', 'special_', 'pbar_', 'nsw_icon_', 'nli_', 'nmi_', 'firewall_', 'laser_', 'ice_', 'iceorb', 'mg_icon', 'spread_icon', 'missile_icon', 'nobj_', 'nwarn_', 'alert_', 'nbret_', 'retm', 'cole_', 'nanc_', 'bar_', 'nsp_box', 'nlz_', 'nuo_', 'homing_')),
  ('ui_dialogue', P('dlg_', 'port_', 'face_')),
  ('ui_map',      P('ncm_', 'nss_', 'map')),
  ('pilots',      P('pcard_', 'pemb_', 'card_', 'pose_', 'sp_', 'aintro_', 'nthp_', 'nsw_box_')),
  ('fonts',       RX(r'^(sfont|g\d|stagefont|bof_font|font)')),
  ('cinematic',   P('cut_', 'nchgF_')),
  # --- player weapons & specials (projectiles, charge, helix, flamethrower, orbs, shards, muzzles) ---
  ('player_weapons', P('nhxv_', 'nhxsb_', 'nhxs_', 'nhxfi_', 'nhxm_', 'nmvh', 'nfw_', 'nibr_', 'lzr_', 'chain_', 'aorb_', 'fllaser', 'flspread', 'fburst', 'nchp_', 'nchg_', 'fchg', 'forb_', 'florb_', 'fball_', 'nfdb_', 'fshard_', 'ashard_', 'nrb_', 'nrbfi_', 'nhb_', 'ndk_', 'beam_', 'eglaser', 'eglR', 'alaser', 'mslB_', 'msl_', 'nmsl', 'nmg_', 'nmgv_', 'pmg_', 'pmgc_', 'mgmuz_', 'spr_', 'nsp_', 'iceshard', 'nfb_', 'nsf_', 'nchl_', 'nch_', 'nspk_', 'nspark_', 'nring_', 'nchunk_', 'nanc', 'nib_', 'nx_small_')),
  # --- pickups / boxes / pills / icons ---
  ('pickups',     P('crate', 'pwr_', 'pill', 'missilebox', 'missilecrate', 'nia_', 'item_', 'pw_', 'nbox_', 'npu_', 'pu_')),
  # --- fx ---
  ('fx_weather',  P('nsd_', 'ncl_', 'nl6c_', 'nwf_', 'ncl6_', 'n6e_', 'n6w_', 'nsky6', 'nl6sky', 'bg6_', 'fx_icewater', 'fx_water', 'fx_lava', 'lavafall', 'waterfall')),
  ('fx_explosions', P('nxp_', 'nx_', 'nck_', 'ntr_', 'nmz_', 'nsr_', 'ndbr_', 'mexh', 'smk_', 'nts_', 'ngm_')),
  ('fx_debris',   RX(r'^(olive|khaki|steel|bossgr|slate|navy|gunmet|bossbl)(tank|jet|boat|boss)\d+_r')),
  ('fx_misc',     P('nfx_', 'nthr')),
  # --- terrain ---
  ('terrain_liquids', P('nwl_', 'nlf_', 'nlq_', 'nlq2_', 'nlqf_', 'tflat_', 'terr_')),
  ('terrain_props',   P('nrs_', 'nst4b_', 'ncon_', 'nrun', 'runway', 'np5_', 'npo_', 'norb5', 'ntur_', 'nspd_', 'nbs_', 'nchx_', 'nob_', 'jungle800')),
  ('terrain_masters', RX(r'^(nst\d|lvl\d|nl8_|bg5_|nl6_)')),
  # --- boss-side art the tables do not name but the stage does ---
  ('boss_s1',  P('ovrotor', 'ovbody', 'mlaunch', 'ndam_', 'chopper_')),
  ('boss_s6',  P('n6bc_', 'nsb_dcarrmk2_', 'nsb_doomsdaycarrier_')),
  ('boss_s8',  P('s8symboss_', 'nvx_')),
  ('eproj_s8', P('nev_')),
  ('mini_s8',  P('nhd_')),
  ('en_s5',    P('nel_')),
  ('en_s7',    P('nsw_')),
  ('en_s9',    P('ns9_', 'ns9e_', 'ns9c_')),
]
def proj_group(k):
    if k.startswith('bfx_'):
        fam = k.split('_')[1]; st = PROJ_STAGE.get(fam, set())
        return ('eproj_s%d' % min(st)) if len(st) == 1 else 'eproj_shared'
    return None

OWNER_HINT = [   # function-name regex -> kind, used only for audit-scoped unknowns
  (r'drawBullets|drawFireType|eShoot|eTwinGuns|_bossProjKey|coleTriDraw|pelletKey|eaCometKey|droneCannonDraw', 'eproj'),
  (r'explode|_drawEffectsInner|nadeBlast|hitBoss|hitSubBoss|drawSmokeTrails|spawnShockRing', 'fx'),
]
fpos = sorted([(m.start(), m.group(1) or m.group(2)) for m in re.finditer(r'\n(?:function\s+([A-Za-z0-9_$]+)\s*\(|const\s+([A-Z][A-Z0-9_]+)\s*=)', game)])
_fs = [p for p, _ in fpos]
def owner(pos):
    i = bisect.bisect_right(_fs, pos) - 1; return fpos[i][1] if i >= 0 else '?'
QUOTE = "['\"" + BT + "]"
def family_owners(f):
    return {owner(m.start()) for m in re.finditer(QUOTE + re.escape(f) + "(_|" + QUOTE + ")", game)}

# ------------------------------------------------------------------ evidence of life, per family
def family_evidence(f, keys):
    ev = set()
    if re.search(QUOTE + re.escape(f) + "(_|" + QUOTE + ")", game): ev.add('code')
    if re.search(r'"' + re.escape(f) + r'[_"]', man_tables): ev.add('table')
    if any(("'" + k + "'") in game or ('"' + k + '"') in game for k in list(keys)[:300]): ev.add('literal')
    if any(audit_tags(k) for k in keys): ev.add('drawn')
    return ev

# ------------------------------------------------------------------ classify
REPACK = {k: c for k, c in cells.items() if isinstance(c[0], int) and c[0] not in KEEP_SHEETS and SRCPATH.get(c[0])}
FAM_KEYS = collections.defaultdict(list)
for k in REPACK: FAM_KEYS[famof(k)].append(k)

def stage_of_tags(tags):
    return {int(m.group(1)) for t in tags for m in [re.match(r'stage(\d)', t)] if m}
_fam_stage_cache = {}
def classify(k):
    if k in KEY_GROUP: return KEY_GROUP[k]
    base = None
    for b in BASE_STAGE:
        if k.startswith(b + '_') and (base is None or len(b) > len(base)): base = b
    if base:
        st = BASE_STAGE[base]; return ('en_s%d' % min(st)) if len(st) == 1 else 'en_shared'
    vb = None
    for b in VAULT:
        if k.startswith(b + '_') and (vb is None or len(b) > len(vb)): vb = b
    if vb: return 'en_s%d' % VAULT[vb]
    if k.startswith('nef_s') and k[5].isdigit(): return 'en_s' + k[5]
    for g, pred in FAMILY_RULES:
        if pred(k): return g
    pg = proj_group(k)
    if pg: return pg
    f = famof(k)
    if f not in _fam_stage_cache:
        tags = set()
        for kk in FAM_KEYS.get(f, ()): tags |= audit_tags(kk)
        st = stage_of_tags(tags)
        own = ' '.join(family_owners(f))
        kind = 'en'
        for rx, kd in OWNER_HINT:
            if re.search(rx, own): kind = kd; break
        if f in ('mfx', 'waf', 'nio', 'nbk', 'mgcf', 'nep', 'nbp', 'ndc'): kind = 'eproj'
        if kind == 'fx': g = 'fx_explosions'
        elif len(st) == 1: g = '%s_s%d' % (kind, min(st))
        elif len(st) > 1: g = kind + '_shared'
        elif kind == 'eproj': g = 'eproj_shared'
        else: g = 'misc'
        _fam_stage_cache[f] = g
    return _fam_stage_cache[f]

# loose manifest PNGs folded into sheets: live boss hulls, the stage-9 pack, pilot intros, stage-6 cloud plates,
# stage-5 planets, the warp portal reel, the three campaign buttons. Big plates (>2048 on a side) stay loose.
FOLD_RX = re.compile(r'^(nsb_(inferno_reaver|rimewall_|cryo_spear|xenoregent_|dcarrmk2_|magmaward_|olivewarden_|blacksteel)|ndam_|ns9|aintro_|bg6_|bg5_|nfx_wportal_|btn_(continue|load|save))')
FOLD = {}
for k, p in img.items():
    if k in cells or '/atlas/' in p or not p.endswith('.png') or not os.path.exists(p): continue
    if not FOLD_RX.match(k): continue
    w, h = pngsize(p)
    if w > 2048 or h > 2048: continue
    FOLD[k] = p

groups = collections.defaultdict(list)
for k in REPACK: groups[classify(k)].append(k)
for k in FOLD: groups[classify(k)].append(k)

# quarantine by evidence: whole families with none (except the debris library), plus the retired rigs.
# KEEP overrides the evidence rule for authored art the suite pins as registered even though no code draws it
# yet: the stage-6 sky units and missile wall (n6e/n6w), the alternate liquid falls (nlqf), the vile morph fx
# (nvx), Falva's fade-in frames Mike asked for (nhxfi/nrbfi, section 184) and the helix laser plate (nmvh).
KEEP = {'n6e', 'n6w', 'nlqf', 'nvx', 'nhxfi', 'nrbfi', 'nmvh',
        'nsf',                                              # the 60 authored spread-fire frames (5 levels x travel/muzzle/impact x 4)
        'nthr0', 'nthr1', 'nthr2', 'nthr3', 'nthr4', 'nthr5'}  # the six thruster types x 4 frames the suite resolves
QUAR = {}
for f, ks in FAM_KEYS.items():
    if f in KEEP or classify(ks[0]) in ('fx_debris', 'retired_rigs'): continue
    ev = family_evidence(f, ks)
    if not ev:
        area = sum(REPACK[k][3] * REPACK[k][4] for k in ks)
        if area >= 40000 or len(ks) >= 12:     # small doubtful families stay in misc
            QUAR[f] = {'keys': sorted(ks), 'why': 'no code prefix, no manifest table, no key literal, never drawn', 'area': area}
for k in list(REPACK):
    if classify(k).startswith('quarantine_'):
        q = QUAR.setdefault(famof(k), {'keys': [], 'why': 'retired rig: no live STAGES/SUBBOSS kind routes to it', 'area': 0})
        if k not in q['keys']: q['keys'].append(k); q['area'] += REPACK[k][3] * REPACK[k][4]
QK = {k for v in QUAR.values() for k in v['keys']}
for g in list(groups): groups[g] = [k for k in groups[g] if k not in QK]
for g in [g for g in groups if g.startswith('quarantine_') or not groups[g]]: del groups[g]

# ------------------------------------------------------------------ report the plan
def rect_of(k):
    if k in REPACK:
        c = REPACK[k]; return (SRCPATH[c[0]], c[1], c[2], c[3], c[4])
    p = FOLD[k]; w, h = pngsize(p); return (p, 0, 0, w, h)
print('=' * 96); print(' ATLAS REPACK 0903 - PLAN'); print('=' * 96)
print(' repackable cells: %d on sheets 0..86   folded loose files: %d   quarantined keys: %d in %d families' % (len(REPACK), len(FOLD), len(QK), len(QUAR)))
tot_area = 0; rows = []
for g in sorted(groups):
    ks = groups[g]; rects = {rect_of(k) for k in ks}; area = sum(r[3] * r[4] for r in rects); tot_area += area
    rows.append((g, len(ks), len(rects), area))
print(' %-22s %6s %6s %8s  sample' % ('SHEET GROUP', 'keys', 'cells', 'Mpx'))
for g, n, r, a in rows: print(' %-22s %6d %6d %8.2f  %s' % (g, n, r, a / 1e6, ' '.join(sorted(groups[g])[:3])))
print(' %-22s %6d %6d %8.2f' % ('TOTAL', sum(r[1] for r in rows), sum(r[2] for r in rows), tot_area / 1e6))
print('\n QUARANTINE (removed from the shipped manifest; pixels stay in git at the recorded commit):')
for f, v in sorted(QUAR.items(), key=lambda kv: -kv[1]['area']): print('   %-14s %5d keys %8.2f Mpx  %s' % (f, len(v['keys']), v['area'] / 1e6, v['why']))
json.dump({'commit': subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip(),
           'note': 'restore: git checkout <commit> -- assets/game/atlas/nca_<sheet>.png, then re-register the cell rows below',
           'families': {f: {'why': v['why'], 'cells': {k: REPACK[k] for k in v['keys']}} for f, v in QUAR.items()}},
          open('docs/ATLAS_QUARANTINE_0903.json', 'w'), indent=0)
json.dump({g: sorted(ks) for g, ks in groups.items()}, open(os.path.join(OUTDOC, 'plan_groups.json'), 'w'), indent=0)

# ------------------------------------------------------------------ pack
from PIL import Image
def shelf_pack(rects):
    """rects: list of (rect, w, h) -> sheets [{'W','H','items':[(rect,x,y)]}]. Height-sorted shelves on a near-square sheet."""
    rects = sorted(rects, key=lambda r: (-r[2], -r[1]))
    area = sum((w + PAD) * (h + PAD) for _, w, h in rects)
    W = int(min(MAXW, max(256, math.ceil(math.sqrt(area * 1.12) / 64) * 64)))
    W = max(W, max(w for _, w, h in rects) + PAD)
    sheets = []; cur = {'x': 0, 'y': 0, 'rowh': 0, 'items': []}
    for r, w, h in rects:
        if cur['x'] + w + PAD > W: cur['x'] = 0; cur['y'] += cur['rowh'] + PAD; cur['rowh'] = 0
        if cur['y'] + h + PAD > MAXH:
            sheets.append(cur); cur = {'x': 0, 'y': 0, 'rowh': 0, 'items': []}
        cur['items'].append((r, cur['x'], cur['y'])); cur['x'] += w + PAD; cur['rowh'] = max(cur['rowh'], h)
    sheets.append(cur)
    for s in sheets:
        s['W'] = max(x + r[3] for r, x, y in s['items']) + PAD; s['H'] = max(y + r[4] for r, x, y in s['items']) + PAD
    return sheets

_src_cache = collections.OrderedDict()
def src_image(path):
    if path in _src_cache: _src_cache.move_to_end(path); return _src_cache[path]
    im = Image.open(path).convert('RGBA'); _src_cache[path] = im
    while len(_src_cache) > 6: _src_cache.popitem(last=False)
    return im
def sheet_path(name): return '%s/%s.png' % (ATLAS, name)

plan = {}
for g, ks in groups.items():
    byrect = collections.defaultdict(list)
    for k in ks: byrect[rect_of(k)].append(k)
    plan[g] = (shelf_pack([(r, r[3], r[4]) for r in byrect]), byrect)
names = []
for g, (sheets, byrect) in sorted(plan.items()):
    for i, s in enumerate(sheets):
        nm = g if len(sheets) == 1 else '%s_%d' % (g, i); s['name'] = nm; names.append(nm)
        print('   sheet %-22s %4dx%-4d  %5d cells  fill %.0f%%' % (nm, s['W'], s['H'], len(s['items']), 100 * sum(r[3] * r[4] for r, _, _ in s['items']) / (s['W'] * s['H'])))
if not WRITE:
    for f, v in sorted(QUAR.items(), key=lambda kv: -kv[1]['area'])[:40]:
        ks = v['keys'][:48]; cell = 96; cols = 12; rowsn = math.ceil(len(ks) / cols)
        cs = Image.new('RGB', (cols * cell, max(1, rowsn) * cell), (40, 40, 40))
        for i, k in enumerate(ks):
            c = REPACK[k]; im = src_image(SRCPATH[c[0]]).crop((c[1], c[2], c[1] + c[3], c[2] + c[4]))
            im.thumbnail((cell - 4, cell - 4)); bg = Image.new('RGBA', (cell, cell), (60, 60, 60, 255)); bg.paste(im, ((cell - im.width) // 2, (cell - im.height) // 2), im)
            cs.paste(bg.convert('RGB'), ((i % cols) * cell, (i // cols) * cell))
        cs.save(os.path.join(OUTDOC, 'quarantine_%s.jpg' % f), quality=80)
    print('\n DRY RUN - nothing written. Contact sheets of the quarantine are in %s. Re-run with --write.' % OUTDOC)
    sys.exit(0)

# ------------------------------------------------------------------ write sheets
newcells = {}; newimg = {}; written = []
for g, (sheets, byrect) in sorted(plan.items()):
    for s in sheets:
        nm = s['name']; im = Image.new('RGBA', (s['W'], s['H']), (0, 0, 0, 0))
        for r, x, y in s['items']:
            src, sx, sy, w, h = r
            im.paste(src_image(src).crop((sx, sy, sx + w, sy + h)), (x, y))
            for k in byrect[r]: newcells[k] = [nm, x, y, w, h]
        out = sheet_path(nm); im.save(out, optimize=True); written.append(out)
        newimg['nca_' + nm] = out
        print('   wrote %-44s %6.2f MB' % (out, os.path.getsize(out) / 1048576), flush=True)

# ------------------------------------------------------------------ verify pixels: every live key, old vs new, BEFORE the manifest moves
import numpy as np
bad = 0; checked = 0
for nm in names:
    arr = np.asarray(Image.open(sheet_path(nm)).convert('RGBA'))
    for k, c in newcells.items():
        if c[0] != nm: continue
        src, sx, sy, w, h = rect_of(k)
        old = np.asarray(src_image(src).crop((sx, sy, sx + w, sy + h)))
        if not np.array_equal(old, arr[c[2]:c[2] + h, c[1]:c[1] + w]): bad += 1; print('   !! PIXEL MISMATCH', k)
        checked += 1
print(' pixel identity: %d cells checked, %d mismatches' % (checked, bad))
if bad: print(' ABORT: sheets written but manifest NOT touched'); sys.exit(2)

# ------------------------------------------------------------------ rewrite the manifest ONCE
for k in QK: cells.pop(k, None); img.pop(k, None)
for k, c in newcells.items():
    cells[k] = c; img[k] = sheet_path(c[0])
for k, p in newimg.items(): img[k] = p
for i in range(0, 87):
    if SRCPATH.get(i) and SRCPATH[i].endswith('/nca_%d.png' % i): img.pop('nca_%d' % i, None)
body = json.dumps(BOFX, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
io.open(MANIFEST, 'wb').write(PRE + body + POST)
print(' manifest rewritten: %d cells, %d img entries' % (len(cells), len(img)))

# ------------------------------------------------------------------ PRELOAD: the stage-1 roster sheets are eager (drop 0809l); name the new ones
g = io.open(GAMEJS, 'rb').read()
roster = sorted({newcells[k][0] for k in newcells if k.startswith('nef_s1_')})
old = b'nca_(?:s1combatfx|8[0-2]|86|8[7-9])'
new = ('nca_(?:s1combatfx|%s|8[7-9])' % '|'.join(re.escape(r) for r in roster)).encode()
assert g.count(old) == 1, 'PRELOAD anchor not found exactly once'
g = g.replace(old, new); io.open(GAMEJS, 'wb').write(g)
print(' PRELOAD now eager on: %s' % ', '.join(roster))

# ------------------------------------------------------------------ retire the numeric sheets (87..89 stay; 79 is stage1roster.png and stays)
freed = 0
for i in range(0, 87):
    p = SRCPATH.get(i)
    if p and p.endswith('/nca_%d.png' % i) and os.path.exists(p): freed += os.path.getsize(p); os.remove(p)
print(' removed nca_0..86: %.1f MB;  new sheets: %.1f MB in %d files' % (freed / 1048576, sum(os.path.getsize(p) for p in written) / 1048576, len(written)))
