"use strict";
/* Four additional Stage6 assault waves. New art is authored; the native actor
   lists still own damage, player weapon contacts, Retina, hit flash and rewards.
   Only a live assault holds the normal campaign dispatch/progress clock. */
const CA111={base:{spawn:spawnEnemy,kill:killEnemy,hit:hitEnemy,draw:drawEnemy,flashes:drawNavalFlashes,
 free:cp22Free,entry:enemyEntrySweep,
 play:updatePlay,begin:beginStage,plan:buildStagePlan,load:stageLoadBegin},clock:0,serial:0,
 actors:[],fx:[],queue:[],queued:new Set(),completed:new Set(),active:null,planned:false,
 masks:new Map(),events:[],nextLaser:0};
for(const B of Object.values(CA111_ART.banks))XART._src[B.key]=B.path;
function ca111Log(e,event,data={}){CA111.events.push({id:e?._ca111?.id||0,event,t:CA111.clock,...data});if(CA111.events.length>2400)CA111.events.shift();}
function carrierAssaultHold111(){return run.stage===6&&!run._gp4StageX&&!!CA111.active;}
function carrierAssaultPending111(){return run.stage===6&&!run._gp4StageX&&CA111.planned&&['pair-top','pair-bottom','nuclear','laser'].some(k=>!CA111.completed.has(k));}
function ca111Queue(kind,key){if(CA111.queued.has(key))return;CA111.queued.add(key);CA111.queue.push({kind,key});ca111Log(null,'queued',{kind,key});}
function ca111New(role,kind,x,y,hp){
 const e=CA111.base.spawn('s6turbine',x,y,{dropOk:role==='carrier'});if(!e)return null;
 for(const k of Object.keys(e))if(k.startsWith('_'))delete e[k];
 Object.assign(e,{type:kind+(role==='carrier'?'strategiccarrier':'strategicwarhead'),kind:role==='warhead'?kind+'Warhead':null,pattern:'s6storm',
 x,y,w:80,h:120,hp,maxhp:hp,score:role==='carrier'?16000:0,dropOk:role==='carrier',
 art:CA111_ART.banks[kind+'_hull'].key,shoots:false,armed:false,fireCd:999,fk:null,vx:0,vy:0,
 spin:0,flash:0,dead:false,_noSep:true,_noBodyContact:true,
 _ca111:{id:++CA111.serial,role,kind,age:0,phase:role==='carrier'?'entry':kind==='nuclear'?'rise':'south',t:0,frame:0,angle:Math.PI/2}});
 CA111.actors.push(e);return e;
}
function ca111Spawn(kind){
 if(run.stage!==6||run._gp4StageX||sc12Blocked())return null;
 const m=CA111_ART.models[kind],x=(camLeftX()+camRightX())/2,e=ca111New('carrier',kind,x,-m.worldSize*.6,EHP(180)*32);
 if(!e)return null;const q=e._ca111;q.lane=x;q.size=m.worldSize;q.cool=1.0;q.launches=0;
 e.w=m.worldSize*.32;e.h=m.worldSize*.70;ca111Log(e,'strategic-arrival',{kind,hp:e.hp});return e;
}
function ca111Deck(e,p){const q=e._ca111,k=q.size/512;return{x:e.x+(p[0]-256)*k,y:e.y+(p[1]-256)*k};}
function ca111Exhaust(p,a,size,phase=0,warm=false){
 const B=CA111_ART.banks[warm?'exhaust_amber':'exhaust'],d=v31Dir(a,B.dirs),ang=d*TAU/B.dirs,
  k=size/256,m=B.mount,x=(m[0]-128)*k,y=(m[1]-128)*k;
 v31Blit(B,(Math.floor(efxClock*26)+phase*2)%B.frames,a,p.x-x*Math.cos(ang)+y*Math.sin(ang),p.y-x*Math.sin(ang)-y*Math.cos(ang),size);
}
function ca111Launch(e,L){
 if(!sc12Alive(e)||e._ca111.phase!=='charge')return;
 const q=e._ca111,m=CA111_ART.models[q.kind],p=ca111Deck(e,m.bay),offset=q.kind==='laser'?(q.launches%2?-24:24):0,
  head=ca111New('warhead',q.kind,p.x+offset,p.y,EHP(65)*(q.kind==='nuclear'?3:2));if(!head)return;
 const a=head._ca111;a.parent=e;a.start={x:head.x,y:head.y};a.size=q.kind==='nuclear'?140:82;a.launchX=p.x+(q.launches%2?-65:65);
 a.target=clamp(player.x+(q.launches%2?-65:65),camLeftX()+70,camRightX()-70);
 a.fuse=q.kind==='nuclear'?[4.8,4.5,4.2][v31Rank()]:[8.0,7.6,7.2][v31Rank()];a.burstReady=CA111.clock+1.0;
 a.angle=q.kind==='nuclear'?Math.PI/2+v31Dir(Math.atan2(-75-p.y,a.launchX-p.x),32)*TAU/32:Math.PI/2;
 head.w=a.size*.38;head.h=a.size*.82;
 head._shootable=true;head._physicalMissile=true;head._noBodyContact=true;
 q.phase='release';q.t=0;q.launches++;q.frame=7;
 combatAudio0927(e,'atomicLaunch',.45);ca111Log(e,'launch',{kind:q.kind,warhead:a.id,x:head.x,y:head.y});
}
function ca111Carrier(e,dt){const q=e._ca111;
 q.age+=dt;q.t+=dt;e.x=q.lane+Math.sin(CA111.clock*24+q.id)*.75+Math.sin(CA111.clock*13)*.4;
 if(q.phase==='entry'){
  e.y+=58*dt;if(e.y>=VH*.47){e.y=VH*.47;q.phase='idle';q.t=0;ca111Log(e,'station');}
 }else{
  e.y=VH*.47+Math.sin(q.age*.65)*3+Math.sin(CA111.clock*27)*.4;
  if(q.phase==='idle'){
   q.frame=0;q.cool-=dt;
   if(q.cool<=0&&!player.dead&&CA111.actors.filter(a=>sc12Alive(a)&&a._ca111.role==='warhead'&&a._ca111.kind===q.kind).length<2){q.phase='open';q.t=0;combatAudio0927(e,'combatServo0927',.7);ca111Log(e,'door-opening');}
  }else if(q.phase==='open'){
   q.frame=Math.min(5,Math.floor(q.t/1.05*6));
   if(q.t>=1.05){q.phase='charge';q.t=0;q.frame=6;const warm=[2.1,1.85,1.6][v31Rank()];
    enemyLockOn(e,warm,{fire:L=>ca111Launch(e,L)});combatAudio0927(e,'bossWeaponCharge',.7);ca111Log(e,'launch-lock',{warm});}
  }else if(q.phase==='charge'){q.frame=6;if(player.dead){ca111CancelLauncher(e);q.phase='close';q.t=0;}}
  else if(q.phase==='release'){q.frame=7;if(q.t>.45){q.phase='close';q.t=0;}}
  else if(q.phase==='close'){q.frame=Math.max(0,5-Math.floor(q.t/.8*6));if(q.t>=.8){q.phase='idle';q.t=0;q.cool=[3.2,2.7,2.3][v31Rank()];}}
 }
}
function ca111CancelLauncher(e){playerLocks=playerLocks.filter(L=>L.src!==e);}
function carrierAssaultShotPass111(e,b){
 // A shootable missile is above its carrier deck. Let an approaching ordinary
 // player round reach that visible missile instead of hitting the hull below.
 if(e?._ca111?.role!=='carrier'||!(b?.vy<0))return false;
 return CA111.actors.some(h=>sc12Alive(h)&&h._ca111.role==='warhead'&&h._ca111.parent===e&&
  b.y>=h.y-h.h*.5&&Math.abs(b.x-h.x)<h.w*.5+(b.w||0)*.5+4&&!(b._hit||[]).includes(h));
}
function ca111Warning(e,remain,total){const q=e._ca111;
 if(!q.impact){q.warnStart={x:e.x,y:e.y};q.warnAt=remain;
  const speed=q.kind==='nuclear'?110:[18,20,22][v31Rank()];q.impact={x:e.x,y:Math.min(VH-44,e.y+remain*speed)};ca111Log(e,'detonation-commit',{...q.impact,seconds:remain});}
 const p=clamp(1-remain/q.warnAt,0,1);e.x=lerp(q.warnStart.x,q.impact.x,p);e.y=lerp(q.warnStart.y,q.impact.y,p);
 combatAudio0927(e,'alertLockon',Math.max(.08,remain*.23));
}
function ca111Warhead(e,dt){const q=e._ca111,oldX=e.x,oldY=e.y,oldPhase=q.phase;q.age+=dt;q.t+=dt;q.frame=Math.floor(q.age*18)%8;
 if(q.kind==='nuclear'){
  if(q.phase==='rise'){
   const p=clamp(q.t/1.7,0,1);e.x=lerp(q.start.x,q.launchX,p);e.y=lerp(q.start.y,-75,p);q.size=lerp(140,44,p);q.angle=-Math.PI/2;
   if(q.t>=1.7){q.phase='apex';q.t=0;q.apexX=e.x;ca111Log(e,'apex');}
  }else if(q.phase==='apex'){
   const p=clamp(q.t/.55,0,1);e.x=q.apexX+Math.sin(p*Math.PI)*28;q.angle=sc12Quant(-Math.PI/2+p*Math.PI);q.size=44;
   if(q.t>=.55){q.phase='fall';q.t=0;q.angle=Math.PI/2;ca111Log(e,'catch-up');}
  }else if(q.phase==='fall'){
  const p=clamp(q.t/q.fuse,0,1),remain=q.fuse-q.t;q.size=lerp(44,150,p);q.angle=Math.PI/2;
   if(remain>1.5){e.x+=clamp((q.target-e.x)*1.8*dt,-65*dt,65*dt);e.y+=(82+p*50)*dt;}
   else ca111Warning(e,remain,1.5);
   if(remain<=0){ca111Detonate(e);return;}
  }
 }else{
  const remain=q.fuse-q.age;q.size=lerp(82,150,clamp(q.age/.8,0,1));q.angle=Math.PI/2;
  if(remain>1.6)e.y+=[18,20,22][v31Rank()]*dt;
  else{q.burst=null;ca111Warning(e,remain,1.6);}
  if(remain<=0){ca111Detonate(e);return;}
  if(!q.impact&&q.age>1.0){
   if(!q.burst&&CA111.clock>=q.burstReady){const start=Math.max(CA111.clock,CA111.nextLaser);q.burst={start,fireAt:start+.72,end:start+1.12,len:Math.min(240,60+(q.age-1)*[20,24,28][v31Rank()])};CA111.nextLaser=start+.62;ca111Log(e,'radial-warning',{len:q.burst.len});}
   if(q.burst){const B=q.burst;if(CA111.clock<B.fireAt)combatWarningTick(e,'radial',Math.max(0,CA111.clock-B.start),.72);
    else if(!B.fired){B.fired=true;combatAudio0927(e,'enemyHeavyLaser',.4);ca111Log(e,'radial-lasers',{len:B.len});}
    if(CA111.clock>B.end){q.burst=null;q.burstReady=CA111.clock+.22;}}
  }
 }
 if(q.kind==='nuclear'&&q.phase!=='apex'&&oldPhase!=='apex'&&Math.hypot(e.x-oldX,e.y-oldY)>.01){const B=CA111_ART.banks.nuclear_head;q.angle=Math.PI/2+v31Dir(Math.atan2(e.y-oldY,e.x-oldX),B.dirs)*TAU/B.dirs;}
 e._noBodyContact=q.kind==='nuclear'?q.phase!=='fall'||q.size<85:q.age<.55;
 const a=q.angle-Math.PI/2,co=Math.abs(Math.cos(a)),si=Math.abs(Math.sin(a));e.w=q.size*(.38*co+.82*si);e.h=q.size*(.82*co+.38*si);
}
function ca111FX(kind,x,y,size,harmful=true){const f={kind,x,y,size,t:0,life:kind==='laser_tornado'?3.8:1.65,harmful,hitSeats:{}};CA111.fx.push(f);return f;}
function ca111Detonate(e){const q=e._ca111;if(e.dead)return;e.dead=true;e.hp=0;q.burst=null;
 ca111FX(q.kind==='nuclear'?'nuclear_blast':'laser_tornado',e.x,e.y,q.kind==='nuclear'?460:310,true);
 combatAudio0927(e,q.kind==='nuclear'?'nuclearDetonate':'combatEnergy0927',.5);shake=Math.max(shake,q.kind==='nuclear'?3:1.5);ca111Log(e,'timed-detonation',{kind:q.kind,x:e.x,y:e.y});}
