"use strict";
/* PixelLab's real branching poses, split into synchronized near/far plates.
   Encounter clocks, warnings, hit flashes and projectile collisions stay native. */
const L21={base:{load:stageLoadBegin,warm:d20Warm,fx:d20Fx,body:d20MainBody,
 draw:mr27Draw,over:mr27Over,arc:sa14BlueArc,charge:sa14ChargeFx,beam:av3Beam,
 projectile:drawCombatFinalProjectile,ball:tb28BallDraw,warfare:drawStage4WarfareProjectile,er26:er26ProjectileDraw},draws:{},hull:null,links:null,last:{}};
for(const bank of Object.values(L21_ART.banks))for(const a of bank.frames)XART._src[a.key]=a.path;
function l21Keys(){return Object.values(L21_ART.banks).flatMap(b=>b.frames.map(a=>a.key));}
function l21Warm(){let ready=true;for(const k of l21Keys())if(!XART.rdy(k))ready=false;return ready;}
stageLoadBegin=function(n,keys){return L21.base.load.call(this,n,[4,8].includes(n)?[...(keys||[]),...l21Keys()]:keys);};
d20Warm=function(){const ready=L21.base.warm.apply(this,arguments);return l21Warm()&&ready;};
function l21Frame(name,t){const bank=L21_ART.banks[name],n=bank.frames.length;return bank.frames[((Math.floor(t*bank.fps)%n)+n)%n];}
function l21Draw(name,t,x,y,height,angle=0,alpha=1,g=ctx){const a=l21Frame(name,t);if(!XART.rdy(a.key))return false;
 const k=height/a.h;g.save();g.translate(x,y);g.rotate(angle);g.imageSmoothingEnabled=false;g.globalAlpha*=clamp(alpha,0,1);
 g.drawImage(XART.get(a.key),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);g.restore();L21.draws[name]=(L21.draws[name]||0)+1;return true;}
function l21Wrap(bank,t,b,height,angle,alpha){const x=b.x,y=b.y;
 const out=l21Draw(bank,t,x,y,height,angle,alpha);L21.last[bank]={frame:Math.floor(t*16)%32,x,y,height,angle};return out;}
// Old crescent artwork is retired from both the charge sockets and outbound
// storm. The new forks change topology across32 generated poses, not one spin.
d20Fx=function(name,t,x,y,size,angle=0,alpha=1,loop=true){if(name==='lightning_loop')return l21Draw('orb',t,x,y,size*L21_ART.banks.orb.renderScale,angle,alpha);
 return L21.base.fx.apply(this,arguments);};
d20SparksDraw=function(){for(const q of D20.sparks){const angle=q.angle+q.t*q.spin,velocity=angle+Math.atan2((28+q.t*q.speed)*q.spin,q.speed);
 l21Draw('bolt',q.t+(q.angle/TAU),q.x,q.y,42*L21_ART.banks.bolt.renderScale,velocity-L21_ART.banks.bolt.axis);}};
d20MainBody=function(b){const N=b._r30.v18,P=N.attack;if(!d20Main(b)||P?.type!=='spiralLightning')return L21.base.body.apply(this,arguments);
 const t=P.t,progress=clamp(t/P.tell,0,1),fade=clamp((P.tell+P.active-t)/.22,0,1),alpha=(.18+.82*progress)*fade,
  size=v18Size(b)*1.15*L21_ART.banks.wrap_front.renderScale*(N.archiveDepth||1);
 // Same frame, pivot and world transform, separated by the actual body blit.
 l21Wrap('wrap_back',t,b,size,0,alpha*.56);const out=L21.base.body.apply(this,arguments);l21Wrap('wrap_front',t,b,size,0,alpha);
 L21.draws.dracodia=(L21.draws.dracodia||0)+1;return out;};
function l21StormEnergy(b){const A=b?._sa14;if(!sa14Storm(b)||!A||b.dead||b.enter)return 0;const P=b._p4Final;
 return Math.max(A.glow||0,P&&['panic','ram'].includes(P.phase)?.82:P?.phase==='rear'?.46:b._s4war?.shield?.active?.16:0);}
