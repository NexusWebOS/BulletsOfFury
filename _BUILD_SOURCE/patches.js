// ============ NEW JS BLOCKS (injected by assemble.py) ============


// [B_XART] inserted right before "function drawBossSprite(b){"
const B_XART = String.raw`/* ===== EXTRA ART (boot / menu / cinematic) + boot chime ===== */
/* ============================================================
   LOAD-ERROR REPORTER (drop 0724de)

   Mike has now reported the same two symptoms three times — no boot chime, dead menu — and I have
   twice shipped a fix for a cause I could not reproduce. Both symptoms are what you get when the
   script THROWS during load: everything after the throw never runs, so the input listeners are
   never attached and the chime is never reached.

   I cannot see his console from here. So instead of guessing a third time, the game now catches
   its own load failure and PAINTS it on the canvas — the message, the file, the line. That turns
   an invisible failure into something Mike can photograph in one second.
   ============================================================ */
(function(){
  if(typeof window==='undefined') return;
  function paint(msg, src, line){
    try{
      var cv=document.getElementById('cv')||document.querySelector('canvas');
      if(!cv) return;
      var c=cv.getContext('2d'); if(!c) return;
      c.setTransform(1,0,0,1,0,0);
      c.fillStyle='#12060a'; c.fillRect(0,0,cv.width,cv.height);
      c.fillStyle='#ff6a5a'; c.font='bold 15px monospace'; c.textAlign='left';
      c.fillText('BULLETS OF FURY — LOAD ERROR', 14, 30);
      c.fillStyle='#ffd7cf'; c.font='11px monospace';
      var words=String(msg||'unknown').split(' '), lineTxt='', y=58;
      for(var i=0;i<words.length;i++){
        var t=lineTxt+words[i]+' ';
        if(c.measureText(t).width > cv.width-28){ c.fillText(lineTxt,14,y); y+=15; lineTxt=words[i]+' '; }
        else lineTxt=t;
      }
      c.fillText(lineTxt,14,y); y+=24;
      c.fillStyle='#9fb0cd';
      if(src)  c.fillText(String(src).split('/').pop()+(line?('  line '+line):''), 14, y);
      c.fillText('Screenshot this and send it to Claude.', 14, y+20);
    }catch(e){}
  }
  window.addEventListener('error', function(ev){
    paint(ev && ev.message, ev && ev.filename, ev && ev.lineno);
  });
  window.addEventListener('unhandledrejection', function(ev){
    paint('unhandled promise: '+((ev&&ev.reason&&ev.reason.message)||ev&&ev.reason), '', 0);
  });
  /* And a watchdog: if nothing has drawn a frame after 8 seconds, the loop never started. */
  window.__bofFrames=0;
  setTimeout(function(){
    if((window.__bofFrames|0) < 3) paint('The render loop never started — the script stopped before it could begin. If no error is shown above, check the browser console.', '', 0);
  }, 8000);
})();

const XART=(function(){
  const X={img:{}};
  function mk(o){ if(!o) return null; const im=new Image(); im.src=(typeof o==='string')?o:('data:'+o.m+';base64,'+o.d); return im; }
  /* LAZY LOADING (drop 0724db).
     This used to build a new Image() for EVERY key the moment the file parsed. The manifest has
     grown to 7,166 images totalling 295 MB, so that fired 7,166 simultaneous requests before the
     first frame — which is why the browser crawled, the menu would not respond, and the boot chime
     never got the bandwidth to decode. One cause, all three symptoms.

     Images are now created on FIRST USE. Every call site already guards on rdy(), which returns
     false until an image has decoded, so nothing has to change anywhere else: a sprite simply
     appears a frame or two after something first asks for it.

     PRELOAD is the short list needed before the player can act — boot, title, the pilots. Those
     are fetched immediately so the opening is never waiting on a lazy miss. */
  /* newbootimage was MISSING from this list, so the loading screen had nothing to cover with —
     four seconds of black before the title. Caught by reading the loading screen, not by testing. */
  /* HELD-WEAPON FX ARE NOW EAGER (drop 0801be). nhxv_/nhxsb_ (Maverick's helix)
     and nfw_ (the flamethrower) are drawn every frame the button is down, and
     both draw paths ask XART.rdy() — load state — before committing. Lazily
     loaded, that meant the first shots of a life rendered nothing (or, before
     this drop, fell through to another weapon's art). Preloading them removes
     the question entirely: by the time the player can fire, the art is decoded. */
  const PRELOAD = /^(cf_boot|cf_logo|logo|startile|newbootimage|bootimage|scard_1|ship_|nthp_|port_|card_|face_|menu|btn_|nui_|nhxv_|nhxsb_|nfw_)/;
  X._src = (window.BOFX && BOFX.img) ? BOFX.img : {};
  /* get() MUST NEVER HAND drawImage A NULL (drop 0724dq).
     Mike is seeing THOUSANDS of draw errors mentioning HTMLImageElement. That is this:
         ctx.drawImage(XART.get(k), ...)   with k missing or not yet decoded
     returns null, and drawImage throws
         "The provided value is not of type '(CSSImageValue or HTMLImageElement or ...)'"
     EVERY FRAME. The loop catches it, so nothing crashes — the frame just stops drawing at that
     point, which is why the menu renders but never finishes its update. It was always happening;
     DBG.verbose merely stopped hiding it after the first report.
     Most call sites DO guard with rdy(), but not all, and a lazy loader makes the unguarded ones
     fire constantly instead of rarely. A 1x1 transparent image is a valid drawImage argument and
     draws nothing, so an unloaded or missing asset now costs a blank pixel rather than the rest of
     the frame. */
  const _BLANK=(function(){
    try{
      const c=document.createElement('canvas'); c.width=1; c.height=1;
      return c;                      // a canvas is a legal CanvasImageSource, and needs no decode
    }catch(e){ return null; }
  })();
  X._touch=function(k){
    if(X.img[k]!==undefined) return X.img[k];
    const src=X._src[k];
    X.img[k]= src ? mk(src) : null;
    return X.img[k];
  };
  X.safe=function(k){
    const im=X._touch(k);
    return (im && im.complete && im.naturalWidth>0) ? im : _BLANK;
  };
  if(window.BOFX&&BOFX.img){ for(const k in BOFX.img) if(PRELOAD.test(k)) X._touch(k); }
  /* get() is used in hundreds of places, many of them feeding drawImage directly. It now returns a
     drawable blank rather than null when the asset is not ready. rdy() is unchanged, so any code
     that CHECKS first still behaves exactly as before. */
  X.get=function(k){ return X.safe(k); };
  X.raw=function(k){ return X._touch(k); };      // for the few places that need the real object
  X.rdy=function(k){ const im=X._touch(k); return !!(im&&im.complete&&im.naturalWidth>0); };
  X.cover=function(k,alpha){ const im=X.img[k]; if(!X.rdy(k)) return false;
    const sc=Math.max(VW/im.naturalWidth, VH/im.naturalHeight), dw=im.naturalWidth*sc, dh=im.naturalHeight*sc;
    if(alpha!=null){ctx.save();ctx.globalAlpha=alpha;} ctx.drawImage(im,(VW-dw)/2,(VH-dh)/2,dw,dh); if(alpha!=null)ctx.restore(); return true; };
  X.draw=function(k,cx,cy,w,alpha){ const im=X.img[k]; if(!X.rdy(k)) return null;
    const h=w*(im.naturalHeight/im.naturalWidth); if(alpha!=null){ctx.save();ctx.globalAlpha=alpha;}
    ctx.drawImage(im,Math.round(cx-w/2),Math.round(cy-h/2),Math.round(w),Math.round(h)); if(alpha!=null)ctx.restore(); return {w:w,h:h}; };
  return X;
})();
const _xtc=document.createElement('canvas'), _xtx=_xtc.getContext('2d');
function flashImg(im,x,y,w,h,alpha){ if(!im||!im.naturalWidth) return;
  _xtc.width=im.naturalWidth;_xtc.height=im.naturalHeight;
  _xtx.globalCompositeOperation='source-over';_xtx.globalAlpha=1;_xtx.clearRect(0,0,_xtc.width,_xtc.height);
  _xtx.drawImage(im,0,0); _xtx.globalCompositeOperation='source-atop'; _xtx.globalAlpha=alpha; _xtx.fillStyle='#fff';
  _xtx.fillRect(0,0,_xtc.width,_xtc.height); _xtx.globalAlpha=1; _xtx.globalCompositeOperation='source-over';
  ctx.drawImage(_xtc,Math.round(x),Math.round(y),Math.round(w),Math.round(h));
}
const BootChime=(function(){
  if(!window.BOFX||!BOFX.chime||!window.Audio) return null;
  /* The chime is fetched EAGERLY and ahead of everything else. It is one small file and it is the
     first thing the player hears; under the old eager image loader it was competing with 7,166
     simultaneous requests and simply never arrived in time. */
  const a=new window.Audio(); a.src=(typeof BOFX.chime==='string')?BOFX.chime:('data:'+BOFX.chime.m+';base64,'+BOFX.chime.d); a.preload='auto';
  try{ a.load(); }catch(e){}
  return { play(v){ try{ a.currentTime=0; a.volume=(v==null?1:v); const p=a.play(); if(p&&p.catch)p.catch(function(){}); }catch(e){} },
    unlock(){ try{ a.muted=true; const p=a.play(); if(p&&p.then){ p.then(function(){ a.pause(); a.currentTime=0; a.muted=false; }).catch(function(){ a.muted=false; }); } else { a.pause(); a.muted=false; } }catch(e){} } };
})();
function hx(h){ h=String(h).replace('#',''); return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)]; }
function rgba(c,a){ return 'rgba('+c[0]+','+c[1]+','+c[2]+','+a+')'; }
function lighten(h,f){ const c=hx(h); const r=Math.min(255,Math.round(c[0]+(255-c[0])*f)); const g=Math.min(255,Math.round(c[1]+(255-c[1])*f)); const b=Math.min(255,Math.round(c[2]+(255-c[2])*f)); return 'rgb('+r+','+g+','+b+')'; }
function anyTap(){ for(const k in Input.keys){ if(Input.tap(k)) return true; } return false; }
/* ============================================================
   SPRITE GAME FONT (drop 0724cq)

   The game's text was drawn with ctx.fillText in a TTF. This routes EVERY text call through the
   94-glyph sprite font instead — uniform 32x40 cells, ASCII 33..126, the fullest set we own.

   It is installed by WRAPPING ctx.fillText once rather than editing 132 call sites. Every existing
   call keeps working unchanged: the wrapper reads ctx.font for the size, ctx.textAlign for the
   anchor and ctx.fillStyle for the colour, and falls straight back to the original fillText for
   anything the sprite font cannot draw. One install point, one place to turn it off.

   METRICS, measured from the glyphs rather than guessed:
     cell 32x40, glyph cap height median 22px, baseline median at y=29 of the cell.
   So a request for "16px" draws a cell of 16*(40/22) and places its top at baseline-29*scale,
   which lands the sprite where the TTF would have put it.
   ============================================================ */
const GF = {
  /* DEFAULT OFF (drop 0724cr). Wrapping ctx.fillText broke input at the start screen in the
     browser — a symptom I could not reproduce in the harness, which stubs the canvas. Shipping a
     build I cannot verify is worse than shipping the TTF, so the sprite font is off by default and
     the game runs exactly as it did before. Set GF.on=true in the console to try it. */
  on: false,
  cell: [32, 40], cap: 22, base: 29,
  track: 0.86,                 // glyph advance as a fraction of cell width — the cells carry padding
  _tint: new Map(),
  key(ch){
    const c = ch.charCodeAt(0);
    if(c < 33 || c > 126) return null;                       // space and control chars have no glyph
    // the extractor names punctuation cNNN (three digits) — padding to two produced 'c33' for '!'
    // and every punctuation glyph silently failed to resolve.
    if(!/[A-Za-z0-9]/.test(ch)) return 'ncm_font_c' + String(c).padStart(3,'0');
    /* CASE-INSENSITIVE (drop 0801by). The gamefont exports one file per letter,
       but SIX landed as lowercase filenames — ncm_font_b, _g, _m, _n, _p, _v —
       almost certainly a case collision at export. Every other letter is
       uppercase. A straight lookup therefore resolves 20 of 26 for uppercase
       text and 6 of 26 for lowercase, and WHICH six flip depending on the case
       you ask for. That is what the harness reported as "missing BGMNPV", and
       after the aliases went in, "missing acdefh" — same defect, other side.

       The face has no case distinction, it is one set of caps, so the lookup
       tries the character then the other case. No caller has to know which way
       a given glyph happened to export. */
    const k='ncm_font_'+ch;
    if(typeof XART!=='undefined' && XART._src && XART._src[k]) return k;
    const alt=(ch===ch.toUpperCase())?ch.toLowerCase():ch.toUpperCase();
    const k2='ncm_font_'+alt;
    if(typeof XART!=='undefined' && XART._src && XART._src[k2]) return k2;
    return k;
  },
  ready(){
    return this.on && typeof XART !== 'undefined' && XART.rdy && XART.rdy('ncm_font_A');
  },
  sizeOf(fontStr){
    const m = /(\d+(?:\.\d+)?)px/.exec(fontStr || '');
    return m ? parseFloat(m[1]) : 10;
  },
  glyph(k, colour){
    if(!colour || colour === '#ffffff' || colour === '#fff') return XART.get(k);
    const id = k + '|' + colour;
    if(this._tint.has(id)) return this._tint.get(id);
    let g = null;
    try { g = (typeof xartTint === 'function') ? xartTint(k, colour, 1) : null; } catch(e){ g = null; }
    if(this._tint.size > 900) this._tint.clear();            // bounded: colours are few, but never unbounded
    this._tint.set(id, g);
    return g || XART.get(k);
  },
  width(text, px){
    const sc = px / this.cap;
    return String(text).length * this.cell[0] * sc * this.track;
  },
  draw(c2, text, x, y){
    const px = this.sizeOf(c2.font);
    const sc = px / this.cap;
    const cw = this.cell[0] * sc, chh = this.cell[1] * sc;
    const adv = cw * this.track;
    const str = String(text);
    let ox = x;
    const al = c2.textAlign;
    if(al === 'center') ox = x - (str.length * adv) / 2;
    else if(al === 'right' || al === 'end') ox = x - str.length * adv;
    const top = y - this.base * sc;                          // fillText's y is the BASELINE
    const colour = (typeof c2.fillStyle === 'string') ? c2.fillStyle : null;
    for(let i = 0; i < str.length; i++){
      const ch = str[i];
      if(ch === ' ') { ox += adv; continue; }
      const k = this.key(ch);
      if(k && XART.rdy(k)){
        const im = this.glyph(k, colour);
        if(im) c2.drawImage(im, ox + (adv - cw) / 2, top, cw, chh);
      }
      ox += adv;
    }
    return true;
  }
};
function installGameFont(c2){
  if(!c2 || c2._gfWrapped) return;
  const orig = c2.fillText.bind(c2);
  const origMeasure = c2.measureText.bind(c2);
  c2._gfOrigFillText = orig;
  c2.fillText = function(text, x, y, maxW){
    if(GF.ready()){
      try { if(GF.draw(c2, text, x, y)) return; } catch(e){ /* fall through to the TTF */ }
    }
    return orig(text, x, y, maxW);
  };
  c2.measureText = function(text){
    if(GF.ready()){
      try { return { width: GF.width(text, GF.sizeOf(c2.font)) }; } catch(e){}
    }
    return origMeasure(text);
  };
  c2._gfWrapped = true;
}
function drawBootBackdrop(dt,darken){
  if(XART.rdy('nbt_1')){ XART.cover('nbt_1');
  } else if(XART.rdy('bootimage')){ XART.cover('bootimage');
    ctx.fillStyle='rgba(6,5,14,'+(darken==null?0.5:darken)+')'; ctx.fillRect(0,0,VW,VH);
  } else { drawTitleBackdrop(dt); }
}
`;

// [B_PILOTS] inserted right after the "let DIFF = DIFFS.normal;" line
const B_PILOTS = String.raw`
const PILOTS=[
  {key:'axel',      name:'AXEL',      role:'COMMANDER',        tint:'#3a8aff', font:3, spd:0.10, fire:0.04, range:0.10},
  {key:'decker',    name:'DECKER',    role:'TECH CONNOISSEUR', tint:'#ffd24a', font:4, spd:-0.04,fire:0.22, range:0.12},
  {key:'maverick',  name:'MAVERICK',  role:'VENOM STRIKE',     tint:'#8de23a', font:1, spd:0.14, fire:0.12, range:0.08},
  {key:'freezer',   name:'FREEZER',   role:'FROSTBITE',        tint:'#6fd0ff', font:3, spd:0.06, fire:0.06, range:-0.02},
  {key:'juggernaut',name:'JUGGERNAUT',role:'UNSTOPPABLE',      tint:'#c08a3a', font:5, spd:-0.08,fire:0.05, range:0.22},
  {key:'yuri',      name:'YURI',      role:'LIGHTNING STRIKE', tint:'#e23a3a', font:2, spd:0.18, fire:0.14, range:0.04},
  {key:'lizzie',    name:'LIZZIE',    role:'BOMBSHELL',        tint:'#ffc21a', font:4, spd:-0.02,fire:0.08, range:0.16},
  {key:'falva',     name:'FALVA',     role:'THE OG',           tint:'#ff2a8f', font:2, spd:0.12, fire:0.16, range:0.06},
  {key:'cole',      name:'COLE',      role:'FLIGHT MASTER',    tint:'#7ad63a', font:1, spd:0.08, fire:0.10, range:0.10, locked:true},
];
// per-pilot special ability: name + short readable description (shown on the select screen)
const SPECIAL_INFO={
  axel:      {name:'AEGIS SHIELD',   desc:'Summons a 5-orb energy shield. Each hit burns one orb.'},
  decker:    {name:'OVERCLOCK',      desc:'Tech surge boosts fire rate and spread for 15s.'},
  maverick:  {name:'VENOM STRIKE',   desc:'Twin venom missiles wind a deadly double-helix.'},
  freezer:   {name:'TIME FREEZE',    desc:'Slows the whole battlefield to half speed for 15s.'},
  juggernaut:{name:'WRECKING BALL',  desc:'Rage mode: invulnerable to enemy fire while active.'},
  yuri:      {name:'CHAIN LIGHTNING',desc:'Bolts arc from your ship and chain between enemies.'},
  cole:      {name:'NUKE STRIKE',    desc:'Three lock-on nuclear warheads level everything.'},
  lizzie:    {name:'ATOM BOMB',      desc:'Missiles become armed A-bombs. Each one levels the screen.'},
  falva:     {name:'ROLLER BALL',    desc:'Hold FIRE 5s to charge, release a pinball of death.'},
};
/* COLE IS A DEVELOPER PASSWORD, NOT A SAVE (drop 0801k). Mike: "He can only be unlocked via a
   password - Cole4u. never save his unlocked status to gamedata or anything. this is a pure
   password developer feature."

   So the flag is SESSION-ONLY. It was being read from and written to localStorage, which meant
   typing the code once unlocked him permanently on that machine — he has effectively been
   unlocked this whole time. No read on boot, no write on unlock: every session starts locked and
   the code has to be typed again. */
let coleUnlocked=false;
function isPilotLocked(P){ return !!(P && P.locked && P.key==='cole' && !coleUnlocked); }
let pilotIndex=0, pilotFlash=0, pilotPending=null, pilotRot=0, pilotFrom=0, pilotSlide=0, pilotComm=null, pilotCommT=0;
let PILOTMOD={spd:0,fire:0,range:0,tint:'#e23a3a'};
let menuFlash=0, menuFlashIdx=-1, titlePending=null;
let diffFlash=0, diffPending=null;
`;

