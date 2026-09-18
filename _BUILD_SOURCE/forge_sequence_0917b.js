/* ============================================================
   THE FORGE SEQUENCE, SPLIT INTO ITS BEATS (Mike, 0917b)

   "Defeat boss, end screen - currency conversion during end screen and stats given - weapons gained
    screen/powers gained screen - the forge screen - the forging screen itself - the forged product
    screen - the loadout selection screen - fade to next level."

   THE FORGE      pick a slot, pick an element it has EARNED              (drawForge)
   THE FORGING    the two inputs welded in the chamber, 0-100%            (drawForging, GS.FORGING)
   THE PRODUCT    the forged badge, its name, and its REAL rounds firing  (drawForging, GS.FORGED)
   THE LOADOUT    six bays and the scrolling pool; START fades out        (drawLoadout, GS.LOADOUT)

   Both plates are SpriteCook art at the debrief's own 477:266 aspect (they fill the cinematic
   viewport with no distortion) and every socket below is MEASURED off them - the longest runs of
   near-black - never guessed. The chamber is a 1:1 edit of the 0916 concept plate Mike asked to play
   off ("I liked that combination screen we had earlier").
   ============================================================ */
const FORGE_CHAMBER={
  slots:[[0.0836,0.1302,0.1265,0.1133],[0.0836,0.2878,0.1265,0.1133],[0.0836,0.4453,0.1265,0.1146],
         [0.0836,0.6016,0.1265,0.1146],[0.0836,0.7604,0.1265,0.1133]],
  hexW:[0.4041,0.2839,0.0785,0.1224],   /* the upper input socket: the WEAPON */
  hexE:[0.4041,0.5195,0.0792,0.1289],   /* the lower input socket: the ELEMENT */
  hexOut:[0.5523,0.4062,0.0770,0.1237], /* the cyan output socket: what comes out */
  core:[0.3379,0.1927,0.3147,0.5586],   /* the chamber's round interior */
  view:[0.7667,0.1719,0.1497,0.6628],   /* the tall glass on the right: the live preview */
  bar:[0.2878,0.8346,0.4237,0.0716],    /* the trough under the chamber: the progress bar */
  title:[0.2400,0.0900,0.5200,0.0800]   /* the plating above the chamber, where the product is named */
};
const LOADOUT_PLATE={
  title:[0.2602,0.1224,0.4797,0.0833],
  /* ⚠ the bay INTERIORS, measured 0917c: the first cut used the outer bevel box (y .3320 h .2135), which
     centred every icon ~6px above the well - Mike's "center all icons in boxes". Four wells read clean;
     the two whose edges merge with the frame take the same measured pitch (.14315). */
  bayX:[0.0858,0.2297,0.3721,0.5153,0.6584,0.8016], bayY:0.3555, bayW:0.1130, bayH:0.1888,
  stripX:[0.0807,0.2246,0.3663,0.5102,0.6541,0.7943], stripY:0.6016, stripW:0.1235, stripH:0.0508,
  pool:[0.0850,0.6780,0.8300,0.1300],
  info:[0.2878,0.8320,0.4244,0.0742]
};
const FORGE_WELD_T0=0.75, FORGE_WELD_T=2.8, FORGE_PRODUCT_WAIT=0.95;
const FSEL_BLINK=14;                           /* Hz: the traced pointer "blinks rapidly" */
const FORGE_ROMAN=['','I','II','III','IV','V'];
function frc(a,W,H){ return [a[0]*W,a[1]*H,a[2]*W,a[3]*H]; }
function fsx(n){ try{ if(Audio&&Audio.SFX&&Audio.SFX[n]){ Audio.SFX[n](); return true; } }catch(_){ } return false; }
function forgeBadgeKey(e,w,l){ return 'micon_forge_'+e+'_'+(w|0)+((l|0)>1?'_'+(l|0):''); }
/* the icon a bay shows: the FORGED badge once a weapon carries an element, the plain one before */
function forgeSlotKey(w){
  const f=forgeEntry(w);
  if(f && XART.rdy(forgeBadgeKey(f.elem,w,f.lv))) return forgeBadgeKey(f.elem,w,f.lv);
  return weaponIconKey(w, Math.max(1,(run.wlevels&&run.wlevels[w])|0));
}
/* draw an icon STRETCHED to a width, the way the unlock page does it: iconBlit only takes a height, so
   one invisible draw measures the width it would take and the real one runs under a horizontal scale */
function forgeIconFit(key,cx,cy,h,wantW,alpha){
  if(typeof iconBlit!=='function') return 0;
  ctx.save(); ctx.globalAlpha=0; const w0=iconBlit(ctx,key,-9999,-9999,h,true)||0; ctx.restore();
  if(!w0) return 0;
  const sx=wantW?Math.min(1.35,wantW/w0):1;
  ctx.save(); ctx.globalAlpha=(alpha==null?1:alpha); ctx.translate(cx,cy); ctx.scale(sx,1); iconBlit(ctx,key,0,0,h,true); ctx.restore();
  return w0*sx;
}

