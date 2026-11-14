from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import json,sys,base64,io
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');E=W/'exports';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
M=json.loads((W/'manifest.json').read_text());errors=[];port,stop=serve(str(R))
def save(name,frames,w,h,pivot):
 folder=E/name;folder.mkdir(exist_ok=True);sheet=Image.new('RGBA',(w*4,h*((len(frames)+3)//4)))
 for i,f in enumerate(frames):f.save(folder/f'{i:02}.png');sheet.paste(f,(i%4*w,i//4*h))
 sheet.save(E/(name+'.webp'),lossless=True,method=1)
 M[name]=dict(cw=w,ch=h,count=len(frames),cols=4,pivot=pivot,meta=[])
def png(data):return Image.open(io.BytesIO(base64.b64decode(data.split(',',1)[1]))).convert('RGBA')
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);ctxb=br.new_context(viewport={'width':1280,'height':800});p=boot(ctxb,port,5,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();if(stageLoadReady(5))updatePlay(0);return stageLoadReady(5)&&XART.rdy(CG_BOLT)&&XART.rdy(c30Row("wave",0).key)&&XART.rdy("c41_wave")}',timeout=180000)
  print('Native dimensions',p.evaluate('({VW,VH,canvas:[ctx.canvas.width,ctx.canvas.height]})'),flush=True)
  # The original Stage5 functions draw into a detached authoring canvas, never
  # the live game. Their bitmap results are exported; production only blits them.
  p.evaluate('''()=>{window.bakeCanvas=document.createElement('canvas');bakeCanvas.width=1024;bakeCanvas.height=1024;window.bakeCtx=bakeCanvas.getContext('2d');window.bakeSwirl=new Function('ctx','b','M','front',cgBolt.toString()+';'+cgSwirl.toString()+';return cgSwirl(b,M,front)');window.bakeBolt=new Function('ctx','from','to','t','width','alpha',cgBolt.toString()+';return cgBolt(from,to,t,width,alpha)');window.bakeAura=new Function('ctx','b','a','strength',c45Aura.toString()+';return c45Aura(b,a,strength)');window.bakeRun=(fn,w,h)=>{bakeCtx.save();try{bakeCtx.setTransform(1,0,0,1,0,0);bakeCtx.clearRect(0,0,1024,1024);fn(bakeCtx);const out=document.createElement('canvas');out.width=w;out.height=h;out.getContext('2d').drawImage(bakeCanvas,0,0,w,h,0,0,w,h);return out.toDataURL('image/png');}finally{bakeCtx.restore();}};}''')
  for front in [False,True]:
   frames=[]
   for i in range(32):
    data=p.evaluate('''({i,front})=>bakeRun(ctx=>{efxClock=i/31*4.464;ctx.save();ctx.translate(256,233);ctx.scale(1.36,1.36);bakeSwirl(ctx,{x:0,y:0},{mode:'ragecharge',k:i/31},front);ctx.restore();},512,512)''',dict(i=i,front=front));frames.append(png(data))
   save('swirl_'+('front'if front else'back'),frames,512,512,[256,256])
  for family in ['formation','cast_fore']:
   frames=[];count=M[family]['count']
   for i in range(count):
    source=E/family/f'{i:02}.png';url='data:image/png;base64,'+base64.b64encode(source.read_bytes()).decode()
    p.evaluate('''async u=>{XART._src.dcr13_bake_actor=u;delete C45.aura;const im=new Image;im.src=u;await im.decode();window.bakeActor=im;window.bakeOldGet=XART.get;window.bakeOldRdy=XART.rdy;XART.get=function(k){return k==='dcr13_bake_actor'?bakeActor:bakeOldGet.call(this,k)};XART.rdy=function(k){return k==='dcr13_bake_actor'?true:bakeOldRdy.call(this,k)};}''',url)
    a=M[family]['meta'][i];strength=1
    if family=='formation':
     u=a['transformationU'];strength=1-.35*max(0,min(1,(u-.8)/.2))if u>=.8 else max(0,min(1,((u-.38)/.42-.6)/.4))**2*(3-2*max(0,min(1,((u-.38)/.42-.6)/.4)))*.8
    data=p.evaluate('''({i,a,strength})=>bakeRun(ctx=>{efxClock=i/12;bakeAura(ctx,{x:256,y:256},{key:'dcr13_bake_actor',pivot:[256,256],bounds:a.bounds},strength)},512,512)''',dict(i=i,a=a,strength=strength));frames.append(png(data));p.evaluate('()=>{XART.get=bakeOldGet;XART.rdy=bakeOldRdy;}')
   save('aura_'+family,frames,512,512,[256,256])
   if family=='cast_fore':save('aura_cast_back',[f.resize((224,224),Image.Resampling.NEAREST)for f in frames],224,224,[112,112])
  # The original26-strike bolt texture/geometry, including its diagonal lead.
  for offset in [-35,-28,-21,-14,-7,0,7,14,21,28,35]:
   frames=[png(p.evaluate('''({i,offset})=>bakeRun(ctx=>{efxClock=i/18;bakeBolt(ctx,{x:80+offset,y:0},{x:80,y:768},i/18,34,1)},160,768)''',dict(i=i,offset=offset)))for i in range(8)]
   save('bolt_'+str(offset+35),frames,160,768,[80,768])
  # Same authored growing energy-head pixels used by Chronus's c46Ball.
  ball=[]
  for i in range(16):
   ball.append(png(p.evaluate('''i=>bakeRun(ctx=>{const a=c30Row('wave',0),im=XART.get(a.key),u=i/15,size=lerp(16,74,u),x=48,y=48;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,40,0,112,85,x-size/2,y-size*.38,size,size*.76);ctx.globalCompositeOperation='lighter';ctx.globalAlpha=CG.ladder[2+(i&1)];ctx.drawImage(im,40,0,112,85,x-size*.35,y-size*.27,size*.7,size*.53);},96,96)''',i)))
  save('ball',ball,96,96,[48,48])
  # Same Chronus red wave, baked to a fixed full-screen downward bank. Its
  # native copied-boss line/collision and warning remain authoritative.
  wave=[]
  for i in range(28):
   data=p.evaluate('''i=>bakeRun(ctx=>{const im=c41Sheet(true);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,i%8*320,Math.floor(i/8)*640,320,640,32,0,320,640)},384,768)''',i);wave.append(png(data))
  save('wave',wave,384,768,[192,24]);br.close()
finally:stop()
assert not errors,errors
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')))
(W/'draconus_cinematic_rage_art_1113.js').write_text("'use strict';\nconst DCR13_ART="+json.dumps(M,separators=(',',':'))+';\n')
(W/'effect-bake.json').write_text(json.dumps(dict(errors=errors,owners=['c45Aura','cgSwirl','cgBolt','c46Ball source head','c41Sheet red wave'],runtimeRasterTransformsAdded=False,banks={n:a['count']for n,a in M.items()if not a['meta']}),indent=2))
print('Baked original Stage5 aura, front/back rising swirl, strike bolts, energy ball and red wave as static authored frames.',flush=True)
