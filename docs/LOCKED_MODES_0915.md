# Boss Rush and Time Attack locked-mode presentation — 2026-09-15

## Result

The New Game mode roster now reads Campaign, Arcade, Co-op, Boss Rush and Time Attack. Boss Rush and Time Attack use new full-detail 16-bit arcade plates. Until the player clears the final Campaign stage, both plates render in grayscale under the exact Nexus II crossed-chain and red-keyhole lock art and reject confirmation with the game's blocked alert.

The account gate is stored as `bof_bonus_modes_v1`. Only `triggerVictory()` with `run.mode === 'campaign'` and `run.stage === CAMPAIGN_STAGES` can set it. An Arcade clear and an early Campaign stage cannot unlock either card. The two encounter routes remain disabled under ACH-14, so a revealed card reports `MODE DEVELOPMENT IN PROGRESS` instead of entering an unfinished mode.

## Art provenance

- `assets/game/ui/modes_0915/boss_rush.png` — generated with OpenAI ImageGen from the existing Campaign mode plate as the visual reference. Final prompt requested one isolated wide 16-bit sci-fi mode panel, exact title `BOSS RUSH`, a boss gauntlet scene, gunmetal/crimson/ember palette, crisp pixel edges, and no lock art.
- `assets/game/ui/modes_0915/time_attack.png` — generated with OpenAI ImageGen from the same reference. Final prompt requested exact title `TIME ATTACK`, a mechanical chronometer, high-speed combat, gunmetal/cyan/cobalt palette, crisp pixel edges, and no lock art.
- `assets/game/ui/modes_0915/nexus_chains.webp` — byte-identical copy of `NexusII-Beta/assets/spritecook/nx66/ovl_chains.webp`, SHA-256 `F526DB98E2775F56AA7371B5D9C36B292662329CBAB082CECBEF1C1C916C2D46`.

ImageGen baked a checkerboard outside each new plate instead of returning usable transparency. The game draws a measured `0,80,2125,555` source crop inside a beveled canvas clip, which removes that surrounding pattern without altering the authored panel. The failed alpha attempts were not shipped.

## Verification

- `node --check assets/game.js` passes.
- `_BUILD_SOURCE/test_locked_modes_0915.cjs`: 15 focused assertions pass in the full suite.
- The exact finished runtime reaches the full-suite summary at **4,013 passing / 57 failing**, exit 1. All failure names match the recorded 57-name baseline, including the intermittent Stage-1 sand-tank timing assertion; this mode batch adds no failure name.
- Real Chromium: 13 checks pass, zero page or console errors. It verifies all five cards, exact asset dimensions, two lock layers, denial alert, Campaign-only persistence, full-color reveal, and the unfinished-route guard.
- Screenshots: `_shots/locked_modes_0915/boss_rush_locked.png`, `_shots/locked_modes_0915/time_attack_locked.png`, `_shots/locked_modes_0915/bonus_modes_revealed.png`.
- Machine-readable browser result: `docs/qa/locked_modes_0915.json`.
