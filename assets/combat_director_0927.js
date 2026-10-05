"use strict";
/* Mike's September 27 director pass. Authored effects, shared attachment geometry. */
const D27_ART_CACHE=new Map(),D27_SHIP_CACHE=new Map();
const D27_SIZES={mg:24,chaingun:32,spread:36,shotgun:47,fire:34,ice:33,lightning:35,toxic:34,laser:30,orb:32,sonic:34,void:34,missile:35,roller:40,helix:34,exhaust:30};
for(const [k,d] of Object.entries(DIRECTOR_ART.sheets))XART._src['d27_'+k]=d.path;
for(const k of Object.keys(DIRECTOR_ART.reels))WM26_REELS[k]={key:'d27_'+k+'_',n:6,size:D27_SIZES[k],pivot:.96,up:true};
function d27Family(kind){
  const k=String(kind||'mg').toLowerCase();
  if(/missile|rocket|torpedo|comet|mlaunch|gmiss|nukem|spacevolley|nmz_[489]$/.test(k))return 'missile';
  if(/shotgun|ndk/.test(k))return 'shotgun';
  if(/rotary|chaingun|slug|cyclone|s4w_muzzle_mg/.test(k))return 'chaingun';
  if(/spread|bshot|spr_/.test(k))return 'spread';
  if(/roller|falva/.test(k))return 'roller';
  if(/helix|^venomx$/.test(k))return 'helix';
  if(/lightning|electric|chainbolt|yuribolt|storm/.test(k))return 'lightning';
  if(/sonic|wave/.test(k))return 'sonic';
  if(/shadow|void|dark|obsid|warp/.test(k))return 'void';
  if(/toxic|sludge|spore|acid|venom|water|tidal|s7acid|s7laser/.test(k))return 'toxic';
  if(/cryo|ice|rime|frost|glacier/.test(k))return 'ice';
  if(/fire|magma|flame|inferno|ember|charred/.test(k))return 'fire';
  if(/orb|plasma|mortar|bomb/.test(k))return 'orb';
  if(/laser|beam|lance|prism|rail|chrome/.test(k))return 'laser';
  return 'mg';
}
function d27MuzzleArt(family,frame,color){
  const d=DIRECTOR_ART.reels[family]||DIRECTOR_ART.reels.mg,fi=clamp(frame|0,0,5),r=d.frames[fi],key='d27_'+d.sheet;
  if(!XART.rdy(key))return null;
  const id=family+':'+fi+':'+(color||'');if(D27_ART_CACHE.has(id))return D27_ART_CACHE.get(id);
  const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');
  g.drawImage(XART.get(key),r[0],r[1],256,256,0,0,256,256);
  if(color){g.globalCompositeOperation='color';g.fillStyle=color;g.fillRect(0,0,256,256);g.globalCompositeOperation='destination-in';g.drawImage(XART.get(key),r[0],r[1],256,256,0,0,256,256);}
  c.naturalWidth=c.naturalHeight=256;c.complete=true;D27_ART_CACHE.set(id,c);return c;
}
function d27MuzzleDraw(g,family,x,y,angle,progress,size,color){
  family=DIRECTOR_ART.reels[family]?family:d27Family(family);
  const fi=Math.floor(clamp(progress||0,0,.999)*6),d=DIRECTOR_ART.reels[family],im=d27MuzzleArt(family,fi,color);if(!im)return false;
  const scale=(size||D27_SIZES[family])/256,r=d.frames[fi];
  g.save();g.imageSmoothingEnabled=false;g.globalCompositeOperation='source-over';g.shadowBlur=0;
  g.translate(x,y);g.rotate((angle==null?-Math.PI/2:angle)+Math.PI/2);
  g.drawImage(im,-r[4]*scale,-r[5]*scale,256*scale,256*scale);g.restore();return true;
}
wm26Family=d27Family;wm26Art=d27MuzzleArt;wm26Draw=d27MuzzleDraw;
wm26Warm=function(){for(const k of Object.keys(DIRECTOR_ART.sheets))XART.rdy('d27_'+k);};
wm26NavalFlash=function(f){
  if(f.atlas||!f.fam)return false;
  // Impact and warning reels also use this list: replace muzzle families only.
  if(!/muzzle|_muz|^nmz_|^mlaunch|^bfx_.+_m$|^s1fx_(military|rotary)/.test(f.fam))return false;
  const family=d27Family(f.fam),color=['mg','chaingun','shotgun','spread','missile'].includes(family)?null:f.muzzleColor;
  return d27MuzzleDraw(ctx,family,f.x,f.y,f.angle==null?Math.PI/2:f.angle,f.t/f.life,clamp((f.hpx||30)*(f.s||1),18,52),color);
};
wm26BossFlash=function(b,F){
  const family=d27Family(F.fam||SHIPBOSS[b._ship].proj),color=['mg','chaingun','missile','spread','shotgun'].includes(family)?null:projectileMuzzleColor(F.fam||SHIPBOSS[b._ship].proj,b);
  for(const slot of F.slots){if(typeof mr27CanFire==='function'&&!mr27CanFire(b,slot))continue;
    const p=shipBossMount(b,slot),part=b._mr27?mr27Part(b,['L','LW','CL'].includes(slot)?'gunL':'gunR'):null;
    d27MuzzleDraw(ctx,family,p.x,p.y,(part?.rot||0)+Math.PI/2,F.t/F.life,F.hpx?Math.min(52,F.hpx*.8):34,color);}
};
// True lasers retain a laser flare. Callers for fire/ice/kinetic are routed explicitly.
roundLaserMuzzleDraw=function(g,x,y,size,hex,frame){return d27MuzzleDraw(g,hex===FIRE_WHIP_PALETTE?'fire':'laser',x,y,-Math.PI/2,(((frame==null?Math.floor(efxClock*24):frame)%8)+8)%8/8,size,hex);};

