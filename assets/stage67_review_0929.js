"use strict";
/* ============================================================================
   STAGE 6 / 7 REVIEW (Mike, 0929). Loaded after mission_repair_0929.js, so every override below
   replaces the newest owner of that function.

   "stage 6 boss should be modular, the fans especially so they spin and we have something that makes
    sense why beams are coming from there. the enemy jets that come out, not too many. THe enemy boss
    jet that escapes the harrier should be a modular larger blue jet of its own. I like the
    aggressiveness, but hes a little too hard. Stage 7 hazard, still doesnt make sense. Enemies should
    not have trianges on them at all. Stage 7 boss, can be more aggessive on furious ... Stage 6 - The
    bombers dont flash when shot, neither does the level 6 boss ... The bomber jets are to small, too
    underwhelming in the bomb sequence and need to use lizzie's atomic bomb sounds ... When the fighters
    come in, dont show their special ability boxes anymore, just give them the ability at random ...
    Stage 7 ending, still underwhelming and you can barely see him go into the portal. and we should be
    flying fast and the fire not as close to us as we fly away. it still looks like the boss tries to
    scroll with us or explosions scroll with us, dont do that. And we need a better entrance for stage 7."

   Notes that are load-bearing are marked with a warning sign; docs/STAGE67_REVIEW_0929.md has the
   measurements.
   ============================================================================ */

/* ---------------------------------------------------------------------------
   A. NO TRIANGLES ON ENEMIES
   The triangles were two things, both procedural:
   1. drawS4/S6/S7DamageOverlay painted a lineTo() flame triangle (orange on 4/6, green on 7) plus
      canvas-circle smoke on every damaged hull. drawEnemyDamage already vents the AUTHORED smoke and
      fire reels (nsd_diss / nsd_chim / nxp_upward) on every unit from the enemy loop, so those
      overlays were a second, procedural damage system stacked on the real one (0809l warned about
      exactly that). They draw nothing now; the authored reels remain.
   2. The FOV cone - a wedge with its apex on the gun - was still drawn off ordinary enemies (the
      stage 3+ bomber lanes, the stage-8 realm fleet, the stage-6 assault gates). The alert sign was
      already suppressed for them (l23WarnSymbolDraw); the cone was not. Ordinary enemies now get a
      straight lane band in the same green / yellow / red phases. Bosses and minibosses keep the cone
      and the alert frames, which is Mike's approved vocabulary for them.
   --------------------------------------------------------------------------- */
drawS4DamageOverlay=function(){};
drawS6DamageOverlay=function(){};
drawS7DamageOverlay=function(){};
const S67_LANE_COL={green:'#32e891',yellow:'#ffd74b',red:'#ff4840'};
function s67LanePhase(k){return typeof l23FovPhase==='function'?l23FovPhase(k):(k>=2/3?'red':k>=1/3?'yellow':'green');}
/* A straight band from (x,y) toward (ex,ey): fill plus two bright edge rules, pulsing as the release
   nears. Drawn in whatever space the caller is in (world, for every current caller). */
function s67LaneBand(x,y,ex,ey,width,k,alphaMul,len){
  const col=s67LanePhase(k),a=Math.atan2(ey-y,ex-x),L=Number.isFinite(len)&&len>0?len:Math.max(24,Math.hypot(ex-x,ey-y));
  const w=Math.max(8,width||20),pl=.5+.5*Math.sin((typeof efxClock!=='undefined'?efxClock:0)*(8+k*20));
  const base=col==='green'?.13:col==='yellow'?.17+.09*pl:.21+.14*pl,m=alphaMul==null?1:alphaMul;
  ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.fillStyle=S67_LANE_COL[col];
  ctx.globalAlpha=base*m;ctx.fillRect(0,-w/2,L,w);
  ctx.globalAlpha=Math.min(1,(base*2.6)*m);ctx.fillRect(0,-w/2,L,2);ctx.fillRect(0,w/2-2,L,2);
  ctx.restore();
}
const S67_BASE={combatWarningDraw,s6OpeningDraw,missionJetSpawn,missionBomb,furyFleetDraw,groundTargetingDraw,
  drawAtomBooms,updateAtomBooms,s6SupplyTick,warhiveInit,warhiveDamage};
combatWarningDraw=function(owner,q){
  if(owner&&q&&q.progress!=null&&!q.alertOnly&&typeof enemyWarningOwner==='function'&&enemyWarningOwner(owner)){
    s67LaneBand(q.x,q.y,q.ex,q.ey,q.width,clamp(q.progress,0,1),q.alpha==null?1:Math.min(1.4,q.alpha*2.4),q.len);return;}
  return S67_BASE.combatWarningDraw(owner,q);
};

/* ---------------------------------------------------------------------------
   B. STAGE 6 ASSAULT - bigger bombers that flash, and an atomic bomb run
   ⚠ Every jet in the assault is spawned as s1jetbomber_b, the lanes included, so "the bomber jets"
   is the whole squadron. The bluejets cells are 128px authored plates that were being drawn at 72;
   the lane gates now draw at 100 (they still fit their rows) and the bomb run at 128, i.e. native.
   Hit boxes keep the proportions the 0929 lanes were tuned with.
   --------------------------------------------------------------------------- */
const S67_BOMBER_DRAW=128,S67_GATE_DRAW=100;
missionJetSpawn=function(event,O){
  const e=S67_BASE.missionJetSpawn(event,O);if(!e)return e;
  const bomb=event.kind==='bomb',side=event.direction!=='south',s=bomb?S67_BOMBER_DRAW:S67_GATE_DRAW;
  e._s67Draw=s;e.w=Math.round(s*.75);e.h=Math.round(s*(side?.56:.90));
  if(bomb){e.hp=e.maxhp=Math.round(e.hp*1.3);e._s67Bomber=true;}
  return e;
};
/* the whole bluejets sheet tinted once per colour, then the cell rect is cut from it */
function s67CellFlash(name,frame,x,y,w,h,e){
  const A=MISSION29_ART[name];if(!A||!XART.rdy(A.key))return false;
  const c=xartTint(A.key,'#ffffff',1);if(!c)return false;
  const r=A.frames[((frame|0)%A.frames.length+A.frames.length)%A.frames.length];
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=Math.min(1,(e.flash||0)*9);ctx.drawImage(c,...r,x,y,w,h);ctx.restore();return true;
}
furyFleetDraw=function(e){
  const A=e._mission29;if(!A)return S67_BASE.furyFleetDraw(e);if(e.dead||e._dyingT!=null)return true;
  const f={east:0,west:1,south:2}[A.direction],s=e._s67Draw||72;
  if(!missionCell('bluejets',f,e.x-s/2,e.y-s/2,s,s))return S67_BASE.furyFleetDraw(e);
  // ⚠ ENGINE HEADER RULE (0912y): every hit flashes. This draw had no flash branch at all.
  if(e.flash>0)s67CellFlash('bluejets',f,e.x-s/2,e.y-s/2,s,s,e);
  e._drawW=s;e._drawH=s;return true;
};
/* The bomb is Lizzie's: her atom plate falls away from the bomber onto the reticle, her launch cue on
   release and her detonation on impact, with a small mushroom from her own lz_nuke reel. The damage
   circle stays the reticle's - the cloud rises ABOVE it, it does not widen what hurts. */
