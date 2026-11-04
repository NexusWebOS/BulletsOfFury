"use strict";
/* Stage7-only lossless atlas pages. Stable original cell/pivot/destination;
   transparent borders are represented as offsets, with no art downsampling. */
const S7P113={base:{v31:v31Blit,r46:r46Blit,load:stageLoadBegin,begin:beginStage},draws:0,misses:0,cells:new Map(),bytes:0,budget:48*1024*1024};
for(const [key,p]of Object.entries(S7P113_ART.pages))XART._src[key]=p.path;
function s7p113Draw(key,index,x,y,size,tint,alpha,registered){
 const B=S7P113_ART.banks[key],r=B.cells[index];if(!r)return true;
 const [page,sx,sy,w,h,ox,oy]=r,k=B.pages[page];if(!XART.rdy(k)){S7P113.misses++;return false;}
 // Restore the original transparent cell before minification. This preserves
 // nearest-neighbour sampling at fractional destinations exactly; trimmed
 // destination rectangles shift a few edge samples in Chromium.
 const id=key+':'+index+':'+(tint||'')+':'+(registered?'in':'atop');let im=S7P113.cells.get(id);
 if(im){S7P113.cells.delete(id);S7P113.cells.set(id,im);}
 else{
  im=document.createElement('canvas');im.width=im.height=B.cell;const g=im.getContext('2d');g.imageSmoothingEnabled=false;
  g.drawImage(XART.get(k),sx,sy,w,h,ox,oy,w,h);
  // Same native hit/shadow tint operation as the corresponding old blitter.
  if(tint){g.globalCompositeOperation=registered?'source-in':'source-atop';g.fillStyle=tint;g.fillRect(0,0,B.cell,B.cell);}
  S7P113.cells.set(id,im);S7P113.bytes+=B.cell*B.cell*4;
  while(S7P113.bytes>S7P113.budget&&S7P113.cells.size>1){const [oldKey,cell]=S7P113.cells.entries().next().value;S7P113.cells.delete(oldKey);S7P113.bytes-=cell.width*cell.height*4;}
 }
 const old=R46.painting;
 if(registered)R46.painting=true;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 try{ctx.drawImage(im,0,0,B.cell,B.cell,x-size/2,y-size/2,size,size);S7P113.draws++;}
 finally{ctx.restore();R46.painting=old;}return true;
}
v31Blit=function(B,f,a,x,y,size,tint=null,alpha=1){
 const P=run.stage===7&&B&&S7P113_ART.banks[B.key];if(!P)return S7P113.base.v31.apply(this,arguments);
 const d=v31Dir(a,B.dirs),cols=B.cols||B.dirs,row=clamp(f|0,0,B.frames-1)*(B.dirRows||1)+Math.floor(d/cols);
 return s7p113Draw(B.key,row*P.cols+d%cols,x,y,size,tint,alpha,false);
};
r46Blit=function(M,row,a,x,y,size,tint=null,alpha=1){
 const P=run.stage===7&&M&&S7P113_ART.banks[M.key];if(!P)return S7P113.base.r46.apply(this,arguments);
 return s7p113Draw(M.key,row*P.cols+s1aDir(a,M.dirs),x,y,size,tint,alpha,true);
};
stageLoadBegin=function(n){const result=S7P113.base.load.apply(this,arguments),L=_stageLoads[n];
 if(n!==7||!L||L.cursor)return result;
 const keys=[],seen=new Set();for(const key of L.keys){const P=S7P113_ART.banks[key];for(const k of P?P.pages:[key])if(!seen.has(k)){seen.add(k);keys.push(k);}}
 L.keys=keys;L.total=keys.length;L.done=!keys.length;return L.total;
};
beginStage=function(n){S7P113.cells.clear();S7P113.bytes=0;if(n!==7&&typeof XART.releaseRoot==='function')for(const k of Object.keys(S7P113_ART.pages))XART.releaseRoot(k);return S7P113.base.begin.apply(this,arguments);};
globalThis.BOF_SEWER_PAGES_1103={state:S7P113,art:S7P113_ART};
