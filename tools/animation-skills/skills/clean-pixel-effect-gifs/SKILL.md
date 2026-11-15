---
name: clean-pixel-effect-gifs
description: Convert keyed AI effect GIFs into stable shared-palette sprite sheets with anchors, timing JSON and review previews using the Kasperzack cleanup workflow.
---

# Clean pixel effect GIFs

Bundled scripts are MIT copies of Kasperzack Games' kit at revision d25ce128ac5f2487e8187d0f1c6f4ac27dced599. Work on copies in the current workspace, preserving raw files. Read [references/cleanup.md](references/cleanup.md) for the exact per-effect recipes and caveats. Install dependencies into a workspace environment using requirements.txt; they are upstream tested versions, not a guarantee for every Python/platform.

From this skill folder, the reproduced explosion recipe is:

```text
python scripts/clean_gif.py assets/explosion.gif --name explosion --mode adaptive --cell 2.6 --impact 1 --scale 1 --neutral-greys --grey-chroma 0.05 --colors 20 --out-dir WORKSPACE_OUTPUT
```

Replace WORKSPACE_OUTPUT with a concrete workspace path. Use absolute paths when running elsewhere. This script writes assets, not new animation drawings.

Choose adaptive when generated blocks do not share a real grid. Set cell from input height / desired native height (301/116 = 2.6 for this sample). Use snap with automatic cell detection only for a consistent real grid. The adaptive backend has a practical lower cell factor around 1.7 in this kit; inspect the result instead of treating that as universal.

All frames use one grid/size and one OKLab palette; cell-majority sampling and accent preservation avoid averaging away small embers. `--colors` is a base budget: up to six accents may be added. The explosion's 20 request produces 26 opaque colours. For a strict hardware budget set `--max-extra 0` and verify the resulting image. Different effects are quantized independently; a shared palette within one animation is not a shared palette across the game. This kit has no fixed-palette import option; explicitly remap/author a project palette when needed.

Use green key for violet effects and left anchor for beams. Do not apply ground jitter correction to a beam's expanding silhouette. Neutral-grey correction is optional for visibly magenta-tinted smoke. Impact indices are zero-based; inspect the actual flash frame. Tags may be absent (pillar) or empty (lightning fireball range 7..6); importers must skip invalid ranges.

Outputs include native PNG sheet, JSON rects/durations/anchor/tags/palette, individual frames, .hex palette, metrics, contact sheet and review GIF; review MP4 requires ffmpeg. Preserve fixed cells and origins; avoid independent tight crops. JSON anchor is a local point, not a world coordinate.

Verify frame count, native size, binary transparency, palette count, exact durations, bounds and anchor placement. Inspect contact sheet plus moving playback at native size and integer enlargement against dark and light backgrounds. Check halo/fringe, missing sparks, smoke hue, clipping and unwanted registration movement. Compare sample pixels with the bundled expected sheet when reproducing the example. Metrics alone do not approve visual quality or native-console compliance.

Source: [creator kit](https://github.com/kasperzackgames/chatgpt-pixel-effects), LICENSE included. Use sibling `prompt-pixel-effect-animations` for generation, and `stage-pixel-effect-impact` for timing/integration.
