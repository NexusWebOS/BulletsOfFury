"use strict";
/* Measured physical swing frames, one clean corrupted actor across every bank.
   Native attack clocks, damage, retinas, hit feedback and recovery retain ownership. */
const H22={base:{blue:ha21Blue,frame:ha21Frame,pose:hb20Pose,pick:hb20Pick,pickup:hb20Pickup,landing:ha21Landing,load:stageLoadBegin,warm:v18Warm,keys:v18Keys,native:v19NativeTick,world:hb20World,melee:hb20Melee,clip:v18Clip,gun:hb20GunMount},draws:{}};
for(const S of Object.values(H22_ART.sheets))XART._src[S.key]=S.path;
for(const [name,rows]of Object.entries(H22_ART.banks)){
 for(const a of rows)BOFX.cells[a.key]=[a.sheet,...a.cell];
 if(name.startsWith('blue_'))HA21_ART.banks[name]=rows;
}
HM10_ART.swing_right=H22_ART.banks.blue_counter_right;HM10_ART.swing_left=H22_ART.banks.blue_counter_left;
function h22Keys(n){return Object.entries(H22_ART.sheets).filter(([name])=>n===5?name.startsWith('h22_blue_'):n===8?name.startsWith('h22_corrupt_'):false).map(([,S])=>S.key);}
stageLoadBegin=function(n,keys){return H22.base.load.call(this,n,[...(keys||[]),...h22Keys(n)]);};
v18Keys=function(){return [...H22.base.keys(),...h22Keys(8)];};
v18Warm=function(){const r=H22.base.warm();return h22Keys(8).map(k=>XART.rdy(k)).every(Boolean)&&r;};
function h22Frame(name,value){const rows=H22_ART.banks[name];return rows?.[Math.min(rows.length-1,Math.max(0,Math.floor(value)))];}
function h22Pose(name,value,k=1.45,rot=0){const a=h22Frame(name,value);if(!a||!XART.rdy(a.key))return null;H22.draws[name]=(H22.draws[name]||0)+1;return{a,k,rot,kind:name};}
function h22Blue(b,frame,k=1.75){const armor=fr27Armor(b),name='blue_slam'+(armor?.hp>0&&armor.activated?'_armor':'');return h22Pose(name,frame,k);}
ha21Blue=function(b){const h=b?._hammer;if(!h||b.dead||b._gp4Host)return H22.base.blue.apply(this,arguments);const s=h.state,t=h.t||0,M=H22_ART.blueSlam,music=b._hammerTime||b._hama;
 if(music&&music.mode!=='attack'||hf19Recovery(b)&&!['recharge1002','recover','back','giant_recover'].includes(s))return H22.base.blue.apply(this,arguments);
 if(h.hb20Pickup){const z=h.hb20Pickup.t,frame=z<.8?0:z<1.78?lerp(0,M.strikeEnd,clamp((z-.8)/.98,0,1)):lerp(M.strikeEnd,H22_ART.banks.blue_slam.length-1,clamp((z-1.78)/1.07,0,1));return h22Blue(b,frame);}
 if(s==='storm_warn')return h22Blue(b,lerp(0,M.windEnd,clamp(t/(hammerFurious()?.9:hammerHard()?1:1.15),0,1)));
 if(s==='storm_slam')return h22Blue(b,lerp(M.windEnd,M.strikeEnd,clamp(t/(hammerFurious()?.46:hammerHard()?.52:.6),0,1)));
 if(s==='storm_split')return h22Blue(b,lerp(M.recoverStart,H22_ART.banks.blue_slam.length-1,clamp(t/.75,0,1)));
 if(s==='warn')return h22Blue(b,lerp(0,M.windEnd,clamp(t/(hammerFurious()?.58:1.2),0,1)));
 if(s==='leap')return h22Blue(b,lerp(M.windEnd,M.strikeEnd,clamp(t/(hammerFurious()?.24:.48),0,1)));
 if(s==='recover')return h22Blue(b,lerp(M.strikeEnd,H22_ART.banks.blue_slam.length-1,clamp(t/hammerRecoverDuration(),0,1)));
 if(['giant_windup','giant_rise','giant_warn','giant_dive','giant_sweep','giant_recover'].includes(s)){
  const frame=s==='giant_dive'?lerp(M.windEnd,M.strikeEnd,clamp(t/.52,0,1)):s==='giant_sweep'?M.strikeEnd:s==='giant_recover'?lerp(M.recoverStart,H22_ART.banks.blue_slam.length-1,clamp(t/.8,0,1)):lerp(0,M.windEnd,clamp(t/(s==='giant_warn'?1.1:s==='giant_rise'?1:.48),0,1));
  return h22Blue(b,frame,1.75*hammerDepthScale(b));
 }
 return H22.base.blue.apply(this,arguments);
};
ha21Landing=function(b,target,kind,frame,scale=1.75){if(b._gp4Host||!['slam','jump'].includes(kind))return H22.base.landing.apply(this,arguments);const a=h22Frame('blue_slam',H22_ART.blueSlam.strikeEnd);return{x:target.x-(a.tip[0]-a.pivot[0])*scale,y:target.y-(a.tip[1]-a.pivot[1])*scale};};
hb20Pick=function(name,t=0,d=1,loop=false){const bank=H22_ART.banks[name];if(bank)return b20Frame(bank,t,d,loop);return H22.base.pick.apply(this,arguments);};
hb20Pose=function(b){const Q=hb20State(b);if(!Q)return H22.base.pose.apply(this,arguments);const A=Q.action,t=A?.t||0,u=t-(A?.tell||0);let name=Q.rage?'corrupt_unarmed':'corrupt_idle',v=Q.rage?1:0,rot=0,k=1.45*(Q.scale||1);
 let absolute=null;const M=H22_ART.corruptSlam;
 if(A){
  if(A.type==='skystrike'){name='corrupt_slam';absolute=u<0?M.windEnd:u<.9?lerp(M.windEnd,M.strikeEnd,clamp(u/.60,0,1)):lerp(M.strikeEnd,H22_ART.banks.corrupt_slam.length-1,clamp((u-.9)/.4,0,1));}
  else if(A.type==='pickup'){name='corrupt_slam';absolute=t<.8?0:t<1.78?lerp(0,M.strikeEnd,clamp((t-.8)/.98,0,1)):lerp(M.strikeEnd,H22_ART.banks.corrupt_slam.length-1,clamp((t-1.78)/.77,0,1));}
  else if(A.type==='side'){name='corrupt_side';v=u<0?t/A.tell*.30:.30+clamp(u/.80,0,1)*.70;}
  else if(A.type==='throw'){name='corrupt_throw';v=u<0?t/A.tell*.55:.55+clamp(u/.5,0,1)*.45;}
  else if(A.type==='ball'){name='corrupt_ball';v=u<0?clamp(t/A.tell,0,1):1;if(u>=0)rot=u*TAU*1.6;const end=H22_ART.banks.corrupt_ball.at(-1),diam=Math.max(end.bounds[2]-end.bounds[0],end.bounds[3]-end.bounds[1]);k=lerp(1.45,110/diam,v)*(Q.scale||1);}
  else if(A.type==='spin'){name='corrupt_spin';v=u<0?0:(u/.7)%1;}
  else if(A.type==='charge'){name='corrupt_charge';v=clamp(t/A.tell,0,1);}
  else if(A.type==='shield'){name='corrupt_shield';v=clamp(t/A.tell,0,1);}
  else if(A.type==='gun'){name=A.dir<0?'corrupt_gun_left':'corrupt_gun';v=u<0?.44:.44+((u/.65)%1)*.55;}
  else if(A.type==='break'){name='corrupt_break';v=t<1.35?t/1.35*.66:.66+clamp((t-1.35)/3.25,0,1)*.34;}
  else if(A.type==='luminaire'){name='corrupt_break';v=1;}
  else if(A.type==='fire'){name='corrupt_fire';v=Math.max(.25,clamp(t/A.duration,0,1));}
  else if(A.type==='punch'){const second=u>=.60,clock=second?u-.60:u;name=second?'corrupt_punch_left':'corrupt_punch';v=clock<0?0:clock<.26?clamp(clock/.26,0,1):1-clamp((clock-.26)/.24,0,1);}
  else if(A.type==='fists'){name='corrupt_fists';v=u<0?lerp(.2,.5,clamp(t/A.tell,0,1)):.5+clamp(u/.25,0,1)*.5;}
  else if(A.type==='dance'){name='corrupt_dance';v=(Math.max(0,u)/1.8)%1;}
 }
 const bank=H22_ART.banks[name];return h22Pose(name,absolute==null?clamp(v,0,.99999)*bank.length:absolute,k,rot);
};
hb20Pickup=function(b,corrupt=false){const C=H22.base.pickup.apply(this,arguments),a=h22Frame(corrupt?'corrupt_slam':'blue_slam',corrupt?H22_ART.corruptSlam.strikeEnd:H22_ART.blueSlam.strikeEnd);
 C.box=hb20World(a,a.tip,C.station,corrupt?1.45:1.75);return C;
};
hb20World=function(a,p,b,k,rot){
 // Legacy punch contacts are source-space landmarks. Preserve the new common
 // transparent pad when those same source coordinates are used by native AI.
 if(a?._h22&&a.bank?.startsWith('corrupt_punch')&&(p[0]===168||p[0]===88)&&p[1]===120){p=a.handR;if(H22.inNative===b)b={...b,...h22PunchPosition(b,hb20State(b).action)};}
 if(a?._h22&&a.w===320&&![a.tip,a.pivot,a.muzzle,a.handL,a.handR].includes(p)&&!a._h22Tool)p=[p[0]+32,p[1]+32];
 return H22.base.world.call(this,a,p,b,k,rot);
};
hb20Melee=function(b,A,from,to,r){if(hb20Own(b)&&A.type==='spin'){const pose=hb20Pose(b),at=hb20World(pose.a,pose.a.tip,b,pose.k,pose.rot),prev=A._h22Blade||at;A._h22Blade=at;return H22.base.melee.call(this,b,A,prev,at,r);}return H22.base.melee.apply(this,arguments);};
hb20GunMount=function(b,A){if(!hb20Own(b))return H22.base.gun.apply(this,arguments);const q=hb20Pose(b);if(!q?.a?.muzzle)return H22.base.gun.apply(this,arguments);return{...hb20World(q.a,q.a.muzzle,b,q.k,q.rot),a:q.a.gunAngle+q.rot};};
function h22PunchPosition(b,A){const Q=hb20State(b),scale=1.45*(Q.scale||1),right=H22_ART.banks.corrupt_punch.at(-1),left=H22_ART.banks.corrupt_punch_left.at(-1),first={x:A.target.x-(right.handR[0]-right.pivot[0])*scale,y:A.target.y-(right.handR[1]-right.pivot[1])*scale},second={x:A.target.x-(left.handR[0]-left.pivot[0])*scale,y:A.target.y-(left.handR[1]-left.pivot[1])*scale},u=A.t-A.tell;
 if(u<.60){const v=u<0?clamp(A.t/A.tell,0,1)*.15:.15+v19Ease(u/.32)*.85;return{x:lerp(A.origin.x,first.x,v),y:lerp(A.origin.y,first.y,v)};}const v=v19Ease((u-.60)/.22);return{x:lerp(first.x,second.x,v),y:lerp(first.y,second.y,v)};
}
v19NativeTick=function(b,dt){const own=hb20Own(b),A=own&&hb20State(b)?.action;let r;const previous=H22.inNative;H22.inNative=b;try{r=H22.base.native.apply(this,arguments);}finally{H22.inNative=previous;}
 if(own&&A?.type==='fists'&&hb20State(b)?.action===A){const q=hb20Pose(b),groundOffset=(250-q.a.pivot[1])*q.k,u=A.t-A.tell;
  if(u<.25)b.y+=(108-groundOffset)*v19Ease(clamp(A.t/A.tell,0,1));else b.y=A.target.y-groundOffset;
  b._drawY=b.y;const p=gd4Create(b,8).p;p.x=b.x;p.y=b.y;
 }else if(own&&A?.type==='punch'&&hb20State(b)?.action===A){Object.assign(b,h22PunchPosition(b,A));b._drawY=b.y;const p=gd4Create(b,8).p;p.x=b.x;p.y=b.y;}
 return r;
};
v18Clip=function(name,t,d,x,y,size,reverse){if(name!=='morph_hammer')return H22.base.clip.apply(this,arguments);const bank=H22_ART.banks.corrupt_charge,u=clamp(t/d,0,.99999),a=bank[Math.floor((reverse?1-u:u)*(bank.length-1))];return b20Image(a,x,y,size/320,0,0);};
globalThis.BOF_HAMMER_CORRECTION=H22;
