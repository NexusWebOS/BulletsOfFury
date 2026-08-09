/* MY FROM-SCRATCH STAGE 1 REBUILD — REVERTED IN DROP 0807v.

   The intent was right and Mike asked for it. The execution was not: stage 1's ground waves
   fire only inside a narrow terrain window — after reaching LAND at scroll 1416 and before the
   halfway cutoff at 2144, roughly t=35s to t=54s — and _s1Ground DEFERS a wave by decrementing
   waveIdx when it is not yet on land, which re-queues it and pushes everything behind it.

   Every placement I tried gave a DIFFERENT result across three suite runs: 4 fails, then 2,
   then 0. A level that plays differently each run is worse than one I have not touched, so the
   original table is restored and this is kept for the next attempt.

   What the next attempt needs to solve FIRST, before moving a single wave:
     - the deferral re-queues into a TIME-ORDERED plan, so a deferred ground wave competes with
       whatever else is due at that moment
     - the miniboss triggers at scroll ~2197, only ~53px past the halfway cutoff, so the entire
       ground section lives on a very thin margin
   Neither is a wave-placement problem. They are a scheduler problem, and that is what to fix.
*/

    if(stageNum===1){
    /* ============================================================
       STAGE 1 — REBUILT FROM SCRATCH (drop 0807v)

       Mike: "were starting from scratch and thats MY call ... the enemies themselves still
       remain for these levels, we just need to re-code them from scratch and 1 at a time as I
       tink thats best."

       Same five units as before — racer, intcp, topgun, jungletank, sandtank. Nothing new is
       introduced and nothing is borrowed from another stage. What is new is that EACH ONE HAS A
       DEFINED JOB, written here in one place, instead of inheriting a generic pattern from a
       shared library that was also feeding seven other stages.

       "You need to also make the enemies operate half like a shmup, half like high speed action."
       That is the through-line of the pacing below: the air units come in FAST on committed
       lines and leave — they are the high-speed half, and you dodge them. The ground units hold
       position and shoot — they are the shmup half, and you fight them. Waves alternate between
       the two so the level breathes instead of being a constant stream.

       THE FOUR UNITS, and what each is for:

         racer      the opener and the pace-setter. Enters top, commits to a straight fast lane,
                    exits bottom. Never turns back. Reads as traffic you weave through.
         topgun     the aggressor. Enters top in a file, holds mid-screen briefly to fire, then
                    presses down. This is the one that makes you move.
         intcp      the flanker. Enters from the SIDE at the player's height, crosses, and leaves.
                    Comes in pairs from alternating edges so the threat swaps sides.
         jungletank / sandtank
                    the ground half. They arrive with the terrain, hold their lane, and shoot up.
                    Gated behind _s1Ground so they never appear over water.

       TIMING. The stage runs ~90s to the miniboss. Waves are placed so there is never more than
       ~4s of nothing, and never two heavy waves back to back. ============================================================ */

    /* ⚠ THE TERRAIN GATE IS KEPT VERBATIM (drop 0807v). These three helpers are hard-won —
       Mike reported the coastline twice before they existed, and the comment inside explains
       exactly why a ground wave must ask the TERRAIN rather than the clock. The waves below are
       rewritten from scratch; this is not, because it was already right. */
    /* the halfway cutoff past which no ground wave fires — it lived at the top of the block I
       replaced, and dropping it took the whole stage down with a ReferenceError (drop 0807v) */
    const S1_HALF = 0.50;
    const _s1Past = () => {
      const cfg = (typeof _levelCfg==='function') ? _levelCfg() : null;
      const range = (cfg && cfg.scrollLen) ? cfg.scrollLen : 4288;
      return (mapScroll||0) / Math.max(1,range) > S1_HALF;
    };
    /* GATE ON THE TERRAIN, NOT THE CLOCK (drop 0801kb). Mike, twice now: "I dont
       see the big tanks at the coast line."

       Timing the beach wave to t=36 put it at scroll 1440 - just 24px past the
       coastline threshold of 1416. Any variance in pacing and the camera is still
       over water, where the swap at line 3843 correctly turns every ground unit
       into a stationship or gunboat. That is the margin the whole wave was riding.

       A ground wave now asks the terrain directly: it fires when we are ON LAND and
       before the halfway cutoff, and simply defers a beat if we are not there yet.
       The wave cannot be mistimed because it no longer depends on timing. */
    const _s1OnLand = () => {
      const cfg = (typeof _levelCfg==='function') ? _levelCfg() : null;
      const H = (cfg && cfg.h) || 4800;
      return (H - (mapScroll||0)) <= 3384 - 60;      // clear of the water, with margin
    };
    const _s1Ground = (fn) => function _g(){
      if(_s1Past()) return;                          // past halfway: no ground at all
      if(!_s1OnLand()){                              // still at sea - wait, do not convert
        if(typeof stagePlan!=='undefined' && stagePlan && waveIdx>0) waveIdx--;
        _waveGap = 0.5;
        return;
      }
      fn();
    };

    /* ---- 0-12s: THE OPENING. Racers only. Establishes the speed before anything shoots. ---- */
    add(2.0,  ()=>{ spawnEnemy('racer', VW*0.22, -30, {_fast:2.6, _noFire:true});
                    spawnEnemy('racer', VW*0.78, -30, {_fast:2.6, _noFire:true}); });
    add(5.0,  ()=>{ spawnEnemy('racer', VW*0.50, -30, {_fast:2.6, _noFire:true}); });
    add(8.0,  ()=>{ for(let i=0;i<3;i++)
                      spawnEnemy('racer', VW*(0.18+i*0.32), -30 - i*40, {_fast:2.2, fk:'gun'}); });

    /* ---- 12-26s: THE FIRST PRESSURE. Topguns hold and fire — the shmup half arrives. ---- */
    add(12.5, ()=>{ spawnEnemy('topgun', VW*0.34, -32, {fk:'gun'});
                    spawnEnemy('topgun', VW*0.66, -32, {fk:'gun'}); });
    add(17.0, ()=>{ for(let i=0;i<3;i++)
                      spawnEnemy('topgun', VW*(0.24+i*0.26), -32 - i*54, {fk:'gun'}); });
    add(22.0, ()=>{ spawnEnemy('racer', VW*0.12, -30, {_fast:2.4, fk:'gun'});
                    spawnEnemy('racer', VW*0.88, -30, {_fast:2.4, fk:'gun'}); });

    /* ---- 26-40s: THE FLANK. Intcp from the sides, alternating, at player height. ---- */
    add(26.5, ()=>{ spawnEnemy('intcp', -28, VH*0.34, {}); spawnEnemy('intcp', -28, VH*0.46, {}); });
    add(31.0, ()=>{ spawnEnemy('intcp', VW+28, VH*0.34, {}); spawnEnemy('intcp', VW+28, VH*0.46, {}); });
    add(35.5, ()=>{ spawnEnemy('intcp', -28, VH*0.30, {}); spawnEnemy('intcp', VW+28, VH*0.52, {}); });

    /* ---- 36-56s: THE GROUND ARRIVES. Behind the land gate, so never over water. ---- */
    /* ⚠ THE GROUND WINDOW IS NARROW, AND I PUT THESE OUTSIDE IT (drop 0807v). A ground wave can
       only fire between reaching LAND (scroll 1416, ~t=35s at 40px/s) and the halfway cutoff
       (scroll 2144, ~t=54s). My first cut placed them at 38, 49 and 58.5 — the last was past the
       cutoff and could never fire, and the deferral on the other two pushed them late enough that
       the miniboss took the scroll first. Four assertions caught it, and non-deterministically,
       which is the tell that it was riding a margin.

       All three now sit early in the window with room to defer. */
    add(36.0, _s1Ground(()=>{ for(let i=0;i<3;i++)
                      spawnEnemy('jungletank', VW*(0.20+i*0.30), -34 - i*62, {_order:i}); }));
    /* ⚠ NO AIR WAVE BETWEEN THE GROUND ONES (drop 0807v). _s1Ground DEFERS by decrementing
       waveIdx, so a ground wave that is not yet on land re-queues itself — and anything sitting
       between two ground waves gets pushed along with it. Interleaving them made the whole
       sequence non-deterministic: three runs of the suite gave three different results. The
       three ground waves are consecutive now, so a defer can only delay them, never reorder
       the level around them. */
    add(43.0, ()=>{ for(let i=0;i<4;i++)
                      spawnEnemy('racer', VW*(0.14+i*0.24), -30 - i*34, {_fast:2.3, fk:'gun'}); });
    add(38.0, _s1Ground(()=>{ spawnEnemy('sandtank', VW*0.26, -30, {});
                              spawnEnemy('sandtank', VW*0.74, -58, {}); }));
    add(54.0, ()=>{ spawnEnemy('topgun', VW*0.30, -32, {fk:'gun'});
                    spawnEnemy('topgun', VW*0.70, -32, {fk:'gun'}); });

    /* ---- 56-78s: MIXED. Air and ground together — both halves at once. ---- */
    add(40.0, _s1Ground(()=>{ for(let i=0;i<3;i++)
                      spawnEnemy('sandtank', VW*(0.18+i*0.32), -30 - i*46, {}); }));
    add(62.0, ()=>{ spawnEnemy('intcp', -28, VH*0.38, {}); spawnEnemy('intcp', VW+28, VH*0.44, {}); });
    add(67.0, ()=>{ for(let i=0;i<4;i++)
                      spawnEnemy('topgun', VW*(0.16+i*0.23), -32 - i*46, {fk:'gun'}); });
    add(72.0, ()=>{ spawnEnemy('racer', VW*0.20, -30, {_fast:2.6, fk:'gun'});
                    spawnEnemy('racer', VW*0.50, -46, {_fast:2.6, fk:'gun'});
                    spawnEnemy('racer', VW*0.80, -30, {_fast:2.6, fk:'gun'}); });

    /* ---- 78-90s: THE RUN-IN. Densest wave of the level, then a beat of quiet before the
           miniboss so its arrival lands. ---- */
    add(78.0, ()=>{ for(let i=0;i<3;i++)
                      spawnEnemy('topgun', VW*(0.26+i*0.24), -32 - i*40, {fk:'gun'}); });
    add(81.5, ()=>{ spawnEnemy('intcp', -28, VH*0.36, {}); spawnEnemy('intcp', -28, VH*0.50, {});
                    spawnEnemy('intcp', VW+28, VH*0.43, {}); });
    add(85.0, ()=>{ for(let i=0;i<4;i++)
                      spawnEnemy('racer', VW*(0.12+i*0.25), -30 - i*30, {_fast:2.5, fk:'gun'}); });
    /* deliberate gap 88-93s: the miniboss should arrive into silence */
    }