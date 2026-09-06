# PASSOVER 0906 — Mike's overnight list

Mike, going to bed: *"I have to go to bed. You have a large large large list, you have my full
approval to make a run through all these fixes, changes, adjustments etc. when done, you may commit
to my folder locally AND upload to the github."*

This is what got done, what it cost, and — more usefully — the eight things that were **not** what
they looked like.

---

## 1. THE TRAPS. Read these before the fixes.

### ⚠ A RECON'S NUMBERS CAN BE THE RIGHT MAGNITUDE ON THE WRONG FRAMES

The session opened holding a change I had already applied: `lizzie:1` added to `SHIP_BANK_FLIP` and
`SHIP_TWIST_FLIP`, on a recon that measured her `pv0/pv1` as nose-RIGHT and `pv3/pv4` as nose-LEFT.
The 0801dj survey in the file disagreed, listing her with the pilots that need no flip.

Re-measured all nine pilots off `bof_player_ships_barrel_rolls.png` in one pass, nose-vs-body ink
centroid normalised by hull width:

| | pv0 / pv1 (LEFT input) | in the flip table? |
|---|---|---|
| axel, decker, freezer, yuri | nose **RIGHT** +0.14…+0.28 | yes — correct |
| cole, falva, juggernaut, maverick, **lizzie** | nose **LEFT** −0.11…−0.35 | no — correct |

**The metric reproduces all four existing entries before it touches the disputed one.** That is the
only reason to believe it. Lizzie's real numbers are pv0 −0.113 / pv1 −0.112 / pv3 +0.073 /
pv4 +0.060 — the recon had the −0.11x pair on the wrong frames. **Both additions retracted.** My
change would have inverted a pilot that was working.

Two side findings:
- **Cole is correctly absent** from `SHIP_BANK_FLIP` even though 0801dj's note lists him among
  "FIVE PILOTS" at +7.66. That figure is a principal-axis ANGLE, a different quantity; his nose
  measures −0.271. Four entries is right, the prose is stale.
- The 0903y survey row for lizzie has pv0 and pv4 **both negative**, which no other pilot does —
  they are the same hull banked each way and must oppose. Corrected in place, with the reasoning,
  so the next reader does not re-derive the same wrong conclusion a third time.

The gravity-mode half of the same complaint **was** real and stands. `ship_bank_l1/l2/l3` carry the
nose swung RIGHT (+0.150/+0.183/+0.183) and `ship_bank_r*` swung LEFT (−0.153/−0.192/−0.123), and
the six `_blue` palette masks agree in sign on every frame — the cross-check that matters, since a
metric artefact would not flip consistently across two independently cut sets. This path
short-circuits the per-pilot flip system entirely, so it was wrong for **all nine pilots** on
stages 5 and 9.

### ⚠ A COMMENT CAN DESCRIBE A CHANGE THE CODE NEVER RECEIVED

`stage4WarfareWall` carried a nine-line note saying the wall "FIRES MACHINE-GUN ROUNDS NOW" — and
line 13840 still passed `'spread'`. The note had also **inverted the two role names** it was
explaining (it said the role "was 'mg'", mapping to the blue lightning bolt; `stage4WarfareShot`
maps `'mg'`→`s4brass` and `'spread'`→`s4rail`). A confident comment is not a measurement, and this
file already says so about a different one.

### ⚠ EIGHT BARE-LF LINES IN A CRLF FILE, FROM AN EARLIER EDIT IN THIS SAME SESSION

`game.js` is 58,318 lines of CRLF and had exactly 8 LF lines, contiguous, at 13824–13831 — the
comment block above. It defeated an exact-match edit and would have shown as a spurious 8-line diff
on commit. **Audit the line endings after any scripted edit**, not just the syntax.

### ⚠ A BOSS'S HIT RECTANGLE CAN SWALLOW THE SHOT THE FIGHT DEPENDS ON

This is the whole of Mike's *"stage 6 boss - completely broken. Horribly broken."* Measured in real
Chromium, sweeping one warhead down the screen and firing a single round at it:

```
warhead y   bossHitTest   deflected
   300         true          NO
   320         true          NO
   340         true          NO
   360         true          NO
   380         true          NO
   400         false         yes
   420         false         yes
```

The Doomsday Carrier's hit rectangle is **640×320 on a 680-wide world** — the full width and the top
three quarters of the screen — and the player-bullet loop collides with the BOSS about 200 lines
before it reaches the omegawarhead deflect. So every shot aimed at a warhead above y≈390 was
absorbed by the hull, and because Mike's own bay rule makes the bays immune to ordinary fire it did
**nothing**: `hitBoss` ran and the HP did not move (7408 before, 7408 after). Deflecting a warhead
is the only way to damage a bay. The entire fight was compressed into a ~50px band just above the
player's own ship, against a round accelerating into them.

