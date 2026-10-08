'use strict';
/* October 7: physical Rookhook, layered Ghostknife spiral, committed air battles.
   Generated hardware/energy is kept in its native-alpha source sheet. */
const RA7={sheet:'ra7_air',draws:{},events:[],deaths:[],serial:0};
const RA7_BASE={kind:ra4AttackKind,attack:rg4Attack,tick:rg4AttackTick,gun:ra4Gun,
 warning:rg4Warning,ship:fr27RebelDrawShip,rebelTick:rebelSquadTick,rebelDraw:rebelSquadDraw,
 damage:rebelSquadDamage,clear:rg4Clear,begin:beginStage,ace:whvAceTick,aceDraw:whvDrawAce,
 aceDeath:whvAceDeathTick,targets:retinaBossTargets,init:rg4Init,playerHit:playerHit,demoTick:rs1004DemoTick,demoDraw:rs1004DemoDraw};
XART._src[RA7.sheet]='assets/game/levels/stage_06/boss/rebel_air_1007/rebel_air.png';
function ra7Log(event,data={}){RA7.events.push({event,...data});if(RA7.events.length>180)RA7.events.shift();}
function ra7Cell(n,x,y,w,h=w,angle=0,alpha=1){if(!XART.rdy(RA7.sheet))return false;
 const im=XART.get(RA7.sheet),cw=im.width/4,ch=im.height/3;ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 ctx.drawImage(im,(n%4)*cw,Math.floor(n/4)*ch,cw,ch,-w/2,-h/2,w,h);ctx.restore();RA7.draws[n]=(RA7.draws[n]||0)+1;return true;}
