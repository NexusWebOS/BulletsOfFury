"use strict";
/* October 5: a true Hammer copy and its articulated sword/shield extension.
   Three outer encounters remain authoritative. Each copied body owns one pool. */
const HK5={events:[],draws:{}};
const HK5_BASE={spawn:spawnBoss,mimic:j3Mimic,morph:j3Morph,save:j3Save,next:j3Next,clear:j3Clear,
 donor:gd4Tick,create:gd4Create,rig:fmcRig,parts:r30Parts,draw:r30DrawBoss,body:f1003bBodyDraw,
 hit:modularHit,targets:retinaBossTargets,warm:r30Warm,head:hammerHeadPoint,grip:hammerGripPoint,
 state:hammerState,impact:hammerStormImpact,gauge:fmcGauge,bullets:drawBullets};
F1003B_FORMS.push({id:'hammer',name:'THE CODE HAMMER',color:'#ff3545',hp:1.2,w:270,h:250,book:['hammer']});
GD4_KIND[8]='hammer';
ON5_CODES.HAMR8={stage:8,role:'boss',phase:2,mimic:8};PASSWORDS.HAMR8=8;
for(const cells of Object.values(HK5_ART))for(const a of cells){XART._src[a.key]=a.path;FMC_ART[a.key]={key:a.key,path:a.path,rects:{pose:[0,0,a.w,a.h]}};}
function hk5Log(event,data={}){HK5.events.push({event,...data});if(HK5.events.length>180)HK5.events.shift();}
function hk5Own(b){return j3State(b)?.encounter===2&&[5,8].includes(j3State(b).mimic);}
function hk5Cell(a,x,y,w,h,rot=0,tint=null){if(!a||!XART.rdy(a.key))return false;ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(tint?xartTint(a.key,tint,1):XART.get(a.key),-w/2,-h/2,w,h);ctx.restore();HK5.draws[a.key]=(HK5.draws[a.key]||0)+1;return true;}
r30Warm=function(){const r=HK5_BASE.warm.apply(this,arguments);for(const a of Object.values(HK5_ART).flat())XART.rdy(a.key);return r;};
spawnBoss=function(){const r=HK5_BASE.spawn.apply(this,arguments),J=j3State(boss);if(J&&J.max.length===8){const n=J.max[5];J.max.push(n);J.hp.push(n);hk5Log('hammerPool',{max:n});}return r;};
j3Next=function(J){for(let n=1;n<=J.hp.length;n++){const i=(J.active+n)%J.hp.length;if(J.hp[i]>0)return i;}return -1;};
j3Save=function(b){const J=j3State(b);if(J?.encounter===2&&J.mimic===8){J.hp[8]=clamp(b.hp,0,J.max[8]);J.modules[8]=b.parts;return;}return HK5_BASE.save.apply(this,arguments);};
j3Morph=function(b,to){const J=j3State(b);if(J?.encounter===2&&J.mimic==null&&typeof to==='number'){
 for(let n=1;n<=J.hp.length;n++){const i=(J.cursor+n)%J.hp.length;if(J.hp[i]>0){to=i;break;}}
 // Avoid the older eight-entry selector; the destination is already committed.
 return ON5F.morph.call(this,b,to);
 }return HK5_BASE.morph.apply(this,arguments);};
j3Mimic=function(b,i){if(i!==8){const r=HK5_BASE.mimic.apply(this,arguments);if(i===5){b._r30.hkKnight=null;b._r30.hkKnightCd=1.2;b._r30.on5Knight=null;b._r30.shield=0;}return r;}
 const J=j3State(b),S=b._r30;if(!J||J.hp[8]<=0)return j3Home(b);j3Save(b);
 J.active=J.mimic=8;J.cursor=8;J.attacks=0;S.form=8;S.finale1003b=S.modular1003c=true;S.base=J.max[8];S.pools=J.max;
 b.parts=J.modules[8]||[{id:'core',hp:J.hp[8],maxhp:J.max[8],destroyed:false,flash:0,spec:{role:'core'}},
 {id:'hammer',hp:100,maxhp:100,destroyed:false,flash:0,spec:{role:'weapon'}}];
 j3Health(b,J.hp[8],J.max[8]);S.mode='reveal1003j';S.t=0;S.attack=null;S.on5Shield=S.on5Knight=null;S.shield=0;b.enter=true;b._noHit=false;
 b.w=270;b.h=250;b.name='THE CODE HAMMER';if(!J.visited.includes(8))J.visited.push(8);j3Log(b,'mimicEnter',{id:'hammer',hp:b.hp,max:b.maxhp});
};
gd4Create=function(b,i){if(i!==8)return HK5_BASE.create.apply(this,arguments);const J=j3State(b);J.gp4Donors??=[];if(J.gp4Donors[8])return J.gp4Donors[8];
 const p={_gp4Host:b,kind:'hammer',x:b.x,y:b.y,w:158,h:176,ty:b.y,hp:b.hp,maxhp:b.maxhp,t:0,flash:0,enter:false,dead:false,_noHit:false};
 hammerBossInit(p);p.x=b.x;p.y=b.y;p.ty=b.ty;p._hammer.balance0922=true;p._hammer.mode='hammer';p._hammer.ballSeen=p._hammer.whirlSeen=false;p._hammer.comboPending=true;
 p._cin30Spoke=true;p.enter=false;p._noHit=false;hammerTarget(p);hammerState(p,'warn');const D={p,i:8,age:0,alien:999,history:[],last:null};J.gp4Donors[8]=D;return D;};
