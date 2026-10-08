# Overdrive Ground Operations: design notes

## October 8, 2026 — current implementation

All three missions are playable in the standalone build. See [README.md](README.md)
for the current behavior, controls, art ownership and measured verification.
Level 2 uses the new compound terrain and original modular **The Warrior**;
Level 3 uses the Miami infantry route; Level 4 contains the hostile Machinist
squad and a selectable Hotwire/Phoenix/Niel companion. Player movement is now
immediate and smooth, with independent aim. Destructible structures remove
their collision/vision geometry when broken. Charge effects belong to the
player cannon; the Warrior uses volleys and a warned ram.

The notes below preserve the earlier research and proposal. Their blue-player
tank, Razorback boss, old map/paths, locked Level 3 and future-level descriptions
are historical, not the current implementation.

These are the top-down ground stages for the Overdrive expansion. They are a standalone page; they do not touch `assets/game.js`.

- **Level 2 (Fury Tank)** is built and playable.
- **Level 3 (pilot on foot)** is designed and its art has arrived; it is the next build.
- **Level 4** is the Machinists' tank level (Wren / Rolf / Chaz). Their art stays out of Level 2.

## 1. Where the mechanics came from

Before any code was written, the reference games were played on the SegaScope emulator and measured with `Sega Engines/_Core/segascope/td_session.js`. This captured what moved, by how much per frame, and what each button spawned.

All of that is **study material only**. No code, art, or data from those cartridges is in this folder. Every line here is original, and every sprite is Bullets of Fury's own.

| Game | What was measured | Where it shows up here |
|---|---|---|
| Granada | <ul><li>The tank **turns before it moves** and drives about 2 px a frame.</li><li>The camera is locked on the tank.</li><li>The heavy shell travels about 15.6 px a frame, with recoil.</li><li>Light shots are separate from the heavy round.</li><li>It has a target radar.</li></ul> | <ul><li>The player tank turns first, then drives at 2.05 px a frame.</li><li>The cannon (B) fires a 15.6 px/frame shell with recoil.</li><li>The radar.</li><li>The follow camera with a look-ahead along the heading.</li></ul> |
| Mercs | <ul><li>Vertical push-scroll that only ever advances, about 1.16 px a frame while pushing.</li><li>The rifle round travels about 5.7 px a frame.</li><li>A screen bomb with limited stock.</li><li>Enemy rounds travel about 2 px a frame.</li></ul> | The Level 3 camera (section 4) and its weapon speeds. |
| Contra: Hard Corps | Not measured on the emulator. It is used by design: four carried weapons you swap between, and losing the weapon in hand when you die. | <ul><li>VULCAN / CRASH / LASER / HOMING, levels 1 to 3, swapped with Z or the mouse wheel.</li><li>Dying loses the gun you were holding.</li><li>The boss is broken apart part by part.</li></ul> |
| Xeno Crisis, Smash TV | Arena rooms. The emulator sessions landed in screen transitions, so the numbers are noisy. | The Level 3 arena rooms (section 4). They need a cleaner capture before the numbers are trusted. |
| Soldiers of Fortune, Demolition Man (stage 2) | **Not studied yet.** Soldiers of Fortune needs a hire-screen boot script. Demolition Man's overhead stage was never reached. | — |

## 2. The Metal Gear layer (live in Level 2)

These are all in `js/stealth.js`.

- **Vision cones.**
  - Each guard, turret and camera has a cone with a range and a half-angle.
  - The cone drawn on screen is the game's own FOV plate (`bmfx_fov_*`), scaled per axis so its edges match the half-angle used for detection. **The cone you see is exactly the cone that tests you.**
  - Wide plates are used for tanks and turrets. Tall, narrow plates are used for snipers and cameras.
- **Cone colours** follow Mike's rule:
  - green at 25% while the guard is calm
  - yellow while it is suspicious or searching, with the yellow hazard frame flashing above it
  - red when it has seen you, with the red frame flashing when it is about to fire
- **Detection meter.**
  - The meter fills faster when you are closer and when you are moving.
  - It reaches *suspect* at 0.3. At that point the guard turns, investigates the spot and scans.
  - It reaches *spotted* at 1.0, which raises the **ALERT**.
- **Line of sight.**
  - Buildings and hedges block sight. Pits do not.
  - **Smoke (Y)** blocks sight for 7 seconds.
  - A tank inside a hedge is **hidden** unless a guard is within 70 px.
