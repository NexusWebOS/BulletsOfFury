"""edit3.py - cut the v3 Bullets of Fury trailer to Cowboy From Hell. Writes edl3.json for compose.py + mix3.py.

    python edit3.py

Mike, on v2: "The trailer was supposed to be all one trailer, and have the sounds in there. Be more thorough
with showcasing instead of doing it 3x with the same pilot throughout different spots in the trailer."

The song map is v2's (it was right): logo and chime, the menus, BOOM, nine pilots, the minibosses, the arsenal,
the bosses, stop-time stabs, the climax, the end card. What changed is what fills it.

  NO FOOTAGE IS SHOWN TWICE. Every pane CLAIMS the source frames it plays (speed and freeze included), and a
  claim that overlaps an earlier one on the same take is a CONFLICT, printed and counted. v2 had 58 takes under
  158 clips and put Lizzie's atom bomb on screen nine times; v3 draws on the 80-take library in capture3.py and
  free() searches only the frames nothing has used yet.
  NO PILOT BACK TO BACK. Every single-pane shot has a subject pilot; the report lists pilot screen time and any
  two consecutive shots of the same pilot. Panes that are only a backdrop (bgonly) are not a subject.
  THE SOUND IS THE SHOT'S. Every pane's take carries takes3/<id>/sfx.wav, rendered from the game's own sound log;
  mix3.py plays each pane's audio under the song at the pane's own source time and speed. The designed accents
  that remain are the chime, the logo slam and a few stabs - v2 had forty.
"""
import os, sys, json, math
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import typeset                               # noqa: E402
from capture3 import TAKES as SPECS          # noqa: E402

ROOT = r'C:\Users\Mdogg\Desktop\BOF-CODE\BulletsOfFury'
SND = os.path.join(ROOT, 'assets', 'game', 'sounds')
SONG = r'C:\Users\Mdogg\Desktop\cowboyfromhell.wav'
TAKES_DIR = os.path.join(HERE, 'takes3')
FPS, W, H = 60, 1920, 1080
T0 = 4.0
LENGTH = 165.0

BM = json.load(open(os.path.join(HERE, 'beatmap.json')))
BARS = [b['t'] for b in BM['bars']]
BEAT = BM['beat_period']


