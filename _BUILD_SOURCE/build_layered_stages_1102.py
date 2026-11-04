"""LS112: reproduce approved terrain, independent material reels and Tesla power art.
All deformation, palette lighting and alpha changes happen OFFLINE here.
The runtime only selects frames and blits source pixels at their delivered size.
"""
from pathlib import Path
import json,math,hashlib,base64,subprocess
import numpy as np
from PIL import Image,ImageFilter,ImageChops
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/layered_stages_1102';D=R/'assets/game/shared/scenery/layered_1102';D.mkdir(parents=True,exist_ok=True)
M=json.loads((S/'manifest.json').read_text(encoding='utf8'))
out={'version':'layered-stages-1102','width':680,'levels':{},'materials':{},'banks':{},'masks':{},'sources':{}}
def save(im,name):
 p=D/name;im.save(p);out['sources'][name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':list(im.size)};return p.relative_to(R).as_posix()
def bank(name,frames,fps):
 w,h=frames[0].size;assert w%2==h%2==0
 cols=4;sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
 for i,im in enumerate(frames):assert im.size==(w,h);sheet.paste(im,(i%cols*w,i//cols*h))
 path=save(sheet,name+'.png');meta={'key':'ls112_'+name,'path':path,'w':w,'h':h,'frames':len(frames),'cols':cols,'fps':fps}
 out['banks'][name]=meta;return meta
native={'2':3568,'3':3568,'4':3568,'5':2208,'6':4488,'7':4204,'8':4096,'9':4096,'X':2760}
routes={}
def quilt_vertical(top,bottom,overlap=128):
 # A source-pixel ownership cut through a shared strip, not an opacity blend.
 a=np.array(top);b=np.array(bottom);left=a[-overlap:,:,:3].astype(float);right=b[:overlap,:,:3].astype(float)
 error=((left-right)**2).mean(2);cost=error.copy();parent=np.zeros(error.shape,np.int16)
 for x in range(1,error.shape[1]):
  candidates=np.stack([np.r_[np.inf,cost[:-1,x-1]],cost[:,x-1],np.r_[cost[1:,x-1],np.inf]])
  pick=np.argmin(candidates,axis=0);parent[:,x]=np.arange(overlap)+pick-1;cost[:,x]+=candidates[pick,np.arange(overlap)]
 path=np.zeros(error.shape[1],int);path[-1]=int(np.argmin(cost[:,-1]))
 for x in range(error.shape[1]-1,0,-1):path[x-1]=parent[path[x],x]
 result=Image.new('RGBA',(top.width,top.height+bottom.height-overlap));result.paste(top,(0,0));mix=np.array(top.crop((0,top.height-overlap,top.width,top.height)))
 for x,y in enumerate(path):mix[y:,x]=b[y:overlap,x]
 result.paste(Image.fromarray(mix),(0,top.height-overlap));result.paste(bottom.crop((0,overlap,bottom.width,bottom.height)),(0,top.height))
 return result
for level in M['levels']:
 k=level['id'];im=Image.open(S/level['terrain']).convert('RGBA')
 if k=='7':
  # Keep the actual stone aperture and its exact 343,310 gate socket at the
  # northern end; the new maintenance route is joined underneath, offline.
  cap=Image.open(S/'native-sewer.png').convert('RGBA').crop((0,0,680,1024))
  # Replace the concept's duplicated gate room with the real portal cap, then
  # join at matching industrial floor rows with one exact pixel-ownership cut.
  im=quilt_vertical(cap,im.crop((0,1024,680,im.height)),128)
 routes[k]=im
 out['levels'][k]={'key':'ls112_stage_'+k,'path':save(im,'stage-'+k+'.png'),'w':680,'h':im.height,'nativeRange':native[k],'material':level['material'],'repeat':level['repeat'],'passive':k in ['5','9'],'title':level['title']}
road=Image.open(S/'routes/stage-4-highway-loop.png').convert('RGBA')
out['highway']={'key':'ls112_highway','path':save(road,'highway.png'),'w':road.width,'h':road.height}
# Expanded escape uses the same new route beneath the unchanged real aperture.
# Its extra distance belongs to the existing rescue owner and never advances waves.
sewer=routes['7'];extra=6144;cut=1024;tile=Image.open(S/'terrain/stage-7-connector.png').convert('RGBA')
tile=tile.resize((680,tile.height*680//tile.width),Image.Resampling.NEAREST)
exit_im=Image.new('RGBA',(680,sewer.height+extra));exit_im.paste(sewer.crop((0,0,680,cut)),(0,0))
for y in range(cut,cut+extra,tile.height):exit_im.paste(tile.crop((0,0,680,min(tile.height,cut+extra-y))),(0,y))
exit_im.paste(sewer.crop((0,cut,680,sewer.height)),(0,cut+extra))
out['sewerExit']={'key':'ls112_sewer_exit','path':save(exit_im,'sewer-exit.png'),'w':680,'h':exit_im.height,'extra':extra,'gate':[343,310]}
# Real alpha footprint masks replace the old precomputed terrain's land data.
for k in ['2','3','4','7']:
 a=np.array(routes[k]);h,w=a.shape[:2];land=a[:,:,3]>230
 if k=='4':
  yy,xx=np.indices((h,w));land &= (xx>=285)&(xx<=395)
  land &= ~((yy>=2730)&(yy<=3070)&(xx>=273)&(xx<=406))
 cell=8;gw=math.ceil(w/cell);gh=math.ceil(h/cell);raw=np.zeros((gh,gw),np.uint8)
 for gy in range(gh):
  for gx in range(gw):raw[gy,gx]=255 if land[gy*cell:(gy+1)*cell,gx*cell:(gx+1)*cell].mean()>.94 else 0
 mask=np.array(Image.fromarray(raw).filter(ImageFilter.MinFilter(3)))>0
 bits=np.packbits(mask.reshape(-1),bitorder='big').tobytes()
 out['masks'][k]={'cell':cell,'gw':gw,'gh':gh,'bits':base64.b64encode(bits).decode(),'validCells':int(mask.sum())}
 Image.fromarray(mask.astype(np.uint8)*255).resize((gw*8,gh*8),Image.Resampling.NEAREST).save(S/('stage-'+k+'-drive-mask.png'))
# Material motion is authored as seamless fixed-frame ripples, never a live shader.
for m in M['materials']:
 name=m['id']
 if name=='lava':frames=[Image.open(S/f'liquids/lava/frames/{i:02d}.png').convert('RGBA') for i in range(8)]
 elif name=='space':frames=[Image.open(S/m['file']).convert('RGBA')]
 else:
  source=Image.open(S/m['file']).convert('RGBA').resize((256,256),Image.Resampling.NEAREST);a=np.array(source);yy,xx=np.indices((256,256));frames=[]
  for f in range(16):
   t=f*math.tau/16
   dx=np.rint(2*np.sin(t+yy*math.tau/64)+np.sin(t*2+xx*math.tau/128)).astype(int)
   dy=np.rint(2*np.cos(t+xx*math.tau/64)+np.sin(t*2+yy*math.tau/128)).astype(int)
   b=a[(yy+dy)%256,(xx+dx)%256].copy();b[:,-1]=b[:,0];b[-1]=b[0]
   frames.append(Image.fromarray(b))
 meta=bank('bed_'+name.replace('-','_'),frames,8 if name!='space' else 1);out['materials'][name]=meta
 if len(frames)>1:frames[0].save(S/(name+'-loop.gif'),save_all=True,append_images=frames[1:],duration=125,loop=0,disposal=2)
# Six exact sockets in the approved Stage4 plate. Never bake the preview ship.
x0,y0,cw,ch=64,2080,552,464;pad=routes['4'].crop((x0,y0,x0+cw,y0+ch));a=np.array(pad);rgb=a[:,:,:3].astype(float)
yy,xx=np.indices((ch,cw));blue=(a[:,:,2]>125)&(a[:,:,1]>80)&(a[:,:,2]>a[:,:,0]*1.22)&(a[:,:,3]>0)
sockets=[(145-x0,2143-y0),(530-x0,2143-y0),(113-x0,2258-y0),(563-x0,2258-y0),(114-x0,2400-y0),(563-x0,2400-y0)]
frames=[]
for f in range(24):
 t=f*math.tau/24;b=a.copy();strength=np.zeros((ch,cw),float)
 for n,(x,y) in enumerate(sockets):
  d=np.hypot(xx-x,yy-y);phase=t-d*.055+n*.63
  strength=np.maximum(strength,(.50+.50*np.sin(phase))*np.exp(-d/270))
 # Luminous pulses travel along the actual authored blue arcs, while the six
 # coil tips remain charged continuously. Source metal/ground/alpha stay exact.
 gain=.70+strength*.75
 for channel in range(3):
  values=np.clip(rgb[:,:,channel]*gain+(strength**5)*[60,65,50][channel],0,255)
  b[:,:,channel]=np.where(blue,values,a[:,:,channel]).astype('uint8')
 for n,(x,y) in enumerate(sockets):
  ring=(np.abs(((yy-y-12)%18)-9)<2)&(yy>y+12)&(yy<y+110)&(np.abs(xx-x)<(33+(yy-y)*.1))
  metal=(a[:,:,2]>a[:,:,0]*1.1)&(a[:,:,2]>38)&(a[:,:,0]<145)&ring
  amount=.20+.23*(.5+.5*math.sin(t+n*.5))
  for c,target in enumerate([50,170,250]):b[:,:,c]=np.where(metal,a[:,:,c]*(1-amount)+target*amount,b[:,:,c]).astype('uint8')
 frames.append(Image.fromarray(b))
out['tesla']={**bank('tesla_power',frames,18),'x':x0,'y':y0,'sockets':[[x+x0,y+y0] for x,y in sockets],'method':'Source-pixel 10/15 coil-band lighting and traveling arc palette pulses; fixed alpha/architecture'}
frames[0].save(S/'tesla-power.gif',save_all=True,append_images=frames[1:],duration=56,loop=0,disposal=2)
out['provenance']={'conceptManifest':hashlib.sha256((S/'manifest.json').read_bytes()).hexdigest(),'animation':'Authored source-derived frames; source RGB retained outside power masks; no runtime generated graphics','stage1':'Unchanged','nativeGameRules':'Existing stage/wave/boss/portal owners retained'}
(D/'manifest.json').write_text(json.dumps(out,separators=(',',':')),encoding='utf8')
(R/'assets/layered_stages_art_1102.js').write_text("'use strict';\nconst LS112_ART="+json.dumps(out,separators=(',',':'))+';\n',encoding='utf8')
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for name,a in pairs(M.banks)do local s=Sprite(a.w,a.h,ColorMode.RGB);local im=Image{fromFile=D..'/'..name..'.png'}
for i=0,a.frames-1 do if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(i%a.cols*a.w,math.floor(i/a.cols)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end
s:saveAs(D..'/'..name..'.aseprite');s:close()end
"""
(D/'author.lua').write_text(lua,encoding='utf8')
subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
print('BUILT',len(out['levels']),'routes;',sum(a['frames'] for a in out['banks'].values()),'authored material/power frames;',len(out['banks']),'Aseprite sources',flush=True)
