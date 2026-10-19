"use strict";
/* Authored motion banks; no per-frame image processing on the normal draw path. */
const AIR13={aliases:new Map(),tints:new Map(),draws:0,fallbacks:0};
for(const d of Object.values(AM13_ART))for(const a of d.aliases)AIR13.aliases.set(a,d);
function air13Pose(id,kind='heading',value=Math.PI/2){
 const d=AIR13.aliases.get(id)||AM13_ART[id];if(!d)return null;
 const m=d[kind];if(!m)return null;
 const f=kind==='roll'?Math.floor(((value%1+1)%1)*m.frames)%m.frames:Math.round(((value-m.startAngle+TAU)%TAU)/TAU*m.frames)%m.frames;
 const key=m.kind==='files'?m.refs[f].key:m.key;
 if(!XART.rdy(key)){AIR13.fallbacks++;return null;}
 const im=XART.get(key);return{d,m,f,key,im,sx:m.kind==='files'?0:f*m.cell};
}
function air13Tint(p,color){
 const k=p.key+'|'+p.f+'|'+color;let im=AIR13.tints.get(k);if(im)return im;
 im=document.createElement('canvas');im.width=im.height=p.m.cell;const c=im.getContext('2d');
 c.drawImage(p.im,p.sx,0,p.m.cell,p.m.cell,0,0,p.m.cell,p.m.cell);c.globalCompositeOperation='source-atop';c.globalAlpha=.84;c.fillStyle=color;c.fillRect(0,0,im.width,im.height);
 if(AIR13.tints.size>=64)AIR13.tints.delete(AIR13.tints.keys().next().value);AIR13.tints.set(k,im);return im;
}
function air13Blit(p,x,y,span,alpha=1,flash=null){
 const size=span*p.m.cell/p.m.span;ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 const im=flash?air13Tint(p,flash):p.im,sx=flash?0:p.sx;
 ctx.drawImage(im,sx,0,p.m.cell,p.m.cell,x-size/2,y-size/2,size,size);ctx.restore();AIR13.draws++;
}
function air13DrawFlight(e,g,q){
 const roll=g.type==='barrel'&&q.side<0;
 // The controller measures clockwise from north; banks measure from east.
 const p=air13Pose('flight_variant_'+g.stage,roll?'roll':'heading',roll?g.age/.8:q.angle-Math.PI/2);if(!p)return false;
 const size=64*q.scale;drawUnitShadow(e.x,e.y,size,size,.24,e);
 air13Blit(p,e.x,e.y,size*p.d.referenceRatio,1,e.flash>0?hitFlashColor(e,'#ffffff'):null);e._air13RenderedKey=p.key;e._air13Frame=p.f;return true;
}
function air13DrawRebel(q,opt={}){
 if(q.dead&&!opt.allowDead)return false;
 if(q.frSomersault&&q.evadeT>0&&!opt.forceRoll&&q.rfHeading==null)return false;
 const key=q.key||REBEL_KEYS[q.i],roll=opt.forceRoll!=null||q.evadeT>0;
 const p=air13Pose(key,roll?'roll':'heading',roll?(opt.forceRoll??(1-q.evadeT/.38)):(q.rfHeading??Math.PI/2));if(!p)return false;
 const w=SHIP_DRAW_H*1.5,alpha=opt.alpha??(q.frCloak>0?.22+.12*Math.sin((q.t||0)*22):1);
 const hot=q.flash>0&&Math.floor((q.t||0)*20)%2===0;
 const angle=opt.allowDead?0:(q.rfHeading??Math.PI/2)-Math.PI/2,c=Math.cos(angle),s=Math.sin(angle);
 const modules=typeof fr27RebelModules==='function'?fr27RebelModules(q):[];
 for(const [a,z,id]of [[-.5,-.17,'left'],[-.17,.17,null],[.17,.5,'right']]){
  if(id&&modules.find(m=>m.id===id)?.hp<=0)continue;
  ctx.save();ctx.beginPath();const left=a===-.5?-w*3:a*w,right=z===.5?w*3:z*w;
  for(const [i,[x,y]]of [[left,-w*3],[right,-w*3],[right,w*3],[left,w*3]].entries()){
   const px=q.x+x*c-y*s,py=q.y+x*s+y*c;i?ctx.lineTo(px,py):ctx.moveTo(px,py);
  }ctx.closePath();ctx.clip();
  if(roll&&angle){ctx.translate(q.x,q.y);ctx.rotate(angle);air13Blit(p,0,0,w*p.d.referenceRatio,alpha,hot?'#ffffff':null);}else air13Blit(p,q.x,q.y,w*p.d.referenceRatio,alpha,hot?'#ffffff':null);ctx.restore();
 }
 if(!opt.allowDead&&q.frCast)combatWarningDraw(q,{x:q.x,y:q.y+28,ex:q.frCast.tx,ey:q.frCast.ty,progress:q.frCast.t/1.1,width:q.frCast.kind==='orb'?75:28,alpha:.30});
 q._air13RenderedKey=p.key;q._air13Frame=p.f;return true;
}
/* Preserve Fury's existing evasions and the intact/damaged ownership of stealth aircraft. */
const AIR13_FURY=furyFleetDraw;
furyFleetDraw=function(e){
 if(run.stage!==1||e.dead||e._dyingT!=null||e._furyMove?.kind!=='roll')return AIR13_FURY.apply(this,arguments);
 const p=air13Pose(e.type,'roll',e._furyMove.t/e._furyMove.dur);if(!p)return AIR13_FURY.apply(this,arguments);
 const span=Math.max(e.w,e.h)*(p.d.nativeRatios[e.type]||1);air13Blit(p,e.x+10,e.y+18,span,.25,'#000000');air13Blit(p,e.x,e.y,span,1,tintColor(e));e._air13RenderedKey=p.key;e._air13Frame=p.f;return true;
};
const AIR13_STEALTH=ap10StealthDraw;
ap10StealthDraw=function(e){
 if(run.stage!==6||e.dead||e._dyingT!=null||e.hp/e.maxhp<.5||!AP10_AIR_TYPES.has(e.type)&&!e._mission29&&!e._fb2Stealth&&!e._s6Strike)return AIR13_STEALTH.apply(this,arguments);
 if(on5Bomber(e)){e._fb2Stealth??={};if(!['blue','red','green','orange'].includes(e._fb2Stealth.role))e._fb2Stealth.role=(e._mission29?fb2MissionRole(e._mission29):null)||((e._side??e._dir??1)>0?'red':'green');e._fb2Stealth.direction||=e._s6Strike?.direction||'south';}
 const A=e._fb2Stealth||e._mission29||e._s6Strike||{},role=e._fb2Stealth?.role||(e._mission29?fb2MissionRole(A):null)||'blue',dir=A.direction||'south';
 if(p2StealthActorPose(e,role,A))return AIR13_STEALTH.apply(this,arguments);
 const p=air13Pose('stealth_'+role,'heading',{south:Math.PI/2,east:0,west:Math.PI,north:-Math.PI/2}[dir]);if(!p)return AIR13_STEALTH.apply(this,arguments);
 const size=e._s67Draw||((e._mission29||e._fb2Stealth)?104:Math.max(64,e._drawH||e.h||64));air13Blit(p,e.x,e.y,size*p.d.referenceRatio,1,e.flash>0?hitFlashColor(e):null);
 e._p2StealthKey=P2_STEALTH.get(role+'|idle').key;e._sm10Facing=dir;e._ap10Palette=role;e._drawW=e._drawH=size;e._air13RenderedKey=p.key;e._air13Frame=p.f;return true;
};
/* Native renderer retains weapons, warning lanes, exhaust and damage skins. Only its
   matching primary hull image is substituted during an authored turn or roll. */