- **Noise.**
  - The cannon carries 420 px and the main gun about 140 px. Explosions and dying tanks are also heard.
  - Noise goes through walls.
  - A guard reacts 0.35 s after hearing something. That delay is what lets a cannon shell land on a target that has not turned yet.
- **Sneak strike.** A hit on a guard that has not noticed you does double damage, and a kill scores double.
- **Alert phases.**
  - **ALERT**: everyone within radio range hunts you, the radar jams, and reinforcements roll in from the nearest off-screen gate (up to 3 alive at once). The timer refills every frame anyone can still see you.
  - **EVASION**: guards search around your last known position with yellow cones. The radar is still jammed.
  - **CAUTION**: guards detect 1.5 times faster and patrol 15% faster.
  - Then back to **SNEAK**.
- **Cameras** sweep and never shoot, but they have the longest radio range. Shooting one is quiet only if nobody sees you do it.
- **GHOST bonus.** Reaching the boss with zero alerts earns 25,000 points.

## 3. Level 2: IRON INFILTRATION

**Map.** The map is the compound master `nst4b_master` (800×3616), played from the south gate north to the command plaza.

- `js/level2_map.js` holds the solid map as 112 rectangles. They were authored by hand from a gridded render of the plate's left half, then mirrored, because the plate is built mirror-symmetric.
- `_research/check_map.py` draws the rectangles, units, patrol routes, props and checkpoints over the plate. Re-run it after any edit.
- It also confirmed that no unit or patrol point starts inside a solid.

**Player.**
- The player drives `tk3`, the blue tank.
- The enemies use `tk0` (tan scout), `tk1` (olive rifle), `tk2` (black heavy, twin shells with a charge tell) and `tk4` (green sniper, long narrow cone, 0.75 s charge tell).
- Every tank switches to its damaged and critical plates as it takes damage.
- **Turrets** are the `nlgt` turret core. **Cameras** are the `nmrv` radar dish.

**Props.** Fuel barrels explode and set off other barrels. Ammo crates and P-boxes break open into pickups, and you can also crush them by driving into them.

**Pickups.**
- Weapon icons (`micon_*`)
- Armour +4 (`crate6`)
- Smoke +2
- Score
- One 1UP

**Checkpoints.** There are four. Dying loses one life and respawns you at the last checkpoint with full armour, and the alert drops to CAUTION.

### Boss: Razorback Mk II

The boss uses the Razorback's own plates: eight hull headings, turret, side guns, missile pods, rotors, scrolling treads, the sonic set and the wreck.

- **Breaking it apart.**
  - Both side guns and both pods are separate targets.
  - The hull takes only 15% damage until the turret falls.
- **Attacks.**
  - *drive*: both guns track you independently while it moves.
  - *cannon*: a turret charge, telegraphed with a yellow then red FOV cone, then three shells.
  - *rack*: a lock-on warning, then six razor missiles that you can shoot down.
  - *nova*: once the turret is gone, a ring of sonic rounds with a rotating gap.
  - *ram*: under 40% health, a green → yellow → red cone, then a straight charge. It stalls when it hits the wall, which is your opening.
- **Arena.** The camera frames both you and the boss. The boss's drive targets always stay within one screen of you, so the camera can always fit you both.

**Music.** It uses tracks from `assets/game/music` that the main game does not play:
- `Unused1` for the stage
- `Unused_UnknownBossTheme` for the boss
- the stage-clear jingle for the results

This is Mike's call to change.

**Results screen.** It uses Mike's rank plates. **L** (LOSER) is given at 5 or more deaths.

## 4. Level 3: BOOTS ON THE GROUND (pilot on foot)

The engine pieces are all reusable: stealth, the map loader, the flow field, pickups and the radar. What changes:

- **Camera.** Mercs-style vertical push-scroll that never scrolls back, with Xeno Crisis-style arena rooms that lock until they are cleared.
- **Pilot.** 8-way run, aim locked by a held button (strafe), and a combat roll with invulnerability frames.
- **Stealth.** The cones get stricter on foot:
  - Long grass and hedges are the hiding spots.
  - A takedown from behind is silent and has no noise radius.
  - Bodies left in a cone raise suspicion.
  - Cardboard-box-style cover is a prop you can carry.
