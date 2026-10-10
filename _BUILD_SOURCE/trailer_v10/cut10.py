# cut10.py - the v10 cut itself, exec'd at the end of edit10.py (all of edit9's helpers are in scope).
# Times are tb(bar, beat) on Gasline's measured grid; every shot is live footage with the game's own sound under it.

GOLD, ICE, FIRE = 'final', '6', '2'
DIFF_LOOK = [('normal', 'EASY / NORMAL', '#3a8aff', ICE), ('hard', 'HARD', '#ff8a1c', 'final'), ('furious', 'FURIOUS', '#ff2a2a', FIRE)]


def clean(sc, k=900):
    """a score that refuses white hit-flash silhouettes outright (raw pixel whiteness, whiteness9.py)"""
    return lambda m: sc(m) - k * (m.get('wr') or 0)


def half(bar, k):
    """the k-th half-bar slot from bar `bar`"""
    return tb(bar, 2 * k), tb(bar, 2 * k + 2)


def frame_of_event(tid, needle, default=0):
    m = meta(tid)
    if not m:
        return default
    ks = sorted(int(k) for k, v in (m.get('event_idx') or {}).items() if needle in v)
    return ks if ks else default


def snd_frames(tid, name):
    try:
        ae = json.load(open(os.path.join(TAKES_DIR, tid, 'audio_events.json')))
        return sorted(e[0] - ae['rec0'] for e in ae['snd'] if e[1] == name and ae['rec0'] is not None)
    except (OSError, ValueError, TypeError):
        return []


# ====================================================================================================================
#  BAR 1: the ColeForge plate
# ====================================================================================================================
black(0.0, tb(2), label='COLEFORGE',
      layers=[image(0.08, tb(2) - 0.04, 'brand/cf_logo.png', y=530, prescale=0.62, kin='fade', out='fade', fade=0.45,
                    fade_out=0.25, drift=0.015, overlay=False)])

# ====================================================================================================================
#  BARS 2-5: the cold open - eight half-bar shots, the hardest the game gets
# ====================================================================================================================
COLD = [('Z_forms', montage_score, cam(1.0, 1.15, ease='inout')), ('M_uber', action, cam(1.0, 1.0)),
        ('S6R_rebfight', busy, cam(1.0, 1.1)), ('B_s5b', fight_score, cam(1.2, 1.35, track='target', lead=150)),
        ('V_sov_furious', boom, cam(1.0, 1.0)), ('B_s2b', fight_score, cam(1.0, 1.1)),
        ('Z_drone', montage_score, cam(1.1, 1.25, track='target', lead=140)), ('B_s7b', fight_score, cam(1.0, 1.0))]
for i, (tid, sc, c) in enumerate(COLD):
    a, b = half(2, i)
    shot(a, b, tid, score=sc, label='cold open ' + tid, c=c)
    hit(a, 'punch', 0.12, 0.03)
hit(tb(2), 'flash', 0.16, 0.8)

# ====================================================================================================================
#  BAR 6: the dip - Dracodia speaks from the void
# ====================================================================================================================
shot(tb(6), tb(7), 'Z_void', lo=900, hi=1500, score=lambda m: 1, label='the void: Dracodia speaks', subject=None,
     c=cam(1.0, 1.08, ease='inout'))

# ====================================================================================================================
#  BARS 7-8: BULLETS OF FURY
# ====================================================================================================================
shot(tb(7), tb(9), 'A_title', src=40, label='BULLETS OF FURY slam', subject=None, desat=0.4, tint=[0, 0, 0, 0.72],
     c=cam(1.25, 1.32, cy=600, ease='inout'),
     layers=[image(tb(7), tb(9), 'brand/bof_logo.png', y=520, prescale=0.80, kin='slam', out='cut', drift=0.02, overlay=False)])
hit(tb(7), 'flash', 0.2, 1.0)
hit(tb(7), 'shake', 0.5, 18)

# ====================================================================================================================
#  BARS 9-14: 9 PILOTS - the line-up, then one half bar each on their special
# ====================================================================================================================
lineup = []
xs = [W * (i + 0.5) / 9 for i in range(9)]
for i, p in enumerate(PILOTS):
    lineup.append(image(tb(9, i * 0.25), tb(10), 'brand/body_%s.png' % p, x=xs[i], y=760,
                        prescale=body_prescale(p, 430), kin='rise', out='cut', overlay=False))
    lineup.append(image(tb(9, i * 0.25), tb(10), 'brand/pav_%s.png' % p, x=xs[i], y=420, prescale=0.75,
                        kin='rise', out='cut', resample='nearest', overlay=False))
