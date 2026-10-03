"""icon_ink_1002 - measure every weapon icon's VISIBLE ink box through the game's own iconBlit.

    python3 _BUILD_SOURCE/icon_ink_1002.py [--write]

Mike (1002): "their weapon pick up icons are very small in game ... we should be keeping a unified system of
h/w for each icon as an engine rule."

Every icon is drawn by iconBlit at a requested HEIGHT, and each art family carries a different transparent
margin inside its cell - the space Fusion badges fill only 57-67 px of a 104x112 cell, so at the same requested
height they draw a third smaller than the micon_ badges beside them. The rule therefore has to be about INK, and
ink cannot be measured at runtime (getImageData refuses a file:// page). So this measures it here, in real
Chromium over http, through the exact draw path the game uses, and --write stores
assets/data/icon_ink_1002.json and assets/icon_ink_1002.js: per key, the ink box as fractions of the box iconBlit drew
(x, y, w, h of ink within [0..1] of the drawn width/height). feedback_1002.js reads that table and draws every
icon so its INK fills one unified box.

Keys measured: every BOFX.icons cell, weaponIconKey() for all nine slots x five levels x nine pilots (both
normal and Freezer/Yuri/Maverick variants fall out of that), the forge badges, and the four space families.
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

KEYS = r"""
()=>{
  const set=new Set(Object.keys((BOFX&&BOFX.icons)||{}));
  const keep=run.pilot,keepStage=run.stage;
  for(const p of ['cole','axel','yuri','falva','decker','freezer','juggernaut','lizzie','maverick']){
    run.pilot=p;
    for(let st of [1,2,3,4,6,7,8]){run.stage=st;
      for(let w=0;w<9;w++)for(let lv=1;lv<=5;lv++){try{const k=weaponIconKey(w,lv);if(k)set.add(k);}catch(e){} try{const k=weaponIconKey(w,lv,{bare:1});if(k)set.add(k);}catch(e){}}}
  }
  run.pilot=keep;run.stage=keepStage;
  for(const f of ['space_laser_icon_','space_fusion_icon_','space_volley_icon_','space_shadow_icon_','micon_lasermist_','micon_firewhip_0919_'])for(let i=1;i<=5;i++)set.add(f+i);
  return [...set].sort();
}
"""
MEASURE = r"""
(keys)=>{
  const out={},H=100,cv=document.createElement('canvas');cv.width=320;cv.height=200;const g=cv.getContext('2d',{willReadFrequently:true});
  for(const k of keys){
    g.clearRect(0,0,320,200);let w=null;
    // ALWAYS the raw draw: once feedback_1002 wraps iconBlit, measuring the wrapper would measure the rule itself
    const raw=(typeof FB2_ICONBLIT==='function')?FB2_ICONBLIT:iconBlit;
    try{w=raw(g,k,160,100,H,true);}catch(e){out[k]={err:String(e).slice(0,80)};continue;}
    if(!w){out[k]={miss:true};continue;}
    const d=g.getImageData(0,0,320,200).data;let x0=999,y0=999,x1=-1,y1=-1;
    for(let y=0;y<200;y++)for(let x=0;x<320;x++){if(d[(y*320+x)*4+3]>24){if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}}
    if(x1<0){out[k]={empty:true,w};continue;}
    const bx=160-w/2,by=100-H/2;
    out[k]={w:+w.toFixed(2),ix:+((x0-bx)/w).toFixed(4),iy:+((y0-by)/H).toFixed(4),iw:+((x1-x0+1)/w).toFixed(4),ih:+((y1-y0+1)/H).toFixed(4),inkW:x1-x0+1,inkH:y1-y0+1};
  }
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true'); a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'], **({'executable_path': chrome} if os.path.exists(chrome) else {}))
        pg = b.new_page()
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(shoot.TRAP_RAF)
        keys = pg.evaluate(KEYS)
        # touch every key (first rdy() call starts the decode), then wait for real time to pass
        res = {}
        for attempt in range(8):
            res = pg.evaluate(MEASURE, keys)
            missing = [k for k, v in res.items() if v.get('miss') or v.get('empty')]
            if not missing: break
            pg.wait_for_timeout(1500)
        b.close()
    stop()
    good = {k: v for k, v in res.items() if 'ih' in v}
    print('keys', len(keys), 'measured', len(good), 'missing', [k for k in res if k not in good][:20])
    rows = sorted(good.items(), key=lambda kv: kv[1]['inkH'])
    for k, v in rows[:12] + [('...', None)] + rows[-6:]:
        print(k if v is None else '%-34s inkH %3d inkW %3d  (ink %.2f x %.2f of the drawn box)' % (k, v['inkH'], v['inkW'], v['iw'], v['ih']))
    if a.write:
        # [ink x, ink y, ink w, ink h] as fractions of the drawn box, plus the box's own aspect (drawn w / h)
        tab = {k: [v['ix'], v['iy'], v['iw'], v['ih'], round(v['w'] / 100.0, 4)] for k, v in good.items()}
        p = os.path.join(ROOT, 'assets/data/icon_ink_1002.json')
        json.dump(tab, open(p, 'w'), separators=(',', ':'), sort_keys=True)
        # a file:// page cannot fetch JSON, so the game reads the same table from a script
        pj = os.path.join(ROOT, 'assets/icon_ink_1002.js')
        open(pj, 'w', newline='\n').write('"use strict";\n/* generated by _BUILD_SOURCE/icon_ink_1002.py --write - do not hand-edit */\nconst ICON_INK_1002=' + json.dumps(tab, separators=(',', ':'), sort_keys=True) + ';\n')
        print('wrote', p, 'and', pj, len(tab), 'entries')
    print('errors', errs[:3])


if __name__ == '__main__':
    main()
