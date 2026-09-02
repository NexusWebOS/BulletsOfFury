/*
 * Isolated 2026-09-01 combat-pattern laboratory.
 *
 * This file deliberately lives outside assets/game.js. It borrows the shipped Stage-1 plate,
 * Lizzie's real runtime ship, and existing enemy/boss artwork, then draws experimental movement
 * and ammunition on a transparent canvas over the real game. Nothing here is imported by the
 * production build. It is a visual/timing prototype, not a stealth gameplay patch.
 */
(()=>{
  'use strict';
  const W=480,H=512,labCv=document.getElementById('lab'),g=labCv.getContext('2d');
  g.imageSmoothingEnabled=false;
  const C={
    gold:'#ffd04b',white:'#fff9d2',orange:'#ff6a22',red:'#ff2d25',
    green:'#48ff7b',greenHot:'#d9ffe2',cyan:'#72e9ff',ink:'#05090c'
  };
  const S={ready:false,t:0,last:0,shots:[],smoke:[],sparks:[],events:[],eventI:0,
    playerX:240,playerY:442,playerVX:0,phase:'',bossCritical:false,disabledPod:0,
    completed:false,metrics:{maxShots:0,closest:999,events:0,intercepts:0,beamDoors:[2,2]}};
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const lerp=(a,b,p)=>a+(b-a)*p;
  const ease=p=>p*p*(3-2*p);
  const TAU=Math.PI*2;

  function art(key){
    try{return (typeof XART!=='undefined'&&XART.rdy(key))?XART.get(key):null;}catch(_){return null;}
  }
  function drawArt(key,x,y,w,h,rot=0,alpha=1,flipY=false){
    const im=art(key);if(!im)return false;
    g.save();g.translate(x,y);g.rotate(rot);if(flipY)g.scale(1,-1);g.globalAlpha=alpha;
    g.drawImage(im,-w/2,-h/2,w,h);g.restore();return true;
  }
  function text(txt,x,y,size=10,col='#fff',align='center'){
    g.save();g.textAlign=align;g.textBaseline='middle';g.font=`bold ${size}px monospace`;
    g.shadowColor='#000';g.shadowBlur=4;g.fillStyle=col;g.fillText(txt,x,y);g.restore();
  }
  function panel(title,detail){
    g.save();g.fillStyle='rgba(2,7,11,.82)';g.fillRect(7,7,W-14,39);
    g.strokeStyle='rgba(255,194,26,.82)';g.strokeRect(7.5,7.5,W-15,38);
    text(title,15,19,11,'#ffd04b','left');text(detail,15,35,8,'#d4e3ed','left');g.restore();
  }
  function banner(txt,col=C.green){
    g.save();g.globalAlpha=.9;g.fillStyle='rgba(0,0,0,.72)';g.fillRect(45,H-43,W-90,24);
    g.strokeStyle=col;g.strokeRect(45.5,H-42.5,W-91,23);text(txt,W/2,H-31,9,col);g.restore();
  }

  function playerScreen(){return {x:S.playerX,y:S.playerY};}
  function aim(x,y,tx,ty,speed){const a=Math.atan2(ty-y,tx-x);return {vx:Math.cos(a)*speed,vy:Math.sin(a)*speed,a};}
  function shot(kind,x,y,vx,vy,opt={}){
    S.shots.push({kind,x,y,vx,vy,t:0,life:opt.life||5,speed:Math.hypot(vx,vy),
      turn:opt.turn||0,curve:opt.curve||0,accel:opt.accel||0,maxSpeed:opt.maxSpeed||999,
      r:opt.r||4,side:opt.side||0,phase:opt.phase||0});
    S.metrics.events++;
  }
  function aimed(kind,x,y,speed,opt={}){
    const p=playerScreen(),v=aim(x,y,p.x,p.y,speed);shot(kind,x,y,v.vx,v.vy,opt);
  }
  function tracer(x,y,speed=300,spread=0,target){
    const p=target||playerScreen(),v=aim(x,y,p.x,p.y,speed),a=v.a+spread;
    shot('tracer',x,y,Math.cos(a)*speed,Math.sin(a)*speed,{life:2.6,r:3});
  }
  function cannon(x,y,speed=185,spread=0){
    const p=playerScreen(),v=aim(x,y,p.x,p.y,speed),a=v.a+spread;
    shot('cannon',x,y,Math.cos(a)*speed,Math.sin(a)*speed,{life:3.5,r:7});
  }
  function greenCurve(x,y,side,phase=0){
    const a=Math.PI/2+side*.30;
    shot('curve',x,y,Math.cos(a)*165,Math.sin(a)*165,{life:4.2,r:6,curve:-side*.78,side,phase});
  }
  function missile(x,y,side){
    const a=Math.PI/2+side*.18;
    shot('missile',x,y,Math.cos(a)*118,Math.sin(a)*118,{life:5.4,r:7,turn:1.15,accel:42,maxSpeed:215,side});
  }

  function event(at,fn){S.events.push({at,fn});}
  function buildEvents(){
    S.events.length=0;
    const slots=[66,177,303,414];
    for(let j=0;j<slots.length;j++){
      const lock={x:240,y:442};
      for(let k=0;k<6;k++)event(2.35+j*.08+k*.10,()=>{
        const p=jetPose(j,S.t);if(k===0)Object.assign(lock,playerScreen());
        tracer(p.x+(j%2?-9:9),p.y+24,305,(j-1.5)*.014,lock);
      });
    }
    for(let k=0;k<3;k++)event(10.65+k*.19,()=>cannon(tankPose(S.t).x,tankPose(S.t).y+27,188,(k-1)*.075));
    for(let k=0;k<5;k++){
      event(12.00+k*.105,()=>{const q=supportJetPose(-1,S.t);tracer(q.x,q.y+18,325,-.035);});
      event(12.16+k*.105,()=>{const q=supportJetPose(1,S.t);tracer(q.x,q.y+18,325,.035);});
    }
    for(let k=0;k<8;k++){
      event(18.25+k*.085,()=>{const b=bossPose(S.t);tracer(b.x-22,b.y+42,318,-.025);});
      event(18.30+k*.085,()=>{const b=bossPose(S.t);tracer(b.x+22,b.y+42,318,.025);});
    }
    event(20.45,()=>{const b=bossPose(S.t);missile(b.x-49,b.y+30,-1);});
    event(20.66,()=>{const b=bossPose(S.t);missile(b.x+49,b.y+30,1);});
    for(let wave=0;wave<4;wave++)for(let i=0;i<4;i++){
      event(22.05+wave*.34+i*.045,()=>{const b=bossPose(S.t),side=i<2?-1:1;greenCurve(b.x+side*50,b.y+22,side,wave*.55+i*.15);});
    }
    event(30.85,()=>{const b=bossPose(S.t);S.bossCritical=true;S.disabledPod=1;for(let i=0;i<18;i++)S.sparks.push({x:b.x+49,y:b.y+30,t:0,life:.46,a:i/18*TAU,r:3.4});});
    for(let k=0;k<6;k++)event(31.25+k*.13,()=>{const b=bossPose(S.t);tracer(b.x-25,b.y+38,342,-.04);});
    S.events.sort((a,b)=>a.at-b.at);S.eventI=0;
  }

  function jetPose(i,t){
    const starts=[66,177,303,414],d=i*.16,u=clamp((t-d)/7.0,0,1),side=i<2?-1:1;
    const x=starts[i]+side*Math.sin(u*Math.PI)*22+Math.sin(u*TAU+i)*5;
    const y=-68+u*650;
    const du=.002,x2=starts[i]+side*Math.sin(clamp(u+du,0,1)*Math.PI)*22+Math.sin(clamp(u+du,0,1)*TAU+i)*5;
    return {x,y,rot:Math.atan2(x2-x,du*650)*.72};
  }
  function tankPose(t){
    const u=clamp((t-7.4)/2.45,0,1),hold=t>9.85;
    return {x:240,y:hold?132:lerp(-70,132,ease(u)),kick:(t>10.55&&t<11.35)?Math.sin((t-10.55)*25)*3:0};
  }
  function supportJetPose(side,t){
    const u=clamp((t-8.4)/6.0,0,1),base=side<0?91:389;
    return {x:base+side*Math.sin(u*Math.PI)*32,y:-50+u*610,rot:side*Math.sin(u*Math.PI)*.24};
  }
  function bossPose(t){
    const u=clamp((t-14.4)/1.55,0,1),y=lerp(-118,122,ease(u));
    const move=Math.max(0,t-16.8),x=240+Math.sin(move*.54)*112;
    return {x,y};
  }

  function updatePlayer(dt){
    let tx;
    if(S.t<7.4)tx=240+Math.sin(S.t*1.10)*112;
    else if(S.t<14.4)tx=240+Math.sin(S.t*1.42)*126;
    else if(S.t<24.0)tx=240+Math.sin(S.t*.92)*118;
    else if(S.t<27.1)tx=222;                      // first two-lane beam door
    else if(S.t<30.2)tx=286;                      // door walks only one lane
    else tx=240+Math.sin(S.t*1.12)*106;
    /* Predict where a committed projectile will cross Lizzie's row. This is deliberately a
       small local dodge, not perfect bot play: it demonstrates that sampled shots remain
       evadable after release, while the beam phases still own their explicit two-lane doors. */
    if(!beamState())for(const q of S.shots){
      if(!(q.vy>20))continue;
      const eta=(S.playerY-q.y)/q.vy;if(!(eta>0&&eta<.72))continue;
      const cross=q.x+q.vx*eta;
      if(Math.abs(cross-tx)<38)tx+=cross<tx?72:-72;
    }
    tx=clamp(tx,34,W-34);
    const old=S.playerX;S.playerX=lerp(S.playerX,tx,clamp(dt*8.2,0,1));S.playerVX=(S.playerX-old)/Math.max(dt,.001);
    S.playerY=443+Math.sin(S.t*1.7)*5;
    try{
      /* Freeze only the laboratory's underlying stage director. The production update still
         draws Lizzie and her rounds, but cannot advance the map, drop crates, or summon its own
         encounter underneath this isolated pattern test. */
      stageTimer=0;mapScroll=2280;camX=160;bossWarned=true;subBossDone=true;subBossTriggered=true;
      warnKind=null;warnT=0;_sc1=true;_sc2=true;_mc1=true;_mc2=true;story=null;_bossCard=null;
      enemies.length=0;eBullets.length=0;powerups.length=0;aiQueue.length=0;
      boss=null;bossActive=false;subBoss=null;subBossActive=false;
      player.x=camX+S.playerX;player.y=S.playerY;player.invuln=1e9;
      player._bank=clamp(S.playerVX/420,-.72,.72);player._px=player.x;player._py=player.y;
    }catch(_){ }
  }
  function updateShots(dt){
    const p=playerScreen();
    for(const q of S.shots){
      q.t+=dt;q.life-=dt;
      if(q.kind==='missile'){
        const desired=Math.atan2(p.y-q.y,p.x-q.x),cur=Math.atan2(q.vy,q.vx);
        let d=((desired-cur+Math.PI*3)%TAU)-Math.PI;d=clamp(d,-q.turn*dt,q.turn*dt);
        const ns=Math.min(q.maxSpeed,q.speed+q.accel*dt),a=cur+d;q.speed=ns;q.vx=Math.cos(a)*ns;q.vy=Math.sin(a)*ns;
        if(Math.random()<.5)S.smoke.push({x:q.x,y:q.y,t:0,life:.42,r:4});
      }else if(q.curve){
        const a=Math.atan2(q.vy,q.vx)+q.curve*dt;q.vx=Math.cos(a)*q.speed;q.vy=Math.sin(a)*q.speed;
      }
      q.x+=q.vx*dt;q.y+=q.vy*dt;
      /* The boss missiles advertise themselves as shootable. Honor that silhouette promise with
         Lizzie's real runtime rounds instead of letting a visually breakable threat ghost through
         her fire. Production bullets are in world X; laboratory threats are in screen X. */
      if(q.kind==='missile' && typeof pBullets!=='undefined'){
        const hit=pBullets.some(b=>b && Math.hypot((b.x-camX)-q.x,b.y-q.y)<15);
        if(hit){
          q.life=0;S.metrics.intercepts++;
          for(let i=0;i<8;i++)S.sparks.push({x:q.x,y:q.y,t:0,life:.28,a:i/8*TAU,r:2.5});
          continue;
        }
      }
      const d=Math.hypot(q.x-p.x,q.y-p.y);S.metrics.closest=Math.min(S.metrics.closest,d);
      if(q.x<-55||q.x>W+55||q.y<-80||q.y>H+80)q.life=0;
    }
    S.shots=S.shots.filter(q=>q.life>0);S.metrics.maxShots=Math.max(S.metrics.maxShots,S.shots.length);
    for(const s of S.smoke){s.t+=dt;s.life-=dt;s.y-=10*dt;s.r+=9*dt;}S.smoke=S.smoke.filter(s=>s.life>0);
    for(const s of S.sparks){s.t+=dt;s.life-=dt;s.x+=Math.cos(s.a)*86*dt;s.y+=Math.sin(s.a)*86*dt;s.r*=.96;}S.sparks=S.sparks.filter(s=>s.life>0);
  }

  function drawTracer(q){
    const a=Math.atan2(q.vy,q.vx)+Math.PI/2;
    g.save();g.translate(q.x,q.y);g.rotate(a);g.shadowColor=C.gold;g.shadowBlur=7;
    g.fillStyle='#5d2709';g.fillRect(-3,-12,6,24);g.fillStyle=C.gold;g.fillRect(-1.8,-10,3.6,20);g.fillStyle=C.white;g.fillRect(-.7,-8,1.4,15);g.restore();
  }
  function drawCannon(q){
    g.save();g.shadowColor=C.orange;g.shadowBlur=12;g.fillStyle=C.ink;g.beginPath();g.arc(q.x,q.y,9,0,TAU);g.fill();
    g.fillStyle=C.orange;g.beginPath();g.arc(q.x,q.y,7,0,TAU);g.fill();g.fillStyle=C.white;g.beginPath();g.arc(q.x,q.y,2.6,0,TAU);g.fill();g.restore();
  }
  function drawCurve(q){
    const a=Math.atan2(q.vy,q.vx)+Math.PI/2;
    g.save();g.translate(q.x,q.y);g.rotate(a);g.shadowColor=C.green;g.shadowBlur=10;g.strokeStyle='#0a541d';g.lineWidth=6;
    g.beginPath();g.arc(0,0,10,-2.2,-.25);g.stroke();g.strokeStyle=C.green;g.lineWidth=3;g.stroke();g.strokeStyle=C.greenHot;g.lineWidth=1;g.stroke();g.restore();
  }
  function drawMissile(q){
    const a=Math.atan2(q.vy,q.vx)+Math.PI/2;
    g.save();g.translate(q.x,q.y);g.rotate(a);g.fillStyle='#231b16';g.fillRect(-5,-10,10,19);
    g.fillStyle=C.red;g.beginPath();g.moveTo(-5,-10);g.lineTo(5,-10);g.lineTo(0,-18);g.closePath();g.fill();
    g.fillStyle='#f5e7bf';g.fillRect(-2,-7,4,12);g.fillStyle=C.orange;g.beginPath();g.moveTo(-4,9);g.lineTo(4,9);g.lineTo(0,17);g.closePath();g.fill();g.restore();
  }
  function drawShots(){
    for(const s of S.smoke){g.save();g.globalAlpha=clamp(s.life/.42,0,.42);g.fillStyle='#c8d1ca';g.beginPath();g.arc(s.x,s.y,s.r,0,TAU);g.fill();g.restore();}
    for(const s of S.sparks){g.save();g.globalAlpha=clamp(s.life/.28,0,1);g.shadowColor=C.orange;g.shadowBlur=7;g.fillStyle=C.white;g.fillRect(s.x-s.r/2,s.y-s.r/2,s.r,s.r);g.restore();}
    for(const q of S.shots){if(q.kind==='tracer')drawTracer(q);else if(q.kind==='cannon')drawCannon(q);else if(q.kind==='curve')drawCurve(q);else drawMissile(q);}
  }

  function drawJets(){
    if(S.t>7.35)return;
    for(let i=0;i<4;i++){const p=jetPose(i,S.t);drawArt('nef_s1_camo_attack_jet_intact',p.x,p.y,73,81,p.rot,1,false);}
  }
  function drawAnchorWave(){
    if(S.t<7.1||S.t>14.55)return;
    const t=tankPose(S.t);drawArt('nef_s1_jungle_tank_intact',t.x,t.y+t.kick,47,64,0,1,false);
    for(const side of [-1,1]){const q=supportJetPose(side,S.t);drawArt('nef_s1_jungle_bomber_intact',q.x,q.y,101,89,q.rot,1,false);}
    if(S.t>9.9&&S.t<11.35){g.save();g.strokeStyle='rgba(255,208,75,.72)';g.setLineDash([5,5]);g.strokeRect(t.x-43,t.y-43,86,86);g.restore();}
  }
  function drawShutters(){
    if(S.t<14.25||S.t>16.28)return;
    const p=clamp((S.t-14.25)/1.38,0,1),open=ease(p),cx=W/2;
    g.save();g.fillStyle='rgba(7,12,12,.94)';g.strokeStyle='#8ea58a';g.lineWidth=2;
    const ww=W*.52*(1-open),leftW=Math.max(0,ww);
    g.fillRect(0,48,leftW,H*.55);g.strokeRect(.5,48.5,leftW-1,H*.55-1);
    g.fillRect(W-leftW,48,leftW,H*.55);g.strokeRect(W-leftW+.5,48.5,leftW-1,H*.55-1);
    for(let y=62;y<300;y+=24){g.fillStyle='rgba(88,110,79,.32)';g.fillRect(0,y,leftW,3);g.fillRect(W-leftW,y,leftW,3);}g.restore();
  }
  function beamState(){
    if(S.t>=24.0&&S.t<27.15)return {start:24.0,release:24.90,end:27.15,gap:2};
    if(S.t>=27.25&&S.t<30.30)return {start:27.25,release:28.10,end:30.30,gap:3};
    return null;
  }
  function drawBeams(){
    const B=beamState();if(!B)return;
    const cols=6,left=42,right=438,cw=(right-left)/cols;
    const live=S.t>=B.release,alpha=live?.86:(.18+.20*Math.sin((S.t-B.start)*18)**2);
    g.save();
    for(let i=0;i<cols;i++){
      if(i===B.gap||i===B.gap+1)continue;
      const x=left+(i+.5)*cw;
      if(live){g.globalCompositeOperation='lighter';g.shadowColor=C.green;g.shadowBlur=16;g.fillStyle=`rgba(72,255,123,${alpha})`;g.fillRect(x-8,50,16,H-96);g.fillStyle='rgba(230,255,235,.88)';g.fillRect(x-2,50,4,H-96);}
      else{g.strokeStyle=`rgba(72,255,123,${alpha})`;g.setLineDash([8,8]);g.strokeRect(x-9,51,18,H-98);}
    }
    g.restore();
    const doorX=left+(B.gap+1)*cw;
    text(live?'COMMITTED BEAM CORRIDOR':'WARNING — TWO-LANE DOOR',doorX,63,8,live?C.white:C.green);
  }
  function drawBoss(){
    if(S.t<14.25)return;
    const b=bossPose(S.t),body=S.bossCritical?'ovbody_critical':'ovbody_intact';
    drawArt(body,b.x,b.y,196,196,Math.sin(Math.max(0,S.t-16.8)*.54)*.08,1,false);
    const ri=Math.floor(S.t*18)%72;drawArt('ovrotor_'+String(ri).padStart(2,'0'),b.x,b.y,196,196,0,.88,false);
    if(S.t>16.05&&S.t<16.78){g.save();g.globalCompositeOperation='lighter';g.globalAlpha=.25+.25*Math.sin(S.t*24)**2;g.fillStyle=C.green;g.beginPath();g.arc(b.x,b.y,58+(S.t-16)*18,0,TAU);g.fill();g.restore();}
    if(S.bossCritical){
      for(let i=0;i<5;i++){const a=S.t*1.4+i*1.7,r=12+i*2;g.save();g.globalAlpha=.26;g.fillStyle='#111';g.beginPath();g.arc(b.x+36+Math.sin(a)*7,b.y-23-(S.t%1)*30-i*4,r,0,TAU);g.fill();g.restore();}
      g.save();g.strokeStyle=C.red;g.lineWidth=2;g.beginPath();g.moveTo(b.x+35,b.y+18);g.lineTo(b.x+55,b.y+34);g.stroke();g.restore();
      text('RIGHT POD DISABLED',b.x+56,b.y+66,7,'#ff796d');
    }
  }
  function drawPhase(){
    let title,detail,foot;
    if(S.t<7.4){title='TEST 01 — RESERVED FORMATION PASS';detail='4 AIRCRAFT • 111 PX SLOT SPACING • NO BODY OVERLAP';foot='TRACERS 305 PX/S • 6-ROUND BURSTS • 0.10s GAP';}
    else if(S.t<14.4){title='TEST 02 — DURABLE ANCHOR + SUPPORT';detail='TANK COMMITS SOUTH • PAUSE / FIRE / RECOVER';foot='CANNON 188 PX/S • SUPPORT TRACERS 325 PX/S';}
    else if(S.t<16.8){title='BOSS TEST — REVEAL IS THE TELEGRAPH';detail='SHUTTERS OPEN • SILHOUETTE HOLD • WEAPONS STAY COLD';foot='1.38s REVEAL • 0.75s RECOGNITION BEAT';}
    else if(S.t<24){title='JUNGLE OVERLORD-X — INDEPENDENT HARDPOINTS';detail='SLOW HULL SLIDE • TWIN MG • SHOOTABLE MISSILES • CURVED WIND';foot='MG 318 PX/S • MISSILE 118→215 PX/S • WIND 165 PX/S';}
    else if(S.t<30.4){title='JUNGLE OVERLORD-X — MOVING SAFE DOOR';detail='6 LANES • 2-LANE OPENING • DOOR MOVES ONLY ONE LANE';foot='0.9s WARNING • 1.25s COMMIT • FULL RECOVERY';}
    else if(S.t<35.2){title='JUNGLE OVERLORD-X — LOCAL DAMAGE STATE';detail='CRITICAL HULL • ONE HARDPOINT DISABLED • FASTER SURVIVING GUN';foot='VISIBLE DAMAGE CHANGES THE ATTACK, NOT JUST THE PALETTE';}
    else{title='PATTERN LAB COMPLETE';detail='PROTOTYPE ONLY — PRODUCTION GAME CODE UNCHANGED';foot='ALL SIX READABILITY CONTRACTS COMPLETED WITH LIZZIE';S.completed=true;}
    panel(title,detail);banner(foot,S.t<30.4?C.gold:C.green);
    S.phase=title;window.__patternLab={t:S.t,phase:title,shots:S.shots.length,metrics:S.metrics,completed:S.completed,errors:window.__qaErrors||[]};
  }

  function draw(){
    g.clearRect(0,0,W,H);g.imageSmoothingEnabled=false;
    drawJets();drawAnchorWave();drawShutters();drawBoss();drawBeams();drawShots();drawPhase();
    if(S.t<1.0){g.save();g.globalAlpha=1-S.t;g.fillStyle='#fff';g.fillRect(0,0,W,H);g.restore();}
  }
  function fireLizzie(dt){
    fireLizzie.cd=(fireLizzie.cd||0)-dt;
    if(S.t>.7&&S.t<35&&fireLizzie.cd<=0){fireLizzie.cd=.16;try{if(typeof pShoot==='function')pShoot();}catch(_){}}
  }
  function reset(){
    S.t=0;S.last=performance.now();S.shots.length=0;S.smoke.length=0;S.sparks.length=0;S.playerX=240;S.playerY=442;
    S.bossCritical=false;S.disabledPod=0;S.completed=false;S.metrics={maxShots:0,closest:999,events:0,intercepts:0,beamDoors:[2,2]};
    buildEvents();fireLizzie.cd=0;
    try{
      run.pilot='lizzie';const pi=PILOTS.findIndex(p=>p.key==='lizzie');if(pi>=0)pilotIndex=pi;
      beginStage(1);setState(GS.PLAY);player.reset();player.invuln=1e9;player.x=400;player.y=S.playerY;
      run.weapon=0;run.wlevels=[1,0,0,0,0,0];run.wlevel=1;run.missileLevel=0;
      stagePlan=[];waveIdx=0;stageTimer=0;mapScroll=2280;camX=160;
      enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
      boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;pwTimer=-9999;spTimer=-9999;
      bossWarned=true;subBossDone=true;subBossTriggered=true;warnKind=null;warnT=0;
      _sc1=true;_sc2=true;_mc1=true;_mc2=true;_bossCard=null;
      /* Test-only camera lock: the wide jungle stage remains centered while Lizzie dodges. */
      updateCamX=function(){camX=160;};
    }catch(e){window.__qaErrors.push(String(e));}
  }
  function tick(now){
    if(!S.ready)return;
    const dt=Math.max(0,Math.min(.05,(now-S.last)/1000));S.last=now;S.t+=dt;
    while(S.eventI<S.events.length&&S.events[S.eventI].at<=S.t){try{S.events[S.eventI].fn();}catch(e){window.__qaErrors.push(String(e));}S.eventI++;}
    updatePlayer(dt);updateShots(dt);fireLizzie(dt);draw();requestAnimationFrame(tick);
  }
  function prewarm(){
    const keys=['ship_lizzie','nef_s1_camo_attack_jet_intact','nef_s1_jungle_bomber_intact','nef_s1_jungle_tank_intact','ovbody_intact','ovbody_critical'];
    for(let i=0;i<72;i++)keys.push('ovrotor_'+String(i).padStart(2,'0'));
    for(const k of keys)art(k);
    return keys.slice(0,6).every(k=>!!art(k));
  }
  function boot(){
    if(!(typeof window.__bofFrames==='number'&&window.__bofFrames>12&&typeof XART!=='undefined'))return setTimeout(boot,60);
    if(!prewarm())return setTimeout(boot,60);
    reset();S.ready=true;window.__patternLabReady=true;requestAnimationFrame(tick);
  }
  addEventListener('keydown',e=>{if(e.key.toLowerCase()==='r')reset();});
  boot();
})();
