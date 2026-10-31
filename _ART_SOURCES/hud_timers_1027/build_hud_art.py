from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,subprocess,hashlib
W=Path(__file__).resolve().parent;R=W.parents[1];D=W/'compiled';D.mkdir(exist_ok=True)
old=Image.open(R/'assets/game/shared/ui/command_1020/hud-a-right.webp').convert('RGBA');ai=W/'square-bay-generated.png';shutil.copy2(ai,D/'square-bay-generated.png');new=Image.open(ai).convert('RGBA').resize(old.size,Image.Resampling.NEAREST);new.paste(old.crop((0,384,376,1024)),(0,384))
# Production cleanup: deterministic square aperture in the generated bezel.
g=ImageDraw.Draw(new);g.rectangle((67,71,300,304),fill=(9,13,16,255));g.rectangle((68,72,299,303),outline=(61,73,77,255),width=1);g.rectangle((70,74,297,301),fill=(3,13,18,255));new.save(D/'hud-right-square.png')
# Reuse the existing steel armor-meter bezel as an authored timer family.
source=old.crop((48,895,328,976))
def nine(src,w,h):
 out=Image.new('RGBA',(w,h));xs=[0,32,src.width-32,src.width];ys=[0,28,src.height-24,src.height];dx=[0,32,w-32,w];dy=[0,28,h-24,h]
 for a in range(3):
  for b in range(3):out.alpha_composite(src.crop((xs[b],ys[a],xs[b+1],ys[a+1])).resize((dx[b+1]-dx[b],dy[a+1]-dy[a]),Image.Resampling.NEAREST),(dx[b],dy[a]))
 return out
for w in [376,480]:nine(source,w,88).save(D/f'timer-{w}.png')
ase=Path(r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe')
for f in ['hud-right-square','timer-376','timer-480']:
 subprocess.run([str(ase),'--batch',str(D/(f+'.png')),'--save-as',str(D/(f+'.aseprite'))],check=True,capture_output=True)
(D/'manifest.json').write_text(json.dumps({'right':{'file':'hud-right-square.png','size':[376,1024],'portrait':[70,74,228,228],'name':[82,329,216,39],'source':str(ai),'unchangedBelowY':384},'headers':{'wide':[376,88],'compactHalf':[480,88]},'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in D.glob('*.png')}},indent=2))
print('Square portrait and two fixed timer housings authored/exported.')

for f in D.glob("*.png"):
 if f.name!="square-bay-generated.png":shutil.copy2(f,R/"assets/game/shared/ui/hud_timers_1027"/f.name)
