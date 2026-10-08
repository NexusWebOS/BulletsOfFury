/* Candidate-preview palette adapter. Same masked compositing as spaceAtlasCanvas.
   Supply a resolver backed by Image or XART; never read pixels or recolor steel. */
(function(root){
  const cache=new Map();
  root.furyCandidatePalette=function(key,pilot,resolve){
    const catalog=root.FURYSHIP_CANDIDATES,frame=catalog.frames[key];
    if(!frame)return null;
    const src=resolve(frame.path);
    if(!src)return null;
    if(pilot==='axel'||!frame.paletteMask)return src;
    const pal=catalog.palettes[pilot],mask=resolve(frame.paletteMask);
    if(!pal||!mask)return null;
    const ck=key+'|'+pilot;if(cache.has(ck))return cache.get(ck);
    const c=document.createElement('canvas');c.width=frame.size[0];c.height=frame.size[1];
    const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(src,0,0);
    const m=document.createElement('canvas');m.width=c.width;m.height=c.height;
    const mg=m.getContext('2d');mg.imageSmoothingEnabled=false;mg.drawImage(mask,0,0);
    if(pal.lum>1){mg.globalCompositeOperation='lighter';mg.globalAlpha=Math.min(1,pal.lum-1);mg.drawImage(mask,0,0);mg.globalAlpha=1;}
    mg.globalCompositeOperation='multiply';mg.fillStyle=pal.color;mg.fillRect(0,0,m.width,m.height);
    mg.globalCompositeOperation='destination-in';mg.drawImage(mask,0,0);
    g.drawImage(m,0,0);cache.set(ck,c);return c;
  };
})(window);
