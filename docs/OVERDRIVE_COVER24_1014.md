# Cover24 — Yuri on our side of the wall, readable gritty lighting

Local build `overdrive1014-cover24-r1`, October 14, 2026.

The old camera occlusion checks proved the wrong layout: the barrier was
closer to the camera than Yuri, leaving his head on the enemy side of a dark
strip. **The intended combat layout is camera → Yuri → cover → enemies/door.**
Keep Yuri visible on our side while he crouches against the wall. Do not
restore the old requirement that the foreground wall hide his entire sprite.

The solid cover now sits at the floor depth for logical y410, ahead of Yuri's
y448 footing, with its intact lip at y336. Its front uses the exact authored
grille artwork cropped to a texture face; thin 3D sides/caps retain shading.
This replaces the oversized dark box and disconnected lower decal. The baked
front artwork retains its original shading/color through a basic material;
the cap/sides remain lit. Damage lowers the lip to y360/y384; destruction
removes that section's body and leaves its existing rubble. All texture
sampling remains nearest with no mipmaps or antialiasing.

Combat draws the cover before Yuri, then near-side attackers/projectiles.
During the hop, Yuri crosses to the far side midway and the layer order
switches; real camera traversal still takes the wall past us into the black
passage and the next room. Initial asset readiness checks include cover
textures, and the fallback render cannot composite an uninitialized GPU pass.

Yuri waits and sidesteps in automatic cover while idle. Fire raises him in
about seven ticks; release settles him back. A short tap queues exactly one
shot for up to 220ms through that rise, cancelled by cutscene input locks.
Hold Cover + Fire for blindfire, Retina for exposed free aim, and B + a side
for immediate side fire. Broken cover cannot automatically protect him.
The existing crouch, prone, fire and blindfire banks are retained. Standing
raises the visual root 18px and blindfire 40px; gun sockets/flashes use the
same root offset. Briefings, rolls, death/revive and traversal keep their
existing roots. No enemy stats, projectile damage or authored PNGs changed.

The room retains Lambert lighting and crisp shadows. Ambient 1.30, hemisphere
0.65 and spotlight 85, plus neutral surface tints, keep authored dark textures
readable. Native screenshot regions measured 2.44×/2.18× luminance on left/right
walls and 2.25× on the floor/front-edge region. These are local image samples,
not a claim of a uniform exposure multiplier. Reactor/Helios and muzzle lights
remain active. Music23's supplied recordings and cue timings are retained.

29 native visual/keyboard checks and 24 synthetic raw M30 checks passed with
zero browser/shader/media/asset errors. Native pixels prove Yuri is visible on
our side, while projected crouch-head and firing-gun positions straddle the
wall lip correctly. Real incoming bullets are blocked in resting cover. All
820 existing PNG hashes match. The M30 test allows the new short rise before
asserting emitted rifle shots; no physical controller presses were performed.

Normal full eight-room input-only routes: mouse 138.750s,
D-pad Retina 136.967s; 2/1 damage,
zero deaths, 33 kills each, all cores/transitions and both boss forms. No health
writes or kill/phase shortcuts in those routes. Required base suite completed
BUILD OK / 0 ERRORS / exit0; module syntax checks passed.

Runtime: `js/lighting22.js`, `js/grid21_renderer.js`, `js/prism_bastion_1013.js`.
Probes: `_research/probe_cover24.py`, `probe_cover24_m30.py`,
`probe_cover24_route.py`, `probe_cover24_controller.py`.
Evidence: `docs/qa/overdrive_cover24_1014.json`, `docs/qa/cover24_views`.
No new graphics, assets/game.js edit, commit or push. Preserve other local work.
