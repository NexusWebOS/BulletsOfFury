from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,math,hashlib,numpy as np,shutil,sys
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/pixellab_hammer_1023';O=W/'shipping';O.mkdir(exist_ok=True)
master=Image.open(W/'locked-hammer.png').convert('RGBA');assert hashlib.sha256((W/'locked-hammer.png').read_bytes()).hexdigest()=='0f3efa84f4a49f01aa1c8d21bcfc6233333621267920752c795a00159ece5641';unit=.13;master=master.resize((round(master.width*unit),round(master.height*unit)),Image.Resampling.NEAREST);pivot=(round(334*unit),round(442*unit));prop=Image.new('RGBA',(640,640));prop.alpha_composite(master,(320-pivot[0],320-pivot[1]));headOnly=Image.new('RGBA',(640,640));headOnly.alpha_composite(master.crop((0,0,round(535*unit),master.height)),(320-pivot[0],320-pivot[1]))
hands=[[[118,186],[180,158]],[[110,166],[160,148]],[[121,115],[168,115]],[[135,77],[162,78]],[[137,77],[155,90]],[[144,132],[143,111]],[[143,180],[144,157]],[[143,195],[144,173]],[[143,195],[144,173]],[[134,195],[173,174]],[[127,190],[181,158]],[[118,186],[180,158]]]
def red(im):
 a=np.array(im);v=a[:,:,:3].astype(float);hi=v.max(2);lo=v.min(2);m=(((v[:,:,2]>v[:,:,0]*1.15)&(v[:,:,2]>70))|((hi-lo<35)&(hi>24)&(hi<220))|((v[:,:,2]>v[:,:,1]*1.2)&(v[:,:,2]>35)))&(a[:,:,3]>0);value=np.maximum(hi,(v@np.array([.2126,.7152,.0722]))*1.4)
 for c,f in enumerate([1,.25,.29]):a[:,:,c][m]=np.clip(value[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
frames=[];rig=[]
for i,hs in enumerate(hands):
 raw=Image.open(W/f'pixellab-slam-raw/{i:02}.png').convert('RGBA');body=Image.new('RGBA',(640,640));body.alpha_composite(raw.resize((448,448),Image.Resampling.NEAREST),(96,64));points=[(round(96+x*1.75),round(64+y*1.75))for x,y in hs];dx=points[1][0]-points[0][0];dy=points[1][1]-points[0][1];angle=math.degrees(math.atan2(dy,dx));g=[sum(p[j]for p in points)/2 for j in range(2)];a=math.radians(angle);head=[round(g[0]-110*math.cos(a)),round(g[1]-110*math.sin(a))];rot=prop.rotate(-angle,Image.Resampling.NEAREST,center=(320,320));im=Image.new('RGBA',(640,640))
 if i==2:im.alpha_composite(rot,(head[0]-320,head[1]-320));im.alpha_composite(body)
 else:im.alpha_composite(body);im.alpha_composite(rot,(head[0]-320,head[1]-320))
 for x,y in points:
  bb=(x-13,y-12,x+14,y+13);im.alpha_composite(body.crop(bb),(bb[0],bb[1]))
 contact=headOnly.rotate(-angle,Image.Resampling.NEAREST,center=(320,320)).getbbox();tip=[head[0],head[1]+contact[3]-321];bounds=im.getbbox();assert min(bounds[:2])>0 and max(bounds[2:])<640
 frames.append(im);rig.append({'frame':i,'head':head,'tip':tip,'hands':points,'sourceHands':hs,'angle':angle,'bodyUnit':1.75,'weaponUnit':.13,'bounds':bounds,'weaponBehindBody':i==2})
A={'banks':{},'sheets':{},'phases':{'corrupt':{'windEnd':4,'strikeEnd':7,'recoverStart':8}},'sources':{'bodyJob':'63077c51-07d4-43f3-857f-12359cf84d0e','sideJob':'85c23e09-9c8e-4845-82dc-ee94694dd636','lockedWeaponSHA256':'0f3efa84f4a49f01aa1c8d21bcfc6233333621267920752c795a00159ece5641'}}
jumpFrames=frames[:];jumpRig=rig[:];sideFrames=[];sideRig=[]
sideHands=[[[151,154],[166,145]],[[168,141],[192,147]],[[182,137],[212,145]],[[171,139],[194,147]],[[122,145],[144,153]],[[101,151],[126,161]],[[96,159],[120,168]],[[111,143],[137,153]],[[142,148],[165,157]],[[169,154],[194,163]],[[192,158],[214,170]],[[195,167],[218,178]],[[151,156],[175,166]]]
for source,flip in [(0,False),(1,False),(2,False),(3,False),(4,False),(5,False),(6,False),(7,False),(0,True),(1,True),(2,True),(3,True),(4,True),(5,True),(6,True),(-1,False)]:
 if source<0:sideFrames.append(jumpFrames[0].copy());sideRig.append({**jumpRig[0],'frame':15,'sourceFrame':'jump-ready'});continue
 raw=Image.open(W/f'pixellab-sides-v3-raw/{source:02}.png').convert('RGBA');body=Image.new('RGBA',(640,640));body.alpha_composite(raw.resize((448,448),Image.Resampling.NEAREST),(96,74));points=[(round(96+x*1.75),round(74+y*1.75))for x,y in sideHands[source]]
 if flip:body=ImageOps.mirror(body);points=[(639-x,y)for x,y in points]
 dx=points[1][0]-points[0][0];dy=points[1][1]-points[0][1];angle=math.degrees(math.atan2(dy,dx));g=[sum(p[j]for p in points)/2 for j in range(2)];a=math.radians(angle);head=[round(g[0]-110*math.cos(a)),round(g[1]-110*math.sin(a))];rot=prop.rotate(-angle,Image.Resampling.NEAREST,center=(320,320));im=Image.new('RGBA',(640,640));behind=False
 if behind:im.alpha_composite(rot,(head[0]-320,head[1]-320));im.alpha_composite(body)
 else:im.alpha_composite(body);im.alpha_composite(rot,(head[0]-320,head[1]-320))
 for x,y in points:
  bb=(x-13,y-12,x+14,y+13);im.alpha_composite(body.crop(bb),(bb[0],bb[1]))
 bounds=im.getbbox();assert min(bounds[:2])>0 and max(bounds[2:])<640;sideFrames.append(im);sideRig.append({'frame':len(sideFrames)-1,'sourceFrame':source,'mirroredBodyOffline':flip,'head':head,'tip':head,'hands':points,'angle':angle,'bounds':bounds,'weaponBehindBody':behind,'bodyUnit':1.75,'weaponUnit':.13,'bankRootOffset':[0,10]})
for name,ims,rig in [('corrupt_jump',jumpFrames,jumpRig),('corrupt_jump_red',[red(f)for f in jumpFrames],jumpRig),('corrupt_sides',sideFrames,sideRig),('corrupt_sides_red',[red(f)for f in sideFrames],sideRig)]:
 sheet=Image.new('RGBA',(640*4,640*math.ceil(len(ims)/4)));white=sheet.copy();rows=[]
 for i,im in enumerate(ims):
  x,y=i%4*640,i//4*640;sheet.alpha_composite(im,(x,y));hit=Image.new('RGBA',(640,640),'white');hit.putalpha(im.getchannel('A'));white.alpha_composite(hit,(x,y));m=rig[i];rows.append({'key':f'ha21_ma23_{name}_{i}','sheet':'ma23_'+name,'cell':[x,y,640,640],'w':640,'h':640,'pivot':[320,354],'bounds':m['bounds'],'tip':m['tip']if i==7 and name.startswith('corrupt_jump') else m['head'],'glow':m['head'],'white':f'ha21_ma23_{name}_hit_{i}','kind':'corrupt','bank':name,'frame':i,'_hf22':True,'_hc23':True,'_ma23':True,'weaponUnit':.13,'armed':True})
 for suffix,im in [('',sheet),('_hit',white)]:
  p=O/(name+suffix+'.webp');im.save(p,lossless=True,exact=True,method=5);A['sheets']['ma23_'+name+suffix]={'key':'nca_ma23_'+name+suffix,'path':'_shots/animation_audit_1023/candidate/'+p.name,'w':im.width,'h':im.height,'legacy':False}
 A['banks'][name]=rows
js='"use strict";\nconst MA23_CANDIDATE='+json.dumps(A,separators=(',',':'))+';\nfor(const s of Object.values(MA23_CANDIDATE.sheets))XART._src[s.key]=s.path;for(const rows of Object.values(MA23_CANDIDATE.banks))for(const a of rows){BOFX.cells[a.key]=[a.sheet,...a.cell];BOFX.cells[a.white]=[a.sheet+"_hit",...a.cell];}Object.assign(HF22_ART.banks,MA23_CANDIDATE.banks);Object.assign(HF22_ART.sheets,MA23_CANDIDATE.sheets);Object.assign(HF22_ART.phases,MA23_CANDIDATE.phases);\n'
(O/'candidate.js').write_text(js,encoding='utf-8');(O/'rig.json').write_text(json.dumps({'jump':jumpRig,'sides':sideRig},indent=2));(O/'manifest.json').write_text(json.dumps(A,indent=2));frames=jumpFrames;c=Image.new('RGB',(640*4,670*3),'#13202c');d=ImageDraw.Draw(c);gifs=[]
for i,im in enumerate(frames):c.paste(im,(i%4*640,i//4*670),im);d.text((i%4*640+6,i//4*670+644),str(i),fill='white');f=Image.new('RGB',(640,640),'#13202c');f.paste(im,(0,0),im);gifs.append(f)
c.thumbnail((1280,1100));c.save(O/'contact.png');gifs[0].save(O/'candidate.gif',save_all=True,append_images=gifs[1:],duration=100,loop=0)
c=Image.new('RGB',(640*4,670*4),'#13202c');d=ImageDraw.Draw(c)
for i,im in enumerate(sideFrames):c.paste(im,(i%4*640,i//4*670),im);d.text((i%4*640+6,i//4*670+644),str(i),fill='white')
c.thumbnail((1280,1400));c.save(O/'sides-contact.png')
print(json.dumps({'frames':len(frames),'bodyCanvas':[640,640],'propSources':1,'unit':.13,'testOnly':True}))
if '--stage-test' in sys.argv:
 target=R/'_shots/animation_audit_1023/candidate';target.mkdir(parents=True,exist_ok=True)
 for p in O.glob('*.webp'):shutil.copy2(p,target/p.name)
 shutil.copy2(O/'candidate.js',target/'candidate.js');print('Copied to ignored QA folder; production index and active banks unchanged.')
