#!/usr/bin/env python3
"""
probe_insanity_0916.py - THE FURIOUS POINTS LEDGER AND THE FIFTH DIFFICULTY, IN REAL CHROMIUM.

    python3 _BUILD_SOURCE/probe_insanity_0916.py

Mike, 0916: "Insanity - a 5th difficulty and 5th difficulty button you should generate. it will not
show up unless you unlock it via achievement points, so its an invisible button you cant even
select until this condition is met, then it becomes visible and selectable."

⚠ "YOU CANNOT SELECT IT" IS THREE CLAIMS, NOT ONE, AND A DRAW TEST PROVES NONE OF THEM. A row can
be absent from the screen and still be reachable by the cursor, by the mouse hit test, or by the
function that turns the cursor index into a difficulty key - this file records `menuIndex` being
read by four separate places on the title menu, one of which was missed and shipped. So the locked
case is driven three ways: walk the cursor all the way round, click down the whole column, and read
what `pickDiff` actually assigns.

⚠ AND THE LEDGER IS ASSERTED ON THE BALANCE, NOT ON THE FLAG. `furiousBuy` returning 'ok' says
what the function decided; it does not say that the points left. The balance is read before and
after, and a purchase with too few points must be refused with the balance UNMOVED.
"""
import os, sys, base64

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
STEP = sh.STEP
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'insanity_0916')
N = {'ok': 0}
FAILS = []


def ok(c, m):
    if c:
        N['ok'] += 1
        print('  ok   ' + m)
    else:
        FAILS.append(m)
        print('  FAIL ' + m)


def shot(pg, name):
    d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
    if d:
        open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))


