from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "_BUILD_SOURCE" / "cinematic_campaign_inputs"
OUT = ROOT / "assets" / "game" / "cinematic_campaign"
BRANDING = OUT / "branding"
EXTERIORS = OUT / "exteriors"
OFFICIAL_BRANDING = OUT / "branding_generated_official"
OFFICIAL_EXTERIORS = OUT / "exteriors_generated_official"
SEATED = OUT / "seated_poses"
LOUNGE = OUT / "cutscenes" / "lounge_and_alliances"
PILOTS = OUT / "cutscenes" / "pilots"
PREVIEWS = OUT / "previews"

FONT_DISPLAY = Path(r"C:\Windows\Fonts\bahnschrift.ttf")
FONT_HEAVY = Path(r"C:\Windows\Fonts\impact.ttf")
CANVAS_SIZE = (1672, 941)

CHARACTERS = (
    "axel",
    "freezer",
    "falva",
    "lizzie",
    "yuri",
    "maverick",
    "juggernaut",
    "decker",
    "cole",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def crop_alpha(image: Image.Image, padding: int = 24) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("Empty alpha image")
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(image.width, bbox[2] + padding)
    bottom = min(image.height, bbox[3] + padding)
    return image.crop((left, top, right, bottom))


def connected_matte_cutout(source: Path) -> Image.Image:
    image = Image.open(source).convert("RGB")
    rgb = np.asarray(image, dtype=np.uint8)
    luma = rgb.mean(axis=2)
    chroma = rgb.max(axis=2).astype(np.int16) - rgb.min(axis=2).astype(np.int16)
    corner_luma = float(luma[0, 0])

    if corner_luma > 128:
        candidate = (luma >= 216) & (chroma <= 20)
    else:
        candidate = (luma <= 48) & (chroma <= 34)

    mask = Image.fromarray(np.where(candidate, 255, 0).astype(np.uint8), "L").copy()
    ImageDraw.floodfill(mask, (0, 0), 128, thresh=0)
    background = np.asarray(mask) == 128
    alpha = np.where(background, 0, 255).astype(np.uint8)
    rgba = np.dstack((rgb, alpha))
    rgba[alpha == 0, :3] = 0
    return crop_alpha(Image.fromarray(rgba, "RGBA"), 32)


def clean_generated_crest(source: Path) -> Image.Image:
    image = Image.open(source).convert("RGBA")
    data = np.asarray(image, dtype=np.uint8).copy()
    # Remove the generator's soft atmospheric alpha; preserve a crisp arcade mark.
    keep = data[:, :, 3] >= 72
    data[:, :, 3] = np.where(keep, 255, 0).astype(np.uint8)
    data[~keep, :3] = 0
    return crop_alpha(Image.fromarray(data, "RGBA"), 32)


def fit_font(text: str, path: Path, max_width: int, start_size: int) -> ImageFont.FreeTypeFont:
    size = start_size
    while size > 12:
        font = ImageFont.truetype(str(path), size)
        box = font.getbbox(text)
        if box[2] - box[0] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(str(path), 12)


def resize_contain(image: Image.Image, width: int, height: int) -> Image.Image:
    scale = min(width / image.width, height / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def metal_gradient(width: int, height: int) -> Image.Image:
    y = np.linspace(0, 1, height, dtype=np.float32)[:, None, None]
    top = np.array([17, 27, 38], dtype=np.float32)[None, None, :]
    bottom = np.array([4, 8, 13], dtype=np.float32)[None, None, :]
    rgb = top * (1 - y) + bottom * y
    rgb = np.repeat(rgb, width, axis=1)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")


def build_branding(crest: Image.Image) -> dict:
    BRANDING.mkdir(parents=True, exist_ok=True)
    crest_path = BRANDING / "fury_hq_earth_division_crest_rgba.png"
    crest.save(crest_path, optimize=True)

    banner = metal_gradient(2048, 512)
    draw = ImageDraw.Draw(banner)
    draw.rectangle((8, 8, 2039, 503), outline=(2, 5, 8, 255), width=16)
    draw.rectangle((28, 28, 2019, 483), outline=(84, 112, 125, 255), width=5)
    draw.rectangle((40, 40, 2007, 471), outline=(82, 225, 40, 255), width=3)
    draw.line((48, 443, 2000, 443), fill=(19, 129, 255, 255), width=4)

    crest_small = resize_contain(crest, 430, 430)
    banner.alpha_composite(crest_small, (55 + (430 - crest_small.width) // 2, 40 + (430 - crest_small.height) // 2))

    font_main = fit_font("FURY HQ", FONT_HEAVY, 1450, 210)
    font_sub = fit_font("EARTH DIVISION", FONT_DISPLAY, 1450, 108)
    draw.text((505, 58), "FURY HQ", font=font_main, fill=(224, 236, 244), stroke_width=7, stroke_fill=(0, 7, 12))
    draw.text((515, 300), "EARTH DIVISION", font=font_sub, fill=(105, 239, 55), stroke_width=4, stroke_fill=(0, 8, 15))
    draw.line((510, 286, 1960, 286), fill=(29, 151, 255), width=5)
    horizontal_path = BRANDING / "fury_hq_earth_division_banner_horizontal.png"
    banner.convert("RGB").save(horizontal_path, optimize=True)

    wordmark = Image.new("RGBA", (2048, 512), (0, 0, 0, 0))
    crest_word = resize_contain(crest, 460, 460)
    wordmark.alpha_composite(crest_word, (10, (512 - crest_word.height) // 2))
    wdraw = ImageDraw.Draw(wordmark)
    wdraw.text((480, 66), "FURY HQ", font=font_main, fill=(232, 241, 247), stroke_width=8, stroke_fill=(0, 8, 14))
    wdraw.text((490, 306), "EARTH DIVISION", font=font_sub, fill=(107, 242, 57), stroke_width=5, stroke_fill=(0, 8, 14))
    wordmark_path = BRANDING / "fury_hq_earth_division_wordmark_rgba.png"
    wordmark.save(wordmark_path, optimize=True)

    vertical = metal_gradient(768, 1536)
    vdraw = ImageDraw.Draw(vertical)
    vdraw.polygon(((0, 0), (768, 0), (768, 1435), (384, 1535), (0, 1435)), fill=(8, 13, 20), outline=(82, 225, 40))
    vdraw.rectangle((28, 28, 739, 1390), outline=(34, 151, 244), width=5)
    crest_vertical = resize_contain(crest, 650, 650)
    vertical.alpha_composite(crest_vertical, ((768 - crest_vertical.width) // 2, 110))
    v_main = fit_font("FURY HQ", FONT_HEAVY, 650, 145)
    v_sub = fit_font("EARTH DIVISION", FONT_DISPLAY, 650, 72)
    main_box = vdraw.textbbox((0, 0), "FURY HQ", font=v_main, stroke_width=5)
    sub_box = vdraw.textbbox((0, 0), "EARTH DIVISION", font=v_sub, stroke_width=3)
    vdraw.text(((768 - (main_box[2] - main_box[0])) // 2, 820), "FURY HQ", font=v_main, fill=(232, 241, 247), stroke_width=5, stroke_fill=(0, 6, 12))
    vdraw.text(((768 - (sub_box[2] - sub_box[0])) // 2, 1000), "EARTH DIVISION", font=v_sub, fill=(105, 239, 55), stroke_width=3, stroke_fill=(0, 6, 12))
    vdraw.line((110, 1125, 658, 1125), fill=(34, 151, 244), width=5)
    vertical_path = BRANDING / "fury_hq_earth_division_banner_vertical.png"
    vertical.convert("RGB").save(vertical_path, optimize=True)

    return {
        "crest": crest_path.relative_to(ROOT).as_posix(),
        "wordmark": wordmark_path.relative_to(ROOT).as_posix(),
        "horizontal_banner": horizontal_path.relative_to(ROOT).as_posix(),
        "vertical_banner": vertical_path.relative_to(ROOT).as_posix(),
    }


def paste_with_shadow(base: Image.Image, overlay: Image.Image, xy: tuple[int, int], blur: int = 10, opacity: int = 170) -> None:
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    alpha = overlay.getchannel("A").point(lambda value: value * opacity // 255)
    black = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    black.putalpha(alpha)
    shadow.alpha_composite(black, (xy[0] + 8, xy[1] + 10))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(shadow)
    base.alpha_composite(overlay, xy)


def mount_exterior_banner(background: Image.Image, banner: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    canvas = background.convert("RGBA")
    width, height = box[2] - box[0], box[3] - box[1]
    sign = banner.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
    sign = ImageEnhance.Brightness(sign).enhance(0.82)
    paste_with_shadow(canvas, sign, (box[0], box[1]), blur=7, opacity=210)
    draw = ImageDraw.Draw(canvas)
    for x in (box[0] + 8, box[2] - 9):
        for y in (box[1] + 8, box[3] - 9):
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(166, 184, 190), outline=(8, 13, 18))
    return canvas.convert("RGB")


def build_exteriors(banner_path: Path) -> dict:
    EXTERIORS.mkdir(parents=True, exist_ok=True)
    banner = Image.open(banner_path).convert("RGBA")
    specs = {
        "01_fury_hq_island_aerial_banner.png": ("exterior_aerial_rgb.png", (980, 205, 1420, 315)),
        "02_fury_hq_beach_approach_banner.png": ("exterior_beach_rgb.png", (940, 155, 1465, 287)),
        "03_fury_hq_jungle_gate_banner.png": ("exterior_jungle_gate_rgb.png", (720, 215, 1155, 324)),
    }
    result = {}
    for filename, (source_name, box) in specs.items():
        background = Image.open(INPUTS / source_name).convert("RGB")
        output = mount_exterior_banner(background, banner, box)
        path = EXTERIORS / filename
        output.save(path, optimize=True)
        result[path.stem] = {
            "file": path.relative_to(ROOT).as_posix(),
            "size": list(path_image_size(path)),
            "banner_text": "FURY HQ — EARTH DIVISION",
            "sha256": sha256(path),
        }
    return result


def load_official_generated_branding() -> dict:
    """Return the approved fully generated identity assets without retyping them."""
    assets = {
        "master_insignia": OFFICIAL_BRANDING / "fury_hq_earth_division_master_generated.png",
        "horizontal_banner": OFFICIAL_BRANDING / "fury_hq_earth_division_horizontal_generated.png",
        "vertical_banner": OFFICIAL_BRANDING / "fury_hq_earth_division_vertical_generated.png",
    }
    for path in assets.values():
        if not path.is_file():
            raise FileNotFoundError(f"Missing official generated branding asset: {path}")
    return {key: path.relative_to(ROOT).as_posix() for key, path in assets.items()}


def load_official_generated_exteriors() -> dict:
    """Return the ImageGen-edited exterior plates with branding built into the architecture."""
    specs = {
        "01_fury_hq_island_aerial_banner": OFFICIAL_EXTERIORS / "01_fury_hq_island_aerial_official_generated.png",
        "02_fury_hq_beach_approach_banner": OFFICIAL_EXTERIORS / "02_fury_hq_beach_approach_official_generated.png",
        "03_fury_hq_jungle_gate_banner": OFFICIAL_EXTERIORS / "03_fury_hq_jungle_gate_official_generated.png",
    }
    result = {}
    for key, path in specs.items():
        if not path.is_file():
            raise FileNotFoundError(f"Missing official generated exterior: {path}")
        result[key] = {
            "file": path.relative_to(ROOT).as_posix(),
            "size": list(path_image_size(path)),
            "banner_text": "FURY HQ — EARTH DIVISION",
            "branding_method": "fully generated in-scene architectural insignia",
            "sha256": sha256(path),
        }
    return result


def path_image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def build_seated_poses() -> tuple[dict, dict[str, Image.Image]]:
    SEATED.mkdir(parents=True, exist_ok=True)
    entries = {}
    images: dict[str, Image.Image] = {}
    for name in CHARACTERS:
        cutout = connected_matte_cutout(INPUTS / f"{name}_seated_rgb.png")
        path = SEATED / f"{name}_seated_rgba.png"
        cutout.save(path, optimize=True)
        images[name] = cutout
        entries[name] = {
            "file": path.relative_to(ROOT).as_posix(),
            "native_size": list(cutout.size),
            "corner_alpha": [
                cutout.getpixel((0, 0))[3],
                cutout.getpixel((cutout.width - 1, 0))[3],
                cutout.getpixel((0, cutout.height - 1))[3],
                cutout.getpixel((cutout.width - 1, cutout.height - 1))[3],
            ],
            "sha256": sha256(path),
        }
    return entries, images


def place_character(canvas: Image.Image, character: Image.Image, center_x: int, baseline: int, height: int, shadow: bool = True) -> tuple[int, int, int, int]:
    scale = height / character.height
    size = (max(1, round(character.width * scale)), height)
    sprite = character.resize(size, Image.Resampling.LANCZOS)
    x = round(center_x - sprite.width / 2)
    y = baseline - sprite.height
    if shadow:
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        draw.ellipse((x + sprite.width * 0.18, baseline - 18, x + sprite.width * 0.82, baseline + 15), fill=(0, 0, 0, 145))
        canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(9)))
    canvas.alpha_composite(sprite, (x, y))
    return (x, y, x + sprite.width, y + sprite.height)


def add_title(canvas: Image.Image, title: str, subtitle: str) -> None:
    panel = Image.new("RGBA", (canvas.width, 116), (1, 5, 10, 210))
    panel_draw = ImageDraw.Draw(panel)
    panel_draw.line((0, 0, canvas.width, 0), fill=(78, 229, 43, 230), width=3)
    panel_draw.line((0, 5, canvas.width, 5), fill=(28, 137, 239, 190), width=2)
    title_font = fit_font(title, FONT_HEAVY, 980, 60)
    sub_font = fit_font(subtitle, FONT_DISPLAY, 980, 30)
    panel_draw.text((42, 15), title, font=title_font, fill=(232, 240, 247), stroke_width=3, stroke_fill=(0, 6, 10))
    panel_draw.text((44, 76), subtitle, font=sub_font, fill=(112, 232, 68))
    panel_draw.text((canvas.width - 420, 44), "FURY HQ — EARTH DIVISION", font=ImageFont.truetype(str(FONT_DISPLAY), 25), fill=(135, 176, 203))
    canvas.alpha_composite(panel, (0, canvas.height - panel.height))


def lounge_scene(background: Image.Image, seated: dict[str, Image.Image], placements: list[tuple[str, int, int, int]], title: str, subtitle: str) -> Image.Image:
    canvas = background.convert("RGBA")
    # Farther seats first; lower baselines naturally draw in front.
    for name, center_x, baseline, height in sorted(placements, key=lambda item: item[2]):
        place_character(canvas, seated[name], center_x, baseline, height)
    add_title(canvas, title, subtitle)
    return canvas.convert("RGB")


def build_lounge_scenes(seated: dict[str, Image.Image], crest: Image.Image) -> dict:
    LOUNGE.mkdir(parents=True, exist_ok=True)
    lounge = Image.open(ROOT / "assets/game/cinematic_backgrounds/fury_hq/08_squad_ready_room.png").convert("RGB")
    specs = {
        "01_brotherhood_axel_freezer_lounge.png": (
            [("axel", 655, 875, 540), ("freezer", 1040, 875, 545)],
            "BROTHERHOOD OF FLIGHT",
            "Axel commands. Freezer never leaves his wing.",
        ),
        "02_princesses_falva_lizzie_lounge.png": (
            [("falva", 665, 875, 525), ("lizzie", 1040, 875, 535)],
            "PRINCESSES OF THE SKY",
            "Falva and Lizzie — sisters in blood and altitude.",
        ),
        "03_lone_wolves_yuri_maverick_lounge.png": (
            [("yuri", 675, 875, 525), ("maverick", 1040, 875, 535)],
            "TWO LONE WOLVES",
            "A lost cadet and a mercenary find unexpected camaraderie.",
        ),
        "04_command_table_cole_decker_juggernaut.png": (
            [("cole", 470, 870, 485), ("decker", 820, 870, 485), ("juggernaut", 1190, 885, 520)],
            "COMMAND, CODE & CHAOS",
            "Cole manages the division. Decker builds it. Juggernaut keeps it alive.",
        ),
        "05_juggernaut_storytime.png": (
            [("falva", 370, 830, 360), ("lizzie", 560, 830, 365), ("juggernaut", 850, 890, 560), ("yuri", 1160, 835, 360), ("maverick", 1370, 835, 365)],
            "THE LOUDEST MAN IN THE ROOM",
            "Everybody gets along with Juggernaut — eventually at full volume.",
        ),
        "06_full_earth_division_lounge.png": (
            [
                ("axel", 350, 735, 315), ("freezer", 585, 735, 315), ("cole", 820, 735, 310), ("decker", 1050, 735, 315),
                ("falva", 250, 885, 325), ("lizzie", 520, 885, 330), ("juggernaut", 835, 900, 375), ("yuri", 1170, 885, 325), ("maverick", 1450, 885, 330),
            ],
            "FURY HQ — EARTH DIVISION",
            "Nine pilots. One headquarters. The campaign begins here.",
        ),
    }

    result = {}
    for filename, (placements, title, subtitle) in specs.items():
        image = lounge_scene(lounge, seated, placements, title, subtitle)
        path = LOUNGE / filename
        image.save(path, optimize=True)
        result[path.stem] = {"file": path.relative_to(ROOT).as_posix(), "size": list(image.size), "title": title, "subtitle": subtitle}

    # Separate restricted-access story beat for Cole and Decker.
    lab = Image.open(INPUTS / "secret_prototype_lab_rgb.png").convert("RGBA")
    decker = Image.open(ROOT / "assets/game/cinematic_characters/decker/poses/01_front_neutral.png").convert("RGBA")
    cole = Image.open(ROOT / "assets/game/cinematic_characters/cole/poses/01_front_neutral.png").convert("RGBA")
    place_character(lab, decker, 350, 885, 650)
    place_character(lab, cole, 1330, 885, 660)
    add_title(lab, "RESTRICTED PROTOTYPES", "Decker built the lasers and photon cannon. Cole alone holds access.")
    restricted_path = LOUNGE / "07_cole_decker_restricted_prototype_lab.png"
    lab.convert("RGB").save(restricted_path, optimize=True)
    result[restricted_path.stem] = {
        "file": restricted_path.relative_to(ROOT).as_posix(),
        "size": list(lab.size),
        "title": "RESTRICTED PROTOTYPES",
        "subtitle": "Decker built the lasers and photon cannon. Cole alone holds access.",
    }
    return result


def build_pilot_scenes(exterior_entries: dict) -> dict:
    PILOTS.mkdir(parents=True, exist_ok=True)
    bg = {
        "launch": ROOT / "assets/game/cinematic_backgrounds/fury_hq/01_launch_bay_runway.png",
        "command": ROOT / "assets/game/cinematic_backgrounds/fury_hq/02_command_deck_nine.png",
        "briefing": ROOT / "assets/game/cinematic_backgrounds/fury_hq/03_briefing_classroom.png",
        "armory": ROOT / "assets/game/cinematic_backgrounds/fury_hq/05_armory_gear_bay.png",
        "ready": ROOT / "assets/game/cinematic_backgrounds/fury_hq/08_squad_ready_room.png",
        "observation": ROOT / "assets/game/cinematic_backgrounds/fury_hq/09_observation_deck.png",
        "lab": INPUTS / "secret_prototype_lab_rgb.png",
        "jungle": ROOT / exterior_entries["03_fury_hq_jungle_gate_banner"]["file"],
        "beach": ROOT / exterior_entries["02_fury_hq_beach_approach_banner"]["file"],
    }

    specs = {
        "axel": ("02_front_left_3q.png", "launch", 440, 886, 680, "AIR COMMANDER", "Brotherhood forged in flight."),
        "freezer": ("03_front_right_3q.png", "launch", 1240, 886, 690, "RIGHT HAND", "The commander's wingman never breaks formation."),
        "falva": ("02_front_left_3q.png", "observation", 450, 886, 660, "PRINCESS OF THE SKY", "Falva reads the horizon before anyone else."),
        "lizzie": ("02_front_left_3q.png", "briefing", 1225, 886, 665, "ELDER PRINCESS", "The eldest sister always takes point."),
        "yuri": ("02_front_left_3q.png", "jungle", 440, 886, 660, "LOST CADET", "He joined seeking answers — and found a division."),
        "maverick": ("02_front_left_3q.png", "beach", 1240, 886, 680, "MERCENARY", "A lone contract becomes a cause."),
        "juggernaut": ("02_front_left_3q.png", "ready", 1120, 886, 700, "HEAVY ASSAULT", "The loudest laugh and biggest heart in FURY HQ."),
        "decker": ("01_front_neutral.png", "lab", 390, 886, 700, "SYSTEMS ARCHITECT", "Code, circuits and weapons nobody else is cleared to see."),
        "cole": ("01_front_neutral.png", "command", 490, 886, 700, "COMMANDING OFFICER", "Earth Division answers to one command."),
    }

    result = {}
    for index, name in enumerate(CHARACTERS, start=1):
        pose_file, bg_key, x, baseline, height, role, tagline = specs[name]
        canvas = Image.open(bg[bg_key]).convert("RGBA")
        character = Image.open(ROOT / f"assets/game/cinematic_characters/{name}/poses/{pose_file}").convert("RGBA")
        place_character(canvas, character, x, baseline, height)
        add_title(canvas, name.upper(), f"{role}  •  {tagline}")
        filename = f"{index:02d}_{name}_campaign_intro.png"
        path = PILOTS / filename
        canvas.convert("RGB").save(path, optimize=True)
        result[name] = {
            "file": path.relative_to(ROOT).as_posix(),
            "role": role,
            "tagline": tagline,
            "background": bg_key,
            "size": list(canvas.size),
        }
    return result


def contact_sheet(items: list[tuple[str, Path]], destination: Path, columns: int = 3, tile: tuple[int, int] = (500, 281)) -> None:
    rows = (len(items) + columns - 1) // columns
    label_h = 36
    canvas = Image.new("RGB", (columns * tile[0], rows * (tile[1] + label_h)), (4, 6, 10))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(FONT_DISPLAY), 20)
    for index, (label, path) in enumerate(items):
        image = Image.open(path).convert("RGB").resize(tile, Image.Resampling.LANCZOS)
        x = (index % columns) * tile[0]
        y = (index // columns) * (tile[1] + label_h)
        canvas.paste(image, (x, y))
        draw.text((x + 8, y + tile[1] + 6), label, font=font, fill=(220, 231, 239))
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, quality=91, optimize=True)


def contained_contact_sheet(
    items: list[tuple[str, Path]],
    destination: Path,
    columns: int = 3,
    tile: tuple[int, int] = (500, 400),
) -> None:
    rows = (len(items) + columns - 1) // columns
    label_h = 42
    canvas = Image.new("RGB", (columns * tile[0], rows * (tile[1] + label_h)), (4, 6, 10))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(FONT_DISPLAY), 20)
    for index, (label, path) in enumerate(items):
        source = Image.open(path).convert("RGBA")
        image = resize_contain(source, tile[0] - 24, tile[1] - 24)
        x = (index % columns) * tile[0]
        y = (index // columns) * (tile[1] + label_h)
        card = Image.new("RGBA", tile, (8, 11, 16, 255))
        card.alpha_composite(image, ((tile[0] - image.width) // 2, (tile[1] - image.height) // 2))
        canvas.paste(card.convert("RGB"), (x, y))
        draw.text((x + 8, y + tile[1] + 8), label, font=font, fill=(220, 231, 239))
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, quality=92, optimize=True)


def seated_qa_sheet(seated: dict[str, Image.Image], destination: Path) -> None:
    tile_w, tile_h = 380, 420
    colors = ((8, 12, 18), (82, 8, 13), (7, 38, 82), (5, 67, 31))
    canvas = Image.new("RGB", (tile_w * 3, tile_h * 3), (3, 5, 8))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(FONT_DISPLAY), 24)
    for index, name in enumerate(CHARACTERS):
        sprite = resize_contain(seated[name], 330, 350)
        x = (index % 3) * tile_w
        y = (index // 3) * tile_h
        draw.rectangle((x, y, x + tile_w, y + tile_h), fill=colors[index % len(colors)])
        canvas.paste(sprite, (x + (tile_w - sprite.width) // 2, y + 14), sprite)
        draw.text((x + 14, y + 380), name.upper(), font=font, fill=(230, 237, 243))
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, quality=93, optimize=True)


def main() -> None:
    branding = load_official_generated_branding()
    exteriors = load_official_generated_exteriors()
    official_insignia = Image.open(ROOT / branding["master_insignia"]).convert("RGBA")
    seated_entries, seated_images = build_seated_poses()
    lounge_entries = build_lounge_scenes(seated_images, official_insignia)
    pilot_entries = build_pilot_scenes(exteriors)

    branding_sheet = PREVIEWS / "fury_hq_official_generated_branding_contact.jpg"
    contained_contact_sheet(
        [(key, ROOT / value) for key, value in branding.items()],
        branding_sheet,
    )
    exterior_sheet = PREVIEWS / "fury_hq_exteriors_contact.jpg"
    contact_sheet([(key, ROOT / value["file"]) for key, value in exteriors.items()], exterior_sheet)
    seated_sheet = PREVIEWS / "seated_pose_edge_qa.jpg"
    seated_qa_sheet(seated_images, seated_sheet)
    campaign_sheet = PREVIEWS / "campaign_cutscenes_contact.jpg"
    campaign_items = [(key, ROOT / value["file"]) for key, value in lounge_entries.items()]
    campaign_items.extend((name, ROOT / value["file"]) for name, value in pilot_entries.items())
    contact_sheet(campaign_items, campaign_sheet)

    narrative = {
        "division": "FURY HQ — Earth Division",
        "alliances": {
            "brotherhood_of_flight": ["axel", "freezer"],
            "princesses_of_the_sky": ["falva", "lizzie"],
            "lone_wolf_camaraderie": ["yuri", "maverick"],
            "restricted_command_technology": ["cole", "decker"],
            "team_heart": ["juggernaut", "everyone"],
        },
        "command": {"commanding_officer": "cole", "air_commander": "axel", "right_hand": "freezer"},
        "secrets": {
            "builder": "decker",
            "authorized_user": "cole",
            "systems": ["prototype lasers", "photon cannon"],
        },
    }

    manifest = {
        "pack": "FURY HQ — Earth Division campaign cinematics",
        "native_cutscene_size": list(CANVAS_SIZE),
        "branding": branding,
        "exteriors": exteriors,
        "seated_poses": seated_entries,
        "lounge_and_alliance_cutscenes": lounge_entries,
        "pilot_campaign_cutscenes": pilot_entries,
        "narrative": narrative,
        "previews": {
            "official_branding": branding_sheet.relative_to(ROOT).as_posix(),
            "exteriors": exterior_sheet.relative_to(ROOT).as_posix(),
            "seated_edge_qa": seated_sheet.relative_to(ROOT).as_posix(),
            "campaign": campaign_sheet.relative_to(ROOT).as_posix(),
        },
        "generation": {
            "mode": "built-in ImageGen reference mode for official branding and exterior signage; deterministic Pillow compositing for character staging",
            "identity_policy": "seated poses generated from the approved six-pose character masters",
            "text_policy": "official FURY HQ and EARTH DIVISION lettering is generated as an integrated physical part of every approved insignia and exterior sign",
            "prompt_record": "assets/game/cinematic_campaign/GENERATION_PROMPTS.md",
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "branding_assets": len(branding),
        "exteriors": len(exteriors),
        "seated_poses": len(seated_entries),
        "lounge_alliance_cutscenes": len(lounge_entries),
        "pilot_cutscenes": len(pilot_entries),
    }, indent=2))


if __name__ == "__main__":
    main()