function ca111FXFrame(f){if(f.kind!=='laser_tornado')return Math.min(7,Math.floor(f.t/f.life*8));
 if(f.t<.36)return Math.min(3,Math.floor(f.t/.09));if(f.t<3.15)return 4+Math.floor((f.t-.36)*16)%6;return Math.min(11,10+Math.floor((f.t-3.15)/.325));}
function ca111Mask(B){let m=CA111.masks.get(B.key);if(m)return m;if(!XART.rdy(B.key))return null;
 const c=document.createElement('canvas');c.width=B.cw;c.height=B.ch*B.frames;const g=c.getContext('2d');g.drawImage(XART.get(B.key),0,0);m=g.getImageData(0,0,c.width,c.height);CA111.masks.set(B.key,m);return m;}
function ca111HazardTouches(f,p){const B=CA111_ART.banks[f.kind],m=ca111Mask(B);if(!m)return false;const frame=ca111FXFrame(f),k=256/f.size;
 for(const dx of[-6,0,6])for(const dy of[-6,0,6]){const x=Math.round(128+(p.x+dx-f.x)*k),y=Math.round(128+(p.y+dy-f.y)*k);if(x<0||x>=256||y<0||y>=256)continue;const i=((frame*256+y)*256+x)*4;if(m.data[i+3]>145&&Math.max(m.data[i],m.data[i+1],m.data[i+2])>150)return true;}return false;}
