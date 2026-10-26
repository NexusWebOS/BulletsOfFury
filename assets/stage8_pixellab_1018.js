"use strict";
/* Mike's Stage 8 redesign: three encounters; main plus FOUR finite copies.
   PixelLab frames own the poses. One module rig owns hits, locks and muzzles.
   The established Dracodia death / red portal / reunion pays the one reward. */
const V18={base:{spawn:spawnBoss,tick:r30Tick,draw:r30DrawBoss,parts:r30Parts,pose:r30Pose,
 hit:modularHit,at:r30At,targets:retinaBossTargets,encounter:j3Encounter,mimic:j3Mimic,
 morph:j3Morph,home:j3Home,save:j3Save,next:j3Next,attack:r30Attack,attackTick:r30AttackTick,
 break:r30Break,gauge:fmcGauge,load:stageLoadBegin,warm:r30Warm,arena:v17ArenaDraw,
 world:drawWorld,body:j3Body,locked:dr5Locked},forms:[0,8,1,6,2],names:{0:'colossus',8:'hammer',1:'helicopter',6:'harrier',2:'volcano'},
 events:[],draws:{},masks:new Map(),crops:new Map(),last:null};
function v18Owned(b){return run.stage===8&&!!b?._r30?.v18;}
dr5Locked=function(){if(v18Owned(boss)&&boss._r30.mode.startsWith('v18'))return state===GS.PLAY;return V18.base.locked.apply(this,arguments);};
function v18Log(b,event,data={}){V18.events.push({event,phase:j3State(b)?.encounter,form:b._r30.v18.form,clock:b._r30.clock,...data});if(V18.events.length>700)V18.events.shift();}
function v18Keys(){return [...Object.values(V18_ART.models).flatMap(m=>m.frames.flatMap(f=>Object.values(f).map(a=>a.key))),...Object.values(V18_ART.clips).flatMap(c=>c.frames.map(a=>a.key)),V18_ART.drone.key,...['fire','fire_root','fire_tip'].flatMap(k=>P2_ART[k].map(a=>a.key))];}
for(const m of Object.values(V18_ART.models))for(const f of m.frames)for(const a of Object.values(f))XART._src[a.key]=a.path;
for(const c of Object.values(V18_ART.clips))for(const a of c.frames)XART._src[a.key]=a.path;
XART._src[V18_ART.drone.key]=V18_ART.drone.path;
function v18Warm(){let ready=true;for(const k of v18Keys())if(!XART.rdy(k))ready=false;return ready;}
stageLoadBegin=function(n,keys){return V18.base.load.call(this,n,n===8?[...(keys||[]),...v18Keys()]:keys);};
r30Warm=function(){const out=V18.base.warm.apply(this,arguments);if(run.stage===8)v18Warm();return out;};
function v18Model(b){const J=j3State(b);return J.encounter===0?'infused':J.encounter===1?'ghost':V18.names[b._r30.v18.form];}
function v18Size(b){return Math.min(410,viewW()*.96);}
function v18Frame(b){const m=V18_ART.models[v18Model(b)],t=b._r30.clock||0;return m.frames[Math.floor(t*m.fps)%m.frames.length];}
function v18SetMode(b,mode){const S=b._r30;S.mode=mode;S.t=0;S.attack=null;b.enter=mode!=='fight';b._noHit=b.enter;v18Log(b,'mode',{mode});}
function v18Clear(b){j3Clear(b);for(const q of groundTargetingFx)if(q.owner===b)q.dead=true;
 eBullets=eBullets.filter(q=>q._v18Owner!==b);b._r30.v18.beams=[];b._r30.v18.attack=null;}
function v18PartsBuild(b,hp){b.parts=['core','left','right'].map(id=>({id,hp:id==='core'?hp:Math.ceil(hp*.24),maxhp:id==='core'?hp:Math.ceil(hp*.24),destroyed:false,flash:0,kick:0,dmg:true}));}
function v18Budget(b){const J=j3State(b),base=J3_SOURCE_HP[diffKey]?.[0]||2600,f={0:1.30,8:1.20,1:.90,6:1.10,2:1.0};
 J.max=Array(9).fill(0);for(const i of V18.forms)J.max[i]=Math.ceil(base*f[i]);J.hp=J.max.slice();J.modules=[];J.active=0;J.mimic=null;J.cursor=0;J.visited=[];}
