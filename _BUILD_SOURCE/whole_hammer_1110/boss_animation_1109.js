'use strict';
/* One landing, planted repeat contacts. New authored poses and their measured
   weapon/mask landmarks share the native attack, damage and hit-flash owners. */
const BA119={events:[],draws:{},base:{pose:ha21Blue,pair:hj22Pair,pairPose:hf22PairPose,
 furiousPose:hf22FuriousPose,pairTick:hj22PairTick,furiousTick:hf22FuriousTick,
 combo:c27ComboTick,duration:hf22PairDuration,landing:ha21Landing,warn:hj22PairDraw,
 jumpPose:rd74JumpPose,sample:rd74Sample,melee:rd74Melee,impact:rd74Impact,
 native:v19NativeTick,load:stageLoadBegin,keys:v18Keys,warm:v18Warm},keys:{5:[],8:[]}};
for(const [name,a]of Object.entries(BA119_ART)){
 const stage=name.startsWith('blue')?5:8,cw=a.cell?.[0]||576,ch=a.cell?.[1]||576;
 for(const mat of ['regular','chrome','red','hit','red_hit']){
  const sheet='ba119_'+name+'_'+mat,key='nca_'+sheet;
  XART._src[key]='assets/game/shared/combat/'+(a.folder||'boss_animation_1109')+'/'+name+'_'+mat+'.webp';if((!name.includes('-arm')||['regular','hit'].includes(mat))&&(mat!=='red_hit'||name==='blue-roll')&&(stage!==5||mat!=='red'))BA119.keys[stage].push(key);
  for(let f=0;f<a.count;f++)BOFX.cells[sheet+'_'+f]=[sheet,f%4*cw,Math.floor(f/4)*ch,cw,ch];
 }
 if(stage===8&&name.startsWith('corrupt-'))for(const mat of ['regular','chrome','red'])RD74_ART.banks['ba119_'+name+'_'+mat]={
  key:'nca_ba119_'+name+'_'+mat,hitKey:'nca_ba119_'+name+'_hit',frames:16,cols:4,cw,ch,pivot:a.pivot,meta:a.meta};
}
function ba119Log(type,data={}){BA119.events.push({type,clock:efxClock,...data});if(BA119.events.length>900)BA119.events.shift();}
function ba119Warm(stage){return (BA119.keys[stage]||[]).map(k=>XART.rdy(k)).every(Boolean);}
stageLoadBegin=function(n,keys){return BA119.base.load.call(this,n,[...(keys||[]),...(BA119.keys[n]||[])]);};
v18Keys=function(){return [...BA119.base.keys(),...BA119.keys[8]];};
v18Warm=function(){return ba119Warm(8)&&BA119.base.warm();};
function ba119Row(bank,f,mat='regular'){
 const a=BA119_ART[bank];f=clamp(Math.floor(f),0,a.count-1);const key='ba119_'+bank+'_'+mat+'_'+f;
 return {...a.meta[f],w:a.cell?.[0]||576,h:a.cell?.[1]||576,pivot:a.pivot,key,white:'ba119_'+bank+'_hit_'+f,
  redHit:'ba119_'+bank+'_red_hit_'+f,_hf22:true,_c26:true,_c27:true,_ba119:true,bank,frame:f};
}
function ba119Pose(bank,f,mat,k=1){const a=ba119Row(bank,f,mat);if(!XART.rdy(a.key)||!XART.rdy(a.white))return null;
 BA119.draws[bank]=(BA119.draws[bank]||0)+1;return {a,k,rot:0,kind:bank};}
