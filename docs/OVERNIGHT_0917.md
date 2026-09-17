# Overnight 0917 — what was built, what to look at first

Mike's brief: *"Go into auto work mode overnight and do not stop. continue improving my boss and
enemy AI, toy around with the weapon combination system and surprise me with some fun upgrades ...
Begin wiring up text for when you kill enemies ... I'll see you at 8am."*

Everything below is committed locally on `main` and **not pushed**. Every item has a Chromium probe
that drives the real game and a section in the suite; the failure names against the `9f64e731`
baseline were byte-identical on every full run (the two documented order-dependent flakes aside).

## Play this first

1. **NEW GAME +** — SELECT MODE shows a sixth row only after a real final campaign clear. Pick it:
   the campaign hub opens with `run.ngplus` set, and DARK MATTER infusions can drop.
   (`docs/NGPLUS_0917.md`)
2. **Infusions** — an element pickup (hex badge) layers on whatever gun you hold. Nine elements,
   three levels, level 3 named: FIREBURST, GLACIAL STRIKE, GODS WRATH, PRISM WAVE, ERADICATION,
   SONIC WAVE, MIRROR SHELL, GEYSER, VOID. Rounds wear the colour on the MG, spread, chaingun, laser,
   missiles and the orb. (`docs/INFUSIONS_0917.md`)
3. **GODS WRATH** — lightning level 3, a kill can strike every hostile from the sky. ⚠ This was
   invisible on the first build for a reason that was NOT the one I first wrote down — see §6 of the
   infusion doc. It shows now (`docs/proofs/infusion_0917/12_gods_wrath_bolts.png`).
4. **FUSION** — hold a level-3 element and pick a different one: THERMAL SHOCK, NAPALM, HYDRO VOLT,
   TESLA MIRROR ... the screen detonates once, then the new element takes the gun.
5. **Kill points** — every kill floats `+N` in the stage face, pops, and settles; 1,000+ is bigger
   and hotter. Kills within 1.2s chain: `+150 x3`, a quarter of the kill paid per chain step.
6. **HARD and up only:** ordinary jets sidestep your rounds (`EVADE_DIFF`), and the ship-boss lane
   patterns pick AGAINST where you are sitting (`BOSS_DENY_DIFF`). EASY/NORMAL are untouched.
   (`docs/ENEMY_EVADE_0917.md`)
7. **Giant beam** (kinetic on the laser), **sonic wave** (kinetic L3 on the MG), **water orb**
   (water on the orb), **void beam** (dark on the laser pulls hostiles into the column), **chromium**
   (mirrors enemy fire back), **cross-element geysers** (a soaked kill by fire/lightning).

## Things flagged for your call

- The NEW GAME + plate is wider than its family (5.23 against 3.4–4.5), so it reads shorter than
  its neighbours at the shared width. One SpriteCook job if you want it taller.
- The giant beam's muzzle orb scales with the beam and gets large at level 3.
- Infusion drop rate is `INFUSION_DROP_P` (0.05) per **drop-eligible kill**, rolled by `killDrop`.
  It used to sit behind the ordinary 18% loot gate, which made the true rate 2.3% — one per ~44 kills,
  and the sweep measured zero across nine stages. One number to turn now. Biased per stage
  (`INFUSION_STAGE_BIAS`); water needs the stage-9 signal, dark needs NEW GAME +.
  ⚠ How many drop-eligible kills a stage even offers varies a lot: measured over 120 s, stage 1 gave
  50 of 50 kills, stage 2 gave 28 of 43, stage 3 only 6 of 36. Stage 3 will always feel leaner.
- `EVADE_DIFF` / `BOSS_DENY_DIFF` numbers are first guesses: 0.30/0.55/0.80 and 0.50/0.75/1.0 for
  HARD/FURIOUS/INSANITY.

## Probes (all real Chromium)

