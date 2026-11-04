from pathlib import Path
import subprocess,os,shutil
from PIL import Image
R=Path(__file__).resolve().parents[2]
S=R/'_BUILD_SOURCE/art_sources/menu_sceneries_1103'
A=R/'assets/game/shared/ui/menu_sceneries_1103'
exe=os.environ.get('ASEPRITE_PATH') or shutil.which('aseprite') or 'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'
keys=['orbit','command','hangar','forge','hq','vault','industrial_front','orbit_front','coastal_front']
for key in keys:
    subprocess.run([exe,'--batch',str(S/(key+'.aseprite')),'--scale',str(512/724),'--save-as',str(A/(key+'.png'))],check=True)
    assert Image.open(A/(key+'.png')).size==(1536,512)
    if not key.endswith('_front'):
        subprocess.run([exe,'--batch',str(S/(key+'.aseprite')),'--scale',str(1280/724),'--crop','1152,0,1536,1280','--save-as',str(A/(key+'_portrait.png'))],check=True)
        assert Image.open(A/(key+'_portrait.png')).size==(1536,1280)
print('Exported 15 even-size native images with original alpha retained.')
