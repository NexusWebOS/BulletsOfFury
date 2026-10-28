from pathlib import Path
from PIL import Image,ImageDraw
import re,json,shutil
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/compact_dialogue_1026';W.mkdir(parents=True,exist_ok=True);D=R/'assets/game/shared/ui/compact_dialogue_1026';D.mkdir(parents=True,exist_ok=True)
source=R/'assets/game/shared/ui/command_1020/dialogue-a.webp';im=Image.open(source).convert('RGBA').resize((460,84),Image.Resampling.NEAREST)
colors=dict(re.findall(r"key:'(\w+)'[^\n]+?tint:'(#[0-9a-fA-F]{6})'",(R/'assets/game.js').read_text(encoding='utf-8')));colors.update(nyx='#b073ff',kaia='#25d9bd',jace='#ff4838',rook='#ff9b30',voss='#ff244b',dracodia='#b98cff',chronos='#c6a6ff',neutral='#a9dcfa')
assets={};poly=[(round(x*460/2160),round(y*84/394))for x,y in [(450,44),(839,44),(872,77),(872,87),(842,112),(482,112),(450,80)]]
for who,col in colors.items():
 mask=Image.new('L',im.size);g=ImageDraw.Draw(mask);g.polygon(poly,fill=80)
 for x,y,rx,ry in [(467,64,23,25),(832,54,6,6),(841,103,7,7)]:g.ellipse((round((x-rx)*460/2160),round((y-ry)*84/394),round((x+rx)*460/2160),round((y+ry)*84/394)),fill=0)
 ink=Image.new('RGBA',im.size,col);ink.putalpha(mask);a=Image.alpha_composite(im,ink)
 for width in [460,360,280,220]:
  if width==460:out=a
  else:
   cut=460-width;out=Image.new('RGBA',(width,84));out.paste(a.crop((0,0,200,84)),(0,0));out.paste(a.crop((200+cut,0,460,84)),(200,0))
  name=f'{who}-{width}.png';out.save(D/name,optimize=True);assets[f'cd27_{who}_{width}']='assets/game/shared/ui/compact_dialogue_1026/'+name
(R/'assets/compact_dialogue_art_1026.js').write_text('"use strict";\nconst CD27_ART='+json.dumps({'widths':[460,360,280,220],'height':84,'assets':assets},separators=(',',':'))+';\n',encoding='utf-8')
(W/'source.json').write_text(json.dumps({'source':str(source),'fixed':{'w':460,'h':84},'narrowWidths':[360,280,220],'note':'Narrow frames remove only an empty middle rail/body segment offline; portrait, header, corner and vertical dimensions stay identical.'},indent=2))
print(len(assets),'authored fixed frame sprites')
