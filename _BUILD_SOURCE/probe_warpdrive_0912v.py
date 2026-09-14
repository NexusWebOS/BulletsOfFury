#!/usr/bin/env python3
"""probe_warpdrive_0912v.py - the stage-5 warp drive, flown gate by gate in real Chromium.

    python _BUILD_SOURCE/probe_warpdrive_0912v.py            # assertions + stills
    python _BUILD_SOURCE/probe_warpdrive_0912v.py --video    # also a 30fps flight, encoded to mp4

An autopilot holds the next gate's line (it writes player.x, which is what the stick would move) and
keeps the pilot alive; everything else - the pass test, the drive, the warp-out, the map - is the game's
own code reacting. Keys are identified by wrapping XART.get and recording the KEY asked for; the tunnel's
placement is proved by recording the MATRIX ctx held when it was blitted, on ctx's own drawImage (0905h:
the prototype trap records nothing, and XART.get has no .src).

⚠ THE PILOT IS KEPT ALIVE BY STUBBING playerHit, NOT BY PINNING invuln. The first cut held invuln at
99999, and the damage blink is Math.floor(invuln/4)%2 - so the ship sat on its HIDDEN phase for the whole
flight and every frame of the video showed gates being passed by nothing. invuln stays 0 here.
"""
import os, sys, json, base64, argparse, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shoot as sh  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUT = os.path.join(ROOT, 'docs', 'proofs', 'warpdrive_0912v')

GRAB = ("(fmt) => { const g=document.querySelector('#screen-area canvas')||document.querySelector('#screen')"
        "||document.querySelector('canvas'); if(!g) return null;"
        " return fmt==='jpg' ? g.toDataURL('image/jpeg',0.9) : g.toDataURL('image/png'); }")

SETUP = r"""
() => {
  ASSETS.ready = true; run.pilot = 'cole'; run.mode = 'arcade';
  if (typeof STAGES !== 'undefined') curStage = STAGES[4];
  beginStage(5); setState(GS.PLAY);
  run._s9taken = 0; run._s9warp = 0; run._s9gate = null;
  player.reset(); player.dead = false; player.invuln = 0; player.y = VH*0.72;
  enemies.length = 0; eBullets.length = 0; pBullets.length = 0;
  campaign.bonusUnlocked = 0; campaign.unlockedMax = 8;
  window.__hits = 0;
  playerHit = function(){ window.__hits++; };           // alive without touching the damage blink
  s5RunInit();
  s5run.spawned = {c1:1, c2:1, mega:1, clash:1};        // the comets and the clash pair are the run's hazards, not the drive's
  window.__keys = {}; window.__lastKey = null; window.__tun = [];
  const g = XART.get;
  XART.get = function(k){ window.__keys[k] = (window.__keys[k]||0) + 1; window.__lastKey = k; return g.apply(this, arguments); };
  const di = ctx.drawImage;
  ctx.drawImage = function(){
    try{
      const k = window.__lastKey;
      if (k && k.indexOf('nfx_warp_tunnel_') === 0 && window.__tun.length < 5000) {
        const m = ctx.getTransform();
        /* tag the CALLER, not the phase: through the jump both the drive (vanishing point) and warpFxDraw
           (screen centre) blit the tunnel in the same frame. Tagging by "s9warp is live" put the drive's own
           blits in the jump bucket twice running, and both runs reported 105px = |VW/2 - vpx| exactly.
           0 = drawn inside wdDriveBackDraw, 1 = drawn by anything else (on stage 5 that is warpFxDraw). */
        window.__tun.push([Math.hypot(m.a, m.b), m.e, m.f, (worldWidth() > viewW() ? camX : 0), wdrive.vpx, window.__inDrive ? 0 : 1]);
      }
    }catch(e){}
    window.__lastKey = null;
    return di.apply(this, arguments);
  };
  /* wdDriveBackDraw is a top-level function declaration, so this reassignment IS the binding the scenery
     hook calls by bare name. It only raises a flag around the original; behaviour is unchanged. */
  window.__inDrive = 0;
  const wd0 = wdDriveBackDraw;
  wdDriveBackDraw = function(){ window.__inDrive = 1; try{ return wd0.apply(this, arguments); } finally { window.__inDrive = 0; } };
  const warm = [];
  for (let i=0;i<8;i++) warm.push('ch_warp_'+i, 'chrift_'+i, 'nfx_wportal_'+i, 'nsr_comet_'+i, 'nfx_s5gate96_'+i);
  for (let i=0;i<16;i++) warm.push('nfx_warp_tunnel_'+i);
  window.__warm = warm; warm.forEach(k => { try{ XART.rdy(k); }catch(e){} });
  /* the autopilot: hold the next gate's line and keep the field clear */
  window.__qaTick = function(){
    try{
      player.dead = false;
      enemies.length = 0; eBullets.length = 0;
      /* the crates the cleared enemies drop are real gameplay, but in a recording of the jump they float
         through the portal and read as part of the effect */
      if (typeof powerups !== 'undefined' && powerups && powerups.length) powerups.length = 0;
      if (s5run && !s5run.done && !s9warp) {
        let tgt = null;
        for (const q of s5run.gates) { if (!q.passed && !q.missed) { tgt = q; break; } }
        if (tgt) { const dx = tgt.x - player.x; player.x += Math.max(-7, Math.min(7, dx)); }
        player.y = VH*0.72;
      }
    }catch(e){}
  };
  return {state: String(state), gates: s5run ? s5run.gates.length : 0, ww: worldWidth(), vw: viewW()};
}
"""

