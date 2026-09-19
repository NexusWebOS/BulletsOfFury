from pathlib import Path
import wave
import numpy as np

rate = 22050
seconds = 4
n = rate * seconds
t = np.arange(n, dtype=np.float64) / rate
rng = np.random.default_rng(9192026)

# All motors and tread impacts complete whole cycles in four seconds, so the
# loop seam carries the same phase instead of making a periodic click.
engine = (0.31 * np.sin(2 * np.pi * 52 * t)
          + 0.18 * np.sin(2 * np.pi * 104 * t + 0.4)
          + 0.09 * np.sin(2 * np.pi * 156 * t + 0.8))
engine *= 0.83 + 0.17 * np.sin(2 * np.pi * 2 * t - 0.5)

noise = rng.standard_normal(n)
rough = np.convolve(noise, np.ones(43) / 43, mode='same')
rough /= max(1e-9, np.max(np.abs(rough)))
rumble = rough * (0.12 + 0.035 * np.sin(2 * np.pi * 13 * t))

step = (t * 13) % 1
strike = np.exp(-step * 18)
clank = strike * (0.17 * np.sin(2 * np.pi * 312 * t)
                  + 0.085 * np.sin(2 * np.pi * 624 * t + 0.45))
grit = rng.standard_normal(n) * strike * 0.055
signal = engine + rumble + clank + grit

signal = np.tanh(signal * 1.35) * 0.73
# Remove the random layer's end-point jump. The periodic motor and tread beat
# retain their normal attack at the seam.
seam = int(rate * 0.06)
signal[-seam:] -= (signal[-1] - signal[0]) * np.linspace(0, 1, seam)
pcm = np.round(np.clip(signal, -1, 1) * 32767).astype('<i2')

dest = Path(__file__).resolve().parent.parent / 'assets/game/sounds/unused_x/rzb_tank_tread_synth_0919.wav'
with wave.open(str(dest), 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(rate)
    wav.writeframes(pcm.tobytes())
print(dest, len(pcm) / rate, float(np.sqrt(np.mean(signal**2))))
