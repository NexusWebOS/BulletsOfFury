"use strict";
/* Eight identities, eight finite lives. Geometry is shared by art, warnings,
   damage and Retina. The existing portal/reunion owns the one final reward. */
for(const a of Object.values(FINALE1003B_ART))XART._src[a.key]=a.path;
const F1003B_BASE={form:r30Form,tick:r30Tick,attack:r30Attack,attackTick:r30AttackTick,
 pose:r30Pose,parts:r30Parts,draw:r30DrawBoss,hit:modularHit,clear:r30Clear,
 break:r30Break,visible:bossHealthVisible,bar:drawHealthBarV2,warm:r30Warm,
 targets:retinaBossTargets,projectile:drawCombatFinalProjectile,locks:_lockTargets};
const F1003B_FORMS=[
 {id:'host',name:'THE ORBITAL HOST',color:'#ff475c',hp:.8,w:270,h:246,book:['talons','gravity','code']},
 {id:'chopper',name:'THE HIVE HELICOPTER',color:'#ffae3a',hp:.9,w:250,h:258,book:['rotorMG','bombing','missiles','gravity']},
 {id:'furnace',name:'THE ALIEN FURNACE',color:'#ffe64a',hp:1,w:280,h:270,book:['magma','eruptions','furnaceBeam','orbit']},
 {id:'cryo',name:'THE CRYO HIVE',color:'#52e4ff',hp:1,w:285,h:260,book:['iceMG','iceLance','iceOrbit','gravity']},
 {id:'storm',name:'THE STORM ORGANISM',color:'#7494ff',hp:1,w:270,h:270,book:['missiles','lightning','ram','code']},
 {id:'knight',name:'THE NULL KNIGHT',color:'#c575ff',hp:1.2,w:210,h:242,book:['knight','knight','orbit']},
 {id:'harrier',name:'THE VOID HARRIER',color:'#ff72ce',hp:1.1,w:330,h:260,book:['turbines','missiles','carrierLance','gravity']},
 {id:'warden',name:'THE LAST WARDEN',color:'#b0ed45',hp:1.25,w:300,h:270,book:['wardenMG','stomp','scissor','gravity','code']}
];
function f1003bDef(b){return F1003B_FORMS[b._r30.form];}
function f1003bLog(b,event,data={}){const h=b._r30.history;h.push({event,form:b._r30.form,...data});if(h.length>480)h.splice(0,h.length-480);}
r30Warm=function(){F1003B_BASE.warm();for(const a of Object.values(FINALE1003B_ART))XART.rdy(a.key);bossBarWarm(8);
 if(typeof Snd!=='undefined'&&Snd.prepare)Snd.prepare('enemyMachineGunHeavy');};
