#!/usr/bin/env python3
"""
sfx_gen.py - ElevenLabs text-to-sound-effects, shaped for a 16-bit shmup.

    python3 _BUILD_SOURCE/sfx_gen.py sheet _BUILD_SOURCE/sfx/shield.json --dry
    python3 _BUILD_SOURCE/sfx_gen.py sheet _BUILD_SOURCE/sfx/shield.json
    python3 _BUILD_SOURCE/sfx_gen.py audit assets/game/sounds          # gate the EXISTING library

⚠ THE KEY IS NEVER IN THIS FILE. Read from _BUILD_SOURCE/.secrets.json, which .gitignore covers
by name. Generated audio is ordinary committed art; the key is not.

============================================================
WHY THERE ARE QUALITY GATES AND NOT JUST A DOWNLOAD

ElevenLabs returns CINEMATIC sound design: a slow swell, a long reverb tail, and often a beat of
silence before anything happens. That is the opposite of an arcade cue, and this repo has already
paid for the difference. From CLAUDE.md:

    test_fl's `_approved259` sound ledger pinned `reviewed_shadow_orb_launch.wav` - the sample
    whose peak lands at 1.805 s of a 2.250 s file, which is Mike's "delayed" complaint.

So a cue whose transient arrives 80% of the way through IS the defect, and it is measurable. Every
generated file is gated on that before it is allowed near assets/:

    PEAK POSITION   the loudest moment must land early (default <= 35% of the file)
    LEAD SILENCE    trimmed, because a leading gap is what "delayed" actually feels like
    DURATION        an impact that runs 3 s is not an impact
    LEVEL           normalised, so one cue is not four times another

⚠ AND THE 16-BIT CHARACTER IS A PROCESS, NOT A PROMPT. Asking for "16-bit" in words gets you a
realistic sound with the words ignored. The era's signature is band-limited and dry: highs rolled
off where the hardware rolled off, the reverb tail cut rather than faded, and a shallow quantise.
That chain is applied here and MEASURED (spectral centroid before/after), because an unmeasured
"make it retro" step is how you turn a good sound into mush.

⚠ THE OUTPUT FORMAT MATCHES THE LIBRARY EXACTLY - mono, 44100, 16-bit PCM WAV - so a generated cue
drops onto an existing key with nothing else to change. Measured off the shipped library.
============================================================
"""
import os, re, sys, json, io, argparse, subprocess, tempfile, urllib.request, urllib.error

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SECRETS = os.path.join(ROOT, '_BUILD_SOURCE', '.secrets.json')
SOUNDS = os.path.join(ROOT, 'assets', 'game', 'sounds')
API = 'https://api.elevenlabs.io/v1'

SR = 44100          # the library's rate, measured
RETRO_SR = 22050    # the band a 16-bit console actually delivered
PEAK_MAX = 0.35     # the transient must land in the first 35% ...
PEAK_FLOOR_S = 0.090  # ... AND later than this in absolute time, or a short tick fails unfairly
LEAD_MAX = 0.040    # seconds of silence tolerated before the attack


def key():
    if not os.path.exists(SECRETS):
        sys.exit('no %s - create it with {"elevenlabs_api_key": "..."} (it is gitignored)' % SECRETS)
    k = json.load(io.open(SECRETS, encoding='utf-8')).get('elevenlabs_api_key')
    if not k:
        sys.exit('elevenlabs_api_key missing from %s' % SECRETS)
    return k


def generate(text, seconds, influence):
    """POST /v1/sound-generation. Returns mp3 bytes."""
    body = {'text': text, 'prompt_influence': influence}
    if seconds:
        body['duration_seconds'] = float(seconds)
    req = urllib.request.Request(API + '/sound-generation', data=json.dumps(body).encode('utf-8'),
                                 headers={'xi-api-key': key(), 'Content-Type': 'application/json'})
    try:
        return urllib.request.urlopen(req, timeout=180).read()
    except urllib.error.HTTPError as e:
        raise SystemExit('ElevenLabs %s: %s' % (e.code, e.read()[:300]))


