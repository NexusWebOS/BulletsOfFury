"use strict";
/* FB112: selected Furious storm contacts. Normal/Hard and Stage X retain their
   native owners. The existing Furious Sumpjaw pair remains the Stage7 contact. */
const FB112={base:{spawn:spawnBoss,sub:spawnSubBoss__inner,tick:updateBoss,subtick:updateSubBoss,
 draw:drawBoss,subdraw:drawSubBoss,hit:hitBoss,subhit:hitSubBoss,at:bossHitTest,
 subat:subBossHitPart,solid:subBossSolidAt,beam:subBossBeamImpact,targets:retinaBossTargets,
 projectile:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,load:stageLoadBegin,
 ready:target17Ready,overlay:encounterDamageOverlay,list:debugFightList},events:[],masks:new Map(),shadows:new Map(),cells:new Map(),cellBytes:0};
for(const B of Object.values(FB112_ART.banks))XART._src[B.key]=B.path;
function fb112Rank(){return diffKey==='furious'&&!run._gp4StageX;}
function fb112Own(b){return !!b?._fb112;}
function fb112Keys(){return Object.values(FB112_ART.banks).map(b=>b.key);}
function fb112Log(b,event,data={}){FB112.events.push({id:b._fb112.id,event,t:b.t,...data});if(FB112.events.length>1600)FB112.events.shift();}
function fb112Dir(a,dirs=32){return v31Dir(a,dirs);}
function fb112Angle(a){return Math.PI/2+TAU*fb112Dir(a)/32;}
function fb112Cell(B,n){
 const key=B.key+':'+n;let c=FB112.cells.get(key);
 if(c){FB112.cells.delete(key);FB112.cells.set(key,c);return c;}
 c=document.createElement('canvas');c.width=c.height=B.cell;
 c.getContext('2d',{willReadFrequently:true}).drawImage(XART.get(B.key),n%B.cols*B.cell,Math.floor(n/B.cols)*B.cell,B.cell,B.cell,0,0,B.cell,B.cell);
 const bytes=B.cell*B.cell*4;while(FB112.cellBytes+bytes>64*1024*1024&&FB112.cells.size){const old=FB112.cells.keys().next().value,drop=FB112.cells.get(old);FB112.cellBytes-=drop.width*drop.height*4;FB112.cells.delete(old);}
 FB112.cells.set(key,c);FB112.cellBytes+=bytes;return c;
}
function fb112Blit(name,f,x,y,k=1,a=Math.PI/2,flash=false,alpha=1){
 const B=FB112_ART.banks[name];if(!B||!XART.rdy(B.key))return false;
 const n=(clamp(f|0,0,B.frames-1)*B.dirs+(B.dirs>1?fb112Dir(a,B.dirs):0)),s=B.cell*k;
 ctx.save();ctx.globalAlpha*=alpha;ctx.drawImage(fb112Cell(B,n),x-s/2,y-s/2,s,s);ctx.restore();return true;
}
function fb112Point(b,p){const q=b._fb112,k=q.scale,a=q.heading-Math.PI/2,x=(p[0]-q.M.cell/2)*k,y=(p[1]-q.M.cell/2)*k;return{x:b.x+x*Math.cos(a)-y*Math.sin(a),y:b.y+x*Math.sin(a)+y*Math.cos(a)};}
function fb112PartPoint(b,p){const at=fb112Point(b,p.mount);p.x=at.x;p.y=at.y;p._retinaOwner=b;return at;}
function fb112Bore(b,p){const at=fb112PartPoint(b,p),a=(p.angle??b._fb112.heading)-Math.PI/2,k=b._fb112.scale,x=p.bore[0]*k,y=(p.bore[1]+(p.recoil>.035?(p.recoilOffset||0):0))*k;return{x:at.x+x*Math.cos(a)-y*Math.sin(a),y:at.y+x*Math.sin(a)+y*Math.cos(a)};}
function fb112Ready(){return fb112Keys().every(k=>XART.rdy(k));}
stageLoadBegin=function(n,keys){if(n!==6){FB112.cells.clear();FB112.cellBytes=0;FB112.masks.clear();FB112.shadows.clear();}if(n===6&&fb112Rank())Snd.prepare(['enemyMachineGunHeavy','combatEnergy0927','bossWeaponCharge','combatModule0927','jetDash','enemyHeavyLaser','expBig','combatBeam0927','overlordWind','c33_thunder']);return FB112.base.load.call(this,n,n===6&&fb112Rank()?[...(keys||[]),...fb112Keys()]:keys);};
function fb112Create(model,sub){
 const M=FB112_ART.models[model],total=Math.round(difficultyHealth15(model==='razor'?1250:4800)*(coopActive()?COOP_BOSS_MUL:1)),b={kind:model==='razor'?'razorwake':'thunderhead',name:model==='razor'?'RAZORWAKE':'THUNDERHEAD',sub,mini:sub,x:worldWidth()/2,y:-M.world*.7,ty:model==='razor'?165:175,w:M.world,h:M.world*.8,hp:total,maxhp:total,t:0,enter:true,dead:false,dying:0,flash:0,fireCd:999,rotor:0,_threat:combatThreat(run.stage)};
 const q=b._fb112={id:model+'-'+Date.now(),model,M,scale:M.world/M.cell,phase:'entry',t:0,seq:0,heading:Math.PI/2,pose:0,fx:[],hazards:[],next:0,death:0,parts:[],open:false};
 const n=M.guns.length,Mp=M.pressures||[];let used=0;
 for(let i=0;i<n;i++){const hp=Math.round(total*(sub?.30:.12));used+=hp;q.parts.push({...M.guns[i],id:'gun'+i,index:i,type:'gun',hp,maxhp:hp,flash:0,recoil:0,angle:Math.PI/2});}
 for(let i=0;i<Mp.length;i++){const hp=Math.round(total*.14);used+=hp;q.parts.push({...Mp[i],id:'pressure'+i,index:i,type:'pressure',hp,maxhp:hp,flash:0,recoil:0,angle:Math.PI/2});}
 q.core={id:'core',type:'core',mount:M.core,bore:[0,0],hp:total-used,maxhp:total-used,flash:0};
 q.vents=(M.shear||[]).map((p,i)=>({id:'wind'+i,type:'vent',mount:p,bore:[0,0],hp:1,angle:Math.PI/2,recoil:0,flash:0}));
 b._s4MiniSafe=sub;continueRewardMark(b);stageLoadBegin(6,fb112Keys());fb112Log(b,'spawn',{hp:total,parts:q.parts.map(p=>({id:p.id,hp:p.hp})),core:q.core.hp});return b;
}
spawnSubBoss__inner=function(kind){if(run.stage===6&&fb112Rank()&&['siegefortress17','siegebomber','razorwake'].includes(kind)){subBoss=fb112Create('razor',true);subBossActive=subBossTriggered=true;subBossDone=false;return subBoss;}return FB112.base.sub.apply(this,arguments);};
spawnBoss=function(kind){if(run.stage===6&&fb112Rank()&&['warhive','thunderhead'].includes(kind)){boss=fb112Create('thunder',false);bossActive=true;bossDefeated=false;return boss;}return FB112.base.spawn.apply(this,arguments);};
debugFightList=function(){return FB112.base.list.apply(this,arguments).map(e=>fb112Rank()&&e.stage===6?{...e,kind:e.role==='mini'?'razorwake':'thunderhead',name:e.role==='mini'?'RAZORWAKE':'THUNDERHEAD'}:e);};
target17Ready=function(b){return fb112Own(b)?false:FB112.base.ready.apply(this,arguments);};
encounterDamageOverlay=function(b){return fb112Own(b)?undefined:FB112.base.overlay.apply(this,arguments);};
function fb112Rolling(b){return b?._fb112?.model==='razor'&&b._fb112.phase==='attack'&&b._fb112.attack==='pass';}
function fb112RollFrame(b){const q=b._fb112,i=Math.max(0,q.M.clips.roll.indexOf(q.pose)),state=(q.parts[0].hp<=0?1:0)|(q.parts[1].hp<=0?2:0);return state*8+i;}
function fb112Visible(b){return b&&!b.dead&&!b.enter&&!fb112Rolling(b)&&b.x>camLeftX()-25&&b.x<camRightX()+25&&b.y>viewTopY()+35&&b.y<VH-35;}
function fb112LiveParts(b){const q=b._fb112;return q.open?[q.core]:q.parts.filter(p=>p.hp>0);}
function fb112Opaque(name,f,a,k,cx,cy,x,y){const B=FB112_ART.banks[name];if(!B||!XART.rdy(B.key))return false;const n=(clamp(f|0,0,B.frames-1)*B.dirs+(B.dirs>1?fb112Dir(a,B.dirs):0)),key=B.key+':'+n;let mask=FB112.masks.get(key);
 if(!mask){const c=document.createElement('canvas');c.width=c.height=B.cell;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(XART.get(B.key),n%B.cols*B.cell,Math.floor(n/B.cols)*B.cell,B.cell,B.cell,0,0,B.cell,B.cell);mask=g.getImageData(0,0,B.cell,B.cell).data;FB112.masks.set(key,mask);}
 const px=Math.floor((x-cx)/k+B.cell/2),py=Math.floor((y-cy)/k+B.cell/2);return px>=0&&px<B.cell&&py>=0&&py<B.cell&&mask[(py*B.cell+px)*4+3]>24;
}
function fb112At(b,x,y,pad=0){if(!fb112Visible(b))return null;const q=b._fb112;let best=null,value=Infinity;
 for(const p of fb112LiveParts(b)){const at=fb112PartPoint(b,p),rx=p.type==='core'?q.M.coreBox[0]*q.scale*.5:p.type==='pressure'?37:22,ry=p.type==='core'?q.M.coreBox[1]*q.scale*.5:p.type==='pressure'?70:43,v=((x-at.x)/(rx+pad))**2+((y-at.y)/(ry+pad))**2,name=q.model+'_'+(p.type==='core'?'body':p.id),f=p.type==='core'?q.pose:p.type==='pressure'?0:p.recoil>.035?1:0,centre=p.type==='core'?b:at;if(v<=1&&v<value&&fb112Opaque(name,f,p.type==='core'?q.heading:p.angle,q.scale,centre.x,centre.y,x,y)){best=p;value=v;}}return best;}
