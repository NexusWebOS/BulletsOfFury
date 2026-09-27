# Stage 7 boss music — September 27, 2026

Mike's `reaperman.wav` is the new Stage 7 boss theme. `BOFA.music.boss7`
and its legacy alias `boss7mus` now resolve to
`assets/game/music/boss7_reaperman_0927.mp3`.

The previous `boss7.mp3` was renamed byte-for-byte to
`assets/game/music/unused13 - stage7b.mp3`, also registered as `unused13`
for later listening. The Stage 7 field theme remains Over The Horizon.
Stage 7's existing miniboss fallback still follows the boss theme.

The Desktop WAV remains untouched, with an identical source copy at
`assets/game/music/originals_0927/reaperman.wav`. The browser copy is
44.1 kHz stereo, 160 kb/s MP3 with 5.1 dB attenuation to match the previous
track's average level. There are no edits to timing or dynamics beyond gain.

`_BUILD_SOURCE/import_reaperman_0927.py` owns the focused music manifest
update; other manifest namespaces are unchanged. Browser verification uses
`_BUILD_SOURCE/probe_reaperman_0927.py` with the real game's sound loader.
Both tracks decode to nonzero stereo audio and play through `Audio.startMusic`
without page or console errors. Temporary proof is in `_shots/reaperman_0927/`;
durable results are in `docs/qa/stage7_music_0927.json`.

No gameplay changes, commit, or push were made in this music pass.
