# PixelLab portals, black void, final arenas and Wind rounds — October 17

Mike requested genuine PixelLab replacements for Stage 7–8 portals, black void
effects and the final arena. He also clarified that Wind MG and spread fire
need small projectiles rather than large slugs. These assets are generated,
exported and installed in the current local build.

Mike's follow-up fixes the live color assignment: Stage 7's boss entrance,
attack rifts and the portal the pilot flies into are green. Stage 8's ordinary
portals are red throughout arrival, the homeward sequence and reunion. The
separate void effects use the approved blue rift animation with a purple/black
palette; the rejected spiral is no longer a live void asset.

## Accepted art

| Family | Form | Loop | Close | Canvas / pivot |
|---|---:|---:|---:|---|
| Blue rift | 32 | 16 | 32 | 320 × 320 / 160,160 |
| Green rift | 32 | 32 | 32 | 320 × 320 / 160,160 |
| Red rift | 16 | 32 | 16 | 320 × 320 / 160,160 |
| Purple-black void rift | 32 | 16 | 32 | 320 × 320 / 160,160 |
| Code corruption | — | 16 | — | 256 × 256 / 128,128 |
| Wind MG, spread, chaingun | — | 16 each | — | 64 × 64 / 32,32 |

Three opaque 512×512 arena plates accompany the animation banks. Phase one
has dark infected material, phase two has violet data fragments, and phase
three is a nearly empty black alien abyss with distant embers. Phase three
has no floor, corridor or side architecture. Three depths of generated code
move independently, illuminate over the first four combat seconds and respond
to the existing attack-release timing. Draw-only calls cannot advance them.
The 400×400 final source uses one proportional scale to 512×512, without side
padding that would leave rectangular bands in the open darkness.

The accepted 387 PNGs occupy 6.39 MiB. Returned provider PNGs, job IDs, prompts,
checksums and the owning normalization audit remain under
`_ART_SOURCES/pixellab_void_1017/`. Private download links and credentials do
not belong in that archive. The initial framed phase-three draft was rejected
and retained only among returned sources; the open PixFlux replacement ships.

## Registration and playback

The exporter selects resolution first and excludes PixelLab's unchanged
input image from each animation response. It uses one proportional scale per
clip, shared transparent padding and integer translations around the primary
aperture. It never fits frames independently or stretches their aspect ratio.
Enclosed accidental central alpha holes are restored to opaque black while
preserving exterior transparency and authored energy/material colors.

Forming begins transparently; closing ends transparently. Both share the exact
normalized open loop pose at their joins. Closing is separately generated,
not a reversed opening. Existing `PL11` playback supplies clockwise circular
formation, premultiplied frame blending, continuous loop wrap and finite
one-shot endpoints. Escape and arrival use fixed physical canvases instead
of shrinking an idle picture to fake closure.

The void variant changes only saturated blue/cyan energy to violet. Its 80
frames retain the blue bank's exact alpha, shape, canvas and pivot. Neutral
chrome and the black aperture remain unchanged; maximum luminance change is
less than 0.5 on the 0–255 scale. Original rejected source/output pictures stay
on disk as provenance, but are absent from the registered live bank.

Every source bank has a contact sheet, onion image and GIF under the ignored
`_shots/pixellab_void_1017/export/`. All accepted poses were inspected and
rendered by the native game context through `XART.get` and `ctx.drawImage`.

## Runtime ownership

`assets/pixellab_void_1017.js` and its generated art manifest load after
`wind_refit_1017.js`. They register the PNGs, include Stage7/8 lazy-load keys
and supply the new plates to the existing encounter renderers.

The Stage7 entrance, escape and Stage8 arrival call `missionToxicPortal` /
`fr27ToxicPortal` directly. Those paths are explicitly connected to the new
green lifecycle banks; changing only `s7mBlit` would leave the old cinematic
art on screen. Attack portals retain their native owners and timing. Stage8
reformation/homeward portals retain their existing PL11 clocks; black void
casts, ground portals and Chromium's spell use the generated void poses.

`v17Route` covers both the direct effect painter and the older `pl11World`
cinematic path. It routes ordinary rifts by stage and resamples normalized
phase time when frame counts differ, preserving finite loop cadence. The
Stage8 arrival explicitly selects red, and legacy void-cell calls resolve to
the new purple-black bank. Void spells keep their separate purple identity.

The Chromium cast still exposes its native module to real damage. Targeting,
collision, actor hit flashes, boss phases, authored stage biomes and ship
movement remain with their existing owners. No new ship-bearing cinematic
plate is generated. Arena output is scoped to the three final encounters;
escape, reunion and continue scenes keep their existing environment.

Wind replaces only the three compact round appearances. The maximum-level
native captures measured MG 6×14, spread 6×13 and chaingun 8×21 visible pixels.
The existing compact painter, trajectories, firing patterns and combat stats
remain in place. Maverick homing lasers remain excluded from Wind/upgrades.

## Verification and review

- `node --check assets/game.js` and both new JavaScript modules: passed.
- Required `node _BUILD_SOURCE/test_fl.js`: 8754 passing assertions, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS`, exit 0. Previous local notes recorded 8742;
  the twelve additional assertions belong to preserved separate local work.
- `_BUILD_SOURCE/probe_pixellab_void_1017.py`: 74/74 in real Edge Chromium,
  zero page, console or asset errors. It verifies every portal key, distinct
  native poses, opaque throats, loop seams, exact phase joins, entrance/escape/
  arrival lifecycles, fixed canvases, all three arenas at both camera fits,
  combat code illumination, paused clocks, real cast-module damage and every
  Wind frame at maximum upgrade level.
- Color follow-up adds native checks for exclusively green Stage7 entrance/
  escape, exclusively red Stage8 arrival, every homeward/reunion phase, the
  shared ordinary-rift routing rule and replacement purple reformation.
  Evidence: `_shots/pixellab_portal_routing_1017/native/`. All 80 palette frames
  also pass independent alpha/pivot and luminance comparisons against blue.
- Loader content verified in Chromium is installed in `index.html`. Eight
  pre-existing source/test/launcher files retain their starting SHA-256 hashes;
  index changes consist solely of the two new loader tags.
- Installed-build boot and review-page check: 14/14, zero browser errors.
  All ten effect selections, pause, replay, scrubbing and onions work.

Structured results: `docs/qa/pixellab_void_1017.json`.
Interactive review: `docs/previews/pixellab_void_1017/index.html`, with effect
and phase selection, pause, replay, frame scrubbing and onion skinning.

Rebuild with `python _BUILD_SOURCE/build_pixellab_void_1017.py`. The exporter
owns PNG output, art manifest and taxonomy registration together.
