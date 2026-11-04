"use strict";
/* ============================================================
   READABILITY (drop 1103) — RD13. Loaded last. window.RD13_OFF=1 disables it. All difficulties.

   From the wave pressure audit (docs/WAVE_AUDIT_1103.md), two things hid enemy fire in the films:

   1. EXPLOSIONS PAINT OVER BULLETS. drawWorld draws drawBullets() before drawEffects(), so every
      explosion covers the rounds inside it. Big units explode big by Mike's own rule (authored death
      frame = unit frame +25%, COVER_TARGET), up to ~330 px on Stage 9, so the size stays. Instead,
      after the effects pass, every live enemy round that sits inside a live explosion gets a small
      THREAT PIP stamped on top: a white core and a ring in the round's own colour, on the 1015 pixel
      ladder. The explosion art is untouched; the round just stays findable through it.
   2. WARNING LANES STACK. combatWarningDraw is the shared telegraph. Two or three translucent cones at
      once tint most of the field and stop meaning "move". Each frame the two most imminent owners
      (highest warning progress) draw at full strength; any others draw at 35% (q.alpha, which the
      FOV drawer already honours). Nothing is removed and timing is unchanged.
   ============================================================ */
(function(){
if(window.RD13_OFF)return;
const RD={frame:0,prog:new Map(),next:new Map(),rank:new Set(),stat:{pips:0,dimmed:0}};
const clockNow=()=>typeof efxClock==='number'?efxClock:(typeof stateT==='number'?stateT:0);
const LADDER=[.32,.52,.74,.95];

/* frame boundary: rank owners from last frame's warning progress */
if(typeof drawWorld==='function'){
  const baseWorld=drawWorld;
  drawWorld=function(){
    if(!window.RD13_OFF){
      RD.frame++;RD.prog=RD.next;RD.next=new Map();
      RD.rank=new Set([...RD.prog.entries()].sort((a,b)=>b[1]-a[1]).slice(0,2).map(e=>e[0]));
    }
    return baseWorld.apply(this,arguments);
  };
}
if(typeof combatWarningDraw==='function'){
  const baseWarn=combatWarningDraw;
  combatWarningDraw=function(owner,q){
    if(window.RD13_OFF||!owner||!q||q.alertOnly||q.progress==null)return baseWarn.apply(this,arguments);
    const k=Math.max(0,Math.min(1,q.progress));RD.next.set(owner,Math.max(RD.next.get(owner)||0,k));
    if(RD.prog.size>2&&RD.prog.has(owner)&&!RD.rank.has(owner)){
      RD.stat.dimmed++;
      return baseWarn.call(this,owner,Object.assign({},q,{alpha:(q.alpha==null?1:q.alpha)*.35}));
    }
    return baseWarn.apply(this,arguments);
  };
}
/* threat pips over explosions */
function hueOf(b){
  const h=window.PFX13&&PFX13._hue?PFX13._hue(b):null;
  if(h)return h;
  const k=String(b.kind||'');
  return /ice|cryo|water|s3|s9/.test(k)?'#9fe8ff':/toxic|acid|s7|bio|green/.test(k)?'#9dff6a':/void|s8|s5|chaos|purple/.test(k)?'#d48cff':'#ff6a5a';
}
if(typeof drawEffects==='function'){
  const baseFx=drawEffects;
  drawEffects=function(){
    const out=baseFx.apply(this,arguments);
    if(window.RD13_OFF||typeof explosions==='undefined'||!explosions.length||typeof eBullets==='undefined'||!eBullets.length)return out;
    const big=explosions.filter(ex=>ex&&!ex.dead&&(ex.r||0)>14);if(!big.length)return out;
    const t=clockNow(),step=LADDER[Math.floor(t*12)%LADDER.length];
    ctx.save();ctx.globalCompositeOperation='source-over';ctx.imageSmoothingEnabled=false;
    for(const b of eBullets){
      if(!b||b.dead)continue;
      let under=false;for(const ex of big){const R=(ex.r||ex.max||0)*1.1;if(Math.abs(b.x-ex.x)<R&&Math.abs(b.y-ex.y)<R&&Math.hypot(b.x-ex.x,b.y-ex.y)<R){under=true;break;}}
      if(!under)continue;
      const x=Math.round(b.x),y=Math.round(b.y),c=hueOf(b);
      ctx.globalAlpha=.9;ctx.fillStyle='#120a14';ctx.fillRect(x-3,y-3,6,6);        // dark seat so the pip reads on white fire
      ctx.globalAlpha=step;ctx.fillStyle=c;ctx.fillRect(x-3,y-2,6,4);ctx.fillRect(x-2,y-3,4,6);
      ctx.globalAlpha=1;ctx.fillStyle='#ffffff';ctx.fillRect(x-1,y-1,2,2);
      RD.stat.pips++;
    }
    ctx.restore();
    return out;
  };
}
window.RD13={state:RD,version:'1103'};
})();
