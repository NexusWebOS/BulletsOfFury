"use strict";
/* Stationary Sovereign generators, paved-road reinforcements and shared, counterable
   weapon locks. Use authored hulls, actual live weapon mounts and native ordnance. */
const TARGET17={events:[],clock:0,tanks:0,nextTank:3,base:{begin:beginStage,update:updatePlay,
 set:er26Set,nodes:stage4ShieldSyncNodes,over:mr27Over,bossHit:bossHitTest,
 projectile:er26ProjectileDraw,element:enemyOrdnanceElement,break:ordnanceBreak1002,drawBoss,drawSubBoss}};
function target17Log(type,data={}){TARGET17.events.push({type,time:TARGET17.clock,...data});if(TARGET17.events.length>360)TARGET17.events.shift();}
function target17Rank(){return diffKey==='insanity'?4:diffKey==='furious'?3:diffKey==='hard'?2:diffKey==='normal'?1:0;}

// Detached objectives stay at their station while the hull charges or flies past.
er26Set=function(b,mode){
 if(sa14Storm(b)&&['sa14-drive','sa14-overflight'].includes(mode)&&!b._target17Station){
  stage4ShieldSyncNodes(b);b._target17Station={x:b.x,y:b._drawY??b.y,
   nodes:b._s4war.shield.nodes.map(n=>({x:n.x,y:n.y}))};
 }
 return TARGET17.base.set.apply(this,arguments);
};
stage4ShieldSyncNodes=function(b){
 const A=b?._target17Station;
 if(!sa14Storm(b)||!A)return TARGET17.base.nodes.apply(this,arguments);
 // Rejoin only when the hull has physically returned; never drag a core down a ram lane.
 if(b._er26.mode==='recover'&&Math.hypot(b.x-A.x,(b._drawY??b.y)-A.y)<8){delete b._target17Station;return TARGET17.base.nodes.apply(this,arguments);}
 for(let i=0;i<b._s4war.shield.nodes.length;i++)Object.assign(b._s4war.shield.nodes[i],A.nodes[i]);
};
mr27Over=function(b){const A=b?._sa14;if(!b?._target17Station||!A)return TARGET17.base.over.apply(this,arguments);
 const scale=A.scale;A.scale=1;try{return TARGET17.base.over.apply(this,arguments);}finally{A.scale=scale;}
};
function target17BossContact(b,x,y){
 if(!sa14Storm(b))return bossHitTest(x,y);
 b._s4ShieldHit=null;b._s4CoreHit=null;
 if(b.dead||b.enter||b._noHit||b._sa14?.depth)return false;
 // Shooting still resolves generators and helpers through bossHitTest. Physical
 // contact asks only about the moving authored hull and its mounted weapons.
 const A=b._sa14||{},k=A.scale||1,a=-(A.angle||0),dx=(x-b.x)/k,dy=(y-(b._drawY??b.y))/k;
 const lx=dx*Math.cos(a)-dy*Math.sin(a),ly=dx*Math.sin(a)+dy*Math.cos(a);
 if(Math.abs(lx)<b.w*.34&&Math.abs(ly)<b.h*.43)return true;
 for(const part of b._mr27?.parts||[])if(!part.dead){const q=mr27Shape(b,part.id),ux=x-q.x,uy=y-q.y,c=Math.cos(q.rot||0),s=Math.sin(q.rot||0);
  if(Math.abs(ux*c+uy*s)<q.w*.46&&Math.abs(-ux*s+uy*c)<q.h*.46)return true;}
 return false;
}

