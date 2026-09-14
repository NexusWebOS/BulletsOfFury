"""check_warn_pick.py - where the level-3 boss shots landed on the laser warn (Mike, on v5: the green/yellow/red frames).

    python check_warn_pick.py        # reads edl3.json and each take's metrics.json

Prints, every 10 frames through each shot, the warn capture3 logged as metrics['lb'] = [family, fraction, released]:
green below 0.33, yellow to 0.67, red to 1.00, FIRE once released.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = int(re.search(r'^FPS\s*(?:,[^=\n]*)?=\s*(\d+)', open(os.path.join(HERE, 'edit3.py'), encoding='utf-8').read(), re.M).group(1))   # edit3: FPS, W, H = 60, 1920, 1080
E = json.load(open(os.path.join(HERE, 'edl3.json')))


def colour(k):
    return 'red' if k >= 2 / 3.0 else ('yellow' if k >= 1 / 3.0 else 'green')


for c in sorted(E['clips'], key=lambda c: c['t0']):
    lab = c.get('label') or ''
    if lab not in ('BOSS s3', 'vs boss E2_s3'):
        continue
    p = c['panes'][0]
    M = json.load(open(os.path.join(HERE, 'takes3', p['take'], 'metrics.json')))
    s, n = int(p['src']), int(round((c['t1'] - c['t0']) * FPS * float(p.get('speed', 1.0))))
    path = []
    for i in range(s, min(len(M), s + n + 1), 10):
        lb = M[i].get('lb')
        if not lb:
            path.append('+%d -' % (i - s))
        elif lb[2]:
            path.append('+%d FIRE' % (i - s))
        else:
            path.append('+%d %s %.2f' % (i - s, colour(lb[1]), lb[1]))
    print('%-14s t %.2f-%.2f  %s src %d (%d frames @%d)\n    %s' % (lab, c['t0'], c['t1'], p['take'], s, n, FPS, ' | '.join(path)))
