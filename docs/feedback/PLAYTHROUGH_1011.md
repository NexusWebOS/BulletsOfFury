# October 11 full gameplay review

Source: `C:/Users/Mdogg/Videos/2026-10-11 12-24-48.mp4`, 65:54.367,
1280 x 720, 30 fps. SHA-256:
`23bd7a46942a982c4f42ad4047fc187f4adce3f429b30c41e6dfa77e9bb49a1f`.
Maverick, Furious, campaign plus encounter passwords. The complete audio was
transcribed locally; 198 captures at 20-second intervals cover the timeline.
Targeted audio rechecks and action captures supplement that overview. This is
a timestamped commentary and gameplay review, not a claim to have watched
every frame. Source audio, word timestamps, alternate decodes and pictures
are retained under ignored `_shots/playthrough_1011/`.

The main implementation pass is installed locally. Mike selected **Armored
Command**, and clarified that **11:26 refers to pellet travel speed**. Normal
spread now travels at 5.6 instead of 7.5 units/frame (336 instead of 450 px/sec),
with the same firing cadence, damage and fan. Maverick's homing lances remain
fixed Level I. At 41:34-41:43, Mike confirmed removal means **only the two
specific small planes shown**, not every small green Stage 6 aircraft.

Interactive review: [frames, onion controls and native captures](../previews/playthrough_1011/index.html).
The request ledger below preserves the source requirements. Implementation
and verification dispositions follow it; outstanding items are explicit.
The regular FOV correction and nine-element arsenal preceded this review.
No commit or push is authorized by this recording alone.

## Request ledger

