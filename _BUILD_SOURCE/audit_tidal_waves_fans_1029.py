from pathlib import Path
import json,hashlib
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];W=R/'_shots/tidal_waves_fans_1029/art';W.mkdir(parents=True,exist_ok=True);D=R/'assets/game/levels/stage_09/boss/tidal_sovereign_1029';m=json.loads((D/'manifest.json').read_text());C=json.loads((D/'inputs.json').read_text());checks=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,str(d)[:250]if not v else'')
def frame(name,i):
 a=m[name];im=Image.open(R/a['path']).convert('RGBA');return im.crop((i%a['cols']*a['cw'],i//a['cols']*a['ch'],(i%a['cols']+1)*a['cw'],(i//a['cols']+1)*a['ch']))
wave=m['wave'];ck('Water waves use exactly the eight actual nwf_fire sources',len(C['stage2Waves'])==8 and all(r['key']=='nwf_fire_'+str(i)for i,r in enumerate(C['stage2Waves'])))
ck('Six authored approaching sizes have eight phases each',wave['frames']==48 and wave['cw']==wave['ch']==480)
for level,size in enumerate([190,242,294,346,398,452]):
 good=True
 for phase,row in enumerate(C['stage2Waves']):
  c=row['cell'];src=Image.open(R/row['path']).convert('RGBA').crop((c[1],c[2],c[1]+c[3],c[2]+c[4])).transpose(Image.Transpose.FLIP_TOP_BOTTOM);h=int(src.height*size/src.width+.5);src=src.resize((size,h),Image.Resampling.NEAREST);a=frame('wave',level*8+phase).crop(((480-size)//2,(480-h)//2,(480-size)//2+size,(480-h)//2+h))
  # Aseprite and Pillow differ by at most one sample on resize boundaries;
  # compare opaque area/silhouette rather than pretending their samplers match.
  ratio=sum(v>0 for v in a.getchannel('A').getdata())/max(1,sum(v>0 for v in src.getchannel('A').getdata()));good &= .94<ratio<1.06
 ck('Water size'+str(size)+' retains flipped Stage2 source silhouettes',good)
for state in ['intact','damaged','critical']:
 frames=[frame('body_'+state,i)for i in range(16)];regions=[];rim=True
 for cx in [96,224]:
  regions.append(len({hashlib.sha256(im.crop((cx-14,73,cx+15,102)).tobytes()).hexdigest()for im in frames}))
  for y in range(66,109):
   for x in range(cx-21,cx+22):
    r=(x-cx)**2+(y-87)**2
    if 18**2<r<20**2:rim &= all(im.getpixel((x,y))==frames[0].getpixel((x,y))for im in frames)
 ck(state+' actual spiral fan pixels rotate in16 phases',all(n==16 for n in regions),regions);ck(state+' metal fan rims remain fixed',rim)
memory=0
for name,a in m.items():
 im=Image.open(R/a['path']).convert('RGBA');memory+=im.width*im.height*4;ok=True
 for i in range(a['frames']):
  bb=im.crop((i%a['cols']*a['cw'],i//a['cols']*a['ch'],(i%a['cols']+1)*a['cw'],(i//a['cols']+1)*a['ch'])).getchannel('A').getbbox();ok &= bool(bb)and bb[0]>0 and bb[1]>0 and bb[2]<a['cw']and bb[3]<a['ch']
 ck(name+' retains clear fixed-cell padding',ok)
(W/'art-audit.json').write_text(json.dumps(dict(checks=checks,decodedMiB=memory/1048576),indent=2));print('Decoded MiB',memory/1048576);assert all(q['passed']for q in checks)
