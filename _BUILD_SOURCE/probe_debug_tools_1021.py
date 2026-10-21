#!/usr/bin/env python3
"""probe_debug_tools_1021.py - the 1021 debug toolkit, driven with real keys in real Chromium.

Mike: "can you improve and upgrade my boss mode and debug modes please?"

  ENGINE (index.html?debug=1), every tool pressed on the keyboard:
    F8 HUD (its text reaches the canvas), F9 GOD (a real playerHit is refused, the ship does not
    blink), - / = / 0 speed (the fixed 60 Hz clock runs speed x ticks), [ ] freeze + one-tick step,
    1-4 phase jumps, 5 kill, F10 restart, the debug menu's INSANITY, the result + best time.
    BUSTED ARMS: with GOD off the same playerHit costs a life; at 1.00x the clock runs 1:1.
  EDITOR (bossmode.html): GOD / phase / FREEZE / STEP / RESTART buttons drive the engine, the
    speed slider is no longer undone the next frame, and a finished fight lands in the RUN LOG.

    python3 _BUILD_SOURCE/probe_debug_tools_1021.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs', 'proofs', 'debug_tools_1021'); os.makedirs(OUT, exist_ok=True)
res = {'ok': 0, 'fail': 0, 'fails': [], 'errors': []}
def ok(c, m):
    if c: res['ok'] += 1; print('ok   ' + m, flush=True)
    else: res['fail'] += 1; res['fails'].append(m); print('FAIL ' + m, flush=True)

port, stop = shoot.serve(ROOT)
try:
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--mute-audio', '--autoplay-policy=no-user-gesture-required'])
        # ---------------------------------------------------------------- ENGINE
        pg = br.new_page(viewport={'width': 1100, 'height': 1200})
        pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
        pg.on('pageerror', lambda e: res['errors'].append('pageerror ' + str(e)[:200]))
        pg.on('console', lambda m: m.type == 'error' and res['errors'].append('console ' + m.text[:200]))
        pg.goto(f'http://127.0.0.1:{port}/index.html?debug=1')
        pg.wait_for_function("() => typeof loop==='function' && window.__bofAssetRuntimeReady && window.DBGT && window.BOSSMODE && BOSSMODE.tools", timeout=180000)
        pg.evaluate(shoot.TRAP_RAF)
        J = lambda e: pg.evaluate('() => (' + e + ')')
        def step(n):
            while n > 0:
                k = min(60, n); e = pg.evaluate(shoot.STEP, k)
                if e: ok(False, 'step threw ' + str(e)[:160]); return
                pg.wait_for_timeout(20); n -= k
        def press(key, f=3):
            pg.keyboard.down(key); step(f); pg.keyboard.up(key); step(f)
        pg.evaluate("()=>{ localStorage.removeItem('bof_debug_best_v1'); localStorage.removeItem('bof_debug_last_v1'); localStorage.removeItem('bof_debug_tools_v1'); DBGT.best={}; DBGT.last=null; DBGT.hud=false; DBGT.god=false; }")
        ok(J("['easy','normal','hard','furious','insanity'].every(k=>DIFF_KEYS.includes(k))"), 'DIFF_KEYS carries INSANITY')
        # the debug menu: cycle the difficulty with real keys until INSANITY
        J("(setState(GS.DEBUG), debugMenu.row=-2, diffKey='furious', 1)"); step(4)
        press('ArrowRight')
        ok(J("diffKey") == 'insanity', 'debug menu RIGHT on the difficulty row reaches INSANITY (%s)' % J("diffKey"))
        press('ArrowRight')
        ok(J("diffKey") == 'easy', 'and wraps back to EASY')
        J("(diffKey='normal', 1)")

        # a fight: stage 2 boss
        ok(J("BOSSMODE.start(2,'boss','cole',false,'normal')"), 'BOSSMODE.start stage 2 boss')
        for _ in range(20):
            step(30)
            if J("!!(bossActive&&boss&&!boss.enter&&debugFight&&debugFight.spawned)"): break
        ok(J("!!(bossActive&&boss)"), 'the boss is live')
        J("(playerHit=playerHit, 1)")
        # F8 HUD - wrap the instance fillText and look for the HUD's own words
        press('F8')
        ok(J("DBGT.hud===true"), 'F8 turns the HUD on')
        hud = pg.evaluate("""()=>{ const seen=[]; const f=ctx.fillText; ctx.fillText=function(t){ seen.push(String(t)); return f.apply(this,arguments); };
            window.__bofStepNow+=1000/60; loop(window.__bofStepNow); ctx.fillText=f; return seen.filter(s=>/DPS|SPEED|HITS|EB /.test(s)); }""")
        ok(len(hud) >= 3, 'HUD lines reach the canvas: %s' % hud[:4])
        pg.screenshot(path=os.path.join(OUT, 'hud.png'))
        # F9 GOD vs the busted arm
        lives0 = J("run.lives")
        press('F9'); ok(J("DBGT.god===true"), 'F9 turns GOD on')
        J("(player.invuln=0, run.shield=0, playerHit(), 1)"); step(2)
        ok(J("run.lives") == lives0 and not J("player.dead"), 'GOD refuses a real playerHit (lives %s -> %s)' % (lives0, J("run.lives")))
        ok(J("player.invuln") < 5, 'GOD does not pin the invuln timer (no blinking ship): %s' % J("player.invuln"))
        ok(J("DBGT.stats.godBlocks") >= 1, 'the refusal is counted')
        press('F9'); ok(J("DBGT.god===false"), 'F9 turns GOD off')
        J("(player.invuln=0, run.shield=0, playerHit(), 1)"); step(2)
        ok(J("run.lives") < lives0 or J("player.dead") or J("player.invuln") > 0, 'BUSTED ARM: with GOD off the same hit lands')
        step(240)   # let any respawn settle
        J("(player.invuln=1e9, 1)")
        # SPEED: the fixed combat clock
        def ticks(n=120):
            a = J("BOF_COMBAT_CLOCK.total"); step(n); return J("BOF_COMBAT_CLOCK.total") - a
        press('Digit0'); t1 = ticks()
        press('Minus'); press('Minus'); press('Minus')   # 1.0 -> 0.75 -> 0.5 -> 0.25
        sp = J("DBGT.speed"); tq = ticks()
        ok(abs(sp - 0.25) < 1e-6, 'three - presses step 1.00x down to 0.25x (%s)' % sp)
        ok(abs(t1 - 120) <= 4, 'at 1.00x the clock runs 1:1 (%s ticks / 120 frames)' % t1)
        ok(22 <= tq <= 38, 'at 0.25x it runs a quarter (%s ticks / 120 frames)' % tq)
        press('Equal'); press('Equal'); press('Equal'); press('Equal'); press('Equal'); press('Equal')
        sp = J("DBGT.speed"); t2 = ticks()
        ok(abs(sp - 2.0) < 1e-6 and 225 <= t2 <= 245, '= steps to 2.00x and the clock runs double (%s ticks)' % t2)
        ok(J("timeScale") == 1, 'timeScale is untouched (the old slider fought updatePlay for it)')
        press('Digit0')
        # FREEZE / STEP
        press('BracketLeft'); ok(J("DBGT.frozen===true"), '[ freezes')
        tf = ticks(60); ok(tf == 0, 'frozen: 0 ticks in 60 frames (%s)' % tf)
        a = J("BOF_COMBAT_CLOCK.total"); press('BracketRight'); d = J("BOF_COMBAT_CLOCK.total") - a
        ok(d == 1, '] advances exactly one tick (%s)' % d)
        press('BracketLeft'); ok(J("DBGT.frozen===false") and ticks(30) >= 28, '[ again runs the clock')
        # phase jumps
        press('Digit2'); fr = J("boss.hp/boss.maxhp")
        ok(abs(fr - 0.5) < 0.02, '2 sets the boss to 50%% (%.3f)' % fr)
        press('Digit3'); fr = J("boss.hp/boss.maxhp"); ok(abs(fr - 0.25) < 0.02, '3 sets 25%% (%.3f)' % fr)
        ok(J("DBGT.stats.assisted===true"), 'a jump marks the run assisted')
        # F10 restart
        press('F10'); step(4)
        ok(J("DBGT.stats.t") < 0.2 and not J("DBGT.stats.assisted"), 'F10 restarts with a fresh, unassisted clock')
        for _ in range(20):
            step(30)
            if J("!!(bossActive&&boss&&debugFight&&debugFight.spawned)"): break
        ok(J("boss&&boss.hp/boss.maxhp") > 0.95, 'the restarted boss is back at full HP (%s)' % J("boss&&boss.hp/boss.maxhp"))
        ok(J("DBGT.last && DBGT.last.won===false"), 'the abandoned attempt is recorded as LOST')
        # an unassisted clear (the engine's own death branch, as a real final hit takes it)
        step(120); J("(BOSSMODE.kill(), 1)")
        for _ in range(40):
            step(30)
            if J("state===GS.DEBUG"): break
        ok(J("state===GS.DEBUG"), 'the cleared fight fades back to the DEBUG menu')
        last = J("DBGT.last")
        ok(last and last['won'] and not last['assisted'] and last['newBest'], 'unassisted win records a NEW BEST: %s' % json.dumps(last)[:200])
        ok(J("debugBestLabel(2,'boss')") != '', 'the menu cell shows the best time (%s)' % J("debugBestLabel(2,'boss')"))
        ok(J("JSON.parse(localStorage.getItem('bof_debug_best_v1'))['2:boss:normal']") is not None, 'the best persists in localStorage')
        menu = pg.evaluate("""()=>{ const seen=[]; const f=ctx.fillText; ctx.fillText=function(t){ seen.push(String(t)); return f.apply(this,arguments); };
            window.__bofStepNow+=1000/60; loop(window.__bofStepNow); ctx.fillText=f; return seen.filter(s=>/LAST:|NEW BEST|F9 GOD/.test(s)); }""")
        ok(len(menu) >= 2, 'the menu prints the last result and the toolkit line: %s' % [m[:60] for m in menu])
        pg.screenshot(path=os.path.join(OUT, 'menu.png'))
        # 5 kill marks assisted, so it never becomes a best
        J("BOSSMODE.start(1,'mini','cole',false,'normal')")
        for _ in range(20):
            step(30)
            if J("!!(subBossActive&&subBoss&&debugFight&&debugFight.spawned)"): break
        press('Digit5')
        for _ in range(40):
            step(30)
            if J("state===GS.DEBUG"): break
        last = J("DBGT.last")
        ok(last and last['won'] and last['assisted'] and not last['newBest'], 'a 5-kill clear is ASSISTED and sets no best: %s' % json.dumps(last)[:160])
        pg.close()

        # ---------------------------------------------------------------- EDITOR
        ed = br.new_page(viewport={'width': 1700, 'height': 1000})
        ed.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
        ed.on('pageerror', lambda e: res['errors'].append('editor pageerror ' + str(e)[:200]))
        ed.goto(f'http://127.0.0.1:{port}/bossmode.html')
        ed.wait_for_function("() => { const f=document.getElementById('host'); try{ return f.contentWindow.BOSSMODE && f.contentWindow.BOSSMODE.ready && f.contentWindow.BOSSMODE.tools; }catch(e){ return false; } }", timeout=240000)
        H = lambda e: ed.evaluate("() => { const W=document.getElementById('host').contentWindow; return (" + e + "); }")
        ed.wait_for_timeout(1500)
        H("W.BOSSMODE.start(2,'boss','cole',false,'normal')")
        ed.wait_for_function("() => { const W=document.getElementById('host').contentWindow; const S=W.BOSSMODE.snapshot(); return S.bossActive && S.boss && W.debugFight && W.debugFight.spawned; }", timeout=60000)
        ed.click('#t-invuln'); ed.wait_for_timeout(200)
        ok(H("W.DBGT.god") is True, 'editor GOD button turns engine GOD on')
        ok(ed.evaluate("document.getElementById('t-invuln').classList.contains('on')"), 'and the button shows it')
        ed.click('[data-hpj="0.5"]'); ed.wait_for_timeout(200)
        ok(abs(H("W.BOSSMODE.boss.hp/W.BOSSMODE.boss.maxhp") - 0.5) < 0.03, 'editor 50 button jumps the boss to 50%')
        ed.fill('#t-speed', '0.4'); ed.dispatch_event('#t-speed', 'input'); ed.wait_for_timeout(700)
        ok(abs(H("W.DBGT.speed") - 0.4) < 1e-6, 'the speed slider holds after frames have run (%s)' % H("W.DBGT.speed"))
        ed.click('#t-freeze'); ed.wait_for_timeout(300)
        a = H("W.BOSSMODE.tools.ticks"); ed.wait_for_timeout(500); b = H("W.BOSSMODE.tools.ticks")
        ok(H("W.DBGT.frozen") and a == b, 'FREEZE stops the engine clock (%s -> %s)' % (a, b))
        ed.click('#t-step'); ed.wait_for_timeout(300)
        ok(H("W.BOSSMODE.tools.ticks") == b + 1, 'STEP advances one tick')
        ed.click('#t-freeze'); ed.fill('#t-speed', '1'); ed.dispatch_event('#t-speed', 'input')
        ed.wait_for_timeout(600)
        ok('DPS' in ed.inner_text('#tf-fight'), 'the footer shows live fight stats: %s' % ed.inner_text('#tf-fight'))
        ed.click('#t-restart'); ed.wait_for_timeout(600)
        ok(H("W.DBGT.stats && W.DBGT.stats.t<0.5 && W.DBGT.stats.assisted===true"), 'RESTART gives a fresh clock, still marked assisted while GOD is on')
        ok(H("W.DBGT.last && W.DBGT.last.won===false"), 'the restarted attempt is logged as LOST')
        ed.wait_for_function("() => { const W=document.getElementById('host').contentWindow; const S=W.BOSSMODE.snapshot(); return S.bossActive && S.boss && W.debugFight && W.debugFight.spawned; }", timeout=60000)
        ed.click('#t-invuln'); H("W.BOSSMODE.kill()")
        ed.wait_for_function("() => /WIN/.test((document.querySelector('#runs-list .run')||{}).textContent||'')", timeout=60000)
        ed.click('#tabs .tab[data-tab="clips"]'); ed.wait_for_timeout(300)
        row = ed.inner_text('#runs-list .run')
        ok('WIN' in row and 'BOSS' in row, 'the RUN LOG lists the clear: %s' % row.replace('\n', ' ')[:140])
        ed.screenshot(path=os.path.join(OUT, 'editor_runlog.png'))
        br.close()
finally:
    stop()
ok(not res['errors'], 'no page/console errors (%d) %s' % (len(res['errors']), res['errors'][:3]))
print('%d ok / %d fail' % (res['ok'], res['fail']))
os.makedirs(os.path.join(ROOT, 'docs', 'qa'), exist_ok=True)
open(os.path.join(ROOT, 'docs', 'qa', 'debug_tools_1021.json'), 'w').write(json.dumps(res, indent=1))
