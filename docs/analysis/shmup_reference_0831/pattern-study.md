# Shmup reference study — 2026-08-31

Twelve supplied recordings were reviewed across their complete 33.5-minute runtime. Broad contact
sheets were followed by one- or two-second samples around useful attack windows so attacks could
be evaluated as sequences rather than single attractive frames. Player-fired effects were tracked
separately from enemy fire to avoid assigning the wrong behavior to boss AI.

## What the clips teach

The strongest encounters repeatedly combine three readable questions:

1. **Where is the promised safe space?** A lane, wedge, or rotating gap is established before the
   damaging pattern reaches the player.
2. **What is following the player?** Aimed bursts and homing pressure punish camping, but commit to
   the sampled position instead of tracking every pixel forever.
3. **When is it safe to counterattack?** Large beams, charges, and physical sweeps have visible
   recovery beats. Spectacle is separated from unavoidable damage.

The footage also shows that density alone is not difficulty. The effective patterns move as a
coherent shape: block rows, counter-rotating fans, paired gun pods, or a fixed beam lane. Unrelated
projectiles stacked on the same beat make the intended answer harder to read without making the
encounter more interesting.

## Clip-by-clip findings

- **19-20-21:** Physical horizontal lane pressure, rectangular fireball formations, and delayed
  rosette-like residue. Best lesson: a large hazard can occupy most of the arena if its open lane is
  stable and visually promised.
- **19-23-02:** Sparse orb rings, mine clusters, and slow large rounds. Useful as spacing reference;
  too simple to serve as a late boss vocabulary by itself.
- **19-25-15:** Independent wing/pod fire, fan volleys, radial formations, and a very large committed
  beam. Best lesson: detached hardpoints let a boss create crossfire without moving the main hull
  unpredictably.
- **19-29-01:** Warning presentation, boss-scale entrance, and a serpentine physical pass. Best
  lesson: the warning and entrance are part of the attack contract, not decoration.
- **19-30-04:** A mechanical boss using its body and breakable structure as the encounter. The crop
  limits projectile study, but reinforces that damage states and physical motion should be visible.
- **19-32-51:** Counter-rotating fans, moving gaps, paired pods, straight beam columns, and phase
  transformations. Strongest reference for controlled bullet density.
- **19-37-28:** Giant mechanical bosses, central beam pillars, side fans, destructible-looking
  sections, and escalating forms. Best lesson: later phases reuse the same grammar faster or from
  more emitters instead of replacing it with unrelated attacks.

## Additional data pass — clips 8–12

- **21-23-57:** A long military stage built from sparse aircraft, tanks, fixed emplacements, and
  large slow ground threats. Its strongest contribution is *quiet pressure*: tanks commit to a
  lane and orientation, terrain and ground targets carry part of the difficulty, and cleanup beats
  keep each wave readable. This confirms that Bullets of Fury's tanks should roll deliberately,
  face south while firing, and never wobble or stack on one another.
- **21-29-16:** Mixed ground/air staging, durable carrier-like enemies, modular damage, and player
  weapon examples. The large carriers advance on a stable heading while individual sections take
  damage, alternate sparse spreads, and leave a boss-sized destruction footprint. The purple
  bending lock-on stream is player fire, not an enemy pattern; it is useful reference for Maverick
  and the space homing weapons only.
- **21-37-52:** A rapid boss montage. The reusable ideas are appendage-led firing origins, curving
  streams whose gaps move predictably, temporary beam corridors, and giant bosses whose hull stays
  readable while local hardpoints do the attacking. Several clips are spectacle cuts rather than
  complete attack cycles, so they are shape references—not timing references.
- **21-39-45:** A short stage-wave sample with compact aircraft formations, pickup spacing, and
  simple aimed fire. It adds little new boss vocabulary, but is good confirmation that enemy groups
  should arrive as authored units with reserved spacing instead of independent random spawns.
- **21-42-35:** A compilation of several arcade shooters. Its useful gameplay section reinforces
  fast, high-contrast enemy shots; short formation passes; large destruction flashes; machinery
  that opens or transforms before attacking; and giant enemies that emerge from the stage
  architecture before their first firing beat. Later unrelated clips and advertisements were
  excluded from the mechanic study. The best new lesson is that fast danger stays fair when each
  squad has one recognizable entry shape and fires one committed burst before recovery or exit.

### New implementation implications

1. **Reserve formation slots before spawning.** Jets, tanks, and boats should claim a unit-sized
   lane cell so two bodies cannot overlap even when their paths converge.
2. **Use durable anchors in normal waves.** A heavy tank, carrier, or emplacement can own a lane
   while faster aircraft create short aimed-pressure beats around it.
3. **Give large enemies local damage states.** Hardpoints should stop firing, smoke, flash, or break
   away before the parent hull dies; the final explosion should cover the full unit and exceed it
   by roughly 25 percent, never fade the enemy out.
4. **Keep high-end hull motion restrained.** For giant bosses, attack complexity belongs in the
   turrets, limbs, projectiles, and temporary arena dividers. The hull itself should slide slowly
   enough that the player can predict the safe region.
5. **Separate weapon behavior from enemy behavior.** The winding lock-on beams in clip 9 support
   player homing/helix weapons, while enemy attacks still need warnings, committed release angles,
   destructible missiles where appropriate, and a recovery beat.
6. **Make the reveal part of the tell.** Doors, shutters, armor plates, and stage machinery can
   expose a boss or hardpoint before it fires. Finish the opening motion, hold the silhouette for a
   short recognition beat, then release the first burst instead of spawning and shooting at once.

## Bullets of Fury mapping

| Stage | Boss identity | Reference mechanic | Implementation direction |
| --- | --- | --- | --- |
| 4 | Storm Sovereign | Independent pods and crossfire | Retain its authored core turrets, helper guns, and slow predictable horizontal travel. |
| 5 | Xeno Regent | Rectangular formation walls | Add staggered void blocks with one promised two-lane door; escorts continue aimed pressure only between walls. |
| 6 | Doomsday Carrier Mk II | Beam columns and alternating pod banks | Retain THUNDERHEAD's warned lanes and alternating storm nodes; do not stack a generic volley underneath. |
| 7 | Sludge Emperor | Delayed residue rosettes | Plant three toxic residues, warn their radius, then bloom sequential gap-rings. The existing flood remains the moving-door pattern. |
| 8 | Vile Existence | Locked cross plus radial follow-up | Retain ANNIHILATION: it samples the old player location, commits, then follows with a ring that removes sectors toward the player. |
| 9 | Tidal Sovereign | Block lanes fused with moving water hazards | Add cascade rows with a two-lane door that walks one column per wave; keep Warden counter-rotation as the aimed-pressure layer. |

## Readability rules for the implementation

- Lane attacks always warn before release and preserve at least two player-widths of escape space.
- The safe opening moves at most one lane per wave.
- Aimed attacks sample once at release; no permanent pixel-perfect tracking.
- A boss cannot start a second set-piece while the first owns the attack channel.
- Horizontal boss travel remains slow and predictable while firing.
- Phase escalation increases emitter count, cadence, or speed—never all three on the same beat.
- Every dense pattern has a recovery beat long enough for the player to recognize the next tell.
