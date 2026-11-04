# Wave footage follow-up — November 3, 2026

Fresh native Furious/GOD films replace Stage1, both Stage6 routes and Stage7. Six unaffected stage films are retained from the previous inspection set, with their original source receipts. The collection remains ten films and313 chapters. Playback: http://127.0.0.1:63094/review/current/all-waves-1101.html?inspection=1103

## Fixes

- Stage6 bomb-pass aircraft were culled before entering the camera, then pinned at the world edge when the entry-only change was tested. Incoming passes now retain their native route until visible and can leave through the far edge. Six real-browser entry/attack/exit cases cover both sides on Normal, Hard and Furious. Existing HP, bomb cadence and rack limits are retained.
- Stage1 optional camouflaged tank reinforcements retried an impossible terrain entry after the dam reached the end of the map. That retry now ends only when no legal entry remains at the exhausted map, so the later authored queue can advance. The native-timing diagnostic was still at30/36 after180 simulation seconds before the change; it reaches36/36 by95 seconds with the change. Boss/miniboss entry was excluded from that queue diagnostic; it is not a whole-campaign completion test.
- Stage7 regular sprite sources are packed onto138 small pages. Selected source grids would expand to2440.2 MiB; the packed pages occupy560.7 MiB of decoded pixel area. A48 MiB bounded cache restores the original transparent cell before the existing destination sampling. Original sources, frame resolution, pivots, animation selection, shield state, hit flashes and weapon sockets are retained. No art was downsampled.

## Measured footage

Stage7's original capture averaged13.87 native render fps; the fresh capture averages50.52. This includes recording overhead on this machine, not a guarantee for every device. Remaining real frame-time spikes are preserved in the movie.

| Stage/route | Chapters | Film length | Native render fps |
|---|---:|---:|---:|
| stage-1 | 36 | 7.15 min | 59.15 |
| stage-2 | 25 | 4.88 min | 58.17 |
| stage-3 | 20 | 3.94 min | 58.98 |
| stage-4 | 22 | 6.54 min | 57.62 |
| stage-5 | 14 | 3.30 min | 58.16 |
| stage-6 | 53 | 11.46 min | 57.41 |
| stage-6-right | 53 | 11.34 min | 58.83 |
| stage-7 | 22 | 5.92 min | 50.52 |
| stage-8 | 30 | 6.28 min | 58.27 |
| stage-9 | 38 | 8.09 min | 58.49 |

## Verification and limits

All15248 packed source cells retain exact alpha and exact RGB wherever alpha is nonzero. Transparent padding and repeated cells are represented by offsets and references.144 paired native draws were inspected; fractional nearest-neighbour edge sampling and one-channel rounding can differ between a full source image and a restored canvas cell. Native comparison receipts retain these differences rather than claiming byte-identical displayed frames.

All final media passes full video/audio decode and audible, unclipped audio checks. Browser checks include30 first/middle/last seeks plus626 decoded observation/cleanup frames covering all313 chapters. No browser page, console or HTTP errors were reported. The fresh films have no recorded damage during observation and no blocked-cleanup cuts.

The next wave waits for the current demonstration, then native player inputs clear the group or it departs. Observation is8 simulation seconds, or18 for heavy encounters. Camera seeks and old-shot resets are explicit independent inspection cuts. Adaptive extras are held; allies hold weapons during observation. This is the pacing Mike selected, not ordinary campaign overlap or proof every pattern is human-dodgeable. Empty native releases remain flagged; retired Stage6 ground-turret cues should not be read as missing new aircraft.

`node --check` passes for the changed runtime files. The required full suite still exits1 before its final summary on the existing `ReferenceError: difficultyHealthBaseline15 is not defined` at `assets/combat_polish_0927b.js:151`. The test fixture was not changed to suppress it.

Native index and engine scripts are pinned in memory during each fresh recording batch so unrelated concurrent story edits cannot change a film halfway through. Actual source hashes and any later on-disk drift remain in each receipt. New menu art and concurrent campaign-story additions are preserved. No Git commit or push was performed by this task.

Reproduction: `_BUILD_SOURCE/wave_followup_1103/`. Lossless page manifest: `assets/game/shared/combat/sewer_pages_1103/manifest.json`. Raw captures, superseded experiments and prior movies remain under the ignored `_shots/` or workspace proof directories.
