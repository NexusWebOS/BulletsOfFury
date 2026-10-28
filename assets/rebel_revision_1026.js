"use strict";
/* Mike's live shield rescue, spectre cloak and interceptable heavy arsenal.
   Existing HP, part damage, FOV, audio and defeat owners remain authoritative. */
const RR26={base:{tick:rebelSquadTick,draw:rebelSquadDraw,ship:fr27RebelDrawShip,
 attack:rg4Attack,act:rg4AttackTick,round:rg4Round,hit:rg4OrdnanceHit,ord:rg4OrdnanceDraw,
 helix:ra4Helix,nova:ra4Nova,supply:s6SupplyTick,supplyDraw:s6SupplyDraw,
 fleet:rd21Fleet,update:updatePlay,world:drawWorld},events:[],cache:new Map()};
XART._src.rr26_wall='assets/game/levels/stage_06/boss/rebel_revision_1026/wall.png';
XART._src.rr26_box='assets/game/levels/stage_06/boss/rebel_revision_1026/wall_box.png';
function rr26Log(kind,data={}){RR26.events.push({kind,t:rg4State()?.age||0,...data});if(RR26.events.length>300)RR26.events.shift();}
function rr26State(G){return G.rr26||(G.rr26={queue:[],returns:[],wall:null,box:false});}
function rr26Warm(){if(!RR26.humWarm&&Snd.pools.helixCharge){Snd.pools.rr26WallHum=Snd.pools.helixCharge;Snd.loopPrepare('rr26WallHum');RR26.humWarm=true;}XART.rdy('rr26_wall');XART.rdy('rr26_box');for(const id of REBEL_KEYS){const d=AM13_ART[id];if(d)XART.rdy(d.heading.key);}for(let i=0;i<8;i++)XART.rdy('florb_'+i);}
rr26Warm();
function rr26Damage(q,dmg){if(!boss||boss.dead||!rd21Live(q))return;boss._rebels.hit=q.i;rebelSquadDamage(boss,dmg);}
function rr26Burst(G,o){if(o._rr26Burst)return;o._rr26Burst=true;G.novaFx.push({x:o.x,y:o.y,t:0,dur:.55});
 let hit=0;for(const q of boss._rebels.ships)if(rd21Live(q)&&Math.hypot(q.x-o.x,q.y-o.y)<210){rr26Damage(q,22);hit++;}
 (Audio.SFX.helixBurst||Audio.SFX.expSmall)?.();rr26Log('helix-counterburst',{hit});}
rg4OrdnanceHit=function(G,o,dmg){const alive=!o.dead,r=RR26.base.hit.apply(this,arguments);if(alive&&o.dead&&o.kind==='helix')rr26Burst(G,o);return r;};
ra4Helix=function(q,G,A){const n=G.ord.length,r=RR26.base.helix.apply(this,arguments);for(const o of G.ord.slice(n)){o.hp=o.max=6;o.life=3.2;o._rr26Energy=true;}return r;};
ra4Nova=function(G,o){if(o.kind==='helix'){if(o.burst)return;o.burst=true;o.dead=true;for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-o.x,player.y-o.y)<42)playerHit('rebel helix burst');});G.novaFx.push({x:o.x,y:o.y,t:0,dur:.55});Audio.SFX.helixBurst?.();return;}return RR26.base.nova.apply(this,arguments);};
function rr26Energy(q,G,a,large=false,x=q.x,y=q.y+32){const o={kind:'energy',owner:q,x,y,vx:Math.cos(a)*(large?125:155),vy:Math.sin(a)*(large?125:155),r:large?23:12,hp:large?6:2,max:large?6:2,t:0,life:5,split:true,bounces:0,flash:0,_rr26Energy:true};G.ord.push(o);rr26Log('energy-launch',{pilot:q.key,large});return o;}
// Replace dense tracer streams with distinct, slower, destructible energy charges.
rg4Round=function(q,a,speed,kind,extra={}){const G=rg4State();if(!G)return RR26.base.round.apply(this,arguments);
 const owner=extra.owner||boss._rebels.ships.find(s=>s===q)||boss._rebels.ships.filter(rd21Live).sort((s,t)=>Math.hypot(s.x-q.x,s.y-q.y)-Math.hypot(t.x-q.x,t.y-q.y))[0];
 if(!owner)return RR26.base.round.apply(this,arguments);
 if(['kaia','rook'].includes(owner.key))return {dead:true,x:q.x,y:q.y+32};
 if(G.age<(owner._rr26RoundAt||0))return {x:q.x,y:q.y+32,vx:0,vy:0,dead:true};
 owner._rr26RoundAt=G.age+.65;if(owner.key==='jace')return rr36Bullet(owner,q.x,q.y+32,a,speed);return rr26Energy(owner,G,a,false,q.x,q.y+32);
};
for(const C of Object.values(RBAL19.cfg)){C.slots=1;C.heavySlots=0;C.tell=Math.max(.65,C.tell);C.cd=Math.max(1.5,C.cd);}
rg4Attack=function(q,R,G,forced){const kind=forced||q.rg4.armed;
 if(kind==='fusion'){q.rg4.armed=null;const A=rd21Personal(q,R,G,'rr26cannon');A.warm=1.65;return A;}
 const result=RR26.base.attack.apply(this,arguments);if(q.rg4?.act?.kind==='fusion'){const A=rd21Personal(q,R,G,'rr26cannon');A.warm=1.65;return A;}return result;};
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(A?.kind!=='rr26cannon')return RR26.base.act.apply(this,arguments);
 A.t+=dt;if(A.phase==='charge'){combatWarningTick(A,'rr26cannon',A.t,A.warm);if(A.t>=A.warm){rr26Energy(q,G,A.a,true);A.phase='recover';A.t=0;(Audio.SFX.maverickHelixRelease||Audio.SFX.enemyShoot)?.();}}
 else if(A.t>1.4)rd21Finish(q,G,6);
};
const rr26Warning=rg4Warning;
rg4Warning=function(q,A){if(A?.kind==='rr26cannon'){if(A.phase==='charge')rd21Fov(A,q.x,q.y+32,A.a,50,A.t/A.warm);return;}return rr26Warning.apply(this,arguments);};
rg4OrdnanceDraw=function(o,G){if(o._rr26Energy){const key=o.kind==='helix'?'ra4_nhxsb_g_'+(1+Math.floor(o.t*16)%2):'florb_'+Math.floor(o.t*16)%8;
 if(XART.rdy(key)){const im=o.flash>0?xartTint(key,'#ffffff',1):o.kind==='helix'?XART.get(key):xartPalette(key,RG4_COLORS[o.owner?.key]||'#55ddff'),d=o.r*2.6;ctx.drawImage(im,o.x-d/2,o.y-d/2,d,d);}return;}
 return RR26.base.ord.apply(this,arguments);};
