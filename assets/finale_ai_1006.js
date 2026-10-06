"use strict";
/* Authored motion coverage and difficulty-aware Stage 8 combat.
   Keep real donor controllers, nine saved pools and the original three encounters. */
const F6={events:[],draws:{},base:{rig:fmcRig,warm:r30Warm,donor:gd4Tick,knight:hk5KnightTick,
 start:hk5AttackStart,clear:j3Clear,mimic:j3Mimic,attack:r30Attack,tick:r30AttackTick,dracula:aa5DraculaTick}};
function f6Log(event,data={}){F6.events.push({event,...data});if(F6.events.length>240)F6.events.shift();}
function f6Furious(){return diffKey==='furious'||diffKey==='insanity';}
function f6Hard(){return f6Furious()||diffKey==='hard';}
for(const a of F6_MOTION){XART._src[a.key]=a.path;FMC_ART[a.key]={key:a.key,path:a.path,rects:{pose:[0,0,a.w,a.h]}};}
r30Warm=function(){const r=F6.base.warm.apply(this,arguments);for(const a of F6_MOTION)XART.rdy(a.key);return r;};
function f6Motion(h){if(!h)return null;const s=h.state,t=h.t||0;
 if(h.hammerDestroyed)return s==='storm_rebuild'?14:['hammer_stun','storm_stun','fr_stun','hammer_exposed'].includes(s)&&t<.30?12:13;
 if(s==='curl')return Math.min(2,Math.floor(t/Math.max(.1,HAMMER_BALL_WARN)*3));
 if(s==='ball')return 2;if(s==='uncurl')return t<.4?2:t<.8?1:3;
 if(['giant_idle','giant_windup','giant_rise','giant_warn'].includes(s))return 4;
 if(s==='giant_dive')return 5;if(s==='giant_sweep')return 6;
 if(['giant_recover','giant_knockback'].includes(s))return 7;
 if(['whirl_warn','whirl_turn'].includes(s))return 8;
 if(['whirlwind','spin','fr_twirl'].includes(s))return 8+(Math.floor(t*9)%4);
 if(h.throw||s==='throw')return 15;
 if(['hammer_stun','storm_stun','fr_stun','hammer_exposed'].includes(s))return t<.30?12:13;
 if(s==='storm_rebuild')return 14;return null;
}
function f6MotionScale(h){const s=h.state,t=h.t||0;
 return s==='giant_rise'?lerp(1,.25,clamp(t,0,1)):s==='giant_warn'?.25:
  s==='giant_dive'?lerp(.25,1.65,clamp(t/.52,0,1)):s==='giant_sweep'?1.65:
  s==='giant_knockback'?lerp(h.counterScale||1,1,clamp(t/.65,0,1)):
  s==='giant_recover'?lerp(h.countered?1:1.65,1,clamp(t/.8,0,1)):1;
}
fmcRig=function(b){const J=j3State(b);if(J?.mimic!==8||!hk5Own(b))return F6.base.rig.apply(this,arguments);
 const h=J.gp4Donors?.[8]?.p._hammer,f=f6Motion(h);if(f==null)return F6.base.rig.apply(this,arguments);
 const a=F6_MOTION[f],scale=.76*f6MotionScale(h),w=a.w*scale,hgt=a.h*scale,rot=h.state==='ball'?(h.angle||0):0;
 const v={p:b.parts.find(p=>p.id==='core'),spec:{px:a.px,py:a.py,art:'pose',sheet:a.key,role:'core'},key:a.key,
  ax:b.x,ay:b.y,w,h:hgt,rot,alpha:1,z:1};Object.assign(v,fmcPoint(v,.5,.5));const out=[v];
 const p=b.parts.find(p=>p.id==='hammer');if(p&&!p.destroyed&&!h.throw&&a.head){const q=fmcPoint(v,a.head[0]/a.w,a.head[1]/a.h);
  out.push({p,spec:{px:.5,py:.5,role:'hammerHead',hidden:true},key:a.key,ax:q.x,ay:q.y,x:q.x,y:q.y,w:64*scale/.76,h:55*scale/.76,rot,alpha:1,z:5});}
 F6.draws[a.name]=(F6.draws[a.name]||0)+1;return out;
};
// Select a live co-op participant fairly; snapshots commit once per warning.
function f6Target(b){const choices=[];for(const seat of seatList())withSeat(seat,()=>{if(!player.dead)choices.push({x:player.x,y:player.y,seat});});
 const S=b._r30,n=S.f6Seat||0;S.f6Seat=n+1;return choices[n%Math.max(1,choices.length)]||{x:player.x,y:player.y,seat:0};}
