from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageOps
import sys,json,struct,zlib,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/cinema';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,d=None):checks.append({'name':n,'ok':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?release-cinema=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 q=p.evaluate("()=>{window.QA16Ending=[];for(const pk of PILOTS.map(p=>p.key)){const rows=c16Rows('ending',pk);QA16Ending.push({pilot:pk,rows:rows.filter(b=>b.text).map(b=>({id:b.id,len:b.text.length,duration:b.duration,hold:b.read16?.hold,actual:b.duration-(b.cm3?.readAt||0)-b.text.length/30-.18}))});}return QA16Ending;}")
 ck('all nine ending routes keep at least2.25 seconds of complete readable text',all(row['actual']>=2.249 for case in q for row in case['rows']),q)
 if not checks[-1]['ok']:print(json.dumps([{'pilot':case['pilot'],**row}for case in q for row in case['rows']if row['actual']<2.249]),flush=True)
 p.evaluate("()=>{run.mode='campaign';run.pilot='juggernaut';diffKey='furious';coopOn=false;window.ENDING16Rows=c16Rows('ending','juggernaut').filter(b=>['ENDING-16','ENDING-17','ENDING-18'].includes(b.id));window.ENDING16Done=0;d1110Ready(d1110Keys(ENDING16Rows));}")
 p.wait_for_function('()=>d1110Ready(d1110Keys(ENDING16Rows))',polling=50)
 p.evaluate("""()=>{window.GuitarPaint16=0;const draw=ctx.drawImage;ctx.drawImage=function(...a){if(a.length===9&&a[3]===270&&a[4]===270){const c=document.createElement('canvas');c.width=c.height=270;const g=c.getContext('2d');g.drawImage(a[0],a[1],a[2],270,270,0,0,270,270);const actual=g.getImageData(0,0,270,270).data;g.clearRect(0,0,270,270);g.drawImage(XART.get(READ16.comicArt.key),a[1],a[2],270,270,0,0,270,270);const expected=g.getImageData(0,0,270,270).data;let error=0,ink=0;for(let i=0;i<actual.length;i+=64){error+=Math.abs(actual[i]-expected[i])+Math.abs(actual[i+1]-expected[i+1])+Math.abs(actual[i+2]-expected[i+2])+Math.abs(actual[i+3]-expected[i+3]);ink+=expected[i+3];}if(!error&&ink>10000)GuitarPaint16++;}return draw.apply(this,a);};}""")
 p.evaluate("()=>d1110Play('qa-ending-guitar',ENDING16Rows,()=>{ENDING16Done++;})")
 samples=[];frames=[]
 for i in range(180):
  p.evaluate(shoot.STEP,6);p.wait_for_timeout(1)
  s=p.evaluate("()=>{const q=BOFCinematicDirector.current,b=q?.beats[q.i];return{id:b?.id,t:q?.t,shown:q?.shown,len:b?.text.length,duration:b?.duration,done:ENDING16Done,bank:D1110_ART.banks['juggernaut-guitar'].key};}")
  samples.append(s)
  if i in [9,20,32,45,65,90,110]:p.screenshot(path=str(O/f'ending-{i}.png'))
  if i<65 and i%2==0:
   raw=p.locator('#screen').screenshot();from io import BytesIO
   frames.append(ImageOps.contain(Image.open(BytesIO(raw)).convert('RGB'),(912,512)))
  if s['done']:break
 ck('native three-line ending reaches its callback once',samples[-1]['done']==1,{'samples':samples})
 ck('actual scene binds the approved guitar bank throughout',all(s['bank']=='release16_juggernaut_guitar'for s in samples))
 ck('own native drawImage paints the approved comic-sheet pixels',p.evaluate('GuitarPaint16>15'),p.evaluate('GuitarPaint16'))
 ck('full first line remains visible for at least two native seconds',sum(.1 for s in samples if s.get('id')=='ENDING-16'and s.get('shown')==s.get('len'))>=2)
 ck('no page console or asset errors',not errors,errors)
 frames[0].save(O/'ending-guitar.gif',save_all=True,append_images=frames[1:],duration=200,loop=0);b.close()
# Independently decode authored .aseprite cels; compare production pixels.
data=(R/'_ART_SOURCES/release_qa_1116/juggernaut-guitar.aseprite').read_bytes();size,magic,count,w,h,depth=struct.unpack_from('<I5H',data);pos=128;history=[];decoded=[];visible=[]
for f in range(count):
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
sheet=Image.open(R/'assets/game/shared/cinematics/release_qa_1116/juggernaut-guitar.webp').convert('RGBA')
ck('six even512x512 cells independently round-trip from editable source',count==6 and w==h==512 and visible==[False,True]and pos==len(data)and all(im.tobytes()==sheet.crop((i%3*512,i//3*512,i%3*512+512,i//3*512+512)).tobytes()for i,im in enumerate(decoded)))
(O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');sys.exit(any(not q['ok']for q in checks))