// Replace the rescue scene with a real shootable third Decker supply box.
rg4RescueStart=function(b,G){if(G.rescueDone||b.dead||b._rebels.frStageX||run.stage!==6)return false;G.rescueDone=true;G.scene=null;G.cloak=0;G.shield=0;const S=rr26State(G);S.box=true;
 const d=s6Wing?.ships.find(q=>q.key==='decker'&&q.hp>0)||player;
 if(s6Wing){s6Wing.boxes??=[];s6Wing.boxes.push({key:'decker',x:d.x,y:Math.max(PLAY.y+150,d.y-100),hp:3,t:0,flash:0,open:false,_rr26Wall:true});}
 S.queue.push(['decker','TEAM, GIVE ME A SECOND. I BROUGHT SOMETHING NEW.']);rr26Log('wall-box');return true;};
function rr26Deploy(G){const S=rr26State(G);if(S.wall)return;const caster=s6Wing?.ships.find(q=>q.key==='decker'&&q.hp>0)||player;S.wall={t:0,dur:12.95,hits:0,cast:1.4,build:.65,hold:10,fade:.9,caster,origin:{x:caster.x,y:caster.y-24}};
 S.queue.push(['decker','WALL UP! HOLD FIRE - IT REFLECTS BOTH WAYS!']);Audio.SFX.shieldUp?.();rr26Log('wall-deployed');}
function rr26WallRect(){const w=viewW(),h=(w/3)*96/356;return {x:camLeftX(),y:viewH()/2-h/2,w,h};}
s6SupplyTick=function(W,dt){const special=(W.boxes||[]).filter(o=>o._rr26Wall&&!o.dead);W.boxes=(W.boxes||[]).filter(o=>!o._rr26Wall);RR26.base.supply.apply(this,arguments);
 const G=rg4State();if(!G)return;for(const o of special){o.t+=dt;o.flash=Math.max(0,o.flash-dt);for(const p of pBullets){if(p.dead||(p._wingKey||_pilotKey())!=='decker')continue;
 const beam=p.kind==='beam'?playerBeamRange(p):null,hit=beam?o.y>=beam.top&&o.y<=beam.bot&&Math.abs(o.x-beam.x)<24+beam.half:Math.abs(p.x-o.x)<24+(p.w||6)/2&&Math.abs(p.y-o.y)<24+(p.h||8)/2;
 if(hit){o.hp-=p.dmg||1;o.flash=.14;if(!p.pierce&&!beam)p.dead=true;if(o.hp<=0){o.dead=true;crateBreak(o.x,o.y,'#83dfff');rr26Deploy(G);break;}}}
 if(!o.dead)W.boxes.push(o);}
};
s6SupplyDraw=function(W){const all=W.boxes||[];W.boxes=all.filter(o=>!o._rr26Wall);try{RR26.base.supplyDraw.apply(this,arguments);}finally{W.boxes=all;}
 for(const o of all)if(o._rr26Wall&&!o.dead&&XART.rdy('rr26_box')){const im=o.flash>0?xartTint('rr26_box','#ffffff',1):XART.get('rr26_box');ctx.drawImage(im,o.x-24,o.y-24,48,48);}
};
function rr26Reflect(G,o){const S=rr26State(G),live=boss._rebels.ships.filter(rd21Live);if(!live.length)return;const target=live[(S.wall.hits++)%live.length];
 S.wall.pulse=.2;S.returns.push({x:o.x,y:o.y,target,t:0,r:o.r||12});o.dead=true;if(S.wall.hits===1)S.queue.push(['voss','OUR SHOTS ARE COMING BACK! BREAK FORMATION!'],['cole','HA! YOU BUILT THAT AND NEVER TOLD US?'],['decker','I WAS SAVING IT FOR A GOOD FIRST IMPRESSION.'],['cole','NICK OF TIME, DECKER. NICK OF TIME!']);
 if(S.wall.hits%3===1)Audio.SFX.shieldHit?.();rr26Log('wall-reflect',{target:target.key});}
