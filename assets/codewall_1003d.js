"use strict";
/* Authored binary rows scroll independently of damage. The same projected
   polygon owns rendering, bullet interception and Retina target geometry. */
for(const a of Object.values(CWD_ART))XART._src[a.key]=a.path;
const CWD={effects:[],serial:0};
const CWD_BASE={warm:r30Warm,begin:beginStage,form:r30Form,attack:r30Attack,
 knight:s81003KnightEnter,tick:r30Tick,at:r30At,hit:modularHit,targets:retinaBossTargets,
 bounds:r30ShieldBounds,wall:s81003ShieldDraw,draw:r30DrawBoss,update:updatePlay,bullets:drawBullets,clear:r30Clear};
function cwdWarm(){for(const a of Object.values(CWD_ART))XART.rdy(a.key);}
r30Warm=function(){CWD_BASE.warm();cwdWarm();};
beginStage=function(n){CWD.effects.length=0;const r=CWD_BASE.begin.apply(this,arguments);if(n===8)cwdWarm();return r;};
r30Form=function(b,n){const r=CWD_BASE.form.apply(this,arguments);if(fmcLive(b)){b._r30.codeWall1003d='blue';b._r30.wallContact1003d=null;}return r;};
function cwdRaise(b,color,hp){const S=b._r30;S.codeWall1003d=color;S.shield=S.shieldMax=Math.ceil(hp);S.wallAge1003=0;S.wallContact1003d=null;}
s81003KnightEnter=function(b,phase){
 const r=CWD_BASE.knight.apply(this,arguments);
 if(fmcLive(b)&&phase==='guard'&&b._r30.shield>0)cwdRaise(b,'red',b._r30.shieldMax);
 return r;
};
r30Attack=function(b){
 const r=CWD_BASE.attack.apply(this,arguments);if(!fmcLive(b))return r;
 const S=b._r30,P=S.attack;
 // Full-height blue walls guard the existing reactor charge; the knight's
 // smaller red projection belongs exclusively to his physical shield.
 if(P&&!P.k1003&&['gravity','orbit','iceOrbit','turbines'].includes(P.type))cwdRaise(b,'blue',S.base*.055);
 return r;
};
r30Tick=function(b,dt){
 const r=CWD_BASE.tick.apply(this,arguments);if(!fmcLive(b))return r;
 const S=b._r30,P=S.attack;
 if(S.codeWall1003d==='blue'&&S.shield>0&&(!P||P.t>=P.tell))S.shield=0;
 return r;
};
r30ShieldBounds=function(b){
 if(!fmcLive(b))return CWD_BASE.bounds.apply(this,arguments);
 const S=b._r30,Q=r30Pose(b),D=f1003bDef(b);
 if(S.codeWall1003d==='red'){
  const v=fmcRig(b).find(v=>v.p.id==='shield');
  if(v)return{x:v.x,y:v.y,w:v.w*1.55,h:v.h*1.38,rot:v.rot,color:'red'};
  return{x:Q.x,y:Q.y,w:0,h:0,rot:0,color:'red'};
 }
 return{x:Q.x,y:Q.y+7,w:(D.w+24)*(Q.scale||1),h:(D.h+26)*(Q.scale||1),rot:0,color:'blue'};
};
function cwdGrowth(b){return clamp((b._r30.wallAge1003||0)/.28,0,1);}
function cwdPolygon(q){return q.color==='red'?[[-.43,-.46],[.43,-.46],[.43,-.13],[.30,.17],[0,.46],[-.30,.17],[-.43,-.13]]:[[-.48,-.48],[.48,-.48],[.48,.48],[-.48,.48]];}
function cwdContains(q,x,y,growth=1){
 const a=-(q.rot||0),dx=x-q.x,dy=y-q.y,px=(dx*Math.cos(a)-dy*Math.sin(a))/q.w,py=(dx*Math.sin(a)+dy*Math.cos(a))/q.h;
 if(!q.w||!q.h||py<.5-growth)return false;
 const points=cwdPolygon(q);let inside=false;
 for(let i=0,j=points.length-1;i<points.length;j=i++){
  const [xi,yi]=points[i],[xj,yj]=points[j];if((yi>py)!==(yj>py)&&px<(xj-xi)*(py-yi)/(yj-yi)+xi)inside=!inside;
 }return inside;
}
function cwdPath(q){const p=cwdPolygon(q);ctx.beginPath();p.forEach(([x,y],i)=>i?ctx.lineTo(x*q.w,y*q.h):ctx.moveTo(x*q.w,y*q.h));ctx.closePath();}
function cwdOffset(clock,row,width){const v=clock*(row%2?-1:1)*(24+row%3*5)+row*11;return((v%width)+width)%width;}
function cwdImage(sheet,color){const a=CWD_ART[sheet];if(!XART.rdy(a.key))return null;return color==='red'&&sheet!=='wall'?xartPalette(a.key,'#ff294b'):XART.get(a.key);}
function cwdCell(sheet,frame,x,y,w,h,alpha=1,rot=0,color='blue'){
 const a=CWD_ART[sheet],box=a?.rects[String(frame)],im=a&&cwdImage(sheet,color);if(!im||!box)return false;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(rot);
 ctx.drawImage(im,...box,-w/2,-h/2,w,h);ctx.restore();return true;
}
function cwdRows(b,q){
 const a=CWD_ART.wall,im=cwdImage('wall'),box=a.rects[q.color==='red'?'redRows':'blueRows'];if(!im)return;
 const [sx,sy,sw,sh]=box,innerW=q.w*.85,innerH=q.h*.85,rowH=innerH/12;
 ctx.save();
 if(q.color==='blue'){ctx.beginPath();ctx.rect(-q.w*.39,-q.h*.39,q.w*.78,q.h*.78);}else cwdPath(q);
 ctx.clip();
 for(let row=0;row<12;row++){
  const offset=cwdOffset(b._r30.clock,row,innerW),y=-innerH/2+row*rowH;
  // Tile a measured authored row, never re-render numbers as font glyphs.
  for(let tile=-1;tile<=1;tile++)ctx.drawImage(im,sx,sy+row*sh/12,sw,sh/12,-innerW/2+offset+tile*innerW,y,innerW,rowH);
 }
 ctx.restore();
}
s81003ShieldDraw=function(b){
 if(!fmcLive(b))return CWD_BASE.wall.apply(this,arguments);
 const S=b._r30;if(S.shield<=0)return;const q=r30ShieldBounds(b),g=cwdGrowth(b);if(!q.w||!g)return;
 ctx.save();ctx.translate(q.x,q.y);ctx.rotate(q.rot);ctx.imageSmoothingEnabled=false;
 ctx.beginPath();ctx.rect(-q.w/2,q.h/2-q.h*g,q.w,q.h*g);ctx.clip();
 ctx.globalAlpha*=q.color==='red'?.72:.65;cwdRows(b,q);
 ctx.globalAlpha/=q.color==='red'?.72:.65;
 cwdCell('wall',q.color==='red'?'redRim':'blueRim',0,0,q.w,q.h,.95);
 // shieldFlash intentionally never changes the wall image, clock or opacity.
 ctx.restore();
};
r30At=function(b,x,y){
 if(!fmcLive(b))return CWD_BASE.at.apply(this,arguments);
 if(!r30Live(b)||r30Pose(b).alpha<.25)return null;
 const S=b._r30,q=r30ShieldBounds(b);
 if(S.shield>0&&cwdContains(q,x,y,cwdGrowth(b))){S.wallContact1003d={x,y,clock:S.clock};return{id:'codeWall1003d',hp:S.shield,dmg:true};}
 const shield=S.shield;S.shield=0;try{return CWD_BASE.at.apply(this,arguments);}finally{S.shield=shield;}
};
function cwdImpact(b,q){
 const S=b._r30;if(S.codeImpactAt1003d!=null&&S.clock-S.codeImpactAt1003d<.065)return;
 S.codeImpactAt1003d=S.clock;const c=S.wallContact1003d;
 const pos=c&&S.clock-c.clock<.16&&cwdContains(q,c.x,c.y)?c:{x:q.x,y:q.y+q.h*.15};
 CWD.effects.push({owner:b,kind:'impact',color:q.color,x:pos.x,y:pos.y,w:64,h:64,t:0,dur:.32});
 (Audio.SFX.projectileRicochet||Audio.SFX.shieldDeflect||function(){})();
}
function cwdShatter(b,q){
 CWD.effects.push({owner:b,kind:'shatter',color:q.color,x:q.x,y:q.y,w:Math.min(175,q.w*.8),h:Math.min(175,q.w*.8),t:0,dur:.68});
 for(let i=0;i<24;i++){
  const a=i*TAU/24,sp=105+(i%4)*24,rotation=q.rot||0;
  const lx=Math.cos(a)*q.w*.27,ly=Math.sin(a)*q.h*.30;
  CWD.effects.push({owner:b,kind:'chip',color:q.color,x:q.x+lx*Math.cos(rotation)-ly*Math.sin(rotation),y:q.y+lx*Math.sin(rotation)+ly*Math.cos(rotation),
   vx:Math.cos(a+rotation)*sp,vy:Math.sin(a+rotation)*sp,rot:a,spin:(i%2?1:-1)*(1+i%3),row:i%12,col:i%7*2,w:12+(i%3)*3,h:10+(i%3)*3,t:0,dur:.75+(i%4)*.12});
 }
 shake=Math.max(shake,5);r30Sound('shieldBreakCombat');f1003bLog(b,'codeWallBreak1003d',{color:q.color,chips:24});
}
modularHit=function(dmg){
 const b=boss;if(!fmcLive(b))return CWD_BASE.hit.apply(this,arguments);
 const S=b._r30;if(!r30Live(b)||!Number.isFinite(dmg)||dmg<=0)return;
 if(S.shield>0){
  const q=r30ShieldBounds(b),p=b._lastPart;
  if(p?.id==='codeWall1003d'||(q.color==='blue'&&!b.parts.includes(p))){
   S.shield=Math.max(0,S.shield-dmg);cwdImpact(b,q);if(!S.shield)cwdShatter(b,q);
   if(CWD.effects.length>96)CWD.effects.splice(0,CWD.effects.length-96);return;
  }
  // A shot hitting an exposed arm/core is not absorbed by a remote shield.
  const shield=S.shield,attack=S.attack;S.shield=0;
  const result=CWD_BASE.hit.apply(this,arguments);
  if(r30Live(b)&&S.attack===attack&&(q.color!=='red'||fmcAlive(b,'shield')&&fmcAlive(b,'shieldArm')))S.shield=shield;
  return result;
 }
 return CWD_BASE.hit.apply(this,arguments);
};
function cwdRetinaModules(b){
 const S=b._r30,shield=S.shield;S.shield=0;let modules;try{modules=CWD_BASE.targets(b);}finally{S.shield=shield;}
 for(const m of modules){const hit=m._retinaHit;m._retinaHit=function(dmg){
  const q=r30ShieldBounds(b);
  if(S.shield>0&&cwdContains(q,m.x,m.y,cwdGrowth(b))){S.wallContact1003d={x:m.x,y:m.y,clock:S.clock};b._lastPart={id:'codeWall1003d'};hitBoss(dmg);}else hit(dmg);
 };}return modules;
}
function cwdShieldTargetState(b){
 const S=b._r30,q=r30ShieldBounds(b),g=cwdGrowth(b),low=Math.max(-.46,.5-g),center=(low+.46)*q.h/2;
 return{...q,x:q.x-Math.sin(q.rot)*center,y:q.y+Math.cos(q.rot)*center,h:Math.max(0,.46-low)*q.h,hp:S.shield,dead:!r30Live(b)||S.shield<=0||g<.04};
}
retinaBossTargets=function(b){
 if(!fmcLive(b))return CWD_BASE.targets.apply(this,arguments);
 const S=b._r30;if(S.shield<=0)return cwdRetinaModules(b);
 if(!r30Live(b)||r30Pose(b).alpha<.25)return [];
 const q=r30ShieldBounds(b),target=retinaDynamicPiece(b,'code-wall-1003d-'+S.form,q.color+' code shield',()=>cwdShieldTargetState(b),
 dmg=>{const v=cwdShieldTargetState(b);S.wallContact1003d={x:v.x,y:v.y,clock:S.clock};b._lastPart={id:'codeWall1003d'};hitBoss(dmg);},q.w*.72,cwdShieldTargetState(b).h*.72);
 if(q.color!=='red')return[target];
 const modules=cwdRetinaModules(b);
 // Exposed modules keep their locks. The physical shield is covered until its
 // projection breaks, preventing a duplicate lock on the same defended plate.
 return[target,...modules.filter(m=>!cwdContains(q,m.x,m.y,cwdGrowth(b)))];
};
function cwdEffectsTick(dt){
 for(const f of CWD.effects){f.t+=dt;if(f.kind==='chip'){f.x+=f.vx*dt;f.y+=f.vy*dt;f.rot+=f.spin*dt;const drag=Math.exp(-1.5*dt);f.vx*=drag;f.vy*=drag;}}
 CWD.effects=CWD.effects.filter(f=>f.t<f.dur);
}
function cwdEffectsDraw(){for(const f of CWD.effects){
 const alpha=Math.min(1,(f.dur-f.t)/.22);
 if(f.kind==='chip'){
  const a=CWD_ART.wall,im=cwdImage('wall'),box=a.rects[f.color==='red'?'redRows':'blueRows'];if(!im)continue;
  const [x,y,w,h]=box;ctx.save();ctx.translate(f.x,f.y);ctx.rotate(f.rot);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,x+f.col*w/15,y+f.row*h/12,w/15,h/12,-f.w/2,-f.h/2,f.w,f.h);ctx.restore();
 }else cwdCell(f.kind,Math.min(7,Math.floor(f.t/f.dur*8)),f.x,f.y,f.w,f.h,alpha,0,f.color);
}}
updatePlay=function(dt){const r=CWD_BASE.update.apply(this,arguments);if(run.stage===8&&state===GS.PLAY)cwdEffectsTick(Math.min(dt,.05));return r;};
drawBullets=function(){const r=CWD_BASE.bullets.apply(this,arguments);cwdEffectsDraw();return r;};
r30Clear=function(b){const r=CWD_BASE.clear.apply(this,arguments);CWD.effects=CWD.effects.filter(f=>f.owner!==b);return r;};
/* New reconstruction scan replaces both old spherical morph and its overlaid
   teleport reel. Encounter timing, modular rigs and eight life pools stay owned
   by the existing controller. */
