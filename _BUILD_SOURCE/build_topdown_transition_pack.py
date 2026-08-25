from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "game" / "cinematic_level_transitions_topdown"
APPROACHES = ROOT / "assets" / "game" / "cinematic_level_approaches"
PREVIEWS = OUT / "previews"
SIZE = (1672, 941)
FONT = Path(r"C:\Windows\Fonts\bahnschrift.ttf")

STAGES = (
    (1, "RUMBLE IN THE JUNGLE", "stage01_rumble_in_the_jungle_topdown.png", "stage01_rumble_in_the_jungle_approach.png", "river islands, stone causeway and dam threshold", False),
    (2, "IT'S HOT IN HERE", "stage02_its_hot_in_here_topdown.png", "stage02_its_hot_in_here_approach.png", "armored desert road through a volcanic combat zone", False),
    (3, "ICE STILL CAN'T SEE", "stage03_ice_still_cant_see_topdown.png", "stage03_ice_still_cant_see_approach.png", "ice-shelf route into a frozen research cavern", False),
    (4, "CROUCHING MISSILES, HIDDEN DEATH", "stage04_crouching_missiles_hidden_death_topdown.png", "stage04_crouching_missiles_hidden_death_approach.png", "coastal checkpoint highway leading to an airbase threshold", False),
    (5, "ALL FOR ONE, NONE FOR ALL", "stage05_all_for_one_none_for_all_topdown.png", "stage05_all_for_one_none_for_all_approach.png", "orbital launch causeway and circular transit gate", False),
    (6, "HEAVY TURBULENCE", "stage06_heavy_turbulence_topdown.png", "stage06_heavy_turbulence_approach.png", "weather deck and daylight-to-supercell cloud route", False),
    (7, "NOT ANOTHER SEWER LEVEL", "stage07_not_another_sewer_level_topdown.png", "stage07_not_another_sewer_level_approach.png", "toxic sewer canal, maintenance causeway and intake", False),
    (8, "FURIOUS DEATH", "stage08_furious_death_topdown.png", "stage08_furious_death_approach.png", "obsidian route across necrotic geology to a gravity abyss", False),
    (9, "THE VELOCITY VOID", "stage09_the_velocity_void_bonus_topdown.png", "stage09_the_velocity_void_bonus_approach.png", "violet-cyan transit-gate corridor", True),
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
    canvas = Image.new("RGB", (tile[0] * 3, (tile[1] + label_h) * 3), (4, 6, 10))
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(str(FONT), 15)
    stage_font = ImageFont.truetype(str(FONT), 16)
    for index, entry in enumerate(entries):
        with Image.open(ROOT / entry["file"]) as source:
            preview = source.convert("RGB").resize(tile, Image.Resampling.LANCZOS)
        x = index % 3 * tile[0]
        y = index // 3 * (tile[1] + label_h)
        canvas.paste(preview, (x, y))
        draw.text((x + 8, y + tile[1] + 4), f"STAGE {entry['stage']}", font=stage_font, fill=(104, 218, 255))
        draw.text((x + 92, y + tile[1] + 5), entry["title"], font=title_font, fill=(232, 238, 244))
        draw.text((x + 8, y + tile[1] + 27), "TOP-DOWN / BOTTOM TO TOP", font=stage_font, fill=(134, 148, 164))
        if entry["bonus"]:
            draw.text((x + 333, y + tile[1] + 27), "BONUS", font=stage_font, fill=(203, 115, 255))
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    path = PREVIEWS / "topdown_transitions_contact.jpg"
    canvas.save(path, quality=93, optimize=True)
    return path


def main() -> None:
    entries = []
    for stage, title, filename, reference_name, route, bonus in STAGES:
        path = OUT / filename
        reference = APPROACHES / reference_name
        if not path.is_file():
            raise FileNotFoundError(path)
        if not reference.is_file():
            raise FileNotFoundError(reference)
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
                "source_reference": reference.relative_to(ROOT).as_posix(),
                "size": list(SIZE),
                "camera": "true top-down near-orthographic 85-90 degrees",
                "flow": "bottom_to_top",
                "route_visual": route,
                "baked_entities": [],
                "environment_only": True,
                "overlay_intent": "interactive cinematic transition staging",
                "sha256": sha256(path),
            }
        )

    zones = {
        "canvas": list(SIZE),
        "coordinate_system": "top-left pixel coordinates [x, y, width, height]",
        "flow": "bottom_to_top",
        "shared_recommended_zones": {
            "entry_bottom": [520, 700, 632, 220],
            "travel_center": [550, 60, 572, 821],
            "left_interaction": [70, 260, 430, 430],
            "right_interaction": [1172, 260, 430, 430],
            "exit_top": [520, 0, 632, 190],
        },
        "notes": [
            "Zones are placement suggestions, not collision bounds.",
            "Travel is composed for bottom entry and top exit; individual scenes may support additional side staging.",
            "All PNGs contain environment only. Add every ship, aircraft, pilot, enemy, projectile, explosion and interactive object at runtime.",
        ],
    }

    contact = make_contact(entries)
    manifest = {
        "pack": "Bullets of Fury top-down interactive cinematic transitions",
        "native_size": list(SIZE),
        "stage_count": len(entries),
        "campaign_stages": 8,
        "bonus_stages": 1,
        "camera": "true top-down / near-orthographic / 85-90 degrees / no horizon",
        "flow": "bottom_to_top",
        "global_constraints": {
            "environment_only": True,
            "no_baked_ships_or_aircraft": True,
            "no_baked_vehicles": True,
            "no_baked_enemies_or_creatures": True,
            "no_baked_characters": True,
            "no_baked_projectiles_or_explosions": True,
            "no_baked_text_logos_or_ui": True,
        },
        "stages": entries,
        "interaction_zones": "assets/game/cinematic_level_transitions_topdown/interaction_zones.json",
        "preview": contact.relative_to(ROOT).as_posix(),
        "generation": {
            "mode": "built-in ImageGen reference workflow",
            "prompt_record": "assets/game/cinematic_level_transitions_topdown/GENERATION_PROMPTS.md",
        },
    }
    (OUT / "interaction_zones.json").write_text(json.dumps(zones, indent=2) + "\n", encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: packaged {len(entries)} top-down transition plates at {SIZE[0]}x{SIZE[1]} RGB.")


if __name__ == "__main__":
    main()
