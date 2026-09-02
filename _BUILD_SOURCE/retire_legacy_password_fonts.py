#!/usr/bin/env python3
"""Permanently retire the pre-BOF password/game fonts.

The approved password screen uses BOF.bofFont (the eight stage alphabets).  The old sfont1..9
and ncm_font glyphs survived only as BOFX atlas cells.  This removes their registrations and
clears their non-aliased pixel rectangles without moving any live atlas coordinates.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "manifest.js"
FAMILY_MAP = ROOT / "assets" / "data" / "ART_FAMILY_MAP.json"
PREFIX = "window.BOFX="


def assignment(source: str, prefix: str) -> tuple[int, int, dict]:
    start = source.index(prefix) + len(prefix)
    depth = 0
    quoted = False
    escaped = False
    end = start
    for end in range(start, len(source)):
        ch = source[end]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return start, end + 1, json.loads(source[start : end + 1])
    raise RuntimeError(f"unterminated {prefix} assignment")


def legacy(key: str) -> bool:
    if key.startswith("ncm_font_"):
        return True
    if not key.startswith("sfont"):
        return False
    head = key.split("_", 1)[0][5:]
    return head.isdigit() and 1 <= int(head) <= 9


def main() -> None:
    source = MANIFEST.read_text(encoding="utf-8")
    start, end, bofx = assignment(source, PREFIX)
    images = bofx.get("img", {})
    cells = bofx.get("cells", {})
    doomed = sorted(k for k in set(images) | set(cells) if legacy(k))
    if not doomed:
        print("legacy password fonts already retired")
        return

    by_rect: dict[tuple, list[str]] = {}
    for key, rect in cells.items():
        by_rect.setdefault(tuple(rect), []).append(key)
    shared = [(rect, keys) for rect, keys in by_rect.items()
              if any(legacy(k) for k in keys) and any(not legacy(k) for k in keys)]
    if shared:
        raise RuntimeError(f"refusing to clear {len(shared)} atlas cells shared with live art")

    atlas_rects: dict[Path, list[tuple[int, int, int, int]]] = {}
    for key in doomed:
        rect = cells.get(key)
        if not rect:
            continue
        sheet, x, y, w, h = rect[:5]
        path = ROOT / "assets" / "game" / "atlas" / f"nca_{sheet}.png"
        atlas_rects.setdefault(path, []).append((x, y, w, h))

    for path, rects in atlas_rects.items():
        if not path.exists():
            raise FileNotFoundError(path)
        image = Image.open(path).convert("RGBA")
        for x, y, w, h in set(rects):
            if x < 0 or y < 0 or x + w > image.width or y + h > image.height:
                raise RuntimeError(f"bad legacy cell {(x, y, w, h)} in {path.name}")
            image.paste((0, 0, 0, 0), (x, y, x + w, y + h))
        image.save(path, optimize=True, compress_level=9)
        print(f"cleared {len(set(rects)):3d} legacy glyph cells from {path.relative_to(ROOT)}")

    for key in doomed:
        images.pop(key, None)
        cells.pop(key, None)
    compact = json.dumps(bofx, ensure_ascii=False, separators=(",", ":"))
    MANIFEST.write_text(source[:start] + compact + source[end:], encoding="utf-8")

    if FAMILY_MAP.exists():
        data = json.loads(FAMILY_MAP.read_text(encoding="utf-8"))
        by_family = data.get("byFamily", {})
        removed_families = [f"sfont{i}" for i in range(1, 10)]
        for family in removed_families:
            by_family.pop(family, None)
        ncm = by_family.get("ncm")
        if ncm:
            ncm["keys"] = max(0, int(ncm.get("keys", 0)) - sum(k.startswith("ncm_font_") for k in doomed))
            ncm["why"] = "campaign-map ncm_ art only; retired ncm_font glyph cells removed"
        data["unreferenced"] = [row for row in data.get("unreferenced", [])
                                if row.get("family") not in removed_families]
        stats = data.get("stats", {})
        stats["families"] = len(by_family)
        stats["namedByCode"] = max(0, int(stats.get("namedByCode", 0)) - 121)
        stats["quarantined"] = max(0, int(stats.get("quarantined", 0)) - 376)
        FAMILY_MAP.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")

    print(f"removed {len(doomed)} legacy font keys ({sum(k.startswith('sfont') for k in doomed)} sfont, "
          f"{sum(k.startswith('ncm_font_') for k in doomed)} ncm_font)")


if __name__ == "__main__":
    main()
