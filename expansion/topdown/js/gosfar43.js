/* Dead Signal: Hotwire's hack, the elevator reveal, and a whole-plate minigun boss.
 * One owner advances the cinematic; ordinary combat retains damage/respawn rules. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,W=TD.World,A=TD.Audio,FX=TD.FX,art=TD.AssaultArt,P=root.TD_GOSFAR43_ART;
 const mission=TD.MISSIONS.find(m=>m.id===3),api=TD.Gosfar43={build:'overdrive1018-gosfar44-r4'};
 const clip=(name,t=0,loop=true)=>{const q=P.banks[name];return q?.frames[loop?Math.floor(Math.max(0,t)*q.fps)%q.frames.length:Math.min(q.frames.length-1,Math.floor(Math.max(0,t)*q.fps))];};
 const plate=(ctx,name,t,x,y,o={})=>art.draw(ctx,clip(name,t,o.loop!==false),x,y,{s:1,...o});
 const segments=[188,276,364,452,540,628];
 // Tall authored modules share one baseline and meet edge-to-edge. Their
 // visual height is independent of the shallow physical wall footprint.
 const coverPose43=TD.Depth35.coverPose,drawCover43=TD.Depth35.drawCover;
 TD.Depth35.coverPose=function(s){if(!s.gosfarWall43)return coverPose43(s);const phase=s.dead?3:!Number.isFinite(s.max)?0:s.hp/s.max<.34?2:s.hp/s.max<.7?1:0;return {key:P.banks.wall.frames[phase],s:1};};
 TD.Depth35.drawCover=function(ctx,s){if(!s.gosfarWall43)return drawCover43(ctx,s);const z=TD.Depth35.coverPose(s);ctx.save();ctx.beginPath();ctx.rect(s.x-44,s.y-116,88,144);ctx.clip();art.draw(ctx,z.key,s.x,s.y+s.type.hh,{s:1,flash:Math.min(.52,(s.flash||0)*5)});ctx.restore();return true;};
 mission.data.structures=mission.data.structures.filter(s=>s.y>560||s.kind==='od_gate36');
 for(const x of segments)mission.data.structures.push({kind:'od_barrier',x,y:365,visual36:'lowwall',dim36:{hw:44,hh:16,hp:x===188?Infinity:150,indestructible:x===188,cover:true},gosfarWall43:true,permanent43:x===188});
 mission.data.brief=['DESTROY THREE RED RELAYS TO DROP THE SECURITY WALL.','MEET HOTWIRE AT THE NORTH FREIGHT ELEVATOR.','STAY IN COVER WHILE SHE HACKS THE TERMINAL.','DEFEAT GOSFAR, THEN ESCAPE TOGETHER IN THE ELEVATOR.'];
 const setup=mission.setup;mission.setup=function(G,...args){setup(G,...args);G.gosfar43=null;};
 const respawn=mission.respawn;mission.respawn=function(G,old,fresh){respawn?.(G,old,fresh);if(G.gosfar43?.phase==='combat'){fresh.x=530;fresh.y=475;G.eshots=[];G.boss.state='recover';G.boss.actionT=0;}};
 const durations={hack:4.5,alarm:6.5,opening:1.9,entrance:2.7,taunt:4.8,plan:5.8,spotted:1.9,bar:1.8,rev:2.2,barrage:9.5,notice:2.4,rally:2.2,victory:2.3,exit:6,close:1.5,fade:1.2};
 const words={hack:['HOTWIRE','Give me a second. I can bring the elevator down.'],alarm:['YURI','That alarm is getting louder. Hotwire... get away from it!'],opening:['HOTWIRE','Someone called it from upstairs. Yuri, get behind that wall!'],taunt:['GOSFAR','*sniff sniff* Do I smell some intruders?','Come out whenever you\'re ready to play.'],plan:['YURI / HOTWIRE','What the fuck are we gonna do?','Do you have any ideas?'],spotted:['GOSFAR','Ahh! There you are!'],bar:['YURI / HOTWIRE','FUUUUCK!!!'],barrage:['HOTWIRE / YURI','This is NOT what we expected!','Keep your head down!'],notice:['YURI','Wait... his barrel! It\'s overheating!'],rally:['HOTWIRE','Take him down before he can recover!','I\'ll cover you. GO!'],victory:['HOTWIRE','He\'s down! Come on, Yuri. Into the elevator!']};
 function change(G,phase){const q=G.gosfar43,b=G.boss;q.phase=phase;q.t=0;q.log.push({phase,at:G.time});b.actionT=0;
  if(phase==='alarm'){q.door=1;A.fadeMusic(0,.6);A.play('warn',.7);A.play('e29_powerDown',.65);}
  if(phase==='opening')A.play('gd_doorOpen',.8);
  if(phase==='entrance'){q.door=6;b.hidden=false;b.state='enter';}
  if(phase==='taunt'){b.state='idle';q.alarm=0;q.power=true;q.door=7;A.play('e29_generator',.6);}
  if(phase==='bar'){q.barVisible=true;A.playMusic('gosfar43',.35);A.play('charge',.65);A.play('od75_debriefCount',.6);}
  if(phase==='rev'){b.state='windup';A.play('od75_minigunSpinUp',.9);}
  if(phase==='barrage'){b.state='shoot';q.nextShot=0;A.play('od75_minigunShot',.8);}
  if(phase==='notice'){b.state='overheat';b.firing=0;q.heat=1;G.eshots=[];A.play('od75_minigunSpinDown',.85);A.play('od75_flameEnd',.5);}
  if(phase==='combat'){q.controlReleased=true;q.heat=1;b.state='overheat';b.actionT=0;b.shield=false;Object.assign(G.player,{scripted:false,inv:75,cover:null,prone:false,stance:'stand',firing:0,moving:false});G.cp={x:530,y:475};G.shots=[];G.eshots=[];q.supplyCd=2;}
  if(phase==='victory'){G.score+=30000;G.units=[];G.eshots=[];G.shots=[];G.grenades=[];G.footGrenades=[];G.burns=[];G.grenades=[];G.footGrenades=[];G.burns=[];A.stopLoops();A.fadeMusic(.35,1.2);FX.boom(b.x,b.y-35,125,'gfx_destruction_',6);A.play('expBoss',.8);}
  if(phase==='exit'){G.player.cover=null;q.hot.action='run';A.play('gd_doorOpen',.6);}
  if(phase==='close'){A.play('gd_doorOpen',.6);}
 }
 function move(a,x,y,speed,dt){const dx=x-a.x,dy=y-a.y,d=Math.hypot(dx,dy),step=Math.min(d,speed*dt);if(d>.01){a.x+=dx/d*step;a.y+=dy/d*step;}a.moving=d>2;a.gaitPhase=((a.gaitPhase||0)+step/76)%1;a.a=a.aim=M.angTo(a.x,a.y,x,y);return d<3;}
 function path(a,points,speed,dt){a.route43??=0;if(a.route43>=points.length){a.moving=false;return true;}const p=points[a.route43];if(move(a,p[0],p[1],speed,dt))a.route43++;return a.route43>=points.length;}
 TD.makeGosfer=function(G,x,y){
  const b={gosfar43:true,name:'GOSFAR',x:400,y:170,hp:1200,max:1200,r:29,state:'idle',shield:true,hidden:true,dead:false,t:0,actionT:0,gait:0,flash:0,angle:0,firing:0,gauge:0,barriers:[],barrierLog:[]};
  G.gosfar43={phase:'hack',t:0,age:0,door:0,alarm:0,power:false,barVisible:false,bar:0,heat:0,log:[{phase:'hack',at:G.time}],wall:G.structures.filter(s=>s.gosfarWall43),hot:{x:350,y:177,action:'hack',t:0,fireCd:0,gaitPhase:0},supplies:[],allyShots:[],shots:0,hits:0,helpKills:0,throws:0};
  G.units=[];G.shots=[];G.eshots=[];G.msgs=[];G.fortress.pending=[];TD.Stealth.reset();G.grenades=[];G.footGrenades=[];G.burns=[];G.player.cover=null;FX.list=[];G.grenades=[];G.footGrenades=[];G.burns=[];G.player.cover=null;FX.list=[];
  b.alive=()=>!b.dead;b.hpFrac=()=>b.hp/b.max;b.aimPoint=()=>({x:b.x,y:b.y-40,r:29});b.aim=b.aimPoint;b.retinaTargets=()=>[{id:b,point:b.aimPoint,valid:()=>!b.dead&&G.gosfar43.phase==='combat'}];
  b.hit=(x,y,r,d,s)=>{if(b.dead||b.hidden)return false;const cx=s?s.x:x,cy=s?s.y-(TD.projectileLift?.(s)??s.drawLift??0):y;if(Math.hypot((cx-b.x)/46,(cy-(b.y-65))/65)>1+(r||0)/45)return false;if(G.gosfar43.phase!=='combat')return true;b.hp=Math.max(0,b.hp-d);b.flash=.14;G.gosfar43.hits++;if(!b.hp){b.dead=true;b.deathT=0;b.state='defeated';b.actionT=0;change(G,'victory');}return true;};b.blast=(x,y,r,d)=>b.hit(x,y,r,d);
  b.tick=dt=>{const q=G.gosfar43;b.t+=dt;b.actionT+=dt;b.flash=Math.max(0,b.flash-dt);b.firing=Math.max(0,b.firing-dt);if(q.phase!=='combat'||b.dead)return;
   b.angle=M.angTo(b.x,b.y,G.player.x,G.player.y);q.heat=b.state==='overheat'?Math.max(0,1-b.actionT/3.4):Math.min(1,b.actionT/2.1);
   if(b.state==='overheat'&&b.actionT>3.4){b.state='move';b.actionT=0;b.targetX=b.x>400?245:555;b.targetY=G.player.y<b.y+35?M.clamp(G.player.y+210,260,495):260;}
   else if(b.state==='move'){const dx=b.targetX-b.x,dy=(b.targetY??260)-b.y,dist=Math.hypot(dx,dy),step=Math.min(dist,90*dt);b.x+=dx/(dist||1)*step;b.y+=dy/(dist||1)*step;W.collide(b,29,false);b.gait+=step/70;if(dist<3||b.actionT>3.2){b.state='windup';b.actionT=0;b.target={x:G.player.x,y:G.player.y};A.play('od75_minigunSpinUp',.75);}}
   else if(b.state==='windup'){if(b.actionT<.7)b.target={x:G.player.x,y:G.player.y};if(b.actionT>1.15){b.state='shoot';b.actionT=0;b.sent=0;}}
   else if(b.state==='shoot'){while(b.sent<48&&b.actionT>=b.sent*.035){fire(G,b,b.target.x+(b.sent-24)*2.2,b.target.y,false);b.sent++;}if(b.actionT>1.9){b.state='overheat';b.actionT=0;A.play('od75_minigunSpinDown',.65);}}
   else if(b.state==='recover'&&b.actionT>1){b.state='overheat';b.actionT=0;}
   if(b.hp<=b.max*.5&&!q.reinforcements){q.reinforcements=true;A.play('warn',.5);for(const side of [-1,1])for(let j=0;j<2;j++){const u=TD.makeUnit('c35_flame',side<0?96:704,245+j*65,{a:0});u.reinforcement39=true;u.sense39={home:{x:u.x,y:u.y,a:0},memory:8,scan:0,visible:false,known:{x:G.player.x,y:G.player.y}};G.units.push(u);}G.say('HOTWIRE: FLAMETHROWERS! I\'VE GOT YOUR BACK.',G.player);}
  };
  b.drawUnder=ctx=>{const q=G.gosfar43;if(q.phase==='combat'&&['windup','shoot'].includes(b.state)){const col=b.state==='shoot'?'red':b.actionT>.76?'red':b.actionT>.38?'yellow':'green',s=TD.gosferSocket(b),target=b.target||G.player;ART.draw(ctx,'bmfx_fov_'+col+'_tall',s.x,s.y,{ax:159.5,ay:11,a:M.angTo(s.x,s.y,target.x,target.y),sx:.30,sy:Math.min(290,Math.hypot(target.x-s.x,target.y-s.y))/267,alpha:.6});}};
  b.draw=ctx=>{if(b.hidden)return;const z=TD.gosferPose(b);art.draw(ctx,z.key,b.x,b.y,{s:1,flash:b.flash>0?.8:0,alpha:b.dead?Math.max(0,1-(b.deathT||0)/2.3):1});};b.drawOver=()=>{};
  return b;
 };
 mission.boss=TD.makeGosfer;
 const previousPose=TD.gosferPose;
 api.direction43=function(b){const q=TD.game.gosfar43;if(q?.phase!=='combat'||b.dead)return 'south';if(b.state==='move'){const dx=b.targetX-b.x,dy=(b.targetY??260)-b.y;return Math.abs(dx)>Math.abs(dy)?dx>0?'east':'west':dy>0?'south':'north';}const target=['windup','shoot'].includes(b.state)&&b.target?b.target:TD.game.player,dx=target.x-b.x,dy=target.y-b.y;return Math.abs(dx)>Math.abs(dy)?dx>0?'east':'west':dy>0?'south':'north';};
 TD.gosferPose=function(b){if(!b.gosfar43)return previousPose(b);const q=TD.game.gosfar43,dir=api.direction43(b);let action=b.dead?'death':b.state==='overheat'?'overheat':b.state==='shoot'?'fire':b.state==='windup'?'rev':b.state==='move'||q?.phase==='entrance'?'walk':'ready';let name='gosfar/'+action+(dir==='south'?'':'/'+dir);if(!P.banks[name])name='gosfar/ready/'+dir;const clock=b.dead?(b.deathT||0):b.state==='move'?b.gait:b.actionT,key=clip(name,clock,!b.dead);return{key,bank:name,phase:P.banks[name].frames.indexOf(key),flip:false,dir};};
 const oldSocket=TD.gosferSocket;TD.gosferSocket=function(b){if(!b.gosfar43)return oldSocket(b);const z=TD.gosferPose(b),m=P.assets[z.key],u=m.muzzle||[82,102];return{x:b.x+u[0]-m.anchor[0],y:b.y+u[1]-m.anchor[1]};};
 function fire(G,b,x,y,scripted){const s=TD.gosferSocket(b),a=M.angTo(s.x,b.y,x,y),f=M.fwd(a);G.eshots.push({owner:b,k:'mg',contra35:true,attackKind35:'mg',x:s.x,y:b.y,a,vx:f[0]*7.8,vy:f[1]*7.8,dmg:scripted?0:1,life:95,r:3,t:0,drawLift:b.y-s.y,liftStart:b.y-s.y,liftEnd:14,spawnX:s.x,spawnY:b.y,flightDist:Math.hypot(x-s.x,y-b.y),hitsProne:true,scripted43:scripted});b.firing=.08;FX.attachedFlash(b,TD.gosferSocket,a,.06);G.gosfar43.shots++;A.play('od75_minigunShot',.8);}
 function scriptTick(G,dt){const q=G.gosfar43,b=G.boss,p=G.player;G.time+=dt;q.age+=dt;q.t+=dt;b.t+=dt;b.actionT+=dt;b.flash=Math.max(0,b.flash-dt);if(b.dead)b.deathT=(b.deathT||0)+dt;q.hot.t+=dt;p.footTime+=dt;p.poseT+=dt;p.firing=0;p.scripted=true;p.inv=90;p.roll=0;p.jump=0;p.action=null;p.vx=p.vy=0;p.prone=false;p.stance='crouch';p.moving=false;G.shots=[];G.msgs=[];
  q.alarm=['alarm','opening','entrance'].includes(q.phase)?Math.min(.42,q.t*.16)*(.55+.45*Math.sin(q.age*9)**2):0;
  if(q.phase==='hack'){p.stance='stand';q.hot.action='hack';move(p,530,411,145,dt);if(Math.floor(q.t*5)!==Math.floor((q.t-dt)*5))A.play('blip',.22);}
  if(['alarm','opening'].includes(q.phase)){p.stance='stand';q.hot.action='run';if(path(q.hot,[[110,206],[110,407],[188,411]],180,dt))q.hot.action='cover';if(move(p,540,411,145,dt)){p.cover43=true;p.stance='crouch';}if(Math.floor(q.t*1.5)!==Math.floor((q.t-dt)*1.5))A.play('gd_doorOpen',.42);}
  if(!['hack','alarm','opening','victory','exit','close','fade'].includes(q.phase)){q.hot.action='cover';q.hot.x=188;q.hot.y=411;p.x=540;p.y=411;p.cover43=true;}
  if(q.phase==='opening')q.door=2+Math.min(4,Math.floor(q.t/1.9*5));
  if(q.phase==='entrance'){b.y=M.lerp(170,260,M.clamp(q.t/2.5,0,1));b.gait=q.t*.9;}
  if(q.phase==='bar'){q.bar=M.clamp(q.t/durations.bar,0,1);b.gauge=q.bar;}
  if(q.phase==='barrage'){q.heat=M.clamp(q.t/9.5,0,1);while(q.nextShot<=q.t){const n=Math.round(q.nextShot/.018),tx=155+(n*29)%500;fire(G,b,tx,380,true);q.nextShot+=.018;}for(let i=1;i<q.wall.length;i++){const wall=q.wall[i],age=q.t-(i-1)*1.45;if(age>0&&!wall.dead){wall.hp=Math.max(0,150-age*96);wall.flash=.05;if(Math.floor(age*12)!==Math.floor((age-dt)*12))FX.concrete(wall.x+(Math.sin(age*33)*35),wall.y-10,25);if(!wall.hp){wall.dead=true;W.remove(wall.rect);FX.concrete(wall.x,wall.y,110);A.play('od75_wallBreach',.8);TD.Cam.kick(4);}}}TD.shotTick(G);}
  if(q.phase==='victory'){q.hot.action='cover';p.cover43=true;}
  if(q.phase==='exit'){p.cover43=false;q.hot.action='run';p.stance='stand';path(p,[[690,420],[690,235],[420,150]],210,dt);if(path(q.hot,[[110,410],[110,235],[380,150]],210,dt))q.hot.action='ready';}
  if(q.phase==='close')q.door=Math.max(0,6-Math.floor(q.t/1.5*7));
  FX.update(dt);for(const wall of q.wall)wall.flash=Math.max(0,wall.flash-dt);TD.Cam.zoom=1;TD.Cam.follow(400,270,.15);TD.Cam.shake*=.86;
  if(q.t>=durations[q.phase]){const order=['hack','alarm','opening','entrance','taunt','plan','spotted','bar','rev','barrage','notice','rally','combat'];if(q.phase==='fade')return 'clear';if(q.phase==='victory'){p.route43=0;q.hot.route43=0;change(G,'exit');}else if(q.phase==='exit'){change(G,'close');}else if(q.phase==='close')change(G,'fade');else change(G,order[order.indexOf(q.phase)+1]);}
 }
 mission.exclusiveWhen=G=>!!G.gosfar43&&G.gosfar43.phase!=='combat';mission.exclusiveStep=scriptTick;
 const cam=mission.cam;mission.cam=function(G){if(G.gosfar43){TD.Cam.zoom=1;TD.Cam.follow(400,270,.10);}else cam(G);};
 const pre=mission.pre;mission.pre=function(G,dt){if(!G.boss?.gosfar43)return pre(G,dt);G.player.scripted=false;G.player.cover43=false;G.player.y=Math.max(180,Math.min(535,G.player.y));};
 const tick=mission.tick;mission.tick=function(G,dt){if(!G.boss?.gosfar43)return tick?.(G,dt);const q=G.gosfar43;if(q.phase!=='combat')return;q.t+=dt;q.age+=dt;q.hot.t+=dt;support(G,dt);};
 function support(G,dt){const q=G.gosfar43,h=q.hot;h.fireCd-=dt;h.actionT=(h.actionT||0)+dt;if(h.actionT>.5&&h.action!=='cover')h.action='cover';
  const enemies=G.units.filter(u=>!u.dead&&u.kind35==='flame'),enemy=enemies.sort((a,b)=>Math.hypot(a.x-h.x,a.y-h.y)-Math.hypot(b.x-h.x,b.y-h.y))[0];
  if(enemy&&h.fireCd<=0&&h.action==='cover'&&q.supplyCd>.5){h.fireSide=enemy.x<188?-1:1;h.peekEnemy=enemy;}
  const goal=(h.peekEnemy&&!h.peekEnemy.dead||h.action==='fire')?188+h.fireSide*18:188;h.x+=Math.sign(goal-h.x)*Math.min(Math.abs(goal-h.x),180*dt);
  if(h.peekEnemy&&!h.peekEnemy.dead&&Math.abs(h.x-goal)<.5){const target=h.peekEnemy;h.peekEnemy=null;h.fireCd=.8;h.action='fire';h.actionT=0;const x=h.x+h.fireSide*29,y=h.y-65,a=M.angTo(x,y,target.x,target.y-25),f=M.fwd(a);q.allyShots.push({x,y,vx:f[0]*650,vy:f[1]*650,a,t:0});A.play('od75_sniper',.65);}
  if(h.peekEnemy?.dead)h.peekEnemy=null;
  for(const s of q.allyShots){s.t+=dt;s.x+=s.vx*dt;s.y+=s.vy*dt;for(const target of G.units)if(!target.dead&&Math.hypot((s.x-target.x)/19,(s.y-(target.y-25))/31)<1){TD.hitUnit(G,target,3,s.x,s.y);if(target.dead)q.helpKills++;s.done=true;FX.concrete(s.x,s.y,12);break;}}q.allyShots=q.allyShots.filter(s=>!s.done&&s.t<1.2);
  q.supplyCd-=dt;if(q.supplyCd<=0){q.supplyCd=10;h.peekEnemy=null;h.action='throw';h.actionT=0;const kind=['flamethrower','cryo_lance','minigun','spread_shotgun'][q.throws++%4];q.supplies.push({kind,x:h.x,y:h.y,tx:M.clamp(G.player.x,290,630),ty:M.clamp(G.player.y,430,515),t:-.28});A.play('od75_mineThrow',.4);G.say('HOTWIRE: CATCH! / '+kind.replaceAll('_',' ').toUpperCase(),G.player);}
  for(const s of q.supplies){s.t+=dt;if(s.t>=.85&&!s.done){s.done=true;G.pickups.push({kind:s.kind,x:s.tx,y:s.ty,t:0});A.play('od75_ammoPickup',.5);}}q.supplies=q.supplies.filter(s=>!s.done);
 }
 const floor=mission.drawFloor;
 // The elevator is one authored door bank. Rendering never stretches its doors.
 mission.drawFloor=function(ctx,G){const q=G.gosfar43;const oldDoor=G.fortress.doorOpen;G.fortress.doorOpen=false;floor(ctx,G);G.fortress.doorOpen=oldDoor;const key=P.banks.elevator.frames[q?.door||0];art.draw(ctx,key,400,180,{s:1});};
 const actors=TD.Depth35.drawActors;TD.Depth35.drawActors=function(ctx,G){if(G.mission!==3||!G.gosfar43)return actors(ctx,G);actors(ctx,G);const q=G.gosfar43,h=q.hot;if(!h.hidden){let name='hotwire/'+h.action;if(!P.banks[name])name='hotwire/cover';if(h.action==='run'){const bank=P.banks['hotwire/run'];if(bank)art.draw(ctx,bank.frames[Math.floor(h.t*12)%bank.frames.length],h.x,h.y,{s:1});else plate(ctx,'hotwire/run',h.t,h.x,h.y);}else {ctx.save();ctx.translate(h.x,h.y);if(h.action==='fire'&&h.fireSide>0)ctx.scale(-1,1);plate(ctx,name,h.action==='hack'||h.action==='cover'?h.t:h.actionT||0,0,0,{loop:h.action==='hack'||h.action==='cover'});ctx.restore();}}for(const s of q.allyShots)TD.drawShot(ctx,{...s,k:'mg',contra35:true,attackKind35:'mg',t:s.t*60,r:3},false);for(const s of q.supplies){if(s.t<0)continue;const u=M.clamp(s.t/.85,0,1);TD.drawFootPickup(ctx,{kind:s.kind,x:M.lerp(s.x,s.tx,u),y:M.lerp(s.y,s.ty,u)-Math.sin(Math.PI*u)*85,t:s.t});}liftFront43(ctx,q);};
 function liftFront43(ctx,q){if(!['close','fade'].includes(q.phase)&&!(q.phase==='exit'&&q.t>4))return;const gap=[[80,80],[80,80],[78,82],[72,88],[63,97],[56,104],[48,112],[48,112]][q.door],key=P.banks.elevator.frames[q.door];for(const [a,b]of [[0,gap[0]],[gap[1],160]]){ctx.save();ctx.beginPath();ctx.rect(320+a,28,b-a,160);ctx.clip();art.draw(ctx,key,400,180,{s:1});ctx.restore();}}
 const foot=TD.footPose;TD.footPose=function(p){if(TD.game?.mission===3&&TD.game.gosfar43&&p.cover43)return {key:clip('yuri/cover',TD.game.gosfar43.age),scale:1,angle:0,action:'panic-cover',dir:'south'};return foot(p);};
 const drawFoot=TD.drawFoot;TD.drawFoot=function(ctx,p,o){if(TD.game?.mission===3&&TD.game.gosfar43?.playerHidden)return;if(TD.game?.gosfar43&&p.scripted)o={...o,flash:0};drawFoot(ctx,p,o);};
 const over=mission.drawOver;mission.drawOver=function(ctx,G){if(!G.gosfar43)return over(ctx,G);const q=G.gosfar43;if(q.alarm>0){ctx.fillStyle='rgba(235,8,18,'+q.alarm+')';ctx.fillRect(TD.Cam.x,TD.Cam.y,TD.VW/TD.Cam.zoom,TD.VH/TD.Cam.zoom);}if(q.phase==='fade'){ctx.fillStyle='rgba(0,0,0,'+M.clamp(q.t/1.2,0,1)+')';ctx.fillRect(TD.Cam.x,TD.Cam.y,TD.VW/TD.Cam.zoom,TD.VH/TD.Cam.zoom);}};
 const hud=mission.hud;mission.hud=function(ctx,text,G){const q=G.gosfar43;if(!q)return hud(ctx,text,G);TD.CornerHUD26.draw(ctx,text,G,false);const b=G.boss,w=TD.VW,h=TD.VH;if(q.barVisible&&!b.dead){art.draw(ctx,'pb20_hud_boss',w/2,62,{s:.76});ctx.fillStyle='#e64e32';ctx.fillRect(w/2-93,59,186*(q.phase==='bar'?q.bar:b.hp/b.max),7);text('GOSFAR / HEAVY ROTARY MINIGUN',w/2,50,9,'#ffcf8a','center');}if(q.alarm>0)text('SECURITY ALERT / FREIGHT LIFT DESCENDING',w/2,110,11,'#ff7871','center');const lines=words[q.phase];if(lines){art.draw(ctx,'pb20_hud_dialogue',w/2,h-48,{s:.9});text(lines[0],w/2,h-68,11,lines[0]==='GOSFAR'?'#c4a3ed':'#88e8ed','center');for(let i=1;i<lines.length;i++)text(lines[i],w/2,h-48+(i-1)*16,10,'#fff','center');}else if(q.phase==='combat')text(b.state==='overheat'?'BARREL OVERHEATED / ATTACK!':'DEFEAT GOSFAR / HOTWIRE IS COVERING YOU',w/2,h-28,10,b.state==='overheat'?'#ffe281':'#d1e7e6','center');return true;};
 const actor=A.actor;A.actor=function(p,gain,player){actor.call(this,p,gain,player);const q=TD.game?.mission===3&&TD.game.gosfar43;if(player&&q&&q.alarm>0)this.loop('gd_alarmLoop','gosfar43-alarm',.75);if(player&&q&&q.phase==='bar'&&q.t<1.7)this.loop('od75_turretServo','gosfar43-bar',.7,1.1);};
 ART.warm(Object.keys(P.assets));
})(window);
