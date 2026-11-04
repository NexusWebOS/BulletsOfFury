"""Native Chromium probe for assets/projectile_fx_1103.js (PFX13).

    python _BUILD_SOURCE/probe_projectile_fx_1103.py

Checks, on real encounters with the full renderer:
  - renderer only: the same frame drawn by both renderers leaves every round's state and the RNG identical
    (the fight itself is not deterministic run to run, so comparing two runs proves nothing)
  - no shadowBlur reaches the canvas while rounds draw (it is converted to pixel rings)
  - zero page/console errors; frame cost on vs off
Screens: _shots/projectiles_1103/live/*.png
"""
from pathlib import Path
import json, sys, base64, http.server
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
O = R / '_shots/projectiles_1103/live'; O.mkdir(parents=True, exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
checks, errors = [], []
def ok(name, cond, info=''):
    checks.append({'name': name, 'pass': bool(cond), 'info': info}); print(('PASS ' if cond else 'FAIL ') + name, info, flush=True)

CASES = [dict(id='s2-boss', stage=2, kind='infernoreaver', diff='furious'),
         dict(id='s5-stage', stage=5, kind='xenoregent', diff='furious', slice=True),
         dict(id='s8-mini', stage=8, kind='heralddeath', diff='furious', mini=True),
         dict(id='s1-stage', stage=1, kind='damkeeper', diff='furious', slice=True)]
RUN = """async ([c,off,frames,shotAt])=>{
  window.PFX13_OFF=off?1:0; c.seed=1103; c.pilot='yuri'; c.level=4; AP7.begin(c);
  for(const k of keybindFor(1).fire||[])if(!k.startsWith('pad_'))Input.keys[k]=true;
  let blurLeak=0,ms=0,shots={},inB=false,cmp=false;
  const own=Object.getOwnPropertyDescriptor(ctx,'shadowBlur')||Object.getOwnPropertyDescriptor(CanvasRenderingContext2D.prototype,'shadowBlur');
  Object.defineProperty(ctx,'shadowBlur',{configurable:true,get(){return own.get.call(this);},set(v){own.set.call(this,v);if(inB&&!cmp&&own.get.call(this)>0)blurLeak++;}});
  const db=drawBullets; drawBullets=function(){inB=true;try{return db.apply(this,arguments);}finally{inB=false;}};
  const sig=[],same={n:0,state:0,rng:0,rounds:0,tOff:0,tOn:0};
  for(let f=0;f<frames;f++){
    player.invuln=99999;player.dead=false;run.shield=999;
    player.x=worldWidth()/2+Math.sin(f/90)*110;player.y=VH-90;
    updatePlay(1/60);
    const t0=performance.now();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);ms+=performance.now()-t0;
    if(!off&&f%60===30){   // same frame, both renderers: does drawing change any round or the RNG?
      const all=[...pBullets,...eBullets],snap=()=>all.map(b=>{const o={};for(const k in b){const v=b[k];if(v===null||typeof v!=='object'&&typeof v!=='function')o[k]=v;}return o;});
      const restore=s0=>all.forEach((b,i)=>{for(const k in b){const v=b[k];if((v===null||typeof v!=='object'&&typeof v!=='function')&&!(k in s0[i]))delete b[k];}Object.assign(b,s0[i]);});
      const rnd=Math.random;let calls=0;Math.random=function(){calls++;return rnd.apply(this,arguments);};
      const s0=snap();ctx.setTransform(SS,0,0,SS,0,0);
      cmp=true;const flush=()=>ctx.getImageData(0,0,1,1);
      window.PFX13_OFF=1;calls=0;drawBullets();const sOff=JSON.stringify(snap()),cOff=calls;restore(s0);
      window.PFX13_OFF=0;calls=0;drawBullets();const sOn=JSON.stringify(snap()),cOn=calls;restore(s0);
      for(let r=0;r<3;r++)for(const m of (r%2?[0,1]:[1,0])){window.PFX13_OFF=m;flush();const q0=performance.now();drawBullets();flush();same[m?'tOff':'tOn']+=(performance.now()-q0)/3;restore(s0);}
      cmp=false;
      Math.random=rnd;window.PFX13_OFF=0;
      same.n++;if(sOff!==sOn)same.state++;if(cOff!==cOn)same.rng++;same.rounds+=all.length;
    }
    if(f%60===59)sig.push(eBullets.length+':'+pBullets.length+':'+eBullets.reduce((a,b)=>a+Math.round(b.x*7+b.y*3),0));
    if(shotAt.includes(f))shots[f]=cv.toDataURL('image/png').split(',')[1];
  }
  drawBullets=db; Object.defineProperty(ctx,'shadowBlur',own);
  for(const k in Input.keys)Input.keys[k]=false;
  return {same,sig,blurLeak,ms:ms/frames,shots,rounds:eBullets.length+pBullets.length};
}"""
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio']); cx = br.new_context(viewport={'width': 1100, 'height': 950})
        cx.route('**/*', lambda r: r.continue_() if r.request.url.startswith(('http://127.0.0.1:', 'data:', 'blob:')) else r.abort())
        p = cx.new_page(); p.set_default_timeout(180000)
        p.on('pageerror', lambda e: errors.append(str(e)[:300]))
        p.on('console', lambda m: errors.append(m.text[:300]) if m.type == 'error' and ('127.0.0.1' in m.text or 'ERR_' not in m.text) else None)
        p.goto(f'http://127.0.0.1:{port}/index.html'); p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        for f in ['balance_lab_1007.js', 'projectile_lab_1007.js']: p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        ok('module loaded and wrapping drawBullets', p.evaluate('()=>!!window.PFX13&&drawBullets!==PFX13.original'))
        for c in CASES:   # warm art for both runs
            p.evaluate(RUN, [c, False, 240, []])
        p.wait_for_timeout(2500)
        for c in CASES:
            off = p.evaluate(RUN, [c, True, 600, [300, 420, 540]])
            on = p.evaluate(RUN, [c, False, 600, [300, 420, 540]])
            sm = on['same']
            ok(f"{c['id']} renderer only: same frame drawn both ways leaves every round and the RNG identical", sm['n'] > 0 and sm['state'] == 0 and sm['rng'] == 0, f"{sm['n']} frames, {sm['rounds']} round-samples, state diffs {sm['state']}, rng diffs {sm['rng']}")
            ok(f"{c['id']} no blur reaches the canvas while rounds draw", on['blurLeak'] == 0, f"on={on['blurLeak']} off={off['blurLeak']} (off shows how many soft-blur draws the shipping path makes)")
            a, b = sm['tOn'] / max(1, sm['n']), sm['tOff'] / max(1, sm['n'])
            ok(f"{c['id']} drawBullets cost, same frames: under +1 ms or faster", a < b + 1.0, f"on {a:.2f} ms vs shipping {b:.2f} ms (whole drawWorld, different timelines: {on['ms']:.1f} vs {off['ms']:.1f})")
            for f, data in on['shots'].items(): (O / f"{c['id']}-{f}-after.png").write_bytes(base64.b64decode(data))
            for f, data in off['shots'].items(): (O / f"{c['id']}-{f}-before.png").write_bytes(base64.b64decode(data))
        br.close()
finally:
    stop()
ok('zero page/console errors', not errors, '; '.join(errors[:3]))
(O / 'report.json').write_text(json.dumps({'checks': checks, 'errors': errors}, indent=2))
print('RESULT', sum(c['pass'] for c in checks), '/', len(checks))
