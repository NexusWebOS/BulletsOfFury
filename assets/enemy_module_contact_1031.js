"use strict";
/* Rotating refits keep native part pools. Classify an actual bullet contact
   against the displayed module's authored alpha, rather than world-left/right. */
const R46_CONTACT={masks:new Map()};
// The same native Crescent is also deployed from the Stage7 Brood bay.
const R46_ESCORT=R46_ART.aliases['8|s8crescent'];
if(R46_ESCORT){R46_ART.aliases['7|s8crescent']=R46_ESCORT;const M=R46_ART.models[R46_ESCORT];if(!M.stages.includes(7))M.stages.push(7);}
function enemyModuleHitPart(e,b){
 if(!r46Model(e)||!e._modJet||!b||!Number.isFinite(b.x+b.y))return null;
 const B=R46_ART.modules['jet_'+(e._modJet==='desert'?'rotary':e._modJet==='black'?'missile':'laser')];
 if(!B||!XART.rdy(B.key))return null;
 let mask=R46_CONTACT.masks.get(B.key);if(!mask){const c=document.createElement('canvas');c.width=B.cell*B.dirs;c.height=B.cell;const g=c.getContext('2d');g.drawImage(XART.get(B.key),0,0);mask=g.getImageData(0,0,c.width,c.height);R46_CONTACT.masks.set(B.key,mask);}
 const size=Math.max(e.w,e.h)*1.28*.32*B.cell/128,k=B.cell/size;
 for(const side of[1,-1]){const name=side<0?'left':'right';if(e._r30?.[name].hp<=0)continue;
  const p=modularJetMount(e,side),a=e._modJetAngles?.[name]??Math.PI/2,d=s1aDir(a,B.dirs),x=Math.round((b.x-p.x)*k+B.cell/2),y=Math.round((b.y-p.y)*k+B.cell/2),r=Math.max(1,Math.ceil(Math.min(5,Math.max(b.w||0,b.h||0)*.5)*k));
  for(let yy=Math.max(0,y-r);yy<=Math.min(B.cell-1,y+r);yy++)for(let xx=Math.max(0,x-r);xx<=Math.min(B.cell-1,x+r);xx++)if(mask.data[(yy*mask.width+d*B.cell+xx)*4+3]>32)return{name,point:p};
 }
 return{name:'turret',point:{x:e.x,y:e.y}};
}
const R46_CONTACT_LOCK=enemyLockOn,R46_CONTACT_EFFECTS=updateEffects;
enemyLockOn=function(e,delay,shot){
 const b=r46Model(e)&&e._modJet&&shot?.fire?[...R46.pending].findLast(b=>b._r46Owner===e&&b._r46Pending&&!b._r46PartGate):null;
 if(!b)return R46_CONTACT_LOCK.apply(this,arguments);
 const left=modularJetPoint(e,-1),right=modularJetPoint(e,1),name=Math.hypot(b.x-left.x,b.y-left.y)<=Math.hypot(b.x-right.x,b.y-right.y)?'left':'right',fire=shot.fire;
 b._r46PartGate=name;const guarded=function(){if(b.dead||e._r30?.[name].hp<=0){b.dead=true;R46.pending.delete(b);return;}return fire.apply(this,arguments);};guarded._r46Round=b;
 const args=Array.from(arguments);args[2]={...shot,fire:guarded};const L=R46_CONTACT_LOCK.apply(this,args);b._r46PartLock=L;return L;
};
updateEffects=function(dt){const result=R46_CONTACT_EFFECTS.apply(this,arguments),changed=new Set();
 for(const b of R46.pending)if(b._r46PartGate&&b._r46Owner?._r30?.[b._r46PartGate].hp<=0){b.dead=true;R46.pending.delete(b);if(b._r46PartLock)changed.add(b._r46PartLock);}
 for(const L of changed)L.launches=L.launches.filter(sh=>!sh.fire?._r46Round?.dead);
 if(changed.size)playerLocks=playerLocks.filter(L=>!changed.has(L)||L.launches.some(sh=>!sh.done)||L.missiles.some(m=>!m.dead));
 return result;
};
// AIR17 indexes its surviving ports. Translate that index back to the real
// left/right module when only one gun remains, before the native flash call.
const R46_CONTACT_EMIT=air17Emit,R46_CONTACT_MUZZLE=stage4Muzzle;
air17Emit=function(e){const old=R46_CONTACT.emitting;R46_CONTACT.emitting=e;try{return R46_CONTACT_EMIT.apply(this,arguments);}finally{R46_CONTACT.emitting=old;}};
stage4Muzzle=function(e,ox,oy,scale,life,family){if(R46_CONTACT.emitting===e&&r46Model(e)&&e._modJet){const live=[-1,1].filter(side=>!e._r30||e._r30[side<0?'left':'right'].hp>0),side=live[ox<0?0:1];if(side==null)return;e._modJetFireSide=side;ox=side*.30;}return R46_CONTACT_MUZZLE.call(this,e,ox,oy,scale,life,family);};
