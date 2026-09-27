# Stage 2–4 encounter revision — September 26, 2026

Mike requested new Stage 2 miniboss patterns, a black Furious version with charred fire, replacement of the Stage 3 Furious enemy swaps with transformations of the original ships, and a revamp of both Stage 4 encounters and their helpers.

His final ordering correction is **neutral fight → nuclear missile → new elemental form**. There is no neutral interval after the blast.

## Encounter changes

| Encounter | New attack structure |
| --- | --- |
| Stage 2 Inferno Reaver, Normal/Hard | Committed wing pursuit bursts, lateral fire run with a gap, interceptable fragmentation fireballs, paired charged fire lances. |
| Stage 2 Inferno Reaver, Furious | Black/charcoal hull with retained ember trim. A separate book: cinder scissors, ash pursuit, charcoal wheel, blackout pass, ash eruption. Charred fireballs have red cores and pale ash highlights. No legacy yellow dart/triangle projectile route. |
| Stage 3 Frost Cruiser | Alternating crosscuts, lateral icebreaker, radial shatter wheel with an escape sector, paired charged lances. The original hull and weapon mounts remain. |
| Stage 3 Rime Wall | Moving gaps in cannon fans, alternating cannon relay, shootable fragmentation orbs, advancing pressure volley, recovery between attacks. Original intact/damaged/critical plates remain. |
| Stage 4 Olive Warden | Suppression sweeps, alternating flank support, staggered missile rack, committed forward drive, paired center-gun break. Hard/Furious gunner and rocketeer visibly fly into station, lock before shooting, alternate firing turns and stop tracking after commitment. Normal retains the solo encounter. |
| Stage 4 Storm Sovereign | Battery sweeps, support turn, missile siege, opposing ion lances, forward drive, late core-gun barrage. Existing four-node shield objectives and 75/50/25% rearm gates remain. Independent helpers alternate charge/fire/overheat turns; the main hull and late central guns do not fire underneath their turn. |

Warnings use the existing combat FOV and framed warning sign. Lasers retain the shared three-second charge. Recovery is interpolated from the actual current position. Difficulty changes cadence, velocity, burst count, recovery time and support pressure.

The new director lives in `assets/encounters_0926.js`, loaded after `assets/stage3_thermo.js`. Narrow hooks in `assets/game.js` connect initialization, motion, attack ownership, damage, hull palette selection and projectile drawing. Authored editor scenes still own their actors when attached. Existing legacy functions remain for those scene tools and earlier isolated tests.

## Furious Stage 3 transformation

1. Fight the original ship for two complete neutral attacks. Fire and Ice deal basic damage with ordinary white hit flashes.
2. Neutral damage is capped at the first quarter of the health bar so a burst cannot remove the required transformation.
3. The enemy eases into view for one second; player position and camera are never assigned by the sequence.
4. The existing large atomic missile descends nose-first. The engine's atomic explosion and secondary cook-offs are followed by roughly 28 additional timed engine explosions.
5. A single smooth white fade/hold/fade reveals the **Fire** palette while explosions continue. No replacement actor or replacement hull is spawned; health, rewards and target identity remain intact.
6. After two completed attacks, a visible charge changes Fire to Ice, then repeats. Opposing elements deal **2×** damage. Same-element and ordinary attacks retain **1×** damage. Freezer's existing pre-scaled thermoshock is normalized at the encounter boundary to avoid multiplying twice; unrelated enemy bonuses remain unchanged.

The transformation and elemental switching are Furious-only. The former Thermocloud/Therno campaign handoffs have been removed. Their stored assets and inactive functions are retained rather than deleting authored work.

## Art

No new boss silhouettes or procedural projectile sprites were introduced. The original plates are palette-mapped once into cached canvases; alpha, outlines and luminance detail remain derived from the source pixels. Projectiles use `mwfx_fireball_*`, `l23fx_cryo_ball_*`, `l23fx_rime_orb_*` and the Stage 4 ordnance reels. The missile uses `lz_bomb` with authored Inferno exhaust; detonations use the shared explosion/atomic system.

## Verification and limits

- Syntax checks for `assets/game.js`, `assets/stage3_thermo.js` and `assets/encounters_0926.js`.
- Full `_BUILD_SOURCE/test_fl.js` suite: see `docs/qa/stage2_4_encounters_0926.json` for the final measured count and comparison against the 5,083-pass/zero-failure baseline.
- New executable regression section covers all 15 encounter/difficulty combinations, independent attack ownership, authored projectile routing, neutral/bomb/form ordering, burst-damage protection, same-actor transformation, elemental multipliers, and alternating helper/overheat windows.
- `_BUILD_SOURCE/probe_encounters_0926.py` runs 76 seconds per encounter/difficulty in real Chromium, exercises later HP gates, captures real renderer screenshots, and checks damage via `hitBoss`/`hitSubBoss`.
- `_BUILD_SOURCE/record_encounters_0926.py` records focused, invulnerable keyboard-flight previews. These are encounter inspection fixtures, **not completed campaign playthroughs or proof of player win rates**. Stage 4 health gates are advanced explicitly to show helper and final-gun behavior.
- Preview and temporary logs: `_shots/encounters_0926/`. Existing work is retained. Nothing was committed or pushed.

Final difficulty feel and comparative completion rates still need Mike's hands-on playtest. The matrix verifies progression, rendering, damage contracts and error-free execution, not that every player will judge each later fight harder.