/* ---- THE SELECTOR (Mike, 0917b) ----------------------------------------------------------------
   "Dont make the selector a square, make the selector do a pixel flash bottom to top mirror of the
    arrow from the menu as you highlight an icon ... trace the icon to make our own hexagon pointer
    that blinks rapidly too."
   The arrow IS the title menu's nsel_arrow (Mike's own selector), turned to point UP at the icon, and
   its rising white is stepped in six PIXEL rows rather than slid - the menu's own SEL_* timing.
   ⚠ THE SWEEP IS CLIPPED IN SCREEN SPACE, BEFORE THE ROTATION. drawSelArrow clips in the sprite's local
   frame, which for a sprite turned a quarter would sweep ACROSS the arrow instead of up it. */
function forgeSelArrowUp(cx, topY, H, variant){
  const v=variant||'y', key=_selKey(v);
  if(typeof XART==='undefined') return false;
  if(XART._src && XART._src[key] && XART._touch) XART._touch(key);
  if(!XART.rdy(key)) return false;
  const im=XART.get(key), nw=im.naturalWidth||im.width, nh=im.naturalHeight||im.height;
  const len=H, thick=H*(nh/Math.max(1,nw)), cy=topY+len/2;       /* the sprite points RIGHT: its width is the length */
  const t=(performance.now()/1000)%SEL_CYCLE;
  const blit=function(img){ ctx.save(); ctx.translate(cx,cy); ctx.rotate(-Math.PI/2); ctx.drawImage(img,-len/2,-thick/2,len,thick); ctx.restore(); };
  ctx.save(); ctx.imageSmoothingEnabled=false;
  ctx.shadowColor='#ffe9a0'; ctx.shadowBlur=6; blit(im); ctx.shadowBlur=0;
  const wc=_selWhite(v);
  if(wc){
    if(t<SEL_RISE){
      const k=Math.ceil((t/SEL_RISE)*6)/6, bandTop=topY+len-len*k;
      ctx.save(); ctx.beginPath(); ctx.rect(cx-thick, bandTop, thick*2, topY+len-bandTop); ctx.clip();
      ctx.globalAlpha=0.92; blit(wc); ctx.restore();
    } else if(t<SEL_RISE+SEL_FLASH){
      ctx.save(); ctx.globalAlpha=1-((t-SEL_RISE)/SEL_FLASH)*0.35; blit(wc); ctx.restore();
    }
  }
  ctx.restore();
  return true;
}
/* the HEXAGON POINTER: a ring traced off the icon's own alpha - dilate the silhouette, flood it one
   colour, punch the silhouette back out. ⚠ NO getImageData: a file:// page taints every canvas that
   has touched a decoded image (Mike's pilot-screen crash, 0917b), and compositing needs no pixel read. */
const _forgeTrace={};
function forgeTraceCanvas(key,h,col){
  const S=2, hh=Math.round(h), ck=key+'|'+hh+'|'+col;
  if(_forgeTrace[ck]) return _forgeTrace[ck];
  if(typeof iconBlit!=='function') return null;
  const probe=document.createElement('canvas'); probe.width=2; probe.height=2;
  const w0=iconBlit(probe.getContext('2d'),key,-9999,-9999,hh,true);
  if(!w0) return null;                              /* not decoded yet: try again next frame, never cache a hole */
  const p=Math.max(2,Math.round(hh*0.075)), W=Math.ceil((w0+p*2+4)*S), Hc=Math.ceil((hh+p*2+4)*S);
  const cv=document.createElement('canvas'); cv.width=W; cv.height=Hc;
  const g=cv.getContext('2d'); g.imageSmoothingEnabled=false;
  const cx=W/2, cy=Hc/2;
  for(let a=0;a<16;a++){ const an=a*TAU/16; iconBlit(g,key,cx+Math.cos(an)*p*S,cy+Math.sin(an)*p*S,hh*S,true); }
  g.globalCompositeOperation='source-in'; g.fillStyle=col; g.fillRect(0,0,W,Hc);
  g.globalCompositeOperation='destination-out'; iconBlit(g,key,cx,cy,hh*S,true);
  return (_forgeTrace[ck]={cv:cv, w:W/S, h:Hc/S});
}
function forgeHexPointer(key,cx,cy,h,col){
  const on=Math.floor(performance.now()/1000*FSEL_BLINK)%2===0;
  const T=forgeTraceCanvas(key,h,on?'#ffffff':(col||'#ffd24a'));
  if(!T) return false;
  ctx.save(); ctx.imageSmoothingEnabled=false;
  ctx.drawImage(T.cv,cx-T.w/2,cy-T.h/2,T.w,T.h);
  if(on){ ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=0.5; ctx.drawImage(T.cv,cx-T.w/2,cy-T.h/2,T.w,T.h); }
  ctx.restore();
  return true;
}

/* ---- THE LIVE PREVIEW: the forged weapon's REAL rounds (Mike: "loads up our new projectile in-game") ----
   Not a picture of a round: pShoot() is called with the forged weapon and element held, and the rounds
   it pushes are drawn by drawBullets - the same two functions a stage uses. The game's globals are
   SWAPPED for the preview's own and restored in a finally, so nothing the preview fires can reach the
   level, and the level cannot reach it. Rounds move by their own velocity (the stage's collision loop
   is not run - there is nothing here to hit); the beam and the flame are anchored to the ship the way
   that loop anchors them. */
