"use strict";
/* Production art wiring and bounded glyph caching. No change to font design. */
for(const a of Object.values(REPAIR30_ART))XART._src[a.key]=a.path;
function repair30Cell(name,t,x,y,w,h,ink,palette){
 const a=REPAIR30_ART[name];if(!a||!XART.rdy(a.key))return false;
 const r=a.frames[((Math.floor(t*a.fps)%a.frames.length)+a.frames.length)%a.frames.length];
 const q=ink&&a.ink?a.ink:[0,0,r[2],r[3]],im=palette?xartPalette(a.key,palette):XART.get(a.key);if(!im)return false;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,r[0]+q[0],r[1]+q[1],q[2],q[3],x-w/2,y-h/2,w,h);ctx.restore();return true;
}
drawShield=function(x,y){
 if(!(run.shield>0))return;
 const space=spaceShipActive(),key=typeof _shipFrameKey==='function'?_shipFrameKey(_pilotKey()):null;
 const im=key&&XART.rdy(key)?XART.get(key):null;
 const hullH=space?SPACE_SHIP_SIZE:SHIP_DRAW_H,hullW=space?hullH*.9:im?hullH*(im.naturalWidth||im.width)/(im.naturalHeight||im.height):44;
 const w=hullW*1.20,h=hullH*1.23;
 ctx.save();ctx.globalAlpha=.62+.06*Math.min(5,run.shield);repair30Cell('shield',efxClock,x,y,w,h,true);ctx.restore();
};
// Full-face pickup art rotates in the screen plane; never choose edge-on/back
// frames from the old broadside turning strips.
pickupTurnFrame=function(key,x,y,h,t,frames){
 frames=frames||12;if(!XART.rdy(key))return false;
 const im=XART.get(key),fw=(im.naturalWidth||im.width)/frames,fh=im.naturalHeight||im.height,w=h*fw/fh;
 ctx.save();ctx.translate(Math.round(x),Math.round(y));ctx.rotate((t||0)*1.3);ctx.imageSmoothingEnabled=false;
 lateShadowImage(ctx,im,0,0,fw,fh,-w/2,-h/2,w,h);ctx.restore();return true;
};
function repair30OrbDraw(b){
 if(b.kind!=='orb'||b._ts||(b._el==='dark'&&(b._voidAge||0)>.52))return false;
 const el=b._inf||b._el||(b._wvar==='toxicorb'?'toxic':b._fire||b._wvar==='magmaorb'?'fire':'ice');
 ctx.save();ctx.translate(b.x,b.y);ctx.rotate(b.spin||0);
 const s=(b.w||18)*1.9,r=repair30Cell('orb_'+el,b.t||0,0,0,s,s,true);ctx.restore();return r;
}
const REPAIR30_FLAME=flameDraw;
flameDraw=function(b){
 // Standard fire, ice-breath and named thermoshock keep their dedicated owner.
 // The remaining infused streams use their authored element reel.
 if(b._inf&&!['fire','ice'].includes(b._inf)){
  const top=b.top==null?Math.max(PLAY.y,(b.y||player.y)-(b.h||100)):b.top,bot=b.bot==null?b.y:b.bot;
  if(bot>top&&repair30Cell('cast_'+b._inf,b.anim||efxClock,b.x,(top+bot)/2,Math.max(20,b.w||32),bot-top,true))return;
 }return REPAIR30_FLAME(b);
};
chaingunRoundDraw=function(b){
 const lv=clamp(b.lv||1,1,5),col=wlvGlow(lv),name=b._inf?'chaingun_round_'+b._inf:'chaingun_round';
 ctx.save();ctx.translate(b.x,b.y);ctx.rotate(Math.atan2(b.vy,b.vx)+Math.PI/2);
 const r=repair30Cell(name,(b.t||efxClock),0,0,8+lv*.9,25+lv*2.5,true,b._inf?null:col);ctx.restore();return r;
};
chaingunMountsDraw=function(dt){
 if(!chaingunMountsVisible())return;
 const rev=clamp(run._chainRev||0,0,1);run._chainSpinT=(run._chainSpinT||0)+(dt||1/60)*(.15+rev);
 const pilot=typeof _pilotKey==='function'?_pilotKey():run.pilot;
 const points=chaingunMountPoints(),z=.18;
 for(let i=0;i<2;i++){
  const name='chaingun_mount_'+pilot+'_'+(i?'right':'left'),a=REPAIR30_ART[name];if(!a)continue;
  const p=points[i],h=a.size[1]*z,w=a.size[0]*z;
  repair30Cell(name,0,p.x,p.y-(a.anchor[1]-a.size[1]/2)*z,w,h,false);
  const barrel=REPAIR30_ART.chaingun_barrel_top,bz=.16;
  const socketY=p.y+(18-a.anchor[1])*z;
  repair30Cell('chaingun_barrel_top',run._chainSpinT,p.x,socketY-(barrel.anchor[1]-barrel.size[1]/2)*bz,barrel.size[0]*bz,barrel.size[1]*bz,false);
  if(player._chainMuzzle>0)wm26Draw(ctx,'chaingun',p.x,socketY-12,-Math.PI/2,1-player._chainMuzzle/.10,18,wlvGlow(clamp(run.wlevel||1,1,5)));
 }
};
/* Tally profiling found >1000 scratch-canvas resizes/repaints per frame just
   for letter outlines. Cache immutable authored glyph masks, not score values.
   Numerical tally and per-section lettering still update every frame. */
