"""mix3.py - the v3 soundtrack: the song, the chime, and every shot's OWN game audio underneath it.

    python mix3.py edl3.json mix3.wav                 # -> 48 kHz 24-bit WAV (+ mix3_sfx.wav, the game bus alone)
    python mix3.py mux video.mp4 mix3.wav out.mp4     # H.264 copied, AAC 320k, faststart

Mike, on v2: "...and have the sounds in there." v2's mix was the song, the chime and forty generic explosion
accents; nothing the game itself made. Here every pane of every clip plays its take's sfx.wav (render_audio.py)
from the pane's own source frame, at the pane's own speed, so a shot sounds like the moment it shows:
  * speed != 1 resamples - slow motion drops in pitch the way a film slow-mo does, which is the point of it
  * a freeze (hold) plays up to the held frame and then lets go with a short fade, never a stuck buffer
  * split screens mix their panes at the per-pane `gain` the edit set (0.4 - 0.7), a single pane at 1.0
  * every clip edge gets an 8 ms fade, so a cut never clicks
THE BALANCE is measured, not guessed: the game bus is scaled to sit GAME_UNDER_SONG dB under the song's own
integrated loudness, then the song ducks under the bus's envelope (up to DUCK_DB) so the hits cut through on
the loud sections without the music vanishing, and a limiter at -1 dBFS catches the summed peaks.
"""
import os, sys, json, subprocess, re, wave, struct
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
FPS = 60
GAME_UNDER_SONG = 4.5     # dB under the song (integrated). At 3.0 the game bus measured ABOVE the ducked song (median +0.6 dB RMS)
DUCK_DB = 3.0             # the most the song dips under a loud hit
DUCK_THR_DB = -12.0
BED_UNDER_SONG = 17.0     # LU: the ambience bed under the song, before it ducks under the game       # ...and only a HIT ducks it: at -24 dBFS the dense bus ducked the song 4.5 dB nearly the whole cut
EDGE = int(0.008 * SR)


