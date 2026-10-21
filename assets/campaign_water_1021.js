'use strict';
/* The campaign uses the approved animated blue ocean, on its own map clock.
   Stage1's terrain/biome gate and original atlas/cell registration stay intact. */
const CW21={base:{warm:cmap2Warm,ocean:cmap2DrawOcean},frame:0,draws:0};
cmap2Warm=function(){const r=CW21.base.warm.apply(this,arguments);XART.rdy(S1W20_ART.key);return r;};
function cw21Ocean(g,left,top,right,bottom,scale=1,originX=0,originY=0){
 const a=S1W20_ART;if(!XART.rdy(a.key))return false;
 const im=XART.get(a.key),c=cmap2.cam,t=cmap2.t,f=Math.floor(t*a.fps)%a.frames;
 const tile=Math.round(a.width*(.6+.4*c.z)),step=tile*scale,wrap=v=>((v%tile)+tile)%tile;
 const ox=originX-wrap(c.x*c.z*CM2_PAR_OCEAN+t*7)*scale,
  oy=originY-wrap(c.y*c.z*CM2_PAR_OCEAN+t*3)*scale;
 g.save();g.imageSmoothingEnabled=false;
 for(let y=oy+Math.floor((top-oy)/step)*step;y<bottom;y+=step)
  for(let x=ox+Math.floor((left-ox)/step)*step;x<right;x+=step)
   g.drawImage(im,...a.cells[f],x,y,step+.5,step+.5);
 g.restore();CW21.frame=f;CW21.draws++;return true;
}
cmap2DrawOcean=function(){
 const left=-campaignViewOffset(),right=VW+campaignViewOffset();
 if(!cw21Ocean(ctx,left,0,right,VH))return CW21.base.ocean.apply(this,arguments);
};
window.BOF_CAMPAIGN_WATER=CW21;
