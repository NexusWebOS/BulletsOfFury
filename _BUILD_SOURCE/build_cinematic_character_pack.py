from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "_BUILD_SOURCE" / "cinematic_character_pose_inputs"
OUTPUT_DIR = ROOT / "assets" / "game" / "cinematic_characters"

CHARACTERS = (
    "axel",
    "cole",
    "decker",
    "falva",
    "freezer",
    "juggernaut",
    "lizzie",
    "maverick",
    "yuri",
)

POSES = (
    "01_front_neutral",
    "02_front_left_3q",
    "03_front_right_3q",
    "04_back_neutral",
    "05_back_left_3q",
    "06_back_right_3q",
)

MATTE_LUMA_MIN = 218
MATTE_CHROMA_MAX = 18
CROP_PADDING = 24


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def extract_alpha(rgb_image: Image.Image) -> Image.Image:
    """Remove the connected near-neutral bright checker matte without resampling.

    The generated subjects are dark-outlined pixel art.  A connected-background
    flood preserves enclosed light details such as eyes, insignia and Axel's fur
    collar while removing the entire checker and its bright edge contamination.
    Output alpha is deliberately binary for crisp arcade-pixel silhouettes.
    """

    rgb = np.asarray(rgb_image.convert("RGB"), dtype=np.uint8)
    high = rgb.max(axis=2).astype(np.int16)
    low = rgb.min(axis=2).astype(np.int16)
    luma = rgb.mean(axis=2)
    chroma = high - low

    candidate = (luma >= MATTE_LUMA_MIN) & (chroma <= MATTE_CHROMA_MAX)
    # Image.fromarray may share a read-only NumPy buffer; floodfill requires a
    # writable PIL allocation or it silently leaves the matte unchanged.
    candidate_image = Image.fromarray(
        np.where(candidate, 255, 0).astype(np.uint8), "L"
    ).copy()

    # The checker field is continuous around every figure, so one corner flood
    # reaches all true background while enclosed costume highlights remain sealed.
    ImageDraw.floodfill(candidate_image, (0, 0), 128, border=0, thresh=0)
    flooded = np.asarray(candidate_image) == 128

    alpha = np.where(flooded, 0, 255).astype(np.uint8)
    rgba = np.dstack((rgb, alpha))
    rgba[alpha == 0, :3] = 0  # transparent pixels carry no matte color
    return Image.fromarray(rgba, "RGBA")


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("No opaque character pixels found")
    return bbox


def padded_crop(image: Image.Image, padding: int) -> tuple[Image.Image, tuple[int, int, int, int]]:
    left, top, right, bottom = alpha_bbox(image)
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.width, right + padding)
    bottom = min(image.height, bottom + padding)
    return image.crop((left, top, right, bottom)), (left, top, right, bottom)


def character_components(image: Image.Image) -> list[dict]:
    """Return the six large 4-connected figure silhouettes, ordered left-to-right."""

    work = image.getchannel("A").point(lambda value: 255 if value else 0).copy()
    components: list[dict] = []
    while True:
        data = np.asarray(work)
        ys, xs = np.where(data == 255)
        if len(xs) == 0:
            break

        seed = (int(xs[0]), int(ys[0]))
        ImageDraw.floodfill(work, seed, 128, thresh=0)
        data = np.asarray(work)
        ys, xs = np.where(data == 128)
        mask = data == 128
        components.append(
            {
                "pixel_count": int(len(xs)),
                "bbox": (
                    int(xs.min()),
                    int(ys.min()),
                    int(xs.max()) + 1,
                    int(ys.max()) + 1,
                ),
                "mask": mask.copy(),
            }
        )

        data = np.array(work)
        data[mask] = 0
        work = Image.fromarray(data.astype(np.uint8), "L").copy()

    components.sort(key=lambda component: component["pixel_count"], reverse=True)
    selected = components[: len(POSES)]
    if len(selected) != len(POSES) or selected[-1]["pixel_count"] < 1000:
        raise RuntimeError(
            f"Expected six substantial figure components; got "
            f"{[component['pixel_count'] for component in selected]}"
        )
    selected.sort(key=lambda component: component["bbox"][0])
    return selected


def exposed_bright_matte_pixels(image: Image.Image) -> int:
    arr = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    alpha = arr[:, :, 3]
    occupied = alpha > 0
    transparent = ~occupied

    neighbor_transparent = np.zeros_like(transparent)
    neighbor_transparent[1:] |= transparent[:-1]
    neighbor_transparent[:-1] |= transparent[1:]
    neighbor_transparent[:, 1:] |= transparent[:, :-1]
    neighbor_transparent[:, :-1] |= transparent[:, 1:]
    edge = occupied & neighbor_transparent

    rgb = arr[:, :, :3].astype(np.int16)
    luma = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    suspicious = edge & (luma >= MATTE_LUMA_MIN) & (chroma <= MATTE_CHROMA_MAX)
    return int(suspicious.sum())


