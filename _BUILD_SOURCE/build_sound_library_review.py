"""Build the non-destructive browser audition page for the 2026-08-28 sound library.

The source MP3s remain under _ART_SOURCES. This script only measures them and creates
review metadata/waveform previews under docs; it never writes into assets/game/sounds.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_ART_SOURCES" / "audio" / "sound_library_2026-08-28" / "raw"
OUT = ROOT / "docs" / "sound-library-review"
WAVES = OUT / "waveforms"


CATEGORY_ORDER = [
    "Automatic Weapons",
    "Shotguns",
    "Lasers & Energy Weapons",
    "Missiles",
    "Explosions & Heavy Ordnance",
    "Pilot Specials & Elements",
    "Transformation & Fusion",
    "Shields",
    "Teleport & Portals",
    "UI, Pickups & Radar",
    "Unsorted Genesis FX",
]


def identity(filename: str) -> dict[str, str]:
    n = filename.lower()
    rules = [
        ("heavy_machine", "Automatic Weapons", "Heavy Machine Gun", "Lizzie heavy machine gun; enemy/boss heavy bursts", "heavy-machine-gun"),
        ("shotgun_reloa", "Shotguns", "Shotgun Reload", "Decker reload or randomized reload alternate", "shotgun-reload"),
        ("shotgun_sound", "Shotguns", "Shotgun Blast", "Decker incendiary shotgun primary blast", "shotgun-blast"),
        ("laser_blast", "Lasers & Energy Weapons", "Laser Blast", "Laser Cannon shot, enemy photon shot, or impact layer", "laser-blast"),
        ("laser_energy", "Lasers & Energy Weapons", "Laser Energy", "Beam charge/release, sustained laser accent, or boss laser", "laser-energy"),
        ("missile_lauch", "Missiles", "Missile Launch", "Player Volley Missile or enemy Jungle missile launch", "missile-launch"),
        ("missile_blast", "Explosions & Heavy Ordnance", "Missile Blast", "Missile detonation primary", "missile-blast"),
        ("missile_explo", "Explosions & Heavy Ordnance", "Missile Explosion", "Missile detonation alternate or layered tail", "missile-explosion"),
        ("atomic_bomb_b", "Explosions & Heavy Ordnance", "Atomic Bomb Build", "Lizzie atomic-bomb warning/build layer", "atomic-build"),
        ("atomic_bomb_d", "Explosions & Heavy Ordnance", "Atomic Bomb Detonation", "Lizzie atomic-bomb detonation primary", "atomic-detonation"),
        ("nuclear_bomb", "Explosions & Heavy Ordnance", "Nuclear Bomb", "Cole nuclear strike launch/detonation candidate", "nuclear-bomb"),
        ("bomb_sound", "Explosions & Heavy Ordnance", "Bomb Impact", "General bomb impact or secondary explosion", "bomb-impact"),
        ("shadow_orb_bl", "Pilot Specials & Elements", "Shadow Orb Blast", "Gravity Mode Shadow Orb charged detonation", "shadow-orb-blast"),
        ("shadow_orb_la", "Pilot Specials & Elements", "Shadow Orb Launch", "Gravity Mode Shadow Orb release/flight", "shadow-orb-launch"),
        ("sonic_boom", "Pilot Specials & Elements", "Sonic Boom", "Cole Sonic Boom half/full/impact candidates", "sonic-boom"),
        ("chain_lightni", "Pilot Specials & Elements", "Chain Lightning", "Chain Lightning release or hit variation", "chain-lightning"),
        ("flameth", "Pilot Specials & Elements", "Flamethrower", "Flamethrower ignition, release, or short attack accent", "flamethrower"),
        ("howling_wind", "Pilot Specials & Elements", "Howling Wind / Crush", "Stage 1 wind vortex, rotor tempest, or wind impact", "jungle-wind"),
        ("energy_buildi", "Transformation & Fusion", "Energy Build", "Long Gravity Mode transformation charge or boss phase build", "energy-build"),
        ("fusion_energy", "Transformation & Fusion", "Fusion Energy", "Gravity Mode spiral/scatter/snap/fusion phase candidate", "fusion-energy"),
        ("ship_fusing", "Transformation & Fusion", "Ship Fusion", "Gravity Mode armor pieces locking together", "ship-fusion"),
        ("spaceship_fusing", "Transformation & Fusion", "Spaceship Fusion", "Gravity Mode final completed-hull fusion", "ship-fusion-final"),
        ("mega_shield", "Shields", "Mega Shield", "Axel Mega Shield activation, impact, or break", "mega-shield"),
        ("video_game_te", "Teleport & Portals", "Teleport", "Stage 8 enemy teleport arrival/departure", "teleport"),
        ("radar_sounds", "UI, Pickups & Radar", "Radar", "Campaign radar, lock, or scanner cue", "radar"),
        ("special_item", "UI, Pickups & Radar", "Special Item", "Special-ability pickup, reveal, or equip cue", "special-item"),
        ("letter_input", "UI, Pickups & Radar", "Letter Input", "Password-entry keypress", "letter-input"),
        ("sega_genesis", "Unsorted Genesis FX", "Unidentified Genesis FX", "Audition before assigning; source filename is truncated", "unsorted-genesis"),
    ]
    for token, category, label, use, group in rules:
        if token in n:
            return {"category": category, "label": label, "proposedUse": use, "group": group}
    return {
        "category": "Unsorted Genesis FX",
        "label": "Unidentified Sound",
        "proposedUse": "Audition before assigning",
        "group": "unsorted",
    }


def probe(path: Path) -> dict:
    raw = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,bit_rate:stream=sample_rate,channels",
            "-of", "json", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(raw.stdout)
    stream = data.get("streams", [{}])[0]
    fmt = data.get("format", {})
    volume = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    mean = re.search(r"mean_volume:\s*([-\d.]+) dB", volume)
    peak = re.search(r"max_volume:\s*([-\d.]+) dB", volume)
    return {
        "duration": round(float(fmt.get("duration", 0)), 3),
        "bitRateKbps": round(float(fmt.get("bit_rate", 0)) / 1000),
        "sampleRate": int(stream.get("sample_rate", 0)),
        "channels": int(stream.get("channels", 0)),
        "meanDb": float(mean.group(1)) if mean else None,
        "peakDb": float(peak.group(1)) if peak else None,
    }


def variant_number(filename: str) -> int | None:
    found = re.search(r"#(\d+)-", filename)
    return int(found.group(1)) if found else None


def make_waveform(source: Path, output: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-loglevel", "error", "-y", "-i", str(source),
            "-filter_complex", "aformat=channel_layouts=mono,showwavespic=s=720x96:colors=0x66f2b3",
            "-frames:v", "1", str(output),
        ],
        check=True,
    )


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing review source: {SOURCE}")
    OUT.mkdir(parents=True, exist_ok=True)
    WAVES.mkdir(parents=True, exist_ok=True)

    entries = []
    for path in sorted(SOURCE.glob("*.mp3"), key=lambda item: item.name.lower()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        sound_id = digest[:12]
        info = identity(path.name)
        metrics = probe(path)
        wave = WAVES / f"{sound_id}.png"
        make_waveform(path, wave)
        flags = []
        if metrics["duration"] >= 5:
            flags.append("long-form")
        if metrics["peakDb"] is not None and metrics["peakDb"] > -0.5:
            flags.append("hot-peak")
        if metrics["meanDb"] is not None and metrics["peakDb"] is not None and metrics["peakDb"] - metrics["meanDb"] < 7:
            flags.append("dense")
        entries.append({
            "id": sound_id,
            "file": path.name,
            "variation": variant_number(path.name),
            "sha256": digest,
            "waveform": f"waveforms/{wave.name}",
            "defaultDecision": "undecided",
            "flags": flags,
            **info,
            **metrics,
        })

    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry["sha256"]] = counts.get(entry["sha256"], 0) + 1
    for entry in entries:
        entry["exactDuplicateCount"] = counts[entry["sha256"]]

    order = {name: index for index, name in enumerate(CATEGORY_ORDER)}
    entries.sort(key=lambda entry: (order.get(entry["category"], 999), entry["group"], entry["variation"] or 0, entry["file"]))
    manifest = {
        "title": "Bullets of Fury — New Sound Library Review",
        "source": "sounds.zip (received 2026-08-28)",
        "productionUntouched": True,
        "audioBase": "../../_ART_SOURCES/audio/sound_library_2026-08-28/raw/",
        "categoryOrder": CATEGORY_ORDER,
        "entries": entries,
    }
    payload = json.dumps(manifest, indent=2, ensure_ascii=False)
    (OUT / "manifest.json").write_text(payload + "\n", encoding="utf-8")
    (OUT / "manifest.js").write_text("window.SOUND_REVIEW = " + payload + ";\n", encoding="utf-8")
    print(f"Built sound review manifest: {len(entries)} sounds across {len(set(e['category'] for e in entries))} categories")
    print(f"Hot peaks: {sum('hot-peak' in e['flags'] for e in entries)}")
    print(f"Long-form: {sum('long-form' in e['flags'] for e in entries)}")
    print(f"Exact duplicate files: {sum(e['exactDuplicateCount'] > 1 for e in entries)}")


if __name__ == "__main__":
    main()
