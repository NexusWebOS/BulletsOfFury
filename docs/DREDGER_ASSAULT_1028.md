# Dredger assault — October 28

Mike requested a fast ram followed by a reverse to mid-screen; visible track motion; 1015 top-cannon light and a north-facing circular warning; separated twin turrets, each with two barrels, recoil and toxic slugs.

## Current owner and art

`assets/dredger_assault_1028.js` loads after the sewer/Warden owners and is scoped to Stage7's tank. The actual native 176×192 body, 76×68 top and ER28 gun source were exported with `_BUILD_SOURCE/export_dredger_1028.py`. `_BUILD_SOURCE/build_dredger_assault_1028.py` owns the new registry, manifest and source-derived banks under `assets/game/levels/stage_07/miniboss/dredger_assault_1028/`.

- Eight authored tread phases move only the measured link bands. Native chassis distance advances them; reversing reverses them; braced fire stops them. Hull/caps/rails remain unchanged.
- Two fixed trunnions at ±43,+66; 64 baked headings ×4 shot-linked recoil phases; two actual source barrels per housing. One proportional 0.94 source scale, fixed112×112 canvas/pivot56,56. Constrained inward aim prevents overlap. Four measured per-frame sockets drive native toxic muzzle flashes and slugs. Native player beams actually hit the exposed barrel alpha from the south; Retina targets use those visible apertures.
- The actual top has a source-aligned 1015 glow companion. Three native-palette192×192 FOV cells reproject the authored broad FOV into a north-facing300-degree circle, leaving a60-degree south opening. The committed finite three-wave slug barrage uses the same angular bounds.
- The whole native hull and top retain their existing dimensions/pixels; all hit companions preserve exact source alpha. Broken turrets use this same baked twin-gun bank while the native D27 debris flight, explosion cadence and terminal blast remain in charge.

## Live behavior and ownership

The ram keeps a committed warning, accelerates over0.20–0.42s, reverses over0.66s to46% screen height, then stays vulnerable and silent for1.65s before advancing the native book. Shared mixer cues remain `bossWeaponCharge`, `enemyMachineGunHeavy`, `combatToxic0927`, `jetDash` and native module-break cues, with retrigger gates. Ordinary slugs reject interception before their first update; physical missiles and defensive clears retain their owners. Gun break removes its target and cancels its rounds; death cancels the new launcher.

The first complete recording exposed a native composite-budget defect: core exhaustion entered death with surviving gun HP still displayed. The tank-only handoff now defers death until core and both gun pools are exhausted. An empty core drops its Retina target; surviving guns keep their attacks and HP. No pools are reset or fabricated, and the final native defeat/reward runs once. Warden ownership is unchanged.

## Verification

27 native controller/render checks pass, including real turret hit pixels/expiry, exposed beam contact, source-matched sockets, non-overlap through extreme aim, moving/reversing tracks, committed ram contact, finite opening, three FOV phases, ordinary interception, break art and complete HP exhaustion. Ten export/rebuild checks pass; all outputs rebuild exactly. The existing16-check Warden rear-lunge/portal regression passes.

Final continuous native Furious fight: **112.60s**, **59.28fps**, decoded peak **-3.1dB**,12 film checks pass, no page/console/asset errors. It uses native debug entry and a labelled invulnerable input observer; no enemy HP, phase or timer writes. The complete gun/core budget is exhausted before the native defeat. File: `_shots/dredger_assault_1028/video/123215/dredger-furious.mp4`. Decoded stills and chapters accompany it. Review: `docs/previews/dredger_assault_1028/index.html`.

Eight real Chromium review checks also pass: full-film decode/load, all three decoded stills, playback advance, all seven chapter seeks, desktop/mobile fit and no video/browser errors. The page loads the local MP4 into a Blob URL because the existing8795 server does not support byte-range seeks. Desktop/mobile captures are under `_shots/dredger_assault_1028/`.

`node --check assets/game.js` and the new runtime pass. Required `node _BUILD_SOURCE/test_fl.js` exits1 before its summary on the pre-existing missing `UNUSED_ASSETS/retired_art_1022/manifest.json`. No assertion failures can be compared because the loader stops before assertions. Evidence: `docs/qa/dredger_assault_1028.json`. No game.js/test_fl.js edits, commit or push.
