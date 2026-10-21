from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import sys,json,base64,hashlib,io,http.server
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot,probe_tutorial_1015 as old
O=R/'_shots/stormglass_water_pixellab_1020';O.mkdir(exist_ok=True)
meta=json.loads((R/'assets/game/levels/tutorial/stormglass_1020/water/ocean.json').read_text(encoding='utf-8'))
sheet=Image.open(R/meta['path']).convert('RGBA');checks=[];errors=[];requests=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));print(('PASS ' if passed else 'FAIL ')+name,flush=True)
def shot(p,name):
 data=base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]'));(O/(name+'.png')).write_bytes(data);return Image.open(io.BytesIO(data)).convert('RGB')
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(120000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.on('request',lambda r:requests.append(r.url) if '/water/ocean.webp' in r.url else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof ht27Stop==="function"');p.evaluate(shoot.TRAP_RAF)
  ck('New water texture stays off the title/boot download path',not requests,requests)
  p.evaluate(old.SETUP,dict(pilot='cole',mode='arcade',clear=True));p.evaluate('startRun(1)');p.evaluate(old.STEPN,40);p.evaluate('Input.injectTap("j")');p.evaluate(old.STEPN,5)
  p.wait_for_function('BOFSTORMGLASS.artReady');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}')
  for _ in range(120):
   m=p.evaluate(old.STEPN,30)
   if m['state']=='play' and m['lesson']:break
  ck('Tutorial waits for the actual PixelLab atlas before play',m['state']=='play' and p.evaluate('XART.rdy(SG20_WATER.key)&&SG20_WATER.frames===32'),m)
  p.evaluate('()=>{TUT.i=TUT_LESSONS.findIndex(l=>l.id==="exam")-1;tutNext();TUT.typed=10000;}')
  rows=[];gif=[]
  for i,cell in enumerate(meta['cells']):
   result=p.evaluate('''i=>{const S=sg20State();S.time=i/SG20_WATER.fps+.0001;S.travel=600;const im=XART.get(SG20_WATER.key),draw=ctx.drawImage,calls=[];ctx.drawImage=function(image,...a){if(image===im)calls.push(a);return draw.call(this,image,...a);};ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);tutOverlayDraw();ctx.drawImage=draw;const c=document.createElement('canvas');c.width=SG20_WATER.width;c.height=SG20_WATER.height;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(im,...SG20_WATER.cells[SG20.waterFrame],0,0,c.width,c.height);return{frame:SG20.waterFrame,calls,tile:c.toDataURL().split(',')[1]};}''',i)
   data=Image.open(io.BytesIO(base64.b64decode(result.pop('tile')))).convert('RGBA')
   x,y,w,h=cell;native_hash=hashlib.sha256(data.tobytes()).hexdigest();expected=hashlib.sha256(sheet.crop((x,y,x+w,y+h)).tobytes()).hexdigest()
   result['pixel_match']=native_hash==expected;result['hash']=native_hash;rows.append(result)
   if i in [0,8,16,24]:shot(p,'native-phase-'+str(i))
   gif.append(shot(p,'frame-'+str(i)))
  ck('All32 PixelLab poses are selected and drawn by the actual game renderer',all(r['frame']==i and len(r['calls'])>0 and all(c[:4]==meta['cells'][i] for c in r['calls']) for i,r in enumerate(rows)),[{'frame':r['frame'],'draws':len(r['calls'])} for r in rows])
  ck('Every native water pose matches its exported lossless atlas pixels',all(r['pixel_match'] for r in rows))
  ck('All32 displayed frames contain distinct animated water',len({r['hash'] for r in rows})==32)
  ck('Fixed even cells render at a common1:1 tile scale',all(c[6:]==[meta['width'],meta['height']] for r in rows for c in r['calls']) and meta['width']%2==meta['height']%2==0)
  order=p.evaluate('''()=>{const im=XART.get(SG20_WATER.key),arch=XART.get(SG20.key),draw=ctx.drawImage,order=[];ctx.drawImage=function(image,...a){order.push(image===im?'ocean':image===arch?'academy':ctx.globalAlpha<.16?'farCloud':'nearCloud');return draw.call(this,image,...a);};ctx.setTransform(SS,0,0,SS,0,0);ctx.save();ctx.translate(-camX,0);sg20Terrain();ctx.restore();ctx.drawImage=draw;return order.filter((s,i)=>!i||s!==order[i-1]);}''')
  ck('Ocean, distant clouds, academy and near clouds retain their proper depth order',order==['ocean','farCloud','academy','nearCloud'],order)
  ck('Water uses one lazy-loaded texture instead of many separate frame requests',len(set(requests))==1,requests)
  audit=json.loads((R/'_ART_SOURCES/stormglass_water_pixellab_1020/audit.json').read_text(encoding='utf-8'))
  deltas=audit['temporal_mean_absolute_deltas'];ck('Animation wrap is within the normal neighboring-frame motion range',deltas[-1]<=max(deltas[:-1])*1.5,{'wrap':deltas[-1],'max_neighbor':max(deltas[:-1])})
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);tutOverlayDraw();}')
  p.screenshot(path=str(O/'native-desktop.png'));p.set_viewport_size(dict(width=390,height=844));p.evaluate('__bofFit()');p.evaluate(old.STEPN,60);shot(p,'native-narrow')
  gif[0].save(O/'native-water.gif',save_all=True,append_images=gif[1:],duration=83,loop=0,optimize=True)
  ck('No native page, console, drawing or asset errors',not errors,errors)
  b.close()
finally:stop()
report={'passed':sum(c['passed'] for c in checks),'total':len(checks),'errors':errors,'checks':checks,'native_frames':rows,'meta':meta}
(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k in ['passed','total','errors']}));raise SystemExit(not all(c['passed'] for c in checks))
