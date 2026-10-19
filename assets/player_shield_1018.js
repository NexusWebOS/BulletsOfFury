"use strict";
/* 1018 - Mike: "all player shields need to be glowing an animated and properly centered with them."
   Then: "the shields arent very pixel animated and I meant make it pixel glow. not a rotating glow around body."
   Then: "why are the shields so big. I mainly wanted just a specific outline of each pilot's ship that pixel glows
   and lets you know they are protected internally with a shield that glows over them too."

   So the shield is no longer a crystal shell around the ship at all. It is the SHIP'S OWN SILHOUETTE:
   - an outline 1 px outside the hull (bright, the pilot's colour lifted toward white) and a fainter ring 1 px outside
     that - the docs/PIXEL_GLOW_1015.md method (hard rings, no blur), traced from the exact frame on screen, so it
     follows banks, the flame flicker, rolls and somersaults;
   - an internal sheen: the hull's own silhouette in the pilot's colour laid OVER the ship at low alpha;
   - animated in hard steps on the game clock: a six-step brightness ladder, and a band of light that runs nose to
     tail through the outline and the sheen. No rotation, no scaling, no blur.

   How it finds the frame: drawShield is called BEFORE the hull in _drawPlayerCore, so it only flags the seat. The
   hull blit is preceded by pf27PlaneThrustDraw(g,key,x,y,w,h) with the exact key and rect, which is recorded; the
   roll/somersault branch draws somerFrameKey()/rollFrameKey() at h=64. After the whole player draw, the outline is
   drawn from the same image at the same rect. The silhouette masks are built once per frame key by compositing
   (source-in / destination-out) - no getImageData, so file:// stays safe. A blinked-off hull draws no shield either.
   The space hull keeps its authored animated bubble.

   LEVELS (Mike: "now we need indication that its become a level 2, level 3, level 4, level 5 shield"):
   - ONE RING PER LEVEL, each 1 px further out (level 1 = a single outline, level 5 = five bands fading outward);
   - brightness and the sheen climb with the level;
   - level 5 adds a gold edge on the outline and runs its light band twice as fast;
   - gaining a level flashes the outline white and snaps it outward one ring at a time in hard steps (0.32 s);
   - losing a level throws a burst of pixel shards off the outline (0.45 s). */
const PS18={base:drawShield,draws:0,lastFit:null,want:{},hull:{},cache:new Map(),lastLv:{},fx:{},shards:[],
 thrust:typeof pf27PlaneThrustDraw==='function'?pf27PlaneThrustDraw:null,player:drawPlayer};
const PS18_PAD=9;                 // five level rings + four flare steps
const PS18_LADDER=[.62,.78,.92,1,.92,.78];
const PS18_GOLD='#ffd24a';
const PS18_FLARE=.32,PS18_SHARD=.45;
function ps18HullInk(pk){
 const r=typeof BOFX!=='undefined'&&BOFX.ships&&BOFX.ships['ship_'+pk];if(!r||r.length<8)return null;
 const k=SHIP_DRAW_H/r[7];   // the hull is blitted from its full canvas at height SHIP_DRAW_H, centred on (x,y)
 return {cx:(r[4]+r[2]/2-r[6]/2)*k,cy:(r[5]+r[3]/2-r[7]/2)*k,w:r[2]*k,h:r[3]*k};
}
function ps18Pilot(){try{return _pilotKey();}catch(e){return run.pilot;}}
function ps18Seat(){return typeof _seat!=='undefined'?_seat:1;}
function ps18Clock(){return typeof efxClock==='number'?efxClock:performance.now()/1000;}
function ps18Tint(pk){const p=typeof PILOTS!=='undefined'&&PILOTS.find(q=>q.key===pk);return (p&&p.tint)||'#6fd0ff';}
function ps18Lift(hex,k){const n=parseInt(hex.slice(1),16),r=n>>16&255,g=n>>8&255,b=n&255,f=c=>Math.round(c+(255-c)*k);
 return 'rgb('+f(r)+','+f(g)+','+f(b)+')';}
function ps18Canvas(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;return c;}
/* silhouette masks at DRAW resolution, so a ring is exactly one screen pixel wide. Ring k is the silhouette grown
   by k px minus it grown by k-1, built lazily per radius and cached per frame key. */
