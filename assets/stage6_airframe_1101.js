"use strict";
/* Mike's Stage6 rule: ONE canonical solid hull per jet.1015 own-pixel light,
   registered direction cells and separate animated gun/exhaust effects only.
   Native wind/helper/stealth entrance and attack/death owners remain. */
const S611={base:{spawn:spawnEnemy,model:r46Model,span:r46Span,pose:r46Pose,body:r46DrawBody,
 end:ai27End,shot:eShootT,early:ovSonicProjectileDraw,final:drawCombatFinalProjectile,
 flash:r46Flash,load:stageLoadBegin,draw:drawEnemy,dash:cp22DashDraw,lock:_lockLaunch,nearest:r46Nearest,flashes:drawNavalFlashes,blit:ASSETS.blit},events:[],serial:0,
 jetModels:{l6v_s0:'fighter_navy',l6v_s1:'bomber_navy',l6v_s2:'fighter_teal',
 l6v_r0:'fighter_black',l6v_r1:'bomber_black',l6v_r2:'heavy_wind',
 l6v_b0:'fighter_black',l6v_b1:'bomber_black',l6v_b2:'heavy_wind'},
 grounds:new Set(['modturret','mgturret','rockturret','turret','microturret','turdrone'])};
for(const B of Object.values(S611_ART.banks))XART._src[B.key]=B.path;
function s611Eligible(e){return run.stage===6&&!run._gp4StageX&&e&&!e._boss&&!e.boss&&!e._mini&&!e._amini&&!e._rebels&&!e.prop&&!e._prop&&!(e._fb2Stealth&&!e._cp22Flight);}
function s611Name(e){if(!s611Eligible(e))return null;if(e._cp22Dash||e.type==='cp22dasher')return'wind_helper';
 if(e._cp22Flight)return e._cp22Flight.mode==='charge'?'heavy_wind':e._cp22Flight.mode==='rain'?'fighter_black':'bomber_navy';
 if(S611.jetModels[e.type])return S611.jetModels[e.type];
 if(['s1jetbomber_b','s1jetbomber','s6bomber'].includes(e.type))return e._s6Strike?.direction==='west'||e._s6Strike?.direction==='north'?'bomber_black':'bomber_navy';
 const id=R46_ART.aliases['6|'+e.type];return({bf_sky_zephyr:'wind_zephyr',bf_sky_gale:'wind_gale',bf_sky_stratus:'wind_stratus',bf_dasher:'wind_helper'})[id]||null;}
function s611M(e){const n=s611Name(e);return n&&S611_ART.models[n];}
function s611Log(e,event,data={}){S611.events.push({id:e?._s611?.id,type:e?.type,event,t:efxClock,...data});if(S611.events.length>1800)S611.events.shift();}
function s611Attach(e){const n=s611Name(e);if(!n)return;const m=S611_ART.models[n];
 if(e._s611?.model!==n){e._s611={id:++S611.serial,model:n,head:Math.PI/2,gun:0,original:[e.w,e.h],hullHP:e.hp};
  if(!m.preservedWind){const b=m.bank;e.w=m.spanWorld*.86;e.h=m.spanWorld*.86;}
  s611Log(e,'canonical-hull',{model:n,hp:e.hp,preservedWind:m.preservedWind});}
}
for(const [name,m]of Object.entries(S611_ART.models)){
 const B=m.bank;B.id='s611_'+name;B.nativeRatios={};B.legacyKeys=[...new Set(Object.values(R46_ART.models).filter(a=>a.stages?.includes(6)).flatMap(a=>a.legacyKeys||[]))];
}
spawnEnemy=function(type,x,y,opt={}){if(run.stage===6&&!run._gp4StageX&&S611.grounds.has(type))return null;
 const e=S611.base.spawn.apply(this,arguments);if(e)s611Attach(e);return e;};
