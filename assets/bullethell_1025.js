'use strict';
/* Oct25: authored weapon barrages, interleaved at native decision boundaries.
   Each wave commits its escape lane before release. HP/death/art remain native. */
const BH25={events:[],serial:0,owners:new Set(),base:{load:stageLoadBegin,update:updatePlay,
 intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,rules:s3kOrdnanceRules,
 rzbNext:razorbackNext,rzbCombat:razorbackCombat,rzbTick:razorbackUpdate,
 erNext:er26Next,erCombat:er26Combat,erWar:er26WarTick,escorts:sa14Escorts,
 bomberNext:hc1007BomberNext,bomberTick:siegeBomberTick,fortressNext:sc13BeginSequence,fortressTick:warhiveTick,reactor:er23Fortress,
 s7Next:s7mNext,s7Tick:s7mTick,heraldNext:hd1003Tell,heraldTick:hd1003Tick,horizonSet:s5924Set,horizonTick:s9VoidHorizonTick,
 drNext:v18StartAttack,drTick:v18AttackTick,drPose:bi24AttackPose,drWeapon:rb23DrawWeapon,
 drawMini:drawSubBoss,drawBoss:drawBoss,s7Hit:s7mHit,miniHit:hitSubBoss,drHit:modularHit},
 cfg:{razor:{style:'rake',cue:'enemyBossCannon'},reaver:{style:'petals',cue:'enemyFlameBolt'},
 frost:{style:'braid',cue:'enemyMachineGunHeavy'},olive:{style:'rake',cue:'enemyMachineGunHeavy'},
 bomber:{style:'braid',cue:'enemyBossCannon'},fortress:{style:'braid',cue:'enemyBossCannon'},
 dredger:{style:'braid',cue:'bossfireSludgeemperor'},warden:{style:'petals',cue:'bossfireSludgeemperor'},
 herald:{style:'petals',cue:'bossfireVileexistence'},horizon:{style:'petals',cue:'enemyBossCannon'},
 claws:{style:'braid',cue:'enemyBossCannon'},dracodia:{style:'petals',cue:'enemyBossCannon'}}};
function bh25Rank(){return diffKey==='easy'?0:diffKey==='normal'?1:diffKey==='hard'?2:3;}
function bh25Log(b,event,data={}){BH25.events.push({event,stage:run.stage,kind:b._bh25?.kind||b._ship||b.kind,time:efxClock,...data});if(BH25.events.length>1200)BH25.events.shift();}
stageLoadBegin=function(n,keys){for(const cue of ['bossWeaponCharge','combatToxic0927',...new Set(Object.values(BH25.cfg).map(c=>c.cue))])Snd.prepare(cue);
 return BH25.base.load.call(this,n,[...(keys||[]),'bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall']);};
