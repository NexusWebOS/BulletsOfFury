'use strict';
/* World-anchored downloaded terrains; native forms, movement, modules and danger
   clocks remain authoritative. Generated terrain/mesh/curtain layers stay below
   combat and HUD. No snapshots, readbacks, per-frame canvases or extra RAF loop. */
const AD20={base:{arena:v17ArenaDraw,mode:v18SetMode,enter:v18Enter,load:stageLoadBegin,warm:r30Warm},
 themes:{1:'jungle',2:'lava',6:'sky',8:'space'},draws:{},events:[],last:null};
for(const a of [...Object.values(AD20_ART.arenas).flatMap(a=>[a.terrain,a.wire]),AD20_ART.curtain])XART._src[a.key]=a.path;
function ad20Keys(){return [...Object.values(AD20_ART.arenas).flatMap(a=>[a.terrain.key,a.wire.key]),AD20_ART.curtain.key,
 ...Array.from({length:8},(_,i)=>'nlq3_lava_'+i),...SG20_CLOUDS];}
function ad20Warm(){let ready=true;for(const k of ad20Keys())if(!XART.rdy(k))ready=false;
 if(!AD20.audioWarm){AD20.audioWarm=true;Snd.prepare(['bossWeaponCharge','teleportIn','bossPhase']);}return ready;}
stageLoadBegin=function(n,keys){return AD20.base.load.call(this,n,n===8?[...(keys||[]),...ad20Keys()]:keys);};
r30Warm=function(){const out=AD20.base.warm.apply(this,arguments);if(run.stage===8)ad20Warm();return out;};
function ad20Live(b){return v18Owned(b)&&j3State(b).encounter===2&&!b.dead&&
 !['dr5Portal','reunion','done','escape','finalFall'].includes(b._r30.mode);}
function ad20Theme(form){return AD20.themes[form]||'void';}
function ad20Log(type,data){AD20.events.push({type,...data});if(AD20.events.length>80)AD20.events.shift();}
v18Enter=function(b,n,form){const out=AD20.base.enter.apply(this,arguments);if(v18Owned(b)&&n!==2){b._r30.v18.arenaCurrent='void';b._r30.v18.arenaDownload=null;}return out;};
v18SetMode=function(b,mode){const previous=b?._r30?.mode,out=AD20.base.mode.apply(this,arguments);if(!ad20Live(b))return out;
 const N=b._r30.v18;
 if(mode==='v18formOut'){
  N.arenaDownload={from:N.arenaCurrent||ad20Theme(N.from??N.form),to:ad20Theme(N.to),mode:'erase'};
  dr21Cue('bossWeaponCharge');ad20Log('erase',{from:N.arenaDownload.from,to:N.arenaDownload.to});
 }else if(mode==='v18formIn'){
  N.arenaDownload={from:N.arenaDownload?.from||N.arenaCurrent||'void',to:ad20Theme(N.form),mode:'build'};
  ad20Log('build',{from:N.arenaDownload.from,to:N.arenaDownload.to});
 }else if(mode==='fight'){
  N.arenaCurrent=ad20Theme(N.form);N.arenaDownload=null;
  if(previous==='v18formIn')ad20Log('complete',{theme:N.arenaCurrent});
 }return out;
};
function ad20Plate(a,alpha=1){if(!a||!XART.rdy(a.key))return false;
 const w=worldWidth(),h=viewH(),span=a.key.startsWith('ad20_lava_')?Math.min(w+48,viewW()+80):w+48,
  k=Math.max(span/a.w,(h+48)/a.h),x=w/2-a.w*k/2,y=viewTopY()+h/2-a.h*k/2;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),x,y,a.w*k,a.h*k);ctx.restore();
 AD20.draws[a.key]=(AD20.draws[a.key]||0)+1;AD20.plate={x,y,k,w:a.w*k,h:a.h*k};return true;}
