# Hammer striking faces — November 10, 2026

Mike corrected the actual contact orientation: Chronos and Dracodia must strike with an end face of the hammer head, instead of flattening the cylindrical side against the target. He reaffirmed the exact blue cylindrical and purple spiked weapon masters for all spinning frames.

## Changes

- Preserved both exact weapon masters, head/shaft geometry, clean whole-body sources, helmet designs, fixed 576×576 cells, shared root and existing material families.
- Re-authored the whole-weapon arcs offline in Aseprite. Downward strokes stop near 178–180 degrees, with the end cap pointing downward. Sideways strokes lead with the corresponding cap. The head is never turned independently of its handle.
- All 80 regular/chromium/rage attack poses use the corrected path. White and red hit material silhouettes follow the final pixels.
- Metadata now distinguishes the actual leading contact face (`tip`) from `headCenter`. Existing native landing, FOV/Retina and contact tests use the striking face. Rage throw release uses `headCenter`, so this correction does not move the detached hammer away from the visible head.
- Dracodia's landing clamp uses the contact pose's visible extents, rather than the union of every possible sweeping-weapon extent. That old union pushed the committed impact away from a center-screen target. His requested target now receives the cap contact; subsequent strikes remain planted.
- Blue 32-view detached spinning art/runtime and all three purple 64-view detached spinning materials/hit pages are unchanged. SHA256 evidence retained. No new head, handle, spike arrangement or weapon type was generated.

## Native verification

38/38 live Chromium mechanics checks passed: Normal/Hard/Furious contact counts, stable root after landing, regular/chromium/rage where applicable, actual white-hit feedback and no browser/renderer errors. Six directional geometry checks passed: contact-cap normal and authored incoming motion align on both overhead strokes and all left/right sweeps. Central target contact was verified at x340 for both copies; Dracodia's two down contacts use the same x/y.

Syntax checks passed. Required full test runner exits1 at the existing `difficultyHealthBaseline15 is not defined` in combat_polish_0927b.js:151, runner test_fl.js:4537. This is not a fully green suite claim. Core game.js is unchanged.

## Review

Fresh real native gameplay, Furious, god-mode observer with firing held off; regular and chromium sequences in each clip, original game audio:

- `_shots/hammer_face_1110/chronos-hammer.mp4` / `.gif`
- `_shots/hammer_face_1110/dracodia-hammer.mp4` / `.gif`

The approved spin preview from the prior pass remains valid because those files were not changed.

## Ownership / source

Current attack metadata is `assets/rigid_hammer_art_1110.js`, pointing to `assets/game/shared/combat/hammer_face_1110/`. `assets/boss_animation_1109.js` retains the contact/landing owner with the scoped clamp correction. `assets/rage_palm_1110.js` distinguishes head-center throw release from attack-face contact. `rigid_hammer_1110.js` and original detached spin images remain unchanged. No index/loader order change.

Editable sources, immutable masters, approved user references, offline builder and geometry audit are under `_ART_SOURCES/hammer_face_1110/`. Native verification and recorder are under `_BUILD_SOURCE/hammer_face_1110/`; the recorder shares the existing rage fixture seed/capture files. This pass supersedes the earlier overhead/side angle arrays from rigid_hammer_1110. Do not rerun that older installer over the new contact metadata.

No Git commit/push or desktop-installer rebuild in this pass.
