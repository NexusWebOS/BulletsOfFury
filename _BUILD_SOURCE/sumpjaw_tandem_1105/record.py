"""Full native Furious Sumpjaw tandem fight;60s hold-fire before the input-only pilot attacks."""
from pathlib import Path
import sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');source=R/'_BUILD_SOURCE/record_boss_comparison_1102.py';sys.path.insert(0,str(source.parent))
text=source.read_text().replace("demonstrate=35 if stage in [5,8]and role=='boss'else 27","demonstrate=60 if stage==7 and role=='mini'else 35 if stage in [5,8]and role=='boss'else 27")
text=text.replace("paths=['index.html']","capture=capture.replace('video/webm;codecs=vp8,opus','video/mp4').replace('cv.captureStream(30)','cv.captureStream(0)').replace('if(cfg.playfield){','if(cfg.playfield){const frame=Math.floor(elapsed*30);if(frame!==window.captureFrame120){window.captureFrame120=frame;window.reviewRecorder?.stream.getVideoTracks()[0]?.requestFrame();}')\npaths=['index.html']")
text=text.replace('storm:b?._fb112?',"tandem:b?._sj120?{mode:b._sj120.mode,hop:b._sj120.hop,cycle:b._sj120.cycle,bar:b._sj120.bar,events:SJ120.events.slice(-10)}:null,storm:b?._fb112?")
sys.argv=[str(source),'--difficulty','furious','--stages','7','--ids','stage7-mini','--track','sumpjaw-tandem-final-1105','--capture-codec','vp8','--playfield']
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
