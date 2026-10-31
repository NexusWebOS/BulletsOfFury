# Dracodia: actual mechanical gates and infector return

The first-host entrance now uses the original PixelLab mechanical gates from the same family as the green sewer gate. Purple is the `black_void` manifest alias backed by `void_rift_*` source frames; red uses `red_rift_*`. The previous energy-only `RD71_ART.gate_purple` and `gate_red` cells remain archived but are not rendered in this sequence.

The purple gate begins at5.4s and keeps the original emergence/closing timing. The red gate begins at9.2s, finishes forming at9.9s and stays open through the10.75s aim warning,12.1s data-bomb release,12.65s impact and12.9–14.0s infector return. The infector hovers visibly in front of the aperture, then flies back to the exact same centre and selects the existing authored emergence frames in reverse while entering. It is hidden inside by14.0s. The gate starts its0.8s authored closure at14.06s, and disappears by14.86s.

The native21s possession/host reveal, full5945HP first-host pool, player protection, data-bomb FOV/socket, code spiral, robotic screams, whole-shoulder breakup and later boss forms retain their existing owners. Stage7's green gate and the blue ending gates are unchanged. Extra return/closure cues route through the existing shared mixer using `combatModule0927` and `warpGate`.

## Sources

- `assets/dracodia_possession_1030.js`: owning intro tick, UFO motion, gate frame selection and fixed blits. All host combat/hit/whole-arm functions remain byte-identical to the pre-change file.
- `assets/dracodia_gated_art_1031.js`: six fixed banks,144 frames total. Purple512px and red384px cells, stable centre pivots and uniform proportional offline scale per bank. Actual metal shell, portal colour and alpha are preserved from PixelLab source.
- `assets/game/levels/stage_08/effects/gated_possession_1031/`: PNGs, six editable Aseprites, authoring Lua, exact input hashes, manifest and provenance.
- `_BUILD_SOURCE/build_dracodia_gated_1031.py --aseprite <local editor>` reproduces the runtime PNGs exactly. No generation service, runtime scaling/rotation, animated opacity or compositing was added.
- `_BUILD_SOURCE/test_dracodia_gated_1031.py` and `record_dracodia_gated_1031.py` exercise the actual renderer and record the native entrance into ignored `_shots/dracodia_gated_1031/` output.

## Verification

38 targeted source/native/playback checks pass, including both full gate lifecycles, no rejected energy-only draw calls, monotonic return to the aperture, no closure over the UFO, impact before return, protected full-health handoff, whole-arm destruction, existing green gate and exact source rebuild. Actual native and decoded film frames were inspected. No game, browser, asset or audio-tap errors.

Current real-engine film: 29.013s,1280x800,30fps capture, 58.34 average native simulation fps, decoded audio mean-22.0dB / peak-6.5dB. Furious / Cole / invulnerable observer. No HP, phase or timer writes during filming. This is the entrance through full-health combat, not a new complete Stage8 fight recording.

[Watch current gated entrance](http://127.0.0.1:51046/?dracodia=gated-return-1031#clip=stage8-gated-possession). Older complete-fight footage remains available and is explicitly labelled as predating this entrance correction. New footage is local; no Git push.

Syntax checks pass for `assets/game.js` and the changed owner. Required full suite reaches its final summary and exits1 with the same five pre-existing failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

`assets/game.js` remains unchanged. Complete measured evidence: `docs/qa/dracodia_gated_1031.json`.
