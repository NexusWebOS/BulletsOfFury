"use strict";
/* Shared ordinary-enemy shield geometry. Native energy, contact and timers own combat. */
const BET24={base:{shield:drawEnemyShieldLayer,enemy:drawEnemy,equip:enemyShieldEquip},bars:0};
function bet24Hull(e){
 const A=bf22Model(e),M=A?.M||AF21.aliases.get(e.type)?.M;
 if(M){const expected=(A?bf22Span(e,M):Math.max(e.w||30,e.h||30)*(AIR13.aliases.get(e.type)?.nativeRatios?.[e.type]||1))*(e._pScale??e._scale??1);
  const measured=A&&e._bf22Rendered?.scale!=null?e._bf22Rendered.scale*M.span:expected;
  // A preceding legacy canvas transform must not become the shell's hull size.
  const span=measured>0&&measured<=expected*1.5?measured:expected;
  return {w:span,h:span};}
 // Legacy full texture dimensions include transparent padding; never let them
 // grow an ordinary shield beyond its native hull envelope.
 return {w:Math.min(e._drawW||e.w||30,(e.w||30)*1.75),h:Math.min(e._drawH||e.h||30,(e.h||30)*1.75)};
}
enemyShieldEquip=function(e){const r=BET24.base.equip.apply(this,arguments);
 if(e?._esh)e._elite24Max=Math.max(e._elite24Max||0,e.maxhp||e._maxhp||e.hp||1);return r;};
drawEnemyShieldLayer=function(e,front){const s=e?._esh;if(!s||e.dead||e._dyingT!=null)return;
 const F=ENEMY_SHIELD_FAMILY[s.family],h=bet24Hull(e);if(!F)return;
 e._elite24Max=Math.max(e._elite24Max||0,e.maxhp||e._maxhp||e.hp||1);
 const name=FV21_SHIELDS[s.family];
 if(name){if(!front)return;const t=s.animT||0,energy=clamp(s.energy/Math.max(1,s.max),0,1);
  let alpha=.22+.16*energy;if(s.phase==='deploy')alpha*=clamp(t/.34,0,1);else if(s.phase==='broken')alpha*=clamp(1-t/.30,0,1);
  const size=Math.max(h.w,h.h)*1.35;e._shield24Size=size;
  return fv21Frame(name,efxClock+(e.t||0)*.1,e.x,e.y,size,alpha,false,0,s.hitT||0);
 }
 const w=e._drawW,hh=e._drawH;e._drawW=h.w;e._drawH=h.h;
 try{return FV21.base.shield.call(this,e,front);}finally{e._drawW=w;e._drawH=hh;}
};
function bet24Bar(e){if(!e._esh||e.dead||e._dyingT!=null||!(e.hp>0)||e._mini||e.prop||e._prop)return;
 const A=globalThis.BET24_ART;if(!A||!XART.rdy(A.frame.key)||!XART.rdy(A.fill.key))return;
 const h=bet24Hull(e),w=48,k=w/A.frame.w,y=e.y+h.h/2+5,x=e.x-w/2;
 const frac=clamp(e.hp/Math.max(1,e._elite24Max||e.maxhp||e._maxhp||e.hp),0,1),F=A.fill;
 ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(A.frame.key),x,y,w,A.frame.h*k);
 if(frac>0)ctx.drawImage(XART.get(F.key),0,0,Math.max(1,Math.floor(F.w*frac)),F.h,x+A.aperture[0]*k,y+A.aperture[1]*k,F.w*frac*k,F.h*k);
 ctx.restore();BET24.bars++;
}
drawEnemy=function(e){const r=BET24.base.enemy.apply(this,arguments);bet24Bar(e);return r;};

// Live Chronos speech now uses command_ui_1020's external HUD radio; the
// cinematic director retains its timing and combat continuation ownership.
