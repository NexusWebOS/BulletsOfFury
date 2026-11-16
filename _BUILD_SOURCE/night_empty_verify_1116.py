from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/empty-frame';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
M=json.loads((R/'_ART_SOURCES/cinema_overnight_1116/empty-frame.json').read_text());checks=[];errors=[]
im=Image.open(R/M['path']).convert('RGBA');x,y,w,h=M['after'];checks.append({'name':'Replacement source is existing fully transparent2x2 pixels','ok':not im.crop((x,y,x+w,y+h)).getchannel('A').getbbox()})
with sync_playwright()as z:
 b=z.chromium.launch(args=['--no-sandbox']);p=b.new_page();p.set_default_timeout(150000);p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto('http://127.0.0.1:8765/index.html?night-empty-frame=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.wait_for_function("()=>XART.rdy('tc119_page_155')")
 q=p.evaluate('''()=>{const B=TC119_ART.banks.beam_coupling_tail,c=B.cells[5],im=XART.get(c[0]);TC119.images[c[0]]=im;function draw(old){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#1d364b';ctx.fillRect(0,0,cv.width,cv.height);const x=c[1];try{if(old)c[1]=556;tc119Blit('beam_coupling_tail',5,240,256);}finally{c[1]=x;ctx.restore();}return ctx.getImageData(0,0,cv.width,cv.height).data;}const a=draw(true),b=draw(false);let different=0;for(let i=0;i<a.length;i++)if(a[i]!==b[i])different++;return{c,different,inBounds:c[1]>=0&&c[2]>=0&&c[1]+c[3]<=im.width&&c[2]+c[4]<=im.height,draws:TC119.draws.beam_coupling_tail};}''')
 checks.append({'name':'Native end-frame blits remain pixel-identical with a valid source rect','ok':q['different']==0 and q['inBounds']and q['draws']==2,'data':q});b.close()
checks.append({'name':'No page errors','ok':not errors,'data':errors});(O/'report.json').write_text(json.dumps({'checks':checks},indent=2),encoding='utf8');print(json.dumps(checks));assert all(q['ok']for q in checks)