/* A detached authored plate stays fully opaque until the terminal blast. */
const D27_MODULE_DEBRIS=[];
function d27ModuleDebrisTick(dt){
  for(let i=D27_MODULE_DEBRIS.length-1;i>=0;i--){
    const d=D27_MODULE_DEBRIS[i];if(d.stage!==run.stage){D27_MODULE_DEBRIS.splice(i,1);continue;}
    d.t+=dt;d.x+=d.vx*dt;d.y+=d.vy*dt;d.vy+=75*dt;d.rot+=d.spin*dt;
    if(d.t>=d.life){explode(d.x,d.y,Math.max(d.w,d.h)*.8,d.palette,'fireball');
      if(typeof spawnShockRing==='function')spawnShockRing(d.x,d.y,Math.max(d.w,d.h)*.65,'fire');
      D27_MODULE_DEBRIS.splice(i,1);}
  }
}
function d27ModuleDebrisDraw(){
  for(const d of D27_MODULE_DEBRIS){if(!d.image)continue;
    ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(d.x,d.y);ctx.rotate(d.rot);
    ctx.drawImage(d.image,-d.w/2,-d.h/2,d.w,d.h);ctx.restore();}
}
/* Reuse authored breakup/explosion families. Each part has an idempotence key. */
function d27ModuleRupture(owner,part,shape,palette){
  if(!owner||!part||part._d27Ruptured||!shape)return false;part._d27Ruptured=true;
  const unit=clamp(Math.max(shape.w||30,shape.h||30),24,100),count=unit>60?18:12;
  const room=Math.max(0,144-_xChain.filter(q=>q.module).length),n=Math.min(count,room),dx=shape.x-owner.x,dy=shape.y-owner.y;
  if(shape.debrisImage){const side=Math.sign(dx)||1;D27_MODULE_DEBRIS.push({image:shape.debrisImage,x:shape.x,y:shape.y,w:shape.w,h:shape.h,
    vx:side*(100+unit*.65),vy:-105-unit*.28,rot:shape.rot||0,spin:side*(5+unit*.025),
    t:0,life:.62+unit*.002,stage:run.stage,palette:palette||'red'});}
  const families=['nxp_dense','nxp_barrage','nxp_radial','nxp_clus'];
  for(let i=0;i<n;i++){
    const a=i*2.39996,r=unit*(.10+.24*(i%4)/3),ox=dx+Math.cos(a)*r,oy=dy+Math.sin(a)*r;
    _xChain.push({module:true,owner,stage:run.stage,ox,oy,t:.04+i*.085,
      x:owner.x+ox,y:owner.y+oy,size:unit*(i===n-1?.95:.35+.16*(i%3)),
      pal:palette||'red',kind:null,fam:families[i%families.length],cls:'turret',hold:.12,
      quiet:i%4!==0,big:false,shake:i%4===0?2:0});
  }
  spawnSmokeRing(shape.x,shape.y,unit*.6);
  if(typeof combatAudio0927==='function')combatAudio0927(owner,'combatModule0927',.3);
  return true;
}

