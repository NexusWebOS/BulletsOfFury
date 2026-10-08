"""beatmap9.py - measure a song's tempo, beat grid, bars and section energy. Writes beatmap9.json.

    python beatmap9.py assets/game/levels/stage_06/audio/music/Level6.mp3 [--out beatmap9.json] [--bpm-lo 70 --bpm-hi 190]

Spectral-flux onset envelope -> autocorrelation for the period -> a phase fit of the beat grid to the onsets.
Bars are four beats from the downbeat whose phase carries the most low-band energy. Every bar gets its RMS,
its share of energy above 2 kHz and its onset density, so the edit can find the drop, the breaks and the end
from the file rather than by ear.
"""
import os, sys, json, argparse, subprocess
import numpy as np

SR = 22050
HOP = 256


def decode(path):
    import imageio_ffmpeg
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def stft_mag(x, n=1024, hop=HOP):
    w = np.hanning(n).astype(np.float32)
    frames = 1 + (len(x) - n) // hop
    idx = np.arange(n)[None, :] + hop * np.arange(frames)[:, None]
    return np.abs(np.fft.rfft(x[idx] * w, axis=1)).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('song')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beatmap9.json'))
    ap.add_argument('--bpm-lo', type=float, default=70)
    ap.add_argument('--bpm-hi', type=float, default=190)
    a = ap.parse_args()
    x = decode(a.song)
    dur = len(x) / SR
    M = stft_mag(x)
    fps = SR / HOP
    logm = np.log1p(M * 10)
    flux = np.maximum(0, np.diff(logm, axis=0)).sum(axis=1)
    flux = np.concatenate([[0], flux])
    # local mean removal
    k = int(fps * 0.5)
    ker = np.ones(k) / k
    env = flux - np.convolve(flux, ker, mode='same')
    env = np.maximum(env, 0)
    env /= (env.max() + 1e-9)
    # autocorrelation over the tempo range
    ac = np.correlate(env, env, mode='full')[len(env) - 1:]
    lo = int(round(fps * 60 / a.bpm_hi))
    hi = int(round(fps * 60 / a.bpm_lo))
    lags = np.arange(lo, hi + 1)
    # weight by a mild log-normal prior around 120 bpm so octave errors prefer the danceable one
    bpms = 60 * fps / lags
    prior = np.exp(-0.5 * (np.log2(bpms / 120.0) / 0.9) ** 2)
    score = ac[lags] * prior
    best = lags[np.argmax(score)]
    # refine with parabolic interpolation on the raw ac
    i = best
    y0, y1, y2 = ac[i - 1], ac[i], ac[i + 1]
    d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
    period_frames = i + d
    period = period_frames / fps
    bpm = 60 / period
    # phase fit: the offset (0..period) maximising summed onset env on the grid
    t_env = np.arange(len(env)) / fps
    best_phase, best_val = 0.0, -1
    for ph in np.linspace(0, period, 200, endpoint=False):
        ts = np.arange(ph, dur, period)
        fi = np.clip(np.round(ts * fps).astype(int), 0, len(env) - 1)
        v = env[fi].sum()
        if v > best_val:
            best_val, best_phase = v, ph
    beats = np.arange(best_phase, dur, period)
    # downbeat: which of 4 phases has the most low-band (<150 Hz) onset energy
    freqs = np.fft.rfftfreq(1024, 1 / SR)
    low = logm[:, freqs < 150].sum(axis=1)
    lowflux = np.maximum(0, np.diff(low, prepend=low[0]))
    best_db, best_dv = 0, -1
    for j in range(4):
        fi = np.clip(np.round(beats[j::4] * fps).astype(int), 0, len(env) - 1)
        v = lowflux[fi].sum()
        if v > best_dv:
            best_dv, best_db = v, j
    bar_starts = beats[best_db::4]
    # per-bar stats
    hi_band = (M[:, freqs > 2000] ** 2).sum(axis=1)
    all_band = (M ** 2).sum(axis=1) + 1e-9
    bars = []
    for bi, t0 in enumerate(bar_starts):
        t1 = bar_starts[bi + 1] if bi + 1 < len(bar_starts) else min(dur, t0 + 4 * period)
        f0, f1 = int(t0 * fps), max(int(t0 * fps) + 1, int(t1 * fps))
        s0, s1 = int(t0 * SR), int(t1 * SR)
        seg = x[s0:s1]
        rms = float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0
        hs = float(hi_band[f0:f1].sum() / all_band[f0:f1].sum()) if f1 > f0 else 0.0
        on = float(env[f0:f1].mean()) if f1 > f0 else 0.0
        bars.append({'i': bi + 1, 't': round(float(t0), 4), 'rms': round(rms, 4), 'hi': round(hs, 4), 'onset': round(on, 4)})
    rmsmax = max(b['rms'] for b in bars) or 1
    for b in bars:
        b['lvl'] = round(b['rms'] / rmsmax, 3)
    # 250 ms RMS curve for the end fade and drops
    win = int(SR * 0.25)
    curve = [round(float(np.sqrt(np.mean(x[j:j + win] ** 2))), 4) for j in range(0, len(x) - win, win)]
    out = {'song': os.path.abspath(a.song), 'duration': round(dur, 4), 'bpm': round(float(bpm), 3),
           'beat_period': round(float(period), 5), 'phase': round(float(best_phase), 4), 'downbeat_beat': int(best_db),
           'beats': [round(float(b), 4) for b in beats], 'bars': bars, 'rms_250ms': curve}
    json.dump(out, open(a.out, 'w'), indent=1)
    print('duration %.2fs  bpm %.2f  period %.4fs  phase %.3fs  downbeat beat %d  bars %d' % (dur, bpm, period, best_phase, best_db, len(bars)))
    for b in bars:
        bar_vis = '#' * int(b['lvl'] * 40)
        print('bar %3d  t %7.2f  lvl %.2f  hi %.3f  on %.3f  %s' % (b['i'], b['t'], b['lvl'], b['hi'], b['onset'], bar_vis))


if __name__ == '__main__':
    main()
