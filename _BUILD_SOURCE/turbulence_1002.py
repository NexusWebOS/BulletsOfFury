"""turbulence_1002 - Stage 6 turbulence cues (Mike, 1002: "we also need turbulance noises generated for the
harrier and them going over us and stuff").

    python3 _BUILD_SOURCE/turbulence_1002.py

Sources (ElevenLabs text-to-sound v2, generated through the ElevenLabs connector, kept verbatim):
  _BUILD_SOURCE/sfx_src_1002/turbulence_carrier_eleven.mp3  heavy buffeting under a passing carrier (2.0 s)
  _BUILD_SOURCE/sfx_src_1002/jetwash_eleven.mp3             a fighter's wake slamming the cockpit (0.48 s)
Outputs assets/game/shared/audio/sounds/turbulence_carrier_1002.mp3 (seamless loop) and jetwash_1002.mp3 (one-shot).

Mastering, measured against the cues they sit beside (volumedetect): the carrier loop is matched to
arc_carrier_turbine_0923 (mean -16.8 dB), the jet wash to arc_jet_dash_0923 (mean -18.3 dB), peaks held under
-1.5 dB. Leading silence is trimmed (the "delayed" defect, sfx_gen.py), the loop is CROSSFADED end-into-start
so the HTML loop has no seam, and both are mono 44.1 kHz 128k like the library. Never reads its own output.
"""
import os, subprocess, tempfile, wave
import numpy as np
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, '_BUILD_SOURCE/sfx_src_1002'); OUT = os.path.join(ROOT, 'assets/game/sounds')
SR = 44100


def load(p):
    t = tempfile.mktemp(suffix='.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-ac', '1', '-ar', str(SR), '-af', 'lowpass=f=11000', t], check=True)
    w = wave.open(t); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768; w.close(); os.remove(t)
    return a


def trim_lead(a, db=-42):
    thr = 10 ** (db / 20); i = int(np.argmax(np.abs(a) > thr)); return a[max(0, i - 40):]


def match(a, mean_db, peak_db=-1.5):
    # gain to the target mean, soft-limit the peaks, and repeat: the limiter takes energy back each pass
    lim = 10 ** (peak_db / 20)
    for _ in range(6):
        rms = np.sqrt(np.mean(a ** 2)); a = a * (10 ** (mean_db / 20) / max(rms, 1e-9))
        if np.max(np.abs(a)) > lim: a = np.tanh(a / lim) * lim   # soft limit, never a hard clip
    return a


def save(a, name):
    t = tempfile.mktemp(suffix='.wav'); w = wave.open(t, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    out = os.path.join(OUT, name)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', t, '-codec:a', 'libmp3lame', '-b:a', '128k', '-ar', str(SR), '-ac', '1', out], check=True)
    os.remove(t); return out


def loop_xfade(a, xf=0.20):
    n = int(SR * xf); body, tail = a[:-n], a[-n:]
    ramp = np.linspace(0, 1, n); body = body.copy(); body[:n] = body[:n] * ramp + tail * (1 - ramp)
    return body


def main():
    c = trim_lead(load(os.path.join(SRC, 'turbulence_carrier_eleven.mp3')))
    c = loop_xfade(match(c, -16.8))
    j = trim_lead(load(os.path.join(SRC, 'jetwash_eleven.mp3')))
    j = match(j, -18.3); n = int(SR * .06); j[-n:] *= np.linspace(1, 0, n)
    for a, nm in [(c, 'turbulence_carrier_1002.mp3'), (j, 'jetwash_1002.mp3')]:
        p = save(a, nm); print(nm, '%.2fs' % (len(a) / SR), 'peak %.1f dB' % (20 * np.log10(np.max(np.abs(a)))), 'mean %.1f dB' % (20 * np.log10(np.sqrt(np.mean(a ** 2)))))


if __name__ == '__main__':
    main()
