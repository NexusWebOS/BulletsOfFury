'use strict';
/* EH57: actual optical pivot, alien lasers, native half-health UFO dash phase. */
const EH57={base:{init:s9VoidHorizonInit,tick:s9VoidHorizonTick,draw:s9VoidHorizonDraw,hit:s9VoidHorizonHit,part:s9VoidHorizonPart,
 targets:retinaBossTargets,eye:s5924Eye,set:s5924Set,projectile:drawCombatFinalProjectile,update:updatePlay,
 intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,rules:s3kOrdnanceRules,load:stageLoadBegin},events:[],owners:new Set()};
for(const[name,a]of Object.entries(EH57_ART)){ER28_ART['eh57_'+name]=a;XART._src[a.key]=a.path;}
function eh57Own(b){return run.stage===9&&b===subBoss&&!!b?._s9rift?.s5924;}
function eh57Log(event,data={}){EH57.events.push({event,time:efxClock,...data});if(EH57.events.length>1800)EH57.events.shift();}
function eh57State(b){if(!b._eh57){b._eh57={clock:0,t:0,mode:'entry',half:false,protected:true,frame:0,angle:0,turn:0,dashTurn:0,
 origin:{x:camLeftX()+viewW()/2,y:viewTopY()+205},from:{x:b._s9rift.core.x,y:viewTopY()-240},beams:[],next:0,pulse:0,hit:new Map()};EH57.owners.add(b);}return b._eh57;}
function eh57Blit(name,f,x,y){return er28Blit('eh57_'+name,f,x,y);}
s9VoidHorizonInit=function(b){const r=EH57.base.init.apply(this,arguments);if(eh57Own(b))eh57State(b);return r;};
stageLoadBegin=function(n,keys){if(n===9)Snd.prepare(['bossWeaponCharge','combatBeam0927','combatOrb0927','jetDash','warpBurst']);return EH57.base.load.call(this,n,n===9?[...(keys||[]),...Object.values(EH57_ART).map(a=>a.key),HH52_ART.star.key,...['field','symbol'].flatMap(r=>['green','yellow','red'].map(c=>'rk50_'+r+'_'+c))]:keys);};
function eh57Point(b){return{x:b._s9rift.core.x,y:b._s9rift.core.y};}
s5924Eye=function(b){return eh57Own(b)?eh57Point(b):EH57.base.eye.apply(this,arguments);};
function eh57Move(b,x,y){const w=b._s9rift.core;w.x=b.x=x;w.y=b.y=b._drawY=y;}
function eh57Set(b,mode){const H=eh57State(b),p=eh57Point(b);H.mode=mode;H.t=0;H.next=0;H.shots=0;H.beams=[];H.from={...p};H.protected=false;
 const hard=diffKey==='hard',r=hard?0:1;H.profile=hard?'hard':'furious';
 H.warm=mode==='orb'?[1.65,1.45][r]:mode==='dash'?[1.50,1.35][r]:[1.50,1.35][r];
 H.period=[.88,.74][r];H.on=[.20,.22][r];H.pulses=mode==='spiral'?[3,4][r]:mode==='sweep'?[2,3][r]:[2,3][r];
 H.active=['spiral','sweep','beam'].includes(mode)?(H.pulses-1)*H.period+H.on+.04:mode==='orb'?1.6:[1.65,1.95][r];
 H.rest=[1.65,1.35][r]/(run.ngplus?1.15:1);H.pulseIndex=-1;
 H.aim=Math.atan2(player.y-p.y,player.x-p.x);H.locked=false;H.phase='charge';H.phaseBorn=H.clock;
 if(mode==='dash'){const side=H.dashTurn++%4,x=clamp(player.x,camLeftX()+75,camRightX()-75),y=clamp(player.y,viewTopY()+90,VH-60);
  H.start=side===0?{x:camLeftX()-240,y}:side===1?{x,y:viewTopY()-240}:side===2?{x:camRightX()+240,y}:{x,y:VH+240};
  H.end=side===0?{x:camRightX()+240,y}:side===1?{x,y:VH+240}:side===2?{x:camLeftX()-240,y}:{x,y:viewTopY()-240};
  H.dashAngle=Math.atan2(H.end.y-H.start.y,H.end.x-H.start.x);H.dashDuration=1.05;
 }
 combatAudio0927(b,'bossWeaponCharge',.2);eh57Log('attack-start',{mode,half:H.half,warm:H.warm,eye:p,target:{x:player.x,y:player.y},start:H.start,end:H.end});
}
function eh57Next(b){const H=eh57State(b),book=diffKey==='hard'?(H.half?['dash','orb','spiral','beam','spin']:['beam','orb','spiral','spin']):(H.half?['dash','spiral','sweep','orb','dash','spin','beam']:['spiral','beam','sweep','orb','spin']);eh57Set(b,book[H.turn++%book.length]);}
s5924Set=function(b,mode){if(eh57Own(b)&&b._eh57){if(mode==='entry')return;return eh57Next(b);}return EH57.base.set.apply(this,arguments);};
function eh57Half(b){const H=eh57State(b);H.half=true;H.mode='half';H.phase='water-charge';H.t=0;H.protected=true;H.from=eh57Point(b);H.beams=[];H.turn=0;
 for(const q of eBullets)if(q._eh57Owner===b)q.dead=true;if(b._eh25?.bomb)eh25Cancel(b,'symbiote-phase-change');delete b._bh25;
 combatAudio0927(b,'bossWeaponCharge',.15);eh57Log('half-health',{hp:b.hp,maxhp:b.maxhp,eye:eh57Point(b)});
}
s9VoidHorizonPart=function(b,x,y){if(!eh57Own(b))return EH57.base.part.apply(this,arguments);const H=eh57State(b),w=b._s9rift.core;
 if(b.enter||b.dead||w.disabled||H.protected||!Number.isFinite(x+y))return null;
 return er28AlphaAt('eh57_ship_hit',H.frame,x-w.x,y-w.y)?w:null;};
