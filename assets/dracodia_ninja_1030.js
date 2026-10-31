'use strict';
/* RD77: main Dracodia is a physical claw fighter. Copies/first host retain owners.
   Every pose, depth sample, shoulder turn and hit flash is an authored cell. */
const RD77={base:{start:v18StartAttack,tick:r30Tick,draw:r30DrawBoss,rig:v18Rig,at:v19AtRect,clear:v18Clear,warnings:v18Warnings,rupture:v18Rupture,donorRupture:v19Rupture,targetTick:target17Tick,targetDraw:target17Draw,contact:target17BossContact,keys:v18Keys,warm:v18Warm,load:stageLoadBegin},events:[],serial:0,draws:0};
for(const [key,a]of Object.entries(RD77_ART.pages)){XART._src[key]=a.path;XART._src[a.hitKey]=a.hitPath;}
function rd77Keys(){return Object.entries(RD77_ART.pages).flatMap(([key,a])=>[key,a.hitKey]);}
v18Keys=function(){return [...RD77.base.keys(),...rd77Keys()];};
v18Warm=function(){const prior=RD77.base.warm();return rd77Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(['slice','hammerImpact','teleportIn','bossWeaponCharge']);return RD77.base.load.call(this,n,n===8?[...(keys||[]),...rd77Keys()]:keys);};
function rd77Own(b){return d20Main(b)&&!b.dead&&b._r30.mode==='fight';}
function rd77Act(b){return rd77Own(b)&&b._r30.v18.attack?._rd77?b._r30.v18.attack:null;}
function rd77Log(b,event,data={}){RD77.events.push({event,clock:b._r30.clock,...data});if(RD77.events.length>500)RD77.events.shift();}
function rd77Arms(b){return b.parts.filter(p=>p.id!=='core'&&!p.destroyed&&p.hp>0);}
function rd77Side(b,id){return b.parts.some(p=>p.id===id&&!p.destroyed&&p.hp>0);}
// No generic claw-fired laser sidecar during the new physical main-body book.
target17Tick=function(b,dt){if(rd77Own(b)){if(b._target17)b._target17.phase='recover';return;}return RD77.base.targetTick.apply(this,arguments);};
target17Draw=function(b){if(rd77Own(b))return;return RD77.base.targetDraw.apply(this,arguments);};
target17BossContact=function(b){if(rd77Act(b))return false;return RD77.base.contact.apply(this,arguments);};
function rd77Start(b){const N=b._r30.v18,rank=target17Rank(),seq=N.rd77Seq||0,order=seq%2?['right','left']:['left','right'],victim=targetShip(b.x,b.y);
 const available=rd77Arms(b);if(available.length===1)order.fill(available[0].id);
 v18Clear(b);N.rd77Seq=seq+1;N.seq++;
 const land={x:clamp(victim.x,camLeftX()+40,camRightX()-40),y:clamp(victim.y,viewTopY()+250,VH-44)},first=seq%2?1:-1,follow=rank>=2?2:1;
 const marks=[land];for(let i=0;i<follow;i++)marks.push({x:clamp(land.x+(order[i]==='left'?-112:112),camLeftX()+42,camRightX()-42),y:clamp(land.y-24-(seq%3===2?i*30:0),viewTopY()+240,VH-48)});
 const P=N.attack={_rd77:true,type:'rd77-ninja',serial:++RD77.serial,t:0,rank,order,marks,origin:{x:b.x,y:b.y},home:{x:worldWidth()/2,y:viewTopY()+viewH()*.34},first,
  stage:'guard',local:0,bank:'guard',frame:0,depth:1,contacts:new Set(),impacts:new Set(),warned:new Set(),follow,index:-1};b._r30.attack=P;N.swipe=null;N.acting=null;N.archiveDepth=1;N.archiveEnergy=0;
 rd77Log(b,'combo-start',{order,marks:marks.map(q=>({...q})),rank});Snd.play('bossWeaponCharge',.8);return P;
}
v18StartAttack=function(b){if(!rd77Own(b))return RD77.base.start.apply(this,arguments);
 if(!rd77Arms(b).length){b._r30.v18.seq++;d20Start(b,'coreMissiles');rd77Log(b,'exposed-core-missiles');return;}
 return rd77Start(b);
};
function rd77Pose(P,bank,u){const rows=RD77_ART.banks[bank];P.bank=bank;P.frame=clamp(Math.floor(clamp(u,0,1)*(rows.length-1)),0,rows.length-1);P.depth=rows[P.frame].depth;return rows[P.frame];}
function rd77Point(mark){return{x:clamp(mark.x,camLeftX()+146,camRightX()-146),y:mark.y-147};}
function rd77Warn(b,P,index,age,duration){if(index>0&&!rd77Side(b,P.order[index-1]))return;if(!P.warned.has(index)){P.warned.add(index);rd77Log(b,'landing-committed',{index,target:{...P.marks[index]},duration});}P.warning={index,progress:clamp(age/duration,0,1)};combatWarningTick(b,'rd77-'+P.serial+'-'+index,Math.min(age,duration),duration,index===0&&age===0);}
function rd77Impact(b,P,index){if(index>0&&!rd77Side(b,P.order[index-1])||P.impacts.has(index))return;P.impacts.add(index);const m=P.marks[index];explode(m.x,m.y,48,'purple');Snd.play('hammerImpact',.55);shake=Math.max(shake,3);rd77Log(b,'landing-impact',{index,target:{...m}});
 for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out||P.contacts.has(seat))return;if(Math.hypot(player.x-m.x,player.y-m.y)<25){P.contacts.add(seat);playerHit('Dracodia claw landing');}});
}
function rd77Touch(b,P){if(P.depth<.85||b._noHit)return;const side=P.index>0?P.order[P.index-1]:null;if(side&&!rd77Side(b,side))return;for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out||P.contacts.has(seat))return;const hit=v18Rig(b).some(v=>v.p.id!=='core'&&(!side||v.p.id===side)&&[[-4,0],[4,0],[0,4],[0,-4],[0,0]].some(([x,y])=>v19AtRect(v,player.x+x,player.y+y)));if(hit){P.contacts.add(seat);playerHit('Dracodia robotic claw slash');rd77Log(b,'claw-contact',{seat,index:P.index});}});}
function rd77Finish(b,P){const N=b._r30.v18;N.attack=null;N.acting=null;N.archiveDepth=1;N.archiveEnergy=0;b._r30.attack=null;b._r30.cd=P.rank>=3?.75:1.05;b._noHit=false;N.home={x:b.x,y:b.y};j3State(b).attacks++;rd77Log(b,'combo-complete',{hp:b.hp,parts:b.parts.filter(p=>!p.destroyed).map(p=>p.id)});}
function rd77Tick(b,P,dt){P.t+=dt;P.warning=null;const t=P.t,N=b._r30.v18,land=rd77Point(P.marks[0]),back={x:clamp(P.origin.x+P.first*65,camLeftX()+110,camRightX()-110),y:viewTopY()+70};let stage;
 if(t<.55){stage='guard';const u=t/.55;rd77Pose(P,'guard',u);b.x=P.origin.x;b.y=P.origin.y;rd77Warn(b,P,0,t,1.85);}
 else if(t<1.2){stage='recede';const u=(t-.55)/.65;rd77Pose(P,'recede',u);b.x=lerp(P.origin.x,back.x,v19Ease(u));b.y=lerp(P.origin.y,back.y,v19Ease(u));rd77Warn(b,P,0,t,1.85);}
 else if(t<1.45){stage='leap';const u=(t-1.2)/.25;rd77Pose(P,'recede',1);b.x=lerp(back.x,land.x,u);b.y=lerp(back.y,viewTopY()-145,u);rd77Warn(b,P,0,t,1.85);}
 else if(t<1.85){stage='plunge';const u=(t-1.45)/.4;rd77Pose(P,'approach',u);b.x=land.x;b.y=lerp(viewTopY()-145,land.y,v19Ease(u));rd77Warn(b,P,0,t,1.85);if(u>.80)rd77Touch(b,P);}
 else if(t<2.10){stage='landing';rd77Pose(P,'approach',1);b.x=land.x;b.y=land.y;P.index=0;rd77Impact(b,P,0);rd77Touch(b,P);}
 else if(t<2.10+P.follow*1.03){const age=t-2.10,i=Math.floor(age/1.03),local=age-i*1.03,target=rd77Point(P.marks[i+1]),from=rd77Point(P.marks[i]);P.index=i+1;
  if(local<.43){stage='side-tell';rd77Pose(P,'guard',local/.43);b.x=from.x;b.y=from.y-14*v19Ease(local/.43);rd77Warn(b,P,i+1,local,.43);}
  else if(local<.87){stage='side-slash';const u=(local-.43)/.44;rd77Pose(P,P.order[i]==='left'?'slashL':'slashR',u);b.x=lerp(from.x,target.x,v19Ease(u));b.y=lerp(from.y-14,target.y,u)-Math.sin(u*Math.PI)*40;if(!P.impacts.has('cue'+i)){P.impacts.add('cue'+i);Snd.play('slice',.9);rd77Log(b,'jump-slash',{side:P.order[i],index:i+1});}rd77Touch(b,P);}
  else{stage='side-land';rd77Pose(P,P.order[i]==='left'?'slashL':'slashR',1);b.x=target.x;b.y=target.y;rd77Impact(b,P,i+1);rd77Touch(b,P);}
 }else{stage='recover';const u=clamp((t-(2.10+P.follow*1.03))/.8,0,1),from=rd77Point(P.marks[P.follow]);rd77Pose(P,'guard',1-u);b.x=lerp(from.x,P.home.x,v19Ease(u));b.y=lerp(from.y,P.home.y,v19Ease(u));if(u>=1)return rd77Finish(b,P);}
 if(stage!==P.stage){P.stage=stage;rd77Log(b,'motion',{stage,bank:P.bank,frame:P.frame,depth:P.depth});if(stage==='leap')Snd.play('teleportIn',.5);}
 b._noHit=P.depth<.85||stage==='leap';b.enter=false;N.archiveDepth=P.depth;N.home={x:b.x,y:b.y};
}
r30Tick=function(b,dt){const P=rd77Act(b);if(!P)return RD77.base.tick.apply(this,arguments);dt=clamp(dt||0,0,.05);j3Timers(b,dt);dr5TalkTick(b,dt);const N=b._r30.v18,Q=v17Clock(b);N.age+=dt;N.formClock+=dt;Q.t+=dt;Q.combat+=dt;Q.transition+=dt;rd77Tick(b,P,dt);};
function rd77Frame(b){const P=rd77Act(b);return P?RD77_ART.banks[P.bank][P.frame]:null;}
v18Rig=function(b){const q=rd77Frame(b);if(!q)return RD77.base.rig.apply(this,arguments);return b.parts.filter(p=>!p.destroyed).map(p=>{const a=q.parts[p.id],point=a.target;return{_rd77:true,p,a,key:a.key,ax:b.x,ay:b.y,x:b.x+point[0],y:b.y+point[1],w:a.w,h:a.h,k:1,rot:0,alpha:1,anchor:[-a.offset[0],-a.offset[1]],spec:{role:p.id==='core'?'core':'weapon'},z:p.id==='core'?1:0};});};
v19AtRect=function(v,x,y){if(!v._rd77)return RD77.base.at.apply(this,arguments);const a=v.a,xx=Math.floor(x-v.ax-a.offset[0]),yy=Math.floor(y-v.ay-a.offset[1]),row=a.spans[yy];if(!row)return false;for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return true;return false;};
function rd77Blit(a,b,hit){const key=hit?RD77_ART.pages[a.key].hitKey:a.key;if(!XART.rdy(key))return;ctx.drawImage(XART.get(key),...a.rect,Math.round(b.x+a.offset[0]),Math.round(b.y+a.offset[1]),a.w,a.h);RD77.draws++;}
function rd77Warning(b,P){const W=P.warning,a=HL51_ART;if(!W||!XART.rdy(a.key))return;const q=P.marks[W.index],u=W.progress,colour=u<.5?0:u<.8?1:2,arrival=Math.min(7,Math.floor(u*24)),f=colour*8+(u>.8&&Math.floor(P.t*14)%2?6:arrival);ctx.drawImage(XART.get(a.key),f%8*64,Math.floor(f/8)*32,64,32,Math.round(q.x)-32,Math.round(q.y)-16,64,32);}
r30DrawBoss=function(b){const P=rd77Act(b);if(!P)return RD77.base.draw.apply(this,arguments);const q=rd77Frame(b);for(const id of ['left','core','right']){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed)continue;rd77Blit(q.parts[id],b,Math.max(b.flash||0,p.flash||0)>.025&&Math.floor(efxClock*36)%2===0);}rd77Warning(b,P);};
v18Warnings=function(b){const P=rd77Act(b);if(P)return;return RD77.base.warnings.apply(this,arguments);};
function rd77Rupture(b,p,base,args){const P=rd77Act(b);if(!P||p.id==='core')return base.apply(null,args);const a=rd77Frame(b).parts[p.id];if(!a||p._rd77Broken)return;p._rd77Broken=true;p._rd30Shattered=true;for(const q of a.rupture)explode(b.x+q[0],b.y+q[1],34,'purple');Snd.play('combatModule0927',.8);rd77Log(b,'whole-claw-break',{part:p.id});}
v18Rupture=function(b,p){return rd77Rupture(b,p,RD77.base.rupture,arguments);};
v19Rupture=function(b,p){return rd77Rupture(b,p,RD77.base.donorRupture,arguments);};
v18Clear=function(b){const P=b?._r30?.v18?.attack;if(P?._rd77){P.warning=null;P.contacts.clear();rd77Log(b,'combo-cancel');}return RD77.base.clear.apply(this,arguments);};
globalThis.BOF_DRACODIA_NINJA_1030=RD77;
