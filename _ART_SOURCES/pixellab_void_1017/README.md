# PixelLab portal, void and final-arena sources

Mike requested PixelLab for Stage 7–8 portals/black void and the three final
arena phases. The authenticated PixelLab MCP service produced these images.
No other image generator supplies this pass. Local project reference uploads
were blocked by automatic approval review, so the accepted generation calls
used text descriptions of the game's palette, chrome and alien materials.
Subsequent animation inputs are PixelLab's own generated endpoint images.

Mike rejected the original black spiral in the next review. The live
`black_void` bank now derives from the approved PixelLab blue rift, using an
exact offline purple/black palette swap. Its 32/16/32 form/loop/close frames
keep the source alpha, silhouette, physical pivot and luminance. Saturated
blue/cyan energy becomes violet; neutral chrome and black pixels stay intact.
`manifest.json` records `derivedFrom` and the palette mode. The rejected
provider frames and earlier unregistered PNGs are preserved, never loaded as
the live void. This follow-up creates no new generation jobs.

`sources.json` records tool names, job IDs and motion/appearance prompts.
`returned/` preserves returned PNGs, including reference inputs in animation
results. Private download URLs and account credentials are not source assets.
The Codex user configuration supplies authentication only for local job tools.

The owning export is `_BUILD_SOURCE/build_pixellab_void_1017.py`. It registers
its output and `assets/pixellab_void_art_1017.js` together. Every portal uses
a fixed 320×320 canvas, pivot160,160. Every clip uses one proportional scale
(256/sourceWidth), shared transparent padding and integer translations around
the primary physical aperture. Enclosed accidental alpha holes are restored
to opaque black without changing the exterior alpha or metal/energy colors.
Only the open join plate and transparent one-shot endpoints are locked explicitly.
Closure is generated separately, never a reversed formation or scaled idle.
The native loop painter retains the established premultiplied-alpha blend.

Final arenas are opaque 512×512 authored plates, with simulation-driven code
parallax below projectiles and warnings. No arena artwork contains ships,
bosses, side walls, corridors or collision geometry. Other stage biomes and
the encounter controllers remain with their existing owners. The 400×400
phase-three source uses one proportional scale to 512×512; it has no black
padding bands that could introduce rectangular edges in the open darkness.

The accepted export contains 320 portal poses, sixteen code poses, three arena
plates and 48 compact Wind projectile poses. Wind uses native 64×64 canvases,
pivot32,32 and one shared art span per weapon family. The earlier framed
phase-three arena draft is retained as provenance but is not shipped.

All accepted banks were contact/onion reviewed and rendered through XART.get
and the actual game canvas in Chromium. See docs/PIXELLAB_VOID_1017.md and
docs/qa/pixellab_void_1017.json for the final checks and integration details.
