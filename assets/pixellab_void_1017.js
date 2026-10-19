"use strict";
/* PixelLab authored pictures; existing encounter clocks and collisions remain
   with their owners. Only the visual environment and effect banks change. */
const VOID17={base:{load:stageLoadBegin,warm:r30Warm,tick:r30Tick,encounter:j3Encounter,
 bg:drawBG,portal:s7mPortalDraw,blit:s7mBlit,toxic:missionToxicPortal,arrival:fr27ToxicPortal,cell:aa5Cell,realm:r30Blit,worldPortal:pl11World,oldVoid:ap10VoidCell},
 draws:{portal:0,back:0,code:0},last:null,portals:[],buffers:new Map()};
for(const [name,entry] of Object.entries(PXV17_ART.portals)){
 PL11_ART[name]=entry;
 for(const phase of PL11.phases)for(const a of entry[phase].frames)XART._src[a.key]=a.path;
}
for(const a of [...PXV17_ART.arenas,...PXV17_ART.code])XART._src[a.key]=a.path;
for(const [family,bank] of Object.entries(PXV17_ART.wind||{})){
 const slot=WP11_FAMILIES.indexOf(family);
 AP10_FX_ART['wind_'+family]=bank.map(a=>({...a,slot,_a17:true}));
 for(const a of bank)XART._src[a.key]=a.path;
}
if(Object.keys(PXV17_ART.wind||{}).length)WP11_KEYS.splice(0,WP11_KEYS.length,...new Map(WP11_FAMILIES.flatMap(f=>AP10_FX_ART['wind_'+f]||[]).map(a=>[a.key,a])).values());
function v17Keys(stage){
 const banks=stage===7?['green_rift','black_void']:Object.keys(PXV17_ART.portals);
 return [...banks.flatMap(name=>PL11.keys(name)),...(stage===8?[...PXV17_ART.arenas,...PXV17_ART.code].map(a=>a.key):[])];
}
function v17Warm(stage=run.stage){for(const key of v17Keys(stage))XART.rdy(key);}
stageLoadBegin=function(n,keys){return VOID17.base.load.call(this,n,[7,8].includes(n)?[...(keys||[]),...v17Keys(n)]:keys);};
r30Warm=function(){const out=VOID17.base.warm.apply(this,arguments);if(run.stage===8)v17Warm(8);return out;};
function v17Clock(b){const J=j3State(b);if(!J)return null;
 return J.v17??={t:0,combat:0,phase:J.encounter||0,previous:null,transition:2};}
j3Encounter=function(b,n){const old=j3State(b)?.encounter,out=VOID17.base.encounter.apply(this,arguments),Q=v17Clock(b);
 if(Q&&old!==n){Q.previous=Number.isInteger(old)?old:null;Q.phase=n;Q.transition=0;Q.combat=0;}
 return out;};
r30Tick=function(b,dt){const Q=run.stage===8?v17Clock(b):null;
 if(Q){const step=clamp(dt||0,0,.05);Q.t+=step;Q.transition+=step;if(b._r30?.mode==='fight')Q.combat+=step;}
 return VOID17.base.tick.apply(this,arguments);};
