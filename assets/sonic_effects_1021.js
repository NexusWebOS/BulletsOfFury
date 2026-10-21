'use strict';
/* Original sonic artwork only. Native rig, sizes, rotation, clipping, hit flashes,
   projectile collision and warning timing remain with the original renderers. */
const SX21={base:{get:XART.get,tank:razorbackDraw,projectile:razorbackProjectileDraw,
 wave:razorbackWaveDraw,heli:ovSonicProjectileDraw,warning:ovSonicWarningDraw,
 boss:drawBossSprite,bossPass:drawBoss,sweepSafe:ovSweepSafeDraw,rushWarning:ovRushWarningDraw,combatWarning:combatWarningDraw,
 rushStart:ovStartRush,chargeStart:ovStartChargeTell,load:stageLoadBegin,warm:warmStage,cole:sonicDrawFront,coleFx:sonicDraw,shot:eShootT,playerWarm:weaponFeedbackWarm},active:false,cache:new Map(),draws:0,last:null};
const SX21_EDGE_KEYS=['warn_escape_arrow_0916',...['green','yellow','red'].map(c=>'bmfx_alert_'+c+'_impact_imminent')];
for(const a of Object.values(SX21_ART.banks))XART._src[a.key]=a.path;
function sx21EdgeWarm(){for(const k of SX21_EDGE_KEYS)XART.rdy(k);}
function sx21Warm(){for(const a of Object.values(SX21_ART.banks))XART.rdy(a.key);sx21EdgeWarm();}
stageLoadBegin=function(n,keys){return SX21.base.load.call(this,n,n===1?[...(keys||[]),...Object.values(SX21_ART.banks).map(a=>a.key),...SX21_EDGE_KEYS]:keys);};
warmStage=function(n){if(n===1)sx21Warm();return SX21.base.warm.apply(this,arguments);};
function sx21Frame(bank,time=efxClock){
 const a=SX21_ART.banks[bank];if(!a||!XART.rdy(a.key))return null;
 const f=Math.floor(Math.max(0,time)*a.fps)%a.frames,id=bank+':'+f;if(SX21.cache.has(id))return SX21.cache.get(id);
 const c=document.createElement('canvas');c.width=a.w;c.height=a.h;
 c.naturalWidth=a.w;c.naturalHeight=a.h;c.complete=true;
 const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 g.drawImage(SX21.base.get(a.key),...a.cells[f],0,0,a.w,a.h);
 c._so21={bank,frame:f,key:a.key,sourceKey:a.sourceKey};SX21.cache.set(id,c);return c;
}
function sx21Scoped(fn,self,args){const old=SX21.active;SX21.active=true;try{return fn.apply(self,args);}finally{SX21.active=old;}}
XART.get=function(key){
 const m=SX21.active&&/^(rzb|rzbf)_sonic_(bullet|wave|ring|charge)$/.exec(key);
 if(m){const bank=m[2]+'_'+(m[1]==='rzbf'?'red':'green'),im=sx21Frame(bank);
  if(im){SX21.draws++;SX21.last=im._so21;return im;}}
 return SX21.base.get.apply(this,arguments);
};
razorbackDraw=function(){return sx21Scoped(SX21.base.tank,this,arguments);};
razorbackWaveDraw=function(){return sx21Scoped(SX21.base.wave,this,arguments);};
razorbackProjectileDraw=function(){return sx21Scoped(SX21.base.projectile,this,arguments);};
function sx21TargetPulseGeometry(q){
 const red=q._target17RazorFurious??!!q._target17Owner?._rzb?.furious;
 const age=q._target17Age||0,size=(red?168:112)*(.70+.30*clamp(age/.65,0,1));
 return{red,bank:'pulse_'+(red?'red':'green'),size,angle:Math.atan2(q.vy,q.vx)+Math.PI/2};
}
function sx21TargetPulseDraw(q){
 const g=sx21TargetPulseGeometry(q),im=sx21Frame(g.bank,q._target17Age||0);if(!im)return true;
 ctx.save();ctx.translate(q.x,q.y);ctx.rotate(g.angle);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-g.size/2,-g.size/2,g.size,g.size);ctx.restore();return true;
}
function sx21PressureGeometry(q){
 const p=clamp((q.t||0)/.65,0,1),size=48+40*p;
 return{size,angle:Math.atan2(q.vy,q.vx)+Math.PI/2};
}
function sx21PressureDraw(q){
 const g=sx21PressureGeometry(q),im=sx21Frame('wave_red',q.t||0);
 if(!im)return false;
 ctx.save();ctx.translate(q.x,q.y);ctx.rotate(g.angle);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-g.size/2,-g.size/2,g.size,g.size);ctx.restore();return true;
}
// Modular sonic turrets used the generic gold orb fallback because they did
// not carry the Razorback-only owner flag. Give that pressure shot its own path.
eShootT=function(x,y,ang,spd,kind,opts){const q=SX21.base.shot.apply(this,arguments);
 if(q&&kind==='rzbSonic'){q._sx21Pressure=true;q.w=36;q.h=28;}return q;};
ovSonicProjectileDraw=function(q){
 if(q.kind==='rzbSonic'&&!q._rzb)return sx21PressureDraw(q);
 return sx21Scoped(SX21.base.heli,this,arguments);};
function sx21HeliCharge(b,progress){
 const m=ovFacingMount(b,0,60),size=42+progress*62;
 // The helicopter originally shared the green Razorback sonic plates.
 // Keep that exact source and a single original charge graphic at its mount.
 return sx21Scoped(weaponFeedbackArt,null,['rzb_sonic_charge',m.x,m.y,size,size,.55+progress*.45,0,true]);
}
ovSonicWarningDraw=function(b){const r=SX21.base.warning.apply(this,arguments),s=b._ovSonic;
 if(s?.phase==='waveTell')sx21HeliCharge(b,clamp(s.t/2.1,0,1));return r;};
