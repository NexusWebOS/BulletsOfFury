from pathlib import Path
import json,subprocess
W=Path(__file__).resolve().parent;D=W.parent if (W.parent/'overlay').is_dir() else W.parent/'outputs/BOF-Cutscenes-1103';O=D/'source-art/aseprite';O.mkdir(exist_ok=True)
M=json.loads((D/'overlay/assets/game/shared/cinematics/story_1103/manifest.json').read_text())
jobs=[]
for name,a in M['banks'].items():
 duration=1/M['comicScroll']['fps']if name.startswith('comic-scroll-')else 1.8 if name.startswith('cable-')else 1/8 if name.startswith('return-')else 1/12
 jobs.append({'name':name,'input':str((D/'overlay'/a['path']).resolve()),'output':str((O/(name+'.aseprite')).resolve()),'w':a['w'],'h':a['h'],'cols':a['cols'],'frames':a['frames'],'duration':duration,'pivot':a['pivot']})
 if name.startswith('comic-scroll-'):jobs[-1]['frameDurations']=[round((i+1)*duration*1000)-round(i*duration*1000)for i in range(a['frames'])]
 if name.startswith('headset-') and a['frames']==24:
  jobs[-1]['tags']=[{'name':n,'first':i+1,'last':j+1}for n,i,j in [('front-talk',0,3),('left-quarter-talk',4,5),('left-profile-talk',6,7),('right-quarter-talk',8,9),('right-profile-talk',10,11),('happy',12,13),('sad',14,15),('angry',16,17),('scared',18,19),('surprised',20,21),('determined',22,23)]]
(W/'aseprite-jobs.json').write_text(json.dumps(jobs))
report=D/'verification/aseprite.json'
r=subprocess.run([r'C:\Users\Mike\Desktop\Retro Dev Tools\Graphics\Aseprite\aseprite.exe','--batch','--script-param','jobs='+str((W/'aseprite-jobs.json').resolve()),'--script-param','report='+str(report.resolve()),'--script',str((D/'source/author_timelines.lua').resolve())],capture_output=True,text=True)
print(r.stdout[-2000:]);print(r.stderr[-2000:]);r.check_returncode()
data=json.loads(report.read_text());bad=[a for a in data if a['different']]
print(json.dumps({'banks':len(data),'frames':sum(a['frames']for a in data),'changed_pixel_frames':sum(a['different']for a in data)}))
if bad:raise SystemExit('Aseprite changed source pixels: '+str(bad))
