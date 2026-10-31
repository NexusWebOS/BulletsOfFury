'use strict';
/* RD97: one committed landing Retina, thrown orb and a rising red plasma mine. */
const RD97={base:{draw:r30DrawBoss,keys:v18Keys,warm:v18Warm,load:stageLoadBegin},events:[],draws:{},cast:.90,flight:.72,rise:1.35,crest:1.05,recover:.80,arm:[2.0,1.8,1.65]};
for(const a of Object.values(RD97_ART.banks))for(const p of a.pages)XART._src[p.key]=p.path;
function rd97Keys(){return Object.values(RD97_ART.banks).flatMap(a=>a.pages.map(p=>p.key));}
// The retired filled warning/flood and old orb banks stay archived, not queued.
rd78Keys=function(){return[];};
v18Keys=function(){return[...RD97.base.keys.apply(this,arguments),...rd97Keys()];};
v18Warm=function(){const old=RD97.base.warm.apply(this,arguments);return rd97Keys().map(k=>XART.rdy(k)).every(Boolean)&&old;};
stageLoadBegin=function(n,keys){return RD97.base.load.call(this,n,n===8?[...(keys||[]),...rd97Keys()]:keys);};
function rd97Log(b,event,data={}){const q={event,clock:b._r30.clock,...data};RD97.events.push(q);if(RD97.events.length>800)RD97.events.shift();rd78Log(b,event,data);}
function rd97Blit(bank,f,x,y){const a=RD97_ART.banks[bank];f=clamp(f|0,0,a.frames-1);const p=a.pages.find(p=>f>=p.start&&f<p.start+p.frames);if(!p||!XART.rdy(p.key))return false;const i=f-p.start;ctx.drawImage(XART.get(p.key),i%a.cols*a.w,Math.floor(i/a.cols)*a.h,a.w,a.h,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.w,a.h);RD97.draws[bank]=(RD97.draws[bank]||0)+1;return true;}
rd78Start=function(b){const N=b._r30.v18,rank=target17Rank();v18Clear(b);const arm=RD97.arm[clamp(d20Rank(),0,2)],tell=RD97.cast+RD97.flight+arm;
 const P=N.attack={_rd78:true,_rd97:true,type:'luminaire',serial:++RD78.serial,t:0,tell,active:RD97.rise+RD97.crest,recover:RD97.recover,rank,phase:'cast',guard:0,origin:{x:b.x,y:b.y},home:{x:worldWidth()/2,y:VH*.55},land:{x:worldWidth()/2,y:VH-46},arm,hits:new Set(),fired:false,ended:false,landed:false,radius:0,floor:0};
 b._r30.attack=P;N.swipe=null;N.acting=null;N.archiveDepth=1;N.archiveEnergy=0;N.seq++;Snd.play('bossWeaponCharge',.65);Snd.play('rd74WaveCharge',.8);combatWarningTick(b,'rd97-'+P.serial,0,P.tell,true);rd97Log(b,'plasma-cast-start',{tell:P.tell,land:{...P.land},safeY:RD97_ART.safeY});return P;};
