#!/usr/bin/env python3
"""build_storyboard_page_1102.py - turns docs/previews/storyboard_1102/storyboard.json + frames into one self-contained
storyboard page (frames embedded), docs/previews/storyboard_1102/index.html."""
import os, json, base64, html
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(os.path.dirname(HERE), 'docs', 'previews', 'storyboard_1102')
B = json.load(open(os.path.join(D, 'storyboard.json'), encoding='utf-8'))

ACTS = [
 ('opening', 'Act I', 'Opening', ['opening', 'opening-finale']),
 ('between', 'Act II', 'Between levels', ['post-%d' % i for i in range(1, 10)]),
 ('ingame', 'Act III', 'In-game scenes', ['ingame-chronos', 'cronos', 'hammer-trap1002', 'ingame-stage6', 'route-left', 'route-right', 'rebel-contact',
                                          'stage-x-voss', 'stage-x-nyx', 'stage-x-rook', 'stage-x-kaia', 'stage-x-jace', 'stage7-approach']),
 ('finale', 'Act IV', 'Finale', ['dracodia-monologue', 'dracodia-rebirth', 'dracodia-transform', 'dracodia-defeat', 'ending']),
]
WHERE = {
 'opening': 'New campaign, before the map. Fury HQ history, the invasion, the satellite takeover and the pilot already airborne.',
 'opening-finale': 'End of the opening, as the logo fly-off hands over to the campaign map.',
 'post-1': 'After the Stage 1 results screen (dam destroyed), before the map.', 'post-2': 'After the Stage 2 results screen (Furnace Tyrant).',
 'post-3': 'After the Stage 3 results screen (ice relay).', 'post-4': 'After the Stage 4 results screen (airbase and power cell).',
 'post-5': 'After the Stage 5 results screen (Chronos defeated, return from orbit).', 'post-6': 'After Stage 6, as the squad comes home and the Stage 7 descent is briefed.',
 'post-7': 'After the Stage 7 portal closes.', 'post-8': 'After Stage 8.', 'post-9': 'After the Stage 9 bonus detour, back to the map.',
 'ingame-chronos': 'Live during the Stage 5 boss arrival, in the side radio while the fight is on screen.',
 'cronos': 'Stage 5, first contact with Chronos.', 'hammer-trap1002': 'Stage 5, when Chronos reveals the trap.',
 'ingame-stage6': 'Live at the start of Stage 6, in the radio while the stealth fighters attack.',
 'route-left': 'Stage 6 route choice: the Harrier carrier.', 'route-right': 'Stage 6 route choice: the Rebel squad.',
 'rebel-contact': 'Stage 6 Rebel route, first contact with the squad.',
 'stage-x-voss': 'Stage X, Voss duel.', 'stage-x-nyx': 'Stage X, Nyx duel.', 'stage-x-rook': 'Stage X, Rook duel.', 'stage-x-kaia': 'Stage X, Kaia duel.', 'stage-x-jace': 'Stage X, Jace duel.',
 'stage7-approach': 'Before Stage 7, the river descent under the city.',
 'dracodia-monologue': 'Stage 8, Dracodia speaks before the final fight.', 'dracodia-rebirth': 'Stage 8, the pilot reacts when Dracodia is reborn.',
 'dracodia-transform': 'Stage 8, the pilot reacts to the transformation.', 'dracodia-defeat': 'Stage 8, final blow.',
 'ending': 'After Dracodia falls: the invasion ending.',
}
scenes = {s['id']: s for s in B['scenes']}
# These lines play over the live encounter in the game; their frames come from the Storyroom rehearsal backdrop.
REHEARSAL = {'rebel-contact', 'stage-x-voss', 'stage-x-nyx', 'stage-x-rook', 'stage-x-kaia', 'stage-x-jace', 'dracodia-monologue', 'dracodia-rebirth', 'dracodia-transform', 'dracodia-defeat'}
def img(path):
    p = os.path.join(D, path)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode() if os.path.exists(p) else ''
nav, body, sc_no, total = [], [], 0, 0
for key, label, name, ids in ACTS:
    present = [i for i in ids if i in scenes and scenes[i]['beats']]
    if not present: continue
    nav.append('<a href="#%s"><span>%s</span>%s</a>' % (key, label, html.escape(name)))
    body.append('<section class="act" id="%s"><header class="act-head"><p class="eyebrow">%s</p><h2>%s</h2><p class="count">%d scenes</p></header>' % (key, label, html.escape(name), len(present)))
    for sid in present:
        s = scenes[sid]; sc_no += 1
        body.append('<article class="scene" id="%s"><div class="scene-head"><p class="slate">SC %02d</p><div><h3>%s</h3><p class="where">%s</p></div><p class="shots">%d shots</p></div><div class="panels">' % (
            html.escape(sid), sc_no, html.escape(s['title'].replace('—', '-')), html.escape(WHERE.get(sid, '') + (' Frames are the Storyroom rehearsal; in the game these lines play over the live fight.' if sid in REHEARSAL else '')), len(s['beats'])))
        for i, bt in enumerate(s['beats']):
            total += 1
            who = html.escape(bt.get('who') or '')
            body.append('<figure class="panel"><div class="frame"><img loading="lazy" alt="SC %02d shot %d: %s" src="%s"><span class="tag">SC %02d &middot; SH %02d</span></div>'
                        '<figcaption>%s<p class="line">%s</p>%s</figcaption></figure>' % (
                sc_no, i + 1, who or 'scene', img(bt['frame']), sc_no, i + 1,
                ('<p class="who">%s</p>' % who) if who else '<p class="who quiet">No speaker</p>', html.escape(bt.get('text') or ''),
                ('<p class="art">%s</p>' % html.escape(bt['art'])) if bt.get('art') else ''))
        body.append('</div></article>')
    body.append('</section>')