function fb112Damage(b,dmg,x,y,part){if(!fb112Visible(b)||!(dmg>0))return 0;const q=b._fb112,p=part||fb112At(b,x??_lastHitX,y??_lastHitY,3);if(!p||p.hp<=0||p===q.core&&!q.open)return 0;
 const E=elementalDamageResult(b,b.sub?'subboss':'boss',_dmgBullet,dmg,x,y);dmg=er26DamageClamp(b,E.dmg);if(!(dmg>0))return 0;
 const before=p.hp;enemyPoolDamage(p,'hp',dmg,'furiousStormPart','maxhp');p.hp=Math.max(0,p.hp);markHit(p,.075);markHit(b,.055);weaponHitSfx('normal');if(typeof stageStats!=='undefined')stageStats.dmgDealt+=before-p.hp;
 if(typeof wc1031Handles==='function'&&wc1031Handles(_dmgBullet)&&!(WC1031.context&&WC1031.context.owner===b)){const at=fb112PartPoint(b,p);playerWeaponImpact(_dmgBullet,p,Number.isFinite(x)?x:at.x,Number.isFinite(y)?y:at.y,before>p.hp);}
 if(p.hp<=0){p._combatWarnings={};q.hazards=q.hazards.filter(h=>h.part!==p);for(const r of eBullets)if(r._fb112Part===p)r.dead=true;const at=fb112PartPoint(b,p);q.fx.push({x:at.x,y:at.y,t:0,size:100});combatAudio0927(p,'combatModule0927',.2);fb112Log(b,'part-break',{part:p.id});}
 if(!q.open&&q.parts.every(p=>p.hp<=0)){q.open=true;q.seq=0;fb112Set(b,'recover');q.wait=1.4;combatAudio0927(b,'combatModule0927',.4);fb112Log(b,'core-open',{hp:q.core.hp});}
 b.hp=q.core.hp+q.parts.reduce((a,p)=>a+p.hp,0);
 if(b.hp<=0&&!b.dead){fb112Cancel(b);achievementEncounterDefeat(b,b.sub?'miniboss':'boss');fb112Log(b,'defeat');if(b.sub){b.dead=true;b.dying=0;unitDeathFX(b,'mini','blue');combatAudio0927(b,'expBig',.2);}else bossDie();}
 return before-p.hp;
}
hitBoss=function(d){return fb112Own(boss)?fb112Damage(boss,d,_lastHitX,_lastHitY):FB112.base.hit.apply(this,arguments);};
hitSubBoss=function(d,x,y){return fb112Own(subBoss)?fb112Damage(subBoss,d,x,y):FB112.base.subhit.apply(this,arguments);};
bossHitTest=function(x,y){return fb112Own(boss)?!!fb112At(boss,x,y):FB112.base.at.apply(this,arguments);};
subBossHitPart=function(x,y){return fb112Own(subBoss)?fb112At(subBoss,x,y):FB112.base.subat.apply(this,arguments);};
subBossSolidAt=function(x,y){return fb112Own(subBoss)?!!fb112At(subBoss,x,y,2):FB112.base.solid.apply(this,arguments);};
retinaBossTargets=function(b){if(!fb112Own(b))return FB112.base.targets.apply(this,arguments);if(!fb112Visible(b))return[];return fb112LiveParts(b).map(p=>retinaDynamicPiece(b,'fb112-'+p.id,p.type,()=>({...fb112PartPoint(b,p),hp:p.hp,dead:!fb112Visible(b)||p.hp<=0||p===b._fb112.core&&!b._fb112.open}),d=>fb112Damage(b,d,null,null,p),p.type==='core'?70:p.type==='pressure'?75:44,p.type==='core'?95:p.type==='pressure'?130:80));};
subBossBeamImpact=function(b,beam){if(!fb112Own(b))return FB112.base.beam.apply(this,arguments);const r=playerBeamRange(beam);if(!r)return null;let best=null;for(const p of fb112LiveParts(b)){const at=fb112PartPoint(b,p);if(Math.abs(at.x-r.x)<r.half+22&&at.y>r.top-35&&at.y<r.bot+35&&(!best||at.y>best.y))best={x:at.x,y:at.y,entry:at.y,key:p.id};}return best;};
function fb112Set(b,phase){const q=b._fb112;q.phase=phase;q.t=0;q.next=0;q.from={x:b.x,y:b.y};q.hits=new Set();fb112Log(b,'phase',{phase});}
function fb112Cancel(b){const q=b._fb112;q.hazards=[];for(const p of [...q.parts,...q.vents]){p._combatWarnings={};p.recoil=0;}b._combatWarnings={};for(const r of eBullets)if(r._fb112Owner===b)r.dead=true;}
function fb112Warn(b,p,angle,t,dur,width=35,len=900){angle=fb112Angle(angle);const at=p?fb112Bore(b,p):b;combatWarningDraw(p||b,{x:at.x,y:at.y,ex:at.x+Math.cos(angle)*len,ey:at.y+Math.sin(angle)*len,width,progress:clamp(t/dur,0,1),fieldOnly:true});}
function fb112Shot(b,p,angle,blade=false){if(p&&p.hp<=0)return;if(p)p.recoil=.07;const at=p?fb112Bore(b,p):fb112PartPoint(b,b._fb112.core),a=fb112Angle(angle);
 const r=eShootT(at.x,at.y,a,blade?3.1:4.2,'l6bolt',{owner:b,silent:true,noMuzzle:true,w:blade?9:5,h:blade?22:15});Object.assign(r,{_fb112Owner:b,_fb112Part:p,_fb112Angle:a,_fb112Born:b.t,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});fb112Log(b,'round',{part:p?.id,x:at.x,y:at.y,angle:a,blade});}
