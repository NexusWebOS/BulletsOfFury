#!/usr/bin/env python3
"""probe_hard_progression_1101.py - Hard and Furious must play through Stages 6, 7, 8 and Stage X.
Real Chromium, the real stage-clear exits (computeStageResults + scLeaveStage, cf4LaunchX, the Stage-7 portal handoff),
real frame stepping through the cinematics that follow each clear. For each difficulty:
  CAMPAIGN  5 clear -> no finale, Stage 6 unlocked and starts
            6 clear (Harrier route) -> Stage 7 unlocked, Stage X offered on the opposite (Rebel) route
            Stage X launches from the map, its encounter spawns, its clear returns to the map marked done
            (and the mirror: 6 cleared on the Rebel route offers Stage X on the Harrier route)
            7 starts; 7 clear -> portal handoff into Stage 8, Stage 8 unlocked with its wave plan built
            8 plays: regular enemies spawn
  ARCADE    5 clear -> Stage 6 begins directly; 6 -> 7; 7 -> 8
  plus 12 s of real play in 7, 8 and Stage X with zero page/console errors.
Also re-checks that Easy/Normal are still refused at Stage 6 (the 1101 finale rule). Screens: _shots/hard_progression_1101/.
"""
import os, sys, base64
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'hard_progression_1101')

PREP = r"""() => { ASSETS.ready = true; window.__now = performance.now(); try { localStorage.clear(); } catch (e) {}
  window.__st = () => ({state: String(state), stage: run.stage, mode: run.mode, unlocked: campaign.unlockedMax, finale: state === NF100.state,
    x: campaign.stageX1004 ? {...campaign.stageX1004} : null, gp4X: run._gp4StageX || null, boss: boss ? (boss.kind || boss.type || 'boss') : null,
    plan: (stagePlan || []).length, enemies: enemies.filter(e => !e.dead).length, warp: state === GS.WARPENTRY});
  return true; }"""

START = r"""(c) => { diffKey = c.diff; DIFF = difficultyForRun(c.mode, c.diff); run.mode = c.mode; coopOn = false; NF100.current = null; NF100.resume = null;
  if (c.fresh) { campaign.unlockedMax = c.stage; campaign.rank = {}; campaign.stageX1004 = null; }
  startRun(c.stage); run.mode = c.mode; DIFF = difficultyForRun(c.mode, c.diff); curStage = STAGES[c.stage - 1]; let err = null, refused = false;
  try { beginStage(c.stage); refused = state === NF100.state; if (!refused) { BOFCinematicDirector.cancel(); storySkip(); setState(GS.PLAY); player.reset(); } } catch (e) { err = String(e).slice(0, 200); }
  if (refused) return {...window.__st(), finale: true, err};
  if (c.route) { try { s6WingInit(); s6Wing.route = c.route; } catch (e) { err = String(e).slice(0, 200); } }
  return {...window.__st(), err}; }"""

CLEAR = r"""() => { let err = null; try { setState(GS.STAGECLEAR); computeStageResults(); const R = drawStageClear._res || {bonus: 0, rank: 'A'};
  scLeaveStage(R); } catch (e) { err = String(e).slice(0, 200); } return {...window.__st(), err}; }"""

STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 200); } }
  return {...window.__st(), err: window.__err || null}; }"""

# skip whatever cinematic/story is running after a clear until we land somewhere stable
SETTLE = r"""(n) => { const seen = []; for (let i = 0; i < n; i++) { window.__now += 1000/60;
    try { if (typeof BOFCinematicDirector !== 'undefined' && BOFCinematicDirector.active && BOFCinematicDirector.active()) BOFCinematicDirector.skip && BOFCinematicDirector.skip(); } catch (e) {}
    try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 200); }
    const s = String(state); if (seen[seen.length - 1] !== s) seen.push(s); if (i > 60 && (state === GS.STAGESEL || state === GS.PLAY || state === GS.WARPENTRY || state === GS.INTRO || state === NF100.state)) break; }
  return {...window.__st(), seen, err: window.__err || null}; }"""

LAUNCHX = r"""() => { let ok = false, err = null; try { ok = cf4LaunchX(); } catch (e) { err = String(e).slice(0, 200); } return {...window.__st(), ok, err}; }"""

def shot(pg, name):
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    res, errs = [], []
    def check(name, ok, info=''):
        res.append(bool(ok)); print(('ok   ' if ok else 'FAIL ') + name + ('   ' + str(info)[:300] if (info and not ok) or os.environ.get('V') else ''), flush=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate(PREP)
        E0 = lambda js, arg=None: pg.evaluate(js, arg) if arg is not None else pg.evaluate(js)
        def E(js, arg=None):
            if js is SETTLE:
                seen = []
                for k in range(arg // 20):
                    r = E0(SETTLE, 20)
                    for x in r['seen']:
                        if not seen or seen[-1] != x: seen.append(x)
                    if r['state'] == 'cutscene' or r['state'] == 'stageclear':
                        pg.keyboard.press('Enter')
                    elif k > 2 and r['state'] in ('stagesel', 'play', 'warpentry', 'intro', 'normal-finale-1031'):
                        break
                r['seen'] = seen; return r
            return E0(js, arg)

        for diff in ('hard', 'furious'):
            D = diff.upper()
            # ---- campaign: 5 -> 6
            E(START, {'diff': diff, 'mode': 'campaign', 'stage': 5, 'fresh': True})
            r = E(CLEAR); s = E(SETTLE, 900)
            check('%s campaign: Stage 5 clear continues to Stage 6 (no finale)' % D, not s['finale'] and (s['stage'] == 6 or s['unlocked'] >= 6), (r, s))
            r = E(START, {'diff': diff, 'mode': 'campaign', 'stage': 6, 'route': 'left'})
            check('%s campaign: Stage 6 starts' % D, not r['finale'] and r['stage'] == 6 and not r['err'], r)
            # ---- 6 clear on the Harrier route -> 7 + Stage X (Rebel)
            r = E(CLEAR); s = E(SETTLE, 1500)
            check('%s campaign: Stage 6 clear unlocks Stage 7' % D, s['unlocked'] >= 7 and not s['finale'], s)
            check('%s campaign: Stage X offered on the opposite (Rebel) route' % D, s['x'] and s['x']['route'] == 'right' and not s['x']['done'], s['x'])
            # ---- Stage X
            r = E(LAUNCHX)
            check('%s Stage X launches from the map' % D, r['ok'] and r['gp4X'] == 'right' and r['state'] == 'play', r)
            s = E(STEP, 60 * 12)
            check('%s Stage X: Rebel encounter spawns and plays 12 s' % D, s['boss'] is not None and s['state'] == 'play' and not s['err'], s)
            shot(pg, '%s-stagex.png' % diff)
            r = E(CLEAR); s = E(SETTLE, 900)
            check('%s Stage X clear returns to the map, route marked done' % D, s['x'] and s['x']['done'] and not s['finale'], (r, s))
            # ---- mirror: 6 cleared on the Rebel route offers Stage X on the Harrier route
            E(START, {'diff': diff, 'mode': 'campaign', 'stage': 6, 'route': 'right', 'fresh': True})
            E(CLEAR); s = E(SETTLE, 1500)
            check('%s mirror: Rebel-route clear offers Stage X on the Harrier route' % D, s['x'] and s['x']['route'] == 'left', s['x'])
            r = E(LAUNCHX); s = E(STEP, 60 * 8)
            check('%s mirror Stage X (Harrier) launches and its encounter spawns' % D, r['ok'] and s['boss'] is not None and not s['err'], (r, s))
            # ---- 7 -> 8
            r = E(START, {'diff': diff, 'mode': 'campaign', 'stage': 7})
            check('%s campaign: Stage 7 starts' % D, not r['finale'] and r['stage'] == 7 and not r['err'], r)
            s = E(STEP, 60 * 12)
            check('%s Stage 7 plays 12 s with enemies' % D, s['state'] == 'play' and s['enemies'] > 0 and not s['err'], s)
            shot(pg, '%s-stage7.png' % diff)
            r = E(CLEAR); s = E(STEP, 30)
            check('%s campaign: Stage 7 clear hands off into Stage 8' % D, s['stage'] == 8 and s['unlocked'] >= 8 and not s['finale'], (r, s))
            check('%s Stage 8 wave plan is built' % D, s['plan'] > 0, s)
            r = E(START, {'diff': diff, 'mode': 'campaign', 'stage': 8})
            s = E(STEP, 60 * 12)
            check('%s Stage 8 plays 12 s with enemies' % D, s['stage'] == 8 and s['state'] == 'play' and s['enemies'] > 0 and not s['finale'] and not s['err'], s)
            shot(pg, '%s-stage8.png' % diff)
            # ---- arcade chain
            E(START, {'diff': diff, 'mode': 'arcade', 'stage': 5})
            E(CLEAR); s = E(SETTLE, 900)
            check('%s arcade: Stage 5 clear continues to Stage 6' % D, s['stage'] == 6 and not s['finale'], s)
            E(START, {'diff': diff, 'mode': 'arcade', 'stage': 6, 'route': 'left'})
            E(CLEAR); s = E(SETTLE, 1500)
            if s['state'] == 'stagesel':
                for k in range(40):
                    pg.keyboard.press('Enter'); s = E0(STEP, 20)
                    if s['stage'] == 7 or s['state'] in ('play', 'intro') and s['stage'] != 6: break
                print('     arcade Stage 6 clear went to the map first; after confirming: stage %s state %s' % (s['stage'], s['state']))
            check('%s arcade: Stage 6 clear continues to Stage 7' % D, s['stage'] == 7 and not s['finale'], s)
            E(START, {'diff': diff, 'mode': 'arcade', 'stage': 7})
            E(CLEAR); s = E(SETTLE, 300)
            check('%s arcade: Stage 7 clear continues to Stage 8' % D, s['stage'] == 8 and not s['finale'], s)

        for diff in ('easy', 'normal'):
            r = E(START, {'diff': diff, 'mode': 'campaign', 'stage': 6, 'fresh': True})
            check('%s is still refused at Stage 6' % diff.upper(), r['finale'], r)
        check('no page/console errors', not errs, errs[:6])
        b.close()
    stop()
    print('%d/%d passed' % (sum(res), len(res)))
    sys.exit(0 if all(res) else 1)

if __name__ == '__main__':
    main()
