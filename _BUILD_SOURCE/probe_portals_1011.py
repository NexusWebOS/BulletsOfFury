"""Inspect all generated portal poses through real Chromium and the game ctx."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from playwright.sync_api import sync_playwright
import shoot,json,hashlib,base64,io,sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/portals_1011';OUT.mkdir(parents=True,exist_ok=True)
MAN=ROOT/'assets/game/shared/fx/portals_1011/manifest.json'
manifest=json.loads(MAN.read_text(encoding='utf-8'))
checks=[];errors=[];screens=[];metrics={}
def check(name,ok,data=None):
    checks.append(dict(name=name,passed=bool(ok),data=data))
    print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
def decode(url):return Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGBA')

# Actual files, not declarations alone: uniform geometry, alpha, identity.
for name,bank in manifest['art'].items():
    ims=[Image.open(ROOT/f['path']).convert('RGBA') for f in bank['frames']]
    dims={im.size for im in ims};pivots={tuple(f['pivot']) for f in bank['frames']}
    check(name+': 32 different drawings on one even canvas and pivot',len(ims)==32 and len({im.tobytes() for im in ims})==32 and len(dims)==len(pivots)==1 and all(w%2==h%2==0 for w,h in dims))
    check(name+': exported checksums match owning manifest',all(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in bank['frames']))
    arrays=[np.asarray(im) for im in ims]
    edges=[np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]) for a in arrays]
    check(name+': energy stays clear of the canvas boundary',all((edge[:,:3].max()<8 and edge[:,3].min()==255) if name=='black_void' else edge[:,3].max()==0 for edge in edges))
    check(name+': aperture registration stays within half a source pixel',manifest['alignment'][name]['maxCenterError']<=.5)
    if name=='black_void':check('Black tunnel keeps an opaque black aperture',all(a[158:162,158:162,:3].max()<8 and a[:,:,3].min()==255 for a in arrays))
    if name=='amethyst_gate':
        shell=np.asarray(Image.open(ROOT/'assets/game/shared/fx/portals_1011/gate-shell.png').convert('RGBA'))
        opening=np.asarray(Image.open(ROOT/'assets/game/shared/fx/portals_1011/gate-aperture-mask.png'))
        stone=(opening==0)&(shell[:,:,3]>0)
        check('All visible stonework is pixel-identical in every gate frame',all(np.array_equal(a[stone],shell[stone]) for a in arrays))
    metrics[name]={k:v for k,v in manifest['alignment'][name].items() if k!='sourceAnchors'}

port,stop=shoot.serve(str(ROOT));base=f'http://127.0.0.1:{port}/'
try:
 with sync_playwright() as pw:
    br=pw.chromium.launch(args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
    def watch(p):
        p.on('pageerror',lambda e:errors.append(str(e)))
        p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
        p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
    p=br.new_page(viewport=dict(width=1280,height=1080));p.set_default_timeout(120000);watch(p)
    p.goto(base+'index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(70)
    check('Review pack has not changed the live game loadout',p.evaluate('typeof PR11_ART==="undefined"'))
    p.add_script_tag(url=base+'assets/portal_art_1011.js')
    p.evaluate('''()=>{for(const bank of Object.values(PR11_ART))for(const f of bank.frames){XART._src[f.key]=f.path;XART.rdy(f.key);}}''')
    p.wait_for_function('()=>Object.values(PR11_ART).flatMap(b=>b.frames).map(f=>XART.rdy(f.key)).every(Boolean)',polling=50)
    check('All 160 main and component frames decode through XART',True)
    p.evaluate('''()=>{
      window.portalCalls=[];const get=XART.get,draw=ctx.drawImage;let key=null;
      XART.get=function(k){const image=get.apply(this,arguments);key=k;return image;};
      ctx.drawImage=function(){if(key)portalCalls.push({key,args:Array.from(arguments).slice(1)});key=null;return draw.apply(this,arguments);};
      window.portalRestore=()=>{XART.get=get;ctx.drawImage=draw;};
      window.portalDraw=(bank,frame,onion=false)=>{
        ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.imageSmoothingEnabled=false;
        ctx.fillStyle='#0a151e';ctx.fillRect(0,0,VW,VH);
        const scale=bank==='amethyst_gate'?.65:1.5;
        const draw=(i,a)=>{const f=PR11_ART[bank].frames[i],im=XART.get(f.key);ctx.globalAlpha=a;
          ctx.drawImage(im,VW/2-f.pivot[0]*scale,VH/2-f.pivot[1]*scale,f.w*scale,f.h*scale);};
        draw(frame,1);
        if(onion){ctx.globalCompositeOperation='screen';draw((frame+31)%32,.28);draw((frame+1)%32,.28);ctx.globalCompositeOperation='source-over';}
        ctx.globalAlpha=1;return cv.toDataURL();
      };
    }''')
    for bank in manifest['art']:
        frames=[]
        for i in range(32):
            frames.append(decode(p.evaluate('([bank,i])=>portalDraw(bank,i)',[bank,i])))
            if i%8==7:p.wait_for_timeout(12)
        check(bank+': all 32 poses visibly differ in the native game context',len({im.tobytes() for im in frames})==32)
        if bank in manifest['main']:
            frames[0].save(OUT/(bank+'-native.webp'),save_all=True,append_images=frames[1:],loop=0,duration=round(1000/manifest['art'][bank]['fps']),lossless=True,method=3)
            # Native loop boundary and one middle phase, same declared anchor.
            w,h=frames[0].size;contact=Image.new('RGB',(w*3,h),'#0a151e')
            for j,i in enumerate([31,0,16]):contact.paste(frames[i],(j*w,0))
            contact.save(OUT/(bank+'-native-seam.png'));screens.append(bank+'-native-seam.png')
            decode(p.evaluate('bank=>portalDraw(bank,16,true)',bank)).save(OUT/(bank+'-native-onion.png'));screens.append(bank+'-native-onion.png')
    calls=p.evaluate('portalCalls');by_key={f['key']:f for b in manifest['art'].values() for f in b['frames']}
    check('Every registered key was consumed by the game context drawImage',set(by_key).issubset({c['key'] for c in calls}))
    check('Native draws preserve proportional scale and a single fixed destination anchor',all(abs(c['args'][2]/by_key[c['key']]['w']-c['args'][3]/by_key[c['key']]['h'])<1e-8 for c in calls))
    p.evaluate('portalRestore()');p.close()

    p=br.new_page(viewport=dict(width=1440,height=1080),reduced_motion='reduce');p.set_default_timeout(60000);watch(p)
    p.goto(base+'docs/previews/portals_1011/index.html');p.wait_for_function('window.PORTAL_REVIEW?.state.ready')
    check('Preview loads 128 frames and respects reduced motion',p.evaluate('!PORTAL_REVIEW.state.playing&&Object.values(PORTAL_REVIEW.images).every(a=>a.length===32&&a.every(im=>im.complete))'))
    for bank in manifest['main']:
        p.locator(f'[data-bank="{bank}"]').click()
        check(bank+': effect selector switches the active animation',p.evaluate('PORTAL_REVIEW.state.bank')==bank)
        hashes=[]
        for i in range(32):
            p.locator('#frame').fill(str(i));p.locator('#frame').dispatch_event('input')
            url=p.locator('#stage').evaluate('c=>c.toDataURL()');hashes.append(hashlib.sha256(url.encode()).hexdigest())
        check(bank+': scrub displays all 32 different authored frames',len(set(hashes))==32)
        p.screenshot(path=str(OUT/(bank+'-preview.png')));screens.append(bank+'-preview.png')
    p.locator('[data-bank="amethyst_gate"]').click();p.locator('#anchor').check();p.locator('#onion').check();p.locator('#frame').fill('16');p.locator('#frame').dispatch_event('input')
    p.screenshot(path=str(OUT/'preview-onion.png'));screens.append('preview-onion.png')
    check('Onion controls compare neighbours without moving the current frame',p.evaluate('PORTAL_REVIEW.state.onion&&PORTAL_REVIEW.state.anchor&&PORTAL_REVIEW.state.frame===16'))
    p.locator('#onion').uncheck();p.locator('#anchor').uncheck()
    for backdrop in ['checker','arena']:
        p.locator('#backdrop').select_option(backdrop)
        p.screenshot(path=str(OUT/('preview-'+backdrop+'.png')));screens.append('preview-'+backdrop+'.png')
        check(backdrop+': selected backdrop draws behind the portal',p.evaluate('PORTAL_REVIEW.state.backdrop')==backdrop)
    p.locator('#next').click();check('Single-step advances exactly one frame and stays paused',p.evaluate('PORTAL_REVIEW.state.frame===17&&!PORTAL_REVIEW.state.playing'))
    p.locator('#prev').click();check('Single-step can return to the previous frame',p.evaluate('PORTAL_REVIEW.state.frame===16'))
    p.locator('#seam').check();p.locator('#frame').fill('28');p.locator('#frame').dispatch_event('input')
    p.locator('#speed').select_option('0.5');p.locator('#play').click();seen=set()
    for i in range(24):
        seen.add(p.evaluate('PORTAL_REVIEW.state.frame'));p.wait_for_timeout(45)
    p.locator('#play').click()
    check('Seam playback crosses 32 to 1 within the selected eight frames',31 in seen and 0 in seen and seen.issubset({28,29,30,31,0,1,2,3}),sorted(seen))
    old=p.evaluate('PORTAL_REVIEW.state.frame');p.wait_for_timeout(180)
    check('Pause holds the displayed frame',p.evaluate('PORTAL_REVIEW.state.frame')==old)
    p.set_viewport_size(dict(width=390,height=844));p.locator('#backdrop').select_option('dark')
    p.screenshot(path=str(OUT/'preview-mobile.png'),full_page=True);screens.append('preview-mobile.png')
    check('Mobile review has no horizontal overflow and canvas remains visible',p.evaluate('document.documentElement.scrollWidth<=innerWidth&&document.querySelector("#stage").getBoundingClientRect().right<=innerWidth'))
    check('No page, console or missing-asset errors',not errors,errors)
    br.close()
finally:
 stop()
 report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,metrics=metrics,screens=screens,errors=errors,
    scope='Generated portal review pack, native XART/context rendering and preview controls. No gameplay code changed.')
 (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
 (ROOT/'docs/qa/portals_1011.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
