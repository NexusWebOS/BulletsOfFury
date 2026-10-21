/* ============================================================
   DEBUG TOOLKIT (1021) - Mike: "can you improve and upgrade my boss mode and debug modes please?"

   Loaded LAST. Owns the in-fight test tools for the title-code DEBUG mode and for Boss Mode's
   engine (index.html?bossmode=1), and the fight telemetry both of them show.

     F8        debug HUD (fight clock, boss HP, phase, DPS, hits, deaths, entity counts, FPS)
     F9        GOD mode - playerHit refuses every hit. NOT a pinned invuln: the damage blink is
               Math.floor(invuln/4)%2, so a pinned timer hides the ship half the time (0912a/0913a)
     F10       restart the current debug fight from its own entry, same pilot and difficulty
     [  /  ]   freeze the combat clock / step ONE 60 Hz tick while frozen
     -  /  =   slow down / speed up the combat clock (0.10x .. 2.00x),  0 = 1.00x
     1 2 3 4   boss HP to 75 / 50 / 25 / 5 %  (phase jumps)
     5         kill the boss (the death BRANCH, via BOSSMODE.kill - barriers absorb a hit)
     6         current weapon to level V

   ⚠ WHY SPEED IS A SCALE ON combatFrame AND NOT `timeScale`. updatePlay resets timeScale to 1 on
   every frame unless Freezer's special is live (`if(timeScale<1 && !specialActive('freezer')...)`),
   so BOSSMODE.setTimeScale - the editor's SPEED slider - was undone the frame after it was set and
   the slider never did anything. And timeScale<1 only ever meant "skip odd frames", a fixed half
   speed. Scaling the dt handed to the fixed 60 Hz clock (maneuver_safety_1007.js) runs exactly
   speed x 60 real ticks a second, deterministically, and leaves every gameplay rule untouched.

   ⚠ A RUN THAT USED ANY ASSIST (god, speed != 1, freeze, HP jump, kill, weapon grant) IS RECORDED
   BUT NEVER SETS A BEST TIME. Best times are the balance instrument; an assisted clear in them would
   make the number lie.
   ============================================================ */