// Retinas fit wholly above the lower HUD. WORLD positions never track camera/ship.
hammerWarningFloorY=function(){return Math.min(PLAY.y+PLAY.h-48,bottomHudLayout().radar.y-44);};
hammerStormFloorY=function(){return hammerWarningFloorY();};
hammerState=function(b,state){const r=HK5_BASE.state.apply(this,arguments);if(state==='mega_charge')b._hammer.hkMegaX=b.x;return r;};
const HK5_TICK=hammerBossTick;
hammerBossTick=function(b,dt){const h=b._hammer;if(h.state==='mega_charge'){
 h.t+=Math.max(0,dt);b.x=h.hkMegaX??b.x;combatWarningTick(b,'archmage-fused-wave',h.t,1.65);
 if(h.t>1.65){h.beamHit=false;h.shotCd=.48;hammerState(b,'mega_beam');}return;
 }return HK5_TICK.apply(this,arguments);};
hammerStormImpact=function(b){const r=HK5_BASE.impact.apply(this,arguments),h=b._hammer;
 const rows=h.stormWaves||[],direction=(h.stormCycle||0)%2?1:-1,cadence=hammerFurious()?.20:hammerHard()?.30:.50;
 rows.forEach((q,i)=>{q.delay=(direction>0?i:rows.length-1-i)*cadence;q.active=.38/(q.riseRate||1)+.24+.60;
 q.y=hammerStormFloorY();q.height=Math.max(110,q.y-(PLAY.y+125));});h.stormOrder=rows.map((q,i)=>i).sort((a,b)=>rows[a].delay-rows[b].delay);return r;};
// Use the rising plate backwards for the drop. Collision reads this SAME shape.
hammerStormSpikeShape=function(q){const u=q.t-q.split-(q.delay||0)-q.warm,rise=.38/(q.riseRate||1),hold=.24,drop=.60;
 if(u<0||u>=rise+hold+drop)return null;const progress=u<rise?u/rise:u<rise+hold?1:1-(u-rise-hold)/drop;
 const f=clamp(Math.floor(progress*7),0,7),ky=q.height/484;
 return{f,sx:f*181,sy:0,sw:181,sh:576,ground:540,kx:q.height/484,ky,height:(540-HAMMER_SPIKE_TIPS[f])*ky};};
// Reactor positions and hands are measured on the native generated cells.
const HK5_HANDS=[[[.25,.69],[.82,.68]],[[.19,.65],[.76,.41]],[[.24,.70],[.89,.49]],[[.34,.18],[.78,.60]],
 [[.31,.16],[.72,.45]],[[.46,.83],[.78,.52]],[[.15,.42],[.76,.52]],[[.87,.49],[.25,.51]],
 [[.34,.18],[.70,.58]],[[.12,.43],[.83,.43]],[[.48,.80],[.69,.58]],[[.30,.58],[.87,.58]]];
