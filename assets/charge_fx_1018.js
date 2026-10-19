"use strict";
/* 1018 - Mike: "now fix the animations when falva or maverick or jace charge and release their attacks"

   Filmed first (_BUILD_SOURCE/probe_charge_film_1018.py), and what was wrong:
   - RELEASE (Falva, Maverick): releaseRoller / releaseHelix called explode() on the ship's own nose. That is the
     orange nx_small fireball every destroyed unit uses, so letting go of a charge looked like taking a hit, and it
     sat burning where the nose WAS for about a second while the ship moved away.
   - MAVERICK'S CHARGE RING: shipChargeDraw drew fchgc_, meant to be a blue/teal palette swap of Falva's pink ring -
     but those four cells are byte-identical to fchg_, so he charged in Falva's pink, which under 'lighter' over his
     teal hull read as a white haze swallowing the ship. And the ring animated on performance.now(), not the game clock.
   - JACE: two charge balls at once (the arsenal's small swirl at +42 px and the showcase's molten ball at +52 px), the
     molten ball grew to 104 px AROUND a point inside his hull, so it covered half the ship; and on release the ball
     turned into a different, green swirl sprite (rg4OrdnanceDraw drew nhxsb_g) - the shot he charged was not the shot
     that left him.

   Now:
   - The ring is the pilot's own colour (Maverick's through xartPalette, which keeps the art's luminance), steps its
     authored frames with the charge and flickers to the next frame as it builds - pixel steps on efxClock, drawn at
     whole pixels, no rotation.
   - Release is the charge ring SNAPPING OUT: the full ring in the pilot's colour, four hard scale steps outward in a
     quarter second, riding the ship. No fireball. The white pop, shake, shards and text stay.
   - Jace charges ONE molten ball, seated in front of his nose so it grows away from the hull, and the ball that
     leaves him is that same molten ball (and so are its nova fragments). */
const CFX18={release:[],base:{ring:shipChargeDraw,roller:releaseRoller,helix:releaseHelix,player:drawPlayer,
 jaceShip:fr27RebelDrawShip,ord:rg4OrdnanceDraw,proj:drawCombatFinalProjectile},draws:{ring:0,release:0,jace:0,ord:0}};
const CFX18_TINT={maverick:'#36d9c4'};    // Falva and Cole keep the ring's own authored colour
function cfx18Ring(i,pilot){const key='fchg_'+i;if(!XART.rdy(key))return null;const c=CFX18_TINT[pilot];return c?(xartPalette(key,c)||XART.get(key)):XART.get(key);}
function cfx18Clock(){return typeof efxClock==='number'?efxClock:performance.now()/1000;}

shipChargeDraw=function(k,x,y,w,h,pilot){
 if(!XART.rdy('fchg_0'))return CFX18.base.ring.apply(this,arguments);
 const t=cfx18Clock(),kk=clamp(k,0,1),full=kk>=.999;
 // build: frames 1..3 track the charge; between steps the ring flickers up to the next frame, more often as it fills
 let fi;
 if(full)fi=2+(Math.floor(t*11)&1);
 else{const s=1+kk*2,base=Math.floor(s),frac=s-base;fi=Math.min(3,base+((Math.floor(t*14)%5)/5<frac?1:0));}
 const im=cfx18Ring(fi,pilot);if(!im)return CFX18.base.ring.apply(this,arguments);
 const step=full?(Math.floor(t*8)&1)*.04:0;                  // a two-step pixel pulse at full, not a smooth breathe
 // SIZED FROM THE DRAWN HULL, not the hitbox: w/h here are the 24x30 hit box, which made a ring the size of the jet
 // that sat ON the hull (Falva's pink-on-pink vanished). The ring is traced round the ship's own ink box instead.
 const H=typeof ps18HullInk==='function'&&pilot!=='cole'?ps18HullInk(pilot):null;
 const cx=H?x+H.cx:x,cy=H?y+H.cy:y,bw=H?H.w*1.55:w*2.05,bh=H?H.h*1.42:h*1.75;
 const dw=Math.round(bw*(1+step)),dh=Math.round(bh*(1+step));
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalCompositeOperation='lighter';
 ctx.globalAlpha=full?(Math.floor(t*16)&1?.95:.78):.55+.40*kk;
 ctx.drawImage(im,Math.round(cx-dw/2),Math.round(cy-dh/2),dw,dh);ctx.restore();CFX18.draws.ring++;CFX18.lastRing={pilot,w:dw,h:dh,cx:Math.round(cx),cy:Math.round(cy)};return true;
};
// A release never fires the generic fireball at the ship's own nose; it snaps the charge ring out instead.
function cfx18NoNoseFire(fn){const ex=explode;explode=function(x,y){if(Math.abs(x-player.x)<30&&Math.abs(y-player.y)<40)return;return ex.apply(this,arguments);};
 try{return fn();}finally{explode=ex;}}
