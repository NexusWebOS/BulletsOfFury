# STEP 2 — 1 -> 2 · WATER

    verify: 77 passed, 0 failed   ·   harness 1757 assertions
    Route runs 382 frames, four beats, hands off to stage 2.

## Your spec, and how each line is met

> *"remember the dam swaps to a destroyed image at the end. Keep the player positioned where they
> were at the time of the cut, and after the cut position them where they should be. from there,
> they fly directly past the broken dam, use the water tile, and make us fly over water. follow
> the player. do not fly them off in the distance to some cut water. this should look fluid. then
> you transition fade as we follow them flying to the stage end stats screen."*

**"follow the player" / "do not fly them off in the distance"** — this is the whole reason 1->2 is
not just the generic outbound. That one CLIMBS the player up and off the top of the screen, which
is the opposite of what you asked for here. So the water route SKIPS the climb entirely: the
player is held at the exact position they had when the boss died, and the WORLD moves underneath.
Asserted: **0 position changes across all 382 frames.**

**Four beats:**

    PAST     2.2s   the jungle keeps scrolling and accelerating, so the broken dam passes BEHIND
    WATER    1.6s   the water flat washes in and takes over the ground
    CRUISE   1.5s   a beat of open water, so it reads as a journey rather than a wipe
    FADE     1.0s   to black, into the stage-end stats

**The water washes DOWN from the top.** In a vertical scroller everything you approach enters from
the top and travels past you. Rising from the bottom would read as the sea coming up to meet the
player. Same lesson the opening's shoreline taught, and it is asserted so it cannot flip back.

**No connector plate.** `o.con` stays null. Built from the stage background plus the 64x64
`tflat_water` flat, tiled and scrolling, with a soft foam line at the boundary so the takeover is
not a hard rectangle.

## Routes are per-join now

`DBG.transitions` gated all eight joins at once, which is why switching it on lit up seven unbuilt
ones. 1 -> 2 is built and tested, so it populates on its own. The rest still wait behind the flag.
One join, one switch.

## THE DAM SWAP IS BROKEN, AND IT IS NOT SOMETHING I DID

Your spec opens with *"remember the dam swaps to a destroyed image at the end."* It does not, and
it has not for some time.

    damBroken flips true correctly at boss death
    the swap then asks for ASSETS.mapJungleDam
    that points at assets/levels/mapJungleDam.png
    THAT FILE DOES NOT EXIST, and no 800x3616 dam variant exists anywhere in the tree

`ASSETS.rdy()` fails, the code falls back to the intact map, and the dam never visibly breaks.
There IS a `lvl1_master_dam` (325x2600) that genuinely differs from `lvl1_master` in its top
region — clearly the dam pair — but it is a **different, smaller asset** than the 800x3616
`mapJungle` the stage actually draws. It is not a drop-in.

I have not touched it. The stage-1 rule stands, and picking a replacement is an art call.

Two ways forward when you want it:
  1. an 800x3616 destroyed variant of mapJungle, and the existing swap starts working immediately
  2. or point stage 1 at the lvl1_master pair instead — but that changes the whole level's
     background, which is exactly the kind of thing I am not doing to level 1 without you saying so

The transition itself is complete either way: the dam passes behind you during the PAST beat. It
just passes intact until that art exists.

## Test it

    COLE1   drops you at the stage-1 boss on its last sliver — kill it and the route plays
