#!/usr/bin/env python3
"""build_hama_0928.py - the HAMA password encounter's audio and cue sheet (Mike 0928).

Mike supplied the MC Hammer "U Can't Touch This" instrumental and asked for a second Hammer Time
password on Stage 5 where the boss and his robots dance and sing to it in sequence: a double
ground slam on every "Hammer ... time!", the breakdown with the lasso and the 360 jump turn, a
moonwalk while the shield rises.

Everything the runtime syncs to is MEASURED off the file here, never typed in by ear:
  * tempo by autocorrelating spectral flux (60-200 BPM sweep, the beat and double-beat lags);
  * the beat phase by fitting that grid to the flux peaks;
  * the song's 8-bar sections by per-bar RMS and the energy above 2 kHz (the chorus bars are darker
    and steadier, the verse bars alternate loud/quiet and brighter, the two breakdowns are the
    loudest and darkest stretches in the track);
  * the "STOP!" cues as the longest dropouts - windows where the 25 fps RMS envelope falls below
    3% of the track peak for at least 0.28 s. The instrumental drops out exactly where the vocal
    shouts "Stop!", so the silence IS the cue.

It also measures the Archmage hammer_throw_0926 plate (the only authored poses of this Hammer with
EMPTY hands, which the robot toss needs) so the runtime can seat each cell by its chest core and its
feet, the same way the Hammer Time troupe sheet is seated.

Writes:
  assets/game/music/hama_instrumental_0928.mp3   (112k CBR / 44.1 kHz stereo, the house boss format)
  assets/hama_art_0928.js                          (HAMA_ART: audio meta, envelope, cues, poses)
The source upload is not modified. Idempotent: reads only the upload and authored PNGs.
"""
import os, sys, json, hashlib, subprocess, argparse
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_MP3 = os.path.join(ROOT, 'assets', 'game', 'music', 'hama_instrumental_0928.mp3')
OUT_JS = os.path.join(ROOT, 'assets', 'hama_art_0928.js')
THROW = os.path.join(ROOT, 'assets', 'game', 'stage5_archmage_0916', 'combat_0926', 'hammer_throw.png')
SR = 11025
ENV_FPS = 25


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return 'ffmpeg'


def decode(path):
    raw = subprocess.run([ffmpeg(), '-hide_banner', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def envelope(x):
    hop = SR // ENV_FPS
    n = len(x) // hop
    rms = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1))
    return rms / rms.max()


def flux(x, h=256, frame=1024):
    nf = (len(x) - frame) // h
    win = np.hanning(frame)
    S = np.abs(np.fft.rfft(np.stack([x[i * h:i * h + frame] * win for i in range(nf)]), axis=1))
    S = np.log1p(S * 10)
    f = np.maximum(0, np.diff(S, axis=0)).sum(1)
    return (f - f.mean()) / f.std(), SR / h


def tempo(fl, fps):
    seg = fl[:int(60 * fps)]
    ac = np.correlate(seg, seg, 'full')[len(seg) - 1:]
    lags = np.arange(len(ac))
    best = max(((np.interp(60 / b * fps, lags, ac) + .5 * np.interp(120 / b * fps, lags, ac)), b) for b in np.arange(80, 180, .05))
    bpm = float(best[1])
    P = 60 / bpm
    ph = max(((fl[(np.arange(p, len(fl) / fps - 1, P) * fps).astype(int)].mean()), p) for p in np.arange(0, P, .005))[1]
    return bpm, float(ph)


def dropouts(env, seconds):
    low = env < .03
    out, i = [], 0
    while i < len(env):
        if low[i]:
            j = i
            while j < len(env) and low[j]:
                j += 1
            out.append((i / ENV_FPS, (j - i) / ENV_FPS))
            i = j
        else:
            i += 1
    return [(round(t, 2), round(l, 2)) for t, l in out if l >= .28 and 2 < t < seconds - 2]


def bars(x, bpm, ph, seconds):
    bar = 240 / bpm
    rows = []
    k = 0
    while ph + (k + 1) * bar <= seconds:
        t0 = ph + k * bar
        seg = x[int(t0 * SR):int((t0 + bar) * SR)]
        S = np.abs(np.fft.rfft(seg)); f = np.fft.rfftfreq(len(seg), 1 / SR)
        rows.append({'t': round(t0, 3), 'rms': float(np.sqrt((seg ** 2).mean())), 'hi': float(S[f > 2000].sum() / S.sum())})
        k += 1
    return rows


