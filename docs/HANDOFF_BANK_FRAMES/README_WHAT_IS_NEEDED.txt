BULLETS OF FURY - BANK / ROLL FRAMES NEEDED (hand-authored)
========================================================================

SpriteCook cannot produce these. Tested four ways - plain prompt, emphatic prompt,
a picture of the exact pose as a reference, and per-frame editing of the hull. Every
time it YAWED the sprite in the image plane instead of ROLLING it about the nose-to-
tail axis: principal axis came back -49, -64 and -45 degrees where the correct answer
is +90 (nose straight up). It also cannot draw a knife-edge - asked for one it returns
a narrowed top view with the canopy still visible, 39px wide where the true edge is 18.

ONLY TWO SHIPS NEED THESE. The other seven still have their original hand-drawn bank
frames and those must NOT be replaced - they carry direction (you can tell left from
right), which anything derived from a squash cannot.

THE RULES FOR EVERY FRAME
------------------------------------------------------------------------
  * The NOSE STAYS POINTING STRAIGHT UP, dead vertical, in every single frame.
    The ship rolls about its own nose-to-tail axis. Do NOT rotate the image.
  * Camera stays directly overhead and never moves.
  * Same design, same colours, same panel detail, same light from above.
  * Transparent background. 1px black outline. NO glow, aura or bloom.
  * NO engine flame - the flame is added by the build, and a drawn one gets doubled.
  * Height stays the same in every frame; only the WIDTH narrows as it rolls.

ONLY ONE SIDE IS NEEDED. Draw the ship banking to ITS RIGHT and the build mirrors
each frame for the left-hand pose. These airframes are laterally symmetric, so the
mirror is exact.


DECKER   - work from decker_TOP_reference.png  (176x218)
------------------------------------------------------------------------
  frame                      target size  what it is
  pv3  (roll 17 deg)         168x218      gentle bank right - fuselage tips, you start to see its right side
  r  (roll 20 deg)           165x218      bank right - the standard lean
  pv4  (roll 27 deg)         157x218      hard bank right
  br7  (roll 45 deg)         124x218      rolling right - wings clearly foreshortened
  br6  (roll 90 deg)         16x218       KNIFE EDGE - only the fuselage spine and the razor edge of the wings
  br5  (roll 135 deg)        124x218      past vertical - now showing the BELLY, still narrow
  NOTE: the 135 deg frame shows the UNDERSIDE. decker_BELLY_reference.png is the
        belly view already generated - use it as the source for that one.

AXEL   - work from axel_TOP_reference.png  (207x214)
------------------------------------------------------------------------
  frame                      target size  what it is
  pv3  (roll 17 deg)         198x214      gentle bank right - fuselage tips, you start to see its right side
  r  (roll 20 deg)           195x214      bank right - the standard lean
  pv4  (roll 27 deg)         184x214      hard bank right
  br7  (roll 45 deg)         146x214      rolling right - wings clearly foreshortened
  br6  (roll 90 deg)         16x214       KNIFE EDGE - only the fuselage spine and the razor edge of the wings
  br5  (roll 135 deg)        146x214      past vertical - now showing the BELLY, still narrow
  NOTE: the 135 deg frame shows the UNDERSIDE. axel_BELLY_reference.png is the
        belly view already generated - use it as the source for that one.

Frames the build already has and does NOT need drawing:
  level (0 deg) = the top reference itself;  180 deg = the belly reference;
  every left-hand pose = a mirror of its right-hand twin;
  the eight somersault frames = derived from top/nose-on/belly/tail-on views.