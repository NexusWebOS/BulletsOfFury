#!/usr/bin/env python3
"""probe_pickicon.py — what does a powerbox pickup ACTUALLY draw?

Mike, 0811m:
  "On Level 3 - Fireorb icon does not appear and displays as ice orb instead when opened from
   a powerbox"
  "On Level 2 - Icebreath icon does not appear and shows as flamethrower icon when opened from
   a powerbox"

⚠ THIS HAS BEEN 'FIXED' TWICE ALREADY AND HE IS STILL LOOKING AT THE WRONG ICON. Drop 0806d
fixed weaponIconKey; drop 0810f fixed the first fallback beneath it. Both fixes were real and
both were verified by asking the RESOLVER what key it returns — which is not the question. The
question is which image lands on the screen, and the draw path has more than one table in it.

So this probe does two things and reports them side by side:

  1. RESOLUTION — for each candidate key in the chain, which of the three art stores holds it
     (XART / ASSETS / BOFX.icons). A key that resolves in none of them is a branch that can
     never draw, and the draw falls through to whatever is beneath it.
  2. PIXELS — it spawns the real pickup, steps the real draw, and crops the icon off the live
     canvas. That crop is the answer. Everything above it is context for why.
"""
import http.server, socketserver, threading, os, functools, base64
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')

def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

RUN=r"""
([stage, pilot, slot, lv])=>{
  ASSETS.ready=true; run.pilot=pilot; run.mode='arcade'; run.stage=stage;
  beginStage(stage); setState(GS.PLAY); player.reset(); player.invuln=1e9;

  run.weapon=slot; run.wlevels=run.wlevels||{}; run.wlevels[slot]=lv;

  const where=(k)=>({
    key:k,
    XART:   (typeof XART!=='undefined' && XART._src && !!XART._src[k]),
    ASSETS: (typeof ASSETS!=='undefined' && typeof ASSETS.has==='function' && !!ASSETS.has(k)),
    icons:  (typeof BOFX!=='undefined' && BOFX.icons && !!BOFX.icons[k]),
  });

  const legacy={0:'mg',1:'spread',2:'missile',3:'laser',4:'firewall',5:'iceorb'}[slot];
  const chain=[
    weaponIconKey(slot, lv),          // what the RESOLVER says the icon is
    'ice_icon_'+lv,                   // fallback used for slot 5
    'firewall_icon_'+lv,              // fallback used for slot 4
    'laser_icon_'+lv,
    'pw_'+legacy+'_'+lv,              // the ASSETS fall-through beneath all of them
    'micon_icebreath_'+lv,
    'micon_fireorb_'+lv,
    'micon_iceorb_'+lv,
  ].map(where);

  /* ⚠ TOUCH THE SHEETS AND RETURN. A single evaluate NEVER YIELDS, so lazily-loaded art can
     not arrive inside it however many frames are stepped — the --warm trap in CLAUDE.md. The
     first XART.rdy call is what STARTS each load; Python then waits at the evaluate boundary,
     which is the only thing that lets the network run, and the drawing happens in STEP two. */
  if(typeof XART!=='undefined'){ XART.rdy('nia_icons'); XART.rdy('nia_icons2'); }
  window.__pk={kind:'weapon', wtype:slot, x:240, y:300, t:0, vy:0, life:99, w:26, h:26};

  return {stage, pilot, slot, lv, resolver:weaponIconKey(slot,lv),
          orbIsFire:(typeof orbIsFire==='function'?orbIsFire():null), chain};
}
"""

DRAW=r"""
()=>{
  /* ⚠ THE POOLS ARE REASSIGNED, NOT MUTATED — powerups = powerups.filter(...) — so a pushed
     object is silently dropped on the first cull and the fixture measures an empty screen.
     Re-seat it every frame and pin its position; that is the same trap that reported 0 rounds
     for every stage when eBullets.push was wrapped. */
  const P=window.__pk;

  /* ⚠ OBSERVE THE REAL CALL, DO NOT RECOMPUTE IT. Cropping the canvas at a position this probe
     works out for itself is the probe_seam.py mistake — it asserted the fix it was meant to test
     because it computed the answer instead of reading it. Wrapping the two lookups the pickup
     branch actually calls records WHICH KEY WON on the real draw path, which is the question.
     (Wrapping is safe here and not the drawImage-counting mistake: nothing is invoked by hand,
     the real frame runs and reports what it asked for.) */
  const seen=[];
  const _ib=iconBlit, _rdy=XART.rdy.bind(XART);
  iconBlit=function(g,k){ const r=_ib.apply(this,arguments); seen.push({via:'iconBlit',key:k,drew:!!r}); return r; };
  XART.rdy=function(k){ const r=_rdy(k);
    if(/^(ice|firewall|laser)_icon_|^pw_/.test(k)) seen.push({via:'legacy',key:k,drew:!!r});
    return r; };

  for(let i=0;i<40;i++){
    if(powerups.indexOf(P)<0) powerups.push(P);
    P.x=240; P.y=300; P.dead=false; P.life=99;
    updatePlay(1/60); try{ drawWorld(1/60); }catch(e){}
  }
  iconBlit=_ib; XART.rdy=_rdy;

  /* keep only the last frame's worth, deduped, so the report is one line per candidate */
  const uniq={}; for(const s of seen) uniq[s.via+' '+s.key]=s.drew;
  const cv=document.getElementById('screen');
  return {picked:Object.keys(uniq).map(k=>k+(uniq[k]?'  <= DREW':'  (miss)')),
          full:cv.toDataURL('image/png'),
          sheetReady:XART.rdy('nia_icons'), inPool:powerups.indexOf(P)>=0};
}
"""
from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port

# stage, pilot, weapon slot, level    -- the two Mike named, plus the control
CASES=[(3,'cole',5,3,'L3 fireball (slot 5, orbIsFire)'),
       (2,'freezer',4,3,'L2 ice breath (slot 4, Freezer)'),
       (1,'cole',5,3,'L1 ice orb (slot 5, control)')]

with sync_playwright() as p:
    for stage,pilot,slot,lv,label in CASES:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
        r=pg.evaluate(RUN,[stage,pilot,slot,lv])
        print('\n%s   resolver -> %s   orbIsFire=%s' % (label, r['resolver'], r['orbIsFire']))
        for c in r['chain']:
            stores=[n for n in ('XART','ASSETS','icons') if c[n]]
            print('    %-24s %s' % (c['key'], ', '.join(stores) if stores else '*** IN NO STORE — this branch can never draw ***'))
        # the evaluate boundary is what lets the icon sheet's network request finish
        pg.wait_for_function("()=>typeof XART!=='undefined' && XART.rdy('nia_icons')", timeout=45000)
        d=pg.evaluate(DRAW)
        print('    sheet ready=%s  pickup in pool=%s   WHAT THE DRAW PATH ASKED FOR:'
              % (d['sheetReady'], d['inPool']))
        for line in d['picked']: print('        '+line)
        with open(os.path.join(OUT,'pickicon_0811m_s%d_%s.png'%(stage,pilot)),'wb') as fh:
            fh.write(base64.b64decode(d['full'].split(',',1)[1]))
        b.close()
