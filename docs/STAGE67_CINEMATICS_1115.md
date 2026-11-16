> Superseded post6 story, November15: FATE15 now returns through the real results/map owner with optional city/underground choice; the old direct-to7 Harrier recording below is archived evidence. See CROSSED_FATE_1115.md for both Furious outcomes and current recordings. Separate HUD canvases were omitted by the older recorder; that capture omission does not resolve the remaining Stage7 player-visibility investigation.

# November15: Stage6 to7 cinematic recording

Current original BOF, Cole/Hard, Harrier branch. Native BOFCinematicDirector.start(6) plays all11 current post6 beats: Harrier down, team check-in, orders continuing, the source below the city, bridge/drains, marking rival contacts, gear warning and staying in communication. The cleared-stage checkpoint callback calls native beginStage(7), omitting only results/map/gear menu pauses. No dialogue skip or manual advance is injected.

The recording includes the native Stage7 card, both stage7-approach panels, riverbank/sewer approach, native run/brake/settle/countdown and transition to GS.PLAY exactly once. Combat assets are decoded before recording so the fixture's loading delay is not mistaken for authored pacing. This is a cinematic checkpoint, not a Harrier fight win, full campaign recording or difficulty/balance test. The alternate rival route differs in the first aftermath line and was not separately filmed.

Movie: _shots/hq_swarm_1115/stage6-to7-full.mp4,66.70s,1824x1024 at30fps, H264/AAC with native game audio. All full-decode checks pass; browser chapters and Range206 seeking work, zero page/console/HTTP errors, audible media audio. Source receipt remains unchanged during recording. Evidence: docs/qa/stage67_cinematics_1115.json.

Observed limitation retained in the film: after the native countdown the prepared checkpoint displays terrain alone, with no visible ship/HUD in the first play frames. The player remains alive at finite coordinates (340,399.36), stage clock advances, canvas alpha1, transform2x and no browser errors. This recording does not certify the gameplay handoff visually; investigate the native campaign entry/render state separately. No Stage6-7 scene art, dialogue or gameplay code was changed for this preview.

Review: http://127.0.0.1:8766/_shots/hq_swarm_1115/review.html
Record again: python _BUILD_SOURCE/hq_swarm_1115_record.py
Package/verify: python _BUILD_SOURCE/hq_swarm_1115_package.py then python _BUILD_SOURCE/hq_swarm_1115_verify_movie.py
The packager reuses existing encoded intermediates; remove only its own named -encoded.mp4 files or use a new output directory when re-recording changed footage. Native WebM receipts remain under _shots/hq_swarm_1115/films.