// Native modular desert tanks, placed only on the paved middle of the highway.
function target17Highway(dt){
 if(run.stage!==4||target17Rank()<2||bossActive||subBossActive||bossDefeated||stageTimer<2)return;
 TARGET17.nextTank-=dt;if(TARGET17.nextTank>0)return;
 const rank=target17Rank(),cap=rank===2?5:7;
 if(enemies.filter(e=>e._target17Tank&&!e.dead&&e._dyingT==null).length>=cap){TARGET17.nextTank=.6;return;}
 const y=-48,sourceY=levelSrcY()+y,W=worldWidth(),choices=[.50,.42,.58,.35,.65],start=TARGET17.tanks%choices.length;
 let x=null;
 for(let i=0;i<choices.length;i++){const xx=W*choices[(start+i)%choices.length];
  if(tankDrivable(xx,sourceY,false)&&tankDrivable(xx-23,sourceY,false)&&tankDrivable(xx+23,sourceY,false)&&
   (typeof groundTrafficCanPlace!=='function'||groundTrafficCanPlace(xx,y,100,112))){x=xx;break;}}
 if(x==null){TARGET17.nextTank=.5;return;}
 const e=spawnEnemy('sandtank',x,y,{shoots:true});
 if(e){e._target17Tank=true;TARGET17.tanks++;target17Log('highway-tank',{x,y,sourceY});}
 TARGET17.nextTank=rank===2?3.8:rank===3?2.6:2.2;
}

