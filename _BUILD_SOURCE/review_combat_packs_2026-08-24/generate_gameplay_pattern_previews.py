from __future__ import annotations

import html
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "CF_EnemyCombatSystems-Vol.2" / "Edited"
OUTPUT = ROOT / "gameplay_pattern_previews_v2"
GIF_DIR = OUTPUT / "gifs"
CONTACT_DIR = OUTPUT / "contact_sheets"

WIDTH = 640
HEIGHT = 480
FPS = 16
FRAME_MS = round(1000 / FPS)
WINDUP_MS = 250
PATTERN_MS = 2400
# The supplied VFX canvases are 192x192 but their visible projectiles are commonly ~158px tall.
# A 0.28 review scale yields a 40-45px visible round, matching the current boss-bullet draw band.
PROJECTILE_SCALE = 0.28
PLAYER_Y = 424


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


FONT_11 = font(11, True)
FONT_13 = font(13)
FONT_15 = font(15, True)
FONT_20 = font(20, True)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def alpha_crop(image: Image.Image) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    return image.crop(bbox) if bbox else image


def scaled_vfx(image: Image.Image, angle_from_down: float = 0.0) -> Image.Image:
    size = max(1, round(image.width * PROJECTILE_SCALE))
    image = image.resize((size, size), Image.Resampling.NEAREST)
    # VFX masters point upward; rotate that forward axis into the requested down-screen angle.
    image = image.rotate(180 + angle_from_down, resample=Image.Resampling.NEAREST, expand=True)
    return alpha_crop(image)


def paste_center(canvas: Image.Image, image: Image.Image, x: float, y: float) -> None:
    canvas.alpha_composite(image, (round(x - image.width / 2), round(y - image.height / 2)))


def make_background() -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (5, 12, 22, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, HEIGHT, 32):
        draw.line((0, y, WIDTH, y), fill=(17, 40, 62, 255), width=1)
    for x in range(0, WIDTH, 32):
        draw.line((x, 0, x, HEIGHT), fill=(13, 31, 50, 255), width=1)
    draw.rectangle((0, 383, WIDTH - 1, HEIGHT - 1), fill=(8, 22, 34, 255))
    draw.line((0, 383, WIDTH, 383), fill=(41, 118, 156, 255), width=2)
    draw.text((10, 389), "PLAYER MANEUVER ZONE", font=FONT_11, fill=(70, 175, 215, 255))
    return image


BACKGROUND = make_background()


def player_position(time_s: float, pattern_index: int) -> tuple[float, float]:
    phase = pattern_index * 0.85
    return WIDTH / 2 + math.sin(time_s * 1.55 + phase) * 112, PLAYER_Y


def draw_player_marker(canvas: Image.Image, x: float, y: float) -> None:
    draw = ImageDraw.Draw(canvas)
    color = (55, 221, 255, 255)
    glow = (20, 97, 130, 255)
    draw.ellipse((x - 20, y - 20, x + 20, y + 20), outline=glow, width=2)
    draw.line((x - 26, y, x - 10, y), fill=color, width=2)
    draw.line((x + 10, y, x + 26, y), fill=color, width=2)
    draw.line((x, y - 26, x, y - 10), fill=color, width=2)
    draw.line((x, y + 10, x, y + 26), fill=color, width=2)
    draw.polygon([(x, y - 12), (x - 9, y + 10), (x, y + 6), (x + 9, y + 10)], fill=(127, 237, 255, 255))


def enemy_motion(category: str, tier: str, time_s: float) -> tuple[float, float]:
    # Motion is deliberately restrained: the pack defines shooting but not movement AI.
    if category in {"ground", "hazard", "fortress"}:
        return WIDTH / 2, 0
    if tier == "boss" or category == "carrier":
        return WIDTH / 2 + math.sin(time_s * 0.8) * 12, 0
    if category in {"razor", "manta", "needle", "scout"}:
        return WIDTH / 2 + math.sin(time_s * 1.3) * 30, 0
    return WIDTH / 2 + math.sin(time_s * 0.9) * 18, 0


