# Creator cleanup recipes and limits

 Clean it into a sprite sheet

#### Problem 5: it isn't real pixel art

Up to 253 colours in one frame, soft edges, no shared grid. Fix: a cleanup script that keys out the background, puts every frame on one pixel grid, gives all frames one palette (26 colours for the explosion), pins the blast to the ground (mean frame-to-frame wobble 0.43 to 0.30 px) and writes a sprite sheet with JSON. With the packages from the [Quickstart](setup.md#quickstart) installed:

```text
python scripts/clean_gif.py example/explosion.gif --name explosion --mode adaptive --cell 2.6 --impact 1 --scale 1 --neutral-greys --grey-chroma 0.05 --colors 20 --out-dir out
```

Swap in your own GIF and name. In a few seconds the script splits the GIF, removes the magenta (with edge despill), brings every frame to one fixed pixel grid, maps all frames to one palette, pulls the magenta tint out of the smoke greys, anchors the blast at the bottom centre (the ground), removes frame-to-frame wobble, cleans key-colour fringe and exports.

It prints two lines: a summary and a per-frame list. Without ffmpeg it also prints a note that the review mp4 was skipped. **Expected for the example** (the summary line):

```text
{"name": "explosion", "cell_px": 2.6, "grid_score": null, "native": [122, 116], "colors_after_snap": 48, "colors_final": 26, "greys_detinted": ["#ab918e", "#5c4343", "#876c6c", "#4c3030", "#b09e9c", "#685253", "#938081", "#2d1b1c", "#e1d0c5", "#1e1011"], "biggest_frame": 8, "jitter_before": {"mean_x_step_px": 0.43, "max_x_step_px": 1.14, "max_abs_x_off_px": 2.14, "max_abs_base_off_px": 25.0}, "jitter_after": {"mean_x_step_px": 0.3, "max_x_step_px": 1.05, "max_abs_x_off_px": 2.14, "max_abs_base_off_px": 25.0}, "fringe_pixels_fixed": 102}
```

and `out/explosion/explosion_sheet.png` is pixel-identical to `example/explosion_sheet.png`.

Outputs in `out/explosion/`:

| File | What |
|---|---|
| `explosion_sheet.png` | the sprite sheet: 16 frames of 122x116 in one row |
| `explosion_sheet.json` | Aseprite-style frame rects, 80 ms per frame, `meta.anchor` (61, 115) = the pixel where the blast touches the ground, frame tags anticipation / impact / fireball / smoke, the palette |
| `explosion_contact.png` | all frames numbered on a dark backdrop: check the flash frame, the peak and the smoke |
| `explosion_x6.gif`, `explosion_x6.mp4` | review animation at x6 (the mp4 only with ffmpeg) |
| `explosion_palette.hex`, `explosion_metrics.json`, `frames/` | palette, every measured number, single frames |

The settings worth knowing, chosen by looking at the contact sheet:

- `--mode adaptive` when the GIF has no clean pixel grid (most ChatGPT GIFs); `--mode snap --cell 0` (detect the grid) when its blocks are clearly all the same size.
- `--cell` (adaptive): the GIF's height divided by the sprite height you want in game pixels. 301 / 116 = 2.6 gives a peak of about 119x114 in the 320x180 scene. Below about 1.7 the downscale stops working.
- `--impact`: the number of the white flash frame (here 1). The scene flashes, shakes and starts its debris on it.
- `--neutral-greys --grey-chroma 0.05`: only if the smoke looks tinted; 0.05 removes a slight pink tint and keeps warm brown smoke near the fire, 0.09 also catches strong purple tints.
- `--scale`: 1 here; 2 only for a coarse GIF whose peak would be too small.
- `--key green` for a green background; `--anchor left` for effects that start at the left edge (beams).
- `python scripts/clean_gif.py --help` lists every option.


## beam



From the repository folder, with the packages from the [Quickstart](setup.md#quickstart) installed:

```text
python scripts/clean_gif.py effects/beam/beam.gif --name beam --anchor left --mode adaptive --cell 2.2 --impact 4 --scale 1 --colors 14 --out-dir out
```

`out/beam/beam_sheet.png` is then pixel-identical to `beam_sheet.png` in this folder, and `out/beam/beam_sheet.json` is identical to `beam_sheet.json`. The summary line it prints:

```text
{"name": "beam", "cell_px": 2.2, "grid_score": null, "native": [200, 98], "colors_after_snap": 48, "colors_final": 20, "greys_detinted": [], "biggest_frame": 7, "jitter_before": {"mean_x_step_px": 12.06, "max_x_step_px": 64.88, "max_abs_x_off_px": 97.27, "max_abs_base_off_px": 30.0}, "jitter_after": {"mean_x_step_px": 12.06, "max_x_step_px": 64.88, "max_abs_x_off_px": 97.27, "max_abs_base_off_px": 30.0}, "fringe_pixels_fixed": 561}
```

- `--anchor left`: the origin is at the left edge, not on the ground. This skips the frame-to-frame wobble fix and the ground row, which is why the jitter numbers above are the same before and after (they follow the beam as it grows to the right; there is no wobble to fix).
- `--cell 2.2`: 216 / 2.2 = 98 px tall and 439 / 2.2 = 200 px wide.
- `--impact 4`: frame 4 (counting from 0) is the first frame where the beam reaches the right edge.
- `--colors 14`: the palette size; the script may add up to 6 accent colours (`--max-extra 6`), and this sheet ends with 20.

## Notes

- As the prompt asks, the beam reaches the right edge (frames 4 to 11 touch it), so its far end is cut flat. In the fight at the top of the main README the two beams meet at a clash point, which hides the ends.
- The fight's second, orange beam is this same sheet, mirrored and palette-swapped in Godot. That fight scene is not part of this repository.

## lightning



From the repository folder, with the packages from the [Quickstart](setup.md#quickstart) installed:

```text
python scripts/clean_gif.py effects/lightning/lightning.gif --name lightning --key green --mode adaptive --cell 1.72 --impact 6 --scale 1 --colors 16 --out-dir out
```

`out/lightning/lightning_sheet.png` is then pixel-identical to `lightning_sheet.png` in this folder, and `out/lightning/lightning_sheet.json` is identical to `lightning_sheet.json`. The summary line it prints:

```text
{"name": "lightning", "cell_px": 1.72, "grid_score": null, "native": [208, 155], "colors_after_snap": 48, "colors_final": 22, "greys_detinted": [], "biggest_frame": 6, "jitter_before": {"mean_x_step_px": 0.93, "max_x_step_px": 4.28, "max_abs_x_off_px": 2.37, "max_abs_base_off_px": 114.0}, "jitter_after": {"mean_x_step_px": 0.48, "max_x_step_px": 1.77, "max_abs_x_off_px": 3.16, "max_abs_base_off_px": 114.0}, "fringe_pixels_fixed": 159}
```

- `--key green`: the GIF's background is green, so the violet glow survives the key.
- `--cell 1.72`: 267 / 1.72 = 155 px tall and 358 / 1.72 = 208 px wide. That is close to the lower limit: below about 1.7 the downscale stops working.
- `--impact 6`: frame 6 (counting from 0) is the strike with the bright white burst at the impact point; it is also the biggest frame.
- `--colors 16`: the palette size; the script may add up to 6 accent colours (`--max-extra 6`), and this sheet ends with 22.

## Notes

- ChatGPT's real grid here is about 4 image pixels, not the 2 to 3 the prompt asked for.
- The flash frame is also the biggest frame, so the JSON's `fireball` tag is empty (from 7 to 6). The other tags: `anticipation` 0 to 5, `impact` 6, `smoke` 7 to 13.
- In the fight at the top of the main README the bolt also gets a hit-stop, 2 impact frames and a coded colour light. Those are part of the fight scene, which is not in this repository.

## fire-pillar



From the repository folder, with the packages from the [Quickstart](setup.md#quickstart) installed:

```text
python scripts/clean_gif.py effects/fire-pillar/firepillar.gif --name firepillar --mode adaptive --cell 2.5 --scale 1 --colors 20 --neutral-greys --grey-chroma 0.05 --out-dir out
```

`out/firepillar/firepillar_sheet.png` is then pixel-identical to `firepillar_sheet.png` in this folder, and `out/firepillar/firepillar_sheet.json` is identical to `firepillar_sheet.json`. The summary line it prints:

```text
{"name": "firepillar", "cell_px": 2.5, "grid_score": null, "native": [106, 143], "colors_after_snap": 48, "colors_final": 26, "greys_detinted": ["#442f2f", "#efd3d4", "#403b3d", "#3c1f1f"], "biggest_frame": 8, "jitter_before": {"mean_x_step_px": 0.86, "max_x_step_px": 3.06, "max_abs_x_off_px": 2.86, "max_abs_base_off_px": 2.0}, "jitter_after": {"mean_x_step_px": 0.49, "max_x_step_px": 1.41, "max_abs_x_off_px": 1.8, "max_abs_base_off_px": 2.0}, "fringe_pixels_fixed": 252}
```

- `--cell 2.5`: 358 / 2.5 = 143 px tall and 265 / 2.5 = 106 px wide.
- No `--impact`: the pillar has no white flash frame, so the JSON has no frame tags.
- `--neutral-greys --grey-chroma 0.05`: pulls the slight magenta tint out of the smoke greys (4 palette greys here) and keeps the warm browns near the fire.
- `--colors 20`: the palette size; the script may add up to 6 accent colours (`--max-extra 6`), and this sheet ends with 26.

## Notes

- The re-roll worked: the highest flame pixel in the GIF is at row 14 of 358, so nothing touches the top edge.
- The light for it is the painted light from step 3 of the main README: the same lit canyon as the explosion.

## eruption



From the repository folder, with the packages from the [Quickstart](setup.md#quickstart) installed:

```text
python scripts/clean_gif.py effects/eruption/eruption.gif --name eruption --mode adaptive --cell 3.4 --impact 5 --scale 1 --colors 20 --neutral-greys --grey-chroma 0.05 --out-dir out
```

`out/eruption/eruption_sheet.png` is then pixel-identical to `eruption_sheet.png` in this folder, and `out/eruption/eruption_sheet.json` is identical to `eruption_sheet.json`. The summary line it prints:

```text
{"name": "eruption", "cell_px": 3.4, "grid_score": null, "native": [91, 91], "colors_after_snap": 48, "colors_final": 24, "greys_detinted": ["#f3e5dc", "#250d0d"], "biggest_frame": 11, "jitter_before": {"mean_x_step_px": 0.41, "max_x_step_px": 1.26, "max_abs_x_off_px": 2.12, "max_abs_base_off_px": 1.0}, "jitter_after": {"mean_x_step_px": 0.37, "max_x_step_px": 1.7, "max_abs_x_off_px": 2.12, "max_abs_base_off_px": 1.0}, "fringe_pixels_fixed": 127}
```

- `--cell 3.4`: 308 / 3.4 = 91 px. A bigger cell than the other effects on purpose: the volcano is far away, so the eruption is small.
- `--impact 5`: tags frame 5 as `impact`. The prompt counts frames from 1 ("frame 5: a bright burst"), the script from 0, so the white burst itself is frame 4 and frame 5 is the first frame of the full eruption. I used 5; use `--impact 4` if your scene should flash on the burst.
- `--neutral-greys --grey-chroma 0.05`: pulls the slight magenta tint out of the palette greys (2 here) and keeps the warm ash browns.
- `--colors 20`: the palette size; the script may add up to 6 accent colours (`--max-extra 6`), and this sheet ends with 24.

## Notes

- Frames 8 to 15 make the loop: going from 15 back to 8 looks like a normal frame step.
- ChatGPT did not keep the ash inside the frame: it touches the top edge from frame 7 on and the right edge from frame 8 on. In the fight at the top of the main README the volcano sits high in the background, so the cut edge is off the top of the screen.