let s67Nukes=[];
function s67AssaultWarm(){for(const k of ['lz_bomb','lz_nuke_0','lz_nuke_1','lz_nuke_2','lz_nuke_3'])try{XART.rdy(k);}catch(_w){}}
missionBomb=function(e){
  const n=e._mission29.n,T=targetShip(e.x,e.y),limit=[3,5,7][n];
  if(groundTargetingFx.filter(q=>q._mission29&&!q.dead).length>=limit)return;
  const offset=e._mission29.targetOffset;s67AssaultWarm();
  const q=groundTargetingSpawn({kind:'missile',x:clamp(T.x+offset,camLeftX()+42,camRightX()-42),
    y:clamp(T.y+offset*.55,viewTopY()+85,VH-48),owner:e,track:false,lane:false,warn:[1.75,1.6,1.45][n],
    radius:[32,35,38][n],size:104,active:.55,sound:'atomicDetonate',shake:12,onImpact:g=>s67AtomicImpact(g)});
  q._mission29=true;q._jetBomb={x:e.x,y:e.y};q._s67Atom=true;
  (Audio.SFX.atomicLaunch||Audio.SFX.missile||function(){})();
};
function s67AtomicImpact(g){
  s67Nukes.push({x:g.x,y:g.y,t:0,dur:1.45,w:196});
  explode(g.x,g.y,118,'red');
  explode(g.x-30,g.y+10,62,'orange',null,null,null,null,true);explode(g.x+32,g.y+6,56,'orange',null,null,null,null,true);
  if(typeof spawnShockRing==='function'){spawnShockRing(g.x,g.y,170,'fire');spawnShockRing(g.x,g.y,105,'fire');}
  atomFlash=Math.max(atomFlash||0,.38);shake=Math.max(shake,12);
  // cook-offs walking out along the base, the way her own atomBlast breaks the silhouette
  const L=camLeftX()+10,R=camRightX()-10;
  for(let i=0;i<6;i++){const side=i%2?1:-1,step=Math.ceil((i+1)/2);
    g._s67Sec=(g._s67Sec||[]);g._s67Sec.push({x:clamp(g.x+side*(24+step*26),L,R),y:g.y+rnd(-6,14),t:.12+step*.08,r:rnd(18,30)});}
  s67Nukes[s67Nukes.length-1].sec=g._s67Sec;
}
updateAtomBooms=function(dt){
  S67_BASE.updateAtomBooms(dt);
  for(const b of s67Nukes){b.t+=dt;
    if(b.sec)while(b.sec.length&&b.sec[0].t<=b.t){const s=b.sec.shift();explode(s.x,s.y,s.r,'red');shake=Math.max(shake,3+s.r*.08);if(Math.random()<.4)(Audio.SFX.expSmall||function(){})();}}
  s67Nukes=s67Nukes.filter(b=>b.t<b.dur);
};
function s67NukeDraw(){
  for(const b of s67Nukes){
    const p=clamp(b.t/b.dur,0,1),k='lz_nuke_'+clamp(Math.floor(p*4),0,3);if(!XART.rdy(k))continue;
    const im=XART.get(k),w=b.w*(.78+p*.34),h=w*(im.naturalHeight||im.height)/(im.naturalWidth||im.width),a=p<.6?1:Math.pow(1-(p-.6)/.4,1.4);
    ctx.save();ctx.globalAlpha=clamp(a,0,1);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,b.x-w/2,b.y-h*.86,w,h);ctx.restore();
  }
}
drawAtomBooms=function(){s67NukeDraw();return S67_BASE.drawAtomBooms();};
/* the falling atom bomb, drawn here instead of groundTargetingDraw's 24px spinning pip */
function s67AtomBombDraw(q){
  if(!XART.rdy('lz_bomb'))return;const im=XART.get('lz_bomb'),J=q._s67JB||q._jetBomb;if(!J)return;
  const u=clamp(q.t/q.warn,0,1),p=u*u,x=lerp(J.x,q.x,p),y=lerp(J.y,q.y,p)-Math.sin(u*Math.PI)*22;
  const h=lerp(54,30,u),w=h*(im.naturalWidth||im.width)/Math.max(1,im.naturalHeight||im.height);
  const a=Math.atan2(q.y-J.y,q.x-J.x)-Math.PI/2+Math.sin(q.t*9)*.10;
  ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();
}
groundTargetingDraw=function(){
  const mine=groundTargetingFx.filter(q=>q._s67Atom&&!q.impact&&!(q.delay>0));
  for(const q of mine){q._s67JB=q._jetBomb;q._jetBomb=null;}
  try{S67_BASE.groundTargetingDraw();}finally{for(const q of mine)q._jetBomb=q._s67JB;}
  for(const q of mine)s67AtomBombDraw(q);
};
/* The assault gates: the band alone. The 0929 draw laid the tall FOV plate into each strip, which
   reads as a big triangle in every lane, plus a triangular alert sign at the edge. */
s6OpeningDraw=function(){
  const O=s6Opening;if(O?.phase!=='assault')return S67_BASE.s6OpeningDraw();
  for(const q of O.lanes){if(q.released)continue;const side=q.direction!=='south',p=clamp(q.t/q.warn,0,1);
    const L=camLeftX(),R=camRightX(),top=viewTopY();
    if(side)s67LaneBand(q.direction==='west'?R:L,q.y,q.direction==='west'?L:R,q.y,58,p,1.25);
    else s67LaneBand(q.x,top,q.x,VH,68,p,1.25);
  }
};

/* ---------------------------------------------------------------------------
   C. THE WING'S SUPPLY BOXES ARE GONE - each fighter's ability arrives at random
   The director still decides WHEN supply is due (stageTimer 18 / 45 / 57); nothing falls, nothing
   has to be shot open, and nobody has to find their own box among nine. Each due box becomes a grant
   at a random moment in the next few seconds, and between drops a random fighting wingman is powered
   up on its own clock. The player's own supply is delivered the same way (scrateYield, as the box
   held).
   --------------------------------------------------------------------------- */
function s67WingBoost(q){
  q.boostT=14;q.specialCd=0;q.missileCd=0;q.hp=Math.min(3,(q.hp||1)+1);
  if(typeof fxBurst==='function')fxBurst(q.x,q.y,24,{color:'#83dfff',rings:1,chunks:0,sparks:8});
  (Audio.SFX.powerup||function(){})();
}
s6SupplyTick=function(W,dt){
  if(!W.boxes)W.boxes=[];if(!W.s67Grants)W.s67Grants=[];
  for(const box of W.boxes)W.s67Grants.push({key:box.key,at:rnd(.5,5.5)});
  W.boxes.length=0;
  for(const g of W.s67Grants){g.at-=dt;if(g.at>0)continue;g.done=true;
    if(g.key===_pilotKey()){if(!player.dead)applyPowerup({kind:scrateYield(),x:player.x,y:player.y});}
    else{const q=W.ships.find(s=>s.key===g.key&&s.phase==='fight');if(q)s67WingBoost(q);}}
  W.s67Grants=W.s67Grants.filter(g=>!g.done);
  W.s67Rand=(W.s67Rand==null?rnd(8,12):W.s67Rand)-dt;
  if(W.s67Rand<=0){W.s67Rand=rnd(7,12);
    const live=W.ships.filter(q=>q.phase==='fight'&&!(q.boostT>0));
    if(live.length)s67WingBoost(live[(Math.random()*live.length)|0]);}
};
s6SupplyDraw=function(){};

/* ---------------------------------------------------------------------------
   D. THE WARHIVE: fewer escorts per launch (was 6, 8 on Hard and Furious)
   --------------------------------------------------------------------------- */
const S67_JETS={easy:3,normal:4,hard:5,furious:5};
warhiveInit=function(b){S67_BASE.warhiveInit(b);const W=b._whv;W.jetN=S67_JETS[diffKey]||4;W.hullFl=0;};
warhiveDamage=function(b,dmg){
  const W=b._whv;let id=b._whvHit;
  if(!id&&W&&W.mode==='carrier'&&_lastHitX!=null)id=whvCarrierHitPart(b,_lastHitX,_lastHitY);
  const r=S67_BASE.warhiveDamage(b,dmg);
  if(W&&W.mode==='carrier'){if(id==='hull')W.hullFl=.16;else if(id==='L'||id==='R')W.parts[id].fl=Math.max(W.parts[id].fl,.18);}
  return r;
};

/* ---------------------------------------------------------------------------
   E. THE STAGE 7 ESCAPE
   What was wrong, measured on the 0929 build (_shots/survey_0929/s7exit_normal):
   * the flight was 180 px/s - a crawl, not an escape;
   * the wreck drew as a near-white silhouette the whole time (a flash term of .10-.17, times 5 in
     s7mBlit, capped at .8);
   * explode() places fixed-world FX, so the cook-offs and the whole "front" stayed put on screen
     while the terrain slid under them - the fire rode along with the ship - and the front was
     spawned climbing toward the player (bottom+100 -> top-100 over 12 s);
   * the ship reached the portal under a wall of explosions and a radio box, then was simply hidden.
   Now: a short self-destruct beat with the wreck in its own colours, then the level itself scrolls
   under the ship at up to 880 px/s. The wreck, every explosion, particle, smoke puff, shock ring and
   atlas flash spawned by the escape is ANCHORED: it moves with the terrain by exactly the distance
   the terrain moved, so the boss falls behind and the fire recedes off the bottom of the screen.
   The flight decelerates onto the portal, which arrives from ahead on the same ground; the ship
   holds, then visibly flies into it and shrinks away, the portal seals, and only then does the
   blast wave roll up over the spot.
   ⚠ The distance is ANALYTIC (s67EscS), not integrated per frame, so the portal lands where it is
   meant to at any frame rate, and the terrain and the anchors can never drift apart.
   --------------------------------------------------------------------------- */
const S67E={SD:2.2,ACC:1.0,VMAX:880,CRUISE:2.9,DEC:1.9,PORTAL_Y:188,PORTAL_H:252,HOLD:.4,ENTRY:1.1,CLOSE:.9};
S67E.ARRIVE=S67E.SD+S67E.ACC+S67E.CRUISE+S67E.DEC;
S67E.TOTAL=S67E.VMAX*(S67E.ACC/2+S67E.CRUISE+S67E.DEC/2);
function s67EscS(t){
  const C=S67E,V=C.VMAX,tau=t-C.SD;if(tau<=0)return 0;
  if(tau<C.ACC){const x=tau/C.ACC;return V*C.ACC*(x*x*x-x*x*x*x/2);}
  const a=V*C.ACC/2;if(tau<C.ACC+C.CRUISE)return a+V*(tau-C.ACC);
  const b=a+V*C.CRUISE,d=tau-C.ACC-C.CRUISE;if(d<C.DEC){const x=d/C.DEC;return b+V*C.DEC*(x-(x*x*x-x*x*x*x/2));}
  return C.TOTAL;
}
function s67EscV(t){
  const C=S67E,tau=t-C.SD,s=x=>x*x*(3-2*x);if(tau<=0)return 0;
  if(tau<C.ACC)return C.VMAX*s(tau/C.ACC);if(tau<C.ACC+C.CRUISE)return C.VMAX;
  const d=tau-C.ACC-C.CRUISE;return d<C.DEC?C.VMAX*(1-s(d/C.DEC)):0;
}
function s67AnchorLists(){return [typeof explosions!=='undefined'?explosions:null,typeof particles!=='undefined'?particles:null,
  typeof smokeTrails!=='undefined'?smokeTrails:null,typeof _navalFlashes!=='undefined'?_navalFlashes:null,
  typeof shockRings!=='undefined'?shockRings:null,typeof _smokeRings!=='undefined'?_smokeRings:null,
  typeof efxBursts!=='undefined'?efxBursts:null];}
