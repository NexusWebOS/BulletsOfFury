'use strict';
// Preserve the previous burst treatment as an opt-in effect for a future encounter.
const C43={draw:hammerBossDraw,tick:hammerBossTick,damage:hammerBossDamage,hit:bossHitTest,blue:ha21Blue,legacyTransformationDraw:c30ChargeDraw,legacyBurstDrive:cgDrive};
function c43Bolt(x,y,height,frame,widthScale=1){const key='c42_bolt_'+(frame%8);if(!XART.rdy(key))return;const k=height/256;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),x-32*k*widthScale,y,64*k*widthScale,height);ctx.restore();}
ha21Blue=function(b){if(c25Own(b)&&b._hammer._hf22Charge){const u=cgChargeU(b);if(u<.30){const bank=cgThrowBank(b);return c27Pose(b,'throw_empty',clamp(u/.30,0,1),1,c26Material(b));}const N=C29_ART.banks.rage_regular.length;return c29Pose('rage',clamp((u-.30)/.62,0,1)*(N-1),u>=.92?'red':'regular');}return C43.blue.apply(this,arguments);};
hammerBossDamage=function(b){if(c25Own(b)&&b._hammer._hf22Charge)return 0;return C43.damage.apply(this,arguments);};
bossHitTest=function(b){if(c25Own(b)&&b._hammer._hf22Charge)return false;return C43.hit.apply(this,arguments);};
hammerBossTick=function(b,dt){if(!c25Own(b)||b.dead)return C43.tick.apply(this,arguments);
 const old=b._c43Float||{x:0,y:0};b.x-=old.x;b.y-=old.y;const r=C43.tick.apply(this,arguments),h=b._hammer;
 const t=efxClock,depth=hammerDepthScale(b),u=h._hf22Charge?cgChargeU(b):null;
 const offset={x:Math.sin(t*.9)*2.5*depth,y:Math.sin(t*1.35)*4*depth+(u!=null&&u<.30?Math.sin(Math.PI*u/.30)*46:0)};
 b.x+=offset.x;b.y+=offset.y;b._drawY=b.y;b._c43Float=offset;if(h._hf22Charge)b._noHit=true;return r;};
hammerBossDraw=function(b){if(!c25Own(b)||!b._hammer._hf22Charge)return C43.draw.apply(this,arguments);
 const C=b._hammer._hf22Charge,u=cgChargeU(b);ctx.save();
 // Accelerating strikes replace shock rings and smoke during the transformation.
 const clock=u*7.2,beat=Math.floor(2*clock+1.8*clock*clock),f=beat%8;
 if(u>=.30&&u<.92){const lanes=[-100,75,-55,110,-80,45],x=b.x+lanes[beat%lanes.length];c43Bolt(x,viewTopY()-8,Math.max(160,b.y+110-viewTopY()),f);}
 if(u<.10)cgHeldTool(b);
 ha21Body(b,ha21Blue(b));
 if(u>=.10&&u<.34){const from=cgReleasePoint(b);if(!C.c43South)C.c43South={x:from.x,y:PLAY.y+PLAY.h+180};const p=clamp((u-.10)/.24,0,1);CG.toolBase(b,from,C.c43South,p,CG_TOOL_K,Math.PI/2+p*Math.PI*4);C43.lastThrow={from,to:C.c43South,p};}
 if(u>=.92&&!C.c44Burst){C.c44Burst=true;fxBurst(b.x,b.y,190,{color:'#ff3a18',rings:3});shake=Math.max(shake,18);c33Sound('thunder',b);}
 if(u>=.92){const height=Math.max(480,b.y+8-viewTopY());c43Bolt(b.x,b.y+8-height,height,Math.min(7,Math.floor((u-.92)/.08*8)),1);shake=Math.max(shake,8);}
 ctx.restore();C43.lastCharge={u,beat,finalStrike:u>=.92,protected:b._noHit};};
window.BOF_CHRONOS_TRANSFORM=C43;

const c43DamageOverlay=encounterDamageOverlay;
encounterDamageOverlay=function(b){if(c25Own(b)&&b._hammer._hf22Charge)return;return c43DamageOverlay.apply(this,arguments);};