function ba119At(b,a,k=1){return{x:b.x+(a.tip[0]-a.pivot[0])*k,y:b.y+(a.tip[1]-a.pivot[1])*k};}
function ba119Blue(b){return c25Own(b)&&!b.dead&&!b._gp4Host&&!b._hammerTime?.hama;}
function ba119Frame(list,u){return list[Math.min(list.length-1,Math.floor(clamp(u,0,.999999)*list.length))];}
const BA119_REPEAT={wind:.76,impact:1.02,left:1.18,leftHit:1.68,leftEnd:2.24,right:2.24,rightHit:2.74,rightEnd:3.30,end:3.55};
function ba119SideFrame(age){return age<.5?age/.5*5:age<.78?5+(age-.5)/.28*4:9+(age-.78)/.28*7;}
function ba119PairPose(b,P){const t=P.clock,T=BA119_REPEAT,k=P.scale||1,mat=c27Material(b);
 if(t<T.wind)return ba119Pose('blue-overhead',ba119Frame([11,12,13,14,15,0,1,2,3,4,5,6,7,8],t/T.wind),mat,k);
 if(t<T.impact)return ba119Pose('blue-overhead',9+(t-T.wind)/(T.impact-T.wind)*3,mat,k);
 if(P.difficulty!=='furious')return ba119Pose('blue-overhead',12+(t-T.impact)/.65*3,mat,k);
 if(t<T.left)return ba119Pose('blue-overhead',11,mat,k);
 if(t<T.leftEnd)return ba119Pose('blue-sides',ba119SideFrame(t-T.left),mat,k);
 if(t<T.rightEnd)return ba119Pose('blue-right',ba119SideFrame(t-T.right),mat,k);
 return ba119Pose('blue-overhead',ba119Frame([12,13,14,15],(t-T.rightEnd)/(T.end-T.rightEnd)),mat,k);
}
hj22Pair=function(b,kind,target){const P=BA119.base.pair.apply(this,arguments);if(kind==='blue'&&ba119Blue(b)){
 P.ba119=true;P.origin={x:b.x,y:b.y};P.target={...target};P.difficulty=diffKey;P.track=null;
 ba119Log('planted-combo-start',{stage:5,difficulty:diffKey,origin:P.origin});}return P;};
hf22PairDuration=function(P){return P.ba119?(P.difficulty==='furious'?BA119_REPEAT.end:1.67):BA119.base.duration(P);};
hf22PairPose=function(b,P){return P?.ba119?ba119PairPose(b,P):BA119.base.pairPose.apply(this,arguments);};
hf22FuriousPose=function(b,P){return P?.ba119?ba119PairPose(b,P):BA119.base.furiousPose.apply(this,arguments);};
function ba119PairTick(b,P){const t=P.clock,T=BA119_REPEAT,k=P.scale||1;
 b.x=P.origin.x;b.y=P.origin.y;b._drawY=b.y;const q=ba119PairPose(b,P);if(!q)return;
 if(!P.ba119Mark){P.ba119Mark=ba119At(b,ba119Row('blue-overhead',11,c27Material(b)),k);P.target={...P.ba119Mark};}
 const hit=(id,start,end,cue)=>{if(t<start||t>end)return;const at=ba119At(b,q.a,k),prev=P['ba119Prev'+id]||at;P['ba119Prev'+id]=at;
  P['ba119Hit'+id]??=new Set();b20HitSegment(b,prev,at,id===2?60*k:28*k,'Chronos planted '+id,P['ba119Hit'+id]);
  if(!P['ba119Cue'+id]){P['ba119Cue'+id]=true;b20Cue(cue);ba119Log('planted-contact',{stage:5,stroke:id,root:{x:b.x,y:b.y},at});}
 };
 hit(2,T.impact,T.impact+.09,'hammerImpact');
 if(t>=T.impact&&!P.impact)P.impact=true;
 if(P.difficulty==='furious'){hit(3,T.leftHit,T.left+.78,'hammerThrow');hit(4,T.rightHit,T.right+.78,'hammerThrow');}
 if(t<T.impact)combatWarningTick(P,'ba119-repeat',Math.min(t,T.wind),T.wind);
}
hj22PairTick=function(b,P){return P.ba119?ba119PairTick(b,P):BA119.base.pairTick.apply(this,arguments);};
hf22FuriousTick=function(b,P){return P.ba119?ba119PairTick(b,P):BA119.base.furiousTick.apply(this,arguments);};
c27ComboTick=function(b,P){return P.ba119?ba119PairTick(b,P):BA119.base.combo.apply(this,arguments);};
hj22PairDraw=function(b,P){if(!P.ba119)return BA119.base.warn.apply(this,arguments);if(b.dead)return;
 const t=P.clock,T=BA119_REPEAT,k=P.scale||1;
 if(t<T.impact){const a=P.ba119Mark||P.target;b20Reticle(a.x,a.y,54*k,clamp(t/T.wind,0,1));}
 if(P.difficulty==='furious')for(const [side,start,hit]of [['blue-sides',T.left,T.leftHit],['blue-right',T.right,T.rightHit]]){
  if(t<start||t>=hit)continue;const a=ba119At(b,ba119Row(side,3),k),z=ba119At(b,ba119Row(side,8),k);
  combatWarningDraw(P,{x:a.x,y:a.y,ex:z.x,ey:z.y,width:58*k,progress:(t-start)/(hit-start),fieldOnly:true});
 }};
