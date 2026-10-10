"""edit10.py - cut the v10 Bullets of Fury trailer to GASLINE (LevelX.mp3, the Stage 6 rebel-fight / Stage X track).
Writes edl10.json for compose.py and mix9.py.  python edit10.py

Mike, 1008: "Design a bot that actually plays the game properly, capturing footage between Easy/Normal, Hard and
Furious where differences and changes occur. The 9 pilots, the 10 stages, the 1 hell of a campaign ... the mini
bosses, the bosses, the special abilities, the pilots, the rebel fight, the alternate path choice, the harrier, the
final boss transforming into different forms and us being in the void, missile volley galore etc. Make it fast,
action paced, show the cutscene of the rebel fighters and us."

Song map (beatmap10.json, measured: 163.1 BPM, bars of 1.471 s; a dip at bar 6, the one break at 35.7-37.2 s, the
silence at 85.5 s and the last hit at ~86.0 s):

  1        ColeForge plate
  2-5      cold open: eight half-bar shots of the hardest action in the game
  6        the dip: Dracodia speaks from the void
  7-8      BULLETS OF FURY
  9-14     9 PILOTS: the line-up, then each on their special
  14-20    10 STAGES: each stage card, then the stage itself (STAGE X at the centre of the map)
  21-26    EASY/NORMAL - HARD - FURIOUS: the Razorback becomes two, then a crimson 150% hyper tank; the break
  27-34    20 BOSSES: minibosses and bosses on the half bar
  35-36    MISSILE VOLLEY GALORE
  37-46    1 HELL OF A CAMPAIGN: the map, stage 6's carrier, the allies, the Rebel cutscene, the choice, LEFT|RIGHT,
           the Harrier, the Rebel fight
  47-57    THE FINALE: the drone, the ghost, the void, Dracodia, eight stolen forms, the destruction
  58       the claims stacked over a quarter-beat recap
  post     the silence -> the logo card: 11.1.26, Steam / PC / Mac / Linux, (c) 2026 ColeForge Productions
"""
import os, sys, json, math
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TAKES_DIR = os.path.join(HERE, 'takes10')
FPS, W, H = 60, 1920, 1080
PF_W, PF_H = 960, 1024
T0 = 0.0                                   # the pre-roll: the song's first sample lands here
SONG = os.path.join(ROOT, 'assets', 'game', 'music', 'LevelX.mp3')
HAMA_SONG = os.path.join(ROOT, 'assets', 'game', 'music', 'HAMA_Instrumental.mp3')
SND = lambda *p: os.path.join(ROOT, 'assets', 'game', *p)

BM = json.load(open(os.path.join(HERE, 'beatmap10.json')))
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
                    mm['wr'] = (w[i] if i < len(w) else 0.0)
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


exec(open(os.path.join(HERE, 'cut10.py')).read())
