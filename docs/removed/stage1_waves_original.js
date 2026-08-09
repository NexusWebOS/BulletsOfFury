if(stageNum===1){
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

    /* --- the opening pass: two jets tear by, one down each side --- */
    add(2.0, ()=>{ spawnEnemy('racer', VW*0.17, -30, {_fast:2.5, _noFire:true});
                   spawnEnemy('racer', VW*0.83, -30, {_fast:2.5, _noFire:true}); });
    /* --- and back over the top, down the outside edges, now shooting --- */
    add(6.0, ()=>{ spawnEnemy('racer', VW*0.09, -30, {fk:'gun'});
                   spawnEnemy('racer', VW*0.91, -30, {fk:'gun'}); });
    add(8.2, ()=>{ spawnEnemy('racer', VW*0.20, -30, {fk:'gun'});
                   spawnEnemy('racer', VW*0.80, -30, {fk:'gun'}); });

    /* --- the beach: four heavy tanks, each set back further, firing in turn ---
       TIMED TO THE ACTUAL COASTLINE (drop 0801jw). Mike: "no tanks were shown or
       visible." They were spawning at t=13, which is mapScroll ~520 - still out
       over the SEA, where the coastline rule at line 3843 correctly swaps any
       ground unit for a stationship or gunboat. That is why he saw ships instead
       of tanks.

       The coast sits at scroll 1416 (camY 3384 on a 4800 master) and the stage
       advances 40px/s, so land begins at t=35. The beach wave now lands just after
       that, and the air waves fill the run out to it. */
    add(36.0, _s1Ground(()=>{ for(let i=0;i<4;i++)
      spawnEnemy('jungletank', VW*(0.15+i*0.235), -34 - i*58, {_order:i}); }));

    /* --- grass jets: in off the very edge, turn inward, then hunt --- */
    add(21.0, ()=>{ spawnEnemy('intcp', -28, 96, {}); spawnEnemy('intcp', -28, 150, {}); });
    add(24.0, ()=>{ spawnEnemy('intcp', VW+28, 96, {}); spawnEnemy('intcp', VW+28, 150, {}); });

    /* --- the diagonal file: four from the top left, moderate speed --- */
    add(30.0, ()=>{ for(let i=0;i<4;i++)
      /* NO HOMING ON THE DIAGONAL (drop 0801kf). Mike: "I got bullet shells homing
         at me". Every other lane was given 'missile', which is a lock-on. The file
         is a strafing pass - guns. */
      spawnEnemy('topgun', VW*0.08+i*12, -32 - i*68, {fk:'gun'}); });

    /* --- sand sections: the little tanks --- */
    add(44.0, _s1Ground(()=>{ spawnEnemy('sandtank', VW*0.24, -30, {});
                              spawnEnemy('sandtank', VW*0.72, -60, {}); }));
    add(50.0, _s1Ground(()=>{ for(let i=0;i<3;i++)
      spawnEnemy('sandtank', VW*(0.18+i*0.30), -30 - i*44, {}); }));

    /* --- one more air wave before the gate --- */
    add(47.0, ()=>{ spawnEnemy('racer', VW*0.30, -30, {fk:'gun'});
                    spawnEnemy('racer', VW*0.70, -30, {fk:'gun'}); });

    /* ---- MINI BOSS lands here, driven by SUBBOSS[1] at 0.45 scroll ---- */

    /* --- after the miniboss: air only, no ground past halfway --- */
    add(58.0, ()=>{ for(let i=0;i<4;i++)
      spawnEnemy('topgun', VW*0.10+i*14, -32 - i*62, {fk:'gun'}); });
    add(64.0, ()=>{ spawnEnemy('intcp', -28, 110, {}); spawnEnemy('intcp', VW+28, 140, {}); });
    add(69.0, ()=>{ spawnEnemy('racer', VW*0.14, -30, {fk:'gun'});
                    spawnEnemy('racer', VW*0.86, -30, {fk:'gun'}); });
    add(75.0, ()=>{ for(let i=0;i<3;i++)
      spawnEnemy('intcp', VW*(0.22+i*0.28), -34 - i*50, {fk:'gun'}); });
    add(81.0, ()=>{ spawnEnemy('topgun', VW*0.20, -30, {fk:'gun'});
                    spawnEnemy('topgun', VW*0.50, -60, {fk:'gun'});
                    spawnEnemy('topgun', VW*0.80, -30, {fk:'gun'}); });
    /* ---- then the helicopter, and the level ends ---- */
  }