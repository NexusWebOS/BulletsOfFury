#!/usr/bin/env python3
"""probe_cmap2_0912v.py - the campaign map in pieces, driven like a player in real Chromium.

    python _BUILD_SOURCE/probe_cmap2_0912v.py            # verify: assertions + stills
    python _BUILD_SOURCE/probe_cmap2_0912v.py --tour     # also a 30fps flight for a video

Drives the real index.html through shoot.py's server, TRAP_RAF and STEP. Every input is a real key
tap through Input.injectTap, read by the game's own handlers - the probe never writes sselCursor,
cmap2.focus or campPause itself, so it cannot assert a change it made (CLAUDE.md, 0906e).
Keys are identified by wrapping XART.get and recording the KEY asked for (0905h: XART.get returns
a fresh canvas with no .src).
"""
import os, sys, json, base64, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shoot as sh  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUT = os.path.join(ROOT, 'docs', 'proofs', 'cmap2_0912v')

GRAB = ("(fmt) => { const g=document.querySelector('#screen-area canvas')||document.querySelector('#screen')"
        "||document.querySelector('canvas'); if(!g) return null;"
        " return fmt==='jpg' ? g.toDataURL('image/jpeg',0.9) : g.toDataURL('image/png'); }")

SETUP = r"""
() => {
  ASSETS.ready = true;
  run.mode = 'campaign'; run.pilot = 'cole';
  campaign.unlockedMax = 8; campaign.rank = {1:'S', 2:'A', 3:'B'}; campaign.bonusUnlocked = 0;
  window.__keys = {};
  const g = XART.get;
  XART.get = function(k){ window.__keys[k] = (window.__keys[k]||0) + 1; return g.apply(this, arguments); };
  window.__warm = cmap2Keys().slice();
  for (let st=1; st<=8; st++) for (const v of ['_lock','_av','_done','_hi0','_hi1']) window.__warm.push('nss_flag'+st+v);
  for (let st=1; st<=8; st++) window.__warm.push('nss_panel_'+st);
  for (let i=0;i<8;i++) window.__warm.push('nss_cursor_'+i);
  window.__warm.push('ship_cole', 'dlg_window');
  cmap2Warm();
  window.__warm.forEach(k => { try{ XART.rdy(k); }catch(e){} });
  return {on: cmap2On(), keys: cmap2Keys().length};
}
"""

