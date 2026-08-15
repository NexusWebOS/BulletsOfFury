# Passover 0812g — the muzzle flash now matches the round it fires

0812d put the nca_87 pack on the machine gun and the spread with Mike's eight-tier palette and
**left the flash behind** — so the gun lit one colour and the bullet left in another. Both weapons,
all eight tiers, now light from the same pack and the same palette.

Proof: `docs/proofs/muzzle_mg_0812g.png`, `muzzle_spread_0812g.png`.

---

## 1. Two faults in the old flash

⚠ **IT WAS CLAMPED TO FIVE TIERS.** `_mgMuzLv` was stored as `min(5, lv)` at **all five**
assignment sites, so Cole's exclusive 6 and 7 lit the level-5 flash — the same fault 0801cb found
in the pellet draw, where tiers that were mechanically real were visually identical to everyone
else's top tier.

⚠ **AND IT RAN ON THE WALL CLOCK.** `(performance.now()/45|0)%6` on a flash that lasts **0.07s**
means the frame you get depends on when you pulled the trigger, not on how far the flash has come —
so a four-frame reel authored to grow and decay was usually entered halfway and often at its last
frame. It is a one-shot off `_mgMuzT` now: exactly the correction 0811y made to the pellet.

The spread takes the pack's **second, wider** flash (cell `[3,3]`, 13250 ink against row 0's
5076–10081) because a spread lights the whole nose, not a single barrel.

## 2. ⚠ `node --check` CANNOT CATCH WHAT NEARLY SHIPPED HERE

I inserted the new block *between* the two legacy branches — leaving `let _p87muz` declared **after**
a branch that reads it. That is a temporal-dead-zone `ReferenceError` on **every spread shot**, and
it passes a syntax check cleanly. Caught by a probe that fails on any thrown error, which is the
only way that class of mistake is caught before Mike sees it.

⚠ **AND IT MUST NOT EARLY-RETURN.** My first cut wrote `if(p87Draw(...)) return;`. That block sits
mid-way through the player overlay draw — **Cole's Aegis aura and the orbiting orbs come after it** —
so the return would have silently deleted them whenever the gun happened to be lit. It sets a flag
instead, and both legacy branches gate on it (without which the spread lights two muzzles at once).

## 3. ⚠ Two probe faults on the same three lines

Worth recording because both produced a confident, wrong bug report:

- **Tier 8 does not fire the machine gun.** `coleTier() >= 8` returns immediately — the fusion
  cannon replaces it, driven from the input path. Asking tier 8 for a muzzle level reads whatever
  the previous shot left behind, which is what made the first run report "still clamped to 5".
- **The pilot must be Cole.** `coleTier()` caps everyone else at 5, so firing as whoever the game
  booted with reports tiers 6 and 7 as clamped when the clamp is the correct rule.

Both were the probe. The code was right the second time and the third.

## 4. Suite

**2,543 assertions / 227 sections / 5 failures** — the same five long-standing ones.

New **§222** pins all four properties: no site clamps to 5, all five store 1–8, the reel runs off
its own remaining time and not the wall clock, and the block flags rather than returning.
