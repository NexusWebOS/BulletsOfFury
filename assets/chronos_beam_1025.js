'use strict';
/* Mike's revised rage: discard the hammer permanently, retreat in depth,
   gather at the hip and release a two-handed wave down a committed FOV. */
const C30={base:{tick:hammerBossTick,draw:hammerBossDraw,blue:ha21Blue,depth:hammerDepthScale,
 hit:bossHitTest,weapon:hammerWeaponTargetable,fire:hammerBossChaingunFire,round:ch23BulletDraw,
 aura:c27TraceAura},events:[],masks:new Map()};
for(const s of Object.values(C30_ART.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(C30_ART.banks))for(const a of rows)BOFX.cells[a.key]=[a.sheet,...a.cell];
function c30Warm(){return Object.values(C30_ART.sheets).map(s=>XART.rdy(s.key)).every(Boolean);}
const c30Load=stageLoadBegin;
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(['shadowCharge','bossPhase','fusionBeam','laserBeamEnd','hammerThrow']);return c30Load.call(this,n,[...(keys||[]),...(n===5?Object.values(C30_ART.sheets).map(s=>s.key):[])]);};
function c30Log(type,data={}){C30.events.push({type,time:efxClock,...data});if(C30.events.length>500)C30.events.shift();}
function c30Own(b){return c25Own(b)&&!b.dead&&!!b._hammer._hf22Red&&!b._hammer._hf22Charge;}
const c30LegacyRageDone=fb2HammerRageDone;
fb2HammerRageDone=function(b){return c30Own(b)||c30LegacyRageDone.apply(this,arguments);};
function c30BudgetTick(b,dt){c29DamageBudget(b,dt);}
function c30Row(bank,f){const a=C30_ART.banks[bank];return a[Math.min(a.length-1,Math.max(0,Math.floor(f)))];}
function c30Pose(bank,f,k=1){const a=c30Row(bank,f);return{a,k,rot:0,kind:'c30_'+bank};}
// The hands stay planted on the original grips. Only the rotary cluster spins;
// minute whole-weapon recoil is shared by body, gun and foreground grips.
ch23BodyFrame=function(){return 0;};
ch23Recoil=function(b){return b._hammer.state==='chaingun'?-.8*clamp((b._hammer.chainMuzzle||0)/.09,0,1):0;};
ch23GunFrame=function(b){return b._hammer.ch23Rev>.04?1+Math.floor(b._hammer.ch23Spin||0)%16:0;};
const c30Cell=ch23Cell;
ch23Cell=function(bank,b,f=0){return bank==='barrel'?c30Row('rotor',f):c30Cell.apply(this,arguments);};
ch23BulletDraw=function(q){if(q?._ch23Round)return chaingunRoundDraw({...q,lv:2});return C30.base.round.apply(this,arguments);};
hammerBossChaingunFire=function(b){const first=eBullets.length,r=C30.base.fire.apply(this,arguments);if(c25Own(b))for(const q of eBullets.slice(first))if(q._ch23Round){q.w=10;q.h=24;q._c30Slug=true;}return r;};
function c30Scale(b){return b._hammer.c30?.scale??1;}
hammerDepthScale=function(b){return c30Own(b)?c30Scale(b):C30.base.depth.apply(this,arguments);};
hammerWeaponTargetable=function(b){return c30Own(b)||c25Own(b)&&b._hammer._hf22Charge?false:C30.base.weapon.apply(this,arguments);};
ha21Blue=function(b){if(!c25Own(b)||b.dead)return C30.base.blue.apply(this,arguments);const h=b._hammer,C=h._hf22Charge,R=h.c30;
 if(C){const u=clamp(C.t/1.8,0,1),mat=u>.59?'red':c26Material(b);return c30Pose('power_'+mat,Math.min(12,u*13));}
 if(c30Own(b)){
  if(!R)return c30Pose('cast',0);
  if(R.phase==='gather')return c30Pose('cast',Math.min(3,R.t/.6*3),R.scale);
  if(R.phase==='thrust')return c30Pose('thrust',R.t/.36*8,R.scale);
  if(R.phase==='beam')return c30Pose('cast',5+(Math.floor(R.t*14)&1),R.scale);
  return c30Pose('cast',R.phase==='recover'?7:0,R.scale);
 }
 return C30.base.blue.apply(this,arguments);
};
function c30Hand(b,release=false){const q=release?c30Pose('cast',5,c30Scale(b)):ha21Blue(b);return hb20World(q.a,q.a.tip||[128,120],b,q.k,0);}
function c30Phase(b,phase){const R=b._hammer.c30;R.phase=phase;R.t=0;b._hammer.state='c30_'+phase;b._hammer.t=0;c30Log('phase',{phase,scale:R.scale});}
function c30Retreat(b){const h=b._hammer,R=h.c30||(h.c30={scale:1,cycle:0});R.from={x:b.x,y:b.y,scale:R.scale};
 R.to={x:lerp(camLeftX(),camRightX(),R.cycle%2?.72:.28),y:viewTopY()+150};R.lock=null;R.hit=new Set();c30Phase(b,'retreat');}
