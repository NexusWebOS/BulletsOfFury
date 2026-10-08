# Windstorm and the Machinists — expansion art

Open `preview.html` through the local expansion art server to review the new roster, assembled modular tanks, Windstorm effects, and ally/player interaction animations. See `DESIGN_NOTES.md` for proposed systems and remaining art work. Graphics only; no game runtime or campaign changes.

Niel retains the user-approved character design. His selected portrait, hex ability badge and vented pickup box now match the current game UI family; see UI_STYLE_MATCH.md. The Machinists use the grounded v2 redesign requested after the first sheet looked too anime-like. Their portrait frames, hex badges and vented ability boxes now match the current game UI family. Their v1 source remains archived but is not displayed or exported into the selected identity assets.

The latest [directional and enemy pass](PASS_2.md) adds crouch-walk and prone fire in four directions for six actor families, west runs, scout/heavy patrol and combat strips, and matching Machinist UI. Review them in the updated animation viewer and `previews/pass2_*` contact sheets.

## Included

- **Niel / Windstorm:** three dialogue expressions, HUD avatar, full-body/front poses, Sirocco ship variants, Windstorm icon and box, six-phase tornado/volley/charge/impact sequences.
- **Wren, Rolf, Chaz:** grounded portraits and complete crew poses, shared squad badge, Foundry/Vector/Redline tanks, projectiles, muzzle/impact FX, special-ability FX and icons.
- **Modular tank exports:** bare hulls, separate tracks, separate turret, rear special module, damaged hull, wreck, concept art, calibrated layer canvases and actual reconstructed assemblies.
- **Phoenix and Hotwire allies:** dedicated helmeted overhead action sheets, north-facing idle/run corrections, grenade throw, roll exits, duck/prone, hit/stun, recovery, death, revive, powerup, assist-heal, and north/south firing.
- **Four shared player bodies:** wall taps, doors, wall lean, crate peek, medkit use, and noise distractions; existing movement/combat actions remain linked from the earlier on-foot package.
- **Interaction objects:** locked/unlocked/ajar/open door, sound cues, medkit pickup/open kit, heal pulses, and special icons.

## Files

`source/` contains 39 unmodified generation masters, including the rejected identity draft. `identity/`, `ship/`, `tanks/`, `players/`, `allies/`, `enemies/`, `ui/`, `fx/`, and `props/` contain the selected normalized exports. `tanks/layers/` contains transparent 256×256 modules on a common pivot, including six phases for each independent track. `cuts/` holds cropped source-resolution working assets. `atlases/` collects normalized sheets; `previews/` contains labeled contact images.

The manifest indexes 924 exported PNGs and 168 sequence definitions (including two clearly marked superseded north-run drafts; the viewer excludes them). Preview pivots are not gameplay collision bodies. `verification.json` records alpha checks and references. Identity art can reach image borders; sprite exports have clear margins. One low-alpha connection in the original tank FX sheet was split and visually reviewed.

`generation.json` records the first 17 source images; `completion-generation.json` records the six completion masters; `ui-style-match-generation.json` records three UI-match masters and their exact reference prompts. `passes-2-generation.json` records 12 directional/enemy/UI masters. `prompts.json` is an older generation snapshot before the north correction. Artwork was generated with the **built-in image_gen tool**. Sharp performs cropping, resizing, alpha-preserving extraction, and module composition. No procedural replacement sprites were drawn.

`build-assets.cjs` rebuilds derivatives using the bundled Sharp path. `make-previews.cjs`, `make-completion-previews.cjs` and `make-ui-style-review.cjs` build contact images. New animations are three/six-frame visual candidates with some shape and pose drift; directional coverage, roots, hand/muzzle sockets, track housings and loop seams still require cleanup before engine registration. The package does not claim production-ready gameplay animation or implemented stealth/AI. [COVERAGE.md](COVERAGE.md) indexes the earlier HUD, stage, weapon, enemy and map requests alongside this pass.

Serve the parent `expansion` folder so links to the earlier packages work. The existing local art server can be started with `node ../onfoot/serve-preview.cjs`; the URL is `http://127.0.0.1:8771/windstorm_machinists/preview.html`.

The selected [Machinist appearance revision](ROSTER_V4.md) gives Rolf blue hair/blue clothing, Wren black/white armor, and blond Chaz a red outfit and forehead bandana. Selected portraits, avatars and full-body poses use versioned v4 exports.
