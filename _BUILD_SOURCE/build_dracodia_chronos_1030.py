"""RD74. PixelLab pose-preserving re-author + one immutable canonical hammer.
All transforms, palettes, code/glow and depth samples are authored offline.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
from scipy.ndimage import distance_transform_edt
import numpy as np,json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_ART_SOURCES/dracodia_chronos_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;D=R/'_ART_SOURCES/dracodia_chronos_1030';O=R/'assets/game/shared/combat/dracodia_chronos_1030';O.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
SIZE=512;PIV=[256,250];K=1.6;OFF=[51,64]
tracking=json.loads((R/'_ART_SOURCES/chronos_motion_1025/tracking.json').read_text());hands={(a['bank'].replace('_regular',''),a['frame']):a['hand'] for a in tracking if a['bank'].endswith('_regular')}
for i in range(9):hands['idle',i]=hands['retract',16]
for bank in ['gun_recall','rage_recall']:
 for i in range(9):hands[bank,i]=[128+(hands['retract',16][0]-128)*i/8,154+(hands['retract',16][1]-154)*i/8]
masterpath=R/'_ART_SOURCES/hammer_consistency_1023/weapon-master.png';master=Image.open(masterpath).convert('RGBA');master=master.resize((round(master.width*.13),round(master.height*.13)),Image.Resampling.NEAREST)
HEAD=(round(334*.13),round(442*.13));GRIP=(HEAD[0]+110,HEAD[1]);prop=Image.new('RGBA',(SIZE,SIZE));prop.alpha_composite(master,(256-GRIP[0],256-GRIP[1]));HREL=[HEAD[0]-GRIP[0],HEAD[1]-GRIP[1]]
ART={'version':1,'cell':SIZE,'pivot':PIV,'banks':{},'weaponSHA256':hashlib.sha256(masterpath.read_bytes()).hexdigest(),'weaponUnit':.13,'source':'PixelLab transfer_outfit from approved Chronos body poses; locked HC23 weapon-master; no runtime sprite transforms.'}; audit=[];cache={}
def palette(im,mat):
 a=np.array(im);v=a[:,:,:3].astype(float);hi=v.max(2);lo=v.min(2);lum=v@np.array([.2126,.7152,.0722]);sat=hi-lo;purple=(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>v[:,:,0]*.93)&(sat>22)
 if mat=='chrome':
  neutral=(sat<38)&(lum>30)&(lum<235);v[neutral]=np.clip(v[neutral]*1.34+10,0,246);v[purple]=np.minimum(246,v[purple]*1.20)
 elif mat=='red':
  m=purple|((v[:,:,2]>v[:,:,0]*1.12)&(sat>25))|((sat<38)&(lum>25)&(lum<222));val=np.minimum(255,np.maximum(hi,lum*1.5));target=np.stack([val,lum*.20,lum*.28],2);v[m]=target[m]
 a[:,:,:3]=np.clip(v,0,255).astype('uint8');return Image.fromarray(a)
def body(bank,f):
 key=(bank,f)
 if key in cache:return cache[key].copy()
 im=Image.open(W/f'generated/{bank}/{f:02}.png').convert('RGBA');a=np.array(im);orig=Image.open(W/f'inputs/{bank}/{f:02}.png').convert('RGBA');v=np.array(orig);m=(v[:,:,0]>85)&(v[:,:,2]>85)&(v[:,:,0]>v[:,:,1]*1.8)&(v[:,:,2]>v[:,:,1]*1.8)&(v[:,:,3]>50)
 # Erase only the explicit tiny input registration dot at the measured fist.
 h=hands.get((bank,f));yy,xx=np.indices(m.shape)
 if h:m&=(xx-h[0])**2+(yy-h[1])**2<9**2
 else:m[:]=False
 if m.any():
  _,ix=distance_transform_edt(m,return_indices=True);a[m]=a[ix[0][m],ix[1][m]]
 im=Image.fromarray(a);cache[key]=im;return im.copy()
def angle(bank,u):
 if bank=='windup':return -math.pi/2-.12+(-.4+math.pi/2+.12)*u
 if bank=='strike':return -.4+(math.pi+.2)*u
 if bank=='retract':return math.pi-.2+(-math.pi/2-.12+math.pi*2-math.pi+.2)*u
 if bank=='left':return -math.pi/2-.12+(-math.pi*.75+math.pi/2+.12)*u
 if bank=='right':return -math.pi/2-.12+(math.pi*.75+math.pi/2+.12)*u
 return -math.pi/2-.12
def code(im,phase,level=2):
 a=im.getchannel('A');rim=a.filter(ImageFilter.MaxFilter(3+2*level));rim=Image.fromarray(np.maximum(0,np.array(rim).astype(int)-np.array(a).astype(int)).astype('uint8'))
 out=Image.new('RGBA',im.size,(255,18,54,0));out.putalpha(rim.point(lambda v:v//(3 if level==1 else 2)));out.alpha_composite(im)
 ink=Image.new('RGBA',im.size);d=ImageDraw.Draw(ink);mask=np.array(a)
 for y in range(20,492,17):
  x=(y*7+phase*11)%260+126
  for dx,dy in [(0,0),(2,0),(0,2),(0,4),(2,4),(4,4),(4,6)]:
   if mask[y+dy,x+dx]>180:d.rectangle((x+dx,y+dy,x+dx+1,y+dy+1),fill=(255,80,110,255))
 out.alpha_composite(ink);return out
def bake(bank,f,mat='regular',empty=False,theta=None,depth=1,charged=0):
 b=palette(body(bank,f),mat);full=Image.new('RGBA',(SIZE,SIZE));full.alpha_composite(b.resize((410,410),Image.Resampling.NEAREST),tuple(OFF));bodymask=full.getchannel('A').copy();h=hands.get((bank,f),[75,162]);grip=[OFF[0]+h[0]*K,OFF[1]+h[1]*K];theta=angle(bank,f/16) if theta is None else theta;phi=theta+math.pi/2;c=math.cos(phi);s=math.sin(phi);tip=[grip[0]+HREL[0]*c-HREL[1]*s,grip[1]+HREL[0]*s+HREL[1]*c]
 if not empty:
  tool=palette(prop,mat if mat=='red' else 'regular').rotate(-phi*180/math.pi,Image.Resampling.NEAREST,center=(256,256));full.alpha_composite(tool,(round(grip[0]-256),round(grip[1]-256)))
  # Re-layer the original visible glove over the rigid handle, offline only.
  hand=Image.new('RGBA',full.size);hand.alpha_composite(b.resize((410,410),Image.Resampling.NEAREST),tuple(OFF));am=Image.new('L',full.size);ImageDraw.Draw(am).ellipse((grip[0]-9,grip[1]-9,grip[0]+9,grip[1]+9),fill=255);hand.putalpha(Image.fromarray(np.minimum(np.array(hand.getchannel('A')),np.array(am))));full.alpha_composite(hand)
 if charged:full=code(full,f,charged)
 if depth!=1:
  k=depth;small=full.resize((round(SIZE*k),round(SIZE*k)),Image.Resampling.NEAREST);m=bodymask.resize(small.size,Image.Resampling.NEAREST);full=Image.new('RGBA',(SIZE,SIZE));at=[round(PIV[i]*(1-k)) for i in [0,1]];full.alpha_composite(small,tuple(at));bodymask=Image.new('L',(SIZE,SIZE));bodymask.paste(m,tuple(at));tip=[PIV[i]+(tip[i]-PIV[i])*k for i in [0,1]];grip=[PIV[i]+(grip[i]-PIV[i])*k for i in [0,1]]
 meta={'tip':[round(v,2) for v in tip],'grip':[round(v,2) for v in grip],'bounds':list(bodymask.getbbox() or [0,0,1,1]),'spans':spans(bodymask),'depth':depth,'empty':empty,'angle':theta}
 if bank=='palm':
  point=[(157,134),(175,123),(182,114),(190,108),(195,104),(198,102)][f];meta['muzzle']=[OFF[0]+point[0]*K,OFF[1]+point[1]*K]
 return full,meta
def spans(a):
 out=[]
 for row in np.array(a)>48:
  v=np.flatnonzero(np.diff(np.r_[False,row,False]));out.append(v.tolist())
 return out
contacts=[]
def emit(name,frames):
 # One even union crop per entire bank, never a per-frame fit or changing pivot.
 boxes=[im.getbbox()for im,m in frames];x0=max(0,min(b[0]for b in boxes)//2*2-2);y0=max(0,min(b[1]for b in boxes)//2*2-2);x1=min(SIZE,math.ceil(max(b[2]for b in boxes)/2)*2+2);y1=min(SIZE,math.ceil(max(b[3]for b in boxes)/2)*2+2);cw=x1-x0;ch=y1-y0
 cols=4;sheet=Image.new('RGBA',(cw*cols,ch*math.ceil(len(frames)/cols)));meta=[]
 for i,(im,m) in enumerate(frames):
  sheet.alpha_composite(im.crop((x0,y0,x1,y1)),(i%cols*cw,i//cols*ch));q={**m}
  for point in ['tip','grip','muzzle']:
   if point in m:q[point]=[m[point][0]-x0,m[point][1]-y0]
  q['bounds']=[m['bounds'][0]-x0,m['bounds'][1]-y0,m['bounds'][2]-x0,m['bounds'][3]-y0]
  if 'spans'in m:q['spans']=[[max(0,min(cw,x-x0))for x in row]for row in m['spans'][y0:y1]]
  meta.append(q)
 path=O/(name+'.webp');sheet.save(path,lossless=True)
 white=Image.new('RGBA',sheet.size,'white');white.putalpha(sheet.getchannel('A'));white.save(O/(name+'_hit.webp'),lossless=True)
 ART['banks'][name]={'key':'rd74_'+name,'path':path.relative_to(R).as_posix(),'hitKey':'rd74_'+name+'_hit','hitPath':(O/(name+'_hit.webp')).relative_to(R).as_posix(),'frames':len(frames),'cols':cols,'cw':cw,'ch':ch,'pivot':[PIV[0]-x0,PIV[1]-y0],'meta':meta}
 contacts.extend([(name,frames[i][0])for i in sorted(set([0,len(frames)//2,len(frames)-1]))]);audit.append({'bank':name,'count':len(frames),'weaponSHA256':ART['weaponSHA256']})
for mat in ['regular','chrome','red']:
 emit('idle_'+mat,[bake('idle',i,mat,charged=1 if mat=='red' else 0)for i in range(9)])
 for bank in ['takeoff','land','windup','strike','retract','left','right']:
  emit(bank+'_'+mat,[bake(bank,i,mat,charged=1 if mat=='red' else 0) for i in range(17)])
 emit('depart_'+mat,[bake('takeoff',i,mat,depth=1-.72*i/16) for i in range(17)])
 emit('approach_'+mat,[bake('windup',i,mat,depth=.28+.72*i/16,charged=1 if mat=='red' else 0) for i in range(17)])
 emit('empty_'+mat,[bake('strike',i,mat,empty=True,charged=1 if mat=='red' else 0) for i in range(17)])
 emit('empty_retract_'+mat,[bake('retract',i,mat,empty=True,charged=1 if mat=='red' else 0) for i in range(17)])
 emit('rage_'+mat,[bake('rage',i,mat,empty=True,charged=1 if mat=='red' else 0)for i in range(13)])
 emit('palm_'+mat,[bake('palm',i,mat,empty=True,charged=1 if mat=='red' else 0)for i in range(6)])
 emit('stun_'+mat,[bake('stun',i,mat,empty=True)for i in range(3)])
 emit('rage_recall_'+mat,[bake('rage_recall',i,mat,empty=True,charged=1 if mat=='red' else 0)for i in range(9)])
 emit('spin_'+mat,[bake('left' if i<16 else 'right',min(i%16*2,32-i%16*2),mat,theta=-math.pi/2+i/32*math.tau,charged=1 if mat=='red' else 0) for i in range(32)])
 # Detached throw is the identical prop, authored at64 headings.
 fs=[]
 for i in range(64):
  im=palette(prop,'red' if mat=='red' else 'regular').rotate(-i/64*360,Image.Resampling.NEAREST,center=(256,256));im=code(im,i,1) if mat=='red' else im;fs.append((im,{'tip':[256+HREL[0]*math.cos(i/64*math.tau),256+HREL[0]*math.sin(i/64*math.tau)],'grip':[256,256],'bounds':list(im.getbbox()),'empty':False,'depth':1}))
 emit('tool_'+mat,fs)
# Progressive chromium takeover on the exact same generated hold. No bubble.
fs=[]
for i in range(25):
 a,m=bake('retract',16,'regular');b,_=bake('retract',16,'chrome');aa=np.array(a);bb=np.array(b);yy,xx=np.indices(aa.shape[:2]);mask=(yy+i*7)%25<i;aa[mask]=bb[mask];im=Image.fromarray(aa);fs.append((code(im,i,1) if i>4 else im,m))
emit('activation',fs)
# The approved Chronos PixelLab flame pixels, isolated from his blue body,
# re-authored into blood-red/magenta energy behind Dracodia's generated body.
def flame(i,level=1):
 source=Image.open(R/f'_ART_SOURCES/chronos_motion_1025/frames/aura_regular/{4+i%21:02}.png').convert('RGBA');a=np.array(source);v=a[:,:,:3].astype(float);warm=(v[:,:,0]>100)&(v[:,:,0]>v[:,:,2]*1.4)&(v[:,:,1]>v[:,:,2]*1.2);near=distance_transform_edt(~warm)<5;mask=warm|((v.min(2)>190)&near);a[:,:,3]=np.where(mask,a[:,:,3],0);hi=v.max(2);a[:,:,:3]=np.stack([hi,hi*.18,hi*.32],2).astype('uint8');white=v.min(2)>215;a[:,:,:3][white]=[255,205,222];yy,xx=np.indices(mask.shape);a[:,:,3][(xx+yy*3)%16>round(level*15)]=0;out=Image.new('RGBA',(SIZE,SIZE));out.alpha_composite(Image.fromarray(a).resize((410,410),Image.Resampling.NEAREST),tuple(OFF));return out
# Rage is the same13 connected acting poses, with source flames and code.
fs=[]
for i in range(48):
 f=2+min(7,int(i/48*8));a,m=bake('rage',f,'red',empty=True);back=flame(i,min(1,.25+i/30));back.alpha_composite(code(a,i,1+i%3));fs.append((back,m))
emit('charge',fs)
emit('rage_flame',[(flame(i),{'tip':PIV,'grip':PIV,'bounds':[0,0,SIZE,SIZE],'empty':True,'depth':1})for i in range(21)])
fs=[]
for i in range(16):
 a,m=bake('idle',i%9,'red');fs.append((code(a,i,1+(i//3)%3),m))
emit('rage_idle',fs)
# Source-driven modular chaingun pose and barrel, recolored to this form.
raw=(R/'assets/chronos_contract_art_1025.js').read_text();ca=json.JSONDecoder().raw_decode(raw[raw.index('{'):])[0]
(W/'compiler-base.json').write_text(json.dumps({'artKeys':list(ca)},indent=2))
raw=(R/'assets/chronos_modular_art_1023.js').read_text();ga=json.JSONDecoder().raw_decode(raw[raw.index('{'):])[0]
def cell(art,row):
 im=Image.open(R/art['sheets'][row['sheet']]['path']).convert('RGBA');x,y,w,h=row['cell'];return im.crop((x,y,x+w,y+h))
def purple(im):
 a=np.array(im);v=a[:,:,:3].astype(float);sat=v.max(2)-v.min(2);m=(v[:,:,2]>v[:,:,0]*1.12)&(sat>25);hi=v.max(2);v[m]=np.stack([hi*.64,hi*.18,hi],2)[m];a[:,:,:3]=np.clip(v,0,255).astype('uint8');return Image.fromarray(a)
for mat in ['regular','chrome','red']:
 fs=[]
 for i in range(9):
  full,m=bake('gun_recall',i,mat,empty=True,charged=1 if mat=='red' else 0)
  if i<4:
   br=ga['banks']['barrel'][1+i%8];im=palette(purple(cell(ga,br)),mat);ar=np.array(im);yy,xx=np.indices(ar.shape[:2]);ar[:,:,3][(xx*3+yy)%16>=16-i*4]=0;full.alpha_composite(Image.fromarray(ar),(PIV[0]-br['pivot'][0],PIV[1]+32-br['pivot'][1]))
  fs.append((full,m))
 emit('gun_recall_'+mat,fs)
for mat in ['chrome','red']:
 fs=[]
 for i in range(24):
  f=[0,1,2,1][i%4];full,m=bake('gun',f,mat,empty=True);br=ga['banks']['barrel'][1+i%8];barrel=palette(purple(cell(ga,br)),mat)
  # A fixed mount on the generated two-hand grip; barrel recoil is baked.
  gx=PIV[0];gy=PIV[1]+32-(3 if i%3==0 else 0);full.alpha_composite(barrel,(gx-br['pivot'][0],gy-br['pivot'][1]));m['muzzle']=[gx,gy+ga['muzzle'][1]-br['pivot'][1]]
  gr=ga['banks']['hands'][[0,2,4][min(f,2)]];glove=purple(cell(ga,gr)).crop((64,130,320,386));glove=palette(glove.resize((184,184),Image.Resampling.NEAREST),mat);full.alpha_composite(glove.resize((294,294),Image.Resampling.NEAREST),(OFF[0]+58,OFF[1]+80));fs.append((full,m))
 emit('gun_'+mat,fs)
 fs=[]
 for i in range(17):
  full,m=bake('pickup',i,mat,empty=True)
  if i>=8:
   u=(i-8)/8;br=ga['banks']['barrel'][1+i%8];barrel=palette(purple(cell(ga,br)),mat);pad=Image.new('RGBA',(384,384));pad.alpha_composite(barrel,(192-br['pivot'][0],192-br['pivot'][1]));pad=pad.rotate(-180*(1-u),Image.Resampling.NEAREST,center=(192,192));gy=round(PIV[1]+139*(1-u)+32*u);full.alpha_composite(pad,(PIV[0]-192,gy-192))
   # Connected native glove pixels in front of the grip once the catch settles.
   if i>=14:
    gr=ga['banks']['hands'][0];glove=palette(purple(cell(ga,gr)).crop((64,130,320,386)).resize((184,184),Image.Resampling.NEAREST),mat);full.alpha_composite(glove.resize((294,294),Image.Resampling.NEAREST),(OFF[0]+58,OFF[1]+80))
  fs.append((full,m))
 emit('pickup_'+mat,fs)
ART['effects']={}
def effect(name,fs,piv):
 cw,ch=fs[0].size;cols=4;sheet=Image.new('RGBA',(cw*cols,ch*math.ceil(len(fs)/cols)))
 for i,im in enumerate(fs):sheet.alpha_composite(im,(i%cols*cw,i//cols*ch))
 path=O/(name+'.webp');sheet.save(path,lossless=True);ART['effects'][name]={'key':'rd74fx_'+name,'path':path.relative_to(R).as_posix(),'cw':cw,'ch':ch,'cols':cols,'frames':len(fs),'pivot':piv}
raw=(R/'assets/hammer_tactical_art_1023.js').read_text();ta=json.JSONDecoder().raw_decode(raw[raw.index('{'):])[0];effect('crate',[purple(cell(ta,row))for row in ta['banks']['crate']],[40,40])
wave=Image.open(R/'assets/game/shared/combat/chronos_wave_1025/wave_smooth.png').convert('RGBA')
for mat in ['purple','red']:
 fs=[]
 for f in range(28):
  im=wave.crop((f%8*320,f//8*640,f%8*320+320,f//8*640+640));im=purple(im) if mat=='purple' else palette(im,'red');fs.append(im)
 effect('wave_'+mat,fs,[160,24])
lightning=Image.open(R/'assets/game/levels/stage_05/boss/stage5_archmage_0916/combat_0926/hammer_lightning.png').convert('RGBA')
fs=[]
for f in range(8):
 im=lightning.crop((f%4*384+78,f//4*512+48,f%4*384+306,f//4*512+464));a=np.array(im);v=a[:,:,:3].astype(float);hi=v.max(2);v=np.stack([hi,hi*.18,hi*.29],2);white=hi>242;v[white]=[255,210,218];a[:,:,:3]=v.astype('uint8');fs.append(Image.fromarray(a).resize((38,640),Image.Resampling.NEAREST))
effect('lightning',fs,[19,0])
raw=(R/'assets/chronos_beam_art_1025.js').read_text();wa=json.JSONDecoder().raw_decode(raw[raw.index('{'):])[0];seed=cell(wa,wa['banks']['wave'][0]).crop((40,0,152,85));fs=[]
for i in range(16):
 k=(10+i*3);out=Image.new('RGBA',(64,64));im=palette(seed,'red').resize((k,k),Image.Resampling.NEAREST);out.alpha_composite(im,((64-k)//2,(64-k)//2));fs.append(out)
effect('gather',fs,[32,32])
manifest=O/'manifest.json';manifest.write_text(json.dumps(ART,separators=(',',':')));(R/'assets/dracodia_chronos_art_1030.js').write_text('"use strict";\nconst RD74_ART='+json.dumps(ART,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
preview=Image.new('RGB',(512*4,512*math.ceil(len(contacts)/4)),'#172332');dr=ImageDraw.Draw(preview)
for i,(n,im) in enumerate(contacts):x=i%4*512;y=i//4*512;preview.paste(im,(x,y),im);dr.text((x+5,y+5),n,fill='white')
preview.save(W/'authored-contact.png');(W/'compiler-audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps({'banks':len(ART['banks']),'frames':sum(a['frames']for a in ART['banks'].values()),'weaponSHA256':ART['weaponSHA256']}),flush=True)
