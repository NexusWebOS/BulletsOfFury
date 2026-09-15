# Hard Razorback duo — September 15, 2026

## Result

S1-05 is complete. Stage 1 on Hard now fields two complete Razorback siege tanks simultaneously.

- Each tank owns its full authored hull rig, destructible gun/turret/hull pools, movement, attacks, projectile ownership, locks, damage feedback, and death sequence.
- The encounter controller owns one combined miniboss gauge and completes only after both tanks are destroyed.
- The two attack books start one step apart: one tank opens with machine suppression while the other charges its sonic attack. Their releases do not stack on the same frame.
- Camera-relative homes, attack lanes, and ram limits keep both complete silhouettes visible and preserve a traversable gap between them.
- Clearing or transitioning one tank removes only that tank's projectiles and Retina locks. The surviving tank continues fighting.
- Ordinary projectiles, held laser beams, flame overlap, player contact, and Retina missiles route to the actual actor and exposed component under the hit point.
- Normal remains the existing single Razorback. Furious remains single so S1-06 can supply its separate 50%-larger hyper-tank design.

## Verification

- `node --check assets/game.js`, test/probe syntax checks, LF/CRLF preservation, and the CRLF-aware diff check pass.
- Focused suite section 330: **14/14** assertions pass for difficulty isolation, two full HP pools, separate homes and attack books, four component targets, actor-specific damage, projectile ownership, collision gaps, independent pressure, and two-kill completion.
- The complete suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/razorback_duo_0915/probe.py`: **17 passed / 0 failed**, with zero page, console, or game-loop errors.
- Pixel-reviewed native frames confirm two fully visible authored tanks, simultaneous machine/sonic pressure, distinct movement lanes, and one remaining tank after its partner is destroyed. The probe also records a five-second native gameplay video.

Machine-readable Chromium evidence: [qa/razorback_duo_0915.json](qa/razorback_duo_0915.json).
