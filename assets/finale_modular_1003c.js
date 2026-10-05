"use strict";
/* Mike 1003c: EVERY finale identity is a real component rig. Render, Retina,
   collision, recoil and emitters use the same forward-kinematic poses. */
for(const a of Object.values(FMC_ART))XART._src[a.key]=a.path;
const FMC_BASE={form:r30Form,parts:r30Parts,pose:r30Pose,warm:r30Warm,attack:r30Attack,
 tick:r30Tick,hit:modularHit,body:f1003bBodyDraw,muzzles:f1003bMuzzles,bar:drawHealthBarV2,
 knightEnter:s81003KnightEnter,knightTick:f1003bKnightTick,shot:f1003bShot,shield:r30ShieldBounds};
function fmcNode(id,art,x,y,w,h,opt={}){return{id,art,x,y,w,h,px:.5,py:.15,hp:.12,z:2,...opt};}
const FMC_RIGS={
 chopper:[
  fmcNode('core','core',0,8,143,190,{py:.5,z:1}),
  fmcNode('tail','tail',0,-75,98,108,{py:.92,z:0,hp:.08}),
  fmcNode('left','left',-55,-30,55,115,{px:.59,py:.15,tags:['rotorMG','code'],emit:[.43,.81]}),
  fmcNode('right','right',55,-30,55,115,{px:.41,py:.15,tags:['rotorMG','code'],emit:[.57,.81]}),
  fmcNode('rackL','rackL',-88,-15,53,95,{py:.16,tags:['missiles','bombing'],emit:[.5,.80]}),
  fmcNode('rackR','rackR',88,-15,53,95,{py:.16,tags:['missiles','bombing'],emit:[.5,.80]}),
  fmcNode('rotor','chopper_rotor',0,-58,232,232,{legacy:true,py:.5,z:4,hp:.10,hit:.30})],
 furnace:[
  fmcNode('core','core',0,-20,150,192,{py:.5,z:1}),
  fmcNode('legL','legL',-33,48,64,111,{py:.16,z:0,hp:.07,role:'leg'}),
  fmcNode('legR','legR',33,48,64,111,{py:.16,z:0,hp:.07,role:'leg'}),
  fmcNode('left','left',-61,-32,85,158,{px:.71,py:.24,role:'claw',tags:['magma','furnaceBeam'],emit:[.44,.58]}),
  fmcNode('right','right',61,-32,85,158,{px:.29,py:.24,role:'claw',tags:['magma','furnaceBeam'],emit:[.56,.58]}),
  fmcNode('reactor','reactor',0,7,48,49,{py:.5,z:3,hp:.10,tags:['furnaceBeam'],emit:[.5,.63]})],
 cryo:[
  fmcNode('core','core',0,0,144,227,{py:.5,z:1}),
  ...[-1,1].flatMap(s=>[
   fmcNode('rack'+(s<0?'L':'R'),'rack'+(s<0?'L':'R'),s*48,-62,67,85,{px:s<0?.76:.24,py:.32,tags:['iceMG'],emit:[.5,.71]}),
   fmcNode('gun'+(s<0?'L':'R')+'1',s<0?'left':'right',s*43,-15,52,109,{px:s<0?.51:.49,py:.14,tags:['iceMG','iceLance'],emit:[s<0?.65:.35,.86]}),
   fmcNode('gun'+(s<0?'L':'R')+'2',s<0?'left':'right',s*36,39,43,87,{px:.5,py:.14,tags:['iceMG','iceLance'],emit:[s<0?.65:.35,.86]})])],
 storm:[
  fmcNode('core','core',0,0,196,226,{sheet:'storm_hull',py:.5,z:1}),
  fmcNode('left','left',-45,27,69,112,{px:.60,py:.18,tags:['code'],emit:[.67,.92]}),
  fmcNode('right','right',45,27,69,112,{px:.40,py:.18,tags:['code'],emit:[.33,.92]}),
  fmcNode('rackL','rackL',-51,-44,61,117,{px:.62,py:.20,tags:['missiles'],emit:[.56,.81]}),
  fmcNode('rackR','rackR',51,-44,61,117,{px:.38,py:.20,tags:['missiles'],emit:[.44,.81]}),
  fmcNode('lightning','lightning',0,-65,48,186,{px:.42,py:.09,z:3,hp:.18,tags:['lightning'],emit:[.53,.82]})],
 knight:[
  fmcNode('core','core',0,0,126,140,{py:.5,z:1}),
  fmcNode('legL','legL',-35,51,55,101,{px:.40,py:.11,z:0,hp:.07,role:'leg'}),
  fmcNode('legR','legR',35,51,55,101,{px:.60,py:.11,z:0,hp:.07,role:'leg'}),
  fmcNode('head','head',0,-57,91,85,{sheet:'head',py:.91,z:4,hp:.10}),
  fmcNode('swordArm','swordArm',-53,-40,62,108,{px:.29,py:.22,hp:.13}),
  fmcNode('shieldArm','shieldArm',53,-40,62,108,{px:.78,py:.22,hp:.11}),
  fmcNode('sword','sword',7,78,51,139,{parent:'swordArm',px:.51,py:.15,z:4,hp:.16}),
  fmcNode('shield','shield',-18,63,78,112,{parent:'shieldArm',py:.42,z:5,hp:.13})],
 harrier:[
  fmcNode('core','core',0,0,158,218,{py:.5,z:1}),
  fmcNode('fanL','fanL',-68,3,100,104,{px:.90,py:.45,z:0,hp:.13,role:'fan'}),
  fmcNode('fanR','fanR',68,3,100,104,{px:.10,py:.45,z:0,hp:.13,role:'fan'}),
  fmcNode('rackL','rackL',-98,52,69,81,{px:.9,py:.40,tags:['missiles'],emit:[.42,.77]}),
  fmcNode('rackR','rackR',98,52,69,81,{px:.1,py:.40,tags:['missiles'],emit:[.58,.77]}),
  fmcNode('beam','beam',0,8,48,92,{py:.15,z:3,hp:.17,tags:['carrierLance'],emit:[.5,.87]})],
 warden:[
  fmcNode('core','core',0,-25,168,190,{py:.5,z:1}),
  fmcNode('legL','legL',-46,42,77,116,{px:.59,py:.13,z:0,hp:.09,role:'leg'}),
  fmcNode('legR','legR',46,42,77,116,{px:.41,py:.13,z:0,hp:.09,role:'leg'}),
  fmcNode('left','left',-68,-50,78,128,{px:.67,py:.28,role:'claw',tags:['scissor'],emit:[.33,.81]}),
  fmcNode('right','right',68,-50,78,128,{px:.33,py:.28,role:'claw',tags:['scissor'],emit:[.67,.81]}),
  fmcNode('gunL','gun',-50,-6,69,99,{py:.19,z:3,hp:.13,tags:['wardenMG','code'],emit:[.5,.76]}),
  fmcNode('gunR','gun',50,-6,69,99,{py:.19,z:3,hp:.13,tags:['wardenMG','code'],emit:[.5,.76]})]
};
function fmcLive(b){return !!b?._r30?.modular1003c;}
function fmcAlive(b,id){return b.parts.some(p=>p.id===id&&!p.destroyed);}
r30Warm=function(){F1003B_BASE.warm();bossBarWarm(8);for(const a of Object.values(FMC_ART))XART.rdy(a.key);
 if(typeof Snd!=='undefined'&&Snd.prepare)Snd.prepare('enemyMachineGunHeavy');};
