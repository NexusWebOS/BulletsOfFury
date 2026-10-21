"use strict";
/* One whole authored actor per frame. Native encounters still own combat and FX. */
const HA21={base:{draw:hammerBossDraw,get:XART.get,tint:xartTint,arch:hammerArchFrame,
 head:hammerHeadPoint,pose:hb20Pose,tool:hb20Pick,load:stageLoadBegin,keys:v18Keys,warm:v18Warm,
 enter:v18Enter,rig:v19HammerRig,pickup:hb20Pickup,chrome:hammerChromiumSheet,energy:hammerEnergySheet,beam:hammerChromiumDraw},tags:new WeakMap(),draws:{},last:null,suppressed:0,painting:null};
for(const [id,a] of Object.entries(HA21_ART.sheets))XART._src[a.key]=a.path;
for(const rows of Object.values(HA21_ART.banks))for(const a of rows)BOFX.cells[a.key]=[a.sheet,...a.cell];
function ha21Keys(n=0){const prefix=n===5?'ha21_blue_':n===8?'ha21_corrupt_':'';return [...Object.entries(HA21_ART.sheets).filter(([id])=>id.startsWith(prefix)).map(([,a])=>a.key),...([0,5].includes(n)?['arch_hammer_flight_0926','arch_hammer_lightning_0926']:[])];}
function ha21Ready(n=run.stage){let ready=true;for(const k of ha21Keys(n))if(!XART.rdy(k))ready=false;return ready;}
stageLoadBegin=function(n,keys){return HA21.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?ha21Keys(n):[])]);};
v18Keys=function(){return [...HA21.base.keys(),...ha21Keys(8)];};
v18Warm=function(){return HA21.base.warm()&&ha21Ready(8);};
XART.get=function(key){const im=HA21.base.get.apply(this,arguments);if(im)HA21.tags.set(im,String(key));return im;};
xartTint=function(key){const im=HA21.base.tint.apply(this,arguments);if(im)HA21.tags.set(im,String(key));return im;};
hammerArchFrame=function(key){const q=HA21.base.arch.apply(this,arguments);if(q?.im)HA21.tags.set(q.im,'arch_'+key);return q;};
hammerChromiumSheet=function(key){const im=HA21.base.chrome.apply(this,arguments);if(im)HA21.tags.set(im,key);return im;};
hammerEnergySheet=function(key){const im=HA21.base.energy.apply(this,arguments);if(im)HA21.tags.set(im,key);return im;};
if(HA21_ART.banks.blue_counter_right){HM10_ART.swing_right=HA21_ART.banks.blue_counter_right;HM10_ART.swing_left=HA21_ART.banks.blue_counter_left;}
const HA21_ACTOR=/^(?:arch_(?:idle|leap_strike_0922|orbital_sweep_0926|storm_charge_0926|hammer_overhead_0926|hammer_throw_0926|combat_0923|arsenal_cast_0926|whirlwind_0926|ship_transform|spiked_ball|twirl_throw(?:_0922)?|spell_raise|chaingun_break_enrage)|hm10_(?:swing_|shield_form)|pt11_hammer_core|fr27_chromium_actions|hb20_blue_(?:slam|side|idle|entry|spin|dance|throw)|ha21_)/;
const HA21_RECOVERY_KEYS=new Set(['arch_stun_0920',...HMF19_ART.banks.recovery.map(a=>a.key)]);
function ha21Frame(name,u=0){const rows=HA21_ART.banks[name];return rows?.[Math.min(rows.length-1,Math.floor(clamp(u,0,.999999)*rows.length))];}
function ha21Pose(name,u=0,k=1.75,rot=0){const a=ha21Frame(name,u);return a&&XART.rdy(a.key)?{a,k,rot,kind:name}:null;}
function ha21Span(a,b,p){return lerp(a,b,clamp(p,0,1))/16;}
function ha21Blue(b){const h=b._hammer,s=h.state,t=h.t||0,C=h.hc11Counter;
 if(b.dead||b._gp4Host||(hf19Recovery(b)&&!['recharge1002','recover','back','giant_recover'].includes(s)))return null;
 const A=fr27Armor(b),armor=A?.hp>0&&A.activated;
 const finish=(name,u=0,k=1.75,rot=0)=>ha21Pose('blue_'+name+(armor&&HA21_ART.banks['blue_'+name+'_armor']?'_armor':''),u,k,rot);
 if(h.hb20Pickup){const t=h.hb20Pickup.t;return finish('slam',t<.8?0:t<1.78?ha21Span(0,11,(t-.8)/.98):ha21Span(11,16,(t-1.78)/1.07));}
 const music=b._hammerTime||b._hama;
 if(music&&music.mode!=='attack'){
  if(music.mode==='intro'&&music.musicStarted&&music.shipFrame!=null)return finish('from_ship',clamp((15-music.shipFrame)/9,0,1));
  return null;
 }
 if(C){const bank=(C.side>0?'blue_counter_right':'blue_counter_left')+(armor?'_armor':'');return ha21Pose(bank,hc11Frame(C)/16,.70*C.scale,C.angle);}
 if(s==='fr_activation')return ha21Pose('blue_chromium',t/FR27_ACT.end);
 if(['flyby','return'].includes(s))return finish('from_ship',0);
 if(s==='unfold')return finish('from_ship',t/2);
 if(s==='curl'){const p=clamp(t/HAMMER_BALL_WARN,0,1);return finish('to_ball',p,lerp(1.75,.85,p));}
 if(s==='uncurl'){const p=clamp(t/1.25,0,1);return finish('to_ball',1-p,lerp(.85,1.75,p));}
 if(s==='ball')return finish('to_ball',1,.85,h.angle||0);
 if(['spin','revenge_charge'].includes(s))return finish('throw',ha21Span(0,6,t/HAMMER_SPIN_TIME));
 if(['fr_twirl','whirl_warn','whirl_turn','whirlwind'].includes(s))return finish('spin',(t/(s==='whirlwind'?.48:.7))%1);
 if(s==='throw')return finish('throw',ha21Span(7,16,t/.30));
 if(s==='hammer_catch')return finish('throw',1-clamp(t/.24,0,1));
 if(s==='warn')return finish('jump',ha21Span(0,7,t/(hammerFurious()?.58:1.2)));
 if(s==='storm_warn')return finish('slam',ha21Span(0,7,t/(hammerFurious()?.9:hammerHard()?1:1.15)));
 if(s==='storm_slam')return finish('slam',ha21Span(7,12,t/(hammerFurious()?.46:hammerHard()?.52:.6)));
 if(s==='storm_split')return finish('slam',ha21Span(12,0,t/.75));
 if(s==='leap')return finish('jump',ha21Span(7,10,t/(hammerFurious()?.27:.52)));
 if(s==='recover')return finish('jump',ha21Span(10,16,t/hammerRecoverDuration()));
 if(s==='giant_windup'||s==='giant_rise')return finish('slam',ha21Span(0,7,t/(s==='giant_rise'?1:.48)),1.75*hammerDepthScale(b));
 if(s==='giant_warn')return finish('slam',ha21Span(7,10,t/1.1),1.75*hammerDepthScale(b));
 if(s==='giant_dive')return finish('slam',ha21Span(10,12,t/.52),1.75*hammerDepthScale(b));
 if(s==='giant_sweep')return finish('slam',ha21Span(12,16,t/.44),1.75*hammerDepthScale(b));
 if(s==='giant_recover')return finish('slam',ha21Span(16,0,t/.8),1.75*hammerDepthScale(b));
 if(['storm_raise','storm_rebuild','recharge1002'].includes(s)||h.recovery?.status==='charging')return finish('hold',Math.min(1,t/1.25));
 if(['spell','spell_blast'].includes(s))return finish(h.hammerDestroyed?'cast_empty':'cast',s==='spell'?t/2.35:.8+(t% .3)/1.5);
 if(['mega_charge','mega_beam'].includes(s))return finish('beam_empty',s==='mega_charge'?t/1.65:.7+(t% .4)*.5);
 if(['enrage','core_orbit'].includes(s))return finish(h.hammerDestroyed?'rage_empty':'rage',t/2.15);
 if(['nova_charge','nova_release'].includes(s))return finish('hold',s==='nova_charge'?t/1.6:1);
 if(s==='shield')return armor?ha21Pose('blue_chromium',1):finish('hold',1);
 if(['chain_warn','chaingun','chain_cool','chaingun_draw','uzi'].includes(s))return null;
 // Chromium remains a solid authored plated form after the takeover.
 if(armor)return ha21Pose('blue_chromium',1);
 return ha21Pose('blue_idle');
}
function ha21Body(b,q){b20Image(q.a,b.x,b.y,q.k,q.rot,Math.max(b.flash||0,b._lastPart?.flash||0));HA21.last=q;HA21.draws[q.kind]=(HA21.draws[q.kind]||0)+1;}
function ha21Flash(b,q){const flash=Math.max(b.flash||0,b._lastPart?.flash||0);if(!(flash>0))return;
 const im=xartTint(q.a.key,'#ffffff',1);if(!im)return;ctx.save();ctx.translate(b.x,b.y);ctx.rotate(q.rot);ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=Math.min(.90,flash/.12);
 ctx.drawImage(im,-q.a.pivot[0]*q.k,-q.a.pivot[1]*q.k,q.a.w*q.k,q.a.h*q.k);ctx.restore();
}
hammerBossDraw=function(b){const q=ha21Blue(b);if(!q)return HA21.base.draw.apply(this,arguments);
 const front=q.kind.includes('beam_empty')||b._hammer.state==='throw',old=HA21.painting;HA21.painting=b;
 if(front)ha21Body(b,q); // Native laser and detached hammer paint in front of the torso.
 const draw=ctx.drawImage;ctx.drawImage=function(im,...args){const key=HA21.tags.get(im);if(key&&(HA21_ACTOR.test(key)||HA21_RECOVERY_KEYS.has(key))){HA21.suppressed++;return;}return draw.call(this,im,...args);};
 try{HA21.base.draw.apply(this,arguments);}finally{ctx.drawImage=draw;HA21.painting=old;}
 if(!front)ha21Body(b,q);else ha21Flash(b,q); // White hit feedback wins over the colored warning field.
};
hammerChromiumDraw=function(x,y,...args){const b=HA21.painting;
 if(b&&b._hammer.state==='mega_beam'&&Math.abs(x-b.x)<1&&Math.abs(y-(b.y-20))<1)y=b.y;
 return HA21.base.beam.call(this,x,y,...args);
};
hammerHeadPoint=function(b){const h=b?._hammer;
 if(!h||h.throw||h.hc11Counter)return HA21.base.head.apply(this,arguments);
 const q=ha21Blue(b);if(!q||!q.a.tip)return HA21.base.head.apply(this,arguments);
 return hb20World(q.a,q.a.tip,b,q.k,q.rot);
};
hb20Pose=function(b){const Q=hb20State(b),A=Q?.action;if(!Q)return HA21.base.pose.apply(this,arguments);
 const t=A?.t||0,u=t-(A?.tell||0);let name=null,p=0,k=1.75*(Q.scale||1),rot=0;
 const S=b._r30;
 if(S.mode==='v18formIn')return ha21Pose('corrupt_from_ship',S.t/1.6,k)||HA21.base.pose.apply(this,arguments);
 if(A){
  if(A.type==='skystrike'){name='jump';p=u<0?ha21Span(0,7,t/A.tell):ha21Span(7,13,u/.65);}
  else if(A.type==='pickup'){name='slam';p=t<.8?0:t<1.78?ha21Span(0,8,(t-.8)/.98):ha21Span(8,16,(t-1.78)/1.07);}
  else if(A.type==='break'){name='stun';p=t<.6?t/.6:t<3.8?1:1-clamp((t-3.8)/.8,0,1);}
  else if(A.type==='side'){name='side';p=u<0?ha21Span(0,7,t/A.tell):ha21Span(7,16,u/1.3);}
  else if(A.type==='throw'){name='throw';p=u<0?ha21Span(0,6,t/A.tell):1;}
  else if(A.type==='ball'){name='to_ball';p=u<0?t/A.tell:1;k=lerp(1.75,1.35,clamp(t/A.tell,0,1));if(u>=0)rot=u*TAU*1.6;}
  else if(A.type==='charge'){name=u<0?'hold':'cast';p=u<0?t/A.tell:Math.min(1,.6+u*.2);}
  else if(A.type==='shield'){name='chromium';p=t/Math.max(.1,A.tell);}
  else if(A.type==='luminaire'){name=Q.broken?'beam_empty':'beam';p=t/A.tell;}
  else if(A.type==='spin'){name='spin';p=u<0?0:(u/.7)%1;}
  else if(A.type==='fire'){name='rage_empty';p=t/A.duration;}
 }
 if(name){const q=ha21Pose('corrupt_'+name,p,k,rot);if(q)return q;}
 if(!A&&!Q.rage)return ha21Pose('corrupt_idle',0,k)||HA21.base.pose.apply(this,arguments);
 return HA21.base.pose.apply(this,arguments);
};
// Keep collision masks and visible whole-body plates registered to one source.
// Existing hit and native part-flash owners are used by v19Paint/b20Image.
v18Enter=function(b,n,form){const r=HA21.base.enter.apply(this,arguments);if(n===2&&form===8)ha21Ready();return r;};
hb20Pickup=function(b,corrupt=false){const C=HA21.base.pickup.apply(this,arguments),a=ha21Frame(corrupt?'corrupt_slam':'blue_slam',(corrupt?8:11)/16);
 if(a)C.box=hb20World(a,a.tip,C.station,1.75);return C;};
// Match the native committed impact, without changing its damage/safe footprint.
function ha21Landing(b,target,kind,frame,scale=1.75){if(b._gp4Host)return null;
 const a=ha21Frame('blue_'+kind,frame/16);if(!a||!XART.rdy(a.key))return null;
 return{x:target.x-(a.tip[0]-a.pivot[0])*scale,y:target.y-(a.tip[1]-a.pivot[1])*scale};
}
window.BOF_HAMMER_ACTING=HA21;
