#!/usr/bin/env python3
"""Remove the retired compact BOF UI font family from shipping data.

The game now uses the Fury dialogue BMF for prose/cinematics and the glyphs embedded in
BOF.stageArt for stage-labelled text.  This removes BOF.bofFont from the generated manifest and
deletes only its eight dedicated PNG sheets.  It refuses to touch any unexpected path.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "manifest.js"
PREFIX = "window.BOF="
FONT_DIR = (ROOT / "assets" / "game" / "fonts").resolve()
EXPECTED = [FONT_DIR / f"bof_font{i}.png" for i in range(1, 9)]


def assignment(source: str, prefix: str) -> tuple[int, int, dict]:
    start = source.index(prefix) + len(prefix)
    depth = 0
    quoted = False
    escaped = False
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


def main() -> None:
    source = MANIFEST.read_text(encoding="utf-8")
    start, end, bof = assignment(source, PREFIX)
    removed = bof.pop("bofFont", None)
    if removed is not None:
        compact = json.dumps(bof, ensure_ascii=False, separators=(",", ":"))
        MANIFEST.write_text(source[:start] + compact + source[end:], encoding="utf-8")
        print(f"removed BOF.bofFont manifest family ({len(removed)} variants)")
    else:
        print("BOF.bofFont already absent from manifest")

    deleted = 0
    for path in EXPECTED:
        resolved = path.resolve()
        if resolved.parent != FONT_DIR or not resolved.name.startswith("bof_font"):
            raise RuntimeError(f"refusing unexpected delete target: {resolved}")
        if resolved.exists():
            resolved.unlink()
            deleted += 1
            print(f"deleted {resolved.relative_to(ROOT)}")
    print(f"deleted {deleted} compact font sheets")


if __name__ == "__main__":
    main()
