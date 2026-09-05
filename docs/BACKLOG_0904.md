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

## DONE (drop 0904t)

**16. Stage 6 scroll + moon** — *"do not ever stop scrolling, do not place the moon there either."*
The SKY never stopped (measured: 260px/s in play, 300 during a boss) — the PARALLAX layer rode
`mapScroll`, which the engine deliberately freezes for a boss so the level stops advancing. Half the
background travelled, half stood still. On stage 6 it rides the sky's own clock now.
The moon was `bg6_moon_full` blitted FULL-SCREEN at 0.9 alpha across the night window — a
moon-sized wash over the playfield, not a body in the sky. Removed; the night tint is carried by
the master's own palette journey, so the opening is still night.

**10. Maverick's laser** — *"only targets one enemy instead of homing to whats in front of it."*
It re-acquires every frame, so it was never locking on — it picked by straight Euclidean distance,
so an enemy off to the SIDE beat one dead ahead the moment it was a few pixels closer. Lateral
offset now dominates the score 3x against forward distance 0.6x, and anything more than half a
screen off-axis is rejected outright.

**15. Volley missile impact** — *"bad, need correction."* It drew eighteen coloured dots and a faint
screen tint, with no authored frame anywhere, so a warhead landed weaker than a bullet. Now calls
the engine's own `nxp_clus` explosion (8 authored frames) with a second `nxp_dense` burst at
level 3+, sparks kept as decoration over a real frame.

---

## DONE (drop 0904v) — fonts

**9. Pilot select fonts + the stage fonts** — Mike supplied `CF_BOFStageFonts-Complete-Vol.2`:
ten authored bitmap families, 46 glyphs each, 96x96 cells, hard alpha. Nine per-stage faces plus a
FINAL LEVEL face.
This is the first set covering **stages 6-9** — the five card alphabets stop at stage 5, so GET
READY / 3-2-1 / GO on the storm, sewer, death and void stages had been drawing in stage 1's grey
jungle stone. All nine now draw their own.
The pilot screen takes the FINAL LEVEL face: it belongs to no stage, and the pilot screen belongs
to no stage either — keying it to the pilot's home stage made the heading change typeface every
time the player scrolled.
⚠ The pack has no `%`, `(`, `)` or `+`, and the stats screen draws a percent sign. stage 2's card
alphabet stays loaded as the donor and stageGlyph borrows from it. The build script REFUSES to
import if the donor cannot supply them.

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
**9. Pilot select fonts** — delete them, use the current stage fonts.
⚠ NEEDS A DECISION FROM MIKE BEFORE IT IS TOUCHED. Investigated and the obvious answer is wrong:
  - the card art (`pcard_<pilot>`) carries NO baked text — the panel is clean;
  - `drawPilot` already routes its own strings through `msgText`, with raw canvas text only as a
    fallback when the bitmap face has not loaded;
  - the card body already uses BOFmil, which a previous drop set deliberately after Mike asked for
    "our dialogue font" — its own comment says so;
  - and the STAGE screens use the same family: `'bold Npx "BOFmil", monospace'`.
  So "use the actual stage fonts" cannot mean the typeface — they already match. What differs in
  the screenshot is the FACE: the headers ("CHOOSE YOUR PILOT!", the pilot name) render through the
  bitmap `fury-dialogue-font`, while the card interior and the footer render as thin canvas BOFmil.
  Most likely Mike wants the card/footer on the bitmap face too. Worth one word from him rather
  than restyling the whole screen on a guess.

---

## Note on sequencing

The stage-9 cluster (11-14) is one coherent pass — fail state, return state, and roster. The two
SpriteCook items (4, 7) are one art run. Everything else is independent and can be picked off in any
order.

---

## DONE (drops 0904w-0904aa) — the 0904 art batch

**Chaos Harrier (0904w)** — no tilt (the banked hulls are never selected), three warps then a
stationary laser window, the wing cannons rebuilt as sustained beams off the authored `ch_lance_`
cannon art that nothing had ever drawn, and the phase-rift teleport FX imported.

**Stage fonts Vol.3 (0904x)** — the metric-locked remaster replaces Vol.2. The faces now carry
their own per-glyph `ride`, so the two-entry hand table from 0822a is a fallback. The pilot card's
interior is on the stage lettering. `stageText` gained a canvas last rung so a character in NO
face stops rendering as a space. The pack's 2x `fury-cutscene-font` was imported (never had been).

**The debrief screen (0904y)** — rebuilt to Mike's concept: title bar, pilot bay, mission brief,
six stat slots with the authored fills and the text ON them, SCORE / RANK, sign-off. Power-Ups
Collected and Weapon of Choice are NEW measurements. '=' is synthesised from the face's own hyphen.

**Stage 9 boss attacks (0904z)** — CF_BossAttacks-Lvl9 imported; both ship bosses' mounts corrected
from the pack's own anchors (the Sovereign's cannons were 37px outboard); five signature attacks
live. The Chaos Harrier's hardpoints were re-measured off its hull in the same pass.

**Doomsday Carrier (0904aa)** — CF_DoomsdayCarrierAttacks-Lvl6 imported. ⚠ Its 16 `s6mb_` families
were referenced by game.js and NONE were registered; the whole attack visual layer had been drawing
nothing.

### Still open on the 0904 packs
- The carrier pack ships **11 named hardpoints** and **six named boss cycles**
  (cyclone_barrage, prism_crossfire, omega_bomb_run, chrome_flak_fan, storm_cage, doomsday_fusion).
  Only the art is in; the mounts and the cycles are the next pass on that boss.
- Seven carrier families are registered but not yet referenced by any draw: ricochetimpact,
  crystalimpact, flakburst, clusterburst, gravityripple, prismbeam, omegabomb-reflected.
- The Stage 9 pack's beam heads + tileable bodies (Warp_CrystalBeam/Tile, Tidal_PressureBeam/Tile)
  and its impacts are imported but not yet wired to a beam act.
- `CF_Stage9PortalCombatPickups-Lvl9` (179 entries) and the remaining four teleport-FX families
  from CF_EnemyTeleportFX-Vol.1 are still unimported.
