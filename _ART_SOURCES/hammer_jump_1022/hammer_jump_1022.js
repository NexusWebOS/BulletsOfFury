"use strict";
/* Fixed authored frame units. New motion, light and hit feedback use stored
   pixels; native attacks own targets, evasions, HP, hazards and audio. */
const HJ22={base:{blue:ha21Blue,pose:hb20Pose,landing:ha21Landing,paint:b20Image,flash:ha21Flash,load:stageLoadBegin,keys:v18Keys,warm:v18Warm,tick:hammerBossTick,draw:hammerBossDraw,recovery:hammerRecoverDuration,start:hb20Start,native:v19NativeTick,donor:v19DonorDraw},draws:{},glowDraws:0,events:[]};
for(const s of Object.values(HJ22_ART.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(HJ22_ART.banks))for(const a of rows){BOFX.cells[a.key]=[a.sheet,...a.cell];if(a.white)BOFX.cells[a.white]=[a.sheet+'_hit',...a.cell];}
function hj22Keys(n){return Object.entries(HJ22_ART.sheets).filter(([id])=>id.includes(n===5?'blue':'corrupt')||id.includes('warning_')).map(([,s])=>s.key);}
stageLoadBegin=function(n,keys){if([5,8].includes(n))Snd.prepare(['hammerImpact','hammerLeap','bossWeaponCharge']);return HJ22.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?hj22Keys(n):[])]);};
v18Keys=function(){return [...HJ22.base.keys(),...hj22Keys(8)];};
v18Warm=function(){const old=HJ22.base.warm();return hj22Keys(8).map(k=>XART.rdy(k)).every(Boolean)&&old;};
function hj22Frame(name,f){const rows=HJ22_ART.banks[name];return rows?.[Math.min(rows.length-1,Math.max(0,Math.floor(f)))];}
function hj22Pose(kind,f,b){let name=kind;if(kind==='blue_jump'&&fr27Armor(b)?.activated&&fr27Armor(b).hp>0&&HJ22_ART.banks.blue_jump_armor)name+='_armor';const a=hj22Frame(name,f);if(!a||!XART.rdy(a.key)||!XART.rdy(a.white))return null;HJ22.draws[name]=(HJ22.draws[name]||0)+1;return{a,k:1,rot:0,kind:name};}
function hj22Light(kind,at){const rows=HJ22_ART.banks[kind+'_glow'];if(!rows?.length)return;const a=rows[Math.floor(efxClock*12)%rows.length];if(!XART.rdy(a.key))return;ctx.drawImage(XART.get(a.key),Math.round(at.x-a.pivot[0]),Math.round(at.y-a.pivot[1]));HJ22.glowDraws++;}
function hj22Point(a,p,x,y,k=1,rot=0,pivot=a.pivot){const dx=(p[0]-pivot[0])*k,dy=(p[1]-pivot[1])*k;return{x:x+dx*Math.cos(rot)-dy*Math.sin(rot),y:y+dx*Math.sin(rot)+dy*Math.cos(rot)};}
function hj22Cell(a,x,y,flash=0,pivot=a.pivot){const key=flash>0&&a.white?a.white:a.key;if(!XART.rdy(key))return false;const old=ctx.imageSmoothingEnabled;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),Math.round(x-pivot[0]),Math.round(y-pivot[1]));ctx.imageSmoothingEnabled=old;return true;}
b20Image=function(a,x,y,k=1,rot=0,flash=0,pivot=a?.pivot){
 if(a?._hj22){hj22Light(a.kind,hj22Point(a,a.glow,x,y,1,0,pivot));return hj22Cell(a,x,y,flash,pivot);}
 const socket=a&&HJ22_ART.legacyGlow[a.key],owner=HA21.painting;
 if(socket&&(!owner||ha21Blue(owner)?.a===a)){
  const kind=/blue/.test(a.key)?'blue':'corrupt',B=boss,Q=kind==='corrupt'&&hb20Own(B)?hb20State(B):null;
  const detached=/tool/.test(a.key),empty=!detached&&(kind==='blue'?B?._hammer?.hammerDestroyed||B?._hammer?.throw:Q?.broken||Q?.rage||Q?.action?.type==='throw'&&Q.action.t>=Q.action.tell);
  if(!empty)hj22Light(kind,hj22Point(a,socket,x,y,k,rot,pivot));
 }
 return HJ22.base.paint.apply(this,arguments);
};
ha21Flash=function(b,q){if(q?.a?._hj22)return hj22Cell(q.a,b.x,b.y,Math.max(b.flash||0,b._lastPart?.flash||0));return HJ22.base.flash.apply(this,arguments);};
function hj22Phase(kind,clock,phase){const M=HJ22_ART.phases[kind],rows=HJ22_ART.banks[kind+'_jump'];if(phase==='wind')return lerp(0,M.windEnd,clamp(clock,0,1));if(phase==='strike')return lerp(M.windEnd,M.strikeEnd,clamp(clock,0,1));return lerp(M.strikeEnd,rows.length-1,clamp(clock,0,1));}
function hj22PairFrame(P,kind){const t=P.clock;
 // Hama's two-contact cadence, performed by each boss's current authored
 // body. Avoid swapping to the older Hama body in the middle of a combo.
 const M=HJ22_ART.phases[kind];
 return{bank:kind+'_jump',f:t<.12?M.strikeEnd:t<.85?hj22Phase(kind,(t-.12)/.73,'wind'):t<1.2?hj22Phase(kind,(t-.85)/.35,'strike'):hj22Phase(kind,(t-1.2)/.5,'recover')};
}
ha21Blue=function(b){const h=b?._hammer;if(b?._hammerTime?.hama)return null;if(!h||b.dead||b._gp4Host)return HJ22.base.blue.apply(this,arguments);const music=b._hammerTime||b._hama;if(music&&music.mode!=='attack'||hf19Recovery(b)&&h.state!=='recover')return HJ22.base.blue.apply(this,arguments);
 if(h._hj22Pair&&h.state==='recover'){const p=hj22PairFrame(h._hj22Pair,'blue');return hj22Pose(p.bank,p.f,b)||HJ22.base.blue.apply(this,arguments);}
 const s=h.state,t=h.t||0;let f=null;
 if(s==='warn')f=hj22Phase('blue',t/(hammerFurious()?.58:1.2),'wind');
 else if(s==='leap')f=hj22Phase('blue',Math.max(0,t/(hammerFurious()?.27:.52)-.12)/.88,'strike');
 else if(s==='recover')f=hj22Phase('blue',t/HJ22.base.recovery(),'recover');
 else if(s==='storm_warn')f=hj22Phase('blue',t/(hammerFurious()?.9:hammerHard()?1:1.15),'wind');
 else if(s==='storm_slam')f=hj22Phase('blue',t/(hammerFurious()?.46:hammerHard()?.52:.6),'strike');
 else if(s==='storm_split')f=hj22Phase('blue',t/.75,'recover');
 return f==null?HJ22.base.blue.apply(this,arguments):hj22Pose('blue_jump',f,b)||HJ22.base.blue.apply(this,arguments);
};
ha21Landing=function(b,target,kind,frame,scale){if(b._gp4Host||b._hammer?.state?.startsWith('giant_')||!['slam','jump'].includes(kind))return HJ22.base.landing.apply(this,arguments);const a=hj22Frame('blue_jump',HJ22_ART.phases.blue.strikeEnd);return{x:target.x-(a.tip[0]-a.pivot[0]),y:target.y-(a.tip[1]-a.pivot[1])};};
hb20Pose=function(b){if(hb20Own(b)){const Q=hb20State(b),A=Q?.action;if(A?.type==='skystrike'){
  if(A._hj22Pair&&A.t>=A._hj22Pair.start){const P=A._hj22Pair;P.clock=A.t-P.start;const f=hj22PairFrame(P,'corrupt');return hj22Pose(f.bank,f.f,b)||HJ22.base.pose.apply(this,arguments);}
  const u=A.t-A.tell,f=u<0?hj22Phase('corrupt',A.t/.6,'wind'):u<.9?hj22Phase('corrupt',Math.max(0,u-.1)/.5,'strike'):hj22Phase('corrupt',(u-.9)/.4,'recover');return hj22Pose('corrupt_jump',f,b)||HJ22.base.pose.apply(this,arguments);
 }}return HJ22.base.pose.apply(this,arguments);};