function ra7LiveTarget(t){return !!(t?.ref&&!t.ref.dead&&!t.ref.out&&(t.seat||t.ref.hp>0&&t.ref.phase!=='leave'));}
function ra7Escape(t){const p=t?.ref;return !ra7LiveTarget(t)||!!(p.roll||p.somer||p._chgDash||p._phased||p._voidDeath);}
function ra7Segment(x,y,ax,ay,bx,by){const dx=bx-ax,dy=by-ay,u=clamp(((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy||1),0,1);return Math.hypot(x-ax-dx*u,y-ay-dy*u);}
function ra7Release(q,A,reason){if(A.target?.ref?._ra7Caught===A)delete A.target.ref._ra7Caught;
 if(A.target?.ref?._ra7Thrown===A)delete A.target.ref._ra7Thrown;
 if(A.phase!=='recover'){A.phase='recover';A.t=0;A.reason=reason;q.rg4.gunCd=Math.max(q.rg4.gunCd,1.2);ra7Log('hookRelease',{reason,pilot:q.key});}}
function ra7HookStart(q,R,G){const M=q.rg4;
 if(R.ships.some(s=>s!==q&&!s.dead&&['turbo','ram','fusion','helix','rookhook'].includes(s.rg4?.act?.kind))){M.cd=.6;return false;}
 const seats=ra4Targets().filter(t=>t.seat),target=seats[(M.serial||0)%Math.max(1,seats.length)]||ra4Target(q,M.serial||0);
 if(!ra7LiveTarget(target))return false;
 M.armed=null;M.n++;M.badge=1.6;M.act={kind:'rookhook',phase:'charge',t:0,warm:diffKey==='easy'?1.65:diffKey==='normal'?1.4:1.2,
  target,a:Math.atan2(target.ref.y-q.y-25,target.ref.x-q.x),tx:target.ref.x,ty:target.ref.y,hx:q.x,hy:q.y+25,
  hp:diffKey==='easy'?3:4,max:diffKey==='easy'?3:4,flash:0,range:Math.min(VH+30,660),distance:0,serial:++RA7.serial};
 q.evadeT=0;q.frSomersault=false;G.releaseAt=G.age+4.4;combatWarningTick(M.act,'rookhook-'+M.act.serial,0,M.act.warm);
 rf28Callout(R,'ROOKHOOK — DODGE OR CUT THE HOOK',q.x,q.y+62,'#ffbd50',1.7,8);av3Sound('target_acquire',.7,.25);ra7Log('hookStart',{seat:target.seat||0});return true;}
ra4AttackKind=function(q,G){if(q.key==='rook'){const n=q.rg4.serial++;return ['rookhook','slug','ram'][n%3];}return RA7_BASE.kind.apply(this,arguments);};
rg4Attack=function(q,R,G,forced){if(q.key==='rook'&&(forced==='rookhook'||!forced&&q.rg4.armed==='rookhook'))return ra7HookStart(q,R,G);
 if(G.arsenal1004c&&R.ships.some(s=>s!==q&&!s.dead&&s.rg4?.act?.kind==='rookhook'&&s.rg4.act.phase!=='recover')){q.rg4.cd=.6;return;}
 if(q.key==='nyx'&&(forced==='cloak'||!forced&&q.rg4.armed==='cloak')){const M=q.rg4,target=ra4Target(q,M.serial),ref=target.ref,warm=1.15*(diffKey==='easy'?1.3:1);
  M.armed=null;M.n++;M.badge=1.35;M.act={kind:'cloak',phase:'charge',t:0,warm,target,tx:ref.x,ty:ref.y,a:Math.atan2(ref.y-q.y,ref.x-q.x),shot:0,cd:0,cycle:0};
  q.frCloak=0;q.evadeT=0;q.frSomersault=false;G.releaseAt=G.age+(diffKey==='easy'?1.8:1.15);av3Sound('teleport_out',.7);ra4Log(G,'specialStart',{pilot:q.key,kind:'cloak'});return;}
 return RA7_BASE.attack.apply(this,arguments);};
function ra7HookHit(q,A,dmg){if(A.phase==='recover'||!(dmg>0))return false;A.hp=Math.max(0,A.hp-dmg);A.flash=.12;
 if(!A.hp){explode(A.hx,A.hy,26,'blue');av3Sound('impact_metal',.8);ra7Release(q,A,'cut');}return true;}
function ra7HookCuts(q,A,dt){if(!['cast','reel','sling'].includes(A.phase))return;A.hitCd=Math.max(0,(A.hitCd||0)-dt);
 for(const p of pBullets){if(p.dead)continue;const B=p.kind==='beam'?playerBeamRange(p):null;
  const hit=B?A.hy+17>=B.top&&A.hy-17<=B.bot&&Math.abs(A.hx-B.x)<B.half+17:ra7Segment(A.hx,A.hy,p.px??p.x,p.py??p.y,p.x,p.y)<17+Math.max(p.w||4,p.h||4)*.35;
  if(!hit||B&&A.hitCd>0)continue;ra7HookHit(q,A,p.dmg||1);if(B)A.hitCd=.12;else if(!p.pierce)p.dead=true;if(A.phase==='recover')break;
 }}
function ra7HookTick(q,R,G,dt){const A=q.rg4.act;if(!A||A.kind!=='rookhook')return;
 A.t+=dt;A.flash=Math.max(0,A.flash-dt);q.evadeT=0;q.rfHeading=null;
 if(q.dead||G.scene||boss?._rebels!==R){ra7Release(q,A,'owner');q.rg4.act=null;return;}
 if(A.phase==='charge'){
  if(!ra7LiveTarget(A.target)){ra7Release(q,A,'target');return;}
  if(A.t<A.warm*.46){A.tx=A.target.ref.x;A.ty=A.target.ref.y;A.a=Math.atan2(A.ty-q.y-25,A.tx-q.x);}
  A.hx=q.x;A.hy=q.y+25;combatWarningTick(A,'rookhook-'+A.serial,Math.min(A.t,A.warm),A.warm);
  if(A.t>=A.warm){A.phase='cast';A.t=0;A.ox=q.x;A.oy=q.y+25;A.distance=0;av3Sound('launch',.85);ra7Log('hookCast',{a:A.a});}
 }else if(A.phase==='cast'){
  const px=A.hx,py=A.hy;A.distance+=dt*(diffKey==='easy'?410:500);A.hx=A.ox+Math.cos(A.a)*A.distance;A.hy=A.oy+Math.sin(A.a)*A.distance;
  const p=A.target.ref;
  if(!ra7Escape(A.target)&&!p._ra7Caught&&ra7Segment(p.x,p.y,px,py,A.hx,A.hy)<20){
   A.phase='reel';A.t=0;A.px=p.x;A.py=p.y;p._ra7Caught=A;A.hx=p.x;A.hy=p.y;
   A.throwSide=p.x<camLeftX()+viewW()/2?-1:1;A.reelX=clamp(q.x+A.throwSide*78,camLeftX()+50,camRightX()-50);A.reelY=clamp(q.y+110,PLAY.y+120,VH-105);
   ra7Log('hookCaught',{seat:A.target.seat||0});av3Sound('impact_metal',.6);
  }else if(A.distance>=A.range||A.hx<camLeftX()-35||A.hx>camRightX()+35||A.hy>VH+35||A.hy<PLAY.y-35)ra7Release(q,A,'miss');
 }else if(A.phase==='reel'){
  if(ra7Escape(A.target)){ra7Release(q,A,'evade');return;}const p=A.target.ref,u=clamp(A.t/.70,0,1),k=u*u*(3-2*u);
  p.x=lerp(A.px,A.reelX,k);p.y=lerp(A.py,A.reelY,k);A.hx=p.x;A.hy=p.y;
  if(A.t>=.70){A.phase='sling';A.t=0;A.radius=Math.max(55,Math.min(110,Math.hypot(p.x-q.x,p.y-q.y)));A.startAngle=Math.atan2(p.y-q.y,p.x-q.x);}
 }else if(A.phase==='sling'){
  if(ra7Escape(A.target)){ra7Release(q,A,'evade');return;}const p=A.target.ref,u=clamp(A.t/.42,0,1),a=A.startAngle-A.throwSide*u*Math.PI*.72;
  p.x=clamp(q.x+Math.cos(a)*A.radius,camLeftX()+24,camRightX()-24);p.y=clamp(q.y+Math.sin(a)*A.radius,PLAY.y+75,VH-55);A.hx=p.x;A.hy=p.y;
  if(A.t>=.42){A.phase='throw';A.t=0;A.px=p.x;A.py=p.y;A.edgeX=A.throwSide<0?camLeftX()+25:camRightX()-25;A.edgeY=clamp(p.y+95,PLAY.y+140,VH-65);delete p._ra7Caught;p._ra7Thrown=A;ra7Log('hookThrow',{side:A.throwSide});av3Sound('launch',.75);}
 }else if(A.phase==='throw'){
  if(ra7Escape(A.target)){ra7Release(q,A,'evade');return;}const p=A.target.ref,u=clamp(A.t/.45,0,1),k=1-(1-u)*(1-u);
  p.x=lerp(A.px,A.edgeX,k);p.y=lerp(A.py,A.edgeY,k);A.hx=lerp(A.px,q.x,u);A.hy=lerp(A.py,q.y+25,u);
  if(u>=1){if(A.target.seat)withSeat(A.target.seat,()=>playerHit('Rookhook edge impact'));
   else if(!p.hurtT){p.hp=Math.max(0,p.hp-1);p.hurtT=1;if(!p.hp){p.phase='leave';p.t=0;}}
   explode(p.x,p.y,32,'blue');ra7Release(q,A,'edge');}
 }else if(A.phase==='recover'){
  A.hx=lerp(A.hx,q.x,Math.min(1,dt*12));A.hy=lerp(A.hy,q.y+25,Math.min(1,dt*12));
  if(A.t>=1.05){q.rg4.act=null;q.rg4.cd=diffKey==='easy'?7:5.8;G.releaseAt=Math.max(G.releaseAt,G.age+.6);}
 }
 ra7HookCuts(q,A,dt);
}
// Forced motion must not deliver an unavoidable second hit from another hull.
// The edge impact still passes through ordinary shield/invulnerability handling.
playerHit=function(source){if((player._ra7Caught||player._ra7Thrown)&&source!=='Rookhook edge impact')return;return RA7_BASE.playerHit.apply(this,arguments);};
function ra7GhostTick(q,R,G,dt){const A=q.rg4.act;A.t+=dt;
 if(A.phase==='charge'){q.frCloak=A.t<A.warm*.7?0:10;if(A.t<A.warm)return;A.phase='fire';A.t=0;A._ra7Pulse=null;A._ra7Gap=0;ra4Log(G,'specialRelease',{pilot:q.key,kind:'cloak'});}
 if(A.phase!=='fire')return;
 q.frCloak=10;A._ra7Gap=Math.max(0,(A._ra7Gap||0)-dt);
 if(!A._ra7Pulse&&A._ra7Gap<=0){const target=ra7LiveTarget(A.target)?A.target:ra4Target(q,A.shot++),p=target.ref;
  A._ra7Pulse={t:0,warm:diffKey==='easy'?1.05:diffKey==='normal'?.85:.72,x:q.x,y:q.y+32,a:Math.atan2(p.y-q.y-32,p.x-q.x)};
 }
 const P=A._ra7Pulse;if(P){P.t+=dt;combatWarningTick(P,'ghostknife',Math.min(P.t,P.warm),P.warm);
  if(P.t>=P.warm){for(const off of [-.14,0,.14])rg4Round({x:P.x,y:P.y-32},P.a+off,diffKey==='easy'?3.4:4.1,'s6tracer',{_ra4Ghost:true,_ra7Ghost:true,owner:q});
   av3Sound('laser_release',.55,.12);ra7Log('ghostknifeVolley');A._ra7Pulse=null;A._ra7Gap=.38;}
 }else q.x=clamp(q.x+Math.sin(G.age*2.4+q.i)*dt*125,camLeftX()+52,camRightX()-52);
 if(A.t>=(G.gang?6.5:5.2)){A.phase='recover';A.t=0;A._ra7Pulse=null;q.frCloak=0;q._ra7Reveal=.55;av3Sound('teleport_in',.7);}
}
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(A?.kind==='rookhook')return ra7HookTick(q,R,G,Math.min(.05,dt));
 if(q.key==='nyx'&&A?.kind==='cloak'&&A.phase!=='recover')return ra7GhostTick(q,R,G,Math.min(.05,dt));return RA7_BASE.tick.apply(this,arguments);};
