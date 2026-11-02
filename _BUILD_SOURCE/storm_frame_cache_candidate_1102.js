/* QA candidate: copy actual source cells once; never rotate or change pixels. */
FB112.cells=new Map();FB112.cellBytes=0;
function fb112Cell(B,n){
 const key=B.key+':'+n;let c=FB112.cells.get(key);
 if(c){FB112.cells.delete(key);FB112.cells.set(key,c);return c;}
 c=document.createElement('canvas');c.width=c.height=B.cell;
 c.getContext('2d',{willReadFrequently:true}).drawImage(XART.get(B.key),n%B.cols*B.cell,Math.floor(n/B.cols)*B.cell,B.cell,B.cell,0,0,B.cell,B.cell);
 const bytes=B.cell*B.cell*4;while(FB112.cellBytes+bytes>64*1024*1024&&FB112.cells.size){const old=FB112.cells.keys().next().value,drop=FB112.cells.get(old);FB112.cellBytes-=drop.width*drop.height*4;FB112.cells.delete(old);}
 FB112.cells.set(key,c);FB112.cellBytes+=bytes;return c;
}
fb112Blit=function(name,f,x,y,k=1,a=Math.PI/2,flash=false,alpha=1){
 const B=FB112_ART.banks[name];if(!B||!XART.rdy(B.key))return false;
 const n=clamp(f|0,0,B.frames-1)*B.dirs+(B.dirs>1?fb112Dir(a,B.dirs):0),s=B.cell*k;
 ctx.save();ctx.globalAlpha*=alpha;ctx.drawImage(fb112Cell(B,n),x-s/2,y-s/2,s,s);ctx.restore();return true;
};