r46Model=function(e){const m=s611M(e);if(m){s611Attach(e);return m.bank;}return S611.base.model.apply(this,arguments);};
r46Span=function(e){const m=s611M(e);return m?m.spanWorld*(e._scale??1):S611.base.span.apply(this,arguments);};
r46Pose=function(e){if(s611M(e))return{kind:'idle',frame:0,row:0};return S611.base.pose.apply(this,arguments);};
ai27End=function(e,old){const out=S611.base.end.apply(this,arguments),m=s611M(e),A=e?._r46;if(!m||!A)return out;s611Attach(e);const S=e._s611,dt=Math.max(.001,A.dt||1/60);
 let target=S.head;
 if(e._cp22Dash)target=e._cp22Dash.a;
 else if(e._cp22Flight)target=e._cp22Flight.mode==='charge'&&e._cp22Flight.phase==='fire'?e._cp22Flight.angle:FB2_DIR_ANG[e._fb2Stealth.direction];
 else if(e._s6Strike)target=FB2_DIR_ANG[e._s6Strike.direction];
 else if(['s6mine','s6buoy','s6probe','s6turbine'].includes(e.type))target=Math.PI/2;
 else if(Math.hypot(A.dx,A.dy)>35)target=Math.atan2(A.dy,A.dx);
 S.head+=clamp(s1aAngle(target-S.head),-4.5*dt,4.5*dt);A.head=S.head;return out;
};
const S611_END=ai27End;ai27End=function(e,old){const start=e?._r46BulletStart??eBullets.length,r=S611_END.apply(this,arguments),m=s611M(e);if(!m||m.preservedWind)return r;
 // Legacy fleet guns also append rounds through eShoot/eMG. Route those
 // actual rounds, including first-update immunity, through the same sockets.
 for(let i=start;i<eBullets.length;i++){const b=eBullets[i];if(!b||b.dead||b._s611Routed||b._r46Owner!==e)continue;const p=s611Gun(e,b.x,b.y),speed=Math.hypot(b.vx,b.vy);delete b._r46Routed;r46RouteRound(e,b,p);b._s611Owner=e;b._s611Routed=true;
  if(!r46Physical(b.kind)){b.vx=Math.cos(p.angle)*speed;b.vy=Math.sin(p.angle)*speed;b.ang=p.angle;b._s611Ammo='slug';}
  s611Log(e,'shot',{kind:b.kind,x:b.x,y:b.y,angle:p.angle,model:e._s611.model,physical:r46Physical(b.kind)});}
 return r;};
function s611Point(e,p){const B=s611M(e).bank,a=r46Angle(e)-Math.PI/2,c=Math.cos(a),s=Math.sin(a),k=r46Span(e)/B.span,x=(p[0]-64)*k,y=(p[1]-64)*k;return{x:e.x+x*c-y*s,y:e.y+x*s+y*c,angle:a+Math.PI/2};}
function s611Blit(B,f,a,x,y,size,tint=null,alpha=1){if(!B||!XART.rdy(B.key))return false;const d=s1aDir(a,B.dirs),c=B.cell,im=tint?xartTint(B.key,tint,1):XART.get(B.key),old=R46.painting;R46.painting=true;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 try{ctx.drawImage(im,d*c,clamp(f|0,0,B.frames-1)*c,c,c,x-size/2,y-size/2,size,size);}finally{ctx.restore();R46.painting=old;}return true;}
r46DrawBody=function(e){const m=s611M(e);if(!m)return S611.base.body.apply(this,arguments);s611Attach(e);const B=m.bank,a=r46Angle(e),size=r46Span(e)*B.cell/B.span;
 r46Blit(B,0,a,e.x+5,e.y+13,size,'#000000',.20);
 if(e._dyingT==null)for(const tail of m.tails){const p=s611Point(e,tail);s611Blit(S611_ART.banks.thruster,Math.floor(efxClock*24)%S611_ART.banks.thruster.frames,p.angle,p.x,p.y,m.preservedWind?30:34);}
 r46Blit(B,0,a,e.x,e.y,size,e.flash>0?hitFlashColor(e):null);
 if(!(e.flash>0)&&e._dyingT==null){ctx.save();ctx.globalCompositeOperation='lighter';r46Blit(m.glow,0,a,e.x,e.y,size,null,pxgStep(.5+.5*Math.sin(efxClock*6+e._s611.id)));ctx.restore();}
 e._r46Rendered={key:B.key,kind:'idle',frame:0,row:0,dir:s1aDir(a,B.dirs),size,angle:a};e._s611Rendered={...e._r46Rendered,model:e._s611.model,exhausts:e._dyingT==null?m.tails.length:0};
};
function s611Gun(e,x,y){const m=s611M(e);if(!m)return null;let i;if(Math.abs(x-e.x)<8)i=(e._s611.gun++)%m.guns.length;else{
 const points=m.guns.map((p,i)=>({p:s611Point(e,p),i}));i=points.reduce((a,b)=>Math.hypot(b.p.x-x,b.p.y-y)<Math.hypot(a.p.x-x,a.p.y-y)?b:a).i;}
 return s611Point(e,m.guns[i]);}
