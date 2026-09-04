"""Pack the 0901 authored combat projectiles into gutter-safe runtime atlases.

The generated source sheets are presentation grids, not trustworthy sprite grids: their
row/column gaps are visually regular but not mathematically uniform.  Cutting them with
``width / columns`` is what shaved lightning forks and projectile exhaust in earlier passes.

This packer finds the transparent valleys between presentation columns/rows, measures each
frame's alpha bounds, applies one scale per animation row (so growth between frames is
preserved), and places every frame inside a fixed padded runtime cell.  It fails the build if
opaque pixels approach a finished cell edge.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "game" / "combat_upgrade_0901" / "source"
OUT = ROOT / "assets" / "game" / "combat_upgrade_0901"
ALPHA_THRESHOLD = 8


@dataclass(frozen=True)
class AtlasSpec:
    sources: tuple[tuple[str, tuple[str, ...]], ...]
    output: str
    cell: tuple[int, int] = (256, 256)
    fit: tuple[int, int] = (184, 184)


SPECS = (
    AtlasSpec(
        (("stage2_volcanic_projectiles_a.png", ("needle", "rake", "slag", "rocket")),
         ("stage2_volcanic_projectiles_b.png", ("bomb", "shock", "breath", "mine"))),
        "stage2_volcanic_projectiles_atlas.png",
    ),
    AtlasSpec(
        (("stage5_alien_projectiles_a.png", ("fracture", "split", "prism", "null")),
         ("stage5_alien_projectiles_b.png", ("missile", "chaos", "halo"))),
        "stage5_alien_projectiles_atlas.png",
    ),
    AtlasSpec(
        (("stage7_toxic_projectiles_a.png", ("acid", "sludge", "shard")),
         ("stage7_toxic_projectiles_b.png", ("bio", "laser", "grenade"))),
        "stage7_toxic_projectiles_atlas.png",
    ),
    AtlasSpec(
        (("stage8_symbiote_projectiles_a.png", ("needle", "rage", "slug", "missile")),
         ("stage8_symbiote_projectiles_b.png", ("pair", "blade", "rift", "parasite"))),
        "stage8_symbiote_projectiles_atlas.png",
    ),
    AtlasSpec(
        (("stage4_chain_lightning_source.png", ("chain_a", "chain_b")),),
        "stage4_chain_lightning_atlas.png",
        cell=(256, 384),
        fit=(164, 304),
    ),
)


def _transparent_boundaries(alpha: np.ndarray, count: int, axis: int) -> list[int]:
    """Return presentation-grid cuts at transparent valleys near each nominal cut."""
    mask = alpha > ALPHA_THRESHOLD
    projection = mask.sum(axis=axis)
    size = projection.shape[0]
    nominal_cell = size / count
    cuts = [0]
    for index in range(1, count):
        nominal = index * nominal_cell
        radius = int(nominal_cell * 0.34)
        lo = max(cuts[-1] + 8, int(nominal - radius))
        hi = min(size - 8, int(nominal + radius))
        if hi <= lo:
            raise RuntimeError(f"No search window for cut {index}/{count}")

        values = projection[lo:hi]
        minimum = int(values.min())
        candidates = np.flatnonzero(values == minimum) + lo
        # A long zero valley is common. Pick the point nearest the expected grid line so
        # neighbouring cells retain comparable whitespace.
        cut = int(candidates[np.argmin(np.abs(candidates - nominal))])
        cuts.append(cut)
    cuts.append(size)
    return cuts


def _alpha_bbox(frame: Image.Image) -> tuple[int, int, int, int]:
    alpha = np.asarray(frame.getchannel("A"))
    ys, xs = np.where(alpha > ALPHA_THRESHOLD)
    if not len(xs):
        raise RuntimeError("Empty animation frame")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def pack(spec: AtlasSpec) -> dict:
    cols = 4
    raw_frames: list[list[Image.Image]] = []
    bboxes: list[list[tuple[int, int, int, int]]] = []
    roles: list[str] = []
    source_cuts = []
    for source_name, source_roles in spec.sources:
        source = Image.open(SOURCE / source_name).convert("RGBA")
        alpha = np.asarray(source.getchannel("A"))
        xcuts = _transparent_boundaries(alpha, cols, axis=0)
        ycuts = _transparent_boundaries(alpha, len(source_roles), axis=1)
        source_cuts.append({"source": source_name, "x": xcuts, "y": ycuts})
        for row, role in enumerate(source_roles):
            frame_row: list[Image.Image] = []
            bbox_row: list[tuple[int, int, int, int]] = []
            for col in range(cols):
                frame = source.crop((xcuts[col], ycuts[row], xcuts[col + 1], ycuts[row + 1]))
                bbox = _alpha_bbox(frame)
                frame_row.append(frame)
                bbox_row.append(bbox)
            roles.append(role)
            raw_frames.append(frame_row)
            bboxes.append(bbox_row)

    rows = len(roles)

    cell_w, cell_h = spec.cell
    fit_w, fit_h = spec.fit
    atlas = Image.new("RGBA", (cell_w * cols, cell_h * rows), (0, 0, 0, 0))
    audit = []
    resampling = getattr(Image, "Resampling", Image).LANCZOS
    for row, role in enumerate(roles):
        # One uniform scale per role preserves the generated small-to-large animation.
        max_w = max(box[2] - box[0] for box in bboxes[row])
        max_h = max(box[3] - box[1] for box in bboxes[row])
        scale = min(1.0, fit_w / max_w, fit_h / max_h)
        row_audit = {"role": role, "scale": round(scale, 5), "frames": []}
        for col in range(cols):
            frame = raw_frames[row][col]
            box = bboxes[row][col]
            sprite = frame.crop(box)
            out_w = max(1, round(sprite.width * scale))
            out_h = max(1, round(sprite.height * scale))
            if (out_w, out_h) != sprite.size:
                sprite = sprite.resize((out_w, out_h), resampling)
            dx = col * cell_w + (cell_w - out_w) // 2
            dy = row * cell_h + (cell_h - out_h) // 2
            atlas.alpha_composite(sprite, (dx, dy))
            gutters = {
                "left": dx - col * cell_w,
                "top": dy - row * cell_h,
                "right": (col + 1) * cell_w - (dx + out_w),
                "bottom": (row + 1) * cell_h - (dy + out_h),
            }
            if min(gutters.values()) < 20:
                raise RuntimeError(f"Unsafe finished gutter: {spec.output} {role} f{col}: {gutters}")
            row_audit["frames"].append({"size": [out_w, out_h], "gutters": gutters})
        audit.append(row_audit)

    output_path = OUT / spec.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output_path, optimize=True)
    return {
        "sources": [name for name, _ in spec.sources],
        "output": spec.output,
        "grid": [cols, rows],
        "cell": [cell_w, cell_h],
        "source_cuts": source_cuts,
        "rows": audit,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"alpha_threshold": ALPHA_THRESHOLD, "atlases": [pack(spec) for spec in SPECS]}
    report_path = OUT / "combat_projectile_atlas_audit.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    for item in report["atlases"]:
        minimum = min(
            min(frame["gutters"].values())
            for row in item["rows"]
            for frame in row["frames"]
        )
        print(f"{item['output']}: {item['grid'][0]}x{item['grid'][1]}, min gutter {minimum}px")
    print(f"audit: {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
