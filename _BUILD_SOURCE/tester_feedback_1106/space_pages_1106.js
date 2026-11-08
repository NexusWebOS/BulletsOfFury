"use strict";
/* Lossless small pages replace oversized Stage5 blits, retaining original cells,
   pivots, heading frames and visible pixels. Hit/shadow colours are authored
   pages too. Masters stay on disk; native combat and animation clocks stay owners. */
const SP116={base:{v31:v31Blit,r46:r46Blit,load:stageLoadBegin,begin:beginStage},
 cells:new Map(),bytes:0,budget:48*1024*1024,draws:0,misses:0,fallbacks:0};
for(const [key,P]of Object.entries(SP116_ART.pages))XART._src[key]=P.path;
function sp116Draw(key,index,x,y,size,tint,alpha,registered){
 const B=SP116_ART.banks[key],r=B?.cells[index];if(!r)return true;
 const [page,sx,sy,w,h,ox,oy]=r,P=B.pages[page],pk=P.variants[tint||'base'];
 if(!pk){SP116.fallbacks++;return null;}
 if(!XART.rdy(pk)){SP116.misses++;return false;}
 const id=key+':'+index+':'+(tint||'base');let im=SP116.cells.get(id);
 if(im){SP116.cells.delete(id);SP116.cells.set(id,im);}
 else{
  // Restore authored transparent padding before the native destination blit.
  // This retains Chromium's nearest-neighbour samples at fractional positions.
  im=document.createElement('canvas');im.width=im.height=B.cell;
  const g=im.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(XART.get(pk),sx,sy,w,h,ox,oy,w,h);
  SP116.cells.set(id,im);SP116.bytes+=B.cell*B.cell*4;
  while(SP116.bytes>SP116.budget&&SP116.cells.size>1){const [k,c]=SP116.cells.entries().next().value;SP116.cells.delete(k);SP116.bytes-=c.width*c.height*4;}
 }
 const prior=R46.painting;if(registered)R46.painting=true;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 try{ctx.drawImage(im,0,0,B.cell,B.cell,x-size/2,y-size/2,size,size);SP116.draws++;}
 finally{ctx.restore();R46.painting=prior;}return true;
}
v31Blit=function(B,f,a,x,y,size,tint=null,alpha=1){const P=run.stage===5&&B&&SP116_ART.banks[B.key];
 if(!P)return SP116.base.v31.apply(this,arguments);
 const d=v31Dir(a,B.dirs),cols=B.cols||B.dirs,row=clamp(f|0,0,B.frames-1)*(B.dirRows||1)+Math.floor(d/cols);
 const r=sp116Draw(B.key,row*P.cols+d%cols,x,y,size,tint,alpha,false);
 return r===null?SP116.base.v31.apply(this,arguments):r;
};
r46Blit=function(M,row,a,x,y,size,tint=null,alpha=1){const P=run.stage===5&&M&&SP116_ART.banks[M.key];
 if(!P)return SP116.base.r46.apply(this,arguments);
 const r=sp116Draw(M.key,row*P.cols+s1aDir(a,M.dirs),x,y,size,tint,alpha,true);
 return r===null?SP116.base.r46.apply(this,arguments):r;
};
stageLoadBegin=function(n){const result=SP116.base.load.apply(this,arguments),L=_stageLoads[n];
 if(n!==5||!L||L.cursor)return result;
 const keys=[],seen=new Set();
 for(const key of L.keys){
  // S511 explicitly retires Voidreaver at spawn. Keep its source on disk,
  // but do not decode an unused 89MB bank for the current orbital roster.
  if(key==='r46_af_xelite_voidreaver')continue;
  const B=SP116_ART.banks[key],items=B?B.pages.flatMap(p=>Object.values(p.variants)):[key];
  for(const k of items)if(!seen.has(k)){seen.add(k);keys.push(k);}
 }
 L.keys=keys;L.total=keys.length;L.done=!keys.length;return L.total;
};
beginStage=function(n){SP116.cells.clear();SP116.bytes=0;
 if(n!==5&&XART.releaseRoot)for(const key of Object.keys(SP116_ART.pages))XART.releaseRoot(key);
 return SP116.base.begin.apply(this,arguments);
};
globalThis.BOF_SPACE_PAGES_1106={state:SP116,art:SP116_ART};