function bh25Due(b,key,period=3,first=false){if(!b||b.dead||b.enter||b._noHit||b._bh25)return false;
 const counts=b._bh25Turns||(b._bh25Turns={});counts[key]=(counts[key]||0)+1;
 return (counts[key]-(first?1:0))%period===0&&b.y<viewTopY()+viewH()*.56&&!b._l23Beam&&!S81003.beams.some(q=>q.owner===b&&q.t<q.life);
}
function bh25PartLive(b,id){if(b.dead)return false;if(id==='turret'&&b._rzb)return b._rzb.pools.turret>0;
 if(b._cargo13&&id==='core')return b._cargo13.core>0&&sc13Open(b);
 if(b._s7mod?.tank&&id==='vent')return b._s7mod.core>0;
 if(id==='core'||id==='emitter')return true;
 if(b._s7mod)return b._s7mod.parts.some(p=>p.id===id&&p.hp>0);
 if(b._hd1003)return hd1003Live(b,hd1003Part(b,id));
 if(b._cargo13)return !b._cargo13.guns[id]?.dead;
 if(b._bomber)return b._bomber.parts.some(p=>p.id===id&&p.hp>0);
 if(b._av3Reaver)return !av3Part(b,id)?.dead;
 if(b._mr27)return !mr27Part(b,id)?.dead;
 if(b._r30)return b.parts.some(p=>p.id===id&&!p.destroyed&&p.hp>0);
 return true;
}
function bh25Ports(b,kind=b._bh25?.kind){let out=[];
 if(kind==='razor'){const R=b._rzb;out=[{id:'turret',...rzbFwd(b,R.turret,(142-R.recoil)*rzbScale(b))}];}
 else if(kind==='warden')out=[{id:'emitter',...s7mMuzzle(b,'emitter')}];
 else if(kind==='dredger'){out=b._bh25?.dorsal||!s7mLive(b._s7mod,'gun').length?[{id:'vent',...bh25DredgerVent(b)}]:s7mLive(b._s7mod,'gun').map(p=>({id:p.id,...bh25DredgerBarrel(b,p.id)}));}
 else if(['reaver','frost','olive'].includes(kind)){
  for(const slot of ['L','R'])if(mr27CanFire(b,slot))out.push({id:kind==='reaver'?av3Slot(slot):'gun'+slot,slot,...shipBossMount(b,slot)});
  if(kind==='olive'&&mr27CanFire(b,'C'))out.push({id:'gunC',slot:'C',...shipBossMount(b,'C')});
  if(!out.length&&kind==='reaver'&&!av3Part(b,'nose').dead)out.push({id:'nose',slot:'C',...shipBossMount(b,'C')});
 }
 else if(kind==='bomber')out=b._bomber.parts.filter(p=>p.id.startsWith('laser')&&p.hp>0).map(p=>({id:p.id,...hc1007Origin(b,p.id)}));
 else if(kind==='fortress'&&sc13Open(b)&&b._cargo13.core>0)out=[{id:'core',...sc13Core(b)}];
 else if(kind==='herald'){out=['gunL','gunR'].filter(id=>hd1003Live(b,hd1003Part(b,id))).map(id=>({id,...hd1003Muzzle(b,id)}));if(!out.length)out=[{id:'head',...hd1003Muzzle(b,'head')}];}
 else if(kind==='horizon')out=[{id:'core',...s5924Eye(b)}];
 else if(kind==='claws')out=rb23Arms(b).map(p=>({id:p.id,...rb23PartPoint(b,p,true)}));
 else if(kind==='dracodia')out=v18Ports(b).map(p=>({id:p.module,...p}));
 return out.filter(p=>Number.isFinite(p.x+p.y)&&bh25PartLive(b,p.id));
}
function bh25Valid(b){const P=b?._bh25;if(!P||b.dead||run.stage!==P.stage||!(b===boss||b===subBoss))return false;
 if(['claws','dracodia'].includes(P.kind))return b._r30.mode==='fight'&&j3State(b).encounter===P.encounter&&b._r30.v18.form===P.form&&b._r30.v18.attack?.type==='bh25';
 if(b._s7mod)return b._s7mod.mode==='bh25';
 if(b._er26)return b._er26.mode==='bh25'&&!b._fb9Body;
 if(P.kind==='fortress')return b._cargo13.mode==='bh25'&&bh25PartLive(b,'core');
 return true;
}
// The Dredger plate contains four barrels per gun assembly. Its old generic
// centre-bottom socket was in the gap between those barrels.
function bh25DredgerBarrel(b,id,barrel=((b._bh25?.wave||0)>>1)%4){const p=s7mPose(b).find(p=>p.id===id),a=p.a+b._s7mod.lean,o=s7mWorld(b,p);
 const x=[-.371,-.276,.270,.361][barrel]*p.w,y=p.h*.45;
 return{x:o.x+x*Math.cos(a)-y*Math.sin(a),y:o.y+x*Math.sin(a)+y*Math.cos(a),a:Math.PI/2+a,angle:Math.PI/2+a,barrel};
}
function bh25DredgerVent(b){const p=s7mPose(b).find(p=>p.id==='core'),o=s7mWorld(b,p),a=p.a+b._s7mod.lean;
 return{x:o.x+Math.sin(a)*p.h*.315,y:o.y-Math.cos(a)*p.h*.315,a:-Math.PI/2+a,angle:-Math.PI/2+a};
}
function bh25DredgerLob(b){const P=b._bh25,rank=P.rank,T={x:clamp(P.escapeX+(P.wave%2?112:-112),camLeftX()+50,camRightX()-50),y:clamp(P.target.y-100+(P.wave%2?32:-32),viewTopY()+230,VH-100)};
 const aim=Math.atan2(VH-38-T.y,P.escapeX-T.x),half=Math.max(.27,Math.atan2(48,VH-38-T.y)),angles=[];
 for(let i=0;i<[12,14,16,18][rank];i++){const a=i*TAU/[12,14,16,18][rank]+P.wave*.19;if(Math.abs(Math.atan2(Math.sin(a-aim),Math.cos(a-aim)))>=half)angles.push(a);}
 const q=tb28Fire(b,{from:()=>b.dead?null:bh25DredgerVent(b),target:T,warm:P.wave===0?P.warm:.80,flight:1.05,mode:'lob',arc:115,art:'toxic',size:32,splash:28,reticle:72,width:22,laneAlpha:.34,silent:P.wave>0,
  onRelease:q=>{if(b._bh25!==P)return;q._bh25Released=true;const p=bh25DredgerVent(b);navalFlash(b,p,.8,'weapon_muzzle_toxic',{n:4,hpx:40,life:.18,angle:p.a,follow:()=>b._bh25===P&&!b.dead?bh25DredgerVent(b):null});combatAudio0927(b,'bossfireSludgeemperor',.45);bh25Log(b,'dorsal-release',{wave:P.wave,x:q.sx,y:q.sy,target:T});},
  onArrive:(q,x,y)=>{if(b._bh25!==P||b.dead)return;const live=eBullets.filter(q=>!q.dead&&q._bh25Owner===b).length;if(live+angles.length<=128)for(const a of angles)bh25Shot(b,{id:'vent',x,y},a);s7mFX(x,y,90,true);combatAudio0927(b,'combatToxic0927',.5);bh25Log(b,'dorsal-splash',{wave:q._bh25Wave,x,y,count:angles.length});}});
 q._bh25Dredger=b;q._bh25Wave=P.wave;q._bh25Angles=angles;P.lob=q;P.previewAt=P.t;P.fireAt=P.t+q.warm;P.phase='lob';
 bh25Log(b,'wave-tell',{wave:P.wave,count:angles.length,reaction:q.warm,source:'dorsal-vent',target:T});
}
function bh25DredgerLobTick(b,dt){const P=b._bh25,q=P.lob;
 if(P.phase==='lob'&&(q.arrived||q.dead)){P.wave++;if(P.wave<P.waves)bh25DredgerLob(b);else{P.phase='recover';P.recoverAt=P.t;bh25Log(b,'section-recovery');}}
 return P.phase==='lob';
}
function bh25Prime(b){const P=b._bh25,ports=bh25Ports(b);P.plan=[];if(!ports.length)return;
 const p=ports[P.wave%ports.length],rank=P.rank,c=BH25.cfg[P.kind],style=c.style;
 // A slowly moving committed opening; at most 34px between successive waves.
 const x=clamp(P.escapeX+Math.sin(P.wave*.52+P.side)*52,camLeftX()+56,camRightX()-56),y=VH-38;
 const gap=Math.atan2(y-p.y,x-p.x),distance=Math.max(150,Math.hypot(x-p.x,y-p.y));
 const half=Math.max(.14,Math.atan2(38+rank*2,distance)),n=style==='petals'?[14,18,22,26][rank]:[9,11,13,15][rank];
 const aim=clamp(Math.atan2(P.target.y-p.y,P.target.x-p.x),.72,Math.PI-.72),turn=P.wave*.115*P.side;
 for(let i=0;i<n;i++){
  const a=style==='petals'?i*TAU/n+turn:aim+(i-(n-1)/2)*(2.20/(n-1))+(style==='braid'?Math.sin(P.wave*.62)*.16:Math.sin(P.wave*.7)*.10);
  if(Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)))<half)continue;
  P.plan.push({id:p.id,slot:p.slot,a});
 }
 P.previewAt=P.t;P.fireAt=P.t+(P.wave===0?P.warm:P.beat);P.gap={x,y,half,angle:gap};
 bh25Log(b,'wave-tell',{wave:P.wave,count:P.plan.length,gap:P.gap,reaction:P.wave===0?P.warm:P.beat});
}
function bh25Start(b,kind,finish){if(!bh25Ports(b,kind).length)return false;
 const rank=bh25Rank(),T=targetShip(b.x,b.y);const P=b._bh25={kind,stage:run.stage,rank,t:0,wave:0,serial:BH25.serial++,phase:'tell',
  warm:[1.65,1.45,1.30,1.18][rank],beat:[.68,.60,.55,.50][rank],waves:[5,6,7,8][rank],speed:[1.85,2.05,2.20,2.35][rank],
  escapeX:clamp(T.x,camLeftX()+90,camRightX()-90),target:{x:T.x,y:T.y},side:BH25.serial%2?1:-1,finish,
  encounter:b._r30?j3State(b).encounter:null,form:b._r30?.v18?.form};
 if(kind==='dredger'){P.dorsal=!!((b._bh25DredgerTurns||0)%2)||!s7mLive(b._s7mod,'gun').length;b._bh25DredgerTurns=(b._bh25DredgerTurns||0)+1;if(P.dorsal)P.waves=[2,3,3,4][rank];}
 BH25.owners.add(b);if(P.dorsal)bh25DredgerLob(b);else if(kind==='claws'){P.phase='raise';P.plan=[];}else bh25Prime(b);combatAudio0927(b,'bossWeaponCharge',.8);bh25Log(b,'section-start',{waves:P.waves,warm:P.warm,style:P.dorsal?'dorsal-splash':BH25.cfg[kind].style});return true;
}
 function bh25Shot(b,p,a){const P=b._bh25,k=P.kind,kind=k==='razor'?'rzbSonic':k==='reaver'?'magma':['frost','olive'].includes(k)?'mg':k==='bomber'?'s6orb':k==='fortress'?'s4bomb':['warden','dredger'].includes(k)?'s7acid':k==='horizon'?'s9pair':'s8pair';
 const needle=['frost','olive'].includes(k),q=eShootT(p.x,p.y,a,P.speed,kind,{owner:b,w:needle?6:10,h:needle?16:10,silent:true,noMuzzle:true});
 if(!q||q.dead)return;
 Object.assign(q,{_bh25Owner:b,_bh25Kind:k,_bh25Part:p.id,_bh25Born:efxClock,_noArsenal:true,_boss:true,_weaponProof:true,_shootable:false,_s3kOriginalProof:false,homing:false});delete q.hp;
 if(k==='razor')Object.assign(q,{_rzb:true,_rzbOwner:b,_rzbFurious:!!b._rzb.furious,_fb9RzbProof:true,ang:a});
 if(k==='reaver')Object.assign(q,{_er26Art:'fire',_er26Source:'magmaward',_er26Draw:22,_er26Charred:false});
 if(['frost','olive'].includes(k))Object.assign(q,{mg:true,_coldTracer1002:true,_er26Source:b._ship});
 if(k==='fortress')Object.assign(q,{_s4wKind:'orb',_bfam:'storm',ang:a});
 if(['warden','dredger'].includes(k))Object.assign(q,{_s7modOwner:b,_s7modOrb:true});
 if(k==='herald')Object.assign(q,{_heraldOwner1003:b,_heraldPart1003:p.id,_hb25Chaos:true,_hb25Born:efxClock});
 if(k==='horizon')Object.assign(q,{_s5924Owner:b,_bf22Theme:'water',_bf22Form:'orb',_bf22Born:efxClock});
 if(['claws','dracodia'].includes(k))Object.assign(q,{_v18Owner:b,_r30Owner:b,_r30Shot:10,_r30Age:0});
 bh25Log(b,'round',{wave:P.wave,part:p.id,x:p.x,y:p.y,angle:a,speed:P.speed});return q;
}
function bh25Flash(b,p,a){const k=b._bh25.kind;
 if(['reaver','frost','olive'].includes(k))shipBossMuzzleStart(b,[p.slot],{life:.14,hpx:34,fam:k==='reaver'?'magma':'mg'});
 else if(k==='herald')hb25Flash(b,p.id,a);
 else if(k==='claws')navalFlash(b,p,.75,'weapon_muzzle_rotary',{n:4,hpx:42,life:.16,angle:a-Math.PI/2,follow:()=>!b.dead?bh25Ports(b).find(q=>q.id===p.id):null});
 else if(k==='dredger')navalFlash(b,p,.8,'weapon_muzzle_toxic',{n:4,hpx:34,life:.16,angle:p.a??a,follow:()=>!b.dead&&bh25PartLive(b,p.id)?bh25DredgerBarrel(b,p.id,p.barrel):null});
 else if(k==='warden')s7mFX(p.x,p.y,42,true);
 else wm26Emit(b,p.x,p.y,a,k==='razor'?'sonic':'laser',null,{size:34,life:.16,follow:()=>!b.dead?bh25Ports(b).find(q=>q.id===p.id):null});
}
function bh25RestoreCounter(b){const M=b?._s7mod;if(!M?.bh25Counter)return;if(!b.dead&&M.shield>0)M.counterTell=M.bh25Counter;delete M.bh25Counter;}
function bh25Cancel(b,reason){if(!b?._bh25)return;bh25Log(b,'section-cancel',{reason});delete b._bh25;BH25.owners.delete(b);bh25RestoreCounter(b);for(const q of eBullets)if(q._bh25Owner===b)q.dead=true;
 for(const q of tb28List)if(q._bh25Dredger===b)q.dead=true;
 if(b._cargo13?.mode==='bh25'&&!b.dead){b._cargo13.mode='recover';b._cargo13.rest=1.2;}
}
function bh25Prune(){for(const b of BH25.owners)if(!bh25Valid(b))bh25Cancel(b,'native-owner-change');
 for(const q of eBullets)if(q._bh25Owner&&(q._bh25Owner.dead||!(q._bh25Owner===boss||q._bh25Owner===subBoss)||!bh25PartLive(q._bh25Owner,q._bh25Part)||efxClock-q._bh25Born>6))q.dead=true;
}
function bh25Tick(b,dt){const P=b._bh25;if(!P)return false;if(!bh25Valid(b)){bh25Cancel(b,'interrupted');return false;}P.t+=dt;
 if(!bh25Ports(b).length){const end=P.finish;bh25Cancel(b,'weapons-destroyed');end();return true;}
 if(P.dorsal&&bh25DredgerLobTick(b,dt))return true;
 if(P.phase==='raise'){if(P.t>=.72){P.phase='tell';bh25Prime(b);}return true;}
 if(P.phase==='tell'){
  if(!P.plan.some(L=>bh25PartLive(b,L.id)))bh25Prime(b);
  combatWarningTick(b,'bh25-'+P.serial+'-'+P.wave,P.t-P.previewAt,P.fireAt-P.previewAt);
  if(P.t+1e-6>=P.fireAt){const ports=bh25Ports(b),shots=P.plan.filter(L=>ports.some(p=>p.id===L.id));
   const live=eBullets.filter(q=>!q.dead&&q._bh25Owner===b).length;
   if(live+shots.length<=128){for(const L of shots){const p=ports.find(p=>p.id===L.id);bh25Shot(b,p,L.a);}const p=ports.find(p=>p.id===shots[0]?.id);
    if(p&&shots.length){bh25Flash(b,p,Math.PI/2);combatAudio0927(b,BH25.cfg[P.kind].cue,.32);}}
   bh25Log(b,'wave-release',{wave:P.wave,count:shots.length,live,cap:128});P.wave++;
   if(P.wave<P.waves)bh25Prime(b);else{P.phase='recover';P.recoverAt=P.t;P.plan=[];bh25Log(b,'section-recovery');}
  }
 }else if(P.t-P.recoverAt>=1.65&&!eBullets.some(q=>!q.dead&&q._bh25Owner===b&&q.y>viewTopY()&&q.y<VH+30&&q.x>camLeftX()-20&&q.x<camRightX()+20)){
  const end=P.finish;bh25Log(b,'section-complete',{duration:P.t});delete b._bh25;BH25.owners.delete(b);end();
 }
 return true;
}
function bh25Draw(b){const P=b?._bh25;if(!P||!bh25Valid(b))return;
 if(P.dorsal){const q=P.lob;if(P.phase==='lob'&&q&&!q.dead&&!q.arrived)for(const a of q._bh25Angles)combatWarningDraw(b,{x:q.tx,y:q.ty,ex:q.tx+Math.cos(a)*VH,ey:q.ty+Math.sin(a)*VH,width:10,progress:clamp(q.t/q.warm,0,1),alpha:.16,fieldOnly:true});return;}
 if(P.phase!=='tell')return;const ports=bh25Ports(b),u=clamp((P.t-P.previewAt)/(P.fireAt-P.previewAt),0,1);
 for(const L of P.plan){const p=ports.find(p=>p.id===L.id);if(!p)continue;combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(L.a)*VH*1.5,ey:p.y+Math.sin(L.a)*VH*1.5,width:10,progress:u,alpha:P.wave===0?.30:.10,fieldOnly:true});}
}
enemyOrdnanceElement=function(q){return q?._bh25Owner?null:BH25.base.element.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return !q?._bh25Owner&&BH25.base.intercept.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._bh25Owner){q._weaponProof=true;q._shootable=false;delete q.hp;return;}return BH25.base.rules.apply(this,arguments);};

