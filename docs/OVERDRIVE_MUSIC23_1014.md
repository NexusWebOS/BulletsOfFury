# Music23 — supplied stage and boss recordings

Local build `overdrive1014-music23-r1`, October 14, 2026.

BOF-BASE is the stage/briefing track for levels 3 and 7. Rise of the Last
Hope is their boss recording. The exact user-supplied stereo 16-bit WAV bytes
are retained under `expansion/topdown/audio/music23`; source hashes, sample
rates and durations are recorded in `manifest.json`. BOF-BASE is 122.4 seconds
at 48kHz; Rise is 40.324127 seconds at 44.1kHz. Both loop normally.

Level 3 retains stage music throughout Gosfer's entrance, then crossfades to
Rise over 1.8 seconds when combat begins. When his actual cover-breaker
volleys destroy all three barriers, protected portrait dialogue lowers the
same boss recording to 18% over 0.6 seconds. It stays lowered throughout
dialogue and lightning, then fades back up over 1.8 seconds when the
transformation finishes. The recording continues from its current position.

Level 7 retains BOF-BASE for rooms 1–7. The room-8 reactor reveal starts the
1.8-second boss crossfade; it continues through glass fracture, whiteout,
Helios reveal and boss retries. A fresh mission launch restores stage music.

The HTMLAudio implementation waits for native playback before fading the
outgoing track, applies fades using elapsed wall time, and releases retired
voices. Music/master settings multiply each voice's current gain, so menus,
pause and mute cannot bypass a fade. Stopping music also cancels pending
locked cues and both sides of an interrupted crossfade. Other campaign stage,
Warrior, title, select and clear recordings retain their existing identities.
Level 7 game-over now stops its music just as other stages do.

34 native Chromium checks passed with zero page, console, asset or media
errors. Actual HTMLAudio durations, playback time, volumes and native loop
wraps were checked. Real WebAudio analysis measured nonzero PCM for both
supplied recordings. The source and delivered WAV hashes match exactly.
Cue-boundary fixtures exercised ordinary level-3 boss spawning, Gosfer's
actual barrier-breaking volleys, dialogue/transformation, the level-7 wave
and reactor hooks, Helios reveal, retry, options, cancellation and menus.
This verification is scoped to audio cues; it is not a new full combat route.
Screenshots were inspected for the existing encounter presentation.

Probe: `expansion/topdown/_research/probe_music23.py`.
Evidence: `docs/qa/overdrive_music23_1014.json` and `docs/qa/music23_views`.
Required base syntax/suite completed BUILD OK / 0 ERRORS / exit 0.
The repository-wide diff check still reports existing CRLF whitespace in
unrelated files; all changed tracked music/runtime files pass the scoped check.
No new graphics, `assets/game.js` edit, commit or push. Preserve all other work.
