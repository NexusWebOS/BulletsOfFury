"""Extract the authored small toxic slug, without repainting or resampling it."""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = root / 'assets/game/combat_upgrade_0901/stage7_toxic_projectiles_atlas.png'
target = root / 'assets/game/combat_final/stage7_warden_toxic_machine_round_0920.png'
atlas = Image.open(source).convert('RGBA')
cell = atlas.crop((0, 0, 256, 256))
assert cell.getbbox() == (88, 110, 167, 146)
cell.crop((84, 106, 171, 150)).save(target)
print(target, Image.open(target).size)
