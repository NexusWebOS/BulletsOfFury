"""Thunderhead: generated disjoint modules, authored reactor/aura and wind beams.
Fixed world-size cells. No runtime image transforms, alpha synthesis or readbacks.
"""
from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
import numpy as np,json,math,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
A=W/'authored';F=A/'frames';F.mkdir(parents=True,exist_ok=True)
O=R/'assets/game/levels/stage_06/boss/thunderhead_modular_1104';O.mkdir(parents=True,exist_ok=True)
sheet=Image.open(W/'thunderhead-modular-generated.png').convert('RGBA')
meta={'version':'1104','banks':{},'masks':{},'pages':{},'sources':{},'model':{},'owner':'_BUILD_SOURCE/thunderhead_modular_1104/build_modular.py'};bits=bytearray()
def clean(im,cut=100):
 a=np.array(im);a[a[:,:,3]<cut]=0;return Image.fromarray(a)
def crop(box):return clean(sheet.crop(box))
def normalized(im,size,scale,anchor):
 out=Image.new('RGBA',size);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
 out.alpha_composite(im,(round(size[0]/2-anchor[0]*scale),round(size[1]/2-anchor[1]*scale)));return out
def white(im):
 out=Image.new('RGBA',im.size,'white');out.putalpha(im.getchannel('A'));return out
def wreck(im):
 a=np.array(im);v=a[:,:,:3].max(2).astype(float);a[:,:,:3]=np.stack([v*.15,v*.19,v*.22],2).astype('uint8');return Image.fromarray(a)
def glow(im,level,phase,core=False):
 a=np.array(im);v=a[:,:,:3].astype(float);yy,xx=np.mgrid[:im.height,:im.width]
 energy=(v[:,:,1]>v[:,:,0]*1.18)&(v[:,:,2]>v[:,:,0]*1.12)&(a[:,:,3]>80)
 pulse=(1+np.sin(yy*.13+xx*.07-phase*math.pi/4))/2
 strength=(.07+level*.15)*( .4+.6*pulse)
 v[energy]=np.clip(v[energy]*(1+strength[energy,None])+np.array([12,22,24])*level,0,255)
 # Material-authored storm light travels across the chrome as well as the
 # reactor glass. Dark ribbing stays readable; original alpha is unchanged.
 lum=v.max(2);band=((pulse>.58)*.7+(pulse>.82)*.3)*level/3
 v=np.clip(v+lum[:,:,None]*band[:,:,None]*np.array([.025,.15,.22]),0,255)
 a[:,:,:3]=v.astype('uint8');return Image.fromarray(a)
def aura(im):
 frames=[];alpha=im.getchannel('A');base=np.array(alpha)
 for level in range(4):
  for phase in range(4):
   step=[0,.45,1,.45][phase];radius=2+level*2+round(step*(level+1));outer=np.array(alpha.filter(ImageFilter.MaxFilter(radius*2+1)))
   edge=np.maximum(0,outer.astype('int16')-base.astype('int16')).astype('uint8')
   a=np.zeros((im.height,im.width,4),dtype='uint8');a[:,:,:3]=[55+level*24,185+level*16,210+level*15];a[:,:,3]=(edge*(.2+level*.17+step*.18)).clip(0,255).astype('uint8')
   # Hot inner rim uses source shape rather than a rectangle or a round bubble.
   inner=np.maximum(0,base.astype('int16')-np.array(alpha.filter(ImageFilter.MinFilter(3))).astype('int16')).astype('uint8')
   a[:,:,3]=np.maximum(a[:,:,3],(inner*(.16+level*.15+step*.15)).clip(0,255).astype('uint8'));frames.append(Image.fromarray(a))
 return frames
