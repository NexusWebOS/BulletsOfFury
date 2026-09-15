# Continue Up reward system — September 15, 2026

## Result

MODE-07 is complete. Continue Up is now a real falling pickup with three explicit reward boundaries:

- An authored difficulty ace always drops one on Hard or Furious.
- A miniboss cleared without either active player losing a life drops one after its destruction sequence.
- A boss cleared without either active player losing a life drops one when its defeat begins.

Each encounter snapshots the combined death count when it spawns. A reward resolves once, and a death by either co-op seat invalidates that encounter's deathless reward. Easy and Normal never receive elite drops because their stage plans contain no difficulty aces; their deathless encounter rewards remain active.

Collecting the pickup adds one shared Continue credit. Finite Arcade and Campaign banks include the bonus, including Stage 9's campaign reserve, and the Continue screen displays the increased remaining count. Easy and Normal campaign keep their existing unlimited bank while recording earned Continue Ups for any later finite rift reserve. Campaign save slots now preserve both spent and earned Continue credits. A new run resets both counters.

The pickup currently composes the shipped authored Life Up plate with a cyan ring and a large `C`, making it distinct in play without adding placeholder art. The requested dedicated SpriteCook Life Up and Continue Up plates remain tracked separately as MODE-08.

## Verification

- `node --check assets/game.js`, the focused test module, and the CRLF suite file pass.
- Focused suite section 324: **18/18** assertions pass for eligibility, one-shot resolution, co-op invalidation, collection, finite and unlimited bank behavior, save/load persistence, and spending the added credit.
- The complete suite reaches its final summary with the same **57 recorded failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/continue_up_rewards_0915/probe.py`: **18 passed / 0 failed**, with zero page or console errors.
- The native probe exercises a real Hard ace death, real pickup collision, real miniboss and boss spawn/death hooks, the authored atlas draw path, collection sound routing, and the actual Continue handler.
- Pixel-reviewed frames are stored under ignored `_shots/continue_up_rewards_0915/`.

Machine-readable Chromium evidence: [qa/continue_up_rewards_0915.json](qa/continue_up_rewards_0915.json).
