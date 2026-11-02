"""Verify the expanded actors by actual XART/game-context pixels and gallery use."""
from pathlib import Path
import base64,json,hashlib
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/cast_performance_1102';O.mkdir(parents=True,exist_ok=True)
M=json.loads((R/'assets/game/shared/cinematics/cast_performance_1102/manifest.json').read_text())
checks=[];errors=[];missing=[]
def ck(name,ok,data=None):
    checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def shot(p,name):
    (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
    br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(120000)
    p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
    p.on('pageerror',lambda e:errors.append(str(e)))
    p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
    p.on('response',lambda r:missing.append(str(r.status)+' '+r.url) if r.status>=400 else None)
    p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
    for pilot,banks in M['pilots'].items():
      for group,bank in banks.items():
        keys=[f['key'] for f in bank['frames']]
        p.wait_for_function('keys=>keys.map(k=>XART.rdy(k)).every(Boolean)',arg=keys)
        stats=p.evaluate('''o=>{cv.width=3072;cv.height=2048;ctx.setTransform(1,0,0,1,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='rgb(13,37,71)';ctx.fillRect(0,0,cv.width,cv.height);
          return o.frames.map((f,i)=>{const x=i%4*768,y=Math.floor(i/4)*1024;const drawn=C112.draw(o.pilot,f.pose,x+384,y+960,1024);const a=ctx.getImageData(x,y,768,1024).data;let count=0,l=768,r=0,t=1024,b=0;
           for(let q=0;q<a.length;q+=4)if(a[q]!==13||a[q+1]!==37||a[q+2]!==71){const px=q/4%768,py=Math.floor(q/4/768);count++;l=Math.min(l,px);r=Math.max(r,px+1);t=Math.min(t,py);b=Math.max(b,py+1);}
           return {pose:f.pose,drawn,count,bounds:[l,t,r,b]};});}''',{'pilot':pilot,'frames':bank['frames']})
        for frame,s in zip(bank['frames'],stats):
          ck(pilot+' '+s['pose']+' paints complete native pixels',s['drawn'] and s['count']>10000 and all(abs(a-b)<=1 for a,b in zip(frame['bounds'],s['bounds'])),s)
        shot(p,pilot+'-'+group+'-native')
        if group=='movement':
          for gait in ['walk','run']:
            frames=[f for f in bank['frames'] if f['pose'].startswith(gait+'_')]
            ck(pilot+' '+gait+' has four distinct authored stride keys',len({f['sha256'] for f in frames})==4)
        p.wait_for_timeout(8)
      em={f['pose']:f for f in banks['emotion']['frames']}
      ck(pilot+' cheer is visibly airborne above the common ground',em['jump_cheer']['bounds'][3]<=860)
      ck(pilot+' floor laughter retains a lower body silhouette',em['floor_laugh']['bounds'][3]-em['floor_laugh']['bounds'][1]<em['happy']['bounds'][3]-em['happy']['bounds'][1])
    aliases=['fb1002_hammer_portrait','fb2_hammer_avatar','h3_hammer_portrait','cin30_cronos']
    p.wait_for_function('keys=>keys.concat(["cp112_chronos_dialogue"]).map(k=>XART.rdy(k)).every(Boolean)',arg=aliases)
    result=p.evaluate('''keys=>{cv.width=cv.height=512;ctx.setTransform(1,0,0,1,0,0);const paint=k=>{ctx.clearRect(0,0,512,512);ctx.drawImage(XART.get(k),0,0);return ctx.getImageData(0,0,512,512).data;};const expected=paint('cp112_chronos_dialogue');return keys.map(k=>{const a=paint(k);let diff=0;for(let i=0;i<a.length;i++)if(a[i]!==expected[i])diff++;return {key:k,differentBytes:diff};});}''',aliases)
    for s in result:ck(s['key']+' uses the framed dialogue closeup',s['differentBytes']==0,s)
    shot(p,'chronos-framed-native')
    for pilot,frame in M['ship_scenes'].items():
      p.wait_for_function('k=>XART.rdy(k)',arg=frame['key'])
      painted=p.evaluate('''k=>{cv.width=1536;cv.height=1024;ctx.setTransform(1,0,0,1,0,0);ctx.drawImage(XART.get(k),0,0);const a=ctx.getImageData(0,0,1536,1024).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]>35)n++;return n;}''',frame['key'])
      ck(pilot+' complete illustrated hangar scene paints natively',painted>700000,painted)
      shot(p,pilot+'-ship-native')
    p.goto((R/'docs/previews/cast_cinematics_1102/standalone.html').as_uri());p.wait_for_function('window.castReady')
    for pilot in M['pilots']:
      p.locator(f'[data-pilot="{pilot}"]').click()
      for cat,count,width in [('seated',6,768),('walk',4,768),('run',4,768),('emotion',8,768),('ship',1,1536),('classic',6,512)]:
        p.locator(f'[data-category="{cat}"]').click()
        p.wait_for_function('o=>{const images=Array.from(document.querySelectorAll("#poses img"));return images.length===o.count&&images.every(im=>im.complete&&im.naturalWidth===o.width&&im.naturalHeight===o.height);}',arg={'count':count,'width':width if cat=='ship' else width//2,'height':1024 if cat=='ship' else 512})
        ck(pilot+' '+cat+' standalone gallery has every complete frame',p.locator('#poses img').count()==count)
      p.locator('[data-category="walk"]').click()
      p.locator('#motion').scroll_into_view_if_needed()
      hashes=[]
      for i in range(4):
        p.wait_for_timeout(180);hashes.append(hashlib.sha256(p.evaluate('document.getElementById("stride").toDataURL()').encode()).hexdigest())
      ck(pilot+' gallery stride loop changes actual pixels',len(set(hashes))>1)
    p.locator('[data-pilot="falva"]').click();p.locator('[data-category="emotion"]').click();p.locator('[data-bg="light"]').click();p.locator('#poses').scroll_into_view_if_needed();p.screenshot(path=str(O/'gallery-falva-emotions-light.png'))
    p.locator('[data-category="ship"]').click();p.locator('#poses').scroll_into_view_if_needed();p.screenshot(path=str(O/'gallery-falva-ship.png'))
    p.set_viewport_size({'width':390,'height':844});p.locator('[data-category="seated"]').click()
    ck('Expanded mobile gallery has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    p.screenshot(path=str(O/'gallery-mobile.png'),full_page=True)
    ck('No page or console errors',not errors,errors);ck('No missing network assets',not missing,missing);br.close()
finally:stop()
# Review sheets contain the actual renderer captures, not a substitute renderer.
for group in ['movement','seated','emotion']:
    board=Image.new('RGB',(1536,1026),'#142333');draw=ImageDraw.Draw(board)
    for i,pilot in enumerate(M['pilots']):
      im=Image.open(O/(pilot+'-'+group+'-native.png')).resize((512,342),Image.Resampling.LANCZOS);x=i%3*512;y=i//3*342;board.paste(im,(x,y));draw.text((x+12,y+8),pilot.upper(),fill='white')
    board.save(O/('all-'+group+'-native.jpg'),quality=95)
report={'passed':sum(c['passed'] for c in checks),'total':len(checks),'errors':errors,'missing':missing,'checks':checks}
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');(R/'docs/qa/cast_performance_1102.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}));raise SystemExit(not all(c['passed'] for c in checks))