/* run fn, then tag everything it spawned as riding the terrain */
function s67Anchor(fn){const L=s67AnchorLists(),n=L.map(a=>a?a.length:0);try{fn();}finally{L.forEach((a,i)=>{if(a)for(let j=n[i];j<a.length;j++)if(a[j])a[j]._s67a=true;});}}
function s67ShiftAnchored(dy){if(!dy)return;for(const a of s67AnchorLists())if(a)for(const q of a)if(q&&q._s67a&&Number.isFinite(q.y))q.y+=dy;}
function s67ToxicBoom(x,y,size,serial){s67Anchor(()=>fr27ToxicExplosion(x,y,size,serial));}
function s67EscSay(who,text,dur){const F=boss&&boss._s7warden&&boss._s7warden.final;if(!F)return;F.radio={who:missionRadioWho(who),full:text,t:0,typed:0,dur:dur||3};}
fr27Exit=function(b,dt){
  const M=b._s7mod,F=b._s7warden.final;let E=M.frExit;
  if(!E||!E.s67){E=M.frExit={s67:true,t:0,beat:0,serial:0,fx:0,S:0,travel:0,groundY:b.y,x:b.x,sourceY:_masterSrcY,
    startX:player.x,startY:player.y,portalX:clamp((camLeftX()+camRightX())/2,170,worldWidth()-170),portalYNow:-400,zoom:1,
    blown:false,portalOn:false,portalT:0,entry:null,wave:null,done:false,v:0};
    for(const k of ['s7m_portal','s7m_explosion','s7m_spew','efx_burst_toxic'])try{XART.rdy(k);}catch(_w){}}
  E.t+=dt;M.t=E.t;M.clock+=dt;const C=S67E,t=E.t;
  F.phase='escape';b._s7FinalNoBar=true;b._s7warden.noHit=true;bossDefeated=true;eBullets.length=0;
  for(const s of seatList())withSeat(s,()=>{player.invuln=Math.max(player.invuln,3);});
  /* the terrain: one analytic distance, handed to the stage-7 backdrop (FR28 drawBG reads
     sourceY - travel) and to every anchored thing, by the same delta */
  const S=s67EscS(t),dS=S-E.S;E.S=S;E.travel=S;E.v=s67EscV(t);s67ShiftAnchored(dS);
  b.x=E.x;b.y=E.groundY+S;F.bossHidden=b.y-(b.h||260)>VH+60;
  E.portalYNow=C.PORTAL_Y-(C.TOTAL-S);
  const name=(PILOTS.find(q=>q.key===run.pilot)?.name||run.pilot).toUpperCase();
  /* radio: never over the portal entry - the lines sit either side of it */
  if(E.beat===0&&t>=.4){E.beat=1;s67EscSay('DECKER','I AM DETECTING A SELF-DESTRUCT SEQUENCE IN THAT THING!',2.6);s7WardenMechSound('scream');}
  if(E.beat===1&&t>=1.9){E.beat=2;s67EscSay('COLE',"IT'S GONNA BLOW! GET OUT OF THERE, NOW!!!",3.0);}
  if(E.beat===2&&E.entry&&E.entry.gone&&t>=E.entry.goneAt+.25){E.beat=3;s67EscSay('DECKER',name+', NOOOOOOOOOOOOOOO!',2.4);}
  if(E.beat===3&&E.wave&&t>=E.wave.t0+2.2){E.beat=4;s67EscSay('COLE','WHERE DID THEY GO? ARE THEY ALL RIGHT? CHECK THE RADAR, NOW!',3.2);}
  if(F.radio){F.radio.t+=dt;F.radio.typed+=dt*44;if(F.radio.t>F.radio.dur)F.radio=null;}
  /* 1. self-destruct: the wreck shakes and cooks off in place, in its own colours */
  if(t<C.SD){
    E.fx-=dt;if(E.fx<=0){E.fx=Math.max(.09,.26-t*.07);const i=E.serial++;
      s67ToxicBoom(b.x+Math.sin(i*2.4)*92,b.y+Math.cos(i*1.7)*70-10,70+(i%3)*24,i);if(i%2)s7mSound('expSmall');}
    shake=Math.max(shake,2+t*2.2);
    if(!E.charge&&t>=.5){E.charge=true;(Audio.SFX.bossWeaponCharge||function(){})();}
  }
  /* 2. the run: thrust, the ship eased onto the centre line, the wreck left behind */
  if(t>=C.SD&&!E.entry){
    if(!E.go){E.go=true;(Audio.SFX.dash||Audio.SFX.launch||function(){})();(Audio.SFX.boost||function(){})();E.fx=0;}
    /* loose pickups (and the boss supply clock, which still runs) are collected, never left over the portal */
    for(const p of powerups)if(!p.dead&&p.kind!=='forgecombo'){try{applyPowerup(p);}catch(_ap){}p.dead=true;}
    const k=clamp((t-C.SD)/1.4,0,1),e=k*k*(3-2*k),hy=VH*.70;
    player.x=lerp(E.startX,E.portalX,e);player.y=lerp(E.startY,hy,e);player._thrustPower=1;
    shake=Math.max(shake,1.5+3.5*(E.v/C.VMAX));
    /* the reactor goes up once it is behind us, below the bottom edge */
    if(!E.blown&&b.y>VH+40){E.blown=true;const bx=b.x,by=b.y;
      s67Anchor(()=>{for(let i=0;i<7;i++)fr27ToxicExplosion(bx+(i-3)*58,by-20+Math.abs(i-3)*14,190+(i%3)*40,E.serial++);
        if(typeof spawnShockRing==='function')for(const r of [200,320])spawnShockRing(bx,by,r,'fire');});
      shake=Math.max(shake,16);E.greenFlash=.42;(Audio.SFX.atomicDetonate||Audio.SFX.expBig||function(){})();s7mSound('expBig');}
    /* the fire behind: spawned under the bottom edge on the ground, so it can only fall away */
    if(E.blown&&t<C.SD+C.ACC+C.CRUISE){E.fx-=dt;if(E.fx<=0){E.fx=.10;
      s67ToxicBoom(camLeftX()+Math.random()*viewW(),VH-12+Math.random()*40,150+Math.random()*70,E.serial++);if(E.serial%4===0)s7mSound('expSmall');}}
    /* the portal comes into view on the ground ahead and the flight settles onto it */
    if(!E.portalOn&&E.portalYNow>-C.PORTAL_H){E.portalOn=true;E.portalT=0;(Audio.SFX.warpGate||Audio.SFX.teleportIn||function(){})();}
    if(t>=C.ARRIVE+C.HOLD){E.entry={t0:t,x0:player.x,y0:player.y,gone:false,scale:1};}
  }
  if(E.portalOn)E.portalT+=dt;
  if(E.entry)for(const p of powerups)if(!p.dead&&p.kind!=='forgecombo')p.dead=true;
  /* 3. into the portal - visible, centred, nothing over it */
  if(E.entry){
    const P=E.entry,u=clamp((t-P.t0)/C.ENTRY,0,1),e=u*u;
    if(!P.gone){player.x=lerp(P.x0,E.portalX,e);player.y=lerp(P.y0,E.portalYNow,e);player._thrustPower=1;
      P.scale=1-.82*clamp((u-.25)/.75,0,1);E.zoom=1+.2*(u*(2-u));F.shipHidden=true;
      if(u>=1){P.gone=true;P.goneAt=t;E.closeT=t;
        s67Anchor(()=>{if(typeof efxBurst==='function')efxBurst('toxic',E.portalX,E.portalYNow,120);if(typeof spawnShockRing==='function')spawnShockRing(E.portalX,E.portalYNow,150,'fire');});
        E.whiteFlash=.55;(Audio.SFX.teleportIn||Audio.SFX.warpGate||function(){})();}}
    else if(!E.wave&&t>=P.goneAt+C.CLOSE*.8)E.wave={t0:t,fx:0};
  }
  /* 4. the blast finally reaches the spot the ship left */
  if(E.wave){const W=E.wave,k=clamp((t-W.t0)/1.5,0,1);W.fx-=dt;
    if(k<1&&W.fx<=0){W.fx=.07;const front=lerp(VH+60,viewTopY()+40,k);
      for(let i=0;i<2;i++)s67ToxicBoom(camLeftX()+Math.random()*viewW(),front+Math.random()*80,170+Math.random()*90,E.serial++);if(E.serial%3===0)s7mSound('expBig');}
    shake=Math.max(shake,k<1?8:0);}
  E.greenFlash=Math.max(0,(E.greenFlash||0)-dt*1.4);E.whiteFlash=Math.max(0,(E.whiteFlash||0)-dt*1.8);
  /* 5. done */
  const end=E.wave?E.wave.t0+6.4:1e9;
  if(t>=end-1.4)E.fade=clamp((t-(end-1.4))/1.2,0,1);
  if(t>=end&&!E.done){E.done=true;
    if(!b._forgeRewardDropped){b._forgeRewardDropped=true;forgeBossDrop(player.x,player.y);run.score+=35000;}
    for(const p of powerups)if(p.kind==='forgecombo'&&!p.dead){applyPowerup(p);p.dead=true;}
    F.finished=true;F.phase='done';F.radio=null;F.shipHidden=false;b.dead=true;bossActive=false;bossDefeated=true;whiteBlast=0;run._l78Entry=1;
    if(typeof cf4PortalHandoff==='function')cf4PortalHandoff();else{if(run.mode==='campaign')campaign._l78Pending=1;drawStageClear._init=false;drawStageClear._res=null;Audio.stopMusic();setState(GS.STAGECLEAR);}}
  return true;
};
/* the wreck: its frozen pose on the ground it died on, in its own colours (a faint overload pulse
   during the self-destruct beat only) */
