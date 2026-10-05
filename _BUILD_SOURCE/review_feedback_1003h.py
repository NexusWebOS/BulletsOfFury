"""Build a small local review from actual Chromium screenshots and recordings."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'_shots/feedback_1003h'
cards=[('stealth-bombers','Stage 6 stealth bomber palette roles'),('team-cole','Cole: timed, protected team briefing'),
 ('rebel-voss','Voss'),('rebel-nyx','Nyx'),('rebel-rook','Rook'),('rebel-kaia','Kaia'),('rebel-jace','Jace'),
 ('rebel-pitch-0','Complete rebel silhouettes: pitch 1'),('rebel-pitch-3','Complete rebel silhouettes: pitch 4'),
 ('hammer-avatar','Cronos: matching portrait'),('hammer-face','Closeup'),('hammer-turn','Turn'),('hammer-shock','Shock'),
 ('hammer-explosion','Animated destruction'),('earth-descent','Current Furyship returns to Earth')]
html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bullets of Fury · Homecoming</title><style>
*{box-sizing:border-box}body{margin:0;background:#070c16;color:#e8f2ff;font:16px/1.6 system-ui}main{max-width:1320px;margin:auto;padding:38px 28px 90px}h1{font-size:38px;line-height:1.15;margin:8px 0}h2{margin-top:42px}p{color:#acbfd7}a{color:#78d6ff}video{width:100%;display:block;background:#000;border:1px solid #2e4564;border-radius:8px}.label{color:#73d3ff;letter-spacing:.13em;font-size:12px;text-transform:uppercase}.row{display:grid;grid-template-columns:1fr 1fr;gap:24px}.row video{max-height:690px}.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}figure{margin:0;background:#111c2c;padding:8px;border:1px solid #26364e;border-radius:8px}figure img{display:block;width:100%;image-rendering:pixelated}figcaption{font-size:13px;padding:8px;color:#b9cfe8}@media(max-width:800px){.row,.gallery{grid-template-columns:1fr}main{padding:20px}h1{font-size:30px}}</style>
<main><div class="label">Bullets of Fury · October 3</div><h1>Hammer down. Welcome home.</h1>
<p>The final explosion, held completely still as color drains to monochrome. The current Furyship stays intact.</p>
<video controls autoplay muted loop playsinline poster="../../assets/game/feedback_1003h/orbital_aftermath.png" src="../../assets/game/feedback_1003h/orbital-aftermath-monochrome.webm"></video>
<p><a href="../../assets/game/feedback_1003h/orbital-aftermath-monochrome.webm" download>Download the fade animation</a> · <a href="../../assets/game/feedback_1003h/orbital_aftermath.png" download>Full-color still</a></p>
<div class="row"><section><h2>The complete homecoming</h2><p>Orbital missile strike, Earth view, face/turn/shock, destruction, monochrome hold, crew welcome, slowing descent and fade.</p><video controls preload="metadata" poster="orbital-overhead.png" src="hammer-homecoming.webm"></video></section>
<section><h2>Rebel introductions</h2><p>All five pilots have their own portrait boxes. The sequence is timed; combat and weapon use resume after the final line.</p><video controls preload="metadata" poster="rebel-voss.png" src="rebel-introductions.webm"></video></section></div>
<h2>In-game checks</h2><p>Captured from the running game in Chromium. Furious chromium armor is 25% lower; the regular body and move set remain intact.</p><div class="gallery">'''
html+=''.join(f'<figure><a href="{name}.png"><img loading="lazy" src="{name}.png" alt="{label}"></a><figcaption>{label}</figcaption></figure>' for name,label in cards)
html+='</div><p><a href="report.json">Native verification report</a> · <a href="../../_ART_SOURCES/feedback_1003h/generation.json">Generated art and exact prompts</a></p></main>'
(O/'review.html').write_text(html,encoding='utf-8');print(O/'review.html')
