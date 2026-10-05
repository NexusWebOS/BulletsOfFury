"""Import Mike's Stage 7 boss theme; preserve the prior track and source WAV."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
MUSIC = ROOT / 'assets/game/music'
OUT = ROOT / '_shots/reaperman_0927'
SOURCE = Path('C:/Users/Mdogg/Desktop/reaperman.wav')
ORIGINAL = MUSIC / 'originals_0927/reaperman.wav'
OLD = MUSIC / 'boss7.mp3'
ARCHIVE = MUSIC / 'Level7mb.mp3'
TARGET = MUSIC / 'Level7b.mp3'
FF = imageio_ffmpeg.get_ffmpeg_exe()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stats(path):
    p = subprocess.run([FF, '-hide_banner', '-i', str(path), '-af', 'volumedetect',
                        '-f', 'null', '-'], capture_output=True, text=True, check=True)
    return {k: float(re.search(k + r':\s+(-?[\d.]+)', p.stderr).group(1))
            for k in ['mean_volume', 'max_volume']}

OUT.mkdir(parents=True, exist_ok=True)
assert SOURCE.is_file()
if OLD.exists():
    assert not ARCHIVE.exists(), 'Archive name already occupied; inspect before replacing.'
    old_hash = digest(OLD)
else:
    assert ARCHIVE.is_file()
    old_hash = digest(ARCHIVE)
old_stats = stats(OLD if OLD.exists() else ARCHIVE)
new_stats = stats(SOURCE)
gain = min(old_stats['mean_volume'] - new_stats['mean_volume'], -1 - new_stats['max_volume'])
ORIGINAL.parent.mkdir(exist_ok=True)
if not ORIGINAL.exists():
    shutil.copy2(SOURCE, ORIGINAL)
assert digest(ORIGINAL) == digest(SOURCE)
if not TARGET.exists():
    subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-n', '-i', str(SOURCE),
                    '-af', f'volume={gain:.3f}dB', '-ar', '44100', '-ac', '2',
                    '-b:a', '160k', str(TARGET)], check=True)
encoded_stats = stats(TARGET)
if OLD.exists():
    OLD.rename(ARCHIVE)
assert digest(ARCHIVE) == old_hash

# Own this small generated namespace through JSON, preserving other manifest data.
manifest = ROOT / 'assets/manifest.js'
src = manifest.read_text(encoding='utf-8')
start = src.index('window.BOFA=') + len('window.BOFA=')
obj, used = json.JSONDecoder().raw_decode(src[start:])
obj['music']['boss7'] = 'assets/game/music/' + TARGET.name
obj['music']['boss7mus'] = obj['music']['boss7']
obj['music']['unused13'] = 'assets/game/music/' + ARCHIVE.name
assert all((ROOT / v).is_file() for v in obj['music'].values())
manifest.write_text(src[:start] + json.dumps(obj, separators=(',', ':'), ensure_ascii=True)
                    + src[start + used:], encoding='utf-8', newline='\n')
report = {'source': str(SOURCE), 'preserved_source': ORIGINAL.relative_to(ROOT).as_posix(),
          'source_sha256': digest(SOURCE), 'active': TARGET.relative_to(ROOT).as_posix(),
          'archive': ARCHIVE.relative_to(ROOT).as_posix(), 'archive_sha256': old_hash,
          'old_levels_db': old_stats, 'input_levels_db': new_stats, 'gain_db': gain,
          'encoded_levels_db': encoded_stats}
(OUT / 'import.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
