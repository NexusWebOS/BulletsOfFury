# Rebel audio and Voss turbo repair — October 13

Local gameplay changes requested after Mike's Stage 6 play session. No commit or push.

Voss now finishes his committed turbo pass outside the visible arena, travels
around its outside edge, and returns visibly from above. His authored wake stays
attached throughout that return and fades after he settles. The first dash uses
the aim already shown by its warning, rather than silently reacquiring the player
at release. The attack retains its existing number of passes, warning times,
damage and firing speeds. Recovery movement does not deal dash damage.

The final introductory turbo exhibition had a second position override after its
wake was appended. Its ship and wake now use the same final position along one
continuous path, including the return to formation before dialogue releases.

Rebel music previously used a one-shot boss-identity latch. A rejected or paused
transport could remain silent for the rest of the encounter. Stage 6 now preloads
the Rebel track and one voice for each of 16 encounter cues. A bounded half-second
health check resumes the existing music element without resetting its position,
and resumes the effects AudioContext if the browser has suspended it. Saved
volume settings are unchanged. Cold attack transients load their cue without
queuing a stale playback request that would sound after the attack had finished.
The existing 64-voice effects limit is retained.

Changed modules: `feedback_1003h.js`, `rebel_arsenal_1004c.js`, and
`audio_extra_1010.js`. The parent task owns index cache stamps and the full game
regression check. No generated art or atlas layout changes were required.

Verification: the native Edge probe passed 93 checks across Stage 6 and Stage X
Rebel encounter fixtures on Easy, Normal, Hard, and Furious. It runs the full
introductory dialogue and turbo exhibition, then the real battle controller and
renderer. Chrome and Firefox each passed 16 focused Normal-fixture checks, for
125 total checks and zero browser errors. Checks include warning commitment,
continuous return movement, wake attachment, precise music resumption, cold-cue
handling, suspended AudioContext recovery, and the effects voice limit. Native
return screenshots were inspected; Voss descends from the top with his wake and
does not reappear in the lower player area.

The actual decoded music streams had RMS levels of 0.249 in Edge, 0.240 in Chrome,
and 0.253 in Firefox. These are media transport/output measurements, not a claim
of human listening or proof of the user's laptop audio device behavior. The
fixtures isolate the real encounters; they are not complete campaign runs.

Reproduce with `_BUILD_SOURCE/probe_rebel_audio_turbo_1013.py` (Edge by default).
Set `BOF_BROWSER=chrome` or `firefox`, and `BOF_QUICK=1` for the focused fixture.
Detailed captures, movement samples and the initial failed transport-seek probe
remain under `_shots/rebel_audio_turbo_1013`. The initial recovery probe exposed
a reset/seek race; the final implementation resumes the same element directly
and all final checks pass. Portable summary: `docs/qa/rebel_audio_turbo_1013.json`.