function cfx18Release(pilot,full){CFX18.release.push({pilot,full:!!full,t:0,seat:typeof _seat!=='undefined'?_seat:1});CFX18.release=CFX18.release.slice(-6);}
releaseRoller=function(charge){const a=arguments;const r=cfx18NoNoseFire(()=>CFX18.base.roller.apply(this,a));cfx18Release('falva',charge>=FALVA_FULL-.02);return r;};
releaseHelix=function(charge){const a=arguments;
 const r=cfx18NoNoseFire(()=>CFX18.base.helix.apply(this,a));
 const b=pBullets.at(-1);cfx18Release('maverick',!!(b&&b._full));return r;};
const CFX18_SNAP=[[1.00,1.00],[1.25,.86],[1.55,.62],[1.90,.36],[2.25,.16]];   // [scale, alpha] - hard steps
drawPlayer=function(){const r=CFX18.base.player.apply(this,arguments);
 const seat=typeof _seat!=='undefined'?_seat:1,dt=1/60;
 for(const R of CFX18.release){if(R.seat!==seat||R.t>=.25)continue;
  const s=CFX18_SNAP[Math.min(4,Math.floor(R.t/.05))],im=cfx18Ring(3,R.pilot);
  if(im&&!player.dead){const H=typeof ps18HullInk==='function'?ps18HullInk(R.pilot):null,k=s[0]*(R.full?1.15:1);
   const w=(H?H.w*1.55:player.w*2.05)*k,h=(H?H.h*1.42:player.h*1.75)*k,cx=player.x+(H?H.cx:0),cy=player.y+(H?H.cy:0);
   ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalCompositeOperation='lighter';ctx.globalAlpha=s[1];
   ctx.drawImage(im,Math.round(cx-w/2),Math.round(cy-h/2),Math.round(w),Math.round(h));ctx.restore();CFX18.draws.release++;}
 }
 return r;};
// the release clock runs on the game clock (paused game, paused burst)
const CFX18_EFFECTS=updateEffects;
updateEffects=function(dt){const r=CFX18_EFFECTS.apply(this,arguments);for(const R of CFX18.release)R.t+=dt||0;CFX18.release=CFX18.release.filter(R=>R.t<.3);return r;};

// ---- Jace: one molten ball, in front of his nose, and the same ball after release ----
const CFX18_JACE_LEAD=40;     // his nose sits ~40 px below his centre (he flies south)
fr27RebelDrawShip=function(q){const A=q.rg4?.act;
 if(!(A?.kind==='helix'&&A.phase==='charge'))return CFX18.base.jaceShip.apply(this,arguments);
 const ball=rs1004Ball,pal=ra4Palette,calls=[];
 rs1004Ball=function(x,y,s,t){calls.push([x,s,t]);return true;};
 ra4Palette=function(k){return /^nhxsb_/.test(k)?null:pal.apply(this,arguments);};   // the arsenal's small swirl ball is not drawn
 let r;try{r=CFX18.base.jaceShip.apply(this,arguments);}finally{rs1004Ball=ball;ra4Palette=pal;}
 for(const c of calls){ball(c[0],q.y+CFX18_JACE_LEAD+c[1]*.46,c[1],c[2]);CFX18.draws.jace++;}
 return r;};
rg4OrdnanceDraw=function(o,G){if(o.kind!=='helix'||!o._rsFullBall)return CFX18.base.ord.apply(this,arguments);
 const s=o.r*2.25;rs1004Ball(o.x,o.y,s,(o.t||0)+2);CFX18.draws.ord++;
 if(o.flash>0){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=Math.min(.8,o.flash*6);rs1004Ball(o.x,o.y,s,(o.t||0)+2);ctx.restore();}};
drawCombatFinalProjectile=function(p){if(p._ra4MiniBall){rs1004Ball(p.x,p.y,19,(p.t||0)+1);return true;}return CFX18.base.proj.apply(this,arguments);};
/* MAVERICK'S WHITE HAZE was drawMavCoilUnder: a pale nchg_sph sphere 52-106 px wide under his hull, additive, under a
   8-26 px shadowBlur - the "circle orb surrounding the ship" Mike retired for the traced ring in 0801bs, still drawn
   underneath it. The traced ring (his teal, above) and the helix ball forming at his nose carry the charge now. */
drawMavCoilUnder=function(){};
/* FALVA'S RING WAS UNDER HER HULL. drawFalvaAura runs before drawPlayer, so the traced ring sat beneath a pink hull of
   the same pink and only its outermost dots showed - the charge read as nothing happening. Maverick's ring is drawn
   over his hull (drawMavCoilOver); hers now is too, from drawFalvaOrbs, which already runs after drawPlayer. */
const CFX18_FALVA={aura:drawFalvaAura,orbs:drawFalvaOrbs};
drawFalvaAura=function(){};
drawFalvaOrbs=function(){const p=_falvaP();
 if(p>=0)shipChargeDraw(Math.min(p,1),player.x,player.y,player.w,player.h,'falva');
 return CFX18_FALVA.orbs.apply(this,arguments);};
drawFalvaCharge=function(){};   // drew the same ring a second time under the hull (game.js 74381); drawn once, over it, above