const S67_S7DRAW=s7mDraw;
s7mDraw=function(b){
  const M=b?._s7mod,E=M?.frExit;if(!E||!E.s67)return S67_S7DRAW(b);
  if(b.y-(b.h||260)>VH+60)return true;
  if(!E.pose){E.pose=s7mPose(b).map(p=>({...p}));}
  M.height=0;M.drop=0;M.lean=0;
  const pulse=E.t<S67E.SD?.018+.022*Math.max(0,Math.sin(E.t*(14+E.t*6))):0,jx=E.t<S67E.SD?Math.sin(E.t*47)*1.6:0;
  for(const p of E.pose){const part=M.parts.find(q=>q.id===p.id);if(part&&part.hp<=0)continue;
    s7mBlit(p.id==='body'?'body':'warden',p.cell,b.x+p.x+jx,b.y+p.y,p.w,p.h,p.a||0,1,pulse);}
  return true;
};
/* speed lines while the level races by, under everything else */
function s67StreaksDraw(E){
  const v=E.v||0;if(v<60)return;const k=v/S67E.VMAX,L=camLeftX(),W=viewW(),top=viewTopY(),H=VH-top+160;
  ctx.save();ctx.fillStyle='#d8ffd0';
  for(let i=0;i<26;i++){const x=L+((i*97.3)%W),y=top-80+((i*173.7+E.S*(1.25+(i%3)*.18))%H),len=18+v*.085;
    ctx.globalAlpha=(.06+.20*k)*(i%3===0?1:.6);ctx.fillRect(Math.round(x),Math.round(y),i%4===0?2:1,Math.round(len));}
  ctx.restore();
}
const S67_PORTAL_WORLD=drawS7FinalPortalWorld;
drawS7FinalPortalWorld=function(){
  if(run.stage!==7)return;const M=boss?._s7mod,E=M&&M.frExit;
  if(!E||!E.s67)return S67_PORTAL_WORLD();
  s67StreaksDraw(E);
  const C=S67E;
  if(E.portalOn&&!(E.closeT&&E.t>E.closeT+C.CLOSE)){
    let f;const age=E.portalT;
    if(E.closeT){const c=clamp((E.t-E.closeT)/C.CLOSE,0,1);f=12+Math.min(3,Math.floor(c*4));}
    else f=age<.8?Math.min(3,Math.floor(age*5)):4+Math.floor(age*10)%8;
    missionToxicPortal(f,E.portalX,E.portalYNow,C.PORTAL_H,C.PORTAL_H*.87);
    if(E.whiteFlash>0){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=E.whiteFlash;missionToxicPortal(f,E.portalX,E.portalYNow,C.PORTAL_H,C.PORTAL_H*.87);ctx.restore();}
  }
  const P=E.entry;
  if(P&&!P.gone&&typeof _drawPlayerCore==='function'){
    const s=P.scale==null?1:P.scale;ctx.save();ctx.translate(player.x,player.y);ctx.scale(s,s);ctx.translate(-player.x,-player.y);
    ctx.globalAlpha=clamp(.25+s,0,1);try{_drawPlayerCore();}catch(_pc){}ctx.restore();
  }
};
const S67_CAM=fr27CinematicCamera;
fr27CinematicCamera=function(){
  const E=run.stage===7&&boss?._s7mod?.frExit;if(!E||!E.s67)return S67_CAM();
  const z=E.zoom||1;if(z===1)return;const px=E.portalX,py=E.portalYNow;
  ctx.translate(px,py);ctx.scale(z,z);ctx.translate(-px,-py);
};
const S67_RADIO_DRAW=s7WardenRadioDraw;
s7WardenRadioDraw=function(){
  const E=boss?._s7mod?.frExit;if(!E||!E.s67)return S67_RADIO_DRAW();
  if(E.greenFlash>0){ctx.save();ctx.fillStyle='rgba(120,255,70,'+Math.min(.45,E.greenFlash)+')';ctx.fillRect(0,0,VW,VH);ctx.restore();}
  FR27_BASE.s7Radio();
  if(E.fade>0){ctx.save();ctx.fillStyle='rgba(0,0,0,'+E.fade+')';ctx.fillRect(0,0,VW,VH);ctx.restore();}
};

/* ---------------------------------------------------------------------------
   F. THE STAGE 7 SLUICE MAKES SENSE
   It read as nonsense for two reasons, both in the picture (_shots/survey_0929/s7sluice_normal):
   the warning was sluice_warning_lane.png - an orange/black striped BOOM with a lamp at each end,
   i.e. a solid barrier that appears across the floor and then is replaced by goo - and the jet
   stopped dead in mid-air halfway across the walkway, like a beam, with nothing where it landed.
   Now the OUTLET warns (its lamp flares, the grate rattles, it dribbles - the authored drip frames),
   the floor shows exactly where the spray will land in the shared green/yellow/red lane, and the
   jet ends in the authored toxic splash (s7m spew) on the floor where it hits, which pools and
   drains after it. Timing, reach and the hit band are unchanged.
   --------------------------------------------------------------------------- */
const S67_SLUICE_MOUTH=350*213/(1774/4);
stage7SluiceDraw=function(){
  if(!run||run.stage!==7||!XART.rdy('s7sluice_vent'))return;
  const sheet=XART.get('s7sluice_vent'),fw=(sheet.naturalWidth||sheet.width)/4,fh=(sheet.naturalHeight||sheet.height)/2;
  const warn=stage7SluiceWarn(),W=worldWidth(),sizeX=350,sizeY=180,rank=diffKey==='furious'?2:diffKey==='hard'?1:0;
  for(const e of stage7SluiceEvents()){
    if(e.tier>rank)continue;const y=e.row-_masterSrcY;if(y<-sizeY*.5||y>VH+sizeY*.5)continue;
    const split=213,originY=y-sizeY*265/fh,warning=e.live&&!e.done&&e.t<warn,firing=e.live&&!e.done&&e.t>=warn,age=e.t-warn;
    ctx.save();ctx.imageSmoothingEnabled=false;if(e.side>0){ctx.translate(W,0);ctx.scale(-1,1);}
    /* the floor lane first, so the pipe and the spray sit on top of it */
    if(warning)s67LaneBand(S67_SLUICE_MOUTH,y,350,y,48,clamp(e.t/warn,0,1),1.35);
    /* the outlet: rattles and dribbles while pressure builds (authored frames 0/1, then the burst frame) */
    const k=warning?clamp(e.t/warn,0,1):0,rattle=warning?Math.sin(e.t*(40+k*50))*(1+k*2):0;
    const pf=warning?(k>.82?2:Math.floor(e.t*7)%2):0;
    if(pf===0)ctx.drawImage(sheet,0,0,split,fh,0,originY+rattle*.4,sizeX*split/fw,sizeY);
    else ctx.drawImage(sheet,pf*fw,0,fw,fh,0,originY+rattle*.4,sizeX,sizeY);
    if(warning){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.25+.45*k*(.5+.5*Math.sin(e.t*(10+k*24)));
      ctx.drawImage(sheet,0,0,split,fh,0,originY,sizeX*split/fw,sizeY);ctx.restore();}
    if(firing){
      const f=stage7SluiceFrame(age),dx=f%4===3?-33:0,dy=f>=4?-31:0,jetY=160,jetH=240;
      ctx.drawImage(sheet,(f%4)*fw+split+dx,Math.floor(f/4)*fh+jetY+dy,fw-split,jetH,
        sizeX*split/fw,originY+sizeY*jetY/fh,sizeX*(fw-split)/fw,sizeY*jetH/fh);
    }
    ctx.restore();
    /* where the jet comes down: the splash, then the pool draining (drawn unmirrored, at the tip) */
    if(firing&&e._s67F0==null)e._s67F0=efxClock-age;
    const sAge=e._s67F0==null?-1:efxClock-e._s67F0;
    if(sAge>=0&&sAge<2.2){
      const reach=sAge<.14?252:350,tip=e.side<0?reach-8:W-reach+8,u=clamp(sAge/1.35,0,1),sf=Math.min(15,Math.floor(u*16));
      const sz=sAge<.14?70:112;s7mBlit('spew',sf,tip,y-sz*.28,sz,sz,0,sAge>1.1?clamp(1-(sAge-1.1)/1.0,0,1):1);
    }
  }
};
/* the splash reel must be decoded before the first vent fires */
const S67_SLUICE_TICK=stage7SluiceTick;
stage7SluiceTick=function(dt){if(run&&run.stage===7)s7mWarm();return S67_SLUICE_TICK(dt);};

/* ---------------------------------------------------------------------------
   G. A BETTER STAGE 7 ENTRANCE
   It was campaign_story's drawGateLaunch: a painted 3/4-view gate still (purple, a different
   perspective and palette from the top-down green sewer), the ship shrinking into it, a fade to
   BLACK, then a hard cut into play. Every other stage enters through the engine's own connector -
   the stage's material, top-down, butt-joined to the level's first frame so the last launch frame
   IS the first play frame (0810j). Stage 7 now does the same over its own sludge (ENTRY_CONN[7] =
   nlq_sludgeF), and the descent is sold ON that strip: the sewer's darkness closes in from the
   edges as the ship goes under, the radar drops its signal, and the ship-system line types in.
   --------------------------------------------------------------------------- */
