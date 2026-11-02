"use strict";
/* One authored airborne hull, five independent circular hatch/cannon modules.
   The controller is NOT a collision actor: only the visible bridge and wells
   own native HP/Retina/contact. Complete composite exhaustion awards one kill. */
const CC111={base:{spawn:spawnEnemy,kill:killEnemy,hit:hitEnemy,play:updatePlay,draw:drawEnemy,
 world:drawWorld,storm:s6StormTick,entry:enemyEntrySweep,beginAI:ai27Begin,endAI:ai27End,
 load:stageLoadBegin,begin:beginStage,plan:buildStagePlan},carriers:[],events:[],clock:0,
 serial:0,epoch:0,nextFire:0,pending:[],groups:[]};
const CC111_CLOUDS=Array.from({length:6},(_,i)=>'nl6c_low_rolling_bank_'+i);
for(const B of [...Object.values(CC111_ART.banks),CC111_ART.beam])XART._src[B.key]=B.path;
function sc12Log(C,event,data={}){CC111.events.push({id:C.id,event,t:CC111.clock,...data});if(CC111.events.length>1200)CC111.events.shift();}
function sc12Alive(e){return e&&!e.dead&&e._dyingT==null&&e.hp>0;}
function sc12Point(C,p){const k=C.h/1024,s=C.entry==='top'?-1:1;return{x:C.x+(p[0]-256)*k*s,y:C.y+(p[1]-512)*k*s};}
function sc12Quant(a){return Math.PI/2+TAU*v31Dir(a,32)/32;}
function sc12Bore(e){const f=e._sc12Frame||0,p=CC111_ART.cannon.bores[f],a=e._sc12Angle-Math.PI/2,k=CC111_ART.cannon.worldSize/192,x=(p[0]-96)*k,y=(p[1]-96)*k;
 return{x:e.x+x*Math.cos(a)-y*Math.sin(a),y:e.y+x*Math.sin(a)+y*Math.cos(a),a:e._sc12Angle};}