ra4Gun=function(q,G,dt){const R=boss?._rebels;if(R?.ships.some(s=>s.rg4?.act?.kind==='rookhook'&&!s.dead&&s.rg4.act.phase!=='recover'))return;
 return RA7_BASE.gun.apply(this,arguments);};
rg4Warning=function(q,A){if(A.kind==='cloak'&&A._ra7Pulse){const P=A._ra7Pulse;for(const off of [-.14,0,.14])combatWarningDraw(P,{x:P.x,y:P.y,ex:P.x+Math.cos(P.a+off)*VH,ey:P.y+Math.sin(P.a+off)*VH,width:13,progress:P.t/P.warm,fieldOnly:off!==0,laneShape:'line'});return;}
 if(A.kind!=='rookhook')return RA7_BASE.warning.apply(this,arguments);if(A.phase!=='charge')return;
 combatWarningDraw(A,{x:q.x,y:q.y+25,ex:q.x+Math.cos(A.a)*A.range,ey:q.y+25+Math.sin(A.a)*A.range,width:42,progress:A.t/A.warm,laneShape:'line',alertX:q.x,alertY:q.y+35});};
function ra7HookDraw(q){const A=q.rg4?.act;if(A?.kind!=='rookhook')return;
 const angle=A.phase==='charge'?A.a:Math.atan2(A.hy-q.y-25,A.hx-q.x),sx=q.x,sy=q.y+25;
 if(A.phase!=='charge'){
  const dx=A.hx-sx,dy=A.hy-sy,d=Math.hypot(dx,dy),n=Math.min(52,Math.ceil(d/12));
  for(let i=0;i<n;i++){const u=i/Math.max(1,n),sag=A.phase==='recover'?Math.sin(u*Math.PI)*16:0;ra7Cell(2,sx+dx*u,sy+dy*u+sag,9,16,angle-Math.PI/2);}
  ra7Cell(['reel','sling'].includes(A.phase)?3:1,A.hx,A.hy,43,43,angle-Math.PI/2);
 }
 ra7Cell(0,sx,sy,36,40,angle-Math.PI/2);RA7.draws.hook=(RA7.draws.hook||0)+1;
}
function ra7NyxSpiral(q,front=false){const A=q.rg4?.act,active=q.frCloak>0||q._ra7CloakDemo||q._ra7Reveal>0||A?.kind==='cloak'&&A.phase==='charge';if(!active)return;
 const t=(q._ra7CloakDemo?.t??q.t??0)*1.45,f=t*8,i=Math.floor(f)%8,blend=f-Math.floor(f),w=104,h=142,fade=q._ra7Reveal>0?clamp(q._ra7Reveal/.55,0,1):1;
 ctx.save();if(front){ctx.beginPath();for(const [top,high]of [[-.38,.14],[-.03,.16],[.29,.16]])ctx.rect(q.x-w/2,q.y+h*top,w,h*high);ctx.clip();}
 ra7Cell(4+i,q.x,q.y,w,h,0,(front?.94:.65)*(1-blend)*fade);ra7Cell(4+(i+1)%8,q.x,q.y,w,h,0,(front?.94:.65)*blend*fade);ctx.restore();
 RA7.draws[front?'nyxFront':'nyxBack']=(RA7.draws[front?'nyxFront':'nyxBack']||0)+1;
}
function ra7Nyx(q){if(q.dead)return;ra7NyxSpiral(q,false);const f=q.evadeT>0?Math.min(7,Math.floor((1-q.evadeT/.38)*8)):0;
 const roll='rr_roll_'+REBEL_SHIPS[q.i]+'_'+f,k=XART.rdy(roll)?roll:'rr_ship_'+REBEL_SHIPS[q.i];if(XART.rdy(k)){
  const im=XART.get(k),w=SHIP_DRAW_H*1.5,h=w*im.height/im.width;ra4Blit(im,q.x,q.y,w,h,0,q.frCloak>0?.14:1);
  if(q.flash>0)ra4Blit(xartTint(k,'#ffffff',1),q.x,q.y,w,h,0,Math.min(1,q.flash*9));
 }ra7NyxSpiral(q,true);if(q.rg4?.act)rg4Warning(q,q.rg4.act);}
