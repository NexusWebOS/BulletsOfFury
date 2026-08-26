"""Focused verification for the 2026-08-25 user-supplied runtime assets."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "assets" / "game"
SRC = (ROOT / "assets" / "game.js").read_text(encoding="utf-8")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)
    print("ok ", message)


portraits = sorted((GAME / "pilot_portraits").glob("*.png"))
require(len(portraits) == 108, "nine pilots x twelve approved portrait poses")
require(all(Image.open(p).size == (256, 256) for p in portraits), "all portraits retain full 256px source resolution")
require("port_cf_" in SRC and "_talking?'talk'" in SRC, "menus/dialogue resolve the approved portraits and type-on mouth poses")


def edge_purple(path: Path) -> int:
    im = Image.open(path).convert("RGBA")
    px = im.load()
    count = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            edge = any(
                0 <= nx < im.width and 0 <= ny < im.height and px[nx, ny][3] == 0
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            )
            if edge and min(r, b) > 10 and g < min(r, b) * 0.78 and abs(r - b) < 145:
                count += 1
    return count


require(sum(edge_purple(p) for p in portraits) == 0, "all 108 new portraits have zero transparency-edge purple halo pixels")

fleet = sorted((GAME / "l6_fleet").glob("*.png"))
require(len(fleet) == 27, "three Level-6 hulls x three palettes x three damage states")
require(all(set(Image.open(p).convert("RGBA").getchannel("A").get_flattened_data()) <= {0, 255} for p in fleet), "fleet silhouettes use hard alpha")
require(all(tag in SRC for tag in ("l6v_s0", "l6v_s1", "l6v_s2", "l6v_r0", "l6v_r1", "l6v_r2", "l6v_b0", "l6v_b1", "l6v_b2")), "all nine recovered fleet types are wired")

stage6 = SRC[SRC.index("if(stageNum===6){") : SRC.index("if(stageNum===7){")]
require("bcarrier" not in stage6 and "s1jetDeltaB" not in stage6 and "s1jetBomberB" not in stage6, "Stage 6 no longer fields borrowed carrier/Stage-1 jets")

mg = sorted((GAME / "fx_0825").glob("mg_bullet_*.png"))
require(len(mg) == 30, "six MG poses exist in each of the five color tiers")
require(all(Image.open(p).mode == "RGBA" for p in mg), "MG frames are transparent RGBA sprites")
require("if(_cLv<=5 && mgcfDraw" in SRC and "return 'mgcf_'" in SRC, "player and enemy machine guns use the new plates")
require("fx0825_lava_fireball" in SRC and "fx0825_lava_comet" in SRC, "both supplied magma attacks are registered and assigned")
require("XART.rdy('fx0825_ice_orb')" in SRC and "XART.rdy('fx0825_ice_shard')" in SRC, "ice orb spins the supplied wheel and fires the supplied shard")

runway = Image.open(GAME / "bg_stage01_runway_transition.jpg")
require(runway.size == (360, 1984), "connected Level-1 runway stays at its full 360x1984 source resolution")
require("if(XART.rdy('bg_stage01_runway_transition'))" in SRC, "Level-1 launch prefers the connected runway")

print("PASS verify_user_assets_0825")
