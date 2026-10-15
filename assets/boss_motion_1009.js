"use strict";
/* Mike's filmed direction: authored acting, measured joints and committed strikes.
   These replacements use the existing encounter owners, HP and module lifetimes. */
const BM9={version:1,events:[],draws:{},base:{begin:beginStage,load:stageLoadBegin,deathDraw:fb1002HammerDeathDraw,
 deathTick:hammerBossDeathTick,stormTarget:hammerStormTarget,stormImpact:hammerStormImpact,
 stormTick:hammerStormTick,stormDraw:hammerStormDraw,stormFloor:hammerStormFloorY,head:hammerHeadPoint,
 dracula:aa5DraculaTick,parts:r30Parts,claw:cf4Claw,draw:r30DrawBoss,
 s7Cell:s7mCell,s7Pose:s7mPose,s7Tick:s7mTick,s7Draw:s7mDraw,s7Set:s7mSet,s7Next:s7mNext,
 s7Warnings:s7mWarnings,shape:mr27Shape,moduleTick:mr27Tick,moduleDraw:mr27Draw,helperDraw:mr27HelperDraw}};
for(const frames of Object.values(BM9_ART))for(const a of frames)XART._src[a.key]=a.path;
function bm9Log(event,data={}){BM9.events.push({event,...data});if(BM9.events.length>240)BM9.events.shift();}
function bm9Warm(names){for(const name of names)for(const a of BM9_ART[name])XART.rdy(a.key);}
function bm9StageNames(n){return n===5?['hammer_death','hammer_counter']:n===7?['spider_claws','spider_legs','landing','turret_charge']:
 n===8?['dracodia_arms','dracodia_core']:n===3||n===4?['turret_charge']:[];}
stageLoadBegin=function(n,keys){const added=bm9StageNames(n).flatMap(name=>BM9_ART[name].map(a=>a.key));
 return BM9.base.load.call(this,n,[...(keys||[]),...added]);};
beginStage=function(n){const r=BM9.base.begin.apply(this,arguments);BM9.events=[];bm9Warm(bm9StageNames(n));return r;};
function bm9Point(a,point,x,y,k,rot=0){const dx=(point[0]-a.pivot[0])*k,dy=(point[1]-a.pivot[1])*k,c=Math.cos(rot),s=Math.sin(rot);return{x:x+dx*c-dy*s,y:y+dx*s+dy*c};}
function bm9Geometry(name,i,x,y,k,rot=0){const a=BM9_ART[name][i],q=bm9Point(a,[a.w/2,a.h/2],x,y,k,rot);
 return{...q,w:a.w*k,h:a.h*k,rot,key:a.key,bm9Tip:bm9Point(a,a.tip,x,y,k,rot),bm9Frame:i};}
function bm9Draw(name,i,x,y,k,rot=0,flash=0){const a=BM9_ART[name][i];if(!XART.rdy(a.key))return false;
 const im=flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key);if(!im)return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 BM9.draws[name]=(BM9.draws[name]||0)+1;return true;}
function bm9HitPath(from,to,width,label){const L={x:from.x,y:from.y,ex:to.x,ey:to.y,width};
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,L)<width/2+3)playerHit(label);});}

/* The approved death acts before it ruptures. Every intact cell has two arms,
   two legs and the same seated head. Cutaways still follow the in-engine death. */
