"use strict";
/* Persistent authored encounters. This layer owns the three outer fights;
   donor bosses retain their original controllers, not generic bullet books. */
const ON5={draws:{},events:[],pending:null};
const ON5F={spawn:spawnBoss,encounter:j3Encounter,mimic:j3Mimic,save:j3Save,home:j3Home,morph:j3Morph,
 tick:r30Tick,draw:r30DrawBoss,pose:r30Pose,rig:fmcRig,alive:fmcAlive,hit:modularHit,
 clear:r30Clear,gauge:fmcGauge,attack:r30Attack,attackTick:r30AttackTick,warm:r30Warm,donor:gd4Tick};
for(const cells of Object.values(ON5_ART))for(const a of cells)XART._src[a.key]=a.path;
for(const [f,a]of ON5_ART.knight.entries())FMC_ART[a.key]={key:a.key,path:a.path,rects:{pose:[0,0,a.w,a.h]}};
function on5Log(event,data={}){ON5.events.push({event,...data});if(ON5.events.length>200)ON5.events.shift();}
function on5Cell(name,f,x,y,w,h=w,rot=0){const a=ON5_ART[name]?.[((f|0)%ON5_ART[name].length+ON5_ART[name].length)%ON5_ART[name].length];
 if(!a||!XART.rdy(a.key))return false;ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(rot);ctx.drawImage(XART.get(a.key),-w/2,-h/2,w,h);ctx.restore();ON5.draws[name]=(ON5.draws[name]||0)+1;return true;}
r30Warm=function(){const r=ON5F.warm.apply(this,arguments);for(const cells of Object.values(ON5_ART))for(const a of cells)XART.rdy(a.key);return r;};
spawnBoss=function(){const r=ON5F.spawn.apply(this,arguments),b=boss,J=j3State(b);if(J){
 J.max=J.max.map((v,i)=>Math.ceil(v*(i===0?1.30:i===5?1.65:1.50)));J.hp=J.max.slice();J.cursor=0;J.modules=[];
 J.on5={supply:11,supplyN:0,clock:0};j3Encounter(b,0);on5Log('finaleBudgets',{max:J.max.slice()});}return r;};
j3Save=function(b){const J=j3State(b);if(!J||J.encounter!==2)return;
 J.hp[J.active]=Math.max(0,Math.min(J.hp[J.active],b.hp));if(J.mimic!=null)J.modules[J.mimic]=b.parts;};
j3Encounter=function(b,n){const r=ON5F.encounter.apply(this,arguments),J=j3State(b),S=b._r30;
 if(J){S.on5Shield=null;S.on5Knight=null;S.on5ShieldCd=3;S.shield=0;
  if(n===1){S.mode='ghostIntro1005';S.t=0;b.enter=true;}
  if(n===2&&S.mode==='coronation1003j'){S.mode='voidIntro1005';S.t=0;b.enter=true;}
 }return r;};
j3Mimic=function(b,i){const J=j3State(b);if(!J||J.hp[i]<=0)return j3Home(b);const r=ON5F.mimic.apply(this,arguments);J.cursor=i;
 if(i===5){b.parts=b.parts.filter(p=>['core','sword','shield'].includes(p.id));J.modules[i]=b.parts;}
 b._r30.on5Shield=null;b._r30.on5ShieldCd=2.8;b._r30.on5Knight=null;return r;};
j3Home=function(b){const J=j3State(b);j3Save(b);if(J.hp.every(h=>h<=0))return j3FinalDeath(b);
 if(J.hp[0]<=0){const next=j3Next(J);return j3Mimic(b,next);}
 J.active=0;j3Encounter(b,2);b._r30.mode='reveal1003j';b._r30.t=0;J.attacks=0;j3Log(b,'draculaReturn',{hp:J.hp[0]});};
j3Morph=function(b,to){const J=j3State(b);if(J?.encounter===2&&J.mimic==null&&typeof to==='number'){
  for(let n=1;n<=8;n++){const i=(J.cursor+n)%8;if(J.hp[i]>0){to=i;break;}}
 }return ON5F.morph.call(this,b,to);};
function on5OrbitBits(b,t,front,size=220){
 for(let i=0;i<18;i++){const phase=t*2.7+i*TAU/18,depth=Math.sin(phase),row=i%3;if((depth>=0)!==front)continue;
  const turn=((phase/TAU%1+1)%1),f=row*8+Math.floor(turn*8),r=size*(.48+.08*Math.sin(i));
  const x=b.x+Math.cos(phase)*r,y=b.y+Math.sin(phase)*r*.43+Math.sin(t*1.8+i)*10;
  const scale=.65+(depth+1)*.24;on5Cell('fragments',f,x,y,(20+i%4*5)*scale,(29+i%3*8)*scale,Math.cos(phase)*.55);
 }}
