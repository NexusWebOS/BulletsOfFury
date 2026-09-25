"""One confirm press completes the reveal and deploys the visible pilot."""
from pathlib import Path

p=Path('assets/game.js');b=p.read_bytes();assert b'\r\n' not in b
old=b"  if(pilotConfirmPressed()){ if(locked){ Audio.SFX.hit(); pilotFlash=1; } else confirmPilot(); }"
new=b"  if(pilotConfirmPressed()){ pcSkip(); if(locked){ Audio.SFX.hit(); pilotFlash=1; } else confirmPilot(); }"
assert b.count(old)==1;p.write_bytes(b.replace(old,new))
