"use strict";
/* Generated chromium reels and the Code Hammer's interruptible void spell.
   Geometry, clocks, damage, pull and telegraphs share a single simulation owner. */
const HC7={events:[],draws:{},base:{warm:r30Warm,cell:aa5Cell,rig:fmcRig,donor:gd4Tick,
 draw:r30DrawBoss,clear:j3Clear,hit:modularHit,targetable:hammerWeaponTargetable,mimic:j3Mimic}};
for(const cells of Object.values(HC7_ART))for(const a of cells){XART._src[a.key]=a.path;
 if(a.key.startsWith('hc7_cast_'))FMC_ART[a.key]={key:a.key,path:a.path,rects:{pose:[0,0,a.w,a.h]}};}
function hc7Log(event,data={}){HC7.events.push({event,...data});if(HC7.events.length>240)HC7.events.shift();}
function hc7Warm(){for(const cells of Object.values(HC7_ART))for(const a of cells)XART.rdy(a.key);XART.rdy(S4REV1006_ART.key);}
r30Warm=function(){const r=HC7.base.warm.apply(this,arguments);hc7Warm();return r;};
function hc7Clock(b){return b?._r30?.clock||j3State(b)?.aa5Clock||0;}
function hc7Frame(name,f,x,y,w,h,alpha=1,rot=0){
 const cells=HC7_ART[name],a=cells[((f%cells.length)+cells.length)%cells.length];if(!XART.rdy(a.key))return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),-w/2,-h/2,w,h);ctx.restore();HC7.draws[name]=(HC7.draws[name]||0)+1;return true;
}
// Blend effect frames on an offscreen surface, then composite the result once.
// This is deliberately restricted to energy; physical boss modules stay opaque.
const HC7_BLEND={};
function hc7Reel(name,t,x,y,w,h,alpha=1,rot=0){
 const cells=HC7_ART[name],age=((t*12)%cells.length+cells.length)%cells.length,i=Math.floor(age),mix=age-i,a=cells[i],b=cells[(i+1)%cells.length];
 if(!XART.rdy(a.key)||!XART.rdy(b.key))return hc7Frame(name,i,x,y,w,h,alpha,rot);
 let cache=HC7_BLEND[name];if(!cache){const cv=document.createElement('canvas');cv.width=cv.height=316;cache=HC7_BLEND[name]={cv,g:cv.getContext('2d'),age:null};}
 if(cache.age!==age){const g=cache.g;g.clearRect(0,0,316,316);g.imageSmoothingEnabled=false;g.globalCompositeOperation='source-over';g.globalAlpha=1-mix;g.drawImage(XART.get(a.key),0,0,316,316);
  g.globalCompositeOperation='lighter';g.globalAlpha=mix;g.drawImage(XART.get(b.key),0,0,316,316);g.globalAlpha=1;g.globalCompositeOperation='source-over';cache.age=age;}
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(cache.cv,-w/2,-h/2,w,h);ctx.restore();
 HC7.draws[name]=(HC7.draws[name]||0)+1;HC7.draws[name+'Phase']=age;return true;
}
function hc7VoidDraw(b,x,y,size,alpha=1){return hc7Reel('void',hc7Clock(b),x,y,size,size,alpha);}
function hc7HelixDraw(b,x,y,w,h,front=false){
 ctx.save();ctx.beginPath();ctx.rect(x-w*.6,front?y:y-h*.6,w*1.2,h*.6);ctx.clip();
 const r=hc7Reel('helix',hc7Clock(b),x,y,w,h,1);ctx.restore();return r;
}
aa5Cell=function(name,f,x,y,w,h=w,rot=0,alpha=1){
 if(name!=='void')return HC7.base.cell.apply(this,arguments);
 return hc7Reel('void',hc7Clock(boss),x,y,w,h,alpha,rot);
};
function hc7RiftOwn(b){return j3State(b)?.encounter===2&&j3State(b).mimic===8&&b._r30.mode==='fight'&&!b.dead&&b.hp>0;}
function hc7RiftReady(b,D){const h=D.p._hammer;return hc7RiftOwn(b)&&!h.hammerDestroyed&&!h.throw&&!h.gp4Emergency&&h.recovery?.status!=='charging'&&
 ['hammer','warn','recover','storm_idle'].includes(h.state)&&!(h.state==='warn'&&h.t>.15)&&fmcAlive(b,'hammer');}
