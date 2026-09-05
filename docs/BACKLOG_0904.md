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

## QUEUED — pruned 0904am against the code, not against memory

⚠ THIS SECTION WAS STALE. It still listed items 8, 9, 10, 11, 12, 13, 14, 15 and 16 as open when
the DONE sections above record all nine as landed. Cross-checked before rewriting.

### Still owed from Mike's 17-item list — FIVE of them
**2. Cutscene shootdowns** — *"use our pseudo-3d graphics"* in the cutscenes where we shoot enemies
down.
**4. Stage-4 miniboss remake** — *"use spritecook, get proper attack frames, muzzle frames,
projectiles etc. it should no longer get its helpers either."* Art run + a behaviour change in its
tick to stop the helper spawns.
**5. Stage-4 boss helper projectiles** — larger. Small and isolated.
**7. The laser telegraph** — *"that ugly field view before a laser comes out needs to be remade via
sprite cook, and it should flash for 3 seconds on/off and an alert symbol of ours should pop up
above the enemy, go from the yellow to red with the sound"*. Art + behaviour + audio; the
1..2..3 / f.f.f telegraph from the earlier list belongs with this one.
**17. Stage 3** — *"where are the new attacks, projectiles and animations for him?"*

### Art in the tree that nothing draws yet
- **Six s6mb_ families** imported with the carrier pack and still unreferenced: `crystalimpact`,
  `flakburst`, `gravityripple`, `omegabomb-reflected`, `prismbeam`, `ricochetimpact`.
  `omegabomb-reflected` is the notable one - the deflect mechanic has a REFLECTED plate authored
  for it and currently redraws the hostile one.
- **The carrier's six named boss cycles** are art-only. Four already exist in spirit as the mega
  phases; what the pack adds beyond the anchors and the flak airburst (both landed 0904ae) is the
  exact authored geometry for the other cycles.

### Packs on disk, not yet imported
- `CF_Stage9PortalCombatPickups-Lvl9` (179 entries, PortalFill families) at `C:\s9p`.
- The four remaining `CF_EnemyTeleportFX-Vol.1` families - phase-needle, plasma-bloom,
  crimson-shatter, gravity-maw. Only the Chaos Harrier's phase-rift was taken.

### Decisions waiting on Mike
- **The 2x cutscene face** (0904x) is live on drawCutscene, cinDialogue and campaignIntroCaption.
  He sent the pack; he never asked for those surfaces to change. One accessor reverts it.
- **`cinDialogue` is now dead code** - it was the beats renderer for the retired pilot openings.
  Left on disk rather than deleted.
- **The debrief shows six stats, not nine.** MISSILES FIRED, MISSILE HITS, SPECIAL DAMAGE, SPECIAL
  HITS and CLEAR TIME were all asked for in 0807o; CLEAR TIME came back in the score row, the other
  four are off the screen because his concept has six slots. SC_CONCEPT plus a row count restores
  them as a 2x4 or 2x5 grid.

### Standing, from earlier findings
- The `cornerLR` / `curveR` pair and the stage-1 spawn fixture are FLAKY, not broken - they have
  swapped places on nearly every run this session. Do not chase them without a seeded harness.

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

---

## 0905 — worked while Mike rested

**Done**
- Seated HQ poses de-matted (26,571 px of enclosed white cleared across 7 files) and wired as the
  ensemble row, which drawCutscene's own comment has described as "seated" since it was written.
- Flak shell bursts with `flakburst` (0904ae had grabbed `clusterburst` - the pack ships one of
  each and clusterburst belongs to the bomblet).
- Gravity mine draws its authored `gravityripple` underneath, via a new FIRETYPES `under` slot.
- **Item 5** - stage-4 boss helper rounds enlarged: drawn x1.45, hitbox x1.18.

**⚠ A CORRECTION TO THIS DOC'S OWN AUDIT.** `omegabomb-reflected` was listed as undrawn. It is
drawn - line 16812 builds the key dynamically as `'s6mb_omegabomb-'+(ref?'reflected':'hostile')` -
and the audit regex only matched literal prefixes, which is the trap CLAUDE.md records for
n6x_/nvl_/s1_/tk*. The deflect mechanic has been correct all along. Genuinely undrawn now:
`crystalimpact`, `prismbeam`, `ricochetimpact`.

**⚠ LIZZIE'S SEATED POSE IS DAMAGED ART.** Her gloves, belt and sleeve panels are washed out to
pale opaque grey - whatever produced the file ate into the art rather than stopping at it. A matte
pass cannot help: deleting those pixels would punch holes in her. She needs regenerating, and is in
the cleaner's SKIP list so a later run cannot damage her further.

