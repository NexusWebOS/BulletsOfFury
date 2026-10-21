"use strict";
/* Dracodia volcano: one articulated hierarchy owns visible anatomy, muzzle
   sockets, alpha hits, target locks and real module destruction. */
const VP23={base:{enter:v18Enter,rig:v19VolcanoRig,paint:v19Paint,at:v19AtRect,hit:modularHit,
 targets:retinaBossTargets,tick:v19NativeTick,mount:furnaceMount,muzzle:furnaceMuzzle,
 combat:furnaceCombat,tell:fztTell,beam:fztBeam,shot:fztShot,swipe:v19SwipeWarning,body:v19Body,
 keys:v18Keys,warm:v18Warm,load:stageLoadBegin,draw:v19DonorDraw,py:fztPy,phase:furnaceEnter,next:furnaceNext,route:furnaceFurySquareRoute},draws:{},events:[],glows:new Map(),active:null};
const VP23_GROUPS={left:[['shoulderL',.30],['left',.70]],right:[['shoulderR',.30],['right',.70]],
 body:[['ventL',.10],['ventR',.10],['legL',.15],['legR',.15],['core',.50]],head:[['head',1]]};
function vp23Own(b){return v19Native(b)&&b._r30.v18.form===2;}
function vp23Proxy(p){return p?._gp4Host&&vp23Own(p._gp4Host);}
function vp23Keys(){return [...Object.values(VP23_ART.parts),VP23_ART.socket,...VP23_ART.flame.frames].map(a=>a.key);}
for(const a of [...Object.values(VP23_ART.parts),VP23_ART.socket,...VP23_ART.flame.frames])XART._src[a.key]=a.path;
function vp23Warm(){let ready=true;for(const k of vp23Keys())if(!XART.rdy(k))ready=false;return ready;}
v18Keys=function(){return [...VP23.base.keys(),...vp23Keys()];};
v18Warm=function(){const before=VP23.base.warm();return vp23Warm()&&before;};
stageLoadBegin=function(n,keys){return VP23.base.load.call(this,n,n===8?[...(keys||[]),...vp23Keys()]:keys);};
function vp23Log(event,data={}){VP23.events.push({event,...data});if(VP23.events.length>250)VP23.events.shift();}
function vp23Group(id){for(const [group,rows] of Object.entries(VP23_GROUPS))if(rows.some(a=>a[0]===id))return group;return null;}
function vp23Sync(b){const F=gd4Create(b,2).p._fz;
 for(const p of b.parts)if(p._vp23&&p.hp<=0)p.destroyed=true;
 for(const key of Object.keys(F.pools))if(!VP23_GROUPS[key]){delete F.pools[key];delete F.max[key];}
 for(const [group,rows] of Object.entries(VP23_GROUPS)){F.pools[group]=rows.reduce((sum,[id])=>sum+Math.max(0,b.parts.find(q=>q.id===id)?.hp||0),0);F.max[group]=rows.reduce((sum,[id])=>sum+(b.parts.find(q=>q.id===id)?.maxhp||0),0);}
}
function vp23Modules(b){if(b.parts.every(p=>p._vp23)){vp23Sync(b);return;}
 const old=b.parts.slice(),parts=[];
 for(const [group,rows] of Object.entries(VP23_GROUPS)){const source=old.find(p=>p.id===(group==='body'?'core':group)),max=Math.max(0,source?.maxhp||0);let remaining=max,health=Math.min(max,Math.max(0,source?.hp||0));
  for(let i=0;i<rows.length;i++){const [id,share]=rows[i],budget=i===rows.length-1?remaining:Math.round(max*share),hp=i===rows.length-1?health:Math.min(health,Math.round((source?.hp||0)*share));remaining-=budget;health-=hp;
   const p=v19Part(id,hp,{role:id==='head'?'head':id==='core'?'core':'weapon',group,label:id});p.maxhp=budget;p.hp=hp;p.destroyed=hp<=0;p._vp23=true;parts.push(p);}}
 b.parts=parts;j3State(b).modules[2]=parts;vp23Sync(b);vp23Log('anatomy',{parts:parts.map(p=>p.id),hp:parts.reduce((s,p)=>s+p.hp,0)});
}
v18Enter=function(b){const result=VP23.base.enter.apply(this,arguments);if(vp23Own(b))vp23Modules(b);return result;};
function vp23Pose(b){const F=gd4Create(b,2).p._fz,N=b._r30.v18,live=b._r30.mode==='fight',t=live?F.t:0,
 charge=live?Math.max(F.charge||0,F.arm.left.charge||0,F.arm.right.charge||0):0,
 flame=live&&F.beams.some(q=>q.kind==='flame'),recoil=live?clamp((F.arm.right.recoil||0)/35,0,1):0,
 fold=live&&F.phase==='core'&&['rotor','rollerball'].includes(F.attack)?v19Ease(F.at/1.2):0;
 return {F,N,live,t,charge,flame,recoil,fold,root:live?F.a:0,heat:live?clamp(charge+(flame?.5:0)+recoil*.3,0,1):0};
}
function vp23Point(v,at){return v19WorldPoint(v,at);}
v19VolcanoRig=function(b){if(!vp23Own(b))return VP23.base.rig.apply(this,arguments);if(gd4Create(b,2).p._fz.phase==='head')return VP23.base.rig.apply(this,arguments).filter(v=>!v.p.destroyed);
 if(!b.parts.every(p=>p._vp23))vp23Modules(b);const P=vp23Pose(b),{F,N}=P,k=v18Size(b)/320,out=[],lookup={},c=Math.cos(P.root),s=Math.sin(P.root);
 const root=at=>({x:b.x+(at[0]-160)*k*c-(at[1]-160)*k*s,y:b.y+(at[0]-160)*k*s+(at[1]-160)*k*c});
 const add=(id,at,rot=P.root,scale=1)=>{const a=VP23_ART.parts[id],p=b.parts.find(q=>q.id===a.owner);if(!p||p.destroyed)return null;
  const anchor=a.anchor,q=a.bounds,K=k*scale,dx=((q[0]+q[2])/2-anchor[0])*K,dy=((q[1]+q[3])/2-anchor[1])*K,cc=Math.cos(rot),ss=Math.sin(rot);
  const v={p,key:a.key,a,anchor,ax:at.x,ay:at.y,k:K,rot,x:at.x+dx*cc-dy*ss,y:at.y+dx*ss+dy*cc,w:(q[2]-q[0])*K,h:(q[3]-q[1])*K,alpha:1,layer:id,spec:{role:p.spec.role},_vp23:true,z:out.length};out.push(v);lookup[id]=v;return v;};
 const bearing=(id,p,at,rot)=>{if(!p||p.destroyed)return;const a=VP23_ART.socket;out.push({p,key:a.key,a,anchor:a.anchor,ax:at.x,ay:at.y,k,rot,x:at.x,y:at.y,w:24*k,h:24*k,alpha:1,layer:'bearing_'+id,spec:{role:p.spec.role},_vp23:true,_vp23Joint:true,z:out.length});};
 add('torso',root(VP23_ART.parts.torso.anchor));
 for(const side of ['L','R']){const sign=side==='L'?-1:1,hip=VP23_ART.parts['thigh'+side].anchor,
  bend=sign*(P.fold*.92+P.recoil*.12+(P.live?Math.sin(P.t*1.5+sign)*.035:0));
  const thigh=add('thigh'+side,root(hip),P.root+bend);if(thigh){const knee=vp23Point(thigh,VP23_ART.parts['foot'+side].anchor);add('foot'+side,knee,P.root+lerp(-bend*.48,sign*1.8,P.fold));bearing('knee'+side,thigh.p,knee,P.root);bearing('hip'+side,thigh.p,root(hip),P.root);}
 }
 for(const side of ['L','R']){const sign=side==='L'?-1:1,id='vent'+side,a=VP23_ART.parts[id],v=add(id,root(a.anchor),P.root+sign*(-P.fold*1.1+P.heat*.11));
  if(v){add('flare'+side,vp23Point(v,VP23_ART.parts['flare'+side].anchor),v.rot);bearing('vent'+side,v.p,{x:v.ax,y:v.ay},P.root);}
 }
 for(const side of ['left','right']){const tag=side==='left'?'L':'R',sign=side==='left'?-1:1,shoulder=VP23_ART.parts['upper'+tag].anchor,station=root(shoulder),Q=N.swipe?.q,
  aim=P.live?P.root+(F.arm[side]?.a||0):0;let upper=P.root+sign*(P.charge*.10+P.recoil*.07+(P.live?Math.sin(P.t*1.1+sign)*.025:0));
  if(Q?.id===side){const at={x:b.x+Q.off.x,y:b.y+Q.off.y},elbow=VP23_ART.parts[side].anchor;upper=Math.atan2(at.y-station.y,at.x-station.x)-Math.atan2(elbow[1]-shoulder[1],elbow[0]-shoulder[0]);}
  add('shoulder'+tag,station,P.root+(upper-P.root)*.35);
  const arm=add('upper'+tag,station,upper);if(!arm)continue;let at=vp23Point(arm,VP23_ART.parts[side].anchor),a=VP23_ART.parts[side],tip=V19_ART.volcanoMuzzles[side],base=Math.atan2(a.anchor[0]-tip[0],tip[1]-a.anchor[1]),rot=P.live?aim-base:0;
  rot=v19SwipeRotation(b,side,rot);if(side==='right'&&P.live&&!Q){const back=fztPt(at.x,at.y,aim,-P.recoil*6*k);at=back;}
  const forearm=add(side,at,rot);if(forearm){bearing('elbow'+tag,forearm.p,vp23Point(arm,VP23_ART.parts[side].anchor),upper);bearing('shoulder'+tag,forearm.p,station,P.root);}
 }
 const reactor=add('reactor',root(VP23_ART.parts.reactor.anchor),P.root,1+P.heat*.08-P.recoil*.025);
 const headAt=root(VP23_ART.parts.head.anchor);headAt.y+=P.fold*10*k;add('head',headAt,P.root+(P.live?Math.sin(P.t*.8)*.025:0));
 return out.sort((a,b)=>Number(b.layer===b.p.id)-Number(a.layer===a.p.id));
};
v19Body=function(b){if(!vp23Own(b))return VP23.base.body.apply(this,arguments);const rig=v18Rig(b),Q=b._r30.v18.swipe?.q;
 if(Q&&Q.t>Q.tell&&Q.t<Q.tell+Q.swing){const v=rig.find(v=>v.layer===Q.id);if(v)for(const ago of [.08,.04]){ctx.save();ctx.globalAlpha*=ago===.08?.09:.18;v19Paint({...v,rot:v19SwipeAngle(Q,Math.max(Q.tell,Q.t-ago))},b);ctx.restore();}}
 for(const v of rig.sort((a,b)=>a.z-b.z))v19Paint(v,b);
};
v18Body=v19Body;
function vp23Glow(a){if(VP23.glows.has(a.key))return VP23.glows.get(a.key);if(!XART.rdy(a.key))return null;const c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d');g.drawImage(XART.get(a.key),0,0);const d=g.getImageData(0,0,c.width,c.height);for(let i=0;i<d.data.length;i+=4)if(!(d.data[i]>170&&d.data[i+1]>60&&d.data[i]>d.data[i+2]*1.5))d.data[i+3]=0;g.putImageData(d,0,0);VP23.glows.set(a.key,c);return c;}
v19Paint=function(v,b){if(!v._vp23)return VP23.base.paint.apply(this,arguments);const P=vp23Pose(b),flare=v.layer.startsWith('flare');
 if(v._vp23Joint){ctx.save();ctx.translate(v.ax,v.ay);ctx.rotate(v.rot);ctx.imageSmoothingEnabled=false;const rect=[-24*v.k,-24*v.k,48*v.k,48*v.k];ctx.drawImage(XART.get(v.key),...rect);const flash=Math.max(v.p.flash||0,b.flash||0);if(flash>0){ctx.globalAlpha*=Math.min(.8,flash/.12);ctx.drawImage(xartTint(v.key,'#fff',1),...rect);}ctx.restore();}
 else if(flare&&VP23_ART.flame.frames.length){const i=(Math.floor(P.t*20)+(v.layer==='flareR'?7:0))%VP23_ART.flame.frames.length,a=VP23_ART.flame.frames[i];ctx.save();ctx.translate(v.ax,v.ay);ctx.rotate(v.rot);ctx.imageSmoothingEnabled=false;const K=v.k*(.7+.3*P.heat);ctx.drawImage(XART.get(a.key),-64*K,-96*K,128*K,128*K);const flash=Math.max(v.p.flash||0,b.flash||0);if(flash>0){ctx.globalAlpha*=Math.min(.8,flash/.12);ctx.drawImage(xartTint(a.key,'#fff',1),-64*K,-96*K,128*K,128*K);}ctx.restore();}
 else{VP23.base.paint.apply(this,arguments);if(['reactor','left','right','ventL','ventR'].includes(v.layer)){const glow=vp23Glow(v.a);if(glow){ctx.save();ctx.translate(v.ax,v.ay);ctx.rotate(v.rot);ctx.globalCompositeOperation='lighter';ctx.globalAlpha*=.10+P.heat*.55;ctx.drawImage(glow,-v.anchor[0]*v.k,-v.anchor[1]*v.k,v.a.w*v.k,v.a.h*v.k);ctx.restore();}}}
 VP23.draws[v.layer]=(VP23.draws[v.layer]||0)+1;
};
v19AtRect=function(v,x,y){if(!v._vp23)return VP23.base.at.apply(this,arguments);if(v.layer.startsWith('flare'))return false;const c=Math.cos(-v.rot),s=Math.sin(-v.rot),dx=x-v.ax,dy=y-v.ay,px=Math.floor((dx*c-dy*s)/v.k+v.anchor[0]),py=Math.floor((dx*s+dy*c)/v.k+v.anchor[1]),m=v18Mask(v.a);return !!(m&&px>=0&&py>=0&&px<v.a.w&&py<v.a.h&&m[py*v.a.w+px]>48);};
function vp23Vulnerable(b,p){return !p.destroyed&&furnaceVulnerable(gd4Create(b,2).p).includes(vp23Group(p.id));}
retinaBossTargets=function(b){if(!vp23Own(b))return VP23.base.targets.apply(this,arguments);if(!r30Live(b)||b._noHit)return[];
 return b.parts.filter(p=>vp23Vulnerable(b,p)).map(p=>retinaDynamicPiece(b,'vp23-'+p.id,p.id,()=>{const vs=v18Rig(b).filter(v=>v.p===p&&!v.layer.startsWith('flare')),v=vs.find(v=>['left','right','reactor','ventL','ventR','footL','footR','head','shoulderL','shoulderR'].includes(v.layer))||vs[0];return{x:v?.x||b.x,y:v?.y||b.y,hp:p.hp,dead:!vp23Own(b)||b._noHit||!vp23Vulnerable(b,p)||!v};},d=>{b._lastPart=p;hitBoss(d);},48,48));
};
modularHit=function(dmg){const b=boss;if(!vp23Own(b))return VP23.base.hit.apply(this,arguments);if(!r30Live(b)||b._noHit||!(dmg>0))return;
 const native=gd4Create(b,2).p,F=native._fz,p=b.parts.includes(b._lastPart)&&!b._lastPart.destroyed?b._lastPart:b.parts.find(p=>vp23Vulnerable(b,p));if(!p)return;
 markHit(p,.12);markHit(b,.12);markHit(native,.12);if(!vp23Vulnerable(b,p))return;const group=vp23Group(p.id),damage=Math.min(p.hp,dmg);p.hp=Math.max(0,p.hp-damage);F.flash[group]=.12;stageStats.dmgDealt+=damage;
 if(p.hp<=0){v19Rupture(b,p);p.destroyed=true;const emitter=p.id==='core'?'reactor':p.id;F.beams=F.beams.filter(q=>q._vp23Emitter!==emitter);F.tells=F.tells.filter(q=>q._vp23Emitter!==emitter);if(p.id==='right')F.fx=F.fx.filter(q=>q.key!=='fzt_cannon_flash');Snd.play('shieldBreakCombat');vp23Log('module-break',{id:p.id,group});}
 vp23Sync(b);b.hp=Math.max(0,Math.min(b.hp-damage,Object.values(F.pools).reduce((s,h)=>s+h,0)));native.hp=b.hp;
 if(F.phase==='arms'&&F.pools.left<=0&&F.pools.right<=0){furnaceEnter(native,'core');vp23Log('phase',{phase:'core'});}
 else if(F.phase==='core'&&F.pools.body<=0){furnaceEnter(native,'head');vp23Log('phase',{phase:'head'});}
 j3Save(b);if(b.hp<=0){furnaceClear(native);r30Break(b);}
};
fztPy=function(y){return VP23.active?viewTopY()+viewH()*.46+(y-240)*viewH()/1000:VP23.base.py.apply(this,arguments);};
v19NativeTick=function(b,dt){if(!vp23Own(b))return VP23.base.tick.apply(this,arguments);vp23Sync(b);const prior=VP23.active;VP23.active=b;try{return VP23.base.tick.apply(this,arguments);}finally{VP23.active=prior;}};
furnaceEnter=function(p){if(!vp23Proxy(p))return VP23.base.phase.apply(this,arguments);const prior=VP23.active;VP23.active=p._gp4Host;try{return VP23.base.phase.apply(this,arguments);}finally{VP23.active=prior;}};
function vp23Missing(b,id){return !!b.parts.find(p=>p.id===id)?.destroyed;}
function vp23AttackAvailable(b,F){if(F.phase==='arms'&&F.attack==='cannon')return !vp23Missing(b,'right')||vp23Missing(b,'left');
 if(F.phase==='core'){if(['ring','coreLaser'].includes(F.attack))return !vp23Missing(b,'core');if(F.attack==='rotor')return !vp23Missing(b,'ventL')||!vp23Missing(b,'ventR');if(F.attack==='rollerball')return !vp23Missing(b,'legL')||!vp23Missing(b,'legR');}return true;}
furnaceNext=function(p){if(!vp23Proxy(p))return VP23.base.next.apply(this,arguments);let out;for(let i=0;i<7;i++){out=VP23.base.next.apply(this,arguments);if(vp23AttackAvailable(p._gp4Host,p._fz))break;}return out;};
furnaceFurySquareRoute=function(W){const rows=VP23.base.route.apply(this,arguments);if(VP23.active)for(const q of rows)q.y=clamp(q.y,viewTopY()+72+144,viewTopY()+viewH()-144);return rows;};
// Weapon destruction disables that emitter even while its shoulder armor is
// still targetable. The shared four native pools remain sums of real modules.
furnaceCombat=function(p,dt){if(!vp23Proxy(p))return VP23.base.combat.apply(this,arguments);const b=p._gp4Host,F=p._fz,saved={};
 if(F.phase==='core'&&F.attack==='rollerball'&&diffKey!=='furious'&&F.rollY==null){const margin=Math.max(96,p.w*.5);F.rollY=clamp(player.y,viewTopY()+72+144,viewTopY()+viewH()-144);F.rollStartY=p.y;F.rollFrom=F.dir>0?margin:worldWidth()-margin;F.rollTo=F.dir>0?worldWidth()-margin:margin;fztSfx('bossWeaponCharge');}
 if(F.phase==='arms')for(const side of ['left','right'])if(b.parts.find(q=>q.id===side)?.destroyed){saved[side]=F.pools[side];F.pools[side]=0;}
 const first=eBullets.length;try{return VP23.base.combat.apply(this,arguments);}finally{for(const [side,hp] of Object.entries(saved))F.pools[side]=hp;vp23Position(p);vp23Rebase(p,first);}
};
function vp23Position(p){const b=p._gp4Host,was={x:p.x,y:p.y};b.x=p.x;b.y=p.y;const rig=v19VolcanoRig(b);if(!rig.length)return{x:0,y:0};const l=Math.min(...rig.map(v=>v.x-(Math.abs(Math.cos(v.rot))*v.w+Math.abs(Math.sin(v.rot))*v.h)/2)),r=Math.max(...rig.map(v=>v.x+(Math.abs(Math.cos(v.rot))*v.w+Math.abs(Math.sin(v.rot))*v.h)/2)),dx=r-l>viewW()-16?(camLeftX()+camRightX()-l-r)/2:l<camLeftX()+8?camLeftX()+8-l:r>camRightX()-8?camRightX()-8-r:0;b.x+=dx;p.x=b.x;return{x:p.x-was.x,y:p.y-was.y};}
function vp23Socket(p,id){const v=v19VolcanoRig(p._gp4Host).find(v=>v.layer===id);if(!v)return null;return vp23Point(v,id==='left'||id==='right'?V19_ART.volcanoMuzzles[id]:id==='reactor'?VP23_ART.parts.reactor.anchor:VP23_ART.parts[id==='ventL'?'flareL':'flareR'].anchor);}
function vp23Rebase(p,first){const F=p._fz;for(const q of [...F.beams,...F.tells])if(q._vp23Emitter){const at=vp23Socket(p,q._vp23Emitter);if(!at)continue;const dx=at.x-q.x,dy=at.y-q.y;q.x=at.x;q.y=at.y;q.ex+=dx;q.ey+=dy;}
 for(const q of eBullets.slice(first))if(q._vp23Emitter){const at=vp23Socket(p,q._vp23Emitter);if(at){q.x=at.x;q.y=at.y;}}
 for(const q of F.fx)if(q.key==='fzt_cannon_flash'&&q.life===q.max){const at=vp23Socket(p,'right');if(at){q.x=at.x;q.y=at.y;}}
}
furnaceMount=function(p,side){if(!vp23Proxy(p))return VP23.base.mount.apply(this,arguments);vp23Position(p);const v=v19VolcanoRig(p._gp4Host).find(v=>v.layer===side);return v?{x:v.ax,y:v.ay,a:p._fz.a+p._fz.arm[side].a}:{x:p.x,y:p.y,a:0};};
furnaceMuzzle=function(p,side){if(!vp23Proxy(p))return VP23.base.muzzle.apply(this,arguments);vp23Position(p);const at=vp23Socket(p,side),m=at?{...at,a:p._fz.a+p._fz.arm[side].a}:{x:p.x,y:p.y,a:0};(p._fz._vp23Muzzles??={})[side]=m;return m;};
function vp23Emitter(F,x,y){const b=boss;if(!vp23Own(b)||gd4Create(b,2).p._fz!==F||F.phase!=='core')return{x,y};const rig=v19VolcanoRig(b);
 if(F.attack==='coreLaser'||F.attack==='ring'){const v=rig.find(v=>v.layer==='reactor');return v?vp23Point(v,VP23_ART.parts.reactor.anchor):{x,y};}
 if(F.attack==='rotor'){const side=(x-b.x)*Math.cos(F.a)+(y-b.y)*Math.sin(F.a)<0?'L':'R',v=rig.find(v=>v.layer==='vent'+side);return v?vp23Point(v,VP23_ART.parts['flare'+side].anchor):{x,y};}return{x,y};}
function vp23EmitterGone(F,x,y){const b=boss;if(!vp23Own(b)||gd4Create(b,2).p._fz!==F||F.phase!=='core')return false;if(['coreLaser','ring'].includes(F.attack))return vp23Missing(b,'core');if(F.attack==='rotor'){const side=(x-b.x)*Math.cos(F.a)+(y-b.y)*Math.sin(F.a)<0?'L':'R';return vp23Missing(b,'vent'+side);}return false;}
function vp23Route(F,x,y){const b=boss;if(!vp23Own(b)||gd4Create(b,2).p._fz!==F)return null;if(F.phase==='core'){if(['coreLaser','ring'].includes(F.attack))return 'reactor';if(F.attack==='rotor')return (x-b.x)*Math.cos(F.a)+(y-b.y)*Math.sin(F.a)<0?'ventL':'ventR';}if(F.phase==='arms'){const rows=Object.entries(F._vp23Muzzles||{}).sort((a,b)=>Math.hypot(a[1].x-x,a[1].y-y)-Math.hypot(b[1].x-x,b[1].y-y));return rows[0]?.[0]||null;}return null;}
fztTell=function(F,x,y){if(vp23EmitterGone(F,x,y))return;const route=vp23Route(F,x,y),at=vp23Emitter(F,x,y),args=[...arguments],n=F.tells.length;args[1]=at.x;args[2]=at.y;const out=VP23.base.tell.apply(this,args);for(const q of F.tells.slice(n))q._vp23Emitter=route;return out;};
fztBeam=function(F,x,y){if(vp23EmitterGone(F,x,y))return;const route=vp23Route(F,x,y),at=vp23Emitter(F,x,y),args=[...arguments],n=F.beams.length;args[1]=at.x;args[2]=at.y;const out=VP23.base.beam.apply(this,args);for(const q of F.beams.slice(n))q._vp23Emitter=route;return out;};
fztShot=function(p,x,y){if(!vp23Proxy(p))return VP23.base.shot.apply(this,arguments);const F=p._fz;if(vp23EmitterGone(F,x,y))return;const at=vp23Emitter(F,x,y),args=[...arguments],n=eBullets.length;args[1]=at.x;args[2]=at.y;const out=VP23.base.shot.apply(this,args);for(const q of eBullets.slice(n))q._vp23Emitter=F.phase==='arms'?'right':F.phase==='core'?'reactor':null;return out;};
v19SwipeWarning=function(b){if(!vp23Own(b))return VP23.base.swipe.apply(this,arguments);const saved=combatWarningDraw;combatWarningDraw=function(owner,q){if(owner===b&&q?.alertOnly)return;return saved.apply(this,arguments);};try{return VP23.base.swipe.apply(this,arguments);}finally{combatWarningDraw=saved;}};
globalThis.BOF_DRACODIA_VOLCANO={state:VP23,warm:vp23Warm,rig:v19VolcanoRig};
