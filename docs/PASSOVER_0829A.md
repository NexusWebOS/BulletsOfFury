# PASSOVER 0829A — Stage 1 Combat AI, Safe VFX Frames, and Sound-Library Review

## Snapshot purpose

This is the current 2026-08-29 continuation point for Mike and the next Codex session. It is
additive to `PASSOVER_0827A.md` and the reconciled house-and-repairs build. Do not replace this
branch with an older loose-asset, pre-Gravity, pre-Velocity-Void, or pre-Stage-1-AI copy.

Canonical Git branch:

```text
codex/reconciled-house-and-repairs
```

Important completed commits immediately below this passover:

```text
c2f9a291  Add new sound library audition workspace
90f661d4  Fix Stage 1 VFX frames and expand Overlord AI
052e9f8e  Build Stage 1 platform and Jungle combat AI
```

The branch head containing this document is the handoff snapshot to pull. The sound review is
deliberately non-destructive: no new review MP3 has replaced a production sound yet.

## Work completed in this continuation

### Stage 1 roster and platform behavior

- Stage 1 enemies now use platform-specific weapons and movement rather than one generic shmup
  behavior. Jets fly committed swerves, curves, attack runs, and banking patterns; they do not
  wobble horizontally.
- Tanks stay terrain-bound, maintain unit-frame separation, face south with fixed barrels, and
  alternate rolling, pausing, cannon fire, and missile fire according to vehicle type.
- River units use their correct controllers. Boats keep water motion without side-to-side wobble;
  mines and barrels remain anchored where placed.
- Machine-gun rounds, cannon shells, Jungle missiles, green lasers, wind blades, vortices, muzzle
  flashes, and impacts are routed through the production Stage 1 combat atlas.
- The Jungle Cruiser miniboss cycles rapid twin machine-gun bursts, green laser volleys, curving
  wind blades, and slow vortex pressure. Its damaged phase accelerates the combined pattern.

### Jungle Overlord-X helicopter boss

- Actively hunts the player's left/right movement and alternates pursuit with broad banked orbits.
- Fires fast twin-machine-gun bursts and destructible homing Jungle missiles from real hardpoints.
- Uses a growing green charge glow and visible lane warning. The warning follows only during its
  early phase, then locks, guaranteeing a fair dodge window.
- Commits to that warned lane during the charge and cannot home onto a late evade.
- Leaves and re-enters continuously from a side, completes a 1.25-turn corner swirl around all
  four playfield corners, fires during the maneuver, and returns to the hunt without teleport cuts.
- Below half health, authored smoke emits from the rotor hub, the helicopter receives local visual
  shake and an angry red pulse, and its attack cadence becomes more aggressive. Collision remains
  stable while the art shakes.

### Safe Stage 1 VFX generation and atlas packing

The earlier combined generation placed effects too closely, causing missing crescents, clipped
rings, and neighboring-frame fragments. The four green effect families were regenerated as
separate six-frame horizontal strips with large gutters:

```text
_ART_SOURCES/stage1_ai_fx/spaced_v2/green_laser_spaced.png
_ART_SOURCES/stage1_ai_fx/spaced_v2/wind_blade_spaced.png
_ART_SOURCES/stage1_ai_fx/spaced_v2/wind_vortex_spaced.png
_ART_SOURCES/stage1_ai_fx/spaced_v2/green_impact_spaced.png
```

`_BUILD_SOURCE/build_stage1_combat_fx.py` now detects six complete frame groups and rejects the
build if a source frame or packed frame enters its 20-pixel safety guard. A clipped frame,
neighboring fragment, or missing group is a hard failure rather than something the game ships.

### New sound-library review workspace

The 55 MP3 files from `sounds.zip` are preserved byte-for-byte under:

```text
_ART_SOURCES/audio/sound_library_2026-08-28/raw/
```

Archive provenance and SHA-256 are recorded in:

```text
_ART_SOURCES/audio/sound_library_2026-08-28/README.md
```

The library is categorized into 11 review families:

- Automatic Weapons
- Shotguns
- Lasers & Energy Weapons
- Missiles
- Explosions & Heavy Ordnance
- Pilot Specials & Elements
- Transformation & Fusion
- Shields
- Teleport & Portals
- UI, Pickups & Radar
- Unsorted Genesis FX

