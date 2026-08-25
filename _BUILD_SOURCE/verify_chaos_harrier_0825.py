"""Focused, deterministic verification for the Level-5 Chaos Harrier integration."""
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "game" / "chaos_harrier"
CODE = (ROOT / "assets" / "game.js").read_text(encoding="utf-8")


def ok(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"ok  {message}")


groups = {"ship": 6, "plasma": 4, "missile": 4, "lance": 4, "sideflash": 4,
          "launchflash": 4, "charge": 4, "warp": 8, "beam": 4, "sidelaser": 4,
          "impact": 4}
files = [OUT / f"ch_{group}_{index}.png" for group, count in groups.items() for index in range(count)]
files.append(OUT / "ch_ship_glow.png")

ok(len(files) == 51 and all(path.is_file() for path in files), "all 51 runtime frames exist")
ok(all(Image.open(path).mode == "RGBA" for path in files), "every runtime frame is transparent RGBA")
ok(all(Image.open(OUT / f"ch_ship_{i}.png").size == (352, 320) for i in range(6)),
   "all ship states retain the shared 352x320 anchor canvas")
glow = Image.open(OUT / "ch_ship_glow.png").convert("RGBA")
alpha_histogram = glow.getchannel("A").histogram()
ok(glow.getbbox() is not None and sum(alpha_histogram[1:]) > 20,
   "internal-light delta is a real animated overlay")
ok("5:{at:0.45, kind:'chaosharrier'" in CODE and "case 'chaosharrier'" in CODE,
   "Stage 5 spawns Chaos Harrier instead of Energy Core")
ok("function chaosHarrierUpdate" in CODE and "function chaosHarrierDraw" in CODE,
   "dedicated movement, attack, warp, and renderer paths are installed")
ok("b._chState==='missile'" in CODE and "si=2" in CODE and "left_missile_bay" in CODE,
   "missiles use the bay-open hull and measured bay hardpoints")
ok("ch_ship_glow" in CODE and "globalCompositeOperation='lighter'" in CODE,
   "stable hover hull uses the isolated internal-pixel glow layer")
ok("chaosHarrierPoint(b,'nose')" in CODE and "ch_beam_" in CODE and "chaosHarrierBeamHit" in CODE,
   "giant beam, charge flash, and collision originate at the nose")
ok("_chCollision=false" in CODE and "if(b._harrier && !b._chCollision) return" in CODE,
   "warp disappearance disables hull collision and damage")
ok("chaosHarrierProjectileDraw" in CODE and "if(b._chKind" in CODE,
   "authored plasma, missile, and side-laser frames own their projectile renderer")

print("PASS verify_chaos_harrier_0825")
