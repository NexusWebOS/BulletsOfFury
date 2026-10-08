"""Native loader ownership inventory and bounded Canvas timing, using real BOF draws."""
from pathlib import Path
import json,sys,time,base64,http.server,argparse
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
args=argparse.ArgumentParser();args.add_argument('--phase',default='before');args=args.parse_args()
O=R/'_shots/asset_layout_1007'/args.phase;O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));report={'errors':[],'requests':[],'scenes':[]}
memory="""()=>{const seen=new Set(),urls=new Set();let count=0,bytes=0,uniqueBytes=0;for(const im of Object.values(XART.img)){if(!im||seen.has(im))continue;seen.add(im);const w=im.naturalWidth||im.width||0,h=im.naturalHeight||im.height||0;if(w>0&&h>0){count++;bytes+=w*h*4;if(!urls.has(im.src||im)){urls.add(im.src||im);uniqueBytes+=w*h*4;}}}return {images:count,rgbaReferenceBytes:bytes,uniqueURLs:urls.size,uniqueRGBAEstimate:uniqueBytes,rotationBytes:typeof ROT5!=='undefined'?ROT5.bytes:0,managed:typeof XART.memoryInfo==='function'?XART.memoryInfo():null};}"""
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':950});p.set_default_timeout(120000)
  p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort())
  p.on('pageerror',lambda e:report['errors'].append(str(e)))
  p.on('response',lambda r:report['errors'].append(str(r.status)+' '+r.url) if r.status>=400 and '127.0.0.1' in r.url else None)
  p.on('console',lambda m:report['errors'].append(m.text[:400]) if m.type=='error' and ('127.0.0.1' in m.text or 'ERR_' not in m.text) else None)
  p.on('request',lambda r:report['requests'].append(r.url.split(str(port)+'/',1)[-1]) if r.url.startswith(f'http://127.0.0.1:{port}/') else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(2500)
  report['boot']=p.evaluate(memory)
  report['bootTextures']=p.evaluate("""()=>Object.entries(XART.img).filter(([k,im])=>im&&(im.naturalWidth||im.width)>0).map(([key,im])=>({key,url:im.src,w:im.naturalWidth||im.width,h:im.naturalHeight||im.height})).sort((a,b)=>b.w*b.h-a.w*a.h)""")
  report['registry']=p.evaluate("""()=>({src:{...XART._src},cells:BOFX.cells,ships:BOFX.ships,playercells:BOFX.playercells,ecells:BOFX.ecells,pilots:PILOTS.map(p=>({key:p.key,name:p.name})),stages:STAGES.map(s=>({name:s.name,boss:s.boss})),roots:Object.fromEntries(Object.keys(XART._src).map(k=>[k,XART.root(k)]))})""")
  for name in ['balance_lab_1007.js','projectile_lab_1007.js']:p.add_script_tag(path=str(R/'_BUILD_SOURCE'/name))
  for stage,kind in ([] if args.phase=='snapshot' else [(1,'damkeeper'),(4,'stormsovereign'),(8,'vileexistence')]):
   c={'stage':stage,'kind':kind,'diff':'furious','pilot':'yuri','level':3,'id':'performance-'+str(stage)}
   p.evaluate('c=>AP7.begin(c)',c)
   deadline=time.monotonic()+110
   while time.monotonic()<deadline:
    p.evaluate('()=>stageLoadTick()');p.wait_for_timeout(30)
    if p.evaluate('()=>stageLoadInfo(run.stage).ready'):break
   p.evaluate('()=>AP7.step(120)');p.wait_for_timeout(300)
   timings=p.evaluate("""()=>{const a=[];for(let n=0;n<120;n++){const t=performance.now();updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);a.push(performance.now()-t);}a.sort((a,b)=>a-b);return {median:a[60],p95:a[114],max:a[119],ss:SS};}""")
   scene={'stage':stage,'timing':timings,'memory':p.evaluate(memory),'loading':p.evaluate('()=>stageLoadInfo(run.stage)'), 'geometry':p.evaluate('()=>AP7.geometry')}
   report['scenes'].append(scene);(O/f'stage-{stage}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
   print(json.dumps(scene),flush=True)
  queues={}
  for stage in range(1,10):queues[str(stage)]=p.evaluate('n=>{run.stage=n;delete _warmed[n];warmStage(n);return _stageLoads[n]?.keys||[];}',stage)
  report['registry']['stageQueues']=queues
  br.close()
finally:stop()
(O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(O/'registry.json').write_text(json.dumps(report['registry'],indent=2)+'\n',encoding='utf-8')
print('COMPLETE',json.dumps({'errors':report['errors'],'boot':report['boot']}),flush=True)
