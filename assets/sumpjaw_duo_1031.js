'use strict';
/* SJ98: Furious-only paired Sumpjaw. One native encounter, two independent health budgets. */
const SJ98={base:{spawn:spawnSubBoss__inner,tick:updateSubBoss,draw:drawSubBoss,hit:hitSubBoss,
 at:subBossHitPart,solid:subBossSolidAt,beam:subBossBeamImpact,targets:retinaBossTargets,
 load:stageLoadBegin,projectile:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,
 ready:target17Ready,damage:encounterDamageOverlay,begin:beginStage},events:[],draws:{},serial:0};
for(const a of Object.values(SJ98_ART.banks))for(const p of a.pages)XART._src[p.key]=p.path;
function sj98Keys(){return Object.values(SJ98_ART.banks).flatMap(a=>a.pages.map(p=>p.key));}
function sj98Own(b){return !!b?._sj98;}
function sj98Rank(){return diffKey==='furious'||diffKey==='insanity';}
function sj98Log(event,data={}){SJ98.events.push({event,clock:efxClock,...data});if(SJ98.events.length>1600)SJ98.events.shift();}
function sj98Blit(n,f,x,y,flip=false,width){const a=SJ98_ART.banks[n];if(!a)return false;f=clamp(f|0,0,a.frames-1);const p=a.pages.find(p=>f>=p.start&&f<p.start+p.frames);if(!p||!XART.rdy(p.key))return false;
 const i=f-p.start,im=XART.get(p.key),w=width==null?a.w:Math.max(0,Math.min(a.w,width|0));if(!w)return true;
 ctx.save();ctx.translate(Math.round(x),Math.round(y));if(flip)ctx.scale(-1,1);
 ctx.drawImage(im,i%a.cols*a.w,Math.floor(i/a.cols)*a.h,w,a.h,-a.pivot[0],-a.pivot[1],w,a.h);ctx.restore();SJ98.draws[n]=(SJ98.draws[n]||0)+1;return true;}
