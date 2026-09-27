"""Build Mike's local overnight review from actual Chromium captures."""
from pathlib import Path
import html,json
OUT=Path('_shots/overnight_0927')
report=json.loads((OUT/'review/report.json').read_text(encoding='utf-8'))
for c in report['clips']:c['folder']='review'
if (OUT/'late-review/report.json').exists():
 late=json.loads((OUT/'late-review/report.json').read_text(encoding='utf-8'))
 for c in late['clips']:c['folder']='late-review'
 report['clips']+=late['clips']
titles={
 'furnace-core':('Stage 2 • Furnace core','Exposed body phase with repeated charge, beam and impact cues.'),
 'furnace-detached-head':('Stage 2 • Detached Furnace head','The final head phase, with its live attack warnings and effects.'),
 'tidal-sentinels':('Stage 9 • Paired Sentinels','Furious opening attack lanes before fusion.'),
 'toxic-shield':('Stage 7 • Weakened core shield','Legs removed for inspection; ordinary shots trigger defensive toxic volleys.'),
 'razorback-reference':('Stage 1 • Razorback reference','Opening attacks and the baseline miniboss rhythm.'),
 'helicopter-reference':('Stage 1 • Helicopter reference','Furious attack pacing and the scrolling battlefield.'),
 'furnace-head':('Stage 2 • Furnace Tyrant','Opening armor and eye-beam warnings with current game audio.'),
 'frost-nuclear':('Stage 3 • Frost Cruiser','One arrival, a neutral opening, the nuclear strike and alternating elemental forms.'),
 'cryo-nuclear':('Stage 3 • Cryo Spear','The same authored boss survives the strike and changes forms without a second entrance.'),
 'olive-warden':('Stage 4 • Olive Warden','Alternating helper fire and marked attack lanes at normal game scale.'),
 'caustic-tank':('Stage 7 • Caustic Siege Tank','Solid-floor movement boundaries, rotating turrets and toxic attacks.'),
 'toxic-legged':('Stage 7 • Portal Warden','Legged opening, approach, landing retinas and toxic ordnance.'),
 'magma-furious':('Stage 2 • Charred Inferno Reaver','Black palette and the Furious attack book; paired warnings and rounds originate at the moving turrets.'),
 'magma-normal':('Stage 2 • Magma Ward','Committed bursts, crossing fire, ground warnings and charged lances.'),
 'rival-crew':('Rival Fight! • Two allied pilots','Five independent missile targets; allied rolls and somersaults respect their recharge timers.'),
 'sovereign-helpers':('Stage 4 • Helpers and generators','Accessible generator columns, world-bounded helper hulls, and a warning sign below the shield gauge.'),
 'tempest-normal':('Stage 6 • Tempest and support','Compact HUD radio, committed charge and offscreen-return warnings; allies target the miniboss and recharge their weapons.'),
 'toxic-core-laser':('Stage 7 • Exposed laser','One moving faceplate reveals the generated emitter; the warning matches its sweeping laser.'),
 'toxic-core-guns':('Stage 7 • Surviving cannons','Both muzzle warning lanes match their actual turrets.'),
 'horizon-audio':('Stage 9 • Horizon','Committed lanes and repeated attack audio.'),
 'hammer-ball':('Stage 5 • Spiked ball','Ball attack retained before the low-health cannon transition.'),
 'hammer-chromium':('Stage 5 • Chromium','Fast Furious eruptions; each warning clears when its spike rises.'),
 'sovereign-framing':('Stage 4 • Sovereign','Normal game scale, reachable generator columns, and shield warnings clear of the gauge.'),
 'harrier-launch':('Stage 6 • Harrier','Bay fighters grow and launch north, then turn into formation.'),
 'eclipse-bomber':('Stage 5 • Eclipse Siege Bomber','Modular engines and cannons, rear bombs, forward beam and lane missiles.'),
 'stage8-fleet':('Stage 8 • Fleet','Spaced volleys and lower simultaneous ship pressure.'),
 'vile-cannons':('Stage 8 • Cannon form','Longer beam tells and eased recovery between attack positions.'),
 'tidal-fusion':('Stage 9 • Fusion','Sentinels converge and the combined hull appears at the same world position.'),
 'vile-final-forms':('Stage 8 • Final forms','World-anchored ghost walls, phantom strikes, knight and duplicates.')}
