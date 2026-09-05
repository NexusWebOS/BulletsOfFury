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

### Still owed from Mike's 17-item list — ⚠ RE-CHECKED 0905k: **TWO**, and both only half
**2. Cutscene shootdowns** — ✅ **DONE (0905e motion, 0905m art).** All three hostiles are now
front three-quarter pseudo-3D, generated as edits off their own top-downs to the cinematic_ships
pack's contract, so hostiles and hero ships share one perspective language. 48 credits.
⚠ **THE OLD PATHS WERE LEFT ALONE.** The three keys borrowed LIVE gameplay sprites from stages 5
and 8 (9, 16 and 8 sibling frames, referenced elsewhere in game.js). Overwriting those to fix a
cutscene would have silently restyled stage-5 and stage-8 enemies mid-fight. New files under
`cinematic_ships/hostiles/`, keys repointed.
**4. Stage-4 miniboss remake** — ✅ **DONE (0905h helpers, 0905i attack frame).** The unit is the
OLIVE WARDEN, not blacksteel. Muzzles and projectiles already existed and were already wired;
only the attack frame was missing. `summoned` now derives from `drones.length`.
**5. Stage-4 boss helper projectiles** — ✅ **DONE 0905c.**
**7. The laser telegraph** — ✅ **DONE (0905h timing/sign/sound, 0905p the lane plate).** The
sign was his own `nwarn_yield`/`nwarn_alert` and cost nothing; the lane plate cost 12.
⚠ **THE 'WHITENING' THAT BLOCKED THIS FOR TWO DROPS WAS GEOMETRY, NOT A MYSTERY.** Measured: the
hull spans y -43..193 and the TL/C/TR mounts sit at y 50..61, so a lane running 640px DOWN from
its mount crosses ~140px of the boss's own body. The fillRects always drew that overlap at
alpha 0.30-0.55 (a glow); the first plate cut drew it at up to **1.0** via a stray `*2.2` and
simply painted over the ship. Same alpha as the fillRects now, plus a ramp across the overlap.
⚠ **AND THE A/B THAT 'PROVED' IT WAS MEASURING ANIMATION.** Two arms captured seconds apart
differ across the WHOLE FRAME — terrain scroll, rain, the dialogue typing on — and a near-white
count over a fixed box picks all of it up. CLAUDE.md already records that same-state frame
isolation is impossible here (the draw reads `performance.now()` directly). **An amplified
difference IMAGE showed it in one look; the number never could, and had me report a mechanism
I did not understand as if it were established.**
Still Mike's call: whether the 3s warn should apply to every beam on stages 2-3 or only the big
ones — one constant.
**17. Stage 3** — ✅ **DONE 0905e.** The attacks and proc3 projectiles were already there; the
defect was the TELEGRAPH wearing the lava boss's red over ice. `L23_ALERT` is per-family now.

### Art in the tree that nothing draws yet
- ✅ **ALL SIX ARE DRAWN. This entry is CLOSED (re-measured 0905n).**
  `crystalimpact`, `prismbeam`, `ricochetimpact` landed in 0905j. `flakburst` and
  `omegabomb-reflected` were already wired before today.
  ⚠ **AND SO WAS `gravityripple` — 0905k's claim that it was 'the only one left' WAS WRONG.**
  It is the gravity mine's `under` layer (`FIRETYPES.s6gravity.under`, drawn at 33128 with
  `underScale:2.6`), so it renders beneath every mine. Measured live in phase 2: **16,196 ripple
  draws against the mine's 17,132**.
  ⚠⚠ **THE MISTAKE WAS THE AUDIT, AND IT IS WORTH MORE THAN THE ITEM.** The 0905k grep excluded
  every line matching `'s6mb_'+` to filter out the two import tables — but that is exactly how
  a real draw site builds its key (`'s6mb_gravityripple_'+(...)`). **The filter that hides the
  registration tables also hides every concatenated draw**, which is the same blind spot that
  left `omegabomb-reflected` on this list. Grep for the family NAME with no prefix filter, then
  read the hits; or better, count `XART.get` keys in a live run, which cannot be fooled either way.
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

## 0905h — items 4 and 7, the halves that cost nothing

**BOTH ARE PARTIAL. The behaviour is in; the SpriteCook art is not, and is what remains.**

**4. Stage-4 miniboss — the helpers are gone. The art run is not done.**
*"it should no longer get its helpers either"* — done and verified. The unit is the **OLIVE
WARDEN** (`olivewarden`), not the Blacksteel Raptor; CLAUDE.md said stage 4's mini was blacksteel
and that is stale — blacksteel moved to stage 6.

⚠ **THE HELPERS WERE BUILT AT INIT, NOT SUMMONED MID-FIGHT.** `stage4WarfareInit` pushed two
chaingun drones for the mini; the `drones` MODE only revealed them. So hiding the mode would have
left them alive and shooting. They are removed at the source, and `summoned` is now DERIVED from
`drones.length`, so the reveal, the draw and the 300px collision broad-phase reach all switch off
together — three consumers, one fact, none can be missed.

