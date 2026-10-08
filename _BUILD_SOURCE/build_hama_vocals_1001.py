"""Mike's own performances -> robot voices and a clock-identical HAMA vocal mix.
No generated speech or cloud voice service. Input archives are lossless FLAC.
Run with --lead/--extras WAV paths once; subsequent builds use the archives.
"""
from pathlib import Path
import argparse,subprocess,json,hashlib,wave
import numpy as np
import imageio_ffmpeg
from hama_robot_dsp_1001 import vocode, RATE
R=Path(__file__).resolve().parents[1];SRC=R/'_ART_SOURCES/hama_vocals_1001';OUT=R/'assets/game/hama_vocals_1001';QA=R/'_shots/hama_hooks_1001'
for p in [SRC,OUT,QA]:p.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe();SR=44100;P=60/132.55;SECONDS=180.013;N=round(SECONDS*SR)
VOICE_REPORT={};MIX_NAME='HAMA.mp3';MUSIC_OUT=R/'assets/game/music'
def ff(args):
 p=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*map(str,args)],capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace'))
 return p.stdout
def decode(p,channels=1):
 args=['-i',p]
 if channels==1:args+=['-af','pan=mono|c0=0.5*c0+0.5*c1']
 return np.frombuffer(ff([*args,'-ar',SR,'-ac',channels,'-f','f32le','-']),dtype='<f4').reshape(-1,channels).copy()
def wav(p,x):
 if x.ndim==1:x=x[:,None]
 with wave.open(str(p),'wb') as w:w.setparams((x.shape[1],2,SR,0,'NONE','not compressed'));w.writeframes((np.clip(x,-.999,.999)*32767).astype('<i2').tobytes())
def mp3(p,x):
 tmp=QA/(p.stem+'.wav');wav(tmp,x);ff(['-i',tmp,'-map_metadata','-1','-c:a','libmp3lame','-b:a','192k',p])
