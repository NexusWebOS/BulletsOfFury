from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import base64,json,http.server
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_ART_SOURCES/cinematic_finish_1020/references';O.mkdir(parents=True,exist_ok=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(120000);p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.refs20=HC10.pilots.flatMap(pk=>[{pilot:pk,kind:'body',key:campaignIntroPortraitKey(pk)},{pilot:pk,kind:'portrait',key:'comm_'+pk+'_idle'},...['front','rear'].map(view=>({pilot:pk,kind:view,key:hc10ShipKey(pk,view)}))]);window.refKeys20=[...refs20.map(a=>a.key),...Object.values(V18_ART.models.colossus.frames[0]).map(a=>a.key)];}''')
  p.wait_for_function('()=>{let ok=true;for(const k of refKeys20)if(!XART.rdy(k))ok=false;return ok;}',polling=75)
  rows=p.evaluate('''()=>{const rows=[];const save=(a,draw)=>{const c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');g.imageSmoothingEnabled=false;draw(g);rows.push({...a,png:c.toDataURL().split(',')[1]});};for(const a of refs20){const im=XART.get(a.key),rect=['front','rear'].includes(a.kind)?hc10ShipGeometry(a.pilot,a.kind).rect:[0,0,im.width,im.height],k=Math.min(480/rect[2],480/rect[3]);save(a,g=>g.drawImage(im,...rect,256-rect[2]*k/2,256-rect[3]*k/2,rect[2]*k,rect[3]*k));}save({pilot:'dracodia',kind:'colossus',key:'native V18 modules'},g=>{for(const a of Object.values(V18_ART.models.colossus.frames[0]))g.drawImage(XART.get(a.key),96,96,320,320);});return rows;}''')
  model=p.evaluate('V18_ART.models.colossus.frames[0]');b.close()
finally:stop()
for row in rows:(O/(row['pilot']+'-'+row['kind']+'.png')).write_bytes(base64.b64decode(row.pop('png')))
(O/'manifest.json').write_text(json.dumps(dict(rows=rows,colossus=model,errors=errors),indent=2)+'\n')
sheet=Image.new('RGB',(1024,1152),'#101522');d=ImageDraw.Draw(sheet)
for i,pk in enumerate(['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']):
 for j,kind in enumerate(['body','portrait','front','rear']):
  im=Image.open(O/(pk+'-'+kind+'.png')).resize((128,128),Image.Resampling.NEAREST);x=j*256+(i%2)*128;y=i//2*224;sheet.paste(im,(x,y),im);d.text((x+4,y+130),pk+' '+kind,fill='white')
sheet.save(O/'actual-pilots-and-ships.png');print(json.dumps(dict(references=len(rows),errors=errors)))
