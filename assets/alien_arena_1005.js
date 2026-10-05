"use strict";
/* Authored void / code layers live below combat. Animation clocks belong to
   simulation, never draw calls, so pause and hit-stop cannot accelerate reels. */
const AA5={draws:{},events:[]};
const AA5_BASE={bg:drawBG,world:drawWorld,tick:r30Tick,encounter:j3Encounter,mimic:j3Mimic,
 warm:r30Warm,intro:on5IntroDraw,parts:r30Parts,body:j3Body,hit:modularHit,
 attack:r30Attack,attackTick:r30AttackTick,pose:r30Pose};
const AA5_DRAW_BOSS=r30DrawBoss;
for(const cells of Object.values(AA5_ART))for(const a of cells)XART._src[a.key]=a.path;
function aa5Warm(){for(const cells of Object.values(AA5_ART))for(const a of cells)XART.rdy(a.key);}
r30Warm=function(){const r=AA5_BASE.warm.apply(this,arguments);aa5Warm();return r;};
function aa5Cell(name,f,x,y,w,h=w,rot=0,alpha=1){const cells=AA5_ART[name],a=cells[((f|0)%cells.length+cells.length)%cells.length];
 if(!XART.rdy(a.key))return false;ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(rot);ctx.globalAlpha*=alpha;
 ctx.drawImage(XART.get(a.key),-w/2,-h/2,w,h);ctx.restore();AA5.draws[name]=(AA5.draws[name]||0)+1;return true;}
function aa5Arena(b){const J=j3State(b);return run.stage===8&&J?.encounter===2&&!b.dead&&!['escape','reunion','done'].includes(b._r30.mode);}
function aa5VoidFrame(t){return 9+Math.floor(t*8)%3;}
function aa5ArenaDraw(b){
 const J=j3State(b),S=b._r30,t=J.aa5Clock||0,fade=S.mode==='voidIntro1005'?clamp((S.t-1.4)/1.6,0,1):1;
 const left=camLeftX(),top=viewTopY(),w=viewW(),h=viewH(),cx=left+w/2,cy=top+h/2;
 ctx.save();ctx.beginPath();ctx.rect(left-12,top-12,w+24,h+24);ctx.clip();ctx.globalAlpha*=fade;
 // Opaque whole authored backdrop is the clear; no sky or preceding frames can
 // leak through its black central corridor at either supported camera zoom.
 aa5Cell('back',0,cx+Math.sin(t*.17)*4,cy+Math.sin(t*.13)*6,w+40,h+50);
 aa5Cell('void',aa5VoidFrame(t),cx+Math.sin(t*.21)*7,top+h*.49,w*1.10,w*1.10,t*.055,.12);
 for(let i=0;i<8;i++){
  const side=i%2?-1:1,row=Math.floor(i/2),x=cx+side*w*(row%2?.39:.32);
  aa5Cell('code',Math.floor(t*9)+i*3,x+Math.sin(t*.4+i)*3,top+h*(.05+row*.27)+Math.sin(t*.3+i)*9,
    w*(row%2?.16:.20),h*.39,0,row%2?.65:.42);
 }
 // Near ribs have independent larger motion; the alpha center preserves the
 // dark vortex instead of covering it with a second opaque illustration.
 aa5Cell('front',0,cx+Math.sin(t*.31)*8,cy+Math.sin(t*.23)*14,w+42,h+72,0,.72);
 ctx.restore();J.aa5ArenaDrawn=true;
}
drawBG=function(dt){const r=AA5_BASE.bg.apply(this,arguments);if(aa5Arena(boss))aa5ArenaDraw(boss);return r;};
j3Encounter=function(b,n){const r=AA5_BASE.encounter.apply(this,arguments),J=j3State(b);if(!J)return r;
 J.aa5Clock??=0;aa5Warm();if(n===1)aa5GhostBuild(b);return r;};
