"use strict";
/* PixelLab gatling reel, opaque recovery acting and authoritative shield art.
   Combat clocks, hit timers, module health and all warning owners are retained. */
const HMF19={base:{draw:hammerBossDraw,blaster:hammerBlasterDraw,gun:hammerBlasterGunDraw,
 pose:hammerChromiumPoseDraw,orbital:hammerOrbitalPose,damage:hammerBossDamage,absorb:cp12Absorb,
 activation:repair30ChromiumActivationDraw,rig:v19HammerRig,at:v19AtRect,donor:v19DonorDraw,
 warm:v18Warm,keys:v18Keys,load:stageLoadBegin,timeDraw:ht27Draw,corePlate:pt11Plate,timeSprite:ht27Sprite},draws:{}};
function hf19Art(){return Object.values(HMF19_ART.banks).flat();}
for(const a of [...hf19Art(),...HM10_ART.shield_form]){
 XART._src[a.key]=a.path;FMC_ART[a.key]={key:a.key,path:a.path,rects:{pose:[0,0,a.w,a.h]}};
}
function hf19Keys(){return hf19Art().map(a=>a.key);}
function hf19Ready(){return hf19Art().every(a=>XART.rdy(a.key));}
v18Keys=function(){return [...HMF19.base.keys(),...hf19Keys()];};
v18Warm=function(){return HMF19.base.warm()&&hf19Ready();};
stageLoadBegin=function(n,keys){return HMF19.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?hf19Keys():[])]);};
function hf19Shield(b){return !b.dead&&(['shield','fr_activation'].includes(b._hammer.state));}
function hf19Recovery(b){return !b.dead&&['recover','back','giant_recover','giant_knockback','hammer_exposed','hammer_stun','storm_stun','fr_stun','recharge1002'].includes(b._hammer.state);}
function hf19Pick(b){const h=b._hammer;if(b.dead||h.hc11Counter)return null;
 if(hf19Shield(b)){const f=h.state==='fr_activation'?Math.min(15,Math.floor(clamp(h.t/FR27_ACT.end,0,.999)*16)):8+Math.floor(h.t*10)%4;return {a:HM10_ART.shield_form[f],k:HM10.bodyScale,kind:'shield'};}
 if(hf19Recovery(b)){const duration=['hammer_stun','storm_stun','fr_stun'].includes(h.state)?1.6:.6,u=clamp(h.t/duration,0,.999),f=u<.18?2:u<.64?1:u<.85?0:4;return {a:HMF19_ART.banks.recovery[f],k:1.14,kind:'recovery'};}
 if(['chain_warn','chaingun','chain_cool'].includes(h.state)&&!h.chainDestroyed){const fire=h.state==='chaingun'&&(h.chainMuzzle||0)>0;
  const f=fire?1+Math.floor((h.t||0)*16)%8:2;return {a:HMF19_ART.banks.chaingun[f],k:1/.70,kind:'chaingun'};}
 return null;
}
function hf19Plate(b,q){const a=q.a;if(!XART.rdy(a.key))return false;ctx.save();ctx.imageSmoothingEnabled=false;
 const im=b.flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key);
 ctx.drawImage(im,b.x-a.pivot[0]*q.k,b.y-a.pivot[1]*q.k,a.w*q.k,a.h*q.k);ctx.restore();HMF19.draws[q.kind]=(HMF19.draws[q.kind]||0)+1;return true;
}
function hf19Caption(b){const c=b._hammer.cp12Caption;if(!(c?.t>0))return;const x=clamp(b.x,camLeftX()+150,camRightX()-150),y=Math.max(PLAY.y+26,b.y-125);
 ctx.save();ctx.fillStyle='rgba(3,8,17,.9)';ctx.fillRect(x-148,y-17,296,31);bmfDrawOn(ctx,window.BOF_UI_FACE||'game',c.text.toUpperCase(),x,y-6,10,'center');ctx.restore();
}
hammerBossDraw=function(b){const active=(!b._hammerTime||b._hammerTime.mode==='attack')&&(!b._hama||b._hama.mode==='attack'),q=active?hf19Pick(b):null;
 if(q&&q.kind!=='chaingun'&&hf19Plate(b,q)){hammerBossAtmosphereDraw(b);if(q.kind==='recovery'){hammerStunEffectsDraw(b);hammerRecoveryBurstDraw(b);}hm10WallDraw(b);hf19Caption(b);return;}
 return HMF19.base.draw.apply(this,arguments);
};
repair30ChromiumActivationDraw=function(b){const q=hf19Pick(b);return q?.kind==='shield'&&hf19Plate(b,q)||HMF19.base.activation.apply(this,arguments);};
hammerBlasterDraw=function(b){const q=hf19Pick(b);if(q?.kind==='chaingun'&&hf19Plate(b,q)){const m=hammerBlasterMount(b),h=b._hammer;if(h.chainMuzzle>0&&typeof wm26Draw==='function')wm26Draw(ctx,'chaingun',m.x,m.muzzleY,Math.PI/2,1-h.chainMuzzle/.09,48);return;}return HMF19.base.blaster.apply(this,arguments);};
hammerBlasterGunDraw=function(b){if(hf19Pick(b)?.kind==='chaingun')return;return HMF19.base.gun.apply(this,arguments);};
// A full, short native silhouette flash must win over the Chromium colour mask.
hammerChromiumPoseDraw=function(b,key,r,k,base){if(!(b.flash>0))return HMF19.base.pose.apply(this,arguments);
 const h=b._hammer,empowered=h.empowered;h.empowered=false;try{return HMF19.base.pose.call(this,b,key,r,k,xartTint(key,'#ffffff',1)||base);}finally{h.empowered=empowered;}
};
hammerOrbitalPose=function(b,f,scale,tint){if(!(b.flash>0)||!XART.rdy('arch_orbital_sweep_0926'))return HMF19.base.orbital.apply(this,arguments);
 const r=HAMMER_STRIKE_REEL[f],k=.70*scale;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(xartTint('arch_orbital_sweep_0926','#ffffff',1),r[0],r[1],r[2],r[3],b.x+(r[0]-r[4])*k,b.y+(r[1]-r[5])*k,r[2]*k,r[3]*k);ctx.restore();return true;
};
cp12Absorb=function(b,q){const r=HMF19.base.absorb.apply(this,arguments);markHit(b,.12);const A=fr27Armor(b);if(A)A.flash=Math.max(A.flash||0,.12);return r;};
hammerBossDamage=function(b,dmg){const dealt=HMF19.base.damage.apply(this,arguments);
 if(dmg>0&&!b.dead&&(!b._hammerTime||b._hammerTime.mode==='attack')&&(!b._hama||b._hama.mode==='attack')){markHit(b,.12);if(hm10WallActive(b)){const A=fr27Armor(b);if(A)A.flash=Math.max(A.flash||0,.12);}}
 return dealt;
};
v19HammerRig=function(b){const p=gd4Create(b,8).p,q=hf19Pick(p);if(!q||!XART.rdy(q.a.key))return HMF19.base.rig.apply(this,arguments);
 const a=q.a,k=q.k,dx=(a.w/2-a.pivot[0])*k,dy=(a.h/2-a.pivot[1])*k;
 return [{p:b.parts.find(p=>p.id==='core'),key:a.key,a,ax:p.x,ay:p.y,x:p.x+dx,y:p.y+dy,w:a.w*k,h:a.h*k,k,rot:0,alpha:1,z:1,_hf19:true,spec:{px:a.pivot[0]/a.w,py:a.pivot[1]/a.h,art:'pose',sheet:a.key,role:'core'}}];
};
v19AtRect=function(v,x,y){if(!v._hf19)return HMF19.base.at.apply(this,arguments);
 const px=Math.floor((x-v.ax)/v.k+v.a.pivot[0]),py=Math.floor((y-v.ay)/v.k+v.a.pivot[1]),m=v18Mask(v.a);
 return !!(m&&px>=0&&py>=0&&px<v.a.w&&py<v.a.h&&m[py*v.a.w+px]>48);
};
v19DonorDraw=function(b){const r=HMF19.base.donor.apply(this,arguments);if(b._r30.v18.form===8){const p=gd4Create(b,8).p;if(hm10WallActive(p))hm10WallDraw(p);}return r;};
// Password choreography keeps its world-wide collision curtain, but uses the
// approved new Chromium wall plates rather than the retired wall recording.
ht27Draw=function(b){const d=b._hammerTime;if(!d?.shield)return HMF19.base.timeDraw.apply(this,arguments);
 const shield=d.shield;d.shield=false;try{HMF19.base.timeDraw.apply(this,arguments);}finally{d.shield=shield;}
 const wall=ht27WallBounds(d),a=HM10_ART.shield_wall[8+Math.floor(d.clock*12)%4];if(!XART.rdy(a.key))return;
 const k=wall.w/a.w;ctx.save();ctx.beginPath();ctx.rect(wall.x,VH*.16,wall.w,wall.h);ctx.clip();ctx.globalAlpha*=.85;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(b.flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key),wall.x,wall.y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
};
window.BOF_HAMMER_FINISH={state:HMF19,pick:hf19Pick,ready:hf19Ready};

// The former idle overlay capped its white flash at 32%, hiding hits on dark steel.
pt11Plate=function(name,f,x,y,k=1,rot=0,flash=0,form=null){
 if(name!=='hammer_core'||!(flash>0))return HMF19.base.corePlate.apply(this,arguments);
 const a=PT11_ART[name]?.[f];if(!a||!XART.rdy(a.key))return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(xartTint(a.key,'#ffffff',1),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;
};

ht27Sprite=function(key,frame,x,footY,height,alpha,flash){
 if(key==='boss'&&boss?._hammerTime&&boss.flash>0){
  const a=HAMMER_TIME_ART.sheets[key],r=a.frames[((frame|0)%a.frames.length+a.frames.length)%a.frames.length],k=height/a.cellHeight;
  if(!XART.rdy('ht27_'+key))return false;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(xartTint('ht27_'+key,'#ffffff',1),r[0],r[1],r[2],r[3],x-r[4]*k,footY-r[5]*k,r[2]*k,r[3]*k);ctx.restore();return true;
 }
 return HMF19.base.timeSprite.apply(this,arguments);
};