| Time | Requested result | Verification needed |
| --- | --- | --- |
| 00:27-02:14 | Remove the split/duplicate startup logo. Generate ColeForge credit banners and a graphical fullscreen control. Local launch should open fullscreen; browser launch needs a working user-gesture button. Fit side housings without black gaps or stretched art. | Browser fullscreen gesture, native launch configuration, multiple aspect ratios. |
| 02:20-02:44 | Animated thrusters in the introduction; slide all nine pilots across as a roster before the title. | Actual nine pilot/ship identities; stable plates and thrusters. |
| 03:04-03:19 | Show all achievements without requiring a filter switch. | Fresh profile and earned/locked achievements. |
| 03:20-04:08 | Document multi-retina and support mouse side buttons; coherent six-button keyboard layout. | Real mouse/keyboard bindings, Help and existing controller prompts. |
| 04:08-04:18 | Rework and center Credits in a proper authored window. | Native menu at narrow/wide sizes. |
| 04:24-04:40 | Fix cropped mode locks and translucent remnants on buttons. | All locked/unlocked mode cards. |
| 04:47-05:01 | Continue means the current browser-session run, not a saved run after fresh boot; Load/Save remain separate. | Fresh boot, suspended run, explicit loaded save. |
| 05:08-05:19 | Difficulty portrait faces point right, like Cole on Furious. | Inspect actual generated button portraits. |
| 05:28-06:42 | Pilot select: move full pilot left, show a large actual ship, larger named affiliation emblem and visible special icons. List Decker's Cloaking System/Incendiary Shotgun, Juggernaut's Wrecking Ball/Charge Dash, Lizzie's Atom Bomb, Falva's Roller Ball, Cole's Sonic Boom/Nuclear Warheads. | All nine selected pilots and locked tenth slot. |
| 06:50-07:20 | Keep approved opening scene plates static; remove the moving car/planes and added explosions. | Original city/naval scenes. |
| 07:24-07:57 | HQ news/briefing uses established characters, pilots and ships. Fix NO SIGNAL placement. Preserve the threat's mystery. | Actual character reference exports and opening playback. |
| 08:19-08:51 | Animate cockpit radar/audio, keep the pilot's helmet appearance, speed up takeoff, animate only thrusters on the ship. Use the actual BOF logo, type-on/audio and fired MG rounds for the title flight. | One continuous opening/takeoff. |
| 09:25-09:34 | Remove the abrupt ship/camera shrink and jump at stage start. | Campaign map to countdown to play. |
| 09:35-09:49 | Install the more readable new HUD with top stocks/score and no radar. | Mike selected **Armored Command**. Live P1/P2 counters and all game layouts. |
| 09:58-10:12 | Bullets should not be shootable; investigate the reported firing/scroll interruption. | Narrow action replay and actual collision owner. |
| 10:18-11:18 | Stage 1 planes approach and fire purposefully without excessive wobble. Spread projectile animation must stay stable. | Actual stage waves and equipped spread tiers. |
| 11:26-11:52 | Slow the excessive attack tempo and remove the jerky special-animation restart. | Identify the displayed attack and inspect its entire loop. |
| 13:31-14:20 | Sonic reward/ordnance must read as sonic; stop preview audio leaking into the next menu; keep the revealed antagonist's face concealed in the cinematic. | Native Forge and inter-stage cinematic. |
| 15:16-15:22; 20:11-21:01 | Maverick defaults to fixed-tier homing lances; his selected form survives stage changes. Preview homing lances correctly; hide Fire Whip until actually forged. | New run, pickup, Forge selection, next stage and save/load. |
| 15:35-15:46 | Mike withdrew the Sonic-slug complaint after identifying the white slugs. | No change requested. |
| 16:12-16:42 | Reduce Stage 2 miniboss barrage overload and avoid stretching fire effects. | Furious tell/release/dodge windows, proportional art. |
| 18:01-19:03 | Furnace's relevant attack should emit a fire wave; improve the head-phase animation. | Physical emitter, stable animation and complete phase. |
| 19:47-19:52 | Forged flamethrower needs to feel like an upgraded version, not its ordinary stream. | Current elemental arsenal versus recorded build. |
| 21:05-21:21 | Replace disliked small ice enemies with distinct ice-ship variants and better projectiles. | New art, actual waves, facing and attack participation. |
| 22:29-25:34 | Regenerate Stage 3 miniboss with a distinctly different design and improved lasers/animation. Move the former too-similar design into Stage 8 as a tougher enemy. Warn the boss's emitted attacks. | Modular hardpoints/death, current boss unchanged, native waves. |
| 26:50-27:38 | Olive Warden charges at its nose; alternating MGs visibly track through the normal FOV and fire from charged physical muzzles. Improve its janky attack motion. | Left/right attack sequence and locked aim. |
| 27:53-28:10 | Restore regular enemy reinforcements during that fight: none Easy, one/two Normal, stronger waves Hard/Furious. | Rank-specific spawns with finite lifetime. |
| 28:35-30:42 | Storm generators visibly spin/light and energize the shield. Core cannon needs darkening, sound, asterisk/FOV. Use lightning balls, faster missiles, stationary objectives and damageable helpers. | Generator break, helper damage, warning and actual projectiles. |
| 30:48-31:54 | Replace the 25% shield reformation with a south exit/northbound chase, scattering lightning balls while escaping. | One finite, beatable final chase; no 25% rearm. |
| 32:21-33:10 | Space miniboss: improved modular cannons/animation, meaningful attacks and correct HP/death threshold. Remove the demonstrated unsuitable attack; passing above must not trap the player. | Targeted footage, actual damage pools and movement bounds. |
| 33:49-34:46 | Hammer forms chromium armor, raises/charges the hammer, then jumps. Animate energy within the actual core; remove the separate disc pasted over it. | Whole authored plates and shield-to-jump sequence. |
| 35:38-36:10 | Hammer must return from offscreen promptly; shorter electrified recovery, visibly ghosted/invulnerable while recovering, no easy damage exploit from above. | Every camera edge, recovery damage gate and return timeout. |
| 36:48-37:13 | Chaingun withstands more damage, visibly tracks/guns the player. Destroying it drops the chain part immediately; Decker asks the player to bring it home intact. | Actual module break/reward exactly once. |
| 37:21-38:14 | Countering the upper safe area should slide into a side hammer swing, not jump out. | Supersedes October 11's earlier upper-half jump request; fixed physical hammer arc. |
| 39:40-43:34 | Stage 6: bomb release after the incoming tell, active enemies, south-facing approaching jets, remove the identified yellow pods/tiny planes, restore allies and a progressing encounter. | Identify each shown unit; full stage route cannot stall. |
| 44:49-46:15 | Stage 7: replace the nonsensical shown attack, shorten idle-before-fire, remove the humanoid walking enemy, give the shown heavy units complete attacks. | Targeted sprites and actual waves, no guessed removals. |
| 47:34-48:37 | Portal continues animating until it closes/disappears. | Opening, held loop, closure, no frozen plate. |
| 50:30-53:43 | Final approach/phase one must challenge a firing player. Drone levitates and raises arms, portal opens behind it, pilot reacts, symbiote consumes it and mutates under a black void. Body form makes warned claw rushes; attached arms never detach for attacks; grab/fling causes an acted ship death. | Full natural intro and body attack cycle; maintain two attached arms. |
| 52:15-54:45 | Actual shoulder/eye weapons charge with darkening and sound, target with retinas, and emit strong beams/alternating circular volleys. Living eye moves/glows. Give phase enough HP to show its attacks. | Muzzle positions, matched collision, difficulty progression. |
| 53:50-54:19 | Raised-arm download animation, visible 0-100 progress and animated glowing code wall. | Barrier formation, active code, damage/recovery. |
| 54:52-55:44 | Defeated body spins/falls/burns/breaks apart. Pieces of black symbiote rise from below, gather into a beating black heart, then mutate into the ghost. No portal for this reformation. | Sequential death and regrowth with no abrupt replacement. |
| 55:50-58:04 | Fix multi-retina on the ghost. Add portal teleport/fast warned claw rushes; ghost helper can download a ghost-colored code shield; eye/orb lasers and sufficient phase HP. | Independent helper, lock validity, active attack cadence. |
| 58:10-58:42 | Final transition portal accelerates and expands from its existing location to blacken the entire view, then reveals the alien arena. No restart/pop-in. | Continuous time/anchor and full scene transition. |
| 58:54-59:25 | Dracodia's dialogue window stays stable and uses a red border. | Native monologue, original portrait animation retained. |
| 59:25-65:54 | Final copied forms need forceful whole-arm attacks, upgraded aggressive versions of their original boss behaviors and better animation. Take time on the final boss before release. | Final audio recheck and every copied form's live tell/attack/recovery. |

