from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
HQ_DIR = ROOT / "assets" / "game" / "cinematic_backgrounds" / "fury_hq"

SCENES = (
    ("01_launch_bay_runway.png", "Launch Bay / Runway", "wide team staging; aircraft launch"),
    ("02_command_deck_nine.png", "Command Deck", "nine stations; full-team command scene"),
    ("03_briefing_classroom.png", "Briefing Classroom", "left podium; Cole instructor staging"),
    ("04_strategic_war_room.png", "Strategic War Room", "holographic table; threat briefing"),
    ("05_armory_gear_bay.png", "Armory / Gear Bay", "gear-up scenes; open center aisle"),
    ("06_medical_decon_wing.png", "Medical / Decon", "treatment, recovery, containment"),
    ("07_engineering_reactor.png", "Engineering / Reactor", "technical crisis; power-core scenes"),
    ("08_squad_ready_room.png", "Squad Ready Room", "character dialogue; downtime scenes"),
    ("09_observation_deck.png", "Observation Deck", "quiet dialogue; storm/runway vista"),
)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    font = ImageFont.load_default()
    tile_width, image_height, label_height = 512, 288, 42
    canvas = Image.new("RGB", (tile_width * 3, (image_height + label_height) * 3), (5, 7, 11))
    draw = ImageDraw.Draw(canvas)
    manifest_scenes: list[dict] = []

    for index, (filename, title, staging) in enumerate(SCENES):
        path = HQ_DIR / filename
        image = Image.open(path).convert("RGB")
        native_size = image.size
        preview = image.resize((tile_width, image_height), Image.Resampling.LANCZOS)
        x = (index % 3) * tile_width
        y = (index // 3) * (image_height + label_height)
        canvas.paste(preview, (x, y))
        draw.rectangle((x, y + image_height, x + tile_width, y + image_height + label_height), fill=(8, 11, 17))
        draw.text((x + 10, y + image_height + 8), title, fill=(226, 234, 242), font=font)
        draw.text((x + 10, y + image_height + 23), staging, fill=(112, 184, 135), font=font)
        manifest_scenes.append(
            {
                "id": path.stem,
                "title": title,
                "file": path.relative_to(ROOT).as_posix(),
                "native_size": list(native_size),
                "resampled": False,
                "staging": staging,
                "sha256": file_hash(path),
            }
        )

    contact_sheet = HQ_DIR / "fury_hq_contact_sheet.jpg"
    canvas.save(contact_sheet, quality=92, optimize=True)

    manifest = {
        "collection": "FURY HQ cinematic backgrounds",
        "scene_count": len(SCENES),
        "master_policy": "Native generated masters are preserved at 1672x941; only the contact sheet is resized.",
        "style": "Neo-Geo / late-1990s arcade military science-fiction pixel-art cinematic plates",
        "character_policy": "Environment plates intentionally contain no characters for later compositing.",
        "contact_sheet": contact_sheet.relative_to(ROOT).as_posix(),
        "scenes": manifest_scenes,
    }
    (HQ_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Cataloged {len(SCENES)} native-size HQ backgrounds")


if __name__ == "__main__":
    main()
