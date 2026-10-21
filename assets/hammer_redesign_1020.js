"use strict";
/* PixelLab Hammer acting and Dracodia's code-weapon / permanent fire finale.
   Stage5 keeps its existing combat clocks. Stage8 owns a separate attack book. */
const HB20={base:{draw:hammerBossDraw,tick:hammerBossTick,phase:hammerPhaseTwoStart,head:hammerHeadPoint,mount:hammerBlasterMount,rig:v19HammerRig,at:v19AtRect,donor:v19DonorDraw,native:v19NativeTick,enter:v18Enter,hit:modularHit,targets:retinaBossTargets,contact:target17BossContact,clear:v18Clear,load:stageLoadBegin,keys:v18Keys,warm:v18Warm},painting:null,tags:new WeakMap(),draws:{}};
b20Register(HB20_ART);
const HB20_PICKUP={box:'hb20_chaingun_crate_exclusive',icon:'hb20_chaingun_icon_exclusive'};
XART._src[HB20_PICKUP.box]='assets/game/shared/pickups/hammer_chaingun_1020/crate.webp';
XART._src[HB20_PICKUP.icon]='assets/game/shared/pickups/hammer_chaingun_1020/icon.webp';
// The existing counter solver reads measured head locations from these frames.
HM10_ART.swing_right=HB20_ART.banks.counter_right;HM10_ART.swing_left=HB20_ART.banks.counter_left;
const hb20AllKeys=()=>[...b20Keys(HB20_ART.banks),...Object.values(HB20_PICKUP)];
v18Keys=function(){return [...HB20.base.keys(),...hb20AllKeys()];};
v18Warm=function(){const before=HB20.base.warm();return Object.values(HB20_PICKUP).map(k=>XART.rdy(k)).every(Boolean)&&b20Ready(HB20_ART.banks)&&before;};
stageLoadBegin=function(n,keys){if([5,8].includes(n))for(const cue of ['hammerImpact','hammerChaingun','shieldBossAbsorb','furnaceFlameIgnite','bossWeaponCharge'])Snd.prepare(cue);return HB20.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?[...hb20AllKeys()]:[])]);};
function hb20Own(b){return v19Native(b)&&b._r30.v18.form===8;}
function hb20State(b){return j3State(b).hb20;}
function hb20Pick(name,t=0,d=1,loop=false){return b20Frame(HB20_ART.banks[name],t,d,loop);}
function hb20World(a,p,b,k=1.4,rot=0){const x=(p[0]-a.pivot[0])*k,y=(p[1]-a.pivot[1])*k;return{x:b.x+x*Math.cos(rot)-y*Math.sin(rot),y:b.y+x*Math.sin(rot)+y*Math.cos(rot)};}
function hb20Blue(b){const h=b._hammer,s=h.state,C=h.hc11Counter;let a,k=1.4,rot=0;
 if(C)return{a:HM10_ART[C.bank][hc11Frame(C)],k:HM10.bodyScale*C.scale,rot:C.angle,kind:'counter'};
 if(h.hb20Pickup){const q=h.hb20Pickup;a=hb20Pick('blue_slam',clamp((q.t-.8)/1.4,0,1),1);}
 else if(['chain_warn','chaingun','chain_cool','chaingun_draw'].includes(s)&&!h.chainDestroyed)a=hb20Pick('blue_gun',h.t,.56,s==='chaingun');
 else if(['curl','ball','uncurl'].includes(s))return null; // Native blue spikeball is explicitly retained.
 else if(['flyby','return','unfold'].includes(s))a=hb20Pick('blue_entry',s==='unfold'?h.t:0,2);
 else if(b._hammerTime?.mode==='intro')a=hb20Pick('blue_entry',(b._hammerTime.clock||0)/Math.max(1,ht27IntroEnd())*2,2);
 else if(hf19Recovery(b)){const q=hf19Pick(b);if(q)return{...q,rot:0};a=hb20Pick('blue_empty');}
 else if(h.throw||h.hammerDestroyed)a=hb20Pick('blue_empty');
 else if(s==='spin'||s==='revenge_charge'||s==='hammer_catch')a=hb20Pick('blue_throw',h.t,s==='spin'?HAMMER_SPIN_TIME:1.2);
 else if(['whirlwind','whirl_warn','whirl_turn','fr_twirl'].includes(s))a=hb20Pick('blue_spin',h.t,.8,true);
 else if(/dance/.test(s)||b._hammerTime&&b._hammerTime.mode!=='attack'||b._hama&&b._hama.mode!=='attack')a=hb20Pick('blue_dance',h.t,1.5,true);
 else if(['warn','leap','recover','giant_windup','giant_rise','giant_warn','giant_dive','giant_sweep','storm_warn','storm_slam'].includes(s)){
  let u=s==='warn'?clamp(h.t/(hammerFurious()?.58:1.2),0,1)*.45:s==='leap'?.45+clamp(h.t/(hammerFurious()?.27:.52),0,1)*.28:s==='recover'?.73+clamp(h.t/hammerRecoverDuration(),0,1)*.27:s==='giant_dive'?.45+clamp(h.t/.52,0,1)*.28:s==='giant_sweep'?.73:.36;
  a=hb20Pick('blue_slam',u,1);if(s.startsWith('giant_'))k*=hammerDepthScale(b);
 }else if(['storm_raise','storm_rebuild','shield','fr_activation','spell','spell_blast','mega_charge','mega_beam','nova_charge','nova_release'].includes(s))a=hb20Pick('blue_slam',.35+Math.sin(h.t*3)*.035,1);
 else a=hb20Pick('blue_idle');
 return a?{a,k,rot,kind:s}:null;
}
// Suppress only retired actor plates while the native Stage5 warning/effect draw
// runs. Shared effects, flying hammers, retinas and the retained spikeball remain.
const hb20Get=XART.get,hb20Tint=xartTint,hb20Blit=ctx.drawImage;
XART.get=function(key){const im=hb20Get.apply(this,arguments);if(im)HB20.tags.set(im,key);return im;};
xartTint=function(key){const im=hb20Tint.apply(this,arguments);if(im)HB20.tags.set(im,key);return im;};
function hb20Retired(key){return /^(hb20_counter_|hf19_(chaingun|recovery)|hm10_(shield_form|shield_wall|core|swing_)|pt11_hammer_core|ht27_boss|hama_boss|fr27_chromium_actions)/.test(key)||/^arch_(idle|master|leap_strike|ship_transform|twirl_throw|chaingun_detach_fire|chaingun_break_enrage|blaster_body|blaster_gun|orbital_sweep|whirlwind|hammer_overhead|hammer_throw|storm_charge|combat|spell_raise|stun|arsenal_cast)/.test(key);}
ctx.drawImage=function(im){if(HB20.painting&&hb20Retired(HB20.tags.get(im)||''))return;return hb20Blit.apply(this,arguments);};
hammerBossDraw=function(b){if(!b?._hammer||b._gp4Host||b.dead)return HB20.base.draw.apply(this,arguments);const q=hb20Blue(b),old=HB20.painting;
 if(q)HB20.painting=b;try{HB20.base.draw.apply(this,arguments);}finally{HB20.painting=old;}
 if(q){b20Image(q.a,b.x,b.y,q.k,q.rot,b.flash||0);HB20.draws[q.kind]=(HB20.draws[q.kind]||0)+1;hm10WallDraw(b);
  if(q.kind==='chaingun'&&b._hammer.chainMuzzle>0){const m=hammerBlasterMount(b);wm26Draw(ctx,'chaingun',m.x,m.muzzleY,Math.PI/2,1-b._hammer.chainMuzzle/.09,48);}}
 if(b._hammer.hb20Pickup)hb20PickupDraw(b,b._hammer.hb20Pickup,false);
};
hammerHeadPoint=function(b){if(!b?._hammer||b._gp4Host||b._hammer.hc11Counter||b._hammer.throw)return HB20.base.head.apply(this,arguments);const q=hb20Blue(b);return q?.a.tip?hb20World(q.a,q.a.tip,b,q.k,q.rot):HB20.base.head.apply(this,arguments);};
hammerBlasterMount=function(b){const m=HB20.base.mount.apply(this,arguments);if(!b?._hammer||b._gp4Host)return m;return{...m,x:b.x,y:b.y+55,muzzleY:b.y+140};};
function hb20Pickup(b,corrupt=false){const a=hb20Pick(corrupt?'corrupt_slam':'blue_slam',corrupt?.52:.7,1),k=corrupt?1.1:1.4,station={x:clamp(b.x,camLeftX()+160,camRightX()-160),y:clamp(b.y,viewTopY()+130,viewTopY()+viewH()*.45)},box=hb20World(a,a.tip||[77,180],station,k);return{t:0,origin:{x:b.x,y:b.y},station,box,corrupt,hit:false,obtained:false};}
hammerPhaseTwoStart=function(b){if(b._gp4Host||b._hammer.hb20PickupDone)return HB20.base.phase.apply(this,arguments);const h=b._hammer;h.hb20Pickup=hb20Pickup(b);h.phasePending=false;h.throw=null;h.hammerDestroyed=false;h.hammerHP=Math.max(1,h.hammerHP);hammerState(b,'hb20_pickup');b._noHit=false;b20Cue('bossWeaponCharge');b20Log('hammer-crate-spawn',{stage:5});};
function hb20PickupTick(b,C,dt){C.t+=dt;const u=v19Ease(C.t/.8);b.x=lerp(C.origin.x,C.station.x,u);b.y=lerp(C.origin.y,C.station.y,u);
 if(!C.hit&&C.t>=1.78){C.hit=true;explode(C.box.x,C.box.y,54,C.corrupt?'purple':'blue');b20Cue('hammerImpact');b20Log('hammer-crate-struck',{stage:C.corrupt?8:5});}
 if(!C.obtained&&C.t>=2.55){C.obtained=true;markHit(b,.25);b20Cue('pickup');b20Log('hammer-chaingun-lv1-obtained',{stage:C.corrupt?8:5,icon:'micon_chaingun_1',art:HB20_PICKUP.icon});}
 return C.t>=2.85;
}
function hb20PickupDraw(b,C,corrupt){
 if(!C.hit&&XART.rdy(HB20_PICKUP.box)){const size=corrupt?62:56;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(HB20_PICKUP.box),C.box.x-size/2,C.box.y-size/2,size,size);ctx.restore();}
 else if(C.hit&&!C.obtained&&XART.rdy(HB20_PICKUP.icon)){const u=clamp((C.t-1.78)/.77,0,1),x=lerp(C.box.x,b.x,u),y=lerp(C.box.y,b.y,u)-Math.sin(u*Math.PI)*45;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(HB20_PICKUP.icon),x-18,y-18,36,36);ctx.restore();}
}

