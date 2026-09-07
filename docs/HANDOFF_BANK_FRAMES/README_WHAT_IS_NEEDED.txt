BULLETS OF FURY - BANK / ROLL FRAMES NEEDED (hand-authored)
==========================================================================

SpriteCook cannot produce these. Tested four ways - plain prompt, emphatic prompt, a
picture of the exact pose as reference, and per-frame editing of the hull. Every time it
YAWED the sprite in the image plane instead of ROLLING it about the nose-to-tail axis:
principal axis came back -49, -64 and -45 degrees where the correct answer is +90 (nose
straight up). It also cannot draw a knife-edge: asked for one it returns a narrowed top
view with the canopy still visible, 39 px wide where the true edge is 18.

THE RULES FOR EVERY FRAME
--------------------------------------------------------------------------
  * The NOSE STAYS POINTING STRAIGHT UP, dead vertical, in every single frame. The ship
    rolls about its own nose-to-tail axis. Do NOT rotate the image.
  * Camera stays directly overhead and never moves.
  * Same design, colours, panel detail, and light from above.
  * Transparent background. 1px black outline. NO glow, aura or bloom.
  * NO ENGINE FLAME - the build bakes the flame on, and a drawn one gets doubled.
    (This is exactly why Falva's existing turn frames are unusable.)
  * Height stays the same in every frame; only the WIDTH narrows as it rolls.

ONLY ONE SIDE IS NEEDED. Draw the ship banking to ITS RIGHT; the build mirrors each frame
for the left-hand pose. These airframes are laterally symmetric, so the mirror is exact.


WHY EACH SHIP IS ON THE LIST (measured widths, not opinion)
==========================================================================
  DECKER      no bank art at all - the hull is new (0906x), everything is a derived squash
  AXEL        no bank art at all - the hull is new (0906x), everything is a derived squash
  YURI        BROKEN: every bank and roll frame is 145 px wide, exactly his hull width. pv1, l,
           pv0, br1 and br2 do not narrow by a single pixel - he never actually banks or rolls.
  LIZZIE      DEGENERATE: pv1, l and pv0 are all 211 px - the three pivot steps are the same
           width, so the lean does not progress. br2 at 44 px is a usable edge.
  FALVA       her widths progress cleanly (152/145/143/135/108/15/108) BUT her turn frames carry a
           BAKED ENGINE FLAME - game.js refuses to use them for that reason, so they are dead art.
  COLE        DEGENERATE and OUT OF ORDER: pv0 (27 deg) is 156 px and pv1 (17 deg) is 153 px, so the
           harder bank is WIDER than the gentle one. l and pv0 are the same width.

ALSO DEGENERATE, NOT ON THE LIST - your call whether to add them:
  MAVERICK    l, pv0 and br1 are all 156 px - three different roll angles, one width.
  FREEZER     br2 is 85 px against a 197 px hull (0.43) - that is not a knife edge, and
              br2 and br3 are both 85, so two different roll angles share a frame.
CLEAN, LEAVE ALONE:
  JUGGERNAUT  203/194/190/181/143/21/143 - a proper progression to a true 21 px edge.


DECKER   - work from decker_TOP_reference.png  (176x218)
--------------------------------------------------------------------------
  frame                    target size  what it is
  pv3  (roll 17 deg)       168x218      gentle bank right - you start to see its right side
  r  (roll 20 deg)         165x218      bank right - the standard lean
  pv4  (roll 27 deg)       157x218      hard bank right
  br7  (roll 45 deg)       124x218      rolling right - wings clearly foreshortened
  br6  (roll 90 deg)       16x218       KNIFE EDGE - fuselage spine and the razor edge of the wings only
  br5  (roll 135 deg)      124x218      past vertical - now showing the BELLY, still narrow
  the 135 deg frame shows the UNDERSIDE - use decker_BELLY_reference.png as its source.

AXEL   - work from axel_TOP_reference.png  (207x214)
--------------------------------------------------------------------------
  frame                    target size  what it is
  pv3  (roll 17 deg)       198x214      gentle bank right - you start to see its right side
  r  (roll 20 deg)         195x214      bank right - the standard lean
  pv4  (roll 27 deg)       184x214      hard bank right
  br7  (roll 45 deg)       146x214      rolling right - wings clearly foreshortened
  br6  (roll 90 deg)       16x214       KNIFE EDGE - fuselage spine and the razor edge of the wings only
  br5  (roll 135 deg)      146x214      past vertical - now showing the BELLY, still narrow
  the 135 deg frame shows the UNDERSIDE - use axel_BELLY_reference.png as its source.

YURI   - work from yuri_TOP_reference.png  (145x162)
--------------------------------------------------------------------------
  frame                    target size  what it is
  pv3  (roll 17 deg)       139x162      gentle bank right - you start to see its right side
  r  (roll 20 deg)         136x162      bank right - the standard lean
  pv4  (roll 27 deg)       129x162      hard bank right
  br7  (roll 45 deg)       103x162      rolling right - wings clearly foreshortened
  br6  (roll 90 deg)       16x162       KNIFE EDGE - fuselage spine and the razor edge of the wings only
  br5  (roll 135 deg)      103x162      past vertical - now showing the BELLY, still narrow
  the 135 deg frame shows the UNDERSIDE - use yuri_BELLY_reference.png as its source.

LIZZIE   - work from lizzie_TOP_reference.png  (222x236)
--------------------------------------------------------------------------
  frame                    target size  what it is
  pv3  (roll 17 deg)       212x236      gentle bank right - you start to see its right side
  r  (roll 20 deg)         209x236      bank right - the standard lean
  pv4  (roll 27 deg)       198x236      hard bank right
  br7  (roll 45 deg)       157x236      rolling right - wings clearly foreshortened
  br6  (roll 90 deg)       16x236       KNIFE EDGE - fuselage spine and the razor edge of the wings only
  br5  (roll 135 deg)      157x236      past vertical - now showing the BELLY, still narrow
  the 135 deg frame shows the UNDERSIDE - use lizzie_BELLY_reference.png as its source.

FALVA   - work from falva_TOP_reference.png  (152x166)
--------------------------------------------------------------------------
  frame                    target size  what it is
  pv3  (roll 17 deg)       145x166      gentle bank right - you start to see its right side
  r  (roll 20 deg)         143x166      bank right - the standard lean
  pv4  (roll 27 deg)       135x166      hard bank right
  br7  (roll 45 deg)       107x166      rolling right - wings clearly foreshortened
  br6  (roll 90 deg)       16x166       KNIFE EDGE - fuselage spine and the razor edge of the wings only
  br5  (roll 135 deg)      107x166      past vertical - now showing the BELLY, still narrow
  the 135 deg frame shows the UNDERSIDE - use falva_BELLY_reference.png as its source.

COLE   - work from cole_TOP_reference.png  (163x214)
--------------------------------------------------------------------------
  frame                    target size  what it is
  pv3  (roll 17 deg)       156x214      gentle bank right - you start to see its right side
  r  (roll 20 deg)         153x214      bank right - the standard lean
  pv4  (roll 27 deg)       145x214      hard bank right
  br7  (roll 45 deg)       115x214      rolling right - wings clearly foreshortened
  br6  (roll 90 deg)       16x214       KNIFE EDGE - fuselage spine and the razor edge of the wings only
  br5  (roll 135 deg)      115x214      past vertical - now showing the BELLY, still narrow
  the 135 deg frame shows the UNDERSIDE - use cole_BELLY_reference.png as its source.

NOT NEEDED - the build already has these:
  level (0 deg) = the top reference itself;   180 deg = the belly reference;
  every left-hand pose = a mirror of its right-hand twin;
  the eight somersault frames = derived from top / nose-on / belly / tail-on views.