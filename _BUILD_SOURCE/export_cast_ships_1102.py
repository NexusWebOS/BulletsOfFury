"""Fresh actual in-game ship identity references for the expanded cast scenes."""
from pathlib import Path
import base64, hashlib, json
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]
O=R/'_ART_SOURCES/cast_performance_1102/references'
O.mkdir(parents=True,exist_ok=True)
pilots=['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']
records=[];errors=[]
port,stop=shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br=pw.chromium.launch(channel='msedge')
        p=br.new_page();p.set_default_timeout(120000)
        p.on('pageerror',lambda e:errors.append(str(e)))
        p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        p.goto(f'http://127.0.0.1:{port}/index.html')
        p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
        for pilot in pilots:
            keys=p.evaluate('''p=>['ship_'+p,'ship_'+p+'_so6','ship_'+p+'_so2',...Object.entries(C22_ART.images).filter(([k,v])=>k.includes(p)&&/ship|front/.test(k)).map(([k,v])=>v.key)]''',pilot)
            for i,key in enumerate(dict.fromkeys(keys)):
                p.wait_for_function('k=>XART.rdy(k)',arg=key)
                data=p.evaluate('''k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return {w:c.width,h:c.height,data:c.toDataURL().split(',')[1]};}''',key)
                path=O/(key+'.png');path.write_bytes(base64.b64decode(data.pop('data')))
                records.append({'pilot':pilot,'key':key,'file':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),**data})
        br.close()
finally:stop()
for pilot in pilots:
    refs=[r for r in records if r['pilot']==pilot]
    board=Image.new('RGB',(1536,1024),'#142333');draw=ImageDraw.Draw(board)
    actor=Image.open(R/f'assets/game/shared/cinematics/cast_1102/{pilot}/neutral.png').convert('RGBA');actor.thumbnail((480,970),Image.Resampling.NEAREST)
    board.paste(actor,((512-actor.width)//2,30),actor);draw.text((18,12),pilot.upper()+' APPROVED ACTOR',fill='white')
    for j,row in enumerate(refs):
        im=Image.open(R/row['file']).convert('RGBA');im.thumbnail((480,440),Image.Resampling.NEAREST)
        x=512+(j%2)*512;y=(j//2)*512
        board.paste(im,(x+(512-im.width)//2,y+45+(440-im.height)//2),im)
        draw.text((x+12,y+12),row['key'],fill='white')
    board.save(O/(pilot+'-ship-identity.png'))
(O/'manifest.json').write_text(json.dumps({'errors':errors,'exports':records},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'exports':len(records),'errors':errors}))
