# Hammerboss acting — October 21, 2026

The standard and corrupted Hammerboss now use a single whole authored body per combat frame. New PixelLab reference acting supplies overhead slams, tucked jumping attacks, extended side swings, raised-hammer charging, throwing follow-through, casting, reactor/laser postures, rage, physical Chromium takeover, full-body spins and ship/ball transformations. The standard boss retains its approved hit/kneel/get-up stun and death acting. The corrupted boss gets a deep unarmed one-knee stun, with a timed hold and reverse get-up.

The references are the existing generated blue and corrupted bodies and empty-handed poses. Ship and ball endpoints were exported from the actual running game through `XART.get`/native `drawImage`, inspected, and supplied as references. No generic replacement ship was used. Source exports, job receipts, raw frames, acceptance decisions and output hashes live in `_ART_SOURCES/hammer_acting_1021/`.

## Combat integration

`assets/hammer_acting_1021.js` owns body selection after existing render owners. It suppresses retired body/casting/charged-palette/recovery plates only when an accepted replacement is ready. Existing shields, warnings, helpers, music choreography, muzzle flashes, flying weapons and terminal death retain their owners. Both native armor and energy-sheet canvases carry explicit source-key tags, including cached variants. The phase-two casting plate cannot draw extra arms over the laser pose.

The laser and released hammer paint in front of the body. Laser origin matches the chest; white damage feedback paints above colored warning fields. Thrown-weapon art warms before first release. The corrected standard throw uses its real wind-up followed by an empty-handed throw pose and eight-frame body recovery. The native projectile supplies the whole independent flying hammer; there is no second held hammer after release.

New measured hammer tips position standard leaps, charged slams, giant strikes, both side counters, corrupted jumps and both crate strikes at their existing committed targets. Existing damage/safe footprints, projectile origins, HP, damage, attack durations and difficulty books remain. Artwork does not move a warning or add an unannounced damage area. Normal, Hard and Furious keep their native timings. Body and part hit timers are never zeroed to preserve a palette.

## Art/export

- 47 runtime banks, 763 cells, 2,752,730 bytes of lossless WebP.
- Standard cells: 256 x 256, chest pivot 128,112.
- Ship transforms: 320 x 320 with shared 32-pixel transparent padding, pivot 160,144, so the entire original aircraft survives chest registration.
- Native side-counter cells: 640 x 640, pivot 320,280, one bank-wide 2.5 proportional export scale.
- Chromium remains a solid plated form after takeover; the action palette preserves black outlines and colored lights/ordnance.
- Stage5 preloads blue acting, Stage8 preloads corrupted acting. Native shared dependencies retain their owners.

The owning exporter `build_hammer_acting_1021.py` writes sheets, cells, manifests, taxonomy and provenance together. No per-frame silhouette fit or independent width/height stretch is used. Original sources are retained. Baked laser rays, invented unarmed props, duplicate ground-strike throw attempts and circular Chromium overlays were rejected rather than registered. Detailed selection is in `decisions.json`.

PixelLab displayed credit balance: $11.05 to $9.58 ($1.47 used); no active jobs remain and no top-up was purchased.

## Verification

`node --check assets/game.js` and new/runtime syntax checks pass. Full `_BUILD_SOURCE/test_fl.js`: 8,943 passing assertions, zero errors, actual exit 0 and final BUILD OK banner. `game.js` remains LF; `test_fl.js` remains CRLF.

Native Chromium: 105 checks pass, including all three difficulties, actual source-cell pixels, one body owner, real committed landing and crate contact, part/owner hit pixels, natural game-clock flash expiry and corrupted action progression. The initial expiry fixture removed an existing armor owner and correctly triggered a Chromium takeover; retaining that real owner resolved the fixture's false white-highlight comparison. No flash timer was suppressed.

Replay controls passed 33 checks before the final layer corrections; the final focused laser/throw release pass adds 7 checks on the finished runtime. A repeated full preview run stalled after corrupted slam and was stopped; its partial output is not counted. The final throw replay now calls native hammerBoomerangStart, retaining the actual committed target rather than entering spin with undefined coordinates. Final screenshots verify the clean laser and visible independent flying hammer. Reports are in `docs/qa/hammer_acting_1021.json`; temporary full logs, source contact sheets and native captures remain under ignored `_shots/hammer_acting_1021/`.

Review: `docs/previews/hammer_acting_1021/index.html`. It runs actual native encounters with a protected review pilot and offers both forms, all three difficulties and the individual attack/transition replays.

## Publication scope

Mike requested publication after finishing this pass. The upload includes the current BOF game fixes, their production art and owning build/probe workflows. Unrelated local projects, trailer/audio scratch files, private configuration and transient upload links remain outside the publication list. No incoming GitHub changes were present when checked.
