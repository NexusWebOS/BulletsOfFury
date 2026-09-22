"""Move Stage-clear Fury Point conversion below the plate's separator rail."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "assets/game.js"
raw = path.read_bytes()
assert b"\r\n" not in raw
old = b"stageTextCoin(art,'LEVEL SCORE '+_sc.toLocaleString('en-US')+'   =','+'+_n,gx+gw/2,(g0+g1)/2,cH,'#ffd24a',0.9,1,0.06);"
new = b"stageTextCoin(art,'LEVEL SCORE '+_sc.toLocaleString('en-US')+'   =','+'+_n,gx+gw/2,g0+(g1-g0)*0.68,cH,'#ffd24a',0.9,1,0.06);"
assert raw.count(old) == 1, raw.count(old)
path.write_bytes(raw.replace(old, new, 1))
print("Positioned FP conversion below the score separator and above sign-off")
