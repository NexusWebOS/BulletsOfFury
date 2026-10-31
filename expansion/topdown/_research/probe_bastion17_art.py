"""Serial native ART asset audit for all three new Level7 packs."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/bastion17_enemies';OUT.mkdir(exist_ok=True)
checks=[];errors=[];stats=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS ' if v else 'FAIL ')+name,flush=True)
packs={n:json.loads((ROOT/f'expansion/topdown/art/bastion17_{n}/manifest.json').read_text()) for n in ('enemies','environment','yuri')}
for name,pack in packs.items():
    rows=[]
    for k,m in pack['assets'].items():
        im=Image.open(ROOT/m['file']).convert('RGBA');a=np.asarray(im)[:,:,3];b=im.getchannel('A').getbbox()
        rows.append({'key':k,'even':im.width%2==0 and im.height%2==0,'matches':list(im.size)==m['size'],
           'hard':set(np.unique(a)).issubset({0,255}),'bounds':b,
           'safe':bool(b and (k.startswith('pb17_stage_') or b[0]>0 and b[1]>0 and b[2]<im.width and b[3]<im.height))})
    check(name+' even declared sizes',all(x['even'] and x['matches'] for x in rows))
    check(name+' opaque pixels and safe gutters',all(x['safe'] and x['hard'] for x in rows))
    stats+=rows
port,stop=shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch();p=browser.new_page(viewport={'width':1320,'height':790})
        p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=90000)
        p.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000);p.evaluate('TDGAME.freeze()')
        p.evaluate('''packs=>{window.reviewPacks=packs;window.reviewAssets=Object.assign({},...Object.values(packs).map(p=>p.assets));window.reviewKeys=Object.keys(reviewAssets);ART.warm(reviewKeys);}''',packs)
        p.wait_for_function('ART.progress(reviewKeys)===1',timeout=90000)
        check('all109 assets decode through live ART registry',p.evaluate('reviewKeys.length===109&&reviewKeys.every(k=>!!ART.get(k))'))
        p.evaluate('''()=>{document.body.style.display='block';document.body.style.overflow='auto';document.querySelector('#screen').style.display='none';document.querySelector('#fs-btn').style.display='none';window.review=document.createElement('canvas');review.id='review';review.width=1280;review.height=720;document.body.appendChild(review);}''')
        for page in range(4):
            p.evaluate('''page=>{const c=review.getContext('2d');c.imageSmoothingEnabled=false;c.fillStyle='#18202b';c.fillRect(0,0,1280,720);c.font='10px monospace';reviewKeys.slice(page*32,(page+1)*32).forEach((key,index)=>{const m=reviewAssets[key],b=m.bounds,cx=index%8*160,cy=Math.floor(index/8)*180,s=Math.min(m.drawScale||1,148/(b[2]-b[0]),148/(b[3]-b[1]));const x=cx+80-((b[0]+b[2])/2-m.anchor[0])*s,y=cy+22+(148-(b[3]-b[1])*s)/2-(b[1]-m.anchor[1])*s;TD.AssaultArt.draw(c,key,x,y,{s});c.fillStyle='#c6d0db';c.fillText(key.replace('pb17_',''),cx+3,cy+12);if(m.muzzle){const mx=x+(m.muzzle[0]-m.anchor[0])*s,my=y+(m.muzzle[1]-m.anchor[1])*s;c.strokeStyle='#ff4778';c.beginPath();c.moveTo(mx-2,my);c.lineTo(mx+2,my);c.moveTo(mx,my-2);c.lineTo(mx,my+2);c.stroke();}});}''',page)
            p.locator('#review').screenshot(path=str(OUT/f'native_all_{page}.png'))
        check('zero native browser errors',not errors);browser.close()
finally:stop()
result={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,'errors':errors,'assets':len(stats)}
(OUT/'pixel_audit.json').write_text(json.dumps(stats,indent=2));(OUT/'verification.json').write_text(json.dumps(result,indent=2))
(ROOT/'docs/qa/overdrive_bastion17_art.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2));sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
