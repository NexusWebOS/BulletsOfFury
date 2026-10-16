# ====================================================================================================================
#  BAR 58: the claims, stacked over a quarter-beat recap (the song's last bar)
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
#  v11 ENDING (Mike, 1014): STOP! HAMMERTIME?! -> the Stage-5 boss on the HAMA soundtrack: the dance, STOP! with his
#  hand out, HAMMER - TIME!, a robot thrown at the pilot, then a robot thrown AT THE CAMERA, the glass cracks, the logo,
#  COMING NOVEMBER 2026, the copyright and the Phoenix engine line.
# ====================================================================================================================
SONG_END = q(T0 + BM['duration'] - 0.35)
black(t_last, SONG_END, label='the song lets go')
t_stop = q(SONG_END + 0.25)
black(SONG_END, t_stop, label='beat')
black(t_stop, t_stop + 0.95, label='STOP!', layers=[text(t_stop, t_stop + 0.95, 'STOP!', face='5', height=230, y=540,
                                                         kin='slam', overlay=False)])
hit(t_stop, 'shake', 0.35, 12)
hit(t_stop, 'flash', 0.1, 0.5)
sfx(t_stop, SND('sfx_0927', 'hammer_slam.mp3'), gain_db=-6.0)
t_ham = q(t_stop + 0.95)
t_cut = q(t_ham + 1.25)
black(t_ham, t_cut, label='HAMMERTIME?!', layers=[text(t_ham, t_cut, 'HAMMERTIME?!', face='5', height=200, y=540,
                                                       kin='slam', overlay=False)])
hit(t_ham, 'shake', 0.45, 16)
hit(t_ham, 'flash', 0.12, 0.6)
sfx(t_ham, SND('sfx_0927', 'hammer_slam.mp3'), gain_db=-4.0)
sfx(t_ham + 0.02, SND('sounds', 'expBig.mp3'), gain_db=-9.0)

HAMA = 'T_hama'
HAMA_SRC_T = None
logo_t0 = q(t_cut + 0.4)
if have(HAMA):
    Ms = M(HAMA)
    hc = [m.get('hc') for m in Ms]
    hm = [(m.get('hm') or [None, None]) for m in Ms]
    ae = json.load(open(os.path.join(TAKES_DIR, HAMA, 'audio_events.json')))
    slams = sorted(e[0] - ae['rec0'] for e in ae['snd'] if e[1] == 'hammerImpact' and e[0] >= ae['rec0'])
    # 1. the breakdown, on a beat of the song a little before the STOP
    want = 110.4
    k_beat = round((want - HAMA_PHASE) / HAMA_BEAT)
    tgt = HAMA_PHASE + k_beat * HAMA_BEAT
    hama_src = min(range(len(hc)), key=lambda i: abs((hc[i] or 0) - tgt))
    stop_f = next((i for i in range(hama_src, len(hm)) if hm[i][1] == 'stop'), hama_src + 300)
    slam2 = [s for s in slams if s > stop_f][:2]
    time_f = slam2[1] if len(slam2) > 1 else stop_f + 160
    end1 = time_f + int(round(1.2 * HAMA_BEAT * FPS))
    hama_t0 = t_cut
    t_stopcut = q(hama_t0 + (stop_f - 8 - hama_src) / FPS)
    t_end1 = q(hama_t0 + (end1 - hama_src) / FPS)
    shot(hama_t0, t_stopcut, HAMA, src=hama_src, label='HAMA: the dance - lasso, 360s, OH-OH', c=cam(1.0, 1.1, ease='inout'))
    shot(t_stopcut, t_end1, HAMA, src=stop_f - 8, cont=True, label='HAMA: STOP! (hand out) HAMMER - TIME!',
         c=cam(1.3, 1.45, track='target', lead=110))
    hit(hama_t0, 'flash', 0.12, 0.6)
    for sf in slam2:
        hit(hama_t0 + (sf - hama_src) / FPS, 'shake', 0.4, 18)
        hit(hama_t0 + (sf - hama_src) / FPS, 'flash', 0.1, 0.4)
    HAMA_SRC_T = hc[hama_src]
    # 2. the tosses after it: each is a run of mode 'toss'; inside it the pose walks windup -> ... -> hold -> thrown
    tosses, i = [], end1
    while i < len(hm):
        if hm[i][0] == 'toss':
            j = i
            while j < len(hm) and hm[j][0] == 'toss':
                j += 1
            hold = next((k for k in range(i, j) if hm[k][1] == 't:hold'), None)
            thrown = next((k for k in range(i, j) if hm[k][1] == 't:thrown'), None)
            if hold is not None and thrown is not None:
                tosses.append((i, hold, thrown, j))
            i = j
        i += 1
    t = t_end1
    if tosses:
        a0, hold, thrown, j = tosses[0]
        # the first: he grabs a helper and throws it at the pilot - through the throw and the robot's flight
        t2 = q(t + (thrown + 70 - a0) / FPS)
        shot(t, t2, HAMA, src=a0, label='HAMA: grabs a robot and throws it at the pilot', c=cam(1.15, 1.25, track='target', lead=60))
        hit(t + (thrown - a0) / FPS, 'punch', 0.14, 0.04)
        t = t2
    if len(tosses) > 1:
        a0, hold, thrown, j = tosses[1]
        # the second: he picks the next one up ... and the camera pushes in as he holds it overhead
        t3 = q(t + (hold + 30 - a0) / FPS)
        shot(t, t3, HAMA, src=a0, label='HAMA: picks up the next robot', c=cam(1.2, 1.9, track='target', lead=-60, ease='in'))
        t4 = q(t3 + 0.30)
        shot(t3, t4, HAMA, src=hold + 30, hold=0.30, label='HAMA: ... and holds it overhead (hold)', c=cam(1.9, 2.0, track='target', lead=-60))
        t = t4
    # 3. THROWN AT THE CAMERA: the robot's own eight tumble views, growing geometrically and accelerating into the lens
    t_fly0 = t
    t_imp = q(t_fly0 + 0.62)
    seq = ['brand/robot_tumble_%d.png' % k for k in (2, 3, 4, 5, 6, 7, 1, 0)]
    fly = {'kind': 'image', 'src': seq[0], 'seq': seq, 'seq_fps': 14, 'seq_hold_last': 0.12, 'x': W / 2, 'y': H / 2,
           'prescale': 1.0, 'anchor': 'c', 't_in': t_fly0, 't_out': t_imp, 'in': 'cut', 'out': 'cut', 'shadow': True,
           'resample': 'nearest', 'drift': 0.0, 'fade': 0.2, 'fade_out': 0.2,
           'fly': {'s0': 0.55, 's1': 9.0, 'pow': 2.2, 'x0': W * 0.50, 'y0': H * 0.30, 'x1': W * 0.52, 'y1': H * 0.48}}
    OVERLAYS.append(fly)
    sfx(t_fly0, SND('sounds', 'whip.mp3'), gain_db=-4.0)
    # under the flight the hold frame stays on screen, the camera all the way in
    if len(tosses) > 1:
        shot(t_fly0, t_imp, HAMA, src=tosses[1][1] + 31, hold=0.62, label='HAMA: the robot leaves his hands', c=cam(2.0, 2.0, track='target', lead=-60))
    # 4. IMPACT: the glass breaks in four quick stages and stays broken
    cracks = [image(t_imp + 0.04 * k, t_imp + (0.04 * (k + 1) if k < 3 else 3.2), 'brand/crack_%d.png' % k, kin='cut',
                    out='fade' if k == 3 else 'cut', fade_out=0.6, shadow=False, overlay=False) for k in range(4)]
    t_crack_end = q(t_imp + 1.35)
    if len(tosses) > 1:
        shot(t_imp, t_crack_end, HAMA, src=tosses[1][1] + 31, hold=1.35, label='HAMA: the screen is cracked', desat=0.35,
             tint=[0, 0, 0, 0.35], c=cam(2.0, 2.05, track='target', lead=-60), layers=cracks)
    else:
        black(t_imp, t_crack_end, layers=cracks, label='the screen is cracked')
    hit(t_imp, 'flash', 0.14, 1.0)
    hit(t_imp, 'shake', 0.7, 26)
    hit(t_imp, 'rgb', 0.3, 12)
    sfx(t_imp, SND('sounds', 'shatter.mp3'), gain_db=-1.0)
    sfx(t_imp, SND('sounds', 'nsp_comet_impact.mp3'), gain_db=-4.0)
    sfx(t_imp + 0.01, SND('sounds', 'expBig.mp3'), gain_db=-8.0)
    logo_t0 = q(t_crack_end)

