"""probe_fusion_icons_1002 - the solid fusion beam and the unified icon size (Mike, 1002), in real Chromium.

    python3 _BUILD_SOURCE/probe_fusion_icons_1002.py [--old]

ICONS: every key in the ink table is drawn through the LIVE iconBlit at 40 and 64 px; its ink must be the
requested height (+-2 px) and never wider than the unified box, every call must report the same box width, and
the space Fusion badges must now match the volley badges beside them (they measured 65-77% before).
BEAM: a released space Fusion shot and Cole's level-8 fusion cannon must both blit fb2_fusion_beam (by KEY, a
wrap on XART.get) and neither may blit the old lances (fusion30_beam / eglaser_*). Sheets are saved for the eye.
--old routes feedback_1002.js to an empty body.
"""
import argparse, base64, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

ICONS = r"""
()=>{
  const keys=Object.keys(ICON_INK_1002),cv=document.createElement('canvas');cv.width=240;cv.height=160;const g=cv.getContext('2d',{willReadFrequently:true});
  const out={};
  for(const H of [40,64]){for(const k of keys){
    g.clearRect(0,0,240,160);const w=iconBlit(g,k,120,80,H,true);if(!w){out[k+'@'+H]={miss:1};continue;}
    const d=g.getImageData(0,0,240,160).data;let x0=999,y0=999,x1=-1,y1=-1;
    for(let y=0;y<160;y++)for(let x=0;x<240;x++)if(d[(y*240+x)*4+3]>24){if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}
    out[k+'@'+H]={w:+w.toFixed(2),inkW:x1-x0+1,inkH:y1-y0+1,cx:(x0+x1)/2,cy:(y0+y1)/2};
  }}
  return out;
}
"""
SHEET = r"""
()=>{
  const keys=['space_fusion_icon_1','space_fusion_icon_3','space_fusion_icon_5','space_volley_icon_3','space_laser_icon_3','micon_thermoshock_3','micon_mg_3','micon_fireorb_3','micon_chaingun_3','micon_laser_3'].filter(k=>ICON_INK_1002[k]);
  const H=48,cv=document.createElement('canvas');cv.width=keys.length*60+20;cv.height=2*70+20;const g=cv.getContext('2d');
  g.fillStyle='#1a1d26';g.fillRect(0,0,cv.width,cv.height);
  const raw=(typeof FB2_ICONBLIT==='function')?FB2_ICONBLIT:iconBlit;
  keys.forEach((k,i)=>{const x=40+i*60;raw(g,k,x,45,H,true);iconBlit(g,k,x,115,H,true);g.strokeStyle='rgba(255,255,255,.25)';g.strokeRect(x-H*.465,115-H/2,H*.93,H);});
  return {keys,url:cv.toDataURL('image/png')};
}
"""
SPACE = r"""
()=>{
  ASSETS.ready=true; window.__bofStepNow=performance.now();
  run.pilot='cole'; run.stage=5; run.mode='arcade'; curStage=STAGES[4];
  beginStage(5); setState(GS.PLAY); player.reset(); playerHit=function(){};
  if(typeof spaceModeStage==='function')try{spaceModeStage(5);}catch(e){}
  run.spaceWeapon=1; enemies.length=0;
  const L=window.__L={keys:{}};const g=XART.get;XART.get=function(k){L.keys[k]=(L.keys[k]||0)+1;return g.apply(this,arguments);};
  XART.rdy('fb2_fusion_beam');XART.rdy('fusion30_beam');
  return {space:typeof spaceWeaponsActive==='function'&&spaceWeaponsActive()};
}
"""
FIRE_SPACE = r"""
()=>{window.__L.keys={};const fc=fusion30Cell;let beams=0;fusion30Cell=function(n){if(n==='beam'&&FUSION30_ART.beam&&XART.rdy(FUSION30_ART.beam.key))window.__L.keys[FUSION30_ART.beam.key]=(window.__L.keys[FUSION30_ART.beam.key]||0)+1;return fc.apply(this,arguments);};
  const ok=spaceShadowRelease(FUSION30_FULL*1.2);let n=0;
  for(let i=0;i<14;i++){window.__bofStepNow+=1000/60;loop(window.__bofStepNow);}
  const shots=pBullets.filter(b=>b.kind==='spaceFusion').length;
  return {ok,shots,keys:Object.keys(window.__L.keys).filter(k=>/fusion|eglaser|lzr_g/.test(k)),url:document.querySelector('#screen').toDataURL('image/png')};}
"""
FIRE_COLE = r"""
()=>{
  run.stage=1;curStage=STAGES[0];beginStage(1);setState(GS.PLAY);player.reset();enemies.length=0;
  run.pilot='cole';run.weapon=0;run.wlevel=8;if(run.wlevels)run.wlevels[0]=8;window.__L.keys={};
  player._fuse=FUSE_FULL;coleFuseRelease();
  for(let i=0;i<10;i++){window.__bofStepNow+=1000/60;loop(window.__bofStepNow);}
  return {lances:pBullets.filter(b=>b.kind==='colefuse').length,keys:Object.keys(window.__L.keys).filter(k=>/fusion|eglaser|lzr_g/.test(k)),url:document.querySelector('#screen').toDataURL('image/png')};}
"""


