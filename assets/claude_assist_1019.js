"use strict";
/* 1019 - Claude Code, working beside Codex's overnight combat pass (docs/OVERNIGHT_COMBAT_1019.md, items 7/8/6/4).
   A late layer: it wraps existing owners and never edits game.js, so the one-game.js-writer rule holds. */
const CA19={base:{cad:_weaponCadence}};
function ca19Off(){return typeof window!=='undefined'&&window.CA19_OFF===1;}

/* ---- item 7: Lizzie's heavy MG is slow in space ------------------------------------------------------------
   Mike: "lizzie's machine gun is slow in space for some reason when she gets the special."
   Measured (probe_lizzie_space_mg_1019.py): docked heavy MG 24 rounds/s on stage 1, 9/s on stage 5. _weaponCadence
   returns the SPACE weapon's 0.24-0.36 s beat before it ever reaches the docked-mount check, while pShoot still
   hands the trigger to the mount - so in space she fired mount slugs at the space laser's cadence, a quarter of
   the mount's own rate (and well below the 54/s laser it displaces). The mount owns the trigger wherever it is
   docked, so it owns the cadence too. */
_weaponCadence=function(){
 if(!ca19Off()&&typeof lzMountActive==='function'&&lzMountActive()&&typeof LZ_SLUG_CD!=='undefined')return LZ_SLUG_CD;
 return CA19.base.cad.apply(this,arguments);
};

/* ---- item 8: Spread Fire's muzzle flash is centred on every ship -----------------------------------------
   Mike: "Spread fire, fix and center the muzzle flash on all ships."
   Measured (probe_spread_muzzle_1019.py): on all nine pilots the flash's visible ink sat 2.0-2.4 px RIGHT of the
   nose's ink. wm26PlayerNose() already finds the nose from the hull frame's own pixels and then adds a flat +2 -
   so every flash, and every nose-launched machine-gun row that uses the same point, was 2 px off on every ship.
   The +2 is taken back out here; the pixel anchor stays the game's. */
CA19.base.nose=wm26PlayerNose;
wm26PlayerNose=function(){
 const p=CA19.base.nose.apply(this,arguments);
 return ca19Off()||!p?p:{...p,x:p.x-2};
};

/* ---- item 6: Stage 5 "enemies dont shoot" -----------------------------------------------------------------
   Mike: "Level 5, enemies dont shoot and have the same problem before we adjusted enemy AI."
   Measured (probe_stage5_fire_1019.py): with nobody firing back, every Stage-5 gunship DOES fire - first shot
   1.2-2.5 s after it appears, at rates comparable to Stages 4 and 6. With the player holding the real space laser,
   21 of 24 units died WITHOUT EVER SHOOTING, and the station, gravity well, satellite, minelayer and rammers died
   with ZERO frames on screen. spaceBulletHit tests every target with no visibility gate, and a space-laser round
   lives until y < -50, so the 54-rounds/s laser was killing the wave in the spawn margin above the screen before
   it entered. Stage 4's ground guns, measured the same way, kill nothing off screen.
   A space round now only hits an ordinary enemy once its centre is on screen (a big hull's edge poking in
   does not count - the first cut allowed that and still lost the station at y -83). Bosses, minibosses, their
   pieces and Stage-5 rocks keep their own rules. Locks/homing still see every target (only the hit test is gated). */
