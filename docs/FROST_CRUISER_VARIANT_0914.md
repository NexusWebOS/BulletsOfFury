# Frost Cruiser Hard/Furious variant - 0914

S3-07 is implemented on the actual stage-3 miniboss, Frost Cruiser (`SUBBOSS[3].kind=frostcruiser`). Cryo Spear (`rimewall`) is an alternate encounter; the stage end boss is a separate `cryospear` actor. The variant follows the live roster rather than historical naming comments.

Hard and Furious use a 226.8 x 226.8 hull, exactly 35% larger than the original 168 x 168. The existing normalized mounts, movement bounds and hull-hit routing consume those dimensions. Easy and Normal keep the original dimensions and authored colors.

A decoded whole-hull canvas is cached with a black/royal-dark-blue armor palette. It preserves alpha, deep black linework, warm pixels and bright saturated emitters, and retains the armor's shading and edge highlights through a monotonic dark-metal ramp. The original source asset and ordnance are untouched. Damaged and enraged states keep the same enlarged hull; their existing smoke, explosion, charge and hit-flash overlays still operate. No atlas or test-harness edits.

This closes size and palette only. The requested new locking rocket spirals, laser sweep and charge patterns remain separate checklist work.

## Verification

`_BUILD_SOURCE/cryo_variant_0914/probe.py` runs the real game in Chromium with `shoot.py`'s RAF trap and the established capture clock. It spawns all four difficulty variants through real debug fights and checks dimensions, scaled mounts, exact pixel protection, actual `drawImage` destinations, spawned missile/nose-round origins, collision coverage, and exclusion of the stage end boss and shared Jungle Cruiser encounter. Controlled HP snapshots exercise damaged and enraged drawing; capture-only invincibility keeps the preview running.

The normal/variant comparison and live damaged, enraged and firing screenshots were visually inspected. The seven-second silent preview is `_shots/cryo_variant_0914/Frost_Cruiser_Hard_Variant_0914.mp4`; it is also decoded after recording. This verifies the requested variant, not full-encounter difficulty balance. Proof and final suite results: `qa/frost_cruiser_variant_0914.json`.

No commit or push.

Syntax passed; all 12 native checks passed with no browser or game-loop errors. Full suite reached its final summary: 3,851 passing assertions / 59 failures, exit 1. Of those failures, 58 match recorded baselines. The additional road-tank heading failure was reproduced against the pre-change game: nine controlled RNG cases produce identical movement before and after, with .999 selecting only heading 7 during the test window in both. No newly introduced failing assertion was found. The intermittent road-tank test remains unresolved.
