/* ============================================================
   PROJECTILE FX (drop 1103) — PFX13. Loaded last. window.PFX13_OFF=1 disables it entirely.

   Mike: "make the ones lacking or janky properly pixel glow inside with the pixels, snake around,
   do cool effects, even show me things maybe I didn't know I needed."

   Measured first (_BUILD_SOURCE/capture_projectile_gallery_1103.py, gallery projectile-gallery.html):
   many rounds still lit themselves with ctx.shadowBlur — a smooth Gaussian smear that is the
   opposite of the 1015 pixel-glow rule (hard steps, no blur) and is also the single most expensive
   thing a canvas can do per draw. Others are 1-frame stills, or bare fillRect/arc primitives.

   WHAT THIS ADDS, all renderer-only (no position, speed, collision, damage or clock writes):
     1. BLUR -> PIXEL GLOW. Inside drawBullets a requested shadowBlur never reaches the canvas.
        Instead each draw made under it gets hard 1-game-px light rings: the sprite's own
        silhouette tinted to the glow colour, grown in whole pixels, alpha on the PXG ladder and
        palette-stepped on the game clock. Primitive fills get the same stepped rings.
     2. INNER LIGHT. Glowing sprites get their own bright pixels added back on a travelling
        ladder step, so the core shimmers inside the art instead of a halo pasted around it.
     3. SNAKE TRAILS. Energy rounds (orbs, plasma, photon, void, lightning...) leave a pixel tail
        that wriggles on a sine across the path; tracers get a two-step motion streak; missiles
        and rockets shed flickering ember pixels. Colour comes from the round's own art.
     4. THINGS YOU DIDN'T KNOW YOU NEEDED:
        - SPAWN POP: an enemy round is born with a hard 2-frame pixel ring, so a new shot reads
          even in a dense pattern.
        - THREAT RIM: enemy rounds get a 1-px dark outline baked from their own silhouette, the
          classic shmup readability fix over bright scenery (lava, explosions, clouds).
        - GRAZE FLASH: a round passing within a hair of the pilot flashes white-hot and spits
          sparks — instant feedback for a near miss.

   Per-feature switches: PFX13.cfg.{glow,inner,trails,pop,rim,graze}. The shipping drawBullets
   chain still draws every round with its own art; this only watches which round is drawing.
   ============================================================ */
