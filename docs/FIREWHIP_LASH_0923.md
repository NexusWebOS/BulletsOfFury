# Firewhip left/right lash — September 23, 2026

Replaced rigid radial sweep geometry with a constant-length rope curve driven from its root. A delayed bend travels toward the tip, producing a slower windup, faster crossing snap and curling reversal. The cycle is continuous across both direction changes. Existing fire frames and anchored circular muzzle are retained; damage, reach and half-stroke duration remain unchanged.

Drawing and collision sample the same 64-node curve. The expanded Chromium probe verifies zero discontinuity at either reversal, constant arc length, matching visual/collision nodes, hits on both sides and one damage application per target per stroke. Its GIF now advances actual Forge ticks through a full 1.4-second left/right cycle; the earlier flame-only GIF intentionally held the sweep at one pose.

Verification: syntax passed; `_BUILD_SOURCE/probe_firewhip_muzzle_0923.py` passed with no page/console errors. Inspected `_shots/firewhip_muzzle_0923/whip_motion_contact.png`; animated result is `whip_motion.gif` in that directory. Full suite log: `_shots/firewhip_lash_suite_0923.log`, exit 1 with 4,890 passing assertions and 80 existing failing assertion names; no new failures. The previously intermittent Stage 1 sand-tank assertion passed this run. No commit or push.
