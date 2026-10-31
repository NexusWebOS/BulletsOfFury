# Desert Breaker and vehicle movement — October 13, 2026

Local implementation of Mike's open desert replacement and vehicle feedback.
No commit or push is part of this pass.

## Campaign replacement

Level 5 / password slot 3 is now **DESERT BREAKER**, a tank battlefield with
four mixed formations (16 hostiles total). The retired Museum of Violence
source remains archived in the checkout; its mission registration is replaced,
and its old pickup/blast hooks are disabled for the desert state. Existing
Level 5 password `OD-237D-5JXP` still resolves to the same campaign slot.

The player starts with a level-2 Vulcan and 12 Retina missiles. Each new
formation refills four missiles (up to 12), downed aircraft drop missile
supplies, and low stock can trigger another supply drop. Aircraft use the
ordinary Retina target identities and guided missile collision. Clear all four
formations to continue into Night Run.

All scheduled reinforcements begin at least 105 pixels north of the current
viewport; large armor begins 130 pixels above it. Pending arrivals stay in the
schedule until their entry time. They travel continuously into view. The center
sand lane stays open. Collision follows the rocky extreme edges.

## Vehicle behavior

Player hull steering now accepts a full reversal; the former 2.65-radian cutoff
could leave the hull facing the wrong direction. New and legacy mobile armor
share gradual steering and acceleration, aligned travel, controlled reverse,
and separation. The four new tank families are larger and have corresponding
collision radii. Fast shells use a swept segment query so crossing a hull
between ticks does not miss it.

Jackal and Bastion can warn for 0.9 seconds before accelerating into a committed
ram. A ram starts only when its warning is on screen; the charge does not home
onto a sidestepping player. Recovery and a cooldown prevent consecutive rams.
Stable authored hull drawings replace rapid alternation between mismatched
whole-vehicle plates. Recoil, turning, travel, track-distance banks (where the
authored modular tracks exist), and exhaust supply continuous motion.

Night Run now brings jets, gun trucks and runners from the north. Trucks
approach, pace, visibly warn and ram. The player truck makes gradual lane
changes, with heading following the motion. Mounted crew are larger. Jets use
straight passes with controlled lane changes. Enemies wait at least 0.7 seconds
after becoming visible before firing; the truck has 120ms hull-impact recovery
so simultaneous impacts do not consume its armor in one instant.

## Authored art

`expansion/topdown/art/desert_1013/source/desert_raw.png` was generated with the
built-in imagegen tool, 1024x1536. Its exact prompt is beside it. The owning
`_research/build_desert_1013.py` uses one uniform nearest-neighbor scale to
export an 800x1200 plate; the source hash, dimensions, and scale are recorded in
`art/desert_1013/export.json`. Both dimensions remain even. Aircraft and armor
retain their existing authored designs. No procedural replacement sprites.

## Verification

`expansion/topdown/_research/probe_desert_1013.py`: 18/18 native Chromium checks,
zero page/console errors against the production index (no injected modules). The checks exercise all mobile armor families remaining finite through turns/braking, full reversal, warned ram and
actual movement-input evasion, swept collision, actual Retina lock and guided
missile flight against a moving aircraft, four-wave death/clear accounting,
north entry, pursuit wreck restart and a complete normal-hull pursuit bot.
Screenshots of the desert, ram warning, live air lock and pursuit were inspected.

The 150-second normal-hull pursuit bot finishes with 88 HP, 65 kills, two
intercepted rockets and zero restarts. It aims every 250ms and fires; this is
feasibility evidence, not a human playtest or physical controller claim. Desert
wave completion uses the ordinary damage/death API to verify scheduling and
progression; separate checks exercise player firing and aircraft missile damage.
Portable check results: `docs/qa/overdrive_desert_1013.json`.

The root integration run owns the required base-game regression suite and
combined campaign verification after all concurrently authored modules load.
