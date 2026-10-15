"use strict";
/* Recording 50:30–58:54. Continuous reformation, physical lock identities,
   committed emitter charges and a finite, damageable download barrier. */
const PT11F={base:{encounter:j3Encounter,tick:r30Tick,draw:r30DrawBoss,intro:on5IntroDraw,
 attack:r30Attack,attackTick:r30AttackTick,parts:r30Parts,targets:retinaBossTargets,
 bounds:r30ShieldBounds,wall:s81003ShieldDraw,at:r30At,image:cwdImage},ghostPaint:false};
function pt11HeartFrame(t){return t<2.0?Math.min(7,Math.floor(t*4)):8+Math.floor((t-2)*12)%8;}
function pt11HeartDraw(b,t,k=1){
 // Authored black fragments rise from below before joining the registered heart.
 for(let i=0;i<12;i++){
  const u=clamp((t-i*.065)/2.1,0,1);if(u>=1)continue;
  const side=i%2?-1:1,x=lerp(b.x+side*(85+i%4*29),b.x,u),y=lerp(viewTopY()+viewH()+40+i*18,b.y+32,u);
  on5Cell('fragments',i%24,x,y,(26+i%3*7)*k,(26+i%3*7)*k,(1-u)*side*.8);
 }
 pt11Plate('black_heart',pt11HeartFrame(t),b.x,b.y,k);
}
function pt11FallDraw(b){const S=b._r30,D=dr5State(b),t=S.t;if(t>=2.8)return;
 const u=clamp(t/1.8,0,1),rot=u*TAU*2,y=u*u*125;
 ctx.save();ctx.translate(b.x,b.y+y);ctx.rotate(rot);ctx.translate(-b.x,-b.y);
 for(const v of D.fallRig||[])r30Blit(v.key,v.x,v.y,v.w,v.h,v.rot,1);ctx.restore();
}
function pt11ReformDraw(b){const S=b._r30,J=j3State(b);
 if(J.encounter===0){pt11HeartDraw(b,S.t,1.08);return;}
 const Q=J.pt11Portal??={x:b.x,y:b.y,t:0,size:340};
 ap10VoidCell(ap10VoidFrame(S.t<.65?'open':'loop',Q.t),Q.x,Q.y,Q.size,Q.size,Q.t*.13);
}
j3Encounter=function(b,n){const J=j3State(b),oldMode=b?._r30?.mode,oldT=b?._r30?.t||0,portal=J?.pt11Portal;
 const r=PT11F.base.encounter.apply(this,arguments);if(!J)return r;
 if(n<2){const boost=diffKey==='easy'?1.2:diffKey==='normal'?1.5:diffKey==='hard'?1.9:2.3;
  const hp=Math.ceil(b.maxhp*boost);j3Health(b,hp,hp);
  for(const p of b.parts)if(p.id!=='core'){p.hp=p.maxhp=Math.ceil(p.maxhp*boost);}
 }
 if(n===1)J.pt11HeartOffset=oldMode==='dr5Reform'?oldT:2;
 if(n===2&&oldMode==='dr5Reform'&&portal)J.pt11Portal={...portal,startT:portal.t};
 return r;
};
r30Tick=function(b,dt){const J=j3State(b),S=b?._r30,mode=S?.mode;
 if(J?.encounter===0&&mode==='takeover'){
  if(S.t>=1.05&&!S._pt11TakeoverLine){S._pt11TakeoverLine=true;dr5Say(b,run.pilot.toUpperCase(),'That thing behind the drone... it is consuming it!');}
  dr5TalkTick(b,dt);
  if(S.t>=5.2&&S._pt11TakeoverLine)dr5State(b).radio=null;
 }
 if(J?.pt11Portal&&['dr5Reform','voidIntro1005'].includes(mode))J.pt11Portal.t+=Math.min(.05,Math.max(0,dt));
 if(J?.encounter===0&&mode==='encounterFall1003j'&&S.t>=2.0&&!dr5State(b).pt11Ruptured){
  const D=dr5State(b);D.pt11Ruptured=true;
  for(const v of D.fallRig||[]){const key=REALM30_ART[v.key]?'r30_'+v.key:v.key;
   if(XART.rdy(key))d27ModuleRupture(b,{...v.p,_d27Ruptured:false},{...v,y:v.y+125,debrisImage:XART.get(key)},'purple');}
 }
 const r=PT11F.base.tick.apply(this,arguments);
 if(J?.encounter===1&&S.shield>0&&!b.parts.some(p=>p.id==='eye'&&!p.destroyed))on5ShieldHit(b,S.shield);
 if(J&&mode!=='dr5Reform'&&S.mode==='dr5Reform'&&J.encounter===1)J.pt11Portal={x:b.x,y:b.y,t:0,size:340};
 return r;
};
on5IntroDraw=function(b){const S=b._r30,J=j3State(b),t=S.t;
 if(S.mode==='takeover'&&pt11Ready('drone_raise')){
  const lift=clamp(t/1.7,0,1),y=b.y-18*lift;
  if(t>.75){const u=t-.75;aa5Cell('void',u<1.1?Math.min(7,Math.floor(u*7)):aa5VoidFrame(u),b.x,y-16,360,360,u*.07,1);}
  on5OrbitBits(b,t,false,215);
  if(t<3.35){ctx.save();ctx.globalAlpha=1-clamp((t-2.7)/.65,0,1);pt11Plate('drone_raise',Math.min(15,Math.floor(lift*15)),b.x,y,.98);ctx.restore();}
  if(t>1.9&&t<4.5)on5Cell('symbiote',Math.min(7,3+Math.floor((t-1.9)*2)),b.x,y,320,320);
  if(t>=3.55){const k=clamp((t-3.55)/1.15,0,1);ctx.save();ctx.translate(b.x,b.y);ctx.scale(.60+.40*k,.60+.40*k);ctx.translate(-b.x,-b.y);j3Body(b,k);ctx.restore();}
  on5OrbitBits(b,t,true,215);return;
 }
 if(S.mode==='ghostIntro1005'){
  const u=clamp((t-1.8)/1.5,0,1);
  if(t<3.3){ctx.save();ctx.globalAlpha=1-u;pt11HeartDraw(b,(J.pt11HeartOffset||2)+t,1.08);ctx.restore();}
  if(u>0){ctx.save();ctx.translate(b.x,b.y);ctx.scale(.64+.36*u,.64+.36*u);ctx.translate(-b.x,-b.y);j3Body(b,u);ctx.restore();}
  return;
 }
 if(S.mode==='voidIntro1005'&&J.pt11Portal){const Q=J.pt11Portal,u=clamp(t/2.1,0,1),ease=u*u*(3-2*u);
  const size=lerp(Q.size,Math.max(worldWidth(),viewH())*3.3,ease);
  if(t<2.6)ap10VoidCell(ap10VoidFrame('loop',Q.t*(1+t*.28)),Q.x,Q.y,size,size,Q.t*.13);
  const dark=t<2.1?clamp((t-.9)/1.0,0,1):clamp((3.7-t)/1.6,0,1);
  if(dark>0){ctx.save();ctx.globalAlpha=dark;ctx.fillStyle='#000';ctx.fillRect(-64,viewTopY()-64,worldWidth()+128,viewH()+128);ctx.restore();}
  if(t>=3.9){ctx.save();const k=.25+.75*clamp((t-3.9)/.8,0,1);ctx.translate(b.x,b.y);ctx.scale(k,k);ctx.translate(-b.x,-b.y);j3Body(b,1);ctx.restore();}
  return;
 }
 return PT11F.base.intro.apply(this,arguments);
};
function pt11GhostTargets(b){
 // Core appears in two plates. It is one pool and therefore one stable lock.
 const seen=new Set(),targets=[];
 for(const v of aa5GhostRig(b)){if(seen.has(v.p.id))continue;seen.add(v.p.id);
  const id=v.p.id,part=v.p,state=()=>{const live=aa5GhostRig(b).find(q=>q.p===part);
   return{x:live?.x??b.x,y:live?.y??b.y,hp:part.hp,dead:!r30Live(b)||b._noHit||!live||part.destroyed};};
  targets.push(retinaDynamicPiece(b,'pt11-ghost-'+id,'spectral module',state,dmg=>{
   const q=state();if(q.dead)return;b._lastPart=part;_lastHitX=q.x;_lastHitY=q.y;
   if(b._r30.shield>0&&cwdContains(r30ShieldBounds(b),q.x,q.y,cwdGrowth(b)))b._lastPart={id:'codeWall1003d'};
   hitBoss(dmg);
  },v.w*.8,v.h*.8));
 }
 if(b._r30.shield>0)targets.push(retinaDynamicPiece(b,'pt11-ghost-wall','spectral barrier',()=>{
  const q=r30ShieldBounds(b);return {...q,hp:b._r30.shield,dead:!r30Live(b)||b._r30.shield<=0};
 },dmg=>{b._lastPart={id:'codeWall1003d'};hitBoss(dmg);},250,220));
 return targets;
}
retinaBossTargets=function(b){return aa5Ghost(b)?r30Live(b)&&!b._noHit?pt11GhostTargets(b):[]:PT11F.base.targets.apply(this,arguments);};
r30Attack=function(b){const r=PT11F.base.attack.apply(this,arguments),P=b?._r30?.attack,J=j3State(b);
 if(!J||J.encounter>=2||!P)return r;
 if(P.download){P.tell=2.2;P.downloadRaised=false;}
 // The lane starts at the same shoulder/eye which glows during its charge.
 if(['hostLance','hostCross'].includes(P.type))P.lanes=[-1,1].map(side=>{const m=pt11HostMuzzle(b,side),tx=P.tx+side*(P.type==='hostCross'?-90:36);return{...s81003Lane(m.x,m.y,tx,P.ty,22),tx,ty:P.ty,_pt11Side:side};});
 if(P.type==='ghostRail'){const eye=aa5GhostRig(b).find(v=>v.p.id==='eye');if(eye)P.lanes=[{...s81003Lane(eye.x,eye.y,P.tx,P.ty,21),tx:P.tx,ty:P.ty,module:'eye'}];}
 return r;
};
r30AttackTick=function(b,dt){const P=b?._r30?.attack,J=j3State(b);
 if(P?.lanes&&P.t<P.tell)for(const L of P.lanes){
  const point=pt11BeamEmitter(b,L);if(point)Object.assign(L,s81003Lane(point.x,point.y,L.tx??P.tx,L.ty??P.ty,L.width));
 }
 if(P?.download&&!P.downloadRaised&&P.t+dt>=P.tell){P.downloadRaised=true;
  if(J.encounter===0||b.parts.some(p=>p.id==='eye'&&!p.destroyed)){
   on5Shield(b,J.encounter===1?'violet':'blue',Math.ceil(b.maxhp*.065));pt11Log('download-complete',{phase:J.encounter});r30Sound('combatEnergy0927');}
 }
 return PT11F.base.attackTick.apply(this,arguments);
};
function pt11HostMuzzle(b,side){
 // Measured dark cannon mouths in the actual 388x345 possessed_body plate.
 const v=r30Parts(b).find(v=>v.p.id==='core'),Q=r30Pose(b);if(!v)return{x:Q.x,y:Q.y};
 const sx=side<0?62:331,sy=side<0?237:233,dx=(sx/388-.5)*v.w,dy=(sy/345-.5)*v.h,c=Math.cos(v.rot||0),s=Math.sin(v.rot||0);
 return{x:v.x+dx*c-dy*s,y:v.y+dx*s+dy*c};
}
function pt11BeamEmitter(b,L){
 if(L._pt11Side)return pt11HostMuzzle(b,L._pt11Side);
 if(aa5Ghost(b)&&L.module){const v=aa5GhostRig(b).find(v=>v.p.id===L.module);if(v)return{x:v.x,y:v.y};}
 return null;
}
PT11F.base.shot=f1003bShot;
f1003bShot=function(b,x,y,a,speed,kind,large){const J=j3State(b),P=b?._r30?.attack;
 if(J?.encounter===0&&P?.type==='hostGuns'){
  const m=pt11HostMuzzle(b,x<b.x?-1:1),offset=a-Math.atan2(P.ty-y,P.tx-x);
  a=Math.atan2(P.ty-m.y,P.tx-m.x)+offset;x=m.x;y=m.y;
 }
 return PT11F.base.shot.call(this,b,x,y,a,speed,kind,large);
};
// A successful claw hit briefly grips the wreck, then throws it into the
// existing anchored burning spin/crash. Shields and invulnerability still run
// through the ordinary hit owner before a capture can be created.
PT11F.base.playerHit=playerHit;PT11F.base.deathSpin=updateDeathSpin;
PT11F.base.locked=dr5Locked;
dr5Locked=function(){return boss?._r30?.mode==='takeover'&&!!j3State(boss)||PT11F.base.locked.apply(this,arguments);};
playerHit=function(source){const wasDead=player.dead,r=PT11F.base.playerHit.apply(this,arguments),b=boss,J=j3State(b);
 if(!wasDead&&player.dead&&player._spin&&J?.encounter<2&&b._r30.mode==='fight'&&
    ['symbiote lunge','MUTATION SPEAR'].includes(source)){
  const parts=(J.encounter===0?r30Parts(b):aa5GhostRig(b)).filter(v=>['left','right','clawL','clawR'].includes(v.p.id));
  const tips=parts.map(v=>({id:v.p.id,x:v.x-Math.sin(v.rot||0)*v.h*.35,y:v.y+Math.cos(v.rot||0)*v.h*.35}));
  tips.sort((a,c)=>Math.hypot(a.x-player.x,a.y-player.y)-Math.hypot(c.x-player.x,c.y-player.y));
  if(tips[0]){player._pt11Grab={owner:b,id:tips[0].id,t:0};player._spin.vx=(tips[0].x<b.x?-1:1)*120;player._spin.vy=115;pt11Log('claw-grab',{seat:_seat||1});}
 }return r;
};
updateDeathSpin=function(dt){const G=player._pt11Grab;
 if(G&&player._spin&&player.dead){G.t+=dt;const b=G.owner,J=j3State(b);
  const v=b&&!b.dead&&(J?.encounter===0?r30Parts(b):aa5GhostRig(b)).find(v=>v.p.id===G.id);
  if(v&&G.t<.28){player.x=clamp(v.x-Math.sin(v.rot||0)*v.h*.35,camLeftX()+12,camRightX()-12);player.y=clamp(v.y+Math.cos(v.rot||0)*v.h*.35,viewTopY()+12,VH-18);player.deathT+=dt;deathSpinAnchor();return;}
  delete player._pt11Grab;pt11Log('claw-fling',{seat:_seat||1});
 }
 return PT11F.base.deathSpin.apply(this,arguments);
};
PT11F.base.beam=s81003Beam;PT11F.base.beamsTick=s81003BeamsTick;PT11F.base.beamsDraw=s81003BeamsDraw;
s81003Beam=function(owner,L,kind,dur){const q=PT11F.base.beam.apply(this,arguments),J=j3State(owner);
 if(J&&J.encounter<2){q._pt11Palette=J.encounter===0?'#e54258':'#ad72ff';q._pt11Heading=Math.atan2(q.ey-q.y,q.ex-q.x);q._pt11Length=Math.hypot(q.ex-q.x,q.ey-q.y);}
 return q;
};
s81003BeamsTick=function(dt){for(const q of S81003.beams)if(q._pt11Palette){
 const p=pt11BeamEmitter(q.owner,q);if(p){q.x=p.x;q.y=p.y;q.ex=p.x+Math.cos(q._pt11Heading)*q._pt11Length;q.ey=p.y+Math.sin(q._pt11Heading)*q._pt11Length;}
 }return PT11F.base.beamsTick.apply(this,arguments);};
