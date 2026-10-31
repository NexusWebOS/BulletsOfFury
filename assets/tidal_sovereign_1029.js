'use strict';
/* TS58: immediate water Sovereign; actual sockets, liquid charge, finite water turns. */
const TS58={events:[],owners:new Set(),serial:0,base:{bossSpawn:spawnBoss,init:s9FusionBossInit,tick:s9FusionBossTick,draw:shipBossDraw,mount:shipBossMount,hit:hitBoss,test:bossHitTest,clamp:er26DamageClamp,targets:retinaBossTargets,load:stageLoadBegin,update:updatePlay,projectile:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,rules:s3kOrdnanceRules,spawn:spawnEnemy,enemy:s8MegaTick,enemyDraw:drawEnemy,ready:target17Ready}};
for(const[n,a]of Object.entries(TS58_ART)){ER28_ART['ts58_'+n]=a;XART._src[a.key]=a.path;}
// Separate countdown gate: the global .90s alertDanger gate skips the .75s middle warning.
for(const [key,uri,g,min]of [
 ['tidalWaterWave','assets/game/levels/stage_09/boss/tidal_sovereign_1029/audio/tidal_wave_rush_1029.mp3',.76,.8],
 ['tidalWallAlert',BOFA.sfx.alertDanger,.48,.4]]){
 const slots=[],list=[];BOFA.sfx[key]=uri;
 for(let i=0;i<2;i++)Object.defineProperty(list,i,{enumerable:true,get(){
  if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
 Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g,native:true,min};Audio.SFX[key]=()=>Snd.play(key);
}
function ts58Own(b){return run.stage===9&&b===boss&&b?._ts58&&b._ship==='tidalsovereign';}
function ts58Log(event,data={}){TS58.events.push({event,time:efxClock,...data});if(TS58.events.length>1800)TS58.events.shift();}
function ts58Blit(n,f,x,y){return er28Blit('ts58_'+n,f,x,y);}
function ts58Move(b,x,y){b.x=x;b.y=b._drawY=y;}
function ts58Point(b,slot){const p=WT25_ART.sockets[slot]||[160,128];return{x:b.x+p[0]-160,y:(b._drawY??b.y)+p[1]-128};}
shipBossMount=function(b,s){return ts58Own(b)?ts58Point(b,s):TS58.base.mount.apply(this,arguments);};
target17Ready=function(b){return ts58Own(b)?false:TS58.base.ready.apply(this,arguments);};
stageLoadBegin=function(n,keys){if(n===9)Snd.prepare(['bossfireTidalfusion','bossWeaponCharge','cfComboWater','combatOrb0927','jetDash','tidalWaterWave','tidalWallAlert']);
 const names=Object.keys(TS58_ART).filter(k=>n===9?!k.startsWith('sentinel'):n===8?k.startsWith('sentinel'):false);
 return TS58.base.load.call(this,n,[...(keys||[]),...names.map(k=>TS58_ART[k].key),...(n===9?[HH52_ART.star.key,...['field','symbol'].flatMap(r=>['green','yellow','red'].map(c=>'rk50_'+r+'_'+c))]:[])]);};
s9FusionBossInit=function(b,baseHp){if(run.stage!==9)return TS58.base.init.apply(this,arguments);
 shipBossInit(b,'tidalsovereign');b.kind='tidalsovereign';b._s9fusion={phase:'tidal',t:0,baseHp};late27Init(b,'tidal');b._late27.suspended=true;
 b._ts58={nativeHP:b.maxhp,clock:0,t:0,seq:0,half:false,mode:'entry',phase:'entry',protected:true,from:{x:worldWidth()/2,y:-180},home:{x:worldWidth()/2,y:158},markers:[],geysers:[],waves:[],flashes:[],charge:0,hit:new Map()};
 b.enter=true;ts58Move(b,worldWidth()/2,-180);b.fireCd=999;b._sba=null;b._s9Beam=null;b._s9Cascade=null;TS58.owners.add(b);ts58Log('immediate-water-entry',{hp:b.hp,maxhp:b.maxhp});return true;};
spawnBoss=function(){const r=TS58.base.bossSpawn.apply(this,arguments);if(ts58Own(boss)&&boss._ts58.mode==='entry')boss.hp=boss.maxhp=boss._ts58.nativeHP;return r;};
function ts58ClearShots(b){for(const q of eBullets)if(q._ts58Owner===b)q.dead=true;const T=b._ts58;T.markers=[];T.geysers=[];T.waves=[];T.flashes=[];T.grenades=[];T.bursts=[];T.pendingRain=[];}
function ts58Clear(b){if(!b?._ts58)return;ts58ClearShots(b);TS58.owners.delete(b);}
function ts58Set(b,kind){if(kind==='rollers')kind='grenades';const T=b._ts58;T.mode=kind;T.phase='charge';T.t=0;T.next=0;T.shots=0;T.charge=0;T.protected=false;T.from={x:b.x,y:b.y};T.aim={x:player.x,y:player.y};T.locked=false;
 T.warm=kind==='grenades'?2.1:kind==='tidal'?FIRE_ALERT_STEP*3+FIRE_ALERT_HOLD:kind==='rain'?1.8:kind==='slide'?1.6:kind==='lamp'?2.5:1.35;
 T.live=kind==='bullets'?2.3:kind==='mortars'?3.6:kind==='grenades'?2.5:kind==='tidal'?4.2:kind==='rain'?3.4:kind==='lamp'?6.5:5.3;if(diffKey==='hard'){if(kind!=='tidal')T.warm+=.25;T.live=kind==='bullets'?2.0:kind==='mortars'?2.7:kind==='rain'?2.7:kind==='lamp'?4.6:T.live;}T.tail=0;T.home.x=(camLeftX()+camRightX())/2;
 if(kind==='tidal'){T.laneBounds={left:camLeftX(),width:viewW()};T.lanes=[.22,.5,.78].map(p=>T.laneBounds.left+T.laneBounds.width*p);T.waveShown=0;}
 if(kind==='slide')T.slideX=clamp(player.x,camLeftX()+95,camRightX()-95);
 combatAudio0927(b,'bossWeaponCharge',.2);ts58Log('water-attack-start',{kind,half:T.half,warm:T.warm});}
function ts58Next(b){const T=b._ts58,book=T.half?['lamp','grenades','rain','slide','tidal','mortars','bullets']:['bullets','mortars','grenades','tidal','rain','slide'];ts58Set(b,book[T.seq++%book.length]);}
function ts58Half(b){const T=b._ts58;ts58ClearShots(b);T.half=true;T.mode='half';T.phase='fill-centre';T.t=0;T.charge=0;T.protected=true;T.from={x:b.x,y:b.y};T.seq=0;
 combatAudio0927(b,'bossWeaponCharge',.2);ts58Log('half-health-fill',{hp:b.hp,maxhp:b.maxhp});}
er26DamageClamp=function(b,d){const v=TS58.base.clamp.apply(this,arguments);if(!ts58Own(b))return v;const T=b._ts58;if(T.protected||b.enter)return 0;return !T.half?Math.min(v,Math.max(0,b.hp-b.maxhp*.5)):v;};
hitBoss=function(){const b=boss,r=TS58.base.hit.apply(this,arguments);if(ts58Own(b)&&!b.dead&&!b._ts58.half&&b.hp<=b.maxhp*.5+.001)ts58Half(b);if(b?.dead&&b._ts58)ts58Clear(b);return r;};
bossHitTest=function(x,y){if(!ts58Own(boss))return TS58.base.test.apply(this,arguments);const b=boss,T=b._ts58;if(b.dead||b.enter||T.protected)return false;
 const yes=er28AlphaAt('ts58_body_hit',0,x-b.x,y-(b._drawY??b.y));if(yes){_lastHitX=x;_lastHitY=y;}return yes;};
retinaBossTargets=function(b){return ts58Own(b)&&(b._ts58.protected||b.enter||b.y<-100||b.y>VH+100)?[]:TS58.base.targets.apply(this,arguments);};
function ts58Flash(b,slot){b._ts58.flashes.push({slot,t:0});}
function ts58Shot(b,slot,a,speed,kind='slug',extra={}){if(eBullets.filter(q=>q._ts58Owner===b&&!q.dead).length>=110)return null;const dy=SG26.context?.b===b?SG26.context.q.next:0,p=extra._worldOrigin?{x:extra._worldOrigin.x,y:extra._worldOrigin.y-dy}:ts58Point(b,slot),q=eShootT(p.x,p.y,a,speed/60,'s9pair',{owner:b,noMuzzle:true,silent:true,w:kind==='lamp'?30:12,h:kind==='lamp'?30:12});if(!q)return null;
 Object.assign(q,{_ts58Owner:b,_ts58Born:b._ts58.clock,_ts58:kind,_weaponProof:true,_shootable:false,_s3kOriginalProof:false,_noArsenal:true,homing:false,_ts60Dir:clamp(Math.round((a-Math.PI/2)/.12)+2,0,4),_ts60Birth:{x:p.x,y:p.y+dy},...extra});q.vx=Math.cos(a)*speed/60;q.vy=Math.sin(a)*speed/60;delete q.hp;if(!extra._worldOrigin)ts58Flash(b,slot);if(kind==='slug'||kind==='jet')ts58Log('water-muzzle-release',{kind,slot,a,x:p.x,y:p.y+dy});return q;}
function ts58Mark(b,x,y,delay=1.5,source='mortar',q=null){const T=b._ts58;if(T.markers.length>=12)return;
 const M={id:++TS58.serial,x:clamp(x,camLeftX()+42,camRightX()-42),y:clamp(y,viewTopY()+100,VH-42),t:0,warm:delay,source,q};T.markers.push(M);ts58Log('ground-water-mark',{x:M.x,y:M.y,warm:delay,source});return M;}
function ts58Mortar(b,slot,x,y,from=null,source='mortar'){const p=from||ts58Point(b,slot),dy=SG26.context?.b===b?SG26.context.q.next:0,q=ts58Shot(b,slot,Math.PI/2,0,'mortar');if(!q)return;if(from){q.x=p.x;q.y=p.y-dy;b._ts58.flashes.pop();}else p.y+=dy;const M=ts58Mark(b,x,y,1.5,source,q);if(!M){q.dead=true;return;}q._ts58Flight={start:p,target:M,t:0,dur:1.5};combatAudio0927(b,'bossfireTidalfusion',.15);}
function ts58Wave(b,x,y,speed=165,small=false){const T=b._ts58;if(T.waves.length>=14)return;T.waves.push({x,y,t:0,speed:small?speed:(VH+300)/FIRE_CROSS,small});combatAudio0927(b,small?'cfComboWater':'tidalWaterWave',.2);ts58Log('tidal-wave',{x,y,small});}
function ts58WaveFrame(W){const phase=Math.floor(W.t*13)%8;if(W.small)return phase;const width=210*(.9+clamp(W.t/FIRE_CROSS,0,1)*1.25),size=clamp(Math.round((width-190)/262*5),0,5);return size*8+phase;}
function ts58Impact(b,M){if(M.source==='fan-grenade'){if(M.grenade)M.grenade.dead=true;ts60Burst(b,M.x,M.y);return;}const T=b._ts58;T.geysers.push({x:M.x,y:M.y,t:0,life:1.35});combatAudio0927(b,'cfComboWater',.12);ts58Log('geyser-impact',{x:M.x,y:M.y,source:M.source});}
function ts60Grenade(b,slot,x,y){const T=b._ts58;T.grenades??=[];if(T.grenades.length>=6)return;const p=ts58Point(b,slot);if(SG26.context?.b===b)p.y+=SG26.context.q.next;const M=ts58Mark(b,x,y,1.8,'fan-grenade');if(!M)return;const G={slot,from:{...p},x:p.x,y:p.y,t:0,life:1.8,target:M,dead:false};M.grenade=G;T.grenades.push(G);ts58Flash(b,slot);combatAudio0927(b,'combatOrb0927',.15);ts58Log('fan-grenade-launch',{slot,x:p.x,y:p.y,target:{x:M.x,y:M.y},fuse:1.8});}
function ts60LaunchRain(b,slot,x,y,source='fan-rain'){const T=b._ts58,q=ts58Shot(b,slot,-Math.PI/2,410,'jet');if(q)(T.pendingRain??=[]).push({q,slot,x,y,source});combatAudio0927(b,'cfComboWater',.2);ts58Log('fan-geyser-launch',{slot,source,x:q?._ts60Birth.x,y:q?._ts60Birth.y});}
function ts60Burst(b,x,y){const T=b._ts58;T.bursts??=[];T.bursts.push({x,y,t:0,life:.65});if(T.bursts.length>16)T.bursts.shift();ts58Damage(b,x,y,48,'Tidal water grenade splash');for(let i=0;i<10;i++)ts58Shot(b,'C',i*TAU/10,175,'spray',{_worldOrigin:{x,y}});combatAudio0927(b,'cfComboWater',.12);ts58Log('water-grenade-explode',{x,y,radius:48,shards:10});}
function ts60Ballistics(b,dt){const T=b._ts58;T.pendingRain??=[];T.grenades??=[];T.bursts??=[];
 for(const P of T.pendingRain){if(P.q.y<viewTopY()-4){const M=ts58Mark(b,P.x,P.y,1.6,P.source);if(M)M.rain=true;P.done=true;P.q.dead=true;ts58Log('fan-jet-offscreen',{slot:P.slot,x:P.q.x,y:P.q.y,target:{x:P.x,y:P.y}});}else if(P.q.dead)P.done=true;}
 T.pendingRain=T.pendingRain.filter(P=>!P.done);
 for(const G of T.grenades){if(G.dead)continue;G.t+=dt;const u=clamp(G.t/G.life,0,1);G.x=lerp(G.from.x,G.target.x,u);G.y=lerp(G.from.y,G.target.y,u)-Math.sin(u*Math.PI)*115;
  if(u<1)for(const seat of seatList())withSeat(seat,()=>{if(!G.dead&&!player.dead&&player.invuln<=0&&Math.hypot(player.x-G.x,player.y-G.y)<24){G.dead=true;G.target.cancelled=true;ts60Burst(b,G.x,G.y);}});
 }
 T.grenades=T.grenades.filter(G=>!G.dead);T.markers=T.markers.filter(M=>!M.cancelled);for(const B of T.bursts)B.t+=dt;T.bursts=T.bursts.filter(B=>B.t<B.life);
}
function ts58Damage(b,x,y,r,label){const T=b._ts58;for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&player.invuln<=0&&Math.hypot(player.x-x,player.y-y)<r+4&&(T.hit.get(seat)||0)<=T.clock){T.hit.set(seat,T.clock+.25);playerHit(label);}});}
function ts58Danger(b,dt){const T=b._ts58;
 ts60Ballistics(b,dt);
 for(const F of T.flashes)F.t+=dt;T.flashes=T.flashes.filter(F=>F.t<.32);
 for(const M of T.markers){M.t+=dt;if(M.q?.dead){M.cancelled=true;continue;}combatWarningTick(M,'ts58-ground-'+M.id,Math.min(M.t,M.warm),M.warm);if(M.t>=M.warm){if(M.q)M.q.dead=true;M.done=true;ts58Impact(b,M);}}
 T.markers=T.markers.filter(M=>!M.done&&!M.cancelled);
 for(const G of T.geysers){G.t+=dt;if(G.t>.13&&G.t<.75)ts58Damage(b,G.x,G.y,32,'Tidal geyser splash');if(!G.fall&&G.t>.66){G.fall=true;ts58Wave(b,G.x,G.y-135,155,true);}}
 T.geysers=T.geysers.filter(G=>G.t<G.life);
 for(const W of T.waves){W.t+=dt;W.y+=W.speed*dt;const bank=W.small?'ts58_fall_wave':'ts58_wave',frame=ts58WaveFrame(W);for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&[[0,0],[-4,0],[4,0],[0,-4],[0,4]].some(([x,y])=>er28AlphaAt(bank,frame,player.x+x-W.x,player.y+y-W.y)))playerHit('Tidal falling water wave');});}
 T.waves=T.waves.filter(W=>W.t<5&&W.y<VH+(W.small?110:180));
 const Q=eBullets.filter(q=>q._ts58Owner===b&&!q.dead);
 for(const q of Q){const age=T.clock-q._ts58Born;if(age>11){q.dead=true;continue;}
  if(q._ts58Flight){const F=q._ts58Flight;F.t+=dt;const u=clamp(F.t/F.dur,0,1);q.x=lerp(F.start.x,F.target.x,u);q.y=lerp(F.start.y,F.target.y,u)-Math.sin(u*Math.PI)*125;q.vx=q.vy=0;}
  if(q._ts58==='lamp'){
   const r=ts58BubbleSize(q)*.32;
   q.vy=clamp(q.vy+(Math.sin(age*1.65+q._ts58Seed)*.055-.001)*dt*60,-1.8,1.8);q.vx=clamp(q.vx+Math.sin(age*.7+q._ts58Seed)*.008*dt*60,-1.2,1.2);q.w=q.h=r*1.6;
   if(q.x<camLeftX()+r){q.x=camLeftX()+r;q.vx=Math.abs(q.vx);}else if(q.x>camRightX()-r){q.x=camRightX()-r;q.vx=-Math.abs(q.vx);}
   if(q.y<viewTopY()+r+30){q.y=viewTopY()+r+30;q.vy=Math.abs(q.vy);}else if(q.y>VH-r){q.y=VH-r;q.vy=-Math.abs(q.vy);}
  }
 }
 const lamps=Q.filter(q=>q._ts58==='lamp'&&!q.dead);
 for(let i=0;i<lamps.length;i++)for(let j=i+1;j<lamps.length;j++){const a=lamps[i],c=lamps[j];if(a.dead||c.dead||a._ts58Mass+c._ts58Mass>7)continue;const d=Math.hypot(a.x-c.x,a.y-c.y);if(d<(ts58BubbleSize(a)+ts58BubbleSize(c))*.21){const m=a._ts58Mass+c._ts58Mass;a.x=(a.x*a._ts58Mass+c.x*c._ts58Mass)/m;a.y=(a.y*a._ts58Mass+c.y*c._ts58Mass)/m;a.vx=(a.vx+c.vx)/2;a.vy=(a.vy+c.vy)/2;a._ts58Mass=m;c.dead=true;ts58Log('bubble-merge',{mass:m,x:a.x,y:a.y});}}
}
function ts58BubbleIndex(q){return Math.min(5,Math.max(0,Math.round(Math.sqrt(q._ts58Mass||1)*1.8)-1));}
function ts58BubbleSize(q){return[28,40,56,72,96,120][ts58BubbleIndex(q)];}
// Mortar feint follows simulation time; sockets/Retinas retain their existing owners.
function ts62MortarMove(b,T,dt){
 const u=clamp(T.t/.8,0,1),ease=u*u*(3-2*u),amplitude=Math.min(78,Math.max(0,(viewW()-336)/2));
 const centre=(camLeftX()+camRightX())/2,target=clamp(lerp(T.from.x,centre,ease)+Math.sin(T.t*2.1)*amplitude*ease,camLeftX()+168,camRightX()-168);
 const x=b.x+clamp(target-b.x,-180*dt,180*dt);
 ts58Move(b,x,T.from.y+Math.sin(T.t*3.1)*5*ease);
}
function ts58Tick(b,dt){const T=b._ts58;dt=Math.min(.05,Math.max(0,dt));T.clock+=dt;T.t+=dt;ts61WaveTell(b,T);b.fireCd=999;b._sba=null;b._s9Beam=null;b._s9Cascade=null;b._hm=999;b._s4MiniSafe=true;ts58Danger(b,dt);
 if(!T.half&&b.hp<=b.maxhp*.5+.001)ts58Half(b);
 if(T.mode==='entry'){const u=clamp(T.t/1.6,0,1),k=u*u*(3-2*u);ts58Move(b,T.home.x,lerp(-180,T.home.y,k));b.enter=u<1;if(u>=1){T.protected=false;ts58Next(b);}return true;}
 if(T.mode==='half'){const u=clamp(T.t/1.5,0,1),k=u*u*(3-2*u);T.charge=clamp(T.t/3,0,1);ts58Move(b,lerp(T.from.x,(camLeftX()+camRightX())/2,k)+Math.sin(T.t*80)*T.charge*3,lerp(T.from.y,VH*.48,k));shake=Math.max(shake,T.charge*2);if(T.t>=3){T.protected=false;T.home={x:(camLeftX()+camRightX())/2,y:VH*.48};ts58Next(b);}return true;}
 const u=T.t-T.warm;
 if(u<0){T.phase='charge';T.charge=clamp(T.t/T.warm,0,1);if(!T.locked&&T.charge>=.45){T.locked=true;T.aim={x:player.x,y:player.y};ts58Log('aim-locked',{kind:T.mode,target:{...T.aim}});}
  let x=T.from.x;if(T.mode==='slide')x=lerp(T.from.x,T.slideX,Math.min(1,T.t/.7));if(T.mode==='lamp')x=(camLeftX()+camRightX())/2;
  if(T.mode==='mortars')ts62MortarMove(b,T,dt);else ts58Move(b,x+(T.mode==='tidal'||T.mode==='lamp'?Math.sin(T.t*90)*T.charge*2.5:0),T.from.y+Math.sin(T.t*4)*2);combatWarningTick(b,'ts58-'+T.mode,T.t,T.warm);return true;}
 T.charge=.4;
 if(u<T.live){if(T.phase!=='fire'){T.phase='fire';ts58Log('water-release',{kind:T.mode});}if(T.mode==='slide'){
   const d=clamp(u/1.3,0,1);if(u<1.3){T.protected=false;ts58Move(b,T.slideX,lerp(T.from.y,VH+240,d));if(u>=T.next){T.next=u+.23;for(const s of[-1,1])ts58Wave(b,b.x+s*65,b.y+30,190,true);ts58Flash(b,'L');ts58Flash(b,'R');combatAudio0927(b,'jetDash',.3);}if(b.y<VH+80)for(const seat of seatList())withSeat(seat,()=>{const dy=SG26.context?.b===b?SG26.context.q.next:0;if(!player.dead&&er28AlphaAt('ts58_body_hit',0,player.x-b.x,player.y-b.y-dy))playerHit('Tidal Slip N Slide hull');});}
   else if(u<2.3){T.protected=true;ts58Move(b,T.slideX,VH+240);}else{const r=clamp((u-2.3)/1.5,0,1),k=r*r*(3-2*r);T.protected=r<1;ts58Move(b,T.home.x,lerp(-180,T.home.y,k));}return true;
  }
  if(T.mode==='mortars')ts62MortarMove(b,T,dt);
  if(T.mode==='tidal'){if(T.shots<3&&!T.waves.some(w=>!w.small)){ts58Wave(b,T.lanes[T.shots],-140,0,false);T.shots++;}return true;}
  if(u>=T.next){const index=T.shots++;T.next=u+(T.mode==='bullets'?(diffKey==='hard'?.28:.23):T.mode==='mortars'?(diffKey==='hard'?1.0:.8):T.mode==='grenades'?.85:T.mode==='rain'?.8:.6);
   if(T.mode==='bullets'){for(const slot of['L','R'])for(const off of(diffKey==='hard'?[-.12,0,.12]:[-.24,-.12,0,.12,.24]))ts58Shot(b,slot,Math.PI/2+off,205,'slug');combatAudio0927(b,'bossfireTidalfusion',.18);}
   else if(T.mode==='mortars'&&index<(diffKey==='hard'?3:4)){const x=clamp(T.aim.x+(index%2?1:-1)*(38+index*18),camLeftX()+55,camRightX()-55),y=clamp(T.aim.y-(index%3)*86,viewTopY()+210,VH-50);ts60LaunchRain(b,index%2?'circleR':'circleL',x,y,'fan-mortar');}
   else if(T.mode==='grenades'&&index<2){const slot=index?'circleR':'circleL';ts60Grenade(b,slot,T.aim.x+(index?55:-55),clamp(T.aim.y-index*65,viewTopY()+220,VH-48));}
   else if(T.mode==='rain'&&index<(diffKey==='hard'?2:3)){for(const slot of['circleL','circleR']){const x=clamp(T.aim.x+(slot==='circleL'?-1:1)*(45+index*32),camLeftX()+48,camRightX()-48),y=clamp(T.aim.y-index*75,viewTopY()+170,VH-48);ts60LaunchRain(b,slot,x,y);}}
   else if(T.mode==='lamp'&&index<(diffKey==='hard'?3:5)){T.next=u+1.2;for(const slot of['circleL','circleR']){const q=ts58Shot(b,slot,Math.PI/2+(slot==='circleL'?-.35:.35),65,'lamp',{_ts58Mass:1.6,_ts58Seed:index*1.7});if(q){q._ts58Born=T.clock;ts58Log('lamp-bubble',{slot,index});}}combatAudio0927(b,'combatOrb0927',.18);}
  }return true;
 }
 T.phase='recover';T.charge=0;T.tail+=dt;const x=T.home.x+Math.sin(T.clock*.5)*30,y=T.home.y+Math.sin(T.clock*.9)*8;ts58Move(b,b.x+clamp(x-b.x,-60*dt,60*dt),b.y+clamp(y-b.y,-55*dt,55*dt));
 const hazards=T.markers.length||T.geysers.length||T.waves.length||T.pendingRain?.length||T.grenades?.length||T.bursts?.length||eBullets.some(q=>q._ts58Owner===b&&!q.dead);if(T.tail>=(diffKey==='hard'?1.65:1.15)&&(!hazards||T.tail>5.0)){ts58Log('water-recover-complete',{kind:T.mode});ts58ClearShots(b);ts58Next(b);}return true;
}
s9FusionBossTick=function(b,dt){if(ts58Own(b)){if(b.dead){ts58Clear(b);return false;}return ts58Tick(b,dt);}return TS58.base.tick.apply(this,arguments);};
function ts61WaveTell(b,T){
 if(T.mode!=='tidal'||T.phase==='recover')return;
 const shown=Math.min(3,1+Math.floor(T.t/FIRE_ALERT_STEP));
 while((T.waveShown||0)<shown){const i=T.waveShown||0;T.waveShown=i+1;combatAudio0927(b,'tidalWallAlert',.12);ts58Log('water-wall-warning',{index:i,x:T.lanes[i]});}
}
function ts61WaveWarnings(b,T){
 if(T.mode!=='tidal'||!['charge','fire'].includes(T.phase))return;
 const shown=Math.min(3,1+Math.floor(T.t/FIRE_ALERT_STEP));
 for(let i=T.shots;i<shown;i++)ts58Blit('wall_warning',i===T.shots?1:0,T.lanes[i],viewTopY()+96+Math.sin(T.t*2.2+i*.7)*7);
}
function ts58Warn(b,T){const charge=T.phase==='charge'||T.mode==='half',p=clamp(T.t/(T.mode==='half'?3:T.warm),0,1);
 if(T.mode==='tidal')return; // Water-wall asterisks render last, above the hull and water art.
 if(!charge||T.mode==='entry')return;
 if(T.mode!=='tidal')hh52Blit('star',0,b.x,Math.max(viewTopY()+40,b.y-140));
 if(T.mode==='lamp'||T.mode==='half'){const colour=p<.45?'green':p<.8?'yellow':'red';rk50Blit('field',colour,b.x,b.y);rk50Blit('symbol',colour,b.x,b.y-145);}
 else if(T.mode==='slide'){combatWarningDraw(b,{x:T.slideX,y:b.y,ex:T.slideX,ey:VH+80,width:320,progress:p,fieldOnly:true});for(let y=b.y+150;y<VH;y+=100)ts58Blit('arrow',Math.floor(T.clock*12)%8,T.slideX,y);for(let y=b.y+130;y<VH;y+=110)ts58Blit('trail',Math.floor(T.clock*12)%16,T.slideX,y);}
 else if(T.mode==='bullets'){for(const slot of['L','R']){const P=ts58Point(b,slot);for(const off of(diffKey==='hard'?[-.12,0,.12]:[-.24,-.12,0,.12,.24])){const a=Math.PI/2+off;combatWarningDraw(b,{...P,ex:P.x+Math.cos(a)*800,ey:P.y+Math.sin(a)*800,width:12,progress:p,fieldOnly:true,laneShape:'line'});}}}
}
shipBossDraw=function(b){if(!ts58Own(b))return TS58.base.draw.apply(this,arguments);const T=b._ts58;if(b.dead)return TS58.base.draw.apply(this,arguments);
 ts58Warn(b,T);for(const M of T.markers)groundTargetReticleDraw(M.x,M.y,78,clamp(M.t/M.warm,0,1),1);
 for(const W of T.waves)ts58Blit(W.small?'fall_wave':'wave',ts58WaveFrame(W),W.x,W.y);
 for(const G of T.geysers)ts58Blit('geyser',Math.min(15,Math.floor(G.t/G.life*16)),G.x,G.y);
 const state=b.hp/b.maxhp>.62?'intact':b.hp/b.maxhp>.3?'damaged':'critical',level=clamp(Math.floor(T.charge*3.99),0,3),f=Math.floor(T.clock*16)%16;
 if(T.charge>.25)ts58Blit('outer',Math.floor(T.clock*(12+T.charge*12))%8,b.x,b._drawY??b.y);
 ts58Blit(b.flash>0?'body_hit':'body_'+state,b.flash>0?0:level*16+f,b.x,b._drawY??b.y);
 if(T.charge>.2)for(const slot of(T.mode==='rain'||T.mode==='mortars'||T.mode==='grenades'?['circleL','circleR']:T.mode==='lamp'||T.mode==='half'?['circleL','circleR','C']:['L','R'])){const p=ts58Point(b,slot);ts58Blit(T.mode==='grenades'?'grenade_charge':slot==='L'||slot==='R'?'forward_muzzle':'muzzle',T.mode==='grenades'?Math.min(15,Math.floor(T.charge*15)):Math.floor(T.clock*16)%16,p.x,p.y);}
 for(const F of T.flashes){const p=ts58Point(b,F.slot);ts58Blit(F.slot==='L'||F.slot==='R'?'forward_muzzle':T.mode==='rain'||T.mode==='mortars'?'fan_muzzle':'muzzle',Math.min(15,Math.floor(F.t/.32*16)),p.x,p.y);}
 for(const G of T.grenades||[])if(!G.dead)ts58Blit('roller',Math.floor(G.t*22)%16,G.x,G.y);
 for(const B of T.bursts||[])ts58Blit('grenade_burst',Math.min(15,Math.floor(B.t/B.life*16)),B.x,B.y);
 for(const q of eBullets)if(q._ts58Owner===b&&q._ts58==='jet'&&!q.dead)ts58Blit('jet',Math.floor((T.clock-q._ts58Born)*22)%16,q.x,q.y);
 for(const M of T.markers)if(M.rain&&M.t>M.warm-.55){const u=(M.t-M.warm+.55)/.55;ts58Blit('rain',Math.floor(T.clock*20)%8,M.x,lerp(viewTopY()-180,M.y,u));}
 ts61WaveWarnings(b,T);return true;};