r46Nearest=function(e,x,y){const m=s611M(e);if(!m||m.preservedWind)return S611.base.nearest.apply(this,arguments);const points=m.guns.map(p=>s611Point(e,p));return points.reduce((a,b)=>Math.hypot(b.x-x,b.y-y)<Math.hypot(a.x-x,a.y-y)?b:a);};
eShootT=function(x,y,a,speed,kind,opt={}){const e=opt.owner||ai27Context,m=s611M(e);if(!m)return S611.base.shot.apply(this,arguments);s611Attach(e);
 const radial=m.preservedWind&&['s6mine','s6buoy','s6probe','s6turbine'].includes(e.type),p=radial?{x,y,angle:a}:s611Gun(e,x,y);
 const facing=m.preservedWind||radial?a:p.angle,b=S611.base.shot.call(this,p.x,p.y,facing,speed,kind,{...opt,owner:e});
 if(b&&!b.dead&&!b._ai27Held){b._s611Owner=e;b._s611Routed=true;if(!m.preservedWind&&!r46Physical(kind))b._s611Ammo='slug';s611Log(e,'shot',{kind,x:b.x,y:b.y,angle:facing,model:e._s611.model,physical:r46Physical(kind)});}return b;
};
_lockLaunch=function(L,shot){const first=eBullets.length,r=S611.base.lock.apply(this,arguments),e=L.src,m=s611M(e);
 if(m&&!m.preservedWind)for(let i=first;i<eBullets.length;i++){const b=eBullets[i];if(!b||b.dead||!r46Physical(b.kind))continue;const p=s611Gun(e,b.x,b.y),speed=Math.hypot(b.vx,b.vy);Object.assign(b,{x:p.x,y:p.y,vx:Math.cos(p.angle)*speed,vy:Math.sin(p.angle)*speed,ang:p.angle,_s611Owner:e});}return r;};
r46Flash=function(e,p,rocket=false){if(!s611M(e))return S611.base.flash.apply(this,arguments);if(!r46Live(e)||e._r46Hold>efxClock&&R46.releasing!==e)return;
 const key=Math.round(p.x-e.x)+':'+Math.round(p.y-e.y),last=e._s611Flash||(e._s611Flash={});if(efxClock-(last[key]??-9)<.025)return;last[key]=efxClock;
 const angle=s611M(e).preservedWind?p.angle:r46Angle(e);R46.fx.push({owner:e,p:{...p,angle},origin:{x:e.x,y:e.y},age:0,life:.10,rocket,_s611:true});e._r46.fireAt=efxClock;s611Log(e,'muzzle',{x:p.x,y:p.y,angle});};
drawNavalFlashes=function(){const all=R46.fx,ours=all.filter(f=>f._s611);R46.fx=all.filter(f=>!f._s611);try{S611.base.flashes.apply(this,arguments);}finally{R46.fx=all;}
 for(const f of ours){const B=S611_ART.banks.muzzle;s611Blit(B,Math.min(B.frames-1,Math.floor(f.age/f.life*B.frames)),f.p.angle,f.p.x+f.owner.x-f.origin.x,f.p.y+f.owner.y-f.origin.y,f.rocket?24:18);}};
// Retired generic nose-flare drawing is separate from the native launcher.
// Keep one compact release at the real barrel, including legacy eMG paths.
drawEnemy=function(e){const old=S611.drawing;if(s611M(e))S611.drawing=e;try{return S611.base.draw.apply(this,arguments);}finally{S611.drawing=old;}};
ASSETS.blit=function(key){if(S611.drawing&&/^t_muz[01]$/.test(key))return;return S611.base.blit.apply(this,arguments);};
function s611Projectile(b){return s611Blit(S611_ART.banks.slug,Math.floor(projectileVisualAge(b)*22)%S611_ART.banks.slug.frames,Math.atan2(b.vy,b.vx),b.x,b.y,28);}
ovSonicProjectileDraw=function(b){return b?._s611Ammo?s611Projectile(b):S611.base.early.apply(this,arguments);};
drawCombatFinalProjectile=function(b){return b?._s611Ammo?s611Projectile(b):S611.base.final.apply(this,arguments);};
cp22DashDraw=function(e){if(!s611M(e))return S611.base.dash.apply(this,arguments);const D=e._cp22Dash;if(e.dead||e._dyingT!=null||D.phase!=='tell')return;
 const x=D.side>0?D.left+2:D.right-2;combatWarningDraw(e,{x,y:D.y,ex:D.side>0?D.right:D.left,ey:D.y,width:64,progress:clamp(D.t/D.warm,0,1),fieldOnly:true});};
stageLoadBegin=function(n,keys){if(n===6)keys=[...(keys||[]),...Object.values(S611_ART.banks).map(b=>b.key)];return S611.base.load.call(this,n,keys);};
globalThis.BOF_SKY_AIRFRAMES={state:S611,art:S611_ART};
