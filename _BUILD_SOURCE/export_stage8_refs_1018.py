"""Export the native Stage 8 identities before PixelLab redesigns them."""
from pathlib import Path
import ast,base64,json,sys
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]
O=R/'_ART_SOURCES/stage8_pixellab_1018/references';O.mkdir(parents=True,exist_ok=True)
Q=R/'_shots/stage8_pixellab_1018';Q.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1500,height=900));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof j3Encounter==="function"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate(SETUP,dict(stage=8,diff='normal',kind='vileexistence',pilot='cole'))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&pt11Ready("drone_raise")}')
  p.evaluate('''()=>{window.s8ref=(phase,mimic)=>{j3Encounter(B,phase);if(mimic!=null)j3Mimic(B,mimic);B._r30.mode='fight';B.enter=false;B.x=worldWidth()/2;B.y=215;B.flash=0;B._r30.attack=null;return {phase,mimic,name:B.name,parts:r30Parts(B).map(v=>({id:v.p.id,key:v.key,x:v.x-B.x,y:v.y-B.y,w:v.w,h:v.h,rot:v.rot})),J:{max:j3State(B).max,hp:j3State(B).hp}};};
  window.s8capture=(name)=>{const out=document.createElement('canvas');out.width=out.height=256;if(name==='drone'){const d=230*.66;out.getContext('2d').drawImage(XART.get('vile24_robot_gray'),128-d/2,128-d/2,d,d);return out.toDataURL('image/png').split(',')[1];}ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(128,128);ctx.scale(.66,.66);ctx.translate(-B.x,-B.y);j3Body(B,1);ctx.restore();out.getContext('2d').drawImage(cv,0,0,256,256,0,0,256,256);return out.toDataURL('image/png').split(',')[1];};}''')
  info=[]
  for name,phase,mimic in [('drone',0,None),('infused',0,None),('ghost',1,None),('colossus',2,None),('hammer',2,8),('helicopter',2,1),('harrier',2,6),('volcano',2,2)]:
   row=p.evaluate('([a,b])=>s8ref(a,b)',[phase,mimic]);row['name']=name
   p.wait_for_function('()=>r30Parts(B).every(v=>XART.rdy(REALM30_ART[v.key]?"r30_"+v.key:v.key))')
   raw=p.evaluate('(name)=>s8capture(name)',name);(O/(name+'.png')).write_bytes(base64.b64decode(raw));info.append(row)
  (O/'native_refs.json').write_text(json.dumps(dict(references=info,errors=errors),indent=2))
  br.close()
finally:stop()
sheet=Image.new('RGB',(1024,560),'#101922');d=ImageDraw.Draw(sheet)
for i,row in enumerate(info):
 x=(i%4)*256;y=(i//4)*280;im=Image.open(O/(row['name']+'.png')).convert('RGBA');sheet.paste(im,(x,y),im);d.text((x+8,y+258),row['name'],fill='white')
sheet.save(Q/'native-references.png');print(json.dumps(dict(errors=errors,references=[dict(name=r['name'],parts=len(r['parts'])) for r in info])))
