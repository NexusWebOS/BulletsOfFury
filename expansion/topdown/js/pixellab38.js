/* Reviewed PixelLab plates. Frames, sockets and release events share one clock. */
(function(root){
 'use strict';
 const TD=root.TD,P=root.TD_PIXELLAB38_ART,A=TD.AssaultArt,C=TD.Contra34,D=TD.Depth35,M=TD.M;
 const api=TD.PixelLab38={build:P.build,enabled:new URLSearchParams(location.search).get('pixelLab')!=='0',stats:{releases:0,turretReleases:0,draws:0}};
 if(!api.enabled)return;
 const bank=(m,a,d='south')=>P.banks[m+'/'+a+'/'+d];
 const at=(q,t=0,loop=q?.loop)=>q?.frames[loop?Math.floor(Math.max(0,t)*q.fps)%q.frames.length:Math.min(q.frames.length-1,Math.floor(Math.max(0,t)*q.fps))];
 const ready=q=>!!q&&q.frames.every(k=>ART.get(k));
 const front=u=>!u.kind35&&u.phase!=='flank'&&!u.rollState35&&!!bank(D.role(u)+'_pseudo3d','fire');
 api.bank=bank;api.frame=at;
 api.blit=function(ctx,k,x,y,s=1,o={}){if(!TD.Grid21?.flat(ctx,k,x,y,s,o))A.draw(ctx,k,x,y,{s,...o});api.stats.draws++;};
 function frontBank(u){
  const m=D.role(u)+'_pseudo3d',a=u.action35;
  if(a==='fire_forward')return bank(m,'fire');
  if(a==='spin_up'||a==='spin_down')return bank(m,a);
  if(a==='reload_break_action')return bank(m,'reload');
  if(a==='draw_forward')return bank(m,'draw_forward')||bank(m,'ready');
  if(a==='reload_pump')return null;
  return bank(m,'ready');
 }
 const frontPose=C.frontPose;
 C.frontPose=function(u){
  if(u.moving35&&!['wind','burst'].includes(u.attack35?.phase)){const side=u.lateral42>0?'east':'west',q=C.clip('side',D.role(u),'walk',side);if(q)return at(q,(u.gait||0)*1.2,true);}
  if(front(u)&&u.artMode38!=='legacy'&&!['enter','rush','vault'].includes(u.phase)){
   const q=frontBank(u);if(ready(q))return at(q,u.actionT35||0,u.action35==='fire_forward'&&D.role(u)==='minigunner');
  }return frontPose(u);
 };
 const attack=D.attack;
 function set(u,a){u.action35=a;u.actionT35=0;}
 function schedule(u,q,d){
  const role=D.role(u),events=q.events;
  if(events.left_shot!=null)return[events.left_shot/q.fps,events.right_shot/q.fps];
  if(events.shot!=null)return[events.shot/q.fps];
  if(role==='minigunner')return Array.from({length:d.count},(_,i)=>i*2/q.fps);
  const start=(role==='sniper'?3:role==='flamethrower'?1:2)/q.fps;
  const gap=Math.max(d.gap,role==='machine_gunner'?.25:role==='roller_alien'?.25:d.gap);
  return Array.from({length:d.count},(_,i)=>start+i*gap);
 }
 D.attack=function(u,dt,allow,emit){
  if(!TD.game?.bastion||!front(u))return attack(u,dt,allow,emit);
  const role=D.role(u),q=bank(role+'_pseudo3d','fire'),d=D.profiles[u.kind];
  // A lazy-loaded bank may become ready halfway through a legacy volley.
  // Select the controller at a cycle boundary so its event queue stays valid.
  if(u.artMode38!=='native'&&u.attack35?.phase&&u.attack35.phase!=='wait'){u.artMode38='legacy';return attack(u,dt,allow,emit);}
  const required=[q,bank(role+'_pseudo3d','ready'),bank(role+'_pseudo3d',role==='minigunner'?'spin_up':'draw_forward')].filter(Boolean);
  if(role==='minigunner')required.push(bank(role+'_pseudo3d','spin_down'));
  if(role==='double_barrel')required.push(bank(role+'_pseudo3d','reload'));
  if(!required.every(ready)){u.artMode38='legacy';return attack(u,dt,allow,emit);}u.artMode38='native';
  const a=u.attack35||(u.attack35={phase:'wait',t:u.fireCd??.8});
  u.actionT35=(u.actionT35||0)+dt;u.fireAge34=(u.fireAge34||0)+dt;u.flashAge38=(u.flashAge38??99)+dt;u.warn=0;
  if(a.phase==='wait'){
   u.firing=0;if(allow)a.t-=dt;
   if(a.t<=0&&allow){const draw=bank(role+'_pseudo3d',role==='minigunner'?'spin_up':'draw_forward');a.phase='wind';a.windDuration=Math.max(d.wind,draw?.duration||0);a.t=a.windDuration;set(u,role==='minigunner'?'spin_up':'draw_forward');const p=TD.game.player;u.target35={x:p.x,y:p.y};}
  }else if(a.phase==='wind'){
   u.firing=0;u.warn=Math.max(0,a.t);a.t-=dt;
   if(!allow){a.phase='wait';a.t=.4;set(u,'idle');return;}
   if(a.t<=0){a.phase='burst';a.sent=0;a.events38=schedule(u,q,d);a.length38=Math.max(q.duration,Math.ceil((a.events38.at(-1)+1/q.fps)/q.duration)*q.duration);set(u,'fire_forward');u.fireT=u.fireAge34=0;}
  }else if(a.phase==='burst'){
   // No queued round survives an interrupted attack or a destroyed owner.
   if(u.dead){a.phase='recover';a.t=d.cd;u.firing=0;set(u,role==='minigunner'?'spin_down':d.reload||'idle');return;}
   while(a.sent<a.events38.length&&u.actionT35+1e-9>=a.events38[a.sent]){
    u.barrel38=a.sent%2?'right':'left';
    for(const off of d.fan)emit(d.shot,off,d.speed,a.sent);
    TD.Audio.play(d.cue,.5);u.flashAge38=0;api.stats.releases++;D.attacks[u.kind]=(D.attacks[u.kind]||0)+1;a.sent++;
   }
   u.firing=Math.max(0,a.length38-u.actionT35);
   if(u.actionT35>=a.length38){a.phase=role==='minigunner'?'down':'recover';a.t=Math.max(d.cd,bank(role+'_pseudo3d','reload')?.duration||0);u.recoverDuration35=a.t;set(u,role==='minigunner'?'spin_down':d.reload||'idle');}
  }else if(a.phase==='down'){
   const spin=bank(role+'_pseudo3d','spin_down');u.firing=Math.max(0,spin.duration-u.actionT35);
   if(u.actionT35>=spin.duration){a.phase='recover';set(u,'idle');}
  }else if(a.phase==='recover'){
   u.firing=0;a.t-=dt;
   if(a.t<=0){a.phase='wait';a.t=.9;set(u,'idle');}
  }
 };
 api.unitSocket=function(u,scale,yOffset=0){
  const k=C.frontPose(u),m=P.assets[k];if(!m?.muzzle)return null;
  const p=m.muzzles?.[u.barrel38]||m.muzzle;return{x:u.x+(p[0]-m.anchor[0])*scale,y:u.y+yOffset-(u.lift||0)+(p[1]-m.anchor[1])*scale};
 };
 api.drawUnitMuzzle=function(ctx,u,scale,yOffset=0){
  if((u.flashAge38??99)>.12||u.dead)return;
  const p=api.unitSocket(u,scale,yOffset),q=P.banks['fx/forward_muzzle_flash'];if(p)api.blit(ctx,at(q,u.flashAge38,false),p.x,p.y,.38);
 };
 const core=C.corePose;C.corePose=function(c,obj){const q=bank('door_core_pseudo3d',obj&&obj.hp<=0?'inactive':'active');return ready(q)?at(q,c.age,true):core(c);};
 const turret=C.turretPose;C.turretPose=function(t){const q=bank('wall_turret_gun_pseudo3d','fire');return t.kind==='gun'&&ready(q)?at(q,t.fire38?t.attackT:0,false):turret(t);};
 api.turretSocket=function(t){const m=P.assets[C.turretPose(t)],p=m?.muzzles?.[t.barrel38||'left']||m?.muzzle;return p?{x:t.x+p[0]-m.anchor[0],y:t.y+p[1]-m.anchor[1]}:{x:t.x,y:t.y+12};};
 api.stepTurret=function(G,t,dt,enemyDt,emit){
  const q=bank('wall_turret_gun_pseudo3d','fire');if(t.kind!=='gun'&&t.kind!=='laser')return false;
  if(t.hp<=0){t.fire38=false;return true;}
  t.age+=dt;t.flash=Math.max(0,t.flash-dt);t.flashAge38=(t.flashAge38??99)+dt;t.cd-=enemyDt;
  // One visible windup for either turret, followed by a committed volley.
  if(!t.fire38&&t.cd<=.9){if(!t.warning38){t.warning38=true;t.target38={x:G.player.x,y:G.player.frontCover29?G.player.y-43:405};TD.Audio.play('od75_turretCharge',.4);}t.warningProgress38=M.clamp(1-t.cd/.9,0,1);}
  if(t.cd<=0&&!t.fire38){t.fire38=true;t.attackT=0;t.sent38=0;t.cd=t.kind==='laser'?3.5:2.7;t.warning38=false;}
  if(t.fire38){
   t.attackT+=enemyDt;
   const native=t.kind==='gun'&&ready(q),ev=native?[q.events.left_shot/q.fps,q.events.right_shot/q.fps]:t.kind==='laser'?[.12]:[.12,.32];
   while(t.sent38<ev.length&&t.attackT+1e-9>=ev[t.sent38]){
    t.barrel38=t.sent38?'right':'left';const p=api.turretSocket(t),before=G.bastion.enemyShots.length;
    emit(G,p.x,p.y,t.kind==='laser'?'laser':'mg');const s=G.bastion.enemyShots[before];if(s){s.tx=t.target38.x;s.ty=t.target38.y;s.owner38=t;s.turret38=true;}
    TD.Audio.play(t.kind==='laser'?'od75_plasma':'od75_minigunShot',.65);t.flashAge38=0;t.sent38++;api.stats.turretReleases++;
   }
   if(t.attackT>=(native?q.duration:.5))t.fire38=false;
  }return true;
 };
 api.drawTurretWarning=function(ctx,t,G){if(t.hp<=0)return;const p=api.turretSocket(t),target=t.target38||{x:G.player.x,y:405},col=t.fire38?'red':t.warning38?(t.warningProgress38>.67?'red':t.warningProgress38>.33?'yellow':'green'):'green',length=Math.hypot(target.x-p.x,target.y-p.y);ART.draw(ctx,'bmfx_fov_'+col+'_tall',p.x,p.y,{ax:159.5,ay:11,a:M.angTo(p.x,p.y,target.x,target.y),sx:(t.kind==='laser'?30:44)/126,sy:length/267,alpha:t.fire38||t.warning38?.9:.4});};
 api.drawTurretMuzzle=function(ctx,t){
  if(t.kind!=='gun'||t.hp<=0||(t.flashAge38??99)>.12)return;const m=P.assets[C.turretPose(t)],p=m?.muzzles?.[t.barrel38];
  if(p)api.blit(ctx,at(P.banks['fx/forward_muzzle_flash'],t.flashAge38,false),t.x+p[0]-m.anchor[0],t.y+p[1]-m.anchor[1],.3);
 };
 const effectKinds={mg:'bullet',laser:'plasma',rocket:'rocket',pellet:'shotgun',double_pellet:'double_shotgun',acid:'acid',plasma:'plasma',flame:'flamethrower',orb:'prism'};
 const forwardShot=C.frontShot;
 C.frontShot=function(ctx,s){
  if(s.t<0)return true;
  const kind=['pellet','double_pellet'].includes(s.kind)?'bullet':effectKinds[s.kind];const q=P.banks['fx/'+kind+'_toward_viewer'];if(!ready(q))return forwardShot(ctx,s);
  const progress=M.clamp(s.t/s.duration,0,1),size=s.kind==='flame'?.55:s.kind==='rocket'?1.05:s.kind==='laser'?.85:1;
  // These authored frames already grow toward camera. Do not shrink a 4px
  // distant round below a screen pixel, or loop it back to its distant pose.
  const k=q.frames[Math.min(q.frames.length-1,Math.floor(progress*(q.frames.length-1)))],dx=s.tx-s.sx,dy=s.ty-s.sy,n=Math.hypot(dx,dy)||1,travel=Math.hypot(s.x-s.sx,s.y-s.sy);
  if(s.kind==='flame'){api.blit(ctx,k,s.x,s.y,size);return true;}
  if(s.kind!=='flame')for(let j=2;j>0;j--){const gap=Math.min(travel,j*7);api.blit(ctx,k,s.x-dx/n*gap,s.y-dy/n*gap,size*.75,{alpha:.38-j*.08});}
  api.blit(ctx,k,s.x,s.y,size*1.25,{tint:'#060b18'});api.blit(ctx,k,s.x,s.y,size,{flash:.12});return true;
 };
 const shot=D.drawShot;
 D.drawShot=function(ctx,s,lift=0){
  const kind=effectKinds[s.kind||s.attackKind35]||'bullet',name=kind==='bullet'?'ballistic':kind==='plasma'&&(s.kind||s.attackKind35)==='laser'?'laser':kind;
  const side=TD.game?.escape29&&!TD.game.escape29.finished,view=side?'side':'topdown',vx=s.vx||0,vy=s.vy||0;
  const dir=side?vx>=0?'east':'west':Math.abs(vx)>Math.abs(vy)?vx>=0?'east':'west':vy>=0?'south':'north';
  const q=P.banks['fx/'+name+'/'+view+'/'+dir];if(!ready(q))return shot(ctx,s,lift);
  // Every shotgun pellet keeps its own collision and sprite; the multi-pellet
  // sheet is reserved for a whole discharge and cannot be stamped on each pellet.
  const single=['shotgun','double_shotgun'].includes(name)?P.banks['fx/ballistic/'+view+'/'+dir]:q;
  const k=at(single,side?s.t||0:(s.t||0)/60,true),scl=name==='flamethrower'?.34:name==='rocket'?.75:1.2,angle=Math.atan2(vy,vx)-({east:0,west:Math.PI,north:-Math.PI/2,south:Math.PI/2}[dir]);
  // Overlapping flame tongues must not paint enlarged dark silhouettes over
  // one another; their authored edge already separates them from scenery.
  if(name==='flamethrower'){api.blit(ctx,k,s.x,s.y-lift,scl,{a:angle});return;}
  const n=Math.hypot(vx,vy)||1;if(name!=='flamethrower')for(let j=2;j>0;j--)api.blit(ctx,k,s.x-vx/n*j*6,s.y-lift-vy/n*j*6,scl*.7,{a:angle,alpha:.3-j*.06});
  api.blit(ctx,k,s.x,s.y-lift,scl*1.3,{a:angle,tint:'#060b18'});api.blit(ctx,k,s.x,s.y-lift,scl,{a:angle,flash:.12});
 };
 const sidePose=TD.Escape29.pose;
 const stepEscape=TD.Escape29.step;
 TD.Escape29.step=function(G,dt){const p=G.player,age=p.shotAge||0;p.fireT38=(p.fireT38??99)+dt;stepEscape(G,dt);if(p.firing>0&&(p.shotAge||0)<=age&&p.fireT38>=bank('yuri_side','fire','east').duration)p.fireT38=0;};
 TD.Escape29.pose=function(G){
  const p=G.player,e=G.escape29,side=p.sideFacing29||'east';
  if(!['corridor','escape'].includes(e.phase)||p.dead||p.vault29||p.jump>0||p.slide29>0||p.sideCover29||p.freeAim||p.stance==='crouch'&&p.moving)return sidePose(G);
  const firing=p.firing>0||(p.fireT38??99)<bank('yuri_side','fire',side).duration;
  let a=p.roll>0?'roll':p.prone?(firing?'prone_fire':p.moving?'crawl':'prone_idle'):p.stance==='crouch'?'crouch_enter':firing?(p.moving?'run_fire':'fire'):p.moving?'run':'idle';
  const q=bank('yuri_side',a,side);if(!ready(q))return sidePose(G);
  const t=a==='roll'?(.5-p.roll)/.5*q.duration:a==='crouch_enter'?q.duration-1/q.fps:firing?(p.fireT38??99)<q.duration?p.fireT38:p.shotAge||0:p.sideGait29||e.age;
  return at(q,t,['idle','walk','run','crawl','prone_idle'].includes(a));
 };
 const footPose=TD.footPose;
 TD.footPose=function(p){
  if(p.pilot!=='yuri'||p.pseudo3D||p.sideScroll||p.cover||p.dead||p.action||p.roll>0||p.jump>0||p.vault29||p.scripted)return footPose(p);
  if(Math.abs(M.wrap(p.aim-Math.PI))>.25)return footPose(p);
  let a=p.stanceTransition?.t<.46?(p.stanceTransition.to==='prone'?'prone_enter':null):p.prone?(p.firing>0?'prone_fire':!p.moving?'prone_idle':null):p.stance==='crouch'?'crouch_enter':p.firing>0?'fire':p.moving?'walk':'idle';
  const q=bank('yuri_topdown',a,'north');if(!ready(q))return footPose(p);
  const t=p.stanceTransition?.t<.46?p.stanceTransition.t/.46*q.duration:a==='crouch_enter'?q.duration-1/q.fps:p.firing>0?p.shotAge||0:p.moving?(p.gaitPhase||0)*q.duration:p.poseT||0;
  return{key:at(q,t,['walk','run','idle','prone_idle'].includes(a)),scale:1,angle:0,action:a,dir:'north'};
 };
 // Gosfer's draw and socket owners call this same whole-plate selector.
 const gosfer=TD.gosferPose;
 TD.gosferPose=function(b){
  if(b.dead||['dialogue','transform'].includes(b.state))return gosfer(b);
  const moving=['patrol','dash','enter'].includes(b.state),di=b.state==='dash'||Math.abs(b.vx||0)>.15?(b.vx||b.dodge||1)>0?'east':'west':'south';
  const q=moving?bank('gosfer_topdown','walk',di):b.state==='shoot'?bank('gosfer_pseudo3d','fire'):bank('gosfer_topdown','ready');
  return ready(q)?{key:at(q,moving?b.gait||b.t||0:b.attackT||0,moving),flip:false,bank:'pixellab38',phase:0}:gosfer(b);
 };
 const helios=C.heliosPose;
 C.heliosPose=function(b){const q=bank('fire_prism_topdown','prism_lightning','south');if(!b.dead&&b.state==='lightning'&&ready(q))return{key:at(q,b.t||0,false),flip:false,action:'prism_lightning'};return helios(b);};
 // Preserve the authored route/collision map; replace its floor material and field.
 const mission=TD.MISSIONS.find(m=>m.id===3);mission.map.key='pl38_fortress_floor';
 const drawCover=D.drawCover;
 D.drawCover=function(ctx,s){
  if(s.gate36){const q=bank('electrical_gate_topdown',s.dead?'inactive':'active');if(ready(q)){A.draw(ctx,at(q,TD.game.time,true),s.x,s.y+s.type.hh,{s:1,flash:s.flash>0?1:0});return true;}}
  return drawCover(ctx,s);
 };
 api.drawCorridorBackdrop=function(ctx,G){
  const k='pl38_service_corridor_far',m=P.assets[k];if(!ART.get(k))return false;
  const e=G.escape29,w=m.size[0]*1.25,first=Math.floor(e.camX/w)*w;
  for(let x=first-w;x<e.camX+900;x+=w)A.draw(ctx,k,x,96,{s:1.25});return true;
 };
 const fore=TD.Base33.drawForeground;
 TD.Base33.drawForeground=function(ctx,G){fore(ctx,G);const e=G.escape29,k='pl38_service_corridor_foreground',w=640,first=Math.floor(e.camX/w)*w;for(let x=first;x<e.camX+900;x+=w)A.draw(ctx,k,x,82,{s:1.25});};
 api.hatchKey=function(G){const e=G.escape29,q=bank('floor_hatch_side','open');return ready(q)?at(q,e.phase==='hinge'?e.t:0,false):null;};
 api.hatchDuration=bank('floor_hatch_side','open').duration;
 ART.warm(Object.keys(P.assets));
})(window);
