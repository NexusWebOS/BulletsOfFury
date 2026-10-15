"use strict";
/* PIXEL GLOW (1015). Mike: "pixel glow should occur instead of overlayed graphics like our stage 5
   boss's middle core. I know the game needs this enhancement in alot of places."

   A pasted glow (an effect cell over the chest, a radial disc, a blurred halo) has its own silhouette
   and grid, so it reads as a sticker on the hull. Pixel glow lights the art's OWN emissive pixels and
   spills that light one to four pixels past them in hard steps. _BUILD_SOURCE/pixel_glow_1015.py bakes,
   per source sheet, a GLOW companion (every lit pixel + 3 hard rings) and a CORE companion (each pose's
   chest core + 4 rings), both the same size and layout as the source.

   HOW IT ATTACHES: one hook on ctx.drawImage. When a registered sheet is blitted while a driver is live,
   its companions are redrawn with the SAME source and destination rectangles under 'lighter', so the
   light cannot drift off the panels it belongs to and no draw site needs editing. A sheet is recognised
   by its pixel size (each registered sheet's size is unique), or by a tag on the per-frame tint canvases
   hammerArchFrame caches - XART.get is not a stable object (CLAUDE.md), so identity is never used for it.
   Brightness walks five fixed steps (PXG_STEPS) on the game clock, the 16-bit palette-cycle look, never a
   smooth fade. Nothing reads pixels at runtime (file:// taints the canvas).

   TO ADD A SHEET: add a row to SHEETS in the baker, run it, then give the owner a driver (pxgDrive).
   Drivers are scoped: outside a driver window the sheets draw exactly as before. */
const PXG_STEPS=[0,.16,.32,.52,.74,.95];
const PXG_TINT={blue:'#3aa6ff',red:'#ff3a2a'};
const PXG={version:1,draws:0,log:{},active:null,bySize:new Map(),tags:new WeakMap(),drawing:false,
 base:{arch:hammerArchFrame,draw:hammerBossDraw,effect:archEffectBlit,init:hammerBossInit,load:stageLoadBegin}};
for(const key in PXG_SHEETS){const S=PXG_SHEETS[key];
 XART._src['pxg_'+key+'_glow']=S.glow;XART._src['pxg_'+key+'_core']=S.core;
 if(!S.loose)PXG.bySize.set(S.size[0]+'x'+S.size[1],key);}
/* loose per-frame plates share one size, so they are known by the key they were fetched under */
PXG.base.get=XART.get;
XART.get=function(k){const im=PXG.base.get.apply(this,arguments);if(im&&typeof im==='object'&&PXG_SHEETS[k])PXG.tags.set(im,{key:k,frame:0});return im;};
function pxgKeys(){return Object.keys(PXG_SHEETS).flatMap(k=>['pxg_'+k+'_glow','pxg_'+k+'_core']);}
function pxgWarm(){for(const k of pxgKeys())XART.rdy(k);}
/* quantise a 0..1 drive onto the fixed brightness ladder */
function pxgStep(x){return PXG_STEPS[Math.max(0,Math.min(PXG_STEPS.length-1,Math.round(clamp(x,0,1)*(PXG_STEPS.length-1))))];}

