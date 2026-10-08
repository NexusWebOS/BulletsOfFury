# On-foot infiltration — systems to build later

This package contains graphics and an art review page. It adds no playable level, collision, combat, AI, inventory, save-state changes, or campaign transition to the engine.

## Mission and stage structure

Travel north from Miami's coastal beach through a palm park with pools to a brick-walled fortress. Breach the gate and advance to the next level, where the route toward recovering the jet continues. Keep the earlier ship crash and Hotwire/Phoenix rescue as their established campaign events; this mission does not replay that introduction. Do not assign this concept a campaign level number until the on-foot detour is placed against the existing bridge, city, and plateau sequence.

The generated stage is a continuous background concept, not a seamless tileset or a finished collision map. It has a coastal road entry, pool courtyards, alternate paths around hedges, tall crate clusters, a fortress forecourt, and a central gate. The independent crate, wall, and gate assets support later construction of a playable version. Pools, surf, hedges, wall heights, gate opening, and walkable margins need authored geometry. Verify player clearance with the intended collision capsule before committing to the painted path widths.

Author ground collision, vision blockers, projectile blockers, cover anchors, noise zones, enemy patrols, spawn points, gate triggers, and checkpoint locations as separate data layers. A crate's drawn height is not its collision footprint. Sort actors against crate/wall bases and use foreground occlusion so a pilot can actually hide behind a tall stack. Full-height stacks block sight; low cover may protect a prone pilot while exposing a standing one. These properties belong to the object definition, not image color sampling.

## Pilot bodies and action graph

Use four helmeted body families: regular male; Juggernaut heavy; Axel/Phoenix athletic; Falva/Lizzie female. The existing manifest also assigns Hotwire to the female family. Eleven pilot palettes remain in `manifest.json`; helmets stay closed and neutral metal/visors keep their colors. Preserve luminous FX when swapping armor. An automatic blue-color filter is only a preview: author armor masks for final integration so roll streaks, revive halos, and sensors are not recolored accidentally.

Movement heading and aim heading must be independent. Standing stationary aim/fire uses existing directional aim poses, weapon sockets, recoil, and the new muzzle effects. Run-and-gun uses the existing north/east/south run strips plus weapon/muzzle layers; west can mirror east after socket review. The new extended sheets are three-frame east-facing candidates, with poses for wall tap, duck-to-prone, crawl, grenade throw, roll-to-prone, roll-to-stand, hit, stun, recovery, death, revive, and powerup. They are not complete directional action sets. North/south versions, distinct sustained crouch movement, held prone aim/fire poses, per-weapon grip variants, and animation root cleanup remain to be authored. Do not rotate the overhead three-quarter bodies as flat decals to manufacture directions.

State transitions to implement:

- Standing/run → duck → prone; prone → crawl while moving; crawl → prone while stationary; recovery returns to standing.
- Standing/run → roll → prone OR roll → recovery → standing. Choose the exit from player intent, with buffered input and a clearly defined commitment window.
- Aim lock → stationary fire; moving fire respects the separate aim heading. Decide whether firing cancels crawl or uses a dedicated crawl-fire pose.
- Grenade windup → release event → follow-through. Spawn the grenade at the hand socket on the release event, not at animation start.
- Wall contact → tap event → return to the prior stance. Emit the noise once at the tap frame.
- Stun → recovery; death → respawn/revive only when the current game rule permits it. Powerup effects should be overlays or short locked states according to later design.

Define stance-specific collision footprints and weapon heights independently of sprite bounds. Roll distance and crawl speed are engine values; the review animation has no authored root motion. Decide roll invulnerability later instead of implicitly granting it. Preserve deterministic action events during frame drops.

## One-hit-kill rule, lives, and revive

Normal on-foot play retains the user's Contra-like one-hit kill. A damaging hit transitions directly to death and consumes a life according to checkpoint rules. There is no player health bar in this HUD. Hit/stun/recovery art can serve enemies, non-damaging EMP/stun events, shielded states if added later, or an explicitly separate alternate mode. It must not silently create a multi-hit player health system.

Revive frames are supplied because requested. Decide whether they represent checkpoint materialization, an ally rescue scripted event, or an optional revive mode. If normal solo play uses only respawn, play the appropriate materialization/recovery frames at the checkpoint. Do not equate a revive animation with a free life. Enemies can have health, armor, stun resistance, and damage stages independently of the player's lethal-hit rule.

## Stealth, wall tapping, and enemy perception

Each enemy needs a facing direction, view range, view angle, alertness state, last-seen position, hearing profile, and suspicion accumulator. Render calm green, suspicious amber, and alert red FOV overlays from the supplied scan frames. The raster cones are presentation art only. Compute actual line of sight with ray casts or an occlusion polygon, then clip the rendered cone at walls and stacked cover. Rotate the cone around its apex; the extracted review images are centered, so author that apex socket first.

Detection must account for posture, range, motion, cover height, lighting if used, and continuous visibility time. Being prone is not automatic invisibility. Suspicion rises during visibility and decays after losing contact; alert enemies remember the last seen location. Define patrol → suspicious → investigate → alert → search → return transitions, including timers and handoff to nearby units. Show question/exclamation marks and last-known-area cues without revealing hidden enemies unless the HUD design allows it.