r30Form=function(b,n){
 const S=b._r30;S.finale1003b=true;n=clamp(n|0,0,7);const D=F1003B_FORMS[n];
 const base={easy:480,normal:820,hard:1100,furious:1420,insanity:1690}[diffKey]||820;
 S.base=base;S.form=n;S.seq=0;S.attack=null;S.cd=1.1;S.shape=D.id;S.pose=D.id;
 S.shield=0;S.shieldMax=1;S.wallAge1003=0;S.ghostHidden=false;S.returning=null;S.nextBurst=0;S.orbitals=[];
 S.pools=F1003B_FORMS.map(d=>Math.ceil(base*d.hp));
 b.hp=b.maxhp=b._vPhaseHp=S.pools[n];b._vForm=n;b.w=D.w;b.h=D.h;b.x=worldWidth()/2;b.ty=225;b.y=b.ty;
 b.parts=[{id:'core',rc:'central_core',dmg:true,hp:b.hp,maxhp:b.hp,destroyed:false,flash:0}];
 if(n===0)for(const id of ['left','right'])b.parts.push({id,rc:id+'_system',dmg:true,hp:Math.ceil(b.hp*.14),maxhp:Math.ceil(b.hp*.14),destroyed:false,flash:0});
 b.modular=true;b._v24={shield:0,shieldMax:1,pattern:null,foes:[],shards:[],muzzles:[],seq:0};
 b.name=D.name;b.dead=false;b._morphT=null;b._symEntry=null;b._lastPart=null;b._noHit=false;
 f1003bLog(b,'form',{id:D.id,hp:b.hp});
};
r30Clear=function(b){
 const r=F1003B_BASE.clear.apply(this,arguments);
 if(b?._r30?.finale1003b){b._r30.orbitals=[];for(const q of groundTargetingFx)if(q.owner===b)q.dead=true;
  for(const e of enemies)if(e._finaleOwner1003b===b)e.dead=true;}
 return r;
};
r30Break=function(b){
 if(!b?._r30?.finale1003b)return F1003B_BASE.break.apply(this,arguments);
 const S=b._r30;if(S.mode!=='fight')return;
 S.mode=S.form===7?'finalFall':'morph1003b';S.t=0;S.origin={x:b.x,y:b.y};S.attack=null;S.shield=0;b.enter=true;b.hp=0;
 f1003bLog(b,'shellBroken');r30Clear(b);r30FX(b,b.x,b.y,260,'morph');r30Sound('expBig');r30Sound('bossPhase');
};
modularHit=function(dmg){
 const b=boss,S=b?._r30;if(!S?.finale1003b||S.shield>0)return F1003B_BASE.hit.apply(this,arguments);
 if(!r30Live(b)||!Number.isFinite(dmg)||dmg<=0)return;
 const p=b.parts.includes(b._lastPart)&&!b._lastPart.destroyed?b._lastPart:b.parts[0];
 const dealt=Math.min(b.hp,dmg);b.hp-=dealt;p.flash=.12;markHit(b,.12);stageStats.dmgDealt+=dealt;
 if(p.id!=='core'){
  p.hp=Math.max(0,p.hp-dmg);if(!p.hp){const v=r30Parts(b).find(v=>v.p===p);p.destroyed=true;
   if(S.attack?.lanes)S.attack.lanes=S.attack.lanes.filter(q=>q.module!==p.id);
   S81003.beams=S81003.beams.filter(q=>q.owner!==b||q.module!==p.id);
   r30FX(b,v?.x||b.x,v?.y||b.y,95);r30Sound('combatModule0927');f1003bLog(b,'moduleBreak',{part:p.id});}
 }
 b.parts[0].hp=b.hp;if(b.hp<=0)r30Break(b);
};
function f1003bCell(id,frame,x,y,w,h,alpha=1){
 const a=FINALE1003B_ART[id];if(!a||!XART.rdy(a.key))return false;
 const f=clamp(frame|0,0,3);ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),(f%2)*a.cw,Math.floor(f/2)*a.ch,a.cw,a.ch,x-w/2,y-h/2,w,h);ctx.restore();return true;
}
r30Pose=function(b){
 if(!b?._r30?.finale1003b)return F1003B_BASE.pose.apply(this,arguments);
 const S=b._r30,P=S.attack;if(P?.k1003)return s81003KnightPose(b);
 let x=b.x,y=b.y,scale=1,alpha=1;
 if(P&&['talons','ram','stomp'].includes(P.type)&&P.t>=P.tell){
  const u=clamp((P.t-P.tell)/P.active,0,1),k=u<.45?Math.sin(u/.45*Math.PI/2):u<.60?1:Math.cos((u-.60)/.4*Math.PI/2);
  x=lerp(P.fromX,P.tx,k);y=lerp(P.fromY,P.ty-(P.type==='talons'?100:P.type==='stomp'?65:20),k);
  if(P.type==='stomp'){y-=Math.sin(Math.min(1,u/.48)*Math.PI)*120;scale=1+.22*Math.sin(Math.min(1,u/.48)*Math.PI);}
 }
 return{x,y,scale,alpha,angle:0,shape:f1003bDef(b).id};
};
r30Parts=function(b){
 if(!b?._r30?.finale1003b)return F1003B_BASE.parts.apply(this,arguments);
 const S=b._r30,Q=r30Pose(b),D=f1003bDef(b),P=S.attack;
 if(S.form!==0)return[{p:b.parts[0],x:Q.x,y:Q.y,w:D.w*(Q.scale||1)*.85,h:D.h*(Q.scale||1)*.9,rot:0,key:D.id,alpha:Q.alpha}];
 const out=[{p:b.parts[0],x:Q.x,y:Q.y,w:174,h:190,rot:0,key:'possessed_body',alpha:1}];
 for(const p of b.parts.slice(1))if(!p.destroyed){
  const side=p.id==='left'?-1:1,u=P?.type==='talons'?clamp((P.t-P.tell)/P.active,0,1):0;
  const rot=side*(.08+Math.sin(S.clock*1.6)*.04+(u>0?Math.sin(u*Math.PI)*.95:0)),h=198;
  const x=Q.x+side*78-Math.sin(rot)*h*.4,y=Q.y-43+Math.cos(rot)*h*.4;
  out.push({p,x,y,w:80,h,rot,key:'possessed_arm'+(side<0?'L':'R'),alpha:1});
 }return out;
};
retinaBossTargets=function(b){
 if(!b?._r30?.finale1003b)return F1003B_BASE.targets.apply(this,arguments);
 if(!r30Live(b)||r30Pose(b).alpha<.25)return [];
 if(b._r30.shield>0)return F1003B_BASE.targets.apply(this,arguments);
 return r30Parts(b).map(v=>retinaDynamicPiece(b,'finale-'+b._r30.form+'-'+v.p.id,'alien module',()=>{
  const q=r30Parts(b).find(q=>q.p===v.p);return{x:q?.x??v.x,y:q?.y??v.y,hp:q&&!v.p.destroyed?v.p.hp:0,dead:!r30Live(b)||!q||v.p.destroyed};
 },dmg=>{b._lastPart=v.p;hitBoss(dmg);},v.w*.8,v.h*.8));
};
function f1003bShot(b,x,y,a,speed,kind='code',large=false){
 if(eBullets.filter(q=>q._finale1003b).length>=110)return;
 const q=r30Shot(b,kind==='missile'?'bomb':'bolt',x,y,a,speed);q._finale1003b=kind;
 if(['fire','ice','toxic'].includes(kind)){delete q._r30Shot;q._er26Art=kind==='ice'?'ice':'fire';q._er26Large=large;q._er26Draw=large?33:21;q.w=q.h=large?20:11;}
 if(kind==='fire'&&large){q.hp=5;q._shootable=true;q._energyOrdnance=true;q.spd=speed;}
 if(kind==='missile'){q.hp=4;q._shootable=true;q.spd=speed;q._er26Source='tb28';q._r30Fuse=2.5;q._finaleTurn=.55;}
 return q;
}
function f1003bMuzzles(b){
 const D=f1003bDef(b);
 // Measured front-facing emitter centers in the generated equal-cell plates.
 const ports={chopper:[.29,.26],furnace:[.34,.12],cryo:[.22,.31],storm:[.17,.40],harrier:[.27,.18],warden:[.15,.16]};
 if(D.id==='host')return r30Parts(b).filter(v=>v.p.id!=='core').map(v=>({x:v.x+Math.sin(v.rot)*v.h*.19,y:v.y-Math.cos(v.rot)*v.h*.19,side:v.p.id==='left'?-1:1,module:v.p.id}));
 const p=ports[D.id]||[.25,.26];return[-1,1].map(side=>({x:b.x+side*D.w*p[0],y:b.y+D.h*p[1],side}));
}
_lockTargets=function(){const list=F1003B_BASE.locks();if(run.stage===8)for(const q of eBullets)if(q._finale1003b==='missile'&&!q.dead)list.push(fb1002MissileTarget(q));return list;};
function f1003bTargets(b,P,kind='lava',count=3){
 for(let i=0;i<count;i++){
  const a=i*TAU/count+P.seq*.9,r=count>1?64:0;
  groundTargetingSpawn({owner:b,kind,x:clamp(P.tx+Math.cos(a)*r,camLeftX()+32,camRightX()-32),y:clamp(P.ty+Math.sin(a)*r,190,VH-52),warn:P.tell,active:.5,radius:kind==='quake'?33:26,size:kind==='quake'?88:76,track:false,lane:false,shake:3});
 }
}
r30Attack=function(b){
 if(!b?._r30?.finale1003b)return F1003B_BASE.attack.apply(this,arguments);
 const S=b._r30,D=f1003bDef(b),n=r30Difficulty(),type=D.book[S.seq++%D.book.length];
 const P=S.attack={type,t:0,tell:diffKey==='easy'?1.45:[1.18,1.02,.88,.82][n],active:2.25,next:0,seq:S.seq,
  tx:clamp(player.x,camLeftX()+52,camRightX()-52),ty:clamp(player.y,240,VH-70),fromX:b.x,fromY:b.y,lanes:[],fired:0};
 f1003bLog(b,'attack',{type});r30Sound('bossWeaponCharge');combatWarningTick(b,'finale-'+S.form+'-'+S.seq,0,P.tell,true);
 if(type==='knight'){s81003KnightStart(b);P.combo=S.seq%2;P.kIndex=0;
  P.kSteps=P.combo?['guard','jumpTell','jump','land','followTell','sweep','slashRecover','out','in','slashTell','slash','recover','out','in']:
   ['guard','slashTell','slash','slashRecover','jumpTell','jump','land','followTell','sweep','slashRecover','jumpTell','jump','land','recover','out','in'];
  s81003KnightEnter(b,P.kSteps[0]);return;
 }
 if(['code','iceLance','furnaceBeam','lightning','carrierLance','scissor'].includes(type)){
  P.active=.8;P.tell+=.35;const ports=type==='lightning'?[{x:b.x,y:b.y+D.h*.43,side:0}]:f1003bMuzzles(b);
  P.lanes=ports.map(m=>({...s81003Lane(m.x,m.y,P.tx+m.side*45,P.ty,type==='lightning'?22:14),tx:P.tx+m.side*45,ty:P.ty,module:m.module}));
 }
 if(['talons','ram','stomp'].includes(type)){P.active=type==='ram'?1.5:2.0;P.tell+=.18;P.lanes=[{x:b.x,y:b.y,ex:P.tx,ey:P.ty,width:type==='talons'?90:76,tx:P.tx,ty:P.ty}];}
 if(type.endsWith('MG'))P.sweepWarnings=f1003bMuzzles(b).flatMap(({x,y,side})=>[-.1,.2,.5].map(offset=>{
  const a=Math.PI/2+side*offset;return{x,y,ex:x+Math.cos(a)*400,ey:y+Math.sin(a)*400,width:24};}));
 if(type==='bombing'||type==='eruptions')f1003bTargets(b,P,'lava',diffKey==='furious'?5:3);
 if(type==='gravity'||type==='turbines'){P.active=2.6;P.tell+=.2;P.gravity={x:clamp(P.tx+(S.seq%2?90:-90),camLeftX()+65,camRightX()-65),y:P.ty-95};}
 if(['orbit','iceOrbit'].includes(type))P.active=2.9;
};
function f1003bKnightTick(b,dt){
 const S=b._r30,P=S.attack,K=P.k1003;P.t+=dt;K.age+=dt;
 const phase=K.phase,dur=s81003KnightDur(phase)+(phase==='recover'?.9:0);
 if(['slashTell','jumpTell','followTell'].includes(phase))combatWarningTick(b,'finale-knight-'+P.seq+'-'+P.kIndex,K.age,dur);
 if(phase==='slash'&&K.age>=.13)s81003KnightHit(b,'slash');
 if(phase==='land'&&K.age>=.02){s81003KnightHit(b,'land');if(!K.orbs){K.orbs=true;f1003bRing(b,K.target.x,K.target.y,7,'code',.42);}}
 if(phase==='sweep'&&K.age>=.04)s81003KnightHit(b,'sweep');
 if(K.age<dur)return;
 const Q=s81003KnightPose(b);K.x=Q.x;K.y=Q.y;
 const next=P.kSteps[++P.kIndex];
 if(next){K.orbs=false;s81003KnightEnter(b,next);return;}
 S.attack=null;S.shield=0;S.cd=2.0;f1003bLog(b,'recover',{seconds:2});
}
function f1003bRing(b,x,y,count,kind,offset=0){
 const aim=Math.atan2(player.y-y,player.x-x);
 // A full angular gap aimed at the ship, with no projectile on its centerline.
 for(let i=0;i<count;i++){const a=aim+offset+TAU*(i+.5)/count;f1003bShot(b,x,y,a,2.3,kind);}
 r30Sound('combatOrb0927');
}
r30AttackTick=function(b,dt){
 if(!b?._r30?.finale1003b)return F1003B_BASE.attackTick.apply(this,arguments);
 const S=b._r30,P=S.attack,n=r30Difficulty();if(!P)return;if(P.k1003)return f1003bKnightTick(b,dt);
 P.t+=dt;const u=P.t-P.tell;combatWarningTick(b,'finale-'+S.form+'-'+P.seq,Math.min(P.t,P.tell),P.tell);
 if(u<0)return;
 if(!P.started){P.started=true;f1003bLog(b,'release',{type:P.type});
  if(P.lanes.length&&!['talons','ram','stomp'].includes(P.type))for(const L of P.lanes)s81003Beam(b,L,P.type==='code'||P.type==='carrierLance'?'code':'alien',.66);
  if(['orbit','iceOrbit','gravity','turbines'].includes(P.type)){
   const q=P.gravity||{x:b.x,y:b.y+80};S.orbitals=Array.from({length:6},(_,i)=>({a:i*TAU/6,x:q.x,y:q.y,cx:q.x,cy:q.y,t:0,kind:P.type==='iceOrbit'?'ice':'code',launched:false}));
  }
  r30Sound(['talons','ram','stomp'].includes(P.type)?'combatAlien0927':'enemyBossCannon');
 }
 if(P.gravity&&u<2.2){const G=P.gravity;for(const seat of seatList())withSeat(seat,()=>{
  if(player.dead||player.roll||player.somer||chargeDashing())return;
  const dx=G.x-player.x,dy=G.y-player.y,d=Math.hypot(dx,dy);if(d>55&&d<330){const speed=(P.type==='turbines'?27:21)*dt;player.x+=dx/d*speed;player.y+=dy/d*speed;}
 });}
 if(['talons','ram','stomp'].includes(P.type)){
  const Q=r30Pose(b);
  if(P.type==='talons')for(const v of r30Parts(b).filter(v=>v.p.id!=='core')){
   const x=v.x-Math.sin(v.rot)*v.h*.38,y=v.y+Math.cos(v.rot)*v.h*.38;
   for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-x,player.y-y)<33)playerHit('orbital host talon');});
  }
  if(P.type==='ram')for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-Q.x,player.y-Q.y)<46)playerHit('alien storm ram');});
  if(P.type==='stomp'&&u>P.active*.45&&!P.struck){P.struck=true;r30Sound('hammerImpact');r30FX(b,P.tx,P.ty,140);shake=Math.max(shake,8);
   for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-P.tx,player.y-P.ty)<44)playerHit('warden gravity stomp');});f1003bRing(b,P.tx,P.ty,9,'code');
  }
 }
 const guns=['rotorMG','iceMG','wardenMG','magma','missiles','bombing','eruptions'];
 if(guns.includes(P.type)&&u>=P.next){
  const rapid=P.type.endsWith('MG'),ice=P.type==='iceMG',magma=P.type==='magma',missile=P.type==='missiles';
  P.next=u+(rapid?.18:missile?.65:.72);P.fired++;
  for(const {x,y,side} of f1003bMuzzles(b)){
   const a=rapid?Math.PI/2+side*(.20+Math.sin(u*2.3)*.30):Math.atan2(P.ty-y,P.tx-x);
   for(let j=0;j<(magma?3:1);j++)f1003bShot(b,x,y,a+(j-(magma?1:0))*.22,rapid?4.1:missile?2.6:2.5,ice?'ice':missile?'missile':magma?'fire':'code',magma);
  }r30Sound(rapid?'enemyMachineGunHeavy':magma?'combatOrb0927':'enemyBossCannon');
 }
 if(u>P.active){S.attack=null;S.shield=0;S.cd=diffKey==='easy'?1.8:P.type==='stomp'||P.type==='ram'?1.65:1.15;f1003bLog(b,'recover',{seconds:S.cd});}
};
function f1003bOrbitals(b,dt){
 const S=b._r30;for(const q of S.orbitals){q.t+=dt;const r=48+q.t*20,a=q.a+q.t*1.7;q.x=q.cx+Math.cos(a)*r;q.y=q.cy+Math.sin(a)*r;
  if(q.t>1.0&&!q.launched){q.launched=true;f1003bShot(b,q.x,q.y,q.a+q.t*1.7,2.8,q.kind);}
 }S.orbitals=S.orbitals.filter(q=>q.t<1.1);
 for(const q of eBullets)if(q._finaleTurn&&!q.dead){const speed=Math.hypot(q.vx,q.vy),a=Math.atan2(q.vy,q.vx),want=Math.atan2(player.y-q.y,player.x-q.x),delta=Math.atan2(Math.sin(want-a),Math.cos(want-a));
  q._finaleLife=(q._finaleLife||0)+dt;if(q._finaleLife<1.25){const a2=a+clamp(delta,-q._finaleTurn*dt,q._finaleTurn*dt);q.vx=Math.cos(a2)*speed;q.vy=Math.sin(a2)*speed;}
 }
}
r30Tick=function(b,dt){
 const S=b._r30;if(!S?.finale1003b)return F1003B_BASE.tick.apply(this,arguments);dt=Math.min(.05,dt);
 if(['finalFall','escape','reunion','done'].includes(S.mode))return F1003B_BASE.tick(b,dt);
 S.t+=dt;S.clock+=dt;b.t+=dt;b.flash=Math.max(0,(b.flash||0)-dt);S.shieldFlash=Math.max(0,(S.shieldFlash||0)-dt);S.wallAge1003+=dt;
 for(const p of b.parts)p.flash=Math.max(0,p.flash-dt);for(const f of S.fx)f.t+=dt;S.fx=S.fx.filter(f=>f.t<.7);
 if(S.mode==='fight'){
  b.enter=false;
  if(!S.attack){const cx=worldWidth()/2,amp=Math.max(0,Math.min(72,(camRightX()-camLeftX()-b.w)*.26));
   b.x+=clamp(cx+Math.sin(S.clock*.7)*amp-b.x,-90*dt,90*dt);b.y+=clamp(b.ty+Math.cos(S.clock*.7)*12-b.y,-50*dt,50*dt);
   S.cd-=dt;if(S.cd<=0)r30Attack(b);}
  else r30AttackTick(b,dt);
  f1003bOrbitals(b,dt);return;
 }
 b.enter=true;for(const seat of seatList())withSeat(seat,()=>{player.invuln=Math.max(player.invuln||0,.3);});
 if(S.mode==='takeover'){
  if(!S.entryCue){S.entryCue=true;r30Sound('combatAlien0927');}
  if(S.t>=5.2){S.mode='fight';S.t=0;b.enter=false;bossPhaseMusic(8,1);r30Sound('bossPhase');}return;
 }
 if(S.mode==='morph1003b'&&S.t>=1.65){r30Form(b,S.form+1);S.mode='reveal';S.t=0;r30Sound('teleportIn');bossPhaseMusic(8,Math.min(3,S.form+1));return;}
 if(S.mode==='reveal'&&S.t>=1.1){S.mode='fight';S.t=0;b.enter=false;}
};
function f1003bBodyDraw(b,alpha=1){
 const S=b._r30,Q=r30Pose(b),D=f1003bDef(b),P=S.attack;
 if(P?.k1003){s81003KnightDraw(b);return;}
 let frame=P?(P.t<P.tell?1:(P.t-P.tell)% .24<.15?2:3):0;
 if(S.form===0)for(const v of r30Parts(b))r30Blit(v.key,v.x,v.y,v.w,v.h,v.rot,alpha);
 else if(D.id==='chopper'){r30Blit('chopper_body',Q.x,Q.y,D.w,D.h,0,alpha);r30Blit('chopper_rotor',Q.x,Q.y-5,D.w+25,D.w+25,S.clock*15,alpha);}
 else if(D.id==='knight')s81003Cell('knight',0,Q.x,Q.y,320,320,alpha);
 else f1003bCell(D.id,frame,Q.x,Q.y,D.w*(Q.scale||1),D.h*(Q.scale||1),alpha);
 if(b.flash>0&&S.form===0)for(const v of r30Parts(b))
  fmcWhiteBlit(v.key,v.x,v.y,v.w,v.h,v.rot,alpha*v.alpha*Math.min(1,b.flash*9));
 s81003ShieldDraw(b);
}
r30DrawBoss=function(b){
 if(!b?._r30?.finale1003b)return F1003B_BASE.draw.apply(this,arguments);
 const S=b._r30,P=S.attack,T=S.t;
 if(['escape','reunion','done'].includes(S.mode))return F1003B_BASE.draw(b);
 ctx.save();
 if(S.mode==='takeover'){
  const u=clamp(T/5.2,0,1);r30Blit('vile24_robot_gray',b.x,b.y,230,230,0,1-clamp((u-.15)/.5,0,1));
  if(u>.25)f1003bBodyDraw(b,clamp((u-.25)/.4,0,1));
  if(u<.85)s81003Cell('morph',Math.min(11,Math.floor(u/.85*12)),b.x,b.y,350,350,1);
 }else if(S.mode==='morph1003b'){
  f1003bBodyDraw(b,Math.max(0,1-T/.65));s81003Cell('morph',Math.min(11,Math.floor(T/1.65*12)),b.x,b.y,360,360,1);
  s81003Cell('teleport',Math.min(7,Math.floor(T/1.65*8)),b.x,b.y,300,340,.85);
 }else f1003bBodyDraw(b,S.mode==='reveal'?clamp(T/.65,0,1):S.mode==='finalFall'?Math.max(0,1-T/2.8):1);
 if(S.mode==='fight'&&P&&!P.k1003&&P.t<P.tell){
  const u=P.t/P.tell;for(const L of P.lanes)s81003Fov(L,u,true);
  if(P.sweepWarnings)for(const L of P.sweepWarnings)s81003Fov(L,u,false);
  if(P.gravity)s81003Target(P.gravity.x,P.gravity.y,180,u);
  if(!P.lanes.length&&!P.gravity&&!P.sweepWarnings&&!['bombing','eruptions'].includes(P.type))for(const {x,y,side} of f1003bMuzzles(b))s81003Fov({...s81003Lane(x,y,P.tx+side*45,P.ty,12),tx:P.tx+side*45,ty:P.ty},u,true);
 }
 if(S.mode==='fight'&&P?.gravity&&P.t>=P.tell)s81003Cell('teleport',5,P.gravity.x,P.gravity.y,150,180,.4);
 for(const q of S.orbitals)s81003Cell('fov',8+Math.floor(q.t*12)%4,q.x,q.y,27,34,.9);
 for(const f of S.fx)if(f.kind!=='morph')r30Blit('fx_'+Math.min(3,Math.floor(f.t/.7*4)),f.x,f.y,f.size,f.size,0,1-f.t/.7);
 ctx.restore();
};
bossHealthVisible=function(b){return b?._r30?.finale1003b?!['escape','reunion','done'].includes(b._r30.mode):F1003B_BASE.visible.apply(this,arguments);};
function f1003bBarFractions(b){const S=b._r30;return F1003B_FORMS.map((d,i)=>S.mode==='takeover'?clamp((S.t-.3-i*.48)/.46,0,1):i<S.form?0:i>S.form?1:clamp(b.hp/b.maxhp,0,1));}
drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld,lagKey){
 const b=boss,S=b?._r30;if(kind!=='boss'||!S?.finale1003b)return F1003B_BASE.bar.apply(this,arguments);
 if(!XART.rdy('bmbar_frame_boss')||!XART.rdy('bmbar_fill_solid'))return false;
 // Eight authored housings with eight luminance-preserving palette variants.
 const h=8,pitch=6,top=cy-5,shift=inWorld?camX:0,rows=f1003bBarFractions(b),O=BMBAR.boss;
 ctx.save();ctx.translate(shift,0);ctx.imageSmoothingEnabled=false;
 drawBossTab('boss',cx,top,w);
 for(let i=7;i>=0;i--){const x=cx-w/2,y=top+i*pitch;ctx.globalAlpha=i<S.form?.30:1;
  ctx.drawImage(XART.get('bmbar_frame_boss'),x,y,w,h);
  const im=xartPalette('bmbar_fill_solid',F1003B_FORMS[i].color);if(im&&rows[i]>0){const fx=x+O.dx*w/700,fy=y+O.dy*h/33,fw=O.w*w/700,fh=O.h*h/33;
   ctx.save();ctx.beginPath();ctx.rect(fx,fy,fw*rows[i],fh);ctx.clip();ctx.drawImage(im,fx,fy,fw,fh);ctx.restore();}
 }
 ctx.globalAlpha=1;if(S.shield>0)drawShieldBarArt(S.shield/S.shieldMax,cx,top+pitch*8+8,w,b);
 ctx.restore();return true;
};
