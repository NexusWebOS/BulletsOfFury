'use strict';
/* First-body part budget, eye weapon and the authored symbiote rebirth reel. */
const RB23={events:[],base:{enter:v18Enter,hit:modularHit,at:r30At,targets:retinaBossTargets,
 attack:v18StartAttack,attackTick:v18AttackTick,tick:r30Tick,draw:r30DrawBoss,body:v18Body,
 break:r30Break,spawn:spawnBoss,player:drawPlayer,arena:v17ArenaDraw,load:stageLoadBegin}};
function rb23Host(b){return v18Owned(b)&&j3State(b).encounter===0;}
function rb23Log(event,data={}){RB23.events.push({event,t:boss?._r30?.clock,...data});if(RB23.events.length>400)RB23.events.shift();}
function er23ArtKeys(){return [...Object.values(ER23_ART.banks).flatMap(a=>[a.key,a.key+'_hit']),...Object.values(ER23_ART.images).map(a=>a.key)];}
for(const a of Object.values(ER23_ART.banks)){XART._src[a.key]=a.path;XART._src[a.key+'_hit']=a.path.replace('.webp','_hit.webp');}
for(const [alias,a]of Object.entries(ER23_ART.images)){XART._src[a.key]=a.path;if(!alias.startsWith('er23_'))XART._src[alias]=a.path;}
function er23DrawBank(name,frame,x,y,flash=false){const a=ER23_ART.banks[name];if(!a)return false;const key=a.key+(flash?'_hit':'');if(!XART.rdy(key))return false;
 const f=clamp(frame|0,0,a.count-1);ctx.drawImage(XART.get(key),(f%a.cols)*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.w,a.h);return true;
}
function er23Curtain(name,step){const a=ER23_ART.banks[name];if(!a||step<=0)return;step=clamp(step|0,0,16);for(let y=viewTopY();y<viewTopY()+viewH();y+=64)for(let x=camLeftX();x<camRightX();x+=64)er23DrawBank(name,step,x,y);}
stageLoadBegin=function(n,keys){const extra=n===8?er23ArtKeys():n===5?Object.entries(ER23_ART.banks).filter(([name])=>/blue_charge|stun|shield_wall|ball_flash/.test(name)).flatMap(([,a])=>[a.key,a.key+'_hit']):n===3?Object.values(ER23_ART.frost).flatMap(a=>[a.key,a.key+'_hit']):[];
 return RB23.base.load.call(this,n,[...(keys||[]),...extra,...(n===5?hf22Keys(5,true):[])]);};
