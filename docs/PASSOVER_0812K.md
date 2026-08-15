0812k: they were not appearing out of thin air, they were teleporting onto it

Two separate causes, both found by measuring where a unit first becomes drawable AND visible and
what FRACTION of its sprite is showing at that moment. That last number is the one that matches
what a player sees: a unit that flies in reveals a sliver, a unit that switches on reveals half of
itself at once.

THE BOATS WERE TELEPORTED ONTO THE SCREEN BY THEIR OWN STATION FLOOR
The waves spawn the flotilla correctly above the top edge - spawnEnemy('s1boatpatrol', VW*0.22,
-40) - and navalSteer ran clamp(e.y, 40, VH-60) on its FIRST tick, snapping it from -50 to +40 in
one frame. Tracked frame by frame: -50 at frame -1, +40 at frame 0, flat thereafter. With an 88px
hull that is 95% of the boat switching on at once, at age zero.

The floor cannot simply be removed. A naval unit holds station against the scroll and its own
southward drift is sin(hdg)*20*0.34, about 7px/s, so without the floor the flotilla would take
THIRTEEN SECONDS to cover the 90px. The floor is right; applying it before the hull had arrived
was not. There is a real approach now at 110px/s - a bit under a second - and _navIn latches so a
boat pushed back up by the scroll is not re-entered.

AND SIDE ENTRIES WERE SPAWNING WITH THE SPRITE ALREADY IN THE WORLD
offRightX(28)/offLeftX(28) put the unit's CENTRE 28px past the world edge, and the stage-1 jets
are 73 and 101 wide - half-widths of 36 and 50. So the hull was already protruding at spawn, and
with the camera panned right the world edge IS the screen edge. Fixed at the push site in
spawnEnemy, where c.w is final (it is not at the offRightX call), so every stage gets it.
HORIZONTAL ONLY and only for units already outside: the note above that push records an earlier
pop-in fix reverted for lifting units vertically and sending ground rigs off their band.

Measured on a 150-second stage-1 run, fraction of the sprite showing on each unit's first visible
frame: the boat 95% -> 1%, and every unit on the stage now 0-1%.

SEVEN MEASUREMENT FAULTS BEFORE THIS WAS TRUE, each producing a confident wrong answer:
  1. probe_popin watches spawnEnemy's ARGUMENT, not where the unit ends up. Reported 0 for 2 drops.
  2. An art check used e.art as if it were a base. It is the FULL baked key for nef units and
     something else for legacy ones - reported 24 of 24 units cold and one blind for 5,220 frames.
  3. A trap on enemies.push found nothing: the pools are REASSIGNED, not mutated, so the wrapper
     died at the first filter.
  4. A first-existence test compared only Y, so units entering from the SIDES at x -28/828/846 in
     an 800-wide world counted as materialising.
  5. A drawable() predicate gated on XART._src first. Every stage-1 unit has _src FALSE and
     rdy TRUE - the atlas CELLS resolve through a different map - so it rejected all 30 units.
  6. An inset metric ADDED half the sprite width, so a jet straddling the left edge at sx=-3
     scored 44px "inside the frame". It invented six of its seven hits.
  7. An inView test used the CENTRE, so a sprite counted as entering only once its middle crossed -
     by which point half of it had legitimately been on screen, and the first-sighting sample
     caught it 46% revealed.

Suite 2,565 / 230 / 5 - the same five long-standing failures. Section 225 asserts both fixes.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
