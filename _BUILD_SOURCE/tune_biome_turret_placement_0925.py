"""Keep ice jets airborne and ensure fixed biome emplacements actually appear."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "assets/game.js"
data = path.read_bytes()

def sub(old: str, new: str) -> None:
    global data
    a = old.encode(); assert data.count(a) == 1, (old[:90], data.count(a))
    data = data.replace(a, new.encode(), 1)

sub("s3barge:'stage3_ice_jet_02',", "")
sub("  const _biomePlate=_biomeArtByStage[run.stage]&&_biomeArtByStage[run.stage][type];",
    "  let _biomePlate=_biomeArtByStage[run.stage]&&_biomeArtByStage[run.stage][type];\n"
    "  if(run.stage===3&&type==='s3interceptor'&&enemies.length%2)\n"
    "    _biomePlate='stage3_ice_jet_02';")
sub("  if(x==null&&[4,6,7,8].includes(stageNum))x=target;",
    "  if(x==null&&[2,3,4,6,7,8].includes(stageNum))x=target;")
assert b"\r\n" not in data
path.write_bytes(data)
print("Two Stage 3 jet variants alternate; biome turret platforms have a fallback")