// Keep the native movement, flashing, collision and module timers running.
razorbackNext=function(b){if(b===subBoss&&b._rzb.state!=='arrival'&&!b._rzb.waves.length&&bh25Due(b,'razor',3)){
 const R=b._rzb;R.attack='bh25';R.at=0;R.charge=0;R.tgt={x:b.x,y:b.y};
 if(bh25Start(b,'razor',()=>BH25.base.rzbNext.call(this,b)))return;
 }return BH25.base.rzbNext.apply(this,arguments);};
razorbackUpdate=function(b,dt){b._bh25Dt=dt;return BH25.base.rzbTick.apply(this,arguments);};
razorbackCombat=function(b){if(b._bh25)return bh25Tick(b,b._bh25Dt||1/60);return BH25.base.rzbCombat.apply(this,arguments);};
er26Next=function(b){const kind=b===subBoss?({magmaward:'reaver',frostcruiser:'frost',olivewarden:'olive'})[b._ship]:null;
 if(b._bh25Queued===kind&&!bh25Ports(b,kind).length)delete b._bh25Queued;
 if(kind&&(b._bh25Queued===kind||bh25Due(b,kind,3))&&bh25Ports(b,kind).length){
  if(kind==='olive'&&(b._sa14?.escortTurn||enemies.some(e=>e._sa14Escort?.owner===b&&!e.dead))){b._bh25Queued=kind;return BH25.base.erNext.apply(this,arguments);}
  delete b._bh25Queued;er26Set(b,'bh25');const R=b._er26;R.to={x:b.x,y:b.y};R.dur=30;R.warnings=[];
  if(bh25Start(b,kind,()=>er26Set(b,'recover')))return;
 }return BH25.base.erNext.apply(this,arguments);};