fb1002HammerDeathDraw=function(b){
 if(!fb1002NormalHammer(b)||!XART.rdy(BM9_ART.hammer_death[0].key))return BM9.base.deathDraw(b);
 const t=b.dying||0,f=t<.55?0:t<1.15?1:t<1.75?2:t<2.30?3:t<2.85?4:t<3.7?5:t<4.85?6:7;
 if(t<5.55)bm9Draw('hammer_death',f,b.x+17+Math.sin(t*41)*Math.max(0,t-2.8),b.y-26,.57);
 for(const q of b._hammer.deathFx1002||[]){const age=t-q.at;if(age>=0&&age<.9)fb1002Cell('electrical',Math.min(15,Math.floor(age/.9*16)),q.x,q.y,q.size,q.size,null,0,1);}
 for(let i=0;i<8;i++){const age=t-4.85-i*.10;if(age>=0&&age<1.25){const x=b.x+17+Math.sin(i*2.4)*90,y=b.y+Math.cos(i*1.7)*75;
  efxFrame('efx_burst_fire',Math.min(7,Math.floor(age/1.25*8)),x-60,y-60,120,120,1);}}
};
hammerBossDeathTick=function(b,dt){const r=BM9.base.deathTick.apply(this,arguments);
 if(fb1002NormalHammer(b)&&b.dying>=4.85&&!b._hammer.bm9Rupture){b._hammer.bm9Rupture=true;
  spawnShockRing(b.x,b.y,220,'fire');Audio.SFX.expBig?.();bm9Log('hammer-authored-rupture',{t:b.dying});}
 return r;};

/* Bottom storm: Retina, preview and spike volume now agree on one bottom band.
   Escape upward earns space, then one fully warned shoulder-height counter. */
hammerStormFloorY=function(){return fb1002NormalHammer(boss)?PLAY.y+PLAY.h-6:BM9.base.stormFloor();};
function bm9StormTop(){return hammerStormFloorY()-Math.min(185,PLAY.h*.36);}
hammerStormTarget=function(b){const r=BM9.base.stormTarget.apply(this,arguments);if(fb1002NormalHammer(b)){
 b._hammer.stormTarget.y=hammerStormFloorY()-12;b._hammer.stormBounds.top=bm9StormTop();b._hammer.stormBounds.bottom=hammerStormFloorY();}return r;};
hammerStormImpact=function(b){const r=BM9.base.stormImpact.apply(this,arguments);if(fb1002NormalHammer(b)){
 const h=b._hammer;h.bm9Counter=null;h.bm9CounterDone=false;
 for(const q of h.stormWaves||[]){q.y=hammerStormFloorY();q.height=hammerStormFloorY()-bm9StormTop();q.radius=9;q.bm9Bottom=true;}
 bm9Log('bottom-spike-zone',{top:bm9StormTop(),bottom:hammerStormFloorY()});}return r;};
