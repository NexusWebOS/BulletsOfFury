"use strict";
/* Space float is a world-position displacement, shared by rendering, collision and
   Retina. Remove its previous displacement before any native mover runs; apply the
   new displacement once afterwards. Native routes, timers and HP remain owners. */
const SG26={serial:0,context:null,base:{begin:ai27Begin,end:ai27End,boss:updateBoss,mini:updateSubBoss,
 hit:hitBoss,damage:hammerBossDamage,test:bossHitTest,targets:retinaBossTargets,
 valid:retinaTargetValid,missile:retinaMissileDamage,space:spaceDamageTarget,weapon:hammerWeaponTargetable}};
function sg26Space(){return !!(run.spaceMode&&(run.stage===5||run.stage===9));}
function sg26Foreground(b){
 if(!b?._hammer)return true;
 const scale=hammerDepthScale(b);
 return !b.dead&&!b._noHit&&Number.isFinite(scale)&&scale>=1-1e-6;
}
function sg26Owner(t){return t?._retinaOwner||t?._spaceBossOwner||t?._spaceSubOwner||t;}
function sg26Reject(b){if(b?._hammer)b._hammerModuleHit=null;}
hitBoss=function(){if(!sg26Foreground(boss)){sg26Reject(boss);return;}return SG26.base.hit.apply(this,arguments);};
hammerBossDamage=function(b){if(!sg26Foreground(b)){sg26Reject(b);return 0;}return SG26.base.damage.apply(this,arguments);};
bossHitTest=function(){if(!sg26Foreground(boss)){sg26Reject(boss);return false;}return SG26.base.test.apply(this,arguments);};
retinaBossTargets=function(b){return sg26Foreground(b)?SG26.base.targets.apply(this,arguments):[];};
retinaTargetValid=function(t){return sg26Foreground(sg26Owner(t))&&SG26.base.valid.apply(this,arguments);};
retinaMissileDamage=function(t){if(!sg26Foreground(sg26Owner(t)))return false;return SG26.base.missile.apply(this,arguments);};
spaceDamageTarget=function(t){if(!sg26Foreground(sg26Owner(t))){sg26Reject(sg26Owner(t));return;}return SG26.base.space.apply(this,arguments);};
hammerWeaponTargetable=function(b){return sg26Foreground(b)&&SG26.base.weapon.apply(this,arguments);};
function sg26Points(b){
 // These are physical hulls, not movement destinations or committed aim points.
 const a=[b];if(b._s9rift?.core)a.push(b._s9rift.core);
 if(b._s9fusion&&b._s9fusion.phase!=='tidal')a.push(b._s9fusion.left,b._s9fusion.right);
 return a.filter(Boolean);
}
function sg26Move(points,dy){for(const q of points){if(Number.isFinite(q.y))q.y+=dy;if(Number.isFinite(q._drawY))q._drawY+=dy;}}
function sg26Begin(b,dt){
 if(!b)return null;const old=b._sg26;
 if(old){sg26Move(old.points,-old.offset);if(old.eye===b._eh25&&old.eye)old.eye.y-=old.offset;old.offset=0;}
 const actor=b===boss||b===subBoss;
 if(!sg26Space()||b.dead||b._dyingT!=null||(!actor&&(b.prop||b._prop||b.pattern==='prop'||b.pattern==='s9meteor'||b._l5Rock||b._l9Rock)))return null;
 const q=old||(b._sg26={clock:0,phase:(++SG26.serial*2.399963229728653)%TAU,offset:0,points:[]});
 q.clock+=Math.max(0,Math.min(.05,dt||0));
 const depth=b._hammer?Math.min(1,Math.max(.25,hammerDepthScale(b))):1;
 q.next=Math.sin(q.clock*1.65+q.phase)*(actor?5:3.5)*depth;
 q.shots=new Set(eBullets);q.parent=SG26.context;SG26.context={b,q};b._sg26Tick=true;return q;
}
function sg26End(b,q){
 if(!q)return;try{
  q.points=sg26Points(b);q.offset=q.next;sg26Move(q.points,q.offset);
  // Horizon's eye and physical core share the same displayed flight height.
  q.eye=b._eh25;if(q.eye)q.eye.y+=q.offset;
  for(const p of eBullets)if(!q.shots.has(p)&&!p.dead){
   p.y+=q.offset;
   for(const k of ['_c32Start','_start','origin'])if(p[k]&&Number.isFinite(p[k].y))p[k].y+=q.offset;
  }
 }finally{b._sg26Tick=false;SG26.context=q.parent;q.shots=null;}
}
ai27Begin=function(e,dt){const q=sg26Begin(e,dt);try{return {native:SG26.base.begin.apply(this,arguments),space:q};}catch(err){sg26End(e,q);throw err;}};
ai27End=function(e,p){try{return SG26.base.end.call(this,e,p?.native);}finally{sg26End(e,p?.space);}};
updateBoss=function(dt){const b=boss,q=sg26Begin(b,dt);try{return SG26.base.boss.apply(this,arguments);}finally{sg26End(b,q);}};
updateSubBoss=function(dt){const b=subBoss,q=sg26Begin(b,dt);try{return SG26.base.mini.apply(this,arguments);}finally{sg26End(b,q);}};
// Muzzle flashes already store owner-relative dy; moving their owner moves the
// flash exactly once. Beam contacts run inside the native tick, before its final
// displacement, so their source must use that same upcoming world position.
for(const name of ['c30Line','c46Line']){
 const native=globalThis[name];globalThis[name]=function(b){const line=native.apply(this,arguments),c=SG26.context;
  return c&&c.b===b?{...line,from:{...line.from,y:line.from.y+c.q.next}}:line;};
}
const sg26Ray=chaosHarrierBeamRay;
chaosHarrierBeamRay=function(b,from){const c=SG26.context;if(c&&c.b===b){const a=[...arguments];a[1]={...from,y:from.y+c.q.next};return sg26Ray.apply(this,a);}return sg26Ray.apply(this,arguments);};
globalThis.BOF_SPACE_GRAVITY_1026={foreground:sg26Foreground,begin:sg26Begin,end:sg26End,state:SG26};
