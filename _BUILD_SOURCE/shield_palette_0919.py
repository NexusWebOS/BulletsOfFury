"""Pixel-exact palette variants of the authored 881x82 SHIELD HUD frame."""
from colorsys import rgb_to_hsv
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'assets/game/ui/bossbar_0918'
SOURCE = DIR / 'shield_frame_v2.png'
img = Image.open(SOURCE).convert('RGBA')
assert img.size == (881, 82)

def blue_energy(r, g, b):
    h, s, v = rgb_to_hsv(r/255, g/255, b/255)
    return (0.45 <= h <= 0.70 and s >= 0.11 and b >= r+8 and b >= g-8)

def variant(kind):
    result = Image.new('RGBA', img.size)
    pixels = []
    for r, g, b, a in img.get_flattened_data():
        if a and blue_energy(r, g, b):
            h, s, v = rgb_to_hsv(r/255, g/255, b/255)
            if kind == 'volcano':
                # Cyan white-hot trim becomes warm ivory; saturated blue becomes ember red.
                if s < 0.42 and v > 0.7:
                    r, g, b = round(255*v), round(203*v), round(174*v)
                else:
                    r, g, b = round(255*v), round((95-52*s)*v), round((75-55*s)*v)
            else:
                # Keep every source luminance step, but remove chroma for cold steel/white.
                y = round((0.16*r + 0.49*g + 0.35*b)*1.08)
                y = max(0, min(255, y))
                r = g = b = y
        pixels.append((r, g, b, a))
    result.putdata(pixels)
    assert result.getchannel('A').tobytes() == img.getchannel('A').tobytes()
    return result

variant('volcano').save(DIR / 'shield_frame_volcano_red.png')
variant('level5').save(DIR / 'shield_frame_level5_steel.png')

# Four atlas fill states, cropped at their manifest coordinates.
from PIL import Image as _Image
_atlas=_Image.open('assets/game/atlas/ui_bossbar.png').convert('RGBA')
for _theme,_tag in [('volcano','volcano_red'),('level5','level5_steel')]:
    for _state,_y in [('over',358),('hex',373),('plasma',388),('low',403)]:
        img=_atlas.crop((2,_y,580,_y+13))
        variant(_theme).save(DIR / ('shield_fill_'+_tag+'_'+_state+'.png'))