function sc12Part(C,index,hp){
 const e=CC111.base.spawn('s6turbine',C.x,C.y,{dropOk:false});if(!e)return null;
 // Retain the actual native actor object, removing the old template controllers.
 for(const k of Object.keys(e))if(k.startsWith('_'))delete e[k];
 Object.assign(e,{type:index<0?'cloudcarrierbridge':'cloudcarrierbay',pattern:'s6storm',
 x:C.x,y:C.y,w:index<0?28:44,h:index<0?34:44,hp,maxhp:hp,score:0,dropOk:false,
 art:'sc12_hull',shoots:false,armed:false,fireCd:999,fk:null,vx:0,vy:0,spin:0,flash:0,
 dead:false,_sc12:C,_sc12Index:index,_noSep:true,_s6storm:'cloudcarrier',
 _sc12Phase:'closed',_sc12Frame:0,_sc12Angle:Math.PI/2,_sc12Age:0,_noBodyContact:true});
 return e;
}
function sc12Blocked(){return !!(bossActive||subBossActive||bossWarned||warnT>0||story||thaw||fb2Talk||fb2Intro);}
function sc12DialogueHold(){return !!(story||thaw||fb2Talk||fb2Intro)&&!(bossActive||subBossActive||bossWarned||warnT>0);}
function sc12Spawn(side=-1,opt={}){
 if(run.stage!==6||run._gp4StageX||sc12Blocked()||CC111.carriers.filter(c=>!c.done&&c.phase!=='dying').length>=2)return null;
 const entry=opt.entry||'bottom',lane=side<0?camLeftX()+105:camRightX()-105;
 const C={id:++CC111.serial,side:side<0?-1:1,h:CC111_ART.hull.worldHeight,entry,lane,
 x:lane,y:entry==='top'?-CC111_ART.hull.worldHeight*.6:VH+CC111_ART.hull.worldHeight*.6,age:0,phase:'entry',score:8000,
 drawEpoch:-1,parts:[],done:false,hullOpen:false,group:opt.group||null};
 C.core=sc12Part(C,-1,EHP(110)*5);if(!C.core)return null;
 for(let i=0;i<5;i++){const e=sc12Part(C,i,EHP(38)*4);if(e)C.parts.push(e);}
 if(C.parts.length!==5){C.core.dead=true;for(const e of C.parts)e.dead=true;return null;}
 C.core._noHit=true;enemies=enemies.filter(e=>e!==C.core);
 C.maxhp=C.core.maxhp+C.parts.reduce((n,e)=>n+e.maxhp,0);C.hp=C.maxhp;
 if(C.group)C.group.members.push(C);
 CC111.carriers.push(C);sc12Place(C);sc12Log(C,'arrival',{side:C.side,hp:C.maxhp,entry});return C;
}
function sc12Pair(entry='bottom'){
 if(CC111.carriers.some(c=>!c.done))return null;
 const G={id:CC111.serial+1,entry,members:[],expected:2,done:false};CC111.groups.push(G);
 const left=sc12Spawn(-1,{entry,group:G});if(!left){G.done=true;return null;}
 CC111.pending.push({at:CC111.clock+1.8,side:1,opt:{entry,group:G}});return G;
}
function sc12Place(C){for(const e of [C.core,...C.parts]){const p=e._sc12Index<0&&C.hullOpen?C:sc12Point(C,e._sc12Index<0?CC111_ART.hull.core:CC111_ART.hull.bays[e._sc12Index]);e.x=p.x;e.y=p.y;}}
function sc12Unlock(C){
 const G=C.group,all=G?G.members:[C];if(G&&all.length!==G.expected||!all.every(c=>c.parts.every(e=>e.dead)))return;
 for(const c of all)if(!c.hullOpen&&!c.done){c.hullOpen=true;c.core._noHit=false;c.core.w=c.h*.14;c.core.h=c.h*.72;
  if(!enemies.includes(c.core))enemies.push(c.core);sc12Place(c);combatAudio0927(c.core,'combatModule0927',.3);sc12Log(c,'hull-exposed');}
}
function sc12Cancel(C){for(const e of C.parts){e._sc12Phase='closed';e._sc12Frame=e.dead?11:0;e._combatWarnings={};} }
function sc12Gun(e,dt){
 const C=e._sc12;if(!sc12Alive(e))return;e._sc12Age+=dt;
 let s=e._sc12Phase,t=e._sc12Age;
 if(s==='closed'&&CC111.clock>=e._sc12Ready){
  e._sc12Phase='opening';e._sc12Age=0;e._sc12Frame=0;
  e._sc12Fire=Math.max(CC111.clock+.76+[1.65,1.45,1.3][v31Rank()],CC111.nextFire);
  CC111.nextFire=e._sc12Fire+turretInterval15(.72,[.72,.64,.58][v31Rank()]);
  combatAudio0927(e,'combatServo0927',.6);sc12Log(C,'opening',{bay:e._sc12Index});
 }else if(s==='opening'){
  e._sc12Frame=Math.min(7,Math.floor(t/.76*8));
  if(t>=.76){e._sc12Phase='warning';e._sc12Age=0;e._sc12Frame=8;
   e._sc12Angle=sc12Quant(Math.atan2(player.y-e.y,player.x-e.x));
   e._sc12Warm=Math.max(.8,e._sc12Fire-CC111.clock);combatAudio0927(e,'bossWeaponCharge',.7);
   sc12Log(C,'warning',{bay:e._sc12Index,angle:e._sc12Angle,warm:e._sc12Warm});}
 }else if(s==='warning'){
  e._sc12Frame=8;combatWarningTick(e,'sc12-laser',t,e._sc12Warm);
  if(t>=e._sc12Warm){e._sc12Phase='fire';e._sc12Age=0;e._sc12Frame=9;
   combatAudio0927(e,'enemyHeavyLaser',.4);sc12Log(C,'laser',{bay:e._sc12Index,...sc12Bore(e)});}
 }else if(s==='fire'){
  e._sc12Frame=t<.10?9:10;
  if(t>=.58){e._sc12Phase='closing';e._sc12Age=0;e._sc12Frame=7;sc12Log(C,'cease',{bay:e._sc12Index});}
 }else if(s==='closing'){
  e._sc12Frame=Math.max(0,7-Math.floor(t/.65*8));
  if(t>=.65){e._sc12Phase='closed';e._sc12Age=0;e._sc12Ready=CC111.clock+turretInterval15(2.0);}
 }
}
function sc12Tick(dt){
 if(sc12DialogueHold())return;
 CC111.clock+=dt;
 for(const p of CC111.pending)if(!p.done&&CC111.clock>=p.at){const c=sc12Spawn(p.side,p.opt);if(c)p.done=true;}
 CC111.pending=CC111.pending.filter(p=>!p.done);
 for(const C of CC111.carriers){if(C.done)continue;
  if(C.phase==='dying'){if(C.corpse.dead)C.done=true;continue;}
  C.age+=dt;C.hp=Math.max(0,C.core.hp)+C.parts.reduce((n,e)=>n+Math.max(0,e.hp),0);
  if(!C.hullOpen)C.core.flash=Math.max(0,(C.core.flash||0)-dt);
  const recoil=C.parts.some(e=>e._sc12Phase==='fire')?.7:0;
  C.x=C.lane+Math.sin(CC111.clock*29+C.id)*(.6+recoil)+Math.sin(CC111.clock*13)*.35;
  if(sc12Blocked()&&C.phase!=='exit'){C.phase='exit';sc12Cancel(C);sc12Log(C,'combat-interlock');}
  if(C.phase==='entry'){
   const target=VH*.49+C.side*12,step=64*dt;C.y+=clamp(target-C.y,-step,step);if(Math.abs(C.y-target)<.5){C.y=target;C.phase='battery';C.arrived=CC111.clock;
    for(const e of C.parts)e._sc12Ready=CC111.clock+e._sc12Index*.44;
    sc12Log(C,'battery-ready');}
  }else if(C.phase==='battery'){
   C.y=VH*.49+C.side*12+Math.sin((CC111.clock-C.arrived)*.7)*3+Math.sin(CC111.clock*24)*.35;
   for(const e of C.parts)sc12Gun(e,dt);sc12Unlock(C);
  }else if(C.phase==='exit'){
   C.y-=105*dt;if(C.y<-C.h*.6){for(const e of [C.core,...C.parts])e.dead=true;C.done=true;}
  }
  sc12Place(C);
 }
 CC111.carriers=CC111.carriers.filter(C=>!C.done);
 for(const G of CC111.groups)if(G.members.length===G.expected&&G.members.every(c=>c.done))G.done=true;
}
function sc12BeamHits(){for(const C of CC111.carriers)if(C.phase==='battery')for(const e of C.parts)
 if(sc12Alive(e)&&e._sc12Phase==='fire'){
  const p=sc12Bore(e),beam={...p,width:12,len:1400,active:e._sc12Age>.08&&e._sc12Age<.53};
  for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&ep13BeamTouches(beam,player))playerHit();});
 }}
