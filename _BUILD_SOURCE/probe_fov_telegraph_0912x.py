"""probe_fov_telegraph_0912x.py - the level-3 laser warns with the Boss Mode pack's FOV cones and alert frames.

Mike, 0912: "Use the proper pov frames for the level 3 boss that we have now" and "When the alert frames show
the laser about to fire. Use those new ones we got that were green yellow and red." His 0906 spec for the
cones: green at 25% when safe, yellow while the attack is prepped with our hazard flashing, red when it is
literally coming - "not with arrows at all".

Drives the real stage-3 boss (cryospear) in real Chromium through shoot.py's server, TRAP_RAF and STEP:
  * the warn is still Mike's 3.00s
  * the draw ASKS FOR bmfx_fov_green_tall in the first third, yellow in the second and red in the last,
    recorded by wrapping XART.get - it returns a canvas with no .src, so a blit cannot be identified any
    other way (CLAUDE.md, 0905h)
  * the frame above the boss is bmfx_alert_<same colour>_danger: green held steady, yellow and red flashing
  * the rime lane never asks for nwarn_lane (the arrows) or the old nwarn signs while the frames are decoded
  * CONTROL: an inferno lane on the same boss still asks for nwarn_lane and never a cone - the family gate
  * PIXELS: the lane below the C cannon shifts toward yellow in the yellow third and toward red in the red
    third against a no-beam baseline - a key that was asked for is not a pixel that landed (0905)
  * zero page/console errors - a draw that throws is swallowed and the tell simply never appears
Writes docs/proofs/fov_telegraph_0912x/_phases.png. Look at it: no number here can see a cone in the wrong place.
"""
import os, sys, io, base64, importlib.util
from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location("shoot", os.path.abspath('_BUILD_SOURCE/shoot.py'))
sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
from playwright.sync_api import sync_playwright

OUT = 'docs/proofs/fov_telegraph_0912x'
os.makedirs(OUT, exist_ok=True)
CAP = "() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }"
HOOK = """() => { if(!window.__kw){ window.__kw=1; const o=XART.get.bind(XART);
  XART.get=function(k){ if(typeof k==='string'&&window.__k) window.__k.push(k); return o(k); }; }
  window.__k=[]; return true; }"""
COLS = ('green', 'yellow', 'red')
KEYS = ['bmfx_fov_%s_tall' % c for c in COLS] + ['bmfx_alert_%s_danger' % c for c in COLS]
FREEZE = """() => { if(boss){ boss.fireCd=1e9; if(boss._s3boss){ boss._s3boss.volley=null; boss._s3boss.cannonSeq=null; } }
  eBullets.length=0; enemies.length=0; }"""
READ = """() => { const B=boss&&boss._l23Beam; return {t:B?B.t:null, rel:B?!!B.released:null,
  keys:(window.__k||[]).filter(function(k){ return k.indexOf('bmfx_')===0||k.indexOf('nwarn_')===0; })}; }"""
GEO = """() => { const m=shipBossMount(boss,'C'); const cam=(worldWidth()>viewW())?camX:0;
  return {mx:m.x, my:m.y, cam:cam, vh:VH, vw:viewW(), vz:(typeof viewZoom==='function'?viewZoom():1)}; }"""


def shot(pg):
    d = pg.evaluate(CAP)
    return Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB') if d else None


def lane_box(g, im):
    """a column straight down the C cannon's lane, below the hull, in canvas pixels - drawWorld's own mapping"""
    s = im.width / float(g['vw'])
    vz = g['vz'] or 1.0
    sy = lambda y: (y * vz + g['vh'] * (1 - vz)) * s
    xc = (g['mx'] - g['cam']) * vz * s
    return (int(xc - 13 * s), int(sy(g['my'] + 110)), int(xc + 13 * s), int(sy(g['vh'] - 16)))


def mean_rgb(im, box):
    return im.crop(box).resize((1, 1), Image.BOX).getpixel((0, 0))


