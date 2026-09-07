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

---

# 0906e — the standing pilots were already in the repo, and a size check called nine wrong ones right

Mike: *"and we do have the pilots on their own, from the cinematics we have. we use their frames
their. you can grab them from that."*

He was right, and the first version of the pilot screen had shipped without them.
**`pose_<pilot>_0..5` is fifty-four cut, background-free standing figures** on the `pilots_1` atlas
at 256x320 — six poses for every one of the nine — and the bay was drawing a portrait bust
captioned NO FIELD PHOTO for eight pilots because I had looked for a `_body_` family, found it only
on Yuri, and stopped. **Searching for the THING instead of for a NAME I had already chosen is the
lesson**, and it is rule 1 wearing different clothes.

## The traps, which are worth more than the fix

⚠ **A SIZE CHECK CANNOT TELL YOU WHOSE ART IT IS, AND IT SCORED NINE WRONG PILOTS AS 9/9.** The
first probe matched blits of 256x320 inside the bay rect and reported every pilot green. Every pose
cell is 256x320, so the size can say *"a pose"* and never *"whose"* — and the screen was in fact
drawing `pose_axel_0` for all nine, because the probe was setting `pilotIdx`, **a variable nothing
in the game reads** (it is `pilotIndex`, and `drawPilot` further overrides it with `pilotFrom`
while `pilotRot > 0.5`). Two independent faults, one green result. The probe now wraps `XART.get`
and records the KEY asked for — the identification route CLAUDE.md already prescribes, because
`XART.get` returns a fresh canvas with no `.src` and no stable identity — and it asserts the pilot
switch took effect instead of assuming it.

⚠ **AND YURI'S CINEMATIC POSES ARE ART MIKE REJECTED, SO ORDERING ALONE WAS NOT ENOUGH.**
`pose_yuri_*` is the previous Yuri — *"I never liked how Yuri turned out"* — and `yuri_body_0..6` is
the 0906 replacement. A chain that simply prefers `_body_0` still falls through to the old
character for the frames before it decodes, because `yuri_body_0` is a **loose file** and
`XART.rdy` is false on its first call: that call is what starts the load. The key-accurate probe
run caught exactly that. `PS_POSE_STALE` removes his pose set from the chain outright, so he shows
a bust for the decode window and then his own art, and never the replaced design for one frame.

⚠ **`pcStats` DOES NOT RETURN THE SAME NUMBER OF ROWS FOR EVERY PILOT, AND THE PANEL OVERFLOWED.**
Three rows for most, **five for Lizzie** (BOMB POWER, DEFENSE). A fixed pitch anchored to the panel
foot ran her last row 10px past the frame and printed DEFENSE across the roster below it. Found by
rendering all nine into one sheet — it is invisible on the eight pilots you would check first,
which is *"render the SET, not the complaint"* in one screenshot. The pitch is solved against the
room left now, opening to 22 when there is space and closing when there is not.

