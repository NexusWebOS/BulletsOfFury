"""Overdrive generated HUD font, equipment panel and solid fills."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[3];A=R/'expansion/topdown/art/hud27';S=A/'source';F=A/'frames';F.mkdir(exist_ok=True,parents=True)
assets={}
def save(key,im):
 im=im.convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));assert all(n%2==0 for n in im.size)
 p=F/(key+'.png');im.save(p);assets[key]={'file':p.relative_to(R).as_posix(),'size':list(im.size),'anchor':[0,0],'bounds':list(im.getbbox()),'drawScale':1}
def pad(im,size):
 out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2));return out
ui=Image.open(S/'ui.png').convert('RGBA');assert ui.size==(512,288)
save('hud27_equipment',pad(ui.crop((25,16,228,93)),(204,78)))
for name,box in [('fill',(248,16,368,30)),('fill_low',(248,53,368,68))]:
 # The generated source is120px across. Stretch its uniform center only,
 # retaining the exact bright top and dark lower edge; no gaps are inserted.
 im=ui.crop(box);im=im.resize((128,im.height),Image.Resampling.NEAREST);save('hud27_'+name,pad(im,(128,16)))
font=Image.open(S/'font.png').convert('RGBA');cell=16;cols=font.width//cell;assert font.width%cell==font.height%cell==0
order="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?:;'\"-+()0123456789/%*=_$";assert len(order)==80 and font.width*font.height==80*cell*cell
glyphs={}
for i,ch in enumerate(order):
 im=font.crop((i%cols*cell,i//cols*cell,i%cols*cell+cell,i//cols*cell+cell));alpha=im.getchannel('A');im=Image.new('RGBA',(cell,cell),'white');im.putalpha(alpha);b=im.getbbox();assert b,(i,ch);key='hud27_glyph_'+str(i);save(key,im);glyphs[ch]={'key':key,'bounds':list(b),'advance':b[2]-b[0]+2}
for gun in ['rifle','desert_eagle','spread_shotgun','minigun','fusion_beam','napalm_launcher','rocket_launcher']:
 p=S/'rifle.png' if gun=='rifle' else R/'expansion/onfoot/weapons'/(gun+'_pickup.png');im=Image.open(p).convert('RGBA');im=im.crop(im.getbbox());scale=min(54/im.width,30/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);save('hud27_gun_'+gun,pad(im,(64,40)))
pack={'assets':assets,'sequences':{},'font':{'name':'Overdrive Arcade HUD','glyphs':glyphs,'cell':16,'columns':cols,'baseline':13,'capTop':3,'capHeight':10},'fill':{'x':8,'y':5,'w':128,'h':14},'equipment':{'w':204,'h':78,'gun':[13,10,66,56],'ammo':[85,16,104,16],'status':[85,42,104,16]},'build':'overdrive1015-hud27-r1'}
(A/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8',newline='\n');(A/'manifest.js').write_text('window.TD_HUD27_ART='+json.dumps(pack,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in S.iterdir()if p.is_file()and p.name!='hashes.json'},indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'assets':len(assets),'glyphs':len(glyphs),'fontGrid':[cols,font.height//cell]}))
