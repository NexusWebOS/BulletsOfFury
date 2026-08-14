# Passover 0811l — the banking channel, enemy separation, and a six-drop spelling gap

Two things were owed from `PASSOVER_0811_HANDOFF.md` §2.1. Both landed. A third turned up on the
way and is much larger than either.

Suite: **2,491 assertions / 220 sections / 5 failures.** Baseline was 2,463 / 218 / 4. The +28 is
fully accounted for: 2 new assertions in section 213, 8 in the new 213b, 18 in the new 213c.

---

## 1. The banking channel — the thing that was actually blocking

`jetTick` derived a jet's lean from the x it **actually moved**:

```js
const _vx=(e.x-(e._px==null?e.x:e._px))/Math.max(1e-4,dt);
```

That is the better signal right up until something outside `jetTick` touches x — and then it is the
worse one, because an external push and a deliberate turn become the same number. It is why the
0811i separation attempt rolled every jet it touched and why *"a straight jet never leans — it is
dead level south"* went red. The assertion was right.

It now reads the heading the aircraft **chose**:

```js
const _vx=_hx*_spd;
```

`_wx` already carries the route, the dodge and the lane-hold, so every deviation the jet picks for
itself still leans — a jet breaking off your missile rolls into the break exactly as before. What
it no longer carries is displacement the aircraft never asked for.

⚠ **`enemyEntrySweep` had already hit this same wall and worked around it** by excluding routed
jets outright (its own comment says so, and ends "For one suite run, that something was me"). That
exclusion is a symptom of the missing channel, not a fix. It can now be reconsidered on its merits.

**The source assertion that pinned the old expression is gone**, replaced by a behavioural one:
shove a jet from outside `jetTick` exactly the way `enemySeparate` does — position and lane
together — and its lean must stay at **0.0000 rad**. That pins both halves of the channel at once.
This is the "assertions can defend a bug" rule: the old one could only ever fail the change it
existed to protect.

---

## 2. Enemy separation — built, measured both ways, and visible

`enemySeparate(dt)` runs once per frame after every mover and after the dead are culled, held under
`_tslow` with everything else.

Three rules, and the last two are what let it push harder than the reverted nudge did:

1. **Half each, out the short side.** Two air units may take the Y exit when Y is the shallower
   overlap; anything on the ground or the water only ever moves sideways, because its Y is its
   station in the world and its movement model is written against it.
2. **A deadzone.** Waves are authored in formation and some touch by design — the bomber echelon at
   `(VW*0.08+i*12, -32-i*68)` overlaps by 0.04px on Y and counted as a stacked pair every frame it
   was on screen. Under 20% burial nothing moves.
3. **The terrain still owns the unit.** A tank is re-checked against `tankDrivable` and a boat
   against the land mask before it may move; a unit the terrain refuses hands its whole share to
   its partner. Without this the pass reintroduces "tanks into the water" from a new direction.

### Measured — `probe_stack.py`, seeded, both arms in real Chromium

| stage | arm | pair-frames | worst | **settled** pair-frames | **settled worst** |
|---|---|---|---|---|---|
| 1 | off | 933 | 71.6% | 837 | **50.3%** |
| 1 | ON  | 848 | 63.3% | 760 | **20.0%** |
| 4 | off | 160 | 150.7% | 160 | **150.7%** |
| 4 | ON  | 335 | 73.3% | 319 | **52.4%** |

### Two things about that table are worth more than the numbers

⚠ **THE WAVES ARE SEEDED NOW, AND THE OLD BASELINES WERE NOT COMPARABLE.** An unseeded pair of
runs moved the sep-OFF stage-1 count between **839 and 424** — a bigger swing than anything
separation does. The handoff's recorded 839 / 71.9% was one sample of a noisy distribution, and
tuning against it would have been tuning against luck. `probe_stack.py` now stubs `Math.random`
with a fixed LCG before `beginStage`, so both arms field the identical battle.

⚠ **`worst` IS A MAX OVER 1800 FRAMES AND CANNOT DISTINGUISH "STACKED" FROM "SPAWNED TOGETHER".**
Two units appearing on the same point pin it near the metric's ceiling on the single frame they
appear, however fast they are then pushed apart — which is why stage 1's worst barely moves under a
working pass and why 71.9% was never a reachable target. The new **settled** columns only count a
pair once both units are half a second old. That is the number that describes what Mike is looking
at, and it is the one that halved and then halved again.