function v17Route(bank,pose){
 const normal=['blue_rift','green_rift','red_rift'].includes(bank);
 const routed=normal?(run.stage===7?'green_rift':run.stage===8?'red_rift':bank):bank;
 if(routed===bank)return {bank,pose};
 const clip=PL11_ART[routed][pose.phase];
 // Match normalized phase time even when the source/target frame counts
 // differ. The native finite-cycle cadence and endpoint timing survive.
 return {bank:routed,pose:PL11.sample(routed,pose.phase,pose.seconds,{duration:pose.duration,
  fps:pose.phase==='loop'?clip.frames.length/pose.duration:clip.fps})};
}
function v17Record(bank,pose,x,y,size){
 VOID17.draws.portal++;VOID17.portals.push({bank,phase:pose.phase,from:pose.from,x,y,size});if(VOID17.portals.length>100)VOID17.portals.shift();
}
function v17Portal(bank,pose,x,y,size,alpha=1,rotation=0){
 ({bank,pose}=v17Route(bank,pose));
 if(!PL11.ready(bank,XART)){v17Warm(run.stage);return false;}
 if(rotation)pose={...pose,rotation:(pose.rotation||0)+rotation};
 const ok=PL11.draw(ctx,pose,x,y,size,k=>XART.get(k),alpha);
 if(ok)v17Record(bank,pose,x,y,size);
 return ok;
}
pl11World=function(bank,pose,x,y,size,alpha=1){
 ({bank,pose}=v17Route(bank,pose));
 const ok=VOID17.base.worldPortal.call(this,bank,pose,x,y,size,alpha);
 if(ok)v17Record(bank,pose,x,y,size);return ok;
};
PL11_GAME.banks.splice(0,PL11_GAME.banks.length,'black_void','red_rift');
function v17LegacyPortal(bank,f,t,open=4,close=12){
 return f<open?PL11.sample(bank,'form',clamp(f/Math.max(1,open-1),0,1),{duration:1}):
  f>=close?PL11.sample(bank,'close',clamp((f-close)/Math.max(1,16-close-1),0,1),{duration:1}):PL11.sample(bank,'loop',t);
}
ap10VoidCell=function(f,x,y,w,h=w,rot=0,alpha=1){
 if(run.stage!==8)return VOID17.base.oldVoid.apply(this,arguments);
 const t=j3State(boss)?.pt11Portal?.t??boss?._r30?.clock??efxClock;
 const pose=f<8?PL11.sample('black_void','form',f/7,{duration:1}):f>=24?PL11.sample('black_void','close',(f-24)/7,{duration:1}):PL11.sample('black_void','loop',t);
 return v17Portal('black_void',pose,x,y,Math.min(w,h),alpha,rot);
};
function v17S7Entrance(M){
 const hasIntro=!!M._mission29Intro,base=hasIntro?3.7:0;
 const intro=hasIntro&&!M._mission29IntroDone;
 const t=intro?Math.max(0,M._mission29Intro.t-3.3):base+(M.mode==='portal'?M.t:M.mode==='entry'?1.4+M.t:2.52+M.t);
 return PL11.sequence('green_rift',t,{form:1.4,loop:1.12+base,close:1.2});
}
function v17S7Exit(E,x,y,alpha=1,rot=0){
 const C=E.k1001&&typeof S7P!=='undefined'?S7P:typeof S67E!=='undefined'?S67E:null;
 const age=E.portalT??Math.max(0,E.t-14.1),duration=C?.CLOSE||1.2;
 const pose=E.closeT?PL11.sample('green_rift','close',E.t-E.closeT,{duration}):
  PL11.sequence('green_rift',age,{form:.6,loop:E.k1001?Math.max(.1,C.PULL+C.ENTRY-C.OPEN-.6):Infinity,close:duration});
 // Escape owners used to grow/shrink an idle picture. Keep one canvas and
 // let the separately authored formation and implosion provide that motion.
 return v17Portal('green_rift',pose,x,y,(C?.PORTAL_H||274)*.87,alpha,rot);
}
missionToxicPortal=function(f,x,y,w,h){
 const M=run.stage===7?boss?._s7mod:null;
 if(M?.frExit)return v17S7Exit(M.frExit,x,y);
 if(M&&!M.tank&&['portal','entry','roar'].includes(M.mode))return v17Portal('green_rift',v17S7Entrance(M),x,y,240);
 if(run.stage===8)return v17Portal('red_rift',v17LegacyPortal('red_rift',f,efxClock),x,y,Math.min(w,h||w));
 return VOID17.base.toxic.apply(this,arguments);
};
fr27ToxicPortal=function(f,x,y,size){
 if(run.stage===8&&state===GS.WARPENTRY&&l78entry){
  const pose=PL11.sequence('red_rift',Math.max(0,l78entry.t-.7),{form:.5,loop:1.8,close:1});
  return v17Portal('red_rift',pose,x,y,170*viewZoom()*1.55);
 }
 return VOID17.base.arrival.apply(this,arguments);
};
s7mPortalDraw=function(){
 if(run.stage!==7)return false;const M=boss?._s7mod;
 if(!M||M.tank||!['portal','entry','roar'].includes(M.mode))return true;
 const pose=v17S7Entrance(M);
 if(!pose.done||pose.phase!=='close')v17Portal('green_rift',pose,worldWidth()/2,149,240);
 return true;
};
s7mBlit=function(name,i,x,y,w,h,rot,alpha,flash){
 if(name==='portal'&&run.stage===7){
  const M=boss?._s7mod,P=M?.portals?.find(p=>Math.abs(p.x-x)<1&&Math.abs(p.y-y)<1);
  if(!P&&M?.frExit)return v17S7Exit(M.frExit,x,y,alpha??1,rot||0);
  if(!P&&M&&!M.tank&&['portal','entry','roar'].includes(M.mode))return v17Portal('green_rift',v17S7Entrance(M),x,y,Math.min(w,h||w),alpha??1,rot||0);
  const t=P?.t??M?.clock??0,life=M?.live||4.6;
  return v17Portal('green_rift',PL11.sequence('green_rift',t,{form:.8,loop:Math.max(.01,life-1.4),close:.6}),x,y,Math.min(w,h||w),alpha??1,rot||0);
 }
 return VOID17.base.blit.apply(this,arguments);
};
aa5Cell=function(name,f,x,y,w,h=w,rot=0,alpha=1){
 if(name==='void'&&run.stage===8){
  const S=boss?._r30,Q=v17Clock(boss),P=S?.attack;
  let pose;
  if(['takeover','voidIntro1005','transform1003j'].includes(S?.mode)&&f<9)
   pose=PL11.sample('black_void','form',clamp(f/8,0,1),{duration:1});
  else if(P&&['ghostWarp','aa5Void','cf4Court'].includes(P.type))
   pose=PL11.sequence('black_void',P.t,{form:Math.min(.7,P.tell||.7),loop:Math.max(.1,(P.tell||1)+(P.active||2)-1.3),close:.6});
  else pose=PL11.sample('black_void','loop',Q?.t||0);
  return v17Portal('black_void',pose,x,y,Math.min(w,h),alpha,rot);
 }
 return VOID17.base.cell.apply(this,arguments);
};
r30Blit=function(key,x,y,w,h,rot,alpha){
 if(key==='vile25_phantom_ground_portal'&&run.stage===8){
  const P=boss?._r30?.attack,t=P?.t||0,life=P?.tell||1.55;
  return v17Portal('black_void',PL11.sequence('black_void',t,{form:life*.3,loop:life*.4,close:life*.3}),x,y,w,alpha??1,rot||0);
 }
 return VOID17.base.realm.apply(this,arguments);
};
if(typeof hc7VoidDraw==='function'){
 VOID17.base.hcVoid=hc7VoidDraw;VOID17.base.hcReel=hc7Reel;
 hc7VoidDraw=function(b,x,y,size,alpha=1){
  if(run.stage!==8)return VOID17.base.hcVoid.apply(this,arguments);
  const C=b?._r30?.hc7Rift;let pose;
  if(C?.phase==='raise')pose=PL11.sample('black_void','form',Math.max(0,C.t-1),{duration:1.6});
  else if(C?.phase==='recover')pose=PL11.sample('black_void','close',C.t,{duration:.75});
  else pose=PL11.sample('black_void','loop',C?.t??hc7Clock(b));
  // The old caller shrank a looping picture. Keep the full physical canvas
  // fixed and let the separately authored opening/closure carry its growth.
  const ok=v17Portal('black_void',pose,x,y,C?C.radius*2:size,alpha);
  if(ok)HC7.draws.void=(HC7.draws.void||0)+1;return ok;
 };
 hc7Reel=function(name,t,x,y,w,h,alpha=1,rot=0){
  if(name==='void'&&run.stage===8)return v17Portal('black_void',PL11.sample('black_void','loop',t),x,y,Math.min(w,h),alpha,rot);
  return VOID17.base.hcReel.apply(this,arguments);
 };
}
if(typeof vile25Sprite==='function'){
 VOID17.base.vileSprite=vile25Sprite;
 vile25Sprite=function(key,x,y,w,h,alpha,flip){
  if(key==='vile25_phantom_ground_portal'&&run.stage===8){
   const S=boss?._r30,P=boss?._v24?.pattern||S?.attack;
   const pose=P?.cycleTime?PL11.sequence('black_void',Math.max(0,P.t-P.tell)%P.cycleTime,{form:P.cycleTime*.3,loop:P.cycleTime*.4,close:P.cycleTime*.3}):PL11.sample('black_void','loop',S?.clock??efxClock);
   return v17Portal('black_void',pose,x,y,w,alpha??1);
  }
  return VOID17.base.vileSprite.apply(this,arguments);
 };
}
if(typeof vile24Cell==='function'){
 VOID17.base.vileCell=vile24Cell;
 vile24Cell=function(key,cols,rows,f,x,y,w,h,alpha){
  if(key==='vile24_ground_portal_rise_sheet'&&run.stage===8){
   const P=boss?._v24?.pattern;let pose;
   if(P?.type==='void'){
    if(P.t<P.tell)pose=PL11.sample('black_void','form',P.t,{duration:P.tell});
    else if(Number.isFinite(P.activeUntil)&&P.t>P.activeUntil-.6)pose=PL11.sample('black_void','close',P.t-P.activeUntil+.6,{duration:.6});
    else pose=PL11.sample('black_void','loop',P.t-P.tell);
   }else pose=PL11.sample('black_void','loop',boss?._r30?.clock??efxClock);
   return v17Portal('black_void',pose,x+w/2,y+h/2,w,alpha??1);
  }
  return VOID17.base.vileCell.apply(this,arguments);
 };
}
function v17Active(b){return run.stage===8&&b?._r30&&!b.dead&&[0,1,2].includes(j3State(b)?.encounter)&&!['escape','reunion','done'].includes(b._r30.mode);}
function v17Plate(a,x,y,k,alpha=1){
 if(alpha<=0||!XART.rdy(a.key))return false;
 const im=XART.get(a.key);if(!im)return false;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;
}
function v17Code(frame,x,y,size,alpha){
 const bank=PXV17_ART.code,pos=((frame%bank.length)+bank.length)%bank.length,i=Math.floor(pos),mix=pos-i;
 const a=bank[i],b=bank[(i+1)%bank.length];if(!XART.rdy(a.key)||!XART.rdy(b.key))return false;
 let c=VOID17.buffers.get('code');if(!c){c=document.createElement('canvas');c.width=a.w;c.height=a.h;VOID17.buffers.set('code',c);}
 const g=c.getContext('2d');g.clearRect(0,0,a.w,a.h);g.globalCompositeOperation='source-over';g.globalAlpha=1-mix;g.drawImage(XART.get(a.key),0,0);
 g.globalCompositeOperation='lighter';g.globalAlpha=mix;g.drawImage(XART.get(b.key),0,0);g.globalAlpha=1;g.globalCompositeOperation='source-over';
 const k=size/a.w;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(c,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;
}
function v17ArenaDraw(b){
 if(!v17Active(b))return false;const J=j3State(b),S=b._r30,Q=v17Clock(b),phase=J.encounter,t=Q.t;
 const left=camLeftX(),top=viewTopY(),w=viewW(),h=viewH(),world=worldWidth(),mid=world/2,cam=left-(world-w)/2;
 const a=PXV17_ART.arenas[phase],k=Math.max((world+160)/a.w,(h+160)/a.h),awake=clamp(Q.combat/4,0,1);
 const fade=phase===2&&S.mode==='voidIntro1005'?clamp((S.t-1.4)/1.6,0,1):1;
 const blend=clamp(Q.transition/1.2,0,1),P=S.attack,pulse=P?Math.max(0,1-Math.abs(P.t-P.tell)/.6):0;
 const dx=Math.sin(t*.11)*9+cam*.08,dy=Math.cos(t*.09)*7;
 ctx.save();ctx.beginPath();ctx.rect(left-20,top-20,w+40,h+40);ctx.clip();ctx.globalAlpha*=fade;
 ctx.fillStyle='#000';ctx.fillRect(left-20,top-20,w+40,h+40);
 const light=[.56,.38,.46];
 if(Q.previous!=null&&blend<1)v17Plate(PXV17_ART.arenas[Q.previous],mid+dx,top+h/2+dy,k,light[Q.previous]);
 if(v17Plate(a,mid+dx,top+h/2+dy,k,(Q.previous==null?1:blend)*light[phase]))VOID17.draws.back++;
 const points=[];
 for(let i=0;i<9;i++){
  const depth=[.08,.18,.34][i%3],size=[104,142,180][i%3],span=h+size*2;
  const x=world*((i*.381966+.12)%1)+cam*depth+Math.sin(t*.15+i)*7;
  const y=top+(((i*.173*h+t*(i%2?-1:1)*(3+depth*18)+size)%span+span)%span)-size;
  const alpha=(.045+depth*.2)*(.16+.84*awake)*(.8+.2*Math.sin(t*.7+i))+pulse*.018;
  const frame=t*14+i*4;
  if(v17Code(frame,x,y,size,alpha))VOID17.draws.code++;
  points.push({x,y,size,alpha,depth,frame});
 }
 ctx.restore();J.aa5ArenaDrawn=true;VOID17.last={phase,t,combat:Q.combat,awake,fade,blend,left,top,w,h,k,dx,dy,points};return true;
}
aa5ArenaDraw=v17ArenaDraw;
drawBG=function(dt){const out=VOID17.base.bg.apply(this,arguments);if(v17Active(boss)&&j3State(boss).encounter!==2)v17ArenaDraw(boss);return out;};
globalThis.BOF_PIXEL_VOID={state:VOID17,drawArena:v17ArenaDraw,warm:v17Warm,active:v17Active};
