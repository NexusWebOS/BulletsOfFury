/* Authored armor with continuous steering, acceleration, muzzle timing and warned rams. */
(function(root){
  'use strict';
  const TD=root.TD,M=TD.M,W=TD.World,FX=TD.FX,art=TD.AssaultArt,A=TD.Audio;
  const defs={jackal:{hp:10,speed:2.35,r:31,gun:'burst',cd:1.6,prefer:[115,225],score:650,ds:.44,ram:true},lancer:{hp:17,speed:1.55,r:34,gun:'snipe',cd:2.8,warn:.6,prefer:[220,315],score:1100,ds:.46},manticore:{hp:23,speed:1.45,r:36,gun:'rocket',cd:3.6,warn:.55,prefer:[190,280],score:1250,ds:.48},bastion:{hp:38,speed:1.1,r:44,gun:'twin',cd:2.6,warn:.5,prefer:[145,230],score:1800,ds:.53,ram:true}};
  for(const [name,def] of Object.entries(defs))TD.ET[name]=Object.assign({odTank:name,art:'od_'+name+'_0',wreck:'od_'+name+'_3',vis:{range:380,half:.9}},def);
  const oldDraw=TD.drawUnit,oldHit=TD.hitUnit,oldTick=TD.unitTick;
  // The old alternate hull drawings changed silhouette on every tread tick.
  // Keep the calibrated hull stable; movement and recoil are continuous.
  TD.drawUnit=function(ctx,u){const d=TD.ET[u.type];if(!d.odTank)return oldDraw(ctx,u);if(u.dead)return;
    const f=M.fwd(u.a),recoil=(u.armorRecoil||0)*2.5,opts={s:d.ds,a:u.a+Math.PI};
    art.draw(ctx,d.art,u.x+4,u.y+5,{...opts,tint:'#000000',alpha:.35});
    art.draw(ctx,d.art,u.x-f[0]*recoil,u.y-f[1]*recoil,{...opts,flash:u.flash>0?1:0});
    if(u.ramState==='warn'||u.fireWarn>0){const k='tank_charge_'+Math.floor((u.armorAge||0)*10)%4;ART.draw(ctx,k,u.x+f[0]*48,u.y+f[1]*48,{s:.27});}
  };
  function shoot(u,G,d){
    const f=M.fwd(u.look),mx=u.x+f[0]*(u.r+13),my=u.y+f[1]*(u.r+13),gun=d.gun;
    if(gun==='burst'){u.armorBurst=4;u.armorBurstT=0;}
    else for(const offset of gun==='rocket'?[-.16,0,.16]:gun==='twin'?[-.07,.07]:[0]){const a=u.look+offset,v=M.fwd(a),speed=gun==='snipe'?7.5:gun==='rocket'?3.1:4.8;
      G.eshots.push({k:gun==='rocket'?'missile':gun==='snipe'?'snipe':'shell',x:mx,y:my,vx:v[0]*speed,vy:v[1]*speed,a,dmg:2,life:140,r:gun==='rocket'?6:5,t:0,shootable:gun==='rocket',homing:gun==='rocket'?22:0,turn:.016});}
    u.armorRecoil=1;u.armorFire=.15;FX.flash(mx,my,u.look,.23);A.play(gun==='rocket'?'missileLaunch':gun==='snipe'?'railCannon':'gd_tankCannon',.4);
  }
  function travel(u,target,speed,G,dt,reverse){
    const n=dt*60;let ax=target.x-u.x,ay=target.y-u.y;
    if(!u.entering&&W.rayBlock(u.x,u.y,target.x,target.y)){const v=TD.Nav.step(TD.Nav.field(target.x,target.y,G.t/60),u.x,u.y);if(v){ax=v[0];ay=v[1];}}
    const want=M.angTo(0,0,ax,ay),heading=reverse?M.wrap(want+Math.PI):want,rate=(u.type==='bastion'?.025:.047)*n;
    u.a=M.turnTo(u.a,heading,rate);u.look=u.a;
    const alignment=Math.max(0,Math.cos(M.wrap(heading-u.a))),goal=speed*alignment*(reverse?-.65:1);
    u.armorSpeed=M.lerp(u.armorSpeed||0,goal,1-Math.exp(-dt*5));
    const f=M.fwd(u.a);u.x+=f[0]*u.armorSpeed*n;u.y+=f[1]*u.armorSpeed*n;
  }
  TD.unitTick=function(u,G,dt){const d=TD.ET[u.type];if(d.still||d.foot||!(d.odTank||d.et||d.mod))return oldTick(u,G,dt);if(u.dead)return;
    const p=G.player,x=u.x,y=u.y;u.armorSpeed??=0;u.armorAge=(u.armorAge||0)+dt;u.flash=Math.max(0,u.flash-dt);u.armorRecoil=(u.armorRecoil||0)*Math.exp(-dt*14);u.armorFire=Math.max(0,(u.armorFire||0)-dt);
    if(u.stunned>0){u.stunned-=dt;return;}
    const dist=M.dist(u.x,u.y,p.x,p.y),to=M.angTo(u.x,u.y,p.x,p.y),seen=!p.dead&&!W.rayBlock(u.x,u.y,p.x,p.y);
    u.ramCd=(u.ramCd??(5+(u.x%4)))-dt;
    if(u.entering){travel(u,{x:u.entryX??u.x,y:u.entryY},d.speed*1.25,G,dt);if(u.y>=u.entryY)u.entering=false;}
    else if(u.ramState==='warn'){
      u.armorSpeed*=Math.exp(-dt*10);u.a=M.turnTo(u.a,u.ramAim,.025*dt*60);u.look=u.a;
      if((u.ramT-=dt)<=0){u.ramState='charge';u.ramT=1.3;u.ramAim=u.a;}
    }else if(u.ramState==='charge'){
      u.a=u.look=u.ramAim;u.armorSpeed=M.lerp(u.armorSpeed||0,d.speed*2.6,1-Math.exp(-dt*8));const f=M.fwd(u.a);u.x+=f[0]*u.armorSpeed*dt*60;u.y+=f[1]*u.armorSpeed*dt*60;
      if((u.ramT-=dt)<=0){u.ramState=null;u.ramCd=7;}
    }else if(u.mode==='alert'||G.mission===5&&G.desert){
      u.mode='alert';u.aware=1;u.sees=seen;
      if(d.ram&&seen&&u.y>TD.Cam.y+70&&u.y<TD.Cam.y+TD.VH-25&&u.x>TD.Cam.x+40&&u.x<TD.Cam.x+TD.VW-40&&dist>120&&dist<290&&Math.abs(M.wrap(to-u.a))<.28&&u.ramCd<=0){u.ramState='warn';u.ramT=.9;u.ramAim=to;G.say('RAM CHARGE',u);A.play('warn',.3);}
      const [lo,hi]=d.prefer;
      if(dist>hi||!seen)travel(u,p,d.speed,G,dt);
      else if(dist<lo)travel(u,p,d.speed,G,dt,true);
      else{u.armorSpeed*=Math.exp(-dt*8);u.a=M.turnTo(u.a,to,.038*dt*60);u.look=u.a;const f=M.fwd(u.a);u.x+=f[0]*u.armorSpeed*dt*60;u.y+=f[1]*u.armorSpeed*dt*60;}
    }else{
      const goal=u.goal||(u.wp?.length?{x:u.wp[u.wi][0],y:u.wp[u.wi][1]}:null);
      if(goal){travel(u,goal,d.speed*.7,G,dt);if(M.dist(u.x,u.y,goal.x,goal.y)<20&&u.wp)u.wi=(u.wi+1)%u.wp.length;}
      else u.armorSpeed=(u.armorSpeed||0)*Math.exp(-dt*8);
    }
    if(!u.entering){
      for(const q of G.props)if(!q.dead)TD.pushOut(u,q);
      for(const q of G.units)if(q!==u&&!q.dead&&!q.airborne&&!q.entering){const dx=u.x-q.x,dy=u.y-q.y,dd=Math.hypot(dx,dy),gap=u.r+q.r;if(dd>0.1&&dd<gap){const k=Math.min(2*dt*60,(gap-dd)*.22);u.x+=dx/dd*k;u.y+=dy/dd*k;}}
      const wall=W.collide(u,u.r,false);if(wall&&u.ramState==='charge'){u.ramState=null;u.ramCd=8;u.armorSpeed=0;FX.concrete(u.x,u.y,70);}
    }
    const moved=Math.hypot(u.x-x,u.y-y);u.armorTravel=(u.armorTravel||0)+moved;
    if(d.mod){u.trackDistance=u.trackDistance||[0,0];u.trackDistance[0]+=moved;u.trackDistance[1]+=moved;u.recoil=(u.armorRecoil||0)*3;}
    if(moved>.25&&Math.floor(u.armorTravel/16)!==Math.floor((u.armorTravel-moved)/16)){const f=M.fwd(u.a);FX.smoke(u.x-f[0]*u.r,u.y-f[1]*u.r,.07,.45);}
    if(!p.dead&&M.dist(u.x,u.y,p.x,p.y)<u.r+p.r){if(u.ramState==='charge'){TD.hurtPlayer(G,3,p.x,p.y);u.ramState=null;u.ramCd=8;u.armorSpeed*=.25;}TD.pushOut(p,u);W.collide(p,p.r,false);}
    if(u.armorBurst>0&&(u.armorBurstT-=dt)<=0){u.armorBurst--;u.armorBurstT=.1;const a=u.look+M.rnd(-.035,.035),f=M.fwd(a);G.eshots.push({k:'mg',x:u.x+f[0]*(u.r+10),y:u.y+f[1]*(u.r+10),vx:f[0]*4.6,vy:f[1]*4.6,a,dmg:1,r:4,life:110,t:0});u.armorFire=.1;FX.flash(u.x+f[0]*(u.r+10),u.y+f[1]*(u.r+10),a,.18);}
    if(!u.entering&&!u.ramState&&seen&&dist<380&&Math.abs(M.wrap(to-u.look))<.16){if(u.fireWarn>0){if((u.fireWarn-=dt)<=0){shoot(u,G,d);u.fireCd=d.cd;}}
      else if((u.fireCd-=dt)<=0){if(d.warn)u.fireWarn=d.warn;else{shoot(u,G,d);u.fireCd=d.cd;}}}
  };
  TD.hitUnit=function(G,u,dmg,x,y,silent){const was=u.dead;oldHit(G,u,dmg,x,y,silent);const t=TD.ET[u.type];if(!was&&u.dead&&t.odTank){const w=G.wrecks.at(-1);if(w&&w.x===u.x&&w.y===u.y){w.art=t.wreck;w.still=true;w.s=t.ds;}FX.concrete(u.x,u.y,80);A.play('expBoss',.35);}};
  for(const m of TD.MISSIONS.filter(m=>m.mode==='tank')){const types=m.id===2?['jackal','lancer','manticore','bastion']:['manticore','jackal','lancer','bastion'];let i=0;for(const u of m.data.units)if(!['camera','turret'].includes(u.type)&&i<4)u.type=types[i++];}
})(window);
