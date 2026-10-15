"use strict";
/* Mike's complete 37:47 October 10 part-two review. Each correction has one
   physical owner; previews exercise the same weapons, emitters and art. */
const P2={events:[],preview:false,base:{intercept:enemyOrdnanceCanIntercept,
 element:enemyOrdnanceElement,shoot:pShoot,preview:forgePreviewSwap,previewTick:forgePreviewTick,
 frame:projectileVisualFrame,drawBullets:drawBullets,orb:playerOrbTick,spawn:spawnEnemy,
 world:drawWorld,play:updatePlay,begin:beginStage,load:stageLoadBegin,shield:drawShield,
 tint:dialogueNameColor,dialogue:dlgBox,frameDraw:dialogueFrameDraw,frameArt:dialogueFrame,tune:ovAttackTune,
 flight:ap10StealthDraw,wing:s6WingTick,quick:gp4QuickEncounter},hulls:new Map(),draws:{}};
function p2Log(event,data={}){P2.events.push({event,...data});if(P2.events.length>160)P2.events.shift();}
for(const bank of Object.values(P2_ART))for(const a of bank)XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){const banks=[...P2_ART.shield,...P2_ART.atom,...AF10_ART.fire_ring,...AF10_ART.electric_ring,...(n===2||n===3?[...P2_ART.fire,...P2_ART.fire_root]:[]),...(n===6?[...P2_ART.jace,...P2_ART.stealth]:[])];
 banks.push(...P2_ART.maverick,...P2_ART.maverick_full,...(n===2||n===3?P2_ART.fire_tip:[]),...(n===6?[...P2_ART.stealth_roll,...P2_ART.stealth_somer]:[]));
 return P2.base.load.call(this,n,[...(keys||[]),...banks.map(a=>a.key)]);};
const P2_FIRE_BEAM=av3Beam,P2_FIRE_MUZZLE=av3Muzzle;
function p2FireColor(c){return c===0||/fire|flame|magma|inferno|orange/i.test(String(c));}
function p2FireReady(){return P2_ART.fire.map(a=>XART.rdy(a.key)).every(Boolean);}
function p2FireMuzzle(g,x,y,size,t,alpha=1){const a=P2_ART.fire[Math.floor(Math.max(0,t)*32)%32],k=size/192;
 if(!XART.rdy(a.key))return false;g.save();g.imageSmoothingEnabled=false;g.globalAlpha*=alpha;
 g.drawImage(XART.get(a.key),...a.muzzle_rect,x-96*k,y-62*k,192*k,148*k);g.restore();P2.draws.fireMuzzle=(P2.draws.fireMuzzle||0)+1;return true;
}
function p2FireProfile(width,length){return {root:Math.min(16,width*.11),half:width*.75,depth:Math.min(length,24+Math.min(106,width*.54))};}
av3Muzzle=function(g,x,y,size,color,t=AV3.clock,alpha=1){
 if(p2FireColor(color)&&p2FireReady())return p2FireMuzzle(g,x,y,size,t,alpha);
 return P2_FIRE_MUZZLE.apply(this,arguments);
};
av3Beam=function(g,x,y,angle,length,width,color,t=AV3.clock,alpha=1,muzzle=true){
 if(![x,y,angle,length,width].every(Number.isFinite)||length<=0||width<.5)return false;
 if(!p2FireColor(color)||!p2FireReady())return P2_FIRE_BEAM.apply(this,arguments);
 const painted=p2RenderFireColumn(g,P2_ART,key=>XART.rdy(key)?XART.get(key):null,x,y,angle,length,width,t,alpha,muzzle);
 if(!painted)return P2_FIRE_BEAM.apply(this,arguments);
 for(const [part,draws]of Object.entries(painted)){const key='fire'+part[0].toUpperCase()+part.slice(1);P2.draws[key]=(P2.draws[key]||0)+draws;}
 P2.draws.fireBeam=(P2.draws.fireBeam||0)+1;return true;
};
const P2_JACE_BALL=rs1004Ball;
rs1004Ball=function(x,y,size,t){const a=P2_ART.jace[Math.floor(Math.max(0,t)*32)%32];
 if(!XART.rdy(a.key))return P2_JACE_BALL.apply(this,arguments);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),x-size/2,y-size/2,size,size);ctx.restore();
 P2.draws.jace=(P2.draws.jace||0)+1;return true;
};
// Ordinary pellets are never ordnance. Elemental coloring must not turn a
// boat's MG or Rook's slug into a fireball that can be erased by spread fire.
function p2Pellet(q){return !!q&&(q.mg||/mg|tracer|pellet|slug|bullet|needle/i.test(q.kind||'')&&!/missile|rocket/.test(q.kind||''));}
enemyOrdnanceElement=function(q){return p2Pellet(q)?null:P2.base.element.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return !p2Pellet(q)&&P2.base.intercept.apply(this,arguments);};
WEAPON_CADENCE[0]=WEAPON_CADENCE[1]=.102; // Retain their shared per-level/pilot cadence.
// Atomic targeting owns the trigger until its launch/impact finishes. Holding
// fire through that sequence must not also spray a normal machine gun.
pShoot=function(){if((specialActive('lizzie')||specialActive('cole'))&&atomBooms.some(b=>b.t<b.dur))return;
 return P2.base.shoot.apply(this,arguments);};
