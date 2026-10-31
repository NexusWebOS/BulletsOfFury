/* Cover tactics use live collision objects and the approved Contra animation banks. */
(function(root){
 'use strict';
 const TD=root.TD,D=TD.Depth35,C=TD.Contra34,M=TD.M,W=TD.World,A=TD.Audio,art=TD.AssaultArt;
 const T=TD.Tactics36={build:'overdrive1016-tactics36-r1',stats:{coverAcquired:0,closeAdvances:0,reloadsHidden:0,rollTransfers:0,coverLost:0,sideCoverStops:0},log:[]};
 const kinds=new Set(['rifle','heavy','laser','rocket','shotgun','double','roller','flame']);
 const dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y),clamp=M.clamp;
 const frame=(q,t,loop=q?.loop)=>q?.frames[loop?Math.floor(Math.max(0,t)*q.fps)%q.frames.length:Math.min(q.frames.length-1,Math.floor(Math.max(0,t)*q.fps))];
 const record=(u,event,s)=>{T.log.push({event,kind:u.kind35||u.kind,x:Math.round(u.x),y:Math.round(u.y),cover:s?.kind||s?.id||s?.x});if(T.log.length>120)T.log.shift();};
 const live=s=>s&&!s.dead&&s.hp!==0&&!s.rect?.dead;
 const rect=s=>s.rect||{x0:s.x-s.type.hw,x1:s.x+s.type.hw,y0:s.y-s.type.hh,y1:s.y+s.type.hh};
 const phase=(t,name)=>{t.state=name;t.time=0;};
 function segment(a,b,q,margin=0){
  let low=0,high=1;const dx=b.x-a.x,dy=b.y-a.y;
  for(const [v,k]of [[-dx,a.x-q.x0+margin],[dx,q.x1-a.x+margin],[-dy,a.y-q.y0+margin],[dy,q.y1-a.y+margin]]){
   if(Math.abs(v)<1e-9){if(k<0)return false;continue;}const x=k/v;if(v<0)low=Math.max(low,x);else high=Math.min(high,x);if(low>high)return false;
  }return true;
 }
 function clear(a,b,r=0){return ![...W.near(Math.min(a.y,b.y)-r,Math.max(a.y,b.y)+r)].some(q=>!q.dead&&q.t==='b'&&segment(a,b,q,r));}
 function open(p,r){if(p.x<r+8||p.x>W.w-r-8||p.y<r+8||p.y>W.h-r-8)return false;return ![...W.near(p.y-r,p.y+r)].some(q=>!q.dead&&q.t==='b'&&p.x+r>q.x0&&p.x-r<q.x1&&p.y+r>q.y0&&p.y-r<q.y1);}
 function occupied(G,s,u){return G.units.some(v=>v!==u&&!v.dead&&v.tactic36?.space==='ground'&&v.tactic36.cover===s&&dist(v,u)<260);}
 function slots(G,u,s){
  const q=rect(s),p=TD.Combat39?.target(u,G)||G.player,r=(u.r||18)+8,c={x:(q.x0+q.x1)/2,y:(q.y0+q.y1)/2};
  const vertical=Math.abs((c.y-p.y)/(q.y1-q.y0+20))>=Math.abs((c.x-p.x)/(q.x1-q.x0+20));
  const sign=vertical?(p.y<c.y?1:-1):(p.x<c.x?1:-1);
  const hide=vertical?{x:clamp(u.x,q.x0+Math.min(20,(q.x1-q.x0)/2),q.x1-Math.min(20,(q.x1-q.x0)/2)),y:sign>0?q.y1+r:q.y0-r}:{x:sign>0?q.x1+r:q.x0-r,y:c.y};
  if(!open(hide,u.r||18)||!segment(p,hide,q))return null;
  const ends=vertical?[{x:q.x0-r-14,y:hide.y},{x:q.x1+r+14,y:hide.y}]:[{x:hide.x,y:q.y0-r-14},{x:hide.x,y:q.y1+r+14}];
  const peek=ends.filter(e=>open(e,u.r||18)&&clear(hide,e,u.r||18)&&clear(e,p)).sort((a,b)=>dist(a,u)-dist(b,u))[0];
  return peek?{cover:s,hide,peek}:null;
 }
 function select(G,u,exclude=null,advance=false){
  const k=u.kind35,desired=k==='shotgun'?155:k==='double'?205:k==='roller'?205:k==='flame'?150:280,current=dist(u,TD.Combat39?.target(u,G)||G.player),choices=[];
  for(const s of G.structures){if(!live(s)||s===exclude||!s.cover||!s.type||s.kind==='od_relay'||/chest|gate|electric/.test(s.kind)||occupied(G,s,u)||dist(u,s)>640)continue;
   const q=slots(G,u,s);if(!q)continue;const range=dist(q.peek,TD.Combat39?.target(u,G)||G.player),fireRange=k==='shotgun'?230:k==='flame'?190:350;
   // A cover slot must let this weapon finish its windup from the peek point.
   // Distant slots otherwise get selected again every time the attack aborts.
   if(range>fireRange||advance&&range>current-35||k==='shotgun'&&range>current+20)continue;
   if(k==='roller'&&exclude&&(dist(q.hide,u)<85||dist(q.hide,u)>390))continue;
   q.score=dist(u,q.hide)*.58+Math.abs(range-desired)*.85+(range<85?110:0);choices.push(q);
  }return choices.sort((a,b)=>a.score-b.score)[0]||null;
 }
 function assign(u,t,q){t.cover=q.cover;t.hide=q.hide;t.peek=q.peek;t.lastPlayer={...(TD.Combat39?.target(u,TD.game)||TD.game.player)};t.coverAge=0;phase(t,'seek');u.cover36=q.cover;T.stats.coverAcquired++;record(u,'acquire',q.cover);}
 function groundMove(G,u,t,target,dt,speed){
  const dx=target.x-u.x,dy=target.y-u.y,d=Math.hypot(dx,dy);if(d<3){u.moveVX36=u.moveVY36=0;return true;}
  let ax=dx/d,ay=dy/d;if(!clear(u,target,(u.r||18)+1)){const f=TD.Nav.step(TD.Nav.field(target.x,target.y,G.t/60),u.x,u.y);if(f){ax=f[0];ay=f[1];}}
  const n=Math.hypot(ax,ay)||1,v=Math.min(speed*(u.freeze39>0?.55:1),d/dt),blend=Math.min(1,dt*10);u.moveVX36=M.lerp(u.moveVX36||0,ax/n*v,blend);u.moveVY36=M.lerp(u.moveVY36||0,ay/n*v,blend);
  const ox=u.x,oy=u.y;u.x+=u.moveVX36*dt;u.y+=u.moveVY36*dt;W.collide(u,u.r,false);u.vx=u.x-ox;u.vy=u.y-oy;u.moving35=Math.hypot(u.vx,u.vy)>.03;u.walk=(u.walk||0)+Math.hypot(u.vx,u.vy)/90;if(Math.abs(u.vx)>.025)u.moveSide36=u.vx>0?'east':'west';
  t.stuck=u.moving35?0:(t.stuck||0)+dt;return dist(u,target)<7;
 }
 function groundEmit(G,u,kind,off,velocity){
  const q=D.groundSocket(u),target=u.target35||G.player,a=M.angTo(q.x,u.y,target.x,target.y)+off,v=M.fwd(a);
  G.eshots.push({k:kind==='laser'?'laser':'mg',attackKind35:kind,contra35:true,x:q.x,y:u.y,vx:v[0]*velocity/60,vy:v[1]*velocity/60,a,dmg:1,life:kind==='flame'?55:120,r:kind==='flame'?7:4,t:0,drawLift:u.y-q.y,liftStart:u.y-q.y,liftEnd:TD.footLift(G.player),spawnX:q.x,spawnY:u.y,flightDist:Math.hypot(target.x-q.x,target.y-u.y),hitsProne:kind==='acid'||kind==='flame'});TD.FX.attachedFlash(u,()=>D.groundSocket(u),a,.1);
 }
 function beginRoll(u,t,q){t.destination=q;t.rollFrom=t.cover;t.rollSide=q.hide.x>=u.x?'east':'west';u.rollState35='fold';u.rollT35=0;u.attack35={phase:'wait',t:.55};u.firing=0;phase(t,'transfer');D.rolls++;record(u,'fold',t.cover);}
 function groundRoll(G,u,t,dt){
  u.rollT35+=dt;const q=t.destination;
  if(u.rollState35==='fold'&&u.rollT35>=.95){u.rollState35='rolling';u.rollT35=0;t.stuck=0;record(u,'roll',q.cover);}
  if(u.rollState35==='rolling'){
   const arrived=groundMove(G,u,t,q.hide,dt,245);if(dist(u,G.player)<28)TD.hurtPlayer(G,1,u.x,u.y,{hitsProne:true});
   if(arrived&&u.rollT35>.35||u.rollT35>3.2||t.stuck>.4||!live(q.cover)){u.rollState35='unfold';u.rollT35=0;record(u,'unfold',q.cover);}
  }
  if(u.rollState35==='unfold'&&u.rollT35>=.95){u.rollState35=null;u.rollCd35=4.4;assign(u,t,q);if(dist(u,q.hide)<12){phase(t,'hidden');T.stats.rollTransfers++;record(u,'transfer-complete',q.cover);}t.destination=null;}
 }
 const previousTick=TD.unitTick;
 TD.unitTick=function(u,G,dt){
  if(!kinds.has(u.kind35))return previousTick(u,G,dt);if(u.dead)return;u.age=(u.age||0)+dt;u.flash=Math.max(0,(u.flash||0)-dt);u.moving35=false;
  const p=TD.Combat39?.target(u,G)||G.player,range=dist(u,p);if(range>700)return;const t=u.tactic36||(u.tactic36={space:'ground',state:'seek',time:0,cover:null});t.time+=dt;t.coverAge=(t.coverAge||0)+dt;u.rollCd35=(u.rollCd35??2.6)-dt;
  u.look=M.angTo(u.x,u.y,p.x,p.y);u.a=M.turnTo(u.a,u.look,Math.min(1,dt*8));u.sees=clear(u,p)&&(TD.Combat39?.canSee(u,G)??true);u.aware=1;u.mode='alert';
  if(t.state==='transfer'){groundRoll(G,u,t,dt);return;}
  if(t.cover&&!live(t.cover)){T.stats.coverLost++;record(u,'cover-destroyed',t.cover);t.cover=null;u.cover36=null;phase(t,'seek');}
  if(t.cover&&t.state==='hidden'&&t.lastPlayer&&dist(t.lastPlayer,p)>100){const q=slots(G,u,t.cover);if(q){t.hide=q.hide;t.peek=q.peek;t.lastPlayer={x:p.x,y:p.y};phase(t,'seek');}else t.cover=null;}
  if(!t.cover&&(t.retry=(t.retry||0)-dt)<=0){const q=select(G,u);if(q)assign(u,t,q);else t.retry=.6;}
  let allow=false;const recovering=u.attack35?.phase==='recover',stillFiring=(u.firing||0)>0;
  if(!t.cover){
   const goalRange=u.kind35==='shotgun'?145:u.kind35==='double'?190:u.kind35==='flame'?150:245;
   const committed=['wind','burst'].includes(u.attack35?.phase);
   if(!committed){const n=range||1,radial=range<goalRange*.68?-1:range>goalRange+20?1:0;
    if(radial||!u.sees){const goal={x:p.x+(u.x-p.x)/n*goalRange,y:p.y+(u.y-p.y)/n*goalRange};groundMove(G,u,t,goal,dt,u.kind35==='shotgun'?118:88);}
    else if(!recovering){t.strafe=(t.strafe||0)+dt;const side=((G.units.indexOf(u)%2)?1:-1)*(Math.floor(t.strafe/1.5)%2?-1:1),goal={x:u.x-(p.y-u.y)/n*side*48,y:u.y+(p.x-u.x)/n*side*48};if(open(goal,u.r||18)&&clear(u,goal,u.r||18))groundMove(G,u,t,goal,dt,48);}
   }allow=u.sees&&range<(u.kind35==='shotgun'?235:u.kind35==='flame'?205:365);
  }else if(t.state==='seek'){
   if(groundMove(G,u,t,t.hide,dt,u.kind35==='shotgun'?122:100))phase(t,'hidden');
   if(t.stuck>.5||t.time>7){t.cover=null;t.retry=.4;}
  }else if(t.state==='hidden'){
   if(recovering){if(!t.loggedReload&&u.kind35==='double'){T.stats.reloadsHidden++;record(u,'reload-hidden',t.cover);t.loggedReload=true;}}
   else if(t.time>.5){
    if(t.coverAge>6.5&&!u.sees){const alternate=select(G,u,t.cover);if(alternate){assign(u,t,alternate);return;}}
    if(u.kind35==='roller'&&u.rollCd35<=0){const q=select(G,u,t.cover);if(q){beginRoll(u,t,q);return;}}
    const q=u.kind35==='shotgun'&&range>230?select(G,u,t.cover,true):null;
    if(q){T.stats.closeAdvances++;assign(u,t,q);}else phase(t,'peek');
   }
  }else if(t.state==='peek'){
   if(groundMove(G,u,t,t.peek,dt,u.kind35==='shotgun'?108:84)){phase(t,'attack');t.loggedReload=false;}
   if(t.time>3.4||t.stuck>.5){t.cover=null;phase(t,'seek');}
  }else if(t.state==='attack'){
   const limit=u.kind35==='shotgun'?250:u.kind35==='flame'?205:385;allow=u.sees&&range<limit&&!p.dead;
   if(recovering&&!stillFiring){phase(t,'retreat');}
   else if((!u.sees||range>limit)&&t.time>1.2&&!['wind','burst'].includes(u.attack35?.phase)){const q=u.kind35==='shotgun'?select(G,u,t.cover,true):null;if(q){T.stats.closeAdvances++;assign(u,t,q);}else if(range>limit){t.cover=null;t.retry=1.5;phase(t,'seek');}else phase(t,'retreat');}
  }else if(t.state==='retreat'){
   if(groundMove(G,u,t,t.hide,dt,u.kind35==='double'?134:116))phase(t,'hidden');
  }
  const low=!!t.cover&&['hidden','retreat'].includes(t.state)&&!stillFiring;u.coverBlend36=M.lerp(u.coverBlend36||0,low?1:0,Math.min(1,dt*9));
  // Reach safety before starting the pump/break-action clip. Otherwise the
  // walk back consumes half its frames behind a locomotion animation.
  if(t.cover&&t.state!=='hidden'&&recovering&&!stillFiring&&D.profiles[u.kind35].reload){u.attack35.t+=dt;u.actionT35=Math.max(0,(u.actionT35||0)-dt);}
  D.attack(u,dt,allow&&!p.dead,(kind,off,speed)=>groundEmit(G,u,kind,off,speed));
 };
 const groundPose=D.groundPose;
 D.groundPose=function(u){
  const t=u.tactic36;if(t?.space!=='ground')return groundPose(u);const role=D.role(u),side=u.moving35?u.moveSide36||'west':Math.sin(u.a)<0?'east':'west';
  if(u.rollState35){const action={fold:'transform_to_ball',rolling:'ball_roll',unfold:'transform_to_humanoid'}[u.rollState35],q=C.clip('side',role,action,t.rollSide||side);if(q)return{key:frame(q,u.rollT35,u.rollState35==='rolling'),s:root.TD_CONTRA34_ART.roles[role].sideScale*.78};}
  if(u.moving35&&!u.rollState35){const q=C.clip('side',role,t.state==='seek'&&u.kind35==='shotgun'?'run':'walk',side);if(q)return{key:frame(q,u.walk||0,true),s:root.TD_CONTRA34_ART.roles[role].sideScale*.78};}
  if((u.coverBlend36||0)>.015&&!u.rollState35&&!u.moving35){
   if(Math.cos(u.a)>-.25&&(u.action35==='reload_break_action'||u.action35==='reload_pump')){const q=C.clip('front',role,u.action35),time=(u.actionT35||0)/Math.max(.1,u.recoverDuration35||1)*(q.frames.length/q.fps);return{key:frame(q,time,false),s:root.TD_CONTRA34_ART.roles[role].frontScale*.55};}
   const q=C.clip('side',role,'crouch_fire',side);if(q)return{key:q.frames[Math.round(clamp(u.coverBlend36,0,1)*4)],s:root.TD_CONTRA34_ART.roles[role].sideScale*.78};
  }return groundPose(u);
 };
 // Rear-view rooms already own real cover and damage routing. Keep that owner;
 // hold reloads behind it, and move rollers to another surviving barricade.
 const oldFrontManeuver=D.frontManeuver;
 D.frontManeuver=function(G,u,dt){
  if(!kinds.has(u.kind))return oldFrontManeuver(G,u,dt);u.canVault=false;if(u.kind==='double')u.canVault=false;
  const t=u.tactic36||(u.tactic36={space:'front',state:'normal',time:0});t.time+=dt;
  if(u.kind==='roller'){
   u.rollCd35=(u.rollCd35??2.7)-dt;
   if(!u.rollState35&&['peek','hide'].includes(u.phase)&&u.rollCd35<=0&&u.attack35?.phase!=='burst'&&!(u.firing>0)){
    const options=G.bastion.enemyCover.filter(s=>live(s)&&s!==u.cover&&Math.abs(s.x-u.x)>65&&!G.units.some(v=>v!==u&&!v.dead&&v.cover===s&&Math.abs(v.x-s.x)<48));
    const q=options.sort((a,b)=>Math.abs(a.x-G.player.x)-Math.abs(b.x-G.player.x))[0];
    if(q){t.destination=q;t.from={x:u.x,y:u.y};t.rollDuration=clamp(Math.abs(q.x-u.x)/245,.55,1.5);u.rollState35='fold';u.rollT35=0;u.attack35={phase:'wait',t:.6};u.firing=0;u.duck=0;D.rolls++;record(u,'front-fold',u.cover);}
   }
   if(u.rollState35){
    u.rollT35+=dt;u.duck=0;if(u.rollState35==='fold'&&u.rollT35>=.76){u.rollState35='rolling';u.rollT35=0;}
    if(u.rollState35==='rolling'){const f=clamp(u.rollT35/t.rollDuration,0,1);u.x=M.lerp(t.from.x,t.destination.x,f);u.y=M.lerp(t.from.y,t.destination.y-12,f);if(f===1){u.rollState35='unfold';u.rollT35=0;}}
    if(u.rollState35==='unfold'&&u.rollT35>=.76){u.rollState35=null;u.rollCd35=4.6;u.cover=t.destination;u.homeX=u.x;u.phase='hide';u.phaseT=0;u.cycles=0;T.stats.rollTransfers++;record(u,'front-transfer-complete',u.cover);t.destination=null;}
    return true;
   }
   return false;
  }
  if(u.attack35?.phase==='recover'&&!(u.firing>0)&&live(u.cover)&&['hide','peek'].includes(u.phase)){
   u.phase='hide';u.phaseT=0;u.duck=clamp((u.duck||0)+dt*5,0,1);if(!t.reloading&&u.kind==='double'){T.stats.reloadsHidden++;record(u,'front-reload-hidden',u.cover);}t.reloading=true;D.attack(u,dt,false,()=>{});return true;
  }
  if(t.reloading){t.reloading=false;u.phase='hide';u.phaseT=.45;}
  return false;
 };
 // Side-view cover blocks the projectile before the unit behind it. This fixes
 // the old enemy-first collision order without giving a troop invulnerability.
 const hitProp=TD.Base33.hitProp;
 TD.Base33.hitProp=function(G,s,impact,enemy){
  if(hitProp(G,s,impact,enemy))return true;const e=G.escape29;if(!e||!['corridor','escape'].includes(e.phase))return false;
  const solid=e.solids.filter(c=>!c.dead&&(!(!enemy&&G.player.sideCover29===c&&G.player.peekExposed))&&TD.Escape29.hitRect(s,c.x,c.y-c.h/2,c.w/2,c.h/2)).sort((a,b)=>Math.abs(a.x-s.px)-Math.abs(b.x-s.px))[0];
  if(!solid)return false;solid.hp-=enemy?1:s.damage||1;solid.flash=.1;s.dead=true;impact(e,s.x,s.y);T.stats.sideCoverStops++;
  if(solid.hp<=0){solid.dead=true;TD.FX.boom(solid.x,solid.y-30,70,'gfx_destruction_',6);}return true;
 };
 const oldSide=D.sideStep;
 D.sideStep=function(G,u,dt){
  if(!['shotgun','double','roller'].includes(u.kind)||u.phase==='enter')return oldSide(G,u,dt);
  const e=G.escape29,p=G.player,t=u.tactic36||(u.tactic36={space:'side',state:'seek',time:0});if(u.dead)return oldSide(G,u,dt);
  u.age+=dt;u.flash=Math.max(0,u.flash-dt);u.y=TD.Escape29.floorAt(u.x);u.moving35=false;t.time+=dt;
  if(t.hop){
   const h=t.hop;h.age+=dt;const f=clamp(h.age/.82,0,1);u.x=M.lerp(h.x,h.to,f);u.y=M.lerp(h.fromY,TD.Escape29.floorAt(h.to),f)-Math.sin(f*Math.PI)*h.height;u.moving35=true;u.moveSide36=h.to>h.x?'east':'west';u.coverBlend36=0;u.firing=0;
   if(f===1){t.hop=null;phase(t,h.returning?'hidden':'attack');if(!h.returning)u.attack35={phase:'wait',t:.5};}return;
  }
  const sign=u.x<p.x?-1:1,range=Math.abs(u.x-p.x),visible=u.x>e.camX-24&&u.x<e.camX+640/C.view(G).z+24;
  if(t.cover&&!live(t.cover)){t.cover=null;phase(t,'seek');T.stats.coverLost++;}
  if(!t.cover){const options=e.solids.filter(s=>live(s)&&Math.abs(s.x-u.x)<360&&Math.sign(s.x-p.x)===sign).sort((a,b)=>Math.abs(a.x-u.x)-Math.abs(b.x-u.x));t.cover=options[0]||null;if(t.cover){t.hideX=t.cover.x+sign*(t.cover.w/2+20);t.safeSign=sign;record(u,'side-acquire',t.cover);}}
  if(u.kind==='roller'){
   u.rollCd35=(u.rollCd35??1.8)-dt;
   if(!u.rollState35&&u.rollCd35<=0&&u.attack35?.phase!=='burst'&&!(u.firing>0)){
    const next=e.solids.filter(s=>live(s)&&s!==t.cover&&Math.abs(s.x-u.x)>70&&Math.abs(s.x-u.x)<500).filter(s=>{const x=s.x+Math.sign(u.x-s.x)*(s.w/2+20);return !e.solids.some(w=>live(w)&&Math.min(u.x,x)<w.x+w.w/2+16&&Math.max(u.x,x)>w.x-w.w/2-16);}).sort((a,b)=>Math.abs(a.x-p.x)-Math.abs(b.x-p.x))[0];
    if(next){t.destination=next;t.rollFrom=t.cover;t.rollX=next.x+Math.sign(u.x-next.x)*(next.w/2+20);t.rollSide=t.rollX>=u.x?'east':'west';u.rollState35='fold';u.rollT35=0;u.attack35={phase:'wait',t:.6};D.rolls++;}
   }
   if(u.rollState35){u.rollT35+=dt;
    if(u.rollState35==='fold'&&u.rollT35>=.95){u.rollState35='rolling';u.rollT35=0;}
    if(u.rollState35==='rolling'){const dx=t.rollX-u.x,v=Math.sign(dx)*Math.min(Math.abs(dx),245*dt),block=e.solids.find(s=>live(s)&&Math.abs(u.x+v-s.x)<s.w/2+18);if(!block)u.x+=v;else{t.destination=block;t.rollX=block.x+Math.sign(u.x-block.x)*(block.w/2+20);}u.walk=(u.walk||0)+Math.abs(v)/100;u.moveSide36=v>0?'east':'west';if(Math.abs(u.x-t.rollX)<5||u.rollT35>2.4||block){u.rollState35='unfold';u.rollT35=0;}}
    if(u.rollState35==='unfold'&&u.rollT35>=.95){u.rollState35=null;u.rollCd35=4.2;t.cover=t.destination;t.hideX=u.x;t.safeSign=Math.sign(u.x-t.cover.x)||1;phase(t,'hidden');if(t.cover!==t.rollFrom){T.stats.rollTransfers++;record(u,'side-transfer-complete',t.cover);}t.destination=null;}return;
   }
  }
  const recovering=u.attack35?.phase==='recover'&&!(u.firing>0),wantHide=t.cover&&(recovering||t.state==='seek'||t.state==='hidden');
  let goal=u.x;if(wantHide)goal=t.hideX;else if(u.kind==='shotgun'&&range>205)goal=p.x+sign*175;
  const speed=wantHide?118:u.kind==='shotgun'?130:88,move=Math.sign(goal-u.x)*Math.min(Math.abs(goal-u.x),speed*dt),block=e.solids.find(s=>live(s)&&Math.abs(u.x+move-s.x)<s.w/2+16);
  if(!block){u.x+=move;u.moving35=Math.abs(move)>.02;u.walk=(u.walk||0)+Math.abs(move)/100;if(move)u.moveSide36=move>0?'east':'west';}
  else if(wantHide&&Math.sign(u.x-t.cover.x)!==t.safeSign){const s=t.cover;t.hop={x:u.x,to:t.hideX,age:0,fromY:u.y,height:Math.max(64,s.h+28),returning:true};phase(t,'hop');return;}
  if(wantHide&&Math.abs(u.x-t.hideX)<8){if(t.state!=='hidden')phase(t,'hidden');if(recovering&&u.kind==='double'&&!t.loggedReload){T.stats.reloadsHidden++;t.loggedReload=true;record(u,'side-reload-hidden',t.cover);}if(!recovering&&t.time>.55){phase(t,'attack');t.loggedReload=false;}}
  u.coverBlend36=M.lerp(u.coverBlend36||0,wantHide&&!u.moving35&&Math.abs(u.x-t.hideX)<12?1:0,Math.min(1,dt*9));
  // Stand to fire, duck during recovery. A solid remains an actual blocker;
  // the gun only fires when its authored muzzle has a clear line over it.
  const q=C.sideSocket(u,G),target={x:p.x,y:p.y-(p.prone?13:48)},blocked=e.solids.some(s=>live(s)&&segment(q,target,{x0:s.x-s.w/2,x1:s.x+s.w/2,y0:s.y-s.h,y1:s.y}));
  const allow=visible&&!p.dead&&!wantHide&&!blocked&&range<(u.kind==='shotgun'?270:540);
  D.attack(u,dt,allow,(kind,off,speed)=>{const socket=C.sideSocket(u,G),aim=u.target35||target,a=M.angTo(socket.x,socket.y,aim.x,aim.y)+off,v=M.fwd(a);e.enemyShots.push({x:socket.x,y:socket.y,px:socket.x,py:socket.y,vx:v[0]*speed,vy:v[1]*speed,a,kind,life:kind==='flame'?1:3,owner:u,contra35:true});});
  if(!allow&&!wantHide&&t.cover&&t.time>1.2){
   // Low foreground cover cannot be shot through. Step into the visible lane
   // by hopping across it with the existing complete authored jump bank.
   if(!t.hop){const s=t.cover;t.hop={x:u.x,to:s.x-sign*(s.w/2+22),age:0,fromY:u.y,height:Math.max(64,s.h+28),returning:false};phase(t,'hop');}
  }
 };
 const sidePose=C.sidePose;
 C.sidePose=function(u,G){
  const t=u.tactic36;if(t?.space!=='side')return sidePose(u,G);const role=D.role(u),side=u.moving35&&u.moveSide36?u.moveSide36:u.x<G.player.x?'east':'west',s=root.TD_CONTRA34_ART.roles[role].sideScale;
  if(u.rollState35){const action={fold:'transform_to_ball',rolling:'ball_roll',unfold:'transform_to_humanoid'}[u.rollState35],q=C.clip('side',role,action,t.rollSide||side);if(q)return{key:frame(q,u.rollT35,u.rollState35==='rolling'),s,side};}
  if(t.hop){const q=C.clip('side',role,'jump',side);if(q)return{key:frame(q,t.hop.age/.82*(q.frames.length/q.fps),false),s,side};}
  if((u.coverBlend36||0)>.015&&!u.rollState35){const q=C.clip('side',role,'crouch_fire',side);if(q)return{key:q.frames[Math.round(clamp(u.coverBlend36,0,1)*4)],s,side};}
  if(u.moving35&&!u.rollState35){const q=C.clip('side',role,u.kind==='shotgun'?'run':'walk',side);if(q)return{key:frame(q,u.walk||0,true),s,side};}
  return sidePose(u,G);
 };
 // Side objects render before actors, so mask the genuinely overlapping area
 // while a crouched enemy is tucked behind one; projectiles use that same box.
 const sideDraw=C.drawSide;
 C.drawSide=function(ctx,u,G){const s=u.tactic36?.space==='side'&&u.tactic36.cover;if(!live(s)||(u.coverBlend36||0)<.3)return sideDraw(ctx,u,G);ctx.save();ctx.beginPath();ctx.rect(u.x-200,u.y-240,400,300);ctx.rect(s.x-s.w/2,s.y-s.h,s.w,s.h);ctx.clip('evenodd');sideDraw(ctx,u,G);ctx.restore();};
 T.coverSlots=slots;T.selectCover=select;T.clearSegment=clear;
})(window);