// [B_BOOTSEQ] replaces drawBoot(); also adds drawLoading()
const B_BOOTSEQ = String.raw`/* BOOT — press-start gate (unlocks audio) then ColeForge cinematic */
function drawBoot(dt){
  ctx.fillStyle='#000'; ctx.fillRect(0,0,VW,VH);
  // ---- gate: wait for a gesture so the chime + music are allowed to play ----
  if(!drawBoot._started){
    /* PRESS-START GATE shows the NEW plate too — the old starfield tile and the assembled
       ColeForge text are gone entirely, per Mike. Same CONTAIN fit so nothing is cropped. */
    if(XART.rdy('cf_boot')){
      const bi=XART.get('cf_boot');
      const bs=Math.min(VW/bi.naturalWidth, VH/bi.naturalHeight);
      ctx.save(); ctx.globalAlpha=0.85;
      ctx.drawImage(bi, (VW-bi.naturalWidth*bs)/2, (VH-bi.naturalHeight*bs)/2,
                        bi.naturalWidth*bs, bi.naturalHeight*bs);
      ctx.restore();
    }
    ctx.textAlign='center';
    if(Math.floor(stateT*1.6)%2){ ctx.fillStyle='#ffe082'; ctx.font='bold 17px "BOFmil", monospace'; ctx.fillText('PRESS START', VW/2, VH*0.66); }
    ctx.fillStyle='#9aa0aa'; ctx.font='9px "BOFmil", monospace'; ctx.fillText('click or press any key', VW/2, VH*0.71);
    if(stateT>0.25 && (Input.mouse.down || anyTap())){
      drawBoot._started=true; drawBoot._ct=0; drawBoot._chimed=false;
      Audio.init(); Audio.resume(); if(BootChime) BootChime.unlock();
    }
    return;
  }
  drawBoot._ct=(drawBoot._ct||0)+dt;
  const t=drawBoot._ct;
  const FADEIN=0.7, RISE0=0.8, HOLD0=1.9, HOLDEND=4.0, EXITEND=4.9, STARFADE=5.5, DONE=5.9;
  /* COLEFORGE BOOT — CONTAIN, NOT COVER (drop 0724bw).
     COVER fills the viewport by CROPPING, and a 16:9 plate in a 480x512 window loses most of its
     width that way — the logo and the whole hangar were being cut off. CONTAIN fits the entire
     image inside the frame and letterboxes the remainder, so nothing is lost and nothing is
     stretched. Aspect is preserved either way; the difference is what gets sacrificed. */
  if(XART.rdy('cf_boot')){
    const im=XART.get('cf_boot');
    const sc=Math.min(VW/im.naturalWidth, VH/im.naturalHeight);
    const w=im.naturalWidth*sc, h=im.naturalHeight*sc;
    const a2=clamp(t/FADEIN,0,1) * (t>HOLDEND ? clamp((DONE-t)/(DONE-HOLDEND),0,1) : 1);
    ctx.save();
    ctx.globalAlpha=a2;
    ctx.drawImage(im, (VW-w)/2, (VH-h)/2, w, h);
    ctx.globalAlpha=a2*0.14; ctx.fillStyle='#8ba0d8';
    ctx.fillRect(0, (t*180)%VH, VW, 2);          // slow arcade scanline sweep
    ctx.restore();
    ctx.globalAlpha=1;
    if(!drawBoot._chimed && t>0.15){ drawBoot._chimed=true; if(BootChime) BootChime.play(); }
    if(t>DONE){ setState(GS.TITLE); menuIndex=0; Audio.startMusic('title'); }
    return;
  }
  // star tile parallax — scroll DOWN, fade in then out
  const starA = clamp(t/FADEIN,0,1) * (t>STARFADE ? clamp((DONE-t)/(DONE-STARFADE),0,1) : 1);
  /* Star-tile parallax REMOVED with the old boot sequence (drop 0724bw). Its trailing
     restore()/else survived my first cut and left a dangling block — the whole if/else is
     gone now, replaced by the plain backdrop the else branch used to draw. */
  ctx.fillStyle='#05030f'; ctx.fillRect(0,0,VW,VH);
  // logo rise / hold / exit — NEW SHUMP logo (ASSETS.menuLogo)
  const _mlogo=(ASSETS.rdy&&ASSETS.rdy(ASSETS.menuLogo))?ASSETS.menuLogo:(XART.rdy('logo')?XART.get('logo'):null);
  if(t>=RISE0 && _mlogo){
    const im=_mlogo; const w=Math.min(VW-26, 430); const h=w*(im.naturalHeight/im.naturalWidth);
    let cy, a;
    if(t<HOLD0){ const p=clamp((t-RISE0)/(HOLD0-RISE0),0,1), e=1-Math.pow(1-p,3); cy=lerp(VH+h*0.6, VH*0.46, e); a=p; }
    else if(t<HOLDEND){ cy=VH*0.46; a=1; }
    else { const p=clamp((t-HOLDEND)/(EXITEND-HOLDEND),0,1), e=p*p; cy=lerp(VH*0.46, -h*0.7, e); a=1-p; }
    ctx.save(); ctx.globalAlpha=clamp(a,0,1); ctx.shadowColor='rgba(255,170,40,0.55)'; ctx.shadowBlur=26;
    ctx.drawImage(im, Math.round(VW/2-w/2), Math.round(cy-h/2), Math.round(w), Math.round(h)); ctx.restore();
  }
  if(!drawBoot._chimed && t>=RISE0+0.04){ drawBoot._chimed=true; if(BootChime) BootChime.play(0.95); else Audio.SFX.boot(); }
  if(t>1.0 && (Input.tap('enter')||Input.mouse.down||keybind.fire.some(k=>Input.tap(k)))){ drawBoot._ct=DONE; }
  if(t>=DONE){ drawBoot._chimed=false; drawBoot._started=false; setState('loading'); }
}
/* LOADING — new boot image + loading bar to 100% */
function drawLoading(dt){
  ctx.fillStyle='#000'; ctx.fillRect(0,0,VW,VH);
  const t=stateT, FADE=0.5, LOAD=3.0, HOLD=0.55, DONE=FADE+LOAD+HOLD;
  const a=clamp(t/FADE,0,1);
  XART.cover('newbootimage', a);
  const pct=clamp((t-FADE)/LOAD,0,1);
  const bw=VW-60, bh=18, bx=30, by=VH-44;
  ctx.save(); ctx.globalAlpha=a;
  ctx.fillStyle='rgba(6,8,14,0.85)'; roundRectFill(bx-5,by-5,bw+10,bh+10,6);
  ctx.fillStyle='#0a0d14'; ctx.fillRect(bx,by,bw,bh);
  const g=ctx.createLinearGradient(bx,0,bx+bw,0); g.addColorStop(0,'#ffe06a'); g.addColorStop(1,'#ff5a1a');
  ctx.fillStyle=g; ctx.fillRect(bx,by,bw*pct,bh);
  ctx.fillStyle='rgba(0,0,0,0.3)'; for(let x=bx; x<bx+bw; x+=12) ctx.fillRect(x,by,2,bh);
  ctx.strokeStyle='#8a919c'; ctx.lineWidth=2; ctx.strokeRect(bx,by,bw,bh);
  ctx.fillStyle='#ffe9b0'; ctx.font='bold 11px "BOFmil", monospace'; ctx.textAlign='left'; ctx.fillText('LOADING',bx,by-7);
  ctx.textAlign='right'; ctx.fillText(Math.round(pct*100)+'%',bx+bw,by-7);
  ctx.restore();
  const step=Math.floor(pct*12); if(drawLoading._s!==step && pct<1 && pct>0){ drawLoading._s=step; Audio.SFX.blip(); }
  if(t>=DONE){ drawLoading._s=-1; goTitle(); }
}`;

// [B_TITLE] replaces from "const TITLE_ITEMS=" through the end of chooseTitle()
const B_TITLE = String.raw`/* RESTORED BY THE BUILD (drop 0724dj).
   drawStaticPlayer lives at gamecode.js:14072, INSIDE the span this block replaces
   (TITLE_ITEMS .. tryExit), so assemble.py deletes it and nothing re-defined it. drawShipSprite
   still calls it, so the game threw `drawStaticPlayer is not defined` EVERY FRAME once it reached
   the LAUNCH state — and the loop's try/catch swallowed it, so the screen simply froze with no
   error shown. That is why Mike could get through the menus and no further.
   Verified in the source: the definition is present there and ABSENT from the built file. */
function drawStaticPlayer(){
  px(-3,-16,6,30,'#d7dbe2'); ctx.fillStyle='#c81f24';
  ctx.beginPath(); ctx.moveTo(-3,-4);ctx.lineTo(-16,10);ctx.lineTo(-3,8);ctx.fill();
  ctx.beginPath(); ctx.moveTo(3,-4);ctx.lineTo(16,10);ctx.lineTo(3,8);ctx.fill();
  ctx.fillStyle='#e23a3a'; ctx.beginPath();ctx.moveTo(0,-22);ctx.lineTo(-4,-10);ctx.lineTo(4,-10);ctx.fill();
  px(-2,-12,4,7,'#1f4e8a'); px(-3,12,6,8,'#3aa0ff');
}
const TITLE_ITEMS=['NEW GAME','PASSWORD','OPTIONS','CREDITS','EXIT GAME'];
const MENU_KEYS=['btn_newgame','btn_password','btn_options','btn_credits','btn_exit'];
/* SPACING (drop 0801bu). Five title buttons: gap 58 -> 66 gives each one clear
   air without pushing the last past the copyright line. */
const TMENU_Y0=172, TMENU_GAP=66, TMENU_W=330;
let _menuScrollX=0;
function drawTitle(dt){
  if(ASSETS.rdy(ASSETS.starplanets)){
    // SCROLLING PLANETS backdrop — left, medium speed, tiled
    const im=ASSETS.starplanets, dw=Math.round(im.naturalWidth*(VH/im.naturalHeight));
    _menuScrollX=(_menuScrollX + dt*36) % dw;
    for(let x=-_menuScrollX; x<VW; x+=dw){ ctx.drawImage(im,0,0,im.naturalWidth,im.naturalHeight, Math.round(x),0, dw,VH); }
    for(const s of starField){ s.x=((s.x - s.z*0.6*dt*60)%VW+VW)%VW; ctx.fillStyle=s.z>1?'#cfe2ff':'#4455aa'; ctx.fillRect(s.x|0,s.y|0,2,2); }
    const g=ctx.createLinearGradient(0,0,0,VH); g.addColorStop(0,'rgba(6,5,14,0.45)'); g.addColorStop(0.34,'rgba(6,5,14,0.10)'); g.addColorStop(1,'rgba(6,5,14,0.55)');
    ctx.fillStyle=g; ctx.fillRect(0,0,VW,VH);
  } else if(XART.rdy('bootimage')){ XART.cover('bootimage');
    const g=ctx.createLinearGradient(0,0,0,VH); g.addColorStop(0,'rgba(6,5,14,0.6)'); g.addColorStop(0.32,'rgba(6,5,14,0.12)'); g.addColorStop(1,'rgba(6,5,14,0.55)');
    ctx.fillStyle=g; ctx.fillRect(0,0,VW,VH);
  } else { ctx.fillStyle='#080611'; ctx.fillRect(0,0,VW,VH);
    for(const s of starField){ s.y=(s.y+s.z*1.5*dt*60)%VH; ctx.fillStyle=s.z>1?'#cfe2ff':'#4455aa'; ctx.fillRect(s.x|0,s.y|0,2,2); } }
  // CANON TITLE LOGO (Mike 0719: logo-01 Primary Inferno)
  if(typeof XART!=='undefined' && XART.rdy('nbl_logo')){
    // fit the band ABOVE '- INSERT COIN -' (text center TMENU_Y0-50=118, top ~105): height-capped
    const lm=XART.get('nbl_logo'), lh=88, lw=lh*(lm.naturalWidth/lm.naturalHeight);
    ctx.drawImage(lm,(VW-lw)/2, 8, lw, lh);
  }
  drawMenuButtons(dt);
  // "- INSERT COIN -" : the STAGE-2 bitmap font, raised, flashing/glowing gold, above the NEW GAME button
  {
    const _t=performance.now()/1000;
    const _pulse=0.5+0.5*Math.sin(_t*3.2);
    const _cx=VW/2, _cy=TMENU_Y0 - 50;                    // raised another 10px (was TMENU_Y0-40)
    const _s2=(ASSETS.stageFont&&ASSETS.stageFont['2'])||(ASSETS.stageArt&&ASSETS.stageArt['2']);
    if(_s2 && typeof stageText==='function'){
      ctx.save();
      ctx.shadowColor='#ffcf3a'; ctx.shadowBlur=12+_pulse*22;   // glowing gold, pulsing
      // gold tint over the stage-2 font glyphs; brightness flashes with the pulse
      const _tint=_pulse>0.5?'#fff2c0':'#ffcf3a';
      stageText(_s2, '- INSERT COIN -', _cx, _cy, 26, _tint, 0.35+0.45*_pulse, 0.7+0.3*_pulse, 0.10);
      ctx.restore();
    } else {
      // font not loaded yet: browser-font gold fallback (still raised + flashing)
      ctx.save(); ctx.textAlign='center'; ctx.textBaseline='alphabetic';
      ctx.font='bold 22px "Arial Black",Impact,sans-serif';
      ctx.shadowColor='#ffcf3a'; ctx.shadowBlur=14+_pulse*20;
      ctx.lineWidth=4; ctx.strokeStyle='rgba(40,20,0,0.9)'; ctx.strokeText('- INSERT COIN -',_cx,_cy);
      const _gy=_cy-18, _g=ctx.createLinearGradient(0,_gy,0,_cy+4);
      _g.addColorStop(0, _pulse>0.5?'#fff6c8':'#ffe082'); _g.addColorStop(0.5,'#ffd23a'); _g.addColorStop(1,'#c8901a');
      ctx.globalAlpha=0.6+0.4*_pulse; ctx.fillStyle=_g; ctx.fillText('- INSERT COIN -',_cx,_cy);
      ctx.restore();
    }
  }
  ctx.fillStyle='rgba(210,216,226,0.85)'; ctx.font='8px "BOFmil", monospace'; ctx.textAlign='center';
  ctx.fillText('COPYRIGHT 2026 COLEFORGE STUDIOS',VW/2,VH-6);
  handleTitleInput();
  /* HARD RESET, ALWAYS AVAILABLE (drop 0724dm).
     Mike's binds were broken AND SAVED, and no rebuild could clear them because the fault lived in
     localStorage. The validator now heals the known shapes — but I have guessed wrong about this
     bug eight times, so there is now an escape hatch that does not depend on me having guessed
     right: F1, or clicking the label, wipes every stored key and reloads. */
  if(Input.down('f1') || Input.down('F1')){
    try{ localStorage.removeItem('bof_keys'); localStorage.removeItem('bof_opts'); localStorage.clear(); }catch(e){}
    try{ location.reload(); }catch(e){}
  }
  {
    const _rl='F1 = RESET CONTROLS';
    ctx.save(); ctx.textAlign='center'; ctx.font='10px "BOFmil", monospace';
    ctx.fillStyle='#7f8aa0'; ctx.fillText(_rl, VW/2, VH-6);
    const m=Input.mouse;
    if(m && m.down && m.y>VH-18 && Math.abs(m.x-VW/2)<90 && !drawTitle._rdown){
      drawTitle._rdown=true;
      try{ localStorage.clear(); }catch(e){}
      try{ location.reload(); }catch(e){}
    }
    if(m && !m.down) drawTitle._rdown=false;
    ctx.restore();
  }
  if(menuFlash>0) menuFlash-=dt;
  if(titlePending!=null && menuFlash<=0){ const m=titlePending; titlePending=null; menuFlashIdx=-1;
    if(m===0){ setState(GS.MODESEL); modeIndex=1; menuIndex=1; }   // NEW GAME -> mode select (boot-05)
    else if(m===1){ setState(GS.PASSWORD); pwInput=''; }
    else if(m===2){ setState(GS.OPTIONS); menuIndex=0; }
    else if(m===3){ setState('credits'); }
    else { tryExit(); } }
}
function drawMenuButton(cx,cy,w,h,label,sel,icon){
  const x=cx-w/2,y=cy-h/2;
  ctx.fillStyle= sel?'#3a3032':'#26282c'; octFill(x,y,w,h,8, sel?'#3a3032':'#26282c');
  ctx.strokeStyle= sel?'#ff3a3a':'#5a5d63'; ctx.lineWidth=2;
  ctx.beginPath();
  const c=8; ctx.moveTo(x+c,y);ctx.lineTo(x+w-c,y);ctx.lineTo(x+w,y+c);ctx.lineTo(x+w,y+h-c);
  ctx.lineTo(x+w-c,y+h);ctx.lineTo(x+c,y+h);ctx.lineTo(x,y+h-c);ctx.lineTo(x,y+c);ctx.closePath(); ctx.stroke();
  octFill(x+6,y+5,w-12,h-10,5,'#12151a');
  if(sel){ ctx.globalAlpha=0.25+0.15*Math.sin(performance.now()/120); octFill(x+6,y+5,w-12,h-10,5,'#5a1010'); ctx.globalAlpha=1;}
  octFill(x+8,y+6,h-12,h-12,4, sel?'#5a1414':'#1a1d22');
  drawMenuIcon(icon, x+8+(h-12)/2, cy);
  ctx.fillStyle=sel?'#ffffff':'#cfd6e0'; ctx.font='bold 16px "BOFmil", monospace'; ctx.textAlign='left';
  ctx.fillText(label, x+h+6, cy+6);
}
function drawMenuIcon(icon,cx,cy){
  ctx.fillStyle='#dfe3ea';
  if(icon==='ship'){ ctx.save();ctx.translate(cx,cy);ctx.scale(0.6,0.6);if(typeof drawStaticPlayer==='function')drawStaticPlayer();ctx.restore(); }
  else if(icon==='lock'){ px(cx-6,cy-2,12,10,'#dfe3ea'); ctx.strokeStyle='#dfe3ea';ctx.lineWidth=2;ctx.beginPath();ctx.arc(cx,cy-3,4,Math.PI,0);ctx.stroke(); px(cx-1,cy+1,2,4,'#26282c'); }
  else if(icon==='gear'){ ctx.fillStyle='#dfe3ea'; for(let a=0;a<8;a++){const an=a*TAU/8;px(cx+Math.cos(an)*7-1.5,cy+Math.sin(an)*7-1.5,3,3,'#dfe3ea');} circle(cx,cy,5); ctx.fillStyle='#26282c';circle(cx,cy,2); }
  else if(icon==='door'){ px(cx-6,cy-7,9,15,'#dfe3ea'); px(cx-4,cy-5,5,11,'#26282c'); px(cx+2,cy-1,2,2,'#dfe3ea'); ctx.strokeStyle='#dfe3ea';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(cx+3,cy+1);ctx.lineTo(cx+8,cy+1);ctx.stroke(); }
  else if(icon==='star'){ ctx.fillStyle='#dfe3ea'; ctx.beginPath(); for(let k=0;k<5;k++){ const a=-Math.PI/2+k*TAU/5, a2=a+TAU/10; ctx.lineTo(cx+Math.cos(a)*7,cy+Math.sin(a)*7); ctx.lineTo(cx+Math.cos(a2)*3,cy+Math.sin(a2)*3); } ctx.closePath(); ctx.fill(); }
}
function drawMenuButtons(dt){
  if(!XART.rdy('btn_newgame')){
    for(let i=0;i<TITLE_ITEMS.length;i++) drawMenuButton(VW/2, TMENU_Y0+i*TMENU_GAP, 250, 40, TITLE_ITEMS[i], i===menuIndex, ['ship','lock','gear','star','door'][i]);
    return;
  }
  for(let i=0;i<5;i++){
    const im=XART.get(MENU_KEYS[i]); if(!XART.rdy(MENU_KEYS[i])) continue;
    const sel=(i===menuIndex), w=sel?TMENU_W*1.04:TMENU_W, h=w*(im.naturalHeight/im.naturalWidth);
    const cx=VW/2, cy=TMENU_Y0+i*TMENU_GAP;
    ctx.save(); if(sel){ ctx.shadowColor='#ffd24a'; ctx.shadowBlur=18; } else ctx.globalAlpha=0.9;
    ctx.drawImage(im, cx-w/2, cy-h/2, w, h); ctx.restore();
    if(menuFlashIdx===i && menuFlash>0) flashImg(im, cx-w/2, cy-h/2, w, h, clamp(menuFlash/0.2,0,1)*0.92);
    if(sel){ const p=Math.sin(performance.now()/130)*2;
      // Mike's selector: north triangle (rotated 90 right at slice time) with the rising white sweep
      if(!(typeof drawSelArrow==='function' && drawSelArrow(cx-w/2-18-p, cy, 22, false) && drawSelArrow(cx+w/2+18+p, cy, 22, true))){
        ctx.fillStyle='#ffe682'; ctx.font='bold 16px "BOFmil", monospace'; ctx.textAlign='center';
        ctx.fillText('\u25B6', cx-w/2-12-p, cy+5); ctx.fillText('\u25C0', cx+w/2+12+p, cy+5); } }
  }
}
function handleTitleInput(){
  /* CURSOR MOVEMENT FIRST, AND IT MAY NOT THROW (drop 0724dn).
     Mike's screen animated perfectly while input did nothing — and everything visible in drawTitle
     is drawn BEFORE this call, which is the LAST statement in the function. So this was throwing
     every frame, the loop's try/catch swallowed it, and the result was a live-looking title with
     dead controls. Exactly the symptom, and invisible by construction.
     The fix is order plus isolation: read the keys and move the cursor in a block that cannot
     throw, THEN do everything else inside a guard that reports rather than dies. */
  try{
    /* ONE HANDLER, ONE LATCH (drop 0801r). There were THREE cursor movers running against two
       shared latches, and I added the third:

         block A  raw keys, latched on _pd/_pu
         block A  Input.menuDown()  <- a CONSUMING tap, added in 0801p
         block B  raw keys again, on the SAME _pd/_pu
         block B  Input.menuDown() again

       A latched mover and a tap mover on the same press both fire, so one keypress moved the
       cursor TWICE — 0 -> 2 -> 4 -> 1 -> 3 through a five-item menu. That reads as a cursor that
       will not step, which is exactly what it looked like.

       Now: this function computes the intent ONCE, moves ONCE, and _handleTitleInputRest no
       longer touches the cursor at all. It is also idempotent per frame, so the loop hoist and the
       draw can both call it safely. */
    try{ if(window.__menudiag) window.__menudiag.calls++; }catch(_){}
    const _fr = (typeof frameCount!=='undefined') ? frameCount : (handleTitleInput._f=(handleTitleInput._f||0)+1);
    if(handleTitleInput._lastFrame === _fr) return;      // already serviced this frame
    handleTitleInput._lastFrame = _fr;
    let _d = Input.down('arrowdown') || Input.down('s');
    let _u = Input.down('arrowup')   || Input.down('w');
    let _g = Input.down('enter')     || Input.down(' ') || Input.down('z');
    try{ if(typeof Input.menuDown==='function' && Input.menuDown()) _d=true; }catch(_){}
    try{ if(typeof Input.menuUp  ==='function' && Input.menuUp())   _u=true; }catch(_){}
    if(_d && !handleTitleInput._pd){ menuIndex=(menuIndex+1)%5; try{ if(window.__menudiag) window.__menudiag.lastMove='down->'+menuIndex; }catch(_){} try{ Audio.SFX.blip&&Audio.SFX.blip(); }catch(_){} }
    if(_u && !handleTitleInput._pu){ menuIndex=(menuIndex+4)%5; try{ if(window.__menudiag) window.__menudiag.lastMove='up->'+menuIndex; }catch(_){} try{ Audio.SFX.blip&&Audio.SFX.blip(); }catch(_){} }
    handleTitleInput._pd=_d; handleTitleInput._pu=_u;
    if(_g && !handleTitleInput._pg){ handleTitleInput._pg=true; try{ chooseTitle(); }catch(_){} }
    if(!_g) handleTitleInput._pg=false;
  }catch(_e0){ /* even this is guarded: nothing may stop the cursor moving */ }
  try{ _handleTitleInputRest(); }
  catch(e){
    /* REPORT IT. A swallowed exception here is what cost eight rounds of guessing. */
    handleTitleInput._err = String((e&&e.message)||e);
    try{
      ctx.save(); ctx.textAlign='left'; ctx.font='9px "BOFmil", monospace';
      ctx.fillStyle='rgba(40,0,0,0.85)'; ctx.fillRect(2,VH-58,VW-4,16);
      ctx.fillStyle='#ff8a7a';
      ctx.fillText('title input error: '+handleTitleInput._err.slice(0,58), 6, VH-46);
      ctx.restore();
    }catch(_){}
  }
}
function _handleTitleInputRest(){
  if(titlePending!=null) return;
  /* DIRECT FALLBACK (drop 0724dm).
     Mike's readout showed 40 keydowns ARRIVING and menuIndex stuck at 0, so the keys reach the page
     but the tap never reaches here. Rather than keep hunting the shared tap pool, this reads the
     raw held-key state and does its own edge detection, local to this screen. It cannot be consumed
     by anything else, it does not depend on keybind being intact, and it runs alongside the normal
     path — whichever fires first moves the cursor. */
  /* THE CURSOR IS MOVED IN ONE PLACE ONLY (drop 0801r). This block used to duplicate the keyboard
     read AND call the consuming menuDown()/menuUp() taps, against the same _pd/_pu latches the
     caller uses. Two movers on one press = two steps. Cursor movement now lives entirely in
     handleTitleInput; this handles mouse only. */
  // hover only steals selection when the mouse actually MOVED this frame (keyboard/pad nav isn't overridden)
  const moved=Input.consumeMouseMoved();
  const my=Input.mouse.y;
  for(let i=0;i<5;i++){ const cy=TMENU_Y0+i*TMENU_GAP;
    /* The x test required the pointer within 165px of centre. Mike's readout put his pointer at
       x=471 on a 480-wide field, so every click missed on x alone. The rows read as full-width
       bands on screen, so the hit box now matches what the player sees. */
    if(Math.abs(my-cy)<TMENU_GAP*0.46){
      if(moved && Input.mouse.inside) menuIndex=i;
      if(Input.mouse.down && !handleTitleInput._md){ menuIndex=i; chooseTitle(); } } }
  handleTitleInput._md=Input.mouse.down;
  if(Input.menuConfirm()) chooseTitle();
}
function chooseTitle(){ if(titlePending!=null) return; Audio.SFX.select(); menuFlashIdx=menuIndex; menuFlash=0.22; titlePending=menuIndex; }`;

