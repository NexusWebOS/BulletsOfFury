"""Native authored hangar + actual aircraft + approved full-body pilot shots."""
from pathlib import Path
import base64,json,hashlib
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]
O=R/'_ART_SOURCES/cast_performance_1102/references/native_shots';O.mkdir(parents=True,exist_ok=True)
Q=R/'_shots/cast_performance_1102';Q.mkdir(parents=True,exist_ok=True)
pilots=['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']
errors=[];records=[]
port,stop=shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(120000)
        p.on('pageerror',lambda e:errors.append(str(e)))
        p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
        p.wait_for_function('()=>XART.rdy("c22_hq_hangar")')
        for pilot in pilots:
            p.wait_for_function('p=>["c22_"+p+"_front",C112.key(p,"neutral")].map(k=>XART.rdy(k)).every(Boolean)',arg=pilot)
            result=p.evaluate('''pilot=>{cv.width=1536;cv.height=1024;ctx.setTransform(1,0,0,1,0,0);ctx.imageSmoothingEnabled=false;
                const bg=XART.get('c22_hq_hangar'),bk=Math.max(1536/bg.width,1024/bg.height);
                ctx.drawImage(bg,(1536-bg.width*bk)/2,(1024-bg.height*bk)/2,bg.width*bk,bg.height*bk);
                const key='c22_'+pilot+'_front',im=XART.get(key);
                const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const a=g.getImageData(0,0,c.width,c.height).data;
                let l=c.width,r=0,t=c.height,b=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>8){const x=i/4%c.width,y=Math.floor(i/4/c.width);l=Math.min(l,x);r=Math.max(r,x+1);t=Math.min(t,y);b=Math.max(b,y+1);}
                const scale=1080/(r-l),x=960-(l+r)/2*scale,y=735-b*scale;
                ctx.drawImage(im,x,y,im.width*scale,im.height*scale);
                const actor=C112.key(pilot,'neutral');C112.draw(pilot,'neutral',365,1000,1024);
                return {ship:key,actor,shipBounds:[420,735-(b-t)*scale,1080,(b-t)*scale],shipSourceBounds:[l,t,r,b],file:cv.toDataURL().split(',')[1]};}''',pilot)
            data=base64.b64decode(result.pop('file'));file=O/(pilot+'.png');file.write_bytes(data)
            result.update(pilot=pilot,file=file.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest());records.append(result)
        br.close()
finally:stop()
board=Image.new('RGB',(1536,1024),'#142333');draw=ImageDraw.Draw(board)
for i,pilot in enumerate(pilots):
    im=Image.open(O/(pilot+'.png'));im.thumbnail((512,341));board.paste(im,((i%3)*512,(i//3)*341));draw.text(((i%3)*512+12,(i//3)*341+12),pilot.upper(),fill='white')
board.save(Q/'all-ship-scenes.jpg',quality=95)
(O/'manifest.json').write_text(json.dumps({'method':'Native game ctx.drawImage composition. Actual C22 fronts and approved full-body actors, no generated aircraft replacement.','errors':errors,'scenes':records},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'scenes':len(records),'errors':errors}))