j3Mimic=function(b,i){const r=AA5_BASE.mimic.apply(this,arguments);const J=j3State(b);if(J){aa5Warm();const D=J.gp4Donors?.[i];if(D){D.aa5Visit=0;D.aa5Cd=6;D.aa5Salvo=null;}}return r;};
r30Tick=function(b,dt){const J=j3State(b);if(J)J.aa5Clock=(J.aa5Clock||0)+Math.min(.05,Math.max(0,dt||0));
 if(cf4Dracula(b)&&b._r30.mode==='fight')return aa5DraculaTick(b,Math.min(.05,Math.max(0,dt||0)));
 const r=AA5_BASE.tick.apply(this,arguments);
 if(J?.encounter===1&&b._r30.mode==='fight'&&!b._r30.aa5Unbound&&b.hp<=b.maxhp*.5&&['hard','furious','insanity'].includes(diffKey)){
  b._r30.aa5Unbound=true;r30Sound('bossPhase');j3Log(b,'ghostUnbound',{cannon:true});
 }return r;};
on5IntroDraw=function(b){const S=b._r30,t=S.t;if(S.mode==='voidIntro1005'){
 on5OrbitBits(b,t,false,290);aa5Cell('void',t<3.3?Math.min(11,Math.floor(t*3.6)):aa5VoidFrame(t),b.x,b.y,440,440,t*.08,.95);
 if(t>=3.9){const k=clamp((t-3.9)/.8,0,1);ctx.save();ctx.translate(b.x,b.y);ctx.scale(.25+.75*k,.25+.75*k);ctx.translate(-b.x,-b.y);j3Body(b,1);ctx.restore();}
 on5OrbitBits(b,t,true,290);return;
 }
 if(S.mode==='takeover'){
 // Entity is visibly BEHIND the normal drone. Tendrils close around it, the
 // drone disappears at the consumed beat, and the mutated host emerges whole.
 on5OrbitBits(b,t,false,215);aa5Cell('void',Math.min(7,Math.floor(t*2.3)),b.x,b.y-18,340,360,0,1);
 if(t<2.2)r30Blit('vile24_robot_gray',b.x,b.y,230,230,0,1);
 if(t>=2.65)j3Body(b,1);on5OrbitBits(b,t,true,215);return;
 }return AA5_BASE.intro.apply(this,arguments);
};
drawWorld=function(dt){const r=AA5_BASE.world.apply(this,arguments),b=boss,S=b?._r30;
 if(S?.mode==='voidIntro1005'&&S.t<3.5){const t=S.t,alpha=t<2.2?clamp((t-.35)/1.3,0,1):clamp((3.5-t)/1.3,0,1);
  ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=alpha;ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);
  const size=Math.max(VW,VH)*(.35+clamp(t/2.2,0,1)*2.4);
  aa5Cell('void',Math.min(11,Math.floor(t*4)),VW/2,VH*.42,size,size,t*.12,1);ctx.restore();
 }return r;};
