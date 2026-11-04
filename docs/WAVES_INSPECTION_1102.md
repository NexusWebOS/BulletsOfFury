# Furious wave inspections — November 2/3, 2026

Requested review: hold fire so native enemies demonstrate their movement and attacks, then clear the group or let it depart before advancing. Mike explicitly selected one-wave-at-a-time pacing. This is real native browser-engine footage with the updated layered stages, Furious difficulty, and native GOD mode. Bosses/minibosses are omitted.

## Recording method

- Each scheduled group has at least eight native simulation seconds before cleanup, or eighteen for large carrier/heavy encounters. Fast flybys may leave naturally before that window ends; individual units are not held artificially onscreen.
- The pilot uses native movement, machine gun fire, Retina and missiles. No enemy health, phase or attack-timer writes are used to manufacture a clear. GOD mode protects the pilot; it is not proof that a human can evade every pattern.
- Later scheduled waves wait. Camera/stage-position seeks between cleared groups use recorded native release locations. Old player/enemy shots and locks are reset at these independent inspection cuts; endless adaptive/onslaught extras are held. Allied offense is held during observation and native during cleanup.
- These are paced inspection scenes, not a continuous campaign or ordinary overlap stress test. They cannot certify normal scheduling, ordinary buildup, or human dodgeability.
- The game renders at its native default quality and native timing. Video delivery is H.264/AAC, 1280×800, 30 fps; encoding does not interpolate away slow frames. Reported frame rates describe this recording environment, including capture overhead.

## Findings and fixes

The initial delayed-fire native-timing trial exposed a real Stage 1 traffic bug: tanks stopped exactly at VH+80 while the offscreen cleanup required y>VH+80. Invisible departed tanks stayed alive and blocked later waves. The production fix permits exit beyond the complete visible footprint and culls after it leaves. It preserves upstream queues, still-visible large hulls and normal score/reward behavior. A real-browser original-versus-fixed probe covers those boundaries.

Stage 6 release 7 creates a skimmer at x=-90 which never becomes visible in the native run; its recorded lifetime ends before a normal on-screen entry. This is flagged as a release failure, distinct from terrain-dependent turret callbacks that produce no actor. The footage does not hide these empty releases.

Stage 7 has substantial draw-bound stalls in the capture environment; early samples include draw p95 above 800ms. It is not a clean performance pass.

A subsequent native-timing trial reached a separate Stage 1 late-spawn stall at 17/36 as terrain reached its end. That remains a scheduling follow-up. Completion of these isolated inspection films does not resolve or conceal it.

Recorder-only corrections: include armed modular turret fixtures in cleanup; target modules before gated hulls; clear leftover player shards at inspection cuts; confirm the native Stage 6 route menu after selecting a route. Superseded/incomplete takes are excluded from publication. Departed actors do not block an independent inspection cut. Any cleanup still unresolved after sixty native simulation seconds is explicitly marked incomplete; its scene ends without a native kill or reward before the next independent inspection. This prevents a failed inspection from hiding later scheduled groups.

## Validation limits

`node --check assets/game.js` passes. The required full suite still stops before its final summary on the existing `ReferenceError: difficultyHealthBaseline15 is not defined` in `assets/combat_polish_0927b.js:151`. It is not a green suite. The test fixture was not altered to suppress this failure.

Final coverage, performance table, native no-release cues, media checks and browser seek checks are populated from the completed receipts below.

## Completed coverage

10 stage/route films; 313 chapters representing 260 unique scheduled entries; 82m 22s. Both Stage 6 routes are included. Stage X has no regular-wave book. All chapters have at least eight native simulation seconds before cleanup; large threats receive eighteen.

| Collection | Duration | Native render fps | Peak enemies | Peak hostile rounds | No visible enemy entries |
|---|---:|---:|---:|---:|---|
| stage-1 | 7:06 | 58.68 | 7 | 25 | 14, 17, 27 |
| stage-2 | 4:52 | 58.17 | 7 | 33 | None |
| stage-3 | 3:56 | 58.98 | 7 | 15 | None |
| stage-4 | 6:32 | 57.62 | 5 | 15 | None |
| stage-5 | 3:17 | 58.16 | 6 | 20 | None |
| stage-6 | 11:33 | 54.06 | 10 | 48 | 7, 17, 20, 24, 28, 32, 36, 39 |
| stage-6-right | 11:46 | 53.68 | 10 | 48 | 7, 17, 20, 24, 28, 32, 36, 39 |
| stage-7 | 18:54 | 13.87 | 7 | 52 | None |
| stage-8 | 6:16 | 58.27 | 3 | 36 | 3, 5, 13, 17, 21 |
| stage-9 | 8:05 | 58.49 | 5 | 39 | None |

Blocked cleanup chapters: {}. They end as inspection cuts without a native defeat or reward. Empty entries remain clearly flagged rather than being certified as successful enemy demonstrations. Terrain-dependent callbacks may decline a release; an actor spawned but never visible requires separate investigation. Counts are per inspection scene and include native helper behavior; they are not ordinary overlap counts.

## Review and media checks

Every final movie passed full decode, H.264/AAC checks and non-silent/non-clipping audio checks. Browser QA decoded 30 first/middle/last chapter seeks across all ten collections, exercised observation/cleanup/full-film controls, rapid route changes and a 390px layout, with no page/console/HTTP errors. Representative actual gameplay frames were visually inspected. This is not an exhaustive human viewing of every attack or an audio-mix approval.

The Stage 7 film joins preserved first-sixteen-wave scenes with a fresh native continuation for waves 17–22. A departed fixed turret had blocked the observer below screen; the QA-only cleanup rule now treats it as departed and resets such fixtures at scene boundaries. Native health, active enemy AI and attack timers are untouched. The source receipts and exact cut ranges are retained. Scene counters can restart on the fresh continuation.

Playback: http://127.0.0.1:63094/review/current/all-waves-1101.html?inspection=1102#level=stage-1&wave=1

## Source and test receipts

Core before: `0b9f9b8701ebf891a7224da6e3c273e208777e45e154bf2a5be73ca7c0a3d0c1`. Core after: `cffaaae7ff5d32f3d8177d55c6d09eea8a555e1f221beedd14c8cbf26559a4a3`. The only production change in this task is the two-location full-footprint ground-vehicle exit repair. LF core and CRLF test-suite line endings are preserved. The full-suite pre-existing failure remains documented above; no test was suppressed or changed.

No Git commit or push was performed for this request. Previous movies and local work are preserved.
