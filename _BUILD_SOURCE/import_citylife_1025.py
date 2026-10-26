"""Import Mike's full results track and update only its music manifest slot."""
from pathlib import Path
import re, subprocess
import imageio_ffmpeg

R = Path(__file__).resolve().parents[1]
source = Path('C:/Users/Mdogg/Desktop/music/citylife.wav')
target = 'assets/game/shared/audio/music/CityLife_StageClear_1025.mp3'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error',
                '-y', '-i', str(source), '-map', '0:a:0', '-c:a', 'libmp3lame',
                '-q:a', '2', str(R / target)], check=True)
manifest = R / 'assets/manifest.js'
data = manifest.read_bytes()
data, count = re.subn(rb'"stageclear":"[^"]+"',
                     ('"stageclear":"' + target + '"').encode(), data)
assert count == 1, count
manifest.write_bytes(data)
print(target)
