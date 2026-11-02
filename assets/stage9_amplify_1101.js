"use strict";
/* S911: independent regular Stage9 identities. Event Horizon, Tidal and final
   encounter owners remain native. Source cells, measured bores, shared mixer. */
const S911={base:{spawn:spawnEnemy,draw:drawEnemy,model:r46Model,shield:drawEnemyShieldLayer,
 entry:enemyEntrySweep,frenzy:enemyFrenzyTick,route:eb11OwnsRoute,beginAI:ai27Begin,endAI:ai27End,
 shotPass:carrierAssaultShotPass111,early:ovSonicProjectileDraw,final:drawCombatFinalProjectile,
 element:enemyOrdnanceElement,break:ordnanceBreak1002,effects:updateEffects,flashes:drawNavalFlashes,intercept:enemyOrdnanceCanIntercept,kill:killEnemy,load:stageLoadBegin,begin:beginStage},
 serial:0,events:[],fx:[],hazards:new Set(),splashes:[],heavy:null,
 defs:{kami:{book:['burst','dash'],speed:135},comet:{book:['burst'],speed:190,pink:true},
 beacon:{book:['nine-orbs'],shield:38,spin:true},spinner:{book:['radial','radial-beam'],spin:true,heavy:true},
 jumper:{book:['burst','jump'],speed:145},beamship:{book:['twin-beam'],shield:42,heavy:true},
 skimmer:{book:['burst','water-fan'],speed:180},ringlaser:{book:['twin-beam','radial'],spin:true,heavy:true},
 gate:{book:['radial-beam','water-fan'],heavy:true},gleech:{book:['gravity-orbs','twin-beam']},
 prismbeam:{book:['twin-beam','water-fan'],shield:42,heavy:true},echo:{book:['burst','echo-run'],speed:190},
 singularity:{book:['nine-orbs','gravity-orbs'],spin:true},prismorb:{book:['water-fan','nine-orbs'],shield:32},
 minelayer:{book:['lay-mines'],speed:185},harrier:{book:['iris-beams','water-fan'],heavy:true,hp:260},
 manta:{book:['water-fan','swoop'],speed:155,pink:true},tidal:{book:['burst','tidal-waves'],speed:150},
 current:{book:['tidal-waves','grenades','superman'],heavy:true,hp:210}},
 aliases:{s9comet:'comet',s9beacon:'beacon',s9gateturret:'gate',wskim:'skimmer',gleech:'gleech',echof:'echo',pmine:'minelayer',vmanta:'manta',tsplit:'tidal',cbreak:'current',s9singularity:'singularity'}};
