#!/usr/bin/env python3
"""
build_atlases.py — ONE LABELLED SHEET PER THING THAT MATTERS.

Mike, 0819e: "make an atlas of every stage's enemy roster including mini bosses ... all current
used projectiles from enemies onto one atlas ... all jets/pilots and their frames+roll frames on
one giant atlas. All properly named. We have to do this for the game as theyre too many atlases
with bogus frames on them."

WHAT THIS IS, AND WHAT IT IS NOT
  It builds REFERENCE sheets, not runtime atlases. Nothing here is loaded by the game and nothing
  is repointed at it — the game keeps drawing from the manifest exactly as before. The value is
  that every sheet is built from the LIVE tables (what buildStagePlan actually spawns, what SUBBOSS
  and STAGES actually name, what PROJ/FIRETYPES actually fire), so a frame that no longer belongs
  to anything simply does not appear, and a spawn type whose art cannot be resolved is printed in
  an UNRESOLVED strip instead of being quietly dropped.

  That last part is the point. "Too many atlases with bogus frames" is not fixed by drawing a
  prettier grid; it is fixed by making the gap between "what ships" and "what is used" visible.

WHY THE SOURCE OF TRUTH IS game.js AND NOT A HAND LIST
  Every hand-maintained list in this project has drifted (see CLAUDE.md on _DELETE, on the stage-4
  waves that named units that could not spawn, on ARSENAL_DRONES). These sheets are regenerated
  from the code, so they cannot drift: rerun it after a roster change and the sheet is current.

  python _BUILD_SOURCE/build_atlases.py            -> docs/atlases/*.png
"""
import io, os, re, sys, json, collections

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("needs Pillow:  pip install pillow"); sys.exit(1)

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
OUT  = os.path.join(GAME, 'docs', 'atlases')
os.makedirs(OUT, exist_ok=True)

MAN = io.open(os.path.join(GAME, 'assets', 'manifest.js'), encoding='utf-8', errors='replace').read()
SRC = io.open(os.path.join(GAME, 'assets', 'game.js'),     encoding='utf-8', errors='replace').read()

# ---------------------------------------------------------------- manifest
_rect = {}
for m in re.finditer(r'"([A-Za-z0-9_]+)"\s*:\s*\[([0-9,\s]+)\]', MAN):
    _rect[m.group(1)] = [int(v) for v in m.group(2).split(',')]
_file = {}
for m in re.finditer(r'"([A-Za-z0-9_]+)"\s*:\s*"([^"]+\.png)"', MAN):
    _file[m.group(1)] = m.group(2)
ALL_KEYS = set(_rect) | set(_file)
_sheets = {}

def sheet_path_for(key):
    """⚠ A KEY CAN CARRY A RECT AND NO FILE. Those rects are [sheetIndex, x, y, w, h] and the index
       IS the atlas number — `nef_s1_jungle_tank_intact` sits at index 86, i.e. atlas/nca_86.png.
       CLAUDE.md records the five-element shape (0813e, where reading them as [x,y,w,h] made every
       rect None); what it does not say is that the index resolves by NAME, which is why the first
       cut of this script rendered every roster cell as MISSING."""
    f = _file.get(key)
    if f: return f
    r = _rect.get(key)
    if r and len(r) >= 5:
        cand = os.path.join('assets', 'game', 'atlas', f'nca_{r[0]}.png')
        if os.path.exists(os.path.join(GAME, cand)): return cand
    # ⚠ SOME ART IS NOT IN THE MANIFEST AT ALL AND LOADS BY PATH CONVENTION. `nsb_jungle_cruiser`
    # — stage 1's miniboss — has ZERO manifest entries and yet serves 200 in play, because the
    # loader falls back to assets/game/<key>.png. Anything resolved only this way is invisible to
    # every manifest-based audit in the project, which is its own answer to "why are there frames
    # nobody can account for".
    cand = os.path.join('assets', 'game', key + '.png')
    if os.path.exists(os.path.join(GAME, cand)): return cand
    return None

