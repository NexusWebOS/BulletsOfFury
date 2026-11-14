from native import *
import shutil,zipfile
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
for src,name in [('phoenix-core-revised','phoenix-core'),('phoenix-vortex','phoenix-vortex'),('eye-lasers','eye-lasers'),('lightning-dodge','purple-lightning'),('shield','shield')]:
 run(['-i',str(W/(src+'.mkv')),'-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(O/(name+'.mp4'))])
with (W/'concat.txt').open('w',encoding='utf-8')as f:
 for n in ['phoenix-core','phoenix-vortex','eye-lasers','purple-lightning','shield']:f.write("file '"+str((O/(n+'.mp4')).resolve()).replace('\\','/')+"'\n")
run(['-f','concat','-safe','0','-i',str(W/'concat.txt'),'-c','copy','-movflags','+faststart',str(O/'dracodia-upgraded.mp4')])
for src,name,duration in [('phoenix-vortex','phoenix-preview',7),('lightning-dodge','lightning-preview',5.5),('shield','shield-preview',3.6)]:
 run(['-ss','0'if src!='shield'else'0.65','-t',str(duration),'-i',str(W/(src+'.mkv')),'-filter_complex','[0:v]fps=15,split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=none','-loop','0',str(O/(name+'.gif'))])
print('Saved native videos and GIF previews',flush=True)