**Found by trapping the write.** Three earlier guesses (the `_shootable` block above it, the omega
bomb art not being registered, the bays' own hit test) were all wrong and all plausible. A
`defineProperty` setter on `pb.dead` that records `new Error().stack` named the line in one run:
`game.js:27874`, inside the boss collision. This file already says "trap the write" for the tank
displacement; it is the same tool.

### ⚠ AN EIGHT-FRAME REEL IS NOT NECESSARILY AN ANIMATION OF WHAT ITS NAME SAYS

Mike: *"chainguns on helpers need to rotate 360 degrees to appear spinning."* Rendered and measured,
`s4w_helper_dual_00..07` has consecutive-frame silhouette IoU of **0.937 to 0.995** — one plate with
an energy-glow flicker, barrels dead still in all eight. Cycling it faster could never have fixed
it. `s4w_final_chaingun_00..07` **is** a real rotating gatling (min IoU 0.800), has been registered
and warmed since the pack landed, and was **drawn by nothing**. Authored art that had never reached
the screen.

⚠ **And rotating the whole `dual` plate would have been wrong**, which was the obvious move: its
barrels hang BELOW the housing, so a true 360° turn points them at the sky for half the revolution
while the rounds still leave downward — tumbling, not spinning. It would also have destroyed the
45° aim tell drop 0903r built at Mike's request.

### ⚠ PLACE A SPRITE FROM THE PLATE, NOT FROM THE FIRING OFFSETS

First cut hung the gatling off `stage4CoreTurretTip`'s `(±36, +51)` — where ROUNDS leave, not where
barrels are drawn — and sized it by eye. Rendered: one oversized gatling across the housing with the
plate's own barrel still poking out beside it. Measured off the plate instead (alpha threshold on
the bottom band so the two clusters separate): clusters at plate x 33..50 and 111..128, centres
**±39**, **18 wide**, running y 100..128 with the muzzle on row **128**. The fire point at row 131
is three rows *below the art*, which is why it cannot place a sprite.

### ⚠ `spawnBoss(kind)` TAKES AN ARGUMENT, AND BARE IT BUILDS THE GENERIC HULL

`spawnBoss()` with no argument gives `kind: undefined`, `name: ''`, and no `_s4war` rig — which
reads exactly like "the stage-4 boss has no helpers". Same family as the `spawnSubBoss__inner`
note already in CLAUDE.md. Cost one probe round trip.

### ⚠ A PROBE THAT HAS ONLY EVER BEEN GREEN IS NOT EVIDENCE

`probe_s5_scroll_0906.py` passed on the fixed build. That proves nothing on its own, so
`STAGE5_SPACE_CRUISE` was temporarily set to 0 and the probe re-run: **39/39 stalled samples in all
three phases**, then restored. It also carries stage 6 as an in-run control, which is known-good
since 0904t.

---

## 2. WHAT LANDED

### Ship turning
- `gravityModeDrawShip` — atlas side letter inverted; fixes all nine pilots on stages 5 and 9.
- `SHIP_BANK_FLIP` / `SHIP_TWIST_FLIP` — lizzie **retracted** (see above), notes corrected.

### Stage 4 miniboss (Olive Warden) — Mike's three asks
- **Attack frames off.** `b._animKey=null`; `nsb_olivewarden_attack` stays on disk. `S.fireFlash`
  went with it — it existed only to drive that line and was then written twice, decremented every
  frame, and read by nothing.
- **Dual MG spread turrets.** The burst alternated one round from R then one from L at a 0.07s
  cadence, which reads as a single stuttering gun; both barrels now fire every beat at double the
  interval — 2 per 0.120s = 16.7/s against 1 per 0.064s = 15.6/s, **+7%**, so the pair is legible
  without a difficulty change. The wall was an eleven-column fan from the CENTRE mount while the two
  barrels sat silent; it is now five columns from each of L and R, 8 rounds against the old 8.
- Wall rounds finally changed from `'spread'` to `'mg'` (the code the old comment claimed).

### Stage 4 boss (Storm Sovereign)
- **Helpers hold WORLD lanes**, not `camX + 72` screen lanes. ⚠ The offset is *solved*, not picked:
  a world x is visible at every camera position iff it lies in `[W−VW, VW]`, so the old 408px
  spacing is impossible in world space — one helper would sit off-screen, alive, shooting and
  unkillable. Centred on the world, half that band less a margin, gives **±128**: lanes at 212 and
  468. Verified at three camera positions: identical x, both on screen. Cost, stated plainly: the
  lanes are 256px apart instead of 408.
- **Rotating barrels** — `s4w_final_chaingun_*` on both sockets, riding the same `reelSpeed`
  accumulator, so it idles slowly and whirls through the burst.
- **Bigger rounds** — helper chaingun `szMul` .80→1.20, boss burst .78→1.10, final gun .82→1.12,
  the three blue-lightning volleys 1.18→1.52, 1.22→1.58, 1.68→2.05.
- **Shield-hit cue** — `shieldHitLight` → `shieldHitHeavy`. ⚠ I cannot hear either; this is the best
  available pick from two existing authored samples, not a judgement of how it sounds.
