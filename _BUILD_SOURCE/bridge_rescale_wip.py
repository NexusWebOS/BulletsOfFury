from PIL import Image, ImageFilter
import os

SP = r"C:\Users\Mdogg\AppData\Local\Temp\claude\C--Users-Mdogg-Desktop-BOF-CODE\f429a46f-41c1-456b-b987-467a8756afca\scratchpad"
SRC = 'assets/game/jungle800_rc2_master.png'
im = Image.open(SRC).convert('RGB')
W, H = im.size

BAND_T, BAND_B = 2290, 2880
SCALE = 0.65
bh = BAND_B - BAND_T
band = im.crop((0, BAND_T, W, BAND_B))
bp = band.load()

# ---- 1. mask the STONE, not the rectangle -------------------------------
# The structure is grey: low saturation. The dirt road is tan - saturation ~40-70 - and the
# canopy is green, so a tight saturation gate separates them. Dark tower interiors are caught
# by the low-luminance clause. Closing then fills the windows and gate slots.
m = Image.new('L', (W, bh), 0)
mp = m.load()
for y in range(bh):
    for x in range(W):
        r, g, b = bp[x, y]
        mx, mn = max(r, g, b), min(r, g, b)
        sat = mx - mn
        lum = (r + g + b) / 3
        if (sat < 30 and 45 < lum < 205) or (sat < 46 and lum <= 45):
            mp[x, y] = 255
m = m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(7))   # close holes
m = m.filter(ImageFilter.GaussianBlur(1.6))

# ---- 2. heal the band: jungle where the structure was -------------------
# copy from clean canopy at the SAME x so the composition and any stream keep their place
heal = im.crop((0, 2960, W, 2960 + bh))
healed = Image.composite(heal, band, m)

# ---- 3. the structure alone, scaled -------------------------------------
struct = band.copy()
struct.putalpha(m)
sw, sh = int(W * SCALE), int(bh * SCALE)
small = struct.resize((sw, sh), Image.LANCZOS)
ox, oy = (W - sw) // 2, (bh - sh) // 2

out_band = healed.convert('RGBA')
out_band.alpha_composite(small, (ox, oy))
out_band = out_band.convert('RGB')

out = im.copy()
out.paste(out_band, (0, BAND_T))
out.save(os.path.join(SP, 'master_rescaled.png'))

prev = Image.new('RGB', (W * 3 + 40, bh + 20), (18, 18, 24))
prev.paste(band, (10, 10))
prev.paste(m.convert('RGB'), (W + 20, 10))
prev.paste(out_band, (W * 2 + 30, 10))
prev.save(os.path.join(SP, 'bridge_before_after.png'))
print('original | stone mask | result')