function rr26WallContact(G,dt){const W=G.rr26?.wall;if(!W||W.t<(W.cast??0)+(W.build??.3)||W.t>W.dur-(W.fade??.3))return;const r=rr26WallRect();
 const crosses=(o,scale)=>{if(o.dead||o._rr26FriendlyReturn)return false;const ny=o.y+(o.vy||0)*dt*scale,rad=(o.r||o.h/2||3);return o.x>=r.x&&o.x<=r.x+r.w&&Math.max(o.y,ny)+rad>=r.y&&Math.min(o.y,ny)-rad<=r.y+r.h;};
 for(const o of eBullets)if(crosses(o,60)){o.y=r.y-8;rr26Reflect(G,o);}
 for(const o of G.ord)if(crosses(o,1)){o.y=r.y-8;rr26Reflect(G,o);}
 for(const p of pBullets){if(p.dead)continue;const beam=p.kind==='beam'?rr26BeamBase(p):null;
  const hit=beam?beam.top<=r.y+r.h&&beam.bot>=r.y&&beam.x>=r.x&&beam.x<=r.x+r.w:crosses(p,60);if(!hit)continue;
  if(beam&&G.age<(p._rr26BounceAt||0))continue;p._rr26BounceAt=G.age+.18;
  const a=beam?Math.PI/2:Math.atan2(-(p.vy||-4),-(p.vx||0)),z=eShootT(clamp(beam?beam.x:p.x,r.x+4,r.x+r.w-4),r.y+r.h+12,a,3.8,'s6orb',{silent:true,w:14,h:14});
  Object.assign(z,{_rr26FriendlyReturn:true,_noArsenal:true,_weaponProof:true});if(!beam)p.dead=true;W.pulse=.2;
  if(G.age>=(W.cueAt||0)){W.cueAt=G.age+.18;Audio.SFX.shieldHit?.();}rr26Log('friendly-reflected',{weapon:p.kind});
 }
}
function rr26BlockShips(G){const W=G?.rr26?.wall;if(!W||W.t<(W.cast??0)+(W.build??.3)||W.t>W.dur-(W.fade??.3))return;const r=rr26WallRect();W.sides??=new WeakMap();
 const block=(q,friendly,radius)=>{if(!q||q.dead||q.out||q.hp<=0)return;let side=W.sides.get(q);if(side==null){side=q.y<r.y?-1:q.y>r.y+r.h?1:friendly?1:-1;W.sides.set(q,side);}
  const limit=side<0?r.y-radius:r.y+r.h+radius;if(side<0?q.y>limit:q.y<limit){q.y=limit;q.vy=0;if(q._drawY!=null)q._drawY=q.y;W.blocks=(W.blocks||0)+1;if(G.age>=(q._rr26BlockLog||0)){q._rr26BlockLog=G.age+.5;rr26Log('wall-block',{pilot:q.key||'player'});}}};
 for(const seat of seatList())withSeat(seat,()=>block(player,true,SHIP_DRAW_H*.42));
 for(const q of s6Wing?.ships||[])block(q,true,SHIP_DRAW_H*.42);
 for(const q of boss?._rebels?.ships||[]){if(typeof vs41Safe==='function'&&vs41Safe(q))continue;block(q,false,SHIP_DRAW_H*.65*(q._rd21Scale||1));}
}
function rr26WallTick(G,dt){const S=rr26State(G),W=S.wall;if(W){W.t+=dt;W.pulse=Math.max(0,(W.pulse||0)-dt);rr26WallContact(G,dt);
 if(Snd.pools.helixCharge){Snd.pools.rr26WallHum??=Snd.pools.helixCharge;Snd.loopOn('rr26WallHum',.30);}
 if(W.t>=W.dur){S.wall=null;Snd.loopOff('rr26WallHum');Audio.SFX.shieldBreak?.();}}
 for(const o of S.returns){o.t+=dt;if(!rd21Live(o.target)){o.target=boss._rebels.ships.find(rd21Live);if(!o.target){o.dead=true;continue;}}
 const dx=o.target.x-o.x,dy=o.target.y-o.y,d=Math.hypot(dx,dy),step=430*dt;if(d<step+20){rr26Damage(o.target,12);o.dead=true;rg4FX(G,2,o.x,o.y,65,.4);rr26Log('reflection-hit',{target:o.target.key});}else{o.x+=dx/d*step;o.y+=dy/d*step;}if(o.t>5)o.dead=true;}
 S.returns=S.returns.filter(o=>!o.dead);
}
const rr26BeamBase=playerBeamRange;
playerBeamRange=function(p){const a=rr26BeamBase.apply(this,arguments),W=rg4State()?.rr26?.wall;if(!a||!W||W.t<(W.cast??0)+(W.build??.3)||W.t>W.dur-(W.fade??.3))return a;const r=rr26WallRect();return a.bot<r.y?a:{...a,top:Math.max(a.top,r.y+r.h)};};
updatePlay=function(dt){const G=rg4State();if(G&&!G.scene){rr26BlockShips(G);rr26WallTick(G,Math.min(.05,dt));}else Snd.loopOff('rr26WallHum');const result=RR26.base.update.apply(this,arguments);rr26BlockShips(rg4State());return result;};
const rr26Projectile=drawCombatFinalProjectile;
drawCombatFinalProjectile=function(p){if(p._rr26FriendlyReturn){const key='florb_'+Math.floor((p.t||0)*16)%8;if(XART.rdy(key))ctx.drawImage(xartPalette(key,'#45ddff'),p.x-13,p.y-13,26,26);return true;}return rr26Projectile.apply(this,arguments);};
// Frame-indexed disappearance and background refraction use the authored alpha mask.
function rr26Pose(q){const d=AM13_ART[q.key],m=d?.heading;if(!m||!XART.rdy(m.key))return null;const a=q.rfHeading??Math.PI/2,f=Math.round(((a-m.startAngle+TAU)%TAU)/TAU*m.frames)%m.frames;
 return {d,m,f,key:m.key,im:XART.get(m.key),sx:f*m.cell};}
