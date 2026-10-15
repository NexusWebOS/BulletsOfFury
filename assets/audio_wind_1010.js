"use strict";
/* Stage 6 grants Wind. Preserve earned Prism recipes when an older save opens. */
const AP10_W={base:{forms:ensureForgeForms,apply:forgeApply,entry:forgeEntry,
 discover:forgeDiscover,grant:infusionGrant,hit:infusionOnHit,burst:efxBurst,drawFx:efxDraw,
 bullets:drawBullets,flame:flameDraw,aura:infusionAuraDraw,pickup:pickupTurnFrame,
 play:updatePlay,load:stageLoadBegin,combine:forgeCombine,select:forgeSelect,grantCombo:forgeComboGrant},draws:0,migrations:0};
for(const a of AP10_FX_ART.wind_icons||[]){
 XART._src[a.key]=a.path;
 const w=a.slot,l=a.level;
 XART._src['micon_forge_wind_'+w+(l>1?'_'+l:'')]=a.path;
}
XART._src.inf_wind=AP10_FX_ART.wind_symbol[0].path;
XART._src.turn_inf_wind_0918=AP10_FX_ART.wind_symbol[0].path;
function ap10WindMigrate(r=run){
 if(!r)return;
 let changed=false;
 if(r.forgeElems?.prism){r.forgeElems.wind=1;changed=true;delete r.forgeElems.prism;}
 for(const f of Object.values(r.forge||{}))if(f?.elem==='prism'){f.elem='wind';changed=true;}
 for(const F of Object.values(r.forgeForms||{}))if(F?.prism){
  const f=F.prism;F.wind={...f,...F.wind,elem:'wind',lv:Math.max(f.lv||1,F.wind?.lv||1)};
  delete F.prism;changed=true;
 }
 if(r.infusion?.elem==='prism'){r.infusion.elem='wind';changed=true;}
 if(changed)AP10_W.migrations++;
 // Keep the original profile keys as historical receipts; copy entitlement.
 for(const [id,value] of Object.entries(achievementState.owned||{}))if(/^forge_(prism_[0-8]_C|element_prism_E)$/.test(id)){
  const fresh=id.replace('prism','wind');if(!achievementState.owned[fresh])achievementState.owned[fresh]=value;
 }
}
ensureForgeForms=function(){ap10WindMigrate();return AP10_W.base.forms.apply(this,arguments);};
forgeApply=function(){ap10WindMigrate();return AP10_W.base.apply.apply(this,arguments);};
forgeEntry=function(){ap10WindMigrate();return AP10_W.base.entry.apply(this,arguments);};
forgeDiscover=function(elem){return AP10_W.base.discover.call(this,elem==='prism'?'wind':elem);};
infusionGrant=function(elem){return AP10_W.base.grant.call(this,elem==='prism'?'wind':elem);};
forgeComboGrant=function(elem,w){ap10WindMigrate();return AP10_W.base.grantCombo.call(this,elem==='prism'?'wind':elem,w);};
forgeCombine=function(w,elem){ap10WindMigrate();return AP10_W.base.combine.call(this,w,elem==='prism'?'wind':elem);};
forgeSelect=function(w,elem){ap10WindMigrate();return AP10_W.base.select.call(this,w,elem==='prism'?'wind':elem);};
function ap10WindWarm(){for(const a of [...(AP10_FX_ART.wind||[]),...(AP10_FX_ART.wind_icons||[]),...(AP10_FX_ART.wind_symbol||[])])XART.rdy(a.key);}
stageLoadBegin=function(n,keys){return AP10_W.base.load.call(this,n,[...(keys||[]),...(AP10_FX_ART.wind||[]).map(a=>a.key),...(AP10_FX_ART.wind_icons||[]).map(a=>a.key),...(AP10_FX_ART.wind_symbol||[]).map(a=>a.key)]);};
function ap10WindCell(i,x,y,size,angle=0,g=ctx){
 const a=AP10_FX_ART.wind?.[i];if(!a||!XART.rdy(a.key))return false;
 const k=size/a.w;g.save();g.translate(x,y);g.rotate(angle);g.imageSmoothingEnabled=false;
 g.drawImage(XART.get(a.key),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);g.restore();AP10_W.draws++;return true;
}
function ap10WindPush(e,b,lv=1){
 if(!e||e.dead||e._dyingT!=null)return;
 if(isSetPiece(e)||e===boss||e===subBoss)return; // Whole encounter plates keep their mounting geometry.
 if(efxClock-(e._ap10GustAt??-9)<.16)return;e._ap10GustAt=efxClock;
 const a=Math.atan2(b.vy||-1,b.vx||0),strength=65+Math.min(5,lv)*12;
 e._ap10Gust={t:.28,vx:Math.cos(a)*strength,vy:Math.sin(a)*strength};
 e._windSlow=Math.max(e._windSlow||0,.45);e.fireCd=Math.max(e.fireCd||0,.26);
}
infusionOnHit=function(e,b,dmg){const r=AP10_W.base.hit.apply(this,arguments);
 if(b?._inf==='wind')ap10WindPush(e,b,b._infLv||run.infusion?.lv||1);return r;};