function ca111Rays(e){const q=e._ca111,B=CA111_ART.banks.laser_head,s=B.sockets[q.frame],angles=[[-Math.PI,-3*Math.PI/4],[-Math.PI/2,-Math.PI/4],[3*Math.PI/4,Math.PI/2],[0,Math.PI/4]],out=[];
 if(!s||s.length<4)return out;for(let i=0;i<4;i++)for(const a of angles[i])out.push({x:e.x+(s[i][0]-128)*q.size/256,y:e.y+(s[i][1]-128)*q.size/256,a,width:12,len:q.burst?.len||0,active:!!q.burst?.fired});return out;}
function ca111Contacts(){
 for(const e of CA111.actors)if(sc12Alive(e)&&e._ca111.role==='warhead'&&e._ca111.kind==='laser'&&e._ca111.burst?.fired)for(const ray of ca111Rays(e))for(const s of seatList())withSeat(s,()=>{if(!player.dead&&!player.out&&ep13BeamTouches(ray,player))playerHit();});
 for(const f of CA111.fx)if(f.harmful&&f.t>.10&&f.t<f.life-.2)for(const s of seatList())withSeat(s,()=>{if(player.dead||player.out||f.hitSeats[s])return;if(ca111HazardTouches(f,player)){f.hitSeats[s]=true;playerHit();}});
}
function ca111Tick(dt){if(sc12DialogueHold())return;CA111.clock+=dt;
 if(!CA111.active&&CA111.queue.length&&!sc12Blocked()&&!CC111.carriers.some(c=>!c.done)){
  const wave=CA111.queue.shift();if(wave.kind.startsWith('pair-')){const group=sc12Pair(wave.kind.slice(5));if(group)CA111.active={...wave,group};else CA111.queue.unshift(wave);}
  else{const e=ca111Spawn(wave.kind);if(e)CA111.active={...wave,actor:e};else CA111.queue.unshift(wave);}
  if(CA111.active)ca111Log(null,'assault-start',{kind:wave.kind,key:wave.key});
 }
 for(const e of CA111.actors){if(e.dead||e._dyingT!=null)continue;const q=e._ca111;
  if(sc12Blocked()){ca111CancelLauncher(e);q.burst=null;if(q.role==='carrier'){q.phase='withdraw';e.y-=100*dt;if(e.y<-q.size)e.dead=true;}else e.dead=true;continue;}
  if(q.role==='carrier')ca111Carrier(e,dt);else ca111Warhead(e,dt);
 }
 for(const f of CA111.fx)f.t+=dt;CA111.fx=CA111.fx.filter(f=>f.t<f.life);
 CA111.actors=CA111.actors.filter(e=>!e.dead);
 // Live warheads are physically in front of the deck. Native primary-round
 // collision must meet the visible missile before the larger hull underneath.
 const front=enemies.filter(e=>e._ca111?.role==='warhead');
 if(front.length)enemies=front.sort((a,b)=>b.y-a.y).concat(enemies.filter(e=>e._ca111?.role!=='warhead'));
 const A=CA111.active;if(A){const done=A.group?A.group.done:A.actor.dead;
  if(done&&!CA111.actors.some(e=>e._ca111.role==='warhead')&&!CA111.fx.length){CA111.completed.add(A.key);ca111Log(null,'assault-complete',{key:A.key});CA111.active=null;}}
}
killEnemy=function(e){const q=e?._ca111;if(!q)return CA111.base.kill.apply(this,arguments);if(e.dead||e._dyingT!=null)return;
 ca111CancelLauncher(e);q.burst=null;
 if(q.role==='warhead'){e.dead=true;e.hp=0;ca111FX(q.kind==='nuclear'?'nuclear_blast':'laser_tornado',e.x,e.y,90,false);combatAudio0927(e,'combatModule0927',.25);ca111Log(e,'warhead-intercepted');return;}
 ca111FX(q.kind==='nuclear'?'nuclear_blast':'laser_tornado',e.x,e.y,300,false);CA111.base.kill(e);ca111Log(e,'strategic-defeat');
};
hitEnemy=function(e){if(e?._ca111?.role==='warhead'&&!enemyOrdnanceCanIntercept(e))return;return CA111.base.hit.apply(this,arguments);};
function ca111Draw(e){const q=e._ca111;
 if(q.role==='carrier'){
  const m=CA111_ART.models[q.kind],B=CA111_ART.banks[m.hull],G=CA111_ART.banks[m.glow],D=CA111_ART.banks[m.door],p=ca111Deck(e,m.bay);
  if(e._dyingT==null)for(let i=0;i<m.engines.length;i++)ca111Exhaust(ca111Deck(e,m.engines[i]),Math.PI/2,124,i,q.kind==='nuclear');
  sc12Blit(B,0,Math.PI/2,e.x,e.y,q.size,q.size,e.flash>0?hitFlashColor(e):null);
  if(!(e.flash>0)&&e._dyingT==null){ctx.save();ctx.globalCompositeOperation='lighter';sc12Blit(G,0,Math.PI/2,e.x,e.y,q.size,q.size,null,pxgStep(.5+.5*Math.sin(efxClock*7)));ctx.restore();}
  sc12Blit(D,q.frame,Math.PI/2,p.x,p.y,m.doorWorld[0],m.doorWorld[1],e.flash>0?hitFlashColor(e):null);
  carrierDeckShadow111(e,B,q.size,q.size);
 }else{
  const B=CA111_ART.banks[q.kind+'_head'],d=v31Dir(q.angle,B.dirs),a=d*TAU/B.dirs,
    x=(B.tail[0]-128)*q.size/256,y=(B.tail[1]-128)*q.size/256,p={x:e.x+x*Math.cos(a)-y*Math.sin(a),y:e.y+x*Math.sin(a)+y*Math.cos(a)};
  ca111Exhaust(p,q.angle+Math.PI,80,Math.floor(q.age*4),q.kind==='nuclear');v31Blit(B,q.frame,q.angle,e.x,e.y,q.size,e.flash>0?hitFlashColor(e):null);
  if(q.burst){for(const ray of ca111Rays(e)){
   if(!q.burst.fired){const k=clamp((CA111.clock-q.burst.start)/.72,0,1);combatWarningDraw(e,{x:ray.x,y:ray.y,ex:ray.x+Math.cos(ray.a)*ray.len,ey:ray.y+Math.sin(ray.a)*ray.len,len:ray.len,width:12,progress:k,fieldOnly:true});}
   else{const b=CA111_ART.banks.laser_ray,size=12*b.cell/b.alphaWidth;for(let z=size*.4;z<ray.len;z+=size*b.segmentStep)v31Blit(b,Math.floor(q.age*28)%b.frames,ray.a,ray.x+Math.cos(ray.a)*z,ray.y+Math.sin(ray.a)*z,size);}
  }}
  if(q.impact){const remain=q.kind==='nuclear'?q.fuse-q.t:q.fuse-q.age;groundTargetReticleDraw(q.impact.x,q.impact.y,q.kind==='nuclear'?360:230,clamp(1-remain/q.warnAt,0,1),.85);campText(Math.max(0,remain).toFixed(1)+'S',e.x+q.size*.44,e.y-q.size*.15,10,'#ffca7c');}
  if(q.phase==='fall'||q.kind==='laser')bossShootGraphic(e.x,e.y-q.size*.18);
 }
 q.rendered={key:CA111_ART.banks[q.role==='carrier'?q.kind+'_hull':q.kind+'_head'].key,frame:q.frame,size:q.size};
}
drawEnemy=function(e){if(e?._ca111){if(!e.dead&&e._ca111.role==='carrier')ca111Draw(e);return;}return CA111.base.draw.apply(this,arguments);};
drawNavalFlashes=function(){const out=CA111.base.flashes.apply(this,arguments);
 for(const e of CA111.actors.filter(e=>sc12Alive(e)&&e._ca111.role==='warhead').sort((a,b)=>a.y-b.y))ca111Draw(e);
 for(const f of CA111.fx)v31Blit(CA111_ART.banks[f.kind],ca111FXFrame(f),Math.PI/2,f.x,f.y,f.size);return out;};