// Hammer head coordinates relative to each SOURCE cell, not the body center.
const HK5_HEADS=[[310,239],[184,54],[183,30],[245,234],[299,232],[65,125],[44,148],[348,137],[351,145],[177,16],[203,217],[349,227],[309,232],[123,56],[63,138],[343,120]];
function hk5HammerFrame(h){const s=h?.state||'';if(h?.gp4Emergency||s==='fr_twirl')return h.t<1?13:14;
 if(s==='fr_activation'||s==='storm_raise'||s==='spell'||s==='mega_charge')return h.t<.4?1:2;
 if(s==='warn'||s==='storm_warn'||s==='giant_warn')return 1;
 if(s==='leap'||s==='giant_dive'||s==='storm_slam')return h.t<.16?9:10;
 if(s==='recover'||s==='giant_recover')return h.t<.24?3:4;
 if(['hammer_stun','storm_stun','fr_stun','hammer_exposed'].includes(s))return 11;
 if(s==='storm_rebuild')return 12;if(['spin','whirlwind','fr_twirl'].includes(s))return 14;
 if(s==='throw')return 15;if(s==='hkSideTell')return h.hkSide<0?5:7;if(s==='hkSideHit')return h.hkSide<0?6:8;return 0;}
function hk5KnightFrame(K){if(!K)return 0;const p=K.phase;
 if(p==='tell')return K.kind==='shieldCode'||K.kind==='shieldSmite'?1:3;
 if(p==='jump')return 4;if(p==='land')return 5;if(p==='followTell')return 3;
 if(p==='rise')return K.side<0?6:7;if(p==='active')return K.kind==='shieldSmite'?2:K.kind==='armageddon'?8:1;
 return K.kind==='leapSlash'?10:11;}
function hk5SideLane(b,h){const a=HK5_ART.hammer[h.hkSide<0?6:8];return{x:b.x,y:b.y+(a.head[1]-a.py*a.h)*.76,ex:b.x+(a.head[0]-a.px*a.w)*.76,width:80};}
function hk5Flight(T){const a=HK5_ART.hammer[16];if(!a||!XART.rdy(a.key))return;const w=a.w*.76,h=a.h*.76;
 ctx.save();ctx.translate(T.x,T.y);ctx.rotate(T.angle||0);ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),-a.px*w,-a.py*h,w,h);ctx.restore();}
fmcRig=function(b){if(!hk5Own(b))return HK5_BASE.rig.apply(this,arguments);const J=j3State(b),K=b._r30.hkKnight,h=J.gp4Donors?.[8]?.p._hammer;
 const hammer=J.mimic===8,f=hammer?hk5HammerFrame(h):hk5KnightFrame(K),a=HK5_ART[hammer?'hammer':'knight'][f],scale=hammer?.76:.68;
 const w=a.w*scale,hgt=a.h*scale,ax=b.x,ay=b.y,core=b.parts.find(p=>p.id==='core');
 const v={p:core,spec:{px:a.px,py:a.py,art:'pose',sheet:a.key,role:'core'},key:a.key,ax,ay,w,h:hgt,rot:0,alpha:1,z:1};
 Object.assign(v,fmcPoint(v,.5,.5));const out=[v];
 if(hammer){const p=b.parts.find(p=>p.id==='hammer');if(p&&!h?.throw&&!h?.hammerDestroyed){const point=HK5_HEADS[f];
  const x=ax+(a.head[0]-a.px*a.w)*scale,y=ay+(a.head[1]-a.py*a.h)*scale;
  out.push({p,spec:{px:.5,py:.5,role:'hammerHead',hidden:true},key:a.key,ax:x,ay:y,x,y,w:64,h:55,rot:0,alpha:1,z:5});}return out;}
 for(const [i,id]of ['sword','shield'].entries()){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed)continue;
  const charged=K&&((id==='shield'&&K.kind==='shieldCode')||(id==='sword'&&K.kind==='armageddon')),
   tool=HK5_ART.knight[(id==='sword'?12:13)+(charged?2:0)],hand=HK5_HANDS[f][i],x=b.x+(hand[0]-a.px)*w,y=b.y+(hand[1]-a.py)*hgt;
  let rot=id==='shield'?0:K&&['tell','followTell'].includes(K.phase)&&!K.kind.startsWith('shield')?Math.PI:K?.phase==='rise'?K.side*lerp(.25,Math.PI*.75,clamp(K.t/.5,0,1)):(K?.kind==='armageddon'?Math.PI:0);
  const n={p,spec:{px:.5,py:id==='sword'?.22:.5,art:'pose',sheet:tool.key,role:id},key:tool.key,ax:x,ay:y,w:id==='sword'?50:82,h:id==='sword'?115:114,rot,alpha:1,z:5};
  Object.assign(n,fmcPoint(n,.5,.5));out.push(n);
 }return out;};