efxBurst=function(elem,x,y,size){if(elem!=='wind')return AP10_W.base.burst.apply(this,arguments);
 if(efxBursts.length>=EFX_BURST_CAP)efxBursts.shift();const b={elem,x,y,t:0,s:size||48};efxBursts.push(b);
 Audio.SFX.cfComboKinetic?.();ap10WindWarm();return b;};
efxDraw=function(){const all=efxBursts,wind=all.filter(b=>b.elem==='wind');
 efxBursts=all.filter(b=>b.elem!=='wind');try{AP10_W.base.drawFx.apply(this,arguments);}finally{efxBursts=all;}
 for(const b of wind)ap10WindCell(12+Math.min(3,Math.floor(b.t/EFX_BURST_T*4)),b.x,b.y,b.s);
 for(const e of enemies)if(e._ap10Gust)ap10WindCell(8+Math.floor(efxClock*20)%4,e.x,e.y,Math.max(e.w,e.h)*1.6);
};
infusionAuraDraw=function(b){if(b._inf==='wind')return;return AP10_W.base.aura.apply(this,arguments);};
function ap10WindRoundDraw(b){
 if(b.dead||b._launchDelay>0||b._inf!=='wind'&&b._el!=='wind')return false;
 const t=b.t||b._bt||efxClock;
 if(b.kind==='orb'||b.kind==='yuriLightningOrb')return ap10WindCell(8+Math.floor(t*20)%4,b.x,b.y,Math.max(b.w||32,b.h||32)*2);
 if(b.kind==='beam'){
  const top=b.top??(b.y-b.h),bottom=b.bot??b.y,length=Math.max(0,bottom-top),width=b.w||22;
  if(length>0)for(let y=bottom;y>top;y-=width*2.2){const len=Math.min(width*2.2,y-top);
   ctx.save();ctx.beginPath();ctx.rect(b.x-width*1.25,y-len,width*2.5,len);ctx.clip();ap10WindCell(4+Math.floor(t*20)%4,b.x,y,width*2.5);ctx.restore();}
  ap10WindCell(Math.min(3,Math.floor((b._bt||0)*16)),b.x,bottom,width*2.5);return true;
 }
 if(b.kind==='shard')return ap10WindCell(4+Math.floor(t*20)%4,b.x,b.y,22,Math.atan2(b.vy,b.vx)+Math.PI/2);
 return false;
}
drawBullets=function(){
 const all=pBullets,owned=all.filter(b=>['orb','yuriLightningOrb','beam','shard'].includes(b.kind)&&(b._inf==='wind'||b._el==='wind'));
 const ready=(AP10_FX_ART.wind||[]).length===16&&(AP10_FX_ART.wind||[]).every(a=>XART.rdy(a.key));
 if(!ready)return AP10_W.base.bullets.apply(this,arguments);
 pBullets=all.filter(b=>!owned.includes(b));try{AP10_W.base.bullets.apply(this,arguments);}finally{pBullets=all;}
 for(const b of owned)ap10WindRoundDraw(b);
 for(const b of all)if(!b.dead&&b._inf==='wind'&&!owned.includes(b)&&!['flame','mist'].includes(b.kind))
  ap10WindCell(4+Math.floor((b.t||0)*20)%4,b.x,b.y+8,Math.min(32,Math.max(b.w||8,b.h||16)),Math.atan2(b.vy||-1,b.vx||0)+Math.PI/2);
};
flameDraw=function(f){if(f._inf!=='wind'||!AP10_FX_ART.wind?.length||!AP10_FX_ART.wind.every(a=>XART.rdy(a.key)))return AP10_W.base.flame.apply(this,arguments);
 const length=f.bot-f.top,width=Math.max(34,f.w||34);
 for(let y=f.bot;y>f.top;y-=width*.7){ctx.save();ctx.beginPath();ctx.rect(f.x-width,y-Math.min(width*.7,y-f.top),width*2,Math.min(width*.7,y-f.top));ctx.clip();
  ap10WindCell(4+Math.floor((f._bt||efxClock)*20)%4,f.x,y,width*1.8);ctx.restore();}
 ap10WindCell(3,f.x,f.bot,width*1.8);};
pickupTurnFrame=function(key,x,y,size,t){if(key!=='turn_inf_wind_0918')return AP10_W.base.pickup.apply(this,arguments);
 const a=AP10_FX_ART.wind_symbol?.[0];if(!a||!XART.rdy(a.key))return false;
 ctx.drawImage(XART.get(a.key),x-size/2,y-size/2,size,size);return true;};
updatePlay=function(dt){ap10WindMigrate();const r=AP10_W.base.play.apply(this,arguments);
 if(state===GS.PLAY)for(const e of enemies){const q=e._ap10Gust;if(!q||e.dead)continue;
  const k=clamp(q.t/.28,0,1);if(!e._ground){e.x=clamp(e.x+q.vx*dt*k,camLeftX()+e.w*.5,camRightX()-e.w*.5);e.y+=q.vy*dt*k;}
  q.t-=dt;if(q.t<=0)e._ap10Gust=null;
 }
 return r;};
ap10WindMigrate();