sa14Escorts=function(b){if((b?._bh25||b?._bh25Queued)&&!b._sa14?.escortTurn)return false;return BH25.base.escorts.apply(this,arguments);};
er26Combat=function(b,dt){if(b._bh25&&b._er26.mode==='bh25')return bh25Tick(b,dt);return BH25.base.erCombat.apply(this,arguments);};
er26WarTick=function(b,dt){if(b._bh25&&b._er26.mode==='bh25')return bh25Tick(b,dt);return BH25.base.erWar.apply(this,arguments);};
hc1007BomberNext=function(b){if(b===subBoss&&bh25Due(b,'bomber',3)&&!b._bomber.bombs.some(q=>!q.dead)&&bh25Ports(b,'bomber').length){
 hc1007BomberSet(b,'recover');b._hc1007.mode='bh25';b._bomber.mode='hc-bh25';if(bh25Start(b,'bomber',()=>hc1007BomberSet(b,'recover')))return;
 }return BH25.base.bomberNext.apply(this,arguments);};
siegeBomberTick=function(b,dt){if(b._bh25?.kind==='bomber'&&!b.dead){const B=b._bomber,H=b._hc1007;B.clock+=dt;B.t+=dt;H.clock+=dt;H.age+=dt;b.flash=Math.max(0,(b.flash||0)-dt);for(const p of B.parts)p.flash=Math.max(0,p.flash-dt);return bh25Tick(b,dt);}
 return BH25.base.bomberTick.apply(this,arguments);};
