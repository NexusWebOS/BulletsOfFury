"use strict";
/* Galaga reference: dvjapcHsqXY, sampled00:15-00:44 and02:03-02:14.
   Regular aircraft only. Motion is numeric route data; existing authored heading
   cells, emitters, warning/attack clocks, hit feedback and death remain native. */
const GF113={base:{spawn:spawnEnemy,beginAI:ai27Begin,endAI:ai27End,entry:enemyEntrySweep,
 frenzy:enemyFrenzyTick,route:eb11OwnsRoute,begin:beginStage,blocked:ai27ShotBlocked},
 groups:[],serial:0,events:[],flying:null,
 profiles:{small:{speed:200,turn:3.8,gap:.75,hold:.62,max:14},medium:{speed:160,turn:3.0,gap:1.05,hold:.85,max:16},large:{speed:136,turn:2.4,gap:1.45,hold:1.05,max:18}},
 models:{2:new Set(['skimmer','wasp','thunder','interceptor','basalt']),3:new Set(['interceptor']),
 4:new Set(['command','heavyjet']),5:new Set(['skimmer']),6:new Set(['fighter_navy','fighter_teal','fighter_black','bomber_navy','bomber_black','heavy_wind','wind_zephyr','wind_gale','wind_stratus']),
 7:new Set(['slime','missilejet','crescent']),8:new Set(['interceptor','imp','voidjet','hellwing','harrier']),9:new Set(['comet','skimmer','echo','tidal','beamship','harrier'])}};