function aa5Ghost(b){return j3State(b)?.encounter===1;}
function aa5GhostBuild(b){
 const hp=b.hp,defs=[['core',1],['armL',.13],['armR',.13],['clawL',.09],['clawR',.09],['tail',.11],['eye',.10],['cannon',.12]];
 b.parts=defs.map(([id,f])=>({id,dmg:true,hp:Math.ceil(hp*f),maxhp:Math.ceil(hp*f),destroyed:false,flash:0,kick:0}));
 b.w=340;b.h=320;b._r30.aa5Unbound=false;b._r30.aa5Ghost=true;b._r30.aa5Collapsed=false;
}
function aa5GhostRig(b){const Q=r30Pose(b),S=b._r30,P=S.attack,t=S.clock||0,u=P?clamp((P.t-P.tell)/(P.active||1),0,1):0;
 if(S.aa5Collapsed)return[];
 const out=[],nodes={},alive=id=>b.parts.find(p=>p.id===id&&!p.destroyed);
 function node(id,f,ax,ay,w,h,rot=0,z=0){const p=alive(id);if(!p)return null;const key=AA5_ART.ghost[f].key;
  const v={p,key,x:ax,y:ay,w,h,rot,alpha:1,z,spec:{role:id.includes('claw')?'claw':'ghost'}};out.push(v);nodes[id]=v;return v;}
 node('tail',2,Q.x,Q.y+104,76,142,Math.sin(t*2)*.13,-3);
 node('core',0,Q.x,Q.y+8,156,178,Math.sin(t)*.025,0);
 node('core',1,Q.x,Q.y-101,142,172,Math.sin(t*1.5)*.035,3);
 for(const side of [-1,1]){const id=side<0?'L':'R';let rot=-side*(.15+Math.sin(t*2+side)*.12);
  if(P?.type==='ghostPinch')rot+=side*Math.sin(u*Math.PI)*.90;
  if(P?.type==='ghostCross')rot+=side*Math.sin(u*Math.PI*2)*.72;
  const ax=Q.x+side*72,ay=Q.y-17,aw=65,ah=132,cx=ax-Math.sin(rot)*ah*.35,cy=ay+Math.cos(rot)*ah*.35;
  const arm=node('arm'+id,side<0?3:4,cx,cy,aw,ah,rot,1);
  if(arm)node('claw'+id,side<0?5:6,cx-Math.sin(rot)*ah*.56,cy+Math.cos(rot)*ah*.56,84,112,rot,2);
 }
 const radius=S.aa5Unbound?154:128;
 node('eye',7,Q.x+Math.cos(t*1.45)*radius,Q.y+Math.sin(t*1.45)*radius*.37,56,59,t*.22,Math.sin(t*1.45)>0?5:-4);
 node('cannon',8,Q.x,Q.y+(S.aa5Unbound?84:48),S.aa5Unbound?52:38,S.aa5Unbound?110:72,0,4);
 return out.sort((a,b)=>a.z-b.z);
}
r30Parts=function(b){return aa5Ghost(b)?aa5GhostRig(b):AA5_BASE.parts.apply(this,arguments);};
j3Body=function(b,alpha=1){if(!aa5Ghost(b))return AA5_BASE.body.apply(this,arguments);
 if(b._r30.aa5Collapsed)return;
 for(const v of aa5GhostRig(b)){r30Blit(v.key,v.x,v.y,v.w,v.h,v.rot,alpha);
  if(Math.max(v.p.flash||0,b.flash||0)>0)fmcWhiteBlit(v.key,v.x,v.y,v.w,v.h,v.rot,Math.min(1,Math.max(v.p.flash||0,b.flash||0)*10)*alpha);}
};
// The live fight renderer's original ghost body also goes through r30Parts;
// j3Body above is the intro path. All projectiles and Retina use that same rig.
modularHit=function(dmg){const b=boss;if(!aa5Ghost(b))return AA5_BASE.hit.apply(this,arguments);
 const before=aa5GhostRig(b),dead=new Set(b.parts.filter(p=>p.destroyed));const r=AA5_BASE.hit.apply(this,arguments);
 for(const p of b.parts)if(p.destroyed&&!dead.has(p)){
  const list=[p];if(p.id==='armL'||p.id==='armR'){const c=b.parts.find(q=>q.id==='claw'+p.id.slice(-1));if(c&&!c.destroyed){c.destroyed=true;c.hp=0;list.push(c);}}
  for(const q of list){const v=before.find(v=>v.p===q);if(v)d27ModuleRupture(b,q,{...v,debrisImage:XART.get(v.key)},'purple');}
 }return r;};
