"use strict";
/* Dracodia: demonic machine choreography. The shared rig, damage and seat
   owners remain authoritative. The shadow ball homes until its final escape window. */
const DR21={base:{start:v18StartAttack,attack:v18AttackTick,tick:r30Tick,rig:v18Rig,draw:r30DrawBoss,
 warnings:v18Warnings,clear:v18Clear,enter:v18Enter,keys:v18Keys,warm:v18Warm,load:stageLoadBegin,world:drawWorld,arena:v17ArenaDraw,
 hit:modularHit,gauge:fmcGauge,shieldFrac:bossShieldFrac,contact:target17BossContact,enemy:d20Enemy,download:d20Download,model:d20Model,paint:v19Paint,
 playerHit,deathTick:updateDeathSpin,deathDraw:drawDeathSpin,begin:beginStage,fx:d20Fx,body:d20MainBody,shot:v18Shot,projectile:drawCombatFinalProjectile,setMode:v18SetMode},
 events:[],draws:{},serial:0,models:new Map(),eyes:new Map(),books:{
 infused:['machineLasers','armOrbs','machineGrab'],
 ghost:['ghostTeleport','soulBomb','downloadRitual','codeAegis','voidWells'],
 colossus:['shadowAscension','downloadRitual','ghostTeleport','codeAegis','spiralLightning','armLasers','scytheReap','codeBombs','voidRoar','coreMissiles']}};