killEnemy=function(e){
 const C=e?._sc12;if(!C)return CC111.base.kill.apply(this,arguments);
 if(e._sc12Index<0&&!C.hullOpen)return;
 if(e.dead||C.phase==='dying')return;e.hp=0;e.dead=true;e.shoots=false;e.flash=0;e._sc12Phase='broken';e._sc12Frame=11;e._combatWarnings={};
 e._noBodyContact=true;unitDeathFX(e,'turret','red');combatAudio0927(e,'combatModule0927',.2);sc12Log(C,'part-break',{bay:e._sc12Index});sc12Unlock(C);
 C.hp=Math.max(0,C.core.hp)+C.parts.reduce((n,p)=>n+Math.max(0,p.hp),0);
 if(C.hp>0)return;
 sc12Cancel(C);C.phase='dying';
 const corpse=CC111.base.spawn('s6turbine',C.x,C.y,{dropOk:true});
 for(const k of Object.keys(corpse))if(k.startsWith('_'))delete corpse[k];
 Object.assign(corpse,{type:'cloudcarrierwreck',pattern:'s6storm',art:'sc12_hull',x:C.x,y:C.y,
 w:C.h*.47,h:C.h,hp:0,maxhp:C.maxhp,score:C.score,dropOk:true,shoots:false,
 _sc12DeathOwner:C,_noSep:true,_s6storm:'cloudcarrier'});
 C.corpse=corpse;CC111.base.kill(corpse);sc12Log(C,'complete-defeat');
};
hitEnemy=function(e){if(e?._sc12){if(e.dead)return;if(e._sc12Index<0&&!e._sc12.hullOpen){markHit(e,.12);return true;}}return CC111.base.hit.apply(this,arguments);};
function sc12Blit(B,f,a,x,y,w,h,tint=null,alpha=1){
 if(!XART.rdy(B.key))return false;const d=v31Dir(a,B.dirs),im=tint?xartTint(B.key,tint,1):XART.get(B.key);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 ctx.drawImage(im,d*B.cw,f*B.ch,B.cw,B.ch,x-w/2,y-h/2,w,h);ctx.restore();return true;
}
function carrierDeckShadow111(C,B,w,h){
 if(!XART.rdy(B.key))return;const canvas=C._deckShadow||(C._deckShadow=document.createElement('canvas'));
 if(canvas.width!==B.cw||canvas.height!==B.ch){canvas.width=B.cw;canvas.height=B.ch;}
 const g=canvas.getContext('2d');C._shadowDrawn=false;
 for(const seat of seatList())withSeat(seat,()=>{
  if(player.dead||player.out||Math.abs(player.x-C.x)>w*.65||Math.abs(player.y-C.y)>h*.65)return;
  const key=_shipFrameKey(_pilotKey());if(!XART.rdy(key))return;
  const im=xartTint(key,'#000000',1),ph=SHIP_DRAW_H,pw=ph*(im.naturalWidth||im.width)/(im.naturalHeight||im.height),kx=B.cw/w,ky=B.ch/h;
  g.clearRect(0,0,canvas.width,canvas.height);g.save();g.imageSmoothingEnabled=false;
  g.drawImage(im,(player.x+8-C.x-pw/2)*kx+B.cw/2,(player.y+14-C.y-ph/2)*ky+B.ch/2,pw*kx,ph*ky);
  g.globalCompositeOperation='destination-in';g.drawImage(XART.get(B.key),0,0,B.cw,B.ch,0,0,B.cw,B.ch);g.restore();
  ctx.save();ctx.globalAlpha=.50;ctx.imageSmoothingEnabled=false;ctx.drawImage(canvas,C.x-w/2,C.y-h/2,w,h);ctx.restore();C._shadowDrawn=true;
 });
}
function sc12Draw(C){
 const dying=C.phase==='dying',H=CC111_ART.hull,B=CC111_ART.banks,core=C.core;
 const body=C.entry==='top'?B.hull_south:B.hull,glow=C.entry==='top'?B.hull_south_glow:B.hull_glow;
 if(!dying){const key=CC111_CLOUDS[Math.floor(efxClock*7)%6];if(XART.rdy(key)){
  const cloud=XART.get(key);ctx.save();ctx.globalAlpha=C.phase==='entry'?.55:.25;
  ctx.drawImage(cloud,C.x+C.side*52-90,C.y+C.h*.25,180,135);ctx.restore();}}
 if(!dying)for(let i=0;i<H.engines.length;i++){const p=sc12Point(C,H.engines[i]);if(typeof ca111Exhaust==='function')ca111Exhaust(p,C.entry==='top'?-Math.PI/2:Math.PI/2,88,i,false);}
 sc12Blit(body,0,Math.PI/2,C.x,C.y,C.h/2,C.h,core.flash>0?hitFlashColor(core):null);
 if(!dying&&!(core.flash>0)){ctx.save();ctx.globalCompositeOperation='lighter';sc12Blit(glow,0,Math.PI/2,C.x,C.y,C.h/2,C.h,null,pxgStep(.5+.5*Math.sin(efxClock*(C.hullOpen?10:5))));ctx.restore();}
 for(const e of C.parts){const f=e.dead?11:e._sc12Frame,a=e._sc12Angle,size=CC111_ART.cannon.worldSize;
  sc12Blit(B.cannon,f,a,e.x,e.y,size,size,e.flash>0?hitFlashColor(e):null);
  if(!e.dead&&!(e.flash>0)&&['warning','fire'].includes(e._sc12Phase)){ctx.save();ctx.globalCompositeOperation='lighter';sc12Blit(B.cannon_glow,f,a,e.x,e.y,size,size,null,pxgStep(.5+.5*Math.sin(efxClock*22)));ctx.restore();}
 }
 // The aircraft's projected silhouette shades the deck and its mounted doors;
 // weapon light and warnings remain above that receiving surface.
 carrierDeckShadow111(C,body,C.h/2,C.h);
 for(const e of C.parts){
  if(dying||!sc12Alive(e))continue;const p=sc12Bore(e);
  if(e._sc12Phase==='warning')combatWarningDraw(e,{x:p.x,y:p.y,ex:p.x+Math.cos(p.a)*1400,ey:p.y+Math.sin(p.a)*1400,width:12,progress:e._sc12Age/e._sc12Warm,fieldOnly:true});
  if(e._sc12Phase==='fire'){
   const beam=CC111_ART.beam,size=12*beam.cell/beam.alphaWidth,step=size*.68;
   if(e._sc12Age<.17)v31Blit(I31_ART.banks.muzzle,Math.min(I31_ART.banks.muzzle.frames-1,Math.floor(e._sc12Age/.17*I31_ART.banks.muzzle.frames)),p.a,p.x,p.y,20);
   for(let z=size*.42;z<1400;z+=step)v31Blit(beam,Math.floor(e._sc12Age*30)%beam.frames,p.a,p.x+Math.cos(p.a)*z,p.y+Math.sin(p.a)*z,size);
  }
 }
 if(!dying&&C.hullOpen)bossShootGraphic(C.x,C.y-C.h*.24);
 C.rendered={hull:body.key,modules:C.parts.map(e=>({frame:e.dead?11:e._sc12Frame,angle:e._sc12Angle,bore:sc12Bore(e)}))};
}
drawWorld=function(){CC111.epoch++;return CC111.base.world.apply(this,arguments);};
drawEnemy=function(e){const C=e?._sc12||e?._sc12DeathOwner;if(!C)return CC111.base.draw.apply(this,arguments);
 if(C.drawEpoch!==CC111.epoch){C.drawEpoch=CC111.epoch;sc12Draw(C);} };