function hc7RiftStart(b){
 if(!hc7RiftOwn(b))return false;const S=b._r30,D=gd4Create(b,8),h=D.p._hammer;
 if(S.hc7Rift||h.hammerDestroyed||h.throw||h.gp4Emergency||h.recovery?.status==='charging'||!fmcAlive(b,'hammer'))return false;
 const cx=worldWidth()/2,cy=PLAY.y+PLAY.h*.68,R=Math.min(218,viewW()*.38);
 const cast={phase:'raise',t:0,age:0,id:(S.hc7Serial||0)+1,x:cx,y:cy,radius:R,core:36,
  ox:b.x,oy:b.y,bx:cx,by:PLAY.y+167,tell:2.6,active:hammerFurious()?6.2:hammerHard()?5.9:5.6,
  lanes:[],pulse:-1,hitCd:{},edgeLeft:cx-R-24,edgeRight:cx+R+24};
 S.hc7Serial=cast.id;S.hc7Rift=cast;D.aa5Salvo=null;D.aa5Cd=6;h.state='hc7Rift';h.t=0;h.hitCd=0;
 b._noHit=false;b.enter=false;D.p._noHit=false;hc7Warm();r30Sound('bossWeaponCharge');hc7Log('riftStart',{id:cast.id,x:cx,y:cy,radius:R,diff:diffKey});return cast;
}
function hc7RiftFinish(b,reason='complete'){
 const S=b?._r30,C=S?.hc7Rift;if(!C)return;S.hc7Rift=null;
 const D=j3State(b)?.gp4Donors?.[8];if(D){D.hc7Cd=hammerFurious()?8:11;D.p.x=b.x;D.p.y=b.y;
  if(D.p._hammer.state==='hc7Rift')hammerState(D.p,D.p._hammer.mode==='storm'?'storm_idle':'recover');}
 hc7Log('riftEnd',{id:C.id,reason});
}
function hc7RiftPhase(C,phase){C.phase=phase;C.t=0;C.lanes=[];hc7Log('riftPhase',{id:C.id,phase});}
function hc7RiftPlan(b,C){
 // Alternating diagonal spokes stop inside the pull perimeter. Both horizontal
 // edge corridors remain safe, and each pair has a complete dissipation window.
 const left=(C.pulse%2===0),angles=left?[.22*Math.PI,1.22*Math.PI]:[.78*Math.PI,1.78*Math.PI];
 C.lanes=angles.map(a=>({x:C.x+Math.cos(a)*C.core,y:C.y+Math.sin(a)*C.core,
  ex:C.x+Math.cos(a)*(C.radius+7),ey:C.y+Math.sin(a)*(C.radius+7),width:12,age:0,phase:'tell',hit:new Set()}));
 hc7Log('riftLightningTell',{id:C.id,pulse:C.pulse,lanes:C.lanes.map(({x,y,ex,ey,width})=>({x,y,ex,ey,width}))});
}
function hc7RiftStep(b,dt){
 const S=b._r30,C=S.hc7Rift,D=j3State(b)?.gp4Donors?.[8];if(!C)return;if(!D){hc7RiftFinish(b,'donor lost');return;}
 const h=D.p._hammer;if(!hc7RiftOwn(b)||h.hammerDestroyed||!fmcAlive(b,'hammer')){hc7RiftFinish(b,'emitter lost');return;}
 dt=clamp(dt,0,.05);C.t+=dt;C.age+=dt;D.age+=dt;D.p.t+=dt;h.t+=dt;h.hitCd=Math.max(0,(h.hitCd||0)-dt);
 D.p.hp=b.hp;D.p.maxhp=b.maxhp;
 if(C.phase==='raise'){
  const u=clamp(C.t/1.0,0,1),e=u*u*(3-2*u);b.x=lerp(C.ox,C.bx,e);b.y=lerp(C.oy,C.by,e);
  combatWarningTick(C,'chromium-rift-'+C.id,C.t,C.tell);
  if(C.t>=C.tell){hc7RiftPhase(C,'active');r30Sound('combatAlien0927');shake=Math.max(shake,4);}
 }else if(C.phase==='active'){
  const ramp=clamp(C.t/.75,0,1),force=hammerFurious()?176:hammerHard()?165:148;
  for(const seat of seatList())withSeat(seat,()=>{
   if(player.dead)return;C.hitCd[seat]=Math.max(0,(C.hitCd[seat]||0)-dt);
   const dx=C.x-player.x,dy=C.y-player.y,d=Math.hypot(dx,dy);
   if(d<C.radius&&d>1&&!player.roll&&!player.somer&&!player._chgDash){const pull=force*(1-d/C.radius)*ramp*dt;player.x+=dx/d*pull;player.y+=dy/d*pull;
    player.x=clamp(player.x,10,worldWidth()-10);player.y=clamp(player.y,PLAY.y+12,PLAY.y+PLAY.h-6);}
   if(Math.hypot(C.x-player.x,C.y-player.y)<C.core+4&&C.hitCd[seat]<=0){playerHit('evil chromium void');C.hitCd[seat]=.8;hc7Log('riftCoreHit',{seat,id:C.id});}
  });
  const pulse=Math.floor(C.t/1.42);if(pulse!==C.pulse&&C.t<C.active-.95){C.pulse=pulse;hc7RiftPlan(b,C);}
  for(const L of C.lanes){L.age+=dt;
   if(L.age<.90){L.phase='tell';combatWarningTick(L,'chromium-fork',L.age,.90);}
   else if(L.age<1.07){L.phase='active';if(!L.fired){L.fired=true;r30Sound('combatBeam0927');}
    for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!L.hit.has(seat)&&s81003Distance(player.x,player.y,L)<L.width/2+3){playerHit('evil chromium lightning');L.hit.add(seat);}});
   }else L.phase=L.age<1.13?'fade':'off';
  }
  if(C.t>=C.active)hc7RiftPhase(C,'recover');
 }else if(C.phase==='recover'){
  if(C.t>=1.2)hc7RiftFinish(b);
 }
 D.p.x=b.x;D.p.y=b.y;b._drawY=b.y;
}
gd4Tick=function(b,dt){
 if(!hc7RiftOwn(b)){if(b?._r30?.hc7Rift)hc7RiftFinish(b,'owner changed');return HC7.base.donor.apply(this,arguments);}
 const D=gd4Create(b,8),S=b._r30;
 if(S.hc7Rift){hc7RiftStep(b,dt);return;}
 D.hc7Cd=(D.hc7Cd??3.5)-Math.max(0,dt);
 if(D.hc7Cd<=0&&hc7RiftReady(b,D)){hc7RiftStart(b);hc7RiftStep(b,dt);return;}
 return HC7.base.donor.apply(this,arguments);
};
function hc7CastFrame(C){
 if(C.phase==='raise')return C.t<.20?0:C.t<.43?1:C.t<.70?2:C.t<1.05?3:C.t<2.15?4:5;
 if(C.phase==='active')return 5;
 return C.t<.3?6:7;
}
fmcRig=function(b){const C=b?._r30?.hc7Rift;if(!C||!hc7RiftOwn(b))return HC7.base.rig.apply(this,arguments);
 const a=HC7_ART.cast[hc7CastFrame(C)],scale=.76,w=a.w*scale,h=a.h*scale;
 const v={p:b.parts.find(p=>p.id==='core'),spec:{px:a.px,py:a.py,art:'pose',sheet:a.key,role:'core'},key:a.key,
  ax:b.x,ay:b.y,w,h,rot:0,alpha:1,z:1};Object.assign(v,fmcPoint(v,.5,.5));const out=[v];
 const p=b.parts.find(p=>p.id==='hammer');if(p&&!p.destroyed){const q=fmcPoint(v,a.head[0]/a.w,a.head[1]/a.h);
  out.push({p,spec:{px:.5,py:.5,role:'hammerHead',hidden:true},key:a.key,ax:q.x,ay:q.y,x:q.x,y:q.y,w:66,h:58,rot:0,alpha:1,z:5});}
 HC7.draws.castFrame=hc7CastFrame(C);return out;
};
function hc7CastPalm(b){const C=b._r30.hc7Rift;if(!C)return null;const a=HC7_ART.cast[hc7CastFrame(C)],v=fmcRig(b)[0];return fmcPoint(v,a.hand[0]/a.w,a.hand[1]/a.h);}
hammerWeaponTargetable=function(p){if(p?._gp4Host?._r30?.hc7Rift&&hc7RiftOwn(p._gp4Host)&&!p._hammer.hammerDestroyed)return true;return HC7.base.targetable.apply(this,arguments);};
modularHit=function(dmg){const b=boss,C=b?._r30?.hc7Rift,r=HC7.base.hit.apply(this,arguments);
 if(C&&(!hc7RiftOwn(b)||!fmcAlive(b,'hammer')||j3State(b)?.gp4Donors?.[8]?.p._hammer.hammerDestroyed))hc7RiftFinish(b,'module break');return r;};