black(tb(9), tb(10), label='9 PILOTS line-up', layers=lineup + [text(tb(9), tb(10), '9 PILOTS', height=150, y=200, overlay=False)])
hit(tb(9), 'flash', 0.14, 0.75)
PILOT_ORDER = ['cole', 'lizzie', 'juggernaut', 'falva', 'maverick', 'yuri', 'decker', 'freezer', 'axel']
for i, p in enumerate(PILOT_ORDER):
    a, b = half(10, i)
    tid = 'P_' + p
    if not have(tid):
        continue
    sp0 = first(tid, lambda m: bool(m.get('sp')), default=10)
    src_p = best(tid, frames_for(a, b), special_score if p == 'lizzie' else special_view, lo=max(0, sp0 - 4), hi=sp0 + 150)
    lay = [text(a, b, p.upper(), height=110, y=88, tint=PILOT_TINT[p], band=0.55, overlay=False),
           image(a, b, 'brand/pav_%s.png' % p, x=250, y=820, prescale=1.05, kin='slide-l', resample='nearest', overlay=False),
           image(a, b, 'brand/body_%s.png' % p, x=1700, y=640, prescale=body_prescale(p, 560), kin='slide-r', overlay=False)]
    shot(a, b, tid, src=src_p, label='%s special' % p, layers=lay, c=cam(1.0, 1.1, track='player', lead=-220))
    hit(a, 'punch', 0.14, 0.035)

# ====================================================================================================================
#  BARS 14.5-20: 10 STAGES - the card on the beat, the stage itself on the next
# ====================================================================================================================
t_st = tb(14, 2)
shot(t_st, tb(16), 'C_mapfly', src=10, label='10 STAGES over the campaign map', subject=None, desat=0.3,
     tint=[0, 0, 0, 0.5], c=cam(1.0, 1.1, ease='inout'),
     layers=[text(t_st, tb(16), '10 STAGES', height=170, y=540, band=0.5, overlay=False)])
hit(t_st, 'flash', 0.14, 0.75)
STAGE_PLAY = {1: 'G_s1', 2: 'G_s2', 3: 'G_s3', 4: 'G_s4', 5: 'G_s5', 6: 'S6R_assault', 7: 'G_s7', 8: 'G_s8', 9: 'G_s9'}
for k_, n in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 10, 9]):
    a, m_, b = tb(16, 2 * k_), tb(16, 2 * k_ + 1), tb(16, 2 * k_ + 2)
    if n == 10:
        shot(a, m_, 'X_rival_map', src=150, label='STAGE X on the map', subject=None, c=cam(1.15, 1.2, cy=700),
             layers=[text(a, m_, 'STAGE X', height=150, y=420, band=0.5, overlay=False)])
        shot(m_, b, 'X_rx_duel', score=busy, label='STAGE X duel', c=cam(1.0, 1.0))
    else:
        shot(a, m_, 'F_card_s%d' % n if n != 8 else 'F_card_s8b', src=48, label='stage %d card' % n, subject=None,
             c=cam(1.28, 1.32, cy=505))
        shot(m_, b, STAGE_PLAY[n], score=busy, label='stage %d play' % n, c=cam(1.0, 1.0))
    hit(a, 'punch', 0.12, 0.03)

# ====================================================================================================================
#  BARS 21-26: EASY/NORMAL - HARD - FURIOUS, one miniboss three ways; then the break
# ====================================================================================================================
for i, (d, word, col, face) in enumerate(DIFF_LOOK):
    a, b = tb(21 + i), tb(22 + i)
    tid = 'V_rzb_' + d
    shot(a, b, tid, score=fight_score, lo=110, label='difficulty ' + word,
         c=cam(1.0, 1.06, ease='inout'),
         layers=[text(a, b, word, face=face, height=130, y=965, tint=None, band=0.6, overlay=False)])
    hit(a, 'flash', 0.12, 0.55)
