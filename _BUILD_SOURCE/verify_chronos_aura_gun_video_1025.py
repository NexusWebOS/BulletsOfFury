from pathlib import Path
import json,subprocess,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_aura_gun_1025/video';F=imageio_ffmpeg.get_ffmpeg_exe();video=O/'chronos-aura-chaingun.mp4';q=json.loads((O/'review.json').read_text());checks={}
r=subprocess.run([F,'-v','error','-i',str(video),'-f','null','-'],capture_output=True);checks['full video/audio decode']=r.returncode==0 and not r.stderr
r=subprocess.run([F,'-v','error','-i',str(video),'-vn','-ac','1','-ar','8000','-f','f32le','-'],capture_output=True,check=True);a=np.frombuffer(r.stdout,dtype='<f4');audio=dict(seconds=len(a)/8000,peak=float(abs(a).max()),rms=float(np.sqrt(np.mean(a*a))),nonzero=float(np.mean(abs(a)>.001)))
checks['audible decoded track']=audio['rms']>.01 and audio['nonzero']>.5 and audio['peak']<1
playing=q['audio']['playing'];checks['impact throw pickup and chaingun decoded playback']=all(playing.get(k,0)>0 for k in ['hammerImpact','hammerThrow','weapon','hammerChaingun'])
checks['no capture/page/console errors']=not q['errors'] and not q['audio'].get('tapError')
checks['all six native recoil frames appear']=len({v['bodyFrame'] for v in q['timeline'] if v['state']=='chaingun'})==6
checks['all eight barrel phases appear']=len({v['rotor'] for v in q['timeline'] if v['state']=='chaingun'})==8
checks['native red charge completes and stays red']=any(v['state']=='hf22_rage_charge' for v in q['timeline']) and all(v['red'] for v in q['timeline'] if v['videoSeconds']>26)
checks['native follow-through includes spin depth and double/side combo']=all(any(v['state']==s for v in q['timeline']) for s in ['whirlwind','giant_rise','giant_bg_drop','c27_depth_combo'])
checks['invulnerable review stays alive']=q['audio']['god'] and not any(v['playerDead'] for v in q['timeline'])
get=lambda state:next(v['videoSeconds'] for v in q['timeline'] if v['state']==state)
pts=[v for v in q['timeline'] if v.get('pickup') is not None];at=lambda t:float(np.interp(t,[v['pickup'] for v in pts],[v['videoSeconds'] for v in pts]))
frames=[('wind-up',at(1.2)),('crate impact',at(1.88)),('hammer release',at(2.5)),('gun catch',at(3.6)),('firing',get('chaingun')+.35),('red transformation',get('hf22_rage_charge')+1.2),('silhouette spin',get('whirlwind')+.25),('depth strike',get('c27_depth_combo')+.15)]
out=Image.new('RGB',(1280,4*415),'#101e2d');d=ImageDraw.Draw(out)
for i,(name,t)in enumerate(frames):
 p=O/f'decoded-{name.replace(" ","-")}.png';subprocess.run([F,'-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(p)],check=True);im=Image.open(p).resize((640,400));x=i%2*640;y=i//2*415;out.paste(im,(x,y));d.text((x+8,y+401),f'{name} {t}s',fill='white')
out.save(O/'video-contact.png');report=dict(checks=checks,passed=sum(checks.values()),failed=sum(not x for x in checks.values()),audio=audio,playing=playing)
(O/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2));raise SystemExit(bool(report['failed']))
