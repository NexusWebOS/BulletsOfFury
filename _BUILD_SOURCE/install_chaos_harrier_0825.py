"""Install the approved Chaos Harrier pack as loose, code-owned runtime frames.

The source pack already has fixed 352x320 ship canvases and hard alpha.  This installer keeps
those canvases intact, copies only runtime PNGs, and derives a cyan-only hover-light overlay so
the hull remains on one stable idle silhouette while its internal pixels pulse independently.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SRC = (
    ROOT
    / "_ART_SOURCES"
    / "CF_ChaosHarrierMiniBoss-Lvl5_0825"
    / "CF_ChaosHarrierMiniBoss-Lvl5"
    / "Edited"
)
OUT = ROOT / "assets" / "game" / "chaos_harrier"
PREVIEW = ROOT / "_BUILD_SOURCE" / "preview_chaos_harrier_0825.png"


GROUPS = {
    "ship": (
        "chaosharrier",
        [
            "chaosharrier-01-hover-a.png",
            "chaosharrier-02-hover-b.png",
            "chaosharrier-03-attack-open.png",
            "chaosharrier-04-bank-left.png",
            "chaosharrier-05-bank-right.png",
            "chaosharrier-06-critical.png",
        ],
    ),
    "plasma": (
        "chaosharrier-projectiles",
        [f"chaosharrier-projectile-{i:02d}-plasma-{i}.png" for i in range(1, 5)],
    ),
    "missile": (
        "chaosharrier-projectiles",
        [f"chaosharrier-projectile-{i + 4:02d}-missile-{i}.png" for i in range(1, 5)],
    ),
    "lance": (
        "chaosharrier-projectiles",
        [f"chaosharrier-projectile-{i + 8:02d}-reactor-lance-{i}.png" for i in range(1, 5)],
    ),
    "sideflash": (
        "chaosharrier-vfx",
        [f"chaosharrier-vfx-{i:02d}-sideflash-{i}.png" for i in range(1, 5)],
    ),
    "launchflash": (
        "chaosharrier-vfx",
        [f"chaosharrier-vfx-{i + 4:02d}-launchflash-{i}.png" for i in range(1, 5)],
    ),
    "charge": (
        "chaosharrier-vfx",
        [f"chaosharrier-vfx-{i + 8:02d}-corecharge-{i}.png" for i in range(1, 5)],
    ),
    "warp": (
        "chaosharrier-warp",
        [
            "chaosharrier-warp-01-sparks.png",
            "chaosharrier-warp-02-slit-open.png",
            "chaosharrier-warp-03-aperture-open.png",
            "chaosharrier-warp-04-aperture-full.png",
            "chaosharrier-warp-05-phase-flash.png",
            "chaosharrier-warp-06-aperture-collapse.png",
            "chaosharrier-warp-07-slit-collapse.png",
            "chaosharrier-warp-08-residue.png",
        ],
    ),
    "beam": (
        "chaosharrier-reactor-laser",
        [f"chaosharrier-reactor-laser-{i:02d}-beam-{i}.png" for i in range(1, 5)],
    ),
    "sidelaser": (
        "chaosharrier-side-lasers",
        [f"chaosharrier-side-lasers-{i:02d}-travel-{i}.png" for i in range(1, 5)],
    ),
    "impact": (
        "chaosharrier-laser-impact",
        [f"chaosharrier-laser-impact-{i:02d}-impact-{i}.png" for i in range(1, 5)],
    ),
}


def copy_frames() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for group, (folder, names) in GROUPS.items():
        for index, name in enumerate(names):
            source = SRC / folder / name
            if not source.is_file():
                raise FileNotFoundError(source)
            shutil.copy2(source, OUT / f"ch_{group}_{index}.png")


def build_glow_overlay() -> None:
    base = Image.open(OUT / "ch_ship_0.png").convert("RGBA")
    bright = Image.open(OUT / "ch_ship_1.png").convert("RGBA")
    overlay = Image.new("RGBA", base.size)
    bp = base.load()
    hp = bright.load()
    op = overlay.load()
    for y in range(base.height):
        for x in range(base.width):
            br, bg, bb, ba = bp[x, y]
            hr, hg, hb, ha = hp[x, y]
            delta = max(abs(hr - br), abs(hg - bg), abs(hb - bb))
            cyan = hb >= 95 and hg >= 70 and hb > hr * 1.20 and hg > hr * 1.05
            if ha and cyan and delta >= 8:
                op[x, y] = (hr, hg, hb, min(255, 70 + delta * 6))
    overlay.save(OUT / "ch_ship_glow.png")


def build_preview() -> None:
    cells = [
        ("HOVER + LIGHTS", "ch_ship_0.png"),
        ("MISSILE BAYS", "ch_ship_2.png"),
        ("BANK LEFT", "ch_ship_3.png"),
        ("BANK RIGHT", "ch_ship_4.png"),
        ("CRITICAL", "ch_ship_5.png"),
        ("WARP PEAK", "ch_warp_4.png"),
        ("MISSILE", "ch_missile_2.png"),
        ("NOSE BEAM", "ch_beam_2.png"),
    ]
    sheet = Image.new("RGB", (4 * 240, 2 * 280), (7, 10, 18))
    draw = ImageDraw.Draw(sheet)
    for i, (label, filename) in enumerate(cells):
        source = Image.open(OUT / filename).convert("RGBA")
        source.thumbnail((220, 235), Image.Resampling.NEAREST)
        x = (i % 4) * 240 + (240 - source.width) // 2
        y = (i // 4) * 280 + 28 + (235 - source.height) // 2
        sheet.paste(source, (x, y), source)
        draw.text(((i % 4) * 240 + 10, (i // 4) * 280 + 8), label, fill=(180, 225, 255))
    sheet.save(PREVIEW)


if __name__ == "__main__":
    copy_frames()
    build_glow_overlay()
    build_preview()
    print(f"installed {sum(len(v[1]) for v in GROUPS.values()) + 1} runtime frames")
    print(PREVIEW)
