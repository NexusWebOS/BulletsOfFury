"use strict";
/* ============================================================
   SHIP FORMING (drop 1104) - SF14. Loaded last. window.SF14_OFF=1 disables it.

   Mike: "enhance and upgrade the space ship forming effects when we turn into it. It's currently a little
   janky and could certainly use a little bit more effort and effects."
   Filmed frame by frame (_BUILD_SOURCE/capture_ship_forming_1104.py), the Stage 5 kit assembly
   (gravityMode drift -> charge -> scatter -> snap -> pixelglow -> whiteout -> reveal) had four problems:
     1. CHARGE (4.1 s) looked like drift: the parts kept orbiting, nothing built up.
     2. SCATTER barely read.
     3. SNAP POPPED: furyShipDrawPhase stops drawing the parts at 78% of the snap, when they are only
        ~60% of the way in, and the finished ship appears from nothing.
     4. PIXELGLOW did not glow: furyIntroWhite eased the whole screen to white across it.
   This layer keeps every phase clock, the approved kit size/orbit (0914/1001c), the authored veil
   curtain and Cole's authored assembly cells. It adds, on the 1015 hard-step ladder (no blur):
     - charge: energy tethers marching from each docked part into the plane, brighter per charge band;
       a stepped pixel core on the plane; every band tick flashes each part's own silhouette cyan;
     - scatter: a pixel shock ring and a white flash on the parts;
     - snap: parts keep converging all the way onto their lock points over a white energy outline of
       the finished ship, each welding with a white flash and sparks as it locks;
     - pixelglow: the white outline drops in steps to reveal the ship, which then glows from its own
       silhouette (outline rings + brightening + sparks) before the screen whites out in hard steps.
   Draw only: no clock, sound, position or state is written except SF14's own bookkeeping on G._sf14.
   ============================================================ */
