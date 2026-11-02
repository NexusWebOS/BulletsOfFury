#!/usr/bin/env python3
"""capture_storyboard_1102.py - storyboard of the game's dialogue with the real frame for every line.
Cinematic scenes come from the game's own script catalog (BOF_STORYBOARD.catalog) and each line is rendered through
the Storyroom preview path (BOF_STORYBOARD.preview, the editor's Shot button): the frame is grabbed once that line's
artwork has loaded and its text has finished typing. In-game radio conversations (Chronos arrival on the Stage 5 boss,
the Stage 6 opening radio) are captured from the live fights. Real Chromium, TRAP_RAF stepping.
Writes docs/previews/storyboard_1102/frames/*.jpg and storyboard.json.
  python _BUILD_SOURCE/capture_storyboard_1102.py [--pilot cole] [--only id,id]
"""
import os, sys, json, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image
A = sys.argv
PILOT = A[A.index('--pilot') + 1] if '--pilot' in A else 'cole'
ONLY = A[A.index('--only') + 1].split(',') if '--only' in A else None
OUT = os.path.join(os.path.dirname(HERE), 'docs', 'previews', 'storyboard_1102')
FR = os.path.join(OUT, 'frames')

def grab(pg, name):
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB')
    im.thumbnail((400, 400)); im.save(os.path.join(FR, name), quality=78); return name

STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 160); } }
  return {state: String(state), line: typeof hqLine !== 'undefined' ? hqLine : null, chars: typeof hqChars !== 'undefined' ? hqChars : null,
          len: (typeof hqSc !== 'undefined' && hqSc && hqSc.beats && hqSc.beats[hqLine]) ? String(hqSc.beats[hqLine].text || '').length : null, err: window.__err || null}; }"""

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(FR, exist_ok=True)
    port, stop = sh.serve(sh.GAME); board = {'pilot': PILOT, 'scenes': []}; errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio']); pg = b.new_page(viewport={'width': 1280, 'height': 900})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate("(pk) => { ASSETS.ready = true; window.__now = performance.now(); const i = PILOTS.findIndex(p => p.key === pk); if (i >= 0) pilotIndex = i; run.pilot = pk; return true; }", PILOT)
        cat = pg.evaluate("(pk) => BOF_STORYBOARD.catalog(pk).map(s => ({id: s.id, title: s.title, group: s.group, kind: s.kind, beats: s.beats.map(b => ({who: b.who || '', text: b.text || '', art: BOF_STORYBOARD.art(b, pk) || null, duration: b.duration || null}))}))", PILOT)
        for sc in cat:
            if ONLY and sc['id'] not in ONLY: continue
            rows = []
            for i, beat in enumerate(sc['beats']):
                pg.evaluate("(c) => { window.__err = null; const s = BOF_STORYBOARD.catalog(c.pk).find(x => x.id === c.id); const cards = s.beats.map((b, k) => ({source: k, enabled: true, fields: {}, edited: []}));"
                            " BOF_STORYBOARD.preview(c.id, c.pk, cards, c.i, true); return true; }", {'pk': PILOT, 'id': sc['id'], 'i': i})
                art = beat['art']
                PRE = "(c) => { window.__err = null; const s = BOF_STORYBOARD.catalog(c.pk).find(x => x.id === c.id); const cards = s.beats.map((b, k) => ({source: k, enabled: true, fields: {}, edited: []})); BOF_STORYBOARD.preview(c.id, c.pk, cards, c.i, true); return true; }"
                # let the line's artwork decode (real time) and its text type out (game time)
                n = 0; settled = None
                for k in range(90):
                    r = pg.evaluate(STEP, 6); n += 6; pg.wait_for_timeout(15)
                    ready = pg.evaluate("(k) => !k || XART.rdy(k)", art)
                    if r['state'] == 'title': break
                    if sc['kind'] in ('director', 'action', 'monologue'):
                        if r['line'] not in (0, None): break
                        if ready and r['len'] is not None and r['chars'] is not None and r['chars'] >= r['len'] and k > 6:
                            settled = n; break
                    elif ready and k >= (4 if sc['kind'] == 'narration' else 24): settled = n; break
                if settled is not None:
                    r = pg.evaluate(STEP, 24)
                if settled is None or r['state'] == 'title' or (sc['kind'] in ('director', 'action', 'monologue') and r['line'] not in (0, None)):
                    # the line ended before the hold: replay it and grab just before its end
                    back = max(6, (settled or n) - 12)
                    pg.evaluate(PRE, {'pk': PILOT, 'id': sc['id'], 'i': i})
                    for k in range(40):
                        if pg.evaluate("(k) => !k || XART.rdy(k)", art): break
                        pg.wait_for_timeout(50)
                    pg.evaluate(STEP, back)
                name = '%s_%02d.jpg' % (sc['id'], i)
                grab(pg, name)
                rows.append({**beat, 'frame': 'frames/' + name})
            board['scenes'].append({'id': sc['id'], 'title': sc['title'], 'group': sc['group'], 'kind': sc['kind'], 'beats': rows})
            print('%-22s %2d lines' % (sc['id'], len(rows)), flush=True)
        pg.evaluate("() => { try { BOF_STORYBOARD.stop(); } catch (e) {} return true; }")
        # ---- in-game: Chronos arrival radio (Stage 5 boss, live) ----
        if not ONLY or 'ingame-chronos' in ONLY:
            pg.evaluate("(pk) => { diffKey = 'normal'; DIFF = DIFFS.normal; run.mode = 'campaign'; startRun(5); run.mode = 'campaign'; curStage = STAGES[4]; beginStage(5); setState(GS.PLAY); player.reset();"
                        " try { BOFCinematicDirector.cancel(); } catch (e) {} playerHit = function(){}; debugJump({stage: 5, role: 'boss'}); return true; }", PILOT)
            seen, rows = set(), []
            for k in range(600):
                pg.evaluate(STEP, 6); pg.wait_for_timeout(5)
                st = pg.evaluate("() => { const F = typeof fb2Intro !== 'undefined' && fb2Intro; if (!F || !F.lines) return null; const L = F.lines[F.i]; return L ? {i: F.i, who: L.who, text: L.text, shown: F.shown, len: String(L.text || '').length, done: F.done} : {done: true}; }")
                if st and st.get('done') and rows: break
                if st and 'i' in st and st['i'] not in seen and st['shown'] >= st['len'] - 1:
                    seen.add(st['i']); name = 'ingame-chronos_%02d.jpg' % st['i']; grab(pg, name); rows.append({'who': st['who'], 'text': st['text'], 'art': None, 'frame': 'frames/' + name})
            board['scenes'].append({'id': 'ingame-chronos', 'title': 'Stage 5 - Chronos arrival (in-game radio)', 'group': 'In-game', 'kind': 'radio', 'beats': rows})
            print('ingame-chronos         %2d lines' % len(rows), flush=True)
        # ---- in-game: Stage 6 opening radio (live) ----
        if not ONLY or 'ingame-stage6' in ONLY:
            pg.evaluate("(pk) => { diffKey = 'normal'; DIFF = DIFFS.hard; diffKey = 'hard'; run.mode = 'campaign'; startRun(6); run.mode = 'campaign'; curStage = STAGES[5]; beginStage(6); setState(GS.PLAY); player.reset();"
                        " try { BOFCinematicDirector.cancel(); storySkip(); } catch (e) {} playerHit = function(){}; return true; }", PILOT)
            seen, rows = set(), []
            for k in range(500):
                pg.evaluate(STEP, 6); pg.wait_for_timeout(5)
                st = pg.evaluate("() => { const O = typeof s6Opening !== 'undefined' && s6Opening; if (!O) return null; const R = O.radio; return {idx: O.radioIndex, phase: O.phase, who: R && (R.who || R.name), text: R && (R.full || R.text || R.line), t: O.allT}; }")
                if not st:
                    if rows: break
                    continue
                if st['idx'] and st['idx'] not in seen and st.get('text'):
                    pg.evaluate(STEP, 50); seen.add(st['idx']); name = 'ingame-stage6_%02d.jpg' % st['idx']; grab(pg, name)
                    rows.append({'who': st['who'] or '', 'text': st['text'] or '', 'art': None, 'frame': 'frames/' + name})
                if st['idx'] is not None and st['idx'] >= 5 and len(rows) >= 5: break
            board['scenes'].append({'id': 'ingame-stage6', 'title': 'Stage 6 - opening radio (in-game)', 'group': 'In-game', 'kind': 'radio', 'beats': rows})
            print('ingame-stage6          %2d lines' % len(rows), flush=True)
        b.close()
    stop()
    path = os.path.join(OUT, 'storyboard.json')
    if ONLY and os.path.exists(path):
        old = json.load(open(path, encoding='utf-8')); keep = {s['id']: s for s in old['scenes']}
        for s in board['scenes']: keep[s['id']] = s
        board['scenes'] = list(keep.values())
    json.dump(board, open(path, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('scenes', len(board['scenes']), 'lines', sum(len(s['beats']) for s in board['scenes']), 'page errors', errs[:3])

if __name__ == '__main__':
    main()
