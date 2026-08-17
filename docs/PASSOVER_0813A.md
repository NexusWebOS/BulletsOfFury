# PASSOVER 0813A — the plume that kills what it touches, stage 2's red, and the reaver's fire

Mike's list, verbatim, with what landed against each.

---

## 1. "Flamethrower and Ice breath - improve hitboxes to be from where they start t owhere they end."

**This was a real miss, and a big one.** `flameDraw` lays the plate down as a **uniform column**
`flameHalfW(lv,1)` wide — the flare width — for the plume's whole length. `flameHit` instead
evaluated `flameHalfW` at the travel fraction, which **tapers to `flameBase` at the nozzle**.

At level 5 that is **96px drawn against 35px tested**. An enemy sitting inside the visible fire,
right beside the ship, took nothing. The taper was invisible art-side, so it read as "the
flamethrower doesn't hit what it's touching" rather than as a width bug.

Measured, before → after (`probe_flamebox.py`):

| | nozzle | middle | tip | drawn |
|---|---|---|---|---|
| fire, before | ~35 | tapering | 96 | 96.3 |
| fire, after | **96.2** | **96.2** | **96.2** | 96.3 |

**The ice had a second, separate bug the probe exposed.** The plume is anchored at the **nozzle**
(`f.bot`, at the ship); `f.top` is the far tip. `ICE_H` shortens the ice reel, and the draw applied
it by holding `f.top` and pulling the **bottom** up — shortening it *at the ship*. Measured at lv5:
fire spanned 87..355 with the ship at 355, **ice spanned 87..328**. The frost floated 27px clear of
its own nozzle, and nothing could be hit point-blank at all (`boundaryAt(nozzle)` returned "no hit").

Now anchored at `f.bot` so the **tip** pulls back. Fire's geometry is bit-identical — `dh === reach`,
so `f.bot-dh/2` is the same centre it always had. Only the ice moved, and it moved onto the ship.

The shape now lives in **one place** (`FLAME_ICE_W/H`, `flameHalfWDrawn`, `flameSpanTop`) and
`flameDraw` takes its scale *from* those, so the drawn column and the hitbox cannot drift apart again.

## 2. "anytime we hit anything with these attacks, shouild make an attack sound like all other attacks do."

0812l wired `weaponHitSfx` at six damage sites, but the enemy-flame site had a **misplaced guard**:

```js
hitEnemy(...); if(typeof stageStats!=='undefined') weaponHitSfx(...); stageStats.hits++;
```

The guard was on the *sound* while `stageStats.hits++` ran *unguarded* right beside it — both wrong
in the same line. Swapped. Both weapons now measure **8 hit sounds** over a 30-frame point-blank burn.

## 3. "Stop using that annoying beep noise wehn homing missiles are shot off at us too."

`enemyLockOn` ended with `Audio.SFX.lockAlert()` — a rising triple-beep. Every racer flight phase
(curl, dive, flee) calls `enemyLockOn` directly, so a busy screen stacked it into a siren. Removed;
the shrinking reticle `updatePlayerLocks` draws on the player carries the telegraph.

The **three remaining** `lockAlert` calls are the wall-of-fire announce — a different mechanic, with
no reticle to read, that Mike did not ask to change. Left alone. Probe: **0 beeps on 5 locks.**

## 4. "Do not use red pellets or effects for his attacks ... It will look bad with the lava."

**The boss was not the source.** `probe_reaverpal.py` showed the INFERNO REAVER fires `eshot` (240
rounds/40s) and `emissile` (14) — never `plasma` — so the obvious-looking `_PLASMA_PAL[2]='red'`
would have recoloured a projectile this boss never fires.

`eshot` is `FIRETYPES.pellet`, whose family *and glow* both come from `PELLET_FAM[run.stage]` — and
stage 2 was **family 0, glow `#ff6b5a`**. Red pellets on an orange-red lava field. Moved to family 2
(`#ffd36b`), the yellow already proven on stage 1, so it is a colour that has shipped rather than a
new guess. `_PLASMA_PAL[2]` moved red → orange with it.

