# Furyship somersault and pilot palettes — September 14

Mike requested the somersault frames and continued the authorized image-generation
work. A new twelve-pose forward-pitch sheet is saved as
`_ART_SOURCES/furyship_0914/somersault.png`. Exact generation and correction prompts
are in `somersault_prompts.json`. Two checkerboard-background attempts were rejected;
the final magenta-matte master was extracted through the owning normalization build.

## Delivery

- Twelve transparent 128 × 128 somersault candidate frames, `somersault_00.png`
  through `somersault_11.png`, added to `assets/game/furyship_0914/`.
- Full forward pitch includes top surface, foreshortened rear view, rear end-on,
  underside with nose south, front end-on and recovery with nose north. This is
  distinct from the eight-pose barrel roll already delivered.
- One shared scale across all twelve frames; edge-on heights remain short. The
  frame catalog records a nominal 20 fps / 0.6-second one-shot sequence. The
  viewer intentionally plays more slowly for inspection.
- Fifty blue/cyan masks cover all thirty component views, eight roll poses and
  twelve somersault poses. They reuse the existing atlas owner's `blue_mask`
  function without importing or executing its top-level atlas rebuild.
- All nine pilot palettes use the actual game's existing color, luminance and
  model-name values. `palette.js` uses the same masked canvas compositing as the
  game's `spaceAtlasCanvas`; it does not recolor neutral steel or outlines.
- `preview.html` now includes the somersault reel and pilot selection. The pack
  has **82 candidate frames plus 50 supporting masks**, not 132 animation frames.
  `catalog.js` and `pack.json` are generated together by `build.py`.

## Verification

Real Chromium loaded and drew 82 candidates plus the approved reference through
XART and the game's canvas: **83 assets**, with no page, console or loop errors.
All **450 palette combinations** (50 frames × 9 pilots) were rendered. A pixel
comparison found **zero changed channels outside the palette masks**. Palette
colors, luminance multipliers and all nine model names matched the runtime.
The nine-pilot sheet and the twelve-pose somersault sheet were visually inspected.

The interactive viewer passed its twelve-reel, pause and frame-selection checks.
Proof is in `docs/qa/furyship_somersault_0914.json`; the GIF at
`_shots/furyship_0914/somersault_preview.gif` records the asset viewer, not gameplay.

## Remaining integration work

The generated reel still has wingspan variation (98–112 opaque pixels) and a
slightly different top-down hull from the original frame 13. Frame 8 is close to
the frame-9 front end-on pose. These remain animation-refinement concerns, not
failures hidden by the successful loader/palette checks. No independent frame
stretching was used to conceal them. The original sixteen-frame reel remains
untouched.

Exact assembly attachment points, smooth intermediate component turns, thruster
anchors during pitch/roll, transition timing and live gameplay verification are
still pending. The palette adapter currently belongs to the candidate viewer;
it is not installed into the game. The `spcboy` unlock is also pending.

SPACE-12 remains partial. SPACE-14 advances to partial for the verified palette
work; neither entry is marked complete. No gameplay runtime, shipping atlas,
manifest or test-suite change occurred. No gameplay-suite rerun is claimed.
Runtime SHA-256 remains
`41a0790603c5e4d8320839e1083b19a6e123e9075fce334a744825dea888d7d5`.


## Later integration update

The candidate-only status above records the earlier asset pass. The ship and effects are now installed; see [FURYSHIP_LIVE_0914.md](FURYSHIP_LIVE_0914.md) for native verification, the in-game video and remaining animation refinement.
