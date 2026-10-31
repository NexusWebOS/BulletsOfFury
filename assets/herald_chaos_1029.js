'use strict';
/* HH52: authored chaos; native joints, damage, death and rewards stay authoritative. */
const HH52={base:{start:hr28Start,tick:hd1003Tick,pose:hd1003Pose,blit:hd1003Blit,draw:heraldDeathDraw,
 projectile:drawCombatFinalProjectile,update:updatePlay,intercept:enemyOrdnanceCanIntercept,rules:s3kOrdnanceRules,
 element:enemyOrdnanceElement,phase:hb25Phase,corner:hb25Corner,load:stageLoadBegin,break:ordnanceBreak1002},events:[],skulls:new Set(),fx:[]};
for(const a of [...Object.values(HH52_ART),...Object.values(HH69_ART)])XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(['geyserLightning','element_lightning_hit','bossWeaponCharge','wardenScream','timedBombBlast','bossfireVileexistence']);return HH52.base.load.call(this,n,n===8?[...(keys||[]),...[...Object.values(HH52_ART),...Object.values(HH69_ART)].map(a=>a.key)]:keys);};
function hh52Log(event,data={}){HH52.events.push({event,time:efxClock,...data});if(HH52.events.length>1600)HH52.events.shift();}
function hh52Blit(name,f,x,y,hit=false){const a=HH52_ART[name+(hit?'_hit':'')]||HH52_ART[name];if(!a||!XART.rdy(a.key))return false;
 f=clamp(f|0,0,a.frames-1);ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
// Tornado appearance is authored; movement and firing stay with the native storm.
function hh69Blit(name,f,x,y){const a=HH69_ART[name];if(!a||!XART.rdy(a.key))return false;f=clamp(f|0,0,a.frames-1);
 ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x)-a.pivot[0],Math.round(y)-a.pivot[1],a.cw,a.ch);return true;}
function hh69Summon(b,A){if(!A.stormBolts){A.stormBolts=[];A.stormNext=0;A.stormBeat=0;A.stormFlash=[-100,-100];}
 A.stormBolts=A.stormBolts.filter(p=>efxClock-p.born<16/60);
 if(A.t>=A.stormNext){const u=clamp(A.t/A.warm,0,1),side=A.stormBeat++%2,p=hr28Tornadoes(A)[side],gap=.38-.29*Math.pow(u,1.6);
  A.stormNext=A.t+gap;A.stormBolts.push({born:efxClock,x:p.x+(A.stormBeat%3-1)*18,y:p.y,side});
  combatAudio0927(b,'geyserLightning',.12);hh52Log('storm-summon-bolt',{side,x:p.x,y:p.y,gap,progress:u});
 }
}
function hh69Volley(b,A,points,u){const side=(A.shot++|0)%2,p=points[side],n=6+bh25Rank()*2,first=eBullets.length;
 hr28Ring(b,p,n,u*.75,2.05);let count=0;
 for(let i=first;i<eBullets.length;i++){const q=eBullets[i];if(q._heraldOwner1003===b){q._hh52Lightning=true;q._hh69Storm=true;count++;}}
 if(count){A.stormFlash=A.stormFlash||[-100,-100];A.stormFlash[side]=efxClock;combatAudio0927(b,'combatOrb0927',.12);}
 hh52Log('tornado-volley',{count,x:p.x,y:p.y,side,flash:count>0});
}
function hh69StormDraw(b,A,u){
 if(u<0)for(const p of A.stormBolts||[]){const age=efxClock-p.born;if(age<16/60)hh69Blit('summon',Math.floor(age*60),p.x,p.y);}
 if(u>=-1/3&&u<4.8+1/3){const points=u<4.8?hr28Tornadoes(A):hr28Tornadoes({...A,t:A.warm+4.8});
  for(let i=0;i<points.length;i++){const p=points[i],phase=((Math.floor((u+1/3)*24)%16)+16)%16;
   if(u<0)hh69Blit('arrive',Math.floor((u+1/3)*24),p.x,p.y);
   else if(u>=4.8)hh69Blit('depart',Math.floor((u-4.8)*24),p.x,p.y);
   else{const age=efxClock-(A.stormFlash?.[i]??-100),level=age<.07?3:age<.13?2:age<.20?1:0;
    if(level)hh69Blit('flash',(level-1)*16+phase,p.x,p.y);else hh52Blit('tornado',phase,p.x,p.y);}
  }
 }
}

