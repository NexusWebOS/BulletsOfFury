#!/usr/bin/env python3
"""Normalize an irregularly spaced strip by detecting its actual alpha bands."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def content_bbox(image: Image.Image, threshold: int):
    return image.getchannel("A").point(lambda value: 255 if value > threshold else 0).getbbox()


def bands(image: Image.Image, threshold: int, expected: int) -> list[tuple[int, int]]:
    alpha = image.getchannel("A")
    occupied = []
    for x in range(image.width):
        occupied.append(alpha.crop((x, 0, x + 1, image.height)).getbbox() is not None)
    result: list[tuple[int, int]] = []
    start = None
    for x, active in enumerate(occupied + [False]):
        if active and start is None:
            start = x
        elif not active and start is not None:
            result.append((start, x))
            start = None
    if len(result) <= expected:
        return result
    gaps = [(result[index + 1][0] - result[index][1], index) for index in range(len(result) - 1)]
    cuts = {index for _, index in sorted(gaps, reverse=True)[: expected - 1]}
    merged: list[tuple[int, int]] = []
    left = result[0][0]
    for index, (_, right) in enumerate(result):
        if index in cuts or index == len(result) - 1:
            merged.append((left, right))
            if index + 1 < len(result):
                left = result[index + 1][0]
    return merged


def compose(content: Image.Image, size: int, scale: float) -> Image.Image:
    width = max(1, round(content.width * scale))
    height = max(1, round(content.height * scale))
    sprite = content.resize((width, height), Image.Resampling.NEAREST)
    frame = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    frame.alpha_composite(sprite, ((size - width) // 2, size - height))
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--frames", type=int, required=True)
    parser.add_argument("--frame-size", type=int, default=256)
    parser.add_argument("--anchor", required=True)
    parser.add_argument("--alpha-threshold", type=int, default=8)
    args = parser.parse_args()

    strip = Image.open(args.input).convert("RGBA")
    runs = bands(strip, args.alpha_threshold, args.frames)
    if len(runs) != args.frames:
        raise SystemExit(f"Expected {args.frames} alpha bands, detected {len(runs)}: {runs}")

    contents: list[Image.Image] = []
    for left, right in runs:
        slot = strip.crop((left, 0, right, strip.height))
        bbox = content_bbox(slot, args.alpha_threshold)
        if bbox is None:
            raise SystemExit("Empty detected sprite band")
        contents.append(slot.crop(bbox))

    anchor = Image.open(args.anchor).convert("RGBA")
    anchor_box = content_bbox(anchor, args.alpha_threshold)
    if anchor_box is None:
        raise SystemExit("Anchor contains no visible pixels")
    anchor_content = anchor.crop(anchor_box)
    max_width = max([anchor_content.width, *(frame.width for frame in contents)])
    max_height = max([anchor_content.height, *(frame.height for frame in contents)])
    scale = min(args.frame_size / max_width, args.frame_size / max_height)

    output = Path(args.out_dir)
    output.mkdir(parents=True, exist_ok=True)
    compose(anchor_content, args.frame_size, scale).save(output / "01.png")
    for index, frame in enumerate(contents[1:], start=2):
        compose(frame, args.frame_size, scale).save(output / f"{index:02d}.png")


if __name__ == "__main__":
    main()
