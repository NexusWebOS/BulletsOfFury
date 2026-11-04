"use strict";
/* ============================================================
   DIFFICULTY ASSIST (drop 1103) — DA13. Loaded last. window.DA13_OFF=1 disables it.

   Mike asked for the waves to be tuned "for hard and normal so we don't overwhelm the underskilled
   players" after the wave pressure audit (docs/WAVE_AUDIT_1103.md). Measured on the real engine with
   a novice pilot, Normal lost 5.1 lives/min on Stage 2 (firewalls and fire debris, not bullets) and
   1.8 on Stage 7 (6 rounds/s); Furious rounds reach 670 px/s; Stage 6 guns ignore the speed dial.

   What this layer does, ONLY on Normal and Hard, ONLY during regular waves (never while a boss or
   miniboss is active, whose patterns are tuned by their own owners). Furious, Insanity and Easy are
   untouched.

   1. FIRE BUDGET. Every round born through eShoot/eShootT is counted. When the screen already holds
      the tier's budget (Normal 25 live rounds, Hard 45) or aimed fire exceeds its rolling rate
      (Normal 1.5/s, Hard 2.5/s), the rounds spawned that frame are taken out of eBullets and held
      as one group, then released together a moment later (at most 0.6 s). Nothing is deleted, the
      caller still holds the same object (tags assigned after the call still land), and a ring or
      fan comes back whole because a frame's spawns travel as one group.
   2. SPEED SPLIT. Aimed rounds (born pointing at the pilot) are capped at Normal 260 / Hard 360 px/s,
      pattern rounds at 330 / 420. The cap is applied every frame and scales spd/_maxspd too, so
      homing and accelerating rounds that rebuild velocity from those fields stay capped. This also
      reaches stage guns that bypass DIFF.ebSpeed.
   3. HAZARDS. Stage 2 firewall: falls in 1.7 s (Normal) / 1.45 s (Hard) instead of 1.25, and only
      catches the pilot inside 0.24 / 0.30 of its sprite instead of 0.34. Fire debris: half (Normal)
      or three quarters (Hard) of the chunks launch, the rest are dropped at launch; the pilot is
      only hit inside 65% / 80% of the native radius; each chunk shows its next 0.4 s of path as
      pixel dots. Stage 8 alien beams and flamethrowers hold their locked lane 0.3 s (Normal) / 0.15 s (Hard)
      longer before firing (the lock time itself is unchanged).
      The firewall's arrival alarm stays off, as Mike asked in 0801ad.
   4. MERCY. On Normal the fire budget is halved for 8 s after a respawn, so one mistake does not
      chain into the next.
   ============================================================ */
