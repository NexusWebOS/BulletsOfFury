"""Rebuild Chronos' short strike from the existing Dracodia formation cue.

Run with Python and FFmpeg (or imageio-ffmpeg installed). Does not edit JS,
gameplay, or the source beam recording. Refuses a changed source hash.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'assets/game/shared/audio/sfx_0927/beam.mp3'
EXPECTED='ebeb6f8a5dbbc38df3975e5aebf662008175bcb3bcf0a2e1f06659fc4fbe9a80'
FILTERS='atrim=start=0:end=0.34,asetpts=PTS-STARTPTS,highpass=f=65,equalizer=f=2600:t=q:w=0.9:g=2,acompressor=threshold=0.18:ratio=2.2:attack=1.5:release=45:makeup=1.4,afade=t=in:st=0:d=0.002,afade=t=out:st=0.25:d=0.09,alimiter=limit=0.82:attack=2:release=35:level=false'

def main():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest!=EXPECTED:raise RuntimeError('Dracodia source changed; inspect it before rebuilding this derivative.')
    ff=shutil.which('ffmpeg')
    if not ff:
        import imageio_ffmpeg
        ff=imageio_ffmpeg.get_ffmpeg_exe()
    authored=ROOT/'_ART_SOURCES/chronos_lightning_audio_1026'
    runtime=ROOT/'assets/game/shared/audio/chronos_lightning_1026/strike.mp3'
    authored.mkdir(parents=True,exist_ok=True);runtime.parent.mkdir(parents=True,exist_ok=True)
    master=authored/'strike.wav'
    subprocess.run([ff,'-v','error','-y','-i',str(SOURCE),'-af',FILTERS,'-ar','48000','-ac','2','-c:a','pcm_s24le',str(master)],check=True)
    subprocess.run([ff,'-v','error','-y','-i',str(master),'-c:a','libmp3lame','-b:a','192k',str(runtime)],check=True)
    manifest={'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),'sourceCue':'combatBeam0927 / Dracodia rd27Lightning','sourceSha256':digest,'sourceLicense':'not supplied','pitchSemitones':0,'seconds':.34,'filters':FILTERS,'master':'_ART_SOURCES/chronos_lightning_audio_1026/strike.wav','runtime':str(runtime.relative_to(ROOT)).replace('\\','/'),'runtimeSha256':hashlib.sha256(runtime.read_bytes()).hexdigest(),'voices':8,'scope':'Chronos rage, wave and Kame opener only; Dracodia source, gain and pool untouched.'}
    (authored/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