(function(){
  'use strict';
  const BEST_KEY='bof_debug_best_v1', LAST_KEY='bof_debug_last_v1', PREF_KEY='bof_debug_tools_v1';
  const SPEEDS=[0.10,0.25,0.50,0.75,1.00,1.50,2.00];
  const DT=window.DBGT={
    hud:false, god:false, speed:1, frozen:false, step:0, fps:60, _last:0,
    stats:null,              // the live fight's telemetry
    last:null,               // the last finished fight
    best:{},                 // 'stage:role:diff' -> {t, pilot, deaths, hits, at}
    entry:null, entryOpts:null
  };
  function load(){
    try{ DT.best=JSON.parse(localStorage.getItem(BEST_KEY)||'{}')||{}; }catch(_){ DT.best={}; }
    try{ DT.last=JSON.parse(localStorage.getItem(LAST_KEY)||'null'); }catch(_){ DT.last=null; }
    try{ const p=JSON.parse(localStorage.getItem(PREF_KEY)||'{}')||{}; DT.hud=!!p.hud; DT.god=!!p.god; }catch(_){}
  }
  function savePrefs(){ try{ localStorage.setItem(PREF_KEY, JSON.stringify({hud:DT.hud, god:DT.god})); }catch(_){} }
  load();

  /* the tools answer only where debug is armed: the title code, ?debug=1, or the Boss Mode host */
  function armed(){ return (typeof debugUnlocked!=='undefined' && debugUnlocked) || (typeof _bmHost!=='undefined' && _bmHost); }
  function inFight(){ return typeof state!=='undefined' && (state===GS.PLAY || state==='paused'); }
  function liveBoss(){
    if(typeof bossActive!=='undefined' && bossActive && boss && !boss.dead) return boss;
    if(typeof subBossActive!=='undefined' && subBossActive && subBoss && !subBoss.dead) return subBoss;
    return null;
  }
  function assist(why){ if(DT.stats){ DT.stats.assisted=true; DT.stats.assists[why]=1; } }
  function say(t, col){ try{ floatText(VW/2, 150, t, col||'#8de23a'); }catch(_){} }
  function fmtT(t){ if(!(t>=0)) return '--:--'; const m=Math.floor(t/60), s=t-m*60; return m+':'+(s<10?'0':'')+s.toFixed(1); }
  function bestKey(stage, role, diff){ return stage+':'+role+':'+(diff||diffKey); }
  window.debugBestLabel=function(stage, role){ const B=DT.best[bestKey(stage, role)]; return B?fmtT(B.t):''; };

  /* ---- GOD: refuse the hit at its one funnel ---------------------------------------------- */
  const _playerHit=playerHit;
  playerHit=function(source){
    if(DT.god && armed() && source!=='fusionOvercharge'){ if(DT.stats) DT.stats.godBlocks++; return; }
    return _playerHit.apply(this, arguments);
  };

  /* ---- SPEED / FREEZE / STEP: scale the fixed combat clock -------------------------------- */
  const _combatFrame=combatFrame;
  combatFrame=function(dt){
    if(!armed()) return _combatFrame(dt);
    /* ⚠ READ THE HOTKEYS BEFORE THE CLOCK RUNS: a frame that runs two ticks (2.00x, or any
       display slower than 60 Hz) calls Input.clearTaps() between them, so a key read after the
       clock - in debugLoopTick - was eaten on exactly the frames the speed tools create. */
    if(hotkeys()) return 0;
    if(DT.frozen && state===GS.PLAY){
      if(DT.step>0){ DT.step--; BOF_COMBAT_CLOCK.debt=0; const n=_combatFrame(1/60); tally(n); return n; }
      if(typeof combatClockReset==='function') combatClockReset();
      return 0;
    }
    const n=_combatFrame(dt*DT.speed); tally(n); return n;
  };
  function tally(steps){
    const S=DT.stats; if(!S || !steps || typeof debugFight==='undefined' || !debugFight) return;
    if(!S.killedAt && debugFight.spawned) S.t+=steps/60;   // the clock starts when the boss is on the field, not at the warning
  }

  /* ---- telemetry ------------------------------------------------------------------------- */
  function newStats(entry){
    return {stage:entry.stage, role:entry.role, kind:entry.kind, name:entry.name, diff:diffKey,
      pilot:(PILOTS[pilotIndex]||{}).key||'', t:0, dealt:0, win:[], lastHp:null, hits:0, hits0:null,
      deaths:0, wasDead:false, killedAt:0, peakEB:0, godBlocks:0, assisted:DT.god||DT.speed!==1, assists:{}, done:false};
  }
  function sample(){
    const S=DT.stats; if(!S || S.done || typeof debugFight==='undefined' || !debugFight) return;
    if(DT.god) assist('god'); if(DT.speed!==1) assist('speed'); if(DT.frozen) assist('freeze');
    const b=liveBoss();
    if(!b && S.ref && S.ref.dead && S.lastHp>0){ S.dealt+=S.lastHp; S.win.push([S.t, S.lastHp]); S.lastHp=0; }   // the killing blow lands on the frame the unit stops being live
    if(b) S.ref=b;
    if(b && b.maxhp){
      if(S.lastHp!=null && b.hp<S.lastHp){ const d=S.lastHp-b.hp; S.dealt+=d; S.win.push([S.t, d]); }
      S.lastHp=b.hp; S.maxhp=b.maxhp;
    }
    while(S.win.length && S.t-S.win[0][0]>3) S.win.shift();
    if(typeof stageStats!=='undefined' && stageStats){ const h=stageStats.dmgTaken|0; if(S.hits0==null) S.hits0=h; S.hits=Math.max(0, h-S.hits0); }
    const dead=!!(player && player.dead); if(dead && !S.wasDead) S.deaths++; S.wasDead=dead;
    S.peakEB=Math.max(S.peakEB, eBullets.length);
    if(!S.killedAt && typeof bossDefeated!=='undefined' && bossDefeated && debugFight.spawned) S.killedAt=S.t||0.0001;
    if(!S.killedAt && S.role==='mini' && debugFight.spawned && typeof subBoss!=='undefined' && subBoss && subBoss.dead) S.killedAt=S.t||0.0001;   // the kill, not the end of the death reel
  }
  function dps(){ const S=DT.stats; if(!S || !S.win.length) return 0; let d=0; for(const w of S.win) d+=w[1]; return d/Math.max(0.5, Math.min(3, S.t-S.win[0][0]+1/60)); }
  function finish(won){
    const S=DT.stats; if(!S || S.done) return; S.done=true;
    const R={stage:S.stage, role:S.role, kind:S.kind, name:S.name, diff:S.diff, pilot:S.pilot, won:!!won,
      t:won?(S.killedAt||S.t):S.t, deaths:S.deaths, hits:S.hits, dealt:Math.round(S.dealt), assisted:!!S.assisted,
      assists:Object.keys(S.assists), peakEB:S.peakEB, at:Date.now(), newBest:false};
    if(won && !R.assisted){
      const k=bestKey(R.stage, R.role, R.diff), B=DT.best[k];
      if(!B || R.t<B.t){ DT.best[k]={t:R.t, pilot:R.pilot, deaths:R.deaths, hits:R.hits, at:R.at}; R.newBest=true;
        try{ localStorage.setItem(BEST_KEY, JSON.stringify(DT.best)); }catch(_){} }
    }
    DT.last=R; try{ localStorage.setItem(LAST_KEY, JSON.stringify(R)); }catch(_){}
    try{ if(window.parent && window.parent!==window && typeof window.parent.BOSSMODE_ONRESULT==='function') window.parent.BOSSMODE_ONRESULT(R); }catch(_){}
  }

  /* the fight boundaries: a start resets the clock and remembers the entry for F10 */
  const _start=debugStartFight;
  debugStartFight=function(entry, opts){
    if(DT.stats && !DT.stats.done) finish(false);
    DT.entry=entry; DT.entryOpts=Object.assign({}, opts||{}, {record:false});
    DT.frozen=false; DT.step=0;
    const ok=_start.apply(this, arguments);
    if(ok) DT.stats=newStats(entry);
    return ok;
  };
  /* every exit of a debug fight goes through debugRouteState (0910a) - finish there */
  const _route=debugRouteState;
  debugRouteState=function(s){
    if(typeof debugFight!=='undefined' && debugFight && DT.stats && !DT.stats.done && typeof _DBG_EXITS!=='undefined' && _DBG_EXITS[s] && s!==GS.FLYOVER)
      finish(!!DT.stats.killedAt);
    return _route.apply(this, arguments);
  };
  function restart(){
    if(!DT.entry) return false;
    if(DT.stats && !DT.stats.done) finish(false);
    try{ debugRecStop(); }catch(_){}
    try{ Audio.stopMusic(); }catch(_){}
    boss=null; subBoss=null; bossActive=false; subBossActive=false; bossDefeated=false; stageEnding=0;
    enemies.length=0; eBullets.length=0; pBullets.length=0; explosions.length=0; particles.length=0;
    shake=0; whiteBlast=0; timeScale=1;
    return debugStartFight(DT.entry, DT.entryOpts);
  }
  function setHpFrac(f){
    const b=liveBoss(); if(!b || !b.maxhp) return false;
    b.hp=Math.max(1, Math.round(b.maxhp*f)); assist('hp');
    if(DT.stats) DT.stats.lastHp=b.hp;                // a jump is not damage dealt
    return true;
  }
  function kill(){ assist('kill'); try{ return window.BOSSMODE.kill(); }catch(_){ return false; } }
  function maxWeapon(){
    if(typeof run==='undefined' || run.weapon==null) return false;
    run.wlevel=5; if(run.wlevels) run.wlevels[run.weapon|0]=5; assist('weapon'); say('WEAPON LV V','#9fe4ff'); return true;
  }
  function setSpeed(v){ DT.speed=Math.max(0.1, Math.min(2, +v||1)); }
  function stepSpeed(d){ let i=SPEEDS.findIndex(function(s){ return Math.abs(s-DT.speed)<1e-6; }); if(i<0) i=4; i=Math.max(0, Math.min(SPEEDS.length-1, i+d)); setSpeed(SPEEDS[i]); say('SPEED '+DT.speed.toFixed(2)+'x','#4aa8ff'); }

  /* ---- hotkeys, from the debug switchboard ----------------------------------------------- */
  const _tick=debugLoopTick;
  debugLoopTick=function(dt){
    _tick.apply(this, arguments);
    const now=performance.now(); if(DT._last){ const f=1000/Math.max(1, now-DT._last); DT.fps=DT.fps*0.92+f*0.08; } DT._last=now;
    if(!armed()) return;
    sample();
    if(state==='paused') hotkeys();          // PLAY reads them at the top of combatFrame
  };
  /* returns true when the frame was spent on a restart */
  function hotkeys(){
    if(!inFight()) return false;
    const T=function(k){ return Input.tap(k); };
    if(T('f8')){ DT.hud=!DT.hud; savePrefs(); }
    if(T('f9')){ DT.god=!DT.god; savePrefs(); if(DT.god){ player.invuln=0; assist('god'); } say('GOD '+(DT.god?'ON':'OFF'), DT.god?'#ffd25a':'#8a919c'); }
    if(T('f10') && DT.entry){ say('RESTART'); restart(); return true; }
    if(T('[')){ DT.frozen=!DT.frozen; DT.step=0; if(DT.frozen) assist('freeze'); say(DT.frozen?'FROZEN  ] = STEP':'RUNNING','#4aa8ff'); }
    if(T(']') && DT.frozen) DT.step++;
    if(T('-')) stepSpeed(-1);
    if(T('=')) stepSpeed(+1);
    if(T('0')){ setSpeed(1); say('SPEED 1.00x','#4aa8ff'); }
    const F={'1':0.75,'2':0.50,'3':0.25,'4':0.05};
    for(const k in F) if(T(k) && setHpFrac(F[k])) say('BOSS HP '+Math.round(F[k]*100)+'%','#ff8a7a');
    if(T('5') && kill()) say('KILL','#ff3a3a');
    if(T('6')) maxWeapon();
    return false;
  }
  /* F8-F10 belong to the browser otherwise (F10 focuses the Windows menu bar) */
  window.addEventListener('keydown', function(e){
    if(!armed()) return; const k=(e.key||'').toLowerCase();
    if(k==='f8'||k==='f9'||k==='f10') try{ e.preventDefault(); }catch(_){}
  }, true);

  /* ---- the HUD ---------------------------------------------------------------------------- */
  function hudText(){
    const S=DT.stats, b=liveBoss(), L=[];
    if(S) L.push('S'+S.stage+' '+(S.role==='boss'?'BOSS':'MINI')+'  '+String(S.name||'').slice(0,22)+'  ['+String(S.diff).toUpperCase()+']');
    else L.push('STAGE '+(run&&run.stage||'?')+'  ['+String(diffKey).toUpperCase()+']');
    if(S) L.push('TIME '+fmtT(S.killedAt||S.t)+(S.killedAt?'  KILLED':'')+'   DPS '+dps().toFixed(1)+'   DEALT '+Math.round(S.dealt));
    if(b) L.push('HP '+Math.ceil(b.hp)+'/'+b.maxhp+' ('+Math.round(100*b.hp/b.maxhp)+'%)  PAT '+String(b._pat||b.pat||b.phase||'-').slice(0,14));
    if(S) L.push('HITS '+S.hits+'  DEATHS '+S.deaths+'  LIVES '+(run.lives|0)+(DT.god?'  GOD x'+S.godBlocks:''));
    L.push('EN '+enemies.length+'  EB '+eBullets.length+(S?' (PK '+S.peakEB+')':'')+'  PB '+pBullets.length+'  FX '+particles.length);
    L.push('SPEED '+DT.speed.toFixed(2)+'x'+(DT.frozen?'  FROZEN':'')+'   FPS '+Math.round(DT.fps)+(S&&S.assisted?'   ASSISTED':''));
    return L;
  }
  function drawHud(){
    if(!armed() || !inFight()) return;
    ctx.save(); ctx.setTransform(SS,0,0,SS,0,0); ctx.textAlign='left'; ctx.textBaseline='top';
    if(DT.hud){
      const L=hudText(), x=6, y=86, lh=11, w=278, h=L.length*lh+31;
      ctx.fillStyle='rgba(6,10,14,0.72)'; ctx.fillRect(x,y,w,h);
      ctx.strokeStyle='#8de23a'; ctx.lineWidth=1; ctx.strokeRect(x+0.5,y+0.5,w-1,h-1);
      ctx.font='bold 9px monospace';
      L.forEach(function(s,i){ ctx.fillStyle=i===0?'#e6ffd0':'#cfd6e0'; ctx.fillText(s, x+5, y+4+i*lh); });
      const b=liveBoss();
      if(b && b.maxhp){ const by=y+h-23; ctx.fillStyle='#2a2d33'; ctx.fillRect(x+5,by,w-10,5);
        ctx.fillStyle=b.hp/b.maxhp>0.5?'#5ad65a':(b.hp/b.maxhp>0.25?'#ffc23a':'#ff4a3a'); ctx.fillRect(x+5,by,(w-10)*Math.max(0,b.hp/b.maxhp),5);
        ctx.fillStyle='#ffffff'; for(const q of [0.75,0.5,0.25]) ctx.fillRect(x+5+(w-10)*q, by-1, 1, 7); }
      ctx.fillStyle='#8a99a8'; ctx.font='8px monospace';
      ctx.fillText('F9 GOD F10 RESET [ ] FRZ/STEP -= SPD 1-4 HP 5 KILL 6 WPN', x+5, y+h-12);
    } else if(DT.god || DT.speed!==1 || DT.frozen){
      const tag=(DT.god?'GOD ':'')+(DT.speed!==1?DT.speed.toFixed(2)+'x ':'')+(DT.frozen?'FROZEN':'');
      ctx.font='bold 9px monospace'; ctx.textAlign='right'; ctx.fillStyle='rgba(6,10,14,0.7)';
      const tw=ctx.measureText(tag).width+8; ctx.fillRect(VW-6-tw, 86, tw, 13);
      ctx.fillStyle='#ffd25a'; ctx.fillText(tag, VW-10, 88);
    }
    ctx.restore();
  }
  const _clocks=drawEncounterClocks;
  drawEncounterClocks=function(){ const r=_clocks.apply(this, arguments); try{ drawHud(); }catch(_){} return r; };

  /* ---- the debug menu's extra lines (called from drawDebugMenu) --------------------------- */
  window.dbgToolsMenuDraw=function(){
    ctx.save(); ctx.textAlign='center'; ctx.textBaseline='alphabetic'; ctx.font='bold 9px "BOFmil", monospace';
    const R=DT.last;
    if(R){
      ctx.fillStyle=R.won?(R.newBest?'#ffd25a':'#8de23a'):'#ff8a7a';
      let s='LAST: S'+R.stage+' '+(R.role==='boss'?'BOSS':'MINI')+' '+String(R.name).slice(0,20)+'  '+(R.won?'WIN ':'LOST ')+fmtT(R.t)+
        '  DEATHS '+R.deaths+'  HITS '+R.hits+(R.newBest?'  NEW BEST':'')+(R.assisted?'  (ASSISTED)':'');
      ctx.fillText(s, VW/2, 396);
    }
    ctx.fillStyle='#8a919c'; ctx.font='9px "BOFmil", monospace';
    ctx.fillText('IN FIGHT: F8 HUD '+(DT.hud?'ON':'OFF')+'   F9 GOD '+(DT.god?'ON':'OFF')+'   F10 RESTART   1-4 HP   [ ] FREEZE / STEP', VW/2, 410);
    ctx.restore();
    if(Input.tap('f8')){ DT.hud=!DT.hud; savePrefs(); }
    if(Input.tap('f9')){ DT.god=!DT.god; savePrefs(); }
  };

  /* ---- the Boss Mode surface -------------------------------------------------------------- */
  const BM=window.BOSSMODE;
  if(BM){
    /* INVULN was player.invuln=1e9, which blinks the ship (the damage blink reads that timer) */
    BM.setInvuln=function(v){ DT.god=!!v; if(v && player) player.invuln=0; };
    BM.setTimeScale=function(v){ setSpeed(v); };
    BM.tools={
      get god(){ return DT.god; }, set god(v){ DT.god=!!v; },
      get speed(){ return DT.speed; }, setSpeed:setSpeed,
      get ticks(){ return BOF_COMBAT_CLOCK.total; },   // the fixed clock's count; the const is not on window
      get frozen(){ return DT.frozen; }, freeze:function(on){ DT.frozen=!!on; DT.step=0; }, step:function(n){ DT.step+=Math.max(1,n|0); },
      get hud(){ return DT.hud; }, setHud:function(on){ DT.hud=!!on; savePrefs(); },
      restart:restart, setHpFrac:setHpFrac, kill:kill, maxWeapon:maxWeapon,
      stats:function(){ const S=DT.stats; if(!S) return null; return {stage:S.stage, role:S.role, kind:S.kind, name:S.name, diff:S.diff, pilot:S.pilot,
        t:S.killedAt||S.t, killed:!!S.killedAt, dps:dps(), dealt:S.dealt, hits:S.hits, deaths:S.deaths, peakEB:S.peakEB, godBlocks:S.godBlocks,
        assisted:!!S.assisted, done:S.done, best:DT.best[bestKey(S.stage,S.role,S.diff)]||null}; },
      last:function(){ return DT.last; }, best:function(){ return DT.best; },
      clearBest:function(){ DT.best={}; try{ localStorage.removeItem(BEST_KEY); }catch(_){} }
    };
  }
})();
