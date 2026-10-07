# Boss 4 lightning core revival — October 6

Storm Sovereign now visibly revives its shield generators: a hollow blue electrical corona gathers around the giant hull's reactor, four staggered lightning conduits reach the generator sockets, and cyan reconstruction rings pulse as the existing authored cores materialize. It runs on the existing 75%, 50% and 25% HP shield rearms. The actual rearm remains 1.08 seconds; the cosmetic afterglow finishes by 1.48 seconds. This makes core return physically legible without reinstating the previous unrelated middle-weapon flash or stale generator rendering.

## Generated art and timing

Built-in imagegen produced three four-frame clips: ship charge, horizontal conduit and socket reconstruction. The initial candidate and a targeted spacing/progression edit are archived with their exact prompts under `_ART_SOURCES/s4_core_revival_1006/`. Final source is `core_revival.png`; deployed exact copy is `assets/game/s4_core_revival_1006/core_revival.png`. The original navy/cobalt/cyan/white RGBA pixels are unchanged.

The tool returned 1448×1086 rather than the requested 1536×1152. Its four-by-three grid has 362-pixel cells and some low-alpha wisps outside the requested padding. The builder measures alpha>=24 bounds and emits exact draw rectangles with fixed per-clip pivots; rendering omits only low-alpha outer wisps beyond those bounds. It does not repaint, resample or rewrite the source image. Native review shows complete blue corona, conduit and socket forms without neighbouring-cell bleed. Metadata/provenance record the mismatch; requested padding is not treated as measured padding.

At rearm start, the hull corona gathers over 0.20 seconds and the existing electrical charge cue fires. Conduits begin at 0.16 seconds with 0.055-second offsets for each socket, then stop at 1.10 seconds. The socket clip runs with the returning core and fades through completion. Effects follow hull draw position and generator world sockets; the conduit renderer rotates the authored strip from its hull anchor to each core. The whole sequence is owned by that shield cycle. Failed duplicate rearm does not restart it. Death, an inactive field, expiry or a fresh encounter suppresses lingering effects.

Runtime `assets/s4_core_revival_1006.js` wraps the existing init/rearm/tick/overlay paths; `assets/s4_core_revival_art_1006.js` and its manifest are emitted by `_BUILD_SOURCE/build_s4_core_revival_1006.py --write`. Run the builder without arguments to verify exact source/deployed bytes and registry metadata. `index.html` loads the art and layer around the existing October 2 layer. Taxonomy key `s4rev1006` records a cosmetic revival effect. Shared `assets/game.js`, boss HP, weapon damage, shield thresholds, core targeting and rewards are unchanged.

## Verification

The full suite passes **7,485 assertions**, 32 above the 7,453 baseline, with exit 0 and the final FALVA/LIZZIE success banner. Game/layer/art syntax checks pass. The native revival probe passes **77 checks** with zero page/console errors: all twelve difficulty/HP-boundary combinations trigger actual threshold damage, hull charge precedes conduit release, all four feeds/socket reels render on the game context at the correct moving sockets, original core timing and HP remain, and effects end without looping. Death/inactive/fresh-stage cleanup and native charge-cue dispatch also pass.

The existing **101-check** Boss 4 audit passes again with the new layer loaded: ordinary fire, native held beams, curved Retina missiles, broken-target cleanup, all rearms and weaponless rams preserve the prior repairs. Combined native checks: **178**, zero errors. Native screenshots were inspected at charge, feed, reconstruction and completion. These are protected fixtures, not unassisted clears or balance proof; muted captures are not an audio audition.

Review `_shots/s4_core_revival_1006/review.html` for native checkpoints and play link. Reload BOF and enter **BOSS4** through the normal password menu. Portable QA and final hashes: `docs/qa/s4_core_revival_1006.json`. Reproduce with `node _BUILD_SOURCE/test_fl.js`, `python _BUILD_SOURCE/probe_s4_core_revival_1006.py`, `python _BUILD_SOURCE/probe_boss4_render_1006.py` and `python _BUILD_SOURCE/build_s4_core_revival_1006.py`.

Local only, uncommitted and not pushed. Earlier Boss 4 repairs, Herald transfer and Contra study remain preserved.