def robot(p,role):
 print('Rendering fully synthetic robot:',p.stem,role,flush=True)
 raw=ff(['-i',p,'-af','pan=mono|c0=0.5*c0+0.5*c1,highpass=f=80,lowpass=f=9200,afftdn=nr=5:nf=-48','-ar',RATE,'-ac','1','-f','f32le','-'])
 synth,stats=vocode(np.frombuffer(raw,dtype='<f4'),role)
 # Resample and compress only the synthesized output. Never mix dry speech back.
 temp=QA/(p.stem+'_'+role+'_vocoder.wav')
 with wave.open(str(temp),'wb') as w:w.setparams((1,2,RATE,0,'NONE','not compressed'));w.writeframes((np.clip(synth,-.99,.99)*32767).astype('<i2').tobytes())
 graph='highpass=f=55,lowpass=f=7800,acompressor=threshold=0.07:ratio=4:attack=3:release=70,aecho=0.9:0.9:17|33:0.10|0.06,alimiter=limit=0.9:level=false'
 raw=ff(['-i',temp,'-af',graph,'-ar',SR,'-ac','1','-f','f32le','-'])
 x=np.frombuffer(raw,dtype='<f4').copy();x=x[:round((125.083605 if p.stem=='lead' else 31.783537)*SR)]
 hop=441;env=np.sqrt(np.mean(x[:len(x)//hop*hop].reshape(-1,hop)**2,axis=1));active=env[env>max(.01,float(env.max())*.06)]
 rms=float(np.sqrt(np.mean(active**2))) if len(active) else .1
 x*=min(4,(.20 if role=='boss' else .16)/max(rms,.001));x=np.tanh(x*1.05)/1.05
 VOICE_REPORT[p.stem+'_'+role]=stats
 return x.astype('float32')
ap=argparse.ArgumentParser();ap.add_argument('--lead');ap.add_argument('--extras');args=ap.parse_args()
sources={}
for name,external in [('lead',args.lead),('extras',args.extras)]:
 p=SRC/(name+'.flac')
 if external:
  original=Path(external);ff(['-i',original,'-map_metadata','-1','-c:a','flac',p]);sources[name]={'originalName':'lmfao.wav' if name=='lead' else 'extras.wav','sha256':hashlib.sha256(original.read_bytes()).hexdigest()}
 if not p.exists():raise FileNotFoundError('Supply --'+name+' for the first build')
 if not external and (SRC/'sources.json').exists():sources[name]=json.loads((SRC/'sources.json').read_text())[name]
(SRC/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
# Only the approved hooks and chants from extras enter the runtime song.
extra=robot(SRC/'extras.flac','crew')
voc=np.zeros((N,2),dtype=np.float32);events=[];captions=[]
def cap(t,end,text,who='boss'):
 captions.append({'t':round(t,3),'end':round(end,3),'text':text,'who':who})
def place(x,a,b,t,role,label,gain=1,pan=0):
 clip=x[round(a*SR):round(b*SR)].copy();fade=min(round(.012*SR),len(clip)//4)
 clip[:fade]*=np.linspace(0,1,fade);tail=min(round(.055*SR),len(clip)//4);clip[-tail:]*=np.linspace(1,0,tail)
 offset=round(t*SR);length=min(len(clip),N-offset)
 if offset<0 or length<=0:return
 voc[offset:offset+length,0]+=clip[:length]*gain*(1-max(0,pan)*.45)
 voc[offset:offset+length,1]+=clip[:length]*gain*(1+min(0,pan)*.45)
 events.append({'t':round(t,3),'end':round(t+length/SR,3),'sourceStart':a,'sourceEnd':b,'role':role,'label':label})
hooks=[(.2,1.4),(3.80,5.18),(7.20,8.85),(10.85,12.2)]
stops=[61.8,115.44,158.64]
for a,b in [(32.791,43.656),(59.951,72.626),(88.921,101.596),(176.2,179.9)]:
 for i,t in enumerate(np.arange(a,b,8*P)):
  sa,sb=hooks[i%len(hooks)]
  if t+sb-sa>b or any(t<s+3*P and t+sb-sa>s-1.25*P for s in stops):continue
  place(extra,sa,sb,float(t),'crew','chorus',pan=(-1 if i%2 else 1)*.38);cap(t,t+sb-sa,'CANT TOUCH THIS','crew')
for at,end in [(101.596,115.44-1.25*P),(145.051,158.64-1.25*P)]:
 place(extra,16.35,16.35+end-at-.08,at,'crew','breakdown chant',.88,.28)
 for i,t in enumerate(np.arange(at,end,2*P)):cap(t,min(t+2*P,end),'OH! OH-OH!','boss' if i%2 else 'crew')
assert all(e['label'] in {'chorus','breakdown chant'} for e in events)
assert all(c['text'] in {'CANT TOUCH THIS','OH! OH-OH!'} for c in captions)
music=decode(R/'assets/game/shared/audio/music/HAMA_Instrumental.mp3',2);bed=np.zeros_like(voc);bed[:min(N,len(music))]=music[:N]
# Slow, short duck envelopes; no frame-by-frame pumping or separate drifting player.
duck=np.ones(N,dtype=np.float32)*.82
for e in events:
 a=max(0,round((e['t']-.04)*SR));b=min(N,round((e['end']+.08)*SR));duck[a:b]=np.minimum(duck[a:b],.47)
hop=441;sample=duck[::hop];smooth=np.convolve(np.pad(sample,(5,5),mode='edge'),np.ones(11)/11,mode='valid');duck=np.interp(np.arange(N)/hop,np.arange(len(smooth)),smooth).astype('float32')
mix=bed*duck[:,None]+voc*.94;peak=float(np.abs(mix).max());mix*=min(1,.83/max(peak,1e-9));mp3(MUSIC_OUT/MIX_NAME,mix)
mp3(QA/'vocal_stem.mp3',voc*.8)
data={'music':'assets/game/music/'+MIX_NAME,'seconds':SECONDS,'bpm':132.55,'voiceTreatment':'deep-vocoder-hooks-only-v3','events':sorted(events,key=lambda e:e['t']),'captions':sorted(captions,key=lambda e:e['t'])}
(OUT/'cues.json').write_text(json.dumps(data,indent=2)+'\n')
(R/'assets/hama_vocals_art_1001.js').write_text('"use strict";\nconst HAMA_VOCALS_1001='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
decoded=decode(MUSIC_OUT/MIX_NAME,2)
report={'revision':'deep-vocoder-hooks-only-v3','vocalContent':['CANT TOUCH THIS','OH! OH-OH!'],'removedVerseStemPeak':float(np.abs(voc[round(12*SR):round(30*SR)]).max()),'voices':VOICE_REPORT,'events':len(events),'captions':len(captions),'seconds':len(decoded)/SR,'peak':float(np.abs(decoded).max()),'clippedSamples':int(np.count_nonzero(np.abs(decoded)>=1)),'rms':float(np.sqrt(np.mean(decoded**2))),'sourceHashes':sources,'originalInstrumentalPreserved':True}
(QA/'mastering.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
