# PASSOVER 0910A — DEBUG MODE, THE RECORDER, AND BOSS MODE

Mike, 0910: *"we need a Debug mode. upon entering the main menu, allow me to freely input the
following combination to unlock the debug mode button - Up Up Down Down A B C ... select each mini
boss fight and boss fight, when selected, jumps me to the direct fight. when fight ends/boss dies,
do the explosion phase fly us off, and then fade us back to the debug menu ... a recorder option by
pressing R while fighting a boss ... Additionally, make an expansive program called "Boss Mode"."*

## What shipped

**Debug mode** (`assets/game.js`, the DEBUG MODE block before `backButton`)
- Title screen: **UP UP DOWN DOWN A B C** on the keyboard → `DEBUG` button, top-right (F2 opens it
  too). Session-only, like the settings since 0909. `?debug=1` unlocks it for a harness.
- The menu is 9 stages × {MINI, BOSS} = 18 fights, read off `STAGES[].boss` and `SUBBOSS[].kind`
  with their authored names. Pilot picker on the top row. Enter / click launches.
- A fight is the REAL stage: `startRun → beginStage` builds it as play does, then the clock is
  moved and the game's OWN warning (`warnT`/`warnKind`) spawns the unit — the alarm, the music
  switch and the arena hold all happen where they always happen. It is `coleSceneApply`'s route
  (COLE1..9) minus the HP sliver, with the wave script, the arsenal mini and the crates spent.
- The exit is the ordinary one: the boss cook-off (5.8s), the FLYOVER fly-off, then instead of
  STAGECLEAR a fade to the debug menu. `setState` routes every post-fight state there while a debug
  fight is live (STAGECLEAR, GAMEOVER, CONTINUE, OUTBOUND, the stage-7 warp, the stage-9 rift
  fallback, RIVAL, TITLE …) — centralised for the same reason `campSuspend` is. A miniboss has no
  stage exit of its own, so once its death reel has run (1.9s) `debugLoopTick` raises
  `bossDefeated` with `stageEnding` already at 3.4 of 5.8 — the "no boss authored" route the
  stage-6 placeholder used. Same fly-off, ~2.4s after the kill.
- **R** records the play canvas (`captureStream` + `MediaRecorder`, webm, 60fps, 8 Mbps) and saves
  `BOF_s<n>_<role>_<kind>_<stamp>.webm` to Downloads on the second press or when the fight ends.
  F3 arms auto-record for every fight; P replays the last clip in a tab. The REC clock is painted
  into the recording on purpose — it is the timestamp we will talk to each other about. **Video
  only:** the music plays through HTMLAudio elements that are not all routed through one
  AudioContext, so there is no single node to tap.
- F4 arms the editor's saved overrides for the session (see below). E opens the editor.

