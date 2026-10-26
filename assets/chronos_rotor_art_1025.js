'use strict';
// Exact, code-native transforms of the authored pixels. No generated geometry.
const C31Texture={
 trim(im){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height).data;let x0=c.width,y0=c.height,x1=0,y1=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(d[(y*c.width+x)*4+3]>32){x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y);}const out=document.createElement('canvas');out.width=Math.max(2,x1-x0+1);out.height=Math.max(2,y1-y0+1);out.getContext('2d').drawImage(c,x0,y0,out.width,out.height,0,0,out.width,out.height);return out;},
 palette(im,mode){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const a=g.getImageData(0,0,c.width,c.height),d=a.data;
  for(let i=0;i<d.length;i+=4){if(!d[i+3])continue;const r=d[i],gr=d[i+1],b=d[i+2],v=Math.max(r,gr,b),lo=Math.min(r,gr,b);
   if(mode==='red'){d[i]=v;d[i+1]=Math.round(lo*.88);d[i+2]=Math.round(lo*.94);}
   else {d[i]=v;d[i+1]=Math.round(v*.70+lo*.27);d[i+2]=Math.round(v*.10+lo*.78);}
  }g.putImageData(a,0,0);return c;},
 rotor(im,angle){const c=document.createElement('canvas');c.width=104;c.height=208;const g=c.getContext('2d');g.drawImage(im,0,0);const original=g.getImageData(0,0,104,208),out=g.getImageData(0,0,104,208),src=original.data,dst=out.data;
  const copy=(x,y,sx,sy)=>{sx=Math.max(0,Math.min(103,Math.round(sx)));sy=Math.max(0,Math.min(207,Math.round(sy)));const to=(y*104+x)*4,from=(sy*104+sx)*4;for(let k=0;k<4;k++)dst[to+k]=src[from+k];};
  // Circumferential UV transport: all six authored flutes travel around the
  // longitudinal axis. Fixed housing/collars do not rock with the barrels.
  for(const [top,bottom]of [[84,110],[120,146]])for(let y=top;y<bottom;y++)for(let x=39;x<=68;x++){
   const u=(x-53.5)/15,theta=Math.asin(Math.max(-1,Math.min(1,u)))+angle;
   const sector=((theta/(Math.PI/3))%1+1)%1;copy(x,y,47+sector*13,y);
  }
  // Rotate the entire authored muzzle disk through 360 degrees in its
  // projected ellipse; bore holes orbit the center rather than changing shape.
  const cs=Math.cos(angle),sn=Math.sin(angle),cx=54,cy=170,rx=21,ry=16;
  for(let y=154;y<=186;y++)for(let x=33;x<=75;x++){const u=(x-cx)/rx,v=(y-cy)/ry;if(u*u+v*v<=1)copy(x,y,cx+(u*cs+v*sn)*rx,cy+(-u*sn+v*cs)*ry);}
  g.putImageData(out,0,0);return c;
 }
};