def bank(name,frames,fps=16,pivot=None,mask=False):
 cw,ch=frames[0].size;assert cw%2==ch%2==0 and all(f.size==(cw,ch)for f in frames)
 cols=max(1,min(8,1536//cw));per=cols*max(1,1536//ch);cells=[]
 for start in range(0,len(frames),per):
  part=frames[start:start+per];page=Image.new('RGBA',(cols*cw,math.ceil(len(part)/cols)*ch));key='tm115_'+name+'_'+str(start//per)
  for i,im in enumerate(part):page.alpha_composite(im,(i%cols*cw,i//cols*ch));cells.append([key,i%cols*cw,i//cols*ch])
  p=O/(name+'_'+str(start//per)+'.png');page.save(p,optimize=True);meta['pages'][key]={'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':page.size}
 meta['banks'][name]={'cw':cw,'ch':ch,'frames':len(frames),'fps':fps,'pivot':pivot or[cw/2,ch/2],'cells':cells}
 d=F/name;d.mkdir(exist_ok=True)
 for i,im in enumerate(frames):im.save(d/(f'{i:03}.png'))
 if mask:
  cells=[]
  for im in frames:
   a=np.array(im)[:,:,3]>80;yy,xx=np.where(a);x0,y0,x1,y1=int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1);offset=len(bits);raw=np.packbits(a[y0:y1,x0:x1].ravel(),bitorder='little');bits.extend(raw.tobytes());cells.append([x0,y0,x1-x0,y1-y0,offset])
  meta['masks'][name]=cells

# Measured standalone generated regions; the second/third row intrude across
# the requested grid gutters, so true source rectangles preserve the pod caps.
hull=crop((421,16,835,388));hull=normalized(hull,(576,576),1.3,(209-421+418,210-16))
# Reactors detach at their collar seams; top crown/nose remain hull structure.
core=crop((946,90,1138,333));core=normalized(core,(192,224),.72,(1045-946,212-90))
gun_specs=[((94,442,325,780),(210,556),(210,756)),((480,440,737,780),(627,550),(552,743)),((939,442,1198,785),(1045,556),(1120,751))]
guns=[];recoil=[];bores=[]
for box,root,bore in gun_specs:
 im=crop(box);anchor=(root[0]-box[0],root[1]-box[1]);guns.append(normalized(im,(192,192),.28,anchor));recoil.append(normalized(im,(192,192),.28,(anchor[0],anchor[1]+8)));bores.append([round((bore[0]-root[0])*.28,2),round((bore[1]-root[1])*.28,2)])
pods=[];podbores=[]
for box,root,bore in [((54,801,358,1245),(211,1018),(211,1194)),((476,801,784,1245),(626,1018),(626,1194))]:
 im=crop(box);pods.append(normalized(im,(192,288),.53,(root[0]-box[0],root[1]-box[1])));podbores.append([round((bore[0]-root[0])*.53,2),round((bore[1]-root[1])*.53,2)])
bank('hull',[glow(hull,l,p*2)for l in range(4)for p in range(4)],mask=True);bank('hull_aura',aura(hull));bank('core',[glow(core,l,p,True)for l in range(4)for p in range(8)],mask=True);bank('core_hit',[white(core)]);bank('core_aura',aura(core));bank('core_wreck',[wreck(core)])
gunframes=guns+recoil
bank('gun',gunframes+[glow(f,l,p*2)for l in range(1,4)for p in range(4)for f in gunframes],mask=True);bank('gun_hit',[white(f)for f in gunframes]);bank('gun_wreck',[wreck(f)for f in guns]);bank('gun_aura',aura(guns[0]))
for i,p in enumerate(pods):
 bank('pod'+str(i),[glow(p,l,phase)for l in range(4)for phase in range(8)],mask=True);bank('pod'+str(i)+'_hit',[white(p)]);bank('pod'+str(i)+'_wreck',[wreck(p)]);bank('pod'+str(i)+'_aura',aura(p))

# One crop and proportional scale for the entire generated16frame beam loop.
raw=Image.open(W/'wind-beam-generated.png').convert('RGBA');beam=[]
for i in range(16):
 cell=raw.crop((i%4*256,i//4*384,i%4*256+256,i//4*384+384));a=np.array(cell);a[a[:,:,3]<24]=0;cell=Image.fromarray(a).crop((28,20,232,375));cell=cell.resize((round(cell.width*1.3),round(cell.height*1.3)),Image.Resampling.NEAREST)
 out=Image.new('RGBA',(288,512));out.alpha_composite(cell,((288-cell.width)//2,0));beam.append(out)
start=[];end=[]
for i in range(6):
 im=beam[i].copy();a=np.array(im);height=round((i+1)/6*512);a[height:]=0;a[:,:,3]=(a[:,:,3]*min(1,(i+1)/4)).astype('uint8');start.append(Image.fromarray(a))
 im=beam[(i+8)%16].copy();a=np.array(im);a[:,:,3]=(a[:,:,3]*(5-i)/6).astype('uint8');end.append(Image.fromarray(a))
bank('wind_beam',start+beam+end,24,[144,0])

def P(x,y):return[round(288+(x-209)*1.3,2),round(288+(y-210)*1.3,2)]
meta['model']={'cell':576,'world':576,'core':P(209,215),'coreBox':[112,160],
 'guns':[{'mount':P(x,y),'bore':bores[0],'recoilOffset':-2.24,'size':192,'hitBox':[70,100]}for x,y in [(135,147),(282,147),(135,289),(282,289)]],
 'pressures':[{'mount':P(x,198),'bore':podbores[i],'size':192,'hitBox':[130,224]}for i,x in enumerate([55,363])],
 'engines':[P(x,44)for x in[99,164,267,328]],'bodyBox':[560,470], 'turretBores':bores,'sourceHullPivot':[209,210]}
mask=O/'opaque_masks.bin';mask.write_bytes(bits);meta['maskPath']=mask.relative_to(R).as_posix();meta['maskBytes']=len(bits)
for n in ['thunderhead-modular-generated.png','wind-beam-generated.png']:meta['sources'][n]=hashlib.sha256((W/n).read_bytes()).hexdigest()
(O/'manifest.json').write_text(json.dumps(meta,indent=2));(A/'manifest.json').write_text(json.dumps(meta,indent=2));(R/'assets/thunderhead_modular_art_1104.js').write_text('"use strict";\nconst TM115_ART='+json.dumps(meta,separators=(',',':'))+';\n')
lua='local root=app.params.root\nlocal banks={'+','.join('{name="'+n+'",n='+str(b['frames'])+',fps='+str(b['fps'])+'}'for n,b in meta['banks'].items())+'}\n'
lua+='for _,b in ipairs(banks)do local first=Image{fromFile=root.."/frames/"..b.name.."/000.png"};local s=Sprite(first.width,first.height,ColorMode.RGB);s.layers[1].name=b.name.." / fixed native cells";for i=0,b.n-1 do if i>0 then s:newEmptyFrame(i+1)end;local im=Image{fromFile=root.."/frames/"..b.name.."/"..string.format("%03d",i)..".png"};s:newCel(s.layers[1],i+1,im,Point(0,0));s.frames[i+1].duration=1/b.fps end;s:saveAs(root.."/"..b.name..".aseprite");s:close()end\n'
(A/'author.lua').write_text(lua)
# Review the real assembled module kit at runtime scale before installation.
unit=hull.copy()
def place(im,at):unit.alpha_composite(im,(round(at[0]-im.width/2),round(at[1]-im.height/2)))
place(core,meta['model']['core'])
for p in meta['model']['pressures']:place(pods[meta['model']['pressures'].index(p)],p['mount'])
for p in meta['model']['guns']:place(guns[0],p['mount'])
unit.save(A/'assembled.png');contact=Image.new('RGB',(1152,768),'#152531');contact.paste(unit,(0,0),unit)
for i,im in enumerate([core,guns[0],pods[0],pods[1]]):contact.paste(im,(576+(i%2)*250,i//2*300),im)
contact.save(A/'contact.jpg',quality=95)
print('Built',len(meta['banks']),'banks;',sum(b['frames']for b in meta['banks'].values()),'frames;',round(sum(p.stat().st_size for p in O.glob('*.png'))/1048576,2),'MB;',len(bits),'collision bytes')
