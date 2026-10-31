/* Gosfer's shield belongs to the arena barriers. All damage and transitions
 * use the ordinary projectile/cover pipeline; dialogue is protected combat. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,I=TD.Input,W=TD.World,A=TD.Audio,FX=TD.FX,art=TD.AssaultArt,pack=root.TD_ASSAULT_ART;
 const seq=(n,k)=>{const q=pack.sequences[n];return q?.frames[Math.max(0,Math.min(q.frames.length-1,k))];};
 const mission=TD.MISSIONS.find(m=>m.id===3),baseHit=TD.hitStructure,baseImpact=TD.structureImpact;
 TD.structureImpact=function(G,s,...args){const prior=TD.coverDamageSource;TD.coverDamageSource=s;try{return baseImpact(G,s,...args);}finally{TD.coverDamageSource=prior;}};
 TD.hitStructure=function(G,s,dmg,ram){if(s.gosferBarrier&&G.boss?.shield&&TD.coverDamageSource?.owner!==G.boss){s.flash=.12;return true;}const was=s.dead,result=baseHit(G,s,dmg,ram);if(!was&&s.dead&&s.gosferBarrier){s.brokenBy=TD.coverDamageSource?.owner===G.boss?'gosfer':'other';G.boss?.barrierLog.push({x:s.x,y:s.y,at:G.time,by:s.brokenBy});}return result;};
 const bodyHit=(b,s)=>{const rx=37+(s.r||0),ry=61+(s.r||0),ax=(s.x-s.vx-b.x)/rx,ay=(s.y-s.vy-(s.drawLift||0)-(b.y-70))/ry,dx=s.vx/rx,dy=s.vy/ry,t=M.clamp(-(ax*dx+ay*dy)/(dx*dx+dy*dy||1),0,1);return Math.hypot(ax+dx*t,ay+dy*t)<=1;};
 function pose(b){let bank='pb20_gosfer_fire_south',n=0,flip=false;
  if(b.dead){bank='pb19_gosfer_death';n=Math.min(7,Math.floor(b.t*9));}
  else if(b.state==='roll'){bank='pb20_gosfer_roll';n=Math.min(7,Math.floor(b.actionT/.56*8));flip=b.travel<0;}
  else if(b.state==='jump'){bank='pb20_gosfer_jump';n=Math.min(7,Math.floor(b.actionT/.9*8));}
  else if(b.state==='enter'&&b.vy>1){bank='pb20_gosfer_walk_south';n=Math.floor((b.gait||0)*8)%8;}
  else if(b.state==='move'){bank=b.phase===2?'pb20_gosfer_run':'pb20_gosfer_walk';n=Math.floor((b.gait||0)*8)%8;flip=b.vx<0;}
  else if(b.state==='strafe'){bank='pb20_gosfer_strafe';n=Math.floor((b.gait||0)*8)%8;flip=b.vx<0;}
  else if(b.state==='shoot'){bank=Math.abs(b.volleyTarget.x-b.x)>100?'pb20_gosfer_fire_angle':'pb20_gosfer_fire_south';n=3+Math.floor(b.actionT*22)%4;flip=bank.endsWith('angle')&&b.volleyTarget.x<b.x;}
  else if(b.state==='windup'){bank=Math.abs((b.volleyTarget?.x||b.x)-b.x)>100?'pb20_gosfer_fire_angle':'pb20_gosfer_fire_south';n=Math.min(2,Math.floor(b.actionT/(b.windup||.55)*3));flip=bank.endsWith('angle')&&b.volleyTarget.x<b.x;}
  else if(b.state==='recover'){bank=Math.abs((b.volleyTarget?.x||b.x)-b.x)>100?'pb20_gosfer_fire_angle':'pb20_gosfer_fire_south';n=b.actionT<.16?6:7;flip=bank.endsWith('angle')&&b.volleyTarget.x<b.x;}
  return {key:seq(bank,n),bank,phase:n,flip};
 }
 TD.gosferPose=pose;
 TD.gosferSocket=function(b){const z=TD.gosferPose(b),m=pack.assets[z.key],q=m.muzzle||[m.anchor[0]+10,m.anchor[1]-78];return {x:b.x+(q[0]-m.anchor[0])*(z.flip?-1:1),y:b.y-(b.jumpZ||0)+q[1]-m.anchor[1]};};
 TD.makeGosfer=function(G,x,y){
  const b={name:'GOSFER',x,y:100,homeY:250,state:'enter',t:0,actionT:0,hp:840,max:840,gauge:0,a:0,aim:0,flash:0,r:23,dead:false,shield:true,phase:1,gait:0,vx:0,pattern:0,targetX:520,barrierLog:[],dialogueLog:[],retina:null};
  b.barriers=[[300,310,'od_barrier'],[530,310,'od_barrier'],[400,365,'od_bosswall']].map(([x,y,kind])=>{let s=G.structures.find(s=>s.kind===kind&&s.x===x&&s.y===y&&!s.dead);if(!s){s=TD.makeStructure({kind,x,y});G.structures.push(s);}s.gosferBarrier=true;s.hp=s.max;s.brokenBy=null;return s;});
  b.remaining=()=>b.barriers.filter(s=>!s.dead);
  b.alive=()=>!b.dead;b.hpFrac=()=>b.hp/b.max;b.aimPoint=()=>({x:b.x,y:b.y,r:b.r});b.aim=b.aimPoint;b.retinaTargets=()=>[{id:b,point:()=>b,valid:()=>!b.dead&&!b.shield&&!['enter','dialogue','transform'].includes(b.state)}];
  b.hit=(x,y,r,d,s)=>{if(b.dead||(s?!bodyHit(b,s):Math.hypot(x-b.x,y-b.y)>b.r+r))return false;if(b.shield||['enter','dialogue','transform'].includes(b.state)){b.shieldFlash=.14;return true;}if((b.state==='roll'&&b.actionT>.08&&b.actionT<.43)||(b.state==='jump'&&b.jumpZ>24))return true;b.hp=Math.max(0,b.hp-d);b.flash=.10;if(!b.hp){b.dead=true;b.state='defeated';b.t=0;TD.Escape29.defeated(G);G.say('GOSFER: DRACODIA... WILL FINISH THIS.',G.player);FX.boom(b.x,b.y,125,'gfx_destruction_',6);A.play('expBoss');}return true;};b.blast=(x,y,r,d)=>b.hit(x,y,r,d);
  const change=(state)=>{b.state=state;b.actionT=0;b.sent=0;};
  const beginDialogue=()=>{b.shield=false;b.state='dialogue';b.dialogueT=0;b.line=0;b.lineT=0;b.retina=null;G.shots=[];G.eshots=[];G.units=[];G.msgs=[];b.dialogueLog.push({line:0,at:G.time});A.fadeMusic(.18,.6);A.play('shieldBreak',.6);};
  const attack=()=>{const p=G.player;b.attack=b.phase===1?['breaker','laser','jump','breaker'][b.pattern%4]:['laser','retina','jump','laser','retina','jump'][b.pattern%6];b.pattern++;b.barrierTarget=b.attack==='breaker'?b.remaining()[0]:null;b.volleyTarget=b.barrierTarget?{x:b.barrierTarget.x,y:b.barrierTarget.y}:{x:p.x,y:p.y};b.lockPoint={...b.volleyTarget};b.windup=b.attack==='retina'?.95:b.attack==='breaker'?.65:b.phase===2?.38:.55;if(b.attack==='retina')b.retina={x:p.x,y:p.y,t:0,locked:false};change(b.attack==='jump'?'jump':'windup');if(b.attack==='jump'){const wall=b.remaining().sort((a,c)=>Math.abs(a.y-b.y)-Math.abs(c.y-b.y))[0];b.jumpFrom={x:b.x,y:b.y};b.jumpTo={x:M.clamp(wall?wall.x:p.x+(b.x<p.x?110:-110),210,590),y:wall?wall.y+(b.y<wall.y?64:-64):b.y<300?395:220};b.homeY=b.jumpTo.y;b.vaultCount29=(b.vaultCount29||0)+1;}};
  b.tick=function(dt){b.t+=dt;b.actionT+=dt;b.flash=Math.max(0,b.flash-dt);b.shieldFlash=Math.max(0,(b.shieldFlash||0)-dt);b.firing=Math.max(0,(b.firing||0)-dt);if(b.dead)return;const p=G.player;
   if(b.state==='enter'){const moved=Math.min(130*dt,b.homeY-b.y);b.vy=moved/dt;b.y+=moved;b.vx=0;b.gait+=moved/72;b.gauge=Math.min(1,b.t/2);G.fortress.doorOpen=true;if(b.t>2.6){change('move');A.playMusic('lastHope',1.8);}return;}
   if(b.shield&&!b.remaining().length){beginDialogue();return;}
   if(b.state==='dialogue'){b.dialogueT+=dt;b.lineT+=dt;const lengths=[2.8,2.1,5.6];if(b.lineT>=lengths[b.line]||b.lineT>.85&&I.tap('A')){if(b.line<2){b.line++;b.lineT=0;b.dialogueLog.push({line:b.line,at:G.time});}else{change('transform');b.transformT=0;}}return;}
   if(b.state==='transform'){b.transformT+=dt;if(b.transformT>3.2){b.phase=2;b.state='move';b.actionT=0;b.targetX=b.x>400?240:560;b.pattern=0;p.inv=45;G.shots=[];G.eshots=[];A.fadeMusic(1,1.8);G.say('PRONE EVADES LASERS / MOVE WHEN RETINA LOCKS',p);}return;}
   const ox=b.x,oy=b.y;b.angle=M.angTo(b.x,b.y,p.x,p.y);
   if(b.state==='move'||b.state==='strafe'){const dx=b.targetX-b.x,sp=b.phase===2?250:135;b.vx=M.lerp(b.vx,Math.sign(dx)*sp,.16);b.x+=b.vx*dt;b.y=M.lerp(b.y,b.homeY,.06);if(Math.abs(dx)<7||b.actionT>(b.phase===2?.68:1.45)){if(b.pattern%3===1){b.travel=b.x>400?-1:1;change('roll');}else attack();}}
   else if(b.state==='roll'){b.vx=b.travel*330;b.x+=b.vx*dt;if(b.actionT>.56)attack();}
   else if(b.state==='jump'){b.vx=0;const u=M.clamp((b.actionT-.12)/.66,0,1),e=u*u*(3-2*u);b.x=M.lerp(b.jumpFrom.x,b.jumpTo.x,e);b.y=M.lerp(b.jumpFrom.y,b.jumpTo.y,e);b.jumpZ=Math.sin(u*Math.PI)*88;if(b.actionT>.9){b.jumpZ=0;b.attack='laser';b.volleyTarget={x:p.x,y:p.y};b.windup=.32;change('windup');}}
   else if(b.state==='windup'){b.vx=0;if(b.retina){b.retina.t+=dt;if(b.actionT<.6){b.retina.x=p.x;b.retina.y=p.y;}else if(!b.retina.locked){b.retina.locked=true;b.volleyTarget={x:b.retina.x,y:b.retina.y};A.play('locked',.4);}}if(b.actionT>b.windup)change('shoot');}
   else if(b.state==='shoot'){const mg=b.attack==='retina',breaker=b.attack==='breaker',interval=mg?.055:b.phase===2?.045:breaker?.075:.075,count=mg?20:breaker?26:b.phase===2?24:12;
    while(b.sent<count&&b.actionT>=b.sent*interval){const socket=TD.gosferSocket(b),offset=breaker?0:mg?Math.sin(b.sent*2.4)*.018:(b.sent-(count-1)/2)*.023,a=M.angTo(socket.x,b.y,b.volleyTarget.x,b.volleyTarget.y)+offset,f=M.fwd(a);G.eshots.push({owner:b,k:mg?'mg':'laser',x:socket.x,y:b.y,a,vx:f[0]*(mg?7.4:b.phase===2?8.2:6.8),vy:f[1]*(mg?7.4:b.phase===2?8.2:6.8),dmg:breaker?4:1,life:115,r:mg?3:4,t:0,drawLift:b.y-socket.y,liftStart:b.y-socket.y,liftEnd:breaker?(b.barrierTarget.kind==='od_bosswall'?25:16):mg?15:45,spawnX:socket.x,spawnY:b.y,flightDist:Math.hypot(b.volleyTarget.x-socket.x,b.volleyTarget.y-b.y),hitsProne:mg,barrierBreaker:breaker});b.angle=a;b.firing=.10;FX.attachedFlash(b,TD.gosferSocket,a,.10);b.sent++;if(b.sent%3===1)A.play(mg?'gd_soldierRifle':'enemyHeavyLaser',.32);}
    if(b.actionT>count*interval+.13){change('recover');b.retina=null;}}
   else if(b.state==='recover'&&b.actionT>(b.phase===2?.48:.6)){b.targetX=b.x>400?240:560;change(b.phase===1&&b.pattern%2?'strafe':'move');}
   b.x=M.clamp(b.x,205,595);b.y=M.clamp(b.y,175,415);if(b.state!=='jump')W.collide(b,20,false);b.gait=(b.gait+Math.hypot(b.x-ox,b.y-oy)/(b.phase===2?85:68))%1;
  };
  b.drawUnder=function(ctx){if(b.shield){const q=b.barrierTarget;if(q&&!q.dead){ctx.strokeStyle='#ffac44';ctx.lineWidth=2;ctx.setLineDash([6,4]);ctx.strokeRect(q.rect.x0-5,q.rect.y0-5,q.type.hw*2+10,q.type.hh*2+10);ctx.setLineDash([]);}}};
  b.draw=function(ctx){const z=TD.gosferPose(b);ctx.save();ctx.translate(b.x,b.y-(b.jumpZ||0));if(z.flip)ctx.scale(-1,1);art.draw(ctx,z.key,3,4,{s:1,tint:'#000',alpha:.28});const energized=b.phase===2||b.state==='transform',pulse=Math.sin(b.t*42);if(energized){ctx.shadowColor=pulse>0?'#adffff':'#b974ff';ctx.shadowBlur=14;}art.draw(ctx,z.key,0,0,{s:1,flash:b.flash>0?.7:0,alpha:b.dead?Math.max(0,1-b.t/2):energized?.52+.48*(pulse+1)/2:1});if(energized&&pulse>.35)art.draw(ctx,z.key,0,0,{s:1,tint:pulse>.75?'#a9ffff':'#a26cff',alpha:.23});ctx.restore();if(b.shield)art.draw(ctx,seq('pb20_gosfer_shield',Math.floor(b.t*16)%8),b.x,b.y-70,{s:1,alpha:b.shieldFlash>0?.55:.30});};
  b.drawOver=function(ctx){if(b.retina){const r=b.retina;art.draw(ctx,'pb20_icon_retina',r.x,r.y-18,{s:.65,alpha:r.locked?1:.65});}if(b.state==='transform'&&b.transformT>.45){art.draw(ctx,seq('pb20_gosfer_lightning',Math.floor(b.transformT*18)%8),b.x,b.y-70,{s:1,alpha:.8});}};
  return b;
 };
 mission.boss=TD.makeGosfer;
 const pre=mission.pre,over=mission.drawOver;
 mission.pre=function(G){pre(G);const p=G.player,b=G.boss;if(b&&['dialogue','transform'].includes(b.state)){p.scripted=true;p.inv=10;p.firing=0;p.roll=0;p.action=null;p.vx=p.vy=0;p.moving=false;G.shots=[];G.eshots=[];} };
 mission.drawOver=function(ctx,G){over(ctx,G);const p=G.player;if(p.cover&&p.y>=p.cover.y&&p.prone)TD.drawStructures(ctx,{...G,structures:[p.cover]});const b=G.boss;if(b&&['dialogue','transform'].includes(b.state)){const amount=b.state==='transform'?.22+.44*M.clamp(b.transformT/1.5,0,1):b.line===2?.22*M.clamp(b.lineT/4,0,1):0;ctx.fillStyle='rgba(1,2,12,'+amount+')';ctx.fillRect(TD.Cam.x,TD.Cam.y,TD.VW,TD.VH);b.draw(ctx);b.drawOver(ctx);}};
 const footPose=TD.footPose;
 TD.footPose=function(p){if(p.pilot==='yuri'&&!p.dead&&!p.action&&!p.jump){let n,bank;if(p.cover&&p.stanceTransition?.t<.46&&!p.roll){bank='pb19_yuri_north_prone_transition';n=Math.min(7,Math.floor(p.stanceTransition.t/.46*8));if(p.stanceTransition.to==='stand')n=7-n;}else if(p.roll>0){bank=p.rollProne?'pb20_yuri_roll_prone':'pb20_yuri_roll_stand';n=Math.min(7,Math.floor((.5-p.roll)/.5*8));}else if(p.cover&&!p.peekExposed&&!p.blindfire&&p.peek<=0){bank=p.prone?'pb20_yuri_wall_prone':'pb20_yuri_wall_crouch';n=p.moving?Math.floor((p.gaitPhase||0)*8)%8:0;}if(bank)return{key:seq(bank,n),scale:1,angle:0,action:bank,dir:'north'};}return footPose(p);};
 function panel(ctx,k,x,y,s=1){art.draw(ctx,k,x,y,{s});}
 TD.ground20HUD=function(ctx,text,G,pseudo){const p=G.player,c=G.bastion,w=TD.VW,h=TD.VH;
  TD.CornerHUD26.draw(ctx,text,G,pseudo);
  if(G.boss?.alive()&&!G.boss.dead){ctx.save();if(G.mission===3&&!pseudo)ctx.translate(0,h-146);const b=G.boss;panel(ctx,'pb20_hud_boss',w/2,113);const frac=b.form==='helios'?(b.state==='enter'?M.clamp(b.t/1.3,0,1):M.clamp(b.hp/180,0,1)):b.state==='enter'?b.gauge??M.clamp(b.t/1.3,0,1):b.hp/b.max;ctx.fillStyle=b.shield?'#6addff':'#ffad35';ctx.fillRect(w/2-122,110,244*frac,9);if(b.form==='helios'){ctx.fillStyle='#ff4235';ctx.fillRect(w/2-122,110,244*(b.state==='enter'?M.clamp((b.t-1.3)/1.3,0,1):M.clamp((b.hp-180)/180,0,1)),9);ctx.save();ctx.beginPath();ctx.rect(w/2-122,110,244*(b.state==='enter'?M.clamp((b.t-1.3)/1.3,0,1):M.clamp((b.hp-180)/180,0,1)),9);ctx.clip();ctx.fillStyle='#ffb879';for(let i=0;i<12;i++)if((i+Math.floor(c.age*10))%3===0)ctx.fillRect(w/2-122+i*20,110,6,2);ctx.restore();}text(b.name+(b.shield?' / SHIELD LINKED':''),w/2,101,10,'#ffdda2','center');ctx.restore();}
  const b=G.boss;if(b?.retina)text(b.retina.locked?'RETINA LOCKED / MOVE!':'MACHINE GUN ACQUIRING / MOVE',w/2,144,11,'#ff8373','center');
  if(b&&['dialogue','transform'].includes(b.state)){const trans=b.state==='transform',fear=trans?Math.min(3,2+Math.floor(b.transformT/.45)):b.line===2?Math.min(2,Math.floor(b.lineT/1.3)):0;panel(ctx,seq('pb20_portrait_yuri',fear),74,h-126,.48);panel(ctx,seq('pb20_portrait_gosfer',trans?3:b.line===2?2:Math.floor(b.lineT*3)%2),w-74,h-126,.48);panel(ctx,'pb20_hud_dialogue',w/2,h-123);let name=trans?'YURI':b.line===1?'YURI':'GOSFER',lines=trans?['Dracodia...?!']:b.line===0?["It's just me and you now."]:b.line===1?['Who are you?']:["Name's Gosfer, Dracodia's right hand man.",'And he wanted me to send his regards.'];text(name,w/2,h-148,12, name==='YURI'?'#98ebff':'#cdadff','center');lines.forEach((s,i)=>text(s,w/2,h-125+i*16,10,'#fff','center'));}
  return true;
 };
 const hud=TD.infantryHUD;TD.infantryHUD=function(ctx,text,G){return G.player.onfoot&&G.mission===3?TD.ground20HUD(ctx,text,G,false):hud(ctx,text,G);};
})(window);
