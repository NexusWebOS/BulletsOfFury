"use strict";
/* PIXEL GLOW (1015). Mike: "pixel glow should occur instead of overlayed graphics like our stage 5
   boss's middle core. I know the game needs this enhancement in alot of places." Then: "only do this
   for enemies and frames we're actually using please. Do a pass for levels 1-9."

   A pasted glow (an effect cell over the chest, a radial disc, a blurred halo) has its own silhouette
   and grid, so it reads as a sticker on the hull. Pixel glow lights the art's OWN emissive pixels and
   spills that light one to three pixels past them in hard steps. _BUILD_SOURCE/pixel_glow_1015.py bakes,
   per source image, a GLOW companion (lit pixels + hard rings) the same size and layout as the source,
   and for the Stage 5 Hammer also a CORE companion (each pose's chest core). Only images the stage-1..9
   survey (probe_glow_usage_1015.py) saw drawn inside drawEnemy / drawSubBoss / drawBoss are baked, and
   on a sheet only the frames that were actually drawn carry any light.

   HOW IT ATTACHES: one hook on ctx.drawImage. When a registered image lands while a driver is live, its
   companion is redrawn with the SAME source and destination rectangles under 'lighter'.
   WHICH IMAGE IS WHICH: XART.get is not a stable object and a cell canvas has no .src (CLAUDE.md), and
   most units are drawn from DERIVED canvases - a crop cut out of a sheet into a module's own cache
   (mr27Cell, hammerArchFrame) or an xartPalette recolour. So every image XART hands out is tagged with
   its key, and the tag follows it through every offscreen copy: drawing a tagged image into another
   canvas tags that canvas with the key and the source rectangle it came from, and a 'color'/'source-in'
   fill over it records the tint. At draw time the source rect maps back to the key's own pixels, so the
   right frame of the right sheet lights, recoloured to the pose's tint (a white hit flash or a black camo
   pass takes no light). Nothing reads pixels at runtime (file:// taints the canvas).
   Brightness walks six fixed steps (PXG_STEPS) on the game clock, the 16-bit palette-cycle look, never a
   smooth fade. Outside a driver window everything draws exactly as before. */
const PXG_STEPS=[0,.16,.32,.52,.74,.95];
const PXG={version:2,draws:0,log:{},active:null,tags:new WeakMap(),phase:new WeakMap(),phaseN:0,drawing:false,
 base:{draw:hammerBossDraw,effect:archEffectBlit,init:hammerBossInit,load:stageLoadBegin,enemy:drawEnemy,sub:drawSubBoss,boss:drawBoss}};
for(const key in PXG_SHEETS){const S=PXG_SHEETS[key];
 XART._src['pxg_'+key+'_glow']=S.glow;if(S.core)XART._src['pxg_'+key+'_core']=S.core;}
function pxgKeys(stage){const out=[];for(const k in PXG_SHEETS){const S=PXG_SHEETS[k];
  if(stage!=null&&S.st&&S.st.indexOf(stage)<0)continue;out.push('pxg_'+k+'_glow');if(S.core)out.push('pxg_'+k+'_core');}return out;}
function pxgWarm(stage){for(const k of pxgKeys(stage))XART.rdy(k);}
/* quantise a 0..1 drive onto the fixed brightness ladder */
function pxgStep(x){return PXG_STEPS[Math.max(0,Math.min(PXG_STEPS.length-1,Math.round(clamp(x,0,1)*(PXG_STEPS.length-1))))];}

/* ---- tags: key + the key-space rectangle an image (or a canvas copied from it) shows ---------- */
PXG.base.touch=XART._touch;
XART._touch=function(k){const im=PXG.base.touch.apply(this,arguments);
 /* a cell canvas is cut from its sheet (which tags it with the SHEET); the cell's own key wins */
 if(im&&typeof im==='object'&&(!PXG.tags.has(im)||(window.BOFX&&((BOFX.cells&&BOFX.cells[k])||(BOFX.playercells&&BOFX.playercells[k])))&&PXG.tags.get(im).key!==k))PXG.tags.set(im,{key:k,ax:1,bx:0,ay:1,by:0,vx0:0,vy0:0,vx1:1e9,vy1:1e9});
 return im;};
