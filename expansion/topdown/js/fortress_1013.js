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
    od_wall:{hw:19,hh:52,hp:45,s:.42,art:'wall',cover:true},
    od_server:{hw:22,hh:18,hp:20,s:.34,art:'server',cover:true},
    od_relay:{hw:23,hh:20,hp:22,s:.32,art:'relay',cover:true},
  };
  const make=TD.makeStructure,hit=TD.hitStructure,draw=TD.drawStructures;
  TD.makeStructure=function(spec){const t=types[spec.kind];if(!t)return make(spec);const s=Object.assign({assault:true,dead:false,flash:0,hp:t.hp,max:t.hp,type:t,cover:t.cover},spec);s.rect=W.add({x0:s.x-t.hw,y0:s.y-t.hh,x1:s.x+t.hw,y1:s.y+t.hh,t:'b',structure:s});return s;};
  TD.hitStructure=function(G,s,dmg,ram){
    if(!s.assault)return hit(G,s,dmg,ram);if(s.dead)return false;s.hp-=dmg;s.flash=.12;
    if(s.hp>0)return true;s.dead=true;W.remove(s.rect);G.structuresBroken++;G.score+=150;
    FX.concrete(s.x,s.y,s.type.explodes?65:90);FX.smoke(s.x,s.y,.28,1.4);FX.debris(s.x,s.y,.22);A.play('gd_wallBreak',.6);TD.Cam.kick(3);
    for(let i=0;i<4;i++){const a=i*Math.PI/2+.35;FX.fragment('concrete_fragment',s.x,s.y,a,.1,Math.cos(a)*80,Math.sin(a)*80);}
    if(s.type.explodes){FX.boom(s.x,s.y,130,'gfx_destruction_',6);TD.blast(G,s.x,s.y,78,10,true);A.play('expB',.65);}
    if(s.kind==='od_relay'&&G.fortress){G.fortress.relays++;G.say('SECURITY RELAY OFFLINE '+G.fortress.relays+'/3',s);TD.footDrop(G,s.x,s.y,'repair');A.play('shieldBreak',.5);}
    if(s.drop)TD.footDrop(G,s.x,s.y,s.drop);return true;
  };
  const impact=TD.structureImpact;
  TD.structureImpact=function(G,shot,ax,ay,bx,by){const p=G.player,cover=p.cover,hp=cover?.hp,enemy=G.eshots.includes(shot);const result=impact(G,shot,ax,ay,bx,by);if(result&&enemy&&cover&&cover.hp!==hp&&p.peekExposed&&cover.type.art!=='wall')TD.hurtPlayer(G,shot.dmg,shot.x,shot.y-30);return result;};
  function drawCover(ctx,s){art.draw(ctx,'od_cover_'+s.type.art+(s.dead?'_broken':''),s.x,s.y+s.type.hh,{s:s.type.s,flash:s.flash>0?s.flash/.12:0});}
  TD.drawStructures=function(ctx,G){draw(ctx,{...G,structures:G.structures.filter(s=>!s.assault)});for(const s of G.structures)if(s.assault)drawCover(ctx,s);};
  const robotTick=TD.unitTick,robotDraw=TD.drawRobot;
  TD.ET.odRobot={foot:'assault',wreck:'of_scout_wreck',hp:6,r:13,speed:1.25,ds:.32,score:400,vis:{range:290,half:.9},gun:'burst',cd:1.7,prefer:[100,230]};
  TD.ET.odElite={foot:'elite',wreck:'of_heavy_robot_wreck',hp:18,r:16,speed:1.65,ds:.36,score:950,vis:{range:340,half:1.3},gun:'twin',cd:1.4,prefer:[120,260]};
  TD.drawAssaultRobot=function(ctx,u,elite){const dir=Math.abs(Math.sin(u.a))>.65?(Math.sin(u.a)>0?'west':'east'):Math.cos(u.a)<0?'north':'south';const key=art.frame((elite?'elite_':'robot_')+dir,(u.walkT||0));art.draw(ctx,key,u.x+3,u.y+3,{s:elite?.36:.32,tint:'#000',alpha:.3});art.draw(ctx,key,u.x,u.y,{s:elite?.36:.32,flash:u.flash>0?1:0});};
  TD.drawRobot=function(ctx,u,type){if(type==='assault'||type==='elite')return TD.drawAssaultRobot(ctx,u,type==='elite');robotDraw(ctx,u,type);};
  TD.unitTick=function(u,G,dt){
    if(!['odRobot','odElite'].includes(u.type))return robotTick(u,G,dt);if(u.dead)return;
    const p=G.player,d=TD.ET[u.type],dist=M.dist(u.x,u.y,p.x,p.y);u.flash=Math.max(0,u.flash-dt);u.fireCd-=dt;
    if(dist>480)return;const sight=p.peekExposed?TD.footAimOrigin(p):p;u.mode='alert';u.aware=1;u.sees=!W.rayBlock(u.x,u.y,sight.x,sight.y);u.look=M.angTo(u.x,u.y,p.x,p.y);u.a=u.look;
    if(dist>145||!u.sees){let f=M.fwd(u.look);if(!u.sees){const n=TD.Nav.step(TD.Nav.field(p.x,p.y,G.t/60),u.x,u.y);if(n)f=n;}
      u.x+=f[0]*d.speed;u.y+=f[1]*d.speed;u.walkT=(u.walkT||0)+dt;W.collide(u,u.r,false);}
    if(u.sees&&dist<330&&!p.dead&&u.fireCd<=0){u.fireCd=d.cd;const a=u.look,f=M.fwd(a),elite=u.type==='odElite';for(const delta of elite?[-.09,0,.09]:[0]){const v=M.fwd(a+delta);G.eshots.push({k:elite?'laser':'mg',x:u.x+f[0]*20,y:u.y+f[1]*20,vx:v[0]*(elite?4:3.5),vy:v[1]*(elite?4:3.5),a:a+delta,dmg:1,life:100,r:4,t:0,drawLift:35});}FX.flash(u.x+f[0]*20,u.y+f[1]*20-35,a,.13);A.play('gd_soldierRifle',.35);}
  };
  TD.makeGosfer=function(G,x,y){
    const b={name:'GOSFER',x,y:y-140,homeY:y,dead:false,state:'enter',t:0,hp:260,max:260,gauge:0,a:0,flash:0,cd:.6,dodgeCd:1.4,evade:0,phase:0,phaseT:0,burst:0,burstT:0,r:22};
    b.alive=()=>!b.dead;b.hpFrac=()=>b.hp/b.max;b.aim=()=>({x:b.x,y:b.y,r:b.r});b.retinaTargets=()=>[{id:b,point:()=>b,valid:()=>!b.dead&&b.state!=='enter'}];
    b.hit=(x,y,r,dmg)=>{if(b.dead||b.state==='enter'||Math.hypot(x-b.x,y-b.y)>b.r+r)return false;b.hp-=dmg;b.flash=.1;if(b.hp<=0){b.hp=0;b.dead=true;b.state='defeated';b.t=0;G.bossDown();G.say('GOSFER: THIS IS ONLY THE BEGINNING.',{x:400,y:260});FX.boom(b.x,b.y,110,'gfx_destruction_',6);FX.ring(b.x,b.y,.5);A.play('expBoss');}return true;};
    b.blast=(x,y,r,d)=>b.hit(x,y,r,d);
    b.tick=function(dt){
      b.t+=dt;b.flash=Math.max(0,b.flash-dt);if(b.dead){if(b.t<1.5&&G.t%12===0)FX.smoke(b.x,b.y,.18,.8);return;}
      const p=G.player;
      if(b.state==='enter'){G.fortress.doorOpen=true;b.y=M.lerp(b.y,b.homeY,.025);b.gauge=Math.min(1,b.t/2);if(G.t%15===0&&b.t<1.7){const dx=G.t%30?-105:105;FX.boom(400+dx,110,110,'gfx_destruction_',6);FX.concrete(400+dx,130,85);TD.Cam.kick(3);}if(b.t>3){b.state='fight';b.t=0;A.playMusic('boss2');G.say('GOSFER - 40 WATT EXECUTIONER',p);}return;}
      b.a=M.angTo(b.x,b.y,p.x,p.y);b.phaseT+=dt;b.dodgeCd-=dt;b.cd-=dt;
      if(b.phaseT>3){b.phase=(b.phase+1)%3;b.phaseT=0;}
      if(b.dodgeCd<=0&&G.shots.some(s=>Math.hypot(s.x-b.x,s.y-b.y)<110)){b.dodgeCd=2.1;b.evade=.24;b.dodge=b.x>400?-1:1;A.play('stylishDodge',.4);}
      if(b.evade>0){b.evade-=dt;b.x+=b.dodge*6.2;}
      else{b.x+=Math.cos(G.time*1.4)*(b.phase===1?2.5:1.25);b.y=M.lerp(b.y,b.homeY+Math.sin(G.time*.7)*55,.035);}
      b.x=M.clamp(b.x,235,565);b.y=M.clamp(b.y,150,330);W.collide(b,20,false);
      if(!p.dead&&b.cd<=0&&b.evade<=0){b.cd=b.phase===2?2.5:1.5;b.burst=b.phase===2?7:4;b.burstT=0;b.volleyAim=b.a;A.play('enemyHeavyLaser',.65);}
      if(b.burst>0&&(b.burstT-=dt)<=0){const n=b.burst--;b.burstT=.12;const spread=b.phase===2?(n-3)*.105:Math.sin(n)*.075;const a=b.volleyAim+spread,f=M.fwd(a);G.eshots.push({k:'laser',x:b.x+f[0]*27,y:b.y+f[1]*27,a,vx:f[0]*5.3,vy:f[1]*5.3,dmg:1,life:100,r:5,t:0,drawLift:40});FX.flash(b.x+f[0]*27,b.y+f[1]*27-40,a,.2);b.firing=.12;}
      b.firing=Math.max(0,(b.firing||0)-dt);
    };
    b.drawUnder=()=>{};b.drawOver=()=>{};b.draw=function(ctx){const dir=Math.abs(Math.sin(b.a))>.7?(Math.sin(b.a)>0?'west':'east'):(Math.cos(b.a)<0?'north':'south');const frame=b.dead?5:b.evade>0?4:b.firing>0?3:1+Math.floor(G.time*9)%2;art.draw(ctx,'od_gosfer_'+dir+'_'+frame,b.x+4,b.y+5,{s:.45,tint:'#000000',alpha:.35});art.draw(ctx,'od_gosfer_'+dir+'_'+frame,b.x,b.y,{s:.45,flash:b.flash>0?1:0,alpha:b.dead?Math.max(0,1-b.t/2):1});};return b;
  };
  const unit=(x,y,elite=false)=>({type:elite?'odElite':'odRobot',x,y,a:0,wp:[[x-30,y],[x+30,y]]});
  const cover=(kind,x,y,drop)=>({kind:'od_'+kind,x,y,drop});
  const structures=[cover('barrier',365,2080),cover('wood',570,2150,'spread_shotgun'),cover('barrel',208,1990),cover('barrel',239,1990),cover('wall',235,1820),cover('crate',474,1830,'minigun'),cover('barrier',510,1650),cover('wood',290,1530,'grenades'),cover('barrel',620,1550),cover('wall',570,1370),cover('barrier',290,1220),cover('crate',540,1130,'fusion_beam'),cover('relay',230,1240),cover('relay',565,800),cover('wood',344,770,'rocket_launcher'),cover('barrier',400,620),cover('server',217,490),cover('server',583,490),cover('crate',250,395,'grenades'),cover('barrel',550,400),cover('barrier',300,310),cover('barrier',530,310)];
  const mission=TD.MISSIONS.find(m=>m.id===3);
  Object.assign(mission,{hidden:false,mode:'foot',view640:true,map:{key:'od_fortress_ground',w:800,h:2400,rects:[[0,0,68,2400,'b'],[732,0,800,2400,'b'],[68,0,732,76,'b'],[68,76,165,550,'b'],[635,76,732,550,'b']]},
    data:{title:'LEVEL 3',name:'FORTRESS / DEAD SIGNAL',brief:['DESTROY THREE RED RELAYS TO OPEN THE AI DATA CENTER.','HOLD COVER TO CROUCH. FIRE TO PEEK, RELEASE TO HIDE.','ASSAULT RIFLE IS UNLIMITED. UPGRADES CARRY AMMO.','THE NORTH BLAST DOORS CONCEAL GOSFER.'],start:{x:400,y:2290,a:Math.PI},checkpoints:[[400,1870],[400,1320],[400,680]],gates:[[400,2320],[400,1370]],bossLine:560,boss:{x:400,y:195},structures,props:[],units:[unit(430,2010),unit(590,1920),unit(170,1730),unit(460,1620),unit(335,1440),unit(655,1280),unit(400,1150),unit(190,1030,true),unit(605,935),unit(320,750,true),unit(500,660),unit(360,480)]},
    boss:TD.makeGosfer,cameraOwns:true,arcadeAssault:true,canReinforce:()=>false,canSpawnBoss:G=>G.fortress.relays>=3,
    setup(G){W.navR=10;G.fortress={doorOpen:false,relays:0};G.structures.push(TD.makeStructure(cover('relay',190,1770)));G.pickups.push({kind:'minigun',foot:true,x:460,y:2200,t:0});},
    pre(G){const p=G.player;p.scripted=G.boss?.state==='enter';if(p.scripted){const fromY=p.y;p.inv=10;p.y=M.lerp(p.y,428,.035);p.a=p.aim=Math.PI;p.moving=p.y>431;p.walkT+=1/60;if(p.moving)p.gaitPhase=((p.gaitPhase||0)+Math.abs(p.y-fromY)/96)%1;G.shots=[];G.eshots=[];}if(G.boss)p.y=Math.min(p.y,445);},
    drawFloor(ctx,G){art.draw(ctx,'od_cover_door'+(G.fortress?.doorOpen?'_open':''),400,129,{s:.65});},
    drawOver(ctx,G){const p=G.player;for(const s of G.structures)if(s.assault&&!s.dead&&s.cover&&p.y<s.y+s.type.hh&&Math.abs(p.x-s.x)<s.type.hw+18&&p.y>s.y-s.type.hh-55)drawCover(ctx,s);},
    hud(ctx,text,G){TD.infantryHUD(ctx,text,G);if(!G.boss)text(G.fortress.relays<3?'DISABLE RED RELAYS: '+G.fortress.relays+'/3':'DATA CENTER UNLOCKED / ADVANCE NORTH',TD.VW/2,72,11,'#ffd060','center');else if(G.boss.state==='enter'){text('MAINFRAME BREACH',TD.VW/2,225,18,'#ff6245','center');text('GOSFER',TD.VW/2,252,24,'#fff','center');text('40 WATT LASER RIFLE / EXTREME REFLEXES',TD.VW/2,276,11,'#8ceaff','center');}return true;},
    cam(G){if(G.boss)TD.Cam.follow(400,TD.VH/2,.1);else{const p=G.player,f=M.fwd(p.aim);TD.Cam.follow(p.x+f[0]*24+p.vx*12,p.y+f[1]*24+p.vy*12,.12);}},
    keys:TD.footBriefKeys,
  });
})(window);
