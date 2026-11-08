"""Real-engine film:45s hold-fire demonstration, then native input-only victory.
Only the recording fixture's demonstration window changes. Enemy HP, phases,
clocks, weather, collision and attacks are never rewritten during the fight.
"""
from pathlib import Path
import sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');source=R/'_BUILD_SOURCE/record_boss_comparison_1102.py';sys.path.insert(0,str(source.parent))
text=source.read_text().replace("demonstrate=35 if stage in [5,8]and role=='boss'else 27","demonstrate=45 if stage==6 and role=='boss'else 35 if stage in [5,8]and role=='boss'else 27")
sys.argv=[str(source),'--difficulty','furious','--stages','6','--ids','stage6-boss','--track','thunderhead-storm-1104','--capture-codec','vp8']
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
