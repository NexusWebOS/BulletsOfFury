'use strict';
/* Nyx is a Retina-only signal until the completed lock burns her cloak away. */
const NY46={base:{targets:retinaBossTargets,hit:rebelSquadHitTest,damage:rebelSquadDamage,
 reveal:rd21Reveal,attack:rg4Attack,act:rg4AttackTick,tick:rebelSquadTick,ship:fr27RebelDrawShip,reflect:rr26Reflect},scan:0,events:[]};
function ny46Own(q,b=boss){return rr33Group(b)&&q?.key==='nyx'&&b._rebels.ships.includes(q);}
function ny46Hidden(q){if(!ny46Own(q)||!boss._rebels.frIntro?.done)return false;if(q._ny46Hidden==null){q._ny46Hidden=true;q._rr26Fade=1;}return q._ny46Hidden||q._ny46Revealing>0||q._rr26Fade>.02;}
function ny46Target(t){return t?._retinaOwner===boss&&String(t._retinaId||'').startsWith('nyx')||!!t&&boss?._rebels?.ships.some(q=>q===t&&q.key==='nyx');}
function ny46Log(event){NY46.events.push({event,time:rg4State()?.age||0});if(NY46.events.length>100)NY46.events.shift();}
function ny46Cloak(q){q._ny46Hidden=true;q._ny46Revealing=0;q._rd21Cloak=true;q.frCloak=10;q._rr26Fade=1;ny46Log('cloaked');}
rd21Reveal=function(q,reason){if(!ny46Own(q))return NY46.base.reveal.apply(this,arguments);if(reason!=='retina'||!q._ny46Hidden||q.dead)return false;
 q._rd21Cloak=true;const r=NY46.base.reveal.call(this,q,reason);q._ny46Hidden=false;q._ny46Revealing=1;q._rd21Visible=7;q._ra7CloakDemo=null;ny46Log('retina-reveal');return r;};
retinaBossTargets=function(b){let out=NY46.base.targets.apply(this,arguments);const q=b?._rebels?.ships.find(q=>ny46Own(q,b)&&!q.dead);if(!q||!b._rebels.frIntro?.done)return out;
 const hidden=ny46Hidden(q);out=out.filter(t=>!String(t._retinaId||'').startsWith('nyx'));
 if((!hidden||NY46.scan)&&!b._rebels.gang1004?.scene)out.push(retinaDynamicPiece(b,'nyx-retina','rival',()=>({x:q.x,y:q.y,hp:q.hp,dead:q.dead}),d=>{if(ny46Hidden(q))return;b._rebels.hit=q.i;b._rebels.frHit=null;hitBoss(d);},62,70));return out;};
rebelSquadHitTest=function(b){const q=b?._rebels?.ships.find(q=>ny46Own(q,b)&&!q.dead);if(!q||!ny46Hidden(q))return NY46.base.hit.apply(this,arguments);
 q.dead=true;try{return NY46.base.hit.apply(this,arguments);}finally{q.dead=false;}};
rebelSquadDamage=function(b){const q=b?._rebels?.ships[b._rebels.hit];if(ny46Own(q,b)&&ny46Hidden(q)){b._rebels.hit=-1;b._rebels.frHit=null;return false;}return NY46.base.damage.apply(this,arguments);};
rg4Attack=function(q){if(ny46Own(q)&&ny46Hidden(q)){q.rg4.cd=Math.max(.4,q.rg4.cd);return;}const r=NY46.base.attack.apply(this,arguments);
 if(ny46Own(q)){q._rd21Cloak=false;q.frCloak=0;}return r;};
rg4AttackTick=function(q){if(!ny46Own(q))return NY46.base.act.apply(this,arguments);if(ny46Hidden(q)){q.rg4.act=null;return;}
 const A=q.rg4?.act,r=NY46.base.act.apply(this,arguments);if(A?.kind==='nx37ambush'&&A.phase==='cloak')ny46Cloak(q);else{q._rd21Cloak=false;q.frCloak=0;}return r;};
function ny46Locked(){const q=boss?._rebels?.ships.find(q=>ny46Own(q)&&!q.dead);if(q?._ny46Hidden)rd21NyxLock(boss,q);}
for(const name of ['cycleLock','updateRetina','retinaScanInput','retinaScanDirection','retinaScanAdd','retinaScanTick','retinaScanFire']){
 const old=globalThis[name];if(typeof old!=='function')continue;
 globalThis[name]=function(){NY46.scan++;try{return old.apply(this,arguments);}finally{NY46.scan--;ny46Locked();}};
}
rebelSquadTick=function(b,dt){const q=b?._rebels?.ships.find(q=>ny46Own(q,b)&&!q.dead);if(q&&ny46Hidden(q)&&q._ny46Hidden){q._rd21Cloak=true;q.frCloak=10;}
 const r=NY46.base.tick.apply(this,arguments);if(!q||q.dead||!b._rebels.frIntro?.done)return r;
 if(q._ny46Hidden==null)ny46Cloak(q);q._ny46Revealing=Math.max(0,(q._ny46Revealing||0)-dt);
 if(q._ny46Hidden){q._rd21Cloak=true;q.frCloak=10;q._rr26Fade=1;}else{q._rd21Cloak=false;q.frCloak=0;}
 if(ny46Hidden(q)){for(const a of s6Wing?.ships||[])if(ny46Target(a.target)){a.target=null;a.think=0;}
  for(const p of pBullets)for(const k of ['tgt','target','_target'])if(ny46Target(p[k]))p[k]=null;
  for(const p of b._rebels.gang1004?.rr26?.returns||[])if(p.target===q){p.target=b._rebels.ships.find(s=>s!==q&&!s.dead);if(!p.target)p.dead=true;}}
 return r;};
rr26Reflect=function(G,o){const q=boss?._rebels?.ships.find(q=>ny46Own(q)&&!q.dead&&ny46Hidden(q));if(!q)return NY46.base.reflect.apply(this,arguments);
 if(!boss._rebels.ships.some(s=>s!==q&&!s.dead)){o.dead=true;return;}q.dead=true;try{return NY46.base.reflect.apply(this,arguments);}finally{q.dead=false;}};
fr27RebelDrawShip=function(q){if(ny46Own(q)&&q._ny46Hidden&&boss._rebels.frIntro?.done)return false;return NY46.base.ship.apply(this,arguments);};
globalThis.BOF_NYX_RETINA_1029=NY46;
