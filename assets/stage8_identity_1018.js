"use strict";
/* Stage 8 identities: native Hammer/Furnace controllers own their combat.
   Dracodia's anatomy emits symbiote attacks, never missiles or gun lasers.
   The original finale still owns the portal, reunion and single reward. */
const V19={base:{enter:v18Enter,tick:r30Tick,draw:r30DrawBoss,body:v18Body,rig:v18Rig,at:r30At,frame:v18Frame,
 hit:modularHit,targets:retinaBossTargets,clear:v18Clear,attack:v18StartAttack,attackTick:v18AttackTick,
 rupture:v18Rupture,break:r30Break,fade:v18Fade,keys:v18Keys,warm:v18Warm,portrait:dr5Portrait,shot:v18Shot,warnings:v18Warnings,
 final:j3FinalDeath,death:dr5DeathTick,disintegrate:dr5Disintegrate,muzzle:furnaceMuzzle,
 mount:furnaceMount,head:furnaceHead,headCombat:furnaceHeadCombat,cannon:furnaceCannon,flame:fztBeam,gd4:gd4Tick,fmc:fmcRig,contact:target17BossContact},
 events:[],draws:{},portraitCache:new Map(),last:null};
function v19Log(b,event,data={}){V19.events.push({event,t:b._r30.clock,form:b._r30.v18.form,...data});if(V19.events.length>700)V19.events.shift();}
function v19Native(b){return v18Owned(b)&&j3State(b).encounter===2&&[8,2,6].includes(b._r30.v18.form);}
function v19Proxy(p){return p?._gp4Host&&v19Native(p._gp4Host);}
function v19Art(){return [...Object.values(V19_ART.volcano),...Object.values(V19_ART.hammer).flat(),...Object.values(V19_ART.clips).flatMap(c=>c.frames.flatMap(a=>[a,...Object.values(a.layers||{})])),...HK5_ART.hammer,...Object.values(FMC_ART)];}
function v19ArtKeys(){return v19Art().map(a=>a.key);}
for(const a of v19Art())XART._src[a.key]=a.path;
v18Keys=function(){return [...V19.base.keys(),...v19ArtKeys()];};
v18Warm=function(){let ready=V19.base.warm();for(const k of v19ArtKeys())if(!XART.rdy(k))ready=false;return ready;};
function v19Part(id,hp,spec={}){return{id,hp,maxhp:hp,destroyed:false,flash:0,kick:0,dmg:true,spec,_v19:true};}
v18Enter=function(b,n,form=0){const saved=n===2&&form===2?j3State(b).modules[form]?.filter(p=>p._v19).map(p=>({id:p.id,hp:p.hp,maxhp:p.maxhp})):null;
 V19.base.enter.apply(this,arguments);const J=j3State(b),N=b._r30.v18;N.swipe=null;N.acting=null;if(n!==2)return;
 N.donorAge=0;N.nextClawAt=7;
 if([8,2,6].includes(form)){
  if(!b.parts.every(p=>p._v19)){
   if(form===8)b.parts=[v19Part('core',b.hp,{role:'core'}),v19Part('hammer',Math.ceil(b.maxhp*.25),{role:'hammerHead'})];
   if(form===6)b.parts=FMC_RIGS.harrier.map(s=>v19Part(s.id,Math.ceil(b.maxhp*(s.id==='core'?1:s.hp)),s));
   if(form===2){const arm=Math.round(b.maxhp*FZT_SHARE.left),body=Math.round(b.maxhp*FZT_SHARE.body),hp={core:body,left:arm,right:arm,head:b.maxhp-body-arm*2};b.parts=['core','head','left','right'].map(id=>v19Part(id,hp[id],{role:id==='core'?'core':id==='head'?'head':'weapon'}));}
   J.modules[form]=b.parts;
  }
  if(saved)for(const q of saved){const p=b.parts.find(p=>p.id===q.id);if(p)Object.assign(p,q);}
  const D=gd4Create(b,form),p=D.p;p.dead=false;p.x=b.x;p.y=b.y;p.hp=b.hp;p.maxhp=b.maxhp;p.enter=false;p._noHit=false;D.age=0;D.alien=999;
  if(form===8){const h=p._hammer;h.balance0922=true;h.phasePending=false;const A=fr27Armor(p);if(A&&!A._v19){A.max=Math.ceil(b.maxhp*.25);A.hp=Math.min(A.hp,A.max);A._v19=true;}
   if(!D._v19){h.mode='hammer';hammerTarget(p);hammerState(p,'warn');}D._v19=true;
  }
  if(form===2){p._v19Volcano=true;const F=p._fz;F.hpSync=true;
   for(const part of b.parts){const id=part.id==='core'?'body':part.id;F.pools[id]=part.hp;F.max[id]=part.maxhp;}
   if(!D._v19){furnaceEnter(p,'arms');F.trans=0;D._v19=true;}F._v19=true;
  }
  b._r30.modular1003c=form!==2;b._r30.finale1003b=form!==2;
 }
 v19Log(b,'native-identity',{form,modules:b.parts.map(p=>p.id)});
};
function v19HammerRig(b){const p=gd4Create(b,8).p,h=p._hammer,C=h.hc11Counter;
 if(C){const f=hc11Frame(C),a=V19_ART.hammer[C.bank][f],k=HM10.bodyScale*C.scale,rot=C.angle||0;
  const make=(id,point,w,hgt,hidden=false)=>{const x=(point[0]-a.pivot[0])*k,y=(point[1]-a.pivot[1])*k,c=Math.cos(rot),s=Math.sin(rot);return{p:b.parts.find(p=>p.id===id),key:a.key,a,ax:C.x,ay:C.y,x:C.x+x*c-y*s,y:C.y+x*s+y*c,w,h:hgt,rot,alpha:1,k,spec:{px:a.pivot[0]/a.w,py:a.pivot[1]/a.h,role:id==='core'?'core':'hammerHead',hidden},z:hidden?5:1};};
  return[make('core',[a.w/2,a.h/2],a.w*k,a.h*k),make('hammer',a.tip,56,56,true)].filter(v=>!v.p.destroyed);
 }
 const rig=V19.base.fmc(b),depth=h.state.startsWith('giant_')?hammerDepthScale(p):1;
 return rig.map(v=>({...v,x:b.x+(v.x-b.x)*depth,y:b.y+(v.y-b.y)*depth,ax:b.x+(v.ax-b.x)*depth,ay:b.y+(v.ay-b.y)*depth,w:v.w*depth,h:v.h*depth}));
}
function v19VolcanoRig(b){const p=gd4Create(b,2).p,F=p._fz,k=v18Size(b)/320,phase=F.phase,out=[];
 for(const id of ['core','legL','legR','head','left','right']){
  const owner=b.parts.find(p=>p.id===(id.startsWith('leg')?'core':id));if(!owner||owner.destroyed&&id!=='head')continue;
  if(phase==='head'&&id!=='head'||phase!=='arms'&&['left','right'].includes(id))continue;
  const a=V19_ART.volcano[id],anchor=V19_ART.volcanoMounts[id],tip=V19_ART.volcanoMuzzles[id],base=tip?Math.atan2(anchor[0]-tip[0],tip[1]-anchor[1]):0;let rot=F.a+(F.arm[id]?.a||0)-base,ax=b.x,ay=b.y;
  if(phase==='head'){rot=F._v19Head?.roll||0;ax=b.x;ay=b.y;}
  else{const x=(anchor[0]-160)*k,y=(anchor[1]-160)*k,c=Math.cos(F.a),s=Math.sin(F.a);ax+=x*c-y*s;ay+=x*s+y*c;}
  rot=v19SwipeRotation(b,id,rot);
  const q=a.bounds,cx=(q[0]+q[2])/2,cy=(q[1]+q[3])/2,dx=(cx-anchor[0])*k,dy=(cy-anchor[1])*k,c=Math.cos(rot),s=Math.sin(rot);
  out.push({p:owner,key:a.key,a,ax,ay,x:ax+dx*c-dy*s,y:ay+dx*s+dy*c,w:(q[2]-q[0])*k,h:(q[3]-q[1])*k,rot,alpha:1,k,anchor,layer:id,spec:{px:anchor[0]/320,py:anchor[1]/320,role:owner.spec.role},z:id==='head'?4:1});
 }return out;
}
fmcRig=function(b){if(v19Native(b)){const f=b._r30.v18.form;if(f===8)return v19HammerRig(b);if(f===2)return v19VolcanoRig(b);}return V19.base.fmc.apply(this,arguments);};
function v19Acting(b){const N=b._r30.v18,P=N.attack,R=dr5State(b).radio,roar=b._r30.mode==='dr5Monologue'&&R?.face===5;
 if(j3State(b).encounter!==2||N.form!==0)return null;const name=roar?'colossus_roar':N.acting;if(!name)return null;
 return v19ClipFrame(name,roar?R.t:P?.t||0,roar?2.5:(P?.tell||0)+(P?.active||2.2));
}
v18Frame=function(b){return b._r30.v18.swipe?V18_ART.models[v18Model(b)].frames[0]:v19Acting(b)?.layers||V19.base.frame(b);};
const V19_LIMBS={infused:{left:[[91,118],[80,238]],right:[[231,118],[244,238]]},
 ghost:{left:[[125,151],[105,248]],right:[[201,145],[229,245]]},
 colossus:{left:[[108,119],[76,251]],right:[[212,119],[243,251]]}};
