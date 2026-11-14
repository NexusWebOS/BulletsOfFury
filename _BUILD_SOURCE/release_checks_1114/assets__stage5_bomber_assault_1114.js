'use strict';
/* Stage5 Eclipse: hunting optics, burst/cool/burst, depth bombing and catch-up.
   Native four-module gate, pools, impact, breakup, reward and defeat stay owners. */
const S5B14={base:{tick:siegeBomberTick,draw:siegeBomberDraw,hit:siegeBomberHit,at:siegeBomberAt,
 beam:siegeBomberBeam,targets:siegeBomberTargets,projectile:drawCombatFinalProjectile,
 intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,load:stageLoadBegin,
 ready:stageLoadReady,foreground:s5RunForegroundDraw,ground:groundTargetingDraw,state:setState,begin:beginStage,gravity:sg26Begin},
 events:[],serial:0,maxRounds:128,maxBombs:24};
for(const [n,a]of Object.entries(S5B14_ART.banks))XART._src['s5b14_'+n]='assets/game/levels/stage_05/miniboss/assault_1114/'+n+'.webp';
function s5b14Own(b){return run.stage===5&&!!b?._bomber&&b.kind==='siegebomber'&&!b._bomber.space;}
function s5b14Warm(){return Object.keys(S5B14_ART.banks).map(n=>XART.rdy('s5b14_'+n)).every(Boolean);}
function s5b14Log(b,event,data={}){S5B14.events.push({event,time:efxClock,phase:b?._s5b14?.phase,x:b?.x,y:b?.y,...data});if(S5B14.events.length>2200)S5B14.events.shift();}
function s5b14Live(b,id){return !b.dead&&(id==='core'?b._bomber.core>0:b._bomber.parts.some(p=>p.id===id&&p.hp>0));}
function s5b14Guns(b){return['laserL','laserR'].filter(id=>s5b14Live(b,id));}
function s5b14Rank(){return diffKey==='easy'?0:diffKey==='normal'?1:diffKey==='hard'?2:3;}
function s5b14Depth(d){return clamp(Math.round((d-.42)/(1.9-.42)*31),0,31);}
function s5b14Blit(name,f,x,y,hit=false){const key='s5b14_'+name+(hit?'_hit':''),a=S5B14_ART.banks[name];if(!a||!XART.rdy(key))return false;
 f=clamp(f|0,0,a.count-1);ctx.drawImage(XART.get(key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
function s5b14Mount(b,id,tip=false){const M=b._s5b14,m=S5B14_ART.mounts[id]||[0,b.h*.34],a=M.head*TAU/16,d=M.depth,dy=m[1]+(tip&&id.startsWith('laser')?b.w*.36*.46:0),x=m[0];
 return{x:b.x+(x*Math.cos(a)-dy*Math.sin(a))*d,y:b.y+(x*Math.sin(a)+dy*Math.cos(a))*d};}
function s5b14Air(b){return !!b?._s5b14?.air;}
function s5b14Cancel(b,all=false){
 if(b?._s5b14){b._s5b14.plan=[];b._s5b14.target=null;}
 for(const q of groundTargetingFx)if(q._s5b14Owner===b&&(all||!q._s5b14Released))q.dead=true;
 if(all)eBullets=eBullets.filter(q=>q._s5b14Owner!==b);
 if(b?._hc1007){b._hc1007.lines=[];b._hc1007.cross=null;}
 if(b?._bh25){BH25.owners.delete(b);delete b._bh25;}
}
function s5b14Mode(b,phase){const M=b._s5b14,B=b._bomber;M.phase=phase;M.t=0;M.from={x:b.x,y:b.y,depth:M.depth};if(phase!=='burst')M.plan=[];
 B.mode='s5b14-'+phase;B.t=0;B.dur=99;M.fore=false;M.air=!['stalk','lock','burst','cool','core-barrage'].includes(phase);b._s4MiniSafe=M.air;
 if(phase==='stalk'){M.depth=1;M.head=0;M.cd=.35;M.cluster=0;M.group=0;M.target=null;}
 if(phase==='lock'){
  M.depth=1;M.head=0;M.victim=targetShip(b.x,b.y);M.target={x:M.victim.x,y:M.victim.y};M.locked=false;M.round=0;
  M.warn=diffKey==='easy'?1.50:M.group?1.00:1.20;M.lockAt=M.warn-.38;M.serial=++S5B14.serial;
  av3Sound('target_acquire',.5,.4);av3Sound('laser_charge',.5,.4);s5b14Log(b,'optic-track',{serial:M.serial,guns:s5b14Guns(b)});
 }
 if(phase==='burst'){M.round=0;M.next=0;M.rounds=diffKey==='easy'?3:diffKey==='normal'?4:diffKey==='hard'?5:6;}
 if(phase==='cool'){M.target=M.target&&{...M.target};M.cool=diffKey==='easy'?2.35:2.0;s5b14Log(b,'cannons-cooling');}
 if(phase==='spool'){s5b14Cancel(b);M.target=null;M.engines=b._bomber.parts.filter(p=>p.id.startsWith('engine')&&p.hp>0).length;Snd.play('jetDash',.5);}
 if(phase==='turn-in'){M.depth=.42;M.head=0;M.diveX=clamp(targetShip(b.x,b.y).x,camLeftX()+90,camRightX()-90);M.safeX=clamp(targetShip(b.x,b.y).x+(M.cycle%2?55:-55),camLeftX()+60,camRightX()-60);}
 if(phase==='charge'){M.depth=.42;M.head=8;M.drop=0;M.dropCd=.12;M.raid=++S5B14.serial;Snd.play('jetDash',.5);}
 if(phase==='catch'){M.catch=0;M.head=0;M.depth=.55;}
 if(phase==='core-barrage'){M.depth=1;M.head=0;M.cd=.25;M.target=null;}
 s5b14Log(b,'phase',{to:phase,hp:b.hp,parts:B.parts.map(p=>[p.id,p.hp])});
}
function s5b14Init(b){b._s5b14={phase:'stalk',t:0,clock:0,depth:1,head:0,air:false,fore:false,cycle:0,group:0,cluster:0,shotAge:{},plan:[],serial:0};
 s5b14Cancel(b);b._hc1007??={clock:0,age:0,lines:[]};b._hc1007.lines=[];b._hc1007.cross=null;s5b14Mode(b,'stalk');s5b14Log(b,'init',{hp:b.hp,maxhp:b.maxhp});}
function s5b14Owned(b){return eBullets.filter(q=>q._s5b14Owner===b&&!q.dead).length;}
function s5b14Bomb(b,source,x,y,warn=1.55,raid=false){if(b.dead||groundTargetingFx.filter(q=>q._s5b14Owner===b&&!q.dead).length>=S5B14.maxBombs)return;
 const q=groundTargetingSpawn({kind:'missile',owner:b,x,y,warn,active:.34,radius:20,size:66,track:false,lane:false,shake:2,sound:'groundBombImpact',onImpact:g=>{if(!b.dead){explode(g.x,g.y,48,'red');s5b14Log(b,'bomb-impact',{x:g.x,y:g.y,raid});}}});
 if(!q)return;Object.assign(q,{_s5b14Owner:b,_s5b14Source:{...source},_s5b14Released:true,_s5b14Raid:raid});b._bomber.bombs.push(q);s5b14Log(b,'bomb-drop',{x:source.x,y:source.y,target:{x,y},warn,raid});}
function s5b14DropRow(b){const M=b._s5b14,rank=s5b14Rank(),columns=[.10,.27,.44,.61,.78,.94].map(f=>camLeftX()+viewW()*f),source=s5b14Mount(b,'core');
 const y=clamp(viewTopY()+viewH()*(.43+(M.drop%4)*.135),viewTopY()+185,VH-35),choices=columns.filter(x=>Math.abs(x-M.safeX)>62),n=rank>=1?2:1;
 for(let j=0;j<n;j++){const x=choices[(M.drop*2+j)%choices.length];s5b14Bomb(b,source,x,y,3.25+(M.drop%2)*.13,true);}
 M.drop++;}
function s5b14Lock(b){const M=b._s5b14;M.locked=true;M.fireRoot={x:b.x,y:b.y};M.plan=s5b14Guns(b).map(id=>{const p=s5b14Mount(b,id,true);return{id,angle:Math.atan2(M.target.y-p.y,M.target.x-p.x),target:{...M.target}};});
 s5b14Log(b,'optic-commit',{serial:M.serial,target:{...M.target},origins:M.plan.map(p=>({...s5b14Mount(b,p.id,true),id:p.id,angle:p.angle}))});}
function s5b14Round(b){const M=b._s5b14;
 for(const P of M.plan){if(!s5b14Live(b,P.id)||s5b14Owned(b)>=S5B14.maxRounds)continue;const p=s5b14Mount(b,P.id,true),angle=P.angle+(M.round%2?.012:-.012),q=eShootT(p.x,p.y,angle,diffKey==='easy'?4.7:5.6,'s6orb',{owner:b,w:6,h:22,silent:true,noMuzzle:true});
  if(q){Object.assign(q,{_s5b14Owner:b,_s5b14Part:P.id,_s5b14Laser:true,_hc1007Owner:b,_hc1007Part:P.id,_noArsenal:true,_boss:true,_weaponProof:true,_shootable:false,homing:false});delete q.hp;M.shotAge[P.id]=0;M.shotAngle??={};M.shotAngle[P.id]=angle;s5b14Log(b,'laser-round',{part:P.id,x:p.x,y:p.y,angle,serial:M.serial,round:M.round});}}
 av3Sound('laser_release',.55,.11);M.round++;}
function s5b14Step(b,dt){const B=b._bomber;if(b.dead){s5b14Cancel(b,true);return S5B14.base.tick.call(this,b,dt);}if(b.enter||B.mode==='entry')return S5B14.base.tick.call(this,b,dt);
 if(!b._s5b14)s5b14Init(b);const M=b._s5b14;dt=clamp(dt,0,.05);
 if(!seatList().some(s=>{let live=false;withSeat(s,()=>live=!player.dead&&!player.out);return live;})){s5b14Cancel(b);return;}
 M.clock+=dt;M.t+=dt;B.clock+=dt;B.t+=dt;b.flash=Math.max(0,(b.flash||0)-dt);for(const p of B.parts)p.flash=Math.max(0,p.flash-dt);for(const id of Object.keys(M.shotAge))M.shotAge[id]+=dt;
 if(b._hc1007){b._hc1007.clock+=dt;b._hc1007.age=M.t;b._hc1007.lines=[];b._hc1007.cross=null;}B.bombs=B.bombs.filter(q=>!q.dead);
 const L=camLeftX(),R=camRightX(),center=(L+R)/2,home=b.ty,left=L+b.w*.52,right=R-b.w*.52,engines=B.parts.filter(p=>p.id.startsWith('engine')&&p.hp>0).length,move=.60+engines*.20;
 if(['stalk','lock','burst','cool','core-barrage'].includes(M.phase)){
  if(M.phase==='burst'||M.phase==='lock'&&M.locked){b.x=M.fireRoot.x;b.y=M.fireRoot.y;}else{const tx=clamp(center+Math.sin(M.clock*.68)*Math.min(84,(right-left)*.48)*move,left,right);b.x+=clamp(tx-b.x,-88*move*dt,88*move*dt);b.y=home+Math.sin(M.clock*1.3)*5;}M.depth=1;M.head=0;M.air=M.fore=false;
 }
 if(M.phase==='stalk'||M.phase==='core-barrage'){
  M.cd-=dt;if(M.cd<=0){const T=targetShip(b.x,b.y),bay=s5b14Mount(b,'core');s5b14Bomb(b,bay,clamp(T.x+(M.cycle%2?42:-42),L+28,R-28),clamp(T.y,viewTopY()+225,VH-38),diffKey==='easy'?1.9:1.55);M.cd=turretInterval15(M.phase==='core-barrage'?.72:1.05);}
  if(M.t>=(M.phase==='core-barrage'?5.0:1.65)){if(s5b14Guns(b).length)s5b14Mode(b,'lock');else if(M.phase==='stalk')s5b14Mode(b,'core-barrage');else s5b14Mode(b,'spool');}
 }else if(M.phase==='lock'){
  if(!s5b14Guns(b).length){s5b14Mode(b,'core-barrage');return;}
  if(!M.locked){const T=M.victim&&!M.victim.dead?M.victim:targetShip(b.x,b.y),rate=turretSpeed15(320);M.target.x+=clamp(T.x-M.target.x,-rate*dt,rate*dt);M.target.y+=clamp(T.y-M.target.y,-rate*dt,rate*dt);if(M.t>=M.lockAt)s5b14Lock(b);}
  combatWarningTick(b,'s5b14-lock-'+M.serial,M.t,M.warn);if(M.t>=M.warn)s5b14Mode(b,'burst');
 }else if(M.phase==='burst'){
  // mode changes preserve the committed plan and target until this burst ends.
  while(M.round<M.rounds&&M.t>=M.next){s5b14Round(b);M.next+=turretInterval15(.145);}
  if(M.t>=M.next+.18){M.group++;if(M.group<2)s5b14Mode(b,'lock');else{s5b14Mode(b,'cool');M.group=0;M.cluster++;}}
 }else if(M.phase==='cool'){if(M.t>=M.cool){if(M.cluster<2&&s5b14Guns(b).length)s5b14Mode(b,'lock');else s5b14Mode(b,'spool');}}
 else if(M.phase==='spool'){b.y=M.from.y+Math.sin(M.t*14)*2;if(M.t>=.65)s5b14Mode(b,'boost');}
 else if(M.phase==='boost'){
  const u=clamp(M.t/(1.30+(2-M.engines)*.24),0,1),e=u*u;b.x=lerp(M.from.x,center,e);b.y=lerp(M.from.y,viewTopY()+65,e);M.depth=lerp(1,.42,u);M.head=0;
  if(u>=1)s5b14Mode(b,'turn-in');
 }else if(M.phase==='turn-in'){
  const u=clamp(M.t/.85,0,1);M.head=Math.round(u*8);M.depth=.42;b.x=lerp(M.from.x,M.diveX,u);if(u>=1)s5b14Mode(b,'charge');
 }else if(M.phase==='charge'){
  const dur=2.45+(2-engines)*.17,u=clamp(M.t/dur,0,1);b.x=M.diveX;b.y=lerp(viewTopY()+65,VH+230,u*u);M.depth=lerp(.42,1.9,u);M.head=8;M.fore=M.depth>1.02;M.dropCd-=dt;
  if(M.dropCd<=0&&u<.70){s5b14DropRow(b);M.dropCd=turretInterval15(diffKey==='easy'?.34:.22);}
  if(u>=1)s5b14Mode(b,'pass');
 }else if(M.phase==='pass'){b.y=lerp(M.from.y,VH+420,clamp(M.t/.60,0,1));M.depth=1.9;M.head=8;M.fore=true;if(M.t>=.60)s5b14Mode(b,'turnback');}
 else if(M.phase==='turnback'){M.head=8+Math.round(clamp(M.t/.7,0,1)*8);M.depth=1.9;M.fore=true;if(M.t>=.7){M.head=0;s5b14Mode(b,'return');Snd.play('jetDash',.5);}}
 else if(M.phase==='return'){
  const u=clamp(M.t/(2.0+(2-engines)*.22),0,1),e=u*u*(3-2*u);b.x=lerp(M.from.x,center,e);b.y=lerp(M.from.y,viewTopY()+90,e);M.depth=lerp(1.9,.55,u);M.head=0;M.fore=M.depth>1.02;if(u>=1)s5b14Mode(b,'catch');
 }else if(M.phase==='catch'){
  const T=targetShip(b.x,b.y),front=clamp((VH*.73-T.y)/(VH*.50),0,1);M.catch+=dt*(.46+front*1.35);const u=clamp(Math.max(M.catch/1.55,M.t/3.65),0,1);b.x=lerp(M.from.x,center,u);b.y=lerp(M.from.y,home,u);M.depth=lerp(.55,1,u);M.head=0;
  if(u>=1){M.cycle++;s5b14Log(b,'caught-up',{seconds:M.t,hp:b.hp});s5b14Mode(b,'stalk');}
 }
 b._drawY=b.y;
}
siegeBomberTick=function(b,dt){return s5b14Own(b)?s5b14Step(b,dt):S5B14.base.tick.apply(this,arguments);};
// This aircraft owns its physical altitude and committed firing pose. Remove a
// previous entry float once, then leave all other space actors on native gravity.
sg26Begin=function(b,dt){if(s5b14Own(b)&&b._s5b14&&!b.enter){const q=b._sg26;if(q?.offset){sg26Move(q.points,-q.offset);if(q.eye===b._eh25&&q.eye)q.eye.y-=q.offset;q.offset=0;}return null;}return S5B14.base.gravity.apply(this,arguments);};

function s5b14Hull(b){const M=b._s5b14;if(!M||b.dead)return;const flight=M.air,turn=M.phase==='turn-in'||M.phase==='turnback',di=s5b14Depth(M.depth),group=di>>3,f=(di%8)*2+(M.head%16===8?1:0),head=((M.head%16)+16)%16;
 const bank=name=>name+(flight?(turn?'_turn':'_flight_'+group):'_cruise'),frame=turn?head:flight?f:head;
 s5b14Blit(bank('core'),frame,b.x,b.y,b.flash>0);
 for(const id of ['engineL','engineR','laserL','laserR']){if(!s5b14Live(b,id))continue;const p=s5b14Mount(b,id),part=b._bomber.parts.find(q=>q.id===id),gun=id.startsWith('laser');
  if(!gun&&['spool','boost','charge','return'].includes(M.phase)){const at=s5b14Mount(b,id),a=M.head*TAU/16,dy=51.6*M.depth;at.x-=Math.sin(a)*dy;at.y+=Math.cos(a)*dy;s5b14Blit('thrust_'+group,(di%8)*8+(head===8?4:0)+Math.floor(M.clock*18)%4,at.x,at.y);}
  if(gun&&!flight){let cf=0;if(M.phase==='lock')cf=Math.min(7,Math.floor(M.t/M.warn*8));else if((M.shotAge[id]??99)<.15)cf=8+Math.min(2,Math.floor(M.shotAge[id]/.05));else if(M.phase==='cool')cf=11+Math.min(4,Math.floor(M.t/.5*5));s5b14Blit('cannon_action',cf,p.x,p.y,part.flash>0);}
  else s5b14Blit(bank(gun?'cannon':'engine'),frame,p.x,p.y,part.flash>0);
  if(gun&&(M.shotAge[id]??99)<.12){const at=s5b14Mount(b,id,true),dir=((Math.round(((M.shotAngle?.[id]??Math.PI/2)-Math.PI/2)/TAU*32)%32)+32)%32;s5b14Blit('muzzle',Math.min(2,Math.floor(M.shotAge[id]/.04))*32+dir,at.x,at.y);}
 }
}
function s5b14Warnings(b){const M=b._s5b14;if(!M||b.dead)return;
 if(M.phase==='lock')for(const id of s5b14Guns(b)){const p=s5b14Mount(b,id,true),P=M.plan.find(q=>q.id===id),angle=P?.angle??Math.atan2(M.target.y-p.y,M.target.x-p.x);combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(angle)*VH*1.5,ey:p.y+Math.sin(angle)*VH*1.5,width:18,progress:clamp(M.t/M.warn,0,1),fieldOnly:true});}
 for(const q of groundTargetingFx)if(q._s5b14Owner===b&&!q.dead&&!q.impact){const u=clamp(q.t/q.warn,0,1),p=q._s5b14Source;pb28Blit('bomb',Math.floor(u*16),lerp(p.x,q.x,u),lerp(p.y,q.y,u)-Math.sin(u*Math.PI)*24);}
}
siegeBomberDraw=function(b){if(!s5b14Own(b)||!b._s5b14)return S5B14.base.draw.apply(this,arguments);const M=b._s5b14;if(b.dead)return;
 if(M.air){const d=Math.min(3,Math.max(0,Math.round((M.depth-.42)/.58*3))),head=((M.head%16)+16)%16,lead=M.phase==='return'?-150:M.phase==='charge'?150:64;s5b14Blit('shadow',d*16+head,b.x+32,b.y+lead);}
 s5b14Warnings(b);if(!M.fore)s5b14Hull(b);
};
function s5b14Optic(b){const M=b._s5b14;if(!M?.target||!s5b14Guns(b).length)return;let f;if(M.phase==='lock')f=M.locked?8+Math.floor(M.t*16)%4:Math.min(7,Math.floor(M.t/M.lockAt*8));else if(M.phase==='burst')f=8+Math.floor(M.t*20)%4;else if(M.phase==='cool'&&M.t<.65)f=12+Math.min(3,Math.floor(M.t/.65*4));else return;s5b14Blit('retina',f,M.target.x,M.target.y);}
s5RunForegroundDraw=function(){const out=S5B14.base.foreground.apply(this,arguments),b=subBoss;if(s5b14Own(b)&&b._s5b14&&!b.dead){if(b._s5b14.fore){s5b14Hull(b);const all=groundTargetingFx;try{groundTargetingFx=all.filter(q=>q._s5b14Owner===b);S5B14.base.ground();}finally{groundTargetingFx=all;}}s5b14Optic(b);}return out;};
groundTargetingDraw=function(){const b=subBoss;if(!s5b14Own(b)||!b._s5b14?.fore)return S5B14.base.ground.apply(this,arguments);const all=groundTargetingFx;try{groundTargetingFx=all.filter(q=>q._s5b14Owner!==b);return S5B14.base.ground.apply(this,arguments);}finally{groundTargetingFx=all;}};
siegeBomberAt=function(b){return s5b14Own(b)&&s5b14Air(b)?null:S5B14.base.at.apply(this,arguments);};
siegeBomberBeam=function(b){return s5b14Own(b)&&s5b14Air(b)?null:S5B14.base.beam.apply(this,arguments);};
siegeBomberTargets=function(b){return s5b14Own(b)&&s5b14Air(b)?[]:S5B14.base.targets.apply(this,arguments);};
siegeBomberHit=function(b){if(s5b14Own(b)&&s5b14Air(b))return;const out=S5B14.base.hit.apply(this,arguments);if(s5b14Own(b)&&b._s5b14){const M=b._s5b14;M.plan=M.plan.filter(p=>s5b14Live(b,p.id));eBullets=eBullets.filter(q=>q._s5b14Owner!==b||!q._s5b14Part||s5b14Live(b,q._s5b14Part));if(b.dead)s5b14Cancel(b,true);}return out;};
drawCombatFinalProjectile=function(q){if(q._s5b14Laser){const h=((Math.round((Math.atan2(q.vy,q.vx)-Math.PI/2)/TAU*32)%32)+32)%32;return s5b14Blit('laser',Math.floor(projectileVisualAge(q)*18)%3*32+h,q.x,q.y);}return S5B14.base.projectile.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._s5b14Laser?false:S5B14.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._s5b14Laser?null:S5B14.base.element.apply(this,arguments);};
stageLoadBegin=function(n,keys){return S5B14.base.load.call(this,n,[...(keys||[]),...(n===5?[...Object.keys(S5B14_ART.banks).map(k=>'s5b14_'+k),...['bomb'].map(k=>PB28_ART[k].key)]:[])]);};
stageLoadReady=function(n=run.stage){return S5B14.base.ready.apply(this,arguments)&&(n!==5||s5b14Warm());};
setState=function(s){if(s!==GS.PLAY&&s!==GS.PAUSED&&s5b14Own(subBoss))s5b14Cancel(subBoss,true);return S5B14.base.state.apply(this,arguments);};
beginStage=function(){if(subBoss?._s5b14)s5b14Cancel(subBoss,true);return S5B14.base.begin.apply(this,arguments);};
globalThis.BOF_STAGE5_BOMBER_ASSAULT_1114=S5B14;
