from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets" / "game" / "cinematic_ships"
PILOTS = ("axel", "freezer", "falva", "lizzie", "yuri", "maverick", "juggernaut", "decker", "cole")
VIEWS = ("01_top_down", "02_front_left_3q", "03_front_right_3q", "04_rear_left_3q", "05_rear_right_3q", "06_hard_bank")
REPAIRS = (
    ("falva", "02_front_left_3q"),
    ("falva", "03_front_right_3q"),
    ("falva", "06_hard_bank"),
    ("lizzie", "04_rear_left_3q"),
    ("lizzie", "05_rear_right_3q"),
    ("decker", "02_front_left_3q"),
    ("decker", "03_front_right_3q"),
    ("decker", "06_hard_bank"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_rgba(path: Path, size: tuple[int, int] | None = None) -> Image.Image:
    assert path.is_file(), f"missing image: {path}"
    image = Image.open(path)
    assert image.mode == "RGBA", f"wrong mode: {path.name} -> {image.mode}"
    if size is not None:
        assert image.size == size, f"wrong size: {path.name} -> {image.size}"
    rgba = np.asarray(image)
    alpha = rgba[..., 3]
    assert int(alpha.min()) == 0 and int(alpha.max()) == 255, f"incomplete alpha range: {path.name}"
    assert np.all(rgba[..., :3][alpha == 0] == 0), f"nonzero RGB under transparent pixels: {path.name}"
    return image


def main() -> None:
    manifest_path = PACK / "manifest.json"
    for required in (
        manifest_path,
        PACK / "README.md",
        PACK / "GENERATION_PROMPTS.md",
        PACK / "previews" / "cinematic_ships_9pilots_contact.jpg",
        PACK / "previews" / "cinematic_ships_tail_repairs_contact.jpg",
    ):
        assert required.is_file(), f"missing pack file: {required}"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["pilot_count"] == 9
    assert manifest["views_per_pilot"] == 6
    assert manifest["total_frames"] == 54
    assert manifest["master_size"] == [1536, 1024]
    assert manifest["fixed_frame_size"] == [512, 512]
    assert [entry["pilot"] for entry in manifest["pilots"]] == list(PILOTS)
    assert [entry["id"] for entry in manifest["view_order"]] == list(VIEWS)
    assert manifest["continuity_repair_count"] == len(REPAIRS)
    assert [(entry["pilot"], entry["view"]) for entry in manifest["continuity_repairs"]] == list(REPAIRS)

    total = 0
    for pilot in manifest["pilots"]:
        master = ROOT / pilot["master"]
        image = verify_rgba(master, (1536, 1024))
        image.close()
        assert pilot["master_sha256"] == sha256(master), f"master hash drift: {master.name}"
        metrics = pilot["edge_metrics"]
        assert metrics["alpha_extrema"] == [0, 255]
        assert metrics["transparent_rgb_zero"] is True
        assert metrics["semi_transparent_key_dominance_p95"] <= 10.0, f"possible key halo: {pilot['pilot']}"
        assert 0.60 < metrics["transparent_fraction"] < 0.95
        assert len(pilot["views"]) == 6

        for expected, view in zip(VIEWS, pilot["views"], strict=True):
            assert view["id"] == expected
            frame = ROOT / view["frame_512"]
            cutout = ROOT / view["cutout_native"]
            frame_image = verify_rgba(frame, (512, 512))
            frame_image.close()
            cutout_image = verify_rgba(cutout)
            assert cutout_image.size == tuple(view["cutout_size"])
            assert cutout_image.width <= 512 and cutout_image.height <= 512
            cutout_image.close()
            assert view["frame_sha256"] == sha256(frame), f"frame hash drift: {frame}"
            assert view["cutout_sha256"] == sha256(cutout), f"cutout hash drift: {cutout}"
            expected_repair = (pilot["pilot"], view["id"]) in REPAIRS
            assert bool(view["continuity_repair_source"]) is expected_repair
            if expected_repair:
                assert (ROOT / view["continuity_repair_source"]).is_file()
            total += 1

    assert total == 54
    print("PASS: 9/9 canonical pilot ships verified with six cinematic views each (54 frames).")
    print("PASS: all fixed frames are 512x512 RGBA and all masters are 1536x1024 RGBA.")
    print("PASS: transparent RGB is zero and semi-transparent edges pass the no-halo key-contamination gate.")
    print(f"PASS: {len(REPAIRS)} targeted tail-continuity repairs are present and tracked in the manifest.")


if __name__ == "__main__":
    main()
