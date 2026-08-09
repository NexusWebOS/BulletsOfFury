# BOSS FIGHT SYSTEM — drop 0731w

Built from how the games you named actually work. Sources read, not guessed at.

## What the research said

**Contra III, Tri-Transforming Wall Walker** — three forms, and one phase where the boss CANNOT BE
HARMED at all. Its sibling is documented as: *"each time it protrudes its drills, its core is
exposed and vulnerable to damage."* The boss opening itself to hurt you is what lets you hurt it.

**Contra III's tank** — *"drives forward, reaching close to the left edge, then reverses to the
far right end and stops for a moment before repeating."* You arrived at the same rule
independently. That stop is not a pause in the animation, it is the attack window.

**Shinobi III, Mechasaurus** — *"Once damaged enough, its head is destroyed."* Shadow Master
*"turns bright red"* halfway. The boss visibly becomes a different thing as you win.

**Boghog, shmups.wiki** — *"Chunking patterns is vital for visibility... group bullets up into
lines and other clear patterns, single stray bullets are hard to read and can often feel unfair."*

**Game Developer, boss design for shmups** — *"Intensity is not found through force, but through
dynamism. The more varied attacks from the boss, the better."* And: mid bosses should never take
longer than end bosses.

## The four rules, and they are enforced in the harness

    1  NOTHING FIRES UNTELEGRAPHED
       Minimum 0.45s wind-up, and the wind-up DRAWS THE SHAPE of what is coming. The fan draws
       its cone, the wall draws its gap, the lance draws its sight line. Eased so urgency lands
       late rather than the whole wind-up feeling uniform.

    2  BULLETS COME IN SHAPES
       fan     7 across a 1.15 rad cone, filling exactly the cone the telegraph drew
       wall    13 across the screen with ONE two-wide gap — the shape is the information
       pincer  two 5-shot arcs converging on the player: you must commit to a side early
       ring    16 evenly spaced, ignores the player entirely — dodged by position, a breather
       mortar  4 arcs onto MARKED ground, marker lit for the whole flight
       lance   one heavy aimed shot, 0.85s wind-up — the fair one-off you asked for

    3  ATTACKING COSTS THE BOSS SOMETHING
       Every pattern leaves a recovery window of 0.6s or more. Damage during it is DOUBLED.
       Pressuring the boss is how you earn your openings — straight from the Contra drill.

    4  PHASES CHANGE THE FIGHT, NOT THE NUMBERS
       Three phases at 100 / 66 / 33 percent. At each one the PATTERN SET is replaced rather
       than the same attacks coming faster. Phase also advances on PARTS LOST, so tearing the
       limbs off accelerates the fight independently of chip damage.

## Kits are per archetype

A boss never gets the whole library — its kit should read as ITS kit.

    mech       fan, lance      -> +pincer      -> pincer, ring, lance
    tank       wall, lance     -> +mortar      -> mortar, pincer, wall
    aircraft   fan, wall       -> +pincer      -> pincer, ring, fan
    fortress   mortar, wall    -> +ring        -> ring, wall, mortar
    crawler    fan, mortar     -> +pincer      -> ring, pincer, mortar
    segmented  ring, lance     -> +pincer      -> pincer, ring, fan

And the next pattern is never the one just used. Dynamism over volume.

## Tanks

Three states, no idle motion, straight from the Contra III tank:

    ROLL    advances at 26 px/s
    BRAKE   decelerates at 54 px/s to a dead stop and holds — this is the attack window
    STRAFE  sideways at 9 px/s, toward open ground, never twice in a row

Excluded from the hover and from thrusters. A tank that bobs is a hovercraft.

## Verified

`verify_0730a.js` — 46 passed, 0 failed. The rules are asserted against LIVE VALUES through a
`bossRules()` introspection hook, not by string-matching source. Matching source only proves the
rule was typed; this proves the fight runs on those numbers.