fr27RebelDrawShip=function(q){if(q.key==='nyx')return ra7Nyx(q);const r=RA7_BASE.ship.apply(this,arguments);if(!q.dead)ra7HookDraw(q);return r;};
rs1004DemoTick=function(R,I,dt){const r=RA7_BASE.demoTick.apply(this,arguments);for(const q of R.ships)q._ra7CloakDemo=null;
 const D=I.showcase?.current;if(D?.kind==='cloak'&&D.q?.key==='nyx')D.q._ra7CloakDemo={t:D.t};return r;};
rs1004DemoDraw=function(R){const D=R.h3Intro?.showcase?.current;if(D?.kind!=='cloak'||D.q?.key!=='nyx')return RA7_BASE.demoDraw.apply(this,arguments);
 const kind=D.kind;D.kind='ra7-spiral';try{return RA7_BASE.demoDraw.apply(this,arguments);}finally{D.kind=kind;}};
retinaBossTargets=function(b){const out=RA7_BASE.targets.apply(this,arguments);const R=b?._rebels;if(!R||b.dead||R.gang1004?.scene)return out;
 for(const q of R.ships){const A=q.rg4?.act;if(!q.dead&&A?.kind==='rookhook'&&['cast','reel','sling'].includes(A.phase))out.push(retinaDynamicPiece(b,'rookhook-'+A.serial,'grapple',()=>({x:A.hx,y:A.hy,hp:A.hp,dead:q.dead||A.hp<=0||q.rg4.act!==A||!['cast','reel','sling'].includes(A.phase)}),d=>ra7HookHit(q,A,d),36,36));}return out;};
