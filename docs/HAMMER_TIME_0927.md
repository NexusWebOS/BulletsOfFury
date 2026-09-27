# HAMMER secret encounter — September 27, 2026

Implemented locally from Mike's requested dancing Hammer fight and supplied `C:/Users/Mdogg/Desktop/mchammer.wav`. The corrected breakdown cue is **0:16**, replacing 0:22. Current break length is eight seconds, ending at **0:24**; Mike specified the start, and eight seconds is the implementation choice pending his playtest.

## Playing it

Enter `HAMMER` in Password, then choose difficulty and pilot. This launches an isolated Stage 5 space encounter with the existing Hammer attack engine, new dancing art, and Mike's remix. Ordinary campaign Hammer uses its normal encounter. Winning or leaving the secret fight cleans up its music/lock and returns to the title. Pause works outside the dance break.

The boss shuffles and performs running steps during rests, displays the palm-out “STOP, HAMMER TIME!” taunt, and mouths with the supplied track's amplitude envelope. Helpers have their own shuffle and turn poses. There is no separately generated singing vocal track.

At soundtrack time 16 seconds the attack is cancelled, hazards are cleared, four helpers assemble, and the generated cyan shield encloses the group. They alternate dance steps and full turns. Controls, direct and automatic weapon release, specials, evasion, incoming damage, and in-game pause are blocked until 24 seconds. Existing shot reflections are harmless visual effects. Visual explosion tails continue to expire. A running special is held and restored after the break, with 0.8 seconds of player protection and a 2.1-second boss opening. The lock follows the playing music clock, including when music volume is zero.

Combat retains jumping strikes, counterable hammer throws, sweeping whirlwind/disarm, and the spiked ball below 65% health. Small helpers can be shot down and fire only during quiet boss rests, with the existing warning system. The secret fight does not advance into the normal chaingun transformation after a disarm. Difficulty HP: Easy 4800, Normal 6800, Hard 8400, Furious 9800. These are starting balance values, not a claim of completed human balance testing.

## Assets and ownership

- Built-in image generation, using the approved single-headed blue Hammer: 16 boss frames, 8 backup dancer frames, 8 forcefield frames. Original RGBA retained; no SpriteCook.
- Source prompts/identities: `docs/hammer_time_prompts_0927.json`.
- Shipped sheets: `assets/game/hammer_time_0927/`.
- Owning build: `_BUILD_SOURCE/build_hammer_time_0927.py`; generated cell rectangles, stable anchors, audio envelope and cue metadata: `assets/hammer_time_art_0927.js`.
- Supplied 143.6-second WAV converted to `assets/game/music/hammer_time_mike_0927.mp3`. Desktop original untouched; source SHA256 retained in metadata. Beat estimate is approximately 136.36 BPM, used for dance frame cadence.
- Runtime integration: `assets/hammer_time_0927.js`, loaded after pilot feedback in `index.html`. This pass does not edit `assets/game.js`.

## Verification

Final full suite: **5513 passing assertions, zero errors, exit 0**, final success banner. Incoming baseline was 5492/0; no incoming or final failing assertion names. New tests cover route/cancel, lock boundaries, all release paths, damage protection, four helpers, visual expiry, restored special, pause restoration, disarm recovery, difficulty health, and normal-run isolation.

Intermediate runs caught a new fixture's nonexistent `coopOff()` helper, then seven test-source failures caused by a Windows encoding conversion. The fixture now uses the actual `coopOn` flag; original UTF-8/CRLF test bytes were restored. The final suite is clean. `game.js` remains LF; both test files remain CRLF. Runtime and generated metadata syntax checks pass.

Real Chromium verification through `_BUILD_SOURCE/shoot.py`:

- Actual password entry → difficulty → secret start; authored XART sheets and Fury ship readiness polled.
- Native lock probe verifies unchanged player position/ammo/lives, zero primary shots, protected boss HP, resumed movement/fire/pause, ordinary-run isolation.
- Four difficulties, 36 simulated seconds each at 60% boss HP: actual jump/throw/whirl/spiked-ball states, finite projectiles, zoom 1. Frames yielded between batches; representative screenshots inspected.
- Forced lethal damage followed through the real frame loop: death animation → flyover → title, secret music and control lock cleaned up. This is a transition fixture, not a gameplay victory.
- Real-time recording: approximately 36 seconds with Mike's track and game SFX. Lock observed from 16.013 to 23.988 seconds, 499 locked frames; no movement, shots, ammo consumption or pause. Control resumed at 24 seconds. Player invulnerability was used only as a recording aid.
- Recorded audio is nonzero throughout the break; sampled mixed peak 0.495 with capture-only gain 0.4, music 75%, SFX 35%. This is not a full-volume mix certification.
- Video decodes successfully. Review images, playback and cue seek buttons checked in Chromium; page/console errors zero. Local server lacks HTTP range support, so the review loads a Blob for reliable seeking; video is also remuxed with a seek index.

Evidence: `_shots/hammer_time_0927/` (native JSON, screenshots, suite output, original and seekable WebM, clip timing/audio JSON, review check). Durable evidence summary: `docs/qa/hammer_time_0927.json`.

Review: `http://127.0.0.1:8794/_shots/hammer_time_0927/review.html`.

Remaining: Mike's feel/balance playtest, confirmation of the eight-second break endpoint, and real controller testing. Prior campaign requests and audio-mixing follow-ups remain separate. No commit/push; previous overnight automation remains paused.