## Current verification baseline

Before this pass: 8,670 assertions, zero failures, full suite final summary and
exit 0. Preserve existing local work and register generated assets through
their owning builder. Frame sizes stay even, with common proportional scale
and fixed physical pivots. Fresh native Chromium evidence is required for
every changed gameplay/rendering path.

## Installed changes and evidence

| Recording scope | Local result | Evidence |
| --- | --- | --- |
| Startup, HUD, menu and pilot select | Single boot logo; authored ColeForge plaques and fullscreen control; selected Armored Command with large lives/missiles and no radar; current-session Continue; corrected lock placement; larger pilot/actual-ship panels and special labels/icons. | Native runtime: five viewport sizes, real fullscreen enter/exit, independent co-op inventories. All nine pilot cards captured wide and narrow. |
| Controls and opening | Multi-lock remains a separate bind; Help identifies side mouse buttons. Approved intro plates stay static; roster and thrusters animate. Cockpit uses authored radar and hand art; title flight uses actual ship and BOF logo. | `ui/help.png`, `cockpit-live.png`, `title-flight.png`; native UI checks. The complete control-remapping workflow was not retested. |
| Stage entry, 09:25 | Launch and play resolve the same neutral ship pixels. No scale discontinuity. | All nine pixel comparisons pass; actual Stage 1 transition: ship height remains 60 px, zero off-scale draws. |
| Spread, 10:18-11:52 | Slower pellet travel; stable projectile plate; Stage 1 evasions commit to a side instead of flipping every frame. Maverick's authored 32-pose ball returns through its poses instead of jumping from frame 31 to 0; charge/release shares its animation clock. | Native spread and dodge checks. Existing authored ball bank retained. |
| Forge/Maverick, 13:31-21:01 | Preview cues stop on leaving. Default fixed-tier lances, explicitly selected beam/lance form preserved, real lance simulation in preview; Fire Whip hidden until forged. Satellite reveal keeps the antagonist faceless. | Native pickup/form/audio checks; two generated mystery plates in review. |
| Stage 2 | Furious miniboss barrage reduced to 18 staggered meteor shots. Furnace flame attack emits physical travelling crescents; core beam remains continuous. Sixteen new head poses. | Native crescent positive/negative collision checks, head-bank capture and release capture. |
| Stage 3 | New six-part cryogenic carrier kit; four independently damageable weapon modules with matching physical muzzles. Two separate sixteen-pose ice-jet banks. Prior carrier moved to Stage 8 as a 455-HP Furious regular heavy with a finite withdrawal and no miniboss route hold. | Native independent cannon break, heavy attack progression and departure checks; carrier and ice-jet/onion captures. |
| Stage 4 | Olive reinforcements restored by difficulty (0 Easy, 2 Normal, 3 Hard, 4 Furious). Storm's generators remain fixed while the hull moves; lightning attack uses charged core warning/release; final quarter becomes a finite south-exit/northbound chase with no shield refill. | Regression plus native charge, fixed-generator, pursuit and damageable-return checks. |
| Space miniboss | Sixteen authored cannon poses, independent cannon HP and retina targets; broken cannon ceases firing; upper route remains open; survives below 30% HP. Existing live attack book already uses sequential lasers rather than the demonstrated crossed rotor pattern. | 60 seconds of native attack selection covers warp, plasma, missile, side fire, beam and salvo; positive module damage tests. |
| Hammer | Sixteen whole boss plates for core energy/raise; shorter invulnerable recovery with prompt return and no healing. Stronger chaingun; immediate one-time salvage and Decker line; upper-half counter is a full-scale side slide. | Native recovery damage gate, independent part reward/pickup and committed side-slide checks. |
| Stage 6 | Removed the identified yellow Storm Buoy. Approaching L6X fleet now faces south. Bomb release waits for its full warning, then has a separate flight interval. Allies restored through the regular director. | Native warning/release/impact checks, actual south-facing sprite gallery, ally spawning check. The two tiny green shapes strongly match rotating loose missile-ammo drops; pickup disposition is awaiting clarification. No broad aircraft removal. |
| Stage 7 | Retired the humanoid Walker. Hellram finishes a warned charge, retreat and six-shot aimed burst; miniboss pressure salvo uses its living physical cannons instead of the old wall row. Portal loops through closure. | Native complete Hellram sequence and twelve physical-muzzle pressure shots. |
| Drone/body form | Sixteen two-arm drone raise poses; symbiote consumption, pilot reaction and body emergence. Higher phase HP, attached-arm rushes, short physical claw grip followed by existing burning-spin death. Raised-arm download shows 0-100 progression and a code barrier. Red beams/rounds begin at the measured cannon mouths. | Native takeover, shield progress, muzzle placement and shield-respecting grip/death checks. |
| Body-to-ghost and final transition | First defeated body falls/burns, then reforms as a beating black heart and ghost without a portal. Stable ghost multi-lock IDs and spectral helper barrier. Second portal carries its original position/clock into the full-screen arena transition; stable red monologue border. | Native heart-to-playable-ghost, lock identity, helper shield and continuous second-portal checks. |
| Final copied forms | Attached physical arms, committed target, live emitter/damage ownership, source recovery scheduling and stronger copied signatures. Hammer copy keeps the native Hammer controller. | 154 native checks across Normal/Furious forms, including positive collision and an ordinary slow-ship dodge. These are bounded fixtures, not a campaign-clear or human-balance claim. |