def event_angles(event: dict[str, Any], origin: tuple[float, float], target: tuple[float, float]) -> list[float]:
    count = max(1, int(event.get("count", 1)))
    spread = float(event.get("spread_degrees", 0))
    if event.get("aim") == "player":
        dx = target[0] - origin[0]
        dy = target[1] - origin[1]
        center = math.degrees(math.atan2(dx, dy))
    else:
        center = 0.0
    if count == 1:
        return [center]
    if spread >= 359:
        return [i * 360 / count for i in range(count)]
    if spread == 0:
        spread = min(18, 5 * (count - 1))
    start = center - spread / 2
    return [start + spread * i / (count - 1) for i in range(count)]


@dataclass
class Shot:
    spawn_ms: int
    x: float
    y: float
    angle: float
    speed: float
    family: str
    detonate_ms: int | None = None
    stationary: bool = False


def vfx_frames(family: str, cache: dict[str, list[Image.Image]]) -> list[Image.Image]:
    if family in cache:
        return cache[family]
    folder = SOURCE / f"vfx-{family}"
    json_path = folder / f"{family}.json"
    images: list[Image.Image] = []
    if json_path.exists():
        data = load_json(json_path)
        for name in data.get("frames", []):
            path = folder / f"{name}.png"
            if path.exists():
                images.append(load_rgba(path))
    cache[family] = images
    return images


def build_shots(pattern: dict[str, Any], anchors: dict[str, list[int]], enemy_x: float, player: tuple[float, float]) -> list[Shot]:
    shots: list[Shot] = []
    enemy_left = enemy_x - 128
    for event in pattern.get("events", []):
        anchor_name = event.get("anchor", "center")
        anchor = anchors.get(anchor_name) or next(iter(anchors.values()), [128, 192])
        origin = (enemy_left + anchor[0], anchor[1])
        family = event.get("projectile")
        if not family:
            continue
        event_time = WINDUP_MS + int(event.get("time_ms", 0)) + int(event.get("delay_ms", 0))
        if event.get("ring_radius_px"):
            count = max(1, int(event.get("count", 1)))
            radius = float(event["ring_radius_px"])
            for index in range(count):
                theta = math.tau * index / count
                shots.append(
                    Shot(event_time, origin[0] + math.cos(theta) * radius, origin[1] + math.sin(theta) * radius, 0, 0, family, stationary=True)
                )
            continue
        for angle in event_angles(event, origin, player):
            shots.append(
                Shot(
                    spawn_ms=event_time,
                    x=origin[0],
                    y=origin[1],
                    angle=angle,
                    speed=float(event.get("speed", 140)),
                    family=family,
                    detonate_ms=int(event["detonate_ms"]) if event.get("detonate_ms") is not None else None,
                )
            )
    return shots


def draw_hud(canvas: Image.Image, enemy: dict[str, Any], pattern: dict[str, Any], pattern_index: int) -> None:
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH, 70), fill=(3, 9, 16, 228))
    draw.text((12, 9), enemy.get("display_name", enemy["asset"]).upper(), font=FONT_20, fill=(237, 246, 255, 255))
    draw.text((13, 37), f"STAGE {enemy['stage']}  •  {enemy.get('tier', '').upper()}  •  {enemy.get('category', '').upper()}", font=FONT_11, fill=(70, 210, 255, 255))
    pattern_name = pattern.get("id", "pattern").removeprefix(enemy["asset"] + "-").replace("-", " ").upper()
    draw.text((WIDTH - 12, 10), f"PATTERN {pattern_index + 1}/4", font=FONT_11, fill=(255, 188, 55, 255), anchor="ra")
    draw.text((WIDTH - 12, 29), pattern_name, font=FONT_15, fill=(255, 234, 188, 255), anchor="ra")
    cooldown = pattern.get("cooldown_ms")
    gate = pattern.get("health_gate")
    detail = f"COOLDOWN {cooldown / 1000:.2f}s" if cooldown else ""
    if gate is not None:
        detail += f"  •  BELOW {round(float(gate) * 100)}% HP"
    draw.text((WIDTH - 12, 51), detail, font=FONT_11, fill=(182, 199, 218, 255), anchor="ra")
    draw.rectangle((0, HEIGHT - 24, WIDTH, HEIGHT), fill=(3, 9, 16, 235))
    draw.text((10, HEIGHT - 19), "AUTHORED FIRING JSON • SINGLE-FLASH INTERPRETATION • REVIEW ONLY — NOT WIRED", font=FONT_11, fill=(255, 120, 128, 255))