def bar(k, beat=0.0):
    k = int(k) + int(beat // 4)
    beat = beat - 4 * int(beat // 4)
    i = k - 1
    a = BARS[i]
    b = BARS[i + 1] if i + 1 < len(BARS) else a + 4 * BEAT
    return a + (b - a) * beat / 4.0


def S(x):
    return x + T0


def tb(k, beat=0.0):
    return S(bar(k, beat))


# ---- takes ---------------------------------------------------------------------------------------------------
_M = {}
MISSING = set()


def meta(tid):
    if tid not in _M:
        d = os.path.join(TAKES_DIR, str(tid))
        try:
            m = json.load(open(os.path.join(d, 'meta.json')))
            m['metrics'] = json.load(open(os.path.join(d, 'metrics.json')))
        except (OSError, ValueError):
            m = None
        _M[tid] = m
    return _M[tid]


def have(tid):
    ok = bool(tid) and meta(tid) is not None and meta(tid)['frames'] > 0
    if tid and not ok:
        MISSING.add(tid)
    return ok


def pick(*tids):
    for t in tids:
        if have(t):
            return t
    return None


def nfr(tid):
    return meta(tid)['frames']


def event(tid, needle, k=0):
    ev = sorted((int(i), js) for i, js in meta(tid)['event_idx'].items() if needle in js)
    return ev[k][0] if len(ev) > k else None


def first(tid, pred, lo=0, default=None):
    M = meta(tid)['metrics']
    for i in range(max(0, int(lo)), len(M)):
        if pred(M[i]):
            return i
    return default


def argmax(tid, key, lo=0, hi=None):
    M = meta(tid)['metrics']
    lo = max(0, int(lo))
    hi = len(M) if hi is None else min(len(M), int(hi))
    if lo >= hi:
        return min(lo, len(M) - 1)
    return max(range(lo, hi), key=lambda i: (M[i].get(key) or 0))


def action(m):
    return (m.get('ex') or 0) * 3 + (m.get('eb') or 0) + (m.get('pb') or 0) * 0.5 + (m.get('sh') or 0) * 2


def boom_score(m):
    return (m.get('ex') or 0) * 4 + (m.get('sh') or 0) * 6 + (m.get('fl') or 0) * 20


def gun(m):
    return (m.get('pb') or 0) + 3 * (m.get('ex') or 0) + 0.3 * (m.get('eb') or 0)


def special_score(m):
    return (6 if m.get('sp') else 0) + action(m)


def entered(tid, key):
    M = meta(tid)['metrics']
    act = first(tid, lambda m: m[key], default=150)
    kill = event(tid, '__kill') or len(M)
    ys = [M[i]['ty'] for i in range(act, min(kill, len(M))) if M[i].get('ty') is not None]
    if not ys:
        return act + 100
    goal = min(0.8 * max(ys), 110)
    return first(tid, lambda m: m.get('ty') is not None and m['ty'] >= goal, lo=act, default=act + 100)


def kill_cy(tid, f):
    M = meta(tid)['metrics']
    for i in range(max(0, f - 1), max(0, f - 40), -1):
        if M[i].get('ty') is not None:
            return M[i]['ty'] * 2
    return 300


_LUM = {}
WHITE, WHITE_MAX = 200, 0.25


def lum(tid):
    """per-frame mean luminance of a take, decoded at 1/8 scale and cached beside it. A special's own whiteout -
    Lizzie's atom bomb, Maverick's helix release - is not flashScreen, so the metrics cannot see it, and in a split
    or a strobe it reads as a blank white panel (measured: 46%, 50% and 80% white on three shots of the first cut)."""
    if tid not in _LUM:
        path = os.path.join(TAKES_DIR, tid, 'lum.json')
        try:
            _LUM[tid] = json.load(open(path))
        except (OSError, ValueError):
            from PIL import ImageStat
            vals = []
            for k in range(nfr(tid)):
                im = Image.open(os.path.join(TAKES_DIR, tid, 's%05d.jpg' % k))
                im.draft('L', (120, 128))
                vals.append(round(ImageStat.Stat(im.convert('L')).mean[0], 1))
            json.dump(vals, open(path, 'w'))
            _LUM[tid] = vals
    return _LUM[tid]


def white_share(tid, a, b):
    L = lum(tid)
    a, b = max(0, int(a)), min(len(L), int(math.ceil(b)))
    return (sum(1 for v in L[a:b] if v > WHITE) / float(b - a)) if b > a else 0.0


def past_white(tid, f, dur, limit=90):
    """move a pinned shot forward - at most `limit` frames - until no more than WHITE_MAX of it is whiteout"""
    span = max(1, int(round(dur * FPS)))
    for d in range(0, limit + 1, 2):
        if white_share(tid, f + d, f + d + span) <= WHITE_MAX:
            return f + d
    return f


# ---- claims: no frame of footage is shown twice ----------------------------------------------------------------
PILOT_OF = {t: s.get('pilot') for t, s in SPECS.items()}
CLAIMS, CONFLICTS, SHOTS = {}, [], []
RESERVED = {}
HI_CAP = {'F_s6': 820}        # v4: the stage-6 run's last frames warn of its miniboss - Mike: no stage-6 bosses at all
RESERVE = [False]
TOL = 3


def span_of(p, t0, t1):
    speed = float(p.get('speed', 1.0))
    if p.get('hold') is not None:
        return p['src'], p['src'] + p['hold'] * FPS * speed + 1
    return p['src'], p['src'] + (t1 - t0) * FPS * speed


def overlap(tid, a, b, table=None):
    for (x, y, lab) in (CLAIMS if table is None else table).get(tid, []):
        if min(b, y) - max(a, x) > TOL:
            return lab
    return None


def claim(tid, a, b, label):
    lab = overlap(tid, a, b)
    if lab:
        CONFLICTS.append('%-13s [%5d-%5d] %-34s overlaps %s' % (tid, a, b, label[:34], lab))
    CLAIMS.setdefault(tid, []).append((int(a), int(math.ceil(b)), label))


def free(tid, dur, score=action, lo=0, hi=None, pad=8):
    """the best-scoring `dur`-second window of `tid` that no shot has claimed or RESERVED.

    The edit is built twice. Pass one (RESERVE) cuts only the shots pinned to a moment - a strike landing, a
    kill, a gate pass - and free() declines everything, so their frames are known before any search runs. Built
    in timeline order alone, bar 65's split took the frames bar 74's strobe needs for Cole's second strike."""
    if RESERVE[0] or not have(tid):
        return None
    M = meta(tid)['metrics']
    span = max(1, int(round(dur * FPS)))
    if tid in HI_CAP:
        hi = min(len(M) - span if hi is None else hi, HI_CAP[tid] - span)
    v = [score(m) for m in M]
    lo = max(0, int(lo))
    hi = len(M) - span if hi is None else min(len(M) - span, int(hi))
    if hi < lo:
        return None
    L = lum(tid)
    wp = [0]
    for k in range(len(M)):
        wp.append(wp[-1] + (1 if k < len(L) and L[k] > WHITE else 0))
    cur = sum(v[lo:lo + span])
    best, bi = None, None
    for i in range(lo, hi + 1):
        if i > lo:
            cur += v[i + span - 1] - v[i - 1]
        if overlap(tid, i - pad, i + span + pad) or overlap(tid, i - pad, i + span + pad, RESERVED):
            continue
        if wp[i + span] - wp[i] > WHITE_MAX * span:          # a special's whiteout reads as a blank panel
            continue
        if best is None or cur > best:
            best, bi = cur, i
    return bi


# ---- the EDL ----------------------------------------------------------------------------------------------------
E = {'clips': [], 'overlays': [], 'hits': []}
SFX = []
CUTS = []


def pane(tid, src, rect=(0, 0, W, H), s0=1.0, s1=None, cy=512, track=None, lead=0, speed=1.0, hold=None,
         ease='out', bg='blur', desat=0.0, tint=None, border=None, bgonly=False, gain=None, intense=False):
    if src is None:
        return None
    # Mike, on v4: "Show full sized view mostly. Only do dynamic zoom in/out on intense moments." A pane shows the whole
    # cabinet, still, unless its call site marks the moment intense. A scale under 1 is grid LAYOUT, not a zoom.
    if not intense and s0 >= 1.0:
        s0, s1, track, lead = 1.0, None, None, 0
    p = {'rect': [int(v) for v in rect], 'take': tid, 'src': max(0, int(round(src))), 'speed': speed, 'bg': bg,
         'cam': {'s0': s0, 's1': s0 if s1 is None else s1, 'ease': ease, 'cx': 480, 'cy': cy, 'track': track, 'lead': lead}}
    if hold is not None:
        p['hold'] = hold
    if desat:
        p['desat'] = desat
    if tint:
        p['tint'] = tint
    if border:
        p['border'] = border
    if bgonly:
        p['bgonly'] = True
    if gain is not None:
        p['gain'] = gain
    return p


def clip(t0, t1, panes=(), layers=(), label='', cont=False, **fx):
    if t1 - t0 < 1.0 / FPS:
        return None
    panes = [p for p in panes if p and have(p['take'])]
    c = {'t0': round(t0, 4), 't1': round(t1, 4), 'panes': panes, 'layers': list(layers), 'label': label}
    c.update(fx)
    E['clips'].append(c)
    for p in panes:
        a, b = span_of(p, t0, t1)
        claim(p['take'], a, b, label or p['take'])
    subj = [PILOT_OF.get(p['take']) for p in panes if not p.get('bgonly')]
    SHOTS.append((t0, t1, subj, label, cont))      # cont: the same shot carried on - its freeze or slow-motion tail
    CUTS.append((t0, label or ','.join(p['take'] for p in panes)))
    return c


def src_at(frame, when, t0, speed=1.0):
    return frame - (when - t0) * FPS * speed


_WC = {}


def clean(s, face):
    miss = set(typeset.has_glyphs(s, str(face)))
    return ''.join(ch for ch in s if ch not in miss).strip() if miss else s


def fit(s, face, max_w, max_h):
    key = (s, str(face))
    if key not in _WC:
        _WC[key] = typeset.text(s, face=str(face), height=100).width
    return int(max(14, min(max_h, 100.0 * max_w / _WC[key])))


def T(s, t_in, t_out, face='final', h=90, x=W / 2, y=H / 2, anchor='c', inn='slam', out='cut', band=0.0, **kw):
    s = clean(s, face)
    L = {'kind': 'text', 'text': s, 'face': str(face), 'height': int(h), 'x': x, 'y': y, 'anchor': anchor,
         't_in': round(t_in, 4), 't_out': round(t_out, 4), 'in': inn, 'out': out}
    if band:
        L['band'] = band
    L.update(kw)
    return L


def I(src, t_in, t_out, x=W / 2, y=H / 2, prescale=1.0, anchor='c', inn='cut', out='cut', **kw):
    L = {'kind': 'image', 'src': src, 'x': x, 'y': y, 'prescale': prescale, 'anchor': anchor,
         't_in': round(t_in, 4), 't_out': round(t_out, 4), 'in': inn, 'out': out}
    L.update(kw)
    return L


def hit(t, kind, dur, amp):
    E['hits'].append({'t': round(t, 4), 'kind': kind, 'dur': dur, 'amp': amp})


def boom(t, k=1.0):
    hit(t, 'flash', 0.16, min(1.0, 0.8 * k))
    hit(t, 'shake', 0.42, 16 * k)
    hit(t, 'punch', 0.24, 0.055 * k)
    hit(t, 'rgb', 0.12, 8 * k)


def accent(t, k=1.0):
    hit(t, 'punch', 0.14, 0.03 * k)
    hit(t, 'rgb', 0.07, 4 * k)


def sfx(t, name, db=-10.0, duck=0.0):
    p = os.path.join(SND, name)
    if os.path.exists(p):
        e = {'file': p, 't': round(t, 4), 'gain_db': db}
        if duck:
            e['duck_db'] = duck                       # a voice line: mix3 dips the song for as long as it speaks
        SFX.append(e)
    else:
        print('  (no sound %s)' % name)


def vo_onset(path, thr_db=-24.0):
    """seconds from the start of a voice file to its first word, so the word - not the file - lands on the hit"""
    import subprocess, imageio_ffmpeg
    import numpy as np
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1',
                        '-ar', '48000', '-'], capture_output=True, check=True)
    x = np.frombuffer(r.stdout, dtype=np.float32)
    n = 480
    k = len(x) // n
    if k == 0:
        return 0.0
    rms = np.sqrt((x[:k * n].reshape(k, n).astype(np.float64) ** 2).mean(axis=1) + 1e-12)
    on = np.where(20 * np.log10(rms / rms.max()) > thr_db)[0]
    return float(on[0] * n / 48000.0) if len(on) else 0.0


# ---- the cast -----------------------------------------------------------------------------------------------------
PILOTS = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']
SPECIAL = {'axel': ['MEGA SHIELD'], 'decker': ['CLOAKING SYSTEM'], 'maverick': ['HELIX BEAM'],
           'freezer': ['TIME FREEZE', 'THERMOSHOCK'], 'juggernaut': ['WRECKING BALL'], 'yuri': ['CHAIN LIGHTNING'],
           'cole': ['NUKE STRIKE'], 'lizzie': ['ATOM BOMB'], 'falva': ['ROLLER BALL']}
ORDER = ['axel', 'yuri', 'freezer', 'falva', 'decker', 'juggernaut', 'maverick', 'cole', 'lizzie']


def moment(p, which=1, nth=0):
    """(take, source frame of the special's big moment, where in its bar that moment lands)"""
    tid = 'S%d_%s' % (which, p)
    if not have(tid):
        return None, 0, 0.0
    sp = event(tid, 'startSpecial') or 0
    if p in ('maverick', 'falva'):
        rel = event(tid, '__fire = false', 1 + nth)
        return tid, (rel if rel is not None else sp + 90 + 130 * nth), 2.0
    if p in ('cole', 'lizzie'):
        launch = event(tid, "'k'", nth)
        if launch is None:
            launch = sp + 80 * (nth + 1)
        det = first(tid, lambda m: (m.get('sh') or 0) >= 12, lo=launch + 10)
        if det is None or det > launch + 200:
            det = argmax(tid, 'sh', launch + 10, launch + 200)
        return tid, det, 2.0
    return tid, max(0, sp + 4), 0.5


