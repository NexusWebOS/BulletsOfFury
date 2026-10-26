from pathlib import Path
import subprocess,json
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];D=R/'_shots/chronos_final_1025';G=D/'gameplay';C=D/'rage-checkpoint';out=G/'final-reviewed.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe()
filters='[0:v]trim=end=150,setpts=PTS-STARTPTS[v0];[0:a]atrim=end=150,asetpts=PTS-STARTPTS[a0];[1:v]setpts=PTS-STARTPTS[v1];[1:a]asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]'
subprocess.run([ff,'-y','-loglevel','error','-i',str(G/'stage5-furious-with-audio.mp4'),'-i',str(C/'rage-checkpoint.mp4'),'-filter_complex',filters,'-map','[v]','-map','[a]','-r','30','-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
a=json.loads((G/'gameplay-recording.json').read_text());b=json.loads((C/'checkpoint-recording.json').read_text());r={'video':out.relative_to(R).as_posix(),'route':'First150s continuous native Furious gameplay with normal controls; then a clearly labeled late-chaingun16%-to-15% HP checkpoint. Native simulation/poses throughout. Invulnerability enabled.','errors':a['errors']+b['errors'],'timeline':[q for q in a['timeline'] if q['videoSeconds']<150]+[{**q,'videoSeconds':q['videoSeconds']+150}for q in b['timeline']],'sourceAudio':{'fight':a['audio'],'checkpoint':b['audio']}};(G/'final-review.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8')
subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],check=True)
for name,time in [('charge',24.8),('double',45.2),('ring',94.6),('rage',158.2),('rage-swing',170)]:
 subprocess.run([ff,'-y','-loglevel','error','-ss',str(time),'-i',str(out),'-frames:v','1',str(D/('review-'+name+'.png'))],check=True)
print(json.dumps({'video':str(out),'fullDecode':True,'errors':r['errors']}),flush=True)
