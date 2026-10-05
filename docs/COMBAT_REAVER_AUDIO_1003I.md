# October 3i — modular Reaver and combat feedback

Mike requested a modular Stage 2 miniboss, generated laser beams and muzzle flashes for bosses/minibosses, and missing combat sound coverage, especially Stage 2 firewalls, Fusion, Cole VI/VII and Levels 6–8. His explicit modular request supersedes the whole-plate rule for the Inferno Reaver.

## Runtime

`assets/combat_1003i.js`, loaded after the existing October 3h layer, owns this pass. It registers its generated images through XART and its recordings through the existing lazy Snd mixer. `assets/combat_art_1003i.js` contains the measured source rectangles. No atlas was edited.

- **Inferno Reaver / Charred Inferno Reaver:** six authored components: core, two wings, two aiming/recoiling guns and nose weapon. Every part uses one transform for drawing, alpha-backed ordinary-shot collision, held-beam intersection, guided Retina targets and hardpoints. Separate part HP and flashes; breakage detaches the part, removes its lock target, cancels its active beam and prevents both named and object-based hardpoints from firing. Existing encounter HP/damage/rewards, attack book, timing and original warnings remain authoritative. Its rig is fitted below the boss gauge.
- **Laser graphics:** eighteen generated strip frames and eighteen muzzle frames across orange, cyan, green, violet, red and gold. Shared tiling and muzzle rendering cover encounter beams, Furnace, Frost/Jungle Cruiser, Hammer, Siege Bomber, Harrier, Tempest, orbital lasers, Stage 8 forms/Herald, Stage 9 sentinel and the legacy carrier paths. Warhive retains its deployed nozzle and shared tapered collision envelope; active/retraction timing and warning graphics remain intact. Small `assets/game.js` hooks cover the Mk-II, legacy Tempest and legacy Warhive renderer. The later Warhive override is handled in the new layer.
- **Audio:** twenty generated families: laser charge/burn/release, Fusion cannon, Cole VI/VII, acquisition, teleport departure/arrival, firewall arrival/burn, toxic spit, alien orb, claw lunge, metal/energy/flesh impacts, code shatter, module break and gravity pulse. Both `Audio.SFX` and direct `Snd.play` aliases resolve to the recordings. Existing kinetic, missile, fire and other appropriate recordings remain active. The silent Cyclone ram now uses the existing jet dash; the silent Turbine volley receives the generated pressure pulse. Missing Rifle Locust machine-gun and Warhive charge/roar aliases are resolved.
- **Audio lifetime:** event cooldowns prevent per-projectile sound piles. Cole loops follow actual volley creation, including co-op; release, death, pause, stage entry and story locks release or stop the new loops. Fusion still emits two piercing lances. The cruiser's beam no longer occupies the player's beam bus. Knight departure no longer layers an arrival cue; sword attacks use lunge rather than module-destruction audio.

## Generated assets and reproduction

- Built-in imagegen exact prompts/source paths: `_ART_SOURCES/combat_1003i/images.json`. Four original image outputs are preserved; the attempted alternate muzzle cleanup is inactive. Three active PNGs are copied unchanged to `assets/game/combat_1003i/`.
- Measured cells, dimensions and hashes: `assets/game/combat_1003i/manifest.json`, `cells.json`. Import owner: `_BUILD_SOURCE/import_combat_1003i.py`. This is an independent asset registration, not a generated atlas manifest edit.
- ElevenLabs Sound Effects v2 generation records and prompts: `_ART_SOURCES/combat_1003i/audio.json`, flow `csYhMmwrGgLtEOrL4TGq`. Twenty unique selected recordings; provider URLs are excluded from durable metadata.
- Untouched audio sources: `_ART_SOURCES/combat_1003i/audio_originals/`. `_BUILD_SOURCE/master_combat_1003i.py` masters from those originals, with short onset/tail ramps and loop seam treatment, then exports 160 kbps stereo MP3. It does not synthesize replacement sounds. Generated-source and runtime SHA-256 fields are distinct.
- `audio-masters.json` records decoded metrics: maximum absolute peak 0.805 or lower, zero clipped samples, largest loop boundary difference below 0.016. These are per-recording measurements, not a claim that arbitrary simultaneous game mixes can never overload.
- Taxonomy prefix `av3_` describes ownership and approved roles. Original music and previous art remain preserved.

## Verification

Final `node --check assets/game.js` and `node --check assets/combat_1003i.js` pass. The full `node _BUILD_SOURCE/test_fl.js` suite exits **0**, reaches **FALVA/LIZZIE BUILD OK, 0 ERRORS**, with **6,967 passing assertions** (previous baseline 6,958).

Real Chromium through `_BUILD_SOURCE/shoot.py`:

| Probe | Passing checks |
| --- | ---: |
| `probe_combat_1003i.py` | 36 |
| `probe_sound_roster_1003i.py` | 98 |
| Existing `probe_finale_modular_1003c.py` | 122 |
| `probe_combat_review_1003i.py` | 4 |
| **Total** | **260** |

No page or console errors in the completed runs. Combat checks exercise Normal/Furious Reaver movement, actual ordinary-projectile damage, guided missiles, disarming, held beams and encounter completion. Beam/muzzle pixels are recorded from the game context and XART access, not cached-canvas identity. Sound checks separate attack and impact routes across the Stage 6–8 roster (including the scheduled stealth-bomber replacement), decode every generated MP3 and measure all twenty through real mixer elements with an AudioContext analyser. Cole loop release and pause shutdown are verified. Existing finale regression covers all eight forms, attacks, destructible emitters, powered sword and final reward.

Early probe failures caught actual missing Cyclone/Turbine sound routes and the later Warhive renderer overriding the original hook; these were fixed. Additional fixture corrections handled the intentional null return from scheduled stealth-bomber spawns, reset Reaver movement before collision tests, and captured carrier beams through the world camera. Initial generation polling returned only a truncated subset of media; batched retrieval plus the importer's unique-20 assertion corrected that before final verification. No outstanding failures in this pass.

Portable report: `docs/qa/combat_1003i.json`. Screenshots, full logs and the interactive review stay under ignored `_shots/combat_1003i/`. `_BUILD_SOURCE/review_combat_1003i.py` builds the review with a playable Reaver encounter, actual screenshots, six-color beam contact sheet and twenty sound controls. Review URL: `http://127.0.0.1:8794/_shots/combat_1003i/review.html`.

These are controlled gameplay and mixer checks, not campaign clears or a final subjective listening/balance approval. The changes are local and uncommitted; preserve the preexisting dirty work. `assets/game.js` remains LF; `_BUILD_SOURCE/test_fl.js` and `index.html` remain CRLF.
