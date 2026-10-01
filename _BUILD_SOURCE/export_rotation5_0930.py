"""Export engine-resolved anchor art to portable 72-heading PNG pages.
No runtime frame is cut out of an atlas by guessed filenames or dimensions.
Authored pitch/roll frames are separate sources, never substituted for yaw.
"""
from pathlib import Path
import sys,json,base64,http.server,hashlib,re,time
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
O=R/'_ART_SOURCES/rotation5_0930';O.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
port,stop=sh.serve(str(R));manifest={'stepDegrees':5,'frameCount':72,'clockwise':True,'zero':'authored heading','pivot':'center','maxSourceEdge':384,'entries':{},'missing':[]};hashes={}
if (O/'manifest.json').exists():
 manifest=json.loads((O/'manifest.json').read_text(encoding='utf-8'));manifest['missing']=[]
 hashes={v['sourceHash']:v['page'] for v in manifest['entries'].values() if (O/v['page']).is_file()}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page()
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>3',timeout=120000);p.evaluate(sh.TRAP_RAF)
  catalog=p.evaluate("""()=>{
   furyShipWarm();const out=[],seen=new Set(),add=(key,rect,name)=>{name=name||key;if(seen.has(name))return;seen.add(name);out.push({key,rect,name});};
   for(const [k,v]of Object.entries(BOFX.cells))if(/^(en_|boss_|mini_)/.test(String(v[0])))add(k);
   for(const k of Object.keys(BOFX.ships))add(k);
   for(const k of FURY_KEYS)if(furyTintedKey(k)){add('fury_'+k);add('fury_'+k+'_blue');}
   for(const [k,a]of Object.entries(REPAIR30_ART))if(/^chaingun_(mount|barrel)/.test(k))for(let i=0;i<a.frames.length;i++)add(a.key,a.frames[i],a.key+'__'+i);
   for(const k of Object.keys(XART._src))if(!BOFX.cells[k]&&/^(furyjet_|furyboat_|furywarship_|rr_ship_|rzb_|ovbody_|ovturret_|whv_|fzt_|vile24_robot|vile24_alien|vile25_void_knight)/.test(k)&&!/(flash|beam|smoke|muzzle|trail|expl|fx|projectile)/.test(k))add(k);
   for(const pack of [ENC30_ART,S7M_ART])for(const [k,a]of Object.entries(pack)){
    if(/vent|entry|beam|flash|fx|fluid|portal/.test(k))continue;
    const key=a.key||'s7m_'+k;if(a.frames)for(let i=0;i<a.frames.length;i++)add(key,a.frames[i],key+'__'+i);else add(key);
   }
   for(const k of ['possessed_body','possessed_armL','possessed_armR','colossus_body','colossus_armL','colossus_armR','chopper_body','chopper_rotor','furnace'])add('r30_'+k);
   return out;
  }""")
  manifest['spacePalette']=p.evaluate('()=>({colors:GRAVITY_PILOT_PAL,luminance:GRAVITY_PILOT_LUM,masks:"_blue",blend:"multiply into mask; source-over onto base"})')
  (O/'catalog.json').write_text(json.dumps(catalog,indent=2));print('Catalog:',len(catalog),flush=True)
  p.evaluate("""()=>{window.rotExportSource=o=>{
   const im=XART.get(o.key),r=o.rect||[0,0,im.naturalWidth||im.width,im.naturalHeight||im.height],scale=Math.min(1,384/Math.max(r[2],r[3]));
   const s=document.createElement('canvas');s.width=Math.max(1,Math.round(r[2]*scale));s.height=Math.max(1,Math.round(r[3]*scale));
   const g=s.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(im,...r,0,0,s.width,s.height);window.rotExportCanvas=s;
   return {data:s.toDataURL().split(',')[1],w:s.width,h:s.height,sourceRect:r,scale};};
   window.rotExportPage=()=>{const s=rotExportCanvas,side=Math.ceil(Math.hypot(s.width,s.height))+6,c=document.createElement('canvas');c.width=side*9;c.height=side*8;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
    for(let i=0;i<72;i++){g.save();g.translate((i%9+.5)*side,(Math.floor(i/9)+.5)*side);g.rotate(i*Math.PI/36);g.drawImage(s,-s.width/2,-s.height/2);g.restore();}
    return {data:c.toDataURL().split(',')[1],side};};
  }""")
  for i,o in enumerate(catalog):
   existing=manifest['entries'].get(o['name'])
   if existing and (O/existing['page']).is_file():continue
   try:
    p.wait_for_function('k=>XART.rdy(k)',arg=o['key'],timeout=20000)
    src=p.evaluate('o=>rotExportSource(o)',o);h=hashlib.sha256(base64.b64decode(src.pop('data'))).hexdigest()
    file=hashes.get(h);side=None
    if file is None:
     data=p.evaluate('()=>rotExportPage()');side=data['side'];file=re.sub(r'[^a-zA-Z0-9_-]','_',o['name'])+'.png'
     (O/file).write_bytes(base64.b64decode(data['data']));hashes[h]=file
    side=side or int((src['w']**2+src['h']**2)**.5+.999999)+6
    manifest['entries'][o['name']]={**o,**src,'page':file,'cell':side,'columns':9,'rows':8,'anchor':[side/2,side/2],'sourceHash':h}
   except Exception as e:manifest['missing'].append({'name':o['name'],'error':str(e)[:200]})
   if i%50==0:
    print(i,'/',len(catalog),'pages',len(hashes),'missing',len(manifest['missing']),flush=True)
    (O/'manifest.json').write_text(json.dumps(manifest,indent=2))
  (O/'manifest.json').write_text(json.dumps(manifest,indent=2));print('DONE',len(manifest['entries']),'sources',len(hashes),'pages',len(manifest['missing']),'missing',flush=True);b.close()
finally:stop()