// [B_DIFF] replaces from "const DIFF_KEYS=" through pickDiff()
const B_DIFF = String.raw`const DIFF_KEYS=['easy','normal','hard','furious'];
const DIFF_IMG=['diff_easy','diff_normal','diff_hard','diff_furious'];
const DIFF_DESC=['5 LIVES \u00B7 SLOWER ENEMIES \u00B7 MORE DROPS','3 LIVES \u00B7 STANDARD FURY','2 LIVES \u00B7 FASTER \u00B7 TOUGHER \u00B7 FEWER DROPS','1 LIFE \u00B7 RELENTLESS \u00B7 NO MERCY'];
function scrollSpaceBG(dt){
  if(ASSETS.rdy(ASSETS.starplanets)){
    const im=ASSETS.starplanets, dw=Math.round(im.naturalWidth*(VH/im.naturalHeight));
    _menuScrollX=(_menuScrollX + dt*36) % dw;
    for(let x=-_menuScrollX; x<VW; x+=dw){ ctx.drawImage(im,0,0,im.naturalWidth,im.naturalHeight, Math.round(x),0, dw,VH); }
    for(const s of starField){ s.x=((s.x - s.z*0.6*dt*60)%VW+VW)%VW; ctx.fillStyle=s.z>1?'#cfe2ff':'#4455aa'; ctx.fillRect(s.x|0,s.y|0,2,2); }
    const g=ctx.createLinearGradient(0,0,0,VH); g.addColorStop(0,'rgba(6,5,14,0.55)'); g.addColorStop(0.34,'rgba(6,5,14,0.18)'); g.addColorStop(1,'rgba(6,5,14,0.62)');
    ctx.fillStyle=g; ctx.fillRect(0,0,VW,VH);
  } else { drawBootBackdrop(dt,0.58); }
}
function drawDiff(dt){
  if(typeof drawCanonBackdrop==='function' && drawCanonBackdrop('nbt_2',0.55)){} else scrollSpaceBG(dt);   // boot-02 canon backdrop
  if(typeof msgText==='function'){ msgText('SELECT DIFFICULTY',VW/2,52,20,'#f2f5ff',0,1,0.08); }
  else { ctx.textAlign='center'; ctx.fillStyle='#f2f5ff'; ctx.font='bold 18px "BOFmil", monospace'; ctx.fillText('SELECT DIFFICULTY',VW/2,56); }
  /* SPACING (drop 0801bu). Was 112/68 - four rows ending at y=316 with 120px of
     dead space beneath before the rules text at VH-72. Re-centred and opened up
     so the block reads as a deliberate column. */
  const startY=124, gap=84, w0=210, N=DIFF_KEYS.length;
  const have = XART.rdy('diff_easy');
  for(let i=0;i<N;i++){
    const cy=startY+i*gap, sel=(i===menuIndex);
    if(have){
      const im=XART.get(DIFF_IMG[i]); const w=sel?w0*1.05:w0, h=w*(im.naturalHeight/im.naturalWidth);
      ctx.save(); if(sel){ctx.shadowColor='#ffdf73';ctx.shadowBlur=15;}else ctx.globalAlpha=0.84;
      ctx.drawImage(im,VW/2-w/2,cy-h/2,w,h); ctx.restore();
      /* CURSOR (drop 0801ba). This screen was the only menu with no selector at
         all - just a glow. drawSelArrow is the shared rising-white selector the
         title/mode/pause menus already use, so the difficulty screen now reads
         the same as every other menu instead of being the odd one out. */
      if(sel && typeof drawSelArrow==='function'){
        // GREEN on this screen, per Mike — the duplicated nsel_arrow_g art.
        drawSelArrow(VW/2-w/2-18, cy, 22, false, 'g');
        drawSelArrow(VW/2+w/2+18, cy, 22, true, 'g');
      }
      if(diffPending===i&&diffFlash>0) flashImg(im,VW/2-w/2,cy-h/2,w,h,clamp(diffFlash/0.2,0,1)*0.92);
      // (no small text under the buttons)
    } else {
      drawMenuButton(VW/2,cy,240,40,DIFFS[DIFF_KEYS[i]].name,sel,null);
      if(sel && typeof drawSelArrow==='function'){
        drawSelArrow(VW/2-138, cy, 22, false, 'g');
        drawSelArrow(VW/2+138, cy, 22, true, 'g');
      }
    }
  }
  // RULES of the highlighted difficulty — LARGE, stage-1 font, at the bottom, readable
  { const desc=DIFF_DESC[clamp(menuIndex,0,N-1)];
    const parts=desc.split(' \u00B7 ');
    const uf=(ASSETS.stageFont&&ASSETS.stageFont['1'])||(ASSETS.stageArt&&ASSETS.stageArt['1']);
    let yy=VH-72;
    for(const line of parts){ if(uf && typeof stageText==='function'){ stageText(uf,line,VW/2,yy,15,null,null,1,0.08); } else { ctx.textAlign='center'; ctx.fillStyle='#eaf2ff'; ctx.font='13px "BOFmil", monospace'; ctx.fillText(line,VW/2,yy); } yy+=20; }
  }
  if(diffFlash>0) diffFlash-=dt;
  if(diffPending!=null && diffFlash<=0){ const m=diffPending; diffPending=null; menuIndex=m; pickDiff(); return; }
  if(diffPending!=null) return;
  if(Input.menuDown()){menuIndex=(menuIndex+1)%N;Audio.SFX.blip();}
  if(Input.menuUp()){menuIndex=(menuIndex+N-1)%N;Audio.SFX.blip();}
  const moved=Input.consumeMouseMoved(); const my=Input.mouse.y;
  for(let i=0;i<N;i++){ const cy=startY+i*gap; if(Math.abs(my-cy)<gap*0.42&&Math.abs(Input.mouse.x-VW/2)<w0*0.5){ if(moved && Input.mouse.inside)menuIndex=i;
    if(Input.mouse.down && !drawDiff._md){ menuIndex=i; confirmDiff(); } } }
  drawDiff._md=Input.mouse.down;
  if(Input.menuConfirm()) confirmDiff();
  if(Input.menuBack()){ setState(GS.TITLE); menuIndex=0; }
  if(backButton()){ setState(GS.TITLE); menuIndex=0; Audio.SFX.select(); }
}
function confirmDiff(){ if(diffPending!=null)return; Audio.SFX.select(); diffPending=menuIndex; diffFlash=0.2; }
function pickDiff(){ diffKey=DIFF_KEYS[menuIndex]; Audio.SFX.select();
  /* MUSIC CROSSES OVER HERE (drop 0724cg), not when the map forms. Choosing a difficulty is the
     moment the player commits, so the menu track fades and the campaign track comes up UNDER the
     boot sequence — by the time the map appears it is already playing rather than starting
     abruptly once the flags land. The map's own start sites now only fire if nothing is playing,
     which keeps password entry and mid-run returns working. */
  if(run.mode==='campaign' && Audio.startMusic){
    if(Audio.fadeOutMusic) Audio.fadeOutMusic(0.5); else if(Audio.stopMusic) Audio.stopMusic();
    Audio.startMusic('neonvelocity');
  }
  setState('pilot'); pilotIndex=Math.min(pilotIndex,PILOTS.length-1);
  // reset all transient pilot-select state so a stale comm/slide from a prior visit never stacks on the card
  pilotComm=null; pilotCommT=0; pilotPending=null; pilotSlide=0; pilotRot=0; pilotFlash=0; }
/* PILOT SELECT — "Choose your Pilot!" left cards in a row */
function drawPilotBG(tint){
  const c=hx(tint);
  ctx.fillStyle='#08080e'; ctx.fillRect(0,0,VW,VH);
  const g=ctx.createLinearGradient(0,0,0,VH);
  g.addColorStop(0,rgba(c,0.10)); g.addColorStop(0.42,rgba(c,0.42)); g.addColorStop(0.60,rgba(c,0.34)); g.addColorStop(1,rgba(c,0.07));
  ctx.fillStyle=g; ctx.fillRect(0,0,VW,VH);
  const rg=ctx.createRadialGradient(VW/2,VH*0.45,24,VW/2,VH*0.45,VW*0.85);
  rg.addColorStop(0,rgba(c,0.26)); rg.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=rg; ctx.fillRect(0,0,VW,VH);
}
function pilotFont(idx){ return (ASSETS.stageArt && ASSETS.stageArt[String(idx)]) || null; }
function startPilotRot(dir){ if(pilotRot>0)return; pilotFrom=pilotIndex; pilotIndex=(pilotIndex+dir+PILOTS.length)%PILOTS.length; pilotRot=1; Audio.SFX.blip(); }
function roundRect(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
function drawCommWindow(o){
  const t=o.tint||'#8ad0ff', c=hx(t), ap=clamp(o.appear==null?1:o.appear,0,1);
  ctx.save();
  ctx.globalAlpha=0.66*ap; ctx.fillStyle='#030407'; ctx.fillRect(0,0,VW,VH); ctx.globalAlpha=1;
  const _fk=(o.frameKey&&XART.rdy(o.frameKey))?o.frameKey:'dlg_window';
  const _dedicated=_fk!=='dlg_window' && XART.rdy(_fk);
  const pw=Math.min(VW-24,446);
  const ph=_dedicated ? Math.round(pw*(XART.get(_fk).naturalHeight/XART.get(_fk).naturalWidth)) : Math.round(pw*0.52);
  const px0=(VW-pw)/2, py0=VH*0.34;
  const ease=ap*ap*(3-2*ap); ctx.translate(0,(1-ease)*20); ctx.globalAlpha=ap;
  if(XART.rdy(_fk)){ ctx.drawImage(XART.get(_fk),px0,py0,pw,ph); }
  else { ctx.fillStyle='rgba(8,12,18,0.95)'; ctx.fillRect(px0,py0,pw,ph); ctx.strokeStyle=t; ctx.lineWidth=3; ctx.strokeRect(px0,py0,pw,ph); }
  /* NO BORDER OVER ART THAT HAS ONE (drop 0801bk). Mike: "no more bordering the
     dialogue boxes, they have their own boxes."

     This drew a full tinted frame — dark seat, coloured stroke, bevel hairline
     and four corner ticks — on top of EVERY pilot, including the ones whose
     dlg_<pilot> art already contains its own box. Two frames stacked. It now
     runs only when there is no dedicated frame art to sit on, which is the case
     the original comment was actually written for. */
  if(!_dedicated){
    const bx=px0+2, by=py0+2, bw=pw-4, bh=ph-4, r=10;
    ctx.save();
    // outer dark seat so the colored border reads on any background
    ctx.strokeStyle='rgba(0,0,0,0.85)'; ctx.lineWidth=6;
    ctx.beginPath(); roundRect(bx,by,bw,bh,r); ctx.stroke();
    // main colored border (pilot tint), with a soft glow
    ctx.shadowColor='rgba('+c[0]+','+c[1]+','+c[2]+',0.6)'; ctx.shadowBlur=8;
    ctx.strokeStyle='rgba('+c[0]+','+c[1]+','+c[2]+',0.95)'; ctx.lineWidth=3;
    ctx.beginPath(); roundRect(bx,by,bw,bh,r); ctx.stroke();
    // inner bright hairline for a beveled edge
    ctx.shadowBlur=0; ctx.strokeStyle='rgba(255,255,255,0.28)'; ctx.lineWidth=1;
    ctx.beginPath(); roundRect(bx+3,by+3,bw-6,bh-6,r-2); ctx.stroke();
    // corner accent ticks in the pilot color
    ctx.strokeStyle='rgba('+c[0]+','+c[1]+','+c[2]+',1)'; ctx.lineWidth=3; const tk=16;
    for(const [ax,ay,sx,sy] of [[bx,by,1,1],[bx+bw,by,-1,1],[bx,by+bh,1,-1],[bx+bw,by+bh,-1,-1]]){
      ctx.beginPath(); ctx.moveTo(ax+sx*tk,ay); ctx.lineTo(ax+sx*4,ay); ctx.lineTo(ax+sx*4,ay+sy*4); ctx.lineTo(ax,ay+sy*4); ctx.moveTo(ax,ay+sy*4); ctx.lineTo(ax,ay+sy*tk); ctx.stroke();
    }
    ctx.restore();
  }
  // interior panel (measured on the dedicated frame art; generic window uses its old insets)
  const inL=px0+pw*(_dedicated?0.075:0.055), inT=py0+ph*(_dedicated?0.16:0.10),
        inW=pw*(_dedicated?0.855:0.89),      inH=ph*(_dedicated?0.66:0.72);
  if(!_dedicated){ ctx.globalAlpha=ap*0.18; ctx.fillStyle=c; ctx.fillRect(inL,inT,inW,inH); ctx.globalAlpha=ap; }
  // portrait: framed inset box, COVER-fit (fills the whole box, no black gaps), head-anchored to the top
  const pbW=inW*0.36, pbH=inH;
  const port=(o.portraitKey&&XART.rdy(o.portraitKey))?XART.get(o.portraitKey):((o.cardKey&&XART.rdy(o.cardKey))?XART.get(o.cardKey):null);
  if(port){
    // recessed portrait plate so the face reads as being INSIDE a frame, not cut by the panel edge
    ctx.save();
    ctx.fillStyle='rgba(4,7,12,0.9)'; roundRectFill(inL,inT,pbW,pbH,4);
    const pad=Math.max(3, pbW*0.05);
    const bxW=pbW-pad*2, bxH=pbH-pad*2;
    // COVER-fit: scale so the portrait fully covers the padded box (crops overflow, never letterboxes)
    const s=Math.max(bxW/port.naturalWidth, bxH/port.naturalHeight);
    const dw=port.naturalWidth*s, dh=port.naturalHeight*s;
    const dx=inL+pad+(bxW-dw)/2;          // horizontally centered
    // vertical: anchor near the top but leave a little headroom so heads/chins aren't jammed to an edge.
    // clamp so we never expose a gap at top or bottom (dy between covering-top and covering-bottom).
    const dyTop=inT+pad, dyBot=inT+pbH-pad-dh;
    const dy=Math.min(dyTop, Math.max(dyBot, dyTop - dh*0.04));
    ctx.beginPath(); roundRect(inL+2,inT+2,pbW-4,pbH-4,3); ctx.clip();   // clip so overflow is hidden
    ctx.drawImage(port, dx, dy, dw, dh);
    ctx.restore();
    // colored frame border around the PORTRAIT in the pilot's color (layered: dark seat + tint + bevel + corner ticks)
    {
      const bx=inL+1, by=inT+1, bw=pbW-2, bh=pbH-2, rr=5;
      ctx.save();
      ctx.strokeStyle='rgba(0,0,0,0.85)'; ctx.lineWidth=4;
      ctx.beginPath(); roundRect(bx,by,bw,bh,rr); ctx.stroke();
      ctx.shadowColor='rgba('+c[0]+','+c[1]+','+c[2]+',0.65)'; ctx.shadowBlur=6;
      ctx.strokeStyle='rgba('+c[0]+','+c[1]+','+c[2]+',0.95)'; ctx.lineWidth=2.5;
      ctx.beginPath(); roundRect(bx,by,bw,bh,rr); ctx.stroke();
      ctx.shadowBlur=0; ctx.strokeStyle='rgba(255,255,255,0.30)'; ctx.lineWidth=1;
      ctx.beginPath(); roundRect(bx+2.5,by+2.5,bw-5,bh-5,rr-1); ctx.stroke();
      // corner accent ticks
      ctx.strokeStyle='rgba('+c[0]+','+c[1]+','+c[2]+',1)'; ctx.lineWidth=2.5; const tk=9;
      for(const [ax,ay,sx,sy] of [[bx,by,1,1],[bx+bw,by,-1,1],[bx,by+bh,1,-1],[bx+bw,by+bh,-1,-1]]){
        ctx.beginPath(); ctx.moveTo(ax+sx*tk,ay); ctx.lineTo(ax+sx*3,ay); ctx.lineTo(ax+sx*3,ay+sy*3); ctx.lineTo(ax,ay+sy*3); ctx.moveTo(ax,ay+sy*3); ctx.lineTo(ax,ay+sy*tk); ctx.stroke();
      }
      ctx.restore();
    }
  }
  const rx=inL+pbW+14, rw=inW-pbW-22;
  ctx.textAlign='left'; ctx.fillStyle=t; ctx.font='20px "BOFmil", monospace';
  ctx.shadowColor='rgba(0,0,0,0.8)'; ctx.shadowBlur=3;
  ctx.fillText((o.name||'').toUpperCase(), rx, inT+26);
  if(o.text){ ctx.fillStyle='#eaf2ff'; ctx.font='14px "BOFmil", monospace';
    // typewriter: only reveal up to charsShown characters when provided
    let shown=o.text;
    if(o.charsShown!=null){ shown=o.text.slice(0, Math.max(0, Math.floor(o.charsShown))); }
    const words=(shown||'').split(' '); let line='', yy=inT+54;
    for(const w of words){ const test=line?line+' '+w:w; if(ctx.measureText(test).width>rw && line){ ctx.fillText(line,rx,yy); line=w; yy+=19; } else line=test; }
    if(line) ctx.fillText(line,rx,yy); }
  ctx.restore();
  return {px0,py0,pw,ph,inL,inT,inW,inH,pbW};
}
function drawPilotComm(P,t){
  const appear=clamp(t/0.26,0,1);
  const _pp=(typeof pilotPortrait==='function')?pilotPortrait(P.key,'idle'):('face_'+P.key);
  const g=drawCommWindow({tint:P.tint, name:P.name, frameKey:'dlg_'+P.key, portraitKey:_pp, cardKey:'card_'+P.key, text:'GOOD LUCK, PILOT!', appear});
  ctx.save(); ctx.globalAlpha=appear; ctx.textAlign='center'; ctx.fillStyle=P.tint; ctx.font='28px "BOFmil", monospace';
  ctx.lineWidth=4; ctx.strokeStyle='rgba(0,0,0,0.6)'; ctx.strokeText(P.name.toUpperCase(),VW/2,g.py0-14); ctx.fillText(P.name.toUpperCase(),VW/2,g.py0-14);
  ctx.restore();
  // (emoji speech bubble removed per Mike)
}
function drawPilot(dt){
  const N=PILOTS.length;
  // fresh entry into the pilot screen: clear any stale comm/selection transient so nothing stacks
  if(stateT<0.05 && !drawPilot._entered){ drawPilot._entered=true; pilotComm=null; pilotCommT=0; pilotPending=null; pilotSlide=0; pilotRot=0; }
  if(stateT>0.2) drawPilot._entered=false;
  if(pilotRot>0 && pilotPending==null){ pilotRot=Math.max(0,pilotRot-dt/0.34); }
  const showIdx=(pilotRot>0.5)?pilotFrom:pilotIndex;
  const P=PILOTS[showIdx];
  /* PILOT CARD (drop 0801j). Mike: "Your going to have us select each pilot, where the card pops
     up, and the text all forms letter by 1 letter, stat bar by star like a Mega Man X menu
     screen." The card restarts whenever the selection changes, so scrolling the roster replays
     the reveal for whoever you land on. */
  if(typeof pcStart==='function'){
    if(drawPilot._pcFor!==P.key){ drawPilot._pcFor=P.key; pcStart(P.key); }
    if(typeof pcUpdate==='function') pcUpdate(dt);
    // any input skips the flourish rather than making the player wait it out
    /* ORDER MATTERS (drop 0801bk). Mike: "pressing enter should work."

       tap() CONSUMES the key. With the taps written first, JavaScript evaluated
       them left-to-right BEFORE `!pcard.done` was ever tested — so Enter was
       swallowed here on every single frame, finished reveal or not, and never
       reached Input.menuConfirm() further down. Enter could not select a pilot
       at all. Guard on the state first; only reach for the key when a skip is
       actually possible. */
    if(typeof Input!=='undefined' && pcard && !pcard.done && typeof pcSkip==='function'
       && (Input.tap('fire')||Input.tap('enter')||Input.tap(' '))){ pcSkip(); }
  }
  drawPilotBG(P.tint);
  /* the reveal (typed text + stat bars + special) is drawn AFTER the shell, over the same rect —
     see the pcDraw call further down, which now receives cardRect. */
  // title in the stage-2 atlas font (full glyph set incl. S), tinted vivid to the pilot colour
  const t2=pilotFont(2);
  if(typeof msgText==='function'){ msgText('CHOOSE YOUR PILOT!',VW/2,42,22,'#f2f5ff',0,1,0.06); }
  else { ctx.textAlign='center'; outlineText('CHOOSE YOUR PILOT!',VW/2,46,'#f2f5ff','#12151a',3); }
  // one card, centred, with a horizontal scale (rotation) transition between pilots
  const locked = isPilotLocked(P);
  /* THE OLD CARDS ARE GONE (drop 0801s). Mike: "you have to remove the old cars."

     card_<pilot> is the pre-CF_PilotCardSystem art with the name, callsign, bio and stat values
     BAKED IN. The new shell + runtime reveal draws all of that itself, so both were rendering the
     same information twice — the old one flat behind, the new one typing out on top.

     The old block is not simply deleted, because it owned three things the screen still needs:
     the horizontal-scale rotation between pilots, the slide-away on select, and the locked flash.
     Those stay; only the SOURCE changes, to the new shell (pcard_<pilot>) and the LOCKED shell.
     cardRect is still published for the hit-testing below. */
  const k = locked ? (XART.rdy('pcard_locked') ? 'pcard_locked' : 'card_cole_locked')
                   : (XART.rdy('pcard_'+P.key) ? 'pcard_'+P.key : 'card_'+P.key);
  let cardRect=null;
  if(XART.rdy(k)){
    const im=XART.get(k);
    let w=Math.min(VW-30,452), h=w*(im.naturalHeight/im.naturalWidth); const maxH=VH*0.62;
    if(h>maxH){ h=maxH; w=h*(im.naturalWidth/im.naturalHeight); }
    let sx=1;
    if(pilotRot>0){ sx=(pilotRot>0.5)?(pilotRot-0.5)/0.5:(0.5-pilotRot)/0.5; sx=Math.max(0.04,sx); }
    const slideX=(pilotPending!=null)? -_ease(clamp(pilotSlide,0,1))*(VW*1.4) : 0;   // slide left & away on select
    const cx=VW/2, cy=VH*0.455; cardRect=[cx-w/2,cy-h/2,w,h];
    ctx.save();
    if(pilotRot<0.04 && pilotPending==null){ ctx.shadowColor=P.tint; ctx.shadowBlur=30; }
    ctx.translate(cx+slideX,cy); ctx.scale(sx,1);
    ctx.drawImage(im,-w/2,-h/2,w,h);
    if(locked && pilotFlash>0){ ctx.globalAlpha=Math.min(0.5,pilotFlash)*0.5/0.5; ctx.fillStyle='#ffffff'; ctx.globalAlpha=Math.min(1,pilotFlash)*0.5; ctx.fillRect(-w/2,-h/2,w,h); ctx.globalAlpha=1; }
    ctx.restore();
    /* the runtime reveal, over the shell we just drew and in its exact rect. Suppressed during
       the rotation and the slide-away so it never smears across the transition. */
    if(!locked && pilotRot<0.04 && pilotPending==null &&
       typeof pcDraw==='function' && pcard) { try{ pcDraw(cardRect); }catch(_){} }
  }
  if(locked){ pilotFlash=Math.max(0,pilotFlash-dt*2.2); } else { pilotFlash=0; }
  // pilot name in that pilot's own stage font, native colours (hidden while sliding away)
  if(pilotRot<0.5 && pilotPending==null && !locked){
    /* The big stage-font name under the card stays — it is the screen's title, not card data.
       The SPECIAL line below it does NOT: the new card carries its own SPECIAL ABILITY section
       with an icon, so printing it again underneath was the same fact twice. */
    const pf=pilotFont(P.font)||t2;
    if(pf){ stageTextMixed(pf,t2,P.name,VW/2,VH*0.80,28,P.tint,1,0.07); }
    else { ctx.textAlign='center'; ctx.fillStyle=P.tint; ctx.font='bold 22px "BOFmil", monospace'; ctx.fillText(P.name,VW/2,VH*0.81); }
    /* the SPECIAL line and its description used to print here, under the card. The new card has
       its own SPECIAL ABILITY section with a real icon, so this was the same fact twice on one
       screen. Removed — the card owns it now. */
  }
  // nav arrows
  ctx.textAlign='center'; ctx.font='bold 30px "BOFmil", monospace';
  ctx.fillStyle=rgba(hx(P.tint),0.85); ctx.fillText('\u25C0',20,VH*0.46+10); ctx.fillText('\u25B6',VW-20,VH*0.46+10);
  { const _backKey=(typeof keyName==='function' && keybind && keybind.back)?keyName(keybind.back[0]):'BKSP';
    const _hint='\u25C0 \u25B6 SCROLL   \u2022   ENTER = LAUNCH   \u2022   '+_backKey+' = BACK';
    if(typeof msgText==='function'){ msgText(_hint, VW/2, VH-14, 10, '#cfd6e0', 0.7, 0.9, 0.12); }
    else { ctx.textAlign='center'; ctx.fillStyle='#cfd6e0'; ctx.font='8px "BOFmil", monospace'; ctx.fillText(_hint,VW/2,VH-12); } }
  // (pip/dot indicator removed per Mike — the player discovers the roster by scrolling)
  // hover check (locked card) -> glow pulse + flashing unlock prompt
  const hoverLocked = locked && cardRect && Input.mouse.x>cardRect[0] && Input.mouse.x<cardRect[0]+cardRect[2] && Input.mouse.y>cardRect[1] && Input.mouse.y<cardRect[1]+cardRect[3];
  if(hoverLocked && pilotPending==null){
    pilotFlash=Math.min(1,pilotFlash+dt*3);
    if(Math.sin(performance.now()/140)>-0.2){
      ctx.textAlign='center'; ctx.font='bold 12px "BOFmil", monospace'; ctx.fillStyle='#ffe98a';
      ctx.fillText('UNLOCK WITH PASSWORD...', VW/2, cardRect[1]+cardRect[3]+18);
    }
  }
  // ---- input ----
  if(pilotComm!=null){ pilotCommT+=dt; drawPilotComm(PILOTS[pilotComm], pilotCommT);
    if(pilotCommT>=1.95){ pilotComm=null; pilotCommT=0; pilotPending=null; pilotSlide=0; const _ps=(typeof PENDING_STAGE!=='undefined'&&PENDING_STAGE)||1; startRun(_ps); if(typeof PENDING_STAGE!=='undefined')PENDING_STAGE=1; } return; }
  if(pilotPending!=null){ pilotSlide+=dt/0.5; if(pilotSlide>=1){ pilotComm=pilotIndex; pilotCommT=0; if(Audio.SFX&&Audio.SFX.goodluck)Audio.SFX.goodluck(); } return; }
  /* NO BACK BUTTON (drop 0801bw). Mike: "remove the back button. k gets you out
     of this menu." menuBack already carries 'k' as of drop 0801bv, and the
     Input.menuBack() call further down handles the exit — so the on-screen
     button and its hit test are simply gone rather than hidden. */
  if(pilotRot>0) return; // lock during spin
  if(Input.menuRight()) startPilotRot(1);
  if(Input.menuLeft()) startPilotRot(-1);
  const mx=Input.mouse.x;
  if(Input.mouse.down && !drawPilot._md){
    if(mx<VW*0.18) startPilotRot(-1);
    else if(mx>VW*0.82) startPilotRot(1);
    else if(cardRect && mx>cardRect[0] && mx<cardRect[0]+cardRect[2]){
      if(locked){ Audio.SFX.hit(); pilotFlash=1; }
      else confirmPilot();
    }
  }
  drawPilot._md=Input.mouse.down;
  if(Input.menuConfirm()){ if(locked){ Audio.SFX.hit(); pilotFlash=1; } else confirmPilot(); }
  if(Input.menuBack()){ setState(GS.DIFF); }
}
function confirmPilot(){ if(pilotPending!=null||pilotRot>0||isPilotLocked(PILOTS[pilotIndex]))return; Audio.SFX.select(); pilotPending=pilotIndex; pilotSlide=0.0001; }
/* CREDITS */
function drawCredits(dt){
  scrollSpaceBG(dt);   // scrolling space backdrop (same as the main menu)
  /* CREDITS now carry the ColeForge brand set (drop 0724bq): the Phoenix Engine logo at the top,
     the four badge icons as a row, and a UI panel behind the text block. */
  if(XART.rdy('cf_logo')){
    const lg=XART.get('cf_logo'), lw=286, lh=lg.naturalHeight*(lw/lg.naturalWidth);
    ctx.drawImage(lg, VW/2-lw/2, 58-lh/2, lw, lh);
  }
  else if(ASSETS.rdy(ASSETS.menuLogo)){ const lg=ASSETS.menuLogo, lw=300, lh=lg.naturalHeight*(lw/lg.naturalWidth); ctx.drawImage(lg, VW/2-lw/2, 64-lh/2, lw, lh); }
  else if(XART.rdy('logo')) XART.draw('logo',VW/2,64,300);
  // badge row — CF shield / star / wings / radar, gently bobbing out of phase
  const _bg=['cfic_shield','cfic_star','cfic_wings','cfic_radar'];
  if(XART.rdy(_bg[0])){
    const bw=42, gap=12, total=_bg.length*bw+(_bg.length-1)*gap;
    _bg.forEach(function(bk,i){
      if(!XART.rdy(bk)) return;
      const im=XART.get(bk), h=bw*(im.naturalHeight/im.naturalWidth);
      const bx=VW/2-total/2+i*(bw+gap), by=112+Math.sin(performance.now()/620+i*0.8)*3;
      ctx.drawImage(im, bx, by-h/2, bw, h);
    });
  }
  // panel behind the credit rows so the text sits on a plate rather than raw space
  if(XART.rdy('cfui_panel')){
    const im=XART.get('cfui_panel'), pw=VW-56, ph=pw*(im.naturalHeight/im.naturalWidth)*1.35;
    ctx.save(); ctx.globalAlpha=0.92;
    ctx.drawImage(im, 28, 176, pw, ph);
    ctx.restore();
  }
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  // stage-1 bitmap font for the section headers + the CREDITS title
  const s1=(ASSETS.stageFont&&ASSETS.stageFont['1'])||(ASSETS.stageArt&&ASSETS.stageArt['1']);
  if(s1 && typeof stageText==='function'){ stageText(s1,'CREDITS',VW/2,150,24,null,null,1,0.08); }
  else { ctx.fillStyle='#f2f5ff'; ctx.font='bold 22px "BOFmil", monospace'; ctx.fillText('CREDITS', VW/2, 150); }
  // label rows -> stage-1 font; name rows -> dialogue font (readable)
  const lines=[
    ['label','DIRECTOR / DESIGNER / CODER / MUSIC / SOUNDS'],
    ['name', 'MICHAEL "FORGE MASTER" COLE'],
    ['gap',''],
    ['label','ART'],
    ['name', 'GPT IMAGES & NANO BANANA PRO'],
    ['gap',''],
    ['name', 'COLEFORGE PHOENIX ENGINE'],
    ['gap',''],
    ['label','WRITTEN, CODED AND DESIGNED BY'],
    ['name', 'MICHAEL "FORGE MASTER" COLE']
  ];
  let y=194;
  lines.forEach(function(row){ const kind=row[0], txt=row[1];
    if(kind==='gap'){ y+=14; return; }
    ctx.textAlign='center';
    if(kind==='label'){
      if(s1 && typeof stageText==='function'){ stageText(s1,txt,VW/2,y+2,13,null,null,1,0.07); y+=28; }
      else { ctx.fillStyle='#aab4c2'; ctx.font='11px "BOFmil", monospace'; ctx.fillText(txt, VW/2, y); y+=24; }
    }
    else { ctx.save(); ctx.shadowColor='rgba(120,180,255,0.5)'; ctx.shadowBlur=6; ctx.fillStyle='#eaf2ff'; ctx.font='bold 14px "BOFmil", monospace'; ctx.fillText(txt, VW/2, y); ctx.restore(); y+=26; }
  });
  ctx.textAlign='center'; ctx.fillStyle='#cfd6e0'; ctx.font='9px "BOFmil", monospace'; ctx.fillText('ENTER / BACKSPACE TO RETURN',VW/2,VH-18);
  if(Input.tap('enter')||Input.tap('backspace')||Input.tap(' ')||backButton()){ setState(GS.TITLE); menuIndex=3; }
}`;

