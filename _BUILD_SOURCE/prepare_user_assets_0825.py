"""Prepare the approved 2026-08-25 portrait-adjacent runtime art.

This is deliberately deterministic pixel work: remove the old magenta matte, preserve hard
pixel edges, build the two requested Level-6 palettes, and split the supplied MG tracer strip
into six actual projectile frames.  No runtime colour overlay is used for the aircraft.
"""
from __future__ import annotations

import colorsys
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
L6_SRC = ROOT / "_ART_SOURCES" / "l6enemies_0825"
USR_SRC = ROOT / "_ART_SOURCES" / "user_assets_0825"
OUT = ROOT / "assets" / "game"
L6_OUT = OUT / "l6_fleet"
FX_OUT = OUT / "fx_0825"
PREVIEW = ROOT / "_BUILD_SOURCE" / "previews_0825"


def neutralize_portrait_halos() -> tuple[int, int]:
    """Turn only transparency-adjacent purple spill into the project's dark neutral edge."""
    portrait_dir = OUT / "pilot_portraits"
    changed = 0
    files = 0
    for path in sorted(portrait_dir.glob("*.png")):
        im = Image.open(path).convert("RGBA")
        px = im.load()
        w, h = im.size
        near = {(x, y) for y in range(h) for x in range(w) if px[x, y][3] == 0}
        for _ in range(4):
            near |= {
                (nx, ny)
                for x, y in tuple(near)
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                if 0 <= nx < w and 0 <= ny < h
            }
        local = 0
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if not a:
                    if r or g or b:
                        px[x, y] = (0, 0, 0, 0)
                    continue
                if (x, y) not in near:
                    continue
                lo = min(r, b)
                if lo > 10 and g < lo * 0.78 and abs(r - b) < 145:
                    # Keep the silhouette solid; remove the purple cast, not the edge pixel.
                    v = min(24, round((r + g + b) / 12))
                    px[x, y] = (v, v, v, a)
                    local += 1
        if local:
            im.save(path, optimize=True)
            files += 1
            changed += local
    return files, changed


def build_bmf_maps() -> Path:
    """Embed BMF metrics so dialogue fonts also work when the game is launched from file://."""
    fonts = OUT / "fonts"
    maps = {}
    for name, folder in (("dialogue", "fury-dialogue-font"), ("cutscene", "fury-cutscene-font")):
        src = fonts / folder / f"{folder}-map.json"
        maps[name] = json.loads(src.read_text(encoding="utf-8"))
    dst = fonts / "bmf_maps.js"
    dst.write_text("window.BOF_BMF_MAPS=" + json.dumps(maps, separators=(",", ":")) + ";\n", encoding="utf-8")
    return dst


def dehalo_magenta(im: Image.Image, passes: int = 4) -> Image.Image:
    """Remove opaque magenta matte remnants adjacent to transparency.

    Sources already contain hard alpha but were flattened against hot magenta before alpha was
    restored.  Only connected edge pixels with both red and blue dominating green are removed;
    blue glass, red lamps, and yellow insignia remain untouched.
    """
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    # Hidden RGB in transparent pixels is normalized so later resampling cannot resurrect pink.
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                px[x, y] = (0, 0, 0, 0)

    for _ in range(passes):
        remove: list[tuple[int, int]] = []
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if not a:
                    continue
                edge = False
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
                        edge = True
                        break
                if not edge:
                    continue
                lo = min(r, b)
                # Strong and dark purple contamination, including the nearly-black fringe.
                if lo > 10 and g < lo * 0.72 and abs(r - b) < 145:
                    remove.append((x, y))
        if not remove:
            break
        for x, y in remove:
            px[x, y] = (0, 0, 0, 0)
    return im


def recolor_metal(im: Image.Image, mode: str) -> Image.Image:
    """Palette-swap neutral steel while retaining damage, lamps, glass, and baked shading."""
    out = im.copy().convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            # Hull metal is near-neutral. Keep saturated cockpit glass, warning lamps, fire/smoke.
            if s > 0.32 or v < 0.055:
                continue
            if mode == "royal":
                nr, ng, nb = colorsys.hsv_to_rgb(220 / 360, 0.72, min(1.0, v * 1.03))
            elif mode == "blackice":
                # Gunmetal low/mid tones with ice-blue plates and highlights.
                sat = 0.66 if v < 0.68 else 0.44
                val = (0.025 + v * 0.34) if v < 0.68 else (0.02 + v * 0.86)
                nr, ng, nb = colorsys.hsv_to_rgb(202 / 360, sat, min(1.0, val))
            else:
                raise ValueError(mode)
            px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
    return out