hammerBossTick=function(b,dt){const h=b?._hammer;if(!h?.hb20Pickup)return HB20.base.tick.apply(this,arguments);h.t+=dt;b.flash=Math.max(0,(b.flash||0)-dt);if(hb20PickupTick(b,h.hb20Pickup,dt)){h.hb20Pickup=null;h.hb20PickupDone=true;HB20.base.phase(b);hammerChainStart(b);markHit(b,.18);}};
function hb20Init(b){const J=j3State(b),N=b._r30.v18;let Q=J.hb20;if(!Q)Q=J.hb20={seq:0,age:0,rage:false,gunSeen:false,broken:false,gunHP:Math.round(J.max[8]*.15),hammerHP:Math.round(J.max[8]*.22),action:null,waves:[],fire:[],scale:1,angle:0,shield:0};
 Q.parts??=[b20Part(b,'core',J.hp[8],'Demonic code heart'),b20Part(b,'hammer',Q.hammerHP,'Two-handed code hammer'),b20Part(b,'chaingun',Q.gunHP,'Held chaingun level1')];b.parts=Q.parts;J.modules[8]=b.parts;b.hp=J.hp[8];b.maxhp=J.max[8];Q.parts[0].hp=b.hp;Q.parts[1].destroyed=Q.broken||Q.rage;Q.parts[2].destroyed=true;Q.scale=1;Q.angle=0;Q.action=null;Q.cool=.65;Q.age=0;Q.waves=[];Q.fire=[];N.swipe=null;b.name=Q.rage?'DRACODIA — UNBOUND FIRE':'DRACODIA — CODE HAMMER';return Q;}
