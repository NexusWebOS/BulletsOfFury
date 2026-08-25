from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CHROMA = ROOT / "_BUILD_SOURCE" / "cinematic_ship_chroma"
REPAIRS = ROOT / "_BUILD_SOURCE" / "cinematic_ship_repairs"
REFERENCES = ROOT / "_BUILD_SOURCE" / "cinematic_ship_inputs"
OUT = ROOT / "assets" / "game" / "cinematic_ships"
PREVIEWS = OUT / "previews"
MASTER_SIZE = (1536, 1024)
FRAME_SIZE = (512, 512)
FONT = Path(r"C:\Windows\Fonts\bahnschrift.ttf")

PILOTS = (
    ("axel", "green"),
    ("freezer", "green"),
    ("falva", "green"),
    ("lizzie", "green"),
    ("yuri", "green"),
    ("maverick", "magenta"),
    ("juggernaut", "green"),
    ("decker", "green"),
    ("cole", "magenta"),
)

VIEWS = (
    ("01_top_down", "strict top-down neutral"),
    ("02_front_left_3q", "front-left three-quarter pseudo-3D"),
    ("03_front_right_3q", "front-right three-quarter pseudo-3D"),
    ("04_rear_left_3q", "rear-left three-quarter"),
    ("05_rear_right_3q", "rear-right three-quarter"),
    ("06_hard_bank", "dramatic hard-bank upper-side"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def chroma_path(pilot: str, key: str) -> Path:
    return CHROMA / f"{pilot}_cinematic_views_chroma_{key}.png"


def repair_path(pilot: str, view: str) -> Path:
    return REPAIRS / pilot / f"{view}_chroma_green.png"


def dekey(image: Image.Image, key: str) -> Image.Image:
    rgb = np.asarray(image.convert("RGB"), dtype=np.float32)
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    if key == "green":
        dominance = green - np.maximum(red, blue)
    elif key == "magenta":
        dominance = np.minimum(red, blue) - green
    else:
        raise ValueError(key)

    positive = dominance[dominance > 0]
    if not positive.size:
        raise ValueError(f"no {key} key field detected")
    background_score = float(np.percentile(positive, 80))
    raw_alpha = np.clip(1.0 - dominance / max(background_score, 1.0), 0.0, 1.0)
    alpha = np.clip((raw_alpha - 0.11) / 0.82, 0.0, 1.0)

    background_mask = dominance >= background_score * 0.72
    key_rgb = np.median(rgb[background_mask], axis=0)
    safe = np.maximum(raw_alpha[..., None], 0.04)
    foreground = (rgb - (1.0 - raw_alpha[..., None]) * key_rgb) / safe
    foreground = np.clip(foreground, 0.0, 255.0)

    alpha_u8 = np.rint(alpha * 255.0).astype(np.uint8)
    foreground[alpha_u8 == 0] = 0.0
    rgba = np.dstack((foreground.astype(np.uint8), alpha_u8))
    return Image.fromarray(rgba, "RGBA")


def checker(size: tuple[int, int], cell: int = 24) -> Image.Image:
    width, height = size
    yy, xx = np.indices((height, width))
    pattern = ((xx // cell + yy // cell) % 2).astype(np.uint8)
    light = np.array((198, 202, 210), dtype=np.uint8)
    dark = np.array((72, 77, 88), dtype=np.uint8)
    return Image.fromarray(np.where(pattern[..., None] == 0, light, dark), "RGB")


def tight_cutout(frame: Image.Image, padding: int = 8) -> Image.Image:
    alpha = frame.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value >= 8 else 0).getbbox()
    if not bbox:
        raise ValueError("empty extracted frame")
    left, top, right, bottom = bbox
    left, top = max(0, left - padding), max(0, top - padding)
    right, bottom = min(frame.width, right + padding), min(frame.height, bottom + padding)
    return frame.crop((left, top, right, bottom))


def edge_metrics(master: Image.Image, key: str) -> dict:
    rgba = np.asarray(master, dtype=np.int16)
    rgb = rgba[..., :3]
    alpha = rgba[..., 3]
    semi = (alpha > 0) & (alpha < 255)
    if key == "green":
        dominance = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])
    else:
        dominance = np.minimum(rgb[..., 0], rgb[..., 2]) - rgb[..., 1]
    semi_values = np.maximum(dominance[semi], 0)
    return {
        "alpha_extrema": [int(alpha.min()), int(alpha.max())],
        "transparent_fraction": round(float(np.mean(alpha == 0)), 6),
        "opaque_fraction": round(float(np.mean(alpha == 255)), 6),
        "semi_transparent_key_dominance_p95": round(float(np.percentile(semi_values, 95)) if semi_values.size else 0.0, 3),
        "transparent_rgb_zero": bool(np.all(rgb[alpha == 0] == 0)),
    }


def main() -> None:
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    entries = []
    repaired_frames = []
    contact = Image.new("RGB", (1536, 1116), (6, 8, 12))
    draw = ImageDraw.Draw(contact)
    title_font = ImageFont.truetype(str(FONT), 22)
    small_font = ImageFont.truetype(str(FONT), 16)

    for index, (pilot, key) in enumerate(PILOTS):
        source = chroma_path(pilot, key)
        with Image.open(source) as image:
            if image.size != MASTER_SIZE:
                raise ValueError(f"{source.name}: expected {MASTER_SIZE}, got {image.size}")
            master = dekey(image, key)

        pilot_repairs = []
        for view_index, (slug, _) in enumerate(VIEWS):
            repair_source = repair_path(pilot, slug)
            if not repair_source.exists():
                continue
            with Image.open(repair_source) as repair_image:
                repair_rgb = repair_image.convert("RGB")
                if repair_rgb.size != FRAME_SIZE:
                    repair_rgb = repair_rgb.resize(FRAME_SIZE, Image.Resampling.LANCZOS)
                repair = dekey(repair_rgb, "green")
            col, row = view_index % 3, view_index // 3
            master.paste(repair, (col * FRAME_SIZE[0], row * FRAME_SIZE[1]))
            pilot_repairs.append(slug)

        pilot_dir = OUT / pilot
        frames_dir = pilot_dir / "frames_512"
        cutouts_dir = pilot_dir / "cutouts_native"
        frames_dir.mkdir(parents=True, exist_ok=True)
        cutouts_dir.mkdir(parents=True, exist_ok=True)
        master_path = pilot_dir / f"{pilot}_cinematic_views_master_rgba.png"
        master.save(master_path)

        view_entries = []
        for view_index, (slug, description) in enumerate(VIEWS):
            col, row = view_index % 3, view_index // 3
            box = (col * 512, row * 512, (col + 1) * 512, (row + 1) * 512)
            frame = master.crop(box)
            frame_path = frames_dir / f"{slug}.png"
            frame.save(frame_path)
            repair_source = repair_path(pilot, slug)
            if repair_source.exists():
                repaired_frames.append((pilot, slug, frame.copy()))
            cutout = tight_cutout(frame)
            cutout_path = cutouts_dir / f"{slug}.png"
            cutout.save(cutout_path)
            view_entries.append(
                {
                    "id": slug,
                    "description": description,
                    "frame_512": frame_path.relative_to(ROOT).as_posix(),
                    "cutout_native": cutout_path.relative_to(ROOT).as_posix(),
                    "cutout_size": list(cutout.size),
                    "frame_sha256": sha256(frame_path),
                    "cutout_sha256": sha256(cutout_path),
                    "continuity_repair_source": repair_source.relative_to(ROOT).as_posix() if repair_source.exists() else None,
                }
            )

        qa = checker(MASTER_SIZE)
        qa.paste(master, (0, 0), master)
        qa_path = pilot_dir / f"{pilot}_edge_qa_checker.jpg"
        qa.save(qa_path, quality=94, optimize=True)

        thumb = checker((512, 341), 16)
        resized = master.resize((512, 341), Image.Resampling.LANCZOS)
        thumb.paste(resized, (0, 0), resized)
        x, y = index % 3 * 512, index // 3 * 372
        contact.paste(thumb, (x, y))
        draw.text((x + 10, y + 344), pilot.upper(), font=title_font, fill=(113, 220, 255))
        draw.text((x + 390, y + 349), "6 VIEWS", font=small_font, fill=(178, 186, 200))

        entries.append(
            {
                "pilot": pilot,
                "master": master_path.relative_to(ROOT).as_posix(),
                "master_size": list(MASTER_SIZE),
                "master_sha256": sha256(master_path),
                "canonical_reference": (REFERENCES / f"{pilot}_canonical_ship_reference_rgba.png").relative_to(ROOT).as_posix(),
                "chroma_source": source.relative_to(ROOT).as_posix(),
                "chroma_key": key,
                "continuity_repairs": pilot_repairs,
                "edge_qa": qa_path.relative_to(ROOT).as_posix(),
                "edge_metrics": edge_metrics(master, key),
                "views": view_entries,
            }
        )

    contact_path = PREVIEWS / "cinematic_ships_9pilots_contact.jpg"
    contact.save(contact_path, quality=94, optimize=True)

    repair_contact = Image.new("RGB", (1024, 512), (6, 8, 12))
    repair_draw = ImageDraw.Draw(repair_contact)
    repair_font = ImageFont.truetype(str(FONT), 14)
    for index, (pilot, slug, frame) in enumerate(repaired_frames):
        x, y = index % 4 * 256, index // 4 * 256
        tile = checker((256, 256), 16)
        resized = frame.resize((256, 256), Image.Resampling.LANCZOS)
        tile.paste(resized, (0, 0), resized)
        repair_contact.paste(tile, (x, y))
        repair_draw.rectangle((x, y + 228, x + 256, y + 256), fill=(4, 7, 12))
        repair_draw.text((x + 8, y + 234), f"{pilot.upper()}  {slug}", font=repair_font, fill=(113, 220, 255))
    repair_contact_path = PREVIEWS / "cinematic_ships_tail_repairs_contact.jpg"
    repair_contact.save(repair_contact_path, quality=95, optimize=True)

    repair_manifest = [
        {"pilot": pilot, "view": slug}
        for pilot, slug, _ in repaired_frames
    ]
    manifest = {
        "pack": "Bullets of Fury pilot cinematic ship views",
        "pilot_count": len(entries),
        "views_per_pilot": len(VIEWS),
        "total_frames": len(entries) * len(VIEWS),
        "master_size": list(MASTER_SIZE),
        "fixed_frame_size": list(FRAME_SIZE),
        "background": "transparent RGBA",
        "edge_contract": "decontaminated alpha; transparent RGB is zero; no matte or halo",
        "generation": "built-in ImageGen reference workflow followed by deterministic chroma decontamination and frame extraction",
        "continuity_repair_count": len(repair_manifest),
        "continuity_repairs": repair_manifest,
        "view_order": [{"id": slug, "description": description} for slug, description in VIEWS],
        "pilots": entries,
        "preview": contact_path.relative_to(ROOT).as_posix(),
        "continuity_repair_preview": repair_contact_path.relative_to(ROOT).as_posix(),
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: built {len(entries)} pilots x {len(VIEWS)} cinematic ship frames ({len(entries) * len(VIEWS)} total).")


if __name__ == "__main__":
    main()
