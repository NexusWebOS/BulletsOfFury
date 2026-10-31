/* Fortress -> AI data center. Authored cover owns its collision and destruction.
 * Gosfer is a whole alien soldier plate; fast reflexes have a bounded cooldown. */
(function(root){
  'use strict';
  const TD=root.TD,M=TD.M,W=TD.World,FX=TD.FX,A=TD.Audio,art=TD.AssaultArt;
  const types={
    od_barrier:{hw:45,hh:13,hp:30,s:.30,art:'barrier',cover:true},
    od_wood:{hw:30,hh:25,hp:12,s:.3,art:'wood',cover:true},
    od_barrel:{hw:14,hh:12,hp:5,s:.22,art:'barrel',cover:true,explodes:true},
    od_crate:{hw:36,hh:20,hp:18,s:.32,art:'crate',cover:true},
    od_wall:{hw:19,hh:52,hp:Infinity,s:.42,art:'wall',cover:true,indestructible:true},
    od_bunker:{hw:77,hh:14,hp:Infinity,s:.64,art:'bunker',cover:true,indestructible:true},
    od_bosswall:{hw:77,hh:14,hp:48,s:1,art:'bosswall',cover:true},
    od_server:{hw:22,hh:18,hp:20,s:.34,art:'server',cover:true},
    od_relay:{hw:23,hh:20,hp:22,s:.32,art:'relay',cover:true},
  };
  const make=TD.makeStructure,hit=TD.hitStructure,draw=TD.drawStructures;
  TD.makeStructure=function(spec){const t=types[spec.kind];if(!t)return make(spec);const s=Object.assign({assault:true,dead:false,flash:0,hp:t.hp,max:t.hp,type:t,cover:t.cover},spec);s.rect=W.add({x0:s.x-t.hw,y0:s.y-t.hh,x1:s.x+t.hw,y1:s.y+t.hh,t:'b',structure:s});return s;};
  TD.hitStructure=function(G,s,dmg,ram){
    if(!s.assault)return hit(G,s,dmg,ram);if(s.dead)return false;s.flash=.12;if(s.type.indestructible)return true;s.hp-=dmg;
    if(s.hp>0)return true;s.dead=true;W.remove(s.rect);G.structuresBroken++;G.score+=150;
    FX.concrete(s.x,s.y,s.type.explodes?65:90);FX.smoke(s.x,s.y,.28,1.4);FX.debris(s.x,s.y,.22);A.play('gd_wallBreak',.6);TD.Cam.kick(3);
    for(let i=0;i<4;i++){const a=i*Math.PI/2+.35;FX.fragment('concrete_fragment',s.x,s.y,a,.1,Math.cos(a)*80,Math.sin(a)*80);}
    if(s.type.explodes){FX.boom(s.x,s.y,130,'gfx_destruction_',6);TD.blast(G,s.x,s.y,78,10,true);A.play('expB',.65);}
    if(s.kind==='od_relay'&&G.fortress){G.fortress.relays++;G.say('SECURITY RELAY OFFLINE '+G.fortress.relays+'/3',s);TD.footDrop(G,s.x,s.y,'repair');A.play('shieldBreak',.5);}
    if(s.drop)TD.footDrop(G,s.x,s.y,s.drop);return true;
  };
  const impact=TD.structureImpact;
  TD.structureImpact=function(G,shot,ax,ay,bx,by){const p=G.player,cover=p.cover,enemy=G.eshots.includes(shot);const result=impact(G,shot,ax,ay,bx,by);if(result&&enemy&&cover&&p.peekExposed&&!p.blindfire&&shot.x>=cover.rect.x0-shot.r&&shot.x<=cover.rect.x1+shot.r&&shot.y>=cover.rect.y0-shot.r&&shot.y<=cover.rect.y1+shot.r&&Math.abs(shot.x-p.x)<25)TD.hurtPlayer(G,shot.dmg,shot.x,shot.y-30,shot);return result;};
  function drawCover(ctx,s){if(TD.Combat29?.drawCover(ctx,s))return;if(s.kind==='od_bosswall'){const phase=s.dead?7:Math.min(6,Math.floor((1-s.hp/s.max)*7));art.draw(ctx,'pb19_cover_'+phase,s.x,s.y+s.type.hh,{s:1,flash:s.flash>0?s.flash/.12:0});return;}const name=s.type.art==='bunker'&&!root.TD_ASSAULT_ART.assets.od_cover_bunker?'barrier':s.type.art;art.draw(ctx,'od_cover_'+name+(s.dead?'_broken':''),s.x,s.y+s.type.hh,{s:s.type.s,flash:s.flash>0?s.flash/.12:0});}
  TD.drawStructures=function(ctx,G){draw(ctx,{...G,structures:G.structures.filter(s=>!s.assault)});for(const s of G.structures)if(s.assault)drawCover(ctx,s);};
  const robotTick=TD.unitTick,robotDraw=TD.drawRobot;
  TD.ET.odRobot={foot:'assault',wreck:'of_scout_wreck',hp:6,r:18,speed:1.25,ds:.37,score:400,vis:{range:290,half:.9},gun:'burst',cd:1.7,prefer:[100,230]};
  TD.ET.odElite={foot:'elite',wreck:'of_heavy_robot_wreck',hp:18,r:22,speed:1.65,ds:.42,score:950,vis:{range:340,half:1.3},gun:'twin',cd:1.4,prefer:[120,260]};
  // Projected torso/leg ellipse is tested against the full segment, in the
  // same lifted coordinates used by the renderer. Fast rounds cannot tunnel
  // through the visible body while only its small foot circle is hittable.
  function bodyHit(u,s,rx,ry,lift){const x=u.x,y=u.y-lift,ax=(s.x-s.vx-x)/(rx+(s.r||0)),ay=(s.y-s.vy-(s.drawLift||0)-y)/(ry+(s.r||0)),bx=(s.x-x)/(rx+(s.r||0)),by=(s.y-(s.drawLift||0)-y)/(ry+(s.r||0)),dx=bx-ax,dy=by-ay,t=M.clamp(-(ax*dx+ay*dy)/(dx*dx+dy*dy||1),0,1);return Math.hypot(ax+t*dx,ay+t*dy)<=1;}
  TD.infantryShotHit=(u,s)=>['odRobot','odElite'].includes(u.type)?bodyHit(u,s,u.type==='odElite'?25:22,u.type==='odElite'?39:34,u.type==='odElite'?38:33):null;
  TD.drawAssaultRobot=function(ctx,u,elite){let dir=Math.abs(Math.sin(u.a))>.72?(Math.sin(u.a)>0?'west':'east'):Math.cos(u.a)<0?'north':'south';if(u.drawDir&&Math.abs(Math.sin(u.a))>.62&&Math.abs(Math.sin(u.a))<.78)dir=u.drawDir;u.drawDir=dir;const strafing=!elite&&u.strafe&&dir==='south'&&root.TD_ASSAULT_ART.sequences.robot_south_strafe;const key=art.frame(strafing?'robot_south_strafe':(elite?'elite_':'robot_')+dir,(u.walkT||0)),scale=elite?.42:.37;art.draw(ctx,key,u.x+3,u.y+3,{s:scale,tint:'#000',alpha:.3});art.draw(ctx,key,u.x,u.y,{s:scale,flash:u.flash>0?1:0});};
  TD.drawRobot=function(ctx,u,type){if(type==='assault'||type==='elite')return TD.drawAssaultRobot(ctx,u,type==='elite');robotDraw(ctx,u,type);};
  TD.unitTick=function(u,G,dt){
    if(!['odRobot','odElite'].includes(u.type))return robotTick(u,G,dt);if(u.dead)return;
    const p=G.player,d=TD.ET[u.type],dist=M.dist(u.x,u.y,p.x,p.y);u.flash=Math.max(0,u.flash-dt);u.fireCd-=dt;
    if(dist>650)return;const sight=p.peekExposed?TD.footAimOrigin(p):p;u.mode='alert';u.aware=1;u.sees=!W.rayBlock(u.x,u.y,sight.x,sight.y);u.look=M.angTo(u.x,u.y,p.x,p.y);u.a=M.turnTo(u.a,u.look,.045);
    let f=[0,0];u.strafe=false;
    if(dist>175||!u.sees){f=M.fwd(u.look);if(!u.sees){const n=TD.Nav.step(TD.Nav.field(p.x,p.y,G.t/60),u.x,u.y);if(n)f=n;}}
    else if(dist>90){u.strafe=true;const side=Math.sin(G.time*.7+(u.spawnId||u.x)*.03)>=0?1:-1;f=M.fwd(u.look+side*Math.PI/2);}
    const flen=Math.hypot(f[0],f[1])||1;f=[f[0]/flen,f[1]/flen];
    const fromX=u.x,fromY=u.y;u.vx=M.lerp(u.vx||0,f[0]*d.speed,.12);u.vy=M.lerp(u.vy||0,f[1]*d.speed,.12);u.x+=u.vx;u.y+=u.vy;W.collide(u,u.r,false);
    for(const o of G.units)if(o!==u&&!o.dead){const dx=u.x-o.x,dy=u.y-o.y,dd=Math.hypot(dx,dy),gap=u.r+o.r;if(dd>0&&dd<gap){u.x+=dx/dd*(gap-dd)*.12;u.y+=dy/dd*(gap-dd)*.12;}}
    u.walkT=(u.walkT||0)+Math.min(3,Math.hypot(u.x-fromX,u.y-fromY))/75;
    if(u.sees&&dist<330&&!p.dead&&u.fireCd<=0){u.fireCd=d.cd;const a=u.look,f=M.fwd(a),elite=u.type==='odElite';for(const delta of elite?[-.09,0,.09]:[0]){const v=M.fwd(a+delta);G.eshots.push({k:elite?'laser':'mg',x:u.x+f[0]*20,y:u.y+f[1]*20,vx:v[0]*(elite?4:3.5),vy:v[1]*(elite?4:3.5),a:a+delta,dmg:1,life:100,r:4,t:0,drawLift:35});}FX.flash(u.x+f[0]*20,u.y+f[1]*20-35,a,.13);A.play('gd_soldierRifle',.35);}
  };
  function gosferPose(b){
    const lateral=b.state==='dash'||b.state==='patrol'&&Math.abs(b.vx||0)>.15;
    let bank='pb19_gosfer_walk_south',phase=0,flip=false;
    if(b.dead){bank='pb19_gosfer_death';phase=Math.floor(b.t*9);}
    else if(b.state==='dash'){bank='pb19_gosfer_dash_east';flip=b.dodge<0;phase=Math.floor((b.gait||0)*8);}
    else if(lateral){bank='pb19_gosfer_walk_east';flip=(b.vx||0)<0;phase=Math.floor((b.gait||0)*8);}
    else if(['windup','shoot','recover'].includes(b.state)){bank='pb19_gosfer_fire_south';phase=b.state==='windup'?Math.min(3,Math.floor(b.attackT/(b.attack==='breaker'?1:.65)*4)):b.state==='shoot'?4+Math.min(1,Math.floor((b.attackT||0)*14)%2):6+Math.min(1,Math.floor((b.attackT||0)*4));}
    const q=root.TD_ASSAULT_ART.sequences[bank];phase=b.dead?Math.min(q.frames.length-1,phase):phase%q.frames.length;
    return{key:q.frames[phase],flip,bank,phase};
  }
  TD.gosferSocket=function(b){const pose=TD.gosferPose(b),m=root.TD_ASSAULT_ART.assets[pose.key],pt=m.muzzle||[m.anchor[0]+30,m.anchor[1]-70];return{x:b.x+(pt[0]-m.anchor[0])*(pose.flip?-1:1),y:b.y+pt[1]-m.anchor[1]};};
  TD.gosferPose=gosferPose;
  TD.makeGosfer=function(G,x,y){
    const homeY=Math.max(230,y);const b={name:'GOSFER',x,y:homeY-140,homeY,dead:false,state:'enter',t:0,hp:260,max:260,gauge:0,a:0,flash:0,cd:.6,dodgeCd:1.4,evade:0,phase:0,phaseT:0,burst:0,burstT:0,r:22};
    b.alive=()=>!b.dead;b.hpFrac=()=>b.hp/b.max;b.aim=()=>({x:b.x,y:b.y,r:b.r});b.retinaTargets=()=>[{id:b,point:()=>b,valid:()=>!b.dead&&b.state!=='enter'}];
    b.hit=(x,y,r,dmg,shot)=>{if(b.dead||b.state==='enter'||(shot?!bodyHit(b,shot,35,58,65):Math.hypot(x-b.x,y-b.y)>b.r+r))return false;b.hp-=dmg;b.flash=.1;if(b.hp<=0){b.hp=0;b.dead=true;b.state='defeated';b.t=0;G.bossDown();G.say('GOSFER: THIS IS ONLY THE BEGINNING.',{x:400,y:260});FX.boom(b.x,b.y,110,'gfx_destruction_',6);FX.ring(b.x,b.y,.5);A.play('expBoss');}return true;};
    b.blast=(x,y,r,d)=>b.hit(x,y,r,d);
    b.tick=function(dt){
      b.t+=dt;b.flash=Math.max(0,b.flash-dt);b.shotAge=(b.shotAge||0)+dt;b.firing=Math.max(0,(b.firing||0)-dt);
      if(b.dead)return;const p=G.player;
      if(b.state==='enter'){G.fortress.doorOpen=true;b.y=M.lerp(b.y,b.homeY,.025);b.gauge=Math.min(1,b.t/2);if(b.t>3){b.state='patrol';b.t=0;b.targetX=520;b.pattern=0;A.playMusic('boss2');G.say('GOSFER / 40 WATT EXECUTIONER',p);}return;}
      b.a=M.turnTo(b.a,M.angTo(b.x,b.y,p.x,p.y),.06);b.attackT=(b.attackT||0)+dt;
      const ox=b.x,oy=b.y;
      const startAttack=()=>{b.attack=['burst','sweep','dash','breaker'][b.pattern%4];b.pattern++;b.state=b.attack==='dash'?'dash':'windup';b.attackT=0;b.volleyAim=b.a;b.dodge=b.x>400?-1:1;b.sent=0;b.volleyTarget={x:p.x,y:p.y};b.firing=0;G.say(b.attack==='breaker'?'GOSFER / COVER BREAKER':b.attack==='sweep'?'GOSFER / LASER SWEEP':b.attack==='dash'?'GOSFER / REFLEX DASH':'GOSFER / LASER BURST',p);A.play('enemyHeavyLaser',.45);};
      if(b.state==='fight')b.state='patrol';
      if(b.state==='patrol'){const dx=(b.targetX||520)-b.x;b.vx=M.lerp(b.vx||0,Math.sign(dx)*1.35,.12);b.x+=b.vx;b.y=M.lerp(b.y,b.homeY,.025);if(Math.abs(dx)<8||b.attackT>1.7)startAttack();}
      else if(b.state==='dash'){b.vx=b.dodge*4.2;b.x+=b.vx;if(b.attackT>.42){b.state='windup';b.attackT=0;b.volleyAim=b.a;}}
      else{b.vx=M.lerp(b.vx||0,0,.3);b.x+=b.vx;
        if(b.state==='windup'&&b.attackT>(b.attack==='breaker'?1:.65)){b.state='shoot';b.attackT=0;b.volleyAim=b.a;}
        if(b.state==='shoot'){
          const interval=b.attack==='breaker'?.18:.14,count=b.attack==='sweep'?7:b.attack==='breaker'?3:4;
          if(b.sent<count&&b.attackT>=b.sent*interval){b.firing=.10;b.shotAge=0;const socket=TD.gosferSocket(b),offset=b.attack==='sweep'?(b.sent-3)*.105:b.attack==='burst'?(b.sent-1.5)*.05:0,a=M.angTo(socket.x,b.y,b.volleyTarget?.x??p.x,b.volleyTarget?.y??p.y)+offset,f=M.fwd(a),heavy=b.attack==='breaker';
            G.eshots.push({k:'laser',x:socket.x,y:b.y,a,vx:f[0]*(heavy?6.1:5.2),vy:f[1]*(heavy?6.1:5.2),dmg:heavy?5:1,life:100,r:heavy?7:4,t:0,drawLift:b.y-socket.y});FX.attachedFlash(b,TD.gosferSocket,a,.11);b.sent++;A.play('enemyHeavyLaser',.45);}
          if(b.attackT>count*interval+.12){b.state='recover';b.attackT=0;}}
        else if(b.state==='recover'&&b.attackT>.55){b.state='patrol';b.attackT=0;b.targetX=b.x>400?280:520;}
      }
      b.x=M.clamp(b.x,235,565);b.y=M.clamp(b.y,195,330);W.collide(b,20,false);b.gait=(b.gait||0)+Math.hypot(b.x-ox,b.y-oy)/64;
    };
    b.drawUnder=()=>{};b.drawOver=()=>{};b.draw=function(ctx){const pose=TD.gosferPose(b);ctx.save();ctx.translate(b.x,b.y);if(pose.flip)ctx.scale(-1,1);art.draw(ctx,pose.key,4,5,{s:1,tint:'#000000',alpha:.35});art.draw(ctx,pose.key,0,0,{s:1,flash:b.flash>0?1:0,alpha:b.dead?Math.max(0,1-b.t/2):1});ctx.restore();};return b;
  };
  const unit=(x,y,elite=false)=>({type:elite?'odElite':'odRobot',x,y,a:0,wp:[[x-30,y],[x+30,y]]});
  const cover=(kind,x,y,drop)=>({kind:'od_'+kind,x,y,drop});
  const structures=[cover('barrier',365,2080),cover('wood',570,2150,'spread_shotgun'),cover('barrel',208,1990),cover('barrel',239,1990),cover('wall',235,1820),cover('crate',474,1830,'minigun'),cover('barrier',510,1650),cover('wood',290,1530,'grenades'),cover('barrel',620,1550),cover('wall',570,1370),cover('barrier',290,1220),cover('crate',540,1130,'fusion_beam'),cover('relay',230,1240),cover('relay',565,800),cover('wood',344,770,'rocket_launcher'),cover('barrier',400,620),cover('server',217,490),cover('server',583,490),cover('crate',250,395,'grenades'),cover('barrel',550,400),cover('barrier',300,310),cover('barrier',530,310)];
  const mission=TD.MISSIONS.find(m=>m.id===3);
  Object.assign(mission,{hidden:false,mode:'foot',view640:true,map:{key:'od_fortress_ground',w:800,h:2400,rects:[[0,0,68,2400,'b'],[732,0,800,2400,'b'],[68,0,732,76,'b'],[68,76,165,550,'b'],[635,76,732,550,'b']]},
    data:{title:'LEVEL 3',name:'FORTRESS / DEAD SIGNAL',brief:['DESTROY THREE RED RELAYS TO OPEN THE AI DATA CENTER.','HOLD COVER TO CROUCH. FIRE TO PEEK, RELEASE TO HIDE.','ASSAULT RIFLE IS UNLIMITED. UPGRADES CARRY AMMO.','THE NORTH BLAST DOORS CONCEAL GOSFER.'],start:{x:400,y:2290,a:Math.PI},checkpoints:[[400,1870],[400,1320],[400,680]],gates:[[400,2320],[400,1370]],bossLine:560,boss:{x:400,y:195},structures,props:[],units:[unit(430,2010),unit(590,1920),unit(170,1730),unit(460,1620),unit(335,1440),unit(655,1280),unit(400,1150),unit(190,1030,true),unit(605,935),unit(320,750,true),unit(500,660),unit(360,480)]},
    boss:TD.makeGosfer,cameraOwns:true,arcadeAssault:true,canReinforce:()=>false,canSpawnBoss:G=>G.fortress.relays>=3,
    setup(G){W.navR=10;G.fortress={doorOpen:false,relays:0,pending:G.units.map((u,i)=>({type:u.type,x:u.x,y:u.y,id:i})),arrivals:[]};G.units=[];for(const [x,y] of [[400,2140],[380,1770],[420,1490],[400,1010],[410,730],[400,365]])G.structures.push(TD.makeStructure(cover(y===365?'bosswall':'bunker',x,y)));G.structures.push(TD.makeStructure(cover('relay',190,1770)));G.pickups.push({kind:'minigun',foot:true,x:460,y:2200,t:0});},
    pre(G){const p=G.player,f=G.fortress;p.scripted=G.boss?.state==='enter';
      if(!G.boss)for(const spec of f.pending)if(!spec.entered&&p.y<spec.y+TD.VH*.72){spec.entered=true;const y=Math.min(spec.y-60,TD.Cam.y-90),u=TD.makeUnit(spec.type,M.clamp(spec.x,95,705),Math.max(90,y),{a:0});u.spawnId=spec.id;u.fireCd=1.2;G.units.push(u);f.arrivals.push({x:u.x,y:u.y,cameraY:TD.Cam.y,at:G.time});}
      if(p.scripted){const fromY=p.y;p.inv=10;p.y=M.lerp(p.y,428,.035);p.a=p.aim=Math.PI;p.moving=p.y>431;p.walkT+=1/60;if(p.moving)p.gaitPhase=((p.gaitPhase||0)+Math.abs(p.y-fromY)/96)%1;G.shots=[];G.eshots=[];}if(G.boss)p.y=Math.min(p.y,445);},
    drawFloor(ctx,G){art.draw(ctx,'od_cover_door'+(G.fortress?.doorOpen?'_open':''),400,129,{s:.65});},
    drawOver(ctx,G){const p=G.player;for(const s of G.structures)if(s.assault&&!s.dead&&s.cover&&p.y<s.y+s.type.hh&&Math.abs(p.x-s.x)<s.type.hw+18&&p.y>s.y-s.type.hh-55)drawCover(ctx,s);},
    hud(ctx,text,G){TD.infantryHUD(ctx,text,G);if(!G.boss)text(G.fortress.relays<3?'DISABLE RED RELAYS: '+G.fortress.relays+'/3':'DATA CENTER UNLOCKED / ADVANCE NORTH',TD.VW/2,72,11,'#ffd060','center');else if(G.boss.state==='enter'){text('MAINFRAME BREACH',TD.VW/2,225,18,'#ff6245','center');text('GOSFER',TD.VW/2,252,24,'#fff','center');text('40 WATT LASER RIFLE / EXTREME REFLEXES',TD.VW/2,276,11,'#8ceaff','center');}return true;},
    cam(G){if(G.boss)TD.Cam.follow(G.player.x,G.player.y,.1);else{const p=G.player,f=M.fwd(p.aim);TD.Cam.follow(p.x+f[0]*24+p.vx*12,p.y+f[1]*24+p.vy*12,.12);}},
    keys:TD.footBriefKeys,
  });
})(window);
