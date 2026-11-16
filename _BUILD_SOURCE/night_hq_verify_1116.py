from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import sys,json,hashlib,struct,zlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/cinema_overnight_1116';O=R/'_shots/cinema_overnight_1116/hq-art';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
m=json.loads((S/'hq-conference.json').read_text(encoding='utf8'));sheet=Image.open(R/m['full']['path']).convert('RGBA');small=Image.open(R/m['comic']['path']).convert('RGBA');checks=[];errors=[]
def ck(n,v,d=None):checks.append({'name':n,'ok':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
data=(S/'hq-conference.aseprite').read_bytes();size,magic,count,w,h,depth=struct.unpack_from('<I5H',data);pos=128;history=[];visible=[];decoded=[]
for frame in range(count):
 length,magic,n,duration=struct.unpack_from('<IHHH',data,pos);end=pos+length;pos+=16;cels={}
 for j in range(n):
  length,kind=struct.unpack_from('<IH',data,pos);q=data[pos+6:pos+length]
  if kind==0x2004:visible.append(bool(struct.unpack_from('<H',q)[0]&1))
  elif kind==0x2005:
   idx,x,y,a,typ,z=struct.unpack_from('<HhhBHh',q)
   if typ==1:cels[idx]=history[struct.unpack_from('<H',q,16)[0]][idx].copy()
   else:ww,hh=struct.unpack_from('<HH',q,16);cels[idx]=Image.frombytes('RGBA',(ww,hh),zlib.decompress(q[20:]))
  pos+=length
 assert pos==end;history.append(cels);out=Image.new('RGBA',(w,h))
 for idx,v in enumerate(visible):
  if v:out.alpha_composite(cels[idx])
 decoded.append(out)
ck('editable four-frame source independently decodes to exact production pixels',count==4 and(w,h)==(888,444)and visible==[False,True]and pos==len(data)and all(im.tobytes()==sheet.crop((i%2*888,i//2*444,i%2*888+888,i//2*444+444)).tobytes()for i,im in enumerate(decoded)))
ck('master and direct comic export use even cells',all(v%2==0 for a in[m['full'],m['comic']]for v in[a['w'],a['h']]))
top,cropH=m['comic']['sharedCrop'][1],m['comic']['sharedCrop'][3]
ck('every comic frame derives directly from the padded master',all(small.crop((i*754,0,(i+1)*754,270)).tobytes()==im.crop((0,top,888,top+cropH)).resize((754,270),Image.Resampling.NEAREST).tobytes()for i,im in enumerate(decoded)))
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox']);tab=b.new_page(viewport={'width':1440,'height':1000});tab.set_default_timeout(180000);tab.on('pageerror',lambda e:errors.append(str(e)));tab.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 tab.goto('http://127.0.0.1:8765/index.html?night-hq-art=1116');tab.wait_for_function('window.__bofFrames>6');tab.evaluate(shoot.TRAP_RAF)
 tab.evaluate("()=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';pilotIndex=8;coopOn=false;diffKey='hard';d1110Play('night-hq-art',c16Rows('ending','cole').filter(b=>b.id==='ENDING-19'),()=>{});window.NightHQBytes=null;const draw=ctx.drawImage;ctx.drawImage=function(...a){if(a.length===9&&a[3]===754&&a[4]===270&&a[0]?.src?.includes('/cinema_overnight_1116/hq-conference-comic.webp')){const c=document.createElement('canvas');c.width=754;c.height=270;const g=c.getContext('2d');g.drawImage(a[0],a[1],a[2],754,270,0,0,754,270);NightHQBytes=g.getImageData(0,0,754,270).data;}return draw.apply(this,a);};}")
 tab.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 for i in range(4):
  got=tab.evaluate("async f=>{NightHQBytes=null;const s=BOFCinematicDirector.current,b=s.beats[0];s.t=2;s.age=20;s.shown=b.text.length;b.hold=f;d1110Visual(b,s);if(!NightHQBytes)return null;const sha=await crypto.subtle.digest('SHA-256',NightHQBytes);return Array.from(new Uint8Array(sha)).map(v=>v.toString(16).padStart(2,'0')).join('');}",i)
  expected=hashlib.sha256(small.crop((i*754,0,(i+1)*754,270)).tobytes()).hexdigest();ck('actual cinematic drawImage paints approved full conference pose '+str(i),got==expected,{'actual':got,'expected':expected});tab.locator('#screen').screenshot(path=str(O/f'pose-{i}.png'))
 ck('native registries all point at the new complete conference family',tab.evaluate("D1110_ART.banks['hq-conference'].key===HQ1110_ART.banks['hq-conference'].key&&C16_ART.banks['art-hq-conference'].key==='nq16_hq_conference_comic'"))
 ck('no page console or asset errors',not errors,errors);b.close()
(O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors,'manifest':m,'scope':'Four retained whole conference poses, exact editable-source round-trip and actual native bitmap draw proof. Costume correction only; no sixteen-frame animation claim or Aseprite GUI claim.'},indent=2),encoding='utf8');assert all(q['ok']for q in checks)
