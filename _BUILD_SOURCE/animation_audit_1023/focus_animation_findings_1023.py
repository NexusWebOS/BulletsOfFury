from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,base64,io,numpy as np
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=W/'focused';O.mkdir(exist_ok=True);catalog=json.loads((W/'roster/catalog.json').read_text());results=[];errors=[];port,stop=shoot.serve(str(R))
def image(s):return Image.open(io.BytesIO(base64.b64decode(s))).convert('RGB')
def compare(a,b):
 a=np.array(a).astype(int);b=np.array(b).astype(int);mask=a.max(2)>12;delta=b.mean(2)-a.mean(2);return int((mask&(delta>20)).sum())
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  p.evaluate('''()=>{AQ23.stackBase=ctx.drawImage;ctx.drawImage=function(im,...a){const w=im?.naturalWidth||im?.width,h=im?.naturalHeight||im?.height;if(AQ23.owner&&(a.some(v=>!Number.isFinite(v))||a.length===8&&(a[0]+a[2]>w+.1||a[1]+a[3]>h+.1))){AQ23.stacks??=[];if(AQ23.stacks.length<8)AQ23.stacks.push({args:a,w,h,stack:new Error().stack,actor:AQ23.owner.type});}return AQ23.stackBase.call(this,im,...a);};}''')
  for st,types in [(4,['sandtank','s4interceptor','s4command']),(6,['s1jetbomber_b','s6bomber']),(8,['s8carrier','s8deathorb','pt11frostcarrier'])]:
   p.evaluate('s=>EA11.setup(s,"normal")',st);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage);}')
   specs=next(s['specs']for s in catalog['stages']if s['stage']==st)
   for typ in types:
    spec=next((s for s in specs if s['type']==typ),None)
    if not spec:continue
    p.evaluate('s=>{AQ23.begin(s);AQ23.stacks=[];}',spec)
    for j in range(20):
     m=p.evaluate('()=>AQ23.step(30)')
     data=p.evaluate('()=>AQ23.draw(E)');normal=image(data['image'])
     if (np.array(normal).max(2)>12).sum()>50:break
    p.wait_for_timeout(200);p.evaluate('()=>{E.x=worldWidth()/2;E.y=220;camX=E.x-viewW()/2;E.flash=0;for(const o of [E._modTurret,E._r30?.left,E._r30?.right,E._r30?.turret])if(o)o.flash=0;}');normal=image(p.evaluate('()=>AQ23.draw(E).image'));hit=p.evaluate('()=>AQ23.hit(E)');native=image(hit['native']['image']);p.wait_for_timeout(250);decoded=image(p.evaluate('()=>{E.flash=.12;return AQ23.draw(E).image}'));meta=p.evaluate('''()=>({keys:AQ23.draw(E).keys,stacks:AQ23.stacks||[],entity:Object.fromEntries(Object.entries(E).filter(([k,v])=>v==null||typeof v!=='object'&&typeof v!=='function')),armor:E._armor17,sourceKeys:AF21.aliases.get(E.type)?.M.sourceKeys,aliases:[...AF21.sourceAliases.entries()].filter(([k])=>k.includes('enc30_jet')),palette:typeof xartPalette==='function'?String(xartPalette).slice(0,200):null})''');row={'stage':st,'type':typ,'diagnosticPlacement':True,'nativeBrightPixels':compare(normal,native),'decodedBrightPixels':compare(normal,decoded),'hpBefore':hit['hpBefore'],'hpAfter':hit['hpAfter'],'timer':hit['timer'],'meta':meta};results.append(row);c=Image.new('RGB',(normal.width*3,normal.height));c.paste(normal,(0,0));c.paste(native,(normal.width,0));c.paste(decoded,(normal.width*2,0));c.save(O/f'{st}-{typ}.png');print(json.dumps({k:v for k,v in row.items()if k!='meta'}),flush=True)
  br.close()
finally:stop();(O/'report.json').write_text(json.dumps({'cases':results,'errors':errors},indent=2))