function on5IntroDraw(b){const S=b._r30,t=S.t,voidIntro=S.mode==='voidIntro1005',ghost=S.mode==='ghostIntro1005';
 const duration=voidIntro?8.7:ghost?4.8:5.2,bodyAt=voidIntro?3.9:ghost?2.2:2.65;
 on5OrbitBits(b,t,false,voidIntro?300:210);
 if(t<bodyAt+.6){const f=t<1.6?Math.min(2,Math.floor(t/1.6*3)):t<bodyAt?3+Math.min(3,Math.floor((t-1.6)/(bodyAt-1.6)*4)):8;
  on5Cell('symbiote',f,b.x,b.y,voidIntro?400:300,voidIntro?400:300);
 }
 if(S.mode==='takeover'&&t<2.2)r30Blit('vile24_robot_gray',b.x,b.y,230,230,0,1);
 if(t>=bodyAt){ctx.save();ctx.translate(b.x,b.y);const k=Math.min(1,(t-bodyAt)/.8);ctx.scale(.25+.75*k,.25+.75*k);ctx.translate(-b.x,-b.y);j3Body(b,1);ctx.restore();}
 on5OrbitBits(b,t,true,voidIntro?300:210);
 if(t>duration-.65)on5Cell('symbiote',10,b.x,b.y,330,330);
}
function on5FightStart(b){const S=b._r30,J=j3State(b);S.mode='fight';S.t=0;S.cd=.65;b.enter=false;bossPhaseMusic(8,J.encounter+1);j3Log(b,'fightStart');r30Sound('bossPhase');}
const ON5_RAISE=cwdRaise;
cwdRaise=function(b,color,hp){const r=ON5_RAISE.apply(this,arguments);if(j3State(b)){
 b._r30.on5Shield={age:0,hp:b._r30.shield,max:b._r30.shieldMax,color};on5Log('shieldRaised',{color,hp:b._r30.shield});}return r;};
function on5Shield(b,color,hp){return cwdRaise(b,color,hp);}
function on5ShieldHit(b,dmg){const S=b._r30,q=r30ShieldBounds(b);const dealt=Math.min(S.shield,dmg);S.shield=Math.max(0,S.shield-dealt);
 if(S.on5Shield)S.on5Shield.hp=S.shield;S.shieldFlash=.14;cwdImpact(b,q);
 if(S.shield===0){cwdShatter(b,q);S.on5Shield=null;S.on5ShieldCd=7;j3Log(b,'shieldExhausted1005',{hp:0});}return dealt;}
modularHit=function(dmg){const b=boss,J=j3State(b),S=b?._r30;
 if(J&&r30Live(b)&&Number.isFinite(dmg)&&dmg>0&&S.shield>0&&b._lastPart?.id==='codeWall1003d')return on5ShieldHit(b,dmg);
 return ON5F.hit.apply(this,arguments);};
r30Clear=function(b){const keep=CWD.effects.filter(f=>f.owner===b&&['chip','shatter','impact'].includes(f.kind));const r=ON5F.clear.apply(this,arguments);
 for(const f of keep)if(!CWD.effects.includes(f))CWD.effects.push(f);if(b?._r30){b._r30.on5Shield=null;b._r30.on5Knight=null;}return r;};