STATE = r"""
() => {
  const w = (typeof sselCursor!=='undefined') ? cmap2World(sselCursor) : null;
  const sc = w ? cmap2ToScreen(w.x, w.y) : null;
  return {state: String(state), boot: sselBoot, bootT: sselBootT, cursor: sselCursor,
          focus: cmap2.focus, bar: cmap2.bar, cam: {x: cmap2.cam.x, y: cmap2.cam.y, z: cmap2.cam.z},
          selScreen: sc, pause: campPause ? {mode: campPause.mode, bar: !!campPause.bar, sel: campPause.sel} : null,
          toast: cmap2.toastT > 0 ? cmap2.toast : '', flash: !!_selFlash, zoom: !!sselZoom,
          cine: sselUnlockCine ? {stage: sselUnlockCine.stage, phase: sselUnlockCine.phase} : null,
          s9: s9MapCine ? s9MapCine.ph : null, bonus: campaign.bonusUnlocked|0,
          unlockedMax: campaign.unlockedMax, committed: !!window.sselCommitted, err: cmap2._err|0};
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tour', action='store_true')
    ap.add_argument('--out', default=OUT)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(ROOT)
    url = 'http://127.0.0.1:%d/index.html' % port
    errs, results = [], []

    def ok(cond, name, detail=''):
        results.append((bool(cond), name, detail))
        print(('  ok   ' if cond else '  FAIL ') + name + ('   [' + str(detail) + ']' if detail != '' else ''))

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:220]) if m.type == 'error' else None)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(sh.TRAP_RAF)
        pg.wait_for_timeout(50)

        s = pg.evaluate(SETUP)
        ok(s['on'], 'the map in pieces is registered and on', s)
        # rdy() is false on its first call - poll it against real time, not a frame count
        pg.wait_for_function("() => window.__warm.every(k => XART.rdy(k))", timeout=60000, polling=200)
        ok(True, 'every piece, flag, panel and cursor decoded', len(pg.evaluate("() => window.__warm")))

        def step(n, chunk=30):
            while n > 0:
                k = min(chunk, n)
                e = pg.evaluate(sh.STEP, k)
                if e:
                    errs.append('STEP threw: ' + e)
                    return
                pg.wait_for_timeout(15)
                n -= k

        def shot(name, fmt='png'):
            d = pg.evaluate(GRAB, fmt)
            path = os.path.join(args.out, name + ('.jpg' if fmt == 'jpg' else '.png'))
            open(path, 'wb').write(base64.b64decode(d.split(',', 1)[1]))
            return path

        def st():
            return pg.evaluate(STATE)

        def tap(k):
            pg.evaluate("(k) => Input.injectTap(k)", k)

        # ================= BOOT =================
        pg.evaluate("() => { window.__keys={}; openStageSelect(3,{boot:true}); }")
        step(int(2.3 * 60)); shot('01_boot_overview')
        a = st()
        ok(a['boot'] > 0 and a['cam']['z'] < 0.7, 'the boot frames the WHOLE world', a['cam'])
        step(int(1.8 * 60)); shot('02_boot_bar_lands')
        step(int(1.0 * 60)); shot('03_boot_flags_drop')
        step(int(1.6 * 60)); shot('04_boot_retina')
        for _ in range(20):
            if st()['boot'] == 0:
                break
            step(30)
        a = st()
        ok(a['boot'] == 0 and a['state'] == 'stagesel', 'the boot sequence completes and hands over', a['boot'])
        step(int(2.0 * 60)); shot('05_live_stage3')
        a = st()
        ok(abs(a['cam']['z'] - 1) < 0.01, 'the camera settles at the live zoom', round(a['cam']['z'], 4))
        k = pg.evaluate("() => window.__keys")
        ok(k.get('cm2_ocean', 0) > 0 and k.get('cm2_bar', 0) > 0, 'the ocean and the bar are drawn from their plates',
           (k.get('cm2_ocean', 0), k.get('cm2_bar', 0)))
        drawn_isl = [i for i in ['1', '2', '3', '4', '5', '6', '7', '8', 'hub'] if k.get('cm2_isl_' + i, 0) > 0]
        ok(len(drawn_isl) == 9, 'all eight stage islands and the citadel draw in colour when unlocked', drawn_isl)
        ok(k.get('cm2_isl_9_lock', 0) > 0 and k.get('cm2_isl_9', 0) == 0, 'the unearned portal draws in its slate lock bake',
           (k.get('cm2_isl_9_lock', 0), k.get('cm2_isl_9', 0)))
        ok(any(k.get('cm2_cloud_%d' % i, 0) > 0 for i in range(7)), 'clouds drift over the map')
        ok(any(kk.startswith('nss_flag') for kk in k), 'the flags stand on the islands')

        # ================= LEFT / RIGHT: STAGE TO STAGE =================
        want = pg.evaluate("() => sselMoveHorizontal(1,1,8,sselCursor)")
        cam0 = st()['cam']
        tap('d'); step(3)
        a = st()
        ok(a['cursor'] == want, 'RIGHT moves the cursor to the stage physically to the right', (a['cursor'], want))
        step(int(1.4 * 60)); shot('06_right_to_stage%d' % a['cursor'])
        a = st()
        tw = pg.evaluate("(s) => cmap2Clamp(cmap2World(s), 1)", a['cursor'])
        ok(abs(a['cam']['x'] - tw['x']) < 12 and abs(a['cam']['y'] - tw['y']) < 12 and (abs(a['cam']['x'] - cam0['x']) > 20 or abs(a['cam']['y'] - cam0['y']) > 20),
           'and the camera flies there', {'cam': a['cam'], 'target': tw})
        want = pg.evaluate("() => sselMoveHorizontal(-1,1,8,sselCursor)")
        tap('a'); step(3)
        ok(st()['cursor'] == want, 'LEFT moves back the other way', (st()['cursor'], want))
        step(int(1.2 * 60))

        # ================= UP: THE BAR =================
        tap('w'); step(3)
        a = st()
        ok(a['focus'] == 'bar', 'UP climbs to the button bar', a['focus'])
        c0 = a['cursor']
        tap('d'); step(3)
        a = st()
        ok(a['bar'] == 1 and a['cursor'] == c0, 'on the bar RIGHT walks button to button and the map cursor does not move',
           (a['bar'], a['cursor'], c0))
        step(20); shot('07_bar_focus_load')
        tap('j'); step(3)
        ok(st()['flash'], 'FIRE on a button strobes it white (Phoenix rule)')
        step(40); shot('08_dropdown_load')
        a = st()
        ok(a['pause'] and a['pause']['bar'] and a['pause']['mode'] == 'load', 'LOAD unrolls its slot drop-down from the bar', a['pause'])
        c1 = st()['cursor']
        tap('d'); tap('s'); step(3)
        a = st()
        ok(a['pause']['sel'] == 1 and a['cursor'] == c1, 'the drop-down owns UP/DOWN and the map cannot move under it',
           (a['pause']['sel'], a['cursor'], c1))
        tap('k'); step(3)
        a = st()
        ok(a['pause'] is None and a['focus'] == 'bar', 'BACK closes the drop-down and leaves you on the bar', (a['pause'], a['focus']))
        tap('d'); step(3); tap('j'); step(45); shot('09_dropdown_exit')
        a = st()
        ok(a['pause'] and a['pause']['mode'] == 'exit' and a['pause']['sel'] == 1,
           'EXIT asks first, with STAY highlighted', a['pause'])
        tap('k'); step(3)
        tap('s'); step(3)
        ok(st()['focus'] == 'map', 'DOWN comes back to the map', st()['focus'])
        tap('p'); step(3)            # 0917d: Start is P / the controller's START; Enter is confirm on the map
        ok(st()['focus'] == 'bar', 'Start climbs to the bar too', st()['focus'])
        tap('p'); step(3)
        ok(st()['focus'] == 'map', 'and Start again comes back down', st()['focus'])
        tap('w'); step(3); tap('k'); step(3)
        ok(st()['focus'] == 'map', 'BACK also comes down off the bar', st()['focus'])

        # ================= SAVE =================
        pg.evaluate("() => { try{ localStorage.removeItem(campSlotKey(1)); }catch(e){} }")
        tap('w'); step(3)
        # the bar WRAPS, so walk by reading it rather than by counting presses from a remembered index
        for _ in range(3):
            if st()['bar'] == 0:
                break
            tap('a'); step(2)
        ok(st()['bar'] == 0 and st()['state'] == 'stagesel', 'LEFT walks back to SAVE', st()['bar'])
        tap('j'); step(40); tap('s'); step(3); tap('j'); step(40)
        a = st()
        saved = pg.evaluate("() => { const s=campReadSlot(1); return s ? {stage:s.stage, v:s.v} : null; }")
        ok(saved is not None and a['pause'] is None, 'SAVE writes the chosen slot (slot 2) and closes', (saved, a['pause']))
        ok(a['toast'] == 'SAVED TO SLOT 2', 'and the receipt names the slot that was written (0810p)', a['toast'])
        shot('10_saved_toast')
        tap('s'); step(3)

        # ================= MOUSE =================
        rect = pg.evaluate("() => cmap2BtnRects()[2]")
        pg.evaluate("(r) => { Input.mouse.x=r.x+r.w/2; Input.mouse.y=r.y+r.h/2; Input.mouse.moved=true; }", rect)
        step(2)
        a = st()
        ok(a['focus'] == 'bar' and a['bar'] == 2, 'pointing at a button selects it', (a['focus'], a['bar']))
        w3 = pg.evaluate("() => { const w=cmap2World(sselCursor); return cmap2ToScreen(w.x, w.y+30); }")
        pg.evaluate("(q) => { Input.mouse.x=q.x; Input.mouse.y=q.y; Input.mouse.moved=true; }", w3)
        step(2)
        ok(st()['focus'] == 'map', 'pointing at an island hands the focus back to the map', st()['focus'])
        pg.evaluate("(r) => { Input.mouse.x=r.x+r.w/2; Input.mouse.y=r.y+r.h/2; Input.mouse.moved=true; Input.mouse.down=true; }", rect)
        step(2)
        pg.evaluate("() => { Input.mouse.down=false; }")
        step(40)
        a = st()
        ok(a['pause'] and a['pause']['mode'] == 'exit', 'a click on EXIT opens its confirm', a['pause'])
        tap('k'); step(3); tap('s'); step(3)
        pg.evaluate("() => { Input.mouse.x=-50; Input.mouse.y=-50; }")

        # ================= DEPLOY =================
        pg.evaluate("() => { window.__dep=null; window.__bs=beginStage; beginStage=function(n){ window.__dep=n; }; }")
        cur = st()['cursor']
        scr = pg.evaluate("() => sselFlagScreenXY(sselCursor)")
        tap('j'); step(30)
        zc = pg.evaluate("() => sselZoom ? {x:sselZoom.x, y:sselZoom.y} : null")
        ok(zc is not None and abs(zc['x'] - scr['x']) < 3 and abs(zc['y'] - scr['y']) < 3,
           'FIRE deploys, and the deploy zoom centres on the flag in SCREEN space', {'zoom': zc, 'flag': scr})
        step(40); shot('11_deploy_zoom')
        step(120)
        ok(pg.evaluate("() => window.__dep") == cur, 'and hands over to the chosen stage', (pg.evaluate("() => window.__dep"), cur))
        pg.evaluate("() => { beginStage=window.__bs; window.sselCommitted=false; _selFlash=null; sselZoom=null; }")

        # ================= UNLOCK CINEMATIC =================
        pg.evaluate("() => { campaign.unlockedMax=4; campaign.rank={1:'S',2:'A',3:'B',4:'B'}; openStageSelect(5,{unlock:5}); }")
        step(int(0.9 * 60)); shot('12_unlock_zoomin')
        for _ in range(30):
            if (st()['cine'] or {}).get('phase') == 'ding':
                break
            step(6)
        a = st()
        tw = pg.evaluate("(z) => cmap2Clamp(cmap2World(5), z)", a['cam']['z'])
        ok(a['cine'] and a['cine']['phase'] == 'ding' and a['cam']['z'] > 1.1, 'the unlock pushes in on the new island', a['cam'])
        ok(abs(a['cam']['x'] - tw['x']) < 25 and abs(a['cam']['y'] - tw['y']) < 25, 'on stage 5, not the parked cursor', {'cam': a['cam'], 'target': tw})
        shot('13_unlock_ding')
        step(int(1.2 * 60)); shot('14_unlock_unfurl')
        for _ in range(40):
            if st()['cine'] is None:
                break
            step(10)
        ok(st()['cine'] is None and st()['unlockedMax'] == 5 and st()['cursor'] == 5, 'and lands with stage 5 unlocked and selected',
           (st()['unlockedMax'], st()['cursor']))

        # ================= THE SECRET =================
        pg.evaluate("() => { campaign.unlockedMax=8; window.__keys={}; openStageSelect(5,{bonusUnlock:true}); }")
        step(int(0.8 * 60)); shot('15_bonus_fly')
        for _ in range(40):
            if st()['s9'] == 'flash':
                break
            step(6)
        step(30); shot('16_bonus_flash')
        fr = pg.evaluate("() => ({p9: sselFlagScreenXY(9), p5: sselFlagScreenXY(5), top: CM2_BAND_TOP, bot: CM2_BAND_BOT})")
        ok(fr['p9']['y'] > fr['top'] and fr['p5']['y'] < fr['bot'] and 0 < fr['p9']['x'] < 480 and 0 < fr['p5']['x'] < 480,
           'the secret frames BOTH nodes in the open sea - the portal clear of the bar, stage 5 clear of the card', fr)
        k = pg.evaluate("() => window.__keys")
        ok(k.get('cm2_isl_9', 0) > 0, 'the portal island comes up in colour as the secret unlocks', k.get('cm2_isl_9', 0))
        for _ in range(40):
            if st()['s9'] is None:
                break
            step(10)
        step(60); shot('17_bonus_live')
        a = st()
        ok(a['bonus'] == 1 and a['cursor'] == 9, 'the secret is earned and selected', (a['bonus'], a['cursor']))
        pg.evaluate("() => { campaign.bonusUnlocked=0; }")

        ok(st()['err'] == 0, 'the map drew without a single swallowed throw', st()['err'])

        # ================= TOUR (video) =================
        if args.tour:
            import tempfile
            tdir = os.path.join(tempfile.gettempdir(), 'bof_cmap2_tour')     # frames are scratch, not proofs
            os.makedirs(tdir, exist_ok=True)
            for f in os.listdir(tdir):
                os.remove(os.path.join(tdir, f))
            pg.evaluate("() => { campaign.unlockedMax=8; campaign.bonusUnlocked=0; cmap2.bar=0; openStageSelect(1,{boot:true}); }")
            n = [0]

            def frames(sec):
                for _ in range(int(sec * 30)):
                    step(2, 2)
                    d = pg.evaluate(GRAB, 'jpg')
                    open(os.path.join(tdir, 'f_%05d.jpg' % n[0]), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                    n[0] += 1
            frames(9.4)          # the boot, all of it
            frames(1.2)
            for key in ['d', 'd', 'd', 'a', 'a', 'a', 'a']:
                tap(key); frames(1.25)
            tap('w'); frames(0.8)             # up to the bar, on SAVE
            tap('d'); frames(0.6)             # LOAD
            tap('d'); frames(0.6)             # EXIT
            tap('j'); frames(1.4)             # EXIT's confirm, STAY lit
            tap('k'); frames(0.5)
            tap('a'); frames(0.5)             # back to LOAD
            tap('j'); frames(1.4)             # the slot drop-down
            tap('k'); frames(0.4)
            tap('s'); frames(1.2)             # down to the map
            print('tour frames:', n[0])
            import subprocess, imageio_ffmpeg
            mp4 = os.path.join(tdir, 'cmap2_tour_0912v.mp4')
            subprocess.check_call([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-framerate', '30',
                                   '-i', os.path.join(tdir, 'f_%05d.jpg'), '-vf', 'scale=720:-2', '-c:v', 'libx264',
                                   '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', mp4])
            print('video -> %s (%.1f MB)' % (mp4, os.path.getsize(mp4) / 1e6))

        b.close()
    stop()

    fails = [r for r in results if not r[0]]
    print('\n%d ok / %d fail' % (len(results) - len(fails), len(fails)))
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:12]:
            print('   ', e)
    json.dump({'results': results, 'errors': errs}, open(os.path.join(args.out, 'probe_result.json'), 'w'), indent=1)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
