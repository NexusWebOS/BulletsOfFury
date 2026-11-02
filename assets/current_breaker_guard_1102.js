"use strict";
/* CBG: Current Breaker guard pass (Claude Code, Nov 2). Late layer after current_breaker_1102.js; CB112 keeps the
   actor, attack book, art, hazards, counters, HP pools, hit flash and death. This layer only:
   - LIQUID PHASES ABSORB: the orb approach, the transformation, the marble-pulse orb and the reform are water. Ordinary
     hits splash on the surface and do no damage (no damage flash), so a Stage-9 loadout (~144 dps measured) can no
     longer kill him before he finishes transforming. He is vulnerable whenever he stands or flies as the humanoid.
   - BACKGROUND IS OUT OF REACH: while he casts from depth (scaled back into the starfield) he leaves the collision and
     lock lists, so rounds pass over him. The authored counter still lands: a missile-reflected roller returns into
     depth for its native 22 damage.
   - HP x CBG_HP on every difficulty (keeps the Normal 1 -> Hard 1.15 -> Furious 1.3225 ladder): the humanoid windows
     total ~14 s; this lets a full-dps pilot see the grenade bank and a flight pass before the kill.
   - WARNINGS: CB112 warns the first tidal shove only (during its charge); volleys 2 and 3 now get the same palm lanes
     for the 0.6 s before release. Background rollers get a tracking aim lane from the casting palm for 0.35 s.
   window.CBG_OFF=1 disables everything. */
const CBG_HP=4;
const CBG_LIQUID=new Set(['entry','transform','reform','marble','marble-settle']);
const CBG_DEPTH=new Set(['depth-arrive','depth-settle','depth-charge','depth-spin','depth-linger','depth-return-exit']);
const CBG={base:{hit:hitEnemy,targets:spaceTargets,locks:_lockTargets,draw:s911Draw,effects:cb112Effects,init:cb112Init},counter:false,splashAt:-1,absorbed:0,events:[]};
function cbgOn(){return !window.CBG_OFF;}
function cbgPhase(e){return cb112Own(e)&&e._cb112?e._cb112.phase:null;}
function cbgDepth(e){const q=e&&e._cb112,p=cbgPhase(e);return !!p&&(CBG_DEPTH.has(p)||p==='depth-exit'&&q.scale<.7);}
function cbgLiquid(e){const p=cbgPhase(e);return !!p&&CBG_LIQUID.has(p);}
// HP scale applied once, at the same moment CB112 claims the actor. Recomputed through S911's own shared-curve call
// with the scaled definition (not rounded-value x4), so Hard/Furious stay within 1 HP of Normal x1.15/x1.3225.
cb112Init=function(e){const fresh=!e._cb112,q=CBG.base.init.apply(this,arguments);
 if(fresh&&cbgOn()&&!e._cbgHp){e._cbgHp=true;const D=S911.defs[e._s911?.model],full=Number.isFinite(e.maxhp)&&e.hp>=e.maxhp;
  const hp=D&&D.hp?Math.ceil(difficultyHealthBaseline15(D.hp*CBG_HP,D.hp*CBG_HP*[1,1.24,1.5][s911Rank()])*(coopActive()?1.5:1)):e.hp*CBG_HP;
  e.hp=full||!Number.isFinite(e.maxhp)?hp:e.hp*hp/e.maxhp;e.maxhp=e._maxhp=hp;if(Number.isFinite(e.maxHp))e.maxHp=hp;}return q;};
// The roller counter calls hitEnemy from inside cb112Effects; mark that window so depth still takes it.
cb112Effects=function(){CBG.counter=true;try{return CBG.base.effects.apply(this,arguments);}finally{CBG.counter=false;}};
hitEnemy=function(e){if(!cbgOn()||!cb112Live(e))return CBG.base.hit.apply(this,arguments);
 if(cbgLiquid(e)||cbgDepth(e)&&!CBG.counter){const b=_dmgBullet,x=b&&Number.isFinite(b.x)?b.x:e.x,y=b&&Number.isFinite(b.y)?b.y:e.y;CBG.absorbed++;
  if(efxClock-CBG.splashAt>.09&&!cbgDepth(e)){CBG.splashAt=efxClock;CB112.fx.push({e,x,y,t:0,life:.4,size:46});if(CB112.fx.length>64)CB112.fx.shift();}
  return;}
 return CBG.base.hit.apply(this,arguments);};
spaceTargets=function(){const a=CBG.base.targets.apply(this,arguments);return cbgOn()?a.filter(t=>!cbgDepth(t)):a;};
_lockTargets=function(){const a=CBG.base.locks.apply(this,arguments);return cbgOn()?a.filter(t=>!cbgDepth(t)):a;};
s911Draw=function(e){const r=CBG.base.draw.apply(this,arguments);if(!cbgOn()||!cb112Live(e)||e._dyingT!=null)return r;const q=e._cb112;if(!q)return r;
 if(q.phase==='tidal'&&q.round>0&&q.next-q.t<.6&&q.next<=3.75){const u=1-(q.next-q.t)/.6;for(const p of s911Guns(e))cb112Warn(e,p.x,p.y,Math.PI/2,u,150);}
 if(q.phase==='depth-spin'&&q.next-q.t<.35&&q.next<=6.1){const ports=s911Guns(e),p=ports[q.round%2],T=targetShip(e.x,e.y);if(p)cb112Warn(e,p.x,p.y,Math.atan2(T.y-p.y,T.x-p.x),1-(q.next-q.t)/.35,44);}
 return r;};
globalThis.BOF_CURRENT_BREAKER_GUARD_1102={state:CBG,hp:CBG_HP,liquid:CBG_LIQUID,depth:CBG_DEPTH,isDepth:cbgDepth,isLiquid:cbgLiquid};