// Main Dracula always owns pool zero. Returning from a copy never selects a fresh
// pool for his body; defeated copies cannot be selected or rebuilt.
r30Tick=function(b,dt){const J=j3State(b),S=b?._r30;if(!J)return ON5F.tick.apply(this,arguments);dt=Math.min(.05,dt);
 if(['ghostIntro1005','voidIntro1005'].includes(S.mode)){
  j3Timers(b,dt);b.enter=true;eBullets.length=0;for(const seat of seatList())withSeat(seat,()=>player.invuln=Math.max(player.invuln||0,.3));
  if(S.mode==='voidIntro1005'){const q=fmcGauge(b);if(q.charge>=0&&q.charge!==J.gaugeLife){J.gaugeLife=q.charge;r30Sound('combatEnergy0927');}}
  if(S.t>=(S.mode==='voidIntro1005'?8.7:4.8))on5FightStart(b);return;
 }
 if(S.mode==='fight'&&J.encounter<2){
  j3Timers(b,dt);b.enter=false;b.x=worldWidth()/2+Math.sin(S.clock*.64)*(J.encounter===1?72:44);b.y=b.ty+Math.sin(S.clock*.9)*12;
  if(S.attack)r30AttackTick(b,dt);else{S.cd-=dt;if(S.cd<=0)r30Attack(b);}on5ShieldTick(b,dt);return;
 }
 const oldShield=S.shield,oldForm=S.form,mode=S.mode,r=ON5F.tick(b,dt);
 if(mode==='fight'&&S.mode==='fight'&&S.form===oldForm&&S.on5Shield&&oldShield>0)S.shield=S.on5Shield.hp;
 if(S.mode==='fight'){on5ShieldTick(b,dt);if(J.encounter===2){J.on5.clock+=dt;J.on5.supply-=dt;
  if(J.on5.supply<=0){J.on5.supply=diffKey==='easy'?18:22;const kind=J.on5.supplyN++%2?'timebomb':'furybomb';
   powerups.push({kind:'capsule',hp:3,flash:0,_on5Content:kind,x:clamp(player.x+(J.on5.supplyN%2?74:-74),camLeftX()+30,camRightX()-30),y:Math.max(85,player.y-165),vy:.8,t:0,w:22,h:32,bob:0,_on5Pill:true});
   XART.rdy(kind==='timebomb'?'timed_bomb_0917c':'fury_bomb_0917c');on5Log('supportPill',{kind});}
 }}return r;
};
function on5ShieldTick(b,dt){const S=b._r30;if(S.on5Shield){S.on5Shield.age+=dt;S.wallAge1003=(S.wallAge1003||0)+dt;S.shieldFlash=Math.max(0,(S.shieldFlash||0)-dt);
 if(S.on5Shield.age>=6.5){on5ShieldHit(b,S.shield);on5Log('shieldDischarged');}}}
fmcGauge=function(b){const S=b?._r30;if(S?.mode==='voidIntro1005'){const t=Math.max(0,S.t-4.3),n=clamp(Math.floor(t/.5),0,7);
 return{charge:S.t<4.3?-1:n,color:F1003B_FORMS[n].color,under:n?F1003B_FORMS[n-1].color:null,frac:S.t<4.3?0:clamp((t-n*.5)/.4,0,1)};}return ON5F.gauge.apply(this,arguments);};
