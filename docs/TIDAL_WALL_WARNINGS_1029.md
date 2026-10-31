> Warning artwork corrected: TIDAL_WARNING_SIGNS_1030.md. Mike meant Stage 2 metal yellow/red warning signs, not the plain impact stars described below.

# Visible water-wall warnings and water-wave audio — October 29

[Watch the corrected water-wall sequence](http://127.0.0.1:51046/?tidal=wall-warnings-audio-1029#clip=stage9-tidal-walls)

The lane asterisks existed, but drew before the entire boss hull. The hull hid them. They now draw last in the boss renderer, above the hull and water effects, at the committed lane positions below the boss gauge. The same authored red asterisk pixels bob with Stage 2's cadence. No runtime glow, scale or tint was added.

The three asterisks appear 0.75 seconds apart, each with one native danger beep through the dedicated tidalWallAlert cue (.4-second gate; the global .9-second danger gate stays unchanged), and keep their individual lane until that wall launches. The original 3.35-second anticipation, one-at-a-time three-wall sequence, lane commitments, approaching water frames and collision remain. Each launched asterisk disappears, leaving the queued walls visible.

Every full-sized wall now plays the dedicated tidalWaterWave cue: a generated rushing ocean swell, foamy crash and wet tail, rather than the previous short ice-breath-derived cfComboWater. ElevenLabs Sound Effects v2 produced four candidates; selected generation YgOFRWvFYWk0uCiyteau is the two-second master. The source and provenance are archived under the boss audio folder. A 70 Hz high-pass, peak limiter and short tail fade retain its original pitch and speed. Two lazy voices use the existing Snd mixer, master/SFX/mute settings, gain 0.76 and 0.8-second retrigger gate. No custom bus, callback scheduling or loop was added. Small geyser-return waves keep their separate existing cue.

55 native Chromium checks pass, including 1,587 actual front-layer changed red asterisk pixels, ordered reveal beeps, three distinct water-wave calls, real decoded mixer playback, existing HP/attack/hit/defeat paths and transferred Sentinel regression checks.

The fresh 147.84-second real-engine Furious recording reaches native defeat, includes all attacks and decoded tidalWaterWave playback, and has no game/browser/media/audio/input errors. Encoded audio mean -20.5 dB, peak -1.9 dB. Gallery playback and HTTP 206 seeking pass. 33/33 film checks pass; the >55 FPS check now passes at 57.67 FPS. This explicitly labelled invulnerable Cole recording demonstrates presentation and mechanics, not human difficulty balance. Native and decoded warning frames were inspected.

Syntax checks pass. The required full suite still exits 1 with the same five existing failures: single-hit flash hold; opening-jump dialogue; jump/chromium ordering; opposite Stage X route persistence; Stage X right-branch encounter. The core game.js and test_fl.js are unchanged. No commit or push.

Owner: assets/tidal_sovereign_1029.js. Rebuild audio: _BUILD_SOURCE/build_tidal_wave_audio_1029.py. Native probe/recorder: _BUILD_SOURCE/probe_tidal_wall_warnings_1029.py and record_tidal_wall_warnings_1029.py. Full evidence: docs/qa/tidal_wall_warnings_1029.json. Existing art, forward spreads, fan geyser returns and exploding fan grenades remain.
