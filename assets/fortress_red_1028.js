'use strict';
/* Stage6 miniboss: eight physical modules, passive turbines, laser batteries,
   then authored red 1015-pulse lightning. Main Harrier ownership is untouched. */
const S6F28={events:[],base:{budget:sc13FinalizeBudget,at:sc13At,continuous:sc13ContinuousAt,
 area:sc13AreaTarget,damage:warhiveDamage,targets:retinaBossTargets,rocket:sc13RocketStart,
 down:s6r18PartsDown,open:sc13Open,tick:warhiveTick,coreDraw:s6r18CoreDraw,due:bh25Due,
 projectile:drawStage4WarfareProjectile,final:drawCombatFinalProjectile,clear:sc13Clear,
 intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,load:stageLoadBegin,say:s6WingSay}};
const S6F28_ART={hull:[1024,512,1,1],fans:[128,128,16,8],fan_hit:[128,128,1,1],fan_wreck:[128,128,1,1],
 red_bolts:[152,152,256,16],red_orbs:[72,72,16,8],red_core:[50,108,12,6],core_hit:[50,108,12,6],
 fan_smoke:[96,144,8,8],fan_fire:[64,64,8,8]};
for(const k of Object.keys(S6F28_ART))XART._src['s6f28_'+k]='assets/game/levels/stage_06/miniboss/fortress_red_1028/'+k+'.png';
function s6f28Own(b){return !!b?._cargo17Mini&&!!b._cargo13&&run.stage===6&&!run._gp4StageX;}
function s6f28Log(b,event,data={}){S6F28.events.push({event,time:b.t,...data});if(S6F28.events.length>600)S6F28.events.shift();}
s6WingSay=function(who,line){if(s6f28Own(subBoss)&&typeof line==='string')line=line
 .replace('TAKE OUT TWO BATTERIES! THAT WILL EXPOSE THE REACTOR.','DESTROY BOTH FANS AND ALL SIX LASER BATTERIES TO OPEN THE REACTOR.')
 .replace('DESTROY ALL SIX LASER BATTERIES TO OPEN THE REACTOR.','DESTROY BOTH FANS AND ALL SIX LASER BATTERIES TO OPEN THE REACTOR.')
 .replace('ALL WEAPONS DOWN. THE REACTOR HATCH IS OPENING!','ALL EIGHT MODULES DOWN. THE REACTOR HATCH IS OPENING!');return S6F28.base.say.call(this,who,line);};
stageLoadBegin=function(n,keys){if(n===6)Snd.prepare?.(['geyserLightning','element_lightning_hit']);
 return S6F28.base.load.call(this,n,n===6?[...(keys||[]),...Object.keys(S6F28_ART).map(k=>'s6f28_'+k)]:keys);};
sc13FinalizeBudget=function(b){if(!s6f28Own(b))return S6F28.base.budget.apply(this,arguments);
 const C=b._cargo13;if(C.s6f28Budget)return;C.s6f28Budget=true;C.budgetFinalized=true;
 const total=Math.round(b.maxhp),gun=Math.max(1,Math.floor(total*.075)),fan=Math.max(1,Math.floor(total*.10));
 C.fans=[-1,1].map((side,i)=>({id:'fan'+i,side,hp:fan,maxhp:fan,dead:false,fl:0,flash:0}));
 for(const g of C.guns){g.hp=g.maxhp=gun;g.dead=false;}
 C.core=C.maxCore=total-gun*6-fan*2;b.hp=b.maxhp=total;sc13Sync(b);
 s6f28Log(b,'budget',{total,gun,fan,core:C.core});};
function s6f28FanMount(b,f){const C=b._cargo13,s=sc13Scale(b);return{x:C.x+f.side*384*s,y:C.y-44*s};}
function s6f28Parts(b){const C=b._cargo13;return[...C.guns,...(C.fans||[])];}
function s6f28Point(b,p){return typeof p.id==='number'?sc13Mount(b,p.id):s6f28FanMount(b,p);}
s6r18PartsDown=function(b){return s6f28Own(b)?s6f28Parts(b).length===8&&s6f28Parts(b).every(p=>p.dead):S6F28.base.down.apply(this,arguments);};
sc13Open=function(b){return s6f28Own(b)?s6r18PartsDown(b)&&s6r18State(b).open>=.999:S6F28.base.open.apply(this,arguments);};
function s6f28Ready(b){return !b.dead&&b._cargo13.ready&&b._cargo13.mode!=='arrive';}
sc13At=function(b,x,y){if(!s6f28Own(b))return S6F28.base.at.apply(this,arguments);if(!s6f28Ready(b))return null;
 const C=b._cargo13,s=sc13Scale(b);
 for(const f of C.fans||[])if(!f.dead){const p=s6f28FanMount(b,f);if(Math.hypot(x-p.x,y-p.y)<44*s+4)return f.id;}
 for(const g of C.guns)if(!g.dead){const p=sc13Mount(b,g.id);if(Math.abs(x-p.x)<18&&y>p.y-19&&y<p.y+37)return g.id;}
 // The sealed body never consumes a primary round on its way to a turbine.
 if(sc13Open(b)){const p=sc13Core(b);if(Math.abs(x-p.x)<35&&Math.abs(y-p.y)<52)return 'core';}return null;};
