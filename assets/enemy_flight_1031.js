"use strict";
/* Stage4-9 audit fixes. Whole authored motion banks, one stable identity,
   physical weapon sockets and finite flight. Native combat/death owners stay. */
const R46={base:{spawn:spawnEnemy,draw:drawEnemy,get:XART.get,tint:xartTint,hardpoint:combatHardpoint,
 mount:bf22Mount,chase:s4ChaseTick,beginAI:ai27Begin,endAI:ai27End,load:stageLoadBegin,begin:beginStage,
 jetDraw:drawModularJet,jetMount:modularJetMount,jetPoint:modularJetPoint,ports:air17Ports,
 naval:navalFlash,muzzle:wm26Emit,effects:updateEffects,flashes:drawNavalFlashes,kill:killEnemy,shot:eShootT,
 intercept:enemyOrdnanceCanIntercept,early:ovSonicProjectileDraw,airProjectile:air17DrawProjectile,warning:combatWarningDraw,lockLaunch:_lockLaunch,atlasFx:combatAtlasFx,missileCue:Audio.SFX.enemyMissile},
 actor:null,painting:false,tags:new WeakMap(),tints:new Map(),fx:[],events:[],pending:new Set(),serial:0,
 factories:{cp22drone:'s7sampler',cp22slime:'s7skimmer',cp22relay:'s7lamprey'}};
