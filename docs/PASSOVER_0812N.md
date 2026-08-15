0812n: beams sweep, they do not follow

Mike: "a charge beam and beam should never follow you. tehy should be like beams that rotate on
the screen that kill you if you touch them, so you have to carefully move while avoiding bullets
between those beams too. Arcade stuff really. Stuff to increase the adrenaline."

0812m's charge beam WAS THE THING HE IS RULING OUT. It locked the player's column and fired down
it - aimed, even if it did not track after the lock. A beam pointed at you is a dodge you either
win or lose in one frame; a beam SWEEPING the field is a space you have to read and move through,
and that is where the tension lives. Replaced, not tuned: nothing in the new hazard reads the
player's position at any point, and there is an assertion that says so.

THE ROTATING BEAM RAKE
n spokes from the boss's own hull, evenly spaced, rotating together on their own clock. The player
threads the gaps while the boss's ordinary guns keep firing - "move carefully between them while
avoiding bullets between those beams".

Three things make it arcade rather than cheap, each a deliberate trade:
  WARM-UP    0.75s drawn thin and dim and NOT lethal, so the sweep is readable before it bites.
  GAP SIZE   the spoke count sets the corridor - 3 spokes leave 120 degrees, 5 leave 72. Phase
             picks it, so the squeeze tightens as the fight goes on.
  RETRACT    a hard duration. A permanent rotating hazard stops being an event and becomes the
             arena, and the player just waits it out at the edge.

Collision is point-to-SEGMENT, not point-to-line: a spoke reaches len and no further, so standing
outside its reach is a legitimate answer. An infinite line would make the whole diagonal lethal.

Measured on a stationary player over a 5-second sweep, which is the worst case by design:
  3 spokes   8-12 hits    5 spokes  12-18 hits    warm-up hits: 0 in every configuration
The spoke count moving the hit count is the phase escalation working. A gap exists by
construction - at the player's typical radius, 3 spokes leave a ~600px arc and 5 leave ~360px.

AN EIGHTH MEASUREMENT FAULT, AND IT SAID THE FEATURE WAS DEAD
The first run reported ZERO hits while the diagnostic showed beams passing 0.3px from the player -
straight through them. playerHit() sets player.dead; it does NOT touch invuln, hp, shield or lives
on a no-shield hit. The probe was watching invuln and hp. Isolating playerHit in one call found it
in a single shot after the geometry had already been proven correct.

Rendered at warm-up, live x3 and live x5 with bullets in flight: docs/proofs/beamrake_0812n.png.

Suite 2,591 / 231 / 5 - the same five long-standing failures.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
