# September 28 weapon graphics — gameplay agent handoff

This pack is **graphics only**. It does not change `assets/game.js`, manifests,
loadouts, damage, audio, saves, pickups, bosses, or the release build. Art lives in
`assets/game/weapon_animation_0928/`; original selected sheets and generation prompts
live in `_ART_SOURCES/weapon_animation_0928/`. Generated with the built-in image_gen
tool. Pillow imports only crop, pad, nearest-neighbor scale, pack and compose reviews.

## Contents

- 18 independent chaingun housings: left/right for Axel, Decker, Maverick, Freezer,
  Juggernaut, Yuri, Lizzie, Falva and Cole. Housings stay fixed on their ship sockets.
- Three 16-frame axial barrel reels: top, bank and underside. Rear coupling anchors
  mate to each housing's front socket. Barrel animation replaces whole-gun rotation.
- .50-cal travel, directional muzzle and metal-shrapnel impact reels; nine infused
  .50-cal round variants. Existing chaingun tier 1–5 icons can remain in use.
- Nine 8-frame orb loops; nine 4-frame laser loops; nine 4-frame elemental casting
  streams; nine 4-frame orb impacts. Elements: Fire/Magma, Ice/Glacial, Lightning,
  Kinetic/Sonic, Chromium, Dark/Void, Toxic, Prism and Water.
- A 12-frame replacement Chromium activation using the **current hammer-only
  boss**. It has no back chaingun, shoulder cannons or older tall-robot silhouette.
  Frames 0–3 raise the free hand, 4–5 receive silver lightning, 6–9 coat the armor,
  and 10–11 settle into the armored stance. Play once, hold frame 11 while armored.

Total: **70 families, 287 frame PNGs**. Each family also has a packed atlas and
`reel.json`; the aggregate `manifest.json` records source cells, frame rectangles,
anchors, playback rates and loop settings. The original oversized/overpacked impact
sheets and old back-chaingun Chromium candidate are **not selected runtime art**.

## Anchors and draw rules

All paths in `manifest.json` are relative to this pack. Each atlas rectangle is
`[x,y,width,height]`. `anchor` is in the normalized frame canvas, not the trimmed
alpha bounds. Draw a frame at `(worldX-anchorX*scale, worldY-anchorY*scale)` and keep
one scale for the entire reel. Sample with image smoothing disabled.

For a complete gun, place the fixed housing at its ship socket using its rear anchor;
then put the barrel rear anchor at `housing.barrelSocket`. Draw barrel behind housing.
The independent muzzle reel belongs at the barrel tip, not the ship center. The
assembly GIF demonstrates all nine pairs with stationary housings and moving barrels.
Final **ship-specific socket coordinates still need in-game placement checks** by the
runtime agent; this graphics pass deliberately does not edit ship draw routines.

The top/bank/underside sheets are authored longitudinal views. Do not yaw-spin the
whole gun to simulate barrel rotation. Select the corresponding authored view during
bank/roll poses; verify each pilot's hull occlusion and attachment pivots in-game.

Orbs use a fixed sphere center. Beams and casting streams use a fixed bottom origin.
The glacial beam uses growing icicle ribs/chips; Ice Breath is a frosted vapor/shard
cone. Sonic has advancing pressure fronts, Chromium has liquid-metal ribbons, Dark
has consuming tendrils, and Water has foaming spray. These are separate authored
silhouettes rather than a universal flame recolor. Use the same reel for existing
level 1–5 combinations and retain the engine's tier-specific width/extent/damage rules.
Freezer's existing Thermoshock `nts_orb_*`/release art can remain its separate mixed
fire/ice family; this pack replaces the nine single-element families.

The 4-frame impacts are concise sprite bursts. End at the final residue, then remove
the effect. Magma contains tiny lava balls and shell shrapnel; implement actual child
projectiles separately. Dark has an implosion and forward semicircle graphic; the
void absorption volume, enemy capture, howl and damage still belong to runtime logic.

## Gameplay work reserved for the other agent

1. Stop Stage 6 wind on death, quit and every encounter/state exit.
2. Route missile hits on an exposed Stage 5 hammer through the healing interrupt,
   cancel restoration FX, and enter the intended stun. Check regular and password
   encounters on all difficulties; curve locked missiles around the barrier.
3. Use this hammer-only Chromium sequence; keep the HP armor fill, hand/core effect
   timing and transition state synchronized. Never select the old back-chaingun form.
4. Restore machinegun↔chaingun form selection, unlock/default chaingun after Stage 5,
   and equip modular mounts from Stage 6. Preserve each machinegun elemental upgrade.
5. Wire the .50-cal graphics and stronger distinct hit FX alongside the intended
   faster projectile speeds and damage. This pack does not tune those numbers.
6. Register new frames through the repository's owning atlas workflow, then verify
   actual rendered pixels and lazy readiness. Do not just add unresolved family keys.

## Verification and review

Run `_BUILD_SOURCE/weapon_animation_0928/import_art.py` to reproduce the imports.
Run `assembly_review.py` to compose modular guns; `verify_preview.py` opens the isolated
art viewer in real Chromium and verifies all 70 canvases, all 43 animated reels,
pixel changes between frames, and absence of page errors. This is art verification,
**not gameplay or unlock verification**. No engine suite is claimed for this pass.

Open `preview.html` through a local HTTP server to filter animated families. PNG
contact sheets, GIF reels, assembly review and browser QA evidence are in `review/`.
Import QA confirms every frame is nonempty, every multi-frame reel has unique pixels,
all canvases have transparent margins, and no normalized frame touches its outer edge.
Manual review corrected uneven source-row/column spacing before packing.

Remaining practical acceptance check: real-game render sizes, hull mounting, animation
rate under frame drops, beam clipping to impact length and per-tier readability.
This art is ready for that integration; it is not yet wired into the game.
