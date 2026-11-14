from pathlib import Path
import subprocess
W=Path(__file__).parent;O=W.parents[1]/'outputs/dam-impact'
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
names=['dam-normal','dam-furious']
for n in names:run(['-i',str(W/(n+'.mkv')),'-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(O/(n+'.mp4'))])
with(W/'concat.txt').open('w',encoding='utf-8')as f:
 for n in names:f.write("file '"+str((O/(n+'.mp4')).resolve()).replace('\\','/')+"'\n")
run(['-f','concat','-safe','0','-i',str(W/'concat.txt'),'-c','copy','-movflags','+faststart',str(O/'dam-crash-transition.mp4')])
run(['-i',str(W/'dam-furious.mkv'),'-filter_complex','[0:v]fps=15,split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(O/'dam-crash.gif')]);print('Saved dam collision and white-fade previews')
