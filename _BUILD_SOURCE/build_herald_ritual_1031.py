"""Re-author the approved generated seal offline; render only fixed cells in game."""
from pathlib import Path
from PIL import Image,ImageEnhance,ImageChops,ImageFilter,ImageDraw
import json,math,subprocess,hashlib,shutil
import imageio_ffmpeg
BASE=Path(__file__).parent;R=BASE.parent if BASE.name=='_BUILD_SOURCE'else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'assets/game/levels/stage_08/miniboss/herald_ritual_1031'if BASE.name=='_BUILD_SOURCE'else BASE
D=W if BASE.name=='_BUILD_SOURCE'else W/'art';D.mkdir(parents=True,exist_ok=True)
REL='assets/game/levels/stage_08/miniboss/herald_ritual_1031';banks={};sources={}
def manifest(folder):return json.loads((R/f'assets/game/levels/stage_08/miniboss/{folder}/manifest.json').read_text())
hs=manifest('herald_spellcaster_1029');hh=manifest('herald_storm_1030')
def cell(a,f):
 p=R/a['path'];sources[a['path']]=hashlib.sha256(p.read_bytes()).hexdigest();im=Image.open(p).convert('RGBA');return im.crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],(f%a['cols']+1)*a['cw'],(f//a['cols']+1)*a['ch']))
def bank(name,frames,pivot,cols=8):
 w,h=frames[0].size;assert w%2==h%2==0
 sh=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
 for n,f in enumerate(frames):assert f.size==(w,h);sh.alpha_composite(f,(n%cols*w,n//cols*h))
 sh.save(D/(name+'.png'));banks[name]=dict(key='hr92_'+name,path=REL+'/'+name+'.png',cw=w,ch=h,cols=cols,frames=len(frames),pivot=pivot)
def mounted(im,size=576):
 out=Image.new('RGBA',(size,size));out.alpha_composite(im,((size-im.width)//2,(size-im.height)//2));return out
def glow(im,amount):
 # Authored 1015 emission: retain every source alpha edge and step to white-hot red.
 r,g,b,a=im.split();r=r.point(lambda v:min(255,int(v+amount*70)));g=g.point(lambda v:min(255,int(v+amount*190)));b=b.point(lambda v:min(255,int(v+amount*150)))
 return Image.merge('RGBA',(r,g,b,a))
def seal(f):return cell(hs['seal_build'],f).resize((384,384),Image.Resampling.NEAREST)
# Explicitly separate the five star strokes from ALL circles/runes. The former
# HS53 partial cells leaked inner-circle pixels into their last star stroke.
complete=cell(hs['seal_build'],55);points=[(128,70),(197,112),(170,186),(88,186),(59,112)];order=[0,2,4,1,3,0];assigned=[]
for y in range(256):
 for x in range(256):
  col=complete.getpixel((x,y))
  if not col[3]:continue
  best=(1e9,0,0)
  for j in range(5):
   a,b=points[order[j]],points[order[j+1]];vx,vy=b[0]-a[0],b[1]-a[1];u=max(0,min(1,((x-a[0])*vx+(y-a[1])*vy)/(vx*vx+vy*vy)));dist=math.hypot(x-a[0]-u*vx,y-a[1]-u*vy)
   if dist<best[0]:best=(dist,j,u)
  group=best[1]if best[0]<7.2 and math.hypot(x-128,y-128)<96 else 5
  along=best[2]if group<5 else (math.atan2(y-128,x-128)+math.pi/2)%math.tau/math.tau
  assigned.append((x,y,col,group,along))
def partial(line,u):
 im=Image.new('RGBA',(256,256))
 for x,y,col,group,along in assigned:
  if group<line or group==line and along<=u:im.putpixel((x,y),col)
 return im.resize((384,384),Image.Resampling.NEAREST)
build=[]
for line in range(5):
 prev=partial(line,0)
 for step in range(12):
  src=partial(line,step/11);delta=ImageChops.subtract(src.getchannel('A'),prev.getchannel('A'))
  # The moving cutting edge flashes white, then settles into the original ruby line.
  lit=Image.new('RGBA',src.size,(255,242,245,0));lit.putalpha(delta.point(lambda a:int(a*max(0,1-step/16))))
  out=src.copy();out.alpha_composite(lit);build.append(mounted(out))
for step in range(24):build.append(mounted(glow(partial(5,step/23),.12)))
bank('inscribe',build,[288,288])
base=seal(55);spin=[]
def angle(t):return 360*(.16*t+.5*1.05*t*t)
for f in range(90):
 t=f/40;energy=.2+.8*f/89;v=glow(base,energy*(.55+.45*math.sin(f*.72)**2));spin.append(mounted(v).rotate(-angle(t),Image.Resampling.NEAREST,center=(288,288)))
bank('spin',spin,[288,288])
grow=[];theta=angle(2.25)
for f in range(32):
 u=f/31;s=1+.36*u*u;im=base.resize((round(384*s),round(384*s)),Image.Resampling.NEAREST);t=f/40
 grow.append(mounted(glow(im,.7+.3*math.sin(f*.8)**2)).rotate(-(theta+360*(2.52*t+.7*t*t)),Image.Resampling.NEAREST,center=(288,288)))
bank('expand',grow,[288,288])
last=grow[-1];sectors=[]
for i in range(18):
 mask=Image.new('L',last.size);ImageDraw.Draw(mask).pieslice((-200,-200,776,776),i*20,(i+1)*20,fill=255)
 a=ImageChops.multiply(last.getchannel('A'),mask);piece=last.copy();piece.putalpha(a);sectors.append(piece)
glass=cell(hs['glass_shard'],0);burst=[]
for f in range(26):
 u=f/25;out=Image.new('RGBA',(832,832))
 for i,piece in enumerate(sectors):
  a=math.radians(i*20+10);travel=142*u;v=glow(piece,1 if f<3 else .28);v.putalpha(v.getchannel('A').point(lambda x:int(x*(1-u)**.65)))
  out.alpha_composite(v,(128+round(math.cos(a)*travel),128+round(math.sin(a)*travel)))
 for i in range(18):
  a=i*math.tau/18+.13;im=glass.rotate(-math.degrees(a)-f*9,Image.Resampling.NEAREST);im.putalpha(im.getchannel('A').point(lambda x:int(x*(1-u))))
  x=416+math.cos(a)*(100+u*155)-im.width/2;y=416+math.sin(a)*(100+u*155)-im.height/2;out.alpha_composite(im,(round(x),round(y)))
 burst.append(out)
bank('shatter',burst,[416,416])
bolts=[]
for f in range(16):
 im=cell(hh['summon'],f).resize((128,448),Image.Resampling.NEAREST);out=Image.new('RGBA',(128,512));out.alpha_composite(im,(0,32));bolts.append(out)
bank('lightning',bolts,[64,256],4)
warning=cell(hh['warning'],0);warn=[]
for target in[(45,255,100),(255,216,35),(255,30,55),(255,255,255)]:
 im=warning.copy();px=im.load()
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=px[x,y]
   if a and (max(r,g,b)-min(r,g,b)>18 or target==(255,255,255)):
    l=max(r,g,b)/255;px[x,y]=(*(round(v*l)for v in target),a)
 warn.append(mounted(im.resize((80,80),Image.Resampling.NEAREST),96))
bank('warning',warn,[48,48],4)
bank('dark',[Image.new('RGBA',(64,64),(3,0,8,round(200*i/15)))for i in range(16)],[32,32],4)
(D/'manifest.json').write_text(json.dumps(banks,indent=2));(D/'provenance.json').write_text(json.dumps(dict(sources=sources,sourceScale=1.5,sealDiameter=360,expandedDiameter=490,model='Five authored source line slices plus circle; clockwise baked turns, expansion, eighteen exact seal sectors plus native ruby prism glass'),indent=2))
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local banks=json.decode(f:read('*a'));f:close()
for name,a in pairs(banks)do local im=Image{fromFile=D..'/'..name..'.png'};local s=Sprite(a.cw,a.ch,ColorMode.RGB);s.layers[1].name='Approved ruby seal / '..name
for n=0,a.frames-1 do if n>0 then s:newEmptyFrame()end;local cell=Image(im,Rectangle(n%a.cols*a.cw,math.floor(n/a.cols)*a.ch,a.cw,a.ch));s:newCel(s.layers[1],n+1,cell,Point(0,0));s.frames[n+1].duration=1/40 end
local slice=s:newSlice(Rectangle(0,0,a.cw,a.ch));slice.name='cast-pivot';slice.pivot=Point(a.pivot[1],a.pivot[2]);s:saveAs(D..'/'..name..'.aseprite');s:close()end
"""
(D/'author.lua').write_text(lua);subprocess.run([r'C:\Users\Mike\Desktop\Retro Dev Tools\Graphics\Aseprite\aseprite.exe','--batch','--script-param','out='+str(D),'--script',str(D/'author.lua')],check=True)
# Master sharp slice variants from the actual approved chip cue; no synthesized or external source.
F=imageio_ffmpeg.get_ffmpeg_exe();A=R/'assets/game/shared/audio/herald_ritual_1031'if BASE.name=='_BUILD_SOURCE'else W/'audio';A.mkdir(exist_ok=True);slicep=R/'assets/game/shared/audio/chip_1011/chip_slice.mp3'
for i,rate in enumerate([1,.965,1.035]):
 subprocess.run([F,'-v','error','-y','-i',str(slicep),'-af',f'asetrate=44100*{rate},aresample=44100,highpass=f=180,equalizer=f=2700:t=q:w=1:g=4,aecho=0.8:0.7:45|85:0.16|0.08,alimiter=limit=0.88:level=false,afade=t=out:st=0.65:d=0.25','-t','0.95','-c:a','libmp3lame','-b:a','192k',str(A/f'slice_{i}.mp3')],check=True)
shutil.copy2(R/'assets/game/shared/audio/chronos_lightning_1026/strike.mp3',A/'lightning.mp3')
(A/'provenance.json').write_text(json.dumps(dict(slice=str(slicep.relative_to(R)),sliceSHA256=hashlib.sha256(slicep.read_bytes()).hexdigest(),lightning='Existing Dracodia-derived chronos_lightning_1026/strike.mp3',processing='Small pitch variants, high-pass, presence EQ, short echoes; native gain and music duck owned by HR92'),indent=2))
plate=Image.new('RGBA',(1200,600),(6,7,14,255));dr=ImageDraw.Draw(plate)
for i,(name,fr)in enumerate([('inscribe',11),('inscribe',35),('inscribe',59),('inscribe',83),('spin',70),('shatter',9)]):
 a=banks[name];sh=Image.open(D/(name+'.png'));im=sh.crop((fr%a['cols']*a['cw'],fr//a['cols']*a['ch'],(fr%a['cols']+1)*a['cw'],(fr//a['cols']+1)*a['ch']));im.thumbnail((380,260),Image.Resampling.NEAREST);x=i%3*400;y=i//3*300;plate.alpha_composite(im,(x,y+20));dr.text((x+8,y+4),name+' '+str(fr),fill='white')
plate.save(W/'ritual-art-review.png');print(json.dumps({k:a['frames']for k,a in banks.items()}))
