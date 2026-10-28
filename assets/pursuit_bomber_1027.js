'use strict';
/* Earth pursuit bomber. Engines own propulsion; the two former cannon modules
   are bomb racks. Native pools, hit routing, breakup, rewards and death stay native. */
const PB28={events:[],maxRounds:128,base:{tick:siegeBomberTick,draw:siegeBomberDraw,blit:polishBlit,
 hit:siegeBomberHit,at:siegeBomberAt,beam:siegeBomberBeam,targets:siegeBomberTargets,projectile:drawCombatFinalProjectile,
 intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,load:stageLoadBegin},drawing:null};
for(const a of Object.values(PB28_ART))XART._src[a.key]=a.path;
function pb28Own(b){return !!b?._bomber&&run.stage===6&&b.kind==='siegebomber'&&!b._bomber.space;}
function pb28Rank(){return diffKey==='easy'?0:diffKey==='normal'?1:diffKey==='hard'?2:3;}
function pb28Log(b,event,data={}){PB28.events.push({event,time:efxClock,mode:b._pb28?.mode,actorX:b.x,actorY:b.y,...data});if(PB28.events.length>1600)PB28.events.shift();}
stageLoadBegin=function(n,keys){if(n===6)for(const k of ['jetDash','alertLockon','bossWeaponCharge','enemyMissile','timedBombBlast'])Snd.prepare(k);
 return PB28.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(PB28_ART).map(a=>a.key)]:keys);};
function pb28Live(b,id){return !b.dead&&(id==='core'?b._bomber.core>0:b._bomber.parts.some(p=>p.id===id&&p.hp>0));}
function pb28Ports(b){const out=siegeBomberParts(b).filter(p=>p.id.startsWith('laser')&&pb28Live(b,p.id)).map(p=>({id:p.id,x:p.x,y:p.y+p.h*.46}));
 if(!out.length&&pb28Live(b,'core'))out.push({id:'core',x:b.x,y:b.y+b.h*.23+b.h*.15});return out;}
