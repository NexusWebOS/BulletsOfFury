# Overdrive startup recording — October 11, 2026

## Current correction: original call, then enhanced Overdrive

Start plays Mike's original **“Bullets of Fury!”** title call first, using the
actual `assets/game/shared/audio/sounds/announce.mp3`. After that clip ends,
Mike's `overdrive.wav` plays with room reverb, arcade echo and loudness matched
to the original call. The original BOF logo appears during the first call;
the Overdrive overlay fades in during the second. Title music starts after
the final echo tail ends.

The source recordings retain their bytes. Natural voice pitch stays unchanged.
Measured loudness: original call **-16.31 LUFS**, processed Overdrive
**-16.30 LUFS**. The supplied Overdrive source is 2.8914966 seconds, stereo
44,100 Hz, 16-bit PCM. Processing adds a 912 ms echo tail.

## Assets and ownership

- Original title call: `assets/game/shared/audio/sounds/announce.mp3`.
- Preserved Overdrive WAV: `expansion/topdown/audio/source/overdrive.wav`.
- Enhanced shipping audio: `expansion/topdown/audio/overdrive-reverb_1011.mp3`.
- Combined audition: `expansion/topdown/audio/overdrive-intro-preview_1011.mp3`.
- Effect recipe, source hashes and loudness measurements:
  `expansion/topdown/audio/startup_reverb_1011.json`.
- Earlier dry MP3 and provenance remain in `overdrive-startup.mp3` and
  `startup.json` as the initial import checkpoint.

`TD.STARTUP_AUDIO.lead` owns the original call; `.file` owns the enhanced
Overdrive call. Both use the saved Master × Voice gain. Start/B skips and
stops the active and queued clips. Leaving the intro releases both. A replay
starts fresh. A failed media request releases its turn in the sequence.

The owning audio builder preserves the imported WAV, exports the dry copy,
measures the reference, adds reverb/echo, matches loudness and exports the
enhanced copy and combined preview. Runtime playback rate is 1.

## Reproduction and evidence

```powershell
python expansion/topdown/_research/build_startup_audio_1011.py
python expansion/topdown/_research/build_original_options_1011.py
python expansion/topdown/_research/build_menu_art_1011.py
python expansion/topdown/_research/probe_restored_frontend_1011.py
python expansion/topdown/_research/probe_chip_audio_1011.py
node --check assets/game.js
node _BUILD_SOURCE/test_fl.js
```

To import the source on another checkout, pass its location with `--source`.
The builder refuses to replace a different preserved recording.

Current evidence: `docs/qa/overdrive_restored_1011.json`. This correction
supersedes the original single-clip startup. Native verification uses actual
browser media time and decoder output, real inputs, isolated saves, the live
canvas renderer and protected completion/control fixtures. The complete base
suite reaches its final summary with **8,700 passing assertions, zero errors
and exit 0**. This pass does not edit the base `assets/game.js` or its test file.

Saved locally; no commit or push for this correction.
