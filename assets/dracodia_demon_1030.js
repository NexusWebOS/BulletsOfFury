'use strict';
/* RD72: first-host physical symbiote claws, inset-tube missiles and fast optic blasts. */
const RD72={base:{start:v18StartAttack,tick:v18AttackTick,pose:bi24AttackPose,body:bi24Draw,weapon:rb23DrawWeapon,warnings:v18Warnings,targetTick:target17Tick,targetDraw:target17Draw,contact:target17BossContact,at:r30At,point:rb23PartPoint,rupture:v18Rupture,clear:v18Clear,update:updatePlay,projectile:drawCombatFinalProjectile,player:drawPlayer,hit:playerHit,spin:updateDeathSpin,load:stageLoadBegin},events:[],muzzles:[],serial:0,drawingGrab:false};
for(const a of Object.values(RD72_ART))XART._src[a.key]=a.path;
function rd72Own(b){return b===boss&&rb23Host(b)&&!b.dead&&b._r30.mode==='fight';}
function rd72Act(b){return rd72Own(b)&&b._r30.v18.attack?._rd72?b._r30.v18.attack:null;}
v18Warnings=function(b){if(rd72Act(b))return;return RD72.base.warnings.apply(this,arguments);};
// The dedicated first-host book replaces the generic claw-mounted laser sidecar.
target17Tick=function(b,dt){if(rb23Host(b)){if(b._target17)b._target17.phase='recover';return;}return RD72.base.targetTick.apply(this,arguments);};
target17Draw=function(b){if(rb23Host(b))return;return RD72.base.targetDraw.apply(this,arguments);};
function rd72Log(event,data={}){RD72.events.push({event,clock:efxClock,...data});if(RD72.events.length>1400)RD72.events.shift();}
function rd72Dir(a){return((Math.round(a/TAU*64)%64)+64)%64;}
function rd72Angle(a){return rd72Dir(a)*TAU/64;}
function rd72Blit(n,f,x,y,hit=false){const a=RD72_ART[n+(hit?'_hit':'')]||RD72_ART[n];if(!a||!XART.rdy(a.key))return false;f=clamp(f|0,0,a.frames-1);ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
function rd72Alpha(n,f,x,y){const a=RD72_ART[n],xx=Math.floor(x+a.pivot[0]),yy=Math.floor(y+a.pivot[1]);if(xx<0||xx>=a.cw||yy<0||yy>=a.ch)return false;const row=a.spans[f][yy];for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return true;return false;}
function rd72Live(b,side){return b.parts.some(p=>p.id===side&&!p.destroyed&&p.hp>0);}
function rd72Port(b,side,q=r25HostSample(b)){const a=RD72_ART['turret_'+(q.name||rd71HostName(q))+'_'+side],v=a?.anchors[q.f];return v?{x:b.x+v[0],y:b.y+v[1]}:{x:b.x+(side==='left'?-58:58),y:b.y+15};}
function rd72Root(b,side){return{x:b.x+(side==='left'?-84:84),y:b.y+24};}
function rd72SafeRelease(G,reason){if(!G)return;withSeat(G.seat,()=>{if(player._rd72Grab===G){delete player._rd72Grab;if(!player.dead){player.x=clamp(G.safe.x,camLeftX()+20,camRightX()-20);player.y=clamp(G.safe.y,viewTopY()+40,VH-30);player.invuln=Math.max(player.invuln||0,60);}}});G.active=false;rd72Log('grab-released',{reason,seat:G.seat});}
function rd72Cancel(b,reason){const P=b?._r30?.v18?.attack;if(P?._rd72&&P.grab)rd72SafeRelease(P.grab,reason);}
stageLoadBegin=function(n,keys){for(const seat of seatList())withSeat(seat,()=>{if(player._rd72Grab)rd72SafeRelease(player._rd72Grab,'stage-change');delete player._rd72Thrown;});RD72.muzzles=[];if(n===8)Snd.prepare(['combatBeam0927','bossWeaponCharge','enemyBossCannon','enemyMissile','rd71ScreamA']);return RD72.base.load.call(this,n,n===8?[...(keys||[]),...Object.values(RD72_ART).map(a=>a.key)]:keys);};
function rd72Start(b,kind){const N=b._r30.v18,arms=rb23Arms(b);if(!arms.length)return RD72.base.start.call(this,b);const rank=target17Rank(),side=arms[(N.rd72Seq||0)%arms.length].id,T=targetShip(b.x,b.y),physical=kind==='swipe'||kind==='grab';
 const P=N.attack={_rd72:true,kind,type:'rd72-'+kind,serial:++RD72.serial,t:0,tell:kind==='eye360'?1.5:kind==='grab'?1.35:rank>=3?1.08:1.25,active:kind==='eye360'?1.1:kind==='eyeSweep'?.85:kind==='eyeFan'?1.2:kind==='missiles'?1.55:1.55,recover:.65,next:0,n:0,side,physical,target:{x:T.x,y:T.y},origin:{x:b.x,y:b.y},beams:[],contacts:new Set(),grip:0};
 N.bi24Rolled=false;N.rb23Seq=(N.rb23Seq||0)+1;b._r30.attack=P;rd72Aim(b,P);combatAudio0927(b,'bossWeaponCharge',.13);rd72Log('attack-start',{kind,side,serial:P.serial,tell:P.tell});return P;
}
v18StartAttack=function(b){if(!rd72Own(b)||!rb23Arms(b).length)return RD72.base.start.apply(this,arguments);const N=b._r30.v18,book=['missiles','swipe','eyeFan','grab','eyeSweep','eye360'];const kind=book[(N.rd72Seq||0)%book.length];N.rd72Seq=(N.rd72Seq||0)+1;return rd72Start(b,kind);};
function rd72Aim(b,P){const T=targetShip(b.x,b.y);P.target={x:clamp(T.x,camLeftX()+24,camRightX()-24),y:clamp(T.y,viewTopY()+50,VH-25)};const eye=rb23Eye(b);P.aim=rd72Angle(Math.atan2(P.target.y-eye.y,P.target.x-eye.x));P.start=P.kind==='eye360'?P.aim-Math.PI:P.aim-(P.kind==='eyeSweep'?1.0:.85);}
function rd72Finish(b,P){if(P.grab?.active)rd72SafeRelease(P.grab,'attack-end');b._r30.v18.attack=null;b._r30.attack=null;b._r30.cd=.75;j3State(b).attacks++;rd72Log('attack-end',{kind:P.kind,serial:P.serial});}
function rd72Rig(b,P,wrist,grip){const root=rd72Root(b,P.side),dx=wrist.x-root.x,dy=wrist.y-root.y,d=Math.hypot(dx,dy)||1,n=clamp(Math.ceil(d/18),2,26),nodes=[];
 for(let i=0;i<=n;i++){const u=i/n,sway=Math.sin(u*Math.PI)*Math.sin(P.t*5-u*5)*7;nodes.push({x:lerp(root.x,wrist.x,u)-dy/d*sway,y:lerp(root.y,wrist.y,u)+dx/d*sway});}
 const dir=rd72Dir(Math.atan2(dy,dx)),a=dir*TAU/64;P.rig={root,wrist:{...wrist},nodes,dir,frame:clamp(grip|0,0,3)*64+dir,tip:{x:wrist.x+Math.cos(a)*34,y:wrist.y+Math.sin(a)*34}};P.grip=grip;
}
function rd72Wrist(root,target){const dx=target.x-root.x,dy=target.y-root.y,d=Math.hypot(dx,dy)||1;return{x:target.x-dx/d*34,y:target.y-dy/d*34};}
function rd72Catch(b,P){if(P.grab)return;for(const seat of seatList())withSeat(seat,()=>{if(P.grab||player.dead||player.out||player.invuln>0||player.roll||player.somer||specialActive('juggernaut')||axelMegaShieldActive())return;if(Math.hypot(player.x-P.rig.tip.x,player.y-P.rig.tip.y)>26)return;
 const G=P.grab={b,seat,side:P.side,t:0,active:true,safe:{x:player.x,y:player.y},caught:{...P.rig.wrist}};player._rd72Grab=G;player.roll=player.somer=null;player.invuln=3;player._vx=player._vy=0;rd72Log('grab-caught',{seat,side:P.side,hp:b.hp,dead:player.dead});});}
function rd72Throw(b,P,G){G.active=false;P.throwAt=P.t;withSeat(G.seat,()=>{delete player._rd72Grab;player.invuln=0;const from={x:player.x,y:player.y},side=from.x<(camLeftX()+camRightX())/2?-1:1;player._rd72ThrowFatal=true;
 try{playerHit('dracodiaClawThrow');}finally{delete player._rd72ThrowFatal;}
 if(player.dead){player._rd72Thrown={from,vx:side*850,vy:-125};player._deathAnchor={...G.safe};rd72Log('grab-fatal-throw',{seat:G.seat,from,side});}
 else{player.x=G.safe.x;player.y=G.safe.y;player.invuln=Math.max(player.invuln||0,30);rd72Log('grab-god-survived',{seat:G.seat});}
 });combatAudio0927(b,'enemyBossCannon',.13);
}
function rd72Physical(b,P,dt){const u=P.t-P.tell,root=rd72Root(b,P.side),rest={x:root.x+(P.side==='left'?-1:1)*0,y:root.y+43},target=rd72Wrist(root,P.target);let w=rest,grip=0;
 if(u<0){const k=clamp(P.t/P.tell,0,1);w={x:rest.x+(P.side==='left'?-1:1)*12*k,y:rest.y-13*k};}
 else if(P.grab?.active){const G=P.grab;G.t+=dt;const hold=rd72Wrist(root,{x:b.x+(P.side==='left'?-110:110),y:b.y-26}),k=clamp(G.t/.65,0,1),e=k*k*(3-2*k);w={x:lerp(G.caught.x,hold.x,e),y:lerp(G.caught.y,hold.y,e)};grip=3;rd72Rig(b,P,w,grip);withSeat(G.seat,()=>{player.x=P.rig.tip.x;player.y=P.rig.tip.y;player.invuln=3;player._bank=0;});if(G.t>=1.25)rd72Throw(b,P,G);return;}
 else if(P.throwAt!=null){const k=clamp((P.t-P.throwAt)/.6,0,1);w={x:lerp(P.rig.wrist.x,rest.x,k),y:lerp(P.rig.wrist.y,rest.y,k)};if(k>=1){rd72Finish(b,P);return;}}
 else if(P.kind==='grab'){
  const k=clamp(u/.42,0,1);if(u<.85){w={x:lerp(rest.x,target.x,k),y:lerp(rest.y,target.y,k)};grip=clamp(Math.floor((u-.32)/.25*4),0,3);}
  else{const k=clamp((u-.85)/.65,0,1);w={x:lerp(target.x,rest.x,k),y:lerp(target.y,rest.y,k)};grip=3-Math.floor(k*3);}
 }else{
  const dx=P.target.x-root.x,dy=P.target.y-root.y,d=Math.hypot(dx,dy)||1,perp={x:-dy/d,y:dx/d},a={x:target.x-perp.x*62,y:target.y-perp.y*62},z={x:target.x+perp.x*62,y:target.y+perp.y*62};
  if(u<.38){const k=clamp(u/.38,0,1);w={x:lerp(rest.x,a.x,k),y:lerp(rest.y,a.y,k)};}
  else if(u<.82){const k=(u-.38)/.44;w={x:lerp(a.x,z.x,k),y:lerp(a.y,z.y,k)};}
  else{const k=clamp((u-.82)/.65,0,1);w={x:lerp(z.x,rest.x,k),y:lerp(z.y,rest.y,k)};}
 }
 rd72Rig(b,P,w,grip);if(P.kind==='grab'&&u>=.32&&u<.85)rd72Catch(b,P);
 if(P.kind==='swipe'&&u>=.30&&u<.9)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!P.contacts.has(seat)&&Math.hypot(player.x-P.rig.tip.x,player.y-P.rig.tip.y)<27){P.contacts.add(seat);playerHit('Dracodia physical claw swipe');rd72Log('claw-contact',{seat,side:P.side});}});
 if(u>=1.55&&P.throwAt==null&&!P.grab?.active)rd72Finish(b,P);
}
function rd72Rocket(b,P,side,angle){const p=rd72Port(b,side),a=rd72Angle(angle),q=eShootT(p.x,p.y,a,4.0+target17Rank()*.3,'emissile',{owner:b,noMuzzle:true,silent:true,w:10,h:26});if(!q)return;
 Object.assign(q,{_rd72Missile:true,_rd72Born:efxClock,_v18Owner:b,_noArsenal:true,_shootable:true,_weaponProof:false,_s3kOriginalProof:false,_energyOrdnance:true,hp:3,homing:false});RD72.muzzles.push({b,side,a,born:efxClock});rd72Log('inset-missile',{side,x:p.x,y:p.y,angle:a});}
