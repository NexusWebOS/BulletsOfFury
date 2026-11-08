"""Full native Furious fight,60s observation before the input-only pilot fires."""
from pathlib import Path
import sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');source=R/'_BUILD_SOURCE/record_boss_comparison_1102.py';sys.path.insert(0,str(source.parent))
text=source.read_text().replace("demonstrate=35 if stage in [5,8]and role=='boss'else 27","demonstrate=60 if stage==6 and role=='mini'else 35 if stage in [5,8]and role=='boss'else 27")
text=text.replace("paths=['index.html']","capture=capture.replace('video/webm;codecs=vp8,opus','video/mp4').replace('cv.captureStream(30)','cv.captureStream(0)').replace('if(cfg.playfield){','if(cfg.playfield){const frame=Math.floor(elapsed*30);if(frame!==window.captureFrame118){window.captureFrame118=frame;window.reviewRecorder?.stream.getVideoTracks()[0]?.requestFrame();}')\npaths=['index.html']")
text=text.replace('storm:b?._fb112?',"tempest:b?._rw118?{state:b._rw118.state,orb:b._rw118.orb?{t:b._rw118.orb.t,size:b._rw118.orb.size}:null,events:RW118.events.slice(-8)}:null,storm:b?._fb112?")
sys.argv=[str(source),'--difficulty','furious','--stages','6','--ids','stage6-mini','--track','razorwake-tempest-final-ready-1105','--capture-codec','vp8','--playfield']
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