function bm9CounterFrame(C){return(C.side>0?0:4)+(C.t<.35?0:C.t<C.tell?1:C.t<C.tell+.22?2:3);}
function bm9CounterHead(b,C,f=bm9CounterFrame(C)){return bm9Geometry('hammer_counter',f,b.x,b.y-26,.60).bm9Tip;}
hammerHeadPoint=function(b){const C=b?._hammer?.bm9Counter;return C?bm9CounterHead(b,C):BM9.base.head.apply(this,arguments);};
hammerStormTick=function(b,dt){const h=b._hammer,C=h.bm9Counter;
 if(C&&fb1002NormalHammer(b)){
  if(h.state!=='storm_split'||h.hammerDestroyed){h.bm9Counter=null;return BM9.base.stormTick.apply(this,arguments);}
  C.t+=dt;hammerStormWaveTick(b,dt);
  if(C.t<C.tell){const u=clamp(C.t/C.tell,0,1),e=u*u*(3-2*u);b.x=lerp(C.ox,C.tx,e);b.y=lerp(C.oy,C.ty,e);
   combatWarningTick(C,'hammer-side-counter',C.t,C.tell);}
  else if(C.t<C.tell+.40){const q=bm9CounterHead(b,C);if(!C.fired){C.fired=true;C.previous=bm9CounterHead(b,C,(C.side>0?0:4)+1);Audio.SFX.hammerThrow?.();}
   bm9HitPath(C.previous,q,38,'Hammer horizontal counter');C.previous=q;}
  if(C.t>C.tell+1.15){h.bm9Counter=null;h.bm9CounterDone=true;
   const home=h.stormHome||{x:worldWidth()/2,y:VH*.34};h.stormRecovery={ox:b.x,oy:b.y,x:home.x,y:home.y,depart:h.t,duration:.9,done:false};}
  return true;
 }
 const r=BM9.base.stormTick.apply(this,arguments);
 if(fb1002NormalHammer(b)&&h.state==='storm_split'&&h.t>.95&&!h.bm9CounterDone&&player.y<bm9StormTop()-18&&!h.hammerDestroyed){
  const side=player.x>=b.x?1:-1;h.bm9Counter={t:0,tell:hammerFurious()?1.35:1.6,side,ox:b.x,oy:b.y,
   tx:clamp(player.x-side*130,camLeftX()+75,camRightX()-75),ty:clamp(player.y+13,PLAY.y+135,bm9StormTop()-40)};
  bm9Log('hammer-upper-counter',{side});Audio.SFX.bossWeaponCharge?.();}
 return r;
};
hammerStormDraw=function(b){const C=b?._hammer?.bm9Counter;if(!C)return BM9.base.stormDraw.apply(this,arguments);
 bm9Draw('hammer_counter',bm9CounterFrame(C),b.x,b.y-26,.60,0,b.flash||0);
 if(C.t<C.tell){const a=bm9CounterHead(b,C,(C.side>0?0:4)+1),z=bm9CounterHead(b,C,(C.side>0?0:4)+2);
  combatWarningDraw(C,{x:a.x,y:a.y,ex:z.x,ey:z.y,width:38,progress:C.t/C.tell,laneShape:'line'});}
 for(const q of b._hammer.stormWaves||[]){hammerStormRedZoneDraw(q);hammerStormRowRetinaDraw(q);hammerStormSpikeDraw(q);hammerStormRowAlertDraw(q);}return true;};

/* Dracodia's own body form: physical alternating claws replace its old volley
   substitutions. Existing Court/Void spells and all eight saved pools survive. */
function bm9DraculaBeat(P){const beat=Math.min(P.count-1,Math.floor(P.t/P.cycle)),local=P.t-beat*P.cycle;
 return{beat,local,id:P.ids[beat%P.ids.length],frame:local<P.tell?1:local<P.tell+.24?2:3,live:local>=P.tell&&local<P.tell+.38};}