v18Enter=function(b){const r=HB20.base.enter.apply(this,arguments);if(hb20Own(b))hb20Init(b);return r;};
function hb20Start(b,type){const Q=hb20State(b),rank=b20Rank(),T=[1.55,1.3,1.1,.95][rank],ship=b20Target(b),target={x:clamp(ship.x,camLeftX()+65,camRightX()-65),y:clamp(ship.y,viewTopY()+120,viewTopY()+viewH()-70)},book=Q.rage?['punch','fists','punch','fists']:['skystrike','shield','side','throw','ball','charge','spin','dance'];
 const A=Q.action={type:type||book[Q.seq++%book.length],t:0,tell:T,target,origin:{x:b.x,y:b.y},hit:new Set(),next:0,n:0};Q.scale=1;Q.angle=0;
 if(A.type==='skystrike'){A.tell=[1.9,1.65,1.45,1.3][rank];A.duration=A.tell+1.75;}
 else if(A.type==='pickup'){A.crate=hb20Pickup(b,true);A.duration=2.85;}
 else if(A.type==='break'){A.tell=0;A.duration=4.6;Q.broken=true;Q.gunSeen=true;Q.parts[1].destroyed=true;Q.parts[2].destroyed=true;Q.shield=4.65;}
 else if(A.type==='luminaire'){A.tell=[2.65,2.35,2.1,1.9][rank];A.duration=A.tell+.65;A.safe=Q.safe;A.area={left:camLeftX(),top:viewTopY(),w:viewW(),h:viewH()};A.coreFrom={x:b.x,y:b.y-45};}
 else if(A.type==='fire'){A.tell=0;A.duration=1.9;Q.rage=true;Q.broken=true;Q.parts[1].destroyed=true;b.name='DRACODIA — UNBOUND FIRE';}
 else if(A.type==='ball'){A.duration=T+3.1;A.dir=target.x>=b.x?1:-1;A.from={x:b.x,y:b.y};A.to={x:A.dir>0?camRightX()-60:camLeftX()+60,y:viewTopY()+viewH()*.76};}
 else if(A.type==='gun'){A.duration=T+3.5;A.dir=b.x>(camLeftX()+camRightX())/2?-1:1;Q.parts[2].destroyed=false;}
 else A.duration=T+(['charge','shield','dance'].includes(A.type)?2.1:1.3);
 b20Cue(['fire','break','luminaire'].includes(A.type)?'shadowCharge':'bossWeaponCharge');b20Log('code-hammer-start',{type:A.type,tell:A.tell,rage:Q.rage});return A;
}
function hb20Pose(b){const Q=hb20State(b),A=Q.action,t=A?.t||0,u=t-(A?.tell||0);let name=Q.rage?'corrupt_unarmed':'corrupt_idle',clock=0,d=1,loop=false,k=1.8,rot=Q.angle;
 if(A){if(A.type==='break'){name='corrupt_break';clock=t;d=4.6;}
  else if(A.type==='fire'){name='corrupt_fire';clock=t;d=A.duration;}
  else if(A.type==='luminaire'){name='corrupt_unarmed';}
  else if(A.type==='pickup'){name='corrupt_slam';clock=clamp((t-.8)/1.4,0,1);}
  else if(A.type==='gun'){name=A.dir<0?'corrupt_gun_left':'corrupt_gun';clock=Math.max(0,u);d=.75;loop=u>=0;k=1.45;}
  else if(A.type==='punch'){name='corrupt_punch';clock=u<0?0:Math.min(1,u/1.25);k=1.55;}
  else if(A.type==='fists'){name='corrupt_fists';clock=u<0?Math.min(.18,t/A.tell*.18):.18+clamp(u/1.3,0,1)*.82;k=1.55;}
  else if(A.type==='ball'){name='corrupt_ball';clock=Math.max(0,u);d=.75;loop=true;k=1.35;}
  else if(A.type==='spin'){name='corrupt_spin';clock=Math.max(0,u);d=1.2;loop=u>=0;}
  else if(A.type==='dance'){name='corrupt_dance';clock=Math.max(0,u);d=1.8;loop=u>=0;}
  else if(A.type==='charge'||A.type==='shield'){name='corrupt_charge';clock=t;d=A.duration;}
  else if(A.type==='side'){name='corrupt_side';clock=u<0?t/A.tell*.18:.18+clamp(u/1.3,0,1)*.82;}
  else if(A.type==='skystrike'){name='corrupt_slam';clock=u<0?.12:.12+clamp(u/1.05,0,1)*.88;}
  else if(A.type==='throw'){name=u<0?'corrupt_spin':'corrupt_unarmed';clock=t;d=A.tell;}
 }
 const a=hb20Pick(name,clock,d,loop)||hb20Pick('corrupt_idle');return{a,k:k*Q.scale,rot,kind:name};
}
v19HammerRig=function(b){if(!hb20Own(b)||!hb20State(b))return HB20.base.rig.apply(this,arguments);const Q=hb20State(b),q=hb20Pose(b),core=Q.parts[0],v=b20Piece(core,q.a,b,q.rot,q.k,'core',1),out=[v],A=Q.action;
 if(!Q.broken&&!Q.rage&&A?.type!=='gun'&&A?.type!=='ball'){let at=hb20World(q.a,q.a.tip||[70,150],b,q.k,q.rot);if(A?.type==='throw'&&A.t>A.tell)at=hb20ToolAt(b,A);const p=Q.parts[1];if(!p.destroyed)out.push({...v,p,x:at.x,y:at.y,w:58,h:58,z:5,layer:'hammer',spec:{role:'hammerHead',hidden:true},_hb20Target:true});}
 if(A?.type==='gun'&&!Q.parts[2].destroyed){const muzzle=hb20GunMount(b,A),at={x:muzzle.x-A.dir*18,y:muzzle.y-8};out.push({...v,p:Q.parts[2],x:at.x,y:at.y,w:74,h:68,z:5,layer:'chaingun',spec:{role:'weapon',hidden:true},_hb20Target:true});}
 return out;
};
v19AtRect=function(v,x,y){if(v._hb20Target)return Math.abs(x-v.x)<v.w/2&&Math.abs(y-v.y)<v.h/2;return HB20.base.at.apply(this,arguments);};
function hb20ToolAt(b,A){const u=clamp((A.t-A.tell)/1.3,0,1),x=lerp(A.origin.x,A.target.x,Math.sin(u*Math.PI)),y=lerp(A.origin.y,A.target.y,Math.sin(u*Math.PI));return{x,y};}
function hb20GunMount(b,A){const pose=hb20Pose(b),p=pose.a.muzzle||(A.dir>0?[183,152]:[73,152]),at=hb20World(pose.a,p,b,pose.k,pose.rot);return{...at,a:A.dir>0?.57:Math.PI-.57};}
function hb20Wave(b,Q,at,fire=false){for(const dir of [-1,1])Q.waves.push({x:at.x,y:at.y,oldX:at.x,t:0,dir,speed:[175,195,220,245][b20Rank()],hit:new Set(),fire});b20Cue('hammerImpact');b20Log('code-hammer-ground-waves',{x:at.x,y:at.y,fire});}
function hb20Melee(b,A,from,to,r=28){b20HitSegment(b,from,to,r,A.type==='punch'?'Dracodia fire punch':'Dracodia code hammer',A.hit);}
function hb20Finish(b,A){const Q=hb20State(b);Q.shield=0;Q.scale=1;Q.angle=0;Q.action=null;Q.cool=[1.15,.95,.8,.68][b20Rank()];b._noHit=false;
 if(A.type==='pickup'){Q.gunSeen=true;hb20Start(b,'gun');markHit(b,.18);}
 else if(A.type==='break'){const p=b20Target(b),current=hb20Quadrant(p.x,p.y);Q.safe=current^(Math.random()<.5?1:2);hb20Start(b,'luminaire');}
 else if(A.type==='luminaire')hb20Start(b,'fire');
 else if(A.type==='gun'){Q.parts[2].destroyed=true;markHit(b,.18);}
 b20Log('code-hammer-finish',{type:A.type,rage:Q.rage});
}
function hb20Quadrant(x,y,area){const a=area||{left:camLeftX(),top:viewTopY(),w:viewW(),h:viewH()};return(x>=a.left+a.w/2?1:0)+(y>=a.top+a.h/2?2:0);}
function hb20Luminaire(b,A){if(A.t<A.tell)return;const a=A.area;for(const seat of seatList())withSeat(seat,()=>{if(player.x<a.left||player.x>a.left+a.w||player.y<a.top||player.y>a.top+a.h)return;if(!A.hit.has(seat)&&!player.dead&&!player.out&&player.invuln<=0&&hb20Quadrant(player.x,player.y,a)!==A.safe){A.hit.add(seat);run.shield=0;playerHit('Code-core luminaire');b20Log('luminaire-hit',{seat});}});}
v19NativeTick=function(b,dt){if(!hb20Own(b)||!hb20State(b))return HB20.base.native.apply(this,arguments);const Q=hb20State(b),N=b._r30.v18,rank=b20Rank();Q.age+=dt;N.donorAge=(N.donorAge||0)+dt;Q.cool=Math.max(0,Q.cool-dt);Q.shield=Math.max(0,Q.shield-dt);Q.gateFlash=Math.max(0,(Q.gateFlash||0)-dt);b._noHit=false;
 if(!Q.action&&Q.cool<=0){if(!Q.gunSeen&&b.hp<=b.maxhp*.66)hb20Start(b,'pickup');else if(!Q.broken&&b.hp<=b.maxhp*.29)hb20Start(b,'break');else hb20Start(b);}
 const A=Q.action;if(A){A.t+=dt;const u=A.t-A.tell;
  if(A.tell>0&&A.t<=A.tell)combatWarningTick(b,'hb20-'+Q.seq+'-'+A.type,A.t,A.tell);
  if(A.type==='pickup'){const done=hb20PickupTick(b,A.crate,dt);if(done)A.t=A.duration;}
  else if(A.type==='skystrike'){if(A.t<.6){const v=A.t/.6;Q.scale=lerp(1,.25,v);b.y=lerp(A.origin.y,viewTopY()-170,v);b._noHit=true;}
   else if(u<0){Q.scale=.25;b.x=A.target.x;b.y=viewTopY()-170;b._noHit=true;}
   else if(u<.65){const v=v19Ease(u/.65);Q.scale=lerp(.25,1.2,v);const q=hb20Pick('corrupt_slam',.70,1),at=hb20World(q,q.tip,b,1.1*1.2);b.x=lerp(A.target.x,A.target.x-(at.x-b.x),v);b.y=lerp(viewTopY()-170,A.target.y-(at.y-b.y),v);b._noHit=v<.7;}
   if(u>=.65&&!A.impact){A.impact=true;hb20Melee(b,A,A.target,A.target,46);hb20Wave(b,Q,A.target);explode(A.target.x,A.target.y,100,'purple');shake=Math.max(shake,10);}
  }
  else if(A.type==='shield'){if(u>=0)Q.shield=.15;}
  else if(A.type==='break'){Q.shield=.15;if(A.t>1.35&&!A.broken){A.broken=true;b20Cue('shieldBreakCombat');b20Log('code-hammer-knee-break');}}
  else if(A.type==='luminaire')hb20Luminaire(b,A);
  else if(A.type==='fire'){Q.rage=true;Q.parts[1].destroyed=true;if(!A.ignite){A.ignite=true;b20Cue('furnaceFlameIgnite');}}
  else if(A.type==='ball'&&u>=0){const v=clamp(u/3.1,0,1),triangle=v<.5?v*2:2-v*2;b.x=lerp(A.from.x,A.to.x,triangle);b.y=lerp(A.from.y,A.to.y,triangle);if(A.previous)hb20Melee(b,A,A.previous,b,48);A.previous={x:b.x,y:b.y};}
  else if(A.type==='throw'&&u>=0){const at=hb20ToolAt(b,A);if(A.previous)hb20Melee(b,A,A.previous,at,28);A.previous=at;if(!A.launched){A.launched=true;b20Cue('hammerThrow');}}
  else if(A.type==='gun'&&u>=0){if(Q.parts[2].destroyed){A.t=A.duration;}else{b.x=clamp(A.origin.x+Math.sin(u*2)*viewW()*.28,camLeftX()+105,camRightX()-105);if(u>=A.next&&u% .72<.45){A.next=u+[.20,.17,.14,.12][rank];const m=hb20GunMount(b,A);for(const d of [-.035,.035]){const q=eShootT(m.x,m.y,m.a+d,4.8+rank*.35,'mg',{w:6,h:15});if(q)q._hb20Owner=b;}A.muzzle=.08;if(!(A.sfx>u)){A.sfx=u+1.3;b20Cue('hammerChaingun');}}A.muzzle=Math.max(0,(A.muzzle||0)-dt);}}
  else if(A.type==='side'&&u>=0&&u<.8){const pose=hb20Pose(b),at=hb20World(pose.a,pose.a.tip||[70,150],b,pose.k);if(A.previous)hb20Melee(b,A,A.previous,at,28);A.previous=at;}
  else if(A.type==='spin'&&u>=0){const at={x:b.x+Math.cos(u*TAU)*100,y:b.y+Math.sin(u*TAU)*100};if(A.previous)hb20Melee(b,A,A.previous,at,26);A.previous=at;}
  else if(A.type==='charge'&&u>=0){if(u>=A.next&&A.n<2){A.n++;A.next=u+.65;const origin={x:b.x,y:b.y+20},rays=12+rank*2,gap=Math.atan2(A.target.y-origin.y,A.target.x-origin.x)+Math.PI;for(let i=0;i<rays;i++){const a=TAU*i/rays+A.n*.1;if(Math.abs(fztWrap(a-gap))>.55){const q=eShootT(origin.x,origin.y,a,2.5+rank*.2,'matter',{w:16,h:16});if(q){q._v19Symbiote=true;q._hb20Owner=b;}}}b20Cue('shadowRelease');}}
  else if(A.type==='punch'){const first={x:A.target.x-(168-128)*1.1,y:A.target.y-(120-112)*1.1},second={x:A.target.x-(88-128)*1.1,y:A.target.y-(120-112)*1.1};
   if(u<.60){const v=u<0?clamp(A.t/A.tell,0,1)*.15:.15+v19Ease(u/.32)*.85;b.x=lerp(A.origin.x,first.x,v);b.y=lerp(A.origin.y,first.y,v);}else{const v=v19Ease((u-.60)/.22);b.x=lerp(first.x,second.x,v);b.y=lerp(first.y,second.y,v);}
   const phase=u>=.60?1:0,pose=hb20Pose(b),tip=phase?[88,120]:[168,120],at=hb20World(pose.a,tip,b,pose.k);A.fists??=[{hit:new Set()},{hit:new Set()}];const fist=A.fists[phase];if((u>=.16&&u<.40||u>=.70&&u<.95)&&fist.previous)b20HitSegment(b,fist.previous,at,26,'Dracodia fire punch',fist.hit);fist.previous=at;if((u>=.2&&!A.impact)||(u>=.73&&!A.secondImpact)){if(A.impact)A.secondImpact=true;A.impact=true;b20Cue('hammerImpact');b20Log('fire-punch',{phase,at,target:A.target});}}
  else if(A.type==='fists'&&u>=.25&&!A.impact){A.impact=true;hb20Melee(b,A,A.target,A.target,48);hb20Wave(b,Q,A.target,true);for(let i=0;i<5;i++)Q.fire.push({x:A.target.x+(i-2)*40,y:A.target.y,t:0,hit:new Set()});b20Cue('furnaceFlameIgnite');}
  if(A.type==='fists'&&u<.25){const v=v19Ease(Math.max(0,A.t/A.tell));b.x=lerp(A.origin.x,A.target.x,v);b.y=lerp(A.origin.y,A.target.y-108,v);}
  if(A.t>=A.duration)hb20Finish(b,A);
 }
 for(const w of Q.waves){w.t+=dt;const from={x:w.x,y:w.y};w.x+=w.dir*w.speed*dt;b20HitSegment(b,from,w,w.fire?22:17,w.fire?'scattering code fire':'code ground wave',w.hit);}Q.waves=Q.waves.filter(w=>w.t<4&&w.x>camLeftX()-80&&w.x<camRightX()+80);
 for(const f of Q.fire){f.t+=dt;if(f.t>.25&&f.t<.85)b20HitSegment(b,f,f,18,'code fire scatter',f.hit);}Q.fire=Q.fire.filter(f=>f.t<1.1);
 Q.parts[0].hp=b.hp;Q.parts[1].hp=Q.hammerHP;Q.parts[2].hp=Q.gunHP;b._drawY=b.y;const p=gd4Create(b,8).p;p.x=b.x;p.y=b.y;p.hp=b.hp;p.maxhp=b.maxhp;p.flash=b.flash;p._noHit=b._noHit;p._hammer.state='hb20_'+(Q.action?.type||'idle');p._hammer.hammerDestroyed=Q.broken||Q.rage;p._hammer.hammerHP=Q.hammerHP;j3Save(b);
 if(!Q.action&&Q.cool>.4){b.x+=clamp(worldWidth()/2-b.x,-120*dt,120*dt);b.y+=clamp(viewTopY()+viewH()*.32-b.y,-120*dt,120*dt);}
 if(N.donorAge>52&&!Q.action&&!Q.waves.length&&j3State(b).hp[0]>0)j3Morph(b,'home');
};
modularHit=function(dmg){const b=boss;if(!hb20Own(b)||!hb20State(b))return HB20.base.hit.apply(this,arguments);const Q=hb20State(b);if(!r30Live(b)||b._noHit||!(dmg>0))return;const p=b.parts.includes(b._lastPart)?b._lastPart:Q.parts[0];markHit(b,.12);markHit(p,.12);
 if(Q.shield>0){if(!(Q.absorbCd>GP4.clock)){Q.absorbCd=GP4.clock+.10;b20Cue('shieldBossAbsorb');}b20Log('code-shield-absorb');return;}
 if(p.id==='hammer'&&!Q.broken){Q.hammerHP=Math.max(0,Q.hammerHP-dmg);if(Q.hammerHP<=0){Q.hammerHP=0;Q.cool=0;Q.action=null;hb20Start(b,'break');}p.hp=Q.hammerHP;return;}
 if(p.id==='chaingun'&&Q.action?.type==='gun'){Q.gunHP=Math.max(0,Q.gunHP-dmg);p.hp=Q.gunHP;if(!p.hp){v19Rupture(b,p);p.destroyed=true;b20Cue('shieldBreakCombat');}return;}
 const floor=!Q.gunSeen?b.maxhp*.65:!Q.broken?b.maxhp*.28:0,d=Math.max(0,Math.min(dmg,b.hp-floor));b.hp-=d;if(d<dmg&&floor>0){Q.gateFlash=.18;if(!(Q.absorbCd>GP4.clock)){Q.absorbCd=GP4.clock+.10;b20Cue('shieldBossAbsorb');}}Q.parts[0].hp=b.hp;stageStats.dmgDealt+=d;j3Save(b);if(b.hp<=0)r30Break(b);
};
retinaBossTargets=function(b){if(!hb20Own(b)||!hb20State(b))return HB20.base.targets.apply(this,arguments);if(!r30Live(b)||b._noHit)return[];const rig=v19HammerRig(b);return rig.map(v=>retinaDynamicPiece(b,'hb20-'+v.p.id,v.p.spec.label,()=>{const at=v19HammerRig(b).find(q=>q.p.id===v.p.id);return{x:at?.x||b.x,y:at?.y||b.y,hp:v.p.hp,dead:!at||v.p.destroyed||!hb20Own(b)||b._noHit};},d=>{b._lastPart=v.p;hitBoss(d);},v.w,v.h));};
target17BossContact=function(b){if(hb20Own(b))return false;return HB20.base.contact.apply(this,arguments);};
function hb20SafeText(A){const names=['TOP LEFT','TOP RIGHT','BOTTOM LEFT','BOTTOM RIGHT'],x=(camLeftX()+camRightX())/2,y=Math.max(viewTopY()+80,PLAY.y+18);ctx.save();ctx.fillStyle='rgba(3,5,14,.86)';ctx.fillRect(x-128,y-7,256,25);bmfDrawOn(ctx,window.BOF_UI_FACE||'game','SAFE: '+names[A.safe],x,y,12,'center');ctx.restore();}
function hb20LuminaireDraw(b,A){const l=A.area.left,top=A.area.top,w=A.area.w/2,h=A.area.h/2,u=clamp(A.t/A.tell,0,1);ctx.save();ctx.beginPath();for(let i=0;i<4;i++)if(i!==A.safe)ctx.rect(l+(i%2)*w,top+(i>>1)*h,w,h);ctx.clip();
 if(A.t<A.tell){const c=u<.5?'rgba(20,210,130,.16)':u<.8?'rgba(255,210,20,.22)':'rgba(255,35,60,.27)';ctx.fillStyle=c;ctx.fillRect(l,top,A.area.w,A.area.h);for(let i=0;i<4;i++)if(i!==A.safe)b20Reticle(l+(i%2+.5)*w,top+((i>>1)+.5)*h,Math.min(w,h)*.43,u);}
 else for(let i=0;i<4;i++)if(i!==A.safe){ctx.save();ctx.beginPath();ctx.rect(l+(i%2)*w,top+(i>>1)*h,w,h);ctx.clip();b20SizedEffect(DR21_ART.banks.ball,A.t,l+(i%2+.5)*w,top+((i>>1)+.5)*h,Math.hypot(w,h)*1.5,A.t*2);ctx.restore();}
 ctx.restore();hb20SafeText(A);if(A.t<A.tell){const p=clamp(A.t/Math.max(.1,A.tell-.2),0,1),target={x:l+(A.safe%2?.25:.75)*A.area.w,y:top+(A.safe<2?.75:.25)*A.area.h};b20SizedEffect(DR21_ART.banks.ball,A.t,lerp(A.coreFrom.x,target.x,p),lerp(A.coreFrom.y,target.y,p),45+p*95,A.t*TAU);}}
