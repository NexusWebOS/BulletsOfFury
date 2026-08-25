from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def verify_characters() -> dict:
    manifest_path = ROOT / "assets/game/cinematic_characters/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checked = 0
    for character in manifest["characters"]:
        assert character["master_corner_alpha"] == [0, 0, 0, 0]
        for frame in character["frames"]:
            path = ROOT / frame["file"]
            image = Image.open(path).convert("RGBA")
            assert list(image.size) == frame["size"]
            assert frame["corner_alpha"] == [0, 0, 0, 0]
            assert frame["exposed_bright_matte_pixels"] == 0
            assert image.getchannel("A").getbbox() is not None
            checked += 1
    assert checked == 54
    return {"characters": len(manifest["characters"]), "pose_frames": checked}


def verify_backgrounds() -> dict:
    manifest_path = ROOT / "assets/game/cinematic_backgrounds/fury_hq/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for scene in manifest["scenes"]:
        path = ROOT / scene["file"]
        image = Image.open(path)
        assert list(image.size) == scene["native_size"] == [1672, 941]
    assert len(manifest["scenes"]) == 9
    return {"hq_backgrounds": len(manifest["scenes"]), "native_size": [1672, 941]}


def verify_explosions() -> dict:
    manifest_path = ROOT / "assets/game/generated_cinematic/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checked = 0
    final_visibility: dict[str, int] = {}
    for name, animation in manifest["explosions"].items():
        assert animation["runtime_frame_count"] == 32
        assert animation["whole_sprite_fade"] is False
        assert len(animation["visibility_256x256"]) == 32
        assert all(row["visible_pixels"] > 0 for row in animation["visibility_256x256"])
        assert animation["visibility_256x256"][-1]["max_alpha"] == 255
        final_visibility[name] = animation["visibility_256x256"][-1]["visible_pixels"]

        for label, size_entry in animation["sizes"].items():
            width, height = (int(value) for value in label.split("x"))
            frame_dir = ROOT / size_entry["frames"]
            frames = sorted(frame_dir.glob("frame_*.png"))
            assert len(frames) == 32
            for frame in frames:
                image = Image.open(frame).convert("RGBA")
                assert image.size == (width, height)
                alpha = np.asarray(image.getchannel("A"), dtype=np.uint8)
                assert int(alpha.max()) > 0
                checked += 1

    assert len(manifest["explosions"]) == 8
    assert checked == 1280
    return {
        "explosion_families": len(manifest["explosions"]),
        "runtime_png_frames": checked,
        "transparent_frames": 0,
        "final_visible_pixels_256": final_visibility,
    }


def main() -> None:
    report = {
        "characters": verify_characters(),
        "backgrounds": verify_backgrounds(),
        "explosions": verify_explosions(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
