# PASSOVER 0825C — Exact Pilot Elements, Herald Name, Portrait Sources

## Result

- Cole has no special orb and no elemental damage bonus. His special kit remains Sonic Boom plus
  nuclear missiles.
- On Stage 2, only Freezer's Ice Breath receives x2 damage.
- On Stage 3, only Freezer's Fire-Ice / thermoshock ball receives x2 damage.
- Generic fire and ice orbs remain x1 for Cole and every other pilot. Freezer's bonus does not leak
  to the wrong attack or to later stages.
- Stage 8 keeps the complete intact Spawn Carrier replacement hull, but its encounter name is now
  **HERALD OF DEATH**.
- The portrait-source re-upload was found on GitHub branch `codex/codex-edition`. The 35 originals
  for Axel, Cole, Decker, Freezer, and Maverick plus their contact sheet are preserved under
  `_ART_SOURCES/BOF_EmotionPortraits_0825/`. They match the live atlas cells pixel-for-pixel, so the
  atlas did not need replacement and the stale portrait TODO is closed.

## Runtime contract

`elementMultiplier(element, attackKind)` returns x2 only when all four properties match:

1. active pilot is Freezer;
2. Stage 2 + `ice` + `icebreath`, or Stage 3 + `fireice` + `fireice`;
3. the projectile call site supplies the authored attack identity;
4. every other combination returns x1.

The bonus is applied consistently to normal enemies, minibosses, and bosses for Ice Breath. Both
thermoshock projectile routes (the charged fireball path and the orb/shard path) carry the Stage 3
identity. Cole's Sonic Boom, nuclear missile, and special-crate routing were not changed.

## Verification

- `node --check assets/game.js` — pass.
- `node --check _BUILD_SOURCE/test_fl.js` — pass.
- `git diff --check` — pass.
- Regression section 238 verifies Cole x1, Freezer Stage 2 Ice Breath x2, Freezer Stage 3
  thermoshock x2, all negative controls, and the Stage 8 encounter name.
- Full regression run reports only the same seven known stale assertions from 0825B; no new
  failures.
- Real headless Chromium capture shows the full intact Stage 8 hull with the `HERALD OF DEATH`
  miniboss bar below the HUD: `docs/proofs/stage8_herald_0825c.png`.