(function(){
if(window.PFX13_OFF||typeof drawBullets!=='function'||typeof ctx==='undefined')return;
const STEPS=[0,.16,.32,.52,.74,.95];
const cfg={glow:true,inner:true,trails:true,pop:true,rim:true,graze:true,clean:true,reels:true,fallback:true};
const P=CanvasRenderingContext2D.prototype;
const BLUR=Object.getOwnPropertyDescriptor(ctx,'shadowBlur')||Object.getOwnPropertyDescriptor(P,'shadowBlur');
const rawDraw=ctx.drawImage,rawFillRect=ctx.fillRect,rawFill=ctx.fill;
const S={budget:40,hueArea:0,on:false,b:null,enemy:false,glow:0,col:'#fff',bodyDone:0,graze:false,hue:null,stat:{converted:0,rings:0}};
const clockNow=()=>typeof efxClock==='number'?efxClock:(typeof stateT==='number'?stateT:performance.now()/1000);

/* ---- caches: tinted silhouettes, dark rims, bright-pixel masks, average colour ---- */
const SIL=new WeakMap();
function canvasOf(w,h){const c=document.createElement('canvas');c.width=Math.max(1,w);c.height=Math.max(1,h);return c;}
function slot(im){let m=SIL.get(im);if(!m){m=new Map();SIL.set(im,m);}return m;}
function cellSize(sw,sh){const k=Math.min(1,96/Math.max(sw,sh));return [Math.max(1,Math.round(sw*k)),Math.max(1,Math.round(sh*k))];}
function silhouette(im,sx,sy,sw,sh,col){
  const m=slot(im),key='s'+sx+','+sy+','+sw+','+sh+col;let c=m.get(key);if(c)return c;
  const [w,h]=cellSize(sw,sh);c=canvasOf(w,h);const g=c.getContext('2d');g.imageSmoothingEnabled=false;
  try{g.drawImage(im,sx,sy,sw,sh,0,0,w,h);}catch(e){return null;}
  g.globalCompositeOperation='source-in';g.fillStyle=col;g.fillRect(0,0,w,h);m.set(key,c);return c;
}
/* the dark rim: silhouette dilated by one cell pixel in eight directions, drawn under the body */
function rim(im,sx,sy,sw,sh){
  const m=slot(im),key='r'+sx+','+sy+','+sw+','+sh;let c=m.get(key);if(c!==undefined)return c;
  const base=silhouette(im,sx,sy,sw,sh,'#06040c');if(!base){m.set(key,null);return null;}
  const w=base.width+4,h=base.height+4;c=canvasOf(w,h);const g=c.getContext('2d');g.imageSmoothingEnabled=false;
  for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++)if(dx*dx+dy*dy<=5)g.drawImage(base,2+dx,2+dy);
  m.set(key,c);return c;
}
/* bright mask + average colour (needs readable pixels; served over http they are, file:// is not) */
function analyse(im,sx,sy,sw,sh){
  const m=slot(im),key='a'+sx+','+sy+','+sw+','+sh;if(m.has(key))return m.get(key);
  if(S.budget--<=0)return null;   // never more than a handful of new reads in one frame
  let out=null;
  try{
    const [w,h]=cellSize(sw,sh),c=canvasOf(w,h),g=c.getContext('2d',{willReadFrequently:true});g.imageSmoothingEnabled=false;
    g.drawImage(im,sx,sy,sw,sh,0,0,w,h);const id=g.getImageData(0,0,w,h),d=id.data;
    let r=0,gg=0,bb=0,n=0,lit=0,edge=0,edgeN=0;
    for(let x=0;x<w;x++)for(const y of [0,h-1]){edgeN++;if(d[(y*w+x)*4+3]>200)edge++;}
    for(let y=0;y<h;y++)for(const x of [0,w-1]){edgeN++;if(d[(y*w+x)*4+3]>200)edge++;}const hot=canvasOf(w,h),hg=hot.getContext('2d'),hd=hg.createImageData(w,h);
    for(let i=0;i<d.length;i+=4){const a=d[i+3];if(a<40)continue;const mx=Math.max(d[i],d[i+1],d[i+2]),mn=Math.min(d[i],d[i+1],d[i+2]);
      const wgt=(mx-mn+20)*a/255;r+=d[i]*wgt;gg+=d[i+1]*wgt;bb+=d[i+2]*wgt;n+=wgt;
      if(mx>170){lit++;hd.data[i]=Math.min(255,d[i]+40);hd.data[i+1]=Math.min(255,d[i+1]+40);hd.data[i+2]=Math.min(255,d[i+2]+40);hd.data[i+3]=255;}}
    hg.putImageData(hd,0,0);
    if(n>0){let R=r/n,G=gg/n,B=bb/n;const mx=Math.max(R,G,B,1),k=255/mx;R*=k;G*=k;B*=k;out={col:'rgb('+(R|0)+','+(G|0)+','+(B|0)+')',hot:lit>2?hot:null,box:edge>edgeN*.5};}
  }catch(e){out=null;}
  m.set(key,out);return out;
}

/* ---- cell hygiene (added after the first gallery review) ----
   Mike: "make sure they don't have pixel cut off or additional frames". Several authored cells carry
   a detached straight-edged strip: the Stage 5 mine and water orb have a bar baked under every cell,
   and some sheet rects reach one row into the neighbouring cell. When a round draws a cell, a cleaned
   copy is drawn instead: every component that is (a) much smaller than the round's own body,
   (b) a thin strip (aspect 2.2+, under 16% of the cell) and (c) nearly rectangular (fills 55%+ of its
   box) is cleared. Crescent blades, sparks and multi-bar beams fail (b) or (c), or are too large to
   count as a sliver, so they stay. The art files are untouched; the cleaned cell is cached per rect. */
function clean(im,sx,sy,sw,sh){
  const m=slot(im),key='c'+sx+','+sy+','+sw+','+sh;if(m.has(key))return m.get(key);
  const w=Math.round(sw),h=Math.round(sh);
  if(w<6||h<6||w>320||h>320){m.set(key,null);return null;}
  if(S.budget--<=0)return null;
  let out=null;
  try{
    const c=canvasOf(w,h),g=c.getContext('2d',{willReadFrequently:true});g.imageSmoothingEnabled=false;
    g.drawImage(im,sx,sy,sw,sh,0,0,w,h);const id=g.getImageData(0,0,w,h),d=id.data,N=w*h;
    const lab=new Int32Array(N),comps=[];let n=0;
    for(let i=0;i<N;i++){if(d[i*4+3]<=24||lab[i])continue;n++;const st=[i];lab[i]=n;let a=0,x0=w,x1=0,y0=h,y1=0;
      while(st.length){const q=st.pop(),x=q%w,y=(q/w)|0;a++;if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;
        for(let yy=y-1;yy<=y+1;yy++)for(let xx=x-1;xx<=x+1;xx++){if(xx<0||yy<0||xx>=w||yy>=h)continue;const r=yy*w+xx;if(!lab[r]&&d[r*4+3]>24){lab[r]=n;st.push(r);}}}
      comps.push({id:n,a,x0,x1,y0,y1});}
    if(comps.length>1){
      let main=comps[0];for(const q of comps)if(q.a>main.a)main=q;
      const drop=new Set();
      for(const q of comps){if(q===main)continue;const cw=q.x1-q.x0+1,ch=q.y1-q.y0+1,thin=Math.min(cw,ch),long=Math.max(cw,ch);
        const strip=q.a<main.a*.5&&q.a>=4&&long>=2.0*thin&&thin<=Math.max(4,Math.min(w,h)*.16)&&q.a>=.55*cw*ch;
        /* a wide flat piece wholly beyond the body (below or above it) in the outer band of the cell:
           the Stage 5 mine bar and water-orb stub. Exhaust flames are taller than wide and side wisps
           overlap the body's rows, so both stay. */
        const beyond=(q.y0>main.y1||q.y1<main.y0)&&(q.y0>=h*.7||q.y1<=h*.3);
        const shelf=beyond&&q.a<main.a*.3&&cw>=1.6*ch&&q.a>=4;
        if(strip||shelf)drop.add(q.id);}
      if(drop.size){
        let orig=null;if(window.PFX13_DEBUG_CLEAN){orig=canvasOf(w,h);orig.getContext('2d').putImageData(id,0,0);}
        for(let i=0;i<N;i++)if(drop.has(lab[i]))d[i*4+3]=0;g.putImageData(id,0,0);out={c,w,h,dropped:drop.size};S.stat.cleaned=(S.stat.cleaned||0)+1;
        if(orig)(window.PFX13_CLEANED=window.PFX13_CLEANED||[]).push({src:String(im.src||im.__key||'canvas').split('/').pop(),rect:[sx,sy,sw,sh],dropped:drop.size,round:S.b&&S.b.kind,orig:orig.toDataURL(),clean:c.toDataURL()});}
    }
  }catch(e){out=null;}
  m.set(key,out);return out;
}

/* ---- the drawImage hook: active only while a single round is being drawn ---- */
function norm(im,a){
  const iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height;
  if(a.length>=8)return [a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]];
  if(a.length>=4)return [0,0,iw,ih,a[0],a[1],a[2],a[3]];
  return [0,0,iw,ih,a[0],a[1],iw,ih];
}
function rings(src,dx,dy,dw,dh,r,t){
  const n=r>=10?3:2,amp=[.46,.24,.11],step=STEPS[3+((Math.floor(t*12+S.phase)%3+3)%3)];
  const sv=ctx.globalCompositeOperation,sa=ctx.globalAlpha,sm=ctx.imageSmoothingEnabled;
  ctx.globalCompositeOperation='lighter';ctx.imageSmoothingEnabled=false;
  /* ring reach follows the sprite, not the blur number: an 18px blur on a 20px volley trail
     drew a halo bigger than the round itself, in blocks */
  const reach=Math.max(1,Math.min(r,Math.abs(Math.min(dw,dh))*.32));
  for(let k=1;k<=n;k++){const grow=Math.max(1,Math.round(k*reach/(n+1)));
    ctx.globalAlpha=sa*amp[k-1]*(.55+step*.6);rawDraw.call(ctx,src,dx-grow,dy-grow,dw+grow*2,dh+grow*2);S.stat.rings++;}
  ctx.globalCompositeOperation=sv;ctx.globalAlpha=sa;ctx.imageSmoothingEnabled=sm;
}
ctx.drawImage=function(im,...a){
  if(S.on&&S.b&&VIS)VIS.set(S.b,(VIS.get(S.b)||0)+1);
  if(!S.on||!im||a.some(v=>!Number.isFinite(v)))return rawDraw.call(this,im,...a);
  const iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height;if(!iw||!ih)return rawDraw.call(this,im,...a);
  let [sx,sy,sw,sh,dx,dy,dw,dh]=norm(im,a);const big=Math.abs(dw*dh)>16,t=clockNow();
  if(cfg.clean){const C=clean(im,sx,sy,sw,sh);if(C){im=C.c;a=[0,0,C.w,C.h,dx,dy,dw,dh];sx=0;sy=0;sw=C.w;sh=C.h;}}
  const body=big&&this.globalAlpha>=.8&&S.bodyDone<2;
  /* a cell with an opaque background (boxy edge) would rim/glow as a square: light it from inside only */
  const A0=(body||S.glow>0)?analyse(im,sx,sy,sw,sh):null,boxy=!A0||A0.box;
  if(body&&A0&&!boxy&&Math.abs(dw*dh)>S.hueArea){S.hue=A0.col;S.hueArea=Math.abs(dw*dh);}   // trail colour from the round's biggest layer
  if(body&&S.enemy&&cfg.rim&&!boxy){const R=rim(im,sx,sy,sw,sh);if(R){
    const px=dw/(R.width-4),py=dh/(R.height-4),sv=this.globalCompositeOperation,sa=this.globalAlpha,sm=this.imageSmoothingEnabled;
    this.globalCompositeOperation='source-over';this.globalAlpha=sa*.72;this.imageSmoothingEnabled=false;
    rawDraw.call(this,R,dx-2*px,dy-2*py,dw+4*px,dh+4*py);this.globalCompositeOperation=sv;this.globalAlpha=sa;this.imageSmoothingEnabled=sm;}}
  if(S.glow>0&&cfg.glow&&big&&!boxy){const sil=silhouette(im,sx,sy,sw,sh,S.col);if(sil)rings(sil,dx,dy,dw,dh,S.glow,t);}
  const out=rawDraw.call(this,im,...a);
  if(body){S.bodyDone++;
    const A=(S.glow>0||S.graze)&&cfg.inner?A0:null;
    if(A&&A.hot){/* inner light: the art's own hot pixels, re-added on a travelling ladder step */
      const sv=this.globalCompositeOperation,sa=this.globalAlpha,sm=this.imageSmoothingEnabled;
      this.globalCompositeOperation='lighter';this.imageSmoothingEnabled=false;
      this.globalAlpha=sa*Math.min(.8,STEPS[(Math.floor(t*14+S.phase)%6+6)%6]*.7+(S.graze?.25:0));
      rawDraw.call(this,A.hot,dx,dy,dw,dh);this.globalCompositeOperation=sv;this.globalAlpha=sa;this.imageSmoothingEnabled=sm;}
    /* graze no longer whitens the whole sprite: in review a white needle read as a glitch. The sparks
       (drawn after the round) and a brighter inner-light step carry the near miss instead. */
  }
  return out;
};
/* primitive fills under a requested blur get the same stepped rings */
ctx.fillRect=function(x,y,w,h){
  if(S.on&&S.b&&VIS)VIS.set(S.b,(VIS.get(S.b)||0)+1);
  if(S.on&&S.glow>0&&cfg.glow&&Number.isFinite(x+y+w+h)){const r=S.glow,n=r>=10?3:2,amp=[.4,.2,.1],sa=this.globalAlpha,sv=this.globalCompositeOperation;
    this.globalCompositeOperation='lighter';
    for(let k=n;k>=1;k--){const g=Math.max(1,Math.round(k*r/(n+1)));this.globalAlpha=sa*amp[k-1];rawFillRect.call(this,x-g,y-g,w+g*2,h+g*2);}
    this.globalAlpha=sa;this.globalCompositeOperation=sv;}
  if(S.on&&!S.hue&&typeof this.fillStyle==='string')S.hue=this.fillStyle;
  return rawFillRect.call(this,x,y,w,h);
};
ctx.fill=function(){
  if(S.on&&S.b&&VIS)VIS.set(S.b,(VIS.get(S.b)||0)+1);
  if(S.on&&S.glow>0&&cfg.glow&&!arguments.length){const r=S.glow,sa=this.globalAlpha,sv=this.globalCompositeOperation,ss=this.strokeStyle,lw=this.lineWidth,lj=this.lineJoin;
    this.globalCompositeOperation='lighter';this.strokeStyle=this.fillStyle;this.lineJoin='miter';
    for(const [k,al] of [[1,.36],[.55,.2]]){this.lineWidth=Math.max(2,Math.round(r*k))*2;this.globalAlpha=sa*al;this.stroke();}
    this.globalAlpha=sa;this.globalCompositeOperation=sv;this.strokeStyle=ss;this.lineWidth=lw;this.lineJoin=lj;}
  if(S.on&&!S.hue&&typeof this.fillStyle==='string')S.hue=this.fillStyle;
  return rawFill.apply(this,arguments);
};
const rawStroke=ctx.stroke;
ctx.stroke=function(){if(S.on&&S.b&&VIS)VIS.set(S.b,(VIS.get(S.b)||0)+1);return rawStroke.apply(this,arguments);};
Object.defineProperty(ctx,'shadowBlur',{configurable:true,
  get(){return BLUR.get.call(this);},
  set(v){if(S.on&&cfg.glow){S.glow=v>0?Math.min(18,v):0;if(v>0){S.col=this.shadowColor||'#ffffff';S.stat.converted++;}BLUR.set.call(this,0);return;}BLUR.set.call(this,v);}});