const AA5_EXTRA=new Set(['ghostPinch','ghostCross','ghostWarp','ghostRail','hostCross','hostRoll']);
r30Attack=function(b){const J=j3State(b),S=b?._r30;
 if(!J||J.encounter>=2)return AA5_BASE.attack.apply(this,arguments);
 const extra=J.encounter===1?['ghostPinch','ghostCross','ghostWarp','ghostRail']:['hostCross','hostRoll'];
 const cycle=S.seq%(4+extra.length);if(cycle<4){const r=AA5_BASE.attack.apply(this,arguments);
  if(aa5Ghost(b)&&S.attack?.type==='ghostLance'){
   const P=S.attack;P.lanes=aa5GhostRig(b).filter(v=>v.p.id.startsWith('claw')).map(v=>({...s81003Lane(v.x,v.y+v.h*.35,P.tx,P.ty,16),tx:P.tx,ty:P.ty,module:v.p.id}));
   if(!P.lanes.length&&b.parts.some(p=>p.id==='cannon'&&!p.destroyed))P.lanes=[{...s81003Lane(b.x,b.y+100,P.tx,P.ty,18),tx:P.tx,ty:P.ty,module:'cannon'}];
  }return r;}
 const type=extra[cycle-4];S.seq++;S.attack={aa5:true,on5:true,type,t:0,tell:diffKey==='easy'?1.5:1.05,active:type==='ghostWarp'?2.7:type==='hostRoll'?1.9:2.6,
  tx:clamp(player.x,camLeftX()+65,camRightX()-65),ty:clamp(player.y,250,VH-70),fromX:b.x,fromY:b.y,next:0,step:0,lanes:[]};
 const P=S.attack;if(type==='ghostRail')P.lanes=[{...s81003Lane(b.x,b.y+112,P.tx,P.ty,19),tx:P.tx,ty:P.ty,module:'cannon'}];
 if(type==='hostCross')P.lanes=[-1,1].map(s=>({...s81003Lane(b.x+s*80,b.y+45,P.tx-s*90,P.ty,16),tx:P.tx-s*90,ty:P.ty}));
 r30Sound('bossWeaponCharge');j3Log(b,'attack',{type});
};
r30Pose=function(b){const P=b?._r30?.attack;if(!P?.aa5)return AA5_BASE.pose.apply(this,arguments);
 const u=clamp((P.t-P.tell)/P.active,0,1),roll=P.type==='hostRoll',warp=P.type==='ghostWarp',dash=roll?Math.sin(u*Math.PI):0;
 return{x:warp&&u>.28?P.tx:lerp(b.x,P.tx,dash),y:warp&&u>.28?Math.max(155,P.ty-180):lerp(b.y,P.ty-45,dash),
  angle:roll?u*TAU*2:0,alpha:1,scale:1,shape:aa5Ghost(b)?'ghost':'host'};};
