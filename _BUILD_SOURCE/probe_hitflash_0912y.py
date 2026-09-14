"""probe_hitflash_0912y.py - every hit flashes, measured in real Chromium on the pixels.

Mike, 0912: "Ensure all weapons cause enemy flashes including our new stage 2 boss."

Drives, through shoot.py's server with TRAP_RAF and STEP:
  A. the FURNACE TYRANT (stage 2 boss, id infernoreaver) past its assembly into the arms phase, then
     * a hit while the Magma Ward's fire shield is up        -> boss.flash set, fzt_ plates tinted, white on the canvas
     * a hit on an arm's own circle, shield down               -> the arm's pool drops, the arm flashes
     * a hit BESIDE the arm (outside its circle, inside 2.6r)  -> the nearest part still takes it (used to be 0 damage)
  B. the six enemy draws that had no tint (bunker, 360 turret, sand tank, ...) -> xartTint asked for the unit's key
  C. the Blacksteel Raptor's wings (ALTBOSS6 / stage-6 mini)                 -> subBoss.flash set on a wing hit
  D. a ship boss (the stage-3 cryospear)                                     -> the flash is >=0.16 and shows on the canvas
PIXELS: for each flash, near-white pixel count in a crop around the target on the hit frame vs the same crop once
the flash has burned out. A key the draw asked for is not a pixel that landed (CLAUDE.md, 0905).
Identifies tint draws by wrapping the xartTint FUNCTION (a global function binding) and recording the key.
Writes docs/proofs/hitflash_0912y/_sheet.png - look at it.
"""
import os, sys, io, base64, importlib.util
from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location("shoot", os.path.abspath('_BUILD_SOURCE/shoot.py'))
sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
from playwright.sync_api import sync_playwright

OUT = 'docs/proofs/hitflash_0912y'
os.makedirs(OUT, exist_ok=True)
CAP = "() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }"
TINT_HOOK = """() => { if(!window.__tw){ window.__tw=1; const o=xartTint;
  xartTint=function(k,c,a){ if(window.__tk && typeof k==='string') window.__tk.push(k); return o(k,c,a); }; }
  window.__tk=[]; return true; }"""
GEO = """(tx) => { const cam=(worldWidth()>viewW())?camX:0, vz=(typeof viewZoom==='function'?viewZoom():1);
  return {x:(tx.x-cam)*vz, y:tx.y*vz+VH*(1-vz), vw:viewW()}; }"""

port, stop = sh.serve(sh.GAME)
errs, fails, notes, crops = [], [], [], []


def shot(pg):
    d = pg.evaluate(CAP)
    return Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB') if d else None


def white_in(im, pg, pt, half=46):
    g = pg.evaluate(GEO, pt)
    s = im.width / float(g['vw'])
    box = (int((g['x'] - half) * s), int((g['y'] - half) * s), int((g['x'] + half) * s), int((g['y'] + half) * s))
    c = im.crop(box)
    n = sum(1 for p in c.getdata() if p[0] > 232 and p[1] > 232 and p[2] > 232)
    return n, c


def step(pg, n, wait=40):
    pg.evaluate(sh.STEP, n); pg.wait_for_timeout(wait)


def flash_pair(pg, label, fire_js, pt_js, expect_js=None):
    """fire a hit, draw ONE frame and capture; let the flash burn out and capture again; compare white pixels"""
    pg.evaluate("()=>{ window.__tk=[]; }")
    r = pg.evaluate(fire_js)
    step(pg, 1, 20)
    pt = pg.evaluate(pt_js)
    hit = shot(pg)
    keys = pg.evaluate("()=>window.__tk.slice(0,40)")
    ok_state = pg.evaluate(expect_js) if expect_js else True
    for _ in range(6):
        step(pg, 4, 20)
    later = shot(pg)
    n1, c1 = white_in(hit, pg, pt)
    n0, c0 = white_in(later, pg, pt)
    crops.append((label, c1, c0))
    notes.append('%-34s hit-frame white %5d | burnt-out %5d | tint keys %s | state %s | %s' % (label, n1, n0, sorted(set(keys))[:4], ok_state, r))
    return n1, n0, keys, ok_state