function c30Start(b){const h=b._hammer;h.hammerDestroyed=true;h.hammerHP=0;h.throw=h.c25Knock=h.c29Break=h.c26Return=h.c27Combo=h._hj22Pair=h._hf22StormPair=h.recovery=null;
 // Permanent unarmed rage replaces the legacy8% hammer emergency reserve.
 h.gp4FailsafeSeen=true;h.gp4Emergency=null;
 h.mode='rage_wave';h.phasePending=false;h.comboPending=false;const A=fr27Armor(b);if(A){A.barrier=0;A.hp=0;A.active=false;A.activated=false;}b._noHit=false;c30Retreat(b);c30Log('hammer-discarded-permanently');}
function c30Lock(b){const R=b._hammer.c30,p=targetShip(b.x,b.y),from=c30Hand(b,true),dy=Math.max(90,p.y-from.y),dx=p.x-from.x;
 const length=(PLAY.y+PLAY.h+90-from.y)/dy;R.lock={x:from.x+dx*length,y:PLAY.y+PLAY.h+90};R.lockedAt=R.t;c30Log('wave-locked',{from,end:R.lock});}
function c30Line(b){const R=b._hammer.c30,from=c30Hand(b,true);return{from,to:R.lock||{x:player.x,y:PLAY.y+PLAY.h+90}};}
hammerBossTick=function(b,dt){if(!c25Own(b)||b.dead)return C30.base.tick.apply(this,arguments);const h=b._hammer;
 if(c30Own(b)){if(!h.c30)c30Start(b);const R=h.c30;c30BudgetTick(b,dt);R.t+=dt;h.t=R.t;b._noHit=false;
  if(R.phase==='retreat'){const done=c35DepthFlight(b,R,.42);if(done){c30Phase(b,'gather');b20Cue('shadowCharge');}}
  else if(R.phase==='gather'){if(!R.lock&&R.t>=.65)c30Lock(b);if(R.t>=1.7)c30Phase(b,'thrust');}
  else if(R.phase==='thrust'){if(R.t>=.36){c30Phase(b,'beam');b20Cue('fusionBeam');shake=Math.max(shake,7);}}
  else if(R.phase==='beam'){const line=c30Line(b),u=clamp(R.t/.25,0,1),to={x:lerp(line.from.x,line.to.x,u),y:lerp(line.from.y,line.to.y,u)};
   if(R.t>0&&R.t<1.18)b20HitSegment(b,line.from,to,38,'Chronos rage energy wave',R.hit);
   if(R.t>=1.35){c30Phase(b,'recover');b20Cue('laserBeamEnd');}}
  else if(R.phase==='recover'&&R.t>=.7){R.cycle++;c30Retreat(b);}
  b._drawY=b.y;return;
 }
 const old=h.ch23Spin||0,C=h._hf22Charge,r=C30.base.tick.apply(this,arguments);
 if(c29Gun(b)&&h.state==='chaingun')h.ch23Spin=old+dt*lerp(12,76,clamp((h.c29GunTime||0)/9,0,1));
 const charge=h._hf22Charge;if(charge&&charge.t>=1.04&&!charge.c30Burst){charge.c30Burst=true;spawnShockRing(b.x,b.y,145,'comet');shake=Math.max(shake,10);b20Cue('bossPhase');c30Log('power-up-release');}
 if(h._hf22Red&&!h._hf22Charge&&!h.c30)c30Start(b);
 return r;
};
bossHitTest=function(x,y){const b=boss;if(!c30Own(b))return C30.base.hit.apply(this,arguments);if(b._noHit)return false;b._hammerModuleHit=null;
 const q=ha21Blue(b),a=q.a,k=q.k;if(!XART.rdy(a.key))return false;let mask=C30.masks.get(a.key);if(!mask){const im=XART.get(a.key),c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d');g.drawImage(im,0,0);mask=g.getImageData(0,0,a.w,a.h).data;C30.masks.set(a.key,mask);}
 const px=Math.floor((x-b.x)/k+a.pivot[0]),py=Math.floor((y-b.y)/k+a.pivot[1]);return px>=0&&py>=0&&px<a.w&&py<a.h&&mask[(py*a.w+px)*4+3]>100;
};
function c30Wave(b){const R=b._hammer.c30,L=c30Line(b),u=clamp(R.t/.25,0,1),length=Math.hypot(L.to.x-L.from.x,L.to.y-L.from.y)*u;
 const f=R.t<.12?1:R.t>=1.18?Math.min(7,6+Math.floor((R.t-1.18)/.085)):2+Math.floor(R.t*18)%4,a=c30Row('wave',f);if(!XART.rdy(a.key))return;
 ctx.save();ctx.translate(L.from.x,L.from.y);ctx.rotate(Math.atan2(L.to.y-L.from.y,L.to.x-L.from.x)-Math.PI/2);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),-68,-8,136,length+8);ctx.restore();C30.lastBeam={...L,width:76,length,frame:f};}
