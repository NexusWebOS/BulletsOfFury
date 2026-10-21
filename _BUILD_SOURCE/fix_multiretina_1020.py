from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'assets/game.js';s=p.read_text(encoding='utf-8');old='if(!retinaScanHeld()&&_nowT-player._tap';new='if(_nowT-player._tap'
assert s.count(old)==2,s.count(old);s=s.replace(old,new);p.write_text(s,encoding='utf-8',newline='\n');print('Multi-Retina no longer rejects left/right dodge taps; ordinary cooldown and mounting restrictions retained.')
