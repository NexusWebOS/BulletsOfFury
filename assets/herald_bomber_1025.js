'use strict';
/* Mike Oct25: red round chaos, Phoenix-style corner flights and claw bombers.
   The native Herald parts still own damage, hit masks, flashes and breakup. */
const HB25={events:[],base:{load:stageLoadBegin,bg:drawBG,tell:hd1003Tell,tick:hd1003Tick,pose:hd1003Pose,blit:hd1003Blit,
 muzzle:hd1003Muzzle,shot:hd1003Shot,draw:heraldDeathDraw,projectile:drawCombatFinalProjectile,update:updatePlay,
 intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,rules:s3kOrdnanceRules},dim:.46};
XART._src[HB25_ART.key]=HB25_ART.path;
stageLoadBegin=function(n,keys){if(n===8)for(const k of ['bossfireVileexistence','combatOrb0927','bossWeaponCharge','jetDash'])Snd.prepare(k);
 return HB25.base.load.call(this,n,[...(keys||[]),...(n===8?[HB25_ART.key]:[])]);};
// Lighting belongs to the scenery pass, before actors, shots and the HUD.
drawBG=function(dt){const r=HB25.base.bg.apply(this,arguments);if(run.stage===3){ctx.save();ctx.globalCompositeOperation='source-over';ctx.globalAlpha=HB25.dim;ctx.fillStyle='#000';ctx.fillRect(camLeftX(),viewTopY(),viewW(),viewH());ctx.restore();}return r;};
function hb25Log(b,event,data={}){HB25.events.push({event,time:efxClock,mode:b._hd1003?._hb25?.kind,...data});if(HB25.events.length>700)HB25.events.shift();}
function hb25Claws(b){return ['gunL','gunR'].filter(id=>hd1003Live(b,hd1003Part(b,id)));}
hd1003Muzzle=function(b,id){if(b?._hd1003&&id.startsWith('gun')){const p=hd1003Part(b,id);return hd1003Point(hd1003Pose(b,p),p,[id==='gunL'?95:113,542]);}return HB25.base.muzzle.apply(this,arguments);};
function hb25Tag(q,b,id,bomb=null){if(!q||q.dead)return q;
 Object.assign(q,{_hb25Chaos:true,_hb25Born:efxClock,_heraldOwner1003:b,_heraldPart1003:id,_noArsenal:true,_boss:true,
  _weaponProof:true,_shootable:false,_s3kOriginalProof:false,homing:false,w:10,h:10});
 delete q.hp;delete q._hp22Feather;delete q._heraldProjectile;if(bomb)q._hb25Bomb=bomb;return q;
}
hd1003Shot=function(b,L,a){const first=eBullets.length,r=HB25.base.shot.apply(this,arguments);for(let i=first;i<eBullets.length;i++)hb25Tag(eBullets[i],b,L.id);if(eBullets.length>first)hb25Flash(b,L.id,a);return r;};
function hb25Flash(b,id,angle=Math.PI/2){const p=hd1003Muzzle(b,id);wm26Emit(b,p.x,p.y,angle,'void','#ff303c',{size:48,life:.20,follow:()=>!b.dead&&hd1003Live(b,hd1003Part(b,id))?hd1003Muzzle(b,id):null});
 hb25Log(b,'claw-flash',{id,x:p.x,y:p.y,angle});
}
function hb25Shot(b,id,p,a,speed,bomb=null){const q=eShootT(p.x,p.y,a,speed,'s8pair',{owner:b,w:10,h:10,noMuzzle:true,silent:true});hb25Tag(q,b,id,bomb);return q;}
enemyOrdnanceCanIntercept=function(q){return !q?._hb25Chaos&&HB25.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._hb25Chaos?null:HB25.base.element.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._hb25Chaos){q._weaponProof=true;q._shootable=false;delete q.hp;return;}return HB25.base.rules.apply(this,arguments);};
drawCombatFinalProjectile=function(q){if(!q?._hb25Chaos)return HB25.base.projectile.apply(this,arguments);
 if(!XART.rdy(HB25_ART.key))return true;const a=HB25_ART,f=Math.floor((efxClock-q._hb25Born)*a.fps)%a.frames,size=q._hb25Bomb?38:q._hb25Drop?32:28;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(q.x,q.y);ctx.rotate((efxClock-q._hb25Born)*1.5);ctx.drawImage(XART.get(a.key),...a.cells[f],-size/2,-size/2,size,size);ctx.restore();return true;
};
function hb25Corner(b,Q){const side=(Q.pass+Q.side)%2,l=camLeftX(),r=camRightX(),top=viewTopY(),bottom=VH;
 if(Q.kind==='bomber'){const from={x:side?r+150:l-150,y:top+138},to={x:side?l-150:r+150,y:top+138};return{from,to,a:side?Math.PI:0};}
 const from={x:side?r+110:l-110,y:top-100},to={x:side?l-110:r+110,y:bottom+110};return{from,to,a:Math.atan2(to.y-from.y,to.x-from.x)};
}
function hb25Turn(a,b,u){return a+Math.atan2(Math.sin(b-a),Math.cos(b-a))*u;}
function hb25Duration(Q){const corner=[1.65,1.5,1.36,1.25][Q.rank];return Q.kind==='bomber'?
 corner*Math.hypot(Q.path.to.x-Q.path.from.x,Q.path.to.y-Q.path.from.y)/Math.hypot(viewW()+220,VH-viewTopY()+210):corner;}
