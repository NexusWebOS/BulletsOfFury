"use strict";
/* WC1031: contact art only. Native damage, flashes, shields, AoE, audio and death
   stay with their owners. The launched round supplies identity, never run.weapon.
   Reels are source-derived fixed96 cells; no runtime rotation/scale/fade tricks. */
const WC1031={base:{enemy:hitEnemy,boss:hitBoss,mini:hitSubBoss,space:spaceDamageTarget,
 retina:retinaMissileDamage,s7:s7mHit,bomber:siegeBomberHit,feedback:weaponFeedbackDraw,
 chain:chaingunImpact,mist:laserMistImpact,spaceDraw:spaceImpactDraw,begin:beginStage},
 context:null,gates:new WeakMap(),parents:new WeakMap(),serial:0,events:[],draws:{},enabled:true};
for(const a of Object.values(WC1031_ART)){XART._src[a.key]=a.path;XART.rdy(a.key);}
function wc1031Describe(b){
 if(!b||!WC1031.enabled)return null;
 const k=b.kind,lv=clamp(b.colorLv||b.lv||1,1,5),tier=['orange','blue','green','white','red'][lv-1];
 const inf=b._inf||b._el,energy={fire:'red',magma:'red',ice:'blue',fireice:'blue',lightning:'blue',chrome:'white',kinetic:'orange',dark:'violet',toxic:'green',water:'blue',prism:'violet',wind:'green'}[inf];
 if(k==='orb'||k==='shard'||k==='yuriLightningOrb'||k==='yuriLightningBolt'){
  let el=inf||(b._ts?'ice':b._fire?'fire':k.startsWith('yuri')?'lightning':'ice');
  if(el==='magma')el='fire';if(el==='fireice')el='ice';
  return {family:'orb',bank:'orb_'+(WC1031_ART['orb_'+el]?el:'ice'),color:energy||'blue',size:k==='shard'?20:34,mark:24};
 }
 if(['venomx','helix','hxspiral','hfl'].includes(k)||k==='mavlaser'&&b._burstVolley){
  const color=k==='mavlaser'?tier:b._full||b._charged&&b._full!==false?'violet':'green';
  return {family:'helix',bank:'energy_'+color,color,size:k==='venomx'?42:26,mark:24};
 }
 if(k==='spaceLaser')return {family:'cannon',bank:'cannon_'+lv,color:tier,size:27,mark:16};
 if(['laser','beam','spaceHelperBeam','lasermist','mavlaser','chain'].includes(k)){
  const color=energy||(['lasermist','spaceHelperBeam','chain'].includes(k)?'blue':k==='beam'&&lv===4?'orange':tier);
  return {family:'laser',bank:'energy_'+color,color,size:k==='beam'?26:22,mark:17};
 }
 if(b._cal50||['mg','spread','lzslug'].includes(k))return {family:'ballistic',bank:'ballistic',color:energy||'orange',size:b._cal50||k==='lzslug'?25:19,mark:b._cal50||k==='lzslug'?16:12};
 return null;
}
function wc1031Handles(b){return !!wc1031Describe(b);}
function wc1031Owner(t){return t?._retinaOwner||t?._spaceBossOwner||t?._spaceSubOwner||t?._xenoOwner||(t&&WC1031.parents.get(t))||t;}
function wc1031Alive(t){const o=wc1031Owner(t);return !!t&&!t.dead&&!(t.hp<=0)&&!o?.dead&&o?._dyingT==null&&!o?._noHit;}
function wc1031Y(t){return Number.isFinite(t?._drawY)?t._drawY:t?.y;}
function wc1031Target(o,b,x,y){
 if(!o||WC1031.context)return o;
 if(o._rebels){const q=o._rebels.ships[o._rebels.hit];if(q&&!q.dead){WC1031.parents.set(q,o);return q;}}
 if(typeof livePieces!=='function'||!Number.isFinite(x+y))return o;
 let best=null,dist=Infinity;
 for(const t of livePieces(o)){
  if(!wc1031Alive(t)||Math.abs(x-t.x)>(t.w||40)*.5+4||Math.abs(y-wc1031Y(t))>(t.h||40)*.5+4)continue;
  const d=Math.hypot(x-t.x,y-wc1031Y(t));if(d<dist){dist=d;best=t;}
 }return best||o;
}
function wc1031Point(b,t,x,y){
 const ty=wc1031Y(t),w=t.w||t._drawW||40,h=t.h||t._drawH||40;
 if(!Number.isFinite(x))x=b?.x;if(!Number.isFinite(y))y=b?.y;
 // A held beam's origin is the pilot, not its hull contact. Broad AoE contacts
 // also clamp to the struck body instead of leaving scorch in empty space.
 return {x:clamp(Number.isFinite(x)?x:t.x,t.x-w*.42,t.x+w*.42),
  y:b?.kind==='beam'?ty+h*.24:clamp(Number.isFinite(y)?y:ty,ty-h*.42,ty+h*.42)};
}
function wc1031Queue(bank,x,y,size,target,mark){
 const a=WC1031_ART[bank];if(!a)return;
 const f={_weaponContact:true,bank,x,y,size,t:0,dur:a.frames/a.fps,target:target||null,
  ox:target?x-target.x:0,oy:target?y-wc1031Y(target):0,mark:!!mark};
 pImpacts.push(f);if(pImpacts.length>180)pImpacts.splice(0,pImpacts.length-180);return f;
}
function playerWeaponImpact(b,target,x,y,damaged=true){
 const d=wc1031Describe(b);if(!d)return false;
 // Handled collisions must never fall back to a fireball, even when the shield
 // rejected damage. Shield owners already render their own absorption feedback.
 if(!wc1031Alive(target))return true;
 const now=efxClock||0,o=wc1031Owner(target);
 const context=WC1031.context;if(context&&context.owner===o)target=context.target;
 const p=wc1031Point(b,target,x,y),g=WC1031.gates.get(target)||{};
 const tag=d.family,last=g[tag];
 if(last!=null&&now>=last&&now-last<(d.family==='ballistic'?.045:.075))return true;
 g[tag]=now;WC1031.gates.set(target,g);
 // Expiring residue follows the same real hull/part. At most three attached
 // marks per target, while continuous beam contact gets a separate short gate.
 if(damaged&&(!g.mark||now<g.mark||now-g.mark>=.17)){
  g.mark=now;const marks=pImpacts.filter(f=>f._weaponContact&&f.mark&&f.target===target&&f.t<f.dur);
  if(marks.length>=3)marks[0].t=marks[0].dur;
  const bank=d.family==='ballistic'||d.family==='laser'||d.family==='cannon'?'singe_'+(WC1031.serial++%6):'residue_'+d.color;
  wc1031Queue(bank,p.x,p.y,d.mark,target,true);
 }
 wc1031Queue(d.bank,p.x,p.y,d.size,target,false);
 WC1031.events.push({at:now,kind:b.kind,family:d.family,bank:d.bank,x:p.x,y:p.y,damaged});if(WC1031.events.length>240)WC1031.events.shift();
 // Suppress only the matching old space-laser contact decoration, not its
 // native projectile lifetime or sound (shadow/volley blasts are untouched).
 if(b.kind==='spaceLaser')b._wc1031Impact=true;
 return true;
}
function playerWeaponBurst(b,x,y,size){
 const d=wc1031Describe(b);if(!d)return false;
 wc1031Queue(d.bank,x,y,size||d.size,null,false);return true;
}
function wc1031Damage(target,b,x,y,fn){
 if(!wc1031Handles(b)||!wc1031Alive(target))return fn();
 const owner=wc1031Owner(target),old=WC1031.context;
 // The outer exact component/space router retains its target through nested
 // hitBoss/hitSubBoss calls, so one damage event creates one contact.
 if(old&&old.owner===owner)return fn();
 const hp=target.hp,ohp=owner.hp,flash=target.flash||0,oflash=owner.flash||0;
 WC1031.context={owner,target};
 try{const r=fn(),damaged=target.hp<hp||owner.hp<ohp;
  if(damaged||(target.flash||0)>flash||(owner.flash||0)>oflash)playerWeaponImpact(b,target,x,y,damaged);
  return r;
 }finally{WC1031.context=old;}
}
hitEnemy=function(e){const a=arguments,b=_dmgBullet;return wc1031Damage(e,b,b?.x,b?.y,()=>WC1031.base.enemy.apply(this,a));};
hitBoss=function(){const a=arguments,b=_dmgBullet,x=b?.kind==='beam'?_lastHitX:b?.x??_lastHitX,y=b?.kind==='beam'?_lastHitY:b?.y??_lastHitY,o=wc1031Handles(b)?wc1031Target(boss,b,x,y):boss;return wc1031Damage(o,b,x,y,()=>WC1031.base.boss.apply(this,a));};
hitSubBoss=function(d,x,y){const a=arguments,b=_dmgBullet,t=wc1031Handles(b)?wc1031Target(subBoss,b,x,y):subBoss;return wc1031Damage(t,b,x,y,()=>WC1031.base.mini.apply(this,a));};
spaceDamageTarget=function(t,d,b){const a=arguments;return wc1031Damage(t,b,b?.x,b?.y,()=>WC1031.base.space.apply(this,a));};
retinaMissileDamage=function(t,d,b){const a=arguments;return wc1031Damage(t,b||_dmgBullet,t?.x,t?.y,()=>WC1031.base.retina.apply(this,a));};
s7mHit=function(t,d,x,y){const a=arguments;return wc1031Damage(t,_dmgBullet,x,y,()=>WC1031.base.s7.apply(this,a));};
siegeBomberHit=function(t,d,x,y){const a=arguments;return wc1031Damage(t,_dmgBullet,x,y,()=>WC1031.base.bomber.apply(this,a));};
chaingunImpact=function(){if(wc1031Handles(_dmgBullet))return;return WC1031.base.chain.apply(this,arguments);};
laserMistImpact=function(x,y,lv,large){
 const before=new Set(pImpacts),r=WC1031.base.mist.apply(this,arguments);
 // Retain the native mist bubbles, mixer cue and damage ledger; migrate only
 // its two rotating/fading decoration entries to the fixed contact reel.
 for(let i=pImpacts.length-1;i>=0;i--)if(pImpacts[i]._lmFx&&!before.has(pImpacts[i]))pImpacts.splice(i,1);
 if(!pImpacts.some(f=>f._weaponContact&&!f.mark&&f.t<.04&&Math.hypot(f.x-x,f.y-y)<32))playerWeaponBurst({kind:'lasermist',lv},x,y,large?32:25);
 return r;
};
spaceImpactDraw=function(b){if(b._wc1031Impact&&b.family==='laser')return true;return WC1031.base.spaceDraw.apply(this,arguments);};
weaponFeedbackDraw=function(p){
 if(!p._weaponContact)return WC1031.base.feedback.apply(this,arguments);
 const a=WC1031_ART[p.bank];if(!a||p.t>=p.dur||p.target&&!wc1031Alive(p.target))return true;
 if(!XART.rdy(a.key))return true;
 if(p.target){p.x=p.target.x+p.ox;p.y=wc1031Y(p.target)+p.oy;}
 const i=Math.min(a.frames-1,Math.floor(p.t*a.fps)),s=p.size;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';
 ctx.drawImage(XART.get(a.key),i%a.cols*a.cw,Math.floor(i/a.cols)*a.ch,a.cw,a.ch,p.x-s/2,p.y-s/2,s,s);ctx.restore();
 WC1031.draws[p.bank]=(WC1031.draws[p.bank]||0)+1;return true;
};
beginStage=function(){WC1031.context=null;WC1031.gates=new WeakMap();WC1031.parents=new WeakMap();WC1031.events=[];WC1031.draws={};return WC1031.base.begin.apply(this,arguments);};
