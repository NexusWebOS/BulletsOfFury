/* Native playtest observer only. No gameplay changes or forced damage/kills. */
window.OV19={units:[],map:new WeakMap(),active:new Set(),projectiles:new WeakSet(),attribution:new WeakMap(),tags:new WeakMap(),emitter:null,scope:null,serial:0,unattributed:{},draws:0,
 runtime:{scripts:[...document.scripts].map(s=>s.src).filter(Boolean),shoulder:typeof SG19!=='undefined',stealth:typeof SK19!=='undefined',rebel:typeof RBAL19!=='undefined',herald:typeof HD19!=='undefined',lizzieSpread:typeof LSP19!=='undefined',lateHulls:typeof LE19!=='undefined',wardenTiming:typeof WT19!=='undefined',volcanoHead:typeof VH19!=='undefined',harrierFans:typeof HF19!=='undefined'}};
function ov19Time(){return PT18.play/60;}
function ov19Unit(q,kind,role='enemy'){
 if(!q||typeof q!=='object')return null;let m=OV19.map.get(q);if(m)return m;
 m={id:++OV19.serial,kind:String(kind||q.type||q._ship||q.kind||q.key||'unknown'),role,stage:run.stage,born:ov19Time(),firstPixels:null,firstWarning:null,firstAttack:null,firstProjectile:null,rounds:0,releases:0,warnings:[],art:[],projectileTraits:[],lastSeen:ov19Time(),ended:null,dead:false,initialHP:q.hp};
 OV19.map.set(q,m);OV19.units.push(m);OV19.active.add(q);return m;
}
const ov19Spawn=spawnEnemy;spawnEnemy=function(kind){const n=enemies.length,r=ov19Spawn.apply(this,arguments);for(let i=n;i<enemies.length;i++)ov19Unit(enemies[i],enemies[i].type||kind);if(r&&enemies.includes(r))ov19Unit(r,r.type||kind);return r;};
function ov19Owner(q){return [q?.owner,q?._v18Owner,q?._s7modOwner,q?._heraldOwner1003,q?._hc1007Owner,q?._er26Owner,OV19.attribution.get(q),q?._boss?(bossActive?boss:subBossActive?subBoss:null):null].find(v=>v&&typeof v==='object'&&OV19.map.has(v))||null;}
function ov19Attack(q,kind){const m=OV19.map.get(q)||(q===boss?ov19Unit(q,q._ship||q.kind,'boss'):q===subBoss?ov19Unit(q,q._ship||q.kind,'mini'):null);if(!m)return;
 m.firstAttack??=ov19Time();m.releases++;if(!m.attackKinds)m.attackKinds={};m.attackKinds[kind]=(m.attackKinds[kind]||0)+1;
}
const ov19Release=eb11Release;eb11Release=function(e,q){const old=OV19.emitter;OV19.emitter=e;try{const r=ov19Release.apply(this,arguments);ov19Attack(e,'queued-'+(e._s5space||e._s6storm||e._s9void||e.type));return r;}finally{OV19.emitter=old;}};
for(const n of ['s5SpaceTick','s6StormTick','s7ToxicTick','s8EnemyTick','s9VoidTick','s3IceTick','s4ChaseTick','s2VolcTick','jetManeuverTick','shipBossManoeuvre','updateBoss','updateSubBoss']){
 const fn=window[n];if(typeof fn!=='function')continue;
 window[n]=function(q){const old=OV19.emitter;OV19.emitter=q&&typeof q==='object'&&(q.type||q.kind||q._ship)?q:n==='updateBoss'?boss:n==='updateSubBoss'?subBoss:old;try{return fn.apply(this,arguments);}finally{OV19.emitter=old;}};
}
for(const n of ['eShootT','eShoot']){const fn=window[n];if(typeof fn!=='function')continue;window[n]=function(){const before=eBullets.length,q=fn.apply(this,arguments);if(OV19.emitter){for(let i=before;i<eBullets.length;i++)OV19.attribution.set(eBullets[i],OV19.emitter);if(q&&typeof q==='object')OV19.attribution.set(q,OV19.emitter);}return q;};}
const ov19AiBegin=ai27Begin,ov19AiEnd=ai27End,ov19Enemies=typeof updateEnemies==='function'?updateEnemies:null;
ai27Begin=function(e){OV19.emitter=e;return ov19AiBegin.apply(this,arguments);};
ai27End=function(){try{return ov19AiEnd.apply(this,arguments);}finally{OV19.emitter=null;}};
if(ov19Enemies)window.updateEnemies=function(){OV19.emitter=null;try{return ov19Enemies.apply(this,arguments);}finally{OV19.emitter=null;}};
const ov19Warn=combatWarningTick;combatWarningTick=function(owner,key,t,warm){const m=OV19.map.get(owner)||(owner===boss?ov19Unit(owner,owner._ship||owner.kind,'boss'):owner===subBoss?ov19Unit(owner,owner._ship||owner.kind,'mini'):null);
 if(m){m.firstWarning??=ov19Time();const w=m.warnings.find(w=>w.key===String(key));if(w)w.warm=warm;else if(m.warnings.length<80)m.warnings.push({key:String(key),time:ov19Time(),warm});}return ov19Warn.apply(this,arguments);};