if(window.BOFCampaignStory)window.BOFCampaignStory.drawGateLaunch=null;
const S67_LAUNCH=drawLaunch;
drawLaunch=function(dt){
  const r=S67_LAUNCH(dt);
  if(run.stage===7&&state===GS.LAUNCH){
    const t=stateT||0,ph=drawLaunch._phase,out=ph==='run'?1:ph==='brake'?clamp(1-(drawLaunch._pt||0)/1.6,0,1):0,k=clamp(t/1.8,0,1)*out;
    if(k>0){ctx.save();
      /* underground: the light closes in from the edges and lifts as the lit level arrives - never a fade to black */
      const g=ctx.createRadialGradient(VW/2,VH*.66,VH*.12,VW/2,VH*.6,VH*.56);
      g.addColorStop(0,'rgba(0,8,0,0)');g.addColorStop(1,'rgba(0,10,2,'+(.86*k)+')');
      ctx.fillStyle=g;ctx.fillRect(-VW,-VH,VW*3,VH*3);ctx.restore();}
    if(t>.5&&t<5.2&&typeof dlgBox==='function'){const full='ENTERING UNDERGROUND. EXTERIOR SIGNAL LOST.',n=Math.floor((t-.5)*34);
      dlgBox({who:'SHIP SYSTEM',full,shown:full.slice(0,n),portrait:false,tint:'#8cff5a',y:16,fade:clamp((5.2-t)/.4,0,1)});}
  }
  return r;
};

/* ---------------------------------------------------------------------------
   H. THE WARDEN ON FURIOUS: CHAINGUN, STOMP-AND-SWAT, TOXIC MORTAR CLOUDS
   Mike: "Make him go into machine gun mode with actual toxic bullets and basically like a chaingun,
   angling his barrels in a sweep pattern. Make him stomp up and down and then swat at us with his
   legs/claws. make him charge up toxic mortar rounds from his core he can launch that cloud the screen."
   Furious only, woven into his rotation every other pick (s7mNext). Normal and Hard are untouched.
   * CHAINGUN: both barrels extend and swing in a SCISSOR sweep (mirrored sines, +-0.72 rad), firing
     alternately at ~22 rounds/s. The rounds are real bullets - kind 'mg', which stage 7 already draws
     in its green pellet family (PELLET_FAM[7] = 3) - not the toxic orbs his chain mode throws.
   * STOMP: three hops toward the pilot, each landing on a committed ground reticle (the shared
     ground-targeting vocabulary), cracking the floor with a splash, a shock ring and a ring of acid;
     then the claws swat (swipeL -> swipeR -> swipeX) on a shortened wind-up.
   * TOXIC MORTAR: the faceplate opens and the core visibly charges (a growing toxic orb, 1.6 s), then
     it lobs four big toxic rounds onto reticles (tb28 lobs: airborne and harmless until they land),
     and each lands as a drifting gas cloud - the stage-6 cloud bank palette-swapped toxic - that hangs
     over the field for ~6 s and CLOUDS THE SCREEN. The clouds hide the fight; they do no damage.
   --------------------------------------------------------------------------- */
const S67W={CG_WARN:.85,CG_FIRE:3.0,CG_SWEEP:.72,CG_RATE:.045,ST_CYCLE:.66,ST_HOPS:3,MO_CHARGE:1.6,MO_N:4,CLOUD_LIFE:6.2};
const S67_WARDEN_MODES=['chaingun','stomp','toxic-mortar'];
function s67Furious(b){const M=b&&b._s7mod;return !!(M&&!M.tank&&M.n===2);}
const S67_S7NEXT=s7mNext;
s7mNext=function(b){
  const M=b._s7mod;
  if(s67Furious(b)){
    M.s67n=(M.s67n||0)+1;
    if(M.s67n%2===0)for(let k=0;k<3;k++){const m=S67_WARDEN_MODES[(M.s67i=(M.s67i||0)+1)%3];
      if(m==='chaingun'&&!s7mLive(M,'gun').length)continue;
      s7mSet(b,m);return;}
  }
  return S67_S7NEXT(b);
};
const S67_S7SET28=s7m28Set;
s7m28Set=function(b,mode){
  const M=b._s7mod;
  if(mode==='chaingun'){M.warn=S67W.CG_WARN;M.live=S67W.CG_FIRE;M.cgBase=aimPlayer(b.x,b.y+60);M.cgAng=null;
    s7mSound('bossWeaponCharge');combatWarningTick(b,'s7m-chaingun',0,M.warn,true);return;}
  if(mode==='stomp'){M.warn=0;M.live=S67W.ST_CYCLE*S67W.ST_HOPS+.35;M.hop=-1;M.lastLand=-1;return;}
  if(mode==='toxic-mortar'){M.warn=S67W.MO_CHARGE;M.live=2.2;M.cast=false;
    for(let i=0;i<6;i++)XART.rdy('nl6c_low_rolling_bank_'+i);s7mSound('bossWeaponCharge');return;}
  if(mode&&mode.startsWith('swipe')&&M.s67Swat>0){M.s67Swat--;M.warn=.46;}
  return S67_S7SET28(b,mode);
};
let s67Clouds=[];
function s67CloudSpawn(x,y){for(let i=0;i<2;i++)s67Clouds.push({x:x+(i?rnd(-40,40):0),y:y+(i?rnd(-30,20):0),t:0,life:S67W.CLOUD_LIFE+rnd(-.6,.6),
  w:rnd(250,330),vx:rnd(-14,14),vy:rnd(-10,4),k:(Math.random()*6)|0});}
const S67_S7TICK28=s7m28Tick;
s7m28Tick=function(b,dt){
  const M=b._s7mod,mode=M.mode;
  if(mode==='chaingun'){
    const guns=s7mLive(M,'gun');if(!guns.length){s7mSet(b,'recover');return true;}
    s7mMove(b,clamp(player.x,160,worldWidth()-160),175,38,dt);
    if(M.t<M.warn){combatWarningTick(b,'s7m-chaingun',M.t,M.warn,true);return true;}
    const u=M.t-M.warn,sw=Math.sin(u*2.35)*S67W.CG_SWEEP;
    M.cgAng={gunL:M.cgBase+sw,gunR:M.cgBase-sw};
    if(M.shotCD<=0){M.shotCD=S67W.CG_RATE;M.shot++;
      const g=guns[M.shot%guns.length],q=s7mMuzzle(b,g.id),a=M.cgAng[g.id];
      const r=eShootT(q.x,q.y,a,4.9,'mg',{w:6,h:14,silent:true});r._s7modOwner=b;r._noArsenal=true;r._boss=true;r._s7modGun=true;
      navalFlash(null,q,.6,'weapon_muzzle_rotary',{n:4,hpx:30,life:.08,follow:()=>s7mMuzzle(b,g.id)});
      if(M.shot%3===1)s7mSound('machineGun');}
    if(M.t>M.warn+M.live){M.cgAng=null;s7mSet(b,'recover');}
    return true;
  }
  if(mode==='stomp'){
    const C=S67W.ST_CYCLE,hop=Math.floor(M.t/C),u=(M.t%C)/C;
    if(hop>=S67W.ST_HOPS){M.height=0;if(M.t>=M.live){M.s67Swat=3;s7mSet(b,'swipeL');}return true;}
    if(hop!==M.hop){M.hop=hop;M.from={x:b.x,y:b.y};
      const tx=clamp(lerp(b.x,player.x,.55),150,worldWidth()-150),ty=clamp(Math.min(player.y-150,b.y+45),150,VH*.52);
      M.hopTo={x:tx,y:ty};
      const g=groundTargetingSpawn({kind:'missile',owner:b,x:tx,y:ty+70,warn:C*.95,active:.18,radius:92,size:170,track:false,shake:0,sound:'hammerImpact'});g._late27=true;}
    M.height=Math.sin(u*Math.PI)*95;const e=u*u*(3-2*u);b.x=lerp(M.from.x,M.hopTo.x,e);b.y=lerp(M.from.y,M.hopTo.y,e);
    if(u>.95&&M.lastLand!==hop){M.lastLand=hop;
      s7mFX(b.x,b.y+70,190,true);shake=Math.max(shake,14);s7mSound('expBig');s7WardenMechSound('foot');
      if(typeof spawnShockRing==='function')spawnShockRing(b.x,b.y+70,150,'fire');
      for(let i=0;i<10;i++){const a=i*TAU/10+hop*.3;s7mShot(b,b.x+Math.cos(a)*60,b.y+70+Math.sin(a)*30,a,2.3,'acid');}}
    return true;
  }
  if(mode==='toxic-mortar'){
    s7mMove(b,worldWidth()/2,165,30,dt);M.mask=Math.min(1,M.mask+dt*2.2);
    if(M.t<M.warn){M.coreFlash=Math.max(M.coreFlash||0,.03+.05*(M.t/M.warn));shake=Math.max(shake,1+2*(M.t/M.warn));return true;}
    if(!M.cast){M.cast=true;s7WardenMechSound('roar');shake=Math.max(shake,9);
      for(let i=0;i<S67W.MO_N;i++){const off=[0,-150,150,-75][i],oy=[0,-40,-40,60][i];
        tb28Fire(b,{from:()=>b.dead?null:s7mMuzzle(b,'emitter'),target:{x:clamp(player.x+off,camLeftX()+60,camRightX()-60),y:clamp(player.y+oy,viewTopY()+120,VH-70)},
          warm:.15+i*.22,flight:1.0,mode:'lob',arc:170,art:'toxic',size:40,splash:44,reticle:96,width:30,laneAlpha:.45,silent:i>0,
          onArrive:(q,x,y)=>{s7mFX(x,y,150,true);s7mSound('expBig');s67CloudSpawn(x,y);}});}}
    if(M.t>M.warn+M.live){M.mask=0;s7mSet(b,'recover');}
    return true;
  }
  return S67_S7TICK28(b,dt);
};
const S67_S7POSE=s7mPose;
s7mPose=function(b){
  const parts=S67_S7POSE(b),M=b._s7mod;
  if(M&&M.mode==='chaingun'){const ext=Math.min(1,M.t/.5)*18;
    for(const p of parts)if(p.id==='gunL'||p.id==='gunR'){const a=(M.cgAng&&M.cgAng[p.id])||M.cgBase||Math.PI/2;
      p.a=clamp(a-Math.PI/2,-.95,.95);p.h=84+ext;p.y=49+ext/2;}}
  return parts;
};
/* the wind-ups, drawn with the Warden: the barrels' sweep envelope and the charging core */
const S67_S7DRAW_FUR=s7mDraw;
s7mDraw=function(b){
  const r=S67_S7DRAW_FUR(b),M=b&&b._s7mod;if(!M||M.frExit)return r;
  if(M.mode==='chaingun'&&M.t<M.warn){for(const g of s7mLive(M,'gun')){const q=s7mMuzzle(b,g.id);
    combatWarningDraw(b,{x:q.x,y:q.y,ex:q.x+Math.cos(M.cgBase)*600,ey:q.y+Math.sin(M.cgBase)*600,progress:M.t/M.warn,width:Math.tan(S67W.CG_SWEEP)*230,alpha:.26,fieldOnly:true});}}
  if(M.mode==='toxic-mortar'&&!M.cast){const k=clamp(M.t/M.warn,0,1),q=s7mMuzzle(b,'emitter'),d=26+k*70;
    ctx.save();ctx.globalCompositeOperation='lighter';s7mBlit('orb',Math.floor(M.clock*14)%8,q.x,q.y-10,d,d,M.clock*3,.45+.5*k);ctx.restore();}
  return r;
};
const S67_UPD_ATOM2=updateAtomBooms;
updateAtomBooms=function(dt){S67_UPD_ATOM2(dt);
  for(const c of s67Clouds){c.t+=dt;c.x+=c.vx*dt;c.y+=c.vy*dt;c.w+=dt*18;}
  s67Clouds=s67Clouds.filter(c=>c.t<c.life&&run.stage===7);};