**Left on the list**
- Items 2 (cutscene shootdowns -> pseudo-3D), 4 (stage-4 miniboss remake), 7 (laser telegraph),
  17 (stage 3 attacks). ⚠ 4 and 7 need SpriteCook art - NOT started, because generating art spends
  Mike's credits and that is his call to make, not something to do while he is asleep.
- `crystalimpact`, `prismbeam`, `ricochetimpact` still undrawn.
- `CF_Stage9PortalCombatPickups-Lvl9` and the four remaining teleport-FX families unimported.
- HQ_ROOM's scene-to-room mapping is my reading of the scripts and is a creative call to review.
- 26+ commits unpushed.

---

## 0905e — items 2 and 17, on Mike's ask

**17. Stage 3 — the attacks were there; the TELEGRAPH was wearing the lava boss's colour.**
His words: *"where are the new attacks, projectiles and animations for him?"* Measured before
changing anything: the seven Rime Wall / Cryo Spear patterns and the `proc3` projectiles landed
0831 (58252627), i.e. BEFORE he wrote the list, and they do fire with authored `l23fx_cryo_/rime_`
art — so "where are they" was not a wiring question. What he was looking at is the laser tell:
I built the red alert field in 0903h for the LAVA boss (his note then was about level 2) and put it
in the shared `l23BossBeamDraw`, so stage 3 inherited a hardcoded `#ff0000` lane. Over cyan ice at
the opening alpha (0.35 × 0.55 pulse = 0.19) red does not read as red — blended with blue it is a
**brown smear**, which is what the Rime Wall has been telegraphing with.
`L23_ALERT` is per-family now. ⚠ **The fix is the ALPHA, not the hue** — swept five candidates on
the real ice field (`docs/proofs/stage3_alert_0905/_sweep.png`): an ice-blue lane vanishes into the
ice (the same mistake one step over), amber reads molten, magenta reads like a pickup. Red at a
higher opening alpha stays red on cyan, so an alert still means one thing everywhere. Stage 2's
values are byte-identical and shown unchanged in `_after.png`; stage 4's `legion` deliberately has
no row and inherits the shipped lava values rather than a guess.

⚠ **I nearly "fixed" something deliberate.** `PROJ` maps `s3shard`→comet / `s3mortar`→blast, which
default to the RED palette, and the mini's shards do look like fire on ice. That mapping is a
registry classification only: `_dedicated` routes any `s[1-9]` kind to its own FIRETYPES row, and
stage 3's rows carry `proc3` → `drawStage3Projectile`, authored silhouettes with a documented
reason ("dark violet silhouette and warm gold core so every round stays legible over white snow").
Changing the palette would have overwritten a design decision. Read the whole chain first.

**2. Cutscene shootdowns — the motion half is done; the ART half is Mike's call.**
His words: *"use our pseudo-3d graphics"*. The scenes are the per-pilot openings (`PILOT_OPENINGS`,
beats `dogfight` / `duo_attack` / `missile_lock` / `ram`), which **are live** — `hqTrigger('pre',1)`
plays them before stage 1 in campaign. ⚠ The comment above `HQ_SCENES` said they were "kept as data
and no longer played"; that was true when written and 0904an put them back. Corrected in place.

- ⚠ **The art does not exist and cannot be faked.** Our ships have seven authored 3/4 views each
  (`cinematic_ships/<pilot>/cutouts_native/`); every enemy plate in the tree — the stage-8 scout,
  the bone interceptor, the whole Vol.1 `xship` set — is TOP-DOWN. Rendered side by side in
  `docs/proofs/cin_shootdown_0905/_candidates.png`. Matching the hero perspective is a SpriteCook
  run, so it sits with items 4 and 7 as **Mike's credits, Mike's call**.
- **Landed without art:** `cinhostile_heavy` was registered and **unreachable** — `flip?[1]:[0]`
  can only pick two of three — so a third of the hostile art had never been on screen. Beats can
  name one now. And the four combat beats got the depth language the `hq_approach` / `depart` beats
  already use, so bandits close on the camera instead of sitting at a fixed size.
- ⚠ **The ram never showed what it hit.** Both airbursts were unconditional and drawn at the
  hostiles' own position at twice their size, so from frame zero the enemies Juggernaut rams were
  covered by their own explosions. They wait for the closing now. Before/after:
  `docs/proofs/cin_shootdown_0905/_before.png`, `_after2.png`.

**Still needs Mike**
- **Item 2's art** — hostiles in the hero ships' 3/4 view (SpriteCook).
- **Stage 3's miniboss has one plate.** `nsb_cryo_spear` has no damaged/critical, so the CRYO SPEAR
  never visibly degrades; every other ship boss and mini that has them declares a `dmg` array. The
  art is not on disk — also a generation job.

Suite **3,214 ok / 67 fail / 278 sections**, thirteen of those assertions new (§275, §276) and all
passing; nothing failing outside the baseline but the two documented corner-run flakes.
