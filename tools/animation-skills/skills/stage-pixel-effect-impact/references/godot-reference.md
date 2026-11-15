# Creator Godot reference

 Play it in Godot

#### Problem 7: it doesn't feel like a hit

Fix, in Godot: a flash, screen shake in whole pixels, a few rocks, a scorch mark, embers, and the smoke held for 1.8 s so it drifts away instead of popping. The fight at the top also uses a 4 to 6 frame hit-stop (everything freezes for 4 to 6 frames at 60 fps) and 2 black-and-white impact frames at the lightning hit and at the slam; those two are in the fight scene, not in the Godot scene here.

Open `godot/project.godot` in Godot 4.7 (Import in the project manager) and press F5. Or from a terminal, where `godot` stands for your Godot executable (on Windows the `..._console.exe` shows the printed lines; in PowerShell put `&` in front of a quoted path):

```text
godot --path godot
```

A 1280x720 window opens (the game renders at 320x180 and scales x4) and prints, among others:

```text
light: painted light from res://backgrounds/canyon_lit.png
explosion: sheet res://sprites/explosion_sheet.png  frames 13  ground (196, 159)  flash 0.4  loop period 0.0
```

The explosion repeats on its own. Keys: Space, Enter or click = explode now, L = auto loop on/off, F = flash 100% / 40% / off.

What the scene does (`main.gd`, `blast.gd`, `shaders/`):

- Plays the sheet at its JSON durations (80 ms a frame) with the sprite origin on the JSON's anchor, so the blast sits on the ground point.
- Measures each frame's fire brightness to drive the light; flashes 40% and shakes the camera in whole pixels on the frame tagged `impact`.
- Draws rocks on gravity arcs with one bounce, a scorch mark and embers in whole pixels, in colours picked from the sheet's palette. Everything is seeded, so a blast always looks the same.
- Holds the fullest smoke frame 1.8 s, lets it rise and drift, and erodes it in clean clumps from the ground up (`shaders/dissolve.gdshader`).
- Blends the background toward the lit copy by the fire's brightness under a soft radial mask, in 4 whole-pixel steps with a fixed 4x4 Bayer pattern between them (`shaders/light_painted.gdshader`). Where the two pictures are identical (sky, stars, far mist) nothing changes, so no band or seam can show.
- `project.godot`: 320x180 viewport, 1280x720 window, viewport stretch with integer scaling, nearest filter, 2D pixel snapping, Compatibility renderer. Every pixel stays square.

Your own files: copy your sheet and its JSON into `godot/sprites/` and your lit background into `godot/backgrounds/`, then pass them after a `--` (or overwrite `explosion_sheet.png`/`.json` and `canyon_lit.png`):

```text
godot --path godot -- --sheet=res://sprites/my_sheet.png --lit=res://backgrounds/my_lit.png
```

| Option (after `--`) | Default | Meaning |
|---|---|---|
| `--sheet=PATH.png` (`--json=PATH.json`) | `res://sprites/explosion_sheet.png` (the JSON next to it) | the sprite sheet from step 2 |
| `--bg=PATH.png` | `res://backgrounds/canyon.png` | the background, 320x180 |
| `--lit=PATH.png` | `res://backgrounds/canyon_lit.png` | the lit copy from step 3; `none` = a simple shader light (it also lights the sky) |
| `--x=196 --ground=159` | 196, 159 | where the blast touches the ground, in game pixels |
| `--flash=0.4` | 0.4 | full-screen flash strength on the impact frame, 0 = off |
| `--shake=1` | 1 | whole-pixel screen shake strength, 0 = off |
| `--hold-from=12` | 12 | this frame (the fullest smoke column) is held 1.8 s, rises, drifts right and erodes from the ground up; later frames are not played |
| `--layers=rocks,scorch,embers` | rocks,scorch,embers | coded extras: rocks fly out and land, a scorch mark stays, embers linger; also `sparks`, `streak`, `dust`, `spark` (the GIF has its own versions of these); `--layers=` = none |
| `--light-y=15` | 15 | centre of the light mask, this many px above the ground |
| `--volcano=1` | 1 | faint glow on the canyon's volcano top at (122, 62); 0 for any other background |
| `--first=0.4` | 0.4 | seconds before the first blast |
| `--interval=2.6` | 2.6 | seconds between the end of one blast's sprite and the next blast |
| `--loop-period=1.0` | off | one blast every N s with the same seed: a seamless loop |

Paths can be `res://...` (inside `godot/`) or absolute.

Record a clip: 8 s = 480 frames of 320x180 as PNG in `godot/capture/` (the path is relative to `godot/`). It needs a window, not `--headless`, and Godot closes by itself when done. The `.gdignore` file in that folder keeps the editor from importing the frames.

```text
godot --path godot --write-movie capture/frame.png --fixed-fps 60 --quit-after 480
```

Using the sheet in your own game: it is one row of equal frames; the JSON has each frame's rect and duration, `meta.anchor` (put the sprite's origin there and place it on the ground), the frame tags (start flash and shake on `impact`) and the palette.