function sj98Ready(){return sj98Keys().every(k=>XART.rdy(k));}
stageLoadBegin=function(n,keys){if(n===7&&sj98Rank())Snd.prepare(['bossWeaponCharge','combatToxic0927','combatModule0927','combatServo0927','jetDash','hammerImpact','expBig']);return SJ98.base.load.call(this,n,n===7&&sj98Rank()?[...(keys||[]),...sj98Keys()]:keys);};
target17Ready=function(b){return sj98Own(b)?false:SJ98.base.ready.apply(this,arguments);};
encounterDamageOverlay=function(b){if(sj98Own(b))return;return SJ98.base.damage.apply(this,arguments);};
function sj98Sync(b){const G=b._sj98;b.hp=G.actors.reduce((s,a)=>s+Math.max(0,a.hp),0);b.maxhp=G.actors.reduce((s,a)=>s+a.maxhp,0);b._drawW=b.w=worldWidth();b._drawH=b.h=VH;b._drawY=b.y=VH/2;b.x=worldWidth()/2;}
function sj98Init(b){
 const total=Math.ceil(1560*DIFF.eHp*1.10),mid=camLeftX()+viewW()/2;
 for(const k of ['_ship','_s7mod','_mr27','_late27','_be','_deathFxStarted'])delete b[k];
 b.name='SUMPJAW PAIR';b.enter=false;b.dead=false;b.fireCd=999;b._noHit=false;b._s4MiniSafe=true;
 const actors=[0,1].map(i=>{const maxhp=Math.ceil(total/2),gill=Math.floor(maxhp*.25);return{i,x:mid+(i?1:-1)*124,y:145,home:{x:mid+(i?1:-1)*124,y:145},hp:maxhp,maxhp,clock:0,phase:'entry',t:0,frame:24,flash:0,dead:false,dying:0,flip:i===1,seq:0,
  pools:[{id:'gillL',hp:gill,maxhp:gill},{id:'gillR',hp:gill,maxhp:gill},{id:'heart',hp:maxhp-2*gill,maxhp:maxhp-2*gill}],hits:new Set(),fx:[],depth:0};});
 b._sj98={actors,clock:0,turn:0,owner:null,rest:1,flights:[],fx:[],fragments:[],cleared:false};
 sj98Sync(b);stageLoadBegin(7,sj98Keys());sj98Log('spawn',{hp:b.maxhp,actors:actors.map(a=>a.maxhp)});return b;
}
spawnSubBoss__inner=function(kind){const out=SJ98.base.spawn.apply(this,arguments);if(run.stage===7&&sj98Rank()&&subBoss&&kind==='dualscoopdredger')sj98Init(subBoss);return out;};
function sj98State(a){return(a.pools[0].hp<=0?1:0)|(a.pools[1].hp<=0?2:0);}
function sj98Foreground(a){return !a.dead&&a.phase!=='entry'&&a.phase!=='dive'&&!(a.phase==='warn'&&a.attack==='breach')&&(a.phase!=='breach'||a.t>=.42);}
function sj98Pose(a){return SJ98_ART.banks['body'+sj98State(a)].poses[a.frame];}
function sj98Socket(a,id){const p=sj98Pose(a),q=id==='heart'?p.mouth:p.gills[id==='gillL'?0:1];return{x:a.x+(a.flip?-q[0]:q[0]),y:a.y+q[1]};}
function sj98Targets(b){if(!sj98Own(b)||b.dead)return[];return b._sj98.actors.flatMap(a=>{
 if(!sj98Foreground(a))return[];return a.pools.filter(p=>p.hp>0&&(p.id!=='heart'||sj98State(a)===3)).map(p=>retinaDynamicPiece(b,'sump'+a.i+'-'+p.id,'Sumpjaw '+(p.id==='heart'?'intake heart':'toxic gill'),()=>({...sj98Socket(a,p.id),hp:p.hp,dead:a.dead||!sj98Foreground(a)||p.hp<=0||p.id==='heart'&&sj98State(a)!==3}),d=>sj98Damage(b,d,null,null,{a,p}),p.id==='heart'?34:30,p.id==='heart'?34:40));
 });}
retinaBossTargets=function(b){return sj98Own(b)?sj98Targets(b):SJ98.base.targets.apply(this,arguments);};
function sj98At(b,x,y,pad=0){if(!sj98Own(b)||b.dead)return null;let best=null,d=Infinity;
 for(const a of b._sj98.actors){if(!sj98Foreground(a))continue;for(const p of a.pools){if(p.hp<=0||p.id==='heart'&&sj98State(a)!==3)continue;const q=sj98Socket(a,p.id),rx=(p.id==='heart'?17:15)+pad,ry=(p.id==='heart'?17:20)+pad,v=((x-q.x)/rx)**2+((y-q.y)/ry)**2;if(v<=1&&v<d){d=v;best={a,p};}}}return best;}
subBossHitPart=function(x,y){return sj98Own(subBoss)?sj98At(subBoss,x,y):SJ98.base.at.apply(this,arguments);};
subBossSolidAt=function(x,y){return sj98Own(subBoss)?!!sj98At(subBoss,x,y,Math.min(3,(_dmgBullet?.w||0)*.25)):SJ98.base.solid.apply(this,arguments);};
function sj98Beam(b,beam){const range=playerBeamRange(beam);if(!range)return null;let best=null;
 for(const a of b._sj98.actors)for(const p of a.pools){if(p.hp<=0||!sj98Foreground(a)||p.id==='heart'&&sj98State(a)!==3)continue;const q=sj98Socket(a,p.id),rx=p.id==='heart'?17:15,ry=p.id==='heart'?17:20;
  if(q.y+ry<range.top||q.y-ry>range.bot||Math.abs(q.x-range.x)>rx+range.half)continue;const y=Math.min(range.bot,q.y+ry-1);if(!best||y>best.entry)best={x:clamp(range.x,q.x-rx+1,q.x+rx-1),y,entry:y,key:'sump'+a.i+'-'+p.id};}return best;}