function ps18Masks(key,im,W,H,tint){
 const ck=key+'|'+W+'x'+H+'|'+tint;let M=PS18.cache.get(ck);if(M)return M;
 const P=PS18_PAD,CW=W+2*P,CH=H+2*P;
 const shape=ps18Canvas(CW,CH),s=shape.getContext('2d');s.imageSmoothingEnabled=false;s.drawImage(im,P,P,W,H);
 const fill=(c,col)=>{const g=c.getContext('2d');g.globalCompositeOperation='source-in';g.fillStyle=col;g.fillRect(0,0,CW,CH);return c;};
 const copy=src=>{const c=ps18Canvas(CW,CH);c.getContext('2d').drawImage(src,0,0);return c;};
 const dils=[shape];
 const dil=r=>{while(dils.length<=r){const k=dils.length,c=ps18Canvas(CW,CH),g=c.getContext('2d');g.imageSmoothingEnabled=false;
   // grow the previous radius by one pixel (8 neighbours): radius k costs 9 blits, not (2k+1)^2
   for(let j=-1;j<=1;j++)for(let i=-1;i<=1;i++)g.drawImage(dils[k-1],i,j);dils.push(c);}return dils[r];};
 const rings={},ringOf=(k,col)=>{const id=k+col;if(rings[id])return rings[id];
  const c=copy(dil(k)),g=c.getContext('2d');g.globalCompositeOperation='destination-out';g.drawImage(dil(k-1),0,0);
  return rings[id]=fill(c,col);};
 M={CW,CH,ring:ringOf,tint,
  lit:ps18Lift(tint,.45),white:ps18Lift(tint,.85),
  sheen:fill(copy(shape),ps18Lift(tint,.25))};
 if(PS18.cache.size>160)PS18.cache.delete(PS18.cache.keys().next().value);
 PS18.cache.set(ck,M);return M;
}
drawShield=function(x,y){
 if(!(run.shield>0))return;
 const lv=Math.min(5,run.shield|0),t=ps18Clock();
 if(spaceShipActive())return ps18Space(x,y,lv,t);
 PS18.want[ps18Seat()]=true;           // drawn over the hull once the hull is on screen (see drawPlayer below)
};
if(PS18.thrust)pf27PlaneThrustDraw=function(g,key,x,y,w,h){
 if(g===ctx)PS18.hull[ps18Seat()]={key,x,y,w,h};
 return PS18.thrust.apply(this,arguments);};
