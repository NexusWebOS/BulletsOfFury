#!/usr/bin/env python3
"""Build the Stage-8 native roster, roll reels, and crimson environment assets.

The combat pack's preview GIF is the approved source for the twelve roster hulls.
Each recovered hull gets the shipped eight-frame attack reel plus a generated
eight-frame longitudinal roll/twist reel on one fixed 256px pivot.  Stage scenery
is copied into a non-destructive crimson family so no magenta key colour or halo
survives in the live finale.
"""

from __future__ import annotations

import colorsys
from collections import Counter, deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
LEVEL8 = ROOT / "_BUILD_SOURCE" / "review_combat_packs_2026-08-24" / \
    "CF_EnemyCombatPatterns-Vol.1" / "Level-8"
PREVIEW = LEVEL8 / "Documentation" / "CF_EnemyCombatSystems-Lvl8-preview.gif"
RIFT_SOURCE = ROOT / "assets" / "game" / "stage8_furious_rift" / "source_sheet.png"

UNITS = [
    "armored_leech", "bone_interceptor", "bone_manta", "hunter_pod",
    "multi_eye_death_orb", "parasite_drone", "razor_disc", "skull_mine",
    "spawn_carrier", "symbiote_fighter", "tentacle_cannon", "void_bomber",
]


def crimsonize(image: Image.Image) -> Image.Image:
    """Move purple/magenta energy into blood-red/ember hues without changing alpha."""
    im = image.convert("RGBA")
    out = Image.new("RGBA", im.size)
    src, dst = im.load(), out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = src[x, y]
            if not a:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            # violet through hot magenta; preserve neutral steel, bone and white glints
            if s > .20 and .68 <= h <= .97:
                nh = .985 if h < .84 else .015
                nr, ng, nb = colorsys.hsv_to_rgb(nh, min(1, s * 1.06), v)
                r, g, b = round(nr * 255), round(ng * 255), round(nb * 255)
            dst[x, y] = (r, g, b, a)
    return out


def edge_clear(cell: Image.Image) -> Image.Image:
    """Remove only dark preview-board pixels connected to a cell edge."""
    rgba = cell.convert("RGBA")
    colors = Counter(rgba.getdata())
    background = {px for px, count in colors.most_common(14)
                  if count > 350 and max(px[:3]) < 95}
    w, h = rgba.size
    pix = rgba.load()
    seen: set[tuple[int, int]] = set()
    todo: deque[tuple[int, int]] = deque()
    for x in range(w):
        todo.extend(((x, 0), (x, h - 1)))
    for y in range(h):
        todo.extend(((0, y), (w - 1, y)))
    while todo:
        x, y = todo.popleft()
        if (x, y) in seen or pix[x, y] not in background:
            continue
        seen.add((x, y))
        pix[x, y] = (0, 0, 0, 0)
        if x: todo.append((x - 1, y))
        if x + 1 < w: todo.append((x + 1, y))
        if y: todo.append((x, y - 1))
        if y + 1 < h: todo.append((x, y + 1))
    return rgba


