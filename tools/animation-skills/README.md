# ColeForge animation skills for the main PC

Portable snapshot, November 15, 2026. Includes **13 skills**, their complete
supporting scripts/references, the accepted eight-frame walk/run motion guides,
Tyler examples, exact prompts, GIF cleanup examples, and the MIT Godot staging demo.
This is a small authoring pack; it does not install or change Bullets of Fury.

## Quickstart

1. Extract **ColeForge-Animation-Skills-2026-11-15.zip** completely. Open the
   `ColeForge-Animation-Skills` folder and double-click **Install-Animation-Skills.cmd**.
   It installs to `%CODEX_HOME%\skills` when configured, otherwise
   `%USERPROFILE%\.codex\skills`. Existing copies of these skills are backed up
   under the Codex home's `skill-backups` folder. Other installed skills stay in place.
2. Restart Codex or open a new chat. The skills can now guide image generation.
3. To run the local GIF cleanup/export tools, install **Python 3.12, 64 bit**, then
   double-click **Setup-Animation-Tools.cmd**. This downloads the tested Python
   dependencies into `.venv` inside this extracted folder. Keep the folder.

No administrator access is needed for skill installation. The installer checks
every packaged file against `manifest.json` before copying and checks installed
skill hashes afterward. Advanced preview/custom destination:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -WhatIf
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Destination 'D:\MyCodex\skills'
```

To restore a previous skill, close Codex, move the new skill folder aside, then
copy that skill's saved folder from `skill-backups` back into `skills`.

## Generate walk and run animations

In Codex, attach the character's approved whole-body reference and ask:

> Use $coleforge-walk-run-frames for this character. Use the bundled walk/run
> guides for motion and my attached character for identity. Make complete drawn
> figures, preserve the same proportions and palette, and export fixed even-sized
> cells with a stable root, exact timing and a seamless loop. Inspect the whole
> animation at game size before integrating it.

The guides and Tyler examples are included locally; you do not need to find the
old SpriteCook jobs. The eight-frame guide is a reusable reference, not a limit
on the number of finished drawings. Use more authored poses when the action needs
them; keep the gait and timing coherent. Still-image generation can make an ordered
sprite sheet; it does not automatically return an animated GIF. Export/play the
frames to verify animation. Image generation requires a capable tool available
in Codex on that PC. Paid SpriteCook/PixelLab services, when requested, require
their own installed plugin, account and credits; this pack transfers no login.

The Elementalist builder under `assets/elementalist-tools` is a recovery snapshot
for an **Elementalist checkout**, not a generic standalone character generator.
Place it in that project's `openbor/tools` folder and retain the required source
inventory. It now uses `ASEPRITE_EXE` or `aseprite` on PATH, instead of a path to
this laptop's editor. Install your own licensed Aseprite separately if needed.
The generic `scripts/check_locomotion.py` checks exported metadata, not anatomy.

## Generate and clean effect GIFs

Ask Codex to use `$prompt-pixel-effect-animations`, then
`$clean-pixel-effect-gifs` and `$stage-pixel-effect-impact`. Supply your new effect
or generated GIF. Prompts, key-color guidance, anchors, timing and cleanup recipes
are bundled. The cleanup tool processes existing animation; it does not draw new
motion. A tested sample command, from this extracted folder, is:

```powershell
.\.venv\Scripts\python.exe .\skills\clean-pixel-effect-gifs\scripts\clean_gif.py .\skills\clean-pixel-effect-gifs\assets\explosion.gif --name explosion --mode adaptive --cell 2.6 --impact 1 --scale 1 --neutral-greys --grey-chroma 0.05 --colors 20 --out-dir .\output
```

This writes fixed-cell PNG frames, a sheet, JSON timing/anchor/palette metadata,
contact sheet and preview GIF. FFmpeg is optional for MP4 previews; install it
separately and put it on PATH. Godot is optional for running the separate demo.
Review the complete result for clarity, cell dimensions, palette, clipping,
registration and loop/one-shot behavior. Preview/example assets are references;
they are not automatically approved for your game.

## Included skills

| Purpose | Skill folders |
|---|---|
| Effect generation, cleanup, staging, background relighting | `prompt-pixel-effect-animations`, `clean-pixel-effect-gifs`, `stage-pixel-effect-impact`, `paint-pixel-background-relighting` |
| Whole-character locomotion and attack workflows | `coleforge-walk-run-frames`, `coleforge-beat-em-up-attack-combo-frames` |
| Shared export, graphics and tool standards | `coleforge-sprite-clarity`, `coleforge-even-frame-dimensions`, `portable-sprite-games`, `coleforge-portability`, `coleforge-art-direction`, `coleforge-sprite-tools`, `coleforge-aseprite` |

Optional genre/editor/study skills mentioned by the shared guides are outside
this focused pack. Historical project/library paths are provenance; locate your
own checkout or art library on the main PC. Their full game libraries are not
required for the bundled examples or the whole-character motion method.

## Provenance and packaging changes

Custom ColeForge instructions, motion guides and accepted examples were copied
from Mike's local skill folders. Four effect workflows include Kasperzack Games'
MIT kit, revision `d25ce128ac5f2487e8187d0f1c6f4ac27dced599`; each original LICENSE
is retained. The Godot reference contains techniques that must be adapted to the
current game's authored-graphics rules. Preserve the project instructions.

Only the exported copies were adjusted: configurable Aseprite lookup, a portable
Elementalist recovery note, repaired upstream Quickstart links, and consistent
text line endings for Git/ZIP transfers. Local original
skills remain unchanged. `requirements.txt` records the versions installed in
the clean Windows/Python 3.12 verification environment. No API credentials,
signed asset links, plugin cache or Python environment are included.
