'use strict';
/* HG70: missile depth counters, lethal laser glass and authored foreground spiral. */
const HG70={base:{update:updatePlay,targets:retinaBossTargets,at:hd1003At,load:stageLoadBegin},events:[]};
for(const [n,a]of Object.entries(HG70_ART)){XART._src[a.key]=a.path;if(['yaw','yaw_hit','spiral','spiral_hit','spin_hit','charge_hit'].includes(n))HD54_ART[n]=a;}
stageLoadBegin=function(n,keys){return HG70.base.load.call(this,n,n===8?[...(keys||[]),...Object.values(HG70_ART).map(a=>a.key)]:keys);};
function hg70Log(event,data={}){HG70.events.push({event,time:efxClock,...data});if(HG70.events.length>1400)HG70.events.shift();}
function hg70Active(F){return !F.done&&!F.returning&&F.b===subBoss&&!F.b.dead&&run.stage===8&&F.q&&!F.q.dead;}
function hg70Reflect(F,shot){if(!hg70Active(F))return false;const q=F.q;F.returning={from:{x:q.x,y:q.y},born:efxClock,level:F.level};F.x=q.x;F.y=q.y;F.done=false;q.dead=true;F.q=null;
 if(shot)shot.dead=true;combatAudio0927(F.b,'missileHit',.10);hg70Log('orb-reflected',{id:F.id,level:F.level,x:F.x,y:F.y});return true;}
function hg70Shatter(F){if(!hg70Active(F))return false;const q=F.q,b=F.b;F.done=true;q.dead=true;
 const size=Math.min(7,Math.floor(F.level*7/9));HH52.fx.push({b,x:q.x,y:q.y,t:0,size,glass:true});if(HH52.fx.length>18)HH52.fx.shift();
 const n=8+Math.floor(F.level*.8),phase=F.spin*.21;let count=0;
 for(let i=0;i<n&&eBullets.filter(p=>p._hg70Glass&&!p.dead).length<80;i++){
  const a=i*TAU/n+phase,p=hs53Round(b,q,a,2.6+F.level*.12,'shard',{_hg70Glass:true,_hs53Dir:((Math.round(a*32/TAU)%32)+32)%32,_hs53Phase:i%8});if(p)count++;
 }
 combatAudio0927(b,'iceOrbImpact',.12);hg70Log('orb-glass-shatter',{id:F.id,level:F.level,fragments:count,x:q.x,y:q.y});return true;}
function hg70Weapon(F,shot){if(!shot||shot.dead)return false;if(shot.kind==='gmiss')return hg70Reflect(F,shot);
 if(shot.kind==='beam'||shot.kind==='laser'){const hit=hg70Shatter(F);if(hit&&shot.kind!=='beam'&&!shot.pierce)shot.dead=true;return hit;}return false;}
function hg70Segment(x,y,x1,y1,x2,y2,r){const dx=x2-x1,dy=y2-y1,d=dx*dx+dy*dy,u=d?clamp(((x-x1)*dx+(y-y1)*dy)/d,0,1):0;return Math.hypot(x-x1-u*dx,y-y1-u*dy)<=r;}
function hg70Intercept(dt){for(const F of HD54.flights){if(!hg70Active(F))continue;const q=F.q,r=Math.max(q.w,q.h)*.5;
 for(const shot of pBullets){if(shot.dead||!['gmiss','beam','laser'].includes(shot.kind))continue;
  let hit=false;if(shot.kind==='beam'){const owner=seatShip(shot.seat||1);hit=Math.abs(owner.x-q.x)<r+shot.w/2&&q.y-r<=owner.y-14&&q.y+r>=(shot.top??-20);}
  else{const scale=shot.kind==='gmiss'?1:dt*60,dx=(shot.vx||0)*scale,dy=(shot.vy??-(shot.spd||0))*scale;
   hit=hg70Segment(q.x,q.y,shot.x,shot.y,shot.x+dx-q.vx*dt*60,shot.y+dy-q.vy*dt*60,r+Math.max(shot.w||8,shot.h||8)*.4);}
  if(hit&&hg70Weapon(F,shot))break;
 }
}}
function hg70Return(F){const r=F.returning,u=clamp((efxClock-r.born)/.72,0,1),a=hd54Own(F.b),meta=a&&HD54_ART[a.bank]?.sockets?.[a.frame],tx=F.b.x+(meta?.[0]||0),ty=F.b.y+(meta?.[1]||-20);
 F.x=lerp(r.from.x,tx,u);F.y=lerp(r.from.y,ty,u);F.level=Math.max(0,Math.floor(r.level*(1-u)));if(u<1)return;
 F.done=true;const b=F.b,before=b.hp;b._hg70Counter=true;
 try{hd1003Hit(b,b.maxhp*.0125,b.x,b.y,'core');}finally{delete b._hg70Counter;}
 HH52.fx.push({b,x:tx,y:ty,t:0,size:2,glass:true});if(HH52.fx.length>18)HH52.fx.shift();combatAudio0927(b,'combatOrb0927',.10);
 hg70Log('orb-counter-hit',{id:F.id,damage:Math.max(0,before-b.hp),hp:b.hp,x:tx,y:ty});}