function hj22Pair(b,kind,target){return{clock:0,target:{...target},origin:{x:b.x,y:b.y},kind,hit:new Set(),impact:false};}
function hj22Warn(b,P){if(P.clock<=1.2){const u=clamp(P.clock/.85,0,1);combatWarningTick(P,'hammer-double-swing',Math.min(P.clock,.85),.85);return u;}return 1;}
function hj22PairTick(b,P){
 const a=hj22Frame(P.kind+'_jump',HJ22_ART.phases[P.kind].strikeEnd),end={x:P.target.x-(a.tip[0]-a.pivot[0]),y:P.target.y-(a.tip[1]-a.pivot[1])},u=clamp(P.clock/1.2,0,1);
 b.x=lerp(P.origin.x,end.x,u);b.y=lerp(P.origin.y,end.y,u)-Math.sin(u*Math.PI)*(P.kind==='blue'?70:110);b._drawY=b.y;hj22Warn(b,P);
 if(P.clock>=1.2&&!P.impact){P.impact=true;b20HitSegment(b,P.target,P.target,P.kind==='blue'?62:46,'Hammer double slam',P.hit);if(P.kind==='corrupt')hb20Wave(b,hb20State(b),P.target);explode(P.target.x,P.target.y,70,P.kind==='blue'?'blue':'purple');shake=Math.max(shake,10);b20Cue('hammerImpact');HJ22.events.push({type:'second-impact',kind:P.kind,x:P.target.x,y:P.target.y});}
}
function hj22PairDraw(b,P){if(b.dead||P.clock>=1.2)return;const u=clamp(P.clock/.85,0,1),f=u<1/3?0:u<2/3?1:2;for(const name of ['warning_cone','warning_reticle']){const a=hj22Frame(name,f);if(a&&XART.rdy(a.key))ctx.drawImage(XART.get(a.key),Math.round(P.target.x-a.pivot[0]),Math.round(P.target.y-a.pivot[1]));}}
hammerRecoverDuration=function(){return boss?._hammer?._hj22Pair?1.72:HJ22.base.recovery.apply(this,arguments);};
hammerBossTick=function(b,dt){const h=b?._hammer,previous=h?.state;const r=HJ22.base.tick.apply(this,arguments);if(!h)return r;if(b.dead){delete h._hj22Pair;h._hj22Double=false;return r;}
 if(previous==='warn'&&h.state==='leap'){h._hj22Double=!b._hammerTime?.hama&&(h._hj22ForceDouble||((h._hj22Leaps=(h._hj22Leaps||0)+1)%2===0));h._hj22ForceDouble=false;}
 if(h.state==='leap'){const u=clamp(h.t/(hammerFurious()?.27:.52),0,1);b.y-=Math.sin(u*Math.PI)*90;}
 if(previous==='leap'&&h.state==='recover'&&h._hj22Double){h._hj22Double=false;h._hj22Pair=hj22Pair(b,'blue',{x:h.tx,y:h.ty+32});HJ22.events.push({type:'double-start',kind:'blue'});}
 if(h._hj22Pair){if(h.state!=='recover'){delete h._hj22Pair;}else{h._hj22Pair.clock=h.t;hj22PairTick(b,h._hj22Pair);}}
 return r;
};
hammerBossDraw=function(b){if(b?._hammer?._hj22Pair)hj22PairDraw(b,b._hammer._hj22Pair);return HJ22.base.draw.apply(this,arguments);};
hb20Start=function(b,type){const force=type==='double',A=HJ22.base.start.call(this,b,force?'skystrike':type),Q=hb20State(b);if(A?.type==='skystrike'&&(force||((Q._hj22Leaps=(Q._hj22Leaps||0)+1)%2===0))){A._hj22Double=true;A.duration+=1.72;}return A;};
v19NativeTick=function(b,dt){const own=hb20Own(b),Q=own&&hb20State(b),A=Q?.action,r=HJ22.base.native.apply(this,arguments);if(b.dead||!own||!A||Q.action!==A||A.type!=='skystrike')return r;
 // Depth is expressed by authored poses. The new bank is never runtime-scaled.
 Q.scale=1;
 // Show the behind-head windup before lift-off, then move the fixed-unit
 // authored body above the screen. Retain the original committed tell time.
 if(A.t<A.tell){const v=clamp((A.t-.6)/.45,0,1);b.x=lerp(A.origin.x,A.target.x,v);b.y=lerp(A.origin.y,viewTopY()-170,v);b._drawY=b.y;const p=gd4Create(b,8).p;p.x=b.x;p.y=b.y;}
 if(A.impact&&A._hj22Double&&!A._hj22Pair){A._hj22Pair=hj22Pair(b,'corrupt',A.target);A._hj22Pair.start=A.t+.15;HJ22.events.push({type:'double-start',kind:'corrupt'});}
 if(A._hj22Pair&&A.t>=A._hj22Pair.start){const P=A._hj22Pair;P.clock=A.t-P.start;hj22PairTick(b,P);const p=gd4Create(b,8).p;p.x=b.x;p.y=b.y;}
 return r;
};
v19DonorDraw=function(b){const A=hb20Own(b)&&hb20State(b)?.action;if(A?._hj22Pair&&A.t>=A._hj22Pair.start)hj22PairDraw(b,A._hj22Pair);return HJ22.base.donor.apply(this,arguments);};
globalThis.BOF_HAMMER_JUMP=HJ22;
const hj22CounterBase=hc11BeginCounter;
hc11BeginCounter=function(b){if(b?._hammer?._hj22Pair)return null;return hj22CounterBase.apply(this,arguments);};
