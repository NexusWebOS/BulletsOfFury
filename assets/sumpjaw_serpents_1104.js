'use strict';
/* SS116: two articulated toxic serpents. Native SJ98 pools/death/rewards retained. */
const SS116={base:{init:sj98Init,ready:sj98Ready,load:stageLoadBegin,projectile:drawCombatFinalProjectile},events:[],draws:{},book:['leap','orb','acid','coil','leap','acid','orb']};
for(const a of Object.values(SS116_ART.banks))for(const p of a.pages)XART._src[p.key]=p.path;
function ss116Keys(){return Object.values(SS116_ART.banks).flatMap(a=>a.pages.map(p=>p.key));}
function ss116Log(event,data={}){SS116.events.push({event,clock:efxClock,...data});if(SS116.events.length>2000)SS116.events.shift();}
function ss116Blit(n,f,x,y){const a=SS116_ART.banks[n];if(!a)return false;f=((f|0)%a.frames+a.frames)%a.frames;const p=a.pages.find(p=>f>=p.start&&f<p.start+p.frames);if(!p||!XART.rdy(p.key))return false;const j=f-p.start;ctx.drawImage(XART.get(p.key),j%a.cols*a.w,Math.floor(j/a.cols)*a.h,a.w,a.h,Math.round(x)-a.pivot[0],Math.round(y)-a.pivot[1],a.w,a.h);SS116.draws[n]=(SS116.draws[n]||0)+1;return true;}
sj98Ready=function(){return SS116.base.ready()&&ss116Keys().every(k=>XART.rdy(k));};
stageLoadBegin=function(n,keys){return SS116.base.load.call(this,n,n===7&&sj98Rank()?[...(keys||[]),...ss116Keys()]:keys);};
function ss116Wrap(a){return Math.atan2(Math.sin(a),Math.cos(a));}
function ss116Heading(a,x,y,dt){if(Math.hypot(x,y)<.05)return;const target=Math.atan2(-x,y);a.heading+=clamp(ss116Wrap(target-a.heading),-10*dt,10*dt);}
function ss116Frame(a){const n=Math.round(ss116Wrap(a.heading)/TAU*32);return(n%32+32)%32+(a.jaw?32:0);}
sj98Pose=function(a){const q=SS116_ART.banks['body'+sj98State(a)].poses[ss116Frame(a)];return{mouth:q.mouth,gills:[q.gillL,q.gillR],bounds:q.bounds};};
sj98Socket=function(a,id){const p=sj98Pose(a),q=id==='heart'?p.mouth:p.gills[id==='gillL'?0:1];return{x:a.x+q[0],y:a.y+q[1]};};
sj98Foreground=function(a){return !a.dead&&a.phase!=='entry'&&(a.height||0)<30;};
function ss116Point(a,dist){let left=dist;for(let i=1;i<a.trail.length;i++){const p=a.trail[i-1],q=a.trail[i],d=Math.hypot(q.x-p.x,q.y-p.y);if(left<=d){const u=left/Math.max(.001,d);return{x:lerp(p.x,q.x,u),y:lerp(p.y,q.y,u),h:lerp(p.h,q.h,u),heading:Math.atan2(-(p.x-q.x),p.y-q.y)};}left-=d;}return a.trail.at(-1);}
function ss116Trail(a){const p=a.trail[0];if(Math.hypot(a.x-p.x,a.gy-p.y)>3||Math.abs(a.height-p.h)>3)a.trail.unshift({x:a.x,y:a.gy,h:a.height,heading:a.heading});if(a.trail.length>130)a.trail.length=130;}
sj98Init=function(b){const out=SS116.base.init(b),G=b._sj98;G.rest=.2;G.serial=0;SS116.events=[];SS116.draws={};for(const a of G.actors){a.flip=false;a.heading=0;a.gy=-80-a.i*70;a.y=a.gy;a.height=0;a.jaw=0;a.trail=Array.from({length:45},(_,i)=>({x:a.x,y:a.gy-i*6,h:0,heading:0}));a.support=2+a.i*.8;}l23FovWarm();stageLoadBegin(7,ss116Keys());ss116Log('spawn',{hp:b.maxhp,actors:G.actors.map(a=>a.maxhp)});return out;};
function ss116Aim(a){return{x:clamp(player.x,camLeftX()+50,camRightX()-50),y:clamp(player.y,100,VH-45)};}
sj98Target=function(a){return ss116Aim(a);};
sj98Start=function(b,a){const G=b._sj98;G.owner=a;a.seq++;a.attack=SS116.book[(a.seq-1+a.i*2)%SS116.book.length];a.phase='warn';a.t=0;a.warn=a.attack==='leap'?.82:a.attack==='coil'?.7:.68;a.target=ss116Aim(a);a.from={x:a.x,y:a.gy};a.hits=new Set();a.jaw=0;a.emitted=0;
 if(a.attack==='leap'){a.leapNo=(a.leapNo||0)+1;a.overflight=a.leapNo%2===0;const sx=a.i?1:-1,goal=a.overflight?{x:clamp(a.target.x+sx*85,camLeftX()+70,camRightX()-70),y:clamp(a.target.y+75,110,VH-42)}:{...a.target};a.land={...goal};let m;for(let i=0;i<3;i++){a.landHeading=Math.atan2(-(a.land.x-a.x),a.land.y-a.gy);const n=(Math.round(a.landHeading/TAU*32)%32+32)%32;m=SS116_ART.banks.body0.poses[32+n].mouth;a.land={x:clamp(goal.x-m[0],camLeftX()+60,camRightX()-60),y:clamp(goal.y-m[1],65,VH-42)};}a.impact={x:a.land.x+m[0],y:a.land.y+m[1]};a.jumpTime=clamp(Math.hypot(a.land.x-a.x,a.land.y-a.gy)/620,.58,.88);}
 combatAudio0927(a,'bossWeaponCharge',.1);sj98Log('attack',{actor:a.i,kind:a.attack,target:a.target,warn:a.warn});ss116Log('tell',{actor:a.i,kind:a.attack,warn:a.warn,target:a.attack==='leap'?a.impact:a.target});};
