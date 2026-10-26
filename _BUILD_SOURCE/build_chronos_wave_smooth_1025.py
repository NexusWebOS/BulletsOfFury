from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path('assets/game/shared/combat/chronos_wave_1025');old=Image.open(root/'wave.png').convert('RGBA');frames=[old.crop((0,0,320,640)),old.crop((320,0,640,640))]
for i in range(1,25):
 im=Image.open(f'_shots/chronos_wave_smooth_1025/source/{i:02d}.png').convert('RGBA');assert im.size==(128,256),im.size
 frames.append(im.resize((320,640),Image.Resampling.NEAREST))
frames += [old.crop((640,640,960,1280)),old.crop((960,640,1280,1280))]
sheet=Image.new('RGBA',(2560,2560));contact=Image.new('RGB',(8*128,4*256),(4,18,30))
for i,f in enumerate(frames):sheet.paste(f,((i%8)*320,(i//8)*640));contact.paste(f.resize((128,256)),((i%8)*128,(i//8)*256),f.resize((128,256)))
sheet.save(root/'wave_smooth.png');contact.save('_shots/chronos_wave_smooth_1025/contact.png')
(root/'manifest_smooth.json').write_text(json.dumps(dict(image='wave_smooth.png',width=2560,height=2560,columns=8,rows=4,frameWidth=320,frameHeight=640,pivot=[160,24],frames=28,sustainFrames=24,fps=24,pixellabJob='a99208a6-648c-4232-99fd-fd2dd53f0386'),indent=2))