a, b = tb(24), tb(25)
_n3 = frames_for(a, b)
split(a, b, [('V_rzb_normal', best('V_rzb_normal', _n3, fight_score, lo=120), None, cam(1.0, 1.0), 0.4),
             ('V_rzb_hard', best('V_rzb_hard', _n3, fight_score, lo=120), None, cam(1.0, 1.0), 0.4),
             ('V_rzb_furious', best('V_rzb_furious', _n3, fight_score, lo=120), None, cam(1.0, 1.0), 0.5)], label='difficulty triptych',
      layers=[text(a, b, w, face=f, height=70 if i == 0 else 84, x=W * (i + 0.5) / 3, y=1000, overlay=False)
              for i, (_, w, c, f) in enumerate(DIFF_LOOK)])
hit(a, 'punch', 0.2, 0.04)
# the Frost Cruiser grows 35% and turns black and royal blue on Hard; the Overlord's four-pass frenzy on Furious
a, b = tb(25), tb(25, 1)
split(a, b, [('V_frost_normal', None, fight_score, cam(1.0, 1.0), 0.45), ('V_frost_hard', None, fight_score, cam(1.0, 1.0), 0.45)],
      label='frost cruiser normal | hard',
      layers=[text(a, b, 'NORMAL', face=ICE, height=70, x=W * 0.25, y=1000, overlay=False),
              text(a, b, 'HARD', height=80, x=W * 0.75, y=1000, overlay=False)])
# the song's break: the claim typed on black
tbr = tb(25, 1)
black(tbr, tb(26, 1), label='20 BOSSES (break)')
typed(tbr + 0.05, tb(26, 1), '20 BOSSES', rate=0.07, height=150, y=540)
a, b = tb(26, 1), tb(27)
shot(a, b, 'V_sov_furious', score=fight_score, label='FURIOUS: the Storm Sovereign', c=cam(1.0, 1.0),
     layers=[text(a, b, 'FURIOUS', face=FIRE, height=110, y=980, overlay=False)])
hit(a, 'flash', 0.18, 0.9)
hit(a, 'shake', 0.4, 12)

# ====================================================================================================================
#  BARS 27-34: the boss montage on the half bar
# ====================================================================================================================
B_ORDER = ['B_s1b', 'B_s2m', 'B_s2b', 'V_frost_hard', 'B_s3b', 'B_s4m', 'B_s4b', 'B_s5b', 'B_s5m', 'S6L_harrier', 'B_s7m', 'B_s7b',
           'B_s8m', 'B_s9m', 'B_s9b', 'V_ovl_furious']
for i, tid in enumerate(B_ORDER):
    a, b = half(27, i)
    c = cam(1.0, 1.1, ease='inout') if i % 2 == 0 else cam(1.15, 1.3, track='target', lead=150)
    shot(a, b, tid, score=clean(montage_score, 3000 if tid == 'S6L_harrier' else 900), lo=1100 if tid == 'S6L_harrier' else 0, label='boss montage ' + tid, c=c)
    hit(a, 'punch', 0.12, 0.03)
hit(tb(27), 'flash', 0.18, 0.85)
hit(tb(31), 'flash', 0.12, 0.5)

# ====================================================================================================================
#  BARS 35-36: MISSILE VOLLEY GALORE
# ====================================================================================================================
a, b = tb(35), tb(36)
shot(a, b, 'M_uber', score=lambda m: (m.get('pb') or 0) + boom(m), lo=0, label='UBER missiles on Retina locks',
     c=cam(1.0, 1.15, ease='inout'), layers=[text(a, tb(35, 2), 'LOCK ON', height=120, y=880, overlay=False),
                                             text(tb(35, 2), b, 'LET IT RAIN', face=FIRE, height=120, y=880, overlay=False)])
hit(a, 'flash', 0.14, 0.7)
shot(*half(36, 0), 'M_rack', score=lambda m: (m.get('pb') or 0) + boom(m), label='ultra missile salvo', c=cam(1.0, 1.0))
shot(*half(36, 1), 'M_cole', score=clean(lambda m: boom(m) + (m.get('pb') or 0)), label='Cole nuclear strikes', c=cam(1.0, 1.1))

