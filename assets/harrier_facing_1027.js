'use strict';
/* The hull's stowed guns face south before the live modular guns take over. */
const HF28={base:{get:XART.get,opening:s6OpeningDraw,tick:warhiveTick,load:stageLoadBegin},northPass:false,handovers:0,last:null};
const HF28_KEYS={whv_closed:'closed',whv_open:'open',whv_broken:'broken',whv_closed_w:'closed_wells',whv_open_w:'open_wells',whv_broken_w:'broken_wells'};
for(const a of Object.values(HF28_ART))XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return HF28.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(HF28_ART).map(a=>a.key)]:keys);};
XART.get=function(key){if(run.stage===6){let name=HF28_KEYS[key];
 if(name){const direction=HF28.northPass&&!name.endsWith('wells')?'north':'south',a=HF28_ART[name+'_'+direction];if(a&&XART.rdy(a.key)){HF28.last={key,art:a.key,screenFacing:'south',opening:HF28.northPass};return HF28.base.get.call(this,a.key);}}
 const m=/^hh21_gun_([0-3])$/.exec(String(key));if(m){const a=HF28_ART['hit_'+m[1]];if(XART.rdy(a.key))return HF28.base.get.call(this,a.key);}
 }return HF28.base.get.apply(this,arguments);};
s6OpeningDraw=function(){const old=HF28.northPass;HF28.northPass=run.stage===6&&s6Opening?.phase==='flyover';try{return HF28.base.opening.apply(this,arguments);}finally{HF28.northPass=old;}};
warhiveTick=function(b,dt){const C=b?._carrier17,wasDepth=!!C&&(C.depth||C.phase==='arrive'||C.phase==='flyover'),out=HF28.base.tick.apply(this,arguments);
 if(run.stage===6&&C===b._carrier17&&wasDepth&&!C.depth&&C.phase==='fight'){
  for(const p of C.parts)if(p.kind==='gun'&&!p.dead){p.angle=p.er28Bearing=p.muzzleAngle=Math.PI/2;p.muzzleAge=99;}HF28.handovers++;
 }return out;};
globalThis.BOF_HARRIER_FACING_1027=HF28;
