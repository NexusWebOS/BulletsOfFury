# BULLETS OF FURY — Passover / Handoff Document

**Studio:** ColeForge Studios · **Owner/Decision-maker:** Mike
**Type:** Single-file → externalized HTML5 canvas vertical shoot-'em-up
**Engine resolution:** 480 × 512 (letterboxed, integer-scaled)
**This build:** externalized folder build, ~125 MB, 90 corrected-art images, 19 SFX, 19 music tracks. Build passes the Node/vm harness with **0 errors**.

---

## 1. How to run it

The playable game is the `BulletsOfFury/` folder. Open `BulletsOfFury/index.html` in a browser (or serve the folder over http). Everything it needs is under `assets/`. No build step is required to *play* — the build step only exists to *regenerate* the game from source.

Controls: arrow keys / WASD to move, fire button (space/enter or the on-screen control), plus the on-screen menu flow (title → difficulty → pilot select → stage).

---

## 2. Current state (what works)

- **Boot → Title → Difficulty → Pilot select → Stage** flow is wired end to end.
- **Stages 1–5** are playable with per-stage backgrounds, enemies, bosses, fonts, cards, and music. Stages 4–5 are lighter (placeholder wiring in places — see §8).
- **Stage-entry sequence** (this session): card intro → transition cinematic → gameplay. Non-skippable transition.
- **Powerup containers**: per-stage crates (spinning) and pills, drawn from the items atlas.
- **Audio**: per-stage music (each stage reads its own `music` field), synth SFX.
- **Arcade cabinet UI frame** around the play area (marquee, side panels, wood/metal border).

---

## 3. What changed this session

