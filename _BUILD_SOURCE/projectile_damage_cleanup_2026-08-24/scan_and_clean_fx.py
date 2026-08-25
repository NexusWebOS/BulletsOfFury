from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "_BUILD_SOURCE" / "review_combat_packs_2026-08-24" / "CF_EnemyCombatSystems-Vol.2" / "Edited"
OUT = Path(__file__).resolve().parent
PROJECTILE_OUT = OUT / "candidates" / "projectiles"
PROJECTILE_PREVIEWS = OUT / "previews" / "projectiles"
DAMAGE_EXTRACTED = OUT / "audit" / "damage_reels"
DAMAGE_PREVIEWS = OUT / "previews" / "damage_reels"

FONT = ImageFont.load_default()
NEIGHBORS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


def mkdirs() -> None:
    for path in (PROJECTILE_OUT, PROJECTILE_PREVIEWS, DAMAGE_EXTRACTED, DAMAGE_PREVIEWS, OUT / "audit"):
        path.mkdir(parents=True, exist_ok=True)


def alpha_components(image: Image.Image) -> list[list[tuple[int, int]]]:
    alpha = image.getchannel("A")
    width, height = image.size
    pixels = alpha.load()
    seen: set[tuple[int, int]] = set()
    components: list[list[tuple[int, int]]] = []
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 0 or (x, y) in seen:
                continue
            queue = deque([(x, y)])
            seen.add((x, y))
            component: list[tuple[int, int]] = []
            while queue:
                cx, cy = queue.popleft()
                component.append((cx, cy))
                for dx, dy in NEIGHBORS:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height and pixels[nx, ny] > 0 and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            components.append(component)
    components.sort(key=len, reverse=True)
    return components


def component_distance(a: list[tuple[int, int]], b: list[tuple[int, int]], early_stop: float = 3.0) -> float:
    ax0 = min(x for x, _ in a)
    ay0 = min(y for _, y in a)
    ax1 = max(x for x, _ in a)
    ay1 = max(y for _, y in a)
    bx0 = min(x for x, _ in b)
    by0 = min(y for _, y in b)
    bx1 = max(x for x, _ in b)
    by1 = max(y for _, y in b)
    box_dx = max(0, ax0 - bx1 - 1, bx0 - ax1 - 1)
    box_dy = max(0, ay0 - by1 - 1, by0 - ay1 - 1)
    if math.hypot(box_dx, box_dy) > early_stop:
        return math.hypot(box_dx, box_dy)
    best = float("inf")
    for x1, y1 in a:
        for x2, y2 in b:
            best = min(best, math.hypot(x1 - x2, y1 - y2))
            if best <= early_stop:
                return best
    return best


def clean_projectile(image: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    rgba = image.convert("RGBA")
    components = alpha_components(rgba)
    alpha_pixels = sum(len(component) for component in components)
    largest = len(components[0]) if components else 0
    dominance = largest / alpha_pixels if alpha_pixels else 0.0
    semitransparent = sum(1 for value in rgba.getchannel("A").getdata() if 0 < value < 255)
    width, height = rgba.size
    edge_touch = any(x in (0, width - 1) or y in (0, height - 1) for component in components for x, y in component)

    # A conservative rule: only clean a sprite with one clearly dominant body.
    # Tiny components close to that body may be intentional glints, so they stay.
    removable: list[list[tuple[int, int]]] = []
    if components and dominance >= 0.55:
        core = [component for component in components if len(component) >= max(9, round(largest * 0.02))]
        for component in components[1:]:
            threshold = max(4, min(10, round(largest * 0.008)))
            if len(component) > threshold:
                continue
            nearest = min((component_distance(component, candidate) for candidate in core), default=float("inf"))
            if nearest > 3.0:
                removable.append(component)

    cleaned = rgba.copy()
    pixels = cleaned.load()
    for component in removable:
        for x, y in component:
            pixels[x, y] = (0, 0, 0, 0)

    return cleaned, {
        "alpha_pixels": alpha_pixels,
        "component_count": len(components),
        "largest_component": largest,
        "largest_component_share": round(dominance, 4),
        "removed_components": len(removable),
        "removed_pixels": sum(len(component) for component in removable),
        "edge_touch": edge_touch,
        "semitransparent_pixels": semitransparent,
    }


def checkerboard(size: tuple[int, int], cell: int = 8) -> Image.Image:
    result = Image.new("RGBA", size, (9, 17, 29, 255))
    draw = ImageDraw.Draw(result)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            color = (18, 31, 49, 255) if (x // cell + y // cell) % 2 else (10, 21, 36, 255)
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=color)
    return result


def display_frame(image: Image.Image, scale: int = 2, label: str | None = None) -> Image.Image:
    panel = checkerboard((image.width * scale, image.height * scale + (18 if label else 0)))
    enlarged = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
    panel.alpha_composite(enlarged, (0, 18 if label else 0))
    if label:
        ImageDraw.Draw(panel).text((5, 4), label, fill=(225, 237, 255, 255), font=FONT)
    return panel


def save_gif(frames: list[Image.Image], path: Path, duration: int = 90) -> None:
    if not frames:
        return
    converted = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255) for frame in frames]
    converted[0].save(path, save_all=True, append_images=converted[1:], duration=duration, loop=0, disposal=2, transparency=0)


