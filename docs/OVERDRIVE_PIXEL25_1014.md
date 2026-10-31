# Overdrive Pixel25 — stages 3 and 7, 2026-10-14

Build **overdrive1014-pixel25-r1**. Local preview on port8781. This is the first integrated
PixelLab enemy/environment/HUD pass for the existing expansion, not a new campaign.

Four original robot weapon classes: rifle, minigun heavy, rocket, and laser.
All four receive a16-frame forward walk,13-frame firing/crouch/falling banks,
and eight static directions. Rifle/heavy also have four-direction walk/fire,
16-frame sidesteps; rifle has a17-frame vault. Total475 character images,
including32 static views and443 action drawings in31 action banks. Shared256x256
RGBA cells, physical root128,224, binary alpha, one translation per bank,
fixed per-class scale, no per-frame fitting. Walk/strafe drop the service's
duplicated reference frame before looping. Actual selected source frames and
exports have transparent edge margins. Review at native scale and with onion
overlay: `expansion/topdown/art/pixel25/preview.html`.

Stage3 replaces only the ordinary rifle/heavy troops with PixelLab designs.
Locomotion follows their existing movement phase; live barrel sockets own flash
and projectile origin. New falling drawings remain after the actor is removed.
Stage7 uses all four classes, firing timers follow the selected bank, stable
body bounds exclude attack effects, and death stays visible through the fall.
Existing AI, weapon cadence/damage and encounter sequencing are retained.
Gosfer, Yuri, Helios and the reactor retain their authored identities/animation
banks. This pass does not claim new PixelLab boss or player animation.

Nine separately generated128x128 components: steel side wall, floor, ceiling,
rear bulkhead, closed/open door, courtyard concrete, brick and server panel.
The room remains actual Three.js corridor geometry with2D actor flats.
Door art is composed into a128x184 plate and its plane keeps that aspect ratio.
Stage3's800x2400 footprint is assembled from the separate components without
moving collision geometry. The selected earlier cores, turrets, cover, barrels
and crates remain. Nearest filtering, no mipmaps/antialiasing; Cover24 lighting
and camera -> Yuri -> cover -> enemies ordering remain correct.

Four generated UI panels (top, bottom, boss, dialogue) are extracted and9-sliced
into the existing exact dimensions and anchors. Dynamic text, stats, portraits,
controller prompts, password menu, music23 cue timing and cover controls remain.

Generated oversized/clipped attack effects were rejected, with clean recoil
clips generated instead. Heavy east firing mirrors its reviewed west recoil
clip; the other source directions are distinct. The rejected candidates remain
inside raw ZIP provenance but are not selected in the manifest. Small contained
rifle/heavy south firing accents remain; real projectiles use the game pipeline.

All raw ZIPs, component PNGs, prompts, job/character IDs and SHA256 hashes are
retained in `art/pixel25/source`. Owner: `_research/build_pixel25.py` rebuilds
from those retained sources; optional `--input-dir` performs initial import.
Manifest has504 keys /492 unique PNGs /63 banks including idle views.
PixelLab used212 included subscription generations total for this pass,
1788 remained after completion, no cash credits used.

Automatic approval review rejected uploading existing private artwork to
PixelLab. No original game art was uploaded; this pass used text descriptions
and references created entirely inside PixelLab. Original820 PNG hashes match.

## Verification

Native graphics/game/viewer:28/28. Synthetic raw M30 mapping:24/24.
All475 character images decoded and drew nonempty native pixels. Actual hit
flash pixels and timer expiry verified in stages3/7. Projectile origin verified
in unobstructed real stage3 combat. No browser/shader/asset errors.

Normal-difficulty input-only full stage7 clears: mouse135.933s,
D-pad Retina139.400s. Both33kills,2damage,0deaths, all8cores,
7room transitions and both boss forms. No health/kill/phase writes in those routes.
These are automated ordinary-input routes, not physical controller/human tests.
Stage3 uses native fixtures rather than a full ordinary-input playthrough.
Base suite completed BUILD OK /0ERRORS /exit0; JavaScript syntax checks passed.
Evidence: `docs/qa/overdrive_pixel25_1014.json`, `docs/qa/pixel25_views`.
Probes: `_research/probe_pixel25.py`, `probe_pixel25_m30.py`,
`probe_pixel25_route.py`, `probe_pixel25_controller.py`.

Local only. No assets/game.js change, commit or push. Preserve all other work.