drawCombatFinalProjectile=function(q){if(q?._ts58Owner){const b=q._ts58Owner,T=b._ts58,f=Math.floor((T.clock-q._ts58Born)*22)%16;
 if(q._ts58==='lamp')return ts58Blit('bubble',ts58BubbleIndex(q)*16+f,q.x,q.y);
 if(q._ts58==='jet')return true;
 if(q._ts58==='slug')return ts58Blit('forward_slug',(q._ts60Dir??2)*16+f,q.x,q.y);
 return ts58Blit(q._ts58==='mortar'?'bomb':'slug',f,q.x,q.y);
 }return TS58.base.projectile.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._ts58Owner||q?._ts58SentinelOwner?false:TS58.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._ts58Owner?null:TS58.base.element.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._ts58Owner||q?._ts58SentinelOwner){q._weaponProof=true;q._shootable=false;delete q.hp;return;}return TS58.base.rules.apply(this,arguments);};
function ts58Sentinel(side,x,y=-130){const first=enemies.length;TS58.base.spawn.call(this,'s8interceptor',x,y,{});const e=enemies[first];if(!e)return null;
 for(const k of['_mutator1003','_mm1003','_mutatorSlot1003','_alien1003','_orbit1003','_frRealmAI','_dr','_cn','_droid','_furyMove','_esh','_enemyShield','_frFlight','_entrySweep'])delete e[k];
 const saved=diffKey,current=EHP(150);let normal;try{diffKey='normal';normal=EHP(150);}finally{diffKey=saved;}
 e._ts58Sentinel={side,t:0,seq:0,cd:1.3,phase:'hover',born:{x,y}};e.type='s8gunship';e.pattern='s8mega';e._s8mega='s8gunship';e.w=188;e.h=142;e._drawW=188;e._drawH=142;e.hp=e.maxhp=e._maxhp=Math.round(150*current/Math.max(1,normal)*le19PartyFactor());e.score=4000;e.shoots=false;e.spin=0;e._ai27=null;e.name=side<0?'WARP SENTINEL ALPHA':'WARP SENTINEL BETA';ts58Log('stage8-sentinel-spawn',{side,hp:e.hp});return e;}