# ====================================================================================================================
#  BARS 37-46: 1 HELL OF A CAMPAIGN - stage 6: the carrier, the allies, the Rebels, the choice, the Harrier
# ====================================================================================================================
a, b = tb(37), tb(38)
shot(a, b, 'C_mapfly', lo=250, score=lambda m: 1, label='1 HELL OF A CAMPAIGN', subject=None, c=cam(1.0, 1.1, ease='inout'),
     desat=0.2, tint=[0, 0, 0, 0.4],
     layers=[text(a, b, '1 HELL OF A', height=110, y=430, band=0.5, overlay=False),
             text(a, b, 'CAMPAIGN', face=FIRE, height=180, y=590, overlay=False)])
hit(a, 'flash', 0.18, 0.85)
hit(a, 'shake', 0.4, 12)
shot(tb(38), tb(39), 'S6R_allies', score=busy, label='S6: the allies join', c=cam(1.0, 1.12, track='player', lead=-180))
shot(tb(39), tb(40), 'S6L_open', src=470, label='S6: the carrier flyover', c=cam(1.0, 1.0))
# the Rebel cutscene - the five Rebels hover over the squad while each one talks (live, protected radio)
shot(tb(40), tb(41), 'S6R_rebintro', src=325, label='REBELS: Voss', c=cam(1.0, 1.08, ease='inout'))
shot(tb(41), tb(42), 'S6R_rebintro', src=925, label='REBELS: Nyx', c=cam(1.08, 1.0, ease='inout'), cont=True)
shot(tb(42), tb(43), 'S6L_choice', src=20, label='S6: CHOOSE YOUR PURSUIT', c=cam(1.35, 1.5, cy=486, ease='inout'))
a, b = tb(43), tb(44)
r_bank = first('S6R_choice', lambda m: (m.get('s6') or [0, 0, None])[2] == 'right', default=200)
l_bank = first('S6L_choice', lambda m: (m.get('s6') or [0, 0, None])[2] == 'left', default=200)
split(a, b, [('S6L_choice', max(l_bank, 200), None, cam(1.0, 1.0), 0.5), ('S6R_choice', max(r_bank, 200), None, cam(1.0, 1.0), 0.5)],
      label='LEFT | RIGHT',
      layers=[text(a, b, 'LEFT', face=ICE, height=120, x=W * 0.25, y=960, overlay=False),
              text(a, b, 'RIGHT', face=FIRE, height=120, x=W * 0.75, y=960, overlay=False)])
hit(a, 'flash', 0.2, 0.9)
hit(a, 'shake', 0.5, 14)
shot(tb(44), tb(45), 'S6L_harrier', score=clean(fight_score, 3000), lo=60, hi=1000, label='the HARRIER', c=cam(1.0, 1.0),
     layers=[text(tb(44), tb(45), 'THE HARRIER', face=ICE, height=100, y=980, overlay=False)])
shot(tb(45), tb(46), 'S6R_rebfight', score=busy, label='THE REBELS: five against five', c=cam(1.0, 1.05),
     layers=[text(tb(45), tb(46), 'THE REBELS', face=FIRE, height=100, y=980, overlay=False)])
shot(*half(46, 0), 'S6L_harrier', score=clean(boom, 3000), lo=880, label='the Harrier falls', c=cam(1.0, 1.1))
shot(*half(46, 1), 'S6R_rebfight', score=busy, lo=700, label='Rebel fury', c=cam(1.1, 1.25, track='player', lead=-200))

# ====================================================================================================================
#  BARS 47-57: THE FINALE - the drone, the ghost, the void, Dracodia and his eight stolen forms
# ====================================================================================================================
shot(tb(47), tb(48), 'Z_drone', score=montage_score, hi=500, label='finale: the mutated drone', c=cam(1.0, 1.1),
     layers=[text(tb(47), tb(48), 'THE FINAL FIGHT', face=FIRE, height=100, y=980, overlay=False)])
hit(tb(47), 'flash', 0.16, 0.8)
shot(tb(48), tb(49), 'Z_ghost', score=clean(montage_score), lo=120, label='finale: the ghost in the code', c=cam(1.0, 1.1))
shot(tb(49), tb(50), 'Z_void', src=60, label='the void opens', subject=None, c=cam(1.0, 1.12, ease='inout'),
     layers=[text(tb(49), tb(50), 'INTO THE VOID', height=100, y=980, overlay=False)])
