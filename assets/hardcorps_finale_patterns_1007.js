"use strict";
/* Physical signatures inserted BETWEEN the existing source-controller moves.
   HP pools, copied source identity, emergency phases, and Hammer remain native. */
const HF7={events:[],draws:0,base:{tick:r30Tick,parts:r30Parts,rig:fmcRig,ghost:aa5GhostRig,draw:r30DrawBoss,clear:j3Clear,mimic:j3Mimic,encounter:j3Encounter,hit:modularHit}};
const HF7_BOOK={host:{name:'MUTATION SPEAR',ids:['left','right'],kind:'arms',active:1.35},ghost:{name:'SPECTRAL RAIL RELAY',ids:['cannon','eye'],kind:'rail',active:3.45},home:{name:'COLOSSUS CROWN GATE',ids:['left','right'],kind:'gate',active:2.1},
 0:{name:'CHROMIUM PINCER',ids:['left','right'],kind:'pincer',active:1.75},1:{name:'SONIC BROADSIDE',ids:['left','right'],kind:'pass',active:2.25},2:{name:'FURNACE BELLOWS',ids:['left','right'],kind:'bellows',active:2.4},
 3:{name:'CRYO SHUTTERS',ids:['gunL1','gunL2','gunR1','gunR2'],kind:'shutters',active:3.45},4:{name:'STORM SCISSORS',ids:['lightning'],kind:'scissors',active:5.15},
 5:{name:'SHIELD BAIT / SWORD RIPOSTE',ids:['sword'],kind:'riposte',active:1.65},6:{name:'HARRIER TURBINE PRESS',ids:['fanL','fanR','beam'],kind:'press',active:3.45},7:{name:'WARDEN CLAW VAULT',ids:['left','right'],kind:'vault',active:1.6}};
