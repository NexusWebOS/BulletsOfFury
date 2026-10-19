"use strict";
/* Native combat repairs: the Hammer earns his recovery, and early aircraft
   have finite, warned gun/missile roles. All pictures remain authored art. */
const CR17={base:{damage:hammerBossDamage,tick:hammerBossTick,rage:fb2HammerRageDone,
 break:hammerRecoveryBreak,begin:beginStage,start:startRun,launch:drawLaunch,
 story:BOFCampaignStory.start,cinemaDraw:BOFCinematicDirector.draw},sewerStarts:0};
function cr17Hammer(b){return run.stage===5&&b===boss&&!!fb1002NormalHammer(b)&&!b._knight1005;}
function cr17Guard(b){const h=b._hammer;if(!h._cr17||h._cr17.max!==b.maxhp)
 h._cr17={max:b.maxhp,tokens:b.maxhp*.018,recoveryDone:false,limited:0,spent:0};return h._cr17;}
hammerBossTick=function(b,dt){if(!cr17Hammer(b))return CR17.base.tick.apply(this,arguments);
 const h=b._hammer,prior=h.state,G=cr17Guard(b),punish=/stun|exposed/.test(prior);
 G.tokens=Math.min(b.maxhp*.018,G.tokens+Math.max(0,dt)*b.maxhp*[.034,.030,.027,.024][vp12Tier()]*(punish?2.2:1));
 const r=CR17.base.tick.apply(this,arguments),R=h.recovery;
 if(R?.status==='complete'||R?.status==='cancelled'&&R._hc17?.hits>=R._hc17?.required)cr17Guard(b).recoveryDone=true;
 return r;
};
hammerRecoveryBreak=function(b){if(cr17Hammer(b)&&b._hammer.recovery?._hc17?.hits>=b._hammer.recovery?._hc17?.required)
 cr17Guard(b).recoveryDone=true;return CR17.base.break.apply(this,arguments);};
fb2HammerRageDone=function(b){if(!CR17.base.rage.apply(this,arguments))return false;
 return !cr17Hammer(b)||cr17Guard(b).recoveryDone;};
hammerBossDamage=function(b,dmg){if(!cr17Hammer(b))return CR17.base.damage.apply(this,arguments);
 const G=cr17Guard(b),h=b._hammer,q=_dmgBullet,auto=q&&['spaceLaser','spaceVolley'].includes(q.kind),A=fr27Armor(b);
 let amount=dmg;
 // Both barrels, all six pulses, Akimbo and the passive rack share ONE budget.
 // No global weapon nerf: ordinary enemies and deliberate counters keep their damage.
 if(auto&&h.recovery?.status!=='charging'&&dmg>0){amount=Math.min(dmg,G.tokens);
  if(amount<dmg)G.limited++;
  if(amount<=.0001){if(!b._noHit){markHit(b);b._hammerModuleHit=null;}return 0;}}
 const before=(A?.hp||0)+(h.hammerHP||0)+(h.chainHP||0),out=CR17.base.damage.call(this,b,amount),
  absorbed=Math.max(0,before-((A?.hp||0)+(h.hammerHP||0)+(h.chainHP||0)));
 if(auto){const spent=Math.min(amount,Math.max(0,out)+absorbed);G.tokens=Math.max(0,G.tokens-spent);G.spent+=spent;}
 return out>0&&!fb2HammerRageDone(b)?Math.min(out,Math.max(0,b.hp-fb2HammerFloor(b))):out;
};

const AIR17={serial:0,clock:0,nextTell:0,owner:null,shots:0,events:[],draws:{},
 base:{volc:volcTick,ice:s3IceTick,chase:s4ChaseTick,jet:ac10Jet,play:updatePlay,
 draw:drawEnemy,bullets:drawBullets,shot:eShootT,plain:eShoot,projectile:er26ProjectileDraw,
 element:enemyOrdnanceElement,timing:vp12FireTiming},
 profiles:[
  {tell:1.05,rest:2.2,rounds:2,gap:.22,speed:2.7,slots:1,cap:70},
  {tell:.88,rest:1.7,rounds:3,gap:.19,speed:3.0,slots:2,cap:90},
  {tell:.76,rest:1.25,rounds:4,gap:.16,speed:3.3,slots:2,cap:112},
  {tell:.66,rest:.90,rounds:6,gap:.13,speed:3.55,slots:3,cap:136}
 ]};