| probe | result |
|---|---|
| `probe_ngplus_0917.py` | 15/0 |
| `probe_infusion_0917.py` | 31/0 |
| `probe_infusion_carriers_0917.py` | 14/0 |
| `probe_chrome_0917.py` | 10/0 |
| `probe_giantbeam_0917.py` | 10/0 |
| `probe_wrath_0917.py` | 5/0 |
| `probe_fusion_0917.py` | 9/0 |
| `probe_killpoints_0917.py` | 10/0 |
| `probe_evade_0917.py` | 11/0 |
| `probe_bossdeny_0917.py` | 8/0 |
| `probe_playtest_0917.py` | see below |

Suite sections 367 (infusions), 368 (NEW GAME +), 369 (evade + denial); 366 now also checks
`EVADE_DIFF` and `BOSS_DENY_DIFF` against every difficulty.

## The playtest sweep

`probe_playtest_0917.py`: every stage on HARD, a level-3 infusion held, trigger held, ship weaving,
45 simulated seconds each through the real stage loop, console read. Result recorded below when it
finished.

**First run (one page for all nine stages): 29 ok / 3 fail, and all three were the probe's.**
Stages 1–8: 0 page or console errors, 0 swallowed draw errors, the frame advanced every chunk,
178 kills, 106 evades, 6 infusion drops. The three fails: the drop counter was cumulative across
stages so stage 4's one drop "appeared" in the stage-5 and stage-9 controls (the gate itself is
proven: 400 stage-5 drops → 0 in the infusion probe); and stage 9 scored 0 kills with 0 rounds
because it inherited state from stage 8 through `SETUP` — stage 9 alone scored 45 kills with 975
rounds in flight. The sweep now opens a fresh page per stage and resets its counters per stage.

**What the sweep found that mattered:** the infusion drop roll sat behind the 18% kill-drop gate
and landed about once per 100 kills (2 in 300 measured) — raised to `INFUSION_DROP_P` 0.14.

**Second run (fresh page per stage): 29 ok / 1 fail across all nine stages, and the one fail was
the sweep asking for luck.** 0 page errors, 0 console errors, 0 draw errors swallowed by the state
draw, 0 stalled chunks, 2,700 frames every stage, 229 kills, 13 evades. Stage 9 — the stage that
inherited state through `SETUP` on the first run — scored 57 kills with 16,548 rounds fired, the
highest of the sweep. See `docs/proofs/playtest_0917/summary.json` and the `stage<N>_mid.png` frames.

**The one fail was `drops > 0`, and chasing it found TWO real bugs.** An eligible kill paid an
infusion about once in 44 on HARD (18% kill gate × `dropMul`, then `INFUSION_DROP_P` × `dropMul`),
so the sweep's eligible kills expected 3 and drew 0 — a one-night-in-twenty result, not a defect in
itself. Measuring the rate properly instead of re-rolling it is what exposed both defects
underneath: a stage the system could not reach at all, and a rate that was two numbers multiplied
where the code read as one.

### ⚠ Stage 8 could never drop an infusion, and the suite said it could

`infusionEligible()` refused any stage whose `bg` is `'space'`. **Three** stages wear that backdrop;
only 5 and 9 hand out the space guns. Stage 8 is an ordinary-weapon stage under space wallpaper, so
one ninth of the campaign quietly had no infusions at all — and `INFUSION_STAGE_BIAS` reserves
**prism for stage 8**, a bias that could never once fire.

The suite's own eligibility assertion passed the whole time: it moved `run.stage` and left
`curStage` alone, so the `bg` branch it was written to cover never ran. *A green suite proves state,
not pixels* — here it proved a variable the game does not consult on its own. The assertion moves
`curStage` with `run.stage` now, and a second one pins the prism bias to an eligible stage.

