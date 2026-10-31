/* DESERT BREAKER replaces the retired museum in campaign/password slot 5.
 * Four mixed armor/air formations enter north of the visible field. */
(function(root){
  'use strict';
  const TD=root.TD,M=TD.M,W=TD.World,A=TD.Audio,FX=TD.FX,Cam=TD.Cam;
  root.TD_ASSAULT_ART.assets.od_desert_ground={file:'expansion/topdown/art/desert_1013/desert_ground.png',size:[800,1200],anchor:[0,0]};
  TD.ET.desertAir={hp:9,r:27,airborne:true,art:'of_scout_air_idle',wreck:'of_scout_air_wreck',ds:.88,speed:2.8,score:1000,vis:{range:800,half:Math.PI},cd:2.7};
  const tick=TD.unitTick,draw=TD.drawUnit,hit=TD.hitUnit;
  TD.unitTick=function(u,G,dt){if(u.type!=='desertAir')return tick(u,G,dt);if(u.dead)return;
    const p=G.player;u.airborne=true;u.flash=Math.max(0,u.flash-dt);u.age=(u.age||0)+dt;u.fireCd-=dt;
    const target=u.entering?{x:u.entryX,y:u.entryY}:u.airGoal||(u.airGoal={x:M.clamp(p.x+(u.lane||1)*150,150,650),y:Math.max(190,p.y-210)});
    if(M.dist(u.x,u.y,target.x,target.y)<40){if(u.entering)u.entering=false;u.lane=-(u.lane||1);u.airGoal={x:M.clamp(p.x+u.lane*190,130,670),y:M.clamp(p.y-200+Math.sin(u.age)*55,160,900)};}
    const want=M.angTo(u.x,u.y,target.x,target.y);u.a=M.turnTo(u.a,want,dt*2.1);const f=M.fwd(u.a),speed=u.entering?155:105;u.x+=f[0]*speed*dt;u.y+=f[1]*speed*dt;u.look=M.angTo(u.x,u.y,p.x,p.y);u.mode='alert';u.aware=1;
    if(!u.entering&&!p.dead&&u.fireCd<=0){u.fireCd=2.7;const a=u.look,v=M.fwd(a);G.eshots.push({k:'missile',x:u.x,y:u.y,a,vx:v[0]*2.8,vy:v[1]*2.8,dmg:2,r:6,t:0,life:170,shootable:true,homing:26,turn:.013});FX.flash(u.x,u.y,a,.16);A.play('missileLaunch',.4);}
  };
  TD.drawUnit=function(ctx,u){if(u.type!=='desertAir')return draw(ctx,u);if(u.dead)return;const o={a:u.a+Math.PI,s:.88};ART.draw(ctx,'of_scout_air_idle',u.x+17,u.y+23,{...o,tint:'#211b18',alpha:.36});ART.draw(ctx,'of_scout_air_idle',u.x,u.y,{...o,flash:u.flash>0?1:0});};
  TD.hitUnit=function(G,u,dmg,x,y,silent){const was=u.dead;hit(G,u,dmg,x,y,silent);if(!was&&u.dead&&G.mission===5){G.desert.defeated++;if(u.type==='desertAir'||G.desert.defeated%3===0)TD.dropPickup(G,M.clamp(u.x,130,670),M.clamp(u.y,170,1050),u.type==='desertAir'?'smoke':'repair');}};
  const waves=[['jackal','desertAir','jackal'],['manticore','desertAir','lancer','jackal'],['bastion','desertAir','manticore','desertAir'],['lancer','bastion','jackal','desertAir','manticore']];
  function deploy(G){const d=G.desert,types=waves[d.wave++];if(!types)return;const top=Cam.y,step=500/Math.max(1,types.length-1);d.pending=types.map((type,i)=>({type,x:types.length===1?400:150+i*step,delay:i*.65}));d.waveClock=0;G.say('NORTH CONTACTS - WAVE '+d.wave+'/4',G.player);A.play('warn',.3);}
  function enter(G,s){const margin=s.type==='desertAir'?105:130,y=Cam.y-margin;const u=TD.makeUnit(s.type,s.x,y,{a:0,mode:'alert',aware:1,entering:true,entryY:Cam.y+110,entryX:s.x,desert:true,lane:s.x<400?1:-1,fireCd:1.7,ramCd:4});u.spawnY=y;u.spawnTop=Cam.y;u.airborne=s.type==='desertAir';G.units.push(u);G.desert.entries.push({type:s.type,y,top:Cam.y,margin});}
  function setup(G){G.desert={wave:0,next:1.4,waveClock:0,pending:[],defeated:0,entries:[],clear:false,supplyT:0};G.player.missiles=12;G.player.weapons=[{id:'vulcan',lv:2}];G.player.wi=0;G.player.hp=G.player.max;G.units=[];TD.Stealth.phase='CAUTION';G.pickups.push({kind:'smoke',x:465,y:1000,t:0},{kind:'repair',x:335,y:1010,t:0});}
  function update(G,dt){const d=G.desert;if(!d||G.player.dead)return;d.waveClock+=dt;
    // Pending spawns remain plain schedule entries until their offscreen entry.
    while(d.pending.length&&d.pending[0].delay<=d.waveClock)enter(G,d.pending.shift());
    const live=G.units.filter(u=>!u.dead).length;if(!live&&!d.pending.length&&!d.clear){if((d.next-=dt)<=0){if(d.wave<waves.length){deploy(G);d.next=2.7;G.player.missiles=Math.min(12,G.player.missiles+4);G.say('MISSILES RESUPPLIED',G.player);}else{d.clear=true;G.ghost=false;G.bossDown();G.say('DESERT CORRIDOR CLEAR',G.player);}}}
    d.supplyT+=dt;if(d.supplyT>20&&G.player.missiles<3){d.supplyT=0;TD.dropPickup(G,G.player.x+50,G.player.y,'smoke');}
    // Keep the engagement below its northern entry so all reinforcements can
    // drive/fly through the visible edge instead of appearing at a border.
    G.player.y=M.clamp(G.player.y,360,1110);G.player.x=M.clamp(G.player.x,125,675);
  }
  function hud(ctx,text,G){const p=G.player,d=G.desert,w=p.weapons[p.wi];ctx.fillStyle='rgba(27,18,10,.86)';ctx.fillRect(8,7,TD.VW-16,50);
    text('DESERT BREAKER',18,20,12,'#ffe6ae');text('WAVE '+Math.max(1,d.wave)+' / 4',TD.VW-18,20,12,'#ffd06c','right');
    text('ARMOR '+Math.ceil(p.hp)+' / '+p.max,18,42,10,p.hp<4?'#ff7559':'#97efae');text(TD.WPN[w.id].name+' Lv'+w.lv,190,42,10,'#fff');text('MISSILES '+p.missiles,TD.VW-18,42,10,'#9adfff','right');
    text(p.retina?.locked?'RETINA LOCK - FIRE CANNON':p.retina?.phase==='seek'?'RETINA ACQUIRING':'RETINA + CANNON: SHOOT DOWN AIRCRAFT',TD.VW/2,TD.VH-16,10,p.retina?.locked?'#8dffbd':'#ffe6ae','center');
    if(p.boosting)text('OVERDRIVE',TD.VW/2,78,12,'#ffd070','center');else if(d.pending.length)text('REINFORCEMENTS APPROACHING FROM NORTH',TD.VW/2,76,10,'#ffca88','center');return true;}
  const mission={id:5,mode:'tank',view640:true,arcadeAssault:true,cameraOwns:true,map:{key:'od_desert_ground',w:800,h:1200,rects:[[0,0,100,1200,'b'],[700,0,800,1200,'b']]},data:{title:'LEVEL 5',name:'DESERT BREAKER',brief:['AN OPEN DESERT CORRIDOR IS UNDER ARMORED OCCUPATION.','DESTROY FOUR MIXED TANK AND AIR FORMATIONS.','USE RETINA AND CANNON MISSILES TO SHOOT AIRCRAFT DOWN.','WATCH THE CHARGE WARNING. BOOST ASIDE BEFORE THEY RAM.'],start:{x:400,y:1030,a:Math.PI},checkpoints:[[400,820],[400,570]],gates:[],bossLine:-1000,boss:{x:400,y:0},units:[],props:[],structures:[]},setup,tick:update,boss:null,canReinforce:()=>false,cam(G){Cam.zoom=1;Cam.follow(G.player.x,G.player.y-85,.10);},hud,score(G,R){R.extraRows=[['ARMORED FORMATIONS',G.desert.wave],['HOSTILES DESTROYED',G.desert.defeated]];}};
  TD.MISSIONS[TD.MISSIONS.findIndex(m=>m.id===5)]=mission;
  TD.Desert={setup,deploy,enter,update,waves,mission};
  TD.CAMPAIGN_WARM.push('od_desert_ground','of_scout_air_idle','of_scout_air_wreck');
})(window);