ovAttackTune=function(){const t={...P2.base.tune.apply(this,arguments)};if(diffKey==='furious'){t.legs=6;t.lock=Math.max(t.lock,.60);}return t;};
// Previews previously inherited Stage 5's space hull/held fusion, and didn't
// advance the held laser age. These fields are scoped; the live run is restored.
forgePreviewSwap=function(P,w,h,fn){const old=P2.preview,bursts=P2.orbBursts;P2.preview=true;P2.orbBursts=P._p2Bursts||[];
 try{return P2.base.preview.call(this,P,w,h,()=>{
  if(P.space==null){run.stage=1;run.spaceMode=false;run._spaceShadowHeld=false;run._spaceShadowCharge=0;
   run._spaceShadowReady=false;run._spaceShadowCooldown=0;run.gravityShipReady=false;
   player._fuse=0;player._chgOn=false;player._orbCd=0;player._p2Preview=true;}
  fn();
 });}finally{P._p2Bursts=P2.orbBursts;P2.orbBursts=bursts;P2.preview=old;}
};
forgePreviewTick=function(P,w,h,dt){const r=P2.base.previewTick.apply(this,arguments);
 for(const b of P?.bullets||[])if(b.kind==='beam')b._bt=(b._bt||0)+Math.min(.05,dt);
 return r;};