/* ---- families: who gets a snake, a streak, embers, or nothing ---- */
const NO_TRAIL=/^(beam|laser|lasermist|flame|firewhip|hxspiral|hfl|venomx|chain|spaceLaser|spaceImpact|spaceHelperBeam|prismRay|chromeRay|flaser|flspread|axbeam|mavlaser|eglaser|lzslug|sonic|ovSonic|rzbSonic|mechmortar|groundup)$/i;
const SNAKE=/orb|plasma|photon|rift|void|lightning|bio|chaos|null|halo|prism|energy|ball|shadow|spark|atom|nova|ion|pulse|star|wisp|soul|spore|fire|ice|toxic|magma|comet|flare|sludge|acid|bubble|blob/i;
const EMBER=/missile|rocket|torpedo|warhead|nuk|shell|bomb|gmiss|emiss|erock/i;
function family(b){
  const k=String(b.kind||'');
  if(NO_TRAIL.test(k)||b._launchDelay>0)return null;
  if((b.h||0)>46||(b.w||0)>46)return null;
  if(EMBER.test(k))return 'ember';
  if(SNAKE.test(k)||b._tb28||b._heraldProjectile)return 'snake';
  return 'streak';
}
const HIST=new WeakMap();
let SEQ=0;   // golden-angle phase per round: never Math.random, which gameplay (and seeded QA) draws from
function hist(b){let h=HIST.get(b);if(!h){h={pts:[],hue:null,phase:(SEQ++*2.39996)%6.2832,born:clockNow()};HIST.set(b,h);}
  const L=h.pts[0];if(!L||Math.abs(L.x-b.x)+Math.abs(L.y-b.y)>.6){h.pts.unshift({x:b.x,y:b.y});if(h.pts.length>18)h.pts.length=18;}return h;}
