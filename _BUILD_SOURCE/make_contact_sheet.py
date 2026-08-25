"""Create a small ordered contact sheet from PNGs in a capture directory."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

p = argparse.ArgumentParser()
p.add_argument("source")
p.add_argument("output")
p.add_argument("--cols", type=int, default=6)
p.add_argument("--width", type=int, default=240)
a = p.parse_args()

files = sorted(Path(a.source).glob("*.png"))
if not files:
    raise SystemExit("no PNGs")
with Image.open(files[0]) as first:
    ratio = first.height / first.width
thumb_h = int(a.width * ratio)
rows = (len(files) + a.cols - 1) // a.cols
sheet = Image.new("RGB", (a.cols * a.width, rows * (thumb_h + 18)), "#111")
draw = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    with Image.open(f) as im:
        thumb = im.convert("RGB").resize((a.width, thumb_h), Image.Resampling.LANCZOS)
    x = (i % a.cols) * a.width
    y = (i // a.cols) * (thumb_h + 18)
    sheet.paste(thumb, (x, y))
    draw.text((x + 4, y + thumb_h + 2), f.stem, fill="white")
sheet.save(a.output, quality=92)