subBossBeamImpact=function(b,beam){return sj98Own(b)?sj98Beam(b,beam):SJ98.base.beam.apply(this,arguments);};
function sj98Clear(b,a){const G=b._sj98;for(const q of eBullets)if(q._sj98Actor===a)q.dead=true;G.flights=G.flights.filter(f=>f.a!==a);G.fx=G.fx.filter(f=>f.a!==a);groundTargetingCancel(a);if(G.owner===a)G.owner=null;}
function sj98Damage(b,raw,x,y,part){if(!sj98Own(b)||b.dead||!Number.isFinite(raw)||raw<=0)return 0;
 if(!part&&_dmgBullet?.kind==='beam'){const q=sj98Beam(b,_dmgBullet);if(!q)return 0;x=q.x;y=q.y;}
 part=part||sj98At(b,x??_lastHitX,y??_lastHitY,2);if(!part)return 0;const{a,p}=part;
 if(a.dead||!sj98Foreground(a)||p.hp<=0||p.id==='heart'&&sj98State(a)!==3)return 0;
 const elem=elementalDamageResult(b,'subboss',_dmgBullet,raw,x,y);let dmg=er26DamageClamp(b,elem.dmg);if(!(dmg>0))return 0;
 const before=p.hp,point=sj98Socket(a,p.id);enemyPoolDamage(p,'hp',dmg,'sumpjawPart','maxhp');p.hp=Math.max(0,p.hp);a.hp=a.pools.reduce((s,p)=>s+p.hp,0);if(a.clock>=(a.flashNext||0)){markHit(a,.065);a.flashNext=a.clock+.16;}weaponHitSfx('normal');
 if(typeof stageStats!=='undefined')stageStats.dmgDealt+=before-p.hp;
 if(p.hp<=0){sj98Log('part-break',{actor:a.i,part:p.id});s7mFX(point.x,point.y,70,true);combatAudio0927(a,'combatModule0927',.12);shake=Math.max(shake,3);
  if(p.id!=='heart'&&sj98State(a)===3){a.phase='stun';a.t=0;sj98Clear(b,a);sj98Log('heart-open',{actor:a.i,hp:a.hp});}}
 if(a.hp<=0&&!a.dead){a.dead=true;a.phase='dead';a.dying=0;sj98Clear(b,a);unitDeathFX({x:a.x,y:a.y,w:176,h:176},'mini','green');combatAudio0927(a,'expBig',.2);sj98Log('actor-defeat',{actor:a.i});}
 sj98Sync(b);
 if(b.hp<=0&&!b.dead){b.dead=true;b.dying=0;const G=b._sj98;G.owner=null;G.flights=[];G.fx=[];G.cleared=true;achievementEncounterDefeat(b,'miniboss');sj98Log('pair-defeat');}
 return before-p.hp;}
hitSubBoss=function(dmg,x,y){return sj98Own(subBoss)?sj98Damage(subBoss,dmg,x,y):SJ98.base.hit.apply(this,arguments);};
function sj98Tell(a,t,life){combatWarningTick(a,'sumpjaw-'+a.i+'-'+a.seq,t,life);}
function sj98Target(a){const m=camLeftX()+viewW()/2,p=SJ98_ART.banks.body0.poses[47],dx=(a.flip?-1:1)*p.mouth[0],lo=a.flip?-p.bounds[2]:p.bounds[0],hi=a.flip?-p.bounds[0]:p.bounds[2],left=(a.i?m+12:camLeftX()+12)-lo+dx,right=(a.i?camRightX()-12:m-12)-hi+dx;return{x:clamp(player.x,left,right),y:clamp(player.y-44,255,VH-112)};}
function sj98Start(b,a){const G=b._sj98;G.owner=a;a.seq++;a.t=0;a.hits=new Set();a.from={x:a.x,y:a.y};const book=['breach','lob','bite'];a.attack=book[(a.seq-1)%book.length];a.phase='warn';
 a.target=sj98Target(a);a.warn=a.attack==='lob'?.85:a.attack==='breach'?1.35:1.25;
 if(a.attack==='breach'){a.phase='dive';a.land={...a.target};}combatAudio0927(a,'bossWeaponCharge',.1);sj98Log('attack',{actor:a.i,kind:a.attack,target:a.target,warn:a.warn});}
