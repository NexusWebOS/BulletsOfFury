"""Prepare independently pivoted 0925 enemy art; keep the generated source plates."""
from pathlib import Path
from shutil import copyfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path.home() / ".codex/generated_images/01a0d568-40a4-7b70-97c0-acc501f39d5b"
OUT = ROOT / "assets/game/enemy_overhaul_0925"
(OUT / "source").mkdir(parents=True, exist_ok=True)
(OUT / "sprites").mkdir(parents=True, exist_ok=True)

def source(uid, name):
    path = next(SRC.glob(f"*{uid}.png"))
    copyfile(path, OUT / "source" / f"{name}_source.png")
    return Image.open(path).convert("RGBA")

def standalone(uid, name):
    im = source(uid, name)
    box = im.getchannel("A").getbbox()
    im = im.crop(box)
    im.thumbnail((240, 240), Image.Resampling.LANCZOS)
    frame = Image.new("RGBA", (256, 256))
    frame.alpha_composite(im, ((256-im.width)//2, (256-im.height)//2))
    frame.save(OUT / "sprites" / f"{name}.png")

standalone("c3fad846-99ec-46d3-9a7e-68ec156bf40d", "stage3_ice_drone_01")
standalone("5dab0448-9cf5-4026-8e96-5154776480c3", "stage4_war_drone_01")

drone_sheet = source("059b6259-8d57-426a-884f-3ee88574aa1a", "cross_stage_drone_sheet")
for i, name in enumerate(("stage2_fire_jet_02", "stage5_space_drone_01",
                          "stage6_storm_drone_01", "stage8_alien_drone_01")):
    x, y = i % 2, i // 2
    piece = drone_sheet.crop((round(x*drone_sheet.width/2), round(y*drone_sheet.height/2),
                              round((x+1)*drone_sheet.width/2), round((y+1)*drone_sheet.height/2)))
    piece = piece.crop(piece.getchannel("A").getbbox())
    piece.thumbnail((240, 240), Image.Resampling.NEAREST)
    frame = Image.new("RGBA", (256, 256))
    frame.alpha_composite(piece, ((256-piece.width)//2, (256-piece.height)//2))
    frame.save(OUT / "sprites" / f"{name}.png")

# Each generated tank sheet is an authored pair: hull on the left, turret on
# the right. Both pieces share one turret-ring pivot after extraction, so the
# source muzzle distance survives rotation without guessed overlays.
for stage, uid in [
    (1, "46e9cbc4-e4a5-479e-8062-eda10bbdc717"),
    (4, "1ab39ae2-6e10-43c9-b418-d6d880c30c7f"),
    (7, "99e392c7-9fa1-4557-bb75-48466901276b"),
]:
    im = source(uid, f"stage{stage}_modular_tank")
    split = im.width // 2
    hull_pivot = (565 if stage != 7 else 560, 385)
    turret_pivot = (1370 if stage != 7 else 1372, 385)
    for part, crop, pivot in (
        ("hull", (0, 0, split, im.height), hull_pivot),
        ("turret", (split, 0, im.width, im.height), turret_pivot),
    ):
        piece = im.crop(crop)
        # Artwork has approximately 560px tread width. A 0.43 sample keeps
        # each contour crisp while fitting the long barrels in a 384px tile.
        piece = piece.resize((round(piece.width * .43), round(piece.height * .43)), Image.Resampling.NEAREST)
        frame = Image.new("RGBA", (384, 384))
        px = 192 - round((pivot[0] - crop[0]) * .43)
        py = 192 - round((pivot[1] - crop[1]) * .43)
        frame.alpha_composite(piece, (px, py))
        frame.save(OUT / "sprites" / f"stage{stage}_tank_{part}.png")

# The toxic core and exhaust were generated as distinct animation sheets.
# Preserve the sheets, and slice cells so the engine can advance by key.
for uid, name, cols, rows in [
    ("a7a0fc48-10ea-4ac7-8000-afaca0e0e68c", "stage7_toxic_core", 4, 2),
    ("8afc4bae-a05f-4e87-8c46-4c6e010b6912", "stage7_toxic_exhaust", 3, 2),
]:
    im = source(uid, name)
    for i in range(cols * rows):
        col, row = i % cols, i // cols
        x0, x1 = round(col*im.width/cols), round((col+1)*im.width/cols)
        y0, y1 = round(row*im.height/rows), round((row+1)*im.height/rows)
        cell = im.crop((x0, y0, x1, y1))
        cell.thumbnail((120, 120), Image.Resampling.NEAREST)
        frame = Image.new("RGBA", (128, 128))
        frame.alpha_composite(cell, ((128-cell.width)//2, (128-cell.height)//2))
        frame.save(OUT / "sprites" / f"{name}_{i}.png")

# Stage-4 jet families share exact hull sockets. Keep every turret as an
# independent pixel plate so aiming and launch effects can follow its pivot.
jet_sheet = source("0ab61164-565d-4711-8044-5489f2b08acd", "stage4_modular_jet_hulls")
for col, name in enumerate(("desert", "black", "snow")):
    x0, x1 = round(col*jet_sheet.width/3), round((col+1)*jet_sheet.width/3)
    piece = jet_sheet.crop((x0, 0, x1, jet_sheet.height))
    piece = piece.crop(piece.getchannel("A").getbbox())
    piece.thumbnail((248, 248), Image.Resampling.NEAREST)
    frame = Image.new("RGBA", (256, 256))
    frame.alpha_composite(piece, ((256-piece.width)//2, (256-piece.height)//2))
    frame.save(OUT / "sprites" / f"stage4_jet_{name}_hull.png")

module_sheet = source("02b54997-164d-43a1-a28e-df3d8f59689b", "stage4_jet_weapon_modules")
for col, name in enumerate(("missile", "laser"), start=1):
    x0, x1 = round(col*module_sheet.width/3), round((col+1)*module_sheet.width/3)
    piece = module_sheet.crop((x0, 0, x1, module_sheet.height//2))
    piece = piece.crop(piece.getchannel("A").getbbox())
    piece.thumbnail((116, 116), Image.Resampling.NEAREST)
    frame = Image.new("RGBA", (128, 128))
    frame.alpha_composite(piece, ((128-piece.width)//2, (128-piece.height)//2))
    frame.save(OUT / "sprites" / f"stage4_jet_{name}_module.png")

mg_sheet = source("61fc23a7-f84c-4882-ad63-3b1438c76e14", "stage4_jet_rotary_module")
mg_cells = [mg_sheet.crop((round(i*mg_sheet.width/4), 0,
                           round((i+1)*mg_sheet.width/4), mg_sheet.height)) for i in range(4)]
for i, piece in enumerate(mg_cells):
    piece = piece.crop(piece.getchannel("A").getbbox())
    piece.thumbnail((116, 116), Image.Resampling.NEAREST)
    frame = Image.new("RGBA", (128, 128))
    frame.alpha_composite(piece, ((128-piece.width)//2, (128-piece.height)//2))
    frame.save(OUT / "sprites" / f"stage4_jet_rotary_module_{i}.png")

flash_sheet = source("ae6d0128-e5bb-40ea-8ea3-93aed7faca28", "weapon_muzzle_sheet")
for col, family in enumerate(("rotary", "missile", "laser", "toxic")):
    for row in range(4):
        x0, x1 = round(col*flash_sheet.width/4), round((col+1)*flash_sheet.width/4)
        y0, y1 = round(row*flash_sheet.height/4), round((row+1)*flash_sheet.height/4)
        piece = flash_sheet.crop((x0, y0, x1, y1))
        piece.thumbnail((128, 128), Image.Resampling.NEAREST)
        frame = Image.new("RGBA", (128, 128))
        frame.alpha_composite(piece, ((128-piece.width)//2, (128-piece.height)//2))
        frame.save(OUT / "sprites" / f"weapon_muzzle_{family}_{row}.png")

base_sheet = source("c8b6bf3b-eb68-440f-a40e-96891a562603", "modular_ground_bases")
for col, (stage, name) in enumerate(((1,"jungle"),(2,"volcano"),(3,"ice"),(4,"desert"),
                                     (6,"city"),(7,"toxic"),(8,"alien"))):
    x, y = col % 4, col // 4
    box = (round(x*base_sheet.width/4), round(y*base_sheet.height/2),
           round((x+1)*base_sheet.width/4), round((y+1)*base_sheet.height/2))
    piece = base_sheet.crop(box)
    piece = piece.crop(piece.getchannel("A").getbbox())
    piece.thumbnail((240, 240), Image.Resampling.NEAREST)
    frame = Image.new("RGBA", (256, 256))
    frame.alpha_composite(piece, ((256-piece.width)//2, (256-piece.height)//2))
    frame.save(OUT / "sprites" / f"ground_base_stage{stage}_{name}.png")

head_sheet = source("b0a11cef-36d6-4b24-bc87-0cca46fe270d", "modular_ground_heads")
for col, name in enumerate(("mg", "missile", "laser", "sonic")):
    piece = head_sheet.crop((round(col*head_sheet.width/4), 0,
                             round((col+1)*head_sheet.width/4), head_sheet.height))
    piece = piece.crop(piece.getchannel("A").getbbox())
    piece.thumbnail((240, 240), Image.Resampling.NEAREST)
    frame = Image.new("RGBA", (256, 256))
    frame.alpha_composite(piece, ((256-piece.width)//2, (256-piece.height)//2))
    frame.save(OUT / "sprites" / f"ground_head_{name}.png")

print("Prepared modular tank and toxic animation sprites under", OUT)