const AIR13_DRAW=drawEnemy;
drawEnemy=function(e){
 if(e._vp12||e.dead||e._dyingT!=null||run.stage===1)return AIR13_DRAW.apply(this,arguments);
 const d=AIR13.aliases.get(e.type),source=d?.sourceKeys?.[e.type];
 if(!d||!source||!XART.rdy(source)||(run.stage!==4&&e.hp<e.maxhp*.5))return AIR13_DRAW.apply(this,arguments);
 const request=e._air13Motion,roll=request?.kind==='roll'||e._barrelT>0;
 if(!roll&&!request&&Math.abs(e.spin||0)<.08)return AIR13_DRAW.apply(this,arguments);
 const dur=['horizon','dreadv'].includes(e.type)?.92:.72;
 const value=roll?(request?request.t/request.dur:1-e._barrelT/dur):(request?.angle??d.heading.startAngle+(e.spin||0));
 const p=air13Pose(e.type,roll?'roll':'heading',value);if(!p)return AIR13_DRAW.apply(this,arguments);
 const original=XART.get(source),get=XART.get,family=source.replace(/_[0-9]+$/,'_'),hulls=new WeakSet([original]),draw=ctx.drawImage,base=ctx.getTransform(),baseAngle=Math.atan2(base.b,base.a);const tags=new WeakMap(),tint=xartTint;let replaced=false;
 XART.get=function(k){const im=get.apply(this,arguments);if(im&&(k===source||family!==source&&k.startsWith(family)&&/^[0-9]+$/.test(k.slice(family.length))))hulls.add(im);return im;};
 xartTint=function(k,color,a){const im=tint.apply(this,arguments);if(im&&(k===source||family!==source&&k.startsWith(family)&&/^[0-9]+$/.test(k.slice(family.length))))tags.set(im,color);return im;};
 ctx.drawImage=function replaceHull(im,...args){
  const color=tags.get(im);if(!hulls.has(im)&&!color)return draw.call(this,im,...args);
  if(hulls.has(im)&&replaced)return draw.call(this,im,...args);
  // Primary hull only. Existing shadow/tint and articulated module paths remain owned by the native renderer.
  if(hulls.has(im))replaced=true;const n=args.length,dx=args[n-4],dy=args[n-3],dw=args[n-2],dh=args[n-1],cx=dx+dw/2,cy=dy+dh/2;
  const matrix=this.getTransform(),angle=Math.atan2(matrix.b,matrix.a)-baseAngle;
  this.save();this.translate(cx,cy);this.rotate(-angle);ctx.drawImage=draw;
  air13Blit(p,0,0,Math.max(e.w,e.h)*(d.nativeRatios[e.type]||1),1,color||(e.flash>0?hitFlashColor(e):null));
  ctx.drawImage=replaceHull;this.restore();e._air13RenderedKey=p.key;e._air13Frame=p.f;
 };
 // Restore even if an unrelated native effect throws.
 try{return AIR13_DRAW.apply(this,arguments);}finally{ctx.drawImage=draw;xartTint=tint;XART.get=get;}
};
const AIR13_BEGIN=beginStage;
beginStage=function(n){AIR13.tints.clear();const r=AIR13_BEGIN.apply(this,arguments);
 for(const d of Object.values(AM13_ART))if(d.stages.includes(n))XART.rdy(d.heading.key);
 for(const id of n===1?['s1jetdelta','s1jetbomber','s1jetdelta_b','s1jetbomber_b','flight_variant_1']:n===6?['voss','nyx','rook','kaia','jace','flight_variant_6']:n===4?['flight_variant_4']:n===8?['flight_variant_8']:n===9?['wskim','horizon','dreadv']:[]){const d=AIR13.aliases.get(id)||AM13_ART[id];if(d?.roll.kind==='strip')XART.rdy(d.roll.key);}
 return r;
};
window.BOF_AIR_MOTION={catalogue:AM13_ART,pose:air13Pose,draw:air13Blit,stats:AIR13};