hit(tb(49), 'shake', 0.5, 10)
shot(tb(50), tb(51), 'Z_void', lo=300, hi=900, score=lambda m: 1, label='DRACODIA', subject=None, c=cam(1.1, 1.2, ease='inout'))
hit(tb(50), 'flash', 0.2, 0.9)
# eight transformations, half a bar each: the morph, then the form it took
MORPHS = [int(k) for k, v in sorted(((int(k), v) for k, v in (meta('Z_forms') or {}).get('event_idx', {}).items()))
          if 'j3Morph' in v] if have('Z_forms') else []
for i in range(8):
    a, b = half(51, i)
    if i < len(MORPHS):
        lo = MORPHS[i] + (40 if i % 2 == 0 else 150)
        shot(a, b, 'Z_forms', score=clean(montage_score), lo=lo, hi=lo + 200, label='Dracodia form %d' % (i + 1),
             c=cam(1.0, 1.12, ease='inout') if i % 2 else cam(1.15, 1.25, track='target', lead=150), cont=i > 0)
    hit(a, 'punch', 0.14, 0.035)
hit(tb(51), 'flash', 0.16, 0.7)
hit(tb(53), 'flash', 0.12, 0.5)
# the destruction: sun beams, opaque modules and charred wreckage
d0 = first('Z_death', lambda m: (m.get('sh') or 0) > 0 or (m.get('ex') or 0) > 3, default=60)
shot(tb(55), tb(56), 'Z_death', src=max(0, d0), label='Dracodia ruptures', c=cam(1.0, 1.1))
shot(tb(56), tb(58), 'Z_death', score=boom, lo=d0 + 200, label='the destruction', c=cam(1.1, 1.0, ease='inout'), cont=True)
hit(tb(55), 'flash', 0.2, 0.9)
hit(tb(55), 'shake', 0.8, 16)
hit(tb(57), 'flash', 0.2, 0.7)

# ====================================================================================================================
#  BAR 58: the claims, stacked over a quarter-beat recap
# ====================================================================================================================
RECAP = ['B_s4b', 'P_cole', 'S6R_rebfight', 'P_freezer', 'X_rx_duel', 'M_uber', 'B_s9b', 'P_yuri']
for i, tid in enumerate(RECAP):
    a, b = tb(58, i * 0.5), tb(58, i * 0.5 + 0.5)
    shot(a, b, tid, score=montage_score, label='recap ' + tid, c=cam(1.0, 1.0), desat=0.1)
CLAIMS = [('9 PILOTS', GOLD), ('10 STAGES', GOLD), ('20 BOSSES', GOLD), ('1 HELL OF A CAMPAIGN', FIRE)]
t_last = q(85.45)
for i, (s_, f) in enumerate(CLAIMS):
    text(tb(58, i), t_last, s_, face=f, height=92, y=300 + i * 150, kin='slam', out='cut', band=0.5)
    hit(tb(58, i), 'punch', 0.12, 0.03)

# ====================================================================================================================
#  THE SILENCE, THE LAST HIT, THE LOGO CARD
# ====================================================================================================================
t_logo = q(86.02)
black(t_last, t_logo, label='silence')
END = q(t_logo + 6.4)
black(t_logo, END, label='logo card', fade_out=1.4,
      layers=[image(t_logo, END, 'brand/bof_logo.png', y=400, prescale=0.66, kin='slam', drift=0.008, overlay=False),
              text(t_logo + 0.6, END, '11.1.26', height=110, y=735, kin='rise', overlay=False),
              text(t_logo + 1.1, END, 'STEAM / PC / MAC / LINUX', height=58, y=855, kin='fade', face=ICE, overlay=False),
              image(t_logo + 1.6, END, 'brand/copyright.png', y=965, prescale=0.8, kin='fade', shadow=False, overlay=False)])
hit(t_logo, 'flash', 0.22, 1.0)
hit(t_logo, 'shake', 0.45, 16)
LENGTH = END

AUDIO = {
    'length': LENGTH,
    't0': T0,
    'takes_dir': TAKES_DIR,
    'song': SONG,
    'song_gain_db': -6.3,
    'song_fade_in': 0.01,
    'song_fade_out': None,
    'music2': None,
    'chime': {'file': SND('sounds', 'cf_boot.mp3'), 't': 0.05, 'gain_db': -12.0},
    'sfx': SFX,
    'fade_out': 0.8,
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


edl = {'clips': CLIPS, 'overlays': OVERLAYS, 'hits': HITS, 'audio': AUDIO}
json.dump(edl, open(os.path.join(HERE, 'edl10.json'), 'w'), indent=1)
report()