function v18Health(b,hp,max=hp){b.hp=hp;b.maxhp=b._vPhaseHp=max;const p=b.parts.find(p=>p.id==='core');if(p){p.hp=hp;p.maxhp=max;p.destroyed=false;}}
function v18Enter(b,n,form=0){const J=j3State(b),S=b._r30,N=S.v18,old=J.encounter;
 J.encounter=n;N.form=n===2?form:0;J.active=N.form;J.mimic=n===2&&form!==0?form:null;J.attacks=0;
 S.form=n===2?form:n;S.shape=n===0?'possessed':n===1?'ghost':'colossus';S.shield=0;S.shieldMax=1;S.returning=null;S.finale1003b=false;S.modular1003c=false;S.ghostHidden=false;
 const base=J3_SOURCE_HP[diffKey]?.[0]||2600,hp=n===2?J.hp[form]:Math.ceil(base*(n===1?1.65:1.45));
 b.parts=n===2&&J.modules[form]?J.modules[form]:[];if(!b.parts.length)v18PartsBuild(b,hp);v18Health(b,hp,n===2?J.max[form]:hp);
 if(n===2)J.modules[form]=b.parts;
 b.dead=false;b.modular=true;b._lastPart=null;b.x=worldWidth()/2;b.ty=viewTopY()+viewH()*.40;b.y=b.ty;b.w=b.h=v18Size(b)*.77;
 N.home={x:b.x,y:b.y};N.beams=[];N.seq=0;N.age=0;N.formClock=0;N.attack=null;S.cd=1.25;
 b.name=n===0?'THE INFUSED ORBITAL HOST':n===1?'THE GHOST IN THE CODE':form===0?'DRACODIA — MASTER OF DESTRUCTION':F1003B_FORMS[form].name;
 const Q=v17Clock(b);Q.phase=n;Q.previous=old===n?null:old;Q.transition=3;Q.combat=0;
 const D=dr5State(b);D.introWanted=false;if(n===2&&old<2)D.introSeen=false;D.radio=null;
 if(n===2&&form!==0)N.cursor=form;
 if(n===2&&!J.visited.includes(form))J.visited.push(form);
 v18Log(b,'identity',{name:v18Model(b),hp,max:b.maxhp});
}
spawnBoss=function(){const out=V18.base.spawn.apply(this,arguments),b=boss;if(run.stage!==8||!b?._r30)return out;
 const S=b._r30;S.v18={form:0,beams:[],seq:0,age:0,formClock:0,arenaPhase:0,transition:null};v18Budget(b);v18Enter(b,0);v18SetMode(b,'v18arrival');v18Warm();return out;};
j3Encounter=function(b,n){if(!v18Owned(b))return V18.base.encounter.apply(this,arguments);v18Clear(b);v18Enter(b,n);v18SetMode(b,n===0?'v18conversion':'v18reveal');};
j3Save=function(b){if(!v18Owned(b))return V18.base.save.apply(this,arguments);const J=j3State(b);if(J.encounter===2){J.hp[J.active]=Math.max(0,Math.min(J.hp[J.active],b.hp));J.modules[J.active]=b.parts;}};
j3Next=function(J){if(!boss||j3State(boss)!==J||!v18Owned(boss))return V18.base.next.apply(this,arguments);const at=V18.forms.indexOf(J.active);
 for(let n=1;n<=V18.forms.length;n++){const id=V18.forms[(at+n)%V18.forms.length];if(J.hp[id]>0)return id;}return -1;};
function v18Next(b){const J=j3State(b),N=b._r30.v18;if(N.form!==0&&J.hp[0]>0)return 0;
 if(N.form===0){const at=V18.forms.indexOf(N.cursor||0);for(let n=1;n<V18.forms.length;n++){const id=V18.forms[(at+n)%V18.forms.length];if(id!==0&&J.hp[id]>0)return id;}}
 return j3Next(J);}
