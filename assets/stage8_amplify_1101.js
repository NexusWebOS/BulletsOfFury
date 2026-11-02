"use strict";
/* Stage8 regular roster, deliberately separate from Herald and Dracodia.
   Authored whole identities, independent source-pixel joints, one real pool
   per unit, native damage/shield/death/Retina/mixer ownership. */
const S811={base:{spawn:spawnEnemy,draw:drawEnemy,entry:enemyEntrySweep,frenzy:enemyFrenzyTick,
 beginAI:ai27Begin,endAI:ai27End,route:eb11OwnsRoute,kill:killEnemy,hit:hitEnemy,
 load:stageLoadBegin,begin:beginStage,early:ovSonicProjectileDraw,final:drawCombatFinalProjectile,
 intercept:enemyOrdnanceCanIntercept,effects:updateEffects,flashes:drawNavalFlashes,
 model:r46Model,shield:drawEnemyShieldLayer,plan:buildStagePlan,shotPass:carrierAssaultShotPass111},serial:0,events:[],fx:[],blasts:[],bombs:new Set(),heavy:null,alpha:new Map(),
 aliases:{s8interceptor:'interceptor',s8spread:'interceptor',s8needlejet:'imp',mm1003_impharrow:'imp',s8scout:'hexpyre',mm1003_hexpyre:'hexpyre',s8voidjet:'voidjet',s8laserharrier:'harrier',s8hellwing:'hellwing',s8parasite:'parasite',s8crescent:'crescent',s8hunter:'hunter',s8stalker1003:'hunter',s8skull:'skull',s8symbiote:'symbiote',s8gunship:'warp',s8warpsentinel:'warp',s8carrier:'carrier',s8deathorb:'deathorb',s8manta:'blue',mm1003_bluehybrid:'blue',mm1003_furnacemaw:'furnacemaw',s8furnacemaw:'furnacemaw',s8bomber:'bomber',s8tentacle:'tentacle'},
 retired:new Set(['s8leech','s8gravity1003','s8razor','s8solar','s8prism1003','ll18raptor','ll18spear','ll18herald','ll18brood']),
 defs:{
 interceptor:{hp:44,book:['laser-burst','beam'],theme:'void',speed:120},imp:{hp:30,book:['depth-spin','hell-burst'],theme:'fire'},
 hexpyre:{hp:70,book:['flamethrower','fire-orbs','fire-beam'],theme:'fire'},voidjet:{hp:420,absolute:true,book:['dark-orbs','dark-beam','missiles'],theme:'void',heavy:true},
 harrier:{hp:110,book:['beam','laser-burst'],theme:'void'},hellwing:{hp:95,book:['hell-burst','missiles','turbo'],theme:'fire',speed:165},
 parasite:{hp:66,book:['void-needles','pincer'],theme:'void'},crescent:{hp:88,book:['laser-burst','sweep'],theme:'void',speed:155},
 hunter:{hp:92,book:['blue-beam','lash'],theme:'blue'},skull:{hp:60,book:['bone-burst','bone-fan'],theme:'void',speed:135},
 symbiote:{hp:72,book:['dark-orbs','void-needles'],theme:'void',speed:140},warp:{hp:156,book:['magma-fire','magma-void','fire-beam'],theme:'fire',heavy:true},
 carrier:{hp:180,book:['laser-burst','bay'],theme:'void',heavy:true},deathorb:{hp:100,book:['dark-orbs','radial-beam'],theme:'void'},
 blue:{hp:450,absolute:true,book:['blue-fan','blue-beam','core-burst'],theme:'blue',heavy:true},furnacemaw:{hp:120,book:['fire-orbs','flamethrower'],theme:'fire'},
 bomber:{hp:124,book:['bombing'],theme:'void',speed:165},tentacle:{hp:142,book:['grasp'],theme:'void'}}};