def gate_pass(k):
    """source frame of W_warp's k-th gate pass (k = 1..8)"""
    return first('W_warp', lambda m: (m.get('gi') or 0) >= k) if have('W_warp') else None


def warp_phase(ph):
    return first('W_warp', lambda m: m.get('wp') == ph) if have('W_warp') else None


# ---- sections -------------------------------------------------------------------------------------------------------
def intro():
    clip(0.0, T0, layers=[I('brand/cf_logo.png', 0.35, T0 - 0.1, y=530, prescale=0.72, inn='fade', fade=0.8,
                             out='fade', fade_out=0.5, drift=0.01)], label='COLEFORGE PHOENIX ENGINE + chime')
    hit(0.62, 'flash', 0.6, 0.14)


def menus():
    t_a, t1, t2 = S(0.0), tb(1), tb(2)
    ttl = pick('A_title', 'A_walk')
    if ttl:
        clip(t_a, t1, [pane(ttl, 0, s0=1.0, s1=1.06, ease='inout', desat=0.2, tint=[0, 0, 0, 0.3])], fade_in=0.8,
             label='title screen breathes in')
        clip(t1, t2, [pane(ttl, (t1 - t_a) * FPS, s0=1.06, s1=1.16, ease='inout', desat=0.5, tint=[0, 0, 0, 0.62])],
             layers=[I('brand/nbl_logo.png', t1, t2, y=510, prescale=2.0, inn='slam', shadow=True, drift=0.025)],
             label='BULLETS OF FURY slam')
    boom(t1, 1.2)
    sfx(t1, 'explosion_boss_core.wav', -15)
    # Mike, on v3: "Make sure we hear BULLETS OF FURY in the beginning." The title screen's own announcer
    # (Audio.SFX.announce on GS.TITLE) sat in every take's pre-roll and never reached the cut. A_title and A_walk are
    # rendered without it now, and it lands here - first word on the slam, the song dipped under it.
    sfx(t1 - vo_onset(os.path.join(SND, 'announce.mp3')), 'announce.mp3', 3.0, duck=9.0)
    w = 'A_walk'
    if not have(w):
        return
    press_new, press_up, press_camp = event(w, "'enter'", 0), event(w, "'w'"), event(w, "'enter'", 1)
    t4 = tb(4)
    src = src_at(press_camp, t4, t2)
    modesel = first(w, lambda m: m['st'] == 'modesel', lo=press_new, default=press_new + 20)
    t_mode = t2 + (modesel - src) / FPS
    t_new = t2 + (press_new - src) / FPS
    clip(t2, t_mode, [pane(w, src, s0=1.75, s1=2.0, cy=420)], label='NEW GAME')
    clip(t_mode, t4, [pane(w, src + (t_mode - t2) * FPS, s0=1.2, s1=1.32, cy=380, ease='inout')],
         label='SELECT MODE -> CAMPAIGN')
    for t, k in ((t_new, 1.0), (t2 + (press_up - src) / FPS, 0.6)):
        accent(t, 1.4 * k)
        hit(t, 'flash', 0.1, 0.3 * k)
    hit(t4, 'flash', 0.14, 0.45)
    hub = first(w, lambda m: m['st'] == 'camphub', default=press_camp + 20)
    b = [tb(4, k) for k in range(5)]
    clip(b[0], b[1], [pane(w, hub + 24, s0=1.3, cy=400)], label='CAMPAIGN hub')
    if have('A_mapboot'):
        # the map in pieces: the bar slams down, the flags drop, and the camera dives into BOOM
        clip(b[1], b[4], [pane('A_mapboot', 226, s0=1.0, s1=2.5, ease='in', cy=470, intense=True)], label='campaign map v2 boot, zooming into BOOM')
    accent(b[1])
    hit(b[3] + 0.2, 'rgb', 0.31, 16)


def boom_montage():
    t5 = tb(5)
    boom(t5, 1.4)
    sfx(t5, 'explosion_boss_core.wav', -7)
    for i, tid in enumerate(['F_s4', 'F_s3', 'F_s1', 'F_s2', 'F_s5', 'F_s6']):
        t0, t1 = tb(5, 2 * i), tb(5, 2 * i + 2)
        if i >= 4 and have('X_launch5'):
            # Mike, on v6: "Show the spaceship transformation scene" - the last two montage beats become the transformation,
            # from the snap through the pixel glow, the white and the reveal into the countdown
            if i == 4:
                t1 = tb(5, 12)
                snap = first('X_launch5', lambda m: m.get('gm') == 'snap', default=192)
                clip(t0, t1, [pane('X_launch5', max(0, snap - 12), s0=1.0)], label='SPACESHIP transformation')
                hit(tb(5, 11), 'flash', 0.12, 0.4)
                accent(t0, 1.3)
                sfx(t0 + 0.05, 'whip.wav', -8)                              # the kit snaps together
                sfx(tb(5, 11), 'reviewed_special_pickup.wav', -5)          # GRAVITY MODE ONLINE
            continue
        if not have(tid):
            continue
        src = free(tid, (t1 - t0) + 0.2)
        if i % 2 == 0:
            clip(t0, t1, [pane(tid, src, s0=2.0, cy=640, track='player', lead=-170)], label=tid + ' x2')
            hit(t0, 'flash', 0.1, 0.25)
        else:
            clip(t0, t1, [pane(tid, src, s0=1.0, s1=1.04, ease='inout')], label=tid)
        accent(t0, 1.3 if i % 2 == 0 else 0.8)
    for j, tid in enumerate(['C2_missiles', 'C_mg', 'C2_spread', 'W_warp']):
        t0, t1 = tb(8, j), tb(8, j + 1)
        if not have(tid):
            continue
        if tid == 'W_warp':
            g = gate_pass(2)
            src = src_at(g, t0 + BEAT * 0.45, t0) if g is not None else free(tid, t1 - t0)
            clip(t0, t1, [pane(tid, src, s0=1.0, s1=1.08, ease='inout')], label='WARP GATE jump')
        else:
            src = free(tid, (t1 - t0) + 0.1, score=gun)
            clip(t0, t1, [pane(tid, src, s0=2.0, cy=640, track='player', lead=-170)], label=tid)
        accent(t0)
    # Mike, on v5: "You may display all 8 stage cards instead of 1-6." Eight one-beat cards fill bars 9-10 exactly, so
    # the sped-up pilot roster gives its two beats up - the 9 PILOTS grid right after says the same thing, properly.
    cards = [t for t in ['F_intro_s%d' % k for k in range(1, 9)] if have(t)]
    ends = [tb(9, j + 1) for j in range(len(cards))]
    if len(cards) >= 8:
        ends[-1] = tb(11)
    for j, tid in enumerate(cards):
        t0, t1 = tb(9, j), ends[j]
        clip(t0, t1, [pane(tid, 90, s0=1.5, s1=1.7, cy=530)], label=tid + ' stage card')
        hit(t0, 'flash', 0.12, 0.35)
        accent(t0, 1.2)
    if have('A_pilots') and tb(9, len(cards)) < tb(11) - BEAT * 0.9:
        t0, t1 = tb(9, len(cards)), tb(11)
        last_ok = (event('A_pilots', "'d'", 7) or 636) - 12
        speed = min(4.0, (last_ok - 60) / max(1.0, (t1 - t0) * FPS))
        clip(t0, t1, [pane('A_pilots', 60, s0=1.0, speed=speed, gain=0.5)], label='pilot roster x%.1f' % speed)
        hit(t1 - 0.25, 'rgb', 0.25, 12)


# Mike, on v3: "use the proper avatar boxes we have and the proper pilot bodies to match ... showcase all players
# abilities 1 by 1 after the 9 pilots part including their secondary ones if they have, use proper palette swapped
# fonts to match them please."
#   bodies   pilot_bodies/<pilot>_body_0 - what psBodyKey draws on the pilot select. v3 used pose_<pilot>_0, and
#            Yuri's pose set is the art Mike rejected ("I never liked how Yuri turned out", PS_POSE_STALE).
#   avatars  pilot_avatars/pav_<pilot> - the square bordered roster avatars (Mike, 0906).
#   fonts    the FINAL-LEVEL face the pilot screen sets every pilot in (pilotFont), palette-swapped at alpha 1 to the
#            pilot's PILOTS[].tint - exactly how drawPilot sets a name.
TINT = {'axel': '#3a8aff', 'decker': '#ffd24a', 'maverick': '#3ad6c8', 'freezer': '#6fd0ff', 'juggernaut': '#c08a3a',
        'yuri': '#e23a3a', 'lizzie': '#ffc21a', 'falva': '#ff2a8f', 'cole': '#7ad63a'}
