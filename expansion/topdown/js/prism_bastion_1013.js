/* Prism Bastion: an authored rear-view cover shooter, with screen-space fire
 * projected into depth. Own simulation keeps its aiming and collision together. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,I=TD.Input,A=TD.Audio,FX=TD.FX;
 const clamp=M.clamp,lerp=M.lerp;
 const PACK=root.TD_BASTION_ART;
 if(PACK){Object.assign(root.TD_ASSAULT_ART.assets,PACK.assets);Object.assign(root.TD_ASSAULT_ART.sequences,PACK.sequences);}
 const art=TD.AssaultArt;
 const FAMILIES={rifle:{bank:'pb_rifle',hp:10,scale:.52,cd:2.4,score:400},heavy:{bank:'pb_heavy',hp:25,scale:.65,cd:3.2,score:900},rocket:{bank:'pb_rocket',hp:14,scale:.54,cd:3.8,score:650},laser:{bank:'pb_laser',hp:13,scale:.53,cd:3.1,score:600}};
 Object.assign(FAMILIES,{shotgun:{bank:'pb_rifle',hp:14,scale:.53,cd:2.7,score:650},double:{bank:'pb_rifle',hp:18,scale:.54,cd:3.1,score:800},roller:{bank:'pb_rifle',hp:16,scale:.54,cd:2.3,score:800},flame:{bank:'pb_heavy',hp:19,scale:.56,cd:2.8,score:850},flyer:{bank:'pb_rifle',hp:12,scale:.53,cd:2.3,score:600},bat:{bank:'pb_rifle',hp:8,scale:.42,cd:2.4,score:450}});
 const LANES=[80,240,400,560],TOTAL_WAVES=5;
 const GUNS={rifle:{name:'RIFLE',cd:.095,damage:2,ammo:0},shotgun:{name:'SPREAD SHOTGUN',cd:.34,damage:2,ammo:22},laser:{name:'LASER BEAM',cd:.20,damage:4,ammo:34},minigun:{name:'MINIGUN',cd:.042,damage:1.6,ammo:180}};
 const assets=()=>root.TD_ASSAULT_ART.assets,sequences=()=>root.TD_ASSAULT_ART.sequences;
 function frame(bank,phase){const modern=bank.startsWith('pb_')?'pb16_'+bank.slice(3):bank,q=sequences()[modern]||sequences()[bank]||PACK?.sequences[bank];return q?.frames[Math.min(q.frames.length-1,Math.floor(Math.max(0,phase)))];}
 function animated(bank,t,fallback){const q=sequences()[bank];return q?frame(bank,Math.floor(t*(q.fps||10))%q.frames.length):fallback;}
 function key(preferred,fallback){return assets()[preferred]?preferred:fallback;}
 function draw(ctx,k,x,y,s=1,o){if(k&&!TD.Grid21?.flat(ctx,k,x,y,s,o))art.draw(ctx,k,x,y,Object.assign({s},o));}
 function scale(k,fallback){return assets()[k]?.drawScale??fallback;}
 function message(G,text){G.msgs=[{text,t:0}];}
 function freshCover(G){const c=G.bastion;c.cover=LANES.map((x,i)=>({x,index:i,hp:52,max:52,flash:0}));c.wallGeneration++;}
 function coverAt(G,x){return G.bastion.cover?.[clamp(Math.floor(x/160),0,3)];}
 function wallPhase(w){return w.hp<=0?3:w.hp<w.max*.34?2:w.hp<w.max*.70?1:0;}
 function damageCover(G,x,n){const w=coverAt(G,x);if(!w||w.hp<=0)return false;const old=wallPhase(w);w.hp=Math.max(0,w.hp-n);w.flash=.09;G.bastion.wallDamage+=n;A.play('impactMetal',.50);TD.Cam.kick(Math.abs(G.player.x-x)<90?2.2:.65);G.bastion.impactCount29=(G.bastion.impactCount29||0)+1;
  if(wallPhase(w)!==old){FX.boom(w.x,394,45,'gfx_destruction_',6);A.play('impactMetal',.35);if(w.hp===0){G.bastion.brokenWalls++;message(G,'COVER BREACHED / SHIFT TO AN INTACT SECTION');}}return true;}
 function setup(G){
  G.bastion={room:0,phase:'advance',t:0,age:0,wave:0,totalWave:0,next:.8,killed:0,cursor:{x:320,y:175},bullets:[],shotEchoes:[],enemyShots:[],hazards:[],sparks:[],barrels:[],entryLog:[],intercepts:0,coverStops:0,damage:0,wallDamage:0,wallGeneration:0,brokenWalls:0,barrelKills:0,vaults:0,clearT:0,flash:0,lastMouse:null,spawned:0,clearedWaves:0,enemyCover:[],pickups:[],pickupLog:[],transitionLog:[],gunShots:{},quickShots:0,enemyCoverStops:0,skin:0,coreRays:[],coreLog:[]};
  Object.assign(G.player,{pseudo3D:true,onfoot:true,x:320,y:448,frontCover29:false,baseVault29:null,hp:1,max:1,oneHit29:true,inv:1.5,dead:false,deadT:0,reviveT:0,prone:false,roll:0,rollCd:0,rollProne:false,stance:'crouch',rise:0,strafe:0,fireCd:0,firing:0,grenadeCd:0,smoke:5,aim:Math.PI,aimSector:2,moving:false,blindfire:false,quickSide:0,quickSideT:0,groundGun:'rifle',gunAmmo:0,peekShotT:0});
  G.units=[];G.shots=[];G.eshots=[];G.props=[];G.structures=[];G.wrecks=[];G.boss=null;G.bossDeadT=null;G.msgs=[];G.time=0;TD.Stealth.alerts=1;FX.list=[];TD.Cam.x=TD.Cam.y=0;TD.Cam.zoom=1;
  freshCover(G);message(G,'PRISM BASTION / BREACH THE CORE');
 }
 function spawn(G,kind,x,delay=0){
  const c=G.bastion,d=FAMILIES[kind],n=Math.max(0,c.totalWave-1),hp=Math.round(d.hp*(1+n*.09));
  const barricade={x,y:285,hp:18+(kind==='heavy'?8:0),max:18+(kind==='heavy'?8:0),kind:c.spawned%3===0?'wall':c.spawned%3===1?'crate':'armored',flash:0};c.enemyCover.push(barricade);
  const u={kind,type:'odRobot',x:320,y:220,homeX:x,targetY:273,hp,max:hp,age:0,a:0,dead:false,flash:0,cd:.85+(c.spawned%3)*.22,burst:0,burstCd:0,phase:'queued',delay,walk:0,velocity:0,scale:d.scale*.25,cover:barricade,duck:0,cycles:0,canVault:false,lateral42:(c.spawned%2?1:-1),roam42:0,vaultDelay:1.3+(c.spawned%2)*.6};
  c.entryLog.push({x:u.x,y:u.y,door:true,room:c.room,wave:c.totalWave});c.spawned++;G.units.push(u);return u;
 }
 function enemyCoverBody(w,phase=wallPhase(w)){const k=frame(w.kind==='crate'?'pb18_enemy_crate':w.kind==='armored'?'pb18_armored_crate':'pb17_enemy_cover_wall',phase),m=assets()[k],q=m?.bounds,sc=scale(k,1)*.9;return q?{x:w.x+((q[0]+q[2])/2-m.anchor[0])*sc,y:w.y+((q[1]+q[3])/2-m.anchor[1])*sc,rx:(q[2]-q[0])*sc*.5,ry:(q[3]-q[1])*sc*.5}:{x:w.x,y:w.y-21,rx:36,ry:21};}
 function enemyCoverHit(G,w,n){if(w.hp<=0)return;const old=wallPhase(w);w.hp=Math.max(0,w.hp-n);w.flash=.10;G.bastion.enemyCoverStops++;if(old!==wallPhase(w)){FX.boom(w.x,w.y-20,w.hp?34:65,'gfx_destruction_',6);A.play('impactMetal',.25);}}
 function launchPickup(G,u){if(!u.elite||u.dropDone)return;u.dropDone=true;const c=G.bastion,q=unitBody(u),gun=['flamethrower','cryo_lance','minigun'][(c.totalWave-2+3)%3];c.pickups.push({gun,sx:q.x,sy:q.y,x:q.x,y:q.y,t:0,duration:1.05});c.pickupLog.push({event:'launch',gun,wave:c.totalWave});}
 function stepPickups(G,dt){const c=G.bastion,p=G.player;for(const q of c.pickups){q.t+=dt;const t=clamp(q.t/q.duration,0,1),ease=t*t*(3-2*t);q.x=lerp(q.sx,p.x,ease);q.y=lerp(q.sy,p.y-52,ease)-Math.sin(t*Math.PI)*70;
   if(t===1&&!p.dead){p.groundGun=q.gun;p.gunAmmo=GUNS[q.gun].ammo;q.dead=true;c.pickupLog.push({event:'collect',gun:q.gun,wave:c.totalWave});message(G,GUNS[q.gun].name+' / READY');A.play('powerup',.65);}}
  c.pickups=c.pickups.filter(q=>!q.dead);
 }
 function turrets(G){const c=G.bastion,n=c.totalWave;c.turrets=[{x:254,y:159,hp:12+n,max:12+n,kind:'gun',cd:2.8,age:0,flash:0},{x:386,y:159,hp:12+n,max:12+n,kind:n>=3?'laser':'gun',cd:3.6,age:0,flash:0}];c.wallCore={x:320,y:138,hp:30+n*3,max:30+n*3,age:0,flash:0};c.coreLog.push({room:n,x:320,y:138});
 }
 function makeBarrels(G){const c=G.bastion,shift=c.totalWave%2?0:25;c.barrels=[{x:145+shift,y:294,hp:6,max:6},{x:207+shift,y:304,hp:6,max:6},{x:487-shift,y:327,hp:6,max:6}].map((b,i)=>Object.assign(b,{id:i,dead:false,flash:0,deathT:0}));}
 function wave(G){const c=G.bastion;if(c.phase==='fight'&&G.units.some(u=>!u.dead))return false;
  c.totalWave++;if(c.totalWave===TOTAL_WAVES){startBoss(G);return true;}c.room=c.totalWave-1;c.wave=1;c.phase='fight';c.t=0;c.next=999;c.skin=Math.floor((c.totalWave-1)/2)%3;G.units=[];c.enemyShots=[];c.bullets=[];c.enemyCover=[];if(!c.coverPrepared)freshCover(G);c.coverPrepared=false;makeBarrels(G);turrets(G);
  const schedules=[['rifle','shotgun','double'],['rifle','roller','rocket','heavy'],['shotgun','double','laser','flyer'],['roller','flame','heavy','rifle','bat'],['double','heavy','rocket','roller','laser'],['shotgun','flame','laser','flyer','rocket','heavy'],['roller','double','rocket','laser','bat','heavy']];
  const kinds=schedules[c.totalWave-1]||schedules.at(-1),slots=[174,450,280,475,225,365];
  kinds.forEach((kind,i)=>{const u=spawn(G,kind,c.totalWave%2?slots[i]:640-slots[i],i*.68);if(c.totalWave>=2&&i===kinds.length-1){u.elite=true;u.hp=Math.round(u.hp*1.25);u.max=u.hp;}});
  message(G,'DEFENSE LINE '+c.totalWave+' / '+'BREAK THE DOOR CORE + CORNER TURRETS');A.play('warn',.6);return true;
 }
 function enterRoom(G){return wave(G);}
 function bullet(G,x,y,kind,delay=0,near=false){const c=G.bastion,p=G.player;near=near||!!p.frontCover29;
  c.enemyShots.push({sx:x,sy:y,x,y,tx:clamp(p.x+(kind==='mg'?(c.enemyShots.length%3-1)*17:0),45,595),ty:p.frontCover29?p.y-43:near?413:405,t:-delay,duration:(near?.34:kind==='laser'?.46:kind==='rocket'?.80:.56)/(TD.DIFFICULTIES[TD.difficulty||'normal'].tempo),kind,near,dead:false,damage:kind==='rocket'?2:1,burst:false});
 }
 function harm(G,n){const p=G.player,c=G.bastion;if(p.roll>.08&&p.roll<.42||p.baseVault29&&p.baseVault29.t>.1&&p.baseVault29.t<.6)return;if(p.dead||p.inv>0||c.phase==='breach'||['transform','reveal'].includes(G.boss?.state))return;const damage=p.oneHit29?p.hp:n*TD.DIFFICULTIES[TD.difficulty||'normal'].damage;p.hp=Math.max(0,Math.round((p.hp-damage)*100)/100);p.inv=.85;p.flash=.15;c.damage+=damage;A.play('hit',.6);TD.Cam.kick(3);
  if(p.hp<=0){p.dead=true;p.deadT=0;p.quickSide=0;p.firing=0;p.blindfire=false;p.moving=false;G.deaths++;A.play('playerDeath');c.enemyShots=[];c.hazards=[];}
 }
 function kill(G,u){if(u.dead)return;launchPickup(G,u);u.dead=true;u.deathT=0;G.kills++;G.score+=FAMILIES[u.kind]?.score||500;G.bastion.killed++;FX.boom(u.x,u.y-20,60,'gfx_destruction_',6);A.play('enemyDie',.5);}
 function startBoss(G){const c=G.bastion;c.room=4;c.totalWave=TOTAL_WAVES;c.wave=5;c.phase='core';c.t=0;c.turrets=[{x:254,y:159,hp:20,max:20,kind:'gun',cd:3.2,age:0,flash:0},{x:386,y:159,hp:20,max:20,kind:'laser',cd:4,age:0,flash:0}];c.wallCore=null;G.units=[];c.enemyShots=[];c.bullets=[];c.barrels=[];c.enemyCover=[];c.coreRays=[];c.coreLog.push({room:5,x:320,y:166,master:true});if(!c.coverPrepared)freshCover(G);c.coverPrepared=false;c.skin=2;
  G.boss={name:'PRISM CONTAINMENT REACTOR',form:'core',state:'enter',x:320,y:190,hp:220,max:220,t:0,phaseT:0,gauge:0,flash:0,cd:2.8,gait:0,alive(){return !this.dead;},hpFrac(){return this.hp/this.max;}};
  message(G,'FOUR LINES BREACHED / PRISM CONTAINMENT REACTOR');A.playMusic('lastHope',1.8);A.play('warn');
 }
 function coreHit(G,n){const b=G.boss;if(!b||b.dead||b.state==='enter'||b.state==='transform'||b.state==='jump')return false;b.hp=Math.max(0,b.hp-n);b.flash=.12;if(b.form==='helios'&&!(b.hitAge<.32))b.hitAge=0;
  if(b.hp<=0&&b.form==='core'){b.state='transform';b.t=0;G.bastion.enemyShots=[];G.bastion.hazards=[];G.bastion.coreRays=[];message(G,'CONTAINMENT FAILURE / GLASS FRACTURE');A.play('expBoss');}
  else if(b.hp<=0){b.dead=true;b.state='dead';b.t=0;G.bastion.enemyShots=[];G.bastion.hazards=[];G.bastion.phase='victory';G.bastion.clearT=0;G.score+=40000;A.play('expBoss');FX.boom(b.x,b.y,200,'gfx_destruction_',6);message(G,'HELIOS / PRISM ENTITY DESTROYED');}
  return true;
 }
 function hazard(G,kind,x,delay,duration){G.bastion.hazards.push({kind,x,t:0,delay,duration,hit:false});}
 function bossStep(G,dt){const c=G.bastion,b=G.boss,p=G.player;if(!b||b.dead)return;b.t+=dt;b.hitAge=(b.hitAge??99)+dt;b.phaseT+=dt;b.flash=Math.max(0,b.flash-dt);
  if(b.state==='enter'){b.gauge=clamp(b.t/(b.form==='core'?1.3:2.6),0,1);if(b.t> (b.form==='core'?1.6:3)){b.state='fight';b.t=0;b.phaseT=0;}return;}
  if(b.state==='transform'){
   c.coreRays=[];c.flash=b.t<.75?0:b.t<1.25?(b.t-.75)/.5:1;
   if(b.t>.1&&b.t<1.0&&G.t%9===0)FX.boom(b.x+Math.sin(b.t*11)*65,b.y,115,'gfx_destruction_',6);
   if(b.t>2.2){Object.assign(b,{name:'HELIOS / PRISM ENTITY',form:'helios',state:'reveal',hp:360,max:360,t:0,phaseT:0,gauge:0,x:320,y:320,pattern:0,gait:0});c.enemyShots=[];c.hazards=[];c.turrets=[];message(G,'HELIOS / PRISM ENTITY');A.play('warn');}return;
  }
  if(b.state==='reveal'){c.flash=clamp(1-b.t/.9,0,1);if(b.t>.9){b.state='enter';b.t=0;c.flash=0;}return;}
  if(b.form==='core'){
   const angle=b.phaseT*.85,active=b.phaseT%5.2>1.1&&b.phaseT%5.2<3.9;
   c.coreRays=[0,1,2].map(i=>({angle:angle+i*Math.PI*2/3,active,length:340}));
   b.rayHitCd=Math.max(0,(b.rayHitCd||0)-dt);
   for(const ray of c.coreRays){if(!active||b.rayHitCd>0)continue;const ex=b.x+Math.cos(ray.angle)*ray.length,ey=b.y+Math.sin(ray.angle)*ray.length,ax=G.player.x-b.x,ay=402-b.y,dx=ex-b.x,dy=ey-b.y,k=clamp((ax*dx+ay*dy)/(dx*dx+dy*dy),0,1);
    if(Math.hypot(ax-dx*k,ay-dy*k)<15){b.rayHitCd=.6;/* Reactor rays are visual charge guides; only travelling bolts can hit. */}}
   b.boltCd29=(b.boltCd29||0)-dt;if(active&&b.boltCd29<=0){b.boltCd29=.32;for(const ray of c.coreRays){const down=Math.sin(ray.angle)>.15,dist=down?(405-b.y)/Math.sin(ray.angle):340,tx=b.x+Math.cos(ray.angle)*dist,ty=down?405:b.y+Math.sin(ray.angle)*340;c.enemyShots.push({sx:b.x,sy:b.y,x:b.x,y:b.y,tx,ty,t:0,duration:.62,kind:'laser',near:false,dead:false,damage:1,burst:false,visualOnly:!down||tx<0||tx>640});}}b.boltCd29=(b.boltCd29||0)-dt;if(active&&b.boltCd29<=0){b.boltCd29=.32;for(const ray of c.coreRays){const tx=b.x+Math.cos(ray.angle)*340,ty=b.y+Math.sin(ray.angle)*340;c.enemyShots.push({sx:b.x,sy:b.y,x:b.x,y:b.y,tx,ty,t:0,duration:.62,kind:'laser',near:false,dead:false,damage:1,burst:false});}}return;
  }
  if(b.state==='fight'){
   const n=b.pattern%4;
   if(n===0){b.state='run';b.fromX=b.x;b.toX=b.x<320?735:-95;b.runT=0;b.exitPause=0;}
   else if(n===1){b.state='volley';b.volley=0;}
   else if(n===2){b.state='lightning';b.lightning=false;}
   else{b.state='jump';b.jumpX=p.x;b.jumpY=b.y;b.fromX=b.x;hazard(G,'geyser',p.x,1.2,1.7);message(G,'GROUND SLAM / MOVE!');A.play('warn',.65);}
   b.t=0;return;
  }
  if(b.state==='run'){
   b.runT+=dt;const speed=240;b.x+=Math.sign(b.toX-b.fromX)*speed*dt;b.gait+=speed*dt/110;
   if(b.x<=-95||b.x>=735){b.state='return';b.t=0;b.x=clamp(b.x,-95,735);b.returnFrom=b.x;b.toX=b.x<0?190:450;}
  }else if(b.state==='return'){
   if(b.t>.3){b.x+=Math.sign(b.toX-b.returnFrom)*170*dt;b.gait+=170*dt/90;if(Math.abs(b.x-b.toX)<5){b.x=b.toX;b.state='recover';b.t=0;}}
  }else if(b.state==='volley'){
   if(b.volley<3&&b.t>.60+b.volley*.96){const pose=heliosPose(b),m=assets()[pose.key],hand=m.emitter||[m.anchor[0]+65,m.anchor[1]-120],bodyScale=scale(pose.key,.85),sx=b.x+(hand[0]-m.anchor[0])*bodyScale*(pose.flip?-1:1),sy=b.y+(hand[1]-m.anchor[1])*bodyScale;for(const offset of [-80,0,80]){const old=p.x;p.x=clamp(old+offset,60,580);bullet(G,sx,sy,'orb');p.x=old;}b.volley++;A.play('enemyLaser',.6);}if(b.t>3.15){b.state='recover';b.t=0;}
  }else if(b.state==='lightning'){
   if(b.t>.7&&!b.lightning){b.lightning=true;const gap=(b.pattern>>2)%3;for(let i=0;i<3;i++)if(i!==gap)hazard(G,'beam',120+i*200,.8,.85);A.play('laser',.7);}if(b.t>2.7){b.state='recover';b.t=0;}
  }else if(b.state==='jump'){
   b.x=lerp(b.fromX,b.jumpX,clamp(b.t/1.15,0,1));b.jumpZ=Math.sin(clamp((b.t-.22)/.68,0,1)*Math.PI)*180;
   if(b.t>=1.15){b.jumpZ=0;b.y=355;TD.Cam.kick(9);A.play('expB');b.state='recover';b.t=0;}
  }else if(b.state==='recover'){
   if(b.t<.65&&b.hitAge>=.32){const dx=(b.pattern%2?-1:1)*65*dt;b.x=clamp(b.x+dx,90,550);b.sideGait=(b.sideGait||0)+Math.abs(dx)/52;}b.y=lerp(b.y,320,dt*3);if(b.t>1.15){b.pattern++;b.state='fight';b.t=0;}
  }
 }
 function intersects(s,x,y,rx,ry){
  // Swept segment against a rendered target ellipse, in the same screen space.
  const ax=(s.oldX-x)/rx,ay=(s.oldY-y)/ry,bx=(s.x-x)/rx,by=(s.y-y)/ry,dx=bx-ax,dy=by-ay;
  const t=clamp(-(ax*dx+ay*dy)/(dx*dx+dy*dy||1),0,1);return(ax+dx*t)**2+(ay+dy*t)**2<=1;
 }
 function aimSector(G){const p=G.player,c=G.bastion,a=Math.atan2(c.cursor.x-p.x,Math.max(12,p.y-64-c.cursor.y));
  if(p.quickSide){p.aimSector=p.quickSide<0?0:4;p.aim=p.quickSide*Math.PI/2;return p.aimSector;}
  const cuts=[-1.02,-.36,.36,1.02];let n=cuts.filter(v=>a>v).length;
  // Small hysteresis prevents a trembling cursor from flipping torso facings.
  if(p.aimSector!=null&&n!==p.aimSector){const edge=cuts[Math.min(n,p.aimSector)];if(Math.abs(a-edge)<.055)n=p.aimSector;}
  p.aimSector=n;p.aim=a;return n;
 }
 function playerPose(G){const native=TD.Combat39?.basePlayerPose(G);if(native)return native;const p=G.player,c=G.bastion,d=p.aimSector??2,dir=['west','northwest','north','northeast','east'][d];if(p.baseVault29)return frame('pb19_yuri_north_hop',Math.min(7,Math.floor(p.baseVault29.t/.72*8)));
  if(c.phase==='breach'){const tr=c.transition;if(tr.phase==='hop')return frame('pb19_yuri_north_hop',Math.min(7,Math.floor(tr.t/.75*8)));return p.moving||tr.phase==='walk'?animated('pb19_yuri_north_walk',c.age,null):frame('pb19_yuri_north_fire',0);}
  if(p.dead)return frame('pb19_yuri_north_death',Math.min(7,Math.floor(p.deadT*9)));
  if(p.reviveT>0)return frame('pb19_yuri_north_revive',Math.min(7,Math.floor((1-p.reviveT)*8)));
  if(p.roll>0)return frame(p.rollProne?'pb20_yuri_roll_prone':'pb20_yuri_roll_stand',Math.min(7,Math.floor((.5-p.roll)/.5*8)));
  if(p.proneBlend?.t<.38&&!p.quickSide)return frame('pb19_yuri_north_prone_transition',p.proneBlend.to==='prone'?Math.min(7,Math.floor(p.proneBlend.t/.38*8)):7-Math.min(7,Math.floor(p.proneBlend.t/.38*8)));
  if(p.prone&&!p.blindfire&&!p.quickSide)return frame('pb20_yuri_wall_prone',p.moving?Math.floor(((p.strafe%1+1)%1)*8):0);
  if(p.throwT>0){const q=sequences()['yuri_'+dir+'_grenade'];return q.frames[Math.min(q.frames.length-1,Math.floor((.6-p.throwT)/.6*q.frames.length))];}
  if(p.blindfire)return animated('pb19_yuri_north_blindfire',p.fireAnimT||0,null);
  if(p.rise<.25)return p.moving?frame('pb20_yuri_wall_crouch',Math.floor(((p.strafe%1+1)%1)*8)):frame('pb20_yuri_wall_crouch',0);
  if(p.rise<.94)return frame('pb19_yuri_north_peek',Math.min(7,Math.round(p.rise*7)));
  const q=sequences()['yuri_'+dir+'_'+(p.moving?'walk':p.firing>0?'fire':'idle')];
  return q.frames[p.moving?Math.floor(((p.strafe%1+1)%1)*q.frames.length)%q.frames.length:p.firing>0?Math.floor((p.shotAge||0)*64)%q.frames.length:0];
 }
 function playerScale(G){return 1.30;}
 function playerCoverOffset(G){const p=G.player;if(p.baseVault29||p.frontCover29||G.state==='brief'||G.bastion.phase==='breach'||p.dead||p.reviveT>0||p.roll>0||p.quickSide||!coverAt(G,p.x)?.hp)return 0;return p.blindfire?-40:-18*clamp(p.rise,0,1);}
 function playerSocket(G){const p=G.player,m=assets()[playerPose(G)],q=m?.muzzle||[m?.anchor[0]+44,m?.anchor[1]-180],s=playerScale(G);return{x:p.x+(q[0]-m.anchor[0])*s,y:p.y+playerCoverOffset(G)+(q[1]-m.anchor[1])*s};}
 function fire(G){const c=G.bastion,p=G.player;if(p.firing<=0)p.fireAnimT=0;p.firing=.16;p.shotAge=0;const socket=playerSocket(G),spread=p.blindfire?Math.sin(c.age*23)*21:0,tx=clamp(c.cursor.x+spread,24,616),ty=clamp(c.cursor.y+(p.blindfire?Math.cos(c.age*17)*14:0),80,449),gun=p.groundGun||'rifle',spec=GUNS[gun],volley={hits:new Map()};
  const offsets=gun==='shotgun'?[-.20,-.10,0,.10,.20]:gun==='flamethrower'?[-.045,.045]:[0],a=Math.atan2(ty-socket.y,tx-socket.x),length=Math.min(spec.range||9999,Math.hypot(tx-socket.x,ty-socket.y));
  for(const da of offsets)c.bullets.push({x:socket.x,y:socket.y,oldX:socket.x,oldY:socket.y,sx:socket.x,sy:socket.y,tx:socket.x+Math.cos(a+da)*(length+(gun==='laser'?70:8)),ty:socket.y+Math.sin(a+da)*(length+(gun==='laser'?70:8)),t:0,duration:gun==='laser'?.12:gun==='flamethrower'?.5:gun==='cryo_lance'?.24:.16,damage:spec.damage,dead:false,blindfire:p.blindfire,gun,volley,hit:new Set(),pierce:gun==='laser'?3:gun==='cryo_lance'?2:1});
  p.muzzleAim=M.angTo(socket.x,socket.y,tx,ty);FX.attachedFlash(p,()=>playerSocket(G),p.muzzleAim,.14);
  p.fireCd=Math.max(-.016,p.fireCd)+(p.blindfire?Math.max(.14,spec.cd):spec.cd);c.gunShots[gun]=(c.gunShots[gun]||0)+1;if(p.quickSide)c.quickShots++;if(gun!=='rifle'&&--p.gunAmmo<=0){p.groundGun='rifle';p.gunAmmo=0;message(G,'RIFLE / SPECIAL AMMO EMPTY');}A.play(gun==='flamethrower'?'firewallLaunch':gun==='cryo_lance'?'enemyHeavyLaser':gun==='laser'?'laser':'gd_soldierRifle',gun==='minigun'?.30:.5);
 }
 function unitPose(u){const fresh=TD.Contra34?.frontPose(u);if(fresh)return fresh;const modern=TD.Pixel25?.pose(u);if(modern)return modern;const state=u.dead?'death':u.phase==='vault'?'vault':u.duck>.05?'crouch':u.firing>0||u.warn>0?'fire':['enter','rush'].includes(u.phase)||Math.abs(u.velocity)>9?'walk':'idle',bank='pb19_'+u.kind+'_'+state,q=sequences()[bank]||sequences()['pb16_'+u.kind+'_'+state];
  if(!q)return frame('pb19_'+u.kind+'_walk',0);
  let n=u.dead?Math.floor(u.deathT*12):state==='walk'?Math.floor((u.gait||0)*q.frames.length)%q.frames.length:state==='fire'?(u.warn>0&&u.firing<=0?Math.floor((.22-u.warn)/.22*4):Math.floor((u.fireT||0)*(q.fps||12))):state==='crouch'?Math.round(u.duck*(q.frames.length-1)):state==='vault'?Math.floor(clamp(u.vaultT/.84,0,.999)*q.frames.length):0;
  return q.frames[Math.min(q.frames.length-1,Math.max(0,n))];
 }
 function unitScale(u){const k=unitPose(u);return scale(k,FAMILIES[u.kind].scale)*(u.scale/FAMILIES[u.kind].scale)*(k.startsWith('c34_side_')?(u.kind==='heavy'?142/100:125/88):1);}
 function unitDuckOffset(u){if(!u.duck)return 0;const m=assets()[unitPose(u)],q=m?.bounds;if(!q||!u.cover)return u.duck*18;const cover=enemyCoverBody(u.cover,0),lip=cover.y-cover.ry;return clamp(lip+3-(u.y+(q[1]-m.anchor[1])*unitScale(u)),0,56)*u.duck;}
 function unitBody(u){const k=unitPose(u),m=assets()[k],s=unitScale(u),q=m?.hitBounds||m?.bounds;if(!q)return{x:u.x,y:u.y-55,rx:30,ry:52};
  return{x:u.x+((q[0]+q[2])/2-m.anchor[0])*s,y:u.y+unitDuckOffset(u)-(u.lift||0)+((q[1]+q[3])/2-m.anchor[1])*s,rx:Math.max(16,(q[2]-q[0])*s*.43),ry:Math.max(24,(q[3]-q[1])*s*.46)};
 }
 function unitSocket(u){if(TD.PixelLab38?.enabled){const p=TD.PixelLab38.unitSocket(u,unitScale(u),unitDuckOffset(u));if(p)return p;}const m=assets()[unitPose(u)],s=unitScale(u);if(m?.muzzle)return{x:u.x+(m.muzzle[0]-m.anchor[0])*s,y:u.y+unitDuckOffset(u)-(u.lift||0)+(m.muzzle[1]-m.anchor[1])*s};const b=unitBody(u);return{x:b.x,y:b.y+9};}
 function explodeBarrel(G,b){if(b.dead)return;b.dead=true;b.hp=0;b.deathT=0;const c=G.bastion;FX.boom(b.x,b.y-20,125,'gfx_destruction_',6);A.play('expB',.6);TD.Cam.kick(3);
  for(const u of G.units)if(!u.dead&&u.phase!=='queued'){const q=unitBody(u);if(Math.hypot(q.x-b.x,(q.y-(b.y-20))*.72)<126){u.hp-=22;u.flash=.18;if(u.hp<=0){kill(G,u);c.barrelKills++;}}}
  for(const w of c.enemyCover)if(w.hp>0&&Math.hypot(w.x-b.x,w.y-b.y)<140)enemyCoverHit(G,w,24);
  for(const t of c.turrets||[])if(t.hp>0&&Math.hypot(t.x-b.x,t.y-b.y)<152)t.hp=Math.max(0,t.hp-14);
  for(const other of c.barrels)if(other!==b&&!other.dead&&Math.hypot(other.x-b.x,other.y-b.y)<92)explodeBarrel(G,other);
 }
 function damageDoorCore(G,damage){const c=G.bastion,q=c.wallCore;if(!q||q.hp<=0)return false;if(c.turrets.some(t=>t.hp>0)){q.shieldFlash39=.18;A.play('blocked',.25);return false;}q.hp=Math.max(0,q.hp-damage);q.flash=.1;return true;}
 function fireHits(G,s){const c=G.bastion,b=G.boss;s.hit??=new Set();
  for(const e of c.enemyShots)if(!e.dead&&e.kind==='rocket'&&intersects(s,e.x,e.y,17,17)){e.dead=s.dead=true;c.intercepts++;FX.boom(e.x,e.y,55,'gfx_destruction_',6);return;}
  const hits=[];
  for(const u of G.units)if(!u.dead&&u.phase!=='queued'&&!s.hit.has(u)){if(u.duck>.5&&u.cover?.hp>0&&['hide','peek'].includes(u.phase))continue;const q=unitBody(u);if(intersects(s,q.x,q.y,q.rx,q.ry))hits.push({type:'unit',o:u,x:q.x,y:q.y});}
  for(const w of c.enemyCover)if(w.hp>0&&!s.hit.has(w)){const q=enemyCoverBody(w);if(s.ty>=q.y-q.ry-2&&intersects(s,q.x,q.y,q.rx,q.ry))hits.push({type:'cover',o:w,x:q.x,y:q.y});}
  for(const a of c.barrels)if(!a.dead&&!s.hit.has(a)&&intersects(s,a.x,a.y-24,21,29))hits.push({type:'barrel',o:a,x:a.x,y:a.y-24});
  for(const t of c.turrets||[])if(t.hp>0&&!s.hit.has(t)&&intersects(s,t.x,t.y,20,20))hits.push({type:'turret',o:t,x:t.x,y:t.y});
  const q=c.wallCore;if(q&&q.hp>0&&!s.hit.has(q)&&intersects(s,q.x,q.y,20,20))hits.push({type:'core',o:q,x:q.x,y:q.y});
  if(b&&!b.dead&&!s.hit.has(b)){const body=bossBody(b);if(intersects(s,body.x,body.y,body.rx,body.ry))hits.push({type:'boss',o:b,x:body.x,y:body.y});}
  hits.sort((a,b)=>Math.hypot(a.x-s.oldX,a.y-s.oldY)-Math.hypot(b.x-s.oldX,b.y-s.oldY));
  for(const h of hits){const o=h.o;if(s.dead)break;if(s.hit.has(o))continue;let damage=s.damage;if(s.volley){const before=s.volley.hits.get(o)||0;damage=Math.max(0,Math.min(damage,(s.gun==='shotgun'?6:99)-before));s.volley.hits.set(o,before+damage);}s.hit.add(o);
   if(h.type==='boss'){if(coreHit(G,damage))s.dead=true;continue;}
   if(h.type==='cover'){enemyCoverHit(G,o,damage);s.dead=true;continue;}
   if(h.type==='core'){if(!damageDoorCore(G,damage)){s.dead=true;continue;}}else o.hp=Math.max(0,o.hp-damage);if(s.gun==='cryo_lance'&&h.type==='unit')o.freeze39=2.5;o.flash=.10;s.pierce=(s.pierce||1)-1;if(s.pierce<=0)s.dead=true;
   if(o.hp<=0){if(h.type==='unit')kill(G,o);else if(h.type==='barrel')explodeBarrel(G,o);else{FX.boom(o.x,o.y,90,'gfx_destruction_',6);G.score+=h.type==='turret'?700:1000;A.play('expB',.6);}}
  }
 }
 function controls(G,dt){const c=G.bastion,p=G.player,[dx,dy]=I.dir(),quick=I.down('B')&&!dy&&!I.down('retina');
  if(!p.baseVault29&&(I.tap('reload')||I.tap('B')&&dy<0)&&!p.roll&&p.rollCd<=0){p.baseVault29={t:0,from:p.y,to:p.frontCover29?448:360};p.prone=false;p.quickSide=0;p.blindfire=false;A.play('stylishDodge',.5);}
  if(p.baseVault29){const v=p.baseVault29;v.t+=dt;if(I.tap('X'))v.roll=true;const t=clamp(v.t/.72,0,1);p.y=lerp(v.from,v.to,t)-Math.sin(t*Math.PI)*45;p.rise=1;p.moving=false;p.firing=0;if(t===1){p.frontCover29=!p.frontCover29;p.baseVault29=null;p.stance=I.down('cover')?'crouch':'stand';if(v.roll){p.roll=.5;p.rollCd=5;p.rollDir=dx||1;}}return;}
  p.rollCd=Math.max(0,(p.rollCd||0)-dt);const rollWas=p.roll;
  if(p.proneBlend)p.proneBlend.t+=dt;
  if(I.tap('prone')){if(p.roll>0)p.rollProne=!p.rollProne;else{p.prone=!p.prone;p.proneBlend={t:0,to:p.prone?'prone':'stand'};}}
  if(I.tap('X')&&p.roll<=0&&p.rollCd<=0){p.rollFromProne39=!!p.prone;p.rollProne=p.prone||I.down('prone')||I.down('cover');p.prone=false;p.roll=.5;p.rollCd=5;p.rollDir=dx?Math.sign(dx):p.lastRollDir||1;p.lastRollDir=p.rollDir;A.play('stylishDodge',.45);}if(I.tap('up')&&!I.down('retina')&&p.prone){p.prone=false;p.proneBlend={t:0,to:'stand'};}
  if(quick){if(!p.quickSide){c.preQuickCursor={...c.cursor};p.quickSideT=0;const threats=G.units.filter(u=>!u.dead&&unitNear(u)).sort((a,b)=>Math.abs(a.x-p.x)-Math.abs(b.x-p.x));p.quickSide=dx?Math.sign(dx):threats.length?Math.sign(threats[0].x-p.x)||1:p.lastQuickSide||1;p.fireCd=Math.min(0,p.fireCd);}
   if(dx&&Math.sign(dx)!==p.quickSide){p.quickSide=Math.sign(dx);p.quickSideT=0;p.fireCd=0;}p.quickSideT+=dt;p.lastQuickSide=p.quickSide;
   const u=G.units.filter(u=>!u.dead&&unitNear(u)&&Math.sign(u.x-p.x)===p.quickSide).sort((a,b)=>Math.abs(a.x-p.x)-Math.abs(b.x-p.x))[0],target=u?unitBody(u):{x:p.x+p.quickSide*330,y:p.y-66};c.cursor={x:clamp(target.x,24,616),y:clamp(target.y,330,430)};
  }else if(p.quickSide){if(p.prone)p.proneBlend={t:0,to:'prone'};p.quickSide=0;p.quickSideT=0;if(c.preQuickCursor)c.cursor={...c.preQuickCursor};c.preQuickCursor=null;}
  p.peekShotT=Math.max(0,(p.peekShotT||0)-dt);if(I.combatLatch.size)p.peekShotT=0;else if(I.tap('A'))p.peekShotT=.22;const trigger=I.down('A')||p.peekShotT>0;
  const heldCover=I.down('cover')||I.down('C'),free=I.down('retina'),safe=!p.frontCover29&&coverAt(G,p.x)?.hp>0,autoCover=safe&&!trigger&&!free&&p.throwT<=0,low=p.roll>0||!quick&&(heldCover||p.prone||(!free&&dy>0)||autoCover);
  p.stance=quick?'stand':p.prone?'prone':low?'crouch':'stand';p.rise=quick?1:p.rise+clamp((low?0:1)-p.rise,-dt*6,dt*(trigger?8:3.8));p.freeAim=free;p.blindfire=low&&trigger&&p.rise<.3;
  const before=p.x;if(p.roll>0)p.x=clamp(p.x+(p.rollDir||1)*300*dt,50,590);else if(!quick){if(free){c.cursor.x=clamp(c.cursor.x+dx*480*dt,24,616);c.cursor.y=clamp(c.cursor.y+dy*420*dt,78,449);}else p.x=clamp(p.x+dx*(low?112:185)*dt,50,590);
   const pointer=I.pointer,mouse=TD.Contra34?{...TD.Contra34.toWorld(G,pointer.x,pointer.y),active:pointer.active}:pointer;if(mouse.active&&(mouse.x!==c.lastMouse?.x||mouse.y!==c.lastMouse?.y)){c.cursor.x=clamp(mouse.x,24,616);c.cursor.y=clamp(mouse.y,78,449);c.lastMouse={x:mouse.x,y:mouse.y};}
   else if(I.state.aim&&!I.state.directionalFire){c.cursor.x=clamp(c.cursor.x+I.state.aim[0]*480*dt,24,616);c.cursor.y=clamp(c.cursor.y+I.state.aim[1]*420*dt,78,449);}
   else if(!free&&dx)c.cursor.x=clamp(c.cursor.x+(p.x-before),24,616);if(free&&TD.Contra34)TD.Contra34.limitCursor(G,c.cursor);
  }
  p.roll=Math.max(0,p.roll-dt);if(rollWas>0&&p.roll<=0){p.prone=!!p.rollProne;p.rise=p.prone?0:p.rise;}
  p.moving=Math.abs(p.x-before)>.01;p.shotAge=(p.shotAge||0)+dt;p.throwT=Math.max(0,(p.throwT||0)-dt);p.strafe+=(p.x-before)/(low?48:72);if(p.firing>0)p.fireAnimT=(p.fireAnimT||0)+dt;p.firing=Math.max(0,p.firing-dt);p.fireCd=Math.max(-.016,p.fireCd-dt);p.grenadeCd=Math.max(0,p.grenadeCd-dt);aimSector(G);
  if(p.roll<=0&&(trigger||quick)&&(p.rise>.84||p.blindfire)&&p.fireCd<=0){fire(G);p.peekShotT=0;}
  if(p.roll<=0&&I.tap('Y')&&p.smoke>0&&p.grenadeCd<=0){p.smoke--;p.grenadeCd=.8;p.throwT=.6;const target=c.cursor;for(const u of G.units)if(!u.dead&&u.phase!=='queued'){const q=unitBody(u);if(Math.hypot(q.x-target.x,(q.y-target.y)*.65)<190){u.hp-=14;if(u.hp<=0)kill(G,u);}}
   for(const w of c.enemyCover)if(w.hp>0&&Math.hypot(w.x-target.x,w.y-target.y)<190)enemyCoverHit(G,w,22);
   for(const barrel of c.barrels)if(!barrel.dead&&Math.hypot(barrel.x-target.x,barrel.y-target.y)<155)explodeBarrel(G,barrel);
   for(const t of c.turrets||[])if(t.hp>0&&Math.hypot(t.x-target.x,t.y-target.y)<155)t.hp=Math.max(0,t.hp-12);if(c.wallCore&&Math.hypot(c.wallCore.x-target.x,c.wallCore.y-target.y)<155)damageDoorCore(G,12);
   if(G.boss){const q=bossBody(G.boss);if(Math.hypot(q.x-target.x,q.y-target.y)<180)coreHit(G,12);}FX.boom(target.x,target.y,145,'gfx_destruction_',6);A.play('expB',.6);}
 }
 function stepUnit(G,u,dt,enemyDt){u.freeze39=Math.max(0,(u.freeze39||0)-dt);if(u.freeze39>0){dt*=.55;enemyDt*=.55;}if(u.dead){u.deathT+=dt;u.lift=Math.max(0,(u.lift||0)-dt*180);return;}const c=G.bastion,d=FAMILIES[u.kind],oldX=u.x,oldY=u.y;u.age+=dt;u.fireT=(u.fireT||0)+dt;u.flash=Math.max(0,u.flash-dt);u.walk+=dt*8;
  if(TD.Depth35?.frontManeuver(G,u,dt))return;
  if(u.phase==='queued'){u.delay-=dt;if(u.delay>0)return;u.phase='enter';u.enterT=0;}
  if(u.phase==='enter'){u.enterT+=dt;const t=clamp(u.enterT/1.35,0,1),e=t*t*(3-2*t);u.x=lerp(320,u.homeX,e);u.y=lerp(220,u.targetY,e);u.scale=d.scale*lerp(.25,.48,t);if(t===1){u.phase='hide';u.phaseT=0;u.duck=0;}}
  else if(u.phase==='hide'){u.phaseT+=enemyDt;u.duck=clamp(u.duck+dt*6,0,1);u.firing=0;u.burst=0;
   if(u.cover.hp<=0||u.phaseT>1.0+(u.kind==='heavy'?.2:0)){u.phase='peek';u.phaseT=0;u.cd=.45;}}
  else if(u.phase==='peek'){u.phaseT+=enemyDt;u.duck=Math.max(0,u.duck-dt*4);
   const attacking=['wind','burst','down'].includes(u.attack35?.phase);u.moving35=false;
   if(!attacking&&u.duck<.15){const edge=32,goal=u.homeX+edge*u.lateral42,dx=Math.sign(goal-u.x)*Math.min(Math.abs(goal-u.x),34*dt);u.x=clamp(u.x+dx,95,545);u.moving35=Math.abs(dx)>.01;u.roam42+=Math.abs(dx);if(Math.abs(u.x-goal)<1)u.lateral42*=-1;}
   if(u.phaseT>1.65&&u.burst<=0&&(!TD.Depth35||u.attack35?.phase==='wait')){u.cycles++;if(u.canVault&&u.cycles>=1){u.phase='rush';u.duck=0;u.targetY=376;u.burst=0;message(G,'RUSHER / WATCH THE FRONT WALL');}else{u.phase='hide';u.phaseT=0;}}}
  else if(u.phase==='rush'){u.y=Math.min(u.targetY,u.y+dt*(110+c.totalWave*4));u.scale=lerp(d.scale*.68,d.scale,clamp((u.y-338)/38,0,1));if(u.y>=u.targetY){u.phase='vault';u.vaultT=0;u.fromX=u.x;u.toX=u.x<320?100:540;u.burst=0;message(G,'VAULTER / SIDE FIRE');A.play('warn',.5);}}
  else if(u.phase==='vault'){u.vaultT+=dt;const t=clamp(u.vaultT/.84,0,1);u.y=lerp(u.targetY,451,t);u.x=lerp(u.fromX,u.toX,t);u.lift=Math.sin(t*Math.PI)*(assets()[unitPose(u)]?.vaultLiftBaked?40:70);u.burst=0;if(t===1){u.phase='flank';u.lift=0;u.cd=.7;c.vaults++;}}
  u.velocity=Math.hypot(u.x-oldX,u.y-oldY)/dt;u.gait=(u.gait||0)+Math.hypot(u.x-oldX,u.y-oldY)/72;
  if(TD.Depth35){TD.Depth35.frontAttack(G,u,enemyDt,(u.phase==='peek'&&u.duck<.15)||u.phase==='flank',bullet,unitSocket);u.warn=Math.max(0,(u.warn||0)-dt);return;}
  if((u.phase==='peek'&&u.duck<.15)||u.phase==='flank'){u.cd-=enemyDt;
   if(u.cd<=0&&u.burst<=0){u.cd=d.cd/(1+(c.totalWave-1)*.04);u.burst=u.kind==='heavy'?4:u.kind==='rifle'?2:1;u.burstCd=.22;u.warn=.22;}
   if(u.burst>0&&(u.burstCd-=dt)<=0){const q=sequences()['px25_'+u.kind+'_fire_south']||sequences()[u.elite?'pb17_elite_fire':'pb16_'+u.kind+'_fire'];if(u.firing<=0)u.fireT=TD.Contra34?0:4/(q?.fps||12);const newClip=TD.Contra34?.clip('front',TD.Contra34.role(u),'fire_forward');u.firing=newClip?newClip.frames.length/newClip.fps:q?(q.frames.length-4)/(q.fps||12):.19;const m=unitSocket(u);bullet(G,m.x,m.y,u.kind==='rocket'?'rocket':u.kind==='laser'?'laser':'mg',0,u.phase==='flank');u.burst--;u.burstCd=.16;A.play(u.kind==='rocket'?'missileLaunch':'gd_soldierRifle',.35);}}
  u.warn=Math.max(0,(u.warn||0)-dt);u.firing=Math.max(0,(u.firing||0)-dt);
 }
 function resolveEnemyShot(G,e){if(e.visualOnly)return;const c=G.bastion,p=G.player,dodges=(p.prone&&!p.quickSide&&!e.hitsProne)||(p.roll>.08&&p.roll<.42);const nearPlayer=Math.abs(e.tx-p.x)<(e.kind==='rocket'?45:23),covered=!p.frontCover29&&p.rise<.35&&!e.near&&coverAt(G,p.x)?.hp>0;
  if(!e.near&&(!nearPlayer||covered)){const blocked=damageCover(G,e.tx,e.kind==='rocket'?11:e.kind==='laser'?3:e.kind==='orb'?4:1.5);if(blocked){c.coverStops++;FX.boom(e.tx,389,26,'gfx_impact_',6);A.play('impactMetal',.18);}else if(nearPlayer&&!dodges)harm(G,e.damage);}
  else if(nearPlayer&&!dodges)harm(G,e.damage);
  if(e.kind==='rocket')FX.boom(e.tx,399,65,'gfx_destruction_',6);
 }
 function beginBreach(G){const c=G.bastion,p=G.player;c.phase='breach';c.transition={phase:'blast',t:0,fromX:p.x,fromY:p.y,fx:0};c.t=0;c.clearedWaves++;c.enemyShots=[];c.bullets=[];c.shotEchoes=[];c.hazards=[];p.peekShotT=0;p.quickSide=0;p.blindfire=false;p.moving=false;p.rise=1;p.hp=Math.min(p.max,p.hp+1);p.smoke=Math.min(5,p.smoke+1);c.transitionLog.push({wave:c.totalWave,phase:'blast'});message(G,'LINE SECURED / REAR WALL BREACH');A.play('expBoss',.55);}
 function breachStep(G,dt){const c=G.bastion,tr=c.transition;tr.t+=dt;const lengths={blast:1,hop:.75,walk:1.65,black:.5,emerge:.7};
  if(tr.phase==='blast'){if(tr.fx<8&&tr.t>tr.fx*.095){FX.boom(150+tr.fx%4*113,122+Math.floor(tr.fx/4)*98,100,'gfx_destruction_',6);tr.fx++;TD.Cam.kick(3);}c.flash=Math.max(0,.6-tr.t*3);}
  if(tr.t<lengths[tr.phase])return;const next={blast:'hop',hop:'walk',walk:'black',black:'emerge',emerge:'done'}[tr.phase];tr.phase=next;tr.t=0;c.transitionLog.push({wave:c.totalWave,phase:next});
  if(next==='walk'){G.units=[];c.barrels=[];c.enemyCover=[];c.turrets=[];c.wallCore=null;FX.list=[];}
  if(next==='emerge'){c.skin=Math.floor(c.totalWave/2)%3;freshCover(G);c.coverPrepared=true;message(G,c.totalWave===4?'FOUR LINES BREACHED / PRISM CONTAINMENT REACTOR':'ADVANCE / FRESH COVER');}
  if(next==='done'){Object.assign(G.player,{x:320,y:448,frontCover29:false,baseVault29:null,prone:false,quickSide:0,aimSector:2});c.cursor={x:320,y:175};c.transition=null;wave(G);}
 }
 function transitionView(G){const c=G.bastion,tr=c.transition;if(!tr)return{x:G.player.x,y:G.player.y,s:1,zoom:1,wallY:454,wallScale:1,backState:0,black:0};const q={blast:1,hop:.75,walk:1.65,black:.5,emerge:.7},t=clamp(tr.t/q[tr.phase],0,1),e=t*t*(3-2*t),base={x:320,y:448,s:1,zoom:1,wallY:454,wallScale:1,backState:7,black:0};
  if(tr.phase==='blast')return{...base,x:tr.fromX,backState:Math.min(7,Math.floor(t*9))};
  if(tr.phase==='hop')return{...base,x:lerp(tr.fromX,320,e),y:lerp(448,358,e)-Math.sin(t*Math.PI)*26};
  if(tr.phase==='walk'){const cameraDepth=3.8*e,depth=1.43-cameraDepth,wallScale=depth>.14?1.43/depth:0;return{...base,y:lerp(358,310,e),s:lerp(1,.80,e),zoom:4.8/(4.8-cameraDepth),wallY:190+264*wallScale,wallScale,black:clamp((t-.65)/.35,0,1)};}
  if(tr.phase==='black')return{...base,zoom:4.8,wallScale:0,black:1};
  return{...base,backState:0,black:1-e};
 }
 function step(G,dt){const c=G.bastion,p=G.player,enemyDt=dt*TD.DIFFICULTIES[TD.difficulty||'normal'].tempo;c.age+=dt;c.t+=dt;G.time+=dt;p.inv=Math.max(0,p.inv-dt);p.reviveT=Math.max(0,(p.reviveT||0)-dt);p.flash=Math.max(0,(p.flash||0)-dt);TD.Cam.x=TD.Cam.y=0;TD.Cam.zoom=1;FX.update(dt);TD.Cam.shake*=.86;
  for(const m of G.msgs)m.t+=dt;G.msgs=G.msgs.filter(m=>m.t<2.6);for(const w of [...c.cover,...c.enemyCover])w.flash=Math.max(0,w.flash-dt);stepPickups(G,dt);for(const b of c.barrels){b.flash=Math.max(0,b.flash-dt);if(b.dead)b.deathT+=dt;}
  if(p.dead){p.deadT+=dt;if(p.deadT>2){G.lives--;if(G.lives<0){G.state='gameover';G.stateT=0;A.stopMusic();return;}
    const keep={deaths:G.deaths,score:G.score,lives:G.lives,time:G.time},room=c.room,totalWave=c.totalWave,form=G.boss?.form,stats={coverStops:c.coverStops,intercepts:c.intercepts,damage:c.damage,entryLog:c.entryLog,coreLog:c.coreLog,age:c.age,clearedWaves:c.clearedWaves,barrelKills:c.barrelKills,vaults:c.vaults,brokenWalls:c.brokenWalls,wallDamage:c.wallDamage,pickupLog:c.pickupLog,transitionLog:c.transitionLog,gunShots:c.gunShots,quickShots:c.quickShots};
    setup(G);Object.assign(G,keep);Object.assign(G.bastion,stats,{room,totalWave:Math.max(0,totalWave-1)});G.player.inv=2;G.player.reviveT=1;
    if(form){startBoss(G);if(form==='helios'){Object.assign(G.boss,{name:'HELIOS / PRISM ENTITY',form:'helios',hp:360,max:360,y:320,pattern:0});G.bastion.turrets=[];G.bastion.coreRays=[];}}
    message(G,form?'REGROUP / FINAL CORE':'REGROUP / DEFENSE LINE '+Math.max(1,totalWave));}return;}
  if(c.phase==='breach'){for(const u of G.units)if(u.dead)u.deathT+=dt;G.units=G.units.filter(u=>!u.dead||u.deathT<1.4);breachStep(G,dt);A.scene(G,dt);return;}
  if(!p.reviveT&&!['transform','reveal'].includes(G.boss?.state))controls(G,dt);
  if(c.phase==='advance'&&c.t>1.55)enterRoom(G);
  if(c.phase==='fight'&&c.wallCore?.hp<=0&&(c.turrets||[]).every(t=>t.hp<=0)){beginBreach(G);return;}
  for(const u of G.units)stepUnit(G,u,dt,enemyDt);G.units=G.units.filter(u=>!u.dead||u.deathT<1.4);
  for(const t of c.turrets||[])if(t.hp>0&&!['transform','reveal'].includes(G.boss?.state)){if(TD.PixelLab38?.stepTurret?.(G,t,dt,enemyDt,bullet))continue;t.age+=dt;if(t.attackT!=null)t.attackT+=dt;t.flash=Math.max(0,t.flash-dt);t.cd-=enemyDt;if(t.cd<=0){t.attackT=0;bullet(G,t.x,t.y,t.kind==='laser'?'laser':'mg');t.cd=t.kind==='laser'?3.5:2.7;}}
  if(c.wallCore){c.wallCore.age+=dt;c.wallCore.flash=Math.max(0,c.wallCore.flash-dt);c.wallCore.shieldFlash39=Math.max(0,(c.wallCore.shieldFlash39||0)-dt);}
  bossStep(G,['enter','transform','reveal'].includes(G.boss?.state)?dt:enemyDt);
  c.shotEchoes??=[];for(const echo of c.shotEchoes)echo.age+=dt;c.shotEchoes=c.shotEchoes.filter(e=>e.age<.075);for(const s of c.bullets){s.oldX=s.x;s.oldY=s.y;s.t+=dt;const t=clamp(s.t/s.duration,0,1);s.x=lerp(s.sx,s.tx,t);s.y=lerp(s.sy,s.ty,t);fireHits(G,s);if(t>=1)s.dead=true;if(s.dead)c.shotEchoes.push({...s,age:0});}c.bullets=c.bullets.filter(s=>!s.dead);
  for(const e of c.enemyShots){if(e.dead)continue;e.t+=dt;if(e.t<0)continue;const t=clamp(e.t/e.duration,0,1);e.x=lerp(e.sx,e.tx,t);e.y=lerp(e.sy,e.ty,t);if(t>=1){e.dead=true;resolveEnemyShot(G,e);}}c.enemyShots=c.enemyShots.filter(e=>!e.dead);
  for(const h of c.hazards){h.t+=dt;if(h.t>h.delay&&h.t<h.delay+h.duration&&Math.abs(p.x-h.x)<(h.kind==='geyser'?68:73)){
   if(h.kind==='geyser'||p.rise>.35||!coverAt(G,p.x)?.hp)harm(G,1);else if(!h.hit){h.hit=true;damageCover(G,p.x,8);c.coverStops++;}}
   if(h.t>h.delay+h.duration)h.dead=true;}c.hazards=c.hazards.filter(h=>!h.dead);
  if(c.phase==='victory'){c.clearT+=dt;if(c.clearT>3)return'clear';}A.scene(G,dt);
 }
 function heliosPose(b){if(TD.Contra34)return TD.Contra34.heliosPose(b);let action='idle',phase=0,flip=false;const c=TD.game?.bastion;
  if(b.dead){action='death';phase=Math.min(7,Math.floor((c?.clearT||0)*10));}
  else if(b.state==='run'||b.state==='return'){action=b.state==='run'?'run':'walk';phase=Math.floor((b.gait||0)*(sequences()['pb19_helios_'+action]?.frames.length||8))%(sequences()['pb19_helios_'+action]?.frames.length||8);flip=b.toX<b.x;}
  else if(b.state==='volley'){action='throw';phase=Math.floor((b.t%.96)/.96*(sequences().pb19_helios_throw?.frames.length||16));}
  else if(b.state==='lightning'){action='lightning';phase=b.t<.75?Math.min(4,Math.floor(b.t/.75*5)):b.t<2.1?5:Math.min(7,6+Math.floor((b.t-2.1)*3));}
  else if(b.state==='jump'){action='jump';phase=b.t<.22?Math.floor(b.t/.22*4):b.t<.9?4+Math.floor((b.t-.22)/.68*7):Math.min(15,11+Math.floor((b.t-.9)/.25*5));}
  else if(b.state==='recover'&&b.t<.65&&b.hitAge>=.32){action='strafe';phase=Math.floor((b.sideGait||0)*8)%8;flip=b.pattern%2===1;}
  else if(b.state==='recover'&&b.hitAge<.32){action='hit';phase=Math.min(7,Math.floor(b.hitAge/.32*8));}
  else phase=Math.floor((c?.age||0)*8)%8;
  return{key:frame('pb19_helios_'+action,phase)||frame('pb16_helios_throw',0),flip,action};
 }
 function masterPose(b){return frame('pb18_master',b.state==='transform'?12+Math.min(3,Math.floor(b.t/.9*4)):b.hp/b.max<.75?8+Math.min(3,Math.floor((1-b.hp/b.max)*4)):Math.floor(b.phaseT*8)%8);}

 function bossBody(b){if(b.form==='core'){const k=masterPose(b),m=assets()[k],q=m.bounds,s=scale(k,.52);return{x:b.x+((q[0]+q[2])/2-m.anchor[0])*s,y:b.y+((q[1]+q[3])/2-m.anchor[1])*s,rx:(q[2]-q[0])*s*.45,ry:(q[3]-q[1])*s*.46};}
  const pose=heliosPose(b),m=assets()[pose.key],q=m.bounds,s=scale(pose.key,.85);
  return{x:b.x+((q[0]+q[2])/2-m.anchor[0])*s*(pose.flip?-1:1),y:b.y-(b.jumpZ||0)+((q[1]+q[3])/2-m.anchor[1])*s,rx:(q[2]-q[0])*s*.43,ry:(q[3]-q[1])*s*.48};
 }
 function bossDraw(ctx,G){TD.Grid21?.flush(ctx);const b=G.boss;if(!b)return;const c=G.bastion;
  if(b.form==='core'){const k=masterPose(b);draw(ctx,k,b.x,b.y,1,{flash:b.flash>0?.6:0});return;}
  const pose=heliosPose(b),charge=['volley','lightning','jump'].includes(b.state),pulse=.7+.3*Math.sin(c.age*9);ctx.save();ctx.globalCompositeOperation='screen';const glow=ctx.createRadialGradient(b.x,b.y-75,8,b.x,b.y-75,180);glow.addColorStop(0,'rgba(255,190,65,'+(charge?.23:.13)*pulse+')');glow.addColorStop(.55,'rgba(174,61,225,'+(charge?.10:.05)*pulse+')');glow.addColorStop(1,'rgba(255,70,12,0)');ctx.fillStyle=glow;ctx.fillRect(b.x-180,b.y-255,360,360);ctx.restore();ctx.save();ctx.shadowColor=charge?'#ffbd5b':'#ff7438';ctx.shadowBlur=charge?20:12;ctx.translate(b.x,b.y-(b.jumpZ||0));if(pose.flip)ctx.scale(-1,1);draw(ctx,pose.key,0,0,scale(pose.key,.85),{flash:b.flash>0?.7:0,alpha:b.dead?Math.max(0,1-G.bastion.clearT/2):1});ctx.restore();
 }
 function playerDraw(ctx,G,x=G.player.x,y=G.player.y,s){const p=G.player;draw(ctx,playerPose(G),x,y+playerCoverOffset(G),s??playerScale(G),{flash:p.flash>0?1:0,alpha:p.inv>0&&Math.floor(G.t/5)%2?.65:1});}
 function unitNear(u){return u.phase==='flank'||u.phase==='vault'&&u.vaultT>=.36;}
 function unitDraw(ctx,u){if(u.phase==='queued'||TD.Contra34&&u.dead&&u.deathT>.12)return;TD.Combat39?.baseWarning(ctx,u);ctx.save();if(u.cover&&['hide','peek'].includes(u.phase)){const w=enemyCoverBody(u.cover,0);if(TD.Grid21?.active)TD.Grid21.clipBottom=w.y+w.ry;ctx.beginPath();ctx.rect(0,0,640,w.y+w.ry);ctx.clip();}draw(ctx,unitPose(u),u.x,u.y+unitDuckOffset(u)-(u.lift||0),unitScale(u),{flash:u.flash>0?1:0,alpha:u.dead?Math.max(0,Math.min(1,(1.4-u.deathT)/.5)):1});TD.PixelLab38?.drawUnitMuzzle?.(ctx,u,unitScale(u),unitDuckOffset(u));ctx.restore();if(TD.Grid21)TD.Grid21.clipBottom=480;}
 function drawWorld(ctx,G){const outputCtx=ctx,c=G.bastion,p=G.player,v=transitionView(G),plate=ART.get('pb18_room');if(!c)return;
  ctx.save();ctx.imageSmoothingEnabled=false;if(TD.Cam.shake>.3)ctx.translate(Math.sin(G.t*1.7)*TD.Cam.shake,0);
  const grid=TD.Grid21?.begin(ctx,G);if(grid)ctx=TD.Grid21.layerContext;ctx.save();ctx.translate(320,190);ctx.scale(v.zoom,v.zoom);ctx.translate(-320,-190);
  if(!grid&&plate)ctx.drawImage(plate.im,plate.sx,plate.sy,plate.sw,plate.sh,0,0,640,480);
  const rear=key('pb18_backwall_'+v.backState,null);if(!grid&&rear)draw(ctx,rear,320,264,1);else if(!grid){const door=key('pb16_door_'+(c.phase==='breach'?3:0),null);if(door)draw(ctx,door,320,215,scale(door,.6));}
  if(c.phase==='breach'&&c.transition.phase==='blast'){const explosion=frame('pb17_blast',Math.min(7,Math.floor(c.transition.t*8)));if(explosion)draw(ctx,explosion,320,177,scale(explosion,1)*1.05,{alpha:Math.min(1,(1-c.transition.t)*3)});}
  for(const t of c.turrets||[]){TD.PixelLab38?.drawTurretWarning?.(ctx,t,G);const firing=t.attackT!=null&&t.attackT<.30;
   const pose=t.kind==='laser'?(firing?(t.attackT<.15?2:3):t.cd<.55?1:0):(firing?Math.min(3,1+Math.floor(t.attackT*10)):0);
   const k=TD.Contra34?.turretPose(t)||frame('pb18_turret_'+t.kind,pose)||key('pb16_turret_'+(t.kind==='laser'?(firing?3:2):(firing?1:0)),'pb_turret_'+(t.kind==='laser'?(firing?3:2):(firing?1:0)));
   draw(ctx,k,t.x,t.y,scale(k,.27),{flash:t.flash>0?1:0,alpha:(t.hp>0?1:.25)*(c.phase==='breach'?(c.transition.phase==='blast'?clamp(1-c.transition.t*1.6,0,1):0):1)});TD.PixelLab38?.drawTurretMuzzle?.(ctx,t);}
  const q=c.wallCore;if(q){const k=(q.hp>0||TD.PixelLab38?.enabled)&&TD.Contra34?TD.Contra34.corePose(c,q):frame('pb18_door_core',q.hp<=0?7:Math.floor(c.age*10)%7);draw(ctx,k,q.x,q.y,scale(k,1),{flash:q.flash>0?1:0,alpha:(q.hp>0?1:.2)*(c.phase==='breach'?(c.transition.phase==='blast'?clamp(1-c.transition.t*1.6,0,1):0):1)});TD.Combat39?.coreShield(ctx,c,q);}
  const far=[];for(const b of c.barrels)far.push({y:b.y,b});for(const w of c.enemyCover)far.push({y:w.y,w});for(const u of G.units)if(!unitNear(u))far.push({y:u.y,u});
  for(const o of far.sort((a,b)=>a.y-b.y)){if(o.u)unitDraw(ctx,o.u);else if(o.w){const w=o.w,k=frame(w.kind==='crate'?'pb18_enemy_crate':w.kind==='armored'?'pb18_armored_crate':'pb17_enemy_cover_wall',wallPhase(w))||key('pb16_wall_'+wallPhase(w),null);draw(ctx,k,w.x,w.y,k?.startsWith('grid21_')||k?.startsWith('pb18_')||k?.startsWith('pb17_')?scale(k,1)*.9:.45,{flash:w.flash>0?1:0});}else{const b=o.b,k=frame(b.dead&&b.deathT<.35?'pb18_barrel_blast':'pb18_barrel',b.dead&&b.deathT<.35?Math.floor(b.deathT/.35*4):b.dead?3:b.hp<=2?2:b.hp<=4?1:0);draw(ctx,k,b.x,b.y,scale(k,.25),{flash:b.flash>0?1:0,alpha:b.dead?.65:1});}}
  bossDraw(ctx,G);TD.Grid21?.flush(ctx);FX.draw(ctx,0);ctx.restore();
  for(const ray of c.coreRays||[]){const k=animated('pb18_laser_ray',c.age,null),b=G.boss;if(k&&b?.form==='core'){const m=assets()[k],length=(m.bounds[2]-m.bounds[0])*1.2;ctx.save();ctx.translate(b.x,b.y);ctx.rotate(ray.angle);draw(ctx,k,length/2,0,1.2,{alpha:ray.active?.88:.20});ctx.restore();}}
  for(const h of c.hazards){if(h.t<h.delay)draw(ctx,animated('pb19_warning',h.t,null),h.x,407,.9,{alpha:.55+.3*Math.sin(h.t*24)**2});
   else if(h.kind==='geyser'){const k=animated('pb19_geyser',h.t-h.delay,frame('pb_geyser',Math.floor((h.t-h.delay)*12)%6));draw(ctx,k,h.x,442,k.startsWith('pb16_')?scale(k,1)*1.2:.95);}
   else{const k=animated('pb19_lightning',c.age,frame('pb_lightning',Math.floor(c.age*15)%6)),modern=k.startsWith('pb16_');ctx.save();ctx.translate(h.x,170);ctx.rotate(Math.PI/2);draw(ctx,k,modern?120:70,0,modern?scale(k,1)*2:1.35);ctx.restore();}}
  TD.Grid21?.flush(ctx);
  const drawEnemyShot=e=>{if(e.t<0)return;if(TD.Contra34?.frontShot(ctx,e))return;const growth=.12+clamp(e.t/e.duration,0,1)*.19,k=animated('pb16_projectile_'+e.kind,c.age,null);
   if(k&&e.kind!=='orb'){if(TD.Lighting22)TD.Lighting22.enemyShot(ctx,e,k,scale(k,1)*(e.near?1.35:.85+clamp(e.t/e.duration,0,1)*.72));else draw(ctx,k,e.x,e.y,scale(k,1));}
   else if(e.kind==='orb'){const k=animated('pb19_orb',c.age,frame('pb_orb',Math.floor(c.age*12)%6));art.draw(ctx,k,e.x,e.y,{s:k.startsWith('pb19_')?(.8+clamp(e.t/e.duration,0,1)*.8):growth*2.5});}
   else {TD.drawShot(ctx,{k:e.kind==='rocket'?'missile':e.kind==='laser'?'laser':'mg',x:e.x,y:e.y,a:M.angTo(e.sx,e.sy,e.tx,e.ty),lv:1,t:c.age*60,r:4},true);}};
  for(const e of c.enemyShots)if(!e.near)drawEnemyShot(e);
  // The barrier is between the enemy doorway and Yuri. His rear-view
  // sprite stays on the CAMERA side, where we can see him crouch against it.
  const crossed=p.frontCover29||p.baseVault29&&p.baseVault29.t>.36||c.phase==='breach'&&(c.transition.phase==='walk'||c.transition.phase==='black'||c.transition.phase==='hop'&&c.transition.t>.38);
  if(crossed)playerDraw(ctx,G,v.x,v.y,playerScale(G)*v.s);
  if(!TD.Grid21?.cover(ctx,G)&&v.wallScale>0)for(const w of c.cover){const k=frame('pb19_cover',w.hp<=0?7:Math.min(6,Math.floor((1-w.hp/w.max)*7)));draw(ctx,k,320+(w.x-320)*v.wallScale,v.wallY,v.wallScale,{flash:w.flash>0?.65:0});}
  if(!crossed)playerDraw(ctx,G,v.x,v.y,playerScale(G)*v.s);
  for(const u of G.units)if(unitNear(u)&&u.y<=p.y)unitDraw(ctx,u);
  TD.Grid21?.flush(ctx);for(const e of c.enemyShots)if(e.near)drawEnemyShot(e);
  for(const u of G.units)if(unitNear(u)&&u.y>p.y)unitDraw(ctx,u);TD.Grid21?.flush(ctx);for(const s of c.shotEchoes||[])TD.Lighting22?.playerShot(ctx,s,Math.max(0,1-s.age/.075));for(const s of c.bullets)TD.Lighting22?.playerShot(ctx,s);FX.draw(ctx,1);
  for(const q of c.pickups){const k=q.gun==='flamethrower'?'od39_flame_pickup':q.gun==='cryo_lance'?'od39_cryo_pickup':animated('pb17_pickup_'+q.gun,c.age,key('gp_ammo_crate_intact',null));draw(ctx,k,q.x,q.y,scale(k,.22));}
  if(c.phase!=='breach'&&c.phase!=='advance'){const aim=c.cursor,ret=animated('pb16_reticle',c.age,key('pb16_reticle',null));if(ret)draw(ctx,ret,aim.x,aim.y,scale(ret,1));else ART.draw(ctx,'retm_'+(Math.floor(c.age*10)%4),aim.x,aim.y,{s:.13,palette:TD.PILOT_INFO[p.pilot]?.[0]||'#ff9440'});}
  TD.Grid21?.end(ctx);if(grid)ctx=outputCtx;if(c.phase==='advance'){const fade=Math.sin(clamp(c.t/1.55,0,1)*Math.PI)*.32;ctx.fillStyle='rgba(3,10,20,'+fade+')';ctx.fillRect(0,32,640,416);}
  if(v.black>0){ctx.fillStyle='rgba(0,0,0,'+v.black+')';ctx.fillRect(0,0,640,480);}
  if(c.flash>0){ctx.fillStyle='rgba(255,255,255,'+c.flash+')';ctx.fillRect(0,0,640,480);}ctx.restore();
 }
 function bossBar(ctx,text,b,c){const x=132,y=50,w=376;
  ctx.fillStyle='rgba(5,8,16,.92)';ctx.fillRect(x-8,y-19,w+16,39);text(b.name,320,y-10,10,'#ffe197','center');ctx.fillStyle='#39252a';ctx.fillRect(x,y,w,13);
  if(b.form==='core'){ctx.fillStyle='#ffad32';ctx.fillRect(x+2,y+2,(w-4)*(b.state==='enter'?clamp(b.t/1.3,0,1):b.hp/b.max),9);}
  else{const orange=b.state==='enter'?clamp(b.t/1.3,0,1):clamp(b.hp/180,0,1),red=b.state==='enter'?clamp((b.t-1.3)/1.3,0,1):clamp((b.hp-180)/180,0,1);ctx.fillStyle='#ffa32b';ctx.fillRect(x+2,y+2,(w-4)*orange,9);ctx.fillStyle='#ff392b';ctx.fillRect(x+2,y+2,(w-4)*red,9);ctx.save();ctx.beginPath();ctx.rect(x+2,y+2,(w-4)*red,9);ctx.clip();for(let i=0;i<14;i++){ctx.fillStyle=i%2?'#ff7840':'#ffbd50';ctx.fillRect(x+((i*31+c.age*90)%w),y+2,7,3+Math.sin(c.age*11+i)*2);}ctx.restore();}
 }
 function hud(ctx,text,G){const c=G.bastion,p=G.player;if(TD.ground20HUD){if(c.flash>.92||transitionView(G).black>.95)return true;TD.ground20HUD(ctx,text,G,true);for(const m of G.msgs)text(m.text,320,G.boss?154:106,10,'#ffe8a7','center');return true;}if(c.flash>.92||transitionView(G).black>.95)return true;ctx.fillStyle='rgba(3,8,15,.88)';ctx.fillRect(0,0,640,32);text('PRISM BASTION',12,15,12,'#ffd477');text(GUNS[p.groundGun||'rifle'].name+(p.groundGun!=='rifle'?' '+p.gunAmmo:''),320,15,9,'#82f3dc','center');text('ARMOR '+Math.ceil(p.hp)+'/'+p.max+' / LIVES '+G.lives,625,15,10,'#b5ffe0','right');
  if(G.boss&&!G.boss.dead&&G.boss.state!=='reveal')bossBar(ctx,text,G.boss,c);else text('DEFENSE LINE '+Math.max(1,c.totalWave)+' / 4  '+'TURRETS FIRST / THEN CORE',320,48,11,'#b7e7ff','center');
  const w=coverAt(G,p.x),safe=w?.hp>0,label=c.phase==='breach'?'ADVANCING':p.quickSide?'QUICK SIDE FIRE':p.dead?'DOWN':p.reviveT>0?'RECOVERING':p.blindfire?'BLINDFIRE':p.freeAim?'RETINA FREE AIM':p.rise<.35?(safe?'IN COVER':'COVER BREACHED'):'EXPOSED';
  text(label,14,456,10,p.rise<.35&&safe?'#8fffa7':'#ffd270');text('GRENADES '+p.smoke,625,456,10,'#d2ebff','right');
  for(const wall of c.cover){ctx.fillStyle='#342c35';ctx.fillRect(260+wall.index*31,452,25,5);ctx.fillStyle=wall.hp>wall.max*.34?'#70cab5':'#ff654d';ctx.fillRect(260+wall.index*31,452,25*(wall.hp/wall.max),5);}
  const hints=I.padStyle()==='six'?[['pad_dpad','MOVE'],['pad_c','COVER'],['pad_a','FIRE'],['pad_z','RETINA'],['pad_b','SIDE FIRE'],['pad_y','GRENADE']]:[['pad_dpad','MOVE'],['pad_l','COVER'],['pad_a','FIRE'],['pad_b','SIDE FIRE'],['pad_y','GRENADE'],['pad_start','PAUSE']];
  hints.forEach(([k,label],i)=>{const x=22+i*104,g=ART.get(k);if(g)ART.draw(ctx,k,x,474,{s:Math.min(19/g.sw,14/g.sh)});text(label,x+14,477,8,'#a0becb');});
  for(const m of G.msgs)text(m.text,320,89,11,'#ffe8a7','center');if(p.dead)text(G.lives>0?'REGROUPING':'LAST STAND',320,235,20,'#ff866e','center');return true;
 }
 TD.Bastion={GUNS,damageDoorCore,setup,step,spawn,wave,startBoss,coreHit,harm,intersects,frame,draw:drawWorld,playerDraw,playerPose,playerSocket,playerCoverOffset,bossBody,coverAt,damageCover,wallPhase,freshCover,explodeBarrel,unitBody,unitPose,unitSocket,unitScale,fireHits,resolveEnemyShot,enemyCoverBody,enemyCoverHit,unitDuckOffset,launchPickup,stepPickups,beginBreach,transitionView,heliosPose,masterPose,fire,kill};
 TD.MISSIONS.push({id:7,mode:'foot',view640:true,pseudo3D:true,map:{key:'pb_stage',w:640,h:480,rects:[]},data:{title:'LEVEL 7',name:'PRISM BASTION',brief:['FOUR WAVES. DESTROY TURRETS, THEN THE SHIELDED DOOR CORE.','AUTO COVER. FIRE TO PEEK; HOLD COVER + FIRE TO BLINDFIRE.','HOLD RETINA + D-PAD TO AIM. B + LEFT/RIGHT FIRES TO YOUR SIDES.','HOP COVER, WALK THROUGH THE BLACK PASSAGE, DEFEAT HELIOS.'],start:{x:320,y:448,a:Math.PI},checkpoints:[],gates:[],bossLine:-1000,boss:{x:320,y:194},units:[],props:[],structures:[]},boss:null,setup,exclusiveStep:step,drawWorld,hud,briefSprite:(ctx,G,x,y)=>playerDraw(ctx,G,x,y+32,playerScale(G)*.60),keys:()=>[['dpad','SIDESTEP'],['a','FIRE'],['c','COVER'],['z','RETINA'],['b','SIDE FIRE'],['start','PAUSE']],score(G,R){R.extraRows=[['COVER BLOCKS',G.bastion.coverStops],['ROCKETS STOPPED',G.bastion.intercepts]];}});
})(window);
