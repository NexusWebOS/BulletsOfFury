# Olive Warden Hard/Furious escorts — 2026-09-15

## Result

The Stage-4 Olive Warden now fields difficulty-only escort formations while Normal retains the approved solo fight.

- Hard deploys two independent escorts: one stationary flank gunner and one aggressive missile protector.
- Furious deploys the gunner plus two missile protectors for a three-ship formation.
- Every helper uses the authored south-facing Olive Carrier plate, matching the Warden's military palette without a runtime recolor.
- The gunner holds its assigned flank, aims a separately animated rotary barrel at the player and fires readable burst groups.
- Protectors follow bounded player-like approach and retreat legs, track the player's column, and release shootable missiles on committed headings. The global post-Stage-1 no-homing rule remains intact.
- Each helper owns separate shield and hull pools. Player rounds route through the real miniboss part hit test, deplete the shield first and can destroy the helper independently.
- The established Hard/Furious Warden orbit, glide, warning, ram and return sequence continues behind the escort controller.

The Furious third helper currently uses the same approved Olive Carrier language. Its requested black-camo Dark Chromium identity and Maverick-style charged ball remain the separate SpriteCook-dependent S4-08/S4-09 work.

## Verification

- `node --check assets/game.js` and `git diff --check -- assets/game.js` pass.
- Focused suite section 323: **14/14** assertions pass for difficulty counts, roles, authored hulls, shield-first damage, mounted fire, pursuit movement, committed shootable missiles and Normal isolation.
- Full suite: **57 recorded failures**, exit 1. All failure names match the established baseline; section 323 adds none.
- Real Chromium: **15/15**, zero page or console errors.
- Native proof opens the real Stage-4 miniboss route, renders both formations, observes live gunner and protector rounds, and sends damage through `subBossSolidAt` and `hitSubBoss` to the escort shield.
- Browser evidence: `docs/qa/olive_warden_escorts_0915.json`.
- Screenshots: `_shots/olive_warden_escorts_0915/warden_escort_01_hard_pair.png` and `warden_escort_02_furious_trio.png`.