// [B_PW] replaces drawPassword() (and adds keypad helpers + legacy)
const B_PW = String.raw`function drawPassword(dt){
  if(typeof drawCanonBackdrop==='function' && drawCanonBackdrop('nbt_3',0.62)){} else drawBootBackdrop(dt,0.66);
  if(typeof msgText==='function'){ msgText('ENTER PASSWORD',VW/2,24,16,'#f2f5ff',0,1,0.10); } else { ctx.fillStyle='#f2f5ff'; ctx.font='bold 16px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText('ENTER PASSWORD',VW/2,24); }
  const _panelDef={x:16,y:42,w:VW-32,h:VH-42-16};
  const _panel=uiRect('password','panel',_panelDef);
  const wx=_panel.x, wy=_panel.y, ww=_panel.w, wh=_panel.h;
  bofPanel(wx,wy,ww,wh);
  // typed-password slot row — LARGE, chars in the bitmap font of the stage this code unlocks
  // figure out which stage the current input matches/prefixes so we can use its font live
  const _PWMAP={'FURY':1,'IRON':2,'DAM5':3,'STRM':4,'ORBT':5,'TURB':6,'SEWR':7,'DETH':8};
  let _pwStage=1;
  for(const code in _PWMAP){ if(code.slice(0,pwInput.length)===pwInput && pwInput.length>0){ _pwStage=_PWMAP[code]; break; } }
  const _pwFont=(ASSETS.stageFont && ASSETS.stageFont[String(_pwStage)]) || (ASSETS.stageArt && ASSETS.stageArt[String(_pwStage)]);
  const slotY=wy+30, slotN=6, slotW=52, slotGap=8, slotsW=slotN*slotW+(slotN-1)*slotGap, slotX0=VW/2-slotsW/2, slotH=48;
  for(let i=0;i<slotN;i++){
    const sx=slotX0+i*(slotW+slotGap);
    ctx.fillStyle='rgba(0,0,0,0.55)'; roundRectFill(sx,slotY,slotW,slotH,5);
    if(i<pwInput.length){ ctx.save(); ctx.shadowColor='#ffb347'; ctx.shadowBlur=8;
      ctx.strokeStyle='#ffd24a'; ctx.lineWidth=2; ctx.strokeRect(sx,slotY,slotW,slotH); ctx.restore();
      // typed char in the NEXT-stage bitmap font, large
      if(_pwFont && typeof stageText==='function'){ stageText(_pwFont, pwInput[i], sx+slotW/2, slotY+slotH/2+2, 40, null, null, 1, 0.08); }
      else if(typeof msgText==='function'){ msgText(pwInput[i], sx+slotW/2, slotY+slotH/2, 34, '#ffffff', 0, 1, 0.08); }
      else { ctx.fillStyle='#ffe08a'; ctx.font='bold 30px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText(pwInput[i],sx+slotW/2,slotY+34); }
    } else { ctx.strokeStyle='#4a4038'; ctx.lineWidth=2; ctx.strokeRect(sx,slotY,slotW,slotH);
      ctx.fillStyle='rgba(255,179,71,0.22)'; ctx.fillRect(sx+10,slotY+slotH-8,slotW-20,3); }
  }
  // procedurally laid-out keypad — buttons and hitboxes share the exact same coordinates, so they can never drift apart
  const HS=pwHotspots(wx,wy,ww,wh);
  /* TYPING IS A MODE (drop 0801bv). Mike: "do not make typing auto write in a
     password, have a button titled enter password - where you select it in the
     enter password menu to type your password during this mode. If not, wasd or
     arrow keys to use our keyboard."

     Before this, every letter key typed the moment the screen opened — which is
     exactly why WASD could not drive the keypad; they are valid password
     characters. The screen now starts in NAVIGATE mode: WASD and the arrows both
     move the on-screen keypad, and raw letters do nothing. Selecting ENTER
     PASSWORD switches to TYPE mode, where the physical keyboard writes directly.
     K / Esc / gamepad-B leaves type mode without leaving the screen. */
  if(drawPassword.typing==null) drawPassword.typing=false;
  const TYPETGT={c:'__TYPE__', x:VW/2-92, y:wy+94, w:184, h:30, isType:true};
  // add a synthetic BACK target (top-left button) so d-pad can reach it
  const BACKTGT={c:'__BACK__', x:10, y:10, w:92, h:32, isBack:true};
  const NAV=HS.concat([BACKTGT, TYPETGT]);
  {
    const on=(drawPassword.sel===NAV.length-1) || drawPassword.typing;
    const gg=ctx.createLinearGradient(0,TYPETGT.y,0,TYPETGT.y+TYPETGT.h);
    if(drawPassword.typing){ gg.addColorStop(0,'#6ac04a'); gg.addColorStop(1,'#2f6b1f'); }
    else if(on){ gg.addColorStop(0,'#ffd36b'); gg.addColorStop(1,'#d17a15'); }
    else { gg.addColorStop(0,'#39404e'); gg.addColorStop(1,'#1e222b'); }
    ctx.fillStyle=gg; roundRectFill(TYPETGT.x,TYPETGT.y,TYPETGT.w,TYPETGT.h,5);
    ctx.strokeStyle=drawPassword.typing?'#bff3a4':(on?'#ffe6a0':'#57607a'); ctx.lineWidth=2;
    ctx.strokeRect(TYPETGT.x,TYPETGT.y,TYPETGT.w,TYPETGT.h);
    ctx.fillStyle=(on||drawPassword.typing)?'#ffffff':'#cfd6e0';
    ctx.font='bold 12px "BOFmil", monospace'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(drawPassword.typing?'TYPING - K TO STOP':'ENTER PASSWORD', VW/2, TYPETGT.y+TYPETGT.h/2);
    ctx.textBaseline='alphabetic';
  }
  // selector stays UNSET (-1) until the player actually navigates with d-pad/gamepad — keyboard
  // users type directly and shouldn't see a highlighted keypad button hijacking their input.
  if(drawPassword.sel==null) drawPassword.sel=-1;
  // ---- d-pad / arrow navigation: pick the nearest target in the pressed direction ----
  const _navDir=(dx,dy)=>{
    const cur=NAV[drawPassword.sel]; if(!cur) { drawPassword.sel=0; return; }
    const ccx=cur.x+cur.w/2, ccy=cur.y+cur.h/2; let best=-1, bd=1e9;
    for(let i=0;i<NAV.length;i++){ if(i===drawPassword.sel) continue; const t=NAV[i];
      const tx=t.x+t.w/2, ty=t.y+t.h/2, ddx=tx-ccx, ddy=ty-ccy;
      if(dx!==0 && Math.sign(ddx)!==dx) continue;
      if(dy!==0 && Math.sign(ddy)!==dy) continue;
      const along=dx!==0?Math.abs(ddx):Math.abs(ddy), perp=dx!==0?Math.abs(ddy):Math.abs(ddx);
      const score=along+perp*2.2; if(score<bd){ bd=score; best=i; }
    }
    if(best>=0){ drawPassword.sel=best; Audio.SFX.blip(); }
  };
  /* WASD *AND* the arrows drive the keypad now. They are only password letters
     while TYPE mode is on, and navigation is disabled in that mode anyway. */
  if(!drawPassword.typing){
    if(Input.tap('arrowleft')||Input.tap('pad_left')||Input.tap('a')) _navDir(-1,0);
    if(Input.tap('arrowright')||Input.tap('pad_right')||Input.tap('d')) _navDir(1,0);
    if(Input.tap('arrowup')||Input.tap('pad_up')||Input.tap('w')) _navDir(0,-1);
    if(Input.tap('arrowdown')||Input.tap('pad_down')||Input.tap('s')) _navDir(0,1);
  }
  const mx=Input.mouse.x, my=Input.mouse.y; let hover=null;
  for(let hi=0; hi<HS.length; hi++){ const h=HS[hi];
    const on = (mx>=h.x && mx<=h.x+h.w && my>=h.y && my<=h.y+h.h) || (drawPassword.sel===hi);
    if(on) hover=h;
    const kg=ctx.createLinearGradient(0,h.y,0,h.y+h.h);
    if(on){ kg.addColorStop(0,'#ffd36b'); kg.addColorStop(1,'#d17a15'); } else { kg.addColorStop(0,'#39404e'); kg.addColorStop(1,'#1e222b'); }
    if(on){ ctx.save(); ctx.shadowColor='#ffb347'; ctx.shadowBlur=8; }
    ctx.fillStyle=kg; roundRectFill(h.x,h.y,h.w,h.h,4);
    if(on) ctx.restore();
    ctx.strokeStyle= on?'#ffe6a0':'#57607a'; ctx.lineWidth=1.5; ctx.strokeRect(h.x,h.y,h.w,h.h);
    ctx.fillStyle='rgba(255,255,255,0.10)'; ctx.fillRect(h.x+2,h.y+2,h.w-4,2);
    ctx.fillStyle= on?'#1a1408':'#e8ecf4'; ctx.font='bold '+(h.wide?11:12)+'px "BOFmil", monospace';
    ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(h.c,h.x+h.w/2,h.y+h.h/2);
  }
  ctx.textBaseline='alphabetic';
  // MOUSE: click a keypad button
  if(Input.mouse.down && !drawPassword._md && hover){ pwKey(hover.c); }
  drawPassword._md=Input.mouse.down;
  // GAMEPAD only: the A/confirm button presses the highlighted on-screen keypad key (or BACK).
  // (Keyboard fire keys are NOT used here — the keyboard types directly below, and Enter submits.)
  const _padFire=Input.tap('pad_b0')||Input.tap('pad_b9');
  if(_padFire){ const t=NAV[drawPassword.sel!=null?drawPassword.sel:0];
    if(t && t.isBack){ setState(GS.TITLE); menuIndex=0; pwInput=''; drawPassword.typing=false; Audio.SFX.select(); return; }
    if(t && t.isType){ drawPassword.typing=!drawPassword.typing; Audio.SFX.select(); return; }
    else if(t){ pwKey(t.c); }
  }
  // KEYBOARD: letters/digits type directly; Enter submits; Backspace deletes (or exits when empty).
  // Enter must NEVER insert the highlighted keypad letter — that caused the "stuck on B" typing.
  if(Input.tap('enter')){ submitPassword(); }
  else if(Input.tap('backspace')||Input.tap('pad_b1')||Input.tap('pad_b8')){
    if(drawPassword.typing){ drawPassword.typing=false; Audio.SFX.blip(); }   // leave type mode first
    else if(pwInput.length) pwKey('BACK');
    else { setState(GS.TITLE); menuIndex=0; }
  }
  else if(drawPassword.typing && Input.tap('escape')){ drawPassword.typing=false; Audio.SFX.blip(); }
  else if(drawPassword.typing){
    /* RAW KEYBOARD ONLY IN TYPE MODE. 'k' is reserved as the exit, so it is the
       one letter the keyboard will not write — the on-screen keypad still can. */
    for(const k in Input.keys){
      if(k==='k'){ if(Input.tap(k)){ drawPassword.typing=false; Audio.SFX.blip(); } continue; }
      if(k.length===1 && /[a-z0-9]/i.test(k) && Input.tap(k)){ pwKey(k.toUpperCase()); }
    }
  }
  if(drawPassword.err>0){ drawPassword.err-=dt; ctx.fillStyle='#ff4a4a'; ctx.font='bold 12px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText('INVALID CODE',VW/2,wy+wh+12); }
  if(drawPassword.unlockMsg>0){ drawPassword.unlockMsg-=dt; ctx.fillStyle='#8de23a'; ctx.font='bold 12px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText('COLE UNLOCKED!',VW/2,wy+wh+12); }
  if(backButton()){ setState(GS.TITLE); menuIndex=0; pwInput=''; Audio.SFX.select(); }
}
function pwHotspots(wx,wy,ww,wh){
  const H=[], r1='ABCDEFGHIJKLM', r2='NOPQRSTUVWXYZ', dg='0123456789';
  const gx0=wx+14, gw=ww-28;
  const rowH=26, rowGap=6;
  // anchor the keypad to the BOTTOM of the screen (4 rows + the action row)
  const totalKbH=(rowH+rowGap)*3 + (rowH+4) + 8;
  const rowY0=VH-16-totalKbH;
  // row1: 13 letters
  { const n=13, bw=(gw-(n-1)*4)/n;
    for(let i=0;i<n;i++) H.push({c:r1[i], x:gx0+i*(bw+4), y:rowY0, w:bw, h:rowH}); }
  // row2: 13 letters
  { const n=13, bw=(gw-(n-1)*4)/n, y=rowY0+(rowH+rowGap);
    for(let i=0;i<n;i++) H.push({c:r2[i], x:gx0+i*(bw+4), y:y, w:bw, h:rowH}); }
  // row3: 10 digits, centered and a bit wider
  { const n=10, bw=(gw*0.8-(n-1)*4)/n, y=rowY0+(rowH+rowGap)*2, x0=gx0+gw*0.1;
    for(let i=0;i<n;i++) H.push({c:dg[i], x:x0+i*(bw+4), y:y, w:bw, h:rowH}); }
  // row4: BACK / CLEAR / ENTER
  { const y=rowY0+(rowH+rowGap)*3+8, bw=(gw-2*10)/3;
    H.push({c:'BACK',  x:gx0,             y:y, w:bw, h:rowH+4, wide:true});
    H.push({c:'CLEAR', x:gx0+bw+10,       y:y, w:bw, h:rowH+4, wide:true});
    H.push({c:'ENTER', x:gx0+2*(bw+10),   y:y, w:bw, h:rowH+4, wide:true});
  }
  return H;
}
function pwKey(c){
  if(c==='BACK'){ if(pwInput.length){pwInput=pwInput.slice(0,-1);Audio.SFX.blip();} else { setState(GS.TITLE); menuIndex=0; } return; }
  if(c==='CLEAR'){ pwInput=''; Audio.SFX.blip(); return; }
  if(c==='ENTER'){ submitPassword(); return; }
  if(pwInput.length<6){ pwInput+=c; Audio.SFX.blip(); }
}
function drawPasswordLegacy(dt){
  ctx.textAlign='center'; ctx.fillStyle='#ffd36b'; ctx.font='bold 18px "BOFmil", monospace'; ctx.fillText('ENTER PASSWORD',VW/2,140);
  metalPanel(VW/2-110,170,220,46); ctx.fillStyle='#8de23a'; ctx.font='bold 22px "BOFmil", monospace';
  const show=(pwInput+'______').slice(0,6); ctx.fillText(show.split('').join(' '),VW/2,202);
  ctx.fillStyle='#9aa0aa'; ctx.font='8px "BOFmil", monospace'; ctx.fillText('TYPE UP TO 6 CHARS \u00B7 ENTER CONFIRM \u00B7 BKSP BACK',VW/2,250);
  for(const k in Input.keys){ if(Input.tap(k)){
    if(k.length===1 && /[a-z0-9]/i.test(k) && pwInput.length<6){ pwInput+=k.toUpperCase(); Audio.SFX.blip(); }
    else if(k==='backspace'){ if(pwInput.length){pwInput=pwInput.slice(0,-1);Audio.SFX.blip();} else {setState(GS.TITLE);menuIndex=0;} }
    else if(k==='enter'){ submitPassword(); } }}
  if(backButton()){ setState(GS.TITLE); menuIndex=0; pwInput=''; Audio.SFX.select(); }
}`;