j3Mimic=function(b,i){if(!v18Owned(b))return V18.base.mimic.apply(this,arguments);if(!V18.forms.includes(i)||j3State(b).hp[i]<=0)i=v18Next(b);
 if(i<0)return j3FinalDeath(b);j3Save(b);v18Clear(b);v18Enter(b,2,i);v18SetMode(b,'v18formIn');};
j3Home=function(b){if(!v18Owned(b))return V18.base.home.apply(this,arguments);return j3Mimic(b,v18Next(b));};
j3Morph=function(b,to){if(!v18Owned(b))return V18.base.morph.apply(this,arguments);j3Save(b);v18Clear(b);
 const J=j3State(b),N=b._r30.v18;N.from=N.form;N.to=to==='home'?v18Next(b):V18.forms.includes(to)&&J.hp[to]>0?to:v18Next(b);
 if(N.to<0)return j3FinalDeath(b);v18SetMode(b,'v18formOut');r30Sound('teleportIn');};
function v18Rig(b){const frame=v18Frame(b),k=v18Size(b)/320;
 return b.parts.filter(p=>!p.destroyed||p.id==='core').map(p=>{const a=frame[p.id],q=a.bounds;return {p,key:a.key,x:b.x+((q[0]+q[2])/2-160)*k,y:b.y+((q[1]+q[3])/2-160)*k,w:(q[2]-q[0])*k,h:(q[3]-q[1])*k,rot:0,alpha:1,a,k,bodyX:b.x,bodyY:b.y,spec:{role:p.id==='core'?'core':'weapon',tags:['v18']}};});}
r30Parts=function(b){return v18Owned(b)?v18Rig(b):V18.base.parts.apply(this,arguments);};
r30Pose=function(b){return v18Owned(b)?{x:b.x,y:b.y,scale:1,angle:0,alpha:1,shape:v18Model(b)}:V18.base.pose.apply(this,arguments);};
function v18Mask(a){if(V18.masks.has(a.key))return V18.masks.get(a.key);if(!XART.rdy(a.key))return null;
 const im=XART.get(a.key),c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0);
 const rgba=g.getImageData(0,0,a.w,a.h).data,mask=new Uint8Array(a.w*a.h);for(let i=0;i<mask.length;i++)mask[i]=rgba[i*4+3];
 if(V18.masks.size>96)V18.masks.delete(V18.masks.keys().next().value);V18.masks.set(a.key,mask);return mask;}
r30At=function(b,x,y){if(!v18Owned(b))return V18.base.at.apply(this,arguments);if(!r30Live(b)||b._noHit)return null;
 for(const v of v18Rig(b).reverse()){const px=Math.floor((x-v.bodyX)/v.k+160),py=Math.floor((y-v.bodyY)/v.k+160),m=v18Mask(v.a);
  if(m&&px>=0&&py>=0&&px<v.a.w&&py<v.a.h&&m[py*v.a.w+px]>48)return v.p;}return null;};
retinaBossTargets=function(b){if(!v18Owned(b))return V18.base.targets.apply(this,arguments);if(!r30Live(b)||b._noHit)return[];
 const stamp=j3State(b).encounter+':'+b._r30.v18.form;
 return v18Rig(b).map(v=>retinaDynamicPiece(b,'v18-'+stamp+'-'+v.p.id,'infused '+v.p.id,()=>{
  const q=v18Rig(b).find(q=>q.p===v.p),current=j3State(b).encounter+':'+b._r30.v18.form;
  return{x:q?.x??v.x,y:q?.y??v.y,hp:v.p.hp,dead:current!==stamp||!r30Live(b)||b._noHit||!q||v.p.destroyed};
 },d=>{if(!r30Live(b)||j3State(b).encounter+':'+b._r30.v18.form!==stamp||v.p.destroyed)return;b._lastPart=v.p;hitBoss(d);},v.w*.8,v.h*.8));};