def render_pattern(
    enemy: dict[str, Any],
    folder: Path,
    pattern: dict[str, Any],
    pattern_index: int,
    cache: dict[str, list[Image.Image]],
) -> tuple[list[Image.Image], Image.Image]:
    attack_frames = [load_rgba(path) for path in sorted(folder.glob(f"{enemy['asset']}-attack-*.png"))]
    intact_path = folder / f"{enemy['asset']}-intact.png"
    intact = load_rgba(intact_path) if intact_path.exists() else attack_frames[0]
    impact_family = enemy.get("vfx", {}).get("impact")
    total_frames = math.ceil(PATTERN_MS / FRAME_MS)
    frames: list[Image.Image] = []
    representative: Image.Image | None = None
    for frame_index in range(total_frames):
        now_ms = frame_index * FRAME_MS
        time_s = now_ms / 1000
        enemy_x, enemy_y = enemy_motion(enemy.get("category", ""), enemy.get("tier", ""), time_s)
        player = player_position(time_s, pattern_index)
        shots = build_shots(pattern, enemy.get("weapon_anchors_px", {}), enemy_x, player)
        canvas = BACKGROUND.copy()
        draw_player_marker(canvas, *player)

        if attack_frames and WINDUP_MS <= now_ms < WINDUP_MS + round(len(attack_frames) / 12 * 1000):
            attack_elapsed = (now_ms - WINDUP_MS) / 1000
            sprite = attack_frames[min(len(attack_frames) - 1, int(attack_elapsed * 12))]
        else:
            sprite = intact
        canvas.alpha_composite(sprite, (round(enemy_x - 128), round(enemy_y)))

        for shot in shots:
            age_ms = now_ms - shot.spawn_ms
            if age_ms < 0:
                continue
            age_s = age_ms / 1000
            dx = math.sin(math.radians(shot.angle))
            dy = math.cos(math.radians(shot.angle))
            x = shot.x if shot.stationary else shot.x + dx * shot.speed * age_s
            y = shot.y if shot.stationary else shot.y + dy * shot.speed * age_s
            detonated = shot.detonate_ms is not None and age_ms >= shot.detonate_ms
            if detonated and impact_family:
                images = vfx_frames(impact_family, cache)
                impact_age = age_ms - shot.detonate_ms
                if images and impact_age < 600:
                    image = images[min(len(images) - 1, int(impact_age / 1000 * 12) % len(images))]
                    image = alpha_crop(image.resize((86, 86), Image.Resampling.NEAREST))
                    paste_center(canvas, image, x, y)
                continue
            images = vfx_frames(shot.family, cache)
            if not images:
                continue
            image = images[int(age_s * 12) % len(images)]
            image = scaled_vfx(image, shot.angle)
            paste_center(canvas, image, x, y)

        draw_hud(canvas, enemy, pattern, pattern_index)
        opaque = canvas.convert("RGB")
        frames.append(opaque)
        if representative is None and now_ms >= 900:
            representative = opaque.copy()
    return frames, representative or frames[len(frames) // 2].copy()


def save_gif(frames: list[Image.Image], path: Path) -> None:
    palette_frames = [
        frame.quantize(colors=160, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        for frame in frames
    ]
    palette_frames[0].save(
        path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )


def make_contact(stage: int, cards: list[tuple[dict[str, Any], dict[str, Any], Image.Image]]) -> Path:
    cell_w, cell_h = 320, 240
    columns = 4
    rows = math.ceil(len(cards) / columns)
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), (5, 12, 22))
    draw = ImageDraw.Draw(sheet)
    for index, (enemy, pattern, image) in enumerate(cards):
        x = (index % columns) * cell_w
        y = (index // columns) * cell_h
        thumb = image.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), outline=(28, 74, 105), width=2)
        draw.rectangle((x, y + cell_h - 38, x + cell_w, y + cell_h), fill=(2, 8, 15))
        label = enemy.get("display_name", enemy["asset"])
        pattern_label = pattern.get("id", "").removeprefix(enemy["asset"] + "-").replace("-", " ")
        draw.text((x + 8, y + cell_h - 34), label.upper(), font=FONT_11, fill=(235, 246, 255))
        draw.text((x + 8, y + cell_h - 18), pattern_label.upper(), font=FONT_11, fill=(68, 203, 255))
    path = CONTACT_DIR / f"stage-{stage}-pattern-contact.png"
    sheet.save(path)
    return path


