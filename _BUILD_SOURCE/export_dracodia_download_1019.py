"""Current live rig identities, fixed common canvas and world scale."""
from pathlib import Path
import ast,base64,http.server,json
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_ART_SOURCES/dracodia_download_1019';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));errors=[];rows=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&d20Warm()&&dr21Warm();}',polling=80)
  for name,phase,form in [('infused',0,0),('ghost',1,0),('colossus',2,0),('hammer',2,8),('helicopter',2,1),('harrier',2,6),('volcano',2,2)]:
   p.evaluate('([phase,form])=>{v18Clear(B);v18Budget(B);v18Enter(B,phase,form);v18Fight(B);B._r30.clock=0;B._r30.v18.acting=null;B._r30.v18.swipe=null;B.parts.forEach(v=>{v.destroyed=false;v.flash=0;});B.flash=0;}',[phase,form])
   p.wait_for_function('()=>v18Rig(B).every(v=>XART.rdy(v.key))',polling=80)
   row=p.evaluate('''()=>{const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d'),names=['save','restore','translate','rotate','scale','drawImage'],saved={};g.translate(128,128);g.scale(.5,.5);g.translate(-B.x,-B.y);g.imageSmoothingEnabled=false;try{for(const n of names){saved[n]=ctx[n];ctx[n]=(...args)=>{if(n==='drawImage')g.globalAlpha=ctx.globalAlpha;return g[n](...args);};}v19Body(B);}finally{for(const n of names)ctx[n]=saved[n];ctx.globalAlpha=1;}return{png:c.toDataURL().split(',')[1],size:v18Size(B),parts:v18Rig(B).map(v=>({key:v.key,id:v.p.id}))};}''')
   raw=base64.b64decode(row.pop('png'));(O/(name+'.png')).write_bytes(raw);row.update(name=name,phase=phase,form=form,canvas=[256,256],pivot=[128,128],worldScale=.5);rows.append(row)
  br.close()
finally:stop()
(O/'native_references.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2))
sheet=Image.new('RGB',(1024,560),'#10121b');d=ImageDraw.Draw(sheet)
for i,row in enumerate(rows):
 im=Image.open(O/(row['name']+'.png'));assert not any(im.getchannel('A').crop(box).getbbox() for box in [(0,0,256,1),(0,255,256,256),(0,0,1,256),(255,0,256,256)]);xy=(i%4*256,i//4*280);sheet.paste(im,xy,im);d.text((xy[0]+6,xy[1]+260),row['name'],fill='white')
sheet.save(O/'native-sheet.png');print(json.dumps(dict(forms=len(rows),errors=errors)),flush=True)
