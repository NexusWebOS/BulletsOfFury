# PASSOVER 0827A — Campaign, Player Atlases, Gravity Mode, and Velocity Void

## Snapshot purpose

This passover locks the complete local 2026-08-26 through 2026-08-27 development pass before the
remaining regression, audio, and combat-AI work continues. It is additive to the reconciled
house-and-repairs build and must not be replaced with an older loose-asset or pre-Gravity copy.

## Included systems

- Campaign input ownership: the assigned Back command cannot leave Campaign; Enter/controller
  Start opens Save/Load/Exit only after the map introduction finishes; Exit Game alone returns to
  the title and restores title music.
- Non-naval spacing and movement: full unit-frame separation, stationary hazards, committed jet
  curves, queued boats, and eight-direction tank driving with south-facing fixed turrets.
- Pilot-facing weapon and ability naming, including Helix Beam, Time Freeze + Thermoshock,
  Wrecking Ball, and Roller Ball.
- Production player atlases for weapon/special icons, player ordnance/projectiles, and complete
  pilot ship/barrel-roll frames. Superseded loose copies are deliberately removed.
- Maverick's independent Level I-V homing/helix laser entities, charged-ball release, dedicated
  Roman-numeral icons, and corrected Level-V helix-color rim.
- Stage 9 Velocity Void: 680-wide void/water master, new space/water roster, projectile and shield
  effects, destructible water rocks, Rift Warden pair, and emergency Tidal Sovereign fusion.
- Gravity Mode V2: Stage 5 owns the Fury-kit assembly; Stage 9 retains the completed craft through
  the secret portal. The transition uses pilot-specific blue-mask palette swaps and completes the
  fused Fury hull before the pixel glow and white flash.
- Gravity Mode Space Armory I-V: Laser Cannon, Shadow Orb, and Volley Missiles with production
  atlas icons/effects, Stage 5/9-only loadout isolation, progression persistence, and pilot-special
  precedence.

## Automated verification at snapshot time

- `node --check assets/game.js` — pass.
- `node --check _BUILD_SOURCE/test_fl.js` — pass.
- `git diff --check` — pass apart from Git's existing LF/CRLF notices.
- Deterministic Gravity Mode probe — pass with no page or console errors.
- Deterministic Space Armory probe — all 210 required atlas cells present; Laser Cannon, Shadow
  Orb, Volley Missiles, pickups, HUD, ground-loadout restore, Stage 9 retention, and special
  precedence pass with no page or console errors.
- Regression section 256 — pass.
- Regression section 257 — pass.

## Known test debt carried into the next ordered task

The full legacy suite reports one assertion in section 203: `stage 1 keeps its small authored
cast`. The assertion still assumes the early sparse four-type Stage 1 roster, while the approved
Stage 1 rebuild now intentionally fields eleven named ground/air/prop families and 24 scheduled
waves. Later regressions already verify that larger roster. The next task must replace the stale
count with the exact approved cast contract; do not delete or shrink the live roster to satisfy the
old assertion.

## Source and proof locations

- Runtime: `assets/game.js`, `assets/manifest.js`, `assets/game/atlas/`,
  `assets/game/gravity_mode/`, and `assets/game/stage9_void_rift/`.
- Builders and deterministic scenarios: `_BUILD_SOURCE/build_*`, `_BUILD_SOURCE/probe_*`, and
  `_BUILD_SOURCE/scenario_*` files added in this pass.
- Labeled atlas references: `docs/atlases/`.
- Gravity and weapon evidence: `docs/proofs/gravity_mode_v2_live/`,
  `docs/proofs/gravity_mode_stage5_stage9_live/`, and
  `docs/proofs/space_weapons_i_v_live/`.

Interactive pilot-by-pilot and full Campaign playtesting is intentionally deferred at the user's
request. The deterministic and static work can continue without treating that deferred visual pass
as completed.
