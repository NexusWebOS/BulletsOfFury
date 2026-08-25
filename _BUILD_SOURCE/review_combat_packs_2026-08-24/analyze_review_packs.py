from __future__ import annotations

import csv
import hashlib
import html
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parent
V1 = ROOT / "CF_EnemyCombatPatterns-Vol.1"
V2 = ROOT / "CF_EnemyCombatSystems-Vol.2" / "Edited"
CARRIER = ROOT / "CF_DoomsdayCarrierAttacks-Lvl6" / "Edited"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def alpha_metrics(path: Path) -> dict[str, Any]:
    with Image.open(path) as source:
        image = source.convert("RGBA")
        alpha = image.getchannel("A")
        colors = alpha.getcolors(maxcolors=256) or []
        alpha_values = {value for _, value in colors}
        bbox = alpha.getbbox()
        width, height = image.size
        occupied = sum(count for count, value in colors if value > 0)
        semitransparent = sum(count for count, value in colors if 0 < value < 255)
        touches = []
        if bbox:
            if bbox[0] == 0:
                touches.append("left")
            if bbox[1] == 0:
                touches.append("top")
            if bbox[2] == width:
                touches.append("right")
            if bbox[3] == height:
                touches.append("bottom")
        magenta = sum(
            1
            for red, green, blue, a in image.getdata()
            if a and red == 255 and green == 0 and blue == 255
        )
        return {
            "size": [width, height],
            "bbox": list(bbox) if bbox else None,
            "occupied": occupied,
            "occupied_ratio": round(occupied / (width * height), 6),
            "binary_alpha": alpha_values.issubset({0, 255}),
            "semitransparent_pixels": semitransparent,
            "border_touches": touches,
            "magenta_pixels": magenta,
        }


def nearest_alpha_distance(path: Path, point: tuple[int, int]) -> float | None:
    with Image.open(path) as source:
        alpha = source.convert("RGBA").getchannel("A")
        bbox = alpha.getbbox()
        if not bbox:
            return None
        px = alpha.load()
        x0 = max(0, point[0] - 20)
        x1 = min(alpha.width, point[0] + 21)
        y0 = max(0, point[1] - 20)
        y1 = min(alpha.height, point[1] + 21)
        best = math.inf
        for y in range(y0, y1):
            for x in range(x0, x1):
                if px[x, y] > 0:
                    best = min(best, math.hypot(x - point[0], y - point[1]))
        return None if best == math.inf else round(best, 2)


def image_difference_ratio(first: Path, second: Path) -> float:
    with Image.open(first) as a_source, Image.open(second) as b_source:
        a = a_source.convert("RGBA")
        b = b_source.convert("RGBA")
        if a.size != b.size:
            return 1.0
        diff = ImageChops.difference(a, b)
        bbox = diff.getbbox()
        if not bbox:
            return 0.0
        changed = sum(1 for pixel in diff.getdata() if pixel != (0, 0, 0, 0))
        return round(changed / (a.width * a.height), 6)


def canonical_pattern_set(data: dict[str, Any]) -> str:
    patterns = data.get("attack_patterns", [])
    normalized = []
    for pattern in patterns:
        item = dict(pattern)
        item.pop("id", None)
        events = []
        for event in item.get("events", []):
            event = dict(event)
            projectile = event.get("projectile")
            if projectile:
                event["projectile"] = projectile.rsplit("-", 1)[-1]
            events.append(event)
        item["events"] = events
        normalized.append(item)
    raw = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def analyze_v1() -> dict[str, Any]:
    rows = []
    signatures: dict[str, list[str]] = defaultdict(list)
    all_json = sorted(V1.glob("Level-*/Metadata/*/*combat.json"))
    for path in all_json:
        data = load_json(path)
        if not data.get("category"):
            continue
        signature = canonical_pattern_set(data)
        signatures[signature].append(data["asset"])
        rows.append(
            {
                "asset": data["asset"],
                "stage": data.get("stage"),
                "category": data.get("category"),
                "weapon_profile": data.get("weapon_profile"),
                "anchors": data.get("weapon_anchors_px", {}),
                "patterns": data.get("attack_patterns", []),
                "pattern_signature": signature,
                "source": relative(path),
            }
        )
    duplicate_groups = [members for members in signatures.values() if len(members) > 1]
    return {
        "count": len(rows),
        "stages": dict(sorted(Counter(row["stage"] for row in rows).items())),
        "categories": dict(Counter(row["category"] for row in rows).most_common()),
        "weapon_profiles": dict(Counter(row["weapon_profile"] for row in rows).most_common()),
        "unique_pattern_sets": len(signatures),
        "duplicate_pattern_groups": duplicate_groups,
        "rows": rows,
    }


