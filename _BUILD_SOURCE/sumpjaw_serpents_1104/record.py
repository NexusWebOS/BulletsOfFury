"""Native real-RAF Furious Sumpjaw fight;45s observation then input-only attack pilot."""
from pathlib import Path
import sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');source=R/'_BUILD_SOURCE/record_boss_comparison_1102.py';sys.path.insert(0,str(source.parent))
text=source.read_text().replace("demonstrate=35 if stage in [5,8]and role=='boss'else 27","demonstrate=45 if stage==7 and role=='mini'else 35 if stage in [5,8]and role=='boss'else 27")
text=text.replace("paths=['index.html']", "capture=capture.replace('video/webm;codecs=vp8,opus','video/mp4')\npaths=['index.html']")
sys.argv=[str(source),'--difficulty','furious','--stages','7','--ids','stage7-mini','--track','sumpjaw-serpents-final-1104','--capture-codec','vp8','--playfield']
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