- **Fix:** the gate is the weapon set (`spaceWeaponsActive`) plus the explicit 5 and 9. `game.js`.
- **Measured** by the new `probe_infusion_rate_0917.py` — 4,000 real `dropPowerup` calls per stage:
  **stage 8: 0 → 513** pickups (expected ~530 at the time; every other eligible stage 478–577;
  stages 5 and 9 stay at 0). **16 ok / 0 fail.** ⚠ Those figures were taken while the roll still
  lived inside `dropPowerup`; after the second fix below the same probe reads **180–203 per 4,000
  on all seven eligible stages, 0 on 5 and 9, 16 ok / 0 fail.**
- **In real play:** `PT_STAGES=8` through the sweep — stage 8 reports eligible, 19 kills, and an
  infusion actually dropped. `docs/proofs/playtest_0917/stage8_mid.png`.
- The sweep no longer asserts on a 3-expected-event coin flip; it asserts what it can honestly see
  (the gate says yes in the live stage) and leaves the rate to the rate probe.

**Third run, with stage 8 eligible: 39 ok / 0 fail.** All nine stages again at 0 page errors, 0
console errors, 0 draw errors, 0 stalled chunks, 2,700 frames each; 215 kills, 11 evades, and **5
infusions dropped in ordinary play — three of them on stage 8**, the stage that could not drop one
the night before.

> ⚠ **THIS RUN STRADDLES A CHANGE TO `game.js` AND IS THEREFORE NOT A SINGLE-BUILD RECORD.** A
> second session was editing this working tree at the same time and rewrote the drop path at
> **08:16:01** — the `killDrop` funnel below. The sweep opens a fresh page per stage, so each stage
> loads whatever is on disk when it starts: **stages 1–2 ran the old roll** (0.14 inside
> `dropPowerup`, behind the 18% loot gate ≈ 2.3% per drop-eligible kill) and **stages 3–9 ran the new
> one** (`INFUSION_DROP_P` 0.05 rolled at the kill site ≈ 4.75%, about double). All five drops fell in
> the second window, which is consistent with both rates and proves neither. The error, frame,
> stall and eligibility columns are unaffected — those hold on both builds — but **the drop counts
> want one clean sweep on the settled build before they are quoted as balance evidence.**

| stage | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| kills | 27 | 19 | 20 | 19 | 14 | 22 | 7 | 31 | 56 |
| drops | 0 | 0 | 0 | 1 | — | 1 | 0 | **3** | — |
| eligible | yes | yes | yes | yes | **no** | yes | yes | **yes** | **no** |

Suite against a clean worktree at `5d74fa4f`: **4,748 ok / 59 fail** against the baseline's
**4,747 / 59**, failure names byte-identical, both runs reaching section 369. The one extra
assertion is the new prism-bias pin. ⚠ That pair was run BEFORE 08:16, so it measures the stage-8
fix alone; the `killDrop` refactor that landed afterwards has not been through a full suite. (⚠ `docs/qa/codex_takeover_0913_failures.txt` is four days
stale and differs from both trees in both directions — build the baseline, do not quote that file.)

### ⚠ And the drop rate was two probabilities multiplied where the code read as one

The infusion rolled *inside* `dropPowerup` — which the two ordinary death paths only reach through
their own `chance(0.18 * DIFF.dropMul)` loot gate. So the real rate was **0.171 × 0.133 = 2.3% per
drop-eligible kill**, one per ~44, and raising the visible constant (0.055 → 0.14) moved the outcome
hardly at all. Traced over 120 s of real play per stage: **129 kills, 84 drop-eligible, 18
`dropPowerup` calls, 2 infusions.**

- **Fix:** `killDrop(e)` — one funnel for both ordinary death paths. The infusion rolls on its own
  first, then the unchanged 18% ammo/shield/life gate underneath it. `INFUSION_DROP_P` (**0.05**) is
  now the per-drop-eligible-kill rate it claims to be, ~1 in 21. A forced `'infuse'` with an empty
  pool drops nothing rather than a pickup with no element on it.
- ⚠ **`dropOk` is not a property of "an enemy".** Over the same window stage 1 gave 50 drop-eligible
  kills of 50, stage 2 gave 28 of 43, and stage 3 only **6 of 36**. One per-kill rate reads three
  different ways on three stages — stage 3 will always feel leaner, by design.
