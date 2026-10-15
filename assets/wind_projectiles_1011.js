"use strict";
/* Wind's nine native carriers own distinct generated reels; simulation stays with each weapon. */
const WP11={base:{bullets:drawBullets,flame:flameDraw,load:stageLoadBegin},draws:{},fallbacks:0};
const WP11_KEYS=WP11_FAMILIES.flatMap(f=>AP10_FX_ART['wind_'+f]||[]);
for(const a of WP11_KEYS)XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return WP11.base.load.call(this,n,[...(keys||[]),...WP11_KEYS.map(a=>a.key)]);};
function wp11Resolve(key){return XART.rdy(key)?XART.get(key):null;}
function wp11Ready(family){const bank=AP10_FX_ART['wind_'+family]||[];return bank.map(a=>XART.rdy(a.key)).some(Boolean);}
function wp11Draw(b){const f=wp11Family(b);if(!f)return false;
 const n=wp11Paint(ctx,AP10_FX_ART['wind_'+f],wp11Resolve,b,efxClock);
 if(n)WP11.draws[f]=(WP11.draws[f]||0)+n;return !!n;
}
drawBullets=function(){
 const all=pBullets,owned=new Set(all.filter(b=>!b.dead&&!(b._launchDelay>0)&&wp11Family(b)&&wp11Ready(wp11Family(b))));
 pBullets=all.filter(b=>!owned.has(b));
 try{WP11.base.bullets.apply(this,arguments);}finally{pBullets=all;}
 for(const b of owned)wp11Draw(b);
};
flameDraw=function(f){if(wp11Family(f)==='gust'&&wp11Draw(f))return;return WP11.base.flame.apply(this,arguments);};
