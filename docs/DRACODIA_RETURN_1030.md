# Dracodia: defeated-form return and conditional limb rebuild — October30

Defeating a copied form now downloads the player back into Dracodia's native main arena, then scans his actual main body back into place. Earlier returns rebuild severed main-body limbs. On the last main life, previously destroyed limbs remain destroyed. Defeating that final life still invokes the original final destruction/reward owner.

`dracodia_return_1030.js` (RD76) handles only a defeated copied life with a surviving main pool. Living-copy morphs, first-host/rebirth choreography and an exhausted final pool retain their existing owners. A4.2s protected transfer clears native attacks, covers the arena switch at0.85s, reveals the arena, then builds the main body from1.6–4.0s. Native combat resumes at4.2s. Pause freezes the transfer; retry creates fresh state. Both local seats retain their existing positions during the covered transfer.

Repair changes limb HP/destruction state only when other copied lives remain. The original main HP, all other copy HP, defeated pools, attack cursor, final-life guard and reward accounting remain with native ownership. It never restores a defeated life or refills main HP. The return commits once.

Art:96 offline body/code-wire cells in six410x410 fixed sheets, from the existing approved16-pose V18 colossus layers. Stable205px pivot; original native410/320 proportional size baked offline. Actual existing authored download curtain and blackout tiles cover the arena transfer. New runtime graphics use fixed blits, clips, frame selection and the existing camera adapter. No new paid generation, runtime recoloring, image-alpha animation or sprite rotation/scaling. Rebuild: `_BUILD_SOURCE/build_dracodia_return_1030.py`; source hashes in the emitted provenance manifest.

Verification:67 native death/return/last-life checks across all four copied forms;17 pause/retry/Normal-Hard-Furious/live-morph boundary checks. No browser/draw errors. Required full suite exits1 with the same five known baseline failures; no new failures. Core game.js is unchanged.

Review: http://127.0.0.1:51046/?dracodia=copy-return-1030#clip=stage8-copy-arena-return

The20.48s live-engine Furious preview is explicitly a checkpoint: brain copy280HP and an already destroyed cached main left arm are prepared before filming; other life pools remain full. GOD plus an input-only aiming bot kills the copy through normal combat. No recorder HP/phase/timer writes during capture. The native defeat returns to the original5330HP main pool and rebuilds both arms. Transition interval59.05FPS; whole checkpoint54.52FPS includes combat stalls outside the transfer and is not a full-fight performance/balance claim. Audible native mixer recording mean−22.4dB, peak−4.5dB; no page/console/asset errors. Existing full fights and chapters remain available.

No commit or GitHub push in this pass.
