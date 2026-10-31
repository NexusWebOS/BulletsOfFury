from pathlib import Path
import subprocess,shutil,json,imageio_ffmpeg,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/dracodia_possession_1030';D=R/'_ART_SOURCES/dracodia_possession_1030/audio';O=R/'assets/game/levels/stage_08/audio/possession_1030';D.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True);FF=imageio_ffmpeg.get_ffmpeg_exe()
sources=[R/'assets/game/levels/stage_08/audio/dracodia_1005/dracodia_shriek.mp3',R/'assets/game/shared/audio/sounds/mechScream.mp3']
for p in sources:shutil.copy2(p,D/p.name)
filters=[]
for name,pitch,echo in [('scream_a',2**(-3/12),'58|119|181'),('scream_b',2**(-5/12),'47|101|163')]:
 f=f'[0:a]aresample=44100,asetrate={44100*pitch:.4f},aresample=44100,highpass=f=95,afreqshift=shift=22,volume=.85[a];[1:a]aresample=44100,asetrate=46722,aresample=44100,highpass=f=180,volume=.33[b];[a][b]amix=inputs=2:duration=longest:normalize=0,aecho=.8:.9:{echo}:.38|.25|.15,alimiter=limit=.82,loudnorm=I=-12:TP=-1.8:LRA=5[out]'
 master=D/(name+'.wav');dest=O/(name+'.mp3');subprocess.run([FF,'-v','error','-y','-i',str(sources[0]),'-i',str(sources[1]),'-filter_complex',f,'-map','[out]','-ar','44100',str(master)],check=True)
 subprocess.run([FF,'-v','error','-y','-i',str(master),'-c:a','libmp3lame','-b:a','192k',str(dest)],check=True);filters.append(dict(name=name,filter=f,master=master.name,path=dest.relative_to(R).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(D/'manifest.json').write_text(json.dumps(dict(sources=[str(p.relative_to(R))for p in sources],pitch='-3 and -5 semitones; secondary metallic voice +1 semitone',processing='22Hz harmonic offset and short reverb reflections; normalized -12LUFS, -1.8dB true peak target',cues=filters),indent=2));print('Rendered two loud, clear robotic scream variants through the existing BOF stems')
