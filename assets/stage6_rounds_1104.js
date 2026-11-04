"use strict";
/* ============================================================
   STAGE 6 FIGHTER ROUNDS (drop 1104) - S6R14. Loaded last. window.S6R14_OFF=1 disables it.

   Mike: "enhance the stage 6 new fighters bullets, I can barely see em".
   The new Stage 6 fighters (stage6_airframe_1101, S611) route their gun rounds through _s611Ammo='slug'
   and drew them from a bank that had recoloured the source slug cyan and shrunk it to ~13x5 px, drawn
   at 28 px: about 6x2 game px of pale cyan, the same colour as the rain, the jets' paint and the sky.
   This draws the SAME authored source slug (mgcf_1_2) in its own amber, unscaled (1 source px = 1 game
   px, ~6x14 px body) with a 1 px dark seat outline, built offline by build_s6_rounds_1104.py.
   Draw only: the round's kind, speed, hitbox, owner and S611 socket routing are untouched, and PFX13
   still adds its pixel glow, rim and trail around whatever this draws.
   ============================================================ */
(function(){
if(window.S6R14_OFF)return;
const B=S6R14_ART.slug,base={early:ovSonicProjectileDraw,final:drawCombatFinalProjectile,load:stageLoadBegin},stat={drawn:0};
XART._src[B.key]=B.path;
function draw(b){
  if(!XART.rdy(B.key))return false;
  const d=s1aDir(Math.atan2(b.vy,b.vx),B.dirs),f=Math.floor(projectileVisualAge(b)*22)%B.frames,s=B.drawSize;
  ctx.save();ctx.imageSmoothingEnabled=false;
  try{ctx.drawImage(XART.get(B.key),d*B.cell,f*B.cell,B.cell,B.cell,Math.round(b.x)-s/2,Math.round(b.y)-s/2,s,s);}finally{ctx.restore();}
  stat.drawn++;return true;
}
// Fall back to the S611 draw while the sheet decodes, so a round is never invisible.
ovSonicProjectileDraw=function(b){if(b?._s611Ammo&&!window.S6R14_OFF&&draw(b))return true;return base.early.apply(this,arguments);};
drawCombatFinalProjectile=function(b){if(b?._s611Ammo&&!window.S6R14_OFF&&draw(b))return true;return base.final.apply(this,arguments);};
stageLoadBegin=function(n,keys){if(n===6)keys=[...(keys||[]),B.key];return base.load.call(this,n,keys);};
window.S6R14={stat,art:B,version:'1104'};
})();
