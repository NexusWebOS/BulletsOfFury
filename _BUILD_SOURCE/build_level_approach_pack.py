from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "game" / "cinematic_level_approaches"
PREVIEWS = OUT / "previews"
SIZE = (1672, 941)
FONT = Path(r"C:\Windows\Fonts\bahnschrift.ttf")

STAGES = (
    (1, "RUMBLE IN THE JUNGLE", "stage01_rumble_in_the_jungle_approach.png", "tropical coast, river causeway and distant dam", False),
    (2, "IT'S HOT IN HERE", "stage02_its_hot_in_here_approach.png", "desert observation apron leading into a volcanic caldera", False),
    (3, "ICE STILL CAN'T SEE", "stage03_ice_still_cant_see_approach.png", "polar research terrace leading toward a glacial canyon", False),
    (4, "CROUCHING MISSILES, HIDDEN DEATH", "stage04_crouching_missiles_hidden_death_approach.png", "empty coastal highway and open-airbase approach", False),
    (5, "ALL FOR ONE, NONE FOR ALL", "stage05_all_for_one_none_for_all_approach.png", "unoccupied orbital deck facing Earth and the asteroid route", False),
    (6, "HEAVY TURBULENCE", "stage06_heavy_turbulence_approach.png", "weather platform facing a day-to-night supercell corridor", False),
    (7, "NOT ANOTHER SEWER LEVEL", "stage07_not_another_sewer_level_approach.png", "dry maintenance platform overlooking the toxic sewer intake", False),
    (8, "FURIOUS DEATH", "stage08_furious_death_approach.png", "empty observation dais facing the necrotic deep-space frontier", False),
    (9, "THE VELOCITY VOID", "stage09_the_velocity_void_bonus_approach.png", "deserted bonus gate platform and nine-ring velocity corridor", True),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_contact(entries: list[dict]) -> Path:
    tile = (520, 293)
    label_h = 50
    columns = 3
    rows = 3
    canvas = Image.new("RGB", (tile[0] * columns, (tile[1] + label_h) * rows), (4, 6, 10))
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(str(FONT), 19)
    stage_font = ImageFont.truetype(str(FONT), 16)
    for index, entry in enumerate(entries):
        source = Image.open(ROOT / entry["file"]).convert("RGB")
        preview = source.resize(tile, Image.Resampling.LANCZOS)
        x = index % columns * tile[0]
        y = index // columns * (tile[1] + label_h)
        canvas.paste(preview, (x, y))
        draw.text((x + 8, y + tile[1] + 4), f"STAGE {entry['stage']}", font=stage_font, fill=(104, 218, 255))
        draw.text((x + 100, y + tile[1] + 4), entry["title"], font=title_font, fill=(232, 238, 244))
        if entry["bonus"]:
            draw.text((x + 8, y + tile[1] + 27), "BONUS ROUTE", font=stage_font, fill=(203, 115, 255))
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    path = PREVIEWS / "level_approaches_contact.jpg"
    canvas.save(path, quality=93, optimize=True)
    return path


def main() -> None:
    entries = []
    for stage, title, filename, route, bonus in STAGES:
        path = OUT / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        with Image.open(path) as image:
            if image.size != SIZE:
                raise ValueError(f"{path.name}: expected {SIZE}, got {image.size}")
            if image.mode != "RGB":
                raise ValueError(f"{path.name}: expected RGB, got {image.mode}")
            image.verify()
        entries.append(
            {
                "stage": stage,
                "title": title,
                "bonus": bonus,
                "file": path.relative_to(ROOT).as_posix(),
                "size": list(SIZE),
                "route_visual": route,
                "baked_entities": [],
                "environment_only": True,
                "overlay_intent": "interactive cinematic staging",
                "sha256": sha256(path),
            }
        )

    zones = {
        "canvas": list(SIZE),
        "coordinate_system": "top-left pixel coordinates [x, y, width, height]",
        "shared_recommended_zones": {
            "foreground_full_cast": [64, 635, 1544, 266],
            "left_actor": [80, 430, 430, 455],
            "center_actor": [621, 430, 430, 455],
            "right_actor": [1162, 430, 430, 455],
            "dialogue_lower_third": [64, 740, 1544, 150],
        },
        "notes": [
            "Zones are placement suggestions, not collision bounds.",
            "Stage 5 and Stage 6 intentionally preserve large open upper regions for runtime aircraft or spacecraft overlays.",
            "All supplied PNGs contain environment only; add every actor, vehicle, enemy, effect and interactive prop at runtime.",
        ],
    }

    contact = make_contact(entries)
    manifest = {
        "pack": "Bullets of Fury interactive cinematic level approaches",
        "native_size": list(SIZE),
        "stage_count": len(entries),
        "campaign_stages": 8,
        "bonus_stages": 1,
        "global_constraints": {
            "environment_only": True,
            "no_baked_ships": True,
            "no_baked_enemies": True,
            "no_baked_characters": True,
            "no_baked_projectiles": True,
            "no_baked_text_or_ui": True,
        },
        "stages": entries,
        "interaction_zones": "assets/game/cinematic_level_approaches/interaction_zones.json",
        "preview": contact.relative_to(ROOT).as_posix(),
        "generation": {
            "mode": "built-in ImageGen reference workflow",
            "prompt_record": "assets/game/cinematic_level_approaches/GENERATION_PROMPTS.md",
        },
    }
    (OUT / "interaction_zones.json").write_text(json.dumps(zones, indent=2) + "\n", encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: packaged {len(entries)} environment-only cinematic approaches at {SIZE[0]}x{SIZE[1]}.")


if __name__ == "__main__":
    main()
