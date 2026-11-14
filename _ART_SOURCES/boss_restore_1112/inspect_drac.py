from pathlib import Path
from PIL import Image,ImageDraw
import json
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Recovered-boss-animations'
s=(R/'assets/hammer_correction_art_1022.js').read_text();h=json.JSONDecoder().raw_decode(s[s.index('const H22_ART=')+len('const H22_ART='):].lstrip())[0]
sources=[]
cells=[];im=Image.open(R/'assets/game/shared/combat/boss_strike_1109b/corrupt-sides_regular.webp').convert('RGBA')
for f in range(16):cells.append(im.crop((f%4*576,f//4*576,f%4*576+576,f//4*576+576)))
sources.append(('boss_strike / frame',cells))
cells=[]
for a in h['banks']['corrupt_side']:
 sheet=h['sheets'][a['sheet']];im=Image.open(R/sheet['path']).convert('RGBA');x,y,w,hgt=a['cell'];cells.append(im.crop((x,y,x+w,y+hgt)))
sources.append(('H22 / frame',cells))
board=Image.new('RGB',(8*256,len(sources)*2*292),'#101820');d=ImageDraw.Draw(board)
for j,(name,cells)in enumerate(sources):
 for f,im in enumerate(cells[:16]):
  im=im.crop(im.getbbox());im.thumbnail((248,256),Image.Resampling.NEAREST);x=f%8*256;y=(j*2+f//8)*292;board.paste(im,(x+(256-im.width)//2,y),im);d.text((x+8,y+260),name+' '+str(f),fill='white')
board.save(O/'draconus-source-frames.png')
