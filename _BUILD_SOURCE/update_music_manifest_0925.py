"""Regenerate only BOFA.music mappings after the 0925 track archive.

The manifest is generated and enormous. This focused owner keeps its JSON
structure and key order intact, updates the audio namespace, and removes one
old music path accidentally registered as an image (fierceplanes).
"""
import json
from pathlib import Path

# Current catalog supersedes the historical 0925 assignments below.
from organize_music_1003 import organize
organize()
raise SystemExit(0)

root = Path(__file__).resolve().parents[1]
path = root / "assets/manifest.js"
src = path.read_text(encoding="utf-8")
prefix = "window.BOFA="
start = src.index(prefix) + len(prefix)
obj, used = json.JSONDecoder().raw_decode(src[start:])
assert isinstance(obj.get("music"), dict)
music = obj["music"]

patch = {
    "stage7mus": "Level7.mp3",
    "deathtrap": "Level6.mp3",
    "boss1": "Level1b.mp3",
    "boss2": "Level2b.mp3",
    "boss3": "Level3b.mp3",
    "boss4": "Level4b.mp3",
    "boss5": "Level5mb.mp3",
    "boss8": "Level8b.mp3",
    "boss8p3": "Level8b3.mp3",
    "finalCinematic": "FinalCinematic.mp3",
}
for key, file in patch.items():
    music[key] = "assets/game/music/" + file
music["boss"] = music["boss1"]
music["ironcage"] = music["boss8"]
music["mini1"] = "assets/game/levels/stage_01/audio/music/Level1mb.mp3"
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
