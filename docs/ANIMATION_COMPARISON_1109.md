# Boss attack animation comparison (Nov 9)

Furious difficulty, filmed in Chromium. Strips are in `docs/previews/anim_1109/` (one frame every 5 game frames).
Pose counts come from a per-frame log of the large sprites drawn, so they miss anything composited offscreen. Trust the strips over the numbers.

Chronos sets the bar: every attack reads as anticipation, contact, recovery, and the body commits to it.

| Attack | Anticipation | Contact | Recovery | Verdict |
|---|---|---|---|---|
| Chronos warn (Stage 5) | 21 poses in 0.6 s, hammer cocked behind him | leap, 15 poses in 0.3 s | 53 poses in 2.2 s | The standard |
| Chronos whirl / giant windup | Body turns, hammer glows, 8-10 poses | Big silhouette change | Settles back | The standard |
| Stage 8 hammer: side swing | **None. 1.1 s frozen on swing frame 0** | Good authored swing | Short | Fix anticipation |
| Stage 8 hammer: spin | **None. 1.1 s frozen on spin frame 0** | Good authored spin | Ends abruptly | Fix anticipation |
| Stage 8 hammer: throw, skystrike | Has real windup / jump | Good | Good | Closest to Chronos |
| Dracodia drone: swipe | **Arm does not cock; only the green-yellow-red lanes warn** | One rotated claw sprite, small against the body | Whole body drifts | Needs art |
| Dracodia drone: grab | **Same: lane only, no reach-back** | Hard to read | Drifts | Needs art |
| Dracodia final: extended claws | Claws barely leave the guard pose | Warning arc does the work | Long static hold | Needs art |

## Root causes
- Hammer side and spin: `dracodia_chronos_1030.js:43-44` samples frame 0 for the whole tell (`u<0?0`).
- Drone swipe and grab: the warning is drawn, but the arm has no wind-up pose to play.
- Final claws: the anticipation lives in the warning arc rather than in the arms.

Not reached in this filming: the final form's `scytheReap`.

## Art requested
Three sheets into `_ART_SOURCES/anim_1109/`: drone claw swipe, final-form claw swing, hammer side/spin anticipation.

## Correction and result (Nov 9)
The drone rows above are wrong about the art: the live owner is `host_whole_arms_1031.js` (RD96), which draws a whole arm from 64 authored poses, not one rotated claw. Its wind-up existed but was slight.

Installed in `playtest_repairs_1108.js` (`PR118_CLAW`, `window.PR118_CLAW_OFF=1`), display only, with strike paths, contact, hitboxes and timers unchanged:
- Drone swipe and grab: the 16 wind-up poses are replaced by the new cock-back frames.
- Final extended claws: new frames through the side and jump tells, then one smear frame at the start of the strike.
- During those tells shots still hit the old pose shapes, not the new silhouette.
- Hammer side and spin wind-ups are still open: the first sheet was 0.63x too small and regular armor only (needs 376x318, pivot 256,122, with chrome and red).

## Chronos Stage 5 swings reviewed (Nov 9): not the standard
The "21 poses" figure counted repeated slots. Art: `docs/previews/anim_1109/chronos_swing_banks.jpg`. Furious, chrome armor, hammer head position per tick.

| Bank | Slots | Distinct poses |
|---|---|---|
| windup | 17 | 7 (slots 9-15 are one held pose) |
| strike | 17 | 5 |
| retract | 17 | 4 |
| left / right | 17 | 16 |

Head jumps between combo moves, with no linking frames: strike end to windup start 151 px, strike end to left 149, left end to right 110, right end to `takeoff:0` 263, `takeoff:0` to retract 150. `takeoff:0` is held at the end of the combo as a stand-in pose.
Inside the side swings, the head jumps 256 px (left) and 239 px (right) at slot 7 to 8, the smear frames.

Joins fixed for Furious (`PR118_JOIN`): no between-move head jump of 100 px or more remains in the log; each bridge stays below about 115 px. The remaining jumps are inside the art (side-swing smear 256/243 px, strike 131, windup 125 and 102). Hard uses a different combo timeline and is unchanged.