pilot = B.get('pilot', 'cole').upper()
page = '''<title>Bullets of Fury Storyboard</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Silkscreen&family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a production storyboard sheet - act bands, slated scenes, numbered panels of real game frames. Single dark theme on purpose (it matches the game's cutscene windows). */
:root{--ink:#0b0f17;--sheet:#121826;--panel:#182033;--rule:#26314a;--text:#e7ecf6;--muted:#93a0bb;--accent:#ff9a3c;--accent2:#5cc8ff;
--display:"Silkscreen","Chakra Petch",ui-monospace,monospace;--head:"Chakra Petch","Barlow",system-ui,sans-serif;--body:"Barlow",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace;color-scheme:dark}
body{background:var(--ink);color:var(--text);font:15px/1.5 var(--body)}
.wrap{max-width:1360px;margin:0 auto;padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.top{display:grid;gap:14px;padding-bottom:22px;border-bottom:1px solid var(--rule)}
.top h1{font:400 clamp(26px,4.4vw,44px)/1.05 var(--display);letter-spacing:.02em;margin:0;color:var(--accent);text-wrap:balance}
.top p{margin:0;color:var(--muted);max-width:72ch}
.meta{display:flex;flex-wrap:wrap;gap:8px 18px;font:500 12px/1.4 var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.meta b{color:var(--text);font-weight:500}
nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--ink);display:flex;flex-wrap:wrap;gap:6px;padding-block:12px;border-bottom:1px solid var(--rule)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--ink)}
nav a{color:var(--text);text-decoration:none;font:600 13px/1 var(--head);padding:8px 12px;border:1px solid var(--rule);border-radius:4px;display:flex;gap:8px;align-items:center}
nav a span{font:400 11px/1 var(--display);color:var(--accent2)}
nav a:hover,nav a:focus-visible{border-color:var(--accent);outline:none}
.act{padding-top:34px}
.act-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;margin-bottom:8px}
.eyebrow{margin:0;font:400 13px/1 var(--display);color:var(--accent2);letter-spacing:.08em}
.act-head h2{margin:0;font:700 clamp(22px,3vw,30px)/1.1 var(--head);text-wrap:balance}
.count{margin:0;font:500 12px/1 var(--mono);color:var(--muted)}
.scene{margin-top:22px;background:var(--sheet);border:1px solid var(--rule);border-radius:6px;padding:16px}
.scene-head{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:start;margin-bottom:14px}
.slate{margin:0;font:400 14px/1 var(--display);background:var(--accent);color:var(--ink);padding:8px 9px;border-radius:3px}
.scene-head h3{margin:0;font:700 19px/1.2 var(--head);text-wrap:balance}
.where{margin:4px 0 0;color:var(--muted);font-size:14px;max-width:80ch}
.shots{margin:0;font:500 12px/1.6 var(--mono);color:var(--muted);white-space:nowrap}
.panels{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.panel{margin:0;background:var(--panel);border:1px solid var(--rule);border-radius:4px;overflow:hidden;display:flex;flex-direction:column}
.frame{position:relative;background:#000;aspect-ratio:480/337;display:flex;align-items:center;justify-content:center}
.frame img{width:100%%;height:100%%;object-fit:contain;image-rendering:pixelated;display:block}
.tag{position:absolute;left:6px;top:6px;font:500 10px/1 var(--mono);background:rgba(11,15,23,.82);color:var(--text);padding:4px 6px;border-radius:3px;letter-spacing:.04em}
figcaption{padding:10px 12px 12px;display:grid;gap:4px;min-width:0}
.who{margin:0;font:600 12px/1.2 var(--head);color:var(--accent);text-transform:uppercase;letter-spacing:.06em}
.who.quiet{color:var(--muted)}
.line{margin:0;font-size:14px;line-height:1.45;overflow-wrap:anywhere}
.art{margin:2px 0 0;font:400 11px/1.3 var(--mono);color:var(--muted);overflow-wrap:anywhere}
footer{margin-top:40px;color:var(--muted);font-size:13px;max-width:80ch}
@media (max-width:560px){.scene-head{grid-template-columns:auto minmax(0,1fr)}.shots{grid-column:2}.panels{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style>
<div class="wrap">
<header class="top"><h1>Bullets of Fury Storyboard</h1>
<p>Every line of dialogue in the campaign, in playing order, with the frame the player sees for it. Frames were rendered by the game itself: cutscenes through the Storyroom preview, the in-game radio scenes from the live Stage 5 and Stage 6 fights.</p>
<div class="meta"><span>Lead pilot <b>%s</b></span><span><b>%d</b> scenes</span><span><b>%d</b> shots</span><span>Other pilots get their own wording in several scenes</span></div></header>
<nav aria-label="Acts">%s</nav>
%s
<footer>Shot labels follow the storyboard convention SC (scene) and SH (shot). The small grey key under a line is the authored art the shot uses. Edit wording and order in the Storyroom (OPEN_STORYBOARD.bat); regenerate this sheet with capture_storyboard_1102.py and build_storyboard_page_1102.py.</footer>
</div>''' % (pilot, sc_no, total, ''.join(nav), ''.join(body))
out = os.path.join(D, 'index.html'); open(out, 'w', encoding='utf-8').write(page)
print('wrote', out, round(os.path.getsize(out) / 1e6, 2), 'MB', sc_no, 'scenes', total, 'shots')