⚠ **THE `drones` PHASE IS KEPT.** It still runs the Warden's own wall attack on its 5.2s beat, so
the fight keeps its rhythm. Verified in real Chromium: 0 drones ever, `summoned` never true, reach
never opened, all three modes still entered — **and peak 24 rounds in flight**, which is the check
that matters: removing a unit's helpers by accidentally disarming the unit looks identical to
success on a probe that only counts drones. `_BUILD_SOURCE/probe_warden_helpers.py`.

**Still owed on item 4:** *"use spritecook, get proper attack frames, muzzle frames, projectiles
etc."* — an art run, Mike's credits, his direction.

**7. The laser telegraph — timing, symbol and sound are in. The field view is not.**

⚠ **THE ALERT SYMBOL HE ASKED FOR ALREADY EXISTED.** *"an alert symbol of OURS"* — `nwarn_yield`
and `nwarn_alert` are the same authored 165x153 triangular sign in yellow and red. Rendered to
find them, not picked by name (`docs/proofs/warden_helpers_0905/_alert_candidates.png`). That half
of item 7 cost no credits at all.

`L23_WARN_T` = 3.00 (his number), `L23_WARN_RED` = 0.60 for the yellow→red flip, blink accelerating
3→8Hz into the release, and an escalating alarm on its own slower cadence so it does not buzz.

⚠ **`L23_WARN_T` LENGTHENS EVERY BEAM ON STAGES 2 AND 3** — warms authored at 0.14–1.00s all become
3.00. That is a balance change wearing a feature, and it is ONE number so Mike can scope it to the
big beams if the Reaver's short jabs should stay short.

⚠⚠ **THE SIGN WAS DRAWN, ON SCREEN, CORRECTLY SIZED — AND INVISIBLE, THROUGH THREE GREEN PROBES.**
Worth reading before writing another draw-side check:
  1. a probe asserting the draw ASKED FOR the art key passed — true, and it proves nothing;
  2. a pixel probe passed on 4,254 "red" pixels that were the **RIME WALL name text**, not the sign;
  3. a `ctx.drawImage` trap caught **zero** blits — because **`ctx` carries its OWN `drawImage`**
     that shadows `CanvasRenderingContext2D.prototype`. Trapping the own property found 26 blits at
     world (352,46) under a scale-2/tx-200 transform = canvas (504,92): exactly where it should be.
The cause was DRAW ORDER, twice. It ran inside `l23BossBeamDraw`, which draws BEFORE the boss hull,
so the hull painted over it; and the boss GAUGE, later again in the HUD pass, owns the top ~39px.
It now draws in `drawWorld` AFTER both hulls, floored at `L23_WARN_MINY` = 46 to clear the gauge.
**Only a screenshot ever showed this. Occlusion is not off-screen, and a state check cannot tell
them apart.**

**Still owed on item 7:** *"that ugly field view before a laser comes out needs to be remade via
sprite cook"* — the LANE plate under the beam, which is the ugly part. Art run, Mike's call.

## 0905i — item 4 art, and the item-7 lane that is NOT wired

**4. The Olive Warden has attack frames. DONE.**

⚠ **ONLY ONE OF THE THREE THINGS ITEM 4 ASKS FOR WAS ACTUALLY MISSING.** *"proper attack frames,
muzzle frames, projectiles etc."* — the muzzles (`s4w_muzzle_mg/orb/lightning`, 8 frames each) and
the rounds (`bfx_legion_`, `s4w_spread_round_`, `s4w_mg_round_`) **already existed and were already
wired**. A manifest grep says 0 `s4w_` keys registered and that is a FALSE NEGATIVE: game.js
registers them at runtime into `XART._src`, and **221 files sit in `assets/game/stage4_warfare/`**.
Checking the directory before generating saved roughly 128 credits of art we already own. Rule 1.

What was genuinely missing: the mini set **no `_animKey` at all**, so it drew a static hull while
the Storm Sovereign cycles its flight/charge/energized reels. `nsb_olivewarden_attack` is one
generated plate (16 credits, `edit_asset_id` off the hull, silhouette IoU **0.933**, 18px clipped).

⚠ **DRIVEN BY THE WALL ATTACK, NOT BY EVERY ROUND.** Keyed to each MG shot it never expired — the
gun cycles every ~0.064s against a 0.16s flash — so the Warden sat in the firing pose permanently
and the idle hull was never drawn once (**measured 930 attack / 0 idle**). On the wall beat it now
measures **20% of frames in the firing pose** across a full mode cycle.
⚠ **GATED ABOVE 0.62 HP.** `_animKey` OVERRIDES the damage plate in `shipBossDraw`, so an ungated
attack frame visually HEALS the Warden whenever it fires at critical health. Verified: at 20% hp,
173,280 critical-plate frames and **zero** attack frames.