aa5DraculaTick=function(b,dt){const S=b._r30,J=j3State(b),old=S.attack,bookSize=['hard','furious','insanity'].includes(diffKey)?5:4;
 if(old&&!old.bm9||!old&&([2,3].includes(J.attacks)||J.attacks>=bookSize))return BM9.base.dracula.apply(this,arguments);
 j3Timers(b,dt);b.enter=false;
 if(!S.attack){S.cd-=dt;if(S.cd>0){on5ShieldTick(b,dt);return;}
  const ids=b.parts.filter(p=>p.id!=='core'&&!p.destroyed&&p.hp>0).map(p=>p.id);
  if(!ids.length){J.attacks=2;return;}
  const low=b.hp/(J.max[J.active]||b.maxhp)<.5,rank=r30Difficulty(),count=low?(rank>0?4:3):2,tell=low?1.05:1.30;
  S.attack={type:'bm9Swipe',bm9:true,aa5Court:true,t:0,tell,cycle:tell+.38+.65,count,ids,
   low,tx:clamp(player.x,camLeftX()+105,camRightX()-105),ty:clamp(player.y-150,PLAY.y+160,VH*.50),
   fromX:b.x,fromY:b.y,beat:-1,previous:null};J.attacks++;S.seq++;
  r30Sound('bossWeaponCharge');r30Sound('combatAlien0927');bm9Log('dracodia-claw-combo',{low,count,formHP:b.hp});}
 const P=S.attack;P.t+=dt;const Q=bm9DraculaBeat(P);
 if(Q.beat!==P.beat){P.beat=Q.beat;P.previous=null;P.fired=false;r30Sound('bossWeaponCharge');}
 if(Q.local<P.tell){const e=clamp(Q.local/(P.tell-.30),0,1);b.x=lerp(b.x,P.tx,Math.min(1,dt*3)*e);b.y=lerp(b.y,P.ty,Math.min(1,dt*3)*e);
  combatWarningTick(P,'dracodia-physical-'+S.seq+'-'+Q.beat,Q.local,P.tell);}
 const v=r30Parts(b).find(v=>v.p.id===Q.id);
 if(v&&Q.live){const tip=cf4Claw(v);if(!P.fired){P.fired=true;r30Sound('hammerImpact');}
  bm9HitPath(P.previous||tip,tip,42,'Dracodia claw');P.previous=tip;
 }else if(v)P.previous=cf4Claw(v);
 if(P.t>=P.count*P.cycle){S.attack=null;S.cd=1.05;bm9Log('dracodia-claw-recovery');}
 on5ShieldTick(b,dt);j3Save(b);
};
r30Parts=function(b){const P=b?._r30?.attack;if(!P?.bm9)return BM9.base.parts.apply(this,arguments);
 const out=BM9.base.parts(b),Q=bm9DraculaBeat(P),k=Math.min(1.12,viewW()/530),side=Q.id==='left'?-1:1;
 for(let i=0;i<out.length;i++){const v=out[i];if(v.p.id==='core'){
   const frame=Q.local<.24?0:Q.local<.55?1:Q.local<P.tell-.30?2:Q.local<P.tell?3:Q.live?(side<0?4:5):Q.local<P.tell+.65?6:7;
   if(XART.rdy(BM9_ART.dracodia_core[frame].key))v.key=BM9_ART.dracodia_core[frame].key;
   v.rot=Math.sin(clamp((Q.local-P.tell)/.38,0,1)*Math.PI)*side*.10;continue;}
  const s=v.p.id==='left'?-1:1,active=v.p.id===Q.id,frame=(s<0?0:4)+(active?Q.frame:0),rot=active?s*(Q.local<P.tell?-.17:.20*Math.sin(clamp((Q.local-P.tell)/.38,0,1)*Math.PI)):0;
  out[i]={...bm9Geometry('dracodia_arms',frame,b.x+s*102*k,b.y-48*k,.60*k,rot),p:v.p,alpha:1};}
 return out;};
cf4Claw=function(v){return v.bm9Tip||BM9.base.claw.apply(this,arguments);};
r30DrawBoss=function(b){const P=b?._r30?.attack;if(!P?.bm9)return BM9.base.draw.apply(this,arguments);
 j3Body(b);const Q=bm9DraculaBeat(P);if(Q.local<P.tell){const v=r30Parts(b).find(v=>v.p.id===Q.id);if(v){const s=Q.id==='left'?-1:1,k=Math.min(1.12,viewW()/530),f=(s<0?0:4)+2;
   const z=bm9Geometry('dracodia_arms',f,b.x+s*102*k,b.y-48*k,.60*k,s*.20).bm9Tip,a=cf4Claw(v);
   combatWarningDraw(P,{x:a.x,y:a.y,ex:z.x,ey:z.y,width:42,progress:Q.local/P.tell,laneShape:'line'});}}
};

/* Warden's authored front claws and rear leg bends retain the exact independent
   module ownership. Native part poses feed drawing, hits, emitters and Retina. */