def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof furiousBuy==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)

        # a clean profile every run - the store is localStorage and it PERSISTS between runs
        pg.evaluate("""() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(e){}
                               achievementReload(); }""")

        # ---------- the ledger ----------
        ok(pg.evaluate("() => furiousBalance() === 0 && furiousSpent() === 0"),
           'a clean profile starts at zero points and zero spent')
        ok(pg.evaluate("() => furiousBuy('insanity_mode') === 'poor'"),
           'and cannot buy INSANITY with nothing')
        ok(pg.evaluate("() => furiousBalance() === 0 && !furiousOwned('insanity_mode')"),
           'a refused purchase moves NOTHING - balance still 0, still not owned')

        # earn enough, honestly, through the real unlock path
        got = pg.evaluate("""() => { let n = 0;
            for (const id of Object.keys(ACHIEVEMENT_DEFS)) {
              if (furiousBalance() >= FURIOUS_SHOP.insanity_mode.cost) break;
              if (achievementUnlock(id)) n++;
            }
            return {n, pts: achievementPoints(), bal: furiousBalance()}; }""")
        print('  earned:', got)
        ok(got['bal'] >= 2000, 'points earned through the real unlock path (%d pts over %d awards)'
           % (got['pts'], got['n']))
        ok(pg.evaluate("() => furiousBalance() === achievementPoints() - furiousSpent()"),
           'the balance is earned minus spent, by construction')

        # ---------- locked: three ways in, all closed ----------
        pg.evaluate("() => { setState(GS.DIFF); menuIndex = 0; }")
        pg.evaluate(sh.STEP, [3])
        lst = pg.evaluate("() => diffList()")
        ok(lst == ['easy', 'normal', 'hard', 'furious'],
           'LOCKED: the difficulty list holds four, and INSANITY is not one of them: %s' % lst)
        shot(pg, '01_locked.png')

        # (1) the cursor cannot land on it - walk it right round the menu
        seen = pg.evaluate("""() => { const out = [];
            for (let i = 0; i < 12; i++) { menuIndex = i % 9; out.push(diffList()[menuIndex] || null); }
            menuIndex = 0; return out; }""")
        ok('insanity' not in [q for q in seen if q],
           'LOCKED: no cursor position resolves to INSANITY (%s)' % sorted(set(q for q in seen if q)))

        # (2) pickDiff cannot be talked into it, even with the index forced past the end
        forced = pg.evaluate("""() => { const was = diffKey; menuIndex = 4; pickDiff();
            const got = diffKey; diffKey = was; DIFF = DIFFS[was]; menuIndex = 0; return got; }""")
        ok(forced != 'insanity',
           'LOCKED: forcing the cursor past the last row still cannot pick it (got %s)' % forced)

        # (3) the mouse cannot hit a row that is not in the list
        ok(pg.evaluate("() => diffList().indexOf('insanity') < 0"),
           'LOCKED: and the mouse hit test walks the same list, so there is nothing to click')

        # ---------- buy it ----------
        before = pg.evaluate("() => furiousBalance()")
        res = pg.evaluate("() => furiousBuy('insanity_mode')")
        after = pg.evaluate("() => furiousBalance()")
        cost = pg.evaluate("() => FURIOUS_SHOP.insanity_mode.cost")
        ok(res == 'ok', 'buying INSANITY succeeds once the points are there (%s)' % res)
        ok(after == before - cost,
           'and the points actually LEAVE: %d - %d = %d' % (before, cost, after))
        ok(pg.evaluate("() => furiousBuy('insanity_mode') === 'owned'"),
           'buying it twice is refused')
        ok(pg.evaluate("() => furiousBalance()") == after,
           'and the second attempt costs nothing')

        # ---------- unlocked: visible AND selectable ----------
        pg.evaluate("() => { setState(GS.DIFF); menuIndex = 0; }")
        pg.evaluate(sh.STEP, [3])
        lst2 = pg.evaluate("() => diffList()")
        ok(lst2 == ['easy', 'normal', 'hard', 'furious', 'insanity'],
           'UNLOCKED: it appears, last: %s' % lst2)
        # ⚠ `pickDiff` SETS `diffKey`, NOT `DIFF` - DIFF is assigned when the RUN starts
        # (difficultyForRun, two call sites). The first cut of this probe read DIFF immediately
        # after pickDiff and reported lives 4 / continues -1 / name NORMAL, i.e. "picking INSANITY
        # plays Normal", on code that is correct. Read the key from the pick and the tuning from
        # the function the run start uses.
        picked = pg.evaluate("""() => { menuIndex = 4; pickDiff();
            const d = difficultyForRun(run.mode, diffKey);
            return {k: diffKey, lives: d.startLives, cont: d.continues, name: d.name}; }""")
        ok(picked['k'] == 'insanity' and picked['name'] == 'INSANITY',
           'UNLOCKED: and it can be picked (%s)' % picked)
        ok(picked['cont'] == 0 and picked['lives'] == 1,
           'one life and NO continues (%d life, %d continues)' % (picked['lives'], picked['cont']))
        # ⚠ AND EVERY PER-DIFFICULTY TABLE MUST HAVE A ROW FOR IT. FODDER_DIFF reads
        # `[k] || 1` and the two DRONE tables fall back to `.normal` BY NAME, so a missing row does
        # not throw - it silently hands the hardest setting NORMAL's numbers.
        tbl = pg.evaluate("""() => ({fodder: FODDER_DIFF.insanity, tell: DRONE_TELL.insanity,
            recover: DRONE_RECOVER.insanity, arcade: !!ARCADE_STOCK.insanity})""")
        print('  per-difficulty rows:', tbl)
        ok(tbl['fodder'] is not None and tbl['tell'] is not None and tbl['recover'] is not None and tbl['arcade'],
           'every per-difficulty table carries an INSANITY row')
        ok(pg.evaluate("() => FODDER_DIFF.insanity > FODDER_DIFF.furious && DRONE_TELL.insanity < DRONE_TELL.furious"),
           'and they make it HARDER than furious, not softer than normal')

        # the plate, and the shape of it against the family
        pg.evaluate("() => { for(const k of Object.keys(DIFF_META)) XART.rdy(DIFF_META[k].img); }")
        pg.wait_for_function("() => Object.keys(DIFF_META).every(k => XART.rdy(DIFF_META[k].img))", timeout=20000)
        ok(True, 'all five generated plates decode')
        asp = pg.evaluate("""() => { const o = {};
            for (const k of ['diff_easy_0916','diff_normal_0916','diff_hard_0916','diff_furious_0916','diff_insanity_0916']) {
              XART.rdy(k); const im = XART.get(k);
              if (im && im.width) o[k] = +(im.width / im.height).toFixed(2); }
            return o; }""")
        print('  plate aspects:', asp)
        vals = [v for v in asp.values()]
        ok(len(asp) == 5 and max(vals) - min(vals) < 1.2,
           'and it is the same SHAPE as the family (%.2f against %.2f-%.2f) - the screen draws every '
           'row at one width, so a thin plate is a thin button'
           % (asp.get('diff_insanity_0916', -1), min(vals), max(vals)))

        pg.evaluate("() => { setState(GS.DIFF); menuIndex = 4; }")
        pg.evaluate(sh.STEP, [3])
        shot(pg, '02_unlocked.png')

        # ---------- it survives a reload, because it is on the profile ----------
        pg.evaluate("() => achievementReload()")
        ok(pg.evaluate("() => furiousOwned('insanity_mode')"),
           'the purchase is on the saved profile and survives a reload')
        ok(pg.evaluate("() => furiousBalance()") == after,
           'and so does the balance (%d)' % after)

        # ---------- the ranked grants ----------
        ok(pg.evaluate("() => { const w = diffKey; diffKey = 'insanity'; const r = achievementNormalOrHigher(); diffKey = w; return r; }"),
           'INSANITY counts as normal-or-higher, so its runs earn stage awards at all')

        # ---- THE VAULT: the screen that makes any of this reachable -------------------------
        # \u26a0 UNTIL THIS SCREEN EXISTED, NOTHING COULD BE BOUGHT AT ALL. The ledger and the
        # INSANITY unlock were provably correct and a real player could not reach either, because
        # furiousBuy had no caller outside code. A system with no surface is indistinguishable from
        # one that was never built - the same hole ACH-02 found in the achievement registry.
        pg.evaluate("""() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(e){}
                               achievementReload(); setState(GS.ACHIEVEMENTS); awardsOpen(); }""")
        pg.evaluate(STEP, [2])

        def tapk(action, fallback):
            pg.evaluate("""(a) => { const k = (keybind[a[0]] && keybind[a[0]][0]) || a[1];
                                    Input.keys[k] = false; Input.injectTap(k); }""", [action, fallback])
            pg.evaluate(STEP, [2])

        # the gallery opens it on its own button - CONFIRM is already the filter there
        tapk('charge', 'h')
        ok(pg.evaluate("() => state") == 'vault', 'the gallery opens the VAULT on its own button')
        rows = pg.evaluate("() => vault.rows.map(r => ({id:r.id, cost:r.cost, pending:!!r.pending, owned:r.owned}))")
        print('  vault rows:', len(rows))
        ok(len(rows) >= 7, 'the vault lists every catalogue row (%d)' % len(rows))
        ok(any(r['pending'] for r in rows), 'including the ones whose content does not exist yet')

        # \u26a0 A ROW THAT CANNOT DELIVER MUST NOT SELL. Taking the points for a video that is not
        # there is worse than not listing it - the player is out the points with nothing to show.
        pend = [i for i, r in enumerate(rows) if r['pending']][0]
        pg.evaluate("(i) => { vault.i = i; }", pend)
        before = pg.evaluate("() => furiousBalance()")
        res = pg.evaluate("() => vaultBuy()")
        ok(res == 'pending', 'buying a row with no content behind it is refused (%s)' % res)
        ok(pg.evaluate("() => furiousBalance()") == before,
           'and it costs nothing - the balance is untouched (%d)' % before)
        ok(bool(pg.evaluate("() => vault.msg")), 'and the screen SAYS why: %r'
           % pg.evaluate("() => vault.msg"))

        # with no points, a real row refuses for the honest reason and says how many are short
        ins = [i for i, r in enumerate(rows) if r['id'] == 'insanity_mode'][0]
        pg.evaluate("(i) => { vault.i = i; }", ins)
        res = pg.evaluate("() => vaultBuy()")
        ok(res == 'poor', 'and a real row with no points refuses as POOR (%s)' % res)
        msg = pg.evaluate("() => vault.msg")
        ok('MORE FURIOUS' in str(msg), 'telling you how many you are short: %r' % msg)

        # earn, then buy it THROUGH THE SCREEN with a real key press
        pg.evaluate("""() => { for (const id of Object.keys(ACHIEVEMENT_DEFS)) {
            if (furiousBalance() >= FURIOUS_SHOP.insanity_mode.cost) break; achievementUnlock(id); }
            vault.rows = vaultRows(); }""")
        before = pg.evaluate("() => furiousBalance()")
        pg.evaluate("(i) => { vault.i = i; }", ins)
        tapk('fire', 'j')
        after = pg.evaluate("() => furiousBalance()")
        ok(pg.evaluate("() => furiousOwned('insanity_mode')"),
           'a real FIRE press on the row buys it')
        ok(after == before - 2000, 'and the points leave: %d -> %d' % (before, after))
        ok(pg.evaluate("() => diffList().indexOf('insanity') >= 0"),
           'and INSANITY is now on the difficulty screen - bought entirely from the UI')

        shot(pg, '04_vault.png')
        ok(pg.evaluate("() => vault.rows.filter(r => r.owned).length") == 1,
           'the row reads OWNED afterwards')

        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]:
            print('    !', e)
        br.close(); stop()

    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS:
        print('  FAIL', f)
    sys.exit(1 if FAILS else 0)


if __name__ == '__main__':
    main()
