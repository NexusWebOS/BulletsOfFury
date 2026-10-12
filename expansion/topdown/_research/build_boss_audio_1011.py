"""Ship Mike's original Stage 2 boss track without changing its mix."""
from pathlib import Path
import hashlib, json, subprocess, wave
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'expansion/topdown/audio'
source = OUT / 'source/BOF-O-BOSS1.wav'
target = OUT / 'BOF-O-BOSS1.mp3'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y',
                '-i', str(source), '-map_metadata', '-1', '-vn',
                '-c:a', 'libmp3lame', '-b:a', '256k', str(target)], check=True)
with wave.open(str(source)) as w:
    meta = {'durationSeconds': w.getnframes() / w.getframerate(),
            'sampleRate': w.getframerate(), 'channels': w.getnchannels()}
meta.update({'source': 'source/BOF-O-BOSS1.wav', 'runtime': target.name,
             'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
             'runtimeSha256': hashlib.sha256(target.read_bytes()).hexdigest(),
             'conversion': 'Stereo MP3 at 256 kbps; no gain, trim, fade or remix',
             'owner': 'Mike supplied BOF-O-BOSS1.wav on October 11, 2026'})
(OUT / 'boss1.json').write_text(json.dumps(meta, indent=2), encoding='utf-8', newline='\n')
print(f'Stage 2 boss track: {meta["durationSeconds"]:.2f}s, stereo, {target.stat().st_size} bytes')
