"use strict";
/* Nine player families. Flight and damage stay with native carriers; art follows
   the round's launch identity, never the weapon currently selected in the HUD. */
const PA11={base:{shoot:pShoot,bullets:drawBullets,flame:flameDraw,aura:infusionAuraDraw,
 load:stageLoadBegin,attack:attackElement,damageElement:damageProjectileElement,autoMissiles:autoFireMissiles},draws:{}};
const EA11_FAMILIES=Object.freeze({
 fire:{name:'FIRE',effect:'Burns targets over time.',stage:2},
 kinetic:{name:'SONIC',effect:'Pressure impacts knock ordinary enemies back.',stage:1},
 lightning:{name:'LIGHTNING',effect:'Arcs jump between nearby targets.',stage:4},
 water:{name:'WATER',effect:'Soaks and slows targets; amplifies lightning.',stage:9},
 ice:{name:'ICE',effect:'Chills targets and builds toward a shatter.',stage:3},
 chrome:{name:'CHROMIUM',effect:'Reflects nearby interceptable rounds; beams lock ordinary targets.',stage:5},
 toxic:{name:'TOXIC',effect:'Poisons targets; plague orbs leave a damaging cloud.',stage:7},
 dark:{name:'DARK MATTER',effect:'Pulls ordinary formations inward; void orbs leave a singularity.',stage:8},
 wind:{name:'WIND',effect:'Pushes and briefly slows ordinary enemies.',stage:6}
});
for(const a of Object.values(EA11_ART.banks))XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return PA11.base.load.call(this,n,[...(keys||[]),...Object.values(EA11_ART.banks).map(a=>a.key)]);};
function ea11Element(b){return b&&!b._enemyReflected&&b.kind!=='mavlaser'&&EA11_FAMILIES[b._inf]?b._inf:null;}
function ea11Role(b){
 const el=ea11Element(b);if(!el||el==='wind')return null;
 if(b.kind==='missile')return 'missile';
 if(b.kind==='lasermist')return 'mist';
 if(b.kind==='yuriLightningOrb')return 'sphere';
 if(['mg','spread','chromeRay','prismRay','forgeFireBlast','yuriLightningBolt'].includes(b.kind))return b._cal50?'heavy':'round';
 if(b.kind==='shard'&&!b._ts&&!['fire','ice'].includes(el))return 'round';
 return null;
}
function ea11Bank(b){
 const el=ea11Element(b),role=ea11Role(b);if(!role)return null;
 if(role==='mist')return REPAIR30_ART['cast_'+el];
 if(role==='sphere')return REPAIR30_ART['orb_'+el];
 return EA11_ART.banks[el+'_'+(role==='missile'?'missile':'round')];
}
function ea11Frame(a,t){return a.frames[Math.floor(Math.max(0,Number.isFinite(t)?t:0)*(a.fps||24))%a.frames.length];}
function ea11RoundDraw(b){
 const a=ea11Bank(b);if(!a||b.dead||b._launchDelay>0||!Number.isFinite(b.x)||!Number.isFinite(b.y)||!XART.rdy(a.key))return false;
 const role=ea11Role(b),r=ea11Frame(a,projectileVisualAge(b)),im=XART.get(a.key),lv=clamp(b.lv||1,1,5);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.shadowBlur=0;ctx.translate(b.x,b.y);
 if(role!=='sphere')ctx.rotate(Math.atan2(b.vy??-1,b.vx||0)+Math.PI/2);
 if(role==='sphere'||role==='mist'){
  const q=a.ink||[0,0,r[2],r[3]],h=role==='sphere'?Math.max(b.w||24,b.h||24)*1.8:25+lv*2.5,k=h/q[3];
  ctx.drawImage(im,r[0]+q[0],r[1]+q[1],q[2],q[3],-q[2]*k/2,-h/2,q[2]*k,h);
 }else{
  const h=role==='missile'?27+lv*2.2:role==='heavy'?23+lv*1.8:b.kind==='yuriLightningBolt'?17+lv:13+lv*1.2;
  const k=h/a.bodyHeight;
  ctx.drawImage(im,...r,-a.pivot[0]*k,-a.pivot[1]*k,r[2]*k,r[3]*k);
 }
 ctx.restore();const id=ea11Element(b)+'/'+role;PA11.draws[id]=(PA11.draws[id]||0)+1;return true;
}
drawBullets=function(){
 const all=pBullets,owned=new Set();
 for(const b of all){const a=ea11Bank(b);if(a&&!b.dead&&!(b._launchDelay>0)&&XART.rdy(a.key))owned.add(b);}
 pBullets=all.filter(b=>!owned.has(b));
 try{PA11.base.bullets.apply(this,arguments);}finally{pBullets=all;}
 for(const b of owned)ea11RoundDraw(b);
};
// Authored energy carries its own light. Remove old opaque rectangular auras.
infusionAuraDraw=function(b){if(ea11Element(b))return;return PA11.base.aura.apply(this,arguments);};
flameDraw=function(b){
 const el=ea11Element(b),a=el&&el!=='wind'&&REPAIR30_ART['cast_'+el];
 // Fire keeps the approved full flame reel; Wind keeps its 16-pose gust owner.
 if(!a||el==='fire'||!XART.rdy(a.key))return PA11.base.flame.apply(this,arguments);
 const top=b.top??b.y-b.h,bot=b.bot??b.y,r=ea11Frame(a,b.anim??efxClock),q=a.ink||[0,0,r[2],r[3]];
 if(![top,bot,b.x].every(Number.isFinite)||bot<=top)return;
 const k=(bot-top)/q[3];ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),r[0]+q[0],r[1]+q[1],q[2],q[3],b.x-q[2]*k/2,top,q[2]*k,bot-top);ctx.restore();
 PA11.draws[el+'/cast']=(PA11.draws[el+'/cast']||0)+1;
};
function ea11Stamp(b,inf,seat,refresh=false){
 if(!b||b._enemyReflected||!infusionCarrier(b))return;
 if(b._inf!==undefined&&!refresh)return;
 if(b._ea11NativeEl===undefined)b._ea11NativeEl=b._el||null;
 b._inf=inf&&EA11_FAMILIES[inf.elem]?inf.elem:null;b._infLv=b._inf?clamp(inf.lv||1,1,5):0;
 b._ea11Stamped=true;
 b.seat??=seat;
 if(b._inf)b._el=b._inf;
 else if(refresh){
  const native=b.kind==='flame'?(flameIsIce()?'ice':'fire'):b._ea11NativeEl;
  if(native)b._el=native;else delete b._el;
 }
}
pShoot=function(){
 const before=new Set(pBullets),seat=_seat||1,inf=run.infusion?{...run.infusion}:null;
 const r=PA11.base.shoot.apply(this,arguments);
 for(const b of pBullets){
  const held=['beam','flame'].includes(b.kind)&&(b.seat||seat)===seat;
  if(!before.has(b)||held)ea11Stamp(b,inf,seat,held);
 }
 return r;
};
autoFireMissiles=function(){
 const before=new Set(pBullets),f=spaceWeaponsActive()?null:forgeEntry(2);
 const r=PA11.base.autoMissiles.apply(this,arguments);
 for(const b of pBullets)if(!before.has(b)&&b.kind==='missile')ea11Stamp(b,f,_seat||1);
 return r;
};
attackElement=function(kind){
 const b=_dmgBullet;if(b?.kind===kind&&ea11Element(b))return b._inf;
 return PA11.base.attack.apply(this,arguments);
};
damageProjectileElement=function(b){
 const el=ea11Element(b);if(el)return el;
 return PA11.base.damageElement.apply(this,arguments);
};
