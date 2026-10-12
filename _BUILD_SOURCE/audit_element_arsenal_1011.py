"""Native pre/post audit of all nine player elements across all nine Forge carriers."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
arg=argparse.ArgumentParser();arg.add_argument('--label',default='before');args=arg.parse_args()
OUT=ROOT/'_shots/element_arsenal_1011'/args.label;OUT.mkdir(parents=True,exist_ok=True)
elements=['fire','kinetic','lightning','water','ice','chrome','toxic','dark','wind'];errors=[];rows=[]
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport=dict(width=1280,height=1000));page.set_default_timeout(120000)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  page.goto(f'http://127.0.0.1:{port}/index.html');page.wait_for_function('window.__bofFrames>4');page.evaluate(shoot.TRAP_RAF)
  page.evaluate(shoot.SETUP,dict(state='PLAY',stage=1,pilot='cole',invuln=True))
  page.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(1).ready}')
  page.evaluate('''()=>{window.__eaAudit={};window.__eaSeen=new Set();const get=XART.get;XART.get=function(k){__eaSeen.add(k);return get.apply(this,arguments)};
   for(const [e,i] of Object.keys(INFUSIONS).map((e,i)=>[e,i])){for(let w=0;w<9;w++){XART.rdy(forgeBadgeKey(e,w,1));}XART.rdy('inf_'+e);}
   if(typeof EA11_ART!=='undefined')for(const a of Object.values(EA11_ART.banks))XART.rdy(a.key);
  }''')
  for elem in elements:
   for slot in range(9):
    page.evaluate('''c=>{window.__eaP=forgePreviewNew(c.slot,c.elem,3);__eaSeen.clear();}''',dict(slot=slot,elem=elem))
    # Drawing warms the actual late renderer, then yields to image decode.
    for _ in range(6):
     page.evaluate('()=>{for(let i=0;i<10;i++)forgePreviewTick(__eaP,240,340,1/60);forgePreviewDraw(__eaP,0,0,240,340)}');page.wait_for_timeout(15)
    q=page.evaluate('''()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);__eaSeen.clear();forgePreviewDraw(__eaP,0,0,240,340);ctx.restore();
     const c=document.createElement('canvas');c.width=240;c.height=340;c.getContext('2d').putImageData(ctx.getImageData(0,0,240,340),0,0);
     return {error:__eaP.err,keys:[...__eaSeen],name:forgeComboName(__eaP.elem,__eaP.w),badge:forgeBadgeKey(__eaP.elem,__eaP.w,1),
      bullets:__eaP.bullets.map(b=>({kind:b.kind,el:b._el,inf:b._inf,lv:b._infLv,seat:b.seat})),png:c.toDataURL('image/png')};}''')
    (OUT/f'{elem}-{slot}.png').write_bytes(base64.b64decode(q.pop('png').split(',',1)[1]));q.update(element=elem,slot=slot);rows.append(q)
   print(elem+': 9 native carriers captured',flush=True)
  browser.close()
finally:stop()
(OUT/'audit.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2),encoding='utf-8')
from PIL import Image,ImageDraw
for e in elements:
 sheet=Image.new('RGB',(9*240,376),(9,15,23));d=ImageDraw.Draw(sheet)
 for w in range(9):
  sheet.paste(Image.open(OUT/f'{e}-{w}.png').convert('RGB'),(w*240,36));d.text((w*240+6,8),rows[elements.index(e)*9+w]['name'],fill='white')
 sheet.save(OUT/(e+'-family.jpg'))
print(json.dumps(dict(cases=len(rows),errors=errors)),flush=True)
sys.exit(1 if errors or any(r['error'] for r in rows) else 0)