s81003BeamsDraw=function(){const all=S81003.beams,mine=all.filter(q=>q._pt11Palette);S81003.beams=all.filter(q=>!q._pt11Palette);
 try{PT11F.base.beamsDraw.apply(this,arguments);}finally{S81003.beams=all;}
 const a=S81003_ART.beams;if(!XART.rdy(a.key))return;
 for(const q of mine){const im=xartPalette(a.key,q._pt11Palette),dx=q.ex-q.x,dy=q.ey-q.y,angle=Math.atan2(dy,dx),h=Math.hypot(dx,dy)/.91,f=4+Math.floor(q.t*18)%4,w=q.width*3.4;
  ctx.save();ctx.translate(q.x,q.y);ctx.rotate(angle-Math.PI/2);ctx.globalAlpha*=Math.min(1,(q.dur-q.t)/.09);ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,(f%a.cols)*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,-w/2,-h*.07,w,h);ctx.restore();
 }
};
r30Parts=function(b){const list=PT11F.base.parts.apply(this,arguments),P=b?._r30?.attack;
 const K=hf7State(b)?.sig;
 if(K&&['arms','gate','pincer'].includes(K.def.kind)){
  const Q=r30Pose(b);for(const v of list)if(['left','right'].includes(v.p.id)){
   const side=v.p.id==='left'?-1:1,wide=v.h>200,rot=v.rot||0;
   v.x=Q.x+side*(wide?118:72)-Math.sin(rot)*v.h*.4;
   v.y=Q.y-(wide?50:35)+Math.cos(rot)*v.h*.4;
  }
 }
 if(j3State(b)?.encounter!==0||!P?.download)return list;
 const Q=r30Pose(b),u=P.t<P.tell?clamp(P.t/.9,0,1):clamp(1-(P.t-P.tell)/.65,0,1);
 for(const v of list)if(['left','right'].includes(v.p.id)){
  const side=v.p.id==='left'?-1:1,rot=side*2.35*u;
  v.rot=rot;v.x=Q.x+side*78-Math.sin(rot)*v.h*.4;v.y=Q.y-43+Math.cos(rot)*v.h*.4;
 }return list;
};
r30ShieldBounds=function(b){if(!aa5Ghost(b))return PT11F.base.bounds.apply(this,arguments);
 const Q=r30Pose(b);return{x:Q.x,y:Q.y+40,w:268,h:220,rot:0,color:'violet'};
};
cwdImage=function(sheet,color){if(PT11F.ghostPaint){const a=CWD_ART[sheet];return a&&XART.rdy(a.key)?xartPalette(a.key,'#ad72ff'):null;}return PT11F.base.image.apply(this,arguments);};
s81003ShieldDraw=function(b){if(!aa5Ghost(b))return PT11F.base.wall.apply(this,arguments);
 if(!(b._r30.shield>0))return;const q=r30ShieldBounds(b),g=cwdGrowth(b);
 ctx.save();ctx.translate(q.x,q.y);ctx.beginPath();ctx.rect(-q.w/2,q.h/2-q.h*g,q.w,q.h*g);ctx.clip();PT11F.ghostPaint=true;
 try{ctx.globalAlpha*=.68;cwdRows(b,q);ctx.globalAlpha/=.68;cwdCell('wall','blueRim',0,0,q.w,q.h,.95);}finally{PT11F.ghostPaint=false;ctx.restore();}
};
r30At=function(b,x,y){if(aa5Ghost(b)&&r30Live(b)&&b._r30.shield>0&&cwdContains(r30ShieldBounds(b),x,y,cwdGrowth(b))){
 b._r30.wallContact1003d={x,y,clock:b._r30.clock};return{id:'codeWall1003d',hp:b._r30.shield,dmg:true};}
 return PT11F.base.at.apply(this,arguments);
};
function pt11ChargeDraw(b,P){const u=clamp(P.t/P.tell,0,1);
 for(const L of P.lanes||[]){wm26Draw(ctx,'orb',L.x,L.y,0,(P.t*12)%1,24+u*26,'#d74965');groundTargetReticleDraw(L.tx??P.tx,L.ty??P.ty,66,u,.8);}
 if(P.download){const Q=r30Pose(b),x=Q.x,y=Math.max(PLAY.y+35,Q.y-118),w=146;
  ctx.save();ctx.fillStyle='#060a16';ctx.fillRect(x-w/2-7,y-19,w+14,42);ctx.strokeStyle=aa5Ghost(b)?'#c390ff':'#70dfff';ctx.strokeRect(x-w/2-7,y-19,w+14,42);
  pcFontLeft('DOWNLOAD '+Math.floor(u*100)+'%',x-w/2+5,y-12,11,'#e9f3ff',1);ctx.fillStyle='#18263a';ctx.fillRect(x-w/2,y+7,w,7);ctx.fillStyle=aa5Ghost(b)?'#ba7eff':'#80e9ff';ctx.fillRect(x-w/2,y+7,Math.round(w*u),7);ctx.restore();
 }
}
r30DrawBoss=function(b){const J=j3State(b),S=b?._r30,P=S?.attack;
 if(J&&S.mode==='dr5Reform'){pt11ReformDraw(b);dr5EffectsDraw(b);return;}
 if(J?.encounter===0&&S.mode==='encounterFall1003j'){pt11FallDraw(b);dr5EffectsDraw(b);return;}
 if(J&&J.encounter<2&&S.mode==='fight'&&P?.lanes?.length&&P.t<P.tell){ctx.save();ctx.globalAlpha=.22*clamp(P.t/.4,0,1);ctx.fillStyle='#000';ctx.fillRect(-32,viewTopY()-32,worldWidth()+64,viewH()+64);ctx.restore();}
 const r=PT11F.base.draw.apply(this,arguments);
 if(J&&J.encounter<2&&S.mode==='fight'){
  if(aa5Ghost(b))s81003ShieldDraw(b);
  if(P&&P.t<P.tell)pt11ChargeDraw(b,P);
 }return r;
};
