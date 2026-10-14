"use strict";
/* Stage 6 left-route cargo fortress. Stage X and the rebel route retain their owners. */
const SC13={keys:['s6cargo13_hull','s6cargo13_turrets','s6cargo13_red_beams','s6cargo13_muzzles','s6cargo13_front_lights'],base:{init:warhiveInit,tick:warhiveTick,
 draw:warhiveDraw,hit:warhiveHitTest,damage:warhiveDamage,targets:warhiveRetinaTargets,
 load:stageLoadBegin,wingSay:s6WingSay},stats:{sequences:0,beams:0,missiles:0,modules:0}};
XART._src.s6cargo13_hull='assets/game/levels/stage_06/boss/siege_carrier_1013/hull.png';
XART._src.s6cargo13_turrets='assets/game/levels/stage_06/boss/siege_carrier_1013/turrets.png';
XART._src.s6cargo13_red_beams='assets/game/levels/stage_06/boss/siege_carrier_1013/red_beams.png';
XART._src.s6cargo13_muzzles='assets/game/levels/stage_06/boss/siege_carrier_1013/muzzles.png';
XART._src.s6cargo13_front_lights='assets/game/levels/stage_06/boss/siege_carrier_1013/front_lights.png';
const SC13_CFG={
 easy:{warm:1.28,step:.76,fire:.42,width:32,rest:1.45,speed:16,hp:.82,rockets:2},
 normal:{warm:1.12,step:.66,fire:.50,width:34,rest:1.25,speed:19,hp:1,rockets:4},
 hard:{warm:1.02,step:.57,fire:.56,width:36,rest:1.10,speed:22,hp:1.15,rockets:4},
 furious:{warm:.94,step:.50,fire:.60,width:38,rest:1.00,speed:24,hp:1.30,rockets:6}
};
const SC13_SOCKETS=[[269,366],[347,366],[426,366],[600,366],[679,366],[759,366]];
const SC13_VENTS=[[493,221,37,9],[493,233,37,9],[493,245,37,9],[493,257,37,9],[493,269,37,9],[493,281,37,9]];
function sc13Config(){return SC13_CFG[diffKey==='insanity'?'furious':diffKey]||SC13_CFG.normal;}
function sc13Owns(b){return !!b?._cargo13;}
function sc13Warm(){for(const k of [...SC13.keys,'nxp_upward_0'])XART.rdy(k);}
stageLoadBegin=function(n,keys){return SC13.base.load.call(this,n,n===6?[...(keys||[]),...SC13.keys]:keys);};
s6WingSay=function(who,line){
 if(run.stage===6&&!run._gp4StageX&&typeof line==='string'){
  line=line.replace('HARRIER BREAKING LEFT. CONTACTS COMING THROUGH!','CARGO FORTRESS BREAKING LEFT. CONTACTS COMING THROUGH!')
   .replace('FIVE-SHIP WING, TAKE THE HARRIER TOGETHER!','FIVE-SHIP WING, DISABLE THOSE LASER BATTERIES!');
 }return SC13.base.wingSay.call(this,who,line);
};
warhiveInit=function(b){
 SC13.base.init.apply(this,arguments);
 if(run.stage!==6||run._gp4StageX||b._gp4Host)return;
 const cfg=sc13Config(),base=Math.max(1800,b._whv.aceMax||2400),core=Math.ceil(base*.74*cfg.hp),hp=Math.ceil(base*.095*cfg.hp);
 b._cargo13={age:0,t:0,mode:'arrive',cfg,core,maxCore:core,coreFl:0,x:camLeftX()+viewW()/2,y:-170,
  dir:1,speed:0,sequence:0,queue:[],lasers:[],rest:cfg.rest,rockets:null,deathFx:0,hit:null,
  guns:SC13_SOCKETS.map((p,i)=>({id:i,hp,maxhp:hp,dead:false,fl:0,heat:0,pose:0,cool:0})),ready:false};
 b.name='WARHIVE SIEGE CARRIER';b.enter=false;b._noHit=false;b.w=viewW()*1.29;b.h=b.w/2;
 b.hp=b.maxhp=core+hp*6;b._whv.mode='carrier';b._whv.ace=null;b._whv.shots=[];
 b.x=b._cargo13.x;b.y=b._cargo13.y;sc13Sync(b);sc13Warm();
};
function sc13Scale(b){return b.w/1024;}
function sc13Mount(b,id){const p=SC13_SOCKETS[id],s=sc13Scale(b),C=b._cargo13;
 return{x:C.x+(p[0]-512)*s,y:C.y+(p[1]-256)*s};}
