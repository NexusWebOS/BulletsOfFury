from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil

W=Path(__file__).resolve().parent;R=W/'references';R.mkdir(exist_ok=True);(W/'jobs').mkdir(exist_ok=True)
im=Image.open(r'C:/Users/Mike/Desktop/hammer.gif')
groups=[list(range(29,37)),list(range(37,45)),list(range(8)),[9,12,15,18,21,24,26,28]]
for g,indices in enumerate(groups):
 board=Image.new('RGB',(1600,800),'#17313b');d=ImageDraw.Draw(board)
 for j,k in enumerate(indices):
  im.seek(k);f=im.convert('RGB');f.thumbnail((400,300));board.paste(f,(j%4*400,j//4*400+50));d.text((j%4*400+8,j//4*400+8),str(g*8+j)+' / reference '+str(k),fill='white')
 board.save(R/('overhead-motion-'+str(g)+'.png'))
shutil.copy2(r'C:/Users/Mike/Desktop/hammer.gif',R/'user-hammer.gif')
shutil.copy2(r'C:/Users/Mike/Desktop/PyCciI.gif',R/'user-tire-hammer.gif')
for n in ['chronos','chronos-exact-head','blue-hammer','dracodia','purple-hammer']:
 shutil.copy2(Path(r'C:/Users/Mike/Documents/New project/BOF-Overhead-Slam-1111/references')/(n+'.png'),R/(n+'.png'))
task={'objective':'Replace four-pose held attacks with smooth reference-led weighted motion for BOTH bosses/forms. Correct hilt grip, deep windup, square ground contact, quick second strike, recovery, winding into true whirlwind, twisting left/right sweeps. Preserve original character/weapon designs and native HP/damage/audio/progression.',
 'userReferences':['user-hammer.gif','user-tire-hammer.gif'],'overheadGuideFrames':groups,'overheadUniqueFrames':32,'sideTargetUniqueFrames':24,'whirlTargetUniqueFrames':32,
 'legacyFrameMap':'New overhead32: index=floor(oldLogicalFrame*2). Full source is chronological32-frame cycle, rotated to start ready. Contact is22. 0..15 lift/load,16..21 downstroke,22 impact,23 compression,24..31 recovery. Interpolate logical frame CHOICE (never pixels) so actual intermediate drawings are used.',
 'installedBaseline':'cap_strikes_1111 remains installed. No new heavy assets installed yet.',
 'candidateNotes':'Straight hilt master exec-7924cc85 is a useful grip identity reference. Unguided sheet exec-91c784f7 has clipped tips and is rejected. User supplied GIF motion now supersedes earlier invented poses.'}
(W/'task.json').write_text(json.dumps(task,indent=2))
print('Prepared four exact8-frame motion guide groups from the user GIF;32 distinct sampled poses.')
