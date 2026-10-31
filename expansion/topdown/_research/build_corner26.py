"""Extract generated Genesis HUD components. Rebuild from retained source."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[3];A=R/'expansion/topdown/art/corner26';S=A/'source';F=A/'frames';F.mkdir(exist_ok=True,parents=True)
im=Image.open(S/'atlas.png').convert('RGBA');assert im.size==(512,288)
assets={}
def save(name,picture):
 picture=picture.convert('RGBA');picture.putalpha(picture.getchannel('A').point(lambda v:255 if v>=128 else 0));assert all(n%2==0 for n in picture.size)
 p=F/(name+'.png');picture.save(p);assets['corner26_'+name]={'file':p.relative_to(R).as_posix(),'size':list(picture.size),'anchor':[0,0],'bounds':list(picture.getbbox()),'drawScale':1}
def pad(box,size):
 part=im.crop(box);out=Image.new('RGBA',size);out.alpha_composite(part,((size[0]-part.width)//2,(size[1]-part.height)//2));return out
def nine(part,size):
 w,h=part.size;tw,th=size;xs=[0,6,w-6,w];ys=[0,5,h-5,h];dx=[0,6,tw-6,tw];dy=[0,5,th-5,th];out=Image.new('RGBA',size)
 for y in range(3):
  for x in range(3):
   q=part.crop((xs[x],ys[y],xs[x+1],ys[y+1])).resize((dx[x+1]-dx[x],dy[y+1]-dy[y]),Image.Resampling.NEAREST);out.alpha_composite(q,(dx[x],dy[y]))
 return out
save('portrait',pad((25,16,78,69),(56,56)))
save('health',nine(im.crop((92,16,227,36)),(144,24)))
save('fill',pad((92,54,220,66),(128,14)))
save('fill_low',pad((92,116,220,129),(128,14)))
save('ammo',pad((367,16,488,62),(128,48)))
pack={'assets':assets,'sequences':{},'fill':{'x':8,'y':5,'w':128,'h':14},'service':'PixelLab','sourceId':'15d24f31-5fb6-477e-8836-5eed3893f729','build':'overdrive1015-corner26-r1'}
(A/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8',newline='\n');(A/'manifest.js').write_text('window.TD_CORNER26_ART='+json.dumps(pack,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in S.iterdir()if p.is_file()and p.name!='hashes.json'},indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'assets':len(assets),'fill':pack['fill']}))
