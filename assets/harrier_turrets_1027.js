'use strict';
/* Native coloured gun modules replace the former highlight-only hull masks. */
const HT28={base:{at:roster17At,muzzle:roster17Muzzle,gun:roster17HullGun},emitting:null,draws:0};
for(let i=0;i<4;i++)for(const hit of[false,true]){const a=HT28_ART['gun_'+i+(hit?'_hit':'')];ER28_ART['hull_gun_'+i+(hit?'_hit':'')]=a;XART._src[a.key]=a.path;}
function ht28Angle(p){return p.muzzleAge<.14&&Number.isFinite(p.muzzleAngle)?p.muzzleAngle:p.er28Bearing??p.angle??Math.PI/2;}
function ht28Frame(p,angle=ht28Angle(p)){return er28Dir(angle-Math.PI/2)+(p.phase==='fire'?Math.floor((p.t||0)*30)%4:0)*64;}
function ht28Opaque(b,p,x,y){const q=roster17Mount(b,p);return er28AlphaAt('hull_gun_'+p.hullGun,ht28Frame(p),x-q.x,y-q.y);}
roster17At=function(b,x,y){if(!roster17Ready(b))return HT28.base.at.apply(this,arguments);
 const C=b._carrier17;for(const p of C.parts)if(p.kind==='gun'&&!p.dead&&ht28Opaque(b,p,x,y))return p.id;
 const id=HT28.base.at.apply(this,arguments);return C.parts.some(p=>p.id===id&&p.kind==='gun')?null:id;};
roster17HullGun=function(b,p,dt){const prior=HT28.emitting;HT28.emitting=p;try{return HT28.base.gun.apply(this,arguments);}finally{HT28.emitting=prior;}};
roster17Muzzle=function(b,p){if(p?.kind!=='gun'||!b?._carrier17)return HT28.base.muzzle.apply(this,arguments);
 const launch=HT28.emitting===p&&p.phase==='fire',round=launch?p.round:Math.max(0,(p.round||0)-1),angle=launch?p.lanes?.[round]??p.angle??Math.PI/2:ht28Angle(p),a=HT28_ART['gun_'+p.hullGun],socket=a.muzzles[ht28Frame(p,angle)][round%2],q=roster17Mount(b,p);
 return{x:q.x+socket[0],y:q.y+socket[1]};};
globalThis.BOF_HARRIER_TURRETS_1027=HT28;
