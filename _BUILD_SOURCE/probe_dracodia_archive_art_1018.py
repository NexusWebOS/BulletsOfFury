"""Render archive banks through the real game's XART and native drawImage."""
from pathlib import Path
import ast,base64,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];fixture='--fixture' in sys.argv;O=R/'_shots/dracodia_archive_1018/art';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof V19!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  if fixture:
   p.add_script_tag(url=f'http://127.0.0.1:{port}/_shots/dracodia_archive_1018/fixture_art.js')
   p.evaluate('D20_ART.fx={}')
   p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/dracodia_archive_1018.js')
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate(SETUP,dict(stage=8,diff='normal',kind='vileexistence',pilot='cole'))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&d20Warm()&&bmfReady("game")}')
  p.evaluate('''()=>{window.archiveArtPixels=input=>{const list=Array.isArray(input)?input:[input],a=list[0];ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.clearRect(0,0,cv.width,cv.height);for(const q of list)d20Art(q,q.w/2,q.h/2,q.w);const v=ctx.getImageData(0,0,a.w,a.h);ctx.restore();return v;};window.archiveArtPng=a=>{const c=document.createElement('canvas');c.width=a.w;c.height=a.h;c.getContext('2d').putImageData(archiveArtPixels(a),0,0);return c.toDataURL('image/png').split(',')[1];};}''')
  for kind in ['spear','brood']:
   png=p.evaluate('(kind)=>archiveArtPng(d20Model(kind).full)',kind);(O/(kind+'-native.png')).write_bytes(base64.b64decode(png))
   check(kind+' original art loads through native XART',bool(png))
  models=p.evaluate('Object.keys(D20_ART.models)')
  for name in models:
   data=p.evaluate('''name=>{const m=D20_ART.models[name],whole=archiveArtPixels(m.full).data,combined=archiveArtPixels(Object.values(m.parts)).data;let error=0;for(let i=0;i<whole.length;i++)if(whole[i]!==combined[i])error++;return{error,parts:Object.keys(m.parts),mounts:m.mounts,muzzles:m.muzzles};}''',name)
   check(name+' native module pixels reassemble the exact hull',data['error']==0 and len(data['parts'])==3,data)
   png=p.evaluate('(name)=>archiveArtPng(D20_ART.models[name].full)',name);(O/(name+'-native.png')).write_bytes(base64.b64decode(png))
  if not fixture:
   banks=p.evaluate('''()=>Object.fromEntries([...Object.entries(D20_ART.models).map(([k,m])=>[k+'_download',m.download]),...Object.entries(D20_ART.fx).map(([k,b])=>[k,b.frames])].map(([k,frames])=>[k,frames.map(a=>a.key)]))''')
   for name,keys in banks.items():
    rows=[]
    for start in range(0,len(keys),8):
     rows+=p.evaluate('''keys=>keys.map(key=>{const a=[...Object.values(D20_ART.models).flatMap(m=>m.download),...Object.values(D20_ART.fx).flatMap(b=>b.frames)].find(a=>a.key===key),v=archiveArtPixels(a).data;let hash=2166136261,pixels=0,edge=0;for(let i=0;i<v.length;i++){hash=Math.imul(hash^v[i],16777619)>>>0;if(i%4===3&&v[i-3]+v[i-2]+v[i-1]>24){pixels++;const p=(i-3)/4,x=p%a.w,y=Math.floor(p/a.w);if(x===0||y===0||x===a.w-1||y===a.h-1)edge++;}}return{key,hash,pixels,edge,w:a.w,h:a.h,pivot:a.pivot};})''',keys[start:start+8]);p.wait_for_timeout(5)
    check(name+' has at least 16 distinct native frames on fixed even geometry',16<=len(rows)<=32 and len({r['hash'] for r in rows})>=len(rows)-1 and len({(r['w'],r['h'],tuple(r['pivot'])) for r in rows})==1 and all(r['w']%2==0 and r['h']%2==0 for r in rows),rows)
    check(name+' has no clipped edge pixels',all(r['edge']==0 for r in rows),[r for r in rows if r['edge']])
  check('no page, console, drawing or missing art errors',not errors,errors[:30]);br.close()
finally:stop()
data=dict(fixture=fixture,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:data[k] for k in ['passed','failed','errors']}));sys.exit(bool(data['failed']))
