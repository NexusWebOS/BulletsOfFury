#!/usr/bin/env python3
"""Build the 2026-08-29 user-approved BOF combat sound map.

The raw review bank remains untouched.  This script makes short, normalized PCM
WAVs for hot gameplay events and explicit two-part charge beds for Maverick and
Cole.  Timing choices come from the audition notes in the 2026-08-29 capture.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "_ART_SOURCES" / "audio" / "sound_library_2026-08-28" / "raw"
OUT = ROOT / "assets" / "game" / "sounds"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def run(*args: str) -> None:
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", *map(str, args)]
    subprocess.run(cmd, check=True)


def finish(path: Path) -> list[str]:
    return ["-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(path)]


def cut(src: str, dst: str, start: float, end: float, gain: float = 0.0) -> None:
    dur = end - start
    fade_out = max(0.0, dur - 0.025)
    flt = (
        f"atrim=start={start}:end={end},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.008,afade=t=out:st={fade_out}:d=0.025,"
        f"volume={gain}dB"
    )
    run("-i", RAW / src, "-af", flt, *finish(OUT / dst))


def pingpong_loop(src: str, dst: str, start: float, end: float, repeats: int = 2,
                  extra_filter: str = "") -> None:
    chains = []
    labels = []
    for i in range(repeats):
        normal = f"n{i}"
        reverse = f"r{i}"
        chains.append(
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS{extra_filter}[{normal}]"
        )
        chains.append(
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,areverse{extra_filter}[{reverse}]"
        )
        labels.extend([f"[{normal}]", f"[{reverse}]"])
    chains.append("".join(labels) + f"concat=n={len(labels)}:v=0:a=1[out]")
    run("-i", RAW / src, "-filter_complex", ";".join(chains), "-map", "[out]",
        *finish(OUT / dst))


def pitch_sequence(src: str, dst: str, start: float, chunk: float,
                   factors: tuple[float, ...], tail_filter: str = "") -> None:
    chains = []
    labels = []
    for i, factor in enumerate(factors):
        label = f"p{i}"
        chains.append(
            f"[0:a]atrim=start={start}:end={start + chunk},asetpts=PTS-STARTPTS,"
            f"asetrate=48000*{factor},aresample=48000,atempo={1 / factor}[{label}]"
        )
        labels.append(f"[{label}]")
    total = chunk * len(factors)
    chains.append(
        "".join(labels)
        + f"concat=n={len(labels)}:v=0:a=1,atrim=duration={total},"
          f"afade=t=in:st=0:d=0.012,afade=t=out:st={max(0, total - 0.012)}:d=0.012"
          f"{tail_filter}[out]"
    )
    run("-i", RAW / src, "-filter_complex", ";".join(chains), "-map", "[out]",
        *finish(OUT / dst))


def sonic_release() -> None:
    sources = (
        "Sonic_boom_16-bit_wa_#1-1787958471096.mp3",
        "Sonic_boom_16-bit_wa_#3-1787958477004.mp3",
        "Sonic_boom_16-bit_wa_#4-1787958481733.mp3",
    )
    inputs: list[str] = []
    for src in sources:
        inputs += ["-i", str(RAW / src)]
    flt = (
        "[0:a]asetrate=48000*0.84,aresample=48000,atempo=1.190476,volume=-2dB[low];"
        "[1:a]adelay=35|35,volume=-4dB[mid];"
        "[2:a]asetrate=48000*1.18,aresample=48000,atempo=0.847458,"
        "adelay=70|70,volume=-6dB[high];"
        "[low][mid][high]amix=inputs=3:duration=longest:normalize=0,"
        "alimiter=limit=0.88,afade=t=out:st=1.42:d=0.08[out]"
    )
    run(*inputs, "-filter_complex", flt, "-map", "[out]",
        *finish(OUT / "reviewed_cole_sonic_release.wav"))


def fusion_sequence() -> None:
    swirl = RAW / "ship_fusing_together_#2-1787959010826.mp3"
    lock = RAW / "16-bit_fusion_energy_#1-1787961238418.mp3"
    flt = (
        "[0:a]atrim=start=0.32:end=2.25,asetpts=PTS-STARTPTS,asplit=3[s0][s1][s2];"
        "[s0]asetrate=48000*0.88,aresample=48000,atempo=1.136364[a];"
        "[s1]asetrate=48000*1.05,aresample=48000,atempo=0.952381[b];"
        "[s2]asetrate=48000*1.24,aresample=48000,atempo=0.806452[c];"
        "[a][b][c]concat=n=3:v=0:a=1,atrim=duration=4.35,volume=-3dB[swirl];"
        "[1:a]atrim=start=1.01:end=3,asetpts=PTS-STARTPTS,adelay=3500|3500,volume=-2dB[lock];"
        "[swirl][lock]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.9[out]"
    )
    run("-i", swirl, "-i", lock, "-filter_complex", flt, "-map", "[out]",
        *finish(OUT / "reviewed_ship_fusion_sequence.wav"))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # Exact tail/middle choices approved during the review.
    cut("16-bit_heavy_machine_#1-1787959257666.mp3", "reviewed_enemy_heavy_mg.wav", .94, 1.50, -3)
    cut("16-bit_heavy_machine_#4-1787959253381.mp3", "reviewed_lizzie_heavy_mg.wav", .37, 1.50, -5)
    cut("16-bit_shotgun_reloa_#1-1787958539891.mp3", "reviewed_decker_reload.wav", 0, 1.50, 1)
    cut("16-bit_laser_blast_w_#2-1787959409830.mp3", "reviewed_enemy_laser.wav", .99, 1.50, 1)
    cut("16-bit_laser_energy__#3-1787961279936.mp3", "reviewed_maverick_helix_release.wav", 1.44, 2.71, -1)
    cut("16-bit_laser_energy__#4-1787961288870.mp3", "reviewed_laser_cannon.wav", .80, 1.58, 1)
    cut("16-bit_atomic_bomb_d_#1-1787958879980.mp3", "reviewed_lizzie_atom_launch.wav", 0, 2.25, -2)
    cut("16-bit_bomb_sound_#2-1787958606052.mp3", "reviewed_lizzie_atom_impact.wav", .405, 1.40, -1)
    cut("16-bit_shadow_orb_la_#2-1787958733173.mp3", "reviewed_shadow_orb_launch.wav", 0, 2.25, -2)
    cut("16-bit_mega_shield_#3-1787959489252.mp3", "reviewed_axel_mega_shield.wav", .548, 1.42, 1)
    cut("16-bit_special_item__#1-1787959505074.mp3", "reviewed_special_pickup.wav", .704, 1.46, 2)

    # Sustained beds use ping-pong construction so HTMLAudio loop boundaries do not click.
    pingpong_loop("Retro_16-bit_flameth_#4-1787958369906.mp3", "reviewed_flamethrower_loop.wav", .05, 1.45, 2, ",volume=-5dB")
    cut("Retro_16-bit_flameth_#4-1787958369906.mp3", "reviewed_flamethrower_start.wav", 0, .42, -4)
    cut("Retro_16-bit_flameth_#4-1787958369906.mp3", "reviewed_flamethrower_end.wav", 1.05, 1.50, -5)
    pingpong_loop("Howling_wind_and_cru_#1-1787958444750.mp3", "reviewed_stage6_wind_loop.wav", 0, 1.50, 2, ",volume=-7dB")

    # Fusion Energy 1 ending 8632: shared beam plus Maverick's rising two-part charge.
    fusion_8632 = "16-bit_fusion_energy_#1-1787961218632.mp3"
    cut(fusion_8632, "reviewed_player_laser_beam_start.wav", 0, .48, -4)
    cut(fusion_8632, "reviewed_player_laser_beam_loop.wav", .48, 2.48, -7)
    cut(fusion_8632, "reviewed_player_laser_beam_end.wav", 2.48, 3.0, -6)
    pitch_sequence(fusion_8632, "reviewed_maverick_charge_build.wav", .25, .30,
                   (.76, .90, 1.06, 1.24), ",volume=-4dB")
    pitch_sequence(fusion_8632, "reviewed_maverick_charge_loop.wav", .72, .50,
                   (.88, 1.04, 1.19, .88), ",tremolo=f=5:d=.22,volume=-7dB")

    fusion_sequence()
    cut("16-bit_fusion_energy_#1-1787961238418.mp3", "reviewed_ship_fusion_lock.wav", 1.01, 3.0, -2)

    # Cole combines all three sonic-wave candidates, with arcade low/high pitch layers.
    sonic_release()
    pitch_sequence("Sonic_boom_16-bit_wa_#1-1787958471096.mp3", "reviewed_cole_sonic_charge_start.wav",
                   .05, .24, (.72, .88, 1.08), ",volume=-6dB")
    pitch_sequence("Sonic_boom_16-bit_wa_#4-1787958481733.mp3", "reviewed_cole_sonic_charge_loop.wav",
                   .10, .50, (.82, 1.06, 1.22, .82), ",tremolo=f=4:d=.25,volume=-8dB")

    print("built reviewed SFX:")
    for path in sorted(OUT.glob("reviewed_*.wav")):
        print(f"  {path.relative_to(ROOT)}  {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
