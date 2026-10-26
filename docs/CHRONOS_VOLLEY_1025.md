# Chronos red-rage palm volleys — October25

Mike supplied two Vegeta firing GIFs and requested laser volleys from both foreground and background. This adds attacks to the permanent15%-HP red rage form; it does not replace the existing red/white wave or restore the hammer.

Final owner `assets/chronos_volley_1025.js`, after C31. Native rotation: foreground barrage at1.08 scale, smooth retreat to background barrage at.42, existing background energy wave, repeat. Each barrage has three warned groups of six alternating discharge beats; beats3 and6 fire both palms. Targets lock before each group. Existing green/yellow/red FOV, native hammerLaser projectiles/oriented collision, actual damage, shared alien laser sound with retrigger gate, and silent simultaneous partner are retained. No delayed fire/audio callbacks survive the owner. Background bolts grow into the same10x54 collision/render dimensions as foreground bolts. Rage body remains shootable through its actual current scaled alpha, with native flash/expiry.

## Whole-body art

GPT supplied distinct left-palm, right-palm, dual-palm and guard keys, referenced to the approved red Chronos actor. Source `_ART_SOURCES/chronos_volley_1025/palms-gpt.png`. Measured pelvis registration aligns the keys before interpolation. PixelLab job `c0d7cff5-7914-40bc-9228-995b14d850a4` supplies nine connected whole-body left-to-right transition frames; dual and guard keys make11 runtime poses. The earlier symmetric PixelLab pass `79e1746d-8dbc-4767-8400-7041003df725` is retained as source history but not selected. No independent limbs or weapon parts.

Owning compiler `_BUILD_SOURCE/build_chronos_volley_1025.py`: fixed256x256 even cells, one218/256 proportional scale, common128,90 pivot, measured palm coordinates transformed with the same scale/padding, clean alpha and native white-hit variants. Manifest `assets/chronos_volley_art_1025.js` and lossless sheets register together. Do not hand-edit generated manifest rows. Projectile and palm-flash art is existing authored art, palette-matched to red/white. Nine transition frames play forward/back between the firing hands; shot and flash sockets follow the current pose.

## Verification

- `_BUILD_SOURCE/probe_chronos_volley_1025.py`:14/14 native checks. Charge gating, both depths, exact endpoint scales, alternating/dual bursts, preserved wave, no ghost hammer, warning groups, palm origins, real body pixel damage and flash expiry, oriented laser collision, real player damage, owner death cancellation; no page/console errors.
- Inspected foreground/background native screenshots and decoded video frames, including palm flash/projectile alignment. The recording is32 seconds of native Furious gameplay with audio, starting at an explicitly labeled15%-HP checkpoint and invulnerability enabled. It is not a full-fight clear.
- `_BUILD_SOURCE/record_chronos_volley_1025.py`; scratch/video `_shots/chronos_volley_1025/`. Foreground fire about7s, background13.5s, wave21.3s, foreground return25s.
- `_BUILD_SOURCE/verify_chronos_volley_1025.py`:8/8. Decoded video audio, both recorded depths, native state progression, browser playback/seek, all frame previews, no browser errors. Shared `av3_laser_release` source also decoded with audible waveform; native `enemyPulseLaserAlien` alias owns this route. Expected local server connection reset comes from cancelling metadata before blob-based seeking.
- Syntax checks pass for game.js and new art/runtime. Required test_fl exits1 before assertions/final summary due the previously recorded missing `_BUILD_SOURCE/retired_art_archive_1022.cjs`.

Primary review `docs/previews/chronos_frames_1025/index.html?revision=palm-volleys-1025`; previous minigun review archived as `full-turn-gold-red-review.html`. No commit/push. Unrelated existing work preserved.
