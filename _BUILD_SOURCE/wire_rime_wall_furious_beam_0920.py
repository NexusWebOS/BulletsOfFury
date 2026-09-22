"""Give the Stage-3 Furious Rime Wall its readable giant blue laser release."""
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
    "    if(!stage3FuryFeintStart(b,pat,step,active,width))return true;",
    "    if(!stage3FuryFeintStart(b,pat,step,active,Math.max(width,62)))return true;",
)

replace_once(
    "    if(B.released){ctx.globalAlpha=1;if(wall){const rim=xartTint(key,'#071c51',1);if(rim)ctx.drawImage(rim,-B.width/2-2,0,B.width+4,len);}ctx.drawImage(im,-B.width/2,0,B.width,len);if(wall){const core=XART.get(key);ctx.drawImage(core,-B.width*.065,0,B.width*.13,len);}}ctx.restore();",
    "    if(B.released){\n"
    "      ctx.globalAlpha=1;\n"
    "      const furyBeam=wall&&diffKey==='furious'&&B._furySimon&&XART.rdy('frost_furious_beam_0920')\n"
    "        ?XART.get('frost_furious_beam_0920'):null;\n"
    "      if(furyBeam){\n"
    "        ctx.globalCompositeOperation='source-over';\n"
    "        const artW=B.width*2.8;ctx.drawImage(furyBeam,-artW*.5,0,artW,len);\n"
    "        ctx.globalCompositeOperation='lighter';\n"
    "      }else{\n"
    "        if(wall){const rim=xartTint(key,'#071c51',1);if(rim)ctx.drawImage(rim,-B.width/2-2,0,B.width+4,len);}\n"
    "        ctx.drawImage(im,-B.width/2,0,B.width,len);\n"
    "        if(wall){const core=XART.get(key);ctx.drawImage(core,-B.width*.065,0,B.width*.13,len);}\n"
    "      }\n"
    "    }ctx.restore();",
)

replace_once(
    "  if(typeof l23FovWarm==='function')l23FovWarm();   // 0912x: the laser's FOV cones and alert frames",
    "  if(typeof l23FovWarm==='function')l23FovWarm();   // 0912x: the laser's FOV cones and alert frames\n"
    "  if(SHIPBOSS[b._ship].key==='nsb_rimewall_intact'&&XART._touch)XART._touch('frost_furious_beam_0920');",
)

GAME.write_bytes(src.encode("utf-8"))
print("Wired Rime Wall Furious giant beam and matching Simon-Says width")
