# Cole, pilot portraits and The Roaming Rebels — September 22

Visual catalog: `docs/PORTRAITS_REBELS_0922.html`.

## Delivered

- [x] Imported Mike's new Cole full-body PNG with its original transparency. Pilot Select, standalone cinematic poses and the Campaign cockpit use the new body. The cockpit clips the standing figure behind its dashboard.
- [x] Preserved all eight Cole ZIP portraits. Neutral, smirking, brooding and salute supply the standard idle/happy/sad/victory states; the other supplied variations are registered as additional expressions.
- [x] Generated nine 12-cell expression sheets matching the supplied pilot references, including missing speech mouths and reactions. Yuri retains his current mohawk/goatee identity. The duplicate Freezer reference is treated as one identity.
- [x] Packaged 116 menu portraits and 116 compact dialogue portraits; dialogue versions face right. Menus, roster avatars, dialogue and legacy `face_`/`port_` callers resolve to current art before cache/atlas lookup. Old source files remain archived, not used as decode fallbacks.
- [x] Generated The Roaming Rebels roster poster: three men, two women, male leader included. This was the stated assumption pending a reply to the crew-size question. The faction opposes all organizations, including Fury HQ. Poster inspiration is not imported as faction canon.
- [x] Generated five distinct transparent ship masters and normalized runtime sprites, facing south toward the player. These are registered in XART as art/editor assets; new encounter behaviors were not requested in this art pass and the existing three-ship Stage 6 encounter is unchanged.
- [x] Saved source art, full generation prompts, working roster data, build scripts and visual catalog in the repository. No atlas repack or generated-manifest edit. No commit/push.

## Working Rebel roster

| Pilot | Role | Ship |
| --- | --- | --- |
| Darius Voss | Leader | Iron Vulture |
| Nyx Calder | Infiltrator | Ghostknife |
| Rook Mercer | Enforcer | Breachhammer |
| Kaia Vane | Signal Hacker | Signal Wraith |
| Jace Riven | Interceptor | Razorjack |

These names are design proposals, adapted from the supplied concept poster rather than fixed user canon. Five members includes Voss; no sixth leader was silently added.

## Assets and provenance

- `assets/game/pilots_0922/`: original reference art, Cole ZIP images, body, nine generated sheets, normalized portraits, comm cells and `provenance.json` with prompts and measured slice rectangles.
- `assets/game/roaming_rebels_0922/`: roster poster, five original ship masters, normalized transparent sprites, five portrait crops, working `roster.json` and full generation prompts in `provenance.json`.
- Generated with built-in `image_gen`. Packaging only crops/resizes authored imagery; no procedural replacement faces or ships. No SpriteCook credits used in this pass.
- Build scripts: `_BUILD_SOURCE/build_portraits_0922.py`, `_BUILD_SOURCE/build_roaming_rebels_0922.py`. Both can rebuild from repository masters/provenance when the original import metadata is absent.
- Existing cinematic background plates with baked-in figures were not repainted in this portrait/body asset pass.

## Verification

`_BUILD_SOURCE/probe_portraits_rebels_0922.py` loads 236 registered assets in real Chromium with empty temporary storage. It checks pixel equality for legacy/current face and avatar routes for all nine pilots, captures their native dialogue, verifies Cole's body selection and Campaign intro, and renders all expressions and five ships through the game's own canvas context. Inspected Pilot Select, Cole cockpit, dialogue, expression grid and fleet. No page/console errors.

The supplied source images and all generated masters were inspected before packaging. Ship alpha channels contain genuine transparency; normalized sprites retain opaque hulls. Syntax check passed. The full regression suite reached its final summary and exited 1 with the same 75 failure names as the immediately preceding supplies baseline; no new failures. Log: `_shots/portraits_rebels_0922/test_fl_final.log`. The obsolete standing-figure assertion was updated to accept Cole's new named body asset. Game LF and test CRLF endings remain intact.