def write_index(records: list[dict[str, Any]], contacts: dict[int, str]) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["asset"]].append(record)
    cards = []
    for asset, items in grouped.items():
        enemy = items[0]
        gifs = "".join(
            f'<figure><img src="{html.escape(item["gif"])}" alt="{html.escape(item["pattern"])}" loading="lazy"><figcaption>{html.escape(item["pattern_label"])}</figcaption></figure>'
            for item in items
        )
        cards.append(
            f'<section class="enemy" data-stage="{enemy["stage"]}"><header><h2>{html.escape(enemy["display_name"])}</h2><span>Stage {enemy["stage"]} · {html.escape(enemy["tier"])} · {html.escape(enemy["category"])}</span></header><div class="patterns">{gifs}</div></section>'
        )
    contact_html = "".join(
        f'<a href="{html.escape(path)}"><img src="{html.escape(path)}" alt="Stage {stage} contact sheet"><b>Stage {stage}</b></a>'
        for stage, path in sorted(contacts.items())
    )
    document = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF Enemy Pattern GIF Review</title><style>
:root{{--bg:#050c16;--panel:#0b1929;--line:#1b4260;--cyan:#4edcff;--text:#edf7ff;--muted:#9bb2c6;--red:#ff6672}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 system-ui,Segoe UI,sans-serif}}main{{max-width:1600px;margin:auto;padding:28px}}h1{{font-size:42px;margin:.15em 0}}.hold{{color:#fff;background:#7a202b;border:1px solid var(--red);padding:7px 12px;border-radius:99px;font-weight:800}}.lead{{color:var(--muted);max-width:1000px;font-size:17px}}.contacts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin:28px 0}}.contacts a{{color:var(--cyan);text-decoration:none;background:var(--panel);border:1px solid var(--line);padding:8px}}.contacts img{{width:100%;height:170px;object-fit:cover;object-position:top}}.enemy{{border:1px solid var(--line);background:var(--panel);margin:22px 0;padding:14px;border-radius:12px}}.enemy header{{display:flex;justify-content:space-between;align-items:baseline;gap:20px}}.enemy h2{{margin:0;color:var(--cyan)}}.enemy header span{{color:var(--muted);text-transform:uppercase;font-size:12px}}.patterns{{display:grid;grid-template-columns:repeat(2,minmax(300px,1fr));gap:12px;margin-top:12px}}figure{{margin:0;background:#02070c;border:1px solid #18334c}}figure img{{width:100%;height:auto;display:block}}figcaption{{padding:8px 10px;color:#ffd287;text-transform:uppercase;font-weight:700}}@media(max-width:800px){{.patterns{{grid-template-columns:1fr}}.enemy header{{display:block}}}}
</style></head><body><main><span class="hold">REVIEW ONLY — NOT WIRED</span><h1>Enemy Attack Pattern GIFs</h1><p class="lead">Each GIF is a 640×480 neutral gameplay simulation built from the supplied eight-frame attack reel, fixed weapon anchors, actual projectile family, speeds, counts, spreads, and event timing. A 250 ms visual wind-up aligns projectile emission to attack frame 4. Separate muzzle VFX are suppressed because the supplied attack reels already bake in flashes. Movement is deliberately minimal because these JSON files do not define movement AI.</p><div class="contacts">{contact_html}</div>{''.join(cards)}</main></body></html>"""
    (OUTPUT / "index.html").write_text(document, encoding="utf-8")


def main() -> None:
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    CONTACT_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    contact_cards: dict[int, list[tuple[dict[str, Any], dict[str, Any], Image.Image]]] = defaultdict(list)
    cache: dict[str, list[Image.Image]] = {}
    folders = sorted(path for path in SOURCE.iterdir() if path.is_dir() and not path.name.startswith("vfx-"))
    for enemy_index, folder in enumerate(folders, 1):
        json_path = folder / f"{folder.name}-combat.json"
        if not json_path.exists():
            continue
        enemy = load_json(json_path)
        patterns = enemy.get("attack_patterns", [])
        print(f"[{enemy_index:02}/{len(folders):02}] {enemy['asset']} ({len(patterns)} patterns)", flush=True)
        for pattern_index, pattern in enumerate(patterns):
            frames, representative = render_pattern(enemy, folder, pattern, pattern_index, cache)
            gif_name = f"{enemy['asset']}--{pattern['id'].removeprefix(enemy['asset'] + '-')}.gif"
            gif_path = GIF_DIR / gif_name
            save_gif(frames, gif_path)
            pattern_label = pattern["id"].removeprefix(enemy["asset"] + "-").replace("-", " ")
            records.append(
                {
                    "asset": enemy["asset"],
                    "display_name": enemy.get("display_name", enemy["asset"]),
                    "stage": enemy.get("stage"),
                    "tier": enemy.get("tier", ""),
                    "category": enemy.get("category", ""),
                    "pattern": pattern["id"],
                    "pattern_label": pattern_label,
                    "gif": f"gifs/{gif_name}",
                    "fps": FPS,
                    "duration_ms": PATTERN_MS,
                    "windup_ms": WINDUP_MS,
                }
            )
            contact_cards[int(enemy["stage"])].append((enemy, pattern, representative))
    contacts = {
        stage: make_contact(stage, cards).relative_to(OUTPUT).as_posix()
        for stage, cards in sorted(contact_cards.items())
    }
    (OUTPUT / "preview_manifest.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    write_index(records, contacts)
    notes = f"""# Enemy attack pattern previews

- {len(records)} individual 640×480 GIFs at {FPS} fps.
- Review artifacts only; nothing is wired into the game.
- Uses each combatant's supplied attack frames, weapon anchors, projectile art, counts, spreads, speeds, and event timing.
- Adds a {WINDUP_MS} ms offset so pattern time zero aligns with attack frame 4 instead of firing before the visual telegraph.
- Suppresses independent muzzle VFX because the attack frames already contain baked muzzle flashes.
- Uses minimal category-based drift only to keep the firing origin readable. The combat JSON does not define movement AI.
- Player marker moves laterally to make aimed bursts visibly track a target.
"""
    (OUTPUT / "README.md").write_text(notes, encoding="utf-8")
    total_bytes = sum(path.stat().st_size for path in GIF_DIR.glob("*.gif"))
    print(f"DONE: {len(records)} GIFs, {total_bytes / 1024 / 1024:.1f} MiB", flush=True)


if __name__ == "__main__":
    main()
