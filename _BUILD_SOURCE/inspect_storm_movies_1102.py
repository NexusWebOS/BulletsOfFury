"""Select actual recorded attack pixels from completed native fights."""
from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/furious_encounters_1102';state=json.loads((R/'_shots/boss_comparison_1102/furious/batch.json').read_text());frames=[];summary={};ff=imageio_ffmpeg.get_ffmpeg_exe()
for jobid in ['stage6-mini','stage6-boss','stage7-mini']:
 job=state['jobs'].get(jobid)
 if not job or not job.get('passed'):continue
 report=json.loads((R/job['folder']/'report.json').read_text());seen={}
 for row in report['timeline']:
  q=row.get('storm')
  if q and q['phase']=='attack':seen.setdefault((q['attack'],q['open']),[]).append(row)
 if not seen:seen={('worm pair',False):report['timeline'][10:-10]}
 summary[jobid]=dict(complete=report['completed'],attacks=[str(k)for k in seen],nativeFps=job['nativeFps'],peakDb=job['peakDb'])
 for (attack,opened),rows in seen.items():
  row=rows[min(2,len(rows)-1)] if attack!='worm pair'else rows[len(rows)//3];t=row['seconds'];file=O/(jobid+'-'+attack+('-core'if opened else'')+'.jpg');subprocess.run([ff,'-v','error','-y','-ss',str(t),'-i',str(R/job['path']),'-frames:v','1','-q:v','2',str(file)],check=True);frames.append((file,f'{jobid} / {attack}'+(' / exposed core'if opened else'')+f' / {t:.1f}s'))
cols=3;cw=480;ch=330;sheet=Image.new('RGB',(cols*cw,((len(frames)+cols-1)//cols)*ch),'#06121d');d=ImageDraw.Draw(sheet)
for i,(file,label)in enumerate(frames):
 im=Image.open(file);im.thumbnail((cw,ch-25));x=i%cols*cw;y=i//cols*ch;sheet.paste(im,(x,y+25));d.text((x+5,y+5),label,fill='white')
sheet.save(O/'final-storm-movies.jpg',quality=94);(O/'film-attack-checks.json').write_text(json.dumps(summary,indent=2));print(summary)
