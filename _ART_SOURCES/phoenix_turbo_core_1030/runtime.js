'use strict';
/* PH82 owns the Phoenix cannon station. Cannon rounds are parallel physical
   bullets; the one laser field belongs to the measured chest core. */
const PH82={base:{tick:v19NativeTick,draw:r30DrawBoss,body:v19Body,rig:v19VolcanoRig,at:r30At,muzzle:ph21Muzzle,pose:bi24AttackPose,hit:modularHit,clear:v18Clear,mode:v18SetMode,scene:ad20Scene,projectile:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,targetTick:target17Tick,targetDraw:target17Draw,keys:v18Keys,warm:v18Warm,load:stageLoadBegin},events:[],draws:{},serial:0};
for(const [key,a]of Object.entries(PH82_ART.pages)){XART._src[key]=a.path;if(a.hitKey)XART._src[a.hitKey]=a.hitPath;}
for(const rows of Object.values(PH82_ART.arena))for(const a of rows)XART._src[a.key]=a.path;
function ph82Keys(){return[...Object.entries(PH82_ART.pages).flatMap(([key,a])=>a.hitKey?[key,a.hitKey]:[key]),...Object.values(PH82_ART.arena).flatMap(rows=>rows.map(a=>a.key))];}
v18Keys=function(){return[...PH82.base.keys(),...ph82Keys()];};
v18Warm=function(){const prior=PH82.base.warm();return ph82Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(['bossWeaponCharge','furnaceLaserCharge','furnaceLaserBurst','enemyBossCannon']);return PH82.base.load.call(this,n,n===8?[...(keys||[]),...ph82Keys()]:keys);};
function ph82Full(b){return !!b&&!b.dead&&ph21Own(b)&&b._r30.mode==='fight'&&ph21State(b)?.stage==='cannons';}
// The final covered handoff changes form before rebuilding parts. Retire the
// Phoenix-only wing/claw IDs using the native zero-HP anatomy, never a healed life.
v18SetMode=function(b,mode){const N=b?._r30?.v18,Q=b?._r30&&j3State(b).ph21;if(mode==='v19FinalReform'&&N?.deathForm===2&&Q&&b.parts===Q.parts){v18PartsBuild(b,0);ph82Log(b,'final-anatomy',{hp:b.hp,parts:b.parts.map(p=>p.id)});}return PH82.base.mode.apply(this,arguments);};
function ph82State(b){return ph21State(b).ph82??={seed:0x8240351,decisions:0,guns:0,goal:null,side:1,flash:{cannonL:-99,cannonR:-99},barrel:{cannonL:0,cannonR:0}};}
function ph82Log(b,event,data={}){PH82.events.push({event,clock:b._r30.clock,...data});if(PH82.events.length>500)PH82.events.shift();}
function ph82Rand(Q){let s=Q.seed;s^=s<<13;s^=s>>>17;s^=s<<5;Q.seed=s>>>0;return Q.seed/4294967296;}
function ph82Pose(b){const Q=ph21State(b),P=Q.action;let phase='recover',f;
 if(P?._ph82){if(P.t<P.tell){phase='wind';f=Math.min(8,Math.floor(P.t/P.tell*9));}else if(P.kind==='core'){phase='wind';f=8;}else if(P.t<P.tell+P.active){phase='strike';f=Math.floor((P.t-P.tell)*20)%9;}else{phase='recover';f=Math.min(4,Math.floor((P.t-P.tell-P.active)/P.recover*5));}}
 else{const n=Math.floor(Q.age*8)%8;f=n<=4?n:8-n;}
 return{phase,f,pose:PH82_ART.poses[phase+'_'+f]};
}
function ph82Dead(b){return(ph21Alive(b,'cannonL')?0:1)|(ph21Alive(b,'cannonR')?0:2);}
function ph82Frame(b){const q=ph82Pose(b);return PH82_ART.banks['body_'+q.phase+'_'+ph82Dead(b)][q.f];}
function ph82Blit(name,f,x,y,hit=false){const rows=PH82_ART.banks[name];if(!rows)return false;const a=rows[clamp(f|0,0,rows.length-1)],page=PH82_ART.pages[a.key],key=hit&&page.hitKey?page.hitKey:a.key;if(!XART.rdy(key))return false;ctx.drawImage(XART.get(key),...a.rect,Math.round(x+a.offset[0]),Math.round(y+a.offset[1]),a.w,a.h);PH82.draws[name]=(PH82.draws[name]||0)+1;return true;}
function ph82Socket(b,id,barrel=0){const q=ph82Pose(b).pose,p=id==='core'?q.core:q.sockets[id]?.[(barrel|0)%2];return p?{x:Math.round(b.x)+p[0],y:Math.round(b.y)+p[1]}:null;}
ph21Muzzle=function(b,id,barrel=0){return ph82Full(b)?ph82Socket(b,id,barrel):PH82.base.muzzle.apply(this,arguments);};
bi24AttackPose=function(b,actor){if(actor!=='phoenix'||!ph82Full(b))return PH82.base.pose.apply(this,arguments);const q=ph82Pose(b);return{a:BI24_ART.banks['phoenix_'+q.phase],f:q.f};};
function ph82Dodge(b){const Q=ph82State(b),danger=pBullets.find(p=>!p.dead&&(p.vy||0)<-.5&&p.y>b.y+15&&p.y<b.y+250&&Math.abs(p.x-b.x)<85);let side=danger?(danger.x<b.x?1:-1):(player.x<b.x?1:player.x>b.x?-1:-Q.side);let x=clamp(b.x+side*(90+ph82Rand(Q)*30),camLeftX()+154,camRightX()-154);if(Math.abs(x-b.x)<25){side=-side;x=clamp(b.x+side*110,camLeftX()+154,camRightX()-154);}Q.side=side;Q.goal={x,y:viewTopY()+160+ph82Rand(Q)*48};ph82Log(b,'evade',{from:{x:b.x,y:b.y},to:{...Q.goal},visibleThreat:!!danger});}
function ph82Move(b,dt){const Q=ph82State(b);if(!Q.goal)ph82Dodge(b);const speed=85+b20Rank()*12;b.x+=clamp(Q.goal.x-b.x,-speed*dt,speed*dt);const y=Q.goal.y+Math.sin(ph21State(b).age*1.8)*7;b.y+=clamp(y-b.y,-48*dt,48*dt);}
function ph82Dir(angle){return clamp(Math.round((angle*180/Math.PI-45)/7.5),0,12);}
function ph82Start(b,kind){if(!ph82Full(b))return null;const Q=ph21State(b),S=ph82State(b),rank=b20Rank();if(!kind){const pick=ph82Rand(S);kind=S.guns>=3||S.guns>=1&&pick<.36?'core':'guns';}if(kind==='guns')S.guns++;else S.guns=0;S.decisions++;
 const P=Q.action={_ph82:true,mode:'ph82-'+kind,kind,t:0,serial:++PH82.serial,tell:kind==='core'?[2,1.8,1.6,1.45][rank]:[1.65,1.5,1.35,1.2][rank],active:kind==='core'?.85:1.25,recover:kind==='core'?.65:.45,next:0,round:0,locked:false,dir:6,origin:{x:b.x,y:b.y}};
 b._r30.v18.attack=b._r30.attack=P;combatWarningTick(b,'ph82-'+P.serial,0,P.tell,true);Snd.play(kind==='core'?'furnaceLaserCharge':'bossWeaponCharge',.65);ph82Log(b,'tell',{kind,tell:P.tell,hp:b.hp});return P;
}
function ph82Lock(b,P){P.locked=true;P.anchor={x:b.x,y:b.y};const core=ph82Socket(b,'core'),S=ph82State(b);P.target={x:player.x+(ph82Rand(S)-.5)*30,y:player.y};P.dir=ph82Dir(Math.atan2(P.target.y-core.y,P.target.x-core.x));ph82Log(b,'aim-commit',{kind:P.kind,dir:P.dir,core,target:P.target});}
function ph82Shoot(b,P){const S=ph82State(b),barrel=P.round%2;let count=0;for(const id of ['cannonL','cannonR'])if(ph21Alive(b,id)){const at=ph82Socket(b,id,barrel);eBullets.push({kind:'mg',x:at.x,y:at.y,vx:0,vy:5.6+b20Rank()*.25,w:5,h:12,t:0,_ph:0,_ph82Owner:b,_ph82Type:'gun',_ph21Owner:b,_v18Owner:b,_weaponProof:true,_shootable:false});S.flash[id]=b._r30.clock;S.barrel[id]=barrel;ph82Log(b,'turbo-round',{id,barrel,x:at.x,y:at.y,vx:0});count++;}if(count)Snd.play('enemyBossCannon',.34);P.round++;}
function ph82Beam(P){const u=P.t-P.tell;if(u<.16)return{name:'launch_'+P.dir,f:Math.min(4,Math.floor(u/.032))};return{name:'beam_'+P.dir,f:Math.floor(u*24)%8};}
function ph82Inside(a,at,x,y){const row=a.spans[Math.floor(y-at.y-a.offset[1])],xx=Math.floor(x-at.x-a.offset[0]);if(!row)return false;for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return true;return false;}
function ph82Finish(b,P){const Q=ph21State(b);Q.action=null;b._r30.v18.attack=b._r30.attack=null;Q.cool=[1.1,1,.9,.8][b20Rank()];ph82Dodge(b);j3Save(b);ph82Log(b,'recovery',{kind:P.kind,rounds:P.round});}
function ph82Cancel(b){const Q=ph21State(b);if(Q?.action?._ph82)Q.action=null;if(b?._r30?.v18?.attack?._ph82)b._r30.v18.attack=b._r30.attack=null;for(const q of eBullets)if(q._ph82Owner===b)q.dead=true;}
v19NativeTick=function(b,dt){if(!ph82Full(b)){if(ph21Own(b)&&b._r30.v18.attack?._ph82)ph82Cancel(b);return PH82.base.tick.apply(this,arguments);}const Q=ph21State(b),N=b._r30.v18,S=ph82State(b);Q.age+=dt;N.donorAge=(N.donorAge||0)+dt;Q.cool=Math.max(0,Q.cool-dt);Q.scale=1;Q.angle=Q.wing=Q.claws=0;b._noHit=false;
 if(!Q.action){if(Q.cool<=0)ph82Start(b);else ph82Move(b,dt);}const P=Q.action;
 if(P?._ph82){P.t+=dt;if(P.t<P.tell*.5){ph82Move(b,dt);const core=ph82Socket(b,'core');P.dir=ph82Dir(Math.atan2(player.y-core.y,player.x-core.x));}else{if(!P.locked)ph82Lock(b,P);b.x=P.anchor.x;b.y=P.anchor.y;}combatWarningTick(b,'ph82-'+P.serial,Math.min(P.t,P.tell),P.tell);const u=P.t-P.tell;
  if(u>=0&&u<P.active){if(P.kind==='guns'){const interval=[.14,.115,.095,.08][b20Rank()];if(u>=P.next){P.next+=interval;ph82Shoot(b,P);}}else{if(!P.released){P.released=true;Snd.play('furnaceLaserBurst',.75);ph82Log(b,'core-beam',{origin:ph82Socket(b,'core'),dir:P.dir});}const q=ph82Beam(P),a=PH82_ART.banks[q.name][q.f],at=ph82Socket(b,'core');for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&[[0,0],[-4,0],[4,0],[0,-4],[0,4]].some(([x,y])=>ph82Inside(a,at,player.x+x,player.y+y)))playerHit('Phoenix core laser');});}}
  if(P.t>=P.tell+P.active+P.recover)ph82Finish(b,P);
 }
 b._drawY=b.y;ph21Part(b,'core').hp=b.hp;j3Save(b);if(N.donorAge>46&&!Q.action&&j3State(b).hp[0]>0)j3Morph(b,'home');
};
function ph82Body(b){const q=ph82Pose(b),hit=Math.max(b.flash||0,...b.parts.map(p=>p.flash||0))>0;ph82Blit('body_'+q.phase+'_'+ph82Dead(b),q.f,b.x,b.y,hit);const P=ph21State(b).action;if(P?._ph82&&P.kind==='core'){const u=P.t-P.tell,level=u<0?clamp(Math.round(1+P.t/P.tell*4+Math.sin(P.t*22)*.6),1,5):u<P.active?5:clamp(Math.ceil(5*(1-(u-P.active)/P.recover)),1,5);ph82Blit('core_'+q.phase+'_'+level,q.f,b.x,b.y);}}
v19Body=function(b){return ph82Full(b)?ph82Body(b):PH82.base.body.apply(this,arguments);};
v19VolcanoRig=function(b){if(!ph82Full(b))return PH82.base.rig.apply(this,arguments);const a=ph82Pose(b).pose;return b.parts.filter(p=>!p.destroyed).map(p=>{const q=a.parts[p.id];return{p,x:Math.round(b.x)+q[0],y:Math.round(b.y)+q[1],w:q[2],h:q[3],ax:b.x,ay:b.y,layer:p.id,spec:p.spec,_ph82:true};});};
r30At=function(b,x,y){if(!ph82Full(b))return PH82.base.at.apply(this,arguments);if(!r30Live(b)||b._noHit)return null;const a=ph82Pose(b).pose,row=a.hitRows[Math.floor(y-Math.round(b.y)+256)],xx=Math.floor(x-Math.round(b.x)+256);if(!row)return null;for(let i=0;i<row.length;i+=3)if(xx>=row[i]&&xx<row[i+1]){const p=ph21Part(b,PH82_ART.ids[row[i+2]]);return p&&ph21Vulnerable(b,p)?p:null;}return null;};
r30DrawBoss=function(b){if(!ph82Full(b))return PH82.base.draw.apply(this,arguments);const Q=ph21State(b),P=Q.action,S=ph82State(b);if(P?._ph82&&P.t<P.tell){const colour=P.t/P.tell<.4?'green':P.t/P.tell<.74?'yellow':'red';if(P.kind==='core'){const p=ph82Socket(b,'core');ph82Blit(colour+'_'+P.dir,0,p.x,p.y);}else for(const id of ['cannonL','cannonR'])if(ph21Alive(b,id)){const p=ph82Socket(b,id);ph82Blit(colour+'_6',0,p.x,p.y);}rd72Blit('asterisk',Math.floor(P.t*9)%2,b.x,Math.max(viewTopY()+65,b.y-120));}ph82Body(b);
 if(P?._ph82&&P.kind==='core'){const u=P.t-P.tell,at=ph82Socket(b,'core');if(u>=0&&u<P.active){const q=ph82Beam(P);ph82Blit(q.name,q.f,at.x,at.y);}else if(u>=P.active&&u<P.active+.32)ph82Blit('recover_'+P.dir,Math.floor((u-P.active)/.32*4),at.x,at.y);}
 for(const id of ['cannonL','cannonR'])if(ph21Alive(b,id)){const age=b._r30.clock-S.flash[id];if(age>=0&&age<.12){const m=ph82Socket(b,id,S.barrel[id]);hc79Bank('muzzle',Math.min(3,Math.floor(age/.12*4))*64+hc79Dir(Math.PI/2),m.x,m.y);}}
};
modularHit=function(dmg){const b=boss,was=ph82Full(b),P=was?ph21State(b).action:null,out=PH82.base.hit.apply(this,arguments);if(was&&!ph82Full(b)){ph82Cancel(b);if(P?.kind==='core')Snd.stopCue('furnaceLaserCharge');}return out;};
v18Clear=function(b){if(ph21Own(b)){ph82Cancel(b);Snd.stopCue('furnaceLaserCharge');}return PH82.base.clear.apply(this,arguments);};
drawCombatFinalProjectile=function(q){if(q?._ph82Type==='gun'){hc79Bank('round',Math.min(5,Math.floor((q.t||0)/.024))*64+hc79Dir(Math.PI/2),q.x,q.y);return true;}return PH82.base.projectile.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._ph82Owner?false:PH82.base.intercept.apply(this,arguments);};
target17Tick=function(b){if(ph82Full(b))return;return PH82.base.targetTick.apply(this,arguments);};
target17Draw=function(b){if(ph82Full(b))return;return PH82.base.targetDraw.apply(this,arguments);};
ad20Scene=function(b,theme,wire=false){if(theme!=='lava')return PH82.base.scene.apply(this,arguments);const t=b._r30.clock||0,f=Math.floor(t*10)%8,a=PH82_ART.arena[wire?'wire':'lava'][f],y=Math.floor(t*8)%256;if(XART.rdy(a.key))for(let yy=y-256;yy<VH;yy+=256)for(let x=0;x<worldWidth();x+=256)ctx.drawImage(XART.get(a.key),x,yy);
 const wallY=Math.floor(t*18)%256;for(const side of ['left','right']){const a=PH82_ART.arena[side][f],x=side==='left'?Math.floor(camLeftX()):Math.ceil(camRightX())-48;if(XART.rdy(a.key))for(let yy=wallY-256;yy<VH;yy+=256)ctx.drawImage(XART.get(a.key),x,yy);}PH82.arena={theme:'dark-lava',left:Math.floor(camLeftX()),right:Math.ceil(camRightX())-48,width:48,frame:f,lavaY:y,wallY};return true;
};
globalThis.BOF_PHOENIX_TURBO_CORE_1030=PH82;
