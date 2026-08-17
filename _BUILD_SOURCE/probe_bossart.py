#!/usr/bin/env python3
"""probe_bossart.py - which bosses and minibosses actually resolve their art?

Mike: "you didnt replace the bosses and minibosses on the other levels like I asked."

CLAUDE.md already records two known holes - Herald's `mba_vr_*` plates absent from XART (routed
around, not fixed) and `subcore`/`ratking` having no new-pack art. This audits ALL of them rather
than the two that happen to be written down, per stage, so the answer is a list and not an anecdote.

⚠ XART.rdy() STARTS the decode and returns FALSE on that first call. Every key is touched once and
then waited on; asking once and believing the answer reports the whole game as missing art.

⚠ A KEY THAT RESOLVES IS NOT A KEY THAT IS RIGHT. This says what the game can DRAW - it cannot say
whether the plate is the one Mike wants. Anything reported present still needs an eyeball.
"""
import http.server, socketserver, threading, functools
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

COLLECT = r"""
()=>{
  const out={bosses:[], subs:[], stages:[]};
  try{
    for(const k in SHIPBOSS){ const d=SHIPBOSS[k]; out.bosses.push({id:k, key:d.key||null, name:d.name||null}); }
  }catch(e){ out.err='SHIPBOSS: '+String(e); }
  try{
    for(const k in SUBBOSS){ const d=SUBBOSS[k]; out.subs.push({id:k, key:d.key||d.art||null, name:d.name||null}); }
  }catch(e){ out.err=(out.err||'')+' SUBBOSS: '+String(e); }
  try{
    for(const s of STAGES) out.stages.push({n:s.n, boss:s.boss||null});
  }catch(e){}
  return out;
}
"""

from playwright.sync_api import sync_playwright
port = serve(GAME)
with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = br.new_page(viewport={'width': 620, 'height': 900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(3000)

    info = pg.evaluate(COLLECT)
    if info.get('err'): print('collect: %s' % info['err'])
    stage_of = {}
    for s in info.get('stages', []):
        if s.get('boss'): stage_of[s['boss']] = s['n']

    keys = [b['key'] for b in info['bosses'] if b['key']] + [s['key'] for s in info['subs'] if s['key']]
    keys = sorted(set(keys))
    # touch every key once (that STARTS the decode), then wait for them to settle
    pg.evaluate("(ks)=>{for(const k of ks){ try{ XART.rdy(k); }catch(e){} }}", keys)
    try:
        pg.wait_for_function("(ks)=>ks.every(k=>{try{return XART.rdy(k);}catch(e){return true;}})",
                             arg=keys, timeout=25000)
    except Exception:
        pass   # some genuinely will not resolve - that is the finding, not an error

    res = pg.evaluate("""(ks)=>{const o={};for(const k of ks){
        let rdy=false, src=false;
        try{ rdy=!!XART.rdy(k); }catch(e){}
        try{ src=!!(XART._src&&XART._src[k]); }catch(e){}
        o[k]={rdy:rdy, src:src};} return o;}""", keys)

    def show(title, rows):
        print('\n=== %s ===' % title)
        miss = 0
        for r in sorted(rows, key=lambda r: (stage_of.get(r['id'], 99), r['id'])):
            k = r['key']
            st = stage_of.get(r['id'])
            stl = ('stage %d' % st) if st else '-'
            if not k:
                print('  %-9s %-18s %-28s *** NO ART KEY AT ALL' % (stl, r['id'][:18], '-')); miss += 1; continue
            v = res.get(k, {})
            if v.get('rdy'):
                print('  %-9s %-18s %-28s ok' % (stl, r['id'][:18], k[:28]))
            else:
                print('  %-9s %-18s %-28s *** DOES NOT RESOLVE%s'
                      % (stl, r['id'][:18], k[:28], ' (not even registered)' if not v.get('src') else ''))
                miss += 1
        return miss

    m1 = show('BOSSES', info['bosses'])
    m2 = show('MINIBOSSES', info['subs'])
    if errs: print('\nPAGE ERRORS: %s' % errs[:2])
    print('\n%d boss(es) and %d miniboss(es) cannot draw their art'
          % (m1, m2) if (m1 or m2) else '\nevery boss and miniboss resolves its art')
    br.close()