function px(x,y,s,col,a){ctx.globalAlpha=a;ctx.fillStyle=col;rawFillRect.call(ctx,Math.round(x-s/2),Math.round(y-s/2),s,s);}
/* Walk back along the recorded flight path from the round itself in fixed steps, so the tail is
   one continuous pixel line whether the game drew 30 or 144 times a second. A jump longer than
   40 px (reflection, respawn, wrap) ends the walk instead of drawing a line across the screen. */
function walk(b,pts,L,step,fn){
  let ax=b.x,ay=b.y,i=0,d=0,next=step;
  while(i<pts.length){
    const p=pts[i],sx=p.x-ax,sy=p.y-ay,seg=Math.hypot(sx,sy);
    if(seg>40)break;
    if(seg<.01){i++;continue;}
    while(next<=d+seg&&next<=L){const k=(next-d)/seg;fn(ax+sx*k,ay+sy*k,-sy/seg,sx/seg,next/L,next);next+=step;}
    if(next>L)break;d+=seg;ax=p.x;ay=p.y;i++;
  }
}
function trail(b,h,fam,t){
  /* Second pass after review: tails were as wide as the round and wriggled far off it (magma, photon,
     lava comet, rift shot). Now a tail is at most 4 px thick and about three body lengths, the wriggle
     stays within 1.4 px, and a small round gets a straight streak instead of a snake. */
  const pts=h.pts,col=h.hue||'#ffd36b';if(pts.length<2)return;
  const body=Math.min(b.w||8,b.h||8),size=Math.max(1,Math.min(4,Math.round(body*.35)));
  if(fam==='snake'&&body<7)fam='streak';
  ctx.save();ctx.globalCompositeOperation='lighter';
  if(fam==='streak'){
    const w=Math.max(1,Math.round(size*.6));
    walk(b,pts,12,1,(x,y,nx,ny,u)=>px(x,y,w,col,u<.4?.34:u<.75?.16:.07));
  }else if(fam==='snake'){
    const L=Math.max(10,Math.min(22,body*2.6)),amp=Math.min(1.4,size*.4);
    walk(b,pts,L,1.5,(x,y,nx,ny,u,d)=>{
      const wig=Math.sin(t*15+h.phase-d*.4)*amp*Math.min(1,d/6);
      const s2=Math.max(1,Math.round(size*(1-u))),a=STEPS[Math.max(1,5-Math.floor(u*5))]*.55;
      px(x+nx*wig,y+ny*wig,s2,col,a);
      if(u<.25&&s2>1)px(x+nx*wig,y+ny*wig,1,'#ffffff',a*.5);
      if(size>=2&&(d|0)%5===0)px(x-nx*wig,y-ny*wig,1,col,a*.6);   // the counter-strand
    });
  }else{ /* embers: hot -> orange -> red -> soot, each pixel flickering off its own seed */
    const E=['#fff2a0','#ffb040','#ff6a1a','#b02a12','#3a1a14'],fr=Math.floor(t*30);
    walk(b,pts,16,2,(x,y,nx,ny,u,d)=>{const sd=Math.sin(d*12.9898+fr*78.233)*43758.5453,j=sd-Math.floor(sd);
      if(j<.3&&u>.3)return;const spread=u*2.4*(j-.5);
      px(x+nx*spread,y+ny*spread,u<.2&&size>1?2:1,E[Math.min(4,Math.floor(u*5))],u<.6?.7:.35);});
  }
  ctx.restore();
}
function pop(b,h,t){
  const age=t-h.born;if(age>.1||age<0)return;
  const r=Math.round(4+age*90),col=h.hue||'#ffffff',sv=ctx.globalAlpha;
  ctx.save();ctx.globalCompositeOperation='lighter';
  const n=Math.max(8,Math.round(r*1.6));for(let i=0;i<n;i++){const a=i/n*Math.PI*2;px(b.x+Math.cos(a)*r,b.y+Math.sin(a)*r,1,i%2?col:'#ffffff',age<.05?.9:.45);}
  ctx.restore();ctx.globalAlpha=sv;
}
function sparks(b,t){
  ctx.save();ctx.globalCompositeOperation='lighter';
  for(let i=0;i<4;i++){const a=t*23+i*1.7,r=5+((t*40+i*3)%7);px(b.x+Math.cos(a)*r,b.y+Math.sin(a)*r,1,i%2?'#ffffff':'#bff6ff',.9);}
  ctx.restore();
}