function v18Rupture(b,p){const v=v18Rig(b).find(v=>v.p===p);if(!v)return;const q=v.a.bounds,c=document.createElement('canvas');c.width=q[2]-q[0];c.height=q[3]-q[1];
 c.getContext('2d').drawImage(XART.get(v.key),q[0],q[1],c.width,c.height,0,0,c.width,c.height);d27ModuleRupture(b,p,{...v,debrisImage:c},'purple');v18Log(b,'module-broken',{module:p.id});}
modularHit=function(dmg){const b=boss;if(!v18Owned(b))return V18.base.hit.apply(this,arguments);if(!r30Live(b)||b._noHit||!Number.isFinite(dmg)||dmg<=0)return;
 const p=b.parts.includes(b._lastPart)&&!b._lastPart.destroyed?b._lastPart:b.parts[0],dealt=Math.min(dmg,b.hp);b.hp-=dealt;markHit(p,.12);markHit(b,.12);stageStats.dmgDealt+=dealt;
 if(p.id!=='core'){p.hp=Math.max(0,p.hp-dmg);if(p.hp<=0){v18Rupture(b,p);p.destroyed=true;b._r30.v18.beams=b._r30.v18.beams.filter(L=>L.module!==p.id);r30Sound('combatModule0927');}}
 b.parts[0].hp=b.hp;j3Save(b);if(b.hp<=0)r30Break(b);};
r30Break=function(b){if(!v18Owned(b))return V18.base.break.apply(this,arguments);if(!r30Live(b))return;
 const J=j3State(b),N=b._r30.v18;for(const p of b.parts)if(!p.destroyed)v18Rupture(b,p);j3Save(b);v18Clear(b);b.hp=0;
 if(J.encounter===2){J.hp[J.active]=0;v18Log(b,'form-defeated',{remaining:V18.forms.filter(i=>J.hp[i]>0)});if(V18.forms.every(i=>J.hp[i]<=0))return j3FinalDeath(b);return j3Morph(b,'home');}
 N.transition={to:J.encounter+1,switched:false};v18SetMode(b,'v18phaseFade');r30Sound('expBig');v18Log(b,'phase-defeated');};
function v18Ports(b){const rig=v18Rig(b),out=rig.filter(v=>v.p.id!=='core').map(v=>({x:v.x,y:v.y+v.h*.28,module:v.p.id}));
 return out.length?out:[{x:b.x,y:b.y+35,module:'core'}];}
