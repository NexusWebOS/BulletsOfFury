# Overdrive Contra34 — enemy import and closer gameplay

Build `overdrive1016-contra34-r1`, local 2026-10-16.

Imported the actual exports from **Create Contra-style enemy sprites**: 2,595 frames in 214 sheets (21.75 MiB). Original PNG bytes, frame rectangles, pivots, provenance and prompts are preserved in art/contra34. No new art was generated or old atlas repacked. The owning import script is _research/build_contra34.py; AssaultArt now accepts sheet rectangles.

Live art usage:
- Corridor: Cobalt rifleman, Ochre minigunner and Jade sniper replace former sideways robots, with eight-pose walking, facing-aware firing, muzzle sockets and body hitboxes.
- Slide chute: Cyan flying alien with fly/fire animation, matching hit bounds and projectile origin. Existing orbit/retreat/return behavior remains.
- Prism Bastion: rifle, heavy, sniper/laser and rocket families use imported identities and front draw/fire animations; new animated corner turrets, door core and physical forward projectiles.
- Helios: whole-body idle/walk/run/lightning/slam/death and generated volley. Glow and encounter behavior remain. Volley origin includes the imported body's display scale.

Front-facing locomotion was not supplied in the export. Door entry, running and vaulting use the corresponding character's authored side walk/run/jump bank at matching body height. Extra shotgun, twin-barrel, roller and flamethrower art is imported but this pass does not add their distinct encounter AI. Troops use the existing defeat explosion rather than fabricated death frames.

Camera: on-foot overhead and side-view play 1.25x; Prism Bastion 1.15x, including Helios. HUD size/position remains fixed. Mouse targeting uses the inverse camera transform and controller Retina stays within the visible field. Nearest-neighbor sampling, no boss zoom-out. Elevator hatch remains above the dialogue box. The overhead Gosfer camera follows Yuri in the closer view.

Verification:
- 23 focused native Chromium checks pass: all imported frames decode; source-bank selection; exact inverse mouse aim in both sections; raw M30 Retina bounds; cover; shootable elevator hatch; visible enemy/boss hit-flash pixels and expiry; gun-tip and scaled boss-hand emission; fixed boss zoom.
- 4 route checks pass: ordinary inputs clear corridor/self-destruct into visible level 4 with zero deaths; stationary cover and peek fire work. No health or encounter changes during that route.
- ColeForge character-animation QA: side walking sequences and onion overlays inspected, followed by native corridor/chute/Bastion/minigunner/Helios/hatch captures.
- All imported frame sizes are even. All 214 sheet hashes match the source exports.
- Required node syntax checks pass. Full test_fl suite exits 0, final BUILD OK / 0 ERRORS.
- A preliminary boss fixture omitted the run origin; the fixture was corrected before the final passing run, with no production workaround.

Evidence: docs/qa/overdrive_contra34_1016.json, overdrive_contra34_route_1016.json, overdrive_contra34_suite_1016.log; screenshots in _shots/contra34.

No commit or push. Unrelated work preserved; assets/game.js was not edited.
