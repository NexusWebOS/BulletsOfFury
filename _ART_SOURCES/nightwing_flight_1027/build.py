"""Source-derived BOF Nightwing flight cells and escort royal-blue palette.
Run from _ART_SOURCES/nightwing_flight_1027 after installing into the repo.
No runtime resampling, rotation, tint, alpha synthesis or image compositing.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math,json,hashlib,os,subprocess
import numpy as np
W=Path(__file__).resolve().parent
R=Path(os.environ.get('BOF_REPO',str(W.parents[1])))
D=W/'compiled';D.mkdir(exist_ok=True)
dest=R/'assets/game/levels/stage_06/boss/nightwing_flight_1027';dest.mkdir(parents=True,exist_ok=True)
manifest={'banks':{},'escorts':{},'sources':{}}
old=json.loads((R/'_ART_SOURCES/nightwing_entrance_1027/compiled/manifest.json').read_text(encoding='utf-8'))
sheet=Image.open(R/old['whole']['path']).convert('RGBA')
def source(name,i=0):
 f=old['groups'][name]['start']+i
 return sheet.crop((f%8*272,f//8*272,f%8*272+272,f//8*272+272))
def cell(q,size):
 c=Image.new('RGBA',(size,size));c.alpha_composite(q,((size-q.width)//2,(size-q.height)//2));return c
def turn(q,angle,scale=1,size=272):
 # Positive world angles turn clockwise. Source whole pose points south.
 if scale!=1:q=q.resize((round(q.width*scale),round(q.height*scale)),Image.Resampling.NEAREST)
 return cell(q.rotate(-angle*180/math.pi,Image.Resampling.NEAREST,expand=True),size)
def white(q):
 o=Image.new('RGBA',q.size,'white');o.putalpha(q.getchannel('A'));return o
def shadow(q):
 o=Image.new('RGBA',q.size,(3,14,31,0));o.putalpha(q.getchannel('A').point(lambda n:round(n*.32)));return o
def export(name,ff,shadows=False,hits=True):
 size=ff[0].width;cols=min(8,4096//size)
 for suffix,frames in [('',ff)]+([('_hit',[white(q)for q in ff])]if hits else[])+([('_shadow',[shadow(q)for q in ff])]if shadows else[]):
  key=name+suffix;out=Image.new('RGBA',(cols*size,math.ceil(len(ff)/cols)*size))
  for i,q in enumerate(frames):out.alpha_composite(q,(i%cols*size,i//cols*size))
  path=dest/(key+'.png');out.save(path,optimize=True)
  manifest['banks'][key]={'key':'nf29_'+key,'path':path.relative_to(R).as_posix(),'cw':size,'ch':size,'cols':cols,'frames':len(ff),'pivot':[size//2,size//2]}
 return ff
# Three genuinely authored bank attitudes, rotated offline in 11.25-degree steps.
# This preserves the accepted blue fuselage and P2 banking silhouettes.
heading=[]
for bank in ['south','bank_left','bank_right']:
 for i in range(32):heading.append(turn(source(bank,i%8 if bank=='south'else 0),i*math.tau/32))
export('heading',heading)
export('flyover',[turn(source('south',i),math.pi,1.6,432)for i in range(8)],True)
for side,label in [(-1,'drift_left'),(1,'drift_right')]:
 ff=[]
 for i in range(24):
  u=i/23;amount=math.sin(math.pi*u);base=source('bank_left'if side<0 else'bank_right')if amount>.22 else source('south',i%8)
  # north -> inside lateral -> south; bank returns flat as speed settles.
  ff.append(turn(base,math.pi+side*math.pi*u,1.6-.95*(u*u*(3-2*u)),432))
 export(label,ff,True)
export('approach',[turn(source('south',i%8),0,.65+.35*(i/15)**.65)for i in range(16)],True)
export('death_large',[turn(source('damaged',i%8),i*math.tau/32,1.6,432)for i in range(32)],False,False)
# Dedicated escort family: all five existing authored motion banks, not a global
# recolour of Stratus aircraft used elsewhere in the campaign.
s=(R/'assets/biome_fleet_art_1022.js').read_text(encoding='utf-8')
bf=json.loads(s[s.index('{'):s.rindex('}')+1]);model=bf['models']['sky_stratus']
target=np.array([65,105,225.],dtype=float);lum=np.array([.2126,.7152,.0722]);Y=target@lum
preview=[];stats={}
for name,a in model['banks'].items():
 path=R/a['path'];im=Image.open(path).convert('RGBA');pix=np.array(im);rgb=pix[:,:,:3].astype(float);y=rgb@lum
 hi=rgb.max(2);lo=rgb.min(2);sat=(hi-lo)/np.maximum(1,hi)
 # Neutral armour and its blue-grey shadows only; keep cyan light/ordnance and
 # nearly-black outlines intact, with ordered royal-blue metal shading.
 mask=(pix[:,:,3]>0)&(y>29)&((sat<.34)|((rgb[:,:,2]>rgb[:,:,0])&(rgb[:,:,1]-rgb[:,:,0]<35)&(sat<.55)))
 stops=[0,29,85,145,200,230,255];colors=np.array([[0,0,0],[10,15,32],[16,32,95],[25,55,160],[40,90,225],[100,150,255],[235,245,255]])
 ramp=np.stack([np.interp(y,stops,colors[:,k])for k in range(3)],axis=2)
 pix[:,:,:3][mask]=np.clip(np.rint(ramp[mask]),0,255).astype(np.uint8)
 out=Image.fromarray(pix);outpath=dest/('royal_'+name+'.png');out.save(outpath,optimize=True)
 entry=dict(a,key='nf29_royal_'+name,path=outpath.relative_to(R).as_posix());manifest['escorts'][name]=entry
 stats[name]={'changed':int(mask.sum()),'max_luminance_error':float(np.max(np.abs((pix[:,:,:3]@lum-y)[mask]))),'alpha_identical':bool(np.array_equal(pix[:,:,3],np.array(im)[:,:,3]))}
 preview.append(out.crop((0,0,128,128)).resize((256,256),Image.Resampling.NEAREST))
 manifest['sources'][a['path']]=hashlib.sha256(path.read_bytes()).hexdigest()
manifest['palette_audit']=stats
manifest['sources'][old['whole']['path']]=hashlib.sha256((R/old['whole']['path']).read_bytes()).hexdigest()
(dest/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(R/'assets/nightwing_flight_art_1027.js').write_text('"use strict";\nconst NF29_ART='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
o=Image.new('RGBA',(1296,864),(13,25,38,255));draw=ImageDraw.Draw(o)
samples=[('TURN / BANK',heading[32+6]),('NORTH FLYOVER',Image.open(dest/'flyover.png').crop((0,0,432,432))),('SHRINKING DRIFT',Image.open(dest/'drift_right.png').crop((4*432,432,5*432,864))),('ROYAL IDLE',preview[0]),('ROYAL ATTACK',preview[1]),('ROYAL DRIFT',preview[2])]
for i,(name,q)in enumerate(samples):o.alpha_composite(q,(i%3*432+(432-q.width)//2,i//3*432+(432-q.height)//2));draw.text((i%3*432+12,i//3*432+12),name,fill='white')
o.save(W/'flight-poses.png')
ase=os.environ.get('ASEPRITE_EXE')
if ase:subprocess.run([ase,'--batch',str(dest/'heading.png'),'--save-as',str(W/'nightwing-flight.aseprite')],check=True,capture_output=True)
print(json.dumps({'banks':len(manifest['banks']),'cells':sum(a['frames']for a in manifest['banks'].values()),'escort_banks':len(stats),'palette':stats}))

