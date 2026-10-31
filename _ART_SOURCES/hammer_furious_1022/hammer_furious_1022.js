"use strict";
/* Authored GPT poses. Simulation owns position/collision/timing; all new
   visual turns, lighting, palettes and flashes are stored frame pixels. */
const HF22={base:{blue:ha21Blue,pose:hb20Pose,paint:b20Image,flash:ha21Flash,landing:ha21Landing,tick:hammerBossTick,draw:hammerBossDraw,recovery:hammerRecoverDuration,start:hb20Start,native:v19NativeTick,donor:v19DonorDraw,load:stageLoadBegin,keys:v18Keys,warm:v18Warm,pair:hj22Pair,release:hammerBoomerangRelease,throwTick:hammerBoomerangTick,flight:hammerFlightDraw,throwDraw:hammerThrowDraw,grip:hammerGripPoint,toolAt:hb20ToolAt},events:[],draws:{}};
for(const s of Object.values(HF22_ART.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(HF22_ART.banks))for(const a of rows){BOFX.cells[a.key]=[a.sheet,...a.cell];if(a.white)BOFX.cells[a.white]=[a.sheet+'_hit',...a.cell];}
function hf22Kind(b){return hb20Own(b)?'corrupt':'blue';}
function hf22Red(b){return hb20Own(b)?!!(hb20State(b)?._hf22Red||hb20State(b)?.rage):!!b?._hammer?._hf22Red;}
function hf22Keys(n,legacy=false){const kind=n===5?'blue':'corrupt';return Object.entries(HF22_ART.sheets).filter(([id,s])=>(id.includes(kind)||id.includes('warning_'))&&!!s.legacy===legacy).map(([,s])=>s.key);}
stageLoadBegin=function(n,keys){if([5,8].includes(n))Snd.prepare(['hammerImpact','hammerThrow','bossWeaponCharge','shadowCharge']);return HF22.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?hf22Keys(n):[])]);};
v18Keys=function(){return [...HF22.base.keys(),...hf22Keys(8)];};
v18Warm=function(){const old=HF22.base.warm();return hf22Keys(8).map(k=>XART.rdy(k)).every(Boolean)&&old;};
function hf22WarmRed(b){return hf22Keys(hf22Kind(b)==='blue'?5:8,true).map(k=>XART.rdy(k)).every(Boolean);}
function hf22Row(bank,f){const rows=HF22_ART.banks[bank];return rows?.[Math.min(rows.length-1,Math.max(0,Math.floor(f)))];}
function hf22Pose(b,bank,f){let name=bank;if(hf22Red(b)&&HF22_ART.banks[bank+'_red'])name+='_red';else if(bank.startsWith('blue_')&&fr27Armor(b)?.activated&&fr27Armor(b)?.hp>0&&HF22_ART.banks[bank+'_armor'])name+='_armor';const a=hf22Row(name,f);if(!a||!XART.rdy(a.key)||a.white&&!XART.rdy(a.white))return null;HF22.draws[name]=(HF22.draws[name]||0)+1;return{a,k:1,rot:0,kind:name};}
function hf22Cell(a,x,y,flash=0){const key=flash>0&&a.white&&XART.rdy(a.white)?a.white:a.key;if(!XART.rdy(key))return false;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]));return true;}
function hf22Swap(q,b){if(!q||!hf22Red(b))return q;const a=HF22_ART.legacyRed[q.a?.key];return a&&XART.rdy(a.key)?{...q,a}:q;}
function hf22Aura(b){if(!hf22Red(b)||b.dead)return;const a=hf22Row(hf22Kind(b)+'_aura',Math.floor(efxClock*12)%4);if(a)hf22Cell(a,b.x,b.y);}
b20Image=function(a,x,y,k=1,rot=0,flash=0,pivot=a?.pivot){
 const Q=hb20Own(boss)&&hb20State(boss),A=Q?.action;
 if(A?.type==='throw'&&a?.bank==='corrupt_tool'){const at=hb20ToolAt(boss,A);return hf22Tool(boss,at,A.t*20);}
 if(a?._hf22&&!a._hf22Legacy)return hf22Cell(a,x,y,flash);
 if(a?._hf22Legacy){const key=flash>0&&XART.rdy(a.white)?a.white:a.key;return HF22.base.paint.call(this,{...a,key},x,y,k,rot,0,pivot);}
 return HF22.base.paint.apply(this,arguments);
};
ha21Flash=function(b,q){if(q?.a?._hf22){if(q.a._hf22Legacy){const flash=Math.max(b.flash||0,b._lastPart?.flash||0);if(flash>0)return b20Image(q.a,b.x,b.y,q.k,q.rot,flash);}else return hf22Cell(q.a,b.x,b.y,Math.max(b.flash||0,b._lastPart?.flash||0));return;}return HF22.base.flash.apply(this,arguments);};
function hf22Phase(kind,u,phase){const M=HF22_ART.phases[kind],rows=HF22_ART.banks[kind+'_jump'];return phase==='wind'?lerp(0,M.windEnd,clamp(u,0,1)):phase==='strike'?lerp(M.windEnd,M.strikeEnd,clamp(u,0,1)):lerp(M.strikeEnd,rows.length-1,clamp(u,0,1));}
function hf22PairDuration(P){return P.difficulty==='furious'?3.55:1.72;}
function hf22PairPose(b,P){const t=P.clock,kind=P.kind,M=HF22_ART.phases[kind];if(t<.12)return hf22Pose(b,kind+'_jump',M.strikeEnd);if(t<.85)return hf22Pose(b,kind+'_jump',hf22Phase(kind,(t-.12)/.73,'wind'));if(t<1.2)return hf22Pose(b,kind+'_jump',hf22Phase(kind,(t-.85)/.35,'strike'));
 if(P.difficulty!=='furious')return hf22Pose(b,kind+'_jump',hf22Phase(kind,(t-1.2)/.52,'recover'));
 const S=HF22_ART.sides[kind];if(t<1.36)return hf22Pose(b,kind+'_jump',M.strikeEnd);if(t<2.14)return hf22Pose(b,kind+'_sides',lerp(0,S.left-1,clamp((t-1.36)/.78,0,1)));if(t<2.92)return hf22Pose(b,kind+'_sides',lerp(S.left,S.left+S.right-1,clamp((t-2.14)/.78,0,1)));return hf22Pose(b,kind+'_sides',S.ready);
}
hj22Pair=function(b,kind,target){return{...HF22.base.pair(b,kind,target),difficulty:diffKey,leftHit:new Set(),rightHit:new Set()};};
hj22PairTick=function(b,P){const a=hf22Row(P.kind+'_jump',HF22_ART.phases[P.kind].strikeEnd),end={x:P.target.x-(a.tip[0]-a.pivot[0]),y:P.target.y-(a.tip[1]-a.pivot[1])},u=clamp(P.clock/1.2,0,1);b.x=lerp(P.origin.x,end.x,u);b.y=lerp(P.origin.y,end.y,u)-Math.sin(u*Math.PI)*(P.kind==='blue'?70:110);b._drawY=b.y;
 if(P.clock<=1.2)combatWarningTick(P,'hammer-second-down',Math.min(P.clock,.85),.85);
 if(P.clock>=1.2&&!P.impact){P.impact=true;b20HitSegment(b,P.target,P.target,P.kind==='blue'?62:46,'Hammer second downward slam',P.hit);if(P.kind==='corrupt')hb20Wave(b,hb20State(b),P.target);explode(P.target.x,P.target.y,70,P.kind==='blue'?'blue':'purple');shake=Math.max(shake,10);b20Cue('hammerImpact');HF22.events.push({type:'second-down',kind:P.kind});}
 if(P.difficulty==='furious')for(const [side,start,active,endTime]of[['left',1.36,1.76,2.14],['right',2.14,2.54,2.92]]){if(P.clock>=start&&P.clock<active)combatWarningTick(P,'hammer-furious-'+side,P.clock-start,active-start);if(P.clock>=active&&P.clock<=endTime){const q=hf22PairPose(b,P);if(!q?.a)continue;const at=hb20World(q.a,q.a.tip,b,1,0),prev=P[side+'Prev']||at;P[side+'Prev']=at;b20HitSegment(b,prev,at,30,'Hammer '+side+' sweep',P[side+'Hit']);if(!P[side+'Cue']){P[side+'Cue']=true;b20Cue('hammerThrow');HF22.events.push({type:side+'-swing',kind:P.kind});}}}
};
function hf22Warning(at,u,dir='down'){const f=u<1/3?0:u<2/3?1:2,a=hf22Row('warning_'+dir,f);if(a)hf22Cell(a,at.x,at.y);}
hj22PairDraw=function(b,P){if(b.dead)return;if(P.clock<1.2){hf22Warning(P.target,clamp(P.clock/.85,0,1));const r=hj22Frame('warning_reticle',P.clock/.85<1/3?0:P.clock/.85<2/3?1:2);if(r&&XART.rdy(r.key))ctx.drawImage(XART.get(r.key),Math.round(P.target.x-r.pivot[0]),Math.round(P.target.y-r.pivot[1]));}
 if(P.difficulty==='furious'){if(P.clock>=1.36&&P.clock<1.76)hf22Warning({x:b.x,y:b.y-15},(P.clock-1.36)/.4,'left');if(P.clock>=2.14&&P.clock<2.54)hf22Warning({x:b.x,y:b.y-15},(P.clock-2.14)/.4,'right');}
};
hammerRecoverDuration=function(){const P=boss?._hammer?._hj22Pair;return P?hf22PairDuration(P):HF22.base.recovery.apply(this,arguments);};
ha21Landing=function(b,target,kind,frame,scale){if(!b._gp4Host&&!b._hammerTime?.hama&&!b._hammer?.state?.startsWith('giant_')&&['slam','jump'].includes(kind)){const a=hf22Row('blue_jump',HF22_ART.phases.blue.strikeEnd);return{x:target.x-(a.tip[0]-a.pivot[0]),y:target.y-(a.tip[1]-a.pivot[1])};}return HF22.base.landing.apply(this,arguments);};
ha21Blue=function(b){const h=b?._hammer;if(!h||b.dead||b._gp4Host||b._hammerTime?.hama)return hf22Swap(HF22.base.blue.apply(this,arguments),b);const music=b._hammerTime||b._hama;if(music&&music.mode!=='attack'||hf19Recovery(b)&&h.state!=='recover')return hf22Swap(HF22.base.blue.apply(this,arguments),b);
 if(h._hf22Charge)return hf22Pose(b,'blue_rage',h._hf22Charge.t<.6?0:1);
 if(h._hf22StormPair)return hf22PairPose(b,h._hf22StormPair);
 if(h._hj22Pair&&h.state==='recover')return hf22PairPose(b,h._hj22Pair);
 const s=h.state,t=h.t||0;let f=null;if(s==='warn')f=hf22Phase('blue',t/(hammerFurious()?.58:1.2),'wind');else if(s==='leap')f=hf22Phase('blue',Math.max(0,t/(hammerFurious()?.27:.52)-.12)/.88,'strike');else if(s==='recover')f=hf22Phase('blue',t/HF22.base.recovery(),'recover');else if(s==='storm_warn')f=hf22Phase('blue',t/(hammerFurious()?.9:hammerHard()?1:1.15),'wind');else if(s==='storm_slam')f=hf22Phase('blue',t/(hammerFurious()?.46:hammerHard()?.52:.6),'strike');else if(s==='storm_split')f=hf22Phase('blue',t/.75,'recover');
 if(f!=null)return hf22Pose(b,'blue_jump',f);if(['spin','revenge_charge'].includes(s))return hf22Pose(b,'blue_throw',clamp(t/(s==='spin'?HAMMER_SPIN_TIME:2),0,1)*4);if(s==='throw')return hf22Pose(b,'blue_throw',t<.15?5:t<.35?6:7);if(s==='hammer_catch')return hf22Pose(b,'blue_throw',0);
 if(['hammer','storm_idle','back','leap_reset','enrage'].includes(s)){if(hf22Red(b))return hf22Pose(b,'blue_rage',2+Math.floor(efxClock*10)%4);return hf22Pose(b,'blue_jump',0);}
 return hf22Swap(HF22.base.blue.apply(this,arguments),b);
};
hb20Pose=function(b){if(hb20Own(b)){const Q=hb20State(b),A=Q?.action,u=(A?.t||0)-(A?.tell||0);if(A?.type==='skystrike'){if(A._hj22Pair&&A.t>=A._hj22Pair.start){A._hj22Pair.clock=A.t-A._hj22Pair.start;return hf22PairPose(b,A._hj22Pair);}const f=u<0?hf22Phase('corrupt',A.t/.6,'wind'):u<.9?hf22Phase('corrupt',Math.max(0,u-.1)/.5,'strike'):hf22Phase('corrupt',(u-.9)/.4,'recover');return hf22Pose(b,'corrupt_jump',f);}
  if(A?.type==='throw')return hf22Pose(b,'corrupt_throw',u<0?clamp(A.t/A.tell,0,1)*4:u<.15?5:u<.35?6:7);
  if(A?.type==='redrage')return hf22Pose(b,'corrupt_rage',A.t<.6?0:1);
  if(A?.type==='fire')return hf22Pose(b,'corrupt_rage',6+Math.min(3,Math.floor(A.t/A.duration*4)));
  if(!A)return hf22Red(b)?hf22Pose(b,'corrupt_rage',(Q.rage||Q.broken?6:2)+Math.floor(efxClock*10)%4):hf22Pose(b,'corrupt_jump',0);
 }return hf22Swap(HF22.base.pose.apply(this,arguments),b);};
