"use strict";
/* Stored whole boss plates return as ordinary field veterans. The encounter
   owns one movement/attack clock; it never borrows a boss gate, HP bar or reward. */
const LL18={clock:0,serial:0,events:[],beams:[],draws:{},base:{spawn:spawnEnemy,plan:buildStagePlan,
 begin:beginStage,load:stageLoadBegin,update:updatePlay,draw:drawEnemy,bullets:drawBullets,
 mega:s8MegaTick,aiBegin:ai27Begin,aiEnd:ai27End,entry:enemyEntrySweep,frenzy:enemyFrenzyTick,kill:killEnemy,ownsRoute:eb11OwnsRoute,profile:stageAiProfile},
 roster:{
  ll18spear:{name:'CRYO SPEAR VETERAN',key:'nsb_cryo_spear',role:'ice',size:200,hp:190,score:4300,
   mounts:[[-.245,.205],[.245,.205],[0,.435]],damage:['nsb_cryo_spear_damaged','nsb_cryo_spear_critical']},
  ll18raptor:{name:'BLACKSTEEL HUNTER',key:'nsb_rap_intact',role:'raptor',size:176,hp:160,score:3800,rotation:Math.PI,
   mounts:[[-.25,-.12],[.25,-.12],[0,.43]],damage:['nsb_rap_crit']},
  ll18herald:{name:'HELLWING EXECUTIONER',key:'nhd_idle_0',role:'herald',size:210,hp:210,score:5200,
   mounts:[[-.29,.24],[.29,.24],[0,.42]]},
  ll18brood:{name:'BROOD SENTINEL',key:'nsb_spawncarrier_intact_v2',role:'brood',size:200,hp:180,score:4600,
   mounts:[[-.316,.234],[.316,.234],[0,.414]],damage:['nsb_spawncarrier_damaged_v2','nsb_spawncarrier_critical_v2']}
 },profiles:{
  normal:{settle:.55,tell:1.05,gap:1.70,burst:3,fan:5,ring:12,speed:2.7,life:16,cap:2,beat:.19},
  hard:{settle:.45,tell:.88,gap:1.22,burst:5,fan:7,ring:16,speed:3.1,life:17,cap:2,beat:.17},
  furious:{settle:.38,tell:.74,gap:.82,burst:7,fan:9,ring:20,speed:3.4,life:18,cap:2,beat:.15}
 }};