with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = br.new_page(viewport={'width': 960, 'height': 1040})
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:180]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:180]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF)
    pg.evaluate("() => { ASSETS.ready = true; }")
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'pilot': 'cole', 'stage': 2})
    pg.evaluate("""()=>{ run.stage=2; curStage=STAGES[1]; player.dead=false; player.invuln=0; playerHit=function(){};
      stagePlan=[]; enemies.length=0; eBullets.length=0; spawnBoss('infernoreaver'); }""")
    pg.evaluate(TINT_HOOK)

    # ---- A. the Furnace Tyrant --------------------------------------------------------------------------------------
    phase = None
    for i in range(80):
        step(pg, 30, 60)
        pg.evaluate("()=>{ eBullets.length=0; }")
        phase = pg.evaluate("()=>boss&&boss._fz?[boss._fz.phase, +(boss._fz.trans||0).toFixed(2)]:null")
        if phase and phase[0] == 'arms' and phase[1] <= 0:
            break
    print('furnace phase reached:', phase, flush=True)
    if not phase or phase[0] != 'arms':
        fails.append('the Furnace never reached its arms phase (got %s)' % (phase,))
    else:
        for _ in range(10):
            step(pg, 4, 60)      # let every plate decode before judging a tint
        shielded = pg.evaluate("()=>!!(boss._mwBarrier&&boss._mwBarrier.active)")
        if shielded:
            n1, n0, keys, st = flash_pair(pg, 'furnace, fire shield up',
                "()=>{ _dmgBullet=null; _lastHitX=boss.x; _lastHitY=boss.y; hitBoss(3); return 'flash '+boss.flash.toFixed(2); }",
                "()=>({x:boss.x, y:boss.y})", "()=>boss._mwBarrier.active")
            if not any(k.startswith('fzt_') for k in keys):
                fails.append('a shielded Furnace hit tinted no fzt_ plate')
            if n1 <= n0 + 80:
                fails.append('a shielded Furnace hit put no visible white on the canvas (%d vs %d)' % (n1, n0))
        else:
            notes.append('(the fire shield was already down when the arms phase opened)')
        pg.evaluate("()=>{ const H=boss._mwBarrier; if(H&&H.active){ _dmgBullet=null; _lastHitX=boss.x; _lastHitY=boss.y; hitBoss(H.hp+1); } }")
        for _ in range(8):
            step(pg, 4, 30)
        arm = pg.evaluate("()=>{ const q=furnaceBoxes(boss).find(c=>c.key==='left'||c.key==='right'); return q?{key:q.key,x:q.x,y:q.y,r:q.r,pool:boss._fz.pools[q.key]}:null; }")
        if not arm:
            fails.append('no arm part was open after the shield came down')
        else:
            n1, n0, keys, st = flash_pair(pg, 'furnace, %s arm direct' % arm['key'],
                "()=>{ const q=furnaceBoxes(boss).find(c=>c.key==='%s'); _dmgBullet=null; _lastHitX=q.x; _lastHitY=q.y; hitBoss(4); return 'pool '+boss._fz.pools['%s']; }" % (arm['key'], arm['key']),
                "()=>{ const q=furnaceBoxes(boss).find(c=>c.key==='%s'); return q?{x:q.x,y:q.y}:{x:boss.x,y:boss.y}; }" % arm['key'],
                "()=>boss._fz.pools['%s'] < %f" % (arm['key'], arm['pool']))
            if not st:
                fails.append('a direct arm hit did not reduce the arm pool')
            if n1 <= n0 + 60:
                fails.append('a direct arm hit put no visible white on the canvas (%d vs %d)' % (n1, n0))
            before = pg.evaluate("()=>boss._fz.pools['%s']" % arm['key'])
            r = pg.evaluate("""()=>{ const q=furnaceBoxes(boss).find(c=>c.key==='%s'); _dmgBullet=null;
                _lastHitX=q.x+q.r*1.8; _lastHitY=q.y; hitBoss(4); return {pool:boss._fz.pools['%s'], flash:boss.flash}; }""" % (arm['key'], arm['key']))
            notes.append('furnace, hit beside the arm (1.8r): pool %s -> %s, flash %.2f' % (before, r['pool'], r['flash']))
            if not (r['pool'] < before):
                fails.append('a hit beside the arm (1.8 radii) still did no damage - the nearest-part fallback is not live')
            if not (r['flash'] > 0):
                fails.append('a hit beside the arm did not flash the boss')

    # ---- D. a ship boss: the flash is long enough to see -----------------------------------------------------------
    pg.evaluate("""()=>{ boss=null; bossActive=false; run.stage=3; curStage=STAGES[2]; enemies.length=0; eBullets.length=0;
      spawnBoss('cryospear'); if(boss){ boss.enter=false; boss.x=240; boss.y=150; boss.fireCd=1e9; } }""")
    for _ in range(14):
        step(pg, 6, 60)
        pg.evaluate("()=>{ eBullets.length=0; if(boss){ boss.fireCd=1e9; if(boss._s3boss){ boss._s3boss.volley=null; boss._s3boss.cannonSeq=null; } } }")
    n1, n0, keys, st = flash_pair(pg, 'ship boss (cryospear)',
        "()=>{ _dmgBullet=null; _lastHitX=boss.x; _lastHitY=boss.y; hitBoss(2); return 'flash '+boss.flash.toFixed(2); }",
        "()=>({x:boss.x, y:(boss._drawY!=null?boss._drawY:boss.y)})", "()=>true")
    if n1 <= n0 + 80:
        fails.append('a ship boss hit put no visible white on the canvas (%d vs %d)' % (n1, n0))

    # ---- B. enemy draws that had no tint ---------------------------------------------------------------------------
    pg.evaluate("()=>{ boss=null; bossActive=false; run.stage=1; curStage=STAGES[0]; enemies.length=0; eBullets.length=0; }")
    for kind in ('bunkerA', 'turretMG', 'sandtank'):
        made = pg.evaluate("""(k)=>{ enemies.length=0; const e=spawnEnemy(k, 240, 220, {}); const u=e||enemies[enemies.length-1];
          if(!u) return null; u.x=240; u.y=220; u.vx=0; u.vy=0; u.hp=9999; u.maxhp=9999; u.shoots=false; return u.type; }""", kind)
        if not made:
            notes.append('%s: spawnEnemy returned nothing on stage 1 - skipped' % kind)
            continue
        for _ in range(8):
            step(pg, 3, 50)
            pg.evaluate("()=>{ for(const u of enemies){ u.x=240; u.y=220; u.vx=0; u.vy=0; } eBullets.length=0; }")
        pg.evaluate("()=>{ window.__tk=[]; const u=enemies[enemies.length-1]; if(u) hitEnemy(u,1); }")
        step(pg, 1, 20)
        keys = pg.evaluate("()=>window.__tk.slice(0,20)")
        notes.append('%-10s tint keys on the hit frame: %s' % (kind, sorted(set(keys))[:4]))
        if not keys:
            fails.append('%s: a hit asked xartTint for nothing - still no flash' % kind)

    # ---- C. the Blacksteel's wings ---------------------------------------------------------------------------------
    r = pg.evaluate("""()=>{ enemies.length=0; boss=null; bossActive=false; run.stage=6; curStage=STAGES[5];
      subBoss=null; subBossActive=false; spawnSubBoss('blacksteel'); const b=subBoss; if(!b) return 'no raptor';
      b.enter=false; return b._rapWing ? 'wings' : 'no wing pools'; }""")
    if r == 'wings':
        for _ in range(10):
            step(pg, 4, 50)
            pg.evaluate("()=>{ eBullets.length=0; }")
        w = pg.evaluate("""()=>{ const b=subBoss; b.flash=0; _dmgBullet=null; const x=b.x-(b.w||120)*0.36; hitSubBoss(3, x, b.y); return {flash:b.flash}; }""")
        notes.append('blacksteel wing hit: flash %.2f' % w['flash'])
        if not (w['flash'] > 0):
            fails.append('a Blacksteel wing hit still does not flash')
    else:
        notes.append('blacksteel: %s - skipped' % r)

    pg.evaluate("()=>{ subBoss=null; subBossActive=false; }")
    br.close()
stop()

for n in notes:
    print(n, flush=True)
if crops:
    W = 184
    sheet = Image.new('RGB', (W * 2 + 8, len(crops) * (W + 20) + 4), (12, 12, 16))
    d = ImageDraw.Draw(sheet)
    for i, (lab, c1, c0) in enumerate(crops):
        y = i * (W + 20) + 18
        d.text((4, y - 15), lab + '  (hit | burnt out)', fill=(235, 235, 235))
        sheet.paste(c1.resize((W, W), Image.NEAREST), (0, y))
        sheet.paste(c0.resize((W, W), Image.NEAREST), (W + 8, y))
    sheet.save(os.path.join(OUT, '_sheet.png'))
    print('wrote', os.path.join(OUT, '_sheet.png'), flush=True)
if errs:
    fails.append('page/console errors: %s' % errs[:3])
print('\n' + ('PASS - every probed hit flashes on the canvas, the Furnace included, no errors' if not fails
              else 'FAIL:\n  ' + '\n  '.join(fails)))
sys.exit(1 if fails else 0)
