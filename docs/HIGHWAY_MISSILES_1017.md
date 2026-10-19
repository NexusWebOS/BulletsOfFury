# Stage 4 roadside atomic missile pads — October 17

Mike requested tall, shootable missiles on launch pads beside the highway.
An escaped missile must return as an atomic strike. The installed owner is
`assets/highway_missiles_1017.js`, loaded after the current combat layers.

The two shoulders use the actual Lost Airbase highway edges: source x334
and x690 on the1024px master, scaled into the680px world. Pad centres are
34px outside those edges. The pad's visible footprint is66px wide; existing
armour retains the highway. Loaded pads and empty cradles follow the same
unwrapped `LA1007.scroll` publication, including reflected tile seams.

## Encounter

1. A pad enters with an upright missile. Its entire missile must become
   visible before its warning countdown begins. Source-pixel amber lamps,
   the existing alert symbol and shared warning beeps announce launch.
2. It launches north with accelerating thrust. Standing and ascending
   missiles remain ordinary enemies: guns, spread, beams, flame, both orbs,
   chainguns and Retina missiles use the existing hit/damage owners.
   Native `markHit` changes the actual damaged pixels and expires normally.
3. Destroying it in either phase prevents the atomic return. Its empty
   ground cradle remains anchored to the shoulder. A Retina lock persists
   while even the ascending tail remains visible above the centre boundary.
4. Only a fully escaped missile commits a return. Its circular nuclear
   Retina marks its actual blast radius, progressing green/yellow/red with
   beeps. The target stays fixed after the pilot moves. The pointed missile
   drops vertically from the north during the last0.95s; descent itself is
   harmless. An escaped return is committed ordnance, not another enemy.
5. Impact uses the approved32-pose atomic cloud, launch/impact sounds,
   flash, shock rings and rumble. The shared ground-strike owner applies
   damage only at impact and at most once per seat. Moving outside the
   marked radius avoids it. The visual mushroom lasts1.8s.

| Difficulty | Missile HP | Visible launch warning | Pad spacing in terrain pixels | Return warning | Blast radius |
|---|---:|---:|---:|---:|---:|
| Easy |14|4.4s|640|3.4s|52px|
| Normal |18|3.8s|540|3.2s|58px|
| Hard |22|3.3s|420|3.0s|64px|
| Furious |26|2.9s|300|2.8s|70px|

Co-op missile HP uses the existing1.5x encounter convention. Simultaneous
missiles are capped at two. Props do not consume the authored fighter-wave
pressure allowance. The director alternates shoulders, pauses new arrivals
through boss/miniboss warnings and fights, and stops14s before the final
boss approach. An already escaped return keeps its independent commitment.
Pause freezes the sequence; stage reset removes its actors and returns.

## Authored art

PixelLab Pixen supplied one128x128 empty pad and one64x192 upright missile.
No local identity image was uploaded. The generated PNGs remain archived
under `_ART_SOURCES/highway_missiles_1017`, with job IDs and exact prompts.
`_BUILD_SOURCE/build_highway_missiles_1017.py` owns the loose exports and
`assets/highway_missile_art_1017.js`. Every frame is even, uncropped and
unstretched; pad pivot64,80/scale0.55 and missile pivot32,96/scale0.64 remain
fixed. The lamp companion contains only the pad's original amber pixels.
Three shipping PNGs total30,034bytes. Existing missile-thrust frames,
nuclear Retina and atomic-cloud frames supply animation. No atlas changes.

## Verification

`python _BUILD_SOURCE/probe_highway_missiles_1017.py` verifies actual keyboard
gunfire across all four difficulties/eight weapons, ascent interception,
late visible-tail hits/locks, cancelling a destroyed missile's return,
one committed escape/impact, circular warning pixels versus the real blast,
safe movement, lethal centre impact, reflected-seam anchoring, hit-flash
pixels/expiry, pause/reset, stage scope and stronger difficulty pressure.
The45s director fixtures spawn3 Normal,4 Hard and5 Furious pads. Native
61/61 checks pass with no page, console, drawing or missing-asset errors.

The existing `_BUILD_SOURCE/probe_targeting_1017.py` passes96/96; the review
page passes6/6 native checks, including its actual gunfire button and
namespaced storage. Required `node --check assets/game.js` passes. The
complete `node _BUILD_SOURCE/test_fl.js` reaches8754 passing assertions,
zero errors, its final BUILD OK banner and exit0. That core harness does
not load the new late layer; the Chromium checks verify its actual owner.
See `docs/qa/highway_missiles_1017.json`; temporary captures/logs are under
`_shots/highway_missiles_1017`. Native screenshots were visually inspected.

The review at `docs/previews/highway_missiles_1017/index.html` embeds the
actual game at its regular FOV/side HUD, replays launches, fires real gun
bursts, and can run the authored highway plan. Its storage is isolated
before boot. Existing `game.js`, test harness, highway-armour and targeting
files retain their starting hashes. The index changes for this request
are exactly two new loader tags. Separate local work remains intact.
No commit or push was requested for this change.
