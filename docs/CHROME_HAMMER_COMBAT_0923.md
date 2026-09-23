# Chrome Hammer combat revision — 2026-09-23

Hard/Furious ball form starts at roughly 100 pixels/second, accelerates over six seconds, then alternates steep zigzag reflection angles. Every wall impact shakes the screen and plays the hammer impact cue. Its 15-second duration and initial committed warning remain.

After uncurling, Hard/Furious raise both arms and charge a pixel-stepped green light up the body. Hard releases one 32-beam radial ring; Furious releases three offset rings spaced 0.55 seconds apart. Easy/Normal retain the ordinary uncurl recovery.

Breaking the attached or thrown hammer opens a three-second body-hit opportunity. Hitting the body during that opportunity causes a five-second kneeling stun with double damage and an expanding blue chromium glow. Recovery restores the hammer and immediately enters the warned leap combo. This opportunity works with native space weapons; those previously bypassed the detached hammer's collision test.

Furious adds a warned hammer whirlwind followed by ascent into the distance and two committed orbital dives. Each descent has a landing reticle, grows toward the camera, and ends in an enlarged two-handed sweep. A missile interrupts the current descent and knocks the boss back; ordinary and native space bullets reflect toward the player. Reflected space rounds retain their art and move as hostile rounds. Existing invulnerability from rolls and somersaults applies to the strikes.

SpriteCook GPT 2.5 Sunburst generated four new poses against the existing master: raised hands, extended hammer whirlwind, overhead dive, and sweeping follow-through. The existing authored kneeling frame is reused. Files and provenance are under `assets/game/stage5_archmage_0916/combat_0923/`; boundary clips exclude neighboring glows in the packed source.

Validation: JavaScript syntax and diff whitespace checks pass. `_BUILD_SOURCE/probe_hammer_combat_0923.py` verifies acceleration/bounces, 96 Furious / 32 Hard nova beams, native-space hammer break, the five-second 2x window, recovery into the leap warning, reflection, missile interruption, two giant strikes, and Normal recovery. Chromium reports no page or console errors; nova, stun, whirlwind, warning, counter and sweep screenshots were inspected. Full suite completed with 80 pre-existing assertion failures (exit 1), no new failure names against `_shots/sfx_test_final_0923.log`; the baseline's intermittent Stage-1 sand-tank failure did not recur. This is focused encounter verification, not a complete natural-play balance run.

Existing dirty work was preserved. No commit or push.