s9VoidHorizonHit=function(b,dmg,x,y){if(!eh57Own(b))return EH57.base.hit.apply(this,arguments);const H=eh57State(b),w=b._s9rift.core;if(H.protected)return false;const flash=w.flash||0,bodyFlash=b.flash||0;
 if(!H.half&&Number.isFinite(dmg))dmg=Math.min(dmg,Math.max(0,w.hp-w.maxhp*.5));const r=EH57.base.hit.call(this,b,dmg,x,y);if(r){if(H.clock>=(H.flashNext||0)){w.flash=b.flash=.065;H.flashNext=H.clock+.16;}else{w.flash=flash;b.flash=bodyFlash;}}
 if(!b.dead&&!H.half&&w.hp<=w.maxhp*.5+.001)eh57Half(b);if(b.dead)eh57Clear(b);return r;};
retinaBossTargets=function(b){if(eh57Own(b)&&(eh57State(b).protected||b.x<camLeftX()-140||b.x>camRightX()+140||b.y<viewTopY()-140||b.y>VH+140))return[];return EH57.base.targets.apply(this,arguments);};
function eh57Clear(b){const H=b?._eh57;if(!H)return;H.beams=[];for(const q of eBullets)if(q._eh57Owner===b)q.dead=true;EH57.owners.delete(b);}
function eh57Round(b,a,speed,orb=false){if(eBullets.filter(q=>q._eh57Owner===b&&!q.dead).length>=120)return null;const p=eh57Point(b),q=eShootT(p.x,p.y,a,speed/60,orb?'s9pair':'s9needle',{owner:b,noMuzzle:true,silent:true,w:orb?36:10,h:orb?36:10});if(!q)return null;
 Object.assign(q,{_eh57Owner:b,_eh57Born:efxClock,_eh57Orb:orb,_eh57Water:eh57State(b).half,_weaponProof:true,_shootable:false,_s3kOriginalProof:false,_noArsenal:true,_boss:true,homing:false});
 q.vx=Math.cos(a)*speed/60;q.vy=Math.sin(a)*speed/60;delete q.hp;return q;
}
function eh57Beam(H,x,y,a,length){H.beams.push({x,y,ex:x+Math.cos(a)*length,ey:y+Math.sin(a)*length,a,length});}
function eh57Heading(H){return H.angle+(H.rayOffset||0);}
function eh57Rays(b,H,u){const p=eh57Point(b);if(SG26.context?.b===b)p.y+=SG26.context.q.next;H.beams=[];
 if(['spiral','sweep','beam'].includes(H.mode)&&u%H.period>=H.on)return;
 if(H.mode==='spiral'){
  const step=20,arms=2,n=24;for(let arm=0;arm<arms;arm++){let prev=p;for(let j=1;j<=n;j++){const r=j*step,theta=eh57Heading(H)+r/250+arm*Math.PI,P={x:p.x+Math.cos(theta)*r,y:p.y+Math.sin(theta)*r};
   eh57Beam(H,prev.x,prev.y,Math.atan2(P.y-prev.y,P.x-prev.x),Math.hypot(P.x-prev.x,P.y-prev.y));prev=P;}}
 }else if(H.mode==='sweep')eh57Beam(H,p.x,p.y,eh57Heading(H),900);
 else if(H.mode==='beam')eh57Beam(H,p.x,p.y,eh57Heading(H),900);
 else if(H.mode==='dash'&&H.phase==='dash')for(const off of[0,Math.PI/2,-Math.PI/2])eh57Beam(H,p.x,p.y,H.angle+off,180);
}
function eh57Touch(b,H){for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out||player.invuln>0||(H.hit.get(seat)||0)>H.clock)return;
 const dy=SG26.context?.b===b?SG26.context.q.next:0;
 const hit=H.beams.some(L=>s81003Distance(player.x,player.y,L)<9)||H.mode==='dash'&&H.phase==='dash'&&s9VoidHorizonPart(b,player.x,player.y-dy);
 if(hit){H.hit.set(seat,H.clock+.25);playerHit('Event Horizon symbiote laser');}});}