- **The tilt is zeroed at source.** `S.poseRot = dir*sin(...)*1.05` is a **60° roll** on the boss
  Mike sent a screenshot of. `shipBossVisualPose` already stopped reading it, so nothing changed on
  screen — but a live 60° assignment is a loaded gun for whoever reconnects `poseRot` next.

### Stage 5 — "DO NOT STOP SCROLLING"
Three separate causes, all reading as one defect:
1. `_bossHold` freezes `mapScroll` for a boss/miniboss — the bug 0904t fixed on stage 6 and did not
   carry across.
2. `mapScroll = Math.min(range, …)` **caps** at the plate end; a looping master has no end, so space
   stopped for good.
3. the launch brake eases to a standstill right before the gravity conversion.

Fixed with `STAGE5_SPACE_CRUISE` / `_stage5SpaceScroll`, an uncapped visual clock advanced inside
`drawLevelMaster` — which still runs while `updatePlay` early-returns, so space keeps moving through
the beats that freeze gameplay. **The rate is deliberately the level's existing 40 px/s, not stage
6's 260**: he asked for it not to stop, not for it to be faster. Stage 5 also gains
`continuousBoss:true` — it was the only `loopMaster` stage without it, so the arena branch still
fired despite the 0825 rule ("STAGES 5-8 NEVER CHANGE TERRAIN MAPPINGS FOR A BOSS") and the cfg's
own comment both saying otherwise.

### Stage 6 boss
The warhead now outranks the hull for a player shot (see the trap above). One definition
(`carrierWarheadDeflectOne`), two call sites — the eBullets loop asks "did any player round touch
me", the pBullets loop asks "did I touch any warhead"; the same test from opposite ends, and they
were about to be two copies of eight lines.

### Falva
Two flank-pinned balls firing straight up → **one** orbiting ball firing a **spread**. The orbit is
Axel's own `performance.now()/440` clock and direction so the two helpers read as one family; the
fan is the player's own spread geometry at n=5 / 0.28 rad. ⚠ **The 45° frames Mike asked for are
not needed and baking them would be worse** — the `flaser` branch already rotates the plate to the
round's velocity, so a bolt at any angle points along it; baked ±45 frames would quantise the fan to
three directions.

### Cinematics
`HQ_HOLD` (0.80s) — a completed line is unskippable for that long. ⚠ **Measured from line-COMPLETE,
not beat-start**: a lockout counted from the beat would be satisfied by the typing itself on exactly
the long lines that need the pause most. A tap during typing still completes the line instantly;
what it must not do is dismiss text nobody has seen. Nothing was running away — `Input.tap` is
edge-triggered and `Input.mouse.down` is cleared on use, both checked — but this is a shmup and the
fire button gets mashed.

### Shadow orb
The launch cue runs 2.250s and **peaks at 1.805s**, reaching −6 dB only at 1.170s. 0903q cut the
impact and its own note already recorded the launch figure — measured, written down, not acted on.
Re-cut by the same rule (60ms ahead of the −6 dB crossing, 4ms fade, −1 dBFS): 1.140s, −6 dB at
60ms, −3 dB at 135ms. Original untouched; one line reverts it.

---

## 3. STILL OPEN

Not started, and each is its own job:

- **The three-state attack-range cone** (green 25% idle / yellow prep / red imminent, hazard sign
  separate) for all bosses. Needs SpriteCook art. Recon located the current arrows at 14614–14626
  (`nwarn_lane`), no shared indicator, stage-7 danger columns painted GREEN against the vocabulary,
  and a dead `bossTelegraph` duplicate at 29362.
- **Stage-4 boss**: pixel glow on the energy sections, attack warnings, and blue lightning more
  often once the shield is down (the rounds are enlarged, the *frequency* is not changed).
- **Stage 6 raptor** — vertical, scaled down, 16-bit.
- **Purple halos on stages 5/6**, and the procedural polygon hulls ("MS-paint triangles") in
  `shipBossDraw`.
- **Entrance size snap** — `playShipPose` (54019) returns ≈73–82.5px while PLAY blits at
  `SHIP_DRAW_H = 60`, a ~21% pop on GO (27% for Yuri). Stages 5/9 have a separate 76.1→48 drop.
- **Cinematics, the creative half** — comic panel treatment, enemy snapshots, SpriteCook dialogue
  windows, the two approved cutscene modes, and new dialogue content. That last one needs Mike's
  voice; bring a draft, do not invent plot.

## 4. SUITE

Baseline before this drop: **3,226 ok / 65 fail** (3,291 attempted). The observed flake band is
64–67 and a ±2 count change is not evidence of anything — compare failure NAMES against a clean
worktree, never totals.

Two assertions were repointed deliberately rather than "fixed":
- the four falva ones pinned **two** balls on flanks, a spec Mike replaced outright;
- the approved-0829 sound ledger pinned `reviewed_shadow_orb_launch.wav`, i.e. the late sample. The
  0903q drop hit the identical situation on the neighbouring line and resolved it the same way. **An
  approved-mapping table defends the sample, not the requirement.**