r30Parts=function(b){if(!hk5Own(b))return HK5_BASE.parts.apply(this,arguments);return fmcRig(b).map(v=>v.p.id==='core'?{...v,x:b.x,y:b.y+25,w:145,h:155}:v);};
f1003bBodyDraw=function(b,alpha=1){if(!hk5Own(b))return HK5_BASE.body.apply(this,arguments);
 for(const v of fmcRig(b)){if(v.spec.hidden)continue;const a=FMC_ART[v.key];ctx.save();ctx.globalAlpha*=alpha;
  fmcCell(v.key,'pose',v.x,v.y,v.w,v.h,v.rot,1);const flash=Math.max(b.flash||0,v.p.flash||0);
  if(flash>0)fmcCell(v.key,'pose',v.x,v.y,v.w,v.h,v.rot,Math.min(1,flash*9),'#ffffff');
  ctx.restore();}
};
hammerHeadPoint=function(p){if(j3State(p?._gp4Host)?.mimic===8){if(p._hammer.throw)return{x:p._hammer.throw.x,y:p._hammer.throw.y};const v=fmcRig(p._gp4Host).find(v=>v.p.id==='hammer');if(v)return{x:v.x,y:v.y};}return HK5_BASE.head.apply(this,arguments);};
hammerGripPoint=function(p){if(j3State(p?._gp4Host)?.mimic===8)return{x:p._gp4Host.x+79.8,y:p._gp4Host.y-27.36};return HK5_BASE.grip.apply(this,arguments);};
function hk5AttackStart(b,kind){const S=b._r30;b.y=Math.max(b.y,PLAY.y+200);S.hkKnight={kind,phase:'tell',t:0,next:0,side:(S.hkKnightN||0)%2?-1:1,ox:b.x,oy:b.y,
 tx:clamp(player.x,camLeftX()+85,camRightX()-85),ty:clamp(player.y,PLAY.y+180,hammerWarningFloorY()-10),blade:null,hitSeats:new Set(),rows:[]};
 S.shield=0;S.on5Shield=null;r30Sound('bossWeaponCharge');hk5Log('knightAttack',{kind});}
function hk5Phase(K,phase){K.phase=phase;K.t=0;K.blade=null;K.hitSeats.clear();hk5Log('knightPhase',{kind:K.kind,phase});}
function hk5BladeHit(b,K){const L=fmcBlade(b);if(!L)return;const prev=K.blade||L;K.blade=L;
 for(const seat of seatList())withSeat(seat,()=>{if(K.hitSeats.has(seat)||player.dead)return;for(let i=0;i<=8;i++){
  const u=i/8,line={x:lerp(prev.x,L.x,u),y:lerp(prev.y,L.y,u),ex:lerp(prev.ex,L.ex,u),ey:lerp(prev.ey,L.ey,u)};
  if(s81003Distance(player.x,player.y,line)<L.width/2+5){playerHit('alien sword '+K.phase);K.hitSeats.add(seat);break;}}
 });}
function hk5EruptionShape(q){const u=q.t-q.tell;if(u<0||u>=q.active)return null;const f=u<.42?Math.min(3,Math.floor(u/.42*4)):u<.58?4:Math.min(7,5+Math.floor((u-.58)/.44*3));
 const reach=[.30,.64,.91,1,1,.83,.61,.22][f]*(q.ex-q.x);return{f,reach};}
function hk5Rows(b,K){const left=camLeftX(),right=camRightX(),bottom=hammerWarningFloorY()-2,top=PLAY.y+205;
 K.rows=Array.from({length:diffKey==='easy'||diffKey==='normal'?2:3},(_,i)=>{const side=(i+(K.side<0?1:0))%2?-1:1,y=lerp(top,bottom,i/(diffKey==='easy'||diffKey==='normal'?1:2));
  return{x:side<0?left+36:right-36,y,ex:side<0?right-20:left+20,side,t:-i*.95,tell:1.55,active:1.46,width:80,hitSeats:new Set()};});
 hk5Log('edgeWarnings',{rows:K.rows.map(q=>({x:q.x,y:q.y,ex:q.ex,side:q.side}))});}
