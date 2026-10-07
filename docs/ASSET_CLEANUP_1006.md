# BOF asset cleanup — October 6–7, 2026

The runtime asset tree fell from **2,322,608,900 to 1,280,832,815 bytes** (about 45%).
Original pixels and audio are recoverable in `UNUSED_ASSETS/cleanup_2026-10-06/` inside
the BOF repository. This separate, Git-ignored archive contains **4,981 files /
1,044,458,415 bytes**, original relative paths, SHA-256 hashes and pre-cleanup snapshots.
Moving the archive does not free its space on the drive; it removes those assets from
the game folders and release payload.

## Changes

- Archived loose frames already packed into deployed atlases, superseded art and
  unused music, using the live browser registry, packed-cell ownership and code paths.
  Current fonts, editor data and generated combat art remain available.
- Moved all three retired prototype rig sheets out of `assets/game/atlas`.
  Their old logical registrations point to the separate archive for local art tools.
  Production stage queues exclude archive roots. A stale unconditional quad-laser
  preload was caught by the extracted ZIP and corrected before delivery.
- Removed 72 superseded portrait cells from the dialogue atlas. Its ten retained
  panels are pixel-identical; all 6,915 other cell rows are unchanged. The sheet shrank
  from 2975×3300 to 1728×1792, saving 9,361,485 PNG bytes and about 26.9 MB decoded RGBA.
  Modern portrait aliases resolve through the current October 5 renderer.
- Removed six unused music aliases from manifest/runtime assignments. Two tiny older
  sound fallbacks remain live because the regression fixtures use them; their archive
  copies also remain byte-identical.
- Stage runtime atlas builders now enumerate both live and archived editable inputs,
  prefer live files and preserve logical sort order, frame numbering and dimensions.
  Stage 4's two pre-existing builder-only extras were recorded, not used to alter its
  deployed sheet. No current art was downsampled by this cleanup.

## Verification

- Full Node suite: **7,485 assertions, zero errors, exit 0, final success banner**.
  Updated stale checks to inspect the currently deployed Stage X/map assets and packed
  roots; loaded atlas metadata in the harness in the same order as the game.
- Archive verification: all 4,981 original hashes, ten pixel-identical repacked panels,
  72 removed portrait cells and all 6,915 unchanged cells pass.
- Builder input audit: 18 checks across Stage 2–9 source keys/dimensions and nested
  archived enumeration pass.
- Native Chromium: 70 checks for nine pilots' portraits/comm poses, menus, **complete
  loading of all nine stages**, and all current ordinary/alternate/phase/donor password
  encounters. Zero page, console or missing-asset errors; zero archive requests.
- Extracted portable build: 24 checks include hashes and HTTP sizes for all 3,816
  runtime files, exact source JS/HTML bytes, nine complete stage loads, effect decoding,
  audio ranges and actual browser audio decoding. Repeated all 77 native Boss 4 revival
  checks against the BAT server. Zero errors. Both ZIP CRC checks pass and the launcher
  works from a path containing spaces.

Evidence: `docs/qa/asset_cleanup_1006.json`, `_shots/asset_cleanup_1006/`, and
workspace `output/bof-asset-cleanup-1006/portable/`. Native fixtures protect the pilot;
these checks do not constitute full campaign clears or difficulty balancing.

## New two-ZIP portable release

| ZIP | Bytes | Decimal MB |
| --- | ---: | ---: |
| BulletsOfFury-Game-and-Audio-2026-10-07.zip | 96,028,909 | 96.03 |
| BulletsOfFury-Art-Assets-2026-10-07.zip | 375,049,092 | 375.05 |

Combined size is **471.08 MB**, below 500 MB. Extract both ZIPs into the same location,
merge their `BulletsOfFury` folders, then run `PLAY_BULLETS_OF_FURY.bat`.
The launcher uses Windows PowerShell; Python and installation are unnecessary.
Original October 6 release ZIPs remain untouched.

The earlier ZIPs already excluded most loose unused donors, so the art ZIP falls by
14.71 MB even though the source asset tree falls by about 1.04 GB. The retained release
still contains large current stage, UI, portrait and cinematic art. Existing portable
conversion uses WebP quality 94–95 at original dimensions with exact alpha; fonts,
core UI and the new Boss 4/Herald effect art use lossless encoding. The archive is excluded.

## Rebuilding and recovery

Run `python _BUILD_SOURCE/atlas_cleanup_1006.py --verify` to verify this batch.
The script is the owning workflow for dialogue repacking and registration changes.
Do not re-run `--apply` against an already completed batch.

`tools/pack_stage_runtime_atlases.py` and `tools/pack_stage5_runtime_atlas.py` read
archived donors directly through `tools/art_sources_1006.py`. Older builders can list
specific source inputs with:

```powershell
python _BUILD_SOURCE/restore_art_source_1006.py --pattern "assets/game/stage3_enemy_damage/**"
```

Adding `--copy` restores missing inputs without losing the archive or overwriting newer
files. Copied inputs intentionally appear live again, so the strict cleanup verifier
will report them unless recorded as reserved files in the journal.

`python _BUILD_SOURCE/atlas_cleanup_1006.py --restore` restores the complete batch only
when the edited runtime/manifest/atlas hashes still match this journal. If later edits
exist, it refuses rather than overwriting them; recover selected files manually instead.
Preserve the archive on this computer or back it up before relocating the repository.

All changes remain local and uncommitted. Earlier Boss 4, Herald, cinematic and study
work was preserved.

## GitHub checkout after the October 7 publication

The game uses committed runtime sheets and runs without the local unused-assets archive.
The full regression suite also runs without that archive. Atlas source rebuilds still need
their original donors: preserve the local archive, or recover selected previously tracked
inputs from Git commit `3d61ff81f` before rebuilding. The archive itself is intentionally
not uploaded. The combined portable ZIP described above predates the later boss upgrades.
