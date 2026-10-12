"""Replace only the pilot-card drawing; preserve its complete input/launch flow."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'assets/game.js';s=p.read_text(encoding='utf-8')
start=s.index('    psPanelBox(PX,PY,PW,PH,P.tint,true);',s.index('function drawPilot(dt)')) if 'pt11PilotCard(P,PX' not in s else -1
if start>=0:
    end=s.index('    if(locked && pilotFlash>0){',start)
    s=s[:start]+'    pt11PilotCard(P,PX,PY,PW,PH,spin,locked);\n'+s[end:]
    p.write_text(s,encoding='utf-8',newline='\n')
p=ROOT/'PLAY_BULLETS_OF_FURY.bat';b=p.read_bytes()
old=b'''start "" /min powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Milliseconds 900; Start-Process 'http://127.0.0.1:%PORT%/index.html'"'''
new=b'''start "" /min %PYEXE% %PYARGS% "_BUILD_SOURCE\\launch_browser_1011.py" %PORT%'''
if old in b:p.write_bytes(b.replace(old,new))
print('Pilot drawing and fullscreen launch updated; input and batch line endings preserved.')
