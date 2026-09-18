# Weapon Forge and Furious Razorback repair — 0918

This batch repairs the Stage-1 Furious miniboss presentation and rebuilds the boss-element progression around global element licenses instead of random weapon pairs.

## Shipped behavior

- The Furious Razorback remains the current authored tank at 150% scale. Only its green armor panels are palette-swapped to neon red; gray armor, black outlines, lights, weapons, and ordnance keep their authored colors. The 25 reproducible plates live in `assets/game/bosses/razorback_furious/` and are built by `_BUILD_SOURCE/build_razorback_furious_palette_0918.py`.
- Furious sonic pressure is split into visible decibel lobes. Directional attacks use five lobes and novas use eleven, with collision-safe gaps matching the rendered openings. Speed and thickness were reduced modestly so the gaps can be read and used.
- Boss victories now award one deterministic element license: Sonic, Fire, Ice, Lightning, Chromium, Tidal, Toxic, Prism, and Dark Matter for stages 1–9. A license applies to every forgeable weapon; bosses do not award random Slugs or other element/weapon pairs.
- The Forge allows two upgrades and two re-specs per stage. Crafted forms persist independently, and re-spec unequips a form without deleting it.
- Loadout form selection supports the base weapon plus every crafted elemental form. Flamethrower can switch to Ice Breath, and the orb slot can switch among Ice Orb, Fire Orb, and Thermoshock when those powers are known.
- Stage 5 can open the Forge after its space boss. Global element rewards and all crafted forms survive campaign save/load and migrate old element/weapon reward records.
- The Forge/loadout plate now contains Fury Points at the top and an embedded RE-SPEC control. The Weapon Found screen uses four authored icon/name bays and announces actual weapon systems separately from boss powers.
- Fire Orb uses a dedicated authored Magma Orb projectile. It is drawn from the opaque volcanic cell without additive washout, preserving the dark rock shell and molten fissures.
- Enemy projectile families, Furious charge/release, boss attack families, and Magma Orb launch all resolve through the real-sample SFX routes. The existing per-family gain and retrigger gates remain active so combat stays audible without stacking into alert-like beeps.

## Generated assets

Image generation mode: `stylized-concept` for the Magma Orb, then `precise-object-edit` for both UI plates.

- `assets/game/player_weapons/magma_orb_0918/magma_orb.png`
  - Prompt: actual in-game MAGMA ORB; dense cracked black volcanic rock; white-yellow molten core; orange lava fissures; neon-red rim; 16-bit arcade pixel art; centered; transparent background; no UI, text, or trail.
- `assets/game/ui/forge_0918/forge_loadout.png`
  - Prompt: edit the current weapon panel into a six-bay Forge/loadout screen with FURY POINTS above, a wide information bar, and an embedded RE-SPEC button while retaining the existing arcade-metal visual language.
- `assets/game/ui/forge_0918/weapon_found.png`
  - Prompt: edit the current weapon panel into a WEAPON FOUND screen with exactly four square icon wells paired with four long name wells and a bottom briefing bar.

The generated source files remain in the Codex generation cache recorded in the task history; the normalized shipping files above are the canonical repository assets.

## Verification

- `node --check assets/game.js`: pass.
- `node _BUILD_SOURCE/test_fl.js`: 4,921 checks pass and the exact 57-name incoming baseline remains. No new failure name.
- `_BUILD_SOURCE/weapon_repair_0918/probe.py`: 9/9 in real Chromium with zero page or console errors.
- The probe verifies 150% scale and static red-panel art, visible/collidable sonic gaps, all-element/all-weapon Forge access, two upgrades and re-specs, persistent selectable forms, orb form switching, Weapon Found contents, live Magma Orb art, and real SFX dispatch.

## Rendered proof

- [Furious Razorback and segmented sonic pressure](proofs/weapon_forge_repair_0918/01_furious_razorback_segmented_sonic.png)
- [Global-element Forge](proofs/weapon_forge_repair_0918/02_forge_global_elements.png)
- [Persistent selectable weapon forms](proofs/weapon_forge_repair_0918/03_loadout_selectable_forms.png)
- [Ice Orb, Fire Orb, and Thermoshock selection](proofs/weapon_forge_repair_0918/04_orb_forms_fire_ice_thermoshock.png)
- [Weapon Found screen](proofs/weapon_forge_repair_0918/05_weapon_found.png)
- [Live Magma Orb projectile](proofs/weapon_forge_repair_0918/06_live_magma_orb.png)