def audit_projectiles() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for family_dir in sorted(path for path in PACK.glob("vfx-*") if path.is_dir()):
        source_frames = sorted(
            path for path in family_dir.glob("*.png")
            if not path.name.endswith("-atlas.png") and "preview" not in path.name
        )
        before: list[Image.Image] = []
        after: list[Image.Image] = []
        cleaned_frames: list[Image.Image] = []
        family_changed = False
        candidate_dir = PROJECTILE_OUT / family_dir.name
        candidate_dir.mkdir(parents=True, exist_ok=True)
        for source_path in source_frames:
            source = Image.open(source_path).convert("RGBA")
            cleaned, metrics = clean_projectile(source)
            changed = metrics["removed_pixels"] > 0
            family_changed = family_changed or changed
            cleaned.save(candidate_dir / source_path.name)
            cleaned_frames.append(cleaned)
            before.append(display_frame(source))
            after.append(display_frame(cleaned))
            rows.append({
                "family": family_dir.name,
                "frame": source_path.name,
                "changed": changed,
                **metrics,
            })
        if source_frames:
            save_gif(before, PROJECTILE_PREVIEWS / f"{family_dir.name}-before.gif")
            save_gif(after, PROJECTILE_PREVIEWS / f"{family_dir.name}-candidate.gif")
            metadata_paths = sorted(family_dir.glob("*.json"))
            if metadata_paths:
                metadata = json.loads(metadata_paths[0].read_text(encoding="utf-8"))
                atlas_name = metadata.get("atlas", {}).get("file")
                rects = metadata.get("atlas", {}).get("rects", {})
                if atlas_name and (family_dir / atlas_name).exists():
                    atlas = Image.open(family_dir / atlas_name).convert("RGBA").copy()
                    for source_path, cleaned in zip(source_frames, cleaned_frames):
                        rect = rects.get(source_path.stem)
                        if rect:
                            x, y, width, height = [int(value) for value in rect]
                            if cleaned.size == (width, height):
                                atlas.paste(cleaned, (x, y))
                    atlas.save(candidate_dir / atlas_name)
                    (candidate_dir / metadata_paths[0].name).write_text(
                        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
                    )
            if family_changed:
                width = before[0].width * 2
                contact = Image.new("RGBA", (width, len(before) * before[0].height + 36), (6, 10, 18, 255))
                draw = ImageDraw.Draw(contact)
                draw.text((8, 6), "ORIGINAL", fill=(255, 190, 120, 255), font=FONT)
                draw.text((before[0].width + 8, 6), "CLEANED CANDIDATE", fill=(124, 255, 176, 255), font=FONT)
                y = 36
                for original, candidate in zip(before, after):
                    contact.alpha_composite(original, (0, y))
                    contact.alpha_composite(candidate, (before[0].width, y))
                    y += original.height
                contact.save(PROJECTILE_PREVIEWS / f"{family_dir.name}-comparison.png")
    return rows


