#!/usr/bin/env python3
"""Turn only edge-connected pure-black sprite-strip backdrop into hard alpha."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--threshold", type=int, default=7)
    args = parser.parse_args()

    image = Image.open(args.input).convert("RGBA")
    px = image.load()
    width, height = image.size
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def backdrop(x: int, y: int) -> bool:
        r, g, b, a = px[x, y]
        return a == 0 or (a > 0 and max(r, g, b) <= args.threshold)

    def push(x: int, y: int) -> None:
        index = y * width + x
        if not seen[index] and backdrop(x, y):
            seen[index] = 1
            queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)
    for y in range(height):
        push(0, y)
        push(width - 1, y)

    while queue:
        x, y = queue.popleft()
        px[x, y] = (0, 0, 0, 0)
        if x:
            push(x - 1, y)
        if x + 1 < width:
            push(x + 1, y)
        if y:
            push(x, y - 1)
        if y + 1 < height:
            push(x, y + 1)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


if __name__ == "__main__":
    main()
