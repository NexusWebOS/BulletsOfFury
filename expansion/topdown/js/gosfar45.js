/* Dead Signal: authored crew, lift traffic, breach walls and difficulty-aware combat. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,W=TD.World,A=TD.Audio,FX=TD.FX,art=TD.AssaultArt,P=root.TD_GOSFAR45_ART;
 const mission=TD.MISSIONS.find(m=>m.id===3),D=TD.Depth35;
 const api=TD.Gosfar45=TD.Gosfar43={build:'overdrive1018-gosfar45-r2'};
 const DUR={hack:3.4,alarm:5.5,opening:1.5,entrance:2.6,taunt:4.5,plan:4.2,spotted:1.5,bar:1.6,rev:2,barrage:9.2,notice:2,rally:2,victory:2.4,exit:5.4,close:1.4,fade:1.2};
 const ORDER=['hack','alarm','opening','entrance','taunt','plan','spotted','bar','rev','barrage','notice','rally','combat'];
 const WORDS={hack:['HOTWIRE','Give me a second. I can bring the elevator down.'],alarm:['YURI','That alarm is getting louder. Hotwire, get away from it!'],opening:['HOTWIRE','Someone called it from upstairs. Get behind the wall!'],taunt:['GOSFAR','*sniff sniff* Do I smell some intruders?','Come out whenever you\'re ready to play.'],plan:['YURI / HOTWIRE','What the fuck are we gonna do?','Do you have any ideas?'],spotted:['GOSFAR','Ahh! There you are!'],bar:['YURI / HOTWIRE','FUUUUCK!!!'],barrage:['HOTWIRE / YURI','This is NOT what we expected!','Get down, Yuri! GET DOWN!'],notice:['YURI','His barrel! It\'s overheating!'],rally:['HOTWIRE','Take him down before he recovers!','I\'ll cover you. GO!'],victory:['HOTWIRE','He\'s down! Come on. Into the elevator!']};
 api.config=function(diff=TD.difficulty){return ({easy:{hp:1000,wind:1.25,burst:60,gap:.042,cool:3.2,speed:100,grenades:1,fuse:1.9,wave:2},normal:{hp:1200,wind:1.1,burst:76,gap:.036,cool:2.5,speed:115,grenades:2,fuse:1.65,wave:2},hard:{hp:1350,wind:.95,burst:88,gap:.03,cool:1.95,speed:135,grenades:2,fuse:1.5,wave:3},furious:{hp:1500,wind:.85,burst:104,gap:.026,cool:1.5,speed:155,grenades:3,fuse:1.4,wave:3},insanity:{hp:1700,wind:.8,burst:116,gap:.024,cool:1.35,speed:165,grenades:3,fuse:1.3,wave:4}})[diff]||api.config('normal');};
 const clip=api.clip=function(name,t=0,loop=true){const b=P.banks[name];return b?.frames[loop?Math.floor(Math.max(0,t)*b.fps)%b.frames.length:Math.min(b.frames.length-1,Math.floor(Math.max(0,t)*b.fps))];};
 function plate(ctx,name,t,x,y,o={}){const k=clip(name,t,o.loop!==false);if(k)art.draw(ctx,k,x,y,{s:1,...o});}
 const dir=a=>Math.abs(Math.sin(a))>Math.abs(Math.cos(a))?(Math.sin(a)<0?'east':'west'):(Math.cos(a)<0?'north':'south');
 function move(a,x,y,speed,dt){const dx=x-a.x,dy=y-a.y,d=Math.hypot(dx,dy),step=Math.min(d,speed*dt);a.moving=d>2;if(d>.01){a.x+=dx/d*step;a.y+=dy/d*step;}a.gaitPhase=((a.gaitPhase||0)+step/88)%1;if(d>2)a.a=a.aim=M.angTo(a.x,a.y,x,y);return d<3;}
 function route(a,points,speed,dt){a.route45??=0;if(a.route45>=points.length){a.moving=false;return true;}const p=points[a.route45];if(move(a,p[0],p[1],speed,dt))a.route45++;return a.route45>=points.length;}
 api.move=move;
 // Feet remain on the authored hexagonal floor, including its lower chamfers.
 api.floorBounds=function(y,r=10){const rows=[[180,137,660],[400,137,660],[414,139,660],[430,155,647],[440,168,631],[450,180,621],[462,200,600],[475,223,574],[495,257,549],[515,292,514]];let a=rows[0],b=rows.at(-1);for(let i=1;i<rows.length;i++)if(y<=rows[i][0]){a=rows[i-1];b=rows[i];break;}const t=M.clamp((y-a[0])/(b[0]-a[0]||1),0,1);return{left:M.lerp(a[1],b[1],t)+18+r,right:M.lerp(a[2],b[2],t)-18-r};};
 function floorClamp(a,r=10){a.y=M.clamp(a.y,175,505);const z=api.floorBounds(a.y,r);a.x=M.clamp(a.x,z.left,z.right);}
 const footTick45=TD.footTick;TD.footTick=function(p,G,dt){const v=footTick45(p,G,dt);if(G.boss?.gosfar45&&G.gosfar43?.phase==='combat')floorClamp(p,p.r);return v;};


 // The lower cover leaves actual paths inside the hexagon. Yuri's right return
 // is shorter; the tall side bulkheads remain visible until Gosfar breaches them.
 mission.data.structures=mission.data.structures.filter(s=>s.y>560||s.kind==='od_gate36');
 for(const x of [240,320,400,480,560])mission.data.structures.push({kind:'od_barrier',x,y:414,visual36:'cover45',dim36:{hw:40,hh:14,hp:x===240?Infinity:180,indestructible:x===240,cover:true},gosfarWall43:true,cover45:true,permanent43:x===240});
 mission.data.structures.push({kind:'od_barrier',x:604,y:384,visual36:'return45',dim36:{hw:20,hh:20,hp:150,cover:true},gosfarWall43:true,cover45:true,right45:true});
 for(const x of [130,670])mission.data.structures.push({kind:'od_outer36',x,y:305,visual36:'breach45',dim36:{hw:23,hh:48,hp:Infinity,indestructible:true,cover:false},side45:true});
 mission.data.brief=['DESTROY THREE RELAYS; MEET HOTWIRE AT THE FREIGHT LIFT.','PRONE UNDER HIGH CHAINGUN FIRE. ROLL OR RUN OUT OF GRENADE RETINAS.','THE LIFT BRINGS REINFORCEMENTS AFTER EACH 15% BOSS HEALTH LOST.','DEFEAT GOSFAR AND TAKE THE ELEVATOR TOGETHER.'];
 const coverPose=D.coverPose,coverDraw=D.drawCover;
 D.coverPose=function(s){if(!s.cover45&&!s.side45)return coverPose(s);const bank=P.banks[s.side45?'env/side':s.right45?'env/return':'env/cover'];const i=s.dead?bank.frames.length-1:s.hp/s.max<.55?1:0;return{key:bank.frames[i],s:s.side45?.75:s.right45?.65:1};};
 D.drawCover=function(ctx,s){if(!s.cover45&&!s.side45)return coverDraw(ctx,s);const z=D.coverPose(s);art.draw(ctx,z.key,s.x,s.y+s.type.hh,{s:z.s,flash:Math.min(.8,(s.flash||0)*6)});return true;};
 const setup=mission.setup;mission.setup=function(G,...args){setup(G,...args);G.gosfar43=null;};
 const respawn=mission.respawn;mission.respawn=function(G,old,fresh){respawn?.(G,old,fresh);if(G.gosfar43?.phase==='combat'){Object.assign(fresh,{x:440,y:465,prone:true,stance:'prone'});G.eshots=[];G.gosfar43.grenades=[];G.boss.state='recover';G.boss.actionT=0;}};
 function state(b,s){b.state=s;b.actionT=0;b.sent=0;b.firing=0;}
 function phase(G,s){const q=G.gosfar43,b=G.boss;q.phase=s;q.t=0;q.log.push({phase:s,at:G.time});b.actionT=0;
  if(s==='alarm'){q.lift={state:'arrive',t:0,queue:[],wave:0,delivered:[],exit:false};A.fadeMusic(0,.6);A.play('warn',.7);A.play('e29_powerDown',.65);}
  if(s==='opening')liftSet(q,'opening');
  if(s==='entrance'){b.hidden=false;state(b,'enter');liftSet(q,'hold');}
  if(s==='taunt'){state(b,'idle');q.power=true;q.alarm=0;liftSet(q,'closing');A.play('e29_generator',.6);}
  if(s==='bar'){q.barVisible=true;A.playMusic('gosfar43',.35);A.play('charge',.65);A.play('od75_debriefCount',.6);}
  if(s==='rev'){state(b,'windup');A.play('od75_minigunSpinUp',.9);}
  if(s==='barrage'){state(b,'shoot');q.nextShot=0;}
  if(s==='notice'){state(b,'overheat');q.heat=1;G.eshots=[];A.play('od75_minigunSpinDown',.85);A.play('od75_flameEnd',.5);}
  if(s==='combat'){q.controlReleased=true;state(b,'overheat');b.shield=false;Object.assign(G.player,{scripted:false,inv:60,cover:null,prone:true,stance:'prone',firing:0,moving:false,cover43:false});G.cp={x:440,y:465};G.shots=[];G.eshots=[];q.supplyCd=4;}
  if(s==='victory'){Object.assign(G.player,{scripted:true,inv:90});G.score+=30000;G.units=[];G.eshots=[];G.shots=[];G.grenades=[];G.footGrenades=[];G.burns=[];q.grenades=[];q.lift.queue=[];q.lift.exit=true;liftSet(q,'arrive');A.stopLoops();A.fadeMusic(.35,1.2);FX.boom(b.x,b.y-35,125,'gfx_destruction_',6);A.play('expBoss',.8);}
  if(s==='exit'){G.player.cover=null;G.player.route45=0;q.hot.route45=0;q.hot.action='walk';}
  if(s==='close')liftSet(q,'closing');
 }
 function liftSet(q,s){q.lift.state=s;q.lift.t=0;if(['opening','closing','arrive','depart'].includes(s))A.play('gd_doorOpen',s==='arrive'?.6:.45);}
 const WAVE=[['rifle','shotgun','rifle','double'],['double','rifle','shotgun','heavy'],['flame','heavy','rifle','shotgun'],['rocket','double','rifle','flame'],['laser','flame','heavy','double'],['flame','heavy','rocket','flyer']];
 function liftTick(G,dt){const q=G.gosfar43,l=q.lift;if(!l)return;l.t+=dt;
  if(l.state==='above'&&l.queue.length&&G.units.filter(u=>!u.dead).length<10){l.active=l.queue.shift();l.spawned=0;liftSet(q,'arrive');}
  else if(l.state==='arrive'&&l.t>1.25){liftSet(q,l.exit||q.phase==='combat'?'opening':'closed');A.play('blip',.6);}
  else if(l.state==='opening'&&l.t>1.1)liftSet(q,'hold');
  else if(l.state==='hold'&&q.phase==='combat'){
   const n=q.config.wave;if(l.active&&l.spawned<n&&l.t>.3+l.spawned*.42){const i=l.spawned++,role=WAVE[l.active.index][i];const u=TD.makeUnit('c35_'+role,370+i*28,210,{a:0});u.reinforcement39=true;u.liftExit45={t:0,to:255+i*12};u.sense39={home:{x:u.x,y:u.y,a:0},memory:8,scan:0,visible:false,known:{x:G.player.x,y:G.player.y}};G.units.push(u);q.arrivals++;A.play('gd_spotted',.35);}
   if(l.t>2.2){if(l.active)l.delivered.push(l.active.index);l.active=null;liftSet(q,'closing');}
  }else if(l.state==='closing'&&l.t>1.1)liftSet(q,l.exit?'closed':'depart');
  else if(l.state==='depart'&&l.t>1.25)liftSet(q,'above');
 }
 const unitTick=TD.unitTick;TD.unitTick=function(u,G,dt){if(u.liftExit45&&!u.dead){const z=u.liftExit45;z.t+=dt;u.moving35=true;u.a=0;u.gait=(u.gait||0)+dt;u.y=Math.min(z.to,u.y+105*dt);u.flash=Math.max(0,(u.flash||0)-dt);if(u.y>=z.to){u.liftExit45=null;u.moving35=false;}return;}const value=unitTick(u,G,dt);if(G.boss?.gosfar45&&!u.dead)floorClamp(u,u.r||18);return value;};
 function thresholds(G){const q=G.gosfar43,b=G.boss;while(q.threshold<6&&b.hp/b.max<=1-.15*(q.threshold+1)+1e-9){q.lift.queue.push({index:q.threshold,at:b.hp/b.max});q.waveLog.push({index:q.threshold,hp:b.hp,at:G.time});q.threshold++;A.play('warn',.5);}}
 function round(G,b,tx,ty,scripted=false,low=false){const s=TD.gosferSocket(b),a=M.angTo(s.x,b.y,tx,ty),f=M.fwd(a),speed=low?7.6:8.4;G.eshots.push({owner:b,k:'mg',contra35:true,attackKind35:'mg',x:s.x,y:b.y,a,vx:f[0]*speed,vy:f[1]*speed,dmg:scripted?0:1,life:110,r:3,t:0,drawLift:b.y-s.y,liftStart:b.y-s.y,liftEnd:low?11:45,spawnX:s.x,spawnY:b.y,flightDist:Math.max(1,Math.hypot(tx-s.x,ty-b.y)),hitsProne:low,scripted43:scripted,high45:!low});b.firing=.08;qStat(G,'shots');FX.attachedFlash(b,TD.gosferSocket,a,.055);A.play('od75_minigunShot',.8);}
 function qStat(G,k){G.gosfar43[k]=(G.gosfar43[k]||0)+1;}
 api.fire=round;
 function throwGrenades(G,b){const q=G.gosfar43,p=G.player,n=q.config.grenades,targets=[];for(let i=0;i<n;i++){const offset=[0,-94,94][i];let tx=M.clamp(p.x+(p.vx||0)*16+offset,180,620),ty=M.clamp(p.y+(p.vy||0)*16+(i?i===1?-15:18:0),200,495);const edge=api.floorBounds(ty,4);tx=M.clamp(tx,edge.left,edge.right);if(targets.some(t=>Math.hypot(tx-t.x,ty-t.y)<72)){const candidates=[p.x-188,p.x+188,(edge.left+edge.right)/2].map(x=>M.clamp(x,edge.left,edge.right));tx=candidates.sort((a,c)=>Math.min(...targets.map(t=>Math.hypot(c-t.x,ty-t.y)))-Math.min(...targets.map(t=>Math.hypot(a-t.x,ty-t.y))))[0];}targets.push({x:tx,y:ty});q.grenades.push({x:b.x,y:b.y-65,tx,ty,t:0,flight:.65,fuse:q.config.fuse,r:TD.difficulty==='easy'?40:48});}q.grenadeVolleys++;A.play('od75_mineThrow',.7);A.play('warn',.5);}
 function grenadeTick(G,dt){const q=G.gosfar43;for(const g of q.grenades){g.t+=dt;if(g.t>=g.fuse&&!g.done){g.done=true;q.explosions++;FX.boom(g.tx,g.ty,115,'of_grenade_blast_',6);A.play('expB',.75);TD.Cam.kick(4);const p=G.player;if(Math.hypot(p.x-g.tx,p.y-g.ty)<g.r+p.r*.5)TD.hurtPlayer(G,2,g.tx,g.ty,{hitsProne:true,grenade45:true});}}q.grenades=q.grenades.filter(g=>!g.done);}
 function breach(G){const q=G.gosfar43;q.breached=true;for(const s of q.side){s.hp=0;s.dead=true;s.flash=.16;W.remove(s.rect);FX.boom(s.x,s.y,145,'gfx_destruction_',6);FX.concrete(s.x,s.y,100);A.play('od75_wallBreach',.8);for(let i=0;i<2;i++){const u=TD.makeUnit('c35_flame',s.x+(s.x<400?32:-32),280+i*55,{a:s.x<400?-Math.PI/2:Math.PI/2});u.reinforcement39=true;G.units.push(u);}}W.navDirty=true;G.pickups.push({kind:'flamethrower',x:400,y:370,t:0});A.play('expB',.8);}
 function attack(G,b){const q=G.gosfar43,p=G.player;b.attack=['high','grenade','high','low','grenade','high'][b.pattern++%6];b.target={x:M.clamp(p.x+(p.vx||0)*12,150,650),y:M.clamp(p.y+(p.vy||0)*12,220,520)};state(b,b.attack==='grenade'?'grenadeWind':'windup');A.play(b.attack==='grenade'?'od75_mineThrow':'od75_minigunSpinUp',.75);q.attackLog.push({kind:b.attack,at:G.time});}
 TD.makeGosfer=function(G){const config=api.config(),b={gosfar43:true,gosfar45:true,name:'GOSFAR',x:400,y:205,r:29,hp:config.hp,max:config.hp,state:'idle',shield:true,hidden:true,dead:false,t:0,actionT:0,gait:0,flash:0,pattern:0,firing:0,angle:0};
  G.gosfar43={phase:'hack',t:0,age:0,config,lift:{state:'above',t:0,queue:[],wave:0,delivered:[],exit:false},wall:G.structures.filter(s=>s.cover45),side:G.structures.filter(s=>s.side45),hot:{x:344,y:220,action:'hack',weapon:'rifle',aim:Math.PI,t:0,actionT:0,fireCd:0,rounds:0,gaitPhase:0},grenades:[],supplies:[],allyShots:[],threshold:0,waveLog:[],arrivals:0,grenadeVolleys:0,explosions:0,attackLog:[],log:[{phase:'hack',at:G.time}],shots:0,hits:0,helpKills:0,throws:0,alarm:0,power:false,bar:0,barVisible:false};
  const q=G.gosfar43;b.sidePanels39=q.side;G.units=[];G.shots=[];G.eshots=[];G.msgs=[];G.fortress.pending=[];G.grenades=[];G.footGrenades=[];G.burns=[];G.player.cover=null;FX.list=[];TD.Stealth.reset();TD.Cam.x=80;TD.Cam.y=48;TD.Cam.zoom=1;
  b.alive=()=>!b.dead;b.hpFrac=()=>b.hp/b.max;b.aimPoint=()=>({x:b.x,y:b.y-62,r:29});b.aim=b.aimPoint;b.retinaTargets=()=>[{id:b,point:b.aimPoint,valid:()=>!b.dead&&q.phase==='combat'}];
  b.hit=(x,y,r,d,s)=>{if(b.dead||b.hidden)return false;const cx=s?s.x:x,cy=s?s.y-(TD.projectileLift?.(s)??s.drawLift??0):y;if(Math.hypot((cx-b.x)/48,(cy-(b.y-65))/68)>1+(r||0)/45)return false;if(q.phase!=='combat')return true;b.hp=Math.max(0,b.hp-d);b.flash=.14;q.hits++;thresholds(G);if(!b.hp){b.dead=true;b.deathT=0;state(b,'defeated');phase(G,'victory');}return true;};b.blast=(x,y,r,d)=>b.hit(x,y,r,d);
  b.tick=function(dt){b.t+=dt;b.actionT+=dt;b.flash=Math.max(0,b.flash-dt);b.firing=Math.max(0,b.firing-dt);if(q.phase!=='combat'||b.dead)return;const p=G.player;b.angle=M.angTo(b.x,b.y,p.x,p.y);thresholds(G);q.heat=b.state==='overheat'?1-M.clamp(b.actionT/config.cool,0,1):b.state==='shoot'?M.clamp(b.actionT/2,0,1):0;
   if(b.hp<=b.max*.5&&!q.breachStarted){q.breachStarted=true;state(b,'breach');A.play('od75_mineThrow',.7);G.say('GOSFAR / BREACH CHARGES! CLEAR THE WALLS!',p);}
   if(b.state==='breach'){if(b.actionT>1.5&&!q.breached)breach(G);if(b.actionT>1.9)state(b,'overheat');return;}
   if(['overheat','recover'].includes(b.state)&&b.actionT>(b.state==='recover'?.9:config.cool)){state(b,'move');b.targetX=[250,550,400][b.pattern%3];b.targetY=p.y<b.y+60?M.clamp(p.y+180,260,370):250+(b.pattern%2)*35;}
   else if(b.state==='move'){const dx=b.targetX-b.x,dy=b.targetY-b.y,d=Math.hypot(dx,dy),step=Math.min(d,config.speed*dt);b.x+=dx/(d||1)*step;b.y+=dy/(d||1)*step;W.collide(b,29,false);floorClamp(b,29);b.gait+=step/88;if(d<4||b.actionT>1.35)attack(G,b);}
   else if(b.state==='grenadeWind'){if(b.actionT>.65){throwGrenades(G,b);state(b,'grenadeThrow');}}
   else if(b.state==='grenadeThrow'&&b.actionT>.6){state(b,'move');b.targetX=b.x<400?550:250;b.targetY=270;}
   else if(b.state==='windup'){if(b.actionT<config.wind*.5)b.target={x:M.clamp(p.x+(p.vx||0)*12,150,650),y:M.clamp(p.y+(p.vy||0)*12,220,520)};if(b.actionT>config.wind)state(b,'shoot');}
   else if(b.state==='shoot'){const low=b.attack==='low',count=low?Math.ceil(config.burst*.38):config.burst,gap=low?config.gap*1.3:config.gap;while(b.sent<count&&b.actionT>=b.sent*gap){const s=TD.gosferSocket(b),base=M.angTo(s.x,b.y,b.target.x,b.target.y),a=base+(low?(b.sent%3-1)*.065:Math.sin(b.sent*.13)*.48),f=M.fwd(a),range=Math.hypot(b.target.x-s.x,b.target.y-b.y);round(G,b,s.x+f[0]*range,b.y+f[1]*range,false,low);b.sent++;}if(b.actionT>count*gap+.08){state(b,'overheat');A.play('od75_minigunSpinDown',.75);}}
  };
  b.drawUnder=ctx=>{if(q.phase==='combat'&&['windup','shoot'].includes(b.state)){const f=b.actionT/config.wind,col=b.state==='shoot'||f>.72?'red':f>.35?'yellow':'green',s=TD.gosferSocket(b),t=b.target||G.player;ART.draw(ctx,'bmfx_fov_'+col+'_tall',s.x,s.y,{ax:159.5,ay:11,a:M.angTo(s.x,s.y,t.x,t.y),sx:b.attack==='low'?.22:.75,sy:Math.min(380,Math.hypot(t.x-s.x,t.y-s.y))/267,alpha:.65});}};
  b.draw=ctx=>{if(b.hidden)return;const z=TD.gosferPose(b);art.draw(ctx,z.key,b.x,b.y,{s:1,flash:b.flash>0?.85:0,alpha:b.dead?Math.max(0,1-(b.deathT||0)/2.3):1});};b.drawOver=()=>{};return b;
 };
 mission.boss=TD.makeGosfer;
 const oldPose=TD.gosferPose,oldSocket=TD.gosferSocket;
 TD.gosferPose=function(b){if(!b.gosfar45)return oldPose(b);const q=TD.game.gosfar43,d=q.phase==='combat'?b.state==='move'?dir(M.angTo(b.x,b.y,b.targetX,b.targetY)):dir(b.target&&['windup','shoot','grenadeWind','grenadeThrow'].includes(b.state)?M.angTo(b.x,b.y,b.target.x,b.target.y):b.angle):'south';let a=b.dead?'death':['breach','grenadeWind','grenadeThrow'].includes(b.state)?'throw':b.state==='shoot'?'fire':b.state==='windup'?'rev':b.state==='overheat'?'overheat':b.state==='move'||q.phase==='entrance'?'walk':'ready';let bank='gosfar/'+a+'/'+d;if(!P.banks[bank])bank='gosfar/'+a+'/south';if(!P.banks[bank])bank='gosfar/ready/'+d;const t=b.dead?b.deathT||0:b.state==='move'?b.gait:b.state==='grenadeThrow'?.65+b.actionT:b.actionT;return{key:clip(bank,t,!b.dead&&!['grenadeWind','grenadeThrow'].includes(b.state)),dir:d,bank,phase:t,flip:false};};
 TD.gosferSocket=function(b){if(!b.gosfar45)return oldSocket(b);const z=TD.gosferPose(b),m=P.assets[z.key],u=m.muzzle||[m.anchor[0],m.anchor[1]-65];return{x:b.x+u[0]-m.anchor[0],y:b.y+u[1]-m.anchor[1]};};
 function breakCover(G,s){if(s.dead||s.permanent43)return;s.hp=0;s.dead=true;s.flash=.12;W.remove(s.rect);FX.concrete(s.x,s.y,100);A.play('od75_wallBreach',.75);TD.Cam.kick(3);}
 function scriptTick(G,dt){const q=G.gosfar43,b=G.boss,p=G.player;G.time+=dt;q.age+=dt;q.t+=dt;b.t+=dt;b.actionT+=dt;b.flash=Math.max(0,b.flash-dt);b.firing=Math.max(0,b.firing-dt);if(b.dead)b.deathT=(b.deathT||0)+dt;q.hot.t+=dt;q.hot.actionT+=dt;liftTick(G,dt);
  Object.assign(p,{scripted:true,inv:90,roll:0,jump:0,action:null,vx:0,vy:0,firing:0,moving:false,cover:null,cover43:false,stance:'stand',prone:false,fireAge39:99});p.footTime+=dt;p.poseT+=dt;G.shots=[];G.msgs=[];
  q.alarm=['alarm','opening','entrance'].includes(q.phase)?Math.min(.42,q.age*.12)*(.55+.45*Math.sin(q.age*9)**2):0;
  if(q.phase==='hack'){q.hot.action='hack';move(p,530,465,145,dt);if(Math.floor(q.t*5)!==Math.floor((q.t-dt)*5))A.play('blip',.22);}
  if(['alarm','opening'].includes(q.phase)){q.hot.action='walk';q.hot.weapon='rifle';if(route(q.hot,[[186,250],[186,435],[232,458]],175,dt)){q.hot.action='cover';q.hot.aim=0;}if(route(p,[[582,444]],170,dt)){p.cover43=true;p.stance='crouch';}if(Math.floor(q.t*1.2)!==Math.floor((q.t-dt)*1.2))A.play('gd_doorOpen',.3);}
  if(!['hack','alarm','opening','victory','exit','close','fade'].includes(q.phase)){q.hot.action='cover';q.hot.x=232;q.hot.y=458;q.hot.aim=0;p.x=582;p.y=444;p.stance='crouch';p.cover43=true;p.aim=0;}
  if(q.phase==='entrance'){b.y=M.lerp(205,285,M.clamp(q.t/2.5,0,1));b.gait=q.t*.9;}
  if(q.phase==='bar')q.bar=M.clamp(q.t/DUR.bar,0,1);
  if(q.phase==='barrage'){
   q.heat=M.clamp(q.t/DUR.barrage,0,1);while(q.nextShot<=q.t){const n=Math.round(q.nextShot/.018);round(G,b,175+n*31%445,430,true);q.nextShot+=.018;}
   // First chew the short right return, then right-to-left across the lower wall.
   const order=[q.wall.find(s=>s.right45),...q.wall.filter(s=>!s.right45&&!s.permanent43).sort((a,c)=>c.x-a.x)];
   for(let i=0;i<order.length;i++){const s=order[i],age=q.t-i*1.5;if(age>0&&!s.dead){s.hp=Math.max(0,(s.max||180)-age*110);s.flash=.06;if(Math.floor(age*12)!==Math.floor((age-dt)*12))FX.concrete(s.x+Math.sin(age*33)*25,s.y-23,22);if(!s.hp)breakCover(G,s);}}
   if(q.t>1.15){p.cover43=false;p.prone=true;p.stance='prone';p.aim=Math.PI;p.drop45=q.t-1.15;}
   TD.shotTick(G);
  }
  if(['notice','rally'].includes(q.phase)){p.cover43=false;p.prone=true;p.stance='prone';p.aim=Math.PI;}
  if(q.phase==='victory'){q.hot.action='cover';p.prone=true;p.stance='prone';}
  if(q.phase==='exit'){p.prone=false;p.stance='stand';q.hot.action='walk';q.hot.weapon='eagle';route(p,[[582,300],[420,200]],165,dt);if(route(q.hot,[[188,428],[180,385],[380,200]],165,dt))q.hot.action='ready';}
  FX.update(dt);for(const s of [...q.wall,...q.side])s.flash=Math.max(0,s.flash-dt);TD.Cam.zoom=1;TD.Cam.follow(400,288,.18);TD.Cam.shake*=.85;
  if(q.t>=DUR[q.phase]){if(q.phase==='fade')return'clear';if(q.phase==='victory')phase(G,'exit');else if(q.phase==='exit')phase(G,'close');else if(q.phase==='close')phase(G,'fade');else phase(G,ORDER[ORDER.indexOf(q.phase)+1]);}
 }
 mission.exclusiveWhen=G=>!!G.gosfar43&&G.gosfar43.phase!=='combat';mission.exclusiveStep=scriptTick;
 const pre=mission.pre;mission.pre=function(G,dt){if(!G.boss?.gosfar45)return pre?.(G,dt);G.player.scripted=false;G.player.cover43=false;G.player.y=M.clamp(G.player.y,180,510);G.player.x=M.clamp(G.player.x,100,700);};
 const cam=mission.cam;mission.cam=function(G){if(G.gosfar43){TD.Cam.zoom=1;TD.Cam.follow(400,288,.1);}else cam?.(G);};
 const tick=mission.tick;mission.tick=function(G,dt){if(!G.boss?.gosfar45)return tick?.(G,dt);const q=G.gosfar43;if(q.phase!=='combat')return;q.t+=dt;q.age+=dt;q.hot.t+=dt;q.hot.actionT+=dt;liftTick(G,dt);grenadeTick(G,dt);support(G,dt);};

 function support(G,dt){const q=G.gosfar43,h=q.hot;h.fireCd-=dt;h.reload=Math.max(0,(h.reload||0)-dt);
  const enemies=G.units.filter(u=>!u.dead&&!u.liftExit45).sort((a,b)=>Math.hypot(a.x-h.x,a.y-h.y)-Math.hypot(b.x-h.x,b.y-h.y));
  if(!h.peek45&&enemies.length&&h.reload<=0&&h.action!=='throw'){const target=enemies[0];h.peek45={state:'out',side:target.x<240?-1:1,target,t:0,burst:0};h.route45=0;h.weapon=target.kind35==='flame'?'eagle':'rifle';}
  const z=h.peek45;
  if(h.action==='throw'){if(h.actionT>.65){h.action='cover';h.actionT=0;}}
  else if(h.reload>0){h.action='reload';}
  else if(z){
   const end=z.side<0?184:298;z.t+=dt;
   if(z.state==='out'){h.action='walk';if(route(h,z.side<0?[[198,444],[184,430],[184,390]]:[[end,450],[end,390]],155,dt)){z.state='aim';z.t=0;h.actionT=0;}}
   if(z.state==='aim'){
    const target=z.target;if(!target.dead){h.aim=M.angTo(h.x,h.y,target.x,target.y);h.action='fire';h.moving=false;
     if(z.t>.24&&h.fireCd<=0&&z.burst<(h.weapon==='eagle'?1:3)){h.fireCd=h.weapon==='eagle'?.8:.09;z.burst++;h.rounds++;const socket=TD.Hotwire45?.socket(h)||{x:h.x,y:h.y-45},a=M.angTo(socket.x,socket.y,target.x,target.y-28),f=M.fwd(a);q.allyShots.push({x:socket.x,y:socket.y,a,vx:f[0]*650,vy:f[1]*650,t:0,damage:h.weapon==='eagle'?4:1.5});A.play(h.weapon==='eagle'?'od75_sniper':'gd_soldierRifle',.55);}
    }
    if(z.t>.72||target.dead){z.state='back';h.route45=0;h.actionT=0;}
   }
   if(z.state==='back'){h.action='walk';if(route(h,z.side<0?[[184,430],[198,444],[232,458]]:[[end,450],[232,458]],155,dt)){h.peek45=null;h.action='cover';h.aim=0;h.actionT=0;if(h.rounds>=(h.weapon==='eagle'?7:30)){h.reload=1.1;h.rounds=0;h.action='reload';A.play('loadoutEquip',.5);}}}
  }else{move(h,232,458,155,dt);h.action=h.moving?'walk':'cover';if(!h.moving)h.aim=0;}
  for(const s of q.allyShots){s.t+=dt;s.x+=s.vx*dt;s.y+=s.vy*dt;for(const u of G.units)if(!u.dead&&Math.hypot((s.x-u.x)/19,(s.y-(u.y-28))/31)<1){TD.hitUnit(G,u,s.damage,s.x,s.y);if(u.dead)q.helpKills++;s.done=true;FX.concrete(s.x,s.y,12);break;}}q.allyShots=q.allyShots.filter(s=>!s.done&&s.t<1.25);
  q.supplyCd-=dt;if(q.supplyCd<=0&&!h.peek45&&h.reload<=0){q.supplyCd=12;h.action='throw';h.actionT=0;const kind=['flamethrower','cryo_lance','minigun','spread_shotgun'][q.throws++%4];q.supplies.push({kind,x:h.x,y:h.y,tx:M.clamp(G.player.x,290,580),ty:M.clamp(G.player.y,350,465),t:-.28});A.play('od75_mineThrow',.4);G.say('HOTWIRE: CATCH!',G.player);}
  for(const s of q.supplies){s.t+=dt;if(s.t>=.85&&!s.done){s.done=true;G.pickups.push({kind:s.kind,x:s.tx,y:s.ty,t:0});A.play('od75_ammoPickup',.5);}}q.supplies=q.supplies.filter(s=>!s.done);
 }

 function liftPose(q){const l=q?.lift;if(!l)return clip('lift/shaft');const t=l.t;if(l.state==='above')return clip('lift/shaft');if(l.state==='depart')return clip('lift/depart',t/1.25*P.banks['lift/depart'].duration,false);if(l.state==='arrive'){const b=P.banks['lift/depart'];return b.frames[Math.max(0,b.frames.length-1-Math.floor(t/1.25*b.frames.length))];}if(l.state==='opening')return clip('lift/open',t/1.1*P.banks['lift/open'].duration,false);if(l.state==='closing'){const b=P.banks['lift/open'];return b.frames[Math.max(0,b.frames.length-1-Math.floor(t/1.1*b.frames.length))];}if(l.state==='hold')return P.banks['lift/open'].frames.at(-1);return clip('lift/open');}
 api.liftPose=liftPose;
 const floor=mission.drawFloor;mission.drawFloor=function(ctx,G){const old=G.fortress.doorOpen;G.fortress.doorOpen=false;floor(ctx,G);G.fortress.doorOpen=old;const q=G.gosfar43;art.draw(ctx,liftPose(q),400,220,{s:.85});if(!q)return;
  for(const g of q.grenades){const z=ART.get('retmb_0');if(z)ART.draw(ctx,'retmb_'+Math.floor(q.age*9)%4,g.tx,g.ty,{sx:g.r*2/z.sw,sy:g.r*1.25/z.sh,palette:g.t/g.fuse>.6?'#ff3434':'#ffc34a',alpha:.9});}
 };
 function liftFront(ctx,q){if(!['close','fade'].includes(q.phase)&&!(q.phase==='exit'&&q.t>3.8))return;const key=liftPose(q),b=P.banks['lift/open'],i=b.frames.indexOf(key),progress=i<0?0:i/(b.frames.length-1),gap=progress*45.05;for(const [x,w]of [[318.4,81.6-gap],[400+gap,81.6-gap]]){ctx.save();ctx.beginPath();ctx.rect(x,63.6,w,163.2);ctx.clip();art.draw(ctx,key,400,220,{s:.85});ctx.restore();}}
 const actors=D.drawActors;D.drawActors=function(ctx,G){actors(ctx,G);if(G.mission!==3||!G.gosfar43)return;const q=G.gosfar43,h=q.hot;if(TD.Hotwire45)TD.Hotwire45.draw(ctx,h);else plate(ctx,'hotwire/ready',0,h.x,h.y);
  for(const g of q.grenades){const t=M.clamp(g.t/g.flight,0,1);art.draw(ctx,'of_grenade',M.lerp(g.x,g.tx,t),M.lerp(g.y,g.ty,t)-Math.sin(Math.PI*t)*75,{s:.22,a:g.t*8});}
  if(G.boss.state==='breach'&&!q.breached)for(const s of q.side){const t=M.clamp((G.boss.actionT-.2)/.5,0,1);art.draw(ctx,t>=1?'od39_claymore_armed':'od39_claymore',M.lerp(G.boss.x,s.x,t),M.lerp(G.boss.y-65,s.y,t)-Math.sin(Math.PI*t)*70,{s:.18});}
  for(const s of q.allyShots)TD.drawShot(ctx,{...s,k:'mg',contra35:true,attackKind35:'mg',t:s.t*60,r:3},false);
  for(const s of q.supplies){if(s.t<0)continue;const t=M.clamp(s.t/.85,0,1);TD.drawFootPickup(ctx,{kind:s.kind,x:M.lerp(s.x,s.tx,t),y:M.lerp(s.y,s.ty,t)-Math.sin(t*Math.PI)*75,t:s.t});}liftFront(ctx,q);
 };
 const foot=TD.footPose;TD.footPose=function(p){const q=TD.game?.gosfar43;if(!q||TD.game.mission!==3)return foot(p);
  // Select authored locomotion explicitly during the shared elevator exit.
  if(p.scripted&&p.moving){const di=TD.Combat39.direction(p.aim),b=TD_COMBAT39_ART.banks['yuri_topdown/walk/'+di];if(p.pilot==='yuri'&&b)return{key:b.frames[Math.floor((p.gaitPhase||0)*b.frames.length)%b.frames.length],scale:1,angle:0,dir:di,action:'walk',bank:'cinematic-locomotion45'};}
  if(p.scripted&&p.cover43&&p.pilot==='yuri')return{key:clip('yuri/cover/east',q.age),scale:1,angle:0,dir:'east',action:'wall-brace'};
  if(p.scripted&&p.prone&&p.pilot==='yuri'){const b=P.banks['yuri/drop/north'];if(b)return{key:clip('yuri/drop/north',Math.min(p.drop45||1,1),false),scale:1,angle:0,dir:'north',action:'prone-enter'};}
  return foot(p);
 };
 const over=mission.drawOver;mission.drawOver=function(ctx,G){const q=G.gosfar43;if(!q)return over?.(ctx,G);if(q.alarm>0){ctx.fillStyle='rgba(235,8,18,'+q.alarm+')';ctx.fillRect(TD.Cam.x,TD.Cam.y,TD.VW,TD.VH);}if(q.phase==='fade'){ctx.fillStyle='rgba(0,0,0,'+M.clamp(q.t/DUR.fade,0,1)+')';ctx.fillRect(TD.Cam.x,TD.Cam.y,TD.VW,TD.VH);}};
 const hud=mission.hud;mission.hud=function(ctx,text,G){const q=G.gosfar43;if(!q)return hud?.(ctx,text,G);TD.CornerHUD26.draw(ctx,text,G,false);const b=G.boss;if(q.barVisible&&!b.dead){art.draw(ctx,'pb20_hud_boss',320,62,{s:.76});ctx.fillStyle='#e64e32';ctx.fillRect(227,59,186*(q.phase==='bar'?q.bar:b.hp/b.max),7);text('GOSFAR / '+(TD.difficulty||'normal').toUpperCase(),320,50,10,'#ffcf8a','center');}
  const words=WORDS[q.phase];if(words){art.draw(ctx,'pb20_hud_dialogue',320,451,{s:.60});text(words[0],320,435,10,words[0]==='GOSFAR'?'#c4a3ed':'#88e8ed','center');for(let i=1;i<words.length;i++)text(words[i],320,451+(i-1)*15,9,'#fff','center');}
  else if(q.phase==='combat'){const cue=['grenadeWind','grenadeThrow'].includes(b.state)||q.grenades.length?'GRENADE RETINAS / MOVE OR ROLL':b.state==='overheat'?'BARRELS HOT / ATTACK!':b.attack==='low'&&['windup','shoot'].includes(b.state)?'LOW BURST / DODGE OR ROLL':'HIGH CHAINGUN / GET PRONE';text(cue,320,461,10,'#ffe281','center');if(q.lift.state!=='above'&&q.lift.active)text('LIFT REINFORCEMENTS / WAVE '+(q.lift.active.index+1),320,102,9,'#ffac72','center');}
  if(q.alarm>0)text('SECURITY ALERT / FREIGHT LIFT DESCENDING',320,110,10,'#ff7871','center');return true;
 };
 const audioActor=A.actor;A.actor=function(p,gain,player){audioActor.call(this,p,gain,player);const q=TD.game?.mission===3&&TD.game.gosfar43;if(!q||!player)return;if(q.alarm>0)this.loop('gd_alarmLoop','gosfar45-alarm',.75);if(q.phase==='bar')this.loop('od75_turretServo','gosfar45-bar',.7,1.1);if(['arrive','depart'].includes(q.lift.state))this.loop('od75_turretServo','gosfar45-lift',.35,.65);};
 ART.warm([...Object.keys(P.assets),'retmb_0','retmb_1','retmb_2','retmb_3','of_grenade']);
})(window);