spawnEnemy=function(type,x,y,opt){if(run.stage===8&&type==='pt11frostcarrier'){ts58Sentinel(-1,worldWidth()*.29);ts58Sentinel(1,worldWidth()*.71);return;}return TS58.base.spawn.apply(this,arguments);};
s8MegaTick=function(e,dt){const S=e?._ts58Sentinel;if(!S)return TS58.base.enemy.apply(this,arguments);if(e.dead||e._dyingT!=null)return;S.t+=dt;e._et=(e._et||0)+dt;e._ai27=null;
 const u=clamp(S.t/1.8,0,1),k=u*u*(3-2*u);e.x=S.born.x+Math.sin(S.t*.85+S.side)*27;e.y=lerp(S.born.y,viewTopY()+130,k)+Math.sin(S.t*1.4)*9;
 if(S.t<1.8)return;if(e.x<camLeftX()+15||e.x>camRightX()-15||e.y+38<viewTopY()+8||e.y+38>VH-16){S.phase='hover';S.warn=0;S.cd=Math.max(S.cd,.35);return;}S.cd-=dt;if(S.cd<=0&&S.phase==='hover'){S.phase='charge';S.warn=0;S.aim=Math.atan2(player.y-e.y,player.x-e.x);}
 if(S.phase==='charge'){S.warn+=dt;combatWarningTick(e,'ts58-sentinel-'+S.side,S.warn,.95);if(S.warn>=.95){S.phase='hover';S.cd=1.8;S.seq++;const n=S.seq%3===0?8:5;for(let i=0;i<n;i++){const a=n===8?S.aim+Math.PI/2+i*TAU/10:S.aim+(i-2)*.13,q=eShootT(e.x,e.y+38,a,3.0,n===8?'s9warp':'s9needle',{owner:e,noMuzzle:true});if(q)Object.assign(q,{_ts58SentinelOwner:e,_weaponProof:true,_shootable:false,_noArsenal:true});}ts58Log('stage8-sentinel-fire',{side:S.side,count:n});}}
};
drawEnemy=function(e){const S=e?._ts58Sentinel;if(!S)return TS58.base.enemyDraw.apply(this,arguments);if(S.phase==='charge'&&!e.dead&&e._dyingT==null){for(let i=-2;i<=2;i++){const a=S.aim+i*.13;combatWarningDraw(e,{x:e.x,y:e.y+38,ex:e.x+Math.cos(a)*700,ey:e.y+38+Math.sin(a)*700,width:16,progress:S.warn/.95,fieldOnly:true});}}
 return ts58Blit(e.flash>0?'sentinel_hit':S.side<0?'sentinel_alpha':'sentinel_beta',Math.floor(S.t*12)%16,e.x,e.y);};
updatePlay=function(dt){for(const b of TS58.owners)if(!ts58Own(b)||b.dead)ts58Clear(b);for(const q of eBullets)if(q._ts58Owner&&(!ts58Own(q._ts58Owner)||q._ts58Owner.dead))q.dead=true;return TS58.base.update.apply(this,arguments);};
globalThis.BOF_TIDAL_SOVEREIGN_1029={state:TS58,start:ts58Set,sentinel:ts58Sentinel};
