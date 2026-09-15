# Retina encounter-router audit — September 15, 2026

The shared Retina target list now represents the damageable structure the player
can actually hit. A protected hull, sealed core, assembly, arrival, phase
transition or invulnerable plate is omitted. Each target keeps a stable identity
while its position and size follow the authored moving part.

Covered component systems:

- Furnace Tyrant left/right arms, exposed body and detached head, with its Magma
  Ward barrier suppressing all false locks.
- Genesis mech limbs and current exposed core/head phase.
- Every live section on sectional tanks, aircraft and leviathans.
- Razorback's current gun, turret or hull phase.
- Tempest Leviathan's four apertures and hull, including both independently
  moving Tempest Brothers.
- Quad-laser miniboss cannons until their sealed hull opens.
- Both Blacksteel wing pools plus its vulnerable fuselage.
- Toxic Portal Warden canisters during its stun window.
- Existing Stage 4 electrical nodes/helpers, Stage 6 storm nodes/missile bays,
  Xeno helpers and Stage 9 split cores.

Missiles pass their selected moving impact point back into each encounter's
existing damage router. They therefore preserve per-part flashes, phase gates,
weapon shutdown, score/stat accounting and destruction effects. Destroyed parts
and shields that reform invalidate an existing single or multi-lock immediately.

Verification:

- Native Chromium: **13 passed / 0 failed** with zero page, console or controlled
  loop errors. A real Retina key tap selected a live Furnace arm; held Retina plus
  the real missile key launched into that wrapper and damaged only the selected
  arm.
- The authored Retina animation was observed through the game canvas on the
  moving Furnace arm. Screenshot:
  `_shots/retina_audit_0915/furnace_arm_retina.png`.
- Complete-suite section 304b adds **12 passing encounter-router assertions** for
  Furnace, quad-laser, Razorback, solo/dual Tempest, Blacksteel, Warden,
  sectional and mech layouts.
- Final syntax check passed. The complete suite reached its final summary at
  **3,862 passed / 58 failed**, exit 1. The failing assertion names exactly match
  the recorded 58-name `boss_designs_0915.json` baseline; none were introduced by
  this change.

Proof: `docs/qa/retina_audit_0915.json`. Source:
`_BUILD_SOURCE/retina_audit_0915/`, `_BUILD_SOURCE/test_retina_audit_0915.cjs`
and the guarded `patch_retina_audit_0915.cjs`. Runtime LF and suite CRLF are
preserved. No commit or push was performed.
