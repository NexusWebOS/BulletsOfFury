# Bullets of Fury portal redesign — October 11, 2026

This approved art now has separate forming/closing animations and shared live
playback. See [the lifecycle follow-up](PORTAL_LIFECYCLE_1011.md) for current
exports, integration and verification. The notes below describe the first
redesign's loop-only state.

Mike rejected the first portal pack because it followed the supplied GIF art
too literally. This revision uses the game's existing electrical coronas,
plasma explosions, alien chrome and machinery as the visual references. The
GIFs retain their role as motion examples. An emerald rift joins blue and red.

[Animated review](previews/portals_1011/index.html?effect=green_rift&revision=bof2).
The existing preview URL now opens the redesign. The prior pack's source files,
exports, builder and QA remain available as history.

| Loop | Visual change | Frames / fps | Canvas / pivot |
|---|---|---|---|
| Fury breach gate | Armored pylons, reactor coils and a purple plasma membrane | 32 / 24 | 512 × 640 / 256, 352 |
| Chromium singularity | Black metallic ribs, silver ridges, violet arcs and emerald traces | 32 / 20 | 320 × 320 / 160, 160 |
| Ion-blue rift | Curved plasma blades, electrical teeth, deep cobalt shadows | 32 / 24 | 320 × 320 / 160, 160 |
| Crimson rift | Matching scarlet plasma with pale hot electrical cores | 32 / 24 | 320 × 320 / 160, 160 |
| Emerald rift | Matching jade/emerald plasma with mint-white electrical cores | 32 / 24 | 320 × 320 / 160, 160 |

There are 160 main frames and 32 additional gate-membrane component frames.
The gate shell and aperture mask are separate reusable assets. The shell's
visible pixels are identical across the full gate animation. All effects now
have transparent exteriors, including the black singularity; dark apertures
retain their native near-opaque black pixels.

## Source and build

- Actual game style board and source hashes:
  `_ART_SOURCES/portals_bof_1011/reference/`.
- Built-in `image_gen` prompts, original returned PNGs and generator filenames:
  `_ART_SOURCES/portals_bof_1011/`.
- Source board owner: `_BUILD_SOURCE/prepare_portal_bof_refs_1011.py`.
- Pack owner: `_BUILD_SOURCE/build_portals_bof_1011.py`.
- Exported frames, four-column sheets, animated lossless WebPs and manifest:
  `assets/game/shared/fx/portals_bof_1011/`.
- Generated registry: `assets/portal_bof_art_1011.js`, `PR11B_ART`, `pr11b_` keys.
- Preview: `docs/previews/portals_1011/`.

The blue design was generated from actual BOF art. Red and green are generated
palette edits of that new sheet, retaining the family silhouette and phase
order. The black singularity and metal gate shell were generated independently
from the same style board. The purple membrane was generated separately so
the armor cannot drift. Its first output had transparent central holes; an
image-generation edit made the centers dark and opaque. The accepted source is
`gate-energy-opaque.png`; the original remains on disk. Exact repair prompt is
`core-opacity-repair.json`.

The generator returned 887 × 1774 animation sheets. The builder records the
rounded equal-grid source rectangles and measured black-aperture centers, then
uses integer translation and padding to produce 320 × 320 frames. All colors
and native alpha are preserved. No per-frame scaling, image rotation, invented
intermediate poses or repeated short banks are used. The gate composes one
shell at a common 0.4 scale with its membrane at a common 2.2 scale behind a
fixed mask derived from the authored opening. Native screenshot review caught
and corrected a gap where that opening narrows between the armored feet; the
mask now continues down the entire doorway. Exported sheets have equal even
cells. Maximum measured registration residual is below 0.5 pixel per axis.

The earlier `blue-tight.png` source is an identical preserved copy of the blue
output, not a rejected design. Its apparent raw-image glow is mostly low alpha;
normal composition was inspected before accepting its complete visible spikes.
Source-border alpha measurements remain in the manifest. Transparent padding
protects all exported canvas boundaries. The base black aperture and the inner
energy shape, rather than flickering external glow, determine the alignment.

## Verification

`python _BUILD_SOURCE/probe_portals_bof_1011.py` completed **61 checks, zero
failures, exit 0**, with no page, console or missing-asset errors. It checks
actual file geometry, hashes, distinct poses, black aperture opacity and fixed
gate armor, including a continuous aperture between the feet. Real Chromium
loads all 192 frames through the game's `XART`
loader and consumes every key with the game's own `drawImage`, yielding between
frame batches. Every rendered frame differs from the other poses in its bank.

The five main loops were inspected with all-frame onion sheets and native
screenshots. The preview's selector, all frame positions, pause/step, speed,
center marker, onion mode, 32-to-1 seam playback and mobile layout were checked.
Diagnostic loop-seam pixel change / median adjacent-frame change: blue 1.350,
red 1.374, green 1.394, singularity 1.360, gate 0.659. Energy deliberately changes
shape; physical centers remain registered.

QA record: `docs/qa/portals_bof_1011.json`. Native captures and onions:
`_shots/portals_bof_1011/`. Both new/updated JavaScript files pass `node --check`.
This revision changes the asset review pack, not live encounters or gameplay.
The full gameplay suite was not rerun. No commit or push was made.
