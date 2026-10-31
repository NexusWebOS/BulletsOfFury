# Neural Archon — moving eyes and laser charge

Mike spotted a frozen rectangular eye/brow patch on the moving brain. The
previous exporter replaced that region with the seed in every idle pose.
Remove that operation: each whole actor now retains its actual PixelLab face.
Every idle, charge and firing pose stores its own measured eye origins. Draw
positions, beam origins and visible beam contact use those same registered
pixels. Warning lanes cover the firing pose envelope without chasing the player.

New PixelLab charge windup lights both eyes, sockets, surrounding brow and
nearby chrome before release. Whole-frame focus poses hold the charged eye
region during firing; recovery reverses the authored charge poses. Matching
white hit partners preserve native visible damage feedback.

New PixelLab laser stream uses16 generated flow poses through every baked
expansion width, at24fps. This replaces the prior two-frame selection from an
older PixelLab take. Current beam art pixels remain the contact owner. No
runtime glow, tint, opacity animation, compositing, rotation or scaling added.

Existing attack timing, cloud shield, geysers, health, Retina, native morph
pacing, other boss forms and final death/reward stay with their current owners.

Native QA compares real exported face pixels with each original source, checks
changing per-frame eye origins, actual charge/laser blits, emitter alignment,
damage/safe lanes and hit feedback. The earlier key-change check alone missed
the stationary pasted face. Gameplay capture is a controlled native replay.

Sources: `_ART_SOURCES/dracodia_eyes_1023/`; current rebuild inputs also live in
`_ART_SOURCES/dracodia_brain_1023/`. The original self-rewriting installer had
damaged its own quoted path replacement; it now uses explicit portable paths.
No commit/push or unrelated art migration is included.
