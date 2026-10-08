'use strict';
/* Scene-boundary memory ownership. No polling or eviction during a live fight. */
const BOF_MEMORY={stage:0,released:0,transitions:0,history:[]};
function bofDerivedCachesRetire(){
 // These caches hold decoded-stage canvases after XART releases the source image.
 // Rebuild lazily for the new mission; shared ship/portrait animations stay warm.
 const caches=[_emisCache,_rampCache,_mwGlowCache,_mfxtc,_palCache,_nuoCache,
  _stage7TerrainCache,_landMasks,_terrMasks,_btmCache,_opnSil,_lateSpriteCache,
  CFX_FLIGHT_LIGHT,hammerTintCache,archTintCache,hammerStormPaletteCache,hammerChromiumCache];
 for(const cache of caches){if(cache instanceof Map)cache.clear();else for(const k in cache)delete cache[k];}
 if(typeof ROT5!=='undefined'){ROT5.cache.clear();ROT5.bytes=0;}
}
function bofMemoryBegin(stage,keys){
 if(!stage||BOF_MEMORY.stage===stage)return;
 const previous=BOF_MEMORY.stage,current='levels/stage_'+String(stage).padStart(2,'0');
 // Protect dependencies explicitly queued by the next encounter, even when a
 // final copied form uses a texture owned by an earlier campaign stage.
 const keep=new Set((keys||[]).map(k=>bofAssetPath(XART._src[k])));
 const old='levels/stage_'+String(previous).padStart(2,'0');let count=0;
 for(const key of Object.keys(XART.img)){
  const src=XART._src[key];if(!src||keep.has(bofAssetPath(src)))continue;
  if(previous&&bofAssetOwner(src)===old){XART.releaseRoot(key);count++;}
 }
 if(previous)bofDerivedCachesRetire();
 BOF_MEMORY.stage=stage;BOF_MEMORY.released+=count;BOF_MEMORY.transitions++;
 BOF_MEMORY.history.push({stage,previous,released:count});if(BOF_MEMORY.history.length>16)BOF_MEMORY.history.shift();
}
const BOF_MEMORY_STAGE_BEGIN=stageLoadBegin;
stageLoadBegin=function(n,keys){const count=BOF_MEMORY_STAGE_BEGIN.apply(this,arguments);bofMemoryBegin(n,_stageLoads[n]?.keys||[]);return count;};
window.BOF_MEMORY=BOF_MEMORY;
