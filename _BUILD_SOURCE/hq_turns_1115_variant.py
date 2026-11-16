from pathlib import Path
import ast,sys,json,base64,hashlib,io
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/hq_turns_1115';INSTALL=OUT/'install';SRC=INSTALL/'_ART_SOURCES/hq_turns_1115';ART=INSTALL/'assets/game/shared/cinematics/hq_turns_1115';sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
tree=ast.parse((ROOT/'_BUILD_SOURCE/hq_turns_1115_build.py').read_text(encoding='utf8'));SCRIPT=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='SCRIPT'for t in n.targets))
SCRIPT=SCRIPT.replace("order=[...HQ19_SQUAD,'decker','axel']","order=['lizzie']").replace('for(let index=0;index<order.length;index++){','for(let j=0;j<order.length;j++){const index=5;').replace('const pk=order[index]','const pk=order[j]')
with sync_playwright()as w:
 b=w.chromium.launch();p=b.new_page();p.set_default_timeout(120000);p.goto('http://127.0.0.1:8765/index.html?hq21alternate');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF);p.evaluate("()=>{applyLizzieSkin(true);for(const s of ['','_pv0','_pv1','_pv2','_pv3','_pv4'])for(const tail of ['','_g1','_g2'])XART.rdy('ship_lizzie'+s+tail);}");p.wait_for_function("()=>['','_pv0','_pv1','_pv2','_pv3','_pv4'].every(s=>XART.rdy('ship_lizzie'+s)&&XART.rdy('ship_lizzie'+s+'_g1')&&XART.rdy('ship_lizzie'+s+'_g2'))")
 data=p.evaluate(SCRIPT);b.close()
assert len(data)==20
pk='lizzie_b42';(SRC/pk).mkdir(exist_ok=True);sheet=Image.new('RGBA',(1280,1024));cells=[]
for a in data:
 im=Image.open(io.BytesIO(base64.b64decode(a.pop('png').split(',')[1]))).convert('RGBA');a['pilot']=pk;f=a['frame'];im.save(SRC/pk/('%02d.png'%f));sheet.alpha_composite(im,((f%5)*256,(f//5)*256));bg=Image.new('RGB',im.size,'#17283a');bg.paste(im,mask=im.getchannel('A'));cells.append(bg)
dest=ART/(pk+'.webp');sheet.save(dest,lossless=True);meta=json.loads((OUT/'art-manifest.json').read_text(encoding='utf8'));base=meta['pilots']['lizzie'];assert hashlib.sha256(dest.read_bytes()).hexdigest()!=base['sha256'];meta['pilots'][pk]={'key':'hq21_turn_lizzie_b42','path':str(dest.relative_to(INSTALL)).replace('\\','/'),'w':256,'h':256,'cols':5,'frames':20,'pivot':[128,128],'bodyHeight':104,'side':'southeast','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'poses':data,'variant':'actual native applyLizzieSkin(true)'}
cells[0].save(OUT/(pk+'-turn.gif'),save_all=True,append_images=cells[1:],duration=65,loop=0)
(OUT/'art-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8',newline='\n');(INSTALL/'assets/hq_turn_art_1115.js').write_text('"use strict";\nconst HQ21_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8',newline='\n');print('Added actual B42 alternate aircraft turn bank without changing the original nine banks')