function f6KnightChoice(b){const S=b._r30,hasSword=fmcAlive(b,'sword'),hasShield=fmcAlive(b,'shield'),n=S.hkKnightN||0;
 if(!hasSword&&!hasShield)return 'coreCode';if(!hasSword)return n%2?'shieldCode':'shieldSmite';if(!hasShield)return n%2?'armageddon':'leapSlash';
 const near=Math.hypot(player.x-b.x,player.y-b.y)<180,book=near?['shieldSmite','leapSlash','shieldCode','armageddon']:['shieldCode','armageddon','leapSlash','shieldSmite'];
 let kind=book[n%4];if(kind===S.f6LastKnight)kind=book[(n+1)%4];S.f6LastKnight=kind;return kind;
}
hk5AttackStart=function(b,kind){const r=F6.base.start.apply(this,arguments),K=b._r30.hkKnight,T=f6Target(b);
 K.tx=clamp(T.x,camLeftX()+85,camRightX()-85);K.ty=clamp(T.y,PLAY.y+180,hammerWarningFloorY()-10);K.targetSeat=T.seat;
 K.f6={furious:f6Furious(),bursts:0,followed:false};f6Log('knightPlan',{kind,tx:K.tx,ty:K.ty,seat:T.seat,diff:diffKey});return r;};
function f6KnightLanes(b,K){const m=fmcRig(b).find(v=>v.p.id==='shield')||{x:b.x,y:b.y+45},a=Math.atan2(K.ty-m.y,K.tx-m.x);
 const offsets=K.f6.bursts%2===0?[-.28,0,.28]:[-.42,-.14,.14,.42];
 return offsets.map(off=>({x:m.x,y:m.y,ex:m.x+Math.cos(a+off)*420,ey:m.y+Math.sin(a+off)*420,width:22,a:a+off}));}
hk5KnightTick=function(b,D,dt){const S=b._r30;let K=S.hkKnight;
 if(!K){S.hkKnightCd=(S.hkKnightCd??1.2)-dt;if(S.hkKnightCd>0)return;const kind=f6KnightChoice(b);S.hkKnightN=(S.hkKnightN||0)+1;hk5AttackStart(b,kind);K=S.hkKnight;}
 K.f6??={furious:f6Furious(),bursts:0,followed:false};
 // Every Furious code burst has its OWN warning; aims stop tracking when chosen.
 if(K.f6.furious&&['shieldCode','coreCode'].includes(K.kind)&&['tell','active'].includes(K.phase)){
  if(K.phase==='tell'){K.t+=dt;K.f6.lanes=f6KnightLanes(b,K);combatWarningTick(b,'f6-knight-code-'+S.hkKnightN+'-'+K.f6.bursts,K.t,1.15);
   if(K.t>=1.15){K.f6.bursts++;const tool=fmcRig(b).find(v=>v.p.id==='shield');
    // A broken shield cannot finish a charged weapon cast.
    if(K.kind==='shieldCode'&&!tool){hk5Phase(K,'recover');return;}
    for(const L of K.f6.lanes){const q=eShootT(L.x,L.y,L.a,4.2,'eglaser',{w:22,h:24});if(q){q._hkCodeFire=true;q._hkOwner=b;q.t=0;q.w=q.h=22;(S.hkShots??=[]).push(q);}}
    r30Sound('enemyBossCannon');hk5Phase(K,'active');f6Log('knightCodeBurst',{n:K.f6.bursts,target:[K.tx,K.ty]});}
  }else{K.t+=dt;if(K.t>=.60){if(K.f6.bursts>=3)hk5Phase(K,'recover');else hk5Phase(K,'tell');}}
  D.p.x=b.x;D.p.y=b.y;return;
 }
 // A second independently warned close strike: never retarget the existing leap.
 if(K.f6.furious&&K.kind==='leapSlash'&&K.phase==='recover'&&!K.f6.followed){
  K.f6.followed=true;const T=f6Target(b);K.tx=clamp(T.x,camLeftX()+85,camRightX()-85);K.ty=clamp(T.y,PLAY.y+180,hammerWarningFloorY()-10);
  K.kind=fmcAlive(b,'shield')?'shieldSmite':fmcAlive(b,'sword')?'leapSlash':'coreCode';K.ox=b.x;K.oy=b.y;hk5Phase(K,'tell');
  f6Log('knightFollowup',{kind:K.kind,tx:K.tx,ty:K.ty});return;
 }
 // Destroyed equipment interrupts the move immediately, not one cycle later.
 if(K.phase!=='recover'&&((K.kind.startsWith('shield')&&!fmcAlive(b,'shield'))||(['leapSlash','armageddon'].includes(K.kind)&&!fmcAlive(b,'sword')))){
  K.rows=[];hk5Phase(K,'recover');f6Log('knightDisarmed',{kind:K.kind});}
 const was=K.phase;F6.base.knight.call(this,b,D,dt);
 if(!S.hkKnight&&was==='recover')S.hkKnightCd=f6Furious()?.78:f6Hard()?.95:1.35;
};
function f6Ports(b){return aa5DonorPorts(b).filter(v=>v.module!=='core'&&fmcAlive(b,v.module));}
const F6_PATTERNS={1:{name:'SONIC CROSSGUN',kind:'code',offsets:[-.28,-.14,.14,.28]},2:{name:'MAGMA RELAY',kind:'fire',offsets:[-.16,.16]},
 3:{name:'ICE GATES',kind:'ice',offsets:[-.42,-.28,.28,.42]},4:{name:'STORM RAKE',kind:'code',offsets:[-.30,0,.30]},
 6:{name:'MISSILE PINCER',kind:'missile',offsets:[-.22,.22]},7:{name:'TOXIC CLAW RELAY',kind:'toxic',offsets:[-.36,-.18,.18,.36]}};
