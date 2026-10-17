"use strict";
for(const a of Object.values(A17_ART))XART._src[a.key]=a.path;
function a17Warm(names){for(const name of names||Object.keys(A17_ART))if(A17_ART[name])XART.rdy(A17_ART[name].key);}
function a17Blit(name,frame,x,y,size,flash=0,angle=0){const a=A17_ART[name];if(!a||!XART.rdy(a.key))return false;
 const f=((Math.floor(frame)%a.n)+a.n)%a.n,k=size/a.span,sx=(f%a.cols)*a.w,sy=Math.floor(f/a.cols)*a.h,im=XART.get(a.key);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(angle);
 ctx.drawImage(im,sx,sy,a.w,a.h,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);
 if(flash>0){const t=xartTint(a.key,'#ffffff',1);if(t){ctx.globalAlpha*=Math.min(1,flash*8);ctx.drawImage(t,sx,sy,a.w,a.h,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);}}
 ctx.restore();return true;
}
const A17_LOAD=stageLoadBegin;stageLoadBegin=function(n,keys){const names=n===4?['stormJet','tankHull','tankTurret','tankShell']:[];
 names.push('windBullets','windSpread','windHeavy','windLaser');return A17_LOAD.call(this,n,[...(keys||[]),...names.map(k=>A17_ART[k].key)]);};