for(const B of Object.values(S811_ART.banks))XART._src[B.key]=B.path;
delete S8MEGA.s8leech; // The retired enemy has no preload/spawn/art owner.
for(const k of Object.keys(XART._src))if(/armored_leech|s81003_gravity/.test(k))delete XART._src[k];
function s811Keys(){const keys=new Set();for(const [name,M]of Object.entries(S811_ART.models)){for(const B of[M.bank,M.glow,M.spin,M.hatch?.bank])if(B)keys.add(B.key);if(name==='tentacle')keys.add(M.shield.key);for(const m of[...M.modules,...(M.arms||[]).flatMap(a=>a.links)]){keys.add(m.bank.key);keys.add(m.glow.key);if(name==='tentacle')keys.add(m.shield.key);}}for(const[n,B]of Object.entries(S811_ART.banks))if((/^(fire|void|blue)_/.test(n)&&!n.endsWith('_flame'))||/^(bone|bomb|darkorb|flame)$/.test(n))keys.add(B.key);return[...keys];}
function s811Live(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function s811M(e){return S811_ART.models[e?._s811?.model];}
function s811Rank(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
function s811Log(e,event,data={}){S811.events.push({id:e?._s811?.id,type:e?.type,event,t:efxClock,...data});if(S811.events.length>2200)S811.events.shift();}
function s811Angle(a,n=32){return Math.PI/2+v31Dir(a,n)*TAU/n;}
function s811Point(e,p,a=null){const A=e._s811,M=s811M(e),k=M.span/256*(A.depth||1),head=s811Angle(a??A.head),r=head-Math.PI/2,x=(p[0]-128)*k,y=(p[1]-128)*k;return{x:e.x+x*Math.cos(r)-y*Math.sin(r),y:e.y+x*Math.sin(r)+y*Math.cos(r),angle:head};}
function s811Part(e,i){const A=e._s811,M=s811M(e),m=M.modules[i],p=s811Point(e,m.mount),angle=s811Angle(A.angles[i]??A.head),r=angle-Math.PI/2,k=M.span/256*(A.depth||1),recoil=efxClock-(A.fired[i]??-99)<.09?2*(A.depth||1):0,x=p.x-Math.cos(angle)*recoil,y=p.y-Math.sin(angle)*recoil;
 return{x,y,angle,tip:{x:x+(m.muzzle[0]*Math.cos(r)-m.muzzle[1]*Math.sin(r))*k,y:y+(m.muzzle[0]*Math.sin(r)+m.muzzle[1]*Math.cos(r))*k,angle}};}
function s811Arm(e,arm){const A=e._s811,M=s811M(e),out=[],p0=s811Point(e,arm.root),k=M.span/256*(A.depth||1),ai=M.arms.indexOf(arm);let p=p0;
 arm.links.forEach((m,j)=>{const swing=A.phase==='strike'?(A.attack==='grasp'?Math.sin(clamp(A.t/.85,0,1)*Math.PI)*.82:Math.sin(clamp(A.t/.68,0,1)*Math.PI)*.72):A.phase==='tell'&&['grasp','lash'].includes(A.attack)?-.24:.11*Math.sin(A.age*3+ai+j*.8),sign=(arm.root[0]<128?-1:1)*Math.sign(arm.links[0].joint[1]||1),a=s811Angle(A.head+sign*swing*(j?1.1:1)),r=a-Math.PI/2,tip={x:p.x+(m.joint[0]*Math.cos(r)-m.joint[1]*Math.sin(r))*k,y:p.y+(m.joint[0]*Math.sin(r)+m.joint[1]*Math.cos(r))*k};out.push({m,p:{...p},angle:a,tip});p=tip;});return out;}
function s811Phase(e,phase){Object.assign(e._s811,{phase,t:0,round:0,beat:0});s811Log(e,phase,{attack:e._s811.attack});}
function s811Fly(e,x,y,speed,turn,dt){const A=e._s811,w=Math.atan2(y-e.y,x-e.x);A.head+=clamp(s1aAngle(w-A.head),-turn*dt,turn*dt);e.x+=Math.cos(A.head)*speed*dt;e.y+=Math.sin(A.head)*speed*dt;}
function s811Attach(e,model,type,opt){const M=S811_ART.models[model],D=S811.defs[model];
 for(const k of Object.keys(e))if(k.startsWith('_')&&!['_dyingT','_dieDur','_maxhp'].includes(k))delete e[k];
 Object.assign(e,{type,name:({voidjet:'DARK MATTER DREADJET',harrier:'ALIEN LASER HARRIER',hellwing:'HELLWING JET',warp:'WARP SENTINEL',blue:'BLUE HYBRID',furnacemaw:'FURNACE MAW'})[model]||model.toUpperCase(),pattern:'s8mega',art:M.bank.key,
 ground:false,shoots:false,armed:false,fk:null,fireCd:999,_fcd:999,_atk:'none',vx:0,vy:0,spin:0,flash:0,_noSep:true,_noHit:false,_continueEligible:false,w:M.span*.90,h:M.span*.94,_drawW:M.span,_drawH:M.span,_stagger:opt?._stagger||0});
 const hp=D.absolute?Math.ceil(difficultyHealthBaseline15(D.hp,D.hp*[1,1.30,1.62][s811Rank()])*(coopActive()?1.5:1)):EHP(D.hp);e.hp=e.maxhp=e._maxhp=hp;
 e._s811={id:++S811.serial,model,phase:'entry',age:0,t:0,beat:0,round:0,cycle:0,head:Math.PI/2,angles:[],fired:[],beams:[],children:[],home:clamp(e.x,camLeftX()+100,camRightX()-100),side:e.x<worldWidth()/2?1:-1,hullHP:hp};
 if(model==='tentacle'){enemyShieldEquip(e,'bubble_void',Math.ceil(48*DIFF.eHp),{once:true,regen:.025});e._noBodyContact=true;}
 if(model==='hunter')e._noBodyContact=true;
 s811Log(e,'spawn',{model,hp,shield:e._esh?.max||0});return e;
}
spawnEnemy=function(type,x,y,opt={}){
 if(run.stage!==8||run._gp4StageX)return S811.base.spawn.apply(this,arguments);
 if(S811.retired.has(type))return null;
 if(type==='modturret'){if(opt._modWeapon==='sonic')return null;type='s8laserharrier';}
 const model=S811.aliases[type];if(!model)return S811.base.spawn.call(this,type,x,y,opt);
 const e=S811.base.spawn.call(this,'s8interceptor',x,y,opt);return e?s811Attach(e,model,type,opt):e;
};
buildStagePlan=function(n){const p=S811.base.plan.apply(this,arguments);if(n!==8)return p;const replace={10:'s8voidjet',13:'s8hellwing',27:'s8tentacle',41:'s8carrier'};
 return p.map(w=>replace[w.t]?{...w,fn:()=>spawnEnemy(replace[w.t],worldWidth()*.5,-170,{})}:w);};
r46Model=function(e){return e?._s811?null:S811.base.model.apply(this,arguments);};
enemyEntrySweep=function(e){if(!e?._s811)return S811.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(!e?._s811)return S811.base.frenzy.apply(this,arguments);};
eb11OwnsRoute=function(e){return !!e?._s811||S811.base.route.apply(this,arguments);};
ai27Begin=function(e,dt){if(!e?._s811)return S811.base.beginAI.apply(this,arguments);const old=ai27Context;ai27Context=null;return old;};
ai27End=function(e,old){if(e?._s811){ai27Context=old;return;}return S811.base.endAI.apply(this,arguments);};
drawEnemyShieldLayer=function(e){if(!e?._s811)return S811.base.shield.apply(this,arguments);};
function s811Guns(e,role='gun'){return s811M(e).modules.map((m,i)=>({m,i})).filter(q=>q.m.role===role).map(q=>({...s811Part(e,q.i).tip,index:q.i}));}
function s811Mounts(e,dt,track){const A=e._s811,M=s811M(e),T=targetShip(e.x,e.y);M.modules.forEach((m,i)=>{if(A.angles[i]==null)A.angles[i]=A.head;if(!track)return;const p=s811Point(e,m.mount),want=A.head+clamp(s1aAngle(Math.atan2(T.y-p.y,T.x-p.x)-A.head),-.72,.72);A.angles[i]+=clamp(s1aAngle(want-A.angles[i]),-2.6*dt,2.6*dt);});}
function s811LaneWidth(attack){return /flame/.test(attack)?Math.ceil(S811_ART.banks.flame.width*245/S811_ART.banks.flame.length):/beam/.test(attack)?22:20;}
function s811Shot(e,p,kind,speed=4.2,silent=false){if(!s811Live(e))return null;const theme=S811.defs[e._s811.model].theme,physical=kind==='missile'||kind==='bomb',orb=/orb/.test(kind),native=physical?'emissile':orb?'s8pair':'s8needle';
 const b=eShootT(p.x,p.y,p.angle,speed,kind==='bomb'?'s8rift':native,{owner:e,noMuzzle:true,silent:true,w:orb?22:physical?12:8,h:orb?22:physical?28:22});if(!b||b.dead||b._ai27Held)return null;
 Object.assign(b,{_s811Kind:kind,_s811Theme:theme,_s811Owner:e,_noArsenal:true,_weaponProof:!(physical||orb),_shootable:physical||orb,_energyOrdnance:!physical,homing:false});
 if(physical){b.hp=kind==='bomb'?3:2;b.life=8;b.spd=speed;b.turn=.06;}if(orb){b.hp=3;b.life=7;}
 e._s811.fired[p.index??0]=efxClock;S811.fx.push({e,p:{...p},from:{x:e.x,y:e.y},index:p.index,t:0,life:.10,theme,size:orb?40:30});
 if(!silent)combatAudio0927(e,physical?'enemyMissile':orb?'combatEnergy0927':kind==='bone'?'enemyMachineGunHeavy':'enemyHeavyLaser',.075);
 s811Log(e,'shot',{kind,theme,index:p.index,x:p.x,y:p.y,angle:p.angle,attack:e._s811.attack});return b;}
enemyOrdnanceCanIntercept=function(b){return b?._s811Kind?b._s811Kind==='missile'||b._s811Kind==='bomb'||/orb/.test(b._s811Kind):S811.base.intercept.apply(this,arguments);};
function s811Start(e){const A=e._s811,D=S811.defs[A.model],r=s811Rank(),T=targetShip(e.x,e.y);if(D.heavy&&s811Live(S811.heavy)&&S811.heavy!==e)return;
 if(D.heavy)S811.heavy=e;A.attack=D.book[A.cycle%D.book.length];A.target={x:T.x,y:T.y};A.start={x:e.x,y:e.y};A.warm=A.attack==='turbo'?1.15:A.attack==='grasp'?1.1:[1.02,.90,.82][r];A.committed=false;s811Phase(e,'tell');
 A.lanes=s811Guns(e).map(p=>({...p,angle:p.angle,width:s811LaneWidth(A.attack),len:/flame/.test(A.attack)?245:1000}));
 if(A.model==='hunter'&&A.attack==='blue-beam')A.lanes.push({...s811Point(e,s811M(e).eyes[0]),width:18,len:1000});
 if(['grasp','lash','pincer','turbo'].includes(A.attack))A.lanes=[{x:e.x,y:e.y,angle:Math.atan2(T.y-e.y,T.x-e.x),width:A.attack==='grasp'?90:62,len:Math.min(650,Math.hypot(T.x-e.x,T.y-e.y)+80)}];
 if(A.attack==='radial-beam')A.lanes=s811Guns(e).map((p,i)=>({...p,angle:Math.PI/4+i*TAU/4,width:18,len:1000}));
 if(A.attack==='bombing'){s811Phase(e,'bombing');A.drop=.2;}
 if(A.attack!=='missiles'&&A.attack!=='bombing')combatAudio0927(e,'bossWeaponCharge',.5);
}
function s811Finish(e){const A=e._s811;if(A.beams.some(b=>b.flame))combatAudio0927(e,'flameThrowerEnd',.3);A.beams=[];A.lanes=[];A.cycle++;if(S811.heavy===e)S811.heavy=null;s811Phase(e,'recover');}
function s811Beam(e,flame=false){const A=e._s811;A.beams=A.lanes.map(p=>({p:{...p},t:0,life:flame?1.25:1.0,flame,theme:A.attack==='blue-beam'?'blue':A.attack==='dark-beam'?'void':A.attack==='fire-beam'?'fire':S811.defs[A.model].theme}));s811Phase(e,'beam');combatAudio0927(e,flame?'flameThrowerStart':'enemyHeavyLaser',.4);s811Log(e,'beam-release',{flame,theme:A.beams[0]?.theme,lanes:A.lanes.length});}
function s811LaunchMissiles(e){const A=e._s811,ports=s811Guns(e,'missile');s811Phase(e,'lock');for(let i=0;i<[4,5,6][s811Rank()];i++)enemyLockOn(e,.95+i*.14,{fire:L=>{if(!s811Live(e)||e._s811.phase!=='lock')return;const ps=s811Guns(e,'missile'),p=ps[i%ps.length];if(!p)return;const b=s811Shot(e,p,'missile',3.5,i%2>0);if(b)s811Log(e,'missile-release',{lock:L.id});}});}
function s811Bomb(e){const A=e._s811,M=s811M(e),p=s811Point(e,M.bay||[128,146]),T=targetShip(e.x,e.y),flight=1.35,target={x:clamp(p.x+Math.sin(A.age*2)*80,camLeftX()+45,camRightX()-45),y:clamp(Math.max(p.y+150,T.y),PLAY.y+100,VH-50)},b=s811Shot(e,p,'bomb',1);
 if(b){b.vx=(target.x-p.x)/flight/60;b.vy=(target.y-p.y)/flight/60;b._s811Bomb={target,age:0,flight};S811.bombs.add(b);s811Log(e,'bomb-drop',{target});}}
function s811Strike(e,dt){const A=e._s811,M=s811M(e),T=targetShip(e.x,e.y),r=s811Rank();
 if(A.attack==='turbo'){e.x+=Math.cos(A.lanes[0].angle)*[540,640,730][r]*dt;e.y+=Math.sin(A.lanes[0].angle)*[540,640,730][r]*dt;if(A.beat<=0){s811Guns(e).forEach((p,i)=>s811Shot(e,p,'hell-slug',5.4,i>0));A.beat=.15;}if(A.t>.42)s811Finish(e);return;}
 const dur=A.attack==='grasp'?.85:.68,u=clamp(A.t/dur,0,1),travel=Math.min(300,Math.max(0,Math.hypot(A.target.x-A.start.x,A.target.y-A.start.y)-40)),a=Math.atan2(A.target.y-A.start.y,A.target.x-A.start.x),v=Math.sin(u*Math.PI);e.x=A.start.x+Math.cos(a)*travel*v;e.y=A.start.y+Math.sin(a)*travel*v;
 if(u>.17&&u<.86){const chains=(M.arms||[]).flatMap(arm=>s811Arm(e,arm));const claws=M.modules.filter(m=>m.role==='claw').map(m=>s811Part(e,M.modules.indexOf(m)));for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out||player.invuln>0)return;const touch=chains.some(q=>s81003Distance(player.x,player.y,{x:q.p.x,y:q.p.y,ex:q.tip.x,ey:q.tip.y})<12)||claws.some(q=>s81003Distance(player.x,player.y,{x:q.x,y:q.y,ex:q.tip.x,ey:q.tip.y})<14);if(touch)playerHit(A.model==='tentacle'?'tentacle grasp':'alien lash');});}
 if(u>=1){e.x=A.start.x;e.y=A.start.y;s811Finish(e);}
}
function s811Tick(e,dt){if(!s811Live(e))return;const A=e._s811,D=S811.defs[A.model],M=s811M(e),r=s811Rank(),T=targetShip(e.x,e.y);A.age+=dt;A.t+=dt;A.beat-=dt;e.shoots=e.armed=false;
 if(e._stagger>0){e._stagger=Math.max(0,e._stagger-dt);return;}
 if(bossActive||subBossActive||bossDefeated||A.age>(D.absolute?44:32)){if(!A.cancelled){s811Cancel(e);A.cancelled=true;}e.y-=180*dt;if(e.y<-M.span)e.dead=true;return;}
 s811Mounts(e,dt,A.phase==='entry'||A.phase==='recover'||A.phase==='tell'&&A.t<A.warm*.5);
 if(A.attack==='radial-beam'&&A.phase==='tell'){A.angles=M.modules.map((_,i)=>Math.PI/4+i*TAU/4);A.lanes=s811Guns(e).map((p,i)=>({...p,angle:A.angles[i],width:18,len:1000}));}
 const entryY=PLAY.y+Math.max(125,M.span*.54);
 if(A.phase==='launch'){const u=clamp(A.t/.65,0,1),p=s811Live(A.launchOwner)?s811Point(A.launchOwner,s811M(A.launchOwner).bay):A.launchPoint;A.depth=.45+.55*u;e.x=p.x+A.launchSide*(20+u*40);e.y=p.y+u*105;e.w=M.span*.90*A.depth;e.h=M.span*.94*A.depth;if(u>=1){A.depth=1;s811Phase(e,'recover');}return;}
 if(A.phase==='entry'){
  if(D.speed){s811Fly(e,A.home,entryY+8,D.speed,3,dt);}else e.y+=85*dt;
  if(e.y>entryY&&e.x>camLeftX()+60&&e.x<camRightX()-60){A.head=Math.PI/2;s811Start(e);}
 }else if(A.phase==='tell'){
  if(A.model==='hunter'&&A.t<A.warm*.5){const want=Math.atan2(A.target.y-e.y,A.target.x-e.x);A.head+=clamp(s1aAngle(want-A.head),-dt*2.6,dt*2.6);}
  if(!A.committed&&A.t>=A.warm*.5){A.committed=true;if(/flame/.test(A.attack))A.angles=A.angles.map(a=>s811Angle(a,16));if(!['grasp','lash','pincer','turbo','radial-beam'].includes(A.attack))A.lanes=s811Guns(e).map(p=>({...p,width:s811LaneWidth(A.attack),len:/flame/.test(A.attack)?245:1000}));if(A.model==='hunter'&&A.attack==='blue-beam')A.lanes.push({...s811Point(e,M.eyes[0]),width:18,len:1000});}
  combatWarningTick(e,'s811-'+A.id,A.t,A.warm);
  if(A.t>=A.warm){if(A.attack==='missiles')s811LaunchMissiles(e);else if(/beam/.test(A.attack)||A.attack==='flamethrower')s811Beam(e,A.attack==='flamethrower');else if(['grasp','lash','pincer','turbo'].includes(A.attack)){s811Phase(e,'strike');combatAudio0927(e,A.attack==='turbo'?'jetDash':'combatServo0927',.4);}else if(A.attack==='depth-spin')s811Phase(e,'spin');else if(A.attack==='bay'){s811Phase(e,'bay');combatAudio0927(e,'combatServo0927',.5);}else s811Phase(e,'fire');}
 }else if(A.phase==='spin'){if(A.t>1.35)s811Finish(e);}
 else if(A.phase==='lock'){if(A.t>2.1)s811Finish(e);}
 else if(A.phase==='beam'){
  for(const b of A.beams){b.t+=dt;for(const seat of seatList())withSeat(seat,()=>{const active=b.t>.07&&b.t<b.life-.08;if(!player.dead&&!player.out&&player.invuln<=0&&active&&(b.flame?s811AlphaContact({B:S811_ART.banks.flame,f:Math.floor(b.t*24)%8,p:b.p,angle:b.p.angle,scale:b.p.len/S811_ART.banks.flame.length},player.x,player.y,8):ep13BeamTouches({x:b.p.x,y:b.p.y,a:b.p.angle,width:b.p.width,len:b.p.len,active},player)))playerHit(b.flame?'alien flamethrower':'alien laser');});}
  if(A.t>(A.beams[0]?.life||1))s811Finish(e);
 }else if(A.phase==='strike')s811Strike(e,dt);
 else if(A.phase==='bay'){
  if(A.t>1.0&&A.round<2&&A.beat<=0){const p=s811Point(e,M.bay);A.children=A.children.filter(s811Live);if(A.children.length<2){const side=A.round?1:-1,child=spawnEnemy('s8interceptor',p.x+side*20,p.y,{_stagger:.12});if(child){Object.assign(child._s811,{phase:'launch',launchOwner:e,launchPoint:p,launchSide:side,depth:.45,home:clamp(p.x+side*85,camLeftX()+80,camRightX()-80)});A.children.push(child);s811Log(e,'fighter-launch',{child:child._s811?.id});}}A.round++;A.beat=.45;combatAudio0927(e,'jetDash',.35);}
  if(A.t>2.7)s811Finish(e);
 }else if(A.phase==='bombing'){
  s811Fly(e,A.home+Math.sin(A.age*1.3)*125,VH+230,165,1.7,dt);A.drop-=dt;if(A.drop<=0&&e.y<VH-120){s811Bomb(e);A.drop=[.62,.50,.40][r];}if(e.y>VH+M.span)e.dead=true;
 }else if(A.phase==='fire'){
  if(D.speed)s811Fly(e,A.home+Math.sin(A.t*1.3)*125,PLAY.y+160+Math.sin(A.t)*28,D.speed*.65,1.4,dt);
  if(A.beat<=0){let ports=s811Guns(e);if(!ports.length)ports=[{...s811Point(e,[128,159]),index:0}];const atk=A.attack,kind=atk==='bone-burst'||atk==='bone-fan'?'bone':atk==='fire-orbs'||atk==='magma-fire'?'fire-orb':atk==='magma-void'||atk==='dark-orbs'||atk==='core-burst'?'dark-orb':atk==='hell-burst'?'hell-slug':atk==='blue-fan'?'blue-laser':'laser';
   ports.forEach((p,i)=>{const offsets=/fan/.test(atk)?[-.20,0,.20]:[0];offsets.forEach((a,j)=>s811Shot(e,{...p,angle:p.angle+a},kind,/orb/.test(kind)?2.5:kind==='bone'?4.7:5.0,i>0||j>0));});A.beat=turretInterval15(/orb/.test(kind)?.38:.20,/orb/.test(kind)?[.38,.32,.27][r]:[.20,.17,.14][r]);A.round++;
   if(A.round>=(/orb/.test(kind)?[3,4,5][r]:[5,6,8][r]))s811Finish(e);}
 }else if(A.phase==='recover'){
  if(D.speed)s811Fly(e,A.home,entryY,Math.min(160,D.speed),3,dt);else{e.x+=Math.sin(A.age*1.4)*10*dt;e.y+=Math.cos(A.age*1.7)*5*dt;}
  if(A.t>[1.15,.95,.8][r]&&e.y>PLAY.y+55&&e.y<VH*.58){A.head+=clamp(s1aAngle(Math.PI/2-A.head),-dt*3,dt*3);if(Math.abs(s1aAngle(A.head-Math.PI/2))<.20)s811Start(e);}
 }
 if(e.x<camLeftX()-M.span||e.x>camRightX()+M.span||e.y>VH+M.span){e.dead=true;s811Cancel(e);}
}
function s811Cancel(e){playerLocks=playerLocks.filter(L=>L.src!==e);S811.fx=S811.fx.filter(f=>f.e!==e);if(e._s811){if(e._s811.beams.some(b=>b.flame))combatAudio0927(e,'flameThrowerEnd',.3);e._s811.beams=[];e._s811.lanes=[];}if(S811.heavy===e)S811.heavy=null;e._combatWarnings={};s811Log(e,'cancel');}
function s811Visual(e){const A=e._s811,M=s811M(e),k=M.span/256*(A.depth||1),list=[],add=(B,f,p,a=A.head,scale=k,glow=null,shield=null)=>list.push({B,f,p,angle:a,scale,glow,shield});
 if(A.phase==='spin'&&M.spin){const f=Math.floor(A.t/1.35*8)%8;add(M.spin,f,e,Math.PI/2);return list;}
 add(M.bank,0,e,A.head,k,M.glow,M.shield);
 M.modules.forEach((m,i)=>{const p=s811Part(e,i);add(m.bank,0,p,p.angle,k,m.glow,m.shield);});
 for(const arm of M.arms||[])for(const q of s811Arm(e,arm))add(q.m.bank,0,q.p,q.angle,k,q.m.glow,q.m.shield);
 if(M.hatch){const f=A.phase==='bay'?A.t<.85?Math.min(3,Math.floor(A.t/.85*4)):A.t<2?3:A.t<2.7?Math.min(7,4+Math.floor((A.t-2)/.7*4)):7:0;add(M.hatch.bank,f,s811Point(e,M.hatch.point),A.head,k*M.hatch.scale);}
 return list;
}
function s811Alpha(q){const B=q.B,d=v31Dir(q.angle,B.dirs),f=clamp(q.f|0,0,B.frames-1),key=B.key+':'+f+':'+d;let a=S811.alpha.get(key);if(a)return a;if(!XART.rdy(B.key))return null;
 const c=document.createElement('canvas');c.width=c.height=B.cell;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(XART.get(B.key),d%B.cols*B.cell,(f*B.dirRows+Math.floor(d/B.cols))*B.cell,B.cell,B.cell,0,0,B.cell,B.cell);a=g.getImageData(0,0,B.cell,B.cell).data;S811.alpha.set(key,a);if(S811.alpha.size>160)S811.alpha.delete(S811.alpha.keys().next().value);return a;
}
function s811AlphaContact(q,x,y,radius=0){const c=q.B.cell,s=q.scale,u=(x-q.p.x)/s+c/2,v=(y-q.p.y)/s+c/2,r=Math.ceil(radius/s);if(u+r<0||v+r<0||u-r>=c||v-r>=c)return false;const a=s811Alpha(q);if(!a)return false;for(let yy=Math.max(0,Math.floor(v-r));yy<=Math.min(c-1,Math.ceil(v+r));yy++)for(let xx=Math.max(0,Math.floor(u-r));xx<=Math.min(c-1,Math.ceil(u+r));xx++)if(a[(yy*c+xx)*4+3]>80)return true;return false;}
function s811OpaqueAt(e,x,y,radius=0){return s811Visual(e).some(q=>s811AlphaContact(q,x,y,radius));}
carrierAssaultShotPass111=function(e,b){if(!e?._s811)return S811.base.shotPass.apply(this,arguments);return !s811OpaqueAt(e,b.x,b.y,Math.max(b.w||2,b.h||2)*.5);};
function s811Draw(e){const A=e._s811,M=s811M(e),tint=e.flash>0?hitFlashColor(e):null,dying=e._dyingT!=null,k=M.span/256;
 if(!dying)for(const t of M.tails){const p=s811Point(e,t),B=S811_ART.banks[S811.defs[A.model].theme+'_thruster'];v31Blit(B,Math.floor(A.age*26)%B.frames,p.angle,p.x,p.y,38*(A.depth||1));}
 const list=s811Visual(e);for(const q of list){v31Blit(q.B,q.f,q.angle,q.p.x,q.p.y,q.B.cell*q.scale,tint);
  if(q.glow&&!tint&&!dying){ctx.save();ctx.globalCompositeOperation='lighter';const gain=A.phase==='tell'?.25+.75*clamp(A.t/A.warm,0,1):.3+.6*Math.sin(A.age*8)**2;v31Blit(q.glow,q.f,q.angle,q.p.x,q.p.y,q.B.cell*q.scale,null,pxgStep(gain));ctx.restore();}
  if(q.shield&&e._esh&&e._esh.phase!=='broken'&&!dying){ctx.save();ctx.globalCompositeOperation='lighter';v31Blit(q.shield,q.f,q.angle,q.p.x,q.p.y,q.B.cell*q.scale,null,(e._esh.phase==='deploy'?clamp(e._esh.animT/.34,0,1):1)*(e._esh.hitT>0?.95:pxgStep(.35+.65*Math.sin(A.age*7)**2)));ctx.restore();}
 }
 e._s811Rendered={model:A.model,dir:v31Dir(A.head),parts:list.length,frame:A.phase==='spin'?Math.floor(A.t/1.35*8)%8:0,phase:A.phase};
 if(!dying&&A.phase==='tell'&&A.attack!=='missiles')for(const L of A.lanes||[])combatWarningDraw(e,{x:L.x,y:L.y,ex:L.x+Math.cos(L.angle)*L.len,ey:L.y+Math.sin(L.angle)*L.len,width:L.width,progress:clamp(A.t/A.warm,0,1),fieldOnly:true});
 if(!dying)for(const b of A.beams)s811DrawBeam(b);
}
function s811DrawBeam(b){const p=b.p;if(b.flame){const B=S811_ART.banks.flame;v31Blit(B,Math.floor(b.t*24)%B.frames,p.angle,p.x,p.y,B.cell*p.len/B.length);return;}const B=S811_ART.banks[b.theme+'_laser'],size=p.width*64/18,step=size*.73,n={x:-Math.sin(p.angle)*p.width/2,y:Math.cos(p.angle)*p.width/2},end={x:p.x+Math.cos(p.angle)*p.len,y:p.y+Math.sin(p.angle)*p.len};ctx.save();ctx.beginPath();ctx.moveTo(p.x+n.x,p.y+n.y);ctx.lineTo(end.x+n.x,end.y+n.y);ctx.lineTo(end.x-n.x,end.y-n.y);ctx.lineTo(p.x-n.x,p.y-n.y);ctx.closePath();ctx.clip();for(let d=step*.5;d<p.len+step;d+=step)v31Blit(B,Math.floor(b.t*24)%B.frames,p.angle,p.x+Math.cos(p.angle)*d,p.y+Math.sin(p.angle)*d,size);ctx.restore();}
drawEnemy=function(e){if(e?._s811&&!e.dead)return s811Draw(e);return S811.base.draw.apply(this,arguments);};
function s811Projectile(b){const kind=b._s811Kind,theme=b._s811Theme||'void',B=S811_ART.banks[kind==='bone'?'bone':kind==='bomb'?'bomb':kind==='dark-orb'?'darkorb':kind==='fire-orb'?'fire_orb':theme+'_'+(kind==='missile'?'missile':/slug/.test(kind)?'slug':'laser')],age=projectileVisualAge(b),f=Math.floor(age*(kind==='bone'?26:22))%B.frames,size=/orb/.test(kind)?48:kind==='bone'?38:kind==='bomb'?54:kind==='missile'?44:34;return v31Blit(B,f,Math.atan2(b.vy,b.vx),b.x,b.y,size);}
ovSonicProjectileDraw=function(b){return b?._s811Kind?s811Projectile(b):S811.base.early.apply(this,arguments);};
drawCombatFinalProjectile=function(b){return b?._s811Kind?s811Projectile(b):S811.base.final.apply(this,arguments);};
updateEffects=function(dt){const r=S811.base.effects.apply(this,arguments);for(const f of S811.fx)f.t+=dt;S811.fx=S811.fx.filter(f=>f.t<f.life&&s811Live(f.e));
 for(const b of S811.bombs){const q=b._s811Bomb;q.age+=dt;if(!b.dead&&q.age>=q.flight){b.dead=true;q.impact=true;S811.blasts.push({e:b._s811Owner,x:q.target.x,y:q.target.y,t:0,life:.72});combatAudio0927(b._s811Owner,'combatEnergy0927',.14);for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&player.invuln<=0&&Math.hypot(player.x-q.target.x,player.y-q.target.y)<55)playerHit('dark matter bomb');});s811Log(b._s811Owner,'bomb-impact',{x:q.target.x,y:q.target.y});}if(b.dead||!eBullets.includes(b))S811.bombs.delete(b);}
 for(const b of S811.blasts)b.t+=dt;S811.blasts=S811.blasts.filter(b=>b.t<b.life);return r;};