warhiveTick=function(b,dt){const before=b._cargo13?.mode,r=BH25.base.fortressTick.apply(this,arguments),C=b._cargo13;
 if(b._cargo17Mini&&C?.mode==='recover'&&before!=='recover'&&sc13Open(b)&&C.core>0&&!C.lasers.length&&!C.queue.length&&!C.rockets&&bh25Due(b,'fortress-core',2,true)){
  C.mode='bh25';delete b.er23Reactor;bh25Start(b,'fortress',()=>{C.mode='recover';C.rest=1.2;});
 }if(b._bh25?.kind==='fortress')bh25Tick(b,dt);return r;};
er23Fortress=function(b){if(b?._bh25)return;return BH25.base.reactor.apply(this,arguments);};
s7mNext=function(b){const M=b._s7mod;if(M&&!M.frExit&&!(M.n===2&&!M.od&&b.hp<=b.maxhp*.5)&&!M.counterTell&&bh25Due(b,M.tank?'dredger':'warden',4)){
 s7mSet(b,'bh25');if(bh25Start(b,M.tank?'dredger':'warden',()=>{s7mSet(b,'recover');bh25RestoreCounter(b);}))return;
 }return BH25.base.s7Next.apply(this,arguments);};
s7mTick=function(b,dt){if(b?._bh25&&b._s7mod?.mode==='bh25'&&!b.dead){bm9S7Common(b,dt);b.flash=Math.max(0,(b.flash||0)-dt);b._drawY=b.y;
 if(r25Own7(b)){const G=r25Gait(b);G.speed=0;G.floorRate=0;G.x=b.x;G.y=b.y;G.lastDX=G.lastDY=0;G.feet={};}return bh25Tick(b,dt);}
 return BH25.base.s7Tick.apply(this,arguments);};
