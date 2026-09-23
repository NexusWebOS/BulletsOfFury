# Chaos Harrier MK II — generated art upgrade

The follow-up request explicitly calls for a new generated miniboss. Stage 5 now
uses a new purple/chromium laser ship, with an intact hull, two independently
aimed wing cannons, central laser emitter, two small launch ports and animated
twin thrusters. Its runtime name is CHAOS HARRIER MK II, with a larger 260-pixel
assembly envelope. Existing shared warnings and upgraded attack patterns remain.

SpriteCook GPT Image 2.5 Sunburst generated an original component design followed
by one consistent 16-frame sheet using that generated design as its reference.
The private old hull was not uploaded: automatic approval review rejected that
export again, so this is a newly generated design from a text brief. Total cost
was 69 SpriteCook credits. Remaining balance after generation: 649.

The four component reels are hull (idle dim, idle bright, charge, cooldown), gun
(idle, charge, recoil, cooldown), central emitter (same four weapon states), and
thruster (four flame frames). No hull or weapon frame contains a laser beam.
Beams, charge effects, hit flashes and warning lanes are rendered separately.

`assets/game/chaos_harrier/mk2_0923/` contains the generation sources, 16 normalized
transparent PNGs, measured anchors and cell rectangles in `frames.json`, and
asset IDs, prompts, model and hashes in `provenance.json`. Rebuild normalization
with `_BUILD_SOURCE/build_harrier_mk2_0923.py`. All frames within each reel share
one scale; gun pivots and beam origins use the same runtime transforms. The left
mechanical cannon is mirrored to seat on its socket; projectile art is untouched.

`node --check assets/game.js` passes. The real Chromium probe
`_BUILD_SOURCE/probe_harrier_modular_0923.py` passes all warning, timing, lane-lock,
damage, death-cleanup, anchor and difficulty checks with zero page/console errors.
Generated hardware is checked through the actual game-context draw calls.
Screenshots inspected in `_shots/harrier_mk2_0923/`; the generated sheet and
normalized frame preview were also inspected. Full-suite completion is recorded
below. This does not claim a full human balance playthrough.

Full suite completed with 4,899 passing assertions and 80 existing failures
(exit 1). No new failure names against the prior Harrier pass; the intermittent
Stage 1 sand-tank check passed this time. Log: `_shots/harrier_mk2_suite_0923.log`.

No commit or push was requested. Earlier working-tree changes remain intact.
