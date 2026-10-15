"use strict";
/* Storm Sovereign: one moving formation for hull, generators and target locks.
   The October 11 stationary generator anchor fought the camera-relative hull
   stations. It also sent lightning-tagged balls through the fireball renderer. */
const S4AC13={base:{nodes:stage4ShieldSyncNodes,helper:stage4CoreTurretTarget,tick:er26Tick,
 shot:er26Shot,warShot:stage4WarfareShot,projectile:er26ProjectileDraw,
 element:enemyOrdnanceElement,impact:ordnanceBreak1002,muzzle:er26Muzzle}};
function s4ac13Owns(b){return !!(b?._ship==='stormsovereign'&&b._s4war&&!b._s4war.mini);}
stage4ShieldSyncNodes=function(b){
 if(!s4ac13Owns(b))return S4AC13.base.nodes.apply(this,arguments);
 const H=b._s4war.shield;if(!H)return;
 // The ship station already reserves this complete formation width. Sockets
 // follow the same hull translation; they cannot drift behind its shield.
 H.anchorX=Math.min(VW*.5-36,b.w*.67+36);H.anchorY=46;H.rowOffset=78;
 for(const n of H.nodes){n.x=b.x+n.side*H.anchorX;n.y=(b._drawY??b.y)+H.anchorY+n.row*H.rowOffset;}
};
stage4CoreTurretTarget=function(b,side){
 if(!s4ac13Owns(b))return S4AC13.base.helper.apply(this,arguments);
 const H=b._s4war.shield,pair=H?.nodes.filter(n=>n.side===side);
 if(!pair?.length)return S4AC13.base.helper.apply(this,arguments);
 // A helper occupies the gap BETWEEN its two generator sockets. Its former
 // Furious vertical bob could cover a socket even after fixing the main hull.
 return {x:clamp(pair.reduce((sum,n)=>sum+n.x,0)/pair.length,56,worldWidth()-56),
  y:pair.reduce((sum,n)=>sum+n.y,0)/pair.length};
};
er26Tick=function(b,dt){const r=S4AC13.base.tick.apply(this,arguments);
 // Some attacks move after their shield tick. Finalize geometry this same
 // simulation frame, before projectile collision, Retina and drawing use it.
 if(s4ac13Owns(b))stage4ShieldSyncNodes(b);return r;
};
function s4ac13Electric(q){return !!q&&(q._s4Electric1013||q._ap10Lightning||q._er26Art==='lightning'||q._tb28?.art==='storm');}
function s4ac13Mark(q){if(!q||q.dead)return q;
 q._s4Electric1013=true;q._er26Art='lightning';q._er26Charred=false;
 q.kind='s4bomb';q._s4wKind='orb';q._bfam='storm';q._noArsenal=true;
 return q;
}
er26Shot=function(b){const q=S4AC13.base.shot.apply(this,arguments);return s4ac13Owns(b)?s4ac13Mark(q):q;};
stage4WarfareShot=function(b,slot,ang,spd,role){const q=S4AC13.base.warShot.apply(this,arguments);
 return s4ac13Owns(b)&&role==='orb'?s4ac13Mark(q):q;
};
er26Muzzle=function(b,slot){if(s4ac13Owns(b))return stage4WarfareMuzzle(b,slot,'orb',.8,.16);
 return S4AC13.base.muzzle.apply(this,arguments);
};
er26ProjectileDraw=function(q){
 if(!s4ac13Electric(q))return S4AC13.base.projectile.apply(this,arguments);
 // Exact authored sixteen-frame ball-lightning reel; no magma fallback and
 // no extra whole-sprite rotation layered over its internal lightning motion.
 const key='s4w_lightning_ball_'+(Math.floor((q.t||0)*18)%16);
 if(!XART.rdy(key))return true;
 const im=XART.get(key),size=q._er26Draw||62*(q.szMul||1);
 ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,Math.round(q.x)-size/2,Math.round(q.y)-size/2,size,size);ctx.restore();return true;
};
enemyOrdnanceElement=function(q){return s4ac13Electric(q)?'lightning':S4AC13.base.element.apply(this,arguments);};
ordnanceBreak1002=function(q){
 if(!s4ac13Electric(q))return S4AC13.base.impact.apply(this,arguments);
 if(q._fbImpact1002)return;q._fbImpact1002=true;q._intercepted=true;
 if(q._tb28){q._tb28.dead=true;q._tb28.phase='done';}
 efxBurst('lightning',q.x,q.y,Math.min(76,Math.max(38,(q._er26Draw||q.w||26)*1.1)));
 Audio.SFX.enemyElectricBolt?.();
};
