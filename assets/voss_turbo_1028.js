"use strict";
/* Twin cannon perch, own-pixel power charge and continuous harmless overhead passes. */
const VS41={events:[],draws:[],base:{attack:rg4Attack,act:rg4AttackTick,ship:fr27RebelDrawShip,warning:rg4Warning,heavy:rbal19Heavy,gun:ra4Gun,ram:ra4RamHit,orb:rr26Energy,ord:rg4OrdnanceDraw,tick:rebelSquadTick,world:drawWorld,load:stageLoadBegin},foreground:false};
for(const a of Object.values(VS41_ART.banks)){ER28_ART[a.key]=a;XART._src[a.key]=a.path;XART.rdy(a.key);}
stageLoadBegin=function(n,keys){if(n===6||n===10){l23FovWarm();Snd.prepare?.(['bossWeaponCharge','chargeDash','jetDash','enemyBossCannon']);}return VS41.base.load.call(this,n,[...(keys||[]),...([6,10].includes(n)?Object.values(VS41_ART.banks).map(a=>a.key):[])]);};
function vs41Log(event,data={}){VS41.events.push({event,t:rg4State()?.age||0,...data});if(VS41.events.length>500)VS41.events.shift();}
function vs41Active(q){return q?.key==='voss'&&q.rg4?.act?._vs41&&!q.dead;}
function vs41Safe(q){return vs41Active(q)&&['dash','turn-north','north','turn-south','approach'].includes(q.rg4.act.phase);}
function vs41Phase(q,A,phase){A.phase=phase;A.t=0;A.from={x:q.x,y:q.y};A.scale=q._rd21Scale||1;vs41Log(phase,{x:q.x,y:q.y});}
function vs41Frame(q){const A=q.rg4?.act,a=q.rfHeading??Math.PI/2;
 if(vs41Active(q)&&A.phase==='dash')return 72+Math.floor((q.t||A.t)*24)%8;
 if(vs41Active(q)&&A.phase==='north')return 64+Math.floor((q.t||A.t)*24)%8;
 if(Math.abs(Math.atan2(Math.sin(a-Math.PI/2),Math.cos(a-Math.PI/2)))<.09)return 48+Math.floor((q.t||0)*24)%8;
 return Math.round((a+TAU)%TAU/TAU*32)%32;
}
function vs41Cannon(q,side){const mods=fr27RebelModules(q);if(q.dead||mods.some(m=>m.id===(side<0?'left':'right')&&m.hp<=0))return null;const xy=VS41_ART.sockets[side<0?0:1],k=VS41_ART.unit*(q._rd21Scale||1);
 return{x:q.x+(xy[0]-96)*k,y:q.y+(xy[1]-96)*k,side,angle:Math.PI/2};}