r30Form=function(b,n){
 FMC_BASE.form.apply(this,arguments);const S=b._r30;S.modular1003c=true;S.gaugeLife=null;
 const rig=FMC_RIGS[f1003bDef(b).id];if(!rig)return;
 b.parts=rig.map(v=>({id:v.id,rc:v.id+'_module',dmg:true,hp:v.id==='core'?b.hp:Math.ceil(b.maxhp*v.hp),
  maxhp:v.id==='core'?b.hp:Math.ceil(b.maxhp*v.hp),destroyed:false,flash:0,kick:0,spec:v}));
};
function fmcKnightAngles(K){
 if(!K)return{arm:.30,wrist:0,shield:-.15};const u=clamp(K.age/s81003KnightDur(K.phase),0,1),ease=u*u*(3-2*u);
 switch(K.phase){
 case 'guard':return{arm:.30,wrist:0,shield:-.65};
 case 'slashTell':return{arm:lerp(.3,2.3,ease),wrist:lerp(0,-.5,ease),shield:-.15};
 case 'slash':return{arm:lerp(2.3,-.5,ease),wrist:lerp(-.5,-1.4,ease),shield:.1};
 case 'jumpTell':return{arm:lerp(.3,2.65,ease),wrist:lerp(0,-.5,ease),shield:-.15};
 case 'jump':{const v=clamp((u-.58)/.42,0,1);return{arm:lerp(2.65,.2,v*v),wrist:lerp(-.5,-.3,v*v),shield:-.3};}
 case 'land':return{arm:.2,wrist:-.3,shield:-.3};
 case 'followTell':return{arm:lerp(.2,1.3,ease),wrist:lerp(-.3,.5,ease),shield:-.15};
 case 'sweep':return{arm:lerp(1.3,-1.3,ease),wrist:lerp(.5,-.5,ease),shield:.2};
 case 'slashRecover':return{arm:lerp(-.5,.3,ease),wrist:lerp(-1.4,0,ease),shield:-.15};
 default:return{arm:.3,wrist:0,shield:-.15};
 }
}
r30Pose=function(b){
 if(!fmcLive(b)||!b._r30.attack?.k1003)return FMC_BASE.pose.apply(this,arguments);
 const K=b._r30.attack.k1003,phase=K.phase,u=clamp(K.age/s81003KnightDur(phase),0,1);
 let x=K.x,y=K.y,alpha=1,scale=1;
 if(phase==='slash'){const v=1-(1-u)**3;x=lerp(K.from.x,K.target.x,v);y=lerp(K.from.y,K.target.y-118,v);}
 if(phase==='jump'){x=lerp(K.from.x,K.target.x,u);y=lerp(K.from.y,K.target.y-135,u)-Math.sin(u*Math.PI)*122;scale=1+.18*Math.sin(u*Math.PI);}
 if(phase==='followTell')y=lerp(K.y,K.target.y-142,u*u*(3-2*u));
 if(phase==='recover'){x=lerp(K.x,K.home.x,u);y=lerp(K.y,K.home.y,u);}
 if(phase==='out')alpha=1-u;if(phase==='in'){x=K.home.x;y=K.home.y;alpha=u;}
 return{x,y,alpha,scale,angle:0,shape:'knight'};
};
function fmcPoint(v,nx,ny){const dx=(nx-v.spec.px)*v.w,dy=(ny-v.spec.py)*v.h,c=Math.cos(v.rot),s=Math.sin(v.rot);return{x:v.ax+dx*c-dy*s,y:v.ay+dx*s+dy*c};}
function fmcRig(b){
 const D=f1003bDef(b),specs=FMC_RIGS[D.id];if(!specs)return FMC_BASE.parts(b);
 const Q=r30Pose(b),S=b._r30,P=S.attack,K=P?.k1003,T=S.clock||0,k=Q.scale||1,parts=[],nodes={};
 const angles=fmcKnightAngles(K);
 for(const v of specs){
  const p=b.parts.find(p=>p.id===v.id);if(!p||p.destroyed)continue;
  const parent=v.parent?nodes[v.parent]:null;if(v.parent&&!parent)continue;
  let ax=Q.x+v.x*k,ay=Q.y+v.y*k,rot=0;
  if(parent){const c=Math.cos(parent.rot),s=Math.sin(parent.rot);ax=parent.ax+(v.x*c-v.y*s)*k;ay=parent.ay+(v.x*s+v.y*c)*k;rot=parent.rot;}
  const side=Math.sign(v.x)||1;
  if(v.role==='leg')rot=side*.09+Math.sin(T*2.6+side)*.065*(K?.phase==='jump'?3:1);
  if(v.id==='head')rot=Math.sin(T*1.7)*.045;
  if(v.role==='claw')rot=side*(-.08+Math.sin(T*1.6)*.055+(P?.type==='scissor'?Math.sin(clamp((P.t-P.tell)/P.active,0,1)*Math.PI)*.85:0));
  if(v.role==='fan')rot=Math.sin(T*2.2+side)*.10;
  if(v.tags&&P&&!K){const a=Math.atan2(P.ty-ay,P.tx-ax)-Math.PI/2;rot+=clamp(a,-.42,.42);}
  if(v.id==='rotor')rot=T*(fmcAlive(b,'tail')?15:9);
  if(D.id==='knight'){
   if(v.id==='swordArm')rot=angles.arm;if(v.id==='shieldArm')rot=angles.shield;if(v.id==='sword')rot+=angles.wrist;
   // The downward strike's wrist aims the real blade at the committed target.
   // Its tip, not a disconnected target-circle, supplies collision below.
   if(v.id==='sword'&&K&&['jump','land'].includes(K.phase)){
    const aim=Math.atan2(K.target.y-ay,K.target.x-ax)-Math.PI/2;
    rot=lerp(rot,aim,K.phase==='land'?1:clamp((K.age/.68-.55)/.45,0,1));
   }
  }
  const recoil=(p.kick||0)/.13*7*k;ax+=Math.sin(rot)*recoil;ay-=Math.cos(rot)*recoil;
  const n={p,spec:v,ax,ay,w:v.w*k,h:v.h*k,rot,key:'fmc_'+(v.sheet||D.id),alpha:Q.alpha??1,z:v.z};
  const mid=fmcPoint(n,.5,.5);n.x=mid.x;n.y=mid.y;parts.push(n);nodes[v.id]=n;
 }
 return parts;
}
r30Parts=function(b){
 if(!fmcLive(b)||b._r30.form===0)return FMC_BASE.parts.apply(this,arguments);
 return fmcRig(b).map(v=>({...v,w:v.w*(v.spec.hit||1),h:v.h*(v.spec.hit||1)}));
};
f1003bMuzzles=function(b){
 if(!fmcLive(b)||b._r30.form===0)return FMC_BASE.muzzles.apply(this,arguments);
 const P=b._r30.attack,type=P?.type||f1003bDef(b).book[0],parts=fmcRig(b);
 let selected=parts.filter(v=>v.spec.tags?.includes(type));
 // Code/gravity belongs to the surviving reactor even after a complete disarm.
 if(!selected.length&&type==='code')selected=parts.filter(v=>v.p.id==='core');
 return selected.map(v=>{const q=fmcPoint(v,...(v.spec.emit||[.5,.76]));return{...q,side:Math.sign(v.spec.x),module:v.p.id};});
};
function fmcAvailable(b,type){
 if(!fmcLive(b))return true;const id=f1003bDef(b).id;
 if(type==='knight')return fmcAlive(b,'sword')&&fmcAlive(b,'swordArm');
 if(type==='turbines')return fmcAlive(b,'fanL')||fmcAlive(b,'fanR');
 if(type==='talons')return fmcAlive(b,'left')||fmcAlive(b,'right');
 if(['gravity','orbit','iceOrbit','eruptions','ram','stomp','code'].includes(type))return true;
 return b.parts.some(p=>!p.destroyed&&p.spec?.tags?.includes(type))||id==='host';
}
r30Attack=function(b){
 if(!fmcLive(b))return FMC_BASE.attack.apply(this,arguments);
 const S=b._r30,D=f1003bDef(b);for(let i=0;i<D.book.length&&!fmcAvailable(b,D.book[S.seq%D.book.length]);i++)S.seq++;
 FMC_BASE.attack(b);const P=S.attack;
 // The old Storm source was a guessed hull coordinate. Bind its lane to the
 // actual independently aimed lightning barrel, just like every other laser.
 if(P.type==='lightning')P.lanes=f1003bMuzzles(b).map(m=>({...s81003Lane(m.x,m.y,P.tx,P.ty,22),tx:P.tx,ty:P.ty,module:m.module}));
};
f1003bShot=function(b,x,y){
 const q=FMC_BASE.shot.apply(this,arguments);if(q&&fmcLive(b)){
  const ports=f1003bMuzzles(b);let best=null,dist=Infinity;for(const v of ports){const d=Math.hypot(v.x-x,v.y-y);if(d<dist){best=v;dist=d;}}
  const part=best&&b.parts.find(p=>p.id===best.module);if(part){part.kick=.13;q._fmcModule=part.id;}
 }return q;
};
modularHit=function(dmg){
 const b=boss;if(!fmcLive(b))return FMC_BASE.hit.apply(this,arguments);
 const was=new Set(b.parts.filter(p=>p.destroyed).map(p=>p.id));const result=FMC_BASE.hit.apply(this,arguments);
 for(const p of b.parts)if(p.destroyed&&!was.has(p.id)){
  const descendants=new Set([p.id]);let changed=true;
  while(changed){changed=false;for(const q of b.parts)if(!q.destroyed&&q.spec?.parent&&descendants.has(q.spec.parent)){q.destroyed=true;q.hp=0;descendants.add(q.id);changed=true;}}
  const S=b._r30;if(S.attack?.lanes)S.attack.lanes=S.attack.lanes.filter(q=>!descendants.has(q.module));
  S81003.beams=S81003.beams.filter(q=>q.owner!==b||!descendants.has(q.module));
  if(descendants.has('shield')||descendants.has('shieldArm'))S.shield=0;
  if((descendants.has('sword')||descendants.has('swordArm'))&&S.attack?.k1003){S.attack=null;S.shield=0;S.cd=1.65;f1003bLog(b,'disarmRecovery');}
 }
 return result;
};
s81003KnightEnter=function(b,phase){
 FMC_BASE.knightEnter.apply(this,arguments);if(!fmcLive(b))return;
 const K=b._r30.attack.k1003;K.previousBlade=null;K.hitSeats=new Set();
 if(phase==='guard'&&(!fmcAlive(b,'shield')||!fmcAlive(b,'shieldArm')))b._r30.shield=0;
 if(phase==='followTell')r30Sound('bossWeaponCharge');
};
function fmcBlade(b){const v=fmcRig(b).find(v=>v.p.id==='sword');if(!v)return null;const a=fmcPoint(v,.5,.36),z=fmcPoint(v,.5,.94);return{x:a.x,y:a.y,ex:z.x,ey:z.y,width:17*(r30Pose(b).scale||1)};}
function fmcBladeHit(b){
 const K=b._r30.attack.k1003,L=fmcBlade(b);if(!L)return;const previous=K.previousBlade||L;K.previousBlade=L;
 for(const seat of seatList())withSeat(seat,()=>{
  if(K.hitSeats.has(seat)||player.dead)return;
  for(let i=0;i<=5;i++){const u=i/5,l={x:lerp(previous.x,L.x,u),y:lerp(previous.y,L.y,u),ex:lerp(previous.ex,L.ex,u),ey:lerp(previous.ey,L.ey,u)};
   if(s81003Distance(player.x,player.y,l)<L.width*.5+3){playerHit('powered alien sword '+K.phase);K.hitSeats.add(seat);break;}}
 });
}
f1003bKnightTick=function(b,dt){
 if(!fmcLive(b))return FMC_BASE.knightTick.apply(this,arguments);
 const S=b._r30,P=S.attack,K=P.k1003;P.t+=dt;K.age+=dt;
 const phase=K.phase,dur=s81003KnightDur(phase)+(phase==='recover'?.9:0);
 if(['slashTell','jumpTell','followTell'].includes(phase))combatWarningTick(b,'finale-knight-'+P.seq+'-'+P.kIndex,K.age,dur);
 if(['slash','land','sweep'].includes(phase)||(phase==='jump'&&K.age>.50))fmcBladeHit(b);
 if(phase==='land'&&!K.orbs){K.orbs=true;f1003bRing(b,K.target.x,K.target.y,7,'code',.42);}
 if(K.age<dur)return;const Q=r30Pose(b);K.x=Q.x;K.y=Q.y;const next=P.kSteps[++P.kIndex];
 if(next){K.orbs=false;s81003KnightEnter(b,next);return;}S.attack=null;S.shield=0;S.cd=2;f1003bLog(b,'recover',{seconds:2});
};
r30Tick=function(b,dt){
 if(fmcLive(b)){
  for(const p of b.parts){p.kick=Math.max(0,(p.kick||0)-dt);p.flash=Math.max(0,(p.flash||0)-dt);}
  const S=b._r30;if(S.mode==='takeover'){const n=fmcGauge(b).charge;if(n!==S.gaugeLife&&n>=0){S.gaugeLife=n;r30Sound('combatEnergy0927');}}
 }
 const result=FMC_BASE.tick.apply(this,arguments);
 if(fmcLive(b)){const P=b._r30.attack;if(P?.started&&P.lanes?.length&&!P.recoil1003c){P.recoil1003c=true;
  for(const L of P.lanes){const p=b.parts.find(p=>p.id===L.module);if(p)p.kick=.13;}}}
 return result;
};
function fmcCell(sheet,part,x,y,w,h,rot=0,alpha=1,tint=null){
 const a=FMC_ART[sheet],r=a?.rects[part];if(!r||!XART.rdy(a.key))return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(tint?xartTint(a.key,tint,1):XART.get(a.key),...r,-w/2,-h/2,w,h);ctx.restore();return true;
}
function fmcWhiteBlit(key,x,y,w,h,rot=0,alpha=1){
 const im=xartTint(REALM30_ART[key]?'r30_'+key:key,'#ffffff',1);if(!im)return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();return true;
}
function fmcCharge(b){
 const K=b._r30.attack?.k1003;if(!K)return null;
 if(['slashTell','jumpTell','followTell'].includes(K.phase))return{frame:Math.min(5,Math.floor(clamp(K.age/s81003KnightDur(K.phase),0,1)*6)),alpha:1};
 if(['jump','slash','land','sweep'].includes(K.phase))return{frame:K.phase==='jump'&&K.age<.50?5:6,alpha:.85};
 if(K.phase==='slashRecover'&&K.age<.18)return{frame:7,alpha:1-K.age/.18};return null;
}
f1003bBodyDraw=function(b,alpha=1){
 if(!fmcLive(b)||b._r30.form===0)return FMC_BASE.body.apply(this,arguments);
 const S=b._r30,D=f1003bDef(b),K=S.attack?.k1003,rig=fmcRig(b),charge=fmcCharge(b);
 if(K){const u=clamp(K.age/s81003KnightDur(K.phase),0,1);
  if(['slashTell','jumpTell','followTell'].includes(K.phase)){
   s81003Target(K.target.x,K.target.y,130,u);
   if(K.phase!=='jumpTell')s81003Fov({x:K.target.x-125,y:K.target.y,ex:K.target.x+125,ey:K.target.y,width:34},u,false);
  }
  if(K.phase==='out'||K.phase==='in')s81003Cell('teleport',Math.min(7,Math.floor(u*8)),K.phase==='out'?K.x:K.home.x,K.phase==='out'?K.y:K.home.y,245,320,.95);
 }
 for(const v of rig.sort((a,b)=>a.z-b.z)){
  const a=alpha*v.alpha,part=v.spec.art,sheet=v.spec.sheet||D.id;
  if(v.spec.legacy)r30Blit(part,v.x,v.y,v.w,v.h,v.rot,a);else fmcCell(sheet,part,v.x,v.y,v.w,v.h,v.rot,a);
  if(v.spec.tags?.includes(S.attack?.type)&&S.attack.t<S.attack.tell){
   const u=S.attack.t/S.attack.tell;ctx.save();ctx.globalCompositeOperation='lighter';
   fmcCell(sheet,part,v.x,v.y,v.w,v.h,v.rot,a*u*(.18+.18*(.5+.5*Math.sin(S.clock*22))));ctx.restore();
  }
  const hit=Math.max(v.p.flash||0,b.flash||0);
  if(hit>0){const white=a*Math.min(1,hit*9);if(v.spec.legacy)fmcWhiteBlit(part,v.x,v.y,v.w,v.h,v.rot,white);
   else fmcCell(sheet,part,v.x,v.y,v.w,v.h,v.rot,white,'#ffffff');}
  if(v.p.kick>0&&v.spec.emit){const m=fmcPoint(v,...v.spec.emit);s81003Cell('impact',Math.min(3,Math.floor((.13-v.p.kick)*28)),m.x,m.y,29,29,a*.85);}
  if(v.p.id==='sword'&&charge){const q=fmcPoint(v,.5,.64);fmcCell('sword_fx',String(charge.frame),q.x,q.y,v.w*1.9,v.h*.94,v.rot,a*charge.alpha);}
 }
 s81003ShieldDraw(b);
};
r30ShieldBounds=function(b){
 if(!fmcLive(b))return FMC_BASE.shield.apply(this,arguments);
 const Q=r30Pose(b),D=f1003bDef(b);return{x:Q.x,y:Q.y+7,w:(D.id==='knight'?285:D.w+20)*(Q.scale||1),h:(D.id==='knight'?300:D.h+20)*(Q.scale||1)};
};
/* One authored housing, eight successive overlays during the entrance. Combat
   always shows ONLY the active form's actual HP and its matching color. */
