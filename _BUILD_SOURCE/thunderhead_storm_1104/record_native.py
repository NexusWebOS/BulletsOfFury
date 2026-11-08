"""Record the real high-quality game canvas directly, avoiding compositor copies.
The native boss health bar remains in the footage. Cabinet side rails are outside
this canvas. Audio, input bot,45s player hold-fire, native HP/defeat remain live.
"""
from pathlib import Path
import sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');source=R/'_BUILD_SOURCE/record_boss_comparison_1102.py';sys.path.insert(0,str(source.parent))
text=source.read_text().replace("demonstrate=35 if stage in [5,8]and role=='boss'else 27","demonstrate=45 if stage==6 and role=='boss'else 35 if stage in [5,8]and role=='boss'else 27")
text=text.replace("paths=['index.html']", "capture=capture.replace('codecs=vp8,opus','codecs=h264,opus')\npaths=['index.html']")
sys.argv=[str(source),'--difficulty','furious','--stages','6','--ids','stage6-boss','--track','thunderhead-storm-native-final-1104','--capture-codec','vp8','--playfield']
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