function rd72BeamHit(b,dir){const p=rb23Eye(b),a=dir*TAU/64,c=Math.cos(a),s=Math.sin(a),len=Math.hypot(viewW(),viewH())+150;
 for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player._rd72Grab)return;const dx=player.x-p.x,dy=player.y-p.y,along=dx*c+dy*s,across=Math.abs(-dx*s+dy*c);if(along>=0&&along<=len&&across<8+Math.min(player._hx||9,player._hy||10))playerHit('Dracodia optic blast');});}
v18AttackTick=function(b,dt){const P=rd72Act(b);if(!P)return RD72.base.tick.apply(this,arguments);if(P.physical&&!rd72Live(b,P.side)){rd72Cancel(b,'arm-destroyed');rd72Finish(b,P);return;}
 P.t+=dt;b.x=P.origin.x;b.y=P.origin.y+Math.sin(b._r30.clock*2)*2;b._drawY=b.y;if(P.t<P.tell-.30)rd72Aim(b,P);const u=P.t-P.tell;P.beams=P.beams.filter(q=>efxClock-q.born<q.life);
 if(u<0)combatWarningTick(b,'rd72-'+P.serial,P.t,P.tell);
 if(P.physical){rd72Physical(b,P,dt);return;}
 if(u>=0&&u<P.active){
  if(P.kind==='missiles'&&u>=P.next&&P.n<6){P.next+=.22;const off=(P.n++%3-1)*.13;for(const p of rb23Arms(b)){const m=rd72Port(b,p.id);rd72Rocket(b,P,p.id,Math.atan2(P.target.y-m.y,P.target.x-m.x)+off);}combatAudio0927(b,'enemyBossCannon',.13);}
  else if(P.kind==='eyeFan'){const count=target17Rank()>=3?12:8,gap=P.active/count;if(u>=P.next&&P.n<count){const k=P.n++/(count-1),v=k<.5?k*2:(1-k)*2,a=rd72Angle(P.aim-.85+v*1.7);P.next+=gap;P.beams.push({dir:rd72Dir(a),born:efxClock,life:.065});combatAudio0927(b,'combatBeam0927',.13);rd72Log('optic-fan-blast',{dir:rd72Dir(a),serial:P.serial});}}
  else if(P.kind==='eyeSweep'||P.kind==='eye360'){const angle=P.start+u/P.active*(P.kind==='eye360'?TAU:2),dir=rd72Dir(angle);P.beams=[{dir,born:efxClock,life:.05}];if(u>=P.next){P.next=u+.18;combatAudio0927(b,'combatBeam0927',.13);}if(P.lastDir!==dir){P.lastDir=dir;rd72Log('optic-turn',{kind:P.kind,dir,serial:P.serial});}}
  for(const q of P.beams)rd72BeamHit(b,q.dir);
 }
 if(u>=P.active+P.recover)rd72Finish(b,P);
};
bi24AttackPose=function(b,actor){const P=rd72Act(b);if(actor==='dracodia'&&P){if(P.physical)return bi24Sample('dracodia_wind',0);const u=P.t<P.tell?P.t/P.tell:P.t<P.tell+P.active?1:1-clamp((P.t-P.tell-P.active)/P.recover,0,1);return bi24Sample('dracodia_wind',u);}return RD72.base.pose.apply(this,arguments);};
function rd72Line(n,dir,x,y,phase=0){const a=dir*TAU/64,len=Math.hypot(viewW(),viewH())+120;for(let d=48;d<len;d+=96)rd72Blit(n,phase*64+dir,x+Math.cos(a)*d,y+Math.sin(a)*d);}
function rd72Colour(P){const k=P.t/P.tell;return k<1/3?'green':k<2/3?'yellow':'red';}
function rd72DrawRig(b,P){const V=P.rig;if(!V)return;const p=b.parts.find(p=>p.id===P.side),hit=(p.flash||0)>0,phase=Math.floor(efxClock*18)%4;
 for(let i=0;i<V.nodes.length-1;i++){const a=V.nodes[i],z=V.nodes[i+1],d=rd72Dir(Math.atan2(z.y-a.y,z.x-a.x));rd72Blit('tendon',phase*64+d,(a.x+z.x)/2,(a.y+z.y)/2,hit);}
 if(P.grab?.active){RD72.drawingGrab=true;try{withSeat(P.grab.seat,()=>RD72.base.player.call(this));}finally{RD72.drawingGrab=false;}}
 rd72Blit('claw',V.frame,V.wrist.x,V.wrist.y,hit);
}
bi24Draw=function(q,b,size,rot=0){const P=rd72Act(b),name=rd71HostName(q);let rendered;if(P?.physical&&P.rig){
  for(const id of ['left','right']){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed)continue;if(id===P.side)rd72Blit('root_'+id,0,b.x,b.y,p.flash>0);else rd71Blit('host_'+name+'_'+id,q.f,b.x,b.y,p.flash>0);}
  const core=b.parts.find(p=>p.id==='core');rd71Blit('host_'+name+'_core',q.f,b.x,b.y,Math.max(core.flash||0,b.flash||0)>0);rd72DrawRig(b,P);BI24.current.set(b,{...q,size:360,k:360/512,rot:0,x:b.x,y:b.y,key:q.a.key});
  rendered=true;
 }else rendered=RD72.base.body.apply(this,arguments);
 if(rb23Host(b)&&RD72_ART['turret_'+name+'_left']&&!rot)for(const side of ['left','right']){const p=rd72Port(b,side,q),part=b.parts.find(p=>p.id===side);if(part&&!part.destroyed)rd72Blit('turret_'+name+'_'+side,q.f,p.x,p.y,Math.max(part.flash||0,b.parts[0]?.flash||0)>0);}return rendered;
};
rb23DrawWeapon=function(b){const P=rd72Act(b);if(!P)return RD72.base.weapon.apply(this,arguments);const eye=rb23Eye(b),phase=Math.floor(efxClock*30)%4;ctx.save();ctx.beginPath();ctx.rect(camLeftX(),viewTopY(),viewW(),viewH());ctx.clip();
 if(P.t<P.tell){const colour=rd72Colour(P);rd72Blit('asterisk',colour==='red'?1:0,eye.x,Math.max(viewTopY()+34,eye.y-78));
  if(P.physical){const r=rd72Root(b,P.side),dx=P.target.x-r.x,dy=P.target.y-r.y,d=Math.hypot(dx,dy)||1;for(const off of P.kind==='swipe'?[-62,0,62]:[-15,0,15])rd72Line('warning_'+colour,rd72Dir(Math.atan2(dy+dx/d*off,dx-dy/d*off)),r.x,r.y);}
  else if(P.kind==='missiles')for(const p of rb23Arms(b)){const r=rd72Port(b,p.id);rd72Line('warning_'+colour,rd72Dir(Math.atan2(P.target.y-r.y,P.target.x-r.x)),r.x,r.y);}
  else{if(P.kind==='eye360'){rd72Blit('circle_'+colour,0,eye.x,eye.y);rd72Blit('rotate_'+colour,0,eye.x,Math.max(viewTopY()+38,eye.y-112));}else for(let i=0;i<7;i++)rd72Line('warning_'+colour,rd72Dir(P.aim-(P.kind==='eyeSweep'?1:.85)+i*(P.kind==='eyeSweep'?2:1.7)/6),eye.x,eye.y);
   if(P.t>P.tell-.42&&Math.floor(P.t/.07)%2===0)rd72Line('guide',rd72Dir(P.start),eye.x,eye.y,phase);rd72Blit('optic_root',phase*64+rd72Dir(P.aim),eye.x,eye.y);}
 }
 for(const q of P.beams){rd72Line('beam',q.dir,eye.x,eye.y,phase);rd72Blit('optic_root',phase*64+q.dir,eye.x,eye.y);}
 for(const f of RD72.muzzles)if(f.b===b&&efxClock-f.born<.16&&rd72Live(b,f.side)){const p=rd72Port(b,f.side);rd72Blit('missile_muzzle',Math.min(3,Math.floor((efxClock-f.born)/.16*4))*64+rd72Dir(f.a),p.x,p.y);}
 ctx.restore();
};
rb23PartPoint=function(b,p,muzzle=false){const P=rd72Act(b);if(P?.physical&&P.rig&&p.id===P.side)return{...P.rig.tip};return RD72.base.point.apply(this,arguments);};
r30At=function(b,x,y){const P=rd72Act(b);if(P?.physical&&P.rig&&rd72Live(b,P.side)){const V=P.rig;if(rd72Alpha('claw',V.frame,x-V.wrist.x,y-V.wrist.y))return b.parts.find(p=>p.id===P.side);for(let i=0;i<V.nodes.length-1;i++){const a=V.nodes[i],z=V.nodes[i+1],dx=z.x-a.x,dy=z.y-a.y,l=dx*dx+dy*dy,k=l?clamp(((x-a.x)*dx+(y-a.y)*dy)/l,0,1):0;if(Math.hypot(x-a.x-dx*k,y-a.y-dy*k)<10)return b.parts.find(p=>p.id===P.side);}}
 const p=RD72.base.at.apply(this,arguments);if(P?.physical&&p?.id===P.side&&!rd72Alpha('root_'+P.side,0,x-b.x,y-b.y))return null;return p;
};
// Gripping fingers capture; their overlap must not also trigger generic lethal hull contact.
target17BossContact=function(b,x,y){if(rd72Act(b)?.kind==='grab')return false;return RD72.base.contact.apply(this,arguments);};
v18Rupture=function(b,p){const P=rd72Act(b);if(P?.physical&&p.id===P.side&&P.rig){rd72Cancel(b,'grabbing-arm-destroyed');for(const v of [P.rig.tip,...P.rig.nodes.filter((_,i)=>i%5===0)])explode(v.x,v.y,48,'purple',null,null,null,null,true);}return RD72.base.rupture.apply(this,arguments);};
v18Clear=function(b){rd72Cancel(b,'owner-clear');return RD72.base.clear.apply(this,arguments);};
drawPlayer=function(){if(player._rd72Grab&&!RD72.drawingGrab)return;return RD72.base.player.apply(this,arguments);};
playerHit=function(source){if(player._rd72Grab&&source!=='dracodiaClawThrow')return;return RD72.base.hit.apply(this,arguments);};
updateDeathSpin=function(dt){const T=player._rd72Thrown,s=player._spin;const out=RD72.base.spin.apply(this,arguments);if(T&&s&&player.dead&&!s.crashed){player.x=T.from.x+T.vx*s.t;player.y=T.from.y+T.vy*s.t+55*s.t*s.t;deathSpinAnchor();}else if(T)delete player._rd72Thrown;return out;};
drawCombatFinalProjectile=function(q){if(q._rd72Missile){return rd72Blit('missile',(Math.floor((efxClock-q._rd72Born)*24)%4)*64+rd72Dir(Math.atan2(q.vy,q.vx)),q.x,q.y);}return RD72.base.projectile.apply(this,arguments);};
updatePlay=function(dt){for(const seat of seatList())withSeat(seat,()=>{const G=player._rd72Grab;if(G&&(G.b!==boss||G.b.dead||run.stage!==8||!rd72Live(G.b,G.side)))rd72SafeRelease(G,'owner-lost');});if(rb23Host(boss))for(const q of eBullets)if(q._target17Owner===boss)q.dead=true;const out=RD72.base.update.apply(this,arguments);RD72.muzzles=RD72.muzzles.filter(f=>f.b===boss&&!f.b.dead&&run.stage===8&&efxClock-f.born<.16);return out;};
globalThis.BOF_DRACODIA_DEMON_1030={state:RD72,start:rd72Start};