const ov19Ground=groundTargetingSpawn;groundTargetingSpawn=function(o){const q=ov19Ground.apply(this,arguments);if(o?.owner)ov19Attack(o.owner,'ground-'+o.kind);return q;};
const ov19Beam=s81003Beam;s81003Beam=function(b){const q=ov19Beam.apply(this,arguments);ov19Attack(b,'beam');return q;};
const ov19Get=XART.get;XART.get=function(key){const im=ov19Get.apply(this,arguments);if(im&&typeof im==='object')OV19.tags.set(im,key);return im;};
const ov19Draw=ctx.drawImage;ctx.drawImage=function(im,...a){const q=OV19.scope,m=q&&OV19.map.get(q);
 if(m&&m.firstPixels==null&&q.x>=camLeftX()&&q.x<=camRightX()&&(q._drawY??q.y)>=PLAY.y&&(q._drawY??q.y)<=VH&&this.globalAlpha>.02){
  const tag=typeof PXG!=='undefined'?PXG.tags.get(im):null,key=OV19.tags.get(im)||tag?.key||'';
  if(!/shadow|muzzle|reticle|alert|fov|smoke|exhaust/i.test(key)&&im){const n=a.length,dx=n>=8?a[4]:a[0],dy=n>=8?a[5]:a[1],w=n>=8?a[6]:n>=4?a[2]:im.width,h=n>=8?a[7]:n>=4?a[3]:im.height,M=this.getTransform();
   const points=[[dx,dy],[dx+w,dy],[dx,dy+h],[dx+w,dy+h]].map(([x,y])=>({x:x*M.a+y*M.c+M.e,y:x*M.b+y*M.d+M.f}));
   if(Math.max(...points.map(p=>p.x))>0&&Math.min(...points.map(p=>p.x))<this.canvas.width&&Math.max(...points.map(p=>p.y))>0&&Math.min(...points.map(p=>p.y))<this.canvas.height){m.firstPixels=ov19Time();if(key)m.art.push(key);OV19.draws++;}
  }
 }return ov19Draw.call(this,im,...a);
};
for(const n of ['drawEnemy','drawBoss','drawSubBoss']){const fn=window[n];window[n]=function(q){const old=OV19.scope;const who=n==='drawEnemy'?q:n==='drawBoss'?boss:subBoss;OV19.scope=who;if(who)ov19Unit(who,who.type||who._ship||who.kind,n==='drawEnemy'?'enemy':n==='drawBoss'?'boss':'mini');try{return fn.apply(this,arguments);}finally{OV19.scope=old;}};}
const ov19After=pt18After;pt18After=function(){ov19After();OV19.emitter=null;
 const now=ov19Time(),live=new Set(enemies);if(boss)live.add(boss);if(subBoss)live.add(subBoss);
 for(const q of live){const m=ov19Unit(q,q.type||q._ship||q.kind,q===boss?'boss':q===subBoss?'mini':'enemy');m.lastSeen=now;m.dead=!!q.dead;if(q.dead)m.ended??=now;}
 for(const q of OV19.active)if(!live.has(q)){const m=OV19.map.get(q);m.ended??=now;m.dead=!!q.dead;OV19.active.delete(q);}
 for(const q of eBullets)if(!OV19.projectiles.has(q)){OV19.projectiles.add(q);const owner=ov19Owner(q),m=owner&&OV19.map.get(owner),kind=q._er26Source||q._s4wKind||q.kind;
  if(m){m.firstProjectile??=now;m.rounds++;if(!m.projectileKinds)m.projectileKinds={};m.projectileKinds[kind]=(m.projectileKinds[kind]||0)+1;
   const intercept=!!enemyOrdnanceCanIntercept(q),homingFlag=!!q.homing,key=String(kind)+'|'+intercept+'|'+homingFlag;
   if(!m.projectileTraits.some(t=>t.key===key))m.projectileTraits.push({key,kind,w:q.w,h:q.h,speed:Math.hypot(q.vx||0,q.vy||0),intercept,homingFlag,lockFlag:!!q.lock,defensiveProof:!!enemyDefensiveProof(q)});
  }else OV19.unattributed[kind]=(OV19.unattributed[kind]||0)+1;
 }
};
window.ov19Summary=()=>({method:'Actual Chromium index/current owners. Visible-center authored drawImage, real warning/release calls, spawned projectile attribution. Protected bot; no human-survival claim. A missing projectile can be a melee/minelayer/beam owner; inspect attackKinds and behavior.',runtime:OV19.runtime,units:OV19.units,unattributed:OV19.unattributed,drawnUnits:OV19.draws});
