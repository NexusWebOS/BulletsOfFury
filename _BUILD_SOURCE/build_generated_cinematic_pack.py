#!/usr/bin/env python3
"""Build the generated cinematic explosion/background asset pack.

The source explosion sheets contain six AI-authored hero poses.  This script
normalizes those poses with one shared scale/anchor, creates alpha-aware
in-betweens, and exports 32-frame Neo-Geo-style runtime sequences at every
requested canvas size.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets" / "game" / "generated_cinematic"
EXPLOSIONS = PACK / "explosions"
BACKGROUNDS = PACK / "backgrounds"
PALETTE_INPUTS = ROOT / "_BUILD_SOURCE" / "generated_cinematic_palette_inputs"

FRAME_SIZES = ((128, 128), (192, 192), (256, 256), (320, 256), (320, 320))
FRAME_COUNT = 32
# Spread the six authored stages across the complete runtime.  The final stage
# remains fully rendered; lifecycle removal belongs to the game, not sprite alpha.
KEY_TIMES = (0, 4, 9, 15, 23, 31)
RECOMMENDED_FPS = 30

ANIMATIONS = {
    "airburst": {
        "source": EXPLOSIONS / "sources" / "airburst_keyframes_6.png",
        "anchor": "center",
        "description": "Spherical white-hot airburst rolling into an ember ring.",
    },
    "ground_blast": {
        "source": EXPLOSIONS / "sources" / "ground_blast_keyframes_6.png",
        "anchor": "bottom-center",
        "description": "Grounded fire dome rising into a tall combustion column.",
    },
}

for base_name, anchor, base_description in (
    ("airburst", "center", "Spherical airburst"),
    ("ground_blast", "bottom-center", "Grounded combustion column"),
):
    for palette in ("blue", "green", "purple"):
        name = f"{base_name}_{palette}"
        ANIMATIONS[name] = {
            "source": EXPLOSIONS / "sources" / f"{name}_keyframes_6.png",
            "palette_input": PALETTE_INPUTS / f"{name}_rgb.png",
            "alpha_source": EXPLOSIONS / "sources" / f"{base_name}_keyframes_6.png",
            "anchor": anchor,
            "palette": palette,
            "variant_of": base_name,
            "description": f"{palette.title()} {base_description.lower()} energy variant.",
        }

BACKGROUND_MASTERS = {
    "storm_bridge": BACKGROUNDS / "masters" / "storm_bridge_master_1448x1086.png",
    "toxic_reactor": BACKGROUNDS / "masters" / "toxic_reactor_master_1448x1086.png",
    "ruined_hangar": BACKGROUNDS / "masters" / "ruined_hangar_master_1448x1086.png",
}


def split_horizontal_strip(image: Image.Image, count: int) -> list[Image.Image]:
    """Split on the quiet alpha valleys nearest the expected slot boundaries.

    Image generation keeps the requested one-row layout but does not guarantee
    mathematically perfect slot centering.  Valley cuts prevent particles from
    the next pose leaking into the previous frame.
    """
    alpha = np.asarray(image.getchannel("A"), dtype=np.uint8)
    activity = (alpha > 3).sum(axis=0).astype(np.float32)
    kernel_width = max(5, round(image.width / count * 0.025))
    if kernel_width % 2 == 0:
        kernel_width += 1
    smoothed = np.convolve(activity, np.ones(kernel_width), mode="same")
    nominal_slot = image.width / count
    cuts = [0]
    for index in range(1, count):
        expected = round(index * nominal_slot)
        radius = round(nominal_slot * 0.38)
        search_left = max(cuts[-1] + 1, expected - radius)
        search_right = min(image.width - 1, expected + radius)
        cut = search_left + int(np.argmin(smoothed[search_left:search_right]))
        cuts.append(cut)
    cuts.append(image.width)

    slots: list[Image.Image] = []
    for index in range(count):
        left = cuts[index]
        right = cuts[index + 1]
        slots.append(image.crop((left, 0, right, image.height)))
    return slots


def alpha_bbox(image: Image.Image, threshold: int = 3) -> tuple[int, int, int, int] | None:
    alpha = image.getchannel("A").point(lambda value: 255 if value > threshold else 0)
    return alpha.getbbox()


def crop_content(image: Image.Image) -> Image.Image:
    bbox = alpha_bbox(image)
    if bbox is None:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    return image.crop(bbox)


def prepare_variant_sources() -> None:
    """Apply proven master alpha geometry to generated RGB palette variants.

    Image generation supplied the intended palette art but repeatedly baked its
    checker preview into RGB.  The orange masters already have validated alpha
    and identical six-pose geometry, so they provide a stable production mask.
    """
    for spec in ANIMATIONS.values():
        palette_input = spec.get("palette_input")
        if palette_input is None:
            continue
        color = Image.open(palette_input).convert("RGB")
        alpha_source = Image.open(spec["alpha_source"]).convert("RGBA")
        if color.size != alpha_source.size:
            raise SystemExit(
                f"Palette input {palette_input} has size {color.size}; "
                f"expected {alpha_source.size}."
            )
        output = color.convert("RGBA")
        output.putalpha(alpha_source.getchannel("A"))
        source_path = Path(spec["source"])
        source_path.parent.mkdir(parents=True, exist_ok=True)
        output.save(source_path, optimize=True)


def normalize_keyframes(
    raw_frames: list[Image.Image], width: int, height: int, anchor: str
) -> list[Image.Image]:
    contents = [crop_content(frame) for frame in raw_frames]
    largest_width = max(frame.width for frame in contents)
    largest_height = max(frame.height for frame in contents)
    pad_x = max(4, round(width * 0.04))
    pad_y = max(4, round(height * 0.04))
    scale = min(
        (width - pad_x * 2) / largest_width,
        (height - pad_y * 2) / largest_height,
    )

    normalized: list[Image.Image] = []
    for content in contents:
        new_size = (
            max(1, round(content.width * scale)),
            max(1, round(content.height * scale)),
        )
        resized = content.resize(new_size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        left = (width - resized.width) // 2
        if anchor == "bottom-center":
            top = height - pad_y - resized.height
        else:
            top = (height - resized.height) // 2
        canvas.alpha_composite(resized, (left, top))
        normalized.append(canvas)
    return normalized


def premultiplied_blend(first: Image.Image, second: Image.Image, amount: float) -> Image.Image:
    """Cross-dissolve RGBA images without introducing dark transparent fringes."""
    a = np.asarray(first, dtype=np.float32) / 255.0
    b = np.asarray(second, dtype=np.float32) / 255.0
    alpha_a = a[..., 3:4]
    alpha_b = b[..., 3:4]
    out_alpha = alpha_a * (1.0 - amount) + alpha_b * amount
    premul = a[..., :3] * alpha_a * (1.0 - amount) + b[..., :3] * alpha_b * amount
    out_rgb = np.divide(
        premul,
        out_alpha,
        out=np.zeros_like(premul),
        where=out_alpha > 1.0e-6,
    )
    rgba = np.concatenate((out_rgb, out_alpha), axis=2)
    return Image.fromarray(np.clip(rgba * 255.0 + 0.5, 0, 255).astype(np.uint8), "RGBA")


def smoothstep(value: float) -> float:
    return value * value * (3.0 - 2.0 * value)


def build_sequence(keyframes: list[Image.Image]) -> list[Image.Image]:
    sequence: list[Image.Image] = []
    for frame_index in range(FRAME_COUNT):
        right_index = next(
            (index for index, time in enumerate(KEY_TIMES) if time >= frame_index),
            len(KEY_TIMES) - 1,
        )
        if KEY_TIMES[right_index] == frame_index or right_index == 0:
            sequence.append(keyframes[right_index].copy())
            continue

        left_index = right_index - 1
        start = KEY_TIMES[left_index]
        end = KEY_TIMES[right_index]
        amount = smoothstep((frame_index - start) / (end - start))
        sequence.append(premultiplied_blend(keyframes[left_index], keyframes[right_index], amount))
    return sequence


def save_strip(frames: list[Image.Image], path: Path) -> None:
    strip = Image.new("RGBA", (sum(frame.width for frame in frames), frames[0].height))
    left = 0
    for frame in frames:
        strip.alpha_composite(frame, (left, 0))
        left += frame.width
    path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(path, optimize=True)


def save_frames(frames: list[Image.Image], directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for index, frame in enumerate(frames):
        frame.save(directory / f"frame_{index:02d}.png", optimize=True)


def checkerboard(size: tuple[int, int], tile: int = 16) -> Image.Image:
    board = Image.new("RGBA", size, (30, 32, 38, 255))
    draw = ImageDraw.Draw(board)
    colors = ((35, 38, 45, 255), (52, 56, 66, 255))
    for top in range(0, size[1], tile):
        for left in range(0, size[0], tile):
            draw.rectangle(
                (left, top, left + tile - 1, top + tile - 1),
                fill=colors[((left // tile) + (top // tile)) % 2],
            )
    return board


def save_contact_sheet(frames: list[Image.Image], path: Path, columns: int = 8) -> None:
    rows = math.ceil(len(frames) / columns)
    gap = 6
    width = columns * frames[0].width + (columns - 1) * gap
    height = rows * frames[0].height + (rows - 1) * gap
    sheet = checkerboard((width, height))
    for index, frame in enumerate(frames):
        left = (index % columns) * (frame.width + gap)
        top = (index // columns) * (frame.height + gap)
        sheet.alpha_composite(frame, (left, top))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def save_animated_preview(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    duration = round(1000 / RECOMMENDED_FPS)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        lossless=True,
        method=6,
    )


def build_explosions() -> dict[str, object]:
    prepare_variant_sources()
    manifest: dict[str, object] = {}
    for name, spec in ANIMATIONS.items():
        source = Image.open(spec["source"]).convert("RGBA")
        raw_frames = split_horizontal_strip(source, len(KEY_TIMES))
        size_entries: dict[str, object] = {}
        preview_frames: list[Image.Image] | None = None

        for width, height in FRAME_SIZES:
            keyframes = normalize_keyframes(raw_frames, width, height, str(spec["anchor"]))
            frames = build_sequence(keyframes)
            label = f"{width}x{height}"
            frame_dir = EXPLOSIONS / name / label / "frames"
            strip_path = EXPLOSIONS / name / label / f"{name}_32frames_strip.png"
            save_frames(frames, frame_dir)
            save_strip(frames, strip_path)
            if (width, height) == (128, 128):
                save_contact_sheet(
                    frames,
                    EXPLOSIONS / name / "previews" / f"{name}_32frames_contact.png",
                )
            if (width, height) == (256, 256):
                preview_frames = frames
            size_entries[label] = {
                "frames": str(frame_dir.relative_to(ROOT)).replace("\\", "/"),
                "strip": str(strip_path.relative_to(ROOT)).replace("\\", "/"),
            }

        assert preview_frames is not None
        preview_path = EXPLOSIONS / name / "previews" / f"{name}_32frames_30fps.webp"
        save_animated_preview(preview_frames, preview_path)
        visibility = []
        for frame_index, frame in enumerate(preview_frames):
            alpha = np.asarray(frame.getchannel("A"), dtype=np.uint8)
            visibility.append(
                {
                    "frame": frame_index,
                    "visible_pixels": int((alpha > 3).sum()),
                    "opaque_pixels": int((alpha == 255).sum()),
                    "max_alpha": int(alpha.max()),
                }
            )
        manifest[name] = {
            "description": spec["description"],
            "source_keyframes": str(Path(spec["source"]).relative_to(ROOT)).replace("\\", "/"),
            "source_keyframe_count": len(KEY_TIMES),
            "runtime_frame_count": FRAME_COUNT,
            "recommended_fps": RECOMMENDED_FPS,
            "whole_sprite_fade": False,
            "final_frame_policy": "persistent authored ember/smoke breakup; engine removes effect after playback",
            "visibility_256x256": visibility,
            "anchor": spec["anchor"],
            "palette": spec.get("palette", "orange"),
            "variant_of": spec.get("variant_of"),
            "preview": str(preview_path.relative_to(ROOT)).replace("\\", "/"),
            "sizes": size_entries,
        }
    return manifest


def build_backgrounds() -> dict[str, object]:
    manifest: dict[str, object] = {}
    for name, source_path in BACKGROUND_MASTERS.items():
        image = Image.open(source_path).convert("RGB")
        outputs: dict[str, str] = {}
        for width, height in ((680, 510), (1360, 1020)):
            output = BACKGROUNDS / "game_plates" / f"{name}_{width}x{height}.png"
            output.parent.mkdir(parents=True, exist_ok=True)
            image.resize((width, height), Image.Resampling.LANCZOS).save(output, optimize=True)
            outputs[f"{width}x{height}"] = str(output.relative_to(ROOT)).replace("\\", "/")
        manifest[name] = {
            "master": str(source_path.relative_to(ROOT)).replace("\\", "/"),
            "master_size": list(image.size),
            "exports": outputs,
        }
    return manifest


def main() -> None:
    manifest = {
        "pack": "BulletsOfFury generated cinematic effects v2",
        "style": "neo-geo / late-1990s arcade shooter pixel art",
        "explosions": build_explosions(),
        "backgrounds": build_backgrounds(),
    }
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