// [B_LAUNCH] inserted right before "function metalBanner(){"
const B_LAUNCH = String.raw`/* ===== SIGNATURE LAUNCH CINEMATIC ===== */
const LAUNCH_TERR=['terr_grass','terr_desert','terr_ice','terr_road','terr_war'];
function _ease(x){ return x<0.5?2*x*x:1-Math.pow(-2*x+2,2)/2; }
let _slines=null;
function _speedLines(intensity){
  if(!_slines){ _slines=[]; for(let i=0;i<46;i++) _slines.push({x:rnd(0,VW),y:rnd(0,VH),len:rnd(20,90),sp:rnd(9,22)}); }
  ctx.save(); ctx.strokeStyle='rgba(255,255,255,'+(0.22*intensity)+')'; ctx.lineWidth=1.5;
  for(const l of _slines){ l.y+=l.sp; if(l.y>VH+l.len){ l.y=-l.len; l.x=rnd(0,VW); }
    ctx.beginPath(); ctx.moveTo(l.x,l.y); ctx.lineTo(l.x,l.y+l.len); ctx.stroke(); } ctx.restore();
}
function _scrollVAbs(img,dist){
  if(!img||!img.complete||!img.naturalWidth){ ctx.fillStyle='#0c0e12'; ctx.fillRect(0,0,VW,VH); return; }
  const sc=Math.max(VW/img.naturalWidth, VH/img.naturalHeight), dw=img.naturalWidth*sc, dh=img.naturalHeight*sc;
  let off=dist%dh; if(off<0)off+=dh;
  for(let yy=off-dh; yy<VH; yy+=dh){ ctx.drawImage(img,(VW-dw)/2,yy,dw,dh); }   /* NO flip */
}
/* draw the selected pilot's ship (idle '', thrust '_t', bank '_l'/'_r') */
function _shipK(suf){ const p=(run&&run.pilot)||'axel'; const k='ship_'+p+(suf||''); return (typeof XART!=='undefined'&&XART.rdy(k))?k:null; }
function drawShipSprite(x,y,h,suf){
  let k=_shipK(suf); if(!k) k=_shipK('_t'); if(!k) k=_shipK('');
  if(k){ const im=XART.get(k); const w=h*(im.naturalWidth/im.naturalHeight); ctx.drawImage(im,x-w/2,y-h/2,w,h); return; }
  if(ASSETS.has&&ASSETS.has('player')){ const fr=ASSETS.dims('player'), sc=h/fr.h;
    // legacy player_thrust blit removed (drop 0724cj) — a second engine under our own
    ASSETS.blit('player',x,y,fr.w*sc,h); return; }
  ctx.save(); ctx.translate(x,y); ctx.scale(h/40,h/40); drawStaticPlayer(); ctx.restore();
}
function _groundScroll(dist){
  ctx.fillStyle='#000'; ctx.fillRect(0,0,VW,VH);
  const pad=XART.get('landingpad'), run=XART.get('runway');
  let padH=0; const padW=VW;
  if(pad&&pad.complete&&pad.naturalWidth){ padH=padW*(pad.naturalHeight/pad.naturalWidth); }
  const padTop=(VH+dist)-padH;                 /* pad bottom starts at VH, slides down as dist grows */
  if(run&&run.complete&&run.naturalWidth){     /* runway attached above the pad, seamless tiling */
    const rw=VW, rh=rw*(run.naturalHeight/run.naturalWidth); let y=padTop;
    while(y>-rh){ y-=rh; ctx.drawImage(run,0,y,rw,rh); }
  }
  if(pad&&pad.complete&&pad.naturalWidth) ctx.drawImage(pad,(VW-padW)/2,padTop,padW,padH);
}
function _pilotStill(P){
  if(typeof drawPilotBG==='function') drawPilotBG(P.tint); else { ctx.fillStyle='#101018'; ctx.fillRect(0,0,VW,VH); }
  const k='card_'+P.key;
  if(XART.rdy(k)){ const im=XART.get(k); let w=Math.min(VW-30,452), h=w*(im.naturalHeight/im.naturalWidth); const mh=VH*0.62; if(h>mh){h=mh;w=h*(im.naturalWidth/im.naturalHeight);} ctx.drawImage(im,VW/2-w/2,VH*0.455-h/2,w,h); }
}
/* ===== continuous filmstrip transition (NO fades / NO cuts) ===== */
const ANCHORY=0.60;                         /* player "front" as a screen fraction */
const SEG_B1=2000, SEG_B2=SEG_B1+2200, SEG_B3=SEG_B2+8800;   /* runway | terrain | liquid | level(entrance) */
function _liquidFrame(){
  /* Upgraded beds first (drop 0724f: seam-healed, native 1:1). These are real Image objects, so
     _region draws them directly; the legacy ASSETS path stays as the fallback for any stage
     whose bed was never upgraded. */
  if(typeof seqBedFrames==='function'){
    const fr=seqBedFrames(run.stage);
    if(fr && fr.length) return fr[Math.floor(performance.now()/150)%fr.length];
  }
  const s=run.stage; let frames=ASSETS.water; if(s===2)frames=ASSETS.lava;
  const f2=(frames&&frames.length)?frames[Math.floor(performance.now()/70)%frames.length]:null;
  return (f2&&ASSETS.rdy&&ASSETS.rdy(f2))?f2:null; }
/* tile an image across world-band [wStart,wEnd]; the world scrolls DOWN as dist grows (no fades) */
function _region(img,wStart,wEnd,dist,tint,fallback){
  const anchorY=VH*ANCHORY;
  const bandTop=anchorY-(wEnd-dist), bandBot=anchorY-(wStart-dist);
  const cTop=Math.max(0,bandTop), cBot=Math.min(VH,bandBot);
  if(cBot<=cTop) return;
  ctx.save(); ctx.beginPath(); ctx.rect(0,cTop,VW,cBot-cTop); ctx.clip();
  if(img&&img.complete&&img.naturalWidth){
    // NATIVE-SIZE LIQUIDS. This stretched every texture to the full VW, so the 128px liquid tiles
    // came out ~3.75x upscaled and mushy during the runway/launch scenes. A small square tile is
    // meant to TILE at 1:1 (that is the whole point of the 0724f tiling fix), so anything that is
    // roughly square and small is now drawn at its own size and repeated across, exactly like the
    // in-level tiler. Wide plates (runways, connectors, masters) still fill the width as before.
    const _sq = img.naturalWidth<=256 && Math.abs(img.naturalWidth-img.naturalHeight)<=img.naturalWidth*0.4;
    const dw = _sq ? img.naturalWidth : VW;
    const dh = _sq ? img.naturalHeight : dw*(img.naturalHeight/img.naturalWidth);
    for(let y=wStart; y<wEnd+dh; y+=dh){
      const st=anchorY-((y+dh)-dist);
      if(st>VH||st+dh<0) continue;
      if(dw<VW){ for(let xx=0; xx<VW; xx+=dw) ctx.drawImage(img, xx, st, dw, dh); continue; }
      ctx.drawImage(img,0,0,img.naturalWidth,img.naturalHeight,0,Math.round(st),dw,Math.ceil(dh));
    }
  } else if(fallback){ ctx.fillStyle=fallback; ctx.fillRect(0,cTop,VW,cBot-cTop); }
  if(tint){ ctx.fillStyle=tint; ctx.fillRect(0,cTop,VW,cBot-cTop);
    ctx.globalAlpha=0.45; ctx.fillStyle='#eaf9ff';
    for(let i=0;i<7;i++){ const y=cTop+((dist*0.5+i*96)%(cBot-cTop)); ctx.fillRect(0,Math.round(y),VW,2); } ctx.globalAlpha=1; }
  ctx.restore();
}
/* the stage itself scrolls in from the top (the "entrance"): drawBG clipped above the SEG_B3 seam */
function _drawLevelRegion(dist,dt){
  const seam=VH*ANCHORY-(SEG_B3-dist);
  if(seam<=0) return;
  ctx.save(); ctx.beginPath(); ctx.rect(0,0,VW,Math.min(VH,seam)); ctx.clip();
  drawBG(dt);
  ctx.restore();
}
function drawLaunch(dt){
  if(drawLaunch._phase===undefined || stateT < (drawLaunch._lastT||0)-0.001){ drawLaunch._dist=0; drawLaunch._spd=110; drawLaunch._phase='run'; drawLaunch._pt=0;
    drawLaunch._eng=false; drawLaunch._thr=false; drawLaunch._brk=false; drawLaunch._go=false; drawLaunch._num=99; drawLaunch._mus=false; }
  drawLaunch._lastT=stateT;
  const t=stateT;
  if(!drawLaunch._mus){ drawLaunch._mus=true; Audio.startMusic((curStage&&curStage.music)||'stage'); }
  const ph=drawLaunch._phase;
  /* ---- speed / phase machine: run is distance-driven so the level always shows before braking ---- */
  const _space=(run.stage===5);
  const _spdCap=_space?3200:1750;   // space launch is faster than we've ever gone
  if(ph==='run'){
    drawLaunch._spd=Math.min(_spdCap, drawLaunch._spd+(_space?2600:1500)*dt);
    drawLaunch._dist+=drawLaunch._spd*dt;
    if(drawLaunch._dist>=SEG_B3+240){ drawLaunch._phase='brake'; drawLaunch._pt=0; if(Audio.SFX.brake)Audio.SFX.brake(); }   /* sped a little past into the level */
    /* STAGE 6 is the exception Mike called out: runway -> SKY. It keeps climbing instead of
       settling onto ground, and the cloud deck thickens as it goes. */
    if(typeof seqCfg==='function' && seqCfg(run.stage).sky){
      drawLaunch._sky=clamp((drawLaunch._dist-SEG_B1)/Math.max(1,(SEG_B3-SEG_B1)),0,1);
      drawLaunch._spd=Math.min(_spdCap*1.35, drawLaunch._spd+900*dt);
    }
  } else if(ph==='brake'){
    drawLaunch._pt+=dt; const p=clamp(drawLaunch._pt/2.0,0,1); drawLaunch._spd=lerp(1750,0,_ease(p));
    drawLaunch._dist+=drawLaunch._spd*dt;                          /* level keeps scrolling in smoothly while braking */
    if(drawLaunch._pt>=2.0){ drawLaunch._phase='settle'; drawLaunch._pt=0; }
  } else if(ph==='settle'){
    /* WAS 'reverse': it shoved dist backwards by up to 300px, which read as the player being
       yanked back just before GO. Mike flagged it. Now the world simply comes to REST — no
       negative travel, no drift — and the ship holds the exact spot it will start play from. */
    drawLaunch._pt+=dt; drawLaunch._spd=0;
    if(drawLaunch._pt>=0.45){ drawLaunch._phase='cd'; drawLaunch._pt=0; }
  } else { drawLaunch._pt+=dt; drawLaunch._spd=0; }
  const dist=drawLaunch._dist, nrm=clamp(drawLaunch._spd/1750,0,1);
  const art=(typeof curArt==='function')&&curArt();
  const X=(typeof XART!=='undefined')?XART:null;
  /* ---- one continuous scroll (far->near): level entrance, liquid, terrain, runway, pad ---- */
  ctx.fillStyle='#05070a'; ctx.fillRect(0,0,VW,VH);
  const rum=nrm*4; ctx.save(); if(rum>0.2) ctx.translate(rnd(-rum,rum),rnd(-rum,rum));
  _drawLevelRegion(dist,dt);
  if(typeof seqCfg==='function' && seqCfg(run.stage).sky){
    /* SKY LAUNCH: open sky instead of a liquid bed, with the parallax cloud deck thickening as
       the climb builds. No ground to tile up here. */
    const sky=clamp(drawLaunch._sky||0,0,1);
    ctx.save();
    ctx.fillStyle=seqCfg(run.stage).fill; ctx.fillRect(0,0,VW,VH);
    if(X && X.rdy('nsky6_par')){
      const im=X.get('nsky6_par');
      const dh=VW*(im.naturalHeight/im.naturalWidth);
      const layers=1+Math.round(sky*3);                 /* more cloud passes the higher we get */
      for(let L=0; L<layers; L++){
        ctx.globalAlpha=0.30+0.16*L;
        let off=((dist*(0.5+L*0.35))%dh); if(off<0) off+=dh;
        for(let yy=off-dh; yy<VH; yy+=dh) ctx.drawImage(im,0,yy,VW,dh);
      }
    }
    ctx.restore();
  } else {
    _region(_liquidFrame(), SEG_B2, SEG_B3, dist, (run.stage===3?'rgba(150,222,255,0.42)':null), (run.stage===2?'#241008':'#0a1505'));
  }
  // TERRAIN region removed per Mike — runway extends straight up to the liquid
  /* RUNWAY: stages 4 and 7 have authored 800x1000 plates (approach / main / exit). Everything
     else has no runway art at all, so it keeps the legacy strip. Never invent a runway. */
  const _rwMain=(typeof seqRunway==='function')?seqRunway(run.stage,'run'):null;
  const _rwApp =(typeof seqRunway==='function')?seqRunway(run.stage,'app'):null;
  /* CONNECTOR: entering stage N>1, the plate that bridges N-1 -> N scrolls through FIRST, below
     the runway. 3>4, 4>5, 6>7 and 7>8 were drawn; 1>2, 2>3 and 5>6 never were, so those stages
     simply open on their own bed instead of a bridge that does not exist. */
  const _con=(typeof seqConnector==='function' && run.stage>1) ? seqConnector(run.stage-1, run.stage) : null;
  if(_con && X) _region(X.get(_con), -2000, -600, dist, null, null);
  if(_rwMain && X){
    /* FULL RUNWAY SEQUENCE, in the order you actually fly it:
         start-approach (behind you, where you rolled from) -> main-runway (tiled, the roll) ->
         runway-exit (the lip you leave the ground on, right before the bed opens up).
       Stages 4 and 7 have all three; stage 1's legacy strip only has the main part. */
    const _rwExit=(typeof seqRunway==='function')?seqRunway(run.stage,'exit'):null;
    if(_rwApp) _region(X.get(_rwApp), -1000, 0, dist, null, null);
    _region(X.get(_rwMain), 0, SEG_B1, dist, null, (typeof seqCfg==='function'?seqCfg(run.stage).fill:'#14140f'));
    if(_rwExit) _region(X.get(_rwExit), SEG_B1, SEG_B2, dist, null, null);
    else _region(X.get(_rwMain), SEG_B1, SEG_B2, dist, null, null);
  } else {
    _region(X&&X.get('runway'), 0, SEG_B2, dist, null, '#14140f');
  }
  if(X){ const pad=X.get('landingpad'); if(pad&&pad.complete&&pad.naturalWidth){    /* pad drawn once at the very start */
    const dw=VW, dh=dw*(pad.naturalHeight/pad.naturalWidth), st=VH*ANCHORY-(dh-dist);
    if(st<VH && st+dh>0) ctx.drawImage(pad,0,Math.round(st),dw,Math.ceil(dh)); } }
  ctx.restore();
  _speedLines((run.stage===5?0.25:0.10)+(run.stage===5?1.3:0.85)*nrm);
  /* ---- sfx cues ---- */
  /* NO LAUNCH OR THRUSTER CUES (drop 0801fd). Mike: "no more thruster or launch
     sounds." Both were one-shots fired from the transition; the music carries it.
     (drawLaunch lives in patches.js, not gamecode.js - my first patch went into
     the dead copy and did nothing, same as the HUD in 0801ej.) */
  /* ---- ship: launches off the pad, pulls up over the run, settles into the level ---- */
  let shipY, suf='_t', shipH=62;
  if(ph==='run'){ shipY=lerp(VH*0.66, VH*0.42, _ease(clamp(dist/SEG_B1,0,1)))+Math.sin(t*3)*3;
    if(_space){ // lifting off: the ship scales up as it rockets toward space
      const lift=_ease(clamp(dist/(SEG_B3),0,1)); shipH=lerp(62, 128, lift); shipY=lerp(VH*0.66, VH*0.30, lift); }
  }
  else if(ph==='brake'){ shipY=lerp(VH*0.42, VH*0.60, _ease(clamp(drawLaunch._pt/2.0,0,1))); if(_space) shipH=lerp(128,62,_ease(clamp(drawLaunch._pt/2.0,0,1))); }
  else { shipY=VH*0.60; suf=''; }  // 3-2-1-GO: hold the ship still, no bob/drift
  drawShipSprite(VW/2, shipY, shipH, suf);
  /* THE PILOT'S OWN ANIMATED PLUME (drop 0801fd). Mike: "start using our pilots
     with the animated thruster during the stage transitions, no more static
     images. this applies for all 9 of them."

     nthp_<pilot>_0..3 is a four-frame plume authored for every one of the nine
     and already in PRELOAD, but it was only ever drawn during PLAY - the
     transition showed the ship with nothing behind it. */
  if(typeof XART!=='undefined'){
    const _tk='nthp_'+(run.pilot||'cole')+'_'+(((performance.now()/70)|0)%4);
    if(XART.rdy(_tk)){
      const im=XART.get(_tk);
      const _th=shipH*1.15, _tw=_th*(im.naturalWidth/Math.max(1,im.naturalHeight));
      ctx.save();
      ctx.globalCompositeOperation='lighter';
      ctx.globalAlpha=(ph==='run')?0.95:0.55;      // full burn on the run, banked on the brake
      ctx.drawImage(im, VW/2-_tw/2, shipY+shipH*0.30, _tw, _th);
      ctx.restore();
    }
  }
  /* ---- GET READY 3-2-1 -> GO ---- */
  if(ph==='cd'){
    const ct=drawLaunch._pt;
    if(ct<3.0){
      const num=3-Math.floor(ct);
      if(drawLaunch._num!==num){ drawLaunch._num=num; if(Audio.SFX.getready)Audio.SFX.getready(); }
      if(art){ stageText(art,'GET READY',VW/2,VH*0.34,20,null,null,1,0.12);
        const f=ct-Math.floor(ct),pop=1+(1-f)*0.5; stageText(art,String(num),VW/2,VH*0.52,52*pop,null,null,1,0.10); }
      else { ctx.textAlign='center'; ctx.fillStyle='#ffd36b'; ctx.font='bold 44px "BOFmil", monospace'; ctx.fillText(String(num),VW/2,VH*0.54); }
    } else {
      if(!drawLaunch._go){ drawLaunch._go=true; if(Audio.SFX.go)Audio.SFX.go(); shake=Math.max(shake,5); }
      const f=clamp((ct-3.0)/0.85,0,1),pop=1+(1-f)*0.8;
      if(typeof msgText==='function'){ msgText('GO!',VW/2,VH*0.46,64*pop,'#ffffff',0,1,0.08); }
      else { ctx.textAlign='center'; ctx.fillStyle='#ffffff'; ctx.font='bold 60px "BOFmil", monospace'; ctx.fillText('GO!',VW/2,VH*0.5); }
      if(ct>=3.85){ finishLaunch(); }
    }
  }
  /* NON-SKIPPABLE: no skip input */
}
function finishLaunch(){ drawLaunch._eng=false; drawLaunch._thr=false;
  if(!drawLaunch._mus) Audio.startMusic((curStage&&curStage.music)||'stage'); drawLaunch._mus=false;
  setState(GS.PLAY);
}
`;

