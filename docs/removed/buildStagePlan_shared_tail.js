/* REMOVED IN DROP 0807u — the shared wave tail from buildStagePlan().

   Mike: "on levels 6 you had enemies from all levels appearing for some reason ... you have
   something conflicting with some other code thats stopping waves from appearing right."

   THIS WAS IT. After each stage's own table ran, this tail added 31 MORE waves across 12 enemy
   types to every stage 2-8, gated only on stageNum>=2 / >=3. Stage 6 was getting assault,
   drone, gunship, frost, cryo, mine, octo, mech, scout, shieldd, turdrone and icegun on top of
   its own storm-front cast — which is exactly the "enemies from all levels" he saw, and why
   the per-stage waves never played as authored.

   Kept here verbatim so nothing is lost while the per-enemy rebuild happens.
*/

if(stageNum===1) return P;

  // common early
  add(2.0, ()=> vRow('drone', Math.round(4*D), {pattern:'sine', stagger:0.0, amp:36}));
  add(4.5, ()=> { for(let i=0;i<Math.round(5*D);i++) spawnEnemy('drone', 40+i*((VW-80)/5), -20-i*18, {pattern:'sine',phase:i*0.6,amp:30}); });
  add(7.5, ()=> vRow('assault', Math.round(2+stageNum*0.4), {pattern:'straight'}));
  add(10.0,()=> { for(let i=0;i<Math.round(6*D);i++) spawnEnemy('drone', VW*0.2+ (i%2)*VW*0.6, -20-i*20, {pattern:'dive',amp:40}); });
  add(13.0,()=> { spawnEnemy('assault', VW*0.30, -60, {pattern:'skydive', _tx:VW*0.30}); spawnEnemy('assault', VW*0.70, -60, {pattern:'skydive', _tx:VW*0.70}); });
  add(16.0,()=> vRow('assault', Math.round(3*D), {pattern:'sine',amp:40}));
  add(19.0,()=> { for(let i=0;i<Math.round(5*D);i++) spawnEnemy('mine', 50+i*((VW-100)/Math.max(1,Math.round(5*D)-1)), -20, {}); });
  add(22.0,()=> vRow('gunship', Math.round(1+stageNum*0.3), {pattern:'straight'}));
  add(25.0,()=> { for(let i=0;i<Math.round(6*D);i++) spawnEnemy('drone', 40+i*((VW-80)/5), -20, {pattern:'sine',phase:i*0.8,amp:34}); });
  add(28.0,()=> vRow('assault', Math.round(3*D), {pattern:'straight'}));
  // mid-heavy depending on stage
  if(stageNum>=2) add(31.0,()=> vRow('octo', Math.round(1+stageNum*0.3), {pattern:'weave'}));
  // STAGE 2 "It's Hot in Here": Galaga-style kamikaze drone pairs that criss-cross then body-dive the player
  if(stageNum===2){
    add(9.0,  ()=> vKamikazePair(1));                 // first taste: one pair
    add(18.0, ()=> vKamikazePair(2));                 // two pairs, staggered
    add(27.0, ()=> vKamikazePair(2, {vy:1.7}));       // faster
    add(38.0, ()=> vKamikazePair(3, {vy:1.8}));       // swarm of three pairs
    add(44.0, ()=> vKamikazePair(2, {vy:2.0}));       // pre-boss pressure
  }
  if(stageNum>=3) add(33.0,()=> vRow('mech', Math.round(1+stageNum*0.25), {pattern:'straight'}));
  // ---- themed master-art enemies ----
  // TANKS SCRAPPED for now (not front-facing). Ground stages get rotating gun turrets instead.
  /* LEGACY STAGE-1 TAIL (drop 0801jw). Mike: "Jets randomly spawned at the beach
     line". These blocks add assault / gunship / scout / shieldd / turdrone on top of
     the authored plan - none of which are in the stage-1 roster he specified. Stage
     4 keeps its share; stage 1 is dropped. */
    if(stageNum===4){
    add(11.5,()=> { spawnEnemy('assault', VW*0.25, -60, {pattern:'skydive', _tx:VW*0.25}); spawnEnemy('assault', VW*0.75, -60, {pattern:'skydive', _tx:VW*0.75}); });
    add(26.0,()=> { spawnEnemy('gunship', VW*0.5, -60, {pattern:'skydive', _tx:VW*0.5}); });
    // small stationary turret-tanks on the ground below the player, firing straight up
  }
  /* LEGACY STAGE-1 TAIL (drop 0801jw). Mike: "Jets randomly spawned at the beach
     line". These blocks add assault / gunship / scout / shieldd / turdrone on top of
     the authored plan - none of which are in the stage-1 roster he specified. Stage
     4 keeps its share; stage 1 is dropped. */
    if(false){
    // Level-1 extra jets folded into the jungle roster (drone/bomber/intcp/turdrone/mdrone per Mike).
    // The primary stage-1 wave block above is the authoritative roster; these are light fill only.
    add(24.0,()=> vRow('scout', Math.round(3*D), {pattern:'weave',amp:46}));
    add(37.0,()=> { spawnEnemy('shieldd',VW*0.4,-30,{}); spawnEnemy('turdrone',VW*0.6,-30,{}); });
  }
  /* THE GENERIC TIMELINE MUST NOT RUN ON STAGE 1 (drop 0801jw). Mike: "Jets
     randomly spawned at the beach line, no tanks were shown or visible."

     Measured: stage 1's plan came back with THIRTY-FOUR entries when the authored
     plan has fifteen. Everything below here - the drone / assault / mine / gunship
     / scout timeline - was appended unconditionally on top of whatever the
     per-stage block had already built. That is the random jets he is seeing, and
     they are what pushed the enemy cap so the tanks had no room.

     Stage 1 is fully authored now, so it opts out. */
  if(stageNum!==1){

  if(stageNum>=3){
    // cryo squadron in the frozen valley and beyond
    add(9.0, ()=> vRow('frost', Math.round(3*D), {pattern:'weave', amp:40}));
    add(17.0,()=> { for(let i=0;i<Math.round(4*D);i++) spawnEnemy('frost', 40+i*((VW-80)/Math.max(1,Math.round(4*D)-1)), -20-i*16, {pattern:'sine',phase:i*0.5,amp:34}); });
    add(26.0,()=> vRow('cryo', Math.round(1+stageNum*0.3), {pattern:'sine', amp:30}));
    add(35.0,()=> vRow('icegun', Math.round(1+stageNum*0.25), {pattern:'strafe'}));
    add(43.0,()=> { vRow('frost', Math.round(3*D), {pattern:'weave',amp:44}); spawnEnemy('cryo', VW*0.5,-30,{pattern:'dive'}); });
  }
  add(34.0,()=> { spawnEnemy('gunship', VW*0.25, -60, {pattern:'skydive', _tx:VW*0.25}); spawnEnemy('gunship', VW*0.75, -60, {pattern:'skydive', _tx:VW*0.75}); spawnEnemy('assault', VW*0.5, -70, {pattern:'skydive', _tx:VW*0.5}); });
  add(37.0,()=> { for(let i=0;i<Math.round(7*D);i++) spawnEnemy('drone', VW*0.15+(i%3)*VW*0.32, -20-((i/3|0))*22, {pattern:'dive',amp:44}); });
  add(40.0,()=> { if(Audio.SFX&&Audio.SFX.enemyunits)Audio.SFX.enemyunits(); vRow('gunship', Math.round(1+stageNum*0.4), {pattern:'sine',amp:24}); });
  add(42.0,()=> vRow('assault', Math.round(4*D), {pattern:'straight'}));
  // last push before boss
  add(curStage.length-3, ()=> vRow('drone', Math.round(5*D), {pattern:'sine',amp:40}));
    }
  /* THE DISPATCHER WALKS THIS ARRAY IN ORDER (drop 0801jx). It holds waveIdx and
     waits for stagePlan[waveIdx].t before moving on - so a single entry whose time
     is later than the ones after it BLOCKS everything behind it.

     Re-timing stage 1's ground waves to land past the coastline put them out of
     sequence: [2, 6, 8.2, 36, 21, 24, 30, 44, 50, 47 ...]. Entry 3 at t=36 stalled
     the queue, and waves 4 onward - every jet after the opening, the miniboss run,
     all of it - never fired. That is why only racers appeared.

     Sorting by time makes the array match the order the dispatcher assumes, and
     costs nothing: authoring stays free to add waves in whatever order reads best. */
  P.sort((a,b)=> (a.t||0) - (b.t||0));