function ll18Profile(){return LL18.profiles[diffKey==='insanity'?'furious':diffKey]||LL18.profiles.normal;}
stageAiProfile=function(stage){const P=LL18.base.profile.apply(this,arguments);if((stage||run.stage)!==8)return P;
 // Carrier escorts need room beside the existing late fleet. The old seven
 // actor Furious ceiling postponed its final authored waves past the approach.
 // Heavy veterans remain capped at two and keep their separate firing budget.
 return {...P,cap:diffKey==='insanity'?10:diffKey==='furious'?9:diffKey==='hard'?7:P.cap};
};
function ll18Log(event,e,data={}){LL18.events.push({event,time:LL18.clock,stage:run.stage,type:e?.type,id:e?._ll18?.id,...data});if(LL18.events.length>420)LL18.events.shift();}
function ll18Alive(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function ll18Keys(n){
 if(n!==7&&n!==8)return [];
 const types=n===7?['ll18raptor','ll18brood']:Object.keys(LL18.roster),keys=types.flatMap(k=>{const d=LL18.roster[k];return[d.key,...(d.damage||[])];});
 keys.push(S81003_ART.beams.key,'fx_ground_strikes_0916','fx_ground_target_reticle','fr27_realm_fleet','fr27_realm_ordnance','s8nf_stealth_crescent_idle','cfx_stage7_toxic_projectiles_v2');
 if(n===8)for(let i=0;i<8;i++)keys.push('l23fx_cryo_ball_'+i,'l23fx_rime_orb_'+i);
 for(let i=0;i<4;i++)keys.push('s8nf_stealth_crescent_muzzle_'+i);
 if(n===8)for(let i=0;i<6;i++)keys.push('nhd_idle_'+i,'nhd_primary_projectile_'+i,'nhd_special_projectile_'+i);
 return keys;
}
stageLoadBegin=function(n,keys){return LL18.base.load.call(this,n,[...(keys||[]),...ll18Keys(n)]);};
beginStage=function(n){LL18.clock=0;LL18.serial=0;LL18.events=[];LL18.beams=[];LL18.draws={};
 const r=LL18.base.begin.apply(this,arguments);ll18Keys(n).forEach(k=>XART.rdy(k));return r;};
function ll18Mount(e,i){const d=LL18.roster[e.type],m=d.mounts[i];return{x:e.x+m[0]*e._drawW,y:e.y+m[1]*e._drawH};}
function ll18Spawn(type,x,y,opt={}){
 const d=LL18.roster[type],e=LL18.base.spawn('s8interceptor',x,y,opt);if(!e)return null;
 // The constructor supplies ordinary collision, death, pickups and Retina.
 // None of its interceptor controllers may also move or fire this new hull.
 for(const k of Object.keys(e))if(/^_(s8|alien1003|orbit1003|fr|fury|eb11|ep13|ai27|entrySweep|dr$|cn$|esh|enemyShield|modJet|ap10Flight|air17|af10)/.test(k))delete e[k];
 const im=XART.rdy(d.key)&&XART.get(d.key),ratio=im?im.width/im.height:(d.role==='herald'?.75:1),h=d.size,w=h*ratio;
 Object.assign(e,{type,name:d.name,pattern:'s8mega',art:d.key,ground:false,shoots:false,fk:null,_atk:'none',
  w:w*.72,h:h*.80,_drawW:w,_drawH:h,_noSep:true,_noHit:false,_continueEligible:false,
  vx:0,vy:0,spin:0,score:d.score,dropOk:true,flash:0});
 // EHP deliberately clamps popcorn enemies to a shot-count band. Veterans use
 // an absolute hull pool, as the existing Frost Siege Veteran does, so these
 // former bosses cannot disappear before demonstrating their first attack.
 e.hp=e.maxhp=e._maxhp=Math.ceil(d.hp*DIFF.eHp*(run.stage===7?.78:1)*(coopActive()?1.5:1));
 e._ll18={id:++LL18.serial,role:d.role,phase:'entry',t:0,age:0,seen:0,cycles:0,shots:0,
  homeX:LL18.serial%2?camLeftX()+w*.5+20:camRightX()-w*.5-20,homeY:viewTopY()+viewH()*.25,
  escorts:[],cd:ll18Profile().settle};
 // Preserve the caller's above-screen entry, accounting for the full image.
 if(y<=PLAY.y)e.y=Math.min(e.y,viewTopY()-h*.55-20);
 ll18Keys(run.stage).forEach(k=>XART.rdy(k));ll18Log('spawn',e,{hp:e.hp});return e;
}
spawnEnemy=function(type,x,y,opt={}){return LL18.roster[type]?ll18Spawn(type,x,y,opt):LL18.base.spawn.apply(this,arguments);};
// Replace selected authored beats; no endless reinforcement clock can refill
// the approach gates. The well-liked Frost Siege Veteran remains at 34.5s.
buildStagePlan=function(n){const plan=LL18.base.plan.apply(this,arguments);if(n!==7&&n!==8)return plan;
 const beats=n===7?{12.5:'ll18brood',28:'ll18raptor',44:'ll18brood'}:
  {10:'ll18raptor',13:'ll18herald',27:'ll18spear',41:'ll18brood'};
 return plan.map(row=>{
  // Retain the displaced Furnace Maw at the final carrier beat. Blue Hybrid
  // and Tentacle Cannon retain their original 47s / 55s waves. A new heavy at
  // 55s could only enter and withdraw before the 57s approach gate, never fire.
  if(n===8&&row.t===51)return {...row,fn:()=>{const W=worldWidth();spawnEnemy('s8carrier',W*.5,-185,{});spawnEnemy('s8gunship',W*.22,-165,{_stagger:.20});spawnEnemy('s8interceptor',W*.78,-90,{_stagger:.40});}};
  const type=beats[row.t];if(!type)return row;return {...row,fn:()=>{
  if(enemies.filter(e=>ll18Alive(e)&&e._ll18).length>=ll18Profile().cap)return row.fn();
  const side=(LL18.serial%2?-.11:.11),x=camLeftX()+VW*(.5+side);spawnEnemy(type,x,viewTopY()-150,{});
  if(n===7&&row.t===28)spawnEnemy('s7canister',worldWidth()*.65,viewTopY()-150,{_stagger:.3});
 }};});
};
enemyEntrySweep=function(e){if(!e?._ll18)return LL18.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(!e?._ll18)return LL18.base.frenzy.apply(this,arguments);};
eb11OwnsRoute=function(e){return !!e?._ll18||LL18.base.ownsRoute.apply(this,arguments);};
ai27Begin=function(e,dt){
 // Mutator hulls replaced the same delayed roster slots but own a different
 // mover. Their unconsumed delay also blocked the shared advanced attack gate.
 if((run.stage===7||run.stage===8)&&e?._mutator1003&&e._stagger>0)e._stagger=Math.max(0,e._stagger-dt);
 if(!e?._ll18)return LL18.base.aiBegin.apply(this,arguments);const old=ai27Context;ai27Context=null;return old;
};
ai27End=function(e,previous){if(!e?._ll18)return LL18.base.aiEnd.apply(this,arguments);ai27Context=previous;};
function ll18RouteClosing(){return bossWarned||bossActive||subBossActive||warnT>0||bossDefeated||
 stageTimer>=curStage.length-3||(!subBossDone&&stageTimer>=curStage.length*(SUBBOSS[run.stage]?.at||2)-.7);}
function ll18Busy(){return !!story||!!debugFight||!!wfx?.fseq||!!BOFCinematicDirector.live;}
function ll18Start(e){
 const A=e._ll18,P=ll18Profile(),d=LL18.roster[e.type],T=targetShip(e.x,e.y);
 if(!T||T.dead)return false;
 // A second heavy can prepare, but overlapping crossing lasers are forbidden.
 const preparing=enemies.filter(o=>o!==e&&ll18Alive(o)&&o._ll18&&['tell','fire'].includes(o._ll18.phase));
 if(LL18.beams.some(b=>b.owner!==e)||preparing.length>=(diffKey==='furious'||diffKey==='insanity'?2:1))return false;
 if((d.role==='raptor'||d.role==='herald')&&preparing.some(o=>o._ll18.lanes?.length))return false;
 const move=A.cycles%2===0?'primary':'special';A.attack=move;A.phase='tell';A.t=0;A.round=0;A.target={x:T.x,y:T.y};
 A.origins=[0,1,2].map(i=>ll18Mount(e,i));A.angles=A.origins.map(m=>Math.atan2(T.y-m.y,T.x-m.x));
 A.warning=P.tell+(move==='special'?.18:0);A.points=[];A.lanes=[];
 if(d.role==='ice'&&move==='special'){
  const count=diffKey==='normal'||diffKey==='easy'?2:3,spacing=70;
  // Entire battery shares one clamped centre; targets never collapse together
  // at a viewport edge, and a clear strip survives on both sides.
  const center=clamp(T.x,camLeftX()+42+(count-1)*spacing/2,camRightX()-42-(count-1)*spacing/2);
  for(let i=0;i<count;i++)A.points.push({x:center+(i-(count-1)/2)*spacing,y:T.y});
 }
 if((d.role==='raptor'&&move==='special')||d.role==='herald'&&move==='primary'){
  // Lock two parallel lanes around the sampled player position, leaving a
  // 48px centre corridor rather than intersecting beams on the player.
  A.lanes=[0,1].map(i=>{const m=A.origins[i],tx=T.x+(i?48:-48);return s81003Lane(m.x,m.y,tx,T.y,12,viewH()+160);});
 }
 combatWarningTick(e,'ll18-'+A.id+'-'+A.cycles,0,A.warning);r30Sound('bossWeaponCharge');
 ll18Log('tell',e,{attack:move,warning:A.warning,target:{...A.target},lanes:A.lanes.map(l=>({...l}))});return true;
}
function ll18Shot(e,i,a,kind='s8pair',speed=ll18Profile().speed){
 if(eBullets.length>=ep13Profile().cap)return null;
 if(e._ll18.role==='brood')kind='s7acid';
 const m=ll18Mount(e,i),b=eShootT(m.x,m.y,a,speed,kind,{owner:e,silent:i===1,noMuzzle:true,w:kind==='emissile'?10:8,h:kind==='emissile'?18:12,szMul:.7});
 if(!b||b.dead)return null;b._ll18=true;b._ll18Owner=e._ll18.id;b._noArsenal=true;
 if(e._ll18.role==='raptor')b._frRealm=0;
 if(e._ll18.role==='brood')b.szMul=.32;
 if(e._ll18.role==='ice'){b._l23fx='cryo_ball';b.szMul=.65;b.w=b.h=12;}
 if(e._ll18.role==='herald'){b._heraldProjectile='primary';b.w=b.h=12;}
 e._ll18.shots++;ll18Log('shot',e,{x:m.x,y:m.y,angle:a,kind});
 wm26EnemyShot(m.x,m.y,a,kind,e);return b;
}
function ll18Release(e){const A=e._ll18,P=ll18Profile(),role=A.role;
 A.phase='fire';A.t=0;A.round=0;A.fired=LL18.clock;ll18Log('release',e,{attack:A.attack,reaction:A.seen});
 if(A.lanes.length){
  LL18.beams.push(...A.lanes.map(L=>({...L,t:0,dur:.55,owner:e})));r30Sound('enemyHeavyLaser');
 }else if(role==='ice'&&A.attack==='special'){
  for(const p of A.points){const q=groundTargetingSpawn({kind:'glacial',...p,warn:1.20,active:.65,radius:23,size:106,track:false,lane:false,owner:e,shake:3});q._late27=true;}
  ll18Log('ice-artillery',e,{points:A.points.map(p=>({...p})),warning:1.20});
 }else if(role==='brood'&&A.attack==='special'){
  // Crescent stays an aircraft in both stages. The old s8scout name is remapped
  // to the modular Hexpyre monster on Stage 8, so it cannot identify a bay jet.
  A.escorts=A.escorts.filter(ll18Alive);const limit=diffKey==='normal'||diffKey==='easy'?1:2;
  if(A.escorts.length<limit&&enemies.filter(ll18Alive).length<13){for(const side of [-1,1]){
   if(A.escorts.length>=limit)break;const child=spawnEnemy('s8crescent',e.x+side*66,e.y+25,{_stagger:.3});
   if(child){child._ll18Escort={age:0,owner:e};child._stagger=side<0?.15:.40;child.hp=child.maxhp=child._maxhp=EHP(run.stage===7?24:36);A.escorts.push(child);ll18Log('scout-launch',e);}
  }}
 }else if(role==='herald'){
  const m=ll18Mount(e,2),aim=Math.atan2(A.target.y-m.y,A.target.x-m.x),gap=.95;
  for(let i=0;i<P.ring;i++){const a=TAU*i/P.ring,d=Math.atan2(Math.sin(a-aim),Math.cos(a-aim));if(Math.abs(d)>gap/2)ll18Shot(e,2,a,'s8pair',P.speed*.78);}
 }
}
function ll18Tick(e,dt){
 const A=e._ll18,P=ll18Profile();A.age+=dt;A.t+=dt;e.shoots=false;e.vx=e.vy=0;e.spin=0;
 const visible=e.x>=camLeftX()+20&&e.x<=camRightX()-20&&e.y>=viewTopY()+e._drawH*.30&&e.y<viewTopY()+viewH()-40;
 if(visible)A.seen+=dt;
 if(ll18RouteClosing()&&A.phase!=='leave'){A.phase='leave';A.t=0;LL18.beams=LL18.beams.filter(b=>b.owner!==e);groundTargetingCancel(e);ll18Log('withdraw',e);}
 if(A.phase==='leave'||A.age>P.life+6){A.phase='leave';e._noHit=false;e.y-=155*dt;if(e.y<viewTopY()-e._drawH)e.dead=true;return;}
 if(ll18Busy())return;
 if(e._frozen||e._mercuryLock>0||e._shieldStun>0)return;
 if(A.phase==='entry'){
  e.x+=clamp(A.homeX-e.x,-100*dt,100*dt);e.y+=Math.min(Math.max(0,A.homeY-e.y),125*dt);
  if(e.y>=A.homeY-1){e.y=A.homeY;A.phase='recover';A.t=0;}return;
 }
 e.y=A.homeY;
 if(A.age>P.life&&A.phase==='recover'){A.phase='leave';A.t=0;return;}
 if(A.phase==='recover'){
  // Reposition only between committed attacks. The hull never slides off its
  // own warning or live beam; each pocket stays within the camera bounds.
  const pad=e._drawW*.5+18,tx=clamp(A.homeX+(A.cycles%2?55:-55),camLeftX()+pad,camRightX()-pad);
  e.x+=clamp(tx-e.x,-85*dt,85*dt);
  if(A.t>=(A.cycles?P.gap:P.settle)&&visible&&ll18Alive(e)&&A.seen>=P.settle)ll18Start(e);return;
 }
 if(A.phase==='tell'){
  // Camera departure or advancing into the battery restarts the full warning.
  if(!visible||targetShip(e.x,e.y).y<e.y+70){A.phase='recover';A.t=0;return;}
  combatWarningTick(e,'ll18-'+A.id+'-'+A.cycles,A.t,A.warning);if(A.t>=A.warning)ll18Release(e);return;
 }
 if(A.phase==='fire'){
  const burst=(A.role==='raptor'||A.role==='brood')&&A.attack==='primary',ice=A.role==='ice'&&A.attack==='primary';
  if(burst&&A.round<P.burst&&A.t>=A.round*P.beat){
   const i=A.round%2;ll18Shot(e,i,A.angles[i],A.role==='brood'?'blob':'s8slug',P.speed+1);A.round++;
  }else if(ice&&A.round<2&&A.t>=A.round*.28){
   const step=.14,m=ll18Mount(e,A.round),aim=A.angles[A.round];
   for(let i=0;i<P.fan;i++)ll18Shot(e,A.round,aim+(i-(P.fan-1)/2)*step,'ice',P.speed*.82);A.round++;
  }
  const life=burst?P.burst*P.beat+.3:ice?.72:A.lanes.length?.62:1.25;
  if(A.t>=life){A.phase='recover';A.t=0;A.cycles++;ll18Log('recover',e,{cycles:A.cycles});}
 }
}
s8MegaTick=function(e,dt){
 if(e?._ll18Escort?.leaving){if(e._frRealmAI)e._frRealmAI.tell=null;return;}
 // The late fixed-facing fleet controller replaced the original mover that
 // consumed _stagger. Its firing gate still tested the never-changing value,
 // permanently disarming every delayed partner in the authored wave table.
 if(e?._stagger>0){e._stagger=Math.max(0,e._stagger-dt);if(e._stagger>0)return;}
 return e?._ll18?ll18Tick(e,dt):LL18.base.mega.apply(this,arguments);
};
function ll18Plate(e){const d=LL18.roster[e.type],A=e._ll18,frac=e.hp/e.maxhp;
 let key=d.key;if(d.role==='herald')key='nhd_idle_'+Math.floor(A.age*8)%6;
 else if(d.damage&&frac<.34)key=d.damage.at(-1);
 if(!XART.rdy(key))return;
 ctx.save();ctx.translate(e.x,e.y);if(d.rotation)ctx.rotate(d.rotation);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(key),-e._drawW/2,-e._drawH/2,e._drawW,e._drawH);
 if(e.flash>0){const white=xartTint(key,hitFlashColor(e,'#ffffff'),1);if(white){ctx.globalAlpha*=Math.min(1,e.flash*8);ctx.drawImage(white,-e._drawW/2,-e._drawH/2,e._drawW,e._drawH);}}
 ctx.restore();LL18.draws[e.type]=(LL18.draws[e.type]||0)+1;
}
drawEnemy=function(e){if(!e?._ll18)return LL18.base.draw.apply(this,arguments);if(e.dead||e._dyingT!=null)return;
 ll18Plate(e);const A=e._ll18;if(A.phase!=='tell')return;
 const progress=A.t/A.warning;
 if(A.points.length)for(const p of A.points)s81003Target(p.x,p.y,66,progress);
 else if(A.lanes.length)for(const L of A.lanes)combatWarningDraw(e,{...L,progress});
 else if(A.role==='herald')drawBossRetina(e,e.x,e.y,(1-progress)*TAU,1);
 else for(const i of [0,1]){const m=A.origins[i],a=A.angles[i];combatWarningDraw(e,{...m,ex:m.x+Math.cos(a)*viewH(),ey:m.y+Math.sin(a)*viewH(),width:18,progress});}
};
function ll18BeamDraw(){for(const q of LL18.beams){
 const len=Math.hypot(q.ex-q.x,q.ey-q.y),a=Math.atan2(q.ey-q.y,q.ex-q.x),h=len/.91;
 s81003Cell('beams',Math.floor(q.t*18)%4,q.x+Math.cos(a)*(h*.5-h*.07),q.y+Math.sin(a)*(h*.5-h*.07),q.width*3.4,h,Math.min(1,(q.dur-q.t)/.09),a-Math.PI/2);
 }}