function pxgWH(im){return [im.naturalWidth||im.width||0,im.naturalHeight||im.height||0];}
/* an offscreen copy: carry the tag across (only for plain copies - no rotation, no mirror) */
function pxgCarry(g,im,a){
 const t=PXG.tags.get(im);if(!t)return;const c=g.canvas;if(!c||c===(typeof canvas!=='undefined'?canvas:null))return;
 const op=g.globalCompositeOperation;if(op!=='source-over'&&op!=='copy'&&op!=='destination-in'&&op!=='source-in'&&op!=='source-atop')return;
 const m=g.getTransform();if(m.b||m.c||m.a<=0||m.d<=0)return;
 const n=a.length,[iw,ih]=pxgWH(im);
 let sx=0,sy=0,sw=iw,sh=ih,dx,dy,dw,dh;
 if(n>=9){sx=a[1];sy=a[2];sw=a[3];sh=a[4];dx=a[5];dy=a[6];dw=a[7];dh=a[8];}
 else{dx=a[1];dy=a[2];dw=n>=5?a[3]:iw;dh=n>=5?a[4]:ih;}
 if(!(sw>0&&sh>0&&dw>0&&dh>0))return;
 /* device-space dest of the copy on canvas c */
 const DX=m.a*dx+m.e,DY=m.d*dy+m.f,DW=m.a*dw,DH=m.d*dh;
 const old=PXG.tags.get(c);
 /* key coords of the copied source rect, through the source's own map */
 const kx0=t.ax*sx+t.bx,ky0=t.ay*sy+t.by,kx1=t.ax*(sx+sw)+t.bx,ky1=t.ay*(sy+sh)+t.by;
 const ax=(kx1-kx0)/DW,ay=(ky1-ky0)/DH;
 const tag={key:t.key,ax,bx:kx0-ax*DX,ay,by:ky0-ay*DY,vx0:Math.max(kx0,t.vx0),vy0:Math.max(ky0,t.vy0),vx1:Math.min(kx1,t.vx1),vy1:Math.min(ky1,t.vy1),tint:t.tint};
 if(old&&old.key!==t.key){PXG.tags.set(c,{key:null});return;}
 if(old&&old.key&&op!=='source-over')return;       /* a mask pass over the same art keeps the first map */
 PXG.tags.set(c,old&&old.tint&&!tag.tint?Object.assign(tag,{tint:old.tint}):tag);
}
function pxgTint(g){const c=g.canvas,t=c&&PXG.tags.get(c);if(!t||!t.key)return;
 const op=g.globalCompositeOperation;if(op!=='color'&&op!=='source-in'&&op!=='source-atop'&&op!=='multiply'&&op!=='hue')return;
 const f=g.fillStyle;if(typeof f!=='string')return;if(t.tint)return;t.tint=f;}
(function(){const P=CanvasRenderingContext2D.prototype,di=P.drawImage,fr=P.fillRect;
 P.drawImage=function(im){const r=di.apply(this,arguments);if(im)try{pxgCarry(this,im,arguments);}catch(e){}return r;};
 P.fillRect=function(){const r=fr.apply(this,arguments);try{pxgTint(this);}catch(e){}return r;};})();
/* the tint a companion should take: white (hit flash) and dark (camo multiply) add no light at all */
function pxgTintHex(t){if(!t)return '';const m=/^#([0-9a-f]{6})$/i.exec(t);if(!m)return 'skip';
 const v=parseInt(m[1],16),r=v>>16&255,g=v>>8&255,b=v&255,mx=Math.max(r,g,b),mn=Math.min(r,g,b);
 if(mx<90)return 'skip';if(mx>215&&(mx-mn)<40)return 'skip';return t;}