sj98End=function(b,a){a.phase='recover';a.t=0;a.jaw=0;a.attack=null;a.height=0;b._sj98.owner=null;b._sj98.rest=.24;sj98Log('recover',{actor:a.i});};
function ss116Shot(b,a,angle,giant=false){const p=sj98Socket(a,'heart');const q=eShootT(p.x,p.y,angle,giant?3.8:5.2,'s7acid',{owner:b,noMuzzle:true,silent:true,w:giant?54:12,h:giant?54:12});if(!q)return;Object.assign(q,{_ss116:giant?'orb':'acid',_sj98Actor:a,_sj98Owner:b,_sj98Age:0,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});if(!b._sj98.fx.some(f=>f.a===a&&f.mouth&&f.t===0))b._sj98.fx.push({a,x:p.x,y:p.y,t:0,mouth:true});combatAudio0927(a,'combatToxic0927',giant?.16:.09);ss116Log(giant?'giant-orb':'acid-spit',{actor:a.i,from:p,angle,speed:giant?3.8:5.2});}
function ss116Spit(b,a,giant=false){const p=sj98Socket(a,'heart'),angle=Math.atan2(a.target.y-p.y,a.target.x-p.x);if(giant){ss116Shot(b,a,angle+(a.emitted-1)*.18,true);}else for(const d of[-.19,0,.19])ss116Shot(b,a,angle+d,false);a.emitted++;a.jaw=1;}
function ss116Travel(a,x,y,speed,dt){const dx=x-a.x,dy=y-a.gy,d=Math.hypot(dx,dy),u=Math.min(1,speed*dt/Math.max(.001,d));ss116Heading(a,dx,dy,dt);a.x+=dx*u;a.gy+=dy*u;}
function ss116Cruise(a,dt,recover=false){const mid=camLeftX()+viewW()/2,side=a.i?1:-1,t=a.clock*1.7+a.i*Math.PI,tx=mid+side*105+Math.sin(t)*56,ty=157+Math.sin(t*1.2+a.i)*74;ss116Travel(a,tx,ty,recover?275:180,dt);}
function ss116Separation(G,a,dt){if(['leap','coil','entry'].includes(a.phase)||a.height>15)return;const other=G.actors.find(q=>q!==a&&!q.dead&&q.height<15&&q.phase!=='entry');if(!other)return;const dx=a.x-other.x,dy=a.gy-other.gy,d=Math.hypot(dx,dy),r=128;if(d<r){const push=Math.min((r-d)*.5,150*dt),side=dx||((a.i?1:-1)*.1);a.x+=side/Math.max(.1,d)*push;a.gy+=(dy||.1)/Math.max(.1,d)*push;}}
function ss116Contact(a){if(a.height>20||!['land','coil'].includes(a.phase))return;const p=sj98Socket(a,'heart');for(const seat of seatList())withSeat(seat,()=>{if(!a.hits.has(seat)&&!player.dead&&Math.hypot(player.x-p.x,player.y-p.y)<29){a.hits.add(seat);playerHit('Sumpjaw pounce');ss116Log('contact',{actor:a.i,seat});}});}
sj98Tick=function(b,dt){const G=b._sj98;b.t+=dt;if(!sj98Ready())return;G.clock+=dt;G.rest-=dt*(ng27On()?1.15:1);const rate=turretSpeed15(1)*(ng27On()?1.15:1);
 for(const a of G.actors){a.clock+=dt;a.flash=Math.max(0,a.flash-dt);a.t+=dt;
  if(a.dead){a.dying+=dt;for(let j=0;j<7;j++)if(a.dying>=.13+j*.13&&!(a.deathBits&(1<<j))){a.deathBits=(a.deathBits||0)|(1<<j);const q=ss116Point(a,35+j*19);explode(q.x,q.y-q.h,32,'green');}if(a.dying>=1.1&&!a.shattered){a.shattered=true;for(let j=0;j<9;j++)G.fragments.push({f:j,x:a.x+(j%3-1)*50,y:a.y+(Math.floor(j/3)-1)*50,vx:(j%3-1)*105,vy:-65+Math.floor(j/3)*50,t:0});}continue;}
  a.jaw=0;
  if(a.phase==='entry'){ss116Travel(a,a.home.x,130+a.i*40,240,dt);if(a.t>1.1+a.i*.25){a.phase='idle';a.t=0;}}
  else if(['idle','recover','stun'].includes(a.phase)){a.height=Math.max(0,a.height-180*dt);ss116Cruise(a,dt,a.phase!=='idle');if(a.phase!=='idle'&&a.t>(a.phase==='stun'?.65:.36)/rate){a.phase='idle';a.t=0;}}
  else if(a.phase==='warn'){const p=sj98Socket(a,'heart');ss116Heading(a,a.target.x-p.x,a.target.y-p.y,dt);sj98Tell(a,a.t,a.warn);a.jaw=Math.floor(a.t*16)%2;if(a.t>=a.warn){a.phase=a.attack;a.t=0;a.from={x:a.x,y:a.gy};a.emitted=0;combatAudio0927(a,a.attack==='leap'?'jetDash':'combatServo0927',.15);sj98Log('release',{actor:a.i,kind:a.attack});ss116Log('release',{actor:a.i,kind:a.attack});}}
  else if(a.phase==='leap'){const u=clamp(a.t/a.jumpTime,0,1),bend=(a.i?1:-1)*Math.sin(u*Math.PI)**2*38,x=lerp(a.from.x,a.land.x,u)+bend,y=lerp(a.from.y,a.land.y,u);ss116Heading(a,x-a.x,y-a.gy,dt);a.x=x;a.gy=y;a.height=Math.sin(u*Math.PI)*96;a.y=a.gy-a.height;a.jaw=1;if(a.emitted===0&&u>.3){a.target=ss116Aim(a);ss116Shot(b,a,Math.atan2(a.target.y-a.y,a.target.x-a.x),true);a.emitted++;}if(u>=1){a.phase='land';a.t=0;a.height=0;a.heading=a.landHeading;G.fx.push({a,x:a.x,y:a.gy,t:0});combatAudio0927(a,'hammerImpact',.15);shake=Math.max(shake,2);ss116Log('landing',{actor:a.i,x:a.impact.x,y:a.impact.y,warning:a.warn,overflight:a.overflight});}}
  else if(a.phase==='land'){a.jaw=1;if(a.t>.18)sj98End(b,a);}
  else if(a.phase==='orb'){const facing=a.heading;ss116Cruise(a,dt);a.heading=facing;const p=sj98Socket(a,'heart');ss116Heading(a,a.target.x-p.x,a.target.y-p.y,dt);while(a.emitted<3&&a.t>=a.emitted*.23/rate)ss116Spit(b,a,true);a.jaw=Math.floor(a.t*24)%2;if(a.t>.85/rate)sj98End(b,a);}
  else if(a.phase==='acid'){const p=sj98Socket(a,'heart');ss116Heading(a,a.target.x-p.x,a.target.y-p.y,dt);while(a.emitted<6&&a.t>=a.emitted*.105/rate)ss116Spit(b,a,false);a.jaw=Math.floor(a.t*30)%2;if(a.t>.8/rate)sj98End(b,a);}
  else if(a.phase==='coil'){const u=clamp(a.t/1.2,0,1),mid=camLeftX()+viewW()/2,cx=clamp(a.from.x,mid-45,mid+45),cy=clamp(a.from.y,145,265),angle=a.i*Math.PI+u*TAU;const x=cx+Math.sin(angle)*112,y=cy+Math.cos(angle)*90;ss116Travel(a,x,y,640,dt);a.jaw=1;while(a.emitted<4&&a.t>=.15+a.emitted*.24/rate){a.target=ss116Aim(a);ss116Shot(b,a,Math.atan2(a.target.y-a.y,a.target.x-a.x),a.emitted%2===0);a.emitted++;}if(u>=1)sj98End(b,a);}
  ss116Separation(G,a,dt);if(a.phase!=='entry'){a.x=clamp(a.x,camLeftX()+60,camRightX()-60);a.gy=clamp(a.gy,65,VH-42);}a.y=a.gy-a.height;ss116Trail(a);ss116Contact(a);
 }
 if(!b.dead&&!G.owner&&G.rest<=0){const ready=G.actors.filter(a=>!a.dead&&a.phase==='idle'),a=ready.find(a=>a.i===G.turn)||ready[0];if(a){G.turn=1-a.i;sj98Start(b,a);}}
 for(const f of G.fx){f.t+=dt;if(f.mouth&&!f.a.dead){const p=sj98Socket(f.a,'heart');f.x=p.x;f.y=p.y;}}G.fx=G.fx.filter(f=>f.t<(f.mouth?.22:.55)&&!f.a.dead);
 for(const q of eBullets)if(q._sj98Owner===b){q._sj98Age+=dt;if(q._sj98Age>3.8||q._sj98Actor.dead||b.dead)q.dead=true;}
 for(const f of G.fragments){f.t+=dt;f.x+=f.vx*dt;f.y+=f.vy*dt;f.vy+=180*dt;}G.fragments=G.fragments.filter(f=>f.t<.85);
 if(b.dead){b.dying+=dt;if(b.dying>=2.4&&!G.rewarded){G.rewarded=true;continueRewardResolve(b,b.x,VH*.4,'miniboss');dropPowerup(b.x,VH*.4,'weapon');run.score+=5200;subBoss=null;subBossActive=false;subBossDone=true;sj98Log('progression');}}
 sj98Sync(b);
};
drawCombatFinalProjectile=function(q){if(q?._ss116)return ss116Blit(q._ss116,Math.floor(q._sj98Age*24)%16,q.x,q.y);return SS116.base.projectile.apply(this,arguments);};
function ss116Segments(a,shadow){for(let i=9;i>=0;i--){const p=ss116Point(a,48+i*17),n=((Math.round(p.heading/TAU*32)%32)+32)%32,mode=shadow?'shadow':a.flash>0?'hit':['warn','orb','acid'].includes(a.phase)?'hot':'body';ss116Blit('segment'+(i>7?2:i>4?1:0)+'_'+mode,n,p.x,p.y+(shadow?12:-p.h));}}
sj98Draw=function(b){const G=b._sj98;
 for(const a of G.actors)if(!a.dead&&a.phase==='warn'&&a.attack!=='leap'){const m=sj98Socket(a,'heart'),angle=Math.atan2(a.target.y-m.y,a.target.x-m.x),spread=a.attack==='orb'?.18:.19;for(const d of[-spread,0,spread])combatWarningDraw(a,{x:m.x,y:m.y,ex:m.x+Math.cos(angle+d)*640,ey:m.y+Math.sin(angle+d)*640,width:a.attack==='orb'?56:18,progress:a.t/a.warn,fieldOnly:true});}
 for(const a of G.actors)if(!a.dead||a.dying<1.1){if(a.phase==='warn'&&a.attack==='leap')sj98Retina(a.impact.x,a.impact.y,a.t,a.warn);if(a.phase==='leap')sj98Retina(a.impact.x,a.impact.y,a.warn,a.warn);ss116Segments(a,true);ss116Blit('head_shadow',ss116Frame(a)%32,a.x,a.gy+12);}
 for(const a of G.actors){if(a.dead&&a.dying>=1.1)continue;ss116Segments(a,false);const state=sj98State(a),white=a.flash>0||a.dead&&Math.floor(a.dying*20)%2,name=white?'hit':(['warn','orb','acid'].includes(a.phase)?'hot':'body')+state;ss116Blit(name,ss116Frame(a),a.x+(a.dead?Math.floor(Math.sin(a.dying*61)*2):0),a.y);}
 for(const f of G.fragments)sj98Blit('fragment',f.f,f.x,f.y);
 for(const f of G.fx)if(f.mouth)ss116Blit('muzzle',Math.min(15,Math.floor(f.t/.22*16)),f.x,f.y);else sj98Blit('splash',Math.min(15,Math.floor(f.t/.55*16)),f.x,f.y);
 for(const a of G.actors){if(a.dead)continue;const p=sj98Pose(a),x=clamp(a.x,camLeftX()+85,camRightX()-85),y=Math.max(34,a.y+p.bounds[1]-20);sj98Blit('health_frame',0,x,y);sj98Blit('health_fill',0,x-72,y+5,false,Math.ceil(144*a.hp/a.maxhp));pm27Draw(ctx,'SUMPJAW '+(a.i+1),x,y-5,8,{family:'command',palette:'toxic',width:130});}
};
globalThis.BOF_SUMPJAW_SERPENTS_1104={state:SS116,init:sj98Init};
BOF_SUMPJAW_DUO_1031.init=sj98Init;