def keep_hull(cell: Image.Image) -> Image.Image:
    """Keep the main hull and nearby engine/muzzle islands; discard labels and dust."""
    w, h = cell.size
    alpha = cell.getchannel("A")
    ap = alpha.load()
    unseen = {(x, y) for y in range(h) for x in range(w) if ap[x, y]}
    comps: list[tuple[list[tuple[int, int]], tuple[int, int, int, int]]] = []
    while unseen:
        start = unseen.pop()
        pts, todo = [start], [start]
        while todo:
            x, y = todo.pop()
            for q in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if q in unseen:
                    unseen.remove(q)
                    todo.append(q)
                    pts.append(q)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        comps.append((pts, (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
    if not comps:
        return cell
    main, box = max(comps, key=lambda c: len(c[0]))
    keep = set(main)
    mx0, my0, mx1, my1 = box
    for pts, (x0, y0, x1, y1) in comps:
        if pts is main:
            continue
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        # Detached wings and exhaust islands are substantial and overlap the hull vertically.
        # Preview labels sit wholly below the hull and are made of many small components.
        if len(pts) >= 80 and mx0 - 24 <= cx <= mx1 + 24 and y0 < 178 and y0 <= my1 and y1 >= my0 - 10:
            keep.update(pts)
    out = Image.new("RGBA", cell.size)
    src, dst = cell.load(), out.load()
    for x, y in keep:
        dst[x, y] = src[x, y]
    return out


def stable_canvas(cleaned: Image.Image) -> Image.Image:
    bbox = cleaned.getbbox()
    if not bbox:
        raise RuntimeError("empty recovered Stage-8 frame")
    sprite = cleaned.crop(bbox)
    if sprite.width > 238 or sprite.height > 238:
        sprite.thumbnail((238, 238), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (256, 256))
    canvas.alpha_composite(sprite, ((256 - sprite.width) // 2, (256 - sprite.height) // 2))
    # The combat preview prints tiny white W/C/R hardpoint letters beneath a few hulls.  They
    # occasionally touch an exhaust pixel and therefore survive connected-component cleanup.
    # Remove only neutral label-colour pixels in the bottom margin; red engines and the actual
    # silhouette remain untouched.
    cp = canvas.load()
    for y in range(200, 256):
        for x in range(256):
            r, g, b, a = cp[x, y]
            if a and max(r, g, b) > 68 and max(r, g, b) - min(r, g, b) < 58:
                cp[x, y] = (0, 0, 0, 0)
    return crimsonize(canvas)


def roll_frame(seed: Image.Image, index: int) -> Image.Image:
    """Generate a readable top-down longitudinal barrel roll on a stable centre pivot."""
    bbox = seed.getbbox()
    if not bbox:
        return seed.copy()
    sprite = seed.crop(bbox)
    widths = (1.00, .78, .48, .20, .14, .44, .76, 1.00)
    angles = (0, -3, -6, -2, 2, 6, 3, 0)
    lighting = (1.00, .94, .84, .68, .76, .90, 1.06, 1.00)
    nw = max(5, round(sprite.width * widths[index]))
    twisted = sprite.resize((nw, sprite.height), Image.Resampling.NEAREST)
    twisted = ImageEnhance.Brightness(twisted).enhance(lighting[index])
    if angles[index]:
        twisted = twisted.rotate(angles[index], resample=Image.Resampling.NEAREST, expand=True)
    canvas = Image.new("RGBA", (256, 256))
    canvas.alpha_composite(twisted, ((256 - twisted.width) // 2, (256 - twisted.height) // 2))
    # A one-pixel hot rim switches sides across the edge-on midpoint and sells the twist.
    if index in (1, 2, 5, 6):
        rim = canvas.getchannel("A").filter(ImageFilter.MaxFilter(3))
        core = canvas.getchannel("A")
        rim = ImageChops.subtract(rim, core)
        edge = Image.new("RGBA", canvas.size, (255, 54, 20, 0))
        edge.putalpha(rim.point(lambda p: min(145, p)))
        canvas = Image.alpha_composite(edge, canvas)
    return canvas


def recover_roster() -> None:
    out = ROOT / "assets" / "game" / "stage8_mega_enemies"
    proof = ROOT / "_BUILD_SOURCE" / "stage8_enemy_redesign"
    out.mkdir(parents=True, exist_ok=True)
    proof.mkdir(parents=True, exist_ok=True)
    src = Image.open(PREVIEW)
    frames = []
    for i in range(src.n_frames):
        src.seek(i)
        frames.append(src.convert("RGBA"))
    contact = Image.new("RGBA", (4 * 286, 3 * 286), (7, 9, 16, 255))
    draw = ImageDraw.Draw(contact)
    roll_contact = Image.new("RGBA", (8 * 132, 12 * 132), (7, 9, 16, 255))
    for idx, name in enumerate(UNITS):
        col, row = idx % 4, idx // 4
        unit_out = out / name
        unit_out.mkdir(parents=True, exist_ok=True)
        recovered = []
        for fi, frame in enumerate(frames):
            cell = frame.crop((col * 256, row * 256, col * 256 + 256, row * 256 + 202))
            canvas = stable_canvas(keep_hull(edge_clear(cell)))
            canvas.save(unit_out / f"attack_{fi + 1:02d}.png", optimize=True)
            recovered.append(canvas)
        for fi in range(8):
            rf = roll_frame(recovered[0], fi)
            rf.save(unit_out / f"roll_{fi + 1:02d}.png", optimize=True)
            thumb = rf.copy()
            thumb.thumbnail((124, 124), Image.Resampling.NEAREST)
            roll_contact.alpha_composite(thumb, (fi * 132 + (132 - thumb.width) // 2,
                                                   idx * 132 + (132 - thumb.height) // 2))
        thumb = recovered[3].copy()
        thumb.thumbnail((232, 226), Image.Resampling.NEAREST)
        contact.alpha_composite(thumb, (col * 286 + (286 - thumb.width) // 2,
                                        row * 286 + 4 + (226 - thumb.height) // 2))
        draw.text((col * 286 + 10, row * 286 + 248), name.upper(), fill=(255, 92, 48, 255))
    contact.save(proof / "stage8_mega_roster.png")
    roll_contact.save(proof / "stage8_roll_twist_reels.png")


def clear_checker(cell: Image.Image) -> Image.Image:
    """Remove the image generator's baked neutral checker, edge-connected only."""
    rgba = cell.convert("RGBA")
    w, h = rgba.size
    pix = rgba.load()
    seen: set[tuple[int, int]] = set()
    todo: deque[tuple[int, int]] = deque()
    for x in range(w):
        todo.extend(((x, 0), (x, h - 1)))
    for y in range(h):
        todo.extend(((0, y), (w - 1, y)))
    def bg(px: tuple[int, int, int, int]) -> bool:
        r, g, b, _ = px
        return max(r, g, b) - min(r, g, b) < 24 and min(r, g, b) > 185
    while todo:
        x, y = todo.popleft()
        if (x, y) in seen or not bg(pix[x, y]):
            continue
        seen.add((x, y)); pix[x, y] = (0, 0, 0, 0)
        if x: todo.append((x - 1, y))
        if x + 1 < w: todo.append((x + 1, y))
        if y: todo.append((x, y - 1))
        if y + 1 < h: todo.append((x, y + 1))
    return rgba


def split_rift() -> None:
    out = ROOT / "assets" / "game" / "stage8_furious_rift"
    proof = ROOT / "_BUILD_SOURCE" / "stage8_enemy_redesign"
    sheet = Image.open(RIFT_SOURCE).convert("RGBA")
    contact = Image.new("RGBA", (4 * 196, 4 * 196), (7, 9, 16, 255))
    for idx in range(16):
        col, row = idx % 4, idx // 4
        x0, x1 = round(col * sheet.width / 4), round((col + 1) * sheet.width / 4)
        y0, y1 = round(row * sheet.height / 4), round((row + 1) * sheet.height / 4)
        frame = stable_canvas(clear_checker(sheet.crop((x0, y0, x1, y1))))
        frame.save(out / f"{idx + 1:02d}.png", optimize=True)
        thumb = frame.copy(); thumb.thumbnail((188, 188), Image.Resampling.NEAREST)
        contact.alpha_composite(thumb, (col * 196 + 4, row * 196 + 4))
    contact.save(proof / "stage8_furious_rift_strip.png")


def recolor_environment() -> None:
    src_root = ROOT / "assets" / "game"
    out = src_root / "stage8_environment_crimson"
    out.mkdir(parents=True, exist_ok=True)
    names = ["nst8_sky_master.png"]
    names += [f"nl8_lg_{i}.png" for i in range(6)]
    names += [f"nl8_rim_{i}.png" for i in range(6)]
    names += [f"nl8_prop_{i}.png" for i in range(12)]
    for name in names:
        crimsonize(Image.open(src_root / name)).save(out / name, optimize=True)


if __name__ == "__main__":
    recover_roster()
    split_rift()
    recolor_environment()