sc13ContinuousAt=function(b,q){if(!s6f28Own(b))return S6F28.base.continuous.apply(this,arguments);if(!s6f28Ready(b))return null;
 const s=sc13Scale(b),hits=[],touch=(p,w,h)=>q.kind==='flame'?flameHit(q,p.x,p.y,w,h):Math.abs(q.x-p.x)<w/2+(q.w||1)/2&&p.y+h/2>q.top&&p.y-h/2<q.bot;
 for(const g of s6f28Parts(b))if(!g.dead){const p=s6f28Point(b,g),fan=typeof g.id==='string';if(!fan)p.y+=9;
  if(touch(p,fan?88*s:36,fan?88*s:56))hits.push({id:g.id,x:p.x});}
 if(hits.length){hits.sort((a,c)=>Math.abs(a.x-q.x)-Math.abs(c.x-q.x));return hits[0].id;}
 return sc13Open(b)&&touch(sc13Core(b),70,104)?'core':null;};
sc13AreaTarget=function(b,x){if(!s6f28Own(b))return S6F28.base.area.apply(this,arguments);if(sc13Open(b))return 'core';
 const live=s6f28Parts(b).filter(p=>!p.dead).sort((a,c)=>Math.abs(s6f28Point(b,a).x-x)-Math.abs(s6f28Point(b,c).x-x));return live[0]?.id??null;};
warhiveDamage=function(b,dmg){if(!s6f28Own(b))return S6F28.base.damage.apply(this,arguments);
 sc13FinalizeBudget(b);if(!s6f28Ready(b))return 0;const C=b._cargo13,q=typeof _dmgBullet!=='undefined'?_dmgBullet:null,direct=C.directId;C.directId=null;C.hit=null;
 let id=direct!=null?direct:q&&(q.kind==='beam'||q.kind==='flame')?sc13ContinuousAt(b,q):q&&Number.isFinite(q.x+q.y)?sc13At(b,q.x,q.y):sc13AreaTarget(b,player.x);
 if(id==null)return 0;dmg=Math.max(0,Number(dmg)||0);if(!dmg)return 0;let dealt=0;
 if(id==='core'){if(!sc13Open(b))return 0;dealt=Math.min(C.core,dmg);C.core-=dealt;C.coreFl=.12;markHit(b);}
 else{const p=s6f28Parts(b).find(p=>p.id===id);if(!p||p.dead)return 0;dealt=Math.min(p.hp,dmg);p.hp-=dealt;p.fl=.12;markHit(p);
  if(p.hp===0){p.dead=true;p.pose=3;C.queue=C.queue.filter(q=>q.id!==id);C.lasers=C.lasers.filter(q=>q.id!==id);
   const m=s6f28Point(b,p);explode(m.x,m.y,58,'red',null,'nxp_barrage');sc13Sound('expBig',.50);SC13.stats.modules++;s6f28Log(b,'module-destroyed',{id});}}
 weaponHitSfx('normal');if(typeof stageStats!=='undefined')stageStats.dmgDealt+=dealt;
 b.hp=C.core+s6f28Parts(b).reduce((n,p)=>n+p.hp,0);sc13Sync(b);
 if(C.core<=0){b.hp=0;sc13Clear(b);bossDie();}return 0;};
retinaBossTargets=function(b){if(!s6f28Own(b))return S6F28.base.targets.apply(this,arguments);sc13FinalizeBudget(b);if(!s6f28Ready(b))return[];
 const C=b._cargo13,s=sc13Scale(b),a=[];
 for(const p of s6f28Parts(b))if(!p.dead){const fan=typeof p.id==='string';a.push(retinaDynamicPiece(b,'fortress '+p.id,fan?'passive turbine':'laser battery',()=>({...s6f28Point(b,p),hp:p.hp,dead:p.dead||b.dead}),d=>{C.directId=p.id;hitSubBoss(d);},fan?88*s:38,fan?88*s:56));}
 if(sc13Open(b))a.push(retinaDynamicPiece(b,'fortress reactor','reactor',()=>({...sc13Core(b),hp:C.core,dead:b.dead}),d=>{C.directId='core';hitSubBoss(d);},68,96));return a;};