drawNavalFlashes=function(){const r=S811.base.flashes.apply(this,arguments);for(const f of S811.fx){let p={x:f.p.x+f.e.x-f.from.x,y:f.p.y+f.e.y-f.from.y,angle:f.p.angle};if(f.index!=null&&s811M(f.e).modules[f.index])p=s811Part(f.e,f.index).tip;const B=S811_ART.banks[f.theme+'_muzzle'];v31Blit(B,Math.min(B.frames-1,Math.floor(f.t/f.life*B.frames)),p.angle,p.x,p.y,f.size);}for(const b of S811.bombs){const q=b._s811Bomb;groundTargetReticleDraw(q.target.x,q.target.y,100,clamp(q.age/q.flight,0,1),.9);}for(const b of S811.blasts)s81003Cell('shatter',Math.min(15,Math.floor(b.t/b.life*16)),b.x,b.y,144,144,1);return r;};
killEnemy=function(e){const r=S811.base.kill.apply(this,arguments);if(e?._s811&&!s811Live(e))s811Cancel(e);return r;};
stageLoadBegin=function(n,keys){if(n===8)keys=[...(keys||[]),...s811Keys(),...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];return S811.base.load.call(this,n,keys);};
beginStage=function(){S811.events=[];S811.fx=[];S811.blasts=[];S811.bombs.clear();S811.heavy=null;return S811.base.begin.apply(this,arguments);};
globalThis.BOF_ALIEN_REFIT={state:S811,art:S811_ART};