function vs41Blit(name,f,x,y,k=1,alpha=1){const a=VS41_ART.banks[name];if(!a||!XART.rdy(a.key))return false;f=(f%a.frames+a.frames)%a.frames;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,x-a.pivot[0]*k,y-a.pivot[1]*k,a.cw*k,a.ch*k);ctx.restore();return true;}
rg4Attack=function(q,R,G,forced){if(q.key!=='voss')return VS41.base.attack.apply(this,arguments);
 if(G.rd21?.fleet||R.ships.some(s=>s!==q&&rbal19Heavy(s))){q.rg4.cd=.6;return;}
 const kind=forced||q.rg4.armed||'turbo',A=rd21Personal(q,R,G,kind==='turbo'?'turbo':'rr26dash');
 Object.assign(A,{_vs41:true,phase:'position',t:0,home:{x:q.x,y:q.y},from:{x:q.x,y:q.y},perch:{x:clamp(q.x,camLeftX()+105,camRightX()-105),y:PLAY.y+65},round:0,cd:0,cycles:0,passes:rd21Rank()>=2?3:2});
 q._rd21Scale=1;q.frSomersault=false;q.evadeT=0;vs41Log('perch-start',{kind:A.kind});return A;
};
rbal19Heavy=function(q){return vs41Active(q)&&q.rg4.act.phase!=='recover'||VS41.base.heavy.apply(this,arguments);};
ra4Gun=function(q){if(q?.key==='voss')return;return VS41.base.gun.apply(this,arguments);};
ra4RamHit=function(q,A){if(q?.key==='voss'&&(A?._vs41||vs41Safe(q)))return;return VS41.base.ram.apply(this,arguments);};
rr26Energy=function(q,G){const o=VS41.base.orb.apply(this,arguments);if(q?.key==='voss'&&o)o._vs41Orb=true;return o;};
function vs41Release(q,G,A){let count=0;for(const side of [-1,1]){const p=vs41Cannon(q,side);if(!p)continue;const a=Math.atan2(A.ty-p.y,A.tx-p.x),o=rr26Energy(q,G,a,false,p.x,p.y);o._vs41Side=side;o.r=13;o.vx=Math.cos(a)*180;o.vy=Math.sin(a)*180;o.life=4.5;
  wm26Emit(q,p.x,p.y,a,'orb','#ff5039',{size:30,life:.11,follow:()=>vs41Active(q)?vs41Cannon(q,side):null});count++;}
 if(count)combatAudio0927(q,'enemyBossCannon',.18);vs41Log('twin-cannon',{count,round:A.round});
}
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(q.key!=='voss'||!A?._vs41)return VS41.base.act.apply(this,arguments);if(!rd21Live(q)){q.rg4.act=null;q._rd21Scale=1;return;}dt=Math.min(.05,dt);A.t+=dt;q.evadeT=0;q.frSomersault=false;q.frCloak=0;
 const smooth=u=>{u=clamp(u,0,1);return u*u*(3-2*u);};
 if(A.phase==='position'){const u=smooth(A.t/.85);q.x=lerp(A.from.x,A.perch.x,u);q.y=lerp(A.from.y,A.perch.y,u);q.rfHeading=Math.PI/2;q._rd21Scale=1;if(A.t>=.85){A.tx=A.target.ref.x;A.ty=A.target.ref.y;A.warm=1.35;vs41Phase(q,A,'charge');combatAudio0927(q,'bossWeaponCharge',.55);}}
 else if(A.phase==='charge'){
  q.x=A.perch.x;q.y=A.perch.y;q.rfHeading=Math.PI/2;if(A.t<A.warm*.42){A.tx=A.target.ref.x;A.ty=A.target.ref.y;}
  combatWarningTick(A,'voss-twin-cannons',Math.min(A.t,A.warm),A.warm);if(A.t>=A.warm){A.cd=0;vs41Phase(q,A,'fire');}
 }else if(A.phase==='fire'){
  q.rfHeading=Math.PI/2;A.cd-=dt;if(A.cd<=0&&A.round<5){A.cd=.30;A.round++;vs41Release(q,G,A);}if(A.t>1.6){A.warm=1.6;vs41Phase(q,A,'turbocharge');combatAudio0927(q,'bossWeaponCharge',.6);}
 }else if(A.phase==='turbocharge'){
  q.rfHeading=Math.PI/2;combatWarningTick(A,'voss-turbo-power',Math.min(A.t,A.warm),A.warm,true);
  if(A.t>=A.warm){A.side=q.x<camLeftX()+viewW()/2?1:-1;A.cycles=0;vs41Phase(q,A,'dash');combatAudio0927(q,'chargeDash',.5);}
 }else if(A.phase==='dash'){
  const u=clamp(A.t/.70,0,1),ease=u*u;q.x=A.from.x;q.y=lerp(A.from.y,VH+110,ease);q.rfHeading=Math.PI/2;q._rd21Scale=lerp(A.scale,1.42,smooth(u));
  if(u>=1)vs41Phase(q,A,'turn-north');
 }else if(A.phase==='turn-north'){
  const u=clamp(A.t/.35,0,1),a=u*Math.PI,r=35;q.x=A.from.x+A.side*r*(1-Math.cos(a));q.y=A.from.y+r*Math.sin(a);q.rfHeading=Math.atan2(Math.cos(a),A.side*Math.sin(a));
  if(u>=1){vs41Phase(q,A,'north');combatAudio0927(q,'jetDash',.5);}
 }else if(A.phase==='north'){
  const u=clamp(A.t/.85,0,1);q.x=A.from.x;q.y=lerp(A.from.y,PLAY.y-115,u);q.rfHeading=-Math.PI/2;q._rd21Scale=lerp(1.42,.72,smooth(u));if(u>=1)vs41Phase(q,A,'turn-south');
 }else if(A.phase==='turn-south'){
  const u=clamp(A.t/.35,0,1),a=u*Math.PI,r=35;q.x=A.from.x-A.side*r*(1-Math.cos(a));q.y=A.from.y-r*Math.sin(a);q.rfHeading=Math.atan2(-Math.cos(a),-A.side*Math.sin(a));
  if(u>=1){A.cycles++;if(A.cycles<A.passes){vs41Phase(q,A,'dash');combatAudio0927(q,'jetDash',.5);}else vs41Phase(q,A,'approach');}
 }else if(A.phase==='approach'){
  const u=smooth(A.t/1.1);q.x=lerp(A.from.x,A.home.x,u);q.y=lerp(A.from.y,A.home.y,u);q.rfHeading=Math.PI/2;q._rd21Scale=lerp(.72,1,u);if(A.t>=1.1)vs41Phase(q,A,'recover');
 }else if(A.phase==='recover'){q.rfHeading=Math.PI/2;q._rd21Scale=1;if(A.t>.9)rd21Finish(q,G,6);}
};
rg4Warning=function(q,A){if(A?._vs41){if(A.phase==='charge')for(const side of [-1,1]){const p=vs41Cannon(q,side);if(!p)continue;rd21Fov(A,p.x,p.y,Math.atan2(A.ty-p.y,A.tx-p.x),24,A.t/A.warm);}return;}return VS41.base.warning.apply(this,arguments);};
fr27RebelDrawShip=function(q){if(q.key!=='voss'||q.dead||rr33Protected()||rg4State()?.rd21?.fleet)return VS41.base.ship.apply(this,arguments);
 const A=q.rg4?.act,active=vs41Active(q),safe=vs41Safe(q),scale=q._rd21Scale||1,k=VS41_ART.unit*scale,f=vs41Frame(q),mods=fr27RebelModules(q),angle=(q.rfHeading??Math.PI/2)-Math.PI/2;
 // The shadow is the exact current authored alpha, at the ground projection.
 const draw=(name,cx=q.x,cy=q.y,z=k,alpha=1)=>{for(const[lo,hi,id]of[[-3,-.17,'left'],[-.17,.17,null],[.17,3,'right']]){
  if(id&&mods.some(m=>m.id===id&&m.hp<=0))continue;ctx.save();ctx.beginPath();const w=90*z/VS41_ART.unit,c=Math.cos(angle),s=Math.sin(angle);
  for(const[i,[x,y]]of[[lo*w,-192*z],[hi*w,-192*z],[hi*w,192*z],[lo*w,192*z]].entries()){const px=cx+x*c-y*s,py=cy+x*s+y*c;i?ctx.lineTo(px,py):ctx.moveTo(px,py);}ctx.closePath();ctx.clip();vs41Blit(name,f,cx,cy,z,alpha);ctx.restore();
 }};
 const height=!safe?0:A.phase==='approach'?1-clamp(A.t/1.1,0,1):A.phase==='dash'&&A.cycles===0?clamp(A.t/.35,0,1):1;
 if(!VS41.foreground)draw('shadow',q.x+12,q.y+lerp(20,65,height),k*lerp(.78,.56,height),lerp(.24,.35,height));
 if(safe&&!VS41.foreground)return true;
 draw(q.flash>0?'hull_hit':'hull');
 if(q.flash<=0){let power=0;if(active&&['charge','turbocharge'].includes(A.phase))power=clamp(A.t/A.warm,0,1);else if(safe)power=.45;
  if(power>0){ctx.save();ctx.globalCompositeOperation='lighter';const step=PXG_STEPS[2+Math.floor((q.t||A.t)*(12+power*22))%4];ctx.globalAlpha*=power*(.4+.6*step);draw('outer');ctx.globalAlpha*=1.3;draw('inner');ctx.restore();}}
 if(active)rg4Warning(q,A);if(q._rd21Volley)ra4LockWarning(q._rd21Volley,'voss');q._vs41Rendered={frame:f,scale:k,safe};
 return true;
};
rg4OrdnanceDraw=function(o,G){if(o._vs41Orb||o.owner?.key==='voss'&&o._rr26Energy){const f=Math.floor((o.t||0)*20)%8,k=38/128;vs41Blit(o.flash>0?'orb_hit':'orb',f,o.x,o.y,k);if(o.flash<=0){ctx.save();ctx.globalCompositeOperation='lighter';vs41Blit('orb_glow',f,o.x,o.y,k,.45+.3*PXG_STEPS[Math.floor((o.t||0)*20)%6]);ctx.restore();}return;}return VS41.base.ord.apply(this,arguments);};
rebelSquadTick=function(b,dt){for(const q of b?._rebels?.ships||[])if(q.key==='voss'&&!q.dead){q.frCast=null;q.cd=999;}
 const r=VS41.base.tick.apply(this,arguments),G=b?._rebels?.gang1004;if(G)for(const o of G.ord)if(o._vs41Orb&&(o.owner.dead||o._vs41Side&&fr27RebelModules(o.owner).some(m=>m.id===(o._vs41Side<0?'left':'right')&&m.hp<=0)))o.dead=true;return r;};
// Ground projection stays in the native boss pass; the elevated aircraft passes
// above players/allies. Both layers use the same live pose, pivot and scale.
drawWorld=function(dt){const r=VS41.base.world.apply(this,arguments),q=boss?._rebels?.ships.find(q=>q.key==='voss');if(state!==GS.PLAY||!vs41Safe(q))return r;
 ctx.save();try{const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);
  ctx.beginPath();ctx.rect(camLeftX(),PLAY.y+18,viewW(),VH-PLAY.y-18);ctx.clip();VS41.foreground=true;fr27RebelDrawShip(q);rg4HealthBars({_rebels:{ships:[q]}});
 }finally{VS41.foreground=false;ctx.restore();}return r;
};