> ⚠ The first pass of that probe was **wrong and looked right**: it drew a bullet onto a black fill,
> but `drawWorld` repaints the whole scene, so it measured the lava backdrop. The tell was `eshot`
> and `emissile` returning *identical* rgb and a pixel count equal to the entire crop box. Frame
> differencing is what isolates a bullet here.

## 5. "hes charging up a fire attack as an aura surrounds him ... a big ass fire orb ... if we dodge out of its path as it gets near us, it goes off screen and does not continue to home"

The last clause is the whole mechanic. A homing shot that never stops homing isn't dodgeable, it's a
timer. `fireorb` homes while **far** and **commits** once inside `FIREORB_COMMIT` (96px): the heading
freezes for good and it flies that line out of the world. `_committed` latches — it can never
re-acquire.

The aura is `b.flash`, which already routes through `xartTint` on the boss's **own authored plate**,
so nothing procedural is drawn. The orb is the authored comet reel at `pal:'orange'`, `szMul:2.6`.

Measured (`probe_fireorb.py`), 1.15s wind-up:

| | closest approach | committed at | left the world |
|---|---|---|---|
| player holds still | **0** (it hits) | 94px | yes, 3.2s |
| player breaks late | **61** (it misses) | 94px | yes, 3.2s |

## 6. "those laser attacks continue to rotate as he wobbles side to side and shoots out rockets we shoot down"

The rotating rake already existed (0812n) and already ticks for ship bosses. Added the **wobble**
under it — the hull drifts across its own spokes so the corridor keeps moving — and a **rocket pair
every 1.25s** while the rake is live. Those are `emissile`, which the eBullet loop already lets
player fire destroy, so they are shootable by construction.

## 7. "do not allow us to pull up the pause/save game menu until we reach this point"

`campPauseIsCampaignScreen()` tested the state and `run.mode==='campaign'` — but `run.mode` is set
the moment CAMPAIGN is picked, so every screen on the way to the map already satisfied it. Now
latched on `campHubSeen`, set when the map is actually drawn and cleared at the title so a second
campaign re-gates. A strict tightening: it cannot enable the menu anywhere it wasn't already allowed.

---

## NOT DONE — still open from Mike's list

These are his asks that this drop does **not** deliver. They are not blocked, just not started:

- **The lava arena.** "when you approahc boss, its supposed to continue to scroll to the lava, and
  then the lava itself is the new arena. vertically scroll fast like were chasing this boss and
  flying." This is stage-flow work — `drawLevelMaster`/`mapScroll` and the boss-approach gate — not
  a boss-behaviour change, and it is the largest item on the list.
- **Cinematics: all characters on screen at once, only the speaker lit.** "dont make them apppear 1
  by 1, just ligth up the one whose talking."
- **Cinematics: facing.** "characters shouldnt be facing away from each other in the cinematics."

## Suite

**2,636 assertions / 234 sections / 5 failures** — the same five that predate this drop (preload
count, the two `_superseded` ledger ones, volley round count, flash families).

Two assertions were rewritten rather than coded around:

- The ice-size assertion parsed the **literal** `const ICE_W = 0.85, ICE_H = 0.90, ...`. The numbers
  moved to module scope so `flameHit` could share them; the bounds are unchanged and it now also
  pins that `flameDraw` takes its scale *from* them.
- My own "why this was removed" comment names `lockAlert`, and a bare substring search read that
  comment as the bug it documents. Tightened to the call.

> ⚠ Section 229 was first appended **after** `process.exit(1)` on line 10356 and silently never ran —
> the assertion count moved for unrelated reasons and it looked fine. Then it crashed on a missing
> `ctxv` argument to `vm.runInContext`. Both were caught only by grepping for the section header in
> the output. This is CLAUDE.md rule 3 exactly: check that the section actually ran.

## Probes

`probe_flamebox.py` (hitbox vs drawn column, both weapons, + sounds + beep),
`probe_fireorb.py` (charge, home, commit, exit),
`probe_reaverpal.py` (what the reaver actually fires, and in what colour).
