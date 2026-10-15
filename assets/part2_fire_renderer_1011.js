"use strict";
// The game and review page draw exactly the same authored origin/body/tip.
function p2RenderFireColumn(g,art,get,x,y,angle,length,width,t,alpha=1,muzzle=true){
 if(![x,y,angle,length,width,t,alpha].every(Number.isFinite)||length<=0||width<.5)return false;
 const frame=Math.floor(Math.max(0,t)*32),a=art.fire[frame%32],root=art.fire_root[frame%16],tip=art.fire_tip[frame%16];
 const im=get(a.key),ri=muzzle&&get(root.key),ti=get(tip.key);if(!im||!ti)return false;
 const k=width/80,half=width*.75,capScale=Math.min(half*2/tip.join_width,length/(tip.join_y-tip.pivot[1]));
 const capDepth=(tip.join_y-tip.pivot[1])*capScale,bodyLength=Math.max(0,length-capDepth+8*capScale);
 const tiles=muzzle?126:127,step=Math.max(102*k,bodyLength/tiles),depth=Math.min(bodyLength,24+Math.min(106,width*.54)),r=Math.min(16,width*.11);
 const result={body:0,root:0,tip:0,muzzle:0};
 g.save();g.translate(x,y);g.rotate(angle+Math.PI/2);g.imageSmoothingEnabled=false;g.globalAlpha*=alpha;
 if(bodyLength>0){g.save();g.beginPath();
  if(muzzle){g.moveTo(-r,0);g.bezierCurveTo(-r,-depth*.25,-half,-depth*.65,-half,-depth);g.lineTo(-half,-bodyLength);
   g.lineTo(half,-bodyLength);g.lineTo(half,-depth);g.bezierCurveTo(half,-depth*.65,r,-depth*.25,r,0);g.closePath();}
  else g.rect(-half,-bodyLength,half*2,bodyLength);
  g.clip();for(let i=0,n=Math.min(tiles,Math.ceil(bodyLength/step));i<n;i++){
   g.drawImage(im,...a.body_rect,-half,-(i+1)*step,half*2,step);result.body++;}
  if(ri){const s=Math.min(.5,width/240);g.drawImage(ri,-root.pivot[0]*s,-root.pivot[1]*s,root.w*s,root.h*s);result.root++;}
  g.restore();
 }
 g.drawImage(ti,-tip.pivot[0]*capScale,-length-tip.pivot[1]*capScale,tip.w*capScale,tip.h*capScale);result.tip++;
 if(muzzle){const s=Math.max(8,Math.min(38,width*.32))/192;
  g.drawImage(im,...a.muzzle_rect,-96*s,-62*s,192*s,148*s);result.muzzle++;}
 g.restore();return result;
}
