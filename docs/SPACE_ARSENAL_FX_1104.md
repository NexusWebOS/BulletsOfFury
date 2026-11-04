# Space Arsenal and ColeForge FX — November 4

Spread Lasers (slot3) and Plasma Cannons (slot4) are installed in the current game. Volley Missiles remain passive slot2. Plasma fires forward from both measured cannon mouths, as Mike confirmed; Spread fires three beams per mouth. Both additions have levels1–5, first pickup0→1, level5 cap, increasing damage/size, tiered chrome boxes, HUD icons/labels, Armory previews and discovery persistence. Optional save fields preserve space tiers, selection and the grounded loadout without changing save version. Legacy saves start the new slots unowned; old untagged boss rewards retain modulo3 mapping.

## Sources and rebuild

The supplied transparent 1x PNGs and timing/pivot metadata are the source, rather than the GIF preview background. Spread uses the central cyan bolt in frame01 of spreadfire_cannon_horizontal_fan; Plasma uses frame02 of vol2_ion_bloom_orb_loop_north. Travel silhouettes stay static; six baked brightness palettes supply1015 light. Directions, sizes, icons, white hits and Cole's green/gray palette were exported offline in Aseprite1.3.18.6-dev. New runtime paths use integer source-over blits, without animated alpha, additive glow, rotation or changing destination size. Existing unrelated rendering stays with its owners.

220 even fixed-cell banks occupy about6.1MB compressed. Loading every size would require156MB decimal decoded. Production warms common sizes and requests the rest lazily; native smoke/ring/shield fallback remains while a size loads. QA deliberately loads all banks.

Sources, hashes, metadata and editable Aseprite files: `_BUILD_SOURCE/coleforge_1104/`. Run `make_config.py` there, then Aseprite with `--batch --script-param config=<absolute build-config.json> --script <absolute build_assets.lua>`. On Windows use `Start-Process -WindowStyle Hidden -Wait`; verify the config.done marker. Copy exports into `assets/game/shared/combat/coleforge_1104/`. The original user pack paths in source-inventory.json must resolve. Original pack frames are unchanged. Column smoke appends six authored dissolve cells ending fully transparent.

## Owners and effect contract

- New guns use native `spaceLaser` simulation and native space hit/damage routing. Modular HP, real hit flashes, foreground gates and impact expiry remain authoritative. The existing decoded spaceLaserCannon shared-mixer cue fires once per volley; native contacts use spaceLaserHit. Muzzle/contact bursts have separate banks. Full tier values live in space_arsenal_1104.js; level5 cadence is0.20s Spread /0.26s Plasma.
- Supplied radial smoke replaces ordinary smoke trails at fixed24/40/64/96 cells; missile exhaust remains native. Existing position/lifetime drives authored frame selection.
- Unangled smoke rings and nsr_fire shock rings use the supplied shockwave. Native angled/colored special rings retain their owners and clocks. Death, burning spin, crash, secondary chains and modular wrecks are preserved.
- Bounded supplementary queue: occasional small bursts, anchored ignition on larger units, boss/miniboss columns, Stage4 ground dust. Cap24; native game dt; stage cleanup; owner/socket anchoring. Named Stage8 boss/miniboss destruction families are excluded. Native death/hit sounds remain authoritative; cosmetic smoke does not add repeated cues.
- Cole nuke keeps area/component damage, crate interaction, stock and nuclearDetonate audio. Its tagged main red overlays use the32-frame green/gray compact tactical cloud at256cell, ground pivot128,216. Native explosion objects still exist and expire.
- Lizzie atomic uses the32-frame rolling mushroom512 and its supplied ground pivot. Native90/26 damage, secondary cookoffs, atomicDetonate and the original white-out/hold remain. New cloud draws below that white-out.
- Strategic carrier nuclear blasts use128/256/512 rolling-mushroom banks under CA111's existing warnings/contact/audio owner. Contact is conservatively intersected with an explicit smaller hot-cap/stem shape following the new art timing; frame22+ gray aftermath is decorative. The old native hazard remains an upper bound. This does not enlarge damage radius or introduce decorative image-alpha collision. Laser-tornado warheads remain native.
- Blue/volt and toxic bubbles use supplied growth, constant-geometry light and white-hit banks. Offline interior dithering keeps hulls readable and the rim intact. Native HP/deploy/break/stun/reflection and Axel's orbiting balls remain. Articulated Stage7/8/9 source-pixel shields are excluded.
- New loose pickups/crates use baked36/40 icons and a40 white hit, retaining native collection/HP/body overlap. Passive rack and old rewards remain compatible.

## Integration

New modules: assets/coleforge_1104_art.js, assets/space_arsenal_1104.js, assets/coleforge_fx_1104.js. Index appends them after existing updates. Five minimal core substitutions: optional level-up helper, optional pickup-icon helper, five-slot Armory preview array, actual preview cadence and discovery normalization space_[0-4]. The concurrent WF14 below-screen pressure change is preserved and is not this pass's work. game.js remains LF; index remains CRLF. No commit/push.

## Observed verification and limits

114 focused native Edge/Chromium checks pass;720 asset/provenance checks pass. Coverage: both ports, all10 tiers, fan/forward velocities, real Stage5 enemy damage, native impact cleanup, Akimbo, first pickup/cap, crate break/reward identity, old boss rewards, passive rack independence, save/legacy load, Stage9 retention, native Armory firing, normalized discovery, native FX clocks/anchors/cap/expiry, ordinary-bullet immunity, physical-missile interception and actual Stage5 bomber hull protection with four live modules. Asset checks cover even cells, extents, editable sources, invariant projectile alpha by heading/glow step, brightness variance, transparent smoke tails and original source hashes.

Three native-engine recordings include current play/HUD canvases copied at native sizes and the existing mixer output. Both weapon clips show all five tiers, their assigned cue and nonzero mixed audio. No browser page/draw errors or shared audio-routing errors were observed. The QA pilot is invulnerable and fire/effect triggers are controlled for review. These are not full campaign runs or balance certification; frame-gap receipts include recording/screenshot overhead. Co-op keeps its documented shared space loadout, not new per-seat inventories. No native-console port is claimed.

Syntax checks pass. Required `node _BUILD_SOURCE/test_fl.js` exits1 before final summary at the existing missing `difficultyHealthBaseline15` in combat_polish_0927b.js:151. It is not a passing full suite; no globals were stubbed to conceal the blocker.

Review: http://127.0.0.1:65043/review.html. Local evidence, recordings and receipts: `_shots/space_arsenal_fx_1104/`.