function hg70Surface(b,A){if(HD54.flights.filter(F=>!F.done).length>=48)return;const a=HD54_ART[A.bank],p=a.sockets[A.frame],point={x:b.x+p[0],y:b.y+p[1]},rank=bh25Rank(),n=8+rank*2;let made=0;
 for(let i=0;i<n&&HD54.flights.filter(F=>!F.done).length<48&&eBullets.filter(q=>q._heraldOwner1003===b&&!q.dead).length<128;i++){const angle=i*TAU/n+A.t*.8,q=eShootT(point.x,point.y,angle,2.8+rank*.18,'s8pair',{owner:b,noMuzzle:true,silent:true,w:32,h:32});if(!q)continue;
  const F={id:++HD54.serial,b,born:efxClock,life:2.6,from:{...point},target:{...point},x:point.x,y:point.y,level:6,spin:i%32,surface:true,q};
  Object.assign(q,{_hd54:true,_hd54Flight:F,_hd54Born:efxClock,_heraldOwner1003:b,_heraldPart1003:'head',_noArsenal:true,_boss:true,_weaponProof:true,_shootable:false,_s3kOriginalProof:false,homing:false});delete q.hp;HD54.flights.push(F);made++;
 }
 combatAudio0927(b,'combatOrb0927',.10);hg70Log('foreground-circle',{count:made,bank:A.bank,frame:A.frame,x:point.x,y:point.y});}
function hg70Foreground(b,A,dt){hd54Phase(A,'foreground');const u=A.t-20.6;A.bank=u<3?'yaw':'spiral';const a=HD54_ART[A.bank];A.frame=Math.floor(u*(u<3?40:60))%a.frames;
 const cx=camLeftX()+viewW()/2;b.x=cx+Math.sin(u*1.5)*Math.min(90,viewW()*.18);b.y=A.origin.y+Math.sin(u*3)*28;A.dark=8;
 if(!A.hg70Front){A.hg70Front=true;A.surfaceNext=A.t+.25;A.depthNext=A.t+.65;hg70Log('foreground-spiral-start');}
 if(A.t>=A.surfaceNext){hg70Surface(b,A);A.surfaceNext=A.t+1.35/(run.ngplus?1.15:1);}
 if(A.t>=A.depthNext){hd54Emit(b,A);A.depthNext=A.t+.42/(run.ngplus?1.15:1);}
 if(u>=10.5){hd54Log('desperation-complete',{hp:b.hp,shots:A.shots});hr28End(b);}}
function hg70Mask(b,x,y){const A=hd54Own(b);if(!A||A.phase!=='foreground'||!HD54_ART[A.bank]?.spans)return undefined;const a=HD54_ART[A.bank],xx=Math.floor(x-b.x+a.pivot[0]),yy=Math.floor(y-b.y+a.pivot[1]);if(xx<0||xx>=a.cw||yy<0||yy>=a.ch)return null;
 const row=a.spans[A.frame][yy];for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return'core';return null;}
hd1003At=function(b,x,y){const m=hg70Mask(b,x,y);return m===undefined?HG70.base.at.apply(this,arguments):m;};
retinaBossTargets=function(b){if(!hd54Boss(b))return HG70.base.targets.apply(this,arguments);const A=hd54Own(b);let list=HG70.base.targets.apply(this,arguments);
 if(A?.phase==='foreground'&&HD54_ART[A.bank]?.spans){list=[retinaDynamicPiece(b,'hg70-rotating-core','Herald spiral core',()=>({x:b.x,y:b.y,hp:b.hp,dead:b.dead||hd54Own(b)?.phase!=='foreground'}),(d,shot)=>{
   if(shot?.kind==='beam'){let found=false;for(let y=Math.max(shot.top||-20,b.y-160);y<Math.min(shot.bot,b.y+160)&&!found;y+=3)if(hg70Mask(b,shot.x,y))found=true;if(!found)return;}
   hd1003Hit(b,d,b.x,b.y,'core');},220,240)];}
 for(const F of HD54.flights)if(hg70Active(F)){const q=F.q;list.push(retinaDynamicPiece(b,'hg70-orb-'+F.id,'Counterable depth orb',()=>({x:q.x,y:q.y,hp:1,dead:!hg70Active(F)}),(d,shot)=>hg70Weapon(F,shot),q.w,q.h));}
 return list;};
globalThis.BOF_HERALD_GOTHIC_1030={state:HG70,reflect:hg70Reflect,shatter:hg70Shatter};