function hb25Phase(b,phase){const Q=b._hd1003._hb25;Q.phase=phase;Q.t=0;Q.from={x:b.x,y:b.y};
 if(phase==='recede'){Q.path=hb25Corner(b,Q);Q.to=Q.path.from;Q.startScale=Q.scale;Q.startAngle=Q.angle;}
 if(phase==='tell'){Q.hit=new Set();Q.pending=null;Q.release=0;Q.drops=0;Q.duration=hb25Duration(Q);Q.vx=(Q.path.to.x-Q.path.from.x)/Q.duration;
  Q.scale=Q.kind==='bomber'?.70:.34;Q.angle=Q.path.a+Math.PI/2;if(Q.kind==='bomber')hb25BombPlan(b,Q);combatAudio0927(b,'bossWeaponCharge',.8);}
 if(phase==='strike'){Q.previous={};combatAudio0927(b,'jetDash',1);}
 if(phase==='return'){Q.startScale=Q.scale;Q.startAngle=Q.angle;Q.to={x:camLeftX()+viewW()/2,y:viewTopY()+155};Q.pending=null;}
 hb25Log(b,'flight-phase',{phase,kind:Q.kind,pass:Q.pass,from:Q.from,to:Q.path.to,duration:Q.duration,speed:Q.duration?Math.hypot(Q.path.to.x-Q.path.from.x,Q.path.to.y-Q.path.from.y)/Q.duration:null});
}
function hb25Flight(b,kind){const H=b._hd1003;H.seq++;H.mode='hb25-flight';H.age=H.attackAge=0;H.lanes=[];H.flashes=[];H.target=null;H._hp22=null;H._hd19=null;
 if(b._hc1007)b._hc1007.cross=null;S81003.beams=S81003.beams.filter(q=>q.owner!==b);
 const rank=bh25Rank();H._hb25={kind,rank,t:0,pass:0,side:H.seq%2,total:rank>=2&&['wingL','wingR'].every(id=>hd1003Live(b,hd1003Part(b,id)))?2:1,
  scale:1,angle:0,wing:0,escapeX:clamp(player.x,camLeftX()+65,camRightX()-65),warm:[1.5,1.3,1.15,1.05][rank]};
 b._s4MiniSafe=true;H.history.push('chaos-'+kind);if(H.history.length>30)H.history.shift();hb25Phase(b,'recede');
}
hd1003Tell=function(b){if(!b?._hd1003||b!==subBoss)return HB25.base.tell.apply(this,arguments);const H=b._hd1003;
 if(hd19Disarmed(b))return hd19Start(b,H.seq%2?'core-lance':'core-fury');
 const book=['barrage','swoop','bomber','cannon-rake','swoop','bomber'],kind=book[(H.hb25Turn||0)%book.length];H.hb25Turn=(H.hb25Turn||0)+1;
 if(kind==='barrage'){H.seq++;H.mode='bh25';H.age=H.attackAge=0;H.lanes=[];H._hp22=null;H._hd19=null;delete H._hb25;if(b._hc1007)b._hc1007.cross=null;
  if(bh25Start(b,'herald',()=>{H.mode='rest';H.age=H.attackAge=0;}))return;}
 if(kind==='cannon-rake')return hd19Start(b,hb25Claws(b).length?'cannon-rake':'core-fury');
 if(kind==='bomber'&&!hb25Claws(b).length)return hd19Start(b,'core-fury');
 return hb25Flight(b,kind==='barrage'?'swoop':kind);
};
// Commit the complete drop carpet during the pass warning. Individual bombs no
// longer hold a fast-moving aircraft in a slow warn/drop/wait loop.
function hb25BombPlan(b,Q){Q.plan=[];Q.interval=[.115,.10,.085,.070][Q.rank];const ids=hb25Claws(b);
 for(let wave=0,time=0;time<=Q.duration;wave++,time=wave*Q.interval)for(let i=0;i<ids.length;i++){
  const id=ids[i],m=hd1003Muzzle(b,id),x=Q.path.from.x+Q.vx*time+(m.x-b.x);if(x<camLeftX()+45||x>camRightX()-45)continue;
  const target={x,y:clamp(viewTopY()+235+((wave+i)%2)*56,viewTopY()+230,VH-130)},P={id,time,wave,target,from:{x,y:m.y},burst:wave%3===0&&i===wave%ids.length,seed:Q.pass*100+wave*2+i};
  if(!P.burst&&Math.abs(x-Q.escapeX)<52)continue;
  Q.plan.push(P);hb25Log(b,'bomb-tell',{id,target,warm:Q.warm,release:time,burst:P.burst,pass:Q.pass});
 }
}
function hb25BombDrop(b,Q,P){if(!hd1003Live(b,hd1003Part(b,P.id))||eBullets.filter(q=>q._hb25Chaos&&!q.dead).length>=128)return;
 const m=hd1003Muzzle(b,P.id);if(!P.burst&&Math.abs(m.x-Q.escapeX)<44)return;
 const flight=.68,dx=P.target.x-m.x,dy=P.target.y-m.y,a=P.burst?Math.atan2(dy,dx):Math.PI/2,
  bomb=P.burst?{at:efxClock+flight,target:P.target,escapeX:Q.escapeX,rank:Q.rank,seed:P.seed}:null,
  q=hb25Shot(b,P.id,m,a,P.burst?Math.hypot(dx,dy)/(flight*60):2.9+Q.rank*.25,bomb);
 if(q){q._hb25Drop=true;if(bomb){q.vx=dx/(flight*60);q.vy=dy/(flight*60);q.spd=Math.hypot(q.vx,q.vy);}Q.drops++;
  hb25Flash(b,P.id,a);combatAudio0927(b,'bossfireVileexistence',.13);hb25Log(b,'bomb-drop',{id:P.id,x:m.x,y:m.y,target:P.target,vx:q.vx,vy:q.vy,burst:P.burst,wave:P.wave,pass:Q.pass});}
}
function hb25Contact(b,Q){if(Q.kind!=='swoop')return;const ids=[...hb25Claws(b),'head'];for(const id of ids){const p=hd1003Part(b,id);if(!hd1003Live(b,p))continue;
 const at=id==='head'?hd1003Center(b,p):hd1003Muzzle(b,id),last=Q.previous[id]||at;
 for(const seat of seatList())withSeat(seat,()=>{if(!Q.hit.has(seat)&&!player.dead&&s81003Distance(player.x,player.y,{x:last.x,y:last.y,ex:at.x,ey:at.y})<(id==='head'?21:24)){Q.hit.add(seat);playerHit('Herald corner talon swoop');}});Q.previous[id]=at;
}}
hd1003Tick=function(b,dt){const H=b._hd1003,Q=H?._hb25;if(!Q||H.mode!=='hb25-flight')return HB25.base.tick.apply(this,arguments);
 if(b.dead)return true;H.clock+=dt;H.age+=dt;H.attackAge+=dt;Q.t+=dt;b.fireCd=999;b._sba=null;b._s4MiniSafe=true;
 if(Q.phase==='recede'){const u=clamp(Q.t/1,0,1),k=u*u*(3-2*u);b.x=lerp(Q.from.x,Q.to.x,k);b.y=lerp(Q.from.y,Q.to.y,k)-Math.sin(u*Math.PI)*65;Q.scale=lerp(Q.startScale,.34,k);Q.angle=hb25Turn(Q.startAngle,Q.path.a+Math.PI/2,k);Q.wing=.22;
  if(u>=1)hb25Phase(b,'tell');
 }else if(Q.phase==='tell'){Q.scale=Q.kind==='bomber'?.70:.34;Q.angle=Q.path.a+Math.PI/2;combatWarningTick(b,'hb25-flight-'+H.seq+'-'+Q.pass,Q.t,Q.warm);if(Q.t>=Q.warm)hb25Phase(b,'strike');
 }else if(Q.phase==='strike'){const u=clamp(Q.t/Q.duration,0,1);b.x=lerp(Q.path.from.x,Q.path.to.x,u);b.y=lerp(Q.path.from.y,Q.path.to.y,u);Q.angle=Q.path.a+Math.PI/2;
  Q.scale=Q.kind==='bomber'?.70:.36+Math.sin(u*Math.PI)*.64;Q.wing=Q.kind==='bomber'?.12*Math.sin(H.clock*8):-.36*Math.sin(u*Math.PI);
  if(Q.kind==='bomber'){
   while(Q.release<Q.plan.length&&Q.t>=Q.plan[Q.release].time)hb25BombDrop(b,Q,Q.plan[Q.release++]);
  }else if(u>.06&&u<.94)hb25Contact(b,Q);
  if(u>=1){Q.pass++;Q.pending=null;if(Q.pass<Q.total)hb25Phase(b,'recede');else hb25Phase(b,'return');}
 }else{const u=clamp(Q.t/1.15,0,1),k=u*u*(3-2*u);b.x=lerp(Q.from.x,Q.to.x,k);b.y=lerp(Q.from.y,Q.to.y,k);Q.scale=lerp(Q.startScale,1,k);Q.angle=hb25Turn(Q.startAngle,0,k);Q.wing=-.08;
  if(u>=1){delete H._hb25;H.mode='rest';H.age=.2;H.lanes=[];b._s4MiniSafe=false;hb25Log(b,'flight-complete',{kind:Q.kind,passes:Q.pass});}}
 b._drawY=b.y;return true;
};
hd1003Pose=function(b,p){const P=HB25.base.pose.apply(this,arguments),Q=b?._hd1003?._hb25;if(!Q)return P;const s=Q.scale,c=Math.cos(Q.angle),sn=Math.sin(Q.angle),dx=(P.x-b.x)*s,dy=(P.y-b.y)*s;
 let a=P.a+Q.angle;if(p.id.startsWith('wing'))a+=(p.id.endsWith('L')?-1:1)*Q.wing;if(p.id.startsWith('gun')&&Q.kind==='bomber')a-=Q.angle*.60;
 return{...P,x:b.x+dx*c-dy*sn,y:b.y+dx*sn+dy*c,a,s:P.s*s};
};
hd1003Blit=function(p,P,flash=0,alpha=1){const H=subBoss?._hd1003,Q=H?._hb25,B=CP22_ART.herald[p.id];if(!Q||!B||p.dead||!XART.rdy(B.key))return HB25.base.blit.apply(this,arguments);
 const f=Math.floor(H.clock*(Q.phase==='strike'?20:12))%B.frames,c=B.cells[f],s=P.s/B.sourceScale;
 ctx.save();ctx.translate(P.x,P.y);ctx.rotate(P.a);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(B.key),...c,-B.pivot[0]*s,-B.pivot[1]*s,B.w*s,B.h*s);
 if(flash>0){const im=xartTint(B.key,'#ffffff',1);if(im){ctx.globalAlpha*=Math.min(1,flash*9);ctx.drawImage(im,...c,-B.pivot[0]*s,-B.pivot[1]*s,B.w*s,B.h*s);}}ctx.restore();return true;
};
heraldDeathDraw=function(b){const Q=b?._hd1003?._hb25;if(Q&&!b.dead){
 if(Q.phase==='tell')combatWarningDraw(b,{...Q.path.from,ex:Q.path.to.x,ey:Q.path.to.y,width:Q.kind==='swoop'?164:80,progress:Q.t/Q.warm,fieldOnly:true,alpha:.40});
 if(Q.kind==='bomber'&&Q.phase==='tell')for(const P of Q.plan)if(hd1003Live(b,hd1003Part(b,P.id))){combatWarningDraw(b,{...P.from,ex:P.target.x,ey:P.burst?P.target.y:VH,width:P.burst?14:28,progress:Q.t/Q.warm,fieldOnly:true,alpha:.24});if(P.burst)groundTargetReticleDraw(P.target.x,P.target.y,60,Q.t/Q.warm,.70);}
 }if(!b.dead)for(const q of eBullets)if(q._heraldOwner1003===b&&q._hb25Bomb&&!q.dead){const B=q._hb25Bomb,at=B.target,u=clamp((efxClock-q._hb25Born)/(B.at-q._hb25Born),0,1);
  groundTargetReticleDraw(at.x,at.y,62,u,.64);for(const a of hb25BurstAngles(B))combatWarningDraw(b,{...at,ex:at.x+Math.cos(a)*VH,ey:at.y+Math.sin(a)*VH,width:10,progress:u,fieldOnly:true,alpha:.12});}
 return HB25.base.draw.apply(this,arguments);
};
function hb25BurstAngles(B){const at=B.target,n=[9,11,13,15][B.rank],gap=Math.atan2(VH-38-at.y,B.escapeX-at.x),half=Math.max(.32,Math.atan2(46,VH-38-at.y)),angles=[];
 for(let i=0;i<n;i++){const a=i*TAU/n+B.seed*.17;if(Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)))>=half)angles.push(a);}return angles;
}
function hb25Burst(q){const b=q._heraldOwner1003,B=q._hb25Bomb;q.dead=true;if(!b||b.dead||!hd1003Live(b,hd1003Part(b,q._heraldPart1003)))return;
 const at={...B.target},n=[9,11,13,15][B.rank],gap=Math.atan2(VH-38-at.y,B.escapeX-at.x),half=Math.max(.32,Math.atan2(46,VH-38-at.y));
 const live=eBullets.filter(q=>q._hb25Chaos&&!q.dead).length;if(live+n>128)return;
 for(const a of hb25BurstAngles(B))hb25Shot(b,q._heraldPart1003,at,a,1.85+B.rank*.13);
 explode(at.x,at.y,40,'red');combatAudio0927(b,'combatOrb0927',.5);hb25Log(b,'bomb-burst',{id:q._heraldPart1003,x:at.x,y:at.y,escapeX:B.escapeX,gap,half});
}
function hb25Prune(){for(const q of [...eBullets])if(q._hb25Chaos){const b=q._heraldOwner1003;
 if(!b||b!==subBoss||b.dead||run.stage!==8||!hd1003Live(b,hd1003Part(b,q._heraldPart1003))||efxClock-q._hb25Born>6){q.dead=true;continue;}
 if(!q.dead&&q._hb25Bomb&&efxClock>=q._hb25Bomb.at)hb25Burst(q);
 }}
updatePlay=function(){const r=HB25.base.update.apply(this,arguments);hb25Prune();return r;};
globalThis.BOF_HERALD_BOMBER_1025={state:HB25,flight:hb25Flight,claws:hb25Claws};