## Generated art and registration

`build_playthrough_art_1011.py` owns 166 loose PNG cells: ten sixteen-pose
banks plus six carrier plates. `build_playthrough_cinematics_1011.py` owns two
faceless satellite plates. The HUD builder uses the selected authored Armored
Command concept. All shipping cells have even dimensions, one physical pivot
and common proportional scale per bank; no hull warping or synthetic poses.
Measured unequal row gutters prevent neighboring hands/horns leaking into the
Hammer, Furnace and drone frames. The drone uses padded 320 x 320 cells so both
lowered and raised hands fit without changing its physical drawing scale.
Sources, prompts and measured registration are in `_ART_SOURCES/playthrough_1011/`.

The 13:31 Forge capture confirmed that Sonic Spread was drawing gold cartridge
sprites. It now draws a 16-pose pressure-wave bank. The 19:47 capture confirmed
that Blast Furnace reused the ordinary fire stream. Its new 16-pose flame has
one registered nozzle, a proportional drawing and 22% extra visible reach.
Opaque contact bands are measured from the same authored frame, so it hits
within the visible flame rather than an unrelated rectangle. The normal fire,
Ice Breath and other elemental owners remain separate. These two banks came
from built-in image generation; exact prompts are in `weapon-prompts.json`.
Native Forge comparisons and actual positive/negative contact checks are in
the review. All 81 elemental combinations still hit native targets and retain
their element; Maverick's homing lances remain fixed Level I and uninfused.

## Verification result and remaining work

The final regression suite reaches **8,700 passing assertions, zero errors,
exit 0**, versus 8,670/0 before the pass. Superseded Walker/buoy roster and pilot
special-name assertions were updated to match the requested content; failures
were not suppressed. Native recording probes: **97 checks pass**, copied forms:
**154 pass**, elemental matrix: **32 checks / 81 combinations pass**, no page/console/asset errors in these
probes. See [the recorded results](../qa/playthrough_1011.json), including the
exact scope, owner hashes and command paths. A scratch identity trace needed
an instrumentation correction; its initial error was not a game failure.

- **41:34-41:43: only the two shown shapes.** A second trace with firing and
  actual green-pixel sprite inspection strongly matches these to rotating loose
  missile-ammo drops: `msl_2_2` is Maverick's assigned missile; the drop renderer
  spins it at a small 18-pixel height. This also agrees with the recorded
  MISSILE+ pickup message. Asked Mike whether to replace the pickup art or
  remove loose Stage 6 ammo drops; other aircraft were preserved. Native
  sources/gallery: `_shots/playthrough_1011/identity/green-keys.json` and PNGs.
- **09:58-10:12 firing/scroll interruption:** not reproduced in the current
  build. Ordinary pellets are verified unshootable; this does not establish
  what caused the recorded interruption.
- **Balance and complete progression:** protected encounter fixtures do not
  replace a full campaign playthrough. Stage 6 branching progression and the
  entire final boss still need that review before release.

No commit or GitHub upload was made. Existing unrelated local work is preserved.