v19DonorDraw=function(b){if(!hb20Own(b)||!hb20State(b))return HB20.base.donor.apply(this,arguments);const Q=hb20State(b),A=Q.action;for(const v of v19HammerRig(b))v19Paint(v,b);
 if(Q.shield>0||Q.gateFlash>0||A?.type==='shield'&&A.t>=A.tell)b20Effect(DR21_ART.banks.shield_main,Q.age,b.x,b.y+30,290,0);
 if(A){const u=A.t-A.tell;if(A.type==='pickup')hb20PickupDraw(b,A.crate,true);
  else if(A.type==='luminaire')hb20LuminaireDraw(b,A);
  else if(A.t<A.tell){if(['skystrike','fists','punch'].includes(A.type)){b20Reticle(A.target.x,A.target.y,A.type==='punch'?48:65,A.t/A.tell);if(A.type==='punch')b20Field(b,A.origin,A.target,140,A.t/A.tell);else b20Field(b,{x:camLeftX(),y:A.target.y},{x:camRightX(),y:A.target.y},A.type==='fists'?44:34,A.t/A.tell);}else if(A.type==='side'||A.type==='throw')b20Field(b,A.origin,A.target,100,A.t/A.tell);else if(A.type==='ball')b20Field(b,A.from,A.to,96,A.t/A.tell);else if(A.type==='gun'){const m=hb20GunMount(b,A);b20Field(b,m,{x:m.x+Math.cos(m.a)*900,y:m.y+Math.sin(m.a)*900},44,A.t/A.tell);}else if(A.type==='spin')b20Reticle(b.x,b.y,130,A.t/A.tell);}
  if(A.type==='throw'&&u>=0){const at=hb20ToolAt(b,A);const tool=hb20Pick('corrupt_tool');b20Image(tool,at.x,at.y,1.1,A.t*TAU,0,tool.tip||[40,103]);}
  if(A.type==='gun'&&A.muzzle>0){const m=hb20GunMount(b,A);wm26Draw(ctx,'chaingun',m.x,m.y,m.a,1-A.muzzle/.08,60);}
  if(A.type==='break'&&A.t>1.3&&A.t<4.1)b20SizedEffect(DR21_ART.banks.ball,Q.age,b.x+34+Math.sin(A.t*65)*3,b.y-22,42,Math.sin(A.t*70)*.08);
 }
 for(const w of Q.waves)b20Effect(w.fire?PH20_ART.plume.frames:DR21_ART.banks.download,w.t,w.x,w.y,w.fire?68:56,w.dir<0?-Math.PI/2:Math.PI/2);
 for(const f of Q.fire)b20Effect(PH20_ART.plume.frames,f.t,f.x,f.y,75,Math.sin(f.t*6)*.3);
};
v18Clear=function(b){if(hb20Own(b)&&hb20State(b)){const Q=hb20State(b);Q.waves=[];Q.fire=[];Q.action=null;for(const q of eBullets)if(q._hb20Owner===b)q.dead=true;}return HB20.base.clear.apply(this,arguments);};
globalThis.BOF_HAMMER_REDESIGN={state:HB20,start:hb20Start,pose:hb20Pose};