**7. The lane plate exists, is registered, and is DELIBERATELY NOT WIRED.**

`nwarn_lane` was generated (12 credits) and it is a real improvement in isolation — a tapered
corridor with hot rails and marching chevrons, against three flat translucent trapezoids with plain
white edge lines (`docs/proofs/laser_telegraph_0905/BEFORE_lane_fullframe.png`).

⚠ **BUT DRAWING IT WHITENS THE BOSS HULL, AND THE MECHANISM IS NOT UNDERSTOOD.** Controlled A/B —
patrol disabled so both arms hold the same x, one redraw before the capture, identical warm k:
**hull near-white 22.3% with the plate against 3.4% with the fillRects**, 35,453 differing pixels in
the hull band. Nothing in the source keys a hull tint on `_l23Beam`. A telegraph upgrade is not
worth a boss that washes out, so the draw stays procedural and the plate waits.

⚠ **AND THREE EARLIER ATTEMPTS TO MEASURE THIS WERE ALL INVALID, IN THE SAME WAY.** The boss
PATROLS. Two arms captured at the same k are at different x, so a fixed sample box compares
boss-present against boss-absent — one run reported "48.6% vs 1.3%, my change caused it" and that
was measuring an empty crop. **Pinning the position is not enough either: the canvas holds the LAST
DRAWN frame, so a pin must be followed by a step before the capture.** Both are now in the note
above the block.

## 0905j — crystalimpact, prismbeam, ricochetimpact

Mike: *"we also need crystalimpact, prismbeam and ricochetimpact"*.

⚠ **ALL THREE WERE ALREADY ON DISK AND ALREADY REGISTERED. NONE COST A CREDIT.** They came in with
the CF_DoomsdayCarrierAttacks-Lvl6 pack in 0904aa, and that drop's own note says so: *"Seven are
not referenced yet - ricochetimpact, crystalimpact, flakburst, clusterburst, gravityripple,
prismbeam, omegabomb-reflected ... registered anyway so the draws that want them can be written."*
8 + 6 + 8 frames in `assets/game/s6_carrier_attacks/`. This was a WIRING job, not an art job.
⚠ A manifest grep finds none of them — they are registered at runtime into `XART._src`. Second time
today that a manifest-only search would have led to buying art the repo already owns.

**Rendered before wiring** (`docs/proofs/s6mb_unused_0905.png`): crystalimpact is a cyan crystalline
burst, ricochetimpact an orange spark burst, and **prismbeam is a 40x104 TILE, not an impact**.

**prismbeam + crystalimpact are ONE feature, and the naming says so.** A tile needs a beam to live
in, and the pack ships the other two parts: `prismmuzzle` as the emitter head, `crystalimpact` as
the cap — exactly the head/tile/cap shape `S9_BEAM` already uses, where the warp sentinel's cap is
called `warpcrystalimpact`. So the carrier gets a **PRISM LANCE** built from the existing S9 beam
machinery (the tick+draw are gated only on `_s9Beam`, so they were already generic — no new code
moves light down the screen).

⚠ **THE BEAM FRAME COUNT HAD TO BECOME PER-PART.** The draw indexed head, tile and cap alike with a
hardcoded `%8`. Every stage-9 family is 8 frames so that was invisible — but **prismbeam is SIX**,
so two frames in every eight would have resolved to nothing and the beam would have strobed.
`hn/tn/cn` default to 8, so both stage-9 entries behave identically.

⚠ **THIS IS A FIGHT CHANGE, SCOPED TO THE CARRIER'S FINAL PHASE.** The phase-3 rotation went `%3`
-> `%4` and nowhere else; phases 0-2 are untouched. It charges on the head plate before it burns,
so it is telegraphed. Moving or removing it is one branch.
⚠ **AND `M.phase` IS DERIVED FROM HP EVERY TICK** (`ratio>.75?0:...`), so forcing `_mega.phase`
does nothing — a probe must drop the boss below 25% hp to reach the last phase at all.

**ricochetimpact** goes where ordinary fire hits the carrier and is NOT on a bay — previously a
0.08 flash and nothing else. It makes a real event visible and teaches the bay mechanic: shots
spark off, warheads are the way in. Additive; no damage or return value changed.
⚠ **AND IT MUST NOT USE `explode()`.** That is the enemy-DEATH routine and brings a shock ring,
debris, white flash and smoke — the first cut answered a bullet bouncing off with a full death
explosion, grey smoke over the hull and **20,930 reel lookups**. `navalFlash`, which the carrier's
other impacts already use, gives the same reel at **1,650** — 12.7x lighter and it reads as a spark.
⚠ **`carrierPlayerHit` RETURNS AT THE SHIELD BRANCH WHILE THE SHIELD IS UP**, so a probe that does
not drop `_bayShield.up` never reaches this code and measures zero.
