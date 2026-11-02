"""Explicit native-plate rotation migration for remaining Stage4-9 owners.
Exports their actual current XART pixels and measured native source rectangles.
Whole plates, independent module pools, pivots and native draw order are kept.
"""
from pathlib import Path
from io import BytesIO
import json,sys,base64,hashlib,math,http.server
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
Q=R/'_shots/enemy_flight_1031';S=R/'_BUILD_SOURCE/enemy_flight_1031/static_sources';S.mkdir(parents=True,exist_ok=True)
O=R/'assets/game/shared/combat/enemy_flight_1031/static';O.mkdir(exist_ok=True)
audit=json.loads((Q/'before/audit.json').read_text());art=json.loads((O.parent/'manifest.json').read_text());keys={}
for q in audit['rows']:
 stage=q['stage'];typ=q['spec']['type']
 if stage<4 or stage>9 or str(stage)+'|'+typ in art['aliases']:continue
 for d in q.get('stats',{}).get('draws',[]):
  key=d['key']
  if abs(d.get('angle',0))<.03:continue
  if key.startswith(('bmfx','bet24','r46','cached','laserbeam','fury_')):continue
  if not key.startswith(('s5atk_','s7atk_','nsb_','nhd_idle_','mm1003_','s81003_','at23_','fr27_realm_fleet','overhaul_tank_7_','overhaul_ground_head_','sm10_toxic_')):continue
  rec=tuple(d['rect'])if d['rect']else None;keys.setdefault(key,{'rects':set(),'stages':set(),'types':set()});keys[key]['rects'].add(rec);keys[key]['stages'].add(stage);keys[key]['types'].add(typ)
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate('(keys)=>keys.forEach(k=>XART.rdy(k))',list(keys));p.wait_for_function('(keys)=>keys.every(k=>XART.rdy(k))',arg=list(keys),timeout=180000)
  for key in keys:
   src=p.evaluate('(key)=>{const im=XART.get(key),c=document.createElement("canvas");c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;c.getContext("2d").drawImage(im,0,0);return c.toDataURL().split(",")[1]}',key)
   (S/(key+'.png')).write_bytes(base64.b64decode(src))
  b.close()
finally:stop()
meta={'owner':'_BUILD_SOURCE/build_enemy_static_1031.py','banks':{},'lookup':{}}
for key,entry in keys.items():
 im=Image.open(S/(key+'.png')).convert('RGBA');rects=sorted(entry['rects'],key=str);frames=[];scale=None;maxspan=0
 for rec in rects:
  x,y,w,h=rec or(0,0,im.width,im.height);maxspan=max(maxspan,w,h)
 bound=288 if any(t.startswith('ll18')for t in entry['types'])else 192;k=min(1,bound/maxspan);cell=math.ceil((bound*math.sqrt(2)+8)/2)*2
 for rec in rects:
  x,y,w,h=rec or(0,0,im.width,im.height);tile=im.crop((x,y,x+w,y+h));tile=tile.resize((round(w*k),round(h*k)),Image.Resampling.NEAREST);pad=Image.new('RGBA',(cell,cell));pad.alpha_composite(tile,((cell-tile.width)//2,(cell-tile.height)//2));frames.append(pad)
 dirs=32;out=Image.new('RGBA',(cell*dirs,cell*len(frames)))
 for f,t in enumerate(frames):
  for d in range(dirs):out.alpha_composite(t.rotate(-d*360/dirs,Image.Resampling.NEAREST),(d*cell,f*cell))
 name='s'+hashlib.sha256(key.encode()).hexdigest()[:14];path=O/(name+'.webp');out.save(path,format='WEBP',lossless=True,method=4)
 B={'key':'r46_'+name,'path':path.relative_to(R).as_posix(),'cell':cell,'dirs':dirs,'frames':len(frames),'scale':k,'rects':[list(r)if r else None for r in rects],'sourceSize':[im.width,im.height],'source':(S/(key+'.png')).relative_to(R).as_posix(),'stages':sorted(entry['stages']),'types':sorted(entry['types']),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 meta['banks'][key]=B;print('EXPORTED',key,len(frames),flush=True)
(O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8');(R/'assets/enemy_static_art_1031.js').write_text('"use strict";\nconst R46_STATIC='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Registered',len(meta['banks']),'current native plate banks')
