"""Frame-pacing probe (1009): how evenly do 60 Hz logic ticks land on displayed frames?

Drives the real game loop() with synthetic vsync timestamps at several refresh rates (with realistic
sub-millisecond rAF jitter), the pilot flying steadily right, and records per displayed frame:
  steps  - logic ticks run that frame (BOF_COMBAT_CLOCK.steps)
  dx     - how far the ship moved on screen that frame
A perfectly paced 60 Hz game moves the same distance every frame at 60 Hz, alternates move/hold
in an exact 1-0 rhythm at 120 Hz, and never shows a 0- or 2-tick frame in the middle of a 60 Hz run.
Usage: python _BUILD_SOURCE/probe_pacing_1009.py [label]
"""
import json, sys, statistics
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh
ROOT = Path(__file__).resolve().parents[1]
LABEL = sys.argv[1] if len(sys.argv) > 1 else 'run'
RATES = [('60', 60.0, 0.35), ('59.94', 59.94, 0.35), ('120', 120.0, 0.25), ('144', 144.0, 0.25), ('60 hitchy', 60.0, 2.5)]
RUN = r"""
([hz, jitter, n, seed]) => {
  let s = seed; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const out = [];
  window.__vs = window.__vs || performance.now();
  Input.keys = Input.keys || {};
  for (let i = 0; i < n; i++) {
    window.__vs += 1000 / hz;
    const now = window.__vs + (rnd() * 2 - 1) * jitter;
    const x0 = player.x - (typeof camX === 'number' ? camX : 0), w0 = player.x;
    loop(now);
    const x1 = player.x - (typeof camX === 'number' ? camX : 0);
    out.push([BOF_COMBAT_CLOCK.steps, +(x1 - x0).toFixed(3), +(player.x - w0).toFixed(3)]);
    if (player.x > worldWidth() - 60 || player.x < 60) { player.x = worldWidth() / 2; }
  }
  return out;
}
"""
port, stop = sh.serve(str(ROOT))
res = {}
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--autoplay-policy=no-user-gesture-required'])
        pg = b.new_page(viewport={'width': 960, 'height': 720})
        pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(f'http://127.0.0.1:{port}/index.html')
        pg.wait_for_function('typeof loop==="function" && typeof BOF_COMBAT_CLOCK!=="undefined" && window.__bofAssetRuntimeReady', timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        print(pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole', 'invuln': True}))
        pg.evaluate("()=>{window.__vs=performance.now();for(let i=0;i<120;i++){window.__vs+=1000/60;loop(window.__vs);}}")
        pg.wait_for_timeout(1500)
        for name, hz, jit in RATES:
            pg.evaluate("()=>{player.invuln=1e9;player.x=worldWidth()/2;for(const k of ['arrowright','d'])Input.keys[k]=true;}")
            frames = pg.evaluate(RUN, [hz, jit, 480, 12345])
            frames = frames[30:]
            steps = [f[0] for f in frames]
            if hz < 90: expect = 'one tick every frame'; bad = sum(1 for s in steps if s != 1)
            else:
                ratio = 60 / hz; bad = 0; acc = 0.0
                ideal = []
                for i in range(len(steps)): acc += ratio; k = int(acc + 1e-9); ideal.append(k); acc -= k
                # judder = a frame whose cumulative tick count drifts from the ideal cadence by a whole tick
                # judder = the running tick count drifting a whole tick from the ideal cadence. A constant
                # phase offset (holding on frame 1 instead of frame 0) is not judder, so measure from the mode.
                c1 = c2 = 0; d = []
                for a, i_ in zip(steps, ideal): c1 += a; c2 += i_; d.append(round(c1 - c2, 6))
                bad = min(sum(1 for x in d if not (b - 1e-6 <= x <= b + 1 + 1e-6)) for b in set(d))   # best one-tick-wide window
                expect = 'ideal %.3f ticks/frame cadence' % ratio
            moving = [abs(f[2]) for f in frames if f[0] == 1]
            res[name] = {'frames': len(steps), 'off_cadence_frames': bad, 'zero_tick': steps.count(0), 'double_tick': sum(1 for s in steps if s >= 2),
                         'expect': expect, 'world_dx_per_tick': round(statistics.median(moving), 3) if moving else None}
            print(name, json.dumps(res[name]), flush=True)
            pg.evaluate("()=>{for(const k of ['arrowright','d'])Input.keys[k]=false;}")
        res['errors'] = errs[:5]
        b.close()
finally:
    stop()
out = ROOT / '_shots/pacing_1009'; out.mkdir(parents=True, exist_ok=True)
(out / (LABEL + '.json')).write_text(json.dumps(res, indent=1))
print('errors', res.get('errors'))
