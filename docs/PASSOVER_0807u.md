# PASSOVER — drop 0807u   (FOUND THE CONFLICT, AND CUT IT)

Build: `BulletsOfFury_0807u`
Harness: **2,198 assertions / 203 sections / 0 failing**, twice, reaching the banner.

---

## 1. THE CONFLICT WAS REAL AND IT WAS ONE BLOCK

Mike: *"on levels 6 you had enemies from all levels appearing for some reason ... you have
something conflicting with some other code thats stopping waves from appearing right, theres many
patterns that arent what I wanted and its breaking the gameplay."*

`buildStagePlan` ran each stage's own table, and then — for every stage except 1 — **fell through
to a shared tail that added 31 MORE waves across 12 enemy types**, gated only on `stageNum>=2`
and `stageNum>=3`:

    assault x9 · drone x6 · gunship x5 · frost x3 · cryo x2 ·
    mine · octo · mech · scout · shieldd · turdrone · icegun

Stage 6 was fielding all of that on top of its own storm-front cast. That is precisely the
"enemies from all levels" he saw, and it is why no stage played the way its table reads: each
stage's authored plan was being buried under a generic one.

**Stage 1 was the only stage that escaped** — it has an early `return P` before the tail. Which is
also why stage 1 has always felt closest to right.

## 2. REMOVED, NOT PATCHED — AND KEPT

83 lines lifted out verbatim into `docs/removed/buildStagePlan_shared_tail.js` with a note
explaining what it was and why it went. Nothing is destroyed; the rebuild can reference it.

Each stage now gets EXACTLY the waves its own block defines:

    1  intcp, racer, topgun (+ its ground units behind the land gate)
    2  ash, carrier, cruc, disc, el_em, el_lr, eye, lance, skim
    5  crescent, hauler, mech, mine, needle, octo, oracle
    6  the jets, l6x_*, raptor, talon, warden, widow — its own cast, nothing borrowed

⚠ **Stages 2-8 are now SPARSE, and that is the intended state**, not a regression. Mike:
*"the enemies themselves still remain for these levels, we just need to re-code them from scratch
and 1 at a time."* The units, art and spawn machinery are all untouched — what is gone is the
generic wave spam that was overriding the authored plans.

Ten assertions now check that stage 6 cannot field any of the tail's signature types.

## 3. WHAT IS PRESERVED, AS ASKED

Untouched: the level 1-3 bosses, the level 1 miniboss, every enemy definition, every sprite, and
`spawnEnemy` itself. Only the wave TABLE tail was cut.

## 4. ALSO IN THIS BUILD

Two stats-screen bugs from Mike's screenshot:

* **The values were never using our font.** The label went through `stageText`, the value through
  `ctx.fillText` — unconditionally, outside the art check. Different face AND different baseline
  (`stageText` centres on cy, `fillText` sits on the alphabetic baseline), which is the drift
  where labels and numbers march apart down the panel. My proof render drew both with glyphs,
  which is why it looked right and the game did not.
* **MISSILE HITS read 117%.** `mslHits` counts ENEMIES hit and one splash missile hits several,
  so hits outran shots. Clamped, along with SPECIAL HITS.

## 5. NEXT, IN MIKE'S STATED ORDER

The rebuild is one enemy at a time, starting with stage 1. Before that, the repeat offenders he
has now raised more than once:

    the helix ball — no lance drawn on it, detonate on CONTACT only, volleys from the burst
    the thrusters — stop overlaying, animate the sprite frames each pilot already has
    every menu backable with a keyboard button
    the fireorb/iceorb icon on level 3
    the stage 1 transition
