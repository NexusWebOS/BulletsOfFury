# Drawn stealth flips, full Furnace flame and helix palettes

Mike's October11 follow-up rejects warped banking frames and requests actual
barrel rolls and somersaults, a complete upper fire graphic, Jace's sphere for
Maverick in his colors, and a less jumpy atomic cloud. This supersedes the
motion and mixed-source atomic banks documented in ANIMATION_ONION_1011.md.

## Delivered art and live behavior

- Blue, red, green and orange heavy stealth fighters each have16 distinct roll
  views and16 distinct somersault views. Actual sidewalls, belly, engine-facing
  and nose-facing views come from drawn plates, without affine deformation.
  The orange fighter carries its two gun pods. Blue/red/green idle/damage plates
  retain the original opening fighter; orange uses its new gun-equipped plate.
  Its damage slot aliases its intact plate; no new damage reel is claimed.
- Existing Harrier elite evasions, inverted posture and fast lateral banks,
  ordinary fighter roll states, and the carrier launch use the new views.
  Original encounter controllers, independent module health and targeting stay
  authoritative. A broad legacy bomber predicate previously recolored any
  marked stealth fighter red: explicit blue/orange/green identities now survive.
- Furnace retains the large32-frame flowing column and16-frame flared origin.
  A new16-frame organic crown completes its leading end. The game and preview
  share `assets/part2_fire_renderer_1011.js`, including the narrow origin,
  flowing body and tip. Invalid geometry returns; the draw budget stays bounded.
- Maverick uses the exact32 Jace sphere poses in green half-charge and
  purple/blue overdrive palettes. Alpha, luminance and the sphere's motion are
  preserved. Charge, launched balls and terminal blooms use those cells. His
  existing aura, charge thresholds, projectiles, damage and release physics
  remain intact. Sixteen pixels of transparent padding protect the two banks.
- Atomic now uses one newly generated32-pose progression at a common physical
  scale,384x576 canvas and fixed ground pivot192,480. It expands, billows and
  dissipates gradually. Rising cap poses7/8 are registered in measured growth
  order. Last wisps fade before removal, and the preview pauses between blasts.

All delivered frames are even: fighters256x256, cap384x384, atomic384x576,
Maverick288x288. Registration only crops, pads, translates and applies a common
proportional scale. Generated sheet gutters are measured from the actual
connected aircraft plate so neighboring row fragments cannot shift its pivot.
No procedural replacement sprites, per-frame stretch or duplicated tweening.

## Files and reproducibility

Built-in image_gen produced six source sheets with112 actual newly drawn
poses. Derived red/green and Maverick palettes add128 cells; those are palette
variants, not128 additional generated motion drawings. The active P2 manifest
contains337 registered cells and335 distinct images. Orange intact/damage and
roll-zero registrations share their exact approved plate.

- Source images, exact generation prompts and source/frame hashes:
  `_ART_SOURCES/part2_motion_1011/`, including `prompts.json`,
  `orange_prompts.json`, `provenance.json` and `audit.json`.
- Shipping graphics: `assets/game/shared/combat/part2_1010/`.
- Owning command: `python _BUILD_SOURCE/build_part2_art_1010.py`. It invokes
  `part2_motion_art_1011.py` after the previous registration helpers, writes all
  pixels and `assets/part2_art_1010.js` together. Original rejected sources
  remain archived; obsolete warped P2 bank poses are excluded from registration.
- Runtime: `assets/part2_combat_1010.js`, `assets/part2_motion_1011.js` and the
  shared fire renderer. These are loaded from the existing index.html.
- Review owner: `_BUILD_SOURCE/build_part2_review_1010.py`. Published locally at
  `http://127.0.0.1:8794/docs/previews/part2_1010/index.html?revision=20261011-motion`.
  The preview includes both moves for all four palettes, both Maverick colors,
  Onion mode, complete fire and the progressive atomic cloud.

## Verification

`node --check assets/game.js` and the changed runtime modules pass. Full
`node _BUILD_SOURCE/test_fl.js` reaches its final summary with8414 passing
assertions, zero failures and exit0. Final raw log:
`_shots/part2_motion_1011/full-tests.log`.

Native Chromium proofs use the game's XART keys and its actual drawing context:
128 fighter motion plates, progressing elite evasions, carrier launch, Maverick
charge/release, alpha/luminance preservation, whole fire and the atomic strike.
The preview additionally checks every frame's borders and fixed camera. Actual
Furnace, Jace and the Harrier are rechecked with the existing presentation probe.
Current reports and native contact sheets/GIFs are under `_shots/part2_motion_1011/`;
the durable summary is `docs/qa/drawn_motion_1011.json`.
The four refreshed native probes total 67 passing checks, zero failures and no
page, console, renderer or missing-asset errors.

Initial visual verification caught an empty motion selector and the broad
bomber recoloring issue. Both were fixed and rerun. Elite fixtures originally
left the encounter in carrier mode, and a transparency check used a luminance
threshold on an opaque canvas; corrected fixtures now exercise live ace mode
and compare alpha through black/white native renders. These are no longer open
failures. Protected fixtures do not establish a human Furious campaign clear.

Existing staged, unstaged and untracked work is preserved. No commit or push
was requested for this correction. HEAD remains7539951.