function fmcGauge(b){
 const S=b._r30,t=S.t-.30;
 if(S.mode==='takeover'&&t<4){const n=clamp(Math.floor(Math.max(0,t)/.5),0,7);return{charge:n,color:F1003B_FORMS[n].color,under:n?F1003B_FORMS[n-1].color:null,frac:clamp((t-n*.5)/.40,0,1)};}
 return{charge:-1,color:f1003bDef(b).color,under:null,frac:clamp(b.hp/b.maxhp,0,1)};
}
drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld,lagKey){
 const b=boss;if(kind!=='boss'||!fmcLive(b))return FMC_BASE.bar.apply(this,arguments);
 if(!XART.rdy('bmbar_frame_boss')||!XART.rdy('bmbar_fill_solid'))return false;
 const G=fmcGauge(b),s=w/BMBAR.frameW,h=BMBAR.frameH*s,x=Math.round(cx-w/2),y=Math.round(cy-h/2),O=BMBAR.boss;
 const fx=x+O.dx*s,fy=y+O.dy*s,fw=O.w*s,fh=O.h*s;
 ctx.save();if(inWorld)ctx.translate(camX,0);ctx.imageSmoothingEnabled=true;
 ctx.drawImage(XART.get('bmbar_frame_boss'),x,y,w,h);drawBossTab('boss',cx,y,w);
 function fill(color,f){const im=xartPalette('bmbar_fill_solid',color);if(!im||f<=0)return;ctx.save();ctx.beginPath();ctx.rect(fx,fy,fw*f,fh);ctx.clip();ctx.drawImage(im,fx,fy,fw,fh);ctx.restore();}
 if(G.under)fill(G.under,1);fill(G.color,G.frac);
 ctx.restore();if(b._r30.shield>0)drawShieldBarArt(b._r30.shield/b._r30.shieldMax,cx+(inWorld?camX:0),cy+h/2+20,w,b);
 return true;
};