function pb28Port(b,id){return pb28Ports(b).find(p=>p.id===id);}
function pb28Blit(name,f,x,y,hit=false){const a=PB28_ART[hit?name+'_hit':name]||PB28_ART[name];if(!a||!XART.rdy(a.key))return false;
 f=((f|0)%a.frames+a.frames)%a.frames;ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
function pb28Dir(a){return((Math.round((a-Math.PI/2)*64/TAU)%64)+64)%64;}
function pb28Cancel(b,all=false){for(const q of groundTargetingFx)if(q._pb28Owner===b&&(all||!q._pb28Released))q.dead=true;
 if(all)for(const q of eBullets)if(q._pb28Owner===b)q.dead=true;
 if(b._hc1007){b._hc1007.lines=[];b._hc1007.cross=null;}if(b._bh25){BH25.owners.delete(b);delete b._bh25;}groundTargetingFx=groundTargetingFx.filter(q=>!q.dead);}
function pb28Mode(b,mode){const M=b._pb28;M.mode=mode;M.t=0;M.from={x:b.x,y:b.y};M.toX=clamp(b.x,camLeftX()+b.w*.53,camRightX()-b.w*.53);b._bomber.mode='pb28-'+mode;b._bomber.t=0;
 if(mode==='weave'){M.cd=.6;M.weaveStart=b.x;M.hidden=false;}
 if(mode==='spool'){pb28Cancel(b);combatAudio0927(b,'jetDash',.4);if(!M.boostSaid){M.boostSaid=true;s6WingSay('COLE','IT IS THROTTLING AHEAD! STAY ON IT!');}}
 if(mode==='ahead'){M.catchup=0;M.hidden=true;}
 if(mode==='reacquire'){M.toX=targetShip(b.x,b.y).x<camLeftX()+viewW()/2?camRightX()-b.w*.53:camLeftX()+b.w*.53;combatAudio0927(b,'alertLockon',.4);pb28Log(b,'pursuer-noticed');}
 if(mode==='ambush'){
  M.hidden=false;M.baseX=b.x;M.wave=0;M.escapeX=clamp(targetShip(b.x,b.y).x+(M.seq++%2?56:-56),camLeftX()+68,camRightX()-68);
  M.fireAt=[1.65,1.40,1.25,1.15][M.rank];M.previewAt=0;M.plan=pb28Plan(b);combatAudio0927(b,'bossWeaponCharge',.4);
  if(!M.ambushSaid){M.ambushSaid=true;s6WingSay('COLE','BOMB BAYS OPEN! WATCH THE MISSILE FAN!');}}
 pb28Log(b,'mode',{x:b.x,y:b.y,escape:M.escapeX});}
function pb28Init(b){b._hc1007={clock:0,seq:0,mode:'pb28',age:0,lines:[]};b._pb28={mode:'weave',t:0,clock:0,rank:pb28Rank(),seq:0,wave:0,serial:0,pods:{laserL:99,laserR:99},hidden:false};pb28Mode(b,'weave');pb28Log(b,'init',{hp:b.hp,maxhp:b.maxhp});}
function pb28Count(b){return eBullets.filter(q=>q._pb28Owner===b&&!q.dead).length;}
function pb28Fragment(b,x,y,a){if(pb28Count(b)>=PB28.maxRounds)return;
 const q=eShootT(x,y,a,2.0+b._pb28.rank*.17,'s6orb',{owner:b,w:7,h:9,silent:true,noMuzzle:true});Object.assign(q,{_pb28Owner:b,_pb28Type:'fragment',_noArsenal:true,_boss:true,_weaponProof:true,_shootable:false,homing:false});delete q.hp;
 return q;}
function pb28Bomb(b,p,target,warm=.9){if(!p||b._pb28.hidden||groundTargetingFx.filter(q=>q._pb28Owner===b&&!q.dead).length>=14)return;
 const q=groundTargetingSpawn({kind:'missile',owner:b,x:target.x,y:target.y,warn:warm+.88,active:.38,radius:22,size:65,track:false,lane:false,sound:'timedBombBlast',shake:2,
  onImpact:q=>{if(b.dead)return;explode(q.x,q.y,48,'red');const M=b._pb28,escape=M.escapeX??clamp(player.x,camLeftX()+50,camRightX()-50),aim=Math.atan2(VH-38-q.y,escape-q.x),half=Math.atan2(43,Math.max(55,Math.hypot(escape-q.x,VH-38-q.y)));
   for(let i=0;i<8+M.rank*2;i++){const a=i*TAU/(8+M.rank*2)+(M.wave||0)*.11;if(Math.abs(Math.atan2(Math.sin(a-aim),Math.cos(a-aim)))<half)continue;pb28Fragment(b,q.x,q.y,a);}pb28Log(b,'bomb-impact',{x:q.x,y:q.y});}});
 Object.assign(q,{_pb28Owner:b,_pb28Part:p.id,_pb28DropAt:warm,_pb28Released:false,_pb28Source:{x:p.x,y:p.y}});pb28Log(b,'bomb-tell',{part:p.id,x:p.x,y:p.y,target:{...target},warm});
}
function pb28BombTick(b){const M=b._pb28;
 for(const q of groundTargetingFx){if(q._pb28Owner!==b||q.dead||q._pb28Released)continue;const p=pb28Port(b,q._pb28Part);
  if(!p||M.hidden){q.dead=true;continue;}q._pb28Source={x:p.x,y:p.y};
  if(q.t>=q._pb28DropAt){q._pb28Released=true;M.pods[p.id]=0;combatAudio0927(b,'enemyMissile',.24);pb28Log(b,'bomb-release',{part:p.id,x:p.x,y:p.y});}}
}
function pb28Plan(b){const M=b._pb28,plan=[],count=[5,6,7,8][M.rank],gapX=clamp(M.escapeX+Math.sin(M.wave*.5)*24,camLeftX()+62,camRightX()-62);M.gapX=gapX;
 for(const p of pb28Ports(b))for(let i=0;i<count;i++){const a=Math.PI/2+(i-(count-1)/2)*2.05/(count-1)+(M.wave%2?.055:-.055),hitX=p.x+Math.cos(a)/Math.sin(a)*(VH-38-p.y);
  if(Math.abs(hitX-gapX)<53)continue;plan.push({id:p.id,a});}
 return plan;}
function pb28Wave(b){const M=b._pb28;let emitted=0;
 for(const L of M.plan){const p=pb28Port(b,L.id);if(!p||M.hidden||pb28Count(b)>=PB28.maxRounds)continue;
  const speed=[3.2,3.6,4.0,4.3][M.rank],q=eShootT(p.x,p.y,L.a,speed,'emissile',{owner:b,w:9,h:19,silent:true,noMuzzle:true});Object.assign(q,{_pb28Owner:b,_pb28Part:p.id,_pb28Type:'missile',_noArsenal:true,_boss:true,_committed:true,homing:false,_shootable:true,hp:1,spd:speed,ang:L.a});M.pods[p.id]=0;emitted++;pb28Log(b,'missile-release',{part:p.id,x:p.x,y:p.y,angle:L.a,gap:M.gapX});}
 const columns=[.12,.28,.50,.72,.88].map(f=>camLeftX()+viewW()*f).filter(x=>Math.abs(x-M.gapX)>68),ports=pb28Ports(b);
 ports.forEach((p,i)=>{if(columns.length)pb28Bomb(b,p,{x:columns[(M.wave+i)%columns.length],y:VH-84+(M.wave%2)*22},[1.18,1.05,.96,.88][M.rank]);});
 if(emitted)combatAudio0927(b,'enemyMissile',.2);pb28Log(b,'ambush-wave',{wave:M.wave,missiles:emitted,gap:M.gapX,live:pb28Count(b)});M.wave++;
}
function pb28Tick(b,dt){const B=b._bomber;if(b.dead){pb28Cancel(b,true);return PB28.base.tick.call(this,b,dt);}
 if(b.enter||B.mode==='entry')return PB28.base.tick.call(this,b,dt);
 if(!b._pb28)pb28Init(b);const M=b._pb28;M.clock+=dt;M.t+=dt;B.clock+=dt;B.t+=dt;b.flash=Math.max(0,(b.flash||0)-dt);for(const p of B.parts)p.flash=Math.max(0,p.flash-dt);
 b._hc1007.clock+=dt;b._hc1007.age=M.t;b._hc1007.lines=[];b._hc1007.cross=null;B.bombs=B.bombs.filter(q=>!q.dead);
 for(const k of Object.keys(M.pods))M.pods[k]+=dt;pb28BombTick(b);
 const engines=B.parts.filter(p=>p.id.startsWith('engine')&&p.hp>0).length,move=.55+engines*.225,home=b.ty,center=camLeftX()+viewW()/2,left=camLeftX()+b.w*.53,right=camRightX()-b.w*.53;
 if(M.mode==='weave'){
  M.hidden=false;const tx=clamp(center+Math.sin(M.clock*.95)*Math.min(92,(right-left)*.48)*move+Math.sin(M.clock*2.1)*12,left,right);b.x+=clamp(tx-b.x,-92*move*dt,92*move*dt);b.y=home+Math.sin(M.clock*1.8)*9;
  M.cd-=dt;if(M.cd<=0){const ports=pb28Ports(b),p=ports[M.serial++%Math.max(1,ports.length)],T=targetShip(b.x,b.y);pb28Bomb(b,p,{x:clamp(T.x+(M.serial%2?48:-48),camLeftX()+34,camRightX()-34),y:clamp(T.y,viewTopY()+240,VH-55)},[1.35,1.15,1.02,.94][M.rank]);M.cd=[1.45,1.18,1.00,.86][M.rank];}
  if(M.t>=[6.2,5.8,5.2,4.8][M.rank])pb28Mode(b,pb28Ports(b).length?'spool':'recover');
 }else if(M.mode==='spool'){b.y=M.from.y+Math.sin(M.t*12)*2;if(M.t>=.65)pb28Mode(b,'boost');}
 else if(M.mode==='boost'){const u=clamp(M.t/(1.25+(2-engines)*.28),0,1);b.y=lerp(M.from.y,viewTopY()-b.h-32,u*u);b.x=lerp(M.from.x,clamp(center+Math.sin(M.clock)*65,left,right),u);M.hidden=b.y+b.h*.62<viewTopY();if(u>=1)pb28Mode(b,'ahead');}
 else if(M.mode==='ahead'){
  const T=targetShip(b.x,b.y),front=clamp((VH*.70-T.y)/(VH*.50),0,1);M.catchup+=dt*(.32+front*1.8);M.hidden=true;
  if(M.catchup>=1.2||M.t>=3.7)pb28Mode(b,'reacquire');
 }else if(M.mode==='reacquire'){const u=clamp(M.t/1.3,0,1),s=u*u*(3-2*u);b.x=lerp(M.from.x,M.toX,s);b.y=lerp(M.from.y,home,s);M.hidden=u<.92;if(u>=1)pb28Mode(b,'ambush');}
 else if(M.mode==='ambush'){
  b.x=clamp(M.baseX+Math.sin(M.clock*.8)*5,left,right);b.y=home+Math.sin(M.clock*1.5)*5;
  combatWarningTick(b,'pb28-wave-'+M.seq+'-'+M.wave,M.t-M.previewAt,M.fireAt-M.previewAt);
  if(M.t>=M.fireAt){pb28Wave(b);if(M.wave>=[4,5,6,7][M.rank])pb28Mode(b,'recover');else{M.previewAt=M.t;M.fireAt=M.t+[.88,.76,.67,.59][M.rank];M.plan=pb28Plan(b);}}
 }else if(M.mode==='recover'){b.y+=(home-b.y)*Math.min(1,dt*3);if(M.t>=2.1)pb28Mode(b,'weave');}
 b._drawY=b.y;
}
siegeBomberTick=function(b,dt){return pb28Own(b)?pb28Tick(b,Math.min(.05,dt)):PB28.base.tick.apply(this,arguments);};
siegeBomberHit=function(b){if(pb28Own(b)&&b._pb28?.hidden)return;const out=PB28.base.hit.apply(this,arguments);if(pb28Own(b)&&b.dead)pb28Cancel(b,true);return out;};
siegeBomberAt=function(b){return pb28Own(b)&&b._pb28?.hidden?null:PB28.base.at.apply(this,arguments);};
siegeBomberBeam=function(b){return pb28Own(b)&&b._pb28?.hidden?null:PB28.base.beam.apply(this,arguments);};
siegeBomberTargets=function(b){return pb28Own(b)&&b._pb28?.hidden?[]:PB28.base.targets.apply(this,arguments);};
polishBlit=function(name,i,x,y,w,h,flash){if(PB28.drawing&&name==='bomber'&&i===2){const b=PB28.drawing,M=b._pb28,p=siegeBomberParts(b).find(p=>p.cell===2&&Math.abs(p.x-x)<1),age=M?.pods[p?.id]??99;
 let frame=0;const pending=groundTargetingFx.find(q=>q._pb28Owner===b&&q._pb28Part===p?.id&&!q.dead&&!q._pb28Released);
 if(pending)frame=Math.min(7,2+Math.floor(pending.t/pending._pb28DropAt*5));else if(M?.mode==='ambush')frame=M.wave?7:Math.min(7,2+Math.floor(M.t/Math.max(.1,M.fireAt)*5));else if(age<.65)frame=Math.min(15,8+Math.floor(age/.65*8));
 return pb28Blit('bay',frame,x,y,flash>0);}return PB28.base.blit.apply(this,arguments);};
function pb28Warnings(b){const M=b._pb28;if(!M||b.dead)return;
 if(M.mode==='reacquire')combatWarningDraw(b,{x:M.toX,y:viewTopY(),ex:M.toX,ey:b.ty+b.h*.65,width:b.w*.8,progress:clamp(M.t/1.3,0,1),fieldOnly:true});
 if(M.hidden)return;
 if(M.mode==='ambush')for(const L of M.plan){const p=pb28Port(b,L.id);if(p)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(L.a)*VH*1.5,ey:p.y+Math.sin(L.a)*VH*1.5,width:12,progress:clamp((M.t-M.previewAt)/(M.fireAt-M.previewAt),0,1),fieldOnly:true,alpha:.22});}
 for(const q of groundTargetingFx)if(q._pb28Owner===b&&!q.dead&&!q.impact){const p=q._pb28Released?q._pb28Source:pb28Port(b,q._pb28Part);if(!p)continue;
  if(!q._pb28Released)combatWarningDraw(b,{x:p.x,y:p.y,ex:q.x,ey:q.y,width:14,progress:clamp(q.t/q.warn,0,1),fieldOnly:true,alpha:.25});
  else{const u=clamp((q.t-q._pb28DropAt)/(q.warn-q._pb28DropAt),0,1);pb28Blit('bomb',Math.floor(u*16),lerp(p.x,q.x,u),lerp(p.y,q.y,u)-Math.sin(u*Math.PI)*18);}}
}
siegeBomberDraw=function(b){if(!pb28Own(b))return PB28.base.draw.apply(this,arguments);pb28Warnings(b);const old=PB28.drawing;PB28.drawing=b;try{PB28.base.draw.apply(this,arguments);
 if(!b.dead&&!b._bomber.parts.some(p=>p.id.startsWith('laser')&&p.hp>0)&&b._bomber.core>0)PB28.base.blit('bomber',3,b.x,b.y+b.h*.23,b.w*.12,b.h*.30,b.flash);
 }finally{PB28.drawing=old;}};
drawCombatFinalProjectile=function(q){if(q._pb28Type==='missile'||q._pb28Type==='fragment'){const name=q._pb28Type,a=PB28_ART[name],dir=pb28Dir(Math.atan2(q.vy,q.vx));return pb28Blit(name,Math.floor(projectileVisualAge(q)*20)%4*64+dir,q.x,q.y);}return PB28.base.projectile.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._pb28Type?null:PB28.base.element.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){if(q?._pb28Type)return q._pb28Type==='missile';return PB28.base.intercept.apply(this,arguments);};
globalThis.BOF_PURSUIT_BOMBER_1027=PB28;
