'use strict';
/* HC79: Dracodia's helicopter only. Fixed authored rotor/bank and pod turns;
   one pose owns pixels, hits, Retina targets, recoil and both muzzle sockets. */
const HC79={base:{enter:v18Enter,start:v18StartAttack,tick:r30Tick,draw:r30DrawBoss,body:v19Body,rig:v18Rig,at:v19AtRect,clear:v18Clear,rupture:v18Rupture,donor:v19Rupture,contact:target17BossContact,warnings:v18Warnings,scene:ad20Scene,plate:rd30Plate,projectile:drawCombatFinalProjectile,sonic:ovSonicProjectileDraw,intercept:enemyOrdnanceCanIntercept,load:stageLoadBegin,keys:v18Keys,warm:v18Warm,targetTick:target17Tick,targetDraw:target17Draw},events:[],draws:{},serial:0};
for(const [key,a]of Object.entries(HC79_ART.pages)){XART._src[key]=a.path;XART._src[a.hitKey]=a.hitPath;}
for(const a of Object.values(HC79_ART.arena))XART._src[a.key]=a.path;
function hc79Keys(){return[...Object.entries(HC79_ART.pages).flatMap(([k,a])=>[k,a.hitKey]),...Object.values(HC79_ART.arena).map(a=>a.key)];}
v18Keys=function(){return[...HC79.base.keys(),...hc79Keys()];};
v18Warm=function(){const prior=HC79.base.warm();return hc79Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(['overlordRotor','overlordGun','overlordRocket','coleSonicFull','bossWeaponCharge','retinaLockBeep']);return HC79.base.load.call(this,n,n===8?[...(keys||[]),...hc79Keys()]:keys);};
function hc79Own(b){return hc22Own(b);}
function hc79Live(b){return hc79Own(b)&&!b.dead&&b._r30.mode==='fight';}
function hc79Log(b,event,data={}){HC79.events.push({event,clock:b._r30.clock,...data});if(HC79.events.length>700)HC79.events.shift();}
function hc79State(b){return b._r30.v18.hc79??={age:0,seq:0,bank:6,bankAngle:0,rotor:0,turn:{left:0,right:0},kick:{left:0,right:0},flash:{left:-99,right:-99},sources:{},action:null,rig:null,smoke:0};}
function hc79Alive(b,id){return b.parts.some(p=>p.id===id&&!p.destroyed&&p.hp>0);}
function hc79Cancel(b){const Q=b?._r30?.v18?.hc79;if(!Q)return;for(const src of Object.values(Q.sources)){src.dead=true;for(const L of playerLocks)if(L.src===src)for(const sh of L.launches)sh.done=true;}Q.action=null;Q.rig=null;}
v18Enter=function(b,n,form){hc79Cancel(b);const out=HC79.base.enter.apply(this,arguments);if(n===2&&form===1){delete b._r30.v18.hc79;b._r30.v18.arenaPhase=2;hc79State(b);b.w=254;b.h=254;}return out;};
function hc79Dir(a){return((Math.round((a-Math.PI/2)/TAU*64)%64)+64)%64;}
function hc79Angle(d){return Math.PI/2+d*TAU/64;}
function hc79Joint(b,id){const Q=hc79State(b),q=HC79_ART.mounts[Q.bank|0][id];return{x:b.x+q[0],y:b.y+q[1]};}
function hc79Pod(b,id){const Q=hc79State(b),recoil=Q.kick[id]>.09?1:Q.kick[id]>0?2:0;return HC79_ART.banks['pod_'+id][recoil*64+hc79Dir(Q.turn[id]+Math.PI/2)];}
function hc79Socket(b,id,name='gun'){const q=hc79Joint(b,id),s=hc79Pod(b,id).sockets[name];return{x:q.x+s[0],y:q.y+s[1]};}
function hc79Aim(b,id,tx,ty,dt,locked=false){const Q=hc79State(b),p=hc79Joint(b,id),goal=Math.atan2(ty-p.y,tx-p.x)-Math.PI/2,d=Math.atan2(Math.sin(goal-Q.turn[id]),Math.cos(goal-Q.turn[id]));Q.turn[id]+=locked?d:clamp(d,-dt*3.1,dt*3.1);}
function hc79Start(b,kind){const Q=hc79State(b),rank=target17Rank();
 for(const src of Object.values(Q.sources))src.dead=true;
 const books=['guns','missiles','sonic','guns','dash','missiles'],armed=hc79Alive(b,'left')||hc79Alive(b,'right');
 if(!kind){for(let i=0;i<books.length;i++){kind=books[Q.seq++%books.length];if(armed||!['guns','missiles'].includes(kind))break;}}
 else if(!armed&&['guns','missiles'].includes(kind))kind='sonic';
 const P={_hc79:true,type:'hc79-'+kind,kind,serial:++HC79.serial,t:0,tell:kind==='guns'?(rank>=3?1.15:rank>=2?1.3:1.45):kind==='missiles'?1.25:kind==='sonic'?1.65:1.5,active:kind==='guns'?1.25:kind==='missiles'?1.5:kind==='sonic'?2.0:1.15,recover:1.05,next:0,sent:0,origin:{x:b.x,y:b.y},target:{x:clamp(player.x,camLeftX()+90,camRightX()-90),y:clamp(player.y,b.y+180,VH-45)},rank,locked:false};
 Q.action=P;b._r30.v18.attack=b._r30.attack=P;
 if(kind==='guns'){P.safeX=clamp(P.target.x+(Q.seq%2?88:-88),camLeftX()+100,camRightX()-100);P.safeY=P.target.y;P.safeHalf=48;P.laneOffset=70;}
 if(kind==='missiles'){
  for(const id of ['left','right'])if(hc79Alive(b,id)){
   const q=hc79Joint(b,id),src=Q.sources[id]={x:q.x,y:q.y,w:30,h:50,dead:false,_hc79Host:b,_hc79Part:id};
   const count=rank>=3?4:rank>=2?3:2;
   for(let i=0;i<count;i++)enemyLockOn(src,P.tell+i*.17,{fire:()=>{if(hc79Live(b)&&Q.action===P&&!src.dead&&hc79Alive(b,id))hc79Missile(b,id,P);}});
  }
 }
 combatWarningTick(b,'hc79-'+P.serial,0,P.tell,true);Snd.play('bossWeaponCharge',.65);hc79Log(b,'attack-tell',{kind,tell:P.tell,target:P.target,safeX:P.safeX,safeY:P.safeY,safeHalf:P.safeHalf});return P;
}
v18StartAttack=function(b){return hc79Live(b)?hc79Start(b):HC79.base.start.apply(this,arguments);};
function hc79Round(b,id,P){if(!hc79Alive(b,id))return;const Q=hc79State(b);Q.kick[id]=.14;const m=hc79Socket(b,id),a=hc79Angle(hc79Dir(Q.turn[id]+Math.PI/2)),speed=5.4;
 const q={kind:'mg',x:m.x,y:m.y,vx:Math.cos(a)*speed,vy:Math.sin(a)*speed,w:5,h:12,t:0,_ph:0,_v18Owner:b,_hc79Owner:b,_hc79Type:'gun',_weaponProof:true,_shootable:false};eBullets.push(q);Q.kick[id]=.14;Q.flash[id]=b._r30.clock;
 hc79Log(b,'gun-shot',{part:id,x:m.x,y:m.y,angle:a,safeX:P.safeX,safeY:P.safeY});
}
function hc79Missile(b,id,P){const Q=hc79State(b);Q.kick[id]=.14;const m=hc79Socket(b,id,'missile'),a=hc79Angle(hc79Dir(Q.turn[id]+Math.PI/2));
 eBullets.push({kind:'s1jungleMissile',x:m.x,y:m.y,vx:Math.cos(a)*2.3,vy:Math.sin(a)*2.3,ang:a,w:14,h:26,t:0,hp:1,homing:true,turn:.035,spd:2.3,_accel:.045,_maxspd:4.5,_shootable:true,_v18Owner:b,_hc79Owner:b,_hc79Type:'missile',_hc79Born:efxClock});
 Q.kick[id]=.14;Q.flash[id]=b._r30.clock;Snd.play('overlordRocket',.6);hc79Log(b,'missile-launch',{part:id,x:m.x,y:m.y,angle:a});
}
function hc79Wave(b,P){const x=b.x,y=b.y+94;eBullets.push({kind:'ovSonic',_ovSonicWave:true,_weaponProof:true,_shootable:false,_south:true,x,y,vx:0,vy:6.7,w:264,h:52,_waveW:264,_waveH:52,ang:Math.PI/2,t:0,_v18Owner:b,_hc79Owner:b,_hc79Type:'sonic'});Snd.play('coleSonicFull',.65);hc79Log(b,'red-sonic',{x,y});}
function hc79Finish(b,P){const Q=hc79State(b);for(const src of Object.values(Q.sources))src.dead=true;Q.action=null;b._r30.v18.attack=b._r30.attack=null;b._r30.v18.home={x:b.x,y:b.y};b._r30.cd=.5;j3State(b).attacks++;hc79Log(b,'recovery',{kind:P.kind});}
function hc79Move(b,Q,P,dt){const before=b.x,clock=Q.age;
 if(!P){const tx=worldWidth()/2+Math.sin(clock*.65)*112;b.x+=clamp(tx-b.x,-105*dt,105*dt);b.y+=clamp(174+Math.sin(clock*1.6)*10-b.y,-65*dt,65*dt);}
 else if(P.kind==='guns'){
  if(P.t<P.tell*.55){b.x+=clamp(P.origin.x+Math.sin(P.t*1.4)*10-b.x,-45*dt,45*dt);b.y+=clamp(174-b.y,-65*dt,65*dt);}
 }else if(P.kind==='missiles'){b.x+=clamp(P.origin.x+Math.sin(P.t*1.7)*18-b.x,-40*dt,40*dt);b.y+=clamp(174+Math.sin(clock*1.3)*8-b.y,-55*dt,55*dt);}
 else if(P.kind==='sonic'){b.x+=clamp(worldWidth()/2-b.x,-100*dt,100*dt);b.y+=clamp(174-b.y,-70*dt,70*dt);}
 else if(P.kind==='dash'){
  if(P.t<P.tell){b.x+=clamp(P.target.x-b.x,-160*dt,160*dt);b.y+=clamp(90-b.y,-110*dt,110*dt);}
  else if(P.t<P.tell+.68)b.y+=980*dt;
  else{if(!P.returned){P.returned=true;b.y=-170;hc79Log(b,'dash-return');}b.y+=clamp(174-b.y,-250*dt,250*dt);}
 }
 const target=P?0:clamp((b.x-before)/Math.max(.001,dt)*.10,-30,30);Q.bankAngle=lerp(Q.bankAngle,target,Math.min(1,dt*7));Q.bank=Math.round(clamp(Q.bankAngle/5+6,0,12));
 b._drawY=b.y;b.enter=false;b._noHit=b.y<-90||b.y>VH+90;
}
function hc79Tick(b,Q,P,dt){Q.age+=dt;Q.rotor=Math.floor(b._r30.clock*HC79_ART.rotorFps)%16;for(const id of ['left','right']){Q.kick[id]=Math.max(0,Q.kick[id]-dt);const src=Q.sources[id];if(src){Object.assign(src,hc79Joint(b,id));src.dead=!hc79Alive(b,id)||!P||P.kind!=='missiles';}}
 hc79Move(b,Q,P,dt);
 if(!P){b._r30.cd-=dt;if(Q.age>42&&V18.forms.filter(i=>j3State(b).hp[i]>0).length>1){j3Save(b);j3Morph(b,'home');return;}if(b._r30.cd<=0)hc79Start(b);return;}
 P.t+=dt;const active=P.t-P.tell;
 if(P.t<P.tell)combatWarningTick(b,'hc79-'+P.serial,P.t,P.tell);
 for(const id of ['left','right'])if(hc79Alive(b,id)){
  if(P.kind==='guns'){if(P.t<P.tell*.7)hc79Aim(b,id,P.safeX+(id==='left'?-1:1)*P.laneOffset,P.safeY,dt);else if(!P.locked)hc79Aim(b,id,P.safeX+(id==='left'?-1:1)*P.laneOffset,P.safeY,dt,true);}
  else if(P.kind==='missiles'){if(P.t<P.tell*.72)hc79Aim(b,id,player.x,player.y,dt);}
  else hc79Aim(b,id,b.x+(id==='left'?-104:104),VH+300,dt);
 }
 if(P.kind==='guns'&&P.t>=P.tell*.7&&!P.locked){P.locked=true;hc79Log(b,'guns-committed',{safeX:P.safeX,safeY:P.safeY});}
 if(active>=0&&!P.fired){P.fired=true;hc79Log(b,'attack-release',{kind:P.kind});}
 if(active>=0&&active<P.active){
  if(P.kind==='guns'&&active>=P.next){for(const id of ['left','right'])hc79Round(b,id,P);P.next+=P.rank>=3?.10:P.rank>=2?.12:.145;Snd.play('overlordGun',.42);}
  if(P.kind==='sonic'&&P.sent<(P.rank>=3?4:P.rank>=2?3:2)&&active>=P.sent*.55){hc79Wave(b,P);P.sent++;}
 }
 if(P.kind==='dash'&&active>=0&&active<.7&&!P.dashCue){P.dashCue=true;Snd.play('overlordWind',.7);}
 if(active>=P.active+P.recover)hc79Finish(b,P);
}
r30Tick=function(b,dt){if(!hc79Live(b)||rd30State(b).transition)return HC79.base.tick.apply(this,arguments);dt=clamp(dt||0,0,.05);j3Timers(b,dt);dr5TalkTick(b,dt);const N=b._r30.v18,Q=v17Clock(b);N.age+=dt;N.formClock+=dt;Q.t+=dt;Q.combat+=dt;Q.transition+=dt;weaponFeedbackLoop('overlordRotor',.32);hc79Tick(b,hc79State(b),N.attack?._hc79?N.attack:null,dt);};
target17Tick=function(b){if(hc79Own(b))return;return HC79.base.targetTick.apply(this,arguments);};
target17Draw=function(b){if(hc79Own(b))return;return HC79.base.targetDraw.apply(this,arguments);};
function hc79Geometry(b){const Q=hc79State(b),stamp=[b._r30.clock,b.x,b.y,Q.bank,Q.rotor,Q.turn.left,Q.turn.right,Q.kick.left>.09?1:Q.kick.left>0?2:0,Q.kick.right>.09?1:Q.kick.right>0?2:0,...b.parts.map(p=>+p.destroyed)].join(':');if(Q.rig?.stamp===stamp&&Q.rig.parts===b.parts)return Q.rig.rows;
 const rows=b.parts.filter(p=>!p.destroyed).map(p=>{const a=p.id==='core'?HC79_ART.banks['core_'+Q.bank][Q.rotor]:hc79Pod(b,p.id),pos=p.id==='core'?b:hc79Joint(b,p.id);return{_hc79:true,p,a,key:a.key,ax:pos.x,ay:pos.y,x:pos.x+a.target[0],y:pos.y+a.target[1],w:a.w,h:a.h,k:1,rot:0,alpha:1,anchor:[-a.offset[0],-a.offset[1]],spec:{role:p.id==='core'?'core':'weapon'},layer:p.id};});Q.rig={stamp,parts:b.parts,rows};return rows;
}
v18Rig=function(b){return hc79Own(b)?hc79Geometry(b):HC79.base.rig.apply(this,arguments);};
v19AtRect=function(v,x,y){if(!v._hc79)return HC79.base.at.apply(this,arguments);const a=v.a,xx=Math.floor(x-v.ax-a.offset[0]),yy=Math.floor(y-v.ay-a.offset[1]),row=a.spans[yy];if(!row)return false;for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return true;return false;};
function hc79Blit(a,x,y,hit=false,g=ctx){const key=hit?HC79_ART.pages[a.key].hitKey:a.key;if(!XART.rdy(key))return false;g.drawImage(XART.get(key),...a.rect,Math.round(x+a.offset[0]),Math.round(y+a.offset[1]),a.w,a.h);return true;}
function hc79Bank(name,f,x,y,g=ctx){const rows=HC79_ART.banks[name];return hc79Blit(rows[((f|0)%rows.length+rows.length)%rows.length],x,y,false,g);}
function hc79Body(b,g=ctx){for(const v of hc79Geometry(b))hc79Blit(v.a,v.ax,v.ay,Math.max(b.flash||0,v.p.flash||0)>.025&&Math.floor(efxClock*30)%2===0,g);HC79.draws.body=(HC79.draws.body||0)+1;}
v19Body=function(b){return hc79Own(b)?hc79Body(b):HC79.base.body.apply(this,arguments);};
rd30Plate=function(b){if(!hc79Own(b))return HC79.base.plate.apply(this,arguments);const c=document.createElement('canvas');c.width=c.height=768;const g=c.getContext('2d');for(const v of hc79Geometry(b))hc79Blit(v.a,384+v.ax-b.x,384+v.ay-b.y,false,g);return c;};
function hc79Warnings(b){const Q=hc79State(b),P=Q.action;if(!P||P.t>=P.tell)return;const u=P.t/P.tell,col=u<1/3?'green':u<2/3?'yellow':'red';
 if(P.kind==='guns'||P.kind==='missiles'){for(const id of ['left','right'])if(hc79Alive(b,id)){const m=hc79Socket(b,id,P.kind==='guns'?'gun':'missile');rd72Line('warning_'+col,rd72Dir(hc79Angle(hc79Dir(Q.turn[id]+Math.PI/2))),m.x,m.y);}}
 else if(P.kind==='sonic')for(const dx of [-115,-58,0,58,115])rd72Line('warning_'+col,rd72Dir(Math.PI/2),b.x+dx,b.y+94);
 else if(P.kind==='dash')rd72Line('warning_'+col,rd72Dir(Math.PI/2),b.x,b.y+90);
 rd72Blit('asterisk',Math.floor(P.t*10)%8,b.x,Math.max(viewTopY()+32,b.y-126));
}
v18Warnings=function(b){if(hc79Own(b))return hc79Warnings(b);return HC79.base.warnings.apply(this,arguments);};
r30DrawBoss=function(b){if(!hc79Live(b))return HC79.base.draw.apply(this,arguments);hc79Body(b);hc79Warnings(b);const Q=hc79State(b);for(const id of ['left','right'])if(hc79Alive(b,id)&&b._r30.clock-Q.flash[id]<.14){const missile=Q.action?.kind==='missiles',m=hc79Socket(b,id,missile?'missile':'gun'),d=hc79Dir(Q.turn[id]+Math.PI/2),f=Math.min(3,Math.floor((b._r30.clock-Q.flash[id])/.14*4));if(missile)rd72Blit('missile_muzzle',f*64+rd72Dir(hc79Angle(d)),m.x,m.y);else hc79Bank('muzzle',f*64+d,m.x,m.y);}};
target17BossContact=function(b,x,y){if(!hc79Own(b))return HC79.base.contact.apply(this,arguments);return hc79Live(b)&&!b._noHit&&hc79Geometry(b).some(v=>v19AtRect(v,x,y));};
function hc79Rupture(b,p,base,args){if(!hc79Own(b))return base.apply(null,args);const v=hc79Geometry(b).find(v=>v.p===p);if(!v||p._hc79Broken)return;p._hc79Broken=true;for(const dx of [-v.w*.25,0,v.w*.25])explode(v.x+dx,v.y,32,'purple');const src=hc79State(b).sources[p.id];if(src){src.dead=true;for(const L of playerLocks)if(L.src===src)for(const sh of L.launches)sh.done=true;}hc79Log(b,'pod-destroyed',{part:p.id,x:v.x,y:v.y});}
v18Rupture=function(b,p){return hc79Rupture(b,p,HC79.base.rupture,arguments);};
v19Rupture=function(b,p){return hc79Rupture(b,p,HC79.base.donor,arguments);};
v18Clear=function(b){hc79Cancel(b);return HC79.base.clear.apply(this,arguments);};
function hc79Projectile(q){if(q?._hc79Type==='gun'){hc79Bank('round',Math.min(5,Math.floor((q.t||0)/.024))*64+hc79Dir(Math.atan2(q.vy,q.vx)),q.x,q.y);return true;}if(q?._hc79Type==='sonic'){hc79Bank('sonic',Math.floor((q.t||0)*30)%12,q.x,q.y);return true;}if(q?._hc79Type==='missile'){rd72Blit('missile',(Math.floor((efxClock-q._hc79Born)*24)%4)*64+rd72Dir(Math.atan2(q.vy,q.vx)),q.x,q.y);return true;}return false;}
drawCombatFinalProjectile=function(q){return hc79Projectile(q)||HC79.base.projectile.apply(this,arguments);};
ovSonicProjectileDraw=function(q){return hc79Projectile(q)||HC79.base.sonic.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._hc79Owner?(q._hc79Type==='missile'):HC79.base.intercept.apply(this,arguments);};
// Opaque ground and stored-alpha near canopy retain distinct world-space rates.
ad20Scene=function(b,theme,wire=false){if(theme!=='jungle')return HC79.base.scene.apply(this,arguments);const t=b._r30.clock||0,draw=(name,rate)=>{const a=HC79_ART.arena[name];if(!XART.rdy(a.key))return;const y=Math.floor(t*rate)%a.h;for(let n=-1;n<2;n++)ctx.drawImage(XART.get(a.key),0,y+n*a.h);HC79.draws[name]=(HC79.draws[name]||0)+1;};draw(wire?'wire':'ground',12);if(!wire)draw('canopy',28);return true;};
globalThis.BOF_DRACODIA_HELICOPTER_1030=HC79;
