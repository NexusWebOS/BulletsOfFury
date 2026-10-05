"""Import approved knight pose components and rotate the Stage 8 music assignment."""
from pathlib import Path
import hashlib,json,shutil,subprocess
from PIL import Image
from collections import deque
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1]
O=R/'assets/game/campaign_focus_1004b';O.mkdir(exist_ok=True)
generated=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c/exec-41508a58-20d2-473f-b722-a8ac2e5a91f5.png')
S=R/'_ART_SOURCES/campaign_focus_1004b';S.mkdir(exist_ok=True)
src=S/'knight_poses.png'
if not src.exists():shutil.copy2(generated,src)
im=Image.open(src).convert('RGBA');rects={}
# Trim the principal component, excluding generation dust and a neighboring row's stray pixels.
def principal_bounds(cell):
 w,h=cell.size;alpha=cell.getchannel('A');mask=bytearray(1 if a>8 else 0 for a in alpha.tobytes());best=[]
 for pos in range(w*h):
  if not mask[pos]:continue
  mask[pos]=0;q=deque([pos]);part=[]
  while q:
   p=q.popleft();part.append(p);x=p%w;y=p//w
   for ny in range(max(0,y-1),min(h,y+2)):
    for nx in range(max(0,x-1),min(w,x+2)):
     n=ny*w+nx
     if mask[n]:mask[n]=0;q.append(n)
  if len(part)>len(best):best=part
 assert best
 return (max(0,min(p%w for p in best)-1),max(0,min(p//w for p in best)-1),min(w,max(p%w for p in best)+2),min(h,max(p//w for p in best)+2))
for row,name in enumerate(['core','legL','legR']):
 for col in range(4):
  cell=im.crop((col*im.width//4,row*im.height//3,(col+1)*im.width//4,(row+1)*im.height//3))
  box=principal_bounds(cell)
  part=cell.crop(box);part.save(O/f'{name}_{col}.png')
  rects[f'{name}_{col}']={'size':part.size,'sourceCell':[col,row],'alphaBounds':box}
(O/'manifest.json').write_text(json.dumps(rects,indent=2)+'\n')
music=R/'assets/game/music';catalog=music/'catalog.json';data=json.loads(catalog.read_text())
if not (music/'Unused_FinalBossDrone.mp3').exists():
 rows={Path(t['file']).name:t for t in data['tracks']}
 first=rows['Level8b.mp3'].copy();second=rows['Level8b2.mp3'].copy();third=rows['Level8b3.mp3'].copy()
 shutil.copy2(music/'Level8b.mp3',music/'Unused_FinalBossDrone.mp3')
 shutil.copy2(music/'Level8b2.mp3',music/'Level8b.mp3')
 shutil.copy2(music/'Level8b3.mp3',music/'Level8b2.mp3')
 rows['Level8b.mp3'].update(formerPath=second['formerPath'],sha256=second['sha256'])
 rows['Level8b2.mp3'].update(formerPath=third['formerPath'],sha256=third['sha256'])
 first['file']='assets/game/music/Unused_FinalBossDrone.mp3';data['tracks'].append(first)
 wav=Path('C:/Users/Mdogg/Desktop/finalform.wav');dst=music/'Level8b3.mp3'
 subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(wav),'-map','0:a:0','-map_metadata','-1','-codec:a','libmp3lame','-b:a','256k','-metadata','title=Final Form',str(dst)],check=True)
 rows['Level8b3.mp3'].update(formerPath=str(wav),sha256=hashlib.sha256(dst.read_bytes()).hexdigest())
 catalog.write_text(json.dumps(data,indent=2)+'\n')
for name in ['Level8b.mp3','Level8b2.mp3','Level8b3.mp3']:
 subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(music/name),'-f','null','-'],check=True)
print('Imported 12 modular poses; all three boss tracks decoded successfully.')
