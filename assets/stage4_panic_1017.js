"use strict";
/* Stage 4: coordinated Warden bombing spirals and the Sovereign's committed
   final-quarter escape. Movement, warnings and releases share the same lanes;
   existing hulls, heading banks, ordnance, damage and death owners stay native. */
const P4_17={serial:0,events:[],base:{wing:wing17Tick,jet:wing17JetTick,balls:sa14Balls,
 fan:sa14FanWarning,guardFan:sg17Fan,rearm:stage4ShieldBeginRearm,war:er26WarTick,
 set:er26Set,clamp:er26DamageClamp,hit:hitBoss,draw:er26Draw,overflight:sa14Overflight}};
function p4Log(event,data={}){P4_17.events.push({event,...data});if(P4_17.events.length>240)P4_17.events.shift();}
function p4Rank(){return Math.min(3,vp12Tier());}
function p4Ease(u){u=clamp(u,0,1);return u*u*(3-2*u);}

// Preserve the lower ranks' one/two-jet rosters, now with the same return to
// orbit as the larger wings. Hard remains four; Furious / Insanity remain six.
WING17_LAYOUT.easy=['S'];WING17_LAYOUT.normal=['S','S'];
WING17_CFG.easy={spin:.55,rx:185,ry:108,every:3.4,tell:.85,rounds:4,gap:.17,speed:3.2};
WING17_CFG.normal={spin:.62,rx:195,ry:112,every:3.0,tell:.70,rounds:5,gap:.14,speed:3.6};
function p4WingRaid(b){
 const W=b._wing17,C=wing17Centre(b),live=W.slots.map(s=>s.e).filter(e=>e&&e.hp>0&&!e.dead&&e._dyingT==null&&e._wing17.t>=WING17_ENTRY);
 if(!live.length)return false;
 const target=targetShip(b.x,b.y),id=++P4_17.serial;
 W.p4Raid={id,t:0};W.p4Next=[16,14,12,10][p4Rank()];
 for(const e of live){const A=e._wing17;
  A.p4Raid={id,t:0,c:{...C},dx:e.x-C.x,dy:e.y-C.y,from:{x:e.x,y:e.y},angle:A.angle,
   sign:id%2?1:-1,bombs:0,aim:{x:target.x,y:target.y},phase:'spiral'};
  A.phase='spiral';A.shots=0;A.shot=0;
 }
 wls17Sfx('tlvJetReady');p4Log('wing-spiral',{id,jets:live.length});return true;
}
wing17Tick=function(b,dt){
 const r=P4_17.base.wing.apply(this,arguments),W=b._wing17;if(!W||b.dead)return r;
 W.p4Next??=[12,11,10,9][p4Rank()];
 if(W.p4Raid){W.p4Raid.t+=dt;
  if(!W.slots.some(s=>s.e&&!s.e.dead&&s.e._dyingT==null&&s.e._wing17.p4Raid))W.p4Raid=null;
 }else{W.p4Next-=dt;if(W.p4Next<=0&&!p4WingRaid(b))W.p4Next=.5;}
 return r;
};
function p4WingBomb(e,D){
 const rank=p4Rank(),slot=e._wing17.slot.i,pass=D.bombs++,n=wing17Layout().length;
 // Every landing site is committed at the start of the run. Spread the racks
 // around the target instead of stacking all six jets on a tracking reticle.
 const x=clamp(D.aim.x+(slot-(n-1)/2)*48+(pass%2?30:-30),camLeftX()+28,camRightX()-28);
 const y=clamp(D.aim.y+(pass-1)*48+(slot%2?22:-22),PLAY.y+90,VH-32);
 const q=groundTargetingSpawn({kind:'missile',x,y,owner:e,track:false,lane:false,
  warn:[1.85,1.65,1.50,1.40][rank],active:.48,radius:24,size:78,shake:3,
  sound:'groundBombImpact',onImpact:g=>explode(g.x,g.y,52,'red')});
 q._jetBomb={x:e.x,y:e.y};q._p4Bomb=true;q._late27=true;
 XART.rdy('lz_bomb');Audio.SFX.groundBombLock?.();
 p4Log('wing-bomb',{id:D.id,slot,pass,x,y});
}
wing17JetTick=function(e,dt){
 const A=e._wing17,D=A.p4Raid,b=A.owner;
 if(!D||!b||b.dead||b.dying||!subBossActive||subBoss!==b)return P4_17.base.jet.apply(this,arguments);
 D.t+=dt;A.t+=dt;e.vx=e.vy=0;e.fireCd=999;
 const prev={x:e.x,y:e.y},spin=2.25,hold=.55,rank=p4Rank();
 if(D.t<spin){
  const u=clamp(D.t/spin,0,1),a=D.sign*u*TAU*1.10,k=1+u*u*4.2,ca=Math.cos(a),sa=Math.sin(a);
  e.x=D.c.x+(D.dx*ca-D.dy*sa)*k;e.y=D.c.y+(D.dx*sa+D.dy*ca)*k;
  // Start exactly at the live orbit point, with real authored headings all
  // around the spiral. Once it clears the field it is no longer a body hazard.
  e._noHit=e.x<camLeftX()-48||e.x>camRightX()+48||e.y<PLAY.y-48||e.y>VH+48;
  const racks=rank<2?2:3;
  if(D.bombs<racks&&D.t>=.12+D.bombs*.38&&e.x>camLeftX()+12&&e.x<camRightX()-12&&e.y>PLAY.y&&e.y<VH-20)p4WingBomb(e,D);
  const move=Math.hypot(e.x-prev.x,e.y-prev.y);if(move>.05)A.angle=Math.atan2(e.y-prev.y,e.x-prev.x);
  A.phase='spiral';return;
 }
 if(D.t<spin+hold){A.phase='away';e._noHit=true;
  combatWarningTick(e,'p4-wing-return-'+D.id,D.t-spin,hold,true);return;}
 // Same edge, same actor and HP, same complete harmless scaling pass as its
 // original entry. Destroyed actors never reach this path or get resurrected.
 const gate=wing17Gate(b,A.slot);e.x=gate.x;e.y=gate.y;e._noHit=true;
 A.t=0;A.from=gate;A.angle=Math.atan2(wing17Centre(b).y-gate.y,wing17Centre(b).x-gate.x);
 A.phase='enter';A.next=.55+A.slot.i*.18;delete A.p4Raid;
 wls17Sfx('tlvJetThrust');p4Log('wing-return',{id:D.id,slot:A.slot.i,hp:e.hp});
};