v18Rig=function(b){if(v19Native(b))return fmcRig(b);const rig=V19.base.rig.apply(this,arguments),P=b._r30.v18.attack;
 return rig.map(v=>{const a=v.a,k=v.k;let anchor=[160,160],ax=b.x,ay=b.y,rot=0;
  const joint=V19_LIMBS[v18Model(b)]?.[v.p.id];
  if(joint&&!v19Acting(b)){
   anchor=joint[0];ax=b.x+(anchor[0]-160)*k;ay=b.y+(anchor[1]-160)*k;rot=v19SwipeRotation(b,v.p.id,0);
  }
  const dx=((a.bounds[0]+a.bounds[2])/2-anchor[0])*k,dy=((a.bounds[1]+a.bounds[3])/2-anchor[1])*k,c=Math.cos(rot),s=Math.sin(rot);
  return{...v,anchor,ax,ay,x:ax+dx*c-dy*s,y:ay+dx*s+dy*c,rot};});
};
r30Parts=function(b){return v18Owned(b)?v18Rig(b):V18.base.parts.apply(this,arguments);};
function v19WorldPoint(v,point){const dx=(point[0]-v.anchor[0])*v.k,dy=(point[1]-v.anchor[1])*v.k,c=Math.cos(v.rot),s=Math.sin(v.rot);return{x:v.ax+dx*c-dy*s,y:v.ay+dx*s+dy*c};}
// A planted shoulder, a committed arc, then a harmless recovery. The same rig
// drives drawing, alpha hits, module locks, the curved tell and swept contact.
function v19Ease(t){t=clamp(t,0,1);return t*t*(3-2*t);}
function v19SwipeAngle(Q,t=Q.t){
 if(t<Q.tell)return lerp(Q.rest,Q.start,v19Ease(t/Q.tell));
 if(t<Q.tell+Q.swing)return lerp(Q.start,Q.end,v19Ease((t-Q.tell)/Q.swing));
 return lerp(Q.end,Q.rest,v19Ease((t-Q.tell-Q.swing)/Q.recover));
}
function v19SwipeRotation(b,id,rest){const W=b._r30.v18.swipe,Q=W?.q;return Q&&Q.id===id?v19SwipeAngle(Q):rest;}
function v19SwipePrepare(b){const N=b._r30.v18,W=N.swipe,id=W.sides[W.index],v=v18Rig(b).find(v=>v.p.id===id);
 if(!v||v.p.destroyed){W.index++;return W.index<W.sides.length?v19SwipePrepare(b):false;}
 const donor=v19Native(b),tip=donor?V19_ART.volcanoMuzzles[id]:V19_LIMBS[v18Model(b)][id][1],side=id==='left'?-1:1,
  r=Math.hypot(tip[0]-v.anchor[0],tip[1]-v.anchor[1])*v.k,off={x:v.ax-b.x,y:v.ay-b.y},
  target={x:clamp(player.x,camLeftX()+18,camRightX()-18),y:clamp(player.y,viewTopY()+130,VH-25)},
  station={x:clamp(target.x-side*r*.55-off.x,camLeftX()+135,camRightX()-135),y:0};
 const dx=target.x-station.x-off.x;station.y=clamp(target.y-Math.sqrt(Math.max(r*r-dx*dx,r*r*.18))-off.y,viewTopY()+150,VH-145);
 const root={x:station.x+off.x,y:station.y+off.y},base=Math.atan2(tip[1]-v.anchor[1],tip[0]-v.anchor[0]),rest=v.rot,
  aim=rest+fztWrap(Math.atan2(target.y-root.y,target.x-root.x)-base-rest),d=Math.min(2,v18Diff()),first=W.index===0,
  tell=first?[1.28,1.08,.90][d]:[.86,.74,.62][d];
 const Q=W.q={id,t:0,tell,swing:[.62,.52,.43][d],recover:.32,rest,start:aim-side*1.16,end:aim+side*1.16,
  target,station,root,from:{x:b.x,y:b.y},off,tip,base,k:v.k,a:v.a,anchor:v.anchor,hit:new Set(),released:false};
 // Measure the distal blade/forearm alpha, not the empty source rectangle.
 const m=v18Mask(v.a),bounds=v.a.bounds;Q.cut=v.anchor[1]+(bounds[3]-v.anchor[1])*.48;let lo=Infinity,hi=0,spread=0;
 if(m)for(let y=Math.ceil(Q.cut);y<bounds[3];y+=2)for(let x=bounds[0];x<bounds[2];x+=2)if(m[y*320+x]>48){
  const dx=x-v.anchor[0],dy=y-v.anchor[1],r=Math.hypot(dx,dy)*v.k;lo=Math.min(lo,r);hi=Math.max(hi,r);spread=Math.max(spread,Math.abs(fztWrap(Math.atan2(dy,dx)-base)));}
 Q.inner=Number.isFinite(lo)?Math.max(0,lo-8):r*.55;Q.outer=Math.max(hi+8,r);Q.spread=spread;
 combatWarningTick(b,'v19-swipe-'+W.serial+'-'+W.index,0,tell);r30Sound('shadowCharge');
 v19Log(b,'swipe-tell',{side:id,type:W.type,tell,swing:Q.swing,arc:Math.abs(Q.end-Q.start),target:{...target}});return true;
}
function v19BeginSwipe(b,type,first){const N=b._r30.v18,donor=v19Native(b);if(N.swipe)return false;
 const live=['left','right'].filter(id=>b.parts.some(p=>p.id===id&&!p.destroyed));if(!live.length)return false;
 N.acting=null;const serial=N.swipeSerial=(N.swipeSerial||0)+1,lead=first||live[(serial-1)%live.length],other=lead==='left'?'right':'left',
  sides=[lead,other].filter(id=>live.includes(id));if(diffKey==='furious'&&sides.length===2)sides.push(lead);
 N.attack={type,swipe:true,t:0,tell:0,active:0,ports:[],targets:[],lanes:[]};b._r30.attack=N.attack;
 N.swipe={serial,type,sides,index:0,q:null,home:{...N.home},donor};v19SwipePrepare(b);N.attack.tell=N.swipe.q.tell;return true;
}
function v19SwipeContact(v,Q,x,y){const c=Math.cos(-v.rot),s=Math.sin(-v.rot),dx=x-v.ax,dy=y-v.ay,
 px=Math.floor((dx*c-dy*s)/v.k+v.anchor[0]),py=Math.floor((dx*s+dy*c)/v.k+v.anchor[1]),m=v18Mask(v.a);
 return py>=Q.cut&&px>=0&&py>=0&&px<320&&py<320&&m?.[py*320+px]>48;
}
function v19SwipeTick(b,dt){const N=b._r30.v18,W=N.swipe,Q=W?.q;if(!W)return;
 if(W.returning){W.returning.t+=dt;const u=v19Ease(W.returning.t/.58);b.x=lerp(W.returning.x,W.home.x,u);b.y=lerp(W.returning.y,W.home.y,u);
  if(u>=1){N.swipe=null;N.attack=null;N.acting=null;b._r30.attack=null;b._r30.cd=diffKey==='furious'?.55:diffKey==='hard'?.8:1.05;j3State(b).attacks++;
   if(W.donor)N.nextClawAt=N.donorAge+8.5;v19Log(b,'swipe-complete',{type:W.type,sides:W.sides});}return;}
 const before=Q.t;Q.t+=dt;N.attack.t+=dt;
 const approach=v19Ease(Q.t/(Q.tell*.78));b.x=lerp(Q.from.x,Q.station.x,approach);b.y=lerp(Q.from.y,Q.station.y,approach);
 combatWarningTick(b,'v19-swipe-'+W.serial+'-'+W.index,Math.min(Q.t,Q.tell),Q.tell);
 const part=b.parts.find(p=>p.id===Q.id),live=part&&!part.destroyed;
 if(live&&Q.t>=Q.tell&&!Q.released){Q.released=true;r30Sound('slice');shake=Math.max(shake,3);v19Log(b,'swipe-release',{side:Q.id,target:{...Q.target},arc:Math.abs(Q.end-Q.start),reaction:Q.tell});
  if(W.index===0)v19Log(b,'organic-release',{type:W.type,reaction:Q.tell});}
 const a=Math.max(before,Q.tell),z=Math.min(Q.t,Q.tell+Q.swing);
 if(live&&z>a){const v=v18Rig(b).find(v=>v.p===part),r=Q.outer,n=Math.max(1,Math.ceil(Math.abs(v19SwipeAngle(Q,z)-v19SwipeAngle(Q,a))*r/5));
  if(v)for(const seat of seatList())withSeat(seat,()=>{if(player.dead||Q.hit.has(seat))return;
   for(let i=0;i<=n;i++){const pose={...v,rot:v19SwipeAngle(Q,lerp(a,z,i/n))};
    if([-5,0,5].some(dx=>[-5,0,5].some(dy=>v19SwipeContact(pose,Q,player.x+dx,player.y+dy)))){
     Q.hit.add(seat);playerHit('symbiote '+Q.id+' swipe');v19Log(b,'swipe-contact',{side:Q.id,seat});break;}}
  });
 }
 if(!live||Q.t>=Q.tell+Q.swing+Q.recover){W.index++;W.q=null;if(W.index<W.sides.length&&v19SwipePrepare(b))return;
  if(W.donor){const p=gd4Create(b,2).p,F=p._fz;if(F.phase==='arms'&&F.trans<=0){furnaceNext(p);
   W.home.y=fztPy(F.attack==='spin900'?260:F.attack==='sweep'?255:240);F.startX=W.home.x;}}
  W.returning={x:b.x,y:b.y,t:0};}
}
function v19SwipeWarning(b){const W=b._r30.v18.swipe,Q=W?.q;if(!Q||Q.t>=Q.tell||!b.parts.some(p=>p.id===Q.id&&!p.destroyed))return;
 const u=Q.t/Q.tell,reverse=Q.end<Q.start,
  a=Q.start+Q.base+(reverse?Q.spread:-Q.spread),z=Q.end+Q.base+(reverse?-Q.spread:Q.spread),key='bmfx_fov_'+l23FovPhase(u)+'_tall';
 // Bend the authored FOV's interior into one continuous curved field. Many
 // tiny cones make a misleading starburst because the native cone has a
 // minimum width/length. Its real scanlines/colors are retained here.
 if(XART.rdy(key)){ctx.save();ctx.beginPath();ctx.arc(Q.root.x,Q.root.y,Q.outer,a,z,reverse);ctx.arc(Q.root.x,Q.root.y,Q.inner,z,a,!reverse);ctx.closePath();ctx.clip();
  ctx.globalAlpha*=.28+u*.20;ctx.drawImage(XART.get(key),132,220,56,20,Q.root.x-Q.outer,Q.root.y-Q.outer,Q.outer*2,Q.outer*2);ctx.restore();}
 combatWarningDraw(b,{x:Q.root.x,y:Q.root.y,progress:u,alertOnly:true,alertX:Q.root.x,alertY:Q.root.y-45});
 groundTargetReticleDraw(Q.target.x,Q.target.y,58,u,.8);
}
target17BossContact=function(b,x,y){return v18Owned(b)&&b._r30.v18.swipe?false:V19.base.contact.apply(this,arguments);};
furnaceMount=function(p,side){if(!p?._v19Volcano)return V19.base.mount.apply(this,arguments);const v=v19VolcanoRig(p._gp4Host).find(v=>v.layer===side);return v?{x:v.ax,y:v.ay,a:p._fz.a+p._fz.arm[side].a}:{x:p.x,y:p.y,a:0};};
furnaceMuzzle=function(p,side){if(!p?._v19Volcano)return V19.base.muzzle.apply(this,arguments);const v=v19VolcanoRig(p._gp4Host).find(v=>v.layer===side);return v?{...v19WorldPoint(v,V19_ART.volcanoMuzzles[side]),a:p._fz.a+p._fz.arm[side].a}:{x:p.x,y:p.y,a:0};};
fztBeam=function(F,x,y,a,len,width,kind){if(!F?._v19||kind!=='flame')return V19.base.flame.apply(this,arguments);
 const n=F.beams.length,out=FURNACE17.base.rawBeam.apply(this,arguments);for(const q of F.beams.slice(n)){q._v19Flame=true;q.clock=F.t;}return out;
};
furnaceCannon=function(p){if(!p?._v19Volcano)return V19.base.cannon.apply(this,arguments);const F=p._fz,beat=F.shotBeat,n=eBullets.length,out=FURNACE17.base.cannon.apply(this,arguments);
 if(F.shotBeat!==beat){F._v19Cannon=(F._v19Cannon||0)+1;const q=eBullets.slice(n).find(q=>q.kind==='fztFireball');if(q&&F._v19Cannon%2===0){const a=q.ang-Math.PI/2,speed=diffKey==='furious'?3.65:diffKey==='hard'?3.3:2.85;
  Object.assign(q,{vx:-Math.sin(a)*speed,vy:Math.cos(a)*speed,w:112,h:34,ang:a,kind:'pt11FireWave',_pt11Wave:true,_pt11Scale:.64,_weaponProof:true,_shootable:false});fztSfx('furnaceFlameRelease');}
 }return out;
};
furnaceHead=function(p){if(!p?._v19Volcano)return V19.base.head.apply(this,arguments);const v=v19VolcanoRig(p._gp4Host).find(v=>v.layer==='head');return v?{x:v.ax,y:v.ay}:{x:p.x,y:p.y};};
function v19AtRect(v,x,y){const c=Math.cos(-v.rot),s=Math.sin(-v.rot),dx=x-v.ax,dy=y-v.ay;
 if(v.anchor){const px=Math.floor((dx*c-dy*s)/v.k+v.anchor[0]),py=Math.floor((dx*s+dy*c)/v.k+v.anchor[1]),m=v18Mask(v.a),w=v.a?.w||320,h=v.a?.h||320;return m&&px>=0&&py>=0&&px<w&&py<h&&m[py*w+px]>48;}
 return Math.abs(x-v.x)<v.w*.5&&Math.abs(y-v.y)<v.h*.5;
}
r30At=function(b,x,y){if(!v18Owned(b))return V18.base.at.apply(this,arguments);if(!r30Live(b)||b._noHit)return null;
 const rig=v18Rig(b).slice().reverse();for(const v of rig)if(!v.p.destroyed&&v19AtRect(v,x,y))return v.p;return null;};
