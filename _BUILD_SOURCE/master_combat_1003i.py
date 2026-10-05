"""Master generated cues; retain untouched ElevenLabs originals and provenance."""
from pathlib import Path
import json,subprocess,shutil,hashlib
import numpy as np
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];A=R/'assets/game/combat_1003i';S=R/'_ART_SOURCES/combat_1003i/audio_originals';S.mkdir(parents=True,exist_ok=True)
ff=imageio_ffmpeg.get_ffmpeg_exe();sr=44100;rows=[]
loops={'laser_burn','firewall_burn','cole_laser6','cole_laser7'}
for p in sorted(A.glob('*.mp3')):
 original=S/p.name
 if not original.exists():shutil.copyfile(p,original)
 raw=subprocess.run([ff,'-v','error','-i',str(original),'-f','f32le','-ac','2','-ar',str(sr),'-'],capture_output=True,check=True).stdout
 x=np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy();rawpeak=float(np.abs(x).max());rawrms=float(np.sqrt(np.mean(x*x)))
 # Short zero-edge ramps remove clicks. Loop endpoints crossfade over 40 ms;
 # the latter is joined to the start once, then plays with a continuous seam.
 if p.stem in loops:
  n=min(int(.04*sr),len(x)//8);ramp=np.linspace(0,1,n)[:,None]
  cross=x[-n:]*(1-ramp)+x[:n]*ramp;x=np.concatenate([cross,x[n:-n]])
  # MP3's transform window can ring at a nonzero file boundary despite a smooth
  # PCM seam. A 4 ms zero-edge ramp prevents an audible tick after encoding.
  n=int(.004*sr);x[:n]*=np.linspace(0,1,n)[:,None];x[-n:]*=np.linspace(1,0,n)[:,None]
 else:
  n=min(int(.004*sr),len(x)//8);x[:n]*=np.linspace(0,1,n)[:,None]
  n=min(int(.035*sr),len(x)//8);x[-n:]*=np.linspace(1,0,n)[:,None]
 rms=float(np.sqrt(np.mean(x*x)));peak=float(np.abs(x).max());target=.13 if p.stem in loops else .17
 gain=min(target/max(rms,1e-9),.79/max(peak,1e-9));x*=gain
 subprocess.run([ff,'-v','error','-y','-f','f32le','-ar',str(sr),'-ac','2','-i','pipe:0','-c:a','libmp3lame','-b:a','160k',str(p)],input=x.astype('<f4').tobytes(),check=True)
 decoded=subprocess.run([ff,'-v','error','-i',str(p),'-f','f32le','-ac','2','-ar',str(sr),'-'],capture_output=True,check=True)
 y=np.frombuffer(decoded.stdout,dtype='<f4').reshape(-1,2)
 rows.append({'name':p.stem,'seconds':round(len(y)/sr,4),'rawPeak':rawpeak,'rawRMS':rawrms,'gain':gain,'peak':float(np.abs(y).max()),'rms':float(np.sqrt(np.mean(y*y))),'clippedSamples':int(np.count_nonzero(np.abs(y)>=1)),'loop':p.stem in loops,'seamDelta':float(np.max(np.abs(y[-1]-y[0]))) if p.stem in loops else None,'source':original.relative_to(R).as_posix(),'file':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(A/'audio-masters.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'count':len(rows),'maxPeak':max(r['peak'] for r in rows),'clipped':sum(r['clippedSamples'] for r in rows),'maxLoopSeam':max(r['seamDelta'] or 0 for r in rows)},indent=2))