port, stop = sh.serve(sh.GAME)
errs, rows, caps, ctrl = [], [], {}, set()
with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = br.new_page(viewport={'width': 960, 'height': 1040})
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:180]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:180]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF)
    pg.evaluate("() => { ASSETS.ready = true; }")
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'pilot': 'cole', 'stage': 3, 'invuln': True})
    pg.evaluate("""()=>{ run.stage=3; curStage=STAGES[2]; player.dead=false;
      stagePlan=[]; enemies.length=0; eBullets.length=0;
      spawnBoss('cryospear'); if(boss){ boss.enter=false; boss.x=240; boss.y=150; } }""")
    pg.wait_for_timeout(1200); pg.evaluate(sh.STEP, 30); pg.wait_for_timeout(400)
    # XART.rdy is false on its first call - poll the frames in before judging anything
    for _ in range(24):
        pg.evaluate("(ks)=>{ ks.forEach(function(k){ XART.rdy(k); }); }", KEYS + ['nwarn_lane', 'nwarn_yield', 'nwarn_alert'])
        pg.evaluate(sh.STEP, 3); pg.wait_for_timeout(90)
    rdy = pg.evaluate("(ks)=>ks.map(function(k){ return XART.rdy(k); })", KEYS)
    print('frames decoded:', dict(zip(KEYS, rdy)), flush=True)

    pg.evaluate(FREEZE); pg.evaluate("()=>{ boss._l23Beam=null; }")
    pg.evaluate(sh.STEP, 2); pg.wait_for_timeout(80)
    base = shot(pg)
    geo = pg.evaluate(GEO)
    # Mike's alternate Rime Wall volley: C holds a fixed corridor, L and R angled out on their own sides
    pg.evaluate("""()=>{ boss._l23Beam=null;
      l23BossBeamStart(boss,'rime',['L','C','R'],[Math.PI/2+.95, Math.PI/2, Math.PI/2-.95], 1.00, 1.05, .24, 48); }""")
    warm = pg.evaluate("()=>boss._l23Beam?boss._l23Beam.warm:null")
    print('authored warm 1.00 -> effective warm:', warm, flush=True)
    pg.evaluate(HOOK)
    want = {'green': 0.17, 'yellow': 0.50, 'red': 0.86}
    for it in range(140):
        pg.evaluate("()=>{ window.__k=[]; }")
        pg.evaluate(FREEZE)
        pg.evaluate(sh.STEP, 2); pg.wait_for_timeout(45)
        st = pg.evaluate(READ)
        if st['t'] is None:
            break
        k = st['t'] / warm
        rows.append((k, st['rel'], set(st['keys'])))
        for col, at in want.items():
            if col not in caps and not st['rel'] and at <= k < at + 0.08:
                caps[col] = (k, shot(pg), pg.evaluate(GEO))
        if st['rel'] and k > 1.2:
            break

    # CONTROL: the same boss, a lava lane - it must still wear its own plate and never a cone
    pg.evaluate("()=>{ boss._l23Beam=null; l23BossBeamStart(boss,'inferno',['C'],[Math.PI/2],.14,.24,.10,34); }")
    for it in range(40):
        pg.evaluate("()=>{ window.__k=[]; }"); pg.evaluate(FREEZE)
        pg.evaluate(sh.STEP, 2); pg.wait_for_timeout(40)
        ctrl |= set(pg.evaluate("()=>(window.__k||[]).filter(function(k){ return k.indexOf('bmfx_fov')===0||k==='nwarn_lane'; })"))
    br.close()
stop()

fails = []
if not warm or abs(warm - 3.0) > 1e-3:
    fails.append("warn is %s, not Mike's 3.00" % warm)
if not all(rdy):
    fails.append('frames never decoded: %s' % [k for k, r in zip(KEYS, rdy) if not r])
third = {c: [] for c in COLS}
for k, rel, ks in rows:
    if rel or k >= 0.995 or min(abs(k - 1 / 3.0), abs(k - 2 / 3.0)) < 0.03:
        continue          # a frame straddling a boundary reads k one step apart from the draw
    third['red' if k >= 2 / 3.0 else ('yellow' if k >= 1 / 3.0 else 'green')].append(ks)