(function(){
if(window.SF14_OFF)return;
const base={phase:furyShipDrawPhase,white:furyIntroWhite},stat={tethers:0,welds:0,rings:0,glow:0};
const LADDER=[0,.16,.32,.52,.74,.95];
const step=v=>{v=clamp(v,0,1);let o=0;for(const s of LADDER)if(v>=s)o=s;return o;};
const hash=(i,k)=>{const s=Math.sin(i*127.1+k*311.7)*43758.5453;return s-Math.floor(s);};
const CYAN='#7fe6ff',ICE='#dff8ff',WHITE='#ffffff';

/* own-pixel silhouettes and outline rings, cached per source canvas */
const tints=new WeakMap(),rings=new WeakMap();
function tinted(im,color){let m=tints.get(im);if(!m)tints.set(im,m={});if(m[color])return m[color];
  const c=document.createElement('canvas');c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;
  const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(im,0,0);g.globalCompositeOperation='source-in';g.fillStyle=color;g.fillRect(0,0,c.width,c.height);
  return m[color]=c;}
function ring(im,r,color){let m=rings.get(im);if(!m)rings.set(im,m={});const k=r+color;if(m[k])return m[k];
  const s=tinted(im,color),pad=r+1,c=document.createElement('canvas');c.width=s.width+pad*2;c.height=s.height+pad*2;
  const g=c.getContext('2d');g.imageSmoothingEnabled=false;
  for(let a=0;a<16;a++){const dx=Math.round(Math.cos(a*Math.PI/8)*r),dy=Math.round(Math.sin(a*Math.PI/8)*r);g.drawImage(s,pad+dx,pad+dy);}
  g.globalCompositeOperation='destination-out';
  const inner=Math.max(0,r-2);for(let a=0;a<16;a++){const dx=Math.round(Math.cos(a*Math.PI/8)*inner),dy=Math.round(Math.sin(a*Math.PI/8)*inner);g.drawImage(s,pad+dx,pad+dy);}
  g.drawImage(s,pad,pad);
  return m[k]={c,pad};}
function blitSil(im,x,y,w,h,color,a,mode){if(!im||a<=0)return;const s=tinted(im,color);
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=a;if(mode)ctx.globalCompositeOperation=mode;ctx.drawImage(s,x-w/2,y-h/2,w,h);ctx.restore();}
function blitRing(im,x,y,w,h,rNative,color,a){if(!im||a<=0)return;const R=ring(im,rNative,color),kx=w/(im.naturalWidth||im.width),ky=h/(im.naturalHeight||im.height);
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=a;ctx.globalCompositeOperation='lighter';
  ctx.drawImage(R.c,x-w/2-R.pad*kx,y-h/2-R.pad*ky,R.c.width*kx,R.c.height*ky);ctx.restore();stat.rings++;}
function dot(x,y,s,color,a){if(a<=0)return;ctx.globalAlpha=a;ctx.fillStyle=color;ctx.fillRect(Math.round(x-s/2),Math.round(y-s/2),s,s);}
function pixelRing(cx,cy,r,n,s,color,a){ctx.save();for(let i=0;i<n;i++){const t=i*TAU/n;dot(cx+Math.cos(t)*r,cy+Math.sin(t)*r*.82,s,color,a);}ctx.restore();}

/* the parts, posed exactly as the base choreography poses them */
function parts(G,x,y,size){const out=[];if(typeof FURY_KIT==='undefined')return out;
  for(let i=0;i<FURY_KIT.length;i++){const p=furyPartPose(G,i,x,y,size);if(p)out.push({i,...p});}return out;}
function partImage(p,pilot){return furyShipCanvas(p.key,pilot);}

function tether(x0,y0,x1,y1,t,strength,i){const d=Math.hypot(x1-x0,y1-y0);if(d<4)return;const n=Math.max(3,Math.floor(d/7));
  for(let k=0;k<n;k++){const u=((k/n)+t*1.6+hash(i,1))%1;if(((k+i)&1)===1&&strength<.7)continue;
    const px=lerp(x0,x1,u),py=lerp(y0,y1,u)+Math.sin(u*Math.PI*2+t*9+i)*2*(1-u);
    dot(px,py,u>.82?3:2,u>.82?WHITE:CYAN,step(strength*(.35+.65*u)));}
  stat.tethers++;}

function chargeFx(G,x,y,size,pilot,cole){
  const S=G._sf14||(G._sf14={band:-1,bandAt:0});const band=Math.max(0,G.chargeBand|0),age=G.age||0;
  if(band!==S.band){S.band=band;S.bandAt=age;}
  const since=age-S.bandAt,strength=.45+.55*band/4,pulse=.75+.25*Math.sin(age*14);
  ctx.save();
  if(!cole)for(const p of parts(G,x,y,size))if(p.entry>=.98)tether(p.x,p.y,x,y,age,strength*pulse,p.i);
  // core: a stepped pixel ring that tightens and brightens per band, plus one expanding ring per band tick
  pixelRing(x,y,size*(.36-.03*band)+Math.sin(age*10)*1.5,24+band*4,2,CYAN,step(.3+.14*band));
  pixelRing(x,y,size*(.36-.03*band)*.6,16,2,WHITE,step(.18+.12*band)*pulse);
  if(since<.45)pixelRing(x,y,size*.3+since*size*1.6,36,3,ICE,step(1-since/.45));
  ctx.restore();
  // band tick: each part flashes its own silhouette, staggered around the kit
  if(!cole)for(const p of parts(G,x,y,size)){const k=since-p.i*.035;if(k<0||k>.18)continue;
    ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rotation||0);blitSil(partImage(p,pilot),0,0,p.size,p.size,CYAN,step(.8*(1-k/.18)),'lighter');ctx.restore();}
}
function scatterFx(G,x,y,size,pilot,cole){const u=clamp(G.t/GRAVITY_SCATTER_DUR,0,1);
  ctx.save();pixelRing(x,y,lerp(size*.3,size*2.4,_ease(u)),56,3,ICE,step(1-u));pixelRing(x,y,lerp(size*.2,size*1.7,_ease(u)),40,2,CYAN,step(.8*(1-u)));ctx.restore();
  if(!cole&&G.t<.14)for(const p of parts(G,x,y,size)){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rotation||0);blitSil(partImage(p,pilot),0,0,p.size,p.size,WHITE,step(1-G.t/.14),'lighter');ctx.restore();}
}
function snapFx(G,x,y,size,pilot){
  const u=clamp(G.t/GRAVITY_SNAP_DUR,0,1),ship=furyShipCanvas('base',pilot);
  if(u>=.78&&ship){
    // the base has swapped to the finished ship: cover it with its own white energy outline, then keep
    // the parts closing all the way onto their lock points over it
    blitSil(ship,x,y,size,size,ICE,1);
    blitRing(ship,x,y,size,size,Math.round(3*(ship.naturalWidth||ship.width)/size),CYAN,step(.9));
  }
  const S=G._sf14||(G._sf14={});S.welded=S.welded||{};
  for(const p of parts(G,x,y,size)){
    const e=u*u;
    if(u>=.78){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rotation||0);furyShipBlit(p.key,0,0,p.size,p.size,pilot,1);ctx.restore();}
    else tether(p.x,p.y,x,y,G.age||0,1,p.i);
    if(e>=.86){const k=(e-.86)/.14;
      if(!S.welded[p.i]){S.welded[p.i]=G.t;stat.welds++;}
      const since=G.t-S.welded[p.i];
      ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rotation||0);blitSil(partImage(p,pilot),0,0,p.size,p.size,WHITE,step(.95-since*4),'lighter');ctx.restore();
      ctx.save();for(let s=0;s<6;s++){const a=hash(p.i,s)*TAU,r=4+since*90*(.6+hash(s,p.i));dot(p.x+Math.cos(a)*r,p.y+Math.sin(a)*r,2,s&1?WHITE:CYAN,step(.9-since*3.5));}ctx.restore();}
  }
}
function glowFx(G,x,y,size,pilot){
  const u=clamp(G.t/GRAVITY_PIXEL_DUR,0,1),ship=furyShipCanvas('base',pilot);if(!ship)return;
  const nat=ship.naturalWidth||ship.width,k=nat/size;
  // hand-off: the white outline that covered the snap steps down over the first 0.2 s
  if(G.t<.2)blitSil(ship,x,y,size,size,ICE,step(1-G.t/.2));
  // the ship lights from its own silhouette, rings growing outward
  blitSil(ship,x,y,size,size,ICE,step(.3+.65*u),'lighter');
  for(let r=0;r<3;r++){const rr=(2+r*3+u*5)*k;blitRing(ship,x,y,size,size,Math.round(rr),r===0?WHITE:CYAN,step((.95-r*.2)*(.6+.4*u)));}
  ctx.save();for(let s=0;s<20;s++){const a=s*TAU/20+hash(s,3)*.3,r=size*.42+((u*1.4+hash(s,7))%1)*size*1.4;
    dot(x+Math.cos(a)*r,y+Math.sin(a)*r*.85,s%3===0?3:2,s&1?WHITE:CYAN,step((1-((u*1.4+hash(s,7))%1))*.9));}ctx.restore();
  stat.glow++;
}