function air17Log(event,e,data={}){AIR17.events.push({event,stage:run.stage,type:e.type,time:AIR17.clock,...data});if(AIR17.events.length>200)AIR17.events.shift();}
function air17Owns(e){return run.stage===2&&(e._af10Jet||e._fireJet1002||e.type==='lance')||
 run.stage===3&&(e._af10Jet||e.type==='s3interceptor')||run.stage===4&&['s4interceptor','s4rocket'].includes(e.type);}
function air17Live(e){return !!e&&!e.dead&&e._dyingT==null&&e.hp>0;}
function air17Blocked(e){return state!==GS.PLAY||!!story||bossActive||subBossActive||warnT>0||
 !air17Live(e)||e._noHit||e._frozen||e._mercuryLock>0||e._shieldStun>0||e._stagger>0||e._eshStun;}
function air17Ports(e){
 if(e._modJet)return [-1,1].filter(side=>!e._r30||e._r30[side<0?'left':'right'].hp>0).map(side=>modularJetPoint(e,side)).filter(p=>!p._disabled);
 const half=e._af10Jet?27:e._vp12?14:Math.min(18,e.w*.25),y=e.y+(e._af10Jet?30:Math.min(22,e.h*.28));
 return [{x:e.x-half,y},{x:e.x+half,y}];
}
function air17State(e){if(!e._air17){const slot=e._vp12?.q.slot??AIR17.serial++,stage=run.stage;
 e._air17={stage,age:0,t:0,phase:'entry',cycle:0,shot:0,delay:(slot%4)*.15,
  role:slot%3===2?'rocketeer':'gunner',element:stage===2?'fire':stage===3?'ice':stage===4&&e._vp12?'lightning':null};
 air17Log('role',e,{role:e._air17.role});}return e._air17;}
