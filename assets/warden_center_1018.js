"use strict";
/* Iron Warden: a real central rotary gun and a single bullet-interception policy. */
const WC18={base:{init:mr27Init,cell:mr27Cell,shape:mr27Shape,at:mr27At,mount:mr27Mount,
 can:mr27CanFire,fire:mr27Fire,tick:mr27Tick,damage:mr27Damage,core:mr27CoreDraw,
 mini:sa14MiniAttack,slug:sa14Slug,shot:eShootT,warShot:stage4WarfareShot,
 rules:s3kOrdnanceRules,element:enemyOrdnanceElement,intercept:enemyOrdnanceCanIntercept,
 break:ordnanceBreak1002,load:stageLoadBegin},owner:null,shots:0,draws:0};
for(const a of WC18_ART.frames)XART._src[a.key]=a.path;
function wc18Owns(b){return b?._ship==='olivewarden';}
function wc18Ready(){return WC18_ART.frames.map(a=>XART.rdy(a.key)).every(Boolean);}
stageLoadBegin=function(n,keys){return WC18.base.load.call(this,n,[...(keys||[]),...(n===4?WC18_ART.frames.map(a=>a.key):[])]);};
function wc18Bullet(q){return !!q&&(q._wc18Bullet||q._er26Source==='olivewarden'&&!/missile|rocket|bomb|orb/.test(q.kind||''));}
function wc18Protect(q){if(!q||q.dead)return q;q._wc18Bullet=true;q._s3kOriginalProof=true;delete q.hp;
 for(const [key,value]of [['_weaponProof',true],['_shootable',false]]){
  if(Object.getOwnPropertyDescriptor(q,key)?.configurable===false)continue;
  Object.defineProperty(q,key,{get:()=>value,set:()=>{},enumerable:true,configurable:true});
 }return q;
}
eShootT=function(x,y,a,speed,kind){const q=WC18.base.shot.apply(this,arguments);
 return WC18.owner&&kind==='mg'?wc18Protect(q):q;};
sa14Slug=function(b){const before=WC18.owner;if(wc18Owns(b))WC18.owner=b;
 try{return WC18.base.slug.apply(this,arguments);}finally{WC18.owner=before;}};
stage4WarfareShot=function(b,slot,angle,speed,role){const q=WC18.base.warShot.apply(this,arguments);
 return wc18Owns(b)&&!['rocket','orb','bomb'].includes(role)?wc18Protect(q):q;};
s3kOrdnanceRules=function(q){if(wc18Bullet(q)){wc18Protect(q);return;}return WC18.base.rules.apply(this,arguments);};
enemyOrdnanceElement=function(q){return wc18Bullet(q)?null:WC18.base.element.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return !wc18Bullet(q)&&WC18.base.intercept.apply(this,arguments);};
ordnanceBreak1002=function(q){if(wc18Bullet(q))return;return WC18.base.break.apply(this,arguments);};
mr27Init=function(b){const r=WC18.base.init.apply(this,arguments);
 if(wc18Owns(b)&&b._mr27&&!mr27Part(b,'gunC')){const hp=Math.ceil(b.maxhp*.08);
  b._mr27.parts.push({id:'gunC',hp,maxhp:hp,flash:0,rot:0,recoil:0,dead:false,age:0,fireAge:99});wc18Ready();
 }return r;};
