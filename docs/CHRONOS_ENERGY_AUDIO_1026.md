# Chronos charge / wave audibility correction — 26 October 2026

The preceding live preview installed lightning only; Clear charge/wave candidates remained separate auditions. This pass installs Clear into the live game.

Native hooks in assets/chronos_energy_audio_1026.js start rage charge on the first actual charge strike, release on the final strike, Kame charge on warpCharge, main wave on fusionBeam and the tail on laserBeamEnd. Ordinary rage gather/wave also use these cues. Repeated legacy charge/beam triggers are consumed once per native cycle, avoiding sample restarts. Dedicated two-voice pools use the shared mixer, master/SFX mute, native gains, global bounded allocator and pause/death/owner cleanup. No charge/damage timing changed.

Lightning still sounds once for every bolt. Its gain is multiplied by .44 while a foreground charge/release/beam cue is playing; its former level returns when those cues finish. The original Dracodia source/pool remains unchanged.

The ordinary1.7s gather derives from the2.6s Clear master via FFmpeg atempo=1.5294117647 (pitch preserved). Retained masters, source hashes and full recipes are under _ART_SOURCES/chronos_energy_1026; the owning encoder is _BUILD_SOURCE/build_chronos_energy_audio_1026.py.

## Proof

- Fresh native-engine checkpoint video and short excerpt use captured game audio, without offline sound overlays.
- All14 focused energy checks pass. Actual per-cue output meters show nonzero charge and beam output in their native phases; see verification.json for levels and exact trigger events.
- Recorded decoded audio peak: -5.0dBFS; native average: 38.1fps.
- All26 rage strikes, final strike and Kame bolts retain accepted lightning cues.
- Syntax passes. Full test_fl.js exits1 with the same five failures as the pre-audio baseline. No new failure names.
- The downloaded build lacks one optional stop_empty.png sheet. The recording uses the existing native recovery fallback only in the browser session. No production art replacement.
- No physical headphone/speaker listening claim. Mike reviews final timbre through the preview; numerical levels alone do not establish preference.

## Unchanged

Combat timing, projectiles, boss HP, authored frames, source sound files, Dracodia audio and unrelated local work remain. No commit or GitHub upload.