function ra7DeathStart(q,b){if(q._ra7Death)return q._ra7Death;const D=q._ra7Death={q,b,t:0,dur:DS_DUR,crashT:DS_CRASH,turns:DS_TURN_MIN+(q.i||0)*72,dir:(q.i||0)%2?-1:1,vx:(q.i||0)%2?-18:18,vy:56,fxT:0,anchor:[],crashed:false};
 D.turns=clamp(D.turns,DS_TURN_MIN,DS_TURN_MAX);RA7.deaths.push(D);ra7Log('deathStart',{pilot:q.key||'ace'});return D;}
function ra7DeathTick(D,dt){const q=D.q;D.t+=dt;if(D.t<D.dur){q.x=clamp(q.x+D.vx*dt,camLeftX()+16,camRightX()-16);q.y=clamp(q.y+D.vy*dt,PLAY.y+16,VH-20);D.fxT-=dt;
  if(D.fxT<=0){D.fxT=1/DS_FX_HZ;const n=explosions.length,ox=rnd(-13,13),oy=rnd(-13,13);explode(q.x+ox,q.y+oy,rnd(15,27),'red');if(explosions[n])D.anchor.push({e:explosions[n],ox,oy});if(D.anchor.length>DS_ANCHOR_MAX)D.anchor.shift();}
 }else if(!D.crashed){D.crashed=true;D.anchor=[];fxBurst(q.x,q.y,66,{color:'#7fd4ff',rings:2});for(let i=0;i<7;i++)explode(q.x+rnd(-18,18),q.y+rnd(-15,15),rnd(28,54),'red');Audio.SFX.death?.();shake=Math.max(shake,10);ra7Log('deathCrash',{pilot:q.key||'ace',at:D.t});}
 D.anchor=D.anchor.filter(a=>a.e&&a.e.t<a.e.dur);for(const a of D.anchor){a.e.x=q.x+a.ox;a.e.y=q.y+a.oy;}
}
function ra7DeathDraw(D){if(D.crashed)return;const q=D.q,f=((Math.round(clamp(D.t/D.dur,0,1)*D.turns*D.dir/45)%8)+8)%8,k='rr_roll_'+REBEL_SHIPS[q.i]+'_'+f;
 if(XART.rdy(k)){const im=XART.get(k),w=SHIP_DRAW_H*1.5,h=w*im.height/im.width;ra4Blit(im,q.x,q.y,w,h,0,1);}RA7.draws.death=(RA7.draws.death||0)+1;}