function rb23Budget(b){if(!rb23Host(b))return;const N=b._r30.v18;if(N.rb23Budget===b.maxhp)return;N.rb23Budget=b.maxhp;
 const left=b.parts.find(p=>p.id==='left'),right=b.parts.find(p=>p.id==='right'),core=b.parts.find(p=>p.id==='core');
 left.hp=left.maxhp=Math.floor(b.maxhp*.333);right.hp=right.maxhp=Math.floor(b.maxhp*.333);core.hp=core.maxhp=b.maxhp-left.hp-right.hp;
 b.hp=b.maxhp;rb23Log('host-budget',{left:left.hp,right:right.hp,body:core.hp,total:b.maxhp});
}
function rb23Arms(b){return b.parts.filter(p=>p.id!=='core'&&!p.destroyed&&p.hp>0);}
v18Enter=function(b,n,form=0){const r=RB23.base.enter.apply(this,arguments);if(n===0){b._r30.v18.rb23Budget=null;rb23Budget(b);}return r;};
modularHit=function(dmg){const b=boss;if(!rb23Host(b))return RB23.base.hit.apply(this,arguments);if(!r30Live(b)||b._noHit||!(dmg>0))return;
 rb23Budget(b);const p=b.parts.includes(b._lastPart)?b._lastPart:b.parts[0];if(!p||p.destroyed)return;
 if(p.id==='core'&&rb23Arms(b).length){p.flash=.12;weaponHitSfx('shield');return;}
 const d=Math.min(dmg,p.hp);p.hp-=d;p.flash=.16;stageStats.dmgDealt+=d;
 if(p.hp<=0&&p.id!=='core'){v18Rupture(b,p);p.destroyed=true;b._r30.v18.beams=b._r30.v18.beams.filter(L=>L.module!==p.id);r30Sound('combatModule0927');rb23Log('arm-destroyed',{id:p.id});
  if(!rb23Arms(b).length){v18Clear(b);b._r30.cd=.4;rb23Log('rolling-core-exposed');}}
 b.hp=b.parts.reduce((n,q)=>n+Math.max(0,q.hp),0);if(b.hp<=0)r30Break(b);
};
r30At=function(b,x,y){if(!rb23Host(b))return RB23.base.at.apply(this,arguments);if(!r30Live(b)||b._noHit)return null;
 const A=b._r30.v18.attack;if(!rb23Arms(b).length&&A?.type==='rb23-roll')return Math.hypot(x-b.x,y-b.y)<92?b.parts[0]:null;
 const frame=v18Frame(b),k=v18Size(b)/320,px=Math.floor((x-b.x)/k+160),py=Math.floor((y-b.y)/k+160);
 for(const p of b.parts.slice().reverse())if(!p.destroyed){const a=frame[p.id],m=v18Mask(a);if(m&&px>=0&&py>=0&&px<a.w&&py<a.h&&m[py*a.w+px]>48)return p;}return null;
};
retinaBossTargets=function(b){if(!rb23Host(b))return RB23.base.targets.apply(this,arguments);if(!r30Live(b)||b._noHit)return [];
 const live=rb23Arms(b),parts=live.length?live:[b.parts[0]];
 return parts.map(p=>retinaDynamicPiece(b,'rb23-'+p.id,p.id==='core'?'exposed rolling core':'arm',()=>{const q=rb23PartPoint(b,p);return {...q,hp:p.hp,dead:p.destroyed||!rb23Host(b)||b.dead};},d=>{b._lastPart=p;hitBoss(d);},70,100));
};
function rb23PartPoint(b,p,muzzle=false){const a=v18Frame(b)[p.id],k=v18Size(b)/320,r=a.bounds;return{x:b.x+((r[0]+r[2])/2-160)*k,y:b.y+((muzzle?r[3]-12:(r[1]+r[3])/2)-160)*k};}
function rb23Eye(b){const m=V18_ART.models.infused,f=Math.floor(b._r30.clock*m.fps)%m.frames.length,p=ER23_ART.hostEyes[f],k=v18Size(b)/320;return {x:b.x+(p[0]-160)*k,y:b.y+(p[1]-160)*k};}
function rb23Path(b,n){const left=camLeftX()+110,right=camRightX()-110,top=viewTopY()+140,bot=VH-130,mid=(left+right)/2;
 if(n%4===0)return [{x:left,y:top+60},{x:right,y:top+60},{x:left,y:bot},{x:right,y:bot}];
 if(n%4===1)return [{x:mid,y:top},{x:mid,y:bot},{x:left,y:top},{x:right,y:bot}];
 if(n%4===2)return [{x:left,y:top},{x:right,y:bot},{x:right,y:top},{x:left,y:bot}];
 return Array.from({length:7},(_,i)=>({x:lerp(left,right,i/6),y:lerp(top,bot,.5+.42*Math.sin(i/6*TAU))}));
}
v18StartAttack=function(b){if(!rb23Host(b))return RB23.base.attack.apply(this,arguments);const N=b._r30.v18;
 N.rb23Seq=(N.rb23Seq||0)+1;
 const T=targetShip(b.x,b.y),roll=!rb23Arms(b).length,pincer=!roll&&N.rb23Seq%2===0,P=N.attack={type:roll?'rb23-roll':pincer?'rb23-pincer':'rb23-eye',t:0,tell:roll?1.2:1.1,active:roll?6.8:pincer?2.3:1.35,origin:{x:b.x,y:b.y},lanes:[],targets:[],ports:[],tx:T.x,ty:T.y,n:0,next:0,move:0,path:rb23Path(b,N.rb23Seq),beamClock:0,beamPhase:'ready',beamCount:0};
 b._r30.attack=P;P.eye=rb23Eye(b);
 if(pincer){for(const p of rb23Arms(b)){const q=rb23PartPoint(b,p,true),a=Math.atan2(T.y-q.y,T.x-q.x);for(const off of [-.18,0,.18])P.lanes.push({...q,ex:q.x+Math.cos(a+off)*VH,ey:q.y+Math.sin(a+off)*VH,width:20,module:p.id,angle:a+off});}}
 else P.lanes=[{x:P.eye.x,y:P.eye.y,ex:P.eye.x,ey:VH+100,width:34,module:'core'}];r30Sound('bossWeaponCharge');rb23Log('host-attack',{type:P.type});
};
function rb23BeamHit(b,P,direction){const eye=P.type==='rb23-roll'?{x:b.x,y:b.y}:rb23Eye(b),width=13;
 for(const seat of seatList())withSeat(seat,()=>{if(player.dead)return;const hit=direction==='down'?player.y>=eye.y&&player.y<=eye.y+600&&Math.abs(player.x-eye.x)<width+4:Math.abs(player.y-eye.y)<width+4&&(direction==='right'?player.x>=eye.x&&player.x<=eye.x+600:player.x<=eye.x&&player.x>=eye.x-600);if(hit)playerHit('Dracodia red eye laser');});
}
v18AttackTick=function(b,dt){const P=b?._r30?.v18?.attack;if(!rb23Host(b)||!P?.type.startsWith('rb23-'))return RB23.base.attackTick.apply(this,arguments);
 const N=b._r30.v18,S=b._r30;P.t+=dt;const u=P.t-P.tell;P.eye=rb23Eye(b);
 if(u<0){combatWarningTick(b,'dracodia-eye-'+N.rb23Seq,P.t,P.tell);if(P.type==='rb23-eye'){b.x+=clamp(P.tx-b.x,-90*dt,90*dt);P.eye=rb23Eye(b);P.lanes[0].x=P.lanes[0].ex=P.eye.x;P.lanes[0].y=P.eye.y;}return;}
 if(P.type==='rb23-pincer'){
  if(u>=P.next&&P.n<4){P.next+=.4;P.n++;for(const L of P.lanes){const p=b.parts.find(p=>p.id===L.module);if(!p||p.destroyed)continue;const q=rb23PartPoint(b,p,true);v18Shot(b,q,L.angle,3.0+target17Rank()*.2,'code');}r30Sound('enemyBossCannon');}
 }else if(P.type==='rb23-eye'){if(!P.fired){P.fired=true;r30Sound('combatBeam0927');}rb23BeamHit(b,P,'down');}
 else{
  P.beamClock+=dt;if(P.beamPhase==='ready'){
   P.move+=dt;const v=clamp(P.move/5.2,0,.9999)*(P.path.length-1),i=Math.floor(v),f=v-i,a=P.path[i],z=P.path[i+1];b.x=lerp(a.x,z.x,f);b.y=lerp(a.y,z.y,f);P.eye={x:b.x,y:b.y};
   if(P.beamClock>.8){P.beamPhase='tell';P.beamClock=0;P.direction=b.x<(camLeftX()+camRightX())/2?'right':'left';r30Sound('bossWeaponCharge');}
  }else if(P.beamPhase==='tell'){combatWarningTick(b,'rolling-eye-'+N.rb23Seq+'-'+P.beamCount,P.beamClock,.60);if(P.beamClock>=.60){P.beamPhase='fire';P.beamClock=0;r30Sound('combatBeam0927');}}
  else{rb23BeamHit(b,P,P.direction);if(P.beamClock>.42){P.beamPhase='ready';P.beamClock=0;P.beamCount++;if(P.beamCount%2===0){const T=targetShip(b.x,b.y);d20Bomb(b,{x:clamp(T.x,camLeftX()+60,camRightX()-60),y:clamp(T.y,viewTopY()+210,VH-60)});}}}
  for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-b.x,player.y-b.y)<62)playerHit('Dracodia rolling core');});
 }
 if(u>=P.active){N.attack=null;S.attack=null;S.cd=.8;N.home={x:clamp(b.x,camLeftX()+100,camRightX()-100),y:clamp(b.y,viewTopY()+140,viewTopY()+260)};j3State(b).attacks++;}
 b._drawY=b.y;
};
v18Body=function(b){if(!rb23Host(b))return RB23.base.body.apply(this,arguments);const P=b._r30.v18.attack;
 if(!rb23Arms(b).length&&P?.type==='rb23-roll')return er23DrawBank(P.t<P.tell?'fold':'roll',P.t<P.tell?Math.min(8,Math.floor(P.t/P.tell*9)):Math.floor((P.t-P.tell)*24)%ER23_ART.banks.roll.count,b.x,b.y,b.parts[0].flash>0);
 const frame=v18Frame(b),n=Math.floor(b._r30.clock*V18_ART.models.infused.fps)%16;
 for(const p of b.parts){if(p.destroyed)continue;let a=frame[p.id];
  if(p.id==='core'&&P?.type==='rb23-eye'&&P.t<P.tell){const phase=Math.min(2,Math.floor(P.t/P.tell*3)),q=ER23_ART.images['er23_host_core_'+n+'_charge'+phase];if(q)a={...a,key:q.key};}
  v18Cell(a,b.x,b.y,v18Size(b));if(p.flash>0)v18Cell(a,b.x,b.y,v18Size(b),1,true);
 }
};
function rb23DrawWeapon(b){const P=b._r30.v18.attack;if(!P?.type.startsWith('rb23-'))return;
 if(P.type==='rb23-pincer'){if(P.t<P.tell)for(const L of P.lanes)combatWarningDraw(b,{...L,progress:P.t/P.tell,fieldOnly:true});return;}
 const u=P.t-P.tell,eye=P.type==='rb23-roll'?{x:b.x,y:b.y}:rb23Eye(b),dir=P.type==='rb23-roll'?P.direction:'down',fire=P.type==='rb23-roll'?P.beamPhase==='fire':u>=0&&u<P.active;
 if(P.type==='rb23-eye'&&u<0)combatWarningDraw(b,{x:eye.x,y:eye.y,ex:eye.x,ey:VH+100,width:34,progress:P.t/P.tell,fieldOnly:true});
 if(P.type==='rb23-roll'&&P.beamPhase==='tell')combatWarningDraw(b,{x:eye.x,y:eye.y,ex:dir==='right'?camRightX()+40:camLeftX()-40,ey:eye.y,width:34,progress:P.beamClock/.60,fieldOnly:true});
 if(fire)er23DrawBank('laser_'+dir,Math.floor((P.type==='rb23-roll'?P.beamClock:u)*24)%16,eye.x,eye.y);
}

