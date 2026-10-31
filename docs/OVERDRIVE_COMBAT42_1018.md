# Overdrive combat42 — local fixes

Build: `overdrive1018-combat42-r5`. No commit, push or deployment.

Ground infantry now keeps weapon distance, repositions between bursts, limits
simultaneous preparation/firing to two units, reconsiders stale cover and commits
its aim after an initial tracking window. Committed shots can continue toward a
last-known position after the player hides. Infantry aim cues appear briefly near
the muzzle instead of permanently filling the playfield. Fixed turrets retain
their full green/yellow/red warning lanes.

Base enemies remain on the distant defense line at root y273, with a smaller
depth scale. They hide, rise, visibly walk sideways before preparing an attack,
fire toward the viewer and reload behind cover. Their movement interval starts
while exposed; it is not consumed while hidden. Foreground rushing/vaulting is
disabled. Four turret/core waves and the existing boss progression remain.

Yuri's dedicated column-brace/pop-out and low-wall peek banks are restored. The
later combat pose layer no longer replaces these with generic crouch/fire. Near
walls sort by their real footprint rather than being forced over the player.
Prone remains **F**, crawl uses movement controls, and **Space/V/H** rolls while
prone. Cover uses **C/Shift**; firing exposes Yuri before his shot releases.

The truck stand is centered in the bed at local pivot `(300,38)`. The near rail
occludes its lower section. Yuri uses a generated 17-frame back-turn bank and a
fixed physical unit while following the turret. Phoenix, Hotwire and Niel use
new identity-referenced 5-frame seated clips. Palette, canvas, root, margins and
onion overlays were checked. The truck's body export excludes disconnected
pixels from the preceding atlas row, preserving its intended component.

Five new firing-recoil takes failed review: hands left the grips or handheld
guns appeared. They are excluded from the live manifest and preserved under
`art/combat42/rejected`. Mike chose to finish the available fixes and prepare
SpriteCook for replacement recoil and extreme-elevation grip poses. Those
dedicated poses remain the art limitation of this pass.

ColeSFX 7.5 adds 42 editable chip cues and a search/play/edit/WAV/ZIP workflow.
The game uses the existing shared mixer. Engine and flame loops have owners and
stop on pause, death and scene exit. Custom mission updates now run the shared
audio update. Starting a mission clears truck state, and vehicle audio also
checks the current mission, preventing carryover into infantry stages.

The local workstation is in `SFXGenerator/colesfx-v75`; the public V7.0 Netlify
site remains unchanged. Its deployed source and existing 1,003-sample library
were preserved without merging the unrelated NightCode remote. The new export
contains 42 WAVs, 42 editable recipes and a measured game manifest.

Verification: 37 new + 104 existing playtest + 54 combat checks pass (195 total).
The required build suite finishes `BUILD OK / 0 ERRORS`, exit 0. Chromium checks
cover actual level3 geometry/attacks and column/wall pixels, exposed base steps
of 27–31 pixels, real keyboard crate collection/boarding, and input-only truck
pursuit through ram/fade/debrief at normal health. The incoming-fire fixture
shows all 17 runner and 9 drone firing frames; 12 bullets plus 4 missiles reduce
hull from 100 to 68. All 42 WAVs decode non-silent. Engine/flame playback advances
and releases on pause/mission change. Three autoplay rejections came from a
developer fixture before native input; real-click playback succeeds.

Levels3/4 were focused/protected checks, not full unprotected human clears. The
automated truck clear is not a human difficulty verdict. Evidence and hashes:
`docs/qa/overdrive_combat42.json`, `_shots/playtest42`.

Rebuild approved art with `_research/build_art42.py`, followed by
`_research/clean_vehicle_exports42.py`. Approved raw frames and receipts are in
`art/combat42/source`. No rejected recoil bank is registered.
