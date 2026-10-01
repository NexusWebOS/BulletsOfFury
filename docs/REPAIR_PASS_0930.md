# September 30 local repair and weapon-art pass

This work is in the primary local checkout on main, based on `f61737b`. Nothing in this pass has been committed or pushed. Preserve the existing HAMA body/poses and source art. The first square Fusion icon concept was rejected and is not installed; the corrected icons use the existing weapon badge references.

## Integrated changes

- **Fusion Cannon:** replaces the space Shadow Orb slot. It has generated pink/purple beam, charge, impact and scar reels, plus five hexagonal I–V badges with the established orange/blue/green/silver/red borders. Full charge is 1.55 seconds; 150% gives 1.5x size; 190–199% gives 2x; 200% triggers the real player death pipeline through shields/invulnerability. The charge view darkens/pinks progressively and warns before overload. Ground Dark Matter + Ice Orb retains its void behavior under the Shadow Orb name.
- **Weapon animation and previews:** connect the existing nine-element orb/cast/chaingun art to runtime. The nine beam reels remain active. Fire Whip, Ice Lance, Ice Breath and Thermoshock retain their dedicated behavior. Preview level now reaches the actual weapon, forge and infusion instead of always running at level 1. Preview state is restored afterward. Chaingun rounds are authored static projectiles; beams/orbs/casts have animated source frames.
- **Chaingun:** larger rounds, roughly 12% more damage, familiar level colors, element-specific round/impact art, spinning modular mounts that follow each co-op seat. Respawn visibility now follows the ship. Existing Cole-exclusive gun progression remains intact.
- **Shields and hit feedback:** generated eight-frame hull-shaped player shield replaces orbiting ice-orb visuals. Sprite bounds are trimmed to the visible rim before sizing. Enemy field/bubble shields use each hull's width and height. Registered hit tint is white; element identity stays in the projectiles and impact effects.
- **Stage 4:** new modular tank/jet art, independently damageable turret/pods, and warned tank missile launches. Tank health increases 35%, jet health 12%. Destroyed modules stop their guns. The miniboss helper is routed before parent invulnerability/damage clamping so overlap no longer swallows its hits.
- **Stage 5:** all difficulties activate Chromium armor (30/60/100% extra health for Normal/Hard/Furious). Activation uses the existing correct raised-hammer robot reel, lightning and core effects. It stages low enough to keep the hammer visible. Normal healing has an exposed 12-HP hammer core, smaller recovery and no combat barrier. HAMMER/HAMA now also select spells, chaingun, restoration and the large beam in addition to jumps, throw, whirlwind and ball; HAMA still alternates robot tosses and preserves dance cues. Active recovery is protected from song interruptions.
- **Stage 6:** a generated blue ace with 20 poses and exact separated fuselage/wing plates, matched lock/hit bounds and independently flashing wings; real blue exhaust at its nozzles. Larger bomber art with release/bay states. Existing modular Harrier fans/cannons and their muzzle positions were preserved and retested.
- **Stage 7:** one stationary vent body plus an eight-cell fluid sequence replaces inconsistent transforming hazard art. Warning/damage range follows the visible stream; no damage before release or outside its reach. Generated top-down sewer approach overlays animated sludge. A girder joins the entrance to the level without the black seam. Existing Furious Warden chaingun/stomp/mortar additions were retested.
- **Stats:** bounded LRU cache for immutable tinted/outlined glyph masks (512 entries / 8 MiB). Scores still update live. A 24-frame score-tally sample dropped from approximately 108ms to 12.5ms average draw time; latest max 17.7ms.
- **Controls/pickups:** Start submits the password once. Retina upgrades no longer spawn. Stage 5 helper-orb rewards are rerolled, including saved reward bags. x100 missile crates no longer spawn; scripted boxes downgrade to x50. Existing direct cinematic ammo grants remain. Pickup turning uses the complete front face rotating in-plane, never an edge-on/back-face frame.

## Owners and rebuilding

