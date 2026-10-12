"""Own the elemental ammunition sheets and registry together. Authored pixels only.

Crop equal source cells, register the rigid nose, apply one common proportional
scale per bank, and pad to even 128px cells. Never interpolate animation poses.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'_ART_SOURCES/element_arsenal_1011'
DEST=ROOT/'assets/game/shared/player_weapons/element_arsenal_1011'
ELEMENTS=['fire','kinetic','lightning','water','ice','chrome','toxic','dark']
# Measured rigid casing spans in the first source cell. Exhaust is excluded.
BODY_HEIGHT={'fire_round':90,'fire_missile':131,'kinetic_round':131,'kinetic_missile':167,
 'lightning_round':157,'lightning_missile':188,'water_round':153,'water_missile':156,
 'ice_round':144,'ice_missile':139,'chrome_round':165,'chrome_missile':175,
 'toxic_round':172,'toxic_missile':140,'dark_round':151,'dark_missile':147}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 DEST.mkdir(parents=True,exist_ok=True);banks={};audit={}
 for el in ELEMENTS:
  for kind in ['round','missile']:
   name=el+'_'+kind;source=SOURCE/(name+'_raw.png')
   if not source.exists():continue
   im=Image.open(source).convert('RGBA');W,H=im.size;cells=[]
   assert .9<W/H<1.1,(name,'expected 4x4 layout')
   for i in range(16):
    rect=[round(i%4*W/4),round(i//4*H/4),round((i%4+1)*W/4),round((i//4+1)*H/4)]
    c=im.crop(rect);p=np.asarray(c);a=p[:,:,3];h,w=a.shape
    # Opaque central nose: excludes changing outboard energy and long exhaust.
    core=(a[:,int(w*.43):int(w*.57)]>200)
    rows=np.where(core.sum(axis=1)>max(3,w*.013))[0];rows=rows[rows<h*.5]
    assert len(rows),name
    top=int(rows[0]);nose=a[top:top+max(8,int(h*.13)),int(w*.34):int(w*.66)]>210
    yy,xx=np.where(nose);x=float(np.median(xx)+int(w*.34))
    # Anchor the rigid nose at the same coordinate; fixed offset, not alpha centre.
    pos=[x,float(top+BODY_HEIGHT[name]/2)]
    bb=c.getbbox();assert bb
    cells.append(dict(im=c,rect=rect,anchor=pos,bounds=bb))
   pivot=[64,48];scale=min(min((pivot[0]-6)/max(1,q['anchor'][0]-q['bounds'][0]),
    (122-pivot[0])/max(1,q['bounds'][2]-q['anchor'][0]),(pivot[1]-6)/max(1,q['anchor'][1]-q['bounds'][1]),
    (122-pivot[1])/max(1,q['bounds'][3]-q['anchor'][1])) for q in cells)
   atlas=Image.new('RGBA',(512,512));frames=[];hashes=[]
   for i,q in enumerate(cells):
    c=q['im'];scaled=c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.NEAREST)
    xy=[round(pivot[j]-q['anchor'][j]*scale) for j in range(2)]
    frame=Image.new('RGBA',(128,128));frame.alpha_composite(scaled,tuple(xy));bb=frame.getbbox()
    assert bb and min(bb[:2])>=4 and max(bb[2:])<=124,(name,i,'clipped export')
    hashes.append(hashlib.sha256(frame.tobytes()).hexdigest())
    atlas.alpha_composite(frame,((i%4)*128,(i//4)*128));frames.append([i%4*128,i//4*128,128,128])
    q['translation']=xy;q.pop('im')
   assert len(set(hashes))==16,(name,'duplicate frames')
   out=DEST/(name+'.png');atlas.save(out,optimize=True)
   banks[name]=dict(key='ea11_'+name,path=out.relative_to(ROOT).as_posix(),frames=frames,
    size=[128,128],pivot=pivot,fps=24,bodyHeight=round(BODY_HEIGHT[name]*scale,3),element=el,kind=kind,sha256=sha(out))
   audit[name]=dict(source=source.relative_to(ROOT).as_posix(),source_sha256=sha(source),scale=scale,
    source_size=[W,H],registration=cells,distinct_frames=len(set(hashes)))
 result=dict(version=1,elements=ELEMENTS+['wind'],banks=banks)
 (DEST/'manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 (SOURCE/'registration.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
 (ROOT/'assets/element_arsenal_art_1011.js').write_text('/* Owned by build_element_arsenal_1011.py. */\nconst EA11_ART='+json.dumps(result,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
 print('Registered',len(banks),'banks;',len(banks)*16,'authored poses')
if __name__=='__main__':build()
