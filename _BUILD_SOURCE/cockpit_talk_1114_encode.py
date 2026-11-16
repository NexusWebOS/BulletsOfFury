from pathlib import Path
import subprocess,json
import imageio_ffmpeg
OUT=ROOT/'_shots/cockpit_talk_1114';FF=imageio_ffmpeg.get_ffmpeg_exe();clips=json.loads((OUT/'recording.json').read_text(encoding='utf-8'))['clips'];ENC=OUT/'encoded';ENC.mkdir(exist_ok=True)
def run(args):subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],check=True)
codec=['-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','128k','-movflags','+faststart']
run(['-i',str(OUT/'cole-service-datalink.webm'),*codec,str(OUT/'cole-service-datalink.mp4')])
pilots=[q['clip']for q in clips if q['clip']!='cole-service-datalink']
for pk in pilots:run(['-ss','1.7','-i',str(OUT/(pk+'-talk.webm')),'-t','2.8',*codec,str(ENC/(pk+'.mp4'))])
(ENC/'concat.txt').write_text('\n'.join("file '"+p+".mp4'"for p in pilots),encoding='utf-8')
run(['-f','concat','-safe','0','-i',str(ENC/'concat.txt'),'-c','copy','-movflags','+faststart',str(OUT/'all-pilots-talking.mp4')])
run(['-i',str(ENC/'cole.mp4'),'-filter_complex','[0:v]fps=10,scale=768:-1:flags=neighbor,split[a][b];[a]palettegen[p];[b][p]paletteuse','-loop','0',str(OUT/'cole-talking.gif')])
proof=[]
for name in ['cole-service-datalink.mp4','all-pilots-talking.mp4']:
 r=subprocess.run([FF,'-v','error','-i',str(OUT/name),'-f','null','-'],capture_output=True,text=True)
 assert r.returncode==0 and not r.stderr,(name,r.stderr)
 levels=subprocess.run([FF,'-hide_banner','-i',str(OUT/name),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True)
 stats=[q.strip()for q in levels.stderr.splitlines()if 'mean_volume:' in q or 'max_volume:' in q]
 proof.append({'file':name,'decodeExitCode':r.returncode,'decodeErrors':r.stderr,'audio':stats})
 print(name+' decoded cleanly; '+str(stats),flush=True)
run(['-ss','2','-i',str(OUT/'all-pilots-talking.mp4'),'-frames:v','1',str(OUT/'decoded-cole.png')])
run(['-ss','13.8','-i',str(OUT/'all-pilots-talking.mp4'),'-frames:v','1',str(OUT/'decoded-falva.png')])
(OUT/'media-qa.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
