/* Dead Signal escape: a continuous authored on-foot route into Prism Bastion.
 * Coordinates and swept projectiles share one space; no hitscan damage. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,I=TD.Input,A=TD.Audio,FX=TD.FX,art=TD.AssaultArt,pack=root.TD_ESCAPE29_ART;
 const clamp=M.clamp,lerp=M.lerp,api=TD.Escape29={build:'overdrive1015-escape29-r1'};
 const mission=TD.MISSIONS.find(m=>m.id===3),oldTick=mission.tick,oldPre=mission.pre;
 const order=[2,3,7,4,5,6];
 for(const m of TD.MISSIONS){m.displayNumber={2:2,3:3,7:4,4:5,5:6,6:7}[m.id]||m.id;m.data.title='LEVEL '+m.displayNumber;}
 TD.campaignStep29=(from,d)=>{const id=TD.MISSIONS[from]?.id,at=order.indexOf(id),next=order[(at+d+order.length)%order.length];return TD.MISSIONS.findIndex(m=>m.id===next);};
 TD.campaignEnd29=sel=>TD.MISSIONS[sel]?.id===order.at(-1);
 mission.data.brief=['ONE HIT. USE LOW COVER, PRONE AND FIVE-SECOND ROLLS.','JUMP TOWARD LOW WALLS TO VAULT. HOLD COVER TO LAND LOW.','GOSFER KEEPS HIS SHIELD UNTIL HE BREAKS EVERY BARRIER.','AFTER GOSFER: ENTER THE ELEVATOR AND ESCAPE TO LEVEL 4.'];
 mission.pre=function(G,dt){oldPre(G,dt);if(G.boss?.dead){G.player.scripted=false;G.bossDeadT=null;G.fortress.doorOpen=true;}};
 mission.tick=function(G,dt){oldTick?.(G,dt);if(G.fortress?.exitReady29&&!G.player.dead&&G.player.y<163&&Math.abs(G.player.x-400)<64)api.begin(G);};
 api.active=G=>!!G.escape29&&!G.escape29.finished;
 api.defeated=function(G){G.bossDeadT=null;G.score+=30000;G.fortress.exitReady29=true;G.fortress.doorOpen=true;G.eshots=[];G.units=[];G.msgs=[];G.say('ELEVATOR OPEN / ENTER THE NORTH DOOR',{x:400,y:230});A.play('gd_doorOpen');};
 const floorAt=x=>x<800?350:x<1510?380:410;
 const initialSolids=()=>[{x:430,w:62,h:54},{x:690,w:68,h:68},{x:1120,w:62,h:54},{x:1450,w:60,h:62},{x:1960,w:64,h:56},{x:2350,w:62,h:56},{x:2780,w:60,h:54}].map((o,i)=>({...o,id:i,y:floorAt(o.x),hp:35,max:35,flash:0,dead:false}));
 const enemySpecs=[{x:610,kind:'rifle'},{x:1040,kind:'rifle'},{x:1320,kind:'heavy'},{x:1800,kind:'rifle'},{x:2150,kind:'laser'},{x:2530,kind:'rifle'},{x:2870,kind:'heavy'},{x:3100,kind:'rifle'}];
 function setPhase(G,phase){const e=G.escape29;e.phase=phase;e.t=0;e.log.push({phase,time:G.time});e.shots=[];e.enemyShots=[];e.cursor={x:420,y:270};e.lastMouse=null;G.player.firing=0;G.player.action=null;G.player.roll=0;G.player.jump=0;
  if(phase==='ascent'){A.play('gd_doorOpen');A.fadeMusic(.25,.7);}
  if(phase==='blackout'){A.play('e29_powerDown');A.fadeMusic(0,.35);}
  if(phase==='emergency'){A.play('e29_generator');A.play('warn',.5);}
  if(phase==='hatch'){e.checkpoint='hatch';e.hatchHp=24;e.cursor={x:374,y:409};Object.assign(G.player,{x:374,y:405});e.message='HOTWIRE: Shoot the floor hatch! Before you and that lift become a pancake!';}
  if(phase==='hinge'){A.play('gd_wallBreak');FX.boom(374,399,95,'gfx_destruction_',6);TD.Cam.kick(8);}
  if(phase==='chute'){e.checkpoint='chute';e.drones=[];e.vents=[];e.nextDrone=.6;e.spawned=0;e.cursor={x:380,y:175};Object.assign(G.player,{x:285,y:355,inv:1.6});e.message="HOTWIRE: Watch your butt. It's about to get hot! Shoot those drones!";A.playMusic('lastHope',1.2);}
  if(phase==='corridor'){e.checkpoint='corridor';e.camX=0;e.solids=initialSolids();e.enemies=[];e.pending=enemySpecs.map(x=>({...x}));e.barrels=[{x:3280,y:410,hp:8},{x:3310,y:410,hp:8},{x:3340,y:410,hp:8}];e.doorHp=1;e.doorBroken=false;e.blastX=-500;e.cursor={x:430,y:290};Object.assign(G.player,{x:100,y:350,velY29:0,inv:1.6,stance:'stand',prone:false});e.message='HOTWIRE: Service corridor. Stay low, use the crates. Keep moving right.';A.playMusic('base',1.2);}
  if(phase==='escape'){e.checkpoint='escape';e.blastX=G.player.x-650;e.message='SELF-DESTRUCT / RUN RIGHT!';A.playMusic('lastHope',.5);A.play('warn');}
  if(phase==='doorSlide'){e.message='HOTWIRE: Through that door! Slide, now!';G.player.slide29=.8;A.play('stylishDodge',.6);}
  if(phase==='drop'){A.play('gd_doorOpen');e.message='HOTWIRE: You made it. Prism Bastion is below you.';}
 }
 api.begin=function(G){
  G.escape29={phase:'ascent',t:0,age:0,camX:0,log:[],shots:[],enemyShots:[],drones:[],vents:[],enemies:[],solids:[],barrels:[],sparks:[],cursor:{x:420,y:270},checkpoint:'hatch',message:'HOTWIRE: Good. Take the service elevator.',shotCount:0,intercepts:0,kills:0,damage:0,hatchHp:24};
  G.boss=null;G.bossDeadT=null;G.units=[];G.eshots=[];G.shots=[];G.msgs=[];FX.list=[];Object.assign(G.player,{x:374,y:405,hp:1,max:1,oneHit29:true,sideScroll:true,pseudo3D:false,dead:false,scripted:false,moving:false,vx:0,vy:0,inv:1,velY29:0,rollCd:0,aim:-Math.PI/2,sideFacing29:'east',stance:'stand',prone:false,peek29:0});TD.Cam.x=TD.Cam.y=0;TD.Cam.zoom=1;setPhase(G,'ascent');
 };
 function hitPlayer(G){const p=G.player,e=G.escape29;if(p.dead||p.inv>0||p.vault29||p.roll>.08&&p.roll<.42||p.slide29>.1&&p.slide29<.5)return false;p.hp=0;p.dead=true;p.deadT=0;p.flash=.18;p.firing=0;G.deaths++;e.damage++;A.play('playerDeath');A.play('hit');TD.Cam.kick(6);return true;}
 function respawn(G){const e=G.escape29,p=G.player;G.lives--;if(G.lives<0){G.state='gameover';G.stateT=0;A.stopMusic();return;}Object.assign(p,{dead:false,deadT:0,hp:1,max:1,inv:2,roll:0,slide29:0,vault29:null,sideCover29:null,peek29:0,prone:false,stance:'stand',velY29:0,fireCd:0});
  const check=e.checkpoint;setPhase(G,check==='escape'?'corridor':check);if(check==='escape'){p.x=1660;p.y=floorAt(p.x);e.pending=e.pending.filter(s=>s.x>p.x);setPhase(G,'escape');e.camX=p.x-200;}
 }
 function aim(G,dt){const e=G.escape29,p=G.player,[dx,dy]=I.dir(),free=I.down('retina');p.freeAim=free;
  const mouse=I.pointer,moved=mouse.active&&(mouse.x!==e.lastMouse?.x||mouse.y!==e.lastMouse?.y);if(moved){e.aimDevice29='mouse';e.lastMouse={x:mouse.x,y:mouse.y};}else if(free&&(dx||dy))e.aimDevice29='pad';
  if(mouse.active&&e.aimDevice29!=='pad'){e.cursor={x:mouse.x+e.camX,y:mouse.y};}
  else if(free){e.cursor.x=clamp(e.cursor.x+dx*520*dt,e.camX+8,e.camX+632);e.cursor.y=clamp(e.cursor.y+dy*460*dt,90,450);}
  else if(!['hatch','chute','hinge'].includes(e.phase)&&dx){p.sideFacing29=dx>0?'east':'west';e.cursor={x:p.x+dx*280,y:p.y-58};}
  p.aim=M.angTo(p.x,p.y-55,e.cursor.x,e.cursor.y);if(Math.abs(Math.sin(p.aim))>.1&&e.phase!=='chute')p.sideFacing29=Math.sin(p.aim)<0?'east':'west';
 }
 api.pose=function(G){const e=G.escape29,p=G.player,side=p.sideFacing29||'east',f=TD.Combat29.frame;
  if(p.dead)return art.frame('pb19_yuri_north_knockback',p.deadT,false)||art.frame('yuri_north_knockback',p.deadT,false);
  if(e.phase==='chute'||e.phase==='hinge')return api.slidePose(G);
  if(p.vault29)return f('vault_'+side,p.vault29.t/.68*.85,false);
  if(p.slide29>0)return f('slide_flat_'+side,(.65-p.slide29),true)||f('prone_'+side,.9,false);
  if(p.roll>0)return f('roll_'+side,(.5-p.roll)/.5*.85,false);
  if(p.prone)return f('prone_'+side,p.moving?p.sideGait29||0:.9,!!p.moving);
  if(p.sideCover29){const q=pack.sequences['e29_cover_peek_'+side];return q?.frames[Math.round(clamp(p.peek29,0,1)*(q.frames.length-1))];}
  if(p.stance==='crouch')return f('crouch_'+side,p.moving?p.sideGait29||0:0,true);
  if(p.moving&&!p.freeAim)return f('run_'+side,p.sideGait29||0,true);
  return TD.Combat29.aimKey(p);
 };
 api.slidePose=function(G){const e=G.escape29,p=G.player,dx=e.cursor.x-p.x,dy=e.cursor.y-(p.y-45);let key;
  if(dy>25)key='e29_slide_down';else if(dx<-40)key='e29_slide_back';else if(Math.abs(dx)<60)key='e29_slide_up';
  return pack.assets[key]?key:TD.Combat29.frame('slide_motion_east',e.age,true);
 };
 api.socket=function(G){const p=G.player,k=api.pose(G),m=pack.assets[k]||root.TD_ASSAULT_ART.assets[k],q=m?.muzzle||[96,100],rootPoint=m?.anchor||[96,160];return{x:p.x+q[0]-rootPoint[0],y:p.y+q[1]-rootPoint[1]};};
 function fire(G){const e=G.escape29,p=G.player,w=p.weapons[p.wi||0],d=TD.FOOT_GUNS[w.id]||TD.FOOT_GUNS.assault_rifle;p.firing=.10;p.shotAge=0;const q=api.socket(G);p.fireCd=Math.max(.045,d.cd/60);const a=M.angTo(q.x,q.y,e.cursor.x,e.cursor.y);
  for(const delta of d.fan||[0]){const v=M.fwd(a+delta);e.shots.push({x:q.x,y:q.y,px:q.x,py:q.y,vx:v[0]*900,vy:v[1]*900,a:a+delta,kind:d.k,damage:d.damage,life:1.5,pierce:d.pierce||0});e.shotCount++;}
  if(Number.isFinite(w.ammo)&&--w.ammo<=0){p.weapons=[p.weapons.find(x=>x.id==='assault_rifle')||{id:'assault_rifle',ammo:Infinity,lv:1}];p.wi=0;}
  A.play(d.k==='laser'?'laser':'gd_soldierRifle',.5);p.muzzleAim=a;
 }
 function hitRect(s,x,y,w,h){let lo=0,hi=1;for(const[a,b,l,r]of[[s.px,s.x,x-w,x+w],[s.py,s.y,y-h,y+h]]){const d=b-a;if(Math.abs(d)<1e-6){if(a<l||a>r)return false;continue;}let n=(l-a)/d,m=(r-a)/d;if(n>m)[n,m]=[m,n];lo=Math.max(lo,n);hi=Math.min(hi,m);if(lo>hi)return false;}return true;}
 function impact(e,x,y){e.sparks.push({x,y,t:0});A.play('impactMetal',.4);TD.Cam.kick(1.2);}
 function enemyShot(G,u,x,y,kind='mg'){const e=G.escape29,p=G.player,target={x:p.x,y:p.y-(p.prone?13:48)},a=M.angTo(x,y,target.x,target.y),v=M.fwd(a),speed=kind==='laser'?400:340;e.enemyShots.push({x,y,px:x,py:y,vx:v[0]*speed,vy:v[1]*speed,a,kind,life:3,owner:u});A.play(kind==='laser'?'enemyHeavyLaser':'gd_soldierRifle',.35);}
 function projectiles(G,dt){const e=G.escape29,p=G.player;
  for(const s of e.shots){s.px=s.x;s.py=s.y;s.x+=s.vx*dt;s.y+=s.vy*dt;s.life-=dt;
   for(const b of e.enemyShots)if(!b.dead&&hitRect(s,b.x,b.y,10,10)){b.dead=s.dead=true;e.intercepts++;impact(e,b.x,b.y);break;}
   if(s.dead)continue;
   if(e.phase==='hatch'&&I.down('retina')&&hitRect(s,374,397,54,13)){e.hatchHp-=s.damage;s.dead=true;e.hatchFlash=.12;impact(e,s.x,s.y);if(e.hatchHp<=0){setPhase(G,'hinge');break;}}
   for(const u of [...(e.drones||[]),...(e.enemies||[])]){if(s.dead||u.dead||u.phase==='retreat'&&u.retreatT>.35)continue;if(hitRect(s,u.x,u.y-(u.drone?0:45),u.drone?24:20,u.drone?20:42)){u.hp-=s.damage;u.flash=.10;s.dead=!s.pierce;impact(e,s.x,s.y);if(u.drone){u.phase='retreat';u.retreatT=.7;u.fireCd=1.5;u.hits=(u.hits||0)+1;}if(u.hp<=0){u.dead=true;u.deadT=0;G.score+=u.drone?450:650;G.kills++;e.kills++;FX.boom(u.x,u.y-(u.drone?0:42),85,'gfx_destruction_',6);A.play('enemyDie',.45);}break;}}
   for(const c of e.solids||[])if(!s.dead&&!c.dead&&hitRect(s,c.x,c.y-c.h/2,c.w/2,c.h/2)){if(p.sideCover29!==c||!p.peekExposed){c.hp-=s.damage;c.flash=.1;s.dead=true;impact(e,s.x,s.y);if(c.hp<=0){c.dead=true;FX.boom(c.x,c.y-30,65,'gfx_destruction_',6);}}}
   for(const b of e.barrels||[])if(!s.dead&&!b.dead&&hitRect(s,b.x,b.y-24,15,26)){s.dead=true;b.hp-=s.damage;b.flash=.12;if(b.hp<=0){b.dead=true;e.doorBroken=true;e.barrels.forEach(q=>q.dead=true);FX.boom(3320,375,180,'gfx_destruction_',6);FX.boom(3405,340,180,'gfx_destruction_',6);A.play('expB');TD.Cam.kick(9);e.message='DOOR BLOWN / DOWN + ROLL TO SLIDE THROUGH';}}
  }
  for(const s of e.enemyShots){if(s.dead)continue;s.px=s.x;s.py=s.y;s.x+=s.vx*dt;s.y+=s.vy*dt;s.life-=dt;
   for(const c of e.solids||[])if(!c.dead&&hitRect(s,c.x,c.y-c.h/2,c.w/2,c.h/2)){c.hp--;c.flash=.1;s.dead=true;impact(e,s.x,s.y);if(c.hp<=0){c.dead=true;FX.boom(c.x,c.y-30,70,'gfx_destruction_',6);}break;}
   if(!s.dead&&hitRect(s,p.x,p.y-(p.prone||p.slide29>0?14:p.stance==='crouch'?30:47),12,p.prone||p.slide29>0?10:p.stance==='crouch'?24:38)){s.dead=true;hitPlayer(G);}
  }
  e.shots=e.shots.filter(s=>!s.dead&&s.life>0);e.enemyShots=e.enemyShots.filter(s=>!s.dead&&s.life>0);e.sparks.forEach(s=>s.t+=dt);e.sparks=e.sparks.filter(s=>s.t<.18);
 }
 function drones(G,dt){const e=G.escape29;e.nextDrone-=dt;if(e.nextDrone<=0&&e.t<24){const side=e.spawned%2?1:-1,x=side<0?90:550;e.nextDrone=3.6;e.spawned++;e.vents.push({x,y:90,t:0});e.drones.push({drone:true,x,y:60,homeX:x,side,yBase:155+(e.spawned%2)*42,hp:10,max:10,phase:'descend',age:0,flash:0,fireCd:2.6,spawn:e.spawned});A.play('gd_wallBreak',.4);}
  for(const u of e.drones){u.flash=Math.max(0,u.flash-dt);u.age+=dt;if(u.dead){u.deadT+=dt;continue;}if(u.phase==='descend'){u.y+=110*dt;if(u.y>=u.yBase)u.phase='orbit';}
   else if(u.phase==='retreat'){u.retreatT-=dt;u.x+=u.side*230*dt;u.y-=65*dt;if(u.retreatT<=0)u.phase='return';}
   else if(u.phase==='return'){u.x=lerp(u.x,u.homeX,dt*5);u.y=lerp(u.y,u.yBase,dt*5);if(Math.hypot(u.x-u.homeX,u.y-u.yBase)<12)u.phase='orbit';}
   else{u.x=lerp(u.x,320+Math.sin(u.age*1.25+u.spawn)*210,dt*3);u.y=u.yBase+Math.sin(u.age*2.2)*25;u.fireCd-=dt;if(u.fireCd<=0){enemyShot(G,u,u.x,u.y+14,'laser');u.fireCd=2.4;u.firing=.15;}u.warn=u.fireCd<.65;}
  }e.drones=e.drones.filter(u=>!u.dead||u.deadT<.8);e.vents.forEach(v=>v.t+=dt);e.vents=e.vents.filter(v=>v.t<2);
 }
 function sideControls(G,dt){const e=G.escape29,p=G.player,[dx,dy]=I.dir(),low=dy>0||I.down('cover')||I.down('C'),free=I.down('retina');p.rollCd=Math.max(0,p.rollCd-dt);const rollWas=p.roll;p.roll=p.roll<=dt+1e-6?0:p.roll-dt;if(rollWas>0&&p.roll===0){p.prone=!!p.rollProne;p.stance=p.prone?'prone':'stand';}p.slide29=Math.max(0,(p.slide29||0)-dt);p.jump=Math.max(0,p.jump-dt);
  if(I.tap('prone')&&!p.vault29){if(p.roll>0)p.rollProne=!p.rollProne;else{p.prone=!p.prone;p.stance=p.prone?'prone':'stand';}}
  if(p.vault29){const v=p.vault29;v.t+=dt;if(I.tap('X')&&p.rollCd<=0)v.roll=true;const u=clamp(v.t/.68,0,1);p.x=lerp(v.from,v.to,u);p.y=lerp(v.y,floorAt(v.to),u)-Math.sin(u*Math.PI)*90;p.moving=false;if(u===1){p.vault29=null;p.stance=low?'crouch':'stand';if(v.roll){p.roll=.5;p.rollCd=5;p.rollDir=Math.sign(v.to-v.from)||1;p.rollProne=I.down('prone')||low;p.firing=0;}}return;}
  const ground=floorAt(p.x),grounded=p.y>=ground-.5,dir=dx?Math.sign(dx):p.sideFacing29==='west'?-1:1;
  if((I.tap('B')||I.tap('reload')||I.tap('jump'))&&grounded&&p.roll<=0&&p.slide29<=0){const wall=e.solids.find(s=>!s.dead&&Math.abs(s.x-p.x)<s.w/2+45&&Math.sign(s.x-p.x)===dir);p.prone=false;p.sideCover29=null;if(wall){p.vault29={from:p.x,to:wall.x+dir*(wall.w/2+28),y:p.y,t:0,roll:false};p.stance='stand';A.play('stylishDodge',.5);return;}p.velY29=-370;p.jump=.70;A.play('stylishDodge',.45);}
  if(I.tap('X')&&grounded&&p.rollCd<=0){p.rollCd=5;p.rollDir=dir;p.rollProne=p.prone||I.down('prone');p.prone=false;p.firing=0;if(low)p.slide29=.65;else p.roll=.5;A.play('stylishDodge',.5);}
  p.stance=p.prone?'prone':low?'crouch':'stand';p.sideCover29=null;
  const old=p.x,speed=p.slide29>0?430:p.roll>0?360:p.prone?68:p.stance==='crouch'?100:255;p.x+=((p.roll>0||p.slide29>0)?p.rollDir:free?0:dx)*speed*dt;p.x=Math.max(25,p.x);
  p.velY29+=1000*dt;p.y+=p.velY29*dt;const floor=floorAt(p.x);if(p.y>=floor){p.y=floor;p.velY29=0;p.jump=0;}
  for(const s of e.solids)if(!s.dead&&p.y>s.y-s.h+4&&Math.abs(p.x-s.x)<=s.w/2+14){if(Math.abs(p.x-s.x)<s.w/2+12)p.x=s.x+(old<s.x?-1:1)*(s.w/2+12);if(low||p.prone)p.sideCover29=s;}
  if(!e.doorBroken&&p.x>3370)p.x=3370;
  p.moving=Math.abs(p.x-old)>.1;p.sideGait29=(p.sideGait29||0)+Math.abs(p.x-old)/180;
  const trigger=I.down('A'),expose=!!p.sideCover29&&trigger;p.peek29=clamp((p.peek29||0)+(expose?dt*4:-dt*6),0,1);p.peekExposed=!!p.sideCover29&&p.peek29>.75;
  if(p.sideCover29&&p.peekExposed){/* The authored peek raises the barrel above its own box. */p.stance='stand';}
  if(I.tap('Y')&&p.smoke>0){p.smoke--;const x=clamp(e.cursor.x,p.x-200,p.x+250);for(const u of e.enemies)if(!u.dead&&Math.abs(u.x-x)<130){u.hp-=15;u.flash=.12;if(u.hp<=0){u.dead=true;u.deadT=0;G.kills++;G.score+=650;}}FX.boom(x,p.y-35,140,'gfx_destruction_',6);A.play('expB',.6);}
  if(e.phase==='corridor'&&p.x>1650)setPhase(G,'escape');
  if(e.phase==='escape'&&e.doorBroken&&p.x>3360&&p.slide29>0)setPhase(G,'doorSlide');
  e.camX=clamp(p.x-200,0,3030);
 }
 function sideEnemies(G,dt){const e=G.escape29,p=G.player;for(const spec of e.pending)if(!spec.entered&&spec.x<e.camX+690){spec.entered=true;e.enemies.push({...spec,x:e.camX+690,y:floorAt(spec.x),homeX:spec.x,hp:spec.kind==='heavy'?24:10,max:spec.kind==='heavy'?24:10,phase:'enter',age:0,fireCd:1.1,flash:0,walk:0});}
  for(const u of e.enemies){u.age+=dt;u.flash=Math.max(0,u.flash-dt);if(u.dead){u.deadT+=dt;continue;}u.y=floorAt(u.x);if(u.phase==='enter'){const d=Math.min(95*dt,Math.abs(u.x-u.homeX));u.x-=d;u.walk+=d/95;if(Math.abs(u.x-u.homeX)<2)u.phase='fight';}else{u.fireCd-=dt;if(u.fireCd<=0){u.burst=u.kind==='heavy'?5:2;u.burstCd=0;u.fireCd=u.kind==='heavy'?2.8:2.2;}}
   if(u.burst>0){u.burstCd-=dt;if(u.burstCd<=0){enemyShot(G,u,u.x-35,u.y-55,u.kind==='laser'?'laser':'mg');u.firing=.18;u.burst--;u.burstCd=.16;}}u.firing=Math.max(0,(u.firing||0)-dt);
  }e.enemies=e.enemies.filter(u=>!u.dead||u.deadT<1.2);e.solids.forEach(s=>s.flash=Math.max(0,s.flash-dt));
 }
 api.step=function(G,dt){const e=G.escape29,p=G.player;e.age+=dt;e.t+=dt;G.time+=dt;p.inv=Math.max(0,p.inv-dt);p.flash=Math.max(0,(p.flash||0)-dt);p.firing=Math.max(0,(p.firing||0)-dt);p.shotAge=(p.shotAge||0)+dt;p.fireCd=Math.max(0,(p.fireCd||0)-dt);e.hatchFlash=Math.max(0,(e.hatchFlash||0)-dt);TD.Cam.x=TD.Cam.y=0;TD.Cam.zoom=1;TD.Cam.shake*=.86;FX.update(dt);
  if(p.dead){p.deadT+=dt;if(p.deadT>1.5)respawn(G);return;}
  if(e.phase==='ascent'&&e.t>3)setPhase(G,'blackout');else if(e.phase==='blackout'&&e.t>1.6)setPhase(G,'emergency');else if(e.phase==='emergency'&&e.t>2.4)setPhase(G,'hatch');
  if(['emergency','hatch','escape'].includes(e.phase)){A.loop('gd_alarmLoop',e,.85,1);TD.Cam.kick(e.phase==='hatch'?1.5:.5);}else A.stopLoops();if(e.phase==='ascent')TD.Cam.kick(.4);
  aim(G,dt);
  if(e.phase==='hatch'&&I.down('retina')){e.cursor={x:p.x,y:p.y+4};p.aim=0;}
  TD.Yuri31?.update(G,dt);
  if(e.phase==='hatch'){p.stance=I.down('retina')?'stand':'crouch';if(e.t>18)hitPlayer(G);}
  if(e.phase==='hinge'&&e.t>1.1)setPhase(G,'chute');
  if(e.phase==='chute'){drones(G,dt);if(e.t>28)setPhase(G,'corridor');}
  if(['corridor','escape'].includes(e.phase)){sideControls(G,dt);e.camX=clamp(p.x-200,0,3030);sideEnemies(G,dt);}
  if(e.phase==='escape'){e.blastX+=212*dt;if(p.x<e.blastX+28)hitPlayer(G);if(G.t%9===0){FX.boom(e.blastX+Math.sin(e.age*10)*50,180+Math.random()*240,140,'gfx_destruction_',6);A.play('expS',.4);TD.Cam.kick(2.2);}}
  if(['hatch','chute','corridor','escape'].includes(e.phase)&&I.down('A')&&p.fireCd<=0&&!p.vault29&&!p.roll&&(!p.sideCover29||p.peekExposed))fire(G);
  projectiles(G,dt);
  if(e.phase==='doorSlide'){p.x+=420*dt;e.camX=3030;if(e.t>.8)setPhase(G,'drop');}
  if(e.phase==='drop'){p.y+=160*dt;if(e.t>1.8){const keep={score:G.score,lives:G.lives,deaths:G.deaths,kills:G.kills,time:G.time},log=e.log;G.sel=TD.MISSIONS.findIndex(m=>m.id===7);e.finished=true;root.TDGAME.start();Object.assign(G,keep);G.escapeHistory29=log;G.player.inv=2;TD.Frontend.progress={sel:G.sel,pilot:TD.pilot,difficulty:TD.difficulty,companion:TD.companion,completed:false};try{localStorage.setItem('bof_od_campaign',JSON.stringify(TD.Frontend.progress));}catch(_){}return;}}
 };
 function plate(ctx,key,x,y,s=1,o){art.draw(ctx,key,x,y,{s,...o});}
 function tiled(ctx,key,left,top,w,h){const im=ART.get(key);if(!im)return;for(let y=top;y<top+h;y+=im.sh)for(let x=left;x<left+w;x+=im.sw)ctx.drawImage(im.im,im.sx,im.sy,im.sw,im.sh,x,y,im.sw,im.sh);}
 function projectileDraw(ctx,s,enemy){const key=s.kind==='laser'?'gfx_ap_shell':enemy?'gfx_shell':'nlz_slug',im=ART.get(key);if(!im)return;const length=enemy?19:23,width=enemy?7:8;ctx.save();ctx.translate(s.x,s.y);ctx.rotate(s.a+Math.PI);ctx.drawImage(im.im,im.sx,im.sy,im.sw,im.sh,-width/2,-length/2,width,length);ctx.restore();}
 function playerDraw(ctx,G){const p=G.player,k=api.pose(G),m=pack.assets[k]||root.TD_ASSAULT_ART.assets[k];if(!m)return;plate(ctx,k,p.x,p.y,1,{flash:p.flash>0?1:0,alpha:p.inv>0&&Math.floor(G.t/5)%2?.55:1});if(p.firing>0&&!p.dead){const q=api.socket(G),im=ART.get('gfx_muzzle_1');if(im)ART.draw(ctx,'gfx_muzzle_1',q.x,q.y,{s:.10,a:p.muzzleAim+Math.PI,ay:im.sh*.8});}}
 api.draw=function(ctx,G){const e=G.escape29,p=G.player;ctx.save();ctx.imageSmoothingEnabled=false;ctx.fillStyle='#070b12';ctx.fillRect(0,0,640,480);if(TD.Cam.shake>.3)ctx.translate(Math.sin(e.age*81)*TD.Cam.shake,Math.cos(e.age*73)*TD.Cam.shake);
  if(['ascent','blackout','emergency','hatch','hinge'].includes(e.phase)){plate(ctx,'e29_elevator',320,240,1.25);const at=e.phase==='hinge'?clamp(e.t/1.1,0,1):0;ctx.save();ctx.translate(320,405);ctx.rotate(at*Math.PI/4);plate(ctx,'e29_hatch',54,0,1,{flash:e.hatchFlash>0?1:0});ctx.restore();playerDraw(ctx,G);
   if(['emergency','hatch'].includes(e.phase)){ctx.fillStyle='rgba(200,5,9,'+(.14+.10*(1+Math.sin(e.age*7))/2)+')';ctx.fillRect(0,0,640,480);}if(e.phase==='blackout'){ctx.fillStyle='rgba(0,0,0,.98)';ctx.fillRect(0,0,640,480);}if(e.phase==='hatch'){const key=api.shootMeKey;if(key)ART.draw(ctx,key,374,367,{s:.7});else TD.OverdriveFont27.draw(ctx,'SHOOT ME!',374,367,14,'#ffe568',120);}
  }else if(e.phase==='chute'){
   const off=e.age*160%256;tiled(ctx,'e29_side_wall',-off,-256,1152,1024);ctx.save();ctx.translate(0,70);ctx.rotate(Math.PI/4);tiled(ctx,'e29_side_floor',-256+(e.age*245%256),0,1400,64);ctx.restore();
   for(const v of e.vents)plate(ctx,'e29_vent',v.x,90,1,{flash:v.t<.13?1:0});for(const u of e.drones){plate(ctx,TD.Combat29.frame('drone',u.age,true)||'e29_drone',u.x,u.y,.65,{flash:u.flash>0?1:0,alpha:u.dead?Math.max(0,1-u.deadT/.8):1});if(u.warn)plate(ctx,'pb20_icon_retina',p.x,p.y-40,.30,{alpha:.7});}playerDraw(ctx,G);
  }else{
   ctx.translate(-e.camX,0);const offset=e.camX-(e.camX*.35%256);tiled(ctx,'e29_side_wall',offset,0,1024,512);for(const [left,right,y]of[[0,800,350],[800,1510,380],[1510,3700,410]]){ctx.save();ctx.beginPath();ctx.rect(left,y,right-left,64);ctx.clip();for(let x=Math.max(left,Math.floor(e.camX/256)*256);x<Math.min(right,e.camX+900);x+=256)plate(ctx,'e29_side_floor',x,y,1,{ax:0,ay:0});ctx.restore();}
   for(const u of e.enemies){const action=u.dead?'death':u.firing>0?'fire':u.phase==='enter'?'walk':'idle',q=TD.Pixel25.seq(u.kind,action,'west')||TD.Pixel25.seq(u.kind,'idle','west'),key=q?.frames[Math.min(q.frames.length-1,u.dead?Math.floor(u.deadT*14):u.phase==='enter'?Math.floor(u.walk*16)%q.frames.length:u.firing>0?5:0)];if(key)art.draw(ctx,key,u.x,u.y,{s:u.kind==='heavy'?.8:.68,flash:u.flash>0?1:0,alpha:u.dead?Math.max(0,1-u.deadT/1.2):1});}
   for(const s of e.solids)if(!s.dead)plate(ctx,'e29_crate',s.x,s.y,s.w/pack.assets.e29_crate.bodyWidth,{flash:s.flash>0?1:0});
   for(const b of e.barrels)if(!b.dead)plate(ctx,'e29_barrel',b.x,b.y,.60,{flash:b.flash>0?1:0});
   plate(ctx,e.doorBroken?'e29_exit_open':'e29_exit',3410,410,1);playerDraw(ctx,G);
   if(e.phase==='escape'){for(let j=0;j<5;j++)ART.draw(ctx,'gfx_destruction_'+Math.floor((e.age*12+j)%6),e.blastX-35+j%2*35,150+j*62,{s:.8});ctx.fillStyle='rgba(220,35,0,.08)';ctx.fillRect(e.camX,90,640,390);}
   ctx.translate(e.camX,0);
  }
  ctx.save();ctx.translate(-e.camX,0);for(const s of e.shots)projectileDraw(ctx,s,false);for(const s of e.enemyShots)projectileDraw(ctx,s,true);for(const s of e.sparks)ART.draw(ctx,'gfx_impact_'+Math.min(5,Math.floor(s.t*32)),s.x,s.y,{s:.14});FX.draw(ctx,0);FX.draw(ctx,1);ctx.restore();
  if(!['blackout','ascent','emergency','drop'].includes(e.phase)&&!p.dead){ART.draw(ctx,'retmb_'+Math.floor(e.age*8)%4,e.cursor.x-e.camX,e.cursor.y,{s:.22});}
  if(e.phase==='drop'){ctx.fillStyle='rgba(0,0,0,'+clamp((e.t-.7)/1.1,0,1)+')';ctx.fillRect(0,0,640,480);}ctx.restore();
 };
 api.hud=function(ctx,text,G){const e=G.escape29;if(e.phase==='blackout')return true;TD.CornerHUD26.draw(ctx,text,G,false);const labels={ascent:'SERVICE ELEVATOR',emergency:'EMERGENCY POWER',hatch:'HOLD RETINA / AIM DOWN / FIRE',chute:'SHOOT DRONES / SURVIVE',corridor:'SERVICE CORRIDOR',escape:'SELF-DESTRUCT / RUN!',doorSlide:'SLIDE THROUGH!',drop:'LEVEL 4 / PRISM BASTION'};TD.OverdriveFont27.draw(ctx,labels[e.phase]||'HATCH BREACHED',320,110,11,e.phase==='escape'?'#ff7662':'#ffe092',480);
  if(['ascent','emergency','hatch'].includes(e.phase))TD.OverdriveFont27.draw(ctx,'FLOOR '+String(Math.floor(3+e.age*(e.phase==='hatch'?5:1.5))).padStart(3,'0'),320,188,9,e.phase==='ascent'?'#91eceb':'#ff8872',160);
  if(e.phase==='hatch')TD.OverdriveFont27.draw(ctx,String(Math.max(0,Math.ceil(18-e.t))).padStart(2,'0'),590,137,15,'#ff7058',50);
  if(e.phase==='chute')TD.OverdriveFont27.draw(ctx,'SURVIVE '+Math.max(0,Math.ceil(28-e.t)),320,135,10,'#9eefff',200);
  if(e.message&&e.t<6){ctx.fillStyle='rgba(2,7,16,.87)';ctx.fillRect(60,419,520,55);ART.draw(ctx,'pav_hotwire',86,447,{s:.13});const words=e.message.replace(/^HOTWIRE: /,'').split(' ');let lines=[''];for(const w of words){let at=lines.length-1;if((lines[at]+' '+w).length>59)lines.push(w);else lines[at]+=(lines[at]?' ':'')+w;}text('HOTWIRE',120,429,10,'#ffc778');lines.slice(0,2).forEach((s,i)=>text(s,120,445+i*13,9,'#fff'));}
  return true;
 };
 api.hitPlayer=hitPlayer;api.setPhase=setPhase;api.hitRect=hitRect;api.floorAt=floorAt;
 // Use the game's existing authored Shoot Me marker when present.
 api.shootMeKey=Object.keys(root.BOFX?.cells||{}).find(k=>/shoot.?me/i.test(k))||Object.keys(root.BOFX?.img||{}).find(k=>/shoot.?me/i.test(k));if(api.shootMeKey)ART.warm([api.shootMeKey]);
 A.sounds.e29_powerDown={file:'expansion/topdown/audio/escape29/power_down.wav',gain:.65,min:.25};A.sounds.e29_generator={file:'expansion/topdown/audio/escape29/generator.wav',gain:.55,min:.25};
})(window);