function v18Line(p,a,w=18){return {...s81003Lane(p.x,p.y,p.x+Math.cos(a)*1000,p.y+Math.sin(a)*1000,w,viewH()*1.6),module:p.module};}
function v18Diff(){return r30Difficulty();}
function v18StartAttack(b){const N=b._r30.v18,name=v18Model(b),books={infused:['claws','guns','crossbeam'],ghost:['ghostRail','pincer','voidbombs'],colossus:['tentacles','voidfan','codewall'],
 hammer:['hammerSwing','chromiumBeams','jump'],helicopter:['rotorgun','missiles','bombs'],harrier:['fanbeam','missiles','wind'],volcano:['magma','flamethrower','firewall']};
 const type=books[name][N.seq++%books[name].length],d=v18Diff(),tell=diffKey==='easy'?1.35:d===0?1.10:d===1?.96:.82;
 const P=N.attack={type,t:0,tell,active:['claws','pincer','tentacles','hammerSwing','jump'].includes(type)?1.40:2.2,next:0,n:0,
  tx:clamp(player.x,camLeftX()+45,camRightX()-45),ty:clamp(player.y,viewTopY()+110,VH-50),origin:{x:b.x,y:b.y},ports:v18Ports(b),lanes:[],targets:[]};
 if(['crossbeam','ghostRail','fanbeam','flamethrower'].includes(type)){
  P.lanes=P.ports.map(p=>v18Line(p,Math.atan2(P.ty-p.y,P.tx-p.x)+(type==='crossbeam'?(p.module==='left'?.22:-.22):0),type==='flamethrower'?28:16));
 }
 if(type==='chromiumBeams'){
  const top=viewTopY()+viewH()*.5;P.active=2.6;P.lanes=[.18,.42,.65,.87].map(u=>({x:camLeftX()+viewW()*u,y:VH+15,ex:camLeftX()+viewW()*u,ey:top,width:24,module:'core'}));
  if(P.ty<top){P.type='jump';P.active=1.4;P.lanes=[];}
 }
 if(['bombs','voidbombs','jump'].includes(P.type))P.targets=[-.17,0,.17].map((o,i)=>({x:clamp(P.tx+o*viewW(),camLeftX()+45,camRightX()-45),y:clamp(P.ty+(i%2?0:-35),viewTopY()+150,VH-45)}));
 b._r30.attack=P;combatWarningTick(b,'v18-'+N.seq,0,P.tell,true);r30Sound('bossWeaponCharge');v18Log(b,'attack-tell',{type:P.type,tell:P.tell,targets:P.targets,lanes:P.lanes});
}
r30Attack=function(b){return v18Owned(b)?v18StartAttack(b):V18.base.attack.apply(this,arguments);};
function v18Shot(b,p,a,speed,kind,large=false){const q=f1003bShot(b,p.x,p.y,a,speed,kind,large);if(q&&!q.dead){q._v18Owner=b;b._r30.v18.shots=(b._r30.v18.shots||0)+1;}return q;}
function v18AttackTick(b,dt){const S=b._r30,N=S.v18,P=N.attack;if(!P)return;P.t+=dt;const u=P.t-P.tell,d=v18Diff();
 combatWarningTick(b,'v18-'+N.seq,Math.min(P.t,P.tell),P.tell);if(u<0)return;
 if(!P.started){P.started=true;v18Log(b,'attack-release',{type:P.type,reaction:P.tell});r30Sound(P.lanes.length?'combatBeam0927':'enemyBossCannon');
  for(const L of P.lanes)if(L.module==='core'||b.parts.some(p=>p.id===L.module&&!p.destroyed))N.beams.push({...L,t:0,life:P.active,owner:b,type:P.type});
  for(const T of P.targets)groundTargetingSpawn({kind:P.type==='voidbombs'?'missile':'lightning',x:T.x,y:T.y,warn:.65,active:.5,radius:P.type==='jump'?47:35,size:80,track:false,lane:false,owner:b,_v18:true});
 }
 if(['claws','pincer','tentacles','hammerSwing','jump'].includes(P.type)){
  const k=Math.sin(clamp(u/P.active,0,1)*Math.PI),tx=P.type==='hammerSwing'?P.tx+(P.tx<P.origin.x?42:-42):P.tx;
  b.x=lerp(P.origin.x,tx,k);b.y=lerp(P.origin.y,P.ty-(P.type==='jump'?20:75),k)-(P.type==='jump'?Math.sin(clamp(u/P.active,0,1)*Math.PI)*75:0);
  if(u>.35&&u<P.active-.25)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-b.x,player.y-(b.y+70))<36)playerHit('infused committed strike');});
 }
 if(u>=P.next){P.n++;P.next=u+(['rotorgun','guns'].includes(P.type)?(d===0?.25:d===1?.19:.14):P.type==='missiles'?.60:.72);
  const ports=v18Ports(b),aim=p=>Math.atan2(P.ty-p.y,P.tx-p.x);
  if(['rotorgun','guns','wind'].includes(P.type))for(const p of ports)for(const off of P.type==='wind'?[-.22,0,.22]:[-.07,.07])v18Shot(b,p,aim(p)+off,3.6+d*.25,'code');
  if(P.type==='missiles')for(const p of ports)v18Shot(b,p,aim(p)+(P.n%2?.18:-.18),2.6+d*.16,'missile');
  if(['magma','voidfan','codewall','firewall'].includes(P.type)){
   if(['codewall','firewall'].includes(P.type)){
    // Committed two-column corridor, unchanged after warning. No homing wall.
    const gap=Math.floor(clamp((P.tx-camLeftX())/viewW()*8,1,6));for(let i=0;i<8;i++)if(i!==gap&&i!==gap-1)
     v18Shot(b,{x:camLeftX()+viewW()*(i+.5)/8,y:b.y+65},Math.PI/2,2.0+d*.15,P.type==='firewall'?'fire':'code',true);
   }else for(const p of ports)for(let i=-2-d;i<=2+d;i++)v18Shot(b,p,aim(p)+i*.17,2.3+Math.abs(i)*.13,P.type==='magma'?'fire':'code',P.type==='magma');
  }
  if(['bombs','voidbombs'].includes(P.type)&&P.n>1)for(const p of ports)v18Shot(b,p,aim(p),2.2,'missile');
 }
 if(u>=P.active){b.x=P.origin.x;b.y=P.origin.y;N.attack=null;S.attack=null;S.cd=d===0?1.15:d===1?.85:.60;j3State(b).attacks++;N.formClock++;}
}
r30AttackTick=function(b,dt){return v18Owned(b)?v18AttackTick(b,dt):V18.base.attackTick.apply(this,arguments);};
function v18ReleaseProtection(){for(const seat of seatList())withSeat(seat,()=>{player.invuln=Math.min(player.invuln||0,.5);});}
function v18Fight(b){v18SetMode(b,'fight');v18ReleaseProtection();b._r30.cd=1.2;bossPhaseMusic(8,j3State(b).encounter+1);r30Sound('bossPhase');}
r30Tick=function(b,dt){if(!v18Owned(b))return V18.base.tick.apply(this,arguments);const S=b._r30,N=S.v18,J=j3State(b);dt=clamp(dt||0,0,.05);
 if(['dr5Monologue','dr5Death','dr5Portal','reunion','done','escape','finalFall'].includes(S.mode)){
  const mode=S.mode,out=V18.base.tick.call(this,b,dt);if(mode==='dr5Monologue'&&S.mode==='fight'){b._noHit=false;v18ReleaseProtection();}return out;
 }
 j3Timers(b,dt);N.age+=dt;const Q=v17Clock(b);Q.t+=dt;Q.transition+=dt;J.aa5Clock=Q.t;dr5TalkTick(b,dt);
 for(const L of N.beams){L.t+=dt;if(L.t<L.life)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,L)<L.width*.5+4)playerHit('infused '+L.type);});}N.beams=N.beams.filter(q=>q.t<q.life);
 if(S.mode==='fight'){
  b.enter=false;b._noHit=false;Q.combat+=dt;if(N.attack)v18AttackTick(b,dt);else{
   b.x=N.home.x+Math.sin(S.clock*.65)*Math.min(24,viewW()*.04);b.y=N.home.y+Math.sin(S.clock*.9)*5;S.cd-=dt;
   if(S.cd<=0){if(J.encounter===2&&J.attacks>=3&&V18.forms.filter(i=>J.hp[i]>0).length>1)return j3Morph(b,N.form===0?v18Next(b):'home');v18StartAttack(b);}
  }return;
 }
 b.enter=true;b._noHit=true;for(const seat of seatList())withSeat(seat,()=>{player.invuln=Math.max(player.invuln||0,.25);});
 if(S.mode==='v18arrival'){b.y=lerp(viewTopY()-180,b.ty,clamp(S.t/1.7,0,1));if(S.t>=1.7){v18SetMode(b,'v18conversion');r30Sound('combatAlien0927');dr5Say(b,run.pilot.toUpperCase(),'The drone... something is taking it over!');}return;}
 if(S.mode==='v18conversion'){if(S.t>2&&!N.infusionCue){N.infusionCue=true;r30Sound('dracodiaShriek');shake=Math.max(shake,8);}if(S.t>=4.3){dr5State(b).radio=null;v18Fight(b);}return;}
 if(S.mode==='v18phaseFade'){
  const T=N.transition;if(!T.switched&&S.t>=1.05){T.switched=true;const t=S.t;v18Enter(b,T.to);N.arenaPhase=T.to;S.t=t;S.mode='v18phaseFade';b.enter=true;b._noHit=true;N.transition=T;
   v18Log(b,'arena-swap',{blackout:1,arena:T.to});dr5Say(b,run.pilot.toUpperCase(),T.to===1?'It is still alive. The code is reforming!':'That is its real body. Break those weapon systems!');}
  if(S.t>=4.9){N.transition=null;const D=dr5State(b);D.radio=null;
   if(J.encounter===2&&!D.introSeen){dr5Ships(b);S.mode='dr5Monologue';S.t=0;D.line=0;b.enter=true;b._noHit=true;v18Log(b,'monologue');}
   else v18Fight(b);
  }return;
 }
 if(S.mode==='v18formOut'&&S.t>=1.45){const to=N.to;v18Enter(b,2,to);v18SetMode(b,'v18formIn');return;}
 if(S.mode==='v18formIn'&&S.t>=1.6){v18Fight(b);return;}
 if(S.mode==='v18reveal'&&S.t>=2.8)v18Fight(b);
};
function v18Cell(a,x,y,size,alpha=1,white=false){if(!a||!XART.rdy(a.key)||alpha<=0)return false;const im=white?xartTint(a.key,'#ffffff',1):XART.get(a.key);if(!im)return false;
 const k=size/a.w;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();V18.draws[a.key]=(V18.draws[a.key]||0)+1;return true;}