⚠ **AND MY OWN NEW ASSERTION FAILED ON CORRECT CODE, IN THE WAY THIS FILE ALREADY DOCUMENTS.**
Section 277 checks that the `NO FIELD PHOTO` caption is gone by reading `drawPilot.toString()` — and
the comment inside `drawPilot` explaining why the caption went **names the caption**. CLAUDE.md
records this exact shape from the 0810j connectors work ("the comment explaining what was removed
named what was removed"). Writing it again is the argument for stripping comments by default rather
than when you remember to.

## What landed

- **`psBodyKey`** resolves `<key>_body_0` → `pose_<key>_0` → `pose_<key>_3`, minus any pilot in
  `PS_POSE_STALE`. All nine bays draw a full standing figure; the NO FIELD PHOTO branch is gone and
  the bust survives only as the quiet decode-window fallback.
- **The info column flows.** The bio's real end drives what sits under it, the ship bay went
  86x78 → **126x120** (Mike asked for the spin to be a feature; it was smaller than the roster
  thumbnails), and narrowing the bio column to suit fills the top of the panel that the wide column
  had left empty. SPECIAL is pinned 26px above the first stat bar because it is that block's
  heading, not a third floating element.
- **`_BUILD_SOURCE/probe_pilotbody_0906.py`** — real Chromium, identifies by key, unlocks Cole so
  his bay is actually measured (a correctly-locked slot is not a missing figure), and reports the
  spin. **It can fail**: `--bust` stubs `psBodyKey` to null and the same run reports 0/9.
- **Suite section 277**, 12 assertions. **3,243 ok / 62 fail**, failure set identical to baseline.

Measured: 9/9 pilots draw a standing figure of themselves, 0 console errors, 0 page errors, and
Maverick's panel hull cycles all eight `br0..br7` over 240 frames while the roster stays level.
Proofs: `docs/PILOT_SELECT_0906.png` (all nine), `docs/proofs/pilotbody_0906/`.

## Also landed: Mike's three enemy bolt families, cut but NOT yet wired

*"I have much better projectiles to use for enemies, orbs, lightning, shadow bolts."* Three plates
share the flamethrower plate's 4x2 layout — the round in flight on row 0, a decaying impact on row 1
— and are cut by `_BUILD_SOURCE/import_bolts_0906.py` into `assets/game/bolts_v1/`:
`nbolt_{cyan,void,bead}_0..3` and `nboltx_{cyan,void,bead}_0..3`. Proof: `docs/BOLTS_0906.png`.

⚠ **THE FLAME IMPORTER'S DESPILL RULE WOULD HAVE DESTROYED TWO OF THE THREE.** `despill_fire`
clamps blue down to green, which is sound for fire (its ramp never has b>g) and catastrophic for
cyan, which is b>g by definition, and for the purple bolt, whose colour **is the key's own
signature**.

⚠ **AND THE SURVIVING KEY INK IS TWO DIFFERENT THINGS.** My first pass called all of it halo and
converted the ink's rim to a black edge per the standing rule — it moved **28 pixels on the cyan
plate and left 10,397**, because the lightning's branching arms ENCLOSE pools of background the
border flood cannot reach, and those are nowhere near an edge. Scoring every unreachable blob by
its distance from **the plate's own background pixel** separates the two populations with no
per-family list: 28 blobs (9,528 px) within 31, 967 blobs (5,180 px) at 48+, 9 in between. Still
background and ≥20px → punch; anything else → black edge, never deleted. That is what makes it safe
for the void family, whose art really is purple: its ink scores 67–90 and not one pixel is punched.
A hand-written "which families may contain magenta" table would have had to get that family right
on nothing but my say-so.

⚠ **THE BEAD ROW IS A SEQUENCE, NOT A LOOP** — frame heights 185 / 351 / 469 / 186, a 61% spread.
Looped it would pulse; it wants driving off the round's own clock, or using as power-graded
variants. Cyan (1% spread) and void (11%) are loops. The importer reports size BEFORE IoU for
exactly this reason: a low IoU means "crackle" or "growth" and those want opposite treatment.

**NOT WIRED, DELIBERATELY.** Which enemies and stages fire which bolt is Mike's call, and CLAUDE.md's
0905e note is explicit that the projectile resolution chain (`PROJ` → `_dedicated` → per-stage
FIRETYPES rows) must be read end to end first — that note exists because reading half of it put an
earlier drop one edit away from overwriting an authored design decision.

---

# 0906f — the SpriteCook pass: nine bordered avatars, nine front-facing pilots, six faction badges

Mike: *"now use spritecook and get me bordered avatars of each pilot, front facing frames of each
pilot like Yuri is facing forward and there affiliation symbols should be regenerated and used on
the cards."*

All three landed. **1,066 credits at the start, 802 at the end** — 22 generations at 12 each.

## The budget objection from 0906d is gone, and with it the composite

`build_pilot_avatars_0906.py` composited ONE lifted frame over nine portraits, and its own header
says why: 66 credits remained and a per-pilot edit is 12–18. Mike topped the account up, so each
pilot now gets a real generation — `edit_asset_id` on their own authored portrait, which is a 1:1
edit and not a lookalike. `build_pilot_avatars_v2_0906.py` supersedes it.

## What was measured rather than assumed

⚠ **THE PALETTE-LOCK RULE IN CLAUDE.md DOES NOT APPLY TO THIS ART CLASS, AND APPLYING IT WOULD HAVE
MADE THINGS WORSE.** That rule ("pixel:true does NOT give you pixel art" → snap to the reference's
palette) was measured on the Cryo Spear: an authored BOSS at **61 colours** against a 19,063-colour
generation, swapping in at 62% HP, i.e. an art-style change mid-fight. Measured here instead: the
authored portraits run **19,815–37,168** colours on opaque pixels and Yuri's own authored avatar is
**120,327**. These are continuous-tone illustrated plates, not low-colour sprites, and the
generations land at ~44,000–92,000 — inside that range. A lock would have flattened art that is
meant to be smooth and made the new avatars LESS like the authored ones. **A rule carries the art
class it was measured on.**

⚠ **AND THE RAW/PIXEL CHOICE INVERTS BETWEEN THE TWO JOBS.** CLAUDE.md says prefer `raw_url` because
`pixel_url` is crushed to the size hint — correct for the avatars, which are opaque. It is wrong for
the standing figures: measured, `raw_url` comes back **RGB with no alpha at all** on a flat white
background, and the cutout SpriteCook computed exists only on `pixel_url`. Re-keying the white
myself is the worse option here — **Falva's suit is white and Lizzie's near-white**, so the flood
threshold the emblems needed would eat into their clothing. Took the crushed plates (228–320px)
against a bay that draws at 95x212.

⚠ **SIX EMBLEMS FOR NINE PILOTS.** Two fly AIRFORCE, two are INDEPENDENT, two are PRINCESSES OF THE
SKY. A faction badge is worn by its members, so keying per pilot would have produced two different
Airforce badges and made the roster read as nine loners rather than six factions.

⚠ **AND THE TWO AFFILIATION TABLES DISAGREE ABOUT TWO PILOTS — OPEN, FOR MIKE.**
`BOFX.pilotcard[].affil` says **lizzie PRINCESSES OF THE SKY** and **cole THE RIGHT HAND MAN**;
`AINTRO_AFFIL` says **STRATEGIC ORDNANCE** and **FURY FOUNDER**. The emblem follows the pilotcard
table because that is what the CARD draws and the card is the surface he asked to change. Neither
of Cole's is a faction — both are titles — so his badge is built from his callsign, Forge Master.
**This needs his call**, and `affilEmblemKey` returns null for an unknown faction rather than
borrowing another one, so a decision either way is one table row.

⚠ **THE SIZE HINT BIT AGAIN, IN A NEW PLACE.** The eight bodies came back at eight different sizes
(228, 240, 240, 280, 282, 284, 308, 320). Scaling each CANVAS to one size leaves every pilot a
different height on screen, because the figure fills a different fraction of each. They are trimmed
to ink and scaled so the FIGURE is one height — and **Yuri's authored 273px sets it**, so the new
eight stand level with him rather than the reference being moved to suit the generations.

⚠ **THE EMBLEM INDENT IS CONDITIONAL ON THE EMBLEM RESOLVING.** `XART.rdy` is false on its first
call, so a fixed indent leaves the subtitle shunted right with an empty gap for the frames before
the badge decodes.

⚠ **AND MY OWN PROBE FLAGGED 8/9 AS WRONG ON A BUILD THAT HAD JUST GOT BETTER.** Its `DEDICATED` set
still listed only Yuri, so once the other eight had dedicated body art the probe called every one of
them a failure. Read the assertion before fixing the code: the expectation was stale, not the game.

## Yuri is excluded from both regenerations, deliberately

His plate is the reference. The gunmetal frame, corner bolt plates, accent bars, dark interior and
rim light in all eight avatar prompts are described FROM it, and `yuri_body_0` is the stance the
eight figures were generated to match. Running either back through the generator would replace
authored art with an imitation of itself. `PS_POSE_STALE` still keeps his superseded `pose_yuri_*`
out of the chain.

## Landed

- **`pav_<pilot>`** — nine bordered avatars, 256x256, each with its own `PILOTS[].tint` on the
  accent bars, so the roster reads as one set and each slot still says whose it is.
- **`<pilot>_body_0`** — nine front-facing figures on one 273px baseline. Lizzie and Falva were the
  two genuinely off-pose in the cinematic set and both now stand square.
- **`affil_<faction>`** — six badges, keyed by affiliation, drawn at the head of the card's subtitle
  row. White keyed by border flood at the anti-aliasing band (232), not at pure white: each plate is
  44–71% pure white with a further 100–800px of soft edge, and keying only >=250 leaves that as a
  halo ring. Proof is rendered on MID-GREY so a halo would show; on black it would not.
- Suite section 277 extended: every affiliation the card can print resolves to a badge, an unknown
  one draws nothing rather than borrowing, and the indent is conditional.

Proofs: `docs/PILOT_SELECT_0906F.png` (all nine cards), `docs/PILOT_AVATARS_V2_0906.png`,
`docs/PILOT_BODIES_0906.png`, `docs/AFFILIATIONS_0906.png`.

---

# 0906g — Lizzie's B-42 comes back as an unlockable costume, and it cost no art

Mike: *"store lizzie's old b-42 bomber sprites as an alternate costume pick if we use the password
bomber."*

## The art was never gone

0906b replaced her B-42 — *"As much as I like Lizzie's B-42 bomber, doesnt fit the game"* — and that
drop **appended** a strip to the ship atlas and repointed her rects at it. So all **seventeen** B-42
frames were still sitting in `bof_player_ships_barrel_rolls.png` exactly where they had always been,
unreferenced. Rendered before a line was written (`docs/LIZZIE_B42_RECOVERED.png`): hull, no-flame,
both banks, five pseudo-3D views and the full eight-frame roll — every one intact, 35–51% ink,
nothing overwritten. The rects came out of the manifest at `554dd4f2^`. **No art job, no atlas edit,
no regeneration.**

⚠ **AND THAT IS ONLY TRUE BECAUSE THE IMPORT APPENDED.** If 0906b had packed the new strip over her
old rows this would have been a regeneration instead. The rule this file already carries — *append a
strip, repoint the rects, pixels and manifest in one write* — is what made a costume free three
drops later. Worth knowing the next time a replacement looks like it should reuse the space.

## The swap is by RECT, not by key, and that is the whole design

⚠ **THERE ARE TWENTY-FOUR SITES IN `game.js` THAT BUILD A `'ship_'+pk` KEY** — the hull, the bank
picker, the roll reel, the launch cinematic, the pilot card, the roster thumbnail, allies, rivals,
the map icon. Giving the B-42 its own key family would mean teaching all twenty-four about costumes,
and the one that got missed would show the wrong aircraft on one surface with **nothing failing
anywhere**. That is `_selfPat` and the hand-written exemption list, in a new costume.

Repointing `BOFX.ships` and flushing XART's cell cache changes what every one of them resolves,
including any added later. Measured: the roster thumbnail changed with no edit anywhere near it.

⚠ **THE FLUSH IS THE LOAD-BEARING HALF, AND `lizzieSkinOn` CANNOT DETECT ITS ABSENCE.** `_shipCells`
is filled on first use and never re-read, so repointing alone changes the table and leaves every
draw showing the plate it already baked — state correct, pixels wrong, which is this file's most
repeated failure. `X._flushShipCells` exists for that one reason. And the flag is set by the same
function that does the repoint, so it stays true even if the flush is deleted: **the probe reads the
canvas XART actually serves, and the suite asserts on `BOFX.ships`, because neither can be satisfied
by the flag.**

⚠ **THE RECTS LIVE IN `game.js`, NOT THE MANIFEST.** `assets/manifest.js` is generated; a hand-added
table there is one regeneration from vanishing, and it would vanish **silently**, because the costume
is opt-in and nobody would be looking at it.

## Traps hit while building it

⚠ **THE FIRST HINT WOULD HAVE DRAWN TWO SPACES.** It read `B-42 BOMBER ▲▼ STOCK` — and the glyph map
has `25C0`/`25B6` (◀▶) but **not** `25B2`/`25BC` (▲▼), and a missing glyph in this engine draws a
space rather than failing. That is the 0903 stage-card bug (`CHOO E YOUR PILOT`) arriving from the
punctuation side. Checked the map rather than assuming, and the prompt is letters only, like every
other prompt on that screen.

⚠ **AND ITS FIRST PLACEMENT RAN THROUGH THE SPEED BAR AND OFF THE PANEL.** At `SHY+SHH+11` the bay's
foot is 208 and the first stat bar's top is 216, and a 27-character line at size 8 is wider than the
126px bay it was centred on — ~38px past the panel's right edge. **Lizzie is the five-stat pilot**,
so she has the least room under the bay of anyone, and the one card this could collide on is the
only card it appears on. Moved inside the frame, onto the 7px `psBlitFit` leaves below the hull.

⚠ **THE UNLOCK BANNER SAID `COLE UNLOCKED!` WHATEVER HAD BEEN UNLOCKED** — one flag drove it and one
string was baked in, so BOMBER would have lit a message naming a different unlock, which reads as
the code not registering. `unlockWho` is set alongside the timer at both sites.

## What landed

- `LIZZIE_B42_RECTS` — seventeen rows, recovered, in the file that uses them.
- `applyLizzieSkin(on)` — repoint + flush, both directions, stock rects captured live rather than
  hard-coded so it survives a re-import of the golden airframe.
- **`BOMBER`** unlocks it (session only, matching `COLE4U`; persisting a costume is a save-format
  decision Mike has not made). It is not also a stage code, so it cannot start a run by accident.
- **UP/DOWN on the pilot screen picks it**, gated on the unlock and on the pilot actually shown.
  `Input.menuUp`/`menuDown` exist and `drawPilot` read neither — checked, not assumed, because the
  generic back handler eating the rebind key in 0903 is exactly what that check is for.
- Suite section 278, 14 assertions. Probe `probe_lizzieskin_0906.py` reads the served canvas before
  and after, both ways, **and inside real PLAY on stage 1** — because "the rect swap is global so it
  follows" is a structural argument, and this file is a list of times those were wrong.

Proofs: `docs/LIZZIE_SKIN_0906.png` (stock vs B-42 on the card),
`docs/LIZZIE_B42_RECOVERED.png` (all seventeen frames as recovered),
`docs/proofs/lizzieskin_0906/lizzie_b42_inplay.png` (flying stage 1).

---

# 0906h/i — the ship and character pass: four ships, three characters, six badges, nine boxes

Mike's list, worked in two commits (0906h ships, 0906i characters). Credits 1,066 → 556.

## The measurements that decided things

⚠ **DECKER'S SWAP BREAKS THE LUMINANCE RULE, AND ONLY HIS.** Measured: his hull is 47% grey at
v≤0.25 and 18.4% in hue 30–60. Black and yellow sit at opposite ends of the value range, so
"palette/luminance swaps, not overlays" would leave the hull dark everywhere the black was and the
swap would be **invisible**. The two bands exchange their measured value RANGES instead of being
flat-filled, so each pixel keeps its position inside its own band and every panel line survives.
One pass over the original pixel — two passes would undo the first with the second.

⚠ **MAVERICK'S GREEN REALLY IS COLE'S GREEN.** 41% of Maverick's hull is hue 90–150; Cole measures
13% in 90–120. Teal at 177 clears the band. And he is moved on **every** surface — ship, 6 portrait
cells, avatar, standing figure, `PILOTS[].tint` — because a pilot whose ship is teal and whose card,
HUD and bars are still Cole-green has not been separated from Cole. `#8de23a` appears 37 times in
game.js and **36 are generic UI greens**, so exactly one row changed.

⚠ **THE PORTRAIT RECOLOUR DEDUPES BY RECT.** `port_maverick_idle` and `_smile` are the SAME rect.
This repo has ~750 aliased cells; iterating keys is how a rule silently double-applies.

⚠ **A GENERATED ROTATION SHEET FAILED FOR THE SECOND TIME.** 8×3 asked, 7×3 returned; row 2 came
back **nose-left**; row 1 is 3/4 perspective, not top-down bank; and connected-component analysis
found **20 components for 21 frames** because two pairs are drawn touching and merge into 870px
blobs against a ~360px ship. A grid slice would have cut ships in half. So both new reels are
**derived**: a barrel roll about the nose axis IS a horizontal cosine scale, which makes the roll
exact (widths 200/141/20/141/200/141/20/141 = |cos| at 45° steps) and correctly ordered, symmetric
and consistently lit by construction. **Bank angles measured off the authored ships** — Cole 0.94–1.00
of hull width (17–20°), Freezer 0.89–0.99 (19–27°) — so the new ships belong to the same fleet.
What is approximated is stated in the script: past 90° a real aircraft shows its underside and a
plate has none, so the second half is the mirrored plate darkened.

⚠ **LIZZIE'S BODY IS RECOLOURED, NOT REGENERATED — TWO ATTEMPTS WERE REFUSED.** `edit_asset_id` on
her standing figure returned `content_policy_violation` twice; rewording her build to "solid and
athletic" did not help. Rather than keep spending credits on refusals, her body takes a **measured
skin shift sampled from her new portrait** (saturation ×0.643, value ×1.330). The correction that
actually reads at the 212px the bay draws her at is the skin. Her build stays as authored — said
plainly rather than quietly dropped.

⚠ **AND FALVA'S ATLAS PORTRAITS NEVER HAD GREY HAIR — I PUT IT THERE.** Rendered the originals
before assuming: `port_falva_*` is auburn-brown throughout. The white streak Mike objected to
appeared in the AVATAR generated in 0906f and nowhere else. The instinct on "no gray or white hair"
is to sweep her whole portrait set for pale pixels, which would have eaten the white trim on her
flight suit to fix a defect that was not in those files.

⚠ **THE AVATAR BOX COLOUR IS MEASURED OFF EACH SHIP, NOT READ FROM THE TINT TABLE.** `PILOTS[].tint`
is close for most and WRONG for the three that changed this drop. The dominant hue is the saturated
ink's **circular mean weighted by saturation** — a plain average is dragged to grey by the gunmetal
every ship is mostly made of, and a modal hue picks whichever accent has the most pixels rather than
the colour the ship reads as. Result: axel 213°, decker 47°, maverick 182°, freezer 278°,
juggernaut 19°, yuri 355°, lizzie 29°, falva 333°, cole 108°.
⚠ **AND ONLY THE FRAME MOVES.** Skin sits at 0.18–0.75 saturation in the same hue band as several
of these tints, so a blanket rotation would turn faces blue for Axel and green for Cole. The
portrait window is excluded by geometry as well as by saturation.

⚠ **YURI IS NO LONGER THE STYLE REFERENCE — HE IS NOW THE ONE BEING MATCHED.** Through 0906f his
authored plate was passed through untouched because everything else was generated to match it.
Mike inverted that, so the special case is **gone** from the avatar builder rather than reversed:
he goes through the same slot as everyone else. His first restyle put him in a grey girder room and
lightened his hair; the retry pinned the flat near-black background and dark hair explicitly.

## Landed

- **Ships**: Decker's yellow/black exchange, Maverick teal, Juggernaut's new skull-free heavy
  gunship (widest hull in the fleet, mirror-IoU 1.000), Falva cleaned (symmetry 0.954 → 1.000,
  8,149 → 7,242 colours). Both new reels appended, never packed over the old rows.
- **Characters**: Lizzie fair-skinned and mature across her portrait set and body; Falva young with
  no grey; Yuri restyled to the others in avatar and standing figure.
- **Six faction badges regenerated with real colour** — blue/silver, violet/gold, crimson steel,
  furnace orange, magenta/gold, emerald/flame.
- **Nine avatar boxes tinted to their own ship.**

Proofs: `docs/SHIPS_0906G.png`, `docs/PILOT_SELECT_0906G.png`, `docs/PILOT_AVATARS_0906G.png`,
`docs/AFFILIATIONS_0906.png`, `docs/CHARS_APPLIED_0906G.png`, `docs/JUGGERNAUT_SHIP_0906G.png`,
`docs/FALVA_SHIP_0906G.png`, `docs/YURI_RESTYLE_0906G.png`.

## Still owed on this list

- **The cutscene emotion faces for Lizzie and Yuri.** Lizzie's six non-idle cells took the measured
  skin shift, which lands her ethnicity but not the mid-thirties read; Yuri's seven are still the
  painterly style. Both are generation jobs and neither shows on the pilot screen.
- **Juggernaut's character still wears a small skull medallion** in his portrait and on his boots.
  Mike asked for no death symbol **on the ship**, which is done — the character's own motif was not
  in scope and has been left rather than assumed.

---

# 0906j — Lizzie and Falva, rebuilt from their own authored cards

Mike: *"go look at falva and lizzies original pilot cards we have and re-generate avatar/actual
frames please."*

## He was right, and it corrects a drift I introduced

`card_lizzie` and `card_falva` are full authored pilot cards on the `pilots_0` atlas, 958x718 each,
with a large hero illustration and — on the `pcard_` variants — a **full standing figure**. Rendered
before anything was regenerated, and they settle two things I had been guessing at:

- **Lizzie on her own card is already the fair-skinned, curvy, mature woman Mike described.** The
  correction he asked for in 0906i was never a change — it was a request to stop drifting from art
  that already existed. Her gold suit has a harness, belt, thigh straps and a BOMBSHELL name tape
  that none of my generated versions carried.
- **Falva on her own card has auburn-brown curls**, not the near-black hair my 0906i regeneration
  gave her. The "no gray or white hair" note was about a streak I introduced; the fix was to go
  back to her card, not to darken her further.

⚠ **SO THE LESSON IS THE ONE THIS FILE KEEPS WRITING DOWN.** I had a character description from
Mike and generated toward it three times, drifting a little each pass, while a definitive authored
reference sat in the atlas under a key I never looked up. **Search for the art before generating
art.** `pcard_*` and `card_*` are twenty keys covering all nine pilots and a locked slot.

## What was used, and why the source differs between the two

- **Both avatars** are `edit_asset_id` on a head-and-shoulders crop of the authored card art, so the
  likeness is theirs and the frame is described to match the other seven.
- **Falva's body** comes from her card's hero figure (standing, arms crossed, leaning on her jet),
  restaged to arms-at-sides with the aircraft and background deleted.
- ⚠ **LIZZIE'S BODY COMES FROM `pcard_lizzie`, NOT FROM HER HERO ILLUSTRATION.** Her hero art is
  SEATED on a bomb rack, and it is also the source that got refused twice by the content filter in
  0906i. `pcard_lizzie` carries a **standing** full-length figure of her in the same suit, on a plain
  dark grid — a better pose reference and a neutral enough plate that the edit went through first
  time. Two problems solved by looking one key further along.

## Landed

`pav_lizzie`, `pav_falva`, `lizzie_body_0`, `falva_body_0` — all four rebuilt from the cards, then
put through the same normaliser as the other seven (figure scaled to Yuri's authored 273px baseline)
and the same box tinting (Lizzie 29 deg, Falva 333 deg, measured off their ships).

Proofs: `docs/ORIGINAL_CARDS_LF.png` (the authored cards as found), `docs/CARDCUTS_LF.png` (the
crops used as sources), `docs/CARDBASED_LF_0906J.png` (before/after on all four),
`docs/PILOT_CARDS_LF_0906J.png` (both finished screens).

**Not changed:** their `port_*` emotion cells. Those are a separate set and neither shows on the
pilot screen; the card-derived look now differs slightly from them, which is worth a pass of its own.