// Mike rejected the mint rectangle painted over the player during strafing.
// The sweep's actual safe gap, bullets and authored attack warnings stay native.
ovSweepSafeDraw=function(b){if(b?.kind==='damkeeper')return;
 return SX21.base.sweepSafe.apply(this,arguments);};
ovStartRush=function(){sx21EdgeWarm();return SX21.base.rushStart.apply(this,arguments);};
ovStartChargeTell=function(){sx21EdgeWarm();return SX21.base.chargeStart.apply(this,arguments);};
function sx21EntryGeometry(lane,dir){
 const z=viewZoom(),north=dir>0,x=clamp(lane,camLeftX()+26/z,camRightX()-26/z);
 const y=north?viewTopY()+(PLAY.y+42)/z:viewTopY()+(VH-36)/z;
 return{x,y,north,z,rotation:north?Math.PI/2:-Math.PI/2};
}
function sx21EntryDraw(b,lane,dir,progress,time){
 const g=sx21EntryGeometry(lane,dir),p=clamp(progress,0,.999),color=l23FovPhase(p),key='bmfx_alert_'+color+'_impact_imminent';
 const pulse=.40+.60*(.5+.5*Math.cos((time||0)*TAU*(3+p*3)));
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=pulse;
 if(XART.rdy(key)){const im=XART.get(key),s=34/g.z;ctx.drawImage(im,g.x-s/2,g.y-s/2,s,s);}
 if(XART.rdy('warn_escape_arrow_0916')){const im=XART.get('warn_escape_arrow_0916'),w=34/g.z,h=w*im.height/im.width;
  for(const d of [30,58]){ctx.save();ctx.translate(g.x,g.y+(g.north?d:-d)/g.z);ctx.rotate(g.rotation);ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();}}
 ctx.restore();SX21.edgeLast={...g,key,progress:p,alpha:pulse,lane,dir};
}
ovRushWarningDraw=function(b,alertOnly){
 const R=b?._ovRush;if(SX21.entryDeferred||!R||!alertOnly||!['choose','lock','fade','charge'].includes(R.phase))return;
 const index=R.phase==='choose'?(R.active??R.index):R.index,lane=R.lanes[index];if(!Number.isFinite(lane))return;
 const progress=R.phase==='choose'?.30+.32*clamp(R.t/(ovHardBoss()?.62:.75),0,1):.999;
 sx21EntryDraw(b,lane,R.dir,progress,b.t||R.t);
};
combatWarningDraw=function(owner,q){
 if(owner?.kind==='damkeeper'&&owner._ovState==='chargeTell'&&owner._chargeTell){
  if(!SX21.entryDeferred&&!q?.fieldOnly){const T=owner._chargeTell;sx21EntryDraw(owner,T.lane,T.dir||1,q.progress,owner.t||T.t);}return;}
 return SX21.base.combatWarning.apply(this,arguments);
};
drawBoss=function(){
 const b=boss,entry=b?.kind==='damkeeper'&&!b.dead,old=SX21.entryDeferred;let r;
 try{if(entry)SX21.entryDeferred=true;r=SX21.base.bossPass.apply(this,arguments);}
 finally{SX21.entryDeferred=old;}
 // An incoming warning belongs to the screen edge even while its hull is
 // offscreen or omitted by a flight/intro renderer.
 if(entry){if(b._ovRush)ovRushWarningDraw(b,true);
  else if(b._ovState==='chargeTell'&&b._chargeTell){const T=b._chargeTell;sx21EntryDraw(b,T.lane,T.dir||1,ovChargeWarningProgress(T),b.t||T.t);}}
 return r;
};
drawBossSprite=function(b){const r=SX21.base.boss.apply(this,arguments);
 if(b?.kind==='damkeeper'&&!b.dead&&!b._ovSonic&&b._ovState==='chargeTell'&&b._chargeTell)
  sx21HeliCharge(b,ovChargeWarningProgress(b._chargeTell));return r;};
weaponFeedbackWarm=function(pilot){const r=SX21.base.playerWarm.apply(this,arguments);if(pilot==='cole')sx21Warm();return r;};
sonicDrawFront=function(b){
 const im=sx21Frame('wave_green',b.t||0);if(!im)return SX21.base.cole.apply(this,arguments);
 const g=sonicFrontGeometry(b),p=clamp(b._p||0,0,1),size=g.w*1.9*(1+.06*Math.sin((b.t||0)*40));
 // Shared helicopter front, flipped toward Cole's upward travel and fitted
 // to his existing wave width. One proportional scale keeps its arc intact.
 ctx.save();ctx.translate(b.x,b.y-2);ctx.globalCompositeOperation='lighter';
 ctx.globalAlpha=.62+.30*p;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-size/2,-size/2,size,size);ctx.restore();
};
sonicDraw=function(){
 const trails=sonicTrail,echoes=trails.filter(s=>!s.imp&&!s.circ&&!s.boom);let r;
 // Keep native charging, impact and release rings; replace the old gold wake.
 try{sonicTrail=trails.filter(s=>s.imp||s.circ||s.boom);r=SX21.base.coleFx.apply(this,arguments);}
 finally{sonicTrail=trails;}
 for(const s of echoes){const u=clamp(s.t/s.dur,0,1),im=sx21Frame('wave_green',s.t);
  if(!im)continue;const size=(s.w||48)*1.9*(1+u*.22);
  ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.14*(1-u)*(1-u);
  ctx.imageSmoothingEnabled=false;ctx.drawImage(im,s.x-size/2,s.y-size/2,size,size);ctx.restore();}
 return r;
};
window.BOF_SONIC_EFFECTS=SX21;
