"""Deterministic, periodic helicopter rotor bed. No external recordings or licenses."""
from pathlib import Path
import numpy as np,wave,json,hashlib
R=Path(__file__).resolve().parents[1]
rate=44100;duration=6;n=rate*duration;t=np.arange(n)/rate;f=np.fft.rfftfreq(n,1/rate);rng=np.random.default_rng(914)
def noise(lo,hi):
 spectrum=np.exp(1j*rng.uniform(0,2*np.pi,len(f)))
 shape=(1-np.exp(-(f/max(1,lo))**4))*np.exp(-(f/hi)**4)/np.sqrt(np.maximum(f,lo));shape[0]=0
 a=np.fft.irfft(spectrum*shape,n);return a/np.std(a)
# Frequencies occupy exact Fourier bins so the six-second loop repeats continuously.
rotor=18;phase=2*np.pi*rotor*t+.17*np.sin(2*np.pi*3*t)
pulse=((1+np.cos(phase))*.5)**7
low=noise(35,370);air=noise(220,2400)
thump=.40*np.sin(phase)+.15*np.sin(phase*2)+.09*np.sin(phase*3)
rumble=.13*np.sin(2*np.pi*90*t+.15*np.sin(2*np.pi*3*t))+.065*np.sin(2*np.pi*180*t)
signal=thump+rumble+low*(.10+.30*pulse)+air*(.025+.12*pulse)
signal=np.tanh(signal*1.1);signal-=signal.mean();signal*=.78/np.max(np.abs(signal))
pcm=np.round(signal*32767).astype('<i2');out=R/'assets/game/sounds/overlord_helicopter_rotor.wav'
with wave.open(str(out),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(pcm.tobytes())
stats={'sampleRate':rate,'seconds':duration,'channels':1,'peak':float(np.max(np.abs(signal))),'rms':float(np.sqrt(np.mean(signal**2))),'seamJump':float(abs(signal[0]-signal[-1])),'maxAdjacentJump':float(np.max(abs(np.diff(signal)))),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'provenance':'Original deterministic synthesis: periodic blade pulses, band-limited turbulent air and engine harmonics.'}
assert stats['seamJump']<=stats['maxAdjacentJump'] and stats['peak']<.8
q=R/'_shots/rotor_audio_0914';q.mkdir(exist_ok=True);(q/'audio.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
print(json.dumps(stats))