for(const B of Object.values(S911_ART.banks))XART._src[B.key]=B.path;
function s911Model(type,opt){return S911.aliases[type]||(type==='s9interceptor'?(opt._s9Role==='jumper'?'jumper':'kami'):type==='s9ring'?(opt._s9Role==='laser'?'ringlaser':'spinner'):type==='s9gunship'?(opt._s9Role==='laser'?'harrier':'beamship'):type==='s9prism'?(opt._s9Role==='orb'?'prismorb':'prismbeam'):null);}
function s911Keys(){return [...new Set(Object.values(S911_ART.banks).map(b=>b.key))];}
function s911M(e){return S911_ART.models[e?._s911?.model];}
function s911Live(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function s911Rank(){return ['furious','insanity'].includes(diffKey)?2:diffKey==='hard'?1:0;}
function s911Log(e,event,data={}){S911.events.push({id:e?._s911?.id,type:e?.type,event,t:efxClock,...data});if(S911.events.length>2000)S911.events.shift();}
function s911Angle(a){return Math.PI/2+v31Dir(a,32)*TAU/32;}
function s911Phase(e,phase){Object.assign(e._s911,{phase,t:0,beat:0,round:0});s911Log(e,phase,{attack:e._s911.attack});}
function s911Point(e,p,a=null){const A=e._s911,M=s911M(e),k=M.span/256,r=s911Angle(a??A.head)-Math.PI/2,x=(p[0]-128)*k,y=(p[1]-128)*k;return{x:e.x+x*Math.cos(r)-y*Math.sin(r),y:e.y+x*Math.sin(r)+y*Math.cos(r),angle:s911Angle(a??A.head)};}
function s911PartFrame(e,m){const A=e._s911;if(!m.bores)return 0;if(A.phase==='tell')return A.t<.45?Math.min(7,Math.floor(A.t/.45*8)):8;if(A.phase==='beam'||efxClock-(A.fired[m.index]??-99)<.12)return 9;return A.phase==='recover'&&A.t<.25?10:0;}
function s911Part(e,i){const A=e._s911,M=s911M(e),m=M.modules[i],p=s911Point(e,m.mount),angle=s911Angle(A.angles[i]??A.head+(m.baseAngle??Math.PI/2)-Math.PI/2),pose=s911Angle(angle-(m.baseAngle??Math.PI/2)+Math.PI/2),r=pose-Math.PI/2,k=M.span/256,f=s911PartFrame(e,m),v=m.bores?.[f]||m.muzzle,barrel=(m.baseAngle??Math.PI/2)+r,recoil=efxClock-(A.fired[i]??-99)<.09?1.6:0,x=p.x-Math.cos(barrel)*recoil,y=p.y-Math.sin(barrel)*recoil;return{x,y,angle:barrel,pose,f,tip:{x:x+(v[0]*Math.cos(r)-v[1]*Math.sin(r))*k,y:y+(v[0]*Math.sin(r)+v[1]*Math.cos(r))*k,angle:barrel,index:i}};}
function s911Pose(e){const A=e._s911;if(A.model!=='current')return 0;if(A.phase==='recover'&&efxClock<(A.holdUntil||0))return A.holdPose;if(A.phase==='flight')return A.t<.22?5:6;if(A.phase==='tell')return A.attack==='tidal-waves'?1:A.attack==='grenades'?2:4;if(A.phase==='fire')return A.attack==='grenades'?3:1;return 0;}
function s911Guns(e){const M=s911M(e),A=e._s911;if(A.model==='current'){const f=s911Pose(e);return M.poseGuns[f].map((p,i)=>({...s911Point(e,p,Math.PI/2),angle:A.head,index:i}));}return M.modules.length?M.modules.map((_,i)=>s911Part(e,i).tip):(M.guns.length?M.guns:[M.core]).map((p,i)=>({...s911Point(e,p),index:i}));}
spawnEnemy=function(type,x,y,opt={}){if(run.stage!==9||run._gp4StageX)return S911.base.spawn.apply(this,arguments);const name=s911Model(type,opt);if(!name)return S911.base.spawn.apply(this,arguments);const e=S911.base.spawn.apply(this,arguments);if(!e)return e;const M=S911_ART.models[name],D=S911.defs[name];for(const k of Object.keys(e))if(k.startsWith('_'))delete e[k];
 Object.assign(e,{type,art:M.bank.key,pattern:'s9refit',ground:false,shoots:false,armed:false,fk:null,fireCd:999,_fcd:999,vx:0,vy:0,spin:0,_noSep:true,w:M.span*.90,h:M.span*.94,_drawW:M.span,_drawH:M.span,_stagger:opt._stagger||0});
 if(D.hp)e.hp=Math.ceil(difficultyHealthBaseline15(D.hp,D.hp*[1,1.24,1.5][s911Rank()])*(coopActive()?1.5:1));e.maxhp=e._maxhp=e.hp;
 e._s911={id:++S911.serial,model:name,role:opt._s9Role,phase:name==='comet'?'pass':'entry',head:name==='comet'?(opt._side===-1?Math.PI:0):Math.PI/2,t:0,age:0,beat:0,round:0,cycle:0,angles:[],fired:[],beams:[],home:clamp(x,camLeftX()+110,camRightX()-110),side:opt._side||1};
 if(name==='current'){e._noBodyContact=true;e.w=M.extent[0]*M.span/256+10;e.h=M.extent[1]*M.span/256+10;}
 if(D.shield)enemyShieldEquip(e,'bubble_ice',Math.ceil(D.shield*DIFF.eHp),{once:true,regen:.025});s911Log(e,'spawn',{model:name,hp:e.hp,shield:e._esh?.max||0});return e;};
r46Model=function(e){return e?._s911?null:S911.base.model.apply(this,arguments);};
enemyEntrySweep=function(e){if(!e?._s911)return S911.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(!e?._s911)return S911.base.frenzy.apply(this,arguments);};
eb11OwnsRoute=function(e){return !!e?._s911||S911.base.route.apply(this,arguments);};
ai27Begin=function(e){if(!e?._s911)return S911.base.beginAI.apply(this,arguments);const old=ai27Context;ai27Context=null;return old;};
ai27End=function(e,old){if(!e?._s911)return S911.base.endAI.apply(this,arguments);ai27Context=old;};
drawEnemyShieldLayer=function(e){if(!e?._s911)return S911.base.shield.apply(this,arguments);};
function s911Fly(e,x,y,speed,turn,dt){const A=e._s911,a=Math.atan2(y-e.y,x-e.x);A.head+=clamp(s1aAngle(a-A.head),-turn*dt,turn*dt);e.x+=Math.cos(A.head)*speed*dt;e.y+=Math.sin(A.head)*speed*dt;}
function s911Mounts(e,dt,track){const A=e._s911,M=s911M(e),T=targetShip(e.x,e.y);M.modules.forEach((m,i)=>{m.index=i;const rest=A.head+(m.baseAngle??Math.PI/2)-Math.PI/2;if(A.angles[i]==null)A.angles[i]=rest;if(S911.defs[A.model].spin||A.attack==='radial-beam'){A.angles[i]=A.model==='gate'&&A.attack==='radial-beam'?A.head+i*TAU/M.modules.length:rest;return;}if(!track)return;const p=s911Point(e,m.mount),want=A.head+clamp(s1aAngle(Math.atan2(T.y-p.y,T.x-p.x)-A.head),-.65,.65);A.angles[i]+=clamp(s1aAngle(want-A.angles[i]),-dt*2.8,dt*2.8);});}
function s911Shot(e,p,kind='slug',speed=4.5,silent=false){if(!s911Live(e))return null;const physical=kind==='grenade'||kind==='mine',orb=/orb/.test(kind),b=eShootT(p.x,p.y,p.angle,speed,physical?'s9rift':'s9needle',{owner:e,noMuzzle:true,silent:true,w:orb?16:physical?22:7,h:orb?16:physical?22:21});if(!b||b.dead||b._ai27Held)return null;
 Object.assign(b,{_s911Kind:kind,_s911Owner:e,_s911Pink:!!S911.defs[e._s911.model].pink,_noArsenal:true,_weaponProof:!physical,_shootable:physical,_energyOrdnance:true,homing:false});if(physical){b.hp=3;b.life=10;}e._s911.fired[p.index??0]=efxClock;S911.fx.push({e,p:{...p},index:p.index,t:0,life:.10});
 if(!silent)combatAudio0927(e,physical||orb?'cfComboWater':'enemyHeavyLaser',.08);s911Log(e,'shot',{kind,index:p.index,x:p.x,y:p.y,angle:p.angle,attack:e._s911.attack});return b;}
enemyOrdnanceCanIntercept=function(b){return b?._s911Kind?['grenade','mine'].includes(b._s911Kind):S911.base.intercept.apply(this,arguments);};
function s911Lanes(e){const A=e._s911,M=s911M(e);let ports=s911Guns(e);return ports.map(p=>({...p,width:A.model==='beamship'?34:A.attack==='iris-beams'?22:20,len:1000}));}
function s911Start(e){const A=e._s911,D=S911.defs[A.model];if(D.heavy&&s911Live(S911.heavy)&&S911.heavy!==e)return;if(D.heavy)S911.heavy=e;A.attack=D.book[A.cycle%D.book.length];A.start={x:e.x,y:e.y};const T=targetShip(e.x,e.y);A.target={x:T.x,y:T.y};A.warm=A.attack==='iris-beams'?1.65:[1.08,.99,.92][s911Rank()];A.committed=false;s911Phase(e,'tell');A.lanes=s911Lanes(e);if(A.attack==='tidal-waves')A.lanes=[{x:e.x,y:e.y+25,angle:Math.PI/2,width:190,len:1000}];if(['dash','jump','swoop','echo-run','superman'].includes(A.attack))A.lanes=[{x:e.x,y:e.y,angle:Math.atan2(T.y-e.y,T.x-e.x),width:A.model==='current'?90:55,len:Math.hypot(T.x-e.x,T.y-e.y)+80}];combatAudio0927(e,'bossWeaponCharge',.6);}
function s911Finish(e){const A=e._s911;if(A.model==='current'){A.holdPose=s911Pose(e);A.holdUntil=efxClock+.18;}A.beams=[];A.lanes=[];A.cycle++;if(S911.heavy===e)S911.heavy=null;s911Phase(e,'recover');}
function s911Beam(e){const A=e._s911;A.lanes=s911Lanes(e);for(const p of A.lanes)S911.fx.push({e,p:{...p},index:p.index,t:0,life:.12});A.beams=A.lanes.map(p=>({p:{...p},t:0,life:A.model==='beamship'?1.5:1.1}));s911Phase(e,'beam');combatAudio0927(e,'enemyHeavyLaser',.4);s911Log(e,'beam-release',{lanes:A.beams.length});}
function s911Wave(e,side){const A=e._s911,p={x:clamp(A.target.x+side*115,camLeftX()+95,camRightX()-95),y:e.y+45,angle:Math.PI/2},b=s911Shot(e,p,'wave',2.1,true);if(b){b.w=180;b.h=24;b._s911Wave=true;}combatAudio0927(e,'cfComboWater',.18);s911Log(e,'wave-release',{x:p.x,y:p.y});}
function s911Grenade(e,p){const A=e._s911,target={x:clamp(A.target.x+(p.index?45:-45),camLeftX()+40,camRightX()-40),y:clamp(A.target.y,PLAY.y+100,VH-45)},b=s911Shot(e,p,'grenade',1,p.index>0);if(b){b._s911Hazard={kind:'grenade',target,age:0,flight:1.35};b.vx=(target.x-p.x)/1.35/60;b.vy=(target.y-p.y)/1.35/60;S911.hazards.add(b);}}
function s911Mine(e){const p=s911Point(e,s911M(e).bay||[128,170]),b=s911Shot(e,p,'mine',0);if(b){b.vx=b.vy=0;b._s911Hazard={kind:'mine',age:0,fuse:6.5,armed:false};S911.hazards.add(b);}}
function s911Tick(e,dt){if(!s911Live(e))return;const A=e._s911,D=S911.defs[A.model],M=s911M(e),r=s911Rank();A.age+=dt;A.t+=dt;A.beat-=dt;e.shoots=e.armed=false;
 if(e._stagger>0){e._stagger=Math.max(0,e._stagger-dt);return;}if(bossActive||subBossActive||bossDefeated||A.age>(D.heavy?43:31)){if(!A.cancelled){s911Cancel(e);A.cancelled=true;}e.y-=170*dt;if(e.y<-M.span)e.dead=true;return;}
 const entryY=PLAY.y+Math.max(115,M.span*.52);s911Mounts(e,dt,['entry','recover'].includes(A.phase)||A.phase==='tell'&&!A.committed||A.phase==='fire'&&!!D.speed);
 if(D.spin&&['fire','recover'].includes(A.phase))A.head+=dt*(A.phase==='fire'?1.9:.6);
 if(A.phase==='pass'){const vx=A.side*190,vy=32+Math.sin(A.age*2)*22;A.head=Math.atan2(vy,vx);e.x+=vx*dt;e.y+=vy*dt;if(A.beat<=0&&e.x>camLeftX()+30&&e.x<camRightX()-30){s911Guns(e).forEach((p,i)=>s911Shot(e,p,'slug',5,i>0));A.beat=.30;}if(e.x<-160||e.x>worldWidth()+160)e.dead=true;return;}
 if(A.phase==='entry'){if(D.speed)s911Fly(e,A.home,entryY+8,D.speed,3,dt);else e.y+=85*dt;if(e.y>=entryY){e.y=entryY;A.head=Math.PI/2;if(A.model==='current'){s911Phase(e,'transform');combatAudio0927(e,'cfComboWater',.5);}else s911Start(e);}}
 else if(A.phase==='transform'){if(A.t>=2.8){A.human=true;s911Log(e,'water-human-complete');s911Phase(e,'recover');}}
 else if(A.phase==='tell'){
  if(!A.committed&&/beam/.test(A.attack))A.lanes=s911Lanes(e);
  if(!A.committed&&A.t>A.warm*.60){A.committed=true;if(!['dash','jump','swoop','echo-run','superman','tidal-waves'].includes(A.attack))A.lanes=s911Lanes(e);}
  combatWarningTick(e,'s911-'+A.id,A.t,A.warm);
  if(A.t>=A.warm){if(/beam/.test(A.attack))s911Beam(e);else if(A.attack==='superman'){A.head=Math.atan2(A.target.y-e.y,A.target.x-e.x);s911Phase(e,'flight');combatAudio0927(e,'jetDash',.5);}else if(['dash','jump','swoop','echo-run'].includes(A.attack)){s911Phase(e,'dash');combatAudio0927(e,'jetDash',.5);}else s911Phase(e,'fire');}
 }else if(A.phase==='beam'){for(const b of A.beams){b.t+=dt;for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&player.invuln<=0&&ep13BeamTouches({x:b.p.x,y:b.p.y,a:b.p.angle,width:b.p.width,len:b.p.len,active:b.t>.08&&b.t<b.life-.1},player))playerHit('water laser');});}if(A.t>(A.beams[0]?.life||1))s911Finish(e);}
 else if(A.phase==='dash'){const dur=A.attack==='jump'?.95:.80,u=clamp(A.t/dur,0,1),a=Math.atan2(A.target.y-A.start.y,A.target.x-A.start.x),dist=Math.min(210,Math.max(0,Math.hypot(A.target.x-A.start.x,A.target.y-A.start.y)-65)),v=Math.sin(u*Math.PI);A.head=a;e.x=A.start.x+Math.cos(a)*dist*v;e.y=A.start.y+Math.sin(a)*dist*v;if(A.beat<=0){s911Guns(e).forEach((p,i)=>s911Shot(e,p,'slug',5.2,i>0));A.beat=.18;}if(u>=1){e.x=A.start.x;e.y=A.start.y;s911Finish(e);}}
 else if(A.phase==='flight'){const u=clamp(A.t/1.8,0,1),a=Math.atan2(A.target.y-A.start.y,A.target.x-A.start.x),dist=Math.min(210,Math.hypot(A.target.x-A.start.x,A.target.y-A.start.y)-70);A.head=a;e.x=A.start.x+Math.cos(a)*dist*Math.sin(u*Math.PI);e.y=A.start.y+Math.sin(a)*dist*Math.sin(u*Math.PI);if(A.t>.22&&A.beat<=0){s911Guns(e).forEach((p,i)=>s911Shot(e,{...p,angle:a+(i?.045:-.045)},'mist',4.2,i>0));A.beat=.10;}if(u>=1){e.x=A.start.x;e.y=A.start.y;s911Finish(e);}}
 else if(A.phase==='fire'){
  if(D.speed&&A.attack!=='lay-mines')s911Fly(e,A.home+Math.sin(A.t*1.6)*90,entryY+Math.sin(A.t*1.3)*24,D.speed*.48,1.6,dt);
  if(A.attack==='lay-mines'){s911Fly(e,A.home+Math.sin(A.age)*100,VH+250,210,1.8,dt);if(A.beat<=0&&e.y<VH-90){s911Mine(e);A.beat=turretInterval15(.62,[.62,.51,.42][r]);}if(e.y>VH+M.span)e.dead=true;}
  else if(A.beat<=0){const ports=s911Guns(e),atk=A.attack;
   if(atk==='tidal-waves'){s911Wave(e,A.round%2?1:-1);A.beat=.7;}
   else if(atk==='grenades'){ports.forEach(p=>s911Grenade(e,p));A.beat=.65;}
   else if(['nine-orbs','radial'].includes(atk)){const p=s911Point(e,M.core),n=atk==='nine-orbs'?9:Math.max(6,ports.length);for(let i=0;i<n;i++)s911Shot(e,{...p,angle:A.head+i*TAU/n},'laser-orb',2.9,i>0);A.beat=turretInterval15(.65,[.65,.55,.48][r]);}
   else ports.forEach((p,i)=>{const orbs=atk==='gravity-orbs',fan=atk==='water-fan';for(const o of fan?[-.19,0,.19]:[0])s911Shot(e,{...p,angle:p.angle+o},orbs?'laser-orb':'slug',orbs?2.6:4.8,i>0||o!==0);A.beat=turretInterval15(orbs?.42:.21,orbs?.42:[.21,.18,.15][r]);});
   A.round++;if(A.round>=(atk==='tidal-waves'?3:atk==='grenades'?2:['nine-orbs','radial','gravity-orbs'].includes(atk)?3:[5,6,7][r]))s911Finish(e);
  }
 }else if(A.phase==='recover'){if(D.speed)s911Fly(e,A.home,entryY,Math.min(140,D.speed),3,dt);else{e.x+=Math.sin(A.age*1.5)*8*dt;e.y+=Math.cos(A.age*1.8)*4*dt;}if(A.t>[1.18,1.02,.9][r]&&e.y>PLAY.y+65&&e.y<VH*.62){A.head+=clamp(s1aAngle(Math.PI/2-A.head),-dt*3,dt*3);if(Math.abs(s1aAngle(A.head-Math.PI/2))<.2)s911Start(e);}}
 if(e.x<camLeftX()-M.span||e.x>camRightX()+M.span||e.y>VH+M.span){e.dead=true;s911Cancel(e);}
}
function s911Cancel(e){playerLocks=playerLocks.filter(L=>L.src!==e);S911.fx=S911.fx.filter(f=>f.e!==e);if(e._s911){e._s911.beams=[];e._s911.lanes=[];}if(S911.heavy===e)S911.heavy=null;for(const b of S911.hazards)if(b._s911Owner===e&&b._s911Hazard.kind==='grenade'){b.dead=true;S911.hazards.delete(b);}e._combatWarnings={};s911Log(e,'cancel');}
function s911Visual(e){const A=e._s911,M=s911M(e),k=M.span/256,list=[],add=(B,f,p,a=A.head,glow=null,shield=null)=>list.push({B,f,p,angle:a,scale:k,glow,shield});
 if(A.model==='current'&&!A.human){add(A.phase==='transform'?M.morph:M.orb,A.phase==='transform'?Math.min(M.morph.frames-1,Math.floor(A.t/2.8*M.morph.frames)):0,e,Math.PI/2);return list;}
 const pose=s911Pose(e),angle=A.model==='current'?Math.PI/2:A.head;add(M.bank,pose,e,angle,M.glow,M.shield);M.modules.forEach((m,i)=>{const p=s911Part(e,i);add(m.bank,p.f,p,p.pose,m.glow,m.shield);});return list;}
