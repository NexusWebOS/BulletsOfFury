"""Generate dedicated Stage-2 lava vent warning and eruption sounds."""
from pathlib import Path
import math, random, wave, struct

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/game/sounds'
SR=44100

def write(name, seconds, sample):
    random.seed(918)
    n=int(seconds*SR); data=[]; lp=0.0
    for i in range(n):
        t=i/SR
        white=random.uniform(-1,1); lp=lp*.94+white*.06
        v=max(-1,min(1,sample(t,seconds,lp,white)))
        data.append(struct.pack('<h',int(v*32767)))
    with wave.open(str(OUT/name),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(b''.join(data))

def warn(t,d,lp,white):
    k=t/d; env=math.sin(math.pi*min(1,k))**.55
    rum=math.sin(math.tau*(54+28*k)*t)+.42*math.sin(math.tau*92*t)
    hiss=lp*(.25+.75*k)
    pulse=(.25+.75*max(0,math.sin(math.tau*(3+5*k)*t)))
    return (.28*rum+.50*hiss)*env*pulse

def erupt(t,d,lp,white):
    attack=min(1,t/.045);tail=max(0,1-t/d)**.42
    roar=.64*lp+.18*white
    sub=math.sin(math.tau*(42+18*t)*t)*math.exp(-t*1.7)
    crack=math.sin(math.tau*126*t)*math.exp(-t*7)
    return attack*tail*(roar*.82+sub*.28+crack*.20)

write('s2_geyser_warn_0918.wav',.95,warn)
write('s2_geyser_erupt_0918.wav',1.45,erupt)
print('wrote Stage-2 fire hazard cues')
