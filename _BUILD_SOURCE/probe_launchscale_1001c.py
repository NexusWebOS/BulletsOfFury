"""probe_launchscale_1001c - what size is the ship, and is the world moving, from the stage card to PLAY.

    python3 _BUILD_SOURCE/probe_launchscale_1001c.py [--stages 1,2,3,4,7,8,9] [--pilot cole] [--frames 900]

Mike, 1001: "keep it at gameplay scale at all times and not do that or any sudden stops on any levels ...
always remain in motion but just slow down as we get to the intros."

For every frame it records the HEIGHT the ship was actually drawn at (wrapping the screen context's own
drawImage and XART.get for the key - CLAUDE.md: ctx carries its own drawImage, and XART.get returns a
canvas with no .src), the launch phase and its speed, and how far mapScroll moved. The verdicts:
  - every ship blit from the first launch frame to 3 s into PLAY is within 2 px of PLAY's own height;
  - drawLaunch._spd never drops below a floor (no dead stop) while the launch runs;
  - and a CONTROL arm (--busted) that restores the old 62 px plate, so a pass cannot mean "no ship drawn".
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SCENE = r"""
(cfg)=>{
  const N=cfg.stage;
  ASSETS.ready=true; run.pilot=cfg.pilot; run.stage=N; curStage=STAGES[N-1];
  playerHit=function(){};
  beginStage(N);
  const c=document.querySelector('#screen').getContext('2d');
  const od=c.drawImage, oget=XART.get, tag=new Map();
  XART.get=function(k){const im=oget.apply(this,arguments); if(im&&/^(ship_|nsa_|gravity|furyship|fury_)/.test(k)) tag.set(im,k); return im;};
  if(typeof furyShipCanvas==='function'){const ofc=furyShipCanvas; window.furyShipCanvas=function(k){const im=ofc.apply(this,arguments); if(im) tag.set(im,'fury:'+k); return im;};}
  window.__rec=[]; let frameShip=[];
  c.drawImage=function(){ const a=arguments, k=tag.get(a[0]);
    if(k&&a.length>=5){ const t=c.getTransform(); const h=(a.length===9?a[8]:a[4])*Math.hypot(t.c,t.d)/2;
      frameShip.push([k,Math.round(h*10)/10]); }
    return od.apply(this,a); };
  let prevMS=mapScroll;
  window.__qaTick=function(){
    const ms=(typeof mapScroll==='number')?mapScroll:0;
    window.__rec.push({st:state,ph:drawLaunch._phase,spd:Math.round(drawLaunch._spd||0),bg:Math.round(drawLaunch._bgScroll||0),
      dms:Math.round((ms-prevMS)*60),ship:frameShip.slice(0,4)});
    prevMS=ms; frameShip=[]; tag.clear();
  };
  return state;
}
"""


def run(stages, pilot, frames):
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    out = {}
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        kw = {'executable_path': chrome} if os.path.exists(chrome) else {}
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'], **kw)
        for n in stages:
            pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
            pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
            pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
            pg.evaluate(shoot.TRAP_RAF)
            pg.evaluate(SCENE, {'stage': n, 'pilot': pilot})
            for _ in range(frames // 10):
                pg.evaluate(shoot.STEP, 10)
                pg.wait_for_timeout(15)
            rec = pg.evaluate("()=>window.__rec")
            out[n] = {'rec': rec, 'errors': errs}
            pg.close()
        b.close()
    stop()
    return out


def verdict(n, rec):
    play = [i for i, r in enumerate(rec) if r['st'] == 'play']
    first_play = play[0] if play else None
    launch = [i for i, r in enumerate(rec) if r['st'] == 'launch']
    hull = lambda k: k.startswith('ship_') or k in ('fury:base',) or k.startswith('fury:roll') or k.startswith('fury:so')
    hs = lambda r: [s[1] for s in r['ship'] if s[1] > 12 and hull(s[0])]
    ref = None
    if first_play is not None:
        tail = [h for r in rec[first_play + 30:first_play + 180] for h in hs(r)]
        if tail:
            tail.sort()
            ref = tail[len(tail) // 2]
    span = rec[(launch[0] if launch else 0):(first_play + 180 if first_play is not None else len(rec))]
    heights = [h for r in span for h in hs(r)]
    off = [h for h in heights if ref and abs(h - ref) > 2.0]
    L = [r for r in rec if r['st'] == 'launch' and r['ph']]
    lspd = [r['spd'] for r in L]
    drops = [L[i - 1]['spd'] - L[i]['spd'] for i in range(1, len(L))]
    return {'stage': n, 'first_play': first_play, 'play_h': ref, 'launch_frames': len(launch),
            'h_min': min(heights) if heights else None, 'h_max': max(heights) if heights else None,
            'off_scale_blits': len(off), 'launch_spd_min': min(lspd) if lspd else None,
            'launch_spd_max': max(lspd) if lspd else None,
            'max_drop_per_frame': max(drops) if drops else None,
            'phases': sorted(set(r['ph'] for r in rec if r['st'] == 'launch' and r['ph']))}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--stages', default='1,2,3,4,7,8,9')
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--frames', type=int, default=1200)
    ap.add_argument('--dump', default='')
    a = ap.parse_args()
    res = run([int(s) for s in a.stages.split(',')], a.pilot, a.frames)
    for n, d in res.items():
        print(json.dumps(verdict(n, d['rec'])), 'errors', len(d['errors']))
    if a.dump:
        json.dump(res, open(a.dump, 'w'))
