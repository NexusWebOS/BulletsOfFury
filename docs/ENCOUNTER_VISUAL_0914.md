# Stage-4 visual audit and Furnace flame shield — 0914

## Stage 4: S4-02 closed by native visual audit

The apparent long orange beams in the submitted Warden crop align with the orange road center markings. Real machine-gun shots are separate 20px sprite draws: mounted left/right spreads and paired center fire. The nine-second native capture shows the separation as the hull glides across those road lines. Shots and rockets originate at their mapped hardpoints; all four gun/rocket sound routes fire and retired blue chaingun attachments are absent.

The red upper rocket racks belong to the authored `nsb_olivewarden_intact` whole hull, matching the screenshot. They are not detached overlays or carrier helpers. The direct XART plate comparison and live Warden views preserve this approved body art. Rocket salvos retain the requested left/right mounted-turret origins. No stage-4 runtime behavior was changed in this batch.

## Furnace: S2-05 fixed

The Furnace's intro branch returned before the shared Magma Ward flame-shield renderer. It also drew its separate four-point overload wave near the end of assembly. The intro now uses the actual eight-frame flame shield throughout arrival, assembly and ignition, continuing the same family into combat. The misleading assembly overload-wave substitute is removed; the existing combat overload effect remains.

Shield initialization warms all eight frames. If a requested animation frame has not decoded, drawing holds another decoded frame from the actual flame-shield family. The intro waits for an actual shield frame before revealing its protected torso. No generic ring or placeholder is substituted.

Real hit absorption, shield break/expiry, one core-phase rearm and the deliberately unshielded head phase remain intact. This does not add new invulnerability to the head or restore a broken shield early.

## Verification

`_BUILD_SOURCE/encounter_visual_0914/probe.py` runs the actual index in Chromium through shoot's RAF trap and the existing capture clock. It records game-context drawImage calls, projectile origins and real damage/phase transitions. Sixteen native checks pass with zero page, console or game-loop errors. Native screenshots were visually inspected, including the whole Warden plate, short gun rounds, Furnace assembly and core rearm.

Both videos decode successfully: `_shots/encounter_visual_0914/Stage4_Mounted_Guns_0914.mp4` (9 seconds) and `Furnace_Real_Flame_Shield_0914.mp4` (10 seconds). These are silent debug-fight captures with capture-only invincibility and controlled phase transitions, not full-level playthroughs.

`node --check assets/game.js` passed. Full suite: 3,853 passing assertions / 57 inherited failures, final summary reached, exit 1. No new failure names against the preceding name-flair baseline. Proof: `qa/encounter_visual_0914.json`. No atlas or test-harness edits, commit or push.