sc13RocketStart=function(b){if(!s6f28Own(b))return S6F28.base.rocket.apply(this,arguments);const C=b._cargo13;C.rockets=null;C.mode='recover';C.rest=C.cfg.rest;};
bh25Due=function(b,key){if(s6f28Own(b)&&key==='fortress-core')return false;return S6F28.base.due.apply(this,arguments);};
// One attack owner. Both books originate at the moving exposed aperture.
const S6F28_REACTOR_BASE=er23Fortress;
er23Fortress=function(b,dt){if(!s6f28Own(b))return S6F28_REACTOR_BASE.apply(this,arguments);
 if(b.dead||!sc13Open(b)){delete b.er23Reactor;return;}
 const A=b.er23Reactor||(b.er23Reactor={phase:'ready',t:0,seq:0});A.t+=dt;
 if(A.phase==='ready'&&A.t>.85){const m=sc13Core(b),T=targetShip(m.x,m.y);A.phase='tell';A.t=0;A.seq++;A.angle=Math.atan2(T.y-m.y,T.x-m.x);
  A.offsets=A.seq%2?[-.48,-.24,0,.24,.48]:[-.34,.34];A.warm=target17Rank()>=3?.85:1.15;combatAudio0927(b,'bossWeaponCharge',.8);}
 if(A.phase==='tell'){combatWarningTick(b,'fortress-reactor-'+A.seq,A.t,A.warm);
  if(A.t>=A.warm){const m=sc13Core(b),orb=A.seq%2===0;
   for(const off of A.offsets){const a=A.angle+off,q=stage4WarfareShot(b,m,a,orb?2.8:4.1,orb?'orb':'lightning');
    Object.assign(q,{_s6f28Owner:b,_s6f28Orb:orb,_s6f28Dir:((Math.round((a-Math.PI/2)*32/TAU)%32)+32)%32,_weaponProof:true,_s3kOriginalProof:true,_shootable:false,_sc13Owner:b});
    delete q._er26Art;s6f28Log(b,'core-projectile',{orb,x:m.x,y:m.y,angle:a});}
   combatAudio0927(b,orb?'element_lightning_hit':'geyserLightning',.45);A.phase='ready';A.t=0;}}
};
function s6f28Blit(name,frame,x,y,k=1){const a=S6F28_ART[name];if(!XART.rdy('s6f28_'+name))return false;
 frame=((frame|0)%a[2]+a[2])%a[2];const w=a[0],h=a[1];ctx.drawImage(XART.get('s6f28_'+name),frame%a[3]*w,Math.floor(frame/a[3])*h,w,h,Math.round(x-w*k/2),Math.round(y-h*k/2),w*k,h*k);return true;}
function s6f28FanDraw(b){const C=b._cargo13,s=sc13Scale(b);for(const f of C.fans||[]){const p=s6f28FanMount(b,f);
 s6f28Blit(Math.max(f.fl,f.flash)>0?'fan_hit':f.dead?'fan_wreck':'fans',f.dead?0:Math.floor(b.t*16),p.x,p.y,s);
 if(f.dead){const frame=Math.floor(b.t*10);s6f28Blit('fan_fire',frame,p.x,p.y-10);s6f28Blit('fan_smoke',frame,p.x,p.y-54);}}}
s6r18CoreDraw=function(b,x,y,height,open,flash){if(!s6f28Own(b))return S6F28.base.coreDraw.apply(this,arguments);if(open<=0)return;
 s6f28Blit(flash>0?'core_hit':'red_core',Math.floor(b.t*16),x,y,height/108);S6R18.draws.reactor++;};
function s6f28Projectile(q){if(!q?._s6f28Owner)return false;const frame=q._s6f28Orb?Math.floor(q.t*18)%16:q._s6f28Dir*8+Math.floor(q.t*20)%8;
 return s6f28Blit(q._s6f28Orb?'red_orbs':'red_bolts',frame,q.x,q.y)||true;}
drawStage4WarfareProjectile=function(q){return s6f28Projectile(q)||S6F28.base.projectile.apply(this,arguments);};
drawCombatFinalProjectile=function(q){return s6f28Projectile(q)||S6F28.base.final.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._s6f28Owner?false:S6F28.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._s6f28Owner?'lightning':S6F28.base.element.apply(this,arguments);};
warhiveTick=function(b,dt){const r=S6F28.base.tick.apply(this,arguments);if(!s6f28Own(b))return r;
 for(const f of b._cargo13.fans||[]){f.fl=Math.max(0,f.fl-dt);f.flash=Math.max(0,f.flash-dt);}return r;};
sc13Clear=function(b){const r=S6F28.base.clear.apply(this,arguments);if(s6f28Own(b)){delete b.er23Reactor;for(const q of eBullets)if(q._s6f28Owner===b)q.dead=true;}return r;};
globalThis.BOF_FORTRESS_RED_1028=S6F28;