def make_composite_preview(character: str, frames: list[Image.Image], destination: Path) -> None:
    tiles: list[Image.Image] = []
    backdrops = ((11, 14, 20), (75, 8, 10), (5, 37, 77), (7, 65, 29))
    font = ImageFont.load_default()

    for index, frame in enumerate(frames):
        bg = backdrops[index % len(backdrops)]
        tile = Image.new("RGB", (frame.width + 24, frame.height + 46), bg)
        tile.paste(frame, (12, 12), frame)
        draw = ImageDraw.Draw(tile)
        draw.text((12, frame.height + 22), POSES[index], fill=(235, 238, 244), font=font)
        tiles.append(tile)

    width = sum(tile.width for tile in tiles)
    height = max(tile.height for tile in tiles)
    canvas = Image.new("RGB", (width, height), (3, 4, 8))
    x = 0
    for tile in tiles:
        canvas.paste(tile, (x, 0))
        x += tile.width

    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, optimize=True)


def build_character(character: str) -> dict:
    source = INPUT_DIR / f"{character}_master_rgb.png"
    if not source.exists():
        raise FileNotFoundError(source)

    raw = Image.open(source).convert("RGB")
    master = extract_alpha(raw)
    components = character_components(master)

    # Remove tiny isolated generation specks from the combined master as well.
    master_data = np.asarray(master, dtype=np.uint8).copy()
    clean_mask = np.zeros((master.height, master.width), dtype=bool)
    for component in components:
        clean_mask |= component["mask"]
    master_data[~clean_mask] = 0
    master = Image.fromarray(master_data, "RGBA")
    char_dir = OUTPUT_DIR / character
    frame_dir = char_dir / "poses"
    frame_dir.mkdir(parents=True, exist_ok=True)

    master_path = char_dir / f"{character}_poses_master_rgba.png"
    master.save(master_path, optimize=True)

    frames: list[Image.Image] = []
    frame_entries: list[dict] = []
    master_rgba = np.asarray(master, dtype=np.uint8)
    for index, (pose, component) in enumerate(zip(POSES, components)):
        pose_data = master_rgba.copy()
        pose_data[~component["mask"]] = 0
        pose_canvas = Image.fromarray(pose_data, "RGBA")
        frame, crop = padded_crop(pose_canvas, CROP_PADDING)
        frame_path = frame_dir / f"{pose}.png"
        frame.save(frame_path, optimize=True)
        frames.append(frame)
        frame_entries.append(
            {
                "pose": pose,
                "file": frame_path.relative_to(ROOT).as_posix(),
                "size": [frame.width, frame.height],
                "source_crop": list(crop),
                "connected_component_pixels": component["pixel_count"],
                "resampled": False,
                "corner_alpha": [
                    frame.getpixel((0, 0))[3],
                    frame.getpixel((frame.width - 1, 0))[3],
                    frame.getpixel((0, frame.height - 1))[3],
                    frame.getpixel((frame.width - 1, frame.height - 1))[3],
                ],
                "exposed_bright_matte_pixels": exposed_bright_matte_pixels(frame),
                "sha256": sha256(frame_path),
            }
        )

    preview_path = char_dir / f"{character}_edge_qa_preview.png"
    make_composite_preview(character, frames, preview_path)

    return {
        "character": character,
        "input": source.relative_to(ROOT).as_posix(),
        "input_sha256": sha256(source),
        "master": master_path.relative_to(ROOT).as_posix(),
        "master_size": [master.width, master.height],
        "master_mode": master.mode,
        "master_corner_alpha": [
            master.getpixel((0, 0))[3],
            master.getpixel((master.width - 1, 0))[3],
            master.getpixel((0, master.height - 1))[3],
            master.getpixel((master.width - 1, master.height - 1))[3],
        ],
        "preview": preview_path.relative_to(ROOT).as_posix(),
        "frames": frame_entries,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    characters = [build_character(character) for character in CHARACTERS]
    manifest = {
        "pack": "FURY cinematic character pose masters",
        "character_count": len(characters),
        "poses_per_character": len(POSES),
        "total_frames": len(characters) * len(POSES),
        "pose_order": list(POSES),
        "pipeline": {
            "resizing": "none",
            "alpha": "binary straight alpha",
            "matte_extraction": "connected bright-neutral flood from sheet border",
            "matte_luma_min": MATTE_LUMA_MIN,
            "matte_chroma_max": MATTE_CHROMA_MAX,
            "crop_padding": CROP_PADDING,
        },
        "characters": characters,
    }
    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {manifest['total_frames']} native-resolution RGBA pose frames")
    print(manifest_path)


if __name__ == "__main__":
    main()