function eh57Dash(b,H,dt){const u=H.t-H.warm;
 if(u<0)return;
 if(u<.65){H.phase='depart';H.protected=true;const v=u/.65;eh57Move(b,lerp(H.from.x,H.start.x,v),lerp(H.from.y,H.start.y,v));}
 else if(u<1.80){H.phase='edge-charge';H.protected=true;eh57Move(b,H.start.x,H.start.y);}
 else if(u<1.80+H.dashDuration){if(H.phase!=='dash'){H.phase='dash';H.protected=false;combatAudio0927(b,'jetDash',.25);eh57Log('dash-release',{start:H.start,end:H.end,duration:H.dashDuration});}
  const v=(u-1.80)/H.dashDuration;eh57Move(b,lerp(H.start.x,H.end.x,v),lerp(H.start.y,H.end.y,v));eh57Rays(b,H,u);
 }else if(u<3.45){H.phase='offscreen';H.protected=true;H.beams=[];eh57Move(b,H.end.x,H.end.y);}
 else if(u<4.85){H.phase='return';H.protected=true;H.beams=[];const v=(u-3.45)/1.4,k=v*v*(3-2*v);eh57Move(b,camLeftX()+viewW()/2,lerp(viewTopY()-240,H.origin.y,k));}
 else if(u<4.85+H.rest){H.phase='recover';H.protected=false;H.beams=[];eh57Move(b,H.origin.x,H.origin.y+Math.sin(H.clock)*6);}
 else{H.protected=false;H.beams=[];eh57Log('dash-complete');eh57Next(b);}
}
s9VoidHorizonTick=function(b,dt){if(!eh57Own(b))return EH57.base.tick.apply(this,arguments);if(b.dead){eh57Clear(b);return true;}
 const H=eh57State(b),F=b._s9rift,w=F.core;dt=Math.min(.05,Math.max(0,dt));H.clock+=dt;H.t+=dt;H.omega=TAU*.60;H.angle+=dt*H.omega;F.t+=dt;w.flash=Math.max(0,w.flash-dt);b.flash=Math.max(0,(b.flash||0)-dt);b._late27=null;b._s4MiniSafe=true;
 if(!H.half&&w.hp<=w.maxhp*.5+.001)eh57Half(b);
 if(H.mode==='entry'){const v=clamp(H.t/1.8,0,1),k=v*v*(3-2*v);eh57Move(b,H.origin.x,lerp(H.from.y,H.origin.y,k));b.enter=v<1;if(v>=1){H.protected=false;eh57Next(b);}}
 else if(H.mode==='half'){
  eh57Move(b,H.from.x+Math.sin(H.t*2)*8,H.from.y+Math.sin(H.t*3)*5);if(H.t>=2.4){H.protected=false;eh57Log('water-phase-ready');eh57Next(b);}
 }else if(H.mode==='dash')eh57Dash(b,H,dt);
 else{const u=H.t-H.warm;
  if(u<0){H.phase='charge';const p=clamp(H.t/H.warm,0,1);
   if(!H.locked){eh57Move(b,H.from.x+Math.sin(H.t*1.4)*16,H.from.y+Math.sin(H.t*2.2)*7);H.aim=Math.atan2(player.y-b.y,player.x-b.x);if(p>=.45){H.locked=true;H.lock={x:b.x,y:b.y};eh57Log('aim-locked',{mode:H.mode,a:H.aim,eye:eh57Point(b)});}}
   combatWarningTick(b,'eh57-'+H.mode,H.t,H.warm);
  }else if(u<H.active){if(H.phase!=='fire'){H.phase='fire';H.fireBorn=H.clock;H.rayOffset=H.aim-H.angle;combatAudio0927(b,H.mode==='orb'?'combatOrb0927':'combatBeam0927',.15);eh57Log('laser-release',{mode:H.mode,eye:eh57Point(b),a:H.aim});}
   eh57Rays(b,H,u);
   if(H.beams.length&&H.pulseIndex!==Math.floor(u/H.period)){H.pulseIndex=Math.floor(u/H.period);combatAudio0927(b,'combatBeam0927',.15);eh57Log('laser-pulse',{mode:H.mode,index:H.pulseIndex,duration:H.on,gap:H.period-H.on});}
   if(H.mode==='orb'&&u>=H.next&&H.shots<(diffKey==='hard'?3:5)){eh57Round(b,H.aim+(H.shots-(diffKey==='hard'?1:2))*.13,diffKey==='hard'?220:250,true);H.shots++;H.next=u+(diffKey==='hard'?.46:.30);combatAudio0927(b,'combatOrb0927',.15);eh57Log('orb-release',{index:H.shots,eye:eh57Point(b)});}
   if(H.mode==='spin'&&u>=H.next){const n=diffKey==='hard'?12:16;for(let i=0;i<n;i++){const a=H.angle+i*TAU/n;if(Math.abs(Math.atan2(Math.sin(a-H.aim),Math.cos(a-H.aim)))>.32)eh57Round(b,a,diffKey==='hard'?180:210);}H.next=u+(diffKey==='hard'?.80:.66);combatAudio0927(b,'combatBeam0927',.25);eh57Log('spin-volley',{count:n});}
  }else{H.phase='recover';H.beams=[];const gx=camLeftX()+viewW()/2+Math.sin(H.clock*.7)*70,gy=H.origin.y+Math.sin(H.clock*1.1)*20;
   eh57Move(b,b.x+clamp(gx-b.x,-65*dt,65*dt),b.y+clamp(gy-b.y,-40*dt,40*dt));if(u>=H.active+H.rest)eh57Next(b);}
 }
 H.frame=((Math.floor(H.angle/TAU*32)%32)+32)%32;F.s5924.mode='eh57-'+H.mode;F.s5924.t=H.t;F.s5924.age=H.clock;F.s5924.angles=[];b.hp=w.hp;
 if(!H.protected)eh57Touch(b,H);return true;
};
function eh57Warning(b,H){if(H.mode==='entry'||H.mode==='half')return;const p=eh57Point(b),progress=clamp(H.t/H.warm,0,1),colour=progress<.45?'green':progress<.8?'yellow':'red';
 if(H.t<H.warm){
  if(['spiral','sweep','beam','spin','dash'].includes(H.mode)){rk50Blit('field',colour,p.x,p.y);rk50Blit('symbol',colour,p.x,Math.max(viewTopY()+34,p.y-165));}
  else combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(H.aim)*900,ey:p.y+Math.sin(H.aim)*900,width:H.mode==='orb'?70:18,progress,fieldOnly:true});
 }
 if(['spiral','beam','sweep'].includes(H.mode)&&H.phase==='fire'&&!H.beams.length){
  const u=H.t-H.warm,next=(Math.floor(u/H.period)+1)*H.period,wait=next-u;
  if(next<H.active){const a=eh57Heading(H)+H.omega*wait;
   for(const off of(H.mode==='spiral'?[0,Math.PI]:[0]))combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a+off)*900,ey:p.y+Math.sin(a+off)*900,width:18,progress:clamp(1-wait/(H.period-H.on),0,1),fieldOnly:true});}
 }
 if(H.mode==='dash'&&['charge','depart','edge-charge'].includes(H.phase)){
  const k=clamp(H.t/(H.warm+1.80),0,1);combatWarningDraw(b,{x:H.start.x,y:H.start.y,ex:H.end.x,ey:H.end.y,width:400,progress:k,fieldOnly:true});
  const x=clamp(H.start.x,camLeftX()+28,camRightX()-28),y=clamp(H.start.y,viewTopY()+48,VH-35);hh52Blit('star',0,x,y);
 }
}
function eh57DrawBeam(L,H){const steps=Math.max(1,Math.ceil(L.length/20)),dir=((Math.round(L.a/TAU*64)%64)+64)%64,f=Math.floor(H.clock*30)%16;
 for(let i=0;i<steps;i++){const d=Math.min(L.length,(i+.5)*L.length/steps);eh57Blit(H.half?'beam_water':'beam',dir*16+f,L.x+Math.cos(L.a)*d,L.y+Math.sin(L.a)*d);}}