s6StormTick=function(e){if(e?._sc12||e?._sc12DeathOwner)return;return CC111.base.storm.apply(this,arguments);};
enemyEntrySweep=function(e){if(e?._sc12||e?._sc12DeathOwner)return;return CC111.base.entry.apply(this,arguments);};
ai27Begin=function(e){if(e?._sc12||e?._sc12DeathOwner){const old=ai27Context;ai27Context=e;return old;}return CC111.base.beginAI.apply(this,arguments);};
ai27End=function(e,old){if(e?._sc12||e?._sc12DeathOwner){ai27Context=old;return;}return CC111.base.endAI.apply(this,arguments);};
updatePlay=function(dt){const active=state===GS.PLAY&&run.stage===6&&!run._gp4StageX;
 if(active)sc12Tick(dt);const out=CC111.base.play.apply(this,arguments);if(active&&state===GS.PLAY&&!sc12Blocked())sc12BeamHits();return out;};
stageLoadBegin=function(n,keys){if(n===6)keys=[...(keys||[]),...Object.values(CC111_ART.banks).map(b=>b.key),CC111_ART.beam.key,I31_ART.banks.muzzle.key,...CC111_CLOUDS,'bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall','boss_shoot_prompt'];return CC111.base.load.call(this,n,keys);};
beginStage=function(){for(const C of CC111.carriers)sc12Cancel(C);CC111.carriers=[];CC111.pending=[];CC111.groups=[];CC111.clock=CC111.nextFire=0;return CC111.base.begin.apply(this,arguments);};
globalThis.BOF_CLOUD_CARRIERS={state:CC111,art:CC111_ART,spawn:sc12Spawn,spawnPair:sc12Pair};