def analyze_v2() -> dict[str, Any]:
    rows = []
    all_png_metrics = []
    for folder in sorted(path for path in V2.iterdir() if path.is_dir() and not path.name.startswith("vfx-")):
        json_path = folder / f"{folder.name}-combat.json"
        if not json_path.exists():
            continue
        data = load_json(json_path)
        png_files = sorted(folder.glob("*.png"))
        frame_files = [
            path
            for path in png_files
            if "atlas" not in path.name and path.name != f"{folder.name}-intact.png"
        ]
        metrics = {path.name: alpha_metrics(path) for path in frame_files}
        all_png_metrics.extend(metrics.values())
        attack = sorted(folder.glob(f"{folder.name}-attack-*.png"))
        death = sorted(folder.glob(f"{folder.name}-death-*.png"))
        anchors = data.get("weapon_anchors_px", {})
        attack_anchor_distances = {}
        if len(attack) >= 4:
            for name, coords in anchors.items():
                attack_anchor_distances[name] = nearest_alpha_distance(
                    attack[3], (int(coords[0]), int(coords[1]))
                )
        death_coverage = [metrics[path.name]["occupied_ratio"] for path in death if path.name in metrics]
        death_loss = None
        if death_coverage and death_coverage[0]:
            death_loss = round(1 - death_coverage[-1] / death_coverage[0], 4)
        attack_change = None
        if len(attack) >= 4:
            attack_change = image_difference_ratio(attack[0], attack[3])
        preview = folder / f"{folder.name}-preview.gif"
        rows.append(
            {
                "asset": data["asset"],
                "display_name": data.get("display_name", data["asset"]),
                "stage": data.get("stage"),
                "category": data.get("category"),
                "tier": data.get("tier"),
                "states": data.get("states", []),
                "anchors": anchors,
                "anchor_distance_at_spawn_frame": attack_anchor_distances,
                "vfx": data.get("vfx", {}),
                "patterns": data.get("attack_patterns", []),
                "pattern_signature": canonical_pattern_set(data),
                "frame_count": len(frame_files),
                "attack_frame_count": len(attack),
                "death_frame_count": len(death),
                "attack_frame_1_to_4_change_ratio": attack_change,
                "death_final_coverage_loss": death_loss,
                "binary_alpha": all(item["binary_alpha"] for item in metrics.values()),
                "semitransparent_pixels": sum(item["semitransparent_pixels"] for item in metrics.values()),
                "magenta_pixels": sum(item["magenta_pixels"] for item in metrics.values()),
                "border_touching_frames": [name for name, item in metrics.items() if item["border_touches"]],
                "preview": relative(preview) if preview.exists() else None,
                "source": relative(json_path),
            }
        )
    signatures: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        signatures[row["pattern_signature"]].append(row["asset"])
    duplicate_groups = [members for members in signatures.values() if len(members) > 1]
    return {
        "count": len(rows),
        "stages": dict(sorted(Counter(row["stage"] for row in rows).items())),
        "categories": dict(Counter(row["category"] for row in rows).most_common()),
        "tiers": dict(Counter(row["tier"] for row in rows).most_common()),
        "unique_pattern_sets": len(signatures),
        "duplicate_pattern_groups": duplicate_groups,
        "png_binary_alpha": all(item["binary_alpha"] for item in all_png_metrics),
        "semitransparent_pixels": sum(item["semitransparent_pixels"] for item in all_png_metrics),
        "magenta_pixels": sum(item["magenta_pixels"] for item in all_png_metrics),
        "border_touching_frame_count": sum(bool(item["border_touches"]) for item in all_png_metrics),
        "rows": rows,
    }