j3Clear=function(b){hc7RiftFinish(b,'encounter clear');return HC7.base.clear.apply(this,arguments);};
j3Mimic=function(b,i){hc7RiftFinish(b,'form changed');const r=HC7.base.mimic.apply(this,arguments),D=j3State(b)?.gp4Donors?.[i];if(D&&i===8)D.hc7Cd=3.5;return r;};
function hc7LightningDraw(L,t,alpha=1){
 // Authored crackling conduit, tinted once into chromium violet.
 const a=S4REV1006_ART,clip=a.clips.conduit,frame=clip.frames[Math.floor(t*15)%clip.frames.length],rect=frame.rect;
 if(!XART.rdy(a.key))return;const dx=L.ex-L.x,dy=L.ey-L.y,len=Math.hypot(dx,dy),sx=len/a.conduitEndpointSpan,sy=.15;
 ctx.save();ctx.translate(L.x,L.y);ctx.rotate(Math.atan2(dy,dx));ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(xartTint(a.key,'#c197ff',.75),...rect,frame.offset[0]*sx,frame.offset[1]*sy,rect[2]*sx,rect[3]*sy);ctx.restore();
}
function hc7RiftDraw(b){
 const C=b._r30.hc7Rift;if(!C)return;
 const visible=C.phase==='raise'?clamp((C.t-1.0)/1.6,0,1):C.phase==='recover'?clamp(1-C.t/.75,0,1):1;
 if(visible>0)hc7VoidDraw(b,C.x,C.y,C.radius*2*visible,Math.min(1,visible*1.8));
 ctx.save();ctx.globalAlpha*=.40;hc7HelixDraw(b,b.x,b.y,240,250,false);ctx.restore();j3Body(b,1);
 ctx.save();ctx.globalAlpha*=.40;hc7HelixDraw(b,b.x,b.y,240,250,true);ctx.restore();
 const palm=hc7CastPalm(b);
 if(C.phase==='raise'){
  groundTargetReticleDraw(C.x,C.y,C.radius*2,clamp(C.t/C.tell,0,1),.82);
  if(C.t>1.05&&palm)hc7LightningDraw({x:palm.x,y:palm.y,ex:C.x,ey:C.y},C.age,.5+.4*Math.sin(C.age*9)**2);
 }else if(C.phase==='active'){
  for(const L of C.lanes){if(L.phase==='tell')combatWarningDraw(L,{...L,progress:clamp(L.age/.90,0,1),laneShape:'line'});
   else if(L.phase==='active'||L.phase==='fade')hc7LightningDraw(L,C.age,clamp((1.13-L.age)/.06,0,1));}
  if(palm)hc7LightningDraw({x:palm.x,y:palm.y,ex:C.x,ey:C.y-C.core},C.age,.58);
 }
}
r30DrawBoss=function(b){if(b?._r30?.hc7Rift&&hc7RiftOwn(b)){hc7RiftDraw(b);return;}
 return HC7.base.draw.apply(this,arguments);};