function hf7Identity(b){const J=j3State(b);return !J||J.mimic===8?null:J.encounter===0?'host':J.encounter===1?'ghost':J.mimic==null?'home':String(J.mimic);}
function hf7Log(b,event,data={}){HF7.events.push({event,form:hf7Identity(b),...data});if(HF7.events.length>240)HF7.events.shift();}
function hf7Alive(b,id){return !b.dead&&b.hp>0&&!!b.parts?.some(p=>p.id===id&&!p.destroyed&&p.hp>0);}
function hf7Rig(b){const id=hf7Identity(b);return id==='ghost'?HF7.base.ghost(b):id==='host'||id==='home'||id==='0'?HF7.base.parts(b):hf7AuthoredRig(b);}
function hf7AuthoredRig(b){const K=hf7State(b)?.sig;if(K?.def.kind!=='riposte')return HF7.base.rig(b);
 // Knight is an authored whole-body pose with tool attachment landmarks. Use
 // those landmarks instead of sliding a weapon away from its depicted hand.
 const S=b._r30,previous=S.hkKnight,u=K.t-K.tell,phase=u<0?'tell':u<.42?'jump':u<1.0?'land':u<K.active?'rise':'recover';
 try{S.hkKnight={kind:'leapSlash',phase,t:Math.max(0,u-1),side:K.tx<b.x?-1:1};return HF7.base.rig(b);}finally{S.hkKnight=previous;}
}
function hf7Port(b,id){const v=hf7Rig(b).find(v=>v.p.id===id);if(!v)return null;return {...v,x:v.x-Math.sin(v.rot||0)*v.h*.35,y:v.y+Math.cos(v.rot||0)*v.h*.35};}
function hf7State(b){return b?._r30?.hf7;}
function hf7Cancel(b,reason='clear'){const H=hf7State(b);if(H?.sig){hf7Log(b,'cancel',{reason});H.sig=null;}eBullets=eBullets.filter(q=>q._hf7Owner!==b);}
function hf7Between(b){const S=b._r30,J=j3State(b);if(S.attack||S.returning||S.hkKnight||S.mode!=='fight'||b.enter)return false;
 if(!(J.mimic>0))return true;const D=J.gp4Donors?.[J.mimic];if(!D||f6Busy(D))return false;const p=D.p;
 if(J.mimic===1)return p._ovState==='fight';if(J.mimic===2)return p._fz?.attack==='cannon'&&((p._fz.at||0)%2.05)>.85;
 if(J.mimic===3||J.mimic===4)return p._er26?.mode==='recover';if(J.mimic===5)return !S.hkKnight;
 if(J.mimic===7)return p._s7mod?.mode==='recover';return true;
}
function hf7Start(b){const id=hf7Identity(b),def=HF7_BOOK[id];if(!def)return null;const H=b._r30.hf7??={id,cd:5,n:0},T=f6Target(b),rank=Math.max(0,hc1007Rank());
 const K=H.sig={id,def,t:0,tell:hc1007Rank()<0?1.85:1.55,active:def.active,recover:hc1007Rank()<0?1.5:rank===0?1.3:1.15,
  n:++H.n,tx:clamp(T.x,camLeftX()+95,camRightX()-95),ty:clamp(T.y,PLAY.y+230,VH-80),seat:T.seat,origin:{x:b.x,y:b.y},ports:[],pose:{},lines:[],phase:'tell',lastRelease:-1};
 for(const module of def.ids){const p=hf7Port(b,module);if(p&&hf7Alive(b,module))K.ports.push({module,x:p.x,y:p.y,cx:p.x+Math.sin(p.rot||0)*p.h*.35,cy:p.y-Math.cos(p.rot||0)*p.h*.35,w:p.w,h:p.h,rot:p.rot||0});}
 if(!K.ports.length){H.sig=null;H.cd=4;return null;}
 const kind=def.kind;
 for(let i=0;i<K.ports.length;i++){const p=K.ports[i],side=p.x<b.x?-1:1;let tx=K.tx,ty=K.ty,width=20;
  if(kind==='gate'||kind==='pincer'){tx=clamp(K.tx+side*(kind==='gate'?105:88),camLeftX()+42,camRightX()-42);width=kind==='gate'?58:42;}
  if(kind==='arms'){if(i!==K.n%K.ports.length)continue;width=54;}
  if(kind==='vault'){tx=K.tx+side*70;width=66;}
  if(kind==='riposte'){width=48;tx=K.tx;}
  if(['arms','gate','pincer','riposte','vault'].includes(kind)){K.lines.push({...p,ex:tx,ey:ty,width,physical:true});continue;}
  if(kind==='pass'){K.lines.push({...p,x:camLeftX()-120,y:K.ty-100,ex:camRightX()+120,ey:K.ty-100,width:110,physical:true});break;}
  if(kind==='bellows'){const a=Math.PI/2-side*.36;K.lines.push({...p,...hc1007Line(p,a,24),a,color:'fire'});}
  if(kind==='rail'){const a=Math.atan2(K.ty-p.y,K.tx-p.x)+(i===0?.18:-.24);K.lines.push({...p,...hc1007Line(p,a,18),a,color:'ice',beat:i%2});}
  if(kind==='shutters'){tx=clamp(K.tx+[-160,-85,85,160][i],camLeftX()+25,camRightX()-25);const a=Math.atan2(VH+70-p.y,tx-p.x);K.lines.push({...p,...hc1007Line(p,a,17),a,color:'ice',beat:i%2});}
  if(kind==='scissors')for(const a of [.20,Math.PI+.20])K.lines.push({...p,...hc1007Line(p,a,20),a,color:'ice'});
  if(kind==='press'){if(p.module==='beam'){const a=Math.atan2(K.ty-p.y,K.tx-p.x);K.lines.push({...p,...hc1007Line(p,a,28),a,color:'ice',beat:1});}else{const a=Math.PI/2+side*.25;K.lines.push({...p,...hc1007Line(p,a,24),a,color:'fire',beat:0});}}
 }
 const D=j3State(b).gp4Donors?.[j3State(b).mimic];if(D){D.aa5Salvo=null;D.aa5Cd=999;K.donorClock=D.p.t;}
 r30Sound('bossWeaponCharge');hc1007Warm();hf7Log(b,'signature',{name:def.name,target:[K.tx,K.ty],seat:K.seat,modules:K.ports.map(p=>p.module)});return K;
}
function hf7Sample(b){const K=hf7State(b)?.sig;if(!K)return null;const u=K.t-K.tell,kind=K.def.kind,lines=K.lines.filter(L=>hf7Alive(b,L.module));
 let phase=K.t<K.tell?'tell':u<K.active?'live':'recover',progress=clamp(K.t/K.tell,0,1),beat=0,alpha=phase==='live'?1:0;
 if(['rail','shutters','press'].includes(kind)&&phase==='live'){
  // First discharge .9s, then a fully absent 1.4s warning before relay release.
  if(u<.90){beat=0;}else if(u<1.1){phase='dissolve';alpha=1-(u-.9)/.2;beat=0;}
  else if(u<2.5){phase='tell';progress=(u-1.1)/1.4;beat=1;}else{beat=1;}
 }
 if(kind==='scissors'&&phase==='live'){
  const local=u%2.65;beat=Math.floor(u/2.65);
  if(local<1.05){}else if(local<1.25){phase='dissolve';alpha=1-(local-1.05)/.2;}
  else{phase=beat===0?'tell':'gap';progress=(local-1.25)/1.4;}
 }
 const chosen=lines.filter(L=>L.beat==null||L.beat===beat).map(L=>{if(L.physical)return L;
  const rig=K.id==='ghost'?aa5GhostRig(b):fmcRig(b),v=rig.find(v=>v.p.id===L.module),p=v?(v.ax!=null?fmcPoint(v,...(v.spec.emit||[.5,.85])):{x:v.x-Math.sin(v.rot||0)*v.h*.35,y:v.y+Math.cos(v.rot||0)*v.h*.35}):L;
  const a=kind==='scissors'?L.a+Math.max(0,Math.min(u,K.active))*Math.PI/K.active:L.a;return {...L,...hc1007Line(p,a,L.width),a};});
 return{K,u,phase,progress,beat,alpha,lines:chosen};
}
function hf7PoseApply(b,rig){const K=hf7State(b)?.sig;if(!K)return rig;return rig.map(v=>{if(v._hf7Posed)return v;const p=K.pose[v.p.id];if(!p)return v;const q={...v,_hf7Posed:true};
  if(p.x!=null){const dx=p.x-q.x,dy=p.y-q.y;q.x+=dx;q.y+=dy;if(q.ax!=null){q.ax+=dx;q.ay+=dy;}}
  q.rot=(q.rot||0)+(p.rot||0);if(q.ax!=null){const dx=(.5-q.spec.px)*q.w,dy=(.5-q.spec.py)*q.h;q.ax=q.x-dx*Math.cos(q.rot)+dy*Math.sin(q.rot);q.ay=q.y-dx*Math.sin(q.rot)-dy*Math.cos(q.rot);}q.alpha=1;return q;});}
