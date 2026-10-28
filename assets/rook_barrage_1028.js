"use strict";
const RK38={attack:rg4Attack,act:rg4AttackTick,kind:ra4AttackKind,tick:rebelSquadTick,ship:fr27RebelDrawShip,warning:rg4Warning,projectile:drawCombatFinalProjectile,impact:pw5Impact,intercept:enemyOrdnanceCanIntercept,damage:rebelSquadDamage,events:[]};
for(const name of ['slugs','spin_symbol','hull_glow']){XART._src['rk38_'+name]='assets/game/levels/stage_06/boss/rook_barrage_1028/'+name+'.png';XART.rdy('rk38_'+name);}
for(let i=0;i<4;i++)XART.rdy('xlz_lightning_impact_'+i);XART.rdy('ngm_shock_7');
function rk38Slug(p){return p?._rr26Rook||p?._rk38Round||p?._ra4Slug||p?.owner?.key==='rook'&&p.kind==='s6tracer';}
pw5Impact=function(p){return rk38Slug(p)?null:RK38.impact.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(p){return rk38Slug(p)?false:RK38.intercept.apply(this,arguments);};
drawCombatFinalProjectile=function(p){if(!rk38Slug(p))return RK38.projectile.apply(this,arguments);if(!XART.rdy('rk38_slugs'))return true;
 const a=Math.atan2(p.vy,p.vx),f=Math.round(((a-Math.PI/2+TAU)%TAU)/TAU*32)%32+32*(Math.floor((p.t||0)*20)%2);
 ctx.drawImage(xartPalette('rk38_slugs','#ff982f'),f%8*48,Math.floor(f/8)*48,48,48,p.x-24,p.y-24,48,48);return true;};
ra4AttackKind=function(q,G){if(q.key==='rook')return ['slug','ram','rk38spin'][(q._rk38Book=(q._rk38Book??-1)+1)%3];return RK38.kind.apply(this,arguments);};
rg4Attack=function(q,R,G,forced){if(q.key!=='rook')return RK38.attack.apply(this,arguments);if(q._rk38Stun){q.rg4.cd=1;return;}
 const kind=forced||q.rg4.armed||ra4AttackKind(q,G);if(kind!=='ram'&&kind!=='rk38spin')return RK38.attack.call(this,q,R,G,'slug');
 if(G.rd21?.fleet||R.ships.some(s=>s!==q&&rbal19Heavy(s))){q.rg4.cd=.6;return;}
 const A=rd21Personal(q,R,G,kind==='ram'?'rk38dash':'rk38spin');Object.assign(A,{warm:kind==='ram'?1.4:2.2,home:{x:q.x,y:q.y},from:{x:q.x,y:q.y},hit:new Set(),spin:0});
 if(kind==='rk38spin'){A.phase='advance';A.center={x:clamp(A.target.ref.x,camLeftX()+100,camRightX()-100),y:VH*.57};}return A;
};
function rk38Path(q,A,to,duration){const u=clamp(A.t/duration,0,1),v=u*u*(3-2*u);q.x=lerp(A.from.x,to.x,v);q.y=lerp(A.from.y,to.y,v);return u===1;}
function rk38Phase(q,A,phase){A.phase=phase;A.t=0;A.from={x:q.x,y:q.y};}
rg4AttackTick=function(q,R,G,dt){if(q.key==='rook'&&q._rk38Stun)return;const A=q.rg4?.act;if(!['rk38dash','rk38spin'].includes(A?.kind))return RK38.act.apply(this,arguments);
 if(!rd21Live(q)){q.rg4.act=null;return;}dt=Math.min(.05,dt);A.t+=dt;q.evadeT=0;q._rd21Scale=1;
 if(A.phase==='advance'){q.rfHeading=Math.atan2(A.center.y-A.from.y,A.center.x-A.from.x);if(rk38Path(q,A,A.center,1.4)){rk38Phase(q,A,'charge');A.ox=q.x;A.oy=q.y;}return;}
 if(A.phase==='charge'){q.x=A.ox;q.y=A.oy;q.rfHeading=Math.PI/2;if(A.t<A.warm*.68){A.tx=A.target.ref.x;A.ty=A.target.ref.y;A.a=Math.atan2(A.ty-q.y,A.tx-q.x);}combatWarningTick(A,'rook-'+A.kind,A.t,A.warm);
  if(A.t<A.warm)return;rk38Phase(q,A,'fire');A.cd=0;A.travel=0;if(A.kind==='rk38dash'){A.end={x:clamp(A.tx,camLeftX()+55,camRightX()-55),y:Math.min(VH-60,A.ty+65)};Audio.SFX.chargeDash?.();}else A.turns=rd21Rank()>=2?3:2.5;
 }
 if(A.phase==='fire'){
  if(A.kind==='rk38dash'){const u=clamp(A.t/.62,0,1);q.x=lerp(A.from.x,A.end.x,u*u);q.y=lerp(A.from.y,A.end.y,u*u);q.rfHeading=Math.atan2(A.end.y-A.from.y,A.end.x-A.from.x);ra4RamHit(q,A);if(u===1)rk38Phase(q,A,'flip');}
  else{q.x=A.from.x;q.y=A.from.y;A.spin=clamp(A.t/3.6,0,1)*TAU*A.turns;q.rfHeading=Math.PI/2+A.spin;A.cd-=dt;
   if(A.cd<=0){for(const side of [-1,1]){const p=rr26Socket(q,side),a=q.rfHeading,z=eShootT(p.x,p.y,a,3.0,'s6tracer',{silent:true,noMuzzle:true});Object.assign(z,{_rk38Round:true,owner:q,_boss:true});wm26Emit(q,p.x,p.y,a,'chaingun','#ff982f',{size:24,life:.09});}Audio.SFX.enemyMachineGunHeavy?.();A.cd=.10;}
   if(A.t>=3.6){RK38.events.push({event:'spin-complete',degrees:A.turns*360});rk38Phase(q,A,'recover');}}
 }else if(A.phase==='flip'){q._rk38Frame=32+Math.min(8,Math.floor(A.t/.35*8));if(A.t>=.35)rk38Phase(q,A,'somer');}
 else if(A.phase==='somer'){const done=rk38Path(q,A,A.home,1.4);q.rfHeading=-Math.PI/2;q._rk38Frame=40+Math.min(7,Math.floor(A.t/1.4*8));if(done){delete q._rk38Frame;rk38Phase(q,A,'recover');}}
 else if(A.phase==='recover'){delete q._rk38Frame;q.rfHeading=Math.PI/2;if(rk38Path(q,A,A.home,1.2))rd21Finish(q,G,3.8);}
};
rg4Warning=function(q,A){if(q.key==='rook'&&q._rk38Stun)return;if(q.key==='rook'&&A?.phase==='charge'){
 if(A.kind==='rr26chain'){for(const side of [-1,1]){const p=rr26Socket(q,side);rd21Fov(A,p.x,p.y,A.a,24,A.t/A.warm);}ra4LockWarning({...A,target:{ref:{x:A.tx,y:A.ty}}},'rook');return;}
 if(A.kind==='rk38spin'){const p=clamp(A.t/A.warm,0,1),color=p<.45?'#5aff79':p<.78?'#ffe455':'#ff334d',r=viewW()*.42;rr26Effect('ngm_shock_7',q.x,q.y,r*2,.85,color);rr26Effect('rk38_spin_symbol',q.x,q.y-78,46,1,color);return;}
 if(A.kind==='rk38dash'){rd21Fov(A,q.x,q.y,A.a,76,A.t/A.warm);return;}}
 return RK38.warning.apply(this,arguments);};
rebelSquadDamage=function(b,dmg){const q=b?._rebels?.ships[b._rebels.hit],before=q?.hp,shot=typeof _dmgBullet==='undefined'?null:_dmgBullet,src=typeof _dmgSrc==='undefined'?'':_dmgSrc;
 const result=RK38.damage.apply(this,arguments);if(q?.key!=='rook'||q.dead||!(q.hp<before))return result;
 const missile=src==='missile'||shot&&(/missile|rocket/i.test(shot.kind||'')||shot._missile||shot._missileVariant);if(!missile)return result;
 if(shot&&typeof shot==='object'){q._rk38Seen??=new WeakSet();if(q._rk38Seen.has(shot))return result;q._rk38Seen.add(shot);}
 const G=b._rebels.gang1004,now=G?.age||0;const hits=q._rk38Missiles||(q._rk38Missiles=[]);if(shot&&hits.some(h=>h.shot===shot)||!shot&&hits.some(h=>now-h.t<.07))return result;
 q._rk38Missiles=hits.filter(h=>now-h.t<=3);q._rk38Missiles.push({t:now,shot});const oldY=q.y;q.y=Math.max(PLAY.y+50,q.y-22);const push=q.y-oldY;if(q._rk38Stun)q._rk38Stun.y=q.y;const A=q.rg4?.act;
 if(A){if(Number.isFinite(A.oy))A.oy+=push;for(const k of ['from','center'])if(A[k])A[k].y+=push;}
 RK38.events.push({event:'missile-knockback',count:q._rk38Missiles.length});
 if(q._rk38Missiles.length>=5&&!q._rk38Stun){q._rk38Stun={t:3,x:q.x,y:q.y};q.stun=3;if(q.rg4){q.rg4.act=null;q.rg4._rbal19Gun=null;}q._rk38Missiles=[];delete q._rk38Frame;Audio.SFX.retinaLockBeep?.();RK38.events.push({event:'stunned'});}return result;
};
rebelSquadTick=function(b,dt){const r=RK38.tick.apply(this,arguments),q=b?._rebels?.ships.find(q=>q.key==='rook');if(!q?._rk38Stun)return r;const S=q._rk38Stun;
 if(q.dead){delete q._rk38Stun;return r;}S.t-=dt;q.x=S.x;q.y=S.y;q.rfHeading=Math.PI/2;q.rg4.act=null;q.rg4._rbal19Gun=null;q.stun=Math.max(.01,S.t);q.rg4.cd=1;
 if(S.t<=0){delete q._rk38Stun;q.stun=0;q.rg4.cd=2;RK38.events.push({event:'stun-recovered'});}return r;};
fr27RebelDrawShip=function(q){if(q.key!=='rook'||q.dead||rr33Protected()||rg4State()?.rd21?.fleet)return RK38.ship.apply(this,arguments);
 const B=RR33_ART.banks.flight_rook;if(!XART.rdy(B.key))return RK38.ship.apply(this,arguments);const a=q.rfHeading??Math.PI/2,f=q._rk38Frame??Math.round(((a+TAU)%TAU)/TAU*32)%32;
 const rect=[f%B.cols*B.cw,Math.floor(f/B.cols)*B.ch,B.cw,B.ch,q.x-B.pivot[0],q.y-B.pivot[1],B.cw,B.ch];
 ctx.drawImage(q.flash>0?xartTint(B.key,'#ffffff',1):XART.get(B.key),...rect);
 if(q._rk38Stun){if(q.flash<=0&&XART.rdy('rk38_hull_glow')){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha*=PXG_STEPS[1+Math.floor((q.t||0)*18)%5];ctx.drawImage(XART.get('rk38_hull_glow'),...rect);ctx.restore();}
  for(let i=0;i<3;i++){const t=(q.t||0)*4+i*TAU/3;rr26Effect('xlz_lightning_impact_'+(Math.floor((q.t||0)*20+i)%4),q.x+Math.cos(t)*35,q.y+Math.sin(t)*36,42,1,'#bfeeff');}return;}
 if(q._rk38Frame==null)for(const side of [-1,1]){const x=q.x+Math.cos(a)*13-Math.sin(a)*side*23,y=q.y+Math.sin(a)*13+Math.cos(a)*side*23;er28Blit('rook_pod',er28Dir(a-Math.PI/2)+Math.floor((q.t||0)*20)%4*64,x,y,q.flash>0);}
 const A=q.rg4?.act;if(A)rg4Warning(q,A);
};