function air17DrawProjectile(q){if(!q._air17Element)return false;
 const a=EA11_ART.banks[q._air17Element+'_'+(q._air17Missile?'missile':'round')];if(!a)return false;
 if(!XART.rdy(a.key))return true;
 const r=ea11Frame(a,q.t||0),height=q._air17Missile?34:18,k=height/a.bodyHeight;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(q.x,q.y);ctx.rotate(Math.atan2(q.vy,q.vx)+Math.PI/2);
 ctx.drawImage(XART.get(a.key),...r,-a.pivot[0]*k,-a.pivot[1]*k,r[2]*k,r[3]*k);ctx.restore();
 const id=q._air17Element+(q._air17Missile?'/missile':'/round');AIR17.draws[id]=(AIR17.draws[id]||0)+1;return true;
}
er26ProjectileDraw=function(q){return air17DrawProjectile(q)||AIR17.base.projectile.apply(this,arguments);};
drawBullets=function(){const all=eBullets,owned=all.filter(q=>q._air17Element&&!q.dead);
 if(!owned.length)return AIR17.base.bullets.apply(this,arguments);
 const set=new Set(owned);eBullets=all.filter(q=>!set.has(q));
 try{AIR17.base.bullets.apply(this,arguments);}finally{eBullets=all;}
 for(const q of owned)air17DrawProjectile(q);
};
enemyOrdnanceElement=function(q){if(q?._air17Element)return null;return AIR17.base.element.apply(this,arguments);};
function air17Emit(e){const C=e._air17,P=AIR17.profiles[vp12Tier()],ports=air17Ports(e);if(!ports.length||eBullets.length>=P.cap)return;
 const missile=C.missile,offsets=!missile&&C.element==='ice'&&C.cycle%2===0?[-.18,.18]:[0];
 for(let side=0;side<ports.length;side++){if(missile&&side!==C.shot%ports.length)continue;const p=ports[side],a=Math.atan2(C.target.y-p.y,C.target.x-p.x);
  for(const off of offsets){const kind=missile?'emissile':C.element==='fire'?'s2needle':C.element==='ice'?'s3shard':run.stage===4?'s4brass':'mg',
   b=eShootT(p.x,p.y,a+off,missile?2.5+vp12Tier()*.2:P.speed,kind,{owner:e,noMuzzle:true,silent:true,w:missile?10:6,h:missile?24:12});
   if(!b||b.dead)continue;Object.assign(b,{_air17Owner:e,_air17Element:C.element,_air17Missile:missile,_committed:true,homing:false,_noArsenal:true});
   if(missile){b.hp=vp12Tier()>=2?2:1;b._shootable=true;b._weaponProof=false;b._s4Accel=.8;b._s4Max=5.4;}
   else{b._weaponProof=true;b._shootable=false;delete b.hp;}
   AIR17.shots++;
  }
  if(run.stage===2)stage2Muzzle(e,side? .28:-.28,.30,.6,.10);
  else if(run.stage===3)stage3Muzzle(e,side? .28:-.28,.30,.6,.10);
  else if(e._modJet){e._modJetFireSide=side?1:-1;stage4Muzzle(e,side?.30:-.30,.30,.6,.10,MUZZLE_MG);}
 }
 if(missile)Audio.SFX.enemyMissile?.();else if(C.element==='lightning')Audio.SFX.enemyElectricBolt?.();else Audio.SFX.enemyMachineGunHeavy?.();
 air17Log(missile?'missile':'burst',e,{element:C.element,cycle:C.cycle});
}
function air17Tick(e,dt){const C=air17State(e),P=AIR17.profiles[vp12Tier()];C.age+=dt;
 if(air17Blocked(e)){C.phase='entry';C.t=0;return;}
 const T=targetShip(e.x,e.y),inView=e.x>camLeftX()+24&&e.x<camRightX()-24&&e.y>PLAY.y+24&&e.y<PLAY.y+PLAY.h*.67,
  room=T&&!T.dead&&!T.out&&Math.hypot(T.x-e.x,T.y-e.y)>140;
 if(!inView||!T||T.dead||T.out||!air17Ports(e).length||!room&&!['tell','fire'].includes(C.phase)){C.phase='entry';C.t=0;return;}
 C.t+=dt;
 if(C.phase==='entry'||C.phase==='recover'){
  const wait=C.phase==='entry'?.22+C.delay:P.rest;
  const busy=enemies.filter(o=>o!==e&&air17Live(o)&&['tell','fire'].includes(o._air17?.phase)).length;
  if(C.t>=wait&&busy<P.slots&&AIR17.clock>=AIR17.nextTell&&eBullets.length<P.cap-16){
   C.target={x:T.x,y:T.y};C.missile=C.role==='rocketeer'||C.cycle%3===2;
   C.phase='tell';C.t=0;C.shot=0;C.beat=0;C.cycle++;AIR17.nextTell=AIR17.clock+.20;
   air17Log('tell',e,{missile:C.missile,warm:P.tell,target:C.target});
  }
 }else if(C.phase==='tell'){
  combatWarningTick(e,'air17-'+C.cycle,C.t,P.tell);
  if(C.t>=P.tell){C.phase='fire';C.t=0;C.beat=0;air17Log('release',e);}
 }else if(C.phase==='fire'){
  const count=C.missile?(vp12Tier()>=2?3:2):P.rounds;
  C.beat-=dt;if(C.beat<=0&&C.shot<count){air17Emit(e);C.shot++;C.beat=C.missile?.26:P.gap;}
  if(C.shot>=count&&C.beat<=0){C.phase='recover';C.t=0;}
 }
}
function air17Flight(e,dt){const C=air17State(e);delete e._ac10Ram;e.shoots=e.armed=false;e.fireCd=999;
 if(ep13Suppressed(e)){air17Tick(e,dt);return;}
 if(e._af10Jet){e._af10Jet.phase='combat';e._af10Jet.t+=dt;}
 const top=PLAY.y+PLAY.h*.23;if(e.y<top)e.y+=115*dt;
 else if(C.age<10.5){const dir=C.role==='rocketeer'?-1:1,tx=clamp(worldWidth()/2+Math.sin(C.age*.85+e.x*.001)*viewW()*.25*dir,camLeftX()+70,camRightX()-70);
  const dx=clamp(tx-e.x,-70*dt,70*dt);e.x+=dx;e.y=top+Math.sin(C.age*1.2)*14;e.spin=clamp(dx/Math.max(dt,1e-5)/250,-.27,.27);
 }else{e.y+=160*dt;e.x+=(C.role==='rocketeer'?-38:38)*dt;if(e.y>VH+110)e.dead=true;}
 air17Tick(e,dt);
}
ac10Jet=function(e,dt){if(air17Owns(e))return air17Flight(e,dt);return AIR17.base.jet.apply(this,arguments);};
volcTick=function(e,dt){if(air17Owns(e))return air17Flight(e,dt);return AIR17.base.volc.apply(this,arguments);};
s3IceTick=function(e,dt){if(air17Owns(e))return air17Flight(e,dt);return AIR17.base.ice.apply(this,arguments);};
// Keep the highway aircraft's authored route and destructible gun mounts.
// Its guns have exactly one attack owner, rather than two stacked schedulers.
s4ChaseTick=function(e,dt){if(!air17Owns(e))return AIR17.base.chase.apply(this,arguments);
 const C=air17State(e);if(C.age>11.5)e._egress=1;
 e._s4Act=null;e._fcd=999;e.fireCd=999;const prev=AIR17.owner;AIR17.owner=e;
 const committing=e.type==='s4interceptor'&&['tell','fire'].includes(C.phase)||
  window.AC19_OFF!==1&&e.type==='s4rocket'&&['entry','tell','fire'].includes(C.phase)&&
  e.x>camLeftX()+24&&e.x<camRightX()-24&&e.y>PLAY.y+24&&e.y<PLAY.y+PLAY.h*.67;
 try{AIR17.base.chase.call(this,e,dt*(committing?.30:1));}finally{AIR17.owner=prev;}
 e._s4Act=null;air17Tick(e,dt);
};
eShootT=function(x,y,a,speed,kind,opts){if(AIR17.owner)return {dead:true,x,y,vx:0,vy:0};return AIR17.base.shot.apply(this,arguments);};
eShoot=function(x,y){if(AIR17.owner)return;return AIR17.base.plain.apply(this,arguments);};
vp12FireTiming=function(g,q){return g._air17?{tell:0,release:999,gap:999}:AIR17.base.timing.apply(this,arguments);};
updatePlay=function(dt){if(state===GS.PLAY&&!story)AIR17.clock+=Math.max(0,dt);
 for(const g of VP12.groups)if([1,4].includes(g.stage)&&!['kamikaze','barrel','peel-bomb'].includes(g.type))g._air17=true;
 const r=AIR17.base.play.apply(this,arguments);
 for(const e of enemies)if(e._vp12?.g._air17&&air17Live(e))air17Tick(e,dt);return r;
};
drawEnemy=function(e){const r=AIR17.base.draw.apply(this,arguments),C=e._air17;if(!air17Live(e)||C?.phase!=='tell'||e._noHit)return r;
 const P=AIR17.profiles[vp12Tier()],ports=air17Ports(e);
 const offsets=!C.missile&&C.element==='ice'&&C.cycle%2===0?[-.18,.18]:[0];let lane=0;
 for(const p of ports)for(const off of offsets){const a=Math.atan2(C.target.y-p.y,C.target.x-p.x)+off;
  combatWarningDraw(e,{...p,ex:p.x+Math.cos(a)*900,ey:p.y+Math.sin(a)*900,width:C.missile?24:16,
   progress:clamp(C.t/P.tell,0,1),fieldOnly:lane++>0});}return r;
};