def analyze_v2_vfx() -> dict[str, Any]:
    rows = []
    for folder in sorted(path for path in V2.iterdir() if path.is_dir() and path.name.startswith("vfx-")):
        json_files = list(folder.glob("*.json"))
        data = load_json(json_files[0]) if json_files else {}
        frames = sorted(path for path in folder.glob("*.png") if "atlas" not in path.name)
        metrics = [alpha_metrics(path) for path in frames]
        previews = list(folder.glob("*preview.gif"))
        rows.append(
            {
                "asset": data.get("asset", folder.name.removeprefix("vfx-")),
                "role": data.get("role") or data.get("category"),
                "frame_count": len(frames),
                "binary_alpha": all(item["binary_alpha"] for item in metrics),
                "border_touching_frames": sum(bool(item["border_touches"]) for item in metrics),
                "preview": relative(previews[0]) if previews else None,
            }
        )
    return {"count": len(rows), "rows": rows}


def analyze_carrier() -> dict[str, Any]:
    patterns_path = CARRIER / "CF_DoomsdayCarrierAttackPatterns-Lvl6.json"
    data = load_json(patterns_path)
    rows = []
    for pattern in data.get("patterns", []):
        animation = CARRIER / "Master Edit" / f"{pattern['boss_animation']}-preview.gif"
        rows.append(
            {
                **pattern,
                "preview": relative(animation) if animation.exists() else None,
            }
        )
    frame_metrics = []
    for path in sorted((CARRIER / "Master Edit").glob("boss-*_f*-boss_*.png")):
        metrics = alpha_metrics(path)
        metrics["file"] = relative(path)
        frame_metrics.append(metrics)
    return {
        "anchors": data.get("anchors", {}),
        "patterns": rows,
        "boss_frame_count": len(frame_metrics),
        "binary_alpha": all(item["binary_alpha"] for item in frame_metrics),
        "semitransparent_pixels": sum(item["semitransparent_pixels"] for item in frame_metrics),
        "magenta_pixels": sum(item["magenta_pixels"] for item in frame_metrics),
        "border_touching_frames": [item["file"] for item in frame_metrics if item["border_touches"]],
    }