/* Six travelling heat pulses within the authored exhaust mask. Hull, outlines,
   alpha and mounting positions are byte-identical to the source frames. */
const D27_RAW_GET=XART.get.bind(XART);
function d27ShipFrames(key){
  const base=String(key||'').replace(/_g[12]$/,''),tab=typeof BOFX!=='undefined'?BOFX.ships:null;
  if(!/^ship_(axel|cole|decker|falva|freezer|juggernaut|lizzie|maverick|yuri)(?:_[lr]|_pv[0-4])?$/.test(base)||!tab?.[base+'_g1']||!tab?.[base+'_g2'])return null;
  const id=base+':'+tab[base].join(',')+':'+(typeof lizzieSkinOn!=='undefined'&&lizzieSkinOn?1:0);
  if(D27_SHIP_CACHE.has(id))return D27_SHIP_CACHE.get(id);
  if(!XART.rdy(base)||!XART.rdy(base+'_g1')||!XART.rdy(base+'_g2'))return null;
  const src=D27_RAW_GET(base),hi=D27_RAW_GET(base+'_g1'),lo=D27_RAW_GET(base+'_g2'),w=src.width,h=src.height;
  const tmp=document.createElement('canvas');tmp.width=w;tmp.height=h;const g=tmp.getContext('2d',{willReadFrequently:true});
  const pixels=im=>{g.clearRect(0,0,w,h);g.drawImage(im,0,0);return g.getImageData(0,0,w,h);},original=pixels(src),up=pixels(hi).data,down=pixels(lo).data;
  const frames=[];for(let f=0;f<6;f++){
    const out=g.createImageData(w,h);out.data.set(original.data);
    for(let i=0;i<up.length;i+=4)if(up[i]!==down[i]||up[i+1]!==down[i+1]||up[i+2]!==down[i+2]){
      const y=Math.floor(i/4/w),pulse=(1+Math.sin(y*.43-f*Math.PI/3))*.5;
      for(let c=0;c<3;c++)out.data[i+c]=Math.round(down[i+c]*(1-pulse)+up[i+c]*pulse);
    }
    const c=document.createElement('canvas');c.width=w;c.height=h;c.naturalWidth=w;c.naturalHeight=h;c.complete=true;c.getContext('2d').putImageData(out,0,0);frames.push(c);
  }
  D27_SHIP_CACHE.set(id,frames);return frames;
}
function d27ShipFrame(key,phase){const frames=d27ShipFrames(key);return frames?frames[((phase==null?Math.floor(performance.now()/55):phase)%6+6)%6]:null;}
XART.get=function(key){return d27ShipFrame(key)||D27_RAW_GET(key);};

function d27FuriousBomber(b){return !!b?._bomber?.space&&(diffKey==='furious'||diffKey==='insanity');}
function d27TempestPalette(canvas){
  const g=canvas.getContext('2d'),im=g.getImageData(0,0,canvas.width,canvas.height),a=im.data;
  for(let i=0;i<a.length;i+=4){if(!a[i+3])continue;const r=a[i],gr=a[i+1],bl=a[i+2],v=Math.max(r,gr,bl);
    if(bl>gr*1.12&&r>gr*1.08){a[i]=Math.min(255,v*1.1);a[i+1]=gr*.20;a[i+2]=bl*.21;}
    else if(v>42){a[i]=r*.36;a[i+1]=gr*.33;a[i+2]=bl*.35;}
  }g.putImageData(im,0,0);return canvas;
}
wm26Warm();
