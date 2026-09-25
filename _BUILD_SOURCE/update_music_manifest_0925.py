"""Regenerate only BOFA.music mappings after the 0925 track archive.

The manifest is generated and enormous. This focused owner keeps its JSON
structure and key order intact, updates the audio namespace, and removes one
old music path accidentally registered as an image (fierceplanes).
"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "assets/manifest.js"
src = path.read_text(encoding="utf-8")
prefix = "window.BOFA="
start = src.index(prefix) + len(prefix)
obj, used = json.JSONDecoder().raw_decode(src[start:])
assert isinstance(obj.get("music"), dict)
music = obj["music"]

patch = {
    "stage7mus": "stage7_over_the_horizon_0925.mp3",
    "deathtrap": "stage6_city_in_the_sky.mp3",
    "boss1": "boss1_helicopterboss.mp3",
    "boss2": "boss2_bossfight3_loud_0920.mp3",
    "boss3": "boss3_pandemonium.mp3",
    "boss4": "boss4_cowboyfromhell_loud_0920.mp3",
    "boss5": "boss5_deadly_night.mp3",
    "boss8": "final_boss_phase1_0925.mp3",
    "boss8p3": "final_boss_phase3_the_final_confrontation_0925.mp3",
    "finalCinematic": "cinematic_final_level_0925.mp3",
}
for key, file in patch.items():
    music[key] = "assets/game/music/" + file
music["boss"] = music["boss1"]
music["ironcage"] = music["boss8"]
music["mini1"] = "assets/game/music/miniboss_fireboss.mp3"
music["mini2"] = music["mini1"]
music["mini3"] = music["lvl3"]

missing = {key: loc for key, loc in music.items() if not (root / loc).is_file()}
assert not missing, missing
encoded = json.dumps(obj, separators=(",", ":"), ensure_ascii=True)
updated = src[:start] + encoded + src[start+used:]
orphan = '"fierceplanes":"assets/game/music/stage7_not_another_sewer.mp3",'
assert updated.count(orphan) == 1
updated = updated.replace(orphan, "", 1)
path.write_text(updated, encoding="utf-8", newline="\n")
print("BOFA music paths resolve:", len(music), "keys; removed orphan image key fierceplanes")
