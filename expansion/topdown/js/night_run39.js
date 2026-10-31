/* A side-on, two-plane pursuit. Projectile travel owns every point of hull damage. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,I=TD.Input,A=TD.AssaultArt,S=TD.Audio,FX=TD.FX;
 const N=TD.NightRun39={build:'overdrive1018-combat42-r5',duration:150,stats:{shots:0,missiles:0}};
 const Q=()=>root.TD_NIGHT39_ART;
 const bank=(name,a,di='east')=>Q()?.banks[name+'/'+a+'/'+di];
 const at=(q,t=0,loop=true)=>q?.frames[loop?Math.floor(Math.max(0,t)*q.fps)%q.frames.length:Math.min(q.frames.length-1,Math.floor(Math.max(0,t)*q.fps))];
 const draw=(ctx,k,x,y,s=1,o={})=>A.draw(ctx,k,x,y,{s,...o});
 const point=(c,x,y)=>({x:x+(c.phase==='onfoot'||c.phase==='boarding'?-c.cam:0),y});
 function setup(G){
  const restarts=G.night39?.restarts||0;
  G.escape29=null;G.bastion=null;G.convoy=null;G.night39={phase:'onfoot',age:0,phaseT:0,combat:0,scroll:0,cam:0,cursor:{x:320,y:230},hp:100,missiles:0,intercepts:0,bulletHits:0,missileHits:0,restarts,next:1.8,waves:0,shots:[],enemyShots:[],enemies:[],boxes:[240,455,680].map(x=>({x,y:330,hp:6,state:'closed',t:0})),pickups:[],crew:[{id:'neil',x:70,y:352},{id:'phoenix',x:105,y:340},{id:'hotwire',x:145,y:349}],truck:{x:1170,y:218,s:.30},car:{x:1030,y:260,s:.29},boarding:[],fireCd:0,missileCd:0,neilCd:0,log:[],flash:0,clear:false};
  Object.assign(G.player,{onfoot:true,pilot:'yuri',sideScroll:true,pseudo3D:false,convoy:false,x:185,y:352,aim:-Math.PI/2,a:-Math.PI/2,hp:100,max:100,dead:false,flash:0,prone:false,roll:0,jump:0,fireCd:0,moving:false,poseT:0,firing:0,inv:0});
  G.units=[];G.shots=[];G.eshots=[];G.props=[];G.structures=[];G.pickups=[];G.wrecks=[];G.boss=null;G.bossDeadT=null;G.time=0;G.kills=0;G.score=0;G.msgs=[];FX.list=[];TD.Stealth.alerts=1;TD.Cam.x=TD.Cam.y=0;TD.Cam.zoom=1;
 }
 function phase(c,name){c.phase=name;c.phaseT=0;c.log.push({event:name,at:c.age});}
 function damage(G,kind){const c=G.night39;if(c.phase!=='pursuit')return false;const d=kind==='missile'?5:1;c.hp=Math.max(0,c.hp-d);G.player.hp=c.hp;c.flash=.13;if(d===5)c.missileHits++;else c.bulletHits++;FX.boom(385+M.rnd(-60,60),280+M.rnd(-15,15),d===5?72:25,'gfx_impact_',6);S.play(d===5?'od75_hullMissile':'od75_hullBullet',.65);TD.Cam.kick(d===5?5:1.4);if(!c.hp){G.player.dead=true;G.deaths++;phase(c,'wreck');c.enemyShots=[];c.shots=[];FX.boom(390,270,180,'gfx_destruction_',6);S.stopEffects();S.play('expBoss');}return true;}
 N.setup=setup;N.damage=damage;
 function spawn(G,kind='runner',fromLeft=false){const c=G.night39,drone=kind==='drone',u={id:++c.waves,kind,x:fromLeft?-110:760,y:drone?125:434+Math.sin(c.waves)*5,hp:drone?22:9,max:drone?22:9,t:0,fireT:0,attack:'approach',cool:1.4+(c.waves%3)*.3,flash:0,dead:false,side:fromLeft?'east':'west',speed:drone?75:85+(c.waves%3)*15};c.enemies.push(u);return u;}
 N.spawn=spawn;
 function launch(c,x,y,tx,ty,kind='bullet',friendly=true,owner=null){const angle=Math.atan2(ty-y,tx-x),speed=kind==='missile'?friendly?390:155:friendly?850:215;c[friendly?'shots':'enemyShots'].push({x,y,px:x,py:y,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,angle,kind,owner,t:0,life:4,r:kind==='missile'?10:3,damage:kind==='missile'?18:2});}
 function kill(G,u){if(u.dead)return;u.dead=true;u.deadT=0;G.kills++;G.score+=u.kind==='drone'?900:350;FX.boom(u.x,u.y-40,u.kind==='drone'?100:55,'gfx_destruction_',6);S.play(u.kind==='drone'?'expB':'enemyDie',.45);}
 function hitSegment(s,x,y,rx,ry){const ax=(s.px-x)/rx,ay=(s.py-y)/ry,dx=(s.x-s.px)/rx,dy=(s.y-s.py)/ry,t=M.clamp(-(ax*dx+ay*dy)/(dx*dx+dy*dy||1),0,1);return Math.hypot(ax+dx*t,ay+dy*t)<=1;}
 const rig={truck:{wheels:[[285,320],[1028,320]],driver:[790,350],passenger:[680,350],gunner:[300,180],pivot:[300,38],muzzle:[222,-45]},car:{wheels:[[335,324],[1165,324]],driver:[800,320]}};
 function mount(c,which,key){const v=c[which],p=rig[which][key];return{x:v.x+p[0]*v.s,y:v.y+p[1]*v.s};}
 function gun(c,target=c.cursor){
  const meta=root.TD_ASSAULT_ART.assets.od39_truck_gun_upper,port=meta?.muzzle,raw=port?[port[0]-meta.anchor[0],port[1]-meta.anchor[1]]:rig.truck.muzzle,pivot=mount(c,'truck','pivot'),dx=target.x-pivot.x,dy=target.y-pivot.y,aim=Math.atan2(dy,dx),flip=dx<0,s=c.truck.s*.8,offset=[raw[0]*(flip?-1:1),raw[1]];
  // The bore is horizontal in the authored plate, above its mounting pivot.
  // Solve from that offset bore, so rounds follow the barrel to the reticle.
  const correction=Math.asin(M.clamp(raw[1]*s/Math.max(1,Math.hypot(dx,dy)),-.98,.98)),angle=flip?aim-Math.PI+correction:aim-correction;
  return{pivot,angle,flip,muzzle:{x:pivot.x+(offset[0]*Math.cos(angle)-offset[1]*Math.sin(angle))*s,y:pivot.y+(offset[0]*Math.sin(angle)+offset[1]*Math.cos(angle))*s}};
 }
 function shoot(G,missile=false,neil=false){
  const c=G.night39,p=G.player;if(missile&&c.missiles<=0)return;
  if(!neil){const q=c.phase==='onfoot'?TD.PixelLab38.bank('yuri_side',p.prone?'prone_fire':'fire',p.side39||'east'):bank('yuri_turret','fire');if((p.fireAge40??99)>=(q?.duration||.75))p.fireAge40=0;p.firing=.16;}
  const pivot=mount(c,'truck','pivot');let socket=c.phase==='onfoot'?footSocket(G):neil?{x:c.car.x+875*c.car.s,y:c.car.y+110*c.car.s}:pivot;
  const target=neil?c.enemies.filter(u=>!u.dead&&u.kind==='runner').sort((a,b)=>Math.abs(a.x-320)-Math.abs(b.x-320))[0]:{x:c.cursor.x+(c.phase==='onfoot'?c.cam:0),y:c.cursor.y};
  if(!target)return;if(!neil&&c.phase!=='onfoot')socket=gun(c,target).muzzle;launch(c,socket.x,socket.y,target.x,target.y-(neil?40:0),missile?'missile':'bullet',true,neil?'neil':'yuri');FX.attachedFlash(neil?c.car:p,()=>neil?{x:c.car.x+875*c.car.s,y:c.car.y+110*c.car.s}:c.phase==='onfoot'?socket:gun(c).muzzle,M.angTo(socket.x,socket.y,target.x,target.y),.09);
  if(missile){c.missiles--;N.stats.missiles++;S.play('missileLaunch',.55);}else{S.play(neil?'od75_rifle':'od75_minigunShot',neil?.3:.42);N.stats.shots++;}
  if(neil)c.neilFire=.12;else{p.firing=.16;c.muzzle=.1;}
 }
 function updateShots(G,dt){
  const c=G.night39;
  for(const s of [...c.shots,...c.enemyShots]){s.t+=dt;s.life-=dt;s.px=s.x;s.py=s.y;s.x+=s.vx*dt;s.y+=s.vy*dt;if(s.life<=0||s.x<-180||s.x>2100||s.y<-100||s.y>550)s.dead=true;}
  for(const s of c.shots){if(s.dead)continue;
   if(c.phase==='onfoot')for(const b of c.boxes){if(b.state==='open'||b.state==='empty')continue;if(hitSegment(s,b.x,b.y-18,28,24)){b.hp-=s.damage;b.flash=.1;b.state=b.hp<=0?'open':'damaged';s.dead=true;if(b.hp<=0){c.pickups.push({x:b.x,y:b.y-35,t:0});S.play('impactMetal',.4);FX.boom(b.x,b.y-18,30,'gfx_impact_',6);}break;}}
   if(s.dead)continue;
   for(const e of c.enemyShots)if(e.kind==='missile'&&!e.dead&&hitSegment(s,e.x,e.y,16,16)){s.dead=e.dead=true;c.intercepts++;G.score+=150;FX.boom(e.x,e.y,50,'gfx_destruction_',6);S.play('missileHit',.4);break;}
   if(s.dead)continue;
   for(const u of c.enemies)if(!u.dead&&hitSegment(s,u.x,u.y-(u.kind==='drone'?0:44),u.kind==='drone'?43:19,u.kind==='drone'?23:43)){u.hp-=s.damage;u.flash=.12;s.dead=true;if(u.hp<=0)kill(G,u);else S.play('impactMetal',.22);if(s.kind==='missile')for(const v of c.enemies)if(!v.dead&&v!==u&&Math.hypot(v.x-u.x,v.y-u.y)<105){v.hp-=10;v.flash=.12;if(v.hp<=0)kill(G,v);}break;}
  }
  for(const s of c.enemyShots)if(!s.dead&&c.phase==='pursuit'&&[[600,250,570,80],[735,100,160,120],[1080,190,150,65]].some(([x,y,rx,ry])=>hitSegment(s,c.truck.x+x*c.truck.s,c.truck.y+y*c.truck.s,rx*c.truck.s,ry*c.truck.s))){s.dead=true;damage(G,s.kind);}
  c.shots=c.shots.filter(s=>!s.dead);c.enemyShots=c.enemyShots.filter(s=>!s.dead);
 }
 function aim(c,dt){const p=I.pointer;if(p.active){c.cursor.x=M.clamp(p.x,10,630);c.cursor.y=M.clamp(p.y,65,440);}else{const v=I.state.aim;if(v&&!I.state.directionalFire){c.cursor.x=M.clamp(c.cursor.x+v[0]*420*dt,10,630);c.cursor.y=M.clamp(c.cursor.y+v[1]*420*dt,65,440);}else if(I.down('retina')){const [dx,dy]=I.dir();c.cursor.x=M.clamp(c.cursor.x+dx*390*dt,10,630);c.cursor.y=M.clamp(c.cursor.y+dy*390*dt,65,440);}}}
 function step(G,dt){
  const c=G.night39,p=G.player;c.age+=dt;c.phaseT+=dt;G.time+=dt;p.poseT+=dt;p.fireAge40=(p.fireAge40??99)+dt;p.firing=Math.max(0,p.firing-dt);c.muzzle=Math.max(0,(c.muzzle||0)-dt);c.flash=Math.max(0,c.flash-dt);c.neilFire=Math.max(0,(c.neilFire||0)-dt);c.fireCd-=dt;c.missileCd-=dt;c.neilCd-=dt;TD.Cam.x=TD.Cam.y=0;TD.Cam.zoom=1;TD.Cam.shake*=.85;FX.update(dt);aim(c,dt);if(c.phase!=='onfoot'){const g=gun(c),angle=Math.atan2(c.cursor.y-g.pivot.y,c.cursor.x-g.pivot.x),target=(1-Math.cos(angle))*8;c.gunnerTurn42=M.lerp(c.gunnerTurn42??target,target,Math.min(1,dt*14));}
  if(c.phase==='onfoot'){
   const [dx]=I.dir();p.moving=!!dx&&!I.down('retina');if(p.moving){p.x=M.clamp(p.x+dx*(p.prone?65:155)*dt,45,1370);p.side39=dx<0?'west':'east';}p.side39=p.side39||'east';
   if(I.pointer.active||I.state.aim||I.down('retina'))p.side39=c.cursor.x+c.cam<p.x?'west':'east';
   if(I.tap('prone')&&!p.roll)p.prone=!p.prone;
   if(I.tap('X')&&p.roll<=0){p.rollFromProne39=p.prone;p.roll=.55;p.rollDir=p.side39==='west'?-1:1;}if(p.roll>0){p.roll-=dt;p.x=M.clamp(p.x+p.rollDir*270*dt,45,1370);}
   if((I.tap('B')||I.tap('jump'))&&!p.jump&&!p.prone)p.jump=.65;if(p.jump>0)p.jump=Math.max(0,p.jump-dt);p.jumpZ=p.jump>0?Math.sin((.65-p.jump)/.65*Math.PI)*49:0;
   c.cam=M.clamp(p.x-220,0,900);if(I.down('A')&&c.fireCd<=0&&!p.roll){shoot(G);c.fireCd=.11;}
   c.crew.forEach((u,i)=>{const tx=p.x-58-i*32,dx=tx-u.x;u.moving=Math.abs(dx)>8;if(u.moving)u.x+=Math.sign(dx)*Math.min(Math.abs(dx),175*dt);});
   for(const k of c.pickups){k.t+=dt;if(Math.abs(k.x-p.x)<38){k.dead=true;c.missiles+=8;S.play('gd_ammoPickup',.55);c.boxes.find(b=>b.x===k.x).state='empty';}}c.pickups=c.pickups.filter(k=>!k.dead);
   if(p.x>990&&c.missiles>0){phase(c,'boarding');c.boarding=c.crew.map(u=>({...u,from:u.x,to:u.id==='neil'?c.car.x+175:c.truck.x+225}));c.yuriFrom=p.x;S.play('gd_coverEnter',.45);}
  }else if(c.phase==='boarding'){
   const t=M.clamp(c.phaseT/2.4,0,1);c.boarding.forEach(u=>{u.x=M.lerp(u.from,u.to,t);u.y=352-Math.sin(t*Math.PI)*18;});p.x=M.lerp(c.yuriFrom,c.truck.x+118,t);p.y=352-Math.sin(t*Math.PI)*90;
   if(c.phaseT>3.3){phase(c,'pursuit');c.cam=0;c.truck={x:235,y:245,s:.31};c.car={x:-30,y:310,s:.35};p.x=320;p.y=250;p.onfoot=false;p.sideScroll=true;I.holdCombat();S.play('od75_gearShift',.8);}
  }else if(c.phase==='pursuit'){
   c.combat+=dt;c.scroll+=dt*520;c.next-=dt;const [dx,dy]=I.dir();if(!I.down('retina')){c.truck.y=M.clamp(c.truck.y+dy*35*dt,230,270);c.truck.x=M.clamp(c.truck.x+dx*42*dt,210,270);}c.car.x=-40+Math.sin(c.combat*.3)*24+(c.neilFire?6:0);
   if(I.down('A')&&c.fireCd<=0){shoot(G);c.fireCd=.075;}if((I.tap('Y')||I.tap('B'))&&c.missileCd<=0&&c.missiles>0){shoot(G,true);c.missileCd=.55;}
   if(c.next<=0){const n=Math.floor(c.combat/6);spawn(G,n%3===2?'drone':'runner',n%4===1);if(c.combat>35&&n%2===0)spawn(G,'runner',n%4===0);c.next=c.combat>110?2.1:c.combat>60?2.8:3.7;}
   if(c.neilCd<=0){shoot(G,false,true);c.neilCd=1.15;}
   for(const u of c.enemies){u.t+=dt;u.flash=Math.max(0,u.flash-dt);if(u.dead){u.deadT+=dt;continue;}const targetX=u.side==='east'?90:u.kind==='drone'?540:580;u.moving40=u.attack==='approach'&&Math.abs(targetX-u.x)>.5;if(u.moving40)u.x+=Math.sign(targetX-u.x)*Math.min(Math.abs(targetX-u.x),u.speed*dt);if(u.kind==='drone')u.y=115+Math.sin(u.t*2)*25;u.cool-=dt;
    if(u.attack==='approach'&&Math.abs(u.x-targetX)<35){u.attack='track';u.cool=.8;}
    if(u.attack==='track'&&u.cool<=0){u.attack='wind';u.cool=u.kind==='drone'?1.2:.85;u.target={x:c.truck.x+(u.kind==='drone'?780:600)*c.truck.s,y:c.truck.y+(u.kind==='drone'?100:245)*c.truck.s};}
    else if(u.attack==='wind'&&u.cool<=0){u.attack='fire';u.fireT=0;u.sent=0;u.cool=.6;}
    else if(u.attack==='fire'){u.fireT+=dt;const q=bank(u.kind==='drone'?'hunter_drone':'arsenal_runner','fire',u.side),length=q?.duration||1.4,events=q?.events?.shot_frames?.map(n=>n/q.fps)||(u.kind==='drone'?[.5]:[.33,.58,.83]);while(u.sent<events.length&&u.fireT>=events[u.sent]){const port=enemySocket(u);launch(c,port.x,port.y,u.target.x,u.target.y,u.kind==='drone'?'missile':'bullet',false,u);FX.attachedFlash(u,()=>enemySocket(u),M.angTo(port.x,port.y,u.target.x,u.target.y),.1);S.play(u.kind==='drone'?'missileLaunch':'gd_soldierRifle',.55);u.sent++;}if(u.fireT>=length){u.attack='track';u.cool=u.kind==='drone'?2.5:2.1;}}
   }
   c.enemies=c.enemies.filter(u=>!u.dead||u.deadT<.5);
   if(c.combat>=N.duration){phase(c,'ram');c.enemyShots=[];c.enemies=[];c.gateX=980;S.play('warn',.55);}
  }else if(c.phase==='ram'){
   c.scroll+=dt*640;c.gateX-=dt*245;c.truck.x+=dt*16;c.car.x+=dt*40;
   if(c.gateX<c.truck.x+350){phase(c,'impact');FX.boom(c.gateX,280,250,'gfx_destruction_',6);FX.boom(c.gateX+60,210,170,'gfx_destruction_',6);S.play('od75_gateCrash',.9);TD.Cam.kick(14);}
  }else if(c.phase==='impact'){c.scroll+=dt*160;if(c.phaseT>1.25)phase(c,'fade');}
  else if(c.phase==='fade'){if(c.phaseT>1.5){c.clear=true;return 'clear';}}
  else if(c.phase==='wreck'){if(c.phaseT>3){c.restarts++;setup(G);I.holdCombat();}return;}
  updateShots(G,dt);return;
 }
 function tile(ctx,key,y,s,scroll){const m=root.TD_ASSAULT_ART.assets[key];if(!m)return;const w=m.size[0]*s,offset=scroll%w;for(let x=-offset-w;x<640+w;x+=w)draw(ctx,key,x,y,s);}
 function crew(ctx,id,action,x,y,t,s=1,di='east'){let q=bank(id,action,di)||bank(id,'idle',di);if(q)draw(ctx,at(q,t,action==='run'),x,y,s);}
 function footPlate(G,action=null,di=null){const p=G.player;di=di||p.side39||'east';const fire=TD.PixelLab38.bank('yuri_side',p.prone?'prone_fire':p.moving?'run_fire':'fire',di),firing=p.firing>0||(p.fireAge40??99)<(fire?.duration||0);let a=action||(p.roll>0?(p.rollFromProne39?'prone_roll':'roll'):p.jump>0?'jump':p.prone?(firing?'prone_fire':p.moving?'crawl':'prone_idle'):firing?p.moving?'run_fire':'fire':p.moving?'run':'idle');let q=bank('yuri_side',a,di)||TD.PixelLab38.bank('yuri_side',a,di)||TD.PixelLab38.bank('yuri_side','idle',di);if(a==='prone_idle'){const hold=TD.PixelLab38.bank('yuri_side','prone_enter',di);if(hold)return at(hold,hold.duration,false);}return at(q,p.roll>0?(.55-p.roll)/.55*q.duration:p.jump>0?(.65-p.jump)/.65*q.duration:firing?p.fireAge40||0:p.poseT*(p.moving?1.25:1),p.roll<=0&&p.jump<=0&&!firing);}
 function footSocket(G){const p=G.player,k=footPlate(G),m=root.TD_ASSAULT_ART.assets[k],v=m?.muzzle||[m.anchor[0]+(p.side39==='west'?-42:42),m.anchor[1]-(p.prone?18:70)];return{x:p.x+(v[0]-m.anchor[0]),y:p.y-(p.jumpZ||0)+(v[1]-m.anchor[1])};}
 function yuri(ctx,G,x,y,s=1,action=null,di=null){draw(ctx,footPlate(G,action,di),x,y-(G.player.jumpZ||0),s);}
 function vehicle(ctx,G,which){const c=G.night39,v=c[which],truck=which==='truck',side=c.phase==='onfoot'||c.phase==='boarding',pt=point(c,v.x,v.y),x=pt.x,y=pt.y,s=v.s,occupied=!side||c.phase==='boarding'&&c.phaseT>2.4,unit=s*2.8;
  // Window occlusion preserves a complete seated plate and its physical body unit.
  if(occupied){ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.beginPath();const window=truck?[[635,35],[745,35],[875,140],[635,140]]:[[560,54],[720,50],[930,155],[600,155]];window.forEach(([xx,yy],i)=>i?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy));ctx.closePath();ctx.clip();ctx.scale(1/s,1/s);if(truck){crew(ctx,'hotwire','sit',rig.truck.passenger[0]*s,rig.truck.passenger[1]*s,c.age,unit);crew(ctx,'phoenix','sit',rig.truck.driver[0]*s,rig.truck.driver[1]*s,c.age,unit);}else crew(ctx,'neil','sit',rig.car.driver[0]*s,rig.car.driver[1]*s,c.age,unit);ctx.restore();}
  const pivot={x:x+rig.truck.pivot[0]*s,y:y+rig.truck.pivot[1]*s};
  if(truck&&occupied){const pose=turretPose42(G);if(pose)draw(ctx,pose.key,pivot.x-160*s*(1-pose.index/8),y+260*s,s*3.2);}
  // The stand goes inside the bed. Its lower pixels are occluded by the bed's near rail.
  if(truck)draw(ctx,'od39_truck_gun_base',pivot.x,pivot.y+24*s,s*.8);
  draw(ctx,'od39_'+(truck?'truck':'mustang')+'_body',x,y,s,{flash:truck&&c.flash>0?1:0});
  for(const [wx,wy]of rig[which].wheels)draw(ctx,'od39_'+(truck?'truck':'mustang')+'_wheel',x+wx*s,y+wy*s,s*(truck?1.13:1.24),{a:side?0:c.scroll/45});
  if(truck){const g=gun(c);ctx.save();ctx.translate(pivot.x,pivot.y);if(!side){ctx.rotate(g.angle);if(g.flip)ctx.scale(-1,1);}draw(ctx,'od39_truck_gun_upper',0,0,s*.8);ctx.restore();}
 }
 function turretPose42(G){
  const c=G.night39,p=G.player,turn=bank('yuri_back42','traverse');if(!turn)return null;
  const g=gun(c),angle=Math.atan2(c.cursor.y-g.pivot.y,c.cursor.x-g.pivot.x),target=(1-Math.cos(angle))*.5*(turn.frames.length-1),index=Math.round(c.gunnerTurn42??target),firing=p.firing>0||(p.fireAge40??99)<.5,sector=Math.round(index/4)*4,q=bank('yuri_back42','recoil_'+sector);
  const useFire=firing&&q&&Math.abs(index-sector)<=1;
  return{key:useFire?at(q,p.fireAge40||0,true):turn.frames[M.clamp(index,0,turn.frames.length-1)],index,sector,bank:useFire?'recoil':'traverse'};
 }
 N.turretPose=turretPose42;
 function pSector(c,m){const a=Math.atan2(c.cursor.y-m.y,c.cursor.x-m.x);return 'aim_'+((Math.round((a+Math.PI)/(Math.PI/4))+8)%8);}
 function enemyPlate(u){const name=u.kind==='drone'?'hunter_drone':'arsenal_runner',q=bank(name,u.attack==='fire'?'fire':u.attack==='approach'?'run':'idle',u.side)||bank(name,'idle',u.side);return at(q,u.attack==='fire'?u.fireT:u.t,u.attack!=='fire');}
 function enemySocket(u){const m=root.TD_ASSAULT_ART.assets[enemyPlate(u)],p=m?.muzzle;return p?{x:u.x+p[0]-m.anchor[0],y:u.y+p[1]-m.anchor[1]}:{x:u.x+(u.side==='west'?-30:30),y:u.y-(u.kind==='drone'?0:57)};}
 function enemyDraw(ctx,u){if(u.dead)return;const k=enemyPlate(u);if(k)draw(ctx,k,u.x,u.y,1,{flash:u.flash>0?1:0});}
 function warning(ctx,u,c){if(u.dead||!['wind','fire'].includes(u.attack))return;const {x,y}=enemySocket(u),target=u.target||{x:c.truck.x+600*c.truck.s,y:c.truck.y+245*c.truck.s},col=u.attack==='fire'?'red':u.attack==='wind'?(u.cool<.28?'red':'yellow'):'green',length=Math.hypot(target.x-x,target.y-y);ART.draw(ctx,'bmfx_fov_'+col+'_tall',x,y,{ax:159.5,ay:11,a:M.angTo(x,y,target.x,target.y),sx:(u.kind==='drone'?24:34)/126,sy:length/267,alpha:col==='green'?.5:.8});}
 function shotDraw(ctx,s,cam=0){const di=s.vx<0?'west':'east',q=root.TD_PIXELLAB38_ART.banks['fx/'+(s.kind==='missile'?'rocket':'ballistic')+'/side/'+di],k=TD.PixelLab38.frame(q,s.t,true),a=s.angle-(di==='west'?Math.PI:0),scl=s.kind==='missile'?.9:1.3,n=Math.hypot(s.vx,s.vy)||1;for(let j=2;j>0;j--)draw(ctx,k,s.x-cam-s.vx/n*j*7,s.y-s.vy/n*j*7,scl*.75,{a,alpha:.35-j*.06});draw(ctx,k,s.x-cam,s.y,scl*1.25,{a,tint:'#060b18'});draw(ctx,k,s.x-cam,s.y,scl,{a,flash:.12});}
 function drawWorld(ctx,G){
  const c=G.night39;if(!c)return;ctx.save();ctx.imageSmoothingEnabled=false;ctx.fillStyle='#080c19';ctx.fillRect(0,0,640,480);
  tile(ctx,'nr39_skyline',-60,1.25,(c.phase==='onfoot'?c.cam*.18:c.scroll*.08));tile(ctx,'nr39_midground',100,1.25,(c.phase==='onfoot'?c.cam*.45:c.scroll*.3));tile(ctx,'nr39_road',275,1.65,c.phase==='onfoot'?c.cam:c.scroll);
  const side=['onfoot','boarding'].includes(c.phase);
  if(c.phase==='ram'||['impact','fade'].includes(c.phase))draw(ctx,'nr39_gate',c.gateX||590,120,1.15,{flash:c.phase==='impact'&&c.phaseT<.12?1:0,alpha:c.phase==='impact'?Math.max(0,1-c.phaseT*1.3):c.phase==='fade'?0:1});
  if(side){vehicle(ctx,G,'truck');vehicle(ctx,G,'car');for(const b of c.boxes){b.flash=Math.max(0,(b.flash||0)-1/60);const k='od39_crate_'+b.state;draw(ctx,k,b.x-c.cam,b.y-15,.22,{flash:b.flash>0?1:0});}for(const k of c.pickups)draw(ctx,'od39_missile_pickup',k.x-c.cam,k.y+Math.sin(k.t*5)*5,.16);const people=c.phase==='boarding'?c.boarding:c.crew;for(const u of people)if(c.phase!=='boarding'||c.phaseT<2.4)crew(ctx,u.id,u.moving||c.phase==='boarding'?'run':'idle',u.x-c.cam,u.y,c.age,.78);if(c.phase!=='boarding'||c.phaseT<2.4)yuri(ctx,G,G.player.x-c.cam,G.player.y);}
  else{for(const u of c.enemies.filter(u=>u.kind==='drone')){warning(ctx,u,c);enemyDraw(ctx,u);}vehicle(ctx,G,'truck');vehicle(ctx,G,'car');for(const u of c.enemies.filter(u=>u.kind!=='drone')){warning(ctx,u,c);enemyDraw(ctx,u);}}
  for(const s of c.shots)shotDraw(ctx,s,side?c.cam:0);for(const s of c.enemyShots)shotDraw(ctx,s);ctx.save();if(side)ctx.translate(-c.cam,0);FX.draw(ctx,1);ctx.restore();
  const retina=ART.get('retmb_0');if(retina)ART.draw(ctx,'retmb_0',c.cursor.x,c.cursor.y,{s:32/retina.sw,alpha:.9,palette:'#ef4242'});if(c.phase==='fade'){ctx.fillStyle='rgba(0,0,0,'+M.clamp(c.phaseT/1.2,0,1)+')';ctx.fillRect(0,0,640,480);}ctx.restore();
 }
 function hud(ctx,text,G){const c=G.night39;if(!c)return true;ctx.fillStyle='rgba(4,8,18,.88)';ctx.fillRect(0,0,640,52);text('BULLETS OF FURY / OVERDRIVE',12,14,10,'#ffbf6f');text('NIGHT RUN',628,14,12,'#d8fff3','right');
  if(['onfoot','boarding'].includes(c.phase)){text(c.phase==='onfoot'?'SHOOT SUPPLY CRATES / COLLECT MISSILES / REACH THE TRUCK':'CREW BOARDING / PHOENIX AT THE WHEEL',320,36,10,'#aaf7dd','center');}else{text('TRUCK '+c.hp+'%',14,34,12,c.hp<30?'#ff5555':'#9dffba');ctx.fillStyle='#381d27';ctx.fillRect(122,29,168,9);ctx.fillStyle=c.hp<30?'#fc493e':'#77ddb2';ctx.fillRect(123,30,166*c.hp/100,7);text(Math.max(0,Math.ceil(N.duration-c.combat))+' SEC',625,34,11,'#fff','right');}
  draw(ctx,'od39_missile_badge',25,455,.09);text(String(c.missiles),45,454,13,'#fff');text(c.phase==='wreck'?'TRUCK LOST / REGROUPING':c.phase==='ram'?'HOLD ON / RAM THE BASE GATE':c.phase==='impact'?'BREACH!':c.phase==='pursuit'?'YURI / TURRET     NIEL / COVERING FIRE':'ALL FOUR / MOVE OUT',320,455,10,'#b5eee5','center');return true;
 }
 const m=TD.MISSIONS.find(m=>m.id===6);Object.assign(m,{mode:'turret',view640:true,setup,exclusiveStep:step,drawWorld,hud,boss:null,briefSprite(ctx,G,x,y){draw(ctx,'od39_truck_body',x-160,y-40,.26);},help:['ON FOOT: WASD / D-PAD MOVE','MOUSE / RIGHT STICK: AIM; J / A: FIRE','SHOOT CRATES, WALK OVER MISSILES, REACH THE TRUCK','F: PRONE; SPACE: ROLL; K: JUMP','PURSUIT: AIM RETICLE AND HOLD FIRE','U / B: FIRE A COLLECTED MISSILE','D-PAD: SHIFT TRUCK; HOLD RETINA FOR FREE AIM','DESTROY DRONE MISSILES BEFORE IMPACT','BULLET = 1% HULL / MISSILE = 5% HULL','100% HULL / SURVIVE / RAM THE BASE GATE'],keys:()=>[['dpad','MOVE'],['a','FIRE'],['y','MISSILE'],['z','RETINA'],['start','PAUSE']],score(G,R){const c=G.night39;R.extraRows=[['TRUCK INTEGRITY',c.hp+'%'],['MISSILES INTERCEPTED',c.intercepts],['PURSUIT RESTARTS',c.restarts]];}});
 m.data.name='NIGHT RUN / OVERDRIVE';m.data.brief=['ALL FOUR ON FOOT. SHOOT CRATES AND COLLECT MISSILES.','PHOENIX DRIVES / HOTWIRE RIDES / YURI MANS THE TURRET.','NIEL COVERS THE TRUCK FROM HIS MUSTANG.','SURVIVE THE PURSUIT AND RAM THE BASE GATE.'];
 N.step=step;N.draw=drawWorld;N.shoot=shoot;N.updateShots=updateShots;N.kill=kill;N.gun=gun;N.rig=rig;N.footPlate=footPlate;N.footSocket=footSocket;N.enemyPlate=enemyPlate;N.enemySocket=enemySocket;
})(window);