/* ---- the wrapper ----
   The shipping drawBullets is a CHAIN (game.js, then stage8_1003, mutator_1003, codewall_1003d,
   element_arsenal_1011, wind_projectiles_1011 ...). Some draw their own beams/shields/debris after
   the base, so the chain must run ONCE per frame or those effects multiply under 'lighter'. Others
   swap pBullets/eBullets for a filtered copy and draw the rounds they own in their own loop.

   So the chain runs untouched, and for exactly its duration array iteration is watched: a for-of
   over any array whose element is a live round announces that round as the loop reaches it. That
   covers the base loops, the filtered copies and every module's own `for(const q of owned)` loop,
   with no knowledge of who wraps whom. Nested loops inside a round's draw are passed through, and
   trails/pops draw once per round per frame however many loops visit it. */
const original=drawBullets,ITER=Array.prototype[Symbol.iterator];
/* Yuri's Lightning Orb/Bolt art is lazy: the first shots of a session drew the white fallback ring
   for ~0.5 s while the PNGs decoded. Ten tiny files; ask for them up front. */
if(typeof XART!=='undefined'&&XART._touch)for(let i=1;i<=5;i++){try{XART._touch('ylo_orb_'+i);XART._touch('ylo_bolt_'+i);}catch(e){}}
let cur=null,depth=0,PS=null,ES=null,DONE=null,VIS=null;
function begin(b,enemy){
  const t=clockNow(),h=b&&!b.dead?hist(b):null,first=!DONE.has(b);DONE.add(b);
  S.on=true;S.b=b;S.enemy=enemy;S.glow=0;S.col=null;S.hueArea=0;S.bodyDone=0;S.hue=null;S.phase=h?h.phase*2:0;S.graze=false;
  if(enemy&&cfg.graze&&h&&typeof player!=='undefined'&&player&&!player.dead){const d=Math.hypot(b.x-player.x,b.y-player.y);S.graze=d<26&&d>6;}
  if(h&&first&&cfg.trails){const fam=family(b);if(fam)trail(b,h,fam,t);}
  if(h&&first&&enemy&&cfg.pop)pop(b,h,t);
  if(VIS&&!VIS.has(b))VIS.set(b,0);
  cur={b,h,t,first};
}
function end(){
  if(!cur)return;const {b,h,t,first}=cur;cur=null;
  S.on=false;BLUR.set.call(ctx,0);
  if(!S.hue&&S.col)S.hue=S.col;   // stroke-only rounds: the glow colour they asked for
  S.glow=0;
  if(h){if(S.hue)h.hue=S.hue;if(first&&S.graze&&cfg.graze)sparks(b,t);}
}
function watched(){
  const self=this,el=self.length?self[0]:null;
  if(depth||!el||!(PS.has(el)||ES.has(el)))return ITER.call(self);
  depth++;let i=0,open=true;
  const close=()=>{end();if(open){open=false;depth--;}};
  return {next(){end();while(i<self.length){const b=self[i++];if(b&&(PS.has(b)||ES.has(b)))begin(b,ES.has(b));return {value:b,done:false};}close();return {value:undefined,done:true};},
          return(v){close();return {value:v,done:true};},[Symbol.iterator](){return this;}};
}
/* ---- no invisible rounds (third review) ----
   Several owners return "handled" without drawing while their art is still decoding (Herald's chaos
   orbs `if(!XART.rdy(HB25_ART.key))return true;`, the targeted rounds in targeting_1017, ...). The
   browser queues the sheet behind hundreds of stage images, so for that stretch a live enemy round
   was simply invisible. Any round the chain visited this frame without a single draw call gets a
   pixel-glow orb in its own colour (or a hot enemy red) until its art arrives. */