def mp3_to_mono(blob):
    """Decode to float32 mono at SR via ffmpeg. Returns numpy array in [-1,1]."""
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, 'in.mp3')
        io.open(src, 'wb').write(blob)
        out = subprocess.run(
            ['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
            capture_output=True)
        if out.returncode != 0:
            raise SystemExit('ffmpeg decode failed: ' + out.stderr.decode()[:300])
        return np.frombuffer(out.stdout, dtype='<f4').astype(np.float64)


def env(x, win=256):
    """Smoothed amplitude envelope - the transient is found on this, not on raw samples,
       because a single stray sample is not an attack."""
    a = np.abs(x)
    if len(a) < win:
        return a
    k = np.ones(win) / win
    return np.convolve(a, k, mode='same')


def trim_lead(x, floor_db=-46.0):
    """⚠ A LEADING GAP IS WHAT 'DELAYED' FEELS LIKE. Cut everything before the sound starts."""
    e = env(x, 128)
    if not len(e) or e.max() <= 0:
        return x, 0.0
    thr = e.max() * (10 ** (floor_db / 20.0))
    idx = np.argmax(e > thr)
    return x[idx:], idx / float(SR)


def trim_tail(x, keep_db=-38.0, max_s=None):
    """Cut the cinematic reverb tail rather than fading it - the era had no tail to speak of."""
    e = env(x, 256)
    if not len(e) or e.max() <= 0:
        return x
    thr = e.max() * (10 ** (keep_db / 20.0))
    above = np.where(e > thr)[0]
    end = int(above[-1]) + int(0.030 * SR) if len(above) else len(x)
    if max_s:
        end = min(end, int(max_s * SR))
    end = min(max(end, int(0.05 * SR)), len(x))
    x = x[:end]
    # a short cosine fade so the cut does not click
    f = int(min(0.012 * SR, len(x) // 4))
    if f > 1:
        x[-f:] *= np.cos(np.linspace(0, np.pi / 2, f)) ** 2
    return x


def retro(x, sr_target=RETRO_SR, bits=0):
    """⚠ BAND-LIMIT FIRST, THEN QUANTISE. Downsampling without the low-pass aliases the highs back
       down as grit that sounds like a broken file rather than an old one."""
    from scipy.signal import resample_poly
    g = np.gcd(int(sr_target), int(SR))
    y = resample_poly(x, int(sr_target) // g, int(SR) // g)     # LPF + decimate
    if bits and bits > 0:
        q = float(2 ** (bits - 1))
        y = np.round(y * q) / q                                  # shallow quantise
    g2 = np.gcd(int(SR), int(sr_target))
    return resample_poly(y, int(SR) // g2, int(sr_target) // g2)  # back to the library rate


def normalize(x, peak=0.89):
    m = np.max(np.abs(x)) if len(x) else 0.0
    return x * (peak / m) if m > 0 else x


def brightness(x, cut=2000.0):
    """Share of energy above `cut` Hz. This is the measurable form of "it sounds muffled".

    ⚠ IT EXISTS BECAUSE THE NUMERIC GATES PASSED TWO DEAD CUES. shield_hit_heavy and shield_low
    came back with a perfect transient, a legal duration and a correct level - and a spectrogram
    that was EMPTY above 1 kHz. A thud with no crack does not read as an impact at any volume, and
    only the rendered picture showed it (CLAUDE.md rule 1, in a medium with no habit of it).

    ⚠ THE THRESHOLD REPRODUCES THE KNOWN-GOOD CASES FIRST, which is the only kind worth trusting:
    the shipped shield_hit_light measures 0.176 and shield_hit_heavy 0.156, while the two dead
    generations measured 0.000 exactly. 0.08 separates them with room on both sides.
    """
    if len(x) < 512:
        return 0.0
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1.0 / SR)
    t = X.sum()
    return float(X[f >= cut].sum() / t) if t > 0 else 0.0


BRIGHT_MIN = 0.08


def centroid(x):
    """Spectral centroid in Hz - the one number that says 'this got darker' without ears."""
    if len(x) < 512:
        return 0.0
    X = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1.0 / SR)
    s = X.sum()
    return float((f * X).sum() / s) if s > 0 else 0.0


def measure(x):
    e = env(x, 256)
    n = len(x)
    pk = int(np.argmax(e)) if n else 0
    rms = float(np.sqrt(np.mean(x ** 2))) if n else 0.0
    return {'secs': round(n / float(SR), 3),
            'peak_at': round(pk / float(SR), 3),
            'peak_frac': round(pk / float(n), 3) if n else 0.0,
            'peak': round(float(np.max(np.abs(x))) if n else 0.0, 3),
            'rms': round(rms, 4),
            'bright': round(brightness(x), 3),
            'centroid': round(centroid(x))}


def write_wav(path, x):
    import wave
    y = np.clip(x, -1.0, 1.0)
    pcm = (y * 32767.0).astype('<i2')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    w = wave.open(path, 'wb')
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes()); w.close()


def read_wav(path):
    import wave
    w = wave.open(path, 'rb')
    n, ch, sw, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
    raw = w.readframes(n); w.close()
    if sw != 2:
        return None, sr
    a = np.frombuffer(raw, dtype='<i2').astype(np.float64) / 32768.0
    if ch > 1:
        a = a.reshape(-1, ch).mean(axis=1)
    return a, sr


# ---------------------------------------------------------------- commands

def cmd_sheet(a):
    sheet = json.load(io.open(a.sheet, encoding='utf-8'))
    items = sheet['sounds'] if isinstance(sheet, dict) else sheet
    outdir = a.out or SOUNDS
    print('%d cues -> %s' % (len(items), outdir))
    if a.dry:
        for it in items:
            print('  %-26s %4.1fs  infl %.2f  %s'
                  % (it['key'], it.get('seconds') or 0, it.get('influence', 0.6), it['prompt'][:76]))
        print('\nDRY - nothing generated, nothing billed.')
        return 0

    rows, bad = [], []
    for it in items:
        k = it['key']
        dst = os.path.join(outdir, k + '.wav')
        if os.path.exists(dst) and not a.force:
            print('  skip %-24s (exists; --force to replace)' % k); continue
        blob = generate(it['prompt'], it.get('seconds'), it.get('influence', 0.6))
        x = mp3_to_mono(blob)
        raw_m = measure(x)

        x, lead = trim_lead(x)
        x = trim_tail(x, max_s=it.get('max_seconds'))
        c_before = centroid(x)
        if not it.get('no_retro'):
            x = retro(x, it.get('retro_sr', RETRO_SR), it.get('bits', 0))
        x = normalize(x, it.get('peak', 0.89))
        m = measure(x)
        m['lead_trimmed'] = round(lead, 3)
        m['centroid_before'] = round(c_before)

        # ============================================================
        # ⚠ A CUE'S CLASS DECIDES WHICH RULES APPLY, AND FORGETTING THAT REFUSED SIX GOOD SOUNDS.
        #
        # The first cut ran the impact gates over everything, and a klaxon came back "muffled" at
        # 0.009 above 2kHz - which is what a deep warning horn IS - while a rising lock-on tone was
        # called "delayed" for peaking at 86%, which is what a RISE does. That is precisely the
        # mistake this tool's own audit had already caught in the shipped library and separated
        # there (swells and spoken lines are late BY DESIGN); the lesson had not been carried into
        # the generator.
        #
        #   impact  a hit, a shot, a snap  -> transient must be early, must have top end
        #   swell   a charge, a klaxon, a rise -> may peak late; brightness floor relaxed
        #   tone    a clean electronic blip  -> early, and bright, but no body expected
        #
        # Declared per cue, defaulted to impact, and STATED - a gate nobody can see the reason for
        # is a gate someone quietly disables.
        # ============================================================
        cls = it.get('class', 'impact')
        gate_time = cls in ('impact', 'tone')
        bright_floor = it.get('min_bright',
                              {'impact': BRIGHT_MIN, 'tone': 0.15, 'swell': 0.015}.get(cls, BRIGHT_MIN))

        why = []
        # ⚠ A FRACTION ALONE PUNISHES SHORT CUES AND THAT IS THE RULE BEING WRONG, NOT THE SOUND.
        # A 0.18s tick peaking at 40% peaks 72ms in, which nobody can perceive as a delay; the
        # complaint this gate encodes was a peak at 1.805s. So lateness must be late in BOTH senses.
        # ⚠ Verified against the ten shipped one-shots the audit flags: every one peaks at 0.21s or
        # later, so the floor rescues NONE of them - the gate still reproduces every known-bad case.
        if gate_time and m['peak_frac'] > PEAK_MAX and m['peak_at'] > PEAK_FLOOR_S:
            why.append('transient lands at %.0f%% of the file AND %.0fms in (max %.0f%% / %.0fms) - '
                       'that is the "delayed" defect'
                       % (m['peak_frac'] * 100, m['peak_at'] * 1000, PEAK_MAX * 100, PEAK_FLOOR_S * 1000))
        if it.get('max_seconds') and m['secs'] > it['max_seconds'] + 0.05:
            why.append('%.2fs exceeds the %.2fs this cue is allowed' % (m['secs'], it['max_seconds']))
        if m['peak'] < 0.2:
            why.append('almost silent (peak %.2f)' % m['peak'])
        mb = bright_floor
        if mb and m['bright'] < mb:
            why.append('muffled - only %.3f of its energy is above 2kHz (need %.2f); a thud with no '
                       'crack does not read as an impact' % (m['bright'], mb))

        if why and not a.keep_bad:
            bad.append((k, why, m))
            print('  FAIL %-24s %s' % (k, '; '.join(why)))
            continue
        write_wav(dst, x)
        rows.append((k, m))
        print('  ok   %-24s %-6s %.2fs  peak@%.0f%%  >2kHz %.2f  centroid %d->%d Hz'
              % (k, cls, m['secs'], m['peak_frac'] * 100, m['bright'],
                 m['centroid_before'], m['centroid']))

    print('\n%d written, %d refused' % (len(rows), len(bad)))
    for k, why, m in bad:
        print('  REFUSED %s: %s' % (k, '; '.join(why)))
    return 1 if bad else 0


def cmd_audit(a):
    """Gate the EXISTING library by the same rule, so 'which of our sounds are the annoying ones'
       is a measurement rather than a memory."""
    import glob
    files = sorted(glob.glob(os.path.join(a.dir, '*.wav')))
    print('auditing %d wav files in %s\n' % (len(files), a.dir))
    late, dup = [], {}
    for f in files:
        x, sr = read_wav(f)
        if x is None or not len(x):
            continue
        m = measure(x)
        h = (os.path.getsize(f), round(m['rms'], 5))
        dup.setdefault(h, []).append(os.path.basename(f))
        if m['peak_frac'] > PEAK_MAX and m['secs'] > 0.30:
            late.append((os.path.basename(f), m))
    late.sort(key=lambda r: -r[1]['peak_frac'])
    """⚠ A SWELL IS NOT A DEFECT. A charge loop, a beam loop and a spoken line are SUPPOSED to peak
       late - gating them would be the 0906 trap in reverse, calling correct art broken. Only
       one-shot IMPACTS and FIRES are judged by the transient rule, so the classification is by
       name and is stated rather than hidden."""
    SWELL = re.compile(r'(_loop|charge|raceStart|sequence|amb_|_start$)', re.I)
    VOICE = set(['enemyunit', 'enemyunits', 'restrictedarea', 'goodluck', 'over', 'announce',
                 'countdown', 'continueVO', 'selectpilot', 'allyArrive', 'allyLeave',
                 'impactImminent'])
    real, byd = [], []
    for n, m in late:
        stem = os.path.splitext(n)[0]
        if stem in VOICE or SWELL.search(stem):
            byd.append((n, m))
        else:
            real.append((n, m))
    print('=== ONE-SHOTS whose transient lands LATE - these are the "delayed" defect ===')
    for n, m in real:
        print('  %-34s peak at %.2fs of %.2fs (%.0f%%)' % (n, m['peak_at'], m['secs'], m['peak_frac'] * 100))
    print('  (%d of %d files)' % (len(real), len(files)))
    print('\n=== late BY DESIGN - swells, loops and spoken lines, left alone ===')
    for n, m in byd:
        print('  %-34s %.0f%%' % (n, m['peak_frac'] * 100))
    print('\n=== files that look IDENTICAL (same size and RMS) ===')
    n = 0
    for h, names in dup.items():
        if len(names) > 1:
            print('  ' + ' == '.join(names)); n += 1
    if not n:
        print('  none')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('sheet'); s.add_argument('sheet'); s.add_argument('--out')
    s.add_argument('--dry', action='store_true'); s.add_argument('--force', action='store_true')
    s.add_argument('--keep-bad', action='store_true',
                   help='write files that fail the gates anyway (records why)')
    s.set_defaults(fn=cmd_sheet)
    d = sub.add_parser('audit'); d.add_argument('dir', nargs='?', default=SOUNDS); d.set_defaults(fn=cmd_audit)
    a = ap.parse_args()
    if not getattr(a, 'fn', None):
        ap.print_help(); return 2
    return a.fn(a)


if __name__ == '__main__':
    sys.exit(main())
