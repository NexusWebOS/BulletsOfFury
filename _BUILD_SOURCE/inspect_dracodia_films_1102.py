"""Actual recorded pixels for the three complete native Dracodia fights."""
from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_comparison_1102';ff=imageio_ffmpeg.get_ffmpeg_exe();sheet=Image.new('RGB',(1440,7*325),'#06121d');draw=ImageDraw.Draw(sheet);receipt=[]
for col,diff in enumerate(['normal','hard','furious']):
 j=json.loads((O/diff/'batch.json').read_text())['jobs']['stage8-boss'];t=json.loads((R/j['folder']/'report.json').read_text())['timeline'];find=lambda predicate:next(q['seconds']for q in t if predicate(q))
 samples=[('Rebirth / download',find(lambda q:q.get('mode')=='dr5Monologue')-5),('Final reveal / dialogue',find(lambda q:q.get('mode')=='dr5Monologue')+2)]
 for form,label in [(8,'Hammer copy'),(1,'Neural Archon'),(6,'Helicopter'),(2,'Volcano')]:samples.append((label,find(lambda q:q.get('phase')==2 and q.get('form')==form and q.get('mode')=='fight')+3))
 samples.append(('Unlocked final body',find(lambda q:bool(q.get('dracodia')and q['dracodia'].get('unlocked')))+3))
 for row,(label,seconds)in enumerate(samples):
  file=O/(diff+'-dracodia-'+str(row)+'.jpg');subprocess.run([ff,'-v','error','-y','-ss',str(seconds),'-i',str(R/j['path']),'-frames:v','1','-q:v','2',str(file)],check=True);im=Image.open(file);im.thumbnail((480,300));sheet.paste(im,(col*480,row*325+25));draw.text((col*480+5,row*325+5),diff.upper()+' / '+label+f' / {seconds:.1f}s',fill='white');receipt.append(dict(difficulty=diff,label=label,seconds=seconds,file=str(file.relative_to(R))))
sheet.save(O/'dracodia-three-difficulties.jpg',quality=94);(O/'dracodia-pixel-receipt.json').write_text(json.dumps(receipt,indent=2));print('Exported',len(receipt),'actual movie frames')
