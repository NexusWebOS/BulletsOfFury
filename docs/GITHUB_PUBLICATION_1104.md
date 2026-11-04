# November 4 development build

Mike authorized publication of the current build. Production source is on `main`
and `codex/build-2026-10-26`; the downloadable build is the November 4 prerelease.

## Included

- Spread Lasers and Plasma Cannons, levels I–V, their newly generated hexagonal
  icons, pickup boxes, save/load and native weapon integration. Plasma fires
  forward from both cannon mouths. Projectile silhouettes use static authored
  frames with baked 1015 brightness steps.
- ColeForge shockwave rings, ignition, smoke, shield and atomic effects, including
  Cole's green/gray warheads; editable sources, generation briefs and builders.
- Stage X power and speed pickups. The P power box now uses a real 16-view yaw
  turn with 16 matching hit views, rather than a light-only animation.
- Layered stage environments and powered Tesla coils; scrolling menu scenery;
  story/cast updates and framed Chronos dialogue.
- High-quality pilot aircraft/Furyships, Galaga-inspired regular aircraft flight,
  wave follow-ups, amber Stage 6 rounds, difficulty/readability layers and the
  recent ship-formation follow-up.

The source snapshot retains the existing completed asset retirements. Duplicate
local copies of already release-hosted Rough Riders films and temporary logs are
left on disk, outside this source publication. The previous review library is
retained; its films are not represented as recordings of the November 4 build.

## Download

Download all three `BOF-runtime-*-2026-11-04.zip` assets from the release and
extract them into the same directory. Open `BulletsOfFury-2026-11-04`, run
`START-BOF.cmd` with Python 3 installed, then visit `http://127.0.0.1:8000`.
The release includes SHA256 checksums and native-engine weapon/pickup previews.

## Verification and limits

The publication scan checks changed/new JavaScript syntax, all 645 local script
references, object-size limits and accidental credentials/signed URLs. The
downloadable ZIPs receive CRC checks and a separate packaged Chromium smoke test.
The publication receipt records those actual results.

Earlier focused real-browser evidence accompanies the individual feature notes:
114 arsenal checks, 720 asset/provenance checks, 21 generated-icon checks and
48 rotating-pickup native checks plus 36 asset checks. These are focused tests,
not a complete campaign or human-dodgeability certification.

The required full `test_fl.js` rerun exits 1 before its final summary at the
pre-existing VM setup error `difficultyHealthBaseline15 is not defined`, in
`assets/combat_polish_0927b.js:151`. No globals were stubbed and no full-suite pass
is claimed. Existing measured render/loading hitches remain documented in the
wave and pilot-quality notes.

Release: https://github.com/NexusWebOS/BulletsOfFury/releases/tag/bof-build-2026-11-04
