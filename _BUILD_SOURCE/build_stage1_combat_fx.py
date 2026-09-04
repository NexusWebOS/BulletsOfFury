"""Build the production Stage-1 combat VFX atlas.

The military projectile families were already approved in the Enemy Combat Systems
review pack.  The Jungle wind/laser rows come from the built-in ImageGen source in
``_ART_SOURCES/stage1_ai_fx``.  This script removes only the light neutral field that
is connected to the image border, normalizes the generated frames, and packs every
family into one lazy-loaded runtime texture.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
GENERATED_SOURCE_ROOT = ROOT / "_ART_SOURCES" / "stage1_ai_fx" / "spaced_v2"
PROJECTILE_ROOT = (
    ROOT
    / "_BUILD_SOURCE"
    / "projectile_damage_cleanup_2026-08-24"
    / "candidates"
    / "projectiles"
)
OUT = ROOT / "assets" / "game" / "atlas" / "stage1_combat_fx.png"
META = ROOT / "assets" / "game" / "atlas" / "stage1_combat_fx.json"

CELL = 192
COLS = 6

APPROVED_ROWS = [
    ("jungle_missile", "vfx-heavy-toxic-jungle-missile", "heavy-toxic-jungle-missile", True),
    ("cannon_shell", "vfx-heavy-heavy-cannon-shell", "heavy-heavy-cannon-shell", True),
    ("military_muzzle", "vfx-heavy-military-cannon-muzzle", "heavy-military-cannon-muzzle", True),
    ("rotary_muzzle", "vfx-heavy-rotary-cannon-muzzle", "heavy-rotary-cannon-muzzle", True),
    ("flak_impact", "vfx-heavy-flak-blossom", "heavy-flak-blossom", False),
]

GENERATED_ROWS = [
    ("green_laser", "green_laser_spaced.png", 112, True),
    ("wind_blade", "wind_blade_spaced.png", 96, False),
    ("wind_vortex", "wind_vortex_spaced.png", 116, False),
    ("green_impact", "green_impact_spaced.png", 116, False),
]

RAW_EDGE_GUARD = 20
ATLAS_EDGE_GUARD = 20
SOURCE_GROUP_PADDING = 40
SOURCE_FRAGMENT_GAP = 64


def border_alpha(source: Image.Image) -> Image.Image:
    """Remove only high-luma neutral pixels connected to the outer border."""

    rgb = np.asarray(source.convert("RGB"), dtype=np.uint8)
    high = rgb.max(axis=2).astype(np.int16)
    low = rgb.min(axis=2).astype(np.int16)
    luma = (
        rgb[:, :, 0].astype(np.int32) * 54
        + rgb[:, :, 1].astype(np.int32) * 183
        + rgb[:, :, 2].astype(np.int32) * 19
    ) // 256
    # The generated preview alternates white and light-gray matte tiles.  Both are neutral
    # and connected, so the lower luma bound has to include the gray half of the checker.
    candidate = ((luma >= 168) & ((high - low) <= 42)).astype(np.uint8) * 255
    # ``fromarray`` may expose a read-only buffer; Pillow's floodfill then silently
    # leaves it untouched.  Copy into a writable image before clearing the matte.
    mask = Image.fromarray(candidate, "L").copy()
    # The generator's neutral checker field is one connected region.  White cores are
    # enclosed by green pixels, so flood-filling from the edge preserves them.
    ImageDraw.floodfill(mask, (0, 0), 128, thresh=0)
    background = np.asarray(mask, dtype=np.uint8) == 128
    alpha = np.where(background, 0, 255).astype(np.uint8)
    rgba = np.dstack((rgb, alpha))
    rgba[alpha == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def normalize_frame(frame: Image.Image, visible_max: int, rotate: bool = False) -> Image.Image:
    if rotate:
        frame = frame.transpose(Image.Transpose.ROTATE_180)
    bbox = frame.getchannel("A").point(lambda value: 255 if value > 4 else 0).getbbox()
    if bbox is None:
        raise RuntimeError("Generated Stage-1 VFX frame contains no visible pixels")
    frame = frame.crop(bbox)
    scale = min(visible_max / max(frame.width, frame.height), 1.0)
    target = (max(1, round(frame.width * scale)), max(1, round(frame.height * scale)))
    if target != frame.size:
        frame = frame.resize(target, Image.Resampling.NEAREST)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.alpha_composite(frame, ((CELL - frame.width) // 2, (CELL - frame.height) // 2))
    normalized_bbox = cell.getchannel("A").point(lambda value: 255 if value > 4 else 0).getbbox()
    if normalized_bbox is None:
        raise RuntimeError("Normalized Stage-1 VFX frame contains no visible pixels")
    left, top, right, bottom = normalized_bbox
    if min(left, top, CELL - right, CELL - bottom) < ATLAS_EDGE_GUARD:
        raise RuntimeError(
            f"Normalized Stage-1 VFX frame violates the {ATLAS_EDGE_GUARD}px atlas edge guard: "
            f"{normalized_bbox}"
        )
    return cell


def generated_frames() -> dict[str, list[Image.Image]]:
    out: dict[str, list[Image.Image]] = {}
    for family, filename, visible_max, rotate in GENERATED_ROWS:
        source_path = GENERATED_SOURCE_ROOT / filename
        clean = border_alpha(Image.open(source_path))
        width, height = clean.size
        alpha = np.asarray(clean.getchannel("A"), dtype=np.uint8) > 4
        occupied_columns = np.flatnonzero(alpha.any(axis=0))
        runs: list[list[int]] = []
        for x_value in occupied_columns:
            x = int(x_value)
            if not runs or x - runs[-1][1] > SOURCE_FRAGMENT_GAP:
                runs.append([x, x])
            else:
                runs[-1][1] = x
        if len(runs) != COLS:
            raise RuntimeError(
                f"{source_path.name} must contain exactly {COLS} isolated frame groups; "
                f"detected {len(runs)} at {runs}"
            )
        frames: list[Image.Image] = []
        for col, (run_left, run_right) in enumerate(runs):
            x0 = max(0, run_left - SOURCE_GROUP_PADDING)
            x1 = min(width, run_right + SOURCE_GROUP_PADDING + 1)
            raw = clean.crop((x0, 0, x1, height))
            raw_bbox = raw.getchannel("A").point(lambda value: 255 if value > 4 else 0).getbbox()
            if raw_bbox is None:
                raise RuntimeError(f"{source_path.name} frame {col} contains no visible pixels")
            left, top, right, bottom = raw_bbox
            clearance = min(left, top, raw.width - right, raw.height - bottom)
            if clearance < RAW_EDGE_GUARD:
                raise RuntimeError(
                    f"{source_path.name} frame {col} is unsafe to slice: visible bbox {raw_bbox} "
                    f"leaves only {clearance}px clearance (need {RAW_EDGE_GUARD}px)"
                )
            frames.append(normalize_frame(raw, visible_max, rotate))
        out[family] = frames
    return out


def approved_frames(folder: str, stem: str, rotate: bool) -> list[Image.Image]:
    frames: list[Image.Image] = []
    for index in range(1, COLS + 1):
        path = PROJECTILE_ROOT / folder / f"{stem}-{index:02d}.png"
        frame = Image.open(path).convert("RGBA")
        if frame.size != (CELL, CELL):
            raise RuntimeError(f"Unexpected approved frame size for {path}: {frame.size}")
        if rotate:
            frame = frame.transpose(Image.Transpose.ROTATE_180)
        frames.append(frame)
    return frames


def main() -> None:
    rows: list[tuple[str, list[Image.Image]]] = []
    for family, folder, stem, rotate in APPROVED_ROWS:
        rows.append((family, approved_frames(folder, stem, rotate)))
    rows.extend(generated_frames().items())

    atlas = Image.new("RGBA", (CELL * COLS, CELL * len(rows)), (0, 0, 0, 0))
    rects: dict[str, list[int]] = {}
    for row, (family, frames) in enumerate(rows):
        for col, frame in enumerate(frames):
            x, y = col * CELL, row * CELL
            atlas.alpha_composite(frame, (x, y))
            rects[f"s1fx_{family}_{col}"] = [x, y, CELL, CELL]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(OUT, optimize=True)
    metadata = {
        "atlas": OUT.relative_to(ROOT).as_posix(),
        "cell": [CELL, CELL],
        "columns": COLS,
        "rows": [name for name, _ in rows],
        "rects": rects,
        "generation": (
            "approved military VFX plus four separately generated, widely spaced built-in "
            "ImageGen Jungle strips; guarded slicing, border-connected neutral-field removal, "
            "and deterministic frame normalization"
        ),
        "source_edge_guard": RAW_EDGE_GUARD,
        "atlas_edge_guard": ATLAS_EDGE_GUARD,
    }
    META.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} {atlas.size[0]}x{atlas.size[1]}")
    print(f"wrote {META.relative_to(ROOT)} with {len(rects)} cells")


if __name__ == "__main__":
    main()