s7mCell=function(name,i,trim){if(typeof i==='string'&&i.startsWith('bm9_'))return XART.rdy(i)?XART.get(i):null;return BM9.base.s7Cell.apply(this,arguments);};
function bm9S7Pose(p,name,f,x,y,k,a){const q=bm9Geometry(name,f,x,y,k,a);return{...p,cell:q.key,x:q.x,y:q.y,w:q.w,h:q.h,a:q.rot,bm9Tip:q.bm9Tip};}
s7mPose=function(b){const out=BM9.base.s7Pose(b),M=b._s7mod;if(!M||M.tank)return out;
 for(let i=0;i<out.length;i++){const p=out[i],s=p.id.endsWith('L')?-1:1;
  if(p.id.startsWith('front')&&(M.mode.startsWith('swipe')||M.mode==='jump')){
   const live=M.mode==='swipeX'||M.mode===(s<0?'swipeL':'swipeR'),local=M.t-M.warn,
    f=(s<0?0:4)+(M.mode==='jump'?(M.t<.26?1:0):!live?0:local<0?1:local<.24?2:3);
   out[i]=bm9S7Pose(p,'spider_claws',f,s*65,-14,.28,live&&local>=0?s*.18:0);
  }else if(p.id.startsWith('rear')&&M.mode==='jump'){
   const f=(s<0?0:4)+(M.t<.26?0:M.t<M.warn-.68?1:M.t<M.warn?2:3);
   out[i]=bm9S7Pose(p,'spider_legs',f,s*65,-78,.28,-s*.45);
  }else if(p.id.startsWith('gun')&&M.mode==='battery1009'){
   const converge=clamp(M.t/.65,0,1);p.x=s*lerp(34,12,converge);p.a=clamp(M.aim-Math.PI/2,-.62,.62);
   const kick=(M.bm9Kick?.[p.id]||0);p.x+=Math.sin(p.a)*kick*7;p.y-=Math.cos(p.a)*kick*7;
  }}return out;};
s7mSet=function(b,mode){const r=BM9.base.s7Set.apply(this,arguments),M=b._s7mod;if(M&&!M.tank){
 if(mode.startsWith('swipe')){M.warn=diffKey==='easy'?1.4:1.1;M.live=.38;M.bm9Previous={};}
 if(mode==='battery1009'){M.warn=1.65;M.live=2.45;M.bm9Kick={};M.bm9Aim=M.aim;M.bm9Side=player.x<b.x?-1:1;Audio.SFX.bossWeaponCharge?.();}
 }return r;};
s7mNext=function(b){const M=b._s7mod;if(M&&!M.tank&&!M.frExit){M.bm9Pick=(M.bm9Pick||0)+1;
 if(M.bm9Pick%3===1&&s7mLive(M,'front').length){s7mSet(b,'swipeX');return;}
 if(M.bm9Pick%3===2&&s7mLive(M,'gun').length){s7mSet(b,'battery1009');return;}}
 return BM9.base.s7Next.apply(this,arguments);};
function bm9S7Common(b,dt){const M=b._s7mod;M.t+=dt;M.clock+=dt;M.shotCD-=dt;M.counter=Math.max(0,M.counter-dt);
 M.coreFlash=Math.max(0,(M.coreFlash||0)-dt);M.shieldFlash=Math.max(0,(M.shieldFlash||0)-dt);for(const p of M.parts)p.flash=Math.max(0,p.flash-dt);
 if(b._s7warden){b._s7warden.noHit=false;b._s7warden.final.phase='fight';b._s7warden.final.t=M.t;}b._s7FinalNoBar=false;}
