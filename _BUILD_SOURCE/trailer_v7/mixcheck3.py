"""mixcheck3.py - can the game be heard under the song? Measured per half second, drawn per clip.

    python mixcheck3.py edl3.json mix3.wav        # reads mix3_bus.wav / mix3_duck.wav / mix3.wav, writes mix3_check.png

Mike asked for the game's own sounds in the trailer, and a mix cannot be listened to from here - so it is measured.
For every half second after the song starts: the song as mixed (ducked), the game bus as mixed (levelled and
trimmed), and the final track. A shot whose game audio sits more than BURIED dB under the song is not in the
trailer in any sense that matters, and those shots are listed by clip label so the edit or the levels can move.
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mix3 import decode, lufs      # noqa: E402

SR = 48000
WIN = 0.5
BURIED = 14.0          # dB under the song
ACTIVE = -48.0         # dBFS: below this the bus is silent on purpose (a menu hold, a freeze)


def env_db(x, win=WIN):
    n = int(win * SR)
    k = len(x) // n
    p = (x[:k * n].astype(np.float64) ** 2).mean(axis=1).reshape(k, n).mean(axis=1)
    return 10 * np.log10(p + 1e-12)


def main(edl_path, mix_wav):
    E = json.load(open(edl_path))
    A = E['audio']
    stem = os.path.splitext(mix_wav)[0]
    song, bus, fin = decode(stem + '_duck.wav'), decode(stem + '_bus.wav'), decode(mix_wav)
    n = min(len(song), len(bus), len(fin))
    S, G, F = env_db(song[:n]), env_db(bus[:n]), env_db(fin[:n])
    t = (np.arange(len(S)) + 0.5) * WIN
    clips = sorted(E['clips'], key=lambda c: c['t0'])

    def clip_at(x):
        for c in clips:
            if c['t0'] <= x < c['t1']:
                return c
        return None

    live = (t >= A['t0'] + 0.5) & (t <= A['length'] - A.get('fade_out', 1.2))
    gap = G - S
    act = live & (G > ACTIVE)
    print('windows after the song starts: %d | game bus active in %.0f%% of them' % (live.sum(), 100.0 * act.sum() / max(1, live.sum())))
    if act.any():
        q = np.percentile(gap[act], [10, 50, 90])
        print('game minus song while active: p10 %+.1f dB, median %+.1f dB, p90 %+.1f dB' % tuple(q))
    buried = {}
    for i in np.where(live & (gap < -BURIED))[0]:
        c = clip_at(t[i])
        if c is None or not any((p.get('gain', 1.0) or 0) > 0 for p in c.get('panes', [])):
            continue                                            # a card, a portrait, a freeze: silence is intended
        buried.setdefault(c['label'], []).append(round(float(gap[i]), 1))
    print('shots with sound buried more than %.0f dB under the song: %d' % (BURIED, len(buried)))
    for lab, g in sorted(buried.items(), key=lambda kv: min(kv[1]))[:25]:
        print('   %-44s %d windows, worst %+.1f dB' % (lab[:44], len(g), min(g)))
    I, P = lufs(mix_wav)
    print('final: %s LUFS integrated, %s dBFS peak' % (I, P))

    # the picture: song / game / final envelopes, clip boundaries, a tick every 10 s
    px = 10                                                     # pixels per second
    Wd, lane, top = int(A['length'] * px) + 60, 110, 28
    im = Image.new('RGB', (Wd, top + 3 * lane + 30), (14, 14, 18))
    d = ImageDraw.Draw(im)
    names = [('SONG (ducked)', S, (90, 150, 255)), ('GAME (as mixed)', G, (255, 150, 60)), ('FINAL', F, (200, 200, 200))]
    for k, (name, series, col) in enumerate(names):
        y0 = top + k * lane
        d.text((4, y0 + 2), name, fill=col)
        for i, v in enumerate(series):
            h = int(max(0.0, min(1.0, (v + 60.0) / 60.0)) * (lane - 18))
            x = 50 + int(t[i] * px)
            d.line([(x, y0 + lane - 4), (x, y0 + lane - 4 - h)], fill=col, width=max(1, int(WIN * px) - 1))
    for c in clips:
        x = 50 + int(c['t0'] * px)
        d.line([(x, top - 6), (x, top + 3 * lane)], fill=(40, 40, 52))
    for s in range(0, int(A['length']) + 1, 10):
        x = 50 + s * px
        d.line([(x, top - 10), (x, top - 2)], fill=(160, 160, 160))
        d.text((x + 2, 4), '%ds' % s, fill=(160, 160, 160))
    for i in np.where(live & (gap < -BURIED))[0]:
        c = clip_at(t[i])
        if c is not None and any((p.get('gain', 1.0) or 0) > 0 for p in c.get('panes', [])):
            x = 50 + int(t[i] * px)
            d.rectangle([x - 2, top + 3 * lane + 6, x + 2, top + 3 * lane + 14], fill=(230, 60, 60))
    out = stem + '_check.png'
    im.save(out)
    print('wrote', out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