function target17Kind(b){
 if(!b||b.dead)return null;
 if(run.stage===1&&(b._rzb||b._rzbPair))return 'sonic';
 if(run.stage===2&&b._ship==='magmaward')return 'fire';
 if(run.stage===3&&b._ship==='frostcruiser')return 'ice';
 if(run.stage===7&&(b._s7mod||b._ship==='dualscoopdredger'||b._ship==='sludgeemperor'))return 'toxic';
 if(run.stage===8&&(b._r30||b._hd1003))return 'dark';
 if(run.stage===9&&(b._s9fusion||b._s9rift||b._ship==='tidalsovereign'))return b._s9fusion?.phase==='tidal'||b._ship==='tidalsovereign'?'water':'dark';
 return null;
}
function target17Ports(b,kind){
 if(kind==='sonic')return (b._rzbPair?.actors||[b]).map((p,i)=>({id:'sonic-'+i,body:p,pos:()=>rzbWorld(p,0,90)})).filter(v=>!v.body.dead&&v.body._rzb?.pools.turret>0&&v.body._rzb.state!=='arrival');
 if(kind==='fire'||kind==='ice')return ['L','R',...(kind==='ice'?['ROCKET_L','ROCKET_R']:[])].filter(s=>mr27CanFire(b,s)).map(slot=>({id:slot,slot,pos:()=>shipBossMount(b,slot)}));
 if(b._s7mod)return b._s7mod.parts.filter(p=>p.id.startsWith('gun')&&p.hp>0).map(p=>({id:p.id,pos:()=>s7mMuzzle(b,p.id)}));
 if(b._hd1003)return b._hd1003.parts.filter(p=>p.id.startsWith('gun')&&hd1003Live(b,p)).map(p=>({id:p.id,pos:()=>hd1003Live(b,p)?hd1003Muzzle(b,p.id):null}));
 if(b._r30&&fmcLive(b)&&b._r30.form>0)return fmcRig(b).filter(v=>v.spec.tags?.length).map(v=>({id:v.p.id,pos:()=>{const q=fmcRig(b).find(q=>q.p.id===v.p.id);return q?fmcPoint(q,...(q.spec.emit||[.5,.76])):null;}}));
 if(b._s9fusion?.phase==='twins')return [b._s9fusion.left,b._s9fusion.right].map((w,i)=>({id:'sentinel-'+i,body:w,pos:()=>({x:w.x,y:w.y+38})})).filter(v=>v.body&&!v.body.disabled&&v.body.hp>0);
 if(kind==='water'&&b._ship==='tidalsovereign')return ['L','R'].map(slot=>({id:'tidal-'+slot,pos:()=>shipBossMount(b,slot)}));
 if(b._s9rift?.core){const w=b._s9rift.core;return w.disabled||w.hp<=0?[]:[{id:'rift-core',pos:()=>({x:w.x,y:w.y+38})}];}
 const pieces=retinaBossTargets(b).filter(p=>!p.dead&&/gun|rack|cannon|left|right|turret|arm/i.test(p._retinaId||p.part?.id||p.kind||''));
 return pieces.map((p,i)=>({id:p._retinaId||p.part?.id||'weapon-'+i,pos:()=>p.dead?null:({x:p.x,y:p.y})}));
}
function target17Ready(b,ports){
 if(!b||b.dead||b.dying||b.enter||b._noHit||b._scene||b._jcGhost||b._mr27?.stun>0)return false;
 if(b._r30&&b._r30.mode!=='fight')return false;
 if(b._s7mod&&['portal','entry','roar','jump','drop','dead','overdrive'].includes(b._s7mod.mode))return false;
 if(b._hd1003&&!['rest','tell','fire'].includes(b._hd1003.mode))return false;
 if(b._s9fusion&&!['twins','tidal'].includes(b._s9fusion.phase))return false;
 return ports.some(p=>{const q=p.pos();return q&&q.x>camLeftX()+20&&q.x<camRightX()-20&&q.y>PLAY.y+18&&q.y<VH-60;});
}
function target17Warm(){
 for(let i=0;i<4;i++){XART.rdy('retm_'+i);XART.rdy('retmb_'+i);}
 for(let i=0;i<16;i++)XART.rdy('pt11_sonic_pulse_'+i);
 for(let i=0;i<8;i++)XART.rdy('l23fx_inferno_mg_'+i);
 for(let i=0;i<6;i++){XART.rdy('bfx_cryo_p_'+i);XART.rdy('bfx_cryo_m_'+i);}
 Snd.prepare?.(['lockon','enemyMachineGunHeavy','missile','bossWeaponCharge','expIce','colePressureImpact']);
}
function target17Emit(b,T,port,rocket){
 let p=port.pos();if(!p)return;const rank=target17Rank(),a=Math.atan2(T.aim.y-p.y,T.aim.x-p.x),kind=T.kind;
 if(port.slot){mr27Fire(b,port.slot,a);p=port.pos();}
 let q;
 if(kind==='sonic'){
  q=eShootT(p.x,p.y,a,2.5+rank*.18,'emissile',{w:32,h:40,silent:true});
  Object.assign(q,{_target17Art:'sonic',_target17Guide:{target:T.target,t:0,for:1.35,turn:1.05},hp:4+Math.min(2,rank),_shootable:true,_weaponProof:false});
  (Audio.SFX.missile||Audio.SFX.bossWeaponCharge)?.();
 }else if(kind==='fire'||kind==='ice'){
  q=eShootT(p.x,p.y,a,(rocket?2.5:3.1)+rank*.16,rocket?'emissile':'mg',{w:rocket?12:7,h:rocket?24:16,silent:true});
  Object.assign(q,{_target17Art:rocket?'ice-missile':kind,_shootable:!!rocket,_weaponProof:!rocket,mg:!rocket,hp:rocket?2:undefined});
  (rocket?Audio.SFX.missile:Audio.SFX.enemyMachineGunHeavy)?.();
 }else if(kind==='toxic')q=s7BossShot(p.x,p.y,a,3.0+rank*.15,'s7acid',{silent:true,w:10,h:18});
 else if(kind==='water')q=s9aShot(p.x,p.y,a,2.7+rank*.15,'tidaltorp',{silent:true});
 else q=eShootT(p.x,p.y,a,3.1+rank*.15,'s9needle',{w:10,h:28,silent:true});
 if(!q||q.dead)return;
 if(q._target17Art)q._er26Art=kind;
 Object.assign(q,{_target17Owner:b,_target17Port:port.id,_target17Element:kind,_target17Age:0,_noArsenal:true,homing:false,_committed:true});
 if(kind!=='sonic'&&kind!=='fire'&&kind!=='ice'){q._shootable=false;q._weaponProof=true;(Audio.SFX.enemyHeavyLaser||Audio.SFX.enemyMachineGunHeavy)?.();}
 if(port.slot)shipBossMuzzleStart(b,[port.slot],{fam:kind==='ice'?'cryo':kind==='fire'?'magma':'mg',life:.13,hpx:34});
 else wm26Emit(b,p.x,p.y,a,kind==='sonic'?'sonic':'orb',kind==='toxic'?'#8fdc61':null,{size:38,life:.14});
 T.shots++;target17Log('weapon-shot',{kind,port:port.id,x:p.x,y:p.y,rocket:!!rocket,serial:T.serial});
}
function target17Tick(b,dt){
 const kind=target17Kind(b);if(!kind)return;
 const ports=target17Ports(b,kind),early=['fire','ice'].includes(kind),rank=target17Rank();
 const T=b._target17||(b._target17={phase:'recover',t:0,cool:kind==='sonic'?2.3:1,serial:0,shots:0,kind});
 T.kind=kind;
 if(!target17Ready(b,ports)){T.phase='recover';T.cool=.65;T.t=0;return;}
 if(T.phase==='recover'){
  T.cool-=dt;if(T.cool>0)return;
  T.target=targetShip(b.x,b.y);if(!T.target||T.target.dead)return;
  T.aim={x:T.target.x,y:T.target.y};T.phase='track';T.t=0;T.serial++;T.beep=0;T.shot=0;T.rocket=0;T.waves=0;
  T.warm=[1.45,1.15,1.0,.90,.86][rank];T.live=early?2.4:kind==='sonic'?.1:.75;T.ids=ports.map(p=>p.id);
  target17Log('tracking',{kind,serial:T.serial,ports:T.ids});
 }
 T.t+=dt;
 const live=ports.filter(p=>T.ids.includes(p.id));
 if(!live.length){T.phase='recover';T.cool=.65;return;}
 if(T.phase==='track'){
  if(T.t<T.warm-.40&&!T.target.dead)T.aim={x:T.target.x,y:T.target.y};
  T.beep-=dt;if(T.beep<=0){Audio.SFX.lockon?.();T.beep=.18;}
  if(b._er26)b._er26.target={...T.aim};
  for(const port of live)if(port.slot){const p=port.pos();mr27Fire(b,port.slot,Math.atan2(T.aim.y-p.y,T.aim.x-p.x));}
  if(T.t<T.warm)return;
  T.phase='fire';T.t=0;target17Log('target-locked',{kind,serial:T.serial,aim:{...T.aim}});
 }
 if(T.phase==='fire'){
  T.shot-=dt;T.rocket-=dt;
  if(T.shot<=0){
   const guns=live.filter(p=>!p.slot?.startsWith('ROCKET'));
   if(kind==='sonic'){if(T.waves===0&&guns.length)target17Emit(b,T,guns[(T.serial-1)%guns.length],false);}
   else if(early){for(const port of guns)target17Emit(b,T,port,false);}
   else if(live.length){target17Emit(b,T,live[T.waves%live.length],false);}
   T.waves++;T.shot=early?[.22,.16,.14,.12,.11][rank]:.24;
  }
  if(kind==='ice'&&T.rocket<=0){for(const port of live.filter(p=>p.slot?.startsWith('ROCKET')))target17Emit(b,T,port,true);T.rocket=.95;}
  if(T.t>=T.live){T.phase='recover';T.cool=early?.50:kind==='sonic'?5.8:5.5-Math.min(3,rank)*.45;T.t=0;}
 }
}
function target17Draw(b){
 const T=b?._target17;if(!T||T.phase!=='track'||b.dead||b._noHit)return;
 const k=clamp(T.t/T.warm,0,1),locked=T.t>=T.warm-.4,r=locked?0:(1-k)*22;
 const x=T.aim.x+Math.cos(T.t*TAU*1.4)*r,y=T.aim.y+Math.sin(T.t*TAU*1.4)*r;
 ph8Icon(ctx,(locked?'retmb_':'retm_')+Math.floor(T.t*16)%4,x,y,56);
 for(const port of target17Ports(b,T.kind).filter(p=>T.ids.includes(p.id))){const p=port.pos();if(!p)continue;
  combatWarningDraw(b,{x:p.x,y:p.y,ex:T.aim.x,ey:T.aim.y,width:T.kind==='sonic'?54:24,progress:k,fieldOnly:true});}
 combatWarningDraw(b,{x:b.x,y:b.y,ex:x,ey:y,width:1,progress:k,alertOnly:true,alertX:b.x,alertY:Math.max(PLAY.y+24,b.y-b.h*.44-22)});
}
er26ProjectileDraw=function(q){
 const art=q._target17Art;if(!art)return TARGET17.base.projectile.apply(this,arguments);
 const age=q._target17Age||0,sonic=art==='sonic',key=sonic?'pt11_sonic_pulse_'+Math.floor(age*16)%16:
  art==='fire'?'l23fx_inferno_mg_'+Math.floor(age*16)%8:'bfx_cryo_'+(art==='ice-missile'?'m_':'p_')+Math.floor(age*14)%6;
 if(!XART.rdy(key))return true;const im=XART.get(key),size=sonic?72:art==='fire'?28:art==='ice-missile'?34:22;
 const h=sonic?size:size*(im.height||im.naturalHeight)/(im.width||im.naturalWidth);
 ctx.save();ctx.translate(q.x,q.y);if(!sonic)ctx.rotate(Math.atan2(q.vy,q.vx)-Math.PI/2);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-size/2,-h/2,size,h);ctx.restore();return true;
};
enemyOrdnanceElement=function(q){
 // The legacy elemental-orb adapter makes every classified object shootable.
 // Gun bullets retain their gun rules; later native ordnance keeps its own family.
 if(q?._target17Owner){if(q.mg)return null;if(['sonic','fire','ice'].includes(q._target17Element))return q._target17Element;}
 return TARGET17.base.element.apply(this,arguments);
};
ordnanceBreak1002=function(q){
 if(q._target17Art==='sonic'){
  if(!q._fbImpact1002){q._fbImpact1002=true;sonicImpact(q.x,q.y,.8);}
  return;
 }
 return TARGET17.base.break.apply(this,arguments);
};
beginStage=function(){TARGET17.clock=0;TARGET17.nextTank=3;TARGET17.tanks=0;TARGET17.events=[];target17Warm();return TARGET17.base.begin.apply(this,arguments);};
updatePlay=function(dt){
 for(const q of eBullets)if(q._target17Owner&&!q.dead){q._target17Age+=dt;
  const G=q._target17Guide;if(G){G.t+=dt;if(G.t<G.for&&G.target&&!G.target.dead){const a=Math.atan2(q.vy,q.vx),want=Math.atan2(G.target.y-q.y,G.target.x-q.x),ang=a+clamp(stage4AngleDelta(a,want),-G.turn*dt,G.turn*dt),speed=Math.hypot(q.vx,q.vy);q.vx=Math.cos(ang)*speed;q.vy=Math.sin(ang)*speed;}}
  if(q._target17Age>5.0){q.dead=true;if(G)ordnanceBreak1002(q);}}
 const r=TARGET17.base.update.apply(this,arguments);
 let alive=false;for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out)alive=true;});
 if(state!==GS.PLAY||!alive||story||fb2Talk)return r;
 TARGET17.clock+=dt;target17Highway(dt);for(const b of [subBossActive?subBoss:null,bossActive?boss:null])target17Tick(b,dt);return r;
};
drawSubBoss=function(){const r=TARGET17.base.drawSubBoss.apply(this,arguments);if(subBossActive)target17Draw(subBoss);return r;};
drawBoss=function(){const r=TARGET17.base.drawBoss.apply(this,arguments);if(bossActive)target17Draw(boss);return r;};