function fallbackOrb(b,enemy){
  const h=HIST.get(b),col=(h&&h.hue)||(enemy?'#ff5a6e':'#9ff6ff'),t=clockNow();
  const r=Math.max(3,Math.min(8,Math.round(Math.min(b.w||10,b.h||10)/2)));
  ctx.save();ctx.globalCompositeOperation='lighter';
  const step=STEPS[3+((Math.floor(t*12+(h?h.phase:0))%3+3)%3)];
  for(let y=-r-2;y<=r+2;y++)for(let x=-r-2;x<=r+2;x++){const d=Math.hypot(x,y);
    if(d<=r*.45)px(b.x+x,b.y+y,1,'#ffffff',.95);else if(d<=r)px(b.x+x,b.y+y,1,col,.85);else if(d<=r+2&&(x+y)%2===0)px(b.x+x,b.y+y,1,col,.35*step);}
  ctx.restore();S.stat.fallback=(S.stat.fallback||0)+1;const fk=(S.stat.fallbackKinds=S.stat.fallbackKinds||{});const kk=b.kind+(b._hb25Chaos?'/hb25':'')+(b._target17Art?'/t17':'');fk[kk]=(fk[kk]||0)+1;
}
drawBullets=function(){
  if(window.PFX13_OFF)return original.apply(this,arguments);
  S.budget=40;PS=new Set(pBullets);ES=new Set(eBullets);DONE=new WeakSet();depth=0;VIS=new Map();
  Array.prototype[Symbol.iterator]=watched;
  try{return original.apply(this,arguments);}
  finally{Array.prototype[Symbol.iterator]=ITER;end();depth=0;S.on=false;
    if(cfg.fallback)for(const [b,n] of VIS)if(n===0&&b&&!b.dead&&!(b._launchDelay>0)&&!b.hidden&&!b.invisible)fallbackOrb(b,ES.has(b));
    PS=ES=null;VIS=null;}
};
/* ---- reel corrections (second review) ----
   - s6omega: its eight authored frames draw the canister at three widths (46/42/32 px in an 80 px
     cell), so the bomb visibly breathes. Mike: "s6 omega needs to remain the same size". Hold the full
     size frame for the whole flight; the inner light and embers keep it alive (the 0914 rule).
   - Stage 3 targeted ice missile: targeting_1017 loops `bfx_cryo_m_*`, the Cryo boss's MUZZLE burst
     (grow, burst, dissipate, cells 139-208 px), as flight art, so it jittered and nearly vanished on
     two frames. Hold the fullest crystal cell. Muzzle flashes outside round drawing are untouched.
   Keys are remapped only while a round is drawing. */
