from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/carriers';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
src=R/'_BUILD_SOURCE/probe_carrier_campaign_1101.py';code=src.read_text(encoding='utf8').replace("O=R/'_shots/carrier_assault_1101'","O=R/'_shots/release_qa_1116/carriers'").replace('http://127.0.0.1:8805/game/index.html','http://127.0.0.1:8765/index.html')
code=code.replace('player.invuln=40002;', 'player.invuln=40002;player._spawnClearT=40002;')
exec(compile(code,str(src),'exec'),{'__file__':str(src),'__name__':'__main__'})