retinaBossTargets=function(b){if(!v19Native(b))return V19.base.targets.apply(this,arguments);if(!r30Live(b)||b._noHit)return[];
 const stamp=b._r30.v18.form,parts=[...new Set(v18Rig(b).map(v=>v.p))],F=stamp===2?gd4Create(b,2).p._fz:null;
 return parts.filter(p=>!F||furnaceVulnerable(gd4Create(b,2).p).includes(p.id==='core'?'body':p.id)).map(p=>retinaDynamicPiece(b,'v19-'+stamp+'-'+p.id,'symbiote '+p.id,()=>{
  const v=v18Rig(b).find(v=>v.p===p);return{x:v?.x||b.x,y:v?.y||b.y,hp:p.hp,dead:stamp!==b._r30.v18.form||!r30Live(b)||b._noHit||p.destroyed||!v};
 },d=>{b._lastPart=p;hitBoss(d);},52,56));
};
function v19NativeTick(b,dt){const N=b._r30.v18,D=gd4Create(b,N.form),p=D.p,prior=D.last,before=b.hp;
 N.donorAge+=dt;p.hp=b.hp;p.maxhp=b.maxhp;p.dead=false;p.flash=Math.max(b.flash||0,p.flash-dt||0);p.t+=dt;p.enter=false;
 if(N.form===8){hammerBossTick(p,dt);b.x=p.x;b.y=p.y;b.hp=Math.min(before,p.hp);p.hp=b.hp;
  const h=p._hammer,tool=b.parts.find(p=>p.id==='hammer');tool.hp=h.hammerHP;tool.maxhp=h.hammerMax;tool.destroyed=!!h.hammerDestroyed;b._noHit=!!p._noHit;
 }else if(N.form===2){const F=p._fz;
  if(N.swipe){F.tells=[];F.beams=[];v19SwipeTick(b,dt);p.x=b.x;p.y=b.y;b._noHit=false;}
  else{furnaceTick(p,dt);b.x=p.x;b.y=p.y;b._noHit=F.trans>0;
   if(F.phase==='arms'&&F.trans<=0&&F.at<.1&&N.donorAge>=N.nextClawAt)v19BeginSwipe(b,'volcanoRake');}
  const rig=v19VolcanoRig(b),left=Math.min(...rig.map(v=>v.x-(Math.abs(Math.cos(v.rot))*v.w+Math.abs(Math.sin(v.rot))*v.h)/2)),right=Math.max(...rig.map(v=>v.x+(Math.abs(Math.cos(v.rot))*v.w+Math.abs(Math.sin(v.rot))*v.h)/2));
  const dx=N.swipe?0:right-left>viewW()-16?(camLeftX()+camRightX()-left-right)/2:left<camLeftX()+8?camLeftX()+8-left:right>camRightX()-8?camRightX()-8-right:0;b.x+=dx;p.x=b.x;
 }
 else{D.age=0;D.alien=999;V19.base.gd4(b,dt);D.age=0;}
 const mode=N.form===8?p._hammer.state:N.form===2?p._fz.phase+':'+p._fz.attack:p._whv.can.last||p._whv.ace.st;
 if(mode!==prior){D.last=mode;D.history.push(mode);v19Log(b,'donor-state',{state:mode});}
 if(N.donorAge>=(diffKey==='furious'?46:42)&&V18.forms.filter(i=>j3State(b).hp[i]>0).length>1){
  const committed=N.form===8&&(hammerStrikeCommitted(p)||p._hammer.recovery?.status==='charging'),safe=N.form!==2||p._fz.at<.1;
  if(!committed&&safe&&!N.swipe){j3Save(b);j3Morph(b,'home');return;}
 }
 b._drawY=b.y;j3Save(b);
}
modularHit=function(dmg){const b=boss;if(!v19Native(b))return V19.base.hit.apply(this,arguments);if(!r30Live(b)||b._noHit||!(dmg>0))return;
 const N=b._r30.v18,D=gd4Create(b,N.form),p=D.p,part=b.parts.includes(b._lastPart)&&!b._lastPart.destroyed?b._lastPart:b.parts[0];
 part.flash=.12;markHit(b,.12);markHit(p,.12);
 if(N.form===8){p.hp=b.hp;p.maxhp=b.maxhp;p._hammerModuleHit=part.id==='hammer'?'hammer':null;const d=hammerBossDamage(p,dmg);b.hp=Math.max(0,p.hp-d);p.hp=b.hp;stageStats.dmgDealt+=d;
  const tool=b.parts.find(q=>q.id==='hammer');tool.hp=p._hammer.hammerHP;tool.destroyed=!!p._hammer.hammerDestroyed;
 }else if(N.form===2){const F=p._fz,id=part.id==='core'?'body':part.id;if(!furnaceVulnerable(p).includes(id))return;
  const d=Math.min(dmg,F.pools[id]);F.pools[id]-=d;part.hp=F.pools[id];F.flash[id]=.12;stageStats.dmgDealt+=d;
  if(part.hp<=0){v19Rupture(b,part);part.destroyed=true;furnaceBreak(p,id);v19Log(b,'furnace-module-break',{module:id,next:F.phase});}
  b.hp=Math.max(0,Math.min(b.hp-d,Object.values(F.pools).reduce((s,h)=>s+Math.max(0,h),0)));p.hp=b.hp;
 }else{const d=Math.min(dmg,b.hp);b.hp-=d;stageStats.dmgDealt+=d;if(part.id!=='core'){part.hp=Math.max(0,part.hp-dmg);if(!part.hp){v19Rupture(b,part);part.destroyed=true;}}
 }
 j3Save(b);if(b.hp<=0)r30Break(b);
};
furnaceHeadCombat=function(p,dt){if(!p?._v19Volcano)return V19.base.headCombat.apply(this,arguments);
 const b=p._gp4Host,F=p._fz,C=f17Tune(),Q=F._v19Head??={serial:-1};
 if(Q.serial!==F.serial)Object.assign(Q,{serial:F.serial,roll:0,dir:F.dir||1,released:false,sound:false});
 const t=F.at,u=clamp((t-C.warm)/C.active,0,1);Q.roll=Q.dir*TAU*u;Q.phase=t<C.warm?'charge':t<C.warm+C.active?'spin':'recover';
 Q.charge=Q.phase==='charge'?clamp(t/C.warm,0,1):Q.phase==='spin'?1:0;F.a=0;F.charge=Q.charge;
 const k=v18Size(b)/320,len=Math.hypot(worldWidth(),viewH())+180,eye=[[-12,10],[12,10]];
 for(let i=0;i<2;i++){const [x,y]=eye[i],c=Math.cos(Q.roll),s=Math.sin(Q.roll),sx=p.x+(x*c-y*s)*k,sy=p.y+(x*s+y*c)*k,a=Q.roll+(i?1:-1)*.14;
  if(Q.phase==='charge'){const e=fztPt(sx,sy,a,len);F.tells.push({x:sx,y:sy,ex:e.x,ey:e.y,progress:Q.charge,width:10,kind:'line'});}
  if(Q.phase==='spin')FURNACE17.base.rawBeam(F,sx,sy,a,len/FZT_S,C.width,'eye');
 }
 if(Q.phase==='charge'){combatWarningTick(p,'v19-volcano-eyes-'+F.serial,t,C.warm);shake=Math.max(shake,.5+Q.charge*3);if(!Q.sound){Q.sound=true;fztSfx('furnaceLaserCharge');}}
 if(Q.phase==='spin'&&!Q.released){Q.released=true;fztSfx('furnaceLaserBurst');v19Log(b,'volcano-eye-release',{seconds:C.active,radians:TAU});}
 if(t>=C.warm+C.active+C.recover){v19Log(b,'volcano-full-head-turn',{radians:Q.roll});furnaceNext(p);}
};
function v19Rupture(b,p){if(!v19Native(b))return V19.base.rupture(b,p);const rig=v18Rig(b).filter(v=>v.p===p&&!v.spec.hidden);if(!rig.length)return;
 for(const v of rig){let im;if(v.a){const a=v.a,q=a.bounds,c=document.createElement('canvas');c.width=q[2]-q[0]+(q[2]-q[0])%2;c.height=q[3]-q[1]+(q[3]-q[1])%2;c.getContext('2d').drawImage(XART.get(a.key),q[0],q[1],q[2]-q[0],q[3]-q[1],0,0,q[2]-q[0],q[3]-q[1]);im=c;}
 else{const a=FMC_ART[v.key]||FMC_ART[v.key.replace(/^fmc_/,'')],r=a?.rects[v.spec.art];if(a&&r){const c=document.createElement('canvas');c.width=r[2]+r[2]%2;c.height=r[3]+r[3]%2;c.getContext('2d').drawImage(XART.get(a.key),...r,0,0,r[2],r[3]);im=c;}}
 const pieces=p._v19Ruptures??={},key=v.layer||p.id;d27ModuleRupture(b,pieces[key]??={id:p.id+'-'+key},{...v,debrisImage:im},'purple');}
 v19Log(b,'module-rupture',{module:p.id});
}
v18Rupture=v19Rupture;
function v19ClipFrame(name,t,duration){const c=V19_ART.clips[name];return c?.frames[Math.min(c.frames.length-1,Math.floor(clamp(t/duration,0,.999999)*c.frames.length))];}
function v19Clip(name,t,duration,b,size=v18Size(b)){const a=v19ClipFrame(name,t,duration);if(a){v18Cell(a,b.x,b.y,size);V19.draws[name]=(V19.draws[name]||0)+1;return true;}return false;}
function v19Paint(v,b){if(v.spec.hidden)return;ctx.save();ctx.imageSmoothingEnabled=false;
 if(v.anchor){ctx.translate(v.ax,v.ay);ctx.rotate(v.rot);ctx.drawImage(XART.get(v.key),-v.anchor[0]*v.k,-v.anchor[1]*v.k,(v.a?.w||320)*v.k,(v.a?.h||320)*v.k);
  const flash=Math.max(v.p.flash||0,b.flash||0);if(flash>0){ctx.globalAlpha=clamp(flash/.12,0,1)*.8;ctx.drawImage(xartTint(v.key,'#ffffff',1),-v.anchor[0]*v.k,-v.anchor[1]*v.k,(v.a?.w||320)*v.k,(v.a?.h||320)*v.k);}
 }else if(v.a){ctx.translate(v.ax,v.ay);ctx.rotate(v.rot);ctx.drawImage(XART.get(v.key),-v.a.pivot[0]*v.k,-v.a.pivot[1]*v.k,v.a.w*v.k,v.a.h*v.k);
  if(Math.max(v.p.flash||0,b.flash||0)>0){ctx.globalAlpha=.8;ctx.drawImage(xartTint(v.key,'#ffffff',1),-v.a.pivot[0]*v.k,-v.a.pivot[1]*v.k,v.a.w*v.k,v.a.h*v.k);}
 }else{const sheet=FMC_ART[v.key]?v.key:v.spec.sheet||v.key.replace(/^fmc_/,'');FF8_BASE.cell(sheet,v.spec.art||'pose',v.x,v.y,v.w,v.h,v.rot,1);const flash=Math.max(v.p.flash||0,b.flash||0);if(flash>0)FF8_BASE.cell(sheet,v.spec.art||'pose',v.x,v.y,v.w,v.h,v.rot,Math.min(.8,flash*8),'#ffffff');}
 ctx.restore();V19.draws[v.key]=(V19.draws[v.key]||0)+1;}
