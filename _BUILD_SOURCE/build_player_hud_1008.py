"""Extract native authored player rows; analyze wells without repainting source art."""
from pathlib import Path
from PIL import Image
import hashlib,json
R=Path(__file__).resolve().parents[1]
defs={};sources={}
def runs(values,gap=1):
 out=[]
 for v in values:
  if not out or v>out[-1][-1]+gap:out.append([])
  out[-1].append(v)
 return out
for theme in [f'stage_{n:02d}' for n in range(1,10)]+['stage_x']:
 src=R/'_ART_SOURCES/hud_themes_1007'/theme/'hud-kit-v2.png'
 im=Image.open(src).convert('RGBA');pix=im.load();w,h=im.size
 green=lambda p:p[1]>145 and p[1]>p[0]*1.5 and p[1]>p[2]*1.4 and p[3]>160
 greenRows=[y for y in range(110,240) if sum(green(pix[x,y]) for x in range(75,365))>150]
 labels=[v for v in runs(greenRows) if len(v)>5]
 rr=runs(greenRows,15)
 assert len(rr)==len(labels)==2,(theme,rr,labels)
 xs=[x for x in range(75,365) if green(pix[x,rr[0][len(rr[0])//2]])]
 gx=min(xs);gw=max(xs)-gx+1
 wells=[[gx,v[0]-1,gw,v[-1]-v[0]+3] for v in rr]
 red=lambda p:p[0]>150 and p[0]>p[1]*1.35 and p[0]>p[2]*1.35 and p[3]>160
 rs=runs([y for y in range(140,215) if sum(red(pix[x,y]) for x in range(595,1040))>220],7);rs=[v for v in rs if len(v)>7]
 assert rs,(theme,'No red resource strip');rs=max(rs,key=len)
 special=[595,rs[0]-1,442,rs[-1]-rs[0]+3]
 crop=[0,40,w,269];cell=im.crop((0,40,w,309))
 dest=R/'assets/game/levels'/('stage_06' if theme=='stage_x' else theme)/'ui'/('player_hud_stagex_1008.png' if theme=='stage_x' else 'player_hud_1008.png')
 dest.parent.mkdir(parents=True,exist_ok=True);cell.save(dest)
 defs[theme]={'key':'ph8_'+theme,'path':dest.relative_to(R).as_posix(),'w':w,'h':269,'sourceY':40,'roll':wells[0],'somer':wells[1],'special':special,'rollLabelTop':labels[0][0]-29,'somerLabelTop':labels[1][0]-30,'emptyX':1020,'greenX':170,'redX':740,'offset':labels[0][0]-151}
 sources[theme]={'source':src.relative_to(R).as_posix(),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop':crop,'output':dest.relative_to(R).as_posix(),'outputSha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'pixelPolicy':'Native pixels and alpha copied unchanged; runtime composites static recesses, live fonts/icons and clipped fill samples.'}
(R/'assets/player_hud_art_1008.js').write_text('"use strict";\nconst PH8_ART='+json.dumps(defs,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
manifest=R/'_ART_SOURCES/player_hud_1008';manifest.mkdir(exist_ok=True)
(manifest/'manifest.json').write_text(json.dumps(sources,indent=2)+'\n',encoding='utf-8')
print('Registered',len(defs),'native player HUD rows:',sum((R/d['path']).stat().st_size for d in defs.values()),'bytes.')