/* The river/bridge/sewer approach was a post-Stage6 scene. Alternate routes
   could skip that owner completely. Stage7 now catches any unseen approach,
   then rejoins its existing top-down connector and native pilot sprite. */
function cr17Approach(){const pk=_pilotKey(),name=(PILOTS.find(p=>p.key===pk)?.name||pk).toUpperCase();
 return [
  {who:'DECKER',text:'The alien signal is below the city. Take us down along the river.',bg:'cin_story_city_descent',flight:'descent'},
  {who:'SHIP SYSTEM',text:'Low altitude confirmed. Following the river toward the iron bridge.',bg:'cin_story_river_high',flight:'river'},
  {who:name,text:'Bridge ahead. Staying low. The signal is on the far bank.',bg:'cin_story_river_bridge',flight:'bridge'},
  {who:'DECKER',text:'That sewer access is the source. We never searched underground.',bg:'cin_story_riverbank_sewer',flight:'approach'},
  {who:name,text:'Taking the lower access tunnel. Keep listening for us.',bg:'cin_stage07_topdown',flight:'enter'}
 ].map(b=>({...b,duration:5.2,_sewer17:true}));
}
function cr17WarmApproach(){for(const b of cr17Approach())XART.rdy(b.bg);XART.rdy('ship_'+_pilotKey());for(let i=0;i<4;i++)XART.rdy('nthp_'+_pilotKey()+'_'+i);}
BOFCampaignStory.start=function(stage,done){if(stage!==6)return CR17.base.story.apply(this,arguments);
 if(run.mode!=='campaign')return false;cr17WarmApproach();
 const rows=BOFCinematicDirector.script(6),cut=rows.findIndex(b=>b.bg==='cin_story_city_descent'),
  r=BOFCinematicDirector.play('post-6',[...rows.slice(0,cut<0?rows.length:cut),...cr17Approach()],done);
 if(r)run._sewerBriefed17=true;return r;};
