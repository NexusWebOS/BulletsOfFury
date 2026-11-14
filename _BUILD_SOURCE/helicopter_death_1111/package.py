from pathlib import Path
import subprocess
W=Path(__file__).parent;O=W.parents[1]/'outputs/helicopter-death'
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
names=['stage1-normal','stage1-furious','dracodia']
for n in names:run(['-i',str(W/(n+'.mkv')),'-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(O/(n+'.mp4'))])
with(W/'concat.txt').open('w',encoding='utf-8')as f:
 for n in names:f.write("file '"+str((O/(n+'.mp4')).resolve()).replace('\\','/')+"'\n")
run(['-f','concat','-safe','0','-i',str(W/'concat.txt'),'-c','copy','-movflags','+faststart',str(O/'helicopter-death-spirals.mp4')])
for n,seconds in [('stage1-furious',8.6),('dracodia',5.4)]:run(['-t',str(seconds),'-i',str(W/(n+'.mkv')),'-filter_complex','[0:v]fps=15,split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(O/(n+'.gif'))])
print('Saved finished Stage1 / Dracodia death movies and GIFs')