function sc13Muzzle(b,id){const p=sc13Mount(b,id);return{x:p.x,y:p.y+25};}
function sc13Core(b){return{x:b._cargo13.x,y:b._cargo13.y+82*sc13Scale(b)};}
function sc13Sync(b){const C=b._cargo13,W=b._whv;b.x=C.x;b.y=C.y;b._drawY=C.y;W.cx=C.x;W.cy=C.y;
 W.core=C.core;W.coreMax=C.maxCore;W.st=C.mode;W.parts.L.dead=C.guns.slice(0,3).every(g=>g.dead);
 W.parts.R.dead=C.guns.slice(3).every(g=>g.dead);W.parts.door.dead=C.core<=0;}
function sc13Open(b){return b._cargo13.guns.filter(g=>g.dead).length>=2;}
function sc13FinalizeBudget(b){
 const C=b._cargo13;if(C.budgetFinalized)return;C.budgetFinalized=true;
 // spawnBoss applies co-op and encounter modifiers after warhiveInit returns.
 // Reconcile once, before any hit, retaining the exact final aggregate budget.
 const total=C.maxCore+C.guns.reduce((sum,g)=>sum+g.maxhp,0),target=Math.round(b.maxhp);
 if(target===total)return;const factor=target/total;
 for(const g of C.guns)g.hp=g.maxhp=Math.max(1,Math.round(g.maxhp*factor));
 C.core=C.maxCore=Math.max(1,target-C.guns.reduce((sum,g)=>sum+g.maxhp,0));b.hp=b.maxhp=target;sc13Sync(b);
}
function sc13Sound(name,volume=.6){whvSfx(name,volume);}
function sc13Clear(b){const C=b._cargo13;if(!C)return;C.queue.length=0;C.lasers.length=0;C.rockets=null;
 for(const g of C.guns){g.pose=g.dead?3:0;g.heat=0;g.cool=0;}
 for(const p of eBullets)if(p._sc13Owner===b)p.dead=true;
}
function sc13BeginSequence(b){
 const C=b._cargo13,c=C.cfg,alive=C.guns.filter(g=>!g.dead).map(g=>g.id),seq=C.sequence++;
 if(!alive.length){C.rest=c.rest;return;}
 const kind=seq%3,order=C.dir>0?[0,1,2,3,4,5]:[5,4,3,2,1,0];
 let groups;
 if(kind===0)groups=order.map(id=>[id]);
 else if(kind===1)groups=C.dir>0?[[0,5],[1,4],[2,3]]:[[2,3],[1,4],[0,5]];
 else groups=seq%2?[[1,3,5],[0,2,4]]:[[0,2,4],[1,3,5]];
 C.queue=[];let at=0;
 for(const group of groups){const ids=group.filter(id=>alive.includes(id));
  for(const id of ids)C.queue.push({id,at});
  // Comb and paired banks completely recover before the next bank starts.
  at+=kind===0?c.step:c.warm+c.fire+.50;
 }
 C.t=0;C.pattern=['BATTERY CASCADE','CROSS-DECK GATES','ALTERNATING COMB'][kind];C.mode='batteries';
 C.reservedGap=kind===2?(groups[0].includes(2)?1:2):null;
 SC13.stats.sequences++;
}
function sc13StartLaser(b,id){const C=b._cargo13,g=C.guns[id];if(g.dead)return;
 const L={id,t:0,warm:C.cfg.warm,fire:C.cfg.fire,width:C.cfg.width,fired:false};C.lasers.push(L);g.pose=1;g.cool=0;
 combatWarningTick(g,'cargo-laser-'+C.sequence+'-'+id,0,L.warm,true);sc13Sound('beamCharge',.45);
}
function sc13LaserTick(b,dt){const C=b._cargo13;
 for(const L of C.lasers){const g=C.guns[L.id];if(g.dead){L.dead=true;continue;}L.t+=dt;
  if(L.t<L.warm){g.pose=1;g.heat=L.t/L.warm;combatWarningTick(g,'cargo-laser-'+C.sequence+'-'+L.id,L.t,L.warm);}
  else if(L.t<L.warm+L.fire){g.pose=2;g.heat=1;
   if(!L.fired){L.fired=true;SC13.stats.beams++;sc13Sound('laserShot',.64);shake=Math.max(shake,1.5);}
   const p=sc13Muzzle(b,L.id),width=sc13BeamWidth(L);
   // Collision uses the visible core, no damage from warning or fading fringe.
   if(width>=L.width*.55)for(const seat of seatList())withSeat(seat,()=>{
    if(!player.dead&&player.y>p.y+6&&Math.abs(player.x-p.x)<width*.5+Math.max(3,(player._hx||9)-3))playerHit({kind:'carrierLaser',owner:b});
   });
  }else{g.pose=0;g.heat=0;g.cool=.40;L.dead=true;}
 }C.lasers=C.lasers.filter(L=>!L.dead);
}
function sc13RocketStart(b){const C=b._cargo13;C.rockets={t:0,warm:1.0,released:false,paths:[]};
 const n=C.cfg.rockets/2;
 for(const side of [-1,1])for(let i=0;i<n;i++)C.rockets.paths.push({side,angle:Math.PI/2-side*(.22+i*.14)});
 sc13Sound('bossWeaponCharge',.40);
}
function sc13RocketMount(b,side){return{x:b._cargo13.x+side*112,y:b._cargo13.y+77};}
function sc13RocketTick(b,dt){const C=b._cargo13,R=C.rockets;if(!R)return;R.t+=dt;
 if(R.t<R.warm)combatWarningTick(R,'cargo-missiles',R.t,R.warm);
 else if(!R.released){R.released=true;
  for(const p of R.paths){const m=sc13RocketMount(b,p.side),speed=2.45;
   eBullets.push({x:m.x,y:m.y,vx:Math.cos(p.angle)*speed,vy:Math.sin(p.angle)*speed,ang:p.angle,
    w:10,h:18,kind:'emissile',hp:1,_shootable:true,spd:speed,t:0,_bright:true,_sc13Owner:b,owner:b});
   SC13.stats.missiles++;
  }sc13Sound('missile',.65);
 }if(R.t>R.warm+2.65){C.rockets=null;C.rest=C.cfg.rest;C.mode='recover';}
}
function sc13DeathTick(b,dt){const C=b._cargo13;b.dying+=dt;C.y+=dt*(17+b.dying*13);sc13Sync(b);C.deathFx-=dt;
 if(C.deathFx<=0&&b.dying<2.2){C.deathFx=.16;const id=Math.floor(b.dying/.16)%6,p=sc13Mount(b,id);
  explode(p.x,p.y,54,'red',null,'nxp_barrage');}
 if(b.dying>=2.2&&!C.crashed){C.crashed=true;for(const id of [0,2,3,5]){const p=sc13Mount(b,id);explode(p.x,p.y,100,'red',null,'nxp_dense');}
  spawnShockRing(C.x,C.y,180,'fire');sc13Sound('expBig',.8);shake=Math.max(shake,10);}
}
warhiveTick=function(b,dt){if(!sc13Owns(b))return SC13.base.tick.apply(this,arguments);
 const C=b._cargo13;sc13FinalizeBudget(b);dt=Math.min(.05,Math.max(0,dt));b.t+=dt;b.flash=Math.max(0,b.flash-dt);
 if(b.dead){sc13Clear(b);sc13DeathTick(b,dt);return;}
 if(!C.ready){sc13Warm();C.ready=SC13.keys.every(k=>XART.rdy(k));if(!C.ready)return;}
 C.age+=dt;C.coreFl=Math.max(0,C.coreFl-dt);for(const g of C.guns){g.fl=Math.max(0,g.fl-dt);g.cool=Math.max(0,(g.cool||0)-dt);}
 const left=camLeftX(),right=camRightX(),centre=(left+right)/2;
 if(C.mode==='arrive'){const u=clamp(C.age/2.6,0,1),ease=1-(1-u)**3;C.y=lerp(-170,72,ease);C.x=centre;
  if(u>=1){C.mode='recover';C.rest=1.2;sc13Sound('bossRoar',.6);s6WingSay('COLE','TAKE OUT TWO BATTERIES! THAT WILL EXPOSE THE REACTOR.');}
 }else{
  const limit=viewW()*.085,target=centre+C.dir*limit;C.speed+=((C.dir*C.cfg.speed)-C.speed)*Math.min(1,dt*1.5);
  C.x+=C.speed*dt;if(C.dir>0&&C.x>=target||C.dir<0&&C.x<=target){C.dir=-C.dir;}
  C.x=clamp(C.x,centre-limit-8,centre+limit+8);C.y=72+Math.sin(C.age*.42)*9;
  if(C.mode==='recover'){C.rest-=dt;if(C.rest<=0){if(C.guns.some(g=>!g.dead))sc13BeginSequence(b);else{C.mode='rockets';sc13RocketStart(b);}}}
  if(C.mode==='batteries'){C.t+=dt;while(C.queue.length&&C.queue[0].at<=C.t){const q=C.queue.shift();sc13StartLaser(b,q.id);}
   sc13LaserTick(b,dt);if(!C.queue.length&&!C.lasers.length){C.mode='rockets';sc13RocketStart(b);}}
  if(C.mode==='rockets')sc13RocketTick(b,dt);
 }
 sc13Sync(b);
};
function sc13At(b,x,y){const C=b._cargo13;if(b.dead||C.mode==='arrive'||!C.ready)return null;
 for(const g of C.guns){if(g.dead)continue;const p=sc13Mount(b,g.id);if(Math.abs(x-p.x)<18&&y>p.y-19&&y<p.y+37)return g.id;}
 const p=sc13Core(b);if(Math.abs(x-p.x)<35&&Math.abs(y-p.y)<52)return 'core';return null;
}
warhiveHitTest=function(b,x,y){if(!sc13Owns(b))return SC13.base.hit.apply(this,arguments);
 b._cargo13.hit=sc13At(b,x,y);return b._cargo13.hit!==null;
};
function sc13ContinuousAt(b,shot){
 const C=b._cargo13,flame=shot.kind==='flame',hits=[];
 const touches=(p,w,h)=>flame?flameHit(shot,p.x,p.y,w,h):
  Math.abs(shot.x-p.x)<w/2+(shot.w||1)/2&&p.y+h/2>shot.top&&p.y-h/2<shot.bot;
 for(const g of C.guns)if(!g.dead){const p=sc13Mount(b,g.id);p.y+=9;if(touches(p,36,56))hits.push({id:g.id,x:p.x,y:p.y});}
 // A continuous beam meets a front battery before the central reactor plate.
 if(hits.length){hits.sort((a,c)=>Math.abs(a.x-shot.x)-Math.abs(c.x-shot.x));return hits[0].id;}
 const p=sc13Core(b);return touches(p,70,104)?'core':null;
}
function sc13AreaTarget(b,x){
 // The engine has already resolved splash/chain/screen-wide contact. Spend
 // that one damage budget on the exposed reactor, otherwise the nearest
 // surviving battery. Never infer an area hit from a previous bullet impact.
 if(sc13Open(b))return 'core';const C=b._cargo13,live=C.guns.filter(g=>!g.dead);
 live.sort((a,c)=>Math.abs(sc13Mount(b,a.id).x-x)-Math.abs(sc13Mount(b,c.id).x-x));return live.length?live[0].id:null;
}
warhiveDamage=function(b,dmg){if(!sc13Owns(b))return SC13.base.damage.apply(this,arguments);
 const C=b._cargo13;sc13FinalizeBudget(b);if(b.dead||C.mode==='arrive')return 0;
 const shot=typeof _dmgBullet!=='undefined'?_dmgBullet:null,continuous=shot&&(shot.kind==='beam'||shot.kind==='flame');
 const direct=C.directId;C.directId=null;C.hit=null;
 let id=direct!=null?direct:continuous?sc13ContinuousAt(b,shot):null;
 if(direct==null&&!continuous){
  if(shot&&Number.isFinite(shot.x)&&Number.isFinite(shot.y))id=sc13At(b,shot.x,shot.y);
  if(id==null)id=sc13AreaTarget(b,shot&&Number.isFinite(shot.x)?shot.x:player.x);
 }
 if(id==null)return 0;dmg=Math.max(0,Number(dmg)||0);
 if(id==='core'){
  if(!sc13Open(b)){if((C.shieldSound||0)<C.age){C.shieldSound=C.age+.12;sc13Sound('shieldHitCombat',.42);}return 0;}
  C.core=Math.max(0,C.core-dmg);C.coreFl=.12;
 }else{const g=C.guns[id];if(!g||g.dead)return 0;g.hp=Math.max(0,g.hp-dmg);g.fl=.12;
  if(g.hp===0){g.dead=true;g.pose=3;C.queue=C.queue.filter(q=>q.id!==id);C.lasers=C.lasers.filter(q=>q.id!==id);
   const p=sc13Mount(b,id);explode(p.x,p.y,58,'red',null,'nxp_barrage');fxBurst(p.x,p.y,40,{color:'#83dfff',rings:1,chunks:5,sparks:8});
   sc13Sound('expBig',.50);SC13.stats.modules++;if(C.guns.filter(g=>g.dead).length===2){showCallout('shoot',1.5);s6WingSay('COLE','REACTOR EXPOSED. KEEP THAT FIRING LANE OPEN!');}}
 }
 weaponHitSfx('normal');if(typeof stageStats!=='undefined')stageStats.dmgDealt+=dmg;
 b.hp=C.core+C.guns.reduce((sum,g)=>sum+g.hp,0);sc13Sync(b);
 if(C.core<=0){b.hp=0;sc13Clear(b);bossDie();}return 0;
};
warhiveRetinaTargets=function(b,a){if(!sc13Owns(b))return SC13.base.targets.apply(this,arguments);
 const C=b._cargo13;sc13FinalizeBudget(b);if(C.mode==='arrive'||b.dead)return;
 for(const g of C.guns)if(!g.dead)a.push(retinaDynamicPiece(b,'cargo gun '+g.id,'laser battery',()=>({...sc13Mount(b,g.id),hp:g.hp,dead:g.dead||b.dead}),d=>{C.directId=g.id;hitBoss(d);},38,56));
 if(sc13Open(b))a.push(retinaDynamicPiece(b,'cargo reactor','exposed reactor',()=>({...sc13Core(b),hp:C.core,dead:b.dead}),d=>{C.directId='core';hitBoss(d);},68,96));
};
function sc13BeamWidth(L){if(L.t<L.warm||L.t>=L.warm+L.fire)return 0;const u=L.t-L.warm;return L.width*clamp(Math.min(u/.08,(L.fire-u)/.10),0,1);}
function sc13Light(b,g){
 if(g.dead||b.dead)return{phase:'off',level:0,color:'#1b2833'};
 if(g.pose===2)return{phase:'fire',level:.86+.14*Math.sin(b.t*40+g.id),color:'#ff354d'};
 if(g.pose===1)return{phase:'charge',level:.25+.65*g.heat+.10*Math.sin(b.t*(16+g.heat*20)),color:g.heat>.70?'#ff3040':'#ff9824'};
 if(g.cool>0)return{phase:'cool',level:g.cool/.4*.65,color:'#68ddff'};
 return{phase:'idle',level:.08,color:'#4baccb'};
}
function sc13LightsDraw(b){const C=b._cargo13,s=sc13Scale(b);
 for(const g of C.guns){const light=sc13Light(b,g),r=SC13_VENTS[g.id];
  // Clip and illuminate the original authored front vent lens, never a glow disc.
  const im=xartTint('s6cargo13_front_lights',light.color,light.phase==='off'?.90:.82);if(!im)continue;
  ctx.save();ctx.globalAlpha=light.phase==='off'?.9:light.level;
  ctx.drawImage(im,g.id*40+1,1,r[2],r[3],C.x+(r[0]-512)*s,C.y+(r[1]-256)*s,r[2]*s,r[3]*s);ctx.restore();
 }
}
function sc13MuzzleDraw(b,g){if(g.dead)return;const m=sc13Muzzle(b,g.id),L=b._cargo13.lasers.find(q=>q.id===g.id);
 let frame=0,size=0,alpha=1;
 if(L&&L.t<L.warm){size=18+g.heat*20;frame=0;alpha=.40+.55*g.heat;}
 else if(L&&L.t<L.warm+L.fire){const u=L.t-L.warm;frame=u<.055?0:1+Math.floor((u-.055)*18)%3;size=58+L.width*.30;}
 else if(g.cool>0){frame=3;size=44;alpha=g.cool/.4*.65;}
 if(size<=0)return;
 const im=xartPalette('s6cargo13_muzzles','#f12640')||XART.get('s6cargo13_muzzles');
 ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(im,frame*128,0,128,128,m.x-size/2,m.y-size/2,size,size);ctx.restore();
}
function sc13GunDraw(b,g){const p=sc13Mount(b,g.id),light=sc13Light(b,g),im=g.pose===1||g.pose===2?(xartPalette('s6cargo13_turrets',light.color)||XART.get('s6cargo13_turrets')):XART.get('s6cargo13_turrets'),size=42,k=size/128;
 const pose=g.dead?3:g.pose;ctx.drawImage(im,pose*128,0,128,160,p.x-64*k,p.y-60*k,128*k,160*k);
 if(g.fl>0&&Math.floor(b.t*30)%2===0){const white=xartTint('s6cargo13_turrets','#ddf6ff',.82);if(white)ctx.drawImage(white,pose*128,0,128,160,p.x-64*k,p.y-60*k,128*k,160*k);}
 if(g.dead)whvPartFx(b,p,0,true,.45,g.id*.7);
 else sc13MuzzleDraw(b,g);
 // Solid health sliver under the gun; wrecks keep their opaque authored state.
 if(!g.dead&&g.hp<g.maxhp){ctx.fillStyle='#061320';ctx.fillRect(p.x-16,p.y-26,32,4);ctx.fillStyle='#7ee7ff';ctx.fillRect(p.x-15,p.y-25,30*g.hp/g.maxhp,2);}
}
function sc13BeamDraw(b,L){const p=sc13Muzzle(b,L.id),g=b._cargo13.guns[L.id];if(g.dead)return;
 if(L.t<L.warm){combatWarningDraw(g,{x:p.x,y:p.y,ex:p.x,ey:VH+15,progress:L.t/L.warm,width:L.width+8,fieldOnly:true,laneShape:'line'});return;}
 const width=sc13BeamWidth(L);if(width<.5)return;
 const im=XART.get('s6cargo13_red_beams'),frame=Math.floor((L.t-L.warm)*16)%4,k=width/80,h=512*k,length=VH-p.y+30;
 // Authored broad red body spans 80px; pink rim lies outside the damage edge.
 // One proportional scale in both axes; bounded vertical tiles avoid stretching.
 ctx.save();ctx.beginPath();ctx.rect(p.x-64*k,p.y,128*k,length);ctx.clip();
 for(let i=0,n=Math.min(96,Math.ceil(length/h));i<n;i++)ctx.drawImage(im,frame*128,0,128,512,p.x-64*k,p.y+i*h,128*k,h);
 ctx.restore();
}
warhiveDraw=function(b){if(!sc13Owns(b))return SC13.base.draw.apply(this,arguments);const C=b._cargo13;
 if(!C.ready||C.crashed)return;ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=1;
 for(const L of C.lasers)sc13BeamDraw(b,L);
 const R=C.rockets;if(R&&!R.released)for(const q of R.paths){const m=sc13RocketMount(b,q.side);combatWarningDraw(R,{x:m.x,y:m.y,ex:m.x+Math.cos(q.angle)*VH,ey:m.y+Math.sin(q.angle)*VH,progress:R.t/R.warm,width:18,fieldOnly:true,laneShape:'line'});}
 const hull=XART.get('s6cargo13_hull');ctx.drawImage(hull,C.x-b.w/2,C.y-b.h/2,b.w,b.h);
 sc13LightsDraw(b);
 if(C.coreFl>0&&Math.floor(b.t*30)%2===0){ctx.save();const p=sc13Core(b);ctx.beginPath();ctx.rect(p.x-40,p.y-60,80,120);ctx.clip();const flash=xartTint('s6cargo13_hull','#dcf6ff',.70);if(flash)ctx.drawImage(flash,C.x-b.w/2,C.y-b.h/2,b.w,b.h);ctx.restore();}
 for(const g of C.guns)sc13GunDraw(b,g);
 if(!b.dead&&sc13Open(b)){const p=sc13Core(b);if(Math.floor(b.t*4)%2===0)bmfDrawOn(ctx,window.BOF_UI_FACE||'game','REACTOR',p.x,p.y+59,7,'center');}
 ctx.restore();
};
// Read-only test/inspection surface also used by the browser encounter guide.
window.BOF_STAGE6_CARRIER={config:SC13_CFG,owns:sc13Owns,mount:sc13Mount,muzzle:sc13Muzzle,core:sc13Core,beamWidth:sc13BeamWidth,light:sc13Light,stats:SC13.stats,
 snapshot(){const b=typeof boss!=='undefined'&&boss,C=b?._cargo13;if(!C)return null;return{name:b.name,mode:C.mode,hp:b.hp,maxhp:b.maxhp,core:C.core,exposed:sc13Open(b),direction:C.dir,
  guns:C.guns.map(g=>({id:g.id,hp:g.hp,dead:g.dead,pose:g.pose,light:sc13Light(b,g),...sc13Mount(b,g.id)})),lasers:C.lasers.map(L=>({...L,x:sc13Muzzle(b,L.id).x,visibleWidth:sc13BeamWidth(L),color:'dark-red'})),queue:C.queue.map(q=>({...q})),dead:b.dead};}};