def save(url, path):
    with open(path, 'wb') as fh: fh.write(base64.b64decode(url.split(',', 1)[1]))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--old', action='store_true'); ap.add_argument('--out', default='_shots/fusion_icons_1002')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'], **({'executable_path': chrome} if os.path.exists(chrome) else {}))
        pg = b.new_page(viewport={'width': 1100, 'height': 1200})
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        pg.on('response', lambda r: errs.append('HTTP %d %s' % (r.status, r.url)) if r.status >= 400 else None)
        if a.old:
            pg.route('**/assets/feedback_1002.js', lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* busted arm */'))
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(shoot.TRAP_RAF)
        for _ in range(4):
            ic = pg.evaluate(ICONS)
            if not any(v.get('miss') for v in ic.values()): break
            pg.wait_for_timeout(1500)
        sh = pg.evaluate(SHEET); save(sh['url'], os.path.join(a.out, 'icons_before_after.png'))
        print('space', pg.evaluate(SPACE)); pg.wait_for_timeout(1500)
        fs = pg.evaluate(FIRE_SPACE); save(fs.pop('url'), os.path.join(a.out, 'space_fusion.png')); print('space fusion', fs)
        pg.wait_for_timeout(800)
        fc = pg.evaluate(FIRE_COLE); save(fc.pop('url'), os.path.join(a.out, 'cole_fusion.png')); print('cole fusion', fc)
        b.close()
    stop()
    # the rule: ink height = the request, UNLESS the icon is wide enough that the width cap governs (ink width = box)
    bad_h = [(k, v['inkH']) for k, v in ic.items() if 'inkH' in v and abs(v['inkH'] - int(k.split('@')[1])) > 2 and abs(v['inkW'] - int(k.split('@')[1]) * 0.93) > 2]
    bad_w = [(k, v['inkW']) for k, v in ic.items() if 'inkW' in v and v['inkW'] > int(k.split('@')[1]) * 0.93 + 2]
    widths = {}
    for k, v in ic.items():
        if 'w' in v: widths.setdefault(k.split('@')[1], set()).add(round(v['w'], 1))
    print('icons measured', len(ic), 'ink height off', len(bad_h), bad_h[:6], 'too wide', len(bad_w), bad_w[:4], 'box widths', {k: sorted(s) for k, s in widths.items()})
    fz = [ic.get('space_fusion_icon_%d@64' % i, {}).get('inkH') for i in range(1, 6)]
    print('space fusion ink heights at 64:', fz, ' volley:', ic.get('space_volley_icon_3@64', {}).get('inkH'))
    if bad_h: fails.append('%d icons do not fill the unified height' % len(bad_h))
    if bad_w: fails.append('%d icons wider than the unified box' % len(bad_w))
    if any(len(s) != 1 for s in widths.values()): fails.append('icons report different box widths')
    if fs['shots'] < 1: fails.append('no space fusion round released')
    if 'fb2_fusion_beam' not in fs['keys'] or 'fusion30_beam' in fs['keys']: fails.append('space fusion did not draw the solid beam: %s' % fs['keys'])
    if fc['lances'] < 2: fails.append('Cole fusion cannon released %d lances' % fc['lances'])
    if 'fb2_fusion_beam' not in fc['keys'] or any(k.startswith('eglaser') or k.startswith('lzr_g') for k in fc['keys']): fails.append('Cole fusion cannon did not draw the solid beam: %s' % fc['keys'])
    print('errors', errs[:4])
    if errs: fails.append('page errors')
    print('FAIL' if fails else 'PASS', fails)


if __name__ == '__main__':
    main()