- ⚠ The rate probe hardcoded `0.14` and failed all seven eligible stages the moment the model
  changed; it reads the live constant now.

## The showcase reel - and the three captures it took to get one worth watching

`_BUILD_SOURCE/capture_infusions_0917.py` films the system in one continuous stage-1 run: real
waves, real enemies, the trigger held, the element GRANTED on a schedule (a 5% kill drop would
leave most of the reel showing nothing) and everything after the grant live. 424 frames at 15fps,
all three canvases composited, encoded with `imageio_ffmpeg`.

    _shots/infusions_0917/BulletsOfFury_Infusions_0917.mp4           29.4 MB  (CRF 18)
    _shots/infusions_0917/BulletsOfFury_Infusions_0917_compact.mp4   12.0 MB  (CRF 26, sendable)
    _shots/infusions_0917/_contact.png                               one frame per beat, labelled

Beats: plain MG -> INCENDIARY -> FIREBURST -> GODS WRATH -> the giant beam (kinetic on the laser)
-> CHROMIUM -> the water orb -> FUSION.

**Each capture was rejected by its own contact sheet, and each rejection was a different class of
fault.** Read the sheet before believing the reel - none of the three was visible in a number.

1. **STAGE 2 WAS THE WRONG STAGE.** Its hulls are FIRE-typed, so ENG-12 absorbs half of every fire
   hit: INCENDIARY and FIREBURST rendered `FIRE DMG ABSORBED` instead of the weapon, and CHROMIUM
   had no enemy rounds on screen to mirror. Moved to stage 1 with enemy fire seeded for that beat.

2. **STAGE 1'S WATER SWALLOWED THE WATER ORB.** The orb and its shards are a pale ice-white and the
   ocean measures **98% blue-dominant at mean rgb 28/71/215**. `probe_waterorb_0917.py` (7/0) proved
   the orb was there the whole time - **239 orb-frames alive, every one `_inf:'water'`, 13,504 shard
   frames, the draw asking for `fx0825_ice_orb` by KEY** - in a picture where it cannot be seen.
   State right, pixels unreadable: 0905e's rule (*an alert must contrast with the FIELD, not match
   the beam*) applied to a showcase. `scan_stage1_bed_0917.py` sampled the live backdrop every 400px
   of scroll: **mapScroll 2400-3200 is 0% blue at mean rgb ~180/140/87**. The reel opens at
   `MAP_SCROLL0 = 2100` and every beat lands between 2133 and 3085, on sand. The shards read now.
   (It also cut the file by a third - animated water is expensive to encode.)

3. ⚠ **A LIVE INFUSION PICKUP HIJACKED A SCRIPTED BEAT.** The GODS WRATH panel came back with an
   orange badge in the EQUIPPED box and `TOXIC` typing across the screen: a real toxic drop had
   been collected mid-beat and replaced the granted lightning. The drop system working exactly as
   built, ruining the one thing the beat exists to show. Fixed twice over - the fed targets carry
   `dropOk = false`, and `PIN` re-asserts the beat's own element every captured frame (FUSION is
   deliberately unpinned, since trading the element away IS that beat).

⚠ **AND ONE PANEL LOOKED LIKE A BUG AND WAS NOT.** The CHROMIUM beat draws a thick white column
that reads as a laser still firing after the weapon switched away - it is the chrome-infused MG
stream, mirrored shells at the gun's own cadence. Zoomed to full size before it was believed; a
'the beam persisted' fix would have been a change to correct code.

**Open, and Mike's call:** water on the ICE ORB is close to a visual no-op - the orb is already
ice-blue and `INFUSIONS.water.body` is `#3fa7ff`, so the palette swap moves almost nothing. Water
reads on the mg/spread/beam, where the base round is not already blue. If the WATER ORB should look
distinct it needs its own body colour, not a swap of the ice plate.

