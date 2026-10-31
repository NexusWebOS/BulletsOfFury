/* Night pursuit: Hotwire maintains speed; the player steers and aims the bed turret.
 * A complete 150-second authored wave schedule. Hull loss restarts the whole run. */
(function(root){
  'use strict';const TD=root.TD,M=TD.M,I=TD.Input,FX=TD.FX,A=TD.Audio,art=TD.AssaultArt;
  for(const type of ['convoyJet','convoyTruck','convoyRunner','convoyElite'])TD.ET[type]={hp:12,r:24,vis:{range:800,half:Math.PI},still:true,score:500};
  function setup(G){
    G.convoy={phase:'search',age:0,combat:0,scroll:0,nextWave:1,wave:0,intercepts:0,eliteSpawned:0,restarts:0,deathT:0,clear:false};
    Object.assign(G.player,{convoy:true,x:320,y:345,a:Math.PI,aim:Math.PI,hp:100,max:100,r:31,inv:0,dead:false,fireCd:0,flash:0,damageCd:0,retina:null,vx:0,vy:-3,steerVX:0,steerVY:0,cruising:false});
    G.units=[];G.shots=[];G.eshots=[];G.wrecks=[];G.msgs=[];G.boss=null;G.bossDeadT=null;G.time=0;G.kills=0;G.score=0;TD.Stealth.alerts=0;FX.list=[];TD.Cam.x=TD.Cam.y=0;TD.Cam.zoom=1;TD.Cam.maxY=480;
  }
  function spawn(G,kind,x,y,side=0){
    const elite=kind==='elite',jet=kind==='jet',truck=kind==='truck';
    y=-Math.max(110,Math.abs(y)%180+110); // Every new hostile first crosses the north edge.
    const u={type:jet?'convoyJet':truck?'convoyTruck':elite?'convoyElite':'convoyRunner',kind,x,y,startX:x,side,a:Math.PI,hp:jet?12:truck?18:elite?20:6,max:jet?12:truck?18:elite?20:6,r:jet?39:truck?43:elite?24:20,t:0,vx:0,vy:0,driveState:'approach',driveT:0,rammed:false,fireCd:jet?1.4:truck?1.7:2.2,flash:0,dead:false,mode:'alert',vis:{range:800,half:Math.PI}};
    G.units.push(u);if(elite)G.convoy.eliteSpawned++;return u;
  }
  function wave(G){
    const c=G.convoy,n=c.wave++,late=c.combat>=115;
    // Alternating left/right pressure always leaves time to intercept rockets.
    if(n%4===0){spawn(G,'jet',160,-100,-1);spawn(G,'jet',480,-185,1);}
    else if(n%4===1){spawn(G,'truck',n%8===1?135:505,560,n%8===1?-1:1);spawn(G,late?'elite':'runner',250,545);spawn(G,late?'elite':'runner',400,590);}
    else if(n%4===2){for(const x of [140,270,500])spawn(G,late?'elite':'runner',x,520+Math.abs(x-300)*.25);spawn(G,'jet',330,-120,0);}
    else{spawn(G,'truck',125,530,-1);spawn(G,'truck',515,610,1);if(late)spawn(G,'elite',320,555);}
    c.nextWave=late?5.2:c.combat>60?6.2:7.4;
  }
  function kill(G,u){u.dead=true;G.kills++;G.score+=u.kind==='elite'?1000:u.kind==='runner'?300:650;FX.boom(u.x,u.y,u.kind==='runner'||u.kind==='elite'?65:130,'gfx_destruction_',6);FX.smoke(u.x,u.y,.3,1.1);FX.debris(u.x,u.y,.25);A.play(u.kind==='jet'?'expBoss':'enemyDie',.5);TD.Cam.kick(2);if(u.kind==='truck')G.wrecks.push({x:u.x,y:u.y,t:0});}
  function damage(G,dmg){
    const p=G.player,c=G.convoy;if(p.dead||c.phase!=='pursuit'||p.damageCd>0)return;p.damageCd=.12;p.hp=Math.max(0,p.hp-dmg*(TD.DIFFICULTIES?.[TD.difficulty||'normal']?.damage||1));p.flash=.13;FX.boom(p.x+M.rnd(-25,25),p.y+M.rnd(-30,35),38,'gfx_impact_',6);A.play('impactMetal',.4);TD.Cam.kick(3);
    if(p.hp<=0){p.dead=true;c.phase='wreck';c.deathT=0;G.deaths++;A.stopLoops();A.play('expBoss');FX.boom(p.x,p.y,210,'gfx_destruction_',6);FX.ring(p.x,p.y,1);FX.debris(p.x,p.y,.6);TD.Cam.kick(12);}
  }
  function bed(p,x=p.x,y=p.y){const f=M.fwd(p.a);return{x:x-f[0]*24,y:y-f[1]*24};}
  TD.Convoy={setup,spawn,damage,wave,bed};
  function shot(x,y,tx,ty,missile,elite){const a=M.angTo(x,y,tx,ty),f=M.fwd(a),speed=missile?2.6:elite?3.9:3.3;return{k:missile?'missile':elite?'laser':'mg',x,y,a,vx:f[0]*speed,vy:f[1]*speed,dmg:missile?9:elite?3:2,r:missile?9:4,life:240,t:0,shootable:missile};}
  function step(G,dt){
    const c=G.convoy,p=G.player;c.age+=dt;G.time+=dt;c.scroll=(c.scroll+dt*(c.phase==='search'?100:195))%1600;
    TD.Cam.x=TD.Cam.y=0;TD.Cam.zoom=1;TD.Cam.shake*=.85;FX.update(dt);p.flash=Math.max(0,p.flash-dt);p.damageCd=Math.max(0,(p.damageCd||0)-dt);
    if(c.phase==='wreck'){
      c.deathT+=dt;if(G.t%12===0&&c.deathT<1.5){FX.boom(p.x+M.rnd(-30,30),p.y+M.rnd(-40,40),85,'gfx_destruction_',6);FX.smoke(p.x,p.y,.4,1.5);}
      if(c.deathT>=3){const restarts=c.restarts+1,deaths=G.deaths;setup(G);G.convoy.restarts=restarts;G.deaths=deaths;I.holdCombat();A.play('loadoutLaunch');}return;
    }
    if(c.phase==='escape'){c.escapeT+=dt;p.y-=dt*120;if(c.escapeT>2.5)return 'clear';return;}
    // Hotwire keeps forward road speed; ordinary directions steer the hull.
    // Only the explicit cruise/free-aim shoulder lends the D-pad to the turret.
    const [dx,dy]=I.dir(),free=I.down('cruise'),len=Math.hypot(dx,dy)||1;
    p.cruising=free;
    p.steerVX=M.lerp(p.steerVX,free?0:dx/len*185,1-Math.exp(-dt*10));
    p.steerVY=M.lerp(p.steerVY,free?0:dy/len*145,1-Math.exp(-dt*10));
    p.x=M.clamp(p.x+p.steerVX*dt,92,548);p.y=M.clamp(p.y+p.steerVY*dt,168,380);
    if((p.x===92&&p.steerVX<0)||(p.x===548&&p.steerVX>0))p.steerVX=0;
    if((p.y===168&&p.steerVY<0)||(p.y===380&&p.steerVY>0))p.steerVY=0;
    p.vx=p.steerVX/60;p.vy=(p.steerVY-195)/60;
    p.a=M.turnTo(p.a,Math.PI+Math.atan2(p.steerVX,195-p.steerVY),dt*1.8);
    if(c.phase==='search'){
      if(c.age>=7.5){c.phase='pursuit';c.combat=0;c.nextWave=.5;TD.Stealth.alerts=1;A.play('alert');TD.Cam.kick(4);G.msgs.push({text:'SPOTTED! PROTECT THE HULL',t:0});}return;
    }
    c.combat+=dt;TD.Retina.tick(p,G,dt);
    const mount=bed(p),aim=I.aim(mount)??(free&&(dx||dy)?M.angTo(0,0,dx,dy):null);
    if(p.retina?.locked&&(I.down('retina')||aim==null)){const t=p.retina.target.point();p.aim=M.angTo(mount.x,mount.y,t.x,t.y);}
    else if(aim!=null)p.aim=aim;
    if(I.down('aimLeft')||I.down('aimRight'))p.aim+=(I.down('aimRight')?1:-1)*.065;
    p.fireCd-=dt;if(I.down('A')&&p.fireCd<=0){p.fireCd=.07;const f=M.fwd(p.aim),x=mount.x+f[0]*42,y=mount.y+f[1]*42;G.shots.push({k:'vulcan',x,y,a:p.aim,vx:f[0]*12,vy:f[1]*12,dmg:2,r:5,life:65,t:0,lv:1});FX.flash(x,y,p.aim,.2);A.play('gd_soldierRifle',.5);}
    if((c.nextWave-=dt)<=0)wave(G);
    for(const u of G.units){if(u.dead)continue;u.t+=dt;u.flash=Math.max(0,u.flash-dt);u.fireCd-=dt;
      const ox=u.x,oy=u.y;u.driveT+=dt;
      if(u.kind==='jet'){
        // A readable straight pass with one smooth lane change, not a sine orbit.
        const target=u.startX+(u.t>2?u.side*70:0);u.vx=M.lerp(u.vx,M.clamp((target-u.x)*1.4,-45,45),1-Math.exp(-dt*2));u.vy=M.lerp(u.vy,90,1-Math.exp(-dt*3));u.x+=u.vx*dt;u.y+=u.vy*dt;u.a=M.turnTo(u.a,Math.PI+Math.atan2(u.vx,195-u.vy),dt*1.4);
      }else if(u.kind==='truck'){
        if(u.driveState==='approach'&&u.y>185){u.driveState='pace';u.driveT=0;}
        if(u.driveState==='pace'&&u.driveT>2.7&&!u.rammed){u.driveState='warn';u.driveT=0;G.msgs.push({text:'GUN TRUCK RAM - SHOOT THE HULL',t:0});A.play('warn',.25);}
        if(u.driveState==='warn'&&u.driveT>.9){u.driveState='ram';u.driveT=0;u.ramX=p.x;u.ramY=p.y+100;u.rammed=true;}
        const ram=u.driveState==='ram',tx=ram?u.ramX:u.startX,ty=ram?u.ramY:245;
        const targetVX=M.clamp((tx-u.x)*1.25,-85,85),targetVY=M.clamp((ty-u.y)*1.3,ram?-50:0,ram?160:90);
        u.vx=M.lerp(u.vx,targetVX,1-Math.exp(-dt*2.2));u.vy=M.lerp(u.vy,targetVY,1-Math.exp(-dt*2.2));u.x+=u.vx*dt;u.y+=u.vy*dt;u.a=M.turnTo(u.a,Math.PI+Math.atan2(u.vx,195-u.vy),dt*1.25);
        if(ram&&u.driveT>3){u.driveState='leave';u.vy=140;}if(u.driveState==='leave')u.y+=dt*100;
      }else{
        const want=M.angTo(u.x,u.y,p.x,p.y+80);u.a=M.turnTo(u.a,want,dt*3.4);const v=M.fwd(u.a);u.vx=M.lerp(u.vx,v[0]*(u.kind==='elite'?78:64),1-Math.exp(-dt*5));u.vy=M.lerp(u.vy,v[1]*(u.kind==='elite'?78:64),1-Math.exp(-dt*5));u.x+=u.vx*dt;u.y+=u.vy*dt;u.walkT=(u.walkT||0)+Math.hypot(u.x-ox,u.y-oy)/65;
      }
      if(!u.entered&&u.y>90){u.entered=true;u.fireCd=Math.max(.7,u.fireCd);}
      if(u.entered&&u.fireCd<=0&&u.y>70&&u.y<470){u.fireCd=u.kind==='jet'?2:u.kind==='truck'?2.1:u.kind==='elite'?1.5:2.7;G.eshots.push(shot(u.x,u.y,p.x,p.y,u.kind==='jet',u.kind==='elite'));A.play(u.kind==='jet'?'missileLaunch':'enemyLaser',.3);}
      if(u.kind!=='jet'&&Math.abs(u.x-p.x)<45&&Math.abs(u.y-p.y)<55){damage(G,u.kind==='truck'?8:4);u.dead=true;FX.boom(u.x,u.y,80,'gfx_destruction_',6);}
      if(u.y>630||u.y< -400||u.t>22){u.dead=true;}
    }
    for(const s of G.shots){s.t++;s.x+=s.vx;s.y+=s.vy;if(--s.life<=0)s.dead=true;
      for(const e of G.eshots)if(!e.dead&&e.shootable&&M.dist(s.x,s.y,e.x,e.y)<e.r+s.r+5){e.dead=s.dead=true;c.intercepts++;G.score+=100;FX.boom(e.x,e.y,70,'gfx_destruction_',6);A.play('missileHit',.6);break;}
      if(s.dead)continue;for(const u of G.units)if(!u.dead&&TD.vehicleShotHit(u,s)){u.hp-=s.dmg;u.flash=.1;s.dead=true;FX.boom(s.x,s.y,22,'gfx_impact_',6);if(u.hp<=0)kill(G,u);break;}
    }
    for(const e of G.eshots){if(e.dead)continue;e.t++;e.x+=e.vx;e.y+=e.vy;if(e.shootable&&e.t%4===0)FX.smoke(e.x,e.y,.045,.3);if(--e.life<=0||e.x< -80||e.x>720||e.y< -100||e.y>580)e.dead=true;if(Math.abs(e.x-p.x)<32+e.r&&Math.abs(e.y-p.y)<57+e.r){damage(G,e.dmg);e.dead=true;}}
    G.shots=G.shots.filter(s=>!s.dead);G.eshots=G.eshots.filter(e=>!e.dead);G.units=G.units.filter(u=>!u.dead);
    for(const w of G.wrecks){w.y+=dt*150;w.t+=dt;}G.wrecks=G.wrecks.filter(w=>w.y<600);
    for(const m of G.msgs)m.t+=dt;G.msgs=G.msgs.filter(m=>m.t<3);
    if(p.hp<35&&G.t%12===0)FX.smoke(p.x,p.y-25,.2,.8);
    if(c.combat>=150&&!p.dead){c.phase='escape';c.escapeT=0;G.units=[];G.eshots=[];G.shots=[];G.ghost=false;A.play('achievement');}
    A.scene(G,dt);
  }
  function player(ctx,G,x=G.player.x,y=G.player.y){
    const p=G.player,c=G.convoy;art.draw(ctx,'od_silverado_'+(p.dead?3:0),x,y,{s:.4,a:p.a+Math.PI,flash:p.flash>0?1:0});
    if(p.dead)return;const a=p.aim+Math.PI,mount=bed(p,x,y);
    if(p.pilot==='yuri')art.draw(ctx,'od_gunner_0',mount.x,mount.y,{s:.29,a,ax:185,ay:220});
    else{ART.draw(ctx,'oft_base',mount.x,mount.y,{s:.55});ART.draw(ctx,'fp_'+p.pilot+'_aim_0',mount.x,mount.y+5,{s:.65,a});ART.draw(ctx,'oft_north',mount.x,mount.y,{s:.9,a});}
  }
  function draw(ctx,G){const c=G.convoy,p=G.player,plate=ART.get('od_night_road');
    ctx.save();const shake=TD.Cam.shake;ctx.translate(shake>.5?Math.sin(G.t*2)*shake:0,0);
    if(plate){const y=c.scroll;for(const k of [-1,0])ctx.drawImage(plate.im,plate.sx,plate.sy,800,1600,-80,y+k*1600,800,1600);}
    for(const w of G.wrecks)art.draw(ctx,'od_guntruck_3',w.x,w.y,{s:.38});
    FX.draw(ctx,0);
    for(const u of G.units.filter(u=>u.kind!=='jet')){if(u.kind==='truck'){art.draw(ctx,'od_guntruck_0',u.x,u.y,{s:.46,a:u.a+Math.PI,flash:u.flash>0?1:0});ART.draw(ctx,'oft_base',u.x,u.y+25,{s:.5});art.draw(ctx,'od_robot_north_0',u.x,u.y+49,{s:.23});ART.draw(ctx,'oft_north',u.x,u.y+25,{s:.65,a:M.angTo(u.x,u.y,p.x,p.y)+Math.PI});}else TD.drawAssaultRobot(ctx,u,u.kind==='elite');}
    player(ctx,G);for(const u of G.units.filter(u=>u.kind==='jet')){art.draw(ctx,'od_hunter_jet_0',u.x+14,u.y+22,{s:.45,a:u.a+Math.PI,tint:'#000000',alpha:.45});art.draw(ctx,'od_hunter_jet_0',u.x,u.y,{s:.45,a:u.a+Math.PI,flash:u.flash>0?1:0});}
    if(c.phase==='search'){const x=M.lerp(90+Math.sin(c.age*1.5)*80,p.x,Math.min(1,c.age/7.5)),y=60+c.age*34;ART.draw(ctx,'bmfx_fov_yellow_tall',x,y,{s:.8,palette:'#b7e8ff',alpha:.45,a:Math.PI});art.draw(ctx,'od_hunter_jet_0',x-85,y-120,{s:.4,a:.28});}
    for(const s of G.shots)TD.drawShot(ctx,s,false);for(const s of G.eshots)TD.drawShot(ctx,s,true);FX.draw(ctx,1);TD.Retina.draw(ctx,p);ctx.restore();
  }
  function hud(ctx,text,G){const c=G.convoy,p=G.player;ctx.fillStyle='rgba(2,8,19,.85)';ctx.fillRect(9,8,622,55);text('SILVERADO / HULL',20,21,11,'#ade7f9');ctx.fillStyle='#253543';ctx.fillRect(20,35,225,14);ctx.fillStyle=p.hp<30?'#ed423b':'#47e297';ctx.fillRect(22,37,221*M.clamp(p.hp/100,0,1),10);text(Math.min(100,Math.ceil(p.hp))+'%',255,42,11,'#fff');const left=Math.max(0,150-c.combat);text(String(Math.floor(left/60)).padStart(2,'0')+':'+String(Math.ceil(left%60)).padStart(2,'0'),611,34,24,'#ffd079','right');ART.draw(ctx,'pav_hotwire',35,446,{s:.14});text('HOTWIRE / DRIVER',63,443,10,'#ffbd75');text('MG UNLIMITED',627,452,10,'#aeeeff','right');
    if(c.phase==='search'){text('LIGHTS OUT. STAY LOW.',320,94,16,'#b1d7ff','center');text('JET SEARCHLIGHTS INBOUND',320,118,10,'#fff','center');}
    if(c.phase==='wreck'){text('HULL DESTROYED',320,194,26,'#ff7152','center');text('RESTARTING THE PURSUIT',320,224,12,'#fff','center');}
    if(c.phase==='escape'){text('EXTRACTION CORRIDOR CLEAR',320,177,19,'#8fffd3','center');text('HOTWIRE: HOLD ON!',320,210,13,'#ffc079','center');}
    for(const m of G.msgs)text(m.text,320,96,16,'#ffdf75','center');if(c.combat>=115&&c.phase==='pursuit')text('RED ELITE PURSUIT',320,78,11,'#ff6555','center');return true;}
  TD.MISSIONS.push({id:6,mode:'turret',view640:true,map:{key:'od_night_road',w:640,h:480,rects:[]},data:{title:'LEVEL 6',name:'NIGHT RUN / HULL ZERO',brief:['D-PAD STEERS. HOTWIRE KEEPS US MOVING.','FACE BUTTONS AIM + FIRE. HOLD L FOR FREE AIM.','SHOOT ROCKETS, GUN TRUCKS AND PURSUING ROBOTS.','SURVIVE 2:30. HULL LOSS RESTARTS THE WHOLE RUN.'],start:{x:320,y:345,a:Math.PI},checkpoints:[],gates:[],bossLine:-1000,boss:{x:0,y:0},units:[],props:[],structures:[]},boss:null,setup,exclusiveStep:step,drawWorld:draw,briefSprite:player,hud,keys:()=>I.padStyle()==='standard'?[['a','FIRE'],['dpad','STEER'],['start','PAUSE']]:[['x','FIRE NORTH'],['y','FIRE WEST'],['dpad','STEER'],['a','FIRE SOUTH'],['b','FIRE EAST'],['start','PAUSE']],score(G,R){R.extraRows=[['ROCKETS STOPPED',G.convoy.intercepts],['PURSUIT RESTARTS',G.convoy.restarts]];}});
})(window);