function rr26Cloak(q,p,fade){const size=SHIP_DRAW_H*1.5*p.d.referenceRatio*p.m.cell/p.m.span,k=p.key+'-'+p.f;let mask=RR26.cache.get(k);
 if(!mask){mask=document.createElement('canvas');mask.width=mask.height=p.m.cell;mask.getContext('2d').drawImage(p.im,p.sx,0,p.m.cell,p.m.cell,0,0,p.m.cell,p.m.cell);RR26.cache.set(k,mask);}
 const c=RR26.fuzz||(RR26.fuzz=document.createElement('canvas'));c.width=c.height=p.m.cell;const g=c.getContext('2d'),m=ctx.getTransform(),x=m.a*(q.x-size/2)+m.e,y=m.d*(q.y-size/2)+m.f,w=size*m.a,h=size*m.d;
 for(let row=0;row<c.height;row+=2){const shift=((row*17+Math.floor(q.t*16)*13)%7)-3;g.drawImage(ctx.canvas,x+shift,y+row/c.height*h,w,2/c.height*h,0,row,c.width,2);}
 g.globalCompositeOperation='destination-in';g.drawImage(mask,0,0);g.globalCompositeOperation='source-over';ctx.save();ctx.globalAlpha*=fade*.42;ctx.drawImage(c,q.x-size/2,q.y-size/2,size,size);ctx.restore();
}
ra7NyxSpiral=function(){};
const rr26Air=air13DrawRebel;
air13DrawRebel=function(q,opt={}){const p=rr26AnimatedPose(q)||rr26Pose(q);if(!p)return rr26Air.apply(this,arguments);if(q.dead&&!opt.allowDead)return false;
 const fade=Math.round((q._rr26Fade||0)*24)/24,span=SHIP_DRAW_H*1.5*(p.d?.referenceRatio||1);
 
 // All headings use actual cells; no static-hull canvas rotation.
 const alpha=opt.alpha===0?0:q.flash>0?1:1-fade*.98;const angle=(q.rfHeading??Math.PI/2)-Math.PI/2,c=Math.cos(angle),sn=Math.sin(angle),w=SHIP_DRAW_H*1.5,mods=fr27RebelModules(q);
 for(const [a,z,id] of [[-.5,-.17,'left'],[-.17,.17,null],[.17,.5,'right']]){if(id&&mods.find(m=>m.id===id)?.hp<=0)continue;
 ctx.save();ctx.beginPath();const left=a===-.5?-w*3:a*w,right=z===.5?w*3:z*w;
 for(const [i,[x,y]] of [[left,-w*3],[right,-w*3],[right,w*3],[left,w*3]].entries()){const px=q.x+x*c-y*sn,py=q.y+x*sn+y*c;i?ctx.lineTo(px,py):ctx.moveTo(px,py);}ctx.closePath();ctx.clip();if(fade)rr26Cloak(q,p,fade);if(p._af21)af21Draw(p,q.x,q.y,SHIP_DRAW_H*1.5*p.M.referenceRatio,alpha,q.flash>0?'#ffffff':null);else AF21.base.blit(p,q.x,q.y,span,alpha,q.flash>0?'#ffffff':null);ctx.restore();}
 q._air13RenderedKey=p.key;q._air13Frame=p.f;return true;};