function s911OpaqueAt(e,x,y,r=0){return s911Visual(e).some(q=>s811AlphaContact(q,x,y,r));}
carrierAssaultShotPass111=function(e,b){return e?._s911?!s911OpaqueAt(e,b.x,b.y,Math.max(b.w||2,b.h||2)*.5):S911.base.shotPass.apply(this,arguments);};
function s911DrawBeam(b){const p=b.p,B=S911_ART.banks.water_laser,size=p.width*64/18,step=size*.72,n={x:-Math.sin(p.angle)*p.width/2,y:Math.cos(p.angle)*p.width/2},end={x:p.x+Math.cos(p.angle)*p.len,y:p.y+Math.sin(p.angle)*p.len};ctx.save();ctx.beginPath();ctx.moveTo(p.x+n.x,p.y+n.y);ctx.lineTo(end.x+n.x,end.y+n.y);ctx.lineTo(end.x-n.x,end.y-n.y);ctx.lineTo(p.x-n.x,p.y-n.y);ctx.closePath();ctx.clip();for(let d=step*.5;d<p.len+step;d+=step)v31Blit(B,Math.floor(b.t*24)%B.frames,p.angle,p.x+Math.cos(p.angle)*d,p.y+Math.sin(p.angle)*d,size);ctx.restore();}
function s911Draw(e){const A=e._s911,M=s911M(e),dying=e._dyingT!=null,tint=e.flash>0?hitFlashColor(e):null;
 if(!dying)for(const t of M.tails){const p=s911Point(e,t),B=S911_ART.banks[(S911.defs[A.model].pink?'pink':'water')+'_thruster'];v31Blit(B,Math.floor(A.age*26)%B.frames,p.angle,p.x,p.y,40);}
 const list=s911Visual(e);for(const q of list){v31Blit(q.B,q.f,q.angle,q.p.x,q.p.y,q.B.cell*q.scale,tint);if(q.glow&&!tint&&!dying){ctx.save();ctx.globalCompositeOperation='lighter';v31Blit(q.glow,q.f,q.angle,q.p.x,q.p.y,q.B.cell*q.scale,null,(A.model==='current'?.34:1)*pxgStep(A.phase==='tell'?.45+.55*clamp(A.t/A.warm,0,1):.3+.65*Math.sin(A.age*8)**2));ctx.restore();}if(q.shield&&e._esh&&e._esh.phase!=='broken'&&!dying){ctx.save();ctx.globalCompositeOperation='lighter';v31Blit(q.shield,q.f,q.angle,q.p.x,q.p.y,q.B.cell*q.scale,null,e._esh.hitT>0?1:pxgStep(.5+.5*Math.sin(A.age*7)**2));ctx.restore();}}
 if(A.model==='beacon'&&!dying){ctx.save();ctx.globalCompositeOperation='lighter';const B=M.coreBank;v31Blit(B,0,A.head,e.x,e.y,B.cell*M.span/256,null,(A.model==='current'?.34:1)*pxgStep(A.phase==='fire'?1:.35+.65*Math.sin(A.age*10)**2));if(e._esh&&e._esh.phase!=='broken'){const B=S911_ART.banks.shield_serpent;v31Blit(B,Math.floor(A.age*26)%8,Math.PI/2,e.x,e.y,216,null,e._esh.hitT>0?1:.85);}ctx.restore();}
 if(A.phase==='tell'&&!dying&&(/beam/.test(A.attack)||['dash','jump','swoop','echo-run','superman','tidal-waves'].includes(A.attack))&&(A.attack!=='iris-beams'||A.t>.45))for(const p of A.lanes||[])combatWarningDraw(e,{x:p.x,y:p.y,ex:p.x+Math.cos(p.angle)*p.len,ey:p.y+Math.sin(p.angle)*p.len,width:p.width,progress:clamp((A.t-(A.attack==='iris-beams'?.45:0))/(A.warm-(A.attack==='iris-beams'?.45:0)),0,1),fieldOnly:true});
 if(!dying)for(const b of A.beams)s911DrawBeam(b);e._s911Rendered={model:A.model,phase:A.phase,pose:s911Pose(e),dir:v31Dir(A.model==='current'?Math.PI/2:A.head),heading:A.head,parts:list.length};
}
drawEnemy=function(e){return e?._s911&&!e.dead?s911Draw(e):S911.base.draw.apply(this,arguments);};
function s911Projectile(b){const kind=b._s911Kind,B=S911_ART.banks[kind==='wave'?'tidal_wave':kind==='grenade'?'water_grenade':kind==='mine'?'water_mine':kind==='laser-orb'?'water_orb':(b._s911Pink?'pink':'water')+'_'+(kind==='mist'?'laser':'slug')],size=kind==='wave'?200:kind==='grenade'?42:kind==='mine'?50:kind==='laser-orb'?40:kind==='mist'?44:32;return v31Blit(B,Math.floor(projectileVisualAge(b)*24)%B.frames,Math.atan2(b.vy,b.vx),b.x,b.y,size,b.flash>0?'#ffffff':null);}
ovSonicProjectileDraw=function(b){return b?._s911Kind?s911Projectile(b):S911.base.early.apply(this,arguments);};
drawCombatFinalProjectile=function(b){return b?._s911Kind?s911Projectile(b):S911.base.final.apply(this,arguments);};
enemyOrdnanceElement=function(b){return b?._s911Kind&&['mine','grenade'].includes(b._s911Kind)?'water':S911.base.element.apply(this,arguments);};
ordnanceBreak1002=function(b){if(b?._s911Kind){if(!b._s911Burst){b._s911Burst=true;s911Splash(b,b,false);}return;}return S911.base.break.apply(this,arguments);};
function s911Splash(b,p,damage=true){S911.splashes.push({x:p.x,y:p.y,t:0,life:.7});combatAudio0927(b._s911Owner,'cfComboWater',.15);for(const seat of seatList())withSeat(seat,()=>{if(damage&&!player.dead&&!player.out&&player.invuln<=0&&Math.hypot(player.x-p.x,player.y-p.y)<58)playerHit('water grenade');});s911Log(b._s911Owner,'water-explosion',{kind:b._s911Kind});b.dead=true;}
updateEffects=function(dt){const v=S911.base.effects.apply(this,arguments);for(const f of S911.fx)f.t+=dt;S911.fx=S911.fx.filter(f=>f.t<f.life&&s911Live(f.e));for(const b of S911.hazards){const h=b._s911Hazard;h.age+=dt;if(!b.dead){if(h.kind==='grenade'&&h.age>=h.flight)s911Splash(b,h.target);if(h.kind==='mine'){h.armed=h.age>.7;if(h.armed&&!h.triggered&&seatList().some(s=>{let close=false;withSeat(s,()=>{close=!player.dead&&!player.out&&Math.hypot(player.x-b.x,player.y-b.y)<86;});return close;})){h.triggered=true;h.fuse=Math.min(h.fuse,h.age+.85);combatAudio0927(b._s911Owner,'bossWeaponCharge',.5);}if(h.age>=h.fuse)s911Splash(b,b);}}if(b.dead||!eBullets.includes(b))S911.hazards.delete(b);}for(const s of S911.splashes)s.t+=dt;S911.splashes=S911.splashes.filter(s=>s.t<s.life);return v;};
drawNavalFlashes=function(){const r=S911.base.flashes.apply(this,arguments);for(const f of S911.fx){let p=f.p;if(f.index!=null)p=s911Guns(f.e)[f.index]||p;const B=S911_ART.banks[(S911.defs[f.e._s911.model].pink?'pink':'water')+'_muzzle'];v31Blit(B,Math.min(B.frames-1,Math.floor(f.t/f.life*B.frames)),p.angle,p.x,p.y,30);}for(const b of S911.hazards){const h=b._s911Hazard;if(h.kind==='grenade')groundTargetReticleDraw(h.target.x,h.target.y,112,clamp(h.age/h.flight,0,1),.9);else if(h.triggered)groundTargetReticleDraw(b.x,b.y,116,clamp(1-(h.fuse-h.age)/.85,0,1),.9);}for(const s of S911.splashes){const B=S911_ART.banks.water_splash;v31Blit(B,Math.min(B.frames-1,Math.floor(s.t/s.life*B.frames)),Math.PI/2,s.x,s.y,154);}return r;};
killEnemy=function(e){const r=S911.base.kill.apply(this,arguments);if(e?._s911&&!s911Live(e))s911Cancel(e);return r;};
stageLoadBegin=function(n,keys){if(n===9)keys=[...(keys||[]),...s911Keys(),...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];return S911.base.load.call(this,n,keys);};
beginStage=function(){S911.events=[];S911.fx=[];S911.hazards.clear();S911.splashes=[];S911.heavy=null;return S911.base.begin.apply(this,arguments);};
globalThis.BOF_STAGE9_REFIT={state:S911,art:S911_ART};