const S67_DRAW_ATOM2=drawAtomBooms;
drawAtomBooms=function(){
  for(const c of s67Clouds){const key='nl6c_low_rolling_bank_'+c.k;if(!XART.rdy(key))continue;const im=xartPalette(key,'#62e82c');if(!im)continue;
    const a=Math.min(1,c.t/.5)*Math.min(1,(c.life-c.t)/1.2),h=c.w*(im.height/im.width);
    // Keep the toxic atmosphere without burying ships, reticles and projectiles.
    const overlap=Math.max(1,s67Clouds.filter(q=>Math.abs(q.x-c.x)<(q.w+c.w)*.35&&Math.abs(q.y-c.y)<h).length);
    ctx.save();ctx.globalAlpha=.26*a/Math.sqrt(overlap);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,c.x-c.w/2,c.y-h/2,c.w,h);ctx.restore();}
  return S67_DRAW_ATOM2();
};

/* ---------------------------------------------------------------------------
   I. THE WARHIVE, MODULAR
   Built from modules (_BUILD_SOURCE/warhive_modular_0929.py derives every one from authored plates):
     well floor  -> the FAN (spinning, motion-blurred, spinning UP and glowing as its cannon charges)
     -> the BEAM CANNON (the Furnace's authored coil cannon in the carrier's gunmetal, cyan coils), which
        DEPLOYS out from under the front of its nacelle on Hard/Furious and retracts when the carrier leaves
     -> the hull plate with both fan wells cut open, so the fans turn UNDER the rim lip instead of a 44px
        disc spinning inside a static painted fan 63px across (the old draw)
     -> door / wreck plates, part fire and smoke, the escorts still in the bay.
   The beam and the cannon volleys leave the cannon's MUZZLE, not the fan hub; the beam itself is the
   Tempest's authored blue beam (tlv_beam). Every hit flashes (0912y): the hull on a hull hit (it had no
   hull flash at all), the fan on a thruster hit, the door on a door hit.
   ⚠ Hit regions, HP, phases and timings are the 0918 rig's, untouched - this is its body, not its brain.
   --------------------------------------------------------------------------- */
for(const [k,f] of [['whv_closed_w','carrier_closed_wells'],['whv_open_w','carrier_open_wells'],['whv_broken_w','carrier_broken_wells'],
  ['whv_well','carrier_well'],['whv_cannon','carrier_cannon'],['whv_acem_body','ace_mod_body'],['whv_acem_wingL','ace_mod_wingL'],['whv_acem_wingR','ace_mod_wingR'],
  ['whv_acem_body_dmg','ace_mod_body_dmg'],['whv_acem_wingL_dmg','ace_mod_wingL_dmg'],['whv_acem_wingR_dmg','ace_mod_wingR_dmg']])
  XART._src[k]='assets/game/bosses/skycarrier/'+f+'.png';
const S67C={FAN_D:58,WELL_D:60,CAN_W:34,CAN_H:59.5,CAN_IN:30,CAN_OUT:84};
const S67_WHV_WARM=whvWarm;
whvWarm=function(){S67_WHV_WARM();for(const k of ['whv_closed_w','whv_open_w','whv_broken_w','whv_well','whv_cannon','tlv_beam','mission29_beam_lightning','whv_acem_body','whv_acem_wingL','whv_acem_wingR','whv_acem_body_dmg','whv_acem_wingL_dmg','whv_acem_wingR_dmg'])try{XART.rdy(k);}catch(_w){}};
function s67WhvDeployed(W){return W.hard&&W.mode==='carrier'&&['open','launch','hold'].includes(W.st);}
/* the cannon's muzzle, in world space: under the front of its nacelle, as far out as it is deployed */
function s67WhvMuzzle(b,side){const W=b._whv,s=WHV_S,dep=(W.dep&&W.dep[side])||0,hub=whvPartPos(b,side);
  return {x:hub.x,y:hub.y+(W.dy||0)+(lerp(S67C.CAN_IN,S67C.CAN_OUT,dep)+S67C.CAN_H*.5-6)*s};}
