# Overdrive special ability art

This is an art package for Hotwire and Phoenix. It is not registered in the game runtime or an atlas. The current Bullets of Fury specials provided the visual references: the armored pickup boxes in `assets/game/atlas/ui_hud.png`, the 112x112 hex badges in `assets/game/atlas/bof_player_weapon_special_icons.png`, the existing Firewhip poses, and the ground Retina.

`manifest.json` lists the loose PNGs, dimensions, and source sheets. `expansion/tools/build_overdrive_special_art.py` rebuilds the normalized files from the untouched masters in `source/`. The frame names are ordered from `00` upward. Each frame in a sequence shares its canvas and anchor; draw the whole sequence at a fixed position rather than recentering each frame's visible pixels.

| Sequence | Frames | Canvas | Intended use |
| --- | ---: | ---: | --- |
| `frames/hotwire_whip_*.png` | 8 | 384x384 | Heated fiber-cable pullback, release, snap and recovery; cable base stays near the lower center at Hotwire's firing hand or ship mount |
| `frames/hotwire_hit_*.png` | 6 | 128x128 | Cable-tip impact that branches into lightning damage, centered on the struck enemy or screen point |
| `frames/hotwire_chain_*.png` | 8 | 256x256 | Secondary lightning spread after impact; center it on the hit location or another chained target |
| `frames/phoenix_retina_*.png` | 8 | 128x128 | Ground target ring while charging, centered about 100 game pixels north of Phoenix |
| `frames/phoenix_mortar_*.png` | 6 | 128x128 | Overhead incendiary shell descent on release, ending at the Retina center |
| `frames/phoenix_volley_*.png` | 8 | 256x256 | Initial impact followed by outward ground bursts on both sides of the strike line |

The `ui/` folder contains `special_hotwire_box.png` and `special_phoenix_box.png` at 360x400, matching the proportions of the current special pickup boxes. `spicon_hotwire.png` and `spicon_phoenix.png` are 112x112 hex badge icons. `phoenix_charge_tether.png` is a 64x256 vertical fire-line master: place its lower end at Phoenix and its upper end at the Retina, scaling its length to the gameplay distance. The Retina and tether should stay visible during charge; the mortar descends after release, then the ground volley plays at impact.

Phoenix's art uses blackened metal, ember orange, and ground fire to give Armageddon its own explosive identity. Hotwire's whip is a dark braided fiber cable with narrow hot copper seams. Its cyan energy appears at the tip and as lightning after contact; the cable itself has no fire. The first three whip frames gather tension, frames 03–06 release and snap, and frame 07 recovers. `manifest.json` includes per-frame timing in milliseconds. The animated GIFs in `previews/` show that timing on a dark background; the individual PNGs retain transparency for gameplay.

## Generation brief

The built-in image generation pass used the current special pickup boxes, five-bolt hex badges, Firewhip poses, and Retina as style references. Hotwire's revised whip sheet was prompted as eight transparent arcade cells with a shared root, distinct stored-tension, release, impact and recovery silhouettes, and a heated braided fiber cable with no flame. The revised contact sheet was prompted as six centered frames growing cyan forks from the cable-tip strike. The separate eight-frame chain sheet was prompted as lightning spreading from a common center to secondary targets without the cable visible. The earlier Hotwire source sheets remain in `source/` for comparison; the builder selects the revised sheets. The Phoenix sheets were prompted as transparent ground targeting, overhead mortar descent, and bilateral ground burst sequences, with fixed anchors within each grid. Separate prompts created the two armored pickup boxes, two hex badges, and the charge fire line. The generated masters are preserved in `source/`; the builder only crops, normalizes, adds transparent frame margins, and creates review GIFs. These are candidate assets for a later gameplay hookup, not an implemented ability.
