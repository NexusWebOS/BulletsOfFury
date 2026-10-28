# The Rough Riders — flight and combat field guide

Mike requested a webpage explaining all five pilots, their flight patterns and attacks with video previews. The responsive page is `docs/previews/rough_riders_guide_1028/index.html`. Open it through the normal local game server at `/docs/previews/rough_riders_guide_1028/`, or use the review at http://127.0.0.1:63068/.

The guide has five selectable dossiers with actual native portraits/aircraft, the generated crew photo, custom crew typeface, timed video chapters, optional move-label captions, attack tells/releases/recoveries and player responses. It includes the native airshow introduction, shared cruising/barrel-roll evasion and four coordinated missile-turn calls. There are eight playable videos (seven fresh previews plus the prior entrance), approximately195 seconds total.

## What the current build actually does

- Voss / Iron Vulture: turbo pursuit/side passes, charged straight rush and north return, shared aimed energy shot.
- Nyx / Ghostknife: spectre cloak, native Retina/missile reveal, shadow-charge retaliation, recovery/recloak. Furious emits three pulses; the latest shared round gate reduces each requested fan to one charge.
- Rook / Breachhammer: fixed-position dual chaingun, aimed lock, alternating sockets and30 Furious slugs. The current override maps his hook/ram selections to this same special.
- Kaia / Signal Wraith: teal roller gatling;8/12/14/16 rounds by difficulty, with finite timing, destructible rollers and side ricochets. The older five-way fan is not her current attack.
- Jace / Razorjack: swerve Helix, destructible6HP ball with native counterburst, charge dash and shared aimed energy shot.
- Squad: physical Retina-guided missile volleys, north/south split and continuous return. Star/Bowling/H/X currently share one staggered combat layout. The new introductory bowling layout is independently correct.

The page clearly distinguishes current behavior from suggested next decisions: restore Rook's distinct options; separate formation geometries; decide Kaia's final spread/roller identity; finish Nyx's dark-purple shadow vocabulary. No proposed change is presented as implemented.

## Evidence and limits

Fresh previews use the actual native game update, renderer, authored art, effects, collision objects and shared audio at normal speed, Furious, with a GOD observer. Selection order is scheduled for inspection. Other pilots' automatic attacks, allies and supply scenes are held back. Reveal and Helix interception use the native event handlers at labelled moments. This is a controlled move exhibit, not an unassisted playthrough or five full individual clears. No enemy HP/attack-phase clocks are rewritten during the takes; native counterburst/evade damage may change HP.

58 native film checks pass: meaningful frame rate and decoded pixel change, audible unclipped audio, no page/console/HTTP/audio-tap errors, signature kinds and charge/release/recovery, Voss rows/return, Nyx cloak/reveal, Rook burst size, Kaia burst count, Jace counterburst, all four fleet calls with missile/scatter/return, and all five native evades. Decoded frame contacts were inspected.

84 webpage checks pass: all five identity switches, video metadata/audio/frame decoding, byte-range requests, three seek points for all eight movies, every pilot chapter, keyboard controls, deep links, mobile playback, no narrow-screen overflow and no page/console/HTTP errors. Desktop and390px mobile screenshots inspected. Full game suite was not rerun because this task makes no runtime/gameplay edits; the previous pass records its five existing baseline failures.

Initial frozen-stream and partial-audio takes were rejected and retained only in the local work folder. The published page contains the audited replacement takes. Runtime source hashes remain exact. No game.js/test_fl.js edits, commit or push.

Portable page builder: `_BUILD_SOURCE/build_rough_riders_guide_1028.py`; native capture tool: `_BUILD_SOURCE/record_rough_riders_guide_1028.py`. Capture evidence/source hashes, raw recording reports and public-page QA accompany the page; aggregate report: `docs/qa/rough_riders_guide_1028.json`.
