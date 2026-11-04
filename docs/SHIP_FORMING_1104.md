# Stage 5 ship forming upgrade (November 4)

Mike: "enhance and upgrade the space ship forming effects when we turn into it. It's currently a little
janky and could certainly use a little bit more effort and effects."

**What was janky** (filmed frame by frame with `_BUILD_SOURCE/capture_ship_forming_1104.py`):
1. Charge (4.1 s) looked like drift: the kit kept orbiting with only a faint ring; nothing built up.
2. Scatter barely read.
3. Snap popped: `furyShipDrawPhase` stops drawing the parts at 78% of the snap, when they are only ~60%
   of the way in, and the finished ship appears from nothing.
4. Pixelglow did not glow the ship: `furyIntroWhite` eased the whole screen to white across it.

**Fix.** New last-loaded layer `assets/ship_forming_1104.js` (SF14; `window.SF14_OFF=1`). Wraps
`furyShipDrawPhase` and `furyIntroWhite`. Every phase clock, sound, the approved kit size/orbit
(0914/1001c), the authored veil curtain and Cole's authored assembly cells are kept. All effects use the
1015 hard-step ladder and the art's own silhouettes; no blur, no Math.random.
- Charge: energy tethers march from each docked part into the plane, brighter per charge band; a stepped
  pixel core tightens around the plane; each band tick flashes every part's silhouette cyan in turn.
- Scatter: two pixel shock rings and a white flash on the parts.
- Snap: from 78% the finished ship is covered by its own white energy silhouette and outline, and the
  parts keep closing all the way onto their lock points over it; each welds with a white flash + sparks.
- Pixelglow: the white frame steps down over 0.2 s, then the ship glows from its own silhouette (three
  outline rings, brightening, sparks). The screen whites out only in the last 45%, in hard steps.
- Cole: his authored cells stay; he gets the core, shock rings and pixelglow halo.

**Verified.** Captures before/after (standard kit pilot) and Cole on/off: identical phase timing frame for
frame, zero page errors. Review: `_shots/ship_forming_1104/ship_forming_before_after.gif`,
`snap_compare.png` (snap hand-off, before top), `a_zoom.png`, `cole_compare.png`.
Capture trap: `_pilotKey()` reads `run.pilot` first; set it, not only `pilotIndex`.
