"""Animate the existing whole Tidal hull's liquid apertures, preserving armor.

No new hull, independent body sections, per-frame fit or runtime recoloring.
32 fixed 320x256 frames per native damage state. Source alpha is identical.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,math
R=Path(__file__).resolve().parents[1]
OUT=R/'assets/game/levels/stage_09/boss/tidal_water_1025';OUT.mkdir(parents=True,exist_ok=True)
PROOF=R/'_shots/warden_tidal_1025/art';PROOF.mkdir(parents=True,exist_ok=True)
def readconst(p,name):return json.JSONDecoder().raw_decode(p.read_text(encoding='utf8').split(name+'=',1)[1])[0]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()[:12]
m=readconst(R/'assets/manifest.js','window.BOFX');o=readconst(R/'assets/stage1_water_art_1020.js','const S1W20_ART')
ocean=Image.open(R/o['path']).convert('RGBA');Y,X=np.indices((256,320));banks={};proof=[]
art={'width':320,'height':256,'frames':32,'columns':4,'fps':12,'pivot':[160,128],
     'sockets':{'L':[120,226],'R':[200,226],'C':[160,237],'circleL':[96,87],'circleR':[224,87]},'sheets':{},'banks':{}}
for state in ['intact','damaged','critical']:
 key='ns9_tidal_'+state;cell=m['cells'][key];src=Image.open(R/m['img'][key]).convert('RGBA').crop((cell[1],cell[2],cell[1]+320,cell[2]+256));a=np.array(src)
 # Only blue liquid INSIDE measured apertures. Armor, outlines, seams, alpha,
 # cannon trunnions and the central metal cross stay byte-identical.
 mask=Image.new('L',(320,256));d=ImageDraw.Draw(mask)
 wing=[(23,76),(41,80),(61,82),(69,110),(58,108),(40,98),(29,86)]
 for pts in [wing,[(320-x,y)for x,y in wing],[(151,39),(156,34),(165,35),(168,44),(168,67),(162,71),(152,68)],[(117,174),(126,174),(126,191),(117,191)],[(194,174),(203,174),(203,191),(194,191)],[(153,203),(166,203),(164,228),(159,236),(154,223)]]:d.polygon(pts,fill=255)
 d.ellipse((128,88,192,150),fill=255)
 for cx in [96,224]:d.ellipse((cx-17,70,cx+17,104),fill=255)
 blue=(a[:,:,2].astype(float)>a[:,:,0]*1.30+12)&(a[:,:,1].astype(float)>a[:,:,0]*1.15+10)&(a[:,:,2]>85)&(a[:,:,3]>0)
 select=(np.array(mask)>0)&blue;sheet=Image.new('RGBA',(1280,2048));changed=[];frames=[]
 for f in range(32):
  b=a.copy();sx,sy,w,h=o['cells'][f];water=np.array(ocean.crop((sx,sy,sx+w,sy+h)))
  tex=water[(Y+f*2)%224,X%224,:3].astype(float)
  # Existing authored blue ocean phases move within the fixed reservoirs.
  b[select,:3]=np.round(a[select,:3]*.70+tex[select]*.30).astype(np.uint8)
  for cx,sign in [(96,1),(224,-1)]:
   angle=sign*f/32*math.tau;dx=X-cx;dy=Y-87
   xx=np.clip(np.rint(cx+dx*math.cos(angle)+dy*math.sin(angle)).astype(int),0,319)
   yy=np.clip(np.rint(87-dx*math.sin(angle)+dy*math.cos(angle)).astype(int),0,255)
   wh=select&((X-cx)**2+(Y-87)**2<17**2)&select[yy,xx]
   b[wh,:3]=a[yy[wh],xx[wh],:3]
  assert np.array_equal(a[~select],b[~select]) and np.array_equal(a[:,:,3],b[:,:,3])
  im=Image.fromarray(b);sheet.alpha_composite(im,((f%4)*320,(f//4)*256));changed.append(int(np.any(a[:,:,:3]!=b[:,:,:3],axis=2).sum()))
  frames.append({'key':'wt25_'+state+'_'+str(f),'rect':[f%4*320,f//4*256,320,256]})
  if f in [0,8,16,24]:proof.append((state+' '+str(f),im))
 p=OUT/(state+'.webp');sheet.save(p,lossless=True,method=6)
 art['sheets'][state]={'key':'wt25_'+state,'path':p.relative_to(R).as_posix(),'sha12':sha(p)}
 art['banks'][key]={'sheet':'wt25_'+state,'frames':frames,'source':m['img'][key],'sourceCell':cell,'liquidPixels':int(select.sum()),'changed':changed}
 Image.fromarray((select*255).astype('uint8')).save(PROOF/(state+'-liquid-mask.png'))
registry=R/'assets/warden_tidal_art_1025.js';registry.write_text("'use strict';\n// Owned by _BUILD_SOURCE/build_warden_tidal_1025.py. Armor and source alpha are preserved.\nconst WT25_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
c=Image.new('RGB',(1280,3*280),(10,16,24));d=ImageDraw.Draw(c)
for i,(label,im)in enumerate(proof):x=i%4*320;y=i//4*280;c.paste(im,(x,y),im);d.text((x+4,y+258),label,fill='white')
c.save(PROOF/'whole-hull-contact.png')
(PROOF/'manifest.json').write_text(json.dumps(art,indent=2),encoding='utf8')
print(json.dumps({'banks':3,'frames':96,'sourceAlphaIdentical':True,'unchangedArmor':True,'bytes':sum(p.stat().st_size for p in OUT.glob('*.webp'))}))