const S67_WHV_TICK=whvCarrierTick;
whvCarrierTick=function(b,dt){
  const W=b._whv;if(!W.dep)W.dep={L:0,R:0};if(!W.spin)W.spin={L:0,R:0};
  for(const id of ['L','R']){const want=s67WhvDeployed(W)&&!W.parts[id].dead?1:0;W.dep[id]+=clamp(want-W.dep[id],-dt*1.8,dt*1.8);
    const B=[W.beam,W.beam2].find(q=>q&&q.side===id),charge=B?clamp(B.t/B.warn,0,1):(W.can.seq&&W.can.seq.side===id?.5:0);
    W.spin[id]+=((W.fanV||9)*(1+charge*2.4)-W.spin[id])*Math.min(1,dt*3);}
  W.hullFl=Math.max(0,(W.hullFl||0)-dt);
  return S67_WHV_TICK(b,dt);
};
/* the Hard cannon book, unchanged in pattern and timing - the rounds leave the deployed muzzle */
whvCannonTick=function(b,dt){
  const W=b._whv,C=W.can,live=['L','R'].filter(s=>!W.parts[s].dead);
  if(!W.hard||!live.length||W.st==='descend'||W.st==='retreat'||W.st==='away')return;
  if(W.beam)return;
  if(C.seq){const S=C.seq;S.t+=dt;
    while(S.shots.length&&S.shots[0].at<=S.t){const s=S.shots.shift(),q=s67WhvMuzzle(b,S.side),a=Math.atan2(player.y-q.y,player.x-q.x)+s.off;
      W.shots.push({x:q.x,y:q.y,vx:Math.cos(a)*s.sp,vy:Math.sin(a)*s.sp,r:13,t:0,kind:'ball'});whvSfx('laserShot',.7);}
    if(!S.shots.length)C.seq=null;return;}
  C.cd-=dt*(DIFF.eFire||1);if(C.cd>0)return;
  const book=(W.fur&&W.od&&live.length===2)?['flurry','twin','spread','beam']:['flurry','spread','beam'];
  const side=live[C.i%live.length],pat=book[C.i%book.length];C.i++;C.last=pat;
  if(pat==='beam'){W.beam={side,t:0,warn:1.55,fire:1.25,w:VW/3};whvSfx('beamCharge');C.cd=2.4;return;}
  if(pat==='twin'){W.beam={side:'L',t:0,warn:1.55,fire:1.2,w:VW/4};W.beam2={side:'R',t:0,warn:1.55,fire:1.2,w:VW/4};whvSfx('beamCharge');C.cd=2.8;return;}
  if(pat==='flurry'){
    for(let k=0;k<5;k++)tb28Fire(b,{from:()=>b.dead||W.parts[side].dead?null:s67WhvMuzzle(b,side),
      target:{x:player.x+rnd(-24,24),y:player.y+rnd(-16,10)},warm:.62+k*.2,track:.45,flight:.7,mode:'direct',art:'plasma',size:26,silent:k>0,
      onArrive:(q,x,y)=>explode(x,y,22,'blue')});
    whvSfx('beamCharge',.5);C.cd=2.3;return;}
  const shots=[];for(let r=0;r<2;r++)for(const o of [-.32,0,.32])shots.push({at:r*.5,off:o,sp:2.9});C.cd=2.0;C.seq={side,t:0,shots};
};
function s67WhvCannonDraw(b,id,alpha){
  const W=b._whv,s=WHV_S,dep=(W.dep&&W.dep[id])||0,hub=whvPartPos(b,id);if(!XART.rdy('whv_cannon'))return;
  const im=XART.get('whv_cannon'),w=S67C.CAN_W*s,h=S67C.CAN_H*s,y=hub.y+(W.dy||0)+lerp(S67C.CAN_IN,S67C.CAN_OUT,dep)*s;
  ctx.save();ctx.globalAlpha=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,hub.x-w/2,y-h/2,w,h);
  const B=[W.beam,W.beam2].find(q=>q&&q.side===id),k=B&&B.t<B.warn?clamp(B.t/B.warn,0,1):B?1:(W.can.seq&&W.can.seq.side===id?.45:0);
  if(k>0){ctx.globalCompositeOperation='lighter';ctx.globalAlpha=alpha*(.25+.6*k*(.6+.4*Math.sin((b.t||0)*(18+k*30))));ctx.drawImage(im,hub.x-w/2,y-h/2,w,h);
    // The coils themselves carry the charge; no spherical orb covering the nozzle.
  }
  ctx.restore();
}
const S67_BASE_WHV_DRAW=whvDrawCarrier;
whvDrawCarrier=function(b){
  const W=b._whv,cx=W.cx,cy=W.cy+(W.dy||0),s=WHV_S,pw=WHV_PLATE.w*s,ph=WHV_PLATE.h*s;
  if(cy<-ph)return;
  const state=W.parts.door.dead?'broken':(W.doorOpen?'open':'closed'),key='whv_'+state+'_w';
  if(!XART.rdy(key)||!XART.rdy('whv_fan')){S67_BASE_WHV_DRAW(b);return;}
  let alpha=1;if(W.mode==='death')alpha=W.t<3.6?1:Math.max(0,1-(W.t-3.6)/.8);if(alpha<=0)return;
  if(!W.fanM)W.fanM={L:0,R:0};
  ctx.save();ctx.globalAlpha=alpha;ctx.imageSmoothingEnabled=false;
  /* 1. the cannons sit UNDER the hull: they slide out from beneath the nacelle */
  for(const id of ['L','R'])if(!W.parts[id].dead)s67WhvCannonDraw(b,id,alpha);
  /* 2. the fans in their open wells */
  for(const id of ['L','R']){const p=W.parts[id],q={x:cx+WHV_NAC[id].x*s,y:cy+WHV_NAC[id].y*s};if(p.dead)continue;
    W.fanM[id]+=((W.spin&&W.spin[id])||W.fanV||9)*(_lastDt||1/60)*(id==='L'?1:-1);
    if(XART.rdy('whv_well')){const d=S67C.WELL_D*s;ctx.drawImage(XART.get('whv_well'),q.x-d/2,q.y-d/2,d,d);}
    const d=S67C.FAN_D*s,a=W.fanM[id],v=(W.spin&&W.spin[id])||9;
    whvSprite('whv_fan',q.x,q.y,d,d,a,alpha);
    whvSprite('whv_fan',q.x,q.y,d,d,a-(id==='L'?1:-1)*Math.min(.35,v*.012),alpha*.42);   // motion blur trailing the spin
    const B=[W.beam,W.beam2].find(z=>z&&z.side===id),k=B?clamp(B.t/B.warn,0,1):0;
    if(k>0){const c=xartPalette('whv_fan','#3ad0ff');if(c){ctx.save();ctx.translate(q.x,q.y);ctx.rotate(a);ctx.globalCompositeOperation='lighter';ctx.globalAlpha=alpha*.55*k;ctx.drawImage(c,-d/2,-d/2,d,d);ctx.restore();}}
    if(p.fl>0){const c=xartTint('whv_fan','#ffffff',1);if(c){ctx.save();ctx.translate(q.x,q.y);ctx.rotate(a);ctx.globalAlpha=alpha*Math.min(1,p.fl*9);ctx.drawImage(c,-d/2,-d/2,d,d);ctx.restore();}}}
  /* 3. the hull, rims over the fans */
  ctx.drawImage(XART.get(key),cx-pw/2,cy-ph/2,pw,ph);
  const hullFlash=Math.max(W.hullFl||0,b.flash||0);
  if(hullFlash>0){const c=xartTint(key,'#ffffff',1);if(c){ctx.save();ctx.globalAlpha=alpha*Math.min(1,hullFlash*9);ctx.drawImage(c,cx-pw/2,cy-ph/2,pw,ph);ctx.restore();}}
  for(const id of ['L','R'])if(W.parts[id].dead){const q={x:cx+WHV_NAC[id].x*s,y:cy+WHV_NAC[id].y*s},d=WHV_POD_R*2.1*s;whvSprite('whv_twreck',q.x,q.y,d,d,0,alpha);}
  const D=W.parts.door;if(D.fl>0&&!D.dead){const q={x:cx,y:cy+WHV_DOOR.y*s},c=xartTint(key,'#ffffff',1);
    if(c){ctx.save();ctx.beginPath();ctx.rect(q.x-WHV_DOOR.w*s/2,q.y-WHV_DOOR.h*s/2,WHV_DOOR.w*s,WHV_DOOR.h*s);ctx.clip();
      ctx.globalAlpha=D.fl*4*alpha;ctx.drawImage(c,cx-pw/2,cy-ph/2,pw,ph);ctx.restore();}}
  for(const id of ['L','R','door']){const p=W.parts[id];whvPartFx(b,whvPartPos(b,id),p.hp/p.max,p.dead,id==='door'?.9:1.15,id==='L'?0:id==='R'?1.7:3.1);}
  ctx.restore();
  for(const e of W.jets)if(e&&!e.dead&&e.y<cy+ph*.55&&typeof drawEnemy==='function'){try{drawEnemy(e);}catch(_de){}}
};
/* One shared beam envelope drives the warning, animation and collision. */
function s67WhvBeamShape(b,B){
  const q=s67WhvMuzzle(b,B.side),u=B.t-B.warn;
  const open=u<0||u>=B.fire?0:clamp(u/.12,0,1)*clamp((B.fire-u)/.18,0,1);
  return {x:q.x,y:q.y,w:B.w*open,open,flare:52,bottom:VH+40};
}
function s67WhvBeamHalf(G,y){const u=clamp((y-G.y)/G.flare,0,1);return G.w*.5*lerp(.05,1,u*u*(3-2*u));}
whvBeamTick1=function(b,dt){
  const W=b._whv,B=W.beam;if(!B)return;
  if(W.parts[B.side].dead||!s67WhvDeployed(W)){W.beam=null;return;}
  B.t+=dt;
  if(B.t<B.warn){combatWarningTick(b,'whvbeam-'+B.side,B.t,B.warn);return;}
  if(!B.sfx){B.sfx=true;whvSfx('laserShot');shake=Math.max(shake,6);}
  const G=s67WhvBeamShape(b,B);
  for(const seat of seatList())withSeat(seat,()=>{
    if(G.open>.04&&player.y>G.y&&player.y<G.bottom&&Math.abs(player.x-G.x)<Math.max(0,s67WhvBeamHalf(G,player.y)-6))playerHit('carrier beam');
  });
  if(B.t>=B.warn+B.fire)W.beam=null;
};
const S67_WHV_SHOTS=whvDrawShots;
whvDrawShots=function(b){
  const W=b._whv,keep=[W.beam,W.beam2];W.beam=null;W.beam2=null;
  try{S67_WHV_SHOTS(b);}finally{W.beam=keep[0];W.beam2=keep[1];}
  for(const B of keep)if(B&&!W.parts[B.side].dead){
    const G=s67WhvBeamShape(b,B);
    if(B.t<B.warn){combatWarningDraw(b,{x:G.x,y:G.y,ex:G.x,ey:G.bottom,progress:B.t/B.warn,width:B.w});continue;}
    if(!G.open)continue;
    const A=MISSION29_ART.beam_lightning,core=tlvImg('tlv_beam');
    if(!core||!XART.rdy(A.key))continue;
    const arc=XART.get(A.key),f=A.frames[Math.floor((b.t||0)*A.fps)%A.frames.length];
    const h=G.bottom-G.y,iw=core.naturalWidth||core.width,ih=core.naturalHeight||core.height;
    ctx.save();ctx.imageSmoothingEnabled=false;
    const strip=(dy,dh)=>{
      const width=s67WhvBeamHalf(G,G.y+dy+dh*.5)*2;
      // Warp the authored plasma into its nozzle; clipping a wide slab made a hard triangle.
      ctx.globalAlpha=.95;
      ctx.drawImage(core,iw*.27,ih*dy/h,iw*.49,ih*dh/h,G.x-width/2,G.y+dy,width,dh);
      ctx.globalAlpha=.24;ctx.globalCompositeOperation='lighter';
      ctx.drawImage(arc,f[0]+A.ink[0],f[1]+A.ink[1]+A.ink[3]*dy/h,A.ink[2],A.ink[3]*dh/h,G.x-width/2,G.y+dy,width,dh);
      ctx.globalCompositeOperation='source-over';
    };
    for(let y=0;y<G.flare;y+=2)strip(y,Math.min(2,G.flare-y));
    strip(G.flare,h-G.flare);
    ctx.restore();
  }
};