r30DrawBoss=function(b){
 if(!fmcLive(b)||!['takeover','morph1003b','reveal'].includes(b._r30.mode))return CWD_BASE.draw.apply(this,arguments);
 const S=b._r30,D=f1003bDef(b),T=S.t;let f,alpha;
 ctx.save();
 if(S.mode==='takeover'){
  const u=clamp(T/4.4,0,1);r30Blit('vile24_robot_gray',b.x,b.y,230,230,0,1-clamp((u-.18)/.46,0,1));
  f1003bBodyDraw(b,clamp((u-.32)/.48,0,1));f=u*11;alpha=Math.min(1,T/.22,Math.max(0,(4.4-T)/.35));
 }else if(S.mode==='morph1003b'){
  f1003bBodyDraw(b,Math.max(0,1-T/1.25));f=clamp(T/1.65,0,1)*5;alpha=Math.min(1,T/.12);
 }else{
  f1003bBodyDraw(b,clamp(T/.65,0,1));f=6+clamp(T/1.1,0,1)*5;alpha=Math.min(1,Math.max(0,(1.1-T)/.25));
 }
 // Cross-fade adjacent authored cells to remove frame pops without blurring
 // their pixel edges. The center stays transparent rather than hiding the rig.
 const frame=Math.min(11,Math.floor(f)),mix=f-frame,w=D.w+45,h=D.h+75;
 cwdCell('morph',frame,b.x,b.y,w,h,alpha*(1-mix)*.78);
 if(frame<11)cwdCell('morph',frame+1,b.x,b.y,w,h,alpha*mix*.78);
 ctx.restore();
};