function sj98End(b,a){a.phase='recover';a.t=0;a.frame=0;a.attack=null;b._sj98.owner=null;b._sj98.rest=.65;sj98Log('recover',{actor:a.i});}
function sj98Move(a,x,y,speed,dt){const d=Math.hypot(x-a.x,y-a.y),u=Math.min(1,speed*dt/Math.max(.001,d));a.x=lerp(a.x,x,u);a.y=lerp(a.y,y,u);}
function sj98Lob(b,a,i){const G=b._sj98,p=sj98Socket(a,'heart'),half=worldWidth()/2;
 const tx=clamp(a.target.x+(i-1)*74,36,worldWidth()-36),ty=clamp(a.target.y+(i%2?35:-15),230,VH-40),life=1.15+i*.12;
 G.flights.push({a,id:++SJ98.serial,from:p,target:{x:tx,y:ty},x:p.x,y:p.y,t:0,life,arc:80});combatAudio0927(a,'combatToxic0927',.12);G.fx.push({a,x:p.x,y:p.y,t:0});sj98Log('toxic-lob',{actor:a.i,from:p,target:{x:tx,y:ty}});}
function sj98Splash(b,F){const G=b._sj98;G.fx.push({a:F.a,x:F.target.x,y:F.target.y,t:0});combatAudio0927(F.a,'combatToxic0927',.12);
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-F.target.x,player.y-F.target.y)<25)playerHit('Sumpjaw toxic landing');});
 for(let i=0;i<5;i++){const angle=i*TAU/5+F.id*.34,q=eShootT(F.target.x,F.target.y,angle,2.75,'s7acid',{owner:b,noMuzzle:true,silent:true,w:14,h:14});Object.assign(q,{_sj98Actor:F.a,_sj98Owner:b,_sj98Age:0,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});}
 sj98Log('splash',{actor:F.a.i,x:F.target.x,y:F.target.y});}