# The primaries are SPECIAL_INFO. The secondaries are what the game itself treats as ONE pilot's own: the three
# pickups that fire playSpecialPickupCue for a single pilot (Decker's incendiary shotgun, Lizzie's heavy MG mount,
# Cole's sonic boom), Juggernaut's charge dash (chargeAvailable is gated on his special), and Freezer's ice breath
# (flameIsIce - the one weapon variant exclusive to a pilot). Laser mist is a global unlock, not Maverick's.
ABILITIES = {
    'axel':       [(['MEGA SHIELD'], 'S1_axel', 'special')],
    'yuri':       [(['CHAIN LIGHTNING'], 'S1_yuri', 'special')],
    'freezer':    [(['TIME FREEZE', 'THERMOSHOCK'], ('S1_freezer', 'C_thermo'), 'special+weapon'), (['ICE BREATH'], 'C_icebreath', 'weapon')],
    'falva':      [(['ROLLER BALL'], 'S1_falva', 'special')],
    'decker':     [(['CLOAKING SYSTEM'], 'S1_decker', 'special'), (['INCENDIARY SHOTGUN'], 'C_shotgun', 'weapon')],
    'juggernaut': [(['WRECKING BALL'], 'S1_juggernaut', 'special'), (['CHARGE DASH'], 'J_charge', 'charge')],
    'maverick':   [(['HELIX BEAM'], 'S1_maverick', 'special')],
    'cole':       [(['NUKE STRIKE'], 'S1_cole', 'special'), (['SONIC BOOM'], 'C_sonic', 'release')],
    'lizzie':     [(['ATOM BOMB'], 'S1_lizzie', 'special'), (['HEAVY MG'], 'C_turret', 'weapon')],
}
SONG_STOP, SONG_BACK = S(44.82), S(45.45)          # the song's stop, and the riff coming back in


def ability_moment(p, tid, how):
    """(source frame of the ability's big moment, where in its bar that moment lands) - or (None, None) for a weapon"""
    if how == 'special':
        _, mom, beat = moment(p, 1)
        return mom, beat
    if how == 'release':
        # Mike, on v4: "Make coles sonic boom an actual charged one." C_sonic holds FIRE past SONIC_MAX and lets go; the
        # second release inside the recording sits at beat 2, so the bar shows the wind-up and then the full wave.
        rel = sorted(int(k) for k, v in meta(tid)['event_idx'].items() if '__fire = false' in v and int(k) >= 0)
        return ((rel[1] if len(rel) > 1 else (rel[0] if rel else 170)) + 2), 2.0
    if how == 'charge':
        go = event(tid, 'Input.keys.h = false', 1)
        if go is None:
            go = event(tid, 'Input.keys.h = false', 0)
        return (go + 3 if go is not None else 240), 2.0            # the ram leaves on the release
    return None, None


def ability_bar(p, k, a, lines, tid, how):
    t0, t1 = tb(k), tb(k + 1)
    lab = '%s  %s' % (p.upper(), ' + '.join(lines))
    ys = [218] if len(lines) == 1 else [210, 290]
    for line, yy in zip(lines, ys):
        E['overlays'].append(T(line, t0 + (BEAT if a == 0 else 0.0), t1, face='final',
                               h=fit(line, 'final', 1000, 78 if len(lines) == 1 else 64), y=yy, inn='slam', band=0.45,
                               tint=TINT[p]))
    sfx(t0 + (BEAT if a == 0 else 0.0), 'reviewed_special_pickup.wav', -6)      # the ability's name lands
    accent(t0, 1.1)
    if isinstance(tid, tuple):
        # Mike, on v6: "Showcase freezers thermoshock balls." One screen, two things: the time freeze for the first half
        # bar, then the thermoshock balls themselves - split fire/ice orbs spraying their shards - for the second.
        tid_a, tid_b = tid
        both = have(tid_a) and have(tid_b)
        t_mid = tb(k, 2.0) if both else t1
        if have(tid_a):
            mom, _b = ability_moment(p, tid_a, 'special')
            src = src_at(mom, tb(k, 1.0), t0) if mom is not None else free(tid_a, (t_mid - t0) + 0.1, score=gun)
            if src is not None:
                clip(t0, t_mid, [pane(tid_a, src, s0=1.0)], label=lab + ' (the freeze)', cont=a > 0)
                boom(tb(k, 1.0), 0.6)
        if have(tid_b):
            t_b0 = t_mid if both else t0
            srcb = free(tid_b, (t1 - t_b0) + 0.15, lo=weapon_lo(tid_b), score=gun)
            if srcb is not None:
                clip(t_b0, t1, [pane(tid_b, srcb, s0=1.0)], label=lab + ' (thermoshock balls)', cont=both or a > 0)
        return
    if not have(tid):
        clip(t0, t1, [], label=lab, cont=a > 0)
        return
    stop = t0 < SONG_STOP < t1
    mom, beat = ability_moment(p, tid, how)
    if mom is not None:
        src = (mom - 6) - (SONG_STOP - t0) * FPS if stop else src_at(mom, tb(k, beat), t0)
    else:
        src = free(tid, (t1 - t0) + 0.15, lo=weapon_lo(tid), score=gun)
        if src is None:
            clip(t0, t1, [], label=lab, cont=a > 0)
            return
    if stop:
        # THE SONG STOPS ON THIS BAR: hold the frame, desaturated, until the riff returns - then the hit lands
        f_stop = src + (SONG_STOP - t0) * FPS
        clip(t0, SONG_STOP, [pane(tid, src, s0=1.0)], label=lab, cont=a > 0)
        clip(SONG_STOP, SONG_BACK, [pane(tid, f_stop, s0=1.0, s1=1.05, ease='inout', hold=0.0, desat=0.75, gain=0.6, intense=True)],
             label='freeze on the stop', cont=True)
        clip(SONG_BACK, t1, [pane(tid, f_stop + 1, s0=1.05, s1=1.0, ease='out', intense=True)], label=lab + ' - after the stop', cont=True)
        boom(SONG_STOP, 0.8)
        sfx(SONG_STOP, 'explosion_air_medium.wav', -13)
        boom(SONG_BACK + 0.1, 1.1)
    else:
        # the charged boom is the one intense moment of an ability screen that is otherwise a still, full view: push in on
        # the ship as it winds up and lets go, or a full-power wave reads as a small green arc (measured in C_sonic's frames)
        zoom = (how == 'release')
        clip(t0, t1, [pane(tid, src, s0=1.0, s1=1.6 if zoom else None, ease='inout', track='player' if zoom else None,
                           lead=-140 if zoom else 0, intense=zoom)], label=lab, cont=a > 0)
        if mom is not None:
            boom(tb(k, beat), 0.9 if beat >= 1 else 0.6)


def pilots():
    """bar 11: the nine avatar boxes. bars 12-25: each pilot's screen, one ability per bar, secondaries included."""
    t11, t12 = tb(11), tb(12)
    lays = [I('brand/pav_%s.png' % p, t11 + j * BEAT / 4.0, t12, x=144 + 204 * j, y=430, prescale=0.75,
              resample='nearest', inn='slam', shadow=True) for j, p in enumerate(ORDER)]
    tt = tb(11, 2)
    lays.append(T('9 PILOTS', tt, t12, face='final', h=150, y=800, inn='slam'))
    clip(t11, t12, [], lays, label='9 PILOTS')
    for j in range(9):
        accent(t11 + j * BEAT / 4.0, 0.5)
    boom(tt, 1.2)
    sfx(tt, 'explosion_air_large.wav', -11)
    # Mike, on v4: "Ensure there is sound all the time." The grid is cards with no footage under it, so it carries the
    # pilot screen's own announcer and a console beep for every avatar that lands.
    sfx(t11 + 0.05, 'selectpilot.mp3', 2.0, duck=6.0)
    for j in range(9):
        sfx(t11 + j * BEAT / 4.0, 'nsp_console_beep.mp3', -8)
    k = 12
    for p in ORDER:
        abil = ABILITIES[p]
        t_p0, t_p1 = tb(k), tb(k + len(abil))
        name = p.upper()
        # the pilot's screen holds across all of their abilities: overlays, so a cut underneath cannot take it away
        E['overlays'].extend([
            I('brand/body_%s.png' % p, t_p0, t_p1, x=250, y=610, prescale=2.35, resample='nearest', inn='slide-l', shadow=True),
            I('brand/pav_%s.png' % p, t_p0 + BEAT * 0.5, t_p1, x=1672, y=560, prescale=1.45, resample='nearest',
              inn='slide-r', shadow=True),
            T(name, t_p0, t_p1, face='final', h=fit(name, 'final', 1000, 104), y=104, inn='slam', band=0.6, tint=TINT[p])])
        sfx(t_p0, 'whip.wav', -6)                  # the body and the avatar box slide in
        sfx(t_p0, 'flagPlant.wav', -4)             # the name lands
        for a, (lines, tid, how) in enumerate(abil):
            ability_bar(p, k + a, a, lines, tid, how)
        k += len(abil)