function v18Body(b){const frame=v18Frame(b),size=v18Size(b);for(const p of b.parts){if(p.destroyed&&p.id!=='core')continue;v18Cell(frame[p.id],b.x,b.y,size);
 const flash=Math.max(p.flash||0,b.flash||0);if(flash>0)v18Cell(frame[p.id],b.x,b.y,size,Math.min(.9,flash*8),true);}}
j3Body=function(b,alpha=1){if(!v18Owned(b))return V18.base.body.apply(this,arguments);ctx.save();ctx.globalAlpha*=alpha;v18Body(b);ctx.restore();};
function v18Clip(name,t,duration,x,y,size,reverse=false){const c=V18_ART.clips[name];if(!c)return false;let u=clamp(t/duration,0,1);if(reverse)u=1-u;
 const f=Math.min(c.frames.length-1,Math.floor(u*c.frames.length));return v18Cell(c.frames[f],x,y,size);}
function v18Fade(b){const S=b._r30;if(S.mode!=='v18phaseFade')return 0;return S.t<1.05?clamp(S.t/1.05,0,1):S.t<1.55?1:1-clamp((S.t-1.55)/1.05,0,1);}
function v18Warnings(b){const P=b._r30.v18.attack;if(!P||P.t>=P.tell)return;const u=P.t/P.tell;
 if(P.lanes.length)for(const L of P.lanes)if(L.module==='core'||b.parts.some(p=>p.id===L.module&&!p.destroyed))s81003Fov(L,u,true);
 else if(P.targets.length)for(const T of P.targets)groundTargetReticleDraw(T.x,T.y,P.type==='jump'?94:70,u,.88);
 else for(const p of P.ports)combatWarningDraw(b,{x:p.x,y:p.y,ex:P.tx,ey:P.ty,width:['magma','voidfan'].includes(P.type)?90:34,progress:u,fieldOnly:false});
}
r30DrawBoss=function(b){if(!v18Owned(b))return V18.base.draw.apply(this,arguments);const S=b._r30,N=S.v18,J=j3State(b),size=v18Size(b);
 if(['dr5Portal','reunion','done','escape'].includes(S.mode))return V18.base.draw.apply(this,arguments);
 if(S.mode==='dr5Death'){if(S.t<10.5){const frame=V18_ART.models.colossus.frames[Math.floor(S.clock*12)%16];for(const a of Object.values(frame))v18Cell(a,b.x,b.y,422);}
  dr5EffectsDraw(b);return;}
 if(S.mode==='v18arrival')v18Cell(V18_ART.drone,b.x,b.y,size*.8);
 else if(S.mode==='v18conversion')v18Clip('conversion',S.t,4.0,b.x,b.y,size);
 else if(S.mode==='v18phaseFade'){
  if(!N.transition?.switched)v18Body(b);else v18Clip(J.encounter===1?'ghost_emerge':'colossus_emerge',Math.max(0,S.t-1.55),3.1,b.x,b.y,size);
 }else if(S.mode==='v18formOut'){
  const name=N.from===0?N.to:N.from;
  if(name&&V18.names[name])v18Clip('morph_'+V18.names[name],(N.from===0||N.to===0)?S.t*.5:S.t,1.45,b.x,b.y,size,N.from!==0);else v18Body(b);
 }else if(S.mode==='v18formIn'){
  const name=N.form||N.from,joined=N.from===0||N.form===0;
  if(name&&V18.names[name])v18Clip('morph_'+V18.names[name],joined?.8+S.t*.5:S.t,1.6,b.x,b.y,size,N.form===0);else v18Body(b);
 }else v18Body(b);
 for(const L of N.beams){const a=Math.atan2(L.ey-L.y,L.ex-L.x),len=Math.hypot(L.ex-L.x,L.ey-L.y),f=Math.floor(L.t*16)%8,h=len/.91;
  if(L.type==='flamethrower')p2RenderFireColumn(ctx,P2_ART,k=>XART.rdy(k)?XART.get(k):null,L.x,L.y,a,len,L.width,L.t,Math.min(1,(L.life-L.t)*5));
  else s81003Cell('beams',f,L.x+Math.cos(a)*(h*.5-h*.07),L.y+Math.sin(a)*(h*.5-h*.07),L.width*3.4,h,Math.min(1,(L.life-L.t)*5),a-Math.PI/2);}
 v18Warnings(b);V18.last={phase:J.encounter,form:N.form,mode:S.mode,frame:Math.floor(S.clock*12)%16,fade:v18Fade(b),beams:N.beams.length};
};
fmcGauge=function(b){if(!v18Owned(b))return V18.base.gauge.apply(this,arguments);const J=j3State(b),id=b._r30.v18.form;
 return{charge:-1,color:J.encounter===0?'#e75b72':J.encounter===1?'#c783ff':F1003B_FORMS[id].color,under:null,frac:clamp(b.hp/Math.max(1,b.maxhp),0,1)};};
