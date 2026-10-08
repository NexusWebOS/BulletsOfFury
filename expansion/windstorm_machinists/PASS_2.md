# Directional infantry, alien patrols and Machinist UI

7 October 2026. Graphics and implementation notes only.

## Delivered

| Art | Coverage | Files |
| --- | --- | --- |
| Crouch-walk | North, east, south, west for regular, heavy, athletic, female, Phoenix and Hotwire | `atlases/stealth_*_4dir.png`; individual frames in `players/` and `allies/` |
| Stationary prone fire | The same six actors and four directions; six phases with fire events at zero-based frames 1 and 3 | Same atlases; `*_prone_fire_*` sequence IDs |
| West run | Six phases for all six actors, drawn facing left | `atlases/west_runs.png`; `*_run_west` sequences |
| Scout and heavy alien robots | Four-direction patrol, east firing, east hit-to-destruction | `enemies/`; `enemy_*` sequences |
| Robot rear-view correction | Six correct north-facing phases per enemy, replacing the front-facing source row | `atlases/enemy_patrol_north_fix.png` |
| Wren, Rolf and Chaz UI | Canonical 256×256 portrait/avatars, 112×112 hex ability badges, 360×400 vented pickup boxes | `identity/*_v3.png`, `ui/*_special_icon.png`, `ui/*_special_box.png` |

The package now indexes **924 PNGs and 168 sequence definitions**, with **38 preserved source masters**. This pass adds 12 masters and 414 indexed frame IDs: 408 motion exports (including 12 superseded enemy north frames), three new boxes and three avatars. Three portraits and three icons are also replaced in the selected manifest while earlier files remain on disk. The selected new animation sequences use 394 frame IDs: the 396 correctly directed frames minus two excluded Phoenix crouch phases.

Phoenix east and south crouch loops use five selected phases because one generated phase in each row changes facing. All other new strips use six. The original enemy north rows remain named `*_draft_*` for provenance and are hidden from the gallery; only the corrected rows are registered as north patrol sequences.

## Export and review

- Infantry and robot frames use transparent 96×96 canvases. New motion uses fixed source-cell anchors at `[48,48]`; muzzle-flash bounds cannot independently recenter the body. This does not eliminate the generator's pose drift.
- The four shared bodies keep cobalt paint regions for the existing pilot palette preview. Phoenix and Hotwire retain their own armor colors. Final palette masks still need authoring.
- Portraits preserve the approved grounded faces, with the actual authored frame template and the same 202×212 inner placement used for Niel. Only the frame accent colors differ. Niel's approved UI correction is retained.
- [Directional contact sheet](previews/pass2_directional.png), [enemy motion contact sheet](previews/pass2_enemies.png), [Machinist UI contact sheet](previews/machinists_ui_v3.png).
- [Exact generation prompts and original output paths](passes-2-generation.json). Generated artwork uses built-in image_gen; Sharp handles extraction, nearest-neighbor scaling and composition.

## Systems to implement later

1. Separate locomotion, stance and aim direction. Crouch movement chooses a directional loop; stationary prone fire locks translation while retaining aim. Root position must not follow image bounds.
2. Author stance transitions and collision silhouettes. Blend run/roll/prone/recovery through valid states; do not teleport between centered pictures or grant invulnerability because an animation is playing.
3. Trigger ammo use, damage, muzzle flash and noise from one committed fire event. The two illustrated flashes are timing candidates, not a requirement for two shots from every weapon. Add weapon-specific gun/grip/muzzle layers for the six weapon types.
4. Use patrol/investigate/alert/search/return AI. Wall taps and thrown distractions generate hearing events at their world locations. FOV overlays must be clipped by walls, crates and closed gates. Patrol graphics do not implement perception or pathfinding.
5. Keep the normal player one-hit death rule. Enemy health can be greater than one; nonlethal hit reactions must return to combat rather than always consuming the entire hit/death strip. Select a separate death transition only at zero health. Wrecks need explicit lifetime and collision rules.
6. Bind ability badges and boxes through pilot/tank IDs; use the same ability identifier for pickup behavior, UI and effects. Tank hull, tracks, turret and special module remain independent.

## Remaining art work before engine registration

Stabilize body roots, scale transitions between old and new sheets, hand/gun sockets, stray effect pixels, gait wraps and prone recoil. Some north/south crouch phases read as low walking and need stronger bent-knee silhouettes. Enemy south patrol weapons are carried upward while the body faces south; firing in that direction needs its own aimed pose. Cover/door/tap/roll and weapon-specific aim coverage is not complete in every direction; this is not an eight-direction production set. Existing turret, tank and air-unit art remains in the earlier on-foot package; this pass adds full patrol strips to the two biped types only.

Build with `node build-assets.cjs`; regenerate the three contact sheets with `node make-pass2-previews.cjs`. See [COVERAGE.md](COVERAGE.md) for the earlier HUD, Miami stage, weapons and campaign map.