for col in COLS:
    lst = third[col]
    cone, sign = 'bmfx_fov_%s_tall' % col, 'bmfx_alert_%s_danger' % col
    other = ['bmfx_fov_%s_tall' % c for c in COLS if c != col]
    n = len(lst)
    n_cone = sum(cone in ks for ks in lst)
    n_other = sum(any(o in ks for o in other) for ks in lst)
    n_sign = sum(sign in ks for ks in lst)
    n_lane = sum('nwarn_lane' in ks for ks in lst)
    n_old = sum(('nwarn_yield' in ks or 'nwarn_alert' in ks) for ks in lst)
    print('%-6s third: %3d frames | cone %3d | other cones %d | alert frame %3d (off %3d) | arrow lane %d | old sign %d'
          % (col, n, n_cone, n_other, n_sign, n - n_sign, n_lane, n_old), flush=True)
    if not n:
        fails.append('no frames measured in the %s third' % col)
        continue
    if n_cone < 0.9 * n:
        fails.append('the %s cone drew on %d of %d frames' % (col, n_cone, n))
    if n_other:
        fails.append('%d frames of the %s third asked for another colour' % (n_other, col))
    if n_lane:
        fails.append('the arrow lane was asked for on %d frames of the %s third' % (n_lane, col))
    if n_old:
        fails.append('the old yellow/red sign drew on %d frames of the %s third' % (n_old, col))
    if n_sign == 0:
        fails.append('the %s alert frame never drew' % col)
    if col == 'green' and n - n_sign > 0.1 * n:
        fails.append('the green frame blinked (%d off) - it should hold steady' % (n - n_sign))
    if col != 'green' and n_sign == n:
        fails.append('the %s frame never blinked off - it should flash' % col)

print('control (inferno lane) asked for:', sorted(ctrl), flush=True)
if 'nwarn_lane' not in ctrl:
    fails.append('CONTROL: the lava lane no longer asks for its own plate')
if any(k.startswith('bmfx_fov') for k in ctrl):
    fails.append('CONTROL: the lava lane asked for a cone - the family gate is open')

box = lane_box(geo, base)
b0 = mean_rgb(base, box)
print('lane box %s | no-beam mean rgb %s' % (box, b0), flush=True)
shift = {}
for col in COLS:
    if col not in caps:
        fails.append('no %s frame was captured' % col)
        continue
    k, im, g = caps[col]
    m = mean_rgb(im, lane_box(g, im))
    shift[col] = ((m[0] - m[2]) - (b0[0] - b0[2]), (m[0] - m[1]) - (b0[0] - b0[1]))
    print('%-6s k=%.2f mean rgb %s | R-B shift %+d | R-G shift %+d' % (col, k, m, shift[col][0], shift[col][1]), flush=True)
if 'yellow' in shift and shift['yellow'][0] < 20:
    fails.append('the lane below the C cannon did not go yellow on the canvas (R-B shift %+d)' % shift['yellow'][0])
if 'red' in shift and shift['red'][1] < 20:
    fails.append('the lane below the C cannon did not go red on the canvas (R-G shift %+d)' % shift['red'][1])

# the proof page: no beam, then the three thirds, full frame, side by side
cells = [('baseline', 'no beam', base)] + [(c, '%s  k=%.2f' % (c, caps[c][0]), caps[c][1]) for c in COLS if c in caps]
W = 480
H = int(W * base.height / base.width)
page = Image.new('RGB', (W * len(cells), H + 24), (12, 12, 16))
d = ImageDraw.Draw(page)
for i, (name, lab, im) in enumerate(cells):
    page.paste(im.resize((W, H), Image.LANCZOS), (i * W, 24))
    d.text((i * W + 8, 6), lab, fill=(235, 235, 235))
    im.save(os.path.join(OUT, name + '.png'))
page.save(os.path.join(OUT, '_phases.png'))
print('wrote', os.path.join(OUT, '_phases.png'), flush=True)

if errs:
    fails.append('errors (a swallowed draw error hides the tell): %s' % errs[:2])
print('\n' + ('PASS - 3s warn, green then yellow then red cones and alert frames, no arrows, lava lane unchanged, no errors'
              if not fails else 'FAIL:\n  ' + '\n  '.join(fails)))
sys.exit(1 if fails else 0)
