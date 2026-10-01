# October 1 (c): one ship size from intro to play, and no dead stops

Mike: *"a main gripe I currently have is the scaling in/out of our ship from the intro to the gameplay itself, can we please just keep it at gameplay scale at all times and not do that or any sudden stops on any levels? always remain in motion but just slow down as we get to the intro's and stuff unless its the fast levels like space and the sky levels."*

The change: `_BUILD_SOURCE/patch_launch_scale_1001c.py` (anchored edits that refuse rather than no-op, and reproduce `assets/game.js` byte for byte from the pre-change tree). Probe: `_BUILD_SOURCE/probe_launchscale_1001c.py`. Suite section: `_BUILD_SOURCE/test_launch_scale_1001c.cjs`.

## What was wrong

All of this was measured off the hull's own blits in real Chromium, before any change.

| Where | Before | Now |
|---|---|---|
| Ground launches (stages 1, 2, 3, 4, 7) | The ship flew in at 62 px, eased up to **76 px** for the countdown, then PLAY cut it to **60** at GO: a 27% pop. Cause: `playShipPose().h` still used 0810a's content-height formula, while PLAY has blitted the hull at `SHIP_DRAW_H` (60) since 0819c. | 60 px on every frame from the first launch frame into PLAY. `playShipPose().h` is `SHIP_DRAW_H`. |
| Ground launch speed | 1750 px/s eased to **0** on a 2 s clock. The level had already landed partway through that, so the world stood dead still for about 0.6 s, crawled at 24 px/s through 3-2-1, then jumped to 40 at GO. | The brake is driven by distance. It starts 2400 px short of the join and decelerates so it reaches PLAY's own **40 px/s** on exactly the frame the level lands. That 40 holds through settle, the load gate, 3-2-1 and GO into PLAY. Lowest launch speed: 40. Largest one-frame drop: 17 px/s. |
| Stage 5 (Fury intro) | The plane was drawn at **90 px**. The space fighter was built at **118 px** and shrunk to 48 during the countdown. | The plane flies at 60 px and the fighter at 48 px, both play sizes. The kit pieces still orbit at the size approved on 0914 and close down onto the play-sized craft only during the snap. The plane holds its size through the charge and tucks only under the closing snap, for about half a second. Speed stays at 1000 px/s throughout, as before. |
| Stage 9 launch | The fighter grew from **14 px** to 48 out of the portal. The brake dropped **3200 → 1750 px/s in one frame**. | 48 px from the first frame. The space brake eases from the speed it is actually flying at. |
| Outbound exit routes | The climbing ship was drawn at **38 px** against PLAY's 60. | 60 px. |
| Stage 8 rift arrival | The ship grew out of the rift from **6 px**. | Comes out at play size. |
| Stage 6 (sky) | Already enters straight into PLAY at sky cruise. | Unchanged. |

Unchanged on purpose:
- The stage 7 escape, where the rift swallows the ship (Mike asked for that shrink on 1001b).
- The somersault and roll reels.
- The boss scroll-hold. It is an eased 0.6 s stop that Mike ordered for boss and miniboss fights.

## Verification

- **probe_launchscale_1001c.py, real Chromium.** The probe identifies the hull by the image object `XART.get` / `furyShipCanvas` returned (CLAUDE.md: never by key timing or `.src`). Results:
  - Stages 1, 2, 3, 4 and 7 draw the hull at **60 px on every frame** from the first launch frame to 3 s into PLAY, with zero off-scale blits. Launch speed never drops below 40 px/s.
  - Stage 9 holds **48 px** throughout.
  - Stage 5 holds the plane at 60 through the sky and the kit orbit, tucks for 30 frames under the snap, then holds the fighter at 48 from its reveal into PLAY.
  - Zero page errors.
- **Frame sheets** in `_shots/scale1001c/` (gitignored) were inspected for the stage 2 landing and countdown and the stage 5 assembly.
- **The first version of the probe missed PLAY's hull entirely.** `_drawPlayerCore` asks `XART.get` for the hull, then calls `pf27PlaneThrustDraw` (more `XART.get` calls) before it blits. "The last key requested" therefore named the thruster, and the ship read as not drawn. The fix was to tag the returned image.