function f6Busy(D){const p=D.p;return !!(p._l23Beam||p._whv?.beam||p._whv?.beam2||p._whv?.ace?.dash||p._whv?.ace?.desp&&p._whv.ace.desp.st!=='done'||p._fz?.tells?.length&&p._fz.attack!=='cannon'||p._fz?.beams?.length||/sonic|rush|sweep/.test(p._ovState||''));}
function f6SalvoLanes(b,D,V){const ports=f6Ports(b);const P=F6_PATTERNS[D.i],shift=D.i===2?(V.n%2?-.10:.10):D.i===4?(V.n%2?-.12:.12):0;
 const selected=D.i===7&&ports.length>1?[ports[V.n%ports.length]]:ports;
 return selected.flatMap(m=>P.offsets.map(off=>{const a=Math.atan2(V.ty-m.y,V.tx-m.x)+off+shift;
  return{...m,a,ex:m.x+Math.cos(a)*450,ey:m.y+Math.sin(a)*450,width:P.kind==='missile'?20:14};}));}
gd4Tick=function(b,dt){const J=j3State(b);if(!J||!(J.mimic>0)||[5,8].includes(J.mimic))return F6.base.donor.apply(this,arguments);
 const D=gd4Create(b,J.mimic);dt=Math.min(.05,Math.max(0,dt));D.aa5Visit=(D.aa5Visit||0)+dt;
 if(f6Furious())D.age=Math.min(D.age,31.7);
 // No blanket speed-up: native controllers retain their readable animation clock.
 D.alien=Math.max(D.alien,2);const r=AA5_DONOR.call(this,b,dt);if(b._r30.mode!=='fight')return r;
 if(f6Furious()&&D.aa5Visit>=40){D.aa5Visit=0;j3Morph(b,'home');return r;}
 D.aa5Cd=(D.aa5Cd??6)-dt;let V=D.aa5Salvo;
 if(V&&f6Busy(D)){D.aa5Salvo=null;D.aa5Cd=3;f6Log('salvoDeferred',{source:D.i});return r;}
 if(!V&&D.aa5Cd<=0&&!f6Busy(D)&&f6Ports(b).length){const T=f6Target(b);
  V=D.aa5Salvo={f6:true,t:0,tell:f6Furious()?1.15:f6Hard()?1.30:1.5,n:0,count:f6Furious()?3:f6Hard()?2:1,tx:T.x,ty:T.y,lanes:[],phase:'tell'};
  f6Log('donorPlan',{source:D.i,pattern:F6_PATTERNS[D.i].name,count:V.count,diff:diffKey,tx:V.tx,ty:V.ty});r30Sound('bossWeaponCharge');}
 if(!V)return r;V.t+=dt;
 if(V.phase==='tell'){V.lanes=f6SalvoLanes(b,D,V);combatWarningTick(b,'f6-donor-'+D.i+'-'+V.n,V.t,V.tell);
  if(V.t>=V.tell){const P=F6_PATTERNS[D.i],speed=f6Furious()?4.1:f6Hard()?3.7:3.3;
   for(const L of V.lanes){if(!fmcAlive(b,L.module))continue;const q=f1003bShot(b,L.x,L.y,L.a,P.kind==='missile'?speed*.8:speed,P.kind,P.kind==='fire'||P.kind==='ice');
    if(q){q._f6Owner=b;q._fmcModule=L.module;if(P.kind==='ice'){q.hp=4;q._shootable=true;q._energyOrdnance=true;q.spd=speed;}}}
   V.n++;V.phase='cool';V.t=V.tell;V.coolT=0;r30Sound('enemyBossCannon');f6Log('donorBurst',{source:D.i,n:V.n,count:V.lanes.length});}
 }else if((V.coolT=(V.coolT||0)+dt)>=.55){if(V.n>=V.count){D.aa5Salvo=null;D.aa5Cd=f6Furious()?8:f6Hard()?10:12;}else{V.phase='tell';V.t=0;r30Sound('bossWeaponCharge');}}
 return r;
};
// Retain the established five-signature colossus book; Furious adds one
// separately warned claw echo with a committed target during each signature.
aa5DraculaTick=function(b,dt){const prior=b._r30.attack,r=F6.base.dracula.apply(this,arguments),P=b._r30.attack;
 if(P&&P!==prior){P.f6=true;const T=f6Target(b);P.tx=clamp(T.x,camLeftX()+65,camRightX()-65);P.ty=clamp(T.y,PLAY.y+240,hammerWarningFloorY());
  if(f6Furious()){P.active+=.45;P.tell=1.15;f6Log('colossusPlan',{type:P.type,diff:diffKey});}}
 if(P&&f6Furious()&&P.t>=P.tell+.45&& !P.f6Echo){const T=f6Target(b);P.f6Echo={t:0,tell:1.15,tx:T.x,ty:T.y,fired:false,lanes:[]};}
 const E=P?.f6Echo;if(E&&!E.fired){E.t+=dt;E.lanes=r30Parts(b).filter(v=>v.p.id!=='core').map(cf4Claw).map(v=>({x:v.x,y:v.y,ex:E.tx,ey:E.ty,width:35}));
  combatWarningTick(b,'f6-colossus-echo-'+b._r30.seq,E.t,E.tell);
  if(E.t>=E.tell){E.fired=true;for(const L of E.lanes)for(const off of [-.20,.20]){const q=f1003bShot(b,L.x,L.y,Math.atan2(E.ty-L.y,E.tx-L.x)+off,4.1,'code',true);if(q)q._f6Owner=b;}
   r30Sound('combatAlien0927');f6Log('colossusEcho',{type:P.type,count:E.lanes.length});}}
 return r;
};
// Furious host/ghost moves retain the authored telegraphs and add two beats to
// their attack book, while normal still teaches each physical strike in order.
r30Attack=function(b){const J=j3State(b),S=b?._r30,oldSeq=S?.seq;let picked=false;
 if(J&&J.encounter<2&&f6Furious()){
  const order=J.encounter===1?[0,6,1,4,2,7,3,5,6,4]:[0,4,1,5,2,3,4,5];
  S.seq=order[(S.f6OuterSeq||0)%order.length];S.f6OuterSeq=(S.f6OuterSeq||0)+1;picked=true;
 }const r=F6.base.attack.apply(this,arguments),P=S?.attack;if(picked)S.seq=oldSeq+1;
 if(P&&J?.encounter<2){P.f6=true;if(f6Furious()){P.tell=Math.max(1.05,P.tell);P.active+=.35;}
  f6Log('outerPlan',{encounter:J.encounter,type:P.type,diff:diffKey});}return r;};
