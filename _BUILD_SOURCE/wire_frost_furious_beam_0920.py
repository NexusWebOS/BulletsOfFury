"""Wire the Furious Frost Cruiser to its authored-source blue beam variant."""
from pathlib import Path


GAME = Path(__file__).resolve().parents[1] / "assets/game.js"
raw = GAME.read_bytes()
assert b"\r\n" not in raw, "game.js must remain LF"
src = raw.decode("utf-8")


def replace_once(old: str, new: str) -> None:
    global src
    assert src.count(old) == 1, f"expected one match, found {src.count(old)}: {old[:80]}"
    src = src.replace(old, new, 1)


replace_once(
    "  BOFX.img.fzt_fire_laser_0920='assets/game/bosses/furnace/fzt_fire_laser_0920.png';",
    "  BOFX.img.fzt_fire_laser_0920='assets/game/bosses/furnace/fzt_fire_laser_0920.png';\n"
    "  BOFX.img.frost_furious_beam_0920='assets/game/bosses/frost/frost_furious_beam_0920.png';",
)

replace_once(
    "  const C=shipBossMount(b,'C'),a=Math.PI/2+(J.beamAng||0),len=VH*1.55,bw=frost?FROST_BEAM_WIDTH:42;\n"
    "  const key='nlz_3_b'+(Math.floor((b.t||0)*14)%6);if(!XART.rdy(key))return;",
    "  const C=shipBossMount(b,'C'),a=Math.PI/2+(J.beamAng||0),len=VH*1.55,bw=frost?FROST_BEAM_WIDTH:42;\n"
    "  if(frost&&diffKey==='furious'){\n"
    "    const key='frost_furious_beam_0920';if(!XART.rdy(key))return;\n"
    "    const im=XART.get(key);\n"
    "    ctx.save();ctx.translate(C.x,C.y);ctx.rotate(a-Math.PI/2);ctx.imageSmoothingEnabled=false;\n"
    "    ctx.globalCompositeOperation='source-over';ctx.shadowColor='#255bd4';ctx.shadowBlur=7;\n"
    "    const artW=bw*2.8;ctx.drawImage(im,-artW*.5,-5,artW,len);\n"
    "    ctx.restore();return;\n"
    "  }\n"
    "  const key='nlz_3_b'+(Math.floor((b.t||0)*14)%6);if(!XART.rdy(key))return;",
)

GAME.write_bytes(src.encode("utf-8"))
print("Wired Furious Frost Cruiser beam; kept LF and existing collision geometry")