function hk5KnightTick(b,D,dt){const S=b._r30;let K=S.hkKnight;
 if(!K){S.hkKnightCd=(S.hkKnightCd??1.2)-dt;if(S.hkKnightCd>0)return;
  const book=['leapSlash','shieldSmite','shieldCode','armageddon'];let kind=book[(S.hkKnightN||0)%4];S.hkKnightN=(S.hkKnightN||0)+1;
  if(kind.startsWith('shield')&&!fmcAlive(b,'shield'))kind='leapSlash';if(['leapSlash','armageddon'].includes(kind)&&!fmcAlive(b,'sword'))kind=fmcAlive(b,'shield')?'shieldCode':'coreCode';
  hk5AttackStart(b,kind);K=S.hkKnight;}
 K.t+=dt;const dur=K.kind==='armageddon'?2.2:1.15;
 if(K.phase==='tell'){combatWarningTick(b,'hk5-'+S.hkKnightN,K.t,dur);if(K.t>=dur){hk5Phase(K,K.kind==='leapSlash'?'jump':'active');if(K.kind==='armageddon')hk5Rows(b,K);r30Sound('combatAlien0927');}}
 else if(K.phase==='jump'){
  const u=clamp(K.t/.72,0,1);b.x=lerp(K.ox,K.tx,u);b.y=lerp(K.oy,K.ty-122,u)-Math.sin(u*Math.PI)*95;
  if(u>.80)hk5BladeHit(b,K);if(u>=1){hk5Phase(K,'land');r30Sound('hammerImpact');r30FX(b,K.tx,K.ty,85);}}
 else if(K.phase==='land'){hk5BladeHit(b,K);if(K.t>.18)hk5Phase(K,'followTell');}
 else if(K.phase==='followTell'){combatWarningTick(b,'hk5-rising-'+S.hkKnightN,K.t,.75);if(K.t>=.75)hk5Phase(K,'rise');}
 else if(K.phase==='rise'){b.y=K.ty-122-Math.sin(clamp(K.t/.5,0,1)*Math.PI/2)*48;hk5BladeHit(b,K);if(K.t>=.5)hk5Phase(K,'recover');}
 else if(K.phase==='active'){
  if(K.kind==='shieldSmite'){const u=clamp(K.t/1.1,0,1),v=Math.sin(u*Math.PI);b.x=lerp(K.ox,K.tx,v);b.y=lerp(K.oy,K.ty-40,v);
   const shield=fmcRig(b).find(v=>v.p.id==='shield');if(shield)for(const seat of seatList())withSeat(seat,()=>{if(!K.hitSeats.has(seat)&&Math.hypot(player.x-shield.x,player.y-shield.y)<53){playerHit('alien shield smite');K.hitSeats.add(seat);}});
   if(u>=1)hk5Phase(K,'recover');
  }else if(K.kind==='armageddon'){
   for(const q of K.rows){q.t+=dt;if(q.t>=0&&q.t<q.tell)combatWarningTick(q,'code-armageddon',q.t,q.tell);
    for(let i=0;i<3;i++){const node={...q,t:q.t-i*.22,active:1.02},A=hk5EruptionShape(node);if(!A)continue;
     if(!q.fired){q.fired=true;r30Sound('expBig');shake=Math.max(shake,4);}const x=lerp(q.x,q.ex,(i+1)/4),a=HK5_ART.effects[A.f],floor=q.y+36,height=(a.foot-a.top)*q.width;
     for(const seat of seatList())withSeat(seat,()=>{if(A.f>=1&&A.f<=6&&!K.hitSeats.has(seat)&&Math.abs(player.x-x)<28&&player.y<floor&&player.y>floor-height){playerHit('binary Armageddon');K.hitSeats.add(seat);}});
    }}if(K.rows.every(q=>q.t>=q.tell+q.active))hk5Phase(K,'recover');
  }else{
   if(K.t>=K.next){K.next=K.t+.55;const tool=fmcRig(b).find(v=>v.p.id==='shield'),m=tool||{x:b.x,y:b.y+45};
   const aim=Math.atan2(K.ty-m.y,K.tx-m.x);for(const off of [-.22,0,.22]){const q=eShootT(m.x,m.y,aim+off,3.8,'eglaser',{w:22,h:24});if(q){q._hkCodeFire=true;q._hkOwner=b;q.t=0;q.w=q.h=22;(S.hkShots??=[]).push(q);}}
    r30Sound('enemyBossCannon');}if(K.t>=2.25)hk5Phase(K,'recover');
  }
 }else if(K.phase==='recover'){const u=clamp(K.t/.8,0,1);b.x=lerp(b.x,K.ox,Math.min(1,dt*5));b.y=lerp(b.y,K.oy,Math.min(1,dt*5));if(u>=1){S.hkKnight=null;S.hkKnightCd=1.15;}}
 D.p.x=b.x;D.p.y=b.y;
}
gd4Tick=function(b,dt){const J=j3State(b);if(!hk5Own(b))return HK5_BASE.donor.apply(this,arguments);const S=b._r30,D=gd4Create(b,J.mimic),p=D.p;
 D.age+=dt;p.t+=dt;p.enter=p.dead=false;p.hp=b.hp;p.maxhp=b.maxhp;
 S.hkImpacts=(S.hkImpacts||[]).filter(q=>(q.t+=dt)<.4);S.hkShots=(S.hkShots||[]).filter(q=>{
  if(!q.dead&&eBullets.includes(q))return true;if(q.x>camLeftX()&&q.x<camRightX()&&q.y>PLAY.y&&q.y<hammerWarningFloorY()+36)S.hkImpacts.push({x:q.x,y:q.y,t:0});return false;});
 if(J.mimic===5)hk5KnightTick(b,D,dt);
 else{const h=p._hammer;
  // Regular source controller, including armor, restore/disarm, throws and 8% reserve.
  if(h.state==='hkSideTell'){h.t+=dt;h.hitCd=Math.max(0,(h.hitCd||0)-dt);combatWarningTick(p,'code-hammer-side',h.t,1.1);if(h.t>=1.1){h.hkSidePrev=hammerHeadPoint(p);hammerState(p,'hkSideHit');}}
  else if(h.state==='hkSideHit'){h.t+=dt;h.hitCd=Math.max(0,(h.hitCd||0)-dt);const v=fmcRig(b).find(v=>v.p.id==='hammer');if(v){const prev=h.hkSidePrev||v,line={x:prev.x,y:prev.y,ex:v.x,ey:v.y};h.hkSidePrev={x:v.x,y:v.y};for(const seat of seatList())withSeat(seat,()=>{
   if(h.hitCd<=0&&s81003Distance(player.x,player.y,line)<38){h.hitCd=.8;playerHit('alien sideways hammer');}});}
   if(h.t>=.42){h.hkSideCd=6;hammerState(p,'hammer');}}
  else{hammerBossTick(p,dt);h.hkSideCd=(h.hkSideCd??4)-dt;
   if(h.hkSideCd<=0&&h.state==='hammer'&&!h.gp4Emergency){h.hkSide=(h.hkSide||1)*-1;hammerState(p,'hkSideTell');}}
  b.x=p.x;b.y=p.y;b.hp=Math.max(0,p.hp);j3Health(b,b.hp,b.maxhp);b._noHit=p._noHit;const module=b.parts.find(q=>q.id==='hammer');module.hp=h.hammerHP;module.maxhp=h.hammerMax;module.destroyed=!!h.hammerDestroyed;
 }
 b._drawY=b.y;const mode=J.mimic===5?S.hkKnight?.phase||'idle':p._hammer.state;if(mode!==D.last){D.last=mode;D.history.push(mode);if(D.history.length>100)D.history.shift();}
 if(D.age>=(diffKey==='furious'?44:38)&&!(p._hammer?.gp4Emergency)&&!S.hkKnight){D.age=0;j3Morph(b,'home');}
};
modularHit=function(dmg){const b=boss,J=j3State(b);if(J?.mimic!==8||!r30Live(b))return HK5_BASE.hit.apply(this,arguments);
 if(!Number.isFinite(dmg)||dmg<=0)return;const D=gd4Create(b,8),p=D.p,h=p._hammer;p.hp=b.hp;p.maxhp=b.maxhp;
 p._hammerModuleHit=b._lastPart?.id==='hammer'?'hammer':null;const dealt=hammerBossDamage(p,dmg);b.hp=Math.max(0,p.hp-dealt);p.hp=b.hp;
 const module=b.parts.find(q=>q.id==='hammer');module.hp=h.hammerHP;module.destroyed=!!h.hammerDestroyed;module.flash=.12;markHit(b,.12);stageStats.dmgDealt+=dealt;
 j3Health(b,b.hp,b.maxhp);j3Save(b);if(!b.hp)r30Break(b);return dealt;
};
retinaBossTargets=function(b){if(j3State(b)?.mimic!==8)return HK5_BASE.targets.apply(this,arguments);if(!r30Live(b)||b._noHit)return[];
 const D=gd4Create(b,8);return r30Parts(b).filter(v=>v.p.id==='core'||hammerWeaponTargetable(D.p)).map(v=>retinaDynamicPiece(b,'code-hammer-'+v.p.id,v.p.id==='hammer'?'hammer':'alien module',()=>{
  const q=r30Parts(b).find(n=>n.p.id===v.p.id);return{x:q?.x??v.x,y:q?.y??v.y,hp:v.p.id==='core'?b.hp:D.p._hammer.hammerHP,dead:!q||!r30Live(b)||v.p.destroyed};
 },d=>{b._lastPart=v.p;hitBoss(d);},v.w*.8,v.h*.8));};