function ps18DrawOutline(H,lv,t,seat){
 if(!XART.rdy(H.key))return false;const im=XART.get(H.key);if(!im)return false;
 const pk=ps18Pilot(),tint=ps18Tint(pk),W=Math.max(1,Math.round(H.w)),Hh=Math.max(1,Math.round(H.h));
 const M=ps18Masks(H.key,im,W,Hh,tint),P=PS18_PAD;
 const left=Math.round(H.x-H.w/2)-P,top=Math.round(H.y-H.h/2)-P;
 const st=Math.floor(t*9)%6,L=PS18_LADDER,F=PS18.fx[seat],fa=F&&F.kind==='up'?t-F.t:-1;
 const flaring=fa>=0&&fa<PS18_FLARE;
 // a weak shield (one pip) stutters, so the player can read that it is about to go
 if(lv<=1&&!flaring&&Math.floor(t*7)%5===0)return true;
 ctx.save();ctx.imageSmoothingEnabled=false;
 // internal glow over the hull, stronger per level
 ctx.globalCompositeOperation='lighter';ctx.globalAlpha=(.07+.045*lv)*L[(st+3)%6];ctx.drawImage(M.sheen,left,top);
 // one ring per level: the outline (k=1) bright and solid, each further ring dimmer
 ctx.globalCompositeOperation='source-over';
 for(let k=lv;k>=2;k--){ctx.globalAlpha=(.26+.05*lv)*(1-(k-2)*.11)*L[(st+k)%6];ctx.drawImage(M.ring(k,tint),left,top);}
 ctx.globalAlpha=(.55+.09*lv)*L[st];ctx.drawImage(M.ring(1,M.lit),left,top);
 ctx.globalCompositeOperation='lighter';ctx.globalAlpha=(.30+.05*lv)*L[st];ctx.drawImage(M.ring(1,M.lit),left,top);
 if(lv>=5){ctx.globalAlpha=.55+.35*(st&1);ctx.drawImage(M.ring(2,PS18_GOLD),left,top);ctx.globalAlpha=.35;ctx.drawImage(M.ring(1,PS18_GOLD),left,top);}
 // the light band runs nose to tail in 2 px steps; twice as fast at level 5, gold there
 const per=lv>=5?.68:1.35,span=M.CH+10,band=5,y0=Math.floor(((t*.9)%per)/per*span/2)*2-band;
 if(y0<M.CH){ctx.save();ctx.beginPath();ctx.rect(left,top+y0,M.CW,band);ctx.clip();
  ctx.globalAlpha=.85;ctx.drawImage(M.ring(1,lv>=5?PS18_GOLD:M.lit),left,top);for(let k=2;k<=lv;k++)ctx.drawImage(M.ring(k,tint),left,top);
  ctx.globalAlpha=.22+.04*lv;ctx.drawImage(M.sheen,left,top);ctx.restore();}
 // LEVEL UP: the outline flashes white and snaps outward one ring per hard step
 if(flaring){const s=Math.min(3,Math.floor(fa/PS18_FLARE*4));
  ctx.globalAlpha=1-s*.22;ctx.drawImage(M.ring(lv+1+s,M.white),left,top);ctx.drawImage(M.ring(1,'#ffffff'),left,top);
  if(s===0){ctx.globalAlpha=.5;ctx.drawImage(M.sheen,left,top);}}
 ctx.restore();
 PS18.lastFit={pk,lv,key:H.key,left,top,w:M.CW,h:M.CH,hull:[H.x-H.w/2,H.y-H.h/2,H.x+H.w/2,H.y+H.h/2]};PS18.draws++;
 return true;
}
// LEVEL DOWN: a burst of pixel shards thrown off the outline, in the pilot's colour, fading in hard steps
function ps18ShardBurst(seat,H,lost,t){
 const tint=ps18Tint(ps18Pilot()),n=8+4*lost;
 for(let i=0;i<n;i++){const a=i/n*Math.PI*2+(i%3)*.21,rx=H.w*.5,ry=H.h*.5;
  PS18.shards.push({seat,t0:t,x:H.x+Math.cos(a)*rx,y:H.y+Math.sin(a)*ry,vx:Math.cos(a)*(70+(i%4)*22),vy:Math.sin(a)*(70+(i%4)*22),
   s:2+(i%2),col:i%3?tint:ps18Lift(tint,.7)});}
 if(PS18.shards.length>120)PS18.shards.splice(0,PS18.shards.length-120);
}
function ps18DrawShards(seat,t){
 if(!PS18.shards.length)return;
 ctx.save();ctx.imageSmoothingEnabled=false;
 PS18.shards=PS18.shards.filter(q=>t-q.t0<PS18_SHARD&&t>=q.t0);
 for(const q of PS18.shards){if(q.seat!==seat)continue;const a=t-q.t0,step=Math.floor(a/PS18_SHARD*4);
  ctx.globalAlpha=1-step*.24;ctx.fillStyle=q.col;
  ctx.fillRect(Math.round(q.x+q.vx*a),Math.round(q.y+q.vy*a),q.s,q.s);}
 ctx.restore();
}
drawPlayer=function(){
 const seat=ps18Seat();PS18.want[seat]=false;PS18.hull[seat]=null;
 const r=PS18.player.apply(this,arguments);
 const lv=Math.min(5,Math.max(0,run.shield|0)),t=ps18Clock(),prev=PS18.lastLv[seat];
 let H=PS18.hull[seat];
 if(!H&&!player.dead){const rk=(typeof somerFrameKey==='function'&&somerFrameKey())||(typeof rollFrameKey==='function'&&rollFrameKey());
  if(rk&&XART.rdy(rk)){const im=XART.get(rk);H={key:rk,x:player.x,y:player.y,h:64,w:64*(im.naturalWidth/im.naturalHeight)};}}
 // a level change is an EVENT: flare on the way up, shards on the way down (never on death or in space)
 if(prev!=null&&lv!==prev&&!player.dead&&!spaceShipActive()){
  if(lv>prev)PS18.fx[seat]={kind:'up',t,lv};
  else{PS18.fx[seat]={kind:'down',t,lv};const HH=H||{x:player.x,y:player.y,w:player.w*2,h:player.h*2};ps18ShardBurst(seat,HH,prev-lv,t);}
 }
 PS18.lastLv[seat]=lv;
 if(PS18.want[seat]&&!player.dead&&H)ps18DrawOutline(H,lv,t,seat);
 if(!player.dead)ps18DrawShards(seat,t);
 PS18.want[seat]=false;PS18.hull[seat]=null;
 return r;
};
// The space hull keeps its authored animated bubble (a pixel reel already), unscaled and unblurred.
function ps18Space(x,y,lv,t){
 const a=typeof REPAIR30_ART!=='undefined'&&REPAIR30_ART.shield;if(!a||!XART.rdy(a.key))return PS18.base.call(this,x,y);
 const h=SPACE_SHIP_SIZE*1.23,w=SPACE_SHIP_SIZE*.9*1.20;
 ctx.save();ctx.globalAlpha=.70+.06*lv;repair30Cell('shield',t,Math.round(x),Math.round(y),Math.round(w),Math.round(h),true);ctx.restore();PS18.draws++;
}
