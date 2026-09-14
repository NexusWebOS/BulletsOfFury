/* Shared authored comm plate: only cyan trim changes; steel and text seat stay neutral. */
function dialogueFrame(who,tint){
  const key='dlg_rect_0914';
  if(!XART.rdy(key))return null;
  const pilot=PILOTS.find(p=>p.key===String(who||'').toLowerCase()) || PILOTS.find(p=>p.key===run.pilot);
  const col=(pilot&&pilot.tint)||tint||'#63cfff';
  const cache=dialogueFrame.cache||(dialogueFrame.cache={});
  if(cache[col])return cache[col];
  const im=XART.get(key),cv=document.createElement('canvas');
  cv.width=im.naturalWidth||im.width;cv.height=im.naturalHeight||im.height;
  const g=cv.getContext('2d');g.drawImage(im,0,0);
  const data=g.getImageData(0,0,cv.width,cv.height),d=data.data,c=hx(col);
  const peak=Math.max(...c,1);
  for(let i=0;i<d.length;i+=4){
    const r=d[i],green=d[i+1],b=d[i+2];
    if(d[i+3]&&b>r*1.35&&green>r*1.25&&b-r>25){
      const light=Math.max(r,green,b)/peak;
      d[i]=Math.min(255,c[0]*light);d[i+1]=Math.min(255,c[1]*light);d[i+2]=Math.min(255,c[2]*light);
    }
  }
  g.putImageData(data,0,0);cache[col]=cv;return cv;
}
function dialogueFrameDraw(who,tint,x,y,w,h){
  const im=dialogueFrame(who,tint);
  if(!im)return false;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x,y,w,h);ctx.restore();return true;
}