/* ---- the hook: a registered image just landed - put its own light back on top, same rects ----- */
function pxgAfterBlit(g,im,a){
 const A=PXG.active;if(!A||PXG.drawing||!im)return;
 const tag=PXG.tags.get(im);if(!tag||!tag.key)return;const S=PXG_SHEETS[tag.key];if(!S)return;
 const tint=pxgTintHex(tag.tint);if(tint==='skip')return;
 const n=a.length,[iw,ih]=pxgWH(im);
 let sx=0,sy=0,sw=iw,sh=ih,dx,dy,dw,dh;
 if(n>=9){sx=a[1];sy=a[2];sw=a[3];sh=a[4];dx=a[5];dy=a[6];dw=a[7];dh=a[8];}
 else{dx=a[1];dy=a[2];dw=n>=5?a[3]:iw;dh=n>=5?a[4]:ih;}
 if(!(sw>0&&sh>0))return;
 /* source rect -> key space, clipped to the part of the key this image really shows */
 let kx0=tag.ax*sx+tag.bx,ky0=tag.ay*sy+tag.by,kx1=tag.ax*(sx+sw)+tag.bx,ky1=tag.ay*(sy+sh)+tag.by;
 const cx0=Math.max(kx0,tag.vx0,0),cy0=Math.max(ky0,tag.vy0,0),cx1=Math.min(kx1,tag.vx1,S.size[0]),cy1=Math.min(ky1,tag.vy1,S.size[1]);
 if(cx1-cx0<1||cy1-cy0<1)return;
 const fx=dw/(kx1-kx0),fy=dh/(ky1-ky0);
 const ddx=dx+(cx0-kx0)*fx,ddy=dy+(cy0-ky0)*fy,ddw=(cx1-cx0)*fx,ddh=(cy1-cy0)*fy;
 const m=g.getTransform(),scale=Math.hypot(m.a,m.b)*Math.abs(fx);
 const layers=[['glow',pxgStep(A.lights)],['core',S.core?pxgStep(A.core):0]];
 PXG.drawing=true;
 try{for(const [layer,alpha] of layers){if(alpha<=0)continue;const k='pxg_'+tag.key+'_'+layer;if(!XART.rdy(k))continue;
   const gi=(tint&&typeof xartPalette==='function'&&xartPalette(k,tint))||XART.get(k);
   const ga=g.globalAlpha;g.save();g.globalCompositeOperation='lighter';g.globalAlpha=alpha*(A.alpha==null?1:A.alpha)*ga;
   /* companions are stored pre-reduced to their draw size (S.n); anything still reduced is smoothed, not speckled */
   g.imageSmoothingEnabled=scale*(S.n||1)<0.6;
   const q=S.n||1;PXG.raw.call(g,gi,cx0/q,cy0/q,(cx1-cx0)/q,(cy1-cy0)/q,ddx,ddy,ddw,ddh);g.restore();PXG.draws++;PXG.log[k]=(PXG.log[k]||0)+1;}}
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

/* ---- drivers -------------------------------------------------------------------------------------
   Ordinary units, minibosses and bosses: the lights hold a low step and breathe slowly, each unit on its
   own phase so a formation never pulses in lockstep; a hit drives them to the top step for the flash, and
   a dying unit's light goes out with it. */
function pxgPhase(u){let p=PXG.phase.get(u);if(p==null){p=(PXG.phaseN++*2.399)%6.283;PXG.phase.set(u,p);}return p;}
function pxgUnitDrive(u,boss){if(!u)return null;
 const t=typeof stateT==='number'?stateT:0,beat=.5+.5*Math.sin(t*(boss?1.7:2.2)+pxgPhase(u));
 let lights=(boss?.34:.30)+.24*beat;
 if((u.flash||0)>0||(u.hitFlash||0)>0)lights=1;
 if(u.dead||u._dyingT!=null){const f=u._dyingT!=null?clamp(1-u._dyingT/.5,0,1):clamp(1-(u.dying||0)/1.6,0,1);lights*=f;}
 return {lights,core:lights};}
function pxgWindow(drive,fn,self,args){const prev=PXG.active;PXG.active=drive;try{return fn.apply(self,args);}finally{PXG.active=prev;}}
drawEnemy=function(e){return pxgWindow(pxgUnitDrive(e,false),PXG.base.enemy,this,arguments);};
drawSubBoss=function(){return pxgWindow(typeof subBoss!=='undefined'?pxgUnitDrive(subBoss,true):null,PXG.base.sub,this,arguments);};
drawBoss=function(){return pxgWindow(typeof boss!=='undefined'?pxgUnitDrive(boss,true):null,PXG.base.boss,this,arguments);};

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
hammerBossDraw=function(b){const prev=PXG.active;PXG.active=(b&&b._hammer)?pxgHammerDrive(b):prev;PXG.hammer=b;
 try{return PXG.base.draw.apply(this,arguments);}finally{PXG.active=prev;PXG.hammer=null;}};
/* the core convergence used to paste effect cell 6 over his chest; the chest now lights from inside */
archEffectBlit=function(cell,x,y,size,rot,alpha){const b=PXG.hammer;
 if(b&&cell===6&&b._hammer&&b._hammer.state==='core_orbit'&&Math.abs(x-b.x)<1){PXG.log.suppressedCorePaste=(PXG.log.suppressedCorePaste||0)+1;return true;}
 return PXG.base.effect.apply(this,arguments);};
hammerBossInit=function(b){const r=PXG.base.init.apply(this,arguments);pxgWarm(5);return r;};
stageLoadBegin=function(n,keys){return PXG.base.load.call(this,n,[...(keys||[]),...pxgKeys(n)]);};