STATE = r"""
() => ({state: String(state), idx: s5run ? s5run.idx : -1, done: s5run ? !!s5run.done : null,
  failed: s5run ? !!s5run.failed : null, lvl: wdrive.lvl, surge: wdrive.surge, flash: wdrive.flash,
  mul: wdScrollMul(), scroll: _stage5SpaceScroll,
  s9: s9warp ? {ph: s9warp.ph, t: s9warp.t, gx: s9warp.gx, gy: s9warp.gy, px: s9warp.px, py: s9warp.py, gone: !!s9warp.gone} : null,
  px: player.x, py: player.y, inv: player.invuln, camX: camX, gate: run._s9gate || null,
  glow: (s5run && s5run.gates[7]) ? s5run.gates[7].glow : 0,
  whiteIn: drawStageSelect._whiteIn || 0, s9cine: s9MapCine ? s9MapCine.ph : null,
  bonus: campaign.bonusUnlocked|0, time: stageTimer, hits: window.__hits|0})
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video', action='store_true')
    ap.add_argument('--out', default=OUT)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    vdir = os.path.join(tempfile.gettempdir(), 'bof_warpdrive_video')
    if args.video:
        os.makedirs(vdir, exist_ok=True)
        for f in os.listdir(vdir):
            os.remove(os.path.join(vdir, f))

    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(ROOT)
    errs, results = [], []

    def ok(cond, name, detail=''):
        results.append((bool(cond), name, detail))
        print(('  ok   ' if cond else '  FAIL ') + name + ('   [' + str(detail) + ']' if detail != '' else ''))

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:220]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(sh.TRAP_RAF)
        pg.wait_for_timeout(50)
        s = pg.evaluate(SETUP)
        ok(s['state'] == 'play' and s['gates'] == 8, 'stage 5 is live with the eight-gate convoy formed', s)
        pg.wait_for_function("() => window.__warm.every(k => XART.rdy(k))", timeout=60000, polling=200)
        ok(True, 'the drive art decoded before the first gate (rdy polled against real time)')

        n_img = [0]

        def shot(name):
            d = pg.evaluate(GRAB, 'png')
            open(os.path.join(args.out, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

        def vframe():
            d = pg.evaluate(GRAB, 'jpg')
            open(os.path.join(vdir, 'f_%05d.jpg' % n_img[0]), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
            n_img[0] += 1

        sim = 0.0
        prev_idx, took = 0, set()
        lvl_after = {}
        scroll_samples = []
        stagesel_at = None
        s9_seen = False
        gate_at_pass = None
        carry_err = None
        gone_before_white = None
        seen_wportal_before_warp = None
        max_inv = 0
        while sim < 60.0:
            e = pg.evaluate(sh.STEP, 2)
            if e:
                errs.append('STEP threw: ' + e)
                break
            sim += 2 / 60.0
            pg.wait_for_timeout(8)
            a = pg.evaluate(STATE)
            if a['state'] == 'play':
                max_inv = max(max_inv, a['inv'] or 0)
            scroll_samples.append((sim, a['scroll'], a['idx'], a['s9'] is not None))
            if args.video and sim >= 3.2:
                vframe()
            if a['idx'] > prev_idx:
                for i in range(prev_idx + 1, a['idx'] + 1):
                    lvl_after[i] = sim
                if a['idx'] == 1:
                    shot('w02_gate1_jump')
                if a['idx'] == 8:
                    gate_at_pass = a['gate']
                prev_idx = a['idx']
            for i, t0 in list(lvl_after.items()):
                if isinstance(t0, float) and sim - t0 >= 0.9:
                    lvl_after[i] = ('lvl', a['lvl'])
            if 'pre' not in took and a['idx'] == 0 and sim > 3.3:
                shot('w01_before_gate1'); took.add('pre')
            if 'g1b' not in took and a['idx'] >= 1 and isinstance(lvl_after.get(1), tuple):
                shot('w03_gate1_after'); took.add('g1b')
            if 'g4' not in took and a['idx'] >= 4 and isinstance(lvl_after.get(4), tuple):
                shot('w04_drive_half'); took.add('g4')
            if 'g7' not in took and a['glow'] > 0.6 and a['idx'] >= 7:
                shot('w05_portal_forms_in_gate8'); took.add('g7')
                k = pg.evaluate("() => window.__keys")
                seen_wportal_before_warp = sum(v for kk, v in k.items() if kk.startswith('nfx_wportal_'))
            if a['s9']:
                s9 = a['s9']
                if not s9_seen:
                    s9_seen = True
                    ok(gate_at_pass is not None and abs(s9['gx'] - gate_at_pass['x']) < 0.01,
                       'the warp-out anchors on the gate that finished the run, in world space',
                       {'gate': gate_at_pass, 's9': s9})
                if s9['ph'] == 'draw' and 'c' not in took and s9['t'] >= 0.45:
                    shot('w06_warp_charge'); took.add('c')
                if s9['ph'] == 'draw' and carry_err is None and s9['t'] >= 0.80:
                    carry_err = abs(a['px'] - s9['px'])
                if s9['ph'] == 'draw' and 'j' not in took and s9['t'] >= 1.02:
                    shot('w07_warp_jump'); took.add('j')
                if s9['ph'] == 'draw' and 'r' not in took and s9['t'] >= 1.30:
                    shot('w08_rift'); took.add('r')
                if s9['ph'] == 'white' and gone_before_white is None:
                    gone_before_white = s9['gone'] or a['py'] < -1000
                if s9['ph'] == 'white' and 'w' not in took and s9['t'] >= 0.3:
                    shot('w09_white_hold'); took.add('w')
            if a['state'] == 'stagesel':
                if stagesel_at is None:
                    stagesel_at = sim
                    ok(a['whiteIn'] > 0.8, 'the map opens INSIDE the held white', round(a['whiteIn'], 3))
                    shot('w10_map_from_white')
                if 'm1' not in took and sim - stagesel_at >= 0.45:
                    shot('w11_map_resolving'); took.add('m1')
                if 'm2' not in took and sim - stagesel_at >= 0.95:
                    ok(a['whiteIn'] <= 0.01, 'and resolves out of it in under a second', round(a['whiteIn'], 3)); took.add('m2')
                if 'm3' not in took and sim - stagesel_at >= 2.3:
                    shot('w12_bonus_unlock_on_map'); took.add('m3')
                if sim - stagesel_at >= 3.4:
                    break

        fin = pg.evaluate(STATE)
        k = pg.evaluate("() => window.__keys")
        tun = pg.evaluate("() => window.__tun")
        b.close()
    stop()

    ok(max_inv < 4, 'the pilot flew the run with no damage blink, so every frame shows the ship', max_inv)
    ok(prev_idx == 8, 'every gate is passed by flying its line, no partial credit', prev_idx)
    lv = {i: v[1] for i, v in lvl_after.items() if isinstance(v, tuple)}
    ok(all(i in lv for i in (2, 4, 6)) and lv[2] < lv[4] < lv[6], 'the drive level climbs gate by gate',
       {i: round(v, 3) for i, v in sorted(lv.items())})

    def rate(pred):
        pts = [(t, sc) for (t, sc, idx, w) in scroll_samples if pred(idx, w)]
        if len(pts) < 10:
            return None
        pts = pts[len(pts) // 3:]
        return (pts[-1][1] - pts[0][1]) / max(1e-6, pts[-1][0] - pts[0][0])
    r0, r7 = rate(lambda idx, w: idx == 0 and not w), rate(lambda idx, w: idx >= 7 and not w)
    ok(r0 is not None and r7 is not None and r7 > 3 * r0, 'space itself accelerates with the drive (px/s of the stage-5 loop)',
       {'before': r0 and round(r0, 1), 'gate7+': r7 and round(r7, 1)})
    burst = sum(v for kk, v in k.items() if kk.startswith('ch_warp_'))
    ring = sum(v for kk, v in k.items() if kk.startswith('nsr_comet_'))
    ok(burst > 0 and ring > 0, "every pass fires the authored jump burst and stage 5's own shock ring", {'ch_warp': burst, 'nsr_comet': ring})
    ok(seen_wportal_before_warp and seen_wportal_before_warp > 0, 'the portal forms inside gate eight while it glows, before the jump',
       seen_wportal_before_warp)
    ok(sum(v for kk, v in k.items() if kk.startswith('chrift_')) > 0, 'the rift tears open through the jump')
    run_t = [r for r in tun if r[5] == 0 and r[0] > 0]
    jump_t = [r for r in tun if r[5] == 1 and r[0] > 0]
    offs = [abs(e / sc - vpx) for (sc, e, f, cx, vpx, ph) in run_t]
    cams = [cx for (sc, e, f, cx, vpx, ph) in run_t]
    ok(len(run_t) > 60 and max(offs) < 1.5 and (max(cams) - min(cams)) > 30,
       "the drive's tunnel is drawn in SCREEN space: on the vanishing point to the pixel while the camera travels",
       {'blits': len(run_t), 'worst_px': round(max(offs), 3) if offs else None,
        'camX_span': round(max(cams) - min(cams), 1) if cams else None})
    joffs = [abs(e / sc - 240) for (sc, e, f, cx, vpx, ph) in jump_t]
    ok(len(jump_t) > 5 and max(joffs) < 1.5, 'and the jump\'s bend (warpFxDraw) is centred on the SCREEN, not dragged by the camera',
       {'blits': len(jump_t), 'worst_px': round(max(joffs), 3) if joffs else None})
    ok(carry_err is not None and carry_err < 3, 'the ship is carried under gate eight in world space, not toward a screen point', carry_err)
    ok(gone_before_white is True, 'and is punched through the mouth and gone before the white', gone_before_white)
    ok(fin['state'] == 'stagesel' and (fin['s9cine'] is not None or fin['bonus'] == 1), 'the map takes over and runs the bonus unlock',
       {'state': fin['state'], 'cine': fin['s9cine'], 'bonus': fin['bonus']})
    ok(not errs, 'no page errors, no swallowed throws', errs[:4])

    if args.video and n_img[0] > 10:
        import imageio_ffmpeg
        mp4 = os.path.join(vdir, 'warpdrive_0912v.mp4')
        subprocess.check_call([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-framerate', '30',
                               '-i', os.path.join(vdir, 'f_%05d.jpg'), '-vf', 'scale=720:-2', '-c:v', 'libx264',
                               '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', mp4])
        print('video: %d frames -> %s (%.1f MB)' % (n_img[0], mp4, os.path.getsize(mp4) / 1e6))

    fails = [r for r in results if not r[0]]
    print('\n%d ok / %d fail' % (len(results) - len(fails), len(fails)))
    json.dump({'results': results, 'errors': errs}, open(os.path.join(args.out, 'probe_result.json'), 'w'), indent=1)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
