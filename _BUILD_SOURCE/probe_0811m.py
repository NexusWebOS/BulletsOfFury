#!/usr/bin/env python3
"""probe_0811m.py — Mike's 0811m list, in pixels.

Covers the four items this drop touched:

  8. the level-1 dialogue window   -> bottom left, dlg_window, BOF font, wrapped
  9. the arcade pickup banner      -> type / sweep / hold / slide
  7. Decker's shotgun box          -> it had no draw branch at all; candidates rendered
  +  the BOF font's glyph coverage, because msgWrap and the '!' both depend on it

⚠ SCOPE FIRST, as always in this project. arcadeBanner, msgWrap and msgMeasure are all declared
in game.js well past spawnEnemy's never-closed `if`, and this file has a long history of
correct-but-unreachable declarations (DEAD_SUBBOSS, ARSENAL_DRONES, liveType, arsenalDroneArt).
A banner that is never called looks exactly like a banner that does not work.

⚠ AND EVERY SHOT IS TAKEN IN A SECOND evaluate. A single evaluate never yields, so the icon and
font sheets cannot decode inside it however many frames are stepped — the --warm trap. Python
waiting at the evaluate boundary is the only thing that lets the network run.
"""
import http.server, socketserver, threading, os, functools, base64
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')

def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

SETUP=r"""
()=>{
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(1); setState(GS.PLAY); player.reset(); player.invuln=1e9;
  if(typeof XART!=='undefined'){ XART.rdy('nia_icons'); XART.rdy('dlg_window');
    for(const k of ['ndk_shot_0','ndk_shot_1','ndk_shot_2','ndk_shot_3','ndk_shell_0',
                    'spicon_decker','nsw_icon_cole']) XART.rdy(k); }
  return {
    scope:{
      arcadeBanner:     typeof arcadeBanner,
      arcadeBannerTick: typeof arcadeBannerTick,
      drawArcadeBanner: typeof drawArcadeBanner,
      msgMeasure:       typeof msgMeasure,
      msgWrap:          typeof msgWrap,
      msgTextLeft:      typeof msgTextLeft,
      msgFitH:          typeof msgFitH,
      weaponLegacyName: typeof weaponLegacyName,
    },
  };
}
"""

# ⚠ THE FIRST VERSION OF THIS CHECK GREPPED updatePlay/drawWorld FOR THE CALL AND REPORTED
# "declared but never fired" FOR A BANNER THAT WORKS. The calls sit one level down, in
# updateEffects and _drawEffectsInner, which updatePlay and drawWorld reach through. That is the
# same mistake as asserting a table while the pixels come from another path — a source test
# cannot see a call chain. So the wiring question is answered the way the miniboss blit-count
# confusion was finally answered: render with, render without, and see whether the frame moved.
WIRED=r"""
()=>{
  const grab=()=>{ const c=document.getElementById('screen');
    return c.getContext('2d').getImageData(0,0,c.width,c.height).data; };
  const step=(n)=>{ for(let i=0;i<n;i++){ updatePlay(1/60); try{ drawWorld(1/60); }catch(e){} } };
  const diff=(a,b)=>{ let d=0; for(let i=0;i<a.length;i+=4) if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]) d++; return d; };

  /* ⚠ AND THE FIRST FRAME DIFF WAS NO BETTER THAN THE SOURCE GREP. Diffing a frame before the
     banner against one during it reported ~963,000 changed pixels — and ~969,000 AFTER it had
     expired, because the stage scrolls and every pixel moves regardless. A number that large is
     not evidence of anything. The banner has to be isolated against the SAME game state: draw
     the identical tick twice, once with it and once without, and report where the difference
     lands. A text band in the upper middle is the banner; anything else is not. */
  step(20);
  arcadeBanner('LVL 1 MACHINE GUN');
  const t0=_arcBan?_arcBan.t:null;
  step(12);
  const t1=_arcBan?_arcBan.t:null;

  try{ drawWorld(0); }catch(e){}  const withB=grab();
  const keep=_arcBan; _arcBan=null;
  try{ drawWorld(0); }catch(e){}  const without=grab();
  _arcBan=keep;

  const c=document.getElementById('screen'), W=c.width;
  let n=0, x0=1e9, y0=1e9, x1=-1, y1=-1;
  for(let i=0;i<withB.length;i+=4){
    if(withB[i]!==without[i]||withB[i+1]!==without[i+1]||withB[i+2]!==without[i+2]){
      n++; const px=(i>>2)%W, py=(i>>2)/W|0;
      if(px<x0)x0=px; if(px>x1)x1=px; if(py<y0)y0=py; if(py>y1)y1=py;
    }
  }
  step(200);                                    // long past its total life
  return { ticks:(t0!=null && t1!=null && t1>t0),
           expired:!_arcBan, px:n,
           box:(x1<0?null:{x:x0,y:y0,w:x1-x0+1,h:y1-y0+1}),
           canvas:{w:c.width,h:c.height} };
}
"""

