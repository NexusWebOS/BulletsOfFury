'use strict';
/* RD78: chest-origin Luminaire. Authored orb bloom/rising flood; exact field spans
   own damage. The upper side pockets remain visible and clear through release. */
const RD78={base:{spawn:spawnBoss,start:v18StartAttack,tick:r30Tick,draw:r30DrawBoss,world:drawWorld,bg:drawBG,rig:v18Rig,clear:v18Clear,contact:target17BossContact,rupture:v18Rupture,donorRupture:v19Rupture,keys:v18Keys,warm:v18Warm,load:stageLoadBegin},events:[],serial:0,draws:{},cues:['rd74WaveCharge','rd74WaveFire']};
for(const a of Object.values(RD78_ART.banks))for(const page of a.pages)XART._src[page.key]=page.path;
function rd78Keys(){return Object.values(RD78_ART.banks).flatMap(a=>a.pages.map(p=>p.key));}
v18Keys=function(){return [...RD78.base.keys(),...rd78Keys()];};
v18Warm=function(){const prior=RD78.base.warm();return rd78Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(boss?._r30?.v18?.attack?._rd78)rd78Stop();if(n===8)Snd.prepare([...RD78.cues,'bossWeaponCharge','expBig','shadowRelease']);return RD78.base.load.call(this,n,n===8?[...(keys||[]),...rd78Keys()]:keys);};
spawnBoss=function(){if(boss?._r30?.v18?.attack?._rd78)rd78Stop();return RD78.base.spawn.apply(this,arguments);};
function rd78Own(b){return d20Main(b)&&!b.dead&&b._r30.mode==='fight';}
function rd78Act(b){return rd78Own(b)&&b._r30.v18.attack?._rd78?b._r30.v18.attack:null;}
target17BossContact=function(b){if(rd78Act(b))return false;return RD78.base.contact.apply(this,arguments);};
function rd78Log(b,event,data={}){RD78.events.push({event,clock:b._r30.clock,...data});if(RD78.events.length>500)RD78.events.shift();}
function rd78Start(b){const N=b._r30.v18,rank=target17Rank();v18Clear(b);
 const P=N.attack={_rd78:true,type:'luminaire',serial:++RD78.serial,t:0,tell:rank>=3?3.8:rank>=2?4:4.2,active:.9,recover:1,rank,phase:'charge',guard:0,
  origin:{x:b.x,y:b.y},left:worldWidth()/2-RD78_ART.world[0]/2,top:0,home:{x:worldWidth()/2,y:VH*.34},hits:new Set(),fired:false,ended:false};
 b._r30.attack=P;N.swipe=null;N.acting=null;N.archiveDepth=1;N.archiveEnergy=0;N.seq++;
 Snd.play('bossWeaponCharge',.65);Snd.play('rd74WaveCharge',.80);combatWarningTick(b,'rd78-'+P.serial,0,P.tell,true);
 rd78Log(b,'luminaire-charge',{tell:P.tell,field:[P.left,P.top,...RD78_ART.world],safe:RD78_ART.safeHints.map(q=>({x:P.left+q[0],y:q[1]}))});return P;
}
v18StartAttack=function(b){if(!rd78Own(b))return RD78.base.start.apply(this,arguments);const N=b._r30.v18,count=N.rd78Decisions||0;N.rd78Decisions=count+1;if(count%3===2)return rd78Start(b);return RD78.base.start.apply(this,arguments);};
function rd78Inside(P,x,y){const xx=Math.floor(x-P.left),yy=Math.floor(y-P.top),row=RD78_ART.dangerSpans[yy];if(!row)return false;for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return true;return false;}
function rd78Stop(){for(const cue of RD78.cues)Snd.stopCue(cue);}
function rd78Finish(b,P){if(P.ended)return;P.ended=true;rd78Stop();const N=b._r30.v18;N.attack=null;N.acting=null;N.archiveEnergy=0;N.archiveDepth=1;b._r30.attack=null;b._r30.cd=1.0;b._noHit=false;N.home={x:b.x,y:b.y};j3State(b).attacks++;rd78Log(b,'luminaire-complete',{hp:b.hp});}
function rd78Tick(b,P,dt){P.t+=dt;const u=P.t-P.tell,N=b._r30.v18;P.guard=Math.min(15,Math.floor(clamp(P.t/.8,0,1)*15));
 const move=v19Ease(P.t/.65);b.x=lerp(P.origin.x,P.home.x,move);b.y=lerp(P.origin.y,P.home.y,move)+Math.sin(P.t*2.6)*1.5;b.enter=b._noHit=false;N.archiveDepth=1;
 if(u<0){P.phase='charge';N.archiveEnergy=clamp(P.t/P.tell,0,1);combatWarningTick(b,'rd78-'+P.serial,P.t,P.tell);}
 else if(u<P.active){P.phase='blast';N.archiveEnergy=1;if(!P.fired){P.fired=true;Snd.stopCue('rd74WaveCharge');Snd.play('rd74WaveFire',.8);Snd.play('shadowRelease',.55);Snd.play('expBig',.45);shake=Math.max(shake,4);rd78Log(b,'luminaire-release');}
  for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out||P.hits.has(seat))return;const inside=[[0,0],[-3,0],[3,0],[0,-3],[0,3]].some(([x,y])=>rd78Inside(P,player.x+x,player.y+y));if(inside){P.hits.add(seat);playerHit('Dracodia Luminaire');rd78Log(b,'luminaire-contact',{seat,x:player.x,y:player.y,dead:player.dead});}});
 }else{if(P.phase!=='recover'){P.phase='recover';rd78Log(b,'luminaire-recovery');}N.archiveEnergy=0;P.guard=Math.max(0,15-Math.floor((u-P.active)/P.recover*15));if(u>=P.active+P.recover)return rd78Finish(b,P);}
 N.home={x:b.x,y:b.y};
}
r30Tick=function(b,dt){const P=rd78Act(b);if(!P)return RD78.base.tick.apply(this,arguments);dt=clamp(dt||0,0,.05);j3Timers(b,dt);dr5TalkTick(b,dt);const N=b._r30.v18,Q=v17Clock(b);N.age+=dt;N.formClock+=dt;Q.t+=dt;Q.combat+=dt;Q.transition+=dt;rd78Tick(b,P,dt);};
function rd78Pose(b){const P=rd78Act(b);return P?RD77_ART.banks.guard[P.guard]:null;}
v18Rig=function(b){const N=b?._r30?.v18,P=N?.attack;if(!P?._rd77&&!P?._rd78)return RD78.base.rig.apply(this,arguments);
 // Beams sample the same immutable pose many times per update. Reuse geometry
 // only while its pose, world origin and actual live anatomy are identical.
 const parts=b.parts,mask=(parts[0]?.destroyed?1:0)|(parts[1]?.destroyed?2:0)|(parts[2]?.destroyed?4:0),old=N.rd78Rig;
 if(old&&old.parts===parts&&old.mask===mask&&old.clock===b._r30.clock&&old.x===b.x&&old.y===b.y&&old.attack===P&&old.frame===P.frame&&old.bank===P.bank&&old.guard===P.guard){RD78.rigCacheHits=(RD78.rigCacheHits||0)+1;return old.rig;}
 const q=P._rd78?RD77_ART.banks.guard[P.guard]:null,rig=q?parts.filter(p=>!p.destroyed).map(p=>{const a=q.parts[p.id];return{_rd77:true,p,a,key:a.key,ax:b.x,ay:b.y,x:b.x+a.target[0],y:b.y+a.target[1],w:a.w,h:a.h,k:1,rot:0,alpha:1,anchor:[-a.offset[0],-a.offset[1]],spec:{role:p.id==='core'?'core':'weapon'},z:p.id==='core'?1:0};}):RD78.base.rig.apply(this,arguments);
 N.rd78Rig={parts,mask,clock:b._r30.clock,x:b.x,y:b.y,attack:P,frame:P.frame,bank:P.bank,guard:P.guard,rig};RD78.rigCacheMisses=(RD78.rigCacheMisses||0)+1;return rig;
};
function rd78Blit(bank,f,x,y){const a=RD78_ART.banks[bank];if(!a)return;f=clamp(Math.floor(f),0,a.frames-1);const page=a.pages.find(p=>f>=p.start&&f<p.start+p.frames);if(!page||!XART.rdy(page.key))return;const local=f-page.start;ctx.drawImage(XART.get(page.key),local%a.cols*a.w,Math.floor(local/a.cols)*a.h,a.w,a.h,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.w,a.h);if(bank==='warning')RD78.lastWarningFrame=f;RD78.draws[bank]=(RD78.draws[bank]||0)+1;}
function rd78Orb(b,P){const q=RD78_ART.orbOffsets[P.guard];return{x:b.x+q[0],y:b.y+q[1]};}
r30DrawBoss=function(b){const P=rd78Act(b);if(!P)return RD78.base.draw.apply(this,arguments);const q=rd78Pose(b),orb=rd78Orb(b,P),u=P.t-P.tell;
 if(u<0)rd78Blit('warning',P.t/P.tell*(RD78_ART.banks.warning.frames+3),P.left,P.top);else if(u<P.active)rd78Blit('blast',u/P.active*23,P.left,P.top);else rd78Blit('recovery',(u-P.active)/P.recover*15,P.left,P.top);
 const pulse=u>=0&&u<P.active&&(u<.14||u>.34&&u<.46);
 for(const id of ['left','core','right']){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed)continue;rd77Blit(q.parts[id],b,pulse||Math.max(b.flash||0,p.flash||0)>.025&&Math.floor(efxClock*36)%2===0);}
 if(u<0)rd78Blit('orb_charge',P.t/P.tell*RD78_ART.banks.orb_charge.frames,orb.x,orb.y);else if(u<P.active)rd78Blit('orb_release',u/P.active*11,orb.x,orb.y);
};
drawBG=function(){const out=RD78.base.bg.apply(this,arguments),P=rd78Act(boss);if(P){const u=P.t-P.tell,level=u<0?Math.round(P.t/P.tell*9):u<P.active?9:Math.round(9*(1-clamp((u-P.active)/P.recover,0,1)));cf50DimDraw(level);}return out;};
function rd78Rupture(b,p,base,args){if(!rd78Act(b)||p.id==='core')return base.apply(null,args);const a=rd78Pose(b).parts[p.id];if(!a||p._rd77Broken)return;p._rd77Broken=p._rd30Shattered=true;for(const q of a.rupture)explode(b.x+q[0],b.y+q[1],34,'purple');Snd.play('combatModule0927',.8);rd78Log(b,'charge-claw-break',{part:p.id});}
v18Rupture=function(b,p){return rd78Rupture(b,p,RD78.base.rupture,arguments);};
v19Rupture=function(b,p){return rd78Rupture(b,p,RD78.base.donorRupture,arguments);};
v18Clear=function(b){const P=b?._r30?.v18?.attack;if(P?._rd78){rd78Stop();P.hits.clear();rd78Log(b,'luminaire-cancel');}return RD78.base.clear.apply(this,arguments);};
globalThis.BOF_DRACODIA_LUMINAIRE_1030=RD78;
