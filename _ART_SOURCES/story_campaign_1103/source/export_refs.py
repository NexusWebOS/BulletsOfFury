from pathlib import Path
import sys, json, base64, hashlib
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=Path(__file__).resolve().parent
O=W/'references';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1360,'height':1024})
  p.set_default_timeout(120000);p.goto(f'http://127.0.0.1:{port}/index.html')
  p.wait_for_function('window.__bofFrames>4')
  if '--intro' in sys.argv:
   dst=O/'intro';dst.mkdir(exist_ok=True);records=[]
   for pilot in ['cole','maverick','decker','axel','freezer','lizzie']:
    key='aintro_'+pilot;p.evaluate('k=>XART.rdy(k)',key);p.wait_for_function('k=>XART.rdy(k)',arg=key,timeout=45000)
    v=p.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return{w:c.width,h:c.height,source:XART._src[k],data:c.toDataURL().split(',')[1]}}''',key)
    (dst/(key+'.png')).write_bytes(base64.b64decode(v.pop('data')));records.append({'key':key,**v});print('Exported '+key,flush=True)
   (dst/'manifest.json').write_text(json.dumps(records,indent=2));br.close();stop();sys.exit(0)
  p.evaluate(shoot.TRAP_RAF)
  if '--extras' in sys.argv:
   meta=p.evaluate('()=>({rebels:RR33_ART})');(O/'extras.json').write_text(json.dumps(meta,indent=2))
   keys=['whv_closed']+['cin_pilot_'+p+'_open' for p in ['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']]
   for key in keys:
    p.wait_for_function('k=>XART.rdy(k)',arg=key,timeout=15000)
    data=p.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL().split(',')[1]}''',key)
    (O/(key+'.png')).write_bytes(base64.b64decode(data));print('Exported '+key,flush=True)
   br.close();stop();sys.exit(0)
  info=p.evaluate('''()=>({W:VW,H:VH,scale:SS,images:C22_ART.images,banks:C22_ART.banks,cast:C112.art,performance:CP112_ART,ships:BOFX.ships,src:Object.fromEntries(Object.entries(XART._src).filter(([k,v])=>/harrier|rr_.*(body|ship)|rebel.*(ship|body)|cin_pilot_.*open|flight.*(cole|axel)|so[26]$/.test(k)))})''')
  (O/'native.json').write_text(json.dumps(info,indent=2))
  records=[]
  for pilot in info['cast']['pilots']:
   keys=['ship_'+pilot,'ship_'+pilot+'_so2','ship_'+pilot+'_so6','c112_'+pilot+'_neutral']
   for key in keys:
    p.wait_for_function('k=>XART.rdy(k)',arg=key)
    v=p.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return {w:c.width,h:c.height,data:c.toDataURL().split(',')[1]}}''',key)
    f=O/(key+'.png');f.write_bytes(base64.b64decode(v.pop('data')))
    records.append({'key':key,**v,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
   print('Exported '+pilot,flush=True)
  (O/'exports.json').write_text(json.dumps(records,indent=2))
  br.close()
finally:stop()
