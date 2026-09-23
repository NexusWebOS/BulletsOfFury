# Stage 9 pilot-view intercept — 2026-09-23

After the Stage 9 card, the game enters a playable 25-second cockpit intercept before the existing launch. The original `pilot_pov_magenta.png` remains the exact cockpit master. Its magenta windshield is keyed at runtime so the authored orbital scene and approaching Stage 9 enemy plates show through; the dashboard is not regenerated. Enemy plates grow and shift with depth to create the pseudo-3D approach. Players aim with directional controls or pointer, fire with the existing fire binding/A, and evade with B. Hits award score; ships that reach the cockpit damage its three-point hull. A breach restarts this short segment and removes score earned in the failed attempt. Completion continues into the normal Stage 9 launch.

The hand art is stored in `assets/game/cockpit_pov_0923/`. Both source strips contain four matching frames: neutral grip, left pull, right pull, and trigger press. They are composited over the static cockpit, so the magenta glass and controls remain consistent. Runtime palette caches recolor glove seams and sleeve blues to the selected pilot's roster tint while preserving skin, glove shading, alpha, and the frame silhouette.

| Hand master | Pilots |
| --- | --- |
| `male_hand_strip.png` | Axel, Decker, Maverick, Freezer, Juggernaut, Cole |
| `female_hand_strip.png` | Yuri, Lizzie, Falva |

The built-in image-generation tool produced the two transparent animation strips. Prompt set:

1. Male master: Use the existing cockpit as a geometry/style reference; draw only a male pilot's right forearm and armored tactical glove as four equal transparent horizontal frames, with a fixed lower-right sleeve anchor and poses for neutral joystick grip, left pull, right pull, and trigger press. Keep dark charcoal leather and recolorable cyan seams, crisp dense 16-bit pixel-art clusters, five fingers, no cockpit or background.
2. Female master: Match the male strip's exact four-slot layout, glove style, scale, and motion; use a narrower female wrist and slimmer practical tactical glove. Draw only the right arm on transparent alpha, with no cockpit or background.

`_BUILD_SOURCE/probe_cockpit_pov_0923.py` enters through the real Stage 9 intro in Chromium, renders the cockpit and both hand masters, verifies all nine palette caches, firing, target kills, evasion, perspective, the exit to launch, and absence of page/console errors. Screenshots and probe output are under ignored `_shots/cockpit_pov_0923/`.

Final verification: `node --check assets/game.js` passed; the full `node _BUILD_SOURCE/test_fl.js` run reached its final summary with 80 inherited failures and zero new failing assertion names versus the pre-cockpit run. The real Chromium probe passed with no page or console errors, including the launch after its portal flash.
