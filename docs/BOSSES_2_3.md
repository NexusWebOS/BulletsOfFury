# STAGE 2 + 3 MECH BOSSES — restored and verified (drop 0801ab)

    verify 212 passed / 0 failed
    both bosses driven END TO END in the harness: spawn -> entrance -> fight -> limb destruction

## What was already intact

The reverts earlier in the session removed the DERIVED CUTS (traced turrets, limb extractions,
erased bases) — they did not touch the mech system. All of this survived:

    mechInit · genesisInit · mechDraw · genesisDraw · mechAimCannons · bossFightTick · mechTankDrive

Stage 2 was complete. Stage 3 had the mech but NO ENTRANCE — the Cryo Behemoth simply appeared.

## Both now enter on the chain haul

The genesis system was already tag-driven, so stage 3 needed a theme rather than new code:

    mbg2  MAGMA   hauls its limbs out of the LAVA. Warm surface, ember locks, white-gold ignite.
    mbg3  CRYO    hauls them out of a FROZEN SHELF. The ice fractures as each piece breaks free —
                  the crack count grows with how many limbs are already home, so the shelf visibly
                  breaks up across the sequence — and the ignite flash is white-blue.

Same machine, same 12.6s beat structure, different world underneath. The same reasoning as the
tank rule: a Cryo Behemoth should not look like it climbed out of a volcano.

## Verified behaviour, both bosses

    builds as an 8-component mech
    enters on the chain-haul genesis, torso first
    the entrance completes on its own
    and hands over to the fight
    7 components carry a limb HP pool (5 limbs x 20%)
    the fight state machine runs and sits in a valid attack phase
    a limb can be shot off independently
    AND ITS ARM GOES WITH IT — they share one health pool, as specified
    the surviving cannon still tracks the player

That last pair is the one worth watching in play: shoot a cannon off and the arm dies with it,
because Mike's rule was that an arm and its cannon are ONE limb hauled in on ONE chain.

## Chain lightning, third attempt (drop 0801aa)

    attempt 1  scale one sprite by its aspect      -> 280px wide on a long arc
    attempt 2  pin the width, stretch the sprite   -> smeared 10x along its axis
    attempt 3  REPEAT the piece along the line     -> correct

Mike: *"you should just be using the short and long pieces, and rotate them where needed to extend
to other enemies like a chain lightning line."*

bolt_0 and bolt_1 are laid end to end along the vector and rotated to it. A long arc is MORE
SEGMENTS, so every piece keeps its own natural proportion no matter how far the chain reaches.
Alternate pieces are mirrored so it never reads as a repeated tile. Measured across a 4-hop chain:
13 segments, 5-12px thick throughout regardless of hop length.

The branched frames (2..8) are kept for the struck node, which is where a fork actually belongs.
