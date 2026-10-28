"""Re-encode the approved Clear masters; preserve pitch for the shorter gather."""
from pathlib import Path
import json,hashlib,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'_ART_SOURCES/chronos_energy_1026'
D=ROOT/'assets/game/shared/audio/chronos_energy_1026'

def main():
    ff=shutil.which('ffmpeg')
    if not ff:
        import imageio_ffmpeg
        ff=imageio_ffmpeg.get_ffmpeg_exe()
    D.mkdir(parents=True,exist_ok=True)
    subprocess.run([ff,'-v','error','-y','-i',str(A/'wave_charge.wav'),'-af','atempo=1.5294117647','-c:a','pcm_s24le',str(A/'gather_charge.wav')],check=True)
    records=[]
    for role in ['rage_charge','rage_release','wave_charge','gather_charge','wave_full','wave_tail']:
        master=A/(role+'.wav');runtime=D/(role+'.mp3')
        subprocess.run([ff,'-v','error','-y','-i',str(master),'-c:a','libmp3lame','-b:a','192k',str(runtime)],check=True)
        records.append({'role':role,'masterSha256':hashlib.sha256(master.read_bytes()).hexdigest(),'runtimeSha256':hashlib.sha256(runtime.read_bytes()).hexdigest()})
    (A/'encode-verification.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print('Encoded six native Chronos cues from retained lossless masters.')

if __name__=='__main__':main()
