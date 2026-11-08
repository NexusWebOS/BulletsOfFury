# Windows build publication — November8,2026

Release: https://github.com/NexusWebOS/BulletsOfFury/releases/tag/bof-windows-2026-11-06-revf
Source branch:codex/build-2026-10-26. This publishes the reviewed2026.11.06f
snapshot, including all required game graphics/audio and the native Fury HQ
launcher/installer source. The ready-game core SHA256 is
`b46bb789b6344f31d0ecba126169447d491152670c09decc6da624bc4b5d2215`.

The3,885,709,224-byte complete installer is delivered as two byte-exact parts
under GitHub's2GiB per-asset limit. The helper verifies each SHA256, concatenates
in order, verifies the whole installer and opens native setup. Installer SHA256:
`ab019939bc940a79ff41e3333787b08ac532347e71a6e0a6019fe4fff9266d37`.
The helper can retrieve missing parts from the fixed public release URLs; it
does not delete downloaded parts or change existing game saves. No credential
is embedded in any source, helper or public manifest.

All18,953 installer payload files and18,956 ZIP files were verified before
publication. Small-piece checks:14 real browser checks plus9 packaged fullscreen
checks. Full test suite retains its existing missing-helper exit1; see
SHIP_PIECE_SIZE_1106.md,STAGE5_SCENE_RESTORATION_1106.md,
TESTER_FEEDBACK_REPAIRS_1106.md and WINDOWS_LAUNCHER_REVISION_B_1106.md.

The original pending Rough Riders tutorial MP4 copies are preserved locally;
their existing review-library releases are unchanged. The new launcher and
Stage5 assembly previews accompany this release. Prior releases are retained.