CA19.base.spaceHit=spaceBulletHit; CA19.base.spaceTargets=spaceTargets; CA19.inHit=0;
function ca19InView(t){
 if(!t||t===boss||t===subBoss||t._retinaOwner||t._spaceBossOwner||t._l5Rock)return true;
 if(typeof enemies==='undefined'||enemies.indexOf(t)<0)return true;
 const th=(t._drawH||t.h||28),tw=(t._drawW||t.w||28),ty=(typeof spaceTargetY==='function'?spaceTargetY(t):t.y);
 const cx=(typeof worldWidth==='function'&&typeof viewW==='function'&&worldWidth()>viewW()&&typeof camX!=='undefined')?camX:0,sx=t.x-cx;
 return ty>2&&ty<VH&&sx>0&&sx<VW;   // its centre is on screen - a sliver of a large hull poking in is not 'arrived'
}
spaceTargets=function(){const a=CA19.base.spaceTargets.apply(this,arguments);return CA19.inHit&&!ca19Off()?a.filter(ca19InView):a;};
spaceBulletHit=function(){CA19.inHit++;try{return CA19.base.spaceHit.apply(this,arguments);}finally{CA19.inHit--;}};
/* ...and the deeper half of the same complaint: every Stage-5 hull spawned with 12 HP. Their authored rows in
   S5SPACE run 28 (repair drone) to 120 (twin station), but spawnEnemy passes them through EHP() - the FODDER
   shots-to-kill model, which caps whatever it is handed (the same trap CLAUDE.md records for the elites). So the
   station, the minelayer and a scout all died to one level-1 laser beat (~0.1 s) while their first volley is
   authored 1-2 s after arrival. The authored value is restored as the NORMAL pool; whatever ratio EHP applies for
   difficulty, stage pressure and co-op is kept on top, so MODE-04's Hard +15% still holds. */
CA19.base.spawn=spawnEnemy;
function ca19S5Hp(e){
 const H=typeof S5SPACE!=='undefined'&&S5SPACE[e._s5space];if(!H||ca19Off())return;
 const cur=EHP(H.hp),saved=diffKey;let nrm=cur;
 try{diffKey='normal';nrm=EHP(H.hp);}finally{diffKey=saved;}
 const hp=Math.max(cur,Math.round(H.hp*cur/Math.max(1,nrm)));
 e.hp=e.maxhp=e._maxhp=hp;e._ca19Hp=1;
}
spawnEnemy=function(){
 const n=enemies.length,r=CA19.base.spawn.apply(this,arguments);
 for(let i=n;i<enemies.length;i++){const e=enemies[i];if(e&&e._s5space&&!e._ca19Hp)ca19S5Hp(e);}
 return r;
};

/* ---- item 4: the Stage-8 Hammer form "doesnt spin properly like our actual hammer boss does" ---------------
   Measured side by side (probe_hammer_compare_1019.py): both run the same hammerBossTick states. The real Stage-5
   Hammer turns its whirlwind on HAMMER_WHIRL_REEL - eight drawings a revolution on h.whirl.reel, which winds up from
   ~10 fps to 20 fps and then accelerates to ~40 fps on later passes (w.reel += dt*(20+pass*7+...)). The Stage-8
   form's f6Motion stepped its four direction poses (front/right/back/left) on a flat t*9 clock - same average
   revolution, no wind-up, no acceleration, and half the drawings - so it read as stepping, not spinning.
   Its four poses now ride the SAME reel clock as the Stage-5 boss (reel/2, four poses a revolution), so the spin
   winds up and accelerates exactly when the real Hammer's does. The ball's roll was measured too: it already turns
   at the same ~570 deg/s as the Stage-5 spiked ball; it only LOOKS still because its authored ball art is almost
   radially symmetric (round pods around a centred eye) - that needs an authored rolling reel, not code. */
CA19.base.f6=typeof f6Motion==='function'?f6Motion:null;
if(CA19.base.f6)f6Motion=function(h){
 const f=CA19.base.f6.apply(this,arguments);
 if(ca19Off()||!h||f==null||f<8||f>11)return f;
 const s=h.state;
 if(s==='whirlwind'&&h.whirl&&Number.isFinite(h.whirl.reel))return 8+(Math.floor(h.whirl.reel/2)%4);
 if(s==='spin'||s==='fr_twirl'){const t=h.t||0;return 8+(Math.floor(t*9+Math.min(t,1.6)*t*7)%4);}   // wind-up: 9 fps rising, like a twirl gathering speed
 return f;
};