for(const B of [...Object.values(R46_ART.models),...Object.values(R46_ART.modules)])XART._src[B.key]=B.path;
for(const B of [...Object.values(R46_STATIC.banks),...Object.values(R46_ORDNANCE.glyphs),...Object.values(R46_FEEDBACK.banks)])XART._src[B.key]=B.path;
R46.glyphMisses=new Map();R46.glyphDraws=0;R46.staticDraws=0;
function r46Live(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function r46Model(e){return e?._r46&&R46_ART.models[e._r46.model];}
function r46Eligible(e){return run.stage>=4&&run.stage<=9&&e&&!e._boss&&!e.boss&&!e._mini&&!e._amini&&!e.prop&&!e._prop;}
function r46Log(e,event,data={}){R46.events.push({id:e?._r46?.id,type:e?.type,event,t:efxClock,...data});if(R46.events.length>1600)R46.events.shift();}
function r46GlyphSignature(b,e=b?._r46Owner){const art={};for(const k of Object.keys(b||{}).sort())if((/(art|theme|form|skin|palette|element|projectile|tint|color|pfam|Kind)/i.test(k)||['_l23fx','_s9a','_s81003','_frRealm','_s7warden'].includes(k))&&!k.startsWith('_r46')&&['string','boolean','number'].includes(typeof b[k]))art[k]=b[k];return JSON.stringify([run.stage,e?.type||'',b?.kind||'',art]);}
function r46Attach(e){if(!r46Eligible(e))return;
 const id=R46_ART.aliases[run.stage+'|'+e.type];if(!id||e._r46?.model===id)return;
 e._r46={id:++R46.serial,model:id,head:Math.PI/2+(e.spin||0),age:0,dx:0,dy:0,lastX:e.x,lastY:e.y};
 const M=r46Model(e),span=r46Span(e);e._drawW=e._drawH=span;
 r46Log(e,'identity',{model:id,hp:e.hp,span});
}
function r46Span(e){const M=r46Model(e);return Math.max(e.w,e.h)*(M.nativeRatios[e.type]||1)*(e._scale??1);}
function r46Angle(e){const a=e._dyingT!=null?Math.PI/2+(e.spin||0):e._r46?.head??Math.PI/2+(e.spin||0);return Math.PI/2+s1aDir(a,16)*TAU/16;}
function r46Point(e,socket='centre'){const M=r46Model(e);if(!M)return null;const p=M.sockets[socket]||M.sockets.centre,a=r46Angle(e)-Math.PI/2,c=Math.cos(a),s=Math.sin(a),k=r46Span(e)/M.span,x=(p[0]-64)*k,y=(p[1]-64)*k;
 return{x:e.x+x*c-y*s,y:e.y+x*s+y*c,angle:a+Math.PI/2,socket};}
function r46Nearest(e,x,y){if(!r46Model(e))return{x,y};const points=e._modJet?[-1,1].map(s=>modularJetPoint(e,s)).filter(p=>!p._disabled):['port','starboard','centre','core'].map(k=>r46Point(e,k));return points.reduce((a,p)=>Math.hypot(p.x-x,p.y-y)<Math.hypot(a.x-x,a.y-y)?p:a,points[0]||{x,y});}
function r46RouteRound(e,b,p){if(!b||b.dead||b._ai27Held||b._r46Routed)return;const dx=p.x-b.x,dy=p.y-b.y;b.x=p.x;b.y=p.y;
 for(const[x,y]of[['ox','oy'],['_x0','_y0'],['x0','y0'],['_originX','_originY'],['startX','startY'],['_startX','_startY']]){if(Number.isFinite(b[x]))b[x]+=dx;if(Number.isFinite(b[y]))b[y]+=dy;}
 b._r46Routed=true;b._r46Owner=e;}
spawnEnemy=function(type,x,y,opt={}){
 // Campaign wave aliases and direct preview/canonical spawns share one factory.
 const mapped=run.stage===7&&R46.factories[type],e=R46.base.spawn.call(this,mapped||type,x,y,opt);
 if(!e)return e;r46Attach(e);return e;
};
XART.get=function(k){const im=R46.base.get.apply(this,arguments);if(im)R46.tags.set(im,{key:k});return im;};
xartTint=function(k,color){const im=R46.base.tint.apply(this,arguments);if(im)R46.tags.set(im,{key:k,color});return im;};
combatHardpoint=function(e,ox,oy){if(!r46Model(e))return R46.base.hardpoint.apply(this,arguments);
 return r46Point(e,Math.abs(ox)<.08&&Math.abs(oy)<.08?'core':ox<-.08?'port':ox>.08?'starboard':'centre');};
bf22Mount=function(e,socket,hover){return r46Model(e)?r46Point(e,socket):R46.base.mount.apply(this,arguments);};
modularJetMount=function(e,side){if(!r46Model(e)||!e._modJet)return R46.base.jetMount.apply(this,arguments);return r46Point(e,side<0?'port':'starboard');};
modularJetPoint=function(e,side){if(!r46Model(e)||!e._modJet)return R46.base.jetPoint.apply(this,arguments);
 const p=modularJetMount(e,side),id=side<0?'left':'right',a=Math.PI/2+s1aDir(e._modJetAngles?.[id]??Math.PI/2,32)*TAU/32,
 reach=Math.max(e.w,e.h)*1.28*.32*.43;
 return{x:p.x+Math.cos(a)*reach,y:p.y+Math.sin(a)*reach,aim:a,angle:a,_disabled:!!e._r30&&e._r30[id].hp<=0,socket:side<0?'port':'starboard'};};
air17Ports=function(e){if(!r46Model(e))return R46.base.ports.apply(this,arguments);
 if(e._modJet)return[-1,1].map(s=>modularJetPoint(e,s)).filter(p=>!p._disabled);
 return['port','starboard'].map(k=>r46Point(e,k));};
function r46Fly(e,tx,ty,speed,turn,dt){const A=e._r46,want=Math.atan2(ty-e.y,tx-e.x);A.head+=clamp(s1aAngle(want-A.head),-turn*dt,turn*dt);e.x+=Math.cos(A.head)*speed*dt;e.y+=Math.sin(A.head)*speed*dt;e.spin=A.head-Math.PI/2;}
s4ChaseTick=function(e,dt){if(!r46Model(e)||!['s4interceptor','s4rocket'].includes(e.type))return R46.base.chase.apply(this,arguments);
 const A=e._r46,C=air17State(e);A.routeAge=(A.routeAge||0)+dt;e.shoots=false;e.fireCd=e._fcd=999;e._s4Act=null;e._frFlight=false;
 if(e.type==='s4rocket')C.role='rocketeer';
 if(A.homeX==null){A.homeX=clamp(e.x,camLeftX()+110,camRightX()-110);A.side=e.x<worldWidth()/2?1:-1;}
 if(A.routeAge<1.8)r46Fly(e,A.homeX,PLAY.y+110,140,2.2,dt);
 else if(A.routeAge<11.0){const t=(A.routeAge-1.8)*.86,tx=clamp(A.homeX+Math.sin(t)*A.side*135,camLeftX()+85,camRightX()-85),ty=PLAY.y+135+Math.sin(t*.72)*50;
  r46Fly(e,tx,ty,['tell','fire'].includes(C.phase)?78:112,2.2,dt);
 }else{r46Fly(e,A.homeX-A.side*130,VH+180,215,1.9,dt);if(e.y>VH+110)e.dead=true;}
 air17Tick(e,dt);
};
ai27Begin=function(e,dt){r46Attach(e);if(r46Eligible(e))e._r46BulletStart=eBullets.length;if(e._r46){const A=e._r46;A.beforeX=e.x;A.beforeY=e.y;A.age+=dt;A.dt=dt;A.first=eBullets.length;}return R46.base.beginAI.apply(this,arguments);};
ai27End=function(e,old){const r=R46.base.endAI.apply(this,arguments),A=e?._r46;
 if(r46Eligible(e))for(let i=e._r46BulletStart||0;i<eBullets.length;i++){const b=eBullets[i];if(!b||b.dead)continue;if(!b._r46Owner){if(r46Model(e)){const p=r46Nearest(e,b.x,b.y);r46RouteRound(e,b,p);r46Flash(e,{...p,angle:Math.atan2(b.vy,b.vx)},r46Physical(b.kind));}b._r46Owner=e;r46Log(e,'shot',{kind:b.kind,x:b.x,y:b.y});}b._r46Glyph=r46GlyphSignature(b,e);}
 if(!A)return r;
 const dx=e.x-A.beforeX,dy=e.y-A.beforeY,dt=Math.max(.001,A.dt||1/60);A.dx=dx/dt;A.dy=dy/dt;
 if(!A.routeAge){let want=Math.PI/2+(e.spin||0);
  if(e._cp22Dash)want=e._cp22Dash.a;
  else if(e._fb2Stealth)want=FB2_DIR_ANG[e._fb2Stealth.direction]??want;
  else if(e._cp22Flight?.mode==='charge'&&e._cp22Flight.phase==='fire')want=e._cp22Flight.angle;
  else if((/^l6v_|^s6dart$|^s5interceptor$|^s5skimmer$|^s8interceptor$|^s8spread$|^s8crescent$|^s8symbiote$|^s9interceptor$|^s9comet$|^echof$/.test(e.type)||e._vp12)&&Math.hypot(dx,dy)/dt>32)want=Math.atan2(dy,dx);
  const still=eb11Queue(e)?._eb11?.started||e._cp22Sewer&&['tell','fire'].includes(e._cp22Sewer.phase);
  if(!still||e._dyingT!=null)A.head+=clamp(s1aAngle(want-A.head),-2.8*dt,2.8*dt);
 }
 for(let i=A.first||0;i<eBullets.length;i++){const b=eBullets[i];if(!b||b.dead||b._r46Owner)continue;b._r46Owner=e;r46Log(e,'shot',{kind:b.kind,x:b.x,y:b.y});}
 return r;
};
function r46Pose(e){const A=e._r46,M=r46Model(e);let kind='idle',value=(efxClock*.9)%1;
 if(M.id.startsWith('bf_')){const p=bf22State(e,'idle',0);kind=p.kind;value=p.value;}
 else{const req=e._air13Motion;
  if(req){kind=req.kind;value=req.t/req.dur;}else if(e._s8Roll){kind='roll';value=e._s8Roll.t/e._s8Roll.dur;}
  else if(e._barrelT>0){kind='roll';value=1-e._barrelT/.72;}
  else if(efxClock-(A.fireAt??-999)<.35){kind='attack';value=(efxClock-A.fireAt)/.35;}
  else if(Math.abs(A.dx)>18){kind='drift';value=A.dx<0?.2:.7;}}
 if(e._dyingT!=null){kind='idle';value=0;}
 const B=M.banks[kind]||M.banks.idle;return{kind,row:B.row+Math.min(B.frames-1,Math.floor(((value%1+1)%1)*B.frames)),frame:Math.floor(((value%1+1)%1)*B.frames)};}
function r46Blit(M,row,angle,x,y,size,color=null,alpha=1){if(!M||!XART.rdy(M.key))return false;
 const d=s1aDir(angle,M.dirs),c=M.cell;let im=XART.get(M.key),sx=d*c,sy=row*c;
 if(color){const id=M.key+'|'+row+'|'+d+'|'+color;let cached=R46.tints.get(id);if(!cached){cached=document.createElement('canvas');cached.width=cached.height=c;const g=cached.getContext('2d');g.drawImage(im,sx,sy,c,c,0,0,c,c);g.globalCompositeOperation='source-in';g.fillStyle=color;g.fillRect(0,0,c,c);if(R46.tints.size>=48)R46.tints.delete(R46.tints.keys().next().value);R46.tints.set(id,cached);}im=cached;sx=sy=0;}
 const old=R46.painting;R46.painting=true;ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;try{ctx.drawImage(im,sx,sy,c,c,x-size/2,y-size/2,size,size);}finally{ctx.restore();R46.painting=old;}return true;}
function r46DrawBody(e){const M=r46Model(e),P=r46Pose(e),a=r46Angle(e),size=r46Span(e)*M.cell/M.span;
 r46Blit(M,P.row,a,e.x+6,e.y+13,size,'#000000',.23);
 if(e._dyingT==null&&!e._r46.noExhaust&&!(M.id.includes('water_undertow')||M.id.includes('horizon'))){
  for(const k of ['exhaustPort','exhaustStarboard']){const p=r46Point(e,k),B=R46_FEEDBACK.banks['exhaust'+run.stage];r46Blit(B,Math.floor(efxClock*24)%B.frames,p.angle,p.x,p.y,42);}}
 r46Blit(M,P.row,a,e.x,e.y,size,e.flash>0?hitFlashColor(e):null);
 e._r46Rendered={key:M.key,kind:P.kind,frame:P.frame,row:P.row,dir:s1aDir(a,M.dirs),size,angle:a};
}
drawModularJet=function(e){if(!r46Model(e)||!e._modJet)return R46.base.jetDraw.apply(this,arguments);
 for(const side of[-1,1]){if(e._r30?.[side<0?'left':'right'].hp<=0)continue;const p=modularJetMount(e,side),a=e._modJetAngles?.[side<0?'left':'right']??Math.PI/2,B=R46_ART.modules['jet_'+(e._modJet==='desert'?'rotary':e._modJet==='black'?'missile':'laser')];
  r46Blit(B,0,a,p.x,p.y,Math.max(e.w,e.h)*1.28*.32*B.cell/128,e.flash>0?hitFlashColor(e):null);
 }return true;};
function r46StaticDraw(im,args,tag,root){const B=R46_STATIC.banks[tag?.key];if(!B||!XART.rdy(B.key))return false;
 const rect=args.length===8?args.slice(0,4):null,row=B.rects.findIndex(r=>r===null&&rect===null||r&&rect&&r.every((v,i)=>v===rect[i]));if(row<0)return false;
 const U=root.inverse().multiply(ctx.getTransform()),a=Math.atan2(U.b,U.a),box=args.slice(-4),x=box[0]+box[2]/2,y=box[1]+box[3]/2,p=U.transformPoint(new DOMPoint(x,y)),src=rect||[0,0,...B.sourceSize],scale=Math.max(Math.hypot(U.a,U.b),Math.hypot(U.c,U.d)),size=B.cell/B.scale*Math.min(Math.abs(box[2])/src[2],Math.abs(box[3])/src[3])*scale;
 ctx.save();ctx.setTransform(root);try{r46Blit(B,row,a+Math.PI/2,p.x,p.y,size,tag.color||null);}finally{ctx.restore();}R46.staticDraws++;return true;}
drawEnemy=function(e){r46Attach(e);const M=r46Model(e);if(e.dead)return R46.base.draw.apply(this,arguments);
 if(!M){if(!r46Eligible(e))return R46.base.draw.apply(this,arguments);const original=ctx.drawImage,root=ctx.getTransform();ctx.drawImage=function(im,...args){if(!R46.painting&&r46StaticDraw(im,args,R46.tags.get(im)||AF21.tags.get(im),root))return;return original.call(this,im,...args);};try{return R46.base.draw.apply(this,arguments);}finally{ctx.drawImage=original;}}
 const previous=R46.actor,original=ctx.drawImage;R46.actor=e;r46DrawBody(e);
 const legacy=new Set(M.legacyKeys);ctx.drawImage=function(im,...args){if(R46.painting)return original.call(this,im,...args);
  const tag=R46.tags.get(im)||AF21.tags.get(im),key=tag?.key||'';
  if(AF21.painting||legacy.has(key)||key.startsWith('r46_'))return;
  return original.call(this,im,...args);
 };
 try{return R46.base.draw.apply(this,arguments);}finally{ctx.drawImage=original;R46.actor=previous;
  e._drawW=e._drawH=r46Span(e);e._bf22Rendered={...(e._bf22Rendered||{}),id:M.id,key:M.key,scale:r46Span(e)/M.span,dx:0,dy:0,angle:r46Angle(e)-Math.PI/2};}
};
function r46Flash(e,p,rocket=false){if(!r46Live(e)||e._r46Hold>efxClock&&R46.releasing!==e)return;const last=e._r46Flash||{},mouth=Math.round(p.x-e.x)+':'+Math.round(p.y-e.y);if(efxClock-(last[mouth]??-9)<.025)return;last[mouth]=efxClock;e._r46Flash=last;
 const bank=({5:'void',6:'sky',7:'toxic',8:'void',9:'water'})[run.stage];
 R46.fx.push({owner:e,p:{...p},origin:{x:e.x,y:e.y},age:0,life:.11,rocket,bank:!rocket&&bank?bank+'_muzzle':null});if(e._r46)e._r46.fireAt=efxClock;r46Log(e,'muzzle',{x:p.x,y:p.y});}
wm26Emit=function(e,x,y,a,family,color,opt={}){if(!opt.player&&e?._r46Hold>efxClock&&R46.releasing!==e)return;if(!opt.player&&r46Model(e)){const p={x,y,angle:a};r46Flash(e,p,/missile|rocket/.test(family||''));return;}return R46.base.muzzle.apply(this,arguments);};
navalFlash=function(e,p,scale,family,opt={}){const native=e||ai27Context;if(native?._r46Hold>efxClock&&R46.releasing!==native)return;const owner=r46Model(e)?e:r46Model(ai27Context)?ai27Context:null;if(owner){r46Flash(owner,{...p,angle:p.angle??p.aim??Math.PI/2},/missile|rocket/.test(family||''));return;}return R46.base.naval.apply(this,arguments);};
function r46Physical(kind){return /missile|rocket|^emr$|^emissile$|^s1jungleMissile$/.test(kind||'');}
_lockLaunch=function(L,shot){const old=R46.nativeLockOwner;R46.nativeLockOwner=L.src;try{return R46.base.lockLaunch.apply(this,arguments);}finally{R46.nativeLockOwner=old;}};
eShootT=function(x,y,a,speed,kind,opt={}){const e=opt.owner||ai27Context;
 const wait=r46Eligible(e)&&r46Physical(kind)&&e._modTurret?.weapon!=='missile'&&R46.nativeLockOwner!==e;
 if(!wait){const p=r46Model(e)?r46Nearest(e,x,y):{x,y},b=R46.base.shot.call(this,p.x,p.y,a,speed,kind,opt);if(r46Model(e)&&b&&!b.dead&&!b._ai27Held){r46RouteRound(e,b,p);r46Log(e,'shot',{kind,x:b.x,y:b.y});}return b;}
 e._r46Hold=efxClock+.06;const b=R46.base.shot.call(this,x,y,a,speed,kind,{...opt,owner:e,noMuzzle:true,silent:true});
 if(!b||b.dead||b._ai27Held)return b;const index=eBullets.indexOf(b);if(index<0)return b;eBullets.splice(index,1);
 const dx=x-e.x,dy=y-e.y,offset=s1aAngle(a-Math.atan2(targetShip(x,y).y-y,targetShip(x,y).x-x));
 let socket=null,distance=Infinity;if(e._modJet){for(const side of[-1,1]){const p=modularJetPoint(e,side),d=Math.hypot(p.x-x,p.y-y);if(d<distance){distance=d;socket=side<0?'moduleL':'moduleR';}}}
 else if(r46Model(e))for(const k of['port','starboard','centre','core']){const p=r46Point(e,k),d=Math.hypot(p.x-x,p.y-y);if(d<distance){distance=d;socket=k;}}
 b._r46Pending=true;b._r46Owner=e;R46.pending.add(b);
 const lock=enemyLockOn(e,diffKey==='furious'?.62:diffKey==='hard'?.70:.80,{fire:L=>{
  if(!r46Live(e)){b.dead=true;R46.pending.delete(b);return;}
  const p=socket==='moduleL'||socket==='moduleR'?modularJetPoint(e,socket==='moduleL'?-1:1):socket?r46Point(e,socket):{x:e.x+dx,y:e.y+dy},T=targetShip(p.x,p.y),ang=Math.atan2(T.y-p.y,T.x-p.x)+offset,sp=Math.hypot(b.vx,b.vy)||speed;
  Object.assign(b,{x:p.x,y:p.y,vx:Math.cos(ang)*sp,vy:Math.sin(ang)*sp,ang,_r46Pending:false});eBullets.push(b);R46.pending.delete(b);
  b._r46Glyph=r46GlyphSignature(b,e);
  const old=R46.releasing;R46.releasing=e;try{r46Flash(e,{...p,angle:ang,socket},true);if(efxClock-(e._r46MissileSound??-9)>.10){Audio.SFX.enemyMissile?.();e._r46MissileSound=efxClock;}}finally{R46.releasing=old;}
  r46Log(e,'missile-release',{kind:b.kind,x:b.x,y:b.y,lock:L.id});
 }});
 if(!lock){b.dead=true;R46.pending.delete(b);}else r46Log(e,'missile-lock',{kind,lock:lock.id});return b;
};
Audio.SFX.enemyMissile=function(){const e=ai27Context;if(e?._r46Hold>efxClock&&R46.releasing!==e)return;return R46.base.missileCue?.apply(this,arguments);};
combatAtlasFx=function(x,y,key,cols,rows,start,count,opt={}){if(opt.owner?._r46Hold>efxClock&&R46.releasing!==opt.owner)return true;return R46.base.atlasFx.apply(this,arguments);};
combatWarningDraw=function(e,opt){const C=e?._air17,missile=e?._modTurret?.weapon==='missile'||['s4missile','s4sam','s4heavyjet','s4rocket','s5satellite'].includes(e?.type)||C?.missile;
 if(r46Eligible(e)&&missile)return;return R46.base.warning.apply(this,arguments);};
function r46DrawGlyph(b){if(!b?._r46Owner||b._r46Pending||run.stage<4||run.stage>9)return false;const sig=b._r46Glyph||r46GlyphSignature(b),B=R46_ORDNANCE.glyphs[sig];
 if(!B){R46.glyphMisses.set(sig,(R46.glyphMisses.get(sig)||0)+1);return false;}if(!XART.rdy(B.key))return true;
 const age=projectileVisualAge(b),angle=Math.atan2(b.vy,b.vx),frame=Math.floor(age*B.fps)%B.frames;
 const size=B.cell*(Math.max(b.w||0,b.h||0)<=36?1.16:1);r46Blit(B,frame,angle,b.x,b.y,size);R46.glyphDraws++;return true;}
ovSonicProjectileDraw=function(b){return r46DrawGlyph(b)||R46.base.early.apply(this,arguments);};
air17DrawProjectile=function(b){return r46DrawGlyph(b)||R46.base.airProjectile.apply(this,arguments);};
updateEffects=function(dt){const r=R46.base.effects.apply(this,arguments);for(const f of R46.fx)f.age+=dt;R46.fx=R46.fx.filter(f=>f.age<f.life&&r46Live(f.owner));for(const b of R46.pending)if(!r46Live(b._r46Owner)){b.dead=true;R46.pending.delete(b);}return r;};
drawNavalFlashes=function(){const r=R46.base.flashes.apply(this,arguments);for(const f of R46.fx){const x=f.p.x+f.owner.x-f.origin.x,y=f.p.y+f.owner.y-f.origin.y;if(f.bank){const B=R46_FEEDBACK.banks[f.bank];r46Blit(B,Math.min(B.frames-1,Math.floor(f.age/f.life*B.frames)),f.p.angle,x,y,38);}else{const key=f.rocket?'rocket_muzzle':'muzzle',B=S1A_ART[key];s1aBlit(key,Math.min(B.frames-1,Math.floor(f.age/f.life*B.frames)),f.p.angle,x,y,f.rocket?38:28);}}return r;};
stageLoadBegin=function(n,keys){if(n>=4&&n<=9){const models=Object.values(R46_ART.models).filter(m=>m.stages.includes(n)),statics=Object.values(R46_STATIC.banks).filter(b=>b.stages.includes(n)),ordnance=Object.entries(R46_ORDNANCE.glyphs).filter(([sig])=>JSON.parse(sig)[0]===n).map(([,b])=>b);keys=[...(keys||[]),...models.map(m=>m.key),...statics.map(b=>b.key),...ordnance.map(b=>b.key),...Object.values(R46_ART.modules).map(m=>m.key),...Object.values(R46_FEEDBACK.banks).map(m=>m.key),...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];}return R46.base.load.call(this,n,keys);};
beginStage=function(){for(const b of R46.pending)b.dead=true;R46.pending.clear();R46.events=[];R46.fx=[];R46.tints.clear();return R46.base.begin.apply(this,arguments);};
killEnemy=function(e){const result=R46.base.kill.apply(this,arguments);if(!r46Live(e)&&(e?._r46||e?._r46Hold!=null)){R46.fx=R46.fx.filter(f=>f.owner!==e);for(const b of R46.pending)if(b._r46Owner===e){b.dead=true;R46.pending.delete(b);}playerLocks=playerLocks.filter(L=>L.src!==e);}return result;};
globalThis.BOF_ENEMY_FLIGHT_REVIEW={state:R46,art:R46_ART};
