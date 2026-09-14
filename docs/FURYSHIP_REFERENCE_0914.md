# Furyship — approved source and production contract

Mike selected `assets/game/gravity_mode/furyship_somersault_13.png` on September 14.
The actual transparent PNG was opened and inspected, along with the sixteen-frame
somersault contact sheet. This resolves SPACE-11 (source identification only).

- Source canvas: **128 × 128**; nontransparent bounds `[19, 7, 109, 121)`.
- SHA-256: `95a0afa9fdf7bad73c6303bf9976b8385dc3b7bff0fd87f95515af677d6b1acf`.
- Top-down, nose north; narrow central spine, swept wings, paired engine pods,
  cyan exhausts, gray metal and teal panels. Preserve its exact assembled silhouette.
- Existing sixteen-frame reel has authored perspective changes. Preserve originals;
  its ordering and scale need animation review before runtime reuse. File numbering
  alone does not establish angles or an evenly timed loop.
- Current runtime `ship_base` and its twelve assembly pieces belong to a different
  atlas design. Their attachment coordinates cannot simply be reused for this craft.

## Production deliverables

Use the approved source as the identity reference for every generation job. Produce
one consistent strip per component/reel, rather than generating poses independently.
All material should have true alpha, crisp pixel clusters and clear dark outlines.
No scenery, text, checkerboard baked into pixels, new weapons or ship redesign.

1. A separable assembly kit: nose, central hull, left wing, right wing, left engine
   pod and right engine pod. Keep the existing guns with their wings. Any exposed
   joining surfaces must fit the approved hull. Adjust this decomposition if the
   reviewed art requires more joints; do not duplicate overlapping hull chunks.
2. For **each** piece: top, front, left side, back and right side views, plus coherent
   turn/pitch strips for the swirling assembly. These require drawn perspective
   changes, not flat rotations or width squashes presented as new views.
3. A matching whole-ship barrel-roll strip. Audit the existing somersault reel for
   reuse, resolving the handoff into and out of frame 13 without a silhouette pop.
4. Separate twin-thruster ignition and running reels, with engine-mouth anchors.
5. Separate assembly energy, joint-lock bursts and a transition veil. Swirling
   pieces stay readable before the veil briefly covers the sky/space handoff; then
   the finished hull and background emerge. Avoid a prolonged opaque white wash.
6. Reusable speed streak/wake reels, independent of pilot and stage, with documented
   direction, origin, loop timing and fade-out behavior.

## Alignment and integration gates

Keep the 128-pixel source coordinate system with the whole-ship center at `(64,64)`.
Record each component's actual socket and local pivot after reviewing generated
top views. Use one scale across all views of a piece, retaining empty space when
it turns edge-on. An exploded-view proof must reassemble into the approved source
at the same size before the animation is accepted.

Retain steel, outlines, highlights and ordnance colors during the nine pilot
palette variants. Names remain Yamado, Moonraker, Lavender, Foxtrout, Collisto,
Janis, Aristotle, Falcon and Draven. Preserve the old fighter for `spcboy` when
the replacement is integrated.

Use a dedicated owning build workflow for new sheets/cells; do not rerun the old
atlas builder over the existing 0913a additions. Verify final assets with XART and
the game's drawImage in real Chromium, including assembly, normal flight, roll,
somersault, death, all nine palettes and the transition at native scale. Record a
live in-game clip after integration.

## Current delivery status

Mike approved the built-in image generator. Eight master sheets and 70 normalized
transparent candidate frames have now been generated and inspected in Chromium.
See [the asset delivery record](FURYSHIP_ASSETS_0914.md) for files, verification
and remaining assembly-fit/integration work. The runtime remains unchanged.


## Later September 14 addition

The pack now includes twelve new somersault poses and nine verified pilot palettes: 82 candidate frames plus 50 masks. See [somersault/palette delivery](FURYSHIP_SOMERSAULT_0914.md) for current proof and remaining integration work. Earlier counts above describe the first batch.
