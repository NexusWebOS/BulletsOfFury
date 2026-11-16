# Ally and sibling dialogue review — November15

Mike requested the existing ally/sibling cinematics for a final dialogue optimization review. This is a review pass: no shipping story, artwork, progression, unlock or save changes.

Two complete chaptered native-audio reels are available at http://127.0.0.1:8766/_shots/ally_dialogue_1115/review.html . Both movies are1824x1024/30fps H264/AAC, fully decoded and tested through Chromium chapter seeking, browser-decoded audio and HTTP206 ranges. The two video players pause each other to prevent overlapping audio. Full timecoded Markdown/JSON transcripts and retained native lossless screenshots accompany them.

## Current scene excerpts

`_shots/ally_dialogue_1115/allies-and-siblings-full.mp4` — 2:25,34 native rows in nine chapters. Selected verbatim from the current scene builders and passed to the real director with ordinary clocks/rendering/letter audio. The reel includes the Stage3 allied-pair roundtable, Cole/Decker's full workshop and Photon Cannon sequence, the actual ending's Axel/Freezer, Falva/Lizzie, Yuri/Cole, Maverick/Cole, Decker/Cole and Juggernaut/Freezer exchanges, then the city banter and current Juggernaut Bulletalica reveal. Each chapter uses the recorded pilot identified in its receipt. These are excerpts, not full campaign transitions or playthrough wins.

Current pair exchanges are mostly shared story beats, not selected-ally-gated unlocks. The gallery identifies that distinction. Current source IDs and exact words are in `dialogue-inventory.json`, `transcript.json` and each clip's native receipts.48/48 capture/package/browser checks pass. Shipping source hashes match before/after capture and packaging.

## Retained exclusive duo scripts

`_shots/ally_dialogue_1115/archived-duo-rehearsal.mp4` — 2:04,27 dialogue lines in six separately labeled chapters: Axel lead/Freezer, Freezer lead/Axel, Falva lead/Lizzie, Juggernaut lead/Yuri, Lizzie lead/Falva, and Decker lead/Maverick. Exact words/casts are read from the existing PILOT_OPENINGS data. Only the words are rehearsed in current native comic/cockpit staging; their retired flight actions are not recreated. All sampled cockpit faces bind the newly confirmed castB-1115 family. These scripts are inactive under the current Fury crawl/selected-pilot jungle introduction. This review does not reconnect them to campaign events. The superseded sisters' grandfather-bomber banter is also preserved as transcript-only reference.

Archive proofs cover exact original wording, every row/order, current portrait receipts, six complete callbacks, native audio, full movie decode, browser chapters and media geometry, mutually exclusive players, range requests and unchanged shipping files. 33/33 checks pass. No page/console/HTTP errors on either recording or the finished review.

## Remaining observations for Mike

- Juggernaut's ending guitar insert still includes an older black-vest illustrated figure next to his current orange-vest portrait. This is visibly identified in the review; it was not silently regenerated.
- Workshop comic plates are retained as currently wired. The review does not certify every baked illustration against the newly chosen likeness references.
- Several ending lines retain short native reading windows. The recordings preserve them so Mike can judge pacing before a dialogue wrap.
- The current album request belongs to Juggernaut, with Cole answering, on the included city branch.

## Reproduce and evidence

Recipes: `_BUILD_SOURCE/ally_dialogue_1115_{record,package,archive,archive_package}.py`. Run record/package for current excerpts first, then archive/archive_package. The archive recorder reuses the same native MediaRecorder capture implementation; it never rewrites shipping scripts. Temporary output stays under `_shots/ally_dialogue_1115`. Transcripts and chapter metadata contain original shot IDs, lead pilots and scene sources. Native WebMs remain in the two `films/` directories.

Durable receipts: `docs/qa/ally_dialogue_1115.json`; detailed recording/QA data under `_shots/ally_dialogue_1115` and its `archive/` folder. Previously passing full game suite is8,969/0 from the immediately preceding stage-frame change; no new full-suite run is claimed for this artifact-only review. Engine and core tests remain byte-identical, with LF/CRLF preserved. No commit/push/installer or game-save changes.