The six files whose generated names were truncated to generic Genesis wording remain explicitly
unassigned. Do not guess their game events before Mike auditions them.

Technical scan results:

- 50 of 55 files peak close enough to 0 dB to require gain staging before integration.
- `16-bit_energy_buildi_#3-1787959640633.mp3` is a 10.16-second long-form transformation build.
- The following two Special Item files are byte-identical duplicates:
  - `16-bit_special_item__#4-1787959513466.mp3`
  - `16-bit_special_item__#4-1787959515674.mp3`

The review UI is:

```text
docs/sound-library-review/index.html
```

It provides waveform previews, one-player playback, category/decision/technical filters, preview
volume, category playlists, A/B comparison, persistent notes, keyboard review controls, and these
decisions: Primary, Alternate, Layer, Reserve, Reject, or Undecided.

Choices live in the browser's local storage. **Export choices** downloads
`bullets-of-fury-sound-library-decisions.json`. Mike should provide that exported file to the next
Codex session. Only then should the selected sounds be normalized, trimmed/layered as requested,
copied into `assets/game/sounds`, registered, wired, and regression-tested.

## How Mike resumes on another workstation

From the existing Bullets of Fury clone:

```powershell
git fetch origin
git switch codex/reconciled-house-and-repairs
git pull --ff-only origin codex/reconciled-house-and-repairs
python -m http.server 8772 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8772/docs/sound-library-review/index.html
```

Review the sounds, write any trim/layer/volume/use notes, click **Export choices**, and preserve the
downloaded JSON for the integration pass. Browser-local choices do not automatically travel through
GitHub; the exported JSON is the explicit handoff.

## How the next Codex session resumes

1. Confirm the active branch is `codex/reconciled-house-and-repairs` and read this file plus
   `PASSOVER_0827A.md`.
2. Confirm Mike's exported sound-decision JSON before replacing any production sound.
3. Rebuild review metadata after adding/removing source files with:

   ```powershell
   python _BUILD_SOURCE\build_sound_library_review.py
   ```

4. Serve the repository root and verify the review page with:

   ```powershell
   python _BUILD_SOURCE\test_sound_library_review.py
   ```

5. When integrating selected sounds, preserve every source MP3 and make replacements as a separate
   commit so the mapping and gain changes remain auditable and reversible.

## Verification and proof at snapshot time

- Complete game regression suite: `FALVA/LIZZIE BUILD OK, 0 ERRORS`.
- Stage 1 regression sections 264 and 265 pass, including VFX edge safety, platform weapons,
  pursuit, fair charge lock, continuous corner swirl, shootable missiles, rotor smoke, local shake,
  and angry hull tint.
- `node --check assets/game.js` — pass.
- `git diff --check` — pass.
- Sound-review browser QA — pass: 55 cards, 11 categories, all 55 MP3 URLs, all 55 waveforms,
  real playback, decisions, A/B compare, and filters.
- Sound-review JS syntax check — pass.

Live Stage 1 proof files:

```text
docs/proofs/stage1_ai_live/Stage1_Air_Naval_Enemy_AI.gif
docs/proofs/stage1_ai_live/Stage1_Armored_Enemy_AI.gif
docs/proofs/stage1_ai_live/Stage1_Jungle_Cruiser_Miniboss_AI.gif
docs/proofs/stage1_ai_live/Stage1_OverlordX_Boss_AI.gif
```

Sound-review proof and reproducible tools:

```text
docs/sound-library-review/sound-library-review-page.png
_BUILD_SOURCE/build_sound_library_review.py
_BUILD_SOURCE/test_sound_library_review.py
```

## Explicitly pending

- Mike's actual Primary/Alternate/Layer/Reserve/Reject sound choices.
- Gain staging, trimming, randomized alternates, and optional layered composites after those choices.
- Production registration and event wiring for the selected sounds.
- Interactive full-game playtesting beyond the deterministic/browser proof passes already recorded.

Do not interpret the new source library's presence in Git as approval to replace all existing SFX.
The review page exists precisely to prevent that mistake.