enemyOrdnanceCanIntercept=function(r){return r?._fb112Owner?false:FB112.base.intercept.apply(this,arguments);};
drawCombatFinalProjectile=function(r){if(r?._fb112Owner){const d=fb112Dir(r._fb112Angle),f=Math.floor((r._fb112Owner.t-r._fb112Born)*24)%16;return fb112Blit('wind_round',d*16+f,r.x,r.y,.5);}return FB112.base.projectile.apply(this,arguments);};
function fb112Start(b){const q=b._fb112;q.seq++;const book=q.model==='razor'?(q.open?['shear','pass','vortex']:['guns','pass','shear','vortex']):q.open?['eye','rail','vortex']:['guns','gates','rail','vortex'];q.attack=book[(q.seq-1)%book.length];fb112Set(b,q.attack==='pass'?'depart':'warn');q.dur=q.attack==='pass'?1.15:1.1;
 const T=targetShip(b.x,b.y);q.target={x:clamp(T.x,camLeftX()+70,camRightX()-70),y:clamp(T.y-65,240,VH-80)};q.lane=worldWidth()/2;q.dir=q.seq%2?1:-1;
 q.passFrom={x:q.dir>0?camLeftX()-155:camRightX()+155,y:clamp(T.y-35,145,VH-115)};q.passTo={x:q.dir>0?camRightX()+155:camLeftX()-155,y:clamp(T.y+35,200,VH-70)};q.columns=Array.from({length:4},(_,i)=>camLeftX()+60+i*(viewW()-120)/3);
 [...q.parts,...q.vents].forEach(p=>{if(p.hp>0){const at=fb112Bore(b,p);p.angle=q.model==='razor'?Math.PI/2:Math.PI/2+clamp(Math.atan2(q.target.y-at.y,q.target.x-at.x)-Math.PI/2,-.32,.32);p.angle=fb112Angle(p.angle);}});
 combatAudio0927(b,q.attack==='pass'?'jetDash':'bossWeaponCharge',.5);fb112Log(b,'warning',{attack:q.attack,target:q.target});
}
function fb112Hazard(b,x,y,kind,part=null){const q=b._fb112,life=kind==='tornado'?2.7:2.5,size=kind==='tornado'?115:95;const h={x,y,t:0,kind,part,life,speed:Math.max(140,(VH+size*.4-y)/(life-.35)),size,hits:new Set()};q.hazards.push(h);q.fx.push({x,y,t:0,size:90});combatAudio0927(b,kind==='tornado'?'overlordWind':'c33_thunder',.9);fb112Log(b,'hazard',{kind,x,y,part:part?.id});}
function fb112Tick(b,dt){if(!b.dead&&!fb112Ready()){stageLoadTick();return;}const q=b._fb112;b.t+=dt;q.t+=dt;b.flash=Math.max(0,b.flash-dt);for(const p of [...q.parts,...q.vents,q.core]){p.flash=Math.max(0,p.flash-dt);p.recoil=Math.max(0,p.recoil-dt);}
 for(const f of q.fx)f.t+=dt;q.fx=q.fx.filter(f=>f.t<.6);
 for(const r of eBullets)if(r._fb112Owner===b&&(b.dead||r._fb112Part?.hp<=0||b.t-r._fb112Born>4))r.dead=true;
 for(const h of q.hazards){h.t+=dt;h.y+=h.speed*dt;if(h.part?.hp<=0||b.dead){h.t=h.life;continue;}if(h.t>.15&&h.t<h.life-.35)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!h.hits.has(seat)&&Math.abs(player.x-h.x)<h.size*.25&&Math.abs(player.y-h.y)<h.size*.38){h.hits.add(seat);playerHit('Storm '+h.kind);}});}
 q.hazards=q.hazards.filter(h=>h.t<h.life&&h.y<VH+180);
 if(b.dead){b.dying+=dt;q.death+=dt;b.y+=28*dt;if(q.model==='razor'){q.heading+=dt*TAU*.75;q.pose=0;}if(q.death>=.2&&q.death<2.2&&q.death>q.next){q.next=q.death+.18;q.fx.push({x:b.x+Math.sin(q.death*27)*b.w*.25,y:b.y+Math.cos(q.death*19)*b.h*.25,t:0,size:140});}
  if(b.sub&&b.dying>3.1&&!q.rewarded){q.rewarded=true;continueRewardResolve(b,b.x,b.y,'miniboss');run.score+=6500;dropPowerup(b.x,b.y,'weapon');subBoss=null;subBossActive=false;subBossDone=true;fb112Log(b,'progression');}return;}
 if(!fb112Ready())return;
 if(q.phase==='entry'){const u=clamp(q.t/2.5,0,1);b.y=lerp(-q.M.world*.7,b.ty,1-(1-u)**3);if(u>=1){b.enter=false;fb112Set(b,'recover');q.wait=1.25;}return;}
 if(q.phase==='recover'){q.heading=Math.PI/2;q.pose=0;if(q.model==='razor')q.parts.forEach(p=>p.angle=q.heading);const home=worldWidth()/2;b.x+=clamp(home-b.x,-dt*100,dt*100);b.y+=clamp(b.ty-b.y,-dt*150,dt*150);if(q.t>q.wait&&q.hazards.length===0)fb112Start(b);return;}
 if(q.phase==='depart'){const u=clamp(q.t/1.4,0,1),v=1-u,P=q.from,A={x:P.x,y:P.y+90},Z=q.passFrom,C={x:Z.x+q.dir*100,y:Z.y-70};b.x=v*v*v*P.x+3*v*v*u*A.x+3*v*u*u*C.x+u*u*u*Z.x;b.y=v*v*v*P.y+3*v*v*u*A.y+3*v*u*u*C.y+u*u*u*Z.y;const dx=3*v*v*(A.x-P.x)+6*v*u*(C.x-A.x)+3*u*u*(Z.x-C.x),dy=3*v*v*(A.y-P.y)+6*v*u*(C.y-A.y)+3*u*u*(Z.y-C.y);q.heading=Math.atan2(dy,dx);q.parts.forEach(p=>p.angle=q.heading);if(u>=1){q.heading=Math.atan2(q.passTo.y-Z.y,q.passTo.x-Z.x);q.parts.forEach(p=>p.angle=q.heading);fb112Set(b,'warn');combatAudio0927(b,'bossWeaponCharge',.5);}return;}
 if(q.phase==='warn'){combatWarningTick(b,'fb112-'+q.seq,q.t,q.dur);q.pose=q.model==='razor'?2:0;if(q.t>=q.dur){fb112Set(b,'attack');combatAudio0927(b,q.attack==='pass'?'jetDash':'combatEnergy0927',.3);if(q.attack==='pass'){q.from=q.passFrom;q.to=q.passTo;q.heading=Math.atan2(q.to.y-q.from.y,q.to.x-q.from.x);q.parts.forEach(p=>p.angle=q.heading);}if(q.attack==='gates')for(const p of q.parts.filter(p=>p.type==='pressure'&&p.hp>0)){const at=fb112Bore(b,p);fb112Hazard(b,at.x,at.y,'tornado',p);}if(q.attack==='vortex')fb112Hazard(b,q.target.x,viewTopY()-40,'tornado');}return;}
 if(q.phase!=='attack')return;
 const attack=q.attack;
 if(attack==='guns'||attack==='shear'){
  if(q.model==='razor')q.pose=q.t<.25?2:0;
  const duration=attack==='guns'?1.55:1.8;
  if(q.t>=q.next&&q.t<duration){for(const p of(attack==='shear'?q.vents:q.parts.filter(p=>p.type==='gun'&&p.hp>0))){
   if(attack==='guns')fb112Shot(b,p,p.angle);else for(const d of[-.28,0,.28])fb112Shot(b,p,p.angle+d,true);
   combatAudio0927(p,attack==='guns'?'enemyMachineGunHeavy':'combatEnergy0927',.11);
  }q.next+=turretInterval15(attack==='guns'?.13:.42);}
  if(q.t>duration+.35){fb112Set(b,'recover');q.wait=1.35;}
 }else if(attack==='pass'){
  const u=clamp(q.t/1.05,0,1);b.x=lerp(q.from.x,q.to.x,u);b.y=lerp(q.from.y,q.to.y,u);q.pose=[0,4,5,6,7,8,9,10][Math.floor(u*16)%8];
  for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!q.hits.has(seat)&&fb112Opaque('razor_roll',fb112RollFrame(b),q.heading,q.scale*512/384,b.x,b.y,player.x,player.y)){q.hits.add(seat);playerHit('Razorwake rolling pass');}});
  if(u>=1){b.x=worldWidth()/2;b.y=viewTopY()-160;q.pose=0;q.heading=Math.PI/2;q.parts.forEach(p=>p.angle=q.heading);fb112Set(b,'recover');q.wait=2.4;}
 }else if(attack==='rail'){
  if(q.t>=q.next&&q.next===0){const gap=q.seq%3;for(let i=0;i<4;i++)if(i!==gap)fb112Hazard(b,q.columns[i],viewTopY()-45,'front');q.next=99;}
  if(q.t>3.1){fb112Set(b,'recover');q.wait=1.5;}
 }else if(attack==='eye'){
  if(q.t>=q.next&&q.t<3.6){for(const d of[-.95,-.75,-.55,.55,.75,.95])fb112Shot(b,null,Math.PI/2+d,true);q.next+=turretInterval15(.58);combatAudio0927(b,'overlordWind',.4);}
  if(q.t>4.0){fb112Set(b,'recover');q.wait=2;}
 }else if((attack==='gates'||attack==='vortex')&&q.t>3){fb112Set(b,'recover');q.wait=1.6;}
 if(q.model==='thunder'){b.x=worldWidth()/2+Math.sin(b.t*.8)*12;b.y=b.ty+Math.sin(b.t*1.1)*5;}
}
updateBoss=function(dt){return fb112Own(boss)?fb112Tick(boss,dt):FB112.base.tick.apply(this,arguments);};
updateSubBoss=function(dt){return fb112Own(subBoss)?fb112Tick(subBoss,dt):FB112.base.subtick.apply(this,arguments);};
function fb112Shadow(name,f,x,y,k,a){const B=FB112_ART.banks[name],n=f*B.dirs+(B.dirs>1?fb112Dir(a,B.dirs):0),key=B.key+':'+n;let c=FB112.shadows.get(key);if(!c){c=document.createElement('canvas');c.width=c.height=B.cell;const g=c.getContext('2d');g.drawImage(XART.get(B.key),n%B.cols*B.cell,Math.floor(n/B.cols)*B.cell,B.cell,B.cell,0,0,B.cell,B.cell);g.globalCompositeOperation='source-in';g.fillStyle='rgba(0,4,9,.45)';g.fillRect(0,0,B.cell,B.cell);FB112.shadows.set(key,c);}const s=B.cell*k;ctx.drawImage(c,x-s/2,y-s/2,s,s);}
function fb112Draw(b){const q=b._fb112,k=q.scale;if(!fb112Ready())return;
 const alive=q.death<3.0;
 if(alive){const shakeX=b.dead?Math.sin(q.death*91)*4:Math.sin(b.t*37)*.7;
  const rolling=fb112Rolling(b);
  if(rolling){const f=fb112RollFrame(b);fb112Shadow('razor_roll',f,b.x,b.y+55,k*512/384*.9,q.heading);fb112Blit('razor_roll',f,b.x,b.y,k*512/384,q.heading);}
  else{
  if(q.model==='razor')fb112Shadow('razor_body',q.pose,b.x,b.y+30,k*.9,q.heading);
  fb112Blit(q.model+'_body',q.pose,b.x+shakeX,b.y,k,q.heading);
  if(q.open&&q.core.flash>0)fb112Blit(q.model+'_hit',q.pose,b.x,b.y,k,q.heading);
  if(!b.dead&&q.core.flash<=0){ctx.save();ctx.globalCompositeOperation='lighter';fb112Blit(q.model+'_flow',Math.floor(b.t*16)%4,b.x,b.y,k,q.heading,false,.4+.3*Math.sin(b.t*7)**2);ctx.restore();}
  for(const p of q.parts){const at=fb112PartPoint(b,p),name=q.model+'_'+p.id,frame=p.type==='pressure'?q.phase==='warn'?Math.min(4,Math.floor(q.t/q.dur*5)):q.phase==='attack'&&q.attack==='gates'?4:0:p.recoil>.035?1:0;
   fb112Blit(name+(p.hp<=0?'_wreck':''),frame,at.x+shakeX,at.y,k,p.angle);if(p.flash>0)fb112Blit(name+'_hit',frame,at.x,at.y,k,p.angle);
   if(p.type==='gun'&&p.recoil>0&&p.hp>0){const m=fb112Bore(b,p),dir=fb112Dir(p.angle),f=dir*8+Math.floor(b.t*55)%8;fb112Blit('wind_muzzle',f,m.x,m.y,.62);}
  }
  for(const p of q.vents)if(!b.dead&&p.recoil>0){const m=fb112Bore(b,p);fb112Blit('wind_muzzle',fb112Dir(p.angle)*8+Math.floor(b.t*55)%8,m.x,m.y,.7);}
  }
  if(!b.dead)for(const e of q.M.engines){const roll=rolling?Math.cos(Math.max(0,q.M.clips.roll.indexOf(q.pose))*TAU/8):1,at=fb112Point(b,[q.M.cell/2+(e[0]-q.M.cell/2)*roll,e[1]]),scale=k*(q.model==='razor'?.36:.28);fb112Blit('exhaust',Math.floor(b.t*28)%4,at.x-Math.cos(q.heading)*96*scale,at.y-Math.sin(q.heading)*96*scale,scale,q.heading);}
 }
 for(const f of q.fx)fb112Blit('storm_burst',Math.min(3,Math.floor(f.t/.6*4)),f.x,f.y,f.size/256);
 for(const h of q.hazards)fb112Blit(h.kind==='tornado'?'tornado':'storm_burst',h.kind==='tornado'?(h.t>h.life-.35?6+Math.min(1,Math.floor((h.t-h.life+.35)/.35*2)):Math.floor(h.t*18)%6):Math.floor(h.t*14)%4,h.x,h.y,h.size/256);
 if(!b.dead&&q.phase==='warn'){
  if(q.attack==='guns')for(const p of q.parts.filter(p=>p.type==='gun'&&p.hp>0))fb112Warn(b,p,p.angle,q.t,q.dur,35);
  else if(q.attack==='shear')for(const p of q.vents)for(const d of[-.28,0,.28])fb112Warn(b,p,p.angle+d,q.t,q.dur,30);
  else if(q.attack==='pass')combatWarningDraw(b,{x:q.passFrom.x,y:q.passFrom.y,ex:q.passTo.x,ey:q.passTo.y,width:q.M.world*1.08,progress:q.t/q.dur,fieldOnly:true});
  else if(q.attack==='gates')for(const p of q.parts.filter(p=>p.type==='pressure'&&p.hp>0))fb112Warn(b,p,Math.PI/2,q.t,q.dur,110);
  else if(q.attack==='vortex')combatWarningDraw(b,{x:q.target.x,y:viewTopY(),ex:q.target.x,ey:VH,width:100,progress:q.t/q.dur,fieldOnly:true});
  else if(q.attack==='rail')for(let i=0;i<4;i++)if(i!==q.seq%3)combatWarningDraw(b,{x:q.columns[i],y:viewTopY(),ex:q.columns[i],ey:VH,width:90,progress:q.t/q.dur,fieldOnly:true});
  else if(q.attack==='eye')for(const d of[-.95,-.75,-.55,.55,.75,.95])fb112Warn(b,q.core,Math.PI/2+d,q.t,q.dur,30);
 }
 if(!b.dead&&q.attack==='eye'&&q.phase==='attack'){const at=fb112PartPoint(b,q.core);ctx.save();ctx.globalCompositeOperation='lighter';fb112Blit('hurricane',Math.floor(b.t*20)%4,at.x,at.y,1.7);ctx.restore();}
 if(b.sub&&!b.dead)drawSubBossBar(b);
}
drawBoss=function(){return fb112Own(boss)?fb112Draw(boss):FB112.base.draw.apply(this,arguments);};
drawSubBoss=function(){return fb112Own(subBoss)?fb112Draw(subBoss):FB112.base.subdraw.apply(this,arguments);};
globalThis.BOF_FURIOUS_ENCOUNTERS_1102={state:FB112,create:fb112Create,at:fb112At,damage:fb112Damage};