ha21Landing=function(b,target,kind,frame,scale){if(ba119Blue(b)&&['slam','jump'].includes(kind)){
 const a=ba119Row('blue-overhead',11,c27Material(b)),k=b._hammer.state.startsWith('giant_')?1.25:1;
 return{x:target.x-(a.tip[0]-a.pivot[0])*k,y:target.y-(a.tip[1]-a.pivot[1])*k};}return BA119.base.landing.apply(this,arguments);};
ha21Blue=function(b){if(!ba119Blue(b)||b._hammer.c25Knock||b._hammer.hb20Pickup)return BA119.base.pose.apply(this,arguments);
 const h=b._hammer,s=h.state,t=h.t||0,mat=c27Material(b),P=h.c27Combo||h._hf22StormPair||(s==='recover'&&h._hj22Pair);
 if(P?.ba119)return ba119PairPose(b,P);
 if(['curl','ball','uncurl'].includes(s)){
  const u=s==='curl'?clamp(t/HAMMER_BALL_WARN,0,1):s==='uncurl'?1-clamp(t/1.65,0,1):1;
  return ba119Pose(s==='ball'?'blue-roll':'blue-fold',s==='ball'?((Math.floor((h.angle||0)/TAU*16)%16)+16)%16:u*15,mat,s==='ball'?1:lerp(1,.45,u*u*(3-2*u)));
 }
 let f=null,k=1;
 if(s==='warn'||s==='storm_warn')f=clamp(t/(s==='warn'?(hammerFurious()?.58:1.2):(hammerFurious()?.9:hammerHard()?1:1.15)),0,1)*8;
 if(s==='leap'||s==='storm_slam')f=8+clamp(t/(s==='leap'?(hammerFurious()?.27:.52):(hammerFurious()?.46:hammerHard()?.52:.6)),0,1)*3;
 if(s==='recover'&&!P)f=11+clamp(t/hammerRecoverDuration(),0,1)*4;
 if(s==='giant_dive'){f=8+clamp(t/.65,0,1)*3;k=hammerDepthScale(b);}
 if(s==='giant_sweep'){f=11;k=1.25;}
 return f==null?BA119.base.pose.apply(this,arguments):ba119Pose('blue-overhead',f,mat,k);
};
// The existing red-ball exception remains a stored, matching alpha silhouette.
BA119.base.paint=c26Paint;
c26Paint=function(a,x,y,k=1,rot=0,flash=0){if(a?._ba119){const red=ba119Blue(boss)&&boss._hammer.state==='ball'&&flash>0&&!boss._hammer.c27BallMissile;
 const key=flash>0?(red?a.redHit:a.white):a.key;if(!XART.rdy(key))return false;
 ctx.drawImage(XART.get(key),Math.round(x-a.pivot[0]*k),Math.round(y-a.pivot[1]*k),a.w*k,a.h*k);return true;}return BA119.base.paint.apply(this,arguments);};
