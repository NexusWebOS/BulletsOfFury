"use strict";
/* One muzzle per physical emitter; generated cold breath and acceleration feedback. */
XART._src.ice_breath_0927=PILOT_FEEDBACK_ART.path;
XART.rdy('ice_breath_0927');
const PF27_LANCES=new Map(),PF27_TAILS=new Map();
function pf27IceBreathDraw(f){
  if(!XART.rdy('ice_breath_0927'))return false;
  const d=PILOT_FEEDBACK_ART,t=f.anim||0,fi=Math.floor(t*d.fps)%d.frames.length,r=d.frames[fi];
  const h=(f.bot-f.top)*FLAME_ICE_H,w=flameHalfW(clamp(f.lv||1,1,5),1)*2*FLAME_ICE_W;
  const sx=w/d.widthPixels,sy=h/d.reachPixels;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalCompositeOperation='source-over';ctx.globalAlpha=.9;
  ctx.drawImage(XART.get('ice_breath_0927'),r[0],r[1],r[2],r[3],f.x-r[4]*sx,f.bot-r[5]*sy,r[2]*sx,r[3]*sy);ctx.restore();
  // The plume includes its own ignition root. No second flare over the same nozzle.
  return true;
}
function pf27LanceArt(shapeLevel,colorLevel){
  if(!XART.rdy('mav_lances_0919'))return null;
  const lv=clamp(shapeLevel||1,1,5),color=clamp(colorLevel||lv,1,5),id=lv+':'+color;
  if(PF27_LANCES.has(id))return PF27_LANCES.get(id);
  const r=[[18,465,173,415],[280,345,220,515],[590,160,220,710],[920,45,280,810],[1275,4,342,920]][lv-1];
  const c=document.createElement('canvas');c.width=r[2];c.height=r[3];const g=c.getContext('2d');g.drawImage(XART.get('mav_lances_0919'),...r,0,0,c.width,c.height);
  // Keep dark outlines, white highlights and alpha; only the colored energy changes hue.
  const im=g.getImageData(0,0,c.width,c.height),a=im.data,hue=[30,216,136,0,3][color-1],sat=color===4?0:.90;
  const H=hue/60,hh=Math.floor(H),f=H-hh;
  for(let i=0;i<a.length;i+=4){if(!a[i+3])continue;const max=Math.max(a[i],a[i+1],a[i+2]),min=Math.min(a[i],a[i+1],a[i+2]);if(max-min<18||max<36)continue;
    const v=max,ss=sat*Math.min(1,(max-min)/Math.max(1,max)*1.3),p=v*(1-ss),q=v*(1-ss*f),t=v*(1-ss*(1-f));
    const rgb=[[v,t,p],[q,v,p],[p,v,t],[p,q,v],[t,p,v],[v,p,q]][hh%6];a[i]=rgb[0];a[i+1]=rgb[1];a[i+2]=rgb[2];}
  g.putImageData(im,0,0);PF27_LANCES.set(id,c);return c;
}
function pf27ThrustTick(p,dt,mvx,mvy,rolling){
  const moving=!!(mvx||mvy),target=p.dead||p.out?0:p._chgDash||p._boost?1:rolling?.65:moving?(mvy<0?1:mvy>0?.38:.70):0;
  const old=p._thrustPower||0;p._thrustPower=old+(target-old)*(1-Math.exp(-dt*(target>old?13:7)));
  if(p._thrustPower<.005)p._thrustPower=0;
}
function pf27ThrustPower(){return clamp(player?._thrustPower||0,0,1);}
function pf27TailParts(key){
  const base=String(key).replace(/_g[12]$/,''),frames=d27ShipFrames(base);if(!frames)return null;
  const id=base+':'+(typeof lizzieSkinOn!=='undefined'&&lizzieSkinOn?1:0);if(PF27_TAILS.has(id))return PF27_TAILS.get(id);
  const hi=D27_RAW_GET(base+'_g1'),lo=D27_RAW_GET(base+'_g2'),w=hi.width,h=hi.height,c=document.createElement('canvas');c.width=w;c.height=h;
  const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(hi,0,0);const a=g.getImageData(0,0,w,h).data;g.clearRect(0,0,w,h);g.drawImage(lo,0,0);const b=g.getImageData(0,0,w,h).data;
  const columns=new Map();for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=(y*w+x)*4;if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]){const v=columns.get(x)||{top:y,bottom:y};v.top=Math.min(v.top,y);v.bottom=Math.max(v.bottom,y);columns.set(x,v);}}
  const groups=[];for(const [x,bounds]of [...columns].sort((a,b)=>a[0]-b[0])){let q=groups[groups.length-1];if(!q||x-q.right>3){q={left:x,right:x,top:bounds.top,bottom:bounds.bottom};groups.push(q);}else{q.right=x;q.top=Math.min(q.top,bounds.top);q.bottom=Math.max(q.bottom,bounds.bottom);}}
  const parts=groups.filter(q=>q.bottom-q.top>3).map(q=>({x:Math.max(0,q.left-1),y:q.top,w:Math.min(w,q.right+2)-Math.max(0,q.left-1),h:Math.min(h,q.bottom+2)-q.top}));
  const result={base,w,h,parts};PF27_TAILS.set(id,result);return result;
}
function pf27PlaneThrustDraw(g,key,x,y,w,h,power){
  const p=clamp(power==null?pf27ThrustPower():power,0,1);if(p<.025)return false;
  const t=pf27TailParts(key);if(!t)return false;const frame=d27ShipFrame(t.base,Math.floor(performance.now()/(55-p*23)));
  g.save();g.imageSmoothingEnabled=false;g.globalCompositeOperation='source-over';g.globalAlpha=1;
  for(const r of t.parts){const dw=r.w*w/t.w*(1+.20*p),dh=r.h*h/t.h*(1+3.2*p),px=x-w/2+(r.x+r.w/2)*w/t.w,py=y-h/2+r.y*h/t.h;
    g.drawImage(frame,r.x,r.y,r.w,r.h,px-dw/2,py,dw,dh);
    g.globalCompositeOperation='lighter';g.globalAlpha=p*.25;g.drawImage(frame,r.x,r.y,r.w,r.h,px-dw/2,py,dw,dh);g.globalCompositeOperation='source-over';g.globalAlpha=1;}
  g.restore();return true;
}
const PF27_SPACE_ROOTS=new WeakMap();
function pf27SpacePlumeDraw(g,im,x,y,w,h,power){
  const p=clamp(power==null?pf27ThrustPower():power,0,1);
  if(p<.025){g.drawImage(im,x,y,w,h);return;}
  let top=PF27_SPACE_ROOTS.get(im);
  if(top==null){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const cx=c.getContext('2d');cx.drawImage(im,0,0);const a=cx.getImageData(0,0,c.width,c.height).data;
    top=0;find:for(let yy=0;yy<c.height;yy++)for(let xx=0;xx<c.width;xx++)if(a[(yy*c.width+xx)*4+3]>32){top=yy;break find;}PF27_SPACE_ROOTS.set(im,top);}
  const dh=(im.height-top)*h/im.height*(1+1.45*p),dy=y+top*h/im.height;
  g.save();g.drawImage(im,0,top,im.width,im.height-top,x,dy,w,dh);g.globalAlpha*=.2*p;g.drawImage(im,0,top,im.width,im.height-top,x,dy,w,dh);g.restore();
}