s9VoidHorizonDraw=function(b){if(!eh57Own(b))return EH57.base.draw.apply(this,arguments);const H=eh57State(b),w=b._s9rift.core;
 eh57Warning(b,H);eh57Blit(w.flash>0?'ship_hit':H.half?'ship_water':'ship',H.frame,w.x,w.y);
 const between=H.phase==='fire'&&['spiral','sweep','beam'].includes(H.mode)&&!H.beams.length,u=H.t-H.warm,wait=H.period-(u%H.period),
 charging=H.mode==='half'||H.phase==='charge'||H.phase==='edge-charge'||between,progress=between?clamp(1-wait/(H.period-H.on),0,1):H.mode==='half'?H.t/2.4:H.phase==='edge-charge'?(H.t-H.warm-.65)/1.15:H.t/H.warm,
 pulse=charging?Math.min(7,Math.floor(clamp(progress,0,1)*8)):H.beams.length?7:Math.floor(H.clock*8)%3;
 eh57Blit(H.half?'eye_white':'eye_glow',H.frame*8+pulse,w.x,w.y);
 if(H.half&&!b.dead)for(let i=0;i<3;i++){const a=H.angle+i*TAU/3;eh57Blit('smoke',(Math.floor(H.clock*12)+i*3)%16,w.x+Math.cos(a)*68,w.y+Math.sin(a)*55);}
 for(const L of H.beams)eh57DrawBeam(L,H);
 if(H.beams.length)eh57Blit('muzzle',Math.floor((H.clock-(H.fireBorn||0))*30)%8,w.x,w.y);
 if(H.mode==='orb'&&charging)eh57Blit(H.half?'orb_water':'orb',Math.floor(H.clock*28)%16,w.x,w.y);
 if(H.mode==='dash'&&H.phase==='dash')for(let i=1;i<=4;i++)eh57Blit('dash',((Math.round(H.dashAngle/TAU*64)%64)+64)%64*8+(Math.floor(H.clock*24)+i)%8,w.x-Math.cos(H.dashAngle)*i*50,w.y-Math.sin(H.dashAngle)*i*50);
 drawSubBossBar(b);return true;
};
drawCombatFinalProjectile=function(q){if(q?._eh57Owner){const H=eh57State(q._eh57Owner),f=Math.floor((efxClock-q._eh57Born)*28)%16;
  if(q._eh57Orb)return eh57Blit(q._eh57Water?'orb_water':'orb',f,q.x,q.y);
  const dir=((Math.round(Math.atan2(q.vy,q.vx)/TAU*64)%64)+64)%64;return eh57Blit(q._eh57Water?'beam_water':'beam',dir*16+f,q.x,q.y);
 }return EH57.base.projectile.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._eh57Owner?false:EH57.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._eh57Owner?null:EH57.base.element.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._eh57Owner){q._weaponProof=true;q._shootable=false;delete q.hp;return;}return EH57.base.rules.apply(this,arguments);};
updatePlay=function(dt){for(const b of EH57.owners)if(!eh57Own(b)||b.dead)eh57Clear(b);for(const q of eBullets)if(q._eh57Owner&&(!eh57Own(q._eh57Owner)||q._eh57Owner.dead||efxClock-q._eh57Born>5))q.dead=true;return EH57.base.update.apply(this,arguments);};
globalThis.BOF_HORIZON_SYMBIOTE_1029={state:EH57,start:eh57Set};
