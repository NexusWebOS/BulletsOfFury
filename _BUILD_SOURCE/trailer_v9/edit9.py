"""edit9.py - cut the v9 Bullets of Fury trailer to CITY IN THE SKY. Writes edl9.json for compose.py and mix9.py.

    python edit9.py            # writes edl9.json and prints the shot report

Mike, 0930: "make a revised trailer thats inspired by this, but uses our city in the sky track. now its 10 levels,
9 pilots, 20 bosses and 1 hell of a campaign ... the normal, hard and furious variants, the level 6 awesome intro
sequence, stage 7's awesome boss fight, stage 6 with the allies, the choice to go left or right, the harrier fight
there, the fury/dog fight at the center of the map, plenty of the level 1 and 2 boss, plenty of level 5 boss, and then
as the song is ending we can fade it out, and fade into Last but not least. Stop? Hammertime? And then cut to the
hama password fight where its at the part where they all do the break down, and he does the Stop! Hammertime! and
then cut to our game logo, 11.1.26. Steam/PC/Mac/Linux. 2026 ColeForge Productions."

The song map (beatmap9.json, measured: 158.4 BPM, 74 bars of 1.515 s):

  pre      ColeForge Phoenix engine plate + the boot chime
  1-2      BULLETS OF FURY slams on the first downbeat
  3-8      10 LEVELS - the text, then all ten stage cards on the half bar (STAGE X filmed live off the map)
  9-18     9 PILOTS - the nine stand in a line, then one bar each on their special
  19-28    20 BOSSES - plenty of the stage 1 Overlord-X and the stage 2 Furnace Tyrant, then the rest on the half bar
  29-34    plenty of the stage 5 Chromium Hammer
  35-40    NORMAL / HARD / FURIOUS - one miniboss, three fights, then all three side by side
  41-48    the stage 6 opening (the energy lifts at bar 41 - the song IS stage 6)
  49-50    the allies, then the choice, in the song's one break
  51-58    the drop: LEFT and RIGHT side by side, then the Harrier and the Rebel Fury traded, then STAGE X at the centre
  59-62    1 HELL OF A CAMPAIGN
  63-70    stage 7's boss fight, at the loudest stretch of the song
  71-73    the Warden's death and the escape through the portal, fading out with the song
  post     LAST BUT NOT LEAST. / STOP? / HAMMERTIME? -> the HAMA breakdown and its STOP / HAMMER / TIME -> the logo card

Mike's standing trailer rules (HANDOFF_CODEX.md) are enforced and reported, not assumed: live in-game footage only;
the game's own sounds under every shot (mix9.py plays each pane's sfx.wav at the pane's own source time); no footage
shown twice (every pane CLAIMS its frames); no pilot on screen twice in a row; pilots' screen time reported; no boss
name cards; full-size view with zooms only on the intense moments. His 0930 request overrides the old "no stage-6
bosses except the Tempest duel" rule: he asked for the Harrier fight and the stage 6 allies by name.
"""
import os, sys, json, math
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TAKES_DIR = os.path.join(HERE, 'takes9')
FPS, W, H = 60, 1920, 1080
PF_W, PF_H = 960, 1024
T0 = 3.2                                   # the pre-roll: the song's first sample lands here
SONG = os.path.join(ROOT, 'assets', 'game', 'music', 'Level6.mp3')
HAMA_SONG = os.path.join(ROOT, 'assets', 'game', 'music', 'HAMA_Instrumental.mp3')
SND = lambda *p: os.path.join(ROOT, 'assets', 'game', *p)

BM = json.load(open(os.path.join(HERE, 'beatmap9.json')))
BEATS = BM['beats']
BEAT = BM['beat_period']
HAMA_BPM, HAMA_PHASE = 132.55, 0.20        # docs/HAMA_0928.md, measured by build_hama_0928.py
HAMA_BEAT = 60.0 / HAMA_BPM

PILOT_TINT = {'axel': '#3a8aff', 'decker': '#ffd24a', 'maverick': '#3ad6c8', 'freezer': '#6fd0ff', 'juggernaut': '#c08a3a',
              'yuri': '#e23a3a', 'lizzie': '#ffc21a', 'falva': '#ff2a8f', 'cole': '#7ad63a'}
PILOTS = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']


def q(t):
    """snap to the 60 fps grid, so a clip edge, a layer and a hit agree on the frame"""
    return round(t * FPS) / FPS


def beat_time(x):
    i = int(math.floor(x))
    fr = x - i
    if i + 1 < len(BEATS):
        return BEATS[i] + (BEATS[i + 1] - BEATS[i]) * fr
    return BEATS[-1] + (x - (len(BEATS) - 1)) * BEAT


def tb(k, beat=0.0):
    """trailer time of bar k (1-based), beat `beat` (may run past 4)"""
    return q(T0 + beat_time((k - 1) * 4 + beat))


# ---- takes ---------------------------------------------------------------------------------------------------------
_M = {}
MISSING = set()


