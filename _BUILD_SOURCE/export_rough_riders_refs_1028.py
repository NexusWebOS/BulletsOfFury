from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont
import sys,json,base64,http.server,hashlib
http.server.ThreadingHTTPServer.request_queue_size=256
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/rough_riders_1028';O=W/'references';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
port,stop=serve(str(R));records=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True);p=br.new_page(viewport={'width':1280,'height':800});p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});spawnBoss('rebelsquad');debugFight.spawned=true;}")
  p.wait_for_function('''()=>{const keys=[];for(const k of REBEL_KEYS){for(const B of Object.values(AF21_ART.models[k].banks))keys.push(B.key);for(const kind of ['heading','roll'])if(AM13_ART[k][kind]?.key)keys.push(AM13_ART[k][kind].key);}keys.push(ER28_ART.rook_pod.key);return keys.every(k=>XART.rdy(k))}''',polling=100,timeout=180000)
  for key in ['voss','nyx','rook','kaia','jace']:
   p.wait_for_function('k=>XART.rdy("rr_portrait_"+k)',arg=key,polling=100,timeout=30000)
   portrait=p.evaluate('''k=>{const im=XART.get('rr_portrait_'+k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL().split(',')[1];}''',key);(O/(key+'-portrait.png')).write_bytes(base64.b64decode(portrait))
   # Mirror the real native ship renderer's paths, clipping, transforms and
   # blits onto an RGBA export. The gameplay canvas is alpha:false.
   for view,a in [('south',1.5707963267948966),('north',-1.5707963267948966)]:
    data=p.evaluate('''v=>{const q=boss._rebels.ships.find(q=>q.key===v.key),c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d'),old={};ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;
     const methods=['save','restore','translate','rotate','scale','transform','setTransform','beginPath','moveTo','lineTo','closePath','rect','clip'];for(const m of methods){old[m]=ctx[m];ctx[m]=function(...a){const r=old[m].apply(this,a);g[m](...a);return r}}old.drawImage=ctx.drawImage;ctx.drawImage=function(im,...a){g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.imageSmoothingEnabled=false;return g.drawImage(im,...a)};
     Object.assign(q,{x:128,y:128,rfHeading:v.angle,evadeT:0,frCloak:0,_rr26Fade:0,flash:0,t:0});if(q.rg4)q.rg4.act=null;
     try{fr27RebelDrawShip(q)}finally{for(const [m,fn]of Object.entries(old))ctx[m]=fn;ctx.restore()}
     return{data:c.toDataURL().split(',')[1],key:q._air13RenderedKey,frame:q._air13Frame};}''',dict(key=key,angle=a))
    dest=O/(key+'-'+view+'.png');dest.write_bytes(base64.b64decode(data.pop('data')));records.append(dict(pilot=key,view=view,**data,sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
   for kind in ['idle','somer','roll','drift']:
    data=p.evaluate('''v=>{const M=AF21_ART.models[v.key],B=M.banks[v.kind],im=XART.get(B.key),c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d'),out=[];for(const cell of B.cells){g.clearRect(0,0,128,128);g.drawImage(im,...cell,0,0,128,128);out.push(c.toDataURL().split(',')[1]);}return{key:B.key,span:M.span,ratio:M.referenceRatio,frames:out};}''',dict(key=key,kind=kind))
    frames=data.pop('frames');folder=O/(key+'-'+kind);folder.mkdir(exist_ok=True)
    for i,data64 in enumerate(frames):(folder/f'{i:02d}.png').write_bytes(base64.b64decode(data64))
    records.append(dict(pilot=key,bank=kind,frames=len(frames),**data))
   print('Exported',key,flush=True)
  br.close()
finally:stop()
(O/'manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
board=Image.new('RGB',(1600,760),(10,18,29));d=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/consolab.ttf',23)
ships=['IRON VULTURE','GHOSTKNIFE','BREACHHAMMER','SIGNAL WRAITH','RAZORJACK']
for i,key in enumerate(['voss','nyx','rook','kaia','jace']):
 x=i*320;d.text((x+22,14),key.upper(),font=font,fill='white');d.text((x+22,43),ships[i],font=font,fill=(94,206,230))
 for name,y,size in [('portrait',92,244),('south',372,256)]:
  im=Image.open(O/(key+'-'+name+'.png')).convert('RGBA');box=im.getbbox();im=im.crop(box);k=min(size/im.width,size/im.height);im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);board.paste(im,(x+(320-im.width)//2,y+(256-im.height)//2),im)
 d.text((x+32,666),'NATIVE GAME REFERENCE',font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17),fill=(160,175,190))
board.save(O/'crew-identity-board.png');print('Identity board ready')
