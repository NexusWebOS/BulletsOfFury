# Yuri31 — slide turns, complete rolls, standing floor fire

Yuri keeps the approved brown mohawk, close beard, sleeved red jacket, shoulder
badge, fitted armor and red-black boots. PixelLab authored the new motion from
the existing Yuri identity. Original art is retained; 145 new exports are added.

- Slide aim uses 15 intermediate drawings per facing and reverses smoothly over
  0.34 seconds. The torso/head/rifle turn while the legs keep their slide travel.
  Pose selection never advances the animation clock. Shots use the current
  authored barrel socket; muzzle flash remains a separate runtime effect.
- The side roll has 24 drawings through push-off, inversion, full shoulder
  rotation, feet planting and recovery. Its complete sequence fits the existing
  half-second movement and five-second cooldown. Jump cannot interrupt it.
  A queued prone finish uses 29 drawings. Crawling after landing stays in the
  grounded tail of the prone bank rather than replaying its lowering transition.
- Standing floor fire has a front-facing idle plus eight clean recoil drawings.
  In the elevator, holding Retina stands Yuri directly over the hatch and aims
  below his feet. The new barrel socket and real projectiles still break it.

Side-facing top-down rolls use the complete rotation. North/south rolls and
Prism Bastion's rear-view roll bank retain their existing art. M30 controls are
unchanged: side-view X rolls; the top-down directional-fire layout uses C to roll.

The generated firing take with baked flashes and an airborne prone-ending take
were rejected. The selected prone landing reuses the corrected Yuri30 grounded
drawings. Exact requests, job IDs and selections are kept in art/yuri31/source
and provenance.json. Fixed 192x224 cells, anchor96,160, one half-scale throughout,
binary alpha, even dimensions, whole authored sprites, measured roots/sockets.

Validation: 22 native Chromium checks pass, 4 ordinary-input corridor/cover
checks pass, no browser errors. Reviewed source contacts, onion overlays and
in-game roll, slide-turn, prone landing and floor-fire captures. All 145 assets
decode; 820 retained-art hashes match. Required game syntax and base suite finish
with exit0 / BUILD OK, 0 ERRORS. M30 input is simulated; no physical pad test.

Runtime: js/yuri31.js and scoped timing/stance/socket changes in js/escape29.js.
Export: _research/build_yuri31.py. QA: _research/probe_yuri31.py and existing
probe_escape29_route.py; reports under docs/qa/overdrive_yuri31*. Review:
art/yuri31/preview.html. Build: overdrive1015-yuri31-r1. No commit or push.