projectileVisualFrame=function(b,fps,n){
 // The spread reel changes its visible center/extent between cells. A flying
 // pellet keeps the approved neutral image; its muzzle still plays every pose.
 if(b?.kind==='spread')return 0;
 return P2.base.frame.apply(this,arguments);
};
drawBullets=function(){
 const all=pBullets,ice=all.filter(b=>b.kind==='beam'&&!b.dead&&(b._inf==='ice'||b._inf==='fireice'));
 const ready=ice.length&&AP10_FX_ART.ice_laser.every(a=>XART.rdy(a.key));
 if(ready)pBullets=all.filter(b=>!ice.includes(b));
 try{P2.base.drawBullets.apply(this,arguments);}finally{pBullets=all;}
 for(const b of ready?ice:[]){const top=b.top??PLAY.y,bot=b.bot??player.y-14;
  av3Beam(ctx,b.x,bot,-Math.PI/2,Math.max(0,bot-top),Math.max(8,b.w||18),'ice',b._bt||b.t||0);
  P2.draws.ice=(P2.draws.ice||0)+1;
 }
 p2DrawOrbBursts();
};
// The personal shield is fitted to actual opaque hull pixels, not the padded
// square atlas cell. Nine generated hull-shaped shells remain independently colored.
function p2Hull(pk){if(P2.hulls.has(pk))return P2.hulls.get(pk);const key='ship_'+pk;if(!XART.rdy(key))return null;
 const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;
 const g=c.getContext('2d');g.drawImage(im,0,0);const p=g.getImageData(0,0,c.width,c.height).data;
 let l=c.width,t=c.height,r=0,b=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(p[(y*c.width+x)*4+3]>80){l=Math.min(l,x);r=Math.max(r,x+1);t=Math.min(t,y);b=Math.max(b,y+1);}
 const h={w:r-l,h:b-t,x:(l+r)/2-im.width/2,y:(t+b)/2-im.height/2,sourceH:im.height};P2.hulls.set(pk,h);return h;
}
const P2_HUD_ICONS=new Map();
function p2HudWeaponIcon(g,key,x,y,height){
 if(!key)return;let im=P2_HUD_ICONS.get(key);
 if(!im){const c=document.createElement('canvas');c.width=c.height=160;const q=c.getContext('2d');
  if(!iconBlit(q,key,80,80,80,true))return;
  let d;try{d=q.getImageData(0,0,160,160).data;}catch(_){return ph8Icon(g,key,x,y,height);}
  let l=160,t=160,r=0,b=0;for(let yy=0;yy<160;yy++)for(let xx=0;xx<160;xx++)if(d[(yy*160+xx)*4+3]>80){l=Math.min(l,xx);r=Math.max(r,xx+1);t=Math.min(t,yy);b=Math.max(b,yy+1);}
  if(r<=l||b<=t)return ph8Icon(g,key,x,y,height);
  im={canvas:c,rect:[l,t,r-l,b-t]};P2_HUD_ICONS.set(key,im);
 }
 const s=Math.min(height/im.rect[3],38/im.rect[2]),w=im.rect[2]*s,h=im.rect[3]*s;
 g.save();g.imageSmoothingEnabled=false;g.drawImage(im.canvas,...im.rect,x-w/2,y-h/2,w,h);g.restore();
}
function p2DrawShell(pk,x,y,alpha=1){const a=P2_ART.shield.find(a=>a.key==='p2_shield_'+pk),h=p2Hull(pk);
 if(!a||!h||!XART.rdy(a.key))return false;
 // The shell's opaque rim surrounds an empty aperture, which occupies about
 // two thirds of the plate. Fit that opening around the hull, with clearance.
 const k=SHIP_DRAW_H/h.sourceH,w=h.w*k*1.85,height=h.h*k*1.65,cx=x+h.x*k,cy=y+h.y*k;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=alpha*(.85+.07*Math.sin(efxClock*12));
 ctx.drawImage(XART.get(a.key),cx-w/2,cy-height/2,w,height);ctx.restore();P2.draws.shield=(P2.draws.shield||0)+1;return true;
}
drawShield=function(x,y){if(run.shield<=0)return;
 if(spaceShipActive()||!p2DrawShell(_pilotKey(),x,y))return P2.base.shield.apply(this,arguments);
};
const P2_RESCUE_FRIENDLY=rg4Friendly;
rg4Friendly=function(m,G){const r=P2_RESCUE_FRIENDLY.apply(this,arguments),C=G.scene;
 if(C?.kind==='rescue'&&C.castAt!=null&&G.members){
  const alpha=clamp((C.age-C.castAt)/.6,0,1)*(1-clamp(G.cloak||0,0,1));
  if(alpha>0)p2DrawShell(m.key,m.ref.x,m.ref.y,alpha);
 }return r;
};
const P2_COLORS={lizzie:'#ffd438',nyx:'#b073ff',kaia:'#25d9bd',jace:'#ff4838',decker:'#ff9b30',rook:'#ff9b30',voss:'#ff244b'};
Object.assign(RETINA_TINTS,P2_COLORS);
const P2_BOSS_RETINA=drawBossRetina;
drawBossRetina=function(t,x,y,spin,alpha){const pk=_pilotKey(),col=P2_COLORS[pk],key='nbret_'+pk;
 if(!col||!XART.rdy(key))return P2_BOSS_RETINA.apply(this,arguments);
 const im=xartPalette(key,col)||XART.get(key);ctx.save();ctx.globalAlpha=alpha==null?.95:alpha;
 ctx.translate(x,y);ctx.rotate(spin||0);ctx.shadowColor=col;ctx.shadowBlur=12;ctx.drawImage(im,-29,-29,58,58);ctx.restore();return true;
};
dialogueNameColor=function(who,fallback){return P2_COLORS[String(who||'').toLowerCase()]||P2.base.tint.apply(this,arguments);};
dlgBox=function(o){return P2.base.dialogue.call(this,{...o,tint:dialogueNameColor(o.who,o.tint)});};
// Retint the authored frame itself: passing a tint was previously ignored by
// the cached yellow master, so Rebel and ally radios all had yellow borders.
const P2_FRAMES=new Map();
dialogueFrameDraw=function(who,tint,x,y,w,h){
 const col=dialogueNameColor(who,tint),key=String(who)+'|'+col;let im=P2_FRAMES.get(key);
 if(!im){const source=P2.base.frameArt.call(this,who,col);if(!source)return false;
  im=document.createElement('canvas');im.width=source.width;im.height=source.height;
  const g=im.getContext('2d');g.drawImage(source,0,0);let D;try{D=g.getImageData(0,0,im.width,im.height);}catch(_){return P2.base.frameDraw.apply(this,arguments);}const p=D.data;
  const c=hx(col),peak=Math.max(c[0],c[1],c[2]);
  for(let yy=0;yy<im.height;yy++)for(let xx=0;xx<im.width;xx++){
   if(xx>im.width*.07&&xx<im.width*.93&&yy>im.height*.12&&yy<im.height*.88)continue;
   const i=(yy*im.width+xx)*4,max=Math.max(p[i],p[i+1],p[i+2]),min=Math.min(p[i],p[i+1],p[i+2]);
   if(p[i+3]&&max-min>24){const light=max/Math.max(1,peak);p[i]=c[0]*light;p[i+1]=c[1]*light;p[i+2]=c[2]*light;}
  }
  g.putImageData(D,0,0);P2_FRAMES.set(key,im);
 }
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x,y,w,h);ctx.restore();return true;
};
// Allies accompany the approach and Rebel fight. Only the Harrier is solo.
// Keep the approach controller running: it owns the route choice and progress.
s6WingTick=function(dt){if(run.stage===6&&boss?._whv&&!AP10_X.intro){if(s6Wing){s6Wing.ships=[];s6Wing.line=null;}return;}
 return P2.base.wing.apply(this,arguments);};
