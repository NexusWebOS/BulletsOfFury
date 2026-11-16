from pathlib import Path
from PIL import Image,ImageDraw
import json,math
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';out=O/'contacts-final';out.mkdir(exist_ok=True)
boss={1:'native-sweep',2:'native-sweep',3:'native-retry',4:'native-retry',5:'native-retry',6:'native-diagnostic',7:'native-sweep',8:'native-current',9:'native-retry'}
rows=[]
for stage in range(1,10):
 sheet=Image.new('RGB',(1440,620),(6,12,20));d=ImageDraw.Draw(sheet);d.text((10,5),f'STAGE {stage} | native protected input bot | not human balance certification',fill='white');rec={'stage':stage,'runs':[]}
 for role,folder in [('mini','native-mini-current'if stage==7 else'native-mini'),('boss',boss[stage])]:
  p=O/folder/f'stage{stage}';r=json.loads((p/'report.json').read_text());files=sorted(p.glob('frame-*.png'))
  if not files:files=sorted(p.glob('phase-*.png'))
  choices=[files[min(len(files)-1,round(q*(len(files)-1)))]for q in [0,.33,.67,1]]
  for j,f in enumerate(choices):
   im=Image.open(f).convert('RGB');im.thumbnail((356,265));x=j*360;y=25+(0 if role=='mini'else 295);sheet.paste(im,(x+(356-im.width)//2,y));d.text((x+5,y+267),role+' '+f.stem,fill=(180,225,255))
  rec['runs'].append({'role':role,'folder':str(p.relative_to(O)).replace('\\','/'),'completed':r['completed'],'defeatSeconds':r.get('defeatSeconds'),'errors':{k:r.get(k,[])for k in['pageErrors','consoleErrors','assetErrors']},'audio':r.get('audio'),'chosen':[f.name for f in choices]})
 sheet.save(out/f'stage{stage}.jpg',quality=91);rows.append(rec)
(out/'index.json').write_text(json.dumps({'rows':rows},indent=2),encoding='utf8');print('9 boards /72 native gameplay screenshots')