spawnBoss=function(){const r=RB23.base.spawn.apply(this,arguments),b=boss;if(rb23Host(b)){const N=b._r30.v18;N.rb23Entrance={ships:seatList().map(seat=>withSeat(seat,()=>({seat,x:player.x,y:player.y}))),portal:{x:worldWidth()/2,y:VH-220}};v18SetMode(b,'dr5er23entry');rb23Budget(b);rb23Log('arena-teleport-start');}return r;};
r30Break=function(b){if(!rb23Host(b))return RB23.base.break.apply(this,arguments);if(rb23Arms(b).length)return;
 v18Clear(b);b.hp=0;b.enter=b._noHit=true;b._r30.mode='dr5er23rebirth';b._r30.t=0;b._r30.v18.rb23Rebirth={from:{x:b.x,y:b.y},burst:-1,bolts:0};dr5Ships(b);dr5State(b).radio=null;Audio.stopMusic();r30Sound('expBig');rb23Log('host-fall-start');};
function rb23SceneTick(b,dt){const S=b._r30,N=S.v18,D=dr5State(b);dr5Protect(b,dt);const t=S.t;
 if(S.mode==='dr5er23entry'){
  const E=N.rb23Entrance;if(!E)return;const u=clamp(t/1.2,0,1);
  for(const q of E.ships)withSeat(q.seat,()=>{player.x=lerp(q.x,E.portal.x,u);player.y=lerp(q.y,E.portal.y,u);});
  if(t>=1.25&&!E.swapped){E.swapped=true;N.arenaPhase=0;r30Sound('teleportIn');rb23Log('arena-teleported');}
  if(t>=2.8){for(const q of E.ships)withSeat(q.seat,()=>{player.x=q.x;player.y=q.y;});N.rb23Entrance=null;b.y=viewTopY()-180;v18SetMode(b,'v18arrival');}
  return;
 }
 const R=N.rb23Rebirth,cy=viewTopY()+viewH()*.38,cx=(camLeftX()+camRightX())/2;
 if(t<4){b.x=R.from.x;b.y=R.from.y+t*t*65;const beat=Math.floor(t/.12);if(beat!==R.burst){R.burst=beat;explode(b.x+Math.sin(beat*2.1)*65,Math.min(VH-15,b.y)+Math.cos(beat*2.3)*35,65,'purple');if(beat%4===0)r30Sound('expBig');}
  if(t>2.3){explode(cx+Math.sin(t*17)*80,VH-20-(t-2.3)*90,45,'purple');}return;}
 if(t>=4&&!R.line1){R.line1=true;dr5Say(b,run.pilot.toUpperCase(),'What the heck was that?');rb23Log('pilot-question');}
 if(t>=6.4&&!R.line2){R.line2=true;dr5Say(b,run.pilot.toUpperCase(),"Uhh, what's going on...?");}
 if(t>=10.4&&!R.silence){R.silence=true;dr5Say(b,run.pilot.toUpperCase(),'...');r30Sound('combatAlien0927');rb23Log('symbiote-heart-rise');}
 if(t>=14&&!R.fuse){R.fuse=true;D.radio=null;r30Sound('teleportIn');rb23Log('matter-fusion');}
 if(t>=17&&t<23){const u=(t-17)/6,n=Math.min(24,Math.floor(24*Math.pow(u,1.65)));
  while(R.bolts<n){R.bolts++;r30Sound('combatBeam0927');rb23Log('corrupted-lightning',{number:R.bolts});}R.boltPhase=(24*Math.pow(u,1.65))%1;}
 if(t>=23&&R.bolts<24){R.bolts=24;rb23Log('corrupted-lightning',{number:24});r30Sound('bossWeaponCharge');}
 if(t>=25.6&&!R.swapped){R.swapped=true;v18Enter(b,2,0);N.rb23Rebirth=R;N.arenaPhase=2;S.mode='dr5er23rebirth';S.t=t;b.x=cx;b.y=cy;D.radio=null;rb23Log('final-arena-whiteout');r30Sound('expBig');}
 if(t>=28.5){N.rb23Rebirth=null;D.radio=null;dr5Ships(b);S.mode='dr5Monologue';S.t=0;b.enter=b._noHit=true;D.line=0;rb23Log('rebirth-complete');bossPhaseMusic(8,3);}
}
r30Tick=function(b,dt){if(!v18Owned(b))return RB23.base.tick.apply(this,arguments);if(b._r30.mode.startsWith('dr5er23'))return rb23SceneTick(b,clamp(dt||0,0,.05));rb23Budget(b);return RB23.base.tick.apply(this,arguments);};
function rb23SceneDraw(b){const S=b._r30,N=S.v18,t=S.t,cx=(camLeftX()+camRightX())/2,cy=viewTopY()+viewH()*.38;
 if(S.mode==='dr5er23entry'){const E=N.rb23Entrance;if(!E)return;er23DrawBank('portal',Math.floor(t*16)%16,E.portal.x,E.portal.y);if(t>=1.10&&t<1.65)er23Curtain('blackout',16);return;}
 if(t<4){v18Body(b);return;}
 if(t<7)return;
 const dark=t<11?Math.floor(clamp((t-9)/2,0,1)*12):t<25.6?12:0;er23Curtain('blackout',dark);
 if(t<14){const rise=clamp((t-7)/3.4,0,1),x=cx+Math.sin((t-7)*2)*Math.min(70,(t-7)*16),y=lerp(VH+170,cy,rise)+Math.cos(t*3)*16;er23DrawBank('symbiote',Math.floor(t*20)%ER23_ART.banks.symbiote.count,x,y);}
 else if(t<17)er23DrawBank('fusion',Math.min(8,Math.floor((t-14)/3*9)),cx,cy);
 else if(t<25.6){er23DrawBank('fusion',8,cx,cy);
  if(t<23&&N.rb23Rebirth?.boltPhase<.6){const n=N.rb23Rebirth.bolts,angle=n*2.39996;er23DrawBank('lightning',Math.floor(t*24)%16,cx+Math.cos(angle)*110,cy+Math.sin(angle)*100);}
  if(t>=23){er23DrawBank('lightning',Math.floor(t*28)%16,cx,cy);er23DrawBank('storm',Math.floor(t*18)%16,cx,cy);}
 }else RB23.base.draw(b);
 if(t>=25.3){const step=t<25.6?Math.floor((t-25.3)/.3*16):16-Math.floor(clamp((t-25.9)/2.6,0,1)*16);er23Curtain('whiteout',step);}
}
r30DrawBoss=function(b){if(v18Owned(b)&&b._r30.mode.startsWith('dr5er23'))return rb23SceneDraw(b);const r=RB23.base.draw.apply(this,arguments);if(rb23Host(b))rb23DrawWeapon(b);return r;};
drawPlayer=function(){const E=rb23Host(boss)&&boss._r30.v18.rb23Entrance;if(E&&boss._r30.t>1.1&&boss._r30.t<1.65)return;return RB23.base.player.apply(this,arguments);};
v17ArenaDraw=function(b){if(v18Owned(b)&&b._r30.mode==='dr5er23entry'&&b._r30.t<1.25)return false;return RB23.base.arena.apply(this,arguments);};aa5ArenaDraw=v17ArenaDraw;
window.BOF_DRACODIA_REBIRTH=RB23;
const rb23Warnings=v18Warnings;v18Warnings=function(b){if(b?._r30?.v18?.attack?.type.startsWith('rb23-'))return;return rb23Warnings.apply(this,arguments);};