r30AttackTick=function(b,dt){const S=b._r30,P=S.attack;if(!P?.aa5)return AA5_BASE.attackTick.apply(this,arguments);
 P.t+=dt;const u=P.t-P.tell;combatWarningTick(b,'aa5-'+S.seq,Math.min(P.t,P.tell),P.tell);if(u<0)return;
 const Q=r30Pose(b);
 if(P.type==='ghostRail'||P.type==='hostCross'){
  if(!P.step){P.step++;if(P.type!=='ghostRail'||b.parts.some(p=>p.id==='cannon'&&!p.destroyed))for(const L of P.lanes)s81003Beam(b,L,'code',1.05);r30Sound('combatBeam0927');}
 }else if(u>=P.next){P.next=u+(P.type==='ghostWarp'?.8:.60);P.step++;
  const claws=aa5Ghost(b)?aa5GhostRig(b).filter(v=>v.p.id.startsWith('claw')):[{x:Q.x-65,y:Q.y+60},{x:Q.x+65,y:Q.y+60}];
  for(const v of claws){const a=Math.atan2(P.ty-v.y,P.tx-v.x);for(const off of [-.16,.16])f1003bShot(b,v.x,v.y,a+off,4.2,'code');}
  if(S.aa5Unbound&&P.step%2===0){const eye=aa5GhostRig(b).find(v=>v.p.id==='eye');if(eye)for(const off of [-.34,0,.34])f1003bShot(b,eye.x,eye.y,Math.atan2(P.ty-eye.y,P.tx-eye.x)+off,3.4,'code');}
  r30Sound('enemyBossCannon');
 }
 if(['ghostPinch','ghostCross','hostRoll'].includes(P.type)){
  const shapes=aa5Ghost(b)?aa5GhostRig(b).filter(v=>v.p.id.startsWith('claw')).map(v=>({x:v.x-Math.sin(v.rot)*v.h*.32,y:v.y+Math.cos(v.rot)*v.h*.32})): [Q];
  for(const v of shapes)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-v.x,player.y-v.y)<(aa5Ghost(b)?32:55))playerHit('symbiote committed strike');});
 }
 if(u>=P.active){S.attack=null;S.cd=diffKey==='easy'?1.3:.95;}
};
r30DrawBoss=function(b){const S=b?._r30,P=S?.attack;
 if(j3State(b)?.encounter===2&&['transform1003j','reveal1003j'].includes(S.mode)){
  on5OrbitBits(b,S.t,false,245);j3Body(b,1);aa5Cell('void',S.mode==='transform1003j'?Math.min(8,Math.floor(S.t*7)):aa5VoidFrame(S.t),b.x,b.y,355,355,S.t*.12,.9);
  on5OrbitBits(b,S.t,true,245);return;
 }
 if(aa5Ghost(b)&&S.mode==='fight'){
  j3Body(b,1);
  if(P&&P.t<P.tell){for(const L of P.lanes||[])s81003Fov(L,P.t/P.tell,true);
   if(!P.lanes?.length){groundTargetReticleDraw(P.tx,P.ty,90,P.t/P.tell,.8);
    for(const v of aa5GhostRig(b).filter(v=>v.p.id.startsWith('claw')))combatWarningDraw(b,{x:v.x,y:v.y,ex:P.tx,ey:P.ty,width:35,progress:P.t/P.tell,fieldOnly:true});}}
  if(P?.type==='ghostWarp')aa5Cell('void',aa5VoidFrame(S.clock),P.tx,Math.max(155,P.ty-180),160,160,S.clock*.3,1);
  return;
 }
 const r=AA5_DRAW_BOSS.apply(this,arguments);
 if(cf4Dracula(b)&&S.mode==='fight'&&P?.aa5Court){
  for(const L of P.voidPorts||[]){aa5Cell('void',aa5VoidFrame(S.clock),L.x,L.y,130,130,S.clock*.16,.9);
   if(P.t<P.tell)combatWarningDraw(b,{...L,ex:P.tx,ey:P.ty,width:34,progress:P.t/P.tell,fieldOnly:true});}
  if(P.aa5Dive&&P.t<P.tell)combatWarningDraw(b,{x:P.fromX,y:P.fromY,ex:P.tx,ey:P.ty,width:150,progress:P.t/P.tell,fieldOnly:true});
 }
 const D=j3State(b)?.gp4Donors?.[j3State(b)?.mimic],V=D?.aa5Salvo;
 if(V&&V.t<V.tell)for(const L of V.lanes)combatWarningDraw(b,{...L,progress:V.t/V.tell,fieldOnly:true});
 if(P?.type==='hostRoll'&&P.t<P.tell)combatWarningDraw(b,{x:P.fromX,y:P.fromY,ex:P.tx,ey:P.ty,width:98,progress:P.t/P.tell,fieldOnly:true});return r;
};
const AA5_BREAK=r30Break;
r30Break=function(b){if(aa5Ghost(b)&&b._r30.mode==='fight'&&!b._r30.aa5Collapsed){
 const rig=aa5GhostRig(b);b._r30.aa5Collapsed=true;
 for(const v of rig)d27ModuleRupture(b,{...v.p,_d27Ruptured:false},{...v,debrisImage:XART.get(v.key)},'purple');
 }return AA5_BREAK.apply(this,arguments);};