drawBullets=function(){const r=LL18.base.bullets.apply(this,arguments);ll18BeamDraw();return r;};
killEnemy=function(e){if(e?._ll18&&!e.dead&&e._dyingT==null){LL18.beams=LL18.beams.filter(b=>b.owner!==e);groundTargetingCancel(e);ll18Log('destroyed',e);}return LL18.base.kill.apply(this,arguments);};
updatePlay=function(dt){if(state===GS.PLAY)LL18.clock+=dt;const r=LL18.base.update.apply(this,arguments);if(state!==GS.PLAY)return r;
 for(const e of enemies)if(e._ll18Escort&&ll18Alive(e)){e._ll18Escort.age+=dt;if(e._ll18Escort.age>12||ll18RouteClosing()||e._ll18Escort.leaving){e._ll18Escort.leaving=true;e._fcd=999;e._s8Act=null;if(e._frRealmAI)e._frRealmAI.tell=null;e.y-=200*dt;if(e.y<viewTopY()-120)e.dead=true;}}
 LL18.beams=LL18.beams.filter(q=>ll18Alive(q.owner)&&(q.t+=dt)<q.dur&&!ll18RouteClosing());
 for(const q of LL18.beams)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,q)<q.width/2+3)playerHit('veteran ion lance');});
 return r;
};
window.BOF_LEGACY_LEGION={state:LL18,profile:ll18Profile,spawn:ll18Spawn};