function v19Body(b){const rig=v18Rig(b),Q=b._r30.v18.swipe?.q;
 if(Q&&Q.t>Q.tell&&Q.t<Q.tell+Q.swing){const v=rig.find(v=>v.p.id===Q.id);if(v)for(const ago of [.08,.04]){ctx.save();ctx.globalAlpha*=ago===.08?.09:.18;v19Paint({...v,rot:v19SwipeAngle(Q,Math.max(Q.tell,Q.t-ago))},b);ctx.restore();}}
 for(const v of rig)v19Paint(v,b);}
v18Body=v19Body;
function v19DonorDraw(b){const D=gd4Create(b,b._r30.v18.form),p=D.p,N=b._r30.v18;
 if(N.form===8){
  // This draw owns the existing native Hammer warning/effect paths; its
  // body is the two-arm symbiote bank, including the measured side swing.
  const h=p._hammer;if(h.hc11Counter){v19Body(b);hc11WarningDraw(h.hc11Counter);for(const q of h.stormWaves||[]){hammerStormRedZoneDraw(q);hammerStormRowRetinaDraw(q);hammerStormSpikeDraw(q);hammerStormRowAlertDraw(q);}}
  else V18.base.draw.call(null,b);
 }else if(N.form===2){v19SwipeWarning(b);v19Body(b);const F=p._fz;
  for(const q of F.tells)fztTellDraw(q,p);for(const q of F.beams){if(q.kind==='flame')av3Beam(ctx,q.x,q.y,q.a+Math.PI/2,q.len,q.width*2,'fire',F.t,1,true);else fztBeamDraw(q);}
  for(const side of ['left','right'])if(F.phase==='arms'&&F.pools[side]>0){const m=furnaceMuzzle(p,side);fztCharge(m.x,m.y,F.arm[side].charge,.65);}
  if(F.phase==='core')fztCharge(b.x,b.y,F.charge,.8);
  if(F.phase==='head'){const Q=F._v19Head;if(Q?.charge>0){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=Q.charge*.38;for(const v of v19VolcanoRig(b))v19Paint(v,b);ctx.restore();}}
  for(const e of F.fx){const u=1-e.life/e.max;fztSprite(e.key,e.x,e.y,(e.a||0)+u*(e.spin||0),e.s*(.7+u*.65),1-u);}
 }else{v19Body(b);whvDrawShots(p);}
}
// Actual form anatomy decides every attack source and its visual footprint.
function v19Organic(b){return v18Owned(b)&&!v19Native(b);}
v18Shot=function(b,p,a,speed,kind,large=false){if(!v19Organic(b))return V19.base.shot.apply(this,arguments);
 const gun=b._r30.v18.attack?.type==='podStrafe',q=gun?eShootT(p.x,p.y,a,speed,'mg',{w:5,h:12}):r30Shot(b,'matter',p.x,p.y,a,speed);
 if(q){q._v18Owner=b;q._v19Symbiote=!gun;q.w=q.h=gun?6:large?22:16;b._r30.v18.shots=(b._r30.v18.shots||0)+1;}return q;
};
v18StartAttack=function(b){if(!v19Organic(b))return V19.base.attack(b);const N=b._r30.v18,name=v18Model(b),books={
 infused:['talonLunge','opticSpores','talonPincer'],ghost:['voidWells','soulBurst','ghostRake'],
 colossus:['scytheReap','voidRoar','heartSpores'],helicopter:['podStrafe','bellyBombs','rotorSpores']};
 let type=books[name][N.seq++%3];const tell=diffKey==='furious'?.90:diffKey==='hard'?1.08:1.28;
 if(['talonLunge','talonPincer','ghostRake','scytheReap'].includes(type)){
  if(v19BeginSwipe(b,type)){v19Log(b,'organic-tell',{type,tell,origin:{x:b.x,y:b.y},targets:[]});return;}
  type=name==='infused'?'opticSpores':name==='ghost'?'soulBurst':'heartSpores';
 }
 const P=N.attack={type,t:0,tell,active:type==='voidRoar'?3.0:type==='scytheReap'?2.2:2.6,n:0,next:0,
  tx:clamp(player.x,camLeftX()+45,camRightX()-45),ty:clamp(player.y,viewTopY()+120,VH-45),origin:{x:b.x,y:b.y},ports:[],targets:[],lanes:[],hit:new Set()};
 const arms=v18Rig(b).filter(v=>v.p.id!=='core');P.ports=arms.map(v=>({x:v.x,y:v.y+v.h*.32,module:v.p.id}));
 if(['voidWells','bellyBombs'].includes(type))P.targets=[-1,0,1].map(i=>({x:clamp(P.tx+i*85,camLeftX()+40,camRightX()-40),y:clamp(P.ty-i%2*35,viewTopY()+145,VH-45)}));
 N.acting=type==='voidRoar'?'colossus_roar':null;b._r30.attack=P;
 combatWarningTick(b,'v19-'+N.seq,0,tell);r30Sound(type==='voidRoar'?'dracodiaShriek':'shadowCharge');v19Log(b,'organic-tell',{type,tell,origin:{x:b.x,y:b.y},targets:P.targets});
};
v18AttackTick=function(b,dt){if(!v19Organic(b))return V19.base.attackTick(b,dt);const S=b._r30,N=S.v18,P=N.attack;if(!P)return;if(N.swipe)return v19SwipeTick(b,dt);
 P.t+=dt;const u=P.t-P.tell,d=v18Diff();combatWarningTick(b,'v19-'+N.seq,Math.min(P.t,P.tell),P.tell);
 if(u<0)return;if(!P.started){P.started=true;r30Sound(['scytheReap','ghostRake'].includes(P.type)?'slice':'shadowRelease');v19Log(b,'organic-release',{type:P.type,reaction:P.tell});}
 if(u>=P.next){P.n++;P.next=u+(['podStrafe','rotorSpores'].includes(P.type)?[.24,.18,.13][Math.min(d,2)]:.75);
  const center={x:b.x,y:b.y+28,module:'core'},aim=p=>Math.atan2(P.ty-p.y,P.tx-p.x),ports=v18Ports(b);
  if(['opticSpores','soulBurst','heartSpores'].includes(P.type))for(let i=-2-d;i<=2+d;i++)v18Shot(b,center,aim(center)+i*.18,2.4+d*.22,'code',true);
  if(P.type==='voidRoar'){const gap=aim(center)+Math.PI;for(let i=0;i<14+d*2;i++){const a=i*TAU/(14+d*2)+P.n*.12;if(Math.abs(fztWrap(a-gap))>.45)v18Shot(b,center,a,2.3+d*.22,'code',true);}shake=Math.max(shake,6);}
  if(P.type==='podStrafe')for(const p of ports)for(const a of [-.07,.07])v18Shot(b,p,aim(p)+a,4.1+d*.30,'code');
  if(P.type==='rotorSpores')for(let i=0;i<8;i++)v18Shot(b,center,TAU*i/8+P.n*.28,2.6,'code');
  if(P.type==='voidWells'&&P.n===1)for(const T of P.targets)(N.hazards??=[]).push({...T,t:0,warm:.9,life:2.4});
  if(P.type==='bellyBombs'&&P.n===1)for(const T of P.targets)groundTargetingSpawn({kind:'missile',x:T.x,y:T.y,warn:.9,active:.5,radius:34,size:82,track:false,lane:false,owner:b,_v19:true});
 }
 if(u>=P.active){b.x=P.origin.x;b.y=P.origin.y;N.attack=null;N.acting=null;S.attack=null;S.cd=diffKey==='furious'?.55:diffKey==='hard'?.8:1.05;j3State(b).attacks++;}
};
v18Warnings=function(b){if(!v19Organic(b))return V19.base.warnings(b);if(b._r30.v18.swipe)return v19SwipeWarning(b);const P=b._r30.v18.attack;if(!P||P.t>=P.tell)return;const u=P.t/P.tell;
 if(P.lanes.length){for(const L of P.lanes)if(b.parts.some(p=>p.id===L.module&&!p.destroyed))s81003Fov(L,u,true);return;}
 if(P.targets.length){for(const T of P.targets)groundTargetReticleDraw(T.x,T.y,74,u,.9);return;}
 if(['voidRoar','rotorSpores'].includes(P.type)){groundTargetReticleDraw(b.x,b.y,155,u,.88);combatWarningDraw(b,{x:b.x,y:b.y,progress:u,alertOnly:true,alertX:b.x,alertY:b.y-135});return;}
 const ports=P.type==='podStrafe'?P.ports:[{x:b.x,y:b.y+28}];for(const p of ports)combatWarningDraw(b,{x:p.x,y:p.y,ex:P.tx,ey:P.ty,width:P.type==='podStrafe'?42:185,progress:u});
};
r30Tick=function(b,dt){if(!v18Owned(b))return V19.base.tick.apply(this,arguments);const S=b._r30,N=S.v18;
 for(const q of N.hazards||[]){q.t+=dt;if(q.t>=q.warm&&q.t<1.8)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-q.x,player.y-q.y)<28)playerHit('visible void well');});}N.hazards=(N.hazards||[]).filter(q=>q.t<q.life);
 if(S.mode==='v19phaseDeath'||S.mode==='v19copyDeath'){
  dt=clamp(dt||0,0,.05);j3Timers(b,dt);dr5TalkTick(b,dt);b.enter=true;b._noHit=true;
  if(S.t>=.55&&!N.deathBurst){N.deathBurst=true;for(const p of b.parts)if(!p.destroyed)v19Rupture(b,p);r30Sound('expBig');shake=Math.max(shake,8);}
  if(S.t>=2.65){if(S.mode==='v19phaseDeath'){N.transition={to:j3State(b).encounter+1,switched:false};v18SetMode(b,'v18phaseFade');}
   else if(V18.forms.every(i=>j3State(b).hp[i]<=0)){N.form=0;v18SetMode(b,'v19FinalReform');}else j3Morph(b,'home');}return;
 }
 if(S.mode==='v19FinalReform'){j3Timers(b,dt);if(S.t>=2.2)j3FinalDeath(b);return;}
 if(S.mode==='fight'&&v19Native(b)){dt=clamp(dt||0,0,.05);j3Timers(b,dt);N.age+=dt;const Q=v17Clock(b);Q.t+=dt;Q.transition+=dt;Q.combat+=dt;dr5TalkTick(b,dt);b.enter=false;b._noHit=false;v19NativeTick(b,dt);return;}
 return V19.base.tick.apply(this,arguments);
};
r30Break=function(b){if(!v18Owned(b))return V19.base.break.apply(this,arguments);if(!r30Live(b))return;
 const J=j3State(b),N=b._r30.v18;N.deathOrigin={x:b.x,y:b.y};N.deathBurst=false;N.deathForm=N.form;j3Save(b);v18Clear(b);b.hp=0;
 if(J.encounter===2){J.hp[N.form]=0;v19Log(b,'copy-defeated',{remaining:V18.forms.filter(i=>J.hp[i]>0)});if(N.form===0&&V18.forms.every(i=>J.hp[i]<=0))return j3FinalDeath(b);v18SetMode(b,'v19copyDeath');}
 else{v19Log(b,'phase-defeated',{phase:J.encounter});v18SetMode(b,'v19phaseDeath');}r30Sound('dracodiaShriek');
};
v18Fade=function(b){return V19.base.fade(b);};
const V19_LOCKED=dr5Locked;dr5Locked=function(){return v18Owned(boss)&&boss._r30.mode.startsWith('v19')?state===GS.PLAY:V19_LOCKED.apply(this,arguments);};
function v19Fragments(b){const rig=v18Rig(b);for(const v of rig)if(!v.spec.hidden)v19Rupture(b,v.p);}
j3FinalDeath=function(b){if(!v18Owned(b))return V19.base.final.apply(this,arguments);const N=b._r30.v18;
 if(dr5State(b).deathStarted)return;N.form=0;N.acting=null;v18Clear(b);V19.base.final(b);N.form=0;N.deathBurst=false;N.deathOrigin={x:b.x,y:b.y};dr5State(b).bodyGone=false;v19Log(b,'final-death');};