const ON5_HEALTH=bossHealthVisible;
bossHealthVisible=function(b){return b?._r30&&['ghostIntro1005','voidIntro1005'].includes(b._r30.mode)||ON5_HEALTH.apply(this,arguments);};
r30DrawBoss=function(b){const J=j3State(b),S=b?._r30;if(!J)return ON5F.draw.apply(this,arguments);
 if(['takeover','ghostIntro1005','voidIntro1005'].includes(S.mode))return on5IntroDraw(b);
 if(['transform1003j','reveal1003j','encounterReform1003j'].includes(S.mode)){
  on5OrbitBits(b,S.t,false,240);if(S.mode!=='encounterReform1003j')j3Body(b,1);
  on5Cell('symbiote',S.mode==='transform1003j'?6:9,b.x,b.y,340,350);on5OrbitBits(b,S.t,true,240);return;
 }
 const r=ON5F.draw.apply(this,arguments);const P=S.attack;if(P?.on5&&P.t<P.tell){
  if(P.lanes?.length)for(const L of P.lanes)s81003Fov(L,P.t/P.tell,true);
  if(['hostClaws','ghostDive'].includes(P.type))groundTargetReticleDraw(P.tx,P.ty,96,P.t/P.tell,.85);
 }const K=S.on5Knight;if(K?.phase==='tell')combatWarningDraw(b,{x:b.x,y:b.y,ex:K.tx,ey:K.ty,width:105,progress:K.t/1.15});return r;
};
// The first two outer bosses are independent threatening encounter books.
r30Attack=function(b){const J=j3State(b),S=b?._r30;if(!J||J.encounter>=2)return ON5F.attack.apply(this,arguments);
 const ghost=J.encounter===1,book=ghost?['ghostVolley','ghostDive','ghostLance','ghostOrbit']:['hostGuns','hostClaws','hostLance','hostOrbit'];
 const type=book[S.seq++%book.length],P=S.attack={on5:true,type,lanes:[],t:0,tell:diffKey==='easy'?1.5:1.15,active:type.endsWith('Lance')?1.0:2.8,next:0,fired:0,
  tx:clamp(player.x,camLeftX()+55,camRightX()-55),ty:clamp(player.y,250,VH-65),fromX:b.x,fromY:b.y};
 if(type.endsWith('Lance'))P.lanes=[-1,1].map(s=>({...s81003Lane(b.x+s*54,b.y+48,P.tx+s*46,P.ty,16),tx:P.tx+s*46,ty:P.ty}));
 if(!ghost&&type.endsWith('Orbit'))on5Shield(b,'blue',Math.ceil(b.maxhp*.045));
 r30Sound('bossWeaponCharge');j3Log(b,'attack',{type});
};
r30AttackTick=function(b,dt){const S=b._r30,P=S.attack;if(!P?.on5)return ON5F.attackTick.apply(this,arguments);P.t+=dt;const u=P.t-P.tell;
 combatWarningTick(b,'on5-'+S.seq,Math.min(P.t,P.tell),P.tell);if(u<0)return;
 if(P.type.endsWith('Lance')&&!P.fired){P.fired++;for(const L of P.lanes)s81003Beam(b,L,'code',P.active);r30Sound('combatBeam0927');}
 else if(P.type==='hostClaws'||P.type==='ghostDive'){
  const Q=r30Pose(b);for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-Q.x,player.y-Q.y)<(P.type==='hostClaws'?57:42))playerHit('symbiote lunge');});
  if(u>=P.next){P.next=u+.58;const a=Math.atan2(P.ty-Q.y,P.tx-Q.x);for(const d of [-.30,.30])f1003bShot(b,Q.x,Q.y+48,a+d,3.3,'code');}
 }else if(u>=P.next&&!P.type.endsWith('Lance')){
  P.next=u+(P.type.endsWith('Orbit')?.88:.42);P.fired++;
  if(P.type.endsWith('Orbit')){const gap=Math.atan2(P.ty-b.y,P.tx-b.x);for(let i=0;i<12;i++){const a=i*TAU/12+P.fired*.11;if(Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)))>.47)f1003bShot(b,b.x,b.y+65,a,2.8,'code');}}
  else for(const s of [-1,1]){const x=b.x+s*66,y=b.y+65,a=Math.atan2(P.ty-y,P.tx-x);for(const d of (P.type==='ghostVolley'?[-.23,0,.23]:[-.11,.11]))f1003bShot(b,x,y,a+d,3.7,'code');}
  r30Sound('enemyBossCannon');
 }
 if(u>=P.active){S.attack=null;S.cd=diffKey==='easy'?1.4:1.05;S.ghostHidden=false;}
};
r30Pose=function(b){const P=b?._r30?.attack;if(P?.on5){const u=clamp((P.t-P.tell)/P.active,0,1),dash=['hostClaws','ghostDive'].includes(P.type),k=dash?Math.sin(u*Math.PI):0;
 return{x:lerp(b.x,P.tx,k),y:lerp(b.y,P.ty-35,k),angle:0,alpha:1,scale:1,shape:j3State(b).encounter===1?'ghost':'host'};}return ON5F.pose.apply(this,arguments);};
// Intact authored knight body. Weapons remain independently targetable.
fmcAlive=function(b,id){if(j3State(b)?.mimic===5&&['head','legL','legR','swordArm','shieldArm'].includes(id))return b.parts.some(p=>p.id==='core'&&!p.destroyed);return ON5F.alive.apply(this,arguments);};
function on5KnightFrame(b){const K=b._r30.on5Knight,h=cf4Knight(b);if(K)return K.phase==='tell'?4:K.kind==='bash'?5:6;
 if(!h)return 0;if(['warn','storm_warn','giant_warn','giant_windup'].includes(h.state))return 1;
 if(['leap','giant_dive','storm_slam'].includes(h.state))return 7;
 if(['recover','giant_sweep'].includes(h.state)&&h.t<.28)return 2;
 if(['spin','whirlwind','throw'].includes(h.state))return 3;
 if(h.state.startsWith('spell'))return 6;return 0;}
const ON5_HANDS=[[[.19,.61],[.82,.64]],[[.19,.15],[.85,.53]],[[.34,.72],[.77,.60]],[[.16,.43],[.93,.56]],[[.19,.65],[.80,.65]],[[.21,.66],[.82,.46]],[[.21,.61],[.79,.19]],[[.20,.14],[.86,.43]]];
fmcRig=function(b){if(j3State(b)?.mimic!==5)return ON5F.rig.apply(this,arguments);
 const Q=r30Pose(b),k=Q.scale||1,f=on5KnightFrame(b),a=ON5_ART.knight[f],w=244*k,h=w*a.h/a.w,out=[];
 const core=b.parts.find(p=>p.id==='core'),spec={px:.5,py:.5,art:'pose',sheet:a.key};
 out.push({p:core,spec,key:a.key,ax:Q.x,ay:Q.y,x:Q.x,y:Q.y,w,h,rot:0,alpha:1,z:1});
 for(const [i,id]of ['sword','shield'].entries()){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed)continue;
  const node=FMC_RIGS.knight.find(n=>n.id===id),hand=ON5_HANDS[f][i],ax=Q.x+(hand[0]-.5)*w,ay=Q.y+(hand[1]-.5)*h;
  const v={p,spec:{...node,parent:null,px:i?.5:.51,py:i?.36:.15},key:'fmc_knight',ax,ay,w:node.w*k,h:node.h*k,rot:i?0:f===1||f===7?Math.PI:f===3?-Math.PI/2:.1,alpha:1,z:5};
  const T=cf4Knight(b)?.throw;if(id==='sword'&&T){v.ax=T.x;v.ay=T.y;v.rot=T.angle;v.spec.px=v.spec.py=.5;}
  Object.assign(v,fmcPoint(v,.5,.5));out.push(v);
 }return out;};
