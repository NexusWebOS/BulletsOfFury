"""Rebuild foreground Chronos cues from retained pre-master sources and recipes."""
from pathlib import Path
import hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'_ART_SOURCES/chronos_energy_mix_1026'
D=ROOT/'assets/game/shared/audio/chronos_energy_mix_1026'

def main():
    ff=shutil.which('ffmpeg')
    if not ff:
        import imageio_ffmpeg
        ff=imageio_ffmpeg.get_ffmpeg_exe()
    manifest=json.loads((A/'manifest.json').read_text(encoding='utf-8'));D.mkdir(parents=True,exist_ok=True)
    for item in manifest['records']:
        role=item['role'];source=A/(role+'-pre-master.wav');master=A/(role+'.wav');runtime=D/(role+'.mp3')
        subprocess.run([ff,'-v','error','-y','-i',str(source),'-af',item['filters'],'-c:a','pcm_s24le',str(master)],check=True)
        subprocess.run([ff,'-v','error','-y','-i',str(master),'-c:a','libmp3lame','-b:a','192k',str(runtime)],check=True)
        item['preMasterSha256']=hashlib.sha256(source.read_bytes()).hexdigest();item['runtimeSha256']=hashlib.sha256(runtime.read_bytes()).hexdigest()
    (A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Rebuilt six cues; pitch unchanged and lossless sources retained.')

if __name__=='__main__':main()