Load order in `index.html`: existing September 29 owners, then `fusion_art_0930.js` / `fusion_0930.js`, `repair_art_0930.js` / `repair_0930.js`, and `encounter_art_0930.js` / `encounters_0930.js`. Core hooks remain in `assets/game.js`; armor eligibility is in `assets/furious_review_0927.js`. `bossmode.html` and `bulletsofdebug.html` both host the same `index.html` engine and therefore load these changes.

Source images and provenance are checked into `_ART_SOURCES/{fusion,repair,encounters}_0930`. Runtime atlases and manifests are under the corresponding `assets/game/` folders. Packing uses explicit reviewed cuts, common pivots/scales and nearest-neighbour resampling. No procedural replacement art. Builders prefer checked-in source images:

```
python _BUILD_SOURCE/build_fusion_0930.py .
python _BUILD_SOURCE/build_repair_art_0930.py
python _BUILD_SOURCE/build_encounter_art_0930.py .
```

`repair_art_0930.js` references existing `weapon_animation_0928` families rather than duplicating those files. Do not restore the rejected square icons or use the retired back-chaingun robot for armor activation.

## Verification

Full engine suite reached **FALVA/LIZZIE BUILD OK, 0 ERRORS**. New section 380 loads the actual new add-ons and checks atlas bounds, charge/death, preview tier/isolation, independent modules and both password arsenals. Older soak tests replace `playerHit`; the new overload regression explicitly retains the genuine engine function captured at boot.

Native Chromium probes and screenshot folders:

| Probe | Coverage |
| --- | --- |
| `probe_fusion_0930.py` | I–V icons, 100/150/199% sizes, swept hits, impacts/scars, real 200% death on 5/9, forbidden drops, Start |
| `probe_repair_0930.py` | ship/pod fit and movement, all nine orbs, overlapping helper hits, armor on all 3 routes × 3 difficulties, full password selectors |
| `probe_encounters_0930.py` | Stage 4 modules/disabled guns/warnings, blue ace modules and eight evasive samples, bomber, vent phases and visible damage boundaries, entry join |
| `probe_combinations_0930.py` | 180 live previews: 4 weapons × 9 elements × 5 levels; 27 animated families and nine authored round plates; cache bounds |
| `probe_hammer_heal_break_0929.py` | regular and HAMMER gun/missile heal interruption, visible stun, barrier removal and combat resumption |
| `probe_hama_heal_0930.py` | same real missile/gun interruption through HAMA |
| `probe_s67_0929.py --only carrier,warden` | Harrier fans/cannons/beam origins and Furious Warden patterns; 14 checks passed |
| `profile_stats_0930.py` | actual stats score-tally rendering |
| `performance_repair_0929/profile_upgrade_0930.py upgrade_0930` | warm automatic-fire samples of stages 5–8 |

Native probes reported no page/console errors. Screenshot evidence remains under ignored `_shots/`; portable result details are in [qa/upgrade_0930.json](qa/upgrade_0930.json), and the corrected icon row is [qa/fusion_icons_0930.png](qa/fusion_icons_0930.png). The later ace exhaust-only change was native-render tested after the full suite.

## Remaining acceptance limits

These are focused checks, not a completed end-to-end campaign or co-op endurance run. Warm FPS samples were 54.1 / 60.0 / 60.0 / 59.3 on stages 5/6/7/8. Stage 8 still recorded one 74.9ms frame; inspect cold asset decoding and late boss density if a player still sees stutter. Stage 7's warm sample had already cleared its nearby enemies; its Warden was covered separately by a functional browser probe, not a long frame-time trace.

Give the complete HAMMER/HAMA songs another manual playthrough to judge new arsenal timing between dance cues. The launch selectors, Chromium activation, protected recovery and actual gun/missile stun are verified. Enemy HP changes and new vent timing still need Mike's difficulty feel review. Directional front-plate shields retain their existing oriented art; this pass tightens field and bubble shells.

No release ZIP, GitHub upload, social action or save migration was performed in this pass.
