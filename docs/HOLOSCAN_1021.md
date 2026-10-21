# B.O.B. Holoscan dossier — October21, 2026

Mike selected concept02 (Holoscan / Exploded View). The tutorial now uses that direction as its live dossier. The copied Overdrive window is no longer rendered or included in tutorial readiness/decode dependencies. Its source record remains for reproducibility.

## Live design

A newly generated empty cyan/black BOF scan frame supplies preserved corners, dark grid and holographic floor; the accepted concept supplies the floor dais. All delivered crops are even-sized. The frame uses corner-preserving nine-slice edges, not a stretched portrait plate. The new frame assets total1,183,916bytes. No new robot or animation generation was purchased: the four accepted PixelLab32-pose turntables are reused.

The full-unit view separates the actual missile pod, ice reactor and cannon. Four selectors include the complete assembled unit and each independent module. Dragging, native left/right or the turn buttons change the authored yaw frames. No flat-image spinning is used. Native up/down and Back retain their existing meanings. Live text uses the corrected BOF Iron Signal font; names and values remain text, rather than baked concept lettering.

Desktop uses the large exploded view, four thumbnails and three bottom intelligence panels. Compact screens use a horizontal part selector and one focused detail panel. Very short displays scroll inside the bounded window and keep Deploy available, preserving readable text instead of shrinking the whole page. Native screenshots cover1920×1080,1366×768,768×1024,390×844,320×568 and844×390. All text fits its regions; dimensions are even.

## Actual combat data

`BOB20_SPEC` in `assets/instructor_bob_1020.js` is shared by the exam spawn and dossier: missile90HP, cannon110HP, reactor240HP, total440HP. Both pods gate the ice reactor. Native fire damage is×1.5, ice×0.5; exposed-core missiles are×2. The concept's invented dimensions, cryogenic cannon description and blanket armor claims are not presented as game rules. The live cannon remains a steel FOV cannon; the launcher owns ground strikes.

The pointer Deploy button queues the native card confirm; the original3.8s scan gate and lesson completion own progression. The card continues to freeze combat/ammo/stage scheduling. Start opens the actual pause/skip menu and temporarily hides the modal. Resume preserves selection and auto-rotation preference. Reduced-motion settings stop automatic rotation while keeping manual turns. A closed/exited dossier releases its canvas buffers. The existing tutorial render tick drives the UI; no additional animation loop or per-frame pixel readback was added.

## Ownership and reproduction

- Runtime: `assets/holoscan_dossier_1021.js` and its scoped CSS, loaded after the native instructor and latest combat owners.
- Art: `assets/game/shared/ui/holoscan_1021/`.
- Sources and prompt provenance: `_ART_SOURCES/holoscan_1021/`.
- Builders: `_BUILD_SOURCE/build_holoscan_1021.py` and `build_holoscan_review_1021.py`.
- Native probes: `probe_holoscan_1021.py`, `probe_instructor_bob_1020.py`, `check_holoscan_review_1021.py`.
- Review: `_shots/holoscan_1021/review.html`; its interactive iframe uses the existing save-isolated preview bootstrap. Native selection, deploy and restart were checked against unchanged persistent storage.

The legacy turntable probe observed `ctx.drawImage` on the gameplay canvas. Its observer now watches the actual selected DOM thumbnail canvas. The four-bank/four-yaw distinct-source-rectangle assertion is retained, and the initial old-observer26/27 report is preserved beside the final27/27 result. Native damaged-pixel, weakness, missile, audio, module removal and handoff assertions remain.

## Verification

- Full required regression:8943 assertions; final BUILD OK / zero errors; exit0.
- msedge:46 passing checks; zero browser/page/resource errors.
- chrome:29 passing checks; zero browser/page/resource errors.
- firefox:29 passing checks; zero browser/page/resource errors.
- tutorial combat:27 passing checks; zero browser/page/resource errors.
- interactive review:8 passing checks; zero browser/page/resource errors.

Core `game.js`, the regression harness and existing pilot art remain unchanged. The instructor owner now reads shared stats and accepts the pointer confirm queue; its combat numbers are preserved. Native audio remains owned by the shared mixer. Cole’s likeness is still unapproved, and the other eight pilots’ new cinematic banks remain on hold. No GitHub publish was requested or performed.
