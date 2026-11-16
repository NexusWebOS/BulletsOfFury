from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/city-atlas';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];M=json.loads((R/'_ART_SOURCES/cinema_overnight_1116/city-atlas.json').read_text(encoding='utf8'))
for a in M['changes']:
 old=Image.open(R/a['source']).convert('RGBA');new=Image.open(R/a['path']).convert('RGBA');checks.append({'name':a['oldKey']+' preserves every original pixel and pads to even extent','ok':new.size==tuple(a['size'])and new.crop((0,0,*old.size)).tobytes()==old.tobytes()and new.height%2==new.width%2==0})
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?night-atlas=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}')
 p.wait_for_function('()=>{city16Warm();for(const p of NQA16)XART.rdy(p.oldKey);return city16Warm()&&NQA16.every(p=>XART.rdy(p.oldKey)&&XART.rdy(p.key))}',polling=50)
 q=p.evaluate('''()=>{let total=0,bad=[],odd=[];for(const[name,B]of Object.entries(CITY16_ART.banks)){if(B.w%2||B.h%2)odd.push(name);for(let f=0;f<B.frames;f++){const c=B.cells[f],im=XART.get(c[0]);total++;if(!im||c[1]<0||c[2]<0||c[1]+B.w>im.width||c[2]+B.h>im.height)bad.push({name,f,c,size:im?[im.width,im.height]:null});}}return{total,bad,odd};}''')
 checks.append({'name':'All4160 current runtime cells have even frames and valid decoded source bounds','ok':q['total']==4160 and not q['bad']and not q['odd'],'data':q})
 affected=json.loads((O/'before.json').read_text(encoding='utf8'))['badCells'];q=p.evaluate('''cells=>{const base=XART.get;const pairs=new Map(NQA16.map(p=>[p.key,p.oldKey]));let different=0,comparisons=[];function render(q,legacy){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#183247';ctx.fillRect(0,0,cv.width,cv.height);if(legacy)XART.get=function(k){return base.call(this,pairs.get(k)||k)};try{city16Bank(q.bank,q.frame,220,200);}finally{XART.get=base;ctx.restore();}return ctx.getImageData(0,0,cv.width,cv.height).data;}for(const q of cells){const a=render(q,true),z=render(q,false);let n=0;for(let i=0;i<a.length;i++)if(a[i]!==z[i])n++;different+=n;comparisons.push({bank:q.bank,frame:q.frame,different:n});}return{different,comparisons};}''',affected)
 checks.append({'name':'All20 repaired cells draw identical native pixels at unchanged pivots','ok':q['different']==0 and len(q['comparisons'])==20,'data':q})
 p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#0b1724';ctx.fillRect(0,0,VW,VH);for(let f=0;f<16;f++)city16Bank('thrust-d0-r0',f,55+f%4*110,70+Math.floor(f/4)*115)}");p.locator('#screen').screenshot(path=str(O/'native-sixteen-frames.png'))
 checks.append({'name':'No page console or asset errors','ok':not errors,'data':errors});b.close()
(O/'after.json').write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Original pixel preservation and current runtime all-cell bounds, plus20 actual Canvas baseline/corrected draw comparisons. No altered sprite silhouettes, animation timings, headings or pivots.'},indent=2),encoding='utf8');print(json.dumps({'pass':sum(q['ok']for q in checks),'fail':[q['name']for q in checks if not q['ok']]},indent=2));assert all(q['ok']for q in checks)
