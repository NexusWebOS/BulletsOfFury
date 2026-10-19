"use strict";
/* Five-on-five readability: rotate background gun lanes, give the active
   special priority, commit each short gun tell, and retain all five arsenals. */
const RBAL19={events:[],draws:0,paintAlpha:1,base:{gun:ra4Gun,attack:rg4Attack,tick:rg4AttackTick,ship:fr27RebelDrawShip},cfg:{
 easy:{slots:1,heavySlots:0,turn:1.30,cd:1.35,tell:.36,speed:2.9,warm:1.15,row:1.35,alpha:.55},
 normal:{slots:2,heavySlots:1,turn:1.15,cd:1.10,tell:.30,speed:3.3,warm:1.12,row:1.20,alpha:.58},
 hard:{slots:3,heavySlots:1,turn:1.05,cd:.95,tell:.25,speed:3.7,warm:1.00,row:1.05,alpha:.58},
 furious:{slots:3,heavySlots:1,turn:.92,cd:.82,tell:.22,speed:4.0,warm:.92,row:.92,alpha:.58},
 insanity:{slots:3,heavySlots:2,turn:.88,cd:.78,tell:.20,speed:4.1,warm:.90,row:.88,alpha:.58}}};
function rbal19Off(){return window.RBAL19_OFF===1;}
function rbal19Cfg(){return RBAL19.cfg[diffKey]||RBAL19.cfg.normal;}
function rbal19Log(event,q,data={}){RBAL19.events.push({event,pilot:q?.key,time:rg4State()?.age||0,...data});if(RBAL19.events.length>200)RBAL19.events.shift();}
function rbal19Heavy(q){const A=q.rg4?.act;return !q.dead&&A&&A.phase!=='recover'&&['turbo','ram','fusion','helix','rookhook'].includes(A.kind);}
function rebelFriendlyBulletAlpha(q){return !rbal19Off()&&q.ally&&run.stage===6&&rg4State()&&!rg4Scene()?rbal19Cfg().alpha:1;}
function rebelFriendlyBulletBegin(q){const old=RBAL19.paintAlpha;RBAL19.paintAlpha=rebelFriendlyBulletAlpha(q);return old;}
function rebelFriendlyBulletEnd(old){RBAL19.paintAlpha=old;}
// A projectile's nested art helpers may assign their own opacity. Apply the
// ally factor once at the actual pixel operation, then restore immediately.
// Only this native game context is wrapped; ship/HUD/cached-art contexts and
// player bullets have factor 1. The per-bullet finally always ends the scope.
for(const method of ['drawImage','fill','stroke','fillRect','strokeRect','fillText','strokeText']){
 const native=ctx[method];ctx[method]=function(){
  if(RBAL19.paintAlpha===1)return native.apply(this,arguments);
  const prior=this.globalAlpha;this.globalAlpha=prior*RBAL19.paintAlpha;
  try{return native.apply(this,arguments);}finally{this.globalAlpha=prior;}
 };
}
// Elemental/Wind owners paint their rounds after the base bullet loop. Give
// those real carriers the same bounded scope, including their nested helpers.
for(const name of ['ea11RoundDraw','wp11Draw','ap10WindRoundDraw']){
 const native=window[name];if(typeof native!=='function')continue;
 window[name]=function(q){const prior=rebelFriendlyBulletBegin(q);
  try{return native.apply(this,arguments);}finally{rebelFriendlyBulletEnd(prior);}
 };
}
ra4Gun=function(q,G,dt){if(rbal19Off()||!G?.arsenal1004c)return RBAL19.base.gun.apply(this,arguments);
 const M=q.rg4,R=boss?._rebels,C=rbal19Cfg();if(!M||!R||!ra4Alive(q)||G.scene||q.stun>0){if(M)M._rbal19Gun=null;return;}
 M.gunCd=Math.max(0,(M.gunCd||0)-dt);
 const hook=R.ships.some(v=>!v.dead&&v.rg4?.act?.kind==='rookhook'&&v.rg4.act.phase!=='recover');
 const special=M.act&&M.act.phase!=='recover',heavy=R.ships.some(rbal19Heavy);
 // Invisible fire is owned by Nyx's separately warned Ghostknife volleys.
 if(hook||special||q.frCloak>0){M._rbal19Gun=null;return;}
 const live=R.ships.filter(v=>ra4Alive(v)&&!(v.rg4?.act&&v.rg4.act.phase!=='recover')&&!v.frCloak),slots=heavy?C.heavySlots:C.slots;
 const start=Math.floor(G.age/C.turn)%Math.max(1,live.length),selected=live.some((v,i)=>v===q&&((i-start+live.length)%live.length)<slots);
 if(!M._rbal19Gun){if(!selected||M.gunCd>0)return;const target=ra4Target(q,M.gunN),ref=target.ref,side=(M.gunN+1)%2?1:-1;
  M._rbal19Gun={t:0,warm:C.tell,side,tx:ref.x,ty:ref.y,target:target.key};rbal19Log('gun-tell',q,{warm:C.tell,target:target.key});return;}
 const T=M._rbal19Gun;T.t+=dt;if(T.t<T.warm)return;
 const a=Math.atan2(T.ty-q.y-28,T.tx-q.x-T.side*18),z=rg4Round({x:q.x+T.side*18,y:q.y},a,C.speed,'s6tracer',{_ra4Gun:true,_ra4Slug:q.key==='rook',owner:q,_rbal19:true});
 M.gunN++;M.gunCd=C.cd;M._rbal19Gun=null;q._ra4GunFlash=.1;
 wm26Emit?.(q,z.x,z.y-12,a,q.key==='rook'?'chaingun':'mg',null,{size:20,life:.1});
 (q.key==='rook'?Audio.SFX.enemyMachineGunHeavy:Audio.SFX.enemyShoot)?.();rbal19Log('gun-release',q,{warm:T.warm,speed:C.speed,target:T.target});
};
rg4Attack=function(q,R,G){const before=q.rg4?.act,r=RBAL19.base.attack.apply(this,arguments),A=q.rg4?.act;
 if(!rbal19Off()&&G?.arsenal1004c&&A&&A!==before){A.warm=Math.max(.9,A.warm*rbal19Cfg().warm);q.rg4._rbal19Gun=null;rbal19Log('special-tell',q,{kind:A.kind,warm:A.warm});}
 return r;
};
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act,phase=A?.phase,r=RBAL19.base.tick.apply(this,arguments);
 if(!rbal19Off()&&A&&q.rg4.act===A&&A.kind==='turbo'&&A.phase==='row'&&phase!=='row')A.warm=rbal19Cfg().row;
 return r;
};
fr27RebelDrawShip=function(q){const r=RBAL19.base.ship.apply(this,arguments),T=q.rg4?._rbal19Gun;
 if(!rbal19Off()&&!q.dead&&T){const p=clamp(T.t/T.warm,0,1);av3Muzzle(ctx,q.x+T.side*18,q.y+28,11+7*p,q.key==='rook'?'fire':'yellow',rg4State()?.age||0,.35+.4*p);RBAL19.draws++;}
 return r;
};
window.BOF_REBEL_BALANCE={state:RBAL19,cfg:rbal19Cfg};
