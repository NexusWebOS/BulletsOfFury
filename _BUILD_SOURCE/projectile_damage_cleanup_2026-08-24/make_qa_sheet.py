from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent
SOURCE = BASE / "candidates" / "damage_effects"
OUTPUT = BASE / "previews" / "damage_effects" / "qa-selected-eight-frame-sheet.png"
KEYS = [
    "nef_s1_jungle_tank_damaged_idle",
    "nef_s1_jungle_tank_critical_idle",
    "nef_s2_lava_crawler_critical_idle",
    "nef_s2_tracked_flame_turret_critical_idle",
    "nef_s3_snow_tank_critical_idle",
    "nef_s3_cryo_barge_critical_idle",
    "mbg2_torso_critical",
    "mbl5_hull_critical",
    "mbc6_command-core_critical",
]
FONT = ImageFont.load_default()


def checker(size):
    image = Image.new("RGBA", size, (7, 13, 23, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], 8):
        for x in range(0, size[0], 8):
            color = (17, 30, 48, 255) if (x // 8 + y // 8) % 2 else (9, 20, 34, 255)
            draw.rectangle((x, y, x + 7, y + 7), fill=color)
    return image


rows = []
for key in KEYS:
    frames = [Image.open(path).convert("RGBA") for path in sorted((SOURCE / key).glob("*.png"))]
    if not frames:
        continue
    tile_w, tile_h = 220, 270
    row = Image.new("RGBA", (tile_w * len(frames), tile_h + 26), (5, 9, 16, 255))
    ImageDraw.Draw(row).text((5, 6), key, fill=(230, 240, 255, 255), font=FONT)
    for index, frame in enumerate(frames):
        scale = min((tile_w - 8) / frame.width, (tile_h - 8) / frame.height, 3.0)
        shown = frame.resize((max(1, round(frame.width * scale)), max(1, round(frame.height * scale))), Image.Resampling.NEAREST)
        tile = checker((tile_w, tile_h))
        tile.alpha_composite(shown, ((tile_w - shown.width) // 2, (tile_h - shown.height) // 2))
        ImageDraw.Draw(tile).text((4, 4), str(index + 1), fill=(255, 214, 92, 255), font=FONT)
        row.alpha_composite(tile, (index * tile_w, 26))
    rows.append(row)

sheet = Image.new("RGBA", (max(row.width for row in rows), sum(row.height + 8 for row in rows)), (3, 7, 13, 255))
y = 0
for row in rows:
    sheet.alpha_composite(row, (0, y))
    y += row.height + 8
sheet.save(OUTPUT)
print(OUTPUT)
