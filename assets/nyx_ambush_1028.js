"use strict";
// Nyx: cloaked mine insertion, twin turret lasers, visible escape and return.
const NX37={attack:rg4Attack,act:rg4AttackTick,tick:rebelSquadTick,ship:fr27RebelDrawShip,draw:rebelSquadDraw,round:rg4Round,gun:ra4Gun,projectile:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,impact:pw5Impact,events:[]};
XART._src.nx37_lasers='assets/game/levels/stage_06/boss/nyx_ambush_1028/lasers.png';
for(const k of ['nx37_lasers','ngm_shock_7',...Array.from({length:4},(_,i)=>'ndr_furymine_idle_'+i)])XART.rdy(k);
function nx37State(G){return G.nx37||(G.nx37={mines:[],waves:[]});}
function nx37Socket(q,side){const a=q.rfHeading??Math.PI/2;return{x:q.x+Math.cos(a)*21-Math.sin(a)*side*18,y:q.y+Math.sin(a)*21+Math.cos(a)*side*18};}
function nx37Move(q,A,end,duration){const u=clamp(A.t/duration,0,1),v=u*u*(3-2*u),dx=end.x-A.from.x,dy=end.y-A.from.y;q.x=lerp(A.from.x,end.x,v);q.y=lerp(A.from.y,end.y,v);q.rfHeading=Math.atan2(dy,dx);return u===1;}
function nx37Phase(q,A,name){A.phase=name;A.t=0;A.from={x:q.x,y:q.y};}
rg4Round=function(q,a,speed,kind,extra={}){if((extra.owner||q).key==='nyx')return{dead:true,x:q.x,y:q.y};return NX37.round.apply(this,arguments);};
ra4Gun=function(q){if(q.key==='nyx')return;return NX37.gun.apply(this,arguments);};
rg4Attack=function(q,R,G){if(q.key!=='nyx')return NX37.attack.apply(this,arguments);
 if(G.rd21?.fleet||R.ships.some(s=>s!==q&&rbal19Heavy(s))){q.rg4.cd=.6;return;}
 const target=ra4Target(q,q.rg4.serial++),p=target.ref;
 q.rg4.armed=null;q.rg4._rbal19Gun=null;q.evadeT=0;q._rd21Cloak=true;q._rd21Visible=999;
 const A=q.rg4.act={kind:'nx37ambush',_rd21:true,phase:'approach',t:0,target,from:{x:q.x,y:q.y},home:{x:camLeftX()+viewW()*.28,y:PLAY.y+105},near:{x:clamp(p.x+(p.x>camLeftX()+viewW()/2?-65:65),camLeftX()+55,camRightX()-55),y:clamp(p.y-90,PLAY.y+160,VH-110)},cd:0,warm:1.8};
 NX37.events.push({event:'approach',target:target.key});return A;
};
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(A?.kind!=='nx37ambush')return NX37.act.apply(this,arguments);
 if(!rd21Live(q)){q.rg4.act=null;return;}A.t+=Math.min(dt,.05);q.evadeT=0;q._rd21Visible=999;q._rd21Scale=1;
 if(A.phase==='approach'){q._rd21Cloak=true;if(nx37Move(q,A,A.near,1.8)){q._rd21Cloak=false;q.frCloak=0;nx37Phase(q,A,'reveal');av3Sound('teleport_in',.65,.3);}}
 else if(A.phase==='reveal'){q.x=A.from.x;q.y=A.from.y;q.rfHeading=Math.PI/2;if(A.t>1.05){nx37State(G).mines.push({x:q.x,y:q.y+35,t:0,phase:'arming',owner:q,beep:0});NX37.events.push({event:'mine-deployed',x:q.x,y:q.y+35});nx37Phase(q,A,'retreat');}}
 else if(A.phase==='retreat'){if(nx37Move(q,A,A.home,1.8)){q.rfHeading=Math.PI/2;nx37Phase(q,A,'charge');A.a=Math.atan2(A.target.ref.y-q.y,A.target.ref.x-q.x);}}
 else if(A.phase==='charge'){const p=clamp(A.t/A.warm,0,1);q.x=A.from.x+(p>.48&&p<.8?Math.sin(A.t*65)*2.5:0);q.y=A.from.y;
  if(p<.72)A.a=Math.atan2(A.target.ref.y-q.y,A.target.ref.x-q.x);q.rfHeading=clamp(A.a,.95,2.19);combatWarningTick(A,'nyx-twin-lasers',A.t,A.warm);
  if(p===1){nx37Phase(q,A,'fire');A.cd=0;}}
 else if(A.phase==='fire'){q.x=A.from.x;q.y=A.from.y;const goal=Math.atan2(A.target.ref.y-q.y,A.target.ref.x-q.x),delta=((goal-A.a+Math.PI*3)%TAU)-Math.PI;A.a=clamp(A.a+clamp(delta,-dt*.42,dt*.42),.95,2.19);q.rfHeading=A.a;A.cd-=dt;
  if(A.cd<=0){for(const side of [-1,1]){const p=nx37Socket(q,side),z=eShootT(p.x,p.y,A.a,4.2,'s6orb',{w:9,h:24,silent:true,noMuzzle:true});Object.assign(z,{_nx37Laser:true,owner:q,_boss:true});wm26Emit(q,p.x,p.y,A.a,'orb','#d6b4ff',{size:18,life:.1});}av3Sound('laser_release',.6,.15);A.cd=.24;}
  if(A.t>2.6){nx37Phase(q,A,'exit');A.edge={x:q.x<camLeftX()+viewW()/2?camLeftX()-100:camRightX()+100,y:PLAY.y-110};}}
 else if(A.phase==='exit'){if(nx37Move(q,A,A.edge,1.4))nx37Phase(q,A,'return');}
 else if(A.phase==='return'){if(nx37Move(q,A,A.home,1.6)){q.rfHeading=Math.PI/2;nx37Phase(q,A,'cloak');}}
 else if(A.phase==='cloak'){q.x=A.home.x;q.y=A.home.y;q._rd21Cloak=true;q.frCloak=10;if(A.t>1.05){q.rg4.act=null;q.rg4.cd=4;q.rfHeading=Math.PI/2;NX37.events.push({event:'recloaked'});}}
};
function nx37Hazards(G,dt){const S=nx37State(G);for(const m of S.mines){if(m.owner.dead){m.dead=true;continue;}m.t+=dt;
 if(m.phase==='arming'&&m.t>=1.2){m.phase='armed';m.t=0;}
 if(m.phase==='armed'&&ra4Targets().some(t=>Math.hypot(t.ref.x-m.x,t.ref.y-m.y)<115)){m.phase='fuse';m.t=0;}
 if(m.phase==='fuse'){m.beep-=dt;if(m.beep<=0){Audio.SFX.retinaLockBeep?.();m.beep=lerp(.25,.08,clamp(m.t/.9,0,1));}if(m.t>=.9){m.dead=true;S.waves.push({x:m.x,y:m.y,t:0,r:0,max:viewW()*.6,owner:m.owner,hit:new Set()});explode(m.x,m.y,72,'purple');Audio.SFX.expBig?.();NX37.events.push({event:'mine-detonated'});}}
 if(m.phase==='armed'&&m.t>10)m.dead=true;}
 S.mines=S.mines.filter(m=>!m.dead);for(const w of S.waves){if(w.owner.dead){w.dead=true;continue;}const old=w.r;w.t+=dt;w.r=Math.min(w.max,w.t*260);
 for(const target of ra4Targets()){const p=target.ref,d=Math.hypot(p.x-w.x,p.y-w.y);if(w.hit.has(p)||d<old-14||d>w.r+14)continue;w.hit.add(p);
 if(target.seat){withSeat(target.seat,()=>{if(!player.roll&&!player.somer)playerHit('Nyx proximity blast');});}
 else if(p.canBeHit&&!p.hurtT){p.hp=Math.max(0,p.hp-1);p.hurtT=1;explode(p.x,p.y,36,'purple');if(!p.hp){p.phase='leave';p.t=0;}}}
 if(w.r>=w.max)w.dead=true;}S.waves=S.waves.filter(w=>!w.dead);}
