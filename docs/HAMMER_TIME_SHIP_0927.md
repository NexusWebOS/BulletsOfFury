# HAMMER soundtrack entrance correction — September 27

Mike corrected the secret encounter's opening: Hammer must fly in as a ship as the
remix starts; the wall rises before the 0:16 dance cue; there is no playable gap.
This supersedes the early entrance release documented in HAMMER_TIME_WALL_0927.md.

Implemented in `assets/hammer_time_0927.js`:

- The actual authored Hammer ship enters from below at soundtrack time zero.
  Playback waits for the ship, transformation, dance art, player hull and music
  readiness. The intro uses media time, so buffering cannot advance it ahead of
  the soundtrack. Menu selection no longer starts the remix early.
- Ship approach: 0–2s. Unfolding: 2–3.6s using existing transformation frames
  15 through 6, avoiding the retired back-gun frames. Canonical hammer windup
  follows, with impact at 6.15s and four staggered helper arrivals from 6.4s.
- Helpers hold their pose until the breakdown. One authored flat wall rises
  from 7–16s, at 50% opacity across the entire world width. Clipping reveals
  the rising panel without vertically compressing its texture.
- At 16s the full wall stays in place and the troupe dances. Movement, firing,
  missiles, specials, evasion and in-game pause remain blocked throughout
  the entrance AND dance. Control first returns at 24s, with a short protected
  opening. Hard/Furious/Insanity helpers retain their warned attacks.

Existing authored assets and supplied `mchammer.wav` import reused; no new art,
new audio, atlas changes, or game.js changes required. No commit or push.

## Verification

- Runtime syntax checks passed. Full suite exited 0 and reached the final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner: **5,545 passing, zero failures**,
  compared with 5,538/0 incoming. Final and incoming failing-name sets empty.
  Two intermediate new fixture failures were caused by FakeAudio not changing
  its mocked paused flag on play; fixed in the fixture.
- Native Chromium probe verifies the actual XART ship draw, staged arrival,
  no early unlock, one wall draw at .5 alpha, blocked damage/actions, release,
  helper targets/damage, all five difficulty attack fixtures, finite projectiles,
  zoom 1, and victory cleanup to title. No page or console errors.
- A physical desktop gamepad fed held buttons into the first probe and selected
  Armory AFTER the verified title return. The final keyboard-driven browsers
  explicitly exclude physical gamepads; no game input behavior was changed for
  this fixture interference. Hardware gamepad play remains a human check.
- Real-time 36.07s Hard recording with the supplied soundtrack and actual SFX:
  break begins 16.011s, last locked frame 23.999s, controls first released
  24.011s. All 500 sampled break frames remained locked. No movement, shots,
  ammunition consumption or pause leaked through the entire opening. Four
  helpers were present and all 12 missiles remained at release. Recorded audio
  peak .528 with capture-only gain .4; recording is audible and decodes.
- Ship, transformation, impact, rising-wall and dance screenshots inspected.
  Review page and seek controls checked in Chromium. All images/video load and
  page/console errors remain zero. LF runtime and CRLF tests preserved.

These are controlled fixtures and an invulnerability-assisted recording, not a
campaign win or a final balance verdict. The eight-second dance endpoint remains
the existing choice. Previous campaign, hardware and balance follow-ups remain.

Review: http://127.0.0.1:8794/_shots/hammer_time_ship_0927/review.html

Evidence: `docs/qa/hammer_time_ship_0927.json`, ignored native screenshots, clip,
logs and review checks under `_shots/hammer_time_ship_0927/` and related logs.