def minis():
    t26 = tb(26)
    if have('D_s3'):
        clip(t26, tb(27), [pane('D_s3', 36, s0=1.7, s1=2.0, cy=450)], label='ENEMY APPROACHING!')
    hit(t26, 'flash', 0.12, 0.45)
    accent(t26, 1.0)
    # five minibosses, two beats each - no stage 6 and no name cards (Mike, on v3)
    for j in range(5):
        tid = 'D_s%d' % (j + 1)
        t0, t1 = tb(27, 2 * j), tb(27, 2 * j + 2)
        if not have(tid):
            continue
        seen = entered(tid, 'sb')
        clip(t0, t1, [pane(tid, src_at(seen + 20, t0 + BEAT, t0), s0=1.0, s1=1.1, ease='inout')], label='MINI s%d' % (j + 1))
        accent(t0)
        boom(t0 + BEAT, 0.6)
    # Mike, on v6: "Show case our retinas and missiles" and "Showcase the new level 6 mini boss dual ship fight a little
    # bit" - the two split bars become the Razorback's Razor Rack (ten missiles queued on ONE retina) and the Tempest
    # Leviathan's jet duel. The splits stay as the fallback while a take is missing.
    alt = [('L_rack', "R.attack = 'missiles'", 20, 'RETINA LOCK - the Razor Rack salvo'),
           ('T_tempest', None, 0, 'TEMPEST LEVIATHAN duel (stage 6 mini - Mike, v6)')]
    for j, group in enumerate((('D2_s1', 'D2_s2'), ('D2_s3', 'D2_s4', 'D2_s5'))):
        t0, t1 = tb(29, 2 + 4 * j), tb(29, 6 + 4 * j)
        atid, needle, lead, alab = alt[j]
        if have(atid):
            # the SECOND rack: its retina arms inside the recording and the barrel roll breaks it - retina, missiles, escape
            ev = event(atid, needle, 1 if atid == 'L_rack' else 0) if needle else None
            if atid == 'T_tempest':
                # the duel's signature beat: the jet dives THROUGH the player's column behind its warning band
                ev = first(atid, lambda m: (m.get('tl') or [None])[0] == 'overtake', default=None)
                lead = -20
            src = (ev + lead) if ev is not None else free(atid, (t1 - t0) + 0.1)
            if src is not None:
                clip(t0, t1, [pane(atid, src, s0=1.0)], label=alab)
                accent(t0, 1.2)
                continue
        wp = 1920 // len(group)
        ps = []
        for r, tid in enumerate(group):
            if not have(tid):
                continue
            kill = event(tid, '__kill') or (nfr(tid) - 120)
            ps.append(pane(tid, free(tid, (t1 - t0) + 0.1, lo=0, hi=kill - 130), rect=(wp * r, 0, wp, 1080), s0=1.0,
                           bg='black', border=[10, 10, 12], gain=0.7))
        clip(t0, t1, ps, label='minis split (second pilots)')
        accent(t0, 1.2)
    kills = [t for t in ('D_s1', 'D_s2', 'D_s4', 'D_s5', 'D_s3') if have(t)]
    for j, tid in enumerate(kills):
        last = (j == len(kills) - 1)
        t0 = tb(31, 2 + j)
        t1 = tb(34) if last else tb(31, 3 + j)
        kill = event(tid, '__kill') or 450
        cy = kill_cy(tid, kill)
        clip(t0, t1, [pane(tid, src_at(kill + 4, t0 + 0.03, t0), s0=1.0 if last else 2.0,
                           s1=1.15 if last else 2.0, cy=cy, ease='inout', intense=True)], label='KILL %s' % tid)
        boom(t0, 1.0 if last else 0.75)


# (take, name, beats, camera scale). v4: the pilot-exclusive weapons - incendiary shotgun, heavy MG, sonic boom, ice
# breath, thermoshock - now sit on their own pilots' screens, so the arsenal is what anyone can pick up.
# v7 (Mike, on v6: "Laser mist is actually laser cannon. You need to showcase shadow orb and the actual laser mist too"):
# C_lasermist is re-filmed on a ground stage as the real LASER MIST; the space LASER CANNON and SHADOW ORB get their own
# takes. Ten weapon bars, one split bar - the arsenal keeps its eleven.
ARSENAL = [('C_spread', 'SPREAD FIRE', 4, 2.0), ('C2_mg', 'MACHINE GUN', 4, 1.0), ('C_missiles', 'MISSILES', 4, 2.0),
           ('C_laser', 'LASER', 4, 1.0), ('C_flame', 'FLAMETHROWER', 4, 2.0), ('C_fireorb', 'FIRE ORB', 4, 1.0),
           ('C_iceorb', 'ICE ORB', 4, 2.0), ('C_lasermist', 'LASER MIST', 4, 1.0), ('C_lasercannon', 'LASER CANNON', 4, 1.0),
           ('C_shadoworb', 'SHADOW ORB', 4, 1.0)]
GRANT = {'C_shotgun': 'dkGrant', 'C_turret': 'lzMountGrant', 'C_sonic': 'sonicGrant'}


def weapon_lo(tid):
    return (event(tid, GRANT[tid]) or 0) + 30 if tid in GRANT else 0


def arsenal():
    beat = 0.0
    for tid, name, beats, s in ARSENAL:
        t0, t1 = tb(34, beat), tb(34, beat + beats)
        beat += beats
        if not have(tid):
            continue
        src = free(tid, t1 - t0, lo=weapon_lo(tid), score=gun)
        # v7: the laser mist's synth bursts peak ~12x, so take levelling cuts the whole take 12 dB and the bar sat 22 dB under
        # the song - its own gain brings the weapon back up to where the other arsenal bars sit
        g = 2.2 if tid == 'C_lasermist' else None
        p = (pane(tid, src, s0=2.0, cy=640, track='player', lead=-170, gain=g) if s >= 2
             else pane(tid, src, s0=1.0, s1=1.05, ease='inout', gain=g))
        clip(t0, t1, [p], [T(name, t0 + 0.04, t1, face='final', h=fit(name, 'final', 1100, 80), x=90, y=985, anchor='l',
                              inn='slide-l', band=0.55)], label=name)
        accent(t0, 1.2)
        hit(t0, 'flash', 0.1, 0.22)
    for j, group in enumerate((('C_spread', 'C2_mg', 'C_laser'),)):
        t0, t1 = tb(44 + j), tb(45 + j)
        wp = 1920 // len(group)
        ps = [pane(tid, free(tid, (t1 - t0) + 0.1, lo=weapon_lo(tid), score=gun), rect=(wp * r, 0, wp, 1080), s0=1.0,
                   bg='black', border=[10, 10, 12], gain=0.6) for r, tid in enumerate(group) if have(tid)]
        clip(t0, t1, ps, label='arsenal split %d' % (j + 1))
        boom(t0, 0.8 if j < 2 else 0.9)


def boss_warning():
    t45, t46 = tb(45), tb(46)
    if have('E_s5'):
        # The game's ALERT carries the boss's own descriptor over the triangle ("ORBITAL SEED CARRIER"). Mike, on v3:
        # "Dont display the name of the bosses" - the camera takes the arrow and ALERT! and leaves that line out of frame.
        clip(t45, t46, [pane('E_s5', 44, s0=2.35, s1=2.6, cy=ALERT_CY, intense=True)], label='ALERT! boss warning')
    hit(t45, 'flash', 0.2, 0.6)
    for x in (91.93, 92.27, 92.60):
        hit(S(x), 'flash', 0.1, 0.3)
        accent(S(x))


