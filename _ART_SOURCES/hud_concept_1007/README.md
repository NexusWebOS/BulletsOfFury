# Bullets of Fury — top HUD concept
Date: 2026-10-07

Mike's sketch is the layout authority. This package contains generated concept art and a separate empty frame source; it does not replace the live HUD yet. The sample numbers, weapon icon and boss name in the finished concept are presentation examples.

## Inspected and compared
- Mike's original sketch: reference-layout.png.
- Current authored assets: assets/game/shared/ui/ui_hud.png and ui_bossbar.png.
- Current live Chromium capture: reference-current-hud.png. The game entered Stage 4 / Storm Sovereign with assets ready and no page or console errors. This is a protected visual fixture, not a balance test.
- Runtime: drawHUDStrip, bottomHudLayout, drawRollCharge, drawEquipCorner, drawCampaignRadar, drawIncomingLockHud, drawSpecialHUD and drawHUDOverlay in assets/game.js; the dedicated HUD row in index.html and wide-screen panels in assets/widescreen_hud_0918.js.

| Area | Current game | New concept |
|---|---|---|
| Maneuvers | Small bars at bottom left | Two prominent green tracks at upper left |
| Lives | Separate top stat box | Beveled tab under the maneuver tracks |
| Weapon | Bottom-right icon and separate top equipment pips | Dedicated square beside the maneuver panel |
| Special | Bottom-center rail, active-state display | Long named red meter in the center |
| Speed / player shield | Top equipment block | Two small indicators in the center lower tab |
| Radar / incoming lock | Bottom-right cluster | Radar square, then lock-on capsule at upper right |
| Missiles | Top BOMBS box | Right-hand lower tab, labeled MISSILES |
| Boss health / boss shield | Large independent bars over the upper fight area | A dedicated shallow lane beneath the player assembly |

## Visual direction
Keep BOF's steel and graphite pixel frames, recessed dark tracks, compact arcade lettering and small amber hardware lights. Green identifies maneuvers, red the special resource, amber weapons/speed/missiles, and cyan shields. Shape, labels and fill amount must also communicate state. No added score panels, portraits or decorative wings were introduced into Mike's layout.

The finished concept preserves the five groups and three beveled lower tabs. It is an art study, not a pixel-perfect export of the sketch's dimensions: the generated frame and boss row are taller and the source has transparent padding. Use the sketch's proportions as the integration target, not the entire PNG canvas as the HUD height.

## Files
- hud-concept-v1.png — finished sample HUD with labels and example values; RGBA.
- hud-frame-source-v1.png — matching empty frame study; RGBA. Labels, radar, icons and fill amounts have been removed. Empty segment outlines remain and are illustrative, not authoritative gameplay capacity.
- reference-layout.png — unchanged user sketch.
- reference-current-hud.png — unedited screenshot of the existing live HUD.
- review.html — local comparison gallery, including dark and light transparency review.
- prompts.json — exact prompts and built-in image_gen mode.
- manifest.json — file dimensions, alpha summary and SHA-256 hashes.
- current-capture.json — native capture readiness and errors.

## Integration contract
1. Reserve HUD space before images load. Put the boss lane immediately below it; showing or hiding a boss must not resize the game or change camera coordinates. Keep the world and collision bounds consistent with the visible playfield.
2. Draw the static frame from a shared cached image. Use live bitmap text, the game's existing weapon icons, and separately clipped fills for all changing values. Do not ship one complete image per pilot, cooldown or stock count.
3. Read real roll/somersault cooldowns, current pilot special name/resource, equipment levels, missile stock and existing incoming-lock/radar state. Preserve gameplay values and targeting behavior. The concept's sample counts and generated weapon illustration must not become game data.
4. Distinguish player shield pips in the center tab from the boss's secondary shield line. Support minibosses, multiple rebel health pools, finale form HP and boss names without overflowing the lane. Keep all currently necessary timed-weapon/lock warnings available.
5. Keep the boss row screen-anchored and clear of ships/projectiles. Secondary score/high score and existing clock information still need an appropriate runtime home; their absence from the sketch is not permission to delete scoring or timing.
6. Use short state-change feedback: a small ready glint, restrained red lock warning, and a brief boss damage trail. Keep the frame stationary. Avoid continuous full-panel pulsing, bloom, blur or full-size animated textures.
7. Before shipping, derive compact, clean slices from the chosen artwork; resolve the empty source's decorative pip count; validate alpha and borders against light and dark scenes; and verify the actual bitmap lettering at native size. This source art is not registered in the runtime or an atlas.
8. Verify native 480-wide presentation, normal desktop, fullscreen wide, narrow/mobile, co-op ownership, long pilot/boss names, all resource states, menu-to-game entry and boss transitions. Measure actual performance after integration. The concept generation does not establish an FPS improvement.

## Validation and scope
Both generated images were visually inspected against the sketch and authored HUD atlas. They contain real alpha transparency. Their original generated bytes are preserved; no Python image editing was used. A fresh Chromium screenshot confirms the current HUD and contains zero recorded browser errors. No live scripts, gameplay balance, atlases or asset-loading manifests were changed for this concept package.
