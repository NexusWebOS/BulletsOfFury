# Windows launcher revision B - November 6, 2026

The game EXE now starts the actual high-quality game fullscreen immediately.
The separate **BOF Launcher.exe** opens Fury HQ, with functional minimize,
maximize/restore and close buttons and a draggable title bar. F11/Alt+Enter
still toggle the game window. Direct startup ignores an old fullscreen-OFF
launcher preference unless explicitly started with --windowed.

The regenerated hangar plate retains the approved gunmetal/amber composition.
Its title bar has the exact BOF Pixelmap Fury Strike lettering stamped offline.
Dynamic menu text still uses the same native glyph banks and centered fit.
Window-button normal/hover/restore states are authored bitmap exports. The
logical 1024x576 launcher uses integer viewport scaling and centered letterboxing.

Pilot selection has no parallax scenery or gradients. Its nine flat 5-bit-channel
palette fills follow each pilot: blue Axel, gold Decker, teal Maverick, purple
Freezer, bronze Juggernaut, red Yuri, amber Lizzie, magenta Falva, olive Cole.
The existing portrait/ship/card/stat/selection owners remain intact.

## Projectile correction and evidence boundaries

The existing live MG/sonic helper already rejected the simple uncolored test
cases. The audit found a protection gap at projectile creation (proof flags
were applied on a later update) and no canonical sonic rejection before
elemental-art classification. This pass preserves original bullet identity
at eMG/eShoot/eShootT creation, rejects bullets/sonic before element testing,
and loads a final interception invariant after the encounter wrappers.
It does not claim an isolated pre-fix ordinary-MG collision was reproduced.

In the actual packaged game, all30 overlapping gun/beam/sonic/missile/helix
collision fixtures retained the hostile shot, even with stale shootable/HP
flags and fire-colored art. The beam was created by native pShoot at level4;
other collision fixtures used the engine's normal projectile data path.
Physical emissile interception still destroyed its target. Authored defensive
clears and explicit non-bullet energy-ball mechanics keep their existing owners.

## Verification

- 12 focused native desktop/game checks passed: actual window controls,
  direct fullscreen with an OFF saved preference, SS2/noGOD normal startup,
  nine distinct single-color backgrounds,30 collision overlaps, physical
  missiles, retained mouse bindings and no browser runtime errors.
- All18777 payload files passed CRC/byte-count/SHA256 verification.
- 9 complete installer checks passed, including native safety/cancel
  self-tests, extraction of all assets, exact updated EXE/core/index/module
  hashes, and removal of only the test-owned installation afterward.
- Deep staging paths exposed a Win32 MAX_PATH failure. The host now targets
  .NET4.6.2 long-path semantics, declares longPathAware and writes validated
  extraction paths through the explicit Win32 long-path namespace. No system
  registry change/admin permission is required. The same long-path test passed.
- node --check assets/game.js passed. The required full test_fl suite exits1
  at its pre-existing missing difficultyHealthBaseline15 helper in
  combat_polish_0927b.js:151, reached from test_fl.js:4537. No full-suite pass,
  full campaign replay or constant60FPS claim is made.

The refreshed preview is real native launcher-window footage. Its sound track
uses the exact original cue PCM aligned to the actual event log; it is not a
live system-audio recording. The visual generation used built-in image_gen,
conditioned on the approved launcher plate; prompt/provenance are in ARTWORK.md
and asset-provenance.json. Existing native BOF sounds remain the cue sources.

## Deliverables

- Installer: `C:\Users\Mike\Documents\New project\Releases\BulletsOfFury-Setup-2026-11-06.exe` (3837333558 bytes)
- Installer SHA256: `2e4be3f62e1e1279931f7d5824801d95a89697cb097dd4004b29a80364acc1b4`
- Ready game: `C:\Users\Mike\Documents\New project\Releases\BulletsOfFury-Windows-2026-11-06\Bullets of Fury.exe`
- Launcher: `C:\Users\Mike\Documents\New project\Releases\BulletsOfFury-Windows-2026-11-06\BOF Launcher.exe`
- Game core SHA256: `3c7f044382ba645d43f96dd08b5089f29f1fb250e5ed190c733ba40f5d9beb98`
- Host SHA256: `99d518b5d0da6ae2e8519708269eb93f25eeb060b6ed4becd0cb9ddafbc3c974`
- Evidence: docs/qa/desktop_windows_1106/revision-b/
- Source: _BUILD_SOURCE/desktop_windows_1106/

No commit or push was requested for this revision. Existing unrelated working
tree changes and prior review videos were retained. The Windows runtime is
Microsoft-signed; the BOF host/setup remains unsigned.
