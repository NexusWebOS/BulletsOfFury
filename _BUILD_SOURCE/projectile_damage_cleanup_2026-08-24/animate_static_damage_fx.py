from __future__ import annotations

import csv
import html
import json
import math
import re
import subprocess
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CANDIDATES = OUT / "candidates" / "damage_effects"
PREVIEWS = OUT / "previews" / "damage_effects"
AUDIT = OUT / "audit"
FONT = ImageFont.load_default()


def manifest_static_damage() -> list[dict[str, object]]:
    js = r'''
global.window={};
require('./assets/manifest.js');
const cells=window.BOFX.cells||{};
const img=window.BOFX.img||{};
const keys=Object.keys(cells).filter(k => /_(damaged|critical)(?:_idle)?$/.test(k));
const output=[];
for(const key of keys){
  const candidates=[
    key.replace(/_(damaged|critical)(_idle)?$/, '_intact$2'),
    key.replace(/_(damaged|critical)(_idle)?$/, '$2'),
    key.replace(/_(damaged|critical)(_idle)?$/, '')
  ];
  const intactKey=candidates.find(candidate => cells[candidate]);
  if(!intactKey) continue;
  output.push({key, cell:cells[key], img:img[key]||null, intactKey, intactCell:cells[intactKey], intactImg:img[intactKey]||null});
}
process.stdout.write(JSON.stringify(output));
'''
    result = subprocess.run(["node", "-e", js], cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def crop(cell: list[int], image_path: str | None) -> Image.Image:
    atlas_index, x, y, width, height = [int(value) for value in cell]
    path = ROOT / (image_path or f"assets/game/atlas/nca_{atlas_index}.png")
    atlas = Image.open(path).convert("RGBA")
    return atlas.crop((x, y, x + width, y + height))


def color_delta(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])


def classify_masks(damaged: Image.Image, intact: Image.Image) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    fire: set[tuple[int, int]] = set()
    smoke: set[tuple[int, int]] = set()
    dp = damaged.convert("RGBA").load()
    ip = intact.convert("RGBA").load()
    width, height = damaged.size
    for y in range(height):
        for x in range(width):
            d = dp[x, y]
            i = ip[x, y]
            if d[3] == 0 or color_delta(d, i) < 38:
                continue
            r, g, b, _ = d
            added = i[3] == 0
            warm = r >= 125 and r >= g * 1.14 and g >= 35 and b < 150
            hot = r >= 190 and g >= 90 and b <= 125
            neutral = 30 <= max(r, g, b) <= 215 and max(r, g, b) - min(r, g, b) <= 30
            if warm or hot:
                # Interior pixels must be a meaningful repaint; exterior flames/sparks are always eligible.
                if added or color_delta(d, i) >= 90:
                    fire.add((x, y))
            elif added and neutral:
                smoke.add((x, y))

    # Add immediately neighboring changed effect pixels so the light moves through the
    # whole flame/smoke cluster instead of producing isolated twinkles.
    loose_changed: set[tuple[int, int]] = set()
    broad_smoke: set[tuple[int, int]] = set()
    for y in range(height):
        for x in range(width):
            d = dp[x, y]
            i = ip[x, y]
            delta = color_delta(d, i)
            if d[3] and delta >= 55:
                loose_changed.add((x, y))
                r, g, b, _ = d
                hi, lo = max(r, g, b), min(r, g, b)
                added = i[3] == 0
                # Full smoke palette: deep charcoal rims, midtone lobes, and pale highlights.
                # Keep this neutral enough to reject ice, painted metal, and exposed wiring
                # even when those pixels touch the cloud.
                if 12 <= hi <= 238 and hi - lo <= 62:
                    broad_smoke.add((x, y))
    for _ in range(2):
        for x, y in tuple(fire):
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                p = (x + dx, y + dy)
                if p not in loose_changed:
                    continue
                r, g, b, a = dp[p[0], p[1]]
                if a and r >= 90 and r >= b * 1.05:
                    fire.add(p)
    # Flood from the reliable neutral exterior seeds through the complete broad smoke
    # palette. This removes the old static cloud as one layer instead of animating only
    # a few internal gray patches.
    queue = deque(smoke)
    visited = set(smoke)
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
            point = (x + dx, y + dy)
            if point in visited or point not in broad_smoke or point in fire:
                continue
            visited.add(point)
            smoke.add(point)
            queue.append(point)
    # One exterior fringe pass captures colored antialias/rim pixels immediately
    # touching the smoke mass without leaking into the intact hull.
    fringe = set()
    for x, y in smoke:
        for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
            px, py = x + dx, y + dy
            if not (0 <= px < width and 0 <= py < height) or (px, py) in fire:
                continue
            if ip[px, py][3] == 0 and dp[px, py][3] and color_delta(dp[px, py], ip[px, py]) >= 38:
                r, g, b, _ = dp[px, py]
                if max(r, g, b) - min(r, g, b) <= 72:
                    fringe.add((px, py))
    smoke.update(fringe)
    smoke.difference_update(fire)
    return fire, smoke