// Keep the established formation volley, then split north/south and return continuously.
rd21Fleet=function(b,G,D,dt){const F=D.fleet;if(!F)return;
 if(!['scatter','return'].includes(F.phase)){
  F.t+=dt;G.releaseAt=G.age+2;const live=b._rebels.ships.filter(rd21Live);
  for(const q of live){const home={x:camLeftX()+(q.i+.5)*viewW()/5,y:PLAY.y+85+(q.i%2)*75};
   if(F.phase==='assemble'){const u=clamp(F.t/1.5,0,1),v=u*u*(3-2*u);q.x=lerp(q._rd21From.x,home.x,v);q.y=lerp(q._rd21From.y,home.y,v);q.rfHeading=u<.85?Math.atan2(home.y-q._rd21From.y,home.x-q._rd21From.x):Math.PI/2;}
   else{q.x=home.x;q.y=home.y;q.rfHeading=Math.PI/2;if(q._rd21Volley){q._rd21Volley.t=F.t;combatWarningTick(q._rd21Volley,'rr26-fleet',F.t,q._rd21Volley.warm);}}
  }
  if(F.phase==='assemble'&&F.t>=1.5){F.phase='tell';F.t=0;for(const q of live){const target=ra4Target(q,D.cycle);q._rd21Volley={t:0,warm:1.35,locked:true,target,a:Math.atan2(target.ref.y-q.y,target.ref.x-q.x),shot:0};}Audio.SFX.retinaCharge?.();}
  else if(F.phase==='tell'&&F.t>=1.35){for(const q of live){const A=q._rd21Volley;ra4Rocket(q,G,A);A.shot++;ra4Rocket(q,G,A);q._rd21Volley=null;}F.phase='hold';F.t=0;}
  else if(F.phase==='hold'&&F.t>=.7){F.phase='scatter';F.t=0;}
  return;
 }
 F.t+=dt;G.releaseAt=G.age+2;const live=b._rebels.ships.filter(rd21Live),cx=camLeftX()+viewW()/2;
 for(const q of live){const north=q.i%2===0,side=q.i%2?1:-1;let P=q._rr26Flight;
 if(!P||P.fleet!==F){P=q._rr26Flight={fleet:F,start:{x:q.x,y:q.y},edge:{x:cx+side*(viewW()/2+100),y:north?PLAY.y-120:VH+120},home:{x:cx+(q.i-2)*Math.min(82,(viewW()-112)/4),y:PLAY.y+83+(q.i%2)*46}};}
 const from=F.phase==='scatter'?P.start:P.edge,to=F.phase==='scatter'?P.edge:P.home,u=clamp(F.t/1.1,0,1),v=u*u*(3-2*u);
 q.x=lerp(from.x,to.x,v);q.y=lerp(from.y,to.y,v);q.rfHeading=Math.atan2(to.y-from.y,to.x-from.x);q.evadeT=0;q._rd21Scale=1;
 }
 if(F.t>=1.1){if(F.phase==='scatter'){F.phase='return';F.t=0;rr26Log('north-south-return');}else{for(const q of live){q.rfHeading=Math.PI/2;q._rr26Flight=null;q.rg4.cd=Math.max(2,q.rg4.cd);}D.fleet=null;D.next=G.age+11;}}
};
rebelSquadTick=function(b,dt){const r=RR26.base.tick.apply(this,arguments),G=b._rebels?.gang1004;if(!G||b.dead)return r;rr26Warm();const S=rr26State(G);
 for(const q of b._rebels.ships){const on=q._rd21Cloak||q.frCloak>0||q._ra7CloakDemo;q._rr26Fade=clamp((q._rr26Fade||0)+(on?1:-1)*dt/1.0,0,1);}
 if(run.stage===6&&!b._rebels.frStageX&&!G.rescueDone&&G.age>18&&!G.scene)rg4RescueStart(b,G);
 if(S.radio){S.radio.t+=dt;if(S.radio.t>S.radio.text.length/34+1.8)S.radio=null;}
 if(!G.scene&&S.queue.length&&!S.radio){const [who,text]=S.queue.shift();S.radio={who,text,t:0};rr26Log('dialogue',{who,text});}
 return r;};
rebelSquadDraw=function(b){const r=RR26.base.draw.apply(this,arguments),G=b._rebels?.gang1004;if(!G)return r;const S=rr26State(G),W=S.wall;
 if(W)rr26DrawWall(W);
 for(const o of S.returns)if(XART.rdy('florb_'+Math.floor(o.t*16)%8)){const im=XART.get('florb_'+Math.floor(o.t*16)%8);ctx.drawImage(im,o.x-15,o.y-15,30,30);}return r;};
globalThis.BOF_REBEL_REVISION_1026=RR26;

drawWorld=function(dt){const r=RR26.base.world.apply(this,arguments),G=rg4State(),C=G?.rr26?.radio;if(C&&!G.scene)h3Radio(C.who.toUpperCase(),C.text,Math.floor(C.t*34),VH*.76);return r;};

const rr26Ship=fr27RebelDrawShip;
fr27RebelDrawShip=function(q){const r=rr26Ship.apply(this,arguments),A=q.rg4?.act;if(!q.dead&&A?.kind==='rr26cannon'&&A.phase==='charge'){const key='florb_'+Math.floor(A.t*16)%8;if(XART.rdy(key)){const d=18+28*clamp(A.t/A.warm,0,1),im=xartPalette(key,RG4_COLORS[q.key]);ctx.drawImage(im,q.x-d/2,q.y+32-d/2,d,d);}}return r;};

// Register the 1015 companion without rewriting the shared generated catalogue.
PXG_SHEETS.rr26_wall={glow:'assets/game/levels/stage_06/boss/rebel_revision_1026/wall_glow.png',size:[384,160],n:1,st:[6]};
XART._src.pxg_rr26_wall_glow=PXG_SHEETS.rr26_wall.glow;XART.rdy('pxg_rr26_wall_glow');
const rr26Begin=beginStage;
beginStage=function(){Snd.loopOff('rr26WallHum');return rr26Begin.apply(this,arguments);};

// Missile tells belong on their victim, never in a directional FOV lane.
const rr26MissileFov=rd21Fov;
rd21Fov=function(owner){
 if(owner?.kind==='rockets'||boss?._rebels?.ships.some(q=>q._rd21Volley===owner))return;
 return rr26MissileFov.apply(this,arguments);
};
const rr26MissileWarning=rg4Warning;
rg4Warning=function(q,A){
 if(A?.kind==='rockets'){if(A.phase==='charge')ra4LockWarning(A,q.key);return;}
 return rr26MissileWarning.apply(this,arguments);
};
const rr26MissileTick=rebelSquadTick;
rebelSquadTick=function(b,dt){
 const r=rr26MissileTick.apply(this,arguments),G=b._rebels?.gang1004;
 if(!G||b.dead)return r;
 const locks=b._rebels.ships.filter(rd21Live).flatMap(q=>[q._rd21Volley,q.rg4?.act?.kind==='rockets'&&q.rg4.act])
  .filter(A=>A&&A.locked&&A.target?.ref&&!A.target.ref.dead&&(!A.phase||A.phase==='charge'));
 const S=rr26State(G);
 if(!G.scene&&locks.length){S.lockBeep=(S.lockBeep||0)-dt;if(S.lockBeep<=0){
  const progress=Math.max(...locks.map(A=>clamp(A.t/A.warm,0,1)));
  S.lockBeep=lerp(.32,.10,progress);Audio.SFX.retinaLockBeep?.();rr26Log('missile-lock-beep');
 }}else S.lockBeep=0;
 return r;
};

