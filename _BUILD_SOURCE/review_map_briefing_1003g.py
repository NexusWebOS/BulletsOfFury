"""Build the local visual review from native game captures."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'_shots/map_briefing_1003g'
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Campaign briefing & Lizzie — October 3</title>
<style>*{box-sizing:border-box}body{margin:0;background:#070f1c;color:#e1ebf6;font:16px/1.55 system-ui,sans-serif}main{max-width:1380px;margin:auto;padding:36px 24px}h1{color:#ffe4a0;font-size:clamp(25px,4vw,42px);margin:0}h2{color:#ffe4a0;font-size:23px;margin:30px 0 10px}p{max-width:880px}a{color:#8bd8ff}video,img{display:block;width:100%;max-height:84vh;object-fit:contain;background:#030810;border:1px solid #2f4560;border-radius:8px}.grid{display:grid;grid-template-columns:2fr 1fr;gap:22px}.tag{display:inline-block;border:1px solid #526379;padding:5px 12px;border-radius:20px;margin:12px 7px 0 0;font-size:13px}.note{color:#a4b6cd;font-size:14px}figure{margin:0}figcaption{color:#abc0da;padding:8px 0}@media(max-width:760px){.grid{grid-template-columns:1fr}main{padding:22px 14px}}</style>
<main><h1>Pick a theater. Read the mission.</h1>
<p>Theater Progression now sits above the mission briefing. A freshly generated blank frame holds centered game lettering that reveals one character at a time on every selection.</p>
<span class="tag">Live game fonts</span><span class="tag">Stable typewriter layout</span><span class="tag">Complete Lizzie frame</span>
<p><a href="/index.html?build=map-briefing-1003g">Open the updated game</a></p>
<h2>Mission selection in motion</h2><video controls muted loop playsinline preload="metadata" src="map-motion.webm" poster="desktop.png"></video>
<p class="note">Captured from the actual game renderer, selecting consecutive missions. Original stage copy and full current titles are rendered as live text.</p>
<h2>Lizzie’s steady comms portrait</h2><video controls muted loop playsinline preload="metadata" src="lizzie-motion.webm" poster="lizzie_dialogue.png"></video>
<p class="note">Her original portrait pixels remain. A complete generated bezel stays fixed while only the mouth animates. The enlarged portrait is a review close-up of the same logical game asset.</p>
<img src="lizzie_poses.png" alt="Lizzie idle and four talking poses, showing the same complete frame in menu and communication directions">
<h2>Desktop and narrow screens</h2><div class="grid"><figure><img src="desktop.png" alt="Theater progression centered immediately above the mission briefing"><figcaption>Progression, mission copy, and original action prompts share one layout.</figcaption></figure><figure><img src="narrow.png" alt="Narrow campaign map without stretching or duplicate control prompts"><figcaption>Portrait screens retain the correct proportions and one prompt row.</figcaption></figure></div>
<h2>Stage X keeps its own briefing</h2><img src="stage_x.png" alt="Stage X mission title and rival briefing inside the new blank frame">
<p class="note">Native checks cover character-by-character reveal, stable centering, all nine stage descriptions, Stage X, both Lizzie portrait directions, and narrow layout. Existing campaign regression verifies island clicks and the bonus portal. No browser errors in completed passes.</p>
</main></html>'''
(O/'review.html').write_text(html,encoding='utf-8')
print(O/'review.html')