// [B_OPTIONS] replaces drawOptions() with a panel-art-skinned version (+ legacy fallback)
const B_OPTIONS = String.raw`/* OPTIONS — skinned with control/volume panel art */
function bofPanel(x,y,w,h){
  // steel plate
  const g=ctx.createLinearGradient(0,y,0,y+h);
  g.addColorStop(0,'rgba(26,30,40,0.96)'); g.addColorStop(0.5,'rgba(14,17,24,0.96)'); g.addColorStop(1,'rgba(20,23,32,0.96)');
  ctx.fillStyle=g; roundRectFill(x,y,w,h,8);
  // rivet strip top/bottom
  ctx.fillStyle='rgba(255,179,71,0.14)'; ctx.fillRect(x+8,y+6,w-16,2); ctx.fillRect(x+8,y+h-8,w-16,2);
  // outer frame + orange corner brackets (BOF HUD style)
  ctx.strokeStyle='#3c4250'; ctx.lineWidth=2; ctx.strokeRect(x,y,w,h);
  ctx.strokeStyle='#ffb347'; ctx.lineWidth=3; const L=22;
  for(const [cx,cy,dx,dy] of [[x,y,1,1],[x+w,y,-1,1],[x,y+h,1,-1],[x+w,y+h,-1,-1]]){
    ctx.beginPath(); ctx.moveTo(cx+dx*L,cy); ctx.lineTo(cx,cy); ctx.lineTo(cx,cy+dy*L); ctx.stroke();
  }
}
function bofTitle(txt,cx,cy,H){
  /* PANEL FONT, NOT THE STAGE FONT (drop 0801bp). Mike: "fix the font up top in
     the options menu."

     This ran through msgText, which composites the per-stage BITMAP font - the
     distressed, chipped lettering meant for stage-name cards. Every other label
     on this panel (VOLUME, CONTROLS, MASTER, the key caps) is drawn in BOFmil,
     so the title was the one element in a different typeface entirely.

     Drawn in BOFmil directly at the panel's own accent colour, with a dark seat
     behind it so it still reads against a bright backdrop. */
  const h=H||16;
  ctx.save();
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.font='bold '+Math.round(h*1.35)+'px "BOFmil", monospace';
  const t=String(txt).toUpperCase();
  ctx.lineWidth=Math.max(3,Math.round(h*0.28)); ctx.strokeStyle='rgba(0,0,0,0.78)';
  ctx.strokeText(t,cx,cy+h*0.35);
  ctx.shadowColor='rgba(255,179,71,0.55)'; ctx.shadowBlur=10;
  ctx.fillStyle='#ffd36b'; ctx.fillText(t,cx,cy+h*0.35);
  ctx.restore(); ctx.textBaseline='alphabetic';
}
const VOL_KINDS=['master','music','sfx','voice'];
const CTRL_ACTS=['left','right','up','down','fire','bomb','retina'];
const CTRL_LABELS=['MOVE LEFT','MOVE RIGHT','MOVE UP','MOVE DOWN','FIRE','MISSILE','RETINA LOCK'];
let voiceVol=1.0, optScroll=0, optSnap=null, optDrag=-1, optSbDrag=false, optSelIdx=0;
function optSnapshot(){ optSnap={master:Audio.getVol('master'),music:Audio.getVol('music'),sfx:Audio.getVol('sfx'),voice:voiceVol,keybind:JSON.parse(JSON.stringify(keybind))}; }
function optCancel(){ if(optSnap){ Audio.setVol('master',optSnap.master); Audio.setVol('music',optSnap.music); Audio.setVol('sfx',optSnap.sfx); voiceVol=optSnap.voice; Audio.setVol('voice',voiceVol); for(const a in optSnap.keybind) keybind[a]=optSnap.keybind[a].slice(); } optSnap=null; optScroll=0; rebindAction=null; setState(GS.TITLE); menuIndex=2; Audio.SFX.select(); }
function optApply(){ saveKeybind(); if(Audio.saveVol)Audio.saveVol(); optSnap=null; optScroll=0; rebindAction=null; setState(GS.TITLE); menuIndex=2; Audio.SFX.select(); }
function drawOptions(dt){
  if(typeof drawCanonBackdrop==='function' && drawCanonBackdrop('nbt_4',0.60,1)){} else drawTitleBackdrop(dt);
  if(optSnap==null) optSnapshot();
  const m=Input.mouse;
  ctx.textBaseline='alphabetic'; bofTitle('OPTIONS',VW/2,20,16);
  const _panelDef={x:28,y:40,w:VW-56,h:VH-40-58};
  const _panel=uiRect('options','panel',_panelDef);
  const wx=_panel.x, wy=_panel.y, ww=_panel.w, wh=_panel.h;
  bofPanel(wx,wy,ww,wh);
  const rows=[{t:'head',label:'VOLUME'}]; const vk=['master','music','sfx','voice'], vl=['MASTER','MUSIC','SFX','VOICE'];
  for(let i=0;i<4;i++) rows.push({t:'vol',k:vk[i],label:vl[i]});
  rows.push({t:'head',label:'CONTROLS'});
  for(let i=0;i<7;i++) rows.push({t:'ctrl',act:CTRL_ACTS[i],label:CTRL_LABELS[i]});
  const selectable=rows.map((r,i)=>({r,i})).filter(o=>o.r.t!=='head');
  if(optSelIdx==null||optSelIdx<0) optSelIdx=0;
  optSelIdx=clamp(optSelIdx,0,selectable.length-1);
  const rh=32, pad=8, contentH=rows.length*rh+pad*2, maxScroll=Math.max(0,contentH-wh);
  if(m.wheel){ optScroll=clamp(optScroll+m.wheel*0.6,0,maxScroll); m.wheel=0; }
  // keyboard navigation: up/down (w/s) move the selection, auto-scrolling into view
  if(!rebindAction){
    if(Input.menuDown()){ optSelIdx=clamp(optSelIdx+1,0,selectable.length-1); }
    if(Input.menuUp()){ optSelIdx=clamp(optSelIdx-1,0,selectable.length-1); }
  }
  const sx0=wx+120, sx1=wx+ww-64, SEG=10, segW=(sx1-sx0)/SEG;
  function adjustVol(k,delta){ let v=(k==='voice')?voiceVol:Audio.getVol(k); v=clamp(Math.round((v+delta)*SEG)/SEG,0,1); if(k==='voice'){voiceVol=v; Audio.setVol('voice',v);} else Audio.setVol(k,v); Audio.SFX.blip(); }
  const selRow=selectable[optSelIdx].r, selY=selectable[optSelIdx].i;
  if(!rebindAction && selRow.t==='vol'){
    if(Input.menuLeft()) adjustVol(selRow.k,-1/SEG);
    if(Input.menuRight()) adjustVol(selRow.k, 1/SEG);
  }
  if(!rebindAction && selRow.t==='ctrl' && (Input.tap('enter')||keybind.fire.some(k=>Input.tap(k)))){ rebindAction=selRow.act; Audio.SFX.blip(); }
  // keep the selected row scrolled into view
  { const targetY=pad+selY*rh; if(targetY-optScroll<0) optScroll=clamp(targetY,0,maxScroll); if(targetY-optScroll>wh-rh) optScroll=clamp(targetY-wh+rh,0,maxScroll); }
  ctx.save(); ctx.beginPath(); ctx.rect(wx,wy,ww,wh); ctx.clip();
  let y=wy+pad-optScroll;
  for(const r of rows){ const cy=y+rh/2, rowIdx=rows.indexOf(r);
    if(y+rh>wy-2 && y<wy+wh+2){
      const isSel = r.t!=='head' && selectable[optSelIdx].r===r;
      if(isSel){ ctx.fillStyle='rgba(255,180,60,0.10)'; ctx.fillRect(wx+2,y,ww-4,rh); }
      if(r.t==='head'){ ctx.fillStyle='#ffb347'; ctx.font='bold 12px "BOFmil", monospace'; ctx.textAlign='left'; ctx.textBaseline='middle'; ctx.fillText(r.label,wx+14,cy); ctx.strokeStyle='rgba(255,150,60,0.28)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(wx+92,cy); ctx.lineTo(wx+ww-14,cy); ctx.stroke(); }
      else if(r.t==='vol'){
        ctx.fillStyle=isSel?menuSelWhite():'#cfd6e0'; ctx.font='bold 11px "BOFmil", monospace'; ctx.textAlign='left'; ctx.textBaseline='middle'; ctx.fillText(r.label,wx+16,cy);
        /* YELLOW on options (drop 0801bk), per Mike. NOTE: gamecode.js also has a
           drawOptions, but B_OPTIONS REPLACES it wholesale — editing the gamecode
           copy changes nothing that ships. This is the live one. */
        /* CURSOR INBOARD (drop 0801bp). Mike: "make the cursor actually visible
           in our options thing."

           menuSelMark draws its arrows at cx +/- (halfW + 16). With halfW =
           ww/2-10 that placed them at wx-26 and wx+ww+26 - OUTSIDE the window on
           both sides. All that showed were the slivers landing on the frame.
           Pulled well inside the row so both arrows sit on the panel. */
        if(isSel && typeof menuSelMark==='function') menuSelMark(wx+ww/2, cy, ww/2-46, '#ffd24a');
        let vol=(r.k==='voice')?voiceVol:Audio.getVol(r.k); const rid='v_'+r.k;
        // segmented rectangle boxes — click a box to set that level, drag across to scroll through them
        const hoverRow = m.x>=sx0-6 && m.x<=sx1+6 && Math.abs(m.y-cy)<12 && m.y>wy && m.y<wy+wh;
        if(m.down && optDrag===-1 && !drawOptions._md && hoverRow) optDrag=rid;
        if(m.down && optDrag===rid){ vol=clamp((m.x-sx0)/(sx1-sx0),0,1); vol=Math.round(vol*SEG)/SEG; if(r.k==='voice'){voiceVol=vol; Audio.setVol('voice',vol);} else Audio.setVol(r.k,vol); }
        const filled=Math.round(vol*SEG);
        for(let s=0;s<SEG;s++){
          const bx=sx0+s*segW, on=s<filled;
          if(on){ ctx.save(); ctx.shadowColor='#ffb347'; ctx.shadowBlur=7;
            const sg=ctx.createLinearGradient(0,cy-7,0,cy+7); sg.addColorStop(0,'#ffd36b'); sg.addColorStop(1,'#ff8a1e');
            ctx.fillStyle=sg; roundRectFill(bx+1,cy-7,segW-2,14,2); ctx.restore();
            ctx.strokeStyle='#3a2a10'; ctx.lineWidth=1; ctx.strokeRect(bx+1,cy-7,segW-2,14);
          } else { ctx.fillStyle='rgba(255,255,255,0.07)'; roundRectFill(bx+1,cy-7,segW-2,14,2);
            ctx.strokeStyle='rgba(255,179,71,0.18)'; ctx.lineWidth=1; ctx.strokeRect(bx+1,cy-7,segW-2,14); }
        }
        ctx.fillStyle='#ffd36b'; ctx.font='bold 9px "BOFmil", monospace'; ctx.textAlign='left'; ctx.fillText(Math.round(vol*100)+'%',sx1+8,cy);
      }
      else if(r.t==='ctrl'){ ctx.fillStyle=isSel?menuSelWhite():'#cfd6e0'; ctx.font='bold 11px "BOFmil", monospace'; ctx.textAlign='left'; ctx.textBaseline='middle'; ctx.fillText(r.label,wx+16,cy);
        /* YELLOW on options (drop 0801bk), per Mike. NOTE: gamecode.js also has a
           drawOptions, but B_OPTIONS REPLACES it wholesale — editing the gamecode
           copy changes nothing that ships. This is the live one. */
        /* CURSOR INBOARD (drop 0801bp). Mike: "make the cursor actually visible
           in our options thing."

           menuSelMark draws its arrows at cx +/- (halfW + 16). With halfW =
           ww/2-10 that placed them at wx-26 and wx+ww+26 - OUTSIDE the window on
           both sides. All that showed were the slivers landing on the frame.
           Pulled well inside the row so both arrows sit on the panel. */
        if(isSel && typeof menuSelMark==='function') menuSelMark(wx+ww/2, cy, ww/2-46, '#ffd24a');
        const bx=wx+ww-124, bw=104, bh=22, active=(rebindAction===r.act);
        const kg=ctx.createLinearGradient(0,cy-bh/2,0,cy+bh/2);
        if(active){ kg.addColorStop(0,'#ffb347'); kg.addColorStop(1,'#c96f14'); } else { kg.addColorStop(0,'#3a4150'); kg.addColorStop(1,'#20242e'); }
        ctx.fillStyle=kg; roundRectFill(bx,cy-bh/2,bw,bh,5);
        ctx.strokeStyle=active?'#ffe27a':(isSel?'#ffb347':'#57607a'); ctx.lineWidth=1.5; ctx.strokeRect(bx,cy-bh/2,bw,bh);
        ctx.fillStyle='rgba(255,255,255,0.10)'; ctx.fillRect(bx+2,cy-bh/2+2,bw-4,3);
        ctx.fillStyle=active?'#1a0f02':'#e8ecf4'; ctx.font='bold 11px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText(active?'PRESS KEY':keyName(keybind[r.act][0]),bx+bw/2,cy);
        if(m.down && !drawOptions._md && m.x>bx && m.x<bx+bw && Math.abs(m.y-cy)<bh/2 && m.y>wy && m.y<wy+wh){ rebindAction=r.act; optSelIdx=selectable.findIndex(o=>o.r===r); Audio.SFX.blip(); } }
    }
    y+=rh;
  }
  ctx.restore(); ctx.textBaseline='alphabetic';
  if(maxScroll>0){ const sbx=wx+ww-6, sbh=wh*wh/contentH, sby=wy+(wh-sbh)*(optScroll/maxScroll);
    ctx.fillStyle='rgba(255,255,255,0.08)'; roundRectFill(sbx,wy,4,wh,2);
    ctx.fillStyle='rgba(255,180,80,0.7)'; roundRectFill(sbx,sby,4,sbh,2);
    if(m.down && !drawOptions._md && m.x>sbx-8 && m.x<sbx+10 && m.y>wy && m.y<wy+wh) optSbDrag=true;
    if(optSbDrag && m.down){ optScroll=clamp((m.y-wy-sbh/2)/(wh-sbh)*maxScroll,0,maxScroll); } }
  if(rebindAction){ for(const k in Input.keys){ if(Input.tap(k)){
      /* REFUSE UNBINDABLE KEYS (drop 0724dl). This is the LIVE rebind handler — the gamecode copy
         is inside a replaced span and never reaches the build, which is why guarding that one did
         nothing. Binding an action to a bare modifier kills it permanently and SAVES that, which is
         how Mike ended up with a menu key on shift and no way to see it. */
      if(k!=='escape' && typeof KEY_UNBINDABLE!=='undefined' && KEY_UNBINDABLE.indexOf(String(k).toLowerCase())>=0){
        if(Audio.SFX.hit) Audio.SFX.hit();
        rebindAction=null; break;
      }
      if(k!=='escape'){
        const cur=keybind[rebindAction]||[];
        // pad_* buttons get APPENDED (keep kb defaults); a normal key REPLACES the primary kb key but keeps pad binds
        if(k.startsWith('pad_')){ if(cur.indexOf(k)<0) keybind[rebindAction]=cur.concat([k]); }
        else { const pads=cur.filter(x=>x.startsWith('pad_')); keybind[rebindAction]=[k].concat(pads); }
      }
      rebindAction=null; Audio.SFX.select(); break; } } }
  const _cDef={x:wx,y:VH-48,w:(ww-16)/2,h:30}, _aDef={x:wx+(ww-16)/2+16,y:VH-48,w:(ww-16)/2,h:30};
  const _cBtn=uiRect('options','btnCancel',_cDef), _aBtn=uiRect('options','btnApply',_aDef);
  const by=_cBtn.y, bh2=_cBtn.h, bw2=_cBtn.w, cbx=_cBtn.x, abx=_aBtn.x;
  const overC=(m.x>cbx&&m.x<cbx+bw2&&m.y>by&&m.y<by+bh2), overA=(m.x>abx&&m.x<abx+bw2&&m.y>by&&m.y<by+bh2);
  /* BUTTONS IN THE PANEL'S OWN LANGUAGE (drop 0801bp). Mike: "upgrade the cancel
     and apply buttons." They were a flat rounded rect with a 2px stroke - and the
     stroke was a squared-off strokeRect that did not follow the rounding, so the
     corners disagreed with the fill. Rebuilt to match bofPanel: brushed vertical
     gradient, rivet strip, corner brackets in the button's own colour, and a lit
     state that glows rather than flooding to a solid fill. */
  function btn(bx,label,col,hot){
    const r=6;
    ctx.save();
    const g=ctx.createLinearGradient(0,by,0,by+bh2);
    if(hot){ g.addColorStop(0,'rgba(58,66,82,0.98)'); g.addColorStop(0.5,'rgba(34,40,52,0.98)'); g.addColorStop(1,'rgba(46,52,66,0.98)'); }
    else   { g.addColorStop(0,'rgba(26,30,40,0.94)'); g.addColorStop(0.5,'rgba(14,17,24,0.94)'); g.addColorStop(1,'rgba(20,23,32,0.94)'); }
    ctx.fillStyle=g; roundRectFill(bx,by,bw2,bh2,r);
    ctx.fillStyle='rgba(255,255,255,0.10)'; ctx.fillRect(bx+8,by+5,bw2-16,1);
    ctx.fillStyle='rgba(0,0,0,0.35)';       ctx.fillRect(bx+8,by+bh2-6,bw2-16,1);
    ctx.strokeStyle='rgba(60,66,80,0.95)'; ctx.lineWidth=2;
    ctx.beginPath(); roundRect(bx,by,bw2,bh2,r); ctx.stroke();
    if(hot){ ctx.shadowColor=col; ctx.shadowBlur=12; }
    ctx.strokeStyle=col; ctx.lineWidth=3; const L=14;
    for(const c of [[bx,by,1,1],[bx+bw2,by,-1,1],[bx,by+bh2,1,-1],[bx+bw2,by+bh2,-1,-1]]){
      ctx.beginPath(); ctx.moveTo(c[0]+c[2]*L,c[1]); ctx.lineTo(c[0],c[1]); ctx.lineTo(c[0],c[1]+c[3]*L); ctx.stroke();
    }
    ctx.shadowBlur=0;
    ctx.font='bold 14px "BOFmil", monospace'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.lineWidth=3; ctx.strokeStyle='rgba(0,0,0,0.7)'; ctx.strokeText(label,bx+bw2/2,by+bh2/2);
    ctx.fillStyle=hot?'#ffffff':col; ctx.fillText(label,bx+bw2/2,by+bh2/2);
    ctx.restore(); ctx.textBaseline='alphabetic';
  }
  btn(cbx,'CANCEL','#e0563a',overC); btn(abx,'APPLY','#6ac04a',overA);
  if(m.down && !drawOptions._md){ if(overC){ optCancel(); return; } if(overA){ optApply(); return; } }
  drawOptions._md=m.down; if(!m.down){ optDrag=-1; optSbDrag=false; }
  if(Input.menuBack()&&!rebindAction){ optCancel(); }
}
function drawOptionsLegacy(dt){
  ctx.textAlign='center'; ctx.fillStyle='#ffd36b'; ctx.font='bold 18px "BOFmil", monospace'; ctx.fillText('OPTIONS',VW/2,90);
  const startY=130, gap=29, kinds=['master','music','sfx'];
  const vols=[Audio.getVol('master'),Audio.getVol('music'),Audio.getVol('sfx')];
  const N=3+OPT_CTRL.length+1;
  for(let i=0;i<3;i++){ const sel=i===menuIndex, y=startY+i*gap;
    ctx.textAlign='left'; ctx.fillStyle=sel?'#fff':'#cfd6e0'; ctx.font='bold 12px "BOFmil", monospace'; ctx.fillText((sel?'> ':'  ')+OPT_VOL[i],44,y);
    const bx=198,by=y-9,bw=130; px(bx,by,bw,10,'#101418'); px(bx,by,bw*vols[i],10,sel?'#ff5a3a':'#7fc01f'); ctx.strokeStyle='#4a4d52'; ctx.strokeRect(bx,by,bw,10); }
  for(let c=0;c<OPT_CTRL.length;c++){ const idx=3+c, sel=idx===menuIndex, y=startY+idx*gap, act=OPT_CTRL[c][0];
    ctx.textAlign='left'; ctx.fillStyle=sel?'#fff':'#cfd6e0'; ctx.font='bold 12px "BOFmil", monospace'; ctx.fillText((sel?'> ':'  ')+OPT_CTRL[c][1],44,y);
    ctx.fillStyle=(rebindAction===act)?'#ffd36b':(sel?'#8de23a':'#9aa0aa'); ctx.fillText((rebindAction===act)?'PRESS A KEY':keyName(keybind[act][0]),198,y); }
  const bIdx=N-1, bsel=bIdx===menuIndex, byy=startY+bIdx*gap;
  ctx.textAlign='left'; ctx.fillStyle=bsel?'#fff':'#cfd6e0'; ctx.font='bold 12px "BOFmil", monospace'; ctx.fillText((bsel?'> ':'  ')+'BACK',44,byy);
  if(rebindAction){ for(const k in Input.keys){ if(Input.tap(k)){ if(k!=='escape'){ keybind[rebindAction]=[k]; saveKeybind(); } rebindAction=null; Audio.SFX.select(); break; } } if(Input.tap('backspace')){ rebindAction=null; } return; }
  if(Input.tap('arrowdown')||Input.tap('s')){menuIndex=(menuIndex+1)%N;Audio.SFX.blip();}
  if(Input.tap('arrowup')||Input.tap('w')){menuIndex=(menuIndex+N-1)%N;Audio.SFX.blip();}
  if(menuIndex<3){ if(Input.tap('arrowleft')){ Audio.setVol(kinds[menuIndex],clamp(vols[menuIndex]-0.1,0,1)); } if(Input.tap('arrowright')){ Audio.setVol(kinds[menuIndex],clamp(vols[menuIndex]+0.1,0,1)); } }
  if(Input.tap('enter')||Input.tap('j')){ if(menuIndex>=3 && menuIndex<3+OPT_CTRL.length){ rebindAction=OPT_CTRL[menuIndex-3][0]; } else if(menuIndex===N-1){ setState(GS.TITLE); menuIndex=2; } }
  if(Input.tap('backspace')){ setState(GS.TITLE); menuIndex=2; }
  if(backButton()){ setState(GS.TITLE); menuIndex=2; Audio.SFX.select(); }
}`;