hd1003Tell=function(b){if(b===subBoss&&bh25Due(b,'herald',3)){const H=b._hd1003;H.seq++;H.mode='bh25';H.age=0;H.lanes=[];H._hp22=null;H._hd19=null;if(b._hc1007)b._hc1007.cross=null;
 if(bh25Start(b,'herald',()=>{H.mode='rest';H.age=0;H.attackAge=0;}))return;
 }return BH25.base.heraldNext.apply(this,arguments);};
hd1003Tick=function(b,dt){if(b._bh25?.kind==='herald'&&!b.dead){const H=b._hd1003;H.clock+=dt;H.age+=dt;H.attackAge+=dt;b.fireCd=999;b._sba=null;b._drawY=b.y;return bh25Tick(b,dt);}
 return BH25.base.heraldTick.apply(this,arguments);};
s5924Set=function(b,mode){if(mode!=='entry'&&bh25Due(b,'horizon',4)){const r=BH25.base.horizonSet.call(this,b,'spin');const Q=b._s9rift.s5924;Q.angles=[];
 if(bh25Start(b,'horizon',()=>BH25.base.horizonSet.call(this,b,mode))){Q.active=8;Q.warm=b._bh25.warm;return r;}}
 return BH25.base.horizonSet.apply(this,arguments);};