# ====================================================================================================================
#  THE LOGO CARD - BULLETS OF FURY, COMING NOVEMBER 2026, the copyright, the Phoenix engine line
# ====================================================================================================================
END = q(logo_t0 + 8.2)
crack_keep = image(logo_t0, logo_t0 + 1.4, 'brand/crack_3.png', kin='cut', out='fade', fade_out=1.0, shadow=False, overlay=False)
black(logo_t0, END, label='logo card', fade_out=1.6,
      layers=[crack_keep,
              image(logo_t0, END, 'brand/bof_logo.png', y=360, prescale=0.62, kin='slam', drift=0.008, overlay=False),
              text(logo_t0 + 0.7, END, 'COMING NOVEMBER 2026', height=96, y=660, kin='rise', overlay=False),
              text(logo_t0 + 1.3, END, 'STEAM / PC / MAC / LINUX', height=50, y=760, kin='fade', face=ICE, overlay=False),
              text(logo_t0 + 1.9, END, 'COPYRIGHT COLEFORGE PRODUCTION', height=46, y=845, kin='fade', overlay=False),
              image(logo_t0 + 2.5, END, 'brand/fine_engine.png', y=935, prescale=1.0, kin='fade', shadow=False, overlay=False),
              image(logo_t0 + 2.9, END, 'brand/fine_contact.png', y=1012, prescale=1.0, kin='fade', shadow=False, overlay=False)])
hit(logo_t0, 'flash', 0.22, 1.0)
hit(logo_t0, 'shake', 0.45, 16)
sfx(logo_t0, SND('sounds', 'expBig.mp3'), gain_db=-6.0)
LENGTH = END

AUDIO = {
    'length': LENGTH,
    't0': T0,
    'takes_dir': TAKES_DIR,
    'song': SONG,
    'song_gain_db': -6.3,
    'song_fade_in': 0.01,
    'song_fade_out': [t_last, SONG_END],
    'music2': ({'file': HAMA_SONG, 't': t_cut, 'src': HAMA_SRC_T, 'fade_in': 0.02, 'fade_out': [END - 3.0, END],
                'match_song': True, 'match_offset_db': -3.0} if HAMA_SRC_T is not None else None),
    'chime': {'file': SND('sounds', 'cf_boot.mp3'), 't': 0.05, 'gain_db': -12.0},
    'sfx': SFX,
    'fade_out': 0.8,
}