def write_catalog(summary: dict[str, Any]) -> None:
    path = ROOT / "combat_catalog.csv"
    fieldnames = [
        "pack",
        "asset",
        "stage",
        "category",
        "tier",
        "weapon_profile",
        "pattern_count",
        "pattern_ids",
        "preview",
        "review_flags",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary["volume_1"]["rows"]:
            writer.writerow(
                {
                    "pack": "volume_1_patterns",
                    "asset": row["asset"],
                    "stage": row["stage"],
                    "category": row["category"],
                    "weapon_profile": row["weapon_profile"],
                    "pattern_count": len(row["patterns"]),
                    "pattern_ids": " | ".join(pattern["id"] for pattern in row["patterns"]),
                    "review_flags": "metadata only; per-enemy runtime frames absent",
                }
            )
        for row in summary["volume_2"]["rows"]:
            flags = []
            if row["death_final_coverage_loss"] is not None and row["death_final_coverage_loss"] > 0.65:
                flags.append("death dissolves/fades")
            if row["border_touching_frames"]:
                flags.append("frame touches canvas border")
            if row["semitransparent_pixels"]:
                flags.append("non-binary alpha")
            writer.writerow(
                {
                    "pack": "volume_2_systems",
                    "asset": row["asset"],
                    "stage": row["stage"],
                    "category": row["category"],
                    "tier": row["tier"],
                    "pattern_count": len(row["patterns"]),
                    "pattern_ids": " | ".join(pattern["id"] for pattern in row["patterns"]),
                    "preview": row["preview"],
                    "review_flags": "; ".join(flags),
                }
            )


def pattern_summary(pattern: dict[str, Any]) -> str:
    parts = [pattern.get("id", "unnamed")]
    if pattern.get("cooldown_ms") is not None:
        parts.append(f"{pattern['cooldown_ms']} ms cooldown")
    if pattern.get("health_gate") is not None:
        parts.append(f"below {round(float(pattern['health_gate']) * 100)}% HP")
    events = pattern.get("events", [])
    if events:
        parts.append(f"{len(events)} event{'s' if len(events) != 1 else ''}")
    return " · ".join(parts)


def write_html(summary: dict[str, Any]) -> None:
    v1 = summary["volume_1"]
    v2 = summary["volume_2"]
    carrier = summary["doomsday_carrier"]

    def img(path: str | None, alt: str, class_name: str = "preview") -> str:
        if not path:
            return '<div class="missing">No preview supplied</div>'
        return f'<img class="{class_name}" src="{html.escape(path)}" alt="{html.escape(alt)}" loading="lazy">'

    stage_cards = []
    stage_names = {
        1: "Jungle Assault",
        2: "Volcanic Depths",
        3: "Frozen Stronghold",
        4: "Blacksite Air War",
        5: "Orbital Chaos",
        6: "Heavy Turbulence",
        7: "Toxic Sewer",
        8: "Furious Death",
        9: "Warp Galaxy",
    }
    for stage in range(1, 10):
        preview = f"CF_EnemyCombatPatterns-Vol.1/Level-{stage}/Documentation/CF_EnemyCombatSystems-Lvl{stage}-preview.gif"
        stage_cards.append(
            f"<article><h3>Stage {stage}: {stage_names[stage]}</h3>{img(preview, f'Stage {stage} overview')}"
            f"<p>{v1['stages'].get(str(stage), v1['stages'].get(stage, 0))} enemy definitions. "
            "This is an overview reel only; individual runtime frames were not supplied in these five ZIPs.</p></article>"
        )

    enemy_cards = []
    for row in v2["rows"]:
        flags = []
        if row["death_final_coverage_loss"] is not None and row["death_final_coverage_loss"] > 0.65:
            flags.append(f"death loses {row['death_final_coverage_loss']:.0%} silhouette coverage")
        if row["border_touching_frames"]:
            flags.append(f"{len(row['border_touching_frames'])} frame(s) touch canvas edge")
        if row["vfx"].get("muzzle") and row["attack_frame_1_to_4_change_ratio"]:
            flags.append("baked firing flash plus separate muzzle VFX reference")
        flag_html = "".join(f'<li class="warn">{html.escape(flag)}</li>' for flag in flags) or '<li class="ok">No automated geometry blocker</li>'
        patterns = "".join(f"<li>{html.escape(pattern_summary(pattern))}</li>" for pattern in row["patterns"])
        enemy_cards.append(
            f"<article id=\"{html.escape(row['asset'])}\"><div class=\"eyebrow\">Stage {row['stage']} · {html.escape(str(row['tier']))} · {html.escape(str(row['category']))}</div>"
            f"<h3>{html.escape(row['display_name'])}</h3>{img(row['preview'], row['display_name'])}"
            f"<p><b>Anchors:</b> {html.escape(json.dumps(row['anchors'], separators=(',', ':')))}</p>"
            f"<p><b>VFX:</b> {html.escape(json.dumps(row['vfx'], separators=(',', ':')))}</p>"
            f"<ul>{patterns}</ul><ul>{flag_html}</ul></article>"
        )

    vfx_cards = []
    for row in summary["volume_2_vfx"]["rows"]:
        vfx_cards.append(
            f"<article><h3>{html.escape(row['asset'])}</h3>{img(row['preview'], row['asset'])}"
            f"<p>{row['frame_count']} standalone frames · role: {html.escape(str(row['role']))}</p></article>"
        )

    carrier_cards = []
    for pattern in carrier["patterns"]:
        carrier_cards.append(
            f"<article><div class=\"eyebrow\">Phase {pattern.get('phase')} · {pattern.get('telegraph_ms')} ms telegraph · {pattern.get('cycle_ms')} ms cycle</div>"
            f"<h3>{html.escape(pattern['id'].replace('_', ' ').title())}</h3>{img(pattern['preview'], pattern['id'])}"
            f"<p>{html.escape(pattern.get('behavior', ''))}</p></article>"
        )

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bullets of Fury Combat Pack Review</title>
<style>
:root{{--bg:#07101b;--panel:#0c1828;--line:#1e3854;--text:#eaf3ff;--muted:#9fb3ca;--cyan:#41d8ff;--amber:#ffbd3f;--red:#ff5f6d;--green:#5bea9b}}
*{{box-sizing:border-box}} body{{margin:0;background:linear-gradient(#050b13,#07101b 38rem);color:var(--text);font:15px/1.5 system-ui,Segoe UI,sans-serif}}
header,main{{max-width:1500px;margin:auto;padding:28px}} h1{{font-size:clamp(28px,5vw,56px);line-height:1;margin:.2em 0}} h2{{font-size:28px;margin:54px 0 14px;color:var(--cyan)}} h3{{margin:.25rem 0 .75rem;font-size:18px}} p{{color:var(--muted)}} .lead{{font-size:18px;max-width:1000px}} .hold{{display:inline-block;border:1px solid var(--red);color:#fff;background:#7b1f2a;padding:8px 14px;border-radius:999px;font-weight:800;letter-spacing:.05em}}
.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:25px 0}} .summary div{{background:var(--panel);border:1px solid var(--line);padding:18px;border-radius:12px}} .summary b{{display:block;font-size:28px;color:var(--amber)}}
.callout{{border-left:5px solid var(--amber);background:#151b22;padding:16px 20px;margin:18px 0}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:15px}} article{{background:linear-gradient(145deg,#0d1b2c,#091321);border:1px solid var(--line);border-radius:12px;padding:14px;overflow:hidden}} .preview{{width:100%;height:280px;object-fit:contain;background-image:linear-gradient(45deg,#122238 25%,transparent 25%),linear-gradient(-45deg,#122238 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#122238 75%),linear-gradient(-45deg,transparent 75%,#122238 75%);background-size:24px 24px;background-position:0 0,0 12px,12px -12px,-12px 0}} .wide{{width:100%;height:auto;max-height:1200px;object-fit:contain}} .eyebrow{{color:var(--cyan);font-size:12px;text-transform:uppercase;font-weight:800;letter-spacing:.08em}} ul{{padding-left:20px}} .warn{{color:#ffd0d5}} .ok{{color:var(--green)}} .missing{{height:180px;display:grid;place-items:center;color:var(--red);border:1px dashed var(--red)}} nav a{{color:var(--cyan);margin-right:18px}} code{{color:#d9f8ff}} footer{{padding:50px 0;color:var(--muted)}}
</style>
</head>
<body><header>
<span class="hold">HOLD — REVIEW ONLY, NOTHING WIRED</span>
<h1>Enemy Combat Pack Review</h1>
<p class="lead">Visual and behavior audit of the five supplied ColeForge ZIPs. The extracted files live only under <code>_BUILD_SOURCE</code>; live game code, manifests, and shipping assets were not changed.</p>
<nav><a href="#decision">Decision</a><a href="#carrier">Doomsday Carrier</a><a href="#volume2">Volume 2</a><a href="#vfx">VFX</a><a href="#volume1">Volume 1</a></nav>
<div class="summary"><div><b>{v1['count']}</b>Volume 1 enemy JSONs</div><div><b>{v2['count']}</b>Volume 2 combatants</div><div><b>{summary['volume_2_vfx']['count']}</b>Volume 2 VFX families</div><div><b>{len(carrier['patterns'])}</b>Carrier attack patterns</div></div>
</header><main>
<section id="decision"><h2>Current decision</h2>
<div class="callout"><b>Do not wire the enemy packs yet.</b> Volume 1 has only {v1['unique_pattern_sets']} distinct behavior sets across {v1['count']} enemies, and the supplied ZIPs omit its individual runtime frames. Volume 2 has only {v2['unique_pattern_sets']} distinct behavior sets across {v2['count']} combatants; several large families are exact behavioral duplicates. Its firing reels also contain baked flashes while their JSON references separate muzzle VFX, and 39 of 48 death reels lose more than 65% of their silhouette coverage through a dissolve-style ending.</div>
<p>The Doomsday Carrier art is the strongest candidate: its 640×320 origin matches the current Stage 6 boss and all 98 boss-cycle frames pass binary-alpha, magenta-key, and border checks. Its logic still needs explicit fragment lifetime, storm-link collision rules, Omega reflection rules, and a timed event list for the final fusion attack.</p>
</section>
<section id="carrier"><h2>Doomsday Carrier Mk II — six proposed attacks</h2><div class="grid">{''.join(carrier_cards)}</div></section>
<section id="volume2"><h2>Volume 2 — 48 combatant previews</h2><img class="wide" src="CF_EnemyCombatSystems-Vol.2/Documentation/CF_EnemyCombatSystems-Vol.2-contact.png" alt="Volume 2 combatant contact sheet"><div class="grid">{''.join(enemy_cards)}</div></section>
<section id="vfx"><h2>Volume 2 — projectile, muzzle and impact previews</h2><img class="wide" src="CF_EnemyCombatSystems-Vol.2/Documentation/CF_EnemyCombatSystems-Vol.2-vfx-contact.png" alt="Volume 2 VFX contact sheet"><div class="grid">{''.join(vfx_cards)}</div></section>
<section id="volume1"><h2>Volume 1 — stage overview previews</h2><img class="wide" src="CF_EnemyCombatPatterns-Vol.1/Master/CF_EnemyCombatSystems-Vol.1-contact.png" alt="Volume 1 stage contact sheet"><div class="grid">{''.join(stage_cards)}</div></section>
<footer>Generated from the extracted review copies. GIFs are previews only and are not runtime masters.</footer>
</main></body></html>"""
    (ROOT / "review_gallery.html").write_text(document, encoding="utf-8")


def write_markdown(summary: dict[str, Any]) -> None:
    v1 = summary["volume_1"]
    v2 = summary["volume_2"]
    carrier = summary["doomsday_carrier"]
    faded = [row for row in v2["rows"] if row["death_final_coverage_loss"] is not None and row["death_final_coverage_loss"] > 0.65]
    borders = [row for row in v2["rows"] if row["border_touching_frames"]]
    text = f"""# Combat pack review — no wiring performed

## Decision

The five supplied ZIPs are isolated in this review folder. Nothing was copied to `assets/game`, added to `assets/manifest.js`, or connected in `assets/game.js`.

- **Volume 1:** hold. It supplies {v1['count']} enemy behavior JSON files but only stage-level preview reels, not the per-enemy runtime frames needed for visual approval. It contains {v1['unique_pattern_sets']} unique pattern sets, so many enemies still behave identically.
- **Volume 2:** hold. It supplies {v2['count']} combatants and 32 VFX families with clean binary alpha, but only {v2['unique_pattern_sets']} unique pattern sets. Baked attack flashes conflict with separate muzzle references, {len(faded)} death reels end in a dissolve-style silhouette loss, and {len(borders)} combatants have at least one frame touching the canvas edge.
- **Doomsday Carrier Mk II:** conditional candidate. All 98 full-boss frames preserve the 640×320 origin, hard alpha, and safe borders. The six patterns are visually readable, but several gameplay rules are underspecified.

## How the supplied enemy system works

Each Volume 2 combatant has a six-frame 10 fps power loop, an eight-frame 12 fps firing reel, a four-frame hit reel, and an eight-frame death reel. JSON declares fixed weapon anchors and says projectiles spawn on firing frame 4. Four attack patterns are then selected: a basic aimed burst, a fan, a composite/signature volley, and a below-35%-HP rage volley.

That is a **firing system**, not a complete enemy behavior system. The JSON does not define entry formation, movement, retreat, strafing, dodging, player-zone limits, or safe-gap policy. The current game already owns those through its entry AI, roster-specific ticks, and `ENEMY_VOLLEY`; a later integration would need one clear owner for movement and one for shooting to avoid double-firing.

## Blocking findings

1. **Behavior duplication:** {v1['count']} Volume 1 enemies collapse to {v1['unique_pattern_sets']} firing sets; {v2['count']} Volume 2 combatants collapse to {v2['unique_pattern_sets']}. The four Volume 2 fortress bosses share the same aimed burst, 54-degree fan, 104-degree secondary barrage, and 360-degree critical rage with only palette/projectile/speed changes. That does not meet the requirement that every enemy, miniboss, and boss behave differently.
2. **Firing timing conflict:** the reels declare projectile spawn on frame 4 (about 250 ms into a 12 fps animation), while many JSON pattern events begin at 0, 110, and 220 ms. The event clock needs an explicit relationship to the firing reel or projectiles will precede their muzzle flash.
3. **Double muzzle risk:** attack frames visibly bake muzzle bursts into the hull, yet every JSON also names a separate muzzle VFX. Choose baked port lighting or independent muzzle animation—not both.
4. **Dissolve deaths:** {len(faded)} of 48 death reels lose over 65% of initial silhouette coverage by the final frame, often through a repeating circular mask. Replace those with solid breakup/explosion frames and a hard removal after the final explosion; do not opacity-fade the hull.
5. **Canvas-edge risk:** 14 frames across {len(borders)} combatants touch an outer canvas edge. These need padding or inspection before atlasing to avoid clipping.
6. **Early-stage density:** several standard Stage 1 units receive 12-shot 360-degree critical rings; hazards receive 16-shot rage rings. That is too much shared omnidirectional pressure for early fodder and conflicts with the current Stage 1 projectile-volume tuning.
7. **Hazard identity:** ammo crates, fuel barrels, fuel tanks, and river mines share one four-pattern detonation kit and reference a military cannon muzzle. Their behavior should be proximity/fuse/chain-reaction driven without gun-style muzzle flashes.

## Doomsday Carrier attack explanation

- **Cyclone Barrage (phase 1):** alternates the two lower pods, firing six three-way fans over 1.28 seconds. Its 220 ms telegraph is the shortest and should be tested at gameplay scale.
- **Prism Crossfire (phase 1):** four upper barrels fire mirrored diagonal lanes three times, reversing the cross angle on the middle volley.
- **Omega Bomb Run (phase 2):** both bays release reflectable bombs after a 720 ms warning. The pack needs explicit deflection input/window, reflected speed/damage, fuse behavior after reflection, and boss-hit result.
- **Chrome Flak Fan (phase 2):** alternating lower cannons fire four timed airburst shells. The JSON specifies five child angles but not child speed, collision size, or lifetime.
- **Storm Cage (phase 2):** four nodes deploy into the lower field and link into a rotating-gap enclosure. Link thickness, damage cadence, activation telegraph, and safe-gap width are missing.
- **Doomsday Fusion (phase 3):** combines bomb corridors, cyclone tracers, prism pressure, and the central beam. It has only a prose description—no deterministic event timeline—so it cannot yet be wired faithfully.

## Approval path

1. Approve/reject the six Carrier visuals individually.
2. Redesign the four fortress bosses and elite/miniboss families so each has a distinct fight mechanic, not a recolored shared template.
3. Replace dissolve deaths and decide whether firing flashes are baked or separate.
4. Supply the nine Volume 1 runtime packs if those 208 animations are candidates for use.
5. After a second preview pass, wire one stage behind a feature flag and playtest bullet density before expanding to the whole roster.
"""
    (ROOT / "REVIEW.md").write_text(text, encoding="utf-8")


def main() -> None:
    summary = {
        "review_policy": "analysis and previews only; no live game wiring",
        "volume_1": analyze_v1(),
        "volume_2": analyze_v2(),
        "volume_2_vfx": analyze_v2_vfx(),
        "doomsday_carrier": analyze_carrier(),
    }
    (ROOT / "analysis_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    write_catalog(summary)
    write_html(summary)
    write_markdown(summary)
    compact = {
        "volume_1_enemies": summary["volume_1"]["count"],
        "volume_1_unique_pattern_sets": summary["volume_1"]["unique_pattern_sets"],
        "volume_1_duplicate_pattern_groups": len(summary["volume_1"]["duplicate_pattern_groups"]),
        "volume_2_combatants": summary["volume_2"]["count"],
        "volume_2_unique_pattern_sets": summary["volume_2"]["unique_pattern_sets"],
        "volume_2_duplicate_pattern_groups": len(summary["volume_2"]["duplicate_pattern_groups"]),
        "volume_2_binary_alpha": summary["volume_2"]["png_binary_alpha"],
        "volume_2_semitransparent_pixels": summary["volume_2"]["semitransparent_pixels"],
        "volume_2_magenta_pixels": summary["volume_2"]["magenta_pixels"],
        "volume_2_border_touching_frames": summary["volume_2"]["border_touching_frame_count"],
        "volume_2_vfx_families": summary["volume_2_vfx"]["count"],
        "carrier_patterns": len(summary["doomsday_carrier"]["patterns"]),
        "carrier_frames": summary["doomsday_carrier"]["boss_frame_count"],
        "carrier_binary_alpha": summary["doomsday_carrier"]["binary_alpha"],
        "carrier_border_touching_frames": len(summary["doomsday_carrier"]["border_touching_frames"]),
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