gp4QuickEncounter=function(){const r=P2.base.quick.apply(this,arguments);if(boss?._whv&&s6Wing)s6Wing.ships=[];return r;};
// The old campaign card described a storm platform for both pursuit branches.
// Rebel dialogue belongs to its own stolen-tech intro; weather chatter belongs
// to the Harrier pursuit and must not announce imaginary control anchors.
const P2_STORY=storyPlay,P2_STAGE_CARD=arcStageCard;
function p2Pursuit(){return boss?._rebels?'right':boss?._whv?'left':s6Wing?.route||GP4.route;}
storyPlay=function(n,scene){if(n===6&&scene==='boss'){
 const route=p2Pursuit();if(route==='right'){if(story?.key==='S06.boss')story=null;return false;}
 if(route==='left'){
  const rows=[['DECKER','THE HARRIER CANNON BANKS ARE CHARGING. WATCH THEIR FIRING LANES.'],
   ['YURI','THE LIGHTNING FIELD IS BUILDING BEHIND THE HARRIER. KEEP MOVING.'],['COLE','CLOSE ON THE HARRIER. WE CANNOT LET IT ESCAPE.']];
  story={key:'P2.S06.HARRIER',when:'combat',lines:rows.filter(q=>!storySpeakerIsPlayer(q[0])),i:0,t:0,typed:0,done:false,fade:1};return true;
 }}return P2_STORY.apply(this,arguments);};
arcStageCard=function(n,which){if(n===6&&which==='boss_warning'){
 const route=p2Pursuit();if(route==='right')return ['REBEL FURY SQUADRON','FIVE HOSTILE FIGHTERS. STOLEN FURY TECHNOLOGY.'];
 if(route==='left')return ['HARRIER PURSUIT','DESTROY THE CANNON BANKS. WATCH FOR THE ELITE FIGHTER.'];
 }return P2_STAGE_CARD.apply(this,arguments);};
