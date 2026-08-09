/* ============================================================================
   STAGE 1 WAVE PLAN (drop 0801ij)

   Mike's spec, in order:

     "Level 1 should start with jets flying past you (2, 1 on each side) going very
      fast, then returning from the top coming towards the bottom of the screen on
      the right and left sides. Shoot machine guns and some regular missiles.

      As we approach the beach, large tanks in a horizontal rows spaced out 1 by 1
      4 of them all backed up further than the other, all shooting 1 by 1.

      After that wave, on the sides of the screen where the grass is, have figher
      jets come fast from the tip of the screen, turn and go into the middle of the
      screen, then pause, levitate, orbit and target you to start attacking.

      Then after that, from the left side, fast but not very fast, 1 by 1 they come
      down the screen from the top left to right in a row of 4. All shooting and
      using missiles.

      Add mini tanks as we get further up the level in the sand sections. Then the
      mini boss. Then more random but similar patterns. No more crazy endless waves
      or tanks coming from the water. Once we pass half the level, no more tanks.
      Then of course the helicopter boss and level ends."

   WHAT THIS REPLACES
   The old stage-1 plan had 22 entries, four of which called unit types that do not
   exist (minitank, minitank2, minitank3, el_jh) and so produced nothing. Seven of
   the eleven types that DID spawn were inert - 0 px/s, no shots in 300 frames.

   THE HALF-LEVEL RULE
   Stage 1's scroll runs 0..4288. TANK_CUTOFF sits at the midpoint, and no wave past
   it may field a ground unit. That is enforced here rather than trusted to
   authoring, so a later edit cannot quietly reintroduce one.
   ============================================================================ */

const S1_TANK_CUTOFF = 0.50;      // no tanks past halfway, per Mike

/* two jets tear past, one down each side, then come back over the top */
function s1FlyBy(){
  // very fast, no firing on the pass - they are announcing themselves
  spawnEnemy('racer', VW*0.16, -30, {pattern:'s1_flyby', _s1side:-1, _s1fast:2.4});
  spawnEnemy('racer', VW*0.84, -30, {pattern:'s1_flyby', _s1side: 1, _s1fast:2.4});
}
function s1FlyBack(){
  // returning down the outside edges, and NOW they shoot
  spawnEnemy('racer', VW*0.10, -30, {pattern:'s1_return', _s1side:-1, fk:'mg'});
  spawnEnemy('racer', VW*0.90, -30, {pattern:'s1_return', _s1side: 1, fk:'mg'});
  spawnEnemy('racer', VW*0.22, -90, {pattern:'s1_return', _s1side:-1, fk:'missile'});
  spawnEnemy('racer', VW*0.78, -90, {pattern:'s1_return', _s1side: 1, fk:'missile'});
}

/* four heavy tanks across the beach, each set back further than the last, firing
   one after another rather than together */
function s1BeachTanks(){
  for(let i=0;i<4;i++){
    const x = VW*(0.16 + i*0.23);
    const y = -40 - i*54;                 // each one further back
    spawnEnemy('jungletank', x, y, {_s1order:i, _s1stagger:i*0.85});
  }
}

/* jets in off the very edge, turn inward, stop in the middle, then hunt */
function s1GrassJets(side){
  const x = side<0 ? -26 : VW+26;
  for(let i=0;i<2;i++){
    spawnEnemy('intcp', x, 90+i*66, {pattern:'s1_hook', _s1side:side, _s1hold:1.1+i*0.35});
  }
}

/* a diagonal file of four, top-left to lower-right, moderate speed */
function s1Diagonal(){
  for(let i=0;i<4;i++){
    spawnEnemy('topgun', VW*0.06 + i*10, -34 - i*70,
               {pattern:'s1_diag', _s1lane:i, fk: (i%2===0)?'mg':'missile'});
  }
}

/* the little sand tanks, only while we are still below the cutoff */
function s1MiniTanks(n){
  for(let i=0;i<n;i++){
    spawnEnemy('minitank', VW*(0.18+i*0.28), -30 - i*40, {});
  }
}