Wall tap generates a spatial noise event with a position, radius, duration, and category. An enemy hearing it turns or investigates the sound location, rather than knowing the player's actual location. Gunfire, explosions, rolling, moving over noisy surfaces, and breaking crates may also create noises with separate profiles. Specify whether walls attenuate sound. Avoid universal alerts unless an alarm unit actually broadcasts one.

Place patrols and waves as authored encounters. Decide which alarms summon reinforcements, whether alarms can be disabled, and whether combat must be cleared to open the gate. The route should support both sneaking past a patrol and fighting through it where intended; enemy spawning must not appear directly in hidden cover behind the player.

## Guns, ammo, breakable powerup boxes

| Gun | Behavior to implement | Ammo/drop graphic |
| --- | --- | --- |
| Desert Eagle | Powerful aimed single shot; cadence and recoil | Magazine |
| Spread Shotgun | Pellet fan; independently resolved pellet collisions | Shell bundle |
| Minigun | Spool-up, sustained fire, recoil and ammo consumption per shot | Ammo belt |
| Fusion Beam | Beam channel with battery drain; clipped by blocking geometry | Energy cells |
| Napalm Launcher | Arcing/incendiary shot; persistent ground burn zone | Fuel canisters |
| Rocket Launcher | Explosive projectile; splash and impact event | Rocket bundle |

Each gun has a pickup, closed box, cracked box, broken-open box, and matching ammo object. Six colors/pictograms distinguish the contents. Generic supply boxes have closed/cracked/breaking/empty states, and separate ammo crates are included. Use a data-driven weapon definition for fire rate, reserve/capacity, projectile, recoil, sockets, target categories, audio, and drop rules. Balance values remain undecided. Track current and reserve ammunition separately; decide reload behavior before mapping inputs. Empty ammo should not consume a shot or trigger damage. Avoid silent infinite fallback ammo.

Set box contents when spawning the box. A break event spawns its drop exactly once, advances to wreck/open state, and persists the consumed state across checkpoints according to the save rules. Do not reroll contents on each damage tick. Gun acquisition and powerup overlays are distinct from healing; ship abilities become handheld gun behavior without restoring player health.

Grenades occupy a separate consumable slot like ship missiles. Implement throw windup/release, count consumption on successful release, airborne height and ground shadow, fuse, landing, blast, damage attribution, and friendly-fire policy. Grenade arcs can cross certain low cover but should respect tall walls under authored rules. Rocket and grenade blasts use one damage event plus visual animation; napalm uses controlled timed ticks. A sustained beam needs consistent endpoints and tiled/stretchable beam segments; the generated pulse images vary in length and need anchor/segment cleanup before use as a continuous beam.

## Ground enemies and attackable air units

The roster supplies scout and heavy alien robots, a turret, light and heavy tanks, a scout air unit, and a gunship. States include directional/idle poses, firing, damaged, wreck, and candidate turret components. Troops need full patrol/walk/crawl if appropriate, attack timing, hit reactions, and deaths. Tank tread alternates are visual candidates with geometry variation, not validated looping tread strips. Tank body/turret art needs a common mount pivot before modular rotation. Air units need a ground shadow, flight height, firing tell, and ground-target collision projection.

Separate visual altitude from target selection. Define which weapons can hit air units, how a ground aim ray selects them, and how explosive splash interacts with projected footprints. Do not give aircraft ground collision bodies that trap the player. Enemy FOV geometry and fire range are separate. Turret awareness, tank turning speed, armor facings, and robot health are independent definitions, with readable warning effects before lethal attacks.

## HUD and display integration

The portrait HUD has a top weapon/ammo/grenade/radar strip and bottom belt/stance/detection/objective strip. Keep the center transparent. Supply runtime text and icons in the documented sockets. The review mockup displays example values only. Three life helmets are baked into the artwork; extract or mask them to support varying life counts. Keep radar markings distinct from the generated decorative grid.

Measure HUD occupied regions before deciding the playable camera's safe area. Scale to the engine's internal pixel resolution with nearest-neighbor sampling; anchor top and bottom strips independently if the viewport aspect ratio differs. Respect low-ammo, grenade-empty, suspicion/alert, selected stance, and objective-update states. Powerup selection must remain readable in motion and against bright sand/water.

## Art integration work still required

Keep all source masters. The export contains centered preview crops, alpha-preserving atlases, and source bounds. These crop centers are not combat pivots. Author per-frame foot/root anchors, hand/muzzle sockets, prone heading, grenade-release hand location, cover lean offsets, and FOV apex. Stabilize size and silhouettes across the three-frame actions before runtime registration. The heavy sheet had a joined death/powerup fringe; its automatic crop split is explicitly recorded in `verification.json` and needs manual review. Preserve enemy wreck silhouettes and avoid deriving hitboxes from effect halos.

Validate animation timing with onion skins; verify roll endpoints and stance changes at the engine's actual scale. Expand north/south coverage, unify pilot/robot world scale, and separate baked action FX if needed. Use the raster stage for visual direction, then build traversable geometry and reusable terrain assets later. This request stops at graphics and these notes.