(function(){
if(window.DA13_OFF)return;
const TIERS={
  normal:{cap:25,aimedRate:1.5,aimed:260,pattern:330,mercy:8,wallTime:1.7,wallBox:.24,debrisDropEvery:2,debrisR:.65,beamBonus:.30},
  hard:  {cap:45,aimedRate:2.5,aimed:360,pattern:420,mercy:0,wallTime:1.45,wallBox:.30,debrisDropEvery:4,debrisR:.80,beamBonus:.15},
};
const MAX_HOLD=.6,AIM_TOL=.14;
const DA={clock:0,on:false,gate:true,frame:0,queue:[],aimed:[],seen:new WeakSet(),mercyUntil:-1,wasDead:false,debrisN:0,
  stat:{held:0,released:0,groups:0,maxWait:0,capped:0,wallRefused:0,debrisDropped:0,debrisRefused:0,beamExtended:0}};
const tier=()=>(typeof diffKey!=='undefined'&&TIERS[diffKey])||null;
function regular(){
  return typeof state!=='undefined'&&state===GS.PLAY&&!bossActive&&!subBossActive&&!(typeof debugFight!=='undefined'&&debugFight);
}
function onScreen(b){return b&&!b.dead&&b.y>PLAY.y-30&&b.y<VH+30;}
function liveCount(){let n=0;for(const b of eBullets)if(onScreen(b))n++;return n;}
function isAimed(b){
  const sp=Math.hypot(b.vx||0,b.vy||0);if(sp<.05||typeof player==='undefined')return false;
  const a1=Math.atan2(b.vy,b.vx),a2=Math.atan2(player.y-b.y,player.x-b.x);let d=Math.abs(a1-a2)%(Math.PI*2);if(d>Math.PI)d=Math.PI*2-d;
  return d<AIM_TOL;
}
function mercyMul(){return DA.clock<DA.mercyUntil?.5:1;}
function gateOpen(T){
  const m=mercyMul();
  while(DA.aimed.length&&DA.clock-DA.aimed[0]>2)DA.aimed.shift();
  return liveCount()<T.cap*m&&DA.aimed.length/2<T.aimedRate*m;
}
function classify(b){
  if(DA.seen.has(b))return;DA.seen.add(b);
  b._da13Aimed=isAimed(b);
}
function noteLive(list){for(const b of list){classify(b);if(b._da13Aimed)DA.aimed.push(DA.clock);}}

/* ---- 1. the fire budget, outermost on both spawn functions ---- */
function wrapSpawn(name){
  const base=globalThis[name];if(typeof base!=='function')return;
  globalThis[name]=function(){
    if(window.DA13_OFF||!DA.on)return base.apply(this,arguments);
    const arr=eBullets,before=arr.length,out=base.apply(this,arguments);
    if(eBullets!==arr||eBullets.length<=before)return out;
    const added=eBullets.slice(before);
    for(const b of added)classify(b);
    if(DA.gate){noteLive(added);return out;}
    /* held: out of the arrays (no update, draw or collision), still the caller's object */
    /* in place: other code may hold this same array this frame, so its identity must not change */
    for(const b of added){const i=eBullets.lastIndexOf(b);if(i>=0)eBullets.splice(i,1);}
    let g=DA.queue[DA.queue.length-1];
    if(!g||g.frame!==DA.frame){g={frame:DA.frame,at:DA.clock,items:[]};DA.queue.push(g);DA.stat.groups++;}
    g.items.push(...added);DA.stat.held+=added.length;
    return out;
  };
}
wrapSpawn('eShoot');wrapSpawn('eShootT');
function release(T,force){
  while(DA.queue.length){
    const g=DA.queue[0],wait=DA.clock-g.at;
    if(!force&&wait<MAX_HOLD&&!(T&&gateOpen(T)))break;
    DA.queue.shift();const back=g.items.filter(b=>b&&!b.dead);
    eBullets.push(...back);noteLive(back);
    DA.stat.released+=g.items.length;DA.stat.maxWait=Math.max(DA.stat.maxWait,+wait.toFixed(3));
    if(!force&&wait<MAX_HOLD)break;          // one group per frame unless overdue
  }
}

/* ---- 2. the speed split ---- */
function capSpeeds(T){
  for(const b of eBullets){
    if(!b||b.dead)continue;classify(b);
    const sp=Math.hypot(b.vx||0,b.vy||0);if(sp<.05)continue;
    const cap=(b._da13Aimed?T.aimed:T.pattern)/60;
    if(sp<=cap*1.02)continue;
    const f=cap/sp;b.vx*=f;b.vy*=f;
    if(typeof b.spd==='number')b.spd*=f;if(typeof b._maxspd==='number')b._maxspd*=f;if(typeof b.speed==='number')b.speed*=f;
    if(!b._da13Capped){b._da13Capped=true;DA.stat.capped++;}
  }
}

/* ---- 3. hazards ---- */
function firewallPace(T,dt){
  if(typeof wfx==='undefined'||!wfx||!wfx.fseq||!wfx.fseq.wave||typeof FIRE_CROSS!=='number')return;
  const W=wfx.fseq.wave,slow=1-FIRE_CROSS/T.wallTime;
  W.y-=(VH+300)/FIRE_CROSS*dt*slow;W.t-=dt*slow;
}
if(typeof debrisLaunch==='function'){
  const baseLaunch=debrisLaunch;
  debrisLaunch=function(){
    const d=baseLaunch.apply(this,arguments),T=tier();
    if(!window.DA13_OFF&&T&&regular()&&d){DA.debrisN++;
      if(DA.debrisN%T.debrisDropEvery===0){d.dead=true;DA.stat.debrisDropped++;}}
    return d;
  };
}
if(typeof playerHit==='function'){
  const baseHit=playerHit;
  playerHit=function(){
    const T=tier();
    if(!window.DA13_OFF&&T&&regular()&&typeof player!=='undefined'&&player){
      const st=String(new Error().stack);
      if(st.indexOf('wfxUpdate')>=0&&typeof wfx!=='undefined'&&wfx&&wfx.fseq&&wfx.fseq.wave){
        const W=wfx.fseq.wave,half=150*(W.sc||1)*T.wallBox;
        if(Math.abs(player.x-W.x)>=half||Math.abs(player.y-W.y)>=half){DA.stat.wallRefused++;return;}
      }else if(st.indexOf('debrisTick')>=0&&typeof fireDebris!=='undefined'){
        let near=null,nd=1e9;for(const d of fireDebris){if(d.delay>0)continue;const q=Math.hypot(player.x-d.x,player.y-d.y);if(q<nd){nd=q;near=d;}}
        if(near&&nd>=(near.r||9)*T.debrisR+8*T.debrisR){DA.stat.debrisRefused++;return;}
      }
    }
    return baseHit.apply(this,arguments);
  };
}
/* Stage 8 beams lock their lanes at half the warning (A.t >= A.warm*.5). Lengthening the warning at
   the start would also delay the lock and let the beam aim later, i.e. better. So the native lock time
   is kept and the bonus is added the moment the lanes commit: the full extra time is dodge time. */
if(typeof s811Tick==='function'){
  const baseTick=s811Tick;
  s811Tick=function(e){
    const r=baseTick.apply(this,arguments),T=tier(),A=e&&e._s811;
    if(!window.DA13_OFF&&T&&regular()&&A&&A.phase==='tell'&&A.committed&&!A._da13&&(/beam/.test(A.attack||'')||A.attack==='flamethrower')){
      A._da13=true;A.warm+=T.beamBonus;DA.stat.beamExtended++;
    }
    if(A&&A.phase!=='tell')A._da13=false;
    return r;
  };
}
/* debris path dots: the next 0.4 s of each chunk's arc, so a random arc is readable */
if(typeof drawEffects==='function'){
  const baseFx=drawEffects;
  drawEffects=function(){
    const r=baseFx.apply(this,arguments),T=tier();
    if(!window.DA13_OFF&&T&&regular()&&typeof fireDebris!=='undefined'&&fireDebris.length&&typeof DEBRIS_G==='number'){
      ctx.save();ctx.globalCompositeOperation='lighter';ctx.imageSmoothingEnabled=false;
      for(const d of fireDebris){if(d.dead||d.delay>0)continue;let x=d.x,y=d.y,vx=d.vx,vy=d.vy;
        for(let k=1;k<=24;k++){vy+=DEBRIS_G;x+=vx;y+=vy;if(k%4)continue;
          ctx.globalAlpha=k<12?.55:.3;ctx.fillStyle=k<12?'#ffd070':'#ff7a1e';ctx.fillRect(Math.round(x)-1,Math.round(y)-1,2,2);}}
      ctx.restore();
    }
    return r;
  };
}

/* ---- the frame: gate, native update, release, caps, hazards, mercy ---- */
const baseUpdate=updatePlay;
updatePlay=function(dt){
  if(window.DA13_OFF)return baseUpdate.apply(this,arguments);
  const T=tier(),step=+dt||0;DA.clock+=step;DA.frame++;
  const was=DA.on;DA.on=!!T&&regular();
  if(was&&!DA.on)release(T,true);                 // a boss arrives: nothing stays held
  DA.gate=DA.on?gateOpen(T):true;
  const out=baseUpdate.apply(this,arguments);
  if(DA.on){
    release(T,false);capSpeeds(T);firewallPace(T,step);
  }
  if(typeof player!=='undefined'&&player){
    if(DA.wasDead&&!player.dead&&T&&T.mercy)DA.mercyUntil=DA.clock+T.mercy;
    DA.wasDead=!!player.dead;
  }
  return out;
};
window.DA13={tiers:TIERS,state:DA,version:'1103'};
})();