function ba119Corrupt(Q,f,bank='corrupt-overhead'){return BA119.base.sample('ba119_'+bank+'_'+rd74Mat(Q),f);}
rd74JumpPose=function(Q,A){const u=A.t-A.tell;
 if(A.t<A.tell)return ba119Corrupt(Q,Math.min(8,A.t/A.tell*8));
 if(u<.55)return ba119Corrupt(Q,8);
 if(u<1)return ba119Corrupt(Q,8+(u-.55)/.45*3);
 if(u<1.4)return ba119Corrupt(Q,11+(u-1)/.4*4);
 if(A.strikes>1&&u<1.85)return ba119Corrupt(Q,ba119Frame([15,0,1,2,3,4,5,6,7,8],(u-1.4)/.45));
 if(A.strikes>1&&u<2.3)return ba119Corrupt(Q,8+(u-1.85)/.45*3);
 if(A.strikes>1&&u<2.7)return ba119Corrupt(Q,11+(u-2.3)/.4*4);
 if(A.strikes===4&&u<3.4)return ba119Corrupt(Q,u<3.1375?(u-2.7)/.4375*5:5+(u-3.1375)/.2625*10,'corrupt-sides');
 if(A.strikes===4&&u<4.1)return ba119Corrupt(Q,u<3.75?(u-3.4)/.35*5:5+(u-3.75)/.35*10,'corrupt-right');
 return ba119Corrupt(Q,15);
};
rd74Sample=function(bank,f=0){const Q=rd74Own(boss)&&hb20State(boss),A=Q?.action;
 if(A?.type==='skystrike'&&f===16){if(bank.startsWith('strike_'))return ba119Corrupt(Q,11);
  if(bank.startsWith('left_'))return ba119Corrupt(Q,5,'corrupt-sides');if(bank.startsWith('right_'))return ba119Corrupt(Q,5,'corrupt-right');}
 return BA119.base.sample.apply(this,arguments);};
function ba119Root(b,A){const q=ba119Corrupt(hb20State(b),11),a=q.a;
 const bounds=[a.bounds],left=Math.max(...bounds.map(r=>a.pivot[0]-r[0]))+4,right=Math.max(...bounds.map(r=>r[2]-a.pivot[0]))+4;
 const root=A.ba119Root||(A.ba119Root={x:clamp(A.target.x-a.tip[0]+a.pivot[0],camLeftX()+left,camRightX()-right),y:clamp(A.target.y-a.tip[1]+a.pivot[1],viewTopY()+135,VH-155)});
 b.x=root.x;b.y=root.y;b._drawY=b.y;return root;}
rd74Melee=function(b,A,part,head){if(A.type==='skystrike'){const u=A.t-A.tell;if(part===3&&u<3||part===4&&u<3.7){A.last=null;return;}ba119Root(b,A);head=rd74Point(b,hb20Pose(b));}return BA119.base.melee.call(this,b,A,part,head);};
rd74Impact=function(b,A,i){if(A.type==='skystrike')ba119Root(b,A);const old=A['impact'+i],out=BA119.base.impact.apply(this,arguments);
 if(!old)ba119Log('planted-contact',{stage:8,stroke:i,root:{x:b.x,y:b.y},at:rd74Point(b,hb20Pose(b))});return out;};
v19NativeTick=function(b,dt){const A=rd74Own(b)&&hb20State(b)?.action,out=BA119.base.native.apply(this,arguments);
 if(A&&hb20State(b).action===A&&A.type==='skystrike'){const u=A.t-A.tell;if(u>=.55)ba119Root(b,A);
  if(A.strikes===4){if(u>=3.1375)rd74Impact(b,A,3);if(u>=3.75)rd74Impact(b,A,4);}
  if(A.strikes===4)for(const [side,start]of [['left',2.7],['right',3.4]])if(u>=start&&u<start+.3)combatWarningTick(b,'ba119-rd74-'+A.serial+'-'+side,u-start,.3);
 }return out;};
