from pathlib import Path
import subprocess
W=Path(__file__).parent;O=W.parents[1]/'outputs/dracodia-helicopter'
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
names=['guns','missiles','intercepts','pod-break']
for n in names:run(['-i',str(W/(n+'.mkv')),'-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(O/(n+'.mp4'))])
with(W/'concat.txt').open('w',encoding='utf-8')as f:
 for n in names:f.write("file '"+str((O/(n+'.mp4')).resolve()).replace('\\','/')+"'\n")
run(['-f','concat','-safe','0','-i',str(W/'concat.txt'),'-c','copy','-movflags','+faststart',str(O/'helicopter-upgraded.mp4')])
for n,t in [('guns',3.7),('intercepts',4.9),('pod-break',1.4)]:run(['-t',str(t),'-i',str(W/(n+'.mkv')),'-filter_complex','[0:v]fps=15,split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(O/(n+'-preview.gif'))])
print('Saved finished native helicopter movie and GIF previews')
