# Hard/Furious difficulty elite aces — 2026-09-15

## Result

Hard and Furious stage plans now add authored Expansion Vol. 1 ace fighters without altering Easy or Normal. Hard schedules one ace inside each stage's combat timeline; Furious schedules two. Every stage has a deliberate primary hull and a distinct secondary Furious hull drawn from the existing nine-fighter roster.

The aces use the established Elite X controller: shield-first durability, predictive horizontal pursuit, incoming-fire evasive rolls and aimed multi-round volleys. Their authored palettes remain baked into the source plates. No runtime tint or ordinary-fodder recolor is used. The new difficulty tag also defines the future Continue Up eligibility boundary.

Stage mapping:

- Stage 1: Razorback / Furytalon
- Stage 2: Emberwing / Furytalon
- Stage 3: Glacier Lance / Tempest
- Stage 4: Furytalon / Razorback
- Stage 5: Void Reaver / Nighthammer
- Stage 6: Tempest / Glacier Lance
- Stage 7: Iron Serpent / Void Reaver
- Stage 8: Nighthammer / Solar Warden
- Stage 9: Solar Warden / Void Reaver

The native browser pass exposed a cold-load issue where an active shield could draw before a later stage's hull. The spawn path now warms the exact renderer key and the base alias together. Final captures show all nine authored hulls, including directional forward shield plates on Furytalon, Iron Serpent, Nighthammer and Solar Warden.

## Verification

- `node --check assets/game.js` and `git diff --check -- assets/game.js` pass.
- Focused suite section 322: **23/23** assertions pass for difficulty isolation, stable plan insertion, authored mapping, elite identity, reward eligibility and all nine art files.
- Full suite before the final warm-key repair: **57 recorded failures**, exit 1. The 56 established baseline names remain, plus the known intermittent Stage-1 sand-tank fixture. A post-repair full-suite run is recorded with the final batch verification.
- Real Chromium: **42/42**, zero page or console errors.
- Browser proof builds all nine live stage plans at Normal, Hard and Furious; it spawns and renders every primary ace, checks the exact authored key, active shield and reward tag, then drives a Furious Tempest through an incoming-fire roll, pursuit and complete volley.
- Browser evidence: `docs/qa/difficulty_elite_aces_0915.json`.
- Screenshots: `_shots/difficulty_elite_aces_0915/elite_stage_01_razorback.png` through `elite_stage_09_solarwarden.png`.