s7mTick=function(b,dt){const M=b?._s7mod;
 if(M?.bm9Landing){M.bm9Landing.t+=dt;if(M.bm9Landing.t>1.1)M.bm9Landing=null;}
 if(!M||M.tank||M.frExit||M.mode==='dead')return BM9.base.s7Tick.apply(this,arguments);
 if(M.mode.startsWith('swipe')){
  bm9S7Common(b,dt);const ids=s7mLive(M,'front').filter(p=>M.mode==='swipeX'||M.mode===(p.id==='frontL'?'swipeL':'swipeR')).map(p=>p.id);
  if(!ids.length){s7mSet(b,'recover');return true;}
  const u=M.t-M.warn;M.lean=Math.sin(clamp(u/.38,0,1)*Math.PI)*.12*(M.mode==='swipeR'?1:-1);
  if(u<0)combatWarningTick(b,'warden-authored-claw',M.t,M.warn);
  for(const p of s7mPose(b).filter(p=>ids.includes(p.id))){const tip=s7mWorld(b,{x:p.bm9Tip.x,y:p.bm9Tip.y});
   if(u>=0&&u<.38){if(!M.shot){M.shot=1;s7mSound('hammerThrow');}bm9HitPath(M.bm9Previous[p.id]||tip,tip,26,'Warden mechanical claw');}
   M.bm9Previous[p.id]=tip;}
  if(u>.38+.65){M.lean=0;s7mSet(b,M.mode==='swipeL'&&s7mLive(M,'front').some(p=>p.id==='frontR')?'swipeR':M.mode==='swipeR'?'swipeX':'jump');}return true;
 }
 if(M.mode==='battery1009'){
  bm9S7Common(b,dt);const guns=s7mLive(M,'gun');if(!guns.length){s7mSet(b,'recover');return true;}
  M.lean=lerp(M.lean,M.bm9Side*.16,Math.min(1,dt*4));for(const id of Object.keys(M.bm9Kick))M.bm9Kick[id]=Math.max(0,M.bm9Kick[id]-dt*9);
  if(M.t<M.warn){combatWarningTick(b,'warden-battery',M.t,M.warn);}
  else if(M.t<M.warn+M.live&&M.shotCD<=0){const gun=guns[M.shot%guns.length],q=s7mMuzzle(b,gun.id);M.shot++;M.bm9Kick[gun.id]=1;
   M.shotCD=M.shot%6===0?.32:M.n===2?.105:.15;s7mShot(b,q.x,q.y,q.a,4.7+M.n*.3,'gun');s7mSound('machineGun');
   navalFlash(null,q,.65,'weapon_muzzle_rotary',{n:4,hpx:29,life:.10,follow:()=>s7mMuzzle(b,gun.id)});}
  if(M.t>M.warn+M.live+.9){M.lean=0;s7mSet(b,s7mLive(M,'front').length?'swipeX':'recover');}return true;
 }
 const prior=M.mode,t=M.t,r=BM9.base.s7Tick.apply(this,arguments);
 if(prior==='jump'&&M.mode==='jump'){
  if(M.t<.26)M.height=0;else if(M.t<1.0)M.height=560*Math.sin((M.t-.26)/.74*Math.PI/2);
  if(t<M.warn&&M.t>=M.warn){M.bm9Landing={x:M.target.x,y:M.target.y+55,t:0};bm9Log('warden-gravel-landing');}}
 return r;
};
s7mWarnings=function(front){const saved=[];for(const b of [boss,subBoss]){const M=b?._s7mod;if(M&&!M.tank&&M.mode.startsWith('swipe')){saved.push([M,M.mode]);M.mode='bm9-claw-warning';}}
 try{BM9.base.s7Warnings(front);}finally{for(const [M,mode] of saved)M.mode=mode;}
 for(const b of [boss,subBoss]){const M=b?._s7mod;if(!M||M.tank||b.dead||M.t>=M.warn)continue;
  if(M.mode.startsWith('swipe'))for(const p of s7mPose(b).filter(p=>p.id.startsWith('front')&&s7mLive(M,'front').some(q=>q.id===p.id)&&
    (M.mode==='swipeX'||M.mode===(p.id==='frontL'?'swipeL':'swipeR')))){
   const s=p.id==='frontL'?-1:1,a=s7mWorld(b,p.bm9Tip),q=bm9Geometry('spider_claws',(s<0?0:4)+2,s*65,-14,.28,s*.18),z=s7mWorld(b,q.bm9Tip);
   combatWarningDraw(b,{x:a.x,y:a.y,ex:z.x,ey:z.y,width:26,progress:M.t/M.warn,laneShape:'line',fieldOnly:!front,alertOnly:front});}
  if(M.mode==='battery1009')for(const gun of s7mLive(M,'gun')){const q=s7mMuzzle(b,gun.id);
   combatWarningDraw(b,{x:q.x,y:q.y,ex:q.x+Math.cos(q.a)*600,ey:q.y+Math.sin(q.a)*600,width:28,progress:M.t/M.warn,fieldOnly:!front,alertOnly:front});}
 }
};
s7mDraw=function(b){const r=BM9.base.s7Draw.apply(this,arguments),M=b?._s7mod;if(M?.bm9Landing){const q=M.bm9Landing;bm9Draw('landing',Math.min(7,Math.floor(q.t/1.1*8)),q.x,q.y,.44);}
 if(M?.mode==='battery1009'&&M.t<M.warn)for(const p of s7mLive(M,'gun')){const q=s7mMuzzle(b,p.id);bm9Charge(q,M.t/M.warn,M.clock,'gold',48);}
 return r;};