function forgePreviewNew(w,elem,lv){ return {w:w|0, elem:elem, lv:lv|0, bullets:[], parts:[], cd:0.45, t:0, fired:0, err:null}; }
function forgePreviewSwap(P,VWp,VHp,fn){
  /* ⚠ 0917d: THE STAGE'S TARGET LISTS ARE SWAPPED OUT TOO. The preview now runs a weapon's OWN tick where it
     has one (the lightning orb's split into bolts, the mist's cloud), and those ticks collide with `enemies`,
     `powerups`, `boss` and `subBoss` and push `zaps` - so every one of them is emptied for the duration and
     put back in the finally, or a preview round fired at x 65 could strike a live unit at world x 65. */
  const sv={pb:pBullets, eb:eBullets, pa:particles, px:player.x, py:player.y, pd:player.dead, pi:player.invuln,
            w:run.weapon, wl:run.wlevel, inf:run.infusion, sh:shake,
            en:enemies, pu:powerups, zp:zaps, ba:bossActive, sba:subBossActive};
  try{
    pBullets=P.bullets; eBullets=[]; particles=P.parts;
    enemies=[]; powerups=[]; zaps=[]; bossActive=false; subBossActive=false;
    player.x=VWp/2; player.y=VHp-40; player.dead=false;
    run.weapon=P.w; run.wlevel=Math.max(1,((run.wlevels&&run.wlevels[P.w])|0)||1);
    run.infusion={elem:P.elem, lv:Math.max(1,P.lv), hits:0};
    fn();
  }catch(err){ P.err=String((err&&err.message)||err); }
  finally{
    P.bullets=pBullets; P.parts=particles;
    pBullets=sv.pb; eBullets=sv.eb; particles=sv.pa; player.x=sv.px; player.y=sv.py; player.dead=sv.pd; player.invuln=sv.pi;
    enemies=sv.en; powerups=sv.pu; zaps=sv.zp; bossActive=sv.ba; subBossActive=sv.sba;
    run.weapon=sv.w; run.wlevel=sv.wl; run.infusion=sv.inf; shake=sv.sh;
  }
}
function forgePreviewTick(P,VWp,VHp,dt){
  if(!P||P.err) return;
  P.t+=dt;
  forgePreviewSwap(P,VWp,VHp,function(){
    P.cd-=dt;
    if(P.cd<=0){ pShoot(); P.fired++; let c=0.2; try{ c=_weaponCadence()||0.2; }catch(_c){ } P.cd=Math.max(0.07,c); }
    for(const b of pBullets){
      if(b._inf===undefined||b.kind==='beam'){ b._inf=(typeof infusionCarrier==='function'&&infusionCarrier(b))?P.elem:null; b._infLv=b._inf?Math.max(1,P.lv):0; }
      /* a weapon with its OWN tick runs it, so the preview shows its real behaviour (the orb splitting) */
      if(typeof yuriLightningOrbTick==='function' && yuriLightningOrbTick(b,dt)) continue;
      if(typeof laserMistTick==='function' && laserMistTick(b,dt)) continue;
      if(typeof spaceBulletTick==='function' && spaceBulletTick(b,dt)) continue;
      if(b.kind==='beam'){ b.life=(b.life==null?0.3:b.life)-dt; if(b.life<=0){ b.dead=true; continue; } b.x=player.x; b.bot=player.y-14; b.top=-20; }
      else if(b.kind==='flame'){ b.life=(b.life==null?0.3:b.life)-dt; b.anim=(b.anim||0)+dt; if(b.life<=0){ b.dead=true; continue; }
        b.x=player.x; b.bot=player.y-14; b.top=b.bot-flameReach(b.lv); b.w=flameBase(b.lv)*2; b.h=flameReach(b.lv); }
      else { b.x+=(b.vx||0); b.y+=(b.vy||0); b.t=(b.t||0)+dt; }
      if(b.y<-80||b.y>VHp+80||b.x<-80||b.x>VWp+80) b.dead=true;
    }
    pBullets=pBullets.filter(function(b){ return !b.dead; });
    if(pBullets.length>90) pBullets=pBullets.slice(pBullets.length-90);
    for(const q of particles){ q.t=(q.t||0)+dt; q.x+=(q.vx||0); q.y+=(q.vy||0); }
    particles=particles.filter(function(q){ return q.t<(q.life||0.3); }).slice(-120);
  });
}
function forgePreviewDraw(P,x,y,w,h){
  ctx.save(); ctx.beginPath(); ctx.rect(x,y,w,h); ctx.clip(); ctx.translate(x,y);
  ctx.fillStyle='#04050a'; ctx.fillRect(0,0,w,h);
  const t=P?P.t:0;
  for(let i=0;i<30;i++){                       /* pixel stars streaming past - it is flying */
    const big=(i%4===0), sx=(i*53.7)%w, sy=((i*97.3)+t*(40+(i%3)*30))%h;
    ctx.fillStyle=big?'#9fb2d8':'#34405a'; ctx.fillRect(Math.floor(sx),Math.floor(sy),big?2:1,big?2:1);
  }
  if(P && !P.err){
    forgePreviewSwap(P,w,h,function(){ drawBullets(); });
    try{ const pk='ship_'+((typeof _pilotKey==='function')?_pilotKey():'axel');
      if(XART.rdy(pk)){ const im=XART.get(pk), sh=Math.min(SHIP_DRAW_H,h*0.2), sw=sh*((im.naturalWidth||im.width)/(im.naturalHeight||im.height));
        ctx.imageSmoothingEnabled=false; ctx.drawImage(im,w/2-sw/2,(h-40)-sh/2,sw,sh); } }catch(_s){ }
  }
  ctx.restore();
}