s9VoidHorizonTick=function(b,dt){if(b._bh25?.kind==='horizon'&&!b.dead){const F=b._s9rift,Q=F.s5924;F.t+=dt;Q.t+=dt;Q.age+=dt;F.core.flash=Math.max(0,F.core.flash-dt);b.flash=Math.max(0,(b.flash||0)-dt);return bh25Tick(b,dt);}
 return BH25.base.horizonTick.apply(this,arguments);};
function bh25DrClear(b){return !enemies.some(e=>e._d20?.owner===b&&!e.dead&&e._dyingT==null&&e._d20.phase!=='erase')&&!D20.sparks.some(e=>e.owner===b)&&!D20.blasts.some(e=>e.owner===b);}
v18StartAttack=function(b){const final=v18Owned(b)&&j3State(b).encounter===2&&v18Model(b)==='colossus';
 if(v18Owned(b)&&b._r30.mode==='fight'&&(rb23Host(b)&&rb23Arms(b).length||final&&bh25DrClear(b))&&bh25Due(b,'dracodia-'+j3State(b).encounter,3,final)){
 const N=b._r30.v18,kind=rb23Host(b)?'claws':'dracodia',P=N.attack={type:'bh25',t:0,tell:1.18,active:8,origin:{x:b.x,y:b.y},lanes:[],targets:[]};b._r30.attack=P;
 if(bh25Start(b,kind,()=>{if(kind==='claws')r25FinishAttack(b,P);else{N.attack=null;b._r30.attack=null;b._r30.cd=.8;N.formClock++;}})){P.tell=b._bh25.warm;return;}
 N.attack=null;b._r30.attack=null;
 }return BH25.base.drNext.apply(this,arguments);};