/* the hook: a registered sheet just landed - put its own light back on top, same rects */
function pxgAfterBlit(g,im,a){
 const A=PXG.active;if(!A||PXG.drawing||!im)return;
 const n=a.length;let key=null,fx=0,fy=0,fw=0,fh=0;
 const tag=PXG.tags.get(im);
 if(tag){key=tag.key;const S=PXG_SHEETS[key];if(!S)return;fw=im.width;fh=im.height;fx=tag.frame*fw;fy=0;
  if(n>=9){fx+=a[1];fy+=a[2];fw=a[3];fh=a[4];}}
 else{key=PXG.bySize.get(im.width+'x'+im.height);if(!key)return;
  if(n>=9){fx=a[1];fy=a[2];fw=a[3];fh=a[4];}else{fw=im.width;fh=im.height;}}
 const dx=n>=9?a[5]:a[1],dy=n>=9?a[6]:a[2],dw=n>=9?a[7]:n>=5?a[3]:fw,dh=n>=9?a[8]:n>=5?a[4]:fh;
 const layers=[['glow',pxgStep(A.lights)],['core',pxgStep(A.core)]];
 PXG.drawing=true;
 try{for(const [layer,alpha] of layers){if(alpha<=0)continue;const k='pxg_'+key+'_'+layer;if(!XART.rdy(k))continue;
   /* a recoloured pose (blue charge, red rage) takes a luminance-kept recolour of its own light;
      a white hit-flash pose needs no extra light at all */
   if(tag&&tag.tint==='white')continue;
   const gi=(tag&&PXG_TINT[tag.tint]&&typeof xartPalette==='function'&&xartPalette(k,PXG_TINT[tag.tint]))||XART.get(k);g.save();g.globalCompositeOperation='lighter';g.globalAlpha=alpha*(A.alpha==null?1:A.alpha);g.imageSmoothingEnabled=false;
   PXG.raw.call(g,gi,fx,fy,fw,fh,dx,dy,dw,dh);g.restore();PXG.draws++;PXG.log[k]=(PXG.log[k]||0)+1;}}
 finally{PXG.drawing=false;}
}
function pxgInstall(){
 if(typeof ctx==='undefined'||!ctx||ctx.__pxg)return;
 PXG.raw=ctx.drawImage;
 const raw=PXG.raw;
 ctx.drawImage=function(im){const r=raw.apply(this,arguments);if(PXG.active)pxgAfterBlit(this,im,arguments);return r;};
 ctx.__pxg=true;
}
pxgInstall();

/* tag hammerArchFrame's cached per-frame tint canvases so a tinted pose still finds its frame */
hammerArchFrame=function(key,frame,tint){const q=PXG.base.arch.apply(this,arguments);
 if(q&&tint&&q.im&&q.im!==XART.get('arch_'+key)&&PXG_SHEETS['arch_'+key]){const n=ARCH_FRAMES[key]||1;PXG.tags.set(q.im,{key:'arch_'+key,frame:clamp(frame|0,0,n-1),tint});}
 return q;};

/* ---- the Stage 5 Chrome Hammer driver ------------------------------------------------------------
   Idle: the core breathes slowly through the low steps and the panel lights hold a low step.
   Charging (core convergence, eradication charge, spell, rage): the core climbs the ladder and beats
   faster, and the panels follow it - the light comes up from inside the armour instead of an effect
   cell being pasted on his chest. A hit drives both to the top step for the flash. */
const PXG_HAMMER_CHARGE={core_orbit:2.15,mega_charge:1.65,spell:1.4,spell_blast:1.35,enrage:2.15,storm_charge:1.2,fr_activation:1.6};
function pxgHammerDrive(b){const h=b&&b._hammer;if(!h)return null;
 const t=typeof stateT==='number'?stateT:0,dur=PXG_HAMMER_CHARGE[h.state];
 let core,lights;
 if(h.state==='mega_beam'){core=1;lights=.8;}
 else if(dur){const k=clamp((h.t||0)/dur,0,1),beat=.5+.5*Math.sin(t*(5+9*k));core=.45+.45*k+.10*beat;lights=.25+.45*k+.08*beat;}
 else{const beat=.5+.5*Math.sin(t*2.6);core=.30+.22*beat;lights=.20+.06*beat;}
 if(b.flash>0){core=1;lights=Math.max(lights,.7);}
 if(b.dead){const f=clamp(1-(b.dying||0)/1.6,0,1);core*=f;lights*=f;}
 return{core,lights};}
hammerBossDraw=function(b){const prev=PXG.active;PXG.active=(b&&b._hammer)?pxgHammerDrive(b):null;PXG.hammer=b;
 try{return PXG.base.draw.apply(this,arguments);}finally{PXG.active=prev;PXG.hammer=null;}};
/* the core convergence used to paste effect cell 6 over his chest; the chest now lights from inside */
archEffectBlit=function(cell,x,y,size,rot,alpha){const b=PXG.hammer;
 if(b&&cell===6&&b._hammer&&b._hammer.state==='core_orbit'&&Math.abs(x-b.x)<1&&PXG_SHEETS.arch_chaingun_break_enrage&&XART.rdy('pxg_arch_chaingun_break_enrage_core')){PXG.log.suppressedCorePaste=(PXG.log.suppressedCorePaste||0)+1;return true;}
 return PXG.base.effect.apply(this,arguments);};
hammerBossInit=function(b){const r=PXG.base.init.apply(this,arguments);pxgWarm();return r;};
stageLoadBegin=function(n,keys){return PXG.base.load.call(this,n,[...(keys||[]),...(n===5?pxgKeys():[])]);};
