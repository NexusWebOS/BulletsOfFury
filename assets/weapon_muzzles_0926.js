"use strict";
/* Authored weapon feedback. Short release reels follow the emitter, never the round.
   Source plates were inspected in native Chromium; no procedural muzzle triangles. */
const WM26_REELS={
  mg:{key:'weapon_muzzle_rotary_',n:4,size:24,pivot:.5},
  chaingun:{key:'bpfx_muzzle_kinetic_',n:8,size:30,pivot:.5},
  spread:{key:'ndk_muz_',n:4,size:34,pivot:.86,up:true},
  shotgun:{key:'ndk_muz_',n:4,size:46,pivot:.86,up:true},
  missile:{key:'weapon_muzzle_missile_',n:4,size:30,pivot:.5},
  laser:{key:'weapon_muzzle_laser_',n:4,size:28,pivot:.5},
  orb:{key:'bpfx_muzzle_void_',n:8,size:32,pivot:.5},
  fire:{key:'bfx_magma_m_',n:6,size:28,pivot:.5},
  ice:{key:'bpfx_muzzle_void_',n:8,size:27,pivot:.5},
  lightning:{key:'bpfx_muzzle_void_',n:8,size:28,pivot:.5},
  sonic:{key:'laser_round_muzzle_',n:8,size:30,pivot:.5}
};
let wm26Releases=[];
const WM26_ART=new Map();
const WM26_ANCHORS=new Map();
function wm26Pixels(key,im){
  if(WM26_ANCHORS.has(key))return WM26_ANCHORS.get(key);
  const w=im.width||im.naturalWidth,h=im.height||im.naturalHeight;
  try{const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');g.drawImage(im,0,0);
    const d=g.getImageData(0,0,w,h).data;let top=h,bottom=0;
    for(let y=0;y<h;y++){let count=0;for(let x=0;x<w;x++)if(d[(y*w+x)*4+3]>100)count++;
      if(count>=3){top=Math.min(top,y);bottom=y;}}
    if(top>=h)return {top:0,bottom:.96,baseX:.5,noseX:.5};
    let sum=0,xsum=0;for(let y=Math.max(top,bottom-Math.ceil(h*.1));y<=bottom;y++)for(let x=0;x<w;x++){
      const i=(y*w+x)*4,a=d[i+3]/255,v=a*(d[i]+d[i+1]+d[i+2]);sum+=v;xsum+=(x+.5)*v;}
    let noseSum=0,noseX=0;for(let y=top;y<Math.min(h,top+Math.ceil(h*.025));y++)for(let x=0;x<w;x++){
      const a=d[(y*w+x)*4+3];if(a>100){noseSum+=a;noseX+=(x+.5)*a;}}
    const out={top:top/h,bottom:(bottom+1)/h,baseX:sum?xsum/sum/w:.5,noseX:noseSum?noseX/noseSum/w:.5};WM26_ANCHORS.set(key,out);return out;
  }catch(_e){return {top:0,bottom:.96,baseX:.5,noseX:.5};}
}
function wm26PlayerNose(){
  const pk=_pilotKey(),frame=Math.abs(player._bank||0)<.06?'ship_'+pk:_shipFrameKey(pk),key=shipGlowKey(frame);
  if(!XART.rdy(key))return {x:player.x+2,y:player.y-SHIP_DRAW_H*.48};
  const im=XART.get(key),anchor=wm26Pixels(key,im);
  const w=SHIP_DRAW_H*(im.width||im.naturalWidth)/(im.height||im.naturalHeight);
  return {x:player.x+w*(anchor.noseX-.5)+2,y:(player._drawY??player.y)+SHIP_DRAW_H*(anchor.top-.5)};
}
function wm26Warm(){for(const r of Object.values(WM26_REELS))for(let i=0;i<r.n;i++)XART.rdy(r.key+i);}
function wm26Family(kind){
  const k=String(kind||'mg').toLowerCase();
  if(/missile|rocket|torpedo|comet|mlaunch|gmiss|nukem|spacevolley|nmz_[489]$/.test(k))return 'missile';
  if(/lightning|electric|chainbolt|yuribolt|storm/.test(k))return 'lightning';
  if(/orb|mortar|bomb|shadow|void/.test(k))return 'orb';
  if(/cryo|ice|rime|frost|s3/.test(k))return 'ice';
  if(/fire|magma|flame|inferno|ember/.test(k))return 'fire';
  if(/sonic|wave/.test(k))return 'sonic';
  if(/shotgun|ndk/.test(k))return 'shotgun';
  if(/spread|bshot|spr_/.test(k))return 'spread';
  if(/rotary|chaingun|slug|cyclone/.test(k))return 'chaingun';
  if(/laser|beam|lance|helix|venom|prism|rail|chrome/.test(k))return 'laser';
  return 'mg';
}
function wm26Art(family,frame,color){
  const r=WM26_REELS[family]||WM26_REELS.mg,k=r.key+clamp(frame|0,0,r.n-1);
  for(let i=0;i<r.n;i++)XART.rdy(r.key+i);
  if(!XART.rdy(k))return null;const im=XART.get(k);if(!color)return im;
  const id=k+'|'+color;if(WM26_ART.has(id))return WM26_ART.get(id);
  const c=document.createElement('canvas');c.width=im.width||im.naturalWidth;c.height=im.height||im.naturalHeight;
  const g=c.getContext('2d');g.drawImage(im,0,0);g.globalCompositeOperation='color';g.fillStyle=color;g.fillRect(0,0,c.width,c.height);
  g.globalCompositeOperation='destination-in';g.drawImage(im,0,0);WM26_ART.set(id,c);return c;
}
function wm26Draw(g,family,x,y,angle,progress,size,color){
  const r=WM26_REELS[family]||WM26_REELS.mg,im=wm26Art(family,Math.floor(clamp(progress,0,.999)*r.n),color);if(!im)return false;
  const h=size||r.size,w=h*(im.width||im.naturalWidth)/Math.max(1,im.height||im.naturalHeight);
  g.save();g.imageSmoothingEnabled=false;g.globalAlpha=1;g.globalCompositeOperation='source-over';g.shadowBlur=0;
  g.translate(x,y);g.rotate((angle==null?-Math.PI/2:angle)+(r.up?Math.PI/2:-Math.PI/2));
  g.drawImage(im,-w/2,-h*r.pivot,w,h);g.restore();return true;
}
function wm26Emit(owner,x,y,angle,family,color,options={}){
  if(!owner||owner.dead||owner.out)return;
  // One flash per barrel on a firing beat; a fan is not five overlapping explosions.
  const old=wm26Releases.find(f=>f.owner===owner&&(options.player&&options.emitter
    ? f.emitter===options.emitter : f.age<.012&&Math.hypot(f.x-x,f.y-y)<6));
  if(old){if(!options.fallback)Object.assign(old,{family,color,fallback:false,follow:options.follow});
    if(options.player&&options.emitter)Object.assign(old,{age:0,life:options.life||.13,x,y,dx:x-owner.x,dy:y-owner.y,angle,size:options.size||WM26_REELS[family].size});return old;}
  const f={owner,x,y,dx:x-owner.x,dy:y-(owner._drawY==null?owner.y:owner._drawY),angle,
    family,color,age:0,life:options.life||.13,size:options.size||WM26_REELS[family].size,
    stage:run.stage,fallback:!!options.fallback,player:!!options.player,emitter:options.emitter||null,follow:options.follow||null};
  wm26Releases.push(f);if(wm26Releases.length>160)wm26Releases.shift();return f;
}
function wm26Point(f){
  if(f.follow)return f.follow();
  return {x:f.owner.x+f.dx,y:(f.owner._drawY==null?f.owner.y:f.owner._drawY)+f.dy,angle:f.angle};
}
function wm26Tick(dt){
  for(const f of wm26Releases)f.age+=dt;
  wm26Releases=wm26Releases.filter(f=>f.age<f.life&&f.stage===run.stage&&!f.owner.dead&&!f.owner.out);
}
function wm26PlayerShots(first){
  const used=new Set(),space=typeof spaceShipActive==='function'&&spaceShipActive();
  for(let i=first;i<pBullets.length;i++){
    const q=pBullets[i];if(q&&q._cal50){q._wm26=true;continue;}   // 0928: .50-cal rounds leave the wing pods, which draw their own flash
    if(!q||q._wm26||(q._launchDelay>0&&q.kind!=='mavlaser')||/^(beam|firewhip|flame|dk|spaceLaser)/.test(q.kind||''))continue;
    if(!Number.isFinite(q.x)||!Number.isFinite(q.y)||Math.hypot(q.x-player.x,q.y-player.y)>85)continue;
    q._wm26=true;const family=q._chaingun?'chaingun':q.kind==='orb'||q.kind==='yuriorb'?'orb':wm26Family(q.kind);
    const element=q._el||q._inf||forgeEntry(run.weapon)?.elem;
    const color=element?projectileMuzzleColor('',null,element):family==='missile'?null:
      q.kind==='venomx'?'#77ee35':family==='ice'?'#67dfff':family==='lightning'?'#ffe448':
      family==='orb'?'#67dfff':wlvGlow(clamp(q.colorLv||q.lv||run.wlevel||1,1,8));
    // A fan is emitted by one nose, not by one barrel for every projectile lane.
    let p=family==='spread'||family==='shotgun'?wm26PlayerNose():{x:player.x,y:player.y-18},emitter='nose';
    if(space){const hp=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE),ports=[...hp.laser,hp.nose];
      if(q.kind==='shadowOrb'){p=hp.nose;emitter='space-nose';}
      else {let best=0;for(let j=1;j<ports.length;j++)if(Math.hypot(ports[j].x-q.x,ports[j].y-q.y)<Math.hypot(ports[best].x-q.x,ports[best].y-q.y))best=j;
        p=ports[best];emitter='space-'+best;}}
    if(used.has(emitter))continue;used.add(emitter);
    wm26Emit(player,p.x,p.y,-Math.PI/2,family,color,{player:true,emitter,size:family==='mg'?20:undefined,
      follow:!space&&(family==='spread'||family==='shotgun')?()=>({...wm26PlayerNose(),angle:-Math.PI/2}):null});
  }
}
function wm26EnemyShot(x,y,angle,kind,owner){
  if(!owner){
    let score=Infinity;for(const e of [boss,subBoss,...enemies]){
      if(!e||e.dead||e.out)continue;
      const dx=(x-e.x)/Math.max(20,e.w*.5+8),dy=(y-(e._drawY==null?e.y:e._drawY))/Math.max(20,e.h*.5+8),d=dx*dx+dy*dy;
      if(d<=1.5&&d<score){score=d;owner=e;}
    }
  }
  // A splitting projectile in open air has no barrel and must not acquire one.
  if(!owner)return;
  let follow=null;if(owner._ship){
    const D=SHIPBOSS[owner._ship];let best=null,dist=12;
    for(const slot of Object.keys(D.mounts||{})){const p=shipBossMount(owner,slot),d=Math.hypot(p.x-x,p.y-y);if(d<dist){dist=d;best=slot;}}
    if(best)follow=()=>owner.dead?null:shipBossMount(owner,best);
  }
  const family=wm26Family(kind),color=['mg','chaingun','missile','spread','shotgun'].includes(family)?null:projectileMuzzleColor(kind,owner);
  wm26Emit(owner,x,y,angle,family,color,{fallback:true,follow});
}
function wm26HasNative(f,p){
  if(_navalFlashes.some(n=>{const q=n.follow?n.follow():n;return q&&Math.hypot(q.x-p.x,q.y-p.y)<15;}))return true;
  const b=f.owner,F=b._smz;
  return !!(F&&F.slots.some(s=>{const q=shipBossMount(b,s);return Math.hypot(q.x-p.x,q.y-p.y)<15;}));
}
function wm26DrawEnemy(){
  for(const f of wm26Releases){if(f.player)continue;const p=wm26Point(f);if(!p||f.fallback&&wm26HasNative(f,p))continue;
    wm26Draw(ctx,f.family,p.x,p.y,p.angle==null?f.angle:p.angle,f.age/f.life,f.size,f.color);}
}
function wm26DrawPlayer(){
  if(player.dead||player.out||player._hammerEvap||
     (typeof _cinematicHidePlayer!=='undefined'&&_cinematicHidePlayer)||
     (typeof s7WardenShipHidden==='function'&&s7WardenShipHidden()))return;
  for(const f of wm26Releases){if(!f.player||f.owner!==player)continue;const p=wm26Point(f);if(!p)continue;
    // The space hull already draws one laser flash at each cannon. Never stack a rack flash there.
    if(player._spaceMuzzle>0&&spaceShipActive()&&spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE).laser.some(h=>Math.hypot(h.x-p.x,h.y-p.y)<6))continue;
    wm26Draw(ctx,f.family,p.x,p.y,f.angle,f.age/f.life,f.size,f.color);}
  if(specialActive('maverick')&&special.mavCharging){
    const p=clamp((special.mavCharge||0)/MAV_FULL,0,1);
    wm26Draw(ctx,'laser',player.x,player.y-18,-Math.PI/2,(efxClock*12)%1,14+p*23,p>=.99?'#9674ff':'#74ef39');
  }
  if(specialActive('falva')&&special.charging){
    const p=clamp((special.charge||0)/FALVA_FULL,0,1);
    wm26Draw(ctx,'roller',player.x,player.y-18,-Math.PI/2,(efxClock*(9+p*9))%1,15+p*26,'#ff62cf');
  }
}
function wm26BossFlash(b,F){
  const D=SHIPBOSS[b._ship],family=wm26Family(F.fam||D.proj),color=projectileMuzzleColor(F.fam||D.proj,b);
  for(const slot of F.slots){const p=shipBossMount(b,slot);wm26Draw(ctx,family,p.x,p.y,Math.PI/2,F.t/F.life,F.hpx?F.hpx*.75:34,color);}
}
function wm26NavalFlash(f){
  // Replace the flat Stage 4 arrows, retain all other authored specialized reels.
  if(!/^s4w_muzzle_/.test(f.fam))return false;
  const family=/lightning/.test(f.fam)?'lightning':/orb/.test(f.fam)?'orb':'chaingun';
  wm26Draw(ctx,family,f.x,f.y,f.angle==null?Math.PI/2:f.angle,f.t/f.life,clamp(f.hpx*f.s,20,48),family==='chaingun'?null:family==='orb'?'#67dfff':'#ffe448');return true;
}
// These release outside pShoot (missile button, auto racks and charged weapons).
// Wrap their release boundary, preserving every return value and damage/timing rule.
function wm26PlayerRelease(fn){return function(...args){const first=pBullets.length;try{return fn.apply(this,args);}finally{wm26PlayerShots(first);}};}
useBomb=wm26PlayerRelease(useBomb);
autoFireMissiles=wm26PlayerRelease(autoFireMissiles);
spaceVolleyLaunchRack=wm26PlayerRelease(spaceVolleyLaunchRack);
spaceShadowRelease=wm26PlayerRelease(spaceShadowRelease);
launchFireball=wm26PlayerRelease(launchFireball);
function wm26EnemyRelease(fn){return function(...args){const first=eBullets.length;const result=fn.apply(this,args);
  for(let i=first;i<eBullets.length;i++){const q=eBullets[i];wm26EnemyShot(q.x,q.y,Math.atan2(q.vy||1,q.vx||0),q.kind);}return result;};}
eMissile=wm26EnemyRelease(eMissile);
eMissileHoming=wm26EnemyRelease(eMissileHoming);
eHomingMissile=wm26EnemyRelease(eHomingMissile);
// The director module warms the current reels after registration.