v18AttackTick=function(b,dt){if(b._r30?.v18?.attack?.type==='bh25'&&b._bh25){b._r30.v18.attack.t+=dt;return bh25Tick(b,dt);}return BH25.base.drTick.apply(this,arguments);};
bi24AttackPose=function(b,actor){if(actor==='dracodia'&&rb23Host(b)&&b._bh25?.kind==='claws')return bi24Sample('dracodia_wind',clamp(b._bh25.t/.72,0,1));return BH25.base.drPose.apply(this,arguments);};
rb23DrawWeapon=function(b){if(b._bh25)return;return BH25.base.drWeapon.apply(this,arguments);};
drawSubBoss=function(){const r=BH25.base.drawMini.apply(this,arguments);bh25Draw(subBoss);return r;};
drawBoss=function(){const r=BH25.base.drawBoss.apply(this,arguments);bh25Draw(boss);return r;};
updatePlay=function(){bh25Prune();const r=BH25.base.update.apply(this,arguments);bh25Prune();return r;};
hitSubBoss=function(){const r=BH25.base.miniHit.apply(this,arguments);bh25Prune();return r;};
s7mHit=function(b){const r=BH25.base.s7Hit.apply(this,arguments),M=b?._s7mod;
 if(b?._bh25&&M?.mode==='bh25'&&M.counterTell){M.bh25Counter??=M.counterTell;M.counterTell=null;}bh25Prune();return r;};
modularHit=function(){const r=BH25.base.drHit.apply(this,arguments);bh25Prune();return r;};
// Reuse native pixels at a compact, proportional size in dense sections.
// Nested projectile owners share one scale; collision keeps the native core.
for(const name of ['drawCombatFinalProjectile','drawFireType','razorbackProjectileDraw','ovSonicProjectileDraw','er26ProjectileDraw','s9aProjectileDraw']){
 const base=globalThis[name];if(typeof base!=='function')continue;
 globalThis[name]=function(q){if(!q?._bh25Owner||BH25.rendering)return base.apply(this,arguments);
  const kind=q._bh25Owner._bh25?.kind||q._bh25Kind,k=kind==='razor'?.55:['warden','dredger'].includes(kind)?.58:kind==='herald'?.78:kind==='fortress'?.75:1;
  BH25.rendering=true;ctx.save();ctx.translate(q.x,q.y);ctx.scale(k,k);ctx.translate(-q.x,-q.y);
  try{return base.apply(this,arguments);}finally{ctx.restore();BH25.rendering=false;}
 };
}
globalThis.BOF_BULLETHELL_1025={state:BH25,start:bh25Start,ports:bh25Ports};