for(const bank of Object.values(DR21_ART.banks))for(const a of bank)XART._src[a.key]=a.path;
for(const a of Object.values(DR22_ART.forms))XART._src[a.key]=a.path;
function dr21Keys(){return [...Object.values(DR21_ART.banks).flat().map(a=>a.key),...Object.values(DR22_ART.forms).map(a=>a.key)];}
const DR21_CUES=['bossWeaponCharge','spaceShadowRelease','fireIceOrbImpact','teleportIn','shadowRelease','shieldHitHeavy','shieldBreakCombat','slice','enemyIceBolt','flameThrowerStart'];
function dr21Warm(){let ready=true;for(const k of dr21Keys())if(!XART.rdy(k))ready=false;for(const cue of DR21_CUES)Snd.prepare(cue);return ready;}
v18Keys=function(){return [...DR21.base.keys(),...dr21Keys()];};
v18Warm=function(){const prior=DR21.base.warm();return dr21Warm()&&prior;};
stageLoadBegin=function(n,keys){return DR21.base.load.call(this,n,[...(keys||[]),...(n===8?dr21Keys():['ice','erase'].flatMap(k=>DR21_ART.banks[k].map(a=>a.key)))]);};
function dr21Rank(){return diffKey==='furious'?3:diffKey==='hard'?2:diffKey==='normal'?1:0;}
function dr21Owns(b){return v18Owned(b)&&!v19Native(b);}
function dr21Log(event,data={}){DR21.events.push({event,...data});if(DR21.events.length>250)DR21.events.shift();}
function dr21Cue(k){Snd.play(k);}
function dr21Art(bank,t,x,y,size,alpha=1,once=false,angle=0){const rows=DR21_ART.banks[bank];if(!rows?.length||once&&t>=rows.length/18)return;
 const a=rows[once?Math.min(rows.length-1,Math.floor(Math.max(0,t)*18)):Math.floor(Math.max(0,t)*18)%rows.length];if(!XART.rdy(a.key))return;
 const k=size/a.w;ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=clamp(alpha,0,1);ctx.translate(x,y);ctx.rotate(angle);ctx.drawImage(XART.get(a.key),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();DR21.draws[bank]=(DR21.draws[bank]||0)+1;
}
function dr21Target(){const targets=[];for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out)targets.push({x:player.x,y:player.y,seat});});return targets[DR21.serial++%Math.max(1,targets.length)]||{x:player.x,y:player.y,seat:1};}
function dr21Begin(b,type){const N=b._r30.v18,d=dr21Rank(),target=dr21Target();N.swipe=null;N.acting=null;N.archiveDepth=1;
 const P=N.attack={_dr21:true,type,t:0,tell:[1.9,1.7,1.5,1.35][d],active:3.0,target:{...target},origin:{x:b.x,y:b.y},hit:new Set(),next:0,n:0,ports:[],targets:[],lanes:[],depth:1,opacity:1};b._r30.attack=P;
 if(type==='shadowAscension'){P.travel=[4.4,4.0,3.65,3.4][d];P.dodgeWindow=[2.0,1.75,1.5,1.25][d];P.lockAt=P.travel-P.dodgeWindow;P.locked=false;P.active=P.travel+.9;P.cast={x:b.x,y:Math.max(viewTopY()+70,b.y-v18Size(b)*.38)};P.x=P.cast.x;P.y=P.cast.y;P.radius=64;P.screenSize=Math.max(viewW(),viewH())*4.8;P.tell=[2.2,2.0,1.8,1.65][d];dr5Say(b,'DRACODIA','Fear THIS!',5);}
 if(type==='ghostTeleport'){P.tell=.75;P.hops=[3,3,4,4][d];P.hop=.62;P.slamTell=[1.4,1.2,1.05,.95][d];P.active=P.hops*P.hop+P.slamTell+1.20;P.positions=Array.from({length:P.hops},(_,i)=>({x:camLeftX()+viewW()*[.28,.72,.35,.65][i],y:viewTopY()+viewH()*(i%2?.43:.46)}));}
 if(type==='downloadRitual'){P.tell=[2.25,2.05,1.85,1.7][d];P.active=3.5;P.shieldMax=P.shield=Math.ceil(b.maxhp*.035);dr5Say(b,'DRACODIA','Your resistance has been downloaded.',4);}
 if(type==='codeAegis'){P.tell=1.0;P.active=[2.1,2.4,2.7,3][d];P.shieldMax=P.shield=Math.ceil(b.maxhp*.045);dr5Say(b,'DRACODIA','Your weapons are obsolete.',3);}
 if(type==='machineLasers'){P.active=2.8;P.ports=v18Ports(b);P.lanes=P.ports.map(p=>({...p,ex:target.x,ey:target.y,width:18,module:p.module}));}
 if(type==='armOrbs'){P.active=2.2;P.ports=v18Ports(b);}
 if(type==='machineGrab'){P.active=1.5;P.tell=[1.85,1.65,1.45,1.3][d];}
 if(type!=='shadowAscension')combatWarningTick(b,'dr21-'+N.seq,0,P.tell,true);dr21Cue(type==='ghostTeleport'?'teleportIn':'bossWeaponCharge');dr21Log('begin',{type,diff:diffKey,tell:P.tell,target:P.target});return P;
}
// The main body must finish its complete new repertoire before a copy morph.
D20.book=DR21.books.colossus.slice();
v18StartAttack=function(b){if(!dr21Owns(b))return DR21.base.start.apply(this,arguments);const N=b._r30.v18,name=v18Model(b),book=DR21.books[name];if(!book)return DR21.base.start.apply(this,arguments);
 const seq=N.seq,type=book[seq%book.length];N.seq=seq+1;
 if(['shadowAscension','ghostTeleport','downloadRitual','codeAegis','machineLasers','armOrbs','machineGrab'].includes(type))return dr21Begin(b,type);
 if(name==='ghost'){const lookup=type==='soulBomb'?1:0;N.seq=lookup;const out=DR21.base.start(b);N.seq=seq+1;return out;}
 N.seq=seq;return DR21.base.start(b);
};
function dr21Finish(b){const N=b._r30.v18,P=N.attack;b.x=P.origin.x;b.y=P.origin.y;b._noHit=false;N.archiveDepth=1;N.attack=null;N.acting=null;b._r30.attack=null;b._r30.cd=[1.35,1.1,.9,.75][dr21Rank()];j3State(b).attacks++;dr5State(b).radio=null;dr21Log('finish',{type:P.type});}
function dr21Contact(P,x,y,r,source){for(const seat of seatList())withSeat(seat,()=>{if(P.hit.has(seat)||player.dead||player.out||player.invuln>0||Math.hypot(player.x-x,player.y-y)>r)return;P.hit.add(seat);playerHit(source);dr21Log('contact',{source,seat,dead:player.dead});});}
function dr21Summon(b){const N=b._r30.v18,d=dr21Rank(),live=enemies.filter(e=>e._d20?.owner===b&&!e.dead&&e._dyingT==null&&e._d20.phase!=='erase'),cap=[1,2,2,3][d];
 const wave=N.demonWave=(N.demonWave||0)+1,kinds=wave%2?['demonJet','demonRobot','spear']:['halberd','demonJet','demonRobot'];
 for(let i=0;live.length<cap&&i<cap;i++){if(i===0&&kinds[0]==='halberd'&&live.some(e=>e._d20.mini))continue;const mini=kinds[i]==='halberd',x=camLeftX()+viewW()*(mini?.5:[.23,.77,.5][i]),y=viewTopY()+viewH()*(mini?.52:i===2?.55:.32),e=d20Enemy(kinds[i],x,y,b,mini);if(e)live.push(e);}
 dr21Cue('teleportIn');dr21Log('summon',{count:live.length,cap});
}
v18AttackTick=function(b,dt){const N=b?._r30?.v18,P=N?.attack;if(!P?._dr21)return DR21.base.attack.apply(this,arguments);
 if(b.dead||b._r30.mode!=='fight'){v18Clear(b);return;}P.t+=clamp(dt||0,0,.05);const t=P.t,u=t-P.tell,d=dr21Rank();if(P.type!=='shadowAscension')combatWarningTick(b,'dr21-'+N.seq,Math.min(t,P.tell),P.tell);
 if(P.type==='shadowAscension'){
  if(!P.locked){let ship=seatShip(P.target.seat);if(!ship||ship.dead||ship.out){const next=dr21Target();P.target.seat=next.seat;ship=seatShip(next.seat);}if(ship&&!ship.dead&&!ship.out){P.target.x=ship.x;P.target.y=ship.y;}
   if(u>=P.lockAt){P.locked=true;const launch=P.launch||P.cast,q=P.lockAt/P.travel;P.commit={x:lerp(launch.x,P.target.x,q),y:lerp(launch.y,P.target.y,q)};P.edgeInset=Math.min(P.radius+56,viewW()*.4);P.target.x=clamp(P.target.x,camLeftX()+P.edgeInset,camRightX()-P.edgeInset);dr21Log('shadow-commit',{target:{...P.target},remaining:P.travel-u,edgeInset:P.edgeInset});}}
  P.spin=P.t*TAU*.85;
  P.depth=1-.52*v19Ease((t-.35)/1.1);b.y=lerp(P.origin.y,viewTopY()+viewH()*.40,v19Ease(t/1.4));b._noHit=P.depth<.78;
  if(u<0){P.cast={x:b.x,y:Math.max(viewTopY()+58,b.y-v18Size(b)*.36*P.depth)};P.x=P.cast.x;P.y=P.cast.y;}
  else{if(!P.released){P.released=true;P.launch={...P.cast};dr21Cue('spaceShadowRelease');dr21Log('shadow-release',{target:P.target});}
   const q=clamp(u/P.travel,0,1),approach=P.locked?clamp((u-P.lockAt)/P.dodgeWindow,0,1):q,start=P.locked?P.commit:P.launch;P.x=lerp(start.x,P.target.x,approach);P.y=lerp(start.y,P.target.y,approach);P.projectedSize=lerp(70,P.screenSize,Math.pow(q,3.8));
   if(q>.94&&u<P.travel+.16)dr21Contact(P,P.x,P.y,P.radius,'Dracodia shadow eradication');
   if(q>=1&&!P.impacted){P.impacted=true;dr21Cue('fireIceOrbImpact');shake=Math.max(shake,5);}
   P.depth=lerp(.48,1,v19Ease((u-P.travel-.1)/.7));}
 }else if(P.type==='ghostTeleport'){
  if(u>=0){const hops=P.hops*P.hop;if(u<hops){const i=Math.min(P.hops-1,Math.floor(u/P.hop)),local=u-i*P.hop,pos=P.positions[i];
    if(P.lastHop!==i){P.lastHop=i;P.depart={x:b.x,y:b.y};b.x=pos.x;b.y=pos.y;dr21Cue('teleportIn');dr21Log('teleport',{i,x:b.x,y:b.y});}
    P.opacity=Math.sin(clamp(local/P.hop,0,1)*Math.PI)*.60;b._noHit=P.opacity<.3;P.ghostAt=local;
   }else{const s=u-hops;if(!P.strike){P.strike=true;P.strikeOrigin={x:b.x,y:b.y};P.target=dr21Target();dr21Cue('bossWeaponCharge');dr21Log('slam-tell',{tell:P.slamTell,target:P.target});}
    P.opacity=1;b._noHit=false;const q=s-P.slamTell;
    if(q<0){b.y=P.strikeOrigin.y-40*v19Ease(s/P.slamTell);combatWarningTick(b,'dr21-slam-'+N.seq,s,P.slamTell);}
    else{if(!P.slamCue){P.slamCue=true;dr21Cue('slice');}const jump=clamp(q/.35,0,1);b.x=lerp(P.strikeOrigin.x,P.target.x,jump);b.y=lerp(P.strikeOrigin.y-40,P.target.y-60,jump);
     if(q>=.28&&q<.52)dr21Contact(P,P.target.x,P.target.y,40,'Dracodia ghost strike');P.slamAge=q;}
   }}
 }else if(P.type==='downloadRitual'){
  P.depth=1-.38*v19Ease(t/.9);if(u>=0&&!P.summoned){P.summoned=true;dr21Summon(b);}if(u>2.5)P.depth=lerp(.62,1,v19Ease((u-2.5)/1));
 }else if(P.type==='codeAegis'){
  if(u>=0&&!P.started){P.started=true;dr21Cue('shadowRelease');}
 }else if(P.type==='machineLasers'){
  if(u>=0)for(let i=0;i<P.lanes.length;i++){const L=P.lanes[i],age=u-i*.95;if(age<0||age>.48||!b.parts.some(p=>p.id===L.module&&!p.destroyed))continue;
   if(!L.started){L.started=true;dr21Cue('shadowRelease');}for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,L)<L.width/2+4)playerHit('Dracodia machine laser');});}
 }else if(P.type==='armOrbs'){
  if(u>=0&&u>=P.next&&P.n<3){P.next=u+.70;P.n++;dr21Cue('spaceShadowRelease');for(const p of v18Ports(b)){const aim=Math.atan2(P.target.y-p.y,P.target.x-p.x);for(const off of d>1?[-.15,0,.15]:[0])v18Shot(b,p,aim+off,2.6+d*.18,'code',true);}}
 }else if(P.type==='machineGrab'){
  if(u>=0){const q=clamp(u/.42,0,1),back=v19Ease((u-.65)/.8);P.depth=1+Math.sin(q*Math.PI)*.25;
   b.x=lerp(lerp(P.origin.x,P.target.x,q),P.origin.x,back);b.y=lerp(lerp(P.origin.y,P.target.y-50,q)-Math.sin(q*Math.PI)*55,P.origin.y,back);
   if(!P.started){P.started=true;dr21Cue('slice');}if(u>.32&&u<.62)dr21Contact(P,P.target.x,P.target.y,31,'Dracodia machine grab');}
 }
 if(u>=P.active)dr21Finish(b);
};
// Skip the older hover wrapper for owned choreography; it must not overwrite
// a teleport, depth retreat or committed jump position after the attack tick.
r30Tick=function(b,dt){if(b?._r30?.v18?.attack?._dr21)return D20.base.tick.call(this,b,dt);return DR21.base.tick.apply(this,arguments);};
v18Rig=function(b){let rig=DR21.base.rig.apply(this,arguments);const P=b?._r30?.v18?.attack;if(!P?._dr21)return rig;
 const depth=P.depth||1,cast=['shadowAscension','downloadRitual'].includes(P.type),hold=cast?v19Ease(P.t/.65)*(P.type==='shadowAscension'&&P.released?1-v19Ease((P.t-P.tell)/.32):1):0;
 return rig.map(source=>{let v={...source,k:source.k*depth,w:source.w*depth,h:source.h*depth,ax:b.x+(source.ax-b.x)*depth,ay:b.y+(source.ay-b.y)*depth};
  let arm=hold*2.55;if(P.type==='armOrbs')arm=v19Ease(P.t/P.tell)*.85*(1-v19Ease((P.t-P.tell)/.28));
  if(P.type==='ghostTeleport'&&P.strike)arm=2.35*(1-v19Ease((P.slamAge||0)/.24));
  if(P.type==='machineGrab')arm=.55*v19Ease(P.t/P.tell);
  v.rot=source.rot+(v.p.id==='left'?arm:v.p.id==='right'?-arm:0);
  if(P.type==='downloadRitual'&&v.p.id==='core')v.rot-=.07*hold;
  const q=v.a.bounds,dx=((q[0]+q[2])/2-v.anchor[0])*v.k,dy=((q[1]+q[3])/2-v.anchor[1])*v.k;v.x=v.ax+dx*Math.cos(v.rot)-dy*Math.sin(v.rot);v.y=v.ay+dx*Math.sin(v.rot)+dy*Math.cos(v.rot);return v;});
};
function dr21EyeMask(v){if(DR21.eyes.has(v.key))return DR21.eyes.get(v.key);if(!XART.rdy(v.key))return null;const c=document.createElement('canvas');c.width=c.height=320;const g=c.getContext('2d');g.drawImage(XART.get(v.key),0,0);const d=g.getImageData(0,0,320,320);for(let y=0;y<320;y++)for(let x=0;x<320;x++){const i=(y*320+x)*4,r=d.data[i],g=d.data[i+1],b=d.data[i+2],eye=y>75&&y<130&&x>135&&x<195&&r>165&&(r>g*1.3||g>170&&b<180||Math.max(r,g,b)-Math.min(r,g,b)<50);d.data[i+3]=eye?d.data[i+3]:0;d.data[i]=d.data[i+1]=d.data[i+2]=255;}g.putImageData(d,0,0);DR21.eyes.set(v.key,c);return c;}
v19Paint=function(v,b){const out=DR21.base.paint.apply(this,arguments),P=b?._r30?.v18?.attack;if(P?._dr21&&P.type==='downloadRitual'&&v.p.id==='core'){const im=dr21EyeMask(v);if(im){ctx.save();ctx.translate(v.ax,v.ay);ctx.rotate(v.rot);ctx.globalAlpha=.8;ctx.drawImage(im,-v.anchor[0]*v.k,-v.anchor[1]*v.k,320*v.k,320*v.k);ctx.restore();}}return out;};
v18Warnings=function(b){const P=b?._r30?.v18?.attack;if(!P?._dr21)return DR21.base.warnings.apply(this,arguments);
 if(P.type==='shadowAscension')return; // Mike: the approaching ball is its own tell; no FOV or reticle.
 if(P.type==='ghostTeleport'){if(P.strike&&P.t<P.tell+P.hops*P.hop+P.slamTell)groundTargetReticleDraw(P.target.x,P.target.y,106,(P.t-P.tell-P.hops*P.hop)/P.slamTell,.95);return;}
 if(P.t>=P.tell)return;const progress=P.t/P.tell;
 if(P.type==='machineGrab'){combatWarningDraw(b,{x:P.origin.x,y:P.origin.y,ex:P.target.x,ey:P.target.y,width:72,progress,fieldOnly:true});groundTargetReticleDraw(P.target.x,P.target.y,88,progress,.9);}
 else if(P.type==='machineLasers')for(const L of P.lanes)combatWarningDraw(b,{...L,progress,fieldOnly:true});
 else if(P.type==='armOrbs')for(const p of P.ports)combatWarningDraw(b,{x:p.x,y:p.y,ex:P.target.x,ey:P.target.y,width:100,progress,fieldOnly:true});
};
// Retained archive attacks follow the same FOV-only presentation as the new
// book. Their existing clocks and committed targets are unchanged.
d20Warnings=function(b){const P=b?._r30?.v18?.attack;if(!P?._d20)return;
 if(P.type==='armLasers'){for(const q of P.arms){const t=P.t-q.at,L=d20ArmLane(b,q);if(!q.disabled&&L&&t>=0&&t<q.tell){combatWarningDraw(b,{...L,progress:t/q.tell,fieldOnly:true});groundTargetReticleDraw(q.target.x,q.target.y,72,t/q.tell,.75);}}return;}
 if(P.t>=P.tell)return;const progress=P.t/P.tell,m=d20BossMount(b,'core');if(!m)return;
 if(P.type==='spiralLightning'){const count=2+d20Rank();for(let i=0;i<count;i++){const a=i*TAU/count;combatWarningDraw(b,{x:m.x,y:m.y,ex:m.x+Math.cos(a)*280,ey:m.y+Math.sin(a)*280,len:280,width:26,progress,fieldOnly:true});}}
 else if(P.type==='coreMissiles')combatWarningDraw(b,{x:m.x,y:m.y,ex:P.target.x,ey:P.target.y,width:165,progress,fieldOnly:true});
 else groundTargetReticleDraw(P.target.x,P.target.y,125,progress,.7);
};
function dr21Shield(b){const P=b?._r30?.v18?.attack;return P?._dr21&&['downloadRitual','codeAegis'].includes(P.type)&&P.shield>0&&P.t<P.tell+P.active?P:null;}
modularHit=function(dmg){const b=boss,P=dr21Shield(b);if(!P||!r30Live(b)||b._noHit||!(dmg>0))return DR21.base.hit.apply(this,arguments);
 const part=b.parts.includes(b._lastPart)?b._lastPart:b.parts[0];markHit(b,.12);if(part)markHit(part,.12);P.shield=Math.max(0,P.shield-dmg);P.shieldFlash=.18;dr21Cue(P.shield?'shieldHitHeavy':'shieldBreakCombat');dr21Log('shield-absorb',{remaining:P.shield});
};
bossShieldFrac=function(b){const P=dr21Shield(b);return P?clamp(P.shield/P.shieldMax,0,1):DR21.base.shieldFrac.apply(this,arguments);};
target17BossContact=function(b){if(b?._r30?.v18?.attack?._dr21)return false;return DR21.base.contact.apply(this,arguments);};
function dr21DrawAttack(b){const P=b._r30.v18.attack,t=P.t,u=t-P.tell;v18Warnings(b);
 if(P.type==='shadowAscension'){const size=u<0?lerp(35,145,clamp(t/P.tell,0,1)):P.projectedSize||70,fade=u<P.travel?1:1-clamp((u-P.travel)/.6,0,1);dr21Art('ball',t,P.x,P.y,size,fade,false,P.spin||0);}
 if(P.type==='ghostTeleport'){if(u>=0&&u<P.hops*P.hop){const bank=v18Model(b)==='ghost'?'fade_ghost':'fade_main';dr21Art(bank,Math.max(0,.49-P.ghostAt),b.x,b.y,v18Size(b),clamp(P.ghostAt/.36,0,1),true);if(P.depart)dr21Art(bank,P.ghostAt,P.depart.x,P.depart.y,v18Size(b),.65*(1-clamp(P.ghostAt/.36,0,1)),true);}if(P.slamAge>=0&&P.slamAge<.7)dr21Art('erase',P.slamAge,P.target.x,P.target.y,150,1,true);}
 if(P.type==='downloadRitual'){dr21Art('download',t,b.x,b.y-v18Size(b)*.24*P.depth,150);}
 if(dr21Shield(b)){P.shieldFlash=Math.max(0,(P.shieldFlash||0)-.016);dr21Art(j3State(b).encounter===1?'shield':'shield_main',t,b.x,b.y,v18Size(b)*1.12*(P.depth||1),.55+(P.shieldFlash||0)*2);}
 if(P.type==='armOrbs')for(const p of v18Ports(b))if(u<0)dr21Art('ball',t,p.x,p.y,38+40*clamp(t/P.tell,0,1));
 if(P.type==='machineLasers')for(let i=0;i<P.lanes.length;i++){const L=P.lanes[i],age=u-i*.95;if(age>=0&&age<.48&&b.parts.some(p=>p.id===L.module&&!p.destroyed))av3Beam(ctx,L.x,L.y,Math.atan2(L.ey-L.y,L.ex-L.x),Math.hypot(viewW(),viewH())+100,18,'void',age,1,true);}
}
function dr21Back(b){return b?._r30?.mode==='fight'&&b._r30.v18.attack?._dr21&&b._r30.v18.attack.depth<.8;}
function dr21Arena(b){const out=DR21.base.arena.apply(this,arguments);if(dr21Back(b)){const P=b._r30.v18.attack;ctx.save();ctx.globalAlpha*=P.opacity??1;v19Body(b);ctx.restore();if(P.type==='downloadRitual')dr21DrawAttack(b);}return out;}
v17ArenaDraw=dr21Arena;aa5ArenaDraw=dr21Arena;
// A sheet has sixteen real PixelLab wireframe frames, all on the exact same
// native reference pivot. The moving scan reveals the live rig at 60 Hz.
function dr21Download(b,t,duration,incoming){const name=v18Model(b),a=DR22_ART.forms[name];if(!a||!XART.rdy(a.key))return false;
 const u=clamp(t/duration,0,1),reveal=v19Ease(incoming?(u-.26)/.62:(u-.06)/.62),growth=incoming?lerp(.22,1,v19Ease(u/.22)):lerp(1,.22,v19Ease((u-.76)/.24)),size=v18Size(b)*a.w/(a.captureSize*a.captureScale),top=b.y-size/2,cut=top+size*reveal,frame=Math.floor(Math.max(0,t)/.07)%a.frames,k=size/a.w;
 // Frame the whole download below the HUD, then ease back into the live rig.
 // This is a render translation; combat positions and sockets do not move.
 const offsetY=Math.max(0,viewTopY()+72-(b.y+(a.bounds[1]-a.pivot[1])*k))*(incoming?1-v19Ease((u-.88)/.12):v19Ease(u/.15));ctx.save();ctx.translate(0,offsetY);
 const wire=()=>{ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(b.x,b.y);ctx.scale(growth,growth);ctx.drawImage(XART.get(a.key),(frame%a.columns)*a.w,Math.floor(frame/a.columns)*a.h,a.w,a.h,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();};
 ctx.save();ctx.beginPath();ctx.rect(b.x-size, incoming?cut:top-1,size*2,incoming?Math.max(0,top+size-cut+1):Math.max(0,cut-top+1));ctx.clip();wire();ctx.restore();
 ctx.save();ctx.beginPath();ctx.rect(b.x-size,incoming?top:cut,size*2,incoming?Math.max(0,cut-top):Math.max(0,top+size-cut));ctx.clip();v19Body(b);ctx.restore();
 if(reveal>0&&reveal<1){ctx.save();ctx.beginPath();ctx.rect(b.x-size,cut-4,size*2,8);ctx.clip();ctx.globalCompositeOperation='lighter';wire();ctx.restore();}
 if(incoming?u<.24:u>.76)dr21Art('download',t,b.x,b.y,70,.7);
 ctx.restore();DR21.transition={name,incoming,u,reveal,frame,growth,offsetY};DR21.draws['wire_'+name]=(DR21.draws['wire_'+name]||0)+1;return true;
}
v18SetMode=function(b,mode){const out=DR21.base.setMode.apply(this,arguments);if(v18Owned(b)&&['v18formIn','v18reveal','v19FinalReform'].includes(mode))dr21Cue('teleportIn');return out;};
r30DrawBoss=function(b){if(v18Owned(b)){const S=b._r30,N=S.v18;
 if(['v18formOut','v18formIn'].includes(S.mode)&&dr21Download(b,S.t,S.mode==='v18formOut'?1.45:1.6,S.mode==='v18formIn'))return;
 if(S.mode==='v18reveal'&&dr21Download(b,S.t,2.8,true))return;
 if(S.mode==='v19FinalReform'&&dr21Download(b,S.t,2.2,true))return;
 if(S.mode==='v18phaseFade'&&N.transition?.switched&&dr21Download(b,Math.max(0,S.t-1.55),3.35,true))return;
 if(S.mode==='v18conversion'){const t=S.t,u=v19Ease(t/4);v18Cell(V18_ART.drone,b.x,b.y,v18Size(b)*.8,1-u);dr21Art('symbiote',t,b.x,b.y,v18Size(b)*lerp(.6,1.15,u),Math.sin(clamp(t/4.3,0,1)*Math.PI));if(t>1.8)dr21Download(b,t-1.8,2.5,true);return;}}
 const P=b?._r30?.v18?.attack;if(!P?._dr21)return DR21.base.draw.apply(this,arguments);if(b.dead||b._r30.mode!=='fight')return;
 if(!dr21Back(b)&&!(P.type==='ghostTeleport'&&P.t>=P.tell&&P.t<P.tell+P.hops*P.hop)){ctx.save();ctx.globalAlpha*=P.opacity??1;v19Body(b);ctx.restore();}if(!(dr21Back(b)&&P.type==='downloadRitual'))dr21DrawAttack(b);
};
v18Enter=function(b){const out=DR21.base.enter.apply(this,arguments);if(v18Owned(b))b._r30.v18.demonWave=0;return out;};
v18Clear=function(b){const P=b?._r30?.v18?.attack;if(P?._dr21){b.x=P.origin.x;b.y=P.origin.y;b._noHit=false;dr21Log('cancel',{type:P.type});}return DR21.base.clear.apply(this,arguments);};
D20.roster.demonJet={name:'INFERNAL WIRE JET',sourceHP:160,size:156,role:'siege',key:DR21_ART.banks.jet[0].key};
D20.roster.demonRobot={name:'DAEMON SENTINEL',sourceHP:210,size:172,role:'siege',key:DR21_ART.banks.robot[0].key};
d20Enemy=function(kind,x,y,b,mini){const e=DR21.base.enemy.apply(this,arguments);if(e&&kind!=='bomb'){const A=e._d20;if(!mini&&!A.mini){e.hp=e.maxhp=e._maxhp=Math.ceil(A.sourceHP*.5);const side=Math.round(e.hp*.22);A.parts.forEach(p=>p.hp=p.maxhp=p.id==='core'?e.hp-2*side:side);}if(['demonJet','demonRobot'].includes(kind)){const a=DR21_ART.banks[kind==='demonJet'?'jet':'robot'][0],k=256/a.w*D20.roster[kind].size/320;e.w=(a.bounds[2]-a.bounds[0])*k*.9;e.h=(a.bounds[3]-a.bounds[1])*k*.9;}e._dr21Helper=true;}return e;};
d20Model=function(kind){if(!['demonJet','demonRobot'].includes(kind))return DR21.base.model.apply(this,arguments);const bank=kind==='demonJet'?'jet':'robot',age=D20.clock||0,f=Math.floor(age*12)%DR21_ART.banks[bank].length,key=kind+':'+f;if(DR21.models.has(key))return DR21.models.get(key);
 const a=DR21_ART.banks[bank][f];if(!XART.rdy(a.key))return null;const im=XART.get(a.key),c=document.createElement('canvas');c.width=c.height=320;c.getContext('2d').drawImage(im,32,32,256,256);const full={key:'dr21-model-'+key,image:c,w:320,h:320,pivot:[160,160]},parts={};
 for(const id of ['core','left','right']){const p=document.createElement('canvas');p.width=p.height=320;const g=p.getContext('2d');g.drawImage(c,0,0);g.globalCompositeOperation='destination-in';g.fillStyle='#fff';g.fillRect(id==='left'?0:id==='right'?208:112,0,id==='core'?96:112,320);parts[id]={...full,key:full.key+'-'+id,image:p};}
 const model={full,parts,download:[],mounts:{core:[160,160],left:[90,205],right:[230,205]},muzzles:{core:[160,220],left:[90,205],right:[230,205]}};DR21.models.set(key,model);return model;
};
d20Download=function(e,erasing=false){const A=e._d20,M=d20Model(A.kind);if(!M)return;const progress=clamp(A.t/(erasing?.8:2),0,1),size=D20.roster[A.kind].size,bank=A.kind==='demonJet'?'jet_download':A.kind==='demonRobot'?'robot_download':null;
 if(bank&&DR21_ART.banks[bank]){const rows=DR21_ART.banks[bank],f=Math.min(rows.length-1,Math.floor((erasing?progress:1-progress)*rows.length)),a=rows[f];v18Cell(a,e.x,e.y,size*.75,erasing?1-progress:progress);}
 else{ctx.save();ctx.globalAlpha=erasing?1-progress:progress;d20Art(M.full,e.x,e.y,size);ctx.restore();}dr21Art('download',A.t,e.x,e.y,size*1.3);if(!erasing)groundTargetReticleDraw(e.x,e.y,size*.7,progress,.5);
};
d20Fx=function(name,t,x,y,size,angle=0,alpha=1,loop=true){if(name==='transfer_loop')return dr21Art('download',t,x,y,size,alpha);return DR21.base.fx.apply(this,arguments);};
// Capture the live Furyship and pilot palette, never the retired space atlas.
// Exact currently equipped aircraft, captured once at death, is the victim.
// Shields, iframe checks, life accounting and respawn stay with playerHit.
function dr21DeathKind(source){const s=String(source||'').toLowerCase();if(/shadow eradication|spectral soul bomb|death.?ball/.test(s))return 'shadow';if(/machine grab/.test(s))return 'throw';if(/ice|cryo|frost|freez/.test(s))return 'ice';if(/laser|beam/.test(s))return 'laser';if(/fire|flame|burn|magma|^s2/.test(s))return 'burn';return null;}
function dr21ProjectileDeathSource(q){return q._frostNoseLaser||q._s3ice?'ice':q._hammerLaser?'laser':q._pt11Wave?'firewall':String(q.kind||'');}
v18Shot=function(b){const q=DR21.base.shot.apply(this,arguments);if(q&&b?._r30?.v18?.attack?.type==='armOrbs')q._dr21Orb=true;return q;};
drawCombatFinalProjectile=function(q){if(q?._dr21Orb){dr21Art('ball',q.t||0,q.x,q.y,72);return true;}if(q?._v19Symbiote){dr21Art('symbiote',q.t||0,q.x,q.y,(q.w||16)*3);return true;}return DR21.base.projectile.apply(this,arguments);};
function dr21Hull(){let im=spaceShipActive()?furyShipCanvas('base',_pilotKey()):XART.rdy('ship_'+_pilotKey()+'_sp0')?XART.get('ship_'+_pilotKey()+'_sp0'):null;if(!im)return null;
 const c=document.createElement('canvas');c.width=c.height=192;const g=c.getContext('2d'),k=120/Math.max(im.width,im.height);g.imageSmoothingEnabled=false;g.drawImage(im,96-im.width*k/2,96-im.height*k/2,im.width*k,im.height*k);return c;}
playerHit=function(source){const kind=dr21DeathKind(source),was=player.dead,hull=kind&&!was?dr21Hull():null;if(!was)player._dr21Death=null;const out=DR21.base.playerHit.apply(this,arguments);
 if(kind&&!was&&player.dead&&hull){if(kind==='ice'){const g=hull.getContext('2d');g.globalCompositeOperation='source-atop';g.fillStyle='rgba(150,225,255,.75)';g.fillRect(0,0,192,192);g.globalCompositeOperation='source-over';}const ball=boss?._r30?.v18?.attack,foreground=kind==='shadow'&&ball?.type==='shadowAscension'?Math.max(300,ball.projectedSize||0):300;player._dr21Death={kind,t:0,life:kind==='shadow'?1.7:1.5,x:player.x,y:player.y,image:hull,foreground,ballTime:kind==='shadow'&&ball?.type==='shadowAscension'?ball.t:0};player._spin=null;player._voidDeath=null;player.deathT=player._dr21Death.life+.4;dr21Cue(kind==='ice'?'enemyIceBolt':kind==='burn'?'flameThrowerStart':'fireIceOrbImpact');}return out;
};
updateDeathSpin=function(dt){const D=player._dr21Death;if(!player.dead){player._dr21Death=null;return DR21.base.deathTick.apply(this,arguments);}if(!D)return DR21.base.deathTick.apply(this,arguments);D.t+=dt;if(D.t>=D.life&&!D.ended){D.ended=true;if(D.kind==='burn'){explode(D.x,D.y,85,'red');dr21Cue('fireIceOrbImpact');}shake=Math.max(shake,5);}};
function dr21HullDeath(D){const t=D.t,u=clamp(t/D.life,0,1),scale=D.kind==='shadow'?lerp(.60,3.25,v19Ease(u/.65)):.65,x=D.kind==='throw'?lerp(D.x,camRightX()+120,v19Ease(u)):D.x,y=D.y-(D.kind==='shadow'?80*v19Ease(u):0),size=192*scale;
 if(D.kind==='shadow')dr21Art('ball',t+(D.ballTime||0),x,y,lerp(D.foreground||300,Math.max(1100,(D.foreground||300)*1.4),v19Ease(u)),1-clamp((u-.75)/.25,0,1),false,(t+(D.ballTime||0))*TAU*.85);
 if(D.kind==='ice'&&u>.40){const q=(u-.4)/.6;for(let iy=0;iy<3;iy++)for(let ix=0;ix<3;ix++){const dx=(ix-1)*90*q,dy=(iy-1)*90*q+90*q*q;ctx.save();ctx.translate(x+dx,y+dy);ctx.rotate((ix-iy)*q*2);ctx.globalAlpha=1-clamp((q-.65)/.35,0,1);ctx.drawImage(D.image,ix*64,iy*64,64,64,(ix-1.5)*size/3,(iy-1.5)*size/3,size/3,size/3);ctx.restore();}}
 else if(u<.86){ctx.save();ctx.translate(x,y);if(D.kind==='burn'||D.kind==='throw')ctx.rotate(u*TAU*2);if(D.kind==='laser'||D.kind==='shadow'){ctx.beginPath();ctx.rect(-size/2,-size/2,size,size*(1-clamp((u-.24)/.5,0,1)));ctx.clip();}ctx.drawImage(D.image,-size/2,-size/2,size,size);ctx.restore();}
 if(D.kind==='shadow')dr21Art('erase',Math.max(0,t-.3),x,y,200+u*280,.65,true);
 else if(D.kind==='ice')dr21Art('ice',Math.max(0,t-.20),x,y,170,1-clamp((u-.35)/.25,0,1),true);
 else if(D.kind==='laser')dr21Art('erase',t,x,y,200,1,true);
 else if(D.kind==='burn'){const key=P2_ART.fire[Math.floor(t*18)%P2_ART.fire.length];v18Cell(key,x,y,120+u*60);}
}
drawDeathSpin=function(){const D=player._dr21Death;if(player.dead&&D){if(D.t<D.life)dr21HullDeath(D);return;}return DR21.base.deathDraw.apply(this,arguments);};
beginStage=function(){for(const seat of seatList())withSeat(seat,()=>{player._dr21Death=null;});return DR21.base.begin.apply(this,arguments);};
// The same mechanical parasite appears in gameplay and surviving-fragment cuts.
for(const key of ['cin_origin_symbiote','cinend_symbiote_survivor'])XART._src[key]=DR21_ART.banks.symbiote[0].path;
XART._src.cin_war_symbiote_twoeyes=DR21_ART.banks.symbiote[0].path;
for(const key of ['cin_origin_emerges_0924','pt11_mystery_emergence'])XART._src[key]='assets/game/shared/cinematics/dracodia_demon_1019/emergence.webp';
for(const key of ['cin_origin_contact_0924','pt11_mystery_contact','cin_origin_arrival','cin_origin_satellite'])XART._src[key]='assets/game/shared/cinematics/dracodia_demon_1019/contact.webp';
drawWorld=function(dt){const out=DR21.base.world.apply(this,arguments),b=boss,P=b?._r30?.v18?.attack,R=b?j3State(b)?.dr5?.radio:null;
 if(P?._dr21&&R&&R.t<dr5TalkDuration(R.text)){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;const y=Math.max(viewTopY()+40,106),h=pcFontFit(R.text,VW-24,14,10);pcFontCenter(R.text,VW/2,y,h,'#f4e8ff',1);DR21.caption={text:R.text,y};ctx.restore();}
 return out;
};
globalThis.BOF_DRACODIA_DEMON={state:DR21,begin:dr21Begin,warm:dr21Warm,draw:dr21DrawAttack};
