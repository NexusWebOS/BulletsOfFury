#!/usr/bin/env python3
"""Build the two real-sample Decker cues added by the 0830 audio repair.

The approved Shotgun #2 source stays untouched.  The casing cue comes from the
project's own sound-engine preview bank.  Both outputs are short PCM WAVs so a
held trigger cannot queue long overlapping media elements.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "_ART_SOURCES" / "audio" / "sound_library_2026-08-28" / "raw"
ENGINE = ROOT / "_SFXGenerator_upload" / "packs" / "preview" / "demo"
OUT = ROOT / "assets" / "game" / "sounds"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def cut(src: Path, dst: Path, end: float, gain: float) -> None:
    fade = max(0.0, end - 0.035)
    filt = (
        f"atrim=start=0:end={end},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.004,afade=t=out:st={fade}:d=0.035,"
        f"volume={gain}dB,alimiter=limit=0.92"
    )
    subprocess.run(
        [
            FFMPEG,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(src),
            "-af",
            filt,
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            str(dst),
        ],
        check=True,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cut(
        RAW / "16-bit_shotgun_sound_#2-1787958510789.mp3",
        OUT / "reviewed_decker_shotgun.wav",
        0.82,
        1.5,
    )
    cut(
        ENGINE / "shell_eject.mp3",
        OUT / "reviewed_decker_shell_eject.wav",
        0.42,
        -4.0,
    )
    for name in ("reviewed_decker_shotgun.wav", "reviewed_decker_shell_eject.wav"):
        path = OUT / name
        print(f"{path.relative_to(ROOT)}\t{path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
