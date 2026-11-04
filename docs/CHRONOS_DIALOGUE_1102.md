# Chronos dialogue avatars — November 2, 2026

The approved Chronos helmet portraits now appear in his shared compact dialogue panel throughout Stage5. Combat taunts previously used floating text beside his body; C113 draws those native director lines through the same avatar panel without pausing combat.

## Visible behavior

- First contact (including the unknown speaker), regular taunts, tactical armor announcements and cinematic speech use the new chrome/blue framed portrait.
- Four source views retain the canonical ribbed dome, horns and cyan U-shaped visor. Neutral covers ordinary speech; turn-right covers trap/dance taunts; turn-left covers Dodge THIS/weapon lines; stern covers armor, power, rage and terminal lines. Explicit C112 view keys remain supported.
- Native final-speech portrait whitening remains owned by SM10. Other pilots and Dracodia keep their own portraits and colors.
- The existing CD27 dialogue remains84 logical pixels high. The68px square avatar draws1:1 inside the74x68 portrait bay; alternate native24/32/40/48/56px cells are available for smaller existing bays. No runtime sprite scaling, rotation, tint or generated frame graphics were added.
- The existing director retains text timing, letter sounds, speech lifetime and combat clocks. The new overlay reuses its cursor, avoiding duplicate letter beeps.

## Ownership and rebuild

- `assets/chronos_dialogue_1102.js`: scoped Chronos routing, legacy aliases, expression selection and compact live panel.
- `assets/chronos_dialogue_art_1102.js`: fixed-size image registry. Loaded after the cast/performance and layered-stage owners in `index.html`.
- `assets/chronos_voice_1025.js`: native body/voice cue ownership retained; floating caption drawing replaced by portrait-panel metadata.
- `_BUILD_SOURCE/build_chronos_dialogue_1102.py`: offline fitting only, from the approved C112 views and CP112 chrome/blue bezel. No paid regeneration.
- `_ART_SOURCES/chronos_dialogue_1102`: source hashes, framed views and contact sheet. The generated folder includes the manifest, four512px busts,24 compact PNGs, a272x68 strip and editable four-frame Aseprite file.

Rebuild with `python _BUILD_SOURCE/build_chronos_dialogue_1102.py` using Pillow and the established Aseprite batch installation. The source path/hash manifest identifies every input. The neutral framed portrait is preserved exactly; other views use one shared source crop/aperture and bezel, fitted offline with nearest sampling.

## Verification

`python _BUILD_SOURCE/probe_chronos_dialogue_1102.py` uses the real Stage5 boss actor, native director, actual tactical announcement queue and game canvas in Chromium/Edge. It writes to ignored `_shots/chronos_dialogue_1102`.

24 focused native checks pass: all views preload; exact compact pixels and legacy alias output; portrait containment/shared height; unknown first contact; three combat expressions; actual tactical armor queue; advancing native combat/FX clocks; Decker preservation; native final portrait whitening; cinematic routing; no page/console/missing-image errors. Actual portrait/panel captures were visually inspected. Four Aseprite poses round-trip with exact RGBA equality.

Syntax checks pass for both new scripts, the changed voice owner and core. The required full suite still exits1 before its final summary with the same pre-existing `ReferenceError: difficultyHealthBaseline15 is not defined` at `assets/combat_polish_0927b.js:151` (VM harness load order). This task does not repair or hide that blocker.

This is portrait/dialogue verification, not a complete boss-balance run. Four authored still views are selected by speech; no new facial-animation bank was requested. Core `game.js` and `test_fl.js` are untouched. Existing local modifications/deletions/untracked material are preserved. No commit or push.

Machine-readable evidence: `docs/qa/chronos_dialogue_1102.json`.
