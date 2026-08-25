from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets" / "game" / "cinematic_campaign"
MANIFEST_PATH = PACK / "manifest.json"
SCENE_SIZE = (1672, 941)
CHARACTERS = {
    "axel",
    "freezer",
    "falva",
    "lizzie",
    "yuri",
    "maverick",
    "juggernaut",
    "decker",
    "cole",
}


def resolve_repo_path(value: str) -> Path:
    return ROOT / Path(value)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_scene(path: Path) -> None:
    assert path.is_file(), f"missing scene: {path}"
    with Image.open(path) as image:
        assert image.size == SCENE_SIZE, f"wrong scene size: {path} -> {image.size}"
        image.verify()


def verify_transparent_asset(
    path: Path,
    expected_size: tuple[int, int] | None = None,
    *,
    require_binary_alpha: bool = False,
) -> None:
    assert path.is_file(), f"missing transparent asset: {path}"
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        if expected_size is not None:
            assert rgba.size == expected_size, f"wrong size: {path} -> {rgba.size}"
        alpha = rgba.getchannel("A")
        assert alpha.getbbox() is not None, f"empty alpha: {path}"
        w, h = rgba.size
        corners = [alpha.getpixel(point) for point in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
        assert corners == [0, 0, 0, 0], f"opaque corners: {path} -> {corners}"
        if require_binary_alpha:
            occupied_alpha_bins = {value for value, count in enumerate(alpha.histogram()) if count}
            assert occupied_alpha_bins.issubset({0, 255}), f"soft alpha/halo risk: {path}"


def main() -> None:
    assert MANIFEST_PATH.is_file(), "manifest.json is missing"
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["pack"] == "FURY HQ — Earth Division campaign cinematics"
    assert tuple(manifest["native_cutscene_size"]) == SCENE_SIZE

    branding = manifest["branding"]
    assert set(branding) == {"master_insignia", "horizontal_banner", "vertical_banner"}
    verify_transparent_asset(resolve_repo_path(branding["master_insignia"]), (1536, 1024))
    horizontal = resolve_repo_path(branding["horizontal_banner"])
    vertical = resolve_repo_path(branding["vertical_banner"])
    with Image.open(horizontal) as image:
        assert image.size == (1983, 793), f"wrong horizontal banner size: {image.size}"
        image.verify()
    with Image.open(vertical) as image:
        assert image.size == (1024, 1535), f"wrong vertical banner size: {image.size}"
        image.verify()

    exteriors = manifest["exteriors"]
    assert len(exteriors) == 3
    for record in exteriors.values():
        path = resolve_repo_path(record["file"])
        verify_scene(path)
        assert record["banner_text"] == "FURY HQ — EARTH DIVISION"
        assert record["branding_method"] == "fully generated in-scene architectural insignia"
        assert record["sha256"] == sha256(path), f"exterior hash drift: {path}"

    seated = manifest["seated_poses"]
    assert set(seated) == CHARACTERS
    for record in seated.values():
        path = resolve_repo_path(record["file"])
        verify_transparent_asset(path, tuple(record["native_size"]), require_binary_alpha=True)
        assert record["corner_alpha"] == [0, 0, 0, 0]
        assert record["sha256"] == sha256(path), f"seated pose hash drift: {path}"

    alliances = manifest["lounge_and_alliance_cutscenes"]
    pilots = manifest["pilot_campaign_cutscenes"]
    assert len(alliances) == 7
    assert set(pilots) == CHARACTERS
    for record in (*alliances.values(), *pilots.values()):
        verify_scene(resolve_repo_path(record["file"]))

    narrative = manifest["narrative"]
    assert narrative["division"] == "FURY HQ — Earth Division"
    assert narrative["command"] == {
        "commanding_officer": "cole",
        "air_commander": "axel",
        "right_hand": "freezer",
    }
    assert narrative["secrets"] == {
        "builder": "decker",
        "authorized_user": "cole",
        "systems": ["prototype lasers", "photon cannon"],
    }

    generation = manifest["generation"]
    assert "generated as an integrated physical part" in generation["text_policy"]

    primary_assets = 3 + len(exteriors) + len(seated) + len(alliances) + len(pilots)
    assert primary_assets == 31
    print(
        "PASS: 31 primary campaign assets verified "
        "(3 generated branding, 3 exterior, 9 seated, 7 alliance, 9 pilot)."
    )
    print("PASS: all 19 baked scenes are 1672x941 and all 9 seated cutouts use binary halo-free alpha.")
    print("PASS: all 3 exteriors use fully generated in-scene FURY HQ — EARTH DIVISION architectural signage.")


if __name__ == "__main__":
    main()