/* ---------------------------------------------------------------------------
   J. THE NIGHTWING ACE: LARGER, MODULAR, A LITTLE EASIER
   * 1.5x (WHV_ACE_S .46 -> .69: 92px -> 138px), hit box and lock size with it.
   * Modular: fuselage and both wings are separate plates (cut at the roots, reassembling byte-exact).
     The wings foreshorten into a bank and sweep back on the dash; a hit flashes the module it landed
     on; each wing smokes and burns on its own as the jet is hurt. The authored roll / somersault /
     belly reels still take over for those manoeuvres - a roll is a whole-aircraft motion.
   * Easier, not tamer (Mike: "I like the aggressiveness, but hes a little too hard"): the same moves on
     longer cooldowns - dodge-roll chance .6/.8 -> .45/.6, gun bursts 3 -> 2, missile salvos 2/4/6 ->
     2/3/4 and 7-9.5 s apart, the Hard dash 10-12.5 s apart.
   --------------------------------------------------------------------------- */
const S67_ACE_S=.69,S67_ACE_K=S67_ACE_S/WHV_ACE_S;
const S67_ACE_SPAWN=whvAceSpawn;
whvAceSpawn=function(b){S67_ACE_SPAWN(b);b.w=Math.round(86*S67_ACE_K);b.h=Math.round(88*S67_ACE_K);const A=b._whv.ace;A.fl={body:0,wingL:0,wingR:0};};
const S67_WHV_HIT=warhiveHitTest;
warhiveHitTest=function(b,x,y){
  const W=b._whv;if(!W||W.mode==='carrier'||W.mode==='death'||!W.ace)return S67_WHV_HIT(b,x,y);
  if(b.dead||whvAceInvuln(W.ace))return false;const A=W.ace,dx=x-A.x;
  const hit=Math.abs(dx)<34*S67_ACE_K&&Math.abs(y-A.y)<40*S67_ACE_K;
  if(hit)A._hitMod=Math.abs(dx)<18*S67_ACE_K?'body':(dx<0?'wingL':'wingR');return hit;
};
const S67_WHV_DMG2=warhiveDamage;
warhiveDamage=function(b,dmg){const W=b._whv,A=W&&W.ace;if(A&&W.mode==='ace'){if(!A.fl)A.fl={body:0,wingL:0,wingR:0};A.fl[A._hitMod||'body']=.16;}return S67_WHV_DMG2(b,dmg);};
whvAceDecide=function(b,A,dt){
  const W=b._whv,hard=W.hard;
  if(A.rollCd<=0){for(const s of pBullets){if(s.dead||!(s.vy<0))continue;
    if(s.y>A.y&&s.y-A.y<130&&Math.abs(s.x-A.x)<52){A.rollCd=hard?2.2:3.0;
      if(Math.random()<(hard?.6:.45)){A.roll={t:0,dir:s.x<A.x?1:-1,x0:A.x};whvSfx('dash',.7);}break;}}}
  if(A.somerCd<=0){let threat=(typeof retina!=='undefined'&&retina&&retina.phase==='locked'&&retina.target===b);
    for(const s of pBullets){if(!s.dead&&s.kind==='gmiss'&&dist2(s.x,s.y,A.x,A.y)<150*150){threat=true;break;}}
    if(threat){A.somerCd=hard?5.0:6.5;A.somer={t:0,y0:A.y};whvSfx('dash',.8);return;}}
  if(A.gunCd<=0&&Math.abs(player.x-A.x)<52){A.gunCd=(A.inverted?.85:1.25)/(DIFF.eFire||1);
    if(A.inverted)whvAceGuns(b,A,.22);else{whvAceGuns(b,A,0);A.burst=1;A.burstT=.11;}}
  if(A.burst>0){A.burstT-=dt;if(A.burstT<=0){A.burst--;A.burstT=.11;whvAceGuns(b,A,0);}}
  if(A.mslCd<=0){A.mslCd=rnd(7,9.5)/(DIFF.eFire||1);whvAceFireMissiles(b,(W.fur&&b.hp<=b.maxhp*.5)?4:hard?3:2);}
  if(hard&&A.dashCd<=0&&!A.inverted){A.dashCd=rnd(10,12.5);A.dash={st:'warn',t:0,x0:A.x,y0:A.y};}
  if(A.inverted){A.invSomerCd-=dt;if(A.invSomerCd<=0){A.invSomerCd=rnd(4.5,6);A.somer={t:0,y0:A.y};}}
};
/* the guns sit out on the bigger airframe */
whvAceGuns=function(b,A,spread){
  for(const s of [-1,1]){const a=Math.PI/2+(spread||0)*s;if(typeof eShoot==='function')eShoot(A.x+s*9*S67_ACE_K,A.y+30*S67_ACE_K,a,6.2,'mg');}
  if(spread&&typeof eShoot==='function')eShoot(A.x,A.y+32*S67_ACE_K,Math.PI/2,6.2,'mg');
  whvSfx('enemyShoot',.6);
};
whvDrawAce=function(b){
  const W=b._whv,A=W.ace;if(!A)return;
  const w=200*S67_ACE_S,h=204*S67_ACE_S;
  if(A.dash&&A.dash.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.dash.ex,ey:A.dash.ey,progress:A.dash.t/.95,width:90});
  const P=A.desp;
  if(P&&P.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.x,ey:VH+60,progress:P.t/.8,width:90});
  if(P&&P.st==='cross'&&P.t<P.lead)combatWarningDraw(b,{x:P.x0,y:P.y0,ex:P.x1,ey:P.y1,progress:P.t/P.lead,width:80,fieldOnly:true});
  if(P&&P.st==='cross'&&P.t<P.lead)return;
  if(A.fl)for(const k in A.fl)A.fl[k]=Math.max(0,A.fl[k]-(_lastDt||1/60));
  if((A.dash&&A.dash.st==='go')||(P&&P.st==='cross')){const c=xartPalette('whv_ace','#3a6cff');
    if(c)for(let i=0;i<A.trail.length-1;i+=2){const p=A.trail[i];ctx.save();ctx.globalAlpha=.1+.25*i/A.trail.length;ctx.globalCompositeOperation='lighter';ctx.drawImage(c,p.x-w/2,p.y-h/2,w,h);ctx.restore();}}
  const whole=b.dead||A.somer||A.roll||A.inverted||Math.abs(A.vx)>170||!XART.rdy('whv_acem_body');
  if(whole){const k=b.dead?'whv_ace':whvAceKey(b,A);whvSprite(k,A.x,A.y,w,h,b.dead?(A.spin||0):0,1);
    if(b.flash>0&&!b.dead){const c=xartTint(k,'#ffffff',1);if(c){ctx.save();ctx.translate(A.x,A.y);ctx.globalAlpha=Math.min(1,b.flash*9);ctx.imageSmoothingEnabled=false;ctx.drawImage(c,-w/2,-h/2,w,h);ctx.restore();}}}
  else{
    const dmg=b.hp/b.maxhp<.5?'_dmg':'',bank=clamp(A.vx/170,-1,1),sweep=A.dash&&A.dash.st==='go'?.14:0;
    const root={wingL:{x:(63-100)*S67_ACE_S,s:1-Math.max(0,-bank)*.30},wingR:{x:(137-100)*S67_ACE_S,s:1-Math.max(0,bank)*.30}};
    for(const m of ['wingL','body','wingR']){const fresh='gp4_acem_'+m+dmg,key=XART._src[fresh]?fresh:'whv_acem_'+m+dmg;if(!XART.rdy(key))continue;const im=XART.get(key);
      ctx.save();ctx.translate(A.x,A.y);ctx.imageSmoothingEnabled=false;
      if(m!=='body'){const R=root[m];ctx.translate(R.x,0);ctx.rotate((m==='wingL'?1:-1)*sweep);ctx.scale(R.s,1);ctx.translate(-R.x,0);}
      ctx.drawImage(im,-w/2,-h/2,w,h);
      const fl=A.fl?A.fl[m]:0;
      if(fl>0||b.flash>0){const c=xartTint(key,'#ffffff',1);if(c){ctx.globalAlpha=Math.min(1,Math.max(fl||0,b.flash||0)*9);ctx.drawImage(c,-w/2,-h/2,w,h);}}
      ctx.restore();}
  }
  if(!b.dead&&!A.inverted&&!A.somer){const f=(Math.floor((b.t||0)*14))%8,c=xartPalette('florb_'+f,'#5a8cff'),d=(12+Math.sin((b.t||0)*30)*2)*S67_ACE_K;
    if(c)for(const s of [-1,1]){ctx.save();ctx.globalAlpha=.8;ctx.globalCompositeOperation='lighter';ctx.drawImage(c,A.x+s*10*S67_ACE_K-d/2,A.y-h*.43-d/2,d,d);ctx.restore();}}
  if(!b.dead){const r=b.hp/b.maxhp;whvPartFx(b,{x:A.x-40*S67_ACE_K,y:A.y},r,false,.8,5);whvPartFx(b,{x:A.x+40*S67_ACE_K,y:A.y},Math.min(1,r*1.15),false,.8,6.3);}
};