const P2_STEALTH=new Map(P2_ART.stealth.map(a=>[a.role+'|'+a.pose,a]));
ap10StealthDraw=function(e){
 if(run.stage!==6||e.dead||e._dyingT!=null||!AP10_AIR_TYPES.has(e.type)&&!e._mission29&&!e._fb2Stealth&&!e._s6Strike)return false;
 if(on5Bomber(e)){e._fb2Stealth??={};
  if(!['blue','red','green','orange'].includes(e._fb2Stealth.role))e._fb2Stealth.role=(e._mission29?fb2MissionRole(e._mission29):null)||((e._side??e._dir??1)>0?'red':'green');
  e._fb2Stealth.direction=e._fb2Stealth.direction||e._s6Strike?.direction||'south';}
 const A=e._fb2Stealth||e._mission29||e._s6Strike||{},dir=A.direction||'south';
 const role=e._fb2Stealth?.role||(e._mission29?fb2MissionRole(A):null)||'blue';
 const pose=e.hp/e.maxhp<.5?'damaged':'idle',a=p2StealthActorPose(e,role,A)||P2_STEALTH.get(role+'|'+pose);
 if(!a||!XART.rdy(a.key))return P2.base.flight.apply(this,arguments);
 const size=e._s67Draw||((e._mission29||e._fb2Stealth)?104:Math.max(64,e._drawH||e.h||64));
 const angle=dir==='east'?-Math.PI/2:dir==='west'?Math.PI/2:dir==='north'?Math.PI:0;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(e.x,e.y);ctx.rotate(angle);
 const im=e.flash>0?xartTint(a.key,hitFlashColor(e),.84):XART.get(a.key);
 ctx.drawImage(im||XART.get(a.key),-size/2,-size/2,size,size);ctx.restore();
 e._p2StealthKey=a.key;e._sm10Facing=dir;e._ap10Palette=role;e._drawW=e._drawH=size;return true;
};
beginStage=function(n){P2.events=[];P2.hulls.clear();P2.orbBursts=[];return P2.base.begin.apply(this,arguments);};
// Launched orbs commit to their own flight, rather than following a moving
// target/player column. Their shards and collision blasts keep their element.
fb10Steer=function(b,dt){if(!b._p2Flight){b._p2Flight={vx:b.vx||0,vy:b.vy||-3.2};p2Log('orb-launched',{x:b.x,y:b.y,element:fb10Kind(b)});}b.vx=b._p2Flight.vx;};
// Contact bursts use the approved thirty-two-pose arcade rings. The live orb
// still owns damage, shrapnel and elemental riders; this reel owns its visible
// shock front, anchored to the exact contact rather than following the ship.
P2.orbBursts=[];
const P2_ORB_BLAST=fb10Blast;
fb10Blast=function(b,x,y,why){const fresh=!b._fb10Ended,k=fb10Kind(b),r=P2_ORB_BLAST.apply(this,arguments);
 if(fresh&&['fire','magma','kinetic'].includes(k)){
  const f={x,y,at:efxClock,life:k==='kinetic'?.8:1.0,bank:k==='kinetic'?'electric_ring':'fire_ring',size:Math.min(250,fb10Init(b).r*2)};
  P2.orbBursts.push(f);if(P2.orbBursts.length>12)P2.orbBursts.shift();
  p2Log('orb-impact',{element:k,x,y,radius:fb10Init(b).r,reason:why});
 }return r;
};
function p2DrawOrbBursts(){P2.orbBursts=P2.orbBursts.filter(f=>efxClock-f.at<f.life);
 for(const f of P2.orbBursts){ctx.save();ctx.globalAlpha=1;
  if(af10Cell(f.bank,Math.max(0,efxClock-f.at),f.life,f.x,f.y,f.size))P2.draws.orbBurst=(P2.draws.orbBurst||0)+1;
  ctx.restore();}
}
// One continuous32-pose cloud owns the strike. Its last wisps fade gently
// before removal; the ground contact never changes with the billowing cap.
drawAtomBooms=function(){
 for(const b of [...atomBooms,...s67Nukes]){const p=clamp(b.t/b.dur,0,1),a=P2_ART.atom[Math.min(31,Math.floor(p*32))];
  if(!XART.rdy(a.key))continue;const w=b.w||384,k=w/a.w;
  ctx.save();ctx.globalAlpha=p>.875?clamp((1-p)/.125,0,1):1;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),b.x-a.pivot[0]*k,b.y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
  P2.draws.atom=(P2.draws.atom||0)+1;
 }
 if(atomFlash>0){ctx.save();ctx.globalAlpha=clamp(atomFlash,0,1);ctx.fillStyle='#fff';ctx.fillRect(-64,viewFillY()-64,worldWidth()+128,VH-viewFillY()+128);ctx.restore();}
};
// Give the urgent rounds enough contrast and room to read while retaining the
// predictive time-to-impact test and all original projectile hit boxes.
pw5Collect=function(){PW5.threats=[];if(state!==GS.PLAY||run.stage<6)return;pw5Warm();
 const W=boss?._whv,G=boss?._rebels?.gang1004,rounds=eBullets.filter(p=>!p.dead).map(p=>[p,60]);
 for(const p of W?.shots||[])rounds.push([p,60]);for(const p of G?.ord||[])if(p.kind!=='helper')rounds.push([p,1]);
 for(const seat of seatList())withSeat(seat,()=>{const found=rounds.map(([p,s])=>pw5Impact(p,player,s)).filter(Boolean).sort((a,b)=>a.t-b.t);
  for(const q of found.slice(0,4))if(!PW5.threats.some(v=>v.p===q.p))PW5.threats.push({...q,seat});});
};
pw5Draw=function(){for(const q of PW5.threats){const p=q.p;if(p.dead)continue;const urgent=q.t<.30,key='bmfx_alert_'+(urgent?'red':'yellow')+'_impact_imminent';
 if(XART.rdy(key)){const size=urgent?26:21;ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=.88+.12*Math.sin(efxClock*(urgent?22:14));
 ctx.drawImage(XART.get(key),p.x-size/2,p.y-size/2,size,size);ctx.restore();PW5.draws++;}}
};

// The equipment strip does not belong underneath the full-screen debrief.
const P2_HUD_STATE=_hudStateWants;
_hudStateWants=function(s){return s===GS.STAGECLEAR?false:P2_HUD_STATE.apply(this,arguments);};