function c30Gather(b){const R=b._hammer.c30,hand=c30Hand(b),u=R.phase==='thrust'?1:clamp(R.t/1.7,0,1),a=c30Row('wave',0);if(XART.rdy(a.key)){const im=XART.get(a.key),size=lerp(8,42,u);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,40,0,112,85,hand.x-size/2,hand.y-size/2,size,size);ctx.restore();}
 const L=c30Line(b);C25.base.warning(b,{x:L.from.x,y:L.from.y,ex:L.to.x,ey:L.to.y,width:76,progress:u,fieldOnly:true});}
function c30ChargeDraw(b){const h=b._hammer,C=h._hf22Charge,q=ha21Blue(b),u=clamp(C.t/1.8,0,1);hammerBossAtmosphereDraw(b);
 // The expanding emission derives from this exact body's alpha; keep its
 // negative space, shoulders and fists readable rather than a detached flame.
 const m=c27AuraStencil(q.a.key);if(m){ctx.save();ctx.translate(b.x,b.y);ctx.imageSmoothingEnabled=false;for(let i=0;i<4;i++){const v=(efxClock*3.7+i/4)%1,s=1+v*.10*u;ctx.save();ctx.scale(s,s);ctx.globalAlpha=.62*(1-v)*u;ctx.drawImage(m.red,-q.a.pivot[0]-m.pad,-q.a.pivot[1]-m.pad-v*42*u);ctx.restore();}ctx.restore();}
 ha21Body(b,q);
 if(u>.2){const top={x:b.x,y:b.y-60};c25Bolt({x:b.x-65,y:b.y+130},top,efxClock*2,20,.9);c25Bolt({x:b.x+65,y:b.y+130},top,efxClock*2+.4,16,.8);}
 if(u>.57&&u<.62&&XART.rdy(q.a.white)){ctx.save();ctx.globalAlpha=.85;ctx.drawImage(XART.get(q.a.white),b.x-q.a.pivot[0],b.y-q.a.pivot[1]);ctx.restore();}
 if(u<.2&&C.tool)c29Tool(b,C.tool,{x:b.x-160,y:viewTopY()-110},u/.2,lerp(1,.2,u/.2));
 C30.lastCharge={frame:q.a.frame,edgeAlpha:150,discarded:u>=.2};
}
hammerBossDraw=function(b){if(!c25Own(b)||b.dead)return C30.base.draw.apply(this,arguments);const h=b._hammer;
 if(h._hf22Charge){c30ChargeDraw(b);return;}
 if(c30Own(b)){hammerBossAtmosphereDraw(b);const q=ha21Blue(b);ha21Body(b,q);const R=h.c30;if(R?.phase==='gather'||R?.phase==='thrust')c30Gather(b);if(R?.phase==='beam')c30Wave(b);return;}
 const r=C30.base.draw.apply(this,arguments);
 if(['giant_warn','giant_dive'].includes(h.state)){const from=hammerHeadPoint(b);C25.base.warning(b,{x:from.x,y:from.y,ex:h.tx,ey:h.ty,width:124,progress:h.state==='giant_dive'?1:clamp(h.t/.6,0,1),fieldOnly:true});C30.lastLanding={x:h.tx,y:h.ty,state:h.state};}
 return r;
};
window.BOF_CHRONOS_BEAM=C30;c30Warm();