dr5Disintegrate=function(b){if(!v18Owned(b))return V19.base.disintegrate.apply(this,arguments);
 const D=dr5State(b);if(D.bodyGone)return;D.bodyGone=true;const frame=V18_ART.models.colossus.frames[0];
 const whole=document.createElement('canvas');whole.width=whole.height=320;const g=whole.getContext('2d',{willReadFrequently:true});for(const a of Object.values(frame))g.drawImage(XART.get(a.key),0,0);
 const k=v18Size(b)/320,N=b._r30.v18;N.shards=[];
 // Actual armor pixels split into even cells and retain one common scale.
 // Native debris remains opaque, travels offscreen and explodes at its end.
 for(let iy=0;iy<4;iy++)for(let ix=0;ix<4;ix++){const x=ix*80,y=iy*80,rgba=g.getImageData(x,y,80,80).data;let filled=0;for(let i=3;i<rgba.length;i+=4)if(rgba[i]>100)filled++;if(filled<50)continue;
  const c=document.createElement('canvas');c.width=c.height=80;c.getContext('2d').drawImage(whole,x,y,80,80,0,0,80,80);const dx=(x+40-160)*k,dy=(y+40-160)*k,a=Math.atan2(dy,dx),i=iy*4+ix,speed=240+i%3*30;
  const shard={image:c,x:b.x+dx,y:b.y+dy,w:80*k,h:80*k,vx:Math.cos(a)*speed,vy:Math.sin(a)*speed-70,rot:0,spin:(i%2?-1:1)*(3+i%4),t:0,life:3.8,stage:run.stage,palette:'purple',nextBlast:.12+i*.025};D27_MODULE_DEBRIS.push(shard);N.shards.push(shard);
 }
 dr5Burst(b,b.x,b.y,330,true);r30Sound('expBig');v19Log(b,'new-colossus-shatter');};