cp22Free=function(){return !carrierAssaultHold111()&&CA111.base.free.apply(this,arguments);};
enemyEntrySweep=function(e){if(e?._ca111)return;return CA111.base.entry.apply(this,arguments);};
updatePlay=function(dt){const active=state===GS.PLAY&&run.stage===6&&!run._gp4StageX;if(active)ca111Tick(dt);const out=CA111.base.play.apply(this,arguments);if(active&&state===GS.PLAY&&!sc12Blocked())ca111Contacts();return out;};
beginStage=function(){for(const e of CA111.actors)ca111CancelLauncher(e);CA111.actors=[];CA111.fx=[];CA111.queue=[];CA111.queued.clear();CA111.completed.clear();CA111.active=null;CA111.planned=false;CA111.clock=CA111.nextLaser=0;return CA111.base.begin.apply(this,arguments);};
stageLoadBegin=function(n,keys){if(n===6)keys=[...(keys||[]),...Object.values(CA111_ART.banks).map(b=>b.key),'fx_ground_target_reticle','boss_shoot_prompt'];return CA111.base.load.call(this,n,keys);};
buildStagePlan=function(n){const P=CA111.base.plan.apply(this,arguments);if(n===6&&!run._gp4StageX){CA111.planned=true;for(const [t,kind,key]of[[18,'pair-top','pair-top'],[35,'pair-bottom','pair-bottom'],[51,'nuclear','nuclear'],[66,'laser','laser']])P.push({t,fn:()=>ca111Queue(kind,key),_ca111:key});P.sort((a,b)=>a.t-b.t);}return P;};
globalThis.BOF_CARRIER_ASSAULT={state:CA111,art:CA111_ART,queue:ca111Queue,spawn:ca111Spawn};
