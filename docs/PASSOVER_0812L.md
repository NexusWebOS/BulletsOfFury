0812l: the weapon-by-stage spec, the ice breath, hit sounds, and boss HP

ONE TABLE DECIDES WHAT A SLOT IS - ICON, NAME AND DROP
Mike: "On stage 2 when Freezer got the icebreath icon, it said Lvl 1 flamethrower."

Exactly that. The ICON lookup already knew about Freezer and about stage 3; the ANNOUNCE read a
flat WEAPONS[] array that knew about neither, so slot 4 said FLAMETHROWER to everyone on every
stage while the art said ice. Two systems answering the same question. His rules are now one
lookup that the icon, the name and the drop bag all read:

  FLAME SLOT   freezer st1 flamethrower | st2 ICEBREATH | st3 WITHHELD | st4+ either
               everyone else            flamethrower
  ORB SLOT     freezer st3+ FIREICE | everyone st3 FIREORB | otherwise ICE ORB

Verified across both pilots and five stages; the announce text now matches the icon in every cell.
The variant is BAKED onto the pickup at spawn rather than recomputed at draw, because stage 4+
lets Freezer roll either flame variant and a per-frame re-roll would flicker between two icons
while the crate falls. And a slot with no variant is simply not in the drop bag, which is how
"disable ice breath for him on stage 3" is enforced - the bag is the thing that matters, not the
icon, which still answers harmlessly for a slot that never drops.

ICE BREATH WAS HALF-TRANSPARENT ON PURPOSE, AND MIKE HAS OVERRULED IT
0801ku set ICE_ALPHA to 0.5 "so the player can still see the enemies inside it". His word now is
"its too transparent, fix it." 0.86, where the plume reads solid and a unit inside is still a
discernible silhouette. NOT fixed by stacking passes - the note beside it records that additive
copies blow a near-white ice mass out to a featureless slab.

A CONTINUOUS WEAPON HAS TO BE HEARD LANDING
The beam, the flamethrower and the ice breath all deal damage on a tick while the trigger is held
and none of them made a sound on contact - only the firing sound. A held laser buried in a boss
was silent, which is why it never read as connecting. Six sites wired: beam and flame each on
enemy, boss and miniboss. RATE-LIMITED PER ELEMENT, which is the whole difficulty: these run every
frame or two, so an ungated call is sixty plays a second and reads as a buzzsaw. One play per 90ms
per element, gated on stateT rather than performance.now() so two hits in one frame cannot both
pass - the same correction 0811y made to the pellet.

BOSS AND MINIBOSS HP RAMP FROM STAGE 2
A multiplier on top of the existing curve, growing with the stage: x1.15 on 2 up to x1.69 on 8.
Stage 1 is deliberately untouched - it is the fight a new player learns on, and the jungle cruiser
was tuned at 210. Applied to the minis in ONE place, after the spawn switch has finished with the
object, because their HP is set in half a dozen branches (the ship table's absolutes, the
quad-laser's own figure, the modular builds) and anywhere earlier would catch only some.

THREE ASSERTIONS DEFENDED THE OLD SPEC and were updated, not the code: the 0801ku 50% alpha, "every
other stage still shows the ice orb" (Freezer keeps the fire-ice orb now), and "Freezer's
flamethrower slot is ICE BREATH on every stage" (it is stage 2 onward, withheld on 3). A fourth of
my own failed on correct code by testing the icon for a withheld slot instead of the drop bag.

Suite 2,570 / 230 / 5 - the same five long-standing failures.

NOT DONE, and not started: the lava boats on stage 2, and the big one - charge-up laser, spread
laser, spread and homing missile attacks, and the jet bosses charging, doing off-screen X-pattern
strikes and vertical ram runs. That is a fight-design pass and wants its own drop.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