function gf113State(e){return e._v31||e._i31||e._s411||e._s511||e._s711||e._s811||e._s911||e._s1aFlight||e._r46||null;}
function gf113Model(e){return e._v31?.model||e._i31?.model||e._s411?.model||e._s511?.model||e._s611?.model||e._s711?.model||e._s811?.model||e._s911?.model||e._r46?.model||e.type;}
function gf113Live(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function gf113Own(e){return !!e?._gf113&&!e._gf113.released&&gf113Live(e);}
function gf113Eligible(e){
 if(window.GF113_OFF||!gf113Live(e)||bossActive||subBossActive||bossDefeated||run.stage<1||run.stage>9||run._gp4StageX||e._boss||e.boss||e._mini||e._amini||e._rebels||e.prop||e._prop||e.ground||e._groundTraffic||e._modTurret||e._sc12||e._ca111)return false;
 if(e._jetManeuver||e._cp22Dash||e._cp22Flight||e._s6Strike||e._fb2Stealth||e._fb9Swoop||e._s1Kamikaze||e._s1Rush||e._wing17||e._s811?.launchOwner)return false;
 if(run.stage===1)return /^s1jetdelta(?:_b)?$/.test(e.type);
 if(run.stage===4&&['s4interceptor','s4rocket'].includes(e.type))return true;
 if(run.stage===5&&e.type==='s5interceptor')return true;
 return !!GF113.models[run.stage]?.has(gf113Model(e));
}
function gf113Log(e,event,extra={}){GF113.events.push({id:e?._gf113?.id,type:e?.type,event,t:efxClock,...extra});if(GF113.events.length>800)GF113.events.shift();}
function gf113Head(e){return gf113State(e)?.head??e._s611?.head??Math.PI/2+(e.spin||0);}
function gf113SetHead(e,a){
 if(e._gf113)e._gf113.flightHeading=a;
 const S=gf113State(e);if(S)S.head=a;
 if(e._r46)e._r46.head=a;if(e._s611)e._s611.head=a;
 e._s1aNativeHead=a;e.spin=run.stage===1?0:a-Math.PI/2;
}
function gf113Committed(e){const S=gf113State(e),phase=S?.phase||'';
 return /tell|warn|charge|burst|beam|fire|lock|pounce|claw|strike|roll|dash|launch|bombing|spin|rev|turn/.test(phase)||!!S?.beams?.some(b=>b.t<b.life)||!!S?.heavy;
}
function gf113AttackReady(e,cone=.65){const A=e?._gf113;if(!A)return true;if(A.phase==='queue'||A.phase==='exit')return false;
 const T=targetShip(e.x,e.y),head=A.active&&!A.paused?A.flightHeading:gf113Head(e);return e.y>viewTopY()+35&&e.y<T.y-75&&Math.abs(s1aAngle(Math.atan2(T.y-e.y,T.x-e.x)-head))<cone;
}
// Cubic Hermite segments and a distance lookup give every follower the same
// smooth path at a controlled speed. No rendering transform is introduced.
function gf113Track(points){
 const out=[{...points[0],s:0}],n=points.length;let length=0,prev=points[0];
 for(let i=0;i<n-1;i++){
  const a=points[i],b=points[i+1],p=points[Math.max(0,i-1)],q=points[Math.min(n-1,i+2)],m={x:(b.x-p.x)*.45,y:(b.y-p.y)*.45},v={x:(q.x-a.x)*.45,y:(q.y-a.y)*.45};
  for(let j=1;j<=28;j++){const t=j/28,t2=t*t,t3=t2*t,A=2*t3-3*t2+1,B=t3-2*t2+t,C=-2*t3+3*t2,D=t3-t2;
   const x=A*a.x+B*m.x+C*b.x+D*v.x,y=A*a.y+B*m.y+C*b.y+D*v.y;length+=Math.hypot(x-prev.x,y-prev.y);out.push({x,y,s:length});prev={x,y};}
 }
 return{points:out,length};
}
function gf113Sample(T,s){const P=T.points;s=clamp(s,0,T.length);let lo=1,hi=P.length-1;
 while(lo<hi){const m=(lo+hi)>>1;if(P[m].s<s)lo=m+1;else hi=m;}
 const a=P[lo-1],b=P[lo],u=(s-a.s)/Math.max(.001,b.s-a.s);return{x:lerp(a.x,b.x,u),y:lerp(a.y,b.y,u),head:Math.atan2(b.y-a.y,b.x-a.x)};
}
function gf113Phase(e,phase,track=null){const A=e._gf113;A.phase=phase;A.pt=0;A.settled=0;A.distance=0;A.track=track;gf113Log(e,phase,{group:A.group.id,slot:A.slot,size:A.size});}
function gf113Entry(e){const A=e._gf113,L=A.left,W=A.width,H=VH-PLAY.y,top=PLAY.y,S=A.side;
 const X=f=>L+W*(S>0?f:1-f),Y=f=>top+H*f;
 const outer=A.size==='large'?.40:.43;
 return gf113Track([{x:e.x,y:e.y},{x:X(.17),y:Y(.14)},{x:X(.20),y:Y(.43)},{x:X(.35),y:Y(.45)},
  {x:X(outer),y:Y(.27)},{x:X(.30),y:Y(.10)},{x:A.home.x,y:A.home.y-44},{x:A.home.x,y:A.home.y}]);
}
function gf113Dive(e){const A=e._gf113,L=A.left,W=A.width,H=VH-PLAY.y,top=PLAY.y,S=A.side,T=targetShip(e.x,e.y),pad=A.pad;
 const tx=clamp(T.x+S*A.slot*Math.max(26,pad*.5),L+pad,L+W-pad),X=f=>L+W*(S>0?f:1-f),Y=f=>top+H*f;
 A.commit={x:tx,y:Math.min(VH-pad*.55,Math.max(top+H*.64,T.y-35))};
 return gf113Track([{x:e.x,y:e.y},{x:e.x+Math.cos(gf113Head(e))*38,y:e.y+Math.sin(gf113Head(e))*38},
  {x:X(.18),y:Y(.40)},{x:tx,y:A.commit.y},{x:X(.80),y:Y(.63)},{x:X(.77),y:Y(.35)},
  {x:A.home.x,y:A.home.y-44},{x:A.home.x,y:A.home.y}]);
}
function gf113Exit(e){const A=e._gf113,S=A.side;
 return gf113Track([{x:e.x,y:e.y},{x:e.x+Math.cos(gf113Head(e))*40,y:e.y+Math.sin(gf113Head(e))*40},
  {x:clamp(e.x+S*A.width*.20,A.left+A.pad,A.left+A.width-A.pad),y:Math.max(PLAY.y+25,e.y-55)},
  {x:S>0?A.left+A.width-A.pad:A.left+A.pad,y:PLAY.y-100},{x:S>0?A.left+A.width+160:A.left-160,y:PLAY.y-230}]);
}
function gf113Attach(e){if(!gf113Eligible(e)||e._gf113)return;
 const L=camLeftX(),R=camRightX(),W=R-L,span=Math.max(e._drawW||e.w||40,e._drawH||e.h||40),model=gf113Model(e);
 let size=span>=112?'large':span>=82?'medium':'small';
 if(run.stage===1)size=e.type.endsWith('_b')?'medium':'small';
 if(run.stage===6)size=/fighter|zephyr/.test(model)?'small':/bomber|stratus|heavy/.test(model)?'large':'medium';
 if(run.stage===8)size=/imp|interceptor/.test(model)?'small':model==='harrier'||model==='voidjet'?'large':'medium';
 if(run.stage===9)size=/comet|echo/.test(model)?'small':/beamship|harrier/.test(model)?'large':'medium';
 const side=e.x<(L+R)/2?1:-1,P=GF113.profiles[size],maxSlots=size==='large'?2:3;
 let G=GF113.groups.find(g=>g.stage===run.stage&&g.size===size&&g.side===side&&g.n<maxSlots&&efxClock-g.born<.8);
 if(!G){G={id:++GF113.serial,order:GF113.groups.length,stage:run.stage,size,side,born:efxClock,n:0};GF113.groups.push(G);if(GF113.groups.length>40)GF113.groups.shift();}
 const slot=G.n++,pad=Math.min(W*.28,Math.max(36,span*.48)),rank=ai27Level(),speed=P.speed*[.92,1,1.06][rank];
 const col=size==='large'?0:slot%2,row=size==='large'?slot:Math.floor(slot/2),fraction=(size==='large'?.25:.20)+col*.18;
 const homeX=clamp(L+W*(side>0?fraction:1-fraction),pad+L,R-pad),homeY=PLAY.y+Math.max(run.stage>=7?145:85,span*.65)+row*Math.max(70,span*.84);
 const A=e._gf113={id:++GF113.serial,size,model,group:G,slot,side,left:L,width:W,pad,nativeFrFlight:!!e._frFlight,flightHeading:gf113Head(e),home:{x:homeX,y:Math.min(VH*.58,homeY)},
 phase:'queue',pt:0,age:0,distance:0,delay:slot*Math.max(P.gap,span*.95/speed)+(G.id%2)*.18+(G.order%2)*.90,speed,last:{x:e.x,y:e.y},offset:{x:0,y:0},held:0,paused:false,track:null};
 // A queue forms wholly outside view. Never relocate a visible native release.
 A.delay=e.y+span*.55<viewTopY()?A.delay:0;
 e._noSep=true;e._frFlight=false;
 gf113Log(e,'attach',{model,size,group:G.id,slot,span});
}
function gf113Blocked(e,p){const A=e._gf113;
 if(p.y<viewTopY()+12||p.y>VH-20)return false;
 for(const o of enemies){if(o===e||!gf113Own(o)||o._gf113.phase==='queue'||o.y<viewTopY()+12||o.y>VH-20)continue;
  const B=o._gf113;if(B.id>A.id)continue;
  const dx=Math.abs(p.x-o.x),dy=Math.abs(p.y-o.y),rx=(Math.max(e.w||30,e._drawW||0)+Math.max(o.w||30,o._drawW||0))*.34,
   ry=(Math.max(e.h||30,e._drawH||0)+Math.max(o.h||30,o._drawH||0))*.34;
  if(dx<rx&&dy<ry){const old=Math.hypot(e.x-o.x,e.y-o.y),next=Math.hypot(p.x-o.x,p.y-o.y);if(next<old-.001)return true;}
 }
 return false;
}
function gf113Advance(e,dt){const A=e._gf113,P=GF113.profiles[A.size];A.age+=dt;A.pt+=dt;A.before={x:e.x,y:e.y};A.first=eBullets.length;
 A.active=false;A.paused=gf113Committed(e)||e._frozen||e._mercuryLock>0||e._shieldStun>0||e._stagger>0;
 if(A.paused){A.nativePosition={x:e.x,y:e.y};return;}
 if(A.phase==='queue'){
  if(A.pt<A.delay){A.active=true;A.desired={x:e.x,y:e.y};return;}
  gf113Phase(e,'entry',gf113Entry(e));
 }
 if(A.age>P.max&&A.phase!=='exit')gf113Phase(e,'exit',gf113Exit(e));
 if(A.phase==='station'){
  A.active=true;A.desired={x:e.x,y:e.y};gf113SetHead(e,gf113Head(e)+clamp(s1aAngle(Math.PI/2-gf113Head(e)),-2.4*dt,2.4*dt));
  if(Math.abs(s1aAngle(Math.PI/2-gf113Head(e)))<.15)A.settled+=dt;
  if(A.settled>P.hold+A.slot*.35+(A.group.order%2)*.45)gf113Phase(e,'dive',gf113Dive(e));else return;
 }
 if(!A.track)return;
 // Blend out only the positional drift of a native committed attack, preserving
 // its complete warning/beam/roll interval and avoiding a snap back to the route.
 if(A.wasPaused){const old=gf113Sample(A.track,A.distance);A.offset={x:e.x-old.x,y:e.y-old.y};A.wasPaused=false;}
 const fade=Math.max(0,1-dt*1.3);A.offset.x*=fade;A.offset.y*=fade;
 // Physical pursuit follows the distance-sampled curve with a bounded yaw rate.
 // Heading and travel therefore agree even across a native attack pause.
 const look=Math.max(55,A.speed/P.turn*1.5),here=gf113Sample(A.track,A.distance);
 const advance=Math.hypot(here.x+A.offset.x-e.x,here.y+A.offset.y-e.y)<look?A.speed*dt:0;
 const next=Math.min(A.track.length,A.distance+advance),q=gf113Sample(A.track,Math.min(A.track.length,next+look));
 const tx=q.x+A.offset.x,ty=q.y+A.offset.y,want=Math.atan2(ty-e.y,tx-e.x),head=gf113Head(e)+clamp(s1aAngle(want-gf113Head(e)),-P.turn*dt,P.turn*dt);
 const end=gf113Sample(A.track,A.track.length),remaining=Math.hypot(end.x+A.offset.x-e.x,end.y+A.offset.y-e.y);
 const alignment=clamp((1+Math.cos(s1aAngle(want-gf113Head(e))))*.5,.10,1);
 const speed=(next>A.track.length-look?Math.min(A.speed,Math.max(18,remaining*2.2)):A.speed)*alignment;
 const step=Math.min(speed*dt,Math.hypot(tx-e.x,ty-e.y)),p={x:e.x+Math.cos(head)*step,y:e.y+Math.sin(head)*step};
 const yielding=gf113Blocked(e,p);
 if(yielding){A.held+=dt;p.x=e.x+(p.x-e.x)*.30;p.y=e.y+(p.y-e.y)*.30;}else A.held=0;
 A.distance=yielding?A.distance+(next-A.distance)*.30:next;A.active=true;A.desired=p;e.x=p.x;e.y=p.y;
 const dx=e.x-A.before.x,dy=e.y-A.before.y;if(Math.hypot(dx,dy)>.001)gf113SetHead(e,Math.atan2(dy,dx));
 e.vx=dx/Math.max(.001,dt)/60;e.vy=dy/Math.max(.001,dt)/60;
 if(A.distance>=A.track.length-look&&remaining<12){
  if(A.phase==='entry')gf113Phase(e,'station');
  else if(A.phase==='dive'){A.didDive=true;gf113Phase(e,'rejoin');}
  else if(A.phase==='exit'){e.dead=true;gf113Log(e,'depart');}
 }
 if(A.phase==='rejoin')gf113Phase(e,'exit',gf113Exit(e));
}
spawnEnemy=function(){const e=GF113.base.spawn.apply(this,arguments);if(e)gf113Attach(e);return e;};
eb11OwnsRoute=function(e){return gf113Own(e)||GF113.base.route.apply(this,arguments);};
enemyEntrySweep=function(e){if(gf113Own(e))return;return GF113.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(gf113Own(e))return;return GF113.base.frenzy.apply(this,arguments);};
ai27Begin=function(e,dt){const old=GF113.base.beginAI.apply(this,arguments);
 if(gf113Own(e)&&(bossActive||subBossActive||bossDefeated||e._s811?.launchOwner||e._s811?.phase==='launch')){e._gf113.released=true;e._gf113.active=false;e._frFlight=e._gf113.nativeFrFlight;gf113Log(e,'native-handoff');}
 if(gf113Own(e)){e._frFlight=false;gf113Advance(e,dt);if(e._ai27)e._ai27.dx=0;
 const S=gf113State(e);if(S&&!gf113Committed(e)&&!gf113AttackReady(e)&&Number.isFinite(S.cd))S.cd=Math.max(S.cd,.10);
 }return old;};
// Native movement helpers become no-ops only while the route owns travel.
// Their callers still advance the original weapons, phase clocks and sounds.
for(const name of ['v31Fly','i31Fly','s411Fly','s511Fly','s711Fly','s811Fly','s911Fly','r46Fly']){
 const base=globalThis[name];if(typeof base!=='function')continue;
 globalThis[name]=function(e){if(gf113Own(e)&&e._gf113.active)return;return base.apply(this,arguments);};
}
ai27End=function(e,old){const A=e?._gf113;
 if(A&&!A.released&&gf113Live(e)){
  if(A.paused){A.wasPaused=true;}
  else if(A.active&&A.desired){
   const dx=A.desired.x-e.x,dy=A.desired.y-e.y;e.x=A.desired.x;e.y=A.desired.y;
   // Legacy direct movers may add a small step after the routed position.
   // Rebase newly released rounds with their origin fields, never their damage,
   // velocity, interception policy, homing or lifetime.
   if(Math.abs(dx)+Math.abs(dy)>.0001)for(let i=A.first;i<eBullets.length;i++){
    const b=eBullets[i];if(!b||b.dead)continue;
    if((b.owner||b._owner||b._r46Owner||b._s411Owner||b._s611Owner||b._s1aOwner)&&![b.owner,b._owner,b._r46Owner,b._s411Owner,b._s611Owner,b._s1aOwner].includes(e))continue;
    for(const [x,y]of [['x','y'],['ox','oy'],['x0','y0'],['_x0','_y0'],['_originX','_originY'],['startX','startY']]){if(Number.isFinite(b[x]))b[x]+=dx;if(Number.isFinite(b[y]))b[y]+=dy;}
   }
  }
  if(e._ai27)e._ai27.dx=0;e._frFlight=false;
 }
 const out=GF113.base.endAI.apply(this,arguments);
 if(A&&!A.released&&gf113Live(e)&&A.active&&!gf113Committed(e))gf113SetHead(e,A.flightHeading);
 return out;
};
ai27ShotBlocked=function(){const e=ai27Context;if(gf113Own(e)&&!gf113Committed(e)&&!gf113AttackReady(e,.65))return true;return GF113.base.blocked.apply(this,arguments);};
for(const name of ['s811Start','s911Start','s711Tell']){const base=globalThis[name];if(typeof base==='function')globalThis[name]=function(e){if(gf113Own(e)){const A=e._gf113;if(A.phase==='entry'||!gf113AttackReady(e))return;if(A.active&&!A.paused)gf113SetHead(e,A.flightHeading);}return base.apply(this,arguments);};}
// Queue delays suppress the native primary tick rather than letting weapons
// age or beam directors fire from an aircraft still outside view.
for(const name of ['jetTick','volcTick','s3IceTick','s4ChaseTick','s5SpaceTick','s6StormTick','s711Tick','s811Tick','s911Tick','airPatternTick','aiTick']){
 const base=globalThis[name];if(typeof base!=='function')continue;
 globalThis[name]=function(e){if(gf113Own(e)&&e._gf113.phase==='queue')return;return base.apply(this,arguments);};
}
beginStage=function(){GF113.groups=[];GF113.serial=0;GF113.events=[];return GF113.base.begin.apply(this,arguments);};
globalThis.BOF_GALAGA_FLIGHT={state:GF113,attach:gf113Attach,owns:gf113Own};
