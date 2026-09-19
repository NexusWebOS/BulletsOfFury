"""Build authored pickup turn strips, Furnace directional strips, and the shield HUD plate.

Runtime code only chooses a finished frame.  It never rotates these sprites on the canvas.
"""
from pathlib import Path
from PIL import Image, ImageFilter
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/game/rotation_frames_0918"
OUT.mkdir(parents=True, exist_ok=True)


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def coin_strip(src: Path, dst: str, frames: int = 12, cell: int = 192) -> None:
    im = rgba(src)
    box = im.getbbox()
    if box:
        im = im.crop(box)
    limit = int(cell * .78)
    scale = min(limit / max(1, im.width), limit / max(1, im.height), 1.0)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.Resampling.LANCZOS)
    strip = Image.new("RGBA", (cell * frames, cell))
    for i in range(frames):
        a = i / frames * math.tau
        # An authored cabinet-style Y turn: narrow edge frames and mirrored far face.
        face = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if math.cos(a) < 0 else im
        w = max(5, round(face.width * (0.13 + .87 * abs(math.cos(a)))))
        h = max(5, round(face.height * (0.96 + .04 * abs(math.cos(a)))))
        frame = face.resize((w, h), Image.Resampling.LANCZOS)
        x = i * cell + (cell - w) // 2
        y = (cell - h) // 2 + round(math.sin(a) * 3)
        strip.alpha_composite(frame, (x, y))
    strip.save(OUT / dst, optimize=True)


def directional_strip(src: Path, dst: str, pivot: tuple[int, int], frames: int = 16, cell: int = 256) -> None:
    im = rgba(src)
    strip = Image.new("RGBA", (cell * frames, cell))
    for i in range(frames):
        ang = i * 360 / frames
        stage = Image.new("RGBA", (cell, cell))
        stage.alpha_composite(im, (cell // 2 - pivot[0], cell // 2 - pivot[1]))
        # PIL positive rotation is counter-clockwise, matching the canvas angle convention visually.
        frame = stage.rotate(-ang, resample=Image.Resampling.BICUBIC, center=(cell // 2, cell // 2))
        strip.alpha_composite(frame, (i * cell, 0))
    strip.save(OUT / dst, optimize=True)


PICKUPS = {
    "life_up_turn.png": "assets/game/ui/pickups_0915/life_up_wings.png",
    "continue_up_turn.png": "assets/game/ui/pickups_0915/continue_up.png",
    "space_helper_turn.png": "assets/game/ui/space_armory_0915/helper_orb_icon.png",
    "space_akimbo_turn.png": "assets/game/ui/space_armory_0915/akimbo_icon.png",
    "space_mine_turn.png": "assets/game/ui/space_armory_0915/proximity_mine_icon.png",
    "fury_bomb_turn.png": "assets/game/ui/pickups_0917b/fury_bomb.png",
    "timed_bomb_turn.png": "assets/game/ui/pickups_0917b/timed_bomb.png",
}
for value in (100, 250, 500, 1000):
    PICKUPS[f"score_{value}_turn.png"] = f"assets/game/ui/pickups_0917b/score_{value}.png"
for elem in ("fire", "ice", "lightning", "prism", "toxic", "kinetic", "chrome", "water", "dark"):
    PICKUPS[f"inf_{elem}_turn.png"] = f"assets/game/ui/infusion_0917/inf_{elem}.png"
for out_name, rel in PICKUPS.items():
    coin_strip(ROOT / rel, out_name)

FURNACE = ROOT / "assets/game/bosses/furnace"
for name in (
    "arm_flame_intact", "arm_flame_damaged", "arm_flame_exposed",
    "arm_cannon_intact", "arm_cannon_damaged", "arm_cannon_exposed",
):
    directional_strip(FURNACE / f"fzt_{name}.png", f"fzt_{name}_turn.png", (64, 40))
for name in ("body_intact", "body_damaged", "body_exposed", "body_wreck", "body_rotor", "body_rotor_damaged"):
    src = rgba(FURNACE / f"fzt_{name}.png")
    directional_strip(FURNACE / f"fzt_{name}.png", f"fzt_{name}_turn.png", (src.width // 2, src.height // 2), cell=384)


def shield_plate() -> None:
    """Key the generated concept and fit it to a compact transparent HUD sprite."""
    src = Path(r"C:\Users\Mike\.codex\generated_images\01a092a0-0744-71b1-8d8d-c95ab7f90646\exec-4c7a9742-9c5c-456f-a9b6-9a1390c41196.png")
    im = rgba(src)
    # Dark generated backdrop becomes alpha. A soft 20px transition preserves the black metal edge.
    pix = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = pix[x, y]
            lum = max(r, g, b)
            blue_bg = b > r * 1.28 and b > g * 1.12 and lum < 105
            if lum < 15 or blue_bg:
                a = 0
            elif lum < 38:
                a = round((lum - 15) / 23 * 255)
            else:
                a = 255
            pix[x, y] = (r, g, b, a)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    im = im.resize((881, 82), Image.Resampling.LANCZOS)
    dst = ROOT / "assets/game/ui/bossbar_0918"
    dst.mkdir(parents=True, exist_ok=True)
    im.save(dst / "shield_frame_v2.png", optimize=True)


shield_plate()
print(f"wrote authored frames to {OUT}")