// [B_STAGEEND] replaces drawStageClear with an arcade stat/rank sequence; also defines stageTextMixed (hoisted, used by drawPilot)
const B_STAGEEND = String.raw`/* STAGE CLEAR — arcade stats + rank */
function stageTextMixed(prim, fb, text, cx, cy, H, fbTint, alpha, sm){
  const sp=(sm==null?0.10:sm)*H; const items=[]; let total=0;
  for(const ch of String(text).toUpperCase()){
    if(ch===' '){ items.push(null); total+=H*0.42+sp; continue; }
    let art=prim, nm=(prim&&prim.font)?prim.font[ch]:null, tint=null;
    if(!nm || !prim.frames[nm]){ art=fb; nm=(fb&&fb.font)?fb.font[ch]:null; tint=fbTint; }
    if(!art || !nm || !art.frames[nm] || !art.img){ items.push(null); total+=H*0.42+sp; continue; }
    const f=art.frames[nm], w=f[2]*(H/f[3]); items.push([art,f,w,tint]); total+=w+sp;
  }
  let x=cx-(total-sp)/2;
  for(const it of items){ if(!it){ x+=H*0.42+sp; continue; } const a=it[0],f=it[1],w=it[2],tint=it[3];
    if(tint) drawFrameTinted(a.img,f,x,cy-H/2,w,H,tint,1.0,alpha); else drawFrameTinted(a.img,f,x,cy-H/2,w,H,null,null,alpha);
    x+=w+sp; }
}
function fmtTime(s){ s=Math.max(0,Math.round(s)); const m=Math.floor(s/60), ss=s%60; return m+':'+String(ss).padStart(2,'0'); }
function computeStageResults(){
  const s=stageStats, time=stageTimer;
  const alive=Math.max(0, s.spawned - s.kills);
  drawStageClear._res={ lines:[
    ['KILLS', s.kills+' / '+s.spawned, s.kills],
    ['ENEMIES LEFT ALIVE', String(alive), alive],
    ['DAMAGE DEALT', String(s.dmgDealt), s.dmgDealt],
    ['DAMAGE TAKEN', String(s.dmgTaken), s.dmgTaken],
    ['MISSILES USED', String(s.missiles), s.missiles],
    ['TIMES DIED', String(s.deaths), s.deaths],
    ['CLEAR TIME', fmtTime(time), -1]
  ]};
}
const RANKCOL={S:'#ffd24a',A:'#8de23a',B:'#5ab0ff',C:'#cfd6e0',D:'#c98a4a',F:'#e23a3a'};
/* Panel-relative coordinates (drop 0801ad). The stat rows were positioned against raw VW/VH, so
   they only lined up if the frame happened to fill the screen exactly. These map a 0..1 position
   inside the FITTED panel rect, so the content tracks the frame at any window size. */
function _SX(f){ const r=drawStageClear._rect; return r ? r[0]+r[2]*f : VW*f; }
function _SY(f){ const r=drawStageClear._rect; return r ? r[1]+r[3]*f : VH*f; }
function drawStageClear(dt){
  const t=stateT;
  if(!drawStageClear._init){ drawStageClear._init=true; computeStageResults();
    Audio.stopMusic(); Audio.startMusic('password'); if(Audio.SFX.stageClear)Audio.SFX.stageClear(); }
  /* THE AUTHORED COMPLETE CARD (drop 0801ax), under the stats block. Typed on after the numbers
     have settled so it reads as a closing beat rather than competing with the score. */
  if(typeof arcStageCard==='function' && typeof arcDraw==='function'){
    const _cc=arcStageCard(run.stage,'complete');
    if(_cc) arcDraw(_cc, VW/2, VH*0.88, 11, clamp((stateT-1.2)/1.6,0,1), '#8de23a');
  }
  const t2=ASSETS.stageArt&&ASSETS.stageArt['2'];
  const theme=['#8de23a','#ff5a2a','#6fd0ff','#d8c068','#d07a3a'][clamp(run.stage-1,0,4)];
  const TITLE0=0.55, PANEL=1.0, REVEAL=1.5, GAP=0.4, NL=7, DONE=REVEAL+NL*GAP+0.5;
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillStyle='#04050a'; ctx.fillRect(0,0,VW,VH);
  // subtle stage-tinted glow backdrop
  const rg=ctx.createRadialGradient(VW/2,VH*0.4,10,VW/2,VH*0.4,VW*0.9);
  rg.addColorStop(0,rgba(hx(theme),0.16)); rg.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=rg; ctx.fillRect(0,0,VW,VH);
  /* STAGE-CLEAR WINDOW (drop 0724bv). The authored 640x480 stats window, drawn over the backdrop
     and under the results text, with the animated COMBAT STATS header above it. Authored at
     640x480 and scaled to the viewport, so nothing has to be repositioned per resolution. */
  /* THE STAT SCREEN FRAME (drop 0801ad). Mike: "the end stat screen, nothing fits. use the
     Statscreen graphic in assets/ui, that'll be easier for you."

     nui_win is 640x480 — a 4:3 window being stretched onto a 480x1024 portrait canvas, which is
     why nothing lined up: every row was computed against a frame whose proportions did not match
     the screen it was drawn on. assets/ui/statscreen.png is 1496x980 and is the authored panel
     for this screen.

     It is fitted by ASPECT rather than stretched to the viewport, and the rows are laid out
     INSIDE the fitted rect instead of against raw VW/VH — so the text sits in the panel's own
     content area at any window size. */
  if(typeof XART!=='undefined' && XART.rdy('statscreen')){
    const im=XART.get('statscreen');
    const sc=Math.min(VW/im.naturalWidth, (VH*0.86)/im.naturalHeight);
    const pw=im.naturalWidth*sc, ph=im.naturalHeight*sc;
    const px0=VW/2-pw/2, py0=VH*0.07;
    ctx.drawImage(im, px0, py0, pw, ph);
    drawStageClear._rect=[px0,py0,pw,ph];
  } else if(typeof XART!=='undefined' && XART.rdy('nui_win')){
    ctx.save(); ctx.globalAlpha=clamp((t-0.15)/0.45,0,1);
    ctx.drawImage(XART.get('nui_win'), 0, 0, VW, VH);
    const hk='nui_hdr_'+(Math.floor(t*6)%4);
    if(XART.rdy(hk)){
      const hi=XART.get(hk), hw=VW*0.46, hh=hw*(hi.naturalHeight/hi.naturalWidth);
      ctx.drawImage(hi, VW/2-hw/2, VH*0.085, hw, hh);
    }
    ctx.restore();
  }
  // title flies in
  const p=clamp(t/TITLE0,0,1), c1=1.70158, c3=c1+1, e=1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2);
  const cx=lerp(-VW*0.7, VW/2, e);
  const _sf=(typeof curFontArt==='function')?curFontArt():t2;
  if(_sf) stageText(_sf,'STAGE '+run.stage+' CLEAR',cx,44,22,null,1.0,1,0.06); else if(t2) stageText(t2,'STAGE '+run.stage+' CLEAR',cx,44,22,null,1.0,1,0.06);
  if(t>=PANEL){
    const res=drawStageClear._res;
    const P=PILOTS.find(p=>p.key===(_pilotKey&&_pilotKey()));
    const pk=P?P.key:'axel';
    // avatar + name pop in, Starfox-64 style
    const ap=clamp((t-PANEL)/0.3,0,1), asc=0.6+ap*0.4;
    /* THE AVATAR WAS FALLING BACK TO THE OLD BAKED CARD (drop 0801u). face_<pilot> does not
       exist — there are no face_ keys in the manifest at all — so this always fell through to
       card_<pilot>, which is the pre-CF_PilotCardSystem art with a name, callsign, bio and stat
       values painted into it. Shrunk to a 68px avatar that is an unreadable smear of stale text.

       port_<pilot>_victory is the right asset: an actual portrait, and the victory pose is the
       correct expression for a stage-clear screen. Falls back through idle, then the new card
       shell, and only then the old card. */
    const avKey=(function(){
      for(const c of ['port_'+pk+'_victory','port_'+pk+'_smile','port_'+pk+'_idle','pcard_'+pk,'card_'+pk]){
        if(typeof XART!=='undefined' && XART.rdy(c)) return c;
      }
      return 'card_'+pk;
    })();
    if(typeof XART!=='undefined' && XART.rdy(avKey)){
      /* LAYOUT (drop 0724ca). The portrait sat at y=96 and the COMBAT STATS header at VH*0.085
         (~44) with its own height on top — they overlapped, and the pilot name landed on the
         header too. Portrait moved below the header band and shrunk so the seven stat rows and
         the password all fit inside the window without running off the bottom. */
      const im=XART.get(avKey), ah=68, aw=ah*(im.naturalWidth/im.naturalHeight);
      ctx.save(); ctx.globalAlpha=ap; ctx.translate(_SX(0.20), _SY(0.125)); ctx.scale(asc,asc);
      ctx.strokeStyle=theme; ctx.lineWidth=2; ctx.strokeRect(-aw/2-3,-ah/2-3,aw+6,ah+6);
      ctx.drawImage(im,-aw/2,-ah/2,aw,ah); ctx.restore();
    }
    ctx.save(); ctx.globalAlpha=ap; ctx.textAlign='left'; ctx.fillStyle='#eaf2ff'; ctx.font='16px "BOFmil", monospace';
    ctx.fillText((P?P.name:'PILOT'), _SX(0.38), _SY(0.117));
    ctx.fillStyle='#cfd6e0'; ctx.font='11px "BOFmil", monospace'; ctx.fillText((P?P.role:''), _SX(0.38), _SY(0.133));
    ctx.restore();
    // stat bars, one at a time, plain default font
    for(let i=0;i<res.lines.length;i++){
      const rt=REVEAL+i*GAP; if(t<rt) continue;
      /* rows start below the portrait block and use a tighter pitch: 7 rows at 38px ran to
         y=368 plus a bar under each, which pushed the last rows and the password off the panel. */
      const a=clamp((t-rt)/0.2,0,1), y=186+i*31;
      if(!drawStageClear['_l'+i]){ drawStageClear['_l'+i]=true; if(Audio.SFX.statsBar)Audio.SFX.statsBar(); else if(Audio.SFX.statTick)Audio.SFX.statTick(); }
      ctx.save(); ctx.globalAlpha=a;
      // stat LABEL — dialogue font (BOFmil), consistent color (no per-stage recolor)
      const _lbl=res.lines[i][0];
        ctx.textAlign='left'; ctx.fillStyle='#eaf2ff'; ctx.font='12px "BOFmil", monospace'; ctx.fillText(_lbl, 46, y);
      const target=res.lines[i][2];
      let val=res.lines[i][1];
      if(target>=0){
        const cp=clamp((t-rt)/0.4,0,1), cur=Math.round(target*cp);
        val = (res.lines[i][0]==='KILLS') ? (cur+' / '+stageStats.spawned) : String(cur);
        if(cp<1){ const fr=Math.floor(t*32); if(drawStageClear['_c'+i]!==fr){ drawStageClear['_c'+i]=fr; if(Audio.SFX.statCount)Audio.SFX.statCount(); } }
        // fill bar — framed art. Use 9-slice for the frame so the metal end-caps keep their
        // proportions instead of being smeared flat, and draw a bit taller so it reads.
        /* INSIDE THE WINDOW. The bars ran 20px from each screen edge, which is OUTSIDE the authored
         640x480 panel — they crossed its frame on both sides. Inset to the panel's own margin. */
      const barX=46, barH=11, barY=y+5, barW=VW-92;
        const _fillRatio=clamp((target>0?cp:1),0,1);
        const _barCols=['bar_red','bar_blue','bar_amber','bar_purple','bar_green','bar_gray'];
        // v2.0 Stats UI: animated stat fills (firepower/speed/shield/armor/bomb/missiles) + new frame.
        const _v2stats=['nsb_firepower','nsb_speed','nsb_shield','nsb_armor','nsb_bomb','nsb_missiles'];
        const _v2k=_v2stats[i%_v2stats.length]+'_'+(((t*9)|0)%8);
        // Mike 0719: ONE bar per category. The nsb_* categorized fills (firepower/speed/...) are
        // reserved for a future pilot-stats window where those categories exist; the stage-clear
        // rows keep the approved bar_frame + single color fill per row.
        const _useV2=false;
        if(_useV2){
          // no-stretch path: dark track, then tiled fill + capped/tiled frame at uniform scale
          ctx.fillStyle='rgba(6,8,12,0.85)'; ctx.fillRect(barX+3,barY+3,barW-6,barH-6);
          drawBarArtNS('nsb_frame', _v2k, barX, barY, barW, barH, _fillRatio);
        } else {
        const _fk=_barCols[i%_barCols.length];
        const _frameKey='bar_frame';
        if(typeof XART!=='undefined' && XART.rdy(_frameKey) && XART.rdy(_fk)){
          const fim=XART.get(_fk), frim=XART.get(_frameKey);
          const inset=4;   // keep the colored fill inside the frame border
          const fx=barX+inset, fyy=barY+inset, fw=barW-inset*2, fh=barH-inset*2;
          // dark track behind everything (shows in the un-filled portion)
          ctx.fillStyle='rgba(6,8,12,0.85)'; ctx.fillRect(fx,fyy,fw,fh);
          // colored fill (its own aspect isn't critical — it's a smooth gradient), clipped to ratio
          if(_fillRatio>0){ ctx.save(); ctx.beginPath(); ctx.rect(fx,fyy,fw*_fillRatio,fh); ctx.clip();
            ctx.drawImage(fim, fx,fyy, fw, fh); ctx.restore(); }
          // 9-slice the frame horizontally: left cap + right cap at natural width, middle stretched
          const sw=frim.naturalWidth, sh=frim.naturalHeight;
          const capS=Math.min(Math.floor(sw*0.16), Math.floor(sh*0.9));  // source cap width
          const capD=Math.round(barH*(capS/sh));                          // dest cap width (aspect-preserved)
          // left cap
          ctx.drawImage(frim, 0,0, capS,sh, barX,barY, capD,barH);
          // right cap
          ctx.drawImage(frim, sw-capS,0, capS,sh, barX+barW-capD,barY, capD,barH);
          // middle (stretched)
          ctx.drawImage(frim, capS,0, sw-capS*2,sh, barX+capD,barY, barW-capD*2,barH);
        } else {
          ctx.fillStyle='rgba(255,255,255,0.08)'; ctx.fillRect(20,y-6,VW-40,6);
          ctx.fillStyle=theme; ctx.fillRect(20,y-6,target>0?((VW-40)*_fillRatio):(VW-40),6);
        }
        }   // end v2-vs-legacy stat bar
      }
      const _vs=String(val);
      ctx.textAlign='right'; ctx.fillStyle='#eaf2ff'; ctx.font='14px "BOFmil", monospace'; ctx.fillText(_vs, VW-20, y);
      ctx.restore();
    }
    if(t>=DONE){
      const codes=['FURY','IRON','DAM5','STRM','ORBT'];
      if(run.stage<5){
        // "NEXT STAGE PASSWORD" label (dialogue font) + the CODE large in the NEXT stage's bitmap font
        ctx.fillStyle='#eaf2ff'; ctx.font='11px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText('NEXT STAGE PASSWORD', VW/2, VH-76);
        const nextStage=run.stage+1;
        const nf=(ASSETS.stageFont && ASSETS.stageFont[String(nextStage)]) || (ASSETS.stageArt && ASSETS.stageArt[String(nextStage)]);
        if(nf && typeof stageText==='function'){ stageText(nf, codes[run.stage], VW/2, VH-48, 30, null, null, 1, 0.10); }
        else { ctx.fillStyle='#ffe6a0'; ctx.font='bold 26px "BOFmil", monospace'; ctx.fillText(codes[run.stage], VW/2, VH-44); }
      }
      ctx.globalAlpha=0.5+0.5*Math.sin(t*5); ctx.fillStyle='#cfd6e0'; ctx.font='10px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText('PRESS FIRE / ENTER',VW/2,VH-20); ctx.globalAlpha=1;
    }
  }
  const fire=Input.tap('enter')||Input.mouse.down||keybind.fire.some(k=>Input.tap(k));
  if(t>0.5 && t<DONE && fire){ stateT=DONE; }
  else if(t>=DONE+0.4 && fire){ run.lives=clamp(run.lives,0,9); Audio.stopMusic();
    /* THE GAME HAS EIGHT STAGES (drop 0724cb). This ended the run at stage 5 — a leftover from when
       only five were built — so clearing 5, 6 or 7 rolled the credits instead of continuing. The
       gamecode copy already used STAGES.length correctly; this patched override did not, and the
       override is the one that runs. Driven off the table now, so adding a stage cannot desync it. */
    if(run.stage>=STAGES.length){ triggerVictory(); }
    else if(RACE_AFTER[run.stage] && rollRivalEncounter()){ startRivalSequence(); }   // 2>3, 4>5, 6>7
    else if(run.mode==='arcade'){
      // OUTBOUND: fly off the top of the map they just cleared, then follow the connector into
      // the next stage. beginStage is called by the cinematic when it hands off, not here.
      if(typeof outboundStart==='function'){ outboundStart(run.stage); setState(GS.OUTBOUND); }
      else beginStage(run.stage+1);
    }
    else {
      // CAMPAIGN: record this stage's rank, unlock the next, and play the unlock cinematic on return
      var _st=run.stage, _next=run.stage+1;
      if(typeof campaign!=='undefined'){
        // placeholder rank (real score->rank correlation is a to-do): S if flawless-ish, else A/B by score
        var _r = (run.lives>=DIFF.startLives ? 'S' : (run.score>50000 ? 'A' : 'B'));
        if(!campaign.rank[_st] || 'SAB'.indexOf(_r) < 'SAB'.indexOf(campaign.rank[_st])) campaign.rank[_st]=_r;
        var _wasLocked = _next>campaign.unlockedMax;
        openStageSelect(_next, _wasLocked ? {unlock:_next} : {});
      } else {
        openStageSelect(_next);
      }
    } }
}`;

