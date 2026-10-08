# Bullets of Fury — Overdrive expansion art

This folder holds the Overdrive expansion art, including Hotwire, Phoenix, Niel and the Machinists. The standalone [Ground Operations build](topdown/README.md) now uses these packs in playable Levels 2–4. Integration into the base game's flight campaign remains separate.

| Folder | Contents |
| --- | --- |
| `concept/` | Expansion cover, logo overlay, pilot designs, front views, and ship concepts |
| `pilot_avatars/` | Hotwire and Phoenix pilot-select portraits composed with the game's existing 256x256 frame |
| `specials/` | Special pickup boxes, hex icons, transparent effect frames, source sheets, animated previews, and `manifest.json` |
| `tools/` | Reproducible portrait and special-art builders |
| `ground/` | Three modular tank families, four helmeted infantry bodies, ground pickups and effects, G.O.D Burst, and an interactive candidate-art viewer |
| `coastline/` | Miami campaign-map extension across the ocean, compound and highway level icons, arrival/departure background plates, and mission beats |
| `onfoot/` | On-foot HUD, Miami beach/park/fortress stage concept, player actions, six handheld weapons and boxes, ammo, enemies, effects and FOV cues |
| `topdown/` | Playable ground campaign: Level 2/The Warrior, Level 3/Miami infantry, Level 4/hostile Machinist tanks with Hotwire, Phoenix or Niel support; current controls and verification in `README.md` |
| `windstorm_machinists/` | Niel/Windstorm, grounded Machinists crew, three modular tanks and effects, track phases, dedicated allies, shared stealth interactions and a consolidated coverage index |

The latest [coverage index](windstorm_machinists/COVERAGE.md) links the saved graphics for the expansion requests and identifies later engine integration work.

Hotwire's special uses a heated braided fiber whip with pullback, release, impact, and recovery frames. Lightning spreads from the impact through a separate effect sequence. Phoenix's Armageddon art includes the charge Retina, fire line, overhead mortar, and bilateral ground bursts. See `specials/README.md` for frame order, dimensions, and intended placement.

From the repository root, rebuild the normalized assets with:

```powershell
python expansion/tools/build_overdrive_pilot_avatars.py
python expansion/tools/build_overdrive_special_art.py
```

Both scripts require Pillow. The portrait builder also reads the game's existing `assets/game/pilot_avatars/avatar_frame_template_0919.png`; it leaves the current pilots untouched. The source masters remain in this folder. The original Bullets of Fury logo remains in `assets/game/ui/logo_0916/bof_logo.png`; the expansion overlay is in `concept/overdrive_word_overlay.png`.
