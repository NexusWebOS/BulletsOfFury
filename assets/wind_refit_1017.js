"use strict";
/* Compact physical ammunition; one full authored frame per wind laser.
   The live combat painter reads the new authored banks directly. */
const WIND17={base:wp11Paint,draws:0,laserDraws:0};
for(const [family,name] of Object.entries({bullets:'windBullets',spread:'windSpread',heavy:'windHeavy',laser:'windLaser'})){
 const a=A17_ART[name],slot=WP11_FAMILIES.indexOf(family);
 AP10_FX_ART['wind_'+family]=Array.from({length:a.n},(_,f)=>({...a,slot,_a17:true,frame:f,fps:18,body_height:a.span,
  sx:(f%a.cols)*a.w,sy:Math.floor(f/a.cols)*a.h}));
}
WP11_KEYS.splice(0,WP11_KEYS.length,...new Map(WP11_FAMILIES.flatMap(f=>AP10_FX_ART['wind_'+f]||[]).map(a=>[a.key,a])).values());
wp11Paint=function(g,bank,resolve,b,clock=0){
 if(!bank?.[0]?._a17){
  const family=WP11_FAMILIES[bank?.[0]?.slot];
  if(!b||!family)return WIND17.base.apply(this,arguments);
  if(family==='gust')return WIND17.base(g,bank,resolve,{...b,w:(b.w||18)*.62},clock);
  if(['missile','mist','tornado','electric'].includes(family)){
   g.save();g.translate(b.x,b.y);g.scale(.60,.60);
   try{return WIND17.base(g,bank,resolve,{...b,x:0,y:0},clock);}finally{g.restore();}
  }return WIND17.base.apply(this,arguments);
 }
 if(!b||b.dead||b._launchDelay>0||!Number.isFinite(b.x))return 0;
 const family=WP11_FAMILIES[bank[0].slot],held=family==='laser',q=wp11Frame(bank,resolve,held?clock:(b.t??b._bt??clock));if(!q)return 0;
 const {a,im}=q,lv=clamp(b._infLv||b.lv||1,1,5);g.save();g.imageSmoothingEnabled=false;g.shadowBlur=0;
 if(held){
  const top=b.top??b.y-(b.h||0),bot=b.bot??b.y,length=bot-top;if(!Number.isFinite(length)||length<=0){g.restore();return 0;}
  const k=length/(a.pivot[1]-a.bounds[1]),width=Math.max(12,(b.w||12)*1.55);
  g.beginPath();g.rect(b.x-width,top,width*2,length+12);g.clip();
  // A single proportional draw contains tip, flowing body and muzzle. No
  // repeated body rectangle or tiled texture can form a seam down the shaft.
  g.drawImage(im,a.sx,a.sy,a.w,a.h,b.x-a.pivot[0]*k,bot-a.pivot[1]*k,a.w*k,a.h*k);WIND17.laserDraws++;
 }else{
  const size=({bullets:12+lv,spread:10+lv*.8,heavy:16+lv})[family],k=size/a.span;
  const angle=Math.atan2(b.vy||-1,b.vx||0)+Math.PI/2;
  g.translate(b.x,b.y);g.rotate(angle);g.drawImage(im,a.sx,a.sy,a.w,a.h,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);
 }
 g.restore();WIND17.draws++;return 1;
};
window.BOF_WIND_REFIT={state:WIND17};
