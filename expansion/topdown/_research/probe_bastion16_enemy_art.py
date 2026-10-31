"""Native ART.draw review of every new Level 7 enemy and Yuri frame."""
from pathlib import Path
import json,sys
from PIL import Image
import numpy as np
from scipy.ndimage import label
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/bastion16_enemies'
OUT.mkdir(exist_ok=True)
errors=[];checks=[]
def check(name,v):checks.append({'name':name,'passed':bool(v)});print(('PASS ' if v else 'FAIL ')+name,flush=True)
packs={name:json.loads((ROOT/f'expansion/topdown/art/bastion16_{name}/manifest.json').read_text()) for name in ('enemies','yuri')}
for name,p in packs.items():
    stats=[]
    for key,m in p['assets'].items():
        im=Image.open(ROOT/m['file']).convert('RGBA');a=np.asarray(im)[:,:,3];b=im.getchannel('A').getbbox()
        labs,n=label(a>0,np.ones((3,3)))
        counts=np.bincount(labs.ravel())[1:]
        extras=sorted([int(c) for c in counts],reverse=True)[1:]
        stats.append({'key':key,'alpha':sorted(int(v) for v in np.unique(a)), 'even':im.width%2==0 and im.height%2==0,
           'safe':bool(b and b[0]>0 and b[1]>0 and b[2]<im.width and b[3]<im.height),
           'components':int(n),'extraPixels':sum(extras),'sizeMatches':list(im.size)==m['size'],
           'muzzleInBounds':not m.get('muzzle') or (b[0]-3<=m['muzzle'][0]<=b[2]+3 and b[1]-3<=m['muzzle'][1]<=b[3]+3)})
    check(name+' all even fixed declared sizes',all(x['even'] and x['sizeMatches'] for x in stats))
    check(name+' hard alpha and safe gutters',all(x['safe'] and set(x['alpha']).issubset({0,255}) for x in stats))
    check(name+' muzzles lie on authored silhouette bounds',all(x['muzzleInBounds'] for x in stats))
    (OUT/(name+'_pixel_audit.json')).write_text(json.dumps(stats,indent=2))

port,stop=shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch()
        p=browser.new_page(viewport={'width':1400,'height':950})
        p.on('pageerror',lambda e:errors.append(str(e)))
        p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',timeout=90000)
        p.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000)
        p.evaluate('TDGAME.freeze()')
        p.evaluate('''packs=>{window.reviewPacks=packs;for(const pack of Object.values(packs)){Object.assign(TD_ASSAULT_ART.assets,pack.assets);Object.assign(TD_ASSAULT_ART.sequences,pack.sequences);}window.reviewKeys=Object.values(packs).flatMap(pack=>Object.keys(pack.assets));ART.warm(reviewKeys);}''',packs)
        p.wait_for_function('ART.progress(reviewKeys)===1',timeout=90000)
        check('all216 new enemy and Yuri frames decode through real ART',p.evaluate('reviewKeys.length===216&&reviewKeys.every(k=>!!ART.get(k))'))
        p.evaluate('''()=>{document.body.style.display='block';document.body.style.overflow='auto';document.querySelector('#screen').style.display='none';document.querySelector('#fs-btn').style.display='none';window.review=document.createElement('canvas');review.id='review';review.width=1280;review.height=850;document.body.appendChild(review);}''')
        for name,pack in packs.items():
            groups=list(pack['sequences'].items())
            for start in range(0,len(groups),4):
                names=[k for k,v in groups[start:start+4]]
                p.evaluate('''({name,names})=>{const ctx=review.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.fillStyle='#18202b';ctx.fillRect(0,0,1280,850);ctx.font='12px monospace';names.forEach((bank,row)=>{const seq=reviewPacks[name].sequences[bank];seq.frames.forEach((key,col)=>{const m=reviewPacks[name].assets[key],x=70+col*154,y=180+row*208;TD.AssaultArt.draw(ctx,key,x,y,{s:m.drawScale||1});ctx.fillStyle='#bcc4ce';ctx.fillText(key.replace('pb16_',''),col*154+3,row*208+23);if(m.muzzle){const mx=x+(m.muzzle[0]-m.anchor[0])*(m.drawScale||1),my=y+(m.muzzle[1]-m.anchor[1])*(m.drawScale||1);ctx.strokeStyle='#ff4778';ctx.beginPath();ctx.moveTo(mx-3,my);ctx.lineTo(mx+3,my);ctx.moveTo(mx,my-3);ctx.lineTo(mx,my+3);ctx.stroke();}});});}''',{'name':name,'names':names})
                p.locator('#review').screenshot(path=str(OUT/f'native_{name}_{start//4}.png'))
        check('no native browser errors',not errors)
        browser.close()
finally:stop()
report={'checks':checks,'errors':errors,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),
        'note':'Native review includes pink QA muzzle markers; markers are not game sprites.'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
sys.exit(0 if not errors and all(x['passed'] for x in checks) else 1)
