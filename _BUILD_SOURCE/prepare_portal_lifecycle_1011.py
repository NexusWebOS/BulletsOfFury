"""Make a fixed 4x8 edit canvas from Mike's approved portal plates."""
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_ART_SOURCES/portal_lifecycle_1011/reference'
OUT.mkdir(parents=True,exist_ok=True)
for name in ['blue_rift','red_rift','green_rift','black_void','gate_energy']:
    seed=Image.open(ROOT/f'assets/game/shared/fx/portals_bof_1011/{name}_00.png').convert('RGBA')
    board=Image.new('RGBA',(1280,2560))
    for i in range(32):board.paste(seed,(i%4*320,i//4*320))
    board.save(OUT/(name+'-grid.png'))
print('Five 1280x2560 reference grids, 320x320 cells.')
