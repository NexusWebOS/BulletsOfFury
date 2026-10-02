"""Fully wet, note-quantized channel vocoder for Mike's supplied recordings.

The recording contributes amplitude envelopes and articulation, never a dry
audio path. Oscillators replace its vocal excitation. No model or voice service.
"""
import numpy as np

RATE = 22050


def track_pitch(x):
    hop, size = 220, 1024
    starts = np.arange(0, len(x), hop)
    padded = np.pad(x, (size//2, size//2))
    pitches, strengths = [], []
    lo, hi = int(RATE/420), int(RATE/65)
    win = np.hanning(size)
    for start in starts:
        frame = padded[start:start+size].astype(np.float64)
        frame -= frame.mean()
        frame *= win
        spec = np.fft.rfft(frame, 2048)
        corr = np.fft.irfft(spec*np.conj(spec), 2048)[:size]
        # Compensate for fewer/windowed samples at larger lags.
        norm = np.fft.irfft(abs(np.fft.rfft(win, 2048))**2, 2048)[:size]
        corr /= np.maximum(norm, 1e-9)
        corr /= max(corr[0], 1e-12)
        peaks = np.flatnonzero((corr[lo:hi]>corr[lo-1:hi-1]) &
                               (corr[lo:hi]>=corr[lo+1:hi+1]))+lo
        if not len(peaks) or np.mean(frame*frame)<1e-6:
            pitches.append(0.0); strengths.append(0.0); continue
        best = max(float(corr[i]) for i in peaks)
        candidates = [i for i in peaks if corr[i]>=max(.5, best*.91)]
        if not candidates:
            pitches.append(0.0); strengths.append(0.0); continue
        lag = candidates[0]
        # Sub-sample parabolic interpolation before hard note quantization.
        denominator = corr[lag-1]-2*corr[lag]+corr[lag+1]
        delta = .5*(corr[lag-1]-corr[lag+1])/denominator if abs(denominator)>1e-10 else 0
        pitches.append(RATE/(lag+np.clip(delta,-.5,.5)))
        strengths.append(float(np.clip(corr[lag],0,1)))
    return starts, np.asarray(pitches), np.asarray(strengths)


def quantized_notes(pitches, strengths, role):
    shift, limits = (-9,(31,43)) if role=='boss' else (-6,(34,46))
    valid=(pitches>0)&(strengths>.5)
    raw=np.full(len(pitches),38.0 if role=='boss' else 41.0)
    raw[valid]=69+12*np.log2(pitches[valid]/440)+shift
    # Continue the last note across consonants; do not invent a pitch for noise.
    for i in range(1,len(raw)):
        if not valid[i]:raw[i]=raw[i-1]
    raw=np.median(np.lib.stride_tricks.sliding_window_view(np.pad(raw,(2,2),mode='edge'),5),axis=1)
    notes=np.clip(np.rint(raw),*limits).astype(int)
    # 30 ms stability gate suppresses tracker chatter, then retunes instantly.
    for i in range(1,len(notes)-2):
        if notes[i]!=notes[i-1] and not np.all(notes[i:i+3]==notes[i]):notes[i]=notes[i-1]
    return notes, valid, shift


def vocode(x, role):
    x=np.asarray(x,dtype=np.float64)
    starts,pitches,strengths=track_pitch(x)
    notes,valid,shift=quantized_notes(pitches,strengths,role)
    # Piecewise constant frequencies give real hard correction, with continuous
    # oscillator phase to avoid clicks when the note changes. All original voice
    # pitch and phase are discarded by the synthesis stage below.
    sample_notes=notes[np.minimum(np.arange(len(x))//220,len(notes)-1)]
    frequencies=440*2.0**((sample_notes-69)/12)
    phase=np.cumsum(frequencies)/RATE
    saw=2*(phase%1)-1
    pulse=np.where((phase%1)<.35,1.0,-1.0)
    carrier=.70*saw+.22*pulse+.08*np.sin(np.pi*phase)
    noise=np.random.default_rng(1001 if role=='boss' else 1002).standard_normal(len(x))*.42
    size,hop=2048,256
    win=np.sqrt(np.hanning(size))
    freqs=np.fft.rfftfreq(size,1/RATE)
    centers=np.geomspace(80,9600,42)
    edges=np.geomspace(80/(centers[1]/centers[0]),9600*(centers[1]/centers[0]),44)
    bands=[]
    for i in range(42):
        band=np.minimum((freqs-edges[i])/(edges[i+1]-edges[i]),
                        (edges[i+2]-freqs)/(edges[i+2]-edges[i+1]))
        band=np.maximum(0,band);bands.append(band/max(band.sum(),1e-9))
    bands=np.asarray(bands)
    formant=2**((-5 if role=='boss' else -3)/12)
    pad=size//2
    source=np.pad(x,(pad,size));synth=np.pad(carrier,(pad,size));hiss=np.pad(noise,(pad,size))
    output=np.zeros(len(source));weight=np.zeros(len(source))
    for start in range(0,len(source)-size,hop):
        a=np.fft.rfft(source[start:start+size]*win)
        c=np.fft.rfft(synth[start:start+size]*win)
        n=np.fft.rfft(hiss[start:start+size]*win)
        confidence=strengths[min(max(0,start)//220,len(strengths)-1)]
        noisy=.10 if confidence>.5 else .82
        high=np.clip((freqs-3200)/2200,0,1)
        noise_mix=noisy+(1-noisy)*high
        c=c*(1-noise_mix)+n*noise_mix
        source_env=np.sqrt(bands@(abs(a)**2)+1e-12)
        # Shift the vocal-tract resonances too; lowering F0 alone retains identity.
        target=np.interp(centers/formant,centers,source_env,left=source_env[0],right=0)
        carrier_env=np.sqrt(bands@(abs(c)**2)+1e-12)
        gain=np.minimum(target/np.maximum(carrier_env,.002),12)
        spectrum=c*np.interp(freqs,centers,gain,left=0,right=0)
        frame=np.fft.irfft(spectrum,size)*win
        output[start:start+size]+=frame;weight[start:start+size]+=win*win
    output=(output/np.maximum(weight,1e-8))[pad:pad+len(x)]
    # Short hardware coloration is fully wet too: there is no natural double.
    output=np.tanh(output*2.4)/2.0
    delay=round(.0037*RATE);output[delay:]+=.18*output[:-delay].copy()
    stats={'processor':'42-band fully wet vocoder with hard chromatic note correction',
           'dryVoiceMix':0,'wetVoiceMix':1,'pitchShiftSemitones':shift,
           'formantShiftSemitones':-5 if role=='boss' else -3,
           'retune':'instant after 30 ms note stability gate','voicedFrames':int(valid.sum()),
           'inputVoicedMedianHz':float(np.median(pitches[valid])) if valid.any() else 0,
           'carrierMedianHz':float(np.median(440*2.0**((notes[valid]-69)/12))) if valid.any() else 0,
           'carrierMidiNotes':sorted(set(notes[valid].tolist())),
           'durationSamples':len(output),'sampleRate':RATE}
    return output.astype(np.float32),stats