function ad20Floor(t,wire=false){
 const f=Math.floor(t*10)%8,key='nlq3_lava_'+f;if(!XART.rdy(key))return false;
 const im=XART.get(key),tw=256,th=256,top=viewTopY(),sy=Math.round((t*8)%th)-th;
 ctx.save();ctx.globalAlpha*=wire?.16:.67;ctx.imageSmoothingEnabled=false;
 let y=sy;while(y>top-th)y-=th;for(;y<VH;y+=th)for(let x=0;x<worldWidth();x+=tw)ctx.drawImage(im,x,y,tw,th);
 ctx.restore();AD20.draws.originalLava=(AD20.draws.originalLava||0)+1;return true;
}
function ad20Curtain(t,y,alpha=1,ambient=false){const a=AD20_ART.curtain;if(!XART.rdy(a.key)||alpha<=0)return;
 const far=ambient==='far',f=Math.floor(t*a.fps)%a.frames,c=a.cells[f],im=XART.get(a.key),w=ambient?(far?270:190):worldWidth()/3+3,h=ambient?w:256;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 if(ambient){const x=worldWidth()*(far?.82:.10)+camX*(far?.34:.16);ctx.drawImage(im,...c,x-w/2,y-h/2,w,h);}
 else for(let i=0;i<3;i++)ctx.drawImage(im,...c,i*(worldWidth()/3)-1,y-h/2,w,h);
 ctx.restore();AD20.draws.curtain=(AD20.draws.curtain||0)+1;AD20.curtainFrame=f;
}
function ad20Scene(b,theme,wire=false){const t=b._r30.clock||0;
 if(theme==='void')return AD20.base.arena.call(this,b);
 const a=AD20_ART.arenas[theme],left=camLeftX(),top=viewTopY(),w=viewW(),h=viewH();
 ctx.save();ctx.fillStyle=theme==='lava'?'#16070c':'#03050d';ctx.fillRect(left-24,top-24,w+48,h+48);
 if(theme==='lava')ad20Floor(t,wire);
 ad20Plate(wire?a.wire:a.terrain,wire?.8:1);
 if(!wire){
  // Far clouds and near data dust have different travel/depth; solid terrain
  // never re-centres on the pilot or follows lateral input.
  if(theme==='sky')for(let i=0;i<2;i++){
   const key=SG20_CLOUDS[(Math.floor(t*2)+i*3)%6];if(!XART.rdy(key))continue;
   const im=XART.get(key),size=270;ctx.save();ctx.globalAlpha*=.10;
   ctx.drawImage(im,worldWidth()*(i?.8:.18)+camX*.20-size/2,top+((t*13+i*h*.55)%(h+size))-size,size,size);ctx.restore();
  }
  ad20Curtain(t*.25,top+((t*7+h*.26)%(h+270))-135,.045,'far');
  ad20Curtain(t*.65,top+h*.57+Math.sin(t*.23)*18,.08,true);
 }
 ctx.restore();return true;
}
function ad20Clip(y,height,draw){if(height<=0)return;ctx.save();ctx.beginPath();ctx.rect(camLeftX()-24,y,viewW()+48,height);ctx.clip();draw();ctx.restore();}
function ad20Arena(b){if(!ad20Live(b))return AD20.base.arena.apply(this,arguments);
 const N=b._r30.v18,S=b._r30,T=N.arenaDownload,theme=ad20Theme(N.form),top=viewTopY(),h=viewH();
 if(!T||!['v18formOut','v18formIn'].includes(S.mode)){
  if(theme==='void'){const out=AD20.base.arena.apply(this,arguments);AD20.last={theme:'void',mode:'native',form:N.form,t:S.clock};return out;}
  ad20Scene(b,theme);N.arenaCurrent=theme;AD20.last={theme,mode:'fight',form:N.form,t:S.clock,
   layers:{terrain:0,farCloud:S.clock*13,nearData:S.clock*.65}};
 }else{
  const outgoing=S.mode==='v18formOut',u=clamp(S.t/(outgoing?1.45:1.6),0,1),v=v19Ease(u),cut=top+h*v;
  ctx.save();ctx.fillStyle='#02030a';ctx.fillRect(camLeftX()-24,top-24,viewW()+48,h+48);ctx.restore();
  if(outgoing){
   ad20Scene(b,T.to,true);
   ad20Clip(cut,top+h-cut+24,()=>ad20Scene(b,T.from));
  }else{
   ad20Scene(b,T.to,true);
   ad20Clip(top-24,cut-top+24,()=>ad20Scene(b,T.to));
  }
  ad20Curtain(S.clock,cut,Math.sin(Math.PI*u)*.8+.15);
  AD20.last={theme:T.to,from:T.from,mode:outgoing?'erase':'build',form:N.form,u,cut,t:S.clock};
 }
 j3State(b).aa5ArenaDrawn=true;return true;
}
v17ArenaDraw=ad20Arena;aa5ArenaDraw=ad20Arena;
window.BOF_ARENA_DOWNLOAD=AD20;