BA119.base.donorDraw=v19DonorDraw;
v19DonorDraw=function(b){const out=BA119.base.donorDraw.apply(this,arguments);if(rd74Own(b)){const Q=hb20State(b),A=Q.action;if(A?.type==='skystrike'){
 const u=A.t-A.tell;if(A.strikes>1&&u>=1.4&&u<2.3)b20Reticle(A.target.x,A.target.y,52,clamp((u-1.4)/.45,0,1));
 if(A.strikes===4)for(const [side,start,f]of [['left',2.7,3],['right',3.4,3]])if(u>=start&&u<start+.3){const bank=side==='left'?'corrupt-sides':'corrupt-right',a=rd74Point(b,ba119Corrupt(Q,f,bank)),z=rd74Point(b,ba119Corrupt(Q,f+3,bank));
 combatWarningDraw(A,{x:a.x,y:a.y,ex:z.x,ey:z.y,width:56,progress:(u-start)/.3,fieldOnly:true});}
 }}return out;};
BA119.base.start=hb20Start;
hb20Start=function(b,type){const A=BA119.base.start.apply(this,arguments);if(rd74Own(b)&&A?.type==='skystrike'){
 const origin={x:b.x,y:b.y};ba119Root(b,A);A.target=rd74Point(b,ba119Corrupt(hb20State(b),11));b.x=origin.x;b.y=origin.y;b._drawY=b.y;}return A;};
BA119.base.glowActive=cgActive;
cgActive=function(b){const h=b?._hammer;return ba119Blue(b)&&!h.c25Knock&&!h.hb20Pickup&&['warn','leap','recover','storm_warn','storm_slam','giant_dive','giant_sweep','c27_depth_combo','hf22_storm_combo','curl','ball','uncurl'].includes(h.state)?false:BA119.base.glowActive.apply(this,arguments);};
// Replace the previous display-only arm overlays. The complete current module
// now owns the same alpha mask, weapon tip, Retina point and breakaway anchors.
window.PR118_CLAW_OFF=1;
function ba119ArmIndex(f){if(f<16)return Math.floor(f/16*6);if(f<28)return 6+Math.floor((f-16)/12*5);
 if(f<32)return 11;if(f<48)return 12+Math.min(3,Math.floor((f-32)/16*4));if(f<56)return 12+Math.min(3,Math.floor((f-48)/8*4));return [15,4,5,6,7,8,9,10][clamp(f-56,0,7)];}
function ba119ArmBank(kind,side){return kind+'-arm'+(side==='right'?'-right':'');}
function ba119ArmAnchor(side,kind='final'){return side==='left'?[kind==='drone'?404:420,145]:[kind==='drone'?171:155,145];}
function ba119Contains(spans,x,y){const row=spans[Math.floor(y)];if(!row)return false;for(let i=0;i<row.length;i+=2)if(x>=row[i]&&x<row[i+1])return true;return false;}
for(const side of ['left','right']){const a=RD96_ART['arm_'+side],bank=BA119_ART[ba119ArmBank('drone',side)],root=ba119ArmAnchor(side,'drone');
 if(!bank)continue;for(let f=0;f<64;f++){const old=a.poses[f],m=bank.meta[ba119ArmIndex(f)];if(bank.mount)old.root=old.root.map((v,k)=>v+bank.mount[k]);
  old.tip=[old.root[0]+m.tip[0]-root[0],old.root[1]+m.tip[1]-root[1]];old.elbow=[lerp(old.root[0],old.tip[0],.48),lerp(old.root[1],old.tip[1],.48)];}
}
BA119.base.armBlit=rd96Blit;BA119.base.armAlpha=rd96Alpha;
rd96Blit=function(n,f,x,y,hit=false){if(n==='arm_left'||n==='arm_right'){
 const side=n.slice(4),bank=ba119ArmBank('drone',side),a=BA119_ART[bank];if(a){const i=ba119ArmIndex(clamp(f|0,0,63)),anchor=ba119ArmAnchor(side,'drone'),root=RD96_ART[n].poses[clamp(f|0,0,63)].root,key='nca_ba119_'+bank+'_'+(hit?'hit':'regular');
  if(!XART.rdy(key))return false;ctx.drawImage(XART.get(key),i%4*576,Math.floor(i/4)*576,576,576,Math.round(x+root[0]-anchor[0]),Math.round(y+root[1]-anchor[1]),576,576);BA119.draws[bank]=(BA119.draws[bank]||0)+1;return true;}}
 return BA119.base.armBlit.apply(this,arguments);};
