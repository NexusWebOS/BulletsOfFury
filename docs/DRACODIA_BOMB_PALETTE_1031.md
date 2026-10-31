# Dracodia data-bomb palette

The existing flying bomb and impact effect now use a red core, purple energy and gray/silver metalwork.38 authored frames across `bomb_charge` and `bomb_burst` were palette-swapped through Aseprite. Exact alpha, dimensions, pivots and frame ordering are unchanged; every other possession bank retains its previous PNG hash. No combat or timing code changed.

The authoritative colour mapping is the `bomb` branch in `_ART_SOURCES/dracodia_possession_1030/author.lua`; both bomb export loops call it. The existing `_BUILD_SOURCE/build_dracodia_possession_1030.py --aseprite <editor>` preserves it on future exports. Updated editable Aseprites, runtime PNGs and manifest hashes are stored with their existing owner. Source/audit: `_ART_SOURCES/dracodia_possession_1030/bomb_palette_1031.json` and `docs/qa/dracodia_bomb_palette_1031.json`.

Fresh live-engine entrance footage confirms the new bomb in flight and on impact, with correct gated portals and the infector's return. No HP, phase or timer writes during filming. Furious / Cole / invulnerable observer;29.272s, 58.55 native fps, decoded audio peak-7.0dB, no browser/game/asset/audio-tap or full-decode errors. The older gated-entrance movie remains on disk; the current review card selects this palette revision.

[Watch current entrance](http://127.0.0.1:51046/?dracodia=bomb-palette-1031#clip=stage8-gated-possession). This is an art-only palette correction; gameplay suite was not rerun. Manifest syntax and native playback were checked. No generation credits or Git push. Core engine unchanged.