furyShipDrawPhase=function(G,x,y,size,planeH,pilot){
  if(window.SF14_OFF||!G)return base.phase.apply(this,arguments);
  const cole=pilot==='cole',ph=G.phase;
  // tethers and the core sit under the hardware: draw them first, the plane and parts land on top
  if(ph==='charge')chargeFx(G,x,y,size,pilot,cole);
  const out=base.phase.apply(this,arguments);
  if(ph==='charge'&&!cole){ // core highlight over the plane itself
    const band=Math.max(0,G.chargeBand|0);ctx.save();pixelRing(x,y,size*.12,10,2,WHITE,step(.2+.15*band));ctx.restore();}
  else if(ph==='scatter')scatterFx(G,x,y,size,pilot,cole);
  else if(ph==='snap'&&!cole)snapFx(G,x,y,size,pilot);
  else if(ph==='pixelglow')glowFx(G,x,y,size,pilot);
  return out;
};
// pixelglow belongs to the ship first: hold the screen clear, then white it out in hard steps
furyIntroWhite=function(G){
  if(window.SF14_OFF||!G||G.phase!=='pixelglow')return base.white.apply(this,arguments);
  return step(clamp((G.t/GRAVITY_PIXEL_DUR-.55)/.45,0,1));
};
window.SF14={stat,version:'1104'};
})();
