"""Publish a local review from completed native evidence; never invent results."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_1003'
report=json.loads((O/'verification.json').read_text(encoding='utf-8'))
suite=(O/'full-suite.log').read_text(encoding='utf-8')
report['baseline']={'assertions':6287,'failing_names':[]}
report['suite']={'assertions':sum(x.startswith('  ok') for x in suite.splitlines()),'failing_names':[x.strip() for x in suite.splitlines() if x.startswith('  FAIL')],'final_banner':'FALVA/LIZZIE BUILD OK, 0 ERRORS' in suite}
assert report['suite']['final_banner'] and not report['suite']['failing_names'],'Suite is incomplete or failing'
assert not report['errors'] and all(c['ok'] for c in report['checks']),'Native checks need repair'
(R/'docs/qa/stage8_1003.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
scenes=[('Full-height binary guard','binary-wall-normal'),('Bullet impact','shield-impact'),('Shield shatter','shield-shatter'),('Fragments flying outward','shield-shards-outward'),('Heavy jump preparation','knight-jumpTell'),('Airborne sword strike','knight-jump'),('Horizontal follow-up','knight-sweep'),('Code teleport','knight-out'),('Gravity unit warning spokes','s8leech-furious-tell'),('Gravity ordnance','s8leech-furious-fire'),('Retina stalker locks its lanes','s8hunter-hard-tell'),('Paired alien lasers','s8hunter-hard-fire'),('Code prism targeting','s8solar-hard-tell'),('Code prism release','s8solar-hard-fire'),('Host code laser warning','boss-code-lance-warning'),('Host code laser release','boss-code-lance-live'),('Colossus-sized binary wall','colossus-full-wall'),('Transformation reel','form-transformation')]
cards=''.join(f'<figure><img loading="lazy" src="{name}.png" alt="{html.escape(title)}"><figcaption>{html.escape(title)}</figcaption></figure>' for title,name in scenes)
assets=''.join(f'<details><summary>{n.title()} sheet</summary><img loading="lazy" src="../../assets/game/levels/stage_08/stage/stage8_1003/{n}.png" alt="{n} generated sheet"></details>' for n in ['knight','wall','impact','shatter','shards','teleport','morph','gravity','stalker','prism','beams','fov'])
checks=len(report['checks']);tests=report['suite']['assertions']
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Stage 8 · Code Knight</title>
<style>body{{margin:0;background:#080e17;color:#e8f5ff;font:16px/1.55 system-ui}}main{{max-width:1200px;margin:auto;padding:40px 26px}}h1{{font-size:clamp(32px,5vw,60px);line-height:1.05;margin:8px 0 20px}}p{{max-width:900px;color:#b9cdd9}}.eyebrow{{color:#50f7ed;letter-spacing:.2em;font-size:12px}}.status{{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}}.status span{{padding:9px 14px;background:#132736;border:1px solid #27576b;border-radius:7px}}video{{width:100%;max-height:720px;background:#020508;border:1px solid #284958}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}figure{{margin:0;background:#101e2b;border:1px solid #243b4e;border-radius:8px;overflow:hidden}}figure img{{width:100%;display:block}}figcaption{{padding:12px 16px;font-weight:650}}a{{color:#6df9e7}}details{{margin:12px 0;border:1px solid #284552;padding:16px;border-radius:7px}}details img{{display:block;max-width:100%;max-height:900px;margin:20px auto;background:#142330}}summary{{cursor:pointer}}h2{{margin-top:40px}}.note{{font-size:14px;color:#8da8bc}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}</style>
<main><div class="eyebrow">BULLETS OF FURY / OCTOBER 3</div><h1>The code fights back.</h1>
<p>Generated knight combat poses, a growing binary wall, directional shield shatter, code teleports and transformations. Three new alien silhouettes enter on existing Stage 8 wave beats with stable hulls, orbital routes and committed laser warnings.</p>
<div class="status"><span>100 generated animation frames + 4 shard crops</span><span>{tests:,} assertions · zero failures</span><span>{checks} Chromium checks · zero browser errors</span></div>
<video controls playsinline preload="metadata" poster="knight-sweep.png" src="knight-combo.webm"></video>
<p class="note">Silent capture of the real game canvas: controlled Hard encounter and alien-unit fixtures with the player protected for inspection. This is not a campaign win or final balance certification.</p>
<p><a href="../../index.html?build=stage8-code-knight-1003">Open current game</a> · <a href="verification.json">Native evidence</a> · <a href="../../docs/qa/stage8_1003.json">Suite comparison</a></p>
<h2>Combat and shield break</h2><div class="grid">{cards}</div><h2>Generated art</h2>{assets}
<p class="note">Built-in image generation. Source originals, exact prompts and crop metadata are preserved in the repository. No SpriteCook or shared-atlas replacement.</p></main></html>'''
(O/'review.html').write_text(page,encoding='utf-8')
print(json.dumps({'assertions':tests,'native_checks':checks,'failing_names':report['suite']['failing_names'],'review':str(O/'review.html')}))