// Fur side chains are individually warned. They cannot skip stun/restore or
// the original source emergency reserve and never add a fourth outer fight.
const F6_HAMMER_STATE=hammerState;
hammerState=function(p,state){const h=p?._hammer,own=j3State(p?._gp4Host)?.mimic===8,prev=h?.state;
 if(own&&f6Furious()&&prev==='hkSideHit'&&state==='hammer'&&!h.gp4Emergency){h.f6Sides=(h.f6Sides||0)+1;
  if(h.f6Sides<2){h.hkSide=-h.hkSide;state='hkSideTell';}else{h.f6Sides=0;h.hkSideCd=4.8;}}
 return F6_HAMMER_STATE.call(this,p,state);
};
j3Mimic=function(b,i){const r=F6.base.mimic.apply(this,arguments),D=j3State(b)?.gp4Donors?.[i];if(D){D.aa5Salvo=null;D.aa5Cd=6;D.aa5Visit=0;}return r;};
j3Clear=function(b){const J=j3State(b);for(const D of J?.gp4Donors||[])if(D){D.aa5Salvo=null;D.aa5Cd=6;if(D.p?._hammer)D.p._hammer.f6Sides=0;}
 eBullets=eBullets.filter(q=>q._f6Owner!==b);return F6.base.clear.apply(this,arguments);};
const F6_DRAW=r30DrawBoss;
r30DrawBoss=function(b){const r=F6_DRAW.apply(this,arguments),J=j3State(b),D=J?.gp4Donors?.[J.mimic],V=D?.aa5Salvo,K=b?._r30?.hkKnight;
 if(b?._r30?.mode!=='fight')return r;
 if(V?.f6&&V.phase==='cool')return r;
 const E=b?._r30?.attack?.f6Echo;if(E&&!E.fired)for(const L of E.lanes)combatWarningDraw(b,{...L,progress:clamp(E.t/E.tell,0,1),fieldOnly:true});
 if(J?.mimic===5&&K?.f6?.furious&&K.phase==='tell'&&K.f6.lanes)for(const L of K.f6.lanes)combatWarningDraw(b,{...L,progress:clamp(K.t/1.15,0,1),fieldOnly:true});
 return r;};
