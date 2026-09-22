#!/usr/bin/env python3
"""Cut the inspected SpriteCook GPT-2.5 sheets into pivot-aligned loose frames.

The raw SpriteCook PNGs live in ignored _shots and their stable asset IDs are
recorded in docs/qa/stage6_rebel_spritecook_0920.json. This script only cuts,
uniformly scales, and pads authored pixels; it does not invent poses.
"""
from pathlib import Path
from collections import deque
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "_shots"
OUT = ROOT / "assets/game/bosses/rebel_squad_0920/frames"
SIZE = 256
INK = 236

SHEETS = {
    "views": (3, 3, ["idle", "bank_l", "bank_r", "roll_l", "overhead", "roll_r",
                     "som_pitch", "som_mid", "som_recover"]),
    "som": (2, 2, ["som_0", "som_1", "som_2", "som_3"]),
    "dash": (2, 2, ["dash_0", "dash_1", "dash_2", "dash_3"]),
}


def trimmed(cell):
    # GPT sheets sometimes let the next cell's nose intrude a few pixels over a
    # grid boundary. Keep substantial connected ink, discard those fragments.
    w, h = cell.size
    mask = cell.getchannel("A").point(lambda a: 255 if a >= 16 else 0).tobytes()
    seen = bytearray(w*h)
    groups = []
    for start in range(w*h):
        if not mask[start] or seen[start]:
            continue
        group = []
        todo = deque([start]); seen[start] = 1
        while todo:
            p = todo.popleft(); group.append(p)
            x, y = p % w, p // w
            for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if 0 <= nx < w and 0 <= ny < h:
                    q = ny*w+nx
                    if mask[q] and not seen[q]:
                        seen[q] = 1; todo.append(q)
        groups.append(group)
    if not groups:
        raise ValueError("Empty SpriteCook cell")
    cutoff = max(40, round(max(map(len, groups)) * .015))
    keep = {p for group in groups if len(group) >= cutoff for p in group}
    px = cell.load()
    for y in range(h):
        for x in range(w):
            if mask[y*w+x] and y*w+x not in keep:
                px[x, y] = (0, 0, 0, 0)
    alpha = cell.getchannel("A").point(lambda a: 255 if a >= 16 else 0)
    box = alpha.getbbox()
    return cell.crop(box)


def cells(path, cols, rows):
    image = Image.open(path).convert("RGBA")
    w, h = image.size
    result = []
    for r in range(rows):
        y0, y1 = r*h//rows, (r+1)*h//rows
        if r < rows-1:
            y1 -= (y1-y0)//10  # discard next row's stray nose or flame
        for c in range(cols):
            result.append(trimmed(image.crop((c*w//cols, y0,
                                              (c+1)*w//cols, y1))))
    return result


def save_family(ship, tag, frames, names):
    # One scale per reel prevents the hull growing when its frame changes.
    extent = max(max(frame.size) for frame in frames)
    scale = INK / extent
    for frame, name in zip(frames, names):
        w, h = [max(1, round(v*scale)) for v in frame.size]
        scaled = frame.resize((w, h), Image.Resampling.NEAREST)
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        canvas.alpha_composite(scaled, ((SIZE-w)//2, (SIZE-h)//2))
        # Clear hidden RGB where alpha is zero to avoid fringe artifacts.
        px = canvas.load()
        for y in range(SIZE):
            for x in range(SIZE):
                if px[x, y][3] == 0:
                    px[x, y] = (0, 0, 0, 0)
        # Rebel bosses occupy the upper field; their noses must point toward
        # the player below. Rotate the authored view, never mirror its details.
        canvas = canvas.transpose(Image.Transpose.ROTATE_180)
        target = OUT / f"{ship}_{name}.png"
        canvas.save(target, optimize=True)
        print(target.relative_to(ROOT), f"ink={w}x{h}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for ship in ("ghost", "phantom", "ouroboros"):
        for tag, (cols, rows, names) in SHEETS.items():
            stem = f"{ship}_gpt25_attempt_raw.png" if ship == "ghost" and tag == "views" else f"{ship}_gpt25_raw.png"
            if tag in ("som", "dash"):
                stem = f"{ship}_{tag}_gpt25_raw.png"
            parts = cells(RAW / stem, cols, rows)
            save_family(ship, tag, parts, names)
        save_family(ship, "under", [trimmed(Image.open(
            RAW / f"{ship}_underside_gpt25_raw.png").convert("RGBA"))], ["belly"])


if __name__ == "__main__":
    main()