⚠ **Stage 4's pair-frames ROSE, 160 → 335, and I do not have a verified cause.** The plausible one
is that units which used to be coincident (and counted once) are now adjacent (and still count on
this metric's generous 0.42 box), plus units surviving differently once they are not sharing a
hitbox. It is a hypothesis, not a measurement. The settled-burial figure is unambiguous and the
pixels below agree with it, so it is recorded rather than explained away.

### Seen — `probe_stack_shot.py`, new

Nine stage-1 units dropped into a 40px box, the same pile-up in both arms, photographed off the
live canvas after `drawWorld` ran on the same frame:

```
docs/proofs/separation_0811l_off.png    77.7% burial — one indistinguishable camo blob
docs/proofs/separation_0811l_on.png     19.9% burial — nine readable aircraft in formation
```

⚠ **The first cut of that proof was 100% EQUIPPED box.** It copied `shoot.py`'s three-canvas
composite but drew each canvas stretched to `#screen`'s size, so `#equipcv` covered the entire
frame and no game was visible at all. One look caught it. `#hud` and `#equipcv` are separate
elements at their own sizes — they are not layers of the play canvas.

---

## 3. ⚠ STAGES 4 AND 6 HAVE BEEN FIELDING 26x26 ONE-HP JETS THAT NEVER FIRED

Found while chasing stage 4's 150.7% pair, because the probe was made to report **which two units**
rather than just a number. It named a `s1jetBomber` with a **26x26** box. That is the default, not
a jet.

Drop 0810p repointed stage 4's and 6's dead jet waves onto "units that EXIST" and spawns
`s1jetDelta` / `s1jetBomber` / `s1jetDeltaB` / `s1jetBomberB`. `S1_JETS` and `NEF_S1` are keyed
`s1jetdelta` / `s1jetbomber` / `s1jetdelta_b` / `s1jetbomber_b`. **Every one of those lookups
missed**, and the units fell through to the generic defaults. Measured at runtime, side by side:

```
s1jetdelta   ->   95x105   hp 6   pattern s1jet   spd 96   atk mg      FIRED 90 rounds in 6s
s1jetDelta   ->   26x26    hp 1   pattern sine    spd —    atk NONE    FIRED 0
```

CLAUDE.md has carried the line *"⚠ BOTH SPELLINGS ARE REQUIRED. Stage 1 fields `s1jetdelta` and
stage 4 fields `s1jetDelta`"* the entire time. **The requirement was written down and never met, and
nothing failed because nothing asked.** It is the "systems declared and never fired" family again,
and this one has been live for six drops.

**Two separate mechanisms had to be fixed, and finding only the first would have looked like a fix
while changing nothing visible:**

- the three appliers (`applyS1Tank` / `applyS1Jet` / `applyNefUnit`) missed their row, so the unit
  got no box, no hp, no speed and no attack;
- `_selfPat` is looked up with the **spelling**, not the resolved row — so even with the row found,
  the generic block below would have overwritten the `s1jet` pattern with a random `sine`. The
  standing `_selfPat` trap, reached through the spelling gap instead of a missing row.

`rosterKey(type)` normalises case and underscores across all three tables; exact hits always win.
Driven from the tables, never hand-listed, so a fifth spelling cannot reintroduce this. A silent
collision would be worse than the bug, so the index keeps the first key it saw and records the
clash in `_rosterDup` — **measured: no collisions across all three tables.**

⚠ **This makes stages 4 and 6 materially harder.** Their jets go from 1-hp drifting squares to
6-hp aircraft with machine guns and missiles flying authored routes. That is what 0810p intended in
writing; it is still a real difficulty change and it is **Mike's call whether the waves now want
re-tuning.** Reverting is one line — drop the `rosterKey` resolution at the applier handoff.

⚠ **`probe_types.py` reported `shoots=3` for these units the whole time.** `shoots:true` is in the
base literal for every enemy, so that column measures a flag, not rounds. It cannot see this class
of bug. `probe_spelling` counts what lands in `eBullets` instead.

---

## 4. The suite's fifth failure — attributed, not assumed

*"every volley fired is 5-8 rounds"* failed on both runs, with different values each time
(`6, 4` then `5, 3`). The handoff lists it as flaky. Flaky-and-failing is not proof of innocence,
so it was attributed directly: the same fixture, seeded, run with the pass off and on.

```
sep off   volleys=8   in-range=True   boat drifted 60.8px
sep ON    volleys=8   in-range=True   boat drifted 60.8px
```

**Identical.** Separation does not touch it — the boat drifts the same 60.8px either way, because
nothing overlaps it in that fixture. Not attributable to this drop. It is, however, now failing
more often than "flaky" suggests and deserves its own look: the fixture spawns one boat but runs
the live stage plan around it for 14 seconds, so its volley grouping depends on whatever else the
stage decides to field.

---

## 5. Free finds

**The two 404s at boot are identified** — CLAUDE.md has listed them as unknown for weeks:

```
GET /assets/data/ui_layout.json     404
GET /assets/fonts/BlackOpsOne.ttf   404
```

Neither is fatal (the BOF font is the single face now, per 0809), but `ui_layout.json` is worth a
look before the stats-screen alignment work — a UI layout file that 404s is a plausible reason a
screen renders correctly in Python and wrongly in the browser.

---

## 6. Still owed, unchanged

- **Boats on water (§2.2)** — untouched. `probe_stack` still reports **779/779 and 781/781 naval
  samples ON LAND** on stage 1. `pickWaterX` is *not* in the tree; it was reverted along with its
  call sites, so it has to be rewritten, not just re-called. The handoff's diagnosis stands: solve
  once, on the first frame the boat is actually on screen (`y > 0`). `sepLandRef()` is new and gives
  you the stage's land mask in the right terms for it.
- **The pop-in predicate (§2.3)** — untouched.
- **The bridge (§2.4)** — untouched.
- **Per-enemy hitboxes** — untouched, and stage 4's 52.4% residual is partly this: burial is
  normalised by the smaller box, and a 26x26 box on a unit drawn far larger inflates it.

## 7. New tools

| tool | proves |
|---|---|
| `probe_stack.py` (rewritten) | scope first, then a **seeded** A/B with a settled-burial column and the worst pair NAMED |
| `probe_stack_shot.py` | the same pile-up off and on, as two PNGs off the live canvas |

`probe_stack.py` reports `typeof enemySeparate` before any measurement, because it is declared in
the region of `game.js` where `DEAD_SUBBOSS`, `ARSENAL_DRONES` and `liveType` all turned out to be
function-scoped inside `spawnEnemy`'s never-closed `if`. A separation pass that is never called
measures exactly like one that does not work. It reports **REACHABLE**.
