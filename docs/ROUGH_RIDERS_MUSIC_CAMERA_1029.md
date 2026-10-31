> October30 music correction: Mike explicitly selected original Gasline. See RIDERS_ROLL_TYPE_MUSIC_1030.md. The standard Stage6 boss assignment below is superseded; steady-camera behavior is retained.

# Rough Riders: standard Stage6 boss music and steady framing — October29

Mike clarified that this encounter should use **Stage6's standard boss recording**, not its regular stage music. The existing H3 owner unconditionally redirected every rebel encounter to the StageX event. RR43 now registers a narrow roughriders6 event pointing at BOFA.music.boss6 (currently assets/game/levels/stage_06/audio/music/Level6b.mp3). Stage6's five-ship Rough Riders encounter alone maps incoming boss/stagex/rival requests to that event before the legacy redirect. Real StageX continues its currently configured ghostrider_1028.mp3 source. Standard Harrier/Nightwing music and other stages retain their owners. No audio was reprocessed or generated.

Warmup, repeated requests and recovery now agree on the same recording. Repeated starts preserve a healthy transport; a paused current element resumes directly rather than restarting/seeking it. Native gain, looping and cue/SFX owners remain. Native decoded waveform and actual source URL were verified, including pause/resume and leaving this encounter's scope.

RR43's scoped draw owner removes impact shake during the complete Stage6 Rough Riders encounter, including intro, combat and native death drawing. Raw impact state is restored after rendering; physical ship recoil, hit flashes, attacks, projectiles and health simulation continue. Horizontal tracking ignores12world-pixel pilot bobs, eases by elapsed time and limits travel to180world pixels/second. It retains the full native horizontal arena and does not add zoom or teleport the camera. Other encounters keep their normal camera behavior.

## Measured evidence

18 native checks pass: actual root matrices are invariant under repeated large impacts during airshow/dialogue/combat; render preserves raw impact state and HP; accepted ship flash/expiry; bounded pan; decoded correct standard boss MP3; audible waveform; repeat requests and paused-clock recovery; real StageX music/camera scope and independent Harrier camera; no page/draw errors.

Fresh **150.12s** native Furious GOD/input-bot footage reaches real squad defeat at **58.53nativefps**. Enemy HP, phases, attack timing and health changes are native. Every observed active-fight music source is the standard Level6b.mp3 recording with the StageX element paused. Every observed root matrix has no impact translation: horizontal offset equals native camera X and vertical offset is zero. The film retains all five actual opponents and native allies. Recorded mean-18.8dB / peak-2.9dB. 17 film/player checks pass, including all refreshed cards and actual moving-video/audio decoding. Old downloaded and prior local videos remain intact.

The existing local full Rough Riders card and its related chapters now point at the new movie. Pilot chapters are live squad-combat windows while each pilot is present; they are not isolated demonstrations. Evidence and raw recording: C:/Users/Mike/Documents/New project/BOF-Rough-Riders-Music-Camera-1028/.

Syntax passes. Required full suite reaches summary with the same five baseline failures (exit1): single-hit flash duration, opening-jump dialogue warning, opening jump return before Chromium, opposite StageX route persistence, StageX right full encounter. No assets/game.js or _BUILD_SOURCE/test_fl.js edits.

Preview: http://127.0.0.1:51046/?riders=boss6-steady#clip=stage6-rough-riders

Owner: assets/rough_riders_steady_1028.js, loaded last in index.html. No commit or GitHub upload.
