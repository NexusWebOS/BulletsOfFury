from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets" / "game" / "cinematic_level_transitions_topdown"
SIZE = (1672, 941)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest_path = PACK / "manifest.json"
    zones_path = PACK / "interaction_zones.json"
    prompt_path = PACK / "GENERATION_PROMPTS.md"
    preview_path = PACK / "previews" / "topdown_transitions_contact.jpg"
    for path in (manifest_path, zones_path, prompt_path, preview_path, PACK / "README.md"):
        assert path.is_file(), f"missing pack file: {path}"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["native_size"] == list(SIZE)
    assert manifest["stage_count"] == 9
    assert manifest["campaign_stages"] == 8
    assert manifest["bonus_stages"] == 1
    assert manifest["flow"] == "bottom_to_top"
    assert "top-down" in manifest["camera"] and "no horizon" in manifest["camera"]
    assert [entry["stage"] for entry in manifest["stages"]] == list(range(1, 10))
    assert sum(bool(entry["bonus"]) for entry in manifest["stages"]) == 1
    assert all(manifest["global_constraints"].values())

    for entry in manifest["stages"]:
        assert entry["environment_only"] is True
        assert entry["baked_entities"] == []
        assert entry["flow"] == "bottom_to_top"
        assert "top-down" in entry["camera"]
        path = ROOT / entry["file"]
        reference = ROOT / entry["source_reference"]
        assert path.is_file(), f"missing stage master: {path}"
        assert reference.is_file(), f"missing source reference: {reference}"
        with Image.open(path) as image:
            assert image.size == SIZE, f"wrong size: {path.name} -> {image.size}"
            assert image.mode == "RGB", f"wrong mode: {path.name} -> {image.mode}"
            image.verify()
        assert entry["sha256"] == sha256(path), f"hash drift: {path.name}"

    zones = json.loads(zones_path.read_text(encoding="utf-8"))
    assert zones["canvas"] == list(SIZE)
    assert zones["flow"] == "bottom_to_top"
    expected = {"entry_bottom", "travel_center", "left_interaction", "right_interaction", "exit_top"}
    assert set(zones["shared_recommended_zones"]) == expected
    for name, (x, y, width, height) in zones["shared_recommended_zones"].items():
        assert min(x, y, width, height) >= 0, f"negative zone: {name}"
        assert x + width <= SIZE[0] and y + height <= SIZE[1], f"zone outside canvas: {name}"

    print("PASS: 9/9 top-down transition masters verified at 1672x941 RGB.")
    print("PASS: camera, bottom-to-top flow and empty-environment constraints verified in the manifest.")
    print("PASS: all suggested interaction zones remain within the native canvas.")


if __name__ == "__main__":
    main()
