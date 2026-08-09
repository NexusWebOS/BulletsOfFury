# BOSS ROSTER — what exists, what is wired

    12 bosses registered   7952 manifest keys   88 MB of boss art
    build: 1335 assertions + 30, node --check clean

## Every boss has

| | |
|---|---|
| components | 7-10 named parts, position-locked on a 384x384 canvas |
| states | 4 per part: intact / damaged / critical / destroyed |
| master | assembled reference |
| fire fx | muzzleflash 6f, projectile 6f, impact 6f (CF_BossFireFX-Vol.2) |
| muzzle anchors | derived from each boss's own weapon components |

ASSEMBLY GUARANTEE VERIFIED ON ALL TWELVE: compositing every `intact` part reproduces the
shipped master at **max channel diff 0**. That is what makes per-part destruction safe — swap one
component to `destroyed` and nothing else shifts by a pixel.

## The roster

    tag     stage  boss                          parts  archetype
    mbg2      2    Magma Colossus                  8    mech      GENESIS
    mbo2      2    Obsidian Drill Tank             8    tank
    mbg3      3    Cryo Behemoth                   8    mech      GENESIS
    mbg3f     3    Glacier Rail Fortress           8    tank
    mbm4      4    MIRV Stalker                    8    tank
    mbw4      4    Warhawk Arsenal                 9    aircraft
    mbl5      5    Legion Command Tank             8    tank
    mbr5      5    Rampart Zero                    7    fortress
    mbc6      6    Cyclone Interceptor Carrier     9    aircraft
    mbs6      6    Storm Sovereign                 9    aircraft
    mbs7      7    Sludge Crawler                  9    crawler
    mbt7      7    Toxic Leviathan                10    segmented

Five distinct archetypes, and they do NOT share a part vocabulary:

    mech        left-cannon, right-cannon, arms, legs, head, torso
    tank        left-track, right-track, front-weapon, weapon-pods, rear-engine, turret-core, hull
    aircraft    engine-pods, weapon-racks, wings, tail, nose, command-core
    fortress    siege-arms, fortress-wings, command-core, ram-gate, gun-decks
    crawler     crusher-claws, front/rear legs, reactor-turret, head-cab, central-hull
    segmented   claws, head-core, body-segment-01..06, tail-blade

That matters for anything written against component names. Muzzle derivation already handles it —
it walks a candidate list per archetype (cannon, weapon-pod, weapon-rack, siege-arm, crusher-claw,
claw) and falls back to the central mount for single-weapon bosses.

## SEPARATE FRAMES: what was authored and what was not

**All 12** got components, damage states and fire fx.

**Only stage 2 and 3** got the Genesis motion pack:

    poseable modular pieces with pivots    only mbg2 / mbg3
    authored key poses (8)                 only mbg2 / mbg3
    broken-joint overlays (6)              only mbg2 / mbg3
    chain / cannonthrow / cannonretrieve   only mbg2 / mbg3   (11 reels vs 5)
    socket-free heads                      only mbg2 / mbg3

So the other ten have **5 reels** (breakup, idle, damage-overlay, muzzleflash, projectile) against
the mechs' **11**. They can be assembled, damaged part by part, and can shoot. They cannot do the
chain-haul genesis entrance, and they have no authored poses to move between.

**That is not a gap in the art so much as a difference in kind.** A tank has tracks, not arms —
there is nothing to sling on a chain. The genesis sequence was built for the two mechs because
they are the only two that come apart into limbs.

## What each of the ten still needs to fight

    1. an entrance          they have breakup for the death; nothing for the arrival
    2. an attack profile    fire fx exists and muzzles are anchored, but nothing decides
                            WHEN they shoot or in what pattern
    3. HP weighting         mechs use 5 limbs x 20%; a tank with 8 parts needs its own split
                            (tracks should not be worth the same as the turret core)

None of that needs new art.
