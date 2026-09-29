# The Hammer's heal can be broken (0929)

Mike: *"when I shoot the hammer when he charges it to restore his energy it is still not breaking and
bringing him to his stun state and he just keeps the shield up and keeps doing it."*

## What was wrong (Hard / Furious armor layer, `assets/furious_review_0927.js`)

| Symptom | Cause |
|---|---|
| Rounds aimed at the raised hammer never reached it | `fr27Reflect` turned back every player round inside the energy wall while he healed, the hammer included |
| When the heal did break, the shield stayed up | `hammerRecoveryBreak` cancelled the heal but left `A.barrier`, `empowered` and the charge in place |
| The stun never ended the heal cycle | `fr_stun` resumed straight into the storm-raise, which re-armed a heal, so he healed again at once |
| HAMMER (password) drew nothing during the stun | its dance draw only paints the boss in `attack` mode |

## What changed

- While he heals, a round aimed at the raised hammer (`hammerHeadPoint`, a ±40 px lane) or any missile passes the wall; rounds at his body are still turned back.
- Breaking the heal drops the barrier, his charge and his empowerment, and puts him in `fr_stun` for `FR27_STUN_T` (4 s), taking double damage.
- Out of the stun he returns to the fight he left (`fr27Resume`): hammer back in hand (`leap_reset`), or the storm rebuild if he was in the storm phase. No second heal starts from it.
- The base disarm stuns (`hammer_stun`, `storm_stun`) are no longer converted into `fr_stun`; the shield stays down through them and they end in the fight.
- `ht27CombatSequence` waits for all of those stuns by name, and the HAMMER dance draw shows the authored stun.

## Proof

- `_BUILD_SOURCE/probe_hammer_heal_break_0929.py` (real Chromium): 0 fails on the fixed build. Its busted arm (`--old`, the pre-fix file) fails 29.
- Suite section 378, `_BUILD_SOURCE/test_hammer_heal_break_0929.cjs`: 32 assertions.
