"""Summarise the wave telemetry sweep (_shots/waves_1103/sweep/*.json) into analysis.json.

    python _BUILD_SOURCE/analyse_waves_1103.py
"""
from pathlib import Path
import json, statistics as stt, collections
R = Path(__file__).resolve().parents[1]; S = R / '_shots/waves_1103/sweep'
runs = {}
for f in S.glob('*.json'):
    d = json.loads(f.read_text())
    if d.get("placeholder"): continue
    st, diff, bot = f.stem.split("-"); runs[(st, diff, bot)] = d

def pct(xs, p):
    xs = sorted(xs); return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else 0

def wave_at(d, t):
    ev = [e for e in d['waves'] if e['clock'] <= t]
    return ev[-1]['i'] if ev else None

def summarise(d):
    sec = d['sec']; n = len(sec) or 1
    nb = [s['nB'] for s in sec]; fired = [s['fired'] for s in sec]; safe = [s['safe'] for s in sec]; ne = [s['nE'] for s in sec]
    # 10 s rolling windows
    win = []
    for i in range(0, max(1, n - 10)):
        w = sec[i:i + 10]
        if not w: break
        hits = (w[-1]['hits'] - (sec[i - 1]['hits'] if i else 0))
        win.append(dict(t=i, shots=sum(s['fired'] for s in w), bullets=round(stt.mean(s['nB'] for s in w), 1), safe=min(s['safe'] for s in w), hits=hits))
    hardest = sorted(win, key=lambda w: (w['hits'], w['shots'], -w['safe']), reverse=True)
    picked = []
    for w in hardest:
        if all(abs(w['t'] - p['t']) >= 15 for p in picked): picked.append(w)
        if len(picked) == 3: break
    for p in picked: p['wave'] = wave_at(d, p['t'] + 5)
    dead, run_, longest = 0, 0, 0
    for s in sec:
        quiet = s['nB'] < 1 and s['fired'] == 0 and s['nE'] < 1
        dead += quiet; run_ = run_ + 1 if quiet else 0; longest = max(longest, run_)
    src = collections.Counter(h['src'] for h in d['hitLog'])
    return dict(
        seconds=n, waves=len(d['waves']), enemies=sum(d['enemyKinds'].values()), shots=d['shots'], shotsPerSec=round(d['shots'] / n, 2),
        peak10Shots=max((w['shots'] for w in win), default=0), bulletsMean=round(stt.mean(nb), 1), bulletsP95=pct(nb, .95), bulletsMax=max((s['nBmax'] for s in sec), default=0),
        enemiesMean=round(stt.mean(ne), 1), enemiesP95=pct(ne, .95), aimed=d['aimedShare'], speedP50=d['speed']['p50'], speedP90=d['speed']['p90'],
        safeP5=pct(safe, .05), tightSec=sum(1 for x in safe if x < .5), crampedSec=sum(1 for x in safe if x < .25),
        deadAirPct=round(100 * dead / n), longestDeadAir=longest, hits=d['hits'], hitsPerMin=d['hitsPerMin'],
        hitSources=src.most_common(6), hardest=picked, bulletKinds=sorted(d['kinds'].items(), key=lambda kv: -kv[1])[:8],
        enemyKinds=sorted(d['enemyKinds'].items(), key=lambda kv: -kv[1])[:10],
        curve=[[s['nB'], s['fired'], s['safe'], s['hits']] for s in sec])

out = {'runs': {}, 'ratios': {}}
for (st, diff, bot), d in sorted(runs.items()):
    out['runs'][f'{st}|{diff}|{bot}'] = summarise(d)
for st in sorted({k[0] for k in runs}, key=lambda s: (int(s.rstrip('r')), s)):
    r = {}
    for bot in ['novice', 'skilled']:
        base = out['runs'].get(f'{st}|normal|{bot}')
        if not base: continue
        for diff in ['hard', 'furious']:
            o = out['runs'].get(f'{st}|{diff}|{bot}')
            if not o: continue
            r[f'{bot}:{diff}'] = {k: (round(o[k] / base[k], 2) if base[k] else None) for k in ['shotsPerSec', 'bulletsMean', 'enemies', 'speedP50', 'hitsPerMin', 'seconds', 'waves']}
    out['ratios'][st] = r
(R / '_shots/waves_1103/analysis.json').write_text(json.dumps(out, indent=1))
print(f"{'stage':6}{'diff':9}{'bot':8}{'sec':>5}{'waves':>6}{'enem':>6}{'shot/s':>7}{'pk10':>6}{'bul':>6}{'bul95':>6}{'aim':>5}{'spd':>5}{'safe5':>6}{'tight':>6}{'dead%':>6}{'hits/m':>7}")
for k, v in out['runs'].items():
    st, diff, bot = k.split('|')
    print(f"{st:6}{diff:9}{bot:8}{v['seconds']:>5}{v['waves']:>6}{v['enemies']:>6}{v['shotsPerSec']:>7}{v['peak10Shots']:>6}{v['bulletsMean']:>6}{v['bulletsP95']:>6}{v['aimed']:>5}{v['speedP50']:>5}{v['safeP5']:>6}{v['tightSec']:>6}{v['deadAirPct']:>6}{v['hitsPerMin']:>7}")