const GLYPH30={map:new Map(),ids:new WeakMap(),next:1,bytes:0,limit:8*1024*1024,hits:0,misses:0};
function glyph30(img,f,color,tint,solid){
 if(!img||!(img.naturalWidth||img.width)||!(f[2]>0&&f[3]>0))return null;
 let id=GLYPH30.ids.get(img);if(!id){id=GLYPH30.next++;GLYPH30.ids.set(img,id);}
 const key=[id,...f.slice(0,4),color,tint,solid].join('|');
 let c=GLYPH30.map.get(key);if(c){GLYPH30.map.delete(key);GLYPH30.map.set(key,c);GLYPH30.hits++;return c;}
 const size=f[2]*f[3]*4;if(size>GLYPH30.limit)return null;
 c=document.createElement('canvas');c.width=f[2];c.height=f[3];const g=c.getContext('2d');
 g.drawImage(img,f[0],f[1],f[2],f[3],0,0,f[2],f[3]);
 g.globalCompositeOperation=solid?'source-in':'color';g.globalAlpha=solid?1:(tint==null?.8:tint);g.fillStyle=color||'#000';g.fillRect(0,0,c.width,c.height);
 if(!solid){g.globalCompositeOperation='destination-in';g.globalAlpha=1;g.drawImage(img,f[0],f[1],f[2],f[3],0,0,c.width,c.height);}
 while(GLYPH30.map.size>=512||GLYPH30.bytes+size>GLYPH30.limit){const k=GLYPH30.map.keys().next().value,v=GLYPH30.map.get(k);GLYPH30.bytes-=v.width*v.height*4;GLYPH30.map.delete(k);}
 GLYPH30.map.set(key,c);GLYPH30.bytes+=size;GLYPH30.misses++;return c;
}
const GLYPH30_BASE={solid:drawFrameSolid,tint:drawFrameTinted};
drawFrameSolid=function(img,f,dx,dy,dw,dh,color,alpha){
 const c=glyph30(img,f,color,1,true);if(!c)return GLYPH30_BASE.solid.apply(this,arguments);
 ctx.save();ctx.imageSmoothingEnabled=false;if(alpha!=null)ctx.globalAlpha=alpha;ctx.drawImage(c,dx,dy,dw,dh);ctx.restore();
};
drawFrameTinted=function(img,f,dx,dy,dw,dh,color,tint,alpha){
 if(!color)return GLYPH30_BASE.tint.apply(this,arguments);
 const c=glyph30(img,f,color,tint,false);if(!c)return GLYPH30_BASE.tint.apply(this,arguments);
 ctx.save();if(alpha!=null)ctx.globalAlpha=alpha;ctx.drawImage(c,dx,dy,dw,dh);ctx.restore();
};

