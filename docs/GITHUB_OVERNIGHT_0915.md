# GitHub overnight build — 2026-09-15

This publication advances the integrated `7635330b` mainline build through the verified 2026-09-15 gameplay batch. It includes the completed shared warning, elemental, shield-stun, no-one-shot, missile-tier, achievement, Arcade parity, locked-mode, Jungle Overlord-X, Furnace Tyrant, Frost Cruiser, Rime Wall, Olive Warden, Chrome Hammer and difficulty-ace work recorded in the request checklist and individual evidence notes.

The final additions before publication are:

- A one-hand Stage-5 Chrome Hammer vertical boomerang with accelerating charge spin, committed outbound lane, hazardous return, capped magnetic retraction and separate sound events.
- One authored Hard ace per stage and two Furious aces per stage, with nine distinct primary hulls, shields, evasive rolls, predictive pursuit and aimed volleys.
- Hard/Furious Olive Warden circular assault, glide, three-color warned body ram and collision-safe curved return.
- Difficulty-only Olive Warden formations: two escorts on Hard and three on Furious, with an authored olive gunner, player-like missile protectors and independent shield/hull damage pools.

## Final verification

- `node --check assets/game.js`: pass.
- `git diff --check`: pass for the gameplay source.
- Full `_BUILD_SOURCE/test_fl.js`: all new focused sections pass; **57 established failures**, exit 1, with no new failure names.
- Native Chromium: latest focused proofs pass 42/42 for difficulty aces and 15/15 for Warden escorts, with zero page or console errors and reviewed gameplay screenshots.
- Request tally at publication: **149 entries: 114 complete / 9 partial / 26 pending; 35 unfinished**.

Local `_shots/` evidence remains ignored. Unrelated local projects and scratch directories are excluded from the commit.
