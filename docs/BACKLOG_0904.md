# 0904 backlog — Mike's list, captured verbatim so nothing is lost

Seventeen items came in one message. Three were flagged urgent ("first things first", "immediately")
and are **done**; the rest are recorded here in Mike's own words with what each will actually take.

---

## DONE (drop 0904q)

**1. Shield impact sound** — *"shield impact noises should be the same as our impact noises, but
distort and pitch shift it please."*
`shieldImpact` / `shieldImpactHeavy` are hit()'s own recipe — 1400Hz square, 30ms, falling bend —
pitched DOWN a fifth and pushed through a waveshaper. Down rather than up because a shield ABSORBS;
the existing blocked-shot cue pitches UP to read as something refusing the hit. Same waveform
underneath, so the two stay related by ear.

**3. Raptor aerobatics OFF** — *"do NOT somersault and barrel roll unti lyou get the fraems you need"*
`RAP_AEROBATICS=false`. The machinery is kept and still probe-tested, so switching it back on when a
roll reel exists is one flag, not a rewrite. My 0904k reasoning was wrong: driving scale.x through a
cosine is a real manoeuvre for a sprite WITH roll frames and a squash for one without.

**6. Boss + miniboss attack audio** — *"wire up sounds for allmini bosses and boss attacks immediately"*
⚠ 22 of 24 boss patterns fired in SILENCE. Verified the central path first (having been wrong about
exactly this on muzzles): shipBossActionTick plays only a phase-change cue and _shipShot is silent.
Now raised at the same choke point as the muzzle flash, so the two can never drift apart, keyed to
the boss's ordnance family and rate-gated so a volley is not a wall of noise.

---

## DONE (drop 0904r) — the stage-9 cluster

**11. Fail + eject** — *"did not fail me on the stage and teleport me backk to stage 5"*
easy/normal carry `continues:-1` (UNCAPPED), which made the only eject branch unreachable for them.
`STAGE9_CONTINUES=1` caps the bonus stage regardless of difficulty.

**12. Return to stage 5** — *"did not bring me bac kto my exact positon ... nor showed me the water
gun pickup"*. There was no save at all; the return called `beginStage(5)` and replayed the level.
Entry snapshots the clock/scroll/wave, return restores it. The reward is Laser Mist and it was
already announced — during stage 9's boss death, one beat before the state left PLAY for the map,
so the banner was raised onto a screen that had gone. Re-raised on arrival in stage 5.

**13. Stuck whiteout** — the merge wrote `whiteBlast`, which the file itself documents as
"never self-decays". Moved to `atomFlash`, which fades in the play update.

**14. Unusable hulls** — `mini_warp_tank` (a tracked ground tank, in deep space) and `gate_carrier`
(the one hull my own tilt audit flagged at 145.7 degrees). Roster 10 -> 8.

---

## DONE (drop 0904s) — stage 5

**8. Sky -> space** — *"do not stop the scroling and use clouds so we dont see the connection but
feels natural like our player went up into space."*
⚠ The leg was ALREADY scrolling continuously and still read as stopping: it ramped 240 -> 1220px/s
then handed straight to PLAY, which runs at 40px/s. A thirty-fold drop in one frame is a wall, not
a continuation. The ramp now decelerates across the final phase and lands on 40.2px/s, so the
background is already moving at the speed stage 5 will move it.
The three backdrops meet on two hard clipped edges; a drifting cloud bank now rides each one,
densest on the join. The upper seam thins as the swirl takes hold — leaving the weather behind is
the altitude cue. First cut scattered clouds by hash and left a third of the seam bare; they are
stepped evenly across the width with jitter inside each step now.

---

## QUEUED

### Art-led (needs SpriteCook)
**4. Stage-4 miniboss remake** — *"use spritecook, get proper attack frames, muzzle frames,
projectiles etc. it should no longer get its helpers either."*
Same shape as the Herald remake: intact/damaged/critical + ordnance, aligned to one footprint on
import. Plus removing its helper spawns, which is a behaviour change in its tick.

**7. The laser telegraph** — *"that ugly field view before a laser comes out needs to be remade via
sprite cook, and it should flash for 3 seconds on/off and an alert symbol of ours should pop up
above the enemy, go from the yellow to red with the sound"*
Art + behaviour + audio. The 1..2..3 / f.f.f telegraph from the earlier list belongs with this.

### Behaviour / engine
**2. Cutscene shootdowns** — *"use our pseudo-3d graphics"* in the cutscenes where we shoot enemies down.
**5. Stage-4 boss helper projectiles** — larger. Small, isolated.
**8. Stage 5 sky→space** — *"you were supposed to connect space and sky, do not stop the scroling and
use clouds so we dont see the connection"*. Reopens 0903w/x; the scroll must never stop.
**16. Stage 6** — *"do not ever stop scrolling, do not place the moon there either."*
**10. Maverick's laser** — targets one enemy instead of homing to what's in front of it.
**15. Volley missile impact FX** — bad, need correction.
**17. Stage 3** — *"where are the new attacks, projectiles and animations for him?"*

### Stage 9 — a cluster, probably one pass
**11.** Losing all 5 lives + continue did NOT fail the stage and send us back to stage 5.
**12.** Returning to stage 5 did not restore the exact position, did not show the water gun pickup,
made no announcement.
**13.** Screen stays flashed white when the final boss merges.
**14.** Still has tanks and weird enemies that do not belong.

### UI
**9. Pilot select fonts** — delete them, use the current stage fonts. (Same complaint as the stats
screen in 0903; that one was fixed, this one was missed.)

---

## Note on sequencing

The stage-9 cluster (11-14) is one coherent pass — fail state, return state, and roster. The two
SpriteCook items (4, 7) are one art run. Everything else is independent and can be picked off in any
order.