**Boss Mode** (`bossmode.html`, `assets/bossmode/`)
- The chrome is the whole of `CF_BossModeAssets-Vol.1`: logo, boot plate, the window frame as a
  CSS 9-slice, both button sets with their hover/pressed states, the 20 icons, the 16 cursors
  (downscaled to 32px with hotspots — the pack's 252px cursors are not usable as CSS cursors), the
  three bitmap faces for panel titles, the loading bar for boot and the HP telemetry.
- The engine is the real game in an iframe: `index.html?bossmode=1` boots itself (the host presses
  START for itself) into `GS.BMHOST`, a black waiting state, and exposes `window.BOSSMODE`.
- BOSS LIST → INSPECTOR (identity, art STATES with HP fractions, size/placement, HP, weapons,
  PATTERNS as phases with the anchors each pattern fires from, derived PHASES table, ANCHORS &
  orientation, movement, HITBOXES, PARTS, notes) → APPLY / UNDO / CANCEL.
- PLATE tab: the plate at zoom with the hull box, the anchors as draggable crosshairs (shift snaps
  to 0.05), missing-anchor warnings per pattern, the facing arrow, extra hitboxes and parts.
- GRAPHICS tab: every registered key belonging to the kind (plate stems + `bfx_<proj>` + the
  per-kind fx families), thumbnails decoded through the host's XART; USE AS PLATE / DAMAGED /
  CRITICAL.
- STAGE tab: PLAY TEST runs the fight with the edits laid on; telemetry bar (HP as a pack fill,
  phase, step, cooldown, position, bullets, REC); anchors overlaid on the live boss through the
  snapshot's camera (`camX`, `viewZoom`); REC / INVULN / SPEED / PAUSE / KILL / SET HP.
- CLIPS tab: every recording plays back inside the editor.
- FILE: NEW BOSS (a variant document on a base row), OPEN, SAVE (into the game's override store),
  SAVE AS / EXPORT (`bossmode_<kind>.json`, schema `bof-bossmode/1`), IMPORT (a doc or an
  overrides bundle), EXPORT ALL OVERRIDES.

## What is live and what is data — stated in the UI, not hidden

`name`, the three art states, `w/h/ty/drawW/drawH`, `hp/hpMul`, `move`, `anchors → mounts`,
`pat/cd/proj`, `pats` are laid onto `SHIPBOSS[kind]` on APPLY and the running boss takes them.
Extra hitboxes, parts, orientation, per-state HP fractions and notes are saved in the .json and
drawn in the editor; the shipping engine does not read them. Each such field says so in its hint,
because a boss is ONE plate with damage STATES (CLAUDE.md, Mike's no-splits rule) and pretending
the engine consumes sub-parts would be the 0814e "components that are empty" trap from the other
side.

⚠ **A normal boot never applies overrides.** Mike's 0909 rule — blank game state on start — covers
this. The host applies them (it is the editor's engine); the game applies them only while the
debug menu's F4 toggle is on. A boss tuned last week must not quietly show up in a campaign run.

## Traps, measured

- **`anyTap()` walks `Input.keys`, so an injected tap for a key that has never been physically
  pressed is invisible to it.** The host's first boot gate uses `anyTap()`; `Input.injectTap
  ('enter')` alone did nothing and the host sat on BOOT forever (probe: `state=boot`). The key has
  to exist in `keys` first. And there is no `frameCount` global — a cadence keyed on it threw
  every frame inside the switchboard's try/catch, silently.
- **`hp=1` + `hitBoss()` cannot kill a boss with a barrier.** The Magma Ward absorbs the hit in
  `magmaWardBarrierDamage` before the hull sees it; the quad-laser and the Blacksteel have their
  own absorbers. `BOSSMODE.kill()` takes the death BRANCH (`bossDie()`; the sub-boss dead block)
  instead. 0814c recorded the modular half of this; the ship half is the same shape.
- **`Input.menuLeft()` consumes its tap**, so `if(menuLeft()||menuRight()){ d=menuLeft()?-1:1 }`
  always answers +1. Read each once.
- **The browser pane gives the iframe no rAF between captures** (memory: `browser-pane-raf-
  suspension`), so the host never leaves BOOT there — 27 frames in 25 seconds. The editor was
  verified in real Chromium by `probe_bossmode_editor.py`; the pane was used only to look at
  the chrome after driving the host to `bmhost` by hand.
- **`XART.raw()` is the object the editor draws from; `XART.get()` is a blank until decoded.**
  Thumbnails poll `rdy` and retry, per the standing first-call rule.

## Verified

- `_BUILD_SOURCE/probe_debugmode.py` — real Chromium, real keyboard events: **31 ok / 0 fail.**
  No button before the code; a wrong sequence stays locked; the code unlocks; F2 opens the menu;
  Enter launches the stage-1 boss through the game's own warning with 0 wave enemies; R starts and
  stops a 205 KB webm; kill → cook-off → FLYOVER → DEBUGFADE → DEBUG with the fight cleaned up;
  the stage-2 mini does the same through its own death reel; dying returns to the menu;
  BACKSPACE returns to the title; the host boots itself to `bmhost`, `start(4,'boss','yuri')`
  spawns the Storm Sovereign, a live override renames and resizes it, reset restores it, stop
  returns to `bmhost`, and a reset leaves nothing saved.
- `_BUILD_SOURCE/probe_bossmode_editor.py` — the editor page: **19 ok / 0 fail.** Boot clears,
  28 list rows (18 fights + 10 unslotted rows), inspector from SHIPBOSS, anchors L/C/R, four pats
  as phases, plate ink 64,034 px, APPLY writes the override and the live row and localStorage,
  PLAY TEST fights the edited row (`MAGMA WARD TEST`, hp 2579), telemetry reads it, 3,795 px of
  anchor overlay on the live stage, STOP returns the host, EXPORT/CANCEL/IMPORT round-trip, 97
  graphics keys, the JSON pane.
- Suite: section 279 added (47 assertions, behavioural for the jump, the kill, both exits, the
  overrides, the recorder's safe failure). One existing assertion repointed: MENU_BACK has eight
  entries now, not seven — the debug menu is backable. Counts are in the report.

## Open

- The recorder captures the play canvas only: no HUD strip (a separate DOM canvas) and no audio.
  Compositing `#hud` into the stream needs an offscreen canvas driven each frame; audio needs
  every music element routed through one `AudioContext` graph. Both are Mike's call on whether
  the clip needs them.
- Fights built in code rather than on `SHIPBOSS` (Jungle Overlord-X, Chaos Harrier, Black
  Cocoon, the stage-9 pair) show as `CODE` in the list: PLAY TEST runs them, the row editor does
  not apply. Moving their stat lines onto the table is the way to make them editable.
- Extra hitboxes and parts are data; wiring them means a sub-hit zone concept in `hitBoss`, which
  is a design decision under the no-splits rule.
- Gamepad entry of the code: A on a pad is also menu-confirm, so it selects NEW GAME. Keyboard
  A/B/C are the letters; the d-pad works for UP/DOWN.

---

# 0910B — THE BOSS AND MINIBOSS GAUGES ARE THE PACK'S BARS

Mike: *"take the health bars from the boss mode assets ... 1 specific bar for minibosses, 1 specific
bar for bosses. use the different fills per levels and via palette swapping ... we do not want to
shrink it ... you tell and do so."*

**The call:** BOSS = the orange-lit `empty-highlight` frame with the hazard-stripe `fill-segmented`;
MINIBOSS = the plain silver `empty` frame with a solid fill. **The fill is clipped, never scaled** —
drawn at its frame-fitted size every frame and `ctx.clip()` cut at the fraction from the left, which
is how the pack's own loading bars are meant to drain (its README: *"fills can be scaled to the
empty frame opening and clipped to progress"*). Per-stage colour is `xartPalette` on the fill; where
a stage already IS an authored fill it is used untouched (1 green, 2 orange, 3 cyan, 8 red), the
other five are hue swaps of the orange plate (4 amber, 5 violet, 6 storm blue, 7 toxic green, 9
void magenta). The grey `fill-disabled` plate is the damage-lag ghost. The critical pulse under 25%
is a brightness flash so the stage colour survives it.

**Baked once, drawn 1:1.** `assets/game/atlas/ui_bossbar.png` (704x258) carries the two frames and
six fills at the size the HUD draws them (700px on the 2x backing), so nothing is resampled 4.6x at
runtime. Nine cells on `ui_bossbar` in the manifest; `bossBarWarm(stage)` in `beginStage` so the
first warning never sees the fallback. The 0810n drawn gauge stays as `drawHealthBarDrawn`, the
fallback for the frames before the sheet decodes — `drawHealthBarV2` still ALWAYS draws.

⚠ **THE FILL BELONGS IN THE OPENING, NOT ACROSS THE CAPS.** The pack's fill plates are 1605 wide
against a 1609 frame, and placed at the map's own offset they cover BOTH end caps — the LED and the
stripe square vanish under the bar at full health. The first render did exactly that. The opening
is x 139..1469 of 1609, measured on the plate; the vertical comes from the pack's placement (8 px
down, 60 tall, of 77) because a column scan reads the dark rails as "well".

Verified: `probe_bossbar_0910b.py` — both gauges draw on all nine stages with a ghost and a
critical pulse (contact sheet), the ART path blits the frame cell (2 blits for boss+mini, not the
drawn fallback), and the fill is blitted at ONE width at 30% and 90% (286.2 / 286.2 px — clipped,
not shrunk). Live shots: Magma Ward, Cryo Spear, Doomsday Carrier at 62%.

## 0910c — the name is off every gauge, and the fill goes in the BLACK

Mike: *"stop displaying the name of the boss entirely for ALL mini and regular bosses. Next, ensure
you dont overlay the line, but you center the fill graphic inside the black properly to fill."*

**Every HUD name label is gone** - the four boss-bar callers, both gauge bodies' miniboss label, the
miniboss fallback bar, both legacy `hbDraw` label arguments, and the `'!! NAME !!'` entrance banner
that flashed while a boss flew in. `run._lastBossName` (the debrief) and the `{BOSS_NAME}` radio
substitution stay: those are screens and dialogue, not the HUD.

⚠ **THE FRAME OPENING IS NOT THE BLACK.** 0910b fitted the fill to the opening between the cap
squares, which still ran the fill over the top and bottom RAILS. The interior is measured off each
frame's own pixels - the longest contiguous run of near-black - and the two frames differ: x
140..1468 on both, y **24..53** on the mini frame and **25..53** on the boss frame, whose lit top
rail is a row thicker. Each kind now draws its own rect. ⚠ **And take the LONGEST CONTIGUOUS run,
not min..max** - a dark strip above the rail made the mini well measure as y 2..53, i.e. the whole
frame, which is how the fill got over the rails in the first place.

## 0910d — the clip is the whole cabinet

The recorder captured `#screen` alone, so every clip dropped the score/lives/bombs strip and the
EQUIPPED box — the two surfaces that say how the fight is going. It composites all three canvases
now, in shoot.py's own layout (hud + equip on a row above the play field), so a frame of a clip and
a frame of the harness are the same picture. ⚠ **The composite runs at the END of `loop()`, after
`drawHUDStrip` has filled the strip for this frame** — composited any earlier it records the
PREVIOUS frame's HUD over this frame's play field, which is invisible until you go looking for a
number in a clip. One seed frame is painted before `captureStream`, or the clip opens on black.
Measured: 960x1152 composite against a 960x1024 screen, 31,509 lit pixels in the HUD row.
Audio is still not captured and is a bigger job — see the README.

## 0910e — SHIP DESTROYED is lettered in the stage you died on

Mike: *"remove this font, use the correct font here please for all stages."* It was drawing through
`msgText`, i.e. the DIALOGUE face — the same fault 0904af fixed on the debrief and 0904v on
GET READY / 3-2-1 / GO, still live on the banner the player sees most. It goes through
`stageText(curFontArt(), …)` now, shrink-to-fit (`stageFitH`) because the stage faces are wide and
this is fourteen characters on a 480px field. `msgText` survives only as the pre-decode fallback,
and `stageText` keeps its own BOFmil fallback, so a slow decode still costs letterforms and nothing
else. Rendered on all nine stages by killing the ship in each (`docs/proofs/`-style contact sheet):
every glyph resolves, including the S that the stage-5 CARD alphabet does not have — the borrow
chain covers it, which is the 0903 CHOO E YOUR PILOT bug not reappearing.

---

# 0911A — THE SCENE DIRECTOR AND THE SCENE EDITOR

Mike, with `CF_BossModeComplete-Vol.1`: *"a boss editor section where it's a scene editor
essentially, but with a grid/tile based system. The way it would work is I could drag my boss across
horizontally, vertically, diagonally, spin, rotate etc. Additionally, we can create zones where the
boss would go, attack zones, safe zones for the player, and a list of the in-game projectiles to key
to the boss, the flashes, the effects, etc."*

## The engine half (`assets/game.js`, "THE SCENE DIRECTOR")

A SCENE is data on the `SHIPBOSS` row (`scene`), laid on by the editor like any other override and
attached at `shipBossInit`. Positions are TILES on the scene's own cell size.

- **Tracks** — `{trigger, mode:once|loop|pingpong, speed, repeat, keys:[{x,y,rot,sx,sy,t,hold,
  ease,actions}]}`. Triggers: start / time / phase / hp-below / proximity. While a track is live the
  director OWNS the hull inside `shipBossManoeuvre` (before the stage-specific ticks); between
  tracks the engine's own manoeuvre state machine runs untouched, so a scene that only adds zones
  and a volley costs the fight nothing it had. Rotation is DEGREES interpolated raw — 0→360 is one
  full spin — and `shipBossVisualPose` adds it. That pose carries Mike's standing "bosses never bank,
  roll or flip" rule; a rot keyed in the editor is his own authoring and is applied only when keyed.
- **Zones** mean something in play: `safe` removes enemy rounds that enter it (enforce:false to
  record only); `attack` is telegraphed on the field with the pack's FOV cone / alert symbol /
  armoured badge while active, and a fire action can aim at it; `boss` fences the engine's own
  manoeuvre while no track is live. Active by time window, by phase, or by an action toggling it.
- **Actions** on keys: `fire` (shapes off the pack's own pattern sheet — stream, spread, fan,
  radial, spiral, aimed, sweep, mirrored, wall, rain, sine — with n / spread / speed / burst /
  interval / step, from any anchor, aimed straight / at the player / at a zone, with the boss's own
  muzzle or any registered flash family), `fx` (explode, any family), `flash`, `sfx`, `shake`,
  `zone` on/off. `kind:'boss'` goes through `_shipShot`, so the round IS what the fight fires.
- **In-game art**: `assets/game/atlas/ui_bossmode_fx.png` — six FOV cones (alpha-128 by authoring,
  drawn at opacity 1 per the pack README), nine alert symbols, three armoured badges. F6 in a debug
  fight toggles the design overlay (path + zone rects) on the real field.
- `BOSSMODE.scene.{attach, detach, state, action, overlay, fx, kinds, shapes}`; the snapshot carries
  the scene state, the world width and the camera.

## The editor half (`assets/bossmode/scene.js`, the SCENE tab)

The field at the stage's size on a tile grid (16–64px cells, snap, shift = free). Tools from the
pack's point markers and guides: SELECT / DRAG, WAYPOINT, BOSS / ATTACK / SAFE ZONE, DELETE. The
boss plate drawn at the selected key's pose with a yellow **R** rotation handle (15° steps), its
anchors on the hull as muzzle markers, the path with direction ticks, waypoint markers in their
normal / hover / selected states. PATH presets (straight, diagonal, elbow, curve, u-turn, s-curve,
zigzag, orbit both ways, figure-eight, patrol, bezier) and MOVE presets (spin both ways, bank both
ways, boost, strafe, evasive zigzag, orbit) generate keys off the selected one. A timeline strip
with travel / hold bars, scrub, PREVIEW playback using the same interpolation rules as the director.
The inspector per waypoint (x, y, rot, scale, travel, hold, ease, duplicate / reorder) and per
zone (type, rect, window, phase, telegraph, symbol, cone anchor, enforce). Actions are added per
key, the FIRE shape picked from the pack's bullet-pattern icons, the ROUND from the boss's own or
every FIRETYPES kind, the FLASH from every registered muzzle family, the EFFECT from every
registered explosion family, the SOUND from `Audio.SFX` — all read off the engine's registry
through the host, not a hand list — with a TEST button that fires the action on the live boss.
ATTACH LIVE sends the scene to the running boss without saving; APPLY puts it on the row;
PLAY TEST runs it; the STAGE tab overlays the path and zones on the real fight with the current key
lit. EXPORT / IMPORT carry it in the fight document.

## Verified

- `probe_scene_0911a.py` (engine, real Chromium, stepped): **23 ok / 0 fail** — key 1 at (96,128)
  for tiles (3,4), the horizontal run to (384,128), the fan from the C anchor as magma rounds, the
  diagonal to (240,256), the keyed muzzle flashed, 228° mid-spin reaching the drawn pose, 1 FOV
  cone blit per frame for the attack zone, a round inside the safe zone removed, ownFire:false
  holding the cooldown, the once-track releasing the hull, the boss zone fencing it to (259,115),
  the palette at 37 muzzle / 16 explode / 12 round families and 113 kinds.
- `probe_scene_editor_0911a.py` (the tab, driven with the MOUSE): **16 ok / 0 fail** — three clicks
  lay three snapped waypoints, a dragged SAFE zone at (1,13 4×2) enforce:true, a dragged ATTACK zone
  set to the FOV cone through the inspector, a FIRE action added via the fan-five picker, the
  spin-clockwise preset appending 180/360 keys, APPLY landing 5 keys + 2 zones on the override and
  the live row, PLAY TEST spawning with the scene attached and the director on key 3 at 2.6s, the
  live overlay at 8,853 px, the safe zone active in the engine, EXPORT carrying the scene, CANCEL
  clearing it.

## Traps

- **`XART.rdy` is false on its first call, and a flash family first asked for at the moment of
  firing draws nothing the first time.** The probe measured exactly that: keyed muzzle, 0 flashes.
  `sceneWarm` touches every family a scene names at attach.
- **A probe that samples off-beat measures a working director as wrong.** Key 1 read (102,128)
  because the hull had already left for key 2 — the keys had no hold. Give the fixture holds and
  sample inside them, or step until the director reports the key reached.
- **The pack's badge names split to `light`/`neon`**, not colours — renamed to green/yellow/red at
  bake so the draw can key by zone type.

# 0911B — the theater layout

Mike: "I need a more theater and full screen for 75% screen like approach and a more modern editor
style for the editor."

`bossmode.html` is restructured; `bossmode.css` is rewritten; `bossmode.js` gains the layout state;
`scene.js` docks its inspector. No engine change.

## The shape

- **RAIL** (48px, left): the six views as icon tabs (`#tabs .tab[data-tab]` — the same selectors the
  probes use), LIST at the bottom.
- **THEATER** (`#w-view`): the view, black ground, the engine iframe filling it. 76% of 1600px, 80% of
  1920px with the dock open; 97% folded or in theater.
- **DOCK** (`#dock`, 340px, right): `#dock-main` = the fight INSPECTOR (editbar + `#insp`);
  `#dock-scene` = the SCENE inspector (`#sc-insp`, built by scene.js into the dock instead of
  `#sc-main`). `body[data-tab=…]` picks which one shows; `selectTab` sets it. The apply bar is
  shared under both.
- **DRAWER** (`#drawer`): the BOSS LIST (`#list-groups`), absolute over the theater, `body.drawer`
  slides it in; a mousedown on the view or a pick closes it. Parked at
  `translateX(calc(-100% - rail - 40px))` — at `-110%` its last 20px and shadow leaked over the rail.
- Header: logo, the pack's file buttons, `#view-title` (`#vt-tab` + `#vt-name`; `syncTitle` writes
  these now, not a `.win-title`), BOSSES / INSPECTOR / THEATER toggles, the engine LED.
- Chrome: flat panels (`--panel/--line` tokens, 1px borders, radius), Segoe/system-ui for the UI,
  Consolas for values; the pack's 9-slice window frame survives only on the OPEN BOSS modal; the
  pack's bitmap font titles the drawer and the dock (`.bm[data-bm]`, filled at boot).

`layout={dock,theater,drawer}` → `layoutApply()` toggles `body.nodock / .theater / .drawer`, marks the
header buttons, persists dock+theater to `localStorage.bof_bm_layout`, and dispatches a window
`resize` 220ms later (after the grid transition) so the scene field (`fit()`, now on resize) and the
plate refit. Keys: L, Tab, T/F11 (F5/F6/Ctrl+S unchanged).

## Traps

- `body{display:grid}` with an implicit column: the header's min-content (logo + 8 buttons + 3
  toggles + LED ≈ 1658px) widened the whole grid past 1600 and the dock fell off the right edge.
  `grid-template-columns:minmax(0,1fr)` on body, `min-width:0;overflow:hidden` on `#top`/`#tele`,
  and the toggles drop their labels under 1750px (`@media`, `.lbl`).
- Do not restyle `.ico` with `background-size` — the atlas rule positions a crop in atlas pixels;
  the three header icons vanished until the override was removed.
- `#dock input{min-width:0}` — inputs' intrinsic 20ch width overflowed the 340px dock.

## Verified

`probe_theater_0911b.py` 16/16 (shares at 1600/1920, drawer in/out, Tab fold + pull tab, T/F11,
scene inspector in the dock, refit, persistence across reload, PLAY TEST in the theater, no 404s,
no page errors); `probe_bossmode_editor.py` 19/19 and `probe_scene_editor_0911a.py` 16/16 unchanged
on the new DOM. Screenshots in `%TEMP%/theater/` (01 default 1600, 02 drawer, 03 theater, 04 scene,
05 play test, 06 default 1920).

# 0912A — the nine somersaults, Juggernaut's charge, the arcade opener and HELP

Mike asked for seven things in one message. All seven shipped; each has its own probe.

## 1. Every pilot somersaults

> "All pilots should get somersalt and properly use their graphics to make them somersalt."

`SOMER_PILOTS` has listed all nine since 0908, and `somersaultAvailable()` also gates on the art.
Counted the manifest: **64 `so` cells, not 72**. Eight pilots flipped; Lizzie silently could not.

**⚠ The `so` reel is not the `br` reel, and that had to be settled before anything was built.**
Compared cell-by-cell rather than by eye:

| | so2 | br2 |
|---|---|---|
| maverick | 196x78 | 39x184 |
| axel | 186x81 | 33x156 |
| juggernaut | 196x85 | 43x178 |

A pitch rotation presents the **span** and loses height; a roll presents the **chord** and keeps
it. Rotating her roll frames into `so` would have shipped a barrel roll wearing a somersault's
name — a bug that passes every "is the key registered" check. Suite section 281 now pins the two
reels as distinct for all nine.

So her reel is **derived from her own level plate** (his "properly use their graphics"), by the
pitch transform the engine already uses for a somersault with no authored reel (`RAP_MAN` /
`blacksteelManoeuvre`: "A somersault does the same on scale.y"). The profile is measured off
Maverick's authored eight, not invented:

```
frame       so0   so1   so2   so3   so4   so5   so6   so7
height/so0  1.00  0.81  0.44  0.89  0.96  0.88  0.54  0.81
width /so0  1.00  1.08  1.12  1.07  0.99  1.04  1.12  1.08
surface     top   top   EDGE  belly belly belly EDGE  top
```

Height collapses as span widens — what a pitching airframe does. The 0.44 floor is fuselage depth,
which is why the authored frames never vanish. so3/so4/so5 are the underside and keep the nose
up-screen (Maverick's do), so they are darkened and desaturated rather than mirrored; a mirror of a
near-symmetric delta is invisible.

**⚠ Built onto BOTH of her sheets.** She is the one pilot whose atlas page is chosen by a live flag
(`_shipSheetOf`) rather than by the key, and `applyLizzieSkin` only walks `LIZZIE_B42_RECTS` keys.
A `so` row on the stock sheet alone would keep its stock rect while the costume was on and crop the
B-42 page at stock coordinates — the asymmetric-key-set failure her own note in game.js describes.
`_so0.._so7` are in that table too. `_BUILD_SOURCE/lizzie_somersault_0912a.py`.

## 2. The charge, the wrecking balls, and the CHARGE bar

His 15s Juggernaut special is now three things sharing one window:

- **Wrecking balls** — six iron balls on chains, two rings, counter-rotating (`WB_RING`). They cull
  enemy rounds (the "shield" half) and carry the ram's *existing* damage calls on a per-ball clock,
  so a ring through a boss cannot out-damage the hull ram that was already balanced. This is also
  what his rage-mode invulnerability finally *looks* like — the i-frames were already at
  `hitPlayer` with nothing on screen to explain them.
- **The charge dash** — hold CHARGE then hold UP to wind up, release to ram. Hold time buys distance
  (`CHG_MIN`..`CHG_MAX`) and duration.
- **The CHARGE bar** — row 0, under SOMERSAULT and ROLL, with the special's remaining window as a
  rail under the fill. The generic SPECIAL bar steps aside for him ("we dont need to use the
  special bar anymore"); his icon still draws.

**⚠ Two bugs the probe caught, and they were the same bug.** The wind-up inherited the roll's "you
can still climb a little while rolling" allowance. UP is *half the charge's own input*, so the
climb ran for the whole wind-up and carried him **189px into the ceiling** — after which a FULL
charge measured **shorter** (152px) than a quick one (171px), because he had no room left to ram.
Reads as "the charge is weak"; actually movement leaking. Excluding `_chgOn`/`_chgDash` from that
branch fixed both: 341px vs 171px, drift 0.

**⚠ The first ring buried the ship.** At r=44 with chains starting at the hull centre, six chains ×
~7 links drew a solid knot of iron exactly where Juggernaut is — the photograph showed a cluster of
wrecking balls with no aircraft in it. Rings are 58/94 now, the chain starts at 24px (outside the
~50px hull), the balls draw slightly under their hit radius, and **chains draw before `drawPlayer`
while balls draw after**, so the aircraft sits on its own rigging with the balls swinging over.

**⚠ Not measured as boss HP.** The first cut of the boss-damage assertion failed against working
code: stage 2's Magma Ward absorbs into barriers before the hull sees a hit, so a real contact
legitimately moves hp by zero. The ball's own re-hit clock is the honest signal.

`barRows()` is the single source for which bar sits on which row — the draw reads it and so does
the debug bridge, because a probe recomputing the layout asserts its own copy of the rule.

**The icon was already right.** `special_icon_juggernaut_wrecking_ball` is a spiked ball on a chain
over fire, on the same hex badge as the other eight. Rendered it before replacing it; a composite
was strictly worse. Not touched.

## 3. Controls

Space was **already** on retina and has been since 0812a — checked, not assumed, and now pinned so
it cannot quietly go away. Added:

| | |
|---|---|
| `retina` | `c`, `space`, **`mouse3`**, `pad_b2` |
| `charge` *(new)* | `h`, **`mouse4`**, `pad_b3` — seat 2 gets `m`/`pad2_b3` |

**⚠ His "button 4 / button 5" are `e.button` 3 and 4.** A side button is 1-indexed to the human and
0-indexed to the browser; binding `mouse4` to the C role would have put it on the forward thumb
button, one off. CHARGE is a bind rather than a literal `'h'`, so the rebind screen and the second
seat can both reach it (`CTRL_ACTS`, `OPT_CTRL`).

## 4. The arcade opener — `GS.OPENER`

**⚠ `GS.INTRO` was already taken** — it is the stage card before `GS.LAUNCH`. Reusing it would have
put a movie trailer between the pilot select and every stage.

Nine beats off the ColeForge logo, in his order: two silhouette cards, the nine-pilot sweep, the
frontal portraits, three live gameplay cuts, the nine-screen montage, the logo. All seven of his
trailer lines are in the table and pinned. Any input skips it at any moment.

- The gameplay cuts are the **real game** — `attractDemoStart` now takes the pilot and the state to
  hold, rather than being copied.
- The nine-screen finale is **choreographed, not simulated**: nine live stages cannot run at once
  and nine recorded clips would be nine files to keep in sync. Each panel is a vignette drawn from
  the same art the game uses — the pilot's hull, a real boss plate, the real spin-out reel — so the
  three outcomes he named are authored. 3 fall / 3 finish a boss / 3 fly out.
- 0811d's "straight to the title" is superseded by this ask; its note is left standing because it
  records the decision being reversed. The attract reel is untouched and still disabled.

**⚠ Silhouettes come from the ship cutouts, not the portraits.** The first cut silhouetted
`port_cf_<p>_idle` and rendered a **black square with a rim light**. Measured: portraits are 77%
opaque (framed busts), `cinship_<p>_2` is 43% (a real cutout). The key existed, the load succeeded,
`rdy()` was true, and the picture was wrong — the render-it rule doing its job.

**⚠ The logo beat ended a 30-second trailer on the ENGINE's name.** `ASSETS.menuLogo` and `'logo'`
are both the "Cole Forge Engine / Rail Shooter Edition" plate. Rendered the three candidates side
by side: `nbl_logo` on `ui_menu_1` is the only BULLETS OF FURY wordmark in the build.

Music: `BOFA.music.opener` → `stage9_bonus_warp_run.mp3`, the one file in `assets/game/music` the
manifest never registered. ⚠ `startMusic` returns nothing, so a `if(!startMusic(x)) startMusic(y)`
fallback would always play y — the track is tested for before it is asked for.

## 5. HELP

A sixth title button, generated with the game's own buttons uploaded as a `reference_asset_id`, so
the frame, end-cap lights, teal circuit interior and orange lettering came back the same family.
Opens `GS.HELP`: three pages (CONTROLS / MOVES / HUD), LEFT-RIGHT to turn, BACK to leave.

**⚠ Every label is read from `keybind`, never typed.** A help screen that hard-codes "FIRE: J" is
wrong the moment anyone rebinds, and wrong *silently*. Pinned by rebinding FIRE in the suite and
checking the page follows.

**⚠ FOUR places knew the title menu was five long.** Two wrap sites in `handleTitleInput`, the art
draw loop (`for(let i=0;i<5;i++)`) and the mouse hit-test. Fixing only the wraps left EXIT GAME
invisible **and** unclickable. Caught by looking at the screenshot, not at the code.

The "screenshots" are live draws of the real art — page 2 uses the pilot's own reel frames, page 3
calls the same `_chargeBar` the play HUD calls. ⚠ Not the edge-on frames: `br2`/`so2` are
quarter-turn slivers that render as a dark splinter at illustration size; the banked frames read as
a manoeuvre in a still. ⚠ `stageText` is centre-only and its tenth argument is `outline`, not an
alignment — an align string there sets a flag and moves nothing.

## Traps recorded

- **`assets/game.js` is LF; `_BUILD_SOURCE/test_fl.js` is CRLF.** Detecting the ending from the file
  is not enough once a stray CRLF is in there — an earlier edit put six CRLF lines into game.js and
  every later anchor missed. Both files normalised and checked.
- **SpriteCook `raw_url` draws transparency as a CHECKERBOARD, not black.** A luminance key on the
  raw charge rings shipped a floating chessboard — invisible on a transparency-checkered contact
  sheet, obvious in-engine. Cut from `pixel_url` and upscale.
- Generated grids carry faint separator lines along their own ruling; inset each quadrant ~5% before
  trimming or the hairline ships with the sprite.
- Slice by cell *except* when the layout is irregular and every object is one solid island — the
  12-glyph pad sheet put START/SELECT pills outside a 4x3 lattice, so a fixed grid would have cut
  two in half.
- `Input` is lexical; a probe cannot hold a key down without a bridge (`BOSSMODE.hold`). `injectTap`
  is an edge and the charge is a hold.

## Verified

| | |
|---|---|
| `probe_somersault_0912a.py` | 10/10 — all nine flip, each on their own reel, i-frames, net dy 0 |
| `probe_charge_0912a.py` | 21/21 — binds, gating, both ram lengths, six balls, two rings, bar rows |
| `probe_opener_0912a.py` | 8/8 — nine beats in order, every beat paints, montage, skip, no 404s |
| `probe_help_0912a.py` | 13/13 — six buttons, wrap both ways, three pages, live binds |
| `test_fl.js` section 281 | added; suite at the documented 90–91 baseline, **zero net new failures** |
| earlier probes | bossmode 19/19, scene editor 16/16, theater 16/16, debug mode 33/33 |

## Open

- The special-ability icon was left alone — it is already a wrecking ball. Say if you want a new one.
- The opener plays on every boot. If that gets old, `openerStart()` is one call to gate.

# 0912B — the proper stage face, and a floor under it

> "whatever font is being used here is bad. please use stage fonts only the proper ones."

Sent with a crop of the HELP controls page: FIRE / MISSILE / RETINA-C and the J / K / C binds under
them, letterforms breaking up.

## Two faults wearing one symptom

**The face.** `uiFontArt()` hands back `ASSETS.stageArt['1']` — the stage-1 **card alphabet**, a
decorative stone set whose coverage stops at stage 5. `curFontArt()` hands back
`ASSETS.stageFontV4[n]` — **CF_BOFStageFonts Vol.2**, the authored per-stage face, the first set
covering all nine stages, and it already falls back to the card sheet for the frames before it has
decoded (stageText draws nothing when its sheet has not landed — the 0810o trap). The help screen
and the opener's trailer cards both used the card alphabet. Both now use `curFontArt()`.

**The size, which was half of it.** Rendered the page's own strings in BOTH faces at
8/9/10/11/13/16px (`_BUILD_SOURCE/probe_font_compare.py`). **Both faces mush below about 11px** —
the strokes are one pixel at that scale and the counters close up. The page was asking for 9px
captions and 7–8px bind lines. Switching the face alone would not have fixed the screenshot; this
is why the comparison was rendered before anything was changed.

`HELP_MIN=11`. `helpLabel` and `opnText` clamp to it, and `stageFitH` shrinks a long line only
down to it.

## The consequence that needed guarding

A floor means an over-long string **runs off the field instead of getting smaller** — the CHARGE
note did exactly that on the first pass. So `helpLabel` records the widest line it has drawn
(`_helpWidest`, measured with the engine's own `stageWidth`) and the probe asserts it fits:
currently 304px of 452px. Every page was re-laid at the new sizes, and the long lines shortened.

⚠ **This face has no usable apostrophe or middle dot at UI size.** Its `'` sits on the baseline, so
LIZZIE'S renders as LIZZIE,S, and `·` renders as a low period that reads as a full stop. Every UI
string on these screens uses hyphens and plain spaces instead.

## Verified

`probe_help_0912a.py` 14/14 (the widest-line guard is the new one), `probe_opener_0912a.py` 8/8,
suite section 281 gains four pins — the floor, the face on both surfaces, and a scan of every
`helpLabel` call site (21 calls, smallest 11). Suite unchanged at the 90–91 baseline.


# 0912C — the suite audit, and the flame flicker that quietly died

## What the 91 failures actually were

Audited rather than tolerated. The single biggest group — **29 assertions** — tested the star
thruster overlay that **0906s deleted on purpose**:

> Mike, 0906: "now you may make them animate via pixel glow inside and viola. we've solved a major
> problem and we can delete those ugly ass old thrusters we were using."

They probe `nthp_`, `drawShipThruster`, `'ntr_'+_tc`, `PILOT_TRAIL`, and the source-comment markers
and mount geometry of a draw that no longer exists. Every one was read individually before being
touched — none tests anything still live.

Retired with `okThr()`: a one-line helper beside `ok()` that counts and skips while
`THRUSTER_GONE` is set. The assertions stay **in place and reversible** — if the overlay ever comes
back, one flag lights all 29 again — and the suite prints one line saying they were retired rather
than silently dropping them. Same idiom as the Magma Colossus mech block.

**91 → 63 failures**, stable across runs (the ±1 stage-1 fixture flake is unchanged).

## The bug the noise was hiding

0906s did not just delete; it **replaced**. 144 `ship_<pilot><suffix>_g1/_g2` cells — the same
silhouette with only the flame's interior brightness changed — picked by `shipGlowKey()` at the one
frame-key chokepoint.

Those cells are in the manifest **at HEAD**. In the **working tree** there are zero:

```
git show HEAD:assets/manifest.js | grep -o '"ship_[a-z0-9_]*_g[12]"' | sort -u | wc -l   ->  144
grep -o '"ship_[a-z0-9_]*_g[12]"' assets/manifest.js | sort -u | wc -l                    ->    0
```

The 0909 re-pack onto one sheet per pilot (`nsa_ship_<pilot>`) rebuilt `BOFX.ships` and the phase
rows did not survive it. ⚠ `shipGlowKey` **fails soft** — `return (BOFX.ships[k2]) ? k2 : key` — so
nothing throws and nothing logs. The flames are simply static and have been since 0909.

Measured in real Chromium on the eight keys that actually carried phases (base, `_l`, `_r`,
`_pv0.._pv4`): **one** distinct key over a full 300ms cycle, on all nine pilots. 0906s measured
three. ⚠ My first measurement used `_nf` and was worthless — `_nf` never had a phase at all. The
key the engine actually picks for level flight is the bare `ship_<pilot>`, via `_shipFrameKey`.

## Why it cannot just be re-pointed

Rendered HEAD's `ship_axel`, `ship_axel_g1` and `ship_axel_g2` beside the working tree's
`ship_axel`. **It is a different aeroplane** — 178x200 with a pale flame against 136x155 with a
cyan one. The hull was replaced after HEAD, and a phase cell shares its plate's silhouette *by
design*, so the old phases belong to the old hull and to nothing else.

Restoring the flicker means **re-baking** 144 phases against the current plates. The original
script (`bake_thruster_glow_0906s.py`) recovered the flame pixels by diffing against a pre-bake
backup of the combined atlas — and that atlas is deleted in the working tree, so that route is
gone too. A re-bake would have to find the flame in the current plates (luminance-weighted, in the
lower band where the plume lives) rather than recover it. That is art work on Mike's ships, so it
is his call, not a silent fix.

## What is pinned now

Suite section **282** asserts the replacement is wired (`shipGlowKey` exists, `SHIP_FLAME_BAKED` is
on, the chokepoint calls it) and carries **one deliberate red**: `SHIP_FLAME_BAKED` is on, so the
phase cells must exist — found 0. That is the single failure that replaces 29 meaningless ones, and
unlike them it describes something actually broken.

It also pins the control: the B-42 propeller keeps its 18 phase rows in `LIZZIE_B42_RECTS` in
game.js rather than in the generated manifest, and that one **does** still flicker — which is the
proof that the picker is fine and the cells are what went missing.

## Verified

Suite 63 failures (from 91), stable over three runs. All drop probes unchanged: somersault 10/10,
charge 21/21, help 14/14, debug mode 33/33.

---

# 0912G/H — BULLETS OF DEBUG, AND THE CAMERA TRAP FOR THE FIFTH TIME

Mike: *"Make an additional extension to my Boss Mode Debug Editor but overall for the entire game
outside of the bosses, calling it 'Bullets of Debug!' ... level backgrounds, waves, enemies,
projectiles, master game stuff, menu layouts, button layouts ... demo how enemies operate and like
bosses, change their properties, data, hp, speed, attack, firing range."*

This is increment 1, and the honest scope statement is at the bottom: what he described is several
projects, and it is being built in verifiable pieces rather than claimed in one pass.

## What landed

**`window.BOFDEBUG`** — the bridge, a sibling of `window.BOSSMODE`, inserted right after it. It
exists for one reason: every roster table in `game.js` is a lexical `const`, so the editor can
already CALL the engine (every column-0 function IS a window property) and cannot SEE its data.

| what | measured |
|---|---|
| roster tables | 22 (`S1_TANKS`, `NEF_S1`…`NEF_S9`, `PROJ`, `FIRETYPES`, `ENEMY_VOLLEY`, `STAGE_AI_PROFILE`, `L6_FLEET`, …) |
| enemy types | **226**, the union of every table plus 17 hand-coded `switch`-body types |
| switch-body types | reported with `row:null` rather than hidden — the editor must key on **type+table**, because name collisions across tables are real |
| movement patterns | read off `updatePlay.toString()`, not hand-listed (68 today) |
| pattern shapes | the scene director's own vocabulary, via `sceneEmitBeat` |
| art | `keys/rdy/get/override/restore/overridden` — an in-memory sprite swap and a put-back |
| lab | a quiet stage with the wave script spent, so one unit can be studied alone |

**`bulletsofdebug.html` + `assets/bulletsofdebug/{bod.css,bod.js,ui/}`** — the editor. Same theater
shape as Boss Mode (rail | viewport | folding dock), cyan pack instead of orange so a screenshot of
one is never mistaken for the other. ENEMY LAB is live: pick from the roster drawer, `S` spawns it
into a quiet stage, and the inspector's sliders write straight to the live unit — hp, hull, speed,
movement pattern, per-unit shadow, and a FIRE panel that emits boss-grade patterns off an ordinary
enemy.

## ⚠⚠ The FOV cone was drawing a world coordinate in screen space

CLAUDE.md records this class **four** times — the launch seam (0810a), the outbound routes (0810c),
the level-1 ship (0810e), and `probe_seam.py`, which recomputed `player.x - camX` instead of
recording what was drawn and therefore asserted the fix it was meant to test. This is the fifth, and
what makes it worth writing down is that **three separate terms were missing, and every one of them
is dormant in exactly the case you would screenshot first.**

### 1. `camX` — zero at the left edge of every stage

The cone looked perfect until the camera scrolled, then sat ~190px right of the ship. `drawWorld`
runs under `translate(-camX)`; the overlay mapped `u.x` straight through.

⚠ **And `camX` alone is not the offset that was drawn.** The translate is applied only while
`worldWidth() > viewW()`, so a non-scrolling stage can hold a value nothing subtracted — an overlay
trusting it there is adrift by exactly that amount, which is the inverse of the bug it was added to
fix. `snapshot().camX` reports the EFFECTIVE camera (`_camEff`).

### 2. the zoom — 1.00 on all nine stages today

Measured, every stage: world **680** against `VIEW_PLATE_W` **680**, so `viewZoom()` returns 1 and
the whole term vanishes. ⚠ **`game.js`'s own comment at `viewZoom()` still says stages 1/2/3/7/8 are
800, and is stale.** The dial is one number — *"To try another plate width, set this to width/800"* —
so a plate change would silently break every overlay in the editor. It is exercised by forcing
`viewZoom` (a column-0 function, therefore a window property) to 0.85 inside the probe.

⚠ **And `y` is not `y*vz`.** `drawWorld` scales and then anchors the BOTTOM edge
(`translate(0, VH*(1-vz)/vz)`), so world y=VH stays on the bottom of the screen and the zoom reveals
rows ABOVE y=0. `bossmode.js:419` already had the correct pair — reading the sibling editor would
have been quicker than rediscovering it.

### 3. the letterbox — derived instead of measured

Sizing the overlay to its own container and computing `sc=min(W/VW,H/VH)` was **19.3px out across
and 19.8px down**: index.html places its canvas inside the iframe with its own layout, which no
arithmetic out here can know. Boss Mode has always read `#screen`'s `getBoundingClientRect` and
pinned its overlay there. ⚠ **And that rect is in the IFRAME's coordinate system** — carrying it into
page space by the iframe's own rect is a third term, worth exactly the iframe's page offset
(measured **-51px, -106px**, which is the rail's width and the header+toolbar's height).

## How it is proved, and why the proof is trustworthy

**`BOFDEBUG.xform`** captures the live CTM off `ctx.drawImage` during a real frame while
`_inWorldXform` is true. ⚠ **On the INSTANCE** — `ctx` carries its own copy of the method, so a
`CanvasRenderingContext2D.prototype` trap records **0 blits** on a draw that is provably running
(0905h, measured).

`probe_bod_overlay_0912h.py` compares that matrix against `BOD.S._mark` — the point `drawOverlay`
actually drew — **in page space, through `getBoundingClientRect` on both sides**. Neither side's
arithmetic checks the other, which is the whole point: a probe that rebuilds `(x-camX)*vz` to check
code computing `(x-camX)*vz` passes on a broken frame.

```
BUSTED (camera ignored)   282.4 px off   <- the check can fail
LIVE                        0.3 px across,  2.0 px down
FORCED ZOOM 0.85            0.3 px across,  1.4 px down
```

## ⚠ Three probe faults on the way, all worth keeping

1. **It moved the unit and then compared against the previous frame's mark.** `S._mark` is what the
   overlay drew LAST frame, so re-seating inside the measurement measures the unit's own travel:
   **+71px across and +134px down on a correct build.** Seating is its own step now, a frame earlier.
2. **The subject was culled mid-run.** A fast mover in a lab that runs real time flew off the bottom
   across four measurements — which read as "the cone stopped painting" and "FIRE fired nothing"
   rather than as a unit that was simply gone. Both checks now say which.
3. **Writing `S.unit` by hand does not render the inspector.** `S.unit` is a FLAG — `unit()`
   re-fetches the live object every time, because `enemies` is reassigned every frame by the cull —
   and the inspector is rendered by `pick()`/`spawn()`. Drive the editor's own path.

## Two smaller ones

⚠ **`FIRE ONCE` defaulted to `shapes()[0]`, which is `stream`, which fires one round.** The pattern
system was working perfectly, and the first click a user ever makes looked like a broken button.
`FIRE_SHAPE0='fan'`.

⚠ **`art.override` must delete the `BOFX.playercells`/`BOFX.cells` row before writing `XART.img[k]`**
(shelved for restore). Cells are checked before the cache, so writing the cache alone changes
nothing — the same shape as 0906g's `_flushShipCells`.

## Verified

| probe | result |
|---|---|
| `probe_bofdebug_0912g.py` | 18 ok / 0 fail — the bridge |
| `probe_bod_editor_0912g.py` | 21 ok / 0 fail — the editor driven like a user |
| `probe_bod_overlay_0912h.py` | 13 ok / 0 fail — the mapping, with a busted arm at 282px |

Suite **section 283** is 11 ok / 0 fail and pins all three terms in SOURCE, ⚠ **with comments
stripped** — the notes explaining this fix quote the wrong formulas by name ("NOT `y*vz`"), which is
section 47's trap, self-inflicted.

## Scope, honestly

What Mike asked for is not one feature. A sprite editor with save-back is its own project, given that
`manifest.js` is generated; waves, menu layouts and button layouts are each their own surface. The
bridge mechanism for save-back is proven (`art.override`/`restore`, measured swapping a cell in and
putting it back); the UI is not built. FIRE, STAGE, ART and JSON remain, and `selectTab` says so
rather than pretending.

## 0912i — the FIRE tab, and the twelve dials it refuses to ship

Mike asked Bullets of Debug to cover *"projectiles ... muzzle flashes, firing speed, damage or
damage per second, projectile patterning ... anchor points"*. Seven subsystems were read before a
control was drawn — `PROJ`/`FIRETYPES`, `drawBullets`, the muzzle functions, `ENEMY_VOLLEY`, the
flash families, damage, and the scene director — and the finding that shaped the whole tab is that
**a literal reading of that list produces sliders that read back the value you wrote and change
nothing.**

⚠⚠ **THERE IS NO ENEMY-TO-PLAYER DAMAGE NUMBER IN THIS ENGINE.** `playerHit()` takes **zero
arguments**, there is no `player.hp` anywhere in the file, and the enemy-bullet collision never
looks at the bullet. Every enemy round costs exactly one shield pip or one life. Four `eBullets`
carry `dmg:1` and it is read by nothing — *"the worst kind of false positive"*. So a damage slider,
and the DPS that would follow from it, cannot exist; `BOFDEBUG.inert()` names them and eleven others
with the measurement that condemned each, and the tab RENDERS that list rather than shipping the
controls. The honest dials are cadence (rounds/second), pattern geometry, and how much screen a
pattern denies.

**The other eleven, all measured:** `curve` (`_curve` is read only by `updateRollers` over `rollers`,
Falva's player pinball pool — enemy bullets never enter it); `homing`/`turn` (gated on
`b.homing && run.stage===1`); `speed` on `emissile`/`_shootable` kinds (the steering block rewrites
`vx/vy` from `spd*DIFF.ebSpeed` every frame); `PROJ.slot/szMul/tint/spin/pal` (**only `.type` is ever
read** — PROJ is looked up in exactly one place in 61,812 lines); `SHIPBOSS[kind].dmg` (an array of
**sprite keys**, and it is in `BM_LIVE_FIELDS`, so Boss Mode can patch it and see no effect);
`ENEMY_VOLLEY` `n`/`spread` (neither key exists on any of the 52 rows); `_volSeed` (exists only in a
comment); `CFX_STAGE_PROJECTILE` (`Object.freeze`'d); FIRETYPES fields on a BPFX kind (the premium
path is an unconditional `return`, not a try-then-fall-back); and a new FIRETYPES row for a kind that
already has a PROJ row.

⚠ **FIVE OF THE TWELVE SHAPES EMIT ONE ROUND PER BEAT, BY DESIGN.** `sceneEmitBeat`'s switch has
cases for only ten — its `default:` comment names **stream and aimed** — and `spiral` and `sine` each
call `fire()` exactly once, while `mirrored` always calls it twice. The movement in `spiral` and
`sweep` comes from the incrementing `beat` index. So a one-shot preview renders five of twelve as a
single round, which is what made `FIRE ONCE` look like a broken button. `BOFDEBUG.burst()` is the
fix, and ⚠ **it is pumped from `updateEffects`, the game's own per-frame tick** — an editor-side
timer would run while the game is paused and on wall-clock time, so the preview would not match a
real fight.

⚠ **THE ANCHOR WAS INERT ON EVERY ORDINARY ENEMY.** Measured on a stage-1 delta jet: all twelve slot
names — C, L, R, LW, RW, nose, tail, bay, b1, b2, gunL, gunR — returned **one point**,
`(x, y + h*0.30)`, because `shipBossMount` reads `SHIPBOSS[b._ship].mounts` and an ordinary enemy has
no `_ship`. A real ship boss gives three distinct points. `shipBossMount` now also honours a per-unit
`_mounts` in the same normalised form, so it composes with the pose rotation and scale for free;
measured byte-identical on the Void Bat before and after.

⚠ **AND THE DEFAULT MUZZLE FLASH IS BOSS-ONLY AND FAILS SILENTLY.** With no `a.flash`,
`sceneEmitBeat` calls `shipBossMuzzleStart`, which returns immediately unless `b._ship` AND that
SHIPBOSS row has both `.proj` and `.mounts` — so firing off an ordinary enemy with the default
produces **zero** flashes. Measured: naming a family queues 1, the default queues 0. The tab has no
"default" option for that reason; the nine families that exist are read off the atlas with their
frame counts.

⚠ **`shadowed` IS A DERIVATION AND THE EDITOR MUST NOT RE-IMPLEMENT IT.** Resolution takes
`PROJ.type` first unless the kind is dedicated (`/^s[1-9]/`, or exactly `magma`/`lavaComet`), so a
row is unreachable only when it is not dedicated AND `PROJ.type` names a **different** row. The first
cut re-derived it in the UI, dropped that last clause, and labelled `blast` shadowed on screen — when
`PROJ.blast.type` IS `blast`, i.e. it resolves to itself. Derived in the bridge, it reproduces
exactly the eight the recon named — `emberGem`, `eshot`, `frostComet`, `kingPellet`, `laser`,
`railshot`, `venomDart`, `voidOrb` — and clears `blast` and `s3shard`. **That is eight authored
projectile rows nothing in the game can draw**, which is worth showing rather than hiding.

⚠ **`setVolley` MUST FIND ROWS BY NORMALISED KEY, NOT BY DERIVING SPELLINGS.** `ENEMY_VOLLEY` is
keyed in both spellings deliberately (0811l) and the roster hands the editor the lower one, so
building `[type, type.toLowerCase()]` never reaches `s1jetDelta`. That is exactly half the fix, which
is the shape of the bug that had stages 4 and 6 fielding 26x26 one-hp jets for six drops.
⚠ **And `enemyVolley` is `(e, force)` — two arguments.** There is no per-call pattern override; it
reads `ENEMY_VOLLEY[e.type]` and nothing else, so a third argument is silently dropped. Unforced it
takes the dead path and mostly returns false without firing.

⚠ **TWO BAD DEFAULTS, BOTH FIRST IMPRESSIONS.** `FIRE ONCE` defaulted to `shapes()[0]` = `stream`
(one round), and the projectile kind defaulted to `'e'`, **which is not a registered kind at all** —
it has no `PROJ` row and no `FIRETYPES` row, so it falls through the whole draw chain to the 12x11
fallback pip. Now `fan` and `pellet`.

Probe: `probe_bod_fire_0912h.py` **18 ok / 0 fail** — it asserts that the shipped controls move
something measurable (a fan lays n distinct headings; a spiral BURST rotates them 24° a beat; a wall
leaves the gap it is told to; the anchor slider moves the mount AND the round leaves from it) and
that the ones that cannot work are **named rather than shipped**. Suite section 284 pins both halves,
including that there is no damage slider.
