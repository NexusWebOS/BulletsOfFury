"""Full native Furious Thunderhead fight;70s observation before the input-only pilot fires."""
from pathlib import Path
import sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');source=R/'_BUILD_SOURCE/record_boss_comparison_1102.py';sys.path.insert(0,str(source.parent))
text=source.read_text().replace("demonstrate=35 if stage in [5,8]and role=='boss'else 27","demonstrate=70 if stage==6 and role=='boss'else 35 if stage in [5,8]and role=='boss'else 27")
text=text.replace("paths=['index.html']","capture=capture.replace('video/webm;codecs=vp8,opus','video/mp4').replace('cv.captureStream(30)','cv.captureStream(0)').replace('if(cfg.playfield){','if(cfg.playfield){const frame=Math.floor(elapsed*30);if(frame!==window.captureFrame118){window.captureFrame118=frame;window.reviewRecorder?.stream.getVideoTracks()[0]?.requestFrame();}')\npaths=['index.html']")
text=text.replace('storm:b?._fb112?',"reactor:b?._tc119?{flow:b._tc119.flow?.state,depth:b._tc119.di,volley:b._tc119.volley,events:TC119.events.slice(-10)}:null,storm:b?._fb112?")
sys.argv=[str(source),'--difficulty','furious','--stages','6','--ids','stage6-boss','--track','thunderhead-reactor-final-1105','--capture-codec','vp8','--playfield']
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