// Helpers are independent targets even while their parent changes pose or is
// temporarily invulnerable. A parent's _noHit must not discard a helper hit.
function repair30DroneBullet(b,pierce,dt){
 const own=subBoss;if(!own||!subBossActive||own.dead||own._ship!=='olivewarden')return false;
 const d=stage4MiniDroneAt(own,b.x,b.y,Math.max(b.w||0,b.h||0)*.45);if(!d)return false;
 if(pierce){
  if(b._repairDrone!==d){b._repairDrone=d;b._repairDroneCD=0;}
  b._repairDroneCD=(b._repairDroneCD||0)-dt;if(b._repairDroneCD>0)return true;b._repairDroneCD=.10;
 }
 _lastHitX=b.x;_lastHitY=b.y;
 const elem=elementalDamageResult(own,'subboss',b,b._bossDmg??b.dmg,b.x,b.y);
 stage4MiniDroneDamage(own,d,elem.dmg);stageStats.hits++;weaponHitSfx('normal');
 if(!pierce||b.kind==='mavlaser')b.dead=true;return true;
}

// The real raised-hammer reel owns the activation, including lightning from sky
// into the hammer and the core-out armor mask. No replacement robot/body plate.
function repair30ChromiumActivationDraw(b){
 const h=b._hammer,s=h.state,R=h.recovery;
 h.state='storm_raise';h.recovery=null;
 try{return hammerStormDraw(b);}finally{h.state=s;h.recovery=R;}
}
const REPAIR30_ARMOR={begin:fr27BeginArmor,restore:fr27Restore,reflect:fr27Reflect,activation:fr27ActivationTick};
FR27_ACT.plate=2.35;FR27_ACT.end=2.85;
fr27BeginArmor=function(b){
 const a=REPAIR30_ARMOR.begin(b),n=fr27Difficulty();
 a.hp=a.max=b.maxhp*[.30,.60,1][n];
 a.checkpoints=n===0?[.75,.35,.15]:n===1?[.35,.15]:[];
 if(n===0)a.half=true;
 const f=b._hammer.frAct;f.combatY=f.y0;f.y0=Math.max(f.y0,PLAY.y+228);b.y=f.y0;
 return a;
};
fr27ActivationTick=function(b,dt){
 const f=b._hammer.frAct;REPAIR30_ARMOR.activation(b,dt);
 if(!f||f.combatY==null)return;
 const p=clamp((b._hammer.t-FR27_ACT.plate)/(FR27_ACT.end-FR27_ACT.plate),0,1);
 if(b._hammer.state!=='fr_activation')b.y=f.combatY;
 else if(p>0)b.y=lerp(f.y0,f.combatY,p*p*(3-2*p));
};
fr27Restore=function(b,fraction,critical,barrier){
 const normal=fr27Difficulty()===0;
 REPAIR30_ARMOR.restore(b,normal?Math.min(fraction,.08):fraction,critical,normal?false:barrier);
 if(normal){const r=b._hammer.recovery;r.coreHP=r.coreMax=12;r.duration=Math.max(r.duration,3.25);}
};
fr27Reflect=function(b,a,dt){if(fr27Difficulty()===0){a.barrier=0;return;}return REPAIR30_ARMOR.reflect(b,a,dt);};
// The song encounters use the same complete arsenal as the regular fight.
// Keep HAMA's alternating robot toss and all authored music/dance cues intact.
const REPAIR30_PASSWORD_ATTACK=HAMA_BASE.attack;
HAMA_BASE.attack=function(b,d){
 const which=(d.attack||0)%8;
 if(which<4)return REPAIR30_PASSWORD_ATTACK(b,d);
 d.attack++;d.mode='attack';d.t=0;
 const h=b._hammer;h.phasePending=false;h.comboPending=false;h.mode='hammer';
 h.throw=null;h.whirl=null;h.knockedHammer=null;h.hammerDestroyed=false;
 if(which===4)hammerSpellStart(b);
 else if(which===5){h.mode='chaingun';hammerChainStart(b);}
 else if(which===6)hammerStormStart(b);
 else hammerState(b,'mega_charge');
};
const REPAIR30_SEQUENCE=ht27CombatSequence,REPAIR30_STORM=hammerStormStart;
ht27CombatSequence=function(b){return REPAIR30_SEQUENCE(b)||!!(b?._hammer?.state==='storm_raise'&&b._hammer.recovery?.status==='charging');};
hammerStormStart=function(b){
 const r=REPAIR30_STORM(b);
 if(fr27Difficulty()===0){const q=b._hammer.recovery;q.coreHP=q.coreMax=12;q.amount=Math.min(q.amount,b.maxhp*.08);q.duration=3.25;}
 return r;
};
