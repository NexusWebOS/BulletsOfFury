"""Convert Mike's Stage X music without trimming, normalizing or changing speed."""
from pathlib import Path
import hashlib,json,subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1]
src=Path('C:/Users/Mdogg/Desktop/Gasline.wav')
dst=R/'assets/game/levels/stage_x/audio/music/LevelX.mp3'
ff=imageio_ffmpeg.get_ffmpeg_exe()
args=[ff,'-hide_banner','-loglevel','error','-y','-i',str(src),'-map','0:a:0','-map_metadata','-1','-codec:a','libmp3lame','-b:a','256k','-metadata','title=Gasline','-metadata','album=Bullets of Fury - Stage X',str(dst)]
subprocess.run(args,check=True)
subprocess.run([ff,'-v','error','-i',str(dst),'-f','null','-'],check=True)
report={'source':str(src),'sourceBytes':src.stat().st_size,'sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'output':dst.relative_to(R).as_posix(),'outputBytes':dst.stat().st_size,'outputSha256':hashlib.sha256(dst.read_bytes()).hexdigest(),
 'codec':'MP3/libmp3lame','bitrate':'256 kbps','sampleRate':48000,'channels':2,'processing':'Format conversion only. Entire source, original speed and gain.','decodeExitCode':0}
(R/'docs/qa/gasline_1003.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