/* Charge and recoil augment the existing Stage 3/4 fire controllers. No second
   projectile director, no changed revival count and no new shootable pellets. */
function bm9Turrets(b){return !!b?._mr27&&['frostcruiser','cryospear','stormsovereign','olivewarden'].includes(b._ship);}
mr27Shape=function(b,id){const q=BM9.base.shape.apply(this,arguments),p=mr27Part(b,id);if(bm9Turrets(b)&&id.startsWith('gun')){
 const kick=p?.recoil||0;q.y+=kick*3;q.x+=Math.sin(q.rot)*kick*8;q.y-=Math.cos(q.rot)*kick*8;}return q;};
mr27Tick=function(b,dt){const r=BM9.base.moduleTick.apply(this,arguments);if(bm9Turrets(b)&&b._er26?.mode==='hc-relay1007'){
 for(const L of b._hc1007?.lines||[]){const p=mr27Part(b,L.id==='L'?'gunL':'gunR');if(p&&!p.dead)p.rot=L.angle-Math.PI/2;}}return r;};
function bm9Charge(q,progress,t,color,size){const row=color==='ice'?4:0,f=row+Math.min(3,Math.floor(clamp(progress,0,.999)*4));
 ctx.save();ctx.globalCompositeOperation='lighter';bm9Draw('turret_charge',f,q.x,q.y,size/443,t*2.5);ctx.restore();}
mr27Draw=function(b){const r=BM9.base.moduleDraw.apply(this,arguments);if(!bm9Turrets(b)||b.dead||b.enter||b._s4war?.shield?.rearming)return r;
 const R=b._er26,H=b._hc1007;if(!R||R.mode==='recover')return r;
 const slots=['L','R'];for(const slot of slots){if(!mr27CanFire(b,slot))continue;const L=H?.lines?.find(q=>q.id===slot),age=L?H.age-L.delay:R.t,warm=L?H.warm:R.warm;
  if(age<0||age>=warm||!(warm>0))continue;const q=shipBossMount(b,slot),p=clamp(age/warm,0,1),color=run.stage===3?'ice':'gold',mini=b===subBoss;
  bm9Charge(q,p,b.t||0,color,mini?30:47);const T=L?H.target:R.s3kAim||R.target||player;
  groundTargetReticleDraw(T.x,T.y,mini?42:65,p,.70);}
 return r;};
mr27HelperDraw=function(b,d){const r=BM9.base.helperDraw.apply(this,arguments);if(bm9Turrets(b)&&!d.dead&&d.state==='windup'&&!mr27HelperState(d).dead){
 const q=stage4CoreTurretTip(d,d.barrelNext||1);bm9Charge(q,clamp(d.stateT/.8,0,1),d.stateT,'gold',36);}return r;};