def hue_projectile(im: Image.Image, color: str) -> Image.Image:
    """Apply a five-colour projectile palette while preserving luminance and hot-white cores."""
    cr, cg, cb = (int(color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    th, ts, _ = colorsys.rgb_to_hsv(cr, cg, cb)
    out = im.copy().convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if ts < 0.08:  # white tier
                nr = ng = nb = min(1.0, 0.22 + v * 0.92)
            elif v > 0.93 and s < 0.28:  # retain a white-hot center
                nr = ng = nb = 1.0
            else:
                nr, ng, nb = colorsys.hsv_to_rgb(th, max(ts, 0.74), v)
            px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
    return out


def build_l6_fleet() -> list[Path]:
    L6_OUT.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []
    state_name = {"intact": "intact", "dama": "dama", "crit": "crit"}
    for src in sorted(L6_SRC.glob("nvy[0-2]_*.png")):
        stem = src.stem
        hull = stem[3]
        state = next(k for k in state_name if f"_{k}_" in stem)
        clean = dehalo_magenta(Image.open(src))
        for pal, plate in (
            ("steel", clean),
            ("royal", recolor_metal(clean, "royal")),
            ("blackice", recolor_metal(clean, "blackice")),
        ):
            dst = L6_OUT / f"n6v{hull}_{pal}_{state_name[state]}_c.png"
            plate.save(dst, optimize=True)
            made.append(dst)
    return made


def build_fx() -> list[Path]:
    FX_OUT.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []
    for source, name in (
        ("mfx_bpow_0_0.png", "lava_comet.png"),
        ("fireball_projectile_f01_96.png", "lava_fireball.png"),
        ("ice_shard.png", "ice_shard.png"),
        ("iceorb_0.png", "ice_orb.png"),
    ):
        dst = FX_OUT / name
        plate = dehalo_magenta(Image.open(USR_SRC / source))
        # Runtime projectile art is authored nose-down. The supplied comet points right.
        if name == "lava_comet.png":
            plate = plate.transpose(Image.Transpose.ROTATE_270)
        plate.save(dst, optimize=True)
        made.append(dst)

    # The supplied plate is six vertically stacked projectile poses, not one 97px-long bullet.
    mg = Image.open(USR_SRC / "boss_machinegun_bullets.png").convert("RGBA")
    raw = mg.load()
    for y in range(mg.height):
        for x in range(mg.width):
            r, g, b, _ = raw[x, y]
            raw[x, y] = (0, 0, 0, 0) if (r > 155 and b > 155 and g < 115) else (r, g, b, 255)
    bands = [(11, 27), (26, 40), (39, 52), (51, 64), (63, 78), (77, 92)]
    colors = {1: "#ff9c25", 2: "#3a8aff", 3: "#5fe07a", 4: "#eff7ff", 5: "#ff4a48"}
    for lv, color in colors.items():
        for fi, (y0, y1) in enumerate(bands):
            fr = mg.crop((0, y0, mg.width, y1))
            box = fr.getbbox()
            if box:
                fr = fr.crop(box)
            canvas = Image.new("RGBA", (16, 20))
            canvas.alpha_composite(fr, ((16 - fr.width) // 2, (20 - fr.height) // 2))
            dst = FX_OUT / f"mg_bullet_{lv}_{fi}.png"
            hue_projectile(canvas, color).save(dst, optimize=True)
            made.append(dst)

    runway = Image.open(USR_SRC / "runway.jpg").convert("RGB")
    runway.save(OUT / "bg_stage01_runway_transition.jpg", quality=94, subsampling=0)
    made.append(OUT / "bg_stage01_runway_transition.jpg")
    return made


def make_preview() -> Path:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    bg = (8, 13, 25, 255)
    sheet = Image.new("RGBA", (1050, 1120), bg)
    draw = ImageDraw.Draw(sheet)
    x0 = 20
    for row, pal in enumerate(("steel", "royal", "blackice")):
        draw.text((x0, 12 + row * 285), pal.upper(), fill=(230, 240, 255, 255))
        x = x0
        for hull in range(3):
            im = Image.open(L6_OUT / f"n6v{hull}_{pal}_intact_c.png").convert("RGBA")
            scale = min(300 / im.width, 235 / im.height)
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.NEAREST)
            sheet.alpha_composite(im, (x + (315 - im.width) // 2, 38 + row * 285))
            x += 335
    draw.text((20, 875), "MG FIVE-COLOR / LAVA / ICE", fill=(230, 240, 255, 255))
    for lv in range(1, 6):
        im = Image.open(FX_OUT / f"mg_bullet_{lv}_3.png").resize((64, 80), Image.Resampling.NEAREST)
        sheet.alpha_composite(im, (25 + (lv - 1) * 90, 910))
    for i, name in enumerate(("lava_comet.png", "lava_fireball.png", "ice_shard.png", "ice_orb.png")):
        im = Image.open(FX_OUT / name).convert("RGBA")
        scale = min(150 / im.width, 150 / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.NEAREST)
        sheet.alpha_composite(im, (500 + i * 130 + (120 - im.width) // 2, 900 + (170 - im.height) // 2))
    dst = PREVIEW / "fleet_fx_contact.png"
    sheet.save(dst)
    return dst


if __name__ == "__main__":
    portrait_files, portrait_pixels = neutralize_portrait_halos()
    bmf = build_bmf_maps()
    fleet = build_l6_fleet()
    fx = build_fx()
    preview = make_preview()
    print(f"portraits={portrait_files}/{portrait_pixels}px bmf={bmf.relative_to(ROOT)} fleet={len(fleet)} fx={len(fx)} preview={preview.relative_to(ROOT)}")