// Kaia: Falva's authored roller frames, cyan-green palette, finite gatling bursts.
for(let i=0;i<4;i++)XART.rdy('nfrb_'+i);
const rr26KaiaAttack=rg4Attack;
rg4Attack=function(q,R,G,forced){
 const result=rr26KaiaAttack.apply(this,arguments),A=q.rg4?.act;
 if(q.key==='kaia'&&A&&['windspread','rockets','roller'].includes(A.kind)){
  A.kind='rr26roller';A.warm=1.35;A.shot=0;A.cd=0;return A;
 }return result;
};
const rr26KaiaHeavy=rbal19Heavy;
rbal19Heavy=function(q){return q.rg4?.act?.kind==='rr26roller'&&q.rg4.act.phase!=='recover'||rr26KaiaHeavy(q);};
const rr26KaiaAct=rg4AttackTick;
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(A?.kind!=='rr26roller')return rr26KaiaAct.apply(this,arguments);
 if(!rd21Live(q)){q.rg4.act=null;return;}
 A.t+=Math.min(.05,dt);
 if(A.phase==='charge'){combatWarningTick(A,'kaia-roller',Math.min(A.t,A.warm),A.warm);
  if(A.t<A.warm)return;A.phase='fire';A.t=0;A.cd=0;A.launch=rr26Socket(q,0);A.launchAngle=A.a;
 }
 if(A.phase==='fire'){A.cd-=dt;if(A.cd<=0){
  const a=A.launchAngle,socket=A.launch,v=[175,195,210,225][rd21Rank()];
  G.ord.push({kind:'roller',_rr26KaiaRoller:true,owner:q,x:socket.x,y:socket.y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,r:16,hp:3,max:3,t:0,life:4,bounces:0,split:true,flash:0});
  q._rr26Kick=.12;wm26Emit?.(q,socket.x,socket.y,a,'orb','#39e6c5',{size:32,life:.16,follow:()=>rr26Socket(q,0)});
  Audio.SFX.falvaRelease?.();rr26Log('kaia-roller',{shot:A.shot});A.shot++;A.cd=.20;
  if(A.shot>=10){A.phase='recover';A.t=0;}
 }}else if(A.phase==='recover'&&A.t>1.4)rd21Finish(q,G,5);
};
const rr26KaiaWarning=rg4Warning;
rg4Warning=function(q,A){if(A?.kind==='rr26roller'){if(A.phase==='charge')rd21Fov(A,q.x,q.y+43,A.a,90,A.t/A.warm);return;}return rr26KaiaWarning.apply(this,arguments);};
const rr26KaiaDraw=rg4OrdnanceDraw;
rg4OrdnanceDraw=function(o,G){if(!o._rr26KaiaRoller)return rr26KaiaDraw.apply(this,arguments);
 rr35RollerDraw(o.x,o.y,48,o.t,o.flash,.7);
};
// Retire Kaia's old attached cannon plates, without changing her hull or modules.
const rr26KaiaShip=fr27RebelDrawShip,rr26KaiaReel=ra4Reel;
let rr26DrawingKaia=false;
ra4Reel=function(name){if(rr26DrawingKaia&&name==='launcher')return;return rr26KaiaReel.apply(this,arguments);};
fr27RebelDrawShip=function(q){const previous=rr26DrawingKaia;rr26DrawingKaia=q.key==='kaia';try{return rr26KaiaShip.apply(this,arguments);}finally{rr26DrawingKaia=previous;}};
const rr26KaiaRound=rg4Round;
rg4Round=function(q){if(q.key==='kaia')return {dead:true,x:q.x,y:q.y+43};return rr26KaiaRound.apply(this,arguments);};

