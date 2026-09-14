# Trailer v7 source archive

Saved on 2026-09-13 during the Codex takeover. The completed trailer is
`C:/Users/Mdogg/Desktop/BulletsOfFury_Trailer.mp4` (588,151,594 bytes).

The scripts and JSON here are exact copies from:

`C:/Users/Mdogg/AppData/Local/Temp/claude/C--Users-Mdogg-Desktop-BOF-CODE/35677c5c-4881-439b-ac67-00f94a260205/scratchpad/trailer/`

`archive_manifest.json` records the initial saved files' sizes and SHA-256 and
confirms that all 14 files matched their originals at takeover. The initial
archive totaled 312,956 bytes before this README and manifest.

Mike's approved update on 2026-09-13 replaces the closing credit with
`BUILT WITH THE ASSISTANCE OF AI & HUMAN TOOLS.` in `edit3.py` and `edl3.json`.
Those two files now differ from the initial archive hashes. The original
scratch sources remain available at the path above.

`render_endcard_0913.py` renders the updated preview and closing frame range
using the preserved compositor and the original workspace assets. It requires
`--scratch` and `--out`; `--preview-only` writes the end-card PNG without video.

`render_v7.sh` records the render sequence. Its dependencies include capture,
audio rendering, edit composition, mixing, mix verification, typesetting, phone
conversion, and still extraction. `beatmap.json` and `edl3.json` preserve the beat
timing and final edit decisions.

This is a source snapshot, not a self-contained render workspace. The generated
`takes3/` footage, audio, fonts, graphics, and other intermediate assets remain in
the original scratch folder. The scripts also contain machine-specific paths,
including the game folder and Desktop `cowboyfromhell.wav`. Audit and configure
those dependencies before rerendering from this directory. The shell recipe
requires a compatible shell, and the Python tools use libraries such as
Playwright, Pillow, NumPy, and imageio-ffmpeg.

Follow the trailer requirements in `HANDOFF_CODEX.md`: live game footage, equal
pilot time, no repeated shots or consecutive shots of one pilot, the game's own
sounds throughout, no boss name cards, and only the Tempest duel for Stage 6.
Preserve the finished trailer and original scratch files unless Mike requests
changes or cleanup.
