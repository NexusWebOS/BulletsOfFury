"use strict";
/* Shared authored-art helpers for Mike's October20 encounter redesign. */
const B20={events:[],draws:{},base:{paint:v19Paint,at:v19AtRect}};
function b20Rank(){return diffKey==='furious'?3:diffKey==='hard'?2:diffKey==='normal'?1:0;}
function b20Target(b){const p=targetShip(b.x,b.y);return{x:p.x,y:p.y};}
function b20Log(kind,data={}){B20.events.push({kind,...data});if(B20.events.length>500)B20.events.shift();}
function b20Cue(key){key=({pickup:'weapon',enemyGun:'enemyMachineGunLight'})[key]||key;const fn=Audio.SFX[key]||Audio.SFX.enemyBossCannon||Audio.SFX.enemyShoot;if(fn)fn();else Snd.play(key);}
function b20Register(art){if(!art)return;if(Array.isArray(art)){art.forEach(b20Register);return;}if(art.path&&art.key)XART._src[art.key]=art.path;else for(const q of Object.values(art))if(q&&typeof q==='object')b20Register(q);}
function b20Keys(art){if(!art)return[];if(Array.isArray(art))return art.flatMap(b20Keys);if(art.key&&art.path)return[art.key];return Object.values(art).filter(q=>q&&typeof q==='object').flatMap(b20Keys);}
function b20Ready(art){let yes=true;for(const key of b20Keys(art))if(!XART.rdy(key))yes=false;return yes;}
function b20Image(a,x,y,k=1,rot=0,flash=0,pivot=a?.pivot){if(!a||!XART.rdy(a.key))return false;ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),-pivot[0]*k,-pivot[1]*k,a.w*k,a.h*k);if(flash>0){ctx.globalAlpha*=Math.min(.85,flash/.12);ctx.drawImage(xartTint(a.key,'#ffffff',1),-pivot[0]*k,-pivot[1]*k,a.w*k,a.h*k);}ctx.restore();B20.draws[a.key]=(B20.draws[a.key]||0)+1;return true;}
function b20Frame(bank,t,seconds=1,loop=false){if(!bank?.length)return null;const u=loop?((t/seconds)%1+1)%1:clamp(t/seconds,0,.99999);return bank[Math.floor(u*bank.length)];}
function b20Piece(p,a,at,rot,k,layer,z=1){const anchor=a.anchor||a.pivot,q=a.bounds,c=Math.cos(rot),s=Math.sin(rot),dx=((q[0]+q[2])/2-anchor[0])*k,dy=((q[1]+q[3])/2-anchor[1])*k;return{p,a,key:a.key,anchor,ax:at.x,ay:at.y,x:at.x+dx*c-dy*s,y:at.y+dx*s+dy*c,w:(q[2]-q[0])*k,h:(q[3]-q[1])*k,k,rot,alpha:1,layer,z,_b20:true,spec:{role:p.spec?.role||'weapon'}};}
v19Paint=function(v,b){if(!v._b20)return B20.base.paint.apply(this,arguments);if(v.spec?.hidden)return;b20Image(v.a,v.ax,v.ay,v.k,v.rot,Math.max(v.p.flash||0,b.flash||0),v.anchor);};
v19AtRect=function(v,x,y){if(!v._b20)return B20.base.at.apply(this,arguments);const c=Math.cos(-v.rot),s=Math.sin(-v.rot),dx=x-v.ax,dy=y-v.ay,px=Math.floor((dx*c-dy*s)/v.k+v.anchor[0]),py=Math.floor((dx*s+dy*c)/v.k+v.anchor[1]),m=v18Mask(v.a);return !!(m&&px>=0&&py>=0&&px<v.a.w&&py<v.a.h&&m[py*v.a.w+px]>48);};
function b20HitSegment(owner,from,to,r,label,hit){for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&player.invuln<=0&&!hit.has(seat)&&s81003Distance(player.x,player.y,{x:from.x,y:from.y,ex:to.x,ey:to.y})<r){hit.add(seat);playerHit(label);b20Log('contact',{label,seat});}});}
function b20Reticle(x,y,r,u){groundTargetReticleDraw(x,y,r*2,clamp(u,0,1),.94);}
function b20Field(owner,from,to,width,u){combatWarningDraw(owner,{x:from.x,y:from.y,ex:to.x,ey:to.y,width,progress:clamp(u,0,1),fieldOnly:true});}
function b20Effect(bank,t,x,y,size,rot=0){const a=b20Frame(bank,t,.65,true);if(a)b20Image(a,x,y,size/Math.max(a.w,a.h),rot,0);}
B20.effectExtents=new WeakMap();
function b20SizedEffect(bank,t,x,y,size,rot=0){if(!bank?.length)return;let extent=B20.effectExtents.get(bank);if(!extent){extent=Math.max(...bank.map(a=>Math.max(a.bounds[2]-a.bounds[0],a.bounds[3]-a.bounds[1])));B20.effectExtents.set(bank,extent);}const a=b20Frame(bank,t,.65,true);if(a)b20Image(a,x,y,size/extent,rot,0);}
function b20Part(b,id,hp,label){return{id,hp,maxhp:hp,destroyed:false,flash:0,kick:0,dmg:true,_v19:true,_vp23:true,spec:{role:id==='core'?'core':id==='head'?'head':'weapon',label}};}
globalThis.BOF_BOSS_REDESIGN=B20;