dr5DeathTick=function(b,dt){if(!v18Owned(b))return V19.base.death.apply(this,arguments);dr5Protect(b,dt);const S=b._r30,D=dr5State(b),t=S.t;
 dr5Cue(b,'v19-death-roar',1.2,()=>dr5Scream(b));dr5Cue(b,'v19-death-rupture',4.2,()=>{dr5Disintegrate(b);D.radio=null;});
 if(t>=3.1&&t<7.8){const n=Math.floor((t-3.1)*6);if(n!==D.v19Burst){D.v19Burst=n;dr5Burst(b,b.x+Math.sin(n*2.4)*95,b.y+Math.cos(n*2.4)*100,65+n%3*24);if(n%3===0)r30Sound('expBig');}shake=Math.max(shake,9);}
 for(const [i,q]of (S.v18.shards||[]).entries())if(D27_MODULE_DEBRIS.includes(q)&&q.t>=q.nextBlast){q.nextBlast=q.t+.28+i%3*.07;explode(q.x,q.y,18+i%4*5,'purple','fireball',i%2?'nxp_dense':'nxp_barrage','boss',.08,true);}
 dr5Cue(b,'v19-terminal-shock',7.8,()=>{dr5Burst(b,b.x,b.y,430,true);whiteBlast=.65;});if(t>7.8)whiteBlast=Math.max(0,.65*(1-(t-7.8)/.9));
 if(t>=10.2){S.mode='dr5Portal';S.t=0;D.radio=null;D.events.clear();dr5Ships(b);dr5Say(b,run.pilot.toUpperCase(),'The code is collapsing! That portal is my way home.');dr5Log(b,'portalHomeOpen');r30Sound('teleportIn');}
};
dr5Portrait=function(face,talk=0){if(!v18Owned(boss)||!V19_ART.clips.avatar)return V19.base.portrait.apply(this,arguments);
 const R=dr5State(boss).radio,bank=talk&&V19_ART.clips.avatar_speech?V19_ART.clips.avatar_speech:V19_ART.clips.avatar,i=talk?Math.floor((R?.t||0)*12)%bank.frames.length:0,a=bank.frames[i],key=bank.frames[0].key+':'+i;
 if(V19.portraitCache.has(key))return V19.portraitCache.get(key);if(!XART.rdy(a.key))return null;
 const old=DR5_ART.portrait[0],c=document.createElement('canvas');c.width=old.w;c.height=old.h;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 if(XART.rdy(old.key))g.drawImage(XART.get(old.key),0,0);g.clearRect(38,40,c.width-76,c.height-78);g.fillStyle='#070812';g.fillRect(38,40,c.width-76,c.height-78);
 const w=c.width-76,h=c.height-78,k=Math.min(w/256,h/256);g.drawImage(XART.get(a.key),32,32,256,256,38+(w-256*k)/2,40+(h-256*k)/2,256*k,256*k);
 c.complete=true;c.naturalWidth=c.width;c.naturalHeight=c.height;V19.portraitCache.set(key,c);V19.draws.avatar=(V19.draws.avatar||0)+1;return c;
};
r30DrawBoss=function(b){if(!v18Owned(b))return V19.base.draw.apply(this,arguments);const S=b._r30,N=S.v18,J=j3State(b);
 if(S.mode==='dr5Death'){if(S.t<4.2)v19Clip('colossus_death',S.t,4.2,b,422);dr5EffectsDraw(b);return;}
 if(S.mode==='v19FinalReform'){v18Clip('colossus_emerge',S.t,2.2,b.x,b.y,v18Size(b));return;}
 if(S.mode==='v19phaseDeath'){v19Clip(J.encounter===0?'infused_death':'ghost_death',S.t,2.65,b);dr5EffectsDraw(b);return;}
 if(S.mode==='v19copyDeath'){const t=S.t,size=v18Size(b);if(t<.55)v19Body(b);else if(N.deathForm===0)v19Clip('colossus_death',t-.55,2.1,b,size);else v17Code(S.clock*14,b.x,b.y,200,.75);
  dr5EffectsDraw(b);return;}
 if(S.mode==='v18phaseFade'&&!N.transition?.switched){v19Clip(J.encounter===0?'infused_death':'ghost_death',1,1,b);return;}
 if(S.mode==='fight'&&v19Native(b)){v19DonorDraw(b);return;}
 if(J.encounter===2&&N.form===0&&(S.mode==='fight'||S.mode==='dr5Monologue')){
  const P=N.attack,R=dr5State(b).radio,roar=S.mode==='dr5Monologue'&&R?.face===5;
  const bank=roar?'colossus_roar':N.acting;if(bank&&v19Acting(b)?.layers){v19Body(b);v18Warnings(b);return;}
 }
 // A Hammer morph must never briefly paste the rejected third arm back in.
 if(['v18formIn','v18formOut'].includes(S.mode)&&[N.form,N.from,N.to].some(i=>[8,6,2].includes(i))){
  const out=S.mode==='v18formOut';ctx.save();ctx.globalAlpha=out?1-clamp((S.t-.35)/.65,0,1):clamp((S.t-.25)/1.1,0,1);v19Body(b);ctx.restore();
  v17Portal('black_void',PL11.sample('black_void',out?'form':'close',S.t,{duration:out?1.45:1.6}),b.x,b.y,v18Size(b)*1.12,.98,S.t*.35);
  V19.draws.cleanNativeTransition=(V19.draws.cleanNativeTransition||0)+1;return;
 }
 const result=V19.base.draw.apply(this,arguments);for(const q of N.hazards||[])v17Portal('black_void',PL11.sequence('black_void',q.t,{form:q.warm,loop:.9,close:.6}),q.x,q.y,84,.92);
 return result;
};
v18Clear=function(b){V19.base.clear(b);b._r30.v18.hazards=[];b._r30.v18.swipe=null;};
globalThis.BOF_STAGE8_IDENTITY=V19;
