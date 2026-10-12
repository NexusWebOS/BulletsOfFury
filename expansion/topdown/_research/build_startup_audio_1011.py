"""Preserve Mike's supplied startup WAV and export its browser playback copy."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import wave
import re
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'expansion/topdown/audio'
source = OUT / 'source/overdrive.wav'
target = OUT / 'overdrive-startup.mp3'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, help='Original supplied recording to import')
args = parser.parse_args()
source.parent.mkdir(parents=True, exist_ok=True)
if args.source and args.source.resolve() != source.resolve():
    supplied_hash = hashlib.sha256(args.source.read_bytes()).hexdigest()
    if source.exists() and hashlib.sha256(source.read_bytes()).hexdigest() != supplied_hash:
        raise SystemExit('A different source recording already exists; preserve it before replacing.')
    shutil.copyfile(args.source, source)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == supplied_hash

subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y',
                '-i', str(source), '-map_metadata', '-1', '-vn',
                '-c:a', 'libmp3lame', '-b:a', '256k', str(target)], check=True)
with wave.open(str(source)) as w:
    meta = {'durationSeconds': w.getnframes() / w.getframerate(),
            'sampleRate': w.getframerate(), 'channels': w.getnchannels(),
            'sampleWidthBytes': w.getsampwidth()}
meta.update({'source': 'source/overdrive.wav', 'runtime': target.name,
             'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
             'runtimeSha256': hashlib.sha256(target.read_bytes()).hexdigest(),
             'conversion': 'MP3 at 256 kbps; original channels/rate, no gain, trim, fade or remix',
             'owner': 'Mike supplied overdrive.wav on October 11, 2026'})
(OUT / 'startup.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8', newline='\n')
print(f'Overdrive startup: {meta["durationSeconds"]:.3f}s, {meta["channels"]} channels, {target.stat().st_size} bytes')

# Match Mike's original title call's measured loudness; keep his natural pitch.
# The room taps provide short reverb, with two longer arcade echo reflections.
reference=ROOT/'assets/game/shared/audio/sounds/announce.mp3'
enhanced=OUT/'overdrive-reverb_1011.mp3'
preview=OUT/'overdrive-intro-preview_1011.mp3'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
def loudness(path,filters=''):
    chain=(filters+',' if filters else '')+'loudnorm=print_format=json'
    result=subprocess.run([ffmpeg,'-v','info','-i',str(path),'-af',chain,'-f','null','-'],capture_output=True,text=True,check=True)
    return json.loads(re.findall(r'\{\s*"input_i".*?\}',result.stderr,re.S)[-1])
ref=loudness(reference)
room='highpass=f=50,lowpass=f=11500,aecho=0.9:1:65|109|157|223|337|461|674|912:0.1|0.08|0.06|0.05|0.22|0.14|0.09|0.05'
measured=loudness(source,room)
norm=f'loudnorm=I={ref["input_i"]}:TP=-1.2:LRA=11:measured_I={measured["input_i"]}:measured_TP={measured["input_tp"]}:measured_LRA={measured["input_lra"]}:measured_thresh={measured["input_thresh"]}:offset={measured["target_offset"]}:linear=true'
subprocess.run([ffmpeg,'-v','error','-y','-i',str(source),'-af',room+','+norm,'-ar','44100','-c:a','libmp3lame','-b:a','256k',str(enhanced)],check=True)
subprocess.run([ffmpeg,'-v','error','-y','-i',str(reference),'-i',str(enhanced),'-filter_complex','[0:a]aformat=sample_rates=44100:channel_layouts=stereo[a];[1:a]aformat=sample_rates=44100:channel_layouts=stereo[b];[a][b]concat=n=2:v=0:a=1[out]','-map','[out]','-c:a','libmp3lame','-b:a','256k',str(preview)],check=True)
recipe={'date':'2026-10-11','owner':'Mike requested the original BOF call followed by his Overdrive recording with matching reverb/echo',
        'reference':str(reference.relative_to(ROOT)).replace('\\','/'),'referenceSha256':hashlib.sha256(reference.read_bytes()).hexdigest(),
        'source':meta['source'],'sourceSha256':meta['sourceSha256'],
        'runtime':enhanced.name,'runtimeSha256':hashlib.sha256(enhanced.read_bytes()).hexdigest(),
        'preview':preview.name,'roomFilter':room,'normalizationFilter':norm,
        'referenceLoudness':ref,'processedLoudness':loudness(enhanced),
        'pitch':'Unchanged, playback rate 1; no generated or substituted voice',
        'order':['Original announce.mp3','Enhanced overdrive-reverb_1011.mp3'],
        'timing':'Second call starts on the first media ended event; title music waits for the final echo tail'}
(OUT/'startup_reverb_1011.json').write_text(json.dumps(recipe,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Enhanced Overdrive: reference '+ref['input_i']+' LUFS, output '+recipe['processedLoudness']['input_i']+' LUFS; reverb/echo tail retained')
