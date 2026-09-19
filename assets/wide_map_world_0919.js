/* Extend the live campaign world outside the native 480x512 game canvas. */
(function(){
'use strict';
const room=document.getElementById('room');if(!room)return;
const canvas=document.createElement('canvas');canvas.id='wide-map-world';canvas.setAttribute('aria-hidden','true');room.appendChild(canvas);
const g=canvas.getContext('2d');let last=0;
function ready(k){return typeof XART!=='undefined'&&XART.rdy(k);}
function draw(now){requestAnimationFrame(draw);if(now-last<85)return;last=now;
 const active=document.body.classList.contains('wide-map');canvas.style.display=active?'block':'none';if(!active)return;
 if(typeof cmap2==='undefined'||typeof cmap2World!=='function'||!ready('cm2_ocean'))return;
 const screen=document.getElementById('screen').getBoundingClientRect();
 const scale=screen.width/480,cam=cmap2.cam,t=cmap2.t;
 if(!screen.width||!cam||!scale)return;
 const W=innerWidth,H=innerHeight;if(canvas.width!==W||canvas.height!==H){canvas.width=W;canvas.height=H;}
 g.imageSmoothingEnabled=false;g.fillStyle='#04102a';g.fillRect(0,0,W,H);
 const originX=screen.left+240*scale,originY=screen.top+218*scale;
 const point=(x,y)=>[originX+(x-cam.x)*cam.z*scale,originY+(y-cam.y)*cam.z*scale];
 const size=n=>n*cam.z*scale;
 const ocean=XART.get('cm2_ocean'),tile=256*(.6+.4*cam.z),full=tile*scale;
 const mod=(a,n)=>((a%n)+n)%n;
 let ox=screen.left-mod(cam.x*cam.z*.38+t*7,tile)*scale;
 let oy=screen.top-mod(cam.y*cam.z*.38+t*3,tile)*scale;
 for(let y=oy-full;y<H;y+=full)for(let x=ox-full;x<W;x+=full)g.drawImage(ocean,x,y,full+.8,full+.8);
 g.globalAlpha=.22;
 ox=screen.left-mod(cam.x*cam.z*.38*.9-t*5+tile*.5,tile)*scale;
 oy=screen.top-mod(cam.y*cam.z*.38*.9+t*4+tile*.37,tile)*scale;
 for(let y=oy-full;y<H;y+=full)for(let x=ox-full;x<W;x+=full)g.drawImage(ocean,x,y,full+.8,full+.8);
 g.globalAlpha=1;
 const order=typeof cmap2Order==='function'?cmap2Order():[1,2,3,4,5,6,7,8,9,'hub'];
 for(const k of order){const key='cm2_isl_'+k+'_shadow';if(!ready(key))continue;
  const w=cmap2World(k),s=cmap2Size(k),lift=cmap2.lift[k]||0;
  const sx=w.x+14+(cam.x-w.x)*.08+3*lift,sy=w.y+24+(cam.y-w.y)*.08+5*lift;
  const [x,y]=point(sx,sy),d=size(s);g.globalAlpha=.55-.12*lift;g.drawImage(XART.get(key),x-d/2,y-d/2,d,d);}
 g.globalAlpha=1;
 for(const k of order){const w=cmap2World(k),s=cmap2Size(k),on=cmap2Unlocked(k),lift=cmap2.lift[k]||0;
  const [x,y]=point(w.x,w.y+cmap2Bob(k)-4*lift),d=size(s);
  const glow='cm2_isl_'+k+'_glow';if(on&&lift>.02&&ready(glow)){g.globalAlpha=(.55+.45*Math.sin(t*4.2))*lift;g.drawImage(XART.get(glow),x-d/2,y-d/2,d,d);g.globalAlpha=1;}
  const key='cm2_isl_'+k+(on?'':'_lock');if(ready(key))g.drawImage(XART.get(key),x-d/2,y-d/2,d,d);}
 if(cmap2.clouds){const span=1340;
  for(let pass=0;pass<2;pass++)for(const q of cmap2.clouds){const key='cm2_cloud_'+q.i+(pass?'':'_shadow');if(!ready(key))continue;
   const im=XART.get(key),iw=(im.naturalWidth||im.width)/2,ih=(im.naturalHeight||im.height)/2;
   const bx=mod(q.x+t*q.sp+200,span)-200;
   const px=pass?bx+cam.x*(1-1.28):bx+28+cam.x*(1-.95);
   const py=pass?q.y+cam.y*(1-1.28):q.y+46+cam.y*(1-.95);
   const [x,y]=point(px,py);g.globalAlpha=pass?.72:.16;g.drawImage(im,x-size(iw)/2,y-size(ih)/2,size(iw),size(ih));}
  g.globalAlpha=1;}
}
room.addEventListener('click',function(e){
 if(!document.body.classList.contains('wide-map')||typeof sselCursor==='undefined'||!cmap2.cam)return;
 if(typeof campPause!=='undefined'&&campPause)return;
 if(typeof sselBoot!=='undefined'&&sselBoot>0)return;
 if(typeof stateT!=='undefined'&&stateT<.4)return;
 const sr=document.getElementById('screen').getBoundingClientRect();
 if(e.clientX>=sr.left&&e.clientX<=sr.right&&e.clientY>=sr.top&&e.clientY<=sr.bottom)return;
 const rr=document.getElementById('wide-right').getBoundingClientRect();
 if(e.clientX>=rr.left&&e.clientX<=rr.right&&e.clientY>=rr.top&&e.clientY<=rr.bottom)return;
 const scale=sr.width/480,cam=cmap2.cam,ox=sr.left+240*scale,oy=sr.top+218*scale;
 const bonus=!!(campaign&&campaign.bonusUnlocked),lo=bonus?9:1,hi=bonus?9:Math.min(8,campaign.unlockedMax||1);
 for(let st=lo;st<=hi;st++){
  const w=cmap2World(st);if(!w)continue;
  const x=ox+(w.x-cam.x)*cam.z*scale,y=oy+(w.y-cam.y)*cam.z*scale;
  if(Math.hypot(e.clientX-x,e.clientY-y)>cmap2Size(st)*.36*cam.z*scale)continue;
  if(st===sselCursor){if(typeof Input!=='undefined')Input.injectTap('enter');}
  else{sselCursor=st;cmap2.focus='map';if(Audio.SFX&&Audio.SFX.blip)Audio.SFX.blip();}
  break;
 }
});
requestAnimationFrame(draw);
})();
