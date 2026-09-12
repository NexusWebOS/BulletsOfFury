#!/usr/bin/env python3
"""
sfx_proof.py - LOOK AT A SOUND, because nobody in this pipeline can hear one.

    python3 _BUILD_SOURCE/sfx_proof.py /tmp/sfxtest --out docs/proofs/sfx_shield.png
    python3 _BUILD_SOURCE/sfx_proof.py /tmp/sfxtest --vs assets/game/sounds --out ...

CLAUDE.md's first rule is "render the art before you trust it" and it has cost this repo real days
when it was skipped. Audio has the same failure mode and no equivalent habit: every check so far
has been a number, and a number cannot tell a punchy arcade hit from a wet cinematic one.

So this draws each cue as a WAVEFORM over a SPECTROGRAM, with the measured transient marked. What
you are looking for in a game cue:

    a vertical wall at the very left      the attack. If the loud part is in the middle, that is
                                          the "delayed" defect Mike has already complained about.
    a short decay that reaches the floor   a long smear to the right is a reverb tail, which is
                                          cinematic and wrong for an arcade cue.
    energy spread up the frequency axis    an impact needs highs to read as an impact. A band that
                                          hugs the bottom is muffled, however good the numbers are.

`--vs` puts the shipped file of the same name underneath the new one, so a replacement is judged
against what it replaces rather than against nothing.
"""
import os, sys, glob, argparse, wave
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SR = 44100


def read(path):
    w = wave.open(path, 'rb')
    n, ch, sw, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
    raw = w.readframes(n); w.close()
    if sw != 2:
        return None, sr
    a = np.frombuffer(raw, dtype='<i2').astype(np.float64) / 32768.0
    if ch > 1:
        a = a.reshape(-1, ch).mean(axis=1)
    return a, sr


def envelope(x, win=256):
    a = np.abs(x)
    if len(a) < win:
        return a
    return np.convolve(a, np.ones(win) / win, mode='same')


def panel(ax_w, ax_s, x, sr, title, colour):
    t = np.arange(len(x)) / float(sr)
    ax_w.plot(t, x, lw=0.4, color=colour)
    e = envelope(x)
    ax_w.plot(t, e, lw=1.1, color='#ffffff', alpha=0.85)
    ax_w.plot(t, -e, lw=1.1, color='#ffffff', alpha=0.85)
    pk = int(np.argmax(e)) if len(e) else 0
    frac = pk / float(len(x)) if len(x) else 0
    ax_w.axvline(pk / float(sr), color='#ff5a6e', lw=1.4, ls='--')
    ax_w.set_xlim(0, max(t[-1] if len(t) else 1, 0.05))
    ax_w.set_ylim(-1.05, 1.05)
    ax_w.set_facecolor('#0b1118')
    ax_w.set_yticks([])
    ax_w.tick_params(colors='#7c8b9a', labelsize=7)
    ax_w.set_title('%s   %.2fs   transient @ %.0f%%' % (title, t[-1] if len(t) else 0, frac * 100),
                   color=('#ff5a6e' if frac > 0.35 and len(x) > 0.30 * sr else '#7cf5ff'),
                   fontsize=9, loc='left')
    for s in ax_w.spines.values():
        s.set_color('#22303d')

    nfft = 512
    hop = 128
    if len(x) > nfft:
        frames = 1 + (len(x) - nfft) // hop
        S = np.empty((nfft // 2 + 1, frames))
        win = np.hanning(nfft)
        for i in range(frames):
            seg = x[i * hop:i * hop + nfft] * win
            S[:, i] = np.abs(np.fft.rfft(seg))
        S = 20 * np.log10(S + 1e-8)
        ax_s.imshow(S, origin='lower', aspect='auto', cmap='magma',
                    extent=[0, len(x) / float(sr), 0, sr / 2.0], vmin=S.max() - 70, vmax=S.max())
    ax_s.set_ylim(0, 12000)
    ax_s.set_facecolor('#0b1118')
    ax_s.tick_params(colors='#7c8b9a', labelsize=7)
    ax_s.set_ylabel('Hz', color='#7c8b9a', fontsize=7)
    for s in ax_s.spines.values():
        s.set_color('#22303d')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('--vs', help='directory holding the files these replace')
    ap.add_argument('--out', default='sfx_proof.png')
    ap.add_argument('--title', default='')
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.dir, '*.wav')))
    if not files:
        sys.exit('no wav files in ' + a.dir)

    rows = []
    for f in files:
        x, sr = read(f)
        if x is None:
            continue
        name = os.path.basename(f)
        rows.append((name + '   NEW', x, sr, '#7cf5ff'))
        if a.vs:
            old = os.path.join(a.vs, name)
            if os.path.exists(old):
                y, sr2 = read(old)
                if y is not None:
                    rows.append((name + '   shipped', y, sr2, '#ffc21a'))

    fig = plt.figure(figsize=(13, 2.5 * len(rows)), facecolor='#070c12')
    gs = fig.add_gridspec(len(rows) * 2, 1, hspace=0.95, top=0.965, bottom=0.02)
    for i, (name, x, sr, col) in enumerate(rows):
        panel(fig.add_subplot(gs[i * 2]), fig.add_subplot(gs[i * 2 + 1]), x, sr, name, col)
    if a.title:
        fig.suptitle(a.title, color='#7cf5ff', fontsize=12, y=0.997)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    fig.savefig(a.out, dpi=110, facecolor='#070c12', bbox_inches='tight')
    print('wrote %s  (%d panels)' % (a.out, len(rows)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