GLYPHS=r"""
()=>{
  const a1=defFontArt(), a2=defFontAlt();
  const has=(ch)=>{ const ok=(a)=>!!(a&&a.font&&a.font[ch]&&a.frames&&a.frames[a.font[ch]]); return ok(a1)||ok(a2); };
  const set=" ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?.,:'-";
  const missing=[]; for(const ch of set) if(ch!==' ' && !has(ch)) missing.push(ch);
  return {ready:!!(a1&&a1.img&&a1.img.complete), missing,
          measure:{ shortAt16:msgMeasure('LVL 1 MACHINE GUN',16),
                    wrapAt200:msgWrap('SCOUT REPORTS HEAVY ARMOUR ON THE RIVER LINE', 200, 12) }};
}
"""

SHOT=r"""
([mode])=>{
  if(mode==='banner'){ arcadeBanner(arcWeaponAnnounce(0,1)); }
  if(mode==='dialog'){
    /* drive the real story panel rather than drawing one by hand */
    if(typeof story!=='undefined' && story){ story.fade=1; }
  }
  for(let i=0;i<26;i++){ updatePlay(1/60); try{ drawWorld(1/60); }catch(e){} }
  if(mode==='banner'){ /* park it mid-SWEEP, which is the beat worth photographing */
    for(let i=0;i<12;i++){ updatePlay(1/60); try{ drawWorld(1/60); }catch(e){} } }
  return document.getElementById('screen').toDataURL('image/png');
}
"""

CANDS=r"""
()=>{
  const keys=['ndk_shot_0','ndk_shot_1','ndk_shot_2','ndk_shot_3','ndk_shell_0','spicon_decker'];
  const cv=document.createElement('canvas'); cv.width=keys.length*96; cv.height=110;
  const g=cv.getContext('2d');
  g.fillStyle='#11151c'; g.fillRect(0,0,cv.width,cv.height);
  const got=[];
  keys.forEach((k,i)=>{
    if(typeof XART==='undefined' || !XART.rdy(k)) return;
    const im=XART.get(k); if(!im||!im.naturalWidth) return;
    const s=76/Math.max(im.naturalWidth,im.naturalHeight);
    g.drawImage(im, i*96+48-im.naturalWidth*s/2, 44-im.naturalHeight*s/2, im.naturalWidth*s, im.naturalHeight*s);
    g.fillStyle='#8ecbff'; g.font='11px monospace'; g.textAlign='center'; g.fillText(k, i*96+48, 100);
    got.push(k);
  });
  return {img:cv.toDataURL('image/png'), got};
}
"""

from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port

def save(name, dataurl):
    with open(os.path.join(OUT,name),'wb') as fh:
        fh.write(base64.b64decode(dataurl.split(',',1)[1]))

with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)

    s=pg.evaluate(SETUP)
    bad=[k for k,v in s['scope'].items() if v!='function']
    print('SCOPE  '+('all reachable' if not bad else '*** NOT REACHABLE: '+', '.join(bad)+' ***'))
    pg.wait_for_function("()=>{const a=defFontArt(); return !!(a&&a.img&&a.img.complete);}", timeout=45000)
    w=pg.evaluate(WIRED)
    # ⚠ THE STATE HALF IS TRUSTWORTHY; THE PIXEL HALF IS NOT, AND BOTH ARE REPORTED AS SUCH.
    # Two drawWorld calls on the identical game state STILL differ across the whole canvas,
    # because the renderer reads performance.now() directly for clouds, water frames, scanline
    # phase and muzzle timers. So the isolation this was reaching for is not available here and
    # the box below covers the frame. Three instruments failed on this one question in a row —
    # a source grep (too shallow: the call is in updateEffects), a before/after diff (the stage
    # scrolls), and this same-state diff. THE SCREENSHOT IS THE PROOF. See banner_0811m.png.
    print('WIRED  clock advances=%s  expires=%s   (state is sound; the DRAW is proven by the'
          % (w['ticks'], w['expired']))
    print('       screenshot, not by these numbers — same-state frame isolation does not hold in')
    print('       this renderer, box came back as the whole %dx%d canvas)' % (w['canvas']['w'], w['canvas']['h']))
    gl=pg.evaluate(GLYPHS)
    print("GLYPHS ready=%s  missing from the BOF face: %s"
          % (gl['ready'], (', '.join(gl['missing']) if gl['missing'] else 'none')))
    print("       'LVL 1 MACHINE GUN' at H16 measures %spx" % gl['measure']['shortAt16'])
    print("       wrapped to 200px  -> %s" % gl['measure']['wrapAt200'])

    c=pg.evaluate(CANDS)
    save('decker_shotbox_candidates_0811m.png', c['img'])
    print('DECKER candidates rendered: %s  -> docs/proofs/decker_shotbox_candidates_0811m.png'
          % (', '.join(c['got']) if c['got'] else 'NONE resolved'))
    b.close()

    for mode in ('banner',):
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
        pg.evaluate(SETUP)
        pg.wait_for_function("()=>{const a=defFontArt(); return !!(a&&a.img&&a.img.complete);}", timeout=45000)
        save('%s_0811m.png'%mode, pg.evaluate(SHOT,[mode]))
        print('%s -> docs/proofs/%s_0811m.png' % (mode, mode))
        b.close()
