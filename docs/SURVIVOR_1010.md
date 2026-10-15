# Damaged satellite survivor — October 10, 2026

> Superseded continuation: the survivor now stays attached to the satellite,
> spreads over its hardware and corrupts the whole screen with green binary
> and code. See [the active takeover](HOMECOMING_TAKEOVER_1010.md) for the
> 16.4-second scene, infection frames and final QA. The crawl/contact art below
> remains active; its coil/launch reel is archived.

Mike requested better generated art and animation for the surviving alien
symbiote after the pilot returns to Fury HQ. The true ending now uses a new
wide dish plate and a matching damaged-panel close-up. The existing black
liquid, embedded mechanical shards and single emerald core remain its identity.

The creature has 32 distinct crawling poses, 16 coiling/charging poses and 16
upper-left takeoff poses. Sixteen authored emerald contact/discharge effects
grow beneath it, burst during takeoff and break into small sparks. The engine
supplies surface travel and flight translation; the creature's changing shape
comes from the generated frames. The old wobbling/rotating still and painted
line trail are retired from this scene.

The survivor clock remains **26.4–33.8s**, preserving the later Fury Command,
deep-space and sequel beats. Local shot times:

| Time within scene | Shot |
| --- | --- |
| 0–1.65s | Wide dish, creeping along the damaged bowl |
| 1.65–4.00s | Close view of the creature pulling over the panels |
| 4.00–5.20s | Tendrils coil, core intensifies, contact arcs grow |
| 5.20–6.30s | Wide view, pointed body streams away to the upper left |
| 6.30–7.40s | Empty dish, then black transition into Fury Command |

The existing ending cue flags fire the charge and launch sounds once. The
previous homecoming fade wraps this new renderer. Ordinary campaign endings
still skip the sequel continuation, and Arcade retains its score card. Active
ending window resizes now update the native viewport rather than stretching
the generated art in CSS.

`_BUILD_SOURCE/build_survivor_1010.py` owns all 82 loose PNGs and
`assets/survivor_art_1010.js` together. All animation cells use **384×384**
transparent canvases and the same **192,192** core station. Native pixels are
cropped, padded and translated by integer amounts. The luminous core component
defines the physical pivot; a changing brightest highlight cannot shift it.
No per-frame fitting, sprite rotation, resampling or procedural sprites are
used. The two background plates receive even transparent padding; their measured
content rectangles retain the authored aspect ratio.

Source images, exact generation prompts, measured native references, hashes and
accepted/rejected generation records are preserved in
`_ART_SOURCES/survivor_1010/`. Rejected sheets had incorrect counts or overlapping
cells. They remain archived and are never registered. The original ending dish
and survivor art also remain on disk. No atlas edits were needed.

Runtime `assets/survivor_1010.js` loads before `hq_landing_1010.js`, so the
homecoming captures the new `victoryDish` owner. Its art is prewarmed for the
late campaign and included in the real ending readiness gate. Preview controls
now include **Symbiote**, **Charge** and **Launch**, with the timeline extended
through the first Fury Command beat. Use `?scene=survivor` to open on the close-up.

Verification: **8,269 regression assertions, zero failures, final success
banner, exit 0**, compared with the preceding 8,256 baseline. **17 native
Chromium checks and 12 preview-control checks pass**, with zero page, console or
asset errors. All 80 animation cells render through native `XART.get` and the
game context; visible pixels match the authored black composite within one
color step, and the physical core stays within one pixel. All nine pilot
choices, narrow layouts, pause/seek/play, cue latching and ending branches pass.

An **8.99s actual engine recording** covers the HQ fade, both dish shots,
charge/discharge, flight, empty dish and Fury Command. Native screenshots,
all-frame contact sheets and 36 timed movie frames were inspected. The recording
is silent; the interactive preview plays the existing sounds. Verification
media and logs are under ignored `_shots/survivor_1010/`.

[Portable QA evidence](qa/survivor_1010.json).

`assets/game.js`, `_BUILD_SOURCE/test_fl.js`, the homecoming art registry and
all previous staged work remain unchanged from the start of this pass. Existing
LF/CRLF endings are preserved. Local only; no commit or push.