def meta(tid):
    if tid not in _M:
        d = os.path.join(TAKES_DIR, tid)
        try:
            m = json.load(open(os.path.join(d, 'meta.json')))
            m['metrics'] = json.load(open(os.path.join(d, 'metrics.json')))
            # whiteness9.py: the share of white-silhouette pixels per frame, as EXCESS over the take's own median
            # (a modular boss flashes per part, which the 'bf' flag cannot see)
            wp = os.path.join(d, 'white.json')
            if os.path.exists(wp):
                w = json.load(open(wp))
                med = sorted(w)[len(w) // 2] if w else 0.0
                for i, mm in enumerate(m['metrics']):
                    mm['wx'] = max(0.0, (w[i] if i < len(w) else 0.0) - med)
        except (OSError, ValueError):
            m = None
        _M[tid] = m
    return _M[tid]


def have(tid):
    ok = meta(tid) is not None and meta(tid)['frames'] > 0
    if not ok:
        MISSING.add(tid)
    return ok


def nfr(tid):
    return meta(tid)['frames'] if have(tid) else 0


def M(tid):
    return meta(tid)['metrics']


def pilot_of(tid):
    m = meta(tid)
    if not m:
        return None
    sp = m.get('spec') or {}
    if sp.get('kind') == 'menu' and not sp.get('pilot'):
        return None
    return sp.get('pilot')


def first(tid, pred, lo=0, default=None):
    if not have(tid):
        return default
    Ms = M(tid)
    for i in range(max(0, int(lo)), len(Ms)):
        try:
            if pred(Ms[i]):
                return i
        except Exception:
            pass
    return default


def last(tid, pred, default=None):
    if not have(tid):
        return default
    Ms = M(tid)
    for i in range(len(Ms) - 1, -1, -1):
        try:
            if pred(Ms[i]):
                return i
        except Exception:
            pass
    return default


def action(m):
    return (m.get('ex') or 0) * 3 + (m.get('eb') or 0) + (m.get('pb') or 0) * 0.5 + (m.get('sh') or 0) * 2


def boom(m):
    return (m.get('ex') or 0) * 4 + (m.get('sh') or 0) * 6 + (m.get('fl') or 0) * 20


def busy(m):
    return action(m) + (m.get('e') or 0) * 2


def special_score(m):
    return (8 if m.get('sp') else 0) + action(m)


def target_on(m):
    """the boss / miniboss is on screen and well inside it"""
    return 1.0 if (m.get('ty') is not None and 20 <= (m.get('ty') or 0) <= 400 and m.get('tsx') is not None
                   and 60 <= m['tsx'] <= 900) else 0.0


def fight_score(m):
    # bf: the boss is mid hit-flash - a white silhouette - on this frame (capture9's LIB9 logs it)
    return action(m) + 12 * target_on(m) - 9 * (m.get('bf') or 0) - 250 * (m.get('wx') or 0)


def montage_score(m):
    # a half-bar cut has no time to recover from a white frame: the boss must be on screen and in its own colours
    return action(m) + 14 * target_on(m) - 90 * (m.get('bf') or 0) - 400 * (m.get('wx') or 0)


def special_view(m):
    return special_score(m) - 7 * (m.get('bf') or 0) - 150 * (m.get('wx') or 0)


# ---- claims: no frame shown twice ----------------------------------------------------------------------------------
CLAIMS = defaultdict(list)
CONFLICTS = []


def claim(tid, a, b, why=''):
    for (x, y, w) in CLAIMS[tid]:
        if a < y and x < b:
            CONFLICTS.append('%s [%d,%d) overlaps [%d,%d) (%s / %s)' % (tid, a, b, x, y, why, w))
    CLAIMS[tid].append((a, b, why))


def free(tid, a, b):
    return all(not (a < y and x < b) for (x, y, _) in CLAIMS[tid])


DEATH_PEN = 80


def best(tid, n, score=action, lo=0, hi=None, step=3):
    """the start frame of the unclaimed n-frame window with the highest summed score"""
    Ms = M(tid)
    hi = len(Ms) if hi is None else min(len(Ms), int(hi))
    lo = max(0, int(lo))
    if hi - lo < n:
        lo = max(0, hi - n)
    sc = [0.0] + [0.0] * len(Ms)
    for i, m in enumerate(Ms):
        # REAL GAMEPLAY (real9.py): a death spin-out may appear, but never wins a shot on its own
        sc[i + 1] = sc[i] + float(score(m)) - DEATH_PEN * (m.get('dd') or 0)
    bestv, bests = None, None
    for s in range(lo, max(lo + 1, hi - n + 1), step):
        if s + n > len(Ms):
            break
        if not free(tid, s, s + n):
            continue
        v = sc[s + n] - sc[s]
        if bestv is None or v > bestv:
            bestv, bests = v, s
    if bests is None:
        # nothing unclaimed that long - fall back to the latest free start (reported as a conflict if it overlaps)
        bests = max(0, min(len(Ms) - n, lo))
    return bests


# ---- the timeline --------------------------------------------------------------------------------------------------
CLIPS, OVERLAYS, HITS, SFX, SHOTS = [], [], [], [], []
FULL = [0, 0, W, H]


def cam(s0=1.0, s1=None, cx=480, cy=512, track=None, track_x=False, lead=0, ease='out'):
    return {'s0': s0, 's1': s0 if s1 is None else s1, 'ease': ease, 'cx': cx, 'cy': cy, 'track': track,
            'track_x': track_x, 'lead': lead}


def pane(tid, src, speed=1.0, rect=None, c=None, **kw):
    p = {'rect': rect or FULL, 'take': tid, 'src': int(src), 'speed': speed, 'bg': 'blur', 'cam': c or cam()}
    p.update(kw)
    return p


def frames_for(t0, t1, speed=1.0, hold=None):
    dur = (t1 - t0) if hold is None else min(t1 - t0, hold)
    return int(math.ceil(dur * FPS * speed)) + 1


def shot(t0, t1, tid, src=None, speed=1.0, c=None, score=action, lo=0, hi=None, label='', layers=None, gain=None,
         subject='auto', clip_kw=None, cont=False, **pane_kw):
    t0, t1 = q(t0), q(t1)
    if not have(tid):
        CLIPS.append({'t0': t0, 't1': t1, 'panes': [], 'layers': layers or [], 'label': 'MISSING ' + tid})
        return None
    n = frames_for(t0, t1, speed, pane_kw.get('hold'))
    if src is None:
        src = best(tid, n, score, lo, hi)
    src = int(max(0, min(nfr(tid) - n, src)))
    # a continuation picks up on the exact next frame of the shot before it; frames_for's one-frame safety margin would
    # otherwise read as a 2-frame overlap of footage that is in fact shown once
    claim(tid, src + (2 if cont else 0), src + n, label or tid)
    p = pane(tid, src, speed, c=c, **pane_kw)
    if gain is not None:
        p['gain'] = gain
    clip = {'t0': t0, 't1': t1, 'panes': [p], 'layers': layers or [], 'label': label or tid}
    clip.update(clip_kw or {})
    CLIPS.append(clip)
    who = pilot_of(tid) if subject == 'auto' else subject
    SHOTS.append({'t0': t0, 't1': t1, 'pilot': who, 'take': tid, 'src': src, 'label': label or tid, 'cont': cont})
    return src


def split(t0, t1, parts, label='', layers=None, subject=None):
    """side-by-side panes: parts = [(tid, src_or_None, score, cam, gain), ...] laid left to right"""
    t0, t1 = q(t0), q(t1)
    k = len(parts)
    wpx = W // k
    panes = []
    for i, (tid, src, score, c, gain) in enumerate(parts):
        if not have(tid):
            continue
        n = frames_for(t0, t1)
        if src is None:
            src = best(tid, n, score)
        src = int(max(0, min(nfr(tid) - n, src)))
        claim(tid, src, src + n, label or tid)
        p = pane(tid, src, 1.0, rect=[i * wpx, 0, wpx if i < k - 1 else W - i * wpx, H], c=c)
        p['gain'] = gain
        p['border'] = [8, 8, 12]
        panes.append(p)
    CLIPS.append({'t0': t0, 't1': t1, 'panes': panes, 'layers': layers or [], 'label': label})
    SHOTS.append({'t0': t0, 't1': t1, 'pilot': subject, 'take': '+'.join(p['take'] for p in panes), 'src': None, 'label': label})


def black(t0, t1, layers=None, label='', **kw):
    c = {'t0': q(t0), 't1': q(t1), 'panes': [], 'layers': layers or [], 'label': label}
    c.update(kw)
    CLIPS.append(c)
    SHOTS.append({'t0': q(t0), 't1': q(t1), 'pilot': None, 'take': None, 'src': None, 'label': label})


def text(t_in, t_out, s, face='final', height=140, x=W / 2, y=H / 2, tint=None, kin='slam', out='cut', band=None,
         anchor='c', drift=0.0, fade=0.25, fade_out=0.2, overlay=True):
    L = {'kind': 'text', 'text': s, 'face': face, 'height': height, 'x': x, 'y': y, 'anchor': anchor,
         't_in': q(t_in), 't_out': q(t_out), 'in': kin, 'out': out, 'fade': fade, 'fade_out': fade_out, 'drift': drift}
    if tint:
        L['tint'] = tint
    if band:
        L['band'] = band
    if overlay:
        OVERLAYS.append(L)
    return L


def image(t_in, t_out, src, x=W / 2, y=H / 2, prescale=1.0, kin='fade', out='cut', anchor='c', shadow=True,
          resample='lanczos', drift=0.0, fade=0.25, fade_out=0.2, overlay=True):
    L = {'kind': 'image', 'src': src, 'x': x, 'y': y, 'prescale': prescale, 'anchor': anchor, 't_in': q(t_in),
         't_out': q(t_out), 'in': kin, 'out': out, 'shadow': shadow, 'resample': resample, 'drift': drift,
         'fade': fade, 'fade_out': fade_out}
    if overlay:
        OVERLAYS.append(L)
    return L


def hit(t, kind, dur, amp):
    HITS.append({'t': q(t), 'kind': kind, 'dur': dur, 'amp': amp})


def sfx(t, path, gain_db=-8.0, duck_db=None):
    s = {'t': round(t, 4), 'file': path, 'gain_db': gain_db}
    if duck_db:
        s['duck_db'] = duck_db
    SFX.append(s)


def typed(t_in, t_out, s, rate=0.072, **kw):
    """a line typed out a character at a time, the way the game's dialogue types, with the game's own letter tick"""
    tick = SND('sounds', 'dialogue_letter_0924.wav')
    import typeset
    full_w = typeset.text(s, face=kw.get('face', 'final'), height=kw.get('height', 140)).width
    kw = dict(kw, anchor='l', x=W / 2 - full_w / 2)      # left-anchored: the line types out, it does not re-centre
    t = t_in
    shown = ''
    for i, ch in enumerate(s):
        shown += ch
        if ch == ' ':
            continue
        nxt = t_in + rate * (i + 1)
        end = t_out if i == len(s) - 1 else nxt
        text(t, end, shown.rstrip(), kin='cut', out='fade' if i == len(s) - 1 else 'cut', **kw)
        sfx(t, tick, gain_db=-4.0)
        t = nxt
    return t


def body_prescale(p, want_h):
    from PIL import Image
    im = Image.open(os.path.join(HERE, 'brand', 'body_%s.png' % p))
    return want_h / float(im.height)


def pav_prescale(p, want_h):
    from PIL import Image
    im = Image.open(os.path.join(HERE, 'brand', 'pav_%s.png' % p))
    return want_h / float(im.height)


# ====================================================================================================================
#  PRE-ROLL: the ColeForge plate and the boot chime
# ====================================================================================================================
black(0.0, tb(1), label='COLEFORGE + chime',
      layers=[image(0.25, tb(1) - 0.05, 'brand/cf_logo.png', y=530, prescale=0.66, kin='fade', out='fade', fade=0.7,
                    fade_out=0.45, drift=0.012, overlay=False)])
hit(0.55, 'flash', 0.6, 0.12)

# ====================================================================================================================
#  BARS 1-2: BULLETS OF FURY
# ====================================================================================================================
if have('A_title'):
    # framed past the title's own logo (the top ~160 rows) so the slam is the only wordmark on screen
    shot(tb(1), tb(3), 'A_title', src=40, label='BULLETS OF FURY slam', subject=None, desat=0.4, tint=[0, 0, 0, 0.72],
         c=cam(1.25, 1.32, cy=600, ease='inout'),
         layers=[image(tb(1), tb(3), 'brand/bof_logo.png', y=520, prescale=0.80, kin='slam', out='cut', drift=0.02,
                       overlay=False)])
hit(tb(1), 'flash', 0.18, 0.95)
hit(tb(1), 'shake', 0.45, 18)

# ====================================================================================================================
#  BARS 3-8: 10 LEVELS - the claim, then ten stage cards on the half bar
# ====================================================================================================================
shot(tb(3), tb(4), 'C_mapfly', src=10, label='10 LEVELS over the campaign map', subject=None, desat=0.35,
     tint=[0, 0, 0, 0.55], c=cam(1.0, 1.08, ease='inout'))
text(tb(3), tb(4), '10 LEVELS', height=170, y=540, band=0.5)
hit(tb(3), 'flash', 0.14, 0.7)
hit(tb(3), 'punch', 0.25, 0.05)
CARD_TAKES = ['F_card_s%d' % n for n in range(1, 8)] + ['F_card_s8b', 'F_card_s9']
k = 0
for n, tid in enumerate(CARD_TAKES + ['X_rival_map']):
    a, b = tb(4, 2 * k), tb(4, 2 * k + 2)
    k += 1
    if tid == 'X_rival_map':
        # the STAGE X card, drawn live by Rival24's intro after the deploy on the campaign map
        src = first(tid, lambda m: m['st'] == 'intro', default=480)
        shot(a, b, tid, src=src + 25, label='STAGE X card', subject=None, c=cam(1.0, 1.06, ease='inout'))
    else:
        # each card settles on screen by frame ~40 and holds to ~195
        shot(a, b, tid, src=48, label='stage %d card' % (n + 1), subject=None, c=cam(1.28, 1.34, cy=505, ease='inout'))
    hit(a, 'punch', 0.16, 0.035)

# ====================================================================================================================
#  BARS 9-18: 9 PILOTS - the line-up, then one bar each on their special
# ====================================================================================================================
lineup = []
xs = [W * (i + 0.5) / 9 for i in range(9)]
for i, p in enumerate(PILOTS):
    # the pilot-select roster: each pilot's own portrait box over their full-body figure
    lineup.append(image(tb(9, i * 0.25), tb(10), 'brand/body_%s.png' % p, x=xs[i], y=760,
                        prescale=body_prescale(p, 430), kin='rise', out='cut', overlay=False))
    lineup.append(image(tb(9, i * 0.25), tb(10), 'brand/pav_%s.png' % p, x=xs[i], y=420, prescale=0.75,
                        kin='rise', out='cut', resample='nearest', overlay=False))
black(tb(9), tb(10), label='9 PILOTS line-up', layers=lineup + [text(tb(9), tb(10), '9 PILOTS', height=150, y=210,
                                                                      overlay=False)])
hit(tb(9), 'flash', 0.14, 0.75)
PILOT_ORDER = ['cole', 'lizzie', 'juggernaut', 'falva', 'maverick', 'yuri', 'decker', 'freezer', 'axel']
for i, p in enumerate(PILOT_ORDER):
    a, b = tb(10 + i), tb(11 + i)
    tid = 'P_' + p
    if not have(tid):
        continue
    sp0 = first(tid, lambda m: bool(m.get('sp')), default=10)
    # Lizzie's special IS a screen-filling white flash (the atom bomb) - the one take the whiteness penalty must not read
    src_p = best(tid, frames_for(a, b), special_score if p == 'lizzie' else special_view, lo=max(0, sp0 - 8), hi=sp0 + 170)
    lay = [text(a, b, p.upper(), height=120, y=92, tint=PILOT_TINT[p], band=0.55, overlay=False),
           image(a, b, 'brand/body_%s.png' % p, x=240, y=640, prescale=body_prescale(p, 600), kin='slide-l', overlay=False),
           image(a + 0.06, b, 'brand/pav_%s.png' % p, x=1680, y=600, prescale=1.25, kin='slide-r',
                 resample='nearest', overlay=False)]
    shot(a, b, tid, src=src_p, label='%s special' % p, layers=lay, c=cam(1.0, 1.12, track='player', lead=-220))
    hit(a, 'punch', 0.18, 0.04)

# ====================================================================================================================
#  BARS 19-28: 20 BOSSES - plenty of stage 1 and stage 2, then the rest on the half bar
# ====================================================================================================================
# Overlord-X: the dam flyover (it climbs through the player lane over the ship), the whip spin, the gauge fill.
e1 = first('E1_entry', lambda m: m.get('ty') is not None and m['ty'] > 0, default=60)
shot(tb(19), tb(21), 'E1_entry', src=max(0, e1 - 10), label='S1 boss: Overlord-X flyover entrance',
     c=cam(1.0, 1.0), layers=[text(tb(19), tb(20), '20 BOSSES', height=160, y=540, band=0.5, overlay=False)])
hit(tb(19), 'flash', 0.16, 0.85)
hit(tb(19), 'shake', 0.4, 12)
shot(tb(21), tb(22), 'E1_frenzy', score=fight_score, label='S1 boss: Furious four-pass frenzy',
     c=cam(1.0, 1.25, track='target', lead=180))
shot(tb(22), tb(23), 'E2_form', score=lambda m: target_on(m) * 6 + boom(m), hi=700, label='S2 boss: Furnace Tyrant assembles',
     c=cam(1.0, 1.0))
shot(tb(23), tb(24), 'E2_core', score=fight_score, label='S2 boss: the rollerball core', c=cam(1.15, 1.3, track='target', lead=150))
shot(tb(24), tb(24, 2), 'E2_head', score=fight_score, hi=780, label='S2 boss: the head flies alone',
     c=cam(1.3, 1.45, track='target', lead=120))
B_ORDER = ['B_s3b', 'B_s4m', 'B_s8b', 'B_s2m', 'B_s4b', 'B_s7m', 'B_s9b', 'B_s5m', 'B_s3m']   # B_s6m: its miniboss never enters inside the take
for i, tid in enumerate(B_ORDER):
    a, b = tb(24, 2 + 2 * i), tb(24, 4 + 2 * i)
    shot(a, b, tid, score=montage_score, label='boss montage %s' % tid, c=cam(1.0, 1.1, ease='inout'))
    hit(a, 'punch', 0.14, 0.03)

# ====================================================================================================================
#  BARS 29-34: plenty of the stage 5 boss, the Chromium Hammer
# ====================================================================================================================
H_SEQ = [('H_arrive', 'arrival and transformation'), ('H_fight', 'hammer fight'), ('H_yuri', 'Hard: hammer jumps'),
         ('H_furious', 'Furious chromium armour'), ('H_yuri', 'Hard: the slam'), ('H_fight', 'boomerang / spiked ball')]
for i, (tid, what) in enumerate(H_SEQ):
    a, b = tb(29 + i), tb(30 + i)
    lo = 0 if i < 3 else nfr(tid) // 2 if have(tid) else 0
    if tid == 'H_arrive':
        lo = first(tid, lambda m: m.get('ty') is not None and (m.get('ty') or 0) > 40, default=250)
    # the Chromium Hammer is dark armour on a dark nebula; at the full-cabinet view it barely reads, so every shot is on it
    shot(a, b, tid, score=fight_score, lo=lo, label='S5 boss: ' + what,
         c=cam(1.3, 1.42, track='target', lead=150) if i % 2 == 0 else cam(1.42, 1.3, track='target', lead=150))
    hit(a, 'punch', 0.16, 0.035)
hit(tb(29), 'flash', 0.14, 0.6)

# ====================================================================================================================
#  BARS 35-40: NORMAL / HARD / FURIOUS
# ====================================================================================================================
DIFF_LOOK = [('normal', 'NORMAL', '#3a8aff'), ('hard', 'HARD', '#ff8a1c'), ('furious', 'FURIOUS', '#ff2a2a')]
for i, (d, word, col) in enumerate(DIFF_LOOK):
    a, b = tb(35, 6 * i), tb(35, 6 * i + 6)
    tid = 'V_rzb_' + d
    shot(a, b, tid, score=fight_score, hi=int(nfr(tid) * 0.7) if have(tid) else None, label='difficulty ' + word,
         c=cam(1.0, 1.08, ease='inout'),
         layers=[text(a, b, word, height=150, y=960, tint=col, band=0.6, overlay=False)])
    hit(a, 'flash', 0.12, 0.55)
a, b = tb(35, 18), tb(41)
split(a, b, [('V_rzb_normal', None, fight_score, cam(1.0, 1.0), 0.45), ('V_rzb_hard', None, fight_score, cam(1.0, 1.0), 0.45),
             ('V_rzb_furious', None, fight_score, cam(1.0, 1.0), 0.55)], label='difficulty triptych',
      layers=[text(a, b, w, height=84, x=W * (i + 0.5) / 3, y=990, tint=c, band=None, overlay=False)
              for i, (_, w, c) in enumerate(DIFF_LOOK)])
hit(a, 'punch', 0.2, 0.04)

# ====================================================================================================================
#  BARS 41-48: THE STAGE 6 OPENING - two runs of the same scripted sequence traded, so no pilot is on twice running
# ====================================================================================================================
def op_first(tid, phase, lo=0, default=0):
    return first(tid, lambda m: m.get('op') == phase, lo=lo, default=default)


A6, B6 = 'S6L_open', 'S6O_x_open'
# measured on S6L_open (op metric): the card to ~215, the cloaked lock-on to 1535 (the Retina settles on the ship around
# 1250-1350 under Decker's warning), the reveal to 1703, the slow-motion SHOOT! intercept 1704-1769, the departure, the
# carrier FLYOVER 1866-2407 (its hull fills the screen ~2050-2200), then the assault.
def play0(t):
    return first(t, lambda m: m['st'] == 'play', default=216)
S6_OPEN = [   # Falva's run leads and carries the flyover, Maverick's run trades in between (screen-time balance)
    (B6, 0, 4, lambda t: play0(t) + 24, 1.0, cam(1.0, 1.0), 'S6 opening: the fly-in, the live sky, the radio'),
    (A6, 4, 4, lambda t: op_first(t, 'reveal', default=1535) - 300, 1.0, cam(1.0, 1.3, track='player', lead=-150), 'S6: the lock-on - a Retina settles on the ship'),
    (B6, 8, 4, lambda t: op_first(t, 'reveal', default=1535) - 12, 1.0, cam(1.0, 1.0), 'S6: LOOK OUT! stealth fighters uncloak'),
    (A6, 12, 4, lambda t: op_first(t, 'intercept', default=1704) - 22, 0.75, cam(1.25, 1.4, cy=430, ease='inout'), 'S6: SHOOT! - the slow-motion intercept'),
    (B6, 16, 8, lambda t: op_first(t, 'flyover', default=1866) + 105, 1.0, cam(1.0, 1.0), 'S6: the CARRIER FLYOVER'),
]
for tid, beat0, beats, srcf, spd, c, label in S6_OPEN:
    if not have(tid):
        continue
    shot(tb(41, beat0), tb(41, beat0 + beats), tid, src=srcf(tid), speed=spd, label=label, c=c)
hit(tb(41), 'flash', 0.16, 0.8)
hit(tb(41, 16), 'shake', 0.6, 10)
AS_A, AS_B = 'S6L_assault', 'S6O_y_assault'
shot(tb(41, 24), tb(41, 28), AS_B, score=busy, label='S6: the assault - warned row gates', c=cam(1.0, 1.0))
shot(tb(41, 28), tb(41, 32), AS_A, score=busy, lo=600, label='S6: the assault - bomber passes, jets from the north',
     c=cam(1.0, 1.1, ease='inout'))

# ====================================================================================================================
#  BARS 49-50: the allies, then the choice, in the song's break
# ====================================================================================================================
shot(tb(49), tb(49, 2), 'S6R_allies', score=busy, label='S6: two wingmen join', c=cam(1.0, 1.15, track='player', lead=-180))
shot(tb(49, 2), tb(50), 'S6L_nine', src=0, label='S6: ALL NINE, FORM UP', c=cam(1.0, 1.0))
ch = first('S6R_choice', lambda m: True, default=0)
shot(tb(50), tb(51), 'S6R_choice', src=20, label='S6: CHOOSE YOUR PURSUIT - left or right', c=cam(1.45, 1.6, cy=486, ease='inout'))

# ====================================================================================================================
#  BARS 51-58: the drop - LEFT and RIGHT side by side, the Harrier and the Rebel Fury traded, STAGE X at the centre
# ====================================================================================================================
a, b = tb(51), tb(52)
r_bank = first('S6R_choice', lambda m: (m.get('s6') or [0, 0, None])[2] == 'right', default=200)
split(a, b, [('S6L_route', 0, None, cam(1.0, 1.0), 0.5), ('S6R_choice', r_bank, None, cam(1.0, 1.0), 0.5)],
      label='LEFT | RIGHT',
      layers=[text(a, b, 'LEFT', height=120, x=W * 0.25, y=940, tint='#8edfff', band=None, overlay=False),
              text(a, b, 'RIGHT', height=120, x=W * 0.75, y=940, tint='#ffb4a3', band=None, overlay=False)])
hit(a, 'flash', 0.2, 0.9)
hit(a, 'shake', 0.5, 14)
HV, RF = 'S6L_harrier', 'S6R_fury'
DROP = [
    (HV, 52, 0, 4, dict(score=fight_score, lo=100, hi=900), cam(1.0, 1.0), 'the HARRIER: the Warhive carrier'),
    ('S6R_furyin', 53, 0, 2, dict(score=busy), cam(1.0, 1.0), 'REBEL FURY: the squad arrives in a V'),
    (HV, 53, 2, 2, dict(score=fight_score, lo=700, hi=1500), cam(1.2, 1.35, track='target', lead=140), 'the HARRIER: fans and escorts'),
    (RF, 54, 0, 4, dict(score=busy), cam(1.0, 1.0), 'REBEL FURY: wall of fury'),
    (HV, 55, 0, 4, dict(src=1500), cam(1.0, 1.15, ease='inout'), 'the HARRIER falls'),   # whvDeathStart fired at window f1500
    (RF, 56, 0, 4, dict(score=busy, lo=900), cam(1.1, 1.3, track='player', lead=-200), 'REBEL FURY: signatures'),
    (HV, 57, 0, 2, dict(src=1636), cam(1.0, 1.2, track='target', lead=120), 'the NIGHTWING ACE bursts out'),   # target swaps to the ace at f1650
]
for tid, bar0, beat0, beats, kw, c, label in DROP:
    shot(tb(bar0, beat0), tb(bar0, beat0 + beats), tid, c=c, label=label, **kw)
# STAGE X - the rebels circle the core at the centre of the map; the rival fight with two wingmen
xm = first('X_rival_map', lambda m: m['st'] == 'stagesel', default=0)
shot(tb(57, 2), tb(58), 'X_rival_map', src=100, label='STAGE X: the centre of the map', subject=None,
     c=cam(1.0, 1.1, ease='inout'))
shot(tb(58), tb(59), 'X_rival_duel', score=busy, label='STAGE X: the rival duel, two wingmen',
     c=cam(1.0, 1.2, track='player', lead=-220))

# ====================================================================================================================
#  BARS 59-62: 1 HELL OF A CAMPAIGN
# ====================================================================================================================
shot(tb(59), tb(60), 'C_mapfly', lo=200, score=lambda m: 1, label='1 HELL OF A CAMPAIGN - the map', subject=None,
     c=cam(1.0, 1.1, ease='inout'), desat=0.2, tint=[0, 0, 0, 0.35],
     layers=[text(tb(59), tb(60), '1 HELL OF A', height=120, y=430, face='6', band=0.5, overlay=False),
             text(tb(59), tb(60), 'CAMPAIGN', height=170, y=590, face='6', overlay=False)])
hit(tb(59), 'flash', 0.16, 0.8)
launch = first('C_launch5', lambda m: m.get('gm') is not None, default=0)
shot(tb(60), tb(61), 'C_launch5', src=595, label='S5: the spaceship transformation - the kit converges and snaps',
     c=cam(1.1, 1.25, cy=520, ease='inout'))
for i, tid in enumerate(['B_s1m', 'E1_frenzy', 'B_s9m', 'E2_core']):
    a, b = tb(61, 2 * i), tb(61, 2 * i + 2)
    sc = montage_score
    shot(a, b, tid, score=sc, label='campaign cut ' + tid, c=cam(1.0, 1.15, ease='inout'))
    hit(a, 'punch', 0.14, 0.03)

# ====================================================================================================================
#  BARS 63-70: STAGE 7's BOSS - the Toxic Portal Warden, Furious and Hard traded; then the death
# ====================================================================================================================
W7 = [('W7_fight', 'Furious: the chaingun scissor'), ('W7_fight2', 'Hard: the rail fan'), ('W7_fight', 'stomp and swat'),
      ('W7_fight2', 'the minefield'), ('W7_fight', 'toxic mortar clouds'), ('W7_fight2', 'the cannon burst')]
for i, (tid, what) in enumerate(W7):
    a, b = tb(63 + i), tb(64 + i)
    lo = 0 if i < 2 else (nfr(tid) // 3 if i < 4 else 2 * nfr(tid) // 3) if have(tid) else 0
    shot(a, b, tid, score=fight_score, lo=lo, label='S7 boss: ' + what,
         c=cam(1.0, 1.0) if i % 2 == 0 else cam(1.15, 1.3, track='target', lead=170))
    hit(a, 'punch', 0.16, 0.035)
hit(tb(63), 'flash', 0.16, 0.85)
# the death and the escape, fading out with the song. W7_escape drives the Warden's own modular damage route
# (capture9 S7K): the modules rupture, the shield breaks, the core dies at the 'core ... dead' event, then the wreck's
# toxic blasts, the portal opening ~430 frames later, the ship flying in, and green blasts filling the screen.
# Two parts of ONE continuous take with a time skip between them (the empty sewer run between the wreck and the portal
# is cut) - one scene, reported as a continuation rather than as a second shot of the same pilot.
if have('W7_escape'):
    ev = [int(k) for k, v in meta('W7_escape')['event_idx'].items() if "'core'" in v]
    death = first('W7_escape', lambda m: bool(m.get('bd')), default=(min(ev) if ev else 500))
    shot(tb(69), tb(71), 'W7_escape', src=max(0, death - 40), label='S7: the Warden dies - the wreck blows',
         c=cam(1.0, 1.12, ease='inout'))
    hit(tb(69), 'flash', 0.22, 0.9)
    hit(tb(69), 'shake', 0.9, 16)
    SONG_END0 = q(T0 + BM['duration'] - 0.6)
    shot(tb(71), SONG_END0, 'W7_escape', src=death + 425, label='S7: the escape through the toxic portal (continues)',
         c=cam(1.0, 1.0), cont=True, clip_kw={'fade_out': 2.4})
    hit(tb(71), 'punch', 0.2, 0.03)
SONG_END = q(T0 + BM['duration'] - 0.6)

# ====================================================================================================================
#  POST-SONG: LAST BUT NOT LEAST. / STOP? / HAMMERTIME? -> HAMA -> the logo card
# ====================================================================================================================
t = SONG_END + 0.35
black(SONG_END, t + 2.6, label='LAST BUT NOT LEAST.')
t_end = typed(t, t + 2.6, 'LAST BUT NOT LEAST.', height=110, y=540)
t_stop = q(t + 2.6 + 0.15)
black(t + 2.6, t_stop, label='beat')
black(t_stop, t_stop + 1.05, label='STOP?', layers=[text(t_stop, t_stop + 1.05, 'STOP?', face='5', height=190, y=540,
                                                          kin='slam', overlay=False)])
hit(t_stop, 'shake', 0.35, 10)
sfx(t_stop, SND('sfx_0927', 'hammer_slam.mp3'), gain_db=-7.0)
t_ham = q(t_stop + 1.05)
t_cut = q(t_ham + 1.2)
black(t_ham, t_cut, label='HAMMERTIME?', layers=[text(t_ham, t_cut, 'HAMMERTIME?', face='5', height=190, y=540,
                                                     kin='slam', overlay=False)])
hit(t_ham, 'shake', 0.45, 14)
sfx(t_ham, SND('sfx_0927', 'hammer_slam.mp3'), gain_db=-5.0)
sfx(t_ham + 0.02, SND('sounds', 'expBig.mp3'), gain_db=-9.0)

# the HAMA breakdown: open on a beat of the instrumental during the OH-OH chant; cut to the logo two beats after TIME!
HAMA = 'T_hama'
hama_t0 = hama_src = logo_t0 = None
if have(HAMA):
    Ms = M(HAMA)
    hc = [m.get('hc') for m in Ms]
    want = 108.2
    k_beat = round((want - HAMA_PHASE) / HAMA_BEAT)
    tgt = HAMA_PHASE + k_beat * HAMA_BEAT
    hama_src = min(range(len(hc)), key=lambda i: abs((hc[i] or 0) - tgt))
    # the TIME slam: the second hammerImpact in the take's own sound log
    ae = json.load(open(os.path.join(TAKES_DIR, HAMA, 'audio_events.json')))
    slams = sorted(e[0] - ae['rec0'] for e in ae['snd'] if e[1] == 'hammerImpact')
    time_f = slams[1] if len(slams) > 1 else hama_src + 460
    end_f = time_f + int(round(2 * HAMA_BEAT * FPS))
    hama_t0 = t_cut
    logo_t0 = q(hama_t0 + (end_f - hama_src) / FPS)
    # the breakdown wide (the whole troupe: lasso bars, jumping 360s, OH-OH), then - one continuous take - in close for
    # STOP! and the two slams, HAMMER on one beat and TIME on the next
    stop_f = slams[0] - int(round(1.5 * HAMA_BEAT * FPS)) if slams else hama_src + 380
    t_stop_cut = q(hama_t0 + (stop_f - hama_src) / FPS)
    shot(hama_t0, t_stop_cut, HAMA, src=hama_src, label='HAMA: the breakdown - OH, OH-OH', c=cam(1.0, 1.12, ease='inout'))
    shot(t_stop_cut, logo_t0, HAMA, src=hama_src + int(round((t_stop_cut - hama_t0) * FPS)), cont=True,
         label='HAMA: STOP! HAMMER - TIME!', c=cam(1.3, 1.42, track='target', lead=120))
    hit(hama_t0, 'flash', 0.12, 0.6)
    for sf in slams[:2]:
        if sf >= hama_src:
            hit(hama_t0 + (sf - hama_src) / FPS, 'shake', 0.4, 16)
            hit(hama_t0 + (sf - hama_src) / FPS, 'flash', 0.1, 0.35)
    HAMA_SRC_T = hc[hama_src]
else:
    logo_t0 = t_cut
    HAMA_SRC_T = None

# the logo card: the wordmark, the date, the platforms, the credit
END = q(logo_t0 + 7.2)
black(logo_t0, END, label='logo card', fade_out=1.6,
      layers=[image(logo_t0, END, 'brand/bof_logo.png', y=400, prescale=0.66, kin='slam', drift=0.008, overlay=False),
              text(logo_t0 + 0.9, END, '11.1.26', height=110, y=735, kin='rise', overlay=False),
              text(logo_t0 + 1.5, END, 'STEAM / PC / MAC / LINUX', height=58, y=855, kin='fade', face='6', overlay=False),
              image(logo_t0 + 2.1, END, 'brand/copyright.png', y=965, prescale=0.8, kin='fade', shadow=False, overlay=False)])
hit(logo_t0, 'flash', 0.22, 1.0)
hit(logo_t0, 'shake', 0.4, 14)
LENGTH = END

# ====================================================================================================================
#  AUDIO
# ====================================================================================================================
AUDIO = {
    'length': LENGTH,
    't0': T0,
    'takes_dir': TAKES_DIR,
    'song': SONG,
    'song_gain_db': -6.3,
    'song_fade_in': 0.02,
    'song_fade_out': [tb(71), SONG_END],
    'music2': ({'file': HAMA_SONG, 't': hama_t0, 'src': HAMA_SRC_T, 'fade_in': 0.02, 'fade_out': [END - 2.6, END],
                'match_song': True, 'match_offset_db': -3.0} if HAMA_SRC_T is not None else None),
    'chime': {'file': SND('sounds', 'cf_boot.mp3'), 't': 0.45, 'gain_db': -0.6},
    'sfx': SFX,
    'fade_out': 0.4,
}


def report():
    print('trailer length %.2f s (%d frames), %d clips, %d overlays, %d hits, %d sfx' % (
        LENGTH, int(round(LENGTH * FPS)), len(CLIPS), len(OVERLAYS), len(HITS), len(SFX)))
    if MISSING:
        print('MISSING TAKES: %s' % sorted(MISSING))
    print('claim conflicts: %d' % len(CONFLICTS))
    for c in CONFLICTS:
        print('   ', c)
    per = defaultdict(float)
    prev = None
    b2b = []
    for s in SHOTS:
        p = s['pilot']
        if p:
            per[p] += s['t1'] - s['t0']
        if p and p == prev and not s.get('cont'):
            b2b.append('%s at %.2f (%s)' % (p, s['t0'], s['label']))
        prev = p
    print('pilot screen time: ' + ', '.join('%s %.1fs' % (p, per.get(p, 0)) for p in PILOTS))
    print('back-to-back same pilot: %d' % len(b2b))
    for x in b2b:
        print('   ', x)
    for s in SHOTS:
        print('  %7.2f-%7.2f %-10s %-18s src %-6s %s' % (s['t0'], s['t1'], s['pilot'] or '-', s['take'] or '-',
                                                     s['src'] if s['src'] is not None else '-', s['label']))


if __name__ == '__main__':
    edl = {'clips': CLIPS, 'overlays': OVERLAYS, 'hits': HITS, 'audio': AUDIO}
    json.dump(edl, open(os.path.join(HERE, 'edl9.json'), 'w'), indent=1)
    report()