rebelSquadDamage=function(b,dmg){const R=b._rebels,q=R?.ships[R.hit],alive=q&&!q.dead,hook=q?.rg4?.act,ne=explosions.length;const result=RA7_BASE.damage.apply(this,arguments);
 if(alive&&q.dead){explosions.splice(ne);if(hook?.kind==='rookhook')ra7Release(q,hook,'owner');if(q.rg4)q.rg4.act=null;
  // Retire the older 2.8-second duplicate hull; this controller owns one wreck.
  delete q._gpDeath;ra7DeathStart(q,b);
  eBullets=eBullets.filter(p=>p.owner!==q);if(R.gang1004){R.gang1004.ord=R.gang1004.ord.filter(p=>p.owner!==q);R.gang1004.beams=R.gang1004.beams.filter(p=>p.owner!==q);}}
 return result;};
rebelSquadTick=function(b,dt){const hooks=b._rebels.ships.filter(q=>q.rg4?.act?.kind==='rookhook').map(q=>[q,q.rg4.act]);
 const r=RA7_BASE.rebelTick.apply(this,arguments);for(const q of b._rebels.ships){q._ra7Reveal=Math.max(0,(q._ra7Reveal||0)-dt);if(b._rebels.frIntro?.done)q._ra7CloakDemo=null;}
 for(const [q,A]of hooks)if(q.dead||q.rg4.act!==A){ra7Release(q,A,'owner');if(q.rg4.act===A)q.rg4.act=null;}
 for(const D of RA7.deaths)if(D.b===b&&D.t<D.dur+D.crashT)ra7DeathTick(D,Math.min(.05,dt));RA7.deaths=RA7.deaths.filter(D=>D.b===boss&&D.t<D.dur+D.crashT);
 if(GP4.death?.q?._ra7Death&&GP4.death.t>=DS_DUR+DS_CRASH)GP4.death=null;
 if(!b.dead&&!GP4.death&&!GP4.deaths.length&&b._rebels.ships.every(q=>q.dead&&q._ra7Death?.crashed&&q._ra7Death.t>=DS_DUR+DS_CRASH))bossDie();return r;};
rebelSquadDraw=function(b){const r=RA7_BASE.rebelDraw.apply(this,arguments);for(const D of RA7.deaths)if(D.b===b)ra7DeathDraw(D);return r;};
rg4Clear=function(G){for(const q of boss?._rebels?.ships||[]){const A=q.rg4?.act;if(A?.kind==='rookhook')ra7Release(q,A,'clear');}return RA7_BASE.clear.apply(this,arguments);};
beginStage=function(){for(const D of RA7.deaths)if(D.q.rg4?.act?.kind==='rookhook')ra7Release(D.q,D.q.rg4.act,'stage');
 for(const q of boss?._rebels?.ships||[]){const A=q.rg4?.act;if(A?.kind==='rookhook')ra7Release(q,A,'stage');}RA7.deaths=[];return RA7_BASE.begin.apply(this,arguments);};
/* The giant blue jet holds a clear center gap between its wing batteries,
   then gives a damage window. Normal evasions/dashes continue between motifs. */