function rd97Orb(b,P){if(P.phase==='cast')return rd78Orb(b,P);const u=clamp((P.t-RD97.cast)/RD97.flight,0,1),from=P.from||rd78Orb(b,{guard:15});return{x:lerp(from.x,P.land.x,u),y:lerp(from.y,P.land.y-50,u)-Math.sin(u*Math.PI)*76};}
rd78Inside=function(P,x,y){if(!P?._rd97||!['rise','crest'].includes(P.phase))return false;const dx=x-P.land.x,dy=P.land.y-y,r=P.radius,h=P.height;if(dy>=0)return dx*dx/(r*r)+dy*dy/(h*h)<1;return-dy<=P.floor&&Math.abs(dx)<r;};
rd78Tick=function(b,P,dt){P.t+=dt;const N=b._r30.v18,move=v19Ease(P.t/.65);b.x=lerp(P.origin.x,P.home.x,move);b.y=lerp(P.origin.y,P.home.y,move)+Math.sin(P.t*2.6)*1.5;b.enter=b._noHit=false;N.archiveDepth=1;
 const flightAt=RD97.cast,landAt=flightAt+RD97.flight,u=P.t-P.tell;
 if(P.t<flightAt){P.phase='cast';P.guard=Math.min(15,Math.floor(P.t/flightAt*16));}
 else if(P.t<landAt){P.phase='flight';P.guard=Math.max(0,15-Math.floor((P.t-flightAt)/.55*16));if(!P.from){P.from=rd78Orb(b,{guard:15});Snd.play('shadowRelease',.65);rd97Log(b,'plasma-orb-thrown',{from:{...P.from},land:{...P.land}});}}
 else if(u<0){P.phase='arming';P.guard=0;if(!P.landed){P.landed=true;Snd.play('combatOrb0927',.75);rd97Log(b,'plasma-mine-landed',{land:{...P.land}});}}
 else if(u<P.active){P.guard=0;P.phase=u<RD97.rise?'rise':'crest';if(!P.fired){P.fired=true;Snd.stopCue('rd74WaveCharge');Snd.play('rd74WaveFire',.85);Snd.play('expBig',.65);shake=Math.max(shake,4);rd97Log(b,'plasma-mine-detonates',{land:{...P.land}});}
  const f=Math.min(RD97_ART.banks.rise.frames-1,Math.floor(u/RD97.rise*RD97_ART.banks.rise.frames)),shape=RD97_ART.banks.rise.poses[f];P.radius=shape.radius;P.height=shape.height;P.floor=shape.floor;
  for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out||P.hits.has(seat))return;const hit=[[0,0],[-3,0],[3,0],[0,-3],[0,3]].some(([dx,dy])=>rd78Inside(P,player.x+dx,player.y+dy));if(hit){P.hits.add(seat);playerHit('Dracodia Luminaire plasma mine');rd97Log(b,'plasma-contact',{seat,x:player.x,y:player.y,phase:P.phase,radius:P.radius,dead:player.dead});}});
 }else{P.guard=0;if(P.phase!=='recover'){P.phase='recover';rd97Log(b,'plasma-recovery');}P.radius=P.floor=0;if(u>=P.active+P.recover)return rd78Finish(b,P);}
 if(P.t<P.tell){combatWarningTick(b,'rd97-'+P.serial,P.t,P.tell);N.archiveEnergy=clamp(P.t/P.tell,0,1);}else N.archiveEnergy=P.phase==='recover'?0:1;N.home={x:b.x,y:b.y};
};
function rd97Retina(P){const u=clamp(P.t/P.tell,0,1),colour=u<.50?0:u<.78?1:2,reveal=Math.min(7,Math.floor(P.t/.20*8)),frame=colour*8+(colour===2&&Math.floor(P.t*14)%2?6:reveal);return rd97Blit('retina',frame,P.land.x,P.land.y);}
r30DrawBoss=function(b){const P=rd78Act(b);if(!P?._rd97)return RD97.base.draw.apply(this,arguments);const q=rd78Pose(b),u=P.t-P.tell;ctx.save();ctx.beginPath();ctx.rect(camLeftX(),viewTopY(),viewW(),viewH());ctx.clip();
 if(P.t<P.tell)rd97Retina(P);
 if(P.phase==='rise')rd97Blit('rise',u/RD97.rise*RD97_ART.banks.rise.frames,P.land.x,P.land.y);
 else if(P.phase==='crest')rd97Blit('crest',Math.floor((u-RD97.rise)*30)%RD97_ART.banks.crest.frames,P.land.x,P.land.y);
 else if(P.phase==='recover')rd97Blit('fall',(u-P.active)/P.recover*RD97_ART.banks.fall.frames,P.land.x,P.land.y);
 for(const id of ['left','core','right']){const p=b.parts.find(p=>p.id===id);if(p&&!p.destroyed)rd77Blit(q.parts[id],b,Math.max(b.flash||0,p.flash||0)>.025);}
 if(P.phase==='cast'){const o=rd97Orb(b,P);rd97Blit('cast',P.t/RD97.cast*RD97_ART.banks.cast.frames,o.x,o.y);}
 else if(P.phase==='flight'){const o=rd97Orb(b,P);rd97Blit('flight',Math.floor((P.t-RD97.cast)*30)%RD97_ART.banks.flight.frames,o.x,o.y);}
 else if(P.phase==='arming')rd97Blit('mine',(P.t-RD97.cast-RD97.flight)/P.arm*RD97_ART.banks.mine.frames,P.land.x,P.land.y);
 ctx.restore();RD97.last={phase:P.phase,time:P.t,land:{...P.land},orb:['cast','flight'].includes(P.phase)?rd97Orb(b,P):null,radius:P.radius,guard:P.guard};};
globalThis.BOF_LUMINAIRE_PLASMA=RD97;