const AA5_TARGETS=retinaBossTargets;
retinaBossTargets=function(b){if(!aa5Ghost(b))return AA5_TARGETS.apply(this,arguments);if(!r30Live(b)||b._noHit)return[];
 return aa5GhostRig(b).map((v,i)=>retinaDynamicPiece(b,'aa5-ghost-'+v.p.id+'-'+i,'spectral module',()=>{
  const live=aa5GhostRig(b).find(q=>q.key===v.key&&q.p===v.p);return{x:live?.x??v.x,y:live?.y??v.y,hp:live?v.p.hp:0,dead:!r30Live(b)||!live||v.p.destroyed};},
  dmg=>{b._lastPart=v.p;hitBoss(dmg);},v.w*.80,v.h*.80));
};
const AA5_SHOT=f1003bShot;
f1003bShot=function(b,x,y){if(!aa5Ghost(b))return AA5_SHOT.apply(this,arguments);
 const args=Array.from(arguments),type=b._r30.attack?.type||'',rig=aa5GhostRig(b);
 let ports=rig.filter(v=>v.p.id.startsWith('claw'));
 if(type.includes('Orbit'))ports=rig.filter(v=>['eye','core'].includes(v.p.id));
 if(type==='ghostRail'||type==='ghostWarp')ports=rig.filter(v=>v.p.id==='cannon');
 if(!ports.length)return{dead:true,x,y};
 const nearest=ports.sort((a,b)=>Math.hypot(a.x-x,a.y-y)-Math.hypot(b.x-x,b.y-y))[0];
 args[1]=nearest.x;args[2]=nearest.y+nearest.h*(nearest.p.id.startsWith('claw')?.36:.25);
 const q=AA5_SHOT.apply(this,args);if(q)q._fmcModule=nearest.p.id;return q;
};
const AA5_DONOR=gd4Tick;
function aa5DonorPorts(b){const rig=fmcRig(b),guns=rig.filter(v=>v.p.id!=='core'&&(v.spec.tags?.length||/gun|claw|rack|fan|left|right/.test(v.p.id)));
 const source=guns.length?guns.slice(0,2):rig.filter(v=>v.p.id==='core').slice(0,1);
 return source.map(v=>{const p=fmcPoint(v,...(v.spec.emit||[.5,.80]));return{...p,module:v.p.id};});
}
gd4Tick=function(b,dt){const J=j3State(b);if(!J||!(J.mimic>0))return AA5_DONOR.apply(this,arguments);
 const D=gd4Create(b,J.mimic),hard=['hard','furious','insanity'].includes(diffKey),furious=['furious','insanity'].includes(diffKey);
 D.aa5Visit=(D.aa5Visit||0)+dt;
 // Furious gets more time with each real campaign controller. Health and
 // destroyed equipment still persist; this never allocates another life.
 if(furious)D.age=Math.min(D.age,31.7);
 if(hard)D.alien=Math.max(D.alien,2);
 const r=AA5_DONOR.call(this,b,dt*(furious?1.08:1));if(b._r30.mode!=='fight')return r;
 if(furious&&D.aa5Visit>=40){D.aa5Visit=0;j3Morph(b,'home');return r;}
 if(!hard||D.i===5)return r;D.aa5Cd=(D.aa5Cd??6)-dt;
 const busy=D.p._l23Beam||D.p._whv?.beam||D.p._whv?.beam2||D.p._whv?.ace?.dash||D.p._whv?.ace?.desp&&D.p._whv.ace.desp.st!=='done';
 if(!D.aa5Salvo&&D.aa5Cd<=0&&!busy){
  const ports=aa5DonorPorts(b),tx=clamp(player.x,camLeftX()+55,camRightX()-55),ty=player.y;
  D.aa5Salvo={t:0,tell:1.15,next:1.15,n:0,tx,ty,lanes:ports.map(p=>({...p,ex:tx,ey:ty,width:D.i===6?24:38}))};
  r30Sound('bossWeaponCharge');j3Log(b,'donorUpgrade',{source:D.i});
 }
 const V=D.aa5Salvo;if(!V)return r;V.t+=dt;combatWarningTick(b,'aa5-donor-'+D.i,Math.min(V.t,V.tell),V.tell);
 if(V.t>=V.next&&V.n<2){V.next+=.42;V.n++;
  const ports=aa5DonorPorts(b);
  for(const m of ports){const a=Math.atan2(V.ty-m.y,V.tx-m.x),kind=D.i===2?'fire':D.i===3?'ice':D.i===6?'missile':'code';
   const offsets=D.i===6?[-.18,.18]:D.i===1?[-.14,0,.14]:D.i===7?[-.32,-.16,.16,.32]:[-.20,.20];
   for(const off of offsets){const q=f1003bShot(b,m.x,m.y,a+off,D.i===6?3.1:3.6,kind,D.i===2||D.i===3);
    if(q&&kind==='ice'){q.hp=4;q._shootable=true;q._energyOrdnance=true;q.spd=3.6;}}
  }r30Sound('enemyBossCannon');
 }
 if(V.t>=V.tell+1.0){D.aa5Salvo=null;D.aa5Cd=furious?8.5:10;}
 return r;
};
function aa5DraculaTick(b,dt){
 const S=b._r30,J=j3State(b);j3Timers(b,dt);b.enter=false;
 const hard=['hard','furious','insanity'].includes(diffKey),book=['cf4Sweep','cf4Crush','cf4Court','aa5Void'];if(hard)book.push('aa5Dive');
 b.x=camLeftX()+viewW()/2+Math.sin(S.clock*.62)*34;b.y=PLAY.y+156+Math.sin(S.clock*.93)*15;
 if(!S.attack){S.cd-=dt;if(S.cd>0){on5ShieldTick(b,dt);return;}
  if(J.attacks>=book.length){j3Morph(b,J.active);return;}
  const kind=book[J.attacks++];S.seq++;
  S.attack={type:kind==='aa5Dive'?'cf4Crush':kind,aa5Court:true,aa5Dive:kind==='aa5Dive',t:0,tell:diffKey==='easy'?1.5:1.05,
   active:kind==='cf4Sweep'?3.1:kind==='cf4Court'?3.2:kind==='aa5Void'?3.0:2.6,next:0,tx:clamp(player.x,camLeftX()+60,camRightX()-60),
   ty:clamp(player.y,PLAY.y+240,VH-65),fromX:b.x,fromY:b.y,voidPorts:[]};
  if(kind==='aa5Void')S.attack.voidPorts=[.23,.77].map(f=>({x:camLeftX()+viewW()*f,y:PLAY.y+175}));
  r30Sound('bossWeaponCharge');j3Log(b,'draculaPattern',{type:kind});
 }
 const P=S.attack;P.t+=dt;const u=P.t-P.tell;combatWarningTick(b,'aa5-dracula-'+S.seq,Math.min(P.t,P.tell),P.tell);
 if(u<0)return;
 if(P.aa5Dive){const k=Math.sin(clamp(u/P.active,0,1)*Math.PI);b.x=lerp(P.fromX,P.tx,k);b.y=lerp(P.fromY,P.ty-115,k);}
 if(P.type!=='aa5Void'&&P.type!=='cf4Court')for(const v of r30Parts(b).filter(v=>v.p.id!=='core')){
  const tip=cf4Claw(v);for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-tip.x,player.y-tip.y)<31)playerHit('colossus sweeping talon');});}
 if(u>=P.next){P.next=u+(P.type==='cf4Court'?.48:P.type==='aa5Void'?.70:.95);
  let ports=P.type==='aa5Void'?P.voidPorts:P.type==='cf4Court'?r30Parts(b).filter(v=>v.p.id!=='core').map(cf4Claw):[{x:b.x,y:b.y+100}];
  if(!ports.length)ports=[{x:b.x,y:b.y+100}];
  for(const v of ports){const a=Math.atan2(P.ty-v.y,P.tx-v.x),offsets=P.type==='aa5Void'?[-.36,-.18,.18,.36]:P.type==='cf4Court'?[-.27,-.13,.13,.27]:[-.22,0,.22];
   for(const off of offsets)f1003bShot(b,v.x,v.y,a+off,P.type==='aa5Void'?3.8:3.5,'code',true);}
  r30Sound('combatAlien0927');
 }
 if(P.type==='cf4Court')for(const seat of seatList())withSeat(seat,()=>{if(!player.dead){const a=Math.atan2(b.y-player.y,b.x-player.x);
  player.x=clamp(player.x+Math.cos(a+.65)*dt*23,camLeftX()+20,camRightX()-20);player.y=clamp(player.y+Math.sin(a+.65)*dt*15,PLAY.y+20,VH-35);}});
 if(u>=P.active){S.attack=null;S.cd=diffKey==='easy'?1.2:.75;}on5ShieldTick(b,dt);j3Save(b);
}