const ON5_GRIP=hammerGripPoint;
hammerGripPoint=function(b){if(b?._gp4Host&&j3State(b._gp4Host)?.mimic===5){
 const v=fmcRig(b._gp4Host).find(v=>v.p.id==='sword');if(v)return{x:v.ax,y:v.ay};}return ON5_GRIP.apply(this,arguments);};
// Code fragments stay opaque until their authored terminal shatter; no fade.
cwdEffectsDraw=function(){for(const f of CWD.effects){
 if(f.kind==='chip'&&f.t<f.dur-.16){const a=CWD_ART.wall,im=cwdImage('wall'),box=a.rects[f.color==='red'?'redRows':'blueRows'];if(!im)continue;
  const [x,y,w,h]=box;ctx.save();ctx.translate(f.x,f.y);ctx.rotate(f.rot);ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,x+f.col*w/15,y+f.row*h/12,w/15,h/12,-f.w/2,-f.h/2,f.w,f.h);ctx.restore();
 }else if(f.kind==='chip')cwdCell('shatter',Math.min(7,Math.floor((f.t-f.dur+.16)/.16*8)),f.x,f.y,f.w*2.5,f.h*2.5,1,0,f.color);
 else cwdCell(f.kind,Math.min(7,Math.floor(f.t/f.dur*8)),f.x,f.y,f.w,f.h,1,0,f.color);
}};
gd4Tick=function(b,dt){const J=j3State(b);if(J?.mimic!==5)return ON5F.donor.apply(this,arguments);
 const S=b._r30,D=gd4Create(b,5),p=D.p;let K=S.on5Knight;
 if(!K){const r=ON5F.donor(b,dt);if(S.mode!=='fight')return r;S.on5ShieldCd=(S.on5ShieldCd||0)-dt;
  if(S.on5ShieldCd<=0&&fmcAlive(b,'shield')){S.on5ShieldCd=8;S.on5Knight={kind:(S.on5KnightN=(S.on5KnightN||0)+1)%2?'bash':'code',phase:'tell',t:0,tx:player.x,ty:player.y,ox:b.x,oy:b.y,next:0};
   on5Shield(b,'red',Math.ceil(b.maxhp*.045));r30Sound('bossWeaponCharge');}return r;}
 D.age+=dt;K.t+=dt;p.hp=b.hp;p.maxhp=b.maxhp;p.t+=dt;
 if(K.phase==='tell'){combatWarningTick(b,'dark-shield-'+S.on5KnightN,K.t,1.15);if(K.t>=1.15){K.phase='active';K.t=0;r30Sound('combatAlien0927');}}
 else if(K.phase==='active'){
  if(K.kind==='bash'){const u=clamp(K.t/1.3,0,1),k=Math.sin(u*Math.PI);b.x=p.x=lerp(K.ox,K.tx,k);b.y=p.y=lerp(K.oy,K.ty-95,k);
   const v=fmcRig(b).find(v=>v.p.id==='shield');if(v)for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-v.x,player.y-v.y)<52)playerHit('dark shield smite');});
  }else if(K.t>=K.next){K.next=K.t+.40;const v=fmcRig(b).find(v=>v.p.id==='shield');if(v){const a=Math.atan2(K.ty-v.y,K.tx-v.x);for(const d of [-.24,0,.24])f1003bShot(b,v.x,v.y,a+d,3.9,'code');r30Sound('enemyBossCannon');}}
  if(K.t>=(K.kind==='bash'?1.3:2.4)){K.phase='recover';K.t=0;}
 }else if(K.t>.65){S.on5Knight=null;hammerTarget(p);hammerState(p,'warn');}
 if(!fmcAlive(b,'shield')){S.on5Knight=null;S.shield=0;}if(D.age>=32){D.age=0;j3Morph(b,'home');}
};