rd96Alpha=function(n,f,x,y){if(n==='arm_left'||n==='arm_right'){const side=n.slice(4),a=BA119_ART[ba119ArmBank('drone',side)];if(a){const root=RD96_ART[n].poses[clamp(f|0,0,63)].root,anchor=ba119ArmAnchor(side,'drone');
 return ba119Contains(a.meta[ba119ArmIndex(f)].spans,x-root[0]+anchor[0],y-root[1]+anchor[1]);}}return BA119.base.armAlpha.apply(this,arguments);};
for(const bank of ['sideL','sideR','jumpL','jumpR']){const rows=RD88_ART.banks[bank];if(!rows)continue;
 const side=bank.endsWith('L')?'left':'right',name=ba119ArmBank('final',side),a=BA119_ART[name];if(!a)continue;
 const key='nca_ba119_'+name+'_regular',hitKey='nca_ba119_'+name+'_hit',anchor=ba119ArmAnchor(side);RD88_ART.pages[key]={hitKey};
 for(let f=0;f<rows.length;f++){const q=rows[f],jump=bank.startsWith('jump'),wind=jump?12:16,strike=jump?28:32;
  const i=f<wind?Math.min(5,Math.floor(f/wind*6)):f<strike?6+Math.min(5,Math.floor((f-wind)/(strike-wind)*6)):12+Math.min(3,Math.floor((f-strike)/(rows.length-strike)*4));
  const m=a.meta[i],J=q.joints[side].shoulder.map((v,k)=>v+(a.mount?.[k]||0));q.joints[side].shoulder=J;const offset=[J[0]-RD88_ART.pivot[0]-anchor[0],J[1]-RD88_ART.pivot[1]-anchor[1]],target=m.tip.map((v,k)=>v+offset[k]);
  const part={...q.parts[side],key,rect:[i%4*576,Math.floor(i/4)*576,576,576],w:576,h:576,offset,spans:m.spans,target,rupture:[J.map((v,k)=>v-RD88_ART.pivot[k]),target]};
  q.parts[side]=part;q.joints[side].tip=target.map((v,k)=>v+RD88_ART.pivot[k]);
  const spans=m.spans.map((row,y)=>{if(Math.abs(y-m.tip[1])>48)return[];const out=[];for(let k=0;k<row.length;k+=2){const lo=Math.max(row[k],m.tip[0]-52),hi=Math.min(row[k+1],m.tip[0]+52);if(hi>lo)out.push(lo,hi);}return out;});
  q.claws[side]={...part,spans};
 }
}
globalThis.BOF_BOSS_ANIMATION_1109=BA119;
// Both legacy float owners run outside the melee helper. Remove their
// displacement while planted, before space gravity offsets hulls or ordnance.
function ba119Planted(b){if(!ba119Blue(b)||b._hammer.c25Knock)return null;const h=b._hammer;
 const P=h.c27Combo||h._hf22StormPair||(h.state==='recover'&&h._hj22Pair);
 return P?.ba119?P.origin:['recover','giant_sweep'].includes(h.state)?h.ba119Landing:null;}
BA119.base.state=hammerState;
hammerState=function(b,s){const out=BA119.base.state.apply(this,arguments);if(ba119Blue(b)&&['recover','giant_sweep'].includes(s))b._hammer.ba119Landing={x:b.x,y:b.y};return out;};
BA119.base.hammerTick=hammerBossTick;
hammerBossTick=function(b,dt){const out=BA119.base.hammerTick.apply(this,arguments),root=ba119Planted(b);
 if(root){b.x=root.x;b.y=root.y;b._drawY=b.y;b._c43Float={x:0,y:0};}return out;};
BA119.base.gravityEnd=sg26End;
sg26End=function(b,q){if(q&&ba119Planted(b)){q.next=0;q.ba119ResumeAt=q.clock;}
 else if(q?.ba119ResumeAt!=null){const u=clamp((q.clock-q.ba119ResumeAt)/.30,0,1);q.next*=u;if(u>=1)delete q.ba119ResumeAt;}
 return BA119.base.gravityEnd.apply(this,arguments);};