fmcRig=function(b){return hf7PoseApply(b,hf7AuthoredRig(b));};
aa5GhostRig=function(b){return hf7PoseApply(b,HF7.base.ghost.apply(this,arguments));};
r30Parts=function(b){return hf7PoseApply(b,HF7.base.parts.apply(this,arguments));};
function hf7PhysicalPose(b,Q){const {K,u}=Q,kind=K.def.kind;K.pose={};
 const attack=clamp(u/K.active,0,1),reach=u<0?-.12*Math.sin(clamp(K.t/K.tell,0,1)*Math.PI):u<K.active?Math.sin(Math.min(1,attack*1.7)*Math.PI/2):Math.max(0,1-(u-K.active)/K.recover);
 if(['arms','gate','pincer'].includes(kind))for(const L of K.lines){if(!hf7Alive(b,L.module))continue;
  const dx=(L.ex-L.x)*reach,dy=(L.ey-L.y)*reach;K.pose[L.module]={x:L.cx+dx,y:L.cy+dy};}
 if(kind==='riposte'){const k=u<0?0:u<K.active?clamp(u/.65,0,1):1-clamp((u-K.active)/K.recover,0,1);
  b.x=lerp(K.origin.x,K.tx+35,k);b.y=lerp(K.origin.y,K.ty-85,k)-(u<K.active?Math.sin(k*Math.PI)*90:0);}
 if(kind==='bellows')for(const p of K.ports)K.pose[p.module]={x:p.cx,y:p.cy-24*Math.min(1,K.t/K.tell),rot:(p.x<b.x?-1:1)*-.2};
 if(kind==='press')for(const p of K.ports)if(p.module.startsWith('fan'))K.pose[p.module]={x:p.cx+(p.x<b.x?-1:1)*25*Math.min(1,K.t/K.tell),y:p.cy};
 if(kind==='rail')for(const p of K.ports)K.pose[p.module]={x:p.cx,y:p.cy};
 if(kind==='pass'){const left=camLeftX()-120,right=camRightX()+120,y=K.ty-100;
  if(u<0){const k=clamp(K.t/K.tell,0,1);b.x=lerp(K.origin.x,left,k);b.y=lerp(K.origin.y,y,k);}else if(u<K.active){b.x=lerp(left,right,attack);b.y=y;}else{const k=clamp((u-K.active)/K.recover,0,1);b.x=lerp(right,K.origin.x,k);b.y=lerp(y,K.origin.y,k);}}
 if(kind==='vault'){const k=u<0?0:u<K.active?attack:1-clamp((u-K.active)/K.recover,0,1);b.x=lerp(K.origin.x,K.tx,k);b.y=lerp(K.origin.y,K.ty-80,k)-Math.sin(k*Math.PI)*170;}
}
function hf7Tick(b,dt){const H=hf7State(b),K=H.sig;if(!K)return;K.t+=dt;j3Timers(b,dt);b.enter=false;
 let Q=hf7Sample(b);hf7PhysicalPose(b,Q);Q=hf7Sample(b);K.phase=Q.phase;
 if(!K.lines.some(L=>hf7Alive(b,L.module))){hf7Finish(b,'disarmed');return;}
 if(Q.phase==='tell')combatWarningTick(b,'hf7-'+K.id+'-'+K.n+'-'+Q.beat,Q.progress*(Q.beat?1.4:K.tell),Q.beat?1.4:K.tell);
 if(Q.phase==='live'){
  if(K.lastRelease!==Q.beat){K.lastRelease=Q.beat;r30Sound('combatBeam0927');hf7Log(b,'release',{name:K.def.name,beat:Q.beat});}
  if(Q.lines[0]?.physical){
   if(K.def.kind==='pass'){const L={x:b.x-65,y:b.y,ex:b.x+65,ey:b.y,width:90};hc1007Hit(L,'sonic broadside');}
   else if(K.def.kind==='vault'){if(Q.u>K.active*.75)for(const p of hf7Rig(b).filter(v=>K.ports.some(p=>p.module===v.p.id)))hc1007Hit({x:p.x,y:p.y+p.h*.30,ex:p.x,ey:p.y+p.h*.42,width:50},'Warden claw landing');}
   else if(K.def.kind==='riposte'){const L=fmcBlade(b);if(L)hc1007Hit(L,'Knight sword riposte');}
   else for(const L of Q.lines){const v=r30Parts(b).find(v=>v.p.id===L.module);if(!v)continue;let tip={x:v.x-Math.sin(v.rot||0)*v.h*.35,y:v.y+Math.cos(v.rot||0)*v.h*.35};
    const prev=K.previous?.[L.module]||tip;hc1007Hit({x:prev.x,y:prev.y,ex:tip.x,ey:tip.y,width:L.width},K.def.name);(K.previous??={})[L.module]=tip;}
  }else for(const L of Q.lines)hc1007Hit(L,K.def.name);
 }
 if(K.t>=K.tell+K.active+K.recover){hf7Finish(b,'recovered');return;}j3Save(b);
}
function hf7Finish(b,reason){const H=hf7State(b),K=H.sig;if(!K)return;b.x=K.origin.x;b.y=K.origin.y;H.sig=null;H.cd=hc1007Rank()<0?12:hc1007Rank()>0?8.5:10;
 const J=j3State(b),D=J.gp4Donors?.[J.mimic];if(D){D.p.x=b.x;D.p.y=b.y;D.aa5Cd=999;}b._r30.cd=Math.max(b._r30.cd||0,.65);hf7Log(b,reason,{name:K.def.name});j3Save(b);}