ALERT_CY = 600       # measured on E_s5: the descriptor sits at playfield y 270-320, ALERT! at ~536


def warn_src(tid, k0, span, lo=0, hi=None, fam='rime'):
    """the first frame of `tid` where a laser warn of `fam` crosses k0 of its length with the next `span` seconds
    unclaimed. Mike, on v5: "When the alert frames show the laser about to fire. Use those new ones we got that were
    green yellow and red." capture3 logs every warn as metrics['lb'] = [family, fraction, released]; the game draws
    green for the first third, yellow for the second, red for the last, then fires.
    Checks CLAIMS only, never RESERVED: a shot pinned here reserved these frames in pass one, and asking RESERVED in
    pass two would find its own reservation and move it."""
    if not have(tid):
        return None
    M = meta(tid)['metrics']
    n = int(round(span * FPS))
    top = len(M) - n if hi is None else min(int(hi), len(M) - n)

    def k_at(i):
        lb = M[i].get('lb') if 0 <= i < len(M) else None
        return lb[1] if (lb and lb[0] == fam and not lb[2]) else None
    for i in range(max(1, int(lo)), max(1, top)):
        k, kp = k_at(i), k_at(i - 1)
        if k is not None and k >= k0 and (kp is None or kp < k0) and not overlap(tid, i, i + n):
            return i
    return None


def bosses():
    # five bosses - stage 6 is out entirely (Mike, on v3) - revealed with no name cards
    for j in range(5):
        tid = 'E_s%d' % (j + 1)
        t0, t1 = tb(46 + j), tb(47 + j)
        if j == 1 and have('E3_s2_form'):
            # Mike, on v6: "Please show the level 2 boss fully forming" - the chains reel the second arm and the head in
            # and the reactor surges, ending on the surge (~153 frames before the arms phase opens)
            arms = first('E3_s2_form', lambda m: m.get('fz') == 'arms', default=575)
            # v7: the head's chains reel it in, it locks, and the reactor SURGES - the bright beat, not the dark descent
            clip(t0, t1, [pane('E3_s2_form', max(0, arms - 215), s0=1.0)], letterbox=56, label='BOSS s2 forming')
            accent(t0, 1.2)
            boom(tb(46 + j, 1), 0.85)
            continue
        if not have(tid):
            continue
        seen = entered(tid, 'bo')
        src = src_at(seen + 20, tb(46 + j, 1), t0)
        if j == 2:
            # Mike, on v5: the level-3 boss's laser warns with the pack's FOV cones - the reveal lands on green going yellow
            src = warn_src(tid, 0.22, t1 - t0, lo=seen) or src
        clip(t0, t1, [pane(tid, src, s0=1.0, s1=1.12, ease='inout')], letterbox=56,
             label='BOSS s%d' % (j + 1))
        accent(t0, 1.2)
        boom(tb(46 + j, 1), 0.85)
    for j in range(5):
        tid = ['E2_s1', 'S2_falva', 'E2_s3', 'J_charge', 'E2_s5'][j]      # stages 2 and 4 from Falva's and Juggernaut's takes (balance)
        t0, t1 = tb(51 + j), tb(52 + j)
        # Mike, on v6: "... And attacking. And then it's seperate phases too." Three of the five vs bars go to the Furnace
        # Tyrant, each on the event that forced its phase through the real damage path.
        fz = {1: ('E3_s2_arms', "__fzt('right')", -80, 'vs FURNACE - the second arm breaks, the core opens'),
              3: ('E3_s2_core', "__fzt('body',0.55)", -40, 'FURNACE core phase'),
              4: ('E3_s2_head', "__fzt('head')", -90, 'FURNACE head flies alone, then dies')}.get(j)
        if fz and have(fz[0]):
            ev = event(fz[0], fz[1], 0)
            src = (ev + fz[2]) if ev is not None else free(fz[0], t1 - t0, score=boom_score)
            if src is not None:
                clip(t0, t1, [pane(fz[0], max(0, src), s0=1.0)], label=fz[3])
                boom(t0 + BEAT * 0.5, 0.7)
                continue
        if not have(tid):
            continue
        kill = event(tid, '__kill') or (nfr(tid) - 60)
        src = free(tid, t1 - t0, score=boom_score, hi=kill - 70)
        if tid == 'E2_s3':
            # ...and the vs shot on the red cones with the laser firing out of them before the cut
            src = warn_src(tid, 0.80, t1 - t0, hi=kill - 70) or src
        clip(t0, t1, [pane(tid, src, s0=1.0 if j % 2 == 0 else 2.0, cy=480)], label='vs boss %s' % tid)
        boom(t0 + BEAT * 0.5, 0.7)
    for j, tid in enumerate(['E_s4', 'E_s2', 'E_s5', 'E_s1']):
        t0, t1 = tb(56, j / 2.0), tb(56, (j + 1) / 2.0)
        if not have(tid):
            continue
        kill = event(tid, '__kill') or 450
        src = free(tid, t1 - t0 + 0.05, score=lambda m: (m.get('eb') or 0) + 2 * (m.get('ex') or 0), hi=kill - 40)
        clip(t0, t1, [pane(tid, src, s0=2.0 if j % 2 else 1.0, cy=500)], label='escalate %s' % tid)
        accent(t0)
    g = pick('G_death', 'G_death2')    # Decker's highway death carries the stop; Falva's the last hit
    if g:
        hitf = event(g, '__realHit') or 0
        t0 = tb(56, 2)
        cy = meta(g)['metrics'][max(0, hitf)]['py'] * 2 - 120
        clip(t0, tb(57), [pane(g, src_at(hitf, t0 + 0.08, t0), s0=2.0, cy=cy, intense=True)], label='SHIP DESTROYED (header rule)')
        boom(t0 + 0.08, 1.0)


STABS = [118.57, 121.34, 121.93, 122.6, 122.77, 123.1, 123.95, 125.30]


def stop_time():
    g = pick('G_death', 'G_death2')    # Decker's highway death carries the stop; Falva's the last hit
    t57, stab0 = tb(57), S(STABS[0])
    if g:
        hitf = event(g, '__realHit') or 0
        th = tb(56, 2) + 0.08
        src = src_at(hitf, th, tb(56, 2)) + (t57 - tb(56, 2)) * FPS
        cy = meta(g)['metrics'][max(0, hitf)]['py'] * 2 - 120
        t_crash = max(t57 + 0.1, th + 1.22)
        clip(t57, t_crash, [pane(g, src, s0=2.0, cy=cy, intense=True)], label='spin -> crash', cont=True)
        clip(t_crash, stab0, [pane(g, src + (t_crash - t57) * FPS, s0=2.0, s1=2.45, cy=cy, ease='inout', speed=0.18,
                                   desat=0.6, intense=True)], label='grey slow motion through the stop', cont=True)
    shots = [('E2_s1', 'kill'), ('E2_s2', 'kill'), ('E2_s3', 'kill'), ('E2_s4', 'kill'), ('E2_s5', 'kill'),
             ('D2_s5', 'kill'), ('S2_cole', 2), ('S2_lizzie', 2)]
    for j, (x, (tid, kind)) in enumerate(zip(STABS, shots)):
        t0 = S(x)
        t1 = S(STABS[j + 1]) if j + 1 < len(STABS) else tb(63)
        if not have(tid):
            continue
        if kind == 'kill':
            f = (event(tid, '__kill') or 450) + 4
            cy, s0 = kill_cy(tid, f - 4), 2.0
        else:
            p = tid.split('_', 1)[1]
            f = moment(p, 2, kind)[1]
            cy, s0 = (kill_cy(tid, f), 1.8) if p == 'cole' else (420, 1.0)
        gap, last = t1 - t0, (j == len(STABS) - 1)
        play = gap if last else (1.0 if gap > 1.2 else min(0.42, gap * 0.6))
        clip(t0, t0 + play, [pane(tid, f, s0=s0, cy=cy, intense=True)], label='STAB %s' % tid)
        if not last and gap - play > 0.05:
            if gap > 1.2:
                clip(t0 + play, t1, [pane(tid, f + play * FPS, s0=s0, s1=s0 * 1.08, cy=cy, ease='inout', speed=0.35,
                                          desat=0.45, intense=True)], label='grey slow motion %s' % tid, cont=True)
            else:
                clip(t0 + play, t1, [pane(tid, f + play * FPS, s0=s0, s1=s0 * 1.06, cy=cy, ease='inout', hold=0.0,
                                          desat=0.55, gain=0.6, intense=True)], label='freeze %s' % tid, cont=True)
        boom(t0, 1.0)
        sfx(t0, 'explosion_boss_core.wav', -16)