mr27Draw=function(b){const energy=l21StormEnergy(b);if(!energy)return L21.base.draw.apply(this,arguments);
 const A=b._sa14,t=b._er26.clock,size=Math.max(b.w,b.h)*1.28*A.scale*L21_ART.banks.wrap_front.renderScale,
  alpha=clamp(.22+energy*.78,0,1),previous=L21.hull;L21.hull=b;
 l21Wrap('wrap_back',t,b,size,A.angle,alpha*.52);let out;try{out=L21.base.draw.apply(this,arguments);}finally{L21.hull=previous;}
 l21Wrap('wrap_front',t,b,size,A.angle,alpha);L21.draws.storm=(L21.draws.storm||0)+1;return out;};
function l21Link(g,x,y,angle,length,width,t,alpha){if(!(length>0))return false;
 const bank=L21_ART.banks.tether,k=clamp(width/24,.18,.65),start={x:40,y:80},end={x:248,y:80},step=(end.x-start.x-16)*k;
 g.save();g.translate(x,y);g.rotate(angle);g.beginPath();g.rect(0,-bank.h*k*.5,length,bank.h*k);g.clip();
 for(let d=0;d<length;d+=step)l21Draw('tether',t+d*.003,d+(bank.pivot[0]-start.x)*k,0,bank.h*k,0,alpha,g);
 g.restore();L21.draws.links=(L21.draws.links||0)+1;return true;}
mr27Over=function(b){if(!sa14Storm(b))return L21.base.over.apply(this,arguments);const prior=L21.links;L21.links=b;
 try{return L21.base.over.apply(this,arguments);}finally{L21.links=prior;}};
av3Beam=function(g,x,y,angle,length,width,color,t=AV3.clock,alpha=1,muzzle=true){if(L21.links&&color==='lightning')return l21Link(g,x,y,angle,length,width,t,alpha);
 return L21.base.beam.apply(this,arguments);};
sa14BlueArc=function(x,y,angle,length,clock,alpha){if(L21.hull)return l21Link(ctx,x,y,angle,length,5,clock,alpha);
 return L21.base.arc.apply(this,arguments);};
sa14ChargeFx=function(b,p,glow,t){if(!sa14Storm(b))return L21.base.charge.apply(this,arguments);
 l21Draw('orb',t,p.x,p.y,(24+glow*42)*L21_ART.banks.orb.renderScale,0,.4+glow*.6);L21.draws.charge=(L21.draws.charge||0)+1;};
function l21BallPaint(x,y,size,t,alpha=1){const out=l21Draw('orb',t||0,x,y,size*L21_ART.banks.orb.renderScale,0,alpha);if(out)L21.draws.stormOrbs=(L21.draws.stormOrbs||0)+1;return out;}
function l21BallShot(q){return run.stage===4&&(q?._sg17Lightning||q?._s4wKind==='orb');}
// Targeted balls have an earlier native draw route than generic projectiles.
// Own that real route too; otherwise the new art exists but never reaches play.
tb28BallDraw=function(art,x,y,size,t,alpha=1){if(run.stage===4&&art==='storm')return l21BallPaint(x,y,size,t,alpha);
 return L21.base.ball.apply(this,arguments);};
drawStage4WarfareProjectile=function(q){if(l21BallShot(q)&&l21BallPaint(q.x,q.y,62*(q.szMul||1),q.t))return true;
 return L21.base.warfare.apply(this,arguments);};
er26ProjectileDraw=function(q){if(l21BallShot(q)&&l21BallPaint(q.x,q.y,q._tb28?.size||62*(q.szMul||1),q.t))return true;
 return L21.base.er26.apply(this,arguments);};
drawCombatFinalProjectile=function(q){if(l21BallShot(q)&&l21BallPaint(q.x,q.y,q._tb28?.size||62*(q.szMul||1),q.t))return true;
 return L21.base.projectile.apply(this,arguments);};
globalThis.BOF_LIGHTNING_DEPTH=L21;
