# Generated weapon icon correction — November4

Mike requested genuinely new weapon illustrations in BOF's existing hexagonal icon style. The earlier cannon-overlay interiors are replaced with two newly generated designs: Spread Lasers has a compact three-emitter fan array; Plasma Cannons has paired short reactor projectors with two visible blue ion cores. Built-in image_gen generated both referenced designs. Original amber/blue/green/silver/red hexagonal borders and native Roman I–V plaques are retained pixel-for-pixel outside the measured weapon panel. The Stage X crate/pill family is separate and unchanged by this correction.

## Generation prompt set

Spread: Reference the original laser icon for chrome, dark pixel outlines, vertical hexagon, amber segment rail and Roman I plaque. Replace the entire old cannon illustration with one compact black/chromium wedge receiver and three short angular cyan laser emitters branching upward-left/upward/upward-right. Confine rays to the inner panel. Keep the entire silhouette, frame and tier plaque visible. Crisp Neo Geo/Sega16-bit pixels, transparent outside the hexagon, no background, captions or extra icons.

Plasma: Reference the generated Spread frame plus the original laser icon style. Replace the interior with two short broad ion projectors facing the viewer: dark gunmetal receiver, chrome radiator fins, blue rings, bright blue-white orb in each round emitter and short blue conduits. Preserve matching hexagon and Roman I plaque. No three-emitter fan, rays or old long ribbed machine-gun barrels. Dense crisp pixel clusters and actual transparent outside frame.

## Files and integration

Raw generated images, measured112px masters and reproducible builder are in `_BUILD_SOURCE/coleforge_1104/generated_icons/`, `build_assets.lua` and `make_config.py`. The canonical source design is copied only inside the convex native weapon panel; the border and badge exclusion remain from the original atlas. All140 family/tier/size/hit variants and editable .aseprite sources were rebuilt. Existing icon keys and runtime paths remain valid. Index refreshes the art registration. No gameplay or projectile/effect bank was changed.

Runtime PNGs: `assets/game/shared/combat/coleforge_1104/{spread,plasma}_icon_<level>_<size>.png`. Contact sheet: `_shots/hex_weapon_icons_1104/generated-hex-icons.png`. Native recordings at http://127.0.0.1:65043/review.html were refreshed for both weapons and the effects preview. The production review folder contains copies of the new videos and receipts.

## Verification

21 focused checks pass: canonical original frame/badge pixels retained on all10icons; distinct interior content on all10icons; all80 non-icon projectile/effect banks unchanged. Existing720 authored-asset/provenance checks pass. Native recordings show every level in the HUD, nonzero audio, no page/draw/audio-routing errors. These controlled clips are visual checks, not a full campaign balance certificate. The previously recorded broad-suite difficultyHealthBaseline15 harness blocker remains; no complete-suite pass is claimed. No commit/push.