// [B_HUD] new image HUD bar (SCORE/HI SCORE/LIVES/BOMBS/weapon) replacing drawHUDCustom; legacy kept as fallback
const B_HUD = String.raw`function drawHUDCustom(){
  // DROP 0720 — new HUD bar (SCORE/HI SCORE/LIVES/BOMBS/EQUIPMENT: SHIELD/SPEED/WEAP)
  if(typeof XART!=='undefined' && XART.rdy('nhud_bar')){
    const im=XART.get('nhud_bar'), HUDH=62;   // fill the reserved strip height
    ctx.drawImage(im,0,0,VW,HUDH);
    // dark-gray divider line separating HUD from the play field (Mike 0720)
    ctx.fillStyle='#2a2d33'; ctx.fillRect(0,HUDH,VW,2); ctx.fillStyle='#15171b'; ctx.fillRect(0,HUDH+2,VW,1);
    const vy=HUDH*0.60; ctx.textBaseline='middle';
    // value-window centers measured from divider positions on the real HUD art
    const CX_SCORE=0.128*VW, CX_HI=0.359*VW, CX_LIVES=0.522*VW, CX_BOMBS=0.64*VW;
    const CX_SHIELD=0.755*VW, CX_SPEED=0.845*VW-10, CX_WEAP=0.935*VW-20;   // SPEED -10, WEAP -20 to center in sub-windows
    ctx.save(); ctx.shadowColor='#ffcf4a'; ctx.shadowBlur=5; ctx.fillStyle='#ffe06b'; ctx.font='bold 12px "BOFmil", monospace'; ctx.textAlign='center';
    ctx.fillText(pad(run.score,7),CX_SCORE,vy); ctx.restore();
    ctx.fillStyle='#ffd36b'; ctx.font='bold 11px "BOFmil", monospace'; ctx.textAlign='center';
    ctx.fillText(pad(Math.max(run.score,(typeof highScore!=='undefined'?highScore:0)),7),CX_HI,vy);
    // pilot -> HUD icon index (life + missile sheets share order:
    // red pink blue green orange dk-yellow yellow dk-green purple)
    const _PICON={yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8};
    const _pi=_PICON[run.pilot]!=null?_PICON[run.pilot]:0;
    // LIVES — always single ship icon + 'xN' (no spilling)
    { const lk='nli_'+_pi; ctx.textBaseline='middle'; ctx.font='bold 12px "BOFmil", monospace';
      const label='x'+run.lives;
      if(typeof XART!=='undefined' && XART.rdy(lk)){ const li=XART.get(lk), ih=15, iw=ih*(li.naturalWidth/li.naturalHeight);
        const gw=iw+3+ctx.measureText(label).width; let lx=CX_LIVES-gw/2;
        ctx.drawImage(li,lx,vy-ih/2,iw,ih); ctx.fillStyle='#cfe6ff'; ctx.textAlign='left'; ctx.fillText(label,lx+iw+3,vy); }
      else { drawMiniShip(CX_LIVES-14,vy-5); ctx.fillStyle='#cfe6ff'; ctx.textAlign='left'; ctx.fillText(label,CX_LIVES-2,vy); } }
    // BOMBS — always single missile icon + 'xN'
    { const mk='nmi_'+_pi; ctx.textBaseline='middle'; ctx.font='bold 12px "BOFmil", monospace';
      const label='x'+run.bombs;
      if(typeof XART!=='undefined' && XART.rdy(mk)){ const mi=XART.get(mk), ih=15, iw=ih*(mi.naturalWidth/mi.naturalHeight);
        const gw=iw+3+ctx.measureText(label).width; let bx=CX_BOMBS-gw/2;
        ctx.drawImage(mi,bx,vy-ih/2,iw,ih); ctx.fillStyle='#ffd36b'; ctx.textAlign='left'; ctx.fillText(label,bx+iw+3,vy); }
      else { drawMiniMissile(CX_BOMBS-14,vy-5); ctx.fillStyle='#ffae6a'; ctx.textAlign='left'; ctx.fillText(label,CX_BOMBS-2,vy); } }
    // EQUIPMENT: shield / speed / weapon pips centered in their 3 sub-boxes
    // (Mike 0720: sub-box centers measured by dividing the EQUIPMENT window into thirds)
    // EQUIPMENT pips: count == level, colored by upgrade-tier color for that level
    // (Mike 0720: L1=1 orange, L2=2 blue, L3=3 green, L4=4 white, L5=5 red — matches WLVL_COL)
    const _LVLCOL=(typeof WLVL_COL!=='undefined')?WLVL_COL:{1:'#ff8a1e',2:'#3a8aff',3:'#5fe07a',4:'#f2f5ff',5:'#ff4a48'};
    const _pips=(cx,lv)=>{ const PW=2.6, GAP=1, tot=5*PW+4*GAP; let x=cx-tot/2; const col=_LVLCOL[clamp(lv,1,5)]||'#ff8a1e';
      for(let i=0;i<5;i++){ ctx.fillStyle=(i<lv)?col:'#1b2430'; ctx.fillRect(x,vy,PW,5); x+=PW+GAP; } };
    _pips(0.757*VW, clamp(run.shield||0,0,5));
    _pips(0.835*VW, clamp((run.speedLevel||0),0,5));
    const wt=({0:'mg',1:'spread',2:'missile',3:'laser',4:'firewall',5:'iceorb'})[run.weapon]||'mg', /* COLE'S TIERS WERE CLAMPED OUT OF THE HUD (drop 0801cb). Mike: "cole, I cant
     get lvl 6 lvl 7 or lvl 8 laser icons even when at lvl 5". The level was
     clamped to 5 before it ever reached the icon lookup, so tiers 6-8 could not
     display no matter how they were reached — including via the 1/2/3 keys. Cole
     goes to 8; everyone else still stops at 5, which is the same gate colePilot()
     already enforces on the weapon itself. */
    wlv=clamp(run.wlevel||1,1,(typeof colePilot==='function'&&colePilot())?8:5);
    _pips(0.913*VW, wlv);
    ctx.textBaseline='alphabetic'; ctx.textAlign='left';
    /* THE BOSS GAUGE LIVES IN THE OTHER HUD (drop 0801ej). Mike: "fix all
       miniboss and boss huds asap. theres no fills showing up."

       This branch draws the nhud_bar HUD and RETURNS. drawHUDCustomImg below is
       the only place the boss gauge is drawn - measured: calling it directly
       emits 3 nbb_ blits, calling drawHUD() emits none. nhud_bar is always
       decoded, so the boss and miniboss bars were unreachable every single run.

       The art was never the problem: 168 nbb_/nmb_ keys are registered, 8 fills
       per stage for both, and drawHealthBarV2 draws them correctly when called -
       green at 0.9, yellow at 0.5, red at 0.2. Nothing called it.

       Drawn here before the return, with a plain gauge as the fallback for the
       frames before the bar art decodes, so there is never simply nothing. */
    if(typeof bossActive!=='undefined' && bossActive && boss && !boss.dead
       && typeof drawHealthBarV2==='function'){
      const _r=clamp((boss.hp||0)/(boss.maxhp||1),0,1);
      const _bw=VW*0.72, _by=VH-58;
      ctx.save();
      ctx.fillStyle='rgba(5,7,10,0.85)';
      ctx.fillRect(VW/2-_bw/2+2, _by+2, _bw-4, 9);
      if(!drawHealthBarV2('boss', _r, VW/2, _by+6.5, _bw)){
        ctx.fillStyle='#3a0c0c'; ctx.fillRect(VW/2-_bw/2, _by, _bw, 13);
        ctx.fillStyle=_r>0.5?'#4fd66a':_r>0.25?'#e8c33a':'#e04b3a';
        ctx.fillRect(VW/2-_bw/2, _by, _bw*_r, 13);
      }
      ctx.fillStyle='#ffd0d0'; ctx.font='bold 8px "BOFmil", monospace'; ctx.textAlign='center';
      ctx.fillText(String(boss.name||'BOSS'), VW/2, _by-4);
      ctx.textAlign='left';
      ctx.restore();
    }
    return;
  }
  return drawHUDCustomImg();
}
function drawHUDCustomImg(){
  if(!(typeof XART!=='undefined' && XART.rdy('hud_bar'))) return drawHUDCustomLegacy();
  const im=XART.get('hud_bar'), HUDH=62;
  ctx.drawImage(im,0,0,VW,HUDH);
  ctx.strokeStyle='rgba(210,160,70,0.55)'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(0,HUDH-0.5); ctx.lineTo(VW,HUDH-0.5); ctx.stroke();
  ctx.strokeStyle='rgba(0,0,0,0.8)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(0,HUDH+1.5); ctx.lineTo(VW,HUDH+1.5); ctx.stroke();
  const cx=[0.138*VW,0.338*VW,0.526*VW,0.693*VW,0.872*VW], vy=HUDH*0.63;
  ctx.textBaseline='middle';
  ctx.save(); ctx.shadowColor='#ffcf4a'; ctx.shadowBlur=6; ctx.fillStyle='#ffe06b'; ctx.font='bold 15px "BOFmil", monospace'; ctx.textAlign='center';
  ctx.fillText(pad(run.score,7),cx[0],vy); ctx.restore();
  ctx.fillStyle='#ffd36b'; ctx.font='bold 13px "BOFmil", monospace'; ctx.textAlign='center';
  ctx.fillText(pad(Math.max(run.score,(typeof highScore!=='undefined'?highScore:0)),7),cx[1],vy);
  ctx.textAlign='center';
  if(run.lives<=4){ let lx=cx[2]-(run.lives-1)*7; for(let i=0;i<run.lives;i++){ drawMiniShip(lx,vy-1); lx+=14; } }
  else { ctx.fillStyle='#cfe6ff'; ctx.font='bold 16px "BOFmil", monospace'; ctx.fillText('x'+run.lives,cx[2],vy); }
  { // MISSILE AMMO count (fired with the bomb key) — number in the slot, small missile pips if few
    ctx.textAlign='center';
    if(run.bombs<=6){ let bx=cx[3]-(run.bombs-1)*8; for(let i=0;i<run.bombs;i++){ ctx.fillStyle='#15181d'; circle(bx,vy+1,3.7); ctx.fillStyle='#ffd36b'; circle(bx,vy-0.4,1.2); ctx.fillStyle='#ff9a3a'; ctx.fillRect(bx-0.8,vy-3.2,1.6,1.5); bx+=13; } }
    else { ctx.save(); ctx.shadowColor='#ffae6a'; ctx.shadowBlur=4; ctx.fillStyle='#ffae6a'; ctx.font='bold 16px "BOFmil", monospace'; ctx.fillText('x'+run.bombs,cx[3],vy); ctx.restore(); }
  }
  const wt=({0:'mg',1:'spread',2:'missile',3:'laser',4:'firewall',5:'iceorb'})[run.weapon]||'mg', wlv=clamp(run.wlevel||1,1,(typeof colePilot==='function'&&colePilot())?8:5);
  const wIcon=((typeof weaponIconKey==='function')?weaponIconKey(run.weapon,wlv):('pw_'+wt+'_'+wlv)), wglow=({0:'#ff5a5a',1:'#b06bff',2:'#6bd06b',3:'#7fe0ff',4:'#ff7a2a'})[run.weapon]||'#fff';
  if(ASSETS.has(wIcon)){ ctx.save(); ctx.shadowColor=wglow; ctx.shadowBlur=8; const dd=ASSETS.dims(wIcon), ss=Math.min(30/dd.w,24/dd.h); ASSETS.blit(wIcon,cx[4],HUDH*0.46,dd.w*ss,dd.h*ss); ctx.restore(); }
  else { ctx.fillStyle=wglow; ctx.font='bold 11px "BOFmil", monospace'; ctx.fillText('L'+wlv,cx[4],vy-2); }
  for(let i=0;i<5;i++){ const on=i<wlv; ctx.fillStyle=on?wglow:'#1b2430'; ctx.fillRect(cx[4]-11+i*5,HUDH-9,3.6,3.6); }
  ctx.textBaseline='alphabetic'; ctx.textAlign='left';
  let ix=VW-10;
  // shield/speed/missile now shown as EQUIPMENT pips in the HUD — no below-HUD icons
  if(boss && bossActive && !boss.dead){
    const by=HUDH+6, bw=VW-44, bxs=22, r=clamp(boss.hp/boss.maxhp,0,1);
    // v2.0 per-stage themed boss bar (frame + 8-frame animated fill), legacy gradient fallback
    const _bst=clamp((run&&run.stage)||1,1,8);
    /* KEY SCHEME FIX (drop 0724bv). This looked for 'nbb<N>_frame' / 'nbb<N>_fill_<f>', but the
       shipped pack registers as 'nbb_frame_<N>' / 'nbb_fill_<N>_<f>'. The keys never resolved, so
       the guard below always fell through to the legacy gradient bar — which is why the v2 art was
       in the build and never once appeared on screen. */
    const _bfk='nbb_frame_'+_bst, _bik='nbb_fill_'+_bst+'_'+(((performance.now()/110)|0)%8);
    const _bsk='nbb_seg_'+_bst;
    /* THE GUARD ASKED FOR TOO MUCH (drop 0801jw). Mike: "Boss bar - still doesnt
       fill in when a boss appears."

       It required the FRAME *and* the clock-selected FILL frame to be decoded in
       the same instant. All 8 fills are registered on all 8 stages - verified - but
       they decode asynchronously and _bik moves every 110ms. Miss that window and
       the whole thing fell through to the legacy gradient, which is the empty bar
       he is seeing.

       drawHealthBarV2 already copes with a missing fill: it scans the other seven
       frames and falls back to a flat colour if none has landed. So the frame alone
       is a sufficient gate, and the fill can arrive when it arrives. */
    if(typeof XART!=='undefined' && XART.rdy(_bfk)){
      const H2=13;
      ctx.fillStyle='rgba(5,7,10,0.85)'; ctx.fillRect(bxs+2,by+2,bw-4,H2-4);
      if(typeof drawHealthBarV2==='function') drawHealthBarV2('boss', r, VW/2, by+H2/2, bw);
      else drawBarArtNS(_bfk, _bik, bxs, by, bw, H2, r);
      ctx.fillStyle='#ffd0d0'; ctx.font='bold 8px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText((boss.name||'BOSS'),VW/2,by-4); ctx.textAlign='left';
    } else {
    ctx.fillStyle='#05070a'; ctx.fillRect(bxs-3,by-3,bw+6,13); ctx.fillStyle='#2a0808'; ctx.fillRect(bxs,by,bw,7);
    const gg=ctx.createLinearGradient(bxs,0,bxs+bw,0); gg.addColorStop(0,'#ff2020'); gg.addColorStop(0.7,'#ff6a2a'); gg.addColorStop(1,'#ffd24a');
    ctx.save(); ctx.shadowColor='#ff3b3b'; ctx.shadowBlur=7; ctx.fillStyle=gg; ctx.fillRect(bxs,by,bw*r,7); ctx.restore();
    ctx.fillStyle='rgba(0,0,0,0.4)'; for(let i=1;i<10;i++) ctx.fillRect(bxs+bw*i/10,by,1,7);
    ctx.fillStyle='#ffd0d0'; ctx.font='bold 8px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText((boss.name||'BOSS'),VW/2,by-4); ctx.textAlign='left';
    }
  }
}
function _miniShipG(g,x,y){ g.fillStyle='#d7dbe2'; g.fillRect(x+2,y,2,8); g.fillStyle='#c81f24';
  g.beginPath(); g.moveTo(x,y+6);g.lineTo(x+3,y+2);g.lineTo(x+3,y+6);g.fill();
  g.beginPath(); g.moveTo(x+6,y+6);g.lineTo(x+3,y+2);g.lineTo(x+3,y+6);g.fill();
  g.fillStyle='#e23a3a'; g.fillRect(x+2,y-1,2,2); }
function _circG(g,x,y,r){ g.beginPath(); g.arc(x,y,r,0,Math.PI*2); g.fill(); }
// DROP 0719g — no-stretch bar renderer (Mike: "don't stretch em").
// Uniform-scales art to the dest HEIGHT, then TILES horizontally: fill repeats across the clipped
// ratio width; frame keeps its end caps at scaled size with the middle band tiled (not smeared).
function drawBarArtNS(frameKey, fillKey, x, y, w, h, ratio){
  if(!(typeof XART!=='undefined' && XART.rdy(frameKey) && XART.rdy(fillKey))) return false;
  const frim=XART.get(frameKey), fim=XART.get(fillKey);
  const inset=Math.max(2, Math.round(h*0.14));
  // fill: ONE bar via 3-slice — end caps at uniform scale, only the smooth gradient middle
  // extends. No tiling (no repeated bars), no whole-image stretch.
  const ih=h-inset*2, fs2=ih/fim.naturalHeight;
  const fsw=fim.naturalWidth, fsh=fim.naturalHeight;
  const fcapS=Math.min(Math.floor(fsw*0.12), fsw>>1), fcapD=Math.max(1, Math.round(fcapS*fs2));
  const iw=w-inset*2, fillW=iw*clamp(ratio,0,1);
  if(fillW>1){
    ctx.save(); ctx.beginPath(); ctx.rect(x+inset, y+inset, fillW, ih); ctx.clip();
    ctx.drawImage(fim, 0,0, fcapS,fsh, x+inset, y+inset, fcapD, ih);                       // left cap
    ctx.drawImage(fim, fsw-fcapS,0, fcapS,fsh, x+inset+iw-fcapD, y+inset, fcapD, ih);      // right cap (at FULL width -> clipped by ratio)
    ctx.drawImage(fim, fcapS,0, fsw-fcapS*2,fsh, x+inset+fcapD, y+inset, iw-fcapD*2, ih);  // middle extends
    ctx.restore();
  }
  // frame: caps at uniform scale, middle tiled
  const sh=frim.naturalHeight, sw=frim.naturalWidth, sc=h/sh;
  const capS=Math.min(Math.floor(sw*0.16), sw>>1), capD=Math.max(1, Math.round(capS*sc));
  const midS=sw-capS*2, midD=Math.max(1, Math.round(midS*sc));
  ctx.drawImage(frim, 0,0, capS,sh, x, y, capD, h);
  ctx.drawImage(frim, sw-capS,0, capS,sh, x+w-capD, y, capD, h);
  ctx.save(); ctx.beginPath(); ctx.rect(x+capD, y, w-capD*2, h); ctx.clip();
  for(let tx=x+capD; tx < x+w-capD + midD; tx+=midD) ctx.drawImage(frim, capS,0, midS,sh, tx, y, midD, h);
  ctx.restore();
  return true;
}
function drawHUDStrip(g){
  // NEW HUD (nhud_bar) on the dedicated hud canvas — mirrors drawHUDCustom's corrected layout
  if(typeof XART!=='undefined' && XART.rdy('nhud_bar')){
    g.drawImage(XART.get('nhud_bar'),0,0,VW,HUDH);
    const vy=HUDH*0.60; g.textBaseline='middle';
    const CX_SCORE=0.128*VW, CX_HI=0.359*VW, CX_LIVES=0.522*VW, CX_BOMBS=0.64*VW;
    g.save(); g.shadowColor='#ffcf4a'; g.shadowBlur=5; g.fillStyle='#ffe06b'; g.font='bold 12px monospace'; g.textAlign='center';
    g.fillText(pad(run.score,7),CX_SCORE,vy); g.restore();
    g.fillStyle='#ffd36b'; g.font='bold 11px monospace'; g.textAlign='center';
    g.fillText(pad(Math.max(run.score,(typeof highScore!=='undefined'?highScore:0)),7),CX_HI,vy);
    const _PICON={yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8};
    const _pi=_PICON[run.pilot]!=null?_PICON[run.pilot]:0;
    // LIVES — single ship icon + xN
    { const lk='nli_'+_pi; g.textBaseline='middle'; g.font='bold 12px monospace'; const label='x'+run.lives;
      if(XART.rdy(lk)){ const li=XART.get(lk), ih=15, iw=ih*(li.naturalWidth/li.naturalHeight);
        const gw=iw+3+g.measureText(label).width; let lx=CX_LIVES-gw/2;
        g.drawImage(li,lx,vy-ih/2,iw,ih); g.fillStyle='#cfe6ff'; g.textAlign='left'; g.fillText(label,lx+iw+3,vy); }
      else { _miniShipG(g,CX_LIVES-14,vy-4); g.fillStyle='#cfe6ff'; g.textAlign='left'; g.fillText(label,CX_LIVES-2,vy); } }
    // BOMBS — single missile icon + xN
    { const mk='nmi_'+_pi; g.textBaseline='middle'; g.font='bold 12px monospace'; const label='x'+run.bombs;
      if(XART.rdy(mk)){ const mi=XART.get(mk), ih=15, iw=ih*(mi.naturalWidth/mi.naturalHeight);
        const gw=iw+3+g.measureText(label).width; let bx=CX_BOMBS-gw/2;
        g.drawImage(mi,bx,vy-ih/2,iw,ih); g.fillStyle='#ffd36b'; g.textAlign='left'; g.fillText(label,bx+iw+3,vy); }
      else { g.fillStyle='#ffae6a'; g.textAlign='center'; g.fillText(label,CX_BOMBS,vy); } }
    // EQUIPMENT pips: count==level, colored by tier (L1 orange..L5 red)
    const _LVLCOL=(typeof WLVL_COL!=='undefined')?WLVL_COL:{1:'#ff8a1e',2:'#3a8aff',3:'#5fe07a',4:'#f2f5ff',5:'#ff4a48'};
    const _pips=(cx,lv)=>{ const PW=2.6, GAP=1, tot=5*PW+4*GAP; let x=cx-tot/2; const col=_LVLCOL[clamp(lv,1,5)]||'#ff8a1e';
      for(let i=0;i<5;i++){ g.fillStyle=(i<lv)?col:'#1b2430'; g.fillRect(x,vy,PW,5); x+=PW+GAP; } };
    _pips(0.757*VW, clamp(run.shield||0,0,5));
    _pips(0.835*VW, clamp((run.speedLevel||0),0,5));
    _pips(0.913*VW, clamp(run.wlevel||1,1,5));
    g.textBaseline='alphabetic'; g.textAlign='left';
    return;
  }
  if(!(typeof XART!=='undefined' && XART.rdy('hud_bar'))){
    g.fillStyle='#0a0d12'; g.fillRect(0,0,VW,HUDH);
    g.fillStyle='#ffe06b'; g.font='bold 13px monospace'; g.textAlign='left'; g.textBaseline='middle';
    g.fillText('SCORE '+pad(run.score,7),8,HUDH*0.38);
    g.fillText('LIVES '+run.lives+'    BOMBS '+run.bombs,8,HUDH*0.74); g.textBaseline='alphabetic'; return;
  }
  g.drawImage(XART.get('hud_bar'),0,0,VW,HUDH);
  const cx=[0.138*VW,0.338*VW,0.526*VW,0.693*VW,0.872*VW], vy=HUDH*0.63;
  g.textBaseline='middle';
  g.save(); g.shadowColor='#ffcf4a'; g.shadowBlur=6; g.fillStyle='#ffe06b'; g.font='bold 15px monospace'; g.textAlign='center';
  g.fillText(pad(run.score,7),cx[0],vy); g.restore();
  g.fillStyle='#ffd36b'; g.font='bold 13px monospace'; g.textAlign='center';
  g.fillText(pad(Math.max(run.score,(typeof highScore!=='undefined'?highScore:0)),7),cx[1],vy);
  g.textAlign='center';
  if(run.lives<=4){ let lx=cx[2]-(run.lives-1)*7; for(let i=0;i<run.lives;i++){ _miniShipG(g,lx,vy-1); lx+=14; } }
  else { g.fillStyle='#cfe6ff'; g.font='bold 16px monospace'; g.fillText('x'+run.lives,cx[2],vy); }
  if(run.bombs<=4){ let bx=cx[3]-(run.bombs-1)*8; for(let i=0;i<run.bombs;i++){ g.fillStyle='#15181d'; _circG(g,bx,vy+1,3.7); g.fillStyle='#ffd36b'; _circG(g,bx,vy-0.4,1.2); g.fillStyle='#ff9a3a'; g.fillRect(bx-0.8,vy-3.2,1.6,1.5); bx+=16; } }
  else { g.fillStyle='#ffae6a'; g.font='bold 16px monospace'; g.fillText('x'+run.bombs,cx[3],vy); }
  const wt=({0:'mg',1:'spread',2:'missile',3:'laser',4:'firewall',5:'iceorb'})[run.weapon]||'mg', wlv=clamp(run.wlevel||1,1,(typeof colePilot==='function'&&colePilot())?8:5);
  const wIcon=((typeof weaponIconKey==='function')?weaponIconKey(run.weapon,wlv):('pw_'+wt+'_'+wlv)), wglow=({0:'#ff5a5a',1:'#b06bff',2:'#6bd06b',3:'#7fe0ff',4:'#ff7a2a'})[run.weapon]||'#fff';
  if(ASSETS.has(wIcon)){ const f=ASSETS.frames[wIcon], ss=Math.min(30/f[2],24/f[3]), dw=f[2]*ss, dh=f[3]*ss;
    g.save(); g.shadowColor=wglow; g.shadowBlur=8; g.drawImage(ASSETS.img,f[0],f[1],f[2],f[3],Math.round(cx[4]-dw/2),Math.round(HUDH*0.46-dh/2),dw,dh); g.restore(); }
  else { g.fillStyle=wglow; g.font='bold 11px monospace'; g.fillText('L'+wlv,cx[4],vy-2); }
  for(let i=0;i<5;i++){ const on=i<wlv; g.fillStyle=on?wglow:'#1b2430'; g.fillRect(cx[4]-11+i*5,HUDH-9,3.6,3.6); }
  g.textBaseline='alphabetic'; g.textAlign='left';
}
function drawHUDOverlay(){
  let ix=VW-10;
  // shield/speed shown as HUD EQUIPMENT pips now — no overlay icons
  if(boss && bossActive && !boss.dead){
    const by=6, bw=VW-44, bxs=22, r=clamp(boss.hp/boss.maxhp,0,1);
    ctx.fillStyle='#05070a'; ctx.fillRect(bxs-3,by-3,bw+6,13); ctx.fillStyle='#2a0808'; ctx.fillRect(bxs,by,bw,7);
    const gg=ctx.createLinearGradient(bxs,0,bxs+bw,0); gg.addColorStop(0,'#ff2020'); gg.addColorStop(0.7,'#ff6a2a'); gg.addColorStop(1,'#ffd24a');
    ctx.save(); ctx.shadowColor='#ff3b3b'; ctx.shadowBlur=7; ctx.fillStyle=gg; ctx.fillRect(bxs,by,bw*r,7); ctx.restore();
    ctx.fillStyle='rgba(0,0,0,0.4)'; for(let i=1;i<10;i++) ctx.fillRect(bxs+bw*i/10,by,1,7);
    ctx.fillStyle='#ffd0d0'; ctx.font='bold 8px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText((boss.name||'BOSS'),VW/2,by-4); ctx.textAlign='left';
  }
}

function drawHUDCustomLegacy(){
  const H=46;
  const g=ctx.createLinearGradient(0,0,0,H); g.addColorStop(0,'#2c333f'); g.addColorStop(0.5,'#171c24'); g.addColorStop(1,'#080a0e');
  ctx.fillStyle=g; ctx.fillRect(0,0,VW,H);
  const sw=(performance.now()/2600)%1; const sg=ctx.createLinearGradient(sw*VW-70,0,sw*VW+70,0);
  sg.addColorStop(0,'rgba(255,255,255,0)'); sg.addColorStop(0.5,'rgba(130,190,255,0.07)'); sg.addColorStop(1,'rgba(255,255,255,0)');
  ctx.fillStyle=sg; ctx.fillRect(0,0,VW,H);
  ctx.fillStyle='#4a5468'; ctx.fillRect(0,0,VW,1); ctx.fillStyle='#3a4252'; ctx.fillRect(0,H-3,VW,1); ctx.fillStyle='#000'; ctx.fillRect(0,H,VW,3);
  ctx.fillStyle='#555f70'; for(let x=8;x<VW;x+=24){ circle(x,5,1.5); circle(x,H-6,1.5); }

  // SCORE panel
  hudPanel(6,5,176,36);
  ctx.textAlign='left'; ctx.fillStyle='#7fd0ff'; ctx.font='7px "BOFmil", monospace'; ctx.fillText('SCORE',14,15);
  ctx.save(); ctx.shadowColor='#ffcf4a'; ctx.shadowBlur=9; ctx.fillStyle='#ffe06b'; ctx.font='bold 18px "BOFmil", monospace'; ctx.fillText(String(run.score).padStart(7,'0'),14,34); ctx.restore();
  ctx.fillStyle='#6f7682'; ctx.font='7px "BOFmil", monospace'; ctx.textAlign='right'; ctx.fillText('HI '+String(Math.max(run.score,(typeof highScore!=='undefined'?highScore:0))).padStart(7,'0'),176,15);

  // CREW + BOMB
  ctx.textAlign='left'; ctx.fillStyle='#7fd0ff'; ctx.font='7px "BOFmil", monospace'; ctx.fillText('CREW',190,15);
  let lx=222; for(let i=0;i<Math.min(run.lives,6);i++){ drawMiniShip(lx,12); lx+=13; }
  if(run.lives>6){ ctx.fillStyle='#cfd6e0'; ctx.font='bold 9px "BOFmil", monospace'; ctx.fillText('x'+run.lives,lx,15); }
  ctx.fillStyle='#ffae6a'; ctx.font='7px "BOFmil", monospace'; ctx.fillText('MISSILE',190,38);
  let bx=224; for(let i=0;i<Math.min(run.bombs,6);i++){ ctx.fillStyle='#15181d'; circle(bx,36,3.2); ctx.fillStyle='#363d47'; circle(bx-1,35,1.2); ctx.fillStyle='#0a0c0f'; ctx.fillRect(bx-1,32.6,2,1.5); ctx.fillStyle='#ffd36b'; circle(bx,31.6,0.9); bx+=10; }

  // WEAPON module
  const wt=({0:'mg',1:'spread',2:'missile',3:'laser',4:'firewall',5:'iceorb'})[run.weapon]||'mg';
  const wname=({0:'MACHINE GUN',1:'SPREAD FIRE',2:'MISSILE',3:'LASER',4:'FLAMETHROWER',5:'ICE ORB'})[run.weapon]||'';
  const wglow=({0:'#ff5a5a',1:'#b06bff',2:'#6bd06b',3:'#7fe0ff',4:'#ff7a2a'})[run.weapon]||'#fff';
  const wlv=clamp(run.wlevel||1,1,(typeof colePilot==='function'&&colePilot())?8:5);
  hudPanel(VW-152,5,146,36);
  const mx=VW-130, my=23;
  ctx.fillStyle='#0c0f15'; hudSlot(mx-16,8,32,30,5);
  const wIcon=((typeof weaponIconKey==='function')?weaponIconKey(run.weapon,wlv):('pw_'+wt+'_'+wlv));
  if(ASSETS.has(wIcon)){ ctx.save(); ctx.shadowColor=wglow; ctx.shadowBlur=9; const dd=ASSETS.dims(wIcon), ss=28/Math.max(dd.w,dd.h); ASSETS.blit(wIcon,mx,my,dd.w*ss,dd.h*ss); ctx.restore(); }
  ctx.textAlign='left'; ctx.fillStyle='#cfe6ff'; ctx.font='bold 8px "BOFmil", monospace'; ctx.fillText(wname,mx+22,16);
  ctx.fillStyle=wglow; ctx.font='bold 8px "BOFmil", monospace'; ctx.fillText('LV '+(run.wlevel||1),mx+22,27);
  for(let i=0;i<6;i++){ const on=i<(run.wlevel||1); ctx.fillStyle=on?(i>=4?'#ffe06b':i>=2?'#8de23a':'#3fa9ff'):'#1b2430';
    if(on){ ctx.save(); ctx.shadowColor=ctx.fillStyle; ctx.shadowBlur=4; ctx.fillRect(mx+22+i*9,32,7,5); ctx.restore(); } else ctx.fillRect(mx+22+i*9,32,7,5); }

  // active powerups shown as EQUIPMENT pips now — no top-right icons

  // boss bar
  if(boss && bossActive && !boss.dead){
    const by=H+6, bw=VW-44, bxs=22, r=clamp(boss.hp/boss.maxhp,0,1);
    ctx.fillStyle='#05070a'; ctx.fillRect(bxs-3,by-3,bw+6,13); ctx.fillStyle='#2a0808'; ctx.fillRect(bxs,by,bw,7);
    const gg=ctx.createLinearGradient(bxs,0,bxs+bw,0); gg.addColorStop(0,'#ff2020'); gg.addColorStop(0.7,'#ff6a2a'); gg.addColorStop(1,'#ffd24a');
    ctx.save(); ctx.shadowColor='#ff3b3b'; ctx.shadowBlur=7; ctx.fillStyle=gg; ctx.fillRect(bxs,by,bw*r,7); ctx.restore();
    ctx.fillStyle='rgba(0,0,0,0.4)'; for(let i=1;i<10;i++) ctx.fillRect(bxs+bw*i/10,by,1,7);
    ctx.strokeStyle='#6a1a1a'; ctx.lineWidth=1; ctx.strokeRect(bxs,by,bw,7);
    ctx.fillStyle='#ffd0d0'; ctx.font='bold 8px "BOFmil", monospace'; ctx.textAlign='center'; ctx.fillText((boss.name||'BOSS'),VW/2,by-4);
  }
  ctx.textAlign='left'; ctx.textBaseline='alphabetic';
}`;
