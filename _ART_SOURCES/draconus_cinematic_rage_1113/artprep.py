from pathlib import Path
import json
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');D=W/'references';D.mkdir(exist_ok=True)
def literal(name,mark):
 s=(R/'assets'/name).read_text();return json.JSONDecoder().raw_decode(s[s.index(mark)+len(mark):].lstrip())[0]
over=literal('overhead_slam_art_1111.js','Object.assign(BA119_ART,')
rage=literal('rage_palm_art_1110.js','const RF1110_ART=')
c30=literal('chronos_beam_art_1025.js','const C30_ART=')
c29=literal('chronos_commitment_art_1025.js','const C29_ART=')
def cell(im,i,cw,ch,cols=4):return im.crop((i%cols*cw,i//cols*ch,i%cols*cw+cw,i//cols*ch+ch))
def atlas(a,spec):
 p=R/spec['sheets'][a['sheet']]['path'];im=Image.open(p).convert('RGBA');x,y,w,h=a['cell'];return im.crop((x,y,x+w,y+h))
def board(name,rows,width=320,height=360):
 out=Image.new('RGB',(max(len(x[1])for x in rows)*width,len(rows)*height),'#14212c');draw=ImageDraw.Draw(out)
 for y,(label,frames)in enumerate(rows):
  draw.text((8,y*height+6),label,fill='white')
  for x,im in enumerate(frames):
   box=im.getbbox();im=im.crop(box);im.thumbnail((width-16,height-40),Image.Resampling.NEAREST);out.paste(im,(x*width+(width-im.width)//2,y*height+34+(height-40-im.height)//2),im)
 out.save(D/name)
rows=[]
for bank in ['cast','thrust']:
 frames=[atlas(a,c30)for a in c30['banks'][bank]];rows.append(('Chronus original '+bank,frames));frames[0].save(D/('chronus-'+bank+'-first.png'))
for bank in ['rage_regular','rage_red']:
 frames=[atlas(a,c29)for a in c29['banks'][bank]];rows.append(('Chronus original '+bank,frames))
board('chronus-original-choreography.png',rows,240,300)
rows=[]
for mat in ['plain','power']:
 a=rage['banks']['drac_charge_fore'];im=Image.open(R/f'assets/game/shared/combat/rage_palm_1110/drac_charge_fore_{mat}.webp').convert('RGBA')
 frames=[cell(im,i,a['cw'],a['ch'])for i in [0,3,6,9,12,15]];rows.append(('Draconus '+mat,frames));frames[0 if mat=='plain'else-1].save(D/('draconus-'+mat+'.png'))
for mat in ['regular','chrome']:
 a=over['corrupt-overhead'];im=Image.open(R/f'assets/game/shared/combat/{a["folder"]}/corrupt-overhead_{mat}.webp').convert('RGBA')
 frames=[cell(im,i,*a['cell'])for i in [0,8,15,16,22,31]];rows.append(('Draconus current center '+mat,frames))
 for i in [0,15,22]:cell(im,i,*a['cell']).save(D/f'draconus-center-{mat}-{i}.png')
board('draconus-current-poses.png',rows)
(W/'reference-inventory.json').write_text(json.dumps(dict(chronus={k:len(v)for k,v in c30['banks'].items()},rage={k:len(v)for k,v in c29['banks'].items()},overhead={k:{a:v for a,v in over[k].items()if a not in ['meta']}for k in ['corrupt-overhead','corrupt-overhead-left','corrupt-overhead-right']}),indent=2))
print('Saved original Chronus choreography and actual Draconus reference crops.',flush=True)