def sections(rows, bpm):
    """Label every bar from its own measurements, smoothed over its neighbours, then cut runs.
    loud (top 15% RMS) + dark (<.31 of energy above 2 kHz) -> breakdown; dark -> chorus; bright ->
    verse (the verse bars also alternate loud/quiet, the chorus bars do not). A run shorter than 3
    bars joins the run before it. Everything before the first 6-bar verse run is the intro."""
    rms = np.array([r['rms'] for r in rows]); hi = np.array([r['hi'] for r in rows])
    thr = np.percentile(rms, 85)
    lab = []
    for k in range(len(rows)):
        lo, hh = max(0, k - 1), min(len(rows), k + 2)
        h = np.median(hi[lo:hh]); r = np.median(rms[lo:hh])
        lab.append('breakdown' if r >= thr and h < .31 else 'chorus' if h < .338 else 'verse')
    runs = []
    for k, l in enumerate(lab):
        if runs and runs[-1][0] == l:
            runs[-1][2] = k + 1
        else:
            runs.append([l, k, k + 1])
    merged = []
    for l, a0, b0 in runs:
        if merged and (b0 - a0 < 3 or merged[-1][0] == l):
            merged[-1][2] = b0
        else:
            merged.append([l, a0, b0])
    first = next(i for i, (l, a0, b0) in enumerate(merged) if l == 'verse' and b0 - a0 >= 6)
    merged = [['intro', 0, merged[first][1]]] + merged[first:]
    bar = 240 / bpm
    return [{'kind': l, 't0': rows[a0]['t'], 't1': round(rows[b0 - 1]['t'] + bar, 3), 'bar0': a0, 'bar1': b0} for l, a0, b0 in merged]


def throw_poses():
    im = np.array(Image.open(THROW))
    H, W = im.shape[:2]
    cw, ch = W // 4, H // 2
    frames = []
    for k in range(8):
        cx, cy = (k % 4) * cw, (k // 4) * ch
        c = im[cy:cy + ch, cx:cx + cw]
        a = c[..., 3] > 40
        ys = np.where(a.any(1))[0]
        r, g, b = c[..., 0].astype(int), c[..., 1].astype(int), c[..., 2].astype(int)
        core = (c[..., 3] > 200) & (b > 230) & (g > 200) & (r > 150)
        yy, xx = np.where(core)
        frames.append([cx, cy, cw, ch, round(float(xx.mean()), 1), int(ys[-1])])
    # body height of the upright empty-handed frame (7) against the troupe sheet's upright frame
    return {'key': 'arch_hammer_throw_0926', 'frames': frames, 'cellHeight': ch,
            'bodyInk': int(np.where((im[ch:, 3 * cw:, 3] > 40).any(1))[0][-1] - np.where((im[ch:, 3 * cw:, 3] > 40).any(1))[0][0])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', help='the supplied instrumental MP3')
    a = ap.parse_args()
    src = a.source
    sha = hashlib.sha256(open(src, 'rb').read()).hexdigest()
    os.makedirs(os.path.dirname(OUT_MP3), exist_ok=True)
    # the source peaks at 0.0 dBFS with a -18.5 dB mean - quieter than the boss tracks and with no
    # headroom to raise; -0.5 dB keeps the MP3 re-encode from clipping. Volume only, no compression.
    subprocess.run([ffmpeg(), '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-ac', '2', '-ar', '44100',
                    '-af', 'volume=-0.5dB', '-codec:a', 'libmp3lame', '-b:a', '112k', OUT_MP3], check=True)
    x = decode(OUT_MP3)
    seconds = round(len(x) / SR, 3)
    env = envelope(x)
    fl, ffps = flux(x)
    bpm, ph = tempo(fl, ffps)
    rows = bars(x, bpm, ph, seconds)
    secs = sections(rows, bpm)
    stops = dropouts(env, seconds)
    art = {
        'audio': {'path': 'assets/game/music/hama_instrumental_0928.mp3', 'seconds': seconds, 'sourceSHA256': sha,
                  'bpm': round(bpm, 3), 'phase': round(ph, 3), 'envelopeFPS': ENV_FPS,
                  'envelope': [round(float(v), 3) for v in env],
                  'stops': stops, 'sections': secs},
        'poses': {'throw': throw_poses()},
    }
    with open(OUT_JS, 'w', newline='\n') as f:
        f.write('/* generated by _BUILD_SOURCE/build_hama_0928.py - do not hand-edit */\n')
        f.write('const HAMA_ART=' + json.dumps(art, separators=(',', ':')) + ';\n')
    print('bpm %.3f phase %.3f seconds %.2f' % (bpm, ph, seconds))
    print('stops', stops)
    for s in secs:
        print('  %-9s %7.2f - %7s  bars %d-%d' % (s['kind'], s['t0'], s['t1'], s['bar0'], s['bar1']))


if __name__ == '__main__':
    main()