function wc18Center(slot){return ['C','CORE','core','gunC'].includes(slot);}
function wc18Pivot(b){return{x:b.x,y:(b._drawY??b.y)+b.h*.40};}
function wc18Pose(b){const p=mr27Part(b,'gunC'),R=b._er26;
 if(p.fireAge<.20)return 8+Math.min(3,Math.floor(p.fireAge*20));
 if(p.fireAge<.60)return 12+Math.min(3,Math.floor((p.fireAge-.20)*10));
 if(R.mode==='sa14-mg'&&R.t<R.warm)return 4+Math.min(3,Math.floor(R.t/R.warm*4));
 return Math.floor(p.age*8)%4;
}
mr27Cell=function(skin,cell,form){if(skin!=='iron'||cell<100)return WC18.base.cell.apply(this,arguments);
 const a=WC18_ART.frames[cell-100];if(!a||!XART.rdy(a.key))return null;
 WC18.draws++;return form==='white'||/^#[0-9a-f]{6}$/i.test(form||'')?xartTint(a.key,form==='white'?'#ffffff':form,1):XART.get(a.key);};
mr27Shape=function(b,id){if(!wc18Owns(b)||id!=='gunC')return WC18.base.shape.apply(this,arguments);
 const p=mr27Part(b,id),k=b.w*.38/256,rot=p.rot||0,dy=(128-WC18_ART.pivot[1])*k,m=wc18Pivot(b);
 return{id,cell:100+wc18Pose(b),x:m.x-Math.sin(rot)*dy,y:m.y+Math.cos(rot)*dy,
  w:256*k,h:256*k,rot};};
function wc18Local(b,x,y){const p=mr27Shape(b,'gunC'),dx=x-p.x,dy=y-p.y,c=Math.cos(p.rot),s=Math.sin(p.rot);
 return{x:(dx*c+dy*s)/p.w*256+128,y:(-dx*s+dy*c)/p.h*256+128};}
function wc18Solid(b,x,y){const p=mr27Part(b,'gunC');if(!p||p.dead)return false;
 const q=wc18Local(b,x,y),mask=WC18_ART.masks[wc18Pose(b)],n=mask.n,gx=Math.floor(q.x/256*n),gy=Math.floor(q.y/256*n);
 return gx>=0&&gx<n&&gy>=0&&gy<n&&Math.floor(parseInt(mask.rows[gy],16)/Math.pow(2,n-1-gx))%2===1;
}
mr27At=function(b,x,y){if(!wc18Owns(b)||!b._mr27)return WC18.base.at.apply(this,arguments);
 if(b.dead||b.enter||b._noHit)return null;if(wc18Solid(b,x,y))return 'gunC';
 // Native side-module rectangles must not turn the new gun's transparent padding solid.
 const all=b._mr27.parts;b._mr27.parts=all.filter(p=>p.id!=='gunC');
 try{return WC18.base.at.apply(this,arguments);}finally{b._mr27.parts=all;}};
mr27Mount=function(b,slot){if(!wc18Owns(b)||!wc18Center(slot)||!mr27Part(b,'gunC'))return WC18.base.mount.apply(this,arguments);
 const p=mr27Part(b,'gunC');if(p.dead)return WC18.base.mount.apply(this,arguments);
 const q=mr27Shape(b,'gunC'),a=WC18_ART.frames[q.cell-100],tip=a.muzzles[p.barrel||0],k=q.w/256,c=Math.cos(q.rot),s=Math.sin(q.rot),dx=(tip[0]-128)*k,dy=(tip[1]-104)*k;
 const m=wc18Pivot(b);return{x:m.x+dx*c-dy*s,y:m.y+dx*s+dy*c};};
mr27CanFire=function(b,slot){if(wc18Owns(b)&&wc18Center(slot)&&mr27Part(b,'gunC'))return !mr27Part(b,'gunC').dead;
 return WC18.base.can.apply(this,arguments);};
mr27Fire=function(b,slot,angle){if(!wc18Owns(b)||!wc18Center(slot))return WC18.base.fire.apply(this,arguments);
 const p=mr27Part(b,'gunC');if(p&&!p.dead){p.rot=angle-Math.PI/2;p.recoil=1;p.fireAge=0;p.barrel=1-(p.barrel||0);WC18.shots++;}};
mr27Tick=function(b,dt){const r=WC18.base.tick.apply(this,arguments);
 if(wc18Owns(b)){const p=mr27Part(b,'gunC');if(p){p.age+=dt;p.fireAge+=dt;
  const T=b._er26._sa14;if(!p.dead&&p.fireAge>.22){const target=T?.aim||player,m=wc18Pivot(b),rot=Math.atan2(target.y-m.y,target.x-m.x)-Math.PI/2;
   p.rot+=stage4AngleDelta(p.rot,clamp(rot,-1,1))*Math.min(1,dt*8);}
 }}return r;};
mr27CoreDraw=function(b){if(wc18Owns(b)&&mr27Part(b,'gunC')&&wc18Ready()&&!wls17Exposed(b))return;
 return WC18.base.core.apply(this,arguments);};
mr27Damage=function(b,dmg,x,y){const id=wc18Owns(b)&&b._mr27?mr27At(b,x??b.x,y??b.y):null,
 p=id==='gunC'?mr27Part(b,id):null,before=p?.hp,result=WC18.base.damage.apply(this,arguments);
 if(p&&p.hp<before)markHit(p,.20);return result;};
sa14MiniAttack=function(b,dt){if(!wc18Owns(b))return WC18.base.mini.apply(this,arguments);
 const R=b._er26,T=R._sa14,c=sa14MiniCfg();R.warnings=[];
 if(!['sa14-mg','sa14-rockets'].includes(R.mode))return WC18.base.mini.apply(this,arguments);
 const slots=R.mode==='sa14-mg'?['L','C','R']:['ROCKET_L','ROCKET_R'];
 if(R.t<R.warm){for(const slot of slots)if(mr27CanFire(b,slot)){
   const p=shipBossMount(b,slot),a=Math.atan2(T.aim.y-p.y,T.aim.x-p.x);
   for(const off of R.mode==='sa14-rockets'&&vp12Tier()>0?[-.045,.045]:[0])
    sa14Warning(b,p,{x:p.x+Math.cos(a+off)*VH,y:p.y+Math.sin(a+off)*VH},R.mode==='sa14-mg'?34:20,R.t/R.warm);
  }combatWarningTick(b,'warden-'+R.serial,R.t,R.warm);return true;
 }
 T.shot-=dt;if(T.shot<=0){
  if(R.mode==='sa14-mg'&&T.wave<c.rounds){const live=slots.filter(s=>mr27CanFire(b,s));
   if(live.length)sa14Slug(b,live[T.wave%live.length],T.aim);T.wave++;T.shot=c.mg;}
  else if(R.mode==='sa14-rockets'&&T.wave<c.waves){sa14Missiles(b,T.aim);T.wave++;T.shot=c.gap;}
 }if(R.t>=R.dur)er26Set(b,'recover');return true;
};
window.BOF_WARDEN_CENTER={ready:wc18Ready,solid:wc18Solid,state:WC18};