def cell(key):
    """the image for one manifest key, or None. Handles whole-file keys and packed rects."""
    f = sheet_path_for(key)
    if not f: return None
    p = os.path.join(GAME, f)
    if not os.path.exists(p): return None
    im = _sheets.get(p)
    if im is None:
        try: im = Image.open(p).convert('RGBA')
        except Exception: return None
        _sheets[p] = im
    r = _rect.get(key)
    if not r: return im
    # rects appear as [sheet,x,y,w,h] and as [x,y,w,h,...]; take the last four that fit the sheet
    for cand in ([r[1:5]] if len(r) >= 5 else []) + ([r[0:4]] if len(r) >= 4 else []):
        x, y, w, h = cand
        if w > 0 and h > 0 and x >= 0 and y >= 0 and x + w <= im.width and y + h <= im.height:
            return im.crop((x, y, x + w, y + h))
    return im

def frames_of(base, limit=8):
    """base_0, base_1 ... as far as they exist; else the bare key."""
    out = [k for k in (f'{base}_{i}' for i in range(limit)) if k in ALL_KEYS]
    if not out and base in ALL_KEYS: out = [base]
    return out

# ---------------------------------------------------------------- live tables
def table(name):
    """parse `const NAME={...}` into {key: rowtext} without evaluating it"""
    m = re.search(r'const\s+' + name + r'\s*=\s*\{', SRC)
    if not m: return {}
    i = m.end() - 1; d = 0
    for j in range(i, len(SRC)):
        if SRC[j] == '{': d += 1
        elif SRC[j] == '}':
            d -= 1
            if d == 0: body = SRC[i+1:j]; break
    else: return {}
    rows, depth, cur, key = {}, 0, '', None
    for part in re.finditer(r'([A-Za-z0-9_]+)\s*:\s*\{([^{}]*)\}', body):
        rows[part.group(1)] = part.group(2)
    return rows

NEF = {}
for t in ('NEF_S1', 'NEF_S2', 'NEF_S3'):
    NEF.update(table(t))
S1_JETS  = table('S1_JETS')
VOLC     = table('VOLC')
SEWER    = table('SEWER')
SHIPBOSS = table('SHIPBOSS')

def art_of(kind):
    """resolve a spawn type to its art base, the way the engine's own tables do"""
    for src in (NEF, S1_JETS):
        if kind in src:
            m = re.search(r"art\s*:\s*'([A-Za-z0-9_]+)'", src[kind])
            if m: return m.group(1)
    if kind in VOLC:
        m = re.search(r"art\s*:\s*'([A-Za-z0-9_]+)'", VOLC[kind])
        if m: return 'nvl_' + m.group(1)
    if kind in SEWER:
        m = re.search(r"art\s*:\s*'([A-Za-z0-9_]+)'", SEWER[kind])
        if m: return 'nsw_' + m.group(1)
    if kind in SHIPBOSS:
        m = re.search(r"key\s*:\s*'([A-Za-z0-9_]+)'", SHIPBOSS[kind])
        if m: return m.group(1)
    return None

# the legacy bosses do not go through SHIPBOSS at all — spawnBoss switches on the name and draws a
# hand-picked plate (CLAUDE.md: "damkeeper -> ovbody_intact"). Mapped explicitly so the roster
# sheets show the boss the stage actually fields rather than an empty cell.
LEGACY_BOSS_ART = {'damkeeper': 'ovbody_intact'}

def keys_for(kind):
    """the frames to SHOW for a spawn type: the damage-state art if it has it, else the reel"""
    if kind in LEGACY_BOSS_ART:
        k = LEGACY_BOSS_ART[kind]
        if k in ALL_KEYS or sheet_path_for(k): return [k], k
    base = art_of(kind)
    tries = []
    if base:
        tries += [base + '_intact', base + '_idle', base]
        tries += [base + '_' + s for s in ('0', '00')]
    tries += [kind, 'nvl_' + kind + '_0', 'nsb_' + kind, kind + '_0']
    for t in tries:
        if t in ALL_KEYS or sheet_path_for(t): return [t], base
    if base:
        f = frames_of(base, 3)
        if f: return f[:1], base
    # ⚠ BOSS AND MINIBOSS KEYS ARE SNAKE_CASED AND THE SPAWN NAMES ARE NOT. `magmaward` is stored as
    # `nsb_magmaward_*` but `junglecruiser` would be `nsb_jungle_cruiser` — the two conventions live
    # side by side, which is the same class of mismatch 0811l fixed for the jet roster with
    # rosterKey(). Compared with underscores stripped so both spellings resolve.
    flat = kind.replace('_', '').lower()
    for suf in ('_intact', '_idle', '_0', ''):
        hit = sorted(k for k in ALL_KEYS
                     if flat in k.replace('_', '').lower() and k.endswith(suf))
        if hit: return [hit[0]], base
    # nothing at all: leave it for the UNRESOLVED strip rather than showing a wrong sprite
    return ([], base)