enemyOrdnanceCanIntercept=function(q){return q?._sj98Owner?false:SJ98.base.intercept.apply(this,arguments);};
drawCombatFinalProjectile=function(q){if(q?._sj98Owner)return sj98Blit('orb',Math.floor(q._sj98Age*18)%16,q.x,q.y);return SJ98.base.projectile.apply(this,arguments);};
function sj98Contact(a,old){if(!sj98Foreground(a)||!['bite','breach'].includes(a.phase))return;const p=sj98Socket(a,'heart');for(const seat of seatList())withSeat(seat,()=>{if(!a.hits.has(seat)&&!player.dead&&s81003Distance(player.x,player.y,{x:old.x,y:old.y,ex:p.x,ey:p.y})<26){a.hits.add(seat);playerHit('Sumpjaw bite');sj98Log('bite-contact',{actor:a.i,seat});}});}
function sj98Tick(b,dt){const G=b._sj98;b.t+=dt;G.clock+=dt;G.rest-=dt*(ng27On()?1.15:1);
 if(!sj98Ready())return;
 for(const a of G.actors){a.clock+=dt;a.flash=Math.max(0,a.flash-dt);if(a.dead){a.dying+=dt;
  for(let j=0;j<5;j++)if(a.dying>=.18+j*.18&&!(a.deathBits&(1<<j))){a.deathBits=(a.deathBits||0)|(1<<j);explode(a.x+(j%2?36:-36),a.y-54+j*22,35,'green');}
  if(a.dying>=1.1&&!a.shattered){a.shattered=true;for(let j=0;j<9;j++)G.fragments.push({f:j,x:a.x+(j%3-1)*64,y:a.y+(Math.floor(j/3)-1)*64,vx:(j%3-1)*95,vy:-65+Math.floor(j/3)*50,t:0});}continue;}
  a.home.x=camLeftX()+viewW()/2+(a.i?1:-1)*124;
  const old=sj98Socket(a,'heart');a.t+=dt;
  if(a.phase==='entry'){a.frame=24+Math.min(23,Math.floor(a.t/.95*24));if(a.t>=1.15+a.i*.25){a.phase='recover';a.t=0;}continue;}
  if(a.phase==='recover'||a.phase==='stun'){sj98Move(a,a.home.x+Math.sin(a.clock*.9+a.i*Math.PI)*12,a.home.y+Math.sin(a.clock*1.1+a.i)*8,95,dt);a.frame=Math.floor(a.clock*15)%16;
   if(a.t>=1.1)a.phase='idle';}
  else if(a.phase==='idle'){sj98Move(a,a.home.x+Math.sin(a.clock*.9+a.i*Math.PI)*12,a.home.y+Math.sin(a.clock*1.1+a.i)*8,55,dt);a.frame=Math.floor(a.clock*15)%16;}
  else if(a.phase==='dive'){a.frame=47-Math.min(23,Math.floor(a.t/.55*24));if(a.t>=.55){a.phase='warn';a.t=0;}}
  else if(a.phase==='warn'){a.frame=16+Math.min(7,Math.floor(a.t/a.warn*8));sj98Tell(a,a.t,a.warn);
   if(a.attack==='breach'){if(a.t<a.warn*.42)a.land=sj98Target(a);a.x=a.land.x-(a.flip?-1:1)*SJ98_ART.banks.body0.poses[47].mouth[0];a.y=a.land.y-SJ98_ART.banks.body0.poses[47].mouth[1];}
   if(a.t>=a.warn){a.t=0;a.phase=a.attack;a.from={x:a.x,y:a.y};a.to=a.attack==='bite'?{x:a.target.x-(a.flip?-1:1)*sj98Pose(a).mouth[0],y:a.target.y-sj98Pose(a).mouth[1]}:{...a.from};a.emitted=0;combatAudio0927(a,a.attack==='lob'?'combatToxic0927':'jetDash',.1);sj98Log('release',{actor:a.i,kind:a.attack});}}
  else if(a.phase==='breach'){a.frame=24+Math.min(23,Math.floor(a.t/.55*24));if(a.t>=.80){shake=Math.max(shake,3);combatAudio0927(a,'hammerImpact',.15);sj98End(b,a);}}
  else if(a.phase==='bite'){a.frame=16+Math.min(7,Math.floor(a.t/.45*8));const u=clamp(a.t/.45,0,1);a.x=lerp(a.from.x,a.to.x,u*u);a.y=lerp(a.from.y,a.to.y,u*u);if(a.t>.62)sj98End(b,a);}
  else if(a.phase==='lob'){a.frame=16+Math.floor(a.t*10)%8;while(a.emitted<3&&a.t>=a.emitted*.38){sj98Lob(b,a,a.emitted++);}if(a.t>1.8)sj98End(b,a);}
  if(['idle','recover','stun'].includes(a.phase)){const p=sj98Pose(a),lo=a.flip?-p.bounds[2]:p.bounds[0],hi=a.flip?-p.bounds[0]:p.bounds[2],mid=camLeftX()+viewW()/2;a.x=clamp(a.x,(a.i?mid+12:camLeftX()+12)-lo,(a.i?camRightX()-12:mid-12)-hi);}
  sj98Contact(a,old);
 }
 if(!b.dead&&!G.owner&&G.rest<=0){const alive=G.actors.filter(a=>!a.dead&&a.phase==='idle');const a=alive.find(a=>a.i===G.turn)||alive[0];if(a){G.turn=1-a.i;sj98Start(b,a);}}
 for(const F of G.flights){if(F.a.dead){F.dead=true;continue;}F.t+=dt;const u=clamp(F.t/F.life,0,1);F.x=lerp(F.from.x,F.target.x,u);F.y=lerp(F.from.y,F.target.y,u)-Math.sin(u*Math.PI)*F.arc;if(u>=1){F.dead=true;sj98Splash(b,F);}}
 G.flights=G.flights.filter(f=>!f.dead);for(const f of G.fx)f.t+=dt;G.fx=G.fx.filter(f=>f.t<.55&&!f.a.dead);
 for(const q of eBullets)if(q._sj98Owner===b){q._sj98Age+=dt;if(q._sj98Age>2.25||q._sj98Actor.dead||b.dead)q.dead=true;}
 for(const f of G.fragments){f.t+=dt;f.x+=f.vx*dt;f.y+=f.vy*dt;f.vy+=180*dt;}G.fragments=G.fragments.filter(f=>f.t<.85);
 if(b.dead){b.dying+=dt;if(b.dying>=2.4&&!G.rewarded){G.rewarded=true;continueRewardResolve(b,b.x,VH*.4,'miniboss');dropPowerup(b.x,VH*.4,'weapon');run.score+=5200;subBoss=null;subBossActive=false;subBossDone=true;sj98Log('progression');}}
 sj98Sync(b);
}
updateSubBoss=function(dt){return sj98Own(subBoss)?sj98Tick(subBoss,dt):SJ98.base.tick.apply(this,arguments);};
function sj98Retina(x,y,t,life){const u=clamp(t/life,0,1),f=u<.35?Math.min(7,Math.floor(u/.35*8)):u<.72?8+Math.min(7,Math.floor((u-.35)/.37*8)):16+Math.floor(t*22)%8;sj98Blit('retina',f,x,y);}
function sj98Draw(b){const G=b._sj98;
 for(const F of G.flights)sj98Retina(F.target.x,F.target.y,F.t,F.life);
 for(const a of G.actors){if(a.phase==='warn'&&['breach','bite'].includes(a.attack)){const p=a.attack==='breach'?a.land:a.target;sj98Retina(p.x,p.y,a.t,a.warn);}}
 for(const a of G.actors){if(a.dead&&a.dying>=1.1)continue;if(a.phase==='warn'&&a.attack==='breach')continue;
  const state=sj98State(a),hot=!a.dead&&['warn','lob'].includes(a.phase),name=(a.flash>0||a.dead&&Math.floor(a.dying*20)%2?'hit':hot?'hot':'body')+state;
  sj98Blit(name,a.frame,a.x+(a.dead?Math.floor(Math.sin(a.dying*61)*2):0),a.y,a.flip);
 }
 for(const f of G.fragments)sj98Blit('fragment',f.f,f.x,f.y);
 for(const F of G.flights)sj98Blit('orb',Math.floor(F.t*20)%16,F.x,F.y);
 for(const f of G.fx)sj98Blit('splash',Math.min(15,Math.floor(f.t/.55*16)),f.x,f.y);
 for(const a of G.actors){if(a.dead)continue;const p=sj98Pose(a),top=a.y+p.bounds[1],x=clamp(a.x,camLeftX()+85,camRightX()-85),y=Math.max(34,top-21);
  sj98Blit('health_frame',0,x,y);sj98Blit('health_fill',0,x-72,y+5,false,Math.ceil(144*a.hp/a.maxhp));pm27Draw(ctx,'SUMPJAW '+(a.i+1),x,y-5,8,{family:'command',palette:'toxic',width:130});
 }
}
drawSubBoss=function(){if(sj98Own(subBoss))return sj98Draw(subBoss);return SJ98.base.draw.apply(this,arguments);};
beginStage=function(){SJ98.events=[];return SJ98.base.begin.apply(this,arguments);};
globalThis.BOF_SUMPJAW_DUO_1031={state:SJ98,init:sj98Init};
