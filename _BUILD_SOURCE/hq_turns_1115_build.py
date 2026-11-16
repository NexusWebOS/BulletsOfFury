from pathlib import Path
import sys,json,base64,hashlib,shutil
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/hq_turns_1115';INSTALL=OUT/'install';ART=INSTALL/'assets/game/shared/cinematics/hq_turns_1115';SRC=INSTALL/'_ART_SOURCES/hq_turns_1115'
ART.mkdir(parents=True,exist_ok=True);SRC.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
SCRIPT=r'''()=>{
 const k=Math.max(888/418,488/236),r={x:12,y:12+(488-236*k)/2,w:418*k,h:236*k},out=[],order=[...HQ19_SQUAD,'decker','axel'];
 const oldBank=player._bank,oldFrame=player._thrustFrame;
 try{for(let index=0;index<order.length;index++){
  const pk=order[index],cx=r.x+r.w*.5,padY=r.y+r.h*.727,own=HQ20_KILLS.filter(k=>k.pilot===pk),last=own.at(-1),side=pk==='decker'?-1:1;
  let origin=null;if(last){const enemy=hq20EnemyPose(last.id,3.4+last.at,r),x=cx+side*r.w*.13,y=padY+18;origin={x,y,h:96,heading:Math.atan2(enemy.y-y,enemy.x-x)+Math.PI/2};}
  const heading=value=>{const u=Math.min(.999999,Math.max(0,value)),v=.4*u+.6*u*u,cx=r.x+r.w*.5,p0=origin||{x:cx,y:r.y+r.h*.451,h:25},side=index%2===0?-1:1,p1={x:p0.x,y:p0.y+110},p2={x:p0.x+side*r.w*.28,y:r.y+r.h*.83},p3={x:cx+side*r.w*.64,y:r.y+r.h+210},iv=1-v,dx=3*iv*iv*(p1.x-p0.x)+6*iv*v*(p2.x-p1.x)+3*v*v*(p3.x-p2.x),dy=3*iv*iv*(p1.y-p0.y)+6*iv*v*(p2.y-p1.y)+3*v*v*(p3.y-p2.y),target=Math.atan2(dx,-dy);if(!origin)return target;const initial=origin.heading||0,delta=((target-initial+Math.PI*3)%(Math.PI*2))-Math.PI;return initial+delta*hq19Ease(u/.24);};
  for(let frame=0;frame<20;frame++){
   const u=frame/19,a=heading(u),before=heading(Math.max(0,u-.025)),delta=((a-before+Math.PI*3)%(Math.PI*2))-Math.PI;
   const duration=origin?.34:.86,envelope=Math.sin(Math.PI*clamp(u/duration,0,1)),bank=(delta>=0?1:-1)*.46*envelope;
   const right=SHIP_BANK_FLIP[pk]?bank<0:bank>0,key='ship_'+pk+(Math.abs(bank)<.12?'':Math.abs(bank)<.48?(right?'_pv3':'_pv1'):(right?'_pv4':'_pv0'));
   const im=D27_RAW_GET(key),c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.translate(128,128);g.rotate(a);const h=104,w=h*im.width/im.height;
   player._thrustFrame=frame%6;g.drawImage(im,-w/2,-h/2,w,h);pf27PlaneThrustDraw(g,key,0,0,w,h,.95);
   out.push({pilot:pk,index,frame,u,heading:a,bank,sourceKey:key,sourceSize:[im.width,im.height],png:c.toDataURL('image/png')});
  }
 }}finally{player._bank=oldBank;player._thrustFrame=oldFrame;}
 return out;
}'''
with sync_playwright()as w:
 b=w.chromium.launch();p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto('http://127.0.0.1:8765/index.html?hq-turn-exports');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{for(const pk of HQ19_PILOTS)for(const suffix of ['', '_pv0','_pv1','_pv2','_pv3','_pv4'])for(const tail of ['','_g1','_g2'])XART.rdy('ship_'+pk+suffix+tail);}")
 p.wait_for_function("()=>HQ19_PILOTS.every(pk=>['','_pv0','_pv1','_pv2','_pv3','_pv4'].every(s=>XART.rdy('ship_'+pk+s)&&XART.rdy('ship_'+pk+s+'_g1')&&XART.rdy('ship_'+pk+s+'_g2')))")
 data=p.evaluate(SCRIPT);assert not errors,errors;b.close()
meta={'generator':'Native Chromium export of actual approved banking poses and native animated exhaust; no generated replacement aircraft','cell':[256,256],'pivot':[128,128],'physicalHullHeight':104,'fps':20/1.3,'flightDuration':1.3,'pilots':{}}
for pk in dict.fromkeys(a['pilot']for a in data):
 frames=[a for a in data if a['pilot']==pk];sheet=Image.new('RGBA',(1280,1024));cells=[];records=[];(SRC/pk).mkdir(exist_ok=True)
 for a in frames:
  im=Image.open(__import__('io').BytesIO(base64.b64decode(a.pop('png').split(',')[1]))).convert('RGBA');assert im.size==(256,256);assert im.getbbox();f=a['frame'];im.save(SRC/pk/('%02d.png'%f));sheet.alpha_composite(im,((f%5)*256,(f//5)*256));cells.append(im);records.append(a)
 dest=ART/(pk+'.webp');sheet.save(dest,lossless=True);meta['pilots'][pk]={'key':'hq21_turn_'+pk,'path':str(dest.relative_to(INSTALL)).replace('\\','/'),'w':256,'h':256,'cols':5,'frames':20,'pivot':[128,128],'bodyHeight':104,'side':'southwest'if frames[0]['index']%2==0 else'southeast','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'poses':records}
 preview=Image.new('RGB',(1280,1024),'#17283a');preview.paste(sheet,mask=sheet.getchannel('A'));preview.resize((960,768),Image.Resampling.NEAREST).save(OUT/(pk+'-turns.jpg'),quality=94)
 gifs=[]
 for cell in cells:
  bg=Image.new('RGB',cell.size,'#17283a');bg.paste(cell,mask=cell.getchannel('A'));gifs.append(bg)
 gifs[0].save(OUT/(pk+'-turn.gif'),save_all=True,append_images=gifs[1:],duration=65,loop=0)
for p in OUT.glob('ship_*.png'):shutil.copy2(p,SRC/p.name)
(SRC/'native-banks.json').write_text((OUT/'native-banks.json').read_text(encoding='utf8'),encoding='utf8')
(OUT/'art-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8',newline='\n')
(INSTALL/'assets/hq_turn_art_1115.js').write_text('"use strict";\nconst HQ21_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
print('Built180 actual banking/turn frames across all9 pilot aircraft; fixed256 cells and physical pivot')