function hh52Special(b){const A=b?._hd1003?.er28;return A?._hh52&&!b.dead&&b._hd1003.mode==='er28-herald'?A:null;}
hr28Start=function(b,kind){HH52.base.start.apply(this,arguments);if(!['storm','nuke','rage'].includes(kind))return;
 const A=b._hd1003.er28;Object.assign(A,{_hh52:true,warm:kind==='rage'?2.5:kind==='nuke'?2.4:2.05,clip:'cast',frame:0,
  bolts:[],next:0,emitted:0,dir:1,lastPlayerX:player.x,castX:player.x,fx:[],phase:'charge'});
 hh52Log('chaos-start',{kind,warm:A.warm});};
function hh52Clip(b,name,f){const A=hh52Special(b);if(A){A.clip=name;A.frame=clamp(f|0,0,HH52_ART['core_'+name].frames-1);}}
function hh52Move(b,A,x,y){b.x=x;b.y=y;b._drawY=y;}
function hh52TornadoHit(p,q){return((q.x-p.x)/39)**2+((q.y-(p.y-8))/78)**2<1;}
function hh52EmitSkull(b,A){if(HH52.skulls.size>=22)return;
 const ids=hb25Claws(b),id=ids.length?ids[A.emitted%ids.length]:'head',p=hd1003Muzzle(b,id);
 const x=clamp(player.x+(A.emitted%3-1)*38,camLeftX()+50,camRightX()-50),a=Math.atan2(VH+50-p.y,(x-p.x)*.45);
 const q=eShootT(p.x,p.y,a,2.65+bh25Rank()*.20,'s8pair',{owner:b,noMuzzle:true,silent:true,w:32,h:32});if(!q)return;
 Object.assign(q,{_hh52Skull:true,_hh52Born:efxClock,_hh52StartY:p.y,_hh52Level:0,_heraldOwner1003:b,_heraldPart1003:id,
  _noArsenal:true,_boss:true,_energyOrdnance:true,_weaponProof:false,_shootable:true,_s3kOriginalProof:false,homing:false,hp:1});
 HH52.skulls.add(q);A.emitted++;combatAudio0927(b,'bossfireVileexistence',.09);hh52Log('skull-release',{index:A.emitted,x:q.x,y:q.y});
}
function hh52SkullBurst(q){if(q._hh52Burst)return;q._hh52Burst=true;const b=q._heraldOwner1003;if(!b||b!==subBoss||b.dead||run.stage!==8)return;
 const level=q._hh52Level||0,radius=22+level*5,n=6+level;
 HH52.fx.push({b,x:q.x,y:q.y,t:0,size:level});if(HH52.fx.length>18)HH52.fx.shift();
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-q.x,player.y-q.y)<radius)playerHit('Herald skull splash');});
 for(let i=0;i<n;i++){if(eBullets.filter(z=>z._heraldOwner1003===b&&!z.dead).length>=128)break;
  const a=i*TAU/n+(q._hh52Born%1),c=eShootT(q.x,q.y,a,2.8+level*.14,'s8pair',{owner:b,noMuzzle:true,silent:true,w:12+level*2,h:12+level*2});
  if(c)Object.assign(c,{_hh52Chunk:true,_hh52Born:efxClock,_hh52Size:Math.min(3,Math.floor(level/2)),_hh52Bounces:0,
   _heraldOwner1003:b,_heraldPart1003:'head',_noArsenal:true,_boss:true,_weaponProof:true,_shootable:false,homing:false});
 }
 combatAudio0927(b,'timedBombBlast',.08);hh52Log('skull-burst',{level,radius,chunks:n,x:q.x,y:q.y});
}
function hh52BoltTell(b,A,u){
 const dx=player.x-A.lastPlayerX;if(Math.abs(dx)>2)A.dir=Math.sign(dx);A.lastPlayerX=player.x;
 const stride=34+Math.min(50,A.emitted*5),l=camLeftX()+48,r=camRightX()-48;
 // Commit every point at birth. Later player/camera movement never drags a warning.
 const x=A.emitted===0?clamp(player.x,l,r):clamp(A.castX+A.dir*stride,l,r),y=clamp(player.y,viewTopY()+100,VH-40);
 A.castX=x;const P={x,y,born:efxClock,at:efxClock+2,done:false,id:A.emitted++};A.bolts.push(P);
 combatAudio0927(b,'bossWeaponCharge',.12);hh52Log('lightning-tell',{id:P.id,x,y,at:P.at,born:P.born,dir:A.dir});
 A.next=u+Math.max(.23,1.05*Math.pow(.83,A.emitted-1))/(run.ngplus?1.15:1);
}
function hh52BoltStrike(b,A,P){P.done=true;P.age=0;A.flashAge=0;
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-P.x,player.y-P.y)<36)playerHit('Herald anchored red lightning');});
 // Red source plasma travels from the actual ground impact, not parallel legacy columns.
 for(const a of[.25,Math.PI-.25,Math.PI/2]){const q=hr28Round(b,P.x,P.y,a,3.4);if(q)q._hh52Lightning=true;}
 combatAudio0927(b,'geyserLightning',.08);hh52Log('lightning-strike',{id:P.id,x:P.x,y:P.y,delay:efxClock-P.born});
}
hd1003Tick=function(b,dt){const A=hh52Special(b),H=b?._hd1003,Q=H?._hb25;
 if(!A){if(Q?._hh52Return)return hh52ReturnTick(b,Q,dt);return HH52.base.tick.apply(this,arguments);}
 H.clock+=dt;H.age+=dt;H.attackAge+=dt;A.t+=dt;b.fireCd=999;b._sba=null;b._s4MiniSafe=true;
 const approach=clamp(A.t/.8,0,1);if(A.phase==='charge')hh52Move(b,A,lerp(A.from.x,A.origin.x,approach),lerp(A.from.y,A.origin.y,approach)+Math.sin(H.clock*2)*3);
 if(A.t<A.warm){A.dark=Math.min(15,Math.floor(A.t/A.warm*15));hh52Clip(b,'cast',Math.floor(A.t/A.warm*24));if(A.kind==='storm')hh69Summon(b,A);combatWarningTick(b,'hh52-'+A.serial,A.t,A.warm);return true;}
 const u=A.t-A.warm;if(A.phase==='charge'){A.phase='active';A.energyFrom=hr28CastPoint(b);hh52Log('chaos-release',{kind:A.kind});combatAudio0927(b,'wardenScream',.12);}
 A.dark=15;A.flashAge=(A.flashAge??9)+dt;
 if(A.kind==='storm'){
  hh52Clip(b,'raised',Math.floor(u*24)%16);
  if(u<4.8){const points=hr28Tornadoes(A);for(let i=0;i<points.length;i++)hr28Contact(A,'hh52-tornado-'+i+'-'+Math.floor(u/.4),q=>hh52TornadoHit(points[i],q),'Herald chaos tornado');
   if(u>=A.next){A.next=u+.43/(run.ngplus?1.15:1);hh69Volley(b,A,points,u);}
  }else hh52Recover(b,A,dt,u-4.8);
 }else if(A.kind==='nuke'){
  hh52Clip(b,'raised',Math.floor(u*24)%16);const count=[10,12,15,18][bh25Rank()];
  if(A.emitted<count&&u>=A.next){hh52EmitSkull(b,A);A.next=u+Math.max(.105,1.05*Math.pow(.81,A.emitted-1))/(run.ngplus?1.15:1);}
  if(A.emitted>=count&&u>A.next+1.2)hh52Recover(b,A,dt,u-A.next-1.2);
 }else if(A.kind==='rage'){
  // Charge -> throw upward -> depart north -> background casting -> north turn -> foreground return.
  if(u<.42){hh52Clip(b,'cast',24+Math.floor(u/.42*8));}
  else if(u<1.52){const v=(u-.42)/1.1;hh52Clip(b,'depart',Math.floor(v*20));hh52Move(b,A,A.origin.x,lerp(A.origin.y,viewTopY()-190,v));}
  else if(u<2.35){const v=(u-1.52)/.83;hh52Clip(b,'far',Math.floor(v*16));hh52Move(b,A,A.origin.x,lerp(viewTopY()-110,viewTopY()+85,v));}
  else if(u<11.8){hh52Clip(b,'far',Math.floor(u*18)%16);hh52Move(b,A,camLeftX()+viewW()/2+Math.sin((u-2.35)*1.0)*viewW()*.27,viewTopY()+85+Math.sin(u*2)*9);
   if(u<8.8&&u>=A.next)hh52BoltTell(b,A,u);
  }else if(u<12.65){const v=(u-11.8)/.85;hh52Clip(b,'far',Math.floor(u*18)%16);hh52Move(b,A,b.x,lerp(viewTopY()+85,viewTopY()-120,v));}
  else if(u<14.25){const v=(u-12.65)/1.6;hh52Clip(b,'arrive',Math.floor(v*20));hh52Move(b,A,lerp(b.x,A.origin.x,Math.min(1,dt*5)),lerp(viewTopY()-120,A.origin.y,v));}
  else hh52Recover(b,A,dt,u-14.25);
  for(const P of A.bolts){if(!P.done&&efxClock>=P.at)hh52BoltStrike(b,A,P);else if(P.done)P.age+=dt;}
  A.bolts=A.bolts.filter(P=>!P.done||P.age<.35);
 }
 b._drawY=b.y;return true;
};
function hh52Recover(b,A,dt,u){A.phase='recover';A.dark=Math.max(0,15-Math.floor(u*18));hh52Clip(b,'lower',Math.min(23,Math.floor(u/.65*24)));if(u>1.1)hr28End(b);}
function hh52PoseBank(b){const A=hh52Special(b);if(A)return{clip:A.clip,f:A.frame};const Q=b?._hd1003?._hb25;if(Q?._hh52Return){return Q.phase==='hh52-grow'?{clip:'grow',f:Math.floor(clamp(Q.t/.6,0,1)*15)}:{clip:'turn',f:((Math.round(Q.angle/TAU*32)%32)+32)%32};}return null;}
hd1003Pose=function(b,p){const C=hh52PoseBank(b);if(!C)return HH52.base.pose.apply(this,arguments);const a=HH52_ART[p.id+'_'+C.clip],P=a.poses[C.f];return{x:b.x+P.x,y:b.y+P.y,a:P.a,s:P.s};};
hd1003Blit=function(p,P,flash=0,alpha=1){const C=hh52PoseBank(subBoss);if(C&&!p.dead)return hh52Blit(p.id+'_'+C.clip,C.f,P.x,P.y,flash>0);return HH52.base.blit.apply(this,arguments);};
heraldDeathDraw=function(b){const A=hh52Special(b);if(!A)return HH52.base.draw.apply(this,arguments);
 const u=A.t-A.warm;
 if(A.kind==='storm')hh69StormDraw(b,A,u);
 if(A.kind==='rage')for(const P of A.bolts){if(!P.done){const progress=clamp((efxClock-P.born)/2,0,1),colour=progress<.55?'green':progress<.82?'yellow':'red';
   hh52Blit('impact_'+colour,0,P.x,P.y);groundTargetReticleDraw(P.x,P.y,64,progress,.70);hh52Blit('star',0,P.x,P.y-45);
  }else if(P.age<.30)er28Blit('lightning',Math.min(15,Math.floor(P.age/.30*16)),P.x,P.y-256);
 }
 // Bypass only retired HR28 special fields. Its native modular draw owner remains.
 const out=HR28.base.draw.apply(this,arguments);
 if(A.kind==='storm'&&u<0)hh69Blit('warning',A.t/A.warm<.70?0:1,b.x,b.y+130);
 if(A.kind==='rage'&&u<.42){const p=u<0?hr28CastPoint(b):{x:A.energyFrom.x,y:lerp(A.energyFrom.y,viewTopY()-55,clamp(u/.42,0,1))};
  hh52Blit('lightning_ball',Math.floor(A.t*24)%16,p.x,p.y);
 }return out;
};
drawCombatFinalProjectile=function(q){if(q._hh52Skull)return hh52Blit('skull_'+q._hh52Level,Math.floor((efxClock-q._hh52Born)*24)%16,q.x,q.y);
 if(q._hh52Lightning)return hh52Blit('lightning_ball',Math.floor((efxClock-q._er28Born)*24)%16,q.x,q.y);
 if(q._hh52Chunk)return hh52Blit('chunk_'+q._hh52Size,Math.floor((efxClock-q._hh52Born)*24)%16,q.x,q.y);return HH52.base.projectile.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){if(q?._hh52Skull)return true;if(q?._hh52Chunk)return false;return HH52.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){if(q?._hh52Skull||q?._hh52Chunk)return null;return HH52.base.element.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._hh52Skull){q._weaponProof=false;q._shootable=true;q._energyOrdnance=true;return;}if(q?._hh52Chunk){q._weaponProof=true;q._shootable=false;return;}return HH52.base.rules.apply(this,arguments);};