- **Weapons.** The same four Hard Corps weapons, re-tuned for a rifle, plus grenades.
- **Boss.** A Contra Hard Corps-style multi-form boss, built once the soldier art exists.

### Art status (2026-10-08): unblocked

The GitHub drop `cc3d7f41` supplied everything Level 3 was waiting on, so the SpriteCook plan that used to be here is moot and nothing needs to be generated:

- `expansion/onfoot/`
  - pilot actions: crouch/prone in four directions, crawl, roll, wall tap, grenade, death, revive
  - six handheld weapons with their boxes and ammo
  - robot troops, a turret, two tanks and two air units
  - FOV scan cones and suspicion/alert marks
  - the portrait HUD
  - the Miami beach → park → fortress stage concept
- `expansion/ground/infantry/`: 112 frames over four helmeted bodies, plus 11 pilot palettes.
- `expansion/windstorm_machinists/`: the Machinists rebel tank squad (Wren / Rolf / Chaz) as modular layered tanks, the basis for the next tank level.

`onfoot/SYSTEMS_NOTES.md` is the contract. Normal on-foot play is **one damaging hit = death**, so there is no health bar.

## 4b. 1008f repair: art lost to the 1006 asset cleanup

The October 6 cleanup moved `retired_rigs_2.png` into the local-only `UNUSED_ASSETS` archive. Level 2 drew three families from it, so they went invisible:

- turrets (`nlgt_`)
- cameras (`nmrv_`)
- the player LASER (`nql_laser_`)

The fixes:

- Turrets now use the on-foot turret set (`oft_north` / `oft_fire` / `oft_damaged` / `oft_wreck`). Those plates are authored facing north, and the fire frame faces east.
- Cameras use its dome (`oft_base`).
- The laser uses the game's own `eglaser_*` bolt reel.

The probe now records every HTTP ≥ 400, so a missing sheet names itself.

## 4c. 1008g-j: Level 2 wears the Overdrive ground art

- **Player tank.** The player drives the ground pack's tank for the chosen pilot: siege for Juggernaut and Phoenix; panzer for Lizzie, Falva and Hotwire; assault for everyone else.
  - Paints are baked offline by `_research/bake_ground_tanks.py` into `art/tanks/`. It uses the pack's own rule: only cobalt panels change, and no pixels are read at runtime.
  - The hull and turret share a 192 px canvas. The pivot is the hull centre (96,124).
  - The damaged hull shows below 40% armour, and death leaves the pilot's wreck plate.
  - Pick the pilot with LEFT/RIGHT on the briefing. The choice is kept in `localStorage`.
- **Enemy tanks** are the on-foot pack's alien tanks:
  - scout and rifle use the light tank; heavy and sniper use the heavy tank
  - movement alternates the idle and tread frames
  - fire, damaged and wreck each have their own frame
- **Ordnance and effects.** The cannon shell, the AP shell (charged), and the muzzle, impact and destruction reels all come from `ground/fx`. Crates are the ground pack's ammo and weapon crates: closed, then open, then broken.
- **Treads.** The ground pack ships its player tracks unanimated (its README says so). The player tank's treads therefore do not scroll yet.
- **1008h path move.** `12dc7982` moved assets into per-stage, per-pilot and shared folders. `_research/repath_1008h.py` follows it.
  - The old boss track `Unused_UnknownBossTheme.mp3` was archived on 1007, so the boss now plays `Unused11.mp3`, an old stage-2 boss mix. Mike's call to change.

## 5. Running it

1. Serve the `BulletsOfFury` folder. The `bof` launch configuration uses port 8712.
2. Open `http://localhost:8712/expansion/topdown/index.html`.

The page loads `../../assets/manifest.js`, so it **must** be opened from inside the BulletsOfFury tree.

**Controls** (the 6-button scheme):

| Key | Button | Action |
|---|---|---|
| J | A | main gun |
| K | B | cannon |
| L | C | hold to strafe |
| H | X | hold to charge a piercing shell |
| U | Y | smoke |
| I or the mouse wheel | Z | swap weapon |
| Enter | Start | pause |

Gamepads work as well. In menus, any face button confirms.

**Testing.** `_research/probe_topdown.py` runs the level in real Chromium with real key events: 19 checks, and page and console errors are counted. Its proof frames go to `_proof/`.