function ra7AceReady(b,A){return run.stage===6&&!b._gp4Host&&!b.dead&&b._whv.mode==='ace'&&A.st==='fight'&&!A.roll&&!A.somer&&!A.dash&&(!A.desp||A.desp.st==='done')&&!A._pw5Gun;}
function ra7AceStart(b,A){A._ra7Gate={t:0,phase:'position',x:clamp(player.x,camLeftX()+105,camRightX()-105),y:PLAY.y+115,n:0,next:0,warn:diffKey==='easy'?1.5:1.15};A._pw5Gun=null;A.burst=0;A._pw5Missiles=0;A.vx=A.vy=0;ra7Log('aceGateStart');}
function ra7AceTick(b,A,dt){const C=A._ra7Gate;C.t+=dt;A.t+=dt;A.gunCd=A.mslCd=A.dashCd=Math.max(2.5,C.warn+1);A.burst=0;if(A.orb)A.orb.cd=2.5;
 if(C.phase==='position'){A.x+=clamp(C.x-A.x,-dt*245,dt*245);A.y+=clamp(C.y-A.y,-dt*200,dt*200);if(C.t>=.7){C.phase='warn';C.t=0;C.x=A.x;C.y=A.y;combatWarningTick(C,'ace-gate',0,C.warn);}}
 else if(C.phase==='warn'){combatWarningTick(C,'ace-gate',Math.min(C.t,C.warn),C.warn);if(C.t>=C.warn){C.phase='fire';C.t=0;C.next=0;}}
 else if(C.phase==='fire'){
  if(C.t>=C.next&&C.n<(diffKey==='easy'?2:3)){C.next+=.34;C.n++;
   for(const side of [-1,1])for(const spread of [0,.14,.28]){const a=Math.PI/2-side*spread;const p=eShootT(C.x+side*50,C.y+48,a,diffKey==='easy'?3.4:4.3,'s6tracer',{owner:b,w:7,h:19,silent:spread>0});p._ra7Gate=true;}
   wm26Emit?.(b,C.x-50,C.y+48,Math.PI/2,'mg',null,{size:24});wm26Emit?.(b,C.x+50,C.y+48,Math.PI/2,'mg',null,{size:24});av3Sound('laser_release',.65,.1);ra7Log('aceGateVolley',{n:C.n});
  }if(C.t>1.2){C.phase='recover';C.t=0;}}
 else if(C.t>1.1){A._ra7Gate=null;A._ra7Cd=diffKey==='easy'?12:9;A.gunCd=Math.max(A.gunCd,.9);ra7Log('aceGateEnd');}
 b.x=A.x;b.y=A.y;
}
whvAceTick=function(b,dt){const A=b?._whv?.ace;if(!A)return RA7_BASE.ace.apply(this,arguments);A._ra7Cd=(A._ra7Cd??5)-dt;
 if(ra7AceReady(b,A)&&A._ra7Cd<=0&&!A._ra7Gate)ra7AceStart(b,A);
 if(A._ra7Gate){if(!ra7AceReady(b,A)){A._ra7Gate=null;A._ra7Cd=3;}else return ra7AceTick(b,A,Math.min(.05,dt));}
 return RA7_BASE.ace.apply(this,arguments);};
whvDrawAce=function(b){const A=b?._whv?.ace;if(A?.crash&&b.dead)return;const r=RA7_BASE.aceDraw.apply(this,arguments),C=A?._ra7Gate;
 if(C?.phase==='warn')for(const side of [-1,1])for(const spread of [0,.28]){const a=Math.PI/2-side*spread;combatWarningDraw(C,{x:C.x+side*50,y:C.y+48,ex:C.x+side*50+Math.cos(a)*VH,ey:C.y+48+Math.sin(a)*VH,width:19,progress:C.t/C.warn,fieldOnly:spread>0,laneShape:'line'});}
 return r;};
whvAceDeathTick=function(b,dt){const A=b._whv.ace;if(!A._ra7Death){A.key='blue ace';A.i=2;ra7DeathStart(A,b);A._ra7Gate=null;A._pw5Gun=null;
 // A cross-pass warning returns early in the authored renderer. Retire the
 // living evasions here so any lethal hit still shows the complete wreck.
 A.dash=A.desp=A.roll=A.somer=null;eBullets=eBullets.filter(p=>p.owner!==b);}
 const D=A._ra7Death;ra7DeathTick(D,Math.min(.05,dt));b.dying+=dt;A.spin=clamp(D.t/D.dur,0,1)*D.turns*D.dir*Math.PI/180;A.crash=D.crashed;b.x=A.x;b.y=A.y;whiteBlast=0;};
XART.rdy(RA7.sheet);
