/* Camera-specific authored plates, perception and objective rules for Overdrive. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,W=TD.World,I=TD.Input,A=TD.AssaultArt,P=root.TD_COMBAT39_ART,D=TD.Depth35;
 const C=TD.Combat39={build:P.build,stats:{sightings:0,searches:0,shots:0,breaches:0},log:[]};
 const bank=(m,a,d)=>P.banks[m+'/'+a+'/'+d];
 const frame=(q,t=0,loop=q?.loop)=>q?.frames[loop?Math.floor(Math.max(0,t)*q.fps)%q.frames.length:Math.min(q.frames.length-1,Math.floor(Math.max(0,t)*q.fps))];
 const ready=q=>q&&q.frames.every(k=>ART.get(k));
 const cardinal=a=>Math.abs(Math.sin(a))>Math.abs(Math.cos(a))?(Math.sin(a)<0?'east':'west'):(Math.cos(a)<0?'north':'south');
 const direction=a=>['south','south-west','west','north-west','north','north-east','east','south-east'][(Math.round(a/(Math.PI/4))%8+8)%8];
 C.bank=bank;C.frame=frame;C.direction=direction;
 C.sprite=function(ctx,k,x,y,s=1,o={}){A.draw(ctx,k,x,y,{s,...o});};
 function choose(m,a,di){return bank(m,a,di)||bank(m,a,cardinal(({'south':0,'south-west':1,'west':2,'north-west':3,'north':4,'north-east':5,'east':6,'south-east':7}[di]||0)*Math.PI/4));}
 C.fireDuration=p=>choose('yuri_topdown',p.prone?'prone_fire':p.moving?'run_fire':'fire',direction(p.aim))?.duration||.75;
 const footPose=TD.footPose;
 TD.footPose=function(p){
  if(p.pilot!=='yuri'||p.pseudo3D||p.sideScroll)return footPose(p);
  if(p.cover&&!p.prone&&!p.roll&&!p.jump&&!p.action&&TD.Yuri36?.coverSpec(p))return footPose(p);
  const di=direction(p.roll>0?p.rollAim:p.action?.aim??p.aim),m='yuri_topdown';let a='idle',t=p.poseT||0,loop=false;
  const firing=p.firing>0||(p.fireAge39??99)<C.fireDuration(p);
  if(p.dead){a='death';t=p.deadT||0;}
  else if(p.roll>0){a=p.rollFromProne39?'prone_roll':p.rollProne?'roll_to_prone':'roll';t=(.5-p.roll)/.5;}
  else if(p.jump>0||p.vault29){a='jump';t=p.vault29?.t??(.65-p.jump)/.65;}
  else if(p.action){a='grenade';t=p.action.t;}
  else if(p.stanceTransition?.t<.46){a=p.stanceTransition.to==='prone'?'prone_enter':'prone_exit';t=p.stanceTransition.t/.46;}
  else if(p.prone){a=firing?'prone_fire':p.moving?'crawl':'prone_idle';t=firing?p.fireAge39||0:p.moving?p.gaitPhase||0:p.poseT||0;loop=!firing;}
  else if(p.cover){a=firing&&p.peekExposed?'fire':'crouch_enter';t=a==='fire'?p.fireAge39||0:1-M.clamp((p.peek||0)/.24,0,1);loop=false;}
  else if(p.stance==='crouch'){a=p.moving?'crouch_walk':'crouch_enter';t=p.moving?p.gaitPhase||0:1;loop=p.moving;}
  else if(firing){a=p.moving?'run_fire':'fire';t=p.fireAge39||0;}
  else if(p.moving){a='walk';t=p.gaitPhase||0;loop=true;}
  let q=choose(m,a,di);
  if(a==='prone_roll'&&!q)q=choose(m,'roll_to_prone',di);
  if(!q)q=choose(m,p.prone?'prone_idle':'idle',di);
  if(!ready(q))return footPose(p);
  if(p.roll>0||p.jump>0||p.vault29||p.stanceTransition?.t<.46||a==='crouch_enter'||a.endsWith('peek'))t*=q.duration;
  else if(p.moving&&!firing)t*=q.duration;
  // Quiet prone holds come from the completed lowering clip, whose palette and root match.
  if(a==='prone_idle'){const hold=choose(m,'prone_enter',di);if(ready(hold)){q=hold;t=q.duration;loop=false;}}
  return{key:frame(q,t,loop||(['fire','run_fire','prone_fire'].includes(a)&&p.firing>0)),scale:1,angle:0,action:a,dir:di,bank:'combat39',phase:t};
 };
 const footTick=TD.footTick;
 TD.footTick=function(p,G,dt){p.fireAge39=(p.fireAge39??99)+dt;return footTick(p,G,dt);};
 // Ground enemies never ask the front/pseudo-3D bank for an attack or reload.
 const groundPose=D.groundPose;
 D.groundPose=function(u){
  if(!u.kind35)return groundPose(u);
  const di=u.attack35?.phase!=='wait'&&u.fireDir39||cardinal(u.a),m=D.role(u)+'_topdown';
  if(u.rollState35)return groundPose(u);
  let a=u.moving35&&!['wind','burst'].includes(u.attack35?.phase)?'walk':u.action35==='fire_forward'?'fire':/^reload/.test(u.action35||'')?'reload':u.action35==='draw_forward'?'draw_forward':'idle';
  let q=bank(m,a,di)||(a==='walk'?bank(m,'walk',di==='east'?'south-east':'south-west'):null)||bank(m,'idle',di);if(!q)return groundPose({...u,action35:'idle',firing:0});
  const t=a==='walk'?(u.walk??u.age??0)*1.4:u.actionT35??u.age??0;
  return{key:frame(q,t,a==='idle'||a==='walk'||a==='fire'&&['minigunner','flamethrower'].includes(D.role(u))),s:D.role(u)==='bat_drone'?1.15:D.role(u)==='minigunner'?1.9:1.75,view:'topdown',dir:di};
 };
 C.canSee=(u,G)=>!!u.sense39?.visible;
 C.target=(u,G)=>u.sense39?.known?{...u.sense39.known,dead:G.player.dead}:G.player;
 C.sense=function(u,G,dt){
  const p=G.player,s=u.sense39||(u.sense39={home:{x:u.x,y:u.y,a:u.a},memory:0,scan:0,known:null,visible:false});
  s.scan+=dt;s.memory=Math.max(0,s.memory-dt);u.freeze39=Math.max(0,(u.freeze39||0)-dt);
  const range=Math.hypot(p.x-u.x,p.y-u.y),angle=M.angTo(u.x,u.y,p.x,p.y),delta=Math.abs(M.wrap(angle-u.a));
  const sight=range<(p.prone?300:p.cover&&!p.peekExposed?210:480)&&delta<(s.memory>0?1.55:1.18)&&!W.rayBlock(u.x,u.y,p.x,p.y)&&!p.dead;
  s.visible=sight;
  if(sight){if(!s.memory){C.stats.sightings++;s.acquired=G.time;}s.known={x:p.x,y:p.y};s.memory=6;u.aware=1;}
  else if(p.firing>0&&range<280&&!p.dead){s.known={x:p.x,y:p.y};s.memory=Math.max(s.memory,3);}
  if(sight&&s.shareAt!==Math.floor(G.time)){s.shareAt=Math.floor(G.time);for(const ally of G.units)if(ally!==u&&ally.kind35&&!ally.dead&&Math.hypot(ally.x-u.x,ally.y-u.y)<160&&!W.rayBlock(u.x,u.y,ally.x,ally.y)){const q=ally.sense39||(ally.sense39={home:{x:ally.x,y:ally.y,a:ally.a},scan:0});q.known={...s.known};q.memory=Math.max(q.memory||0,3);}}
  return s;
 };
 const tickUnit=TD.unitTick;
 TD.unitTick=function(u,G,dt){
  if(!u.kind35||u.dead)return tickUnit(u,G,dt);const s=C.sense(u,G,dt);
  if(!s.memory){u.age=(u.age||0)+dt;u.flash=Math.max(0,(u.flash||0)-dt);u.aware=0;u.sees=false;u.moving35=false;u.action35='idle';u.firing=0;u.attack35={phase:'wait',t:.45};u.a=M.turnTo(u.a,s.home.a+Math.sin(s.scan*.55)*.65,dt*.7);return;}
  if(!s.visible&&s.known&&Math.hypot(u.x-s.known.x,u.y-s.known.y)<65&&!['wind','burst','recover'].includes(u.attack35?.phase)&&!u.tactic36?.cover){u.a=M.wrap(u.a+dt*1.1);u.look=u.a;u.action35='idle';u.firing=0;u.moving35=false;u.age=(u.age||0)+dt;C.stats.searches++;return;}
  return tickUnit(u,G,dt*(u.freeze39>0?.65:1));
 };
 const attack=D.attack;
 D.attack=function(u,dt,allow,emit){
  if(!u.kind35)return attack(u,dt,allow,emit);
  const role=D.role(u),di=u.attack35?.phase!=='wait'&&u.fireDir39||cardinal(u.a),q=bank(role+'_topdown','fire',di),d=D.profiles[u.kind35];
  if(!u.groundNative39&&u.attack35?.phase&&u.attack35.phase!=='wait')return attack(u,dt,allow&&C.canSee(u,TD.game),emit);
  if(!ready(q))return attack(u,dt,allow&&C.canSee(u,TD.game),(kind,off,speed,n)=>{if(u.dead||!C.canSee(u,TD.game))return;emit(kind,off,speed,n);C.stats.shots++;});
  u.groundNative39=true;const a=u.attack35||(u.attack35={phase:'wait',t:.6});u.actionT35=(u.actionT35||0)+dt;u.fireAge34=(u.fireAge34||0)+dt;u.firing=Math.max(0,(u.firing||0)-dt);u.warn=0;
  const set=name=>{u.action35=name;u.actionT35=0;};
  if(u.dead){u.firing=0;a.phase='wait';return;}
  if(a.phase==='wait'){a.t-=dt;if(a.t<=0&&allow&&C.canSee(u,TD.game)&&TD.game.units.filter(v=>v!==u&&!v.dead&&['wind','burst'].includes(v.attack35?.phase)).length<2){a.phase='wind';a.windDuration=Math.max(d.wind,bank(role+'_topdown','draw_forward',di)?.duration||0);a.t=a.windDuration;set('draw_forward');u.target35={x:TD.game.player.x,y:TD.game.player.y};u.fireDir39=di;}}
  else if(a.phase==='wind'){if(a.t>a.windDuration*.45&&C.canSee(u,TD.game)){u.target35={...u.sense39.known};u.fireDir39=cardinal(u.a);}u.warn=Math.max(0,a.t);a.t-=dt;if((!allow||!C.canSee(u,TD.game))&&a.t>a.windDuration*.45){a.phase='wait';a.t=.4;set('idle');return;}if(a.t<=0){a.phase='burst';a.sent=0;a.events39=q.events?.shot_frames?.map(n=>n/q.fps)||Array.from({length:d.count},(_,i)=>(d.count===1?2:d.count===2?2+i*3:d.count>=7?1+i:2+i*2)/q.fps);a.length39=Math.max(q.duration,(a.events39.at(-1)||0)+1/q.fps);set('fire_forward');u.fireT=u.fireAge34=0;}}
  else if(a.phase==='burst'){
   while(a.sent<a.events39.length&&u.actionT35+1e-9>=a.events39[a.sent]){for(const off of d.fan)emit(d.shot,off,d.speed,a.sent);TD.Audio.play(d.cue,.5);a.sent++;C.stats.shots++;D.attacks[u.kind35]=(D.attacks[u.kind35]||0)+1;}
   u.firing=Math.max(0,a.length39-u.actionT35);if(u.actionT35>=a.length39){a.phase='recover';a.t=Math.max(d.cd,bank(role+'_topdown','reload',di)?.duration||0);u.recoverDuration35=a.t;set(d.reload||'idle');}
  }else if(a.phase==='recover'){a.t-=dt;u.firing=0;if(a.t<=0){a.phase='wait';a.t=.65;set('idle');}}
 };
 const cones=['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall');ART.warm(cones);
 C.warning=function(ctx,u,G){
  if(u.dead||!u.kind35||Math.hypot(u.x-G.player.x,u.y-G.player.y)>520)return;
  const phase=u.attack35?.phase;if(!['wind','burst'].includes(phase)||!u.sense39?.visible)return;const progress=phase==='wind'?1-(u.attack35.t/(u.attack35.windDuration||D.profiles[u.kind35]?.wind||1)):0,col=phase==='burst'||phase==='recover'&&u.firing>0?'red':phase==='wind'?(progress>.67?'red':progress>.33?'yellow':'green'):'green';
  const socket=D.groundSocket(u),target=u.target35,angle=['wind','burst'].includes(phase)&&target?M.angTo(socket.x,socket.y,target.x,target.y-TD.footLift(G.player)):u.a;
  const length=u.kind35==='flame'?90:u.kind35==='shotgun'?80:100;
  ART.draw(ctx,'bmfx_fov_'+col+'_tall',socket.x,socket.y,{ax:159.5,ay:11,a:angle,sx:(u.kind35==='shotgun'?48:24)/126,sy:length/267,alpha:col==='green'?.5:.85});
 };
 const drawActors=D.drawActors;D.drawActors=function(ctx,G){for(const u of G.units)C.warning(ctx,u,G);drawActors(ctx,G);};
 TD.FOOT_GUNS.flamethrower={name:'FLAMETHROWER',cap:120,reserve:0,cd:4,damage:1.4,k:'flame39',speed:5.3,life:38,radius:8,fan:[-.055,.055],cue:'firewallLaunch'};
 TD.FOOT_GUNS.cryo_lance={name:'CRYO LANCE',cap:36,reserve:0,cd:15,damage:4,k:'cryo39',speed:11,life:45,radius:5,pierce:1,cue:'enemyHeavyLaser'};
 TD.Bastion.GUNS.flamethrower={name:'FLAMETHROWER',cd:.07,damage:1.25,ammo:120,range:210};
 TD.Bastion.GUNS.cryo_lance={name:'CRYO LANCE',cd:.24,damage:4,ammo:36};
 const shot=TD.drawShot;
 const baseShot=TD.Lighting22.playerShot;
 TD.Lighting22.playerShot=function(ctx,s,fade=1){if(s.gun==='cryo_lance'){A.draw(ctx,'od39_cryo_bolt',s.x,s.y,{s:.17,a:Math.atan2(s.ty-s.sy,s.tx-s.sx),alpha:fade});return;}if(s.gun==='flamethrower'){const q=root.TD_PIXELLAB38_ART.banks['fx/flamethrower_toward_viewer'];A.draw(ctx,TD.PixelLab38.frame(q,s.t,true),s.x,s.y,{s:.24,alpha:fade});return;}baseShot(ctx,s,fade);};
 TD.drawShot=function(ctx,s,enemy){
  if(s.weapon39==='flamethrower'||s.k==='flame39'){D.drawShot(ctx,{...s,attackKind35:'flame'},TD.projectileLift(s));return;}
  if(s.weapon39==='cryo_lance'||s.k==='cryo39'){A.draw(ctx,'od39_cryo_bolt',s.x,s.y-TD.projectileLift(s),{s:.16,a:s.a+Math.PI/2});return;}
  return shot(ctx,s,enemy);
 };
 const pickup=TD.drawFootPickup;TD.drawFootPickup=function(ctx,k){if(['flamethrower','cryo_lance'].includes(k.kind)){A.draw(ctx,k.kind==='flamethrower'?'od39_flame_pickup':'od39_cryo_pickup',k.x,k.y,{s:.18});return;}pickup(ctx,k);};
 const mission=TD.MISSIONS.find(m=>m.id===3),setup=mission.setup;
 mission.setup=function(G){setup(G);G.pickups.push({kind:'flamethrower',x:210,y:2220,t:0},{kind:'cryo_lance',x:580,y:1680,t:0});};
 mission.help=['WASD / D-PAD: MOVE','MOUSE OR Q / E: AIM; J / LEFT MOUSE: FIRE','F: TOGGLE PRONE / WASD: CRAWL','SPACE / V / H: ROLL; F + ROLL: FINISH PRONE','ROLL WHILE PRONE: BODY ROLL, REMAIN PRONE','K / X: JUMP; U: GRENADE; C / SHIFT: COVER','I + FIRE IN COVER: BLINDFIRE','SHORT AIM CUE: PREPARING TO FIRE / MOVE OR BREAK SIGHT','DESTROY COVER TO BREAK ENEMY FIRING POSITIONS','FIND FLAMETHROWER AND CRYO LANCE SUPPLIES','ENTER: PAUSE / B: BACK'];
 TD.footBriefKeys=()=>[['dpad','MOVE'],['a','FIRE'],['x','ROLL'],['y','GRENADE'],['c','COVER'],['start','PAUSE']];
 const bossPose=TD.gosferPose;
 TD.gosferPose=function(b){
  const di=b.state==='roll'?(b.travel>0?'east':'west'):cardinal(b.angle??0),moving=['enter','move','strafe','dash'].includes(b.state),a=b.dead?'death':b.claymore39?.phase==='throw'?'throw_claymore':b.state==='transform'?'transform':b.state==='roll'?'roll':b.state==='jump'?'jump':b.state==='shoot'?'fire':b.state==='windup'?'draw_forward':moving?'walk':'idle';
  const q=bank('gosfer_topdown',a,di)||(['death','throw_claymore','jump'].includes(a)?bank('gosfer_topdown',a,'south'):null)||bank('gosfer_topdown','idle',di);if(!q)return bossPose(b);
  const shotLength=(b.attack==='retina'?20*.055:b.attack==='breaker'?26*.075:b.phase===2?24*.045:12*.075)+.13;
  const t=a==='roll'?(b.actionT||0)/.56*q.duration:a==='jump'?(b.actionT||0)/.9*q.duration:a==='fire'?(b.actionT||0)/shotLength*q.duration:moving?(b.gait||0)*q.duration:b.state==='transform'?(b.transformT||0)/3.2*q.duration:b.claymore39?.phase==='throw'?b.claymore39.t:b.actionT||b.t||0;
  return{key:frame(q,t,moving||a==='idle'),flip:false,scale:1,bank:'combat39',phase:t};
 };
 TD.gosferSocket=function(b){const z=TD.gosferPose(b),m=root.TD_ASSAULT_ART.assets[z.key],q=m.muzzle||[m.anchor[0],m.anchor[1]-70];return{x:b.x+q[0]-m.anchor[0],y:b.y-(b.jumpZ||0)+q[1]-m.anchor[1]};};
 const makeBoss=TD.makeGosfer;
 TD.makeGosfer=function(G,x,y){
  const b=makeBoss(G,x,y),tick=b.tick,under=b.drawUnder,over=b.drawOver;
  b.sidePanels39=[180,620].map(x=>{const s=TD.makeStructure({kind:'od_outer36',x,y:255,visual36:'outer_v',dim36:{hw:22,hh:72}});s.gosferDoor39=true;G.structures.push(s);return s;});
  b.tick=function(dt){
   if(!b.dead&&!b.shield&&b.hp<=b.max*.5&&!b.claymore39){b.claymore39={phase:'throw',t:0,resume:b.state,mines:[{x:180,y:255,side:-1,release:.22},{x:620,y:255,side:1,release:.62}]};b.state='claymore';b.actionT=0;b.firing=0;TD.Audio.play('od75_mineThrow',.6);G.say('GOSFER / BREACH CHARGES! / CLEAR THE SIDE WALLS',G.player);C.log.push({event:'half-health',hp:b.hp});}
   const q=b.claymore39;
   if(q&&q.phase!=='done'&&!b.dead){q.t+=dt;b.t+=dt;b.flash=Math.max(0,b.flash-dt);b.firing=0;
    if(q.phase==='throw'&&q.t>=1.1){q.phase='armed';q.t=0;TD.Audio.play('od75_mineArm',.65);}
    else if(q.phase==='armed'&&q.t>=1.2){q.phase='blast';q.t=0;q.breached=true;C.stats.breaches+=2;for(const m of q.mines){TD.FX.boom(m.x,m.y,160,'gfx_destruction_',6);TD.Audio.play('expB',.7);C.breachWall(G,m);for(let j=0;j<2;j++){const u=TD.makeUnit('c35_flame',m.x+m.side*14,225+j*76,{a:m.side<0?-Math.PI/2:Math.PI/2});u.sense39={home:{x:u.x,y:u.y,a:u.a},memory:8,scan:0,visible:false,known:{x:G.player.x,y:G.player.y}};u.reinforcement39=true;G.units.push(u);}}W.navDirty=true;G.pickups.push({kind:'flamethrower',x:b.x,y:b.y+90,t:0});TD.Cam.kick(8);C.log.push({event:'wall-breaches',reinforcements:4});}
    else if(q.phase==='blast'&&q.t>.6){q.phase='done';b.state='recover';b.actionT=0;}return;
   }
   tick(dt);
  };
  b.drawUnder=function(ctx){under?.(ctx);const q=b.claymore39;if(!q)return;for(const m of q.mines){if(q.phase==='throw'&&q.t>=m.release){const t=M.clamp((q.t-m.release)/.42,0,1);A.draw(ctx,t===1?'od39_claymore_armed':'od39_claymore',M.lerp(b.x,m.x,t),M.lerp(b.y-65,m.y,t)-Math.sin(t*Math.PI)*70,{s:.14,a:t*Math.PI*2*m.side});}else if(q.phase==='armed')A.draw(ctx,'od39_claymore_armed',m.x,m.y,{s:.18,a:m.side*Math.PI/2});}};
  b.drawOver=function(ctx){over?.(ctx);};return b;
 };
 mission.boss=TD.makeGosfer;
 C.breachWall=function(G,m){for(const s of G.boss.sidePanels39)if(Math.abs(s.x-m.x)<30){s.dead=true;s.hp=0;W.remove(s.rect);}};
 const coverDraw=D.drawCover;D.drawCover=function(ctx,s){if(s.gosferDoor39&&s.dead){A.draw(ctx,'l36_lowwall_3',s.x,s.y+40,{s:.72});return true;}return coverDraw(ctx,s);};
 C.breachedWall=(G,y)=>!!G.boss?.claymore39?.breached&&Math.abs(y-255)<105;
 const sidePose39=TD.Escape29.pose;TD.Escape29.pose=function(G){const p=G.player,q=root.TD_NIGHT39_ART.banks['yuri_side/prone_roll/'+(p.sideFacing29||'east')];return p.roll>0&&p.rollFromProne39&&q?frame(q,(.5-p.roll)/.5*q.duration,false):sidePose39(G);};
 C.basePlayerPose=function(G){const p=G.player,q=bank('yuri_base','prone_roll','north');return p.roll>0&&p.rollFromProne39&&q?frame(q,(.5-p.roll)/.5*q.duration,false):null;};
 C.coreShield=function(ctx,c,q){if(!q||q.hp<=0||!c.turrets.some(t=>t.hp>0))return;const seq=root.TD_ASSAULT_ART.sequences.pb20_gosfer_shield;if(seq)A.draw(ctx,seq.frames[Math.floor(c.age*12)%seq.frames.length],q.x,q.y,{s:.45,alpha:q.shieldFlash39>0?.75:.25});};
 C.baseWarning=function(ctx,u){if(u.dead||!['peek','flank'].includes(u.phase))return;const G=TD.game,a=u.attack35,phase=a?.phase||'wait';if(!['wind','burst'].includes(phase))return;const progress=phase==='wind'?1-a.t/(a.windDuration||D.profiles[u.kind]?.wind||1):0,col=phase==='burst'||phase==='recover'&&u.firing>0?'red':phase==='wind'?(progress>.67?'red':progress>.33?'yellow':'green'):'green',socket=TD.Bastion.unitSocket(u),target={x:u.target35?.x??G.player.x,y:G.player.frontCover29?G.player.y-43:405},length=Math.min(95,Math.hypot(target.x-socket.x,target.y-socket.y));ART.draw(ctx,'bmfx_fov_'+col+'_tall',socket.x,socket.y,{ax:159.5,ay:11,a:M.angTo(socket.x,socket.y,target.x,target.y),sx:(['shotgun','double'].includes(u.kind)?48:24)/126,sy:length/267,alpha:col==='green'?.5:.85});};
 const baseMission=TD.MISSIONS.find(m=>m.id===7),baseHud=baseMission.hud;
 baseMission.hud=function(ctx,text,G){const r=baseHud(ctx,text,G),c=G.bastion;if(c.phase==='fight'){const left=c.turrets.filter(t=>t.hp>0).length;text('WAVE '+c.totalWave+' / 4  /  '+(left?'CORE SHIELDED / '+left+' TURRETS':'CORE EXPOSED / BREAK THE DOOR'),320,88,9,left?'#a3e8ff':'#ffce70','center');}return r;};
 for(const [id,key]of [['flamethrower','od39_flame_pickup'],['cryo_lance','od39_cryo_pickup']]){const alias='hud27_gun_'+id;root.TD_HUD27_ART.assets[alias]=P.assets[key];root.TD_ASSAULT_ART.assets[alias]=P.assets[key];}
 const hudModel=TD.CornerHUD26.model;TD.CornerHUD26.model=function(G,pseudo){const v=hudModel(G,pseudo),id=pseudo?G.player.groundGun:G.player.weapons?.[G.player.wi||0]?.id;if(['flamethrower','cryo_lance'].includes(id)){v.weapon=id;v.weaponKey='hud27_gun_'+id;}return v;};
 ART.warm(Object.keys(P.assets));
})(window);
