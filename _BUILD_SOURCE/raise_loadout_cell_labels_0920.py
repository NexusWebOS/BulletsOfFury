"""Keep Loadout element labels above the authored bottom rail."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "assets/game.js"
raw = path.read_bytes()
assert b"\r\n" not in raw
old = b"if(art)stageText(art,c.name,cx,B[1]+B[3]*.86,"
new = b"if(art)stageText(art,c.name,cx,B[1]+B[3]*.80,"
assert raw.count(old) == 1, raw.count(old)
path.write_bytes(raw.replace(old, new, 1))
