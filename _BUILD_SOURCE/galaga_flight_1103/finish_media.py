from pathlib import Path
import subprocess,json,os
W=Path(__file__).parent
for kind in ['small','medium','large']:
 source=W/f'{kind}.webm';target=W/f'{kind}-indexed.webm'
 # Packet-copy remux writes duration and seek cues without encoding frames.
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-map','0:v:0','-c','copy',str(target)],check=True)
 target.replace(source)
 subprocess.run(['ffmpeg','-v','error','-y','-ss','7','-i',str(source),'-frames:v','1','-update','1',str(W/f'{kind}-poster.png')],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-show_entries','stream=codec_name,width,height,r_frame_rate','-of','json',str(source)]))
 assert float(probe['format']['duration'])>20 and probe['streams'][0]['width']==960
 (W/f'{kind}-media.json').write_text(json.dumps(probe,indent=2),encoding='utf8')
 print(kind,probe['format'],flush=True)
