# Stage6 Fortress: passive fans and red reactor — October28

The Stage6 miniboss now has **two passive turbine modules and six laser batteries**. All eight must be destroyed before the existing animated reactor aperture opens. Protected body pixels do not stop player fire; bullets, beams, splash and Retina resolve real live parts. Destroyed fans lose their targets and retain anchored authored fire/smoke. Accepted fan hits show an authored white silhouette and expire naturally.

The complete original difficulty/co-op HP budget is preserved: each fan10%, each battery7.5%, the reactor receives the rounding remainder (about35%). Furious solo remains1950HP. Damage accounting sums all eight live part pools and core; repeat hits on wrecks do nothing. The native miniboss reward/death lifecycle is retained.

Front batteries retain their independent red laser patterns, charge sound, FOV, collision width and destruction cancellation. Fortress missile start now returns to recovery. The exposed core exclusively alternates committed five-bolt spreads with two lightning-orb pincers. Both emit from the actual moving aperture. Lightning has .85s Furious /1.15s lower-difficulty anticipation, .85s recovery, native charge and electric release sounds. The former generic Fortress barrage is disabled so two reactor books cannot overlap. Core energy cannot be intercepted, including its first update; death cancels its rounds and warnings. No fan launches any attack.

The existing screenshot-matched eight-frame branching lightning and sixteen-frame electric orb are palette-authored red in Aseprite. Four emissive value steps implement the1015-style pulse in the pixels themselves. Bolts have32 offline direction variants; runtime selects the nearest direction. Orbs have16 fixed72x72 cells. Bolts use152x152 cells with shared pivot and transparent gutters; no runtime tint, alpha animation, filter, rotation or per-frame scale. The core has12 red pulse cells and matching hit cells. Fans use16 authored128x128 rotor poses, a wreck state and hit silhouette; the clean hull removes the baked rotor behind each real module. Separate fixed96x144 smoke and64x64 fire banks follow broken turbine sockets. All extents are even. Main Harrier, Nightwing, Rough Riders and the other stages keep their existing owners. The prior solo-miniboss rule remains.

Runtime owner: assets/fortress_red_1028.js, loaded after S6SOLO. Two scoped lines in stage6_carrier_1013.js select the clean miniboss hull and its fan renderer. Aseprite sources, Lua recipe, source snapshots, metadata and runtime banks reside in assets/game/levels/stage_06/miniboss/fortress_red_1028/. The source atlas owners are not repacked. No paid generation credits were used.

## Measured verification

31 native checks pass: all four difficulties, exact budgets, eight targets, normal and continuous hits through body columns, accepted white hit pixels/expiry, both destruction orders, all-batteries-only gate, real fan smoke/fire anchors, no Fortress missiles, both red attack types, non-interception, death cleanup, ordinary mini completion, solo support and unchanged main encounter ownership. Native screenshots and decoded film frames were inspected. No browser/draw/HTTP errors.

Fresh **82.33s** Furious native film reaches real defeat at **58.89 nativefps**. It uses the native invulnerable input-only bot, real HP/phases/timers and no enemy state writes. First exposed-core attack demonstration lasts9seconds through input withholding only. All observed snapshots have zero NPC allies and zero Fortress missiles. Both red core books appear. Recorded audio mean-20.0dB / peak-3.6dB. 13 film/preview checks pass, including actual local playback, seeking and decoded audio. Earlier downloaded and solo movies remain intact.

Syntax checks pass. Required full suite reaches summary and exits1 with the same five baseline failures: single-hit flash duration; opening-jump dialogue warning; opening jump return before Chromium; opposite StageX route persistence; StageX right full encounter. No edits to assets/game.js or _BUILD_SOURCE/test_fl.js.

Preview: http://127.0.0.1:51046/?fortress=red-core#clip=stage6-miniboss

Evidence: C:/Users/Mike/Documents/New project/BOF-Fortress-Red-Core-1028/. This local change has **not been committed or pushed**.
