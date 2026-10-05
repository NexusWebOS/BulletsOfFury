"use strict";
/* Mike, October 3: restore the stored Herald, regenerate at higher quality,
   and make it modular. This named exception supersedes the old whole-plate rule. */
XART._src[HD1003_ART.key]=HD1003_ART.path;
SUBBOSS[8]={kind:'heralddeath',at:ALTBOSS[8].at,afterScroll:ALTBOSS[8].afterScroll};
const HD1003_BASE={begin:beginStage,spawn:spawnSubBoss__inner,move:shipBossManoeuvre,
 draw:heraldDeathDraw,update:updateSubBoss,hit:hitSubBoss,at:subBossHitPart,
 solid:subBossSolidAt,targets:retinaBossTargets,mount:shipBossMount};
function hd1003Owns(b){return !!b?._hd1003;}
function hd1003Warm(){
 XART.rdy(HD1003_ART.key);s81003WarningWarm();
 for(const kind of ['primary','special'])for(let i=0;i<6;i++)XART.rdy('nhd_'+kind+'_projectile_'+i);
}
beginStage=function(n){const r=HD1003_BASE.begin.apply(this,arguments);if(n===8)hd1003Warm();return r;};
spawnSubBoss__inner=function(kind){
 const r=HD1003_BASE.spawn.apply(this,arguments);
 if(kind==='heralddeath'&&subBoss?._ship===kind)hd1003Init(subBoss);
 return r;
};
function hd1003Init(b){
 if(b._hd1003)return b._hd1003;hd1003Warm();
 b.w=340;b.h=240;b.ty=157;b.fireCd=999;b._be=null;b._sba=null;
 const H=b._hd1003={clock:0,age:0,mode:'rest',seq:0,history:[],parts:[],debris:[],shots:0,deadBeats:0};
 for(const [id,spec] of Object.entries(HD1003_ART.parts))H.parts.push({id,spec,hp:Math.ceil(b.maxhp*(id.startsWith('wing')?.10:.13)),maxhp:Math.ceil(b.maxhp*(id.startsWith('wing')?.10:.13)),dead:false,flash:0,kick:0});
 return H;
}
function hd1003Part(b,id){return b._hd1003.parts.find(p=>p.id===id);}
function hd1003Live(b,p){return !b.dead&&!p.dead&&(p.id==='core'||p.id==='head'||p.hp>0);}
function hd1003Pose(b,p){
 const H=b._hd1003,s=p.spec,side=p.id.endsWith('L')?-1:1;
 let angle=0;
 if(p.id.startsWith('wing'))angle=side*(H.mode==='rest'?.08*Math.sin(H.clock*2.8):.16);
 if(p.id.startsWith('gun'))angle=H.target?clamp(Math.atan2(H.target.y-(b.y+s.attach[1]),H.target.x-(b.x+s.attach[0]))-Math.PI/2,-.42,.42):side*.04;
 if(p.id==='head')angle=H.mode==='rest'?.025*Math.sin(H.clock*1.7):0;
 const pose={x:b.x+s.attach[0],y:b.y+s.attach[1]-(p.kick||0),a:angle,s:s.scale};
 return pose;
}
function hd1003Point(P,p,v){const dx=(v[0]-p.spec.pivot[0])*P.s,dy=(v[1]-p.spec.pivot[1])*P.s;return{x:P.x+dx*Math.cos(P.a)-dy*Math.sin(P.a),y:P.y+dx*Math.sin(P.a)+dy*Math.cos(P.a)};}
function hd1003Center(b,p){return hd1003Point(hd1003Pose(b,p),p,p.spec.hit);}
function hd1003Muzzle(b,id){const p=hd1003Part(b,id);return hd1003Point(hd1003Pose(b,p),p,p.spec.muzzle||p.spec.hit);}
shipBossMount=function(b,slot){if(hd1003Owns(b))return hd1003Muzzle(b,slot==='L'?'gunL':slot==='R'?'gunR':'head');return HD1003_BASE.mount.apply(this,arguments);};
function hd1003At(b,x,y){
 if(!b||b.dead||b.enter||!Number.isFinite(x+y))return null;
 // Frontmost visible part wins; gaps and detached modules never catch pellets.
 for(const p of [...b._hd1003.parts].sort((a,b)=>b.spec.z-a.spec.z)){
  if(!hd1003Live(b,p))continue;const P=hd1003Pose(b,p),dx=x-P.x,dy=y-P.y;
  const lx=(dx*Math.cos(P.a)+dy*Math.sin(P.a))/P.s+p.spec.pivot[0],ly=(-dx*Math.sin(P.a)+dy*Math.cos(P.a))/P.s+p.spec.pivot[1],h=p.spec.hit;
  if(((lx-h[0])/h[2])**2+((ly-h[1])/h[3])**2<=1)return p.id;
 }return null;
}
subBossHitPart=function(x,y){return hd1003Owns(subBoss)?hd1003At(subBoss,x,y):HD1003_BASE.at.apply(this,arguments);};
subBossSolidAt=function(x,y){return hd1003Owns(subBoss)?hd1003At(subBoss,x,y)!==null:HD1003_BASE.solid.apply(this,arguments);};
function hd1003Break(b,p){
 if(p.dead)return;const H=b._hd1003,P=hd1003Pose(b,p),q=hd1003Center(b,p);p.dead=true;p.hp=0;
 H.debris.push({p,P:{...P},t:0,vx:p.id.endsWith('L')?-90:90,vy:38,spin:p.id.endsWith('L')?-1.3:1.3});
 S81003.beams=S81003.beams.filter(q=>q.owner!==b||q.heraldPart!==p.id);
 explode(q.x,q.y,p.id.startsWith('wing')?68:50,'orange');r30Sound('combatModule0927');shake=Math.max(shake,4);
}
function hd1003Hit(b,dmg,x,y,id){
 if(b!==subBoss||b.dead||b.enter||!Number.isFinite(dmg)||dmg<=0)return;
 const partId=id||(Number.isFinite(x+y)?hd1003At(b,x,y):'core');if(!partId)return;
 const p=hd1003Part(b,partId);if(!p||!hd1003Live(b,p))return;
 const before=b.hp,flash=b.flash;
 // Native damage keeps elemental reactions, stats, achievements and defeat rewards.
 HD1003_BASE.hit.call(this,dmg*(partId==='head'?1.2:1),x,y);
 const dealt=Math.max(0,before-b.hp);b.flash=flash;p.flash=.18;
 if(partId!=='core'&&partId!=='head'){p.hp=Math.max(0,p.hp-dealt);if(p.hp<=0)hd1003Break(b,p);}
 if(b.dead){b._hd1003.mode='dead';S81003.beams=S81003.beams.filter(q=>q.owner!==b);groundTargetingCancel(b);}
}
hitSubBoss=function(dmg,hx,hy){if(hd1003Owns(subBoss))return hd1003Hit(subBoss,dmg,hx,hy);return HD1003_BASE.hit.apply(this,arguments);};
retinaBossTargets=function(b){
 if(!hd1003Owns(b))return HD1003_BASE.targets.apply(this,arguments);
 if(b.dead||b.enter)return [];
 return b._hd1003.parts.filter(p=>hd1003Live(b,p)).map(p=>retinaDynamicPiece(b,'herald-'+p.id,'Herald module',()=>({
  ...hd1003Center(b,p),hp:p.id==='core'||p.id==='head'?b.hp:p.hp,dead:!hd1003Live(b,p)}),
  (d,q)=>{const P=hd1003Center(b,p);hd1003Hit(b,d,P.x,P.y,p.id);},p.spec.hit[2]*p.spec.scale*1.7,p.spec.hit[3]*p.spec.scale*1.7));
};
function hd1003Tell(b){
 const H=b._hd1003,rank=diffKey==='furious'?2:diffKey==='hard'?1:0;
 const book=diffKey==='easy'?['skulls','salvo']:['skulls','lances','salvo'];H.attack=book[H.seq++%book.length];
 H.mode='tell';H.age=0;H.shots=0;H.rank=rank;H.warm=diffKey==='easy'?1.5:[1.22,1.08,.96][rank];
 const T=targetShip(b.x,b.y);H.target={x:T.x,y:T.y};H.lanes=[];
 for(const p of H.parts)p.kick=0;
 let ids=H.attack==='lances'?['wingL','wingR']:H.attack==='skulls'?['gunL','gunR']:['head'];
 ids=ids.filter(id=>hd1003Live(b,hd1003Part(b,id)));
 if(!ids.length){H.attack='salvo';ids=['head'];}
 for(const id of ids){const P=hd1003Muzzle(b,id),side=id.endsWith('L')?-1:id.endsWith('R')?1:0;
  const tx=H.target.x+(H.attack==='lances'?side*42:0),ty=H.target.y;
  H.lanes.push({...s81003Lane(P.x,P.y,tx,ty,H.attack==='lances'?15:44),id,tx,ty});
 }
 H.history.push(H.attack);if(H.history.length>30)H.history.shift();r30Sound('bossWeaponCharge');
}
function hd1003Shot(b,L,a,special){
 const p=hd1003Part(b,L.id);if(!hd1003Live(b,p))return;
 const P=hd1003Muzzle(b,L.id),q=eShootT(P.x,P.y,a,2.8+b._hd1003.rank*.35,'s8pair',{w:16,h:16,owner:b,silent:true});
 if(q&&!q.dead){q._heraldProjectile=special?'special':'primary';q._noArsenal=true;q._heraldOwner1003=b;q._heraldPart1003=L.id;p.kick=3;}
}
function hd1003Tick(b,dt){
 const H=b._hd1003;H.clock+=dt;H.age+=dt;b.fireCd=999;b._sba=null;b._drawY=b.y;
 if(H.mode==='rest'){
  const aliveWings=H.parts.filter(p=>p.id.startsWith('wing')&&!p.dead).length;
  const tx=clamp(worldWidth()/2+Math.sin(H.clock*.65)*aliveWings*35,camLeftX()+165,camRightX()-165);
  b.x+=clamp(tx-b.x,-48*dt,48*dt);b.y+=clamp(b.ty-b.y,-45*dt,45*dt);
  if(H.age>(H.seq?1.05:1.6))hd1003Tell(b);
 }else if(H.mode==='tell'){
  combatWarningTick(b,'herald-'+H.seq,H.age,H.warm);
  if(H.age>=H.warm){H.mode='fire';H.age=0;r30Sound(H.attack==='lances'?'combatBeam0927':'bossfireVileexistence');
   if(H.attack==='lances')for(const L of H.lanes)if(hd1003Live(b,hd1003Part(b,L.id))){const q=s81003Beam(b,L,'alien',.62);q.heraldPart=L.id;}
  }
 }else if(H.mode==='fire'){
  if(H.attack==='skulls'&&H.shots===0){for(const L of H.lanes){const a=Math.atan2(L.ey-L.y,L.ex-L.x),n=3+H.rank*2;for(let i=0;i<n;i++)hd1003Shot(b,L,a+(i-(n-1)/2)*.12,false);}H.shots++;}
  if(H.attack==='salvo'&&H.shots<3+H.rank&&H.age>=H.shots*.2){const L=H.lanes[0];hd1003Shot(b,L,Math.atan2(L.ey-L.y,L.ex-L.x)+(H.shots%2?.12:-.12),true);H.shots++;r30Sound('combatOrb0927');}
  if(H.age>1.05){H.mode='rest';H.age=0;}
 }
 b._drawY=b.y;return true;
}
shipBossManoeuvre=function(b,dt){if(hd1003Owns(b)&&!b.dead&&!b.enter)return hd1003Tick(b,Math.min(.05,dt));return HD1003_BASE.move.apply(this,arguments);};
function hd1003Blit(p,P,flash=0,alpha=1){
 const key=HD1003_ART.key;if(!XART.rdy(key))return false;const s=p.spec,r=s.rect;
 ctx.save();ctx.translate(P.x,P.y);ctx.rotate(P.a);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(key),...r,-s.pivot[0]*P.s,-s.pivot[1]*P.s,r[2]*P.s,r[3]*P.s);
 if(flash>0){const im=xartTint(key,'#ffffff',1);if(im){ctx.globalAlpha*=Math.min(1,flash*9);ctx.drawImage(im,...r,-s.pivot[0]*P.s,-s.pivot[1]*P.s,r[2]*P.s,r[3]*P.s);}}
 ctx.restore();return true;
}
heraldDeathDraw=function(b){
 if(!hd1003Owns(b))return HD1003_BASE.draw.apply(this,arguments);
 if(!XART.rdy(HD1003_ART.key))return HD1003_BASE.draw.apply(this,arguments);
 const H=b._hd1003;
 if(!b.dead&&H.mode==='tell'){
  for(const L of H.lanes)if(hd1003Live(b,hd1003Part(b,L.id)))s81003Fov(L,H.age/H.warm,H.attack==='lances',b);
  combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,progress:H.age/H.warm,alertOnly:true,alertX:b.x,alertY:48});
 }
 for(const d of H.debris)hd1003Blit(d.p,d.P,0,Math.max(0,1-d.t/1.2));
 for(const p of [...H.parts].sort((a,b)=>a.spec.z-b.spec.z))if(!p.dead&&(!b.dead||b.dying<1.05))hd1003Blit(p,hd1003Pose(b,p),Math.max(p.flash,b.flash||0));
 return true;
};
updateSubBoss=function(dt){
 const b=subBoss,H=b?._hd1003;
 if(H){
  for(const p of H.parts){p.flash=Math.max(0,p.flash-dt);p.kick=Math.max(0,p.kick-dt*22);}
  for(const d of H.debris){d.t+=dt;d.P.x+=d.vx*dt;d.P.y+=d.vy*dt;d.vy+=80*dt;d.P.a+=d.spin*dt;}H.debris=H.debris.filter(d=>d.t<1.2);
  if(b.dead){
   const ids=['gunL','gunR','wingL','wingR','head'];
   for(let i=0;i<ids.length;i++)if(b.dying+dt>=.12+i*.16&&!(H.deadBeats&(1<<i))){H.deadBeats|=1<<i;hd1003Break(b,hd1003Part(b,ids[i]));}
   if(b.dying+dt>=1.0&&!H.finalBlast){H.finalBlast=true;unitDeathFX(b,'mini','red');r30Sound('expBig');shake=Math.max(shake,10);}
  }
 }
 return HD1003_BASE.update.apply(this,arguments);
};
