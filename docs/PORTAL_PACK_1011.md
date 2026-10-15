# Portals and black void — October 11, 2026

**Superseded visually:** Mike rejected the GIF-like treatment. The current
preview shows the [BOF material redesign](PORTAL_BOF_REDESIGN_1011.md), including
the new green rift. This document records the first pack; its exports remain
separate and unchanged.

Mike requested portals matching the four supplied GIFs, with at least 16–32
frames per animation, onion review and stable centers. This pack supplies four
32-frame loops, plus a separate 32-frame purple membrane and stationary gate
shell for composition. It is a generated asset review pack, not an encounter
replacement. The live game index and gameplay scripts are unchanged by this pass.

[Open the animated review](previews/portals_1011/index.html).

| Animation | Frames | Canvas | Physical pivot | Playback | Alpha |
|---|---:|---|---|---:|---|
| Amethyst gate | 32 | 512 × 640 | 256, 352 | 24 fps | Transparent outside the stone arch |
| Black void tunnel | 32 | 320 × 320 | 160, 160 | 16 fps | Opaque black tunnel layer |
| Azure teleport rift | 32 | 320 × 320 | 160, 160 | 24 fps | Native transparent outer glow |
| Crimson teleport rift | 32 | 320 × 320 | 160, 160 | 24 fps | Native transparent outer glow |
| Amethyst energy component | 32 | 320 × 320 | 160, 160 | 24 fps | Native transparent exterior |

The rifts keep their dark interiors. The tunnel retains its opaque black core
and surround; use it over black or as a cinematic layer, rather than treating
black as a transparent color key. The gate energy and shell are also exported
separately. There are 128 main drawings and 32 additional component drawings.

## References and generation

The user’s original files remain untouched. Copies, representative PNG frames
and frame counts/timing are in `_ART_SOURCES/portals_1011/reference/`:

- `portal.gif`: five poses, stored delays zero; concentric violet pulses inside
  a stationary obsidian arch. No reliable playback timing was inferred.
- `void-portal.gif`: 45 poses at 100 ms; red/violet/navy filaments spiral into a
  fixed black aperture.
- `tp.gif`: seven poses at 120 ms; blue-white energy crawls around an upright
  doorway with darker cobalt turbulence inside.
- `tp2.gif`: seven poses at 120 ms; the corresponding red teleport treatment.

Built-in `image_gen` generated complete 4-column × 8-row sheets from the
reference contact sheets. The crimson sheet also used the accepted blue sheet
to preserve the paired silhouette. The amethyst arch was generated as a separate
static plate so its masonry cannot jump with the energy frames.

Exact prompts: `_ART_SOURCES/portals_1011/prompts.json`. Native returned PNGs:
`_ART_SOURCES/portals_1011/returned/`. Source and export SHA-256 hashes are in
the reference inspection and shipping manifest. The first blue sheet crowded
the cell boundaries and was rejected; it is retained as provenance and never
registered. The accepted revision has greater margins.

## Registration and build ownership

Run `python _BUILD_SOURCE/build_portals_1011.py`. It writes the frame PNGs,
equal-cell sprite sheets, lossless animated WebPs, manifest,
`assets/portal_art_1011.js` and the `pr11_` taxonomy entry together.

The generator returned 887 × 1774 sheets rather than the requested exact grid
resolution. The builder records each rounded equal-grid source rectangle and
pads the accepted poses onto even, fixed canvases. It does not stretch each
pose to its changing visible bounds, rotate one frame into synthetic poses or
repeat a smaller bank to claim 32 drawings.

Registration follows the physical opening, not an outer flame or changing glow:

- Blue and red: center of the enclosed bright rim. Tiny gaps are closed only
  in the analysis mask; the original pixels and native alpha are preserved.
- Black tunnel: center of the contiguous dark aperture.
- Purple membrane: weighted center of the small focal spark within its dark
  surrounding gap. All bright arms are measured together. The first connected
  component approach followed individual arms and produced a visible jump;
  onion review caught it and the final build corrects it.
- Gate: one immutable shell, a fixed aperture mask, one shell scale of 0.4 and
  one membrane scale of 2.6. Energy remains behind the same opening in all poses.

Translation is rounded to whole pixels. The residual measured center error is
less than half a pixel per axis in every delivered bank. This is registration
rounding; the authored flame edges and travelling rings still change shape.
All frame and sheet dimensions are even. The main gate’s complete canvas is
512 × 640, while its physical opening center intentionally sits at 256, 352.
Use the recorded pivot, not the center of the full canvas.

## Review and verification

The review provides normal/half/quarter speed, pause, individual frame stepping,
scrub, a fixed center cross, previous/next onion overlays, and a last-four / 
first-four loop-seam mode. Dark, checkerboard and the authored alien-void arena
backgrounds are available. Downloads point to the actual generated sheets and
animated WebPs. Reduced-motion preference starts paused.

`python _BUILD_SOURCE/probe_portals_1011.py` completed **49 checks, zero
failures, exit 0**. No page, console or missing-asset errors were recorded.
It loaded all 160 frames through the real game’s `XART` loader and consumed
each key on the real game context’s `drawImage`, yielding between batches.
It verified decoded pixels, unique poses, even fixed dimensions, clear canvas
boundaries, proportional rendering and pixel-identical visible gate masonry.
The preview controls, every main-bank frame, loop boundary and mobile layout
were also exercised in Chromium.

All-frame onions and native frame-32 / frame-1 / middle-frame captures were
inspected. Mean pixel change at the loop boundary, relative to the median
adjacent-frame change: gate 0.476, void 1.093, blue 1.168, red 1.402. These are
diagnostic comparisons, not a claim that flickering energy must have identical
pixel changes every frame.

The first probe run had one false failure from comparing invisible RGB values
outside the gate. The corrected check compares visible stonework and passes.
The other 48 checks passed in that run. Final report:
`docs/qa/portals_1011.json`; native screenshots, onions and loops:
`_shots/portals_1011/`. JavaScript syntax checks passed for both new JS files.
No gameplay changed, so the full gameplay regression suite was not rerun for
this asset-only pack. No commit or push was made.