r30Tick=function(b,dt){const id=hf7Identity(b),S=b?._r30;if(id==null||!S||S.mode!=='fight'||b.dead||b.hp<=0){if(S?.hf7?.sig)hf7Cancel(b,'not fighting');return HF7.base.tick.apply(this,arguments);}
 dt=Math.min(.05,Math.max(0,dt));let H=S.hf7;if(!H||H.id!==id)H=S.hf7={id,cd:id==='1'?.35:3.2,n:0,sig:null};
 // Replace the generic extra donor spread overlay with a source-specific move.
 // Native source attacks are never removed or artificially sped up.
 const J=j3State(b),D=J.gp4Donors?.[J.mimic];if(D&&J.mimic!==8){D.aa5Salvo=null;D.aa5Cd=999;}
 if(H.sig)return hf7Tick(b,dt);H.cd-=dt;
 if(H.cd<=0&&hf7Between(b)&&hf7Start(b))return hf7Tick(b,dt);
 return HF7.base.tick.apply(this,arguments);
};
r30DrawBoss=function(b){const r=HF7.base.draw.apply(this,arguments),Q=hf7Sample(b);if(!Q||b._r30.mode!=='fight')return r;const {K}=Q;
 if(Q.phase==='tell'){for(const L of Q.lines)hc1007Warn(b,L,Q.progress);if(Q.lines[0])hc1007Warn(b,Q.lines[0],Q.progress,true);}
 else if(['live','dissolve'].includes(Q.phase))for(const L of Q.lines)if(!L.physical){av3Beam(ctx,L.x,L.y,L.a,Math.hypot(L.ex-L.x,L.ey-L.y),L.width,L.color,b.t,Q.alpha,true);HF7.draws++;}
 return r;
};
modularHit=function(){const b=boss,r=HF7.base.hit.apply(this,arguments);if(b&&hf7State(b)?.sig){const K=hf7State(b).sig;if(K&&!K.lines.some(L=>hf7Alive(b,L.module)))hf7Finish(b,'disarmed');}return r;};
j3Clear=function(b){hf7Cancel(b);return HF7.base.clear.apply(this,arguments);};
j3Mimic=function(b){hf7Cancel(b,'form changed');if(b?._r30)b._r30.hf7=null;return HF7.base.mimic.apply(this,arguments);};
j3Encounter=function(b){hf7Cancel(b,'encounter changed');if(b?._r30)b._r30.hf7=null;return HF7.base.encounter.apply(this,arguments);};