function hk5Warning(b,K){const u=clamp(K.t/(K.kind==='armageddon'?2.2:1.15),0,1);
 if(K.phase==='tell'){const tool=fmcRig(b).find(v=>v.p.id===(K.kind.startsWith('shield')?'shield':'sword'));
  if(tool){ctx.save();ctx.globalCompositeOperation='lighter';fmcCell(tool.key,'pose',tool.x,tool.y,tool.w,tool.h,tool.rot,.20+.25*Math.sin(K.t*13)**2);ctx.restore();}
  if(K.kind!=='armageddon')combatWarningDraw(b,{x:b.x,y:b.y,ex:K.tx,ey:K.ty,width:K.kind==='leapSlash'?95:75,progress:u});
 }if(K.phase==='followTell')combatWarningDraw(b,{x:b.x-110,y:K.ty-30,ex:b.x+110,ey:K.ty-30,width:65,progress:clamp(K.t/.75,0,1)});
 for(const q of K.rows||[]){if(q.t<0)continue;if(q.t<q.tell){const progress=q.t/q.tell;
  groundTargetReticleDraw(q.x,q.y,72,progress,.9);combatWarningDraw(q,{x:q.x,y:q.y,ex:q.ex,ey:q.y,width:q.width,progress});
  // Mandatory direction glyph: arrows originate on the actual edge Retina.
  campText(q.side<0?'>>>':'<<<',q.x+(q.side<0?47:-47),q.y-9,13,'#ffdb91');HK5.draws.edgeArrow=(HK5.draws.edgeArrow||0)+1;
 }for(let i=0;i<3;i++){const node={...q,t:q.t-i*.22,active:1.02},A=hk5EruptionShape(node);if(A){const a=HK5_ART.effects[A.f],x=lerp(q.x,q.ex,(i+1)/4);
   hk5Cell(a,x,q.y+36-(a.foot-.5)*q.width,72,q.width);}}}
}
r30DrawBoss=function(b){if(!hk5Own(b)||b._r30.mode!=='fight')return HK5_BASE.draw.apply(this,arguments);
 const J=j3State(b),D=J.gp4Donors?.[J.mimic];if(J.mimic===8&&D)hammerBossAtmosphereDraw(D.p);f1003bBodyDraw(b);if(J.mimic===5){const K=b._r30.hkKnight;if(K)hk5Warning(b,K);for(const q of b._r30.hkImpacts||[])hk5Cell(HK5_ART.effects[12+Math.min(3,Math.floor(q.t/.4*4))],q.x,q.y,80,80);return;}
 if(!D)return;const p=D.p,h=p._hammer,s=h.state;
 if(s==='hkSideTell'){const q=hk5SideLane(b,h);combatWarningDraw(p,{...q,ey:q.y,progress:clamp(h.t/1.1,0,1)});}
 else if(s==='warn')combatWarningDraw(p,{x:b.x,y:b.y,ex:h.tx,ey:h.ty,width:70,progress:clamp(h.t/1.1,0,1)});
 if(s==='giant_warn'){const k=clamp(h.t/1.1,0,1);combatWarningDraw(p,{x:b.x,y:b.y,ex:h.tx,ey:h.ty,progress:k,width:150});groundTargetReticleDraw(h.tx,h.ty,230,k,.85);}
 if(['whirl_warn','whirl_turn'].includes(s)&&h.whirl){const w=h.whirl;combatWarningDraw(p,{x:w.startX,y:w.y+36,ex:w.endX,ey:w.y+36,progress:clamp(h.t/w.warm,0,1),width:208});}
 if(['storm_warn','storm_slam'].includes(s)&&h.stormTarget){const warm=hammerFurious()?.9:hammerHard()?1:1.15,k=s==='storm_slam'?1:clamp(h.t/warm,0,1),q=h.stormTarget;
  groundTargetReticleDraw(q.x,q.y,125,k,.95);if(s==='storm_warn')combatWarningDraw(p,{x:b.x,y:b.y,ex:q.x,ey:q.y,progress:k,width:108});}
 if(s==='curl'&&h.ballWarn){const q=hammerBallLaunchPath(p);combatWarningDraw(p,{x:q.x,y:q.y,ex:q.ex,ey:q.ey,width:112,progress:clamp(h.t/HAMMER_BALL_WARN,0,1)});}
 if(s==='uzi'&&h.t<.75)combatWarningDraw(p,{x:b.x,y:b.y+8,ex:h.uziAimX??player.x,ey:h.uziAimY||player.y,width:64,progress:clamp(h.t/.75,0,1)});
 if(['chaingun_draw','chain_warn','chaingun','chain_cool'].includes(s)){if(s==='chain_warn'){const m=hammerBlasterMount(p),warm=hammerFurious()?.65:hammerHard()?.75:.85;combatWarningDraw(p,{x:m.x,y:m.muzzleY,ex:m.x,ey:hammerWarningFloorY(),width:44,progress:clamp(h.t/warm,0,1)});}hammerBlasterGunDraw(p,s==='chaingun_draw'?clamp((h.t/2-.35)/.25,0,1):1);}
 if(s==='fr_twirl'&&h.t<2.2)combatWarningDraw(p,{x:b.x,y:b.y+65,ex:b.x,ey:hammerWarningFloorY(),width:260,progress:h.t/2.2});
 if(['fr_stun','hammer_stun','storm_stun'].includes(s)){hammerStunEffectsDraw(p);hammerRecoveryBurstDraw(p);}
 if(s==='mega_charge')combatWarningDraw(p,{x:b.x,y:b.y-20,ex:b.x,ey:hammerWarningFloorY(),width:hammerEradWidth(),progress:clamp(h.t/1.65,0,1)});
 if(s==='mega_beam')hammerChromiumDraw(b.x,hammerWarningFloorY(),b.y-20,hammerEradWidth(),h.t,hammerEradDuration());
 if(['spell','spell_blast'].includes(s))for(const q of s==='spell'?h.spellTargets:h.pillars){groundTargetReticleDraw(q.x,hammerWarningFloorY(),72,clamp(h.t/2.35,0,1),.9);if(s==='spell_blast')hammerChromiumDraw(q.x,hammerWarningFloorY(),PLAY.y,44,h.t,1.35);}
 for(const q of h.stormWaves||[]){hammerStormRedZoneDraw(q);hammerStormRowRetinaDraw(q);hammerStormSpikeDraw(q);hammerStormRowAlertDraw(q);}
 if(h.throw)hk5Flight(h.throw);
 if(h.gp4Emergency||s==='fr_activation'||s==='storm_raise'){
  const m=hammerHeadPoint(p);archEffectBlit(9,m.x,m.y,80,h.t*4,1);combatWarningDraw(p,{x:m.x,y:PLAY.y,ex:m.x,ey:m.y,width:18,progress:clamp(h.t/2,0,1)});}
 if(h.frArmor?.barrier>0){const y=b.y+85;cwdCell('wall',0,b.x,y,300,45,1,0,'red');}
};
fmcGauge=function(b){const q=HK5_BASE.gauge.apply(this,arguments),D=j3State(b)?.mimic===8?j3State(b).gp4Donors?.[8]:null,A=D?.p._hammer.frArmor;
 if(A?.hp>0&&b._r30.mode==='fight')return{charge:-1,color:'#dee8f1',under:'#ff3545',frac:A.hp/A.max};return q;};
j3Clear=function(b){if(b?._r30){b._r30.hkKnight=null;b._r30.hkKnightCd=1.2;b._r30.hkShots=[];b._r30.hkImpacts=[];}eBullets=eBullets.filter(q=>q._hkOwner!==b);return HK5_BASE.clear.apply(this,arguments);};
drawBullets=function(){const saved=eBullets,own=saved.filter(q=>q._hkCodeFire&&!q.dead);eBullets=saved.filter(q=>!q._hkCodeFire);
 try{HK5_BASE.bullets.apply(this,arguments);}finally{eBullets=saved;}
 for(const q of own){const f=8+(Math.floor((q.t||0)*13)%4);hk5Cell(HK5_ART.effects[f],q.x,q.y,48,55,Math.atan2(q.vy,q.vx)-Math.PI/2);}
};