def ffmpeg_exe():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def decode(path):
    """any audio file -> float32 (n, 2) at 48 kHz"""
    r = subprocess.run([ffmpeg_exe(), '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).reshape(-1, 2).copy()


def read_float_wav(path):
    with open(path, 'rb') as fh:
        data = fh.read()
    i = data.index(b'data')
    n = struct.unpack('<I', data[i + 4:i + 8])[0]
    return np.frombuffer(data[i + 8:i + 8 + n], dtype=np.float32).reshape(-1, 2)


def write_float_wav(path, x):
    x = np.ascontiguousarray(x.astype(np.float32))
    raw = x.tobytes()
    hdr = b'RIFF' + struct.pack('<I', 4 + 26 + 8 + len(raw)) + b'WAVE'
    hdr += b'fmt ' + struct.pack('<IHHIIHH', 18, 3, 2, SR, SR * 8, 8, 32) + struct.pack('<H', 0)
    hdr += b'data' + struct.pack('<I', len(raw))
    with open(path, 'wb') as fh:
        fh.write(hdr)
        fh.write(raw)


def lufs(path):
    r = subprocess.run([ffmpeg_exe(), '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind('Summary'):]
    I = re.search(r'I:\s+(-?[\d.]+) LUFS', tail)
    P = re.search(r'Peak:\s+(-?[\d.]+) dBFS', tail)
    return (float(I.group(1)) if I else None), (float(P.group(1)) if P else None)


def db(x):
    return 10 ** (x / 20.0)


# EVERY TAKE IS LEVELLED BEFORE IT MEETS THE SONG. W_warp's gate run measured far hotter than a boss fight, most
# of it the stage-5 space laser cannon (leaving that one family out dropped the run 6.2 dB). Left alone, every
# warp shot would slam the limiter while a pilot's special sat under the music. Levelling each take to one
# integrated loudness keeps its own dynamics and removes the jumps between shots. Boosts are capped: a menu take
# is a few blips and must not be lifted to battle level.
TAKE_LUFS = -20.0
TAKE_CUT, TAKE_BOOST = -12.0, 3.0


class Stems:
    def __init__(self, takes_dir):
        self.dir, self.cache, self.gains = takes_dir, {}, {}

    def get(self, tid):
        if tid not in self.cache:
            p = os.path.join(self.dir, tid, 'sfx.wav')
            if os.path.exists(p):
                I, _ = lufs(p)
                gdb = 0.0 if (I is None or I < -60) else max(TAKE_CUT, min(TAKE_BOOST, TAKE_LUFS - I))
                self.cache[tid] = read_float_wav(p) * np.float32(db(gdb))
                self.gains[tid] = (I, round(gdb, 1))
            else:
                self.cache[tid] = None
        return self.cache[tid]


def place_pane(bus, clip, pane, stems):
    x = stems.get(pane['take'])
    if x is None:
        return 0
    g = float(pane.get('gain', 1.0 if len(clip['panes']) == 1 else 0.6))
    if g <= 0:
        return 0
    t0, t1 = clip['t0'], clip['t1']
    n = int(round((t1 - t0) * SR))
    o0 = int(round(t0 * SR))
    if n <= 0 or o0 >= len(bus):
        return 0
    n = min(n, len(bus) - o0)
    speed = float(pane.get('speed', 1.0))
    src = pane['src'] / float(FPS)
    tt = np.arange(n, dtype=np.float64) / SR
    st = src + tt * speed
    live = np.ones(n, dtype=np.float32)
    if pane.get('hold') is not None:
        # THE PICTURE FREEZES, THE SOUND DOES NOT (Mike, on v4: "Ensure there is sound all the time"). It rolls on under
        # the held frame and settles 6 dB down over a quarter second, the way a trailer holds a frame without losing the room.
        rel = int(float(pane['hold']) * SR)
        if rel < n:
            k = np.arange(n - rel, dtype=np.float32)
            live[rel:] = 1.0 - 0.5 * np.minimum(1.0, k / float(0.25 * SR))
    if pane.get('desat', 0) >= 0.5:
        g *= 0.6
    pos = st * SR
    i0 = np.floor(pos).astype(np.int64)
    fr = (pos - i0).astype(np.float32)[:, None]
    valid = (i0 >= 0) & (i0 + 1 < len(x))
    i0c = np.clip(i0, 0, len(x) - 2)
    y = x[i0c] * (1 - fr) + x[i0c + 1] * fr
    y[~valid] = 0.0
    env = live.copy()
    e = min(EDGE, n // 2)
    if e > 0:
        ramp = np.linspace(0.0, 1.0, e, dtype=np.float32)
        env[:e] *= ramp
        env[-e:] *= ramp[::-1]
    bus[o0:o0 + n] += y * (env * g)[:, None]
    return 1


def bed_layer(A, N):
    """every clip's stage ambience, looped on trailer time (consecutive clips on a stage continue rather than restart),
    120 ms crossfades at the cuts"""
    spans = A.get('beds') or []
    if not spans:
        return None
    out = np.zeros((N, 2), dtype=np.float32)
    cache = {}
    xf = int(0.12 * SR)
    for b in spans:
        if b['file'] not in cache:
            cache[b['file']] = decode(b['file'])
        y = cache[b['file']]
        o0, o1 = int(round(b['t0'] * SR)), min(N, int(round(b['t1'] * SR)))
        n = o1 - o0
        if n <= 0 or not len(y):
            continue
        env = np.ones(n, dtype=np.float32)
        e = min(xf, n // 2)
        if e > 0:
            r = np.linspace(0.0, 1.0, e, dtype=np.float32)
            env[:e] *= r
            env[-e:] *= r[::-1]
        out[o0:o1] += y[np.arange(o0, o1) % len(y)] * env[:, None]
    return out


def envelope(x, attack=0.01, release=0.30):
    """a fast-attack / slow-release follower on the bus magnitude, in linear amplitude"""
    m = np.abs(x).max(axis=1)
    hop = 240
    blocks = m[:len(m) // hop * hop].reshape(-1, hop).max(axis=1)
    out = np.zeros_like(blocks)
    a = np.exp(-hop / (attack * SR))
    r = np.exp(-hop / (release * SR))
    v = 0.0
    for i, b in enumerate(blocks):
        v = a * v + (1 - a) * b if b > v else r * v + (1 - r) * b
        out[i] = v
    full = np.repeat(out, hop)
    if len(full) < len(m):
        full = np.concatenate([full, np.full(len(m) - len(full), full[-1] if len(full) else 0.0)])
    return full


def mix(edl_path, out_wav):
    E = json.load(open(edl_path))
    A = E['audio']
    N = int(round(A['length'] * SR))
    stems = Stems(A.get('takes_dir') or os.path.join(HERE, 'takes3'))

    bus = np.zeros((N, 2), dtype=np.float32)
    placed = 0
    for c in E['clips']:
        for p in c.get('panes', []):
            placed += place_pane(bus, c, p, stems)
    lv = sorted(stems.gains.items(), key=lambda kv: kv[1][1])
    if lv:
        print('take levelling over %d takes: most cut %s | most lifted %s' % (
            len(lv), ', '.join('%s %+.1f dB' % (k, v[1]) for k, v in lv[:4]),
            ', '.join('%s %+.1f dB' % (k, v[1]) for k, v in lv[-3:])))
    voice = []
    for s in A.get('sfx', []):
        y = decode(s['file']) * db(s.get('gain_db', -10.0))
        o = int(round(s['t'] * SR))
        if o < N:
            k = min(len(y), N - o)
            bus[o:o + k] += y[:k]
            if s.get('duck_db'):
                voice.append((o, k, float(s['duck_db'])))
    sfx_path = os.path.splitext(out_wav)[0] + '_sfx.wav'
    write_float_wav(sfx_path, bus)

    song = decode(A['song'])
    fi = int(float(A.get('song_fade_in', 0.5)) * SR)
    song[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
    song *= db(A.get('song_gain_db', -6.3))
    lay = np.zeros((N, 2), dtype=np.float32)
    o = int(round(A['t0'] * SR))
    k = min(len(song), N - o)
    lay[o:o + k] = song[:k]
    song_path = os.path.splitext(out_wav)[0] + '_song.wav'
    write_float_wav(song_path, lay)

    I_song, _ = lufs(song_path)
    I_bus, _ = lufs(sfx_path)
    trim = 0.0
    if I_song is not None and I_bus is not None:
        trim = (I_song - GAME_UNDER_SONG) - I_bus
        bus *= db(trim)

    env = envelope(bus)
    thr = db(DUCK_THR_DB)
    over = np.clip(20 * np.log10(np.maximum(env, 1e-6) / thr), 0, None)
    duck = db(-np.minimum(DUCK_DB, over * 0.45)).astype(np.float32)
    lay *= duck[:, None]
    if voice:
        # A VOICE LINE dips the song for as long as it speaks. The hit ducker keys on peaks and lets the riff ride over
        # a word (Mike, on v3: "Make sure we hear BULLETS OF FURY in the beginning").
        hop = 480
        vd = np.zeros(N // hop + 2, dtype=np.float32)
        for (o, k, d) in voice:
            a0, a1 = max(0, (o - int(0.08 * SR)) // hop), (o + k) // hop + 1
            vd[a0:a1] = np.maximum(vd[a0:a1], d)
        w = np.hanning(25).astype(np.float32)
        vd = np.convolve(vd, w / w.sum(), mode='same')                 # ~0.25 s in and out, no pumping edge
        lay *= db(-np.repeat(vd, hop)[:N]).astype(np.float32)[:, None]
    stem = os.path.splitext(out_wav)[0]
    bed = bed_layer(A, N)
    if bed is not None:
        write_float_wav(stem + '_bedraw.wav', bed)
        I_bed, _ = lufs(stem + '_bedraw.wav')
        if I_bed is not None and I_song is not None:
            bed *= db((I_song - BED_UNDER_SONG) - I_bed)
        env_db = 20 * np.log10(np.maximum(env, 1e-6))
        bed *= db(-np.clip((env_db + 42.0) * 0.6, 0.0, 14.0)).astype(np.float32)[:, None]   # gone under the game, up in its gaps
        bus += bed
        print('ambience bed: %d spans, %.1f LUFS raw, laid %.0f LU under the song' % (len(A.get('beds') or []), I_bed or 0, BED_UNDER_SONG))
    write_float_wav(stem + '_bus.wav', bus)       # the game bus as mixed (levelled, trimmed) - mixcheck3.py reads it
    write_float_wav(stem + '_duck.wav', lay)      # the song as mixed (ducked)

    ch = A['chime']
    cy = decode(ch['file']) * db(ch.get('gain_db', 0.0))
    total = lay + bus
    o = int(round(ch['t'] * SR))
    k = min(len(cy), N - o)
    total[o:o + k] += cy[:k]
    fo = int(float(A.get('fade_out', 1.2)) * SR)
    total[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]

    pre = os.path.splitext(out_wav)[0] + '_pre.wav'
    write_float_wav(pre, total)
    subprocess.check_call([ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', pre, '-af',
                           'alimiter=limit=0.891:attack=4:release=80:level=false', '-ar', str(SR), '-c:a', 'pcm_s24le', out_wav])
    I, P = lufs(out_wav)
    print('panes with game audio: %d | song %.1f LUFS, game bus %.1f LUFS -> trimmed %+.1f dB | final %s LUFS, peak %s dBFS -> %s'
          % (placed, I_song or 0, I_bus or 0, trim, I, P, out_wav))


def mux(video, wav, out):
    subprocess.check_call([ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-map', '0:v:0', '-map', '1:a:0',
                           '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-shortest',
                           '-movflags', '+faststart', out])
    print('wrote %s (%.1f MB)' % (out, os.path.getsize(out) / 1e6))


if __name__ == '__main__':
    if sys.argv[1] == 'mux':
        mux(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        mix(sys.argv[1], sys.argv[2])
