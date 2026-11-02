"""Native Chromium pixels for all cast assets and actual Chronos dialogue routes."""
from pathlib import Path
import ast, base64, hashlib, json
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
import shoot

R=Path(__file__).resolve().parents[1]
O=R/'_shots/cast_cinematics_1102'
O.mkdir(parents=True,exist_ok=True)
M=json.loads((R/'assets/game/shared/cinematics/cast_1102/manifest.json').read_text())
checks=[]; errors=[]; failed_requests=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
def ck(name,ok,data=None):
    checks.append({'name':name,'passed':bool(ok),'data':data})
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def save(p,name):
    (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
port,stop=shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
        p=b.new_page(viewport={'width':1366,'height':768})
        p.set_default_timeout(120000)
        p.on('pageerror',lambda e:errors.append(str(e)))
        p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
        p.on('response',lambda r:failed_requests.append(str(r.status)+' '+r.url) if r.status>=400 else None)
        p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
        p.goto(f'http://127.0.0.1:{port}/index.html')
        p.wait_for_function('window.__bofFrames>4')
        p.evaluate(shoot.TRAP_RAF)
        p.evaluate('()=>{window.castOriginalCanvas={w:cv.width,h:cv.height};}')
        pilot_names=list(M['pilots'])
        for pilot,bank in M['pilots'].items():
            p.wait_for_function('p=>Object.values(C112.art.pilots[p]).map(k=>XART.rdy(k)).every(Boolean)',arg=pilot)
            result=p.evaluate('''p=>{cv.width=3072;cv.height=1024;ctx.setTransform(1,0,0,1,0,0);ctx.imageSmoothingEnabled=false;
                ctx.fillStyle='rgb(13,37,71)';ctx.fillRect(0,0,cv.width,cv.height);
                const stats=[];for(let i=0;i<C112.poses.length;i++){
                    const pose=C112.poses[i],key=C112.key(p,pose);C112.draw(p,pose,i*512+256,976,1024);
                    const a=ctx.getImageData(i*512,0,512,1024).data;let n=0,l=512,r=0,t=1024,b=0,redMatte=0;
                    for(let q=0;q<a.length;q+=4)if(a[q]!==13||a[q+1]!==37||a[q+2]!==71){const x=q/4%512,y=Math.floor(q/4/512);n++;l=Math.min(l,x);r=Math.max(r,x+1);t=Math.min(t,y);b=Math.max(b,y+1);}
                    stats.push({pose,key,n,bounds:[l,t,r,b],redMatte});
                }ctx.globalCompositeOperation='destination-over';ctx.fillStyle='#142333';ctx.fillRect(0,0,cv.width,cv.height);ctx.globalCompositeOperation='source-over';return stats;}''',pilot)
            for f,stats in zip(bank['frames'],result):
                ck(pilot+' '+f['pose']+' paints complete registered native pixels',stats['n']>60000 and all(abs(a-b)<=1 for a,b in zip(stats['bounds'],f['bounds'])),stats)
            save(p,pilot+'-native')
            p.wait_for_timeout(10)
        keys=[f['key'] for f in M['chronos']['frames']]
        p.wait_for_function('keys=>keys.map(k=>XART.rdy(k)).every(Boolean)',arg=keys)
        stats=p.evaluate('''keys=>{cv.width=2048;cv.height=512;ctx.setTransform(1,0,0,1,0,0);const out=[];
            for(let i=0;i<keys.length;i++){ctx.drawImage(XART.get(keys[i]),i*512,0);const a=ctx.getImageData(i*512,0,512,512).data;
                let blue=0,opaque=0;for(let q=0;q<a.length;q+=4){if(a[q+3]>32)opaque++;if(a[q+2]>150&&a[q+2]>a[q]*1.5&&a[q+3]>100)blue++;}out.push({key:keys[i],blue,opaque});}
            ctx.globalCompositeOperation='destination-over';ctx.fillStyle='#142333';ctx.fillRect(0,0,cv.width,cv.height);ctx.globalCompositeOperation='source-over';return out;}''',keys)
        for s in stats:ck(s['key']+' paints blue visor and complete helm',s['blue']>1000 and s['opaque']>60000,s)
        save(p,'chronos-native')
        aliases=['fb1002_hammer_portrait','fb2_hammer_avatar','h3_hammer_portrait','cin30_cronos']
        p.wait_for_function('keys=>keys.map(k=>XART.rdy(k)).every(Boolean)',arg=aliases)
        alias_stats=p.evaluate('''keys=>{cv.width=cv.height=512;ctx.setTransform(1,0,0,1,0,0);
            const bytes=k=>{ctx.clearRect(0,0,512,512);ctx.drawImage(XART.get(k),0,0);return ctx.getImageData(0,0,512,512).data;};
            const expected=bytes(C112.art.chronos.neutral);return keys.map(k=>{const a=bytes(k);let diff=0;for(let i=0;i<a.length;i++)if(a[i]!==expected[i])diff++;return {key:k,differentBytes:diff};});}''',aliases)
        for s in alias_stats:ck(s['key']+' resolves new avatar through actual pixels',s['differentBytes']==0,s)
        # Preserve the native terminal portrait whitening owner through the new alias.
        fade=p.evaluate('''()=>{const original=H3.ending;try{H3.ending={sm10:{portrait:0}};
            const pixel=()=>{ctx.clearRect(0,0,512,512);ctx.drawImage(XART.get('sm10_hammer_portrait'),0,0);return Array.from(ctx.getImageData(256,300,1,1).data);};
            const before=pixel();H3.ending.sm10.portrait=1;const after=pixel();return {before,after};}finally{H3.ending=original;}}''')
        ck('Native ending portrait whitening still applies',sum(fade['after'][:3])>sum(fade['before'][:3])+100,fade)
        p.evaluate('()=>{cv.width=castOriginalCanvas.w;cv.height=castOriginalCanvas.h;ctx.setTransform(SS,0,0,SS,0,0);UI20.warm();}')
        p.wait_for_function('()=>UI20_KEYS.every(k=>XART.rdy(k))&&bmfReady("dialogue")')
        p.evaluate('()=>{run.pilot="cole";BOFCinematicDirector.preview("cronos","cole");}')
        first=p.evaluate('()=>BOFCinematicDirector.current.beats.findIndex(b=>/^CHRONOS$/i.test(b.who))')
        p.evaluate('i=>{const s=BOFCinematicDirector.current;s.i=i;s.shown=s.beats[i].text.length;}',first)
        p.wait_for_function('()=>{const b=BOFCinematicDirector.current.beats[BOFCinematicDirector.current.i];return XART.rdy(BOFCinematicDirector.artFor(b))&&XART.rdy("bg_stage05_loop_0923");}')
        p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);BOFCinematicDirector.draw();}')
        save(p,'chronos-first-contact')
        ck('First contact uses new native Chronos portrait',p.evaluate('UI20.dialogue.portrait==="cin30_cronos"'),p.evaluate('UI20.dialogue.portrait'))
        p.evaluate('()=>{BOFCinematicDirector.cancel();setState(GS.PLAY);ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#142333";ctx.fillRect(0,0,VW,VH);dlgBox({who:"CHRONOS",portrait:false,portraitKey:"fb1002_hammer_portrait",full:"Such a foolish mortal. Now, let us dance!",shown:"Such a foolish mortal. Now, let us dance!",pw:460,ph:132,x:10,y:360,screenSpace:false});}')
        save(p,'chronos-dialogue-native')
        # Use the existing native entry and speech owner as a short regression.
        p.evaluate(SETUP,{'stage':5,'pilot':'cole'})
        p.evaluate('()=>{spawnBoss(curStage.boss);fb1002HammerDialogue(boss);}')
        ck('Native trap dialogue retains both authored Chronos lines',p.evaluate('()=>{const s=BOFCinematicDirector.current;return s.id==="hammer-trap1002"&&s.beats.length===2&&s.beats.every(b=>b.art==="fb1002_hammer_portrait");}'))
        p.evaluate('()=>BOFCinematicDirector.cancel()')
        ck('Gameplay reset does not replace pilot portrait identities',p.evaluate('()=>PILOTS.every(p=>!/^c112/.test(pilotPortrait(p.key,"idle")))'))
        p.goto(f'http://127.0.0.1:{port}/docs/previews/cast_cinematics_1102/index.html')
        p.wait_for_function('window.castReady')
        for pilot in pilot_names:
            p.locator(f'button[data-pilot="{pilot}"]').click()
            p.wait_for_function('()=>Array.from(document.querySelectorAll("#poses img")).every(im=>im.complete&&im.naturalWidth===512&&im.naturalHeight===1024)')
            ck(pilot+' gallery loads all six complete frames',p.locator('#poses img').count()==6)
        p.locator('button[data-pilot="lizzie"]').click()
        p.locator('[data-bg="light"]').click()
        p.locator('#poses').scroll_into_view_if_needed()
        p.screenshot(path=str(O/'gallery-light.png'))
        p.set_viewport_size({'width':390,'height':844})
        ck('Mobile gallery has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        p.screenshot(path=str(O/'gallery-mobile.png'),full_page=True)
        p.goto((R/'docs/previews/cast_cinematics_1102/standalone.html').as_uri())
        p.wait_for_function('window.castReady')
        p.locator('button[data-pilot="freezer"]').click()
        p.locator('#poses').scroll_into_view_if_needed()
        p.wait_for_function('()=>Array.from(document.querySelectorAll("#poses img")).every(im=>im.complete&&im.naturalWidth===512&&im.naturalHeight===1024)')
        ck('Standalone local gallery works without an HTTP server',p.evaluate('()=>location.protocol==="file:"&&Array.from(document.querySelectorAll("#poses img")).every(im=>im.src.startsWith("data:image/png;base64,"))'))
        ck('No page or console errors',not errors,errors)
        ck('No missing network assets',not failed_requests,failed_requests)
        b.close()
finally:
    stop()
report={'passed':sum(c['passed'] for c in checks),'total':len(checks),'errors':errors,'failed_requests':failed_requests,'checks':checks}
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
(R/'docs/qa/cast_cinematics_1102.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
raise SystemExit(not all(c['passed'] for c in checks))