/* ---- THE FORGING, then THE PRODUCT -------------------------------------------------------------- */
let forging=null;
function forgingStart(o){
  forging={w:o.w|0, elem:o.elem, lv:Math.max(1,o.lv|0), t:0, pct:-1, doneT:-1, flash:0, sparks:[], arcs:null, arcT:0,
           preview:null, md:!!(Input&&Input.mouse&&Input.mouse.down)};
  try{ ['forge_chamber_0917b','inf_'+o.elem,forgeBadgeKey(o.elem,o.w,o.lv),'ship_'+_pilotKey(),_selKey('y')].forEach(function(k){ XART.rdy(k); });
       XART.rdy(weaponIconKey(o.w, Math.max(1,(run.wlevels&&run.wlevels[o.w])|0))); }catch(_w){ }
  setState(GS.FORGING);
}
function forgingLeave(toLoadout){
  forging=null;
  const F=forge;
  if(!toLoadout && F){ setState(GS.FORGE); return; }
  const done=F&&F.onDone; forge=null; run._wbag=[];
  if(done) done(); else setState(GS.TITLE);
}
function forgeArc(x0,y0,x1,y1,col,jag){
  const n=9, pts=[[x0,y0]];
  for(let i=1;i<n;i++){ const k=i/n, nx=-(y1-y0), ny=(x1-x0), L=Math.max(1,Math.hypot(nx,ny)), o=(Math.random()*2-1)*jag;
    pts.push([x0+(x1-x0)*k+nx/L*o, y0+(y1-y0)*k+ny/L*o]); }
  pts.push([x1,y1]);
  return {pts:pts,col:col};
}
function drawForging(dt){
  const FG=forging;
  const W=(typeof cutsceneViewWidth==='function')?cutsceneViewWidth():VW, H=VH;
  ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
  if(!FG){ setState(forge?GS.FORGE:GS.TITLE); return; }
  FG.t+=dt; const t=FG.t;
  const art=(typeof curFontArt==='function')?curFontArt():null;
  const I=INFUSIONS[FG.elem]||{body:'#ffffff',glow:'#ffffff',name:''};
  const product=(state===GS.FORGED);
  const plate=XART.rdy('forge_chamber_0917b')?XART.get('forge_chamber_0917b'):null;
  const fade=product?1:Math.min(1,t/0.35);
  ctx.save(); ctx.globalAlpha=fade;
  if(plate){ ctx.imageSmoothingEnabled=false; ctx.drawImage(plate,0,0,W,H); } else { ctx.fillStyle='#161a22'; ctx.fillRect(0,0,W,H); }
  ctx.restore();
  const C=FORGE_CHAMBER, hw=frc(C.hexW,W,H), he=frc(C.hexE,W,H), ho=frc(C.hexOut,W,H), core=frc(C.core,W,H);
  const cW=[hw[0]+hw[2]/2,hw[1]+hw[3]/2], cE=[he[0]+he[2]/2,he[1]+he[3]/2], cO=[ho[0]+ho[2]/2,ho[1]+ho[3]/2];
  const p=product?1:Math.max(0,Math.min(1,(t-FORGE_WELD_T0)/FORGE_WELD_T));
  const welding=!product && t>=FORGE_WELD_T0 && p<1;
  if(!product && p>=1 && FG.doneT<0){ FG.doneT=t; FG.flash=1; shake=Math.max(shake,4); fsx('powerup'); fsx('life'); }
  if(welding && FG.pct<0){ fsx('beamCharge')||fsx('laserCharge')||fsx('retinaCharge'); }
  const pct=Math.floor(p*100);
  if(welding && Math.floor(pct/10)!==Math.floor(Math.max(0,FG.pct)/10)) fsx('blip');
  FG.pct=pct;
  const glowA=product?0.35+0.12*Math.sin(t*4):(0.10+0.55*p);

  /* the chamber's own light, in the element's colour, rising with the weld */
  ctx.save(); ctx.globalCompositeOperation='lighter';
  const gr=ctx.createRadialGradient(core[0]+core[2]/2,core[1]+core[3]/2,2,core[0]+core[2]/2,core[1]+core[3]/2,core[2]*0.55);
  gr.addColorStop(0,I.glow); gr.addColorStop(1,'rgba(0,0,0,0)');
  ctx.globalAlpha=glowA*fade; ctx.fillStyle=gr; ctx.fillRect(core[0],core[1],core[2],core[3]);
  ctx.restore();

  /* the two inputs, seated in their sockets; they shiver as the weld takes them */
  const jit=welding?p*2.2:0;
  const inA=product?0.30:(FG.doneT>=0?Math.max(0.30,1-(t-FG.doneT)*1.6):Math.min(1,t/0.45));
  const wKey=weaponIconKey(FG.w, Math.max(1,(run.wlevels&&run.wlevels[FG.w])|0));
  forgeIconFit(wKey, cW[0]+(Math.random()*2-1)*jit, cW[1]+(Math.random()*2-1)*jit, hw[3]*0.80, 0, inA*fade);
  forgeIconFit('inf_'+FG.elem, cE[0]+(Math.random()*2-1)*jit, cE[1]+(Math.random()*2-1)*jit, he[3]*0.80, 0, inA*fade);

  /* arcs down the pipes and sparks riding them into the output */
  if(welding){
    FG.arcT-=dt;
    if(FG.arcT<=0){ FG.arcT=0.05; const j=4+p*9;
      FG.arcs=[forgeArc(cW[0],cW[1],cO[0],cO[1],I.glow,j), forgeArc(cE[0],cE[1],cO[0],cO[1],I.glow,j)]; }
    for(let k=0;k<2;k++){ if(Math.random()<0.4+p*0.5){ const s0=k?cE:cW;
      FG.sparks.push({x:s0[0],y:s0[1],tx:cO[0],ty:cO[1],t:0,life:0.35+Math.random()*0.25,c:Math.random()<0.5?I.body:'#ffffff'}); } }
  } else FG.arcs=null;
  if(FG.arcs){
    ctx.save(); ctx.globalCompositeOperation='lighter'; ctx.lineJoin='round';
    for(const A of FG.arcs){
      for(const pass of [[4,A.col,0.45],[1.6,'#ffffff',0.95]]){
        ctx.globalAlpha=pass[2]; ctx.strokeStyle=pass[1]; ctx.lineWidth=pass[0]; ctx.beginPath();
        A.pts.forEach(function(q,i){ if(i) ctx.lineTo(q[0],q[1]); else ctx.moveTo(q[0],q[1]); }); ctx.stroke();
      }
    }
    ctx.restore();
  }
  FG.sparks=FG.sparks.filter(function(s){ s.t+=dt; return s.t<s.life; });
  ctx.save(); ctx.globalCompositeOperation='lighter';
  for(const s of FG.sparks){ const k=s.t/s.life, x=s.x+(s.tx-s.x)*k, y=s.y+(s.ty-s.y)*k+Math.sin(k*9)*3;
    ctx.globalAlpha=1-k*0.6; ctx.fillStyle=s.c; ctx.fillRect(Math.round(x)-1,Math.round(y)-1,3,3); }
  ctx.restore();

  /* the output: nothing until 100%, then the FORGED badge pops into the cyan socket */
  if(FG.doneT>=0 || product){
    const since=product?9:(t-FG.doneT), pop=1+0.6*Math.max(0,1-since/0.28);
    const bk=forgeBadgeKey(FG.elem,FG.w,FG.lv);
    ctx.save(); ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=0.35+0.25*Math.sin(t*6);
    const og=ctx.createRadialGradient(cO[0],cO[1],1,cO[0],cO[1],ho[3]*0.95);
    og.addColorStop(0,I.glow); og.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle=og; ctx.fillRect(cO[0]-ho[3],cO[1]-ho[3],ho[3]*2,ho[3]*2);
    ctx.restore();
    forgeIconFit(bk, cO[0], cO[1], ho[3]*0.86*pop, 0, 1);
  }

  /* the left column: the loadout while it welds, the five LEVELS once it is made */
  const art2=art;
  for(let i=0;i<5;i++){
    const r=frc(C.slots[i],W,H), cx=r[0]+r[2]/2, cy=r[1]+r[3]/2;
    /* the loadout, in both phases - levels are the in-game upgrade, not the Forge's (Mike, 0917c) */
    {
      const L=run.loadout||[], at=Math.max(0,L.indexOf(FG.w)), from=Math.max(0,Math.min(Math.max(0,L.length-5),at-2)), w2=L[from+i];
      if(w2==null) continue;
      forgeIconFit(forgeSlotKey(w2), cx, cy, r[3]*0.80, r[2]*0.62, (w2===FG.w?1:0.35)*fade);
    }
  }

  /* the tall glass: the rounds themselves once it is made; the recipe while it is being made */
  const V=frc(C.view,W,H), vin=[V[0]+5,V[1]+5,V[2]-10,V[3]-10];
  if(product){
    if(!FG.preview) FG.preview=forgePreviewNew(FG.w,FG.elem,FG.lv);
    forgePreviewTick(FG.preview,vin[2],vin[3],dt);
    forgePreviewDraw(FG.preview,vin[0],vin[1],vin[2],vin[3]);
  } else if(art2){
    const lines=[WEAPONS[FG.w]||'WEAPON','+',I.name,'=',(FG.doneT>=0?'FORGED':'?')];
    const lh=Math.min(V[3]*0.06,(typeof stageFitH==='function')?stageFitH(art2,'MACHINE GUN',V[2]*0.84,V[3]*0.06,7,0.06):11);
    lines.forEach(function(s,i){ stageText(art2,s,V[0]+V[2]/2,V[1]+V[3]*(0.22+i*0.14),lh,i===2?I.body:(i===4?'#ffffff':'#9fd6ff'),0.85,Math.min(1,Math.max(0,(t-0.3-i*0.18)/0.3)),0.06); });
  }

  /* the trough: 0-100% as the weld runs, the product's name and power once it is made */
  const B=frc(C.bar,W,H), bi=[B[0]+B[3]*0.22,B[1]+B[3]*0.22,B[2]-B[3]*0.44,B[3]*0.56];
  if(!product){
    const blocks=24, bw=bi[2]/blocks, on=Math.floor(p*blocks+1e-6);
    for(let k=0;k<on;k++){ ctx.fillStyle=(k%2)?I.body:I.glow; ctx.fillRect(Math.round(bi[0]+k*bw)+1,Math.round(bi[1]),Math.max(1,Math.round(bw)-2),Math.round(bi[3])); }
    const txt=(FG.doneT>=0)?'FORGED!':('FORGING   '+pct+'%');
    if(art2) stageText(art2,txt,B[0]+B[2]/2,B[1]+B[3]/2,Math.min(B[3]*0.46,14),'#ffffff',0.9,fade,0.08);
  } else if(art2){
    const nm=(WEAPONS[FG.w]||'WEAPON')+'   +   '+I.name;
    const nh=Math.min(B[3]*0.46,(typeof stageFitH==='function')?stageFitH(art2,nm,B[2]*0.92,B[3]*0.46,7,0.06):12);
    stageText(art2,nm,B[0]+B[2]/2,B[1]+B[3]/2,nh,I.body,0.85,1,0.06);
  }

  /* the product's NAME, typed across the plating above the chamber */
  if(art2 && (product || FG.doneT>=0)){
    const T=frc(C.title,W,H), full=forgeComboName(FG.elem,FG.w);
    const since=product?Math.max(0,t-(FG.productT||0)):0;
    const shown=product?full.slice(0,Math.max(0,Math.round(since*28))):'';
    if(shown){
      const th=Math.min(T[3]*0.72,(typeof stageFitH==='function')?stageFitH(art2,full,T[2],T[3]*0.72,9,0.08):T[3]*0.6);
      const fw=stageWidth(art2,full,th,0.08), sw=stageWidth(art2,shown,th,0.08);
      stageText(art2,shown,T[0]+T[2]/2-fw/2+sw/2,T[1]+T[3]/2,th,I.body,0.9,1,0.08);
      if(since<full.length/28 && Math.floor(since*28)!==Math.floor((since-dt)*28)) fsx('blip');
    }
  }

  /* the white of the weld landing */
  if(FG.flash>0){ ctx.save(); ctx.globalAlpha=Math.min(1,FG.flash)*0.85; ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H); ctx.restore(); FG.flash=Math.max(0,FG.flash-dt*2.4); }

  /* controls */
  const moreCombos=!!(forge && (run.forgeCombos|0)>0 && forgeDiscovered().length);
  /* B always returns to the Forge: with no combine left it still has RE-SPEC and the ARMORY */
  const hints=product?[['pad_a','LOADOUT'],['pad_b',moreCombos?'FORGE MORE':'FORGE']]:[['pad_a','SKIP']];
  if(t>0.5) controlHintRow(hints,H*0.968,W/2,W-24);

  /* input - every consuming reader read ONCE */
  const mB=(Input.menuBack?Input.menuBack():false), mS=(Input.menuStart?Input.menuStart():false);
  const fire=(keybind.fire||[]).filter(function(k){ return !/^mouse/.test(k); }).some(function(k){ return Input.tap(k); });
  const click=Input.mouse.down&&!FG.md; FG.md=!!Input.mouse.down;
  const go=fire||click||mS||Input.tap('enter');
  if(!product){
    if(go && t>0.4 && FG.doneT<0){ FG.t=Math.max(FG.t,FORGE_WELD_T0+FORGE_WELD_T); }        /* a press finishes the weld */
    else if(FG.doneT>=0 && (t-FG.doneT>FORGE_PRODUCT_WAIT || (go && t-FG.doneT>0.3))){ FG.productT=t; setState(GS.FORGED); }
    return;
  }
  if(t-(FG.productT||0)<0.4) return;
  if(mB){ fsx('blip'); forgingLeave(false); }
  else if(go){ Input.mouse.down=false; fsx('blip'); forgingLeave(true); }
}