// A complete row includes straight down the centre. Ice retains its authored
// walking gap. The same electric geometry supplies both FOVs and projectiles.
function p4BallLanes(b,behind=false){
 const count=7+p4Rank()*2,span=Math.min(b.w*.76,viewW()*.76),out=[];
 for(let i=0;i<count;i++){const u=(i-(count-1)/2)/((count-1)/2);
  out.push({x:b.x+u*span*.5,y:(b._drawY??b.y)+b.h*((behind?.30:.35)-Math.abs(u)*.08),
   angle:Math.PI/2-u*(behind?.48:.42),width:24});
 }return out;
}
function p4EmitBalls(b,lanes,final=false){
 let count=0;for(const p of lanes){
  const q=stage4WarfareShot(b,p,p.angle,2.8+p4Rank()*.35,'orb',{szMul:.7});if(q.dead)continue;
  s4ac13Mark(q);Object.assign(q,{_er26Source:b._ship,_sa14Volley:true,_sa14Electric:true,_p4FinalShot:final});count++;
 }b._er26.shots+=count;shake=Math.max(shake,4);Audio.SFX.geyserLightning?.();
 shipBossMuzzleStart(b,['C'],{fam:'lightning',life:.22,hpx:70});return count;
}
sa14Balls=function(b,ice,behind=false){
 if(ice||!sa14Storm(b))return P4_17.base.balls.apply(this,arguments);
 const n=p4EmitBalls(b,p4BallLanes(b,behind));b._er26._sa14.wave++;
 sa14Log('lightning-volley',b,{wave:b._er26._sa14.wave,gap:null,count:n,behind});return n;
};
sa14FanWarning=function(b,progress){if(!sa14Storm(b))return P4_17.base.fan.apply(this,arguments);
 for(const p of p4BallLanes(b))b._er26.warnings.push({...p,progress});
};
sg17Fan=function(b){
 const R=b._er26,T=R?._sa14;
 if(R?.mode==='sa14-overflight'&&R.t>=4.8&&T?.p4BallWarm&&T.shot>0)
  return p4BallLanes(b,true).map(p=>({...p,progress:clamp(1-T.shot/T.p4BallWarm,0,1)}));
 const old=P4_17.base.guardFan.apply(this,arguments);if(!old)return null;
 return p4BallLanes(b,b._er26.mode==='sa14-overflight').map(p=>({...p,progress:old[0].progress}));
};