ordnanceBreak1002=function(q){if(q?._hh52Skull){hh52SkullBurst(q);return;}return HH52.base.break.apply(this,arguments);};
updatePlay=function(dt){
 const skulls=[...HH52.skulls];for(const q of skulls){if(!q.dead){q._hh52Level=clamp(Math.floor((q.y-q._hh52StartY)/Math.max(80,VH-q._hh52StartY)*8),0,7);q.w=q.h=28+q._hh52Level*10;}}
 // Shattered glass flies outward once. No edge reflection or clamping.
 for(const q of eBullets)if(q._hh52Chunk&&!q.dead){const pad=72;
  if(q.x<camLeftX()-pad||q.x>camRightX()+pad||q.y<viewTopY()-pad||q.y>VH+pad||efxClock-q._hh52Born>2.6||q._heraldOwner1003!==subBoss||subBoss?.dead||run.stage!==8)q.dead=true;
 }
 const out=HH52.base.update.apply(this,arguments);
 for(const q of skulls){if(q._heraldOwner1003!==subBoss||subBoss?.dead||run.stage!==8){q.dead=true;HH52.skulls.delete(q);continue;}
  if(q.dead&&q.x>camLeftX()-20&&q.x<camRightX()+20&&q.y>viewTopY()&&q.y<VH+5)hh52SkullBurst(q);
  if(q.dead||!eBullets.includes(q))HH52.skulls.delete(q);
 }
 for(const F of HH52.fx)F.t+=dt;HH52.fx=HH52.fx.filter(F=>F.t<.5&&F.b===subBoss&&!F.b.dead&&run.stage===8);
 return out;
};
const HH52_EFFECTS=drawEffects;
drawEffects=function(){const out=HH52_EFFECTS.apply(this,arguments);for(const F of HH52.fx)hh52Blit((F.glass?'glass_':'impact_')+F.size,Math.min(15,Math.floor(F.t/.5*16)),F.x,F.y);return out;};
// Every pass wraps outside the camera and re-enters opposite its exit edge.
hb25Corner=function(b,Q){if(Q.pass===0)return HH52.base.corner.apply(this,arguments);const pass=Q.pass;Q.pass=0;const out=HH52.base.corner.call(this,b,Q);Q.pass=pass;return out;};
hb25Phase=function(b,phase){const Q=b._hd1003._hb25;if((phase==='recede'&&Q.pass>0)||phase==='return'){
  Q._hh52Return=true;Q.phase='hh52-wrap';Q.t=0;Q.from={x:b.x,y:b.y};Q.angle=Q.path.a+Math.PI/2;
  Q.returnToPass=phase==='recede';Q.pending=null;Q.entry={...Q.path.from};Q.route=[{x:b.x,y:viewTopY()-280},{x:Q.entry.x,y:viewTopY()-280},Q.entry];Q.routeIndex=0;
  hh52Log('flight-opposite-entry',{exit:{x:b.x,y:b.y},entry:Q.entry,kind:Q.kind,nextPass:Q.returnToPass});return;
 }return HH52.base.phase.apply(this,arguments);};
