from pathlib import Path
import json,sys,base64,statistics
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot;from serve_bof_1013 import AssetServer;shoot.http.server.ThreadingHTTPServer=AssetServer
O=R/'_shots/bastion20/gallery';O.mkdir(parents=True,exist_ok=True);errors=[];port,stop=shoot.serve(str(R));D=json.loads((R/'expansion/topdown/art/bastion20/manifest.json').read_text(encoding='utf-8'))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch();p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded',timeout=90000);p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000);p.evaluate('TDGAME.freeze();ART.warm(Object.keys(TD_BASTION20_ART.assets))');p.wait_for_function('ART.progress(Object.keys(TD_BASTION20_ART.assets))===1',timeout=90000)
  audit=p.evaluate('''()=>Object.entries(TD_BASTION20_ART.assets).map(([k,m])=>{const c=document.createElement('canvas');c.width=m.size[0];c.height=m.size[1];const x=c.getContext('2d');x.imageSmoothingEnabled=false;ART.draw(x,k,m.anchor[0],m.anchor[1],{s:1,ax:m.anchor[0],ay:m.anchor[1]});const d=x.getImageData(0,0,c.width,c.height).data;return{key:k,painted:d.some((v,i)=>i%4===3&&v>0),even:c.width%2===0&&c.height%2===0,uncropped:m.bounds[0]>=2&&m.bounds[1]>=2&&m.bounds[2]<=c.width-2&&m.bounds[3]<=c.height-2};})''')
  for k,q in D['sequences'].items():
   if not k.startswith('pb20_')or'hud_'in k:continue
   data=p.evaluate('''k=>{const q=TD_BASTION20_ART.sequences[k],c=document.createElement('canvas');c.width=1024;c.height=Math.ceil(q.frames.length/4)*272;const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#101820';x.fillRect(0,0,c.width,c.height);q.frames.forEach((f,i)=>{const m=TD_BASTION20_ART.assets[f];let ox=(i%4)*256+128,oy=Math.floor(i/4)*272+(k.includes('portrait')?136:k.includes('shield')||k.includes('lightning')?136:244);ART.draw(x,f,ox,oy,{s:1,ax:m.anchor[0],ay:m.anchor[1]});x.fillStyle='#88e3ea';x.font='10px monospace';x.fillText(i,Math.floor(i%4)*256+8,Math.floor(i/4)*272+266);});return c.toDataURL('image/png').split(',')[1];}''',k);(O/(k+'.png')).write_bytes(base64.b64decode(data))
  heights={k:statistics.mean(D['assets'][f]['bounds'][3]-D['assets'][f]['bounds'][1]for f in D['sequences'][k]['frames'])for k in ['pb20_gosfer_fire_south','pb20_gosfer_fire_angle']}
  result={'nativeDraws':audit,'passed':sum(q['painted']and q['even']and q['uncropped']for q in audit),'failed':sum(not(q['painted']and q['even']and q['uncropped'])for q in audit),'firingHeights':heights,'firingRatio':max(heights.values())/min(heights.values()),'errors':errors};(O/'report.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items()if k!='nativeDraws'}));b.close()
finally:stop()
sys.exit(0 if result['failed']==0 and result['firingRatio']<1.02 and not errors else 1)
