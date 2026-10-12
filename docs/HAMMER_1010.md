# Hammer — depth, commitment and authored Chromium

Mike's October 10 direction is wired into the Stage 5 fight. Use **BOSS5** for
the regular boss encounter; HAMMER and HAMA keep their existing music mechanics.

Background body contact now follows the same scale that draws the orbital
poses. The .25-scale warning and early dive cannot collide with a pilot; the
dive crosses the player's plane when it returns to scale 1, approximately
.279 seconds into the .52-second descent. The body target silhouette scales
with the pose and the hammer target uses the actual drawn head coordinates.

Missiles and normal weapons damage the armor through the dive without
reflecting or cancelling it. Depleting the hammer during a committed jump
queues its break until the strike lands. The one-time 8% emergency reserve
also waits for the committed strike, then still restores 38% and resumes rage.
Normal recovery counterplay, checkpoint heals, stun and fight progression use
their existing authoritative owners.

Chromium absorbs body shots without spawning hostile copies. The exposed
healing hammer remains reachable, and its break drops the wall as before.

Six generated banks add **96 authored frames**, 16 per bank: whole-body shield
formation, right and left side swings, chrome wall formation/sustain/shatter,
core charge/pulse and chrome energy spike rise/sustain/shatter. Full heads and
two arms are retained. Poses use the same physical chest pivot and body scale;
the side swing warning and damage path use the measured visible hammer tip.
The warning contains every released pose and the original 38-pixel impact
width, including the curved travel between the new poses.
The reactor and wall effects continue independently during white hit flashes.

Art provenance and exact built-in image-generation prompts:
`_ART_SOURCES/hammer_1010/README.md` and `prompts.json`. The owned importer is
`_BUILD_SOURCE/build_hammer_1010.py`; all shipping frame dimensions are even.
No packed atlas or generated shared manifest was edited.

Verification record: `docs/qa/hammer_1010.json`. Native captured clips and
contact sheets: `_shots/hammer_1010/review.html`. The protected visual clips
verify choreography and pixels; they do not establish human clear difficulty
or replace a complete campaign playthrough.