function hh52ReturnTick(b,Q,dt){const H=b._hd1003;H.clock+=dt;H.age+=dt;Q.t+=dt;b.fireCd=999;b._s4MiniSafe=true;
 if(Q.phase==='hh52-wrap'){const T=Q.route[Q.routeIndex],dx=T.x-b.x,dy=T.y-b.y,d=Math.hypot(dx,dy),v=1000*dt;
  if(d>v){b.x+=dx/d*v;b.y+=dy/d*v;}else{b.x=T.x;b.y=T.y;if(++Q.routeIndex>=Q.route.length){
   if(Q.returnToPass){Q._hh52Return=false;HH52.base.phase.call(this,b,'recede');return true;}
   Q.phase='hh52-turn';Q.t=0;Q.from={x:b.x,y:b.y};Q.startAngle=Q.angle;Q.to={x:camLeftX()+viewW()/2,y:viewTopY()+155};}}
 }else if(Q.phase==='hh52-turn'){const u=clamp(Q.t/1.35,0,1),k=u*u*(3-2*u);b.x=lerp(Q.from.x,Q.to.x,k);b.y=lerp(Q.from.y,Q.to.y,k)-Math.sin(u*Math.PI)*45;Q.angle=hb25Turn(Q.startAngle,0,k);
  if(u>=1){Q.phase='hh52-grow';Q.t=0;}}
 else{Q.angle=0;if(Q.t>=.6){delete H._hb25;H.mode='rest';H.age=.2;H.lanes=[];b._s4MiniSafe=false;hh52Log('flight-return-complete');}}
 b._drawY=b.y;return true;
}
globalThis.BOF_HERALD_CHAOS_1029={state:HH52,start:hr28Start};
