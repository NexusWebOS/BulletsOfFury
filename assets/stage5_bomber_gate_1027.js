'use strict';
/* The four Stage5/6 bomber modules shield its core without blocking their lanes. */
const SB28={base:{at:siegeBomberAt,hit:siegeBomberHit,targets:siegeBomberTargets},opened:new WeakSet(),events:[],blocked:0};
function sb28Own(b){return (run.stage===5||run.stage===6)&&!!b?._bomber;}
function sb28Closed(b){return sb28Own(b)&&b._bomber.parts.some(p=>p.hp>0);}
siegeBomberAt=function(b,x,y,pad=0){if(pb28Own(b)&&b._pb28?.hidden)return null;if(!sb28Closed(b))return SB28.base.at.apply(this,arguments);
 if(b.dead||b.enter||!Number.isFinite(x)||!Number.isFinite(y))return null;
 // A protected core is absent from offensive collision. Only a live physical
 // module can stop a round, including when its column crosses the body plate.
 for(const q of siegeBomberParts(b).slice().reverse()){
  if(q.id==='core'||!b._bomber.parts.some(p=>p.id===q.id&&p.hp>0))continue;
  if(Math.abs(x-q.x)<q.w*.5+Math.max(4,pad)&&Math.abs(y-q.y)<q.h*.5+Math.max(4,pad))return q.id;
 }return null;};
siegeBomberTargets=function(b){const out=SB28.base.targets.apply(this,arguments);return sb28Closed(b)?out.filter(t=>t._retinaId!=='bomber-core'):out;};
siegeBomberHit=function(b,dmg,x,y,id){const closed=sb28Closed(b);
 if(closed){id=id||(Number.isFinite(x)&&Number.isFinite(y)?siegeBomberAt(b,x,y,Math.max(2,(_dmgBullet?.w||0)*.35)):null);
  if(!id||id==='core'){SB28.blocked++;return;}
 }
 const out=SB28.base.hit.call(this,b,dmg,x,y,id);
 if(closed&&!sb28Closed(b)&&!b.dead&&b._bomber.core>0&&!SB28.opened.has(b)){
  SB28.opened.add(b);SB28.events.push({event:'core-exposed',time:efxClock,hp:b.hp,core:b._bomber.core});showCallout('shoot',1.6);
 }return out;};
globalThis.BOF_STAGE5_BOMBER_GATE_1027=SB28;
