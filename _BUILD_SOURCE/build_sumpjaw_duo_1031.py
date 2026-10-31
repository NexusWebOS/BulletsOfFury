from pathlib import Path
import json, math, hashlib, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

R=Path(__file__).resolve().parents[1]
W=R/'_ART_SOURCES/sumpjaw_duo_1031'
D=R/'assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031';D.mkdir(parents=True,exist_ok=True)
REL='assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031/'
M={'banks':{},'format':'Fixed even cells; one common192px source unit;256px motion canvas; baked glow/rotation/depth; no runtime transforms.', 'jobs':['86d8100a-a47b-46d3-a506-ff196b86ee00','09cadfa8-bf7c-47d5-b233-662826f04987']}
frames={}
def bank(n,ims,pivot=None,meta=None,fps=20):
 w,h=ims[0].size;assert w%2==h%2==0 and all(i.size==(w,h)for i in ims)
 cols=min(8,4096//w);per=cols*min(8,4096//h);pages=[]
 for start in range(0,len(ims),per):
  row=ims[start:start+per];out=Image.new('RGBA',(cols*w,math.ceil(len(row)/cols)*h))
  for j,im in enumerate(row):out.alpha_composite(im,(j%cols*w,j//cols*h))
  name=f'{n}_{start//per}.png';out.save(D/name);pages.append(dict(key='sj98_'+n+'_'+str(start//per),path=REL+name,start=start,frames=len(row)))
 M['banks'][n]=dict(w=w,h=h,cols=cols,frames=len(ims),pivot=pivot or[w//2,h//2],fps=fps,pages=pages)
 if meta is not None:M['banks'][n]['poses']=meta
 frames[n]=ims

idle=[Image.open(W/f'sources/pixellab/body_{i:02d}.png').convert('RGBA')for i in range(1,9)]
bite=[Image.open(W/f'sources/bite/bite_{i:02d}.png').convert('RGBA')for i in range(1,9)]

def points(im):
 a=np.array(im);yy,xx=np.mgrid[:192,:192];green=(a[:,:,1]>100)&(a[:,:,1]>a[:,:,0].astype(float)*1.1)&(a[:,:,1]>a[:,:,2].astype(float)*1.3)&(a[:,:,3]>100)
 result=[]
 for cx,cy,rx,ry in [(94,84,20,25),(151,87,20,25),(124,138,23,23)]:
  mask=green&(((xx-cx)/rx)**2+((yy-cy)/ry)**2<1)
  ys,xs=np.where(mask)
  result.append([float(np.median(xs))if len(xs)else cx,float(np.median(ys))if len(xs)else cy])
 return result

def damage(im,state,hot=0):
 out=np.array(im).copy();yy,xx=np.mgrid[:192,:192];ps=points(im)
 for i in range(2):
  if not state&(1<<i):continue
  cx,cy=ps[i];area=((xx-cx)/15)**2+((yy-cy)/20)**2<1
  green=(out[:,:,1]>out[:,:,0].astype(float)*1.08)&(out[:,:,1]>out[:,:,2].astype(float)*1.2)&area
  lum=out[:,:,:3].max(2)
  out[:,:,0][green]=(lum[green]*.20).astype('uint8');out[:,:,1][green]=(lum[green]*.22).astype('uint8');out[:,:,2][green]=(lum[green]*.17).astype('uint8')
  # Broken glass keeps the existing outline; only a fine angular crack is authored.
  crack=area&(np.abs(xx-cx+(yy-cy)*.34)<.65)&(out[:,:,3]>100)
  out[crack,:3]=[111,122,87]
 if hot:
  a=out[:,:,3];rgb=out[:,:,:3].astype(float);lum=rgb.max(2);g=(rgb[:,:,1]>rgb[:,:,0]*1.13)&(a>0)
  rgb[g,0]=np.minimum(250,rgb[g,0]+hot*75);rgb[g,1]=np.minimum(255,rgb[g,1]+hot*35);rgb[g,2]=np.minimum(180,rgb[g,2]+hot*55)
  out[:,:,:3]=rgb.astype('uint8')
 return Image.fromarray(out)

def pose(im,scale=1,angle=0):
 c=Image.new('RGBA',(256,256));k=round(192*scale);f=im.resize((k,k),Image.Resampling.NEAREST)
 c.alpha_composite(f,(128-k//2,128-k//2))
 if angle:c=c.rotate(angle,resample=Image.Resampling.NEAREST,center=(128,128))
 ps=[];a=math.radians(angle)
 for x,y in points(im):
  x=(x-96)*scale;y=(y-96)*scale;ps.append([round(x*math.cos(a)+y*math.sin(a),3),round(-x*math.sin(a)+y*math.cos(a),3)])
 bb=c.getbbox()or(128,128,128,128)
 return c,dict(gills=ps[:2],mouth=ps[2],scale=scale,bounds=[bb[0]-128,bb[1]-128,bb[2]-128,bb[3]-128])

spec=[]
for i in range(16):spec.append((idle[(i if i<8 else 15-i)%8],1,0,'idle'))
for i in range(8):spec.append((bite[i],1,0,'bite'))
for i in range(24):
 u=i/23;k=.12+.88*(1-(1-u)**2);a=55*(1-u)
 spec.append((bite[min(7,i//3)],k,a,'breach'))
for i in range(17):spec.append((idle[i%8],1,-40+5*i,'turn'))
M['clips']={'idle':[0,16],'bite':[16,8],'breach':[24,24],'turn':[48,17]}
for state in range(4):
 ims=[];hits=[];hot=[];meta=[]
 for i,(im,k,a,name)in enumerate(spec):
  source=damage(im,state);f,p=pose(source,k,a);meta.append(p);ims.append(f)
  white=Image.new('RGBA',f.size,'white');white.putalpha(f.getchannel('A'));hits.append(white)
  g,_=pose(damage(im,state,.4+.6*math.sin(i*.8)**2),k,a)
  mask=g.getchannel('A');rim=mask.filter(ImageFilter.MaxFilter(3));outline=Image.new('RGBA',g.size,(140,234,30,0));outline.putalpha(Image.fromarray(np.maximum(0,np.array(rim).astype(int)-np.array(mask).astype(int)).astype('uint8')));outline.alpha_composite(g);hot.append(outline)
 bank('body'+str(state),ims,meta=meta);bank('hit'+str(state),hits);bank('hot'+str(state),hot)

# Authored death fragments preserve real source pixels; the native explosions own the breakup.
seed=damage(idle[0],3);fragment=[]
for y in range(3):
 for x in range(3):
  c=Image.new('RGBA',(64,64));c.alpha_composite(seed.crop((x*64,y*64,x*64+64,y*64+64)));fragment.append(c)
bank('fragment',fragment)

# Small local health frame, authored once offline; the runtime only clips its fill.
bar=Image.new('RGBA',(160,28));g=ImageDraw.Draw(bar)
g.polygon([(4,0),(155,0),(159,4),(159,23),(155,27),(4,27),(0,23),(0,4)],fill='#080d0d',outline='#8c9481')
g.line([(4,2),(154,2),(156,4)],fill='#d1d5ba',width=1);g.line([(2,6),(2,21),(5,24),(154,24)],fill='#424e43',width=2)
g.rectangle((7,18,152,23),fill='#020604',outline='#57684d');g.rectangle((8,5,11,11),fill='#b2e42c');g.rectangle((148,5,151,11),fill='#b2e42c')
bank('health_frame',[bar],pivot=[80,14]);fill=Image.new('RGBA',(144,4));g=ImageDraw.Draw(fill)
for y,col in enumerate(['#edffc3','#a7f139','#55c61d','#297b18']):g.line((0,y,143,y),fill=col)
bank('health_fill',[fill],pivot=[0,0])

retina=Image.open(R/'assets/game/levels/stage_08/miniboss/herald_landing_retinas_1030/retina.png').convert('RGBA')
bank('retina',[retina.crop((i%8*64,i//8*32,i%8*64+64,i//8*32+32))for i in range(24)],pivot=[32,16])
# Existing toxic projectile and splash retain the game's current authored style.
for name,src,cols,rows,count,sz in [('orb','assets/game/shared/combat/encounter_revision_1027/toxic_orb.png',4,4,16,28),('splash','assets/game/levels/stage_07/miniboss/dredger_final_1029/ooze.png',4,4,16,80)]:
 im=Image.open(R/src).convert('RGBA');cw=im.width//cols;ch=im.height//rows
 out=[]
 for i in range(count):
  f=im.crop((i%cols*cw,i//cols*ch,i%cols*cw+cw,i//cols*ch+ch));k=sz/max(cw,ch);f=f.resize((round(cw*k),round(ch*k)),Image.Resampling.NEAREST);c=Image.new('RGBA',(sz,sz));c.alpha_composite(f,((sz-f.width)//2,(sz-f.height)//2));out.append(c)
 bank(name,out,pivot=[40,68]if name=='splash'else None)

M['sourceHashes']={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest()for p in (W/'sources').rglob('*.png')}
(D/'manifest.json').write_text(json.dumps(M,separators=(',',':')),encoding='utf-8')
(R/'assets/sumpjaw_art_1031.js').write_text("'use strict';\nconst SJ98_ART="+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8')
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local s=Sprite(a.w,a.h,ColorMode.RGB)
 for _,page in ipairs(a.pages)do local path=page.path:match('([^/]+)$');local im=Image{fromFile=D..'/'..path}
  for j=0,page.frames-1 do local i=page.start+j;if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(j%a.cols*a.w,math.floor(j/a.cols)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end
 end;s:saveAs(D..'/'..n..'.aseprite');s:close()
end
"""
(D/'author.lua').write_text(lua,encoding='utf-8');subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
review=Image.new('RGBA',(1024,768),(13,20,24,255))
for j,(name,f)in enumerate([('body0',0),('body0',19),('body0',32),('body0',47),('body1',0),('body2',0),('body3',0),('hot0',19),('body0',48),('body0',56),('body0',64),('hit0',0)]):review.alpha_composite(frames[name][f],(j%4*256,j//4*256))
review.save(W/'art-review.png');print('Authored',sum(a['frames']for a in M['banks'].values()),'frames;',len(M['banks']),'editable banks.')