BOFCinematicDirector.draw=function(){const s=BOFCinematicDirector.current,b=s?.beats?.[s.i];
 if(!b?._sewer17)return CR17.base.cinemaDraw.apply(this,arguments);
 CR17.base.cinemaDraw.apply(this,arguments);
 const W=cutsceneViewWidth(),u=clamp(s.t/(b.duration||5.2),0,1),ease=u*u*(3-2*u),
  y=VH*lerp(.54,b.flight==='enter'?.24:.43,ease),size=VH*lerp(.20,b.flight==='enter'?.075:.17,ease);
 ctx.save();ctx.imageSmoothingEnabled=false;
 const key=_shipK('');if(key){const im=XART.get(key),w=size*im.width/im.height;
  const frame=player._thrustFrame;player._thrustFrame=s.age*18;
  try{pf27PlaneThrustDraw(ctx,key,W*.5,y,w,size,.65);}finally{player._thrustFrame=frame;}
  drawShipSprite(W*.5,y,size,'');}
 ctx.restore();
};
startRun=function(){run._sewerBriefed17=false;return CR17.base.start.apply(this,arguments);};
drawLaunch=function(dt){if(run.stage===7&&run.mode==='campaign'&&!run._sewerBriefed17){
  cr17WarmApproach();if(BOFCinematicDirector.play('stage7-approach',cr17Approach(),()=>{setState(GS.LAUNCH);})){run._sewerBriefed17=true;CR17.sewerStarts++;return;}
 }return CR17.base.launch.apply(this,arguments);};
beginStage=function(n){AIR17.serial=0;AIR17.clock=0;AIR17.nextTell=0;AIR17.events=[];AIR17.shots=0;AIR17.draws={};
 return CR17.base.begin.apply(this,arguments);};
window.BOF_COMBAT_REVISION={hammer:cr17Guard,air:AIR17,state:CR17};