function v18Arena(b){if(!v18Owned(b)||['dr5Portal','reunion','done','escape'].includes(b._r30.mode))return V18.base.arena(b);
 const N=b._r30.v18,Q=v17Clock(b),phase=N.arenaPhase,a=PXV17_ART.arenas[phase],t=b._r30.clock,left=camLeftX(),top=viewTopY(),w=viewW(),h=viewH(),world=worldWidth();
 const scale=Math.max((world+100)/a.w,(h+100)/a.h),combat=Q.combat||0;
 ctx.save();ctx.fillStyle='#000';ctx.fillRect(left-32,top-32,w+64,h+64);v17Plate(a,world/2+Math.sin(t*.1)*5,top+h/2+Math.cos(t*.08)*6,scale,[.56,.38,.46][phase]);
 for(let i=0;i<9;i++){const depth=[.08,.18,.34][i%3],size=[104,142,180][i%3],span=h+size*2;
  const x=world*((i*.381966+.12)%1)+(left-(world-w)/2)*depth,y=top+((i*.173*h+t*(i%2?-1:1)*(3+depth*18)+size)%span+span)%span-size;
  v17Code(t*14+i*4,x,y,size,(.045+depth*.2)*(.16+.84*clamp(combat/4,0,1)));}
 ctx.restore();j3State(b).aa5ArenaDrawn=true;VOID17.last={phase,fade:1,blend:1,awake:clamp(combat/4,0,1),t,combat};return true;}
v17ArenaDraw=v18Arena;aa5ArenaDraw=v18Arena;
drawWorld=function(dt){const out=V18.base.world.apply(this,arguments),b=boss;if(v18Owned(b)){
 const fade=v18Fade(b);if(fade>0){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=fade;ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);ctx.restore();}
 }return out;};
globalThis.BOF_STAGE8_PIXEL=V18;
