'use strict';
// PixelLab 24-frame sustain with authored launch/release; fixed 320x640 cells.
const C41={state:hammerState,beam:hammerChromiumDraw,active:cgActive,cache:new Map()};
XART._src.c41_wave='assets/game/shared/combat/chronos_wave_1025/wave_smooth.png';
const c41Load=stageLoadBegin;stageLoadBegin=function(n,keys){return c41Load.call(this,n,[...(keys||[]),...(n===5?['c41_wave']:[])]);};
function c41Sheet(red){if(!XART.rdy('c41_wave'))return null;const im=XART.get('c41_wave');if(!red)return im;if(!C41.cache.has('red')){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height);for(let i=0;i<d.data.length;i+=4){const r=d.data[i],b=d.data[i+2];d.data[i]=b;d.data[i+1]=r;d.data[i+2]=r;}g.putImageData(d,0,0);C41.cache.set('red',c);}return C41.cache.get('red');}
function c41Draw(from,to,t,dur,red){const im=c41Sheet(red);if(!im)return false;const f=c41Frame(t,dur);
 const length=Math.hypot(to.x-from.x,to.y-from.y),k=length/608;ctx.save();ctx.translate(from.x,from.y);ctx.rotate(Math.atan2(to.y-from.y,to.x-from.x)-Math.PI/2);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,(f%8)*320,Math.floor(f/8)*640,320,640,-160*k,-24*k,320*k,640*k);ctx.restore();return true;}
hammerChromiumDraw=function(x,y,endY,width,t,dur){if(c25Own(boss)&&boss._hammer.state==='mega_beam')return c41Draw({x,y},{x,y:endY},t,dur,false);return C41.beam.apply(this,arguments);};
c30Wave=function(b){const R=b._hammer.c30,L=c30Line(b);c41Draw(L.from,L.to,R.t,1.35,true);C30.lastBeam={...L,width:76,length:Math.hypot(L.to.x-L.from.x,L.to.y-L.from.y),frame:Math.min(7,Math.floor(R.t*14))};};
// Remove the retired multi-pillar spell from this encounter, including its warning.
hammerState=function(b,s){if(c25Own(b)&&['spell','spell_blast'].includes(s)){b._hammer.pillars=[];b._hammer.spellTargets=[];s='hammer';}return C41.state.call(this,b,s);};
// Body glow interception must never mistake a wave/effect plate for the actor.
cgActive=function(b){if(c25Own(b)&&b._hammer.state==='mega_beam')return false;if(c25Own(b)&&b._hammer.c30&&['gather','thrust','beam','recover'].includes(b._hammer.c30.phase))return false;return C41.active.apply(this,arguments);};
window.BOF_CHRONOS_WAVE=C41;

function c41Frame(t,dur){return t<.16?Math.max(0,Math.floor(t/.08)):t>=dur-.18?Math.min(27,26+Math.floor((t-dur+.18)/.09)):2+Math.floor((t-.16)*24)%24;}
function c41Hit(from,to,t,dur,p){
 const im=c41Sheet(false);if(!im)return false;
 if(!C41.mask){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);C41.mask=g.getImageData(0,0,c.width,c.height).data;}
 const dx=to.x-from.x,dy=to.y-from.y,len=Math.hypot(dx,dy),k=len/608;
 const px=p.x-from.x,py=p.y-from.y;
 const x=Math.floor(160+(px*dy-py*dx)/len/k),y=Math.floor(24+(px*dx+py*dy)/len/k),f=c41Frame(t,dur);
 if(x<0||x>=320||y<0||y>=640)return false;
 const i=(((Math.floor(f/8)*640+y)*2560+(f%8)*320+x)*4);
 return C41.mask[i+3]>180&&Math.max(C41.mask[i],C41.mask[i+1],C41.mask[i+2])>150;
}
const c41Segment=b20HitSegment;
b20HitSegment=function(b,from,to,r,label,hit){
 if(c25Own(b)&&label==='Chronos rage energy wave'){
  const L=c30Line(b);if(!c41Hit(L.from,L.to,b._hammer.c30.t,1.35,player))return;
  return c41Segment.call(this,b,L.from,L.to,Math.hypot(L.to.x-L.from.x,L.to.y-L.from.y)*.27,label,hit);
 }
 return c41Segment.apply(this,arguments);
};
