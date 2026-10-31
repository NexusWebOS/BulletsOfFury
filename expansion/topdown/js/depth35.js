/* Shared authored enemy roster, attack clocks and raised top-down scenery. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,A=TD.Audio,W=TD.World,C=TD.Contra34,art=TD.AssaultArt,P=root.TD_DEPTH35_ART,CP=root.TD_CONTRA34_ART;
 const D=TD.Depth35={build:P.build,attacks:{},rolls:0,draws:0};
 const roles={rifle:'machine_gunner',heavy:'minigunner',laser:'sniper',rocket:'rocket_launcher',shotgun:'shotgunner',double:'double_barrel',roller:'roller_alien',flame:'flamethrower',flyer:'flying_alien',bat:'bat_drone'};
 D.profiles={
  rifle:{hp:10,cd:2.1,wind:.28,count:3,gap:.13,fan:[0],speed:340,cue:'gd_soldierRifle',shot:'mg'},
  heavy:{hp:26,cd:2.6,wind:.65,count:8,gap:.10,fan:[0],speed:360,cue:'gd_soldierRifle',shot:'mg'},
  laser:{hp:12,cd:2.6,wind:.7,count:1,gap:.1,fan:[0],speed:480,cue:'enemyHeavyLaser',shot:'laser'},
  rocket:{hp:16,cd:3,wind:.65,count:1,gap:.1,fan:[0],speed:230,cue:'missileLaunch',shot:'rocket'},
  shotgun:{hp:14,cd:2.7,wind:.5,count:1,gap:.1,fan:[-.18,-.09,0,.09,.18],speed:330,cue:'gd_tankCannon',shot:'pellet',reload:'reload_pump'},
  double:{hp:18,cd:3.1,wind:.55,count:2,gap:.32,fan:[-.21,-.14,-.07,0,.07,.14,.21],speed:350,cue:'gd_tankCannon',shot:'double_pellet',reload:'reload_break_action'},
  roller:{hp:16,cd:2.25,wind:.38,count:3,gap:.16,fan:[0],speed:310,cue:'enemyHeavyLaser',shot:'acid'},
  flame:{hp:19,cd:2.8,wind:.55,count:7,gap:.12,fan:[-.06,0,.06],speed:230,cue:'firewallLaunch',shot:'flame'},
  flyer:{hp:12,cd:2.3,wind:.45,count:3,gap:.18,fan:[-.07,.07],speed:290,cue:'enemyHeavyLaser',shot:'plasma'},
  bat:{hp:8,cd:2.4,wind:.45,count:2,gap:.18,fan:[-.1,.1],speed:300,cue:'enemyHeavyLaser',shot:'acid'}
 };
 D.role=u=>u.contraRole||roles[u.kind35||u.kind]||'machine_gunner';C.role=D.role;
 const at=(q,t,loop=q?.loop)=>q?.frames[loop?Math.floor(Math.max(0,t)*q.fps)%q.frames.length:Math.min(q.frames.length-1,Math.floor(Math.max(0,t)*q.fps))];
 const seq=(role,a)=>P.sequences['d35_'+role+'_'+a];
 const frontClip=(role,a)=>C.clip('front',role,role==='flamethrower'&&a==='fire_forward'?'flame_burst':a)||C.clip('front',role,'hover');
 const state=(u,a)=>{u.action35=a;u.actionT35=0;};
 D.attack=function(u,dt,allow,emit){
  const kind=u.kind35||u.kind,d=D.profiles[kind];if(!d)return;
  u.actionT35=(u.actionT35||0)+dt;u.firing=Math.max(0,(u.firing||0)-dt);u.fireAge34=(u.fireAge34||0)+dt;
  if(!u.attack35)u.attack35={phase:'wait',t:u.fireCd??.8};const a=u.attack35;
  if(a.phase==='wait'){a.t-=dt;if(a.t<=0&&allow){a.phase='wind';a.t=d.wind;state(u,'draw_forward');u.warn=d.wind;const p=TD.game.player;u.target35={x:p.x,y:p.y-(p.sideScroll?(p.prone?13:48):0)};}}
  else if(a.phase==='wind'){a.t-=dt;u.warn=Math.max(0,a.t);if(!allow){a.phase='wait';a.t=.3;state(u,'idle');return;}if(a.t<=0){a.phase='burst';a.t=0;a.sent=0;}}
  if(a.phase==='burst'){
   if(!allow){a.phase='wait';a.t=.45;state(u,'idle');return;}
   a.t-=dt;if(a.t<=0){if(a.sent===0){state(u,'fire_forward');u.fireT=0;u.fireAge34=0;const q=frontClip(D.role(u),'fire_forward');u.fireLength35=q?q.frames.length/q.fps:.5;}u.firing=Math.max(u.firing||0,(u.fireLength35||.5)-u.actionT35);
    for(const off of d.fan)emit(d.shot,off,d.speed,a.sent);A.play(d.cue,.35);D.attacks[kind]=(D.attacks[kind]||0)+1;a.sent++;a.t=d.gap;
    if(a.sent>=d.count){a.phase='recover';a.t=d.cd;u.recoverDuration35=Math.max(.4,d.cd-u.firing);}
   }
  }else if(a.phase==='recover'){a.t-=dt;if(u.firing<=0&&d.reload&&u.action35!==d.reload)state(u,d.reload);else if(u.firing<=0&&!d.reload&&u.action35==='fire_forward')state(u,'idle');if(a.t<=0){a.phase='wait';a.t=0;}}
 };
 function actionClip(u,side,tag='side'){
  const role=D.role(u),roll=u.rollState35;
  if(roll){const action={fold:'transform_to_ball',rolling:'ball_roll',unfold:'transform_to_humanoid'}[roll];return {q:C.clip('side',role,action,side),t:u.rollT35,loop:roll==='rolling'};}
  const moving=u.phase==='enter'||u.phase==='rush'||u.moving35,air=role==='flying_alien',act=u.phase==='vault'?'jump':moving?'walk':u.firing>0?'fire':'idle';
  const q=C.clip(tag,role,air?(u.firing>0?'fly_fire':'fly'):act,side);
  return {q,t:moving?(u.walk||u.walkT||0):u.firing>0?(u.fireAge34||0):u.age||0,loop:act!=='jump'};
 }
 C.sidePose=function(u,G){const role=D.role(u),side=u.x<G.player.x?'east':'west',c=actionClip(u,side);if(c.q)return{key:at(c.q,c.t,c.loop),s:CP.roles[role].sideScale,side};const q=C.clip('front',role,u.firing>0?'fire_forward':'draw_forward')||seq(role,'hover');return{key:at(q,u.actionT35||u.age||0,true),s:CP.roles[role].frontScale*.7,side};};
 C.sideBody=function(u,G){const z=C.sidePose(u,G),m=TD_ASSAULT_ART.assets[z.key],b=m.bounds;return{x:u.x+((b[0]+b[2])/2-m.anchor[0])*z.s,y:u.y+((b[1]+b[3])/2-m.anchor[1])*z.s,rx:Math.max(12,Math.min(29,(b[2]-b[0])*z.s*.36)),ry:Math.max(10,(b[3]-b[1])*z.s*.43)};};
 const oldFront=C.frontPose;C.frontPose=function(u){
  const role=D.role(u);if(!roles[u.kind])return oldFront(u);
  if(u.rollState35){const a={fold:'fold_to_ball',rolling:'ball_roll',unfold:'unfold_to_humanoid'}[u.rollState35];return at(seq(role,a),u.rollT35,u.rollState35==='rolling');}
  if(['enter','rush','vault','flank'].includes(u.phase)){
   const side=(u.toX??u.homeX??320)<320?'west':'east',a=u.phase==='vault'?'jump':u.phase==='rush'?'run':u.phase==='flank'?(u.firing>0?'fire':'idle'):'walk',q=C.clip('side',role,a,u.phase==='flank'?(u.x<320?'east':'west'):side);
   if(q)return at(q,u.phase==='vault'?u.vaultT:u.phase==='flank'?u.fireAge34||0:(u.gait||0)*.7,u.phase!=='vault');
  }
  const q=frontClip(role,u.action35)||frontClip(role,u.firing>0?'fire_forward':'draw_forward')||seq(role,'hover');
  const reload=['reload_pump','reload_break_action'].includes(u.action35),t=reload?u.actionT35/Math.max(.1,u.recoverDuration35)*(q.frames.length/q.fps):u.action35==='idle'?0:u.actionT35||0;
  return at(q,t,false);
 };
 D.frontAttack=(G,u,dt,allow,bullet,socket)=>D.attack(u,dt,allow,(kind,off)=>{const q=socket(u),before=G.bastion.enemyShots.length;bullet(G,q.x,q.y,kind,0,u.phase==='flank');const s=G.bastion.enemyShots[before];s.tx=M.clamp((u.target35?.x??s.tx)+Math.tan(off)*400,10,630);s.contra35=true;s.hitsProne=kind==='acid'||kind==='flame';s.duration=kind==='rocket'?.85:kind==='laser'?.42:kind==='flame'?.68:.58;});
 D.frontManeuver=function(G,u,dt){
  if(u.kind!=='roller')return false;u.rollCd35=(u.rollCd35??3)-dt;
  if(!u.rollState35&&u.phase==='peek'&&u.rollCd35<=0&&u.attack35?.phase!=='burst'){u.rollState35='fold';u.rollT35=0;u.firing=0;u.attack35={phase:'wait',t:.6};u.fromX35=u.x;u.toX35=u.x<320?Math.min(530,u.x+180):Math.max(110,u.x-180);D.rolls++;}
  if(!u.rollState35)return false;u.rollT35+=dt;u.duck=0;
  if(u.rollState35==='fold'&&u.rollT35>.76){u.rollState35='rolling';u.rollT35=0;}
  if(u.rollState35==='rolling'){const t=M.clamp(u.rollT35/.8,0,1);u.x=M.lerp(u.fromX35,u.toX35,t);if(t===1){u.rollState35='unfold';u.rollT35=0;}}
  if(u.rollState35==='unfold'&&u.rollT35>.76){u.rollState35=null;u.rollCd35=5.4;u.phase='peek';u.phaseT=0;u.cycles=0;u.cover={x:u.x,y:285,hp:0,max:1};}
  return true;
 };
 D.sideStep=function(G,u,dt){
  const e=G.escape29,p=G.player,d=D.profiles[u.kind];u.age+=dt;u.flash=Math.max(0,u.flash-dt);if(u.dead){u.deadT+=dt;return;}
  u.y=TD.Escape29.floorAt(u.x);u.moving35=false;
  if(u.phase==='enter'){const v=Math.sign(u.homeX-u.x)*Math.min(105*dt,Math.abs(u.homeX-u.x));u.x+=v;u.walk+=Math.abs(v)/105;if(Math.abs(u.x-u.homeX)<2)u.phase='fight';return;}
  u.rollCd35=(u.rollCd35??2.4)-dt;
  if(u.kind==='roller'&&u.rollCd35<=0&&!u.rollState35&&u.attack35?.phase!=='burst'){u.rollState35='fold';u.rollT35=0;u.rollDir35=Math.sign(p.x-u.x)||-1;u.attack35={phase:'wait',t:.5};D.rolls++;}
  if(u.rollState35){u.rollT35+=dt;if(u.rollState35==='fold'&&u.rollT35>.95){u.rollState35='rolling';u.rollT35=0;}if(u.rollState35==='rolling'){const x=u.x+u.rollDir35*250*dt,blocked=e.solids.some(s=>!s.dead&&Math.abs(s.x-x)<s.w/2+14);if(!blocked)u.x=x;if(u.rollT35>.72||blocked){u.rollState35='unfold';u.rollT35=0;}if(Math.abs(u.x-p.x)<24&&p.y>u.y-24)TD.Escape29.hitPlayer(G);}if(u.rollState35==='unfold'&&u.rollT35>.95){u.rollState35=null;u.rollCd35=4.4;}return;}
  const visible=u.x>e.camX-24&&u.x<e.camX+640/C.view(G).z+24;
  D.attack(u,dt,visible&&Math.abs(u.x-p.x)<580&&!p.dead,(kind,off,speed)=>{const q=C.sideSocket(u,G),target=u.target35||{x:p.x,y:p.y-48},a=M.angTo(q.x,q.y,target.x,target.y)+off,v=M.fwd(a);e.enemyShots.push({x:q.x,y:q.y,px:q.x,py:q.y,vx:v[0]*speed,vy:v[1]*speed,a,kind,life:kind==='flame'?1:3,owner:u,contra35:true});});
 };
 const FXIDS={mg:'bullet_front',laser:'sniper_front',rocket:'rocket_front',pellet:'pellets_front',double_pellet:'double_pellets_front',acid:'acid_front',plasma:'plasma_front',flame:'flame_front',orb:'prism_front'};
 const oldFrontShot=C.frontShot;C.frontShot=function(ctx,s){if(!FXIDS[s.kind])return oldFrontShot(ctx,s);if(s.t<0)return true;const q=C.clip('fx',FXIDS[s.kind],'flight'),f=M.clamp(s.t/s.duration,0,.999),k=q.frames[Math.floor(f*q.frames.length)],m=TD_ASSAULT_ART.assets[k],size=(s.kind==='flame'?18:10)+f*(s.kind==='flame'?22:12);art.draw(ctx,k,s.x,s.y,{s:size/Math.max(m.bounds[2]-m.bounds[0],m.bounds[3]-m.bounds[1])});return true;};
 D.drawShot=function(ctx,s,lift=0){const q=C.clip('fx',FXIDS[s.kind||s.attackKind35]||'bullet_front','flight'),k=at(q,(s.t||s.life||0)*.1,true),m=TD_ASSAULT_ART.assets[k],size=(s.kind||s.attackKind35)==='flame'?22:(s.kind||s.attackKind35)==='rocket'?19:12;art.draw(ctx,k,s.x,s.y-lift,{s:size/Math.max(m.bounds[2]-m.bounds[0],m.bounds[3]-m.bounds[1])});};
 // The overhead route uses the same roster; arrivals still come from beyond its top edge.
 const mission=TD.MISSIONS.find(m=>m.id===3),setup=mission.setup,makeUnit=TD.makeUnit;
 for(const [kind,d] of Object.entries(D.profiles))TD.ET['c35_'+kind]={...TD.ET.odRobot,hp:d.hp,r:kind==='heavy'?22:18,score:kind==='heavy'?900:550};
 TD.makeUnit=function(type,...args){const u=makeUnit(type,...args);if(type.startsWith('c35_')){u.kind35=type.slice(4);u.contraRole=roles[u.kind35];u.attack35={phase:'wait',t:1.2};u.phase='fight';u.age=0;}return u;};
 mission.setup=function(G){setup(G);const roster=['rifle','shotgun','double','roller','rocket','heavy','flyer','flame','laser','roller','bat','double'];G.fortress.pending.forEach((s,i)=>s.type='c35_'+roster[i%roster.length]);};
 D.groundPose=function(u){const role=D.role(u),side=Math.sin(u.a)<0?'east':'west',c=actionClip(u,side),low=u.rollState35;
  if((u.moving35||low)&&c.q)return{key:at(c.q,c.t,c.loop),s:CP.roles[role].sideScale*.78};
  const facing=TD.AssaultArt.direction(u.a).replace('south','south-').replace('north','north-').replace(/-$/,'');
  if(u.action35&&u.action35!=='idle'&&Math.cos(u.a)>-.25){const q=frontClip(role,u.action35);if(q)return{key:at(q,u.actionT35,false),s:CP.roles[role].frontScale*.55};}
  const q=seq(role,'idle_'+facing)||seq(role,'hover');if(q){const k=at(q,u.age,true);return{key:k,s:P.assets[k].drawScale*.55};}
  const k=C.frontPose({...u,kind:u.kind35,phase:'peek'});return{key:k,s:CP.roles[role].frontScale*.55};
 };
 D.groundBody=function(u){const z=D.groundPose(u),m=TD_ASSAULT_ART.assets[z.key],b=m.bounds;return{x:u.x+((b[0]+b[2])/2-m.anchor[0])*z.s,y:u.y+((b[1]+b[3])/2-m.anchor[1])*z.s,rx:Math.max(10,(b[2]-b[0])*z.s*.36),ry:Math.max(10,(b[3]-b[1])*z.s*.45)};};
 D.groundSocket=function(u){const z=D.groundPose(u),m=TD_ASSAULT_ART.assets[z.key];return{x:u.x+(m.muzzle[0]-m.anchor[0])*z.s,y:u.y+(m.muzzle[1]-m.anchor[1])*z.s};};
 const unitTick=TD.unitTick;TD.unitTick=function(u,G,dt){if(!u.kind35)return unitTick(u,G,dt);if(u.dead)return;u.age+=dt;u.flash=Math.max(0,u.flash-dt);const p=TD.Combat39?.target(u,G)||G.player,d=D.profiles[u.kind35],dist=M.dist(u.x,u.y,p.x,p.y);if(dist>660)return;
  u.look=M.angTo(u.x,u.y,p.x,p.y);u.a=M.turnTo(u.a,u.look,.08);u.sees=!W.rayBlock(u.x,u.y,p.x,p.y)&&(TD.Combat39?.canSee(u,G)??true);u.aware=1;u.mode='alert';
  u.rollCd35=(u.rollCd35??3)-dt;
  if(u.kind35==='roller'&&u.rollCd35<=0&&u.sees&&!u.rollState35&&dist<330){u.rollState35='fold';u.rollT35=0;u.rollAim35=u.look;u.attack35={phase:'wait',t:.5};D.rolls++;}
  const ox=u.x,oy=u.y;let f=[0,0],speed=78;
  if(u.rollState35){u.rollT35+=dt;if(u.rollState35==='fold'&&u.rollT35>.95){u.rollState35='rolling';u.rollT35=0;}if(u.rollState35==='rolling'){f=M.fwd(u.rollAim35);speed=240;if(u.rollT35>.7){u.rollState35='unfold';u.rollT35=0;}if(dist<28)TD.hurtPlayer(G,1,u.x,u.y,{hitsProne:true});}if(u.rollState35==='unfold'&&u.rollT35>.95){u.rollState35=null;u.rollCd35=5;}}
  else if(dist>(['shotgun','double','flame'].includes(u.kind35)?145:210)||!u.sees){f=M.fwd(u.look);if(!u.sees)f=TD.Nav.step(TD.Nav.field(p.x,p.y,G.t/60),u.x,u.y)||f;}
  else if(u.attack35?.phase==='wait'&&dist>100){f=M.fwd(u.look+(Math.sin(u.age*.7+u.spawnId)>=0?1:-1)*Math.PI/2);speed=48;}
  const n=Math.hypot(...f)||1;u.x+=f[0]/n*speed*dt;u.y+=f[1]/n*speed*dt;W.collide(u,u.r,false);u.vx=u.x-ox;u.vy=u.y-oy;u.moving35=Math.hypot(u.vx,u.vy)>.05;u.walk=(u.walk||0)+Math.hypot(u.vx,u.vy)/100;
  if(!u.rollState35)D.attack(u,dt,u.sees&&dist<365&&!p.dead,(kind,off,velocity)=>{const q=D.groundSocket(u),target=u.target35||p,a=M.angTo(q.x,u.y,target.x,target.y)+off,v=M.fwd(a),life=kind==='flame'?55:120;G.eshots.push({k:kind==='laser'?'laser':'mg',attackKind35:kind,contra35:true,x:q.x,y:u.y,vx:v[0]*velocity/60,vy:v[1]*velocity/60,a,dmg:1,life,r:kind==='flame'?7:4,t:0,drawLift:u.y-q.y,liftStart:u.y-q.y,liftEnd:TD.footLift(G.player),spawnX:q.x,spawnY:u.y,flightDist:Math.hypot(target.x-q.x,target.y-u.y),hitsProne:kind==='acid'||kind==='flame'});TD.FX.attachedFlash(u,()=>D.groundSocket(u),a,.1);});
 };
 const robot=TD.drawAssaultRobot;TD.drawAssaultRobot=function(ctx,u,elite){if(!u.kind35)return robot(ctx,u,elite);const z=D.groundPose(u);art.draw(ctx,z.key,u.x,u.y,{s:z.s,flash:u.flash>0?1:0});D.draws++;};
 const bodyHit=TD.infantryShotHit;TD.infantryShotHit=function(u,s){if(!u.kind35)return bodyHit(u,s);const b=D.groundBody(u),lift=TD.projectileLift(s),x0=(s.x-s.vx-b.x)/(b.rx+(s.r||0)),y0=(s.y-s.vy-lift-b.y)/(b.ry+(s.r||0)),dx=s.vx/(b.rx+(s.r||0)),dy=s.vy/(b.ry+(s.r||0)),t=M.clamp(-(x0*dx+y0*dy)/(dx*dx+dy*dy||1),0,1);return Math.hypot(x0+dx*t,y0+dy*t)<=1;};
 const drawShot=TD.drawShot;TD.drawShot=function(ctx,s,enemy){if(s.contra35)return D.drawShot(ctx,s,TD.projectileLift(s));return drawShot(ctx,s,enemy);};
 // A common body unit per authored stance bank, never a resize-to-fit per frame.
 const pose=TD.footPose;TD.footPose=function(p){const z=pose(p);if(p.pilot!=='yuri'||p.pseudo3D)return z;const k=z.key||'';let f=1;
  if(!p.dead&&!p.action&&!p.cover&&!p.roll&&!p.jump&&!(p.stanceTransition?.t<.46)&&Math.abs(Math.sin(p.aim))>.72&&['crouch','prone'].includes(p.stance)){
   const side=Math.sin(p.aim)<0?'east':'west',bank='e29_'+(p.stance==='prone'?'prone_':'crouch_')+side,q=TD_ESCAPE29_ART.sequences[bank],t=p.moving?(p.gaitPhase||0)*q.frames.length/q.fps:p.stance==='prone'?.9:0,key=at(q,t,!!p.moving);if(key)return{key,scale:1,angle:0,action:p.stance,dir:side};
  }
  if(k.startsWith('pb19_yuri_')&&(/crawl|prone_fire/.test(k)))f=.76;
  return f===1?z:{...z,scale:z.scale*f};
 };
 const drawFoot=TD.drawFoot;TD.drawFoot=function(ctx,p,o){if(p.pilot!=='yuri'||p.pseudo3D)return drawFoot(ctx,p,o);const z=TD.footPose(p);ctx.save();ctx.imageSmoothingEnabled=false;art.draw(ctx,z.key,p.x,p.y-(p.jumpZ||0),{s:z.scale,flash:o?.flash||0,alpha:p.dead?.65:1});ctx.restore();};
 // These plates have visible top planes and fixed collision footprints.
 mission.map.key='d35_ground';
 D.coverPose=function(s){const name=s.kind==='od_bosswall'?'bunker':s.kind.slice(3),phase=s.dead?3:!Number.isFinite(s.max)?0:s.hp/s.max<.34?2:s.hp/s.max<.7?1:0,key='d35_'+name+'_'+phase,m=P.assets[key];return m?{key,s:s.type.hw*2/P.assets['d35_'+name+'_0'].bodyWidth}:null;};
 D.drawCover=function(ctx,s){const z=D.coverPose(s);if(!z)return false;art.draw(ctx,z.key,s.x,s.y+s.type.hh,{s:z.s,flash:s.flash>0?1:0});return true;};
 const cover=TD.Combat29.drawCover;TD.Combat29.drawCover=(ctx,s)=>D.drawCover(ctx,s)||cover(ctx,s);
 D.drawActors=function(ctx,G){const objects=G.structures.map(s=>({y:s.y+(s.type?.hh||0),draw:()=>s.assault?D.drawCover(ctx,s):TD.drawStructures(ctx,{...G,structures:[s]})}));for(const u of G.units)if(Math.abs(u.y-TD.Cam.y)<560)objects.push({y:u.y,draw:()=>TD.drawUnit(ctx,u)});if(G.boss)objects.push({y:G.boss.y,draw:()=>G.boss.draw(ctx,G.t/60)});const p=G.player;objects.push({y:p.y,draw:()=>TD.drawFoot(ctx,p,{flash:p.inv>0&&Math.floor(p.inv/4)%2?1:0})});objects.sort((a,b)=>a.y-b.y).forEach(o=>o.draw());};
 mission.drawOver=function(){};
 const floor=mission.drawFloor;mission.drawFloor=function(ctx,G){floor(ctx,G);for(const x of [49,751])for(let y=Math.max(120,Math.floor(TD.Cam.y/112)*112);y<TD.Cam.y+TD.VH/TD.Cam.zoom+150&&y<2400;y+=112)art.draw(ctx,'d35_wall_0',x,y,{s:.82});};
 ART.warm(Object.keys(P.assets));
})(window);