cards=[]
order=['razorback-reference','helicopter-reference','magma-normal','magma-furious','furnace-head','furnace-core','furnace-detached-head','frost-nuclear','cryo-nuclear','olive-warden','sovereign-framing','sovereign-helpers','eclipse-bomber','hammer-ball','hammer-chromium','tempest-normal','harrier-launch','rival-crew','caustic-tank','toxic-legged','toxic-shield','toxic-core-guns','toxic-core-laser','stage8-fleet','vile-cannons','vile-final-forms','horizon-audio','tidal-sentinels','tidal-fusion']
report['clips'].sort(key=lambda c:order.index(c['name']))
links=[]
for c in report['clips']:
 name=c['name'];title,desc=titles[name];folder=c['folder']
 if name in ['razorback-reference','magma-normal','frost-nuclear','olive-warden','eclipse-bomber','tempest-normal','caustic-tank','stage8-fleet','horizon-audio']:
  links.append(f'<a href="#{name}">{html.escape(title.split(" • ")[0])}</a>')
 cards.append(f'''<article id="{name}"><h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p>
 <video controls preload="metadata" poster="{folder}/{name}-1.png" src="{folder}/{name}.webm"></video>
 <footer>{c['diff'].title()} · {c['seconds']} seconds · captured game audio</footer></article>''')
sounds=['missile_auto_1','missile_auto_3','boss_charge','hammer_slam','stun','beam','toxic','ice','alien','cannon','module_break','energy_release','servo_charge','plasma_orb']
audio=''.join(f'<div><b>{s.replace("_"," ").title()}</b><audio controls preload="none" src="../../assets/game/sfx_0927/{s}.mp3"></audio></div>' for s in sounds)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Bullets of Fury • Overnight review</title>
<style>*{box-sizing:border-box}body{margin:0;background:#080d14;color:#e5edf7;font:16px/1.5 system-ui}main{max-width:1240px;margin:auto;padding:36px 24px}h1{color:#ffcc68;font-size:34px;margin:0}h2{font-size:22px;margin:0 0 8px}p{color:#b4c5d8;margin:8px 0 18px}.note{border-left:4px solid #efa637;padding:12px 18px;background:#17212d;margin:24px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:22px}article{padding:20px;background:#101c29;border:1px solid #29415b;border-radius:9px}video{display:block;width:100%;max-height:610px;background:#000}footer{font-size:14px;color:#9ab3cf;padding-top:12px}.audio{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px}.audio>div{background:#101c29;padding:15px;border-radius:6px}audio{width:100%;margin-top:10px}a{color:#86d8ff}section{margin:36px 0}img{width:100%;object-fit:contain}.facts{display:flex;flex-wrap:wrap;gap:12px}.facts span{padding:10px 16px;background:#152537;border-radius:5px}</style>
<main><h1>Bullets of Fury</h1><p>September 27 • Overnight gameplay and audio review</p>
<div class="note">These are real Chromium recordings. Boss clips use damage immunity and selected starting phases to inspect attacks; they are not campaign victories. The fleet clip uses ordinary firing with immunity. Music is muted in these clips so the new effects can be heard.</div>
<div class="facts"><span>Stage 4 zoom stays 1×</span><span>Unselected map regions do not flash</span><span>Space missiles damage targets without Retina</span><span>14 mastered sound effects</span></div>
<nav class="facts" aria-label="Jump to stage">'''+ ' · '.join(links)+'''</nav><section class="grid">'''+''.join(cards)+'''</section><section><h2>Sound audition</h2><p>ElevenLabs sources layered and mastered with the ColeForge SFX engine. In-game volume and overlapping sounds differ from solo playback.</p><div class="audio">'''+audio+'''</div></section>
<section><h2>Combat radio</h2><p>Chatter stays in the reserved bottom HUD, pages without dropping words, and pauses for an active special.</p><div class="grid"><article><img src="radio/page-one.png" alt="Compact radio page"><p>Two readable lines and the pilot portrait.</p></article><article><img src="radio/special-priority.png" alt="Special ability has HUD priority"><p>Active special takes the bay; the message waits.</p></article></div></section><section><h2>New ammunition animation</h2><p>Six generated ice families for Stage 3 and six military families for Stage 4. These frame sheets are captured through the game renderer.</p><div class="grid"><article><h2>Stage 3 ice</h2><img src="ice-ordnance/all-frames.png" alt="24 generated ice projectile frames in the game renderer"></article><article><h2>Stage 4 ordnance</h2><img src="ordnance/all-frames.png" alt="24 generated military projectile frames in the game renderer"></article></div></section><section><h2>Armory and earlier encounter changes</h2><p><a href="../overhaul_0927b/armory-final.png">Open the generated Armory collection screen</a> · <a href="../../docs/VIDEO_REVIEW_0927.md">Video findings and verification limits</a></p></section>
<section><h2>What still needs a player pass</h2><p>Tempest attack overlap, Hammer counters after spending defensive moves, the Warden destruction sequence after losing weapon tiers, and final-form clone/portal decisions remain balance priorities. Physical 8BitDo hardware has not been verified.</p><p><a href="../../docs/qa/BOSS_DIFFICULTY_REVIEW_0927.md">Read the Normal / Hard / Furious encounter recommendations</a></p></section><p>Local working build. Nothing committed or pushed.</p></main></html>'''
(OUT/'review.html').write_text(page,encoding='utf-8')
print(OUT/'review.html')