// Rook's locked chaingun and Voss's charged fly-through keep native combat owners.
const rr26RolesAttack=rg4Attack;
rg4Attack=function(q,R,G,forced){const before=q.rg4?.act,result=rr26RolesAttack.apply(this,arguments),A=q.rg4?.act;
 if(!A||A===before)return result;
 if(q.key==='rook')Object.assign(A,{kind:'rr26chain',phase:'charge',t:0,warm:1.65,ox:q.x,oy:q.y,shot:0,cd:0,beep:0,locked:true});
 if(q.key==='voss'){
  if(A.kind==='depthram'){A.kind='turbo';A._rd21=false;A.cycle=0;}
  else if(['rr26cannon','fusion','ram'].includes(A.kind))Object.assign(A,{kind:'rr26dash',phase:'charge',t:0,warm:1.65,ox:q.x,oy:q.y,hit:new Set()});
 }return A;
};
const rr26RolesHeavy=rbal19Heavy;
rbal19Heavy=function(q){return !q.dead&&['rr26chain','rr26dash'].includes(q.rg4?.act?.kind)&&q.rg4.act.phase!=='recover'||rr26RolesHeavy(q);};
const rr26RolesAct=rg4AttackTick;
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(!['rr26chain','rr26dash'].includes(A?.kind))return rr26RolesAct.apply(this,arguments);
 if(!rd21Live(q)){q.rg4.act=null;return;}dt=Math.min(.05,dt);A.t+=dt;const chain=A.kind==='rr26chain';
 if(A.phase==='charge'){
  q.x=A.ox;q.y=A.oy;q._rd21Scale=1;
  if(A.t<A.warm*.72){const p=A.target.ref;A.tx=p.x;A.ty=p.y;A.a=Math.atan2(p.y-q.y-32,p.x-q.x);}
  q.rfHeading=A.a;combatWarningTick(A,'rr26-role-'+q.rg4.n,Math.min(A.t,A.warm),A.warm);
  if(chain){A.beep-=dt;if(A.beep<=0){A.beep=lerp(.34,.085,clamp(A.t/A.warm,0,1));Audio.SFX.retinaLockBeep?.();}}
  if(A.t<A.warm)return;
  const p=A.target.ref;A.caught=!p.dead&&Math.hypot(p.x-A.tx,p.y-A.ty)<30;
  A.phase='fire';A.t=0;A.cd=0;A.travel=0;rr26Log(chain?'rook-chain-release':'voss-dash-release',{caught:A.caught});
  if(!chain)Audio.SFX.chargeDash?.();
 }
 if(A.phase==='fire'){
  if(chain){q.x=A.ox;q.y=A.oy;A.cd-=dt;if(A.cd<=0){A.cd+=.09;
   const socket=rr26Socket(q,A.shot%2?-1:1),x=socket.x,y=socket.y;
   const z=eShootT(x,y,A.a,4.8,'s6tracer',{_noArsenal:true,silent:true});
   z._ra4Slug=true;z._rr26Rook=true;q._rr26Kick=.09;z._rr26Owner=q;z._rr26Track=A.caught?A.target.ref:null;z._weaponProof=true;
   wm26Emit?.(q,x,y,A.a,'chaingun',null,{size:28,life:.11});Audio.SFX.enemyMachineGunHeavy?.();A.shot++;
   if(A.shot>=[16,22,26,30][rd21Rank()]){A.phase='recover';A.t=0;}
  }}else{
   A.travel+=Math.min(780,220+A.t*2100)*dt;q.x=A.ox+Math.cos(A.a)*A.travel;q.y=A.oy+Math.sin(A.a)*A.travel;q.rfHeading=A.a;
   ra4TurboTrace(q,A);ra4RamHit(q,A);
   if(q.x<camLeftX()-100||q.x>camRightX()+100||q.y>VH+100||q.y<PLAY.y-100){A.phase='offscreen';A.t=0;}
  }
 }else if(A.phase==='offscreen'&&A.t>.35){A.phase='north';A.t=0;q.x=clamp(A.ox,camLeftX()+60,camRightX()-60);q.y=PLAY.y-120;q.rfHeading=Math.PI/2;rr26Log('voss-north-return');
 }else if(A.phase==='north'){const u=clamp(A.t/1.0,0,1);q.y=lerp(PLAY.y-120,A.oy,1-Math.pow(1-u,2));q.rfHeading=Math.PI/2;if(A.t>=1){A.phase='recover';A.t=0;}
 }else if(A.phase==='recover'&&A.t>1.1)rd21Finish(q,G,chain?5:6);
};
const rr26RolesWarning=rg4Warning;
rg4Warning=function(q,A){if(['rr26chain','rr26dash'].includes(A?.kind)){
 if(A.phase==='charge'){rd21Fov(A,q.x,q.y+32,A.a,A.kind==='rr26chain'?48:74,A.t/A.warm);
  if(A.kind==='rr26chain'){const marker={...A,target:{ref:{x:A.tx,y:A.ty}}};ra4LockWarning(marker,'rook');}}
 return;}return rr26RolesWarning.apply(this,arguments);
};
const rr26RolesUpdate=updatePlay;
updatePlay=function(dt){for(const z of eBullets){if(!z._rr26Rook||z.dead)continue;
 if(z._rr26Owner?.dead){z.dead=true;continue;}const p=z._rr26Track;
 if(p&&!p.dead&&(z.t||0)<1.0){const a=Math.atan2(z.vy,z.vx),goal=Math.atan2(p.y-z.y,p.x-z.x),d=((goal-a+Math.PI*3)%TAU)-Math.PI,n=a+clamp(d,-dt*.8,dt*.8);z.vx=Math.cos(n)*4.8;z.vy=Math.sin(n)*4.8;z.ang=n;}
 }return rr26RolesUpdate.apply(this,arguments);};
const rr26RolesShip=fr27RebelDrawShip;
fr27RebelDrawShip=function(q){const r=rr26RolesShip.apply(this,arguments),A=q.rg4?.act;
 if(!q.dead&&A?.kind==='rr26dash'&&A.phase==='charge'){const key='florb_'+Math.floor(A.t*20)%8;if(XART.rdy(key)){const d=20+42*clamp(A.t/A.warm,0,1);ctx.drawImage(xartPalette(key,RG4_COLORS.voss),q.x-d/2,q.y-d/2,d,d);}}
 return r;};

// Authored effects only: casting and construction use native frames, not CSS fades.
function rr26Socket(q,side=0){const a=q.rfHeading??Math.PI/2,forward=side?31:42,lateral=side*20;
 return {x:q.x+Math.cos(a)*forward-Math.sin(a)*lateral,y:q.y+Math.sin(a)*forward+Math.cos(a)*lateral,angle:a};}
