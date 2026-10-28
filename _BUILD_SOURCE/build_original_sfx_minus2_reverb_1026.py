"""Encode the retained, approved minus-two-semitone/reverb lossless masters."""
from pathlib import Path
import json,shutil,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'_ART_SOURCES/original_sfx_minus2_reverb_1026'
D=ROOT/'assets/game/shared/audio/original_sfx_minus2_reverb_1026'
def main():
    ff=shutil.which('ffmpeg')
    if not ff:
        import imageio_ffmpeg
        ff=imageio_ffmpeg.get_ffmpeg_exe()
    manifest=json.loads((A/'manifest.json').read_text(encoding='utf-8'));D.mkdir(parents=True,exist_ok=True)
    for item in manifest['files']:
        master=A/Path(item['master']).name;dest=D/Path(item['runtime']).name
        subprocess.run([ff,'-v','error','-y','-i',str(master),'-c:a','libmp3lame','-b:a','192k',str(dest)],check=True)
        item['runtimeSha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
    (A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Encoded all eight approved recordings without further audio treatments.')
if __name__=='__main__':main()