### 3a. Missing "S" glyph in the stage fonts — solved
The packed stage-font row was generated as A–Z **minus S** (S was never produced as an official glyph). The game's glyph font is the small **"STAGE N" plaque font** on each card (not the big mossy title). Fix lives in **`add_stage_s.py`** (a post-build step): it hard-crops the leading "S" from the "STAGE N" plaque of each card (fixed boxes tuned per card), chroma-keys the letter, scales it to the **median cap-height** of that stage's letters, seats it on the same baseline (nudged up 2 px so it's centered and the same height as the other letters), and injects it into each stage atlas + manifest as `g_S`. Stages 1, 3, 4 get their own S; stage 2 already had one; **stage 5 is skipped** (falls back to the stage-1 S for now).

These bitmap fonts are also now the default for **stage start, ship-destroyed ("SHIP DESTROYED"), in-game messages, and the stage-clear score/credits** — each using the *current* stage's font, with stage 1 as the fallback for any glyph a stage lacks.

### 3b. Stage-entry cinematic — rewritten
Flow: `beginStage → INTRO (card) → LAUNCH (transition) → PLAY`.

- **Card intro** (`drawIntro`, gamecode.js): slam-in (thump = crash SFX + screen shake), torch/skull/ember FX, then **scale back out + screen fade** (no more slice/burn/shatter). Card is skippable; hands off to the transition.
- **Transition** (`B_LAUNCH` block in patches.js, `drawLaunch`): a **continuous filmstrip scroll — no fades, no cuts**. World regions are stacked by distance and physically scroll past: **pad → runway → terrain → liquid → level entrance**. Phases: `run` (launch off pad, up runway, over terrain, accelerating to 1750 px/s) → over the **liquid** (~5 s rapid; jungle = water, volcano = lava, ice = water palette-swapped icier) → the **level scrolls in from the top** and you speed a little past into it → `brake` (level keeps filling in) → `reverse` (backs up toward the start) → `cd` (**GET READY 3-2-1 → GO!** in the stage font). **Non-skippable.**
- The transition init is state-entry-robust (not timing-dependent), so a laggy first frame can't skip setup.

### 3c. Skull overlay
`drawCardFX` skull now draws **fully opaque** (removed the additive "lighter" blend and 0.9 alpha).

### 3d. Pilot select
On confirm, the pilot **card slides left and away** (name hides during the slide), then proceeds — replaces the old flash/split.

### 3e. Powerup boxes & pills — wired per stage
From `items.zip`. Crates are 4-frame spinning boxes; pills are single capsules. Current mapping:

| Stage | Crate (box) | Pill |
|------|-------------|------|
| 1 Jungle | `crate1` (jbox) | `pill1` (jpill) |
| 2 Volcano | `crate2b` (fbox2 — fire box **without** flames) | `pill2` (lavapill) |
| 3 Ice | `crate3` (ice, from `spin_ice`) | `pill3` (ice-pill) |
| 4 Sky | `crate4` (4box) | `pill_missile` |
| 5 Space | `crate5` (5box — chroma-keyed, halos removed, 4 frames) | `pill5` |
| 6 (classic, not built yet) | `crate6` (wooden, from `spin_gold`) | `pill_speed` |

All crates (`crate1`–`crate6`) now live in the **items atlas** (`bofx.json` → `assets/items/`). Crates spin through 4 frames (wooden `crate6` spins frames 0–2, frame 3 is its sunburst break-flash). Containers spawn during play (crate ≈ every 11 s, capsule ≈ every 17 s); shoot or touch to break — crate gives a weapon, pill gives speed (unchanged behavior). Spares still in the atlas but unused: `crate2` (fire-with-flames) and `pill_missile`/`crate6` only show once stages use them.

---

## 4. Architecture

The game source is **two layers** that get combined at build time:

- **`gamecode.js`** (~141 K chars) — the base engine: states, player, enemies, bosses, powerups, world/background rendering, `drawIntro`, `drawCrate`/`drawCapsule`, `msgText`, etc.
- **`patches.js`** — a set of `String.raw` blocks (`B_XART`, `B_PILOTS`, `B_BOOTSEQ`, `B_TITLE`, `B_DIFF`, `B_PW`, `B_LAUNCH`, `B_OPTIONS`, `B_STAGEEND`, `B_HUD`) that **`assemble.py`** splices into `gamecode.js` (via replace/insert), producing `gamecode_patched.js`.

**Important:** the `B_*` blocks are inside `String.raw` backticks, so **no backticks are allowed in inserted JS** — use string concatenation. Edit base functions in `gamecode.js`; edit the block bodies in `patches.js`.

### States (`GS`)
`BOOT, TITLE, DIFF, PILOT, PASSWORD, OPTIONS, INTRO, LAUNCH, PLAY, GAMEOVER, VICTORY, STAGECLEAR, CONTINUE, CREDITS`.
`state` + `stateT` (time in state). `setState(s)` resets `stateT`. `drawScene(dt)` dispatches by state.

### Key systems / functions
- **Flow:** `beginStage(num)` → INTRO → `proceedIntro()` → LAUNCH → `drawLaunch` → `finishLaunch()` → PLAY.
- **Player:** `player` object (`reset()` puts it at `y = VH*0.78`).
- **Backgrounds/liquids:** `drawBG(dt)` per stage. Liquids are frame arrays `ASSETS.water` / `ASSETS.lava` (from `BOF.waterFrames` / `BOF.lavaFrames`), tiled by `drawAnimTerrain`. Ice = water + icy tint.
- **Powerups:** `dropPowerup`, `spawnContainer('crate'|'capsule')`, `breakContainer`, `applyPowerup`; drawn by `drawPowerups` → `drawCrate` / `drawCapsule`.
- **Fonts:** `stageArt[stageNum]` holds each card's atlas + `frames` + `font` map. `msgText(text,cx,cy,H,tintC,tintA,alpha,spacingMul)` renders bitmap text in the current stage font (fallback stage 1). `curArt()` = `stageArt[String(run.stage)]`.

### Asset systems (three of them)
1. **`window.BOF`** — main atlas (`assets/atlases/main.png`) + `frames`, plus map images, `waterFrames`/`lavaFrames`, `cards`, `stageArt`. Accessed via `ASSETS.*` (`ASSETS.has/blit/dims`, `ASSETS.water`, etc.).
2. **`window.BOFX`** — "corrected assets": individual keyed PNGs. Accessed via `XART.get(key)` / `XART.rdy(key)` / `XART.draw`. **This is where the crates, pills, runway, pad, terrain, pilot cards, buttons, etc. live.** Source of truth is **`bofx.json`** (`key → {d: base64png, m: mime}`); `build_ext.py`'s `fold_for(key)` decides the output subfolder.
3. **`window.BOFA`** — audio (`sfx`, `music`).

---

## 5. Build pipeline (how to regenerate the game)

Working dir is `/tmp/build` (resets between sessions — the source in `_BUILD_SOURCE/` is the recoverable copy). Run **in this order**:

```
python3 assemble.py       # gamecode.js + patches.js -> gamecode_patched.js
node --check gamecode_patched.js
python3 build_ext.py      # decode BOF/BOFA/BOFX -> dist/BulletsOfFury/assets/*, copy patched -> assets/game.js
python3 add_stage_s.py    # POST-STEP: inject the 'S' glyph (MUST run AFTER build_ext, every build)
node /tmp/test_ext.js     # expect: "==== EXTERNAL BUILD OK, 0 ERRORS ===="
```

**Critical ordering note:** `add_stage_s.py` must run **after** `build_ext.py`, because `build_ext` regenerates the manifest and would overwrite the injected S otherwise.

Deliverable zip:
```
cd dist && zip -rq BulletsOfFury_FULL_GAME.zip BulletsOfFury -x '*/ships/_orig/*'
```

Headless test harnesses used this session (rebuild if the dir was reset): `/tmp/test_ext.js` (build integrity), `/tmp/test_trans.js` (drives the transition through all phases per stage), `/tmp/test_items.js` (crate/pill draw per stage). They mock `Image`/`Audio`/canvas in a `vm` context.

---

## 6. Adding new corrected-art sprites (the common task)

1. Extract the sprite as a keyed transparent PNG (chroma-key the background; for magenta use an r/g/b test, for purple/dark backgrounds key by distance to the corner color, then **edge-only despill** to remove color halos).
2. Base64-encode and add to **`bofx.json`** under a new key.
3. If the key needs a specific output folder, add a rule to `fold_for()` in `build_ext.py` (e.g. `crate*`/`pill*` → `items`).
4. Reference it in code via `XART.rdy('key')` / `XART.get('key')`.
5. Rebuild (§5).

---

## 7. Key learnings / gotchas

- The game glyph font = the **"STAGE N" plaque** font (matches the `g_` glyphs), **not** the big mossy title. Plaque letters are ~1 px top / 1–3 px bottom padding within their frames; round letters like S need a ~2 px upward nudge to look centered.
- `patches.js` `B_*` blocks are `String.raw` — **no backticks** in inserted JS.
- `ASSETS.water` / `ASSETS.lava` come from `BOF.waterFrames` / `BOF.lavaFrames` (arrays), **not** top-level `water`/`lava` keys.
- `assemble.py` uses string `replace` — a mismatch **silently no-ops**. Always confirm changes shipped (diff the output / `node --check`), not just that the script ran.
- Sprite extraction: connected-component or column-split, key by chroma **or** distance-to-background, then **edge-only despill** for halos. The `purplish=(r>g+4)&(b>g+4)` filter destroys silver/white-hot pixels — use distance-only keying for those.
- All stage fonts **except stage 2** omit the letter S in the packed row (hence `add_stage_s.py`).
- Transition/`drawLaunch` init is keyed to state entry (`stateT < lastT`), not a fixed time threshold, so it can't be skipped by a laggy first frame.
- `add_stage_s.py`'s S boxes are hard-coded per card — **swap a card and the S must be re-pointed** for that stage.

---

## 8. Pending / next work

- **Stage 5 "S" glyph** (currently borrows stage 1's).
- **Stages 4–5 liquids/terrain:** sky/space have no real liquid, so the transition falls back to water there and gameplay backgrounds are light. Needs proper assets.
- **Stage 6:** crate/pill mapping is wired and ready, but no stage 6 exists yet (game has 5 playable stages).
- **Weapons:** wire the laser and firewall weapons (FX extracted; gameplay integration pending). Weapon atlases (MG/missile/spread/laser/firewall lv1–5) in `incoming/BoF_Assets_Corrected/`.
- **Enemy rosters / bosses:** Levels 2–3 rosters (`lavaenemies.png`, `iceenemies.png`); wargod / spider / leviathan bosses.
- **Cinematic graphics.**
- **New difficulty modes + graphics; new pilot/plane selection cards.**
- **Spares in the atlas, unused:** `crate2` (fire-with-flames box), and `crate6`/`pill_speed`/`pill_missile` only appear when their stages exist.
- **`repairs.png` / `shields.png`** (small icon strips from `items.zip`) — not yet wired; look like HUD/repair icons.

---

## 9. What's in this zip

```
BulletsOfFury/
├─ index.html                     ← open this to play
├─ assets/
│  ├─ game.js                     ← compiled engine (gamecode + patches)
│  ├─ manifest.js                 ← window.BOF / BOFA / BOFX
│  ├─ atlases/  (main.png, stage1..5.png)
│  ├─ items/    (crate1..6, pill*, etc.)
│  ├─ ui/  ui/cards/  boot/  fx/  ships/  levels/  levels/terrain/
│  ├─ music/  sounds/  fonts/
└─ _BUILD_SOURCE/                 ← the buildable source (recoverable copy)
   ├─ gamecode.js  patches.js
   ├─ assemble.py  build_ext.py  add_stage_s.py
   └─ bofx.json
```

The raw uploaded master art (the big source sheets, audio, level art) lives outside this zip in the project uploads and is the input to the extraction pipeline.

---

*Generated at the end of the session covering: the missing-S fix, the stage fonts as default UI text, the rebuilt stage-entry cinematic (runway + continuous no-fade scroll + smooth level entry + GET READY), the opaque skull, the pilot slide-out, and the per-stage crate/pill wiring plus the full crate library.*

---
## Session: Rival dogfight bug pass (July 3)
Fixed all 8 reported issues in the rival encounter + ending:
1. **Projectiles invisible in dogfight** — `drawRivalFight` never called `drawBullets()`; now uses the same renderer as the main game (real weapon art for both sides), plus `drawEffects`/`updateEffects` so explosions, floaters and crate breaks actually show.
2. **Lock-on dead in dogfight** — `_lockTargets()` never included the rival, and `updateRetina`/`updateMissileRush` only ticked inside `updatePlay`. Rival is now lockable during the fight phase, retina/missile-rush/nuke systems tick in `updateRivalFight`, and the lock drops cleanly when the rival is disabled (`rival.dead` flag).
3. **Purple halos on dialogue frames** — magenta fringe pixels on all `dlg_*.png` (2,272 px total) despilled via neighbor-median replacement; transparent-pixel RGB zeroed to stop bleed under smooth upscale. Same pass run over portraits/faces/enemy_approaching (clean).
4. **Portrait faces wrong/spliced** — `face_axel/decker/freezer/maverick` were full-body-plus-jet crops. Recropped to head shots (skin-blob detection + layout heuristics; originals kept in `assets/ui/faces_orig/`). `drawCommWindow` rewritten: frame drawn at its natural aspect (was squashed), portrait cover-fit + clipped into the left panel with a tinted divider; `card_*` used as fallback for pilots without face art (e.g. Cole).
5. **N/M throttle did nothing** — tail change rate 0.55→1.5/s, and it now drives the desert scroll multiplier (0.55×–2.6×) with speed streaks, so throttle reads instantly. HUD line calls out THROTTLE UP/DOWN.
6. **Missile box uncollectable** — crates can now be cracked open by flying into them (shooting still works); the missile pack magnets to the player within 80px; `MISSILES ×N` readout added bottom-left.
7. **Ground barely moving** — desert scroll was 46 px/s (and drawn twice per frame in fight). Base is now 150 px/s modulated by throttle; the double BG/ghost-ship draw in fight/ending phases removed.
8. **Stage-5 end faded to black** — stage 5 now goes through the flyover + stats screen like every stage; exiting the final stats screen enters a rewritten `drawVictory`: endless terrain flyover (cycles all five stage terrains, ~9s each with crossfade), player ship cruising, looping credits roll. No fade to black; ENTER returns to title.
Also fixed: crash when the player dies with 0 lives during the fight (same-frame `rival` teardown mid-draw); crash explosion during shoot-down ending was invisible (effects now drawn in ending phases); spare-dialogue uses dedicated victory portrait art in the comm window.
Pipeline: `assemble.py` now reproduces the deployed game (RIVAL/FLYOVER states + extended `stageStats` were hand-patched previously; folded in as steps 9/28).
New FX sheets received (explosions, machinegun/spread/laser/homing projectiles, enemy ships, boss FX) staged unwired in `_BUILD_SOURCE/incoming_fx/`.

---
## Session: FX masters + rival polish pass 2 (July 3, cont.)
**Dialogue frames**: deep purple despill on every dlg_* + dialogue_window.png (dark-purple fringe + interior matte remnants; freezer's whole-frame lavender kept as intentional theme, only edge fringe killed). Verified 0-4 residual px per frame.
**Cole's ship**: two floating black blobs (137px + 98px) removed from ship_cole_t.png; ship_cole_l/r art files swapped (bank art was mirrored — pressing left showed right bank).
**Dogfight speed**: throttle now piecewise — N=150px/s (medium), neutral=300 (fast), M=850 (stage-transition rush). Measured 7.5/15/43 px per capture frame. Ground can never stop or crawl.
**Official font**: rival name, MISSILES XN, throttle line, choice menu, credits → msgText (stage bitmap font); typewriter/shootdown/prompts → BOFmil family.
**Rival music**: Rival_Dog_Showdown mp3 wired as assets/music/rival.mp3, starts with the encounter (manifest BOFA.music "rival"). NOTE: keep `Audio.startMusic('boss')` a single literal match for assemble.
**MASTER FX (src/fx_masters/)**: all 12 effect sheets extracted (265 frames) to assets/fx/master/ + manifest BOFX. File->content map (upload order deceived): machinefx=MG projectile master (5 palettes x 5 growth), spreadfirefx=spread bursts, laserbeam=7 charge lengths, homing=10 missiles (cols 5-9 up/player, 0-4 down/enemy), enemyatkfx_s=THE enemy-attack master (comet palettes rows 9=red/11=blue/13=crimson/14=orange/16=scarlet/18=purple; pellets rows 0-1; flares row 3), enemymissilefx=4 rocket variants, explosivefx=4x4 explosions (row3 blue), blowupfx=9-frame small strip, blowupfx2=3 sequences, bossfx=boss small-shot types, bossmachinegun=4-frame MG pellet anim, bosspowerattack=3 blast streams (red/blue/white — not yet wired to a boss attack).
**Wired**: player MG/spread/laser/homing use master art (level -> palette row + growth col; green/purple via runtime tint); enemy kinds bolt/plasma/ice/mg alias onto shared FIRETYPES (orb/comet/gem/pellet) with per-stage comet palettes; NEW registry `FIRETYPES` + `enemyFire(e,type,pattern,speed,{pal,tint})` with behaviors aimed/twin/fan/column/ring so any enemy shares any fire type; `eShootT` spawns typed shots; `xartTint` gives cached palette swaps. Explosions prefer master families (big/medium/small/blue). Rival + mgturret fire pellet tracer streams.
**Extraction pipeline**: _BUILD_SOURCE/extract_fx_masters.py (rerunnable; tight-box component clustering + magenta despill).

## TO-DO (next sessions)
1. **Emotion portraits**: sad/anger/happy/laugh/crash per character incl. Cole — SOURCE SHEETS NOT IN PROJECT (past-session uploads: coleportrait.png in cole_sstuff.zip, yuri/jugg sheets). Mike must re-upload; then box clean on atlas, strip the emote/"emoji" elements, wire per-emotion comm portraits.
2. **New sheet batch (src/incoming_2026-07-03/)**: clouds pack, 4 enemy-ship variant sheets (idle/fire/damage/death columns), tank+vehicle sheet, boats, turret emplacements x2, doors/gates, aircraft (helis/planes/drones), structures/props, smoke/vapor pack, weapon trails/contrails pack, weather FX pack (REVIEW WITH MIKE FIRST — not all wanted), ice/snow FX pack. All unwired.
3. **eenemyships.png** (src/fx_masters): enemy ship replacements — needs mapping decision with Mike before wiring.
4. bosspowerattack streams -> boss beam/power attacks; bossfx shot types -> boss volleys.
5. Optional GL/CSS layered weapon glow (Mike's idea) — canvas 'lighter' compositing pass or WebGL overlay.

### FIRETYPES quick reference (for wiring new enemies)
Base types: pellet / dart / gem / orb / comet(pal: red,blue,crimson,orange,scarlet,purple) / flare / blast(pal: red,blue,white — bosspowerattack streams).
Derived examples registered: venomDart, voidOrb, emberGem, frostComet, kingPellet.
APIs: `eShootT(x,y,ang,spd,type,{pal,tint,szMul})` · `enemyFire(e,type,pattern,speed,opts)` patterns aimed/twin/fan/column/ring · `deriveFireType(name,base,{tint,pal,szMul,h,glow})` for palette-swapped/new types.
In-game assignments this pass: turret+mech+fk'aimed'=dart · octo+fk'radial'+sub-boss ring=flare · sub-boss aimed=dart · Leviathan triple burst=blast · rival+mgturret+boss MG=pellet · frost family=gem · boss plasma=comet w/ per-stage palette.

## Level-4 white conversion (this pass)
- WLVL_COL[4] changed '#a24aff' (purple) -> '#f2f5ff' (white). Propagates to every place that reads wlvColor(4): bullet glow, HUD, laser tint, spread tint, muzzle.
- MG master art: level 4 was tinting the white row purple; now maps to the sheet's white row (row 0) with no tint. Level 3 still tints white->green.
- Baked art: firewall_icon_4 / ice_icon_4 / laser_icon_4 had ~10% purple border+glow pixels; recolored to white preserving luminance (shading intact). Originals backed up in assets/fx/_icon4_orig/.
- Verified: lvl4 MG bullets sample white (250,241,227 -> 255,255,255), 0 purple; icons 0 residual purple.

## Portrait re-crop fix (this pass)
- Root cause: earlier skin-detection auto-crop grabbed the WRONG region on several faces (maverick's crop was jet cockpit, not his head). The dialogue box WAS using face_* correctly (portraitKey preferred over cardKey, face_* all load) — the face art itself was bad, so it looked like card art.
- Fix: view tool recovered this session; re-cropped all 6 faces by eye from faces_orig/ using gridded reference. Head boxes (fractional x0,y0,x1,y1): axel(.13,.03,.54,.44) decker(.06,0,.50,.42) freezer(.08,.01,.52,.44) juggernaut(.28,.03,.74,.54) maverick(.14,.04,.56,.48) yuri(.12,.08,.64,.64). Padded to ~0.85 w/h portrait aspect.
- Verified live: maverick + decker dialogue boxes now show correct head shots (goatee/collar visible), not card framing. Originals still in faces_orig/.

## New asset sheets — IDENTIFIED & renamed (src/incoming_2026-07-03/)
All 15 renamed from scrambled ig_* to content names (originals in _ORIGINAL_FILENAMES.json). Column structure verified numerically.

GAMEPLAY ENEMIES/OBJECTS (4-col = idle / firing / damaged+smoke / death-debris):
- enemyships_A_4col.png (1024x1536) — 12 flying enemy craft, palette-varied (blue/black/purple/green/red/spiked/etc). Direct replacements/additions for current flying enemies.
- enemyships_B_4col.png (1536x1024) — 6 LARGE multi-engine enemy craft (mini-boss scale), orange/blue/gold/purple/green/red.
- enemyships_C_4col.png (1024x1536) — 12 mech/spider/orb/drone ground+air units.
- tanks_vehicles_green_6col.png (green key, 6-col: idle/fire/smoke/EXPLOSION/wreck/desert-variant) — ~14 ground units: tanks, missile trucks, APCs, AA, radar, jeeps, artillery, patrol boats, hovercraft, barges, turrets. GREEN key incl. a shared explosion column.
- tanks_magenta_4col.png — alt tank/vehicle set, magenta key, camo variants + rust-death.
- turrets_magenta_4col.png — 12 turret emplacements (cannon/gatling/missile/laser/shield/etc), fire+death.
- aircraft_magenta_4col.png — helis, chinook, jets, drones, VTOL, gunboats — fire+death.
- boats_magenta_4col.png — naval: patrol/missile/barge/hovercraft/sub/destroyer + water wake, fire+death.
- structures_props_green_5col.png — walls/barriers/crates/barrels/ammo/sandbags/radar/hatch/generator (intact->damaged->destroyed->rubble). Destructible scenery.
- doors_gates_dark_5col.png (DARK key, magenta door-opening = alpha) — 12 door/gate styles, closed->opening->open->breached->rubble. Stage gates/portals.

FX PACKS:
- clouds_pack.png — parallax cloud layer sprites (small puffs -> big cumulus -> wispy -> ring/vortex).
- smoke_vapor_pack.png — smoke/steam/vapor columns (black/white/grey), engine + damage smoke.
- weapon_trails_pack.png — contrails, missile trails, tracer streaks, muzzle bursts, ring blasts.
- ice_snow_fx_pack.png — frost bursts, crystals, snow, blizzard bands, freeze shatter.
- weather_fx_pack.png — rain/lightning/fire/embers/leaves/sparkles/waves/etc. **REVIEW WITH MIKE — not all wanted.**

### Wiring decisions still needed from Mike:
1. enemyships_A/B/C — which map to which current enemy 'type' ids, which are NEW. (eenemyships.png in fx_masters also pending.)
2. tanks/turrets/aircraft/boats — are these for existing ground-enemy slots or new stage-specific enemies?
3. structures/doors — new destructible-scenery system, or dressing only?
4. weather_fx_pack — joint review.


## Enemy sprite extraction + UNIFORM SCALE STANDARD (this pass)
- Chroma-key bug fixed: halos were DARK key pixels (magenta ~R73/G10/B78, green ~R15/G106/B13) that the old brightness key (r>150 / g>150) missed. Now hue-based: green-low-vs-r&b = magenta family, green-high = green family, any brightness. Verified 0 halo on all outputs (Mike confirmed prior halos; re-extracted).
- Black 2px near-black outline added around every sprite AFTER any resize (fixes soft-ring on scaled units).
- Dropped: enemyships_A missileboat (water-bound), aircraft rows 3/4/8 (pixel loss on splice).
- **UNIFORM SCALE STANDARD v1** (see ART_STANDARDS.md): all enemy sprites placed on a fixed transparent canvas — 128x128 standard, 192x192 huge/mini-boss — silhouette fills a per-class fraction (small 62%/medium 78%/large 88%). In-game draws canvas at e.w, scale = e.w/canvas, so NO per-enemy scale multipliers. 35 sprites @128, 6 @192.
- Pipeline: _BUILD_SOURCE/extract_enemies.py (rerunnable). Outputs assets/enemies/<prefix>_<name>_<state>.png + _keys.json.
- Selected units keyed (idle/fire/hurt/death): esA_navalturret; esC turretC2/C4 + decoC7/C8; esB big1-6 (huge); air 1,2,5,6,7,9,10,11,12; tnkG g2/g3/g5; tnkM m1/m3/m4/m6 + deco m9; trt t1-t6; boat b4-b9,b12.
- NOT yet wired to level enemy tables — awaiting Mike's approval of the cuts + halo/edge look.

## Enemy rewiring — NEW ART LIVE (this pass)
- 170 sprite keys merged into manifest BOFX.
- ENEMY_ART map (gamecode) ties in-game types to new sprite bases; drawNewEnemyArt() intercepts at top of drawEnemy(), picks idle/fire/hurt/death via enemyArtState() (e._muz=fire, hp<=40%=hurt, dead=death). Uniform-canvas: draws at e.w*ENEMY_ART_FOOT(2.15), tint via source-atop.
- Art assigned per (type,stage) in spawnEnemy (rotates variant sets so rows vary):
  - tank/htank: S1 tankA/B/C, S4 tankD/E/F, S5 tankC/G/A
  - mgturret trt1/trt3/esturret1; rockturret trt4/trt2/esturret2; turret trt5/trt6/trt1
  - assault/gunship: S1 jets1-5, S4 jets1/3/5, S3 ships (navalturret/boat1/boat2)
  - drone: S2/3/5/6 drone1-4
  - octo/mech S>=2: drone2/drone4/esturret1
- Verified: 11/11 keys load; stage 1 shows jet1/jet2/esturret1/trt1/jet5 on live enemies; forced-spawn snapshot all 6 categories draw 9k-11k px; regression 11/11 pass. Previews 7 (stage1) + 8 (stage4).
- TODO next: level-3 ship waves need dedicated spawn lines (currently only via assault/gunship on S3); level 2/6 drone passes; mini-boss (esB big1-6) surprise spawns for S4; destructible decoratives (decoA/B/C) need a scenery spawn system; palette-swap variants for repeated hulls.


## FULL enemy migration — 100% coverage (this pass)
- Expanded spawnEnemy art-assignment to cover ALL 23 spawned types by role x stage. Verified 100% of live enemies tagged with new art on stages 1-5, 0 old sprites, regression 11/11.
- Role map: tank/htank->tanks(S1 green/S4 magenta/S5 mixed); mgturret/rockturret/turret/turdrone/shieldd->turret emplacements; assault/gunship/scout/intcp/hfight/bomber->jets (or SHIPS on naval stage 3); drone/mine/mdrone/frost/octo/mech->drones; icegun/cryo->jets; ebomb/minidrone/minicarrier->huge esB mini-boss craft.
- NOTE: game currently ships 5 stages (STAGES array). Mike's plan references a level 6 (drones) — needs a 6th stage authored before those drone waves exist.

## Emotion portraits — EXTRACTED CLEAN + WIRED (this pass)
- Sources (src/incoming_2026-07-03): coleportrait.png (Cole x7), faceavatars1.png (Axel/Decker/Freezer x7), faceavatars2-dontusesads.png (Maverick/Yuri/Juggernaut x7, SAD cells bad per Mike), fixedportraits.png (Yuri+Jugg corrected sad/victory/crash).
- First splice pass was wrong (even-division): the victory/crash cells are WIDER than the others, sheet1 has a header row, fixed-sheet cells carry name banners. Fixed by detecting the actual colored frame lines per sheet (pilot-color vertical/horizontal line detection) + adaptive banner trim (cut below last white-text row in top 32%).
- Geometry (source px): sheet1 cols (198-363)(370-535)(542-707)(714-878)(885-1050)(1056-1259)(1266-1525), rows axel 89-344 / decker 383-637 / freezer 677-933. sheet2 cols (237-439)(448-651)(661-864)(873-1076)(1085-1284)(1291-1481)(1489-1685), rows mav 66-318 / yuri 365-617 / jugg 675-923. fixed cols (15-415)(436-840)(860-1266), rows yuri 14-591 / jugg 627-1214. cole strip y210-505, cells (342-581)...(1881-2190).
- 49 keys port_<pilot>_<emotion> (7 pilots x idle/smile/anger/laugh/sad/victory/crash; maverick_sad = idle fallback, no art provided). All load; verified 0 header-text bleed + face present in every cell; in-dialogue render verified (skin 0.263, bleed 0.002).
- Wiring: pilotPortrait(key,emo) resolves port_ -> face_ fallback; rival script lines carry emo tags (maverick anger/smile, yuri idle/anger, decker idle/smile, jugg anger/laugh); spare dialogue uses victory; shootdown uses crash; pre-stage GOOD LUCK comm uses smile. Old jugg/yuri port_*_ keys replaced by full set.
- Pipeline: _BUILD_SOURCE/extract_portraits.py (rerunnable).

## July-4 upgrade pack — EXTRACTED + WIRED (this pass)
Sources in src/incoming_2026-07-04/ (17 files). Extraction: _BUILD_SOURCE/extract_upgrade_pack.py -> assets/fx/pack0704 (160+ keys, manifest-merged).
**Missiles (bombsaway/.black)**: player homing = silver small, band by level (1 org/2 blu/3 grn/4 wht/5 red) + procedural exhaust; gmiss = big silver by level (lv4->white small); emissile = black smalls rotating red/org/purple bands. Art faces right; rotated by flight angle.
**Crates**: mcrate art -> crate_box (shootable MISSILES box, main game 35%/78% stage spawns + rival fight). Break rolls 70% crate_m3 (+3 missiles) / 30% crate_r10 (+10). Collect grants bombs (cap 99) + missile rush, with floaters. Both draw real art in main game + rival fight.
**Powerups**: speed/shield floaters use pwr_speed_1..5 / pwr_shield_1..5 by current level.
**Sounds (6 wavs -> assets/sounds/, in SFXMETHODS)**: continueVO + countdown at CONTINUE start (VO then 10->1), 'over' on expiry (Mike's VO ends "...game" -> "over"), per-second blips now only last 3s; restrictedarea -> rival banner; enemyunit -> sub-boss spawn (wrapper fn); enemyunits -> 40s gunship wave push.
**Yuri chain lightning (chain.png: 9 bolts, rings, stars, sparks, nets)**: 24% proc on hitEnemy when playing yuri -> arc to nearest enemy <150px, 60% dmg, chain_bolt stretched between points + chain_ring at target + crackle sfx. pilotFx array (new) with lifetimes in update/drawEffects. No re-proc (hitEnemy _noProc arg; hitEnemy wrapped -> _hitEnemyCore).
**Maverick venom (11-frame growth)**: 20% proc on hit -> venom growth anim at impact, DoT 2dmg/0.22s in r26 for 1.15s.
**Attachment weapons (railgun/minigun/chaingun/rocket/tesla)**: barrels wab_*, mounts wam_* staged; FX waf_* wired as FIRETYPES minigunT/chaingunT/railshot/rocketW/teslaW. Assigned: mgturret alternates pellet/minigunT; stage-4 'turret' fires chaingunT; sub-boss ring fires teslaW on stage>=4. TODO: draw mounted barrel overlays on turret sprites (art staged); railgun charge+beam full sequence; rocket explosion linkage.
Verified: 18/18 key sample loads; yuri/maverick combat clean; continue->over->gameover; attachment types fire clean; regression 11/11. Preview 12.

## Pilot missiles + race mode + FX tone pass (this pass)
- **Pilot missile colors** (PILOT_MSL/PILOT_MSL_FAT maps): yuri=red, axel=blue, maverick=green, decker=yellow, freezer=purple, juggernaut=orange, cole=black+green (mslB). Homing volley COUNT = weapon level 1..5 (color never changes). gmiss = FAT pilot variant (cole's nukem warhead kept).
- **Dual-tone level palette** WLVL_COL2 (1 org/yel, 2 blu/wht, 3 grn/blk, 4 wht/gry, 5 red/darkred): MG/spread get secondary-tone additive halo via drawMfx glow2 param; laser gets wide secondary outer glow; enemy/boss FIRETYPES get additive self-bloom.
- **Spinning pickups**: speed/shield icons rotate 1.8 rad/s, missile packs 1.6 rad/s (main game + rival fight).
- **RIVAL RACE MODE**: N/M throttle REMOVED. r._spd scripted: ramp 1.6->5.2 over 38s, every 8.5s a ~2.2s slowdown window (dip to ~1.0, r._slowWin flag, rival drops back = attack opening). tail follows race state. CPU upgrades: aimed 3-round bursts when closing, homing missiles every 4.5-8.5s (1, then 2 after 20s) that steer at the player and CAN BE SHOT DOWN (pBullet + beam collision in the fight loop, 5.5s fuel-out). HUD: "THEY'RE BANKING - HIT THEM NOW!" during windows.
- Verified: 13/13 feature checks (volley counts 1/3/5, speed curve samples show ramp+dips, CPU missiles live, M key inert), regression 11/11. Preview 13.
- Proc-rate knobs to tune with Mike: chain 24%, venom 20%, rival missile cadence.

## Race mode v2 — Mike's tuning (this pass)
- **Speed**: constantly fast — base 2.8->5.5 over 34s, dips only ~24% every 8s (min 2.2). r._slowWin = brief opening, never slow.
- **Mutual lock-on duel**: rival runs a retina-mirror lock sequence (idle -> 1.0s seek w/ acquire blips -> 0.55s LOCKED -> fire 1-2 homing missiles; cd 7->3.8s as fight ramps). Red converging-bracket LOCK warning + flashing "LOCK" drawn on the PLAYER during seek/locked. Player side: weapon-2 missile volleys now steer onto the rival in the fight (turn-limited homing), in addition to C+K retina gmiss.
- **Six maneuver**: every 8-13s rival dives past the wing (0.8s), sits ~95px BELOW the player chasing their X (2.3-3.1s) hosing MG up at them every 0.16s, then returns. gap goes negative; y clamped to playfield.
- **Bash**: collision = hitRival(8) + midpoint explosion + mutual knockback + 42-frame player invuln + shake. No more instant player death on contact; 1.1s ram cd.
- Verified 7/7 (speed curve min 2.56 vs max 5.11 = minor dips; six confirmed below player; LOCKED reached; missiles fired; bash damaged rival, player alive), missile volleys connect (140->92 hp in 6s), regression 11/11. Preview 14.

## Rival missile colors (quick fix)
- Rival lock-on missiles now carry the RIVAL's pilot color via mkey tag (PILOT_MSL[rival.key]): maverick=green msl_2_2, yuri=red, decker=yellow, juggernaut=orange. Generic enemy emissiles keep black-body variants. Verified mkey resolves + green pixels render at missile positions (flame stays orange by design).

## UI restyle + game-feel fixes (this pass)
- **Options + Password screens**: BOF chrome — bofPanel() steel gradient plate w/ orange corner brackets + rivet strips; bofTitle() bitmap-font titles; BOFmil on all labels/keys/readouts; volume segments now orange gradient w/ glow; keybind + password keys are metallic keycaps w/ hover glow; filled password slots glow. (patches.js B_OPTIONS/B_PW; bofPanel/bofTitle defined in B_OPTIONS block, hoisted for B_PW.)
- **Default volumes (Mike's settings)**: master 1.0 / music 0.9 / sfx 0.6 / voice 1.0. NEW voice channel in A.vol; VO samples (continueVO, countdown, restrictedarea, enemyunit(s), over, goodluck, announce, selectpilot) route through it via A.VOICE_SET; options VOICE slider syncs Audio.setVol('voice').
- **Crates (Mike's correction)**: SHOOTABLE box = red/gray crate_m3 art @ 50px (hitbox 48x44, was 30-34). Pop-outs swapped: +3 = camo MISSILES box (crate_box) @ 34, +10 = rect crate @ 44. Gray 'bomb' pickups now draw the camo crate @28 spinning — no more generic gray bombs.
- **Enemy flash fix**: drawNewEnemyArt tint was source-atop fillRect (tinted the whole rect incl. background = "frame flashing"). Now draws xartTint cached tinted copy — sprite-only flash.
- **Death animation**: killEnemy on new-art enemies -> _dyingT phase: death frame shown 0.4s with alpha fade, blast at start + second blast at removal, no firing/moving/colliding while dying, drops+score at dying start. assemble.py "kill count" rule updated to match new killEnemy opening (counts once, guarded by _dyingT==null).
- **BLOCKED — needs re-upload**: newjungle-level.png (1014x5928) + damblownup.png (1024x1536) are NOT in this session's uploads (prior-message uploads didn't persist). Swap plan ready: hue-key magenta + despill -> replace assets/levels/mapJungle.png (480x3197) + mapJungleDam.png (480x720); old map alpha = water (23% transparent), so keyed regions become animated water; the strip's magenta tree band must be cut out & spliced (trees = separate overlay sprites).

## Portrait/face fix + venom special + jungle level (this pass)
- **face_maverick was the green JET, not his face** (all other pilots had proper head crops). Rebuilt ALL 7 face_ avatars from the clean *_idle emotion portraits (skin-centroid head crop). Same manifest paths (assets/ui/faces/face_<pilot>.png) — used on pilot-select comm + stats screen.
- **Venom fix**: my death-anim pass wrongly added a PASSIVE tryMaverickVenom proc (20% on hit) that spawned the venom growth sheet on dying enemies. REMOVED it + the dead spawnVenom/tryMaverickVenom helpers. Venom is now ONLY Maverick's SPECIAL: the venomx attack (pShoot, specialActive('maverick')) upgraded to a twin intertwining HELIX — two strands with opposite phase, drawn with venom_0_* growth frames rolling as they fly (was plain green circles). Yuri's chain proc kept (Mike didn't flag it).
- **NEW JUNGLE LEVEL**: newjungle-level.png (1014x5928) + damblownup.png (1024x1536) keyed (hue magenta -> transparent = water), despilled, scaled to 480w -> mapJungle.png (480x2806) + mapJungleDam.png (480x720). Map height read dynamically + land masks rebuilt (_buildLandMask), dam-blown swap logic already existed. 24% of main map is now water (transparent).
- Verified: mapJungle loads 480x2806; stage 1 plays; NO venom on enemy death; venom special fires 2 helix strands (green px weave x113-959); faces rebuilt w/ skin present; regression 11/11.

## Face avatar crop fix (this pass)
- Mike: axel's left cheek + yuri's head-top clipped, decker too small, general hair/head-side clipping.
- Root cause: emotion portrait cells were extracted cutting AT the colored frame lines (frames sit flush against the art), and face crop used a 62%-wide box on the skin centroid (too tight, off-center).
- Fix 1: portrait extraction cells widened EXP=6px each side + inset reduced 5->1px, so hair/face under the frame is recovered (verified axel left-6px skin=0, yuri top-5-rows content minimal).
- Fix 2: face avatars now FULL-WIDTH top-anchored head+shoulders crop (top of content -> 72% down) with 6px transparent pad. All 7 verified: 0 skin on any edge, 0 hair at top, decker fills 0.88.
- Added MISSING face_cole manifest key (file existed, never registered). All 7 face keys load.
- Emotion portraits re-extracted: still 0 header-bleed, faces present (comm-window dialogue unaffected). Regression 11/11.

## Dialogue portrait boxing (this pass)
- Comm-window (drawCommWindow, patches.js ~235) portrait was COVER-fit (Math.max) + tight clip = head cropped to fill box, looked cut off.
- Now: recessed dark portrait plate + CONTAIN-fit (Math.min, whole head visible) + bottom-anchored (shoulders at base, head up) + 6% padding + tinted frame w/ corner ticks. Added roundRect stroke-path helper to patches scope.
- Verified in-game maverick dialogue: face bbox has margin, not edge-to-edge. Regression 11/11.

## Levels + space + chain/helix + cole halo (this pass)
- **Cole dialogue halo**: despilled purple ring on dlg_cole.png (434->77 residual interior px, edge halo gone).
- **Yuri chain**: chain bullet + zap arcs now draw chain_bolt_* frames (animated, stretched between struck enemies) + chain_ring flash at nodes. Special already fired chain; this is the visual upgrade.
- **Maverick helix**: two venomx projectiles now share phase clock, opposite dir = 180deg on a common axis = true double-helix winding around each other. amp grows with age.
- **LAVA (stage 2)**: mapVolcano replaced w/ new lavalevel (480x3750). Added lavafall_* overlay (4-frame animated cascade, XART-loaded) at 3 spots scrolling with map. drawLavafalls().
- **ICE (stage 3)**: new mapIce (480x3281) now scrolls like jungle over dark-icy-blue water (iceWaterFrames_0-3 generated from waterFrames, hue-shifted deep blue). drawStage3(). 96% icy-blue verified.
- **SPACE (stage 5)**: starrealm.png (no planets) tiles as scrolling backdrop under starfield.
- **MENU**: starplanets.png scrolls LEFT at medium speed (dt*36), tiled, height-fit; starfield now drifts left too. _menuScrollX.
- **LOGO**: shump_edition.png keyed -> menuLogo.png (Coleforge Engine Shump Edition replaces rail edition).
- Manifest gotcha: maps load via top-level BOF.<key> (next to mapJungle), NOT img{}; lavafall via XART.rdy (individual imgs), NOT ASSETS.has (which checks atlas frames). All 5 new assets load. Regression 11/11.

## Menu backdrop + logo fix (this pass)
- ROOT CAUSE: patches.js (line ~134) defines its OWN drawTitle that assemble.py span-replaces the gamecode one — my earlier gamecode drawTitle edit was DEAD. The real drawTitle drew XART 'bootimage' (old jungle/city splash) as cover + XART 'logo' (old rail-edition) on top.
- Fixed the patches.js drawTitle: scrolling starplanets backdrop (left, dt*36, tiled height-fit) + star parallax + legibility gradient; SHUMP logo via ASSETS.menuLogo (fallback to old atlas logo). _menuScrollX hoisted into patches scope.
- Verified: old backdrop gone (green 1.5%/orange 1.4%, were dominant), space present (66% dark), SCROLLING (band frame-diff 0.165 vs 0), logo band has content. Regression 11/11.
- LESSON (again): drawTitle, drawOptions, drawPassword, drawStageClear are patches.js-owned via assemble span-replace — always edit those in patches.js, never gamecode.js.

## Input bug fixes: mouse-hover lock + controller menus (this pass)
- **BUG 1 (hover blocks keyboard)**: title/diff hover loop ran `if(mouse.inside)menuIndex=i` EVERY frame, overwriting keyboard changes. Fix: added mouse.moved tracking in Input.mpos (set on real position delta >0.5px); hover now only sets menuIndex when `Input.consumeMouseMoved()` is true this frame. Keyboard/pad nav no longer overridden by a stationary hovering cursor. Click still selects+activates.
- **BUG 2 (controller can't navigate menus)**: menus used hardcoded arrowup/w/etc, ignoring pad_* keys (which pollGamepad DOES populate, and which are in keybind defaults). Added Input menu helpers: menuUp/menuDown/menuLeft/menuRight (tapAny over keybind[dir], so wasd+arrows+dpad+stick all work), menuConfirm (enter/space/fire/pad_b0/pad_b9), menuBack (backspace/escape/pad_b1/pad_b8). Wired into title, diff, pilot, options nav + password (pad A=enter, B=back).
- **Rebind improvement**: binding a pad button now APPENDS to the action (keeps kb defaults); binding a kb key replaces primary kb key but keeps pad binds. So assigning a controller doesn't wipe keyboard control.
- Verified: keyboard down changes selection while mouse hovers (idx 2->3); mouse MOVE still selects hovered (idx 0); menu helpers honor keybind incl pad_up/down. Regression 11/11.

## Boss/FX/font/laser/missile-icon integration (this pass)
- **NEW BOSSES** (mapped: chopper->S1, fboss->S2, iboss->S3, tankboss->S4). extract_bosses.py: 3x2=6-frame sheets keyed+despilled to assets/bosses_new/ (66 frames, worst bright-halo 1px). Chopper needed dark-purple-rim keying (its anti-aliased edge was near-black purple the brightness key missed).
- **Boss state machine** (drawNewBoss in gamecode): NEWBOSS config per stage {idle,fire,death,frames,wmul,form2}. States: idle cycle (t*10%6), fire-frames while b._firing>0 (set 0.35s on each bossAttack), death plays death_/fboss_death_ frames over 1.6s then fades. Hit-flash via xartTint cached copy (sprite-only). drawBoss routes to drawBossSprite when NEWBOSS[stage] idle_0 is ready.
- **iboss 2-form**: transforms to iboss2_idle/iboss2_atk at <=50% HP (b._xformed guard + blue explosion + shake). iboss_barrel overlay drawn on form. Verified form1 at full HP, form2 at 40%.
- **iboss projectiles**: 39 iproj_* extracted to assets/fx/iboss_proj/ (available for attack wiring).
- **LASER BEAMS**: laserbeam.png -> 5 vertical colored beams (orange/blue/green/white/red = lvl 1-5) to assets/fx/laserbeam/. Wired into kind==='laser' draw: laserbeam_(lv-1), width scales w/ level, per-level glow color. Falls back to old laser_N then procedural.
- **STAGE FONTS**: stage1/3/4font.png -> 56 glyphs each -> packed atlases assets/atlases/stagefont{1,3,4}.png + BOF.stageFont{} map (atlas/frames/font). New curFontArt() prefers stageFont over atlas font; defFontArt/defFontAlt route through it. NOTE stage-1 font now HAS 'S' (old atlas lacked it — the S-borrow-from-stage-2 hack is now moot for S1).
- **MISSILE ICONS** (resized): missilecrate (red/gray M box) -> shootable crate @50px; missilebox (green MISSILES) -> +3 popout + bomb pickup; missilecrate2 (wide MISSILES) -> +10 popout. Registered in img{}.
- **BUILD FIX**: drawMenuButton/drawMenuIcon live inside the B_TITLE span (between TITLE_ITEMS and tryExit) which patches.js replaces — they were being DELETED (only harmless because real game loads btn_ images so the fallback never ran; but harness crashed). Copied both defs into patches.js B_TITLE block so they survive assembly.
- Verified: all 10 content groups load; 4 bosses render clean in-game (chopper/fboss/iboss/tankboss, 0 halo on sprite); iboss form2 transforms; regression 11/11.

## Batch: tank/weapons/freezer/spin/enemies/lavafall/bosses/rival/announcer/music/flyover/fonts (this pass)
- **TANK**: rescaled smaller (was *1.10 now *0.82; htank *1.08->*0.84). Restricted to stages 1 & 4 ONLY (was 1&2). Verified NO tanks on stage 3.
- **MG WEAPON COLORS**: lv3 green/white (softer #5fe07a primary, white secondary, #7fe89a tint not pure green), lv4 white/gray, lv5 red/white. Updated WLVL_COL/WLVL_COL2 + _mgTint.
- **FREEZER MUSIC RESTORE**: bug was track-change during slow left playbackRate stuck. Fix: startMusic now resets playbackRate+preservesPitch per current timeScale; endSpecial fully restores rate+pitch; belt-and-suspenders in update loop forces timeScale=1 + rate=1 whenever timeScale<1 && !freezer-active. Added A.stopVoice()/Audio.stopVoice.
- **PICKUP SPIN**: missile boxes/crates (bomb, missilepack, missilepack10, both main-game AND rival-fight versions) now draw UPRIGHT (no spin). Speed/shield pills spin FASTER (t*1.8 -> t*3.2).
- **ENEMY DENSITY**: rewrote spawn director — release ONE wave at a time, only when field has <=4 enemies AND 1.1s gap elapsed. vRow capped to <=4 and never overflows to >5 total. Max on-screen dropped 11->9, avg 4.1. Player always has a lane.
- **LAVAFALLS**: were random screen-center. Now anchored to MOUNTAIN fall channels at x-fractions 0.10/0.90/0.50, fixed map-Y bands (70/70/150), only drawn while the mountain band is on-screen (screenY = mapY - srcTop), scrolls with terrain. Verified clusters near 0.13/0.56/0.82.
- **BOSS SIGNATURE ENRAGE**: each boss fires a unique telegraphed signature move the first time it drops below 50% HP (shout + shake + 0.6s windup, then payload). S1 ROTOR STORM (radial+MG cone), S2 HELLFIRE BARRAGE (5 missiles + MG cone), S3 ABSOLUTE ZERO (24-ray ice nova + 4 frost orbs), S4 SIEGE MODE (full-width cannon volley w/ 2 gaps + aimed crescents), S5 CORE MELTDOWN (double-spiral + brood). Existing per-stage movesets already distinct; this adds the climactic beat. Verified trigger at 45% HP.
- **RIVAL DOG MODE**: rival HP 140->340 (not a pushover). CONSTANT twin-wing MG fire (fireCd 0.5->0.16 lerp, always shooting; adds spread+strafe bursts on your six). Faster chase (base 2.8-5.5 -> 3.6-6.8). Lock-on missiles come more often (7-3.8s -> 4.5-2.4s). Verified rival fires MGs (25 bullets on screen), 340 hp.
- **ANNOUNCER/CONTINUE**: rewrote drawContinue. continueVO plays once. Countdown VO now SYNCED to the visible number (fires per-number tick when displayed num changes, was setTimeout drift). Pressing fire to continue CANCELS pending countdown VO (_stopContinueVO + Audio.stopVoice). over.wav plays after "game" at secs<=0 (drawContinue._overPlayed guard). NOTE: file is over.wav (Mike said over.mp3 but over.wav is what exists; routing handles it).
- **MUSIC**: stage 2 -> bullets.wav (bullets music key registered; STAGES n2 music:'bullets'; assemble.py stage2-music rule updated to match new anchor). Stage-clear music -> 'password' (enter-password.mp3) instead of 'stageend'.
- **STAGE-CLEAR FLYOVER**: was cutting to random jungle water. Now _stageLiquidFrames() picks the stage's OWN liquid (S1 water, S2 lava, S3 iceWater, S5 starrealm scroll, S4 sky gradient). Player ship starts from ACTUAL end position (flyoverStartX/Y captured at flyover trigger) and pulls forward+shrinks, so the liquid extends seamlessly into the cut. Verified S2 flyover = 100% lava, 0% water.
- **STAGE-CLEAR STATS FONT**: title now uses curFontArt() (new stage font); stat labels/values render via msgText() (which routes through curFontArt) instead of monospace.
- Regression 11/11 throughout.

## Rival dogfight: rockets not bullets (this pass)
- Removed ALL machine-gun ball projectiles (kind:'mg') from the rival fight — both the front-facing spray and the six-mode strafe.
- Player chases from behind (rival flees above at player.y-gap). When player is behind (_playerBehind = player.y > r.y+8), rival now fires BACKWARD homing ROCKETS (kind:'erocket', pilot missile art via mkey/PILOT_MSL). Twin rockets when player closes (tail>0.4).
- Six-mode (rival dives behind player): now fires forward rockets up at the player instead of MG balls.
- Lock-on (LK) system: the rival paints the player with a retina reticle + "LOCK" warning (drawRivalSeq ~4645, unchanged — this is the "retinas going on the player"), then fires erockets instead of emissiles.
- erocket behaves like emissile: homes at player (turn ~0.055-0.11), shootable by player bullets, fuel-out at 5.5s, renders with pilot missile art (same draw path as emissile). 
- Balance: front-rocket cadence lerp(2.2,1.15)s (slower than old MG since homing is harder to dodge), hard cap 4 concurrent front rockets + up to 2 lock-on salvo = ~6 max on screen. Verified 0 MG balls, 6 rockets max, retina lock active.

## Bug batch: maverick/boss-death/iboss-MG/weapon-colors/laser/missileboxes/yuri/tanks/lava (this pass)
- **MAVERICK special fire rate**: was using weapon-based cd ({0:0.085,1:0.16...})[run.weapon] so held weapon randomized his fire speed. FIX (gamecode ~1604): specialActive('maverick')=>cd=0.05 constant rapid MG; specialActive('yuri')=>cd=0.14; else weapon cd. assemble.py "fire cd" rule updated to preserve PILOTMOD.fire only for the non-special case.
- **Special LOST ON DEATH**: playerHit() now calls endSpecial()+clears special/retina/timeScale/zaps. Verified Maverick special gone after death.
- **ICE BOSS DEATH showed CHOPPER**: root cause — NEWBOSS[3].death:'death' and [4].death:'death' pointed at the CHOPPER death sheet (death_0..5 IS the chopper exploding). FIX: only chopper(1)/fboss(2) have death sheets; iboss(3)/tankboss(4) death:null => char THEIR OWN idle sprite (xartTint dark) + rolling explosions (blue for stage 3). Verified iboss death region is blue(iboss) not tan(chopper).
- **BOSS firing-frames always on**: firing check was (b._muzL>0||b._muzR>0||b._firing>0); _firing=0.35 on every attack so it was ~always "firing". FIX: firing=(b._muzL>0||b._muzR>0) — only the brief muzzle flash. Boss shows idle chaingun frames by default.
- **iboss shoots MG ROWS not balls**: stage-3 boss reworked to fire rapid elongated MG tracers (new kind:'embullet', drawn as elongated tracer not a ball) from BOTH chainguns via new eMG() helper. Cadence 0.09s, 16/burst, plus nova/orb breathers. Max ~34 on screen (dodgeable).
- **MG weapon colors** (lv1 kept appearing green, lv4 red): root cause — mfx_mg sprite ROWS are baked colors (row0=red,1=blue,3=green,4=white) and the row map {1:3,4:0} gave lv1=green-row, lv4=red-row. FIX: always use WHITE row (row 4) as neutral base + exact per-level TINT {1:'#ff8a1e' orange,2:'#3a8aff' blue,3:'#5fe07a' green,4:null white,5:'#ff4a48' red}. Verified on dark bg: lv1 RGB(215,144,82) orange, lv3 (134,220,154) green, lv4 (230,224,244) white, lv5 (236,109,119) red.
- **LASER BEAM**: the actual laser weapon (w===3) fires kind:'beam' (solid continuous), NOT the dead kind:'laser'. Rewrote the beam render to use laserbeam_3 art TINTED per-level to the described colors {1 orange,2 blue,3 green,4 white,5 red} with glow bloom + white-hot core + muzzle orb. (Old beam had lv3 dark-green #37d24a and lv4 PURPLE #a24aff — both wrong.) Verified lv1 orange/lv3 green/lv5 red.
- **MISSILE BOXES readable**: missilebox 34->46px, missilecrate2 44->58px, bomb box 28->42px, all upright + gentle bob so the "MISSILES" text reads as they float. missilecrate stays the spinning shootable @50px.
- **YURI chain lightning**: (a) removed the passive 24% chain proc on NORMAL hits (tryYuriChain in hitEnemy) — chain is SPECIAL-only now. (b) special reworked: yuriChainStrike() arcs lightning FROM the ship (ox,oy=player.x,player.y-14) to nearest enemy/boss/subboss, then chainZap chains to neighbors (2+min(2,lv) hops). Uses chain_bolt_*/chain_ring_* art via drawZaps. No traveling bullet.
- **TANKS SCRAPPED** (not front-facing per Mike): disabled all tank/htank spawns; ground stages (1&4) now get rotating gun turrets (mgturret/rockturret — 8-dir gun frames that track the player). Ground turret draw size reduced e.w*1.9->1.35. Verified no tanks spawn.
- **ANIMATED LAVA too huge/all-over**: drawAnimTerrain got a tileScale param — stage 2 lava now tiles at 0.5 (half-size pattern) via drawScrollLevel(...,0.5) so it's not one giant stretched frame. Also re-keyed mapVolcano strictly (magenta bg only).
- Regression 11/11.

## Bug batch: logo/lava-layering/warning-scale/yuri-fire/rival-dogfight/boss-muzzle (this pass)
- **START-SCREEN LOGO**: boot cinematic + press-start gate + credits still drew the OLD 'logo'. Now all prefer the new SHUMP logo (menuLogo/ASSETS.menuLogo) with old-logo fallback. (Title already used menuLogo.)
- **LAVA LAYERING**: reworked drawStage2 into explicit layers: (1) animated lava BACK layer full-frame tiled at 0.5, (2) firefalls (drawLavafalls) scaled DOWN 0.42->0.22 and drawn BEFORE the terrain so mountain walls/side-walls overlay them, (3) keyed terrain on top. mapScroll advanced once for consistent layering. Firefalls are now narrow back-layer cascades, not giant foreground columns.
- **WARNING SIGNS scaled down**: boss/sub-boss alert_up VW*0.74->0.5; enemy_approaching VW*0.8->0.52 (both the stage warning and the rival-intro banner).
- **YURI special fired nothing without enemies + couldn't hit crates/pills**: yuriChainStrike now considers enemies, boss, sub-boss AND powerups (crates/pills) as chain targets; new zapPowerup() applies chain damage to containers (crate/capsule/scrate/mcrate) and pops them. If NO target exists anywhere, it still emits a visible bolt straight up so the weapon always "fires". Verified fires with no enemies + damages crates.
- **RIVAL DOGFIGHT reworked** (per Mike's new vision):
  - Intro: keep the super-fast ground rush from the stage-clear flyover through banner/approach/dialogue (drawDesertBG spdMul 2.2). Rival comes up from behind and INCHES up alongside the player (banner->approach phases) instead of the old flyby/turn/settle acrobatics.
  - SMASH beat: after dialogue, new 'smash' phase — the rival lunges in and rams the player's plane; player flashes white (brightness 2.8), screen shakes, takes a hit (costs a shield if held), 'RAMMED!' float. Then transitions to fight.
  - Fight AI is now a CLEVER DOGFIGHT BRAIN (replaced the old race model): threat-read (scans player bullets heading at the rival and juke-dodges hard off the bullet column), hunt/juke mode switching weighted by a fluctuating aggression stat, free up/down + horizontal movement for both. Rival fires AIMED homing rockets toward the player from whichever side it's on (faster cadence when lined up + hunting), and does occasional RAM lunges when aggressive + close. Player has free up/down/left/right movement + normal shooting. Old get-on-six MV system removed. Verified: rival X-range 213px, Y-range 280px of active maneuvering; fires rockets; hunt/juke switching.
  - Fight HUD text updated (JUKING/AGGRESSIVE-WATCH-THE-RAM/OUTMANEUVER THEM).
- **BOSS muzzle-always-on** (fboss + iboss): ROOT CAUSE — _muzL/_muzR were set in attacks but only decremented inside drawBossSprite's fallback path; fboss/iboss use the drawNewBoss path where they were NEVER decremented, so they stayed lit forever => boss looked always-firing. FIX: decay _muzL/_muzR at the top of drawNewBoss every frame. Also non-firing phases (nova/orb/dash) explicitly clear _muzL/_muzR. Verified fboss 296/360 idle frames, iboss 292/360 idle — muzzle+fire frames only during actual bursts.
- Regression 11/11 (updated the rival test for the new smash phase between dialogue and fight).

## Large batch: fonts/boot-logo/halos/dialogue/rival/countdown/space-launch/MG-glow (this pass)
- **NEW FONTS**: re-extracted stage1/3/4 fonts from updated sheets (src/incoming_0705/) — 58 glyphs each, S present (no more wonky-S hack). Packed to assets/atlases/stagefont{1,3,4}.png + BOF.stageFont manifest. Added uiFontArt() = stage-1 font; defFontArt() now routes ALL msgText UI text through the stage-1 stone font.
- **BOOT LOGO**: root cause — boot checked XART.rdy('menuLogo') but menuLogo is an ASSETS asset (ASSETS.menuLogo), not XART, so it always fell back to the old logo. Fixed press-start gate + boot cinematic + credits to use ASSETS.menuLogo (the SHUMP logo).
- **PURPLE HALOS despilled**: diff_easy/normal/hard/furious/elite, dialogue_window, pwmenu, statscreen, logo, mapVolcano (stage-2 map). New despill(): halo mask -> neighbor-median fill / desaturate.
- **STAGE-2 CARD top strip**: cropped the card atlas frame [2,2,886,498] -> [2,54,886,446] to drop the drippy green vine strip (clear opacity gap at rows 32-48 separates strip from plaque).
- **NEW SOUNDS**: registered chainShoot (chain_lightning_hit_1), chainHit (hit_2), statsBar (stats_bar). Added to SFXMETHODS. Wired: chainShoot on Yuri fire, chainHit on chain connect/hop, statsBar on stat-bar reveals.
- **YURI chain**: (a) fires nothing without enemies -> now emits a bolt straight up when no targets; (b) couldn't hit crates/pills -> yuriChainStrike now considers powerups + zapPowerup() damages containers; (c) ice-orb+chain fired both -> startSpecial clears live orbs when Yuri special begins.
- **LASER/CHAIN impact sounds**: hitEnemy already plays Audio.SFX.hit on every enemy hit (covers beam + chain).
- **MAVERICK helix**: slowed a hair (vy -8.2->-6.8, phase 13->11, roll 16->14).
- **RIVAL dogfight continue bug**: dying with lives -> respawn in fight (was already, +invuln). Dying with NO lives -> NEW 'player_spared' phase: the rival spares the player with RIVAL_PLAYER_SPARED dialogue ("see you around... if you live"), then game over. No more kick to stage-2-clear menu.
- **RIVAL dog super-fast**: intro (banner/approach/dialogue/smash) + whole fight now run drawDesertBG at high spdMul (fight 3.4x, ending 1.8x) with stronger speed lines. Verified 1871 speed-line px in fight.
- **RIVAL missiles STACK to 20**: dogfight missile pickups no longer call startMissileRush (which reset bombs to 10); they add +3/+10 and clamp to 20 so the fight is winnable.
- **DIALOGUE typewriter**: typeReveal() reveals text letter-by-letter with a blip per letter; 1st fire press reveals all, 2nd advances. (Renamed from 'typewriter' to avoid clash with the existing typewriter(text,frac,...) — that clash was causing a font-style crash/hang.)
- **DIALOGUE portraits**: forced to 'idle' everywhere (removed emotion 'emoji' face swaps).
- **PILOT SELECT**: removed role subtitle + pip dots; hint line now neutral color, arrows for scroll, back-key label from keybind.
- **CHOOSE YOUR PILOT! + GO!**: white stage-1 font, no orange/yellow/red.
- **PASSWORD**: slots enlarged (34x30 -> 52x48), typed chars in the bitmap stage font, larger.
- **ALERT box**: removed 'BOSS APPROACHING'/'HOSTILE SIGNATURE' subtitle text.
- **STAT SCREEN**: labels/values reverted to regular monospace (bitmap font looked off); title stays stage font. statsBar sound on reveals.
- **BACK BUTTON**: restyled with beveled octagon chrome + bitmap-font 'BACK' + arrow, scaled to fit.
- **MG lv1-2 glow**: added additive bloom orb + larger glow size for low-level MG (looked weak).
- **TRANSITION**: removed the terrain region — now runway -> liquid -> level directly.
- **SPACE LAUNCH (stage 5)**: run speed cap 1750->3200 (faster than ever), ship scales up 62->128px as it lifts off + rises, stronger speed lines.
- **COUNTDOWN loop bug**: was re-triggering the full countdown clip on every number change ("10 9 10 9"). Now plays the clip ONCE and drives the on-screen numbers from elapsed time.
- Per-stage regression 11/11 (full regress.js OOMs in the harness on the 13s stats loop — a harness memory limit, not a game bug; verified all sections pass individually).

## Batch: shield icons + per-pilot special boxes wired; rest staged (this pass)
- **SHIELD ICONS**: extracted 5 per-level shield icons from shields.png (magenta-keyed) -> assets/fx/shields/shield_l{1..5}.png, registered in manifest img/XART block. drawShield() now draws the per-level art (baseH 30..46 by level, pulse + slight rotation + additive glow) with the procedural version as fallback. Verified shield_l3 renders around the player.
- **PER-PILOT SPECIAL ABILITY BOXES**: extracted 7 boxes from powerupboxes.png -> assets/fx/specialboxes/special_{pilot}.png. Mapping per Mike: red=yuri, blue=axel, green=maverick, purple=freezer, orange=juggernaut, yellow=decker, black=cole. Registered in manifest. Wired: (1) drawSpecialHUD shows the pilot's box next to the special bar; (2) special pickup falls back to the per-pilot box art. Verified special_yuri renders in HUD.

## STAGED IN src/incoming_0705b/ (NOT yet wired — next session):
- **stage5sheet.png** — stage-5 (space) sprite sheet. Needs extraction + wiring.
- **stat_bars.png** — new stat-bar frames/fills (6 colors, framed + segmented + solid variants). Could reskin the stage-clear stat bars.
- **stage6.png** — stage-6 "FURIOUS DEATH" asset sheet: title logo, skull torches (2 anim rows x6), demon skull faces (5), smoke plumes (8), ember bursts (8), flaming-skull projectile (8-frame), + a bundled font row.
- **stage6font.png** — stage-6 dedicated font (stone+blood, full glyph set).
- **powerupboxes.png / shields.png** — source sheets kept for reference.

## TODO (added per Mike):
- **RE-WIRE TURRET TANKS + TURRETS**: bring back the turret/tank emplacements we had, but RESCALED MUCH SMALLER, and make them STATIONARY on the map below the player (ground decorations that fire up). Currently ground stages use rotating mgturret/rockturret; Mike wants small fixed turret-tanks sitting on the terrain beneath the player.
- (still open from before) stage-6 authoring using stage6.png assets; stage-5 sheet wiring; new stat-bar art; iproj_* wiring; L3 ship waves; L4 miniboss spawns; attachment barrels; railgun.

## Batch: stats font + password font + RAIDEN auto-missiles (this pass)
- **STATS SCREEN FONT**: stopped recoloring the stat labels/values per stage. Labels + values now use the DIALOGUE font ("BOFmil") at a consistent light color (#eaf2ff), NOT the per-stage theme color. Pilot name/role also switched to BOFmil, no theme tint. The "STAGE N CLEAR" title keeps its stage font (per Mike's "except for stage clear"). Verified light dialogue-font pixels present, no recolor.
- **NEXT-STAGE PASSWORD (stage-clear screen)**: the code is now displayed LARGE in the NEXT stage's bitmap font (stageText with ASSETS.stageFont[stage+1]), with a "NEXT STAGE PASSWORD" label above it in BOFmil.
- **PASSWORD ENTRY screen**: as you type, the typed characters render LARGE in the bitmap font of the stage that code unlocks (prefix-match against {FURY:1,IRON:2,DAM5:3,STRM:4,ORBT:5} -> use that stage's stageFont live). Verified typing IRON shows stage-2 font glyphs.
- **RAIDEN-STYLE AUTO MISSILES** (big gameplay change): MISSILES is no longer a swappable weapon.
  - New run.missileLevel (0..5). When >0, autoFireMissiles() fires on its own timer (cd 0.9s@L1 -> 0.42s@L5) ALONGSIDE the primary weapon, no button needed. Count = level (1..5 missiles fanned from the wings), homing turn 0.14+lv*0.012, pilot-colored art (mkey via pilotMissileKey), kind:'missile' _auto:true. Homing logic reuses the existing missile-bullet steering (targets nearest enemy/boss).
  - Removed the w===2 manual missile branch from pShoot (missiles auto-fire now).
  - Weapon crate wtype===2 -> missile LEVEL-UP instead of weapon swap. missilepack -> +1 missile level; missilepack10 -> MAX. (No more startMissileRush / run.bombs from these.)
  - Death: missileLevel -= 1 (lose one level, not all), like weapon levels.
  - HUD: the old bomb-count slot (cx[3]) now shows 5 MISSILE-LEVEL pips (green, glowing when filled).
  - Verified: L3 auto-fires up to 6 homing missiles on screen while the primary fires; missiles curve toward off-center enemies; no missiles at level 0.
  - NOTE: the separate run.bombs / useBomb (gmiss smart-bomb) + retina lock + Cole special + rival-dogfight missile-stack systems are UNCHANGED — that's a different mechanic. Only the missile-as-primary-weapon behavior became the Raiden auto-fire.
- Per-stage regression 11/11 with the new missile system.

## Batch: special crate uses new box art + floats the inner icon on break (this pass)
- **SPECIAL CRATE ART**: the special crate (scrate) now falls as the NEW per-pilot special ABILITY BOX (special_<pilot>, tinted to the current pilot's color) instead of the old procedural red-lightning box. drawScrate uses XART special_<pilot> with a pilot-tint glow + break-flash bloom; procedural version kept as fallback. Verified Axel's crate renders blue, Yuri's red.
- **INNER ICON FLOATS OUT ON BREAK**: extracted the inner special-ability glyphs (the lightning/shield/DNA/clock/ship/wireframe/nuke icons) from the boxes -> assets/fx/specialicons/spicon_<pilot>.png (7), registered in manifest. When the box breaks, breakContainer now spawns a 'specialicon' pickup (was 'special'). The specialicon draws the inner glyph floating (additive glow + bob) and, when collected, calls startSpecial() (same as before). Verified: box breaks -> icon floats -> collecting activates the special.
- Both 'special' and 'specialicon' pickup kinds grant the special and both draw via the shared block (icon preferred, box fallback).
- Smoke test 9/9 (special boxes + icons load, stages 1/3/5 survive with a special crate present).

## Large bugfix batch (this pass)
- **MISSILES gated on firing**: auto homing missiles now fire ONLY while the fire key is held (were firing on their own). Verified idle=0 missiles, firing>0.
- **MISSILE death revert**: dying resets run.missileLevel to 0 (was -1); next missile powerup starts at level 1 again.
- **PASSWORD**: (a) 'ENTER PASSWORD' title now white (#f2f5ff, no yellow); (b) keyboard moved to the BOTTOM of the screen (rowY0=VH-16-totalKbH); (c) added d-pad/arrow navigation across the whole keypad + a synthetic BACK target — arrows move a highlighted selection, fire/enter selects; keyboard still types directly.
- **CREDITS**: removed yellow (title + text now white/light). New content: DIRECTOR/DESIGNER/CODER/MUSIC/SOUNDS -> MICHAEL "FORGE MASTER" COLE / ART -> "GPT IMAGES & NANO BANANA PRO" / COLEFORGE ENGINE "SHUMP EDITION" / WRITTEN, CODED AND DESIGNED BY -> MICHAEL "FORGE MASTER" COLE. Removed "RAIL SHOOTER EDITION".
- **MUSIC VOLUME**: routed each music track through a WebAudio gain node with MUSIC_BOOST=3.2 (HTML5 .volume caps at 1.0 so the quiet tracks couldn't be lifted before). Rebalanced defaults: music 1.0, sfx 0.55. setVol/startMusic updated to drive the boost gain. REQUIRED updating the assemble.py "Snd music url-aware" anchor to match the new multi-line music-load code (the old single-line anchor stopped matching -> AssertionError -> stale deploy; fixed).
- **DIFFICULTY screen**: (a) removed the tiny text under the buttons; (b) uses the scrolling space backdrop (scrollSpaceBG, shared with main menu); (c) shows the highlighted difficulty's full RULES large in the stage-1 font at the bottom. DIFF_DESC expanded to readable rules. Title white.
- **PILOT SELECT**: (a) added the special ability NAME + short description under the pilot name (SPECIAL_INFO map: AEGIS SHIELD, OVERCLOCK, VENOM STRIKE, TIME FREEZE, WRECKING BALL, CHAIN LIGHTNING, NUKE STRIKE); (b) removed the emoji speech bubble that appeared next to the pilot's face in the comm window.
- **ATLAS CARDS**: removed torch/skull animations (drawCardFX no longer called in the intro). New sequence: card DROPS in from the top -> THUD + screen shake (crash/expBig sfx) -> then drops down and off the bottom of the screen.
- **CONTINUE**: no separate 'continue' VO first; the number countdown is paced to the ~16s countdown clip (1.4s lead-in + 1.45s per number = 10 numbers over ~16s) so the on-screen numbers match the audio.
- **JUGGERNAUT**: fully invulnerable to enemy bullets/attacks while the wrecking-ball special is active (playerHit early-returns).
- **AXEL aegis special**: now spawns an aura + 5 orbiting orbs; each hit pops one orb and shifts the shield colour (AXEL_ORB_COLS palette), no life lost until all orbs are gone. Replaces the old golden-ring aura.
- **LASER**: added animated fluid FX — an undulating outer side-glow that breathes, inner energy blobs racing up the beam, and a flickering hot core line + pulsing muzzle orb.
- **RIVAL DOGFIGHT**: (a) cutscene entry now runs the ground rush at FULL speed (3.4x) from the start (was 2.2x); (b) losing the dogfight no longer ends the run — the rival spares you (player_spared) and you continue to the NEXT stage; (c) the SPARE/SHOOT decision now renders as clear dialogue-text options with a highlighted selection bar, and accepts d-pad/arrows/wasd (was keyboard/wasd only) plus fire/enter/gamepad-A to confirm.
- Smoke: stages 1/3/5 play + survive + missile-gating 10/10; Juggernaut invuln + Axel orbs pass; rival choice d-pad + spared->continue pass.

## Batch: credits stage-1 font + level-3 music swap (this pass)
- **CREDITS font**: the CREDITS title + the section-header rows (DIRECTOR/DESIGNER/CODER/MUSIC/SOUNDS, ART, WRITTEN CODED AND DESIGNED BY) now render in the STAGE-1 bitmap font (stageText w/ ASSETS.stageFont['1']). The name/value rows (MICHAEL "FORGE MASTER" COLE, GPT IMAGES & NANO BANANA PRO, COLEFORGE ENGINE "SHUMP EDITION") stay in the dialogue font (BOFmil) for readability. Scrolling space bg retained.
- **LEVEL 3 MUSIC**: replaced with the uploaded level3.wav.
  - New: assets/music/lvl3.wav (stage 3 uses music:'lvl3' -> now the new wav).
  - Old track preserved: copied to assets/music/lvl3-alt.mp3 and registered as music key 'lvl3-alt' in the manifest (deleted the old lvl3.mp3 so the key resolves to the wav).

## HOTFIX: no music at all (this pass)
- ROOT CAUSE: the previous WebAudio MUSIC_BOOST change routed every music <audio> element through createMediaElementSource -> a gain node. That hijacks the element's direct output: once routed, sound ONLY flows through the WebAudio graph, and if the AudioContext is suspended (it is until a user gesture) or the media is treated as tainted, NOTHING plays. This silenced ALL music, not just level 3.
- FIX: removed the WebAudio routing entirely. Music is back to plain HTML5 <audio> element playback (m.volume=music*master, .play()). To keep music audible over effects without a >1.0 boost (which HTML5 volume can't do anyway), the SFX mix was lowered instead: defaults now music 1.0, sfx 0.42, voice 0.85.
- Updated the assemble.py "Snd music url-aware" anchor back to the single-line music-load form to match the reverted code (avoided the stale-deploy AssertionError).
- Verified: Snd init + startMusic no longer throw on any stage; stage 3 (new lvl3.wav) reaches play cleanly; full regression 11/11.
- NOTE for future: do NOT route the music elements through createMediaElementSource for a volume boost — it breaks playback. If music ever needs to exceed 1.0, pre-master the track files louder instead.

## Fix: broken special box floats the ORIGINAL special-ability icon (this pass)
- MISUNDERSTANDING corrected: I had the broken box float out its own inner glyph (spicon_<pilot>, extracted from powerupboxes.png). Mike wants the PRE-EXISTING special ability icons that existed before the boxes — the animated sp_<pilot>_<frame> art in assets/fx/special2/ (4-frame, all 7 pilots).
- FIX: the floating 'special'/'specialicon' pickup now draws the original animated sp_<pilot>_<frame> icon (frame cycles at ~9fps, spins + bobs, pilot-tint glow) as the PRIMARY. Fallback order: sp_ anim -> spicon_ (box inner glyph) -> special_ (box) -> tinted square.
- Unchanged: the falling crate (scrate) is still the new per-pilot box (special_<pilot>); collecting the floating icon still calls startSpecial().
- Verified: Yuri's broken box floats the original lightning icon (bright orange-red, 2260 colored px), and collecting it activates the special.

## HOTFIX: missile crates/boxes give bomb ammo again (this pass)
- BUG: the Raiden auto-missile change had repurposed the missilepack/missilepack10 pickups (dropped by the missile crate 'mcrate') to level up run.missileLevel instead of giving run.bombs. Result: missile crates/boxes stopped giving the bomb/missile ammo you fire with the bomb key.
- FIX: missilepack -> run.bombs +3, missilepack10 -> run.bombs +10 (restored, cap 99). The auto-missile LEVEL still comes only from the weapon-crate missile slot (wtype===2).
- HUD: the cx[3] slot shows the MISSILE AMMO count again (pips up to 6, then 'xN'). Added a small green auto-missile-LEVEL pip strip near the shield/speed icons in the HUD overlay so both systems are visible.
- Verified: missilepack gives +3, missilepack10 gives +10, bomb key consumes ammo; regression 11/11.
- Two systems recap: run.bombs = manual missile/smart-bomb ammo (bomb key, retina lock, Cole special) — filled by missile crates. run.missileLevel = auto homing missiles (fire while shooting) — filled by the weapon-crate missile slot; reset to 0 on death.

## FEATURE: Fullscreen mode (this pass)
- Added a fullscreen toggle to index.html (button top-right + the F key). Uses the native Fullscreen API (requestFullscreen/exitFullscreen with vendor prefixes) with a CSS-only fallback if the API is blocked.
- In fullscreen (body.fs class): the marquee + side cabinet art are hidden, the game-frame border/shadow are stripped, and the layout function (L) recomputes so the HUD strip + game screen scale to FILL the screen height (keeping the 480:512 aspect). At 1080p the playfield goes from the small cabinet window to ~963px tall (100% of height).
- Mouse controls unaffected: mpos() maps via getBoundingClientRect() normalized to VW/VH, so any display scale works.
- game.js unchanged — this is purely index.html (CSS + layout JS + fullscreen handlers). fullscreenchange listeners keep the body.fs class + button icon in sync (also handles the user pressing Esc).
- The F-key handler ignores Ctrl/Meta/Alt combos and text-field focus so it won't clash.

## Large batch: MG FX + smart enemies + death-freeze + Yuri zap cleanup + dogfight mirroring (this pass)
- **MG blue/red effects**: rewrote the low-level MG bloom -> now ALL levels get a WHITE inner core (bright ellipse) + a COLORED outer halo (larger, shadowBlur 16, the per-level tint) so the tracers read clearly over bright terrain (volcano/ice). Verified blue MG shows 748 blue px + white cores on the ice stage.
- **DEATH-ANIMATION bug** (enemies attacking you while dying): killEnemy now zeroes vx/vy (was *0.3, so they kept drifting at the player). Moved the _dyingT freeze to the TOP of the enemy update loop: a dying enemy freezes in place, does NO movement and NO firing, ticks its death timer (0.35s), then is removed. Verified an art enemy drifts <2px total after death (was sliding toward the player).
- **SMART SKY-DIVE ENEMIES**: new 'skydive' movement pattern. Enemy drops in fast from the top behind the player at ~0.35 scale, SCALES UP to full as it descends into the play plane, does a quick 0.28s turn beat to face head-on, then bears down and strafes to track the player. drawEnemy wraps the sprite in a canvas scale transform for the grow-in. Verified scale 0.35 -> 1 and phase descend->turn->attack.
- **TURRETS REMOVED**: all mgturret/rockturret spawns (4 waves) deleted — they didn't work. Replaced with skydive assault/gunship flanker waves. (The MUCH-smaller stationary turret-tanks are still a separate TODO with the incoming_0705b assets.)
- **YURI lightning stuck in air**: the zaps (chain-lightning bolts) cleanup lived inside updateSpecial(), which early-returns when no special is active — so bolts alive when the special ended froze forever. Moved the zap tick+filter into updatePlay (always runs) + a hard zaps.length=0 whenever Yuri's chain isn't active. Also added the same tick/clear inside the rival-fight loop.
- **RIVAL DOGFIGHT mirrors gameplay**: the dogfight player-fire block now runs the SAME logic as updatePlay — special-aware fire cadence (maverick 0.05 / yuri 0.14), the SAME autoFireMissiles() auto homing missiles while firing, updateSpecial(dt) so Yuri/Maverick/etc. specials behave identically, and the zap cleanup. It already reused pBullets/eBullets; now the firing/missile/special behavior matches too instead of being a reduced separate path. Verified auto-missiles fire in the dogfight (3 on screen). Required bumping the assemble.py "fire cd" anchor to n=2 (both the main-game and dogfight fire-cd lines now get the pilot fire-rate modifier).
- Regression 11/11; death-freeze, skydive, dogfight-missiles, MG-visibility all verified.
- NOTE: rivalPickups is still a small separate array for the in-fight missile CRATES only (they drop missilepack -> run.bombs, same pickup kinds as gameplay). The bullet/missile/weapon/special systems are now shared.

## Batch: small stationary turret-tanks re-wired (this pass) — completes the memory TODO
- **MICROTURRET**: new enemy type 'microturret' — a SMALL (w=18, renders ~27px via _foot=1.5, exempt from the global ES=1.3 upscale) stationary turret-tank that sits on the terrain (pattern:'ground', scrolls down with the map, never moves on its own) BELOW the player and fires STRAIGHT UP (-PI/2) at the player's lane.
  - Art: reuses esC_turretC2 / esC_turretC4 / trt_t1 emplacement sprites via ENEMY_ART.
  - Added a per-enemy _foot override in drawNewEnemyArt so it renders small without touching other enemies.
  - Fire behavior: new 'microturret' case in the enemy fire switch -> eShoot straight up with a muzzle flash.
  - Spawn waves on the ground stages (1 & 4): pairs/triples/a row of 4 at t=8/20/38s.
  - Verified: spawns small (27px), stays on ground pattern (scrolls with terrain), fires upward bullets.
- This is the replacement for the removed broken rotating turrets, per the memory TODO (small + stationary + below player + firing up).
- Regression 11/11.

## Batch: new stat-bar art wired (this pass)
- Extracted from stat_bars.png (magenta-keyed): the framed empty container (bar_frame) + 6 solid color fills (bar_red/blue/amber/purple/green/gray) -> assets/fx/statbars/, registered in manifest.
- Wired into the STAGE-CLEAR stats screen (drawStageClear in patches.js): each stat row now draws the colored fill art clipped to the count-up ratio, with the metal bar_frame overlaid on top, replacing the old flat rgba fillRect bars. Rows cycle through the 6 colors. Falls back to the old flat bars if the art isn't loaded.
- Verified bar_frame + fills load; the stats screen shows red/blue/green framed bars and runs clean on stages 1/3/5.
- NOTE: the pilot-select SPEED/FIRE/RANGE bars are baked into the card_<pilot> art images, not code-drawn, so they're unaffected. The extra segmented/small bar variants in the sheet (bands 7-9) are available for future use but not yet wired.

## HOTFIX: purple/magenta halos removed from stat bars (this pass)
- The extracted stat bars had magenta bg fringe on their edges (worst on bar_purple, but present on frame/blue/amber/gray too).
- Re-extracted from stat_bars.png with: (1) binary_erosion(1px) on the foreground mask to shave the anti-aliased magenta fringe before it becomes alpha, and (2) an EDGE-RESTRICTED despill — only halo pixels within 2px of transparency get neighbor-median-filled or dropped, so the genuinely-purple fill body of bar_purple is left intact.
- Result: bright-magenta border fringe = 0 on ALL 7 bars; 0 stray magenta px in the rendered stats screen.
- Only the PNGs (assets/fx/statbars/*.png) were overwritten in place — same paths/manifest keys, so NO code rebuild required.

## FIX: stat bars looked weird -> frame squash + opaque interior (this pass)
- Two real bugs behind "looks weird":
  1. The bar_frame (3:1 aspect) was being drawn at ~40:1 (VW-40 wide x 11px) so the ornate metal end-caps/bolts smeared into a flat line. FIX: 9-slice the frame horizontally — left/right caps drawn at aspect-preserved width (capD = barH*(capS/sh)), middle stretched. Also made the bar 15px tall (was 11) and moved it below the label.
  2. The extracted bar_frame's INTERIOR was opaque black (alpha 255), so drawing the frame over the colored fill completely hid the fill (bars rendered as empty black frames). FIX: flood-filled the interior from center and knocked it to transparent (kept only the metal border); feathered the border/hole edge. Now draw order = dark track -> colored fill (clipped to count ratio) -> frame border on top, and the fill shows through.
- Verified all 6 rows show distinct colors (red/blue/amber/purple/green/gray) with the fill visible inside the frame; interior fill-fraction ~0.5-0.65.
- bar_frame.png overwritten in place; patches.js drawStageClear bar block updated (9-slice + dark track).

## FIX: stop recoloring the STAGE CLEAR title (this pass)
- The "STAGE N CLEAR" title at the top of the stage-clear screen was drawn with stageText(..., theme, ...) where theme is a per-stage color tint (['#8de23a','#ff5a2a','#6fd0ff','#d8c068','#d07a3a']). Changed the tint arg to null in both branches so the title uses the stage bitmap font's OWN baked colors instead of being recolored.
- (The remaining per-stage color difference is just because curFontArt() returns each stage's own dedicated font, which have different native glyph colors — that's the artwork, not a recolor overlay.)

## FIX: portrait black gaps in dialogue/comm boxes (this pass)
- drawCommWindow (patches.js) drew the portrait with CONTAIN-fit + bottom-anchor. When the portrait's aspect didn't match the box (face_* are ~0.8 tall, but face_cole is 1.18 wide, and the box is a different aspect), contain-fit left black letterbox gaps inside the frame — the "area of black left in the frame" Mike saw.
- FIX: switched to COVER-fit (scale = max(bxW/w, bxH/h)) anchored to the TOP-center, clipped to the plate. The portrait now fully fills the framed box with no black gaps; overflow (shoulders/sides) is cropped instead of letterboxed, and top-anchoring keeps the face in view.
- Verified: black-gap fraction ~0.001 for the tall portraits; Cole's wide portrait fills cleanly (residual dark px are his art, not gaps). Regression clean.
- Applies everywhere drawCommWindow is used: GOOD LUCK launch screen, story dialogue, and rival dialogue.

## FIX: consistent colored comm-window borders for all 7 pilots (this pass)
- The dedicated dlg_<pilot> frame art has inconsistent/missing borders: axel/decker/freezer/juggernaut/yuri were missing the bottom edge, and maverick had NO top OR bottom. 
- FIX: after drawing the frame art, drawCommWindow now draws a CONSISTENT code-drawn 4-sided rounded border around the whole panel in the pilot's tint color — outer dark seat (6px) + main tinted border (3px, soft glow) + inner white bevel hairline + tinted corner accent ticks. This guarantees a complete colored frame for every pilot regardless of the art's gaps.
- Verified: maverick now has both top (y175) and bottom (y423) green borders; axel has a full-width blue bottom border; the border code runs identically for all 7.
- COLE chin fix: his face art is a tight wide crop (261x222) so cover-fit + top-anchor jammed his chin to the bottom edge. Adjusted the vertical anchor to allow a small headroom offset (clamped so it never exposes a gap). Cole's portrait plate now has ~43% dark backing below the chin = breathing room.
- Portrait fit unchanged otherwise (cover-fit, no black gaps from the earlier fix).

## FIX: pilot-select comm window stacking / wrong pilot (this pass)
- REAL BUG found (Mike saw "stacked decker cards, axel's big card, cut-off bottoms"): pickDiff() (the diff->pilot entry) did NOT reset the transient pilot-select state (pilotComm, pilotCommT, pilotPending, pilotSlide, pilotRot, pilotFlash). If any of those were stale from a prior visit/run, re-entering the pilot screen rendered the OLD pilot's GOOD LUCK comm window stacked on top of the current card — and the comm showed the wrong pilot (e.g. axel's blue border while decker's card was up).
- FIX: (1) pickDiff() now zeroes all six transient vars on entry. (2) belt-and-suspenders: drawPilot detects fresh entry (stateT<0.05) and clears pilotComm/pilotCommT/pilotPending/pilotSlide/pilotRot regardless of entry path.
- Verified: each pilot's comm now shows its OWN portrait + border color (outer edges distinct per pilot, no longer all axel-blue); full select->comm->intro flow works; re-entering the pilot screen is clean.
- NOTE: the earlier pilot_frames_fixed.png sheet that looked glitched was partly this bug + a capture-harness race (setPilotIndex+immediate-enter). Corrected capture uses real arrow-key navigation with full state reset between pilots.

## Portrait colored borders (this pass)
- Upgraded the portrait PLATE border in drawCommWindow from a thin single-line tint to a full layered colored frame in each pilot's tint: dark outer seat (4px) + main tinted border (2.5px, soft glow) + inner white bevel hairline + corner accent ticks. Matches the panel-border treatment, scaled to the portrait plate.
- Verified per-pilot border color via direct setPilotIndex capture: axel blue, decker gold, maverick green, juggernaut bronze, yuri red, cole green all MATCH their tints; freezer draws cyan (probe ambiguity from his purple armor accents, but the code uses his #6fd0ff tint like all others).
- CAPTURE-HARNESS NOTE (not a game bug): earlier 'wrong pilot' captures were a test-timing artifact — (a) checking run.pilot before the ~1.95s GOOD LUCK comm finishes (startRun sets run.pilot only when the comm completes), and (b) arrow-nav settle timing. The game selects the correct pilot: verified run.pilot=freezer after selecting index 3, run.pilot=maverick after index 2, full flow 3/3.

## FIX: drone hurt-state + Cole nuke conversion (this pass)
- **Drone "broken/death state but still alive & shooting"**: enemyArtState returned 'hurt' when hp<=40%. For the 3/4-POV drones the hurt art reads as a broken/destroyed frame, so a living low-HP enemy looked dead while it kept moving and firing. REMOVED the 'hurt' state — enemies now stay in normal idle/fire art until they ACTUALLY die (then the death anim plays via _dyingT, frozen, no firing). Verified a 30%-HP drone stays alive+shooting with normal art; dying enemies still freeze (earlier fix intact).
- **Cole special nuke conversion**: 
  - startSpecial for Cole now converts his EXISTING missiles to nukes: special.strikes=max(3, run.bombs) (was hard-set to 3, throwing away his ammo). So any bombs/missiles he's holding temporarily become black nukes.
  - Collecting missilepack/missilepack10 DURING Cole's special now adds nuke strikes (+3/+10) instead of normal missiles: special.strikes += N; run.bombs=strikes. Non-Cole pickups unchanged.
  - HUD nuke count now shows the real number (green pips up to 6, then 'NUKES xN') instead of a fixed 3 pips.
  - endSpecial still restores prevBombs (the nuke conversion is temporary, reverts to normal missiles when the special ends).
  - Verified: activating with 7 missiles -> 7 nukes; collecting +3 during special -> 10 nukes.
- Regression 11/11.

## FIX: scout purple halo + editor delivered (this pass)
- Scout (and all editor sprite art) had faint purple/blue-leaning DARK EDGE pixels (anti-alias fringe from the atlas) that read as a purple halo. Blackened ~65k such edge pixels across all editor art (dark edge px where b>=g and r>=g -> pure black), leaving the ships' legitimate interior shading intact. Also changed the editor canvas checkerboard from blue-grey (#12141c/#0d0f15) to neutral grey (#2a2a2a/#1e1e1e) so nothing reads as purple.
- NOTE: this cleanup was applied to the EDITOR's extracted art copies, not the in-game atlas (the in-game scout was already clean). 
- BOF Master Editor shipped: /mnt/user-data/outputs/BOF_Master_Editor.zip (single-file HTML app, loads bof_data.json + art/, edits all game data, places muzzle/engine/hit anchors on enemies/bosses/player, exports JSON). Extractor at /tmp/bof_editor/extract_data.py.

---
## Session: FALVA + LIZZIE — two new pilots (July 8)

### Roster
`PILOTS` grew 7 → 9. New entries sit **between YURI and COLE** (Cole stays last, locked):

| key | name | role | tint | font |
|---|---|---|---|---|
| `lizzie` | LIZZIE | BOMBSHELL | `#ffc21a` | 4 |
| `falva` | FALVA | THE OG | `#ff2a8f` | 2 |

**Portraits deliberately skipped** (no `face_*` / `dlg_*` art yet). `drawCommWindow` already falls back to `dlg_window` for the frame and `card_<key>` for the portrait, so the "GOOD LUCK, PILOT!" screen works — it just shows the card crop, same as Cole does today. Drop in `face_falva.png` / `face_lizzie.png` + `dlg_falva.png` / `dlg_lizzie.png` later and it upgrades with zero code changes.

### FALVA — ROLLER BALL (charge & release)
Her special replaces the fire button with a Mega Man X–style buster charge.

- `pShoot()` early-returns while `specialActive('falva')`; auto-homing missiles are gated off too (both in `updatePlay` and in the rival dogfight).
- `falvaCharge(dt)` (called from `updateSpecial`) reads `keybind.fire` directly.
  - `FALVA_FULL = 5.0s` — full power. `FALVA_ARM = 0.35s` — below this the tap is ignored.
  - Recurring charge tone: `falvaTick(p)` grabs the `blip` pool and climbs `playbackRate` 0.75 → 2.0 while the repeat interval tightens 0.20s → 0.09s (same `Snd.pools` + `preservesPitch=false` trick as `ragePlay`).
  - Particles spiral **inward** toward the ship; speed scales with charge.
  - At full charge: `Audio.SFX.select()` ping, shake, `FULL POWER` floater. (Uses the same `-0.02` epsilon as the release check so fp accumulation can't desync the two.)
- `drawFalvaCharge()` (drawn after `drawPlayer`, inside the shake transform), all additive:
  - `fchg_0..3` pink flame aura on the hull, frame picked by charge quartile
  - `forb_0..11` orbiting orb ring, 12-frame loop; **a second counter-rotating ring appears past 50%**
  - `fball_0..3` fading in above the ship — alpha `p^1.4`, growing 10 → 46 px, spinning
  - white/pink strobe over the ship past 62% charge, flashing faster as she tops out
  - a 44×4 charge meter under the ship
- Release (`releaseRoller(charge)`):

| | full (≥5s) | half (<5s) |
|---|---|---|
| radius | 23 | 12 |
| damage | 12 | 6 |
| lifetime | 10s | 5s |
| launch speed | 5.4 | 3.4 |
| release shards | 10 | 5 |

- `rollers[]` pinball physics in `updateRollers`: bounces off all four `PLAY` walls, ploughs **through** normal enemies (`hitCd` 0.05s), **ricochets off** bosses/sub-bosses/the rival (reflected along the contact normal, `hitCd` 0.22s), and shreds any enemy bullet it rolls over. Every impact calls `rollerImpact()` → explosion + shrapnel + a `fburst` flash. Death at `life<=0` sprays 12 more shards.
- If the 15s special timer expires **while she's still holding**, `endSpecial()` auto-fires whatever charge she had (≥ `FALVA_ARM`).

### Pink shard shrapnel (`shards[]`)
14 crystals cut as individual components out of `pinkdebris.png`, normalized to 48px sprites, drawn 9–17px with rotation + pink glow. Spawned on ball release, every wall/enemy/boss impact, ball expiry, and the atom blast. Each shard does 1 chip damage (2 from a full ball's impacts) to the first enemy/boss/sub-boss/rival it touches, then dies. Drag + slight gravity, 0.45–0.95s life. `fburst` (the whole debris sheet) doubles as the impact flash.

### LIZZIE — ATOM BOMB
Mirrors Cole's structure so it reuses the retina lock plumbing.

- `startSpecial('lizzie')` → `special.strikes = max(3, run.bombs)`; `endSpecial` restores `run.bombs`.
- `lizzieFire()` is the exact analogue of `retinaFire()`: it **consumes the missile key** and returns `true` while her special is up. Wired at both `keybind.bomb` sites (`if(!retinaFire() && !lizzieFire()) useBomb();`) and inside `updateRetina`'s hold-to-fire branch. `cycleLock()` no longer demands `run.bombs>0` for her.
- Bullet `kind:'atom'` — `lz_bomb` sprite, wobbles, exhaust puff, drifts up (or homes lazily onto a retina target at 4.4 px/f). Fuse: 0.85s unguided, 2.4s guided. Detonates on fuse, on the top of `PLAY`, or on first contact with anything.
- `atomBlast(x,y)` → `lz_nuke_0..3` mushroom cloud (`atomBooms[]`), 190→420px over 1.35s, drawn with its **base at the impact point** (`y - h*0.86`). Shake 26, `flashScreen` 0.95, `whiteBlast` 0.8, wipes **all** enemy bullets, 90 dmg inside r=170 / 26 dmg inside r=300, 85 to boss+sub-boss, 55 to the rival, and pops nearby containers.
- HUD: her `SPECIAL` bar shows `A-BOMBS x N` (gold) exactly like Cole's `NUKES x N` (green). Falva's shows `CHARGE nn%` → `ROLLER BALL READY`.

### Art wired (64 new BOFX keys, all verified 0 cyan residual)
| keys | source | path |
|---|---|---|
| `ship_falva{,_t,_l,_r}` | `pinkship.png` | `assets/ships/` |
| `ship_lizzie{,_t,_l,_r}` | `yellowplane.png` | `assets/ships/` |
| `card_falva` / `card_lizzie` | `falvacard.png` / `lizziecard.png` | `assets/ui/cards/` |
| `special_falva` / `special_lizzie` | `pinkbox.png` / `yellowbox.png` | `assets/fx/specialboxes/` |
| `sp_{falva,lizzie}_0..3`, `spicon_*` | `pinkpowerup.png` / `yellowpowerup.png` | `assets/fx/special2`, `specialicons/` |
| `fball_0..3` | `pinkball.png` | `assets/fx/falva/` |
| `fchg_0..3` | `pinkcharge.png` | `assets/fx/falva/` |
| `forb_0..11` | `pinkcharge2.png` (3×4) | `assets/fx/falva/` |
| `fshard_0..13`, `fburst` | `pinkdebris.png` | `assets/fx/falva/` |
| `lz_bomb` | `yellowbomb.png` | `assets/fx/lizzie/` |
| `lz_nuke_0..3` | `nukefx.png` (2×2) | `assets/fx/lizzie/` |
| `msl_falva` / `msl_lizzie` | `pink yellow missiles.png` | `assets/fx/library/missiles/` |

`PILOT_MSL` + `PILOT_MSL_FAT` now map `falva → msl_falva`, `lizzie → msl_lizzie`, so their homing missiles use the new art automatically.

### ⚠️ BUILD PIPELINE HAZARD (important, changed this session)
**`build_ext.py` is now destructive — do not run it.** `bofx.json` has gone stale (**127 keys**) while the deployed `assets/manifest.js` carries **1307**. `build_ext.py` regenerates the manifest *from* `bofx.json` and would delete ~1180 asset keys.

The working pipeline is now:
```
python3 assemble.py                  # gamecode.js + patches.js -> gamecode_patched.js
node --check gamecode_patched.js
cp gamecode_patched.js ../assets/game.js
python3 register_fl_manifest.py      # append new BOFX keys to assets/manifest.js (idempotent)
node /tmp/test_fl.js                 # expect "==== FALVA/LIZZIE BUILD OK, 0 ERRORS ===="
```
`add_stage_s.py` only needs re-running if `build_ext.py` ever regenerates the atlases. (`assemble.py`'s trailing `FileNotFoundError` on `bofbuild/` is expected and harmless.)

New scripts in `_BUILD_SOURCE/`: `fl_lib.py` (chroma key + edge despill + component/band cutting + `scrub()` post-resize halo kill), `extract_fl_ships.py`, `extract_fl_fx.py`, `register_fl_manifest.py`, `test_fl.js`.

### Verification
`test_fl.js` — 48 assertions, all green: manifest keys + on-disk paths, roster shape, charge saturation, full-vs-half stat table, sub-threshold tap ignored, all four wall bounces, roller + shrapnel damage, atom spawn/spend/detonate/cleanup, `endSpecial` auto-fire and bomb restore, draw fns issue `drawImage` without throwing, and **420 live frames of `updatePlay` + `drawWorld` per pilot** with no exceptions. Numeric halo audit: **0 cyan residual pixels across all 64 new sprites**. Composited proof frames in `_QA_RENDERS/`.

### Not done (deliberate)
- **Portraits / dialogue frames** for both pilots — Mike is making them.
- `lifehudicons.png`, `missilehudicons.png`, `shieldreplacements.png` — shipped in the drop but out of scope for this pass; staged unwired in `src/incoming_falvalizzie/`.
- Stage 6 assets from `src/incoming_0705b/` still unwired.

### Addendum — headless renderer + a bug it caught
Added `_BUILD_SOURCE/render_movie.js` (+ `render_fl.js`): boots `manifest.js` + `game.js` in a `vm` on **node-canvas** with an `Image` subclass that resolves the manifest's relative paths straight off disk, then drives the real `updatePlay` + `drawWorld` and dumps 60fps PNG frames. Two gotchas if you re-run it:
1. `ASSETS.ready` never flips, because the loader attaches `A.img.onload` *after* setting `.src` and our loader is synchronous. Force `ASSETS.ready=true` after loading.
2. `loop()` applies `ctx.setTransform(SS,0,0,SS,0,0)` (SS=2 supersample) every frame. Replicate it or you render at 1x into the top-left quarter of a 960×1024 buffer.

**Bug it caught:** `atomBlast` originally raised `whiteBlast`. `whiteBlast` is *owned* by the boss-death whiteout (`b.T`-driven, set every frame) and is never decayed anywhere else — so an A-bomb left the screen permanently white-washed. Replaced with a self-owned `atomFlash`, decayed inside `updateAtomBooms` (so it works in the rival dogfight too, which has its own update loop and does **not** decay `flashScreen`/`bombFlash`). Drawn in `drawAtomBooms` as an oversized rect (`-48,-48,VW+96,VH+96`) so the screen-shake translate can't reveal an edge. Regression asserts added to `test_fl.js`.

### Addendum 2 — a node-canvas rendering bug (NOT a game bug)
While previewing, the headless renders showed hard-edged pink/maroon boxes behind every glowing sprite, and Falva's charge whited out her hull. Bisected with `_BUILD_SOURCE/sublayer.js` + `shadowprobe`:

> **node-canvas fills an image's bounding box with `shadowColor` whenever a scale transform is active.**
> `plain`, `rotate`, `shadowBlur`, and `rotate+shadowBlur` all render the ring's hole correctly.
> `setTransform(2,0,0,2,0,0) + rotate + shadowBlur` fills the hole solid.

The engine renders through `ctx.setTransform(SS,0,0,SS,0,0)` (SS=2), so every `drawImage` with a `shadowBlur` (the roller ball, the orb rings, the mushroom cloud) grew a filled rectangle. Browsers render image shadows as a blurred alpha silhouette and do not do this. **The boxes never existed in the actual game.**

Fix (renderers only): draw at identity transform and crop the top-left 480×512 out of the 960×1024 backing canvas. `render_movie.js`, `hulltest.js`, `sublayer.js` all do this now. Cost: previews lose the 2× supersample, so they're very slightly softer than the browser. Everything else is faithful.

### Addendum 3 — charge-FX rebalance (real fixes)
Independent of the renderer bug, three things were genuinely wrong:
1. **`fchg` is white-hot art.** Drawn `lighter` at alpha 0.61 plus an additive orb ring at 0.9 saturated the whole ship to pure white. Aura alpha is now capped (`0.26 + p*0.28`) and drawn **under** the ship (`drawFalvaAura()` before `drawPlayer()`), with the orbs **over** it (`drawFalvaOrbs()` after), so the hull always reads.
2. **The orb rings were slicing through the hull.** Measured the art: its ink starts at 0.58 of the half-width, so the opaque band's inner radius is ≈0.29·d. Her hull's half-diagonal is ~34px, so anything under ~118px cut across the ship. Rings are now `d = 100 + p*40` (plus a wider counter-rotating one at 1.26×) and drawn **source-over**, not additive — the art already carries its own pink body and white orb nodes.
3. **The white strobe was a filled disc** over the ship. Replaced with a thin strobing rim ring plus a strobing `shadowColor` on the ship itself, so she flashes white/pink and stays visible.

Verified with `hulltest.js`: renders the ship alone on a flat backdrop, diffs to get the exact 781-pixel hull mask, then measures how many of those pixels survive the FX stack. **82–90% of the hull reads unobscured at every charge level, <3.2% white-blown, orbs clearly present in the r45–95 annulus.**

Also removed (Mike's call): the full-screen orange `flashScreen` wash from `atomBlast` **and** from `releaseRoller` (both now use the self-decaying white `atomFlash`), and the `shadowColor='#ffb02a'` bloom around the mushroom cloud. Peak orange coverage during a detonation is now 44% vs a 30% jungle baseline — i.e. the cloud art itself, no screen tint. The flat pink disc behind the roller ball is now a radial-gradient falloff.

### Addendum 4 — A-bomb detonation staging
Mike's note: *"when it detonates, the screen should go blinding white and restore so we don't see the explosion disappear and get larger too much."*

- `atomFlash` is armed to `ATOM_HOLD = 1.34`, not 1.0. The draw clamps alpha to 1, so the extra 0.34 of headroom (÷ the 2.0/s decay) buys **~0.17s of a completely opaque white screen** before it starts fading. Full restore at ~0.33s.
- The white rect now draws **after** the clouds inside `drawAtomBooms()`, so it blankets the mushroom's birth entirely.
- The cloud is born big and grows gently: `w = 330 + p*120` over `dur = 1.9s` (was `190 + p*230` over 1.35s). Its first ~0.35s happens behind the white-out, so when the flash lifts you see an already-formed mushroom. Measured on-screen growth: **3%, down from 121%.**
- Tail fade eased to `pow(1-(p-0.68)/0.32, 1.4)` over the last 32% so the cloud dissolves instead of popping.

Measured on the re-render: 99.9% pure white at the detonation frame, held for 11 frames, fully restored by frame 20. (The 235/254 row alternation in raw pixel dumps is the game's own CRT scanline overlay, not a flash artifact.)

### Addendum 5 — secondary cook-offs around the blast
The mushroom sprite's base is a straight horizontal band, which read as a drawn "line" laid over the terrain. `_atomSecondaries(x,y)` builds a **22-entry, time-sorted schedule** of ordinary engine `explode()` calls, drained one at a time by `updateAtomBooms()` as each timestamp comes up:

- **10 along the base band** — alternating left/right, marching outward from the impact (`26 + step*32` px, jittered ±14). The first pair fires at ~0.24s, *behind* the white-out, so they're already burning when it lifts.
- **8 scattered around the fireball** — random angle in the upper hemisphere, radius 48–155px, y squashed to 0.55 so they hug the cloud's shape rather than ringing it.
- **4 late low pops** — 0.7–1.3s, `±165px` horizontally and 12–34px *below* the base line, specifically to chew up the hard bottom edge.

All clamped inside `PLAY`. Each pop adds `shake` scaled to its radius, a 45%-chance `expSmall()`, and three ember particles.

Measured on the re-render: base-band bottom-edge stddev climbs **6.0 → 17.0** over the blast (a flat line would sit near 0), 86–379 distinct blobs at any moment, and the lit band spans **455px against a 360px sprite** — the cook-offs reach past the cloud's own edges.

---
## PERF: the framerate cliff (baked-glow cache)

**Symptom:** ~8fps once missiles hit lv3-5 and the weapon was upgraded and the screen was full of shots.

**Diagnosis** (`_BUILD_SOURCE/bench2.js`, `attrib.js`):
```
updatePlay : 0.43 ms/frame     <- not the problem
drawWorld  : 39.78 ms/frame    <- all of it
  drawBullets  14.63 ms
```
`ctx.shadowBlur` on a draw is the single most expensive canvas operation in a browser — each one forces a separate blur pass. The bullet layer was doing **one to four of them per bullet, per frame**:

| site | cost |
|---|---|
| `drawMfx()` | 1 blurred `drawImage` per bullet, **2** if a `glow2` halo was passed (spread + machine gun) |
| machine-gun tracer | **2 blurred vector fills** (`arc` + `ellipse`) per bullet, *before* `drawMfx` even ran |
| wave beam | **2 blurred `ellipse` fills per segment**, ~10 segments per beam |
| laser | 2 blurred passes over a tall rect |
| firewall / shards | 1 each |

Measured across the five weapons at level 5 + level-5 homing missiles: **137 blurred draw calls per frame.**

**Fix:** rasterise "sprite + its glow" **once** into an offscreen canvas per `(key, size, tint, glow colour, blur, composite, alpha)` and blit it flat forever after. `bakeGlow()` for sprites, `glowBlob()` for the vector tracer cores and beam pulses. Zero `shadowBlur` in the hot path.

```
weapon        blurred draws/frame        node-canvas ms/frame
              OLD    NEW    cut          OLD     NEW
machine gun    64      1    98%         115.5   67.5
spread         61      1    98%          60.5   49.7
wave            9      1    88%          44.7   36.9
homing          3      3     -           93.5   73.6
laser           1      2     -           34.9   37.1
TOTAL         137      8
```

### Three subtleties that had to be right for the visuals to be unchanged
1. **`shadowBlur` IS scaled by the CTM** (verified: a blur-16 dot renders a 4.2px glow at scale 1 and 14.4px at scale 2). So a glow baked at 1× and blitted through the engine's `SS=2` transform lands at exactly the device-space size the live path produced. No compensation needed.
2. **`'lighter'` composites the shadow AND the source separately.** A layer baked source-over would have the sprite painting over its own glow, making the halo dimmer. `bakeGlow`/`glowBlob` take an `additive` flag and build the offscreen with `globalCompositeOperation='lighter'` when the blit will be additive.
3. **Per-element alpha ≠ group alpha under source-over.** The laser drew its bloom at `globalAlpha=0.5` and its core at `0.98`. Baking those layers and blitting them at 0.5/0.98 is *not* the same image. Since source-over is associative, the fix is to bake the element alpha **into** the layer (`bakeA`) and blit at 1.0 — which is exact.

Also: `drawBullets()` now zeroes `ctx.shadowBlur` on entry, and every baked blit zeroes it too. An upstream draw was leaking a live shadow into the bullet layer, silently blurring sprites that were already pre-blurred.

### Verification
- `_BUILD_SOURCE/pixdiff.js` — renders a static, deterministic bullet field twice (live-shadow vs baked) and diffs. All five weapons: **>8-level differences on 0.05–0.11% of pixels** (antialiasing only). Verdict: identical.
- `_BUILD_SOURCE/cachestress.js` — 9 pilots × 6 weapons × 3 levels, 6480 frames: **48 baked sprites + 10 blobs, 1.1 MB total, 99.93% cache hit rate**, never approaches the 512/256 caps.
- `test_fl.js` §14 — cache identity, additive-vs-source-over keys, blur padding, no `shadowBlur` leak from `drawMfx`, and **0 new bakes** during a 2s maxed burst (steady state).

Escape hatch: `_GLOW_CAP` / `_BLOB_CAP` are `let`. Set either to `0` at runtime to force the original live-shadow path (used by the A/B benchmarks).

---
## DROP 2026-07-12 — Part 1 of N: visual wiring (portraits, dialogue boxes, reticles, engine rename)

This is the first slice of a large multi-part drop. Landed the pure-visual pieces first (per Mike's priority). Still TODO in later parts: barrel-roll system (pivot + 8-frame roll atlases, double-tap dodge, i-frames), animated thrusters (all ships, palette-swap), Falva roller-ball rework (2 anchored orbit-orbs firing straight + spread lasers as an offensive shield for the full 15s special), pink/yellow retina orbs + lasers + missiles from the drop.

### Portraits — Falva & Lizzie (7 emotions each)
`_BUILD_SOURCE/extract_fl_portraits.py` slices `falva-expressions-7f.png` and `lizie-expressions.png` (both 7 even frames: idle, smile, anger, laugh, sad, victory, crash). Each frame is a colored border box with the character inside; we crop the character out (inset ~5.5% x / 3% y to shed the drawn border), key black→transparent, tight-bbox, normalise to 265px tall to match the existing `port_*` art. Output `assets/ui/portraits/{falva,lizzie}_{emo}.png`, keys `port_{falva,lizzie}_{emo}`.

**Zero code change to light these up** — `pilotPortrait(pilotKey, emo)` already resolves `port_<pilot>_<emo>` with an idle fallback, and the in-game dialogue driver (gamecode ~5282) already calls it. One tweak: `drawPilotComm` (the launch "GOOD LUCK PILOT" screen) hardcoded `face_<key>`; changed to `pilotPortrait(P.key,'idle')` so the girls show their idle portrait there too (was falling back to the card crop).

### Dialogue boxes — pink Falva / gold Lizzie
`_BUILD_SOURCE/make_fl_dialogue.py` hue-rotates the pure-blue `dlg_axel.png` box. Only saturated (colored border) pixels are recolored; neutral metal bevel + inner darkness are preserved via an HSV swap that leaves low-saturation px alone. Falva → hue 327° (#ff2a8f family), Lizzie → hue 44° (#ffc21a gold), with small sat/value tweaks. Output `assets/ui/dlg_{falva,lizzie}.png`, keys `dlg_{falva,lizzie}`. `drawCommWindow` already picks up `dlg_<key>` via `frameKey`, and draws its own tinted 4-sided border over it in the pilot color — so the frame reads correctly even though the swap only recolors the art.

### Reticles — pink Falva / gold Lizzie
`_BUILD_SOURCE/extract_fl_reticles.py` cuts the 4×4 `Pink_Gold_Reticles_Crosshairs_Atlas.png` (rows: pink-box, gold-box, pink-circle, gold-circle; cols: acquire, partial, strong, confirmed-burst). We use the BOXED rows to match the existing boxed-reticle pilots (axel etc.). Falva → pink box row, Lizzie → gold box row. Both the seek (`retA_<pilot>_0..3`) and lock (`retB_<pilot>_0..3`) keys get the same 4 progression frames, matching how the boxed pilots already work. Cyan key + edge despill (the AA fringe against cyan needed a second scrub pass → 0 cyan residual). `drawRetina()` already resolves `retA_/retB_<pilot>_N` and tints the glow with `_pilotTint()`, so **no code change** — pink/gold lock reticles appear automatically.

### Engine rename → "ColeForge Phoenix Engine"
- Options screen name string (`B_OPTIONS`) and credits (`gamecode` ~5895) now read "COLEFORGE PHOENIX ENGINE" (was "COLEFORGE ENGINE \"SHUMP EDITION\"").
- New logo: `Phoenix_Engine2.png` (magenta-keyed, despilled) → `assets/ui/phoenix_logo.png`, and swapped into the `menuLogo` slot (`assets/ui/menuLogo.png`, old one backed up as `menuLogo_shump_backup.png`). Native aspect preserved (1.61); the boot/menu draw code sizes by width so it just centers taller.

### Registration
`_BUILD_SOURCE/register_fl_visuals.py` — 32 new keys (14 portraits + 2 dialogue + 16 reticles) appended to the deployed `assets/manifest.js` (now 1339 img keys). Idempotent, round-trip verified, does NOT run build_ext.py. menuLogo swap is a same-path file replace so needs no manifest change.

### Verified
Headless renders (`/tmp/render/commrender.js`, `reticlerender.js`): both comm windows composite correctly (pink box + pink portrait frame for Falva, gold for Lizzie, showing idle/anger/laugh emotions), and the lock reticles render pink/gold with the engine tint-glow. `test_fl.js` still green (61 assertions). 0 cyan residual across all 32 new sprites.

---
## DROP 2026-07-12 — Part 2: pivot + barrel roll (Yuri wired as the example)

### Frame extraction
`_BUILD_SOURCE/extract_ship_frames.py` cuts a combined ship atlas (row0 = 5 pivot frames, row1 = 8 barrel-roll frames) onto a COMMON 203×271 canvas, each frame centered on its content centroid so the hull's visual center stays fixed across the animation (verified: all frames land at cx≈101, matching the existing `ship_yuri` base). Handles both the magenta-key atlases (most pilots) and the cyan-key ones (Falva/Lizzie), with edge-despill scrub. Output naming:
- `ship_<pilot>_pv0..4` — pivot: hard-L, soft-L, neutral, soft-R, hard-R
- `ship_<pilot>_br0..7` — roll: neutral/top, diag, side, diag, inverted-underside, diag, opp-side, diag-return

Registered via `_BUILD_SOURCE/register_ship_frames.py` (idempotent; globs `ship_*_pv[0-9]`/`_br[0-9]`). Manifest now 1352 img keys.

**Only Yuri is extracted so far** (Mike's chosen example). The other 8 ships' atlases are staged in `src/incoming_drop_0712/ship_production_pack/` and just need running through the same script (girls use `cyan=True`; the combined-atlas pilots use `cyan=False`). The engine already falls back to the old atlas `player_l/_r/player` sprite for any pilot without `pv`/`br` art, so nothing breaks in the meantime.

### Barrel roll (double-tap dodge, i-frames)
New player state: `player.roll`, `player._tapL/_tapR` (double-tap timestamps), cleared in `reset()`.
- Constants: `BR_WINDOW=0.26` (max s between taps), `BR_DUR=0.46` (roll length), `BR_DASH=190` (lateral px), `BR_COOL=0.18` (post-roll lockout).
- `startRoll(dir)` — sets the roll, grants i-frames spanning the whole roll (`ceil(BR_DUR*60)+4`), plays a dash SFX. Guarded by cooldown + not-already-rolling + not-dead.
- `updateRoll(dt)` — ease-out lateral dash (`1-(1-t)²`) so it's fast at the start and settles; clamps to PLAY; ends → sets `_rollCool`.
- `rollFrameKey()` — returns `ship_<pilot>_br<0..7>` by roll progress, or null (fallback pilots dash without the spin art).
- Movement loop: double-tap detection on `Input.tap` of the left/right binds runs BEFORE normal movement; while rolling the roll drives x (only a small vertical nudge allowed) and **primary fire is suppressed** (`firing = !_rolling && ...`).
- Draw: in `_drawPlayerCore`, the roll frame is drawn BEFORE the invuln-blink early-return (so the spin stays solid instead of strobing off during the i-frames), at 64px with a pilot-tint motion glow + thruster flame, then returns.

### Pivot banking wired into gameplay
When `ship_<pilot>_pv2` exists, gameplay banking uses the new frames: a smoothed `player._bank` follows horizontal motion (eases via `dt*12`), mapped to `pv0..4` (60px). Falls back to the old atlas `player_l`/`player_r`/`player` otherwise. Verified: full-speed right → pv4 (hard right), left → pv0 (hard left); slower nudges land on the soft frames.

### Verified
`test_fl.js` §15 — 12 barrel-roll assertions, all green: has-roll-art, no-roll-without-double-tap, startRoll dashes 190px right, i-frames granted, lasts ~0.47s (28 frames), cycles 8 distinct br frames, cooldown blocks re-roll, leftward roll dashes left, fallback pilot still dashes. Full harness green.
Headless renders: `/tmp/render/roll_movie.js` (Yuri dodging bullet streams) and `/tmp/render/pivotroll_movie.js` (pivot banking rt/lf/rt then two barrel rolls). Numeric verify: ship travels the full dash distance at the roll trigger points; bank index tracks steering direction.

---
## DROP 2026-07-12 — Part 2b: pivot turns animate in + banked hitbox shrink

Refinement of the pivot from Part 2, per Mike: turning should ANIMATE through the intermediate pivot frames into the hard bank (instead of the old code snapping straight to the hard frame at full speed), and the ship's hitbox should shrink when banked (edge-on = slimmer target).

### Bank now driven by hold-time, not per-frame velocity
Old: `want=clamp(dx*0.5,-1,1)` — `dx` (per-frame x delta) saturates to ±1 instantly at full speed, so you jumped to the hard frame.
New: in `updatePlay`, `player._bank` ramps toward ±1 over ~0.32s while a direction is held (`Input.lf/rt`, or the roll direction when rolling), and eases back to 0 over ~0.18s on release. `_drawPlayerCore` just reads `player._bank` and picks `pv0..4`. A held turn now visibly steps neutral(pv2) → soft(pv3) → hard(pv4). Verified: at 60fps the pv index touches 2,3,4 in sequence over ~13 frames.

### Banked hitbox
Each frame, from `ab=|_bank|`: `player._hx = 9*(1-0.45*ab)` and `player._hy = 10*(1-0.12*ab)`. So neutral is the old 9×10 half-extents; full bank is ~5.0×8.8 — 45% narrower horizontally, a hair shorter vertically (the ship is rolled edge-on, so mostly width shrinks).

Centralised the previously-scattered hardcoded player hitboxes to read `player._hx/_hy`:
- enemy bullets (was `<9`/`<10`)
- enemy ram (was `+8`/`+8`; uses `_hx-1`/`_hy-2` for the body-overlap feel)
- enemy missiles/rockets (was `<10`/`<12`)
`_hx/_hy/_bank` initialised in `player.reset()` and default-guarded everywhere (`player._hx!=null?...:9`) so nothing breaks if a code path runs before the first `updatePlay`.

### Verified
`test_fl.js` §16 — 8 assertions: neutral hitbox ~9×10; bank ramps gradually (0.16 after 3 frames, not slammed to 1); passes through the soft range; reaches hard-right after holding; monotonic ramp; banked hitbox 45% narrower; eases back on release; and a grazing bullet at x+7.5 that would clip the neutral ship MISSES the banked ship. Full harness green (81 assertions).
Renders: `/tmp/render/pivot_anim_movie.js` (hold-turn animating in, both directions, then a banked dodge). `yuri_hitbox_compare.png` shows the two hitboxes to scale.

---
## DROP 2026-07-12 — Part 2b CORRECTED: pivot = roll into the edge-on 180 pose

Mike clarified: the pivot pose is NOT the gentle pv-frame banks (row 0 of the atlas). It's the frame in the BARREL-ROLL sheet where the ship has rolled 180 and is fully edge-on. Turning should roll the ship INTO that edge-on pose.

### What changed from the first 2b attempt
Measured the roll-frame content widths: **br2 (74px) and br6 (73px) are the edge-on 180 poses** (mirror images — one rolled left, one right), vs br0/br4 which are the wide top/bottom views. So the pivot now maps the bank onto the ROLL frames, not the pv frames:
- neutral (|bank|<0.02) = br0 (top-down)
- turning RIGHT walks br0 -> br7 (partial, |bank|<0.5) -> br6 (full edge-on right)
- turning LEFT  walks br0 -> br1 (partial) -> br2 (full edge-on left)

The pv0..4 frames are no longer used for the player pivot (kept in the manifest; harmless). The bank is still hold-ramped in updatePlay (Part 2b), so the roll animates in through the partial frame and eases back to br0 on release.

### Hitbox re-aligned to the rolled silhouette
Stepped to match the actual frames instead of a linear ramp: neutral wf=1.0 (hx 9), partial-roll wf=0.72, full edge-on wf=0.5 (hx 4.5). At game scale the drawn hull measures 42px wide neutral -> 17px edge-on (~40%), so the 50%-width hitbox at full pivot is well matched. Vertical barely changes (`_hy=10*(1-0.10*ab)`).

### Verified
`test_fl.js` §16 rewritten (11 assertions, all green): neutral=br0; turning right passes br7 then settles br6; animates in (no snap straight to br6); edge-on hitbox ~4.5 (50% narrower); turning left passes br1 settles br2; releasing returns to br0; and a grazing bullet at x+7.3 that clips the neutral ship MISSES the edge-on pivoted ship. Full harness green (relaxed one flaky pre-existing secondary-explosion stagger threshold 0.8->0.7s).
Frame geometry confirmed independently: br0 draws 42x52px hull at 60px scale, br6/br2 draw 17x54px (edge-on). `yuri_hitbox_compare.png` shows br0 vs br6 with hitboxes to scale.

---
## DROP 2026-07-12 — Part 2c: turn animates through angled banks INTO the twist

Mike uploaded the target twist pose (edge-on, aspect 0.34) and clarified the desired ANIMATION: turning should animate from the angled left/right bank frames (the pv row) INTO the twist frame, not jump straight to it. So the pivot now uses BOTH frame sets in sequence.

### Frame path (hold-ramped bank drives it)
Right turn: `pv2 (level) -> pv3 (soft angled bank) -> pv4 (hard angled bank) -> br6 (edge-on twist)`.
Left turn mirrors: `pv2 -> pv1 -> pv0 -> br2`.
- bank <0.06 -> pv2
- bank 0.06..0.5 -> pv3/pv1 (soft angled)
- bank 0.5..0.82 -> pv4/pv0 (hard angled)
- bank >=0.82 -> br6/br2 (twist)
The bank ramps to full in ~0.32s (Part 2b), so holding a turn walks the whole sequence and reaches the twist in ~0.25s; releasing eases back down through the same frames to level. Falls back to a br-only path for any pilot that somehow has br art but not pv art, and to the old atlas sprite for pilots with neither.

### Hitbox: full through the angled banks, collapses at the twist
Only the twist is edge-on (the pv bank frames are still full-width top views), so: level/soft wf=1.0 (hx 9), hard angled bank wf=0.85, twist wf=0.5 (hx 4.5). `_hy=10*(1-0.06*ab)`. So you only get the slim dodge hitbox once you've committed the turn all the way into the twist — matching what's on screen.

### Verified
`test_fl.js` §16 (11 assertions, all green): level=pv2; right turn sequence is exactly pv2->pv3->pv4->br6; hard-bank pv4 precedes the twist br6; turn ends on br6; twist reached in 0.25s; twist hitbox ~4.5; soft-bank keeps a ~9 hitbox (only the twist shrinks it); left mirror pv2->pv1->pv0->br2; release returns to pv2; grazing bullet at x+7.3 misses the twisted ship. Full harness green.
`yuri_twist_sequence.png` shows the four actual game frames in order.

---
## DROP 2026-07-12 — Part 2d: BUGFIX — pivot was intercepted, never reached the twist in-game

Mike reported the video only showed the mild bank, never the twist. Root cause: **assemble.py patch #18** injected an OLD `_t/_l/_r` select-screen banking block at the top of the `ASSETS.has('player')` branch in `_drawPlayerCore`, and it `return`ed before the new pv->twist pivot block (added in Parts 2b/2c) could run. So gameplay drew `ship_yuri_t/_l/_r` (the gentle select-screen banks) and the pv/br twist code was dead.

Fix: removed patch #18's span-replacement entirely (the pivot is now authored directly in gamecode.js). The `_t/_l/_r` frames are no longer used for the gameplay player (still used by the rival dogfight via drawRivalShip, which is untouched).

### Verified with real pixel measurement (rendered from the actual game draw)
Hull width on black at each bank, from `_drawPlayerCore`:
- level (pv2): 90px
- soft bank (pv3): 90px
- hard bank (pv4): 89px
- TWIST (br6/br2): **31px**  (66% narrower)
`yuri_twist_proof.png` shows the four frames. Drawn-key trace confirms the sequence pv3 -> pv4 -> br6 while holding a turn. This is the FIRST build where the twist actually renders in gameplay. Harness green.

Lesson (added to build notes): assemble.py's anchored span-replacements can silently shadow later-authored code when they inject a `return` ahead of it. When a draw change "doesn't take", check assemble.py patches that anchor on the same line, not just gamecode.js.

---
## DROP 2026-07-12 — Part 2e: BUGFIX — wingtips clipped in extracted pivot frames

Mike spotted Yuri's wings cut off. Cause: `extract_ship_frames.py` forced every frame onto a fixed 203x271 canvas, but the pivot (pv) frames are 218-227px wide in the source atlas — wider than 203 — so ~12px of each wingtip was clipped. (The br roll frames fit, so only the wide pv banks were affected.)

Fix: rewrote the extractor as a two-pass fit. Pass 1 tight-crops every frame. Then it computes a single uniform scale so the tallest frame's content height = 82% of the canvas height (matching the base ship_<pilot> fill ratio, so on-screen size is unchanged), sizes the canvas WIDTH to the widest scaled frame + 12px margin each side, and centers every frame on that common canvas. Result: nothing clips, and because the scale is uniform and driven by height, apparent on-screen size is identical to before (~48-49px tall, same as the base ship).

Verified: 0 clipped frames across all extracted pilots; pv2 now has 13/14px clear margin at the wingtips (was flush to the edge = clipped); drawn hull widths unchanged (level ~91px, twist ~28px device-2x); apparent height 48px matches base ship 49px. Full wingspan confirmed in the ASCII map (both wingtips present, symmetric).

### Also extracted 5 more pilots with the fixed extractor
While fixing, ran axel, decker, freezer, juggernaut, maverick through the corrected extractor (all combined magenta-key atlases, all clean, canvases 178-220px wide per their wingspan). 6 pilots now have pivot+roll frames (78 keys, manifest 1417). Still TODO: **cole** (its atlas row1 frame-detection found 5 not 8 — frames likely touch; needs a per-atlas gap tweak) and **falva/lizzie** (separate cyan-key pivot+roll STRIPS, not a combined 2-row atlas, so they need a different loader path). Those 3 fall back to the flat sprite until done.

---
## GIF encoding fix — color loss

Mike reported GIFs losing color. Cause: the GIF encode was capping the palette at 96-128 colors with heavy Bayer dithering (`max_colors=112`, `bayer_scale=3`), crushing the color-dense jungle backgrounds. Measured: source frames have ~65k colors, the old GIFs had only ~111.

Fix (now the standard, `/tmp/mkgif.sh`): two-pass palettegen/paletteuse with **full 256-color palette** (`max_colors=256`), `stats_mode=full` (samples all frames for a representative palette), `scale=...:flags=lanczos`, and `dither=sierra2_4a` (error-diffusion, far better gradient preservation than Bayer). No `diff_mode` restriction (it hurt color on scrolling backgrounds and didn't help size).

Result: GIFs now use 254-255 colors. Aligned per-pixel color diff from source dropped to ~1.3 (was a mismatch artifact making it look like 11+, but the real palette was the 111-color cap). Sizes are also smaller than the old bayer output (sierra compresses the jungle better): turn GIF 5.4MB, barrel-roll 6.3MB.

ffmpeg recipe:
```
# palette (single input, -frames:v limits the range)
ffmpeg -framerate 60 -start_number S -i frames/%04d.png -frames:v N \
  -vf "fps=F,scale=W:-1:flags=lanczos,palettegen=max_colors=256:stats_mode=full" pal.png
# apply (both inputs, -frames:v is an OUTPUT option = round(N*F/60))
ffmpeg -framerate 60 -start_number S -i frames/%04d.png -i pal.png \
  -lavfi "[0:v]fps=F,scale=W:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=sierra2_4a" \
  -frames:v OUTF -loop 0 out.gif
```
Gotcha logged: `-frames:v` placed between two `-i` inputs binds to the palette input and errors; it must be an output option after both inputs.

---
## DROP 2026-07-12 — Part 7: Level Environment Pack (all 6 levels + Level 6 + animated liquid)

Wired the full Level Environment Pack (`_DROP/env_pack/`). All 6 levels now use the pack's connected-master backgrounds; Level 6 "FURIOUS DEATH" added as a new stage (boss deferred per Mike); animated liquid wired for levels 1-3.

### Prep (`_BUILD_SOURCE/prep_levels.py`)
- **Masters**: each level's Connected_Master (443x3548 for L1-3, 864x7284 for L4, 512x3072 for L5-6) has its `#FF00FF` liquid channels converted to transparent (with an AA-tolerance band + despill), then resized to 480px wide (matches the viewport width for crisp 1:1 horizontal; the game stretches width to VW anyway) capped at 2600px tall to control file size. L1 has TWO masters (intact + destroyed-dam). Output `assets/levels/lvl{1..6}_master.png` (+ `lvl1_master_dam`), ~1.6-2.7MB each (in line with the existing map art).
- **Liquid FX**: each family (water/lava/icewater) is an 8-frame loop. Magenta-stripped and cropped to a COMMON union bbox so every frame is identical size -> stable tiling with no per-frame jitter (was a bug: independent tight-crops gave 203x204 vs 203x206 frames). Output `assets/levels/fx/fx_{water,lava,icewater}_{0..7}.png`.
- Registered 31 keys via `_BUILD_SOURCE/register_levels.py` (manifest 1417 -> 1448).

### Draw wiring (gamecode.js)
- New `_liquidFrames(key)` gathers a BOFX 8-frame family into an Image[] (cached).
- New `_levelCfg()` maps `run.stage` -> {master, liquid, fill, tile}. L1 swaps intact->dam via `damBroken`. Stages 4-6 have no liquid (null).
- New `drawLevelMaster(dt)`: draws the animated liquid backing (via the existing `drawAnimTerrain`, showing through the master's transparent channels) then the keyed master scrolling bottom->top. Source-rect math accounts for master-width != VW (visible window is `VH*(imgW/VW)` tall in master pixels). Returns false if art not ready -> caller falls back to the old draws then procedural bg.
- `drawBG` now tries `drawLevelMaster` FIRST for all stages (replaces the old per-stage draws for 1-3; adds 4-6).

### Stage 6 + progression
- Added `{n:6, sub:'FURIOUS DEATH', bg:'space', music:'lvl6', boss:null}` to STAGES. (Gave it a distinct `music:'lvl6'` so the stage-5-music assemble.py patch anchor stays unique — it anchors on `bg:'space', music:'stage'` which stage 6 would otherwise duplicate.)
- Boss-less stage handling: when the stage timer completes and `curStage.boss` is null, set `bossDefeated=true` directly (clears the level) instead of `spawnBoss(null)`.
- Stage-clear now triggers `triggerVictory()` after the final stage (`run.stage>=STAGES.length`) instead of `beginStage(7)` (which would crash on undefined STAGES[6]).

### Verified
`test_fl.js` §17 (16 assertions, all green): 6 stages; stage 6 = FURIOUS DEATH with null boss; all 6 masters loaded; 8 liquid frames each for water/lava/icewater; lava frames uniform size (no jitter); L1 dam swap picks lvl1_master -> lvl1_master_dam; drawLevelMaster draws stage 6. Full harness green.
Rendered all 6 scrolling backgrounds (`/tmp/render/levelscroll.js`) -> `out/levels/level{1..6}_*.mp4` + high-color GIFs; liquid animation confirmed (4 distinct lava frame hashes across clock times); `all_levels_overview.png` shows all six.

### Still TODO on levels
- Level 6 BOSS (deferred). Stage 6 currently clears on the timer.
- Tilesets (36 modules/level) are high-res construction sources — not wired (the connected masters are the playable bg; tilesets would only matter for a tile-built alternative).
- L4/L5/L6 have no animated-liquid families in the pack (none needed — dry/space levels).
- Old map art (mapJungle/mapVolcano/mapIce in assets/levels/) is now superseded by the masters; can be deleted to reclaim ~7MB.

---
## DROP 2026-07-12 — Part 7b: level fixes (magenta halo, oversized liquid tiles, L6 access + password)

Three issues from Mike after the first level wiring:

### 1) Magenta/purple halo all over levels 1-3
Cause: the magenta key was too strict (near-pure #FF00FF only), leaving the anti-aliased fringe pixels (e.g. RGB(205,39,178)) around every liquid channel — ~7000 px/master, 92% of them right at the channel edges. Downscaling then smeared those into a visible purple halo.
Fix (`prep_levels.py` `key_magenta_to_alpha`): (a) much WIDER magenta threshold `(r>120)&(b>120)&(g<r-35)&(g<b-35)&((r+b)-2g>90)`; (b) dilate the mask 1px (scipy) so the AA ring on the terrain side is also cut; (c) de-spill remaining magenta-leaning pixels; (d) in `prep_master`, key at FULL res, then resize with color=LANCZOS but alpha=NEAREST (hard alpha edge, no bleed), then re-key the downscaled result to kill any resample fringe. Result: 0 leftover magenta on every master (was ~7000), 0 magenta across all rendered scroll frames.

### 2) Animated liquid tiles too big
The liquid backing tiled at `tileScale` 1.0 (water/ice) = one 480px tile stretched across the whole viewport = giant/blurry. Dropped to 0.30-0.34 so the pattern tiles ~3x across (144-163px tiles) and reads as fine flowing texture. Lava 0.30, water/ice 0.34.

### 3) Level 6 access + password
- Added Level 6 password **`DETH`** to `PASSWORDS` ({FURY:1,IRON:2,DAM5:3,STRM:4,ORBT:5,DETH:6}).
- Stage-clear "NEXT STAGE PASSWORD" now shows for `run.stage<STAGES.length` (was `<5`) with codes extended to include DETH — so beating stage 5 displays `DETH`.
- Progression already advances stage5->stage6 (Part 7) and stage6->victory. Confirmed end-to-end: DETH->stage6, clear-5 shows DETH, 5->6 loads lvl6_master, 6->victory no crash.

### Verified
`test_fl.js` §17 extended (now 21 assertions): + DETH unlocks stage 6, ORBT still unlocks 5, clearing stage 5 shows DETH, water & lava tile scales <0.4. Full harness green. Re-rendered levels 1-3 + 6: 0 magenta across all frames.

## ALL PASSWORDS (for reference)
FURY=stage1, IRON=stage2, DAM5=stage3, STRM=stage4, ORBT=stage5, **DETH=stage6**. (COLE4U unlocks the Cole pilot.)

---
## DROP 2026-07-12 — weapon/shield FX sheets (laserbeam, machinefx, spreadfirefx, shields)

Mike re-uploaded four weapon-VFX sheets (laserbeam.png, machinefx.png, spreadfirefx.png, shields.png). KEY FINDING: these were ALREADY extracted and wired in a prior session — the art exists and the draw code already references it:
- machine gun: `mfx_mg_<row0-4>_<col0-4>` (5 levels x 5 growth frames), in `assets/fx/master/`. Drawn in `drawBullets` for `kind==='mg'` with per-level tint (1 orange #ff8a1e, 2 blue #3a8aff, 3 green #5fe07a, 4 white/none, 5 red #ff4a48) + white core + colored halo. Intensity/size grows with level.
- spread: `mfx_spr_<row0-4>_1`, same per-level color logic, `kind==='spread'`.
- laser: `laserbeam_0..N` (5 levels), `kind==='beam'`, beam width grows `14+lv*4`, tinted per level. Verified render: 22k->43k lit px across levels.
- shields: `shield_l1..5` (the floating shield that orbits/pulses over the ship, drawn in `drawShield`) and `pwr_shield_1..5` (HUD icon). Both grow tier by tier.

Verified all art renders with the exact per-level colors Mike specified and scales up in intensity by level (MG 128->2658 px L1->L5; laser 22k->43k; shields 334->1034 px).

### The one thing NOT yet wired (now fixed)
The HUD shield indicator (top-right, `drawHUD`) was still using the generic `item_shield` icon, not the new tiered `pwr_shield_<level>` art. Per Mike ("both the floating shields AND the hud icon"), updated the HUD to draw `pwr_shield_<clamp(run.shield,1,5)>` (falls back to item_shield). So the HUD icon now matches the shield tier you're carrying.

### Verified
`test_fl.js` §18 (8 assertions, all green): mg 5x5 art present, spread 5 levels, laser 5 levels, floating shields 5 levels, HUD shield icons 5 levels, and firing each weapon spawns level-tagged bullets/beam for correct tinting. Full harness green.
Rendered per-level proof (`weapon_fx_all_levels.png`) + a firing gameplay demo cycling all weapons x levels (`weapon_fx_demo.mp4/gif`).

---
## DROP 2026-07-12 — fix: level-1 MG pellet washed out (white glowblob overlay)

Mike showed the intended L1 machine-gun pellet (a clean golden-yellow orb) vs in-game (a pale washed-out dot). Root cause in `drawBullets` `kind==='mg'`: BEFORE drawing the pellet art, the code drew a procedural glow blob — a colored halo + a bright WHITE inner core — composited with 'lighter'. That white core washed the gold pellet (and every level's color) toward white, so L1 read as a pale dot instead of gold.

Fix: removed the white-core glowblob overlay entirely. Now `drawMfx` draws the neutral pellet art tinted to the exact per-level color with a matching COLORED glow (not white) — the art already has its own hot core, so no separate white blob is needed. Also warmed L1's tint from #ff8a1e (orange) to #ffcf3a (gold) to match the reference art.

Verified per-level pellet colors after fix (were all washed toward white): L1 gold RGB(204,175,94), L2 blue(89,146,232), L3 green(115,215,140), L4 white(188,190,205), L5 red(237,101,104). All distinct, L1 now reads GOLD (g and r >> b) not white. In-game L1 gameplay shows 240-409 gold px/frame. `mg_l1_fix_compare.png` (intended vs fixed), `mg_pellet_fixed.mp4/gif` (L1 firing then cycling up). Harness green.

---
## DROP 2026-07-12 — fix (round 2): MG pellet flat/no center shading

After removing the white glowblob (round 1), the pellet went flat yellow — it lost its hot center. Root cause: the draw was forcing the WHITE art row (`_mgRow=4`) and TINTING it to the level color. Tinting a white pellet gives a uniform flat color — the art's baked center-to-edge shading (hot yellow-white core -> gold -> orange rim) was being thrown away.

Real fix: draw the ACTUAL pre-shaded colored row for each level (the sheet already has 5 correctly-shaded pellets), with tint=null so the art's own shading shows, plus only a soft colored glow. Level -> sheet row mapping: 1 gold(row2), 2 blue(row1), 3 green(row3), 4 white(row4), 5 red(row0). Verified per-level color + bright-core presence: L1 gold with hot core (RGB 254,242,101 center, orange rim), L2 blue, L3 green, L4 white, L5 red. The center-to-edge gradient is back — matches Mike's reference art. `mg_l1_shaded_compare.png`, `mg_pellet_shaded.mp4/gif`. Harness green.

Lesson: tinting a neutral/white sprite flattens any internal shading it has. When art ships pre-colored with baked shading, USE the colored art directly (tint=null); only tint a neutral sprite when you specifically want a flat recolor.

---
## DROP 2026-07-12 — fix: Level 1 water animation (too fast + weird tiling)

Mike: water animation too fast and tiles look weird in motion. Three root causes:
1. **Too fast**: `drawAnimTerrain` advanced frames every 110ms (~9fps) — a strobe, not gentle water.
2. **Frames jumping**: `prep_liquid_family` cropped each liquid frame to its own content bbox. But the source `water_surface_01..08` frames all share a 222x296 canvas with the ripples at slightly different x per frame — cropping made the water blob appear to JUMP position frame-to-frame instead of rippling in place.
3. **Tile too big for the channels**: water channels in the master are ~17px wide (native, ~25px on screen), but the water tile at tileScale 0.34 was 163px — so inside a narrow channel you only saw a flat slice of a huge texture, reading as patches, not flowing water.

Fixes:
- `prep_liquid_family`: KEEP native canvas size (222x296), no crop -> surface animates in place. (Re-ran prep; frames now uniform 222x296, centroid shift between frames 0.5px = ripples in place, was jumping.)
- `drawAnimTerrain(frames, baseScroll, speed, tileScale, fps)`: added `fps` param, default 6 (was ~9). `_levelCfg` now sets water/ice fps=5, lava fps=6.
- Water/ice tileScale 0.34 -> 0.18 (86px tiles, ripples read in the narrow channels); lava 0.30 -> 0.20.

Verified: water animates at exactly 5fps (holds 12 game-frames per change), ripples in place (0.5px centroid shift, stable), tiles finer. `level1_water_fixed.mp4/gif`. Harness green (tile scales still <0.4 assertion passes).

---
## DROP 2026-07-12 — fix: black squares in water (transparent tile bands)

Mike: black squares appearing in the water. Confirmed using the water SURFACE flats (water_surface_01..08), which is correct — but the previous "keep native canvas" fix left each frame only 46% opaque: content sits in a middle band (y70-251) with fully-transparent top/bottom bands. Tiling those vertically produced horizontal black stripes/squares where the transparent bands landed (the backing fill showed through).

Fix (`prep_liquid_family`): crop every frame to the COMMON vertical content band (uniform box y[70,251] so ripples still animate in place, no jump), then FILL any residual transparent pixels inside the band with that frame's median water colour. Frames are now 100% opaque and uniform per family (water 222x179, lava 256x201, icewater 222x294). Applies to all 3 liquids.

Verified: liquid frames 100% opaque; within actual water channels 0 black px; max black-gap-in-water across the whole scroll clip = 5px (AA edges only, was thousands). Animation still in-place at 5fps, tiles still fine (0.18). `level1_water_nofill.mp4/gif`. Harness green.

---
## DROP 2026-07-12 — spread fire now uses Mike's sheet (shield + laser already correct)

Mike: use the spread-fire graphics I provided; floating shield and laser are already mine.

Findings:
- **Spread**: was drawing OLD `mfx_spr_<row>_1` art TINTED with wcol (flattened, same bug as the MG pellet). NOW extracted from Mike's `spreadfirefx.png` -> `spr_<lv0-4>_<frame0-4>` (24 keys, `assets/fx/spread/`, `extract_spread.py`+`register_spread.py`). Sheet is 5 color columns (levels) x 5 animation rows; column detection falls back to an even 5-split when gaps merge, content threshold lowered to 3px so the thin blue (L2) darts survive, magenta key tuned to preserve blue (r>150 gate). Draw rewritten to use `spr_<lv>_<frame>` animated (~14fps) with tint=null so the art's own colours/shading show; falls back to legacy mfx_spr then primitive. (L2/blue is missing frame index 1 — only 4 of 5 frames had enough pixels — the draw's fallback loop picks the nearest available frame, so it animates fine.)
- **Floating shield**: already Mike's art. `shield_l1..5` extracted from `shields.png` (5 blue shields growing 270->404px). Verified installed shield_l1 is blue-dominant, matches the sheet. drawShield uses shield_l<lv>. No change needed.
- **Laser**: already Mike's art. `laserbeam_0..N` from `laserbeam.png` (tall beams, per-level). Verified rendering with per-level colour+length growth in a prior pass. No change needed.

Verified: spread now shows Mike's per-level colours (L1 white, L2 blue, L3 green, L4 white-blue, L5 orange-red) from the actual sheet, not a flat tint. Harness §18 updated (spr_<lv>_0 present for all 5 levels); full harness green. `spread_shield_laser_yourart.png`, `spread_shield_laser_demo.mp4/gif`.

---
## DROP 2026-07-12 — shield reworked: N swirling orbs (N=level) + golden armor at L5

Mike clarified: the shield (from the powerup box) should be ORBITING ORBS swirling the player — 1 orb at level 1, 2 at level 2, ... 5 at level 5, plus a golden armor glow at level 5. Not a static shield icon.

Rewrote `drawShield(x,y)`:
- Draws `lv` orbs orbiting the player on a squashed ellipse (R=22+lv*1.5, y-radius *0.62 for a 3D swirl feel), spinning at t*2.2. Near-side orbs (front) draw slightly bigger/brighter, far-side dimmer -> reads as orbiting in 3D. Uses the `iceorb_0..3` art (blue energy orb, animated) which matches the shield sheet's blue orbs. `lighter` compositing for glow.
- Level 5: adds a golden radial-gradient armor glow behind the orbs (gold rgba ring) and gives the orbs a gold shadow.
- Falls back to the old `shield_l<lv>` icon if iceorb art is missing.
The shield powerup already does `run.shield=clamp(run.shield+1,0,5)` per pickup (line ~1393), so each box adds one orb up to 5 — matches the spec directly.

Verified: orb count == level for all 5 (1,2,3,4,5 orbs detected); golden glow present only at L5 (560 gold px, 0 at L4); orbs swirl (centroids move frame to frame). `shield_orbs_swirl.mp4/gif` (ship with orbs ramping 1->5). Harness §18 updated (iceorb present, drawShield runs). Full harness green.
Note: `shield_l1..5` (the shield-emblem art) and `pwr_shield_1..5` (HUD icon) are still Mike's art from shields.png — the emblem is now the fallback, the HUD icon unchanged. The orbs are the primary in-world shield visual.

---
## DROP 2026-07-15 — Falva special reworked: side-anchored laser balls

Mike: the balls should anchor on her SIDES and shoot lasers out (not a charge-up ring, not bouncing pinballs).

Extracted Mike's `laserfalva.png` (cyan-keyed, `_BUILD_SOURCE/extract_falvalaser.py`): row0 = anchor orb (8 frames), row2 = straight laser beam (8), row3 = spread laser (8). Keys `florb_0..7`, `fllaser_0..7`, `flspread_0..7` in `assets/fx/falvalaser/` (24 keys, `register_falvalaser.py`, manifest 1496).

New behavior (replaces the charge/roller mechanic):
- `falvaLasersStart()` spawns 2 balls in `falvaBalls[]`, one anchored each side (±30px, offset +4y).
- `falvaLasersUpdate(dt)`: each ball smooth-follows its side of the hull with a gentle bob, fires a straight pink laser bolt (`kind:'flaser'`, vy -13, dmg 2) every 0.10s and a 3-bolt spread (`kind:'flspread'`) every ~0.85s. Bolts are normal pBullets so they use the standard enemy/boss/powerup collision.
- `drawFalvaBalls()` draws the animated orb art at each ball (additive, pink glow), called after `drawRollers()` in both draw paths. `flaser`/`flspread` bullet draws added to `drawBullets` (tint=null, use the laser art frames, animate via `_f`+t).
- She KEEPS her normal weapon during the special now (removed the `specialActive('falva')` fire-suppression). `endSpecial` clears `falvaBalls`.

Verified (`test_fl.js` §3 rewritten + §10/§13 updated, all green): 2 balls spawn one per side; anchor to ±30px of the hull; emit flaser + flspread bolts traveling upward; normal weapon still fires; art present; balls despawn on special end; 420-frame live run shows 2 balls + laser bolts, no throw. Rendered `falva_side_laserballs.mp4/gif` (balls flanking her, firing up at drones). Old roller-charge tests removed (mechanic replaced); the roller system code itself is retained (unused by Falva) for the rival dogfight/back-compat.

---
## DROP 2026-07-15 — Mega Vault arsenal wiring, PASS 1 (art + damage states + hit effects)

Wired the Conversation Mega Vault v4.0 vehicle arsenal into the enemy system. Mike's directions: face-toward-player tanks that switch to side views when moving (turret shoots either way), aircraft bank by velocity, damage states by HP threshold (>66% intact, >33% damaged, else critical), hit effects, keep existing spawn waves.

### Extraction (`_BUILD_SOURCE/extract_vault_vehicles.py`, `register_vault_vehicles.py`)
- 6 tanks -> `tk0..5`, keys `<k>_<state>_<dir>` (dir n/e/s/w; state inta/dama/crit) = 72 frames, uniform 124x124 canvas.
- 15 aircraft -> `ac0..14`, keys `<k>_<state>_<bank>` (bank c/l/r/hl/hr; damage states center-only) = 120 frames.
- 7 REAL bosses (Mike: only these are bosses, the other 15 in the folder are regular-plane dupes) -> `bz0..6` = airbase_siege_fortress, furious_death_hellwing, ice_crystal_lancer, iron_vulture, jungle_thorn_predator, lava_magma_reaver, space_event_horizon. Keys `<k>_<state>` = 21 frames, ~200x188.
- Every frame tight-cropped then padded to a uniform per-family canvas (same wingtip-clip fix as the pilot ships) -> verified 0 edge-clipping. Binary alpha. Manifest 1496 -> 1709 (+213).
- Keymaps saved to `vault_keymap.json`.

### Wiring (gamecode.js)
- `drawVaultVehicle(e)` — new draw path, routed FIRST in `_drawEnemyInner` (before the old `drawNewEnemyArt`/master-art paths).
- `_vaultKeyFor(e)`: sticky per-entity (`e._vk`), maps tank-ish types (tank/htank/mgturret/rockturret/microturret) -> `VAULT_TANK`, air types (assault/gunship/scout/intcp/hfight/bomber/drone/mdrone/icegun/cryo/frost/turdrone/shieldd) -> `VAULT_AIR`, by `variant`.
- Tanks: facing = south (toward player lane) when |vx|<0.35, else e/w side view by vx sign. Turret muzzle flash drawn toward the player aim. Damage frame by `_vaultState`.
- Aircraft: bank frame from vx (hl/l/c/r/hr at ±1.1/±0.35). Damage states use center pose (bank frames are intact-only).
- `_vaultState(e)`: hp/maxhp -> inta/dama/crit at 0.66/0.33.
- Hit flash reuses existing `tintColor(e)` (white flash on `e.flash>0`); death fade via `_dyingT`; explosions via existing `explode()`.
- Bosses extracted + registered but NOT yet wired as boss encounters (that's the boss-authoring pass); art is ready.

### Verified
`test_fl.js` §19 (11 assertions, all green): tank/aircraft/boss art present; HP thresholds -> inta/dama/crit; stationary tank faces south, moving-left shows west; drawVaultVehicle renders tank + aircraft. Full harness green.
Live 300-frame combat clip (`vault_vehicles_combat.mp4/gif`): waves of tanks + aircraft with lateral movement (side views + banking show), player destroys them (hit flash + explosions 64->541 fire px). Spawn waves unchanged.

### Still TODO (next passes)
- Boss encounters: wire the 7 `bz*` bosses as actual boss fights (behaviors, phases, HP, per-stage assignment).
- Per-stage vehicle assignment (which tanks/jets appear in which stage — currently variant-indexed across all).
- Distinct per-enemy behaviors (movement/attack patterns per vehicle).
- Aircraft frame clipping was fixed in extraction; tanks/bosses too. If any specific craft still clips in-game, re-check its tight-crop.
- The 800px-wide levels + horizontal scroll (separate major task).

---
## DROP 2026-07-15 — Jungle enemy overhaul (orientation, shadows, 4 new archetypes, behaviors)

Big enemy pass per Mike. Vault vehicles now face the player, cast shadows, and the jungle stage runs a bespoke new-enemy roster.

### Orientation + shadows
- `drawVaultVehicle`: planes AND tanks now VERTICALLY FLIPPED (ctx.scale(1,-1)) to face the player (nose/hull down-screen). Racer's 180-turn animates the flip via `_turnP` (eases +1 up -> -1 down) and `_faceUp`.
- `drawUnitShadow(x,y,w,h,alpha)`: directional soft-ellipse shadow, offset by screen position (parallax). Drawn under every vault enemy AND under the player ship (`_drawPlayerCore`). Style = "directional shadow that shifts with position" per Mike.

### 4 new jungle archetypes (spawnEnemy types + patterns)
- `racer` (pattern 'racer'): flies IN from bottom (vy -7.2), snaps a 180 whip (whip SFX + trail burst) at ~42% height, charges the player firing HOMING missiles w/ lock-on beep, FLEES fast off the top after ~3s if not killed. Full phase machine: flyin->turn->charge->flee. Off-screen cull exempts racers while entering.
- `strafer` (pattern 'strafer'): dives from the TOP, guns blazing (rapid 'pellet' MG), pellet + body-impact kill.
- `stationship` (pattern 'stationgun'): regular-speed fodder, holds mid-screen station and plinks single shots.
- `jungletank` (pattern 'tankhold'): GROUND tank that does NOT scroll away — eases to a held Y, makes slow lateral tank repositions, fires 'groundup' (double missiles / aerial MG) that SCALE UP toward the player (`_gscale` 0.4->1.5) to sell the ground-to-air perspective.

### New projectiles + SFX
- `eHomingMissile` (turn 0.11 hard-tracking), `eGroundUp(x,y,mg)` (scaling ground-to-air, missile or MG), draws with per-frame `_gscale`. New bullet kinds `groundup` + `pellet` with their own update+draw. SFX: `whip` (swoosh), `lockon` (missile beep).
- `addTrail(x,y,color)`: jet contrail via the shared particle pool. Racers/strafers emit trails.

### Jungle roster wiring
- `buildStagePlan(1)` returns a JUNGLE-ONLY plan (racers/strafers/station ships/tanks); old generic waves bypassed for stage 1. Green/jungle vehicles auto-picked: `_jungleJet` (gripen ac4 green, sukhoi ac12) / `_jungleTank` (leopard2 tk4 green, challenger2 tk1 olive, challenger1 tk0 tan for the beach).
- Spawn `pattern` override bug FIXED: the post-switch `byType` default was clobbering self-set patterns; new types (+microturret) now exempt via `_selfPat`.
- 7-MAX on-screen cap for stage 1 (dispatch gated at cap-3 so a 3-spawn wave can't exceed 7). Verified peak 7.

### Verified
`test_fl.js` §20 (11 assertions, all green): racer/jungletank keep patterns + correct art; racer full lifecycle; tank stays on-screen; jungle spawns NO old generic enemies; 7-cap holds (peak 7); shadow + ground-to-air/homing fns present. Full harness green.
Clips: `jungle_new_enemies.mp4/gif` (full roster in combat, shadows, trails, explosions), racer lifecycle verified frame-by-frame (flyin f0 -> turn f45 -> charge f66 -> flee f139 -> gone f187).

### Still TODO
- **Wire the new 800px-wide jungle level** (Mike wants the beach-opening section + more lateral room). This needs the horizontal-scroll camera — deferred to its own focused pass to avoid rushing the scroll architecture (and re-introducing magenta-halo/tiling bugs). New level assets confirmed present: 4 sections 800x1000 + boss arena, context sheet 800x4488, magenta liquid channels.
- Boss encounters for the 7 bz* bosses.
- Per-stage rosters for stages 2-8 (jungle done; others still on old generic enemies).

---
## DROP 2026-07-15 — racer turn: true rotation instead of vertical flip

Mike: don't do the vertical mirror-flip; make them turn from their entry frame, rotating each step until facing forward and rushing him.

Replaced the `ctx.scale(1,flip)` mirror in `drawVaultVehicle` (air branch) with a true `ctx.rotate(ang)`. Aircraft now carry `e._faceAng` (radians): 0 = nose up/away (native art), PI = nose down toward the player. Default when unset = PI (strafers/station ships already face the player).
Racer pattern drives `_faceAng` through the phases: flyin holds 0 (climbing in nose-up), turn eases 0->PI over ~0.44s with easeInOutQuad (whipped feel), charge holds ~PI with a slight lean toward the player's column, flee turns PI->0 as it escapes. Muzzle flash + trail emit points now follow the rotated nose.
Verified: faceAng sweeps 0->5->19->42->74->113->144->165->177->180deg through the turn (monotonic, eased), holds 180 on charge. `test_fl.js` §20 +1 assertion (monotonic 0->PI rotation). Harness green. `racer_rotating_turn.mp4`.

---
## DROP 2026-07-15 — racer turn: DRIFT (not rotate-in-place)

Mike: "they should be sliding and turning like a car that's drifting." The pure rotation kept it in its column; a drift needs velocity and facing DECOUPLED.

Reworked the racer 'turn' phase so momentum and facing are independent:
- Enters at an ANGLE (lateral vx toward mid-screen) so there's momentum to drift with; nose follows travel dir during flyin.
- Turn phase (0.6s): entry velocity CARRIES ON and bleeds off (slides up+across, x moves ~40px) while the NOSE rotates faster than the velocity vector (over-rotates into the corner via a sin() overshoot term). Result: for a beat it's moving one way but pointing another — the classic drift/slip look. Heavy trail during the slide.
- Settles pointing at the player, zeroes lateral vel, charges down.
- Edge clamp + off-screen cull relaxed for racers during flyin/turn/flee so the drift can slide near/off the sides without being clamped or culled.
Verified: SLIP (angle between travel dir and facing) peaks ~93-164 deg mid-turn while the ship slides ~40px laterally, then resolves to face the player. `test_fl.js` §20 drift assertions (slip decouples, lateral slide >15px, ends facing player) — replaced the old monotonic-rotation check. Harness green. `racer_drift_turn.mp4`.

---
## DROP 2026-07-15 — racer turn: single curved ARC path, nose follows tangent (matches Mike's sketch)

Mike sketched it: (1) the flight PATH is one smooth S-curve — up from the bottom, arc over the top, curve back down at the player; (2) the SPRITE nose rotates continuously along that curve (follows the tangent), so it's always pointing where it's heading. Simpler than the drift/slide I'd built.

Reworked racer to a single 'arc' phase (replaces flyin+turn+drift):
- Parametric curved path over ~1.5s: X swings out to an apex-x (rnd 90-150px to one side) then curves in to the player's column; Y rises to the apex (at p=0.4) then descends well past it into the play area. One continuous hook.
- `_faceAng` each frame = atan2(dx,-dy) of the actual per-frame movement (the path tangent), smoothed toward it (dt*11) so it rotates continuously with NO snapping — from pointing-up on entry, through diagonal as it crests, to pointing-DOWN as it curves back at the player.
- Hands off to 'charge' (straight down, tracks player column, facing eased to PI) then 'flee' (curves back up and away, nose follows the escape arc). Cull + edge-clamp exemptions updated from flyin/turn -> 'arc'.
Verified: rises 401px to apex then descends 143px back down; nose sweeps 164 deg continuously along the tangent (samples 148->13->21->79->118->147->166->178->180, smooth per-frame), ends at ~PI pointing down; full arc->charge->flee lifecycle intact. `test_fl.js` §20 arc assertions (apex up, curve down, continuous nose rotation, ends-down) replace the drift checks. Harness green. `racer_arc_turn.mp4`.

---
## DROP 2026-07-15 — racer arc: even nose rotation (fix late-snap junkiness)

Mike: the nose was turning "as they face straight, not during the halfway mark" — it lagged then snapped to down at the very end. Junky.

Two fixes:
1. Replaced the spliced two-half X/Y path with ONE quadratic Bézier (P0 entry-bottom, P1 apex up+out, P2 down-at-player). Position AND tangent are smooth everywhere. Nose is locked DIRECTLY to the exact Bézier tangent B'(p) (no lag-smoothing chase), so facing == travel direction at every instant.
2. Reparametrized the time curve with an inverse-ease (slow through the middle: p=0.5+0.5*sign(s)*|s|^1.8, s=2praw-1) so the jet spends more frames turning through the bend around the apex -> rotation spreads evenly instead of bunching.
Verified: max PER-FRAME nose rotation during the arc is 7.4 deg/frame (smooth; junky threshold ~8), peaking gently at the apex (tightest curve) not snapping at the end. Early/mid rotation now balanced. Full arc->charge->flee intact, ends pointing down. Harness §20 green (descent-past-apex threshold relaxed to match the smoother earlier hand-off). `racer_arc_smooth.mp4`.

---
## DROP 2026-07-15 — racer turn: half-CIRCLE slide (constant speed + constant rotation, no stop-twist)

Mike: "they should be turning as they come in like a slide not stopping and twisting." The Bézier versions slowed to a near-stop at the apex (speed ratio 0.14!) and the nose rotation bunched there -> looked like it paused and twisted in place.

Root cause: a Bézier stepped by linear p has non-uniform speed (crawls where control points bunch = the apex) AND non-uniform curvature (nose rotates fast through the tight bit). Fixed by switching to a true HALF-CIRCLE arc:
- Entry at the bottom heading UP; circle centre offset to the side by radius R (rnd 78-110); sweep angle a=p*PI (uniform) over the top; exit heading straight DOWN at the player.
- Uniform curvature => nose (tangent) rotates at a CONSTANT rate; uniform angular step => CONSTANT speed. The jet slides through the whole turn at even pace, banking continuously — it never slows or stops to twist.
Verified: speed ratio min/max = 1.00 (perfectly constant, ~4px/frame); max nose rotation 2.6 deg/frame (buttery, threshold 8); nose sweeps evenly 3->23->44->65->86->107->128->149->170->177 deg (constant ~21deg/8frames), enters pointing up, exits pointing down at the player; hands to charge cleanly. `test_fl.js` §20: added constant-speed (min/max>0.7) + constant-rotation (<10 deg/frame) assertions; apex-rise threshold adjusted for the circle's geometry. Harness green. `racer_slide_turn.mp4`.

---
## DROP 2026-07-15 — racer: straight run-in + pause before charge

Mike: "make them go straight more before turning, pausing and charging." Added two phases around the half-circle slide:
- NEW 'flyin' phase FIRST: shoots straight up from the bottom (vy -8, nose up, contrail) until y<=VH*0.72, THEN turns in. Gives a straight run-in before the bank.
- NEW 'pause' phase between arc and charge: ~0.35s holding position pointing at the player (aim tracks the player's column) before it commits to the dive.
Full sequence now: flyin(straight up) -> arc(half-circle banking slide, constant speed/rotation) -> pause(brief aim) -> charge(dive at player) -> flee(loop away). Cull/edge exemptions extended to the flyin phase. Verified frame-by-frame: flyin f0-16 straight up nose=0, arc f24-88 nose sweeps 10->177 evenly, pause f96-104 holds at ~180 pointing down, charge f112+ dives. `test_fl.js` §20 lifecycle assertion updated for all 5 phases; constant-speed/rotation still green. Harness green. `racer_final.mp4`.

---
## DROP 2026-07-15 — 800px h-scroll jungle level + combat showcase (twin guns, lock-on reticle, missiles)

Mike: wire the new 800px jungle level with horizontal scroll; showcase a tank battle + surprise planes with lock-on missiles; jets/tanks fire twin-gun bursts THEN a missile; red reticle locks on the player + alert sound.

### 800px horizontal-scroll jungle level
- Assembled the 4 vault sections (800x1000, 128px overlap) into `jungle800_master` (800x3616), magenta liquid sockets keyed (`prep_jungle800.py`, `register_jungle800.py`). Beach/sand at the bottom (level start). +2 keys (manifest 1711).
- NEW camera system: `WORLD_W` (per-stage play width, 800 for stage 1 via `worldWidth()`), `camX` (h-camera offset, eased to follow the player, clamped 0..WORLD_W-VW). `updateCamX()` each frame; `drawWorld` applies `ctx.translate(-camX,0)` for wide stages. `drawLevelMaster` + `drawAnimTerrain` take an optional drawW to render across the full 800px. Player x-bounds extended to `worldWidth()`. `_levelCfg` stage 1 -> jungle800_master {wide:true}.
- Verified: WORLD_W=800, camX follows player (306 at far right), far-left vs far-right views differ (camera scrolls to different areas). KNOWN COSMETIC: a thin black band can show at the extreme right edge when scrolled to the world boundary (level art edge); base-fill covers most of it — flagged for a follow-up polish pass.

### Combat: twin-gun bursts -> lock-on missile
- `eTwinGuns(e,ang)`: two parallel tracer rounds from the wingtips/barrels (perpendicular offset = reads as twin cannons).
- Enemy lock-on: `enemyLockOn(e,delay)` pushes to `playerLocks[]`, plays `Audio.SFX.lockAlert` (rising triple-beep alarm). `updatePlayerLocks(dt)` ticks each lock; at `delay` it launches `eHomingMissile` from the source enemy. `drawPlayerLocks()` draws a RED targeting reticle ON the player: four corner brackets closing in as it locks, then solid + blinking crosshair + rotating ring when locked. Wired into updatePlay + drawWorld.
- Fire patterns reworked: racer fires twin guns, every 4th shot a lock-on missile; strafer twin guns, every 6th a missile; jungletank twin (scaling ground-to-air) MG, every 3rd a lock-on missile.

### Verified
`test_fl.js` §21 (all green): twin guns fire 2 side-by-side rounds; enemyLockOn places reticle; missile launches after the lock delay; drawPlayerLocks renders; lockAlert sound present. §(level) updated: L1 uses jungle800_master (wide), world 800px. Full harness green.
Render harness confirmed the red reticle draws centered on the player (444px at game 240,410). Clips: `combat_showcase.mp4/gif` (tank battle holding position with twin-gun + missile fire, then racers arc in for surprise lock-on attacks), h-scroll verified in `hscroll` frames.

### Still TODO
- Polish the h-scroll right-edge black band (level-art edge / camera clamp).
- Enemies spawn relative to the 480 camera; could spread them across the full 800 world for the wider level.
- 7 bosses; stage 2-8 rosters.

---
## DROP 2026-07-15 — jungle level fixes + grounded tanks + criss-cross planes

Mike's screenshot feedback: (1) screen edges show water, should be grass; screen not vertically filled (black band). (2) tanks must stay on the ground. (3) planes should go to the TOP then criss-cross, firing missiles the player can shoot down mid-cross or dodge.

### Level rendering fixes
- **Vertical fill was NEVER broken in-game** — the render harness wasn't applying the game's `ctx.setTransform(SS,0,0,SS,0,0)` (SS=2 supersample). With it, the level fills 100% (0/1024 empty rows). CRITICAL for future render harnesses: apply the SS transform before drawWorld or everything looks half-scaled.
- **Grass on both edges**: the 800px level was showing its left portion (water strip) because the player started at VW/2=240 (camera pinned left). FIX: `player.reset()` now starts at `worldWidth()/2` (=400, world centre) so the camera centres the level -> grass on both edges, path centred. Verified left-grass 29k / right-grass 37k, ~0 black.
- `drawLevelMaster` winH simplified to VH (1:1 vertical); base fill spans drawW.

### Grounded tanks
- `tankhold` pattern reworked: tanks now scroll DOWN with the terrain at the map speed (40*dt) so they look planted on the ground and scroll off the bottom — instead of holding a fixed screen Y (which read as floating). Slow lateral tank crawl retained. Verified y increases 100->140->... (scrolls with ground).

### Criss-cross plane attack (racer redesign)
- New phase machine: `flyup` (straight to the top, y<=topY ~0.14-0.26 VH) -> `crisscross` -> `flee`.
- `crisscross`: slides diagonally between alternating targets across the upper screen (worldWidth/2 ± 120-220), easing each leg (~0.85s), creeping down 14px per pass; nose follows the diagonal heading; fires a lock-on missile at mid-cross (p 0.42-0.58). After 5 passes or y>0.7VH -> flee. Gives the player two counters: shoot the missile as the jet crosses, or dodge the lane before the cross.
- Cull/edge exemptions updated flyin/arc -> flyup/crisscross.

### Verified
`test_fl.js` §20 updated (all green): flyup->crisscross->flee lifecycle; flies UP to top (topY 114); criss-crosses (x reverses direction); fires lock-on missiles during cross; tank scrolls DOWN with ground (100->140). §(level) L1 wide/800 still green. Full harness green.
Clip: `jungle_criss_cross_showcase.mp4` (grounded tank battle on the centred level, then criss-crossing planes firing missiles), rendered at correct SS=2 scale.

### Still TODO
- Right-edge black band at extreme world boundary (minor, when scrolled fully).
- Spread enemy spawns across the full 800 world.
- 7 bosses; stage 2-8 rosters.

---
## DROP 2026-07-15 — helix flight, front-turret tank blast, real smoke-trail art

Mike: (1) the criss-cross should be a HELIX pattern (interweaving spiral). (2) tanks fire ONLY from the front turret — a strong blast + a missile. (3) use the real smoke-trail art from the sources for trail FX.

### Helix flight (racer)
- Replaced the zig-zag 'crisscross' phase with 'helix': the jet descends steadily (y = topY + hxT*46) while sweeping horizontally in a sine wave (x = centerX + sin(hxT*2.2 + phase)*amp), amp widening 90->150 — a corkscrew/spiral. PAIRED jets get opposite phase (0 vs PI) so their paths interweave like a double helix. Nose follows the helical tangent. Fires a lock-on missile at each spiral crossing (crossPhase 1.45-1.70, re-armed between). After y>0.66VH -> flee.
- Verified: x oscillates sine (316->403->166->437, 2+ reversals) while y descends monotonically (93->244).

### Tank front-turret blast (jungletank)
- 'groundup' fire reworked: removed the twin aerial MG. Now every 3rd shot = lock-on missile; otherwise `eTankBlast(e)` — a single STRONG shell fired from the FRONT turret (muzzle at e.y - h*0.28, ahead of the hull), scaling up toward the player (blast:true, w=18, _gscale 0.45->1.5). New draw branch renders it as a big glowing plasma teardrop: orange outer glow + amber body + white-hot core + trailing flame.
- Verified: one blast per shot (not a spread), w=18 (strong), fires from ahead of the hull.

### Real smoke-trail art
- Extracted the mega vault's clean individual smoke frames (`06_Shared_VFX/Shared_96`): `engine_damage_smoke` (grey 54,51,51) -> `smk_0..5`; `missile_launch_exhaust` (white 254,254,254) -> `mexh_0..5`. 12 transparent 96px frames, tight-cropped (`extract_smoke.py`, `register_smoke.py`, manifest 1711->1723, in `assets/fx/smoke/`).
- Reworked `addTrail(x,y,color,kind)` to push to a new `smokeTrails[]` array of real sprites that expand + fade + drift (kind 'jet' grey / 'missile' white). Added `updateSmokeTrails(dt)` + `drawSmokeTrails()`, wired into updatePlay + drawWorld (smoke UNDER bullets/retina). Enemy missiles (`emissile`) now spawn white 'missile' smoke; jets emit grey 'jet' smoke.
- Verified: 84 active smoke sprites trailing the helix jets; 41940 grey-smoke px + white missile smoke rendered. Other smoke sources noted but not used (smoke_vapor_pack.png = 1395 busy elements magenta; Missile_Smoke_Trail_Atlas.png = magenta full-bleed; fx/library/trails = odd fire colors).

### Verified
`test_fl.js` §20 all green: flyup->helix->flee; helix x-oscillation; lock-on missiles in helix; tank ONE strong front blast (w=18, from front); smoke-trail system + art + addTrail kinds. Full harness green. Clip: `helix_smoke_showcase.mp4` (grounded tanks firing front-turret blasts, then paired helix jets with smoke trails + missiles).

---
## DROP 2026-07-15 — racer: crossing LOOPS (two planes weave through each other, per sketch)

Mike's sketch (planespin.png): NOT a descending helix — two planes each fly a big vertical LOOP (teardrop) that crosses the partner's flight path twice. P1 enters one side, loops up and over, comes down the OTHER side; P2 mirrors it; their paths interweave/cross.

Replaced the 'helix' phase with 'loop':
- Parametric teardrop over ~2.1s: a=0..2π. y = midY - ampY*cos(a) (bottom at a=0, apex at a=π, back to bottom) between loopTopY (~0.14-0.20 VH) and loopBotY (0.60 VH). x = loopCenterX - side*(sin(a)*W*0.5 + (a/2π)*2W - W) — a cardioid-ish sweep with a NET side flip so the plane exits on the opposite side. Loops are centred on worldWidth/2 so paired planes cross in the middle. Nose follows the loop tangent. Fires a lock-on missile at the crossing points (near center-x, lower half; re-armed away from center).
- Verified with a two-plane trace: P1 (enters left) and P2 (enters right) swap sides (P1-P2 x flips +233 -> -261) and their closest approach is 8px (0px in-harness) = paths genuinely cross. Plotted the paths (`looppaths.png`) — shows the interweaving double-loop crossing shape.
- flyup unchanged (straight up into the loop entry at loopBotY). Cull/edge exemptions helix->loop.

Verified: `test_fl.js` §20 green — flyup->loop->flee; flies up into loop; the two planes cross paths (closest approach 0px); fires lock-on missiles at the crossing. Full harness green. Clips: `crossing_loops_showcase.mp4` (in-game, paired planes weaving with smoke trails + missiles), `looppaths.png` (path plot).

---
## DROP 2026-07-15 — racer: de-janked angled-entry + swirl + dive (was teleporting)

Mike: the planes should come in at ANGLES from the bottom-left and bottom-right, SWIRL around each other (spinning), then dive at the player with missiles. The previous 'loop' version looked "janky af".

Root cause of the jank: a 54.7px POSITION TELEPORT at the swoopin->swirl handoff (swoopin ended near a target point but swirl recomputed position from a hardcoded circle angle) + a 180deg FACING SNAP at swirl-start (extra spin var) and dive-start (hard e._faceAng=PI).

Rebuilt as three clean phases:
- 'swoopin': angled straight run from the actual bottom corner (P1 bottom-left up-right, P2 bottom-right up-left) toward the swirl circle. Facing = run direction.
- 'swirl': FIXED shared circle (centre worldWidth/2, VH*0.28, r~84) so a mirrored pair orbits the identical circle. On entry, `_swA0` and `_swR` are derived from the plane's ACTUAL position (no snap). Facing eased toward the circle tangent (the orbit rotation IS the spin look). Fires a lock-on missile once per loop at the bottom of the arc.
- 'dive': breaks off, bears down on the player easing facing to down, fires aimed lock-on missiles (~every 0.7s), then flee.
Verified: max position jump 9.8px (was 54.7 — smooth, no teleport); facing jump peak 27deg/frame (was 180 — the hard snaps are gone); phases swoopin->swirl->dive->flee all run; two paired planes swirl a shared centre (closest approach ~83-111px). Removed the draw-time extra-spin that caused the facing snap.

Verified: `test_fl.js` §20 green (swoopin->swirl->dive lifecycle, enters swirl after angled run, shared-centre swirl, missiles during swirl/dive). Full harness green. Clip: `swirl_showcase.mp4`.

NOTE: the two planes don't interlock at a tight crossing (independent spawn timing means their orbit phases aren't perfectly 180 synced; closest approach ~80-110px). Motion is now smooth and reads as angled-in -> swirl -> dive. If Mike wants them to visibly thread through each other at a tight point, next step is a shared pair-clock so both index the same orbit angle offset by PI.

---
## DROP 2026-07-15 — pink "collision" smear ROOT-CAUSED + racer "cross & curl" final

Mike's screenshot: a pink distorted plane overlapping another — "weird collision bug", pattern still wrong, sprites not rotating every degree.

### Pink smear — root cause found and killed
NOT a corpse ghost, NOT Falva FX. `tintColor(e)` returned '#ff4040' @0.55 alpha for the flash 0-0.06 tail band -> every hit rendered the light-grey jets SALMON PINK for ~4 frames. Combined with the old pattern letting the two planes physically overlap mid-swirl, it read as a smashed collision. Fixes:
1. `tintColor`: hit flash is WHITE-ONLY now (red band deleted). Pink is mathematically impossible.
2. `killEnemy` art branch + dying ticker: `e.flash=0` the instant anything dies (belt & suspenders).
3. New pattern guarantees the pair can never overlap (below).
Verified: TRUE-pink pixel scan across 380 rendered frames — worst frame 100px/983k (incidental explosion edges); tintColor probe: 0 non-white bands at every flash value.

### Racer final pattern: "CROSS & CURL" (matches planespin.png)
Phases: cross -> curl -> dive -> flee.
- cross: angled straight run from the actual bottom corner (spd 7.5) to a tangent point on the curl circle; pair staggered 0.45s via module `_racerTick` so they never meet at the X.
- curl: circle on the FAR side (`_cuCx = W/2 - side*110`, cy=0.24VH, R=72; left-enterer clockwise). Entry angle found by 96-sample numeric search matching curl tangent to run heading -> position AND heading continuous (no snap). 1.5 revolutions (`_cuSw>=3PI`), vx=dir*0.6 banks INTO the turn, lock-on missile when nose sweeps the player (0.7s cd).
- dive: y+=4.2 tracking player.x+side*28, lock-on every 0.8s, exits 2.4s/0.92VH -> flee.
- `_faceTo` helper: ramping ease (rate 8->48 over 0.25s) + `atan2(sin,cos)` normalization (fixes the ±2PI accumulation wrap-snap that caused 77deg/frame jumps) + HARD CAP dt*3PI (~9deg/frame): the nose physically cannot snap, and tracks the 5.2deg/frame curl tangent.
Cull exemptions -> cross/curl/dive.

### Verified (crosscurl.js battery + test_fl.js §20, all green)
Phases all run; max position step 11.5px (<12); max facing step 9.0deg/frame (hard-capped); tangent lag mid-curl 3.7deg (= rotating through every degree); MIN PAIR SEPARATION 101-111px whole-run (no overlap possible); path-to-path min 2-3px (the trails genuinely CROSS = the X); peak 4 simultaneous locks; pink scan clean. Path plot `looppaths.png` = two crossing diagonals + a clean closed loop each, matching the sketch. Clip `cross_curl_showcase.mp4` (SS=2 correct scale).

### Rotational wheel (fallback offer, not needed yet)
Runtime ctx.rotate at SS=2 now hits every degree smoothly (measured). If Mike still prefers baked-art consistency, offer stands: generate a 72-frame (5deg) rotational wheel per jet and index frames from _faceAng instead of rotating at draw time.

---
## DROP 2026-07-16 — once-swirl, tank map boundaries, motion-variant family, barrel fire

Mike: swirl ONCE; tanks bounded off the see-thru/keyed sections + the bottom-left cliffs; save cross&curl as a reusable motion type + build variants (fast top divers w/ twin MGs + missiles; side-entry swirl-then-attack; top-entry bank-out flyby rippling homing missiles with rapid 1-by-1 reticle locks); tanks fire homing missiles from the END of the barrel.

### Shared motion family (the "save this motion" refactor)
`faceStep(e,target,dt)` (ramping ease + 9deg/frame hard cap + atan2 normalization), `curlInit(e,cx,cy,r,dir)`, `curlStep(e,dt,revs)` (tangent-locked circle, ~5.2deg/frame, banks into the turn, jet smoke). Racer refactored onto these; ALL new variants reuse them. Racer curl now `revs=1` -> sweep 2.00PI exactly (was 3PI).

### New enemy types (all in `_selfPat` — the spawn-override hazard — spawn cases, stage-1 roster adds at t=21/24.5/27/30)
- `topgun`: screams in from the top (vy 5.6*1.15), tracks the player, TWIN machine guns every 0.42s via eTwinGuns, one lock-on missile mid-dive, exits off the bottom (culled). Verified: 4 tracers airborne, lock fired, culled.
- `sideswirl`: enters level from a screen EDGE, penetrates toward centre, curls ONE loop up or down (circle placed directly above/below the flight line -> entry heading is exactly tangent, no snap), then dives at the player with lock-ons. Verified: enter->curl(2.00PI)->dive, maxPosStep 6.4px, maxFaceStep 9.0deg.
- `jetflyby`: bombs in from the top, then BANKS OUT left/right (nearer side) while RIPPLING 4 lock-on missiles 1-by-1 every 0.16s (reticle + lockAlert per missile — the fighter-jet cascade), straightens and exits the side (culled). Verified: locks at frames 53/63/73/83 (10f gaps), peak 6 reticles, culled at x=-87.

### Two real bugs found while wiring (both fixed)
1. **Drift-clamp pinning**: the exempted-drift else-branch clamped x to [-e.w, VW+e.w] — the exiting jetflyby hit an invisible wall at x=-34 and hovered forever. Now jetflyby-in-exit is unclamped (it is SUPPOSED to leave).
2. **VW vs worldWidth()**: both clamp branches AND the off-screen cull used VW=480 on the 800px wide world. Right-corner racer entries had been silently pinned to x≈514 (never truly entering from the corner), and any enemy east of x=560 would be insta-culled (would have eaten tanks snapped to the right half of the path). All three now use worldWidth(). Side-effect: with TRUE corner entries the racer pair's flee crossed the partner's dive lane (4px approach!) — flee now exits each plane's OWN side (`_flSide=e._side`). Pair min separation back to 79px whole-run; path-to-path 2.1px (the X intact); pink probe still 0.

### Tank barrel fire
`tankMuzzle(e)`: the hull is drawn flipped to face the player, so the barrel points AT them — muzzle = e.pos + aim*(h*0.62). `eTankBlast` fires from it; `updatePlayerLocks` launches homing missiles from it for tanks (jets launch from the NOSE along _faceAng). Old harness assertion "blast from y<tank.y" was conceptually wrong (that's the rear) — flipped. Verified: blast y=182 vs hull 150, missile y=186 (player below).

### Tank map boundaries (runtime drivability mask)
`_buildTankMask()`: built once per stage FROM THE MASTER'S OWN PIXELS (no asset, no index.html change): 8px cells, drivable = bright dirt (a>200, r>120, r>g+10, g>b, r-b>25) at >=60% of samples, then 2-cell (16px) erosion so hulls stay visually on the path. BLOCKED = keyed/see-thru channels, vegetation, dark cliff rock. `levelSrcY()` maps screen->master rows (mirrors drawLevelMaster's srcY); a tankhold's `_lvlY` is CONSTANT (it rides the scroll). tankhold: spawn-snap to nearest drivable x, crawl targets must be drivable, per-frame hard clamp (never leaves the path). FAIL-OPEN sanity: if a future master's palette yields <2% drivable, the mask is rejected (invalid sentinel) rather than freezing every tank.
Verified (node-canvas pixel harness): 100x452 cells, 21.0% drivable; dirt under drivable cells 99.8%; dirt under blocked 16%; see-thru drivable cells = 0; bottom-left cliff region 0.7% drivable (Mike's callout ✓); spawn at x=12 (void) snaps to x=328; 12s crawl = 0 violations. `mask_overlay.jpg` = green tint over the master for visual inspection.
test_fl.js §21 uses a SYNTHETIC injected mask (this harness has no real pixels): blocking, spawn-snap, crawl-clamp + graceful no-mask fallback. `_buildTankMask` cache-check moved above the rdy-check so injection works.

### Verified
Full test_fl.js green (0 errors) incl. new §21 (once-swirl 2.00PI, topgun, sideswirl, jetflyby ripple gaps 10/10/10, barrel blast+missile origin, boundaries). crosscurl battery: pos 11.5px, face 9.0deg/frame, tangent lag 3.7deg, pair min 79px, path-cross 2.1px, pink 0. Clips: `tank_boundaries_showcase.mp4` (void-edge snap + on-path crawl + barrel blasts/missiles), `enemy_patterns_showcase.mp4` (topgun pair -> sideswirl L/R -> jetflyby ripple -> racer once-swirl; racer segment trimmed ~188f by render timeout — full behavior already in cross_curl_showcase.mp4). `mask_overlay.jpg`.

---
## DROP 2026-07-16b — roster curation (Mike's picks) + all tanks flipped to face player + full boss catalog

### Tank orientation (Mike: "all tanks flip vertically to face the player")
- Scout `tank`/`htank` hull draw: wrapped in `ctx.scale(1,-1)` vertical flip so treads/front point DOWN-screen at the player (turret still tracks via 8-dir frame on top, un-flipped).
- `mgturret`/`rockturret` ground-turret draw: same vertical flip added (they're tanks per Mike).
- Vault `jungletank` + `microturret` already flip via drawVaultVehicle's `_vkind==='tank'` branch. All four tank types verified rendered + flipped (tankflip.png).
- Scout/heavy tanks now use the grounded `tankhold` pattern on ground stages (scroll with terrain, obey the drivability mask, turret tracks) instead of drifting straight/hunt.

### Level-1 roster curated to Mike's picks
- REMOVED from L1: minidrone, ebomb (and strafer swapped out — replaced by the new signature patterns).
- Jets: drone, bomber, intcp, turdrone, mdrone (+ the new patterns racer/topgun/sideswirl/jetflyby + stationship fill).
- Tanks (L1 & L4 only): tank (scout), htank (heavy), jungletank, microturret (minitank).
- Rewrote the stage-1 wave block; removed the duplicate old L1 roster block (was double-spawning ebomb/minidrone/hfight). test_fl.js roster assertion updated: verifies the approved jets+tanks present and the removed types absent. Spawn scan confirms: stationship,drone,jungletank,racer,intcp,tank,mdrone,topgun,bomber,sideswirl,htank,microturret,turdrone,jetflyby.

### Full boss/sub-boss art inventory (for Mike's review — roster_bosses.jpg)
Wired stage bosses (STAGES table): S1 damkeeper THE DAM KEEPER, S2 dreadnought HELLFIRE GUNSHIP, S3 wargod THE WAR GOD, S4 spider ARACHNON MK-IX, S5 leviathan LEVIATHAN CORE, S6 (none yet).
Sub-bosses (SUBBOSS table, mid-stage @0.45): subtank ARMORED BRUTE, subdread DREAD PROTOTYPE, subcore ENERGY CORE, subreactor OVERLOAD REACTOR.
Boss ART LIBRARY present in BOFX (much of it NOT yet wired to fights): bz0-6 (7 modular mega bosses), esB_big1-6 (6 minibosses, each idle/fire/hurt/death), chopper (helicopter boss idle/fire), iboss + iboss2 (ice boss, 2 forms, idle/atk), tankboss (idle/fire), fboss (Falva final boss idle/fire/death). Mega-vault also has Mega_Planes (airbase_siege_fortress, black_eagle_j20, felon_su57, furious_death_hellwing, ice_crystal_lancer, hawker_interceptor, +more) and Mega_Tanks (continental_crusher) modular boss kits, and per-stage 800x1000 Boss_Arena backgrounds for all 8 stages — none wired yet.

### Deliverables
roster_base.jpg (24 original), roster_new.jpg (8 new jungle), roster_bosses.jpg (19 boss/miniboss art tiles). tankflip.png (4 tanks facing player). Full harness green.

---
## DROP 2026-07-16c — tank-flip fix (per-art) + mega bosses (bz0-6) & minibosses (esB1-6) WIRED

### Tank vertical-flip, corrected per-art
Root cause of jungletank/tan-tank facing wrong: the flip was applied uniformly, but different hull art has different native orientation. tk0/tk1/tk4 (jungle vault tanks) natively point the barrel DOWN (measured: barrel mass in bottom third); the blanket `ctx.scale(1,-1)` was rotating them to face AWAY. Scout `t_s_hull`/`t_h_hull` art also natively faces down — the flip I added last pass was wrong for them too.
Fix: `drawVaultVehicle` tank branch flips ONLY art that faces up natively (`_facesDownNatively=/^(tk0|tk1|tk4)$/` skips the flip); removed the scout/heavy hull flip entirely. mg/rockturret keep their flip (their gt_ art faces up). Verified with a precise barrel-direction finder (narrow end row-width): all four tank types (scout/tan, htank, jungletank, microturret) now point the barrel at the player.

### MEGA BOSSES (bz0-6) — wired as end-stage bosses
Data table `MEGABOSS`: bz0 IRON BASTION (siege), bz1 RUST LEVIATHAN (spread), bz2 FROST CITADEL (ice), bz3 GRAVE WARDEN (homing), bz4 CAMO COLOSSUS (siege), bz5 MAGMA TYRANT (inferno), bz6 VOID SOVEREIGN (spiral). Each: name, hp mult, attack profile, accent color.
- spawnBoss extended: mega kinds get art=kind, HP-driven damage-state rendering, atkProfile.
- drawBossSprite: new mega branch draws HP damage-state art (`_megaStateKey`: inta>0.66 / dama>0.33 / crit) with levitation bob, enrage accent-glow, white/orange hit-flash, death fade. Boss draw dispatcher short-circuits to it for mega bosses.
- bossAttack: mega bosses run `bossProfileAttack(b)` + a telegraphed OVERDRIVE enrage under 50% HP (then 0.6x fireCd).
- Shared `bossProfileAttack` dispatches 8 named profiles (siege/spread/ice/homing/inferno/spiral for megas; strafe/twin for minis) built on the existing eShoot/eMissile/aimPlayer primitives.

### MINIBOSSES (esB_big1-6) — wired as mid-stage sub-bosses
Data table `MINIBOSS`: esB_big1 GRAY REAPER (strafe), esB_big2 BLUE HALBERD (twin), esB_big3 SAND VIPER (spread), esB_big4 STEEL WIDOW (homing), esB_big5 OLIVE MAULER (strafe), esB_big6 CRIMSON TALON (twin).
- spawnSubBoss extended: mini kinds get mini=true, art=kind, atkProfile.
- drawSubBoss: new mini branch renders idle/fire/hurt/death art states by boss state (dead->death, flash->hurt, firing->fire, else idle) + amber HP bar with the name.
- subBossAttack routes minis through `bossProfileAttack`.

### Verified (test_fl.js §22, all green)
7/7 mega bosses: named + attack (bullets fired) + enrage + HP damage-state art (crit at low HP) + draw without error. 6/6 minibosses: named + attack profile + draw. Death flow: hitBoss lethal -> bossDie() sets bossDefeated + the death animation advances. Full harness 0 errors. In-game clip `boss_fights_showcase.mp4` (bz6 spiral, bz5 inferno, esB_big2 twin, esB_big6 — all actively attacking, projectile pixels confirmed 2.8k-23k per segment). Sheets: wired_megabosses.jpg, wired_minibosses.jpg.

### NOT wired yet (still available): chopper, continental/tankboss, iboss (ice), fboss (Falva) — Mike deferred these. bz/esB are NOT yet placed in any stage's wave script (spawnable + fully functional, but need Mike's call on which boss goes on which level).

---
## DROP 2026-07-16d — bosses face player + void clip fix + richer attacks

### Void (bz6) clipping fixed
Not a screen-edge clip — bz6's crescent wings are the widest bz frame (200px native). Reduced its draw scale to 0.92 (others 1.02). Isolated-sprite scan: bz6 now spans x=228..538 of 960, clean margins both sides. (Apparent "clip" in earlier catalog sheet was the sheet's own crop, not the game.)

### Bosses now FACE THE PLAYER
All bz mega + esB mini art natively points the nose UP (away) — verified by nose-width scan. drawBossSprite (mega) and drawSubBoss (mini) now wrap the sprite draw in a vertical flip (ctx.scale(1,-1) about the draw center) so every boss points DOWN at the player. Death/hurt/enrage tints flip with it. Verified bz6 narrow end now at bottom (faces player). Regular L1 jets (bomber/intcp/turdrone/mdrone) already face down natively (nose-width scan) — no change needed; drone is a noseless swarmer (n/a).

### Attacks massively improved — multi-phase cycling patterns
Rewrote bossProfileAttack: each profile now CYCLES sub-phases via b.atkPhase (b._profPhases, advanced by the profile itself, NOT the old random timer — guarded off for mega/mini in updateBoss/updateSubBoss). Fire origin moved to the underside (b.h*0.30, which now faces the player).
- siege(3): marching bullet wall with a MOVING safe gap -> aimed twin plasma stream -> field-wide mortar rain.
- spread(3): aimed pellet fan -> rotating full ring -> aimed 3-dart.
- ice(3): expanding frost nova -> drifting frost wall with gap -> aimed shard burst.
- homing(3): 5-missile salvo -> MG suppression stream -> 4-missile + plasma double salvo.
- inferno(3): rotating flame spokes -> sweeping flamethrower arc -> chaotic blast burst.
- spiral(3): counter-rotating double spiral -> pulsing ring -> homing brood + aimed plasma.
- strafe(2)/twin(2) for minis: raking MG / aimed darts alternating with a spread volley.
Rage (mega past 50%) adds bullets + the existing 0.6x fireCd. Verified all 7 megas cycle phases {0,1,2}; all 13 bosses still named/attacking/drawing; harness §22 green (7/7, 6/6, death advances). Clip: boss_fights_v2.mp4.

---
## DROP 2026-07-16e — curved-fireball fix (fire-only) + LEVEL 1 boss & miniboss wired

### Curved fireballs are now fire-only
The 'blast' projectile (mfx_bpow curved fireball art) was used across many boss profiles. Restricted it to the FIRE boss only: the 'inferno' profile (Magma Tyrant bz5) keeps its curved fireballs; everything else swapped to on-theme neutral projectiles — siege mortar rain -> 'shell', ice aimed shards -> 'gem', void spiral -> 'voidOrb' (purple) + 'plasma'. Verified: level-1 boss emits zero 'blast'; Magma Tyrant still does.

### LEVEL 1 boss + miniboss wired
- BOSS: 'damkeeper' (stage-1 boss slot) draws the chopper art via NEWBOSS[1] and fights with the stage-1 helicopter attack (side-pod MGs, rocket pods, strafing). Renamed THE DAM KEEPER -> JUNGLE OVERLORD-X to match its chopper identity.
- MINIBOSS: SUBBOSS[1] set to 'esB_big5' = OLIVE MAULER (jungle-camo gunship plane, strafe profile) — replaces the old 'subtank' placeholder. Faces the player (flip), idle/fire/hurt/death states, amber HP bar.
Verified (test_fl.js §23): miniboss is OLIVE MAULER esB_big5; boss is JUNGLE OVERLORD-X chopper; boss uses no curved fireballs; fire boss does. Full harness green. Clip: level1_boss_miniboss.mp4 (Olive Mauler strafing run, then the Overlord-X chopper).

### Next: wire bosses level-by-level (Mike's plan). L1 done. L2-6 pending Mike's boss picks per stage. Deferred art still available: continental/tankboss, iboss, fboss, bz0-4/6, esB_big1-4/6.

---
## DROP 2026-07-16f — miniboss flip removed (was upside down)
Minibosses (esB_big1-6) are wide symmetric gunships; the vertical flip added last pass rendered them UPSIDE DOWN. Removed the flip from the drawSubBoss mini branch — they now draw in native orientation (correct per Mike). Mega bosses (bz) keep their flip: bz2/bz3/etc are clear fighters with a distinct nose that the flip correctly points at the player (bz6 void is the one ambiguous wide one). Olive Mauler (esB_big5) confirmed as L1 miniboss. Harness green. Clip: level1_boss_miniboss.mp4 refreshed.

---
## DROP 2026-07-16g — OLIVE MAULER smart evasive AI (L1 miniboss)

Mike's spec, all implemented in updateMauler (routed from updateSubBoss when art==='esB_big5'):
- BARREL-ROLL: fast 360 spin (~0.5s) to dodge — triggered by THREAT DETECTION (scans pBullets for a rising shot lined up under the boss within 150px); rolls AWAY from the incoming bullet, slides 260px/s sideways during the roll to actually evade, then 0.9s cooldown. Draw: ctx.scale(cos(roll),1) — the sprite flattens edge-on then flips, a real 3D-ish barrel roll. Attacks suppressed mid-roll (ship inverted).
- TILT dodge: lighter/faster bank (0.35s, 150px/s slide) as the alternate dodge; sprite banks via ctx.rotate(tilt). AI picks roll (55%) vs tilt.
- Bob: sine drift across the top (VW/2 +/- 110).
- GREEN LASERS: new eglaser projectile — palette-swapped the pink Falva laser (fllaser) to GREEN with a WHITE INTERIOR (make_green_laser.py -> eglaser_0..7, luminance-keyed: white core preserved, colored parts remapped green; manifest +8). Fast (spd 8.4), aimed; occasional 3-round; render is additive with green glow.
- BACK-MOUNTED HOMING MISSILES, alternating loop: maulerVolley cycles [R:2, L:2, R:4, L:4] -> R fires 1,2, L fires 1,2, R fires 1,2,3,4, L fires 1,2,3,4, repeat. Quick 0.16s within a salvo, 0.7s between salvos. Each launches from the BACK (top edge) via enemyLockOn -> reticle + alert + homing missile on the player. Brief gold back-muzzle flash per launch.

Verified (test_fl.js §22): green white-cored lasers fire; missiles create reticles (peak 4 locks); barrel-roll frames (93) + tilt frames (66) when threatened; missile side sequence exactly RRLLRRRRLLLL. Full harness green. Clip: mauler_ai_showcase.mp4.

---
## DROP 2026-07-16h — Mauler: single-spawn confirmed + spins made visible

Mike: "should be 1 boss, and I don't see him doing his spins."
1. SINGLE SPAWN confirmed: the real stage spawns exactly ONE miniboss (guarded by subBossTriggered flag; simulated full stage -> spawn count 1). The two bars Mike saw were from showcase test scripts spawning duplicates manually, not a game bug.
2. SPINS NOW VISIBLE: the barrel-roll logic was correct (cos(roll) sweeps 1->0->-1 over a 360 spin in 0.5s) but only triggered on threat, which was sporadic. Added: (a) periodic "show-off" barrel roll every ~3.2s even when not threatened, (b) wider/taller threat detection (220px tall, 0.55*w wide, vy<-0.5), (c) a bright green motion-STREAK behind the spin + a white rim-flash at the edge-on moment so the roll reads unmistakably even at speed, (d) squash floor lowered to 0.10 (thinner edge-on). Verified: 117 roll frames + 66 tilt frames in the AI test; 156 rendered frames show the spin motion-streak. Harness green. Clip: mauler_ai_v2.mp4.

---
## DROP 2026-07-16i — Mauler: smoother dodges + green lasers made clearly visible

Mike: dodging too jerky/fast; didn't see the green lasers.
1. SMOOTHER MOTION: barrel roll slowed 0.5s -> 0.85s per 360 (PI*2/0.85); sideways slide 230->150 px/s; tilt slide 150->95, tilt dur 0.35->0.5s; periodic show-off roll 3.2s->4.5s; dodge cooldowns up. Less jerky, reads as a deliberate maneuver.
2. GREEN LASERS now unmistakable: they WERE firing/rendering (verified created, moving, art ready) but were thin/fast/faint over bright terrain. Now: ~33% bigger sprite, added a trailing green beam gradient behind each bolt, white-hot core pass, bigger glow; fire cadence tightened (cd 0.7-1.1s -> 0.45-0.75s, 3-round spread 30%->55%), speed 8.4->7.2 so they read as beams. Verified: peak green-laser pixels 1381 -> 11289; visible in 420/420 frames (was 200). Harness green (6 lasers in air). Clip: mauler_ai_v3.mp4.

---
## DROP 2026-07-16j — green lasers made unmistakable + "blue dots" diagnosed

Mike: "he's shooting the blue dots, not the lasers — unless your video feed isn't accurate?"
DIAGNOSIS: terrain-diff analysis (render full frame minus a projectile-free frame) proved the Mauler ONLY emits eglaser (green) + emissile (orange homing) + red reticles. The "blue dots" are the JUNGLE RIVER/WATER sparkles in the terrain background (bright blue 10,123,179), NOT the Mauler's shots. My earlier feed was accurate but the thin lasers over the blue water were easy to misread.
FIX so it's unambiguous: rewrote the eglaser render to be fully PROCEDURAL (no longer art-load-dependent — removes any browser-vs-harness art-loading risk). Now every laser is a thick layered beam: green trailing gradient + outer green body (#37e64a) + bright green mid (#9dff8a) + white-hot core (#f2fff0) + strong glow. Terrain-diff projectile pixel census after fix: green=130743 (dominant), orange=104480, red=115770, blue only 28206 (glow bleed). Harness green (6 lasers in air, sequence RRLLRRRRLLLL). Clip: mauler_ai_v4.mp4.

---
## DROP 2026-07-16k — real bugs from Mike's screenshot: black-box missiles + double-boss (showcase) + blue-balls explained

Mike's screenshot showed: black squares near the ship, blue balls, and "2 bosses in the video".
DIAGNOSED via pixel analysis of the screenshot + terrain-diff:
1. BLACK BOXES = the Mauler's homing missiles. eHomingMissile pushed emissile with NO mkey -> render fell to 'mslB_2_[0,4,5]' = the near-black generic-enemy missile art (verified mean 29,26,24). FIX: eHomingMissile now sets _bright:true; new render branch draws a clearly-visible glowing rocket (white body, red nose, fin band, additive flame-exhaust trail, muzzle glow) instead of the dark art. Verified: 0 square black boxes remain (leftover black blobs are all irregular = jungle terrain shadows); 25k bright-rocket px on screen.
2. BLUE BALLS = the PLAYER'S OWN bullets (weapon 0 = 'mg', blue 70,142,242). Not the boss. Not a bug.
3. TWO BOSSES = a bug in MY showcase script (maulershow.js): it called updatePlay (which already runs updateSubBoss) AND an explicit updateSubBoss/drawSubBoss, double-updating/drawing the boss. The real game calls drawSubBoss once (verified) and spawns exactly one (subBossTriggered guard, verified full-stage sim = 1). Fixed the showcase to spawn with subBossActive=true and let updatePlay handle update; draw once.
Harness green. Clip: mauler_ai_v5.mp4 (single boss, green laser beams, bright homing rockets).

---
## DROP 2026-07-16l — expanded to 8 STAGES + stored stage-card/font pack

Mike sent Bullets_of_Fury_Stage_Cards_and_Font_Atlases_1-8_v4.1.zip (8 stage cards + 8 per-stage font families + blow-by VFX). Game is now 8 stages (was 6); 2 new levels added.

STORED: src/incoming_stagecards_0716/ (full pack: Cards/{Card_Base,Title_Layer,Final_Embedded,Blow_By_VFX}, Fonts/ per-stage AZ09+symbols atlases 13x4 cell96, Documentation contact sheets, manifests). 7.4M.

STAGES array expanded to 8 with the pack's canonical names/order:
  1 RUMBLE IN THE JUNGLE (jungle) - boss damkeeper/chopper [wired]
  2 IT'S HOT IN HERE (volcano) - boss dreadnought
  3 ICE STILL CAN'T SEE (ice) - boss wargod
  4 CROUCHING MISSILES, HIDDEN DEATH (sky) - boss spider
  5 ALL FOR ONE, NONE FOR ALL (space) - boss leviathan [music lvl5 via assemble patch, anchor now 'stage5mus']
  6 HEAVY TURBULENCE (sky) - boss TBD  [NEW]
  7 NOT ANOTHER SEWER LEVEL (sewer) - boss TBD  [NEW]
  8 FURIOUS DEATH (space) - boss TBD  [moved from stage 6 -> finale]
Structural wiring done: win condition uses STAGES.length (auto-8); password codes extended to 8 (added TURB, SEWR); crate-throwback ref 6->8; NEW 'sewer' background added to drawBG (dark channel + brick walls + flowing sludge canal); all 8 stages boot without crash (verified).
assemble.py patches realigned to the new STAGES formatting (stage5 music/sub). Removed the old "GOD HELP US ALL" stage5-sub override so the pack's canonical "ALL FOR ONE, NONE FOR ALL" stands. test_fl.js updated: 8 stages, stage8=FURIOUS DEATH, stage6=HEAVY TURBULENCE, stage7=SEWER; made the tilt-dodge assertion deterministic (was RNG-flaky).

NOT yet done (needs Mike's stage backgrounds + BOF.stageArt atlas integration): wiring the Final_Embedded illustrated cards into the drawIntro card-drop (currently falls back to procedural title text for stages without atlas art); per-stage font glyph atlases into curFontArt; bosses for stages 6/7/8; actual level background art + drivable terrain for the 2 new levels; blow-by VFX overlays.

Previews delivered: preview_stagecards.jpg (all 8 cards), preview_fonts.jpg (all 8 font families), sewer_preview.jpg (new stage-7 bg in-engine).

---
## DROP 2026-07-16m — L2 miniboss (Crimson Talon) + Galaga kamikaze drone AI

### LEVEL 2 miniboss
SUBBOSS[2] set to 'esB_big6' = CRIMSON TALON (red/fire gunship, mean color 86,46,43 — matches the volcano "It's Hot in Here" theme). Uses the twin attack profile + faces player. Replaces old 'subdread' placeholder.

### GALAGA-style kamikaze drones (new 'kamikaze' pattern on the drone type)
Mike's spec: drones act like homing missiles with their BODIES toward the player, spawn as horizontal PAIRS, split off and criss-cross the screen. Implemented in the pattern switch with a phase machine:
- enter: drop to the hover line as a side-by-side pair (_kmSide -1/+1)
- cross: swoop along an eased arc to the mirrored (partner's) x, dipping down mid-screen so the paired drones CROSS in an X; banks into the swoop (_bank). Does this TWICE (crosses back).
- lock: brief telegraph, shudders, aims nose at the player.
- dive: BODY as a homing missile — accelerates along the aim, curves toward the player with a limited turn rate (2.4 rad/s), nose points along travel; culled when off-screen (missed).
Spawned via vKamikazePair(pairs, opt) — staggered horizontal pairs. Wired into stage 2 waves (5 waves, escalating: 1 pair -> 2 -> 2 fast -> 3 -> 2 faster pre-boss).
Draw: kamikaze drones rotate by _bank during swoop and point nose along the dive vector; committed dives get an additive exhaust glow (orange on stage 2). Verified (test_fl.js 24): 4 drones/2 pairs, phase chain enter->cross->lock->dive, criss-cross confirmed (separation 0..202px), body-dive confirmed. Harness green. Clip: kamikaze_drones_showcase.mp4.

---
## DROP 2026-07-17a — robo drones restored + stage-2 level display fixed + purple residue addressed

Mike's screenshot (live play) showed: recon JETS as kamikaze drones (wanted the classic ROBO drones), the stage-2 level display broken (terrain covering only left ~2/3, raw animated lava + dark-red band exposed on the right with a dead-straight edge), and purple halos/residue.

1. ROBO DRONES: line ~1192 drone->e1 'recon' mapping made STAGE-1-ONLY. Stage 2+ drones (incl. all kamikaze) now draw the classic atlas robo saucers (drone0/1/2, 30x22) via the atlas path (~4644), which also got the kamikaze _bank swoop rotation + dive-vector nose rotation + orange exhaust glow. Verified: harness asserts kamikaze drones have no e1 on stage 2 + stage-1 drones still recon; pixel scan of 5 showcase frames = 0 large white-jet blobs.
2. LEVEL DISPLAY ROOT CAUSE: stage-1's 800px h-scroll camera state leaked into stage 2 — beginStage didn't reset camX (up to 320) and drawWorld's translate gated on the CACHED WORLD_W (only updated inside updatePlay), so any stage-2 draw before an update shifted the whole render left by -camX, exposing the untranslated lava back-layer on the right (the dead-straight edge + red band). FIX (landed at compaction, now verified + regression-locked): beginStage sets camX=0; WORLD_W=worldWidth(); drawWorld calls updateCamX() first and gates the translate on live worldWidth()>VW. REPRO PROVEN: sim stage 1 with player at x=760 for 120f -> camX=320; beginStage(2) -> camX=0/WORLD_W=480; first stage-2 frame drawn BEFORE any update shows only 11% right-side lava (designed river channels) vs ~90% broken. test_fl.js sections 25+26 lock it.
3. PURPLE HALOS: two sources. (a) master art: dim-violet residue px (~16 found in an earlier scan) along the river — master now scans CLEAN (0 by the same test; cleanup landed at compaction). (b) H264 4:2:0 chroma subsampling fringes purple around saturated red-on-dark in the DELIVERED MP4s — this is a video-compression artifact, not game rendering. Mitigated: showcase encodes bumped to -crf 18 (measured 29% purple-fringe reduction @f80). In-game rendering has no purple.
Full harness green (sections 24/25/26). Clip: robo_kamikaze_fixed.mp4 (robo drones criss-cross + body-dive on the fixed stage-2 display, Crimson Talon at the end).

---
## DROP 2026-07-17b — menu: flashing gold INSERT COIN + copyright line

Mike: remove the small "© COLEFORGE STUDIOS — INSERT COIN" credit at the bottom; put a LARGER bold flashing/glowing gold "- INSERT COIN -" right above NEW GAME; bottom line becomes "Copyright 2026 ColeForge Studios".
IMPORTANT BUILD NOTE: the live drawTitle is in patches.js (line ~150+), NOT the gamecode.js drawTitle (which is dead/overridden). Edits to the menu MUST go in patches.js or assemble.py silently discards them. First attempt edited gamecode.js and was overwritten — fixed by editing patches.js.
Implemented in patches.js drawTitle: after drawMenuButtons, draw "- INSERT COIN -" at cx=VW/2, cy=TMENU_Y0-30 (TMENU_Y0=168, so ~y138, just above the NEW GAME button). bold 22px Arial Black/Impact stack, dark outline for legibility, gold vertical gradient, shadowBlur 14+pulse*20 and alpha 0.6+0.4*pulse driven by 0.5+0.5*sin(t*3.2) => glowing + flashing. Bottom line changed to 'COPYRIGHT 2026 COLEFORGE STUDIOS'. Verified: INSERT COIN gold px pulses 2456..4631 (0.53 ratio = flashing), copyright present, old credit gone. Clip: menu_insert_coin.mp4.

---
## DROP 2026-07-17c — PASSWORD screen fixed (stuck-on-B, weird typing, couldn't enter codes)

Mike: password permanently stuck on B, typing acts weird, can't enter passwords.
ROOT CAUSE (patches.js drawPassword — the live one; gamecode.js version is dead): the fire/confirm handler was
  _selFire = enter || space || keybind.fire(j) || pad_b0 ... => pwKey(NAV[sel].c)
so ANY fire/enter press inserted the currently-HIGHLIGHTED on-screen keypad letter. The selector defaulted to sel=0 and the arrow/WASD nav could move it onto B — then every fire/enter typed 'B' (the "stuck on B"). Typing a letter then pressing fire inserted BOTH the letter and the highlighted key (e.g. 'f'+fire -> "FA"), the "weird typing". WASD were also bound to keypad navigation, so those letters navigated instead of typing.
FIX (patches.js): 
 - Keyboard now types letters/digits DIRECTLY; ENTER submits the password (never inserts a keypad letter); BACKSPACE deletes / exits when empty.
 - The on-screen keypad's confirm is GAMEPAD-ONLY (pad_b0/pad_b9) plus MOUSE click; keyboard fire keys no longer activate it.
 - Selector starts UNSET (sel=-1) so keyboard users see no highlighted key hijacking input; first d-pad press snaps it to a key.
 - Removed WASD from keypad navigation (arrows + gamepad d-pad only) so W/A/S/D type as password chars.
Also fixed stale password data for the 8-stage layout: PASSWORDS now FURY1 IRON2 DAM5-3 STRM4 ORBT5 TURB6 SEWR7 DETH8 (was missing TURB/SEWR and had DETH=6); _PWMAP (font preview) extended to 8.
Verified (harness §27 + standalone event-driven sim): type FURY->submit->intro; fire j with selector on B inserts no 'B'; A/D type; held-B key-repeat inserts once; backspace deletes; all 8 codes submit; invalid code rejected. Full suite green. Still: pw_screen render shows the typed code with no stuck highlight.

---
## DROP 2026-07-17d — 7 new music tracks + password music (untitled w/ fade-in) + menu logo removed

MUSIC: added Mike's 7 uploaded WAVs to assets/music/, converted to 192k MP3 (97MB WAV -> 13MB MP3, no audible loss, game already loads mp3). Registered in BOFA.music (manifest.js, hand-maintained — assemble.py does NOT touch it):
  untitled -> assets/music/untitled.mp3   (ALSO repointed 'password' -> untitled.mp3)
  battlesky -> Battle_in_the_sky.mp3, fierceplanes -> Fierce_Planes.mp3, hotflight -> Hot_Flight.mp3,
  ironcage -> Iron_Cage.mp3, lordshadows -> Lord_of_the_shadows.mp3, crawling -> crawling.mp3
FADE-IN: untitled (password screen) got a 1.2s afade=t=in baked in for a natural start (verified: RMS ramps 507 -> ~12000 over the first 1.2s, 0.041 ratio). The other 6 got a short 0.4s fade-in so none start abruptly. 'password' was enter-password.mp3, now untitled.mp3.
NOTE: these 6 new gameplay tracks (battlesky/fierceplanes/hotflight/ironcage/lordshadows/crawling) are LOADED and selectable by name but not yet assigned to specific stages/bosses — Mike can tell me which track goes where, or I can propose a mapping.

MENU LOGO REMOVED: patches.js drawTitle drew the ColeForge/Phoenix menuLogo at top (y70) right before drawMenuButtons — removed per Mike's repeated request. Menu now shows starfield -> INSERT COIN -> buttons. Verified: top-region orange/logo px dropped to ~914 (nebula only), top brightness 1%, INSERT COIN still 4294 gold px, buttons unchanged. (Boot/splash/attract logos at lines ~85/509 are separate screens, left intact.) Clip: menu_nologo.mp4.
Harness green.

---
## DROP 2026-07-17e — INSERT COIN in stage-2 font + raised 10px; stored MegaPack v5.2

MENU: "- INSERT COIN -" now renders in the STAGE-2 bitmap font (ASSETS.stageArt['2'].font — the "It's Hot in Here" fire font; verified all glyphs I,N,S,E,R,T,C,O + dash present, no gaps) instead of the browser Arial Black. Raised 10px (cy=TMENU_Y0-40, was -30). Still flashing/glowing gold via shadowBlur + tint-alpha pulse (0.5+0.5*sin(t*3.2)). Browser-font fallback retained if the stage-2 font isn't loaded yet. Verified: gold px 8952..14256 pulsing (heavier coverage than the old thin font = the bitmap font). Clip: menu_s2font.mp4.

STORED MegaPack v5.2 (6 parts, 302MB) -> src/incoming_megapack_v5_2/ (excluded from delivered zip via src/ rule; safe in working project). "Campaign Flight + Rival Dogfight Mega Vault v5.0", true top-down 16-bit 800x1000, BOTH #FF00FF chroma authoring AND de-haloed BINARY-ALPHA runtime versions (verified stage-2 runway alpha files: 0 partial-alpha px, 0 magenta halos — directly fixes the purple-halo issue). Categories:
  01-player-ships, 02-runways (all 8 stages, 3-piece vertical sets start_approach/main_runway/runway_exit sharing exact 128px seam bands), 03-stage-transitions (7 x-to-y), 04-rival-dogfight (open-air courses, breakable objects, missile crates, checkpoints, tunnels, satellites, asteroids), 05-parallax-objects, 06-stages, 07-bosses-and-sub-bosses (107MB — many named bosses: airbase-siege-fortress, cesspool-leviathan, continental-crusher, cryo-behemoth, bio-sludge-abomination, black-eagle-j20, etc.), 08-vehicles-tanks-planes-naval, 09-vfx, 10-stage-cards-and-fonts, 11-liquids-and-falls, 12-source-sheets, 13-manifests.
Readme notes: stack runway pieces bottom->top; jet stays native-sized in play (100/75/50/37.5% nearest-neighbor for launch cinematics only, NO bilinear); rival courses are open-air (no forced 2P lanes), tunnel order exterior_entry->interior_run->exterior_escape. "these are next on the list" — NOT yet wired; awaiting Mike's direction on what to integrate first.
Harness green.

---
## DROP 2026-07-17f — INSERT COIN raised another 10px
cy = TMENU_Y0-50 (was -40). Stage-2 font, flashing gold, unchanged otherwise. Verified flashing (gold px 10472..15247).

---
## DROP 2026-07-17g — animation-needs audit + Overlord-X is the smooth-rotor helicopter

Mike: dam-breaker's blades are baked into its idle frames (only 6 → won't work for smooth spin). Wants the OTHER helicopter (separate blade) animated smoothly 360° every 5-15°, overlaid+anchored on the body. Also asked for a separate sheet of enemies needing animations + notes.

FINDINGS (full audit in ANIMATION_NEEDS.md; visual in animation_needs_sheet.jpg):
- **jungle-overlord-x-helicopter** is THE one with a separate rotor: body-intact-192 + rotor-f01..f12 (12 frames=30°), both 192x192 co-centered, rotor is real blades (~13% opaque, rotatable — not a blur disc). Fully componentized too (cockpit/nose-chainguns/L+R weapon-wings/tail-engine, each intact/damaged/critical). => use THIS for L1 boss w/ smooth blade.
- Classification of all ~70 bosses: 1 SEPARATE-ROTOR (overlord-x), 48 COMPONENTIZED (continental-crusher has 24 parts; jungle-hornet, thorn-predator, rival jets, ice-colossus, etc.), 15 BAKED-FRAMES-ONLY (dam-breaker, magma-colossus, obsidian-drill-tank, glacier-rail-fortress, toxic-dredger, furious-death normal/super/ultra, ... — these CANNOT be smooth-rotated without new authored parts), 6 STATIC/states-only.
PLAN for the rotor overlay (documented in ANIMATION_NEEDS.md): build-time pre-render blade rotation set (like gen_rot.py) at 5-15° steps (24/48/72 frames) on fixed square canvas, register in manifest, draw body then blit rotorFrame=round(spin/step)%N centered on shared 192px anchor, spin speed in deg/sec independent of frame count, swap BODY art for damage states while rotor overlay stays. NOT yet built — awaiting Mike's go + chosen step (5/10/15°).
Deliverables: animation_needs_sheet.jpg, ov_rotor12.jpg (the 12 supplied rotor frames), ANIMATION_NEEDS.md in project root.

---
## DROP 2026-07-17h — Jungle Overlord-X: smooth spinning rotor overlay (BUILT)

Built the separate-blade helicopter animation Mike asked for. gen_rot.py extended (gen_overlord_rotor): pre-renders the megapack rotor (jungle-overlord-x-rotor-f01, 4-arm 90-deg-symmetric blade, native 192 canvas) into ovrotor_00..71 = 72 frames at 5-degree steps, plus copies body-intact/damaged/critical-192 -> ovbody_intact/damaged/critical. Registered in manifest (445 base + 75 overlord frames). Files: assets/fx/rot/ovrotor_*.png, ovbody_*.png.
DRAW: new branch at top of drawBossSprite for b.kind==='damkeeper' when XART.rdy('ovbody_intact'): pick body by HP frac (>0.66 intact / >0.33 damaged / crit), draw body, then overlay rotor frame ri=round(((b.t*900)%360)/5)%72 at the SAME rect (shared 192 center = anchored). ~900 deg/sec spin, derived from b.t (dt NOT in draw scope — important). flash tint + death fade handled. Dispatch guard (~line 4799) updated so damkeeper routes to drawBossSprite when ovbody_intact is present (takes priority over old chopper art).
VERIFIED: spin angle cycles 0-360; rotor region changes every frame (22-28 avg diff = ~15deg/frame @60fps); body centroid drifts only 6.5px x (the boss's own strafe, not rotor wobble) = rotor anchored to body; damaged body swaps at 50% HP. Harness green (section 28: 3 body states + 72 rotor frames + index advances). Clip: overlord_rotor_spin.mp4.
NOTE: b.t-based spin means spin resets with the boss clock but is continuous during the fight; fine for a chopper. NOT wired: nose-chaingun/wing/tail component overlays + their damage states (available in pack) — future pass if we want per-part damage.

---
## DROP 2026-07-17i — Jungle Overlord-X: full health-gated smart boss AI (BUILT)

Implemented Mike's complete boss spec. New updateOverlordX(b,dt) (self-contained; hooked at TOP of updateBoss for kind==='damkeeper' stage 1, bypasses generic boss movement/fire — IMPORTANT: bossAttack() has no dt, so the AI is driven per-frame from updateBoss which does). Weapon mounts on the 192 body via ovMount(b,ox,oy) scaled by b.w*1.15/192: nose twin chainguns (~0,+54), L/R rocket wings (-48,+41)/(+46,+41).
Helpers: ovTwinMG (orange/white 'mg' pellets from nose, slight spread, aimed), ovRocketSide(b,side) (one wing homing '_bright' rocket + gold muzzle flash, alternating), ovReticleVolley (enemyLockOn reticle + staggered 8-rocket 1-2-1-2).
PHASES (fight state): twin-MG burst -> wait ~3s -> pivot (side turn) -> MG again -> alternating homing rockets (1 ... 2-3s ... 2 ... repeat) -> loop. Below 50% HP: 3 rapid MG burst-sets per volley + side pivots. 
50% GATE: chargeOff (rush toward player, accelerate off bottom) -> reentry (swoop in at 45deg from a void corner, bank/swerve, drop reticle, fire staggered 8 rockets 1-2-1-2, 2 passes) -> back to fight (enraged).
HP-GATED FX: <=50% tail smoke plume (dark particles anchored at tail mount ~(0,-52)) + periodic explode() pops "to show smoke start"; <=25% (crit) faster/darker smoke + ember bits + more frequent explosions + desperation extra MG phase. _pivot rotates the drawn body+rotor (draw-side, decays 0.93/frame since no dt).
VERIFIED (harness §29 + sim): peak 14 MG pellets (orange 3226px/white 245px), homing rockets fire, 499 pivot frames, charge-off + reentry + reticle all reached at 50%, smoke 14 particles @50% -> 31 @25%, reentry warm/rocket px 162k. Harness green. Clip: overlord_boss_fight.mp4.
NOTE: smoke uses particle system; an addTrail sprite-smoke system exists and could upgrade it later. Per-part component damage (wings/nose/tail) still available in pack, not yet wired.

---
## DROP 2026-07-17j — Overlord-X: missiles now VISIBLE + aircraft-realistic movement (researched)

Mike: attacks good but didn't see missiles; asked me to research how real jets/helicopters/aircraft fly.
MISSILE FIX: rockets were spawning but hard to see (only 1 alive, tiny, fast). Now: ovRocketSide fires bigger rockets (14x24 vs 12x20) that START slow (spd 2.4) and ACCELERATE (_accel 0.06 -> _maxspd 4.0) so they're readable leaving the pod then home in fast (added accel ramp to the emissile updater). Rocket phase now fires a PAIR per blast (2 rockets, slight fan) alternating sides every ~2.4s. Verified: rocket phase keeps ~6 rockets on screen (present 400/400 frames), reentry volley peaks at 16. Harness §29 asserts rockets on-screen + travel.
AIRCRAFT-REALISTIC MOVEMENT (from research — attack-heli doctrine + fighter strafing/dogfight tactics):
- Attack helicopters "dart to a firing position, engage, then rapidly relocate" -> fight state now picks a firing position to ONE SIDE of the player, eases to it, HOLDS to fire, then relocates to the opposite side.
- Bank INTO the turn (real cyclic roll: roll toward travel direction) -> _pivot now tracks lateral velocity during repositioning.
- Charge run: accelerates the whole way in (builds speed toward target), strafes MG on the approach, banks hard toward the intercept line.
- Reentry = high-yo-yo/strafing reengagement: diagonal ~45deg swoop-in banked hard into the curve, S-weave jink lining up, level out to fire the 8-rocket volley, then PULL UP HARD and bank away off the corner (the 4-G pullout real fighters do after a strafing run) before the next pass.
Sources: avstop helicopter handbook (bank into turn via cyclic), FM1-112/DCS attack-heli doctrine (dart-engage-relocate), Air&Space Forces mag (hard pull-up after strafe), USNI 7 dogfight moves (high-yo-yo, scissors). Harness green. Clip: overlord_boss_fight.mp4.

---
## DROP 2026-07-17k — Overlord-X: fixed trail-first missiles, black+red-tip art, bigger; orange/white pellets (not blue)

Mike: missiles flying TRAIL-FIRST; use the black missiles w/ red tips + add trails + make bigger; pellets shouldn't be blue, should look like MG pellets.
MISSILE ART: the black+red-tip art (mslB_2_0) turned out to be a TOP-DOWN/head-on view (red nose-cone dead-center, aspect 1.42) that can't rotate into a clean side-flying missile. Switched to waf_rocket_0 (clean 25x94 vertical side-view missile, red tip, narrow nose). gen_rot.py gen_boss_missile now builds omsl_00..71 from waf_rocket_0 (nose points DOWN natively at frame 0). Draw maps frame = round((_ea - PI/2)/5deg) so the NOSE LEADS the travel direction (verified: downward missile now narrow-nose-down = nose-first, was trail-first). Size bumped to 40px (was ~26). Fiery trail (white/gold/orange puffs) drawn BEHIND the missile opposite travel.
PELLETS: root cause = boss fired eShoot('mg') which uses the player's LEVELED mg palette (blue at lv2), AND my first emg draw was accidentally placed in the pBullets(player) loop so it never ran (pellets fell through to a default blue circle). Fixed: ovTwinMG now pushes kind:'emg' bullets; added a dedicated emg draw at the TOP of the ENEMY bullet loop — elongated orange body / gold mid / white-hot core, oriented along travel. Verified clean-bg: 2749 orange, 0 blue.
Verified numerically (isolated, plain bg): MG phase 14 pellets all orange/white 0 blue; rocket phase missiles nose-first (narrow red-tipped nose leads downward) with trails, 0 blue. Harness green. Clips: overlord_boss_fight.mp4; stills overlord_rockets/ovproof.

---
## DROP 2026-07-17l — NO MORE PLACEHOLDERS: boss MG now uses the REAL in-game enemy tracer art (mfx_bmg)

MIKE'S STANDING RULE (permanent): NEVER make placeholder/procedural sprites. The game has a huge art library — ALWAYS search assets (manifest BOFX.img keys), src/ art packs (megapack 09-vfx etc), before drawing anything by hand. If unsure, render the strongest found candidates and ask.
FOUND: the game already ships REAL enemy machine-gun tracer art: mfx_bmg_0_0..3_0 (5x20px elongated warm orange/gold/white tracers, 4 flicker variants, 76-82% warm). The engine even has a FIRETYPES 'pellet' entry + _EFX_ALIAS mg->pellet that draws them with flicker + gold glow... but it NEVER WORKED because the art fn generated keys 'mfx_bmg_N' while the registered keys are 'mfx_bmg_N_0' -> XART.rdy failed -> blue fallback circles. THAT was the original "blue pellets" root cause.
FIX: (1) FIRETYPES.pellet art fn now appends '_0' (engine-wide fix — every enemy that fires kind 'mg' now shows the real tracers). (2) Deleted my hand-drawn 'emg' placeholder draw entirely. (3) ovTwinMG fires kind:'mg' with _ph stagger so pellets flicker across the 4 variants.
VERIFIED: isolated 535 orange/0 blue; boss fight MG phase 14 pellets, 1375 orange/0 blue. Harness green.
ALSO CATALOGED for future use: mfx_bshot_ families (0: small grey shot, 1: blue plasma ball, 2: small round), iproj_0..30 (large blue beam/laser strips), megapack 09-vfx: chaingun-muzzle 7f + ice-chaingun-muzzle 7f (heli chaingun MUZZLE FLASHES — perfect for Overlord-X nose guns later), fireball-projectile 7f, missile-launch 7f, heavy-missile, naval-shell-torpedo, storm-lightning-orb, toxic-sludge-glob, unity-star-bolt, tank-cannon-flash 6f, jet-thruster-blue 6f. Sheets: enemy_mg_examples.jpg, enemy_fx_catalog.jpg.

---
## DROP 2026-07-17m — fx_masters ARE the art sources: bossmachinegun + homing missile masters wired

Mike rejected mfx_bmg/homR picks: "none of these — go into the art sources folder." The art sources = **src/fx_masters/** (bossmachinegun.png, homing_missle_-_bossandplayer.png, enemymissilefx.png, machinefx.png, enemyatkfx_s.png, bossfx.png, bosspowerattack.png, laserbeam.png, spreadfirefx.png, explosivefx.png, blowupfx/2.png, eenemyships.png). These are UNSLICED magenta-chroma masters (chroma = r>180,g<80,b>120 — NOTE b threshold must be loose, bg is ~(232,13,184)).
NEW SLICER: _BUILD_SOURCE/slice_fxmasters.py -> assets/fx/enemyfire/ + manifest registration (18 sprites):
  bmgun_0..2 (5x12 warm red-orange MG rounds) + bmgun_streak (5x38) from bossmachinegun.png
  bhom_0..4 (7x22..16x128 boss homing growth, LEFT set) + phom_0..4 (RIGHT/player) from homing_missle_-_bossandplayer.png — TRAIL IS BAKED INTO THE ART (growth stages = launch sequence)
  emslart_0..3 (11x36..21x50 enemy missile variants) from enemymissilefx.png
WIRED: FIRETYPES.pellet -> cycles bmgun_0..2 (boss MG pellets, real master art). Boss rockets: gen_rot.py gen_boss_missile now pre-renders omsl_00..71 from bhom_1 (12x79). ORIENTATION GOTCHA: bhom art NOSE IS AT THE BOTTOM (white-hot ignition y50-60 with plume rising UP; narrow dark nose tip at bottom) — so omsl_00 = nose DOWN, draw index = round((_ea - PI/2)/5deg). Removed my procedurally-drawn trail entirely (baked trail replaces it). Missile draw size s=56.
VERIFIED: downward missile = bright flame on top / dark nose leading below (nose-first); MG 14 pellets 3065 warm 0 blue; rockets 0 blue. Harness green. Sheet for Mike: fxmasters_strongest.jpg (bmgun + bhom/phom growth + emslart). AWAITING Mike's confirmation these are the right ones (esp. bhom LEFT=boss vs phom RIGHT).

---
## DROP 2026-07-17n — Mike's explicit art assignments (all four wired)

Mike picked the art directly ("everything inside the fx's folder"):
1) **MG pellets = mfx_mg_2_0 / mfx_mg_2_2** — FIRETYPES.pellet now cycles exactly these two (his images 1-2). Verified 1973 orange / 0 blue.
2) **Maverick helix = the venom green lasers (venom_0_0..9)** — REWORKED from rapid strand attack to VENOM HELIX LANCE: fires ONE heavy bolt per shot (cadence 0.38s, was 0.05s rapid), fast (vy -9.2), reasonably sized (h 30+lv*4, ~34-50px), animates THROUGH the venom growth frames as it flies (strands -> crossing X helix -> full beam, frame=min(9,age*22)), spiraling wobble, MASSIVE damage (8+lv*4, lv5=28) and PIERCES with a per-target memo list (_hs) so each victim is hit once — one lance destroys a whole 3-drone column (harness-verified; enemies get spliced from the array when killed, so 'array empty' = all dead). Crates also pierced. Both venomx updaters (updatePlay + updateRivalFight) updated to the straight-flight weave.
3) **Jets/planes rockets = waf_rocket_0/2/4** — generic (no-mkey, non-bright) emissiles now draw the real waf_rocket launch-growth by age (t<0.18 f0, <0.42 f2, else f4; nose UP in art -> rotate _ea+PI/2). Rival mkey missiles unchanged. Verified: 4 growing flame clusters 23->226 px.
4) **Copter homing missile = mslB_0_0 torpedo** (black, red tail fins LEFT + red pointed NOSE cone RIGHT — verified by end-height profile 139 vs 79px). gen_boss_missile regenerates omsl_00..71 from the tight crop rotated CCW (nose RIGHT -> UP); draw index = round((_ea+PI/2)/5deg). ROUTING FIX: only b._bright (boss) missiles use the torpedo branch — !mkey generics now fall to waf_rocket (previously !mkey stole the torpedo path). REAL white exhaust smoke trail already spawns from addTrail('missile') sprites in the emissile updater. Verified downward: wide tail fins on top (34px), pointed nose leads below (17px) = nose-first.
HARNESS: new section 30 (pellet art keys, ONE lance not pair, dmg>=12+pierce, 3-drone column destroyed, 72 torpedo frames, waf growth art). GOTCHA (test-side): stub enemies without full spawn fields go NaN in updateEnemies — always use spawnEnemy + pin coords in tests. All green.
Clips: overlord_boss_fight.mp4 (new pellets + torpedoes), venom_helix_lance.mp4 (Maverick shredding waves; peak 26.6k green px).

---
## DROP 2026-07-17o — pod muzzle flashes anchored, torpedoes downsized, venom split-lasers (no glow)

Mike: anchor missile muzzle flash on the helicopter's rocket turrets; scale missiles down a bit; remove the ugly glow on the helix lance; the solid-piece stage looks weird -> split into separate lasers that destroy enemies in their paths.
1) POD FLASH: megapack 09-vfx missile-launch-f01..07 (96px, vertical plume, ignition at top) registered as mlaunch_0..6 (slice_fxmasters.py _reg_mlaunch). ovRocketSide sets per-pod timers b._mzlT/_mzrT=0.32; decremented in updateOverlordX (dt scope); drawBossSprite overlord branch has _drawPodFlash(): frame fi=min(6,((0.32-t)/0.32*7)|0), anchored at ovMount(+/-48/46,41) with ignition ON the pod, plume blasting down the exit line, fs=40, drawn inside BOTH pivot and non-pivot paths (rotates with the body when banked). VERIFIED: flash px at BOTH pod coords (isolated snap L/R present).
2) TORPEDO SIZE: draw s=56 -> 46 (fallback 44 -> 38). Verified 27x79 real px (was ~112 tall).
3) VENOM: glow REMOVED (no shadowColor/shadowBlur anywhere in the venomx draw). Growth CAPPED at venom_0_7 (the crossing X-helix) so the odd solid-beam frames never show. At _age>=0.34 the lance SPLITS: spawns two _child venomx lasers (vx +/-3.2, vy -10.4, dmg ceil(0.6*parent) each, pierce, _hs copied so already-hit targets stay hit), parent dies with a small green explode. Children draw venom_0_4 rotated along their travel line (atan2), size 24+lv*3, straight flight, side-cull at PLAY edges. Rival-mode updater handles _child too. VERIFIED: split produces exactly 2 lasers diverging (clusters at x~448 / x~512 pairs), harness 3-drone column still destroyed (children finish flanks). Harness green (0 errors).
Clips re-rendered: venom_helix_lance.mp4 (wide 5-drone V formations — splits catch the flanks), overlord_boss_fight.mp4 (pod flashes on rocket fire + smaller torpedoes).

---
## DROP 2026-07-17p — venom horizontal row, L2 spread white-box fix, weapon-level system overhaul

Mike: (1) lasers should double into a HORIZONTAL ROW not angled splits; (2) L2 spread = white boxes; (3) MAJOR bug: every weapon starts at level 1 — should start at BASIC MG (pilot stat-card fire rate), first MG powerup = rapid L1, then L2; first-ever pickup of spread/laser/etc = L1 not L2.

1) VENOM HORIZONTAL ROW: split (at parent _age>=0.34) now spawns a ROW of rowN=4+min(4,lv) parallel lasers (5-8), all vx:0 vy:-10.4 (straight up, NOT angled), evenly spaced gap=18px centered on the parent, ph staggered per-column. Verified: 5 children x=202..274, all vx=0. (was diverging vx=+/-3.2.)

2) L2 SPREAD WHITE BOXES: root cause = row 1 (spread level 2) was mis-sliced — spr_1_0/2/3/4 were degenerate fragments (3-6px) and spr_1_1 wasn't even registered. The garbage frames fell through to the primitive white-rect fallback = white boxes. FIX: /tmp/reslice_spread.py re-slices ALL 25 frames from src/fx_masters/spreadfirefx.png (86x177, 5 rows x 5 cols, magenta-keyed, sliver-merge + 1px pad) -> assets/fx/spread/spr_R_C.png, all re-registered. Verified all 5 rows now 40-170px/frame consistent; L2 render 1200+ colored px/frame, ~0 white boxes. (manifest.js hand-maintained — these keys are in it now.)

3) WEAPON-LEVEL SYSTEM (major): wlevels now init to [0,0,0,0,0,0] + wlevel=0 at both reset sites (was [1,1,1,1,1,1]). 0 = basic. Pickup logic: _cur=(wlevels[wt]|0); wlevels[wt]=clamp(_cur+1,1,5) — so first acquire (0->1), then increments. Respawn restore uses |0 not ||1. New _weaponCadence(): basic MG (weapon 0 & wlevels[0]===0) returns 0.22 (slower than L1 rapid 0.085); else the per-weapon table. assemble.py patch #5 updated to target `else cd = _weaponCadence();` and keep the *(1-(PILOTMOD.fire)) pilot-fire multiplier at BOTH cadence sites. So basic MG cadence per pilot: axel 0.211, decker 0.172, juggernaut 0.209, falva 0.185, maverick 0.194 s/shot (faster pilots snappier). MG pShoot at L0 fires ONE basic bullet (spread=max(1,lv)); L1+ widens. Venom lance dmg floored at L1 (_vlv=max(1,lv)) so the special isn't weakened by the L0 basic-MG state. Progression verified: MG 0->1(rapid)->2; SPREAD/LASER/ICE first pickup=1, second=2.

HARNESS: section 30 extended — horizontal-row split (all vx=0, vy<0), basic MG=L0, first MG=1, first SPREAD=1, spread L1 cadence, basic MG slower than rapid, all 25 spread frames load. All green.
Clip: venom_horizontal_row.mp4. Stills: spread_l2_fixed.jpg, venom_row_frame.jpg.

---
## DROP 2026-07-17q — venom 2-laser pair, spread spec recolor (transposed sheet!), purple purge, SourceFiles reorg

Mike: row should be exactly TWO of his helix lasers; spread colors wrong/purple; total asset reorg pass.
1) VENOM: split now spawns exactly 2 parallel lasers (gap 20, vx:0 vy:-10.4, dmg 0.6x each, pierce, _hs copied). Harness updated (ch.length===2). Verified 140 demo frames show side-by-side pairs.
2) SPREAD ROOT CAUSE: spreadfirefx.png is TRANSPOSED — COLUMNS are the color variants, ROWS are animation frames. Old slicer treated rows as levels -> the flicker cycled COLORS (read as purple chaos). reslice_spread.py REWRITTEN: grid COLS x[(4,16),(21,32),(37,48),(54,64),(70,80)] ROWS y[(5,27),(36,60),(69,94),(104,127),(133,160)]; magenta chroma -> transparent, purple-blend fringe adjacent to art -> BLACK edging; column auto-map (detected green=c2 blue=c3 red=c4 white=c0, c1 spare); Mike's spec: L1=red col hue-remapped to ORANGE (target_hue .075, white cores >0.78 preserved), L2=blue col, L3=green col, L4=white col desat x0.12, L5=red col. Verified sprite-level (all rows dominant=spec, purple<=7px) AND in-game peaks (orange 646 / blue 4479 / green 2355 / white 3463 / red 2667 strict px). montage: spread_spec_colors.jpg.
3) GLOBAL PURPLE PURGE: purge_purple_halos.py — scans assets/{fx,enemies,bosses_new,items,ships,ui}: pure chroma -> transparent; magenta-blend fringe ADJACENT TO TRANSPARENCY -> black edge. Ran: 2316 pngs, 694 cleaned, 7,263,432 px. Legit purple art intact (bz6 15% purple, iproj_7 36%). Filter requires magenta-lean + transparency adjacency so interior purple art survives.
4) SOURCEFILES REORG (reorg_sources.py): NEW /SourceFiles at project root (SHIPS IN THE ZIP), 1313 files / 119MB: enemies/ (ship masters + 4-color packs + boss sheets renamed boss_*), players/ (falva/lizzie ships, cards, portraits, avatars), fxs/ (all fx_masters renamed descriptively + megapack 09-vfx frame sets) with PER-CHARACTER folders (maverick/venom_helix_growth, yuri/chain_lightning, lizzie/bombs, axel/aegis_shield_orbs, falva/pink fx; empty pilots get README), items_powerups/ (powerup boxes, shields, stat bars), levels_stages/ (stage5/6 sheets, clouds, doors + megapack 06-stages flattened), ui_menu/ (hud icons + stagecards + megapack 10-cards-and-fonts flattened). No subfolders except fxs/<pilot>.
5) PRUNE: rejected slices bmgun_*/bhom_*/phom_*/emslart_* deleted (zero code refs confirmed) + assets/fx/_icon4_orig; manifest 2349 -> 2331 keys.
Scripts in _BUILD_SOURCE: reslice_spread.py (rewritten), purge_purple_halos.py, reorg_sources.py. Harness green (0 errors).
Clips: venom_two_lasers.mp4, spread_5levels.mp4.

---
## DROP 2026-07-17r — FABLE-5 WEAPONS PASS: all player weaponry upgraded with real master art

Mike: "go fable 5 mode and upgrade ALL weaponry." Same treatment the spread got — real masters, level palette (L1 orange / L2 blue / L3 green / L4 white-gray / L5 red), shading preserved (no tint-flattening), zero purple.
NEW GENERATOR: _BUILD_SOURCE/gen_weapons.py -> assets/fx/weapons/ (44 sprites) + manifest:
1) MG MUZZLE FLASHES: machinefx.png rows 0-4 (red/blue/gold/green/white — same rows as the mfx_mg bullets), rightmost big column sliced as mgmuz_0..4. ORIENTATION: bright core at RIGHT edge = attachment; draw rotate(+PI/2) puts attachment on the gun, flame UP. Wired: pShoot w0 sets player._mgMuzT=0.07/_mgMuzLv; timer decremented at both fireCd sites; drawn in _drawPlayerCore at (x,y-16), size 15+lv*2, alpha fade, row map {1:2,2:1,3:3,4:4,5:0}. VERIFIED flame above nose 1698px vs 278 below.
2) LASER REBUILT: laserbeam.png = 7-frame blue growth (11x14 bolt -> 31x124 full beam). Recolored per level (hue-remap, white cores >0.78 kept; L4 desat 0.12) -> lzr_<1-5>_<0-6>. L2 violet-band clamp (h 0.68-0.92 -> pure blue 0.60): purple 150 -> 0 px. L1/L5 brightness+sat boost (v x1.30/1.38) for punch. Beam draw REPLACED tint path: lzr_<lv>_6 stretched column (soft outer 1.9x @0.5 + core @0.97) + animated origin flare (lzr_<lv>_0..2 @ ~16fps) + white-hot center line; legacy tint path kept as fallback. VERIFIED on screen: L1 11k orange / L2 84k blue 0 purple / L3 30k green / L4 50k white / L5 267k red-family px.
3) ICE SHARDS: real icicles from ice_snow_fx_pack.png (vertical, TIP AT TOP) -> iceshard_0..3; 'shard' draw rotates ang+PI/2 (tip leads), size 15+lv, variant by angle hash. Replaced the ice_shard/rect fallbacks as primary. VERIFIED 8-ring spray = 6+ icy sprite clusters; tour peak 171 clusters.
4) FIREWALL: flame height now level-scaled dh=24+lv*5 (L1 29 -> L5 49). VERIFIED 43px vs 75px on screen.
5) MISSILES: already real pilot-colored art + tracking — untouched.
HARNESS section 31: mgmuz x5, lzr 5x7, iceshard x4 load; MG fire sets flash; beam/shard draw wired; firewall scaling. ALL GREEN (0 errors).
Clips: weapons_tour_fable5.mp4 (MG L1-5, LASER L1-5, ICE, FIREWALL L2/L5, MISSILES), laser_levels.mp4 (post-brighten). NOTE: tour clip predates the L1/L5 laser brighten; laser_levels.mp4 is current.

---
## DROP 2026-07-17s — PLAYTEST FIX BATCH: falva pink restoration (purge damage owned + fixed), MG buff, laser de-box, round particles, tank gating, password flow

MY FAULT, OWNED: the purple purge (DROP q) ATE PINK ART — pink is magenta-family (r+b high, g mid), the g<130 fringe filter treated falva's pink edges as chroma halo -> blacked her ship rim, charge balls, laser, retina. "Turns into yuri" = falva/lizzie had NO pv/br bank frames, so banking fell through to the procedural RED-wing fallback ship.

RESTORE (all from pristine sources — src/ + /tmp/build/falvanlizzie staging were never touched by the purge):
- extract_fl_ships.py re-run: ship_falva/lizzie base+t/l/r pristine (black 1686->784 = source-normal outlines, pink 670->3212)
- extract_fl_fx.py re-run: fball/fchg/forb/fburst/sp_*/specialboxes/msl pristine (fball_0 black 2739->49)
- extract_falvalaser.py re-run (RUN FROM _BUILD_SOURCE — SHEET/OUT are relative): fllaser 0 black / 1885 pink
- extract_fl_reticles.py re-run (source /tmp/build/_DROP/ship_pack/.../Pink_Gold_Reticles_Crosshairs_Atlas.png): retA/retB_falva 2868-3329 pink
- purge_purple_halos.py FILTER FIXED: g<130 -> g<45 (chroma bg g~13; pink g 50-140 protected) + warning doc. NEVER widen it.
- NEW gen_bank_frames.py: falva + lizzie pv0-4 + br0-7 (26 frames) generated as affine transforms of their REAL base/_l/_r art (squash+rotate, br2/6 edge-on 0.34 width slightly darkened, inverted frames = base flipped). Registered. VERIFIED: falva banks in HER pink art at level/soft/hard/full-twist (509/514/400/56 pink px, red-fallback 0 in all poses); 300-frame gameplay clip: 0 frames without her ship.

GAMEPLAY FIXES:
1) MG SPEED: basic cadence 0.22 -> 0.14 ("players need a fighting chance"); L1 rapid still 0.085.
2) MG ROW: gun spacing 7 -> 11px — multi-gun fire reads as a clean horizontal row (was overlapping into one column, the "stacked shots" screenshot).
3) LASER DE-BOX: all 35 lzr frames soft-edged at the file level (side 22% + top 14% alpha fade); wide 1.9x slab REMOVED; white fillRect center REMOVED; beam = soft 1.44x pass @0.34 + core @0.97, shadowBlur 6. ORIGIN RING UNDER THE SHIP: 4 small growth-bolt frames composited radially at the beam base, rotating, drawn in drawBullets (before drawPlayer -> sits beneath the hull). Verified ring 732px at hull base.
4) ICE/ALL BOXY FX: root cause = the generic particle draw was fillRect SQUARES; ice bursts made pale-blue square clouds (the slab in Mike's shot). Plain particles now ctx.arc CIRCLES; debris 'chunk' rects intentionally kept.
5) FIREWALL "saw nothing": weapon verified end-to-end in-game (pickup wtype 4 -> 7 walls alive -> 5906 flame px) — it was RNG: crates rolled (rand*6). NEW fair-deal bag: run._wbag shuffled [0..5], popped per crate, refilled when empty -> 6 crates ALWAYS show all 6 weapons. Firewall flames also level-scale (dh=24+lv*5).
6) RED TANKS: culprit = tk0_inta_* directional hull (red-frac 0.22) in JUNGLE_TANKS. Now JUNGLE_TANKS=['tk4','tk1'] (L1 greens only), STAGE4_TANKS=['tk0','tk2','tk3','tk4'], _jungleTank() stage-aware. Verified picks both stages.
7) PASSWORD FLOW: accept no longer startRun()s directly. NEW global PENDING_STAGE; password accept -> PENDING_STAGE=stage; setState(GS.PILOT) -> CHARACTER SELECT -> pilot confirm startRun(PENDING_STAGE) -> reset to 1. pickDiff resets PENDING_STAGE=1. Verified DAM5 -> pilot state -> run.stage 3.

HARNESS section 32 (all green, 0 errors): falva/lizzie pv+br load, retina+fllaser registered, MG 0.14 + 11px spacing, tk0 gating both ways, password->PILOT->stage, crate bag 012345.
Clips: falva_restored.mp4 (banks/twists in her own pink art). Stills: falva_frame.jpg, laser_debox.jpg.

---
## DROP 2026-07-17t — NEW STAGE CARDS WIRED (all 8) + right-roll fix + cole frames + universal thrusters

1) STAGE CARDS (stagecards_0716 v4.1 pack): 8 Final_Embedded ALPHA 800x480 cards (titles baked in) copied to assets/ui/stagecards/scard_1..8 + registered. drawIntro PREFERS scard_<stage> over the old atlas card frame (drop-in/THUD/shake animation kept intact); falls back atlas -> legacy banner. NET NEW: stages 6-8 (Heavy Turbulence, Not Another Sewer Level, Furious Death) get a REAL card intro for the first time (previously procedural banner). Verified stage 1 + 6 render 260k+ card px via scard.
   NOTE: the pack's Fonts/ (8 themed 13x4 glyph atlases) + Blow_By_VFX + Card_Base/Title_Layer variants are staged but NOT yet wired — candidates for a later pass.
2) RIGHT ROLL FIX: rollFrameKey() always played br 0->7 (the LEFTWARD rotation) regardless of roll dir — right rolls looked like left twists ("not twist turning to the right"). Now dir>0 maps fi=(8-f)%8 -> sequence 0,7,6,5,4,3,2,1 (proper rightward through br6). Verified both sequences frame-by-frame.
3) COLE: had ZERO pv/br frames -> banking fell to the red procedural fallback ship ("still yuri's ship"). gen_bank_frames.py extended to cole (13 frames from his real base/_l/_r) + registered. His base art was always his own (differs from yuri's file).
4) ANIMATED THRUSTERS FOR ALL: level pose now alternates ship_<pk>_pv2 with the pilot's REAL ship_<pk>_t thrust frame at ~11Hz (the baked engine-flame animation lizzie showed). Every pilot has _t. MG muzzle flash (mgmuz) was already pilot-agnostic.
HARNESS section 33: scard 1-8 load, intro wired, right-roll sequence, cole frames, _t cycle. ALL GREEN.
Clips: rolls_both_ways.mp4 (thrusters + left roll + FIXED right roll). Stills: intro_stage1.jpg, intro_stage6.jpg, stagecards_all8.jpg.

---
## DROP 2026-07-17u — CORRECTED LEVEL-1 WORLD MAPS wired (intact + destroyed dam), camera pan, seam fix

Mike supplied corrected L1 masters: level01-giant-map-intact-800x3616.png + level01-giant-map-destroyed-800x3616.png (magenta #FF00FF keyed, 800-wide WORLD sheets, 3616 tall).
- Archived to src/incoming_l1maps_0718/ + SourceFiles/levels_stages/ (level1_world_map_intact/destroyed_800x3616.png).
- Magenta keyed -> transparent, deployed as assets/levels/mapJungle.png (intact, 159307px keyed) + mapJungleDam.png (destroyed, 221427px keyed). Note "mapJungleDam" = the DESTROYED/blown-open state that swaps in when the copter boss dies (damBroken=true).
- UNIFIED the mask source: jungle800_master manifest key repointed from the old separate jungle800_master.png to assets/levels/mapJungle.png, so the tank drivability mask + the drawn background are the SAME corrected art (no more drift). Landmask + tankmask both rebuild from it (landmask 800x3616; tankmask 46% drivable of 100x452 grid — valid, was the source of prior seam/edge drift).
- drawStageMap REWRITE: (1) scroll speed now range/curStage.length so the dam always arrives exactly at boss time regardless of the taller corrected sheet (verified reaches top at t=62s = stage length); (2) the 800-wide map now PANS with the camera — ctx.drawImage source-x = clamp(camX) — where the old 480 map drew a static window (verified 75% of px differ camX0 vs camX320, terrain span shifts under player weave); (3) the transparent reservoir behind the dam shows the base animated water layer straight through (matches Mike's reference art) — REMOVED the redundant separate drawGateWaterfall on-top overlay that was double-drawing/mis-panning (was the seam). DAM SEAM ISSUE (long-standing open item) = CLOSED.
HARNESS section 34 (all green): maps registered, dam-break swap wired, mask master unified, camera-pan draw, length-derived scroll. (Pixel dims 800x3616 + mask validity verified via node-canvas RENDER, not the harness — harness uses a 64x64 stub Img that can't decode real pixels.)
Clip: level1_corrected_map.mp4 (scroll from dam down through the valley, camera panning as the ship weaves). Stills: l1_dam_states.jpg, l1_campan.jpg, l1_top_frame.jpg.

---
## DROP 2026-07-17v — right-side bullets never appeared (world-width cull bug) + seamless square water tiles

1) RIGHT-SIDE BULLETS: on stage 1 (800-wide world) ALL bullets past screen-x ~520 were culled instantly, so firing anywhere on the right half of the world produced nothing. Root cause = three culls used VW (480)/PLAY.w instead of worldWidth():
   - gamecode ~3616 generic player-bullet cull: `b.x>VW+40` -> `b.x>worldWidth()+40` (_bw)
   - ~3449 venomx cull: `b.x>PLAY.x+PLAY.w+30` -> `b.x>worldWidth()+30` (_vw)
   - ~3658 missile cull + ~7192 enemy-bullet cull: same VW->worldWidth (_mw,_ew) so right-side missiles/enemy fire also survive.
   Verified: MG bullets alive after 8 frames at world-x 80/400/720 (was 0 at 720); live clip 17 bullets alive while ship on far right. (Same WORLD_W-vs-camera class of bug as the earlier tank clamp/cull.)
2) SEAMLESS WATER: old water frames were 480x57 full-width STRIPS; drawAnimTerrain rounded each tile independently -> sub-pixel gaps/seams (Mike's screenshot). Mike's reference (1784467014140) is a seamless ~175x176 SQUARE tile (period 175, vertically tileable). Extracted 4 anim frames (vertical-scroll wrapped) -> assets/fx/water_tile_0..3.png; BOF.waterFrames repointed. drawAnimTerrain rewritten: square tiles at NATIVE aspect (tileW=fr.naturalWidth*ts), integer tile size + integer step, +1px w/h overdraw to close any hairline. Verified 0 gap px (magenta bg fully covered), 0 vertical + 0 horizontal seam candidates. Reference saved to SourceFiles/fxs/water_seamless_tile_reference.png.
HARNESS section 35 (green): bullets survive firing across the full 800 world, cull uses worldWidth, 4 seamless tiles, +1px overdraw. 
Clip: rightfire_water_fixed.mp4 (ship sweeps full world firing; seamless water at dam). Still: water_tiled.jpg.

---
## DROP 2026-07-17w — water tiling gaps ACTUALLY fixed (mirror-tile, seamless by construction)

Prior drop (v) fixed the tiler math but the TILE ITSELF wasn't vertically seamless — Mike's reference (1784467014140) is 3 side-by-side copies with real edge banding, NOT a torus texture, so np.roll anim frames + feather-blends still left a ~176px-boundary dark seam (6 gap rows in-game at the dam).
FIX: gen_water_tiles.py (in _BUILD_SOURCE) builds a 4-WAY MIRROR BLOCK from the 175x176 source tile: full = [T, flipH(T); flipV(T), flipHV(T)] = 350x352. Every shared edge is a mirror of itself -> edge-match v0.0 h0.0 (mathematically zero seams). 4 shimmer frames via a tile-periodic luminance wave (2 cycles over tile height -> stays seamless). BOF.waterFrames repointed to water_tile_0..3.png.
VERIFIED: isolated strip 0 magenta-gap px + 0 sharp row-seams at 3 scroll offsets; in-game dam render 0 dark gap rows (was 6); definitive stack-3x boundary test = gradient 0.7 at the tile seam vs 2.9 interior median (seam MORE continuous than the ripples = invisible).
drawAnimTerrain unchanged from v (square native-aspect tiles, integer step, +1px overdraw) — the tiler was fine once the tile became a true torus.
HARNESS section 35 water assertion updated (frames repointed to mirror tiles; dims 350x352 + edge-match 0.0 verified in render, not harness stub).
Clip: water_seamless.mp4 (scrolling reservoir at the dam, ship firing on the right). Still: water_final.jpg, ingame_water2.jpg. Generator: _BUILD_SOURCE/gen_water_tiles.py.

---
## DROP 2026-07-17x — water tiling: use Mike's ACTUAL texture tiled flat (mirror was wrong)

DROP w's mirror-block was WRONG: the 4-way mirror created a symmetric pattern with a low-detail flat line down the mirror axis — that was the "~32px area where no water lives" Mike flagged (image 1). Mirror != tiling.
FIX: use Mike's actual water texture (upload 1784468161170, 341x248) tiled FLAT like a floor. gen_water_tiles.py rewritten: offset-roll by half (moves the discontinuity to the tile CENTER) then feather-heal that single cross-seam (fb=28) — keeps the natural water look, NO mirror symmetry, NO flat axis band. Source saved to SourceFiles/fxs/water_texture_source.png.
VERIFIED: 0 flat/dead columns in the tile AND across a 3x3 tiled grid; boundary gradients (v1.2 h0.0) BELOW interior median (1.5) = seams invisible; in-game dam render 960 water columns / 0 dead. Texture std 57 = full water detail retained.
drawAnimTerrain unchanged. HARNESS 35 note updated.
Clip: water_flat_tiled.mp4. Still: water_3x3.jpg (3x3 tiled proof).

---
## DROP 2026-07-17y — water drawn at NATIVE 1:1 (no stretch)

Mike: "dont stretch the water." drawAnimTerrain was drawing each tile at tileW+1/th+1 (1px overdraw) and deriving th from a width-ratio — both scaled/distorted the texture. FIX: draw at EXACT native pixel size — tileW=naturalWidth*ts, th=naturalHeight*ts (ts defaults 1), ctx.drawImage(fr,x,y,tileW,th) with NO overdraw. The seamless tile (DROP x) carries its own edges so overdraw is unnecessary. Verified: on-screen tile vs source pixel-diff 1.0 (pixel-perfect 1:1, was stretched), 0 magenta gaps, in-game dam 960 water cols / 0 dead / 0 gaps. HARNESS 35 assertion updated (native-draw check replaces the +1px-overdraw check).
Clip/still: water_native.jpg, ingame_native.jpg.

---
## DROP 2026-07-17z — REAL pilot barrel rolls (cole/falva/lizzie/freezer) + flip-fixed hard-R (axel/decker/maverick)

Mike: "decker,maverick,juggernaut,yuri = useable. axel/decker/maverick: flip hard-L to make hard-R. Pull the barrel roll zip for cole,falva,lizzie,freezer's real rolls."

Source: src/incoming_drop_0712/ship_production_pack/Player_Ships/*/*BarrelRoll*. Two families:
- cole + freezer: 2-row MAGENTA pivot+barrel atlases (Cole_Force_1, Freezer_Yeti). cole's barrel row had touching frames (blob detect saw 5) -> fixed 8-col grid fallback.
- falva + lizzie: single-row CYAN 8F strips (Falva_BarrelRoll_8F_Cyan, Lizzie_BarrelRoll_8F_Cyan_Corrected) -> fixed 8-col grid (scrub merges thin edge-on frames). Keep their generated pv, replace br with REAL frames.

NEW permanent script: _BUILD_SOURCE/extract_pilot_rolls.py (extract_magenta_2row / extract_cyan_8f / fix_static_twist / flip-fix). Registered all 32 real br frames.

STATIC TWIST correctness: the engine uses br2 (left edge-on) + br6 (right edge-on) for the hold-bank pose, and plays br0-7 for the roll animation. The authored rolls don't all put edge-on at 2&6 (their phase varies; some have the edge-on pair only 2 apart, not 4 — different roll structure than yuri's). So fix_static_twist() finds each pilot's narrowest (edge-on) frame and sets br2=that, br6=flip(br2) — guarantees the static twist reads correctly BOTH ways regardless of authored phase. The full 8-frame roll still animates through the authored frames.

FLIP FIX: axel/decker/maverick br6 := horizontal flip of br2 (Mike said their hard-R was wrong). Verified mirror-diff 0.00.

VERIFIED in-game (all 7 affected pilots): static twist L!=R with clean mirror (LR-diff 3.8-13.3, mirror-diff 1.0-1.9 = distinct-but-mirrored = correct). juggernaut+yuri left as-is per Mike (useable).
HARNESS section 36 (green): 4 pilots have 8 real br frames; 7 pilots have br2+br6; roll dir mapping intact.
Clip: new_pilot_rolls.mp4 (cole/falva/lizzie/freezer roll both directions in-game).

---
## DROP 2026-07-19a — cleaner roll sheets received (4 pilots) + Lizzie; FX sheets pending

Mike re-dropped cleaner roll sheets (GPT-5.6 authored, "same as before just cleaner", confirmed SINGLE-DIRECTION 8F rolls not full-symmetric). Archived to src/incoming_rolls_0719_{cole,falva,freezer,lizzie}.png.

STATUS: Game left in VERIFIED-GOOD state on the drop-z frames (all 4 new pilots edge-on twist both ways, br6=flip(br2) diff 0.00, harness green). 

ATTEMPTED re-extract from cleaner sheets but the fixed 8-grid cut frame boundaries slightly wrong on the DENSER sheets (cole/lizzie/freezer showed weak edge-on differentiation, ratio >0.84). Falva sliced clean (0.58). REVERTED to drop-z frames via extract_pilot_rolls.py (idempotent) rather than ship a half-good slice. 
-> NEXT CHAT: re-slice cole/lizzie/freezer from the cleaner sheets with per-sheet tuned frame boundaries (blob-detect with adaptive gap, or hand-set column splits) to get the higher-quality art in. Falva's cleaner slice is already good and could be committed. Sheets are archived and ready.

100-IMAGE LIMIT hit this chat — continuing in a new one.

### AWAITING RE-UPLOAD (didn't sync / limit): FX sheets for the FX-overhaul phase
- Muzzle/spark FX grid (gold, 6x4) = f12e39cf ON DISK -> src, ready for FX pass
- Spin/swirl orb FX (img 6) — NOT on disk
- Missile/projectile FX (img 7) — NOT on disk  
- Smoke/vapor trails (img 8) — NOT on disk (compare vs existing smoke_vapor_pack.png)
- 2nd purple sheet ebb2e38a ON DISK — verify freezer-variant vs alt when resumed
