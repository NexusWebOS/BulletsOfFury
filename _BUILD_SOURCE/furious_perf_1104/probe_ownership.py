from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2];W=R/'_shots/furious_perf_1104';W.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
port,stop=serve(str(R));source=R/'_BUILD_SOURCE/probe_furious_encounters_1102.py';text=source.read_text()
out=W/'ownership';out.mkdir(exist_ok=True)
text=text.replace("O=R/'_shots/furious_encounters_1102'",'O=Path('+repr(str(out))+')').replace('http://127.0.0.1:8805/game/index.html',f'http://127.0.0.1:{port}/index.html')
try:exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
finally:stop()