/* ---- THE LOADOUT: six bays and the pool (Mike, 0917b: "the 6 box loadout screen") --------------- */
let loadoutScr=null;
/* ⚠ IT OPENS WHEN THERE IS A CHOICE, OR WHEN THE FORGE RAN. More weapons than bays is a real choice;
   after a weld it is the "confirm and launch" beat of Mike's order (forge -> forging -> product ->
   loadout -> fade). A player whose six weapons already fill the six bays and who forged nothing has
   nothing to decide here, and an empty page teaches mashing - the Forge's own rule (forgeVisible). The
   first cut opened it for any pool over ONE and the arcade route check caught it: a plain arcade clear
   must still go straight to the next stage (0915). */
function loadoutVisible(){
  if(!run) return false;
  if(typeof spaceWeaponsActive==='function' && spaceWeaponsActive()) return false;
  const pool=(typeof crateWeaponPool==='function')?crateWeaponPool(true):[];
  return pool.length>FORGE_LOADOUT_MAX || !!run._forgeShown;
}
function loadoutStart(onDone){
  const load=forgeLoadoutSync();
  const pool=(typeof crateWeaponPool==='function')?crateWeaponPool(true):load.slice();
  loadoutScr={onDone:onDone||null, t:0, sel:0, row:0, psel:0, pscroll:0, exitT:-1, msg:'', msgT:0, pool:pool,
              md:!!(Input&&Input.mouse&&Input.mouse.down)};
  try{ XART.rdy('loadout_bays_0917b'); XART.rdy(_selKey('y'));
       for(const w of pool){ XART.rdy(weaponIconKey(w,Math.max(1,(run.wlevels&&run.wlevels[w])|0))); const f=forgeEntry(w); if(f) XART.rdy(forgeBadgeKey(f.elem,w,f.lv)); }
       if(typeof laserMistWarm==='function') laserMistWarm(); }catch(_l){ }
  setState(GS.LOADOUT);
}
function loadoutSay(m,sfx){ if(loadoutScr){ loadoutScr.msg=m; loadoutScr.msgT=2.2; } if(sfx) fsx(sfx); }
function drawLoadout(dt){
  const L=loadoutScr;
  const W=(typeof cutsceneViewWidth==='function')?cutsceneViewWidth():VW, H=VH;
  ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
  if(!L){ setState(GS.TITLE); return; }
  L.t+=dt; const t=L.t; if(L.msgT>0) L.msgT-=dt;
  const art=(typeof curFontArt==='function')?curFontArt():null;
  const P=LOADOUT_PLATE, load=run.loadout||[];
  const A=function(d){ return Math.max(0,Math.min(1,(t-d)/0.3)); };
  const plate=XART.rdy('loadout_bays_0917b')?XART.get('loadout_bays_0917b'):null;
  ctx.save(); ctx.globalAlpha=Math.min(1,t/0.4);
  if(plate){ ctx.imageSmoothingEnabled=false; ctx.drawImage(plate,0,0,W,H); } else { ctx.fillStyle='#161a22'; ctx.fillRect(0,0,W,H); }
  ctx.restore();
  L.sel=clamp(L.sel|0,0,Math.max(0,load.length-1));
  const selW=load[L.sel];
  if(art){
    const T=frc(P.title,W,H), tt='LOADOUT   '+load.length+' OF '+FORGE_LOADOUT_MAX;
    stageText(art,tt,T[0]+T[2]/2,T[1]+T[3]/2,Math.min(T[3]*0.56,(typeof stageFitH==='function')?stageFitH(art,tt,T[2]*0.9,T[3]*0.56,9,0.08):T[3]*0.5),'#ffd24a',0.9,A(0.1),0.08);
  }
  /* the six bays */
  for(let i=0;i<FORGE_LOADOUT_MAX;i++){
    const w=load[i], a=A(0.25+i*0.07);
    const bx=P.bayX[i]*W, by=P.bayY*H, bw=P.bayW*W, bh=P.bayH*H, cx=bx+bw/2, cy=by+bh/2;
    if(w==null||a<=0) continue;
    const key=forgeSlotKey(w);
    forgeIconFit(key,cx,cy,Math.min(bh,bw)*0.86,0,a);   /* centred, never stretched */
    const f=forgeEntry(w), nm=(typeof weaponDisplayName==='function')?weaponDisplayName(w):WEAPONS[w];
    if(art){ const sx=P.stripX[i]*W, sy=P.stripY*H, sw2=P.stripW*W, sh2=P.stripH*H;
      const nh=Math.min(sh2*0.56,(typeof stageFitH==='function')?stageFitH(art,nm,sw2*0.9,sh2*0.56,6,0.05):sh2*0.5);
      stageText(art,nm,sx+sw2/2,sy+sh2/2,nh,f?INFUSIONS[f.elem].body:'#c8d2e2',0.8,a,0.05); }
    if(i===L.sel && L.exitT<0){
      ctx.save(); ctx.globalAlpha=(L.row===0?1:0.45); if(L.row===0) forgeHexPointer(key,cx,cy,Math.min(bh,bw)*0.86,'#ffd24a'); ctx.restore();
      if(L.row===0) forgeSelArrowUp(cx, by+bh+H*0.004, H*0.050);
    }
  }
  /* the pool: every unlocked weapon, a scrolling strip - dim until a bay is opened */
  const PB=frc(P.pool,W,H), pa=A(0.7);
  if(pa>0){
    ctx.save(); ctx.globalAlpha=pa*0.9; ctx.fillStyle='#0a0c12'; ctx.fillRect(PB[0],PB[1],PB[2],PB[3]);
    ctx.globalAlpha=pa; ctx.strokeStyle=L.row===1?'#ffd24a':'#566074'; ctx.lineWidth=2; ctx.strokeRect(PB[0]+1,PB[1]+1,PB[2]-2,PB[3]-2); ctx.restore();
    const n=L.pool.length, view=Math.min(n,7);
    L.psel=clamp(L.psel|0,0,Math.max(0,n-1));
    const maxS=Math.max(0,n-view); L.pscroll=clamp(Math.min(L.pscroll|0,L.psel),L.psel-view+1,maxS); L.pscroll=clamp(L.pscroll,0,maxS);
    const pitch=PB[2]/7, ih=PB[3]*0.62, ox=PB[0]+(PB[2]-pitch*view)/2;
    for(let k=0;k<view;k++){
      const i=k+L.pscroll, w=L.pool[i], cx=ox+pitch*(k+0.5), cy=PB[1]+PB[3]*0.42;
      const inL=load.indexOf(w), isSel=(L.row===1&&i===L.psel);
      const key=forgeSlotKey(w);
      forgeIconFit(key,cx,cy,ih,0,pa*(L.row===1?(isSel?1:0.6):0.45));
      if(inL>=0 && art) stageText(art,String(inL+1),cx+ih*0.46,PB[1]+PB[3]*0.16,Math.max(7,PB[3]*0.16),'#9fd6ff',0.8,pa,0.05);
      if(isSel){ forgeHexPointer(key,cx,cy,ih,'#ffd24a'); forgeSelArrowUp(cx,cy+ih*0.52,PB[3]*0.30); }
    }
    ctx.save(); ctx.fillStyle='#9fd6ff'; ctx.globalAlpha=pa*0.85;
    const ah=PB[3]*0.22, ay=PB[1]+PB[3]/2;
    if(L.pscroll>0){ ctx.beginPath(); ctx.moveTo(PB[0]+6,ay); ctx.lineTo(PB[0]+6+ah*0.7,ay-ah/2); ctx.lineTo(PB[0]+6+ah*0.7,ay+ah/2); ctx.closePath(); ctx.fill(); }
    if(L.pscroll<maxS){ ctx.beginPath(); ctx.moveTo(PB[0]+PB[2]-6,ay); ctx.lineTo(PB[0]+PB[2]-6-ah*0.7,ay-ah/2); ctx.lineTo(PB[0]+PB[2]-6-ah*0.7,ay+ah/2); ctx.closePath(); ctx.fill(); }
    ctx.restore();
  }
  /* the information bar: what the cursor is on */
  if(art){
    const IB=frc(P.info,W,H);
    let txt, col='#ffd24a';
    if(L.msgT>0 && L.msg){ txt=L.msg; col='#ffffff'; }
    else if(L.row===1){ const w=L.pool[L.psel], j=load.indexOf(w); txt=((typeof weaponDisplayName==='function')?weaponDisplayName(w):WEAPONS[w])+(j>=0?('   -   IN BAY '+(j+1)):'   -   FIRE PUTS IT IN BAY '+(L.sel+1)); }
    else if(selW!=null){ const f=forgeEntry(selW); txt='BAY '+(L.sel+1)+':  '+((typeof weaponDisplayName==='function')?weaponDisplayName(selW):WEAPONS[selW])+(f?('   -   '+INFUSIONS[f.elem].name):''); if(f) col=INFUSIONS[f.elem].body; }
    else txt='NOTHING UNLOCKED';
    const th=Math.min(IB[3]*0.46,(typeof stageFitH==='function')?stageFitH(art,txt,IB[2]*0.94,IB[3]*0.46,7,0.06):12);
    stageText(art,txt,IB[0]+IB[2]/2,IB[1]+IB[3]/2,th,col,0.85,A(0.4),0.06);
  }
  if(A(0.6)>0 && L.exitT<0){
    const hints=(L.row===1)?[['pad_dpad','SCROLL'],['pad_a','EQUIP'],['pad_b','BACK']]:[['pad_dpad','BAY'],['pad_a','CHANGE'],['pad_start','LAUNCH']];
    controlHintRow(hints,H*0.968,W/2,W-24);
  }
  /* FADE TO THE NEXT LEVEL (Mike: "the loadout selection screen - fade to next level") */
  if(L.exitT>=0){
    L.exitT+=dt;
    ctx.save(); ctx.globalAlpha=Math.min(1,L.exitT/0.6); ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H); ctx.restore();
    if(L.exitT>=0.62){ const done=L.onDone; loadoutScr=null; run._wbag=[]; if(done) done(); else setState(GS.TITLE); }
    return;
  }
  /* input - every consuming reader read ONCE (menuLeft()||menuRight() is always +1 otherwise) */
  const mL=(Input.menuLeft?Input.menuLeft():false), mR=(Input.menuRight?Input.menuRight():false);
  const mU=(Input.menuUp?Input.menuUp():false), mD=(Input.menuDown?Input.menuDown():false);
  const mB=(Input.menuBack?Input.menuBack():false), mS=(Input.menuStart?Input.menuStart():false);
  const fire=(keybind.fire||[]).filter(function(k){ return !/^mouse/.test(k); }).some(function(k){ return Input.tap(k); });
  const click=Input.mouse.down&&!L.md; L.md=!!Input.mouse.down;
  const enter=Input.tap('enter');
  if(t<0.6) return;
  if(L.row===0){
    if(mL && load.length){ L.sel=(L.sel-1+load.length)%load.length; fsx('blip'); }
    else if(mR && load.length){ L.sel=(L.sel+1)%load.length; fsx('blip'); }
    else if(mS||enter){ Input.mouse.down=false; L.exitT=0; fsx('powerup'); }
    else if((fire||click||mD) && selW!=null){
      if(FORGE_FIXED[selW]) loadoutSay('MISSILES STAY MISSILES','blocked');
      else if(L.pool.length<2) loadoutSay('NOTHING ELSE UNLOCKED YET','blocked');
      else { L.row=1; L.psel=Math.max(0,L.pool.indexOf(selW)); L.pscroll=0; fsx('blip'); }
    }
  } else {
    const n=L.pool.length;
    if(mL && n){ L.psel=(L.psel-1+n)%n; fsx('blip'); }          /* a ding on every icon */
    else if(mR && n){ L.psel=(L.psel+1)%n; fsx('blip'); }
    else if(mB||mU){ L.row=0; fsx('blip'); }
    else if(fire||click||enter){
      const w=L.pool[L.psel], r=forgePick(L.sel,w);
      if(r==='fixedelsewhere') loadoutSay('MISSILES STAY IN THEIR OWN BAY','blocked');
      else if(r==='fixed') loadoutSay('MISSILES STAY MISSILES','blocked');
      else { if(r==='ok') loadoutSay('BAY '+(L.sel+1)+':  '+((typeof weaponDisplayName==='function')?weaponDisplayName(w):WEAPONS[w]),'powerup'); else fsx('blip'); L.row=0; }
    }
  }
}
