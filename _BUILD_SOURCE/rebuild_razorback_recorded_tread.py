"""Rebuild the Razorback tread loop from the archived motor and CC0 field recording.

Source: 77Pacer, "Tank Tread", Freesound 425271, CC0 1.0.
The original recording is a rolling garage door that reads as heavy treads.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import wave

import numpy as np


ROOT = Path(__file__).resolve().parent.parent
SOUNDS = ROOT / "assets" / "game" / "sounds"
SOURCE = SOUNDS / "tank_tread_77pacer_cc0_source.mp3"
MOTOR = SOUNDS / "unused_x" / "rzb_tank_tread_synth_0919.wav"
OUTPUT = SOUNDS / "rzb_tank_tread_loop_0919.wav"
RATE = 22050


def read_mono(path):
    with wave.open(str(path), "rb") as wav:
        assert (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) == (1, 2, RATE)
        return np.frombuffer(wav.readframes(wav.getnframes()), dtype="<i2").astype(np.float64) / 32768


def main():
    with TemporaryDirectory() as tmp:
        decoded = Path(tmp) / "recording.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(SOURCE),
                        "-ac", "1", "-ar", str(RATE), "-c:a", "pcm_s16le", str(decoded)], check=True)
        record = read_mono(decoded)
    motor = read_mono(MOTOR)
    n, seam = RATE * 2, int(RATE * .14)
    record = record[int(.25 * RATE):int(.25 * RATE) + n + seam]
    assert len(record) == n + seam
    record -= np.convolve(record, np.ones(121) / 121, mode="same")
    record *= .15 / max(1e-8, float(np.sqrt(np.mean(record ** 2))))
    motor = motor[:n + seam]
    motor *= .115 / max(1e-8, float(np.sqrt(np.mean(motor ** 2))))
    mixed = np.tanh((record + motor) * 1.65) * .82
    loop = mixed[:n].copy()
    fade = np.linspace(0, 1, seam)
    loop[:seam] = mixed[n:n + seam] * (1 - fade) + mixed[:seam] * fade
    edge = int(RATE * .006)
    join = (loop[0] + loop[-1]) * .5
    ramp = np.linspace(0, 1, edge)
    loop[:edge] = join + (loop[:edge] - join) * ramp
    loop[-edge:] = join + (loop[-edge:] - join) * ramp[::-1]
    assert abs(loop[0] - loop[-1]) < 1e-6
    pcm = np.round(np.clip(loop, -1, 1) * 32767).astype("<i2")
    with wave.open(str(OUTPUT), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(pcm.tobytes())
    print(OUTPUT, "seconds", len(pcm) / RATE, "RMS", float(np.sqrt(np.mean(loop ** 2))))


if __name__ == "__main__":
    main()
