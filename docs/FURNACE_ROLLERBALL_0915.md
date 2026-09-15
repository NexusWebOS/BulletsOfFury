# Furnace Tyrant accelerating rollerball — 2026-09-15

## Result

The Furnace Tyrant now owns a live rollerball attack in its core-phase sequence. The previous Inferno Reaver roll helper was unreachable because the Furnace controller owns and returns from the Stage-2 boss update first.

The new attack:

1. Samples the player's vertical position once and commits to that horizontal lane.
2. Displays the shared green/yellow/red field-of-view warning for 1.45 seconds while the whole authored boss plate winds up.
3. Crosses the playfield six times. Leg duration compresses from 1.24 seconds to 0.44 seconds, producing slow, medium, fast and super-fast travel.
4. Accelerates its continuous rotation from 5 to 25 radians per second during the live crossings.
5. Uses a whole-body contact footprint. Normal movement can clear the warned lane; barrel-roll and somersault invulnerability can pass through it.
6. Keeps the real Magma Ward flame shield around the rotating Furnace plate and returns cleanly to the existing rotor attack afterward.

No procedural or replacement art was added. The move rotates the approved Furnace core/head plates and existing authored shield.

## Verification

- `node --check assets/game.js` passes; runtime LF and suite CRLF line endings are preserved.
- Focused suite section 315: **10/10** assertions pass for the warning, lane lock, six crossings, speed and spin acceleration, full-width travel, contact damage, sounds and bounded handoff.
- Full suite: **4,060 passing / 57 failing**, exit 1. Every failing assertion is part of the established baseline, including the intermittent Stage-1 sand-tank timing assertion on this run.
- Real Chromium: **14/14**, zero page or console errors.
- Measured browser travel peaks rise from 590 to 1,662 px/s; rotation rises from 12.1 to 25.0 rad/s after the windup.
- Browser evidence: `docs/qa/furnace_rollerball_0915.json`.
- Screenshots: `_shots/furnace_rollerball_0915/furnace_rollerball_warning.png`, `furnace_rollerball_slow.png`, `furnace_rollerball_fast.png`, and `furnace_rollerball_superfast.png`.