# ---------------------------------------------------------------- sheet drawing
try:    FONT = ImageFont.truetype("consola.ttf", 11)
except Exception: FONT = ImageFont.load_default()
try:    FONT_B = ImageFont.truetype("consolab.ttf", 15)
except Exception: FONT_B = FONT

BG, FG, DIM, WARN = (14, 15, 20), (232, 238, 248), (128, 140, 160), (255, 150, 90)

def sheet(title, groups, path, cellw=118, cellh=118, cols=None):
    """groups: [(heading, [(label, PIL image or None), ...]), ...]"""
    pad, head, lab = 14, 30, 26
    cols = cols or 10
    rows_total, blocks = 0, []
    for name, items in groups:
        r = max(1, (len(items) + cols - 1) // cols)
        blocks.append((name, items, r)); rows_total += r
    W = pad * 2 + cols * cellw
    H = pad * 2 + 44 + sum(head + r * (cellh + lab) for _, _, r in blocks)
    img = Image.new('RGBA', (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    d.text((pad, pad), title, font=FONT_B, fill=FG)
    d.line([(pad, pad + 26), (W - pad, pad + 26)], fill=(70, 80, 100), width=1)
    y = pad + 44
    for name, items, r in blocks:
        d.text((pad, y + 8), name, font=FONT_B, fill=(150, 200, 255))
        y += head
        for n, (label, im) in enumerate(items):
            cx = pad + (n % cols) * cellw
            cy = y + (n // cols) * (cellh + lab)
            d.rectangle([cx, cy, cx + cellw - 6, cy + cellh - 6], outline=(46, 52, 66))
            if im is not None:
                g = im.copy()
                g.thumbnail((cellw - 18, cellh - 18), Image.NEAREST)
                img.alpha_composite(g, (cx + (cellw - 6 - g.width) // 2,
                                        cy + (cellh - 6 - g.height) // 2))
            else:
                d.text((cx + 8, cy + cellh // 2 - 8), 'MISSING', font=FONT, fill=WARN)
            t = label if len(label) <= 18 else label[:17] + '…'
            d.text((cx + 3, cy + cellh - 3), t, font=FONT, fill=DIM)
        y += r * (cellh + lab)
    img.convert('RGB').save(path)
    print('  wrote', os.path.relpath(path, GAME), f'({img.width}x{img.height})')

# ---------------------------------------------------------------- rosters from the live plan
i = SRC.index('function buildStagePlan')
BODY = SRC[i:i + 220000]
marks = sorted([(int(m.group(1)), m.start()) for m in re.finditer(r'if\(stageNum===(\d)\)\{', BODY)],
               key=lambda t: t[1])
ARMS = {}
for n, (st, pos) in enumerate(marks):
    ARMS[st] = BODY[pos: marks[n + 1][1] if n + 1 < len(marks) else pos + 40000]
CALL = re.compile(r"(?:spawnEnemy|vRow|aiWaveRush|aiWaveSweep|aiWaveColumns|aiWaveSplit|"
                  r"aiWaveCross|aiWaveLoopCurved|aiAttach)\(\s*'([A-Za-z0-9_]+)'")

m = re.search(r'const SUBBOSS\s*=\s*\{(.*?)\n\}', SRC, re.S)
SUB = dict(re.findall(r"(\d)\s*:\s*\{[^}]*kind\s*:\s*'([A-Za-z0-9_]+)'", m.group(1))) if m else {}
BOSS = re.findall(r"boss:'([a-z0-9_]+)'", SRC)

def build_stage_sheets():
    unresolved_all = []
    for st in range(1, 9):
        kinds = sorted(set(CALL.findall(ARMS.get(st, ''))))
        items, unresolved = [], []
        for k in kinds:
            ks, base = keys_for(k)
            if ks: items.append((k, cell(ks[0])))
            else:  unresolved.append(k)
        groups = [(f'FODDER + WAVE UNITS  ({len(items)} resolved)', items or [('none', None)])]
        mini = SUB.get(str(st))
        if mini:
            ks, _ = keys_for(mini)
            groups.append(('MINIBOSS', [(mini, cell(ks[0]) if ks else None)]))
        if st - 1 < len(BOSS):
            b = BOSS[st - 1]; ks, _ = keys_for(b)
            groups.append(('BOSS', [(b, cell(ks[0]) if ks else None)]))
        if unresolved:
            groups.append(('UNRESOLVED — spawned by the plan, no art found',
                           [(u, None) for u in unresolved]))
            unresolved_all += [f'stage {st}: {u}' for u in unresolved]
        sheet(f'BULLETS OF FURY — STAGE {st} ENEMY ROSTER', groups,
              os.path.join(OUT, f'Stage_{st}_Enemy_Roster.png'))
    return unresolved_all

def build_powerups():
    groups = []
    def grp(name, pat, limit=60):
        ks = sorted(k for k in ALL_KEYS if re.search(pat, k))[:limit]
        if ks: groups.append((f'{name}  ({len(ks)})', [(k, cell(k)) for k in ks]))
    grp('WEAPON ICONS  machine gun / laser / flame / ice / fire / fireice / missile', r'^micon_')
    grp('SPECIAL ABILITY ICONS  (9 pilots)', r'^spicon_')
    grp('POWER-UP BOXES + CRATES', r'(box|crate)', 40)
    grp('SPEED PILLS', r'pill')
    grp('PICKUPS', r'(pickup|pkup|powerup)', 40)
    sheet('BULLETS OF FURY — MASTER POWERUP SHEET', groups,
          os.path.join(OUT, 'Master_PowerUp_Sheet.png'))

def build_projectiles():
    # enemy rounds: whatever PROJ/FIRETYPES actually name
    fam = set()
    for m in re.finditer(r"'(mfx_[a-z]+)_", SRC): fam.add(m.group(1))
    for m in re.finditer(r"'(bfx_magma_[pmi])_", SRC): fam.add(m.group(1))
    egroups = []
    for f in sorted(fam):
        fr = frames_of(f, 8)
        if fr: egroups.append((f, [(k, cell(k)) for k in fr]))
    sheet('BULLETS OF FURY — ENEMY PROJECTILES (all families in use)', egroups,
          os.path.join(OUT, 'Enemy_Projectiles.png'))

    pgroups = []
    for pat, name in ((r'^nwp_', 'PLAYER WEAPON FX'), (r'^nts_', 'THERMOSHOCK'),
                      (r'^nlz_', 'LASER'), (r'^nhxv_p', 'PLAYER ROUNDS'),
                      (r'^waf_', 'WEAPON ART')):
        ks = sorted(k for k in ALL_KEYS if re.search(pat, k))[:60]
        if ks: pgroups.append((f'{name}  ({len(ks)})', [(k, cell(k)) for k in ks]))
    sheet('BULLETS OF FURY — PLAYER PROJECTILES + ATTACK FX', pgroups,
          os.path.join(OUT, 'Player_Projectiles_FX.png'))

def build_pilots():
    pilots = ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']
    groups = []
    for p in pilots:
        ks = sorted(k for k in ALL_KEYS if k.startswith('ship_' + p))
        base = [k for k in ks if k == 'ship_' + p]
        roll = [k for k in ks if '_br' in k]
        rest = [k for k in ks if k not in base and k not in roll]
        row = base + rest + roll
        if row: groups.append((f'{p.upper()}  ({len(row)} frames — hull, banks, roll)',
                               [(k.replace('ship_' + p, '') or 'idle', cell(k)) for k in row]))
    sheet('BULLETS OF FURY — PILOT SHIPS: ALL FRAMES + ROLL FRAMES', groups,
          os.path.join(OUT, 'Pilot_Ships_All_Frames.png'), cellw=104, cellh=104, cols=12)

if __name__ == '__main__':
    print('building reference atlases ->', os.path.relpath(OUT, GAME))
    un = build_stage_sheets()
    build_powerups()
    build_projectiles()
    build_pilots()
    if un:
        print('\nUNRESOLVED spawn types (the plan names them; no art resolved):')
        for u in un: print('   ', u)
    print('\ndone.')