def taglines():
    """Mike, on v4: "Explain that there are 8 levels, 18 bosses, 1 hell of a campaign." Three statements slammed on the
    stop-time hits - the first stab, the second-to-last and the last - each over its own kill or strike."""
    for text, t0, t1 in (('8 LEVELS', S(STABS[0]), S(STABS[1])),
                         ('18 BOSSES', S(STABS[6]), S(STABS[7])),
                         ('1 HELL OF A CAMPAIGN', S(STABS[7]), tb(63))):
        E['overlays'].append(T(text, t0, t1, face='final', h=fit(text, 'final', 1560, 170), y=540, inn='slam', band=0.62))
        sfx(t0, 'explosion_air_large.wav', -12)


def climax():
    # bar 63 - eight one-beat cuts across eight pilots
    beats = [('F_s1', None), ('W_warp', 3), ('F_s2', None), ('S1_yuri', None), ('F_s3', None), ('W_warp', 5),
             ('F_s5', None), ('F_s6', None)]
    for j, (tid, gate) in enumerate(beats):
        t0, t1 = tb(63, j), tb(63, j + 1)
        if not have(tid):
            continue
        if gate:
            gp = gate_pass(gate)
            src = src_at(gp, t0 + 0.12, t0) if gp is not None else None
        else:
            src = free(tid, t1 - t0 + 0.05, score=boom_score if tid.startswith('F_') else special_score)
        clip(t0, t1, [pane(tid, src, s0=2.0 if j % 2 == 0 else 1.0, cy=560, track='player' if tid.startswith('F_') else None,
                           lead=-120)], label='beat %s' % tid)
        accent(t0, 1.2)
    # bar 65 - eight split pairs, sixteen panes
    pairs = [('S1_axel', 'S1_decker'), ('C_mg', 'C_missiles'), ('S1_freezer', 'S1_juggernaut'), ('F_s4', 'C_spread'),
             ('S1_falva', 'S1_maverick'), ('C_fireorb', 'C_iceorb'), ('S1_cole', 'S1_lizzie'), ('C_thermo', 'C_turret')]
    for j, pair in enumerate(pairs):
        t0, t1 = tb(65, j), tb(65, j + 1)
        ps = [pane(tid, free(tid, t1 - t0 + 0.05, score=boom_score, lo=weapon_lo(tid)), rect=(960 * r, 0, 960, 1080),
                   s0=1.0, bg='black', border=[10, 10, 12], gain=0.7) for r, tid in enumerate(pair) if have(tid)]
        clip(t0, t1, ps, label='split %s' % '|'.join(pair))
        accent(t0, 1.0)
    # bar 67 - four three-ways
    triples = [('S2_axel', 'S2_decker', 'S2_yuri'), ('E2_s1', 'E2_s3', 'E2_s5'), ('C_sonic', 'C_shotgun', 'C_lasermist'),
               ('S2_falva', 'S2_freezer', 'S2_juggernaut')]
    for j, tri in enumerate(triples):
        t0, t1 = tb(67, 2 * j), tb(67, 2 * j + 2)
        ps = []
        for r, tid in enumerate(tri):
            if not have(tid):
                continue
            hi = (event(tid, '__kill') or nfr(tid)) - 50 if tid.startswith('E2') else None
            ps.append(pane(tid, free(tid, t1 - t0 + 0.05, score=boom_score, lo=weapon_lo(tid), hi=hi),
                           rect=(640 * r, 0, 640, 1080), s0=1.0, bg='black', border=[10, 10, 12], gain=0.6))
        clip(t0, t1, ps, label='three-way %s' % '|'.join(tri))
        boom(t0, 0.6)
    # bar 69 - nine specials at once, third windows, half speed so a short free window fills the bar
    ps = []
    for j, p in enumerate(ORDER):
        tid = 'S%d_%s' % (1 if j % 2 == 0 else 2, p)
        if not have(tid):
            continue
        ps.append(pane(tid, free(tid, (tb(70) - tb(69)) * 0.55 + 0.05, score=special_score), rect=(640 * (j % 3), 360 * (j // 3), 640, 360),
                       s0=0.62, cy=560, bg='black', border=[10, 10, 12], speed=0.55, gain=0.4))
    clip(tb(69), tb(70), ps, label='nine specials (third windows)')
    boom(tb(69), 1.0)
    # bar 70 - six boss deaths (Mike, on v3: no stage-6 bosses at all)
    ps = []
    for j, tid in enumerate(['E_s1', 'E_s2', 'E_s3', 'E_s4', 'E_s5', 'D2_s3']):
        if have(tid):
            f = (event(tid, '__kill') or 450) - 6
            ps.append(pane(tid, f, rect=(640 * (j % 3), 540 * (j // 3), 640, 540), s0=0.75, cy=kill_cy(tid, f), bg='black',
                           border=[10, 10, 12], gain=0.5))
    clip(tb(70), tb(71), ps, label='six boss deaths')
    boom(tb(70), 1.1)
    # bar 71 - the nine avatar boxes on the half beats, blasts between them
    blasts = ['S2_freezer', 'S2_axel', 'C_thermo', 'S2_maverick', 'S2_falva', 'S2_decker', 'S2_yuri']
    bg = 'F_s6' if have('F_s6') else None
    bg0 = free(bg, tb(73) - tb(71) + 0.1, score=action) if bg else None      # ONE backdrop, played straight through
    slots = [0, 2, 4, 6, 8, 10, 12, 14, 15]
    bi = 0
    for j in range(16):
        t0, t1 = tb(71, j / 2.0), tb(71, (j + 1) / 2.0)
        if j in slots:
            p = ORDER[slots.index(j)]
            lay = [I('brand/pav_%s.png' % p, t0, t1, y=540, prescale=2.5, resample='nearest', inn='slam', shadow=True)]
            panes = [pane(bg, bg0 + (t0 - tb(71)) * FPS, s0=1.0, desat=0.4, tint=[0, 0, 0, 0.72], bgonly=True, gain=0.0)] if bg0 is not None else []
            clip(t0, t1, panes, lay, label='portrait %s' % p)
            hit(t0, 'flash', 0.08, 0.18)
        else:
            tid = blasts[bi % len(blasts)]
            bi += 1
            if not have(tid):
                continue
            f = free(tid, t1 - t0 + 0.05, score=boom_score, lo=weapon_lo(tid))
            clip(t0, t1, [pane(tid, f, s0=2.0, cy=kill_cy(tid, f) if f is not None else 420, intense=True)], label='blast %s' % tid)
            accent(t0, 1.4)
    # bar 73 - the campaign map, the warp jump, a helix release, a stage in full cry
    t = [tb(73, j) for j in range(5)]
    if have('A_mapfly'):
        # stage to stage on the map in pieces, nav ping inside the shot. The drop-down this used to show was the EXIT
        # confirm, which put "RETURN TO MAIN MENU" in the climax of a trailer.
        hop = event('A_mapfly', "'d'", 1) or 135
        clip(t[0], t[1], [pane('A_mapfly', hop - 2, s0=1.0, s1=1.15, ease='inout', gain=0.9)], label='campaign map: stage to stage')
    rift = warp_phase('draw')
    if rift is not None:
        clip(t[1], t[2], [pane('W_warp', rift + 50, s0=1.0, s1=1.15, ease='in', intense=True)], label='WARP DRIVE jump')
    tid, mom, _ = moment('maverick', 1, 2)
    if tid:
        clip(t[2], t[3], [pane(tid, src_at(mom, t[2] + 0.1, t[2]), s0=1.0)], label='helix release (third)')
    if have('F_s2'):
        clip(t[3], t[4], [pane('F_s2', free('F_s2', t[4] - t[3] + 0.05, score=boom_score), s0=2.0, cy=600)], label='F_s2 blast')
    for tt in t[:4]:
        boom(tt, 0.8)
    # bar 74 - a half-beat strobe, every cut a white hit
    strobe = [('S1_cole', 1), ('D2_s2', 'kill'), ('S1_lizzie', 1), ('D2_s4', 'kill'), ('D2_s1', 'kill'), ('S2_juggernaut', 'free'),
              ('F_s5', 'free'), ('W_warp', 'gate8')]
    for j, (tid, kind) in enumerate(strobe):
        t0, t1 = tb(74, j / 2.0), tb(74, (j + 1) / 2.0)
        if not have(tid):
            continue
        if kind == 'kill':
            k = event(tid, '__kill') or 420
            f, cy, s = k + 12, kill_cy(tid, k), 2.0
        elif kind == 'gate8':
            f, cy, s = gate_pass(8), 560, 1.0
        elif kind == 'free':
            f = free(tid, t1 - t0 + 0.05, score=boom_score)
            cy, s = 520, 2.0
        else:
            p = tid.split('_', 1)[1]
            f, cy, s = past_white(tid, moment(p, 1, kind)[1] + 8, t1 - t0), 420, 1.0
        clip(t0, t1, [pane(tid, f, s0=s, cy=cy, intense=True)], label='strobe %s' % tid)
        hit(t0, 'flash', 0.07, 0.5 if j % 2 == 0 else 0.3)
        accent(t0, 1.3)
    # the last four hits before the logo
    final = [(bar(75), 'G_death2', 'die'), (152.03, 'S1_cole', 2), (152.53, 'S1_lizzie', 2), (152.70, 'C2_missiles', 'free')]
    for j, (x, tid, kind) in enumerate(final):
        t0 = S(x)
        t1 = S(final[j + 1][0]) if j + 1 < len(final) else S(153.38)
        if not have(tid):
            continue
        if kind == 'die':
            hf = event(tid, '__realHit') or 0
            clip(t0, t1, [pane(tid, hf + 30, s0=2.0, cy=meta(tid)['metrics'][max(0, hf)]['py'] * 2 - 120, intense=True)], label='death spin')
        elif kind == 'free':
            clip(t0, t1, [pane(tid, free(tid, t1 - t0 + 0.05, score=boom_score), s0=2.0, cy=600, intense=True)], label='last blast %s' % tid)
        else:
            p = tid.split('_', 1)[1]
            clip(t0, t1, [pane(tid, past_white(tid, moment(p, int(tid[1]), kind)[1] - 2, t1 - t0), s0=1.0)], label='%s strike' % p)
        boom(t0, 0.9)


def end_card():
    tF = S(153.38)
    bg = pick('A_mapboot')
    panes = [pane(bg, min(nfr(bg) - 1, 560), s0=1.0, s1=1.1, ease='inout', desat=0.35, tint=[0, 0, 0, 0.8], bgonly=True, gain=0.0)] if bg else []
    lays = [I('brand/nbl_logo.png', tF, LENGTH, y=440, prescale=2.1, inn='slam', shadow=True, drift=0.006),
            T('COMING SOON', S(155.9), LENGTH, face='final', h=86, y=850, inn='rise'),
            T('BUILT WITH THE ASSISTANCE OF AI & HUMAN TOOLS.', S(157.0), LENGTH, face='final', h=44, y=935, inn='fade', fade=0.5),
            I('brand/cf_logo.png', S(156.6), LENGTH, y=1012, prescale=0.12, inn='fade', fade=0.6)]
    clip(tF, LENGTH, panes, lays, fade_out=1.2, label='END CARD')
    boom(tF, 1.6)
    hit(tF, 'flash', 0.5, 1.0)
    sfx(tF, 'explosion_boss_core.wav', -5)
    sfx(S(156.6), 'cf_boot.mp3', -1)


def coverage():
    fr = int(LENGTH * FPS)
    cov = bytearray(fr)
    for c in E['clips']:
        for f in range(int(round(c['t0'] * FPS)), min(fr, int(round(c['t1'] * FPS)))):
            cov[f] += 1
    gaps, overlaps, f = [], [], 0
    while f < fr:
        if cov[f] != 1:
            g, v = f, cov[f]
            while f < fr and cov[f] == v:
                f += 1
            (gaps if v == 0 else overlaps).append((round(g / FPS, 2), round(f / FPS, 2)))
        else:
            f += 1
    return gaps, overlaps


def report():
    per, shots, runs = {}, {}, []
    prev, prev_label = None, None
    for (t0, t1, subj, label, cont) in sorted(SHOTS, key=lambda s: (s[0], s[1])):
        wgt = (t1 - t0) / max(1, len(subj))
        for p in subj:
            if p:
                per[p] = per.get(p, 0.0) + wgt
                if not cont:
                    shots[p] = shots.get(p, 0) + 1
        if cont:                                   # a freeze or slow-motion tail is screen time, not a new shot
            continue
        one = subj[0] if len(subj) == 1 else None
        if one and prev == one:
            runs.append('%.2fs %s twice: %s -> %s' % (t0, one, prev_label, label))
        prev, prev_label = one, label
    lines = ['pilot screen time (split panes share their shot):']
    for p in sorted(per, key=lambda k: -per[k]):
        lines.append('  %-11s %5.1fs over %3d panes' % (p, per[p], shots[p]))
    used = sorted({p['take'] for c in E['clips'] for p in c['panes']})
    lines.append('takes used: %d of %d recorded' % (len(used), len([t for t in SPECS if have(t)])))
    lines.append('back-to-back same pilot: %s' % (runs or '-'))
    lines.append('footage conflicts (a frame shown twice): %d' % len(CONFLICTS))
    lines += ['  ' + c for c in CONFLICTS[:40]]
    return '\n'.join(lines)


def build():
    E.clear()
    E.update({'clips': [], 'overlays': [], 'hits': []})
    del SFX[:], CUTS[:], SHOTS[:], CONFLICTS[:]
    CLAIMS.clear()
    for section in (intro, menus, boom_montage, pilots, minis, arsenal, boss_warning, bosses, stop_time, taglines, climax, end_card):
        section()


BEDS = {1: 'amb_jungle.mp3', 2: 'amb_volcanic.mp3', 3: 'amb_arctic.mp3', 4: 'amb_airbase.mp3', 5: 'amb_airbase.mp3',
        6: 'amb_storm.mp3', None: 'amb_airbase.mp3'}


def beds():
    """one stage ambience per clip, from its first real pane's take - mix3 lays it under everything and ducks it under
    the game, so no moment of the trailer is ever silent (Mike, on v4: "Ensure there is sound all the time")"""
    out = []
    for c in sorted(E['clips'], key=lambda c: c['t0']):
        stage = None
        for p in c['panes']:
            if not p.get('bgonly'):
                stage = SPECS.get(p['take'], {}).get('stage')
                break
        out.append({'t0': c['t0'], 't1': c['t1'], 'file': os.path.join(SND, BEDS.get(stage, BEDS[None]))})
    return out


def main():
    RESERVE[0] = True                       # pass one: only the shots pinned to a moment claim their frames
    build()
    RESERVED.update({k: list(v) for k, v in CLAIMS.items()})
    RESERVE[0] = False
    build()
    E['audio'] = {'length': LENGTH, 't0': T0, 'song': SONG, 'song_gain_db': -6.3, 'song_fade_in': 0.45, 'song_end': None,
                  'chime': {'file': os.path.join(SND, 'cf_boot.mp3'), 't': 0.55, 'gain_db': -0.6},
                  'sfx': SFX, 'fade_out': 1.2, 'takes_dir': TAKES_DIR, 'beds': beds()}
    out = os.path.join(HERE, 'edl3.json')
    json.dump(E, open(out, 'w'), indent=0)
    with open(os.path.join(HERE, 'cutlist_v3.txt'), 'w') as fh:
        for t, label in sorted(CUTS):
            fh.write('%7.2f  (song %6.2f)  %s\n' % (t, t - T0, label))
    gaps, overlaps = coverage()
    print('%d clips, %d hits, %d accents -> %s' % (len(E['clips']), len(E['hits']), len(SFX), out))
    print('missing takes: %s' % (sorted(MISSING) or '-'))
    print('gaps (black): %s' % (gaps or '-'))
    print('overlaps: %s' % (overlaps or '-'))
    print(report())


if __name__ == '__main__':
    main()
