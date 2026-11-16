from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'_shots/crossed_fate_1115';S=R/'_ART_SOURCES/crossed_fate_1115';A=R/'assets/game/shared/cinematics/crossed_fate_1115'
S.mkdir(parents=True,exist_ok=True);A.mkdir(parents=True,exist_ok=True)
raw=S/'generated-medals.png'
im=Image.open(raw).convert('RGBA');w,h=im.size
tiles=[im.crop((i*w//2,0,(i+1)*w//2,h))for i in range(2)];boxes=[x.getbbox()for x in tiles]
box=(min(b[0]for b in boxes),min(b[1]for b in boxes),max(b[2]for b in boxes),max(b[3]for b in boxes));k=min(228/(box[2]-box[0]),228/(box[3]-box[1]))
meta={'version':1,'source':'Current TC119 modular Storm Cannon, current HF28 Harrier and built-in imagegen medal pair. No replacement aircraft generation.','banks':{},'icons':{}}
for name,tile in zip(['crossed_fate','road_not_taken'],tiles):
 tile=tile.crop(box);tile=tile.resize((round(tile.width*k),round(tile.height*k)),Image.Resampling.NEAREST)
 c=Image.new('RGBA',(256,256));c.alpha_composite(tile,((256-tile.width)//2,(256-tile.height)//2));dest=A/(name+'.png');c.save(dest)
 meta['icons'][name]={'key':'fate15_'+name,'path':str(dest.relative_to(R)).replace('\\','/'),'w':256,'h':256,'pivot':[128,128],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
def bank(name,cells,body=576):
 assert cells and all(c.size==(800,800)for c in cells)
 bounds=[c.getbbox()for c in cells];left=max(0,min(b[0]for b in bounds)-4)//2*2;top=max(0,min(b[1]for b in bounds)-4)//2*2
 right=min(800,(max(b[2]for b in bounds)+5)//2*2);bottom=min(800,(max(b[3]for b in bounds)+5)//2*2)
 crop=[left,top,right,bottom];cw=right-left;ch=bottom-top
 B={'w':cw,'h':ch,'pivot':[400-left,400-top],'sourceCanvas':[800,800],'sharedCrop':crop,'bodyWidth':body,'frames':len(cells),'pages':[],'cells':[]}
 for start in range(0,len(cells),16):
  chunk=cells[start:start+16];cols=min(4,len(chunk));sheet=Image.new('RGBA',(cw*cols,ch*math.ceil(len(chunk)/cols)));key='fate15_'+name+'_'+str(start//16)
  for f,c in enumerate(chunk):
   assert c.getbbox()and all(v%2==0 for v in c.size)
   sheet.alpha_composite(c.crop(crop),((f%cols)*cw,(f//cols)*ch));B['cells'].append([key,(f%cols)*cw,(f//cols)*ch]);c.save(S/(name+'-%02d.png'%(start+f)))
  dest=A/(name+'-'+str(start//16)+'.webp');sheet.save(dest,lossless=True)
  B['pages'].append({'key':key,'path':str(dest.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'w':sheet.width,'h':sheet.height})
 meta['banks'][name]=B
for direction in ['nw','w']:
 cells=[]
 for i in range(16):
  source=S/('storm-native-'+direction+'-%02d.png'%i);c=Image.open(source).convert('RGBA');assert c.getbbox();cells.append(c)
 bank('storm_'+direction,cells)
 shadow=[]
 for c in cells:
  s=Image.new('RGBA',c.size,(0,0,0,0));s.putalpha(c.getchannel('A').point(lambda a:round(a*.27)));shadow.append(s)
 bank('storm_'+direction+'_shadow',shadow)

south=Image.open(S/'harrier-south.png').convert('RGBA');broken=Image.open(S/'harrier-broken.png').convert('RGBA')
def posed(src,angle):
 c=Image.new('RGBA',(800,800));c.alpha_composite(src,((800-src.width)//2,(800-src.height)//2))
 return c.rotate(-angle*180/math.pi,resample=Image.Resampling.NEAREST,center=(400,400))
for name,a in [('harrier_nw',math.pi-.52),('harrier_north',math.pi)]:
 c=posed(south,a);bank(name,[c],512);s=Image.new('RGBA',c.size);s.putalpha(c.getchannel('A').point(lambda a:round(a*.27)));bank(name+'_shadow',[s],512)
bank('harrier_crash',[posed(broken,math.pi+4*math.pi*i/47)for i in range(48)],512)
(S/'manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8',newline='\n')
(R/'assets/crossed_fate_art_1115.js').write_text('"use strict";\nconst FATE15_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
print(json.dumps({'medalSource':im.size,'medalSharedCrop':box,'banks':{n:b['frames']for n,b in meta['banks'].items()},'icons':list(meta['icons'])}),flush=True)