function rr26AnimatedPose(q){
 const a=q.rfHeading??Math.PI/2,A=q.rg4?.act;if(q._rr26Fade>.01)return null;
 if(q.evadeT>0&&Math.abs(a-Math.PI/2)<.2){const d=AM13_ART[q.key],m=d.roll;if(m&&XART.rdy(m.key)){const f=Math.floor((1-q.evadeT/.38)*m.frames+m.frames)%m.frames;return{d,m,f,key:m.key,im:XART.get(m.key),sx:f*m.cell};}}
 if(Math.abs(a-Math.PI/2)>.39)return null;
 const kind=A&&['charge','fire'].includes(A.phase)?'attack':'idle',speed=A?.phase==='charge'?2+8*clamp(A.t/A.warm,0,1):12;
 const p=af21Pose(q.key,kind,(q.t||0)*speed/8);if(p){p.rotation=0;q._rr26Anim={kind,frame:p.f};}return p;
}
function rr26Effect(key,x,y,d,alpha=1,color){if(!XART.rdy(key))return;ctx.save();ctx.globalAlpha*=alpha;const im=color?xartPalette(key,color):XART.get(key);ctx.drawImage(im,x-d/2,y-d/2,d,d);ctx.restore();}
function rr26DrawWall(W){const r=rr26WallRect(),cast=W.cast??0,build=W.build??.3,fade=W.fade??.3;
 const u=clamp((W.t-cast)/build,0,1),end=clamp((W.dur-W.t)/fade,0,1),a=Math.floor(Math.min(u,end)*24)/24;
 if(W.t<cast){const q=W.caster,origin=q&&!q.dead?{x:q.x,y:q.y-24}:W.origin;if(!origin)return;
  const travel=clamp((W.t-.55)/(cast-.55),0,1),v=travel*travel*(3-2*travel),x=lerp(origin.x,r.x+r.w/2,v),y=lerp(origin.y,r.y+r.h/2,v);
  rr26Effect('florb_'+Math.floor(W.t*20)%8,x,y,18+22*Math.min(W.t/.55,1),1,'#45ddff');
  rr26Effect('florb_'+Math.floor(W.t*20+4)%8,origin.x,origin.y,42,Math.max(0,1-travel),'#45ddff');return;
 }
 if(!XART.rdy('rr26_wall'))return;
 ctx.save();ctx.beginPath();const width=r.w*u;ctx.rect(r.x+(r.w-width)/2,r.y,width,r.h);ctx.clip();
 const im=xartPalette('rr26_wall','#45ddff')||XART.get('rr26_wall');
 for(let i=0;i<3;i++){const step=Math.floor(W.t*16+i*2)%10,light=PXG_STEPS[step<6?step:10-step];
 pxgWindow({lights:W.pulse>0?1:light,core:0,alpha:a},()=>{ctx.save();ctx.globalAlpha*=a*.78;ctx.drawImage(im,14,32,356,96,r.x+i*r.w/3,r.y,r.w/3,r.h);ctx.restore();},null,[]);}
 ctx.restore();
 if(u<1)for(const sign of [-1,1])rr26Effect('florb_'+Math.floor(W.t*24)%8,r.x+r.w/2+sign*width/2,r.y+r.h/2,34,a,'#45ddff');
}
const rr26PolishTick=rebelSquadTick;
rebelSquadTick=function(b,dt){for(const q of b._rebels?.ships||[])q._rr26Kick=Math.max(0,(q._rr26Kick||0)-dt);return rr26PolishTick.apply(this,arguments);};
const rr26PolishShip=fr27RebelDrawShip;
fr27RebelDrawShip=function(q){const A=q.rg4?.act,dy=q._rr26Kick?Math.sin(q._rr26Kick/.12*Math.PI)*2.5:0;
 ctx.save();ctx.translate(0,-dy);let r;try{r=rr26PolishShip.apply(this,arguments);}finally{ctx.restore();}
 if(!q.dead&&A?.kind==='rr26roller'&&['charge','fire'].includes(A.phase)){const p=rr26Socket(q),f=Math.floor((q.t||0)*20)%4;
  const k=A.phase==='charge'?clamp(A.t/A.warm,0,1):clamp(A.cd/.20,0,1);rr35RollerDraw(p.x,p.y,16+32*k,q.t||A.t,0,.2+.75*k);}
 return r;
};
for(const id of REBEL_KEYS)for(const kind of ['idle','attack']){const B=AF21_ART.models[id]?.banks[kind];if(B)XART.rdy(B.key);}

// Kaia's source-referenced PixelLab rotation and own-pixel 1015 ring light.
XART._src.rr35_roller='assets/game/levels/stage_06/boss/kaia_roller_1028/spin.png';
PXG_SHEETS.rr35_roller={glow:'assets/game/levels/stage_06/boss/kaia_roller_1028/spin_glow.png',size:[256,256],n:1,st:[6]};
XART._src.pxg_rr35_roller_glow=PXG_SHEETS.rr35_roller.glow;
for(const key of ['rr35_roller','pxg_rr35_roller_glow'])XART.rdy(key);
function rr35RollerDraw(x,y,d,t,flash,energy){
 if(!XART.rdy('rr35_roller'))return;
 const f=Math.floor(t*24)%16,im=flash>0?xartTint('rr35_roller','#ffffff',1):xartPalette('rr35_roller','#39e6c5');
 const pulse=PXG_STEPS[Math.floor(t*24)%10<6?Math.floor(t*24)%10:10-Math.floor(t*24)%10];
 pxgWindow({lights:flash>0?0:energy*(.45+.55*pulse),core:0,alpha:1},()=>ctx.drawImage(im,(f%4)*64,Math.floor(f/4)*64,64,64,x-d/2,y-d/2,d,d),null,[]);
}
const rr35Impact=pw5Impact;
pw5Impact=function(p){if(p?._rr26KaiaRoller)return null;return rr35Impact.apply(this,arguments);};
