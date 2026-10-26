# October 25 — authored bullet hell sections

Mike requested bullet hell sections for Dracodia, the Stage 7 boss and the minibosses, including Herald of Death. Inspected the [Ansimuz reference](https://www.youtube.com/watch?v=-2F7j9-0Fys&t=156s), including its collision-core explanation and rotating ring/fan demonstration. Adapted those ideas to the existing vertical playfield and authored weapons.

Final owner: `assets/bullethell_1025.js`, loaded immediately after `stage78_review_1025.js`. No new artwork or SpriteCook generation; the native projectiles and proportional render paths supply the pixels. No `assets/game.js` edits in this pass.

## Encounter patterns

| Encounter | Added section |
|---|---|
| Stage 1 Razorback | Offset sonic artillery fans |
| Stage 2 Inferno Reaver | Rotating cinder rings from surviving guns |
| Stage 3 Frost Cruiser | Alternating gun braids |
| Stage 4 Olive Warden | Three-mount gun rakes after the escort turn finishes |
| Stage 5 Eclipse Siege Bomber | Staggered cannon braids |
| Stage 6 Warhive Siege Fortress | Electric orb relay through surviving batteries, then the exposed reactor |
| Stage 7 Caustic Dredger | Alternating toxic cannon fans |
| Stage 7 Warden | Rotating acid flowers from the native emitter |
| Stage 8 Herald of Death | Feather vortex from living wings, with a head fallback |
| Stage 8 Dracodia, first body | Raised claws alternate code fans; a destroyed claw stops firing |
| Stage 8 Dracodia, final main body | Code flowers before army downloads and between eligible native attacks |
| Stage 9 Event Horizon | Rotating eye rings |

## Combat contracts

- Sections are inserted at native attack decisions. First-body Dracodia uses the third decision; Warden/Dredger and Event Horizon use the fourth. Final Dracodia opens with a barrage before the archive army. His army, bombs, lightning and blasts interlock with later barrages. New sections do not consume his original attack-book progress.
- Each wave commits its opening before release. Its lateral movement is bounded; successive waves move the opening by at most 34 pixels. Native green/yellow/red FOV art previews the same angles and current weapon sockets, with low opacity during repeated waves. Claws visibly raise before their first warning is committed.
- Furious uses eight waves, up to 26 directions per ring or 15 per fan, a 1.18-second first warning and 0.50-second repeated warnings. Normal uses six waves, 18/11 directions, 1.45/0.60-second warnings; Hard uses seven, 22/13, 1.30/0.55. Easy uses five slower waves. Escape sectors remove directions from these counts.
- A launcher has a 128-round ceiling and finite projectile lifetime. Recovery waits for its live pattern to clear. Projectiles keep the existing small player collision core; there is no global player hitbox change.
- New ordinary rounds cannot be intercepted, including before their first update. Native bomb/shield defensive clears remain available. Existing physical rockets keep their native interception rules.
- One native launch cue and muzzle effect per volley. Existing shared mixer/retrigger gates are used; there are no delayed audio callbacks to outlive a launcher. Wing/claw/module destruction removes pending and released fire from that part.
- Native damage, flash timers, HP budgets, rewards and deaths remain authoritative. Warden braces his walking legs during a barrage; shield retaliation waits and receives its own complete tell. First-body Dracodia retains the 33.3/33.3/33.4 budget, protected core, breakaway arms, ball/code bombs and protected rebirth. All final form pools and the four approved copies remain intact.

## Review and verification

Review: `docs/previews/bullethell_1025/index.html`. Twelve short, audible, real-time clips show the new sections. They are explicitly labelled invulnerable input-bot checkpoints. Eleven checkpoints are reached by advancing the native loop without enemy HP or phase writes; the final-body clip explicitly selects the native final-form fixture. These are pattern reviews, not new complete-fight recordings or proof of human difficulty.

- `_BUILD_SOURCE/probe_bullethell_1025.py`: native decisions, finite completion, bullet budgets and offensive/defensive interception contracts across all nine minibosses plus Warden and first-body Dracodia.
- `_BUILD_SOURCE/probe_bullethell_pixels_1025.py`: native checks covering actual damaged pixels and expiry, shield-counter and archive-army interlocks, destroyed wing/claw cancellation, ball/rebirth, final form ledgers and decoded mixer playback. Native screenshots inspected.
- `_BUILD_SOURCE/record_bullethell_1025.py`: audible real-time checkpoints; independent full MP4 decode and native completion checks.
- `_BUILD_SOURCE/publish_bullethell_1025.py` and `check_bullethell_review_1025.py`: review, seek/frame-step/slow-motion/byte-range checks. Evidence is kept under `_shots/bullethell_1025/`; consolidated delivery evidence is in `docs/qa/bullethell_1025.json`.

Required `node --check assets/game.js` and the new runtime syntax check pass. Required `_BUILD_SOURCE/test_fl.js` exits **1 before assertions or its final summary** because `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing, matching the recorded pre-existing blocker. The suite is not reported as passing.

The earlier [24 timestamped fight findings](FURIOUS_789_REVIEW_1025.md) and original/revised full-fight gallery remain available. Earlier copied-form congestion, Volcano offscreen passes and Stage 9 contrast findings remain separate follow-ups. No commit or push.
