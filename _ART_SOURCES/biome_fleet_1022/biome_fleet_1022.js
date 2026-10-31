"use strict";
/* Stage-scoped PixelLab fleet. Native controllers retain HP, tells, collision,
   audio, shields and deaths. Only hull banks and launcher-owned art change. */
const BF22={actor:null,aliases:new Map(),draws:0,shots:0,muzzles:0,
 base:{draw:drawEnemy,pose:af21Pose,blit:af21Draw,hardpoint:combatHardpoint,
 muzzle:wm26Emit,naval:navalFlash,projectile:ovSonicProjectileDraw,load:stageLoadBegin,touch:XART._touch,get:XART.get,h6:drawL6Jet},beamTints:new Map()};
for(const S of Object.values(BF22_ART.sheets))XART._src[S.key]=S.path;
for(const [id,M] of Object.entries(BF22_ART.models)){
 AF21_ART.models['bf22_'+id]=M;
 for(const alias of M.aliases)BF22.aliases.set(M.stages[0]+'|'+alias,{id,M});
}
function bf22Model(e){
 if(!e||e._bob20||e._mini||e._rebels||e.prop||e._prop)return null;
 const n=e._volc?2:e._s6storm||e._l6x||e._h6?6:e._s9void||e._s9?9:(e._bf22Stage||run.stage);
 return BF22.aliases.get(n+'|'+e.type)||null;
}
function bf22Span(e,M){return Math.max(e.w||32,e.h||32)*(M.nativeRatios[e.type]||1);}
XART.get=function(key){const im=BF22.base.get.apply(this,arguments),theme=BF22.actor&&bf22Theme(BF22.actor);
 if(!im||!theme||!/^laserbeam_\d+$/.test(key))return im;
 const color={magma:'#ff7925',sky:'#65e0d2',water:'#39d9f4'}[theme],cache=key+'|'+color;
 if(BF22.beamTints.has(cache))return BF22.beamTints.get(cache);
 const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);
 g.globalCompositeOperation='color';g.fillStyle=color;g.fillRect(0,0,c.width,c.height);g.globalCompositeOperation='destination-in';g.drawImage(im,0,0);
 BF22.beamTints.set(cache,c);return c;
};
XART._touch=function(key){
 const A=BF22.actor&&bf22Model(BF22.actor);
 if(A)for(const source of Object.values(BF22_ART.models).filter(M=>M.stages[0]===A.M.stages[0]).flatMap(M=>Object.values(M.sourceKeys)).filter(Boolean)){
  const family=source.replace(/_\d+$/,'_');if(key===source||family!==source&&key.startsWith(family)&&/^\d+$/.test(key.slice(family.length))){key=A.M.banks.idle.key;break;}
 }
 return BF22.base.touch.call(this,key);
};
function bf22Queue(e){return e._s2Act||e._s6Act||e._s9Act;}
function bf22State(e,kind,value){
 const req=e._air13Motion,q=bf22Queue(e),now=efxClock;
 if(req?.kind==='somer'||req?.kind==='roll')return {kind:req.kind,value:clamp(req.t/req.dur,0,.999)};
 if(Number.isFinite(e._roll))return {kind:'roll',value:clamp(e._roll,0,.999)};
 if(e._barrelT>0)return {kind:'roll',value:clamp(1-e._barrelT/(['horizon','dreadv'].includes(e.type)?.92:.72),0,.999)};
 if(kind==='roll'||kind==='somer')return {kind,value};
 if(q&&q._eb11?.started!==false){
  const at=Math.max(.01,q.at||.4),dur=Math.max(at+.01,q.dur||at+.3);
  return {kind:'attack',value:clamp(q.t<=at?q.t/at*.5:.5+(q.t-at)/(dur-at)*.5,0,.999)};
 }
 if(now-(e._bf22FireAt??-999)<.4)return {kind:'attack',value:clamp((now-e._bf22FireAt)/.4,0,.999)};
 const motion=Math.abs(e._bank||0)>.035||Math.abs(e.vx||0)>.15||Math.abs(e.spin||0)>.08;
 return {kind:motion?'drift':'idle',value:motion?((e.vx||e._bank||e.spin||1)<0?.20:.70):now*.9};
}
af21Pose=function(id,kind='idle',value=0){
 const e=BF22.actor,A=e&&bf22Model(e),entry=AF21.aliases.get(id);
 if(!A||entry?.M!==A.M)return BF22.base.pose.apply(this,arguments);
 const s=BF22.selection||bf22State(e,kind,value),p=BF22.base.pose.call(this,id,s.kind,s.value);
 if(p){p.kind=s.kind;p.f=Math.min(p.m.frames-1,Math.floor(((s.value%1+1)%1)*p.m.frames));}
 return p;
};
af21Draw=function(p,x,y,span,alpha=1,flash=null,module=null){
 const e=BF22.actor;if(!p?.M?._bf22||!e)return BF22.base.blit.apply(this,arguments);
 // Existing flight/scale transforms surround this draw and remain authoritative.
 const r=BF22.base.blit.apply(this,arguments),tr=ctx.getTransform(),root=BF22.root||tr,
  relative=Math.hypot(tr.a,tr.b)/Math.max(.0001,Math.hypot(root.a,root.b)),point=root.inverse().transformPoint(tr.transformPoint(new DOMPoint(x,y)));
 e._bf22Rendered={id:p.M.id,kind:p.kind,frame:p.f,key:p.key,span,
  scale:span/p.M.span*relative,dx:point.x-e.x,dy:point.y-e.y,
  x:e.x,y:e.y,angle:Math.atan2(tr.b,tr.a)-Math.atan2(root.b,root.a)+(p.rotation||0)};BF22.draws++;return r;
};
drawEnemy=function(e){
 const A=bf22Model(e);if(!A||e.dead)return BF22.base.draw.apply(this,arguments);
 const oldActor=BF22.actor,oldRoot=BF22.root,oldSelection=BF22.selection,oldAir=AIR13.aliases.get(e.type),saved=new Map();
 // Read motion once before legacy forward-pose wrappers temporarily hide _roll.
 BF22.selection=bf22State(e,'idle',0);BF22.actor=e;BF22.root=ctx.getTransform();for(const M of Object.values(BF22_ART.models).filter(M=>M.stages[0]===A.M.stages[0]))for(const alias of M.aliases){if(!saved.has(alias))saved.set(alias,AF21.aliases.get(alias));AF21.aliases.set(alias,A);}AIR13.aliases.set(e.type,{...(oldAir||{}),...A.M,
  heading:oldAir?.heading||{startAngle:Math.PI/2},roll:oldAir?.roll||A.M.banks.roll});
 try{
  // The death controller still owns its burning spin, crash and explosions.
  // Retain the new body during that native sequence rather than reviving old art.
  if(e._dyingT!=null){const p=BF22.base.pose.call(this,e.type,'idle',0);if(p){p.rotation=e.spin||0;return af21Draw(p,e.x,e.y,bf22Span(e,A.M),1,e.flash>0?hitFlashColor(e):null);}}
  e._bf22Rendered=null;const result=BF22.base.draw.apply(this,arguments);
  // Some legacy bomber/phase renderers intentionally return while their old
  // plate decodes. A complete new bank must not wait for that retired texture.
  if(!e._bf22Rendered){
   const p=af21Pose(e.type,'idle',0);if(p){
    const direction=e._fb2Stealth?.direction||e._mission29?.direction;
    p.rotation=direction?({south:0,north:Math.PI,east:-Math.PI/2,west:Math.PI/2}[direction]||0):(e.spin||0);
    const span=bf22Span(e,A.M)*(e._scale!=null?e._scale:1);
    af21Draw(p,e.x,e.y+(e._volc?volcHover(e):0),span,e._s9PhaseT>0?.30:1,e.flash>0?hitFlashColor(e):null);
   }
  }
  return result;
 }finally{
  BF22.actor=oldActor;BF22.root=oldRoot;BF22.selection=oldSelection;for(const [alias,old] of saved)old?AF21.aliases.set(alias,old):AF21.aliases.delete(alias);
  oldAir?AIR13.aliases.set(e.type,oldAir):AIR13.aliases.delete(e.type);
 }
};
const bf22OldGlow=volcGlowDraw;
volcGlowDraw=function(e){if(bf22Model(e))return;return bf22OldGlow.apply(this,arguments);};
drawL6Jet=function(e){const A=bf22Model(e);if(!A||BF22.actor!==e)return BF22.base.h6.apply(this,arguments);
 const p=af21Pose(e.type,'idle',0);if(!p)return false;p.rotation=e.spin||0;
 const span=bf22Span(e,A.M)*(e._pScale??1);e._drawW=e._drawH=span;
 return af21Draw(p,e.x,e.y,span,1,e.flash>0?hitFlashColor(e):null);
};
function bf22Mount(e,socket,hover=false){
 const A=bf22Model(e);if(!A)return null;
 const m=A.M,p=m.sockets[socket]||m.sockets.centre,scale=e._bf22Rendered?.scale??bf22Span(e,m)/m.span;
 // VOLC's native levitation is also added by volcHardpoint; its caller opts in.
 const a=e._bf22Rendered?.angle??(e._volc?0:e.spin||0),c=Math.cos(a),s=Math.sin(a),x=(p[0]-64)*scale,y=(p[1]-64)*scale;
 return {x:e.x+(e._bf22Rendered?.dx||0)+x*c-y*s,y:e.y+x*s+y*c+(e._volc?(hover?volcHover(e):0):(e._bf22Rendered?.dy||0)),angle:a+Math.PI/2};
}
combatHardpoint=function(e,ox,oy){
 if(!bf22Model(e))return BF22.base.hardpoint.apply(this,arguments);
 const socket=ox<-.1?'port':ox>.1?'starboard':'centre',p=bf22Mount(e,socket);
 e._bf22LastSocket=socket;return p;
};
function bf22Nearest(e,x,y){
 let best='centre',distance=Infinity;for(const k of ['port','starboard','centre']){const p=bf22Mount(e,k,true),d=Math.hypot(p.x-x,p.y-y);if(d<distance){best=k;distance=d;}}
 return best;
}
function bf22Theme(e){const n=bf22Model(e)?.M.stages[0];return n===2?'magma':n===6?'sky':n===9?'water':null;}
function bf22Flash(e,socket,angle,life=.16){
 const theme=bf22Theme(e),B=BF22_ART.effects[theme+'_muzzle'];if(!B||e.dead||e._dyingT!=null)return false;
 const stamp=e._bf22Muzzles||(e._bf22Muzzles={});if(efxClock-(stamp[socket]??-999)<.035)return true;
 const p=bf22Mount(e,socket,true);if(!p)return false;
 const size=Math.max(18,Math.min(38,bf22Span(e,bf22Model(e).M)*.38));
 const ok=combatAtlasFx(p.x,p.y,B.key,B.columns,1,0,B.frames,{owner:e,life:Math.min(.22,life),hpx:size,wpx:size,
  angle:(angle??p.angle)-Math.PI/2,follow:()=>e.dead||e._dyingT!=null?null:{...bf22Mount(e,socket,true),angle:(angle??p.angle)-Math.PI/2}});
 if(ok){stamp[socket]=efxClock;e._bf22FireAt=efxClock;BF22.muzzles++;}return ok;
}
wm26Emit=function(owner,x,y,angle,family,color,options={}){
 if(!options.player&&bf22Model(owner)){
  BF22.launcher=owner;
  bf22Flash(owner,bf22Nearest(owner,x,y),angle,options.life);return;
 }
 return BF22.base.muzzle.apply(this,arguments);
};
navalFlash=function(e,mz,scale,fam,opts={}){
 const owner=bf22Model(e)?e:bf22Model(ai27Context)?ai27Context:null;
 if(owner){bf22Flash(owner,bf22Nearest(owner,mz.x,mz.y),opts.angle,opts.life);return;}
 return BF22.base.naval.apply(this,arguments);
};
function bf22Tag(first,owner){
 const theme=bf22Theme(owner);if(!theme)return;
 for(let i=first;i<eBullets.length;i++){
  const b=eBullets[i];if(!b||b.dead||b._bf22Theme)continue;
  b._bf22Theme=theme;b._bf22Owner=owner;b._bf22Born=efxClock;
  // Existing native collision boxes, trajectories and shootable missile flags stay.
  const kind=b.kind||'';b._bf22Form=/wind|sonic|wave|rake|slash|crescent/i.test(kind)?'wave':/tracer|bullet|needle|laser|missile|rocket|slug|shard|lance|kinetic|^mg$/i.test(kind)?'needle':'orb';
  BF22.shots++;
 }
}
for(const name of ['eShootT','eShoot','eMG','eGreenLaser','eMissile','eMissileHoming','eHomingMissile']){
 const base=globalThis[name];if(typeof base!=='function')continue;
 globalThis[name]=function(...args){const owner=bf22Model(args[5]?.owner)?args[5].owner:ai27Context,first=eBullets.length,previous=BF22.launcher;
  BF22.launcher=null;try{const result=base.apply(this,args),actor=bf22Model(owner)?owner:BF22.launcher;bf22Tag(first,actor);
   if(bf22Model(actor)&&eBullets.length>first&&!args[5]?.noMuzzle){const b=eBullets[first];bf22Flash(actor,bf22Nearest(actor,b.x,b.y),Math.atan2(b.vy||0,b.vx||0));}
   return result;
  }finally{BF22.launcher=previous;}};
}
// Native controllers that append bullets directly still have one owning actor.
const bf22End=ai27End;
ai27End=function(e,previous){
 const first=e._bf22BulletStart;if(first!=null)bf22Tag(first,e);
 return bf22End.apply(this,arguments);
};
const bf22Begin=ai27Begin;
ai27Begin=function(e,dt){if(bf22Model(e))e._bf22BulletStart=eBullets.length;return bf22Begin.apply(this,arguments);};
function bf22EffectDraw(B,x,y,w,h,angle,age){
 if(!B||!XART.rdy(B.key))return false;const im=XART.get(B.key),f=Math.floor(Math.max(0,age)*B.fps)%B.frames,c=B.cells[f];
 const ink=B.ink||[0,0,64,64];ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(angle||0);
 ctx.drawImage(im,...c,-(ink[0]+ink[2])/2/64*w,-(ink[1]+ink[3])/2/64*h,w,h);ctx.restore();return true;
}
ovSonicProjectileDraw=function(b){
 if(!b?._bf22Theme)return BF22.base.projectile.apply(this,arguments);
 const B=BF22_ART.effects[b._bf22Theme+'_'+b._bf22Form];if(!B)return BF22.base.projectile.apply(this,arguments);
 const ink=B.ink||[8,8,56,56],iw=ink[2]-ink[0],ih=ink[3]-ink[1];
 const scale=Math.min((b.w||7)/Math.max(1,iw),(b.h||7)/Math.max(1,ih));
 return bf22EffectDraw(B,b.x,b.y,64*scale,64*scale,Math.atan2(b.vy||0,b.vx||0)-Math.PI/2,efxClock-(b._bf22Born||0));
};
stageLoadBegin=function(n,keys){
 const extra=Object.values(BF22_ART.effects).filter(B=>B.stages.includes(n)).map(B=>B.key);
 return BF22.base.load.call(this,n,[...(keys||[]),...extra]);
};
globalThis.BOF_BIOME_FLEET={state:BF22,art:BF22_ART,model:bf22Model,mount:bf22Mount};