def mask_components(mask: set[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    remaining = set(mask)
    components: list[list[tuple[int, int]]] = []
    while remaining:
        seed = remaining.pop()
        queue = deque([seed])
        component = [seed]
        while queue:
            x, y = queue.popleft()
            for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
                point = (x + dx, y + dy)
                if point in remaining:
                    remaining.remove(point)
                    queue.append(point)
                    component.append(point)
        components.append(component)
    return sorted(components, key=len, reverse=True)


def transformed_component(
    source: Image.Image,
    component: list[tuple[int, int]],
    frame_index: int,
    kind: str,
    component_index: int,
) -> list[tuple[int, int, tuple[int, int, int, int]]]:
    src = source.convert("RGBA")
    left = min(x for x, _ in component)
    top = min(y for _, y in component)
    right = max(x for x, _ in component)
    bottom = max(y for _, y in component)
    width, height = right - left + 1, bottom - top + 1
    crop = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    cp = crop.load()
    sp = src.load()
    for x, y in component:
        cp[x - left, y - top] = sp[x, y]

    if frame_index == 0:
        return [(x, y, sp[x, y]) for x, y in component]

    if kind == "fire" and len(component) <= 10:
        # Embers visibly hop upward and sideways, returning toward their start for a loop.
        rise = (0, -1, -2, -3, -4, -3, -2, -1)[frame_index]
        sway = round(math.sin(frame_index * math.pi / 4 + component_index * 1.7) * 2)
        return [(x + sway, y + rise, sp[x, y]) for x, y in component]

    if kind == "fire":
        scales = (1.00, 1.12, 0.94, 1.20, 0.88, 1.10, 0.96, 1.05)
        scale_y = scales[frame_index]
        max_sway = max(1, min(4, width // 5 + 1))
    else:
        scales = (1.00, 1.05, 1.10, 1.15, 1.10, 1.05, 1.01, 0.97)
        scale_y = scales[frame_index]
        max_sway = max(2, min(7, width // 5 + 1))

    resized_h = max(1, round(height * scale_y))
    resized = crop.resize((width, resized_h), Image.Resampling.NEAREST)
    rp = resized.load()
    anchor_y = bottom - resized_h + 1
    points: list[tuple[int, int, tuple[int, int, int, int]]] = []
    for row in range(resized_h):
        normalized = 1.0 - row / max(1, resized_h - 1)
        phase = frame_index * math.pi / 4 + component_index * 0.9
        if kind == "fire":
            shift_x = round(math.sin(phase + row * 0.42) * max_sway * normalized)
            shift_y = 0
        else:
            whole_drift = (0, 2, 4, 3, 1, -2, -3, -1)[frame_index]
            shift_x = whole_drift + round(math.sin(phase + row * 0.18) * max_sway * (0.35 + normalized * 0.65))
            rise = (0, -2, -4, -6, -8, -6, -4, -2)[frame_index]
            shift_y = rise
        for col in range(width):
            color = rp[col, row]
            if color[3]:
                points.append((left + col + shift_x, anchor_y + row + shift_y, color))
    return points


def animate_frame(
    damaged: Image.Image,
    intact: Image.Image,
    fire: set[tuple[int, int]],
    smoke: set[tuple[int, int]],
    frame_index: int,
) -> Image.Image:
    # Remove the baked static effect first, restoring the intact hull beneath it.
    # The damaged/scorched hull outside the isolated effect masks stays untouched.
    output = damaged.convert("RGBA").copy()
    dst = output.load()
    intact_pixels = intact.convert("RGBA").load()
    for x, y in fire | smoke:
        dst[x, y] = intact_pixels[x, y] if intact_pixels[x, y][3] else (0, 0, 0, 0)

    width, height = output.size
    smoke_components = mask_components(smoke)
    fire_components = mask_components(fire)
    # Smoke goes down first; hot flame cores and embers sit on top.
    for kind, components in (("smoke", smoke_components), ("fire", fire_components)):
        for index, component in enumerate(components):
            for x, y, color in transformed_component(damaged, component, frame_index, kind, index):
                if 0 <= x < width and 0 <= y < height:
                    dst[x, y] = color
    return output


def checkerboard(size: tuple[int, int], cell: int = 8) -> Image.Image:
    panel = Image.new("RGBA", size, (8, 15, 26, 255))
    draw = ImageDraw.Draw(panel)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            fill = (18, 31, 49, 255) if (x // cell + y // cell) % 2 else (10, 21, 36, 255)
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=fill)
    return panel


def preview_frames(frames: list[Image.Image], label: str) -> list[Image.Image]:
    max_w = max(frame.width for frame in frames)
    max_h = max(frame.height for frame in frames)
    scale = max(1, min(3, 640 // max_w, 640 // max_h))
    result: list[Image.Image] = []
    for index, frame in enumerate(frames):
        panel = checkerboard((max_w, max_h + 18))
        panel.alpha_composite(frame, ((max_w - frame.width) // 2, 18 + (max_h - frame.height) // 2))
        ImageDraw.Draw(panel).text((4, 3), f"{label}  {index + 1}/{len(frames)}", fill=(230, 240, 255, 255), font=FONT)
        result.append(panel.resize((panel.width * scale, panel.height * scale), Image.Resampling.NEAREST))
    return result


def save_gif(frames: list[Image.Image], path: Path) -> None:
    paletted = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=255) for frame in frames]
    paletted[0].save(path, save_all=True, append_images=paletted[1:], duration=110, loop=0, disposal=2, transparency=0)


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value)


def main() -> None:
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    definitions = manifest_static_damage()
    rows: list[dict[str, object]] = []
    generated: list[dict[str, object]] = []
    seen_cells: dict[tuple[int, ...], str] = {}
    aliases: list[dict[str, str]] = []
    for definition in definitions:
        key = str(definition["key"])
        cell_id = tuple(int(v) for v in definition["cell"])
        if cell_id in seen_cells:
            aliases.append({"alias": key, "candidate": seen_cells[cell_id]})
            continue
        damaged = crop(definition["cell"], definition.get("img"))
        intact = crop(definition["intactCell"], definition.get("intactImg"))
        if damaged.size != intact.size:
            rows.append({"key": key, "intact_key": definition["intactKey"], "status": "size_mismatch", "fire_pixels": 0, "smoke_pixels": 0})
            continue
        fire, smoke = classify_masks(damaged, intact)
        effect_pixels = len(fire) + len(smoke)
        if effect_pixels < 4:
            rows.append({"key": key, "intact_key": definition["intactKey"], "status": "no_high_confidence_fire_smoke", "fire_pixels": len(fire), "smoke_pixels": len(smoke)})
            continue
        name = safe_name(key)
        candidate_dir = CANDIDATES / name
        candidate_dir.mkdir(parents=True, exist_ok=True)
        frames = [animate_frame(damaged, intact, fire, smoke, index) for index in range(8)]
        for index, frame in enumerate(frames, start=1):
            frame.save(candidate_dir / f"{name}-{index:02d}.png")
        preview_path = PREVIEWS / f"{name}.gif"
        save_gif(preview_frames(frames, key), preview_path)
        seen_cells[cell_id] = key
        entry = {"key": key, "intact_key": definition["intactKey"], "status": "candidate_generated", "fire_pixels": len(fire), "smoke_pixels": len(smoke)}
        rows.append(entry)
        generated.append(entry)

    with (AUDIT / "static_damage_effect_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "intact_key", "status", "fire_pixels", "smoke_pixels"])
        writer.writeheader()
        writer.writerows(rows)
    with (AUDIT / "static_damage_aliases.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["alias", "candidate"])
        writer.writeheader()
        writer.writerows(aliases)

    cards = []
    for entry in generated:
        key = str(entry["key"])
        file_name = f"{safe_name(key)}.gif"
        cards.append(
            f'<article><img src="{html.escape(file_name)}" alt="{html.escape(key)}"><h2>{html.escape(key)}</h2>'
            f'<p>fire pixels: {entry["fire_pixels"]} · smoke pixels: {entry["smoke_pixels"]}</p></article>'
        )
    gallery = f"""<!doctype html><html><head><meta charset="utf-8"><title>Damage FX candidates</title>
<style>body{{margin:0;background:#070d17;color:#eaf2ff;font:14px system-ui}}header{{position:sticky;top:0;padding:16px;background:#08111fee;border-bottom:1px solid #28405f;z-index:2}}main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;padding:14px}}article{{background:#0d1929;border:1px solid #263e5c;border-radius:8px;padding:10px}}img{{display:block;max-width:100%;max-height:540px;margin:auto;image-rendering:pixelated}}h2{{font-size:13px;overflow-wrap:anywhere}}p{{color:#9fb5d0}}</style></head>
<body><header><strong>Static damage fire/smoke animation candidates</strong> · {len(generated)} unique cells · eight frames each · true effect-shape motion · no live wiring</header><main>{''.join(cards)}</main></body></html>"""
    (PREVIEWS / "index.html").write_text(gallery, encoding="utf-8")
    print(json.dumps({"manifest_damage_keys": len(definitions), "unique_candidates": len(generated), "aliases": len(aliases), "audit_rows": len(rows), "output": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
