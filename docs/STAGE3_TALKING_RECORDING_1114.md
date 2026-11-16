# Stage 3 — fresh complete cinematic reel

Mike requested the full Stage 3 cutscenes recorded with the new talking cockpit frames, including lift-off. The new reel was captured from the running original BOF checkout at `D:/BOF-Downloads/2026-11-14/RevG-source` on November 14. Earlier recordings were retained.

The full 144.18-second MP4 is `_shots/stage3_talking_1114/stage3-full-cinematics.mp4`. The chapter page is `_shots/stage3_talking_1114/review.html`, served on port 8766 with media byte-range support so chapters can seek. The existing game server remains on port 8765. The plain game server did not support media seeking; no game runtime change was needed.

The reel includes:

- 00:00 — Complete service data-link conversation with Cole's new seated talking frames and Decker at base.
- 00:25 — Top-down systems heat charge.
- 00:41.5 — Lift-off with animated thrusters and native audio.
- 00:47.3 — Fade and campaign map continuation.
- 00:48.7 — Stage 3 card, fly-in, braking, settle and gameplay handoff.
- 01:07.5 — Complete HQ briefing after Stage 3.
- 01:52.5 — Workshop and Photon Cannon prototype sequence.

These are three complete native cinematic checkpoints, played at native speed without dialogue skips. Gameplay between arrival and the post-stage HQ scene is omitted. The reel is not a campaign playthrough. It contains game music, letter sounds and native effects; no new spoken voiceover was generated.

The source recordings cover all ten service sequence beats and all 23 HQ/prototype beats. The service sequence and HQ continuation each run exactly once. Cole's cockpit bank is `cp15_cole`, with multiple generated mouth poses observed. Native arrival runs through `run`, `brake`, `settle` and `cd` before PLAY. There were no page, console or HTTP errors in any capture.

The final MP4 uses fixed 1824×1024 capture framing at 30 fps, H.264/AAC and fast-start metadata with embedded chapters. It decodes without errors. Audio mean is −14.5 dB and peak −1.9 dB, below clipping. Representative decoded frames were inspected for the speaking cockpit, data-link, heat charge, lift-off, map, arrival and HQ/workshop scenes.

Raw WebM captures, recording metadata, frame contact sheet and browser playback evidence are retained with the movie. Durable evidence is `docs/qa/stage3_talking_cinematics_1114.json`. Reproduce with `_BUILD_SOURCE/record_stage3_talking_1114.py` followed by `_BUILD_SOURCE/package_stage3_talking_1114.py` while this checkout is served on port 8765. `_BUILD_SOURCE/serve_stage3_talking_1114.py` starts the loopback-only preview server on the first available port from 8766 to 8775, with its URL saved in the preview directory's `server.json`.

No game source, gameplay state owners, cinematic script, generated artwork or test files were changed for this recording request. No commit or push was performed. The core suite was not rerun for this media-only task; the preceding implementation's 8,969/0 receipt remains in `docs/qa/cockpit_talk_1114.json`.