const P4_FINAL_CFG={
 easy:{tell:2.40,ballGap:2.9,ballWarn:1.35,boltGap:4.8,angerWarn:1.15,mult:2.0},
 normal:{tell:2.15,ballGap:2.55,ballWarn:1.20,boltGap:4.0,angerWarn:1.05,mult:2.1},
 hard:{tell:1.95,ballGap:2.20,ballWarn:1.05,boltGap:3.5,angerWarn:.95,mult:2.2},
 furious:{tell:1.75,ballGap:1.95,ballWarn:.95,boltGap:3.0,angerWarn:.88,mult:2.3}
};
function p4FinalCfg(){return P4_FINAL_CFG[diffKey==='insanity'?'furious':diffKey]||P4_FINAL_CFG.normal;}
function p4FinalStart(b){
 if(!sa14Storm(b)||b._p4Final||b.dead||b.hp<=0||b.enter)return false;
 const R=b._er26,S=b._s4war,H=S.shield,target=targetShip(b.x,b.y);
 if(H.active||H.rearming)return false;
 const id=++P4_17.serial;
 b._p4Final={id,t:0,rearT:0,phase:'panic',from:{x:b.x,y:b.y},aim:{x:target.x,y:target.y},
  exit:{x:b.x,y:VH+b.h*.75+100},attacks:[],serial:0,ball:.12,bolt:1.45,anger:0,angerCd:0,damage:0};
 S._pt11Chase??={};S._pt11Chase.done=true;S.mode='chase';S.giantStrike=null;S.finalGuns='off';
 S.shieldThresholdIndex=S.shieldThresholds.length;
 H.active=H.rearming=false;H.breakT=0;for(const n of H.nodes){n.dead=true;n.hp=0;}
 b._ap10Storm=b._l23Beam=null;if(b._mr27)b._mr27.ram1002=null;
 P4_17.base.set.call(this,b,'sa14-final');R.mode='sa14-final';R.dur=Infinity;R.od=true;R.warnings=[];
 b._sa14.angle=0;b._sa14.scale=1;b._sa14.depth=false;Audio.SFX.bossPhase?.();
 p4Log('final-panic',{id,hp:b.hp});return true;
}
stage4ShieldBeginRearm=function(b,threshold){
 const r=P4_17.base.rearm.apply(this,arguments);
 if(sa14Storm(b)&&threshold<=.251&&b._s4war._pt11Chase)p4FinalStart(b);return r;
};
er26Set=function(b,mode){if(sa14Storm(b)&&b._p4Final&&!b.dead&&b.hp>0)return;
 const r=P4_17.base.set.apply(this,arguments);
 if(sa14Storm(b)&&mode==='sa14-overflight')b._er26._sa14.shot=b._er26._sa14.p4BallWarm=p4FinalCfg().ballWarn;
 return r;
};
sa14Overflight=function(b,dt){
 const R=b._er26,T=R._sa14;if(!sa14Storm(b)||R.t<4.8)return P4_17.base.overflight.apply(this,arguments);
 const A=sa14State(b);A.angle=Math.PI;A.scale=1;A.depth=false;b._noHit=b._s4Airborne=false;R.warnings=[];
 b.y=PLAY.y+135-(R.t-4.8)*9;b.x+=clamp(camLeftX()+viewW()*.5-b.x,-45*dt,45*dt);b._drawY=b.y;
 T.p4BallWarm??=p4FinalCfg().ballWarn;T.shot-=dt;
 if(T.shot>0){const progress=clamp(1-T.shot/T.p4BallWarm,0,1);
  for(const p of p4BallLanes(b,true))R.warnings.push({...p,progress});
  combatWarningTick(b,'p4-overflight-'+R.serial+'-'+T.wave,T.p4BallWarm-T.shot,T.p4BallWarm);
 }else{sa14Balls(b,false,true);T.shot=T.p4BallWarm;}
 if(R.t>=R.dur){sa14Log('pursuit-complete',b);er26Set(b,'recover');}return true;
};
function p4BoltLanes(b,q){
 const n=q.kind==='anger'?2+p4Rank():2,out=[],y=(b._drawY??b.y)+b.h*.30;
 for(let i=0;i<n;i++){const u=n===1?0:(i-(n-1)/2)/((n-1)/2),x=b.x+u*b.w*.25;
  // Lock the target once. Movement can take the pilot clear of the lane.
  const base=clamp(Math.atan2(q.aim.y-y,q.aim.x-b.x),Math.PI*.28,Math.PI*.72);
  out.push({x,y,angle:base+u*.13,width:22});
 }return out;
}
function p4Queue(b,kind,warm){const P=b._p4Final,target=targetShip(b.x,b.y);
 const q={kind,t:0,warm,id:++P.serial,aim:{x:target.x,y:target.y}};P.attacks.push(q);
 p4Log('final-warning',{id:P.id,attack:q.id,kind,warm});return q;
}
function p4FinalAttacks(b,dt){
 const P=b._p4Final,c=p4FinalCfg(),R=b._er26;P.ball-=dt;P.bolt-=dt;P.angerCd=Math.max(0,P.angerCd-dt);
 if(P.ball<=0){p4Queue(b,'balls',c.ballWarn);P.ball=c.ballGap;}
 if(P.bolt<=0){p4Queue(b,'bolts',c.angerWarn+.18);P.bolt=c.boltGap;}
 if(P.anger>=1&&P.angerCd<=0&&P.attacks.filter(q=>q.kind==='anger').length<2){
  P.anger-=1;P.angerCd=.80;p4Queue(b,'anger',c.angerWarn);
 }
 let glow=0;for(const q of P.attacks){q.t+=dt;
  const lanes=q.kind==='balls'?p4BallLanes(b,true):p4BoltLanes(b,q);
  if(q.t<q.warm){const progress=q.t/q.warm;glow=Math.max(glow,progress);
   for(const lane of lanes)R.warnings.push({...lane,progress});
   combatWarningTick(b,'p4-final-'+P.id+'-'+q.id,q.t,q.warm);continue;
  }
  if(q.kind==='balls')p4EmitBalls(b,lanes,true);
  else{for(const lane of lanes){const shot=stage4WarfareShot(b,lane,lane.angle,3.6+p4Rank()*.3,'lightning',{szMul:.80});
    Object.assign(shot,{_p4FinalShot:true,_p4Retaliation:q.kind==='anger',_er26Source:b._ship,_weaponProof:true,_shootable:false});
   }R.shots+=lanes.length;Audio.SFX.enemyElectricBolt?.();shake=Math.max(shake,3);
  }
  q.dead=true;p4Log('final-release',{id:P.id,attack:q.id,kind:q.kind,count:lanes.length,warned:q.t});
 }P.attacks=P.attacks.filter(q=>!q.dead);sa14State(b).glow=glow*.62;
}
function p4FinalTick(b,dt){
 const P=b._p4Final,A=sa14State(b),R=b._er26,c=p4FinalCfg();
 P.t+=dt;R.mode='sa14-final';R.warnings=[];A.glow=0;
 const ramEnd=c.tell+.82,holdEnd=ramEnd+.26,returnEnd=holdEnd+1.85;
 if(P.t<c.tell){
  P.phase='panic';const u=P.t/c.tell;
  A.glow=.60+.40*u;shake=Math.max(shake,2+u*4);
  if(u<.64){const target=targetShip(b.x,b.y);P.aim={x:target.x,y:target.y};}
  P.exit.x=clamp(P.aim.x,camLeftX()+b.w*.25,camRightX()-b.w*.25);
  sa14Warning(b,{x:b.x,y:b.y},P.exit,b.w*.60,u);combatWarningTick(b,'p4-panic-'+P.id,P.t,c.tell);sa14Rev(b,u,dt);
  A.angle=0;A.depth=false;b._noHit=false;
 }else if(P.t<ramEnd){
  if(P.phase==='panic'){sa14Stop(b);Audio.SFX.chargeDash?.();Audio.SFX.tlvJetThrust?.();shake=Math.max(shake,7);p4Log('final-ram',{id:P.id,x:P.exit.x});}
  P.phase='ram';const u=p4Ease((P.t-c.tell)/.82);
  b.x=lerp(P.from.x,P.exit.x,u);b.y=lerp(P.from.y,P.exit.y,u);A.angle=0;A.scale=1;
  A.depth=b.y-b.h*.5>VH;b._noHit=A.depth;
 }else if(P.t<holdEnd){P.phase='away';b.y=P.exit.y;A.depth=true;b._noHit=true;
 }else if(P.t<returnEnd){
  P.phase='overhead';const u=p4Ease((P.t-holdEnd)/1.85);
  A.angle=Math.PI;A.scale=lerp(2.45,1,u);A.depth=true;b._noHit=true;A.glow=.20;
  b.x=lerp(P.exit.x,camLeftX()+viewW()*.5,u);b.y=lerp(P.exit.y,PLAY.y+135,u);sa14Rumble(b,.35,dt);
 }else{
  if(P.phase!=='rear'){P.phase='rear';p4Log('final-northbound',{id:P.id});Audio.SFX.tlvJetBrake?.();}
  P.rearT+=dt;A.angle=Math.PI;A.scale=1;A.depth=false;b._noHit=false;
  const x=camLeftX()+viewW()*.5+Math.sin(P.rearT*.42)*viewW()*.10;
  b.x+=clamp(x-b.x,-38*dt,38*dt);b.y=Math.max(PLAY.y+96,PLAY.y+135-P.rearT*5);
  b._drawY=b.y;p4FinalAttacks(b,dt);
 }
 b._drawY=b.y;b._s4Airborne=A.depth;stage4ShieldSyncNodes(b);sa14CoreTick(b,dt);return true;
}
er26WarTick=function(b,dt){
 if(sa14Storm(b)&&!b.dead&&b.hp>0){
  if(!b._p4Final&&!b.enter&&(b._s4war._pt11Chase||b.hp<=b.maxhp*.25001))p4FinalStart(b);
  if(b._p4Final)return p4FinalTick(b,dt);
 }return P4_17.base.war.apply(this,arguments);
};
er26DamageClamp=function(b,dmg){
 dmg=P4_17.base.clamp.apply(this,arguments);const P=b?._p4Final;if(!P||!sa14Storm(b)||dmg<=0)return dmg;
 // Commit to the ram even under a nuke. Once northbound the exposed hull
 // burns down fast; there is no new HP pool, heal, or perpetual phase floor.
 return P.phase==='rear'?dmg*p4FinalCfg().mult:Math.max(0,Math.min(dmg,b.hp-b.maxhp*.04));
};
hitBoss=function(){
 const b=boss,before=b?.hp,r=P4_17.base.hit.apply(this,arguments),P=b?._p4Final;
 if(P&&sa14Storm(b)&&P.phase==='rear'&&!b.dead&&b.hp>0){const loss=Math.max(0,before-b.hp);
  if(loss>0){P.damage+=loss;P.anger=Math.min(2,P.anger+loss/Math.max(1,b.maxhp*.012));}
 }return r;
};
window.BOF_STAGE4_PANIC={stats:P4_17,lanes:p4BallLanes,raid:p4WingRaid,start:p4FinalStart};
er26Draw=function(b){const r=P4_17.base.draw.apply(this,arguments);
 if(!sa14Mini(b)||b.dead)return r;
 for(const s of b._wing17?.slots||[]){const e=s.e,D=e?._wing17.p4Raid;if(!e||e.dead||e._dyingT!=null||!D||e._wing17.phase!=='away')continue;
  const g=wing17Gate(b,s),o=wing17Orbit(b,s,b._wing17.t),x=clamp(g.x,camLeftX()+24,camRightX()-24),y=clamp(g.y,PLAY.y+20,VH-14);
  combatWarningDraw(e,{x,y,ex:o.x,ey:o.y,width:80,progress:clamp((D.t-2.25)/.55,0,1),alertX:x,alertY:s.edge==='N'?y+44:y-42});
 }return r;
};