function hf22BeginBlueRage(b){const h=b._hammer;if(h._hf22Red||h._hf22Charge)return;h._hf22Red=true;h._hf22Charge={t:0,resume:h.state};h.state='hf22_rage_charge';h.t=0;hf22WarmRed(b);b20Cue('shadowCharge');HF22.events.push({type:'rage',kind:'blue'});}
hammerBossTick=function(b,dt){if(b?._gp4Host||b?._hammerTime?.hama)return HF22.base.tick.apply(this,arguments);const h=b?._hammer,previous=h?.state;if(h&&!b.dead&&!h._hf22Red&&!h.hb20Pickup&&!h.hc11Counter&&h.recovery?.status!=='charging'&&b.hp<=b.maxhp*.35&&['hammer','storm_idle'].includes(h.state)&&!h.phasePending)hf22BeginBlueRage(b);
 if(h?._hf22StormPair)h.state='hf22_storm_combo';
 const r=HF22.base.tick.apply(this,arguments);if(!h)return r;if(b.dead){delete h._hf22Charge;delete h._hf22StormPair;return r;}
 if(h._hf22Charge){const C=h._hf22Charge;C.t+=dt;const ready=hf22WarmRed(b);if(C.t>=1.8&&(ready||C.t>=8)){delete h._hf22Charge;hammerState(b,C.resume);}return r;}
 if(previous==='warn'&&h.state==='leap')h._hj22Double=diffKey==='hard'||diffKey==='furious';
 if(previous==='leap'&&h.state==='recover'){h.followCount=hammerFurious()?5:hammerHard()?3:1;HF22.events.push({type:'first-down',kind:'blue',difficulty:diffKey});}
 if(previous==='storm_slam'&&h.state==='storm_split'){HF22.events.push({type:'first-down',kind:'blue-storm',difficulty:diffKey});if(diffKey==='hard'||diffKey==='furious')h._hf22StormPair=hj22Pair(b,'blue',h.stormTarget);}
 if(h._hf22StormPair){const P=h._hf22StormPair;P.clock+=dt;hammerStormWaveTick(b,dt);hj22PairTick(b,P);if(P.clock>=hf22PairDuration(P)){delete h._hf22StormPair;hammerState(b,'storm_split');h.t=1;}}
 return r;
};
function hf22ThrowWarning(b,u){hf22Warning({x:camLeftX()+44,y:viewTopY()+viewH()-70},u);hf22Warning({x:camRightX()-44,y:viewTopY()+70},u,'up');hf22Warning({x:camLeftX()+30,y:viewTopY()+70},u,'right');hf22Warning({x:camRightX()-30,y:viewTopY()+viewH()-70},u,'left');}
hammerBossDraw=function(b){hf22Aura(b);if(b?._hammer?._hf22StormPair)hj22PairDraw(b,b._hammer._hf22StormPair);if(['spin','revenge_charge'].includes(b?._hammer?.state))hf22ThrowWarning(b,clamp(b._hammer.t/(b._hammer.state==='spin'?HAMMER_SPIN_TIME:2),0,1));return HF22.base.draw.apply(this,arguments);};
hb20Start=function(b,type){const A=HF22.base.start.apply(this,arguments),Q=hb20State(b);if(A?.type==='skystrike'){A._hj22Double=diffKey==='hard'||diffKey==='furious';A.duration=A.tell+1.75+(A._hj22Double?(diffKey==='furious'?3.55:1.72):0);}if(A?.type==='throw')A.duration=A.tell+3.2;if(A?.type==='redrage'){Q._hf22Red=true;A.tell=0;A.duration=1.8;hf22WarmRed(b);b20Cue('shadowCharge');HF22.events.push({type:'rage',kind:'corrupt'});}if(A?.type==='fire'){Q._hf22Red=true;hf22WarmRed(b);}return A;};
v19NativeTick=function(b,dt){if(hb20Own(b)&&!b.dead){const Q=hb20State(b);if(Q&&!Q.action&&Q.cool<=0&&!Q._hf22Red&&!Q.broken&&!Q.rage&&b.hp<=b.maxhp*.45)hb20Start(b,'redrage');if(Q?.action?.type==='redrage'){Q.action._hf22Wait=(Q.action._hf22Wait||0)+dt;if(Q.action.t>=1.6&&!hf22WarmRed(b)&&Q.action._hf22Wait<8)Q.action.t=1.59;}}
 const r=HF22.base.native.apply(this,arguments);return r;
};
v19DonorDraw=function(b){if(hb20Own(b)){hf22Aura(b);const A=hb20State(b)?.action;if(A?.type==='throw'&&A.t<A.tell)hf22ThrowWarning(b,A.t/A.tell);}return HF22.base.donor.apply(this,arguments);};
function hf22Tool(b,at,angle){const kind=hf22Kind(b),a=hf22Row(kind+'_tool'+(hf22Red(b)?'_red':''),((Math.floor(angle/TAU*32)%32)+32)%32),Q=kind==='corrupt'&&hb20State(b),flash=Math.max(b.flash||0,Q?.parts?.[1]?.flash||0,b._lastPart?.flash||0);return a&&hf22Cell(a,at.x,at.y,flash);}
function hf22Orbit(b,age,origin,duration=2.6){const cx=(camLeftX()+camRightX())/2,cy=viewTopY()+viewH()/2,rx=Math.max(60,viewW()/2-44),ry=Math.max(70,viewH()/2-70),theta=Math.atan2((origin.y-cy)/ry,(origin.x-cx)/rx),angle=theta+clamp((age-.2)/(duration-.2),0,1)*TAU,edge={x:cx+Math.cos(angle)*rx,y:cy+Math.sin(angle)*ry};return age<.2?{x:lerp(origin.x,edge.x,age/.2),y:lerp(origin.y,edge.y,age/.2)}:edge;}
hammerBoomerangRelease=function(b){if(b?._gp4Host||b?._hammerTime?.hama)return HF22.base.release.apply(this,arguments);const a=hf22Row('blue_throw',4),at=hb20World(a,a.tip,b,1,0),r=HF22.base.release.apply(this,arguments),T=b._hammer.throw;if(T){T.x=T.ox=at.x;T.y=T.oy=at.y;T._hf22Origin={...at};T._hf22Age=0;T.phase='hf22_orbit';T.t=0;T.trail=[];HF22.events.push({type:'throw-release',kind:'blue',x:at.x,y:at.y});}return r;};
hammerBoomerangTick=function(b,dt){const T=b?._hammer?.throw;if(!T?._hf22Origin||T.reflected||T.phase!=='hf22_orbit')return HF22.base.throwTick.apply(this,arguments);T._hf22Age+=dt;T.t+=dt;T.angle+=dt*20;const at=hf22Orbit(b,T._hf22Age,T._hf22Origin);T.x=at.x;T.y=at.y;hammerBoomerangHit(T,dt);if(T._hf22Age>=2.6){T.phase='return';T.t=0;b20Cue('hammerMagnet');}return true;};
hammerGripPoint=function(b){if(b?._hammer?.throw?._hf22Origin||b?._hammer?.state==='hammer_catch'){const a=hf22Row('blue_throw',0);return hb20World(a,a.tip,b,1,0);}return HF22.base.grip.apply(this,arguments);};
hammerFlightDraw=function(T,alpha){if(boss?._hammer?.throw?._hf22Origin){if(alpha!=null&&alpha<1)return false;return hf22Tool(boss,T,T.angle);}return HF22.base.flight.apply(this,arguments);};
hammerThrowDraw=function(b){if(!b._gp4Host&&!b._hammerTime?.hama&&['spin','throw','hammer_catch','revenge_charge'].includes(b?._hammer?.state)){if(b._hammer.throw)hammerFlightDraw(b._hammer.throw,1);return true;}return HF22.base.throwDraw.apply(this,arguments);};
hb20ToolAt=function(b,A){if(hb20Own(b)&&A?.type==='throw'){const source=hf22Row('corrupt_throw',4),origin=hb20World(source,source.tip,A.origin,1,0),u=Math.max(0,A.t-A.tell);if(u<=2.6)return hf22Orbit(b,u,origin);const ready=hf22Row('corrupt_throw',0),to=hb20World(ready,ready.tip,b,1,0),from=hf22Orbit(b,2.6,origin),v=clamp((u-2.6)/.55,0,1);return{x:lerp(from.x,to.x,v),y:lerp(from.y,to.y,v)};}return HF22.base.toolAt.apply(this,arguments);};
globalThis.BOF_HAMMER_FURIOUS=HF22;
const hf22CounterBase=hc11BeginCounter;
hc11BeginCounter=function(b){if(b?._hammer?._hf22StormPair||b?._hammer?._hf22Charge)return null;return hf22CounterBase.apply(this,arguments);};