rebelSquadTick=function(b,dt){const r=NX37.tick.apply(this,arguments),G=b?._rebels?.gang1004;if(!G||b.dead)return r;nx37Hazards(G,dt);
 const q=b._rebels.ships.find(q=>q.key==='nyx');if(q&&rd21Live(q)&&b._rebels.frIntro?.done&&!G.scene&&!G.rd21?.fleet&&!q.rg4.act&&q.rg4.cd<=0)rg4Attack(q,b._rebels,G);return r;};
const nx37Warning=rg4Warning;
rg4Warning=function(q,A){if(A?.kind==='nx37ambush'){if(A.phase==='charge')for(const side of [-1,1]){const p=nx37Socket(q,side);rd21Fov(A,p.x,p.y,A.a,18,A.t/A.warm);}return;}return nx37Warning.apply(this,arguments);};
fr27RebelDrawShip=function(q){if(q.key!=='nyx'||q.dead||rr33Protected()||rg4State()?.rd21?.fleet)return NX37.ship.apply(this,arguments);air13DrawRebel(q);const A=q.rg4?.act;if(A)rg4Warning(q,A);};
enemyOrdnanceCanIntercept=function(p){return p?._nx37Laser?false:NX37.intercept.apply(this,arguments);};
pw5Impact=function(p){return p?._nx37Laser?null:NX37.impact.apply(this,arguments);};
drawCombatFinalProjectile=function(p){if(!p._nx37Laser)return NX37.projectile.apply(this,arguments);if(!XART.rdy('nx37_lasers'))return true;const f=Math.round(((Math.atan2(p.vy,p.vx)-Math.PI/2+TAU)%TAU)/TAU*32)%32;ctx.drawImage(xartPalette('nx37_lasers','#d6b4ff'),f%8*64,Math.floor(f/8)*64,64,64,p.x-32,p.y-32,64,64);return true;};
rebelSquadDraw=function(b){const r=NX37.draw.apply(this,arguments),G=b?._rebels?.gang1004;if(!G)return r;for(const m of G.nx37?.mines||[]){const key='ndr_furymine_idle_'+Math.floor(m.t*(m.phase==='fuse'?24:8))%4;rr26Effect(key,m.x,m.y,36,1,m.phase==='fuse'?'#ff6699':'#d6b4ff');}
 for(const w of G.nx37?.waves||[])rr26Effect('ngm_shock_7',w.x,w.y,w.r*2,1,'#d6b4ff');return r;};