def manifest_damage_cells() -> dict[str, dict[str, object]]:
    js = r'''
global.window={};
require('./assets/manifest.js');
const cells=window.BOFX.cells||{};
const img=window.BOFX.img||{};
const rx=/(?:_dmgov_|_dmg_|_smoke_)\d+$/;
const out={};
for(const [key,cell] of Object.entries(cells)) {
  if(rx.test(key) && (key.startsWith('mb') || key.startsWith('n6') || key.startsWith('ngm') || key.startsWith('nx'))) {
    out[key]={cell, img:img[key]||null};
  }
}
process.stdout.write(JSON.stringify(out));
'''
    result = subprocess.run(["node", "-e", js], cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def group_key(key: str) -> str:
    return re.sub(r"\d+$", "", key).rstrip("_")


def crop_cell(definition: dict[str, object]) -> Image.Image:
    cell = definition["cell"]
    atlas_index, x, y, width, height = [int(value) for value in cell]
    image_path = definition.get("img") or f"assets/game/atlas/nca_{atlas_index}.png"
    atlas = Image.open(ROOT / str(image_path)).convert("RGBA")
    return atlas.crop((x, y, x + width, y + height))


def rgba_hash(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def warm_pixels(image: Image.Image) -> int:
    count = 0
    for r, g, b, a in image.convert("RGBA").getdata():
        if a and r >= 115 and r >= g * 1.18 and g >= b * 0.72 and b < 145:
            count += 1
    return count


def smoke_pixels(image: Image.Image) -> int:
    count = 0
    for r, g, b, a in image.convert("RGBA").getdata():
        hi, lo = max(r, g, b), min(r, g, b)
        if a and 38 <= hi <= 205 and hi - lo <= 24:
            count += 1
    return count


def mean_frame_delta(a: Image.Image, b: Image.Image) -> float:
    if a.size != b.size:
        return 1.0
    pa = a.convert("RGBA").tobytes()
    pb = b.convert("RGBA").tobytes()
    return sum(x != y for x, y in zip(pa, pb)) / len(pa)


def audit_damage_reels() -> list[dict[str, object]]:
    definitions = manifest_damage_cells()
    groups: dict[str, list[tuple[str, dict[str, object]]]] = {}
    for key, definition in definitions.items():
        groups.setdefault(group_key(key), []).append((key, definition))

    rows: list[dict[str, object]] = []
    sheet_panels: list[tuple[str, Image.Image]] = []
    for group, entries in sorted(groups.items()):
        entries.sort(key=lambda item: int(re.search(r"(\d+)$", item[0]).group(1)))
        frames: list[Image.Image] = []
        frame_dir = DAMAGE_EXTRACTED / group
        frame_dir.mkdir(parents=True, exist_ok=True)
        for key, definition in entries:
            frame = crop_cell(definition)
            frames.append(frame)
            frame.save(frame_dir / f"{key}.png")
        hashes = [rgba_hash(frame) for frame in frames]
        deltas = [mean_frame_delta(frames[index - 1], frame) for index, frame in enumerate(frames) if index]
        warm = [warm_pixels(frame) for frame in frames]
        smoke = [smoke_pixels(frame) for frame in frames]
        unique = len(set(hashes))
        static = unique == 1
        mean_delta = sum(deltas) / len(deltas) if deltas else 0.0
        rows.append({
            "group": group,
            "frame_count": len(frames),
            "unique_frames": unique,
            "static": static,
            "mean_byte_delta": round(mean_delta, 6),
            "warm_pixel_range": max(warm) - min(warm) if warm else 0,
            "smoke_pixel_range": max(smoke) - min(smoke) if smoke else 0,
            "max_width": max((frame.width for frame in frames), default=0),
            "max_height": max((frame.height for frame in frames), default=0),
        })
        if frames:
            max_w = max(frame.width for frame in frames)
            max_h = max(frame.height for frame in frames)
            gif_frames: list[Image.Image] = []
            for index, frame in enumerate(frames):
                panel = checkerboard((max_w, max_h + 18))
                panel.alpha_composite(frame, ((max_w - frame.width) // 2, 18 + (max_h - frame.height) // 2))
                ImageDraw.Draw(panel).text((4, 3), f"{group} {index + 1}/{len(frames)}", fill=(230, 240, 255, 255), font=FONT)
                gif_frames.append(panel.resize((max_w * 2, (max_h + 18) * 2), Image.Resampling.NEAREST))
            save_gif(gif_frames, DAMAGE_PREVIEWS / f"{group}.gif", duration=110)
            strip_w = min(1400, sum(min(240, frame.width) for frame in gif_frames))
            thumb_h = 180
            strip = Image.new("RGBA", (strip_w, thumb_h + 24), (6, 10, 18, 255))
            draw = ImageDraw.Draw(strip)
            draw.text((5, 5), group, fill=(230, 240, 255, 255), font=FONT)
            x = 0
            for frame in frames:
                scale = min(1.0, 220 / frame.width, thumb_h / frame.height)
                thumb = frame.resize((max(1, round(frame.width * scale)), max(1, round(frame.height * scale))), Image.Resampling.NEAREST)
                tile = checkerboard((thumb.width, thumb_h))
                tile.alpha_composite(thumb, (0, (thumb_h - thumb.height) // 2))
                if x + tile.width > strip.width:
                    break
                strip.alpha_composite(tile, (x, 24))
                x += tile.width
            sheet_panels.append((group, strip))

    if sheet_panels:
        width = max(panel.width for _, panel in sheet_panels)
        height = sum(panel.height + 8 for _, panel in sheet_panels)
        sheet = Image.new("RGBA", (width, height), (4, 8, 14, 255))
        y = 0
        for _, panel in sheet_panels:
            sheet.alpha_composite(panel, (0, y))
            y += panel.height + 8
        sheet.save(DAMAGE_PREVIEWS / "damage-reel-contact-sheet.png")
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_readme(projectile_rows: list[dict[str, object]], damage_rows: list[dict[str, object]]) -> None:
    changed_frames = [row for row in projectile_rows if row["changed"]]
    changed_families = sorted({str(row["family"]) for row in changed_frames})
    static_damage = [row for row in damage_rows if row["static"]]
    static_effect_path = OUT / "audit" / "static_damage_effect_audit.csv"
    static_effect_rows: list[dict[str, str]] = []
    if static_effect_path.exists():
        with static_effect_path.open("r", newline="", encoding="utf-8") as handle:
            static_effect_rows = list(csv.DictReader(handle))
    static_candidates = [row for row in static_effect_rows if row.get("status") == "candidate_generated"]
    text = f"""# Projectile and damage-effect cleanup review

This folder is non-live review material. Nothing here is referenced by `assets/manifest.js` or `assets/game.js`.

## Projectile scan

- Families scanned: {len(set(str(row['family']) for row in projectile_rows))}
- Frames scanned: {len(projectile_rows)}
- Candidate frames with disconnected micro-components removed: {len(changed_frames)}
- Families with at least one candidate change: {len(changed_families)}
- Changed families: {', '.join(changed_families) if changed_families else 'none'}

The cleanup is intentionally conservative. It runs only when one connected body owns at least 55% of visible pixels. Components near the body remain, and multi-pellet/impact families are not auto-cleaned.

## Existing damage/smoke reels

- Reels extracted from the live manifest: {len(damage_rows)}
- Reels whose frames are exact duplicates: {len(static_damage)}
- Exact-duplicate reels: {', '.join(str(row['group']) for row in static_damage) if static_damage else 'none'}

The CSV also records warm-pixel and neutral-smoke pixel variation. Low variation identifies effects that may technically have multiple frames while their fire/smoke remains visually frozen.

## Static damaged/critical cells

- Unique cells compared against intact counterparts: {len(static_effect_rows)}
- Eight-frame moving fire/smoke candidates generated: {len(static_candidates)}
- Each candidate preserves canvas dimensions, damaged hull pixels, hull silhouette, and anchor. Flame tongues, smoke lobes, and embers change position and effect silhouette across the reel.
- `previews/damage_effects/index.html` is the review gallery. `previews/damage_effects/qa-selected-eight-frame-sheet.png` is the compact QA sample.

## Review locations

- `previews/projectiles/`: original and cleaned candidate GIFs; changed families also have comparison PNGs.
- `previews/damage_reels/`: live damage/smoke reels extracted from atlases.
- `audit/projectile_audit.csv`: component-level projectile results.
- `audit/damage_reel_audit.csv`: reel uniqueness and effect-pixel variation.
- `candidates/projectiles/`: standalone candidate PNGs, never wired.
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    mkdirs()
    projectile_rows = audit_projectiles()
    damage_rows = audit_damage_reels()
    write_csv(OUT / "audit" / "projectile_audit.csv", projectile_rows)
    write_csv(OUT / "audit" / "damage_reel_audit.csv", damage_rows)
    write_readme(projectile_rows, damage_rows)
    print(json.dumps({
        "projectile_frames": len(projectile_rows),
        "projectile_changed_frames": sum(bool(row["changed"]) for row in projectile_rows),
        "projectile_changed_families": len({str(row["family"]) for row in projectile_rows if row["changed"]}),
        "damage_reels": len(damage_rows),
        "static_damage_reels": sum(bool(row["static"]) for row in damage_rows),
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
