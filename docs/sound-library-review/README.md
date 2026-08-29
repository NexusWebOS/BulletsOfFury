# New sound library review

This is a non-destructive audition surface for `sounds.zip`, received on 2026-08-28.
The 55 source MP3s remain under `_ART_SOURCES/audio/sound_library_2026-08-28/raw`;
none are registered in or copied over `assets/game/sounds` during this review pass.

Run `_BUILD_SOURCE/build_sound_library_review.py` to refresh technical metadata,
content hashes, and waveform images. Serve the repository root and open
`/docs/sound-library-review/index.html`.

Review choices are stored in browser local storage. **Export choices** downloads a
JSON handoff containing the Primary, Alternate, Layer, Reserve, and Reject decisions
plus notes. That handoff can be applied in a later, explicitly approved integration pass.
