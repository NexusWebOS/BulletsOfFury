# Passover 0812f — the bosses had the same unwarmed-art bug, and NEWBOSS is a dead table

Continues 0812e. Mike: *"upgrade all remaining minis and regular bosses."* Before upgrading
anything I audited what the eight bosses actually do — and two of them were not drawing their art.

---

## 1. ⚠ A KIND NAME IS NOT AN ART PREFIX — for BOSSES as well

0812c found this for the minibosses. `warmStage` warms `addPrefix(STAGES[n-1].boss)`, i.e. the
KIND name. Audited by spawning each stage's boss after a full `beginStage` + `warmStage`, with
`XART.rdy` wrapped to record what it was asked for:

```
stage 1  damkeeper       chopper_idle_0       NOT READY
stage 2  infernoreaver   nsb_inferno_reaver   NOT READY   <- opened on the silhouette fallback
stage 3  cryospear       nsb_cryo_spear       NOT READY   <- opened on the silhouette fallback
stage 4  warhawk         (scenery only)
stage 5  voidbat         (scenery only)
stage 6  stormsovereign  (scenery only)
stage 7  toxicleviathan  -
stage 8  vileexistence   -
```

`addPrefix('infernoreaver')` cannot match `nsb_inferno_reaver`. Warming is **driven off the tables**
now rather than hand-listed — any ship boss warms its own hull key, any NEWBOSS stage its idle
reel, any ship mini its hull — so a boss added later is warmed by code that already exists.
Stages 2 and 3 now report **nothing unready**.

## 2. ⚠ THE ENTIRE `NEWBOSS` TABLE POINTS AT ART THAT DOES NOT EXIST

All four idle keys are absent from every namespace:

```
1 chopper_idle    2 fboss_idle    3 iboss_idle    4 tankboss_idle     NONE REGISTERED
```

So `_hasNewBoss` in `drawBoss` can never be true, and every stage falls through to its other path.
For stage 1 that is the **legacy helicopter sprite**, which is what actually renders — and it
renders well (`docs/proofs/boss_s1_0812f.png`). Stages 2–4 have their own ship/mech paths.

Nothing is broken by this, but a whole branch of `drawBoss` is unreachable and it cost a probe
cycle to discover. §221 pins it as **state**: the assertion fails the day that art is registered,
and that failure is the reminder to finish the wiring or delete the branch.

⚠ **My audit labelled stage 1 "PROCEDURAL FALLBACK", which was wrong** — my probe's path detector
ended in a catch-all, and the truth is it takes `drawBossSprite` with the legacy art. Recorded
because the label was alarming and the reality is benign.

## 3. Suite

**2,537 assertions / 226 sections / 5 failures** — the same five long-standing ones.

## 4. Where the bosses stand

```
stage  boss             draw path   art at spawn
1      damkeeper        legacy      ok (NEWBOSS art absent - see above)
2      infernoreaver    ship        FIXED here
3      cryospear        ship        FIXED here
4      warhawk          mech        ok
5      voidbat          ship        ok
6      stormsovereign   mech        ok
7      toxicleviathan   mech        ok
8      vileexistence    modular     ok
```

Still owed: the Herald's `mba_vr_*` plates (not in `XART._src` at all - routed around in 0812c,
not resolved), `subcore` and `ratking` as the two minis with no new-pack art, and stage 8's boss
which Mike has said is not built.
