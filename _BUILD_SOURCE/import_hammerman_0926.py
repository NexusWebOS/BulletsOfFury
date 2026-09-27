"""Preserve Mike's source; encode to the existing Stage 5 track's measured level."""
from pathlib import Path
import subprocess,re,json,shutil
import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
source=Path('C:/Users/Mdogg/Desktop/Hammerman Cometh.wav')
music=Path('assets/game/music');out=Path('_shots/muzzles_0926')
def stats(path):
 p=subprocess.run([ff,'-hide_banner','-i',str(path),'-af','volumedetect','-f','null','-'],capture_output=True,text=True,check=True)
 return {k:float(re.search(k+r':\s+(-?[\d.]+)',p.stderr).group(1)) for k in ['mean_volume','max_volume']}
old=stats(music/'boss5_deadly_night.mp3');new=stats(source)
gain=min(old['mean_volume']-new['mean_volume'],-1-new['max_volume'])
original=music/'originals_0926'/'Hammerman Cometh.wav';original.parent.mkdir(exist_ok=True)
if not original.exists():shutil.copy2(source,original)
target=music/'boss5_hammerman_cometh_0926.mp3'
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(source),'-af',f'volume={gain:.3f}dB','-ar','44100','-ac','2','-b:a','112k',str(target)],check=True)
result={'source':str(source),'original':str(original),'target':str(target),'old':old,'input':new,'gain_db':gain,'encoded':stats(target)}
(out/'music.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
