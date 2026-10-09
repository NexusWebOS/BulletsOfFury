# Level 5: Museum of Violence (October 9, 2026)

Mike asked me to study **Mercs**, **Demolition Man** (for the stage 2 / museum stage) and **Contra: Hard Corps**
(for weaponry and boss AI), reverse engineer them, and merge the result into the top-down shooter section,
combined with the stealth / Metal Gear sections.

The result is **Level 5, MUSEUM OF VIOLENCE**, a new on-foot mission in the Overdrive ground build at
`expansion/topdown/`.

## How the games were studied, and what "reverse engineered" means here

None of the cartridges, and no emulator, are in this repository or this container. I also do not decompile
commercial ROMs. That leaves three sources:

1. **The earlier SegaScope measurements**, recorded in `expansion/topdown/DESIGN.md` §1. Mike's own emulator
   sessions measured Mercs' push-scroll (about 1.16 px a frame while pushing), its rifle (about 5.7 px a frame)
   and its enemy rounds (about 2 px a frame). Those speeds were already the engine's units.
2. **Published behaviour**: manuals, reviews and wikis.
   - [Sega Retro: Mercs](https://segaretro.org/Mercs)
   - [Wikipedia: Mercs](https://en.wikipedia.org/wiki/Mercs)
   - [Sega-16 Mercs review](https://www.sega-16.com/?p=6732)
   - [Wikipedia: Demolition Man (video game)](https://en.wikipedia.org/wiki/Demolition_Man_(video_game))
   - [Mean Machines Sega review of Demolition Man](https://everygamegoing.com/larticle/Demolition-Man-000/32147)
   - [Sega Retro: Contra: Hard Corps](https://segaretro.org/Contra:_Hard_Corps)
   - [Giant Bomb: Contra: Hard Corps](https://www.giantbomb.com/games/3030-13902/)
3. **BOF's existing Hard Corps boss study**: `docs/BOSS_STUDY_0918.md` and `docs/HARDCORPS_BOSSES_1007.md`.

Every system below is **original code written for this engine** from that behaviour. No cartridge code, art or
data is used.

## What came from where

| Source | Behaviour | How Level 5 implements it |
|---|---|---|
| **Mercs** | The screen follows you north and never scrolls back. | The camera's lower limit ratchets up and you are kept on screen, so the wing you enter is a committed choice. |
| **Mercs** | A Mega Crash bomb hits everything on screen, with limited stock (3 to start, more found in the stage). | **A+B together** (Mercs' two-button bomb) or **G**. It hits every on-screen enemy, prop and boss part, clears enemy rounds, and gives brief invulnerability. Start with 3, cap 5. Pressing it never also reloads. |
| **Mercs** | POW raises weapon power. | POW pickup (the authored kinetic badge): the gun in hand goes LV1 → LV3. +40% damage and −12% cooldown per level. |
| **Mercs** | You board vehicles; each has its own health and ejects you when destroyed. | The exhibit Fury tank in the east wing is boarded by walking into it. It runs on the full tank engine (vulcan + homing, its own 14-point armour). Destroyed, it explodes, leaves its wreck and ejects you alive with no life lost. **O / Select** dismounts and parks it. |
| **Demolition Man** (museum stage) | An overhead, Smash TV-style section set in the city museum. Hostages are held there. You shoot the artworks to find power-ups. | The **Hall of Arms** locks with laser curtains for three waves, then unlocks. **31 exhibits** (23 of them holding fixed contents set at spawn): statues, vases, paintings, rifle and plasma weapon cases (the Museum of Violence's weapons), alarm panels and rope barriers. Each breaks once into its authored broken plate. **Five hostages** (Fury ground crew) are freed by walking to them and each hands over a reward. Shooting or blasting one kills them for −5000. |
| **Contra: Hard Corps** | Four carried weapons. Death loses the one in hand. A bomb. Branching routes. Bosses broken apart in phases. | **A–D slots**: a fifth gun replaces the one in hand. Death drops only that gun (the pistol always stays). You respawn where you fell. The route branches three ways after the Hall of Arms. **THE EXHIBIT** boss is broken apart in three forms (below). |
| **Metal Gear** | Cones, alert phases, cameras, noise, hiding, CQC, bodies, lasers, alarms, ducts. | Existing: green/yellow/red cones, SNEAK / CAUTION / ALERT / EVASION, cameras, noise and the radar. **New in Level 5**: <ul><li>**Laser tripwires** that you crawl under prone, or shoot an emitter to kill.</li><li>**Alarm panels**, now the only source of reinforcements; break them and nobody answers.</li><li>A **crawl duct** that is prone-only, hides you, and guards cannot follow into.</li><li>**CQC**: fire from behind an unaware guard is a silent takedown with no round and no noise.</li><li>**Bodies** that another guard can find, which sends the museum to CAUTION.</li><li>**Local radio range**: a guard calls only the guards near him.</li></ul> |

## The mission

1. **Lobby.** Two patrols, two cameras, an alarm panel, exhibits and a hostage. Learn the stealth.
2. **Hall of Arms** (Smash TV / Demolition Man). It locks and sends three waves. The weapon cases on its plinths
   hold the spread shotgun, minigun, fusion beam and rocket launcher. This room's alarm does **not** count against
   the GHOST bonus. When it clears, it shows the route choice.
3. **Three routes north** (Hard Corps branching, committed by the Mercs push-scroll):
   - **West gallery (stealth):** a painting maze with patrols, a camera, two laser tripwires, an alarm panel and
     two hostages.
   - **Central duct:** prone only and hidden. It is the ghost route.
   - **East vehicle hall (armour):** heavies, a turret and an alarm. The boardable exhibit tank is here.
4. **Rotunda.** The routes rejoin here. A patrol, a camera, an alarm and the last hostage.
5. **Grand hall: THE EXHIBIT** (`boss_exhibit.js`). It is the Razorback Mk II on display, reactivated, on the
   Razorback's own authored plates. It follows the Hard Corps rhythm of cause → commit → attack → crossing →
   recovery, and escalates by reshaping the fight, not by adding HP:
   - **ON DISPLAY.** It is bolted to its turntable. Twin guns track you, it fires a warned cannon spread, and it
     launches a locked rack of shootable missiles.
   - **BREAKOUT** (both pods broken, or below 72%). The plinth shatters. It drives, and its green → yellow → red
     ram smashes the hall's statues, which are your cover. It stalls on the wall, and a stalled hull takes
     double damage.
   - **OVERDRIVE** (turret broken). Sonic rings with a rotating gap, sonic walls with one hole to cross through,
     and faster rams.

   The hull takes 15% damage until the turret falls.

## Art

All new art was generated with SpriteCook. Its sources and prompts are kept in
`expansion/topdown/art/museum_1009/`.

- **Museum plate** (gpt-image-2, 2K, 9:16). The layout came back close to the brief. A second edit cut the
  rotunda's two side doorways. The plate is normalized to 800×1422.
- **Exhibit sheet** (gpt-image-2.5-flare, transparent): 16 cells, in intact/broken pairs.
  - Each pair is cropped with one shared rectangle, so a state swap never moves the prop.
  - The laser post's painted beam was cut off the plate. The live beam is drawn from the game's authored
    `tank_laser_crimson` bolt.
- Total cost: 28 credits. 10 remain.

Builder: `_research/build_museum_1009.py`. Collision overlay: `_research/check_museum_1009.py`. The overlay draws
every wall, the ring, the curtains and each placement over the plate.

Reused, unchanged:

- Hostages use the on-foot pack's stun, recovery, power-up and death reels.
- The exhibit tank is Niel's paint.
- Mega Crash uses the `fury_bomb` pickup, and POW uses the `inf_kinetic` badge.

## Engine changes (all gated, so Levels 2–4 are unchanged)

- **`core.js`**:
  - Rect type `'d'` (duct): solid unless the mover is prone, opaque to sight, and not walkable for guards.
  - Nav clearance is now a per-mission value (`World.navR`). It stays 14 for tanks; Level 5 sets 9 so the
    gallery lanes exist for pathing.
  - New binds: `crash` (G) and `exitVehicle` (O / Select).
- **`main.js`**:
  - Mission hooks: `setup`, `pre`, `tick`, `cam`, `respawn`, `canReinforce`, `drawFloor`, `drawOver`, `hud`,
    `score`, `keys`, `help`.
  - A fourth title card.
  - Results can carry extra rows.
- **`tank.js`**: `TD.PROP` is exposed, so a mission can register prop kinds with their own `draw` and `onBreak`.
- **`campaign.js`**:
  - Gun level scales damage and cadence. LV1 is unchanged, so Level 3 is identical.
  - Optional four-slot carry.
  - Pickups `pow`, `crash`, `life` and `score`.
  - The duct hides you.
  - The Miami tall-stack occlusion is now limited to Level 3.

## Verification (native Chromium)

`python expansion/topdown/_research/probe_museum_1009.py`: **28/28**, with zero page, console or HTTP errors.

- The probe uses real keys for the title, the brief, Mega Crash (hold J, tap K), CQC, the laser, the duct and
  boarding.
- The previous build's probes still pass: `probe_campaign_1008.py` **29/29** and `probe_ground_1008.py`
  **23/23**.
- Those two ran through a wrapper that answers the browser's own `/favicon.ico` request. This Chromium build
  logs that 404 without a URL, which their error filter cannot recognize.
- The probe's 17 screenshots were inspected. They live in ignored `_shots/museum_1009/`; the results JSON is
  `docs/qa/museum_1009.json`.

These are protected fixtures that isolate mechanics and pixels. They are **not** an unassisted clear and not a
balance sign-off.

## Open, for Mike

- **Music.** The mission uses the expansion's existing stage and boss tracks. Mike's call.
- **Hostage art.** Hostages wear the helmeted pilot bodies' stun reel, so they read as captured Fury crew, not
  civilians. Civilian art would be a separate generation.
- **Balance.**
  - Three Hall of Arms waves under a one-hit rule.
  - Mega Crash strength: it kills every on-screen guard.
  - Exhibit tank armour of 14.

  All are first-pass numbers.
- **Gallery pathing.** The gallery maze is narrower than the 24 px nav grid, so an alerted guard there paths
  poorly and falls back to direct movement. Patrols use waypoints in open lanes.