/* - s9lattice / s7spore: 12-frame bloom reels (heights 44->215->44 px) played on a one-second loop,
     so every second the round collapsed to a speck and snapped back. Bloom in once (0-4), then
     ping-pong the plateau (5-8, 150-178 px) on the round's own flight clock. */
const bloomHold=(k,b)=>{const t=(b&&(b._visualAge??b.t))||0,f=Math.floor(t*12);
  const i=f<=4?Math.max(0,f):5+[0,1,2,3,2,1][(f-5)%6];return k.replace(/_\d+$/,'_'+i);};
const REEL_HOLD=[[/^s6mb_omegabomb-(hostile|reflected)_\d+$/,k=>k.replace(/_\d+$/,'_0')],[/^bfx_cryo_m_\d+$/,()=>'bfx_cryo_m_2'],
  [/^(s9lattice|s7spore)_\d+$/,bloomHold]];
if(typeof XART!=='undefined'){
  const remap=k=>{if(!S.on||!cfg.reels||typeof k!=='string')return k;for(const [re,f] of REEL_HOLD)if(re.test(k))return f(k,S.b);return k;};
  for(const fn of ['get','raw','rdy']){const base=XART[fn];if(typeof base==='function')XART[fn]=function(k){const r=[].slice.call(arguments);r[0]=remap(k);return base.apply(this,r);};}
  try{XART._touch('bfx_cryo_m_2');XART._touch('s6mb_omegabomb-hostile_0');XART._touch('s6mb_omegabomb-reflected_0');}catch(e){}
}
/* - Premium boss-projectile reels (`bpfx_proj_<family>_0..7`): drawBossProjectileArt draws a frame only
     once that frame has decoded and otherwise lets the round's own art draw, so rounds flipped
     between two looks frame by frame (Stage 4 kinetic tracer <-> blue ball, Herald needles red <->
     blue) until all eight arrived. They are warmed at load and used only when the whole reel is ready.
   - Herald's dark claw needles (`_target17Element:'dark'` from `_heraldPart1003`) keep their own red
     dark needle. The generic blue premium laser was replacing it once loaded ("the s8/s9 needles keep
     turning blue"). */
if(typeof drawBossProjectileArt==='function'){
  const baseArt=drawBossProjectileArt,FAM=['kinetic','laser','missile','void'];
  const ready=f=>{for(let i=0;i<8;i++)if(!XART.rdy('bpfx_proj_'+f+'_'+i))return false;return true;};
  try{for(const f of FAM)for(let i=0;i<8;i++)XART._touch('bpfx_proj_'+f+'_'+i);}catch(e){}
  drawBossProjectileArt=function(b,family){
    if(window.PFX13_OFF||!cfg.reels)return baseArt.apply(this,arguments);
    if(b&&b._target17Element==='dark'&&b._heraldPart1003)return false;
    if(family&&!ready(family))return false;
    return baseArt.apply(this,arguments);
  };
}
window.PFX13={cfg,stat:S.stat,original,version:"1103",_hue:b=>{const h=HIST.get(b);return h&&h.hue||null;},_clean:(im,sx,sy,sw,sh)=>{S.budget=99;return clean(im,sx,sy,sw,sh);},_dbg:()=>({depth,on:S.on,cur:!!cur,ps:PS?PS.size:-1})};
})();
