# Luminaire: thrown red plasma mine and rising half-dome

RD97 replaces the old filled warning and screen-flood Luminaire graphics in Dracodia's final main life. One native ground Retina marks a committed landing point. Dracodia charges his chest, throws a visible orb onto that point, and the orb becomes an expanding red plasma mine. Its bright red pixel glow pulses continuously. It detonates into an upward-growing plasma half-dome; the player escapes by flying north above the rim. The dome is the actual attack, with no separate filled FOV overlay.

## Timing, geometry and ownership

The landing point is world center, 46px above the bottom (340,466 on the native 680x512 world). It never follows the player after committing. Chest charge lasts0.90s, throw0.72s, then harmless mine arming lasts2.00/1.80/1.65s on Normal/Hard/Furious. The player has3.62/3.42/3.27s before detonation. The orb curves from the current chest socket into the mine, which grows from100 to164px while remaining rooted at the landing point.

The dome rises over1.35s, crests for1.05s and collapses through0.80s of authored frames. Each rise frame has matching analytic damage metadata; final inset damage extents are394.61px horizontally,376px vertically and64px below the base. Collision stays inside the bright rim. There is no hidden safe strip at the bottom. The upper band around y70 is reachable with ordinary movement and remains safe through the cast's end. Dracodia's casting position is lowered to55% of screen height so his crown cannot block that escape route.

The existing RD78 attack discriminator remains authoritative. Native RD88 two-claw-combos-then-Luminaire selection, whole-part hit masks/white damage frames, HP, life/copy protection, arm destruction, cancellation, death and retry owners are retained. Only rise/crest can hit, once per live seat per cast, through native playerHit. Pause freezes all phase clocks. Native charge, launch, landing and wave sounds accompany the actual events; cancellation stops the long charge/wave voices.

Ordinary bullet interception rules and retired bullet-attached asterisks are unchanged. This attack uses a native ground Retina, not a projectile asterisk or geometric FOV.

## Runtime, editable art and generation provenance

- `assets/luminaire_plasma_1031.js` owns this final-main-life sequence and delegates the remaining renderer/combat owners.
- `assets/luminaire_plasma_art_1031.js` and `assets/game/levels/stage_08/boss/luminaire_plasma_1031/` register192 authored frames in seven even fixed-cell banks: chest charge32, flight24, mine32, rise40, crest16, collapse24 and native Retina24. Large pages stay below4096px. The original old field pages remain archived but are no longer queued.
- `_ART_SOURCES/luminaire_plasma_1031/` retains both unmodified generated originals, exact generation prompts, seven editable Aseprite files and the review plate. The runtime folder also retains source inputs, manifest, pivots and authoring Lua.
- `_BUILD_SOURCE/build_luminaire_plasma_1031.py` reproduces every runtime PNG exactly from the saved sources. Proportional resizing, fixed bottom pivots, pixel glow, texture motion and fades are baked offline. Runtime rendering is fixed frame blits without sprite scaling, rotation, filters or animated alpha.

**Generation tool/mode:** built-in `image_gen.imagegen`, two new images, `transparent_background=true`, no reference uploads. No PixelLab credits were used for this pass. Exact full prompts and tool options are saved in `_ART_SOURCES/luminaire_plasma_1031/generation_prompts.json` and copied into the QA JSON.

Original tool outputs:

- Orb: `C:/Users/Mike/.codex/generated_images/01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f/exec-338f6d8c-a703-407e-b7f9-8f1abd07b448.png`
- Dome: `C:/Users/Mike/.codex/generated_images/01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f/exec-91ae79a3-ab61-40bf-aa12-1917c5201b37.png`

Saved project sources: `_ART_SOURCES/luminaire_plasma_1031/generated_orb.png` and `generated_dome.png`. The generated artwork is used for the actual mine/detonation; the approved native HL51 green/yellow/red ground target supplies the only warning.

## Verification and real-engine footage

47 focused/source/rebuild/playback checks pass:37 native/frame checks,4 source/provenance/rebuild checks and6 browser playback/bookmark checks. Cole, Juggernaut and Yuri reach the upper escape on Normal, Hard and Furious with no invulnerability, speed, armor or shield upgrades. The cast's end is included. Stationary center and bottom positions invoke native death. Tests also exercise fixed landing, harmless arming, monotonic growth, hit geometry, pause, cancellation, audio stop, native attack book, arm destruction, native final defeat and retry. New banks draw; the old warning/blast/recovery draw zero times. No browser, asset or rendering errors.

Fresh native Furious final-main-life film:145.177s,1280x800,30fps capture,55.51 average native simulation fps. The checkpoint begins at full5330HP with intact limbs; preceding copied lives are cleared before capture. Cole uses an invulnerable input bot with native weapons and movement. No HP/phase/timer writes occur during filming. Five real mine casts, actual health depletion and native final-main-life defeat are recorded. There are zero mine contacts while the bot flies north. Audio mean-21.6dB / peak-5.5dB; complete decode is clean. Actual native and decoded movie frames were visually reviewed.

- [New Luminaire attack chapter](http://127.0.0.1:51046/?luminaire=red-plasma-mine-1031#clip=stage8-dracodia-luminaire)
- [Full current final main life](http://127.0.0.1:51046/?luminaire=red-plasma-mine-1031#clip=stage8-dracodia-ninja)
- [Native claw combos into the mine](http://127.0.0.1:51046/?luminaire=red-plasma-mine-1031#clip=stage8-dracodia-ninja-combo)

Existing Luminaire and ninja-combo bookmarks point to this recording. Older clips are retained and labelled as previous. This film does not claim to re-record the first host, copied lives or other bosses. The local preview video is `C:/Users/Mike/Documents/New project/BOF-Downloaded-Stage6-9-1028/videos/stage8-dracodia-plasma-mine-1031.mp4`.

Reusable native test/recorder: `_BUILD_SOURCE/test_luminaire_plasma_1031.py` and `record_luminaire_plasma_1031.py`; outputs go under `_shots/luminaire_plasma_1031/`. Evidence and exact checks: `docs/qa/luminaire_plasma_1031.json`.

Syntax checks pass for the new runtime/art registration and core game. The required full `test_fl.js` suite completes with exit1 and the same five pre-existing failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

Core `assets/game.js` SHA256 remains `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`. No Git commit, push or video upload was requested or performed for this correction.
