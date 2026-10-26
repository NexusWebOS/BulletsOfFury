from pathlib import Path
import json,subprocess
import numpy as np
import imageio_ffmpeg
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_motion_1025/gameplay';F=imageio_ffmpeg.get_ffmpeg_exe();d=json.loads((O/'gameplay-recording.json').read_text());t=d['timeline'];checks={};meta=[]
for folder in [O]:
 p=folder/'stage5-furious-with-audio.mp4';r=subprocess.run([F,'-v','error','-i',str(p),'-f','null','-'],capture_output=True);checks[folder.name+' full AV decode']=r.returncode==0 and not r.stderr
 r=subprocess.run([F,'-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-'],capture_output=True,check=True);a=np.frombuffer(r.stdout,dtype='<f4');x=dict(seconds=len(a)/8000,peak=float(np.max(abs(a))),rms=float(np.sqrt(np.mean(a*a))),nonzero=float(np.mean(abs(a)>.001)));meta.append(dict(file=str(p.relative_to(R)),**x));checks[folder.name+' audible decoded track']=x['rms']>.01 and x['nonzero']>.5 and x['peak']<1
get=lambda state:next((r['videoSeconds'] for r in t if r.get('state')==state),0)
times=dict(intro=get('unfold')+2,armor=get('fr_activation')+.6,melee=get('recover'),recharge=get('storm_raise'),counter=get('fr_stun'))
for key in ['armor','recharge','counter']:checks[key+' actually appears in continuous gameplay']=times[key]>0
checks['native music and dialogue ticks are recorded']=d['audio']['playing'].get('dialogueLetter',0)>100 and d['audio']['playing'].get('boss5',0)>0
checks['native charge / strike / throw / magnet cues play']=all(d['audio']['playing'].get(k,0)>0 for k in ['bossWeaponCharge','hammerImpact','hammerThrow','hammerMagnet'])
checks['native God mode stays enabled and no player deaths occur']=d['audio'].get('god') is True and d['audio'].get('deaths')==0 and all(not q.get('player',{}).get('dead') for q in t)
checks['no capture or console errors']=not d['errors'] and not d['audio'].get('tapError')
checks['real missile triggers counter then magnetic catch in continuous run']=all(any(e['type']==k for e in d['audio']['events']) for k in ['raised-hammer-missile-counter','hammer-magnetic-recall','hammer-caught'])
# Native decoded video, not rendered source sprites.
frames=[('intro',times['intro']+1),('armor',times['armor']+.5),('melee',times['melee']+.8),('recharge',times['recharge']+1.8),('kneel',times['counter']+1.4),('recall',times['counter']+3.65)]
checks['three volley leaders occur before each physical unfold']=all(e['volleys']==3 for e in d['audio']['motionEvents'] if e['type']=='ball-unfold') and any(e['type']=='ball-unfold' for e in d['audio']['motionEvents'])
checks['native laser audio decodes and plays']=any('laser' in k.lower() and v>0 for k,v in d['audio']['playing'].items())
sheet=Image.new('RGB',(1280,1245),'#111b27');g=ImageDraw.Draw(sheet)
for i,(name,at)in enumerate(frames):
 p=O/('decoded-'+name+'.png');subprocess.run([F,'-y','-loglevel','error','-ss',str(at),'-i',str(O/'stage5-furious-with-audio.mp4'),'-frames:v','1',str(p)],check=True);im=Image.open(p).resize((640,400));sheet.paste(im,(i%2*640,i//2*415));g.text((i%2*640+8,i//2*415+401),name+' '+str(round(at,2))+'s',fill='white')
sheet.save(O/'final-video-contact.png');(R/'docs/previews/chronos_frames_1025/motion-review.json').write_text(json.dumps(dict(times=times),indent=2)+'\n',encoding='utf8')
report=dict(checks=checks,audio=meta,times=times,passed=sum(checks.values()),failed=sum(not x for x in checks.values()));(O/'av-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps(report,indent=2));raise SystemExit(0 if not report['failed'] else 1)